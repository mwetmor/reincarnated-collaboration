# MIGRATION — VDM-1 ingest wave 14 (basin-3 mapping load, kit_mapping 218→397)

**Date:** 2026-07-18
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1 (basin-3 Diablo d2/d3/d4/di, 179 kits) — run steward gandalf; fires under Matt's standing
autonomous-run mandate. WRITE commission (standing read-only default lifted for `corpus.db` only).
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged; single `BEGIN`…`COMMIT` txn; integrity_check + foreign_key_check both clean post-write).

**Scope:** Load 179 engine-mapping rows from basin-3 into `kit_mapping` table (218 → 397). Source: 15
mapping-batch JSONL files under `agentic_orchestration/research/vdm1/stage2/basin3/`.

**FILES GOVERN.** All expected counts asserted EXACTLY before load; any mismatch halts (never reconcile
silently). PRE-LOAD assertion table matched file-truth exactly (all 15 batches × 179 rows total).

---

## Backup + md5 chain

- **File:** `corpus.db.pre-vdm1-ingest14-20260718T183517`
- **Backup md5:** `90e29009b21998af5baa71991548c398` (== INGEST-13 post-md5; chain-head confirmed; unbroken chain)
- **md5 sidecar:** `corpus.db.pre-vdm1-ingest14-20260718T183517.md5.txt`
- **Pre-ingest live md5:** `90e29009b21998af5baa71991548c398`
- **Post-ingest live md5:** `366f9a73810b40b83597bf49c6f52885`
- **md5 chain:** `90e29009b21998af5baa71991548c398` → `366f9a73810b40b83597bf49c6f52885`

Backup retained on disk for reversibility; deliberately NOT committed (`*.db` and timestamped backup
names are gitignored under `curated/.gitignore`).

---

## Inputs (file-truth — `.../vdm1/stage2/basin3/`, 15 mapping-batch JSONL files)

All files `json.loads`-clean (0 parse failures). 179 rows / 179 distinct kit_ids. Recount asserted
EXACTLY (PRE-LOAD guard).

| Batch | Rows | EXACT | CLOSE | APPROX | GAPPED | MAPPED | MAPPED_DOCKET |
|---|---|---|---|---|---|---|---|
| 01 | 12 | 1 | 9 | 2 | 0 | 12 | 0 |
| 02 | 12 | 3 | 9 | 0 | 0 | 12 | 0 |
| 03 | 12 | 3 | 3 | 3 | 3 | 9 | 3 |
| 04 | 12 | 0 | 6 | 2 | 4 | 8 | 4 |
| 05 | 12 | 2 | 6 | 2 | 2 | 10 | 2 |
| 06 | 12 | 0 | 7 | 3 | 2 | 10 | 2 |
| 07 | 12 | 0 | 8 | 2 | 2 | 10 | 2 |
| 08 | 12 | 0 | 10 | 0 | 2 | 10 | 2 |
| 09 | 12 | 0 | 9 | 2 | 1 | 11 | 1 |
| 10 | 12 | 2 | 8 | 0 | 2 | 10 | 2 |
| 11 | 12 | 0 | 10 | 2 | 0 | 12 | 0 |
| 12 | 12 | 2 | 8 | 0 | 2 | 10 | 2 |
| 13 | 12 | 0 | 10 | 1 | 1 | 11 | 1 |
| 14 | 12 | 0 | 4 | 4 | 4 | 8 | 4 |
| 15 | 11 | 0 | 6 | 2 | 3 | 8 | 3 |
| **TOTAL** | **179** | **13** | **113** | **25** | **28** | **151** | **28** |

Advisory histogram (from dispatch): EXACT=13 / CLOSE=113 / APPROX=25 / GAPPED=28; MAPPED=151 / MAPPED_DOCKET=28.
File-truth matches advisory exactly — no discrepancy.

---

## Pre-load assertion table

| # | Assert | Expected | Actual | Result |
|---|---|---|---|---|
| 1 | `SELECT COUNT(*) FROM kit_mapping` | 218 | 218 | PASS |
| 2 | md5(corpus.db) == chain-head | `90e29009b21998af5baa71991548c398` | `90e29009b21998af5baa71991548c398` | PASS |
| 3 | File recount: 15 files → 179 rows / 179 distinct kit_ids | 179 / 179 | 179 / 179 | PASS |
| 4 | Zero kit_id collision with existing kit_mapping | 0 collisions | 0 collisions | PASS |
| 5a | grade ∈ {EXACT,CLOSE,APPROX,GAPPED} on every row | 0 violations | 0 violations | PASS |
| 5b | terminal_state ∈ {MAPPED,MAPPED_DOCKET} on every row | 0 violations | 0 violations | PASS |
| 5c | biconditional GAPPED ⟺ MAPPED_DOCKET on every row | 0 violations | 0 violations | PASS |
| 6 | Advisory grade histogram EXACT=13/CLOSE=113/APPROX=25/GAPPED=28 | matches file-truth | exact match | PASS (files govern) |
| 6b | Advisory terminal histogram MAPPED=151/MAPPED_DOCKET=28 | matches file-truth | exact match | PASS (files govern) |

**Advisory-vs-file discrepancy: NONE.** File-truth and advisory numbers agree exactly on all counts.

---

## Load

- 179 rows inserted in ONE transaction (`BEGIN` … `COMMIT`).
- `mapping_json` serialized as `json.dumps(dict, ensure_ascii=False)` (TEXT column).
- `mapping_provenance = 'authored-vdm1'` (matches all 218 existing rows).
- `authored_date = '2026-07-18'` (matches all 218 existing rows).

---

## Post-load assertion table

| # | Assert | Expected | Actual | Result |
|---|---|---|---|---|
| 9a | `COUNT(*) FROM kit_mapping` | 397 | 397 | PASS |
| 9b | Basin-3 kit_ids present in DB | 179 | 179 | PASS |
| 10 | Round-trip fidelity: `json.loads(db.mapping_json)` == source dict | 179 clean | 179 clean | PASS |
| 11a | In-DB grade histogram for 179 basin-3 rows | EXACT=13/CLOSE=113/APPROX=25/GAPPED=28 | exact match | PASS |
| 11b | In-DB terminal histogram for 179 basin-3 rows | MAPPED=151/MAPPED_DOCKET=28 | exact match | PASS |
| 11c | Biconditional GAPPED ⟺ MAPPED_DOCKET in-DB | 0 violations | 0 violations | PASS |
| 12 | Post-md5 computed | `366f9a73810b40b83597bf49c6f52885` | `366f9a73810b40b83597bf49c6f52885` | PASS |

**Integrity:** `PRAGMA integrity_check` = ok; `PRAGMA foreign_key_check` = clean; `PRAGMA journal_mode` = delete.

---

## Pre/post state

| Table | Before | After | Δ |
|---|---|---|---|
| `kit_mapping` | 218 | 397 | +179 |

---

## Reproducibility + reversibility

Inputs static (post-audit basin-3 mapping JSONL, 15 files). Load is idempotent against a clean
baseline (zero-collision guard ensures no double-insert path). Full restore = copy
`corpus.db.pre-vdm1-ingest14-20260718T183517` over `corpus.db` (backup md5 `90e29009b21998af5baa71991548c398`).

---

## ADR-004

No engine-telemetry change; star-lord-side MIGRATION.md unaffected (all writes are elrond-seam corpus
curation). Auto-committed per project discipline (Matt-authorized VDM-1 charge). **NO push — steward
(gandalf) pushes per basin checkpoint.**

## Commit note

Pathspec-only: this migration doc. `corpus.db` is gitignored and NOT committed. Backups + md5 sidecar
stay on disk (uncommitted). Basin-3 stage-2 mapping inputs (gandalf's, static) are not touched.
