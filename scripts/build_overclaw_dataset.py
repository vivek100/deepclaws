"""Build a small Overclaw dataset from the canonical LiveSQLBench dataset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="eval/dataset.gt.json", help="Canonical merged eval dataset.")
    parser.add_argument(
        "--output",
        default=".overclaw/agents/kimi-go-brr/setup_spec/dataset.json",
        help="Output path for Overclaw dataset.json.",
    )
    parser.add_argument("--db-id", required=True, help="Actual Ghost database ID to use at runtime.")
    parser.add_argument("--schema", required=True, help="Schema name to target.")
    parser.add_argument("--limit", type=int, default=5, help="Number of rows to keep.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = json.loads(Path(args.source).read_text(encoding="utf-8"))
    subset = rows[: args.limit]

    overclaw_rows = []
    for row in subset:
        gold_sqls = row.get("sol_sql", []) or []
        if not gold_sqls:
            continue
        overclaw_rows.append(
            {
                "input": {
                    "question": row["question"],
                    "db_id": args.db_id,
                    "schema": args.schema,
                    "evidence": json.dumps(row.get("external_knowledge", [])),
                },
                "expected_output": {
                    "final_sql": gold_sqls[0],
                    "has_sql": True,
                    "schema_name": args.schema,
                },
                "metadata": {
                    "instance_id": row["instance_id"],
                    "difficulty": row.get("difficulty", ""),
                    "category": row.get("category", ""),
                },
            }
        )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(overclaw_rows, indent=2), encoding="utf-8")
    print(f"Wrote {len(overclaw_rows)} Overclaw cases to {output}")


if __name__ == "__main__":
    main()
