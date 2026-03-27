# Auth0 Sponsor Notes

## Why it matters here

Auth0 is the sponsor that can make the demo feel safe instead of just capable. For this project, the highest-value Auth0 features are:

- User authentication for the frontend demo and any operator dashboard.
- Token Vault if the agent ever calls Slack, GitHub, Gmail, or other third-party tools on behalf of a user.
- Asynchronous authorization for human approval on high-risk actions.
- Fine-grained authorization for any future RAG layer.

Official docs reviewed:

- https://auth0.com/ai/docs/intro/overview
- https://auth0.com/ai/docs/sdks/overview

## Best fit for this hackathon

Recommended scope:

1. Add Auth0 login to the demo frontend.
2. Gate sensitive actions behind authenticated user context.
3. Treat Token Vault and async authorization as stretch goals unless you actually ship tool calling.

That keeps the sponsor story real without expanding the project too far.

## What the official docs say

- Auth0 for AI Agents is positioned around four core patterns: user authentication, calling your own APIs on behalf of a user, calling third-party APIs through Token Vault, and async human approval for critical actions.
- Auth0 publishes SDKs for JavaScript, Python, LangChain, LlamaIndex, Vercel AI, Cloudflare, and Genkit.
- Their sample apps lean toward full-stack agent apps with secure tool calling and approval flows, which is relevant if this project grows beyond SQL-only execution.

## Practical integration plan

### Phase 1: login only

- Protect the frontend and any evaluation dashboard.
- Store Auth0 domain, client ID, and app callback URLs in env.
- Add user identity to traces and experiment metadata.

### Phase 2: operator approvals

- Require explicit approval before any destructive or external action.
- Good fit if the agent evolves from read-only SQL analytics into write actions or tool execution.

### Phase 3: secure third-party tool access

- Use Token Vault only if you truly need GitHub, Slack, or similar tools on behalf of a user.
- Do not add this just for sponsor checkbox value.

## Skill status

Installed:

- `auth0/agent-skills@auth0-quickstart`

Notes:

- The installed skill is general-purpose and helps route to the right Auth0 workflow by framework.
- Restart Codex to pick up new skills.

## Build checklist

- Create an Auth0 app for the actual frontend framework once the app exists.
- Keep callback and logout URLs aligned with local dev ports.
- Do not commit Auth0 secrets.
- If the frontend is Next.js, use the dedicated Auth0 Next.js path instead of a generic quickstart.

## Links worth keeping

- Overview: https://auth0.com/ai/docs/intro/overview
- SDK overview: https://auth0.com/ai/docs/sdks/overview
- AI samples: https://auth0.com/ai
- Next.js examples: https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md
