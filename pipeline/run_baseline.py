"""Run a baseline evaluation slice and save artifacts."""

from __future__ import annotations

import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from agent.agent import run_question
from agent.prompts import SQL_SYSTEM_PROMPT
from eval.score import execute_sql, extract_final_sql, score_single


@dataclass
class EvalResult:
    instance_id: str
    schema_name: str
    question: str
    predicted_sql: str
    executable_success: bool
    exact_match: bool | None
    execution_output: str
    error: str
    difficulty: str
    category: str


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _git_sha() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return "unknown"
    return result.stdout.strip()


def _load_rows(dataset_path: str, limit: int | None) -> list[dict[str, Any]]:
    rows = json.loads(Path(dataset_path).read_text(encoding="utf-8"))
    if limit is None:
        return rows
    return rows[:limit]


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _render_summary(
    *,
    iteration_id: str,
    dataset_path: str,
    db_id: str,
    schema_name: str,
    total: int,
    executable_passes: int,
    exact_scored: int,
    exact_passes: int,
) -> str:
    executable_rate = (executable_passes / total * 100.0) if total else 0.0
    exact_rate = (exact_passes / exact_scored * 100.0) if exact_scored else None
    exact_line = (
        f"- Exact benchmark accuracy: {exact_rate:.1f}% ({exact_passes}/{exact_scored})"
        if exact_rate is not None
        else "- Exact benchmark accuracy: unavailable in local dataset slice (no gold SQL/test cases)"
    )
    return "\n".join(
        [
            f"# {iteration_id} Baseline",
            "",
            f"- Timestamp (UTC): {_utc_now()}",
            f"- Git SHA: `{_git_sha()}`",
            f"- Dataset: `{dataset_path}`",
            f"- Ghost database ID: `{db_id}`",
            f"- Schema: `{schema_name}`",
            f"- Questions run: {total}",
            f"- Executable success: {executable_rate:.1f}% ({executable_passes}/{total})",
            exact_line,
            "",
            "This phase records an operational baseline. The public LiveSQLBench Lite slice on disk does not expose gold SQL or test cases, so executable success is the tracked metric until the private evaluation package is added.",
        ]
    )


def run_baseline(
    *,
    dataset_path: str,
    db_id: str,
    schema_name: str,
    iteration_id: str,
    limit: int | None = None,
) -> dict[str, Any]:
    load_dotenv(".env")

    rows = _load_rows(dataset_path, limit)
    experiment_dir = Path("experiments") / iteration_id
    _ensure_dir(experiment_dir)

    results: list[EvalResult] = []
    exact_scored = 0
    exact_passes = 0

    for row in rows:
        evidence = "; ".join(row.get("external_knowledge", []))
        error = ""
        try:
            agent_result = run_question(
                question=row["question"],
                db_id=db_id,
                schema_name=schema_name,
                evidence=evidence,
            )
            predicted_sql = extract_final_sql(agent_result)
            executable_success, execution_output = execute_sql(db_id, schema_name, predicted_sql)
        except Exception as exc:  # pragma: no cover - runtime guard
            agent_result = {}
            predicted_sql = ""
            executable_success = False
            execution_output = ""
            error = f"{type(exc).__name__}: {exc}"

        gold_sql_candidates = row.get("sol_sql", []) or []
        gold_sql = gold_sql_candidates[0] if gold_sql_candidates else ""
        exact_match = score_single(predicted_sql, gold_sql)
        if exact_match is not None:
            exact_scored += 1
            if exact_match:
                exact_passes += 1

        results.append(
            EvalResult(
                instance_id=row["instance_id"],
                schema_name=schema_name,
                question=row["question"],
                predicted_sql=predicted_sql,
                executable_success=executable_success,
                exact_match=exact_match,
                execution_output=execution_output,
                error=error,
                difficulty=row.get("difficulty", ""),
                category=row.get("category", ""),
            )
        )

    total = len(results)
    executable_passes = sum(1 for item in results if item.executable_success)

    metadata = {
        "iteration_id": iteration_id,
        "created_at_utc": _utc_now(),
        "git_sha": _git_sha(),
        "dataset_path": dataset_path,
        "ghost_database_id": db_id,
        "schema_name": schema_name,
        "question_count": total,
        "metrics": {
            "primary_metric": "executable_success_rate",
            "exact_accuracy_available": exact_scored > 0,
        },
    }
    summary = _render_summary(
        iteration_id=iteration_id,
        dataset_path=dataset_path,
        db_id=db_id,
        schema_name=schema_name,
        total=total,
        executable_passes=executable_passes,
        exact_scored=exact_scored,
        exact_passes=exact_passes,
    )

    (experiment_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    (experiment_dir / "results.json").write_text(
        json.dumps([asdict(result) for result in results], indent=2),
        encoding="utf-8",
    )
    (experiment_dir / "summary.md").write_text(summary, encoding="utf-8")
    (experiment_dir / "prompt.txt").write_text(SQL_SYSTEM_PROMPT, encoding="utf-8")

    return {
        "metadata": metadata,
        "results": [asdict(result) for result in results],
        "summary": summary,
        "executable_success_rate": (executable_passes / total) if total else 0.0,
        "exact_accuracy_rate": (exact_passes / exact_scored) if exact_scored else None,
    }
