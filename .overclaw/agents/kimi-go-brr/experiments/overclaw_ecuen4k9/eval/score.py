"""Evaluation helpers for baseline SQL-agent runs."""

from __future__ import annotations

import re
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage

from agent.tools import ghost_sql


SQL_BLOCK_RE = re.compile(r"```sql\s*(.*?)```", re.IGNORECASE | re.DOTALL)
SQL_STATEMENT_RE = re.compile(
    r"(?is)\b(with|select|insert|update|delete)\b.*?;",
)


def extract_messages(result: dict[str, Any]) -> list[BaseMessage]:
    """Return LangGraph messages from an agent result payload."""
    messages = result.get("messages", [])
    return [message for message in messages if isinstance(message, BaseMessage)]


def extract_final_text(result: dict[str, Any]) -> str:
    """Return the last AI message content as plain text."""
    messages = extract_messages(result)
    for message in reversed(messages):
        if isinstance(message, AIMessage):
            content = message.content
            return content if isinstance(content, str) else str(content)
    return ""


def extract_final_sql(result: dict[str, Any]) -> str:
    """Extract the final SQL block or final SQL-looking statement."""
    text = extract_final_text(result)
    if not text:
        return ""

    sql_blocks = SQL_BLOCK_RE.findall(text)
    if sql_blocks:
        return sql_blocks[-1].strip()

    statements = SQL_STATEMENT_RE.findall(text)
    if statements:
        last_match = None
        for match in SQL_STATEMENT_RE.finditer(text):
            last_match = match
        if last_match is not None:
            return last_match.group(0).strip()

    return ""


def execute_sql(database_id: str, schema_name: str, sql: str) -> tuple[bool, str]:
    """Execute SQL with the Ghost tool wrapper and return success plus output."""
    if not sql.strip():
        return False, "No SQL extracted from agent output."

    try:
        output = ghost_sql.func(database_id=database_id, schema=schema_name, query=sql)
    except Exception as exc:  # pragma: no cover - defensive wrapper
        return False, f"{type(exc).__name__}: {exc}"
    return True, output


def score_single(predicted_sql: str, gold_sql: str) -> bool | None:
    """Return exact SQL match when gold SQL exists, otherwise None."""
    if not gold_sql.strip():
        return None
    return predicted_sql.strip() == gold_sql.strip()
