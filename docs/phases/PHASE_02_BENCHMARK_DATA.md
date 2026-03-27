# Phase 2: Benchmark Data

## Goal

Download a small LiveSQLBench subset and make at least one benchmark database queryable inside Ghost.

## Scope

- dataset download
- small eval subset creation
- one benchmark schema and sample data loaded into Ghost

## Deliverables

- `scripts/download_benchmark.py`
- `scripts/sqlite_to_postgres_sql.py`
- `eval/dataset.json`

## Tasks

1. Download the benchmark metadata and inspect the field structure.
2. Save a small evaluation subset locally.
3. Choose the smallest useful database to load first.
4. Generate a Postgres-compatible SQL load script from the SQLite benchmark DB.
5. Load schema and data into the Ghost main database through `ghost sql`.
6. Verify at least one benchmark question maps to real tables in Ghost.

## Validation

- local dataset file exists
- at least one benchmark DB is live in Ghost
- manual SQL queries return expected rows

## Exit criteria

- `eval/dataset.json` exists
- one benchmark question can be answered against Ghost-backed data

## Risks

- benchmark packaging may be more complex than the docs imply
- loading all databases may take too long for the first pass

## Notes

- Start small. One database and a narrow dataset slice is enough to unlock Phase 3.
- Airbyte stays out unless direct loading becomes a bottleneck.
- The official SQLite variant is the fastest practical source for benchmark DB assets in this environment.
