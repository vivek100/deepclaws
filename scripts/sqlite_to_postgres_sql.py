"""Generate a Postgres-compatible SQL load script from a SQLite benchmark DB."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sqlite-path", required=True, help="Path to the SQLite database file.")
    parser.add_argument("--output", required=True, help="Path to write the generated SQL script.")
    parser.add_argument("--schema", required=True, help="Target Postgres schema name.")
    parser.add_argument(
        "--drop-schema",
        action="store_true",
        help="Drop and recreate the target schema in the generated SQL.",
    )
    parser.add_argument(
        "--table",
        action="append",
        dest="tables",
        help="Optional table filter. Can be provided multiple times.",
    )
    parser.add_argument(
        "--row-limit",
        type=int,
        default=None,
        help="Optional per-table row limit for smoke tests.",
    )
    return parser.parse_args()


def quote_ident(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


def quote_literal(value: object) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, bytes):
        return "'\\x" + value.hex() + "'"
    return "'" + str(value).replace("\\", "\\\\").replace("'", "''") + "'"


def map_sqlite_type(type_name: str) -> str:
    normalized = (type_name or "").upper()
    if "INT" in normalized:
        return "BIGINT"
    if any(token in normalized for token in ("REAL", "FLOA", "DOUB")):
        return "DOUBLE PRECISION"
    if "NUM" in normalized or "DEC" in normalized:
        return "NUMERIC"
    if "BOOL" in normalized:
        return "BOOLEAN"
    if "BLOB" in normalized:
        return "BYTEA"
    return "TEXT"


def iter_tables(conn: sqlite3.Connection, only_tables: set[str] | None) -> list[str]:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
    )
    tables = [row[0] for row in cur.fetchall()]
    if only_tables is None:
        return tables
    return [table for table in tables if table in only_tables]


def table_columns(conn: sqlite3.Connection, table_name: str) -> list[tuple[str, str]]:
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info([{table_name}])")
    return [(row[1], row[2]) for row in cur.fetchall()]


def table_rows(
    conn: sqlite3.Connection, table_name: str, row_limit: int | None
) -> list[tuple[object, ...]]:
    cur = conn.cursor()
    query = f"SELECT * FROM [{table_name}]"
    if row_limit is not None:
        query += f" LIMIT {row_limit}"
    cur.execute(query)
    return cur.fetchall()


def build_script(
    conn: sqlite3.Connection,
    schema_name: str,
    only_tables: set[str] | None,
    row_limit: int | None,
    drop_schema: bool,
) -> str:
    lines: list[str] = []
    lines.append("BEGIN;")
    lines.append("SET client_min_messages TO WARNING;")
    if drop_schema:
        lines.append(f"DROP SCHEMA IF EXISTS {quote_ident(schema_name)} CASCADE;")
    lines.append(f"CREATE SCHEMA IF NOT EXISTS {quote_ident(schema_name)};")
    lines.append("")

    for table_name in iter_tables(conn, only_tables):
        columns = table_columns(conn, table_name)
        column_defs = ", ".join(
            f"{quote_ident(col_name)} {map_sqlite_type(col_type)}"
            for col_name, col_type in columns
        )
        lines.append(
            f"DROP TABLE IF EXISTS {quote_ident(schema_name)}.{quote_ident(table_name)} CASCADE;"
        )
        lines.append(
            f"CREATE TABLE {quote_ident(schema_name)}.{quote_ident(table_name)} ({column_defs});"
        )

        rows = table_rows(conn, table_name, row_limit)
        if rows:
            col_list = ", ".join(quote_ident(name) for name, _ in columns)
            value_chunks = []
            for row in rows:
                literals = ", ".join(quote_literal(value) for value in row)
                value_chunks.append(f"({literals})")
            lines.append(
                f"INSERT INTO {quote_ident(schema_name)}.{quote_ident(table_name)} ({col_list}) VALUES"
            )
            lines.append(",\n".join(value_chunks) + ";")
        lines.append("")

    lines.append("COMMIT;")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    sqlite_path = Path(args.sqlite_path)
    if not sqlite_path.exists():
        raise FileNotFoundError(f"SQLite file not found: {sqlite_path}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    only_tables = set(args.tables) if args.tables else None

    conn = sqlite3.connect(str(sqlite_path))
    try:
        script = build_script(
            conn=conn,
            schema_name=args.schema,
            only_tables=only_tables,
            row_limit=args.row_limit,
            drop_schema=args.drop_schema,
        )
    finally:
        conn.close()

    output_path.write_text(script, encoding="utf-8")
    print(f"Wrote SQL load script to {output_path}")


if __name__ == "__main__":
    main()
