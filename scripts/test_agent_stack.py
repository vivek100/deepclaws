"""Smoke-test Ghost tools and optional Tinker inference for the agent stack."""

from __future__ import annotations

import argparse
import os

from dotenv import load_dotenv

from agent.agent import run_question
from agent.tools import ghost_schema, ghost_sql

load_dotenv()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db-id", required=True, help="Ghost database ID.")
    parser.add_argument("--schema", required=True, help="Target schema name.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("== ghost_schema smoke ==")
    print(ghost_schema.func(args.db_id, args.schema))

    print("\n== ghost_sql smoke ==")
    print(ghost_sql.func(args.db_id, args.schema, "SELECT COUNT(*) AS signals_count FROM signals;"))

    if not os.getenv("TINKER_API_KEY") or not os.getenv("TINKER_MODEL_PATH"):
        print("\n== agent inference smoke ==")
        print("SKIP: TINKER_API_KEY or TINKER_MODEL_PATH is not set.")
        return

    print("\n== agent inference smoke ==")
    result = run_question(
        question="How many signals are there?",
        db_id=args.db_id,
        schema_name=args.schema,
    )
    print(result)


if __name__ == "__main__":
    main()
