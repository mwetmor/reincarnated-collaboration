# MIGRATION — VDM-1 ingest wave 5 (kit_mapping wave-2; PoE1 mapping 05-08)

**Date:** 2026-07-18
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1
**Script:** `agentic_orchestration/research/curated/scripts/corpus_vdm1_ingest5_2026_07_18.py`
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged; readonly crawlers run concurrently between sessions — NEVER flipped to WAL)

**Scope — one job:** land the SECOND `kit_mapping` wave (PoE1 mapping batches 05-08,
46 rows). Steward-audited, **ZERO re-grades** — the committed
`mapping-batch-0{5,6,7,8}.jsonl` files ARE the audited state. NO stage-1 batches, NO
errata, NO backfill, NO promotions this wave (those all landed at ingest-4). This
completes PoE1 mapping at **94/94** (48 wave-1 + 46 wave-2 = one row per PoE1 kit).

---

## Backup

- **File:** `corpus.db.pre-vdm1-ingest5-2026-07-18-backup`
- **md5:** `735eaed1b5ef92e4a3dc31e700a79123` (matched live DB at backup time)

(Backup is gitignored, same as `corpus.db` — retained on disk for reversibility, not
committed.)

---

## Inputs (committed, static)

Stage-2: `agentic_orchestration/research/vdm1/stage2/poe1/mapping-batch-0{5,6,7,8}.jsonl`

| Batch | Lines |
|---|---|
| mapping-batch-05 | 12 |
| mapping-batch-06 | 12 |
| mapping-batch-07 | 12 |
| mapping-batch-08 | 10 |
| **Total** | **46** |

All 46 rows parsed clean (`load_jsonl` runs `json.loads` per line; **0 malformed**).
Row shape matches wave-1 (ingest-4): `kit_id`, `mapping_json` (nested dict serialized
1:1 via `json.dumps(..., ensure_ascii=False)`), `grade`, `deviation_notes`,
`terminal_state`. `mapping_provenance` defaults to `authored-vdm1` (the kit_mapping
run-tag convention — the table has no `run_tag` column; provenance IS the tag);
`authored_date` defaults to `date('now')`.

---

## INSERT-ONLY guard (dispatch LAW — no upsert)

Pre-write guard: if ANY of the 46 kit_ids already had a `kit_mapping` row, HALT and
report. Enforced as a pre-write assert against the live DB's existing kit_mapping kit
set BEFORE the write txn opens. **0 collisions** — none of the 46 wave-2 kits
overlapped the 48 wave-1 kits. Also verified: **0 FK-missing** (all 46 present in
`canon_corpus`), **0 in-file dupes**, **0 enum/FK rejects**.

---

## kit_mapping wave-2 — 46 rows ingested (whole-DB now 94)

Wave-2 file-level distribution (before merge): grade CLOSE 30 / APPROX 12 / GAPPED 4
(EXACT 0); terminal MAPPED 42 / MAPPED_DOCKET 4. Wave-2 GAPPED = MAPPED_DOCKET =
{spectres, ward-loop, wild-strike, wormblaster} (in-file R-M7 1:1 holds).

**Post-ingest asserts (all pass — verified in-script AND by independent readonly query):**

| # | Assert | Result |
|---|---|---|
| 1 | `kit_mapping` total == 48 + 46 | **94** ✓ |
| 1 | distinct kit_ids == 94 (one row per PoE1 kit) | 94 ✓ |
| 1 | INSERT-only: PK collisions | **0** ✓ |
| 2 | whole-DB grade histogram EXACT / CLOSE / APPROX / GAPPED | **2 / 62 / 22 / 8** ✓ (exact) |
| 3 | R-M7 1:1: `MAPPED_DOCKET` set == `GAPPED` set, count 8 | ✓ (identical sets) |
| 3 | GAPPED/DOCKET kit set == exact 8-kit dispatch set | ✓ (see below) |
| 3 | grade↔terminal incoherent rows (GAPPED xor MAPPED_DOCKET) | 0 ✓ |
| 4 | `mint_ledger` remains 0 rows | 0 ✓ |
| 4 | `mechanic_gap_docket` remains 0 rows | 0 ✓ |
| — | new rows carry `mapping_provenance='authored-vdm1'` | 0 non-conforming ✓ |
| — | `kit_mapping` FK orphans back to `canon_corpus` | 0 ✓ |
| 5 | `PRAGMA journal_mode` == delete | delete ✓ |
| — | `PRAGMA integrity_check` | ok ✓ |
| — | `PRAGMA foreign_key_check` | empty ✓ |

**The 8-kit GAPPED / MAPPED_DOCKET set (whole-DB, R-M7 1:1):**
`poe1-aurabot, poe1-detonate-dead, poe1-forbidden-rite, poe1-heavy-strike-stun,
poe1-spectres, poe1-ward-loop, poe1-wild-strike, poe1-wormblaster`
(wave-1 contributed the first four; wave-2 the last four.)

**Note on wild-strike + wormblaster continuity with ingest-4:** both were flagged at
ingest-4 on the verify/promotion side (wild-strike = negative kit, negative_canon
CONFIRMED; wormblaster = mechanics UNSUPPORTED, stayed kb-legacy, stage-4 residue
flag). Their arrival here as GAPPED→MAPPED_DOCKET is consistent — a kit that could not
be verified/promoted on the corpus side maps to a docket terminal on the mapping side.
No cross-table contradiction.

---

## NOT ingested this wave (await steward ratification at ingest-6)

The candidate side-files are **NOT** read or ingested this wave:
`mint-candidates-batch-*`, `docket-candidates-batch-*`, `mapping-batch-*-summary.md`.
Only the four `mapping-batch-0{5..8}.jsonl` files were read. `mint_ledger` and
`mechanic_gap_docket` therefore **remain 0 rows** (asserted). Steward ratification of
the mint / docket candidate sets lands at **ingest-6**.

---

## Reproducibility

Inputs are committed and static. Re-running the script against
`corpus.db.pre-vdm1-ingest5-2026-07-18-backup` reproduces this state exactly. Dry-run
mode (no `--apply`) validates and reports counts — including the INSERT-only collision
guard and the projected 94 total — without writing. The write path is a single
`BEGIN IMMEDIATE` … `COMMIT` (short txn; concurrent readonly crawlers unaffected),
opened through an index.lock-retry wrapper (wait 30s, retry 3×; **0 retries fired**
this wave). journal_mode kept DELETE throughout.

---

## ADR-004 + reversibility

No engine-telemetry change; star-lord-side `MIGRATION.md` unaffected (the only write
is 46 `kit_mapping` INSERTs, elrond's seam). Reversible:
`corpus.db.pre-vdm1-ingest5-2026-07-18-backup` restores the exact PRE state; or the 46
rows are removable by their kit set + `mapping_provenance='authored-vdm1'` +
`authored_date`. Auto-committed per project discipline (Matt-authorized VDM-1 charge).
**NO push — gandalf pushes per basin checkpoint (R-9).**

---

## Commit note

Pathspec-only commit (matches ingest-1..4 precedent): migration doc + ingest script.
`corpus.db` and the backup are gitignored/untracked and are NOT committed (verified via
`git check-ignore`). No push (per charter R-9 — gandalf pushes; + ADR-006).
