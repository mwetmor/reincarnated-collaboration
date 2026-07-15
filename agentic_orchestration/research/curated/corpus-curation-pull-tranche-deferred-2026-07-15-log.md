# Corpus curation log — pull-tranche INSERTED then REVERTED (census freeze)

> **STATUS:** CURRENT (record of a completed revert). Edition-II Stage 1-R.
> **Author:** elrond (data steward) · **Date:** 2026-07-15
> **Store:** `agentic_orchestration/research/curated/corpus.db` (elrond-owned, gitignored — this log is the committed record)
> **Batch class:** REVERT (undo of a prior in-flight insert), under a mid-flight Matt ruling.

---

## 0. What this log records

The pull-intrinsic class-kit tranche (legolas `b7f773d3`) was **INSERTED** into corpus.db under
the prior Edition-II brief (Stage 1), then **REVERTED** under Matt's census-freeze ruling issued
mid-flight the same day. This log records **what actually happened** — it does not pretend the
insert never fired. The 7 rows are now **QUEUED post-Edition-II** alongside the full Lost Ark
tranche.

## 1. Matt's ruling (2026-07-15 — the reason for the revert)

Verbatim:

> "Queue the full Lost Ark tranche post-Edition-II… let's not add gravity or anything until post
> edition 2."

Encoded (gandalf ARCHITECT parse, confirmed in parallel):
- **CENSUS FREEZE for Edition-II** — NO new corpus rows curate into corpus.db until
  post-Edition-II. This explicitly includes the 7 pull-tranche rows the prior pass inserted.
- The pull **VOCABULARY** still enters at Edition-II (register v1.2, `pull` as a function level —
  Matt's earlier ruling stands). The pull slice lights ONLY where EXISTING kits re-key on
  evidence (corrections, not additions — C3 precedent). Stage 3.
- The pull-tranche research file is **feasibility EVIDENCE at the research layer** (already
  committed under `research/knowledge/mcd-pull-mechanic/`) — NOT corpus rows this edition.

## 2. What the prior Stage-1 insert did (the full batch footprint reverted)

Script: `agentic_orchestration/research/scripts/corpus_ingest_pull_tranche_2026_07_15.py`
(run **twice** — row upserts are idempotent; the schema_meta INSERT is not). Batch footprint,
verified on disk before the revert:

| # | mutation | detail |
|---|---|---|
| 1 | +7 rows in `canon_corpus` | `la-destroyer-vortex-gravity`, `la-destroyer-gravity-impact`, `la-destroyer-gravity-force`, `la-destroyer-gravity-compression`, `d4-spiritborn-vortex`, `d3-wizard-black-hole`, `di-cyclone-strike-monk-base` (644 → 651) |
| 2 | +7 rows in `canon_engine_key` | same 7 kit_ids, keyed with `function=pull` (6 of 7; gravity-compression `function=none` per flag a) + cell_key (618 → 625) |
| 3 | mech_note SUFFIX-append on 2 EXISTING rows | `di-cyclone-monk-pvp` (+575 chars), `d3-zbarb` (+684 chars) — "EDITION-II ENRICHMENT 2026-07-15" addenda |
| 4 | +`corpus_schema_meta` marker ×2 | `pull-tranche-edition2-stage1-2026-07-15` written twice (script run twice) — meta rows 6 → 8 |

## 3. The revert (Stage 1-R — what I did)

Script: `agentic_orchestration/research/scripts/corpus_revert_pull_tranche_2026_07_15.py`

1. **Confirmed pre-state:** corpus=651, all 7 tranche kit_ids present in both `canon_corpus` and
   `canon_engine_key`, both enrichment markers present, 2 stage-1 meta rows.
2. **Fresh safety copy** (before touching): `corpus.db.pre-revert-2026-07-15-backup` (651 rows).
   The pre-insert backup `corpus.db.pre-edition2-2026-07-15-backup` (644 rows) also on disk.
3. **Reverted ALL FOUR mutation classes** (a pure 7-row delete would leave the enrichment appends
   + meta rows — the identity proof in step 4 forces the whole batch):
   - `DELETE` the 7 kit_ids from `canon_engine_key` (FK child) then `canon_corpus` (parent).
   - **Restored** `di-cyclone-monk-pvp` + `d3-zbarb` `mech_note` **verbatim from the pre-insert
     backup** (provably identity-producing; the enrichment was a pure suffix append).
   - `DELETE` both `pull-tranche-edition2-stage1-2026-07-15` meta rows.
4. **Survivor-integrity proof (in-script, fail-loud):** full `.dump` of the reverted DB diffed
   against the full `.dump` of `corpus.db.pre-edition2-2026-07-15-backup`. Result:
   **0 removed lines; the ONLY additions are the two legitimate Stage-2 register-v1.2 tables**
   (`atlas_feasibility_cuts_v1_2_2026_07_15` + `atlas_feasibility_ladder_v1_2_2026_07_15`, 19
   additive `.dump` lines). Every other object byte-identical → the census is byte-identical to
   pre-insert.
5. **WAL checkpoint** (TRUNCATE); integrity_check = ok; WAL file 0 bytes.

### 3a. Baseline correction (noted for the audit)

The brief's Stage 1-R step 4 assumed "the insert was the only batch since that backup." Verified
on disk, that is **not quite true**: the prior agent's **Stage-2 register-v1.2 generator**
(`feasibility_cuts_register_v1_2_2026_07_15.py`) ALSO ran after the backup was taken and
materialized the two `atlas_feasibility_*_v1_2_2026_07_15` tables into corpus.db. Those are the
**legitimate pull-vocabulary register** (Stage 2 work) and are OUT of the census-freeze revert
scope — they STAY. The honest identity invariant is therefore: **reverted DB == pre-insert backup
+ exactly the two v1.2 register tables, nothing else** — asserted precisely, fail-loud on any
deviation. The census tables (`canon_corpus`, `canon_engine_key`) are byte-identical to pre-insert.

## 4. Proven final state

| table | pre-insert backup | current (reverted) | pre-revert safety copy |
|---|---|---|---|
| `canon_corpus` | 644 | **644** | 651 |
| `canon_engine_key` | 618 | **618** | 625 |
| `corpus_schema_meta` | 6 | **6** | 8 |
| 7 tranche rows present | 0 | **0** | 7 |
| enrichment markers | 0 | **0** | 2 |

- **Dump-clean:** census byte-identical to `corpus.db.pre-edition2-2026-07-15-backup`; only
  addition = the two v1.2 register tables (legitimate Stage 2).
- **WAL:** checkpointed, 0 bytes. **integrity_check:** ok.

## 5. Disposition of the 7 rows (QUEUED, not discarded)

The 7 pull-intrinsic rows are **queued for post-Edition-II curation**, to land alongside the full
Lost Ark tranche (Matt's "queue the full Lost Ark tranche post-Edition-II"). Their curation is
fully worked out and reversible-ready:
- **Keying is settled** — the insert script's manifest (source-anchored to the tranche table)
  carries the full 14-slot cell_key per row, gandalf's 5 flags dispositioned, and the Stage-0
  hybrid verdicts (both proposed hybrids → damage-primary + pull rider). Re-applying is a
  re-run of the (idempotent) insert script post-Edition-II.
- **The evidence is durable** — `research/knowledge/mcd-pull-mechanic/2026-07-15-pull-intrinsic-classkit-tranche.md`
  (committed) is the standing feasibility record; this edition it serves as RED-3′-adjacent
  vetting evidence + the ecology-annotation source for register v1.2, NOT as corpus rows.
- **This edition** the pull slice is lit only via Stage-3 re-keys of EXISTING corpus kits
  (`d3-zbarb`, `di-cyclone-monk-pvp`, the 6 mcd- pull kits) — corrections, not additions.

## 6. Provenance

- **Revert script (committed):** `research/scripts/corpus_revert_pull_tranche_2026_07_15.py`
- **Insert script (committed, from the prior brief):** `research/scripts/corpus_ingest_pull_tranche_2026_07_15.py`
- **Backups (local, gitignored):** `corpus.db.pre-edition2-2026-07-15-backup` (pre-insert, 644),
  `corpus.db.pre-revert-2026-07-15-backup` (pre-revert safety, 651).
- **Ruling authority:** Matt 2026-07-15 (census freeze, quoted §1); Edition-II chain spec §10.

---

**Signed:** elrond (data steward) — the log records that the insert fired and was reverted; it
does not rewrite the record to pretend otherwise. The rows are queued, the evidence is durable,
the census is frozen, and the vocabulary enters clean.
