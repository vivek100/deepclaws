# Overmind and Overclaw Sponsor Notes

## Why it matters here

Overmind and Overclaw are the best fit for the "self-improving agent" part of the pitch. They cover tracing, diagnosis, and automated improvement instead of only raw execution.

Sources reviewed:

- Existing repo copy of the Overclaw docs in the previous version of this file
- https://docs.overmindlab.ai/guides/overclaw_doc

## What Overclaw is good for

Overclaw is an optimizer. It runs an agent against a dataset, traces calls, scores outputs, proposes fixes, validates candidates, and keeps only improvements.

That lines up well with the project's loop:

1. Run LiveSQLBench subset.
2. Score pass/fail.
3. Inspect traces.
4. Generate prompt or logic improvements.
5. Re-run and keep only better versions.

## Recommended sponsor path

### Safer path for hackathon

Use Overmind SDK style tracing first, then do manual prompt iteration if needed.

Why:

- Lower integration risk.
- Still gives you a sponsor-aligned tracing story.
- Avoids overcommitting to a full optimizer if the core agent is not stable yet.

### Stronger path if time allows

Use Overclaw for one controlled optimization loop on a small eval set.

Good constraints:

- 10 to 20 representative tasks first.
- Stable scoring function.
- One prompt file and one agent entrypoint.

## What to wire

- Trace every agent run and tool invocation.
- Save the current system prompt and eval result with each iteration.
- Keep one artifact per iteration: score, prompt diff, and notable failure pattern.

## Minimal process

1. Run baseline eval.
2. Capture traces.
3. Review failures.
4. Change prompt or tool descriptions.
5. Re-run holdout subset.
6. Accept only if score improves.

## Hackathon guidance

- Treat Overmind tracing as the default path.
- Treat full Overclaw optimize loops as a stretch upgrade once scoring is reliable.
- Do not let optimizer complexity block the baseline benchmark demo.

## Links worth keeping

- Overclaw docs: https://docs.overmindlab.ai/guides/overclaw_doc
- Overmind docs root: https://docs.overmindlab.ai/


---
title: Overclaw | Overmind
description: Overclaw is an agent optimizer.
---

# OverClaw

**Automatically optimize your AI agent’s prompts, tools, model selection, and logic — without manual prompt tweaking.**

OverClaw runs your agent against a test dataset, traces every LLM call and tool invocation, scores the outputs, and uses a strong reasoning model to generate concrete improvements. Changes that raise the score are kept; the rest are reverted. After several rounds you get a measurably better agent.

---

## Why OverClaw?

Building AI agents is easy. Making them *reliable* is hard. You ship an agent, it works 70% of the time, and then you spend weeks reading logs, tweaking prompts, adjusting tool definitions, and re-running evals — only to find that fixing one case breaks three others.

OverClaw replaces that manual loop with structured, automated experimentation. Point it at your agent, give it a test dataset (or let it generate one), and it will iteratively diagnose failures, generate fixes, and validate improvements — all while respecting the rules and constraints you care about.

### What makes it different

**Policy-driven optimization.** Most optimization tools maximize a score. OverClaw maximizes a score *while respecting your policies*. You define the decision rules, constraints, and expectations your agent must follow, and those policies guide *every* stage — evaluation criteria, test data synthesis, diagnosis, and scoring. This means the optimizer can’t game metrics in ways that violate your business rules.

**Full-stack agent optimization.** OverClaw doesn’t just tweak prompts. It can modify system prompts, tool descriptions, model selection, agent control flow, output parsing, and iteration limits — all in a single optimization run. It understands the full picture of how your agent works.

**Trace-aware diagnosis.** Every optimization cycle starts with detailed traces of what your agent actually did — every LLM call, every tool invocation, every intermediate result. The diagnosis model sees exactly where things went wrong, not just that the final output was incorrect.

### What gets optimized

| Area                  | Examples                                                                       |
| --------------------- | ------------------------------------------------------------------------------ |
| **System prompts**    | More precise instructions, output format enforcement, better few-shot examples |
| **Tool descriptions** | Clearer parameters, better usage guidance, improved error handling             |
| **Model selection**   | Finding the right quality/cost tradeoff per task                               |
| **Agent logic**       | Tool-call ordering, retry strategies, iteration limits, output parsing         |
| **Policy compliance** | Alignment with your domain rules, edge case handling, consistency constraints  |

### Compared to other approaches

| Approach                                     | Limitation                                                       | OverClaw                                                                |
| -------------------------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Manual prompt tuning                         | Slow, subjective, doesn’t scale, no systematic regression checks | Automated diagnosis and codegen with regression-aware acceptance        |
| Generic prompt optimizers (DSPy, etc.)       | Optimize prompts in isolation, ignore tool use and agent logic   | Optimizes prompts, tools, code, and model selection together            |
| Eval-only frameworks (Braintrust, Langsmith) | Tell you *what’s wrong* but not how to fix it                    | Diagnoses failures and generates concrete code fixes                    |
| Fine-tuning                                  | Requires large datasets, expensive, loses generality             | Works with small test sets (10–50 cases), keeps the agent’s flexibility |
| Manual A/B testing                           | Time-consuming, requires infrastructure                          | Automated best-of-N candidate evaluation with statistical safeguards    |

---

## Installation

**Requirements:**

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) (modern Python package manager)
- API keys for at least one LLM provider (OpenAI, Anthropic)

### Install as a CLI tool

Terminal window

```
uv tool install overclaw
```

### Install for local development

Terminal window

```
git clone https://github.com/overmind-core/overclaw
cd overclaw
uv tool install -e .
```

### Verify installation

Terminal window

```
overclaw --help
```

---

## Quick Start

### 1. Initialize

Terminal window

```
overclaw init
```

This creates a `.overclaw/` directory in your project root and walks you through configuring API keys and default models. The configuration is stored in `.overclaw/.env`. Safe to re-run at any time.

### 2. Register your agent

Terminal window

```
overclaw agent register lead-qualification agents.my_agent:run
```

This tells OverClaw which Python function to call for each test case. The module path (`agents.my_agent`) is resolved relative to your project root, and `run` is the function name.

Your agent function must accept an input dict and return a dict:

```
from overclaw.core.tracer import call_llm, call_tool


def run(input: dict) -> dict:
    # Use call_llm and call_tool for full tracing support
    response = call_llm(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a lead qualification agent..."},
            {"role": "user", "content": str(input)}
        ]
    )


    return {
        "category": "hot",
        "lead_score": 85,
        "reasoning": "Company has 500+ employees and mentioned enterprise pricing"
    }
```

### 3. Setup evaluation

Terminal window

```
overclaw setup lead-qualification
```

This interactive flow prepares everything the optimizer needs. It will:

1. **Analyze your agent code** to detect input/output schema, tools, and decision logic
2. **Generate or refine policies** that define what correct behavior looks like
3. **Create or import a test dataset** with diverse cases
4. **Propose evaluation criteria** with scoring rules for each output field

You can skip the interactive prompts with `--fast` for CI/automation use.

### 4. Optimize

Terminal window

```
overclaw optimize lead-qualification
```

This kicks off the iterative optimization loop. Sit back and watch as OverClaw diagnoses failures, generates fixes, validates them, and keeps what works.

---

## Core Concepts

### Policies

Policies are the foundation of meaningful optimization. They tell the optimizer *what* the agent should do, not just how it currently scores — preventing improvements that raise numbers but violate business rules.

A policy document (`policies.md`) looks like this:

```
# Agent Policy: Lead Qualification


## Purpose
Qualifies inbound sales leads by analyzing company data and inquiry content.


## Decision Rules
1. If the inquiry mentions "enterprise" or "custom pricing", classify as hot
2. Companies with 500+ employees get a minimum lead score of 60
3. Inquiries about specific product features indicate warm interest


## Constraints
- Never disqualify without checking company size
- Score and category must be consistent (hot = 70+, warm = 40-69, cold = <40)
- Reasoning must reference specific data points from the input


## Priority Order
1. Accuracy of category classification
2. Score calibration
3. Reasoning quality


## Edge Cases
| Scenario             | Expected Behaviour                    |
|----------------------|---------------------------------------|
| Missing company name | Default to cold, note in reasoning    |
| Competitor inquiry   | Classify as cold, recommend nurture   |
```

You can provide an existing policy document during setup:

Terminal window

```
overclaw setup lead-qualification --policy docs/my_policy.md
```

OverClaw will analyze it against your agent code and suggest refinements. If you don’t provide one, a policy is automatically inferred from your code. Either way, you can refine it in a conversational loop before approving.

Policies feed into diagnosis prompts, code generation constraints, synthetic data generation, and LLM-as-Judge scoring — so every stage of the pipeline respects your domain rules.

### Test Data

Data files are JSON arrays where each element has an `input` and `expected_output`:

```
[
  {
    "input": {
      "company_name": "Acme Corp",
      "employee_count": 1200,
      "inquiry": "Need enterprise pricing for our sales team"
    },
    "expected_output": {
      "category": "hot",
      "lead_score": 85,
      "reasoning": "Large enterprise requesting custom pricing indicates high intent"
    }
  },
  {
    "input": {
      "company_name": "SmallBiz LLC",
      "employee_count": 15,
      "inquiry": "Just browsing your features page"
    },
    "expected_output": {
      "category": "cold",
      "lead_score": 20,
      "reasoning": "Small company with no specific intent or product interest"
    }
  }
]
```

Place data files in your agent directory under `data/` and OverClaw will detect them during setup. A test set of 10–50 diverse cases is usually sufficient. If you don’t have data, OverClaw generates realistic synthetic test cases using the policy and agent description.

### Tracing

OverClaw provides two helper functions — `call_llm` and `call_tool` — that your agent should use instead of calling LLM APIs directly. These wrappers record detailed spans for every invocation:

- **LLM calls**: model, messages, token usage, cost, latency, tool-call metadata
- **Tool calls**: function name, arguments, result, latency, errors

Using these wrappers gives the optimizer full visibility into *why* your agent produced a given output, enabling much more targeted diagnosis and fixes. If you use `litellm.completion` or provider SDKs directly, OverClaw will still capture input/output and total latency, but won’t have per-call span detail.

---

## How the Optimization Loop Works

Each iteration of `overclaw optimize` follows a structured pipeline:

### Step 1: Run

The agent is executed against every test case in the training set. Each run produces a full trace capturing every LLM call, tool invocation, intermediate result, and the final output.

### Step 2: Score

Outputs are scored against the evaluation spec on a 0–100 scale across multiple dimensions:

- **Structural correctness** — Are all expected fields present and non-empty?
- **Value accuracy** — Do enum fields match? Are numeric fields within tolerance bands?
- **Cross-field consistency** — Do related fields agree with each other (e.g., “hot” category with score ≥ 70)?
- **Tool usage** — Were the right tools called, with correct parameters, in the right order?
- **LLM-as-Judge** (optional) — A judge model provides semantic scoring using policy-aware rubrics for dimensions that can’t be checked mechanically

### Step 3: Diagnose

The analyzer model receives the current agent code, per-case traces, scores, the policy document, and the history of previously attempted fixes (both successful and failed). It identifies failure patterns and root causes — not just “the score was low” but “the agent is calling the search tool before validating input, leading to empty results on cases with missing fields.”

### Step 4: Generate candidates

Multiple candidate fixes are generated, each biased toward a different optimization area — tool descriptions, core logic, input handling, system prompt. This best-of-N approach increases the chances of finding an improvement. For diversity, the last candidate uses a separate independent diagnosis.

### Step 5: Validate

Candidates go through syntax checking, interface verification (does the entrypoint still exist with the right signature?), and a smoke test on a small random subset. Candidates that crash or score dramatically below the current best are dropped early.

### Step 6: Evaluate

Surviving candidates are scored on the full training dataset. The best candidate is selected by adjusted score (accounting for complexity penalties).

### Step 7: Accept or revert

The best candidate is kept *only if* it meets strict acceptance criteria:

- It must beat the **global best score** (not just the previous iteration)
- It must not regress too many individual test cases
- Per-case regression is checked with a 3-point threshold, with multiple tiers (net-positive improvement, magnitude override)

If no candidate improves, the iteration is marked as a stall. After a configurable number of consecutive stalls (early stopping patience), optimization ends.

### Post-optimization

After all iterations complete, OverClaw:

1. Writes the best agent version to `experiments/best_agent.py`
2. Evaluates on the **holdout set** (unseen cases) to check for overfitting
3. Optionally rolls back if holdout performance is catastrophically worse
4. Generates a `report.md` summarizing scores, improvements, and diffs

---

## Under the Hood

### Optimization safeguards

OverClaw includes several mechanisms to prevent common failure modes in automated optimization:

**Train/holdout split.** A portion of test cases is held out and never seen during optimization. After the loop completes, the best agent is evaluated on holdout cases. If holdout performance drops catastrophically, OverClaw searches across recent accepted snapshots for a version that generalizes better.

**Regression-aware acceptance.** A candidate that raises the average score by 2 points but tanks 5 individual cases is likely memorizing patterns rather than making a genuine improvement. OverClaw checks per-case deltas and rejects candidates that regress too many cases, even if the average improves.

**Complexity penalty.** The optimizer applies a quadratic penalty for excessive prompt size growth, code line growth, new branches, and hardcoded training outputs. This discourages the model from “solving” test cases by adding massive prompt text or if-else chains for specific inputs.

**Label leakage prevention.** Analyzer prompts redact expected outputs when presenting failing cases to the diagnosis model. This prevents the optimizer from simply copying test answers into the agent code. Accepted code is also scanned for patterns that suggest data leakage.

**Temperature annealing.** The code generation temperature starts at 0.8 (exploratory) and decreases to 0.4 (focused) over iterations. If the optimizer stalls for two consecutive rounds, temperature is bumped back up to encourage exploration of different fix strategies.

### Multi-file agents

By default, OverClaw optimizes the single file containing your registered entrypoint. But many real agents are split across multiple modules — one for prompts, one for tools, one for orchestration logic, etc.

OverClaw handles this through the `AgentBundle` system. When your entrypoint imports from local modules, OverClaw:

1. Statically resolves the import graph from your entrypoint
2. Identifies which files are in scope for optimization
3. Generates targeted edits per file (not a monolithic rewrite)
4. Splices changes back into your original project structure

Your directory layout stays intact throughout the process.

### Parallel execution

Agent evaluations run in a `ThreadPoolExecutor` for speed. Thread-local tracing ensures each concurrent agent run gets its own isolated trace context, so spans don’t cross-contaminate between test cases.

---

## CLI Reference

```
overclaw init                              Configure API keys and models
overclaw agent register <name> <mod:fn>    Register an agent
overclaw agent list                        List registered agents
overclaw agent show <name>                 Show agent status and pipeline progress
overclaw agent update <name> <mod:fn>      Update entrypoint
overclaw agent remove <name>               Remove from registry (does not delete files)
overclaw setup <name> [--fast] [--policy]  Analyze agent, build eval spec and dataset
overclaw optimize <name> [--fast]          Run optimization loop
```

| Flag            | Available on        | Description                                        |
| --------------- | ------------------- | -------------------------------------------------- |
| `--fast`        | `setup`, `optimize` | Skip interactive prompts, use defaults from `.env` |
| `--policy PATH` | `setup`             | Provide an existing policy document for analysis   |

Run `overclaw <command> --help` for full documentation on any command.

---

## Output

After optimization, results are saved under `.overclaw/agents/<name>/`:

| Path                        | Description                                         |
| --------------------------- | --------------------------------------------------- |
| `setup_spec/policies.md`    | Agent policy document (human-editable)              |
| `setup_spec/eval_spec.json` | Machine-readable evaluation criteria                |
| `setup_spec/dataset.json`   | Test dataset used for optimization                  |
| `experiments/best_agent.py` | The highest-scoring agent version                   |
| `experiments/best_agent/`   | All optimized files (multi-file agents only)        |
| `experiments/results.tsv`   | Score history for every iteration                   |
| `experiments/traces/`       | Detailed JSON traces of every agent run             |
| `experiments/report.md`     | Summary report with scores, improvements, and diffs |

All artifacts are human-readable and editable. You can modify the policy or eval spec and re-run `overclaw optimize` to continue improving from where you left off.
