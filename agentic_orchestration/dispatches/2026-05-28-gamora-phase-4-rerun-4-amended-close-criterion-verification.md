# DISPATCH — Gamora Phase 4 RE-RUN-4: Amended Close-Criterion Verification (7-Profile Sweep)

**Authored:** 2026-05-28 (post-freeze hive-mind re-entry; Mode A item 3)
**Author:** knight-rider (Cycle 14 Mode A hive-mind orchestrator)
**Recipient:** gamora (simulation seam; bounded_viability_validation + t4_sim_cycling)
**Pattern:** Pattern A-light (fire sweep + attest telemetry + brief report)
**Expected effort:** ~30 min (sweep ~80s wall + read + attestation)
**Status:** PENDING — fires on receipt
**Authority:** Matt 2026-05-28 adjudication lock + KR Mode A charge

---

## 0. CONTEXT (read first — 3 min)

Mode A Dispatch 2 (gamora R3 forensic + hotfix) closed at engine `00b7f02` + tag `gamora/v2.9-r3-t2-zero-kpm-hotfix-1` + collab `9d30581`. BVV anchor verified: T1+T2+T3+T5 ALL PASS. Root cause was **BVV harness band-reject artifact** (KR's preliminary deterministic-zeroing-bug intuition refuted; initial gamora SC2 BASE-under-calibration diagnosis also refuted); hotfix landed in `gauntlet_sim.py` (T1 routing migration + ENCOUNTER_COHORT_KPM_BAND upper-bound recalibration). BASE values preserved (no cross-seam impact).

**This dispatch verifies the hotfix holds across the 7-profile sweep** (low / mid / max_a / max_b / mixed_v1 / mixed_v2 / mixed_v3). BVV anchor PASS at single profile is necessary but not sufficient — Phase 4 RE-RUN-3 also passed some profiles at single targets but failed compound. The 7-profile sweep is the actual close-criterion measurement.

---

## 1. THE TASK

**Fire Phase 4 RE-RUN-4 sweep against current engine state (`00b7f02`).** Same shape as Phase 4 RE-RUN-3 — 7-profile multi-dim sweep over kits × encounter_types × investment_levels × T4_variants. Same sweep harness; only the hotfix changes the band-reject behavior.

**Acceptance:**
- **T1 (DPS variance):** PASS at BVV anchor + each of 7 profiles (cross-path parity within threshold; no Infinity values indicate complete-path-zero, but check each)
- **T2 (zero-KPM count):** PASS at BVV anchor + each of 7 profiles (zero cells across all kits × encounter types)
- **T3 (saturation):** PASS structural at BVV anchor + each of 7 profiles (ceiling removed)
- **T5 (floor):** PASS 0 violations at BVV anchor + each of 7 profiles
- **T4 (specialization):** MEASURED FOR RECORD (Cycle 16+ deferred via BC axis expansion); does NOT gate close

If T1+T2+T3+T5 all PASS across BVV anchor + 7 profiles → **Cycle 14 v1 MVP amended close-criterion satisfied.**

If any T1/T2/T3/T5 FAILS at any profile → identify which profile + which target + which kit-cell pattern; surface back to KR for diagnosis + potential hotfix iteration (R3-prime).

---

## 2. EXPECTED INVESTIGATION SHAPE (Pattern A-light)

### 2.1 Fire the sweep

Use the same sweep harness as Phase 4 RE-RUN-3 (per `cycle-14-wave-5-season-001/w-alpha-7-plus-phase-4-rerun-3-two-layer-t4-sweep-telemetry.json` invocation pattern). Output telemetry to `cycle-14-wave-5-season-001/w-alpha-7-plus-phase-4-rerun-4-amended-close-criterion-telemetry.json` (or follow your existing naming convention).

**Pre-flight (Discipline #47 R47.5 + #1.1):** `vm_stat` confirm > 1 GB free before firing. Sweep is expected to allocate similar to RE-RUN-3 — ~80s wall-time + working set similar magnitude. If memory pressure is high, surface to KR.

### 2.2 Telemetry attestation

After sweep returns, attest:

1. **Per-profile compound_pass:** does each profile show `compound_pass=True` under the AMENDED close-criterion (T1+T2+T3+T5; T4 not required)? The raw `compound_pass` field in telemetry may still consider T4 — IF SO, build a derived close-criterion check that EXCLUDES T4 specialization and report per-profile derived-compound-pass.

2. **Per-target metrics:** report T1, T2, T3, T4 (measured-for-record), T5 metrics per profile.

3. **BVV anchor re-verify:** baseline `bounded-viability-validation-baseline-2026-05-28.json` should be re-fired post-hotfix (gamora may have already done this at hotfix close; verify still PASS for record).

4. **Strip-and-ship 18/18 kits ship:** verify still holds.

5. **Cycle 16+-relevant T4 data:** record T4 metric per profile + per-kit peak distribution for the Cycle 16+ BC axis expansion baseline (this becomes pre-Cycle-16 evidence for the BC axis expansion design call).

### 2.3 Report format

Append a "## Completion record" section to this dispatch with:

1. **VERDICT** — single line: "Phase 4 RE-RUN-4 verifies amended close-criterion T1+T2+T3+T5 PASS across all 7 profiles at engine `00b7f02`" (or partial-pass with specifics; or FAIL with diagnosis)
2. **Per-profile table** — T1 / T2 / T3 / T4 (measured) / T5 metrics
3. **Derived-compound-pass per profile** — under amended criterion (T1+T2+T3+T5; T4 measured-for-record)
4. **BVV anchor verification** — still PASS confirmation
5. **Telemetry path** — output JSON location
6. **Pre-Cycle-16 T4 baseline data** — per-profile T4 specialization metric + per-kit peak distribution (for future BC axis expansion design call)
7. **Any anomalies** — kits or profiles with unexpected behavior; surface to KR if action is needed
8. **Auto-commit + tag** per CLAUDE.md addendum; tag `gamora/v2.9-r3-phase-4-rerun-4-verification-1` (or your seam convention)

---

## 3. OUT OF SCOPE

- ❌ Any code change (hotfix landed at Mode A Dispatch 2; this is verification-only)
- ❌ Any new BASE / encounter HP / fight-engine tune
- ❌ Cycle 16+ BC axis expansion impl
- ❌ Two-layer T4 architectural amendment
- ❌ R1 / R2 / R4 work (all adjudicated)
- ❌ jack-ryan Gate-2 review (Mode A Dispatch 5)
- ❌ Cycle 14 closure record (Mode A Dispatch 6)
- ❌ Pushing without KR coordination

---

## 4. RISKS + COMPLICATIONS

- **Profile-specific FAIL surface:** if hotfix works at BVV anchor but a specific profile (e.g., mixed_v1 / mixed_v3) still shows Infinity cross-path parity OR T2 zero-KPM in a sub-cluster, the band recalibration may be insufficient for that profile's investment configuration. Surface to KR for diagnosis; potential R3-prime hotfix iteration scope: same `gauntlet_sim.py` band table, profile-aware band tuning.
- **T4 measurement at the record:** record T4 metric per profile in your completion record EVEN THOUGH T4 doesn't gate close. This data becomes pre-Cycle-16 evidence for the BC axis expansion design call (substrate signal for `damage_element_profile` + other candidate axes per c-hybrid § 1.1 amendment).
- **Compound_pass field in telemetry may not match amended criterion:** the raw `compound_pass` field probably ANDs all 5 targets. Build derived-compound-pass for amended criterion (T1+T2+T3+T5 only; T4 excluded). Surface the derived value in your completion record.
- **Discipline #47 candidate active:** R47.4 single-seam sequencing; no parallel work fires while you run.
- **Discipline #1.1 pre-fire resource-bounds projection:** expected sweep allocation < 1 GB (~RE-RUN-3 working set); `vm_stat` pre-flight; abort if memory unsafe.

---

## 5. URGENCY + SEQUENCING

**Fires THIRD in KR Mode A dispatch sequence — verifies BLOCKING-close item delivered by Dispatch 2.** If this passes → KR fires Mode A Dispatch 4 (gandalf canonical close-criterion capture) → Mode A Dispatch 5 (jack-ryan Gate-2) → Mode A Dispatch 6 (Cycle 14 closure record + Matt surface).

If this FAILS → KR diagnoses + iterates R3-prime hotfix dispatch; Cycle 14 close blocked until amended criterion passes 7-profile.

**Single-seam sequencing per R47.4 preserved.**

---

**KR signature:** authored per Matt 2026-05-28 adjudication lock + KR Mode A hive-mind charge + Disc #47 R47.4 single-seam sequencing + Disc #1.1 pre-fire vm_stat check + R3 hotfix verification gate. This is the cheapest empirical refutation of "does the amended close-criterion hold across 7 profiles?" — sweep + telemetry attestation in ~30 min.

---

## Completion record

(gamora appends here)
