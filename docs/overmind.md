# Overmind and Overclaw Sponsor Notes

## Why it matters here

Overmind and Overclaw are the best fit for the "self-improving agent" part of the pitch. They cover tracing, diagnosis, and automated improvement instead of only raw execution.

Sources reviewed:

- Existing repo copy of the Overclaw docs in the previous version of this file
- https://docs.overmindlab.ai/guides/overclaw_doc

## What Overclaw is good for

Overclaw is an optimizer. It runs an agent against a dataset, traces calls, scores outputs, proposes fixes, validates candidates, and keeps only improvements.

That lines up well with the project's loop:

1. Run LiveSQLBench subset.
2. Score pass/fail.
3. Inspect traces.
4. Generate prompt or logic improvements.
5. Re-run and keep only better versions.

## Recommended sponsor path

### Safer path for hackathon

Use Overmind SDK style tracing first, then do manual prompt iteration if needed.

Why:

- Lower integration risk.
- Still gives you a sponsor-aligned tracing story.
- Avoids overcommitting to a full optimizer if the core agent is not stable yet.

### Stronger path if time allows

Use Overclaw for one controlled optimization loop on a small eval set.

Good constraints:

- 10 to 20 representative tasks first.
- Stable scoring function.
- One prompt file and one agent entrypoint.

## What to wire

- Trace every agent run and tool invocation.
- Save the current system prompt and eval result with each iteration.
- Keep one artifact per iteration: score, prompt diff, and notable failure pattern.

## Minimal process

1. Run baseline eval.
2. Capture traces.
3. Review failures.
4. Change prompt or tool descriptions.
5. Re-run holdout subset.
6. Accept only if score improves.

## Hackathon guidance

- Treat Overmind tracing as the default path.
- Treat full Overclaw optimize loops as a stretch upgrade once scoring is reliable.
- Do not let optimizer complexity block the baseline benchmark demo.

## Links worth keeping

- Overclaw docs: https://docs.overmindlab.ai/guides/overclaw_doc
- Overmind docs root: https://docs.overmindlab.ai/
