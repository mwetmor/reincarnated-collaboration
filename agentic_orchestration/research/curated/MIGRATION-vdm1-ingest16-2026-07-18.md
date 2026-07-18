# MIGRATION — VDM-1 ingest wave 16 (basin-4 mapping load, kit_mapping 397→449)

**Date:** 2026-07-18
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1 (basin-4 Lost Ark, 52 kits) — run steward gandalf; fires under Matt's standing
autonomous-run mandate. WRITE commission (standing read-only default lifted for `corpus.db` only).
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged; single `BEGIN`…`COMMIT` txn; integrity_check + foreign_key_check both clean post-write).

**Scope:** Load 52 engine-mapping rows from basin-4 into `kit_mapping` table (397 → 449). Source: 5
mapping-batch JSONL files under `agentic_orchestration/research/vdm1/stage2/basin4/`.

**FILES GOVERN.** All expected counts asserted EXACTLY before load; any mismatch halts (never reconcile
silently). PRE-LOAD assertion table matched file-truth exactly (all 5 batches × 52 rows total).

---

## Backup + md5 chain

- **File:** `corpus.db.pre-vdm1-ingest16-20260718T212721`
- **Backup md5:** `f8a924defb23ee46151794720d85647e` (== INGEST-15 post-md5; chain-head confirmed; unbroken chain)
- **md5 sidecar:** `corpus.db.pre-vdm1-ingest16-20260718T212721.md5.txt`
- **Pre-ingest live md5:** `f8a924defb23ee46151794720d85647e`
- **Post-ingest live md5:** `91edd323858310372bacb99c43fee148`
- **md5 chain:** `f8a924defb23ee46151794720d85647e` → `91edd323858310372bacb99c43fee148`

Backup retained on disk for reversibility; deliberately NOT committed (`*.db` and timestamped backup
names are gitignored under `curated/.gitignore`).

---

## Inputs (file-truth — `.../vdm1/stage2/basin4/`, 5 mapping-batch JSONL files)

All files `json.loads`-clean (0 parse failures). 52 rows / 52 distinct kit_ids. Recount asserted
EXACTLY (PRE-LOAD guard).

| Batch | Rows | EXACT | CLOSE | APPROX | GAPPED | MAPPED | MAPPED_DOCKET |
|---|---|---|---|---|---|---|---|
| 01 | 11 | 1 | 8 | 0 | 2 | 9 | 2 |
| 02 | 11 | 0 | 8 | 0 | 3 | 8 | 3 |
| 03 | 10 | 0 | 7 | 1 | 2 | 8 | 2 |
| 04 | 10 | 0 | 9 | 0 | 1 | 9 | 1 |
| 05 | 10 | 1 | 9 | 0 | 0 | 10 | 0 |
| **TOTAL** | **52** | **2** | **41** | **1** | **8** | **44** | **8** |

Advisory histogram (from dispatch): EXACT=2 / CLOSE=41 / APPROX=1 / GAPPED=8; MAPPED=44 / MAPPED_DOCKET=8.
File-truth matches advisory exactly — no discrepancy.

Per-batch advisory (cross-check): n01 9 MAPPED/2 DOCKET · n02 8/3 · n03 8/2 · n04 9/1 · n05 10/0.
File-truth matches per-batch advisory exactly.

---

## Pre-load assertion table

| # | Assert | Expected | Actual | Result |
|---|---|---|---|---|
| 1 | `SELECT COUNT(*) FROM kit_mapping` | 397 | 397 | PASS |
| 2 | md5(corpus.db) == chain-head | `f8a924defb23ee46151794720d85647e` | `f8a924defb23ee46151794720d85647e` | PASS |
| 3 | File recount: 5 files → 52 rows / 52 distinct kit_ids | 52 / 52 | 52 / 52 | PASS |
| 4 | Zero kit_id collision with existing kit_mapping (`la-%` count == 0) | 0 collisions | 0 collisions | PASS |
| 5a | grade ∈ {EXACT,CLOSE,APPROX,GAPPED} on every row | 0 violations | 0 violations | PASS |
| 5b | terminal_state ∈ {MAPPED,MAPPED_DOCKET} on every row | 0 violations | 0 violations | PASS |
| 5c | biconditional GAPPED ⟺ MAPPED_DOCKET on every row | 0 violations | 0 violations | PASS |
| 6 | Advisory grade histogram EXACT=2/CLOSE=41/APPROX=1/GAPPED=8 | matches file-truth | exact match | PASS (files govern) |
| 6b | Advisory terminal histogram MAPPED=44/MAPPED_DOCKET=8 | matches file-truth | exact match | PASS (files govern) |

**Advisory-vs-file discrepancy: NONE.** File-truth and advisory numbers agree exactly on all counts.

---

## Load

- 52 rows inserted in ONE transaction (`BEGIN` … `COMMIT`).
- `mapping_json` serialized as `json.dumps(dict, ensure_ascii=False)` (TEXT column).
- `mapping_provenance = 'authored-vdm1'` (matches all 397 existing rows).
- `authored_date = '2026-07-18'` (matches all 397 existing rows).

---

## Post-load assertion table

| # | Assert | Expected | Actual | Result |
|---|---|---|---|---|
| 9a | `COUNT(*) FROM kit_mapping` | 449 | 449 | PASS |
| 9b | Basin-4 `la-%` kit_ids present in DB | 52 | 52 | PASS |
| 9c | Distinct `la-%` kit_ids in DB | 52 | 52 | PASS |
| 10 | Round-trip fidelity: `json.loads(db.mapping_json)` == source dict | 52 clean | 52 clean | PASS |
| 11a | In-DB grade histogram for 52 basin-4 rows | EXACT=2/CLOSE=41/APPROX=1/GAPPED=8 | exact match | PASS |
| 11b | In-DB terminal histogram for 52 basin-4 rows | MAPPED=44/MAPPED_DOCKET=8 | exact match | PASS |
| 11c | Biconditional GAPPED ⟺ MAPPED_DOCKET in-DB | 0 violations | 0 violations | PASS |
| 12 | Post-md5 computed | `91edd323858310372bacb99c43fee148` | `91edd323858310372bacb99c43fee148` | PASS |

**Integrity:** `PRAGMA integrity_check` = ok; `PRAGMA foreign_key_check` = clean; `PRAGMA journal_mode` = delete.

---

## Pre/post state

| Table | Before | After | Δ |
|---|---|---|---|
| `kit_mapping` | 397 | 449 | +52 |

---

## Reproducibility + reversibility

Inputs static (post-audit basin-4 mapping JSONL, 5 files). Load is idempotent against a clean
baseline (zero-collision guard ensures no double-insert path). Full restore = copy
`corpus.db.pre-vdm1-ingest16-20260718T212721` over `corpus.db` (backup md5 `f8a924defb23ee46151794720d85647e`).

---

## ADR-004

No engine-telemetry change; star-lord-side MIGRATION.md unaffected (all writes are elrond-seam corpus
curation). Auto-committed per project discipline (Matt-authorized VDM-1 charge). **NO push — steward
(gandalf) pushes per basin checkpoint.**

## Commit note

Pathspec-only: this migration doc. `corpus.db` is gitignored and NOT committed. Backups + md5 sidecar
stay on disk (uncommitted). Basin-4 stage-2 mapping inputs (gandalf's, static) are not touched.
