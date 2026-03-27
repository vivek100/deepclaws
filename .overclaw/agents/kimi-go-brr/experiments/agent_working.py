"""Overclaw-compatible entrypoint for the SQL agent."""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

from agent.agent import run_question
from eval.score import extract_final_sql

load_dotenv()


def run(input: dict[str, Any]) -> dict[str, Any]:
    """Run the SQL agent with an Overclaw-compatible dict-in/dict-out signature."""
    question = str(input.get("question", "")).strip()
    if not question:
        raise ValueError("input.question is required")

    db_id = str(input.get("db_id") or os.getenv("GHOST_MAIN_DB_ID", "")).strip()
    if not db_id:
        raise ValueError("input.db_id or GHOST_MAIN_DB_ID is required")

    schema_name = str(input.get("schema") or input.get("schema_name") or "").strip()
    if not schema_name:
        raise ValueError("input.schema is required")

    evidence = str(input.get("evidence", "")).strip()
    agent_result = run_question(
        question=question,
        db_id=db_id,
        schema_name=schema_name,
        evidence=evidence,
    )

    final_sql = extract_final_sql(agent_result)
    return {
        "final_sql": final_sql,
        "has_sql": bool(final_sql),
        "schema_name": schema_name,
    }
