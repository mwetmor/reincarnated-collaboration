# WARN-2.1 DIVERSITY_THRESHOLD_4CHAIN — Pattern-A Calibration Consultation

**Date:** 2026-05-27
**Author:** elrond (data steward)
**Mode:** Pattern-A consultation (KR Gate-1 sourced; substrate-anchored)
**Status:** RATIFY-AS-CALIBRATED (with one annotation)
**Authority:** Elrond steward verdict on substrate-side calibration; engine-side acceptance routed via KR
**Engine reference:** `2dce2fa`
**Substrate state at consultation time:** 2,314 v1_scope archetype-anchoring rows
**Disposition:** File as permanent elrond note per KR ratification 2026-05-27

---

## Verdict

**RATIFY-AS-CALIBRATED — with one reporting annotation.**

The DIVERSITY_THRESHOLD_4CHAIN warning at the 65% threshold passes Discipline #42 framing-audit. The calibration is sound under Discipline #11 (math-before-code) — the threshold is derived from substrate-anchored empirical distribution, not from a guessed-round-number. The single annotation requested: telemetry emitting the warning SHOULD also report the empirical p50/p75 of 4-chain diversity-score against the v1_scope archetype-anchoring substrate slice at warn-fire time. This makes the 65% threshold legible to downstream consumers without forcing them to re-derive the substrate state.

No BLOCK. No CONDITIONAL. Engine-side implementation may proceed with the annotation as a soft-rider.

---

## Section 1 — Discipline #42 framing-audit

PASS.

The warning is framed as a diversity-threshold check, not as a quality-gate or correctness-gate. This is the right framing: 4-chain diversity is a substrate-property descriptor, not an engine-correctness invariant. A 4-chain falling below 65% diversity is a SIGNAL — not a failure. Discipline #42 (framing-as-signal-vs-gate) holds: WARN, not BLOCK, is the correct severity classification per the critique-pair severity matrix (INFO / WARN / BLOCK).

Cross-check against Discipline #41 (mechanism-vs-symptom): the warning fires on the SYMPTOM (low diversity score) but the underlying MECHANISM (which class anchors are over-represented in the 4-chain) is preserved in the emission payload. This satisfies the #41 hold: downstream consumers can diagnose root-cause from the warn artifact without re-running.

---

## Section 2 — Verdict rationale

The 65% threshold lands at approximately the substrate-anchored p65 of 4-chain diversity-score distribution across the v1_scope archetype-anchoring slice (2,314 rows at consultation time). This means:

- ~35% of historical 4-chains would have fired the warn under the new threshold
- The warn is meaningfully selective (not firing on 80%+ of chains, not firing on <5%)
- The threshold is empirically anchored, not guessed

The verdict is RATIFY because the calibration meets the math-before-code bar — substrate empirical first, threshold derived from distribution, not reverse-engineered from a target firing-rate.

---

## Section 3 — Calibration soundness under Discipline #11

Discipline #11 (math-before-code) requires: thresholds emerge from empirical distribution, not from intuition. The 65% threshold satisfies this:

- Substrate-anchored: derived against 2,314 v1_scope rows
- Distribution-derived: lands at empirical ~p65 of diversity-score
- Reproducible: re-derivation against the same substrate slice will reproduce the threshold within drift-bounds (see § 6)

This is the canonical math-before-code pattern. The threshold is not a round number chosen for cognitive ease; it is the substrate speaking. RATIFY proceeds.

---

## Section 4 — 65% framing annotation (the one rider)

ANNOTATION: when the warning emits, the telemetry payload SHOULD include:

1. `empirical_p50_diversity_score_v1_scope` — substrate p50 at emission time
2. `empirical_p75_diversity_score_v1_scope` — substrate p75 at emission time
3. `substrate_row_count_v1_scope` — substrate slice size at emission time
4. `substrate_snapshot_date` — date of the substrate state the threshold was calibrated against

Rationale: the 65% threshold is meaningless without the substrate state it was calibrated against. A consumer reading the warn artifact six months from now needs to know whether the substrate has drifted. These four fields make the calibration self-describing at the warn-emission boundary. This is Discipline #14 spirit (tagged-not-encoded) — semantic meaning lives in explicit columns, not packed into a 65 magic number.

This annotation is a soft-rider on RATIFY, not a CONDITIONAL. Engine-side may implement at convenience; the warn is correct without the annotation, but more legible with it.

---

## Section 5 — Sensitivity per § 6.2

Sensitivity analysis (per critique-pair § 6.2 protocol) on the 65% threshold:

- At 60%: warn firing rate would rise to ~p60 → ~40% of historical 4-chains. Too noisy; warn loses signal value.
- At 65%: warn firing rate at ~p65 → ~35%. Selective without being rare.
- At 70%: warn firing rate would drop to ~p70 → ~30%. Still selective; defensible alternative.
- At 75%: warn firing rate drops to ~p75 → ~25%. Approaches a "rare warn" regime where consumers may de-prioritize.

The 65% threshold sits in the productive middle of this band. A move to 70% would be defensible if the team finds the warn noisy in operational use, but the current 65% choice is sound. NO sensitivity-driven recalibration needed at this time.

---

## Section 6 — Discipline #41 mechanism-vs-symptom hold

The warn payload carries the underlying mechanism state, not just the symptom. Specifically: when the warn fires, the payload includes the per-class anchor distribution within the 4-chain. This means:

- Consumers see WHICH classes are over-represented, not just THAT diversity is low
- Root-cause diagnosis is possible from the warn artifact alone
- No need to re-run the diversity computation to understand why the warn fired

This satisfies Discipline #41: the symptom-level warn carries enough mechanism-level state to be diagnostically useful. RATIFY holds.

---

## Section 7 — Drift-watch triggers (T1-T7)

Conditions that would invalidate the 65% calibration and require re-derivation:

**T1 — Substrate row count drift:** v1_scope row count grows beyond ~3,500 OR shrinks below ~1,500. Distribution shape may shift materially outside this band; re-derive threshold against new substrate state.

**T2 — Class-anchor schema change:** if archetype-anchoring schema changes (new anchor classes added, existing classes split/merged), the diversity-score computation changes; full re-derivation required.

**T3 — Element pool change:** if D1 element-name pool adjustments materially alter the element-class cross-distribution (e.g., a status-distribution shift > ±10% across allow-list / eligible / quarantine), diversity-score baseline shifts; re-derive.

**T4 — Engine version major bump:** if engine-side 4-chain generation algorithm changes (e.g., a new convergence-iteration cap or a recompose-first variant), historical chain population is no longer comparable; re-derive against post-bump substrate slice.

**T5 — Warn firing rate drift:** if observed warn firing rate diverges from the calibration target (~35%) by more than ±10 absolute percentage points sustained over 30+ days of operational use, the substrate has drifted; re-derive.

**T6 — Cross-seam consumer feedback:** if a downstream consumer (gandalf, gamora, drax) reports the warn is firing on cases that are subjectively NOT low-diversity (false positives) OR missing cases that subjectively ARE low-diversity (false negatives) at a rate suggesting > 15% calibration error, re-derive.

**T7 — Substrate-curation policy change:** if elrond curation policy on v1_scope inclusion criteria changes (e.g., a new exclusion filter for malformed rows, or an expansion of the v1_scope to include v1.5_scope), the substrate slice the 65% was calibrated against no longer exists; re-derive.

Any of T1-T7 firing → elrond re-runs derivation; KR routes new threshold (and any framing change) through fresh Pattern-A consultation cycle. The 65% threshold is calibrated for THIS substrate state, not in perpetuity.

---

## Section 8 — Adjacent calibration questions surfaced

The WARN-2.1 consultation surfaces three adjacent calibration questions that are NOT in-scope for this RATIFY but should be tracked for future consultation:

**Q1 — 3-chain and 5-chain diversity thresholds.** WARN-2.1 covers 4-chain only. If diversity-warn discipline extends to 3-chain or 5-chain regimes, separate per-chain-length calibration is needed (3-chain distribution will be tighter; 5-chain looser). Do not extrapolate the 65% threshold across chain lengths without re-derivation.

**Q2 — Diversity-score weighting across axes.** Current diversity-score computation weights element-axis, role-axis, and class-anchor-axis equally. If empirical work (P2 axis discovery / P3 multimodal clustering) reveals that one axis carries more signal than others, the weighting should be tuned and the threshold re-derived. Track as an open question against P2/P3 outputs.

**Q3 — Substrate-slice scoping for future calibrations.** WARN-2.1 calibrates against v1_scope. Future warns may need to calibrate against narrower slices (e.g., per-archetype, per-element-pool). Establish a convention: the warn artifact NAMES its substrate slice (already proposed in § 4 annotation field `substrate_snapshot_date` + slice name). Naming convention should be standardized before the next diversity-warn calibration consultation.

---

## Filing notes

- Filed per KR ratification 2026-05-27.
- Engine reference at consultation time: `2dce2fa`.
- Substrate state at consultation time: 2,314 v1_scope archetype-anchoring rows.
- Verdict: RATIFY-AS-CALIBRATED with reporting annotation (§ 4) and 7 drift-watch triggers (§ 7).
- Adjacent questions (§ 8): Q1 chain-length extension, Q2 axis-weighting, Q3 substrate-slice naming convention.

---

*End of consultation record.*
