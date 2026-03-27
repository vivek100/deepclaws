# Airbyte Sponsor Notes

## Why it matters here

Airbyte is the ingestion story. In this project it is less important than Ghost, but still useful because the benchmark data has to land somewhere repeatable before the eval loop starts.

Official docs reviewed:

- https://docs.airbyte.com/

Installed skill reviewed:

- `airbytehq/airbyte-agent-connectors@airbyte-agent-connectors`

## What the official docs confirm

- Airbyte positions itself as a data integration and agentic data platform.
- The docs cover replication, connectors, developers, and AI-agent features.

## Best fit for this hackathon

Use Airbyte for the benchmark data ingestion narrative:

- Source: benchmark files or upstream dataset export
- Destination: the main Ghost Postgres database
- Outcome: repeatable seeding before forking

This is a good sponsor story, but it should not block the rest of the build. If setup becomes slow, seed Postgres directly and keep Airbyte as the planned production ingestion path.

## About the installed skill

The installed Airbyte skill is not the generic replication setup guide. It is focused on Airbyte Agent Connectors for third-party SaaS APIs.

That means:

- It is useful if the project later needs SaaS tool access through typed Python connectors.
- It is not the main tool for loading LiveSQLBench into Postgres.

Risk note:

- The skill registry flagged this install with a high-risk Snyk assessment. Treat it as documentation to inspect before use, not a trusted dependency to wire in blindly.
- Restart Codex to pick up new skills.

## Recommended project stance

- Use Airbyte branding and docs for ingestion architecture.
- Do not force the connector skill into the benchmark pipeline unless you actually need its SaaS connector model.
- Keep the fallback simple: direct load into Ghost, then fork from there.

## Links worth keeping

- Airbyte docs: https://docs.airbyte.com/
- Airbyte AI agents docs: https://docs.airbyte.com/ai-agents
- Skill repo: https://github.com/airbytehq/airbyte-agent-connectors
