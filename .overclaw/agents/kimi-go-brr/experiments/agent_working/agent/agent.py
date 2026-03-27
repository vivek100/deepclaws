"""Agent entrypoint."""

from __future__ import annotations

from dotenv import load_dotenv

from agent.llm import create_llm
from agent.prompts import SQL_SYSTEM_PROMPT
from agent.react import build_react_agent
from agent.tools import ghost_connect, ghost_list, ghost_schema, ghost_sql

load_dotenv()


def create_agent():
    """Create the LangGraph ReAct agent harness."""
    llm = create_llm()
    return build_react_agent(
        llm=llm,
        tools=[ghost_list, ghost_connect, ghost_schema, ghost_sql],
        system_prompt=SQL_SYSTEM_PROMPT,
    )


def run_question(question: str, db_id: str, schema_name: str, evidence: str = "") -> dict:
    agent = create_agent()
    prompt = f"""
Target Ghost database ID: {db_id}
Target schema: {schema_name}
Question: {question}
External knowledge: {evidence or "None"}

Inspect the schema first, then write and validate SQL against the target schema.
Return the final SQL and the answer summary.
"""
    return agent.invoke({"messages": [{"role": "user", "content": prompt}]})
