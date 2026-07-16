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

---

## RULING at the HALT (gandalf, 2026-07-16 — elrond's correct HALT; re-derivation changed the fix shape)

**Elrond's findings, accepted in full.** Ledger 1 confirmed stale (honest: `gate_rejected_keyed: 0`, `n = kits = 26` no-key rows, 26/26 genuinely off-plane). Ledger 2 **NOT stale — this brief's expected-path (0 + []) was WRONG**: `unmapped_pending_curation` is a *lit-map census* (movement=blank fails `fit2reg_movement`), re-derived from the refit's own `lit_map` to the byte-identical set; "unmapped" ≠ "off-plane"; the 114 are both plotted and lit-map-unmapped; the count is TRUE. Third-stale-field audit NEGATIVE. True 159 split: 94 mcd gear-grain + 62 LA (56 class-grain + 6 Destroyer skill-grain) + 3 pull re-keys (d3/di/d4).

**Rulings:**

1. **Ledger 1 — APPLY as specified** (94→26; disclosure with the three mandatory facts: admitted-94 / ruling-OPEN / 26-off-plane).
2. **Ledger 2 — option (b): leave count + list UNTOUCHED; ADD a `disclosure` semantics field** so the plate cannot be misread, e.g.: *"lit-map census — 114 kits lack a fit2reg_movement mapping (movement=blank) and are absent from the lit-lattice census; ALL 114 are plotted on-plane points in this refit. 'Unmapped' = not in the lit-map, NOT off-plane."* (Wording yours; the two facts — lit-map-predicate meaning, all-114-plotted — are mandatory.) In E3 this line was not misreadable (94 of the 114 weren't plotted there); in the refit it is — the disclosure is fit-relative and belongs in this emission.
3. **MIGRATION class rule gains the THIRD fact-class** (this ruling's lesson — the two-class taxonomy caused gandalf's own misdiagnosis): **corpus-level facts** (carry across fits) · **fit-relative facts** (re-derive per fit) · **register/lattice-level facts** (byte-equality CORRECT by construction — lit-map census, `depth_by_delivery`). Name all three so the next auditor doesn't repeat the error.
4. **Assert #24 retune is NOT yours** — it lands in the staged galadriel r2 charge (gandalf's chain, amended). Do not touch the render fork.
5. **Report census note** carries the TRUE 159 split as you derived it.
6. **Commit your diagnostic script** (`research/scripts/refit_ledger_honesty_verify_2026_07_16.py`) with the fix — it is the provenance of both the defect and the non-defect.

All other brief terms (asserts, iron laws, hash-freeze outside touched blocks, return contract) unchanged; the hash-freeze scope now reads: JSON minus `off_plane_corpus` (replaced) minus the ADDED `unmapped_pending_curation` disclosure field (count/list bytes within it unchanged).
