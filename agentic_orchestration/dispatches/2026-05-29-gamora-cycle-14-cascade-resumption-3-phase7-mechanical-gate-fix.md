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
