# Phase 4: Baseline Evaluation

## Goal

Produce the first reproducible benchmark run and save iteration artifacts on disk.

## Scope

- scoring logic
- baseline runner
- experiment artifact layout

## Deliverables

- `eval/score.py`
- `pipeline/run_baseline.py`
- `experiments/iteration_001/`

## Tasks

1. Implement SQL execution and result comparison.
2. Extract final SQL from agent output in a consistent way.
3. Run a small baseline slice before attempting the full subset.
4. Save results and a readable summary under `experiments/iteration_001/`.

## Required artifacts

- `metadata.json`
- `results.json`
- `summary.md`
- prompt snapshot

## Validation

- baseline runner completes
- pass/fail counts are visible
- experiment directory can be inspected after the run

## Exit criteria

- the project has a real baseline score
- artifacts are good enough to compare against later iterations

## Risks

- SQL extraction from model output may be brittle
- result-set comparison may need normalization

## Notes

- Reproducibility matters more than score quality in this phase.
