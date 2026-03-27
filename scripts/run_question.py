"""Run one question through the SQL agent."""

from __future__ import annotations

import argparse
import json

from dotenv import load_dotenv

from agent.agent import run_question

load_dotenv()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db-id", required=True, help="Ghost database ID.")
    parser.add_argument("--schema", required=True, help="Target schema name.")
    parser.add_argument("--question", required=True, help="Natural-language question.")
    parser.add_argument("--evidence", default="", help="Optional extra benchmark knowledge.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_question(
        question=args.question,
        db_id=args.db_id,
        schema_name=args.schema,
        evidence=args.evidence,
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
