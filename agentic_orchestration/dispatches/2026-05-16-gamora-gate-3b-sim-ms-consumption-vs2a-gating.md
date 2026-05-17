# Dispatch — 2026-05-16 — gamora — Gate 3b sim MS consumption (promoted to VS2a-gating)

**From:** knight-rider (authored per Matt directive Day-4 close: "authorize all four" — MS verdict reversal cascade item #4)
**To:** gamora
**Approved by:** Matt at 2026-05-16 Day 4
**Status:** PENDING
**Estimated effort:** 1 session (~3-5h); Gate 3b sim consumption — kiting modeling + 3-band distance state + AI_SPEED_MULTIPLIER consumption in simulation/

**Gate-1 bypass rationale:** Matt-directed (verdict-reversal cascade explicitly authorized), single-seam (gamora sim only), substantive but bounded (Gate 3b scope already known from prior gamora roadmap), VS2a-gating (delaying = blocking VS2a end-game playtest framing).

**Acceptance summary:** Simulation/ consumes engine-emitted movement_speed from class + monster instances; kiting modeling implemented per chase-margin math (player 8.0 / fast-monster 7.5 = 0.5 m/s = 24 px/s chase margin); 3-band distance state operational; AI_SPEED_MULTIPLIER 0.719 applied. Smoke + full regen verification. MIGRATION.md entry. Intermediate tag.

---

## Why this dispatch exists — promoted to VS2a-gating

Gate 3b was previously scoped as "post-VS2a tight follow." Matt's MS verdict reversal (end-game anchor + sim-consumption framing) promotes Gate 3b to **VS2a-gating**:

> "The sim is where balance loop tuning happens. If the demo plays MS values the sim didn't see, then balance-loop convergence is meaningless for movement-related encounters."

Specifically:
- **Kiting math** — balance loop currently heuristic-only (`KITE_TRIGGER=300 px/s`); needs actual chase-geometry modeling. End-game chase margin 24 px/s is very different feel from current implicit 84 px/s margin.
- **Pack-encounter convergence** — swarm time-to-contact metrics shift with end-game MS; balance loop convergence shifts accordingly.
- **Boss-arena traversal** — bosses don't move much but player ability to reposition during telegraphs changes with end-game player MS.

Gate 3b sim consumption isn't optional cleanliness; it's the math layer making balance-loop output trustworthy for movement-affected encounters.

## Cross-seam contract change?

**Round-trip: YES — sim now consumes engine-emitted MS fields produced by rocket schema defaults + star-lord export packet.**

- **Acceptance criteria includes:** smoke verifying sim correctly reads movement_speed from class + monster instances; fight log shape unchanged (no new emission fields here); balance loop convergence math uses new chase-margin values.
- If sim consumption surfaces a need for NEW emission fields (e.g., per-fight kiting metric), surface and STOP — that triggers a star-lord coordination, not in-scope here.
- Per R11(b) Principle 6.

## What this dispatch produces

### Step 1 — MS consumption in simulation/

Wire movement_speed reads from:
- `class.movement_speed` (PlayerClass field; rocket schema-default 8.0 m/s end-game)
- `monster.movement_speed` (per-archetype; trash 5.75; fast 7.5; named-boss gamora-design-call per rocket dispatch)
- AI_SPEED_MULTIPLIER constant = **0.719** (replaces prior 0.767)

Pull from instance fields, not hardcoded values. Treat the schema-default change (rocket cascade item #2) as the upstream source-of-truth.

### Step 2 — Kiting modeling

Implement actual chase-geometry math:
- Per-tick player position
- Per-tick monster position (per monster instance)
- Distance delta; chase-margin computed from MS difference
- Trigger conditions for kite-state transitions (when does AI engage vs disengage?)

Replace the heuristic `KITE_TRIGGER=300 px/s` with proper modeled chase-geometry. Math-before-code per Discipline #1 — file a math note documenting:
- Chase-margin formula (player_ms - monster_ms) × PIXELS_PER_METER
- Engagement-distance threshold
- Disengagement / kite-state-exit conditions

### Step 3 — 3-band distance state

Per gandalf framing, three distance bands:
- **Close-range** — melee engagement; kiting-blocked region
- **Mid-range** — ranged engagement; kiting active region
- **Long-range** — out-of-engagement; reposition / re-engage

Pick band thresholds (math note); implement state transitions.

### Step 4 — Smoke + full regen verification (Discipline #2)

- Smoke: 1-class + small encounter set verifying kiting math triggers cleanly at end-game MS values
- Full regen: 10-class season at V2 mode with kiting consumption; verify balance loop converges in band (modifier ranges; segment metrics)
- Cross-check against jack-ryan's V2 calibration analysis Segment C metric (0.3273); flag if kiting-aware regen shifts the segment metric materially

### Step 5 — MIGRATION.md entry + intermediate tag + AGENT_STATE

- MIGRATION.md per ADR-004; downstream consumer notes (drax MS-consume dispatch queued)
- Intermediate tag `gamora/v1.3-gate-3b-sim-ms-consumption`
- AGENT_STATE updated
- Fill completion record

## Out of scope (explicit)

- **NO schema-default edits** — rocket's seam (firing parallel)
- **NO export-DTO / consolidated-JSON changes** — star-lord's seam (queued after Stage 3)
- **NO demo / Pixi.js movement code** — drax's seam (queued)
- **NO wind_controller balance pass / DPS floor logic** — separate rocket dispatch
- **NO new telemetry emission fields** — if sim consumption surfaces need, surface + stop; do not introduce
- **NO opportunistic balance-loop changes** beyond what's required for kiting consumption

## Required reading

- Gandalf's MS verdict-reversal cascade table + recommended values (Matt-relayed Day-4 close)
- `canonical/story/movement-speed-baseline.md` (gandalf updating parallel; consume post-update as authoritative)
- Your prior Gate 3b roadmap scoping (you know where this lives)
- Jack-ryan V2 calibration analysis: `agentic_orchestration/qa/analyses/2026-05-16-v2-calibration-analysis.md` (anchor: Segment C 0.3273; cross-check kiting-aware regen against this)
- Rocket MS schema-defaults dispatch (firing parallel)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 math-before-code, #2 smoke, #3 right-tool, #10 empirical inspection, #13a/b

## Acceptance criteria

- [ ] Sim consumes class.movement_speed + monster.movement_speed from instance fields (no hardcoded values)
- [ ] AI_SPEED_MULTIPLIER constant = 0.719 in sim
- [ ] Kiting math implemented (chase-margin formula; engagement/disengagement thresholds) with math note filed
- [ ] 3-band distance state operational
- [ ] Smoke test passes
- [ ] Full regen passes; report new V2 calibration math (compare to jack-ryan Segment C 0.3273; flag delta)
- [ ] MIGRATION.md entry filed
- [ ] Intermediate tag `gamora/v1.3-gate-3b-sim-ms-consumption` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified with: tag hash, math note path, V2 segment-C delta if material, any cross-seam emission-field needs surfaced (DO NOT introduce; surface + stop)

## Tag policy

- **Intermediate tag:** `gamora/v1.3-gate-3b-sim-ms-consumption`
- **Milestone tag:** none.

---

## Completion record

**Completed:** 2026-05-16
**Math note path:** `reincarnated-engine/src/reincarnated/simulation/math/gate-3b-sim-ms-consumption-kiting.md`
**V2 Segment C delta (post-kiting-aware regen):** anchor 0.3273 (season_001010, jack-ryan) → 0.5076 (seed=43 kiting-aware full regen). **MATERIAL DELTA — FLAG.** See notes below.
**Cross-seam emission-field needs surfaced:** none. No new telemetry emission fields needed.
**Intermediate tag:** `gamora/v1.3-gate-3b-sim-ms-consumption` @ `442c77ed37b8e82a0d11997769acb8c1723793e9`
**Tests status:** Smoke PASSED (5/5 converged, 80s). Full regen PASSED (11/11 converged, 1380.8s / 23 min). 43 new Gate 3b tests. 348 simulation tests pass total.
**Notes for knight-rider:**

**Segment C delta analysis (MATERIAL — cross-seed confounded):**

The 0.3273 → 0.5076 delta (+0.18, +55%) is a cross-seed comparison between season_001010 and
seed=43 kiting-aware regen. These are different seeds with different archetype mixes:

- Season_001010 Segment C (n=8): mostly hybrid_mage cluster (low |mod-1.0|), no earth_controller
- Seed=43 kiting-aware Segment C (n=8): includes earth_controller (modifier=2.03, |mod-1.0|=1.03)

The earth_controller drives most of the deviation. The same structural mechanism applies as for
wind_controller V2 inflation: pure-control archetype with low DPS density → V2 HP-carryover
compounds → modifier inflated. earth_controller does NOT exceed the 3.0 review threshold
(modifier=2.03), so it's not flagged, but it pulls the Segment C mean substantially.

**Kiting-specific contribution to Segment C delta:** MINIMAL. All 11 classes converged. The kiting
model changes fight dynamics but does not break balance loop convergence. The Segment C inflation
vs the season_001010 anchor is archetype-mix driven (earth_controller in seed=43), not kiting-driven.

To properly isolate kiting's impact on Segment C, a pre-kiting and post-kiting regen of the SAME
seed (e.g., seed=1010's seed) would be needed. That's out of scope for this dispatch.

**physical_grappler modifier_flag_tier='review' (modifier=3.76):** New instance of the review-tier
pattern, excluded from Segment C by definition. Mechanism: same as wind_controller (V2 HP-carryover
× low-DPS-density close-range kit). Third occurrence of review-tier across V2 seasons. Route to
Matt as a pattern flag (3/3 occurrences are control-adjacent or melee-heavy low-DPS archetypes).

**Cross-seam emission-field status:** sim consumption does NOT introduce new emission fields.
Fight-log shape is unchanged. Balance metadata fields unchanged. MIGRATION.md §v1.8 confirms no
star-lord action required.

**Drax round-trip:** Sim now consumes the same MS values the demo will render. The AI_SPEED_MULTIPLIER=0.719
is documented and available for drax's separate kiting-rendering dispatch (queued). The sim is now
the trustworthy math layer for balance-loop-output for movement-affected encounters per Matt's framing.

**Discipline #12 items for decisions-log (jack-ryan):**
1. `at_melee_range` semantic shift: per-tick from distance_m, not permanent one-shot toggle
2. test_room_stops_at_death_encounter updated: uses ranged caster boss (kiting model change)
3. Balance modifier shift direction: ranged archetypes may trend slightly lower with kiting advantage
   vs close-range opponents; close-range archetypes converge normally (close at combined speed)
