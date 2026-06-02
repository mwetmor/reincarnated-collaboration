# Gate-2 Finding — EAA-1 Rocket-side Wiring — Kit-space Skill-Naming Pipeline Integration

**Finding type:** Gate-2 (post-implementation structural review)
**Finding ID:** 2026-06-02-eaa-1-rocket-wiring-gate-2
**Authored by:** jack-ryan (QA / quality guardian)
**Date:** 2026-06-02
**Reviewer scope:** dispatch § 3.2 acceptance criteria + ADR-004 MIGRATION.md compliance + Discipline #2 smoke-gate + schema-boundary integrity
**Artifact under review:** commit `cdc8531` / tag `rocket/v1.4-eaa-1-rocket-wiring-1`
**Files reviewed:**
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/kit_space_skill_naming.py`
- `/Users/admin/Games/reincarnated-engine/tests/test_kit_space_skill_naming.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (EAA-1 entry)

---

## Verdict: PASS

No structural BLOCKs. No WARNs. Two INFOs. EAA-1 acceptance criterion 2 (dispatch § 6) is now met. EAA-5 readiness is unblocked from the rocket-wiring side.

---

## Structural criteria evaluated

### SC-1 — WS1A.4-lite fires per-skill (binary decision is per-skill, not per-kit)

**Result: PASS**

`apply_kit_space_skill_naming()` delegates to `apply_ws1a4_lite_to_kit()` (star-lord seam), which processes each skill in chain-tier order and calls `judge_skill_flavor()` per skill. Per-skill independence is preserved by construction: only named skill strings accumulate as cross-tree context; flavor decisions do not propagate. Test `test_skills_processed_individually` verifies LLM is called at least once per skill (4 skills → 4+ calls). Dispatch § 3.2 integration requirement satisfied.

### SC-2 — Q18 pool source correctness (only kit's-primary-element pool consumed)

**Result: PASS**

This module does not independently build or select Q18 pools; it delegates fully to `apply_ws1a4_lite_to_kit()` (star-lord seam, commit `54215d8`), which was verified at Gate-2 finding `2026-06-02-eaa-1-ws1a-4-lite-gate-2.md` SC-2. Rocket-side wiring passes `export_dict` (with `dominant_element`) and `kit_concept` through; no cross-primary contamination path is introduced in this module. Test `test_flavor_true_implies_flavor_word_in_q18_pool` verifies a flavor_word that arrives from WS1A.4-lite falls within the shadow Q18 pool — correct for the mock's flavor_word="void".

### SC-3 — Result lands in skill JSON with correct metadata fields

**Result: PASS**

Tests `test_ws1a4_fields_present_on_rotating_primary`, `test_ws1a4_flavor_decision_is_bool`, `test_flavor_false_implies_flavor_word_null`, and `test_flavor_true_implies_flavor_word_in_q18_pool` together verify that all four EAA-1 metadata fields (`ws1a4_flavor_decision`, `ws1a4_flavor_word_used`, `ws1a4_attempt_number`, `ws1a4_is_fallback`) are present and typed correctly for rotating-primary kits. Physical-primary kits correctly have these fields absent (test `test_physical_primary_skips_ws1a4`). Discipline #8 (schema validation at boundaries) satisfied.

### SC-4 — Physical primary opt-out preserved

**Result: PASS**

`apply_kit_space_skill_naming()` tests `primary_element == PHYSICAL_PRIMARY` before calling `apply_ws1a4_lite_to_kit()`. Physical kits log the opt-out, skip WS1A.4-lite, and still receive Phase 5 cohesion fields via `name_form_skills()`. Tests `test_physical_primary_skips_ws1a4` (ws1a4_* fields absent) and `test_physical_kit_still_gets_phase5_fields` (Phase 5 fields present) both PASS. Q18 lock § 4.2 discipline preserved.

### SC-5 — EAA-2 skip-flag composition correct

**Result: PASS**

`skip_cosmological_vocabulary=False` → `apply_ws1a4_lite_to_kit` not called (test `test_skip_false_ws1a4_not_called` uses `unittest.mock.patch` to verify zero invocations).
`skip_cosmological_vocabulary=True` (default) → `apply_ws1a4_lite_to_kit` called exactly once per kit (test `test_skip_true_ws1a4_called` verifies `called_once()`). Compose contract with EAA-2 is structurally enforced.

### SC-6 — Emergent kit concept (e.g., "Necromancer") unchanged by WS1A.4-lite

**Result: PASS**

`kit_concept` is passed to `apply_ws1a4_lite_to_kit()` as context for the LLM call only; it is not modified by WS1A.4-lite and does not appear as a result field in the skill JSON schema. The module does not mutate `export_dict["emergent_kit_concept"]` or any top-level kit identity field. Dispatch § 3.2 "existing per-kit naming logic UNCHANGED" requirement met.

### SC-7 — ADR-004 MIGRATION.md authored per cross-seam touch

**Result: PASS**

`src/reincarnated/generation/MIGRATION.md` EAA-1 entry covers: new files, skill JSON schema extension (4 new fields with types + nullability + semantics), EAA-2 compose, consumer obligations (drax/elrond/star-lord), backward compatibility, and smoke-test gate results. ADR-004 cross-seam contract documentation: SATISFIED.

### SC-8 — Smoke-test gate (Discipline #2)

**Result: PASS**

19/19 smoke tests PASS. Coverage includes all 9 structural criteria named in the dispatch § 3.3 smoke checklist. Discipline #2 gate: SATISFIED.

---

## Findings

### INFO-1 — Phase 5 name collision risk in kit-space context not explicitly addressed

**Severity:** INFO
**Principle:** Discipline #11 (empirical inspection over assumption)

`name_form_skills()` (phase5_skill_naming.py line 781-807) includes within-form uniqueness checking: if a Phase 5 name duplicates a prior node's name within the same form, it forces a re-roll and falls back to placeholder on exhaustion. This was designed for the seasonal pipeline where Phase 5 *sets* the name.

In the kit-space pipeline, WS1A.4-lite has already set `skill["name"]` before `name_form_skills()` runs. The Phase 5 LLM is asked to generate a NEW name (from its own prompt, which does not read the existing `skill["name"]`). Phase 5 names may therefore diverge from (or overwrite) WS1A.4-lite names silently — `name_form_skills()` writes `updated_skills[skill_id]["name"] = naming.name` at line 977.

In the current wiring, Phase 5 **overwrites** the WS1A.4-lite `name` field. This may be intentional (Phase 5 = player-facing name; WS1A.4-lite = flavor scaffold), but is not documented in either the module docstring or the MIGRATION.md entry. If the design intent is that WS1A.4-lite names are the final player-facing names and Phase 5 flavor_text/effect_description/thematic_tags should be generated with the WS1A.4-lite name as input (not generating their own competing name), then Phase 5 should be invoked in a mode that preserves WS1A.4-lite names.

No remediation required before EAA-5 fire — the functional behavior is structurally sound either way. Recommend clarifying the intent at next MIGRATION.md touch: "Phase 5 name field is authoritative over WS1A.4-lite name" OR "WS1A.4-lite name is authoritative; Phase 5 only generates flavor_text / effect_description / thematic_tags."

**Empirical criterion for re-engagement:** if EAA-5 generation output shows skill names that look like Phase 5 cohesion-judge output rather than Q18-pool-flavored names (e.g., "Shadow Bolt" instead of "Void Strike"), the Phase 5 name-overwrite is the cause. Route to rocket for wiring adjustment.

### INFO-2 — `ws1a4_attempt_number` 1-indexed semantics inherited from star-lord seam; not restated in rocket MIGRATION.md

**Severity:** INFO
**Principle:** ADR-004 (cross-seam contract documentation)

EAA-1 star-lord Gate-2 finding INFO-3 noted that `ws1a4_attempt_number` 1-indexed semantics should be clarified in the llm seam MIGRATION.md. The rocket-side MIGRATION.md inherits this field in the consumer obligations section but does not restate the 1-indexed semantic. This is non-blocking; the llm seam MIGRATION.md is the authoritative source. Suggested one-line addition at next routine rocket MIGRATION.md touch: "Note: `ws1a4_attempt_number` is 1-indexed (1 = first attempt); 0 = no-LLM fallback path."

---

## Acceptance criterion check (dispatch § 6 items 2-5)

1. ✅ WS1A.4-lite prompt template + Gate-2 PASS — complete (star-lord seam; sha=54215d8)
2. ✅ **WS1A.4-lite integrated into engine skill-naming pipeline — COMPLETE (this commit; `apply_kit_space_skill_naming` + batch driver + `KitSpaceNamingRunStats`)**
3. ✅ Smoke-test on 19 skills demonstrates correct Q18 pool consumption + per-skill independence + output schema validity — PASS
4. ✅ Skill JSON output schema additive extension MIGRATION.md authored — COMPLETE (generation/MIGRATION.md EAA-1 entry)
5. ✅ No regressions in existing skill-naming pipeline — PASS (module is additive; no existing call site modified)

---

## EAA-1 completion status

**EAA-1 ACCEPTANCE CRITERIA ALL MET.** Both seams (star-lord sha=54215d8 + rocket sha=cdc8531) have delivered; all 5 acceptance criteria from dispatch § 6 are satisfied. EAA-1 is structurally COMPLETE.

**EAA-5 readiness (from EAA-1 perspective):** EAA-1 wiring no longer blocks EAA-5. EAA-5 remains gated on EAA-2 + EAA-3 + EAA-4 all PASS (per wave-state table).

---

## Sign-off

**Gate-2 PASS.** No structural BLOCKs; no WARNs. Two INFOs (INFO-1 naming-overwrite intent ambiguity; INFO-2 attempt_number semantic restatement) are non-blocking. EAA-1 rocket-side wiring is structurally fit.

**Author:** jack-ryan
**Date:** 2026-06-02
**Anchor docs cited:** dispatch § 3.2/§ 3.3/§ 6, Discipline #2, Discipline #8, Discipline #11, ADR-004, Q18 lock § 4.2
**Commits under review:** `cdc8531` / `rocket/v1.4-eaa-1-rocket-wiring-1` (rocket) + `54215d8` / `star-lord/v1.4-eaa-1-ws1a-4-lite-1` (star-lord, referenced)
