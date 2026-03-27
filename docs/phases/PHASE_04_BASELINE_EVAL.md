# Phase 4: Baseline Evaluation

## Goal

Produce the first reproducible benchmark-aligned run and save iteration artifacts on disk.

## Scope

- scoring logic
- baseline runner
- experiment artifact layout
- GT/test-case integration

## Deliverables

- `eval/score.py`
- `pipeline/run_baseline.py`
- `scripts/run_eval.py`
- `experiments/iteration_001/`
- `docs/BASELINE_SCOREBOARD.md`

## Tasks

1. Integrate the official GT file into the public dataset by `instance_id`.
2. Implement SQL extraction from agent output in a consistent way.
3. Run the official-style test-case evaluation path for each instance.
4. Centralize the local eval slice and track all runs from one CLI.
5. Run a small baseline slice before attempting the full subset.
6. Save results and a readable summary under `experiments/iteration_001/`.

## Required artifacts

- `metadata.json`
- `results.json`
- `summary.md`
- prompt snapshot
- baseline scoreboard entry
- integrated dataset with protected fields present

## Validation

- baseline runner completes
- test-case pass/fail counts are visible
- experiment directory can be inspected after the run

## Exit criteria

- the project has a real benchmark score
- artifacts are good enough to compare against later iterations

## Risks

- SQL extraction from model output may be brittle
- the public Lite slice omits benchmark golds, so GT integration is mandatory
- some management tasks need test-case execution rather than simple result comparison

## Notes

- Reproducibility matters more than score quality in this phase.
