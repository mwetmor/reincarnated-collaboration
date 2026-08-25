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

---

## ⚑ VERIFICATION RECORD — 2026-08-25 (knight-rider, per Matt agenda item 4: *"verify machine-wide in the first hour; record the check either way"*)

### Part A — the check as ordered. FACT: the var is UNSET on every surface.

Six surfaces checked, all negative:

| Surface | Result |
|---|---|
| Live process env (`env \| grep ENABLE_PROMPT_CACHING_1H`) | unset |
| `~/.zshrc` · `~/.zshenv` · `~/.zprofile` · `~/.bash_profile` · `~/.bashrc` | absent from all five |
| `~/.claude/settings.json` | present, `env` block is `{}` |
| `~/Games/reincarnated-collaboration/.claude/settings.local.json` | present, `env` block is `{}` |
| `~/.claude/settings.local.json` · project `.claude/settings.json` | do not exist |
| `launchctl getenv ENABLE_PROMPT_CACHING_1H` | empty |

The **only** occurrences anywhere under `~/.claude` are (a) session transcripts of agents *discussing* this row since 2026-08-23, and (b) the vendor changelog. **Nothing has ever set it.** The agenda line is closed: the loop is now dated in both directions.

### Part B — SEPARATE FINDING, not part of the ordered check: the U-3 premise is in question.

The check was ordered on the premise stated in "Why" above. Verifying the var's absence surfaced evidence against that premise, so it is recorded here rather than acted on.

1. **The changelog entry that introduced the var scopes it away from this machine's auth path.** `~/.claude/cache/changelog.md:282` — *"Added `ENABLE_PROMPT_CACHING_1H` env var to opt into 1-hour prompt cache TTL **on API key, Bedrock, Vertex, and Foundry**."* Matt's auth is **Max-subscription-only**: `~/.zshrc:1` reads `# ANTHROPIC_API_KEY removed 2026-06-12 — Claude Code must bill the Max subscription, not console credits`, and the live env has zero API-key entries. None of the four named surfaces is the surface in use.
2. **A later changelog line implies subscribers already get the 1-hour TTL by default.** `changelog.md:293` — *"Fixed subscribers who set `DISABLE_TELEMETRY` falling back to 5-minute prompt cache TTL instead of 1 hour."* The bug being *fixed* is subscribers falling **to** 5 min; the corrected baseline it restores them **to** is 1 h.

**Consequence:** on this machine's auth path the prescribed action may be a **no-op**, and U-3's headline — *"possibly the largest single cost lever on the board"* — is unevidenced as stated. This does not refute it; it removes its support. Installed CC version at check time: **2.1.119**.

**This is not a reason to skip the export** (one line, no downside if inert). It is a reason not to let the July-burn diagnosis rest on it. If the export is made and July-class burn persists, that is *not* a surprise to be re-investigated from scratch — it is the predicted outcome of Part B.

### Part C — a defect in the prescribed remedy, independent of Part B.

The Action above prescribes `~/.zshrc`. **That surface does not cover Remote Control servers or any non-interactive launch** — `.zshrc` is sourced for interactive shells only. Per `CLAUDE.md`, Remote Control is an established launch path on this Mac. If the action is taken at all, the correct surface is the **`env` block in `~/.claude/settings.json`** (currently `{}`), which applies to every Claude Code session on the host regardless of how the shell was entered. `~/.zshenv` is the shell-level equivalent if a shell var is genuinely wanted.

### Re-based empirical criterion

The original criterion ("how much of the July-class burn survives the cache fix") presumes the fix engages. **Re-based:** before treating the export as a cost lever, establish that TTL is actually 5 min on subscription auth — cheapest refuting test is a single long session with a >5-minute inter-turn gap, reading cache-read vs cache-creation token attribution across the gap (`/usage`). If cache-read is intact across a 20-minute gap, the premise is dead and U-3 closes as **NO-OP**, not as done.

**Recorded by:** knight-rider, 2026-08-25. **Disposition:** ordered check CLOSED (var unset, evidenced). Underlying action **still parked for Matt** — now with its premise flagged and its remedy surface corrected.
