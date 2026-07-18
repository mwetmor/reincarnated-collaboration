# VDM-1 Stage-3 calibration protocol (V-0 gate) — PRE-REGISTERED

> **✓ EXECUTED 2026-07-18 — verdict GO w/ amendments.** Results + D-rulings: `2026-07-18-vdm1-stage3-gate-result.md`. This doc remains the pre-registration record (methods were fixed before final data landed).

> Drafted 2026-07-18 while mapping 05-06 + ingest-4 in flight, BEFORE final PoE1 data lands — measurement methods fixed now so the self-check cannot grade its own homework. Charter §6; run-state ledger is the data source of record. Executor: gandalf (steward). Output: GO / AMEND / NO-GO for the ~490-kit scale-out + brief amendments.

## A. Measurements (each = predicted vs actual + one-line verdict)

1. **Prior-vs-actual per claim family, KIT-level.** Priors: identity ~.97 · core skills ~.90 · key items ~.85 · era ~.85 · negative-canon ~.95. Method: collapse verify rows to kit×family verdicts (worst-verdict-wins: CONTRA > UNSUP > CONFIRMED) — this normalizes b06+ granular-row drift. Actual = CONFIRMED / (CONFIRMED+CONTRADICTED) per family (UNSUPPORTED excluded — silence is not error). Era interim: 12 contra-kits/94 ≈ 12.8% vs ~15% predicted.
2. **Era contamination — register, not row verdicts.** The floor-based register (12 kits post-ingest-3 + any ingest-4 delta) + intro-patch annotations is the instrument; row-verdict rates are verdict-policy-sensitive (b07 graded floor-vs-intro CONFIRMED-with-note where b02-b05 said CONTRADICTED). Emit: systematic-sweep spec (one poedb pass resolving all register kits' intro patches; pairs with capstone_alterations backfill).
3. **kb-vs-source contradiction delta (sleeper study).** Partition kits by fact_provenance (kb-legacy 2640 vs named-source-unfetched 2140 at launch); compare contradiction rates. Predicted: kb-derived HIGHER.
4. **Extraction overhead.** Predicted +25-40%/kit. Actual: task usage per batch (b07 ≈92k tokens/12 kits, b08 ≈90k/10 kits; earlier batches comparable) + ~2-3 fetches/kit vs spec. Verdict on cost-per-kit for 490-kit projection.
5. **Mint-rate.** Interim 2 mints/48 mapped ≈ 4.2%; explosion = red-flag halt per charter. Also docket-rate (8/48 ≈ 17%) — is GAPPED≈8% (4/48) a stable shape?
6. **Dossier coverage by family.** Known structural holes: capstone_alterations guide-silent (b03 100% abstain, b04 uniform); item_alterations sparse on skill-centric kits (b05 56%). Decision: targeted poedb sweep scope (stage-4 candidate) vs accept-abstention.
7. **Mapping grade shape.** Interim 48: EXACT 2 / CLOSE 32 / APPROX 10 / GAPPED 4. Zero-ish EXACT is the HONEST shape (engine-owns-archetype only). Watch: does 05-08 hold it, or does grade optimism creep at scale?
8. **~0% contradiction = failed run detector:** PASSED already (12 ≫ 0).

## B. Decisions the gate must emit

- **D-1 GO/AMEND/NO-GO** for remaining basins (charter §6 order: post-cutoff → GD/LE → kb deep canon → LA harvest-grade → small → residue) + 107 probe backfill.
- **D-2 Brief amendments (crawl):** (a) uniform verdict law — era floor predating skill/co-skill introduction = CONTRADICTED even with genuine back-half presence (kills the b07 policy split); (b) intro-patch check stays mandatory; (c) self-report histograms advisory only — file truth is the count (b06/b07/b08 all drifted).
- **D-3 Brief amendments (mapping):** R-M1..R-M7 carry forward; add any 05-08 audit rulings as R-M8+.
- **D-4 Candidate ratification batch:** 8 docket + 2 mint (+ 05-08 accruals); consolidate entity-as-consumable-resource-pool family (animate-weapon, bladefall, dark-pact; detonate-dead adjacent) into ONE mechanic_gap_docket row with evidence_kits list; TIMED-WHILE-ACTIVE-APPROX accrual count vs R-M5 threshold.
- **D-5 Register sweep + capstone backfill:** ratify the paired poedb pass as one dispatch or defer to stage-4.
- **D-6 Re-plan arithmetic:** batches×size×parallelism for ~490 at measured cost/kit; wayback dependence per basin (post-cutoff basin should need less; GD/LE sources stabler than PoE pre-3.29).

## C. Standing review-book accumulators (do NOT resolve at stage-3 — Matt-tier)

hp_cost_scale 0.30 ceiling (≥3 kits clamped) · reservation_percent 0.75 cap (≥2 kits) · mint/docket ratification record · GX-02 form-swap gate (10 flags) · union/recipe docket candidate (6) · REVIEW-1 earthshatter phantom alias · REVIEW-2 poets-pen-vd roster_atlas class (cross-seam per ADR-004) · IP-clearance gate on devlog citation export · wormblaster residue (promotion-gate fail).

## ERRATA index (quick ref)

1 crackling-lance era · 2 deaths-oath era floor 2.x→1.x · 3 generals-cry 3.7→3.11 · 4 hexblast-mines 3.7→3.12 · 5 icicle-mines 3.7→3.8 · 6 lightning-conduit 3.14→3.19 · 7 pconc 3.14→3.16 · 8 seismic-trap bucket DROP (patch-buff-seeded class) · 9 kinetic-fusillade era_year 2013→2024 · 10 venom-gyre 3.7→3.8 · 11 viper-poison bucket (drop-vs-restamp, elrond adjudicating) · 12 ward-loop 3.14→3.15 · 13 winter-orb 3.0→3.5.
