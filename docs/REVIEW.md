# Docs Review

## Main docs

### `PLAN.md`

What is strong:

- Clear one-line pitch.
- Cohesive sponsor narrative.
- Good architecture shape for a hackathon demo.

What needs tightening:

- There are visible encoding artifacts throughout the file.
- Several sponsor claims are still aspirational rather than verified implementation choices.
- The plan assumes both tracing and automated optimization; those should be separated into baseline and stretch scope.

### `SETUP.md`

What is strong:

- The file already captures most of the desired stack in one place.
- The integration order mostly makes sense.

What needs tightening:

- Some commands are clearly illustrative and should be labeled as unverified templates.
- Airbyte, Tinker, and Overclaw sections are ambitious for a hackathon and need fallback paths.
- The file should eventually split into "must ship" vs "nice to ship".

## Sponsor docs

Before this pass:

- `ghost.md` was only a URL.
- `macroscrope.md` was only a URL.
- `Autho0.md` was a raw link dump.
- `overmind.md` was mostly pasted vendor copy instead of project guidance.

After this pass:

- Each sponsor doc is now a project-focused internal note.
- Added `SPONSORS.md` as a single matrix for priority and implementation stance.
- Added `airbyte.md` because Airbyte is in the plan and now has an installed skill to track.

## Recommended next doc cleanup

1. Fix encoding issues in `PLAN.md`.
2. Split `SETUP.md` into baseline setup and stretch integrations.
3. Add a `README.md` once code exists, using `PLAN.md` as source material instead of keeping everything in one giant planning file.
4. Keep local CLI utilities explicit in the plan so frontend/API work later wraps real execution paths.
