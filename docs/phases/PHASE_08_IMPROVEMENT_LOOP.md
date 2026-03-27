# Phase 8: Improvement Loop

## Goal

Use results from the baseline and traced runs to make targeted improvements and measure whether they help.

## Scope

- prompt iteration
- tool refinement
- optional Overclaw optimization pass

## Deliverables

- `experiments/iteration_002/`
- comparison summary between baseline and improved run

## Tasks

1. Review traced failures from baseline.
2. Pick the smallest prompt or tool change likely to improve outcomes.
3. Commit that change on an iteration branch.
4. Re-run the same benchmark slice.
5. Save artifacts and compare against baseline.

## Validation

- iteration 2 differs from iteration 1 in code or prompt
- score or reliability improves in a measurable way

## Exit criteria

- at least one improvement cycle is documented end to end

## Risks

- noisy eval slices may hide whether a change helped
- too many changes at once will weaken the story

## Notes

- Prefer manual iteration first.
- Add Overclaw only after the scoring path is stable and trusted.
