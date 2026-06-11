# Gamora (Fable-5) — Spatial-Fidelity Re-Profile (follow-up to the throughput consult)

**STATUS:** FOLLOW-UP COMMISSION — paste-ready opener for the Gamora session that just delivered the throughput profile (or a fresh Fable-5 Gamora session)
**Date:** 2026-06-10
**Author:** gandalf (Opus 4.8)
**Predecessor:** `agentic_orchestration/gamora/notes/2026-06-10-sim-throughput-profile-and-runner-architecture.md` (your throughput profile, commit d6f6871)
**Why this follow-up exists:** Matt identified that the profiled sim is NOT the combat the game actually has. The numbers you measured (0.81 s/kit) are the **current 1-vs-1, 1-D-distance abstraction** (`fight_engine.py` state_a/state_b + scalar `distance_m`). The real game's combat is **spatial and multi-actor** — and crucially, an **older engine version already implemented it and left real battle data.** So the fidelity question is empirically answerable, not a guess.

**Launch:** `cd ~/Games/reincarnated-engine && claude --agent gamora --model claude-opus-4-8`

---

## PASTE-READY OPENER (everything below the line)

---

You are gamora. Read your OP, run session-start, and read your own throughput-profile deliverable from earlier (`agentic_orchestration/gamora/notes/2026-06-10-sim-throughput-profile-and-runner-architecture.md`) — this is a direct follow-up to it. Then take on the redirect below.

**Mission: re-profile per-kit cost against the REAL spatial, multi-actor combat — using actual battle data from the older spatial engine version — and re-project the 4,000-variant wall-clock from that.**

### The correction (from Matt)
Your throughput profile measured today's fight engine, which is a **1-vs-1 duel on a 1-D distance line** (no spatial zones, no summons, no multi-actor). That is NOT the game's actual combat. **An older version of the engine ran kits through actual spatial battle:**
- **5 2-D spatial zones**
- **5 battle types: swarmer, trash, mini-boss, boss, and small hallway / gauntlet**

That older spatial engine produced **real battle telemetry.** Your job is to find the most recent such data and measure the *real* combat cost from it — not estimate a multiplier off the abstracted duel.

### Critical scoping instruction (don't measure the wrong thing)
The old spatial runs were slow **primarily because of a combinatorial iteration strategy** — after roughly the first ~30 runs, it iterated combinatorially and exploded. **DISREGARD that combinatorial-iteration overhead entirely.** We are NOT iterating combinatorially anymore — the new strategy is **launching 10× variants per general kit** (the 40 general kits × 10 variants → ~4,000 model). So:
- Measure the **per-fight and per-kit cost of the spatial battle itself** (the 5 zones × 5 battle types), isolated from the combinatorial-search strategy that wrapped it.
- Then project **~4,000 kit-variants** (400 × 10×) through that spatial combat under the parallel-runner architecture from your prior deliverable — NOT through a combinatorial explosion.

### What I need (deliverable contents)
1. **Locate the spatial-engine battle data** — the most recent telemetry from the 5-zone / 5-battle-type version. State exactly what you found (paths, dates, run counts) and how recent it is. If the spatial engine *code* still exists, note where; if only telemetry survives, profile from the telemetry. If neither survives in usable form, say so plainly and estimate with explicit, flagged assumptions (don't fabricate measured numbers).
2. **Real per-fight / per-kit cost under spatial multi-actor combat** — measured (or telemetry-derived), broken down by the 5 battle types where the data allows (swarmer and boss-with-adds will cost very differently — actor count is the cost driver). Mark measured-vs-assumed on every number per Discipline #40.
3. **The honest multiplier** — how much more expensive is real spatial combat than the 1-D duel you profiled? This is the number that tells us whether the 12-minute figure was optimistic, and by how much.
4. **Re-projected 4,000-variant wall-clock** — under the parallel-runner architecture (§ 5 of your prior deliverable: parallel + T1 surrogate filter + warm-start + full-fidelity gate on the final 400), using the SPATIAL per-kit cost. The headline: "real combat, 4,000 variants → *what* wall-clock, on Mac vs. the PC's 20-core box vs. (only if needed) cloud."
5. **Updated greenfield + contract flags** — does the spatial-combat cost change your "wrap, don't rebuild" verdict? (Throughput-wise it likely still holds — spatial multi-actor is heavier per tick but still CPU-bound / O(n) / parallel.) And update the sim-side contract number for the generation↔sim forward-architecture: "~X s per spatial kit-variant validation; ~Y min per 4,000-variant sweep."

### Disciplines (carry over)
- **Empirical-first** — use the real spatial data; don't extrapolate a guess if the data exists. Mark measured-vs-assumed.
- **Preserve resolver math (crown jewel)** — same as before; this is a measurement + runner question, not a math rewrite.
- **Surrogate-for-search / full-fidelity-gate-on-the-final-400** — non-negotiable; the spatial gauntlet is the ship gate.
- **Scaffold register** — every assumed number flagged; especially flag any place where you're inferring spatial cost from partial/old telemetry.

### Output
Append to your existing deliverable as a new section (§ 10 "Spatial-fidelity re-profile") OR write a companion note `agentic_orchestration/gamora/notes/2026-06-10-spatial-fidelity-reprofile.md` — your call. Auto-commit authorized. Report: the data you found (and how recent), the real spatial per-kit cost, the multiplier over the 1-D duel, and the re-projected 4,000-variant wall-clock.
