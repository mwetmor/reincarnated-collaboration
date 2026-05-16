# Dispatch — 2026-05-16 — rocket — B11 generator support: geometry palette expansion 16 → 25 active types (VS2a critical-path)

**From:** knight-rider (authored per roadmap §VS2a B11 + gandalf geometry-VFX-coverage commission note: "B11 engine + sim phases may proceed" while drax demo integration is HELD on Track 4)
**To:** rocket
**Approved by:** Matt at 2026-05-16 Day 4 batch directive ("draft and fire others who are idle as we need to move on to VS2a")
**Status:** PENDING — ACTIVE (D1 Q1/Q4 amendments completed @ `rocket/v1.3-d1-rubric-q1-q4-amendments @ 6cadbf5c`; form-bias Stage 1 completed @ `rocket/v1.3-form-bias-stage-1-embodiment-axis @ 73db17f`; this dispatch unblocked 2026-05-16 Day 4)
**Estimated effort:** 2-3 sessions (~8-12h); generator-side geometry palette expansion + ability_grammar updates + smoke validation; VS2a critical-path.
**Acceptance:** Geometry palette expanded from 16 → 25 active types per `canonical/09-geometry-palette-discussion.md`; new geometry types are generator-emitable; ability_grammar accommodates the expansion; smoke season generates skills using new geometry types; intermediate tag; MIGRATION.md per ADR-004.

---

## Context — what gandalf's commission unblocks

Per gandalf's 2026-05-16 geometry-VFX-coverage-investigation commission notification:

> Notify rocket + gamora that B11 engine + sim phases may proceed; notify drax that B11 demo integration is HELD pending gap-severity assessment

**B11 engine-side work (THIS dispatch + future gamora sim-side work) is unblocked.** Drax B11 demo integration is HELD pending gandalf's Track 4 gap-severity assessment (which depends on legolas geometry-signature re-pass + elrond rubric — both in flight / authored).

## What this dispatch does

Per `canonical/09-geometry-palette-discussion.md` (consult for the canonical 25-type list):

### Step 1 — Geometry palette extension

In the generator's geometry-palette definition (likely `src/reincarnated/generation/ability_grammar.py` or `composition_rules.py`):

- Add the 9 NEW geometry types per the canonical 09 doc — extending current 16 to 25 active types
- Examples (verify against canonical/09 — these are illustrative): `leap_strike`, `vortex_pull`, `summon`, `buff_self`, `debuff_target`, `melee_strike`, `melee_arc`, `melee_thrust`, `melee_cleave` (or per the specific 9 in canonical/09)
- Each new geometry type needs: identifier, mechanical signature (damage/control/sustain), range_profile compatibility, energy-system compatibility

### Step 2 — ability_grammar update

If `ability_grammar.py` validates geometry assignments per skill, extend the grammar to:
- Accept new geometry types as valid
- Validate per-archetype geometry constraints (per `composition_rules.py` if relevant)
- Preserve all existing 16-type validations

### Step 3 — Generator emission

Update `class_generator.py` (and any related orchestration) to:
- Sample from the expanded 25-type palette during skill generation (where appropriate)
- Respect per-archetype constraints (e.g., warrior archetypes weight toward melee_*; mage archetypes weight toward arcane projectile types)
- Per-archetype distribution should naturally bias toward genre-canonical geometry types

### Step 4 — Tests + smoke

Per Discipline #2:
- Add unit tests for new geometry-type validity + per-archetype constraint validation
- Smoke a 5-class season; verify new geometry types appear in generated skills
- Verify NO existing tests fail (additive expansion should preserve all 16-type baseline behavior)

### Step 5 — MIGRATION.md entry

Append entry to `src/reincarnated/generation/MIGRATION.md`:
- 9 new geometry types with semantics
- Per-archetype distribution behavior
- Cross-seam consumers:
  - **Gamora** (Stage A2 sim consumption per spatial-data cascade Step 3): new geometry types must be sim-resolvable; gamora may need follow-on if new geometries lack sim mechanics
  - **Drax** (B11 demo integration; HELD on gandalf Track 4): demo must render the 9 new geometry types when integration unblocks
  - **Elrond** (geometry × element coverage matrix): the rubric output (Track 3 dispatch) operates against the 25-type vocabulary; gap-severity (Track 4) assesses CRITICAL coverage gaps per the 25-type expansion

### Step 6 — Intermediate tag + AGENT_STATE + completion record

- Tag: `rocket/v1.3-b11-geometry-palette-25-types` intermediate
- AGENT_STATE.md updated
- Completion record at bottom of this dispatch filled

## Cross-seam considerations

- **Gandalf:** the 9 new types per `canonical/09-geometry-palette-discussion.md` are gandalf-design-lineage; don't deviate without gandalf input
- **Gamora:** READ-ONLY; B11 sim-side work (mechanical resolution for new geometry types) is a separate gamora dispatch. If new geometries lack sim-mechanic-resolution paths, file finding; do NOT modify gamora's seam
- **Drax:** READ-ONLY; B11 demo integration HELD pending gandalf Track 4 gap-severity assessment
- **Elrond:** READ-ONLY; geometry × element coverage rubric (Track 3 dispatch) operates against your expanded vocabulary
- **Knight-rider:** notify at completion; the B11 generator + sim phases proceed; drax demo phase unblocks post-Track 4

## Out of scope (explicit)

- **NO sim-side mechanical resolution for new geometry types** — gamora's seam; separate dispatch
- **NO drax demo rendering** — HELD on gandalf Track 4
- **NO geometry-vocabulary extension beyond the canonical 09 list** — gandalf design-lineage
- **NO per-archetype distribution tuning beyond defaults** — playtest may surface tuning needs; separate dispatch
- **NO B13 active mobility / telegraphs / i-frames** — separate work; deferred per roadmap

## Required reading

- `canonical/09-geometry-palette-discussion.md` (source-of-truth for 25-type list + per-type semantics)
- `canonical/16-project-roadmap.md` §VS2a B11 (scope framing)
- 2026-05-16 spatial-data jsonschema decisions-log entry (committed `303258c`) — per-encounter dimension library context for spatial validation
- `reincarnated-engine/src/reincarnated/generation/ability_grammar.py` + `composition_rules.py` (target files)
- `reincarnated-engine/src/reincarnated/generation/class_generator.py` (orchestration target)
- `agentic_orchestration/dispatches/2026-05-16-legolas-geometry-signature-re-pass.md` (parallel work; legolas catalogs vendor coverage against the 30-target vocab; your generator emits the 25-active subset)
- `canonical/story/drift-audit.md` Drift-11 entry (load-bearing-dimension catch pattern)

## Acceptance criteria

- [ ] 9 new geometry types added to generator-emitable palette (25 total active)
- [ ] ability_grammar accommodates the expansion; per-archetype constraints preserved
- [ ] Generator emits new geometry types in smoke season
- [ ] Unit tests pass (existing + new geometry-type tests)
- [ ] No existing tests fail (additive preservation)
- [ ] MIGRATION.md entry filed
- [ ] Intermediate tag `rocket/v1.3-b11-geometry-palette-25-types` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion

## Tag policy

- **Intermediate tag:** `rocket/v1.3-b11-geometry-palette-25-types` at the commit closing palette expansion + smoke pass.
- **Milestone tag:** none from this dispatch.

---

## Completion record

**Completed:** 2026-05-16

**Intermediate tag:** `rocket/v1.3-b11-geometry-palette-25-types` @ `ec31682`

**9 new geometry types added (list):**
1. `dash_attack` — motion-AOE gap-closer; close-range warrior (upgraded from DEFER per B11)
2. `leap_strike` — jump-strike landing AOE; alternate close-range gap-closer (upgraded from DEFER)
3. `whirlwind` — spinning AOE-while-moving; warrior cleave identity (upgraded from DEFER)
4. `chain_lightning` — primary hit arcs to N nearby targets (PoE Chain meta)
5. `ricochet_bounce` — projectile bounces target-to-target
6. `fork` — projectile splits into N on impact (PoE Fork meta)
7. `vortex_pull` — pulls enemies to point + AOE; controller positional identity
8. `ring` — donut-shaped AOE (outer minus inner radius); Shock-Nova archetype enabler
9. `multi_projectile` — radial N-projectile burst; hunter/skirmisher AOE (PoE Multishot meta)

All 9 were already wired into VALID_GEOMETRIES, _CLOSE_RANGE_GEOMETRY_POOLS,
_MEDIUM_LONG_GEOMETRY_AUGMENTS, AOE_GEOMETRIES, and archetype templates from B6 work.
This dispatch adds the 4 canonical parameter expansions and the geometry_params field.

**New schema field added:** `Ability.geometry_params: dict[str, str] = {}` (additive)

**4 B11 parameter expansions implemented:**
- `collision_mode` on `line`: stop_on_first (70%) / pierce_all (30%)
- `angle_distribution` on `multi_projectile`: spread (55%) / cardinal/diagonal/star (15% each)
- `sweep_shape` on `melee_arc`: pie (70%) / crescent (30%)
- `damage_falloff` on radial geometries: uniform (50%) / linear (30%) / exponential (20%)

**Per-archetype distribution observations (5-class smoke):**
- physical_warrior (close/rage): emits melee_strike, ground_slam, melee_arc, dash_attack — B11 gap-closer active
- water_controller (medium/control): emits ring, vortex_pull — B11 controller shapes active
- hunter (long/physical/focus): emits ranged_physical, fork, ricochet_bounce — B11 multi-target active
- fire_mage (medium/mana): emits circle, cone, projectile — pre-B11 shapes dominant (expected; archetype bias)
- wind_caster (medium/mana): emits multi_projectile, line — B11 radial burst active
- chain_lightning, leap_strike, whirlwind not seen in 5-class smoke (probabilistic; archetype/seed)

**Smoke status:** PASS — 5-class smoke generates without errors; 6/9 B11 new types emitted; all 4 parameter expansion types confirmed working; all 450 prior tests pass; 46 new B11 tests pass.

**MIGRATION.md path:** `src/reincarnated/generation/MIGRATION.md`

**Notes for knight-rider:**

1. **Gamora B11 dispatch required.** 9 new geometry types are emittable but not sim-resolvable.
   Gamora sim currently treats unknown geometries as single_target. The largest gaps:
   - Multi-target dispatch (chain_lightning, ricochet_bounce, fork) — needs N-target fan-out
   - Positional displacement (vortex_pull, leap_strike) — needs enemy position update
   - Motion-AOE sequences (dash_attack, whirlwind) — needs movement-phase hit-during-motion
   - Donut hitbox (ring) — needs outer-minus-inner radius exclusion logic
   Full gap detail in MIGRATION.md. Recommend gamora B11 sim-side dispatch as next gamora task.

2. **Drax B11 demo integration remains HELD** pending gandalf Track 4 gap-severity assessment.
   No action required from drax until Track 4 completes. `geometry_params` is available on Ability
   objects when drax integration unblocks.

3. **Step-1-bounded-review of 156-entry D1 pool** (queued behind this dispatch per commission
   framing) is now unblocked on the rocket side. That review proceeds against the amended D1 rubric
   (Q1/Q4 amendments at `rocket/v1.3-d1-rubric-q1-q4-amendments`).

4. **B13 strafe_mode and dodge_stance** from canonical/09 B13 section are NOT yet in VALID_GEOMETRIES.
   Those require a future B13 generator dispatch. The 3 already-implemented B13 types (blink,
   defensive_dash, roll) are in VALID_GEOMETRIES and emit correctly.

5. **Acceptance criteria checklist:**
   - [x] 9 new geometry types added to generator-emitable palette (25 total active)
   - [x] ability_grammar accommodates expansion; per-archetype constraints preserved
   - [x] Generator emits new geometry types in smoke season (6/9 in 5-class; probabilistic)
   - [x] Unit tests pass (46 new + 450 existing)
   - [x] No existing tests fail (additive preservation confirmed)
   - [x] MIGRATION.md entry filed
   - [x] Intermediate tag `rocket/v1.3-b11-geometry-palette-25-types` cut
   - [x] AGENT_STATE.md updated
   - [ ] Knight-rider notified (this record serves as notification)
