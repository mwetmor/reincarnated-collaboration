# Dispatch — 2026-05-21 — gamora — W0.9: Gauntlet architecture migration (retire PackProxy ×8; true multi-monster positional gauntlet default)

**From:** knight-rider
**To:** gamora (simulation seam)
**Approved by:** **Matt 2026-05-21 "Confirm § 2.9 edit"** (gandalf attestation 2026-05-21); structural architectural commitment per activation dispatch § 2.9 + § 5
**Status:** PENDING — ACTIVE (gamora may execute when launched)
**Estimated effort:** ~1-2 weeks (substantial; 6 sub-tasks per activation dispatch § 2.9)
**Acceptance:** PackProxy ×8 retired from swarm-tier convergence; R2 spatial sub-gauntlet promoted to default for all 5 tiers; smoke-test mode + parallel batches + cell-targeted convergence performance optimization; telemetry instrumentation; calibration sweep validates sensible per-tier WR distributions; tag `qd-rebuild/v0.9-gauntlet-migration-complete`.

---

## Context — why this dispatch exists

Per activation dispatch § 2.9 + Matt 2026-05-21 ratification: the QD-engine architecture commits to **ONE gauntlet implementation (true multi-monster positional swarms) and ONE execution path (convergence during archive population)**. PackProxy ×8 swarm-tier abstraction RETIRED. P7 W7.2 reference-archetype certification becomes an archive QUERY (not gauntlet re-execution).

**The "fix the arena, not the synergy" anchor** (recompose-hive governance principle 2026-05-20): PackProxy ×8 abstracted 8-monster swarms as one big entity with N×HP and ×N AOE damage. This is the WRONG ARENA for kits that will face true 8-monster spatial gameplay in actual Reincarnated demo + game. True multi-monster positional gauntlet IS the same arena the player faces.

**Empirical reinforcement from Track C synthesis (2026-05-21 § 2.3):** 100% Pattern-A under same-calibration across all substrates may be partly a function of PackProxy abstraction stripping out mobility/positioning/kiting strategies that kits would otherwise exercise. The migration is more than just "fix the arena" — it's a candidate empirical fix to the boss-floor problem.

## Sub-tasks (per activation dispatch § 2.9)

### W0.9.1 — Retire PackProxy ×8 from swarm-tier convergence path

Route swarm-tier convergence through true multi-monster spatial sim (extend existing R2 spatial sub-gauntlet). Specifics:
- Inspect `simulation/combatant.py` PackProxy class — identify all call sites and consumers
- Inspect `simulation/balance_loop.py` swarm-tier handling — does it route via PackProxy or directly?
- Migrate swarm-tier to use the same multi-monster spatial sim path used for R2 spatial sub-tests
- Preserve PackProxy class as DEPRECATED but in-tree (don't delete; ADR-004 cross-seam awareness) OR remove if no consumers remain — your call after the inspection; document choice in MIGRATION.md

### W0.9.2 — Promote R2 spatial sub-gauntlet to default convergence path for all 5 tiers

Currently R2 spatial sub-gauntlet is used for specific spatial sub-tests. Migrate so it's the DEFAULT convergence path for swarm + magic + elite + mini-boss + boss tiers. Each tier's "room" (R2 large/small room structure per existing R2 spatial design) becomes the convergence-time test arena.

### W0.9.3 — Implement gauntlet usage modes (convergence vs validation)

ONE gauntlet sim code; different input/output pipelines per usage mode:
- **Convergence usage mode**: input = candidate kit + BC-target; output = converged_modifier + per-tier WR + telemetry → archive insertion
- **Validation usage mode**: input = archive entry (kit + BC coordinate); output = behavioral verification result (per-tier WR within contract; spatial AI behavior sensible)
- Same simulation code under both modes; differ only in input fixture + output consumer

### W0.9.4 — Performance optimization

True multi-monster spatial sim is slower than PackProxy ×8 abstraction. Bake in these mitigations per Discipline #2 (smoke-test discipline):
- **Smoke-test mode**: fast initial evaluation per kit (reduced fight count + simplified spatial AI); full-fidelity escalation only for kits that pass smoke
- **Parallel batches**: archive filling parallelizes across many kits simultaneously (where possible without telemetry collision)
- **Cell-targeted convergence**: don't exhaustively converge all kits; target cells per Phase 1 archive-state inspection priority (per workflow doc Phase 1)
- **Optional: reduced-tick-rate evaluation** for early convergence iterations; full-tick-rate only for final convergence verification

**Net performance target:** archive filling may be 2-5× slower than PackProxy-based filling, but each archive entry is empirically valid against actual gameplay reality.

### W0.9.5 — Telemetry instrumentation for true multi-monster sim

Extend telemetry to capture:
- Per-entity damage logs (per-monster-instance damage taken; not just per-pack aggregate)
- Spatial positioning data (player position over time; per-monster positions; per-cast targeting)
- AI behavior traces (target selection, attack execution, lifecycle events)
- Per-event source-tagged damage attribution (cast / reactive / proxy / environmental) — feeds P2 BC measurement work

Schema version bump expected: v2.13 → v2.14 (new fields). Coordinate with star-lord at the boundary (MIGRATION.md cross-seam clause).

### W0.9.6 — Calibration sweep (Discipline #17)

Verify true multi-monster gauntlet produces sensible per-tier WR distributions:
- Run convergence on 5-10 representative kits across the substrate spectrum (per Track C: uniform across all 7 substrates)
- Compare per-tier WR distribution to PackProxy ×8 baseline (telemetry from recompose-hive's season_100005 + Track C TC-1 + TC-2)
- Validate per-tier WR contract bounds (swarm 0.65-0.80; magic 0.55-0.70; elite 0.45-0.60; mini-boss 0.35-0.55; boss 0.30-0.45) are reachable under the new gauntlet
- Document calibration values; flag thresholds needing adjustment

**Discipline #17 (empirical-calibration smoke gate) anchor:** if the calibration sweep shows substantial per-tier WR shift beyond expected (e.g., boss WR collapses to 0 universally, OR boss WR universally satisfies the contract for the first time), surface to knight-rider + gandalf. The shift IS the empirical signal of whether the gauntlet migration alone resolves boss-floor (Track C OQ that's now testable).

## Required reading before starting

- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` § 2.9 (full architectural rationale + sub-task breakdown)
- `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md` § 2.3 (gauntlet migration as candidate empirical fix to boss-floor)
- `canonical/story/per-tier-recompose-validation-findings-2026-05-19.md` (recompose-hive findings; "fix the arena, not the synergy" governance principle § 11.5)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3 (per-axis spatial-AI implications; multi-monster sim deferrals)
- Existing R2 spatial sub-gauntlet code paths (find via grep; inspect)
- `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` (your prior records)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (especially #1 math-before-code, #2 smoke-test, #11.1 state-space conditioning, #17 empirical calibration, R11(b) cross-seam round-trip)

## Math-before-code (Discipline #1; REQUIRED for this dispatch)

Before W0.9.1 implementation, author a math note at `reincarnated-engine/src/reincarnated/simulation/math/gauntlet-migration-arena-equivalence.md`. Cover:

1. **Per-tier WR expectation under PackProxy ×8 vs true multi-monster**: predict the expected per-tier WR shift (magnitude + direction + edge cases) when migrating
2. **AOE damage formula equivalence**: PackProxy applies ×N AOE damage to single entity with N×HP. True multi-monster applies AOE to N separate entities each at HP. Verify damage-conservation across the migration (caveat: spatial AOE may NOT hit all N entities depending on positioning — this is the load-bearing semantic difference)
3. **Performance estimate**: predict the wall-clock per-kit convergence under W0.9.4 mitigations
4. **Convergence-iteration impact**: predict whether convergence iterations per kit increase (more spatial variables) or stay roughly constant
5. **Calibration sweep prediction**: what should per-tier WR distributions look like under the new gauntlet for canonical archetypes (e.g., D2 Hammerdin / D3 DH / PoE Cyclone Slayer-equivalents per the 12-archetype reference roster)

Per Discipline #1: predict THEN implement THEN verify. If measured ≠ predicted, re-diagnose mechanism BEFORE adjusting parameters.

## Cross-seam contract change? (Principle 6 gate)

**YES** — W0.9.5 telemetry instrumentation adds fields. Round-trip required per ADR-004 + REVIEW_PROCESS.md Principle 6.

**Round-trip smoke: per W0.9.5 — schema v2.13 → v2.14 with new fields (per-entity damage logs; spatial positioning data; AI behavior traces; per-event source-tagged damage attribution). Production-path fixture: convergence run of 1 canonical kit (e.g., a current shadow_mage kit from season_100005) through new gauntlet. Consumer boundary exercised: star-lord telemetry consumer reads new fields without error. Field-presence check: all new schema v2.14 fields populate in `class_balance_results.json` for the test kit.**

MIGRATION.md entry required per ADR-004. Coordinate with star-lord at the schema boundary (R11(b) discipline).

## Scope

- [ ] Math note authored BEFORE implementation (Discipline #1)
- [ ] W0.9.1 PackProxy ×8 retired from swarm-tier convergence
- [ ] W0.9.2 R2 spatial sub-gauntlet promoted to default for all 5 tiers
- [ ] W0.9.3 Convergence vs validation usage modes implemented (one sim code; different pipelines)
- [ ] W0.9.4 Performance mitigations implemented (smoke-test mode + parallel batches + cell-targeted convergence)
- [ ] W0.9.5 Telemetry instrumentation extended (schema v2.14; coordinate with star-lord)
- [ ] W0.9.6 Calibration sweep documented + per-tier WR distributions validated
- [ ] MIGRATION.md entry per ADR-004
- [ ] Round-trip smoke per Principle 6
- [ ] AGENT_STATE.md updated
- [ ] Tag: `qd-rebuild/v0.9-gauntlet-migration-complete`

## Acceptance criteria

- [ ] All 6 sub-tasks (W0.9.1-W0.9.6) complete
- [ ] Math note predictions vs measurements: documented (Discipline #1)
- [ ] No regressions in existing sim behavior (run prior smoke seasons; verify cell convergence behavior preserved for archive-comparable kits)
- [ ] Performance target met: archive filling ≤ 5× slower than PackProxy baseline (per W0.9.4 target)
- [ ] Round-trip smoke: schema v2.14 fields populate end-to-end (gamora sim → star-lord telemetry consumer); fixture documented
- [ ] Calibration sweep findings documented; Discipline #17 followed
- [ ] If calibration sweep shows substantial boss-tier WR shift (Track C testable surface): surface to knight-rider + gandalf (per critique-pair pattern for W0.9: gandalf reviews architectural alignment; jack-ryan reviews migration correctness + Discipline #13a drift)

## Out of scope

- Joint-gate (Discipline #18) implementation — that's P5 W5.6
- Cohesion-BC or visual-BC integration with new gauntlet — P5
- Profile A/B/C/D filtering — P6
- Reference-archetype certification (P7 W7.2 archive QUERY; not this dispatch's re-execution)
- Reducing W0.9 scope to only swarm-tier (the architectural commitment is single-implementation across all 5 tiers; partial migration retains the "wrong arena" problem)
- Implementing W1.13 skill tree node population (P1 timeframe; W0.9 is gauntlet-side; W1.13 is generation-side)

## Open questions for the agent to resolve

- **PackProxy preservation choice (W0.9.1)**: keep as DEPRECATED in-tree, or remove? Document choice with reasoning in MIGRATION.md.
- **Reduced-tick-rate evaluation (W0.9.4 optional)**: implement now, or stage for follow-on optimization? Recommendation: implement IF math-note predicts substantial perf gap; defer if W0.9.4 baseline already meets ≤5× target.
- **AI behavior traces (W0.9.5)**: granularity choice — every AI decision event, or sampled? Document with reasoning; star-lord boundary requires structured output.
- **Per-monster-instance HP tracking (W0.9.5)**: telemetry-side capacity — verify telemetry DB can hold the new volume; coordinate with star-lord MIGRATION.md.
- **Calibration sweep substrate selection (W0.9.6)**: per Track C uniform-depth, sample from all 7 elements; recommend ~1 kit per substrate (7 total) + ~3 archetype variants for spread; document selection rationale.

## Critique-pair structure

- **gandalf** reviews architectural alignment ("fix the arena" principle preservation; one-implementation-two-usages framing; Track C empirical-validation alignment)
- **jack-ryan** reviews migration correctness (PackProxy retirement complete; no legacy paths remain; Discipline #13a drift check; R11(b) round-trip)
- **knight-rider** folds verdict into state-of-hive doc + P1 readiness assessment

## References

- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` § 2.9 (full architectural commitment + sub-task spec)
- `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md` § 2.3 (gauntlet migration as candidate boss-floor fix)
- `canonical/story/per-tier-recompose-validation-findings-2026-05-19.md` § 11.5 ("fix the arena, not the synergy" governance principle)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3.3 (Axis 2A proxy density implications for multi-monster sim)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` Phase 3 (convergence + measurement; consumer of new gauntlet)
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-21 QD-rebuild activation entry (W0.9 commitment)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (especially #1, #2, #11.1, #17, R11(b), Pattern P7)

---

## Completion record

**Phase 1 (math-before-code): COMPLETE — 2026-05-21**
**Phase 2 (implementation W0.9.1–W0.9.6): PENDING jack-ryan Gate-1 review**

### Step 0 deliverables

- [x] Math note authored: `reincarnated-engine/src/reincarnated/simulation/math/gauntlet-migration-arena-equivalence.md`
- [x] PackProxy call sites inventoried (10 live sites in balance_loop.py; 2 in damage_resolver.py; 2 in combatant.py; 3 test files)
- [x] R2 spatial sub-gauntlet locations documented (spatial_gauntlet/ module; 7 script callers; ZERO balance_loop integration; SCAFFOLDING status confirmed)
- [x] AGENT_STATE.md updated: "W0.9 Step 0 math-before-code complete; awaiting jack-ryan Gate-1 routing before Phase 2 implementation"
- [x] Dispatch partial-completion record appended (this record)

### Key findings from Step 0

**PackProxy call sites (live, non-comment):** 10 distinct sites in balance_loop.py + 2 in damage_resolver.py + 3 test files requiring migration attention.

**R2 spatial sub-gauntlet current state:** Fully decoupled from convergence path (scripts-only callers). SCAFFOLDING status per spatial_engine.py docstring. Three existing scenarios: open_arena (8 swarm), chokepoint (8 swarm), boss_with_adds (1 boss + 2 elite). Magic and elite tier spatial scenarios are NOT yet defined — gap for W0.9.2.

**Math note key predictions:**
1. Per-tier WR: Swarm drops from ~1.000 to 0.70–0.85 (AOE classes) under spatial; boss WR partially emerges from 0.000 — high-modifier classes (≥0.30) predicted 0.30–0.55; low-modifier mages predicted 0.05–0.20.
2. AOE damage: NOT conserved — spatial k_bar≈3–4 vs PackProxy automatic 8×; single-target conserved (1:1). Load-bearing semantic shift confirmed as intentional.
3. Performance: ≤5× target requires reduced-tick-rate evaluation (W0.9.4 optional → REQUIRED per math note). Baseline mitigations + parallel batches reach ~3–10×; adding reduced-tick brings to <2×.
4. Convergence iterations: +1–4 additional iterations vs 1D; mage/controller overhead increases from 5–9 to 6–12. Recommend MAX_ITERATIONS=15 for spatial path.
5. Joint-resolution call: Spatial migration PARTIALLY resolves Pattern-A. Full resolution for mage archetypes requires joint resolution with B14.5 V2 tier-weighted lever (W0.1).

**Architectural concerns for Gate-1 review:**
- SPATIAL_DAMAGE_SCALE=4.0 needs re-calibration for convergence use (currently calibrated for sub-gauntlet smoke only)
- Magic and elite spatial scenario definitions are a Phase 2 design gap (W0.9.2)
- Swarm convergence weight: recommend 0.0→1.0 (Discipline #12 semantic shift requiring explicit framing)
- `MAX_ITERATIONS` increase to 15 for spatial path

### Routing

- **jack-ryan:** Gate-1 review of math note for migration correctness + Discipline #13a drift check
- **gandalf:** Architectural alignment review ("fix the arena" principle + one-implementation-two-usages framing + Track C empirical-validation alignment)
- **knight-rider:** Fold verdict into state-of-hive + P1 readiness assessment; decide W0.9.4 reduced-tick-rate call before gamora begins Phase 2

### Tags

- `qd-rebuild/v0.9-gauntlet-migration-complete` — NOT YET (fires after full implementation + calibration sweep)

---

**Phase 1.5 (amendment fold-in): COMPLETE — 2026-05-20**

### Phase 1.5 deliverables

All 7 Gate-1 amendments folded into math note `simulation/math/gauntlet-migration-arena-equivalence.md`:

- [x] **A1 (REQUIRED — jack-ryan):** §6.6 added — LC-003 cross-seam schema gap acknowledged; 3 floor-lock fields (`floor_lock_recompose`, `working_modifier`, `floor_lock_detected`) confirmed in v2.14 scope; round-trip smoke fixture spec written
- [x] **A2+A6 combined (WARN + Architectural):** §6.1 updated — `SPATIAL_DAMAGE_SCALE` reframed as Discipline #17 empirical-calibration parameter (not design constant); re-calibration trigger condition added ("required if physical_warrior boss WR < 0.30 in W0.9.6 sweep")
- [x] **A3 (WARN — jack-ryan):** §3.4 updated — tick-rate stability verification criterion added (±0.05 WR delta threshold; disqualification logic per tier)
- [x] **A4 (Architectural — gandalf):** §6.4 updated — P7 W7.2 archive-query clarification added; architectural violation clause for certification re-execution
- [x] **A5 (Architectural — gandalf, most consequential):** §6.7 added — W0.9.5 telemetry plan for all 8 BC axes; per-fight event spec for Axes 2, 2A, 2B, 3A, 3B, 4, 5; Axis 1 derivable from Axis 2 geometry tags; BLOCKING gap framing
- [x] **A7 (Architectural — gandalf):** §5.4 updated — swarm weight 0.0→1.0 framed as architectural shift (arena change), not tuning preference; commit message + decisions-log requirement stated
- [x] **A8 (Architectural — gandalf):** §6.3 updated — hard gate for magic/elite/mini-boss scenario definitions; gandalf delegation requirement stated; fallback scope (swarm+boss only) if delegation not confirmed at Phase 2 kickoff
- [x] Math note status header updated to Phase 1 + Phase 1.5 complete
- [x] AGENT_STATE.md updated: "W0.9 Phase 1 + Phase 1.5 (amendment fold-in) complete; awaiting Phase 2 implementation kickoff"
- [x] Intermediate tag fired: `qd-rebuild/v0.9-math-note-phase-1-complete`

**Phase 2 (implementation W0.9.1–W0.9.6): PENDING — awaiting Phase 2 implementation kickoff**
