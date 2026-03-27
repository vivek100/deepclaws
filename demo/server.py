"""FastAPI demo server for the Ghost + Overclaw SQL-agent flow."""

from __future__ import annotations

import json
import os
import queue
import re
import subprocess
import threading
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agent.overclaw_agent import run as run_overclaw_agent

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web"
DATASET_PATH = ROOT / "eval" / "dataset.gt.json"
OVERCLAW_DATASET_PATH = ROOT / ".overclaw" / "agents" / "kimi-go-brr" / "setup_spec" / "dataset.json"
OVERCLAW_EXPERIMENTS_DIR = ROOT / ".overclaw" / "agents" / "kimi-go-brr" / "experiments"
GHOST_EXE = Path(r"C:\Users\shukl\AppData\Local\Programs\Ghost\ghost.exe")

QUESTION_ROW_RE = re.compile(r"^(?P<id>[a-z0-9]+)\s+(?P<name>\S+)\s+", re.IGNORECASE)

app = FastAPI(title="deepclaws demo")
app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")


@dataclass
class RunState:
    run_id: str
    instance_id: str
    status: str = "queued"
    phase: str = "queued"
    logs: list[str] = field(default_factory=list)
    fork_db_id: str | None = None
    fork_name: str | None = None
    final_sql: str | None = None
    artifacts: dict[str, str] = field(default_factory=dict)
    error: str | None = None
    queue: queue.Queue[str] = field(default_factory=queue.Queue)


class RunRequest(BaseModel):
    instance_id: str


RUNS: dict[str, RunState] = {}


def emit(run: RunState, message: str) -> None:
    stamped = f"[{time.strftime('%H:%M:%S')}] {message}"
    run.logs.append(stamped)
    run.queue.put(stamped)


def load_questions() -> list[dict[str, Any]]:
    rows = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    return rows


def find_question(instance_id: str) -> dict[str, Any]:
    for row in load_questions():
        if row["instance_id"] == instance_id:
            return row
    raise KeyError(instance_id)


def _run_command(args: list[str], *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def list_ghost_databases() -> list[dict[str, str]]:
    result = _run_command([str(GHOST_EXE), "list"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "ghost list failed")

    rows = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("ID") or line.startswith("-"):
            continue
        parts = re.split(r"\s{2,}", line)
        if len(parts) >= 2:
            rows.append({"id": parts[0], "name": parts[1]})
    return rows


def resolve_main_db_id() -> str:
    configured = os.getenv("GHOST_MAIN_DB_ID", "").strip()
    if configured:
        return configured
    for row in list_ghost_databases():
        if row["name"] == "livesqlbench-main":
            return row["id"]
    raise RuntimeError("Could not resolve Ghost main DB ID. Set GHOST_MAIN_DB_ID.")


def create_ghost_fork(run: RunState) -> str:
    main_id = resolve_main_db_id()
    fork_name = f"deepclaws-{run.run_id[:8]}"
    run.fork_name = fork_name
    emit(run, f"Forking Ghost DB `{main_id}` as `{fork_name}`")
    before = {row["id"] for row in list_ghost_databases()}
    result = _run_command([str(GHOST_EXE), "fork", main_id, "--name", fork_name, "--wait"])
    emit(run, result.stdout.strip() or "ghost fork completed")
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ghost fork failed")

    for row in list_ghost_databases():
        if row["name"] == fork_name and row["id"] not in before:
            return row["id"]
    for row in list_ghost_databases():
        if row["name"] == fork_name:
            return row["id"]
    raise RuntimeError("Could not find forked Ghost database in ghost list output.")


def write_overclaw_dataset(row: dict[str, Any], db_id: str, schema_name: str) -> None:
    gold_sqls = row.get("sol_sql", []) or []
    if not gold_sqls:
        raise RuntimeError(f"No sol_sql found for {row['instance_id']}")
    payload = [
        {
            "input": {
                "question": row["question"],
                "db_id": db_id,
                "schema": schema_name,
                "evidence": json.dumps(row.get("external_knowledge", [])),
            },
            "expected_output": {
                "final_sql": gold_sqls[0],
                "has_sql": True,
                "schema_name": schema_name,
            },
            "metadata": {
                "instance_id": row["instance_id"],
                "difficulty": row.get("difficulty", ""),
                "category": row.get("category", ""),
            },
        }
    ]
    OVERCLAW_DATASET_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def build_overclaw_env() -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def orchestrate_run(run: RunState) -> None:
    try:
        row = find_question(run.instance_id)
        schema_name = row["db_id"]

        run.status = "running"
        run.phase = "forking"
        emit(run, f"Selected question `{row['instance_id']}`")

        fork_db_id = create_ghost_fork(run)
        run.fork_db_id = fork_db_id
        emit(run, f"Fork ready: `{fork_db_id}`")

        run.phase = "agent"
        emit(run, "Running base agent on selected question")
        agent_result = run_overclaw_agent(
            {
                "question": row["question"],
                "db_id": fork_db_id,
                "schema": schema_name,
                "evidence": json.dumps(row.get("external_knowledge", [])),
            }
        )
        run.final_sql = agent_result.get("final_sql")
        emit(run, f"Base agent final_sql:\n{run.final_sql or '<none>'}")

        run.phase = "prepare_overclaw"
        write_overclaw_dataset(row, fork_db_id, schema_name)
        emit(run, f"Wrote 1-case Overclaw dataset for fork `{fork_db_id}`")

        run.phase = "optimize"
        emit(run, "Starting `overclaw optimize kimi-go-brr --fast`")
        proc = subprocess.Popen(
            ["overclaw", "optimize", "kimi-go-brr", "--fast"],
            cwd=str(ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=build_overclaw_env(),
        )
        assert proc.stdout is not None
        for line in proc.stdout:
            emit(run, line.rstrip())
        code = proc.wait()
        if code != 0:
            raise RuntimeError(f"Overclaw exited with code {code}")

        run.phase = "report"
        results_path = OVERCLAW_EXPERIMENTS_DIR / "results.tsv"
        report_path = OVERCLAW_EXPERIMENTS_DIR / "report.md"
        if results_path.exists():
            run.artifacts["results_tsv"] = str(results_path)
        if report_path.exists():
            run.artifacts["report_md"] = str(report_path)
        emit(run, "Overclaw run finished")

        run.phase = "complete"
        run.status = "complete"
    except Exception as exc:
        run.status = "error"
        run.phase = "error"
        run.error = f"{type(exc).__name__}: {exc}"
        emit(run, f"ERROR: {run.error}")
    finally:
        run.queue.put("__COMPLETE__")


@app.get("/")
def root() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


@app.get("/api/questions")
def api_questions() -> list[dict[str, Any]]:
    rows = load_questions()
    return [
        {
            "instance_id": row["instance_id"],
            "question": row["question"],
            "difficulty": row.get("difficulty", ""),
            "category": row.get("category", ""),
        }
        for row in rows
    ]


@app.post("/api/runs")
def api_runs(request: RunRequest) -> dict[str, Any]:
    try:
        find_question(request.instance_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown question {request.instance_id}") from exc

    run = RunState(run_id=uuid.uuid4().hex, instance_id=request.instance_id)
    RUNS[run.run_id] = run
    thread = threading.Thread(target=orchestrate_run, args=(run,), daemon=True)
    thread.start()
    return {"run_id": run.run_id}


@app.get("/api/runs/{run_id}")
def api_run(run_id: str) -> dict[str, Any]:
    run = RUNS.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return {
        "run_id": run.run_id,
        "instance_id": run.instance_id,
        "status": run.status,
        "phase": run.phase,
        "fork_db_id": run.fork_db_id,
        "fork_name": run.fork_name,
        "final_sql": run.final_sql,
        "artifacts": run.artifacts,
        "error": run.error,
    }


@app.get("/api/runs/{run_id}/events")
def api_run_events(run_id: str) -> StreamingResponse:
    run = RUNS.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")

    def event_stream():
        for line in run.logs:
            yield f"data: {line}\n\n"
        while True:
            item = run.queue.get()
            if item == "__COMPLETE__":
                yield "event: done\ndata: complete\n\n"
                break
            yield f"data: {item}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
