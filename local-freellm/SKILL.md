

# freellm

## Purpose
Free, no-API-key LLM access for light tasks. Since 2026-10-14 routes through a
local FreeLLMAPI instance (tashfeenahmed/freellmapi, MIT) at
a local FreeLLMAPI checkout (`$FREELLMAPI_HOME`) → `http://localhost:3001`, model
`pollinations-openai` pinned (verified: clean Chinese output, ~4s). The
router's `auto` mode was rejected: it picks reasoning-distilled free models
that leak chain-of-thought into answers. Fallback chain: local router →
Gemini (`gemini-3.8-flash` via stored Secure Vault credential
`custom.google-ai-studio`, helper
a Gemini chat helper script (`$GEMINI_CHAT_PATH`),
verified 2026-10-20, ~22s) → direct Pollinations anonymous endpoint.

## Tooling
CLI: `bin/freellm.py` in this skill folder.
Stdlib only (`urllib` + `sqlite3`), no dependencies. Starts/restarts the local
router with `$FREELLMAPI_HOME/start.sh` (no-op if already running).
The router's unified key is read at runtime from its own sqlite DB
(`server/data/freeapi.db`) — localhost-only, locally generated, never stored
in files or printed. Usage:

```
# one-shot prompt
python3 bin/freellm.py "prompt text"
# with system prompt / longer output
python3 bin/freellm.py --system "you are a copywriter" \
  --max-tokens 800 "prompt text"
# list current models
python3 bin/freellm.py --models
```

Prints the assistant text to stdout; exits non-zero with the error on stderr on
failure. Reads prompt from argv; if argv is empty, reads stdin.

## Auth
None. Anonymous tier, no key, no credential helpers. Never attach any stored
credential to these requests, and never ask the user for a key for this skill.

## Operating Rules
1. Use for LIGHT tasks only: drafting, rewriting, X/video copy, summarization,
   simple code snippets, classification, first-pass triage. Goal is to save
   Muse tokens and the OpenRouter `:free` 50/day quota.
2. Do NOT use for: stock scoring (VModel/USModel), financial analysis,
   deep-research verdicts, or anything where a wrong answer costs money.
   Those stay on Muse / OpenRouter.
3. Default model is `pollinations-openai` via the local router (pinned
   2026-10-14 for output quality); `--model auto` exists but often returns
   thinking-trace leakage — avoid unless experimenting. `--models` lists the
   router's catalog (214 entries, most need real provider keys; only the
   keyless-configured ones actually answer).
   Backup keyed model (2026-10-19): `agnes-2.5-flash` / `agnes-3.0-flash`
   (Agnes AI, currently $0 promo) — user's key stored encrypted in the
   router's own DB (api_keys, platform='agnes'); verified end-to-end via the
   local router. Use when the Pollinations route is degraded. Note: this
   model sometimes leaks reasoning narration into the answer — spot-check.
4. Gemini route (2026-10-20): user's own Google AI Studio free key stored in
   Secure Vault as connector `custom.google-ai-studio`; the key is never
   readable, only used through a surrogate on approved requests to
   generativelanguage.googleapis.com (`x-goog-api-key` header). Free-tier
   data may be used by Google to improve products — same light-work-only
   scope as the rest of this skill, never stock/money/model-code.
5. Treat output as a draft: it can be weaker at reasoning and may hallucinate.
   Spot-check anything factual before it reaches the user.
6. If the local server is down, the CLI tries Gemini next, then direct
   Pollinations automatically (stderr notes each hop). Restart the router with
   `$FREELLMAPI_HOME/start.sh`. If all fail repeatedly, fall back
   to the OpenRouter skill; do not retry in a tight loop.
## Available connectors

Use `muse.connector_search` to find the current connector docs before following
recovered instructions.
