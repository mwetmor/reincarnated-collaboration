# Edition IV spec — admitting the curated LA/MCD to the atlas (DRAFT FOR RATIFICATION)

**Status:** DRAFT — pre-registered, awaiting Matt ratification of the P-parameters (§ 12) before the run fires
**Date:** 2026-07-16 · **Author:** gandalf (SPEC-AUTHOR)
**Authority:** Matt WAVE-4 ruling 2026-07-16 (`canonical/matt_decision_needed/2026-07-16-edition3-vs-refit-candidate-1-adoption.md` § WAVE 4): *"Edition IV = anchored-E3 + curated LA/MCD"* behind pre-registered gates. This spec replaces the shelved archipelago charter as the atlas forward artifact.
**Companions:** `MIGRATION.md` (GRAIN LAW · INGEST CLASS RULE · la-mcd-curation entry) · `atlas-edition3.json` (served truth) · `archipelago-mock-report.md` (SHELVED recognition record) · curation brief + ruling (`agentic_orchestration/gandalf/briefs/2026-07-16-elrond-la-mcd-curation-brief.md`)

---

## 0. TL;DR + the architecture fork (P-0 — the one decision that shapes everything)

Reading `atlas-edition3.json` at spec-time surfaced a load-bearing fact the wave-4 language didn't have: **E3 is not a refit.** Its `basis` block reads `"edition": 1, "frozen": true`; its `fit_layer_frozen_vs` reads *"Edition-I (atlas.json) — basis + 506 point coords + tombstones byte-identical."* Editions II and III kept Edition-I's frozen MCA basis and **admitted new citizens by supplementary projection** (the 37 tombstones project INTO the frozen space; they never influence it). Three editions of camera stability came from never moving the camera — while the one true refit ever attempted (refit-candidate-1) rotated 117° and died as an evidence exhibit.

So "E3's method," taken literally, already contains a cleaner mechanism for wave-4's intent (stable camera · ratified-only coloring · gated admission) than the Procrustes machinery I proposed before reading the artifact:

- **Path A — SUPPLEMENTARY ADMISSION (gandalf's lean).** Keep the frozen E1 basis. Project the curated rows in as supplementary points, exactly as the tombstones were. The camera cannot move **by construction** — the congruence gate passes vacuously (byte-identical ratified positions), the way F-1 passed vacuously in the mock. The proven house method, extended to its fourth edition.
- **Path B — TRUE REFIT + PROCRUSTES ANCHOR (wave-4's literal language).** Re-fit MCA on the staged corpus; Procrustes-align the new plane to E3's camera on common members; gate congruence ≥ threshold on the 86 ratified members. The basis learns the new corpus's variance; anchoring restores orientation but not distortion.

**Lean: Path A for E4, with Path B seated as the pre-registered E5 refit law behind an empirical trigger (§ 9).** Path A's known cost — the frozen basis never learns LA/MCD variance — is *measurable* (per-point representation quality, § 9); if the new corpus is poorly expressed in E1's axes, that measurement IS the refit trigger, and the Procrustes law fires for Edition V with its gates already registered. Admission-without-mutation now; re-derivation when evidence demands it. This is the GRAIN-LAW arc's shape applied to geometry: never mutate served truth; grow by disciplined admission; refit as a new-Edition event behind gates.

Everything below is written to execute under either path; path-specific sections are marked.

---

## 1. Objective + non-goals

**Objective:** admit the §9.19-curated LA/MCD rows (and the 6 new tombstones) to the served atlas as Edition IV, behind pre-registered gates, producing the plate on which the docket-1 review sitting (MELEE-STRIKE names + lit proto-island) runs.

**Non-goals (hard):** NO family propagation — τ is dead for coloring; the E4 plate colors **exactly the gateA-ratified members** (`gateA_group` non-null), families grow only by ratification waves. NO archipelago territory surface (shelved, criterion on record). NO serving change until Matt ratifies the gate report + side-by-side render. NO method drift beyond what P-0 selects.

## 2. Census + inputs (queried 2026-07-16, post-curation `8decaaae`)

| population | count | source |
|---|---:|---|
| corpus total | 585 | canon_corpus |
| `grain='kit'` | 566 | = 523 non-negative + 43 negative |
| kit + `cell_key` resolved | 509 | pre-existing (E1-era derivation) |
| kit + `cell_key` NULL | 57 | the curated LA/MCD (raw jsonl in `canon_engine_key.raw_json`) |
| E3 served points | 506 | = 469 active (basis members) + 37 supplementary tombstones |
| dossier-owed (post-cutoff c=0.4) | 4 | Wildsoul ×2 · Valkyrie ×2 |

**Expected E4 plate (under P-1 holdout):** 506 + 53 = **559** = 469 active-basis + 90 supplementary (37 legacy tombstones + 47 new positives + 6 new tombstones) — subject to run reconciliation, fail-loud.

**Reconciliation items (elrond names these in the run report; no silent disposition):**
- **R-1:** 509 keyed kit rows vs 506 E3 points — **3 keyed rows are not E3 citizens.** Name them, state why (staged out? era? never admitted?), disposition explicitly.
- **R-2:** the 6 new LA negatives need `death_class` seating per the tombstone convention before plate admission.
- **R-3:** exactly one pre-existing kit row carries `unresolved=1` WITH a cell_key — name it, state what its flag means, disposition.

## 3. Stage predicate (pre-registered terms — the law as code)

A row enters the E4 plate iff ALL hold:

- **T1 (GRAIN LAW):** `grain = 'kit'`. Excludes the 19 system-records including `la-monetization-confound` by construction.
- **T2 (provenance / source):** row traces to a speced ingest — the fifteen reference corpora, E1-lineage, or a §9.19 run (commits `da003065` / `14abd361`). Equivalently: **zero rows from the three breach direct-insert paths** — vacuous post-deletion, kept as a regression tripwire (fail-loud if non-vacuous).
- **T3 (fit-input):** `cell_key IS NOT NULL` after § 4 derivation. Underivable rows abstain + are named (never force-fitted).
- **T4 (dossier holdout — P-1):** `dossier_owed = 0`. The 4 post-cutoff-class records (c=0.4) stay catalogued until their dossiers pay; admission then is a routine E-next supplement.
- **T5 (tombstone stratum):** `negative = 1` rows ARE admitted, as supplementary tombstones (F-1: kit death is not geography; E3 precedent — the 37).
- Staged census reported **term-by-term** (rows excluded per term, named for T3/T4), reconciled against § 2 expected counts.

## 4. Cell_key derivation stage (owed work, both paths)

The curated 57 carry `unresolved=1`, `cell_key=NULL` by design — this stage resolves them:

- **D1:** derive each row's mechanical coordinates from its §9.19 `proj` axes (verbatim jsonl preserved per-row in `canon_engine_key.raw_json`) using **the same code-path that produced the existing 509 cell_keys.** No new mapping rules minted mid-run; if a §9.19 axis has no existing mapping, the row abstains (T3) and the gap is reported — mapping extensions are a spec amendment, not a run improvisation.
- **D2:** derivation coverage reported (n/57 resolved; target 57, honest short-fall named).
- **D3:** post-derivation, `unresolved` flips 1→0 for resolved rows; corpus.db is the only mutation surface at this stage.

## 5. Path A — supplementary admission (lean)

- **A1:** basis untouched — `atlas-edition4.json` carries the identical frozen E1 `basis` block (MCA, Greenacre-corrected inertia, MFA block-weighted, 14-dim parallel-analysis retention), `"frozen": true`, `fit_layer_frozen_vs: "Edition-I"` — extending the E2/E3 byte-identical guarantee: **all 506 existing point coords unchanged.**
- **A2:** the 53 admitted rows project in as supplementary points via the existing supplementary-projection machinery (`atlas-coordinates-supplementary.csv` lineage — the tombstones' path). Supplementary points never influence the basis (standard MCA supplementary treatment).
- **A3:** point contract = E3's fields (`kit_id, franchise, gateA_group, supplementary, x, y`) + **`edition_admitted: 4`** on new points (parse-contract-friendly extension; existing points unchanged).
- **A4:** ghost field re-emitted on the **unchanged frozen lattice** with occupancy/depth deltas recorded as `edition4_change` (the E3 artifact's own change-field convention).
- **A5:** coloring = ratified-only (§ 1). New LA/MCD points carry NO family color — they are uncolored citizens until a ratification wave seats them (docket machinery).

## 6. Path B — true refit + Procrustes anchor (wave-4 literal; seats as the E5 law if A ratifies)

- **B1:** re-fit E1's method (unchanged hyperparameters — method drift would be a different fork) on the staged population.
- **B2:** Procrustes-align the new 2D plane to E3's camera: transform = translation + rotation + reflection, **NO scale** (preserves E3 distance semantics; optimal scale s* computed and DISCLOSED, never applied). Anchor set = all members common to E3 and the new fit (maximal stability); the gate measures on the ratified 86 only (the design-load-bearing subset).
- **B3:** congruence gate per § 7 G-3 at the P-2 threshold; per-family centroid displacement + max-mover table disclosed for Matt's side-by-side review.

## 7. Gates (pre-registered — locked at spec ratification, immutable at run; any FAIL → E4 not served, E3 remains truth, failure report → Matt fork)

- **G-1 (grain):** staged population 100% `grain='kit'`; zero system/gear/class rows. Binary.
- **G-2 (provenance):** T2 verified non-silently — the breach-path tripwire query runs and returns zero. Binary.
- **G-3 (camera congruence on ratified members):** Path A — **PASS by construction** (frozen basis; ratified positions byte-identical), disclosed as vacuous-with-teeth: the byte-identity check RUNS (it is the E2/E3 guarantee, now a gate). Path B — congruence coefficient ≥ **0.85** (P-2) over the 86 gateA members' plane positions post-anchor.
- **G-4 (census reconciliation):** staged census matches § 2 expectations after named reconciliations R-1..R-3; every delta named. Fail-loud, no silent absorption.

## 8. Prediction registry (P-DF-1 discipline — registered here, graded at Matt's review sitting)

- **P-E4-1:** `mcd-summoner`'s nearest ratified family (full-space nearest-seed) = **MINION-PET**. *(Channel-C evidence; docket-6.)*
- **P-E4-2:** LA gauge-melee identities (Wardancer/Striker/Breaker-class records) **mutually condense** — mean pairwise full-space distance below corpus mean. *(Proto-GAUGE; docket-2.)*
- **P-E4-3:** each of the 6 LA negative twins lands **nearer its positive twin** than the corpus median nearest-neighbor distance. *(Tombstone-beside-parent, F-1 extension.)*
- **P-E4-4 (Path A diagnostic + P-3 input):** the 53 supplementary points' median representation quality (cos² in the frozen basis) falls within **2×** of the E1-actives' median — i.e., E1's axes can express LA/MCD variance without a refit.

## 9. Representation-quality disclosure + the E5 refit trigger (P-3)

Path A's honest cost, made empirical: per-point **cos² (squared cosine / communality) in the frozen basis** is computed for all 53 admitted points and disclosed in the artifact + gate report. **REFIT TRIGGER (pre-registered):** if the admitted cohort's median cos² < **0.5×** the E1-active median, the frozen basis is declared unable to express the grown corpus, and **Edition V fires as a Path-B refit** (§ 6, gates already registered). Relative threshold — self-calibrating against the basis's own baseline, no invented absolute. Until triggered, supplementary admission remains the standing method for future corpora (post-dossier LA records, future §9.19 games).

## 10. Emission + artifact contract

- `atlas-edition4.json` (this dir): E3's full key set (`edition: 4`, basis per path, points, loadings ref, counts, ghost_field, badge fields, `p_df_1_verdict`) + `edition_admitted` field + § 9 cos² table + gate report block.
- Emitter: extend `agentic_orchestration/research/scripts/build_atlas_json_edition3.py` lineage (new script `build_atlas_json_edition4.py`; cite parent in header).
- **Nothing served at emission.** Serving cutover is a separate post-ratification wave (§ 11).
- corpus.db mutations limited to § 4 D3 (`cell_key`, `unresolved`). MIGRATION entry records the run + gate results.

## 11. Ratification path + serving-cutover wave

1. Matt ratifies **this spec's P-parameters** (§ 12) → run authorized.
2. elrond executes §§ 3–10; gandalf verify-gates at artifact level (independent re-queries, gate re-computation spot-checks).
3. galadriel renders **side-by-side: E3 served vs E4 candidate** (one composite; under Path A visually identical geography + new points lit — that IS the demonstration) + the census/gate legend.
4. **Matt reviews + ratifies Edition IV** (the human gate is final).
5. **Serving-cutover wave** (post-ratification, the items queued since the dead candidate): vendor `atlas-edition4.json` to serving · glance re-vendor · display-name map refresh · render-head template-literal fix rides the cutover.
6. Then the **docket-1 review sitting** fires on the ratified E4 plate: MELEE-STRIKE names + lit proto-island (full-space credentials per candidate; plate = display, full-space = evidence) + docket-6 MINION-PET re-seed, one sitting.

## 12. Matt-visible parameters (rule these; everything else is pre-registered mechanics)

| # | Parameter | gandalf lean | Alternative |
|---|---|---|---|
| **P-0** | E4 architecture | **Path A — supplementary admission** (house method; camera immovable by construction; refit machinery seated as E5 law) | Path B — true refit + Procrustes now (basis learns LA/MCD variance immediately; heavier; anchoring corrects rotation, not distortion) |
| **P-1** | 4 dossier-owed records | **Hold out** until dossiers pay (BEST-ONLY spirit: when in doubt, leave out) | Admit at c=0.4 with confidence disclosed |
| **P-2** | Path-B congruence threshold | **≥ 0.85** on ratified 86 (mirrors the 0.860 full-space stability that held while the plane rotated) | Matt sets other |
| **P-3** | E5 refit trigger | **median cos² of admitted cohort < 0.5× E1-active median** | Matt sets other |

---

**Cross-references:** decision file § WAVE 4 · MIGRATION `la-mcd-curation-9.19-2026-07-16` · pipeline-spec §9.19.5 (BEST-ONLY · deletion · staging law as superseded by wave-4) · engine tracker SESSION-DELTA 2026-07-16-g (discovery docket + review protocol).
Tracker-delta: new open decision — E4 P-parameters (P-0 architecture fork foremost) → engine tracker, delta -g "Open with Matt."

**Signed:** gandalf (SPEC-AUTHOR) — the camera that never moved is the camera Matt already trusts; admit new citizens into it, and let the evidence, not the appetite, call the next refit.
