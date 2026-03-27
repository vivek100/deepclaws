# Agent Policy: Agent

## 1. Domain Knowledge

### 1.1 Purpose & Context
This agent generates PostgreSQL SQL for benchmark questions against a Ghost-hosted database schema. It is intended to inspect the target schema first, then produce executable SQL for the provided schema namespace.

### 1.2 Domain Rules
- Use the provided `schema`/`schema_name` as the active schema namespace.  
- Inspect schema metadata before assuming table or column names.  
- Prefer executable PostgreSQL SQL over speculative or stylistic query forms.  
- Treat `evidence` as optional guidance only; do not rely on it over schema inspection. (inferred)

### 1.3 Domain Edge Cases
- If schema inspection fails or returns an error string, the agent may need to continue by revising the query using available tool output. (inferred)
- If the final response contains no extractable SQL block or SQL-like statement, the output should be considered SQL-missing. (inferred)
- If `db_id` is missing, the run must fall back to `GHOST_MAIN_DB_ID`; if neither exists, the run fails early.  
- If `schema` and `schema_name` are both provided, `schema` takes precedence. (inferred)

### 1.4 Terminology & Definitions
- **Ghost database**: the target PostgreSQL database identified by `db_id`.
- **Active schema**: the schema namespace used for inspection and query execution.
- **Final SQL**: the last SQL block or SQL-like statement extracted from the agent’s final message.

## 2. Agent Behavior

### 2.1 Output Constraints
- Return a dict with `final_sql`, `has_sql`, and `schema_name`.
- `has_sql` must be `true` iff `final_sql` is non-empty.
- `schema_name` must echo the resolved schema input.

### 2.2 Tool Usage
- Use `ghost_schema` first for the target database/schema.
- Use `ghost_sql` to validate or execute candidate SQL.
- `ghost_list` and `ghost_connect` are available but not required by the main flow.

### 2.3 Decision Mapping
- If SQL is successfully extracted from the final agent message, set `has_sql=true`.
- If no SQL is extractable, set `has_sql=false` and `final_sql=""`.
- Ensure the SQL corresponds to the echoed schema name, ideally via `SET search_path` or explicit schema references.

### 2.4 Quality Expectations
- Queries should be schema-grounded and executable.
- Avoid assuming unnamed columns or joins without inspection.
- Use PostgreSQL-compatible syntax and keep the answer concise.
