# MIGRATION — VDM-1 ingest wave 8 (FIRST basin-1 ingest: PoE2 b01+b02 + adjudications + roster hygiene)

**Date:** 2026-07-18
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1 (basin-1)
**Script:** `agentic_orchestration/research/curated/scripts/corpus_vdm1_ingest8_2026_07_18.py`
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged; concurrent readonly basin-1 b03/b04 crawl agents
+ parallel git commits — NEVER flipped to WAL; single write txn kept short; index.lock
retry wrapper wait 30s / retry 3× — **0 retries fired**)

**Scope — four parts (dispatch):** (1) standard stage-1 ingest of the first two
basin-1 PoE2 batches (kits 1-24) into `verify_ledger` / `kit_citations` /
`kit_dossier`, mirroring the ingest-1..4 PoE1 practice exactly; (2) a 3-kit era
adjudication docket (ERRATA-16/17/18) + a phantom-mechanic REVIEW (erasure, no data
change); (3) 3 `mech_note` annotations (no restamps); (4) 2 basin-2 roster-hygiene
fixes. This is the FIRST PoE2 landing (0 poe2 verify rows existed pre-wave).

---

## Backup

- **File:** `corpus.db.pre-vdm1-ingest8-2026-07-18-backup`
- **md5:** `b998581dd185be2b5f6545cbd5f774f5` (matched live DB at backup time; also
  matches the post-ingest7 live md5 — clean lineage, no intervening write)
- **post-ingest live md5:** `e8c95af487a3432ef8182a5bb8d98b29`

(Backup is gitignored via `*-backup`, same as `corpus.db` via `*.db` — retained on
disk for reversibility, not committed. `-backup` suffix per the established ingest-1..7
convention so it is ignored like prior waves.)

---

## Inputs (committed, static — under `.../vdm1/stage1/basin1/`)

Row counts RECOUNTED from files (file-truth governs; matched the dispatch statement):

| File | Rows | Destination |
|---|---|---|
| `batch-01-verify.jsonl` | 38 (28 CONFIRMED / 2 CONTRADICTED / 8 UNSUPPORTED) | `verify_ledger` |
| `batch-02-verify.jsonl` | 60 (56 C / 2 X / 2 U) | `verify_ledger` |
| `batch-01-citations.jsonl` | 36 | `kit_citations` (dedupe) |
| `batch-02-citations.jsonl` | 34 | `kit_citations` (dedupe) |
| `batch-01-dossier.jsonl` | 72 (24 abstained) | `kit_dossier` |
| `batch-02-dossier.jsonl` | 72 (16 abstained) | `kit_dossier` |

All six files parsed clean (`load_jsonl` runs `json.loads` per line; **0 malformed**).
Kit coverage 12 + 12 = **24 distinct poe2 kits** (kits 1-24); the verify kit-set and the
dossier kit-set are **identical** (0 verify-only, 0 dossier-only).

---

## PART 1 — standard stage-1 ingest

### verify_ledger (+98)

- b01 **38** / b02 **60** = **98** landed. All families/verdicts pass the schema
  CHECK enums; all 24 kit_ids resolve to `canon_corpus` rows (0 FK rejects).
- **Filler-drop rule fires 0×.** The ingest-4 rule (negative_canon UNSUPPORTED on a
  `negative=0` kit → DROP) is retained; all 3 negative_canon rows in these batches sit
  on `negative=1` kits (`poe2-chronomancer-01`, `poe2-concoction` UNSUPPORTED;
  `poe2-perfect-strike-01` CONFIRMED), so none drops. All 98 rows land as stated —
  the dispatch counts are the FULL file counts, no post-drop reconciliation.
- Boolean-drift guard (`coerce_bin`) retained; b01/b02 emit INTEGER 0/1 → **0 coercions**.

### kit_citations (+70)

- b01 **36** / b02 **34** = 70 input rows. **Dedupe:** 0 dedup-existing (first PoE2
  landing — no `(kit,url)` collision with the 285 prior rows), 0 within-batch dupes →
  all **70 land**. 0 orphan/unmapped (every citation kit_id resolves to `canon_corpus`).
- Field map (same as ingest-4): `cite_class` {communal 36, dataset 15, authored 17,
  official 2} → `cite_class`; `rank_class='attested-era'` (all 70, live 2026-07-18
  fetches); `quarantined=0` (all); `archive_url ← archive_url`; `accessed_date`,
  `site`, `author_handle`, `title` mapped 1:1.

### kit_dossier (+144)

- b01 **72** / b02 **72** = 144 landed (12 kits × 6 families × 2 batches). **Abstained:**
  b01 **24** / b02 **16** = 40; every abstained row is payload-NULL on input
  (**0 abstain-payload-stripped** — the steward-pre-verified clean claim held under the
  in-script abstain⇒NULL law). **0 string-conf** (all `conf` numeric or null).
- Provenance: all 144 land the column default `extraction_provenance='fetched-vdm1'`
  (per stage-1 convention; contrast ingest-7's `d5-backfill`). Post-write there are
  **622** `fetched-vdm1` dossier rows (478 prior stage-1 + 144 this wave; the 86
  `d5-backfill` rows are the remainder of 708).

---

## PART 2 — adjudication docket (ERRATA-16/17/18 + REVIEW-2)

Each restamp is a guarded single-row `UPDATE canon_corpus SET eras=? WHERE kit_id=? AND
eras=?` (asserted `rowcount==1` against the EXACT current value). `errata_applied=1` is
set ONLY on CONTRADICTED-era verify rows (the established convention — ingest-6 header /
errata-ledger). Full rationale in the errata ledger; one-line summaries here.

| # | kit | old eras | new eras | class | flags |
|---|---|---|---|---|---|
| ERRATA-16 | `poe2-acolyte-darkness` | `0.1;0.2-dawn` | `0.3-edict;0.4;0.5-ancients` | D-2a-to-limit (both stamped bands predate the 0.3.0 debut; restamp to attested 0.3-0.5) | 1 |
| ERRATA-17 | `poe2-concoction` | `0.2-dawn;0.3-edict;0.4;0.5-ancients` | `0.1;0.2-dawn;0.3-edict;0.4;0.5-ancients` | **floor-too-LATE (NEW)** — extend floor to attested 0.1 (BACKFILL shape, but a CONTRADICTED era row landed ⇒ flagged) | 1 |
| ERRATA-18 | `poe2-grim-feast` | `0.2-dawn;0.3-edict;0.4` | `0.2-dawn` | ERRATA-8/11 trim — ES-overleech died at the 0.3.0 rework; drop the 2 post-rework bands | 2 |

- **ERRATA-16 (acolyte-darkness):** Into the Breach poe2db version history STARTS at
  v0.3.0 (runs through v0.5.0). Both stamped bands (0.1, 0.2-dawn) predate the debut, so
  the naive floor-narrow empties the stamp. Per the ERRATA-11 rule (drop unattested bands
  + restamp to the crawl-attested later window), the corrected value is the attested
  0.3-0.5 window. Verified the crawler's anchor in `batch-01-verify.jsonl` first: era row
  CONTRADICTED, anchor "version history starting from v0.3.0, with updates continuing
  through v0.5.0". 1 flag (the single CONTRADICTED era row, claim "0.1, 0.2-dawn").
- **ERRATA-17 (concoction):** the maxroll Poisonous Concoction guide carries "Adjusted
  build for patch 0.1.0e Hotfix 6" — attested presence in 0.1, one band BELOW the stamped
  floor 0.2-dawn. The stamped floor postdates attested presence (inverse of D-2a). RULING:
  **extend the floor to 0.1** (fill-from-verified-crawl, BACKFILL-1 VBV precedent) rather
  than leave + annotate — the attestation is a specific, dated hotfix guide, so the fill is
  evidence-grounded. Flag discriminator vs BACKFILL-1: BACKFILL-1's era row was CONFIRMED
  (no flag); here the era row is CONTRADICTED (the stamp is internally inconsistent re: 0.1
  presence) ⇒ flag. Later four bands untouched.
- **ERRATA-18 (grim-feast):** Grim Feast was "completely reworked and re-enabled" at 0.3.0
  (poe2db) — the ES-overleech identity the kit describes existed ONLY in 0.2-dawn; the
  0.3.0+ skill is a DIFFERENT mechanic (minion-revival). The b02 era rows split granularly:
  1 CONFIRMED (0.2-dawn) + 2 CONTRADICTED (0.3-edict, 0.4). TRIM to `0.2-dawn`. **Split-kit
  (ES vs post-rework Grim Resurrection) considered and REJECTED** as overkill for one kit —
  the trim + a `mech_note` annotation record the rework boundary losslessly. FIRST errata to
  flag **2** rows on one kit (paired-band drop; the ERRATA-8 seismic-trap shape flagged 1
  because only 1 band was contradicted). The CONFIRMED 0.2-dawn row is NOT flagged.

**errata_applied total: 12 → 16** (+1 acolyte, +1 concoction, +2 grim-feast). Post-write
audit: 0 flagged rows are non-era-CONTRADICTED.

### REVIEW-2 (basin-1) — `poe2-erasure-edc-lich` "Erasure" phantom-mechanic (NO data change)

- Crawl reports "Erasure" 404s on poe2db and is absent from all lich/witch sources;
  Essence Drain + Contagion CONFIRMED. "Erasure" appears in `core_skills`
  `["Essence Drain lineage","Contagion","Erasure"]` AND in `mech_note`.
- **Investigated the canon_corpus row.** "Erasure" IS in core_skills → annotated it as
  unverified-possible-phantom in `mech_note` (append). **NOT deleted** — mirrors how
  earthshatter's phantom alias was handled (REVIEW-1) and the `di-spiritform-druid-pvp`
  PHANTOM precedent. no-silent-edits: SOURCE-NOT-FOUND is honest silence, not disproof.
- **REVIEW-2 stays OPEN for Matt-tier review.** The era verify row is CONFIRMED → no
  `errata_applied`; identity+mechanics UNSUPPORTED are honest silences captured by the
  landing-zone verify rows.

---

## PART 3 — mech_note annotations (no restamps)

The annotation home is `canon_corpus.mech_note` (established for phantom/lineage notes —
see `di-spiritform-druid-pvp` PHANTOM note + the PoE1 demon-form-class notes). Each is a
guarded single-row `UPDATE` (rowcount==1) that **PREPENDS** a dated `[VDM-1 basin-1
2026-07-18]`-tagged clause; the original harvest note is preserved verbatim AFTER the
clause (no-silent-transformation — the stale `Era=...` substrings inside the original
notes are left intact, superseded by the tagged clause + the restamped `eras` column).

| kit | annotation |
|---|---|
| `poe2-demon-form` | element framing MISLEADING — Demon Form is element-AGNOSTIC (Spark/lightning + cold + fire variants all attested); "fire spells in-form" is not the defining/exclusive mechanic. No element/eras restamp this wave (element correction is stage-later). |
| `poe2-minion-infernalist` | (a) Infernalist→Lich lineage shift (Infernalist hosted 0.1/0.2, Lich dominant 0.3+; class field understates lineage); (b) "Loyal Hellhound" alias in core_skills UNSUPPORTED — actual skill name "Summon Infernal Hound"; alias NOT deleted. |
| `poe2-infernal-legion` | Infernalist→Lich lineage shift (Infernalist dominant 0.1/0.2 per Kripp Dec2024/Jan2025; current maxroll guide = Lich); era stamps CONFIRMED; class field understates lineage. |
| `poe2-erasure-edc-lich` | (the REVIEW-2 phantom clause above) |

Preservation verified post-write: "Erasure" remains in `poe2-erasure-edc-lich`
core_skills; "Loyal Hellhound" remains in `poe2-minion-infernalist` core_skills; all 4
notes start with the `[VDM-1 basin-1 2026-07-18]` tag.

---

## PART 4 — basin-2 roster hygiene

| # | kit | fix |
|---|---|---|
| R1 | `le-ring-of-shields` | `corpus_bucket` `'poe1'` → `'le'` (provenance error; kit is Last Epoch). eras + core_skills NULL → **left NULL** (kb-absent). |
| R2 | `le-shift-bladedancer` | bucket already `'le'` (correct) → **no write**; eras + core_skills NULL → left NULL (kb-absent). |

- **R1 verified before fixing:** the kit is LE (id prefix `le-`); the correct sibling
  bucket value is `'le'` (36 of 37 `le-` rows carry `'le'`; `le-ring-of-shields` was the
  **sole** outlier at `'poe1'`). Guarded single-row `UPDATE ... WHERE kit_id=? AND
  corpus_bucket='poe1'` (rowcount==1). Post-write: **0** `le-` rows remain non-`le`.
- **kb-source silence documented:** neither LE kit exists in the mobile-JSONL kb source
  (`claude-mobile-session-docs/ARPG-canonical-kit-research/**/canon-corpus-*.jsonl` — 17
  files searched; both ABSENT). The dispatch's honest-fill rule ("fill if kb has values,
  else leave NULL for the basin-2 crawl to verify") therefore resolves to **leave NULL**
  for eras + core_skills on both. Only the R1 bucket is written.
- **R2 is documented, not written** (verified-correct bucket + intentional-NULL-left).
  Asserted in-script (bucket=='le', eras IS NULL, core_skills IS NULL — unchanged).

---

## Post-ingest asserts (all pass — in-script AND independent readonly query)

| # | Assert | Result |
|---|---|---|
| 1 | `verify_ledger` == pre + 98 | 345 → **443** ✓ |
| 2 | `kit_citations` == pre + 70 (0 dedupe) | 285 → **355** ✓ |
| 3 | `kit_dossier` == pre + 144 | 564 → **708** ✓ |
| 4 | `canon_corpus` UNCHANGED | 585 → **585** ✓ |
| 5 | verify b01/b02 == 38/60 | ✓ |
| 6 | filler-drop == 0 | ✓ |
| 7 | dossier abstained b01/b02 == 24/16 | ✓ |
| 8 | abstain-payload-stripped == 0 | ✓ |
| 9 | bool coercions == 0 | ✓ |
| 10 | citation input total (landed+deduped) == 70 | ✓ |
| 11 | errata_applied == 12 + 4 == 16 | ✓ |
| 12 | flagged rows all era/CONTRADICTED | 0 bad ✓ |
| 13 | per-kit flags: acolyte 1 / concoction 1 / grim-feast 2 | ✓ |
| 14 | 3 restamped eras land exactly | ✓ |
| 15 | roster bucket `le-ring-of-shields` == 'le'; 0 `le-` outliers | ✓ |
| 16 | `le-shift-bladedancer` unchanged (le / NULL / NULL) | ✓ |
| 17 | "Erasure" retained in core_skills (not deleted) | ✓ |
| 18 | "Loyal Hellhound" retained in core_skills (not deleted) | ✓ |
| 19 | all 4 mech_note annotations prepended | ✓ |
| 20 | landing-zone orphans (verify/cite/dossier) | 0 / 0 / 0 ✓ |
| — | `PRAGMA journal_mode` == delete | delete ✓ |
| — | `PRAGMA integrity_check` | ok ✓ |
| — | `PRAGMA foreign_key_check` | empty ✓ |

---

## Reproducibility + ADR-004 + reversibility

Inputs committed + static. Dry-run (no `--apply`) validates and reports all counts —
the 38/60 verify, 36/34→70 citations, 72/72 dossier (24/16 abstained), the 3 restamps
+ 4 flags, the roster fix — without writing; re-running `--apply` against
`corpus.db.pre-vdm1-ingest8-2026-07-18-backup` reproduces this state exactly. The write
path is a single `BEGIN IMMEDIATE … COMMIT` (short txn; concurrent readonly b03/b04
crawlers + their parallel commits unaffected), opened through an index.lock-retry wrapper
(wait 30s, retry 3×; **0 retries fired**). journal_mode kept DELETE throughout.

No engine-telemetry change; star-lord-side `MIGRATION.md` unaffected (all writes are in
elrond's seam: 98 `verify_ledger` + 70 `kit_citations` + 144 `kit_dossier` inserts; 3
`canon_corpus.eras` restamps; 1 `canon_corpus.corpus_bucket` fix; 4 `canon_corpus.mech_note`
appends). Reversible: the backup restores the exact PRE state; or each restamp/fix reverts
by re-writing the prior value (the errata-ledger records old→new for all three eras + the
bucket), the annotations by stripping the `[VDM-1 basin-1 2026-07-18]` prefix, and the
landing rows by `(kit_id)` / `(kit_id,url)`. Auto-committed per project discipline
(Matt-authorized VDM-1 charge).

---

## Commit note

Pathspec-only commit (matches ingest-1..7 precedent exactly): migration doc + ingest
script + errata-ledger. `corpus.db` and the backup are gitignored (`*.db` / `*-backup`)
and are NOT committed. The static JSONL inputs live under `.../vdm1/stage1/basin1/` and
are the basin-1 crawl artifacts (committed on the crawl side). **No push** (steward
pushes per charter + ADR-006).

---

## Anomalies / carry-forward notes (out of this dispatch's scope)

- **`corpus_bucket` singleton duplicates:** the table carries both short codes and long
  names for three Diablo lines — `d3`(48)/`diablo-3`(1), `d4`(45)/`diablo-4`(1),
  `di`(23)/`diablo-immortal`(1). This is a normalization concern (gamecode-normalize
  territory, cf. `corpus_gamecode_normalize_2026_07_16`), NOT in this dispatch's scope;
  flagged for a future roster-hygiene pass. `le`/`poe1`/`poe2` are clean single-token.
- **Stale `Era=...` substrings inside original mech_notes:** the 3 restamped kits' original
  harvest notes still contain their pre-restamp `Era=...` prose (e.g. grim-feast's
  "Era=0.2-dawn through 0.4"). These are preserved verbatim after the tagged clause per
  no-silent-transformation; the authoritative era is the `eras` column + the tagged clause.
  A future note-normalization pass could reconcile the prose, but silent in-prose edits are
  deliberately avoided here.
