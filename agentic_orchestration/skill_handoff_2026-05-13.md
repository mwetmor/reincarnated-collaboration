# Skill handoff — 2026-05-13 (Day 0)

**Audience:** knight-rider on first invocation.
**Purpose:** Project state snapshot at team-establishment moment.

This is the **founding handoff**. Subsequent handoffs (one per working day) are produced by knight-rider at session end and read by the next session's knight-rider at startup.

---

## Project state as of 2026-05-13

### Recent milestones shipped (engine, last 5 days)

| Tag | What | Date |
|---|---|---|
| `v1.3-b14-5-secondary-loop` | B14.5 V1 primary loop (recompose-first balance) | 2026-05-12 |
| `v1.3-b10-1-structure` | B10.1 tier structure + Model B gauntlet | 2026-05-12 |
| `v1.3-b14-5-primary-loop` | B14.5 V1 first cut | 2026-05-12 |
| `v1.3-b10-pre-rename` | B10 pre-rename checkpoint | 2026-05-12 |

### Loadout app — production state

URL: `https://reincarnated-loadout.vercel.app`

Tags in `reincarnated-loadout`:
- `v0.3.3-sample-gear` — synthesized gear by class affinity + game-icons.net SVGs
- `v0.3.2-sample` — Sample (Engine Baseline View) page
- `v0.3.1-flavor` — FlavorTip component wired everywhere
- `v0.3-mobile-deployed` — initial Vercel deploy

Live routes: `/loadout`, `/sample`, `/analytics` (6 of 9 charts)

Worktree: `~/Games/reincarnated-loadout-analytics/` exists (analytics-overnight branch, merged into main). Can be cleaned up: `git worktree remove ../reincarnated-loadout-analytics`.

### Recent Yomi season regen

- Season: `season_002328` (seed 2328)
- Anchor: Yomi (Japanese underworld, mythological_specific)
- Theme element: wind → miasma
- 10 classes generated, all converged, validation PASSED
- Cost: $0.98, 41.6 min wall time
- Worktree: `~/Games/reincarnated-engine-side-seed/` (can be cleaned up; data already copied into loadout repo and main engine repo)

---

## Active work queues by seam

### rocket — Content Generation

**Open:**
- D1 element pool — recent quality adjustments (pall/miasma/rime/shear/billow demoted, hurricane/cloud added). Consider `vocabulary_commonness` sub-property in D1 rubric.
- B6 archetype templates — hunter template review (1.82 modifier range, widest in dataset per sidecar analysis)
- Earth_controller convergence slowness (7.0 avg iters — slowest archetype) — diagnostic warranted

**Cross-seam pending:** none currently

### gamora — Simulation + Spirit Guide

**Active:** B10.2 — pack-proxy (Model C) + native swarm composition rules

**Kickoff prompt drafted:** `~/Games/reincarnated-collaboration/b10-2-kickoff-prompt.md`

Key math-before-code items per kickoff:
- Pack size N (proposed 6-10)
- HP scaling factor (linear vs sub-linear)
- AOE multiplier mechanics
- Cost projection update
- Queued micro-fix: strengthen `len(tiers_present) >= 2` assertion

**Downstream open (deferred):**
- B14.5 V2 (evaluate-at-converged)
- B10 V2 (sequential rooms with HP carryover)

### star-lord — Output / Telemetry / LLM

**Open (queued for attention):**
- Telemetry field gaps (per sidecar analysis): `convergence_wall_time_seconds` empty, `engine_version` "unknown", `seasonal_element_name` empty, `termination_reason` missing from class_fight_loadouts
- LLM cost ledger formalization (currently informal; ~$0.85-1.00/season observed)
- Bow + dex affix pool empty (spawned task from May 12 work — non-fatal warning)

### drax — Presentation (demo + loadout)

**Open on loadout (queued for attention):**
- Gear effects rendering — base items shown without rolled effects from effect_pool (Matt flagged 2026-05-13). Real engine catalog data present; renderer doesn't read effect_pool. Scope: ~1-2 hrs. Tag: `v0.4-gear-effects`.
- Tailwind safelist trim — currently broad; refactor `className={\`...${dyn}...\`}` to static, then narrow safelist
- CC-BY attribution UI footer (currently in commit messages only)
- Tier 3 analytics (3 remaining charts)
- Add a git remote to the loadout repo for off-laptop backup

**Open on demo:** none active (demo1 shipped 2026-05-08)

### jack-ryan — Analyst / QA

**Open:**
- No pending Gate 2 items (this is Day 0)
- Drain `qa/pending/` as items arrive
- Reconsider: 12 disciplines complete; check whether B10.1 closeout surfaced anything new

---

## Coordination items for first session

1. **Verify worktree state.** Run `git worktree list` in both reincarnated-engine and reincarnated-loadout. Clean up stale worktrees if no active work depends on them.

2. **Initialize AGENT_STATE.md per seam.** Each developer's first session should create their checkpoint file. Format in AGENTS.md Section 4 Tactic 3.

3. **First task assignment.** Two strong candidates:
   - **gamora — B10.2** (kickoff prompt ready; math-before-code work clearly defined)
   - **drax — loadout gear effects** (clear scope, contained, ~1-2 hrs, ships v0.4-gear-effects)

   Suggest dispatching both in parallel — different repos, no overlap.

4. **First Gate 1 from jack-ryan.** Run gamora's B10.2 prompt past jack-ryan in DESIGN-MODE before kickoff. Specifically check: math-before-code requirements present? Cost projection update planned? Queued micro-fix included?

---

## Things NOT to do in the first session

- Don't have rocket start anything new — no urgent content-gen work; let B10.2 land first
- Don't touch the loadout production URL until drax confirms gear effects work
- Don't run a full season regen unless validating a B10.2 closure — smoke-only for iteration
- Don't merge from `stage-a2` to `main` without Matt approval

---

## Files knight-rider should read on Day 1 (in addition to AGENTS.md/GOVERNANCE.md/REVIEW_PROCESS.md)

1. This file
2. `~/Games/reincarnated-engine/canonical/16-project-roadmap.md` — current B-series state
3. `~/Games/reincarnated-engine/design/decisions/decisions-log.md` — last 3-5 entries
4. `~/Games/reincarnated-collaboration/canonical/28-engine-arpg-rebalance-design.md` — current rebalance design
5. `~/Games/reincarnated-collaboration/b10-2-kickoff-prompt.md` — gamora's first task

---

## Closing note

This is Day 0. The team has not yet operated. Calibration is expected over the first few sessions — especially the jack-ryan async review cadence (how often to batch?) and the per-seam tag prefix adoption. Treat the first week as a soft-launch and revise patterns as needed via ADR amendments.
