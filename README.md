Field-tested skills for AI agents: free-model routing, free-offer verification, and design discipline.

# Agent Skills Pack

A curated set of agent skills, each battle-tested in daily operation. Every skill is a self-contained folder with a `SKILL.md` you can drop into any agent framework that reads skill files.

## The skills

- **local-freellm** — Route light work (drafting, rewriting, summarization, classification) to a free, no-key local LLM router, with a helper CLI and hard rules about what must never be routed there (money judgments, personal data, credentials).
- **local-aider** — Drive the Aider coding CLI against free OpenRouter models as a one-shot, non-interactive worker: exact invocation pattern, environment quirks, and failure modes.
- **local-freetoken-bots** — Discover and health-check zero-priced OpenRouter models for child-agent workflows: a radar script, quota-safe fallback rules, and a daily health-check routine.
- **verify_free_offer_before_counting** — Verify a "free" offer against its official terms and one live call before counting it as available — including the unauthenticated-vs-authenticated control pair that stops a blocked egress from being misread as a dead key.
- **evaluate_before_adopt** — A structured gate for evaluating a tool, post, or tutorial before adopting it: extract the workflow, verify the claims, run a minimal trial, then file it as a reusable skill.
- **check_delivered_before_offering** — Before offering the user anything, check what was already delivered and what inventory actually exists — no duplicate offers, no filler substitutes for an empty format.
- **local-design-system** — Design-system discipline for HTML/CSS pages and print pieces: decide a direction and define tokens before layout, with font, anti-slop, and accessibility rules.

## License

MIT — see `LICENSE`.
