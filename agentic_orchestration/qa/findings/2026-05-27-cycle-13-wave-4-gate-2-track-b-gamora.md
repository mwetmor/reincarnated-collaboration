# Finding — 2026-05-27 — Cycle 13 Wave 4 Gate-2: Track B Gamora Sim Cycling

**Reviewer:** jack-ryan
**Severity:** PASS (0 BLOCK; 0 WARN; 5 INFO)
**Target:** engine commit `10a6193` + collab commit `c956a4b`
**Developer:** gamora
**Principles applied:** Principles 1 / 2 / 3 / 4 / 6; Disciplines #1 / #1.1 / #1.2 / #11 / #18 / #18.2 / #26 / #30 / Principle 6

---

## Verdict

**PASS.**

All 10 critique dimensions satisfied. 193 tests confirmed PASS empirically (91 Wave 4 + 102 Wave 3 carryover; 0 regressions). WARN-pattern: **PRESERVED — 0 count failures; all 5 module-level assertions verified empirically.** All 6 sub-waves W4G.0-W4G.5 landed. SC-7 § 9 methodology pattern named per Discipline #30. 12-strata cohort × scope coverage matrix initialized. 3 in-flight bugs caught and fixed correctly. MIGRATION.md § v1.29 filed per ADR-004 with star-lord follow-on flagged.

Wave 4 Track B is CLOSED.

---

## Discipline #11 WARN-pattern PRESERVED verdict (CRITICAL)

**Status: PRESERVED. Full closure maintained through Wave 4.**

Empirical re-run performed this review session (Track B test files):

```
test_cycle13_wave4_sim_cycling.py: 91 tests PASS
test_cycle13_wave3_t4_scope_dimension.py: 102 tests PASS (regression clean)
```

Total Track B: 193 PASS. Zero failures. Combined with Track A: 346 total PASS in 0.60s.

**5/5 module-level assertions verified empirically via Python import + `len()` / direct value:**

| Assertion | Claimed | Actual | Status |
|---|---|---|---|
| `len(COHORT_ARCHETYPES)` | 4 | 4 | PASS |
| `len(T4_SCOPE_VALUES)` | 3 | 3 | PASS |
| `STRATA_COUNT_MAX` | 12 | 12 | PASS |
| `len(COHORT_KPM_BAND)` | 4 | 4 | PASS |
| `len(SURVIVAL_FLOOR_BY_COHORT)` | 4 | 4 | PASS |

Additional spot-checks from test class `TestPostScriptEmpiricalCounts` (all PASS in empirical run):
- `len(SCOPE_CHAIN_BREADTH) == 3` — PASS
- `len(REQUIRED_FIELDS) == 12` (test-file constant; 12 required T4SimRecord fields for star-lord export) — PASS
- All 4 cohorts named in `COHORT_KPM_BAND` + `SURVIVAL_FLOOR_BY_COHORT` — PASS
- All 3 scopes named in `SCOPE_CHAIN_BREADTH` — PASS

Module-load asserts enforce count correctness at import time in `t4_sim_cycling.py` (lines 74-84 for COHORT_ARCHETYPES/T4_SCOPE_VALUES/STRATA_COUNT_MAX; lines 124-126 for COHORT_KPM_BAND; lines 140-142 for SURVIVAL_FLOOR_BY_COHORT). Fail-fast discipline maintained.

**Cite:** Discipline #11 (empirical inspection via Python import + pytest run performed this review session; not inferred from gamora completion record).

---

## What I found — 10 critique dimensions

### D1 — Architectural alignment (#18 + #11) — INFO (fully aligned)

Empirical spot-check across `t4_sim_cycling.py` (first 450 lines + key sub-wave functions) and math note:

- SC-7 FULL methodology pattern consumed per Discipline #18.2: gamora fired SC-7 post-Wave-3-baseline (engine commit `2e8bc33` = baseline; SC-7 FULL = commit `6ebf6c8`). Correct extension-hotspot timing.
- Methodology pattern named at module docstring lines 9-14: verbatim match to SC-7 § A.2 per Discipline #30 (see D2 below).
- `CoverageMatrix` class correctly implements 12-strata initialization: `__post_init__` builds `all_strata` as Cartesian product `COHORT_ARCHETYPES × T4_SCOPE_VALUES` (lines 400-409). All strata start as `empty`; `mark_populated()` transitions them.
- W4G.3 critical structural note honored: "B14.5 historical medians INVALID as Wave 4 anchors." `COHORT_KPM_BAND` values in `t4_sim_cycling.py:117-122` are sourced from `endgame_mob_stat_profile.py:ENDGAME_COHORT_KPM_BAND` (Wave 4 fresh empirical; code citation at line 111-113 per Discipline #1.2). Not B14.5 historical.
- Block C scaffolding P_node + C_archetype + W function: sub-gate architecture implements `COHORT_KPM_BAND` (C_archetype) and `SURVIVAL_FLOOR_BY_COHORT` (C_archetype survival) per Block C Scaffold § 2.2. Band adjustment factor at W4G.3 (1.18/0.88/1.0) implements the W function.

No architectural drift from SC-7 § 9 FULL framework or Block C scaffolding.

**Cite:** Discipline #11 (code-line inspection). Discipline #18.2 (SC-7 timing post-baseline correct).

---

### D2 — SC-7 methodology pattern verification per #30 — INFO (fully verified)

Module docstring lines 9-14 (verified empirically):

```
"Per-weapon-cohort-exhaustive with sub-option-B DOMINANT (~85-90% estimated cohort-clear
fraction per Wave 3 COHORT_SCOPE_PRIORS analysis); stratified by progression node
(endgame-reference-encounter first per Block C § 1.5); tiered quick-estimate first
validation with elevated Tier 1 for I1 edge cases; scope-dimension-aware KPM band
calibration stratified by class chain count"
```

This matches SC-7 § A.2 verbatim (sub-option-B relabeled from "fallback" to "dominant path" per SC-7 FULL closure). Discipline #30 (sim-methodology-naming explicit-pattern-at-math-hotspots) PASS.

Math note `§ 1 — Methodology pattern name` also records verbatim match at line 14 (file confirmed present).

**Cite:** Discipline #30 (methodology pattern named explicitly at implementation site and math note; not just in dispatch).

---

### D3 — Sub-wave W4G.0-W4G.5 completeness (Discipline #1.2) — INFO (all 6 complete)

Per completion record and empirical code-line inspection:

| Sub-wave | Implementation artifact | Status |
|---|---|---|
| W4G.0 | `CoverageMatrix.__post_init__()`: 12 strata initialized; `w4g0_calibration_setup()` function; SC-6 integrity verified (18 encounters / 5 profiles / 4 cohorts / 3 scopes) | COMPLETE |
| W4G.1 | `_route_tier_1()` with REJECT/PROVISIONAL_PASS/BORDERLINE routing; `_is_i1_elevated()` trigger for 20-fight elevation; `TIER_1_REJECT_THRESHOLD=0.30` + `TIER_1_PROVISIONAL_PASS=0.05` per SC-7 § D2 | COMPLETE |
| W4G.2 | Full-sim 20 fights; `_evaluate_compound_gate()` all 6 sub-gates; `T4SimRecord` dataclass; `tier_2_batch` population | COMPLETE |
| W4G.3 | `w4g3_kpm_median_calibration()`; `KPMCalibration` dataclass; `band_adjustment_factor` logic (1.18/0.88/1.0); fresh empirical baseline from Wave 4 Tier 2 fight outcomes (NOT B14.5) | COMPLETE |
| W4G.4 | `w4g4_subgate_calibration()`; sg6 WARN counting; sg3 zero-damage-floor warn rate check (first-cycle empirical per SC-7) | COMPLETE |
| W4G.5 | `w4g5_archive_insertion_and_quality_report()`; stub-write mode (sentinel `export/wave4_schema_landed.sentinel` absent); output at `simulation/output/wave4_sim_results_stub_{timestamp}.json`; `QualityReport` with regen_rate + quarantine_rate + cohort classification | COMPLETE |

**Cite:** Discipline #1.2 (sub-wave implementation claims verifiable at code-line level; math note covers all sub-waves).

---

### D4 — Compute budget verification per #1.1 — INFO (within projection)

Constants at `t4_sim_cycling.py:104-106` (Discipline #1.1):

- `COMPUTE_BUDGET_FIGHTS_ENDGAME_ONLY = 9_340` — matches SC-7 § 9.4 projection.
- `COMPUTE_BUDGET_WALL_CLOCK_MIN_ENDGAME = 19.0` — matches SC-7 § 9.4 upper bound (~19-53 min range; 19 is endgame-only mode).
- `COMPUTE_BUDGET_PEAK_MEMORY_MB = 5.0` — sequential per-fight processing; <5MB.

Completion record states: "Wall-clock ~19 min upper bound. Peak memory <5MB. M2 8GB not at risk." Consistent with constants.

M2 8GB threshold: peak <5MB is within bound (5MB << 8GB; no risk). Per SC-7 § 9.4 compute re-projection.

**Cite:** Discipline #1.1 (resource-bounds projection verified at code-line level against SC-7 projection).

---

### D5 — Cohort × scope coverage matrix (12 strata) — INFO (correctly implemented)

`CoverageMatrix` at `t4_sim_cycling.py:387-435`:

- `all_strata`: tuple of 12 `StratumKey` instances from `COHORT_ARCHETYPES × T4_SCOPE_VALUES`.
- `__post_init__` initializes all 12 to `empty` set.
- `mark_populated()` transitions stratum from `empty` → `populated`.
- `w4g0_calibration_setup()` returns initialized `CoverageMatrix` for use in W4G.1-W4G.5.

Tests in `TestW4G0CoverageMatrix`:
- `test_coverage_matrix_12_strata`: `len(matrix.empty) == 12` — PASS empirically.
- `test_strata_labels_12`: `len(strata_labels) == 12` — PASS empirically.

Population occurs at runtime as legendary configs are processed; strata with no generated legendaries remain EMPTY (acceptable per math note § 2 coverage matrix definition).

**Cite:** Discipline #11 (test empirically verified 12-strata initialization).

---

### D6 — Sub-gate 6 cognitive-load burst threshold amendment (per SC-7 § E1) — INFO (implemented; structural placeholder acknowledged)

`_check_cognitive_load_burst()` at `t4_sim_cycling.py:701-733`:

- `scope_chain_breadth` encoding: CHARACTER_WIDE = `-1` sentinel (→ `class_chain_count` at runtime); CHAIN_WIDE_OWN = 1; CHAIN_WIDE_PARALLEL = 2. Matches SC-7 § E1 amendment.
- Threshold formula: `COGNITIVE_LOAD_BURST_BASE (8) × breadth`. For CHARACTER_WIDE 3-chain: threshold = 24; OWN: 8; PARALLEL: 16. Correct per SC-7.
- `SCOPE_CHAIN_BREADTH` dict at lines 152-156 with all 3 scopes.

**Structural placeholder observation (INFO not WARN):** `_check_cognitive_load_burst()` returns `SUBGATE_PASS, 0.0, threshold` unconditionally at line 733 because `FightSummary` does not carry per-tick event counts (action_trace data not available from `FightResult`). Code comment explicitly acknowledges this: "Actual per-0.5s window analysis requires action_trace instrumentation. Structural placeholder that PASSES for v1. Flagged for W5."

This is the correct V1 handling per SC-7 § E1: threshold formula implemented; measurement deferred to action_trace instrumentation (W5 enhancement). Not a WARN — gambit is acknowledged, documented, and the SC-7 framework explicitly defers calibration per Discipline #18.2.

**Cite:** Discipline #18.2 (sub-gate 6 calibration deferred post-Wave-4-baseline; placeholder is correct V1 stance). Discipline #1.2 (code comment cites W5 requirement).

---

### D7 — KPM median calibration (W4G.3) — INFO (fresh empirical; correctly sourced)

`KPMCalibration` dataclass at `t4_sim_cycling.py:438-...` and `w4g3_kpm_median_calibration()`:

- Initial bands (`COHORT_KPM_BAND`): sourced from `endgame_mob_stat_profile.py:ENDGAME_COHORT_KPM_BAND` (code citation at line 111-113). Not B14.5 historical.
- Band adjustment factor: `1.18` if observed pass_rate < 0.40 (band too tight); `0.88` if pass_rate > 0.85 (band too loose); `1.0` otherwise. SC-7 § B3 structural amendment honored.
- `w4g3_kpm_median_calibration()` accepts `Sequence[T4SimRecord]` and computes per-cohort median KPM from Tier 2 fight outcomes, producing fresh Wave 4 empirical baselines.

Tests in `TestKPMCalibration` and `TestBandCalibrationLogic` all PASS empirically.

SC-7 § B3 critical note: "historical B14.5 medians INVALID as Wave 4 anchors — scope-amplification effect changes KPM distribution structurally." Implementation sourcing from SC-6 endgame profiles (Wave 4 fresh) correctly honors this.

**Cite:** Discipline #11 (empirical band sourcing verified at code-line 111-113). SC-7 § B3 structural constraint honored.

---

### D8 — Discipline #11 WARN-pattern PRESERVED — PRESERVED (0 failures)

See dedicated section above. 5/5 module-level count assertions PASS empirically. 193/193 tests PASS. Module-load asserts provide structural enforcement at `t4_sim_cycling.py` import time. WARN-pattern PRESERVED milestone maintained through Wave 4 (Track B first baseline establishment) with zero failures.

The gamora completion record claims 5 assertions; empirical verification confirms 5 module-level + 9 additional test-class assertions (all PASS). No count mismatch found anywhere.

**VERDICT: PRESERVED.**

**Cite:** Discipline #11 (empirical inspection performed; not inferred from gamora completion record).

---

### D9 — Three in-flight bugs caught + fixed — INFO (all fixes correct)

**Bug 1: Monster constructor mismatch**
- Issue: `Monster(BaseModel)` requires `skills: list[Skill]`, `color_palette`, `mana_max`, etc. — Pydantic fields not available in sim cycling context (no bestiary lookup, no generation pipeline).
- Fix: `_build_synthetic_mob_combatant()` at `t4_sim_cycling.py:861-925` constructs `CombatantState` directly, bypassing `Monster` schema entirely. Code comment at line 872-881 explains the architectural rationale.
- Assessment: Correct fix. Constructing `CombatantState` directly is the right pattern for synthetic sim mobs — mirrors the Cycle 12 Wave 5 pattern from `combatant.py:from_player_class()`.

**Bug 2: flag_regen_rate threshold**
- Issue: Threshold `> 8.0` would never trigger on `[0,1]` metric (regen_rate is a fraction 0.0-1.0).
- Fix: Corrected to `> 0.08` at `t4_sim_cycling.py:505` (8% fraction threshold per SC-7 § B1).
- Verified empirically: `grep -n "flag_regen_rate\|> 0.08"` confirms `self.regen_rate > 0.08` at line 505.
- Tests: `test_flag_regen_rate_above_threshold` + `test_flag_regen_rate_below_threshold` PASS.
- Assessment: Correct fix. `> 8.0` on a `[0,1]` domain was logically dead code. Catch quality: HIGH — this would have silently suppressed all quality warnings during V1 sim cycling.

**Bug 3: datetime.utcnow deprecation**
- Issue: `datetime.utcnow()` deprecated in Python 3.12 (generates DeprecationWarning; removed in 3.14).
- Fix: Replaced with `datetime.now(timezone.utc)` at `t4_sim_cycling.py:1315`; `from datetime import datetime, timezone` at line 35.
- Verified empirically: `grep -n "utcnow"` returns no results; `datetime.now(timezone.utc)` confirmed at line 1315.
- Assessment: Correct fix. Timezone-aware datetime is the correct Python 3.12+ pattern.

All 3 bug catches are quality-positive findings. The `flag_regen_rate` catch is particularly significant — silent quality-gate suppression in a balance sim is a high-severity defect.

**Cite:** Discipline #11 (empirical verification of all 3 fixes at code-line level). INFO (bug catches are a quality-positive observation, not a finding against gamora).

---

### D10 — MIGRATION.md § v1.29 + star-lord follow-on flag — INFO (filed; compliant)

`simulation/MIGRATION.md § v1.29` (verified):

- Complete `T4SimRecord.to_dict()` field inventory: 12 required fields per REQUIRED_FIELDS constant in test file — identity (5) + tier outcomes (2) + compound gate (2) + scope metadata (2) + wave provenance (1). All fields documented.
- Star-lord cross-seam dependency documented: "star-lord action: create `export/wave4_schema_landed.sentinel` + add T4 sim cycling export table + ingest `simulation/output/wave4_sim_results_*.json`."
- Sentinel detection documented: gamora reads `src/reincarnated/export/wave4_schema_landed.sentinel` to detect star-lord schema landing; stub-write mode if absent.
- Integration handoff path clean: stub output at `simulation/output/wave4_sim_results_stub_{timestamp}.json` provides star-lord ingest source when sentinel-write dispatch completes.

Star-lord follow-on flag explicitly called out per dispatch out-of-scope note. Routes via KR (separate small dispatch).

**Cite:** ADR-004 (cross-seam schema change documented; star-lord follow-on gated correctly). ADR-006 (gamora does not touch export/ seam; star-lord authors actual schema change).

---

## Severity summary

| ID | Severity | Finding |
|---|---|---|
| I1 | INFO | Architectural alignment: fully aligned with SC-7 § 9 FULL framework + Block C scaffolding; methodology pattern named correctly per #30; B14.5 historical-median prohibition honored |
| I2 | INFO | Sub-gate 6 is a structural placeholder (action_trace not available from FightSummary); SC-7 § E1 threshold formula implemented correctly; calibration deferred to W5 per #18.2 — correct V1 stance |
| I3 | INFO | WARN-pattern PRESERVED: 193/193 PASS; all 5 module-level + 9 test-class count assertions PASS; 0 failures — first baseline established |
| I4 | INFO | Three in-flight bugs caught + fixed correctly; flag_regen_rate catch (> 8.0 → > 0.08) is highest-quality catch — would have silently suppressed quality warnings during V1 sim cycling |
| I5 | INFO | MIGRATION.md § v1.29 filed; star-lord follow-on flag correct; sentinel-detection stub-write pattern is correct stub pattern for concurrent dispatch coordination |

---

## Rationale

**PASS (not PASS-with-WARN):** No WARN conditions found in Wave 4 Track B implementation. All 6 sub-waves landed. SC-7 § 9 FULL methodology pattern consumed correctly. KPM bands sourced fresh (not B14.5 historical). Sub-gate 6 structural placeholder is the correct V1 stance given action_trace data unavailability — Discipline #18.2 explicitly defers calibration to post-baseline. BLOCK threshold not met by any finding.

**PASS on WARN-pattern:** 5/5 module-level count assertions match runtime values exactly. Test class `TestPostScriptEmpiricalCounts` passes all 9 tests. Zero mismatch. This is Track B's FIRST WARN-pattern PRESERVED establishment (Wave 4 = Track B baseline for future waves).

**PASS on Discipline #1 math-before-code:** math note present at `simulation/math/cycle-13-wave-4-sim-cycling-math-2026-05-27.md`; covers all sub-waves with methodology pattern + Tier routing thresholds + KPM band formula + sub-gate 6 scope_chain_breadth + compute budget + archive insertion.

**PASS on Discipline #1.1 resource-bounds:** compute budget constants declared at code-line level; <5MB peak memory; ~19 min wall-clock upper bound; M2 8GB not at risk.

**PASS on bug catches:** All 3 fixes are correct. `flag_regen_rate` threshold fix (> 8.0 → > 0.08) is the most consequential — it restores the quality-warning gate that was logically dead at the `[0,1]` domain. The catch quality reflects good empirical discipline.

**Cite:** Review Principles 1-5. ADR-002 (direct APPROVE — within-seam implementation; star-lord follow-on is separate seam dispatch; no Matt escalation required). ADR-004 (MIGRATION.md § v1.29 documented). ADR-006 (gamora does not touch export/ seam). Disciplines #1 / #1.1 / #1.2 / #11 / #18 / #18.2 / #26 / #30.

---

## Action

No blocking actions required.

- [ ] **KR (Wave 4 CLOSE — Track B):** Tag `jack-ryan(gate-2): PASS — Cycle 13 Wave 4 Track B gamora sim cycling`. Track B is CLOSED.
- [ ] **KR (star-lord follow-on dispatch — REQUIRED):** Small dispatch per MIGRATION.md § v1.29 flag: (1) create `src/reincarnated/export/wave4_schema_landed.sentinel`; (2) add T4 sim cycling export table; (3) ingest `simulation/output/wave4_sim_results_stub_*.json`. Routes separately per gamora MIGRATION.md and dispatch out-of-scope note.
- [ ] **KR (sub-gate 6 W5 enhancement flag):** action_trace instrumentation needed for actual per-0.5s burst measurement. Sub-gate 6 returns PASS unconditionally in V1; W5 must add action_trace data path. Note for Wave 5 dispatch scope.

---

## Next-action sequence for KR

1. **Wave 4 Track B CLOSED — PASS.** WARN-pattern PRESERVED (0 failures).
2. **Both Track A + Track B PASS — Wave 4 CLOSED.**
3. **Tag:** `jack-ryan(gate-2): bundled — Track A spec-driven gear gen PASS + Track B sim cycling PASS`.
4. **Route star-lord follow-on dispatch** (small; sentinel creation + export table + stub ingest; gates on star-lord completing before Wave 5 gamora archive consumption).
5. **Wave 5 dispatch** authoring: gauntlet sim PASS + initial mechanical season generation. Sub-gate 6 action_trace instrumentation scoped into Wave 5.
6. **Cycle 13 CLOSE** gated on Wave 5 gauntlet sim PASS.

---

## References

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/t4_sim_cycling.py` — empirically inspected (lines 1-450 + key sub-wave functions; 1315 total lines; all major structural elements verified)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/cycle-13-wave-4-sim-cycling-math-2026-05-27.md` — confirmed present; covers W4G.0-W4G.5; methodology pattern verbatim match
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` — § v1.29 verified (lines 69-247); T4SimRecord field inventory; star-lord follow-on flag; sentinel detection
- `/Users/admin/Games/reincarnated-engine/tests/test_cycle13_wave4_sim_cycling.py` — empirically inspected (91 tests; all PASS; REQUIRED_FIELDS constant at line 646; TestPostScriptEmpiricalCounts at line 855)
- Pytest run: `346 passed in 0.60s` (all 6 Cycle 13 wave test files; 193 Track B + 153 Track A; 0 regressions)
- Python import spot-check: 5/5 module-level count assertions verified via `len()` / direct value; SCOPE_CHAIN_BREADTH len=3 verified
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-3-gate-2-rocket-implementation.md` — Wave 3 Gate-2 PASS baseline
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-05-26-cycle-13-wave-4-sim-methodology-framework.md` — SC-7 FULL framework; § 9 consumed at implementation

---

**Signed:** jack-ryan (analyst / QA / quality guardian)
**Gate-2 verdict:** PASS
**Severity counts:** INFO=5 / WARN=0 / BLOCK=0
**WARN-pattern preservation status:** PRESERVED (193/193 PASS; 5/5 module-level + 9 test-class count assertions PASS; 0 failures — Track B first baseline established)
**Track B CLOSE status:** CLOSED — Wave 4 Track B complete; star-lord follow-on dispatch flagged; Wave 5 gauntlet sim PASS is next gate
