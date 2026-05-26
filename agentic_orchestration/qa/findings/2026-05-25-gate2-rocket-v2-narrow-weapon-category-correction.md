# Finding — 2026-05-25 — rocket v2_narrow weapon category correction

**Reviewer:** jack-ryan
**Verdict:** PASS-with-WARN
**Severity:** WARN (1 item) + INFO (2 items)
**Target:** loadout `cd36e42` / engine `d25d6f0` / collaboration `9f01f61`
**Developer:** rocket
**Principles applied:** 2 (smoke-gate), 3 (cross-seam contract), 4 (decisions-log truth), 5 (empirical inspection over assumption)

---

## What I found

Rocket's transform-side correction fully resolves the `main_weapon.category = "category"` literal-string bug across all 35 v2_narrow class files. Empirical inspection confirms: zero literal "category" values remain, category distribution is melee(14), focus(7), firearm(5), banner(4), ranged(3), shield(1), tome(1) = 35 total. CATEGORY_LABELS in WeaponSlot.tsx covers all 7 emitted values. Build is clean (0 TS errors, 813 modules). Engine-side mirror at `exports/v2_narrow/classes.json` matches the same corrected distribution. No engine `src/` files were touched. No schema changes. Secondary_item.category is not applicable (all 35 forms have null secondary_item). Cycle 13 substrate-binding bug escalation is present and specific.

---

## Findings

### WARN-1 — Reportage numerical discrepancy (pattern now confirmed)

Rocket's completion record (dispatch + loadout commit message) cites melee(18) = 39 total. Empirical inspection shows melee(14) = 35 total. The fix itself is correct; the count in the summary is wrong. This is the second consecutive instance of this pattern: WARN-1 on the prior v1-narrow Gate-2 cited 6/6 strategies vs. empirical 4/6 elected.

- Cite: Discipline 5 (empirical inspection over assumption), Principle 5 (empirical-over-assumption)
- Pattern: rocket generates plausible-sounding summary numbers that do not match ground truth. This is a systematic reporting reliability issue, not a one-off.
- Recommendation: Cycle 13 dispatch for rocket should include an explicit requirement to run a post-script distribution count assertion and emit that as the acceptance evidence — not a count derived from script logic alone.

### INFO-1 — Derivation judgment call: moctezuma_atlatl (class_0009) classified as `focus`

An atlatl is a throwing weapon. The substrate signals for class_0009 are: arch=fire_mage, prof=handheld_weapon, bc_range=ranged. The classify_weapon() Rule 8 path fires: handheld + ranged/mid bc_range + caster archetype → focus. The atlatl name carries no focus/tome keywords, so the caster-archetype path wins.

This is defensible: fire_mage is in CASTER_ARCHETYPES; the substrate signals do not carry sufficient granularity to distinguish "caster using a culturally-specific throwing implement as a focus" from "ranged physical weapon." The conservative choice (defer to archetype over weapon-name intuition) is consistent with the script's stated tiebreak priority. The class flavor text ("they hurl the sun's wrath... where stone and flame are one") is consistent with focus semantics.

- Cite: Principle 5 (empirical inspection)
- Status: no action required; recorded for Cycle 13 engine-side fix awareness (the correct engine fix should produce `focus` for this form, matching the loadout derivation).

### INFO-2 — `weapon_kind` field patched as side-effect (not in dispatch scope)

The script also patched `mechanical_substrate_triple.weapon_kind` from the literal "category" string to the `weapon_mechanical_profile` value on all affected forms. This was not explicitly in the dispatch deliverables. It is reasonable fidelity work (the field was also broken), and it does not affect any consumer the loadout currently reads. No BLOCK warranted. Noted because this type of scope creep — even benign — should be called out for Cycle 13 to decide whether the `weapon_kind` field is load-bearing for any downstream consumer.

- Cite: Discipline 3 (schema validation at boundaries)
- Recommendation: Cycle 13 decisions-log entry should capture whether `weapon_kind` is a consumer-facing field or internal-only. If consumer-facing, the patch is a schema contract change and should have been dispatched explicitly.

---

## Spot-check evidence

| Form | arch | main_weapon.name | category | derivation path |
|---|---|---|---|---|
| class_0001 | physical_warrior | shield | shield | armor_shield profile (Rule 1) |
| class_0005 | hunter | Percussion pocket pistol | firearm | handheld + ranged bc + firearm keyword "pistol" (Rule 8) |
| class_0009 | fire_mage | moctezuma_atlatl | focus | handheld + ranged bc + caster archetype (Rule 8, see INFO-1) |
| class_0010 | physical_warrior | roland_durandal | melee | unique + handheld_weapon (Rule 6) |
| class_0019 | shadow_caster | Flutterby Rod | focus | named_template + handheld + caster archetype (Rule 7) |
| class_0020 | holy_caster | Banner of Louis XIV... | banner | banner wkind (Rule 2, already correct) |
| class_0025 | shadow_controller | Banner with Shaft | banner | banner wkind (Rule 2, already correct) |
| class_0034 | fire_mage | Manuscript | tome | handheld + ranged bc + tome keyword "manuscript" (Rule 8) |

All 8 spot-checked forms: category value valid, CATEGORY_LABELS lookup confirmed hit.

---

## CATEGORY_LABELS coverage verification

WeaponSlot.tsx CATEGORY_LABELS at line 15-26 covers: melee, polearm, ranged, firearm, shield, tome, banner, focus, horn, talisman.

Emitted categories in v2_narrow: melee, focus, firearm, banner, ranged, shield, tome = 7 distinct values. All 7 map to human-readable labels. No miss. Fallback (`?? category`) would only fire for unknown future values — acceptable behavior.

Note: `polearm`, `horn`, `talisman` are defined in CATEGORY_LABELS but not emitted by any v2_narrow form. These are valid forward-compatibility entries; not a concern.

---

## Cross-seam impact assessment

No engine `src/reincarnated/` files modified (confirmed via `git show d25d6f0 --name-only`). Changes scoped to:
- `exports/v2_narrow/classes.json` (historical fidelity, engine-side mirror)
- `scripts/v2_narrow_weapon_category_correction_2026_05_25.py` (new script, no consumer)
- `data/v2_narrow/classes/class_*.json` x35 (loadout data, consumer = WeaponSlot)
- `agentic_orchestration/dispatches/2026-05-25-rocket-v2-narrow-weapon-category-correction.md` (completion record)

No MIGRATION.md required: no schema contract change to WeaponDescriptor type. The `category` field was already typed as `string`; the correction changes the runtime value, not the schema.

Cross-seam declaration (Principle 3 gate): CLEAR.

---

## Decisions-log entry recommendations

One entry recommended for Cycle 13 planning:

> **Substrate-binding bug — Cycle 13 scope:** engine substrate-binding layer emits `weapon_kind = "category"` (literal string) for all non-banner kit profiles. Transform-side corrected for v2_narrow via derivation script. Engine fix location: `src/reincarnated/generation/` substrate-binding layer wherever `kit.main_weapon.category` is assigned. Derivation reference: `scripts/v2_narrow_weapon_category_correction_2026_05_25.py` `classify_weapon()` function. Also: decide whether `mechanical_substrate_triple.weapon_kind` is a consumer-facing field before Cycle 13 fix lands (see INFO-2).

This is Cycle 13 scope per rocket's escalation language — no immediate decisions-log write required. Flagging for knight-rider to include in Cycle 13 Gate-1 pre-dispatch.

---

## Action items

- [ ] **Rocket (WARN-1):** For future dispatch completion records, run a post-script count assertion (e.g., `python3 -c "..."`) and paste the output as acceptance evidence. Do not derive summary counts from script logic alone.
- [ ] **Knight-rider (INFO-2 / Cycle 13):** Include `weapon_kind` consumer-status determination in Cycle 13 substrate-binding dispatch scope.
- [ ] **Matt (no BLOCK — informational):** WARN-1 pattern is now two consecutive dispatches. If rocket continues to misreport summary counts, consider adding an explicit count-verification step to Gate-2 protocol for rocket dispatches.

---

## References

- Dispatch: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-25-rocket-v2-narrow-weapon-category-correction.md`
- Loadout commit: `cd36e42` — `data/v2_narrow/classes/` (35 files)
- Engine commit: `d25d6f0` — `exports/v2_narrow/classes.json` + `scripts/v2_narrow_weapon_category_correction_2026_05_25.py`
- Collaboration commit: `9f01f61` — dispatch completion record
- WeaponSlot: `/Users/admin/Games/reincarnated-loadout/src/components/WeaponSlot/WeaponSlot.tsx` lines 15-26
- Correction script: `/Users/admin/Games/reincarnated-engine/scripts/v2_narrow_weapon_category_correction_2026_05_25.py`
- Loadout class data: `/Users/admin/Games/reincarnated-loadout/data/v2_narrow/classes/` (35 files)
- Engine mirror: `/Users/admin/Games/reincarnated-engine/exports/v2_narrow/classes.json`
