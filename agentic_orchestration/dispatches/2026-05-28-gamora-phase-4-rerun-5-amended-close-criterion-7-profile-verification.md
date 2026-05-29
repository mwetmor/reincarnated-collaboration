# DISPATCH — Gamora Phase 4 RE-RUN-5: Amended Close-Criterion 7-Profile Verification (Phase A1 Dispatch 3)

**Authored:** 2026-05-28 (Mode A Phase A1 Dispatch 3; post gamora R3-prime band lower-bound recalibration)
**Author:** knight-rider (Cycle 14 Mode A hive-mind orchestrator)
**Recipient:** gamora (simulation seam; bounded_viability_validation + unified_calibration_loop sweep harness)
**Pattern:** Pattern A-light (fire sweep + attest telemetry + brief report)
**Expected effort:** ~20-30 min (sweep ~80-100s wall + read + attestation)
**Status:** PENDING — fires on receipt
**Authority:** Matt 2026-05-28 A1 election lock + KR Mode A 2-phase charge + Phase A1 sequence

---

## 0. CONTEXT (read first — 3 min)

Phase A1 sequence status:
- ✅ **Dispatch 1 (T1 base-context amendment)** — engine `20dde52` + `0ac79a0` + tag `gamora/v2.10-t1-base-context-amendment-1` + collab `bd7f6f3`. Shape I (flag-gated T1 sub-pass); BVV anchor T1=1.1442 PASS; compound_pass(A1)=True
- ✅ **Dispatch 2 (R3-prime band lower-bound recalibration)** — engine `854e94a` + `5eaf800` + tag `gamora/v2.11-r3-prime-band-lower-bound-1` + collab `4e42385`. Shape L-I (uniform lower bound = global-min × 0.85); 6 encounter types recalibrated (scope extension from 4 to 6 per empirical finding); Disc #12 Epoch Break C declared; BVV anchor PASS on disk
- 🔥 **Dispatch 3 (THIS DISPATCH)** — Phase 4 RE-RUN-5 7-profile sweep verification
- ⏳ **Dispatch 4** (gandalf canonical close-criterion capture + C1-C5 rename)
- ⏳ **Dispatch 5** (jack-ryan Gate-2 wave-close + Disc #42/43/47 ratifications)
- ⏳ **Dispatch 6** (KR Path α v1 closure record + Wave 5 cascade entry pre-scope)

**KR Disc #42 cheapest-empirical-refutation (post-Dispatch-2 BVV anchor verification):**

On-disk BVV baseline file (`cycle-14-wave-5-season-001/bounded-viability-validation-baseline-2026-05-28.json`; run_at 2026-05-29T03:10:26 UTC) confirms:
- compound_pass=True (under amended close-criterion 4/4)
- T2 metric=0 / zero count=0 / violation cells=[]
- wis_02/mini_boss: kit_kpm=65.934 / cohort_median=93.75 / ratio=0.703 / is_zero=False

Your Dispatch 2 completion record noted "BVV anchor T2=1 (wis_02/mini_boss genuine zero — pre-existing)" — this appears to be an intermediate-state mis-report; the on-disk file shows PASS. KR has logged the meta-observation for jack-ryan Gate-2 awareness (not a separate canonical instance; reinforces the existing four-instance Disc #42 case).

---

## 1. THE TASK

**Fire Phase 4 RE-RUN-5 sweep against current engine state (`5eaf800`).** Same shape as Phase 4 RE-RUN-4 — 7-profile multi-dim sweep over kits × encounter_types × investment_levels × T4_variants. Both prior amendments (Dispatch 1 + Dispatch 2) now active:
- T1 measured at base-context (DDA off) per Dispatch 1 Shape I sub-pass
- Band lower bounds at global-min × 0.85 (L-I uniform; 6 encounter types) per Dispatch 2

Per your Dispatch 1 attestation: *"Phase 4 sweep coordination: RE-RUN-5 (Mode A Dispatch 3) will pick up the amendment automatically — 2 gauntlets per profile (DDA-active for T2/T3/T4/T5; base-context for T1). No additional wiring needed."*

**Acceptance criterion (amended close-criterion 4/4):**
- **T1 (base-context, cross-path DPS variance):** PASS at BVV anchor + each of 7 profiles
- **T2 (zero-KPM count):** PASS at BVV anchor + each of 7 profiles (0 zero cells)
- **T3 (saturation structural):** PASS at BVV anchor + each of 7 profiles
- **T5 (floor 0 violations):** PASS at BVV anchor + each of 7 profiles
- **T4 (Secondary T4 specialization):** MEASURED FOR RECORD only (Cycle 16+ deferred via BC axis expansion); does NOT gate close

If T1+T2+T3+T5 all PASS across BVV anchor + 7 profiles → **Path α v1 closure ENGINE READINESS GATE satisfied.** KR fires Dispatch 4 (gandalf canonical close-criterion capture).

If any T1/T2/T3/T5 FAILS at any profile → surface to KR with framing-audit Q1/Q2/Q3 applied to the failure mode BEFORE assuming production-layer cause (per Matt surface-to-Matt protocol).

---

## 2. EXPECTED INVESTIGATION SHAPE (Pattern A-light)

### 2.1 Fire the sweep

Use the same sweep harness as Phase 4 RE-RUN-4 (per `unified_calibration_loop.py` Phase 4 sweep code path). Output telemetry to `cycle-14-wave-5-season-001/w-alpha-7-plus-phase-4-rerun-5-amended-close-criterion-7-profile-telemetry.json` (or follow your existing naming convention).

**Pre-flight (Disc #47 R47.5 + #1.1):** `vm_stat` confirm > 1 GB free before firing. Sweep expected to allocate similar to RE-RUN-4 — ~80-100s wall + working set similar magnitude. If memory pressure is high, surface to KR.

### 2.2 Telemetry attestation

After sweep returns, attest:

1. **Per-profile compound_pass(A1):** does each of the 7 profiles show compound_pass=True under the AMENDED close-criterion (T1-base + T2-all-profiles + T3 + T5 = 4/4; T4 NOT required)? Use the `compound_pass` field from `harness_parameters` post-Dispatch-1 amendment (which reflects A1 4/4 criterion per Dispatch 1 SHIFT B).
2. **Per-target metrics:** report T1 (base-context) / T2 / T3 / T4 (measured-for-record) / T5 metrics per profile.
3. **BVV anchor re-verify:** baseline still PASS confirmation (matches on-disk file at run_at 2026-05-29T03:10:26 UTC).
4. **Strip-and-ship 18/18 kits ship:** verify still holds.
5. **Pre-Cycle-16 T4 baseline data:** record T4 metric per profile + per-kit peak distribution for the Cycle 16+ BC axis expansion design call.

### 2.3 Report format

Append a "## Completion record" section to this dispatch with:

1. **VERDICT** — single line: "Phase 4 RE-RUN-5 verifies amended close-criterion T1-base+T2+T3+T5 PASS across all 7 profiles at engine `5eaf800` + post-Dispatch-1/2 state" (or partial-pass with specifics; or FAIL with diagnosis + framing-audit Q1/Q2/Q3 applied)
2. **Per-profile table** — T1 (base) / T2 / T3 / T4 (measured) / T5 metrics + compound_pass(A1) verdict
3. **BVV anchor verification** — still PASS confirmation (matches on-disk file)
4. **Telemetry path** — output JSON location
5. **Pre-Cycle-16 T4 baseline data** — per-profile T4 specialization metric + per-kit peak distribution (for BC axis expansion design call)
6. **Any anomalies** — kits or profiles with unexpected behavior; surface to KR if action is needed
7. **Auto-commit + tag** per CLAUDE.md addendum; tag `gamora/v2.11-r3-phase-4-rerun-5-verification-1` (or your seam convention)

---

## 3. OUT OF SCOPE

- ❌ Any code change (Dispatches 1+2 land the amendments; this is verification-only)
- ❌ Any new BASE / encounter HP / fight-engine tune
- ❌ Cycle 16+ BC axis expansion impl
- ❌ Two-layer T4 architectural amendment
- ❌ R1 / R2 / R4 work (all adjudicated)
- ❌ Canonical close-criterion capture (Phase A1 Dispatch 4; gandalf)
- ❌ Jack-ryan Gate-2 review (Phase A1 Dispatch 5)
- ❌ Path α v1 closure record (Phase A1 Dispatch 6; KR — per ITEM 2 amendment)
- ❌ Wave 5 production cascade (Phase A2; post Matt 3-gate surface)
- ❌ Pushing without KR coordination

---

## 4. RISKS + COMPLICATIONS

- **Profile-specific FAIL surface:** if any profile (especially max_b / mixed_v1 / mixed_v3 — those NOT covered by Dispatch 2's single-profile smoke at low/mid/max_a) still shows T2 FAIL or T1 FAIL at base-context, the recalibration or T1 amendment may be insufficient for that profile's composition. Surface to KR for diagnosis; potential R3-prime-prime hotfix iteration scope.
- **T1 base-context verification:** Dispatch 1 attests Phase 4 sweep picks up the amendment automatically (2 gauntlets per profile). VERIFY this is in fact happening at sweep fire — check that `t1_measurement_context` field appears in per-profile results AND that T1 metric reflects base-context (DDA-off) measurement.
- **T4 pre-Cycle-16 baseline data quality:** record T4 metric per profile EVEN THOUGH T4 doesn't gate close. This data becomes pre-Cycle-16 evidence for the BC axis expansion design call (substrate signal for `damage_element_profile` + other candidate axes per c-hybrid § 1.1 amendment).
- **Compound_pass field semantic verification:** Dispatch 1 SHIFT B amended compound_pass from 5/5 to 4/4. Verify the field correctly reflects A1 criterion in the sweep output. If raw `compound_pass` still ANDs all 5 targets, build derived-compound-pass(A1) for the 4/4 criterion.
- **Disc #42 framing-audit on YOUR completion record:** before attesting "all 7 profiles PASS", verify the on-disk telemetry file matches your attestation (Disc #42 reinforcement; KR caught a discrepancy at Dispatch 2 verification).
- **Disc #47 candidate active:** R47.4 single-seam; R47.5 pre-flight vm_stat.
- **Disc #1.1 pre-fire resource-bounds:** expected sweep allocation < 1 GB (~RE-RUN-3/4 working set); pre-flight check.

---

## 5. URGENCY + SEQUENCING

**Fires THIRD in Phase A1 sequence — verifies BLOCKING-close item (R3 ∪ R3-A ∪ R3-B) delivered across Dispatches 1+2.** If this passes → KR fires Phase A1 Dispatch 4 (gandalf canonical close-criterion capture).

If this FAILS → KR surfaces to Matt with framing-audit Q1/Q2/Q3 applied to the failure mode (per Matt surface-to-Matt protocol — RE-RUN-5 FAIL is an explicit surface condition).

**Single-seam sequencing per R47.4 preserved.**

---

## 6. SURFACING-TO-KR PROTOCOL

Surface back to KR via completion record on this dispatch when:
- ✅ All 7 profiles PASS amended close-criterion 4/4 — normal close (KR fires Dispatch 4)
- ⚠️ Partial pass (e.g., 5/7 or 6/7 profiles PASS; 1-2 profiles FAIL at T1 or T2) — surface IMMEDIATELY with framing-audit Q1/Q2/Q3 applied to the failure mode
- ⚠️ Sweep produces unexpected output (e.g., T1 measurement context field missing; compound_pass(A1) field semantically unclear) — surface IMMEDIATELY
- 🚨 BVV anchor regressed from on-disk PASS state — surface IMMEDIATELY (this would indicate an upstream issue from Dispatches 1+2)
- 🚨 Framing-audit Q1-Q6 surfaces an assumption KR or gandalf got wrong — surface IMMEDIATELY

Per Matt 2026-05-23 hive-mind decision-routing: seam-owner decides in-scope work; Matt is LAST-resort escalation. Sweep firing is in-scope; surfacing FAIL conditions is the explicit Matt-surface gate.

---

**KR signature:** authored per Matt A1 election lock + KR Mode A 2-phase charge + Disc #47 R47.4 single-seam sequencing + Disc #42 Q1-Q6 framing-audit at dispatch-authoring gate (self-audited PASS). This dispatch is the cheapest empirical refutation of "does the amended close-criterion hold across 7 profiles?" — sweep + telemetry attestation in ~20-30 min. RE-RUN-5 PASS = Path α v1 engine readiness gate satisfied → unblocks canonical close-criterion capture + Gate-2 + closure record.

---

## Completion record

(gamora appends here)
