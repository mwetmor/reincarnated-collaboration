# Dispatch — 2026-05-21 — gamora — W0.1: B14.5 V2 energy-type lever in primary recompose loop (LC-004 calibration-side fix)

**From:** knight-rider
**To:** gamora (simulation seam)
**Approved by:** **gandalf endorsement 2026-05-21 § 4** (operational sequencing within knight-rider's autonomy per protocol § 7.1; gandalf explicitly endorses B14.5 V2 follow-on interpretation of W0.1); per activation dispatch § 4 Step 4 W0.1
**Status:** PENDING — ACTIVE (gamora may execute when launched)
**Estimated effort:** ~1-2 weeks (substantial; calibration-side complement to W0.2 architectural fix)
**Acceptance:** Energy-type lever implemented in primary recompose loop (`balance_loop.py`); calibration sweep verifies modifier compression toward `mean |mod - 1.0| ≈ 0.50` (down from current ~0.82 epoch); tag `qd-rebuild/v0.1-b14-5-v2-energy-type-lever`.

---

## Context — the LC-004 architecture

LC-004 (jack-ryan legacy constraint audit) names the energy-type mechanical gradient: rage/physical classes face structural ~3-5× DPS-per-modifier disadvantage vs elemental/mana classes. Per the 2026-05-16 decisions-log entry, the architectural fix has **two parts**:

1. **B6 pre-work (rocket generation; SHIPPED 2026-05-16 at `rocket/v1.3-b6-energy-type-tiers`)** — energy-type-aware tier-range assignment in `b6_archetype_templates.py`. Tier-addressable portion. Closes the magnitude-per-hit lever (~1.7× partial correction).
2. **B14.5 V2 (gamora simulation; THIS DISPATCH)** — energy-type lever in primary recompose loop. Closes the non-tier-addressable portion (rage startup; miss rate; physical positioning). Targets full mean |mod - 1.0| ≈ 0.50 epoch.

**Per Track C synthesis (2026-05-21 § 1.2)**: modifier ranges differentiate by substrate cluster:
- Lightning / fire: 0.072–0.103 (lean kits)
- Water: 0.134–0.258 (sustained-presence)
- Wind / earth / holy: 0.134–0.505 (control/support)
- Physical: 0.134–1.000 (armor mitigation + melee geometry)

The physical 0.134-1.000 spread is the structural target of this work. **Per OQ-6** (Track C synthesis § 3): class_0019 hit modifier=1.0 ceiling and still produced boss_wr=0.0 — physical hunter archetype may be systemically mis-matched. Energy-type lever needs to either close the gap OR surface that the gap is irreducible at the simulation layer (which then routes to W0.2 architectural fix + W0.9 gauntlet migration as the joint resolution).

## What this dispatch does

### Step 0 — Math-before-code (Discipline #1; REQUIRED)

Author a math note at `reincarnated-engine/src/reincarnated/simulation/math/w0-1-b14-5-v2-energy-type-lever.md`. Cover:

1. **The LC-004 disadvantage decomposition** (re-derive from gamora's prior `simulation/math/modifier-range-root-cause.md` §4.3): rage startup (~1.5-2.0×); physical miss rate (~1.18×); armor mitigation (~1.23×); melee positioning (~1.1×); combined ~2.4-3.3× before tier shift
2. **B6 pre-work residual**: B6 closed ~1.7× tier-addressable; remaining ~1.4-1.9× lives at simulation layer (this dispatch's target)
3. **The lever design**: energy-type-aware adjustment in primary recompose loop. Specifically — what does the lever modify? Options to consider:
   - Rage startup energy (e.g., grant 15-20 starting rage to physical classes; per gamora's prior investigation, this compresses modifiers by ~20%)
   - Effective per-hit damage adjustment for physical (account for miss-rate during convergence rather than equilibrating around miss-affected DPS)
   - Armor mitigation adjustment (energy-type-aware ARMOR_MITIGATION_K)
   - Combined approach (likely)
4. **Predicted modifier compression**: per chosen lever, predict mean |mod - 1.0| shift from current ~0.82 epoch toward 0.50 target
5. **OQ-6 integration**: predict whether the lever closes physical hunter's modifier=1.0 ceiling pathology, OR whether OQ-6 needs architectural intervention beyond simulation (W0.2 + W0.9 territory)

Per Discipline #1: predict THEN implement THEN verify. Per the prior recompose-hive precedent, math notes guide implementation; "tune until pass" anti-pattern is explicitly forbidden.

### Step 1 — Lever implementation

Target: `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` primary recompose loop (or `_primary_recompose_loop` or whatever the convergence-time lever-evaluation function is named in current state).

Add: energy-type lever per math note Step 0. Use named constants per Discipline #18 (Discipline #18 here refers to the existing named-constants discipline, not the candidate Discipline #18 joint-gate). Document the constant block with rationale + reversibility + cross-refs (per `LEVER_FLOOR_LOCK_WORKING_MODIFIER` docstring precedent).

### Step 2 — Unit tests + smoke

Per the recompose-hive P1 unit-test pattern (`tests/test_balance_loop.py`):
- Add unit tests that confirm the energy-type lever fires correctly under controlled mock conditions
- Confirm telemetry round-trip (per recompose-hive R11(b) discipline)
- Smoke gate per Discipline #2: 5-class smoke season under cold-start canonical convergence (Discipline #11.1: cold-start equilibrium-state signals only)
- Full test suite: 179/179 PASS preserved

### Step 3 — Calibration sweep (Discipline #17)

Per recompose-hive's `season_100005` empirical baseline:
- Run cold-start convergence on a multi-substrate season under new energy-type lever
- Measure mean |mod - 1.0| epoch — predict vs measure per math note
- Validate against per-tier WR contract bounds (swarm 0.65-0.80 / magic 0.55-0.70 / elite 0.45-0.60 / mini-boss 0.35-0.55 / boss 0.30-0.45)
- Document calibration values + flag any threshold needing >30% adjustment (per Discipline #17 calibration-sweep-anomaly threshold)

### Step 4 — Coordinate with W0.9 (gauntlet architecture migration)

W0.9 + W0.1 are both gamora-owned simulation-side workstreams. Coordinate:
- W0.9 retires PackProxy ×8 + introduces true multi-monster gauntlet
- W0.1 adjusts the convergence lever space within whatever gauntlet is active
- The calibration sweep in Step 3 should ideally run on the NEW gauntlet (post-W0.9) for empirical alignment with QD-archive convergence reality

**Sequencing recommendation:** if W0.9 fires first (or in parallel and ships first), W0.1 calibration sweep uses new gauntlet. If W0.1 fires first, document the calibration sweep results under OLD gauntlet (PackProxy ×8 baseline) + flag to re-run under new gauntlet post-W0.9.

Coordinate with knight-rider on sequencing.

### Step 5 — MIGRATION.md (if cross-seam)

Energy-type lever in convergence likely affects:
- **Telemetry (star-lord)**: new lever may emit new telemetry fields (per-attempt energy_type_lever_applied; convergence-iteration impact); schema v2.14 implications coordinated with W0.9
- **Generation (rocket)**: lever evaluation reads kit metadata (energy_type); confirm field availability + propagation

MIGRATION.md entry per ADR-004 + R11(b) round-trip.

### Step 6 — Tag

Intermediate tag: `qd-rebuild/v0.1-b14-5-v2-energy-type-lever`.

## Required reading before starting

- `agentic_orchestration/dispatches/2026-05-16-rocket-b6-pre-work-energy-type-aware-tiers.md` (B6 pre-work dispatch + completion record; the rocket-side complement)
- `reincarnated-engine/src/reincarnated/generation/math/b6-pre-work-energy-tier-shift.md` (rocket's math note on tier-addressable portion; cite the ~2.4-3.3× combined factor and the 1.7× residual logic)
- `reincarnated-engine/src/reincarnated/simulation/math/modifier-range-root-cause.md` §4.3 (gamora's prior LC-004 decomposition)
- `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md` § 1.2 + § 3 OQ-6 (modifier ranges per substrate; physical hunter ceiling)
- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` LC-004
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-16 entry "B10.4 Option 2 modifier baseline" (the originating LC-004 analysis)
- `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` (target file)
- `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` (your prior records — recompose-hive P0/P1/P2 are precedents for primary-recompose-loop lever work)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (especially #1, #2, #11.1, #17, #18 named-constants discipline, R11(b))

## Math-before-code (REQUIRED — see Step 0)

Knight-rider routes the math note for jack-ryan Gate-1 review BEFORE code change. Per recompose-hive P1 precedent: gandalf brief v1.0 → jack-ryan Gate-1 → amendments folded → implementation. Same critique-pair pattern here.

## Cross-seam contract change? (Principle 6 gate)

**Likely YES** — energy-type lever telemetry fields are NEW. Round-trip required.

**Round-trip smoke: per Step 5 — new telemetry fields (energy_type_lever_applied; per-attempt lever decision) populate in `class_balance_results.json`. Production-path fixture: convergence run of 1 physical-archetype kit + 1 mage-archetype kit; verify per-attempt lever decisions differ. Consumer boundary exercised: star-lord telemetry consumer reads new fields without error. Field-presence check: all new fields populate for the test kits.**

MIGRATION.md entry per ADR-004. Coordinate with star-lord + W0.9 (schema v2.14 likely shared).

## Scope

- [x] Math-before-code note authored (Step 0; route through knight-rider for jack-ryan Gate-1 BEFORE code change)
- [ ] Energy-type lever implemented in primary recompose loop (Step 1)
- [ ] Unit tests added + smoke pass (Step 2)
- [ ] Calibration sweep documented (Step 3; mean |mod - 1.0| shift; per-tier WR validation)
- [ ] Coordinated with W0.9 sequencing (Step 4)
- [ ] MIGRATION.md per ADR-004 (Step 5)
- [ ] Round-trip smoke per Principle 6
- [x] AGENT_STATE.md updated
- [ ] Tag: `qd-rebuild/v0.1-b14-5-v2-energy-type-lever`

## Acceptance criteria

- [ ] Math note predictions documented vs calibration sweep measurements (Discipline #1)
- [ ] Mean |mod - 1.0| epoch shift in expected direction (closer to 0.50 target)
- [ ] No regressions in existing 179/179 tests
- [ ] Cold-start canonical convergence on smoke season passes (Discipline #11.1)
- [ ] Round-trip smoke: new telemetry fields populate end-to-end (gamora sim → star-lord)
- [ ] OQ-6 (physical hunter modifier=1.0 ceiling): document whether lever closes it OR surfaces irreducibility

## Out of scope

- Architectural archetype refactor (W0.2; rocket-side)
- Gauntlet architecture migration (W0.9; same gamora; separate dispatch)
- Skill tree node population (W1.13; P1)
- Multi-dim convergence optimizer (P2/P3)
- Cohesion-judge integration (P5)
- Profile A/B/C/D filtering (P6)

## Open questions for the agent to resolve

- **Lever composition**: combined (rage startup + miss-rate adjustment + armor adjustment) or selective? Math note Step 0 documents choice with reasoning.
- **W0.9 sequencing**: if W0.9 is in-flight, do you wait for it to complete before W0.1 Step 3 calibration sweep, OR run sweep under both gauntlets (PackProxy baseline + new gauntlet)? Coordinate with knight-rider.
- **OQ-6 physical hunter**: if the lever closes the modifier=1.0 ceiling pathology, document; if not (boss_wr still 0 under lever-applied + modifier ceiling), document that OQ-6 routes to W0.2 + W0.9 joint resolution; this is a Track C-flagged downstream item, not a W0.1 acceptance blocker.
- **Reversibility**: per recompose-hive precedent (named constants; soft-disable via constant assignment), the lever should be reversible via single-constant change. Document the reversibility plan in code docstring + this dispatch's completion record.

## Critique-pair structure

- **jack-ryan** Gate-1 reviews math note BEFORE code (architectural alignment + amendment surface)
- **gandalf** Gate-2 reviews calibration sweep findings + OQ-6 disposition (design-judgment alignment)
- **knight-rider** folds verdict into state-of-hive doc + decisions-log entry

## References

- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` § 4 Step 4 W0.1
- `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md` § 1.2 + § 3 OQ-6 (modifier-range data + physical hunter ceiling)
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` § 6.1.2 W0.1 (success criterion: post-fix mean |mod - 1.0| moves toward 0.50)
- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` LC-004 (full disposition)
- `agentic_orchestration/dispatches/2026-05-16-rocket-b6-pre-work-energy-type-aware-tiers.md` (B6 pre-work precedent — tier-addressable portion shipped)
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-16 "B10.4 Option 2 modifier baseline" entry (LC-004 derivation)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (especially #1, #2, #11.1, #17, R11(b), #18 named-constants, Pattern P7)
- `agentic_orchestration/matt-briefing-qd-rebuild-activation-2026-05-21.md` § 4 (this dispatch interpretation of W0.1; gandalf endorsement)

---

## Completion record

### Phase 1 (math-before-code) — COMPLETE 2026-05-21

**Completed by:** gamora
**Date:** 2026-05-21
**Math note:** `reincarnated-engine/src/reincarnated/simulation/math/w0-1-b14-5-v2-energy-type-lever.md`
**AGENT_STATE.md:** updated with W0.1 Phase 1 status

**Key deliverables:**
- LC-004 decomposition updated with Discipline #11.1 cold-start tier-aware factors (boss-tier miss rate 1.82×, not the warm-start aggregate ~1.18×)
- Lever design: combined sub-lever A (rage startup energy cost priority in `_lever_cooldown_energy`) + sub-lever B (new `_lever_energy_type_calibration` as 4th lever in `_primary_recompose_loop`; probe adjustment factor `ENERGY_TYPE_LEVER_PROBE_ADJUSTMENT = 1.25` for `frozenset({"rage", "combo", "stamina-as-resource"})` classes)
- Modifier compression prediction: physical_warrior 0.38 → 0.60–0.70 (post-B6+W0.1 combined); mean |mod-1.0| 0.82 → 0.65–0.72
- OQ-6 disposition: IRREDUCIBLE at W0.1 simulation layer; routes to W0.2 + W0.9 joint resolution
- W0.9 joint-resolution call: W0.1 is physical/rage upward compression; mage low-modifier compression is W0.9 + existing tier-weighted convergence (boss_weight=4.0) path; these are parallel, not serial
- Reversibility: `ENERGY_TYPE_LEVER_PROBE_ADJUSTMENT = 1.0` for soft-disable; named constants; floor-lock interaction guard (G3 — sub-lever B must short-circuit when `floor_lock_detected=True`)
- Cross-seam: `energy_type_lever_applied: bool` field rides W0.9 schema v2.14 migration (coordinate with star-lord)
- Three Gate-1 architectural concerns documented: G1 (probe adjustment soundness), G2 (focus/hunter exclusion criterion), G3 (floor-lock interaction)

**Open questions resolved:**
- Lever composition: combined sub-lever A + B (not armor adjustment — armor gap closed by B6; not per-tier target modification — global change, incorrect seam)
- W0.9 sequencing: calibration sweep preferred AFTER W0.9 Phase 2; document as PackProxy baseline if run before
- OQ-6: documented as W0.2 + W0.9 joint resolution; NOT a W0.1 acceptance blocker (per dispatch § OQ-6)
- Reversibility: documented per recompose-hive precedent (named constants, soft-disable, docstring framing)

**Phase 2 (implementation) status:** PENDING — awaiting jack-ryan Gate-1 + gandalf architectural review routing via knight-rider

**Tag `qd-rebuild/v0.1-b14-5-v2-energy-type-lever`:** NOT YET — fires after full implementation + calibration sweep ships
