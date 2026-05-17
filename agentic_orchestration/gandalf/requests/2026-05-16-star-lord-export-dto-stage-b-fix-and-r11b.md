# Gandalf request to knight-rider — star-lord export-DTO Stage B fix + R11(b) cross-seam round-trip discipline

**From:** gandalf
**To:** knight-rider (for star-lord + rocket dispatch authoring)
**Date:** 2026-05-16 (Day 4 close)
**Authorized by:** Matt at 2026-05-16 Day 4 ("yes file the finding and dispatch commission")
**Type:** Multi-track remediation commission — corrects Pattern P7 #3 silent-drop + locks Discipline-level prevention
**Estimated effort:** Star-lord 3-5 sessions (~8-15h); rocket 1 session (~1-2h, parallelizable); knight-rider decisions-log entry + R11(b) discipline drafting

**Source finding:** `agentic_orchestration/gandalf/findings/2026-05-16-export-dto-stage-b-silent-drop.md`

---

## Why this commission exists

Gandalf finding filed today documents the third Pattern P7 (silent-drop) instance in one day: 10+ engine-schema fields silently drop at the Stage B export-DTO boundary (`ExportClass(...)` constructor in `season_exporter.py:581-599`) and never reach the demo-facing `classes.json`. Empirically verified on `season_001010` (regenerated 22:41 tonight, post-every-wiring-fix).

This blocks:
- Demo consuming engine-emitted `movement_speed` (drax hardcoded matching values; data flow is broken in fact)
- VS2b loadout embodiment-narrative display end-to-end (spec authored today; cannot consume engine emission)
- B6 skill-tree UI (when ships) consuming `tier`/`chain_id`/`chain_position` (spec authored today; same boundary will silently drop)
- Stage A7 Spirit Guide build-coach consuming `convergence_report` (Stage A1 forward-compat field; same drop)

Three parallel tracks needed:

---

## Track A — Star-lord: extend Stage B DTOs + add Stage B export-boundary validator

**Estimated:** 2-3 sessions (~6-10h)
**Owner:** star-lord (seam: `src/reincarnated/export/`)
**Pre-conditions:** Star-lord's current queue depth (Stage 2 cosmological vocab → V2.4 telemetry → V2 regen → Stage 3 cipher migration); this Track A is HIGH priority because it precondition-blocks Stage 3 cipher migration completion validation. **Recommend re-prioritizing in star-lord queue.**

### Scope

1. **Extend `ExportClass(...)` constructor** in `season_exporter.py:581-599` to pull every field present in the Stage-A intermediate JSON. Use a model-driven or wildcard approach (NOT per-field cherry-pick) so future engine-side additions don't recur this pattern. Specifically must include:
   - `movement_speed`
   - `embodiment_tag`, `embodiment_anatomy_tags`, `embodiment_action_register`
   - `class_role_function`, `gear_slot_labels`
   - `grouping_pair_structure`, `grouping_season_id`, `grouping_layer_version`
   - `convergence_report`

2. **Extend `ExportMonster(...)` constructor** to pull `movement_speed` (depends on Track B landing `_monster_to_dict` first; sequential coordination with rocket dispatch)

3. **Extend `ExportSkill(...)` constructor** to pull all Stage A1 forward-compat schema fields: `tier`, `chain_id`, `chain_position`, `parent_skill_ids`, `scaling_coefficient`, `cast_time`, `damage_resolution_time`, `i_frame_window`, `set_id`, `set_position`, `set_piece_count_required` — these are populated as defaults today but will be load-bearing as B6/B13/B15 ship

4. **Add Stage B export-boundary validator** analogous to Stage A's `_REQUIRED_CLASS_KEYS` in `season_writer.py:322-333`. Place in `season_exporter.py` AFTER the `[c.model_dump() for c in export_classes]` call. Validates the consolidated `classes.json` payload contains every field from the intermediate JSON. Raises on drift with explicit field-name attribution per Discipline #11.

5. **Smoke-test:** regen a fresh season, run grep on consolidated `classes.json` and `monsters.json`, verify all 10+ fields present with non-null values. Validator must catch any silent drop introduced by future schema additions.

6. **MIGRATION.md entry** documenting Stage-B-validator + DTO model-driven pattern.

7. **Intermediate tag:** `star-lord/v1.x-stage-b-export-dto-fix` per ADR-003.

### Discipline checks

- **Discipline #2 (smoke-test):** verify all fields present in consolidated export
- **Discipline #11 (attribution):** validator raises with explicit field name + entity id + stage attribution
- **Discipline #12 (semantic shift):** export-DTO model becomes the contract for engine-to-demo data; any future field addition must update both Stage A and Stage B
- **Discipline #14 (internal-vs-generative schema separation):** Stage B output IS the generative-side schema; consumers (drax loadout, demo) bind to this; validator enforces the boundary

### What this dispatch does NOT do

- Does NOT add new schema fields (only wires existing fields through Stage B)
- Does NOT remove fields (additive only; ADR-004 boundary)
- Does NOT touch `simulation/`, `generation/`, or `output/season_writer.py` Stage A — those are correct
- Does NOT author R11(b) discipline doc (separate Track C)

---

## Track B — Rocket: `_monster_to_dict` gap fix

**Estimated:** 1 session (~1-2h)
**Owner:** rocket (seam: `src/reincarnated/output/season_writer.py` for `_monster_to_dict`)
**Parallelizable with Track A** — independent gap; can ship in any order; Track A's `ExportMonster` extension depends on Track B landing first OR coordinates on the same `movement_speed` field name.

### Scope

1. **Add `movement_speed` to `_monster_to_dict()`** at `season_writer.py:292-314`. Pulls from `monster.movement_speed` schema field (rocket shipped today `62624dd`).
2. **Update monster export-boundary validator** if one exists analogous to `_REQUIRED_CLASS_KEYS`; add the field to required set.
3. **Smoke:** regen a monster pool, verify `monsters.json` (intermediate per-monster file) contains `movement_speed` with non-null value.
4. **MIGRATION.md entry** per ADR-004 (small; one-line addendum).
5. **Intermediate tag:** `rocket/v1.x-monster-to-dict-movement-speed`.

### Cross-seam coordination

Star-lord Track A's `ExportMonster(...)` extension needs Track B's output to consume. Sequence:
- Track B ships first (1-2h)
- Track A's `ExportMonster(...)` extension lands with confidence the intermediate JSON has the field
- Smoke-tests validate end-to-end

---

## Track C — Knight-rider: R11(b) cross-seam round-trip discipline + decisions-log entry

**Estimated:** ~2-3h knight-rider authoring + jack-ryan Gate-1 review + Matt approval
**Owner:** knight-rider authoring; jack-ryan Gate-1; Matt approves

### Scope

1. **Draft R11(b) discipline** for `reincarnated-engine/design/working-agreement/engineering-disciplines.md`:
   - **Name:** R11(b) — Cross-seam round-trip validation
   - **Rule:** Every engine-side schema field addition MUST be validated end-to-end at the consumer boundary (engine emit → intermediate → consolidated export → demo / loadout consume) before claiming "wired through." Stage-A wiring alone is insufficient; Stage-B export-DTO must also surface the field.
   - **Concrete check:** for each new field, smoke-test regen + grep on consolidated export + assert non-null at the most downstream consumer.
   - **Empirical basis:** Pattern P7 instances 2026-05-16 (#1 recorder.py `loadout_json`; #2 `_class_to_dict` form-bias; #3 Stage B DTO silent-drop — this finding).

2. **Decisions-log entry** locking the Stage-B-validation discipline + naming the three P7 instances as empirical basis. Possibly amends Discipline #14 (internal-vs-generative schema separation) with a Stage-B-validation clause specifying that the generative-side schema IS the Stage-B consolidated export, not the Stage-A intermediate.

3. **Jack-ryan Gate-1** on the discipline draft + decisions-log entry per CHANGELOG 2026-05-16 dispatch rubric (strategy doc that will produce decisions-log entries; INVOKE Gate 1).

### Cross-seam coordination

- Discipline lands BEFORE or CONCURRENT with Track A star-lord work — Track A's validator implementation is the operational expression of R11(b)'s rule
- Decisions-log entry references both Track A's validator commit + Track B's monster gap fix as the implementation

---

## Acceptance criteria (combined commission)

- [ ] Track A: `ExportClass(...)` + `ExportMonster(...)` + `ExportSkill(...)` extended; Stage B validator added; smoke verifies all 10+ fields reach consolidated `classes.json` + `monsters.json` with non-null values; MIGRATION.md entry filed; intermediate tag cut
- [ ] Track B: `_monster_to_dict` includes `movement_speed`; smoke verifies; MIGRATION.md entry; intermediate tag cut
- [ ] Track C: R11(b) discipline drafted; jack-ryan Gate-1 PASSED; Matt-approved; lands in `engineering-disciplines.md`; decisions-log entry committed
- [ ] Re-verify finding: gandalf reruns `grep -c "movement_speed" exports/<fresh-season>/classes.json` → ≥10 occurrences (one per class); same for `embodiment_tag`, `grouping_pair_structure`, `convergence_report`
- [ ] Knight-rider notifies gandalf at completion; gandalf updates `b6-skill-tree-ui-scoping.md` + `embodiment-display-loadout.md` with Stage-B-validator-honored note (forward-compat protection)

---

## What this commission unblocks

- **VS2b loadout embodiment-narrative display** — drax can consume engine-emitted `embodiment_tag` + `embodiment_narrative_beat` once it ships
- **Demo consuming engine-emitted `movement_speed`** — drax's `world/movement.ts` can replace hardcoded values with engine reads (eventually; this isn't an immediate refactor — drax decides timing)
- **B6 skill-tree UI consuming tier/chain data** — when B6 main ships and emits real tier/chain values, they reach the demo without re-running this finding's loop
- **Stage A7 Spirit Guide build-coach consuming `convergence_report`** — pre-cleared
- **R11(b) discipline operationalized** — future schema additions caught at the boundary, not in playtest

---

## Sequencing recommendation

**Both Track A and Track B run in parallel.** Track C (discipline doc) can run in parallel with both, lands when both ship.

**Priority:** HIGH. Sequence ahead of star-lord's current queue (Stage 2 cosmological vocab → V2.4 → V2 regen → Stage 3 cipher migration). Track A's Stage-B validator is also a precondition for Stage 3 cipher migration validation — Stage 3 hides canonical-four from LLM and adds `seasonal_element` + `seasonal_dominant_element` fields; if Stage B silently drops these, the cipher migration ships broken.

**Recommended re-sequence for star-lord queue:**
1. THIS Track A (Stage B export-DTO fix + validator) — 6-10h
2. Then Stage 2 cosmological vocab (existing dispatch; HOLD-on-prior)
3. Then V2.4 telemetry (existing dispatch)
4. Then V2 regen (existing dispatch)
5. Then Stage 3 cipher migration (existing dispatch) — validates correctly because Stage B validator catches any new silent drop

Track A is a precondition for Stage 3 ship correctness, not just a fix-as-you-go item.

---

— gandalf, 2026-05-16 (Day 4 close)
