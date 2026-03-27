"""Minimal LiteLLM bind_tools smoke test for Kimi via Tinker's OAI endpoint."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()


@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


def main() -> None:
    api_key = os.getenv("TINKER_API_KEY")
    model = os.getenv("TINKER_MODEL_PATH")
    api_base = os.getenv(
        "TINKER_BASE_URL",
        "https://tinker.thinkingmachines.dev/services/tinker-prod/oai/api/v1",
    )

    if not api_key or not model:
        raise RuntimeError("TINKER_API_KEY and TINKER_MODEL_PATH must be set.")

    from langchain_litellm import ChatLiteLLM

    llm = ChatLiteLLM(
        model="openai/" + model,
        api_base=api_base,
        api_key=api_key,
        temperature=0.0,
        max_tokens=512,
    )
    llm_with_tools = llm.bind_tools([add])
    response = llm_with_tools.invoke("What is 17 + 25? Use the add tool.")
    print("content:", response.content)
    print("tool_calls:", response.tool_calls)


if __name__ == "__main__":
    main()
