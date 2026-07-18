# VDM-1 RUN STATE — verify + dossier + map (autonomous)

> **Charter:** `agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-charter.md` (v1 RATIFIED — Matt rulings R-1..R-9, R-10 dissolved). Launched 2026-07-18. Matt interface: R-8(b) — THE REVIEW BOOK at end; red-flag pings only. Push-as-you-go (R-9). Steward: gandalf.

**HARD FIRE:** PoE1's 94 kits complete crawl+verify+dossier before **July 24** (3.29 league churn).

## Stage ledger

| # | Stage | Owner | State |
|---|---|---|---|
| 0a | Schema landing zone (`kit_dossier` · `kit_citations` · `verify_ledger` · `kit_mapping` · `mint_ledger` · `mechanic_gap_docket` + conf-provenance tags + JSONL `core_skills` ingestion fix) | elrond | ✓ DONE (commit `2b73ee95`, pushed) — 6 tables live, all asserts held; fact_provenance backfill 2640 kb-legacy / 2140 named-source-unfetched (0 http in sources_used — corpus verified nowhere, per charter §2); core_skills 573/585 ingested, 0 orphans, 12 census-drift residue rows logged |
| 0b | Census reconciliation + PoE1 search-spec generation + stale mobile-flag inventory | legolas | ✓ DONE (commit `6ea07069`, pushed) — DB strict superset (0 JSONL-not-DB / 10 DB-only / 0 id-mismatch); the 94-vs-91 gap = 3 DB-only kits (blood-magic-kit, totem-hierophant, vaal-blade-vortex, all with source_urls); 94 search specs (82 wayback, 6 negatives, 34 thin-material); stale flags: 515 rows → ~397 STALE-LANDED (elrond bulk-reclass) / ~74 partial / ~16 STILL-OPEN (form-swap 10 → GX-02 gate; union/recipe 6 → docket candidate) |
| 0c | Crosswalk tables (element · ailment · supports→5-lane · items · capstone→T4 · geometry phrase-book) | gandalf | ✓ DONE — `design-inputs/2026-07-18-vdm1-crosswalks.md` |
| 1 | PoE1 tranche: crawl + verify + dossier (94 kits, 8 batches × ~12) | legolas | ⏳ IN FLIGHT — see batch table |
| 2 | PoE1 tranche: mapping authoring + grades | gandalf | ○ blocked on 1 |
| 3 | Calibration self-check (priors · kb-delta · cost · mint-rate) → re-plan ~490 | gandalf | ○ blocked on 2 |
| 4 | Remaining basins per charter §6 (post-cutoff → GD/LE → kb deep canon → LA harvest-grade → small → residue) + 107 probe backfill | legolas+elrond+gandalf | ○ blocked on 3 |
| 5 | 10% blind re-projection rider (judgment-grade axes per partition) | legolas | ○ blocked on 4 |
| 6 | THE REVIEW BOOK + devlog citation export (IP-clearance-gated) + tracker registration | gandalf | ○ blocked on 4/5 |

## Stage-1 batch tracker (PoE1: 94 kits, slices of `stage0/poe1-search-specs.jsonl`)

| Batch | Spec lines | State | Outcome |
|---|---|---|---|
| 01 | 1–12 | ⏳ fired 2026-07-18 | — |
| 02 | 13–24 | ⏳ fired 2026-07-18 | — |
| 03 | 25–36 | ○ | — |
| 04 | 37–48 | ○ | — |
| 05 | 49–60 | ○ | — |
| 06 | 61–72 | ○ | — |
| 07 | 73–84 | ○ | — |
| 08 | 85–94 | ○ | — |

Batch discipline: agents commit pathspec-only, do NOT push (steward pushes after artifact-level verification — parallel pushes would race). Outputs: `research/vdm1/stage1/poe1/batch-NN-{verify,citations,dossier}.jsonl` + `batch-NN-summary.md`. Elrond ingest fires every ~2-3 completed batches.

## Pre-registered priors (grade at stage 3)

identity ~.97 · core skills ~.90 · key items ~.85 · era ~.85 · negative-canon ~.95 · extraction overhead +25–40%/kit · kb-derived contradiction rate predicted HIGHER than source-derived (sleeper study — measure the delta). **~0% contradiction = failed run** (rubber-stamp detector).

## Red-flag ledger (Matt-ping events only)

_(empty at launch)_

## Basin checkpoints

_(rows appended per basin: date · basin · kits · verdict histogram · citations · dossier coverage · mapping grades · mints · dockets · commit)_

## Corpus-state anchors at launch (measured 2026-07-17/18)

585 rows / 565 census denominator / V10 97.5% expressible / probe facts 478×10 / source_urls 60 / kb-only sources 403/478 / mapping columns 0/585 / no-probe kits 107 (LA 53).
