# MIGRATION — Atlas fit/ghost-field layer (Elrond-owned)

**Owner:** elrond
**Scope:** schema + fact-honesty migrations for the atlas fit artifacts under `agentic_orchestration/research/curated/atlas/` (editions, refit candidates, ghost-field ledgers, comparison reports). Parallels the top-level `../MIGRATION.md` (corpus/register data layer) and star-lord's engine-side `MIGRATION.md` per AGENTS.md Tactic 2 + ADR-004.
**Append-only.** Most recent entry at the top.

---

## grain-law-ratification-2026-07-16 — `grain` column added to `canon_corpus` (kit|gear|class) + THE GRAIN LAW — 2026-07-16 — **APPLIED (Matt-ruled; column ratified)**

### THE GRAIN LAW (ratified — Matt rulings 2026-07-16, verbatim)
> *corpus grain = emission grain. The engine emits kits; the atlas plots what the engine can emit. **Every future fit-stage predicate MUST include `grain = 'kit'`.***

Two Matt rulings, ONE law. Verbatim:
1. **mcd:** *"Exclude the Minecraft Dungeons kits entirely."* → the 120 `mcd-` rows are **gear** grain.
2. **Lost Ark:** *"On Lost Ark, yes we CANNOT emit full classes… I would recommend deleting these entirely rather than decomposing."* → the 56 LA class-engraving rows are **class** grain (excluded from fits). The 6 Destroyer skill-grain rows (`la-destroyer-*`) are **kit** grain and survive. **This is a grain-based reading, not source-based** (gandalf's flagged interpretation — source-based exclusion of the whole `la` source is one predicate change away if Matt prefers; the ruling as written keeps the 6).

Both rulings are recorded in `canonical/matt_decision_needed/2026-07-16-edition3-vs-refit-candidate-1-adoption.md § RULING`. One law implements both and closes the failure class that contaminated Refit-Candidate-1: **manual fit-stage holds do not survive predicate rewrites; a ratified column does.** The 94 mcd gear-grain rows leaked into Refit-Candidate-1 precisely because the exclusion lived only in a hand-written stage predicate, not in the data. A `grain` column that every fit predicate references makes the exclusion structural and un-forgettable.

### What changed (one line)
Two additive columns on `canon_corpus`: **`grain` (TEXT ∈ {kit, gear, class}, NULL for non-emittable system-records)** and **`grain_note` (TEXT, provenance/flag annotation)**. Backfilled by provenance-anchored derivation. **Zero deletes** — catalogue philosophy: score/filter at consumption, never purge. Rows stay catalogued **INERT**; only the fit-STAGE predicate filters them out (`grain='kit'`, composed with the existing `row_class='combat-kit' ∧ negative=0 ∧ cell_key NOT NULL`).

### Derivation rules (provenance-anchored — derived per row, never assumed)
Applied in order; the branches are provably disjoint (no `la-destroyer-*` or `mcd` row is a system-record — asserted):
| Rule | Selector | grain | n |
|---|---|---|---|
| Minecraft Dungeons | `game='mcd'` (all `architecture='notable'`) | `gear` | 120 |
| LA Destroyer skill-grain | `game='la' AND kit_id LIKE 'la-destroyer-%'` | `kit` | 6 |
| LA class-engraving | `game='la'` (remainder; all `architecture='class-engraving'`) | `class` | 56 |
| System-record | `row_class='system-record'` (non-mcd/la) | `NULL` | 18 |
| Default (combat-kit) | everything else | `kit` | 509 |

**GRAIN CENSUS (709 rows):** `kit`=**515** · `gear`=**120** · `class`=**56** · `NULL`(system-record)=**18**. (The 515 kit includes the 6 LA Destroyer + 509 other-game combat-kits.)

### The NULL choice for system-records (deterministic, NOT ambiguous)
The 18 `row_class='system-record'` rows (loot-economy / progression / mobility-grammar / modifier-grammar cross-game infrastructure records — e.g. `di-inferno-ladder`, `ud-link-rune-grammar`, `poe1-blood-magic-kit`) are **none of kit/gear/class** on the emission axis. The vocabulary is fixed at `kit|gear|class`; forcing any of them onto a system-record would be a silent lie (a loot-economy record is not a "kit"). They are left **NULL with `grain_note`** — a deterministic, reproducible, documented NULL, **not** an ambiguity flag. They are already excluded from every fit by `row_class='combat-kit'`, so the composite GRAIN LAW predicate (`grain='kit' AND row_class='combat-kit'`) never depends on their grain value. Marking them `kit` for tidiness was rejected: honesty over convenience (Discipline #14 spirit — do not encode a value the data does not support).

### FLAG LIST (grain-ambiguous, resolved-per-ruling — 2 rows, under HALT threshold 20)
Two Destroyer rows carry conflicting provenance signals:
- `la-destroyer-rage-hammer` ("Rage Hammer Destroyer")
- `la-destroyer-gravity-training` ("Gravity Training Destroyer")

Their **kit_id prefix** (`la-destroyer-*`) says skill-grain → `kit`; their **architecture column** (`class-engraving`) says `class`; and their **folk_name pattern** (`<Build> Destroyer`, suffix form) matches the 56 class-grain rows, unlike the other 4 Destroyer rows (`Destroyer — <Skill>`, em-dash form, `architecture` empty). Matt's ruling is explicit and authoritative that **all 6 Destroyer rows are kit-grain citizens**, and the kit_id-prefix reading yields exactly the ruled 6/56 split. Both rows are therefore set `grain='kit'` **per the ruling**, each carrying a `grain_note` recording the architecture conflict so the source-vs-grain tension stays visible on inspection. If Matt prefers the architecture-column reading (58 class / 4 kit), it is a one-line re-derivation; the ruling as written (6 kit) is implemented.

### Reversibility + reproducibility
`grain` is fully re-derivable from provenance columns (`game`, `kit_id`, `architecture`, `canon_engine_key.row_class`) via `../scripts/corpus_grain_ratification_2026_07_16.py`, which is idempotent (re-running re-derives to identical values) and fail-loud (asserts the ruling arithmetic: gear=120, class=56, LA-kit=6, vocab-clean, flags≤20, zero non-system NULLs). No raw value is destroyed; the column is additive.

### Iron laws honored
- **Edition III + every served artifact READ-ONLY** — untouched.
- **Refit-Candidate-1 artifacts READ-ONLY** (permanent evidence exhibit; Matt's mcd ruling makes it never-adoptable) — untouched.
- **No re-fit / no re-emission** of any existing atlas artifact in this migration. The only mutation is the additive `grain`/`grain_note` backfill on `corpus.db`.

### ADR compliance
- **ADR-004:** this entry. No engine-telemetry change; star-lord-side `MIGRATION.md` unaffected. All work is collab-side curation (elrond data layer).
- Auto-committed per project discipline (Matt-authorized implementation under the GRAIN LAW rulings). Push deferred to KR's gate.
- **Consumer note for every future fit author:** the fit-stage predicate is now `grain='kit' AND row_class='combat-kit' AND negative=0 AND cell_key IS NOT NULL`. Do not hand-hold the mcd/LA exclusion in the predicate text — reference the ratified `grain` column. That is the whole point of the law.

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
