# Phase 5: Tracing

## Goal

Attach tracing to the baseline flow so failures can be diagnosed with real run context.

## Scope

- Overmind tracing initialization
- trace metadata for iteration and model version
- tool-call visibility

## Deliverables

- tracing setup in `agent/agent.py`
- iteration metadata added in pipeline code

## Tasks

1. Initialize tracing in the runtime path that executes the agent.
2. Attach iteration ID, dataset slice, and Git SHA to each run.
3. Make sure Ghost tool calls are visible enough to debug failures.
4. Save trace links or run IDs into experiment artifacts where possible.

## Validation

- baseline run appears in tracing
- failed questions are inspectable with enough context to diagnose

## Exit criteria

- one full benchmark run is visible in tracing
- traces are useful enough to explain at least one failure mode

## Risks

- tracing wrappers may add noise or latency
- metadata may be incomplete if wired too late

## Notes

- Tracing is baseline.
- Full automated optimization is not baseline.
