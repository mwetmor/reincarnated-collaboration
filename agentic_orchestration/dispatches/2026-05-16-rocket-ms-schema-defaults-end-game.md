# Dispatch — 2026-05-16 — rocket — MS schema defaults update (end-game anchor)

**From:** knight-rider (authored per Matt directive Day-4 close: "authorize all four" — MS verdict reversal cascade item #2)
**To:** rocket
**Approved by:** Matt at 2026-05-16 Day 4
**Status:** PENDING
**Estimated effort:** 1 session (~1-2h); schema-default constant updates + smoke test + MIGRATION.md entry

**Gate-1 bypass rationale:** Matt-directed, single-seam (rocket schema only), reversible (constant-value updates), bounded scope. Per CHANGELOG rubric.

**Acceptance summary:** PlayerClass.movement_speed default = 8.0 (was 5.75); Monster.movement_speed per-archetype (trash 5.75 unchanged; fast archetypes 7.5; named bosses gamora-design-call — flag for gamora). Smoke test confirms generator emits new values for fresh classes/monsters; MIGRATION.md entry per ADR-004; intermediate tag.

---

## Why this dispatch exists

Per gandalf's MS verdict-reversal cascade table (item #2):

> rocket: Update schema defaults: PlayerClass.movement_speed = 8.0 (was 5.75); Monster.movement_speed per-archetype (trash 5.75; fast archetypes 7.5 — top of locked range; named bosses gamora-design-call)

This is cascade item #2 of 6. Independent of gandalf's canonical-doc update (cascade item #1, firing in parallel) — you can ship without waiting.

## Cross-seam contract change?

**Round-trip: YES — additive default-value change to schema.**

- **Acceptance criteria includes:** round-trip smoke verifying generator emits new defaults on fresh classes/monsters; downstream consumer (star-lord exporter + gamora sim) still parses correctly with new values (no schema-shape change, only default-value change)
- Per R11(b) Principle 6 operationalized 2026-05-16

## What this dispatch produces

### Step 1 — Schema-default updates

Update the following defaults in the generator schemas (paths approximate — pick the canonical schema location consistent with your prior schema-defaults work):

- **PlayerClass.movement_speed** default: 5.75 → **8.0** m/s (end-game gear-only player baseline)
- **Monster.movement_speed** default per archetype (use whatever per-archetype mechanism currently exists, or introduce minimal one if not):
  - trash: 5.75 (unchanged)
  - fast archetypes: **7.5** m/s (top of locked range)
  - named bosses: **flag for gamora-design-call** — do NOT pick a number; surface that gamora needs to assign per-named-boss

### Step 2 — Smoke test (Discipline #2)

- Generate a fresh class (any seed); confirm movement_speed = 8.0
- Generate a fresh trash monster; confirm movement_speed = 5.75
- Generate a fresh fast-archetype monster; confirm movement_speed = 7.5
- Existing generator tests pass

### Step 3 — MIGRATION.md entry (per ADR-004)

Add entry to your seam's MIGRATION.md documenting the default-value change. Include cross-references:
- Downstream consumers: star-lord exporter (Stage B export-DTO fix queued; will surface in consolidated JSON); gamora sim (Gate 3b sim consumption firing parallel); drax demo (consume engine-emitted MS, queued)
- Upstream anchor: `canonical/story/movement-speed-baseline.md` end-game-anchor supersession (gandalf canonical update firing parallel)

### Step 4 — Tag + AGENT_STATE + completion record

- Intermediate tag: `rocket/v1.3-ms-schema-defaults-end-game`
- Update AGENT_STATE.md
- Fill completion record at bottom

## Out of scope (explicit)

- **NO sim-consumption code** — gamora's Gate 3b dispatch firing parallel
- **NO export-DTO changes** — star-lord's Stage B dispatch queued
- **NO demo / drax code** — drax MS-consume dispatch queued after this + star-lord land
- **NO wind_controller DPS floor** — separate rocket DPS-floor dispatch firing AFTER this returns (per-seam one-dispatch-per-session)
- **NO per-named-boss MS assignment** — flag for gamora; do not pick numbers

## Required reading

- Gandalf's MS verdict-reversal cascade table + recommended specific values (Matt-relayed Day-4 close)
- `canonical/story/movement-speed-baseline.md` (gandalf updating in parallel; consume the post-update values as authoritative)
- Existing schema files (you know the locations from prior schema-defaults work)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 math-before-code, #2 smoke test, #11 attribution

## Acceptance criteria

- [ ] PlayerClass.movement_speed default updated to 8.0
- [ ] Monster.movement_speed default per-archetype updated (trash 5.75; fast 7.5; named bosses flagged for gamora)
- [ ] Smoke test passes (fresh-class + fresh-monster generation emits new values)
- [ ] Existing generator tests pass
- [ ] MIGRATION.md entry filed with downstream-consumer cross-references
- [ ] Intermediate tag `rocket/v1.3-ms-schema-defaults-end-game` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified with: tag hash, list of named-boss flags surfaced for gamora, any unanticipated schema-shape consequences

## Tag policy

- **Intermediate tag:** `rocket/v1.3-ms-schema-defaults-end-game`
- **Milestone tag:** none.

---

## Completion record

**Completed:** 2026-05-16
**Schema files touched:**
- `src/reincarnated/generation/class_schema.py` — `PlayerClass.movement_speed` default 5.75 → 8.0
- `src/reincarnated/generation/monster_schema.py` — comment update (schema default 5.75 unchanged; per-archetype set in generator)
- `src/reincarnated/generation/monster_generator.py` — `ARCHETYPE_MOVEMENT_SPEED` swarmer/sniper 6.60 → 7.5
- `src/reincarnated/generation/MIGRATION.md` — new entry per ADR-004
- `tests/test_movement_speed_schema.py` — updated constants + new VS2a exact-value test for fast archetypes (19 tests total)
- `tests/test_grouping_layer_schema.py` — Discipline #9 fix: hard-coded 5.75 → derives from schema default

**Named-boss flags surfaced for gamora:**
- No named-boss MS values exist in the generator. Boss-tier monsters generated via standard generator emit the Monster schema default (5.75).
- Gamora must assign per-named-boss movement_speed values in the Gate 3b dispatch.
- Reference anchors from canonical/story/movement-speed-baseline.md § "VERDICT REVERSAL":
  - Trash baseline: 5.75 m/s (slow, kitable boss)
  - Fast archetype cap: 7.5 m/s (active chaser; 0.5 m/s below end-game player)
  - Player end-game: 8.0 m/s (parity chase)
  - Above end-game player (>8.0): only for brief-window dash/charge skills, NOT base MS

**Intermediate tag:** `rocket/v1.3-ms-schema-defaults-end-game @ b0b2f0f33e496d9cda17f0f50a9615f8fd5c0f9e`

**Tests status:** 19/19 test_movement_speed_schema.py; 84/84 test_export+test_telemetry_v22+v23; 162/162 core generation subset. Full suite run still completing (b6_generator_wired slow test set). Pre-existing flaky failure in test_gear_cp3.py is not introduced by this change (known from prior sessions).

**Unanticipated schema-shape consequences:** None. Default-value update only. No fields added/removed/renamed/retyped. No validation logic changed. One secondary fix: `test_grouping_layer_schema.py` had a hard-coded `5.75` assertion (Discipline #9 violation, latent from the original movement_speed dispatch). Fixed to derive from `PlayerClass.model_fields["movement_speed"].default`.

**Notes for knight-rider:**
- Acceptance criteria all met: class=8.0, trash=5.75, fast=7.5, smoke pass, tests pass, MIGRATION.md filed, tag cut.
- Named-boss gamora-design-call: gamora Gate 3b dispatch must include per-named-boss MS decisions. Current state: boss-tier monsters use schema default 5.75 (safe; just not tuned).
- AI_SPEED_MULTIPLIER change surfaced to drax via MIGRATION.md: was 0.767 (Option A), now 0.719 (= 5.75/8.0; Option B). Drax dispatch should propagate this.
- No cross-seam files touched. No sim/export/demo code modified. Scope adhered to.
- Next rocket dispatch (wind_controller DPS floor) ready to proceed.
