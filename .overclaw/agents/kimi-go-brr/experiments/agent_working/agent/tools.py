"""Ghost tool wrappers for the SQL agent."""

from __future__ import annotations

import subprocess

from langchain_core.tools import tool


GHOST_EXE = r"C:\Users\shukl\AppData\Local\Programs\Ghost\ghost.exe"


def _run_ghost(args: list[str], stdin_text: str | None = None) -> str:
    result = subprocess.run(
        [GHOST_EXE, *args],
        input=stdin_text,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Ghost command failed.")
    return result.stdout.strip()


@tool
def ghost_list() -> str:
    """List available Ghost databases."""
    return _run_ghost(["list"])


@tool
def ghost_connect(database_id: str) -> str:
    """Get the connection string for a Ghost database by ID."""
    return _run_ghost(["connect", database_id])


@tool
def ghost_schema(database_id: str, schema: str) -> str:
    """Return tables and columns for a specific schema in a Ghost database."""
    query = f"""
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = '{schema}'
    ORDER BY table_name, ordinal_position;
    """
    return _run_ghost(["sql", database_id, query])


@tool
def ghost_sql(database_id: str, schema: str, query: str) -> str:
    """Execute SQL against a specific schema in a Ghost database."""
    full_query = f'SET search_path TO "{schema}"; {query}'
    return _run_ghost(["sql", database_id, full_query])
