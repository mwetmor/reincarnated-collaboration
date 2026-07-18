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
| 01 | 1–12 | ✓ DONE | 40 CONFIRMED / 0 CONTRA / 12 UNSUP (all filler negative_canon on negative=0 — dropped at ingest) / 0 SNF · dossier 71/72 · 14 author handles · anchors 100% |
| 02 | 13–24 | ✓ DONE | 34 C / **1 CONTRADICTED** / 17 U / 0 SNF · **ERRATA-1: crackling-lance era 3.7-3.13 → 3.12-3.13 (skill debuted 3.12 Heist)** · cleave death_class flagged inference-not-attested (honest UNSUP) · dossier 93% |
| 03 | 25–36 | ⏳ fired | — |
| 04 | 37–48 | ⏳ fired | — |
| 05 | 49–60 | ○ | — |
| 06 | 61–72 | ○ | — |
| 07 | 73–84 | ○ | — |
| 08 | 85–94 | ○ | — |

Batch discipline: agents commit pathspec-only, do NOT push (steward pushes after artifact-level verification — parallel pushes would race). Outputs: `research/vdm1/stage1/poe1/batch-NN-{verify,citations,dossier}.jsonl` + `batch-NN-summary.md`. Elrond ingest fires every ~2-3 completed batches. Briefs by reference: `stage1/poe1/BATCH-BRIEF-TEMPLATE.md` (batches 03+).

**Run notes (stage-0/1 operational):**
- Stale-flag reclass DONE (elrond `c806bcda`): 402 STALE-LANDED archived → `mobile_blocking_mechanics_archived` (LANDED-<wave> prefix), live flag → `expressible-now`; partition exact 402+79+18+16=515; residual live blockers 113; form-swap 10 + union/recipe 6 verifiably untouched.
- **Infra: corpus.db journal_mode WAL → DELETE (steward, data-neutral).** WAL + last-connection-cleanup deleted -shm/-wal, and readonly connections can't recreate them → SQLITE_CANTOPEN(14) for every crawler between elrond sessions. DELETE mode restores universal readonly access; elrond instructed to keep it.
- poewiki.net Anubis-403-blocked, fandom paywalled → domain order re-led with poedb.tw/poe-vault (template updated).
- Abstain-law refinement: 2 rows (b01 autobomber/author_credit, b02 blood-magic/variants) carried `{"note":...}` payloads on abstained=1 — DB CHECK rejects; elrond logs at ingest-1, re-insert with null payload at ingest-2; template hardened for 05+.
- Ingest-1 fired (batches 01-02 + ERRATA-1 + fact_provenance promotions to `verified-v1.1` for clean kits).
- Running tally after 24/94 kits: 74 CONFIRMED / 1 CONTRADICTED / 29 UNSUPPORTED / 0 SNF · 0 quarantined-domain hits · anchors 100% on C/C verdicts.

## Pre-registered priors (grade at stage 3)

identity ~.97 · core skills ~.90 · key items ~.85 · era ~.85 · negative-canon ~.95 · extraction overhead +25–40%/kit · kb-derived contradiction rate predicted HIGHER than source-derived (sleeper study — measure the delta). **~0% contradiction = failed run** (rubber-stamp detector).

## Red-flag ledger (Matt-ping events only)

_(empty at launch)_

## Basin checkpoints

_(rows appended per basin: date · basin · kits · verdict histogram · citations · dossier coverage · mapping grades · mints · dockets · commit)_

## Corpus-state anchors at launch (measured 2026-07-17/18)

585 rows / 565 census denominator / V10 97.5% expressible / probe facts 478×10 / source_urls 60 / kb-only sources 403/478 / mapping columns 0/585 / no-probe kits 107 (LA 53).
