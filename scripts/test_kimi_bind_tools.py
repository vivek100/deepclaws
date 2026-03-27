"""Minimal bind_tools smoke test for Kimi on Tinker's OpenAI-compatible endpoint."""

from __future__ import annotations

from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda

from agent.llm import create_llm
from agent.kimi_compat import maybe_parse_kimi_tool_calls

load_dotenv()

from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


def main() -> None:
    llm = create_llm()
    llm_with_tools = llm.bind_tools([add])
    response = llm_with_tools.invoke("What is 17 + 25? Use the add tool.")
    print("raw content:", response.content)
    print("raw tool_calls:", response.tool_calls)

    compat = llm_with_tools | RunnableLambda(maybe_parse_kimi_tool_calls)
    compat_response = compat.invoke("What is 17 + 25? Use the add tool.")
    print("compat content:", compat_response.content)
    print("compat tool_calls:", compat_response.tool_calls)


if __name__ == "__main__":
    main()
