# MIGRATION — Atlas fit/ghost-field layer (Elrond-owned)

**Owner:** elrond
**Scope:** schema + fact-honesty migrations for the atlas fit artifacts under `agentic_orchestration/research/curated/atlas/` (editions, refit candidates, ghost-field ledgers, comparison reports). Parallels the top-level `../MIGRATION.md` (corpus/register data layer) and star-lord's engine-side `MIGRATION.md` per AGENTS.md Tactic 2 + ADR-004.
**Append-only.** Most recent entry at the top.

---

## refit-candidate-1-ledger-honesty-2026-07-16 — surgical fit-relative ghost-field ledger correction (emission-side only) — 2026-07-16 — **APPLIED (comparison artifact; Matt adoption still pending)**

### What changed (one line)
Two ghost-field census ledgers in `atlas-refit-candidate-1.json` were carried byte-verbatim from Edition III into an emission whose FIT membership had changed. `off_plane_corpus` (declared 94 off-plane) was FALSE — all 94 `mcd-` gear-grain kits are on-plane points in the refit — and was RE-DERIVED to the honest fit-relative value (**26**). `unmapped_pending_curation` (114) was investigated and found NOT stale — it is a *lit-map census*, TRUE by re-derivation — but was rendering misreadably on the plate, so a **`unmapped_pending_curation_disclosure`** semantics field was ADDED (count + list bytes untouched). Emission-side ONLY: no coordinate, fit, drill-in, `p_df_1`, `plane_alignment`, or lattice change. Lattice byte-identical (`depth_sum_check` = 767,411,820). No "Edition IV"/"edition4" string introduced.

### The defect and the non-defect (provenance)
- **Ledger 1 — `off_plane_corpus`: STALE fit-relative fact.** Edition III served `{gate_rejected_keyed: 94, kits: [94 mcd gear kits], n: 94}`. The refit's stage predicate (**combat-kit ∧ cell_key NOT NULL ∧ negative=0 → 628**) ADMITTED all 94 keyed gear-grain kits as on-plane points (94/94 overlap with `points[].kit_id`). Honest re-derivation: `gate_rejected_keyed: 0` (the stage gate rejected none of the keyed 94) · `n = kits = 26` (the mcd rows carrying no cell key — they never entered the fit; 0/26 overlap with points) · `n_mcd_total: 120` · `unresolved_no_key: 26`. The `kits` list is now the 26 no-key kit_ids (identical to `unresolved_no_key_kits`, which is correct: under this fit the off-plane kits ARE exactly the no-key kits).
- **Ledger 2 — `unmapped_pending_curation`: NOT stale (register/lattice-level census, TRUE by construction).** The 114 are kits lacking a `fit2reg_movement` mapping (movement=blank) and thus absent from the lit-lattice census — re-derived from the refit's OWN `lit_map` to the byte-identical set of 114. "Unmapped" = not present in the lit-map, NOT off-plane; all 114 are nonetheless plotted as on-plane points. The count is genuinely TRUE. It went *misreadable* (not false) in the refit because in Edition III 94 of the 114 weren't plotted there, so the footer wasn't ambiguous; in the refit all 114 are plotted, so the plate needed the fit-relative `..._disclosure` field to prevent "unmapped" being read as "off-plane".
- **Third-stale-field audit: NEGATIVE.** `unmapped_would_seal_excluded/_kits` (0/[]) re-derived correct; `depth_by_delivery` (lattice-level) byte-equal and correct; `red3_note` already refit-specific. No further carried-over field is false.

### THE THREE-CLASS FACT RULE (state this so the next auditor does not repeat the error)
A ghost-field emission carries facts of three distinct provenance classes. Byte-equality across fits is a DIFFERENT correctness question for each:

1. **Corpus-level facts** — properties of the corpus rows independent of any fit (e.g. `n_mcd_total = 120`; the 26 no-cell-key mcd rows). **May carry across fits byte-equal.** Byte-equality is fine.
2. **Fit-relative facts** — WHO is on-plane / which kits the stage predicate admitted (e.g. `off_plane_corpus.n`, `.kits`, `.gate_rejected_keyed`). **MUST re-derive per fit against that fit's actual membership.** Byte-carrying these is the defect this entry corrects. Iff you change the fit, you must recompute these.
3. **Register/lattice-level facts** — properties of the register v1.3 lattice + the reg-to-fit mapping census (e.g. the lit-map census / `unmapped_pending_curation`, `depth_by_delivery`, `depth_sum_check`, sealed/feasible denominators). **Byte-equality is CORRECT BY CONSTRUCTION** — the lattice did not move; only the FIT projection of it did. Do NOT "re-derive to a new number"; verify byte-equality and, if the same TRUE number can be *misread* under the new fit's plotting, add a fit-relative disclosure (as done here for the 114).

### Case lineage (why the misdiagnosis happened)
The original charge operated on a **two-class taxonomy** (corpus-level carry vs fit-relative re-derive) and predicted `unmapped_pending_curation` would re-derive to `0 + []` under the refit. That prediction was WRONG: the 114 is a class-3 register/lattice-level census, not a class-2 fit-relative fact. The re-derivation at the HALT surfaced the missing third class. gandalf's RULING added class 3 to the taxonomy precisely because the two-class model caused gandalf's own initial misdiagnosis of the 114. The lesson: before declaring a carried-over census "stale," classify its provenance — a register/lattice census that is byte-equal by construction is not stale, it is correct, and the fix is disclosure (not re-derivation).

### The fix (surgical text replacement — NOT `json.dump`)
The artifact is 6.8 MB (628 points with coordinates). A full `json.dump` re-serialization would drift float formatting across the whole file. The fix was applied as a **byte-level text replacement** of exactly the `off_plane_corpus` block plus a single inserted `unmapped_pending_curation_disclosure` line, with formatting (6-space key indent, 8-space list indent, literal em-dash) matched to the surrounding emission.
- **Fail-loud asserts before write (all PASSED):** `set(off_plane_corpus.kits) ∩ set(points[].kit_id) == ∅` (0 overlap) · `n == len(kits) == 26` · `unresolved_no_key == len(unresolved_no_key_kits) == 26` · `gate_rejected_keyed == 0` · `n_mcd_total == 120` · `unmapped_pending_curation == 114` and its `_kits` list byte-identical to the pre-fix emission · the ONLY new ghost_field key is `unmapped_pending_curation_disclosure`.
- **Rest-of-JSON byte-identical proof:** JSON minus the (replaced) `off_plane_corpus` block minus the (added) `unmapped_pending_curation_disclosure` line == the pre-fix JSON minus its `off_plane_corpus` block, byte-for-byte (SHA-256 `e3d407f8…` on both). Nothing else drifted; `points`/coords/loadings/ghost projections/`drill_in`/`p_df_1`/`plane_alignment`/lattice all BYTE-UNTOUCHED.

### The two disclosure strings (they render verbatim on the plate for Matt's eyes)
- **`off_plane_corpus.disclosure`:** *"94 gear-grain kits (mcd-) were ADMITTED at kit grain by this refit's stage predicate (combat-kit ∧ cell_key NOT NULL ∧ negative=0) and are plotted as on-plane points; the E1-era deferred grain ruling is thereby exercised implicitly and remains OPEN for Matt. 26 mcd rows carry no cell key and remain genuinely off-plane — they are the kits listed here."* (Three mandatory facts: admitted-94 / ruling-OPEN / 26-off-plane.)
- **`unmapped_pending_curation_disclosure`:** *"lit-map census — these 114 kits lack a fit2reg_movement mapping (movement=blank) and are therefore absent from the lit-lattice census; ALL 114 are nonetheless plotted as on-plane points in this refit. 'Unmapped' means not present in the lit-map, NOT off-plane."* (Two mandatory facts: lit-map-predicate meaning / all-114-plotted.)

### Companion corrections
- **Comparison report** `refit-candidate-1-comparison-report.md`: §8 census-table row `off_plane_corpus N` refit column `94 → **26**`; added a "Census note — off_plane_corpus honesty correction" paragraph (the correction + grain-admission disclosure + the 114 lit-map-census clarification + the TRUE 159 new-actives split: **94 mcd gear-grain + 62 Lost Ark [56 class-grain + 6 Destroyer skill-grain] + 3 pull re-keys (d3/di/d4)**, 0 dropped vs Edition-I's 469).
- **Diagnostic script committed:** `../scripts/refit_ledger_honesty_verify_2026_07_16.py` — verify-only (no writes); reproduces the 628-point fit membership from `corpus.db`, cross-checks both carried ledgers, and derives the honest values. Committed WITH this fix as the provenance of both the defect (ledger 1) and the non-defect (ledger 2).

### Not in this charge (routed elsewhere)
- **galadriel re-render + assert #24 retune** — the render fork is galadriel's staged r2 charge (gandalf's chain, amended). No galadriel render script was touched by this fix.

### ADR compliance
- **ADR-004:** this entry. No engine-telemetry change; star-lord-side MIGRATION.md unaffected. All work is collab-side curation (elrond atlas tree). Edition III + every served artifact READ-ONLY — untouched.
- **Reversibility:** the honest values are fully reproducible from `../scripts/refit_ledger_honesty_verify_2026_07_16.py` + `corpus.db` + the 628-point set; the correction is a documented, deterministic re-derivation, not a destructive edit.
- **Naming discipline:** "Edition IV"/"edition4" appears in NO code/artifact/stamp/log touched by this fix.
- Auto-committed per project discipline (Matt-authorized surgical fix under gandalf's RULING). Push deferred to KR's gate.
