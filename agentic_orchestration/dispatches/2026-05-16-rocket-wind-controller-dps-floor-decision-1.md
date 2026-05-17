# Dispatch — 2026-05-16 — rocket — wind_controller DPS floor (Decision 1; 3-floor approach)

**From:** knight-rider (authored per gandalf wind_controller Decision-1 recommendation + Matt directive Day-4 close: "authorize all four")
**To:** rocket
**Approved by:** Matt at 2026-05-16 Day 4
**Status:** QUEUED — fires after your in-flight rocket MS-schema-defaults dispatch returns (per-seam one-dispatch-per-session discipline)
**Estimated effort:** 1 session (~1-2h); archetype-template amendment + smoke; B6 pre-work pair

**Gate-1 bypass rationale:** Matt-directed (gandalf-recommended; jack-ryan-reinforced via V1-vs-V2 inversion finding), single-seam (rocket archetype-template only), reversible (constraint addition; can relax), bounded scope.

**Acceptance summary:** wind_controller archetype template gains 3-floor constraint per gandalf's recommendation: **skill-count floor** (≥4 DPS-producing skills) + **geometry-coverage floor** (at least one DPS skill is AOE-shaped) + **tier-coverage floor** (at least one DPS skill at Tier 1-2 / early-game accessible). Smoke verifies generator produces compliant wind_controller kits on fresh seeds. MIGRATION.md entry. Intermediate tag.

---

## Why this dispatch exists

Gamora's wind_controller V2 investigation classified the anomaly as "Kit-design issue (structural), compound." Two factors:
- **Factor A:** V2 HP-carryover × low-DPS-density kit (any wind_controller in V2 has elevated modifier)
- **Factor B:** RNG strong-outlier target slot (compounds Factor A when wind_controller gets target=0.60)

Gandalf's design analysis: "Pure control archetypes with no DPS floor are rare in solo ARPGs and almost universally party-dependent when they exist." No commercially-shipped solo-viable ARPG controller has zero DPS path. A 3.5× damage modifier reads as balance bug (engine compensating for absent damage), not archetype feature. **Players read scale through gear/skill/synergy, not engine-level numerical compensation.**

Jack-ryan's V2 calibration analysis reinforced: wind_controller had **LOWEST V1 modifier range** (0.089 — most consistent V1 archetype) yet produces **LARGEST V2 inflation** (~25× V1 mean). V1's per-encounter HP reset masked the template's low-DPS-density problem; V2's room HP-carryover unmasked it.

Per gandalf's sequencing recommendation, this is the first step of a 4-step chain. Decisions 2 (clamp gate operationalization) + 3 (strong_outlier_compatible tag) are **conditional** — fire only if Decision 1 ships + 2-3 regens still show modifier ≥3.0 routinely.

## Cross-seam contract change?

**Round-trip: YES — additive archetype-template constraints affecting generated content.**

- **Acceptance criteria includes:** round-trip smoke verifying fresh wind_controller generation produces compliant kits; downstream consumers (gamora simulation; balance loop) parse correctly with new kits
- No schema-shape change; constraint operates within existing skill-pool selection layer
- Per R11(b) Principle 6

## What this dispatch produces

### Step 1 — 3-floor constraint design (math-before-code per Discipline #1)

File a math note documenting:
- **Skill-count floor:** ≥4 DPS-producing skills (define "DPS-producing": skill that emits direct damage; control-with-damage hybrid counts; pure-control / pure-utility does not)
- **Geometry-coverage floor:** at least one DPS skill has AOE geometry (cone / nova / ground_slam / vortex_pull / aura_radial / impact_burst / etc. — exclude single-target projectile_straight if it's the only damage path)
- **Tier-coverage floor:** at least one DPS skill at Tier 1 or Tier 2 (early-game accessible — not gated to Tier 3+ only)

Document the validation order + failure semantics: if generator can't produce a kit satisfying all 3 floors after N attempts, what happens? (Options: reroll skill selection / accept with WARN + flag for review / extend pool / fail-loud. Pick + justify.)

### Step 2 — Generator wiring

Implement the 3 floors as kit-validation constraints in the wind_controller archetype template (or wherever per-archetype kit constraints live in current generation/ code).

### Step 3 — Smoke test (Discipline #2 + R11(b))

- Generate fresh wind_controller kits across 5+ seeds
- Verify each kit satisfies all 3 floors (skill count ≥4 DPS; ≥1 AOE; ≥1 Tier 1-2)
- Verify existing generator tests pass
- Verify other archetypes are not affected (constraints apply to wind_controller template only — do NOT cascade-amend other templates without explicit scope)

### Step 4 — Math note + MIGRATION.md

- Math note at `~/Games/reincarnated-engine/design/notes/wind-controller-dps-floor-2026-05-16.md`
- MIGRATION.md entry per ADR-004 — downstream consumer notes: gamora simulation (kit shape changes; balance loop should converge differently); knight-rider (post-ship 2-3 regen measurement triggers Decision 2/3 evaluation)

### Step 5 — Tag + AGENT_STATE + completion record

- Intermediate tag: `rocket/v1.3-wind-controller-dps-floor`
- AGENT_STATE updated
- Fill completion record

## Out of scope (explicit)

- **NO other-archetype DPS floors.** This is wind_controller-specific per gandalf Decision 1 scope.
- **NO clamp-gate-as-rejection logic** (gamora Decision 2 — conditional; activates only if step-3 measurement demands)
- **NO strong_outlier_compatible archetype tag** (rocket Decision 3 — conditional; activates only if Factor B remains material after Decision 1 ships)
- **NO MS schema work** (separate rocket MS-defaults dispatch in flight)
- **NO B6 trait/skill architecture changes** beyond the 3-floor wind_controller amendment
- **NO regen execution** (gamora's seam; gamora runs the post-ship 2-3 regens to measure)

## Required reading

- Gamora wind_controller math note: `~/Games/reincarnated-engine/src/reincarnated/simulation/math/wind-controller-v2-anomaly-2026-05-16.md`
- Jack-ryan V2 calibration analysis: `agentic_orchestration/qa/analyses/2026-05-16-v2-calibration-analysis.md` (especially V1-vs-V2 inversion finding)
- Gandalf's wind_controller Decision-1 recommendation (Matt-relayed Day-4 close — 3-floor approach)
- Your existing wind_controller archetype template (current state)
- B6 pre-work scoping (this is paired amendment per gandalf framing)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 math-before-code, #2 smoke, #12 semantic-shifting (archetype-template policy change), #13a/b

## Acceptance criteria

- [ ] Math note filed documenting 3-floor design + validation order + failure semantics
- [ ] Skill-count floor (≥4 DPS-producing) implemented for wind_controller template
- [ ] Geometry-coverage floor (≥1 AOE DPS) implemented
- [ ] Tier-coverage floor (≥1 Tier 1-2 DPS) implemented
- [ ] Smoke test: fresh wind_controller kits across 5+ seeds all satisfy 3 floors
- [ ] Existing generator tests pass; other archetypes unaffected
- [ ] MIGRATION.md entry filed with downstream consumer notes
- [ ] Intermediate tag `rocket/v1.3-wind-controller-dps-floor` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified with: tag hash, math note path, any pool-exhaustion concerns surfaced (does wind_controller skill pool have ≥4 DPS-producing AOE Tier-1-2 candidates?)

## Tag policy

- **Intermediate tag:** `rocket/v1.3-wind-controller-dps-floor`
- **Milestone tag:** none.

---

## Completion record

**Completed:** 2026-05-16
**Math note path:** `reincarnated-engine/design/notes/wind-controller-dps-floor-2026-05-16.md`
**Pool-exhaustion concerns:** None. Wind_controller geometry bias strongly prefers AOE types (line, cone, multi_projectile, vortex_pull, fork — all BIAS_PREFERRED=2.0 and all in AOE_GEOMETRIES). Tier 1+2 covers ~8/12 slots; ≥4 DPS skills distributed across 12 slots make floor 3 near-certain. Full analysis in math note §5.
**Intermediate tag:** `rocket/v1.3-wind-controller-dps-floor @ 2d22486`
**Tests status:** 49/49 test_wind_controller_dps_floor.py; 244/244 broader suite pass (test_class_generation, test_movement_speed_schema, test_grouping_layer_schema, test_energy_types, test_b11_geometry_palette all green)

**Notes for knight-rider:**

1. **Smoke results clean across 7 seeds including the two historically-anomalous ones (1006, 1010).** All 3 floors satisfied on every seed: seed 1010 shows DPS=4, DPS-AOE=4, DPS-T1/2=2; seed 1006 shows DPS=5, DPS-AOE=3, DPS-T1/2=3.

2. **Required_roles amendment:** Added `("burst_damage", 1)` to wind_controller required_roles (now 8 required slots total). This guarantees 3 DPS roles from required slots alone, making the `min_4_dps_skills` constraint satisfiable with high probability from free-slot sampling without burning retries. Math note §3 documents the derivation.

3. **Pre-existing physical_grappler failure noted:** `require_control_with_ailment` fails across all seeds for physical_grappler — pre-existing, not introduced by this dispatch. Documented in test file comment and excluded from "other archetypes unaffected" parameterization. Surface to knight-rider as known issue if not already tracked.

4. **Round-trip smoke needed (gamora seam):** Per cross-seam contract change (R11(b) Principle 6), gamora must verify the simulation parses new wind_controller kits cleanly and the balance loop converges correctly with the new kit shape. This is gamora's seam — not actioned here.

5. **Decision 2 + 3 trigger condition:** Both are conditional. After gamora runs 2-3 fresh regens with this code: if wind_controller modifier ≥3.0 routinely at target=0.50, Decision 2 activates (clamp gate as rejection, gamora seam). If Factor B (target=0.60 outlier slot) remains the dominant driver of ≥3.0 modifiers even with Decision 1 in place, Decision 3 activates (strong_outlier_compatible tag, rocket seam).

6. **MIGRATION.md filed** at `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` with full downstream consumer notes per ADR-004.
