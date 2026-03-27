# Phase 3: Runnable Agent

## Goal

Build the first SQL agent that can inspect Ghost schema and generate executable SQL.

## Scope

- Ghost-backed tools
- initial system prompt
- runnable agent entrypoint

## Deliverables

- `agent/tools.py`
- `agent/prompts.py`
- `agent/agent.py`

## Tasks

1. Implement `ghost_schema`.
2. Implement `ghost_sql`.
3. Implement `ghost_connect`.
4. Write the first SQL-focused system prompt.
5. Create an entrypoint that runs one benchmark question through the agent.

## Validation

- agent can read schema
- agent returns SQL for hand-picked prompts
- at least one generated query can be executed against Ghost

## Exit criteria

- the project has a runnable agent shell
- the agent produces SQL on real benchmark-backed inputs

## Risks

- prompt too weak for multi-table joins
- tool outputs too noisy for the model to use well

## Notes

- Keep the first version simple and debuggable.
- Do not optimize before you can run and inspect failures.
