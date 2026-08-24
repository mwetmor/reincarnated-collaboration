# U-3 — Set `ENABLE_PROMPT_CACHING_1H=1` machine-wide (cache-TTL fix)

**Parked:** 2026-08-23 (gandalf, workflow-upgrades U-3; research of record same date). **Non-blocking but cost-critical** — possibly the largest single cost lever on the board, and it's one env line.

## Why (~30 seconds of context)

On Claude subscriptions, prompt-cache TTL silently drops **1 h → 5 min** once usage credits engage, unless this env var is set. Any long-running session with >5-minute gaps between turns then reprocesses its FULL context at every gap — at undiscounted API rates once credits are billing. Part of the late-July token exhaustion (the 2.5-day throttled multi-arm run) may have been cache thrash, not genuine demand. (Anthropic docs primary; research of record 2026-08-23.)

## Action (~2 minutes, Mac)

1. Append to `~/.zshrc`:
   ```bash
   export ENABLE_PROMPT_CACHING_1H=1
   ```
2. `source ~/.zshrc` (or open a fresh terminal).
3. Restart any long-lived Claude Code sessions / Remote Control servers so they inherit the var — sessions launched before the export won't have it.

## What it unblocks

- The empirical criterion for U-3 itself: how much of the July-class burn survives the cache fix (measured on comparable work post-fix, via `/usage` attribution).
- Gates the scale decision on U-4 (serialized Codex lane) — if most of the burn was cache thrash, the cost case for offloading changes shape.

**Source:** `agentic_orchestration/workflow-upgrades.md` § U-3.
