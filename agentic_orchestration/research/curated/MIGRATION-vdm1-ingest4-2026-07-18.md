# MIGRATION — VDM-1 ingest wave 4 (PoE1 batches 07-08 + first kit_mapping wave)

**Date:** 2026-07-18
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1
**Script:** `agentic_orchestration/research/curated/scripts/corpus_vdm1_ingest4_2026_07_18.py`
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged; readonly crawlers + mapping agents run concurrently — NOT flipped to WAL)

Loads PoE1 crawl batches 07-08 (22 kits) into the landing-zone tables
(`verify_ledger`, `kit_citations`, `kit_dossier`), applies FOUR era errata
(ERRATA-10..13 — all b08-era) + one era BACKFILL (VBV, NULL→value), records the
Unattested-Register + floor-based bucket-audit register annotations, applies
fact-provenance promotions, and — for the FIRST time — ingests the stage-2
`kit_mapping` table (48 rows, mapping-batch-01..04). Follows the ingest-3 procedure
(`corpus_vdm1_ingest3_2026_07_18.py`) exactly, with the additions documented below.

---

## Backup

- **File:** `corpus.db.pre-vdm1-ingest4-2026-07-18-backup`
- **md5:** `c6cbe77e3e8f017ed593b40bfd97c965` (matched live DB at backup time)

A stale `corpus.db-shm` sidecar was present pre-ingest (no `-wal`). Left untouched
per the dispatch law (deleting -shm/-wal previously broke the concurrent readonly
crawlers). Harmless in DELETE mode.

---

## Inputs (committed, static)

Stage-1: `agentic_orchestration/research/vdm1/stage1/poe1/batch-{07,08}-{verify,citations,dossier}.jsonl`
Stage-2: `agentic_orchestration/research/vdm1/stage2/poe1/mapping-batch-0{1,2,3,4}.jsonl`

| Stream | B07 lines | B08 lines | Total |
|---|---|---|---|
| verify | 53 | 46 | 99 |
| citations | 38 | 34 | 72 |
| dossier | 72 | 60 | 132 |
| mapping (stage-2) | — | — | 48 (12+12+12+12) |

Both batches pre-verified by the steward. Verdict tallies (verify streams):
- **B07** (53 rows, 12 kits): identity 12 CONFIRMED; mechanics 12 CONFIRMED;
  era 19 CONFIRMED / 9 UNSUPPORTED / **0 CONTRADICTED**; negative_canon 1 CONFIRMED.
- **B08** (46 rows, 10 kits): identity 11 CONFIRMED / 1 UNSUPPORTED; mechanics 9
  CONFIRMED / 1 UNSUPPORTED; era 16 CONFIRMED / **4 CONTRADICTED** / 3 UNSUPPORTED;
  negative_canon 1 CONFIRMED.

**Negative kits:** `poe1-sweep` (b07) + `poe1-wild-strike` (b08) — both `negative=1`
in canon_corpus, both negative_canon **CONFIRMED** (substantive, source-quoted). **0
filler dropped this wave** (the filler rule drops negative_canon UNSUPPORTED on
`negative=0` kits only; neither applies).

**Defect-repair validation:** batch-07-dossier line 2
(`poe1-spectral-throw/skill_geometry`) had a premature close-brace repaired by the
steward via parse-and-merge (content unchanged; keys merged
`source_url/anchor_quote/abstained/conf`). The script's `load_jsonl` runs
`json.loads` per line and raises on any malformed row — this wave parsed **0
malformed lines** (all 303 stage-1 + 48 stage-2 lines parsed clean), independently
confirming the repair.

---

## FORMAT NOTES

- **batch-07/08 verify rows are GRANULAR** (same one-row-per-era-band split as
  batch-06): b07 = 53 rows / 12 kits, b08 = 46 rows / 10 kits. Rows are additive and
  independently attestable per era band. The errata-mark guard is UNAFFECTED: each of
  the four ERRATA-10..13 kits carries **exactly one** CONTRADICTED era row (verified
  pre-flight), regardless of how many CONFIRMED era-band rows accompany it. The
  RESTAMP/DROP adjudications (esp. ERRATA-11) are made legible by this split — the
  CONTRADICTED band and the paired CONFIRMED band are separate rows on the same kit.
- **NO boolean-drift this wave.** batch-07/08 emit **integer** 0/1 for both
  `abstained` (dossier) and `quarantined` (citations) — verified: 132 int abstained,
  72 int quarantined, 0 JSON booleans. The `coerce_bin` guard is retained for
  parity/safety and fired **0 bool-coercions** (contrast ingest-3's 36).

---

## Ingested row counts (defaults: run_tag='vdm1', extraction/mapping provenance defaults)

| Table | B07 | B08 | Ingested | Post-ingest total |
|---|---|---|---|---|
| `verify_ledger` | 53 | 46 | **99** | 246 + 99 = **345** ✓ |
| `kit_citations` | 38 | 34 | **72** | 197 + 72 = **269** ✓ |
| `kit_dossier` | 72 | 60 | **132** | 432 + 132 = **564** ✓ |
| `kit_mapping` | — | — | **48** | 0 + 48 = **48** ✓ |

Rejected-malformed rows (enum/FK/CHECK violations): **0** across all four streams.
Cross-wave UNIQUE-key collision check (pre-flight): **0** on
`kit_citations(kit_id,url)`, **0** on `kit_dossier(kit_id,family,source_url)`, **0**
`kit_mapping` PK collisions. No b07/b08 kit overlaps any prior-wave verify_ledger kit
(verified: 0 overlap).

---

## Abstained dossier rows — payload CHECK (no reconciliation needed)

This wave's dossier carries **29 abstained rows** (B07=25, B08=4), and **every one
arrived with `payload_json = NULL`** — 0 payload-carrying abstains, 0 stripped. The
schema CHECK `(abstained = 0 OR payload_json IS NULL)` held. Whole-DB after this
wave: **138 abstained rows** (109 prior + 29), 0 with non-NULL payload.

---

## ERRATA-10..13 — four anchored era corrections (all b08-era)

All four are CONTRADICTED verify rows carrying their anchor quote. Each `UPDATE` was
guarded to hit **exactly 1** `canon_corpus` row against the exact current DB value
(pre-flight assert on `old` value + post-`UPDATE` `rowcount==1` assert).
`verify_ledger.errata_applied=1` set on the single CONTRADICTED era row per kit
(verified: 1/1/1/1). Full adjudications + verbatim anchors in the errata ledger.

| Errata | kit_id | old → new | class / rationale (one-line) |
|---|---|---|---|
| ERRATA-10 | `poe1-venom-gyre` | `3.7-3.13;3.20+` → `3.8-3.13;3.20+` | debut-inside-bucket: skill debut 3.8.0 → floor 3.7→3.8 |
| ERRATA-11 | `poe1-viper-poison` | `3.0-3.6;3.7-3.13` → `3.7-3.13` | **RESTAMP** (ERRATA-8 class): combined-kit impossibility drops 3.0-3.6; attested 3.7-3.13 kept |
| ERRATA-12 | `poe1-ward-loop` | `3.14-3.19;3.20+` → `3.15-3.19;3.20+` | debut-inside-bucket: Ward mechanic debut 3.15 → floor 3.14→3.15 |
| ERRATA-13 | `poe1-winter-orb` | `3.0-3.6` → `3.5-3.6` | debut-inside-bucket: skill debut 3.5.0 → floor 3.0→3.5 (poe.ninja 9% at 3.5) |

### ERRATA-11 adjudication (drop-vs-restamp under the ERRATA-8 seismic-trap precedent)

The dispatch posed the choice explicitly: the ENTIRE `3.0-3.6` bucket is a
**combined-kit impossibility** — the stamped kit is the *dual-skill Poison Assassin*
(Viper Strike + Pestilent Strike), and co-skill Pestilent Strike debuts **3.8.0**, so
the combined kit as stamped cannot exist anywhere in 3.0-3.6. Viper-Strike-alone is a
*different claim* and is not what is stamped. The ERRATA-8 rule: **if no in-bucket
attestation of the combined kit, DROP the bucket; RESTAMP only if the b08 anchors
attest a specific later window.**

The b08 anchors **DO attest a specific later window**: a CONFIRMED positive `era` row
on **3.7-3.13**, anchored by the "[3.8] Pestilent Strike & Viper Strike Poison
Assassin | 6M Shaper DPS" thread (tylam6746, patch 3.8). Therefore the verdict is
**RESTAMP, not blanket DROP**: drop only the unattested 3.0-3.6 bucket; keep the
attested 3.7-3.13 → `3.7-3.13`. (The surviving band is retained as the whole wide
bucket — no sub-band floor-narrowing inside an attested wide bucket, consistent with
the wave-3 register semantics that treat a wide bucket as the attested unit.)

**Contrast with ERRATA-8 (seismic-trap, which DROPPED with no restamp):** seismic-trap
had its earliest attestation on a *different* floor (3.16, in the 3.14-3.19 bucket),
so dropping 3.7-3.13 needed no restamp — the 3.14-3.19 band already stood alone.
viper-poison's impossibility is at 3.0-3.6 and a *distinct adjacent* band (3.7-3.13)
is positively attested, so that attested band becomes the sole surviving stamp. Same
"band-unattested" root class; the DROP-only-vs-DROP-and-keep discriminator turns on
whether a distinct later band carries positive evidence.

- **not-corrected fields:** none beyond the single `eras` value per kit.
- **register effect:** all four errata kits are individually verified this wave, so
  none is a stage-3 floor-register member regardless of eras.
- **promotion exclusion:** all four carried a CONTRADICTED era → EXCLUDED from
  promotion (venom-gyre / viper-poison / winter-orb are zero-probe kits so the
  exclusion is moot; ward-loop likewise excluded).

---

## BACKFILL-1 — poe1-vaal-blade-vortex era fill (NULL → attested crawl value; NOT errata)

- **field:** `canon_corpus.eras`. **old → new:** `NULL` → `3.0-3.6;3.7-3.13`.
- VBV is a **DB-only census kit** that carried **no era stamp** (SQL `NULL`, not `''`
  — verified via `typeof(eras)='null'`). The b07 `era` verify row is **CONFIRMED**;
  its anchor establishes the window ("added 3.3.0 … [3.8 Video Guide] … confirms
  3.7-3.13"). 3.3.0 lands in the `3.0-3.6` bucket; the 3.8 guide confirms `3.7-3.13`.
- This is a **fill-from-verified-crawl**, NOT an errata (no prior value to
  contradict). **NO `errata_applied` flag** (reserved for CONTRADICTED-era
  corrections; VBV's era is CONFIRMED). Verified: VBV has 0 `errata_applied=1` rows.
- Guarded UPDATE `eras IS NULL` → value, `rowcount==1`. (The `WHERE eras=?` idiom
  cannot match NULL; the script uses `eras IS NULL` for the NULL-fill path.)
- VBV has 0 probe facts (zero-probe kit) so it promotes 0 rows; the era fill does not
  gate promotion.

---

## REGISTER — Unattested Register + floor-based bucket-audit register (EMPTIED to 0)

The floor-based bucket-audit register (a kit qualifies iff its era FLOOR equals a wide
bucket `3.0-3.6`/`3.7-3.13`/`3.14-3.19` AND it is not individually verified across
waves) **empties to 0 this wave**. Wave-3's register was **12 kits**; **all 12 are
crawled in batches 07-08** (spectres, split-arrow-bleed, sst, storm-brand,
tectonic-slam, toxic-rain, venom-gyre, viper-poison, ward-loop, winter-orb,
woc-ignite, wormblaster) and drop off the audit surface. Verified: 0 residual
floor-based register members post-wave-4. This is the natural terminal state of the
PoE1 wide-bucket tail being fully crawled.

Three annotations attach to now-verified rows as **stage-3 systematic sweep inputs**
(NOT data writes):

- **UNATTESTED REGISTER — `poe1-totem-hierophant`:** era **UNSUPPORTED** (b07); eras
  unrecoverable from search. DB `eras` stays **NULL** (no attested window to fill —
  contrast BACKFILL-1). The verify row ("Era stamps absent from DB — cannot verify")
  is the record. Enters the **Unattested Register** per charter stream-1.
- **INTRO-PATCH ANNOT — `poe1-tectonic-slam` (intro 3.2.0):** `3.0-3.6` floor
  CONFIRMED (genuine back-half presence). NO errata basis. Intro patch **3.2.0**
  (inside the bucket) attached to its register row for the stage-3 debut-vs-floor
  sweep.
- **INTRO-PATCH ANNOT — `poe1-toxic-rain` (intro 3.4.0):** `3.0-3.6` floor CONFIRMED.
  NO errata basis. Intro patch **3.4.0** (inside the bucket) attached. (Its `3.7-3.13`
  mid-band was graded UNSUPPORTED — a partition-analysis input, not an errata; the
  multi-band stamp is retained unchanged.)

---

## kit_mapping — FIRST INGEST WAVE (48 rows; provenance authored-vdm1)

The stage-2 `kit_mapping` table is populated for the first time (was 0 rows). All 48
rows from `mapping-batch-01..04.jsonl` are steward-audited **ACCEPTED** — the
post-audit file state is truth (per dispatch: b01 arc=CLOSE + bane curse:amplify; b04
forbidden-rite + heavy-strike-stun = GAPPED). Each row loads `mapping_json` (nested
dict serialized), `grade`, `deviation_notes`, `terminal_state`; `mapping_provenance`
defaults to `authored-vdm1`.

**Load-time asserts (all pass — dispatch file truths):**

| Assert | Result |
|---|---|
| grade histogram EXACT / CLOSE / APPROX / GAPPED | **2 / 32 / 10 / 4** ✓ |
| terminal histogram MAPPED / MAPPED_DOCKET | 44 / 4 ✓ |
| terminal MAPPED_DOCKET rows == exactly the GAPPED rows (R-M7 1:1 law) | ✓ (identical sets) |
| GAPPED == MAPPED_DOCKET kits | `aurabot, detonate-dead, forbidden-rite, heavy-strike-stun` |
| 48 distinct kit_ids (0 in-file dupes) | 48/48 ✓ |
| all 48 kit_ids present in canon_corpus | 48/48 ✓ (0 missing) |
| grade↔terminal coherence (post-load) | EXACT/CLOSE/APPROX all MAPPED; GAPPED all MAPPED_DOCKET ✓ |

**NOT ingested** (await steward ratification at stage-3): `mint-candidates-batch-*`,
`docket-candidates-batch-*`, `mapping-batch-*-summary.md`. Only the four
`mapping-batch-0{1..4}.jsonl` files were read.

---

## fact_provenance promotions

Rule (unchanged): kits with `mechanics=CONFIRMED` AND **zero** CONTRADICTED verdicts
anywhere → flip `canon_probe_facts.fact_provenance` →`verified-v1.1`.

- **Promote set:** **17 kits** (12 b07 kits + 5 promotable b08 kits: wander,
  warchief, whispering-ice, wild-strike, woc-ignite). Excluded: the four ERRATA-10..13
  kits (CONTRADICTED era) + wormblaster (mechanics UNSUPPORTED, see below).
- **Rows promoted:** **130** (13 kits × 10 facts each).
- **Zero-promotion kits (in promote set but 0 rows flipped):** `poe1-sweep`,
  `poe1-totem-hierophant`, `poe1-vaal-blade-vortex`, `poe1-wild-strike` — **all four
  have ZERO probe facts** (verified: 0 `canon_probe_facts` rows each; they are among
  the charter's 107 zero-probe-fact kits). 0 promoted is correct, not a miss. (Prior
  waves saw a different zero-promotion cause — reaper/glacial-hammer had non-legacy
  provenance; these have no facts at all.)

**Whole-DB provenance after this wave:** `verified-v1.1` = **720** (590 prior + 130);
`kb-legacy` 2130→2030 (−100); `named-source-unfetched` 2060→2030 (−30). −100 + −30 =
−130 = exactly the 130 promoted. ✓

### wormblaster — FAILS the gate, stays legacy (stage-4 residue flag)

`poe1-wormblaster` (batch-08) is **NOT promoted**. Its **mechanics verdict is
UNSUPPORTED**: pobarchives 403'd, and the 3.3 forum thread that WAS located shows a
**"[3.3] Wormblaster the 4.5th — Flameblast / Herald of Ash Slayer"** variant — a
different build entirely from the claimed **CoC + Barrage + Pathfinder**. It fails the
`mechanics=CONFIRMED` gate directly (its identity + both era rows are CONFIRMED, so 0
CONTRADICTED — but 0 CONTRADICTED is not sufficient; the gate requires mechanics
CONFIRMED). Asserted NOT in `promote_kits`; verified **0** `verified-v1.1` facts
post-ingest. **Flagged for stage-4 residue** (its probe facts, if any are later
authored, stay legacy until the claimed mechanics are attested from a fetched source).

---

## Asserts (all pass)

| # | Assert | Result |
|---|---|---|
| 1 | `verify_ledger` count == 246 + 99 | 345 ✓ |
| 1 | `kit_citations` count == 197 + 72 | 269 ✓ |
| 1 | `kit_dossier` count == 432 + 132 | 564 ✓ |
| 1 | `kit_mapping` count == 0 + 48 | 48 ✓ |
| 1 | ingest rejects (enum/FK/CHECK), all four streams | 0 ✓ |
| 1 | cross-wave UNIQUE/PK collisions (citations / dossier / mapping) | 0 / 0 / 0 ✓ |
| 1 | verify-kit overlap with prior waves | 0 ✓ |
| 2 | `canon_corpus` row count unchanged | 585 ✓ |
| 3 | ERRATA-10..13 eras set to exact new values | 4/4 ✓ |
| 3 | BACKFILL-1 VBV eras == `3.0-3.6;3.7-3.13` | ✓ |
| 4 | `errata_applied=1` total (8 prior + 4 this wave), all era/CONTRADICTED | 12 rows, 0 non-conforming ✓ |
| 4 | each of the 4 errata kits: exactly 1 `errata_applied` row | 1/1/1/1 ✓ |
| 4 | VBV backfill does NOT set `errata_applied` | 0 ✓ |
| 5 | mapping grade histogram EXACT2/CLOSE32/APPROX10/GAPPED4 | ✓ |
| 5 | mapping MAPPED_DOCKET == GAPPED set (R-M7 1:1) | ✓ |
| 5 | mapping 48 distinct kit_ids, all in canon_corpus | ✓ |
| 6 | `PRAGMA journal_mode` == delete | delete ✓ |
| 6 | `PRAGMA integrity_check` | ok ✓ |
| 6 | `PRAGMA foreign_key_check` | empty ✓ |
| 7 | landing-zone orphans (verify_ledger / kit_mapping) | 0 / 0 ✓ |
| 7 | no N/A-filler leaked into ledger | 0 rows `N/A%` ✓ |
| 7 | abstained dossier rows with non-NULL payload | 0 of 138 ✓ |
| 8 | `verified-v1.1` total == 720; provenance arithmetic balances (−130) | 720 ✓ |
| 8 | promote set == 17 kits; 130 rows promoted | ✓ |
| 9 | wormblaster NOT promoted (mechanics UNSUPPORTED) | 0 `verified-v1.1` ✓ |
| 9 | 4 zero-promotion kits have 0 probe facts | 0/0/0/0 ✓ |

---

## Reproducibility

Inputs are committed and static. Re-running the script against
`corpus.db.pre-vdm1-ingest4-2026-07-18-backup` reproduces this state exactly.
Dry-run mode (no `--apply`) validates and reports counts without writing. The write
path is a single `BEGIN IMMEDIATE` … `COMMIT` (short txn; concurrent readonly crawlers
+ mapping agents unaffected), opened through an index.lock-retry wrapper (wait 30s,
retry 3×; 0 retries fired this wave). journal_mode kept DELETE throughout.

---

## ADR-004 + reversibility

No engine-telemetry change; star-lord-side MIGRATION.md unaffected (all writes are
corpus-curation in the landing zone + `canon_corpus.eras` + `canon_probe_facts`
provenance + `kit_mapping`, all elrond's seam). Reversible:
`corpus.db.pre-vdm1-ingest4-2026-07-18-backup` restores the exact PRE state. Errata
are reversible via the `errata_applied` flag + this ledger; the VBV backfill is
reversible (single `UPDATE … SET eras=NULL`). Auto-committed per project discipline
(Matt-authorized VDM-1 charge). **NO push — gandalf pushes per basin checkpoint (R-9).**

---

## Commit note

Pathspec-only commit (matches ingest-1/2/3 precedent): migration doc + errata ledger +
ingest script. `corpus.db` is gitignored/untracked and is NOT committed (verified:
`git check-ignore` hits it). No push (per charter R-9 — gandalf pushes; + ADR-006).
