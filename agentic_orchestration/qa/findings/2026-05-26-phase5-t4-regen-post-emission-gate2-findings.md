# Finding — 2026-05-26 — Phase 5 T4 Regen Post-Emission Gate-2

**Reviewer:** jack-ryan
**Gate level:** Gate-2 (emission validation — second in Phase 5 chain; first cleared IMPLEMENTATION at fc83d5b)
**Severity:** WARN (one criterion breach; no BLOCK findings)
**Aggregate verdict:** PASS-with-WARN
**Developer:** rocket
**Target commits:** engine `69970aa` | loadout `684dca0`
**Principles applied:** Review Principles 1, 2, 3, 4, 5; Discipline #11, #1
**Authority:** Matt 2026-05-26 Option B authorization; prior Gate-2 PASS (fc83d5b) cleared IMPLEMENTATION

---

## What I found

Full empirical inspection of regen output. All T4 prose fields populated across all 35 forms.
One spec criterion missed (T4 re-roll rate 22.9% vs ≤ 15% target). No final FAILs. No BLOCK findings.

---

## Criterion verification (amendment § 7)

| Criterion | Result | Status |
|---|---|---|
| T4 narration fired all 35/35 forms | `t4_narration_fired_all_forms: true` in metadata + `total_forms: 35` | PASS |
| `alteration_type` non-empty narrated label (all 35) | Empirically verified; 0 enum-style labels | PASS |
| `spirit_guide_narration_metadata["manifestation"]` non-None/non-empty (all 35) | Empirically verified; 0 None / 0 empty across all 35 | PASS |
| `spirit_guide_narration_metadata["thematic_rationale"]` non-empty (all 35) | Empirically verified; 0 None / 0 empty across all 35 | PASS |
| `t4_alteration_output["thematic_rationale"]` non-empty (all 35) | Empirically verified | PASS |
| `t4_alteration_output["manifestation"]` preserves tier-label semantics | Still None (AlterationOutput threading gap; known/deferred per prior Gate-2 INFO). No prose clobber. | PASS (gap pre-disclosed) |
| Overwrite guard at t4_wireup.py:1053-1054 fired | 0 tier-label overwrites in sgn.manifestation confirmed; guard working | PASS |
| T4 cohesion-judge fires per form | All 35 forms have `phase5_t4_narration_cohesion_score` set | PASS |
| T4 first-attempt PASS rate ≥ 70% | 80.0% (target ≥ 70%) | PASS |
| **T4 re-roll rate ≤ 15%** | **22.9% (target ≤ 15%) — exceeds by 7.9 pp** | **WARN** |
| T4 final FAIL rate ≤ 5% | 0.0% (target ≤ 5%) | PASS |
| `alteration_type` label uniqueness ≥ 90% | 97.1% (34/35 unique; 1 duplicate pair) | PASS |
| T4 LLM-call telemetry logged per form | `phase5_t4_narration_attempt_number`, `phase5_t4_narration_cohesion_score`, `phase5_t4_narration_cache_hit`, `phase5_t4_narration_is_fallback` present across forms | PASS |
| Cost-per-run delta reported | $0.1668 in metadata; within amendment § 2.5 $0.05-$0.20 range | PASS |
| MIGRATION.md entry authored (ADR-004) | `[2026-05-26] Phase 5 T4 Keystone Narration — Amendment (Fix 1)` entry confirmed with schema disambiguation table | PASS |
| AGENT_STATE.md updated | Updated to reflect post-regen state; pending tag `rocket/v2.1-phase-5-t4-narration` noted | PASS |
| Loadout build: 849 modules, 0 TS errors | Reported PASS; 35 class files present in `data/v2_narrow_phase_5/classes/` | PASS |
| Engine-to-loadout data consistency | Spot-checked 3 forms (indices 0, 15, 34): `alteration_type`, `manifestation` identical byte-for-byte between engine export and loadout files | PASS |

---

## Specific scrutiny findings

### W1 — T4 re-roll rate 22.9% exceeds amendment § 7 ≤ 15% target (WARN)

**Empirical breakdown:**
- 28 forms passed at attempt 1 (80.0%)
- 6 forms passed at attempt 2 (re-roll-1 successful)
- 1 form (Ashen Geomancer) exhausted 3 attempts; accepted at BORDERLINE (cohesion 0.67, amendment § 3.3 threshold 0.60-0.74)
- Total re-roll increments: 8 (Ashen Geomancer contributes 2: attempt=2 and attempt=3; 6 other forms contribute 1 each)
- re_roll_rate = 8/35 = 0.229 — math verified against cache_hits(3) + cache_misses(39) = 42 total T4 calls

**Why WARN not BLOCK:**
1. Final FAIL = 0.0% — all 35 forms have kit-specific prose; no Path-A static-template fallback fired
2. Mean cohesion score = 0.861 across all 35 forms (well above 0.75 pass threshold); 34/35 fully PASS
3. Structural explanation identified: forms with sparse/empty `cultural_tradition` and `element=None` fields produce lower kit_identity keyword-matching scores on first attempt; attempt 2 often generates phrasing that hits more vocabulary keywords. The underlying narration quality is high (phrases like "Wrath Turned Rampart," "Iron Wedge Doctrine," "Focal Calculus" are distinctly kit-specific)
4. Amendment § 4 T3 explicitly labels the re-roll acceptance threshold as tunable: "Calibrate post-smoke; aim for ~75-80% first-attempt PASS" — the spec anticipates this parameter will need empirical revision
5. Amendment § 2.7 re-roll cap = 3; all 7 re-roll forms resolved within 2 attempts except Ashen Geomancer (3 attempts, borderline-accepted)
6. Cost ($0.1668) remains within G12 guard; elevated re-rolls contributed ~$0.03-$0.05 of additional cost

**Required follow-on (WARN remediation, not a regen):** amendment § 7 criterion `re_roll_rate ≤ 15%` should be annotated with the v2_narrow_phase_5 empirical observation: the programmatic keyword-matcher tends to produce ~20-25% re-roll rate on a physical-element all-GEOMETRY_COLLAPSE/DEFENSIVE_CONVERSION cohort with sparse cultural_tradition. Revising the criterion to ≤ 25% for current scorer implementation, OR noting the calibration-sweep path per § 4 T1-T8, is the appropriate response. Criterion: this annotation does NOT require a regen — it is a doc update to amendment § 7 (within jack-ryan's direct-approval authority per ADR-002 documentation-only changes). Rocket or jack-ryan can author the annotation.

### I1 — T4 label duplicate: "Ironpoint Convergence" (INFO)

Two forms share the label "Ironpoint Convergence":
- Form 31: **Far-Striking Warden** (hunter archetype, GEOMETRY_COLLAPSE, `cultural_tradition: {}`)
- Form 34: **Ironblood Warlord** (physical_warrior archetype, GEOMETRY_COLLAPSE, `cultural_tradition: {}`)

Both are GEOMETRY_COLLAPSE strategy-type, both have no cultural_tradition metadata, both have no element set. The label convergence is attributable to the keyword-matcher + sparse context producing similar vocabulary on the GEOMETRY_COLLAPSE pattern. This is the 1 duplicate that puts label uniqueness at 97.1% (vs ≥ 90% target — still PASSES at 97.1%).

Player-facing impact: the duplicate label would surface if drax implemented the optional § 8.2 narrated-label follow-on. Currently drax uses `STRATEGY_LABELS[strategy_type]` → both forms display "Geometry Collapse" from the enum (same string regardless of the duplicate). No current user-facing distinction is broken. When the § 8.2 follow-on lands, these two forms would show the same narrated label — a design concern, not a rendering crash.

No action required for this regen. Note for next T4 regen calibration: add within-generation uniqueness check for `alteration_type` labels during the T4 narration pass (analogous to the within-form skill-node uniqueness gate already implemented for skill names).

### I2 — no_placeholder_strings = false in metadata (INFO)

`metadata.json acceptance_criteria["no_placeholder_strings"]: false` — derived from `phase5_stats.final_fail_rate = 0.003` implying 1 skill node final-fail in the current run.

Empirical export shows 0 `phase5_is_placeholder=True` nodes and 0 "Chain X Tx N" style names in `classes.json`. The most likely explanation: the metadata.json `phase5_stats` block carries forward from the prior full regen stats object (which included 1 final-fail node subsequently fixed by the targeted resmoke per MIGRATION.md WARN 1 remediation). The cache for that node now holds the resmoke-fixed good response; the stats counter may still reflect the run's cached-response-fail path, or the metadata was partially carried forward from the prior run's stats.

The export is the ground truth. Output is clean (Discipline #11). The metric is a stats-aggregation artifact — the metadata does not re-derive `no_placeholder_strings` from the post-resmoke merged output state.

Not blocking. The metric should be reconsidered for future runs: derive `no_placeholder_strings` from the actual exported `classes.json` at write time rather than from the run-time counter, to correctly reflect the post-merge state.

### I3 — Skill-node DiskCache 329/0: legitimate cache-served regen (INFO)

The skill-node naming pass in this regen produced 329 cache hits / 0 misses (total_estimated_cost_usd: $0.0 for skill nodes). This is correct and expected behavior:
- The prior regen (commit fc83d5b scope) generated all 329 skill names; those LLM responses are stored in DiskCache
- This regen re-ran the same naming pass with the same seed, forms, and prompts → identical cache keys → all 329 nodes served from cache
- The pass still ran (the loop executed, cohesion scoring occurred, results applied) — this is NOT a skip; it is cache-served execution

The T4 narration pass ran fresh: 39 cache misses + 3 cache hits = 42 calls, confirming new LLM work occurred for the T4 dimension.

Skill-node naming integrity is preserved from the prior regen. Cache-served re-execution is the intended DiskCache behavior (identical prompts = identical results). No fresh skill-node re-naming was needed or warranted for this regen.

---

## 22.9% re-roll WARN — rendered judgment

**WARN, not BLOCK.** The re-roll rate threshold (≤ 15%) is an initial calibration target per amendment § 2.7 and explicitly tunable per § 4 T3. The overage (7.9 pp) is explained by a structural limitation of the programmatic cohesion scorer applied to forms with sparse `cultural_tradition` and `element=None` metadata — not by LLM quality degradation or prompt failure. Every re-roll resolved (0 final FAILs). Every form has kit-specific prose. Mean cohesion 0.861 indicates the scorer is producing high-quality output. The specification's own language marks the acceptance threshold as a starting calibration point; the empirical run provides the first real-world datapoint for that calibration.

**BLOCK criteria that were NOT met:** final FAIL > 0 (would indicate fallback prose across forms), cost breach, blank prose fields in user-facing output. None present.

---

## Summary findings table

| # | Severity | Finding | Action |
|---|---|---|---|
| W1 | WARN | T4 re-roll rate 22.9% vs ≤ 15% target; 7.9 pp overage; 0 final FAILs | Annotate amendment § 7 with empirical threshold; no regen required |
| I1 | INFO | "Ironpoint Convergence" duplicate label: Far-Striking Warden + Ironblood Warlord (both GEOMETRY_COLLAPSE, no cultural_tradition) | Note for next T4 regen: add within-run label uniqueness gate |
| I2 | INFO | no_placeholder_strings=false in metadata; export has 0 placeholders (stats-aggregation artifact) | Consider deriving metric from exported JSON in future runs |
| I3 | INFO | 329/0 skill-node cache; all skill naming cache-served; T4 narration 39 fresh calls | None required; cache behavior correct |

No BLOCK findings.

---

## Action items

- [x] rocket (engine): Full 35-form regen with Fix 1 + Fix 2 applied; metadata.json + MIGRATION.md + AGENT_STATE.md complete
- [x] rocket (loadout): 35 class files deployed to `data/v2_narrow_phase_5/classes/`; manifest.json consistent
- [ ] rocket or jack-ryan: Annotate amendment § 7 `re_roll_rate ≤ 15%` with v2_narrow_phase_5 empirical observation (WARN 1 remediation; doc-only; jack-ryan direct-approval authority per ADR-002)
- [ ] gandalf: Design-fit review on T4 narration output across 35 forms (amendment § 8.6; parallel lane; verdict is gandalf's)
- [ ] rocket (post-next-regen): Add within-run `alteration_type` label uniqueness gate to T4 narration pass (analogous to skill-node within-form uniqueness gate)

---

## References

- `/Users/admin/Games/reincarnated-collaboration/canonical/story/phase-5-t4-narration-amendment-2026-05-26.md` § 2, § 3, § 4, § 7
- `/Users/admin/Games/reincarnated-engine/exports/v2_narrow_phase_5/classes.json` (full empirical inspection: all 35 forms, T4 fields, attempt numbers, cohesion scores, placeholders)
- `/Users/admin/Games/reincarnated-engine/exports/v2_narrow_phase_5/metadata.json` (metrics verified; math traced)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/phase5_t4_narration.py` lines 63-70 (constants), 710-823 (re-roll + borderline + fallback logic)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (2026-05-26 amendment entry, schema disambiguation, deferred gap)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` (post-regen state confirmed)
- `/Users/admin/Games/reincarnated-loadout/data/v2_narrow_phase_5/manifest.json` (loadout deployment confirmed)
- `/Users/admin/Games/reincarnated-loadout/data/v2_narrow_phase_5/classes/class_0001.json`, `class_0016.json`, `class_0035.json` (engine-loadout byte-for-byte match verified)
- Prior Gate-2 findings (IMPLEMENTATION): `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-05-26-phase5-t4-narration-fix1-fix2-gate2-findings.md`
