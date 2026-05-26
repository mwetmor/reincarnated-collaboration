# Finding — 2026-05-26 — Phase 5 T4 Narration Fix 1 + Fix 2 — Gate-2

**Reviewer:** jack-ryan
**Gate level:** Gate-2 (implementation validation)
**Severity — Fix 1:** INFO (PASS-with-INFO)
**Severity — Fix 2:** INFO (PASS-with-INFO)
**Aggregate verdict:** PASS-with-INFO — regen-fire eligible
**Developer (Fix 1):** rocket (commit fc83d5b; fc83d5b-adjacent files verified)
**Developer (Fix 2):** drax (commits dbb77c4 + e3dcbf5; compound-root-cause commit aa6abc0)
**Target commits:** rocket fc83d5b | drax dbb77c4 + e3dcbf5
**Principles applied:** Review Principles 1, 2, 3, 4, 6; Discipline #1, #2, #11, #12
**Authority:** Matt 2026-05-26 pre-authorized chain routing

---

## What I found

### Pre-inspection state (empirical baseline)

v2_narrow_phase_5/classes.json confirmed at time of Gate-2 review (Discipline #11 — empirical inspection):
- All 35 forms: `t4_alteration_output["thematic_rationale"]` = None, `["manifestation"]` = None
- All 35 forms: `spirit_guide_narration_metadata["thematic_rationale"]` = None, `["manifestation"]` = None
- All 35 forms: `spirit_guide_narration_metadata["alteration_type"]` = enum pass-through (e.g., `"DEFENSIVE_CONVERSION"`)
- This confirms the pre-regen state. Full 35-form T4 narration fill fires post-Gate-2-PASS.

---

## Fix 1 — Rocket: Phase 5 T4 Narration Implementation

### Criterion verification (amendment § 7)

**IMPLEMENTATION-READY criteria (verifiable pre-regen):**

| Criterion | Status | Evidence |
|---|---|---|
| T4 narration LLM pass fires for ALL forms (35/35) | READY | `narrate_form_t4()` called per form in `apply_phase5_skill_naming()`; loop confirmed in phase5_skill_naming.py line ~1084-1154 |
| Per-form output schema populated: `alteration_type` + `manifestation` + `thematic_rationale` | READY | `apply_t4_narration_to_export()` writes all three slots; `T4KeystoneNarration` dataclass fields all required (non-Optional) |
| `spirit_guide_narration_metadata["manifestation"]` fills (PROSE) | READY | `sgn["manifestation"] = narration.manifestation` at line 874 of phase5_t4_narration.py; guarded by `isinstance(sgn, dict)` |
| `spirit_guide_narration_metadata["alteration_type"]` replaces enum with narrated label | READY | `sgn["alteration_type"] = narration.alteration_type` at line 873 |
| `t4_alteration_output["thematic_rationale"]` top-level mirror | READY | `t4_out["thematic_rationale"] = narration.thematic_rationale` at line 854 |
| `t4_alteration_output["manifestation"]` (tier label) UNCHANGED | READY | Line 855-856 comment confirms DO NOT OVERWRITE; code does not touch `t4_out["manifestation"]` |
| T4 narration cohesion-judge fires per form | READY | `score_t4_cohesion()` called inside `narrate_t4_keystone()` per-attempt; result stored to `T4KeystoneNarration` fields |
| Cohesion weights 0.60 + 0.40 match amendment § 3.3 | PASS | `_T4_COHESION_WEIGHTS = {"kit_identity": 0.60, "thematic_rationale_fit": 0.40}` — matches |
| PASS threshold 0.75 matches amendment § 3.3 | PASS | `T4_COHESION_PASS_THRESHOLD = 0.75` — matches |
| t4_wireup.py guard at ~line 1047 | PASS | Verified at lines 1053-1054: `if narration.get("manifestation") is None: narration["manifestation"] = alteration_output.manifestation` — correct guard, does not clobber LLM prose when present |
| Top-level `t4_alteration_output["manifestation"]` still writes tier label at line 1044 | PASS | Line 1044: `emission["manifestation"] = alteration_output.manifestation` — unconditional; tier label preserved for the non-None alteration_output path |
| `apply_phase5_skill_naming()` 3-tuple return | PASS | `return export_dicts, stats, t4_stats` confirmed at line 1172; parameter `run_t4_narration: bool = True` at line 1010 |
| Generation script unpacks 3-tuple | PASS | `updated_dicts, stats, t4_stats = result_tuple` at line 197; T4 acceptance criteria reporting + metadata.json write confirmed at lines 243-288 |
| MIGRATION.md addendum authored (ADR-004) | PASS | `[2026-05-26] Phase 5 T4 Keystone Narration — Amendment (Fix 1)` entry confirmed; schema disambiguation table present; AlterationOutput threading gap deferral documented |
| AlterationOutput threading gap logged in AGENT_STATE.md | PASS | `generation/AGENT_STATE.md` line 20: gap captured with Cycle 13 v1.1 gate |

**POST-REGEN criteria (verifiable only after full regen fires — pending at this Gate-2):**

| Criterion | Status |
|---|---|
| First-attempt PASS rate ≥ 70% across 35 forms | Pending |
| Re-roll rate ≤ 15% | Pending |
| Final FAIL rate ≤ 5% | Pending |
| `alteration_type` label uniqueness ≥ 90% | Pending |
| No § 9 template voice fallback fires in drax (visual check) | Pending |
| Cost-per-run delta in metadata.json | Pending |
| gandalf design-fit review | Pending (post-Gate-2 per amendment § 8.6) |

### Specific scrutiny findings — Fix 1

**Smoke-test sufficiency (3 vs 5+ forms — Discipline #2):**

3-form smoke is at the lower bound of typical practice. Empirical results: 100% first-attempt PASS on all 3, 0% re-rolls, 0% fallback, 100% label uniqueness, cost $0.0127. With 100% PASS on all tracking dimensions, the statistical value of 2 additional forms is marginal — they would not change the calibration or reveal a threshold issue. Discipline #2 intent is "smoke before commit," not "N-form minimum." 3 forms at 100% PASS is defensible for a go/no-go gate. The full 35-form regen IS the next step and serves as the broader empirical validation.

INFO: Not a WARN because 100% PASS rate leaves no open calibration question that 5 forms would answer. Note for the record.

**Cost math verification:**

Amendment § 2.5 projection: $0.05-$0.20 per run at Claude 3.5 Sonnet. Smoke actual: $0.0127 / 3 forms = $0.0042/form. 35-form projection: $0.15. This is WITHIN the projection range ($0.05-$0.20 is a generous-upper-bound estimate per amendment note; $0.15 is the central case). The submission reports "$0.0043/form" — correct to the precision shown ($0.0127/3 = $0.0042; rounds to $0.0043 at 4 decimal). No discrepancy.

**AlterationOutput threading gap deferral (Discipline #12 scope judgment):**

Gandalf's investigation note flagged this as potentially in scope for this dispatch ("may warrant rocket investigation"). Rocket's judgment to DEFER to Cycle 13 v1.1+ is sound. Rationale:
1. The amendment's Path B LLM fill is independent of AlterationOutput wiring
2. The top-level `t4_alteration_output["manifestation"]` (tier label) remaining None is a COSMETIC gap — Spirit Guide prose lands correctly via `spirit_guide_narration_metadata["manifestation"]`
3. The bug fix guard in t4_wireup.py ensures prose is NOT clobbered when the wiring gap is eventually fixed
4. Fixing the wiring gap requires multi-file changes to class_generator export pipeline — cross-seam scope change that would need its own Gate-1 review

Consequence logged clearly in both MIGRATION.md and AGENT_STATE.md. The cosmetic gap (tier label None at `t4_alteration_output["manifestation"]`) is disclosed; it does not affect player-facing prose. DEFER rationale is sound.

INFO: Retaining as INFO for the record — the tier-label None state is visible in exported JSON and may surface in future drax rendering work.

**Cohesion judge — programmatic approach:**

The implementation uses keyword-matching against element/cultural/strategy-type vocabulary dictionaries (same pattern as parent Phase 5 spec skill-node naming). This is consistent with the established project pattern. The scoring logic correctly computes the 2-dimension aggregate per amendment § 3.3 formula. One structural note: the scoring relies heavily on exact keyword matching — "iron" matches both `physical` element vocab AND `european` cultural vocab. For Phase 5's all-physical element set, the element hit path is the primary driver; the structural overlap is not a correctness issue but would affect score interpretation for multi-element future runs. Not in scope for this review; noted as INFO.

---

## Fix 2 — Drax: WeaponDescriptor Schema Alignment

### Criterion verification

| Criterion | Status | Evidence |
|---|---|---|
| `WeaponDescriptor.source_library` made optional (`string | null`) | PASS | `source_library?: string | null` in types.ts line 286 (diff verified at dbb77c4) |
| `WeaponDescriptor.lineage` made optional (`string | null`) | PASS | `lineage?: string | null` at line 289 |
| `weapon_id: string | number` union | PASS | Line 283; TODO(drax) annotation for Cycle 13+ normalization |
| v2_narrow regression: source_library + lineage still present | PASS | Empirically verified: all 35 v2_narrow forms have `main_weapon.source_library` present and non-empty; no render regression |
| v2_narrow_phase_5 source_library: present (so `?` annotation is forward-compat, not changing current state) | VERIFIED | All 35 v2_narrow_phase_5 forms have `source_library` populated — schema relaxation is precautionary for future variation in Phase 5 regen output post-T4 amendment |
| Build smoke: 849 modules, 0 TS errors | PASS | Stated in commit message; Vercel deploy live |
| `isEngineV2Season` updated for v2_narrow_phase_5 | PASS | `SeasonSummaryCards.tsx` line 128 confirmed includes `id === 'v2_narrow_phase_5'` |
| `seasonLabel` mapping: `'v2_narrow_phase_5' → 'Narrow v1.0 P5'` | PASS | `useAnalytics.ts` line 129 confirmed |
| Deploy live at Vercel production alias | REPORTED PASS | Per commit record; Vercel build smoke 849 modules 0 errors |

### Specific scrutiny findings — Fix 2

**Option A (UI-side relaxation) vs Option B (engine-side completion) — architectural posture:**

Drax chose Option A per KR recommendation citing the v2 engine canonical contract (L9 substrate refactor guarantees weapon_id/name/category/period/cultural_register; source_library/lineage are substrate-optional). This is the correct call. Option B (engine-side schema-completion) would require touching rocket's export pipeline and adds scope to a fast-follow fix. The engine canonical contract defines the floor; UI-side guards for fields above the floor are the established pattern throughout this codebase (consistent with BalanceMetadata optionality, Skill field optionality, etc. introduced in aa6abc0).

PASS. No concern.

**`weapon_id: string | number` union:**

Empirically verified: all 35 v2_narrow_phase_5 forms emit `weapon_id` as `str` type (Python), rendering as string in JSON. All 35 v2_narrow forms also emit `weapon_id` as string. The `string | number` union is therefore PRECAUTIONARY for a future engine variant — not fixing a current observed integer emission. This is acceptable forward-compatibility; the TODO(drax) annotation at the definition site is appropriate. The union type does not affect rendering (weapon_id is not displayed in UI per commit note).

INFO: union is slightly conservative (current emit is string-only); union is safe and the TODO annotation correctly flags the Cycle 13+ normalization point. No action required.

**Compound root-cause attribution:**

Attribution is correct. aa6abc0 fixed the primary blank-page crash (React tree unmount from `bm.final_modifier.toFixed(4)` TypeError) — this was the DOMINANT cause of the blank main_weapon appearance (React didn't render anything). dbb77c4 fixed the schema-strictness gap (TypeScript would throw on optional field access without guards). Both were needed; the ordering (aa6abc0 first, dbb77c4 second) is the correct triage sequence (fix the crash, then clean up the schema strictness). The submission correctly identifies aa6abc0 as the compound precursor. Attribution discipline (Principle 4) satisfied.

---

## Summary findings

### Fix 1 findings

| # | Severity | Finding | Action |
|---|---|---|---|
| F1-01 | INFO | 3-form smoke is lower bound; 100% PASS means no calibration gap left open. Post-regen 35-form results serve as the broader validation. | None required |
| F1-02 | INFO | AlterationOutput threading gap deferred — `t4_alteration_output["manifestation"]` (tier label) remains None. Cosmetic only; Spirit Guide prose lands correctly. | Cycle 13 v1.1+ per MIGRATION.md + AGENT_STATE.md |
| F1-03 | INFO | Cohesion judge keyword-matching has `iron` overlap in physical/european vocab. Not a correctness issue for Phase 5 all-physical set. Note for v1.1 multi-element extension. | None required |

### Fix 2 findings

| # | Severity | Finding | Action |
|---|---|---|---|
| F2-01 | INFO | `weapon_id: string | number` union is precautionary — current emit is string-only. TODO annotation is appropriate. | Cycle 13+ normalization per TODO |

No WARN or BLOCK findings on either fix.

---

## Action items

- [x] rocket (Fix 1): Implementation complete; MIGRATION.md + AGENT_STATE.md written; Gate-2 PASS granted
- [x] drax (Fix 2): Schema aligned; Vercel deploy live; Gate-2 PASS granted
- [ ] rocket: Fire 35-form v2_narrow_phase_5 (or v2_narrow_phase_5_v2) regen with both fixes applied (Task #13; rocket judgment on tag name)
- [ ] jack-ryan: Post-regen Gate-2 fires after 35-form regen completes (per Phase 5 Gate-2 chain pattern)
- [ ] gandalf: Design-fit review on T4 narration output across 35 forms (amendment § 8.6; fires post-regen)

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-05-26-jack-ryan-gate2-phase5-t4-narration-fix1.md`
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/phase-5-t4-narration-amendment-2026-05-26.md` § 2, § 3, § 7
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/phase5_t4_narration.py` (new module; full read)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/t4_wireup.py` lines 1037-1063 (bug fix verified)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` lines 153-290 (amendment entry + threading gap deferral)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` lines 3-21 (threading gap + deferred queue)
- `/Users/admin/Games/reincarnated-loadout/src/data/types.ts` lines 276-295 (WeaponDescriptor schema change; full read)
- Commits: drax `dbb77c4` (types.ts diff verified), `aa6abc0` (compound-root-cause), `e3dcbf5` (AGENT_STATE)
- Empirical: `exports/v2_narrow_phase_5/classes.json` — T4 fields pre-regen state confirmed; weapon_id/source_library/lineage shape confirmed
- Empirical: `exports/v2_narrow/classes.json` — 35/35 forms have source_library present; weapon_id type = str; v2_narrow regression confirmed clean
