# elrond charge — Refit-Candidate-1 fit-relative ledger honesty fix (surgical; render-blocking)

**From:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-16 · **Follows:** A′–D completion (`da992f78`, verified GREEN at gandalf's gate) · **Blocks:** the comparison package to Matt (galadriel re-render gated on this).

## Defect (found at gandalf's A-render verify gate; galadriel surfaced, gandalf diagnosed)

Two ghost-field census ledgers in `atlas-refit-candidate-1.json` were carried **byte-verbatim from Edition III** into an emission whose FIT membership changed. Both are now false and BOTH RENDER ON THE PLATE:

1. **`ghost_field.off_plane_corpus`** — declares *"94 gear-grain kits (mcd-) sit in the corpus off-plane"* with `gate_rejected_keyed: 94, kits: 94, n: 94`. **All 94 kit_ids are on-plane points in the refit** (verified 94/94 overlap). The refit's stage predicate (combat-kit ∧ cell_key NOT NULL ∧ negative=0 → 628) ADMITTED them.
2. **`ghost_field.unmapped_pending_curation` = 114 (+ `_kits`)** — **all 114 are on-plane points in the refit** (verified 114/114; composition: mcd 94, poe2 6, la 4, d3 3, le 2, poe1 2, d4 1, di 1, hot 1). The plate footer renders "… 114 unmapped …" — false.

`unmapped_would_seal_excluded/_kits` (0/empty) and `depth_by_delivery` (lattice-level) are byte-equal AND correct — do not touch. `red3_note` already refit-specific — do not touch.

**Class rule going forward (state it in your MIGRATION entry):** corpus-level facts (n_mcd_total=120, the 26 no-key rows) may carry across fits; **fit-relative facts (who is on-plane) must re-derive per fit.**

## The fix (emission-side ONLY — no coordinate, fit, drill-in, p_df_1, alignment, or lattice change)

1. **Re-derive both ledgers against the refit's actual fit membership** (corpus.db + the 628-point set):
   - `off_plane_corpus`: keep the schema keys. Honest values: `gate_rejected_keyed: 0` (the refit's stage gate rejected none of the keyed 94), `n`/`kits`: the rows genuinely off-plane (expected: the 26 `unresolved_no_key` mcd rows; derive, don't assume), `n_mcd_total: 120`, `unresolved_no_key: 26` (re-assert from corpus). **New `disclosure` string — it renders verbatim on the plate, so write it for Matt's eyes.** It MUST state the grain fact honestly, e.g.: *"94 gear-grain kits (mcd-) ADMITTED at kit grain by this refit's stage predicate — the E1-era deferred grain ruling is hereby exercised implicitly and remains OPEN for Matt; 26 mcd rows (no cell key) remain off-plane."* (Wording yours; the three facts — admitted-94, ruling-open, 26-off-plane — are mandatory.)
   - `unmapped_pending_curation`/`_kits`: re-derive who is pending-curation-unmapped under the refit (expected 0 + [] if all 114 were admitted; derive, don't assume). If a nonzero remainder exists, list it.
2. **Fail-loud asserts before emit:** `set(off_plane kits) ∩ set(points kit_ids) == ∅` and `set(unmapped kits) ∩ points == ∅`; counts == list lengths; every other ghost_field field BYTE-IDENTICAL to the current `da992f78` emission (assert by hash of the JSON minus the two blocks — the fix must not drift anything else).
3. **Report fix:** `refit-candidate-1-comparison-report.md` census table row `off_plane_corpus N | 94 | 94` → correct refit column; add one short census-note paragraph stating the two-ledger correction + the grain-admission disclosure (with the 150/159 context if you verify it: of the 159 new actives vs E1's 469, 94 are gear-grain mcd and ~56 are class-grain LA — verify the split from corpus, report the true numbers).
4. **MIGRATION.md** entry (the class rule + what changed).

## Iron laws (unchanged)

Edition III + every served artifact READ-ONLY · no "Edition IV"/"edition4" · lattice byte-identical (767,411,820) · points/coords/loadings/ghost projections/drill_in/p_df_1/plane_alignment BYTE-UNTOUCHED.

## Return contract

≤15 lines: the two re-derived ledgers' honest values · assert results (intersections empty; rest-of-JSON hash unchanged) · report row corrected · commit hash. Auto-commit. **NO push.** HALT if: re-derivation shows a third stale fit-relative field (enumerate, don't fix silently) · any byte outside the two blocks + report + MIGRATION changes.

**Signed:** gandalf — the comparison package does not ship with a plate that contradicts its own points.
