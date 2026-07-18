# MIGRATION — VDM-1 ingest wave 1 (PoE1 batches 01-02)

**Date:** 2026-07-18
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1
**Script:** `agentic_orchestration/research/curated/scripts/corpus_vdm1_ingest1_2026_07_18.py`
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged; readonly crawlers batches 03-04 run concurrently)

Loads the completed PoE1 crawl batches 01-02 into the landing-zone tables
(`verify_ledger`, `kit_citations`, `kit_dossier`, built at commit `2b73ee95`)
and applies the run's first errata + fact-provenance promotions.

---

## Backup

- **File:** `corpus.db.pre-vdm1-ingest1-2026-07-18-backup`
- **md5:** `418161954e79057a02c891252ed244c0` (matched live DB at backup time)

---

## Inputs (committed, static)

`agentic_orchestration/research/vdm1/stage1/poe1/batch-{01,02}-{verify,citations,dossier}.jsonl`

| Stream | B01 lines | B02 lines | Total lines |
|---|---|---|---|
| verify | 56 | 48 | 104 |
| citations | 34 | 32 | 66 |
| dossier | 72 | 72 | 144 |

(Batch summaries stated verify=52/52; actual non-blank line counts are 56/48.
The discrepancy is a summary-histogram rounding of the folded claim audit, not a
data defect — every line validated against the CHECK enums and FK. Counts below
are computed from the actual JSONL, which is the authority.)

---

## Ingested row counts (defaults: run_tag='vdm1', extraction_provenance='fetched-vdm1')

| Table | B01 | B02 | Total ingested | JSONL lines − dropped-filler |
|---|---|---|---|---|
| `verify_ledger` | 44 | 38 | **82** | 104 − 22 = 82 ✓ |
| `kit_citations` | 34 | 32 | **66** | 66 − 0 = 66 ✓ |
| `kit_dossier` | 72 | 72 | **144** | 144 − 0 = 144 ✓ |

Rejected-malformed rows (enum/FK violations): **0**. Every row validated clean.

---

## Dropped-filler (N/A-filler negative_canon rows)

Rule: `negative_canon` UNSUPPORTED rows on `canon_corpus.negative=0` kits are
N/A-filler (not honest silence) → DROP at ingest. Discriminator is the DB
`negative` flag (authoritative), not the claim_text.

| Batch | Dropped-filler rows |
|---|---|
| 01 | 12 |
| 02 | 10 |
| **Total** | **22** |

Batch-02 had 12 negative_canon rows but only 10 are filler. The 2 retained are
on the run's only two `negative=1` kits and ingest normally:

- `poe1-charged-dash` — negative_canon **CONFIRMED** (intrinsic design flaw:
  pulses cannot overlap; teleport cannot be canceled). Substantive, source-quoted.
- `poe1-cleave` — negative_canon **UNSUPPORTED** but substantive (extrinsic-no-lever;
  fell off meta without a hard nerf). Honest silence on a real causal claim, NOT
  N/A-filler — the death class is an inference, source-silent on the kill event.
  Curation note per batch-02 summary red-flag #4: `cleave.death_class` remains an
  inference, not a source-attested event.

Post-ingest check: `verify_ledger` contains **0** rows with `claim_text LIKE 'N/A%'`.

---

## Abstained dossier rows — payload CHECK reconciliation (documented, not silent)

The schema enforces `CHECK (abstained = 0 OR payload_json IS NULL)`. Seven dossier
rows are abstained (`abstained=1`). Five arrived with `payload_json = NULL`
(constraint-clean). **Two** arrived carrying an explanatory `{"note": ...}` payload,
which violates the CHECK. Per no-silent-transformation law, the note text is
**preserved verbatim here**; the stored `payload_json` was set to NULL so the row
ingests validly as the honest abstention it is. The note is abstention *metadata*,
not fetched content, and was NOT injected into `anchor_quote` (which must stay
verbatim-from-page).

| Batch | Line | kit_id | family | preserved note (verbatim) |
|---|---|---|---|---|
| 01 | 47 | `poe1-autobomber` | author_credit | `No single canonical author recovered from fetched sources for classic HoI Autobomber — community-evolved archetype without one attributed guide.` |
| 02 | 12 | `poe1-blood-magic-kit` | variants | `System-record kit: mechanic not build-grain. Source text does not enumerate named sub-variants.` |

Post-ingest: 7 abstained rows, 0 of them with non-NULL payload. CHECK held.

---

## ERRATA-1 — poe1-crackling-lance era correction

- **field:** `canon_corpus.eras`
- **old → new:** `3.7-3.13` → `3.12-3.13`
- **verdict:** CONTRADICTED (batch-02, era claim family)
- **source anchor:** Crackling Lance debuted patch **3.12.0 (Heist, 2020-09)**;
  cannot have been meta 3.7-3.11. Confirmed via mmogah.com + pathofexile.com/forum
  announcement + multiple 3.12-dated guide titles.
- **UPDATE rowcount:** 1 (asserted).
- **`verify_ledger.errata_applied`:** set to 1 on the ingested crackling-lance
  `era` row (exactly one row flagged; verdict=CONTRADICTED).
- **not-corrected:** `era_year` (=2013) is a separate mint-era attribute unrelated
  to the PoE patch band; left untouched.
- **ledger:** recorded at `agentic_orchestration/research/vdm1/errata-ledger.md`
  (ERRATA-1). Append-only.

## SOFT-FLAG-1 — poe1-aurastacker (no data change)

Era stamp `3.7-3.13` CONFIRMED (build existed via Aul's Uprising, patch 3.10) but
guide evidence skews 3.14-3.19 (Jix guide labeled 3.18). Plausible, not contradicted.
Recorded as SOFT-FLAG in the errata ledger; **no field changed** this wave.

---

## fact_provenance promotions

Rule: kits with `mechanics=CONFIRMED` AND **zero** CONTRADICTED verdicts anywhere
on the kit → flip `canon_probe_facts.fact_provenance` from
`named-source-unfetched`/`kb-legacy` → `verified-v1.1`.

- **Promote set:** 23 kits (all batch kits except `poe1-crackling-lance`).
- **crackling-lance:** EXCLUDED — carried a CONTRADICTED era; provenance stays
  `kb-legacy` (10 facts) this wave.
- **Rows promoted:** **200** (20 kits × 10 facts each).
- **Zero-promotion kits (in promote set but 0 rows flipped):**
  `poe1-blood-magic-kit`, `poe1-charged-dash`, `poe1-cleave` — these have **no
  `canon_probe_facts` rows at all** (verified: empty result), so 0 promoted is
  correct, not a miss.

Per-kit promotion rowcounts (non-zero): each of the 20 = 10.
Post-state for the 24-kit set: `verified-v1.1` = 200, `kb-legacy` = 10
(crackling-lance).

---

## Asserts (all pass)

| # | Assert | Result |
|---|---|---|
| 1 | `verify_ledger` count == 104 − 22 dropped-filler | 82 == 82 ✓ |
| 1 | `kit_citations` count == 66 | 66 == 66 ✓ |
| 1 | `kit_dossier` count == 144 | 144 == 144 ✓ |
| 2 | `canon_corpus` row count unchanged | 585 == 585 ✓ |
| 2 | canon_corpus untouched except crackling-lance `eras` | only `eras` on 1 row changed ✓ |
| 3 | `errata_applied=1` on exactly the crackling-lance era row | 1 row, era/CONTRADICTED ✓ |
| 4 | `PRAGMA journal_mode` == delete | delete ✓ |
| 4 | `PRAGMA integrity_check` | ok ✓ |
| 4 | `PRAGMA foreign_key_check` | empty (clean) ✓ |
| 5 | no N/A-filler leaked into ledger | 0 rows `N/A%` ✓ |
| 5 | abstained dossier rows with non-NULL payload | 0 of 7 ✓ |

---

## Reproducibility

Inputs are committed and static. Re-running the script against the pre-ingest
backup reproduces this state exactly. Dry-run mode (no `--apply`) validates and
reports counts without writing. Write path is a single `BEGIN IMMEDIATE` …
`COMMIT` (short txn; concurrent readonly crawlers unaffected).
