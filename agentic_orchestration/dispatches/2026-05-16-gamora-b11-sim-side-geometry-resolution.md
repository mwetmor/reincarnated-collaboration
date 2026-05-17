# Dispatch — 2026-05-16 — gamora — B11 sim-side geometry resolution (9 new types; sequenced BEFORE drax B11 demo)

**From:** knight-rider (authored per rocket B11 generator completion gap-flag + Matt 2026-05-16 sequencing directive: "agree for #2, before" — gamora B11 sim BEFORE drax B11 demo)
**To:** gamora
**Approved by:** Matt at 2026-05-16 Day 4 (Tier 1 #2 confirmed: BEFORE drax B11 demo unblock)
**Status:** PENDING — ACTIVE (modifier-clamp gate completed @ `gamora/v1.3-modifier-clamp-gate`; this dispatch unblocked 2026-05-16 Day 4)

**AMENDMENT 2026-05-16 (post gandalf Track 4 approval)**: Matt confirmed 4 vocabulary collapses today. Bake these into your sim mechanics work:
- `projectile_homing` → DROP (collapse to `projectile_straight` + homing behavioral flag; sim implements homing as projectile mechanic, not separate geometry type)
- `aura_directional` → DROP (collapse to `cone + persistent + damage_falloff: uniform`)
- `melee_cleave` → DROP (collapse to `melee_arc + sweep_shape: wide_arc` — sim adds `sweep_shape` parameter to `melee_arc` mechanics; ranges: narrow / standard / wide_arc)
- `iframe_dash` → DROP (collapse to `dash_attack` / `defensive_dash` with `i_frame_window` metadata; sim adds `i_frame_window` parameter to dash mechanics; default 0.1-0.2s window)

Add the following sim-parameter support per Track 4 collapses:
- `sweep_shape` parameter on `melee_arc` (values: narrow / standard / wide_arc; affects hit-cone angle)
- `i_frame_window` metadata on `dash_attack` / `defensive_dash` (seconds value; player invulnerable during window)
- `homing` behavioral flag on `projectile_straight` (boolean; if true, projectile tracks initial target)
- `damage_falloff: uniform` value on `cone` geometry persistence parameter
**Estimated effort:** 3-4 sessions (~10-15h); sim-side mechanic implementation for 4 categories of new geometry types; calibration validation against prior 5-class smoke from rocket B11.
**Acceptance:** Sim mechanics implemented for 9 new B11 geometry types per the 4 mechanic categories below; sim no longer falls back to single_target for these types; smoke season verifies sim resolves per-type mechanics correctly; calibration regression check vs prior modifier ranges; intermediate tag; MIGRATION.md per ADR-004.

---

## Context — what rocket B11 left unresolved

Per rocket B11 generator completion (`rocket/v1.3-b11-geometry-palette-25-types @ ec31682` + MIGRATION.md):

> The 9 new geometry types emit from generator but are NOT sim-resolvable; sim falls back to single_target for unknown geometries. Gamora needs a B11 sim-side dispatch to close.

**Gap detail** per rocket MIGRATION.md:
- **Multi-target fan-out** (3 types): `chain_lightning`, `ricochet_bounce`, `fork`
- **Positional displacement** (2 types): `vortex_pull`, `leap_strike`
- **Motion-AOE sequences** (2 types): `dash_attack`, `whirlwind`
- **Donut hitbox** (1 type): `ring`
- **Plus support type** (1 type): `multi_projectile` (likely fan-out variant)

**Why BEFORE drax B11 demo** (Matt sequencing decision 2026-05-16): cohesive ship; demo integration sees fully resolved sim; matches "do it right" pattern from arena re-dim → room/hallway directive. Drax B11 demo dispatch remains HELD pending gandalf Track 4 gap-severity assessment (in flight now) AND your sim-side resolution (this dispatch).

## What this dispatch does

### Step 1 — Multi-target fan-out (3 types)

Implement sim mechanics for:

- **`chain_lightning`**: primary hit on target, then arcs to N additional nearby targets within radius R, damage falloff per arc (PoE Chain meta). Parameters: N (chain count; default 3-5; should be configurable per skill), R (arc radius; default 4-6m), per-arc damage multiplier (default 0.7 per arc per PoE convention).
- **`ricochet_bounce`**: projectile hits target, bounces to next-nearest target, repeats up to N bounces. Parameters: N (bounce count; default 2-4), max bounce distance (default 5-8m).
- **`fork`**: projectile splits into 2-3 new projectiles upon hit OR at midflight; new projectiles continue toward new targets. Parameters: fork count (default 2-3), fork angle (default 30-45°).

**Fan-out target selection logic**: nearest-target priority within radius; do not re-target same enemy (no double-dipping); decay damage per fan-out tier per existing damage attribution conventions.

### Step 2 — Positional displacement (2 types)

- **`vortex_pull`**: applies force vector pulling targets toward origin point over duration D. Parameters: pull strength (m/s²), pull duration D (default 0.5-1.0s), pull radius (default 4-6m). Affects all targets within radius; respects enemy mass / displacement-immunity if such mechanics exist.
- **`leap_strike`**: caster jumps to target location (existing player-movement-speed values apply for travel duration); upon landing emits AOE damage burst. Parameters: jump distance cap (default 6-10m), landing AOE radius (default 2-3m), AOE damage multiplier (default 1.2-1.5x base).

**Displacement-immunity**: do not displace boss-tier enemies (per genre convention); flag for gandalf design call if you need to define which enemy tiers are immune.

### Step 3 — Motion-AOE sequences (2 types)

- **`dash_attack`**: caster moves rapidly along vector for duration D, applying damage to all enemies in path. Parameters: dash distance (default 4-8m), dash duration (default 0.2-0.4s), path-hitbox width (default 1-2m).
- **`whirlwind`**: caster spins in place applying continuous AOE damage to all enemies in radius R for duration D (or until canceled). Parameters: radius (default 2-3m), duration (default 1-3s OR until energy depletion), tick rate (default 4-6 ticks/s), per-tick damage multiplier.

**Motion semantics**: dash_attack should respect arena bounds (consult room/hallway topology from drax dispatch in-flight — for now, fallback to existing bound-clamping). whirlwind anchors caster position during channel.

### Step 4 — Donut hitbox (1 type)

- **`ring`**: AOE damage in annular region (outer radius R, inner radius r); enemies at center are SAFE, enemies in ring are hit. Parameters: outer radius (default 4-6m), inner radius (default 1-2m), damage multiplier (default 1.2-1.5x base for the "skilled-positioning" payoff).

**Geometric resolution**: distance-from-origin check; inside inner radius = miss; between inner+outer = hit; outside outer = miss.

### Step 5 — Multi_projectile (support type)

- **`multi_projectile`**: caster emits N projectiles in fan pattern. Parameters: projectile count (default 3-5), fan angle (default 60-120°), per-projectile damage (typically reduced from single-target baseline; default 0.5-0.7x per projectile).

May overlap with `fork` mechanically; treat as distinct types per rocket's emission convention.

### Step 6 — Calibration regression check

This is load-bearing per Discipline #1 (math-before-code) — the new mechanics could shift class modifier distributions:

- Smoke a 5-class season post-implementation (use same archetypes as rocket B11 smoke: fire_mage / water_controller / physical_warrior / wind_caster / hunter)
- Compare modifier values vs the previous calibration baseline (pre-B11; pre-new-mechanic introduction)
- If any modifier moves >2.0 in either direction from prior baseline, FLAG via your modifier-clamp gate (just landed) + surface to knight-rider for routing
- If modifiers stay within ±0.5 of prior baseline, calibration is preserved (expected outcome — the new mechanics are sub-optimal default-parameter sets pending B6.1 tuning)

### Step 7 — Tests + smoke

Per Discipline #2:
- Unit tests per geometry type: mechanic-trigger; parameter-bounds; fan-out target selection; AOE radius/inner-radius correctness
- Smoke 5-class season verifies new geometry types resolve mechanically (NOT fall-back-to-single_target)
- Verify NO existing tests fail (additive sim mechanics should preserve all baseline 16-type behavior)
- Calibration regression check per Step 6 above

### Step 8 — MIGRATION.md entry

Append to `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (or equivalent gamora-owned MIGRATION):

- 9 new geometry-type sim mechanics with semantics + default parameters
- Cross-seam consumers:
  - **Rocket** (READ-ONLY): B11 generator emits the types; this dispatch resolves the sim-mechanic gap
  - **Drax** (B11 demo integration; HELD on gandalf Track 4): demo rendering needs to reflect these mechanics visually (chain arcs visible; vortex pull visible; ring donut hitbox visible)
  - **Star-lord** (telemetry): per-fight emission may need new fields if any of these mechanics require attribution beyond existing damage-source tracking (your call on whether telemetry schema changes are needed; likely NOT for this dispatch)
  - **Knight-rider**: notify at completion; drax B11 demo dispatch now has full upstream resolution (generator + sim); gandalf Track 4 + this dispatch are the joint gate for drax B11 demo unblock

### Step 9 — Intermediate tag + AGENT_STATE + completion record

- Tag: `gamora/v1.3-b11-sim-side-geometry-resolution`
- AGENT_STATE.md updated
- Completion record at bottom of this dispatch filled
- Flag any default-parameter sets you suspect need B6.1 tuning attention (separate downstream dispatch territory; don't tune here)

## Cross-seam considerations

- **Rocket**: READ-ONLY upstream; B11 generator gives you the emit-side substrate; do NOT modify rocket files
- **Drax**: READ-ONLY downstream; B11 demo integration HELD on gandalf Track 4 + this dispatch; do NOT modify drax files
- **Gandalf**: READ-ONLY upstream design intent (canonical/09 geometry palette); if you need design clarification on any geometry's intended mechanic feel, surface as finding for gandalf input
- **Star-lord**: READ-ONLY; if telemetry schema needs amendment to capture new mechanic attribution, file finding; do NOT modify star-lord files
- **Knight-rider**: notify at completion; drax B11 demo dispatch routing depends on both this + gandalf Track 4

## Out of scope (explicit)

- **NO drax demo rendering** — HELD on gandalf Track 4 + this dispatch joint resolution
- **NO geometry-vocabulary extensions beyond the 9 rocket-emitted types** — gandalf design-lineage; new types require gandalf input
- **NO B6.1 default-parameter tuning** — flag defaults that need attention; separate downstream dispatch
- **NO B13 active mobility / telegraphs / i-frames** — separate work per roadmap
- **NO ailment-damage-signatures** — deferred per prior decision (Round table ailment-deferral 2026-05-12); not this dispatch's scope
- **NO modifier-clamp gate amendments** — that work landed separately this session (`gamora/v1.3-modifier-clamp-gate`); use it for regression detection only

## Required reading

- `canonical/09-geometry-palette-discussion.md` (source-of-truth for geometry-type semantics)
- `agentic_orchestration/dispatches/2026-05-16-rocket-b11-generator-geometry-palette-expansion.md` (completion record + MIGRATION.md gap detail; your input substrate)
- `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (rocket B11 entry — sim-resolution gap list)
- `reincarnated-engine/src/reincarnated/simulation/` (your target seam)
- Your prior wind_controller investigation findings (Pattern P6 relevance) + your prior modifier-clamp gate dispatch (`gamora/v1.3-modifier-clamp-gate`) — for calibration-regression-check usage
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1 (math-before-code: calibration regression check); #2 (smoke); #11 (attribution: damage source tracking per geometry type); #12 (semantic-shifting: new mechanics shift modifier distributions; calibration discipline applies)

## Acceptance criteria

- [ ] Multi-target fan-out mechanics: chain_lightning + ricochet_bounce + fork
- [ ] Positional displacement mechanics: vortex_pull + leap_strike
- [ ] Motion-AOE sequence mechanics: dash_attack + whirlwind
- [ ] Donut hitbox mechanic: ring
- [ ] Multi_projectile mechanic
- [ ] Sim no longer falls back to single_target for any of the 9 types
- [ ] Unit tests per geometry type pass
- [ ] 5-class smoke verifies sim resolution (not fallback)
- [ ] Calibration regression check: modifier shifts within ±0.5 of prior baseline OR flagged via modifier-clamp gate
- [ ] No existing tests fail
- [ ] MIGRATION.md entry filed (cross-seam consumer notes)
- [ ] Intermediate tag `gamora/v1.3-b11-sim-side-geometry-resolution` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion (drax B11 demo dispatch routing depends)

## Tag policy

- **Intermediate tag:** `gamora/v1.3-b11-sim-side-geometry-resolution` at the commit closing sim mechanics + smoke + calibration check.
- **Milestone tag:** none from this dispatch.

---

## Completion record

**Completed:** 2026-05-16 (Day 4)
**Intermediate tag:** `gamora/v1.3-b11-sim-side-geometry-resolution` (commit `0278fba`)

**Sim-resolution status (per type):**
| Geometry | Status | Multiplier (default) | Notes |
|---|---|---|---|
| `chain_lightning` | RESOLVED | 2.533× | Geometric series N=3, decay=0.7 |
| `ricochet_bounce` | RESOLVED | 2.533× | Same series as chain_lightning at defaults |
| `fork` | RESOLVED | 2.2× | 1.0 + N×per_fork_mult (N=2, mult=0.6) |
| `multi_projectile` | RESOLVED | 2.6× | N×per_projectile_mult (N=4, mult=0.65) |
| `ring` | RESOLVED | 1.2× | Skilled-positioning payoff multiplier |
| `leap_strike` | RESOLVED | 1.3× | Landing AOE burst multiplier |
| `vortex_pull` | RESOLVED | 1.0× | Pull is positional; standard AOE hit in 1v1 |
| `dash_attack` | RESOLVED | 1.0× | Standard hit; i_frame_window is metadata |
| `whirlwind` | RESOLVED | 1.0× | Channel magnitude pre-baked in skill |

All 9 types: sim no longer falls back to single_target.

**Track 4 collapses — sim-side parameter support:**
- `sweep_shape` on `melee_arc`: registered as metadata (narrow/standard/wide_arc); no damage change
- `i_frame_window` on `dash_attack`/`defensive_dash`: registered as metadata (default 0.15s); B13 scope for invulnerability simulation
- `homing` flag on `projectile_straight`: registered as metadata; VS2a+ kiting model scope
- `damage_falloff: uniform` on `cone`: registered as valid value alongside linear/exponential; no damage change (informational)

**Calibration regression check result:**
STABLE. Max modifier shift from prior V2 baseline: 0.1781 (physical_warrior; shift < 0.5 threshold).
No modifier-clamp gate triggers (all modifiers < 3.0). All 5 classes converged in smoke.
Direction matches math note §9 prediction: fan-out DPS uplift → binary search drives modifiers DOWN.

**Discipline #12 semantic shift:** `test_different_seeds_vary` updated. fire_mage seed=4 has 4 B11
fan-out geometry skills (ricochet_bounce, multi_projectile, chain_lightning, ring). Pre-B11
modifier=0.55 gave ~60% win rate; post-B11 same modifier gives ~100% win rate. Updated to 0.30
with explicit comment. Documented in MIGRATION.md §v1.7.

**Default-parameter sets flagged for B6.1 attention:**
1. `chain_lightning` N=3, decay=0.7 → 2.53×. If lightning archetypes are over-powered, lower N to 2 (1.70×).
2. `multi_projectile` N=4, per_mult=0.65 → 2.6×. Hunter primary_attack will have very high DPS — monitor modifier distribution.
3. `fork` N=2, per_mult=0.6 → 2.2×. Watch physical_skirmisher kits with fork + other AOE skills.
4. `ring` 1.2× bonus may be conservative — design intent is meaningful skilled-positioning payoff. Consider 1.35-1.5× in B6.1.

**Smoke status:**
PASS. Seed=43, 5 classes, smoke_test=True, V1 mode, 70.5s wall time.
7/9 B11 geometries emitted in smoke kits (chain_lightning, dash_attack, multi_projectile,
ricochet_bounce, ring, vortex_pull, whirlwind). fork + leap_strike not in this seed — probabilistic; expected.
All 5 classes converged. No modifier-clamp gate triggers.

**Tests:** 88 new tests in `tests/test_b11_geometry_mechanics.py`. Total suite: 1596 tests pass, 0 fail.

**MIGRATION.md path:** `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` §v1.7

**Math note:** `reincarnated-engine/src/reincarnated/simulation/math/b11-geometry-sim-mechanics.md`

**Notes for knight-rider:**
- Both upstream gates for drax B11 demo dispatch are now COMPLETE:
  - gandalf Track 4: COMPLETE (vocabulary-collapse decisions confirmed; per `canonical/story/geometry-vfx-coverage-assessment.md`)
  - This dispatch: COMPLETE (sim resolves all 9 B11 geometry types)
- Drax B11 demo dispatch may be ROUTED. Drax should consume:
  - gandalf Track 4 § 4.1 composite-render strategies (per geometry/element pair)
  - gandalf Track 4 § 4.2 per-element GREEN list (11 elements GREEN; acid YELLOW; void pending Pixogen license)
  - Track 4 vocabulary-collapse parameter semantics (sweep_shape, i_frame_window, homing, damage_falloff: uniform)
- Pixogen license verification dispatch still needed (separate operational dispatch — blocks void element in drax B11 integration)
- B6.1 tuning dispatch needed for the 4 default-parameter sets flagged above (separate downstream dispatch; not B11-ship-blocking)
- Star-lord: no action required for this dispatch (no telemetry schema changes)
- Rocket: no action required (generator already correct; canonical-09 vocabulary amendment for the 4 collapsed geometries is a separate small dispatch)

— gamora, 2026-05-16 (Day 4)
