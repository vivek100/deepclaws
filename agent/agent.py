"""Agent entrypoint."""

from __future__ import annotations

from agent.prompts import SQL_SYSTEM_PROMPT


def run_question(question: str, db_name: str, evidence: str = "") -> dict:
    return {
        "question": question,
        "db_name": db_name,
        "evidence": evidence,
        "system_prompt": SQL_SYSTEM_PROMPT,
        "status": "Phase 3 implementation pending.",
    }
