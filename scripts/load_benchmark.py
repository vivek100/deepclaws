"""Load a SQLite benchmark database into Postgres/Ghost under a target schema."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sqlite-path", required=True, help="Path to the SQLite template file.")
    parser.add_argument("--postgres-url", required=True, help="Postgres connection string.")
    parser.add_argument("--schema", required=True, help="Target Postgres schema name.")
    parser.add_argument(
        "--drop-schema",
        action="store_true",
        help="Drop and recreate the target schema before loading.",
    )
    return parser.parse_args()


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
    if "DATE" in normalized or "TIME" in normalized:
        return "TEXT"
    if "BLOB" in normalized:
        return "BYTEA"
    return "TEXT"


def iter_tables(conn: sqlite3.Connection) -> list[str]:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
    )
    return [row[0] for row in cur.fetchall()]


def table_columns(conn: sqlite3.Connection, table_name: str) -> list[tuple[str, str]]:
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info([{table_name}])")
    return [(row[1], row[2]) for row in cur.fetchall()]


def create_table(
    pg_cur: psycopg2.extensions.cursor,
    schema_name: str,
    table_name: str,
    columns: list[tuple[str, str]],
) -> None:
    column_defs = [
        sql.SQL("{} {}").format(sql.Identifier(col_name), sql.SQL(map_sqlite_type(col_type)))
        for col_name, col_type in columns
    ]
    stmt = sql.SQL("CREATE TABLE {}.{} ({})").format(
        sql.Identifier(schema_name),
        sql.Identifier(table_name),
        sql.SQL(", ").join(column_defs),
    )
    pg_cur.execute(stmt)


def copy_rows(
    sqlite_conn: sqlite3.Connection,
    pg_cur: psycopg2.extensions.cursor,
    schema_name: str,
    table_name: str,
    columns: list[tuple[str, str]],
) -> int:
    col_names = [name for name, _ in columns]
    sqlite_cur = sqlite_conn.cursor()
    sqlite_cur.execute(f"SELECT * FROM [{table_name}]")
    rows = sqlite_cur.fetchall()
    if not rows:
        return 0

    insert_stmt = sql.SQL("INSERT INTO {}.{} ({}) VALUES %s").format(
        sql.Identifier(schema_name),
        sql.Identifier(table_name),
        sql.SQL(", ").join(sql.Identifier(name) for name in col_names),
    )
    execute_values(pg_cur, insert_stmt.as_string(pg_cur), rows, page_size=500)
    return len(rows)


def main() -> None:
    args = parse_args()
    sqlite_path = Path(args.sqlite_path)
    if not sqlite_path.exists():
        raise FileNotFoundError(f"SQLite file not found: {sqlite_path}")

    sqlite_conn = sqlite3.connect(str(sqlite_path))
    pg_conn = psycopg2.connect(args.postgres_url)
    pg_conn.autocommit = False
    pg_cur = pg_conn.cursor()

    try:
        if args.drop_schema:
            pg_cur.execute(
                sql.SQL("DROP SCHEMA IF EXISTS {} CASCADE").format(sql.Identifier(args.schema))
            )
        pg_cur.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(args.schema)))

        loaded_counts: list[tuple[str, int]] = []
        for table_name in iter_tables(sqlite_conn):
            columns = table_columns(sqlite_conn, table_name)
            pg_cur.execute(
                sql.SQL("DROP TABLE IF EXISTS {}.{} CASCADE").format(
                    sql.Identifier(args.schema),
                    sql.Identifier(table_name),
                )
            )
            create_table(pg_cur, args.schema, table_name, columns)
            row_count = copy_rows(sqlite_conn, pg_cur, args.schema, table_name, columns)
            loaded_counts.append((table_name, row_count))
            print(f"Loaded {table_name}: {row_count} rows")

        pg_conn.commit()
    except Exception:
        pg_conn.rollback()
        raise
    finally:
        pg_cur.close()
        pg_conn.close()
        sqlite_conn.close()

    print(f"Loaded schema '{args.schema}' from {sqlite_path}")
    for table_name, row_count in loaded_counts:
        print(f"- {table_name}: {row_count} rows")


if __name__ == "__main__":
    main()
