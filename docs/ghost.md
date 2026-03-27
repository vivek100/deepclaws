# Ghost Sponsor Notes

## Why it matters here

Ghost is the cleanest sponsor fit in the whole stack. The project needs isolated Postgres environments and cheap forking for repeated eval runs, and Ghost is built exactly for that.

Official docs reviewed:

- https://ghost.build/docs/

## What the official docs confirm

- Ghost provides managed Postgres databases with unlimited forks inside a bounded "Space".
- The CLI supports `create`, `list`, `connect`, `fork`, `pause`, `resume`, `schema`, `sql`, and `logs`.
- Ghost has first-party MCP support through `ghost mcp install`.
- The MCP exposes database lifecycle tools plus `search_docs` and `view_skill`.

## Recommended role in this project

Use Ghost as the canonical database runtime for every benchmark iteration:

1. Create one main database for loaded LiveSQLBench data.
2. Fork it per experiment run.
3. Run the agent against the fork.
4. Pause or delete forks after the eval.

That directly supports the core demo story: repeatable, isolated evaluation loops.

## Minimum command path

```powershell
ghost login
ghost create --name livesqlbench-main
ghost connect livesqlbench-main
ghost fork livesqlbench-main --name livesqlbench-iter-1
ghost schema livesqlbench-iter-1
ghost sql livesqlbench-iter-1 "select 1;"
ghost pause livesqlbench-iter-1
```

## MCP path

```powershell
ghost mcp install
ghost mcp list
```

The MCP tools most relevant to this repo are:

- `ghost_fork`
- `ghost_connect`
- `ghost_schema`
- `ghost_sql`
- `ghost_pause`

## Hackathon guidance

- Ghost is not optional for the current architecture. It is part of the main product story.
- Prefer a single seeded source database plus many forks instead of recreating schemas for each run.
- If time gets tight, prioritize `create`, `fork`, `connect`, `schema`, and `sql`.

## Links worth keeping

- Docs: https://ghost.build/docs/
- Install script for Windows PowerShell: `irm https://install.ghost.build/install.ps1 | iex`
