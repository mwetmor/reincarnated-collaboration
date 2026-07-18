# MIGRATION — VDM-1 ingest wave 7 (D-5 poedb backfill, fill-only merge)

**Date:** 2026-07-18
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1
**Script:** `agentic_orchestration/research/curated/scripts/corpus_vdm1_ingest7_2026_07_18.py`
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged; readonly basin-1 crawl agents + a basin-2 spec-gen
agent read concurrently — NEVER flipped to WAL; write txn kept short)

**Scope — one job:** the D-5 poedb sweep backfilled the two structurally-sparse
dossier families (`capstone_alterations`, `item_alterations`) for PoE1. This is a
**FILL-ONLY enrichment merge**: a backfill row lands ONLY where the existing stage-1
`kit_dossier` row for that `(kit_id, family)` is abstained (or absent). Stage-1
guide-tier fills are primary and are NEVER overwritten. The 8 backfill rows that are
themselves abstained do NOT land — the stage-1 abstention already records the silence.
gandalf steward-repaired the input's schema deviations before handoff (abstained rows
strictly null-payload/null-conf; conf as numeric 0.9/0.75/0.5) — see the STEWARD AUDIT
+ REPAIR ADDENDUM at the bottom of `backfill-capstone-items-summary.md`.

---

## Backup

- **File:** `corpus.db.pre-vdm1-ingest7-2026-07-18-backup`
- **md5:** `072ec2729982a7874918b8383f6d5cd4` (matched live DB at backup time; also
  matches the post-ingest6 live md5 — clean lineage, no intervening write)
- **post-ingest live md5:** `b998581dd185be2b5f6545cbd5f774f5`

(Backup is gitignored via `*-backup`, same as `corpus.db` via `*.db` — retained on
disk for reversibility, not committed. The dispatch's suggested timestamp-suffix name
was renamed to the established `-backup` convention so it is ignored like ingest-1..6.)

---

## Inputs (committed, static — under `.../vdm1/stage1/poe1/`)

| File | Rows | Destination |
|---|---|---|
| `backfill-capstone-items-dossier.jsonl` | 94 (86 non-abstained · 8 abstained) | `kit_dossier` (fill-only) |
| `backfill-capstone-items-citations.jsonl` | 66 | `kit_citations` (derived kit_id + dedupe) |

Both parsed clean (`load_jsonl` runs `json.loads` per line; **0 malformed**).

---

## JOB — fill-only dossier merge + citation append

### THE FILL-ONLY LAW (binding)

A backfill dossier row lands ONLY where the existing stage-1 `kit_dossier` row for
`(kit_id, family)` is abstained (or absent). NEVER overwrite a non-abstained stage-1
row. Backfill rows themselves abstained do NOT land (skip + count).

Pre-write guard: exactly ONE `kit_dossier` row exists per `(kit_id, family)` in the
target families for PoE1 (asserted; 0 multi-row keys → no `UNIQUE(kit_id, family,
source_url)` risk). Every FLIP is an in-place single-row `UPDATE … WHERE kit_id=? AND
family=? AND abstained=1` — the `abstained=1` clause is a belt-and-braces guard so a
non-abstained (primary) row can never be clobbered; each flip asserted `rowcount==1`.

### Dossier landing (per family)

| family | flip (abst→fill) | insert-new | skip-non-abstained | skip-abstained |
|---|---|---|---|---|
| `capstone_alterations` | **57** | 0 | 0 | 1 |
| `item_alterations` | **29** | 0 | 0 | 7 |
| **TOTAL** | **86** | **0** | **0** | **8** |

- **All 86 non-abstained backfill rows FLIP** abstained→filled. Every one of the 94
  PoE1 kits already carried a stage-1 **abstained** row for BOTH families (incl.
  `poe1-incinerate` item_alterations — the addendum hedged it might be pre-filled from
  stage-1; **file truth: it was abstained**, so it flips). **0 inserts** (no absent
  `(kit,fam)` rows), **0 skip-non-abstained** (no stage-1 row was already filled).
- **`kit_dossier` row count UNCHANGED (564 → 564)** — flips are in-place UPDATEs; only
  inserts change the count, and there were none. Asserted `post == pre + inserts`.
- **8 skipped-abstained** (do NOT land — the exact still-silent set from the summary):
  - capstone_alterations ×1: `poe1-sweep`
  - item_alterations ×7: `poe1-edc`, `poe1-icicle-mines`, `poe1-lightning-conduit`,
    `poe1-seismic-trap`, `poe1-soulrend`, `poe1-storm-brand`, `poe1-sweep`
  - Each asserted null-payload AND null-conf on input (steward-repair verified).

### Provenance stamp

Flipped/inserted rows stamped `extraction_provenance = 'd5-backfill'` — the FIRST
non-default value in `kit_dossier` (ingests 1-6 all landed the column default
`'fetched-vdm1'`). The D-5 catalogue sweep is a distinct enrichment source vs the
stage-1 guide-tier fills; stamping it lets a reader partition guide-tier from
catalogue-backfill provenance. No schema change (column already accepts arbitrary
TEXT). Post-write: exactly **86** rows carry `d5-backfill`.

`conf` histogram on the 86 landed rows (verbatim from the steward-repaired float map):
**0.9 ×78** (direct poedb verbatim) · **0.75 ×1** (mjolner, WebSearch-snippet recovery,
one hop weaker) · **0.5 ×7** (variant names captured, zero mechanic-diff text: edc,
icicle-mines, lightning-conduit, seismic-trap, soulrend, storm-brand, tornado-shot —
all capstone_alterations).

### Abstention rates (PoE1, per family — before → after)

| family | before | after | Δ (= flips) |
|---|---|---|---|
| `capstone_alterations` | 58 / 94 | **1 / 94** | −57 |
| `item_alterations` | 36 / 94 | **7 / 94** | −29 |

Post-write abstention drop equals the per-family flip count exactly (asserted).

### Citations — derived kit_id + dedupe (66 input rows)

**Structural note:** the D-5 crawl was **skill-batched, not kit-batched**, so its
citation file is **URL-keyed and carries NO `kit_id`** — unlike the stage-1 batch
citation files (ingest-4) which carried an explicit per-row `kit_id`. `kit_citations`
requires `kit_id NOT NULL` with `UNIQUE(kit_id, url)`, so each citation's `kit_id` is
**DERIVED deterministically** (no fabrication — every derivation traces to a dossier
row or a payload-subject match):

- **PRIMARY** (58 URLs): url == a non-abstained backfill dossier row's `source_url`
  → that row's kit_id(s). **4 URLs fan to 2 kits** (shared core skill across kits:
  Flameblast, Cast_On_Critical_Strike_Support, Blade_Vortex, Siege_Ballista); each
  fanned kit is cited (page-provenance-per-kit, matching how stage-1 recorded the same
  shared pages).
- **SECONDARY** (8 URLs): supporting/cross-reference pages (a unique-item page, a
  keystone page, a co-skill page) fetched WHILE building another kit's dossier — not
  any row's primary `source_url`. Mapped by payload-subject match to the owning kit:

  | URL | owning kit | basis |
  |---|---|---|
  | `unique.php?n=Mjölner` | `poe1-mjolner` | Mjolner trigger line = mjolner capstone payload |
  | `us/Ancestral_Bond` | `poe1-pizza-sticks` | Ancestral Bond keystone in pizza-sticks payload |
  | `us/Cyclone` | `poe1-hoag` | "Cyclone of Tumult … HoAG poison applier" (crawl note) |
  | `us/Earthshatter_of_Prominence` | `poe1-earthshatter` | Earthshatter transfig in payload |
  | `us/Herald_of_Agony` | `poe1-hoag` | HoAG core skill page |
  | `us/Minion_Instability` | `poe1-srs` | MI keystone (SRS is the MI archetype) |
  | `us/Sweep` | `poe1-sweep` | Sweep skill page (kit abstained — supporting silence) |
  | `us/Volatile_Dead` | `poe1-poets-pen-vd` | VD transfig in payload |

  Cross-validation: **3 of these 8** (Herald_of_Agony→hoag, Volatile_Dead→poets-pen-vd,
  Sweep→sweep) **already exist** in `kit_citations` under exactly these derived kits —
  confirming the derivation, and deduping out.

**Dedupe discipline** (same `UNIQUE(kit,url)` contract as ingests 1-6): skip any
`(kit_id, url)` already in `kit_citations`; skip within-batch dupes; count both.

- new (kit,url) landed: **16** · dedup-existing: **54** · dedup-within: **0** ·
  orphan/unmapped: **0** (every citation resolves to a real `canon_corpus` kit).
- `kit_citations` **269 → 285 (+16)**.
- 54 dedupe-existing = these poedb pages were already cited in stage-1 under the SAME
  derived kits (strong corroboration of the URL→kit derivation).
- Field map: input `class='communal'` (all 66) → `cite_class='communal'`;
  `rank_class='attested-era'` (live pages fetched 2026-07-18 — current attestation,
  not a recovered Wayback snapshot); `archive_url ← snapshot` (all null);
  `accessed_date ← access_date`; `quarantined=0`; `title` NULL (input carries none).
  The input `notes` field is provenance-narrative, not a `kit_citations` column — it
  is preserved in the committed input file (no column home; no datum lost).

---

## Post-ingest asserts (all pass — in-script AND independent readonly query)

| # | Assert | Result |
|---|---|---|
| 1 | `kit_dossier` total == pre + inserts (0) | 564 → **564** ✓ |
| 2 | `kit_citations` total == pre + 16 | 269 → **285** ✓ |
| 3 | flipped == 86 (each `rowcount==1`, guarded `abstained=1`) | **86** ✓ |
| 4 | flip + insert + skip-non-abstained == 86 | **86** ✓ |
| 5 | skip-abstained == 8 | **8** ✓ |
| 6 | `d5-backfill` provenance rows == 86 | **86** ✓ |
| 7 | conf histogram (0.9×78 / 0.75×1 / 0.5×7) | ✓ |
| 8 | capstone abstention 58 → 1 (Δ = −57 flips) | ✓ |
| 8 | item abstention 36 → 7 (Δ = −29 flips) | ✓ |
| 9 | abstained-with-payload (no-fabrication) | **0** ✓ |
| 10 | filled(abstained=0)-with-null-payload | **0** ✓ |
| 11 | citation orphan (kit absent from canon_corpus) | **0** ✓ |
| 12 | `PRAGMA journal_mode` == delete | delete ✓ |
| — | `PRAGMA integrity_check` | ok ✓ |
| — | `PRAGMA foreign_key_check` | empty ✓ |

---

## Errata ledger

**Not touched.** This wave is pure enrichment — every landed row's payload/conf/anchor
came from the steward-repaired D-5 file; the 8 still-silent rows are recorded silences,
not factual contradictions. No `errata_applied` flag is set (that convention is for
CONTRADICTED verify rows; this ingest writes no verify rows). `errata_applied` total
stays **12** (unchanged from ingest-4/6). One self-report-vs-file-truth note (already
captured by gandalf in the summary addendum, not an errata): the addendum hedged
`poe1-incinerate` item_alterations might be pre-filled from stage-1; file truth is it
was abstained and flipped here. No errata-ledger entry warranted.

---

## Reproducibility + ADR-004 + reversibility

Inputs committed + static. Dry-run (no `--apply`) validates and reports all counts —
the 57/29 per-family flips, the 86/0/0/8 totals, the 16-new/54-dedup citation split —
without writing; re-running `--apply` against `corpus.db.pre-vdm1-ingest7-2026-07-18-backup`
reproduces this state exactly. The write path is a single `BEGIN IMMEDIATE … COMMIT`
(short txn; concurrent readonly crawlers unaffected), opened through an index.lock-retry
wrapper (wait 30s, retry 3×; **0 retries fired**). journal_mode kept DELETE throughout.

No engine-telemetry change; star-lord-side `MIGRATION.md` unaffected (all writes are in
elrond's seam: 86 in-place `kit_dossier` flips + 16 `kit_citations` inserts). Reversible:
the backup restores the exact PRE state; or the flips revert by re-abstaining the 86
`extraction_provenance='d5-backfill'` rows (payload/source_url/anchor→null, abstained→1,
conf→null) and the citations by `(kit_id, url)` on the 16 landed pairs. Auto-committed
per project discipline (Matt-authorized VDM-1 charge).

---

## Commit note

Pathspec-only commit (matches ingest-1..6 precedent exactly): migration doc + ingest
script. `corpus.db` and the backup are gitignored (`*.db` / `*-backup`; verified via
`git check-ignore`) and are NOT committed. The static JSONL inputs live under
`.../vdm1/stage1/poe1/` and are gandalf's crawl artifacts (committed on the crawl side).
**No push** (steward pushes per charter + ADR-006).
