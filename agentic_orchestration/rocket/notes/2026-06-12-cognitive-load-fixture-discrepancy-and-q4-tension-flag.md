# FLAG to gandalf — two surfaced issues from Item 3 (cognitive load) + Item 5 (coupling depth)

**From:** rocket (content-generation seam)
**To:** gandalf (design steward) — cc knight-rider
**Date:** 2026-06-12
**Context:** executing dispatch `2026-06-12-rocket-generation-handoff.md` Items 2/3/5.
**Disposition:** do-not-self-adjust. Implemented the LOCKED spec exactly; flagging two
authoring-side issues for design ruling. Neither blocks the implementation — both are robust at
the BIN level, which is what gates downstream eligibility.

---

## Flag 1 — Session 3 § 6.4 cognitive-load fixture table is internally inconsistent (arithmetic)

The § 6.4 table is presented as acceptance fixtures, but 3 of its 6 rows have
`formula(displayed columns) ≠ displayed score`. The LOCKED § 6.2 formula is:

```
cognitive_load_score = skill_count×1.0 + sequence_depth×2.0 + state_conditions×1.5 + timing_windows×2.5
```

| Fixture | (skill, seq, state, timing) | formula→score | § 6.4 listed | Δ | bin(formula) | bin(listed) |
|---|---|---|---|---|---|---|
| Simple AoE | (3,0,0,0) | 3.0 | 3.0 | 0 | LOW | LOW |
| Combo DoT | (4,0,1,0) | 5.5 | 5.5 | 0 | LOW | LOW |
| MOMENTUM_CASCADE | (5,0,1,1) | **9.0** | 8.0 | +1.0 | MEDIUM | MEDIUM |
| RESONANCE+hybrid | (5,2,2,2) | 17.0 | 17.0 | 0 | HIGH | HIGH |
| TEMPORAL+charge | (5,0,2,2) | **13.0** | 10.5 | +2.5 | MEDIUM | MEDIUM |
| RES+MOM 3-chain | (6,2,3,3) | **22.0** | 19.5 | +2.5 | HIGH | HIGH |

**All six BINS agree** regardless of the score discrepancy. Since the bin (LOW/MEDIUM/HIGH) is
what gates RESONANCE_LOOP / TEMPORAL_CHARGE eligibility and feeds Item 11's generation prior, the
metric is robust to the arithmetic discrepancy.

**What I implemented (within HOW latitude):** the LOCKED § 6.2 formula EXACTLY. Tests assert the 3
self-consistent fixtures to their SCORE and all 6 fixtures to their BIN
(`tests/test_kit_finalization.py::test_cognitive_load_formula_and_bins`). I did **not** silently
reconcile the discrepancy by altering the formula weights or bin thresholds.

**Ruling requested:** is the § 6.4 listed-score column an authoring arithmetic slip (most likely —
the deltas look like dropped `timing×2.5` or `state×1.5` terms), or is there an intended
weighting nuance the displayed columns don't capture? If the former, no code change is needed (the
formula is the source of truth and bins are correct). If the latter, the formula spec needs a
§ 6.2 amendment and I'll re-derive.

---

## Flag 2 — Q4 (S3) vs § 3.3 (S4) tension on coupling's contribution to sequence_depth

- **Session 3 Q4** rules: `sequence_depth` is **T4-only for now**.
- **Session 4 § 3.3** says: `coupling_depth … contributes to the sequence_depth factor`.

These partially conflict — coupling depth is a chain/prerequisite property, which Q4 currently
EXCLUDES from sequence_depth.

**What I implemented:** T4-only sequence_depth (Q4 governs), gated by a module-level config flag
`INCLUDE_COUPLING_IN_SEQUENCE_DEPTH = False` (kit_finalization.py). When Matt/gandalf rule Q4 to
include the chain contribution, flip the flag — coupling then enters as
`max(0, coupling_depth - 1)` added to the T4 sequence_depth. This is the "one-line amendment"
posture the dispatch § 12 Q4 placeholder anticipated.

**Ruling requested:** confirm Q4 stays T4-only (flag remains False) until a BC measurement pass
shows whether coupling materially moves cognitive-load bins, OR rule to enable the coupling
contribution now. No code change needed to keep the current default; flipping is one line + a test.

---

## Cross-refs

- Math note: `reincarnated-engine/src/reincarnated/generation/math/session-3-4-kit-finalization-predictor-cogload-coupling-2026-06-12.md` (§ 2.3 fixture audit; § 4 Q4 tension)
- Implementation: `reincarnated-engine/src/reincarnated/generation/kit_finalization.py`
- Tests: `reincarnated-engine/tests/test_kit_finalization.py` (25 pass)
