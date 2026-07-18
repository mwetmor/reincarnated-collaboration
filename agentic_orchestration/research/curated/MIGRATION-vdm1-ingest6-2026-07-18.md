# MIGRATION — VDM-1 ingest wave 6 (ERRATA-14/15 D-2a retro + ratified candidates)

**Date:** 2026-07-18
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1
**Script:** `agentic_orchestration/research/curated/scripts/corpus_vdm1_ingest6_2026_07_18.py`
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged; readonly crawlers run concurrently between sessions — NEVER flipped to WAL)

**Scope — two jobs:** (1) ERRATA-14/15, the stage-3 D-2a uniform-law retro-application
to two era floors b07 graded CONFIRMED under the now-retired policy split; and (2) the
stage-3 D-4 ratified CANDIDATE ingestion — 8 docket rows into `mechanic_gap_docket` +
6 mint rows into `mint_ledger`, all `steward-ratified-candidate` (one mint GRADUATED).
These are CANDIDATE records: **no engine change is authorized**; Matt-tier approval
happens at THE REVIEW BOOK.

---

## Backup

- **File:** `corpus.db.pre-vdm1-ingest6-2026-07-18-backup`
- **md5:** `6204fa04b9b415781ff85f080d7075fc` (matched live DB at backup time)
- **post-ingest live md5:** `072ec2729982a7874918b8383f6d5cd4`

(Backup is gitignored, same as `corpus.db` — retained on disk for reversibility, not
committed.)

---

## Inputs (committed, static)

| File | Rows | Destination |
|---|---|---|
| `.../vdm1/stage2/poe1/ratified-docket-rows.jsonl` | 8 | `mechanic_gap_docket` |
| `.../vdm1/stage2/poe1/ratified-mint-candidates.jsonl` | 6 | `mint_ledger` |

Both parsed clean (`load_jsonl` runs `json.loads` per line; **0 malformed**). These two
files are the **consolidation of record** (16 docket filings → 8; 8 mint filings → 6).
The 24 per-batch candidate side-files (`docket-candidates-batch-NN` /
`mint-candidates-batch-NN`) are the raw filings and are **NOT** read or ingested — the
ratified files supersede them.

---

## JOB 1 — ERRATA-14/15 (stage-3 D-2a uniform-law retro)

The **retired** policy split let an era floor stand if the skill had "genuine back-half
presence" in the bucket; b07 graded both these floors CONFIRMED under that split (see
errata-ledger REGISTER-ANNOT wave 4). The stage-3 **D-2a uniform law** is: *an era floor
that predates the skill's introduction patch is CONTRADICTED, regardless of back-half
meta presence.* Both kits' leftmost bucket floor is narrowed to the debut patch.

| Errata | kit_id | old eras | new eras | debut |
|---|---|---|---|---|
| ERRATA-14 | `poe1-tectonic-slam` | `3.0-3.6` | `3.2-3.6` | 3.2.0 |
| ERRATA-15 | `poe1-toxic-rain` | `3.0-3.6;3.7-3.13;3.14-3.19;3.20+` | `3.4-3.6;3.7-3.13;3.14-3.19;3.20+` | 3.4.0 |

- Each `canon_corpus.eras` UPDATE is **guarded to EXACTLY 1 row** against the exact
  current value (prior-value assert held in-script both pre-flight and inside the txn;
  `rowcount == 1` asserted).
- **ONLY the leftmost bucket's floor moves.** For toxic-rain the three later buckets
  (`3.7-3.13`, `3.14-3.19`, `3.20+`) are untouched — `3.7-3.13`'s b07 UNSUPPORTED grade
  is a partition-analysis input, not an errata basis; `3.14-3.19`/`3.20+` are CONFIRMED.
- **DISPATCH LAW honored:** the b07 `verify_ledger` verdict rows are **NOT** retro-edited
  — they keep their historical **CONFIRMED** grades. **NO `errata_applied` flag is set**
  this wave (that convention is reserved for CONTRADICTED-era verify rows; these kits
  have none). Same provenance shape as ERRATA-9 / BACKFILL-1: data restamp + ledger, no
  flag. **`errata_applied` total STAYS 12** (unchanged from ingest-4).
- Source anchors (verbatim, drawn from the kits' own b07 era CONFIRMED verify rows):
  "Tectonic Slam was introduced in patch 3.2.0 as a new Strength Skill Gem";
  "Toxic Rain was introduced in version 3.4.0 (Delve league)."
- Both restamps recorded in `.../vdm1/errata-ledger.md` (ERRATA-14, ERRATA-15), each
  explicitly noting it **supersedes** the corresponding wave-4 REGISTER-ANNOT (which
  reflected the retired split) while preserving the b07 CONFIRMED verdict row unedited.

---

## JOB 2 — Ratified candidate ingestion (stage-3 D-4)

Both target tables were **empty pre-ingest** (asserted `pre_docket == 0`,
`pre_mint == 0`); this is INSERT-only into fresh tables.

### Guarded additive schema migrations (non-destructive)

Two nullable columns added (idempotent — only if absent; no default rewrite, no data
touched):

- `mechanic_gap_docket` **ADD COLUMN `provenance_json` TEXT** — carries the file's
  `consolidated_from` + `notes` losslessly (the table already had a `status` column,
  used directly). No-fabrication: no datum dropped.
- `mint_ledger` **ADD COLUMN `status` TEXT** — the GRADUATED distinction is
  query-load-bearing and deserves a first-class home (parallels the docket table's
  existing `status`). The mint file's `consolidated_from` + `notes` are packed into the
  existing `ladder_step_audit` column as a small JSON object (that column is exactly the
  "which ladder step / provenance" slot).

These are ADR-004-internal (elrond's seam only); no engine-telemetry schema touched.

### Field mapping

| File field | `mechanic_gap_docket` column | `mint_ledger` column |
|---|---|---|
| `mechanism_class` | `mechanism_class` | — |
| `mint_class` | — | `mint_class` (CHECK quantitative\|qualitative) |
| `spec_text` | `spec_text_or_path` | — |
| `description` | — | `description` |
| `evidence_kits` / `forced_by_kits` | `evidence_kits` (JSON array) | `forced_by_kits` (JSON array) |
| `destination` | `destination` | — |
| `status` | `status` | `status` (new col) |
| `consolidated_from` + `notes` | `provenance_json` (new col, JSON) | `ladder_step_audit` (JSON) |

JSON serialized 1:1 via `json.dumps(..., ensure_ascii=False)`. `created_date` defaults
to `date('now')` on both tables.

### Validation gates (all passed; 0 rejects)

- status ∈ {`steward-ratified-candidate`, `steward-ratified-candidate-GRADUATED`} per row;
- `mint_class` ∈ {quantitative, qualitative};
- every `evidence_kits` / `forced_by_kits` entry exists in `canon_corpus` (FK sanity —
  report-and-HALT, not silent drop); **0 missing**;
- exactly 1 GRADUATED mint row.

---

## Post-ingest asserts (all pass — verified in-script AND by independent readonly query)

| # | Assert | Result |
|---|---|---|
| 1 | `mechanic_gap_docket` total == 0 + 8 | **8** ✓ |
| 2 | `mint_ledger` total == 0 + 6 | **6** ✓ |
| 3 | `entity-as-consumable-resource-pool` docket row `evidence_kits` length | **7** ✓ |
| 4 | GRADUATED mint rows == 1, its `forced_by_kits` length | **1 / 3** ✓ |
| 5 | ERRATA-14 guard: prior `3.0-3.6`, UPDATE rowcount | 1 ✓; landed `3.2-3.6` ✓ |
| 5 | ERRATA-15 guard: prior 4-band, UPDATE rowcount | 1 ✓; landed `3.4-3.6;…` ✓ |
| 6 | `errata_applied` total (UNCHANGED this wave) | **12** ✓ |
| 6 | tectonic-slam / toxic-rain `errata_applied` rows | 0 / 0 ✓ |
| 6 | tectonic-slam / toxic-rain era verify rows still CONFIRMED | ✓ (b07 rows untouched) |
| 7 | `canon_corpus` row count unchanged | 585 ✓ |
| 8 | non-ratified status leaked (docket + mint) | 0 ✓ |
| 9 | `PRAGMA journal_mode` == delete | delete ✓ |
| — | `PRAGMA integrity_check` | ok ✓ |
| — | `PRAGMA foreign_key_check` | empty ✓ |

---

## Reproducibility

Inputs are committed and static. Re-running the script against
`corpus.db.pre-vdm1-ingest6-2026-07-18-backup` reproduces this state exactly. Dry-run
mode (no `--apply`) validates and reports counts — including the ERRATA prior-value
guards, the entity-pool=7 / GRADUATED=3 named asserts, and the 8/6 projected totals —
without writing. The write path is a single `BEGIN IMMEDIATE` … `COMMIT` (short txn;
concurrent readonly crawlers unaffected), opened through an index.lock-retry wrapper
(wait 30s, retry 3×; **0 retries fired** this wave). journal_mode kept DELETE throughout.

---

## ADR-004 + reversibility

No engine-telemetry change; star-lord-side `MIGRATION.md` unaffected (all writes are in
elrond's seam: two guarded `canon_corpus.eras` restamps, two additive nullable columns,
8 + 6 candidate INSERTs). Reversible: `corpus.db.pre-vdm1-ingest6-2026-07-18-backup`
restores the exact PRE state; or the candidate rows are removable by table +
`status IN ('steward-ratified-candidate','steward-ratified-candidate-GRADUATED')`, the
eras restamps by their guarded inverse, and the added columns by table rebuild.
Auto-committed per project discipline (Matt-authorized VDM-1 charge).

**Candidate status:** the 8 docket + 6 mint rows are NON-authoritative CANDIDATE
records. No engine change is authorized by this ingest; Matt-tier ratification happens
at THE REVIEW BOOK.

---

## Commit note

Pathspec-only commit (matches ingest-1..5 precedent): migration doc + ingest script +
errata-ledger append. `corpus.db` and the backup are gitignored/untracked and are NOT
committed (verified via `git check-ignore`). **No push** (per charter R-9 — gandalf
pushes per basin checkpoint; + ADR-006).
