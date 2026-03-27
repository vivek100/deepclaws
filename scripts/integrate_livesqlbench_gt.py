"""Merge public LiveSQLBench rows with the protected GT JSONL by instance_id."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-dataset", default="eval/dataset.json", help="Path to public JSON dataset.")
    parser.add_argument(
        "--gt-jsonl",
        default="data/livesqlbench/livesqlbench_gt_kg_testcases_0528.jsonl",
        help="Path to GT JSONL file received from LiveSQLBench.",
    )
    parser.add_argument(
        "--output",
        default="eval/dataset.gt.json",
        help="Path to write the merged canonical dataset.",
    )
    return parser.parse_args()


def load_gt_map(path: Path) -> dict[str, dict]:
    gt_map: dict[str, dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        gt_map[row["instance_id"]] = row
    return gt_map


def main() -> None:
    args = parse_args()
    public_rows = json.loads(Path(args.public_dataset).read_text(encoding="utf-8"))
    gt_map = load_gt_map(Path(args.gt_jsonl))

    merged = []
    missing = []
    for row in public_rows:
        instance_id = row["instance_id"]
        gt = gt_map.get(instance_id)
        if gt is None:
            missing.append(instance_id)
            merged.append(row)
            continue
        merged_row = dict(row)
        merged_row["sol_sql"] = gt.get("sol_sql", [])
        merged_row["external_knowledge"] = gt.get("external_knowledge", [])
        merged_row["test_cases"] = gt.get("test_cases", [])
        merged.append(merged_row)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(merged, indent=2), encoding="utf-8")

    print(f"Wrote {len(merged)} merged rows to {output}")
    if missing:
        print(f"Missing GT rows for {len(missing)} instance(s): {', '.join(missing[:10])}")


if __name__ == "__main__":
    main()
