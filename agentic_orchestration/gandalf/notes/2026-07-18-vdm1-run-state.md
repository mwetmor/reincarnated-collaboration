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
| 2 | PoE1 tranche: mapping authoring + grades | gandalf | ⏳ IN FLIGHT — batch-01 mapped + steward-audited (ACCEPTED w/ 2 corrections; rulings R-M1..R-M6 binding); batch-02 fired |
| 3 | Calibration self-check (priors · kb-delta · cost · mint-rate) → re-plan ~490 | gandalf | ○ blocked on 2 |
| 4 | Remaining basins per charter §6 (post-cutoff → GD/LE → kb deep canon → LA harvest-grade → small → residue) + 107 probe backfill | legolas+elrond+gandalf | ○ blocked on 3 |
| 5 | 10% blind re-projection rider (judgment-grade axes per partition) | legolas | ○ blocked on 4 |
| 6 | THE REVIEW BOOK + devlog citation export (IP-clearance-gated) + tracker registration | gandalf | ○ blocked on 4/5 |

## Stage-1 batch tracker (PoE1: 94 kits, slices of `stage0/poe1-search-specs.jsonl`)

| Batch | Spec lines | State | Outcome |
|---|---|---|---|
| 01 | 1–12 | ✓ DONE | 40 CONFIRMED / 0 CONTRA / 12 UNSUP (all filler negative_canon on negative=0 — dropped at ingest) / 0 SNF · dossier 71/72 · 14 author handles · anchors 100% |
| 02 | 13–24 | ✓ DONE | 34 C / **1 CONTRADICTED** / 17 U / 0 SNF · **ERRATA-1: crackling-lance era 3.7-3.13 → 3.12-3.13 (skill debuted 3.12 Heist)** · cleave death_class flagged inference-not-attested (honest UNSUP) · dossier 93% |
| 03 | 25–36 | ✓ DONE | 32 C / **1 CONTRADICTED** / 3 U / 0 SNF · **ERRATA-2 candidate: deaths-oath era floor 2.x → 1.x (item attested v1.0.2, Nov-2013 forum)** · dossier 65% (capstone_alterations universally source-silent) · 5 author handles · anchors 100% |
| 04 | 37–48 | ✓ DONE | 34 C / **2 CONTRADICTED** / 1 U / 0 SNF · **ERRATA-3: generals-cry era floor 3.7 → 3.11 · ERRATA-4: hexblast-mines era floor 3.7 → 3.12 (both skill-introduction violations)** · dossier 83% (capstone_alterations uniform abstain) · glacial-hammer negative_canon CONFIRMED · anchors 100% |
| 05 | 49–60 | ✓ DONE | 31 C / **3 CONTRADICTED** / 2 U / 0 SNF · **ERRATA-5/6/7 candidates: icicle-mines 3.7→3.8 · lightning-conduit 3.14→3.19 (five patches — worst yet) · pconc 3.14→3.16** · first identity UNSUPPORTED (minion-pact-bv, 3.28-recent folk name unattested) · kinetic-fusillade era_year=2013 bulk-fill artifact (actual 3.27/2024) → rekey at ingest-3 · dossier 56% (item_alterations sparse, skill-centric kits) · anchors 100% |
| 06 | 61–72 | ⏳ fired | — |
| 07 | 73–84 | ○ | — |
| 08 | 85–94 | ○ | — |

Batch discipline: agents commit pathspec-only, do NOT push (steward pushes after artifact-level verification — parallel pushes would race). Outputs: `research/vdm1/stage1/poe1/batch-NN-{verify,citations,dossier}.jsonl` + `batch-NN-summary.md`. Elrond ingest fires every ~2-3 completed batches. Briefs by reference: `stage1/poe1/BATCH-BRIEF-TEMPLATE.md` (batches 03+).

**Run notes (stage-0/1 operational):**
- Stale-flag reclass DONE (elrond `c806bcda`): 402 STALE-LANDED archived → `mobile_blocking_mechanics_archived` (LANDED-<wave> prefix), live flag → `expressible-now`; partition exact 402+79+18+16=515; residual live blockers 113; form-swap 10 + union/recipe 6 verifiably untouched.
- **Infra: corpus.db journal_mode WAL → DELETE (steward, data-neutral).** WAL + last-connection-cleanup deleted -shm/-wal, and readonly connections can't recreate them → SQLITE_CANTOPEN(14) for every crawler between elrond sessions. DELETE mode restores universal readonly access; elrond instructed to keep it.
- poewiki.net Anubis-403-blocked, fandom paywalled → domain order re-led with poedb.tw/poe-vault (template updated).
- Abstain-law refinement: 2 rows (b01 autobomber/author_credit, b02 blood-magic/variants) carried `{"note":...}` payloads on abstained=1 — DB CHECK rejects; elrond logs at ingest-1, re-insert with null payload at ingest-2; template hardened for 05+.
- Ingest-1 fired (batches 01-02 + ERRATA-1 + fact_provenance promotions to `verified-v1.1` for clean kits).
- Batch-03 flags for ingest-2: (a) ERRATA-2 candidate deaths-oath era floor (elrond review); (b) earthshatter alias "Foulborn Ghostwrithe zerker(3.28)" unfindable in any source — phantom-alias candidate; (c) `capstone_alterations` structurally source-silent from guide-tier fetches (universal abstention b03) → targeted poedb gem-level backfill pass queued as stage-4 candidate.
- Running tally after 48/94 kits: 140 CONFIRMED / 4 CONTRADICTED / 33 UNSUPPORTED / 0 SNF · 0 quarantined-domain hits · anchors 100% on C/C verdicts. ALL 4 contradictions are era-family (prior ~.85 named it weakest — tracking true; era contra rate ~8% vs ~15% predicted).
- **SYSTEMATIC FINDING (batch-04 red flag): the `3.7-3.13` era bucket is a contamination vector** — 3 of 4 era contradictions are kits stamped at that bucket's floor before the skill debuted (crackling-lance 3.12, generals-cry 3.11, hexblast-mines 3.12). Ingest-2 emits a bucket-audit register (all 585 kits using the bucket) for stage-3; batch-05+ briefs carry an explicit introduction-patch check addendum.
- Ingest-2 DONE (elrond `d5be1348`): verify 155 / citations 139 / dossier 288 · ERRATA-2/3/4 applied (guarded 1 row each) · REVIEW-1 earthshatter phantom alias logged unadjudicated · bucket-audit register 50 kits post-errata (3.7-3.13 is PoE-only vocab) · promotions → whole-DB verified-v1.1 = 400 · asserts all pass, journal DELETE held. Stage-4 candidate queued: targeted poedb pass for capstone_alterations (structurally guide-silent: b03 100% abstain, b04 uniform abstain) — pairs with the bucket audit as one poedb sweep.
- **Bucket contamination GENERALIZES (batch-05): 3.14-3.19 implicated too** (lightning-conduit 3.19-debut stamped 3.14; pconc 3.16-debut stamped 3.14). 6 of 7 run contradictions are bucket-floor-vs-introduction. Ingest-3 to extend the audit register to ALL wide-bucket floors + rekey kinetic-fusillade era_year.
- **Mapping batch-01 steward audit (DRIFT-CRITIC) DONE — ACCEPTED w/ corrections:** arc EXACT→CLOSE (engine chain decays 0.7×/hop vs Arc per-remaining-chain growth; mapper asserted false nativeness → audit-precedent rule) · bane Despair curse:sap→curse:amplify (crosswalk §2 law gap — Despair row added, binding) · enum sweep 12/12 clean · shock→sunder 4/4, engine-shock leaked 0× · docket 2 ladder-correct (aurabot scope-boundary, animate-weapon loot-as-ammo) · **first quantitative mint-candidate: per-kit chain-decay override >1.0 (forced by arc)** · post-audit histogram EXACT 0 / CLOSE 9 / APPROX 2 / GAPPED 1 (zero-EXACT is the honest shape) · rulings R-M1..R-M6 appended to template, binding 02+.
- Running tally after 60/94 kits: 171 CONFIRMED / 7 CONTRADICTED / 35 UNSUPPORTED / 0 SNF · 0 quarantined-domain hits · anchors 100% on C/C verdicts · all 7 contradictions era-family.

## Pre-registered priors (grade at stage 3)

identity ~.97 · core skills ~.90 · key items ~.85 · era ~.85 · negative-canon ~.95 · extraction overhead +25–40%/kit · kb-derived contradiction rate predicted HIGHER than source-derived (sleeper study — measure the delta). **~0% contradiction = failed run** (rubber-stamp detector).

## Red-flag ledger (Matt-ping events only)

_(empty at launch)_

## Basin checkpoints

_(rows appended per basin: date · basin · kits · verdict histogram · citations · dossier coverage · mapping grades · mints · dockets · commit)_

## Corpus-state anchors at launch (measured 2026-07-17/18)

585 rows / 565 census denominator / V10 97.5% expressible / probe facts 478×10 / source_urls 60 / kb-only sources 403/478 / mapping columns 0/585 / no-probe kits 107 (LA 53).
