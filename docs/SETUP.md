# Deep Agent Setup and Execution

This file is the implementation-facing setup guide for the project. It is intentionally organized around shipping order instead of sponsor order.

Use this together with:

- `docs/IMPLEMENTATION_PLAN.md` for the full phased build plan
- `docs/AGENT_VERSIONING.md` for Git workflow and iteration tracking

## Current build order

1. Phase 1: repo scaffold and Ghost smoke test
2. Phase 2: benchmark download and database loading
3. Phase 3: agent with Ghost tools
4. Phase 4: evaluation harness and baseline
5. Phase 5: tracing
6. Phase 6: iteration workflow with Git versions
7. Phase 7: demo UI and PR review

## Current local state

- Project directories have been scaffolded.
- `uv` is available locally.
- `ghost` CLI is installed locally.
- Git has been initialized locally.
- Ghost login has been completed.
- Smoke-test databases exist in Ghost: one main DB and one fork.

## Phase 1: repo scaffold and Ghost smoke test

Goal:

- Create the runnable project structure
- Install minimal dependencies
- Verify Ghost works before writing agent code around it

Minimum checks:

- `ghost login`
- `ghost create --name livesqlbench-main`
- `ghost connect <database-id>`
- `ghost fork <database-id> --name livesqlbench-smoke --wait`
- `ghost sql <database-id> "select 1;"`
- `ghost schema <database-id>`

Done when:

- One Ghost main DB exists
- One fork can be created and queried
- Connection strategy is clear for local code

Current implementation notes:

- `pyproject.toml`, `.env.example`, and basic module placeholders are in place.
- Ghost CLI `v0.4.5` is installed and working.
- Ghost login succeeded and created a space.
- `livesqlbench-main` was created successfully.
- A fork named `livesqlbench-smoke` was created successfully.
- `ghost sql <fork-id> "select 1 as smoke_test;"` returned `1`.
- This Ghost CLI uses database IDs for `fork`, `connect`, `sql`, and `schema`.
- The next build step is Phase 2: benchmark download and DB loading.

## Phase 2: benchmark download and database loading

Goal:

- Get a small, real LiveSQLBench subset locally
- Load benchmark schema/data into Ghost

Scope:

- Start with a very small subset and one database if needed
- Ignore Airbyte unless direct loading becomes painful

Done when:

- `eval/dataset.json` exists
- At least one benchmark database is queryable inside Ghost

## Phase 3: agent with Ghost tools

Goal:

- Build the first runnable SQL agent against Ghost

Scope:

- `agent/tools.py`
- `agent/prompts.py`
- `agent/agent.py`

Required tools:

- `ghost_schema`
- `ghost_sql`
- `ghost_connect`

Optional later:

- `ghost_fork`

Done when:

- The agent can answer a few hand-picked questions and produce SQL

## Phase 4: evaluation harness and baseline

Goal:

- Produce a real baseline score and save artifacts

Scope:

- `eval/score.py`
- `pipeline/run_baseline.py`
- `experiments/iteration_001/`

Artifacts to save:

- dataset slice used
- prompt version
- model config
- results JSON
- summary markdown

Done when:

- A baseline iteration exists on disk and can be reproduced

## Phase 5: tracing

Goal:

- Add Overmind tracing after the baseline path is stable

Scope:

- Trace each agent run
- Trace tool usage
- Attach iteration ID and Git commit SHA to runs

Done when:

- One baseline iteration has trace visibility in the tracing tool

## Phase 6: iteration workflow with Git versions

Goal:

- Use Git as the source of truth for agent evolution

Rules:

- Every accepted agent improvement gets a commit
- Every major iteration gets a tag or named branch
- Experiment artifacts reference the exact commit SHA

Use:

- `docs/AGENT_VERSIONING.md`

Done when:

- You can map any experiment result back to exact code and prompt state

## Phase 7: demo UI and PR review

Goal:

- Build the story layer after the core loop works

Scope:

- dashboard
- live eval run view
- Macroscope PR review on iteration branches

Done when:

- The demo can show one live run and one score progression story

## Deferred for now

- Airbyte as required ingestion path
- Auth0 integration
- Tinker SFT/RL as required baseline functionality
- Macroscope as an early dependency
- Full Overclaw optimization loop before baseline stability
