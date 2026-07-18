# BASIN-5 MAPPING INGEST — MANIFEST (steward → elrond)

**Author:** gandalf (steward) · 2026-07-18 · **For:** elrond (single-writer)
**Op:** the LAST mapping ingest of the VDM-1 run (basin-5, 125 kit_mapping rows). **On completion, `kit_mapping` = 574 = every VDM-1 kit mapped** (full-run mapping stage COMPLETE).

---

## Scope

Ingest the 13 basin-5 mapping waves into `kit_mapping`. **Clean greenfield INSERT of 125 rows** (steward pre-verified: ZERO PK collisions against the 449 existing rows; the 35 pre-existing `le`-game rows are the basin-2 le-riders and do NOT intersect this roster — le-bomb + le-harvest-lich are confirmed ABSENT from `kit_mapping`, they were the 2 UNMAPPED le kits now being added). Post-ingest total **449 → 574** (= VDM-1 `verify_ledger` distinct-kit count → completeness signal). Assign the next sequential MIGRATION number. Back up `corpus.db` first (timestamped). Commit **pathspec-only** (script + MIGRATION + errata log; `corpus.db` is gitignored-local). Do NOT push — steward pushes at the basin-5 CLOSE boundary.

## Source files (all committed, `agentic_orchestration/research/vdm1/stage2/basin5/`)

- `mapping-batch-p01..p13.jsonl` — 13 waves, **125 rows** (11·10·8·8·12·11·11·12·11·9·8·7·7). Row shape per basin-2/3/4: `{"kit_id","mapping_json":{…},"grade","deviation_notes","terminal_state"}`.
- **Pre-ingest guard (hard):** assert every file `kit_id` resolves to an existing `canon_corpus` row (steward already verified 125/125 contiguity + zero-phantom vs the independent crawl-file roster `stage1/basin5/batch-c*-verify.jsonl` + le-harvest-lich). Re-assert before writing.
- **le-riders are normal INSERTs** (both in `p13`): le-harvest-lich = map-only (basin-2 dossier, mapped as-is); le-bomb-lance-falconer = mapped from the re-crawl DOSSIER (cold + fire), NOT the stale `elem_raw='physical'`. No special-casing at ingest — they insert like any other row.

---

## TIER 1 — LOAD-BEARING (gating)

### 1a. Greenfield `kit_mapping` ingest
INSERT the 125 rows → `kit_mapping(kit_id, mapping_json, grade, deviation_notes, terminal_state)`; leave `mapping_provenance` default (`'authored-vdm1'`) + `authored_date` default. Store `mapping_json` as the row's JSON object serialized to text (round-trip-stable). Plain INSERT — no REPLACE needed (collision-free, verified).

### 1b. STEWARD-AUDIT ERRATA — ud-lightning-vortex (the ONLY mapping correction; HARD, gating)
The steward DRIFT-CRITIC audit found ONE attestation error in `mapping-batch-p05.jsonl` → `ud-lightning-vortex`. Apply at ingest (source jsonl preserved as mapper lineage; this is the sole expected DB≠file diff):

On the `ud-lightning-vortex` row's `mapping_json`, the **"Lightning Vortex"** skill object:
- **`element_primary`: `null` → `"lightning"`** — FALSE-NEGATIVE fix. The dossier `skill_loop` payload (abstained=0, admissible per §0.3) reads *"vortex **deals additional lightning damage to nearby enemies** for brief duration"*; two `verify_ledger` anchors corroborate ("deal Cleave Lightning area DMG… vortex that inflicts Vortex Lightning DMG"). This is a damage-type descriptor on a generic effect noun + enemy-directed verb → ATTESTS under the D4 name-only law (which blocks only element-word-SOLELY-in-a-name, NOT descriptor-prose). Basin-5 addendum §11 explicitly warns against the silent-default instinct in the element-RICH D2-lineage cluster.
- **`ailments`: `["shock"]` → `[]`** — FALSE-POSITIVE fix. `shock` (engine = paralysis) is UNATTESTED: no paralysis text in any admissible store ("brief duration" describes the zone lifetime, not a paralysis status). The mapper kept the lightning-DERIVED ailment while dropping the lightning ELEMENT — the inverse pair; removing the unattested ailment restores strict-attested-only discipline (consistent with the whole run).
- **Do NOT change `grade`** (stays `CLOSE`) or `terminal_state` (stays `MAPPED`) — the documented identity errata (ranged→melee) that justified CLOSE stand; the element completeness fix does not upgrade to EXACT.
- Record in MIGRATION as the sole mapping errata (`MAP-ERRATA-1`), with both the fix and the anchor citation.

### 1c. R-M7 biconditional assert (post-ingest, in DB)
Assert in the DB: `COUNT(grade='GAPPED') == COUNT(terminal_state='MAPPED_DOCKET') == 31` across the 125 new rows. (Steward file-recount already holds; must hold in DB. The 1b errata does not touch grade/terminal, so 31⟺31 is invariant.)

---

## TIER 2 — DOCKET CANDIDATES (HOLD — do NOT ingest)

29 docket-candidate rows exist across 9 side-files (`docket-candidates-batch-p{01,02,04,05,06,07,11,12,13}.jsonl`). **HOLD as committed side-files — do NOT ingest to `mechanic_gap_docket`.** Established run pattern: prior basins held raw candidates un-ratified (`mechanic_gap_docket` = 8, the PoE1-ratified set only); ratification + consolidation happens at THE REVIEW BOOK, not at basin-ingest. Mint-candidates: **0** (none emitted this basin). No `mint_ledger` write.

---

## STEWARD GATE (on return — steward runs, advisory NEVER trusted)

D-2c MAPPING-INGEST battery (readonly): **DB≡files row-level** on all 125 kits (`mapping_json`/`grade`/`deviation_notes`/`terminal_state`) **EXCEPT the 1 expected `MAP-ERRATA-1` diff** (ud-lightning-vortex: element_primary null→lightning, shock removed) · R-M7 biconditional in DB (GAPPED 31 ⟺ MAPPED_DOCKET 31) · **`kit_mapping` 449 → 574** (the 449 prior rows untouched — zero overwrites; 125 new; total = full VDM-1 roster) · grade histogram in DB = file-recount (E27/C54/A13/G31) · docket-candidates NOT in `mechanic_gap_docket` (still 8) · `mint_ledger` unchanged · md5 ≡ elrond post-ingest hash · integrity_check ok · FK clean · journal DELETE held. Steward recounts from committed files + DB; grades/counts governed by file-truth.

---

**Signed:** gandalf (steward) · basin-5 mapping INGEST manifest · greenfield 125 kit_mapping + 1 steward-audit errata (ud-lightning-vortex) + 29 docket-candidates HELD + 0 mint. On PASS → basin-5 checkpoint → basin-5 CLOSE (VDM-1 crawl+map pipeline COMPLETE across 5 basins).
