# Phase 7: Git-Based Versioning

## Goal

Make every benchmark iteration traceable to an exact code and prompt revision.

## Scope

- branch naming
- commit conventions
- tags for major checkpoints
- experiment metadata with Git references

## Deliverables

- `docs/AGENT_VERSIONING.md`
- Git initialization if not already present
- iteration metadata that records branch and commit SHA

## Tasks

1. Initialize Git if the repo is not already versioned.
2. Commit the scaffold and baseline separately.
3. Use iteration branches when making meaningful agent changes.
4. Record `git_sha` and `git_branch` inside experiment metadata.
5. Tag milestone builds that may be shown in the demo.

## Validation

- every experiment folder maps to a commit
- important milestones have tags
- prompt changes are versioned like code changes

## Exit criteria

- the improvement story is defensible from code history alone
- a later iteration can be compared directly against baseline in Git

## Risks

- running experiments before committing changes creates ambiguity
- prompt edits can be forgotten if treated as scratch notes

## Notes

- This phase is mandatory for the benchmark narrative.
- Macroscope review can layer on top later, but Git history is the core source of truth.
