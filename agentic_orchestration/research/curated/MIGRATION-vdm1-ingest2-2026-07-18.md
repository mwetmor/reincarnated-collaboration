# MIGRATION — VDM-1 ingest wave 2 (PoE1 batches 03-04)

**Date:** 2026-07-18
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1
**Script:** `agentic_orchestration/research/curated/scripts/corpus_vdm1_ingest2_2026_07_18.py`
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged; readonly crawlers run concurrently — NOT flipped to WAL)

Loads PoE1 crawl batches 03-04 (24 kits) into the landing-zone tables
(`verify_ledger`, `kit_citations`, `kit_dossier`), applies three anchored errata
(ERRATA-2/3/4), logs one unadjudicated phantom-alias review (REVIEW-1), emits the
stage-3 bucket-audit register, and applies fact-provenance promotions. Follows the
ingest-1 procedure (`corpus_vdm1_ingest1_2026_07_18.py`) exactly.

---

## Backup

- **File:** `corpus.db.pre-vdm1-ingest2-2026-07-18-backup`
- **md5:** `f9444177ecc10ebd2f71a1559cf532b7` (matched live DB at backup time)

Note: a stale `corpus.db-shm` sidecar was present pre-ingest (no `-wal`). It was
**left untouched** per the dispatch law (deleting -shm/-wal previously broke the
concurrent readonly crawlers). Harmless in DELETE mode.

---

## Inputs (committed, static)

`agentic_orchestration/research/vdm1/stage1/poe1/batch-{03,04}-{verify,citations,dossier}.jsonl`

| Stream | B03 lines | B04 lines | Total lines |
|---|---|---|---|
| verify | 36 | 37 | 73 |
| citations | 41 | 32 | 73 |
| dossier | 72 | 72 | 144 |

Both batches pre-verified by the steward (gandalf): anchors 100% on C/C rows;
abstain rows carry null payload; batch-04 has exactly one negative_canon row
(poe1-glacial-hammer, negative=1). No filler to drop this wave.

Verdict tally (verify streams): B03 = 32 CONFIRMED / 1 CONTRADICTED / 3 UNSUPPORTED
(12 identity + 12 mechanics + 12 era, 0 negative_canon). B04 = 34 CONFIRMED /
2 CONTRADICTED / 1 UNSUPPORTED (12 identity + 12 mechanics + 12 era + 1 negative_canon).

---

## Ingested row counts (defaults: run_tag='vdm1', extraction_provenance='fetched-vdm1')

| Table | B03 | B04 | Total ingested | JSONL lines − dropped-filler | Post-ingest table total |
|---|---|---|---|---|---|
| `verify_ledger` | 36 | 37 | **73** | 73 − 0 = 73 ✓ | 82 + 73 = **155** ✓ |
| `kit_citations` | 41 | 32 | **73** | 73 − 0 = 73 ✓ | 66 + 73 = **139** ✓ |
| `kit_dossier` | 72 | 72 | **144** | 144 − 0 = 144 ✓ | 144 + 144 = **288** ✓ |

Rejected-malformed rows (enum/FK violations): **0**. Every row validated clean.

---

## Dropped-filler (N/A-filler negative_canon rows)

Rule (unchanged from ingest-1): `negative_canon` UNSUPPORTED rows on
`canon_corpus.negative=0` kits are N/A-filler → DROP. Discriminator is the DB
`negative` flag (authoritative).

| Batch | negative_canon rows | Dropped-filler | Retained |
|---|---|---|---|
| 03 | 0 | 0 | — |
| 04 | 1 | 0 | `poe1-glacial-hammer` (CONFIRMED, negative=1) — substantive, source-quoted |
| **Total** | **1** | **0** | 1 |

`poe1-glacial-hammer` negative_canon is **CONFIRMED** on the run's one negative=1
kit this wave: the skill is a POE-original melee prototype (patch 0.8.6) that fell
out of meta after 3.0-3.6. Anchor: "Melee strike skill in modern POE [listed as a
con] … GGG has been on a nerfing spree…I had to look for other alternatives."
Ingests normally (boss-emission-ready per D-02).

Post-ingest check: `verify_ledger` contains **0** rows with `claim_text LIKE 'N/A%'`.

---

## Abstained dossier rows — payload CHECK (no reconciliation needed this wave)

The schema enforces `CHECK (abstained = 0 OR payload_json IS NULL)`. This wave's
dossier streams carry **39 abstained rows** (B03=25, B04=14), and **every one
already arrived with `payload_json = NULL`** — 0 payload-carrying abstains. Nothing
to strip (contrast ingest-1, which stripped 2). The strip-and-preserve guard from
ingest-1 is retained in the script for parity/safety but fired 0 times.

Post-ingest (whole DB): 46 abstained rows total (7 from ingest-1 + 39 this wave),
0 of them with non-NULL payload. CHECK held.

---

## ERRATA-2/3/4 — three anchored era corrections

All three are CONTRADICTED verify rows carrying their anchor quote. Each `UPDATE`
was guarded to hit **exactly 1** `canon_corpus` row against the exact current DB
value (pre-flight assert on `old` value + post-`UPDATE` `rowcount==1` assert).
`verify_ledger.errata_applied=1` set on the single CONTRADICTED era row per kit.
Full adjudications + verbatim anchors in the errata ledger (ERRATA-2/3/4).

| Errata | kit_id | field | old → new | batch | rationale (one-line) |
|---|---|---|---|---|---|
| ERRATA-2 | `poe1-deaths-oath` | `eras` | `2.x;3.0-3.6;3.7-3.13` → `1.x;3.0-3.6;3.7-3.13` | 03 | item attested v1.0.2 (1.x band), Nov-26-2013 forum thread → floor extends DOWN 2.x→1.x |
| ERRATA-3 | `poe1-generals-cry` | `eras` | `3.7-3.13;3.20+` → `3.11-3.13;3.20+` | 04 | skill debuted patch 3.11.0 inside the 3.7-3.13 bucket → floor narrows 3.7→3.11 |
| ERRATA-4 | `poe1-hexblast-mines` | `eras` | `3.7-3.13;3.20+` → `3.12-3.13;3.20+` | 04 | skill debuted 3.12.0 (Heist, GGG patch notes) → floor narrows 3.7→3.12 |

- **UPDATE rowcount:** 1 each (asserted).
- **not-corrected fields:** none beyond the single `eras` bucket per kit.
- **register effect:** ERRATA-2 leaves the `3.7-3.13` bucket token intact
  (deaths-oath STAYS in the register). ERRATA-3/4 narrow their kits OUT of the
  literal `3.7-3.13` token (generals-cry + hexblast-mines LEAVE the register:
  52 → 50 for the corrected state).

All three kits carried a CONTRADICTED era and are therefore **EXCLUDED** from this
wave's fact_provenance promotion (their 30 probe facts stay legacy — verified below).

---

## REVIEW-1 — poe1-earthshatter phantom alias (UNADJUDICATED — NO data change)

Alias `Foulborn Ghostwrithe zerker(3.28)` (carried in earthshatter's `identity`
claim) could not be located in ANY fetched source by batch-03. Per the no-silent-
edits law it was **NOT deleted** — SOURCE-NOT-FOUND is honest silence, not a
contradiction. Logged as **REVIEW-1** in the errata ledger (unadjudicated; needs
steward/Matt eyes). earthshatter's identity verdict is CONFIRMED overall (build
identity attested; this specific alias is not). The alias row is present and intact
in `verify_ledger` (asserted). Recommended: targeted re-crawl to attest/refute, or
a steward ruling if judged a harvest artifact.

---

## BUCKET-AUDIT REGISTER (stage-3 audit surface)

Enumeration of every `canon_corpus` kit (scope: all 585) whose era stamp uses or
floors at the **3.7-3.13** bucket, captured as a **pre-errata snapshot** (the audit
surface as it stood at wave-2 start). Selector: `eras LIKE '%3.7-3.13%'`.

**Register size (pre-errata): 52 kits.** All 52 are PoE1 — the `3.7-3.13` band is
PoE-patch vocabulary; no other game/source in the corpus uses it, which is why the
"all 585" scope resolves to a PoE1-only set (verified: the `LIKE` returns 0 non-poe1
rows). **No eras were changed beyond the three anchored errata above.**

**Post-errata register size: 50** — ERRATA-3 (generals-cry) and ERRATA-4
(hexblast-mines) narrow their floors out of the literal `3.7-3.13` token. The other
50 (including deaths-oath, whose floor changed 2.x→1.x but retains the `3.7-3.13`
bucket, and earthshatter, unchanged) remain. The stage-3 audit should treat these
50 as live candidates for the same debut-vs-floor scrutiny the three errata received.

Full pre-errata register (kit_id | eras):

| # | kit_id | eras (pre-errata) |
|---|---|---|
| 1 | poe1-aegis-max-block | 3.7-3.13;3.14-3.19;3.20+ |
| 2 | poe1-animate-weapon | 1.x;3.7-3.13;3.20+ |
| 3 | poe1-arc | 1.x;2.x;3.0-3.6;3.7-3.13 |
| 4 | poe1-archmage | 3.7-3.13;3.20+ |
| 5 | poe1-armageddon-brand | 3.0-3.6;3.7-3.13 |
| 6 | poe1-aurabot | 2.x;3.0-3.6;3.7-3.13;3.14-3.19;3.20+ |
| 7 | poe1-aurastacker | 3.7-3.13 |
| 8 | poe1-autobomber | 3.0-3.6;3.7-3.13 |
| 9 | poe1-ball-lightning | 3.0-3.6;3.7-3.13 |
| 10 | poe1-bane | 3.0-3.6;3.7-3.13 |
| 11 | poe1-baron-zombies | 3.0-3.6;3.7-3.13 |
| 12 | poe1-bladefall-bladeblast | 3.7-3.13 |
| 13 | poe1-caustic-arrow | 1.x;2.x;3.7-3.13 |
| 14 | poe1-charged-dash | 3.0-3.6;3.7-3.13 |
| 15 | poe1-cleave | 1.x;2.x;3.0-3.6;3.7-3.13 |
| 16 | poe1-coc-ice-nova | 3.0-3.6;3.7-3.13;3.20+ |
| 17 | poe1-cold-dot-occ | 3.0-3.6;3.7-3.13;3.14-3.19 |
| 18 | poe1-cyclone | 2.x;3.0-3.6;3.7-3.13;3.20+ |
| 19 | poe1-deaths-oath | 2.x;3.0-3.6;3.7-3.13 *(→ ERRATA-2: floor now 1.x; STAYS in register)* |
| 20 | poe1-detonate-dead | 1.x;3.7-3.13;3.14-3.19 |
| 21 | poe1-divine-ire | 3.0-3.6;3.7-3.13 |
| 22 | poe1-earthshatter | 3.7-3.13;3.20+ *(REVIEW-1 phantom alias; era CONFIRMED, unchanged; skill debuted 3.11 — soft candidate, NOT corrected per dispatch)* |
| 23 | poe1-edc | 2.x;3.0-3.6;3.7-3.13;3.14-3.19 |
| 24 | poe1-fire-trap | 1.x;2.x;3.7-3.13 |
| 25 | poe1-flicker | 1.x;2.x;3.0-3.6;3.7-3.13;3.20+ |
| 26 | poe1-frost-blades | 2.x;3.7-3.13;3.20+ |
| 27 | poe1-generals-cry | 3.7-3.13;3.20+ *(→ ERRATA-3: floor now 3.11; LEAVES register)* |
| 28 | poe1-glacial-cascade-mines | 3.0-3.6;3.7-3.13 |
| 29 | poe1-golementalist | 2.x;3.0-3.6;3.7-3.13 |
| 30 | poe1-hexblast-mines | 3.7-3.13;3.20+ *(→ ERRATA-4: floor now 3.12; LEAVES register)* |
| 31 | poe1-hoag | 3.0-3.6;3.7-3.13 |
| 32 | poe1-ice-shot | 3.7-3.13;3.20+ |
| 33 | poe1-icicle-mines | 3.7-3.13 |
| 34 | poe1-lacerate-glad | 3.0-3.6;3.7-3.13;3.20+ |
| 35 | poe1-poison-bv | 2.x;3.0-3.6;3.7-3.13;3.14-3.19 |
| 36 | poe1-righteous-fire | 1.x;3.0-3.6;3.7-3.13;3.14-3.19;3.20+ |
| 37 | poe1-scourge-arrow | 3.0-3.6;3.7-3.13 |
| 38 | poe1-seismic-trap | 3.7-3.13;3.14-3.19 |
| 39 | poe1-skeleton-mages | 3.7-3.13;3.14-3.19 |
| 40 | poe1-soulrend | 3.0-3.6;3.7-3.13 |
| 41 | poe1-spectres | 3.0-3.6;3.7-3.13;3.14-3.19 |
| 42 | poe1-split-arrow-bleed | 3.0-3.6;3.7-3.13 |
| 43 | poe1-srs | 1.x;2.x;3.0-3.6;3.7-3.13;3.20+ |
| 44 | poe1-storm-brand | 3.0-3.6;3.7-3.13 |
| 45 | poe1-tornado-shot | 1.x;3.0-3.6;3.7-3.13;3.20+ |
| 46 | poe1-toxic-rain | 3.0-3.6;3.7-3.13;3.14-3.19;3.20+ |
| 47 | poe1-venom-gyre | 3.7-3.13;3.20+ |
| 48 | poe1-viper-poison | 3.0-3.6;3.7-3.13 |
| 49 | poe1-whispering-ice | 2.x;3.0-3.6;3.7-3.13;3.20+ |
| 50 | poe1-wild-strike | 2.x;3.0-3.6;3.7-3.13 |
| 51 | poe1-woc-ignite | 3.7-3.13;3.14-3.19 |
| 52 | poe1-wormblaster | 3.0-3.6;3.7-3.13 |

---

## fact_provenance promotions

Rule (unchanged): kits with `mechanics=CONFIRMED` AND **zero** CONTRADICTED verdicts
anywhere on the kit → flip `canon_probe_facts.fact_provenance` from
`named-source-unfetched`/`kb-legacy` → `verified-v1.1`.

- **Promote set:** 21 kits (all 24 batch kits except the three errata kits
  `poe1-deaths-oath`, `poe1-generals-cry`, `poe1-hexblast-mines`).
- **Rows promoted:** **200** (20 kits × 10 facts each).
- **Zero-promotion kit (in promote set but 0 rows flipped):** `poe1-glacial-hammer`
  — its 10 probe facts were already in a non-promotable provenance at write time
  (0 rows in `('named-source-unfetched','kb-legacy')`), so 0 promoted is correct,
  not a miss. (Note: a pre-write `-readonly` snapshot briefly showed 10 kb-legacy
  facts for this kit; the authoritative post-txn state under a fresh connection is
  the truth and the promotion `UPDATE` matched it exactly. Whole-DB provenance
  arithmetic balances — see asserts.)
- **Excluded (CONTRADICTED era):** the three errata kits' 30 probe facts stay legacy:
  deaths-oath = 10 `kb-legacy`, generals-cry = 10 `named-source-unfetched`,
  hexblast-mines = 10 `kb-legacy` (verified unchanged).

Whole-DB provenance after this wave: `verified-v1.1` = **400** (200 from ingest-1 +
200 this wave); `kb-legacy` 2460→2290 (−170); `named-source-unfetched` 2120→2090
(−30). The −170 + −30 = −200 exactly equals the 200 promoted. ✓

---

## Asserts (all pass)

| # | Assert | Result |
|---|---|---|
| 1 | `verify_ledger` count == 82 + 73 | 155 == 155 ✓ |
| 1 | `kit_citations` count == 66 + 73 | 139 == 139 ✓ |
| 1 | `kit_dossier` count == 144 + 144 | 288 == 288 ✓ |
| 1 | ingest rejects (enum/FK) | 0 ✓ |
| 2 | `canon_corpus` row count unchanged | 585 == 585 ✓ |
| 2 | canon_corpus untouched except the 3 errata `eras` | only `eras` on 3 rows changed ✓ |
| 3 | `errata_applied=1` rows total (1 ingest-1 + 3 this wave), all era/CONTRADICTED | 4 rows ✓ |
| 3 | each errata `UPDATE` rowcount == 1 | 1/1/1 ✓ |
| 4 | `PRAGMA journal_mode` == delete | delete ✓ |
| 4 | `PRAGMA integrity_check` | ok ✓ |
| 4 | `PRAGMA foreign_key_check` | empty (clean) ✓ |
| 5 | landing-zone orphans (FK to canon_corpus), all 3 tables | 0 / 0 / 0 ✓ |
| 6 | `verified-v1.1` total == 400; provenance arithmetic balances (−200) | 400 ✓ |
| 6 | errata kits' 30 probe facts unchanged (none verified-v1.1) | 30 legacy ✓ |
| 7 | no N/A-filler leaked into ledger | 0 rows `N/A%` ✓ |
| 8 | abstained dossier rows with non-NULL payload | 0 of 46 ✓ |
| 9 | glacial-hammer negative_canon CONFIRMED row landed | 1 row ✓ |
| 10 | earthshatter phantom alias preserved (not deleted) | present ✓ |

---

## Reproducibility

Inputs are committed and static. Re-running the script against
`corpus.db.pre-vdm1-ingest2-2026-07-18-backup` reproduces this state exactly.
Dry-run mode (no `--apply`) validates and reports counts without writing. The write
path is a single `BEGIN IMMEDIATE` … `COMMIT` (short txn; concurrent readonly
crawlers unaffected). journal_mode kept DELETE throughout.

---

## Commit note

Pathspec-only commit (matches ingest-1 precedent, commit `72561cc9`): migration doc
+ errata ledger + ingest script. `corpus.db` is gitignored/untracked and is NOT
committed (verified: `git check-ignore` hits it; ingest-1's commit touched 3 files,
not the DB). No push (per dispatch + ADR-006).
