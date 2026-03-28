# DeepClaws

DeepClaws is a self-improving SQL agent built for LiveSQLBench.

The project combines:
- Ghost database forks for isolated evaluation environments
- `moonshotai/Kimi-K2.5` on Tinker as the base reasoning model
- Overclaw for iterative analysis and optimization
- Macroscope as the PR-generation handoff after optimization

## What It Does

DeepClaws takes a benchmark question, creates a fresh Ghost-backed eval environment, runs a Kimi-powered SQL agent, scores the result against gold SQL output equivalence, and uses Overclaw to propose and test prompt or orchestration improvements.

The current system is designed to push Kimi 2.5 toward higher benchmark accuracy through a closed self-evaluation loop. Our working target is roughly a 10% uplift through iterative optimization, though that number should be treated as an optimization goal rather than a finalized benchmark claim.

## System Flow

1. Create a fresh Ghost fork for the selected benchmark case.
2. Bind the case and gold SQL into the eval dataset for that run.
3. Run the Kimi agent against the forked environment.
4. Evaluate correctness by comparing executed predicted SQL results against executed gold SQL results.
5. Run Overclaw to diagnose failures and test candidate improvements.
6. Produce artifacts and a PR handoff payload for Macroscope.

## Judge Notes

- The evaluation target is binary correctness, not SQL string matching.
- The current demo path uses a reduced optimization loop for speed.
- PR generation is prepared in the app handoff, but Macroscope automation is still the next integration step.

## Run Locally

Prerequisites:
- Ghost CLI installed and logged in
- `.env` populated with Tinker and project keys
- `.overclaw/.env` populated with Overclaw model settings
- benchmark data present under `data/livesqlbench`

Start the app:

```powershell
.\.venv\Scripts\python.exe scripts\run_demo_ui.py
```

Open `http://127.0.0.1:8000`.

## Key Files

- UI: [web/index.html](web/index.html)
- Backend runner: [demo/server.py](demo/server.py)
- Agent entrypoint for Overclaw: [agent/overclaw_agent.py](agent/overclaw_agent.py)
- GT-backed dataset: [eval/dataset.gt.json](eval/dataset.gt.json)
- One-case Overclaw dataset: [.overclaw/agents/kimi-go-brr/setup_spec/dataset.json](.overclaw/agents/kimi-go-brr/setup_spec/dataset.json)
- Demo optimizer wrapper: [scripts/run_overclaw_custom.py](scripts/run_overclaw_custom.py)
