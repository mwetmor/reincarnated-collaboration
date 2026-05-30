# Dispatch: star-lord — Cascade-R4 Follow-On Scope 3 — Nameless Kit Remediation

**Date:** 2026-05-29
**Execution date:** 2026-05-30
**Author:** knight-rider (dispatch prompt inline in session)
**Agent:** star-lord
**Priority:** HIGH (Matt directive: "kits can't be nameless")
**Authorization:** Matt 2026-05-29 verbatim + hive-mind decision-routing (cascade-r4 follow-on)

---

## § 1. Scope

Cascade-R4 Follow-On Scope 3 — Nameless-kit remediation + retry-on-parse-failure + W-S2 regex fix + substrate-derived fallback pattern + targeted re-fire across 34 nameless kits + 3 Wave-S re-fires.

**Root cause confirmed:** All 34 FAIL_RECORD kits had `error="parse_failure"` + `regeneration_fired=false`. The Wave B regeneration loop in `_call_wave_b_single` fired on W-B compliance gate failures but NOT on parse_failure. When the LLM returned malformed JSON, the code recorded the failure but did not retry.

**W-S2 root cause confirmed:** `WAVE_S_PATTERN_REGEX = [A-Z][a-z]+` too strict; doesn't match hyphenated compounds like "Mixed-Element". All 3 retroactive Wave-S calls FAIL_RECORD on W-S2.

---

## § 2. Work-items Completed

### Work-item 1 — Retry-on-parse-failure (COMPLETE)

`_call_wave_b_single` now retries on parse_failure (max 2 retries; exponential backoff via semaphore). `regeneration_reason="parse_failure_retry"` captured distinctly from compliance-gate regen. Existing W-B compliance gate regeneration preserved (zero regression).

### Work-item 2 — Substrate fallback pattern (COMPLETE)

`_build_wave_b_fallback_name()` implemented. Pattern: `[FactionEpithet] [Element] [WeaponFamily] Bearer`. New status `FALLBACK_SUBSTRATE_DERIVED`. `ai_tell_compliance_score=1.0` (substrate-derived → no AI-tell risk). Fires only after parse retries exhausted.

**Actual result:** 0 kits needed FALLBACK_SUBSTRATE_DERIVED. All 34 resolved to ACCEPT on parse-retry.

### Work-item 3 — W-S2 regex fix (COMPLETE)

`WAVE_S_PATTERN_REGEX` amended via `_WAVE_S_WORD_TOKEN = r"[A-Z][A-Za-z]*(-[A-Z][A-Za-z]*)*"`.
- Matches hyphenated compounds: Mixed-Element, Lightning-Scarred, Lightning-Struck
- `{0,4}/{0,3}` allows single-token NounPhrase
- All 3 existing retroactive season names now PASS W-S2

### Work-item 4 — 34-kit targeted re-fire (COMPLETE)

All 34 nameless kits remediated. 100% ACCEPT on parse-retry.

| Season | kits | nameless_before | accept_retry | fallback | still_nameless |
|---|---|---|---|---|---|
| season_001 | 34 | 9 | 9 | 0 | 0 |
| season_002 | 33 | 13 | 13 | 0 | 0 |
| season_003 | 33 | 12 | 12 | 0 | 0 |
| **TOTAL** | **100** | **34** | **34** | **0** | **0** |

Note: 2 kits in season_003 had W-B8 purity guard applied in re-fire script (kit_name_placeholder contained "Knight" / "Assassin" class-vocabulary; cleared to None; LLM used remaining substrate). This is re-fire-script-only mitigation; the fix prevents CascadeBlockError at re-fire time without modifying `_call_wave_b_single` (future seasons that generate these kits fresh will need a substrate-purification fix in `_build_kits_input_for_wave_b` — KR routing trigger surfaced below).

### Work-item 5 — Wave-S re-fire (COMPLETE)

All 3 seasons ACCEPT post-regex-fix:
- season_001: "Season of the Lightning-Scorched Chain" — ACCEPT
- season_002: "Season of the Storm-Shadowed Siege" — ACCEPT
- season_003: "Season of the Grounded Arcs" — ACCEPT

W-S7 Jaccard distinctness confirmed (chronological order enforced).

### Work-item 6 — MIGRATION.md §v1.65 + tests (COMPLETE)

- MIGRATION.md §v1.65 authored at `reincarnated-engine/src/reincarnated/export/MIGRATION.md`
- 15 new tests in `tests/test_cascade_r4_followon_nameless_kit_remediation.py` — all 15 PASS
- 250/250 wave tests PASS post-remediation (235 prior + 15 new); 0 regressions

---

## § 3. Tag

`star-lord/v1.0-cascade-r4-followon-nameless-kit-remediation-1`

---

## § 4. KR Routing Triggers

**Surfaced item — W-B8 purity in `_build_kits_input_for_wave_b`:**
2 season_003 kits had `kit_name_placeholder` with class-vocabulary ("Black Knight Ultra Greatsword", "Assassin's Throwing Axe"). The re-fire script cleared these manually. Future fresh season runs will need the same guard in `_build_kits_input_for_wave_b()` in `wave5_season_orchestrator.py` (rocket seam). Suggest routing a dispatch to rocket: add W-B8 purity pre-check to `_build_kits_input_for_wave_b` to clear `kit_name_placeholder` when it contains SUBSTRATE_PURITY_VOCAB_REGEX matches. Small, targeted, within-seam.

**No other KR routing triggers.** Matt directive satisfied: zero nameless kits.

---

## Completion Record

**COMPLETE 2026-05-30 (star-lord):**

- Work-item 1 (retry-on-parse-failure): PASS — `_call_wave_b_single` retries max 2 on parse_failure
- Work-item 2 (substrate fallback): PASS — `_build_wave_b_fallback_name()` + FALLBACK_SUBSTRATE_DERIVED implemented (not needed in practice; 0 kits exhausted retries)
- Work-item 3 (W-S2 regex): PASS — all 3 retroactive season names now PASS W-S2
- Work-item 4 (34-kit re-fire): PASS — 34/34 remediated; 100/100 kits named; 0 nameless
- Work-item 5 (Wave-S re-fire): PASS — 3/3 seasons ACCEPT
- Work-item 6 (MIGRATION + tests): PASS — §v1.65 authored; 250/250 tests; 0 regressions
- Tag: `star-lord/v1.0-cascade-r4-followon-nameless-kit-remediation-1`
- Commits: `16d6e01` (engine code + tests + MIGRATION + scripts), `9d3820e` (test un-skip + purity guard), `7513e54` (data artifacts)
- 100% kit coverage confirmed: zero nameless kits across all 3 production seasons

**Total cost:** ~$0.34 Wave B re-fire (34 × ~$0.01) + ~$0.045 Wave-S re-fire = ~$0.385 estimated
(within $0.50 projection; actual LLM cost confirmed in-envelope)

**Cross-seam data contract for drax (§ v1.65 addendum):**
- `wave_b_identities.json` — all 100 kits now have non-empty `kit_name_canonical`
- New status `FALLBACK_SUBSTRATE_DERIVED` defined (not present in current data; informational)
- `season_summary.json` — `wave_s_final_compliance_status` now ACCEPT across all 3 seasons
- No drax display-logic change required
