# MIGRATION — VDM-1 ingest wave 15 (basin-4 Lost Ark crawl load: dossier + verify + citations)

**Date:** 2026-07-18
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1 (basin-4 Lost Ark, 52 kits) — run steward gandalf; fires under Matt's standing
autonomous-run mandate. WRITE commission (standing read-only default lifted for `corpus.db` only).
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged; never flipped to WAL; single `BEGIN`…`COMMIT` txn;
integrity_check + foreign_key_check both clean post-write).

**Scope:** Pure INSERT of basin-4 Lost Ark crawl data into three tables: `kit_dossier` (+312 rows),
`verify_ledger` (+177 rows), `kit_citations` (+75 rows). Greenfield only — no backfill, no supersede,
no errata, no promotion gate. The 53rd LA kit `la-monetization-confound` (is_system=1) is correctly
absent from all source files and was not touched.

**FILES GOVERN.** All expected counts asserted EXACTLY before the transaction; any mismatch halts
(never reconcile silently). PRE-LOAD assertion table matched file-truth exactly (5 batches × 3 files).

---

## Backup + md5 chain

- **File:** `corpus.db.pre-vdm1-ingest15-20260718T203625`
- **Backup md5:** `4550cf06e25534879ae5f61f7cdbec72` (backup re-pages via `.backup`; backup md5 ≠
  live chain-head, content identical — integrity_check=ok, journal_mode=delete on backup).
- **md5 sidecar:** `corpus.db.pre-vdm1-ingest15-20260718T203625.md5.txt`
- **Pre-ingest live md5:** `366f9a73810b40b83597bf49c6f52885` (== INGEST-14 post-md5; chain-head
  confirmed; unbroken chain, no interim writes between waves).
- **Post-ingest live md5:** `f8a924defb23ee46151794720d85647e`
- **md5 chain:** `366f9a73810b40b83597bf49c6f52885` → `f8a924defb23ee46151794720d85647e`

Backup retained on disk for reversibility; deliberately NOT committed (`*.db` and timestamped backup
names are gitignored under `curated/.gitignore`).

---

## Inputs (file-truth — `.../vdm1/stage1/basin4/`, 15 JSONL files across 5 batches)

All files `json.loads`-clean (0 parse failures). Recount asserted EXACTLY (PRE-LOAD guard):

| Batch | verify (C/X/U/SNF) | citations | dossier (abstained) |
|---|---|---|---|
| 01 | 34 (32/1/1/0) | 14 | 66 (0) |
| 02 | 34 (33/1/0/0) | 16 | 66 (2) |
| 03 | 44 (42/0/2/0) | 14 | 60 (8) |
| 04 | 34 (30/3/1/0) | 16 | 60 (0) |
| 05 | 31 (31/0/0/0) | 15 | 60 (6) |
| **TOTAL** | **177 (168/5/4/0)** | **75** | **312 (16)** |

- 52 distinct `la-%` kit_ids (is_system=0) across all three unions; all three sets are identical.
- `la-monetization-confound` (is_system=1) absent from all files — correctly so.
- Citations column set = schema column set exactly; 0 extra, 0 missing fields.
- Abstained-16 dossier rows: all carry null payload_json in source (no fabrication; assertion 8 PASS).
- 0 intra-file UNIQUE(kit_id, family, source_url) collisions (assertion 7 PASS).

---

## Pre-load assertion table

| # | Assert | Expected | Actual | Result |
|---|---|---|---|---|
| 1 | `SELECT COUNT(*) FROM kit_dossier` | 2394 | 2394 | PASS |
| 2 | `SELECT COUNT(*) FROM verify_ledger` | 1512 | 1512 | PASS |
| 3 | `SELECT COUNT(*) FROM kit_citations` | 951 | 951 | PASS |
| 4 | `md5(corpus.db)` == chain-head `366f9a73810b40b83597bf49c6f52885` | match | `366f9a73810b40b83597bf49c6f52885` | PASS |
| 5 | File recounts: dossier=312 / verify=177 / citations=75; 52 distinct `la-%` kits in each; 0 parse failures | exact | exact | PASS |
| 6 | Zero pre-existing `la-%` rows in all three tables | 0/0/0 | 0/0/0 | PASS |
| 7 | Dossier UNIQUE(kit_id, family, source_url): 0 intra-file collisions | 0 | 0 | PASS |
| 8a | Every abstained=1 row has null payload_json in source | 0 violations | 0 violations | PASS |
| 8b | Every abstained=0 row has non-null payload object in source | 0 violations | 0 violations | PASS |
| 8c | `conf` is REAL-or-null (never a string) | 0 violations | 0 violations | PASS |
| 9a | Dossier family ∈ {skill_loop, skill_geometry, item_alterations, capstone_alterations, author_credit, variants} | 0 violations | 0 violations | PASS |
| 9b | Verify verdict ∈ {CONFIRMED, CONTRADICTED, UNSUPPORTED, SOURCE_NOT_FOUND} | 0 violations | 0 violations | PASS |
| 9c | Verify claim_family ∈ {identity, mechanics, era, negative_canon} | 0 violations | 0 violations | PASS |
| 9d | Citations cite_class ∈ {authored, communal, official, dataset} (non-null only) | 0 violations | 0 violations | PASS |
| 9e | Citations rank_class ∈ {recovered, attested-era} (non-null only) | 0 violations | 0 violations | PASS |
| 10 | CONFIRMED/CONTRADICTED verify rows all have non-empty anchor_quote | 0 violations | 0 violations | PASS |

All 10 assertion groups PASS. Transaction proceeded.

---

## Load

- 312 `kit_dossier` rows, 177 `verify_ledger` rows, 75 `kit_citations` rows inserted in ONE transaction
  (`BEGIN` … `COMMIT`).
- `payload_json` serialization: non-null source objects → `json.dumps(obj, ensure_ascii=False)` (TEXT);
  null source values → SQL NULL.
- `extraction_provenance = 'fetched-vdm1'` on all 312 new dossier rows (column default; also set
  explicitly in INSERT).
- `verify_ledger` column defaults applied: `errata_applied=0`, `run_tag='vdm1'`,
  `verified_date=date('now')`.
- No `OR IGNORE` semantics used — pure INSERT (greenfield; zero collision expected and asserted).

---

## Post-load assertion table

| # | Assert | Expected | Actual | Result |
|---|---|---|---|---|
| P1 | `SELECT COUNT(*) FROM kit_dossier` | 2706 | 2706 | PASS |
| P2 | `SELECT COUNT(*) FROM verify_ledger` | 1689 | 1689 | PASS |
| P3 | `SELECT COUNT(*) FROM kit_citations` | 1026 | 1026 | PASS |
| P4 | LA dossier rows | 312 | 312 | PASS |
| P5 | LA verify rows | 177 | 177 | PASS |
| P6 | LA citations rows | 75 | 75 | PASS |
| P7 | Distinct kit_ids in LA dossier | 52 | 52 | PASS |
| P8 | Distinct kit_ids in LA verify | 52 | 52 | PASS |
| P9 | Distinct kit_ids in LA citations | 52 | 52 | PASS |
| P10 | In-DB verify histogram for 177 LA rows: 168C/5X/4U/0SNF | 168/5/4/0 | 168/5/4/0 | PASS |
| P11 | Round-trip fidelity: `json.loads(db.payload_json)` == source object (3-row sample) | PASS | PASS | PASS |
| P12 | Abstained rows: `payload_json IS NULL` in-DB (0 violations) | 0 | 0 | PASS |
| P13 | `PRAGMA integrity_check` | ok | ok | PASS |
| P14 | `PRAGMA foreign_key_check` | clean | clean (0 rows) | PASS |
| P15 | `PRAGMA journal_mode` | delete | delete | PASS |
| P16 | Post-ingest md5 | computed | `f8a924defb23ee46151794720d85647e` | PASS |

All 16 post-load assertions PASS.

---

## Pre/post state

| Table | Before | After | Delta |
|---|---|---|---|
| `kit_dossier` | 2394 | 2706 | +312 |
| `verify_ledger` | 1512 | 1689 | +177 |
| `kit_citations` | 951 | 1026 | +75 |

---

## Reproducibility + reversibility

Inputs static (post-audit basin-4 JSONL, 5 batches × 3 files). Load is idempotent against a clean
baseline (zero-collision guard ensures no double-insert path). Full restore = copy
`corpus.db.pre-vdm1-ingest15-20260718T203625` over `corpus.db` (backup integrity_check=ok; restores
the `366f9a73810b40b83597bf49c6f52885` live-equivalent baseline; pre-counts kd=2394, vl=1512,
kc=951 confirmed).

---

## ADR-004

No engine-telemetry change; star-lord-side MIGRATION.md unaffected (all writes are elrond-seam corpus
curation). Auto-committed per project discipline (Matt-authorized VDM-1 charge). **NO push — steward
(gandalf) pushes per basin checkpoint.**

## Commit note

Pathspec-only: this migration doc. `corpus.db` is gitignored and NOT committed. Backups + md5 sidecar
stay on disk (uncommitted). Basin-4 stage-1 crawl inputs (Legolas's, static) are not touched.
