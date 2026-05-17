# Dispatch — 2026-05-16 — rocket — movement_speed schema field (per gandalf movement-speed-baseline lock)

**From:** knight-rider (authored per gandalf's 2026-05-16 Day 4 movement-speed-baseline commission handoff item #1)
**To:** rocket
**Approved by:** Matt at 2026-05-16 Day 4 (gandalf locked values approved verbatim per "Matt-approved 2026-05-16" on `canonical/story/movement-speed-baseline.md`; explicit operationalization authorization per "author and fire rocket")
**Status:** PENDING — ACTIVE
**Estimated effort:** 1-2 hours per gandalf handoff
**Acceptance:** `movement_speed` field added to the engine schema (m/s, 2-decimal); class default 5.75; monster trash default 5.75; monster fast archetype range 6.6-7.5 supported; schema additive (no removals); intermediate tag; MIGRATION.md entry per ADR-004 (cross-seam: gamora consumes for Stage A2 sim extension; star-lord consumes for telemetry; drax consumes for rendering).

---

## Context — gandalf locked values (verbatim)

Per `canonical/story/movement-speed-baseline.md` (Matt-approved 2026-05-16; gandalf authored):

| Parameter | Value | Demo px/s at 48 px/m |
|---|---|---|
| Player base MS | 5.75 m/s | 276 px/s |
| Early game | 6.0 m/s | 288 px/s |
| **Mid game (VS2a)** | **7.5 m/s** | **360 px/s** |
| Late game | 8.0 m/s | 384 px/s |
| Monster trash | 5.75 m/s | 276 px/s |
| Monster fast archetypes | 6.6–7.5 m/s | 317–360 px/s |
| PIXELS_PER_METER | 48 (constant) | — |
| Range-profile MS variance | DROPPED | All classes uniform |

**Design-family anchor:** D3 / D4 / Last Epoch (conservative late-game delta +39% over trash baseline; positional gameplay preserved through progression; fast monster archetypes practically threatening at endgame). **Deliberately NOT the PoE-1 zoom-zoom track.**

## What this dispatch does

### Step 1 — Schema field additions

**Player class schema (`class_schema.py` or equivalent):**
- Add `movement_speed: float` field
- Default: **5.75** (m/s)
- 2-decimal precision (e.g., 5.75, 6.00, 7.50, 8.00)
- Per-class scaling: per gandalf's locked values + design-family framing, classes may scale within early/mid/late ranges — the schema accommodates per-class scaling but the default-value commitment per gandalf is 5.75 (base) for all classes uniformly

**Monster schema (`monster_schema.py` or equivalent):**
- Add `movement_speed: float` field
- Default: **5.75** (m/s) for trash monsters
- 2-decimal precision
- Per-archetype scaling: fast archetypes range 6.6-7.5 m/s; gandalf's locked values support per-monster-archetype scaling within these bounds

**Generator wiring (`monster_generator.py` + `class_generator.py` or equivalent):**
- Emit movement_speed when generating monsters and player classes
- Use the defaults above unless archetype-specific overrides land (gandalf-locked scaling per archetype family is the future design surface; this dispatch lands the defaults + the schema)

### Step 2 — MIGRATION.md entry (cross-seam contract per ADR-004)

Append a new entry to `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (or the relevant generation-seam MIGRATION.md). Document:

- New `movement_speed: float` field on class + monster schemas
- Unit convention: m/s (meters per second)
- 2-decimal precision
- Defaults: class 5.75; monster trash 5.75; monster fast archetypes 6.6-7.5 range
- Cross-seam consumers:
  - **Gamora** Stage A2 movement-speed-aware sim extension (per engine-balance-stewardship Lock 3b; post-VS2a tight follow per gandalf handoff #3) — consumes movement_speed for kiting modeling + 3-band distance state
  - **Star-lord** telemetry per-fight observed-MS emission (per gandalf handoff #5; separate dispatch) — consumes movement_speed for per-fight telemetry rows
  - **Drax** PixiJS demo rendering (per gandalf handoff #2; HELD pending decisions-log entry) — consumes movement_speed via PIXELS_PER_METER=48 conversion (5.75 m/s → 276 px/s, etc.)

### Step 3 — Tests + smoke

Per Discipline #2 (smoke-test discipline):
- Add unit tests for movement_speed schema presence + default-value emission
- Smoke a 5-class season generation; verify all classes emit movement_speed=5.75 default
- Smoke a monster pool generation; verify trash monsters emit movement_speed=5.75 + fast archetypes are in 6.6-7.5 range

### Step 4 — Intermediate tag

Tag: `rocket/v1.3-movement-speed-schema-field` at the commit closing schema + generator + tests pass.

**Milestone tag:** none from this dispatch. Standard ADR-003 protocol.

## Cross-seam considerations

- **Gandalf:** the values + the design-family anchor are gandalf-locked + Matt-approved. No design-instinct re-litigation; you implement to-spec.
- **Gamora:** READ-ONLY consumer (Stage A2 follow-on dispatch consumes; not this dispatch). If schema fields you add are insufficient for gamora's eventual Stage A2 work, surface a finding; do NOT modify gamora's seam.
- **Star-lord:** READ-ONLY consumer (telemetry observed-MS dispatch — separately authored per gandalf handoff #5).
- **Drax:** READ-ONLY consumer (PixiJS rendering dispatch — separately authored per gandalf handoff #2; HELD pending knight-rider's decisions-log entry landing).
- **Knight-rider:** notify at completion; coordinates the decisions-log entry drafting in parallel (your output isn't blocked on the decisions-log entry; you implement schema while knight-rider drafts).

## Out of scope (explicit)

- **NO per-class movement_speed override values.** Defaults only per gandalf-locked baselines. Per-class scaling-within-range is future generation-side design surface; not this dispatch's scope.
- **NO simulator-side consumption.** Gamora's seam; separate dispatch (Stage A2 movement-speed-aware sim extension; post-VS2a tight follow).
- **NO telemetry per-fight observed-MS emission.** Star-lord's seam; separate dispatch (gandalf handoff #5).
- **NO PixiJS rendering implementation.** Drax's seam; separate dispatch HELD pending decisions-log entry.
- **NO arena-scale verification.** Drax's verification work per gandalf's "single thing to watch" note; not generation-side.
- **NO spatial / floor / wall data schema work** (the separate gandalf spatial-data jsonschema commission addresses this; held pending Matt confirmation that gandalf's movement-speed work covers / doesn't cover the spatial-data half).

## Required reading

- `canonical/story/movement-speed-baseline.md` (gandalf's locked values; Matt-approved; source-of-truth)
- `agentic_orchestration/gandalf/requests/2026-05-16-movement-speed-baseline-vs2a-gating.md` (gandalf's commission + handoff items #1-5 + the decisions-log entry template)
- `canonical/16-project-roadmap.md` §VS2a (updated by gandalf with locked values + B12 split entry)
- `canonical/story/engine-balance-stewardship.md` § Gate 3 (updated by gandalf with supersession note)
- 2026-05-16 form-bias 5-entry batch (committed `5d51b5a`) — Entry 1 strategic-axis lock + Entry 2 three-layer model; spatial / movement work lives at the substrate-mechanical layer (sub-lock a)
- `reincarnated-engine/src/reincarnated/generation/class_schema.py` + `monster_schema.py` (your target files)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #2 (smoke-test); #11 (attribution: cite gandalf's locked values verbatim in code comments); #12 (semantic-shifting: movement_speed becomes a meaningful axis after this lands)

## Acceptance criteria

- [ ] `movement_speed: float` field added to class + monster schemas with defaults (class 5.75; monster trash 5.75; monster fast archetypes 6.6-7.5 range)
- [ ] Generator emits movement_speed for all classes + monsters
- [ ] Unit tests pass (existing + new movement_speed tests)
- [ ] Smoke season verifies field presence + correct defaults
- [ ] MIGRATION.md entry filed per ADR-004 cross-seam contract
- [ ] Intermediate tag `rocket/v1.3-movement-speed-schema-field` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion

---

## Completion record

**Completed:** 2026-05-16
**Intermediate tag:** `rocket/v1.3-movement-speed-schema-field` @ commit `62624dd`
**Smoke status:** PASSED — 5-class smoke (fire_mage/water_controller/hybrid_mage/wind_caster/physical_warrior all emit movement_speed=5.75); 8-monster smoke (trash baseline 5.75, fast archetypes swarmer/sniper emit 6.60 in locked range). Full suite: 1384 passed, 0 failed. Star-lord v2.2 defensive-null test `test_smoke_with_rocket_emitted_default_5_75` PASSED confirming cross-seam coordination is clean.
**MIGRATION.md path:** `reincarnated-engine/src/reincarnated/generation/MIGRATION.md`
**Notes for knight-rider:** Schema is additive — existing season JSON without movement_speed deserializes at default 5.75. Gamora Stage A2 can now consume `PlayerClass.movement_speed` + `Monster.movement_speed` (both always populated, no null handling needed). Star-lord v2.2 telemetry dispatch already has defensive null handling that is now satisfied by the 5.75 default. Drax dispatch (gandalf handoff #2 HELD) can consume immediately when knight-rider unblocks it; PIXELS_PER_METER=48 is drax-side constant (5.75 * 48 = 276 px/s base; 7.5 * 48 = 360 px/s VS2a mid). Fast-archetype fine-tuning within the locked 6.6-7.5 m/s range is gamora Stage A2 design-call per gandalf; current swarmer/sniper = 6.60 m/s (low end of range).
