# Baseline Scoreboard

This file tracks the project's measured starting point before prompt or code optimization.

## Current status

- `iteration_001_smoke`: executable success rate `100.0%` (`1/1`)
- `iteration_001`: pending full-slice run
- Primary metric for the current local slice: executable success rate
- Exact benchmark accuracy: blocked until the official GT package is integrated into the local dataset and scored with the official-style test-case path

## Notes

- The public `birdsql/livesqlbench-base-lite` slice we saved locally does not expose benchmark gold SQL, test cases, or full external knowledge, so the current baseline is an operational smoke metric rather than true leaderboard accuracy.
- The first smoke artifact is saved under `experiments/iteration_001_smoke/`.
- Official benchmark alignment requires:
  - integrating the emailed GT file with `integrate_gt_data.py`
  - running against the benchmark test cases
  - treating executable success as secondary diagnostics only
