"""Run the current baseline evaluation slice."""

from __future__ import annotations

import argparse
import json

from pipeline.run_baseline import run_baseline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default="eval/dataset.json", help="Path to local eval rows.")
    parser.add_argument("--db-id", required=True, help="Ghost database ID to query.")
    parser.add_argument("--schema", required=True, help="Schema name to target.")
    parser.add_argument("--iteration", default="iteration_001", help="Experiment output folder name.")
    parser.add_argument("--limit", type=int, default=None, help="Optional max number of rows to run.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_baseline(
        dataset_path=args.dataset,
        db_id=args.db_id,
        schema_name=args.schema,
        iteration_id=args.iteration,
        limit=args.limit,
    )
    print(json.dumps(result["metadata"], indent=2))
    print()
    print(result["summary"])


if __name__ == "__main__":
    main()
