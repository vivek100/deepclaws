# Implementation Plan

## Objective

Ship a working self-improving SQL agent in the smallest sequence that still preserves the main demo story:

1. query real benchmark data
2. run against Ghost forks
3. score results
4. trace runs
5. iterate agent versions in Git

## Guiding decisions

- Ignore Airbyte and Auth0 for now.
- Add Macroscope later, after the repo has real code and PRs.
- Treat Overmind tracing as baseline and Overclaw optimization as stretch.
- Use Git commits and tags as the official history of agent versions.

## Phase 1: Foundation

Deliverables:

- repo structure created
- Python environment initialized
- Ghost CLI verified locally
- `.env.example` defined with only critical vars

Files:

- `agent/`
- `eval/`
- `pipeline/`
- `experiments/`
- `.env.example`

Exit criteria:

- Ghost main DB and one fork can be created and queried

Phase doc:

- `docs/phases/PHASE_01_FOUNDATION.md`

## Phase 2: Benchmark data

Deliverables:

- LiveSQLBench subset downloader
- first benchmark dataset slice committed
- one benchmark database loaded into Ghost

Files:

- `scripts/download_benchmark.py`
- `scripts/load_benchmark.py`
- `eval/dataset.json`

Exit criteria:

- one benchmark question can be matched to a live Ghost-backed database

Phase doc:

- `docs/phases/PHASE_02_BENCHMARK_DATA.md`

## Phase 3: Runnable agent

Deliverables:

- Ghost-backed tools
- first system prompt
- runnable agent entrypoint

Files:

- `agent/tools.py`
- `agent/prompts.py`
- `agent/agent.py`

Exit criteria:

- agent returns SQL for hand-picked benchmark questions

Phase doc:

- `docs/phases/PHASE_03_RUNNABLE_AGENT.md`

## Phase 4: Baseline evaluation

Deliverables:

- evaluation runner
- SQL extraction and scoring
- first saved experiment directory

Files:

- `eval/score.py`
- `pipeline/run_baseline.py`
- `experiments/iteration_001/`

Exit criteria:

- a reproducible baseline score exists

Phase doc:

- `docs/phases/PHASE_04_BASELINE_EVAL.md`

## Phase 5: Tracing

Deliverables:

- Overmind tracing initialization
- iteration metadata attached to runs

Files:

- `agent/agent.py`
- `pipeline/run_baseline.py`

Exit criteria:

- baseline run is visible in tracing with enough context to debug failures

Phase doc:

- `docs/phases/PHASE_05_TRACING.md`

## Phase 6: Git-based agent iteration

Deliverables:

- branch naming convention
- commit tagging convention
- experiment metadata including Git SHA
- iteration summary template

Files:

- `docs/AGENT_VERSIONING.md`
- `experiments/iteration_XXX/metadata.json`

Exit criteria:

- every experiment can be traced back to an exact code revision

Phase doc:

- `docs/phases/PHASE_06_VERSIONING.md`

## Phase 7: Improvement loop

Deliverables:

- prompt revision flow
- optional Overclaw optimization pass
- iteration comparison summary

Exit criteria:

- iteration 2 clearly differs from iteration 1 in both code/prompt and score

Phase doc:

- `docs/phases/PHASE_07_IMPROVEMENT_LOOP.md`

## Phase 8: Demo surface

Deliverables:

- live run view
- dashboard for scores and diffs
- optional Macroscope PR review workflow

Exit criteria:

- demo can show one run and one improvement arc

Phase doc:

- `docs/phases/PHASE_08_DEMO_SURFACE.md`

## Immediate next actions

1. Scaffold the repo structure from the planned modules.
2. Install minimal dependencies only.
3. Run a Ghost smoke test and document the exact commands that worked.
4. Download a small LiveSQLBench subset.
5. Build the first Ghost-backed agent shell.

## Non-goals for first implementation pass

- production auth
- production ingestion stack
- automated fine-tuning
- polished frontend
- full autonomous optimization loop
