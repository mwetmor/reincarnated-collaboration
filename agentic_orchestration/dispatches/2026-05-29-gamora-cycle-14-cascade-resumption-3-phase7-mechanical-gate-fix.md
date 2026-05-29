# Dispatch — Gamora — Cycle 14 Cascade-Resumption-3 Phase 7 Mechanical Gate Fix (Option α)

**Date:** 2026-05-29
**From:** knight-rider (orchestrator)
**To:** gamora (engine simulation + spirit-guide seam — simulation/, spirit_guide/)
**Authority:**
- Matt 2026-05-29 cascade-resumption-3 authorization + Amendments 1-4 (hive-state clarification; KR auto-routes in-scope)
- Gamora Phase 7 mechanical gate investigation Verdict B (collab `0dcce25`) — genuine calibration issue; Option α fix recommended
- Pre-ratified per investigation dispatch § 3 (Verdict B → gamora seam-owner fix dispatch)
- Hive-mind decision-routing — gamora is Phase 7 + gauntlet sim seam-owner

**Pattern:** Pattern A-light follow-up patch (~1-2h implementation + math note + tests)
**R48.4 / R48.5 RETIRED per Amendment 3**
**Standalone dispatch this batch**

---

## 0. TL;DR

**Implement Option α from gamora investigation verdict:**

1. **Align Phase 7 bridge `pass_rate` measurement** to use `eligible_encounters_passed(cohort)` (the metric A2-1 Step 1 calibrated to via W-α6 24-cell `ENCOUNTER_COHORT_KPM_BAND` table)
2. **Recalibrate `P7_GAUNTLET_PASS_FLOOR`** to ~0.50 (matching `GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6 = 9/18`)
3. **Math note** at `reincarnated-engine/src/reincarnated/simulation/math/cascade-r3-phase7-mechanical-gate-alignment-2026-05-29.md` (Disc #1)

Bounded scope: `phase7_bridge._run_gauntlet_for_kit` + `phase7_verdict.P7_GAUNTLET_PASS_FLOOR`. Two-layer gate architecture is sound; this is alignment-correction not architectural change.

**Effort:** ~1-2h.

---

## 1. Required first reads

1. Your investigation note at `agentic_orchestration/gamora/notes/2026-05-29-cascade-r3-phase7-mechanical-gate-investigation.md` — Verdict B + causal chain + Option α recommendation
2. `reincarnated-engine/src/reincarnated/simulation/phase7_bridge.py`:
   - `_run_gauntlet_for_kit()` — legendary_config dict construction site (missing damage_scaling_path)
   - cohort midpoint calculation
3. `reincarnated-engine/src/reincarnated/simulation/phase7_verdict.py`:
   - `P7_GAUNTLET_PASS_FLOOR` constant (currently 0.70 against pass_rate)
4. `reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py`:
   - `run_gauntlet_sim()` damage_scaling_path derivation logic + '_fallback' path
   - `get_archetype_cohort_kpm_band()` — legacy COHORT_KPM_BAND vs W-α6 ENCOUNTER_COHORT_KPM_BAND
   - `eligible_encounters_passed(cohort)` measurement (the metric A2-1 Step 1 calibrated to)
   - `GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6 = 9/18` reference
5. A2-1 Step 1 gamora completion record at `agentic_orchestration/dispatches/2026-05-29-gamora-cycle-14-a2-1-step-1-synthetic-kit-kpm-recalibration.md` — synthetic kit magnitude calibration anchor + W-α6 measurement framework
6. `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.6.9 Path α V1 close-criterion (C1-C5 measurement vocabulary; C2 is gauntlet measurement)
7. Your AGENT_STATE.md at `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md`
8. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disc #1 + #2 + #11 + #42a + #45 LOAD-BEARING

---

## 2. Scope

### 2.1 Math note (Disc #1 BEFORE code change)

Author at `reincarnated-engine/src/reincarnated/simulation/math/cascade-r3-phase7-mechanical-gate-alignment-2026-05-29.md`:

- Current Phase 7 bridge measurement: `pass_rate = encounters_passed / total_encounters`; threshold `P7_GAUNTLET_PASS_FLOOR = 0.70`; falls back to legacy COHORT_KPM_BAND when damage_scaling_path missing
- A2-1 Step 1 calibration anchor: `eligible_encounters_passed(cohort) >= 9` against W-α6 24-cell ENCOUNTER_COHORT_KPM_BAND
- Alignment correction: change Phase 7 bridge to read `eligible_encounters_passed(cohort)` instead of computing pass_rate; threshold becomes `>= 9/18` equivalent (0.50)
- Math: 9/18 = 0.50 (W-α6 calibration anchor) — matches GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6
- Cohort midpoint calculation unchanged at high level (mean of per-kit eligible_encounters_passed values per cohort); midpoint band threshold becomes 0.50-derived
- Expected behavior post-fix: synthetic kit KPMs (71-446 span) measured against W-α6 ENCOUNTER_COHORT_KPM_BAND (24 cells per cohort) produce non-zero pass_rate; cohort midpoints produce meaningful values; Phase 7 mechanical gate fires per Path α v1 close-criterion intent

### 2.2 Fix 1 — Phase 7 bridge `pass_rate` alignment

At `simulation/phase7_bridge.py` `_run_gauntlet_for_kit()` and downstream pass_rate measurement site:

**Current behavior:** Constructs legendary_config dict; passes to `run_gauntlet_sim()`; gauntlet sim derives `damage_scaling_path` from config/kit OR falls back to `'_fallback'`; under `'_fallback'`, uses legacy narrow `COHORT_KPM_BAND` (~75 KPM); kits with KPM outside the band produce in_band=False; `encounters_passed(cohort) = 0`; `pass_rate = 0.0`.

**Required post-fix behavior:** Phase 7 bridge measures kit performance via `eligible_encounters_passed(cohort)` (the W-α6 ENCOUNTER_COHORT_KPM_BAND-derived metric A2-1 Step 1 calibrated against). Threshold semantically equivalent to GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6 = 9/18 = 0.50.

**Implementation approach** (gamora elects per simpler-implementation):
- **Option α.1 — Plumb damage_scaling_path through legendary_config:** Add damage_scaling_path key to legendary_config in `_run_gauntlet_for_kit()`; gauntlet sim uses this to read W-α6 ENCOUNTER_COHORT_KPM_BAND (NOT '_fallback'); pass_rate then meaningful
- **Option α.2 — Direct alignment:** Change Phase 7 bridge to call `eligible_encounters_passed(cohort)` directly (bypass damage_scaling_path derivation); ENCOUNTER_COHORT_KPM_BAND-based measurement

Gamora elects per simpler-implementation. KR ratifies either.

### 2.3 Fix 2 — Recalibrate `P7_GAUNTLET_PASS_FLOOR`

At `simulation/phase7_verdict.py`:

**Current:** `P7_GAUNTLET_PASS_FLOOR = 0.70` (against legacy pass_rate ratio)

**Required post-fix:** `P7_GAUNTLET_PASS_FLOOR = 0.50` (matching GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6 = 9/18 — W-α6 calibration anchor)

If Option α.1 elected, the threshold may stay at 0.70 against ratio (eligible_encounters_passed / 18 = ratio; 9/18 = 0.50; verify gamora math note for correct threshold).

### 2.4 Tests

- Update existing Phase 7 tests where applicable (per Disc #11 grep + smoke verification)
- New test: kit with A2-1 Step 1 calibrated KPM passes Phase 7 mechanical gate (verify the fix unblocks expected behavior)
- New test: kit with sub-threshold KPM FAILS Phase 7 mechanical gate (gate still binding)
- Verify existing tests PASS (no regression)

### 2.5 Disc #42a context-dependent-semantics flag

Pass_rate / eligible_encounters_passed measurement-context-dependent-semantics pattern (Instance 2 sub-case): document in completion record for jack-ryan + gandalf canonical-write consideration at Cycle 14 wave-close. NOT in S6a-FIX-PHASE7 scope; ratification candidacy data point.

---

## 3. Pre-ratified contingent decisions

| Decision point | Pre-ratified action |
|---|---|
| Option α.1 vs α.2 implementation | Gamora elects per simpler-implementation; KR ratifies either |
| Math note threshold derivation | Per Disc #1 math note (gamora authored before code change); KR ratifies |
| Recalibration threshold precise value | Gamora math note derives; KR ratifies (~0.50 baseline per W-α6 anchor) |
| Cohort midpoint calculation impact | Verify midpoint semantics preserve under new measurement; gamora elects if alternative needed; surface only if architectural alternative surfaces |

---

## 4. Acceptance criteria

### 4.1 Math note authored (Disc #1)

- Math note at `reincarnated-engine/src/reincarnated/simulation/math/cascade-r3-phase7-mechanical-gate-alignment-2026-05-29.md`
- Captures current behavior + A2-1 Step 1 calibration anchor + alignment correction math

### 4.2 Phase 7 bridge alignment (Disc #11 grep)

- Either damage_scaling_path plumbed through legendary_config (Option α.1) OR direct eligible_encounters_passed measurement (Option α.2)
- pass_rate / threshold semantic alignment with W-α6 calibration anchor verified via grep

### 4.3 Threshold recalibrated

- P7_GAUNTLET_PASS_FLOOR aligned with W-α6 (0.50 baseline OR per gamora math note derivation)

### 4.4 Tests

- New positive test (A2-1 Step 1 calibrated kit passes Phase 7 mechanical gate)
- New negative test (sub-threshold kit fails)
- All existing tests PASS (no regression)

### 4.5 Smoke verification (Disc #2)

- Re-run S6a smoke (smoke=False; small sample) — verify Phase 7 produces non-zero shipped_worthy
- Compare against pre-fix shipped_worthy=0 result; confirm fix effective

### 4.6 Tag

- Engine commit + tag (gamora prefix per CLAUDE.md: e.g., `gamora/v2.17-cascade-r3-phase7-mechanical-gate-fix-1`)

---

## 5. Out-of-scope

- Phase 7 cohesion gate (cohesion_judge_confidence-based; S5b closed; BINDING)
- Phase 7 mechanical gate ARCHITECTURE changes (two-layer gate sound per investigation)
- Substrate library modifications
- Gauntlet variant enumeration changes (S2 closed)
- Wave A / F-C / Wave B implementation changes (S5 + S5b closed)
- A/B comparison protocol
- S6c A2-1 RE-FIRE-3 full season fire itself (post-fix)
- Recognition Record Amendment 3 H1 variant inheritance investigation (separable axis; H1 fires at A2-1 RE-FIRE-3)

---

## 6. Surface to knight-rider conditions

| Condition | Trigger | Action |
|---|---|---|
| **Math note reveals deeper Phase 7 architectural concern** | Beyond alignment-correction | Halt + surface to KR — gandalf design-spec-as-math handoff candidate |
| **Cohort midpoint calculation semantics shift unexpectedly** | New measurement changes midpoint interpretation | Document at completion record; surface to KR if architectural |
| **Smoke verification HALTS again** | Phase 7 still produces shipped_worthy=0 post-fix | Halt + surface to KR — different root cause; new investigation |
| **Disc #42a framing-audit catch** | Q1-Q6 surfaces pre-imposed assumption mid-fix | Halt + surface to KR |
| **Effort exceeds ~3h** | Implementation complexity significantly beyond ~1-2h | Surface to KR — scope reconsideration |

---

## 7. Engineering disciplines composition

| Discipline | Application |
|---|---|
| **Disc #1 math-before-code** | Math note authored BEFORE code change per § 2.1 |
| **Disc #2 smoke-test before tag** | § 4.5 smoke re-fire verification |
| **Disc #11 empirical inspection** | § 4.2-4.5 acceptance gates |
| **Disc #42a framing-audit Q1-Q6** | LOAD-BEARING — Instance 2 sub-case (measurement-context-dependent-semantics); document for jack-ryan + gandalf canonical-write at Cycle 14 wave-close |
| **Disc #45 vocabulary lock** | Aligned measurement vocabulary (eligible_encounters_passed) per W-α6 anchor |
| **Disc #48 RETIRED per Amendment 3** | No pre-flight vm_stat gate |
| **Recognition → empirical validation → commit** | Recognition: gamora investigation Verdict B; Validation: § 4 acceptance + smoke re-fire; Commit: gamora auto-commits per CLAUDE.md addendum |

---

## 8. Deliverables

1. **Math note** at `reincarnated-engine/src/reincarnated/simulation/math/cascade-r3-phase7-mechanical-gate-alignment-2026-05-29.md` (Disc #1 BEFORE code)
2. **Engine commit(s)** — phase7_bridge.py + phase7_verdict.py + tests + tag (gamora prefix per CLAUDE.md)
3. **MIGRATION.md entry** at `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (if cross-seam impact; likely minimal — both files are gamora seam)
4. **Completion record appended to this dispatch file** — captures: (a) math note path; (b) Option α.1 vs α.2 election + implementation evidence; (c) threshold recalibration; (d) tests results; (e) smoke re-fire results (Phase 7 mechanical gate fires; shipped_worthy > 0); (f) Disc #42a Instance 2 sub-case context; (g) any surface-to-KR findings
5. **AGENT_STATE.md checkpoint** at `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` — Phase 7 fix CLOSED + S6c queued
6. **Auto-commit per CLAUDE.md team commit + push discipline addendum 2026-05-25** — work-products of authorized cascade-resumption-3 work; push REQUIRES Matt-explicit-auth (do NOT push)

---

## 9. Sign-off

**Authored:** knight-rider per Matt 2026-05-29 Amendment 4 hive-state clarification (KR auto-routes in-scope) + investigation dispatch § 3 pre-ratified Verdict B routing

**Gamora session-start protocol:**
1. Onboard via § 1 required first reads (your own investigation note + Phase 7 code surfaces + A2-1 Step 1 calibration anchor)
2. Apply Disc #42a framing-audit Q1-Q6 at dispatch consumption — Instance 2 sub-case awareness LOAD-BEARING (pass_rate semantic alignment)
3. Author § 2.1 math note BEFORE code (Disc #1)
4. Execute § 2.2 + § 2.3 + § 2.4 + § 2.5
5. Apply § 4 acceptance gates INCLUDING § 4.5 smoke re-fire (verify Phase 7 produces non-zero shipped_worthy)
6. Surface per § 6 if triggered
7. Author § 8 deliverables
8. Auto-commit per CLAUDE.md addendum

**KR next-step on close:** verify § 4 acceptance + § 8 deliverables INCLUDING smoke re-fire shows Phase 7 mechanical gate produces non-zero shipped_worthy; route S6c dispatch (A2-1 RE-FIRE-3 full season_001 production).

**Cascade trajectory:** Phase 7 fix → S6c (A2-1 RE-FIRE-3) → A2-2 → A2-7 + D13 parallel-fire → Cycle 14 v1 MVP D9 close.

**Signed:** knight-rider (orchestrator)

---

## Completion record

**Completed:** 2026-05-29
**Author:** gamora
**Tag:** `gamora/v2.17-cascade-r3-phase7-mechanical-gate-fix-1`

### (a) Math note path + key derivation

`/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/cascade-r3-phase7-mechanical-gate-alignment-2026-05-29.md`

Key derivation:
- A2-1 Step 1 calibrated to `eligible_encounters_passed(cohort) >= GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6 = 9`
- As fraction: `9 / 18 = 0.50` (18 encounters per cohort, full mode)
- Recalibrated threshold: `P7_GAUNTLET_PASS_FLOOR = 0.50` (strict greater-than; > 9/18)
- Boundary condition: `pass_rate = 9/18 = 0.50` FAILS strict floor (requires > 0.50 = at least 10/18)

### (b) Option α.1 vs α.2 election + implementation evidence

**Option α.2 elected (corrected implementation).** Option α.1 (plumb damage_scaling_path) was infeasible: `ARCHETYPE_COHORT_KPM_BAND` is `None` at runtime (Cycle 15 deferred); would still fall through to legacy `COHORT_KPM_BAND`.

**Implementation evidence (phase7_bridge.py `_run_gauntlet_for_kit`):**

First-pass α.2 used `quality_report.eligible_encounters_in_band` — discovered via empirical probe that this is the SUM across ALL 4 cohorts (gauntlet always runs all 4 regardless of `config['cohorts']` annotation). Empirical evidence: 1-kit probe showed aggregate=43 vs per-target-cohort=15.

Corrected α.2: call `w5g0_gauntlet_setup` + `w5g1_gauntlet_execution` directly to access `GauntletKitResult` objects, then:
```python
enc_passed = kit_result.eligible_encounters_passed(gauntlet_archetype)
```
This reads per-cohort eligible count via `ENCOUNTER_COHORT_KPM_BAND` — the W-α6 calibration-aligned measurement.

### (c) Threshold recalibration

`P7_GAUNTLET_PASS_FLOOR`: `0.70` → `0.50`
`_P7_PASS_FLOOR_EXPECTED` (postscript assertion): `0.70` → `0.50`
Math note: § 3.2 (Option T1 — strict greater-than preserved; boundary kit at exactly 9/18 fails)

### (d) Test results

**New tests:**
- `test_G_P7_9_mechanical_gate_positive`: 10/18 and 12/18 PASS recalibrated floor 0.50; boundary 9/18 correctly FAILS strict floor. PASS.
- `test_G_P7_10_mechanical_gate_negative`: 8/18 and 0/18 FAIL recalibrated floor 0.50; gate remains binding. PASS.

**Updated existing tests (G-P7-6 + G-P7-7):** Floor test values updated to use fractions below/at 0.50 (8/18, 0.50) instead of pre-fix values (0.65, 0.70, 0.60) which now pass under new floor.

**All Phase 7 bridge tests: 11/11 PASS.**

**Pre-existing failures (confirmed not regressions):** 13 failures in `test_cycle13_wave5_gauntlet_sim.py` + `test_cycle13_wave5_season_generation.py` confirmed pre-existing via `git stash` + re-test (same failures on HEAD without fix). These are W-α6 architecture mismatches in Cycle 13 tests not yet updated.

### (e) S6a smoke re-fire results

**Pre-fix (S6a investigation telemetry):**
```json
{"kits_evaluated": 18, "kits_shipped_worthy": 0, "kits_held_mechanical": 18,
 "cohort_midpoints": {"damage": 0.0, "defensive": 0.0278, "control": 0.85, "support": 0.85, "hybrid": 0.85}}
```

**Post-fix (S6a re-fire 2026-05-29):**
```json
{"kits_evaluated": 18, "kits_shipped_worthy": 12, "kits_held_cohesion": 0, "kits_held_mechanical": 6,
 "cohort_midpoints": {"damage": 0.8333, "defensive": 0.1111, "control": 0.85, "support": 0.85, "hybrid": 0.85},
 "acceptance_rate": 0.6667, "wall_clock_seconds": 3.54}
```

Phase 7 mechanical gate FIRES. shipped_worthy: 0 → 12. Cohort midpoints correctly in [0,1] range.
6 held-mechanical kits: failing either floor (pass_rate ≤ 0.50) or band check (defensive kits with low midpoint 0.1111 face tight band). Gate is binding and meaningful.

### (f) Disc #42a Instance 2 sub-case context (pass_rate semantic alignment)

**Pattern:** `pass_rate` — same field name, context-dependent semantics.

| Context | Measurement | Band type | Result |
|---|---|---|---|
| Phase 7 bridge (pre-fix) | `encounters_passed / 18` via legacy `in_band` flag | COHORT_KPM_BAND (~75 KPM ±15%) | ≈ 0.0 (near-zero for synthetic kits) |
| A2-1 Step 1 calibration | `eligible_encounters_passed >= 9` | ENCOUNTER_COHORT_KPM_BAND (per-enc-type) | GAUNTLET_PASS: 18/18 |
| Phase 7 bridge (post-fix) | `eligible_encounters_passed(gauntlet_archetype) / 18` | ENCOUNTER_COHORT_KPM_BAND (per-enc-type) | 0.0–1.0 range; calibration-aligned |

Flagged for jack-ryan + gandalf canonical-write consideration at Cycle 14 wave-close. Same-name field with context-dependent semantics is a recurrent pattern (Disc #42a Instance 2). This specific sub-case: A2-1 calibration used a boolean gate criterion (`gauntlet_pass = eligible >= 9`) while Phase 7 used a ratio computation — both named "pass" but via different code paths.

**Additional sub-case discovered during implementation:** `quality_report.eligible_encounters_in_band` is an ALL-4-cohort aggregate (not per-cohort). The field name suggests "eligible encounters in band" without scope qualification. Naming clarification opportunity for Cycle 15 or canonical-write.

### (g) Surface-to-KR findings

**No § 6 surface triggers fired:**
- Math note did not reveal deeper architectural concern; Two-layer gate design confirmed sound.
- Cohort midpoint semantics post-fix are correct (fractions in [0,1] range; empirical values meaningful).
- Smoke re-fire PASSED (shipped_worthy = 12 > 0).
- Disc #42a Q1-Q6 clean (no framing creep; causal chain traceable; scope bounded).
- Effort within ~2h estimate.

**One finding for KR awareness (not a surface trigger; informational):**
`gauntlet_sim.w5g1_gauntlet_execution` always runs all 4 `COHORT_ARCHETYPES` regardless of `config['cohorts']` annotation. The `cohorts` key in legendary_config is metadata only — it does NOT filter the cohort execution loop. This means:
- `quality_report.eligible_encounters_in_band` = sum across all 4 cohorts for any call
- Phase 7 bridge now bypasses `run_gauntlet_sim()` in favor of direct `w5g0+w5g1` access
- No architectural change needed (existing behavior is correct for full gauntlet; Phase 7 just needs per-cohort access)

This is informational context for S6c routing + any future Phase 7 changes. Not a blocking concern.

### MIGRATION.md

`§ v1.61` filed in `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`:
- `_run_gauntlet_for_kit` measurement semantics change
- `P7_GAUNTLET_PASS_FLOOR` recalibration
- Cross-seam impact: minimal (gamora-seam files only; `gauntlet_pass_rate` writeback values now correct fractions)

### S6c readiness

Phase 7 mechanical gate fix COMPLETE. S6c (A2-1 RE-FIRE-3 full season_001 production) is unblocked. Phase 7 smoke re-fire confirms the gate fires and produces meaningful shipped_worthy count. Cohort midpoints are empirically calibrated from base kit pass_rates. KR can route S6c dispatch.
