# MIGRATION — VDM-1 ingest wave 18 (basin-5 MAPPING INGEST — LAST mapping ingest of VDM-1 run)

**Date:** 2026-07-18
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1 (basin-5 mapping stage) — run steward gandalf; fires under Matt's standing
autonomous-run mandate. WRITE commission (standing read-only default lifted for `corpus.db` only).
**Script:** `agentic_orchestration/research/scripts/vdm1_ingest18_basin5_mapping_2026_07_18.py`
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged; transactions via executemany + targeted UPDATE;
integrity_check + foreign_key_check both clean post-write).

**Spec:** `agentic_orchestration/research/vdm1/stage2/basin5/INGEST-BASIN5-MAPPING-MANIFEST.md`

**Scope:** Greenfield INSERT 125 kit_mapping rows (mapping-batch-p01..p13.jsonl) + MAP-ERRATA-1
(ud-lightning-vortex element correction). TIER-2 HOLD: mechanic_gap_docket and mint_ledger
untouched. On completion: `kit_mapping` 449 → 574 = every VDM-1 kit mapped (full-run mapping
stage COMPLETE).

**FILES GOVERN.** All expected counts asserted EXACTLY before write; mismatch → ABORT.

---

## Backup + md5 chain

- **File:** `corpus.db.pre-vdm1-ingest18-20260718T234606`
- **Backup md5:** `87bb6b471dbf3e42e56292f6fc577994` (== INGEST-17 post-md5; chain-head confirmed; unbroken)
- **Pre-ingest live md5:** `87bb6b471dbf3e42e56292f6fc577994`
- **Post-ingest live md5:** `4a1ae47c7ded48f6443780602eb7e8ea`
- **md5 chain:** `87bb6b471dbf3e42e56292f6fc577994` → `4a1ae47c7ded48f6443780602eb7e8ea`

Backup retained on disk; NOT committed (`*.db` and timestamped backup names gitignored under
`curated/.gitignore`).

---

## TIER 1 — Greenfield kit_mapping ingest (125 rows, p01–p13)

### Source files

All 13 batch files under `agentic_orchestration/research/vdm1/stage2/basin5/`, each a JSONL of
`{kit_id, mapping_json, grade, deviation_notes, terminal_state}` rows.

| Batch | Rows |
|---|---|
| p01 | 11 |
| p02 | 10 |
| p03 | 8 |
| p04 | 8 |
| p05 | 12 |
| p06 | 11 |
| p07 | 11 |
| p08 | 12 |
| p09 | 11 |
| p10 | 9 |
| p11 | 8 |
| p12 | 7 |
| p13 | 7 |
| **TOTAL** | **125** |

Row shape matches manifest spec (11·10·8·8·12·11·11·12·11·9·8·7·7). All 125 rows json.loads-clean
(0 parse failures). All 125 kit_ids resolve to existing `canon_corpus` rows (zero phantoms). Zero
pre-existing `kit_mapping` rows for these kit_ids (collision-free per steward pre-audit + elrond
re-assert). le-harvest-lich + le-bomb-lance-falconer both in p13; both inserted as normal rows
(no special-casing).

### Rows inserted

| Table | Inserted |
|---|---|
| `kit_mapping` | 125 |

`mapping_json` stored as compact JSON text (separators `(",",":")`, `ensure_ascii=False`); values
are round-trip-stable from source JSONL.

### 1a. Post-insert totals

| kit_mapping | Before | After | Delta |
|---|---|---|---|
| Total rows | 449 | 574 | +125 |

---

## MAP-ERRATA-1 — ud-lightning-vortex (gating, sole expected DB≠file diff)

**Anchor:** `INGEST-BASIN5-MAPPING-MANIFEST.md` §1b (STEWARD-AUDIT ERRATA).

On the `ud-lightning-vortex` row's `mapping_json`, the `"Lightning Vortex"` skill object:

| Field | Before | After | Rationale |
|---|---|---|---|
| `element_primary` | `null` | `"lightning"` | FALSE-NEGATIVE fix. Dossier skill_loop payload: "vortex deals additional lightning damage to nearby enemies"; two verify_ledger anchors corroborate ("deal Cleave Lightning area DMG"; "vortex that inflicts Vortex Lightning DMG"). Damage-type descriptor on enemy-directed verb → attests under D4 name-only law (which blocks element-word SOLELY in a name, not descriptor-prose). Basin-5 addendum §11: element-RICH D2-lineage cluster warns against silent-default instinct. |
| `ailments` | `["shock"]` | `[]` | FALSE-POSITIVE fix. `shock` (engine = paralysis) is UNATTESTED: no paralysis text in any admissible store ("brief duration" describes zone lifetime, not paralysis status). Mapper kept the lightning-derived ailment while dropping the lightning element — the inverse pair; removing the unattested ailment restores strict-attested-only discipline. |

`grade` (CLOSE) and `terminal_state` (MAPPED) unchanged. The identity errata (ranged→melee) that
justified CLOSE stand; the element completeness fix does not upgrade to EXACT.

Applied via targeted `UPDATE kit_mapping SET mapping_json=? WHERE kit_id='ud-lightning-vortex'`
after the greenfield INSERT. Rowcount asserted == 1.

---

## 1c. R-M7 biconditional assert (post-ingest, scoped to new 125 rows)

```
COUNT(grade='GAPPED') == COUNT(terminal_state='MAPPED_DOCKET') == 31
```

Result: **31 == 31 — PASS**

The errata does not touch grade/terminal_state; the biconditional is invariant across MAP-ERRATA-1.

---

## Grade histogram

### New 125 rows (basin-5)

| Grade | Count |
|---|---|
| EXACT (E) | 27 |
| CLOSE (C) | 54 |
| APPROX (A) | 13 |
| GAPPED (G) | 31 |
| **TOTAL** | **125** |

File-recount expectation per manifest: E27/C54/A13/G31 — **matches exactly**.

### Full kit_mapping (all 574 rows, post-ingest)

| Grade | Count |
|---|---|
| EXACT | 53 |
| CLOSE | 347 |
| APPROX | 88 |
| GAPPED | 86 |
| **TOTAL** | **574** |

---

## TIER 2 — HOLD

29 docket-candidate rows across 9 side-files
(`docket-candidates-batch-p{01,02,04,05,06,07,11,12,13}.jsonl`) committed as static files.
**NOT ingested to `mechanic_gap_docket`** — held un-ratified per established run pattern.
`mechanic_gap_docket` remains at **8** (the PoE1-ratified set only; ratification + consolidation
happens at THE REVIEW BOOK, not at basin-ingest).

Mint-candidates: **0** (none emitted this basin). No `mint_ledger` write. `mint_ledger` remains
at **6**.

---

## Prior rows untouched

449 pre-existing `kit_mapping` rows (basins 1–4 + basin-2 le-riders) are confirmed untouched:
query `WHERE kit_id NOT IN (basin-5 id list)` returns exactly 449. Zero overwrites.

---

## Pre/post state

| Table | Before | After | Delta |
|---|---|---|---|
| `kit_mapping` | 449 | 574 | +125 |
| `mechanic_gap_docket` | 8 | 8 | 0 |
| `mint_ledger` | 6 | 6 | 0 |
| `canon_corpus` | 585 | 585 | 0 |

---

## Verification

- `PRAGMA integrity_check` = **ok**
- `PRAGMA foreign_key_check` = **clean** (zero rows returned)
- `PRAGMA journal_mode` = **delete**
- Pre-ingest guard 1: all 125 kit_ids in `canon_corpus` — **PASS**
- Pre-ingest guard 2: zero of 125 kit_ids pre-existing in `kit_mapping` — **PASS**
- MAP-ERRATA-1: element_primary=lightning, ailments=[] on ud-lightning-vortex — **APPLIED + VERIFIED**
- MAP-ERRATA-1 guard: grade=CLOSE, terminal_state=MAPPED — **UNCHANGED**
- R-M7: 31 == 31 — **PASS**
- Grade histogram matches file-recount (E27/C54/A13/G31) — **PASS**
- 449 prior rows untouched — **CONFIRMED**
- mechanic_gap_docket = 8 — **UNCHANGED**
- mint_ledger = 6 — **UNCHANGED**

---

## Anomaly log

None. All assertions passed on first execution. No anomalies to report.

---

## Reproducibility + reversibility

Inputs static (committed basin-5 mapping JSONL, 13 files + 9 docket-candidate side-files, all
in `agentic_orchestration/research/vdm1/stage2/basin5/`). Full restore = copy
`corpus.db.pre-vdm1-ingest18-20260718T234606` over `corpus.db` (backup md5
`87bb6b471dbf3e42e56292f6fc577994`).

---

## ADR-004

No engine-telemetry change; star-lord-side MIGRATION.md unaffected (all writes are elrond-seam
corpus curation). Auto-committed per project discipline (Matt-authorized VDM-1 charge).
**NO push — steward (gandalf) pushes per basin checkpoint.**

## Commit note

Pathspec-only: this migration doc + the ingest script. `corpus.db` is gitignored and NOT committed.
Backup + md5 sidecar stay on disk (uncommitted). Basin-5 stage-2 mapping inputs (gandalf's,
static) not touched.
