# MIGRATION — VDM-1 ingest wave 3 (PoE1 batches 05-06)

**Date:** 2026-07-18
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1
**Script:** `agentic_orchestration/research/curated/scripts/corpus_vdm1_ingest3_2026_07_18.py`
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged; readonly crawlers + mapping agents run concurrently — NOT flipped to WAL)

Loads PoE1 crawl batches 05-06 (24 kits) into the landing-zone tables
(`verify_ledger`, `kit_citations`, `kit_dossier`), applies FIVE errata
(ERRATA-5/6/7/8 era corrections + ERRATA-9 era_year rekey), logs one unadjudicated
cross-seam class review (REVIEW-2), extends the stage-3 bucket-audit register to ALL
wide-bucket floors, and applies fact-provenance promotions. Follows the ingest-2
procedure (`corpus_vdm1_ingest2_2026_07_18.py`) exactly, with three additions
documented below (boolean-drift normalization, ERRATA-9 non-eras column, index.lock
retry).

---

## Backup

- **File:** `corpus.db.pre-vdm1-ingest3-2026-07-18-backup`
- **md5:** `125ad00096e5352753db325eee9fb93d` (matched live DB at backup time)

A stale `corpus.db-shm` sidecar was present pre-ingest (no `-wal`). Left untouched
per the dispatch law (deleting -shm/-wal previously broke the concurrent readonly
crawlers). Harmless in DELETE mode.

---

## Inputs (committed, static)

`agentic_orchestration/research/vdm1/stage1/poe1/batch-{05,06}-{verify,citations,dossier}.jsonl`

| Stream | B05 lines | B06 lines | Total lines |
|---|---|---|---|
| verify | 36 | 55 | 91 |
| citations | 22 | 36 | 58 |
| dossier | 72 | 72 | 144 |

Both batches pre-verified by the steward: anchors 100% on C/C rows (verified: 0
CONFIRMED/CONTRADICTED verify rows with a blank/NULL anchor); abstain rows carry null
payload; batch-05 has **0** negative_canon rows (all negative=false); batch-06 has
**exactly 1** (poe1-reaper, CONFIRMED, negative=1 — legitimate). No filler to drop.

Verdict tally (verify streams):
- **B05** (36 rows, 12 kits): 11 identity CONFIRMED / 1 identity UNSUPPORTED;
  12 mechanics CONFIRMED; 8 era CONFIRMED / 3 era CONTRADICTED / 1 era UNSUPPORTED.
- **B06** (55 rows, 12 kits, GRANULAR — see below): 14 identity CONFIRMED;
  12 mechanics CONFIRMED; 26 era CONFIRMED / 1 era CONTRADICTED / 1 era UNSUPPORTED;
  1 negative_canon CONFIRMED.

---

## FORMAT DRIFT — batch-06 GRANULAR verify rows (ingested as-is; per-kit normalization deferred)

batch-06 emitted **granular** verify rows where earlier batches emitted folded ones:

- **identity split** folk-name / aliases → **14 identity rows** for 12 kits (2 kits —
  `pizza-sticks`, `poets-pen-vd` — carry a separate row for the primary folk-name and
  for the alias set; the other 10 carry 1).
- **era split** one-row-per-era-band → **28 era rows** for 12 kits (e.g.,
  `righteous-fire` = 5 era rows for its 5 bands `1.x;3.0-3.6;3.7-3.13;3.14-3.19;3.20+`;
  `poison-bv` and `spark` = 4 each; several = 2; a few = 1).
- **55 verify rows total** for 12 kits vs the ~36 of earlier batches (12+12+12).

**Ingested AS-IS** per dispatch — the rows are additive and more checkable (each era
band is now independently attestable). The granularity is **recorded here so
partition analysis / stage-3 can normalize per-kit later** (e.g., collapse per-band
era rows to a single per-kit era verdict, or keep the band-grain if useful). The
errata-mark guard is UNAFFECTED: each errata kit still carries **exactly one**
CONTRADICTED era row (verified pre-flight), regardless of how many CONFIRMED era-band
rows accompany it. seismic-trap (ERRATA-8) is the clearest case — it has 2 era rows
(1 CONTRADICTED on 3.7-3.13 + 1 CONFIRMED on 3.14-3.19); only the CONTRADICTED row is
flagged.

Per-kit verify-row-count table for batch-06 (for the partition normalizer):

| kit_id | identity | mechanics | era | neg | total |
|---|---|---|---|---|---|
| poe1-pizza-sticks | 2 | 1 | 1 | 0 | 4 |
| poe1-poets-pen-vd | 2 | 1 | 1 | 0 | 4 |
| poe1-poison-bv | 1 | 1 | 4 | 0 | 6 |
| poe1-reaper | 1 | 1 | 1 | 1 | 4 |
| poe1-righteous-fire | 1 | 1 | 5 | 0 | 7 |
| poe1-scourge-arrow | 1 | 1 | 2 | 0 | 4 |
| poe1-seismic-trap | 1 | 1 | 2 | 0 | 4 |
| poe1-siege-ballista | 1 | 1 | 2 | 0 | 4 |
| poe1-skeleton-mages | 1 | 1 | 2 | 0 | 4 |
| poe1-soulrend | 1 | 1 | 2 | 0 | 4 |
| poe1-spark | 1 | 1 | 4 | 0 | 6 |
| poe1-spectral-helix | 1 | 1 | 2 | 0 | 4 |
| **total** | **14** | **12** | **28** | **1** | **55** |

---

## Script additions vs ingest-2 (all logged; no silent transformation)

1. **BOOLEAN-DRIFT NORMALIZATION.** batch-06 emits a JSON boolean for `quarantined`
   (`false`) where batch-05 emits an integer (`0`). Python maps `False == 0` and
   `False in {0,1}` is `True`, so the membership check passes — but to avoid silent
   type drift into an INTEGER column, the script **coerces bool→int explicitly** at
   stage time (`coerce_bin`). **36 coercions** logged this wave, all
   `citations.quarantined: false → 0` (every batch-06 citation row). `int(False)` is
   the value SQLite would store anyway; the coercion changes nothing about the datum,
   only makes the type explicit. (batch-06 `dossier.abstained` was already emitted as
   integer 0/1 — 0 coercions there.) The same guard rejects any non-binary value as
   malformed. `author_handle: "unknown"` (batch-06) is a valid string, ingested as-is.
2. **ERRATA-9 era_year rekey** — a NON-eras `canon_corpus` column. Does NOT set
   `verify_ledger.errata_applied` (that flag is reserved for the CONTRADICTED-era-row
   convention; kinetic-fusillade's era verdict is CONFIRMED). See ERRATA section.
3. **index.lock RETRY on the write connection** (`connect_with_retry`: wait 30s,
   retry 3×) per dispatch LAW — readonly crawlers + mapping agents run concurrently.
   The write handle probes the lock with a no-op `BEGIN IMMEDIATE; COMMIT;` before the
   real txn; on `database is locked` it waits and retries. This wave acquired the lock
   on the first attempt (0 retries fired).

---

## Ingested row counts (defaults: run_tag='vdm1', extraction_provenance='fetched-vdm1')

| Table | B05 | B06 | Total ingested | JSONL lines − dropped-filler | Post-ingest table total |
|---|---|---|---|---|---|
| `verify_ledger` | 36 | 55 | **91** | 91 − 0 = 91 ✓ | 155 + 91 = **246** ✓ |
| `kit_citations` | 22 | 36 | **58** | 58 − 0 = 58 ✓ | 139 + 58 = **197** ✓ |
| `kit_dossier` | 72 | 72 | **144** | 144 − 0 = 144 ✓ | 288 + 144 = **432** ✓ |

Rejected-malformed rows (enum/FK violations): **0**. Every row validated clean.
Cross-wave UNIQUE-key collision check (batch-05/06 keys vs already-ingested rows):
**0 collisions** on `kit_citations(kit_id,url)` and `kit_dossier(kit_id,family,source_url)`
— verified pre-flight. No batch-05/06 kit overlaps any prior-wave verify_ledger kit.

---

## Dropped-filler (N/A-filler negative_canon rows)

Rule (unchanged from ingest-1/2): `negative_canon` UNSUPPORTED rows on
`canon_corpus.negative=0` kits are N/A-filler → DROP. Discriminator is the DB
`negative` flag (authoritative).

| Batch | negative_canon rows | Dropped-filler | Retained |
|---|---|---|---|
| 05 | 0 | 0 | — |
| 06 | 1 | 0 | `poe1-reaper` (CONFIRMED, negative=1) — substantive, source-quoted |
| **Total** | **1** | **0** | 1 |

`poe1-reaper` negative_canon is **CONFIRMED** on the run's one negative=1 kit this
wave: Summon Reaper fell out of meta due to insufficient damage scaling. Anchor:
"Build guide update is discontinued because I don't feel comfortable to recommend
this build anymore… the power of this build is no longer enough…". Ingests normally.

Post-ingest check: `verify_ledger` contains **0** rows with `claim_text LIKE 'N/A%'`.

---

## Abstained dossier rows — payload CHECK (no reconciliation needed this wave)

The schema enforces `CHECK (abstained = 0 OR payload_json IS NULL)`. This wave's
dossier streams carry **63 abstained rows** (B05=36, B06=27), and **every one already
arrived with `payload_json = NULL`** — 0 payload-carrying abstains. Nothing to strip
(contrast ingest-1, which stripped 2). The strip-and-preserve guard from ingest-1 is
retained in the script for parity/safety but fired 0 times.

Post-ingest (whole DB): **109 abstained rows** total (46 from waves 1-2 + 63 this
wave), 0 of them with non-NULL payload. CHECK held.

---

## ERRATA-5/6/7/8 — four anchored era corrections

All four are CONTRADICTED verify rows carrying their anchor quote. Each `UPDATE` was
guarded to hit **exactly 1** `canon_corpus` row against the exact current DB value
(pre-flight assert on `old` value + post-`UPDATE` `rowcount==1` assert).
`verify_ledger.errata_applied=1` set on the single CONTRADICTED era row per kit
(verified: 1/1/1/1). Full adjudications + verbatim anchors in the errata ledger.

| Errata | kit_id | field | old → new | batch | class / rationale (one-line) |
|---|---|---|---|---|---|
| ERRATA-5 | `poe1-icicle-mines` | `eras` | `3.7-3.13` → `3.8-3.13` | 05 | debut-inside-bucket: skill introduced 3.8.0 → floor 3.7→3.8 |
| ERRATA-6 | `poe1-lightning-conduit` | `eras` | `3.14-3.19;3.20+` → `3.19;3.20+` | 05 | debut-inside-bucket (top): introduced 3.19.0 LoK → bucket collapses to single patch 3.19 |
| ERRATA-7 | `poe1-pconc` | `eras` | `3.14-3.19;3.20+` → `3.16-3.19;3.20+` | 05 | debut-inside-bucket: introduced 3.16.0 Scourge → floor 3.14→3.16 |
| ERRATA-8 | `poe1-seismic-trap` | `eras` | `3.7-3.13;3.14-3.19` → `3.14-3.19` | 06 | **DISTINCT CLASS** — patch-buff-seeded stamp, no adoption evidence: DROP unattested bucket |

**ERRATA-8 is a distinct root-cause class** from the debut-floor corrections. Seismic
Trap **existed since 3.3.0** (predates the whole `3.7-3.13` bucket), so a naive
debut-floor rule would wrongly KEEP the bucket (skill present). But *skill presence ≠
meta build presence*: the crawl found **no attestation** of a Seismic Trap meta build
in 3.7-3.13; earliest confirmed meta is **3.16** (3.16/3.18 forum guides). A 3.13-era
patch-buff most plausibly **seeded the era stamp** without any adoption evidence. The
correction DROPS the entire unattested `3.7-3.13` bucket (rather than narrowing a
floor), leaving only the attested `3.14-3.19` window. batch-06's granular era rows
made this legible: one CONTRADICTED row (3.7-3.13) + one CONFIRMED positive row
(3.14-3.19) on the same kit. **Stage-3 methodology note:** for any multi-band PoE1
stamp where the skill's debut PREDATES a stamped band, require positive meta evidence
for THAT band — do not treat skill-existence as band-attestation.

- **not-corrected fields:** none beyond the single `eras` bucket per kit. All four
  kits' identity + mechanics verdicts are CONFIRMED and untouched.
- **register effect:** all four errata kits are individually verified this wave, so
  none is a stage-3 register member regardless of eras (the register excludes
  individually-verified kits — see below). ERRATA-5 keeps a `3.8-3.13` token but the
  kit is verified; ERRATA-8 re-floors to `3.14-3.19` (also verified).
- **promotion exclusion:** all four carried a CONTRADICTED era → EXCLUDED from this
  wave's fact_provenance promotion (their 40 probe facts stay legacy — verified 0
  `verified-v1.1` each).

---

## ERRATA-9 — poe1-kinetic-fusillade era_year rekey (2013 → 2024; NON-eras column)

- **field:** `canon_corpus.era_year` (a distinct introduction-year column, NOT `eras`).
- **old → new:** `2013` → `2024`. Guarded UPDATE, rowcount==1 (asserted).
- **verdict:** the `era` verify row is **CONFIRMED** (stamped `3.20+` is correct;
  Kinetic Fusillade added in version **3.27.0**, in the 3.20+ band). `era_year=2013`
  is a **bulk-fill artifact** — every batch-05/06 kit carries the identical 2013
  placeholder. batch-05 citations anchor the true year: guide titles `[3.27]` (PoE
  forum) and `(3.28)` (maxroll.gg); PoE 3.27/3.28 shipped in **2024**.
- **errata_applied flag:** **NOT set.** The flag is reserved for CONTRADICTED-era-row
  corrections; kinetic-fusillade's era is CONFIRMED, so flagging it would falsely
  imply the era stamp was wrong. This ledger + migration doc are the sole audit trail
  (no-silent-transformation). Verified: kinetic-fusillade has 0 `errata_applied=1`
  rows post-ingest.
- **promotion:** kinetic-fusillade **IS PROMOTED** (10 facts) — era CONFIRMED, no
  CONTRADICTED anywhere; the non-eras era_year rekey does not gate promotion.

### era_year-artifact (stage-3 candidate)

The identical **2013 bulk-fill placeholder** persists on the other 23 batch-05/06 kits
(and on prior-wave kits) — verified: all six adjudication kits showed `era_year=2013`.
Only kinetic-fusillade was rekeyed this wave (the sole dispatch red flag). A
**systematic `era_year` backfill from the verified `eras` band + citation dates** is a
clean stage-3 candidate: the `eras` floor band already implies an era window, and the
per-kit citation `[X.Y]` title tags give a defensible introduction year. Recommend
stage-3 backfill `era_year` for all VDM-1-verified kits from their attested band
rather than leaving the 2013 placeholder.

---

## REVIEW-2 — poe1-poets-pen-vd class field (CROSS-SEAM; NO in-scope column to correct)

**Adjudication outcome: logged as REVIEW, NOT applied as errata.** The dispatch red
flag ("DB class field says Elementalist/Necromancer; batch-06 shows Berserker (3.1)
then Inquisitor (3.2+)") is **evidence-CONFIRMED** but **has no writable target in
`corpus.db`**:

- There is **no `class`/ascendancy column** anywhere in `canon_corpus` or
  `canon_probe_facts`. Searched all tables — the class value lives in
  **`roster_atlas.class_v4r2`** (mirrored in `roster_lineage_enrichment`), which is
  OUTSIDE elrond's landing-zone write scope.
- **`poe1-poets-pen-vd` has NO row in `roster_atlas`** (verified: 0 rows in both
  roster_atlas and roster_lineage_enrichment for this kit_id). So even the upstream
  store lacks the value to correct.

The class evidence IS captured and anchored in the landing zone (ingested this wave):
the batch-06 `variants` dossier row payload is `["Berserker/Marauder (3.1 original)",
"Inquisitor Templar (3.2+ after Berserker nerf)", "Occultist", "Scion Ascendant
(3.10)"]` with verbatim anchor "as of Patch 3.2, this build is no longer supported.
Berserker class is no longer viable choice… leading to the Templar[/Inquisitor]"; the
identity CONFIRMED row cites the odealo title "Poet's Pen Volatile Dead
**Berserker/Marauder** Patch 3.1 Build". So the primary sources attest
**Berserker (3.1) → Inquisitor Templar (3.2+)**, NOT Elementalist/Necromancer.

**Cross-seam routing (ADR-004):** correcting the authoritative class value requires the
`roster_atlas` owner. elrond authors the request (this REVIEW row + errata-ledger
REVIEW-2); the roster-side change is applied by the owning agent, routed via
knight-rider. **No corpus.db field is silently changed** — poets-pen-vd still PROMOTES
normally on its probe-fact substrate (identity UNSUPPORTED does not apply here; its
identity rows are CONFIRMED). Recommended correction: `Inquisitor` (3.2+ canonical
peak) with Berserker (3.1 original) lineage noted, wherever authoritatively stored.

---

## BUCKET-AUDIT REGISTER (stage-3 audit surface) — EXTENDED to ALL wide floors

Wave-2's register covered the **3.7-3.13** floor only (via selector
`eras LIKE '%3.7-3.13%'`; 50 kits post-errata). Per the wave-3 dispatch, the register
is **extended to ALL wide-bucket floors** — `3.0-3.6`, `3.7-3.13`, `3.14-3.19` — with
the precise selector: **a kit qualifies iff its era FLOOR (leftmost band) equals a
wide bucket AND it has NOT been individually verified/errata'd** across waves 1-3.

**Selector semantics (floor-based, per dispatch wording):** "era floor equals a bucket
floor." A debut-vs-floor scrutiny only makes sense where the *floor itself* is a wide
bucket (the debut patch is ambiguous within it). Kits whose floor is a narrow band
(`1.x`, `2.x`, `3.20+`) already have a precise floor and merely *pass through* wide
buckets mid-life — they are NOT register candidates. State reflects post-wave-3 errata
(the four ERRATA-5..8 floor changes applied in-memory).

**Register size (post-wave-3, floor-based): 12 kits.** By floor bucket:
**9 at `3.0-3.6`, 2 at `3.7-3.13`, 1 at `3.14-3.19`.** All 12 are PoE1 (verified: 0
non-poe1 hits — the wide-bucket vocabulary is PoE-patch-specific).

### Transition from wave-2 (legibility)

- Wave-2's `3.7-3.13` register was **50 kits**. Of those, **38 are now individually
  verified** across waves 1-3 (crawled in batches 01-06) and **drop off** the audit
  surface. The remaining **12 wave-2 register kits are still unverified**:
  `spectres, split-arrow-bleed, srs, storm-brand, tornado-shot, toxic-rain, venom-gyre,
  viper-poison, whispering-ice, wild-strike, woc-ignite, wormblaster`.
- The **floor-based** wave-3 register (12) and the wave-2-style **LIKE-anywhere**
  count (19 unverified kits with any wide bucket present) differ by 7 — those 7 have a
  *narrow* floor (e.g., `srs` = `1.x;2.x;3.0-3.6;3.7-3.13;3.20+`, floor `1.x`) and
  merely traverse wide buckets. Reported here for continuity; the **authoritative
  register is the floor-based 12** per the dispatch selector. Stage-3 may widen to the
  LIKE-anywhere 19 if it wants mid-life-band scrutiny too.
- **33 additional wide-floor kits** are EXCLUDED because individually verified in
  waves 1-3 (they had a wide floor but have been crawled).

### Full register (post-wave-3, floor-based; stage-3 input)

| # | kit_id | eras (post-wave-3) | floor bucket |
|---|---|---|---|
| 1 | poe1-spectres | 3.0-3.6;3.7-3.13;3.14-3.19 | 3.0-3.6 |
| 2 | poe1-split-arrow-bleed | 3.0-3.6;3.7-3.13 | 3.0-3.6 |
| 3 | poe1-sst | 3.0-3.6;3.20+ | 3.0-3.6 |
| 4 | poe1-storm-brand | 3.0-3.6;3.7-3.13 | 3.0-3.6 |
| 5 | poe1-tectonic-slam | 3.0-3.6 | 3.0-3.6 |
| 6 | poe1-toxic-rain | 3.0-3.6;3.7-3.13;3.14-3.19;3.20+ | 3.0-3.6 |
| 7 | poe1-venom-gyre | 3.7-3.13;3.20+ | 3.7-3.13 |
| 8 | poe1-viper-poison | 3.0-3.6;3.7-3.13 | 3.0-3.6 |
| 9 | poe1-ward-loop | 3.14-3.19;3.20+ | 3.14-3.19 |
| 10 | poe1-winter-orb | 3.0-3.6 | 3.0-3.6 |
| 11 | poe1-woc-ignite | 3.7-3.13;3.14-3.19 | 3.7-3.13 |
| 12 | poe1-wormblaster | 3.0-3.6;3.7-3.13 | 3.0-3.6 |

Stage-3 should treat these 12 as live candidates for debut-vs-floor scrutiny (and
apply the ERRATA-8 "skill present but band unattested" test to their multi-band
stamps). Note `poe1-woc-ignite` appears in BOTH the wave-2 register (as `3.7-3.13`
floor) and here — it was never crawled, so it correctly persists.

---

## fact_provenance promotions

Rule (unchanged): kits with `mechanics=CONFIRMED` AND **zero** CONTRADICTED verdicts
anywhere on the kit → flip `canon_probe_facts.fact_provenance` from
`named-source-unfetched`/`kb-legacy` → `verified-v1.1`.

- **Promote set:** 20 kits (all 24 batch kits except the four era-errata kits
  `poe1-icicle-mines`, `poe1-lightning-conduit`, `poe1-pconc`, `poe1-seismic-trap`).
- **Rows promoted:** **190** (19 kits × 10 facts each).
- **Zero-promotion kit (in promote set but 0 rows flipped):** `poe1-reaper` — its 10
  probe facts were already in a non-promotable provenance at write time (0 rows in
  `('named-source-unfetched','kb-legacy')`), so 0 promoted is correct, not a miss.
  (Same pattern as `glacial-hammer` in wave-2 — the wave's negative_canon kit.)
- **Excluded (CONTRADICTED era):** the four errata kits' 40 probe facts stay legacy
  (verified 0 `verified-v1.1` each).

### PROMOTION RULING — poe1-minion-pact-bv (identity UNSUPPORTED does NOT block)

**RULING: identity-UNSUPPORTED does NOT block promotion. minion-pact-bv PROMOTES (10
rows).** Rationale:

- The promotion gate is `mechanics=CONFIRMED AND zero CONTRADICTED anywhere`.
  minion-pact-bv has **mechanics=CONFIRMED** (Minion Pact gem sacrifice mechanic
  quoted verbatim), **era=CONFIRMED** (3.20+), and **zero CONTRADICTED** verdicts. It
  qualifies under the unchanged rule.
- The identity=UNSUPPORTED is **honest silence on the folk-name** — the anchor is NULL
  because the community nickname "Minion Pact Blade Vortex" simply wasn't located in
  the fetched sources for a **3.28-recent** (near-cutoff) kit. It is NOT a
  contradiction of any fact.
- `verified-v1.1` certifies the **probe-fact substrate** (delivery/footprint/control/
  … — the engine-consumed mechanical facts), NOT the folk-name. Blocking promotion on
  identity-silence would conflate "we couldn't attest the nickname" with "the facts
  are wrong," penalizing honest silence — contrary to charter (no-fabrication /
  honest-silence discipline). The mechanics ARE source-confirmed.
- **Therefore promote.** (Verified: minion-pact-bv now has 10 `verified-v1.1` facts.)
- **Scope note:** this ruling is specific to identity-UNSUPPORTED (honest silence on
  the nickname). It does NOT extend to a CONTRADICTED identity (which would be a real
  conflict and would exclude), nor to mechanics-UNSUPPORTED (which would fail the
  `mechanics=CONFIRMED` gate directly).

**Note:** `poe1-kinetic-fusillade` and `poe1-poets-pen-vd` both PROMOTE normally
(kinetic-fusillade: era CONFIRMED, only era_year rekeyed — ERRATA-9; poets-pen-vd:
identity+mechanics+era CONFIRMED, class review is cross-seam and does not gate). Both
verified 10 `verified-v1.1` facts.

Whole-DB provenance after this wave: `verified-v1.1` = **590** (400 from waves 1-2 +
190 this wave); `kb-legacy` 2290→2130 (−160); `named-source-unfetched` 2090→2060
(−30). The −160 + −30 = −190 exactly equals the 190 promoted. ✓

---

## Asserts (all pass)

| # | Assert | Result |
|---|---|---|
| 1 | `verify_ledger` count == 155 + 91 | 246 == 246 ✓ |
| 1 | `kit_citations` count == 139 + 58 | 197 == 197 ✓ |
| 1 | `kit_dossier` count == 288 + 144 | 432 == 432 ✓ |
| 1 | ingest rejects (enum/FK) | 0 ✓ |
| 1 | cross-wave UNIQUE-key collisions (citations / dossier) | 0 / 0 ✓ |
| 2 | `canon_corpus` row count unchanged | 585 == 585 ✓ |
| 3 | ERRATA-5..8 eras set to exact new values | 4/4 ✓ |
| 3 | ERRATA-9 `era_year` == 2024 (kinetic-fusillade) | 2024 ✓ |
| 4 | `errata_applied=1` total (4 prior + 4 this wave), all era/CONTRADICTED | 8 rows, 0 non-conforming ✓ |
| 4 | each of the 4 errata kits: exactly 1 `errata_applied` row | 1/1/1/1 ✓ |
| 4 | kinetic-fusillade `errata_applied` rows (era_year rekey does NOT flag) | 0 ✓ |
| 5 | `PRAGMA journal_mode` == delete | delete ✓ |
| 5 | `PRAGMA integrity_check` | ok ✓ |
| 5 | `PRAGMA foreign_key_check` | empty (clean) ✓ |
| 6 | landing-zone orphans (FK to canon_corpus), all 3 tables | 0 / 0 / 0 ✓ |
| 7 | no N/A-filler leaked into ledger | 0 rows `N/A%` ✓ |
| 7 | abstained dossier rows with non-NULL payload | 0 of 109 ✓ |
| 8 | `verified-v1.1` total == 590; provenance arithmetic balances (−190) | 590 ✓ |
| 9 | reaper negative_canon CONFIRMED row landed | 1 row ✓ |
| 9 | 4 errata kits' probe facts unchanged (0 `verified-v1.1` each) | 0/0/0/0 ✓ |
| 10 | minion-pact-bv promoted (ruling) | 10 `verified-v1.1` ✓ |
| 10 | kinetic-fusillade promoted | 10 `verified-v1.1` ✓ |

---

## Reproducibility

Inputs are committed and static. Re-running the script against
`corpus.db.pre-vdm1-ingest3-2026-07-18-backup` reproduces this state exactly.
Dry-run mode (no `--apply`) validates and reports counts without writing. The write
path is a single `BEGIN IMMEDIATE` … `COMMIT` (short txn; concurrent readonly crawlers
+ mapping agents unaffected), opened through an index.lock-retry wrapper (wait 30s,
retry 3×). journal_mode kept DELETE throughout.

---

## Commit note

Pathspec-only commit (matches ingest-1/2 precedent, commits `72561cc9` / earlier):
migration doc + errata ledger + ingest script. `corpus.db` is gitignored/untracked and
is NOT committed (verified: `git check-ignore` hits it). No push (per dispatch +
ADR-006).
