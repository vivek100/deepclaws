# Deep Agents Hackathon — Project Plan
> **Theme**: Autonomous, self-improving AI agents that tap real-time data, make sense of it, and take action

---

## 🎯 One-Line Pitch

A self-improving SQL analytics deep agent that benchmarks itself against **LiveSQLBench**, iterates on its own prompts and logic across isolated database forks, and measurably gets better — all without human intervention. Every failed eval becomes training data for the next model generation.

---

## 🧩 The Problem

LLM agents for complex SQL analytics are unreliable. Even frontier models score under **40% on LiveSQLBench** — a contamination-free, real-world Postgres benchmark. The fix today is manual: read logs, tweak prompts, re-run. That doesn't scale.

**We automate the entire improvement loop: prompt optimization → eval → SFT data collection → fine-tuning.**

---

## 🏗️ Full Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                                │
│                                                                  │
│  LiveSQLBench (HuggingFace: birdsql/livesqlbench-base-lite)      │
│       │                                                          │
│       ▼  Airbyte → Postgres destination connector               │
│  Ghost Main DB  ──── ghost fork ──▶  Ghost Fork DB (per run)     │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                       AGENT LAYER                                │
│                                                                  │
│  deepagents (langchain-ai/deepagents)                            │
│  └── create_deep_agent(model=tinker_endpoint, tools=[...])       │
│       ├── tool: ghost_schema    (inspect schema)                 │
│       ├── tool: ghost_sql       (execute SQL)                    │
│       ├── tool: ghost_connect   (get connection string)          │
│       ├── built-in: write_todos (task planning + decomposition)  │
│       ├── built-in: file system (offload large schema context)   │
│       └── built-in: spawn_subagent (complex sub-tasks)          │
│                                                                  │
│  Inference: Tinker OpenAI-compatible API                         │
│  → Kimi K2 Thinking (1T param reasoning model)                  │
│  → or Qwen3-235B — single string change to swap                 │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                    EVALUATION LAYER                              │
│                                                                  │
│  Metric: Success Rate (pass/fail per LiveSQLBench test case)     │
│  Run ~50 questions per iteration                                 │
│  Ground truth: gold SQL from LiveSQLBench dataset               │
│                                                                  │
│  Tracing: Overmind / Overclaw  OR  Truefoundry AI Gateway       │
│  → Every LLM call + tool invocation recorded with full trace    │
│  → Passing evals collected as SFT training data                 │
│  → Failing evals collected for diagnosis                        │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│              SELF-IMPROVEMENT LAYER (two mechanisms)             │
│                                                                  │
│  [A] Prompt Optimization — fast, every iteration                │
│      Overclaw: traces failures → diagnoses root cause           │
│      → generates prompt / tool / logic candidates               │
│      → validates on holdout → keeps only improvements           │
│      → Kiro opens PR → Macroscope reviews it                    │
│                                                                  │
│  [B] SFT Fine-Tuning — stretch goal, runs in background         │
│      Collect (question, schema, gold_sql) from passing evals    │
│      → format as Tinker SFT dataset                             │
│      → Tinker: train LoRA on Kimi K2 / Qwen3                   │
│      → swap in fine-tuned model for next eval round             │
│      → measure score delta: base vs. fine-tuned                 │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                      FRONTEND LAYER                              │
│                                                                  │
│  [1] Live Eval Run View                                          │
│      Stream one LiveSQLBench question through the agent live     │
│      → NL question → agent thinking → SQL output → result       │
│      → Pass/fail badge, token cost, latency, Ghost fork used    │
│                                                                  │
│  [2] Benchmark Dashboard                                         │
│      → Line chart: our Success Rate across iterations           │
│      → Dotted baselines: o3-mini 47%, GPT-4.1 44%, etc.        │
│      → Per-category breakdown: SELECT vs CRUD                   │
│      → Prompt diff viewer between iterations                    │
│      → SFT data counter: examples accumulated per run           │
│      → Model label: "Iter 3: Kimi K2 + Tinker LoRA"            │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔄 The Self-Improvement Loop

```
Iteration N:
  1. ghost fork <main_db>           → clean isolated DB for this run
  2. deep agent runs 50 LiveSQLBench questions
     - deepagents handles planning, subagents, context management
     - Tinker API for inference (Kimi K2 Thinking or Qwen3)
  3. score vs ground truth          → Success Rate %
  4. trace all LLM + tool calls (Overclaw / Truefoundry)
  5. passing evals → add to SFT dataset
  6. Overclaw diagnoses failures → generates prompt/tool fixes
  7. Kiro applies best fix → opens PR
  8. Macroscope reviews PR → approvability score
  9. if score improves → accept, proceed
 10. [async] Tinker SFT on accumulated passing evals → new LoRA
 11. goto Iteration N+1 on new Ghost fork, with improved prompt+model

Demo stop: 3 iterations
```

---

## 🛠️ Tech Stack & Prize Tracks

| Tool | Role | Prize Track |
|------|------|-------------|
| **deepagents** (`langchain-ai/deepagents`) | Core deep agent — planning, subagents, file system | Satisfies "deep agent" requirement |
| **Ghost** (`ghost.build`) | Managed Postgres + `ghost fork` per eval run | ✅ Best Use of Ghost ($1,998) |
| **Airbyte** | Sync LiveSQLBench → Ghost main DB | ✅ Airbyte: Conquer with Context ($1,750) |
| **Overmind / Overclaw** | Tracing + automated prompt improvement loop | ✅ Overmind Builders Prize ($651) |
| **Truefoundry** | Fallback AI Gateway for tracing | ✅ Truefoundry: AI Gateway ($600) |
| **Tinker** (Thinking Machines) | Inference (OpenAI-compat) + SFT/RL fine-tuning | Differentiator — the "learning" angle |
| **Kiro** | Builds everything + orchestrates loop + opens PRs | ✅ Best Use of Kiro |
| **Macroscope** | Reviews each agent iteration PR | ✅ Macroscope ($1,000) |

**Prize potential: $6,599+ across 6 tracks**

---

## 🤖 Why deepagents (not raw LangGraph)

deepagents bundles planning tools, virtual file-system based memory, and subagent orchestration out of the box, whereas plain LangGraph requires building all of that from scratch. For LiveSQLBench-Large with ~1K columns per DB, the built-in file system context management and subagent spawning aren't optional — they're needed to avoid context overflow.

```python
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model

agent = create_deep_agent(
    model=init_chat_model("openai:kimi-k2"),  # Tinker endpoint
    tools=[ghost_schema, ghost_sql, ghost_connect],
    system_prompt="You are an expert SQL analytics agent. ..."
)
```

`create_deep_agent` returns a compiled LangGraph graph — use it with streaming, Studio, checkpointers, or any LangGraph feature.

---

## 🔥 Why Tinker for Inference + Training

Tinker now has an OpenAI API-compatible inference interface — it plugs into any OpenAI-compatible platform by just specifying the model path. That means deepagents uses Tinker as a drop-in.

For the SFT loop: Tinker lets you fine-tune open-weight models like Qwen and Llama, including large MoE models like Qwen3-235B-A22B. You write a simple loop that runs on a CPU machine, and Tinker handles distributed training across GPUs.

The flywheel:
```
eval run → passing examples (question + schema + gold_sql)
→ SFT dataset → Tinker LoRA fine-tune on Kimi K2 Thinking
→ better base model → next eval run → higher score
```

---

## 📊 Benchmark: LiveSQLBench (Base-Lite)

**HuggingFace:** `birdsql/livesqlbench-base-lite` — 270 tasks, 18 Postgres DBs  
**GitHub + eval scripts:** `github.com/bird-bench/livesqlbench`  
**Leaderboard:** `livesqlbench.ai`

**Published baselines (model track, Base-Lite):**

| Model | Success Rate |
|-------|-------------|
| o3-mini | 47.78% |
| GPT-4.1 | ~44% |
| o4-mini | ~42% |
| Gemini 2.5 Flash | ~37% |
| Claude Opus 4.6 (all datasets) | 36.44% |

**Demo target arc:** ~30% → ~37% → ~43% across 3 iterations  
**Demo subset:** 50 questions per run

---

## 🖥️ Frontend Plan (React + Recharts)

### View 1 — Live Eval Run Showcase
- Stream one LiveSQLBench question through the agent in real-time
- Panel showing: NL question → agent todo steps → SQL generated → execution result
- Pass/Fail badge, token cost, latency, Ghost fork ID

### View 2 — Benchmark Dashboard
- **Line chart**: our agent's Success Rate across iterations
- **Dotted reference lines**: published model baselines (o3-mini, GPT-4.1)
- **Category breakdown bar**: SELECT vs CRUD per iteration
- **Prompt diff panel**: side-by-side diff of system prompt Iter 1 vs Iter 3
- **SFT counter**: "Training examples collected: 47 → 89 → 134"
- **Model badge per iteration**: "Base Kimi K2" → "Kimi K2 + Tinker LoRA"

---

## 📁 Repo Structure

```
deep-agent/
├── agent/
│   ├── agent.py           # create_deep_agent entrypoint
│   ├── tools.py           # ghost_schema, ghost_sql, ghost_connect
│   └── prompts.py         # system prompt (optimized per iteration)
├── eval/
│   ├── score.py           # LiveSQLBench pass/fail scoring
│   ├── dataset.json       # 50-question subset
│   └── ground_truth/      # gold SQL files
├── pipeline/
│   ├── ingest.py          # Airbyte → Ghost main DB
│   ├── fork.py            # ghost fork per iteration
│   └── loop.py            # full improvement loop orchestration
├── training/
│   ├── collect_sft.py     # format passing evals as SFT data
│   └── tinker_train.py    # Tinker LoRA training loop
├── .overclaw/
│   ├── policies.md        # SQL agent policy
│   └── eval_spec.json     # scoring criteria
├── frontend/
│   ├── src/
│   │   ├── EvalRunView.tsx      # live run showcase
│   │   └── Dashboard.tsx        # benchmark charts
│   └── package.json
├── experiments/
│   ├── iteration_1/       # traces, scores, prompt, agent version
│   ├── iteration_2/
│   └── iteration_3/
├── PLAN.md
└── README.md
```

---

## 🎬 3-Minute Demo Script

**0:00–0:20** — Problem
> "Frontier models score under 40% on real SQL benchmarks. Manual tuning doesn't scale."

**0:20–1:00** — Show the agent running live (View 1)
> Stream one LiveSQLBench question. Agent plans, spawns a schema subagent, writes SQL, executes against a Ghost fork. Pass ✅.

**1:00–2:20** — Show the improvement story (View 2)
> Dashboard: 3 iterations, score climbing from 30% → 43%. Prompt diff shows what Overclaw changed. SFT counter shows training data accumulating. Iter 3 uses Tinker LoRA.

**2:20–3:00** — Close
> "Three iterations, no human in the loop. The agent audits itself, Kiro fixes its code, Macroscope reviews it, Tinker trains the next version. This is self-improving infrastructure."

---

## ⚡ Build Order (11am → 4:30pm)

| Time | Task |
|------|------|
| 11:00–11:30 | Kiro scaffolds repo + Ghost CLI + Airbyte pipeline to Ghost |
| 11:30–12:15 | deepagents agent with Ghost tools + eval scoring script |
| 12:15–1:00 | Load 50-question subset, run Iteration 1 baseline |
| 1:00–1:30 | 🍕 Lunch — Iter 1 runs in background |
| 1:30–2:15 | Wire Overclaw / Truefoundry tracing + improvement loop |
| 1:45 | Start Tinker SFT job on Iter 1 passing evals (async, background) |
| 2:15–3:00 | Run Iter 2 + 3, collect results |
| 3:00–3:45 | Frontend: Dashboard + Live Eval View (Kiro builds this) |
| 3:45–4:15 | Polish, record demo video, write README |
| 4:15–4:30 | Submit Devpost + push public GitHub |

---

## 🔑 Open Decisions

- [ ] **Overclaw API key**: Try Overclaw first. If blocked, Truefoundry for tracing + manual prompt round still tells the story.
- [ ] **Tinker inference**: Confirm OpenAI-compat endpoint works with deepagents `init_chat_model`. Should be a base URL + model string swap.
- [ ] **Tinker SFT**: Start the job at 1:45pm regardless of how many examples (even 20 is fine). Show it running in the dashboard.
- [ ] **RL vs SFT**: SFT first (simpler). RL is the pitch closer: "and for the next step, we run RL on the failure traces."
- [ ] **Frontend**: React + Recharts. Kiro should scaffold this in ~30 min from a spec.
