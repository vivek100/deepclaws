"""LLM creation for the Ghost SQL agent."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


def create_llm():
    """Create the LangChain chat model for the agent."""
    api_key = os.getenv("TINKER_API_KEY")
    model = os.getenv("TINKER_MODEL_PATH")
    base_url = os.getenv(
        "TINKER_BASE_URL",
        "https://tinker.thinkingmachines.dev/services/tinker-prod/oai/api/v1",
    )

    if not api_key:
        raise RuntimeError("TINKER_API_KEY is not set.")
    if not model:
        raise RuntimeError("TINKER_MODEL_PATH is not set.")

    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=model,
        base_url=base_url,
        api_key=api_key,
        temperature=0.0,
    )
