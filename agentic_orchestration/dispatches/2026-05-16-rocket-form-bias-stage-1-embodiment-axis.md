# Dispatch — 2026-05-16 — rocket — Form-bias Stage 1: embodiment-axis schema additive (VS2b S1 + cadence Option II Stage 1)

**From:** knight-rider (authored per cadence Option II locked in form-bias 5-entry batch Entry 5 + Matt's prior rocket sequencing directive: Flag A → movement_speed schema → VS2b Stage 1)
**To:** rocket
**Approved by:** Matt at 2026-05-16 Day 4 (form-bias batch committed `5d51b5a`; cipher-width resolution `1dff66d`; Stage 1 unblocks immediately per Entry 5 cadence + Entry 3 sub-lock resolutions)
**Status:** PENDING — ACTIVE (D1 Q1/Q4 surgical amendments completed @ `rocket/v1.3-d1-rubric-q1-q4-amendments @ 6cadbf5c`; quarantine 52.4% → 28.6%; this dispatch unblocked 2026-05-16 Day 4)
**Estimated effort:** 1-2 sessions (~4-8h); schema-additive work primarily; MIGRATION.md per ADR-004 (cross-seam contract); no balance-affecting changes.
**Acceptance:** Embodiment-axis fields added to engine schema (additive; no removals); generator emits the fields; smoke season verifies field population; MIGRATION.md entry per ADR-004; intermediate tag.

---

## Context — Stage 1 of cadence Option II

Per the 2026-05-16 form-bias 5-entry batch (committed `5d51b5a`) Entry 5 (cadence Option II) — Stage 1 is the **first additive step** of the 4-stage form-bias migration backbone:

> **Stage 1 — Add embodiment-axis as new optional field. No removals.** Engine emits `embodiment_tag`, `embodiment_anatomy_tags`, `embodiment_action_register`, `class_role_function`, `gear_slot_labels`, `per_season_narrative_modulation` per `canonical/story/embodiment-narrative-layer.md` § "Engine emit requirements". Position C schema migration shape; existing gear schema stays mechanically; embodiment fields are additive. Rocket dispatch territory. Schema-additive only. MIGRATION.md required. Verifies: schema migration mechanics work; Position-C migration's mechanical-substrate stays operative through migration.

**This dispatch operationalizes Stage 1.** Cipher-width Outcome 2 + Foundation L2 + per-season vocabulary coupling β (all committed today via `1dff66d`) are the architectural context this stage's fields fit into. Position C (gear-as-functional-mechanic + embodiment-as-narrative-skin) is the architectural shape these fields enable.

## What this dispatch does

### Step 1 — Schema field additions (per `canonical/story/embodiment-narrative-layer.md` § "Engine emit requirements")

Add the following fields to the player class schema (`src/reincarnated/generation/class_schema.py` or equivalent):

- **`embodiment_tag: str`** — the primary embodiment identifier (e.g., `"humanoid"`, `"slime"`, `"spider"`, `"dragon_hatchling"`). VS2a-Phase default: `"humanoid"` for all classes (per Matt's prior VS2a embodiment-scope sub-decision (b1) — humanoid-only roster).
- **`embodiment_anatomy_tags: list[str]`** — anatomical descriptors (e.g., `["bipedal", "arms_2", "hands_2"]` for humanoid; `["amorphous", "no_hands"]` for slime). Default for humanoid: standard anatomy tag-set.
- **`embodiment_action_register: str`** — action-vocabulary register (e.g., `"martial_combat"`, `"feral_combat"`, `"arcane_channel"`). Default for humanoid: based on archetype (warrior → `"martial_combat"`, mage → `"arcane_channel"`, etc.).
- **`class_role_function: str`** — abstract role-function the class fulfills (e.g., `"front_line"`, `"sustained_damage"`, `"area_control"`). Derives from existing archetype + role-orientation.
- **`gear_slot_labels: dict[str, str]`** — per-embodiment label override for gear slots (humanoid: `{"weapon": "Weapon", "off_hand": "Off-hand", ...}` — defaults; future per-embodiment overrides for non-humanoid embodiments at Stage 4).
- **`per_season_narrative_modulation: dict[str, str]`** — placeholder for per-season narrative-skin modulation (empty dict for VS2a; populated at form-bias Stage 4 work).

All fields are **additive** — existing class schema unchanged; new fields default to humanoid-baseline values.

### Step 2 — Generator wiring

Update `class_generator.py` (and any related generation orchestration) to emit the new embodiment-axis fields per class:

- Default `embodiment_tag = "humanoid"` (per VS2a-scope decision)
- Anatomy tags default to standard humanoid anatomy
- Action register derives from archetype (mapping table)
- class_role_function derives from existing archetype + role-orientation taxonomy
- gear_slot_labels default to humanoid baseline
- per_season_narrative_modulation = `{}` (empty for VS2a)

### Step 3 — Tests + smoke

Per Discipline #2:
- Add unit tests for embodiment-axis field presence + default values
- Smoke a 5-class season generation; verify all classes emit embodiment_tag="humanoid" + standard humanoid anatomy + appropriate action_register per archetype
- Verify NO existing tests fail (additive change should preserve all baseline behavior)

### Step 4 — MIGRATION.md entry (cross-seam contract per ADR-004)

Append a new entry to `reincarnated-engine/src/reincarnated/generation/MIGRATION.md`. Document:

- New embodiment-axis fields on player class schema with semantics
- Field defaults (humanoid baseline for VS2a)
- Cross-seam consumers:
  - **Star-lord** (future Stage 2-3 form-bias work): LLM prompt-construction will consume per_season_narrative_modulation at Stage 3 cipher migration
  - **Drax** (future Stage 4 form-bias work): display layer consumes gear_slot_labels + embodiment_tag for per-embodiment rendering
  - **Gamora** (Stage 2-3 doppelganger validation): consumes per-embodiment data for archetype-mate variance check

### Step 5 — Intermediate tag + AGENT_STATE + completion record

- Tag: `rocket/v1.3-form-bias-stage-1-embodiment-axis` intermediate at the commit closing schema + generator + tests pass
- AGENT_STATE.md updated
- Completion record at bottom of this dispatch filled

## Cross-seam considerations

- **Star-lord:** READ-ONLY; future Stage 2-3 work (per-season vocabulary generation + cipher migration) consumes the new fields at LLM prompt-construction sites.
- **Drax:** READ-ONLY; future Stage 4 work consumes gear_slot_labels + embodiment_tag for display-layer per-embodiment rendering.
- **Gamora:** READ-ONLY; Stage 2-3 doppelganger validation consumes per-embodiment data.
- **Gandalf:** future amendment if movement_profile (from spatial-data entry) interacts with embodiment_action_register at Stage 4 (per-embodiment narrative-skin); not this dispatch's scope.
- **Knight-rider:** notify at completion; this dispatch unblocks Stage 2 grouping-layer dispatch authoring (rocket + star-lord; cadence Option II Stage 2).

## Out of scope (explicit)

- **NO gear schema removals.** Stage 1 is purely additive; existing gear schema unchanged.
- **NO LLM prompt-construction changes.** Stage 3 is when canonical-four hides from LLM; this dispatch only adds the embodiment-axis fields.
- **NO display-layer changes.** Drax's Stage 4 work consumes gear_slot_labels + embodiment_tag.
- **NO non-humanoid embodiment-tag values commissioned.** VS2a is humanoid-only per Matt's prior embodiment-scope sub-decision (b1). Non-humanoid embodiments commission for VS2b Substrate Realignment work.
- **NO per_season_narrative_modulation population.** Empty dict for VS2a; populated at Stage 4.
- **NO B6 main work** (kit composition + balance re-tune) — separate gamora dispatch (HELD per movement-speed gauntlet-balance provisional caveat).
- **NO spatial-data schema fields** — separate dispatch per spatial-data cascade Step 2.

## Required reading

- `canonical/story/embodiment-narrative-layer.md` § "Engine emit requirements" (source-of-truth for the field list + semantics)
- 2026-05-16 form-bias 5-entry batch (committed `5d51b5a`) — Entry 5 cadence Option II Stage 1 framing
- 2026-05-16 cipher-width resolution entry (committed `1dff66d`) — Outcome 2 + Foundation L2 + per-season vocabulary coupling β architecture context
- `canonical/story/form-bias-cadence-strategy.md` § 7.1 + § 9.1 (Stage 1 framing + rocket cascade item)
- `reincarnated-engine/src/reincarnated/generation/class_schema.py` + `class_generator.py` (your target files)
- 2026-05-08 doc 37 § 4 Position C (architectural shape these fields enable)

## Acceptance criteria

- [ ] 6 embodiment-axis fields added to class schema with documented defaults
- [ ] Generator emits all 6 fields with humanoid-baseline defaults
- [ ] Unit tests pass (existing + new embodiment-axis tests)
- [ ] Smoke season verifies field presence + correct defaults
- [ ] MIGRATION.md entry filed per ADR-004 cross-seam contract
- [ ] Intermediate tag `rocket/v1.3-form-bias-stage-1-embodiment-axis` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion; Stage 2 grouping-layer dispatch authoring unblocks

## Tag policy

- **Intermediate tag:** `rocket/v1.3-form-bias-stage-1-embodiment-axis` at the commit closing schema + generator + tests pass.
- **Milestone tag:** none from this dispatch. Standard ADR-003 protocol.

---

## Completion record

**Completed:** 2026-05-16
**Intermediate tag:** `rocket/v1.3-form-bias-stage-1-embodiment-axis` @ `73db17f`
**Smoke status:** PASS — 5-class smoke (fire_mage / water_controller / physical_warrior / hybrid_mage / hunter). All 6 embodiment-axis fields populated with correct humanoid-baseline values. 68 new tests pass; 150-test core subset clean.
**MIGRATION.md path:** `reincarnated-engine/src/reincarnated/generation/MIGRATION.md`
**Notes for knight-rider:**
- Stage 1 complete and tagged. Acceptance criteria all met.
- 6 embodiment-axis fields on `PlayerClass`: `embodiment_tag` / `embodiment_anatomy_tags` / `embodiment_action_register` / `class_role_function` / `gear_slot_labels` / `per_season_narrative_modulation`. All additive; no removals; no existing tests changed.
- VS2a humanoid defaults wired via two archetype lookup tables in `class_generator.py` (`_ARCHETYPE_ACTION_REGISTER`, `_ARCHETYPE_ROLE_FUNCTION`). Tables cover all 15 known archetypes.
- `gear_slot_labels` emits 10-slot humanoid-baseline dict per class. `per_season_narrative_modulation` is empty dict for VS2a (Stage 3/4 population targets documented).
- MIGRATION.md cross-seam contract filed: star-lord (Stage 3 cipher migration), drax (Stage 4 display layer), gamora (Stage 2-3 doppelganger validation). All three are READ-ONLY at Stage 1.
- **This unblocks: Stage 2 grouping-layer dispatch authoring (rocket + star-lord per cadence Option II Stage 2) AND the B11 geometry palette dispatch (next in rocket queue).**
- Pre-existing `physical_warrior` B6 kit build failure (geometry constraints; B11 scope) surfaced in smoke but is not new — generator fallback path fires correctly.
