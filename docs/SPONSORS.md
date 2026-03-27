# Sponsor Integration Matrix

## Current status

| Sponsor | Project role | Priority | Status | Notes |
|---|---|---:|---|---|
| Ghost | Database runtime and per-run forks | High | Strong fit | Core sponsor for the actual benchmark loop |
| Overmind / Overclaw | Tracing and automated improvement | High | Strong fit | Start with tracing, add optimizer only if baseline works |
| Airbyte | Data ingestion into Ghost | Medium | Partial fit | Good architecture story, but direct load fallback is fine |
| Macroscope | PR review on generated changes | Medium | Secondary | Useful once repo has actual code and PRs |
| Auth0 | Login, secure tool access, approvals | Medium | Stretch fit | Strong if frontend or external tool calling ships |

## Installed skills

Installed in the user skill directory:

- `auth0/agent-skills@auth0-quickstart`
- `airbytehq/airbyte-agent-connectors@airbyte-agent-connectors`

Notes:

- Restart Codex to pick up new skills.
- The Airbyte skill install reported a high-risk Snyk assessment, so review it before relying on it.

## What to build first

1. Ghost-backed benchmark execution.
2. Eval scoring and saved experiment outputs.
3. Overmind tracing around the agent loop.
4. Airbyte ingestion only if direct loading is too brittle to explain.
5. Auth0 and Macroscope once there is a UI or PR workflow worth securing and reviewing.
