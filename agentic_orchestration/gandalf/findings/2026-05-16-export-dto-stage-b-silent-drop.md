# Finding — Export-pipeline Stage B silent-drop (Pattern P7 #3 in one day)

**Status:** Gandalf-filed empirical finding; Drift-12 / Pattern P7 classification.
**Authored:** 2026-05-16 (Day 4 close) by gandalf in response to Matt's verification question on movement-speed JSON-packet wiring.
**Severity:** 🔴 Mid-impact, time-critical — silently drops 10+ engine-schema fields at the demo-facing export boundary; blocks VS2b loadout embodiment-narrative display end-to-end; will block B6 skill-tree UI; partially camouflaged in VS2a only because drax has hardcoded matching values.

**Companion classifications:**
- Drift-12 (paths-audit P6 instance — engine emits field, downstream consumer doesn't receive it)
- Pattern P7 (silent-drop) #3 in 2026-05-16; sibling to (1) recorder.py `loadout_json: None` silent drop (fixed by gamora V2.1); (2) `_class_to_dict` form-bias-fields silent drop (fixed by commit `4bbc906`)
- Discipline #13a candidate (implementation-vs-intent drift — Stage 1 form-bias work claimed completion; never reached the surface it was supposed to reach)
- Discipline #11 attribution gap (no cross-seam round-trip validation)

---

## Empirical evidence

Ran on freshest regen (`season_001010` generated 22:41 tonight — after every wiring fix shipped today including form-bias Stage 1+2 wiring at commit `4bbc906` 20:16):

| Field | Engine schema | season_001010/classes.json | season_001010/monsters.json |
|---|---|---|---|
| `movement_speed` | ✅ present on PlayerClass + Monster (rocket `62624dd`) | ❌ 0 occurrences | ❌ 0 occurrences |
| `embodiment_tag` | ✅ present on PlayerClass (rocket Stage 1 `73db17f`) | ❌ 0 occurrences | n/a |
| `embodiment_anatomy_tags` | ✅ present | ❌ 0 occurrences | n/a |
| `embodiment_action_register` | ✅ present | ❌ 0 occurrences | n/a |
| `class_role_function` | ✅ present | ❌ 0 occurrences | n/a |
| `gear_slot_labels` | ✅ present | ❌ 0 occurrences | n/a |
| `grouping_pair_structure` | ✅ present on PlayerClass (rocket Stage 2 `03fb8cb`) | ❌ 0 occurrences | n/a |
| `grouping_season_id` | ✅ present | ❌ 0 occurrences | n/a |
| `grouping_layer_version` | ✅ present | ❌ 0 occurrences | n/a |
| `convergence_report` | ✅ present (Stage A1 `1aa99b5`) | ❌ 0 occurrences | n/a |

Demo-facing `classes.json` carries 15 fields: `id`, `name`, `title_completion`, `flavor_text`, `archetype_tag`, `energy_type`, `role_orientation`, `range_profile`, `dominant_element`, `is_act_boss`, `color_palette`, `stat_distribution`, `skills`, `carried_gear`, `balance_metadata`. **None of the 10+ schema fields added since Stage A1 forward-compat reach this file.**

---

## Root cause — two-stage export pipeline with cherry-pick DTO at Stage B

### Stage A — `src/reincarnated/output/season_writer.py`

Writes per-class intermediate JSON files at `season_dir/classes/<class_id>.json`. Uses `_class_to_dict()` (lines 253-289) which DOES include `movement_speed` (line 282) plus all form-bias Stage 1+2 fields (today's commit `4bbc906` fix).

Stage A also has an export-boundary validator (`_REQUIRED_CLASS_KEYS` frozenset at lines 322-333) that raises on missing fields. ✅ Correct discipline at Stage A.

### Stage B — `src/reincarnated/export/season_exporter.py`

Reads the Stage-A intermediate files, then **re-instantiates via the `ExportClass(...)` pydantic DTO** at lines 581-599 with **explicit per-field `class_json.get("field_name", default)` calls**, then writes the consolidated demo-facing `classes.json` via `[c.model_dump() for c in export_classes]` at line 630.

The `ExportClass(...)` constructor at lines 581-599 pulls 16 named fields explicitly. **It does NOT pull `movement_speed`, `embodiment_tag`, `embodiment_anatomy_tags`, `embodiment_action_register`, `class_role_function`, `gear_slot_labels`, `grouping_pair_structure`, `grouping_season_id`, `grouping_layer_version`, or `convergence_report`.**

Stage B has NO export-boundary validator analogous to Stage A's `_REQUIRED_CLASS_KEYS`. Fields silently drop without raising.

### For monsters: gap at Stage A too

`_monster_to_dict()` at `season_writer.py:292-314` doesn't include `movement_speed`. Gap is at Stage A for monsters (not just Stage B). When fixed at Stage A, the same Stage B cherry-pick problem applies via whatever `ExportMonster(...)` equivalent exists.

---

## Scope of impact

### 🔴 Blocks demo consuming engine-emitted `movement_speed`

Drax's `world/movement.ts` currently has hardcoded values matching gandalf-locked spec (5.75 / 6.0 / 7.5 / 8.0 / AI_SPEED_MULTIPLIER 0.767). Working in VS2a only because **drax hardcoded the right numbers**. Engine-to-demo data flow for `movement_speed` is broken; if values change in engine, demo won't pick up; drax must hand-update.

### 🔴 Blocks VS2b loadout embodiment-narrative display

Per spec authored today at `canonical/story/embodiment-display-loadout.md`, the loadout-side surface requires `embodiment_tag` + (new) `embodiment_narrative_beat` + `spirit_name` reaching the loadout app via this same `classes.json`. If `embodiment_tag` is dropped at Stage B, the entire VS2b display surface cannot consume engine emission. **VS2b ship is direct-blocked by this finding** if not fixed.

### 🔴 Will block B6 skill-tree UI

Per spec authored today at `canonical/story/b6-skill-tree-ui-scoping.md` § 10, drax consumes per-skill `tier`, `chain_id`, `chain_position`, `parent_skill_ids`, `scaling_coefficient`. These ride on the Skill schema; the Stage B pipeline likely has an analogous `ExportSkill(...)` DTO with the same cherry-pick pattern. **When B6 main ships and emits real tier data, it will silently drop at the same boundary** unless fixed first.

### 🟡 Spirit Guide / build-coach (Stage A7) cascade

`convergence_report` (B14 multi-band optimal-distribution data) silently drops too. Stage A7 Spirit Guide build-coach reads this to compute Strong/Solid/Marginal/Sidegrade/Downgrade verdicts. Pre-blocks Stage A7's UI surface.

### 🟡 Cross-seam attribution audit

Gamora Gate 3b sim consumption reads `Monster.movement_speed` directly from engine internals — does NOT consume the export packet — so sim work is not blocked by this finding. But cross-validation against the export packet (a Discipline #11 attribution check) would surface this gap, and currently doesn't because no such check exists.

---

## What would have caught this earlier — R11(b) discipline

Per star-lord AGENT_STATE.md line 625 (filed today):
> *"Both [P7 instances] would have been caught earlier by R11(b) cross-seam round-trip discipline (run field X through generation → export → validate at consumer boundary). R11(b) dispatch authoring is a knight-rider decision, not star-lord's autonomous scope. Flagging here as carry-forward for knight-rider review."*

This finding is the third P7 instance in one day. It strengthens the case for R11(b) considerably.

---

## What this finding does NOT do

- Does NOT propose the fix (recommended commission scope; star-lord seam)
- Does NOT propose the test (recommended in companion commission)
- Does NOT propose the decisions-log entry (recommended; knight-rider drafts)
- Does NOT autonomously trigger any work (per CHANGELOG 2026-05-16 — flagged items route through knight-rider; gandalf surfaces, does not pick up)

---

## Recommended next actions

For knight-rider:
1. Author star-lord dispatch (commission filed in parallel at `agentic_orchestration/gandalf/requests/2026-05-16-star-lord-export-dto-stage-b-fix-and-r11b.md`) to extend `ExportClass(...)`, `ExportMonster(...)`, `ExportSkill(...)` DTOs + add Stage B export-boundary validator
2. Author rocket dispatch (small) to add `movement_speed` to `_monster_to_dict` in `season_writer.py:292-314`
3. Author R11(b) cross-seam round-trip discipline dispatch (star-lord flagged today; this finding strengthens case)
4. Draft decisions-log entry locking "Stage-B export-boundary validation required at every engine-schema field addition" — possibly amends Discipline #14 with Stage-B clause

For gandalf (self):
- This finding files; surfaces to knight-rider; awaits commission authoring + Matt approval
- Re-verify post-fix by re-running grep on next regen — confirm all 10+ fields reach `classes.json`
- Update `b6-skill-tree-ui-scoping.md` § 10 and `embodiment-display-loadout.md` § 10 with note that Stage B validator must include the spec's required fields (forward-compat protection)

For Matt:
- Approve commission cascade (Stage B DTO fix + monster_to_dict gap + R11(b) discipline + decisions-log entry)
- Or push back on any item — finding scope is mine; remediation is knight-rider's; Matt approves both

---

— gandalf, 2026-05-16 (Day 4 close)
