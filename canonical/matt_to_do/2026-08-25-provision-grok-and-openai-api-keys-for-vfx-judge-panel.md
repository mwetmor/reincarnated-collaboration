# matt_to_do — Provision xAI (Grok) + OpenAI (Codex) API keys for the VFX describe/judge panel

**Filed:** 2026-08-25 (gandalf, RUN-CONDUCTOR — VFX-DEPTH run charter R-13).
**Class:** credential provisioning — only you can do this. **Effort:** two console visits + two env vars.

## What it unblocks

Charter R-13 (your ruling: *"more than one pass and from more than one model — we can call claude, grok and codex"*): the Grok and Codex seats of the blind DESCRIBE panel (per-skill extraction) and the blind JUDGE panel (lap cadence). **Claude seats fire without this** — the run is not blocked, but until keys land the panel is single-family (correlated blindness).

## The ask

1. **xAI:** create an API key (console.x.ai) — Grok vision seats.
2. **OpenAI:** create an API key (platform.openai.com) — Codex/GPT seats.
3. Optional third: **Google AI Studio** key — Gemini is the one video-NATIVE candidate (true motion input rather than frame batches); your call whether to seat it.

## Key-hygiene note (the 2026-06-12 precedent binds)

Your `ANTHROPIC_API_KEY` was removed from `.zshrc` on 2026-06-12 precisely because globally-exported keys leak into every sub-agent. **Recommendation:** do NOT export these globally. Put them in a dedicated env file (e.g., `~/.config/reincarnated/panel-keys.env`, chmod 600) that ONLY the panel-call script sources. star-lord (llm/ seam) builds the call path against that file and never echoes keys into logs or receipts.

## Disposition options

(a) keys provisioned → panel seats activate next lap · (b) "Claude-only for now" — complete answer; R-13 records the panel as single-family by choice · (c) defer — seats stay gated, run proceeds.
