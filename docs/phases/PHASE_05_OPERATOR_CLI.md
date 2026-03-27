# Phase 5: Operator CLI

## Goal

Create stable CLI utilities for the common workflows Codex and local development need before these flows are exposed via an API.

## Why this phase exists

The project will eventually expose these actions to a frontend through backend endpoints, but that is the wrong first interface.

We need command-line entrypoints first so:

- Codex can run repeatable workflows directly
- local debugging is fast
- API design later can wrap real execution paths instead of reimplementing them

## Scope

- run one question against the agent
- run an eval slice
- inspect saved experiment artifacts
- optionally create a new iteration working directory

## Deliverables

- `scripts/run_question.py`
- `scripts/run_eval.py`
- `scripts/show_experiment.py`
- optional `scripts/new_iteration.py`

## Tasks

1. Define a consistent CLI style with arguments and defaults.
2. Add a command to run one benchmark question against a chosen Ghost database.
3. Add a command to run an eval subset with `--limit` and output controls.
4. Add a command to inspect saved experiment metadata and summary files.
5. Keep the internal function boundaries reusable so API endpoints can call the same code later.

## Example commands

```powershell
uv run python scripts/run_question.py --db <database-id> --question "How many users are there?"
uv run python scripts/run_eval.py --dataset eval/dataset.json --limit 10 --iteration 001
uv run python scripts/show_experiment.py --iteration 001
```

## Validation

- the common local workflows can be executed without writing custom shell commands each time
- CLI commands call reusable Python code instead of burying logic in shell scripts

## Exit criteria

- Codex can run the main local workflows through stable command names
- the future backend API can wrap these same code paths cleanly

## Risks

- too much CLI polish too early
- business logic drifting into scripts instead of shared modules

## Notes

- This phase is a bridge between local implementation and future API exposure.
- The API should wrap these code paths later, not replace them.
