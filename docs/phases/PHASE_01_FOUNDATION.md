# Phase 1: Foundation

## Goal

Create the runnable repo skeleton and verify Ghost works before building agent logic around it.

## Scope

- create project directories
- initialize Python environment
- define minimal environment variables
- verify Ghost CLI and database lifecycle commands

## Deliverables

- `agent/`
- `eval/`
- `pipeline/`
- `training/`
- `scripts/`
- `experiments/`
- `.env.example`

## Tasks

1. Create the repo structure from the planned modules.
2. Install only the minimum dependencies needed to talk to Ghost and run Python code.
3. Log in to Ghost and create one main database.
4. Fork the main database and run basic SQL against the fork.
5. Record the exact commands that worked in `docs/SETUP.md`.

## Validation

- `ghost create --name livesqlbench-main` works
- `ghost fork <database-id> --name livesqlbench-smoke --wait` works
- `ghost connect <database-id>` returns a usable connection string
- `ghost sql <database-id> "select 1 as smoke_test;"` executes successfully
- `ghost schema <database-id>` returns database metadata

## Exit criteria

- one main database exists
- one fork can be created and queried
- local environment shape is clear enough to start Phase 2

## Risks

- Ghost auth or CLI install issues
- unclear connection strategy for Python code

## Notes

- Do not start on tracing or UI work here.
- This phase is purely about making the runtime real.
- Ghost CLI command usage is ID-based for most database operations, not name-based.
