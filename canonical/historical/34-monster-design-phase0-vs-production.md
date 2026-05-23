# 34 — Monster design: Phase 0 vs production carry-forward

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Status:** Active, captured 2026-05-13
**Author:** Drafted in dialogue with Matt (Senior Architect)
**Audience:** Anyone planning B-series work, future production transition, or gauntlet-related changes
**Related:** `28-engine-arpg-rebalance-design.md` (B-series), `30-engine-explainer-current.md`, `31-engine-explainer-future.md`, `16-project-roadmap.md`

---

## Why this doc exists

During B10.1 closure (2026-05-13), a strategic question surfaced: *should the gauntlet's monster composition be tuned to address observed player-archetype gaps (e.g., hunter modifier range, fire over-representation)?*

The investigation surfaced that this question collapses if we draw a layer distinction clearly. This doc captures that distinction so future B-series work doesn't re-derive it and so the production transition has a clear hand-off list.

---

## The two layers of monster design

| Layer | What it is | Phase 0 status | Production carry-forward |
|---|---|---|---|
| **Monster GENERATION** | Tier vocabulary, stat ranges, ability composition, element/archetype distribution, pack composition rules, generation pipeline | Owned by `rocket` seam (`generation/`) | **YES — direct carry-forward.** Production game uses the same procedural monster generation. |
| **Gauntlet STRUCTURE** | The 12-monster A3 test pool, balance-loop convergence on a static gauntlet, doppelganger gate, smoke-test gauntlet composition | Owned by `gamora` seam (`simulation/`) | **NO — Phase 0 throwaway.** Production has no "test gauntlet"; monsters appear in real encounters, dungeons, zones. |

The distinction is load-bearing because it changes where each problem class belongs.

---

## What carries forward to production

### Monster generation pipeline (rocket)

- **Tier vocabulary** — `swarm / magic / trash / elite / mini-boss / boss` is a universal ARPG semantic. Ports forward unchanged.
- **Tier-band stat ranges** (HP factor, armor %, skill count, effective attribute) — calibrated values become production defaults; can be tuned per-season in production.
- **Element / archetype generation rules** — seasonal element selection, archetype diversity within tier slot, all carry forward.
- **Ability composition** — the same B6 kit builder logic (with refinements) generates monster abilities in production.
- **Pack composition rules** (B10.2 deliverable) — pack size N, homogeneity (single element / single archetype per pack), AOE differential mechanics. **This is the production carry-forward asset of B10.2.**
- **Engine's internal canonical library** (`src/reincarnated/canonical/`) — ability templates, geometry palette, role taxonomies. The reference data that production generation consumes.

### What this means for B-series investment

**Worth investing now:**
- B10.2 (pack-proxy semantics + native swarm composition)
- B11+ (geometry implementation, telegraphs, active mobility — all part of monster ability generation)
- B6 archetype template refinements (hunter range issues, etc. — player-side, but the *template logic* is generation infrastructure)
- D1 element pool quality (rocket's domain)

**Worth investing less:**
- Adaptive gauntlet composition (would drive a feedback loop that doesn't carry forward)
- Per-season gauntlet test themes (the *test* layer doesn't ship; but the *capability to theme monster composition* DOES — invest in the generation-side capability, not the test-side knob)

---

## What does NOT carry forward to production

### Gauntlet structure (gamora)

- **The 12-monster A3 gauntlet pool** — this is a *balance-validation instrument*, not gameplay content. Production replaces it with real encounters in dungeons / zones / seasonal events.
- **Balance-loop convergence on a static gauntlet** — production balance comes from real player telemetry, not simulation convergence iterations. The `balance_modifier`, `target_win_rate`, doppelganger gate, and convergence iteration logic are all Phase 0 specific.
- **Doppelganger gate** — Phase 0 archetype mirror-match defense. Production has different validation (telemetry-driven).
- **Smoke-test gauntlet** (~5 classes, 30 fights, 2-3 min) — purely a development iteration construct.

### What this means for production transition

When Phase 0 ships and production begins:

- **Keep** the entire `generation/` codebase (rocket's seam) — refined and ported, but conceptually the same system.
- **Keep** the engine's internal canonical library (`src/reincarnated/canonical/`).
- **Replace** the entire `simulation/balance_loop.py` and associated convergence infrastructure with telemetry-driven balance dashboards.
- **Replace** the gauntlet construct with production encounter design (which CONSUMES generated monsters but doesn't validate them via simulation).
- **Repurpose** the simulation engine itself — it likely becomes a *playtesting tool* in production rather than a balance-validation gate.

This split should inform any decision about how much polish to put into balance-loop code vs. generation code.

---

## Implications for player-archetype problems

The B14.5 sidecar analyses surfaced player-side issues:

1. **Hunter modifier range** (1.82, widest in dataset)
2. **Earth_controller convergence slowness** (7.0 avg iters, slowest archetype)
3. **Fire over-representation** (23.6% vs 20% expected)
4. **Mana energy homogeneity** (~85% of classes)

These are PLAYER-side problems. The gauntlet's role is to *expose* them honestly via the balance loop. The fixes belong in:

- **B6 archetype templates** (rocket) — fix hunter shape consistency, earth_controller kit structure
- **D1 element pool** (rocket) — address fire bias if selection algorithm needs balancing
- **B-series energy diversity work** (rocket) — explore rage/stamina/focus/combo archetypes

**Do NOT fix these by adjusting the gauntlet** (e.g., "give hunter more close-range monsters to fight"). That:

1. Creates a feedback loop that doesn't carry forward to production
2. Hides the player-side issue rather than surfacing it
3. Makes future analyses harder — you can't isolate template quality from monster compensation
4. Conflates two questions: "is the gauntlet representative?" and "are player classes well-shaped?"

---

## Implications for damage_scalar work

Per-skill `damage_scalar` (currently ~1.06-1.18 across skill ranks) is a player-generation parameter. It controls vertical rank progression — higher scalar = more endgame power scaling.

**Where the fix lives:** player generation logic (rocket), specifically skill generation in `generation/skill_*`.

**Gauntlet's role:** expose whether scalars are too high (player wins at endgame ranks too easily) or too low (player can't reach target win rate). This is the gauntlet doing its job; don't compensate via monster tuning.

---

## Architecture decision (locked)

**Phase 0 gauntlet = Architecture A: fair test environment.**

- Monsters generated independently of player problems
- Balance loop adapts player power (via `balance_modifier`) to monster difficulty
- Player-archetype issues fixed in player-side generation, not via monster composition tuning
- Convergence iterations are how the system reaches target win rates honestly

This architecture is correct *because the gauntlet is a test harness, not a gameplay surface*. The "fairness" comes from the gauntlet *not* having an opinion about which player archetypes should win or lose — it just tests them.

---

## Test-side parameters (limited investment)

There are legitimate Phase 0 reasons to vary gauntlet composition:

- Smoke-test vs full-regen gauntlet sizes (compute budget)
- Specific class diagnostics (e.g., when investigating hunter range, manually constructing a close-range gauntlet for that diagnostic)

These are **manual analyst tools** (jack-ryan / gamora using them during investigation), not automated balance-loop coupling. They don't need infrastructure investment.

---

## Production transition checklist (for future)

When Phase 0 ships and production work begins, this is the carry-forward / replacement list:

**Carry forward (refine in place):**
- [ ] `reincarnated-engine/src/reincarnated/generation/` — entire seam
- [ ] `reincarnated-engine/src/reincarnated/element/`
- [ ] `reincarnated-engine/src/reincarnated/anchor/`
- [ ] `reincarnated-engine/src/reincarnated/foundation/`
- [ ] `reincarnated-engine/src/reincarnated/canonical/` (engine's internal library)
- [ ] `reincarnated-engine/data/seasonal_elements/`
- [ ] B-series refinements (B6, B10.2, B11, B15, B16) — each commits an asset to production

**Replace (Phase 0 throwaway):**
- [ ] `reincarnated-engine/src/reincarnated/simulation/balance_loop.py`
- [ ] `reincarnated-engine/src/reincarnated/simulation/build_reference_gauntlet`
- [ ] Doppelganger gate logic
- [ ] Convergence iteration infrastructure
- [ ] Smoke-test gauntlet construct

**Repurpose:**
- [ ] Fight engine itself — likely becomes a *playtesting / encounter-tuning tool* in production rather than a balance gate
- [ ] Telemetry infrastructure — production needs richer telemetry (real player data) but the architecture is similar

---

## References

- `28-engine-arpg-rebalance-design.md` — current B-series state (especially B10, B14 sections)
- `30-engine-explainer-current.md` — what the engine currently produces
- `31-engine-explainer-future.md` — production design intent
- `16-project-roadmap.md` — B-series sequencing
- `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_b14_5_sidecar_analyses.md` — the 5 empirical analyses that surfaced this question
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` — pending entry: "Gauntlet is test harness, not gameplay surface (2026-05-13)"
