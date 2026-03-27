# Macroscope Sponsor Notes

## Why it matters here

Macroscope is the review and observability layer for code changes around the self-improvement loop. It is not the core runtime, but it strengthens the "agent improves itself and gets reviewed" story.

Official docs reviewed:

- https://docs.macroscope.com/setup-instructions

## What the official docs confirm

- Setup starts by connecting GitHub repositories.
- Macroscope processes recent repo activity and new changes going forward.
- It can generate commit and PR summaries, review PRs for correctness issues, and suggest fixes.
- Product context matters: the docs explicitly recommend adding a product overview in workspace settings so reviews and summaries are more accurate.

## Recommended role in this project

Use Macroscope for PR review on agent-generated or optimization-generated changes:

1. Connect the repo once code exists in GitHub.
2. Add a concise product overview describing the SQL agent, eval loop, Ghost forking, and sponsor constraints.
3. Route each improvement branch through Macroscope review before merging.

## Practical setup

1. Sign up at `app.macroscope.com`.
2. Connect the GitHub repo.
3. Activate code review.
4. Add the project overview in workspace settings.
5. Optionally connect Slack for team visibility.

## Hackathon guidance

- This is a secondary sponsor integration, not a blocker.
- It becomes valuable once the repo has actual code and PRs to review.
- Do not spend early build time here before the agent, eval loop, and Ghost flow exist.

## Links worth keeping

- Setup docs: https://docs.macroscope.com/setup-instructions
- App: https://app.macroscope.com
