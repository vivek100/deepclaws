# Agent Versioning

Use Git as the source of truth for every meaningful agent change.

## Why

The project is explicitly about agent improvement over time. If experiment outputs are not tied to exact code and prompt states, the benchmark story becomes weak.

## Rules

1. Every accepted prompt or logic change gets a commit.
2. Every benchmark iteration records the current Git SHA.
3. Never report an iteration score without storing the exact prompt and code revision behind it.
4. Treat experiment artifacts as outputs of a Git revision, not replacements for version control.

## Branching model

Recommended branches:

- `main`
- `iter/001-baseline`
- `iter/002-prompt-tuning`
- `iter/003-tracing`

Use iteration branches when a change set is large enough to deserve review or comparison. Small fixes can land directly during early setup if you are still bootstrapping.

## Commit convention

Recommended commit prefixes:

- `setup:` environment and scaffolding
- `data:` benchmark download or DB loading
- `agent:` prompt, tools, or orchestration changes
- `eval:` scoring and experiment harness
- `trace:` tracing and observability wiring
- `demo:` frontend and presentation changes

Examples:

- `setup: scaffold agent and eval modules`
- `agent: add first Ghost schema and SQL tools`
- `eval: save baseline iteration artifacts`
- `trace: attach iteration metadata to overmind runs`

## Tagging

Tag major checkpoints:

- `v0-baseline`
- `v1-first-score`
- `v2-traced-baseline`
- `v3-iter-2-improved`

Tags should represent milestones you may want to demo or compare later.

## Required experiment metadata

Each experiment directory should include a metadata file with at least:

```json
{
  "iteration": "001",
  "git_sha": "abc123",
  "git_branch": "iter/001-baseline",
  "model": "tinker://...",
  "prompt_file": "agent/prompts.py",
  "dataset": "eval/dataset.json",
  "ghost_db": "livesqlbench-iter-1"
}
```

## What to save per iteration

Inside `experiments/iteration_XXX/` save:

- `metadata.json`
- `results.json`
- `summary.md`
- `prompt.txt` or prompt snapshot
- optional trace links

Do not rely on Git alone for experiment outputs, and do not rely on experiment folders alone for code history. Use both.

## PR and review flow

Later, when GitHub and Macroscope are wired:

1. create iteration branch
2. run eval
3. save artifacts
4. open PR
5. review with Macroscope
6. merge only if score or reliability improves

## Minimum viable workflow for now

1. Make a change.
2. Run a benchmark slice.
3. Save iteration artifacts.
4. Commit the change.
5. Record the commit SHA in experiment metadata.

That is enough to make the improvement story defensible.
