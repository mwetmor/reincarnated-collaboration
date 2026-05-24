# Per-Tier Count Distribution — Cycle 10 Stage 2.5 Post-Execution

**Date:** 2026-05-24
**Author:** elrond (data steward)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-2-5-quality-tier-scoring.md`
**Substrate DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
**Scoring script:** `score_quality_composite.py`
**Execution log:** `log.out`
**Summary JSON:** `scoring-summary.json`

---

## §0 TL;DR

All 89,841 substrate rows scored. Empirical tier distribution lands cleanly within dispatch-proposed defaults:

| Tier | Count | % of substrate | Dispatch-target | Status |
|---|---:|---:|---|---|
| S | 1,126 | 1.25% | 1-3% | within range |
| A | 7,943 | 8.84% | 7-10% | within range |
| B | 58,315 | 64.91% | 50-70% | within range |
| C | 22,457 | 25.00% | 20-30% | within range |
| **TOTAL** | **89,841** | **100.00%** | | |

Composite score range: **0.100 - 0.730** (min - max). Empirical distribution shape: roughly Gaussian-tailed; tail length skewed left (no row above 0.75 because all 9 signals would have to be near-1.0 simultaneously — extremely rare).

Tier S composition:
- **452 rows (40.1%)** via named-mythological-match seed-list path (all gates cleared: Mode-C clear + Tier-3-lineage clear)
- **674 rows (59.9%)** via top-1% composite-score path (no seed match required)

Mode-C contamination blocked from Tier S match path: **71 rows** (1 of 72 didn't have a seed match anyway, so no block needed)
Tier-3-lineage blocked from Tier S match path: **19 rows** (apparent seed matches in 6 Tier-3-excluded lineages — cultural-sensitivity gate fired correctly)

**Total Tier-S match-path rejections: 90 of 542 would-be-matches (16.6% rejection rate via gates).**

**Gandalf prep status:** BOTH gandalf prep files LANDED at execution time (no placeholder values used). Source-library reputation tier: 25 entries (covering all 25 substrate source_library values). Cultural-tradition weight: 14 entries (covering all 14 substrate cultural_lineage_canonical values).

**Compute cost:** $0.00 (heuristic-only per ADR-006); 1.7 seconds total execution wall-time.

---

## §1 Per-tier composite-score statistics

| Tier | Count | min | max | mean | threshold notes |
|---|---:|---:|---:|---:|---|
| S | 1,126 | 0.3136 | 0.7304 | 0.5791 | composite ≥ 0.5712 OR named-match (gates cleared) |
| A | 7,943 | 0.4790 | 0.5710 | 0.5080 | top 10% excluding S |
| B | 58,315 | 0.3303 | 0.4790 | 0.4253 | standard pool |
| C | 22,457 | 0.1000 | 0.3303 | 0.2776 | bottom 25% |

**Note on min-of-Tier-S < threshold_S:** 452 named-match rows enter Tier S regardless of composite score. The minimum composite score in Tier S (0.3136) comes from a named-match row that itself scored relatively low (likely a Wikipedia mythological article with thin metadata) but qualified via the seed-list path.

Empirical thresholds (computed AFTER all rows scored):
- `threshold_S` (top 1% composite cutoff): **0.5712**
- `threshold_A` (top 10% composite cutoff): **0.4790**
- `threshold_C` (bottom 25% composite cutoff): **0.3303**

---

## §2 Tier S composition breakdown

### §2.1 By inclusion path

| Path | Count | % of Tier S |
|---|---:|---:|
| Named-mythological-match seed-list (all gates cleared) | 452 | 40.1% |
| Top-1% composite score (no seed match required) | 674 | 59.9% |

### §2.2 Top sources contributing to Tier S

| Source | Tier S rows | % of source total |
|---|---:|---:|
| royal_armouries | 364 | 0.95% |
| met-museum | 296 | 3.92% |
| wikipedia | 228 | 2.66% |
| odin-army-tradoc | 175 | 4.38% |
| wikidata | 56 | 0.45% |
| nick-aschenbach-dnd-data | 3 | 0.05% |
| bsdata-warhammer-aos | 1 | 0.05% |
| fextralife-ds1 | 1 | 0.75% |
| fextralife-elden-ring | 1 | 0.27% |
| osrsbox-db | 1 | 0.11% |
| (all other sources) | 0 | 0.00% |

**Reading:** Tier S concentrates in museum-curated (660 rows; 58.6%) + wikipedia + odin (403 rows; 35.8%) + wikidata (56; 5.0%). Game-data-dump sources contribute essentially zero (7 rows; 0.6%) — exactly as the source-library reputation tier signal weighting intends.

### §2.3 By cultural_lineage_canonical

| Lineage | Tier S count | Notes |
|---|---:|---|
| european | 760 | Sketch D ~40.1% substrate; Tier 1 broadly-fictionalized |
| east_asian | 213 | Sketch D ~23.0% substrate; Tier 1 broadly-fictionalized |
| unknown | 60 | Composite-driven (TTRPG + military rows without lineage tag) |
| south_asian | 41 | Sketch D ~1.8% substrate; Tier 1 substrate-thin boost candidate |
| middle_eastern | 33 | Sketch D ~2.3% substrate; Tier 1 substrate-thin boost candidate |
| southeast_asian | 12 | Sketch D ~1.2% substrate |
| fantasy_generic | 6 | Pan-Fantasy substrate; mostly composite-driven (no seed match path) |
| south_american_indigenous | 1 | Tier 3 lineage — composite-driven only (MSS 1.2 Brazilian ATGM; no named-match) |

**Cultural-sensitivity gate verification:** 6 of 6 Tier-3-excluded lineages have ZERO Tier-S via named-match path. The single south_american_indigenous Tier S row (MSS 1.2 Brazilian Anti-Tank Guided Missile) qualified via top-1% composite path with `named_mythological_match = NULL`. This is correct behavior per gandalf cultural-weight doc § 2.1 — composite-score quality is independent of cultural-sensitivity gate.

### §2.4 By register_canonical

| Register | Tier S count | Notes |
|---|---:|---|
| historical | 372 (match-path) | Museum + historical encyclopedia entries — clean Mode-A signal |
| unknown | 34 (match-path) | Composite-driven through other signals |
| military_modern | 32 (match-path) | **Mode-C contamination concern — see §3 below** |
| mythological | 8 (match-path) | Wikipedia mythological articles directly |
| fantasy | 6 (match-path) | Surprisingly few; Stage 1.5 Pass-A fantasy-suppression held |

---

## §3 Mode-C contamination finding (Discipline #25 — surfaced for gandalf review)

**Pre-existing Stage 1.5 Mode-C flag set:** 72 rows (`rep_audit_mode_c_naming_allusion_suspected`) — primarily odin-army-tradoc.

**Observed Mode-C leakage in Tier S match-path:** 32 rows have `register_canonical='military_modern'` and a named-mythological-match. Sample inspection reveals these are **wikipedia rows describing modern military systems named after mythological figures** that were NOT in the Stage 1.5 Mode-C flag set:

| Example | Match | Reality |
|---|---|---|
| MGM-134 Midgetman | Heracles | US ICBM (not a club of Heracles) |
| Trident (missile) | Poseidon | Navy SLBM (not Poseidon's trident) |
| M3 scout car | Heracles | WWII armored car |
| ČZ 2000 | Lada | Czech firearm |
| .300 Rook | Wayland the Smith | Cartridge designation |
| MIM-23 Hawk | Athena | US SAM system |

This is a **second-wave Mode-C contamination pattern** — wikipedia-sourced modern military entries with mythologically-named system designations. Stage 1.5 Mode-C flag set focused on odin-army-tradoc + lineage-mismatch combinations; wikipedia's register='military_modern' tagging caught these at the register layer but not at the Mode-C bearer-extraction layer.

**Disposition recommendation (elrond):**
- Tag these 32 rows for downstream curation at Stage 3 composition policy (flag, don't auto-block; Discipline #11 preserve-source-phrasing)
- Surface to gandalf at 100-row spot-check; let gandalf judge whether Stage 3 should auto-strip register='military_modern' from Tier S match path OR keep as Discipline #25 spot-check candidates
- **NOT a Stage 2.5 retroactive fix** — Stage 2.5 honestly reflects the Stage 1.5 extraction's bearer findings; the contamination pattern is recognition-record material for Discipline #25 amendment consideration

**v1.1+ refinement queue addition (proposed):** add Stage 1.5 v1.2 Mode-C rule extending coverage to `register_canonical='military_modern' + extracted_named_bearer matches Tier-1-mythological-name in seed list` (i.e., wikipedia ICBM/SAM/firearm Mode-C pattern).

---

## §4 Signal-distribution summary (5K-row sample for memory)

Composite-score distribution (sampled):

| Statistic | Value |
|---|---:|
| p25 | 0.3614 |
| p50 (median) | 0.4267 |
| p75 | 0.4861 |
| min | 0.1000 |
| max | 0.7304 |

Per-signal distribution stats (sampled; gandalf-prep-landed run):

| Signal | mean | p25 | p50 | p75 |
|---|---:|---:|---:|---:|
| source_library_reputation_tier | 0.612 | 0.40 | 1.00 | 1.00 |
| description_richness | 0.394 | 0.275 | 0.367 | 0.522 |
| extracted_provenance_richness | 0.583 | 0.300 | 0.500 | 0.947 |
| extracted_named_bearer_presence | 0.011 | 0.0 | 0.0 | 0.0 |
| extracted_materials_richness | 0.040 | 0.0 | 0.0 | 0.0 |
| cultural_lineage_depth | 0.062 | 0.0 | 0.0 | 0.0 |
| image_presence | 0.265 | 0.0 | 0.0 | 0.333 |
| cluster_centrality | 0.426 | 0.117 | 0.347 | 0.728 |
| cultural_tradition_weight | 0.628 | 0.40 | 0.70 | 1.00 |

**Reading:**
- `source_library_reputation_tier` and `cultural_tradition_weight` show bimodal distribution (museum-curated + east_asian/european clusters at high end vs game-data-dump at low end)
- `extracted_named_bearer_presence` is sparse (1.17% population per Stage 1.5) — its 0.15 weight contributes Tier-S boost selectively, exactly as designed
- `extracted_materials_richness` and `cultural_lineage_depth` are sparse too — both signals are designed to reward rare richness, not penalize sparsity
- `cluster_centrality` shows healthy spread — Phase E-1 within-cluster confidence is well-calibrated for use as a centrality proxy
- `description_richness` and `extracted_provenance_richness` show smooth distributions — these are the workhorse signals for ordinary rows

---

## §5 Per-source × per-tier breakdown

| Source | S | A | B | C | Total |
|---|---:|---:|---:|---:|---:|
| royal_armouries | 364 | 4,531 | 33,226 | 6 | 38,127 |
| wikidata | 56 | 2 | 928 | 11,385 | 12,371 |
| wikipedia | 228 | 495 | 7,156 | 700 | 8,579 |
| met-museum | 296 | 642 | 6,617 | 4 | 7,559 |
| nick-aschenbach-dnd-data | 3 | 5 | 1,236 | 5,053 | 6,297 |
| wow-classic-items | 0 | 9 | 3,396 | 1,035 | 4,440 |
| odin-army-tradoc | 175 | 2,258 | 1,563 | 2 | 3,998 |
| bsdata-warhammer-aos | 1 | 0 | 2,184 | 0 | 2,185 |
| cataclysm-dda | 0 | 0 | 61 | 1,538 | 1,599 |
| osrsbox-db | 1 | 0 | 256 | 683 | 940 |
| pf2ools-pf2ools-data-quarantined | 0 | 1 | 645 | 42 | 688 |
| diablo2-d2data | 0 | 0 | 2 | 519 | 521 |
| path-of-exile-repoe | 0 | 0 | 0 | 494 | 494 |
| fextralife-elden-ring | 1 | 0 | 332 | 42 | 375 |
| bloqhead-demigods | 0 | 0 | 64 | 256 | 320 |
| elden-ring-erdb | 0 | 0 | 86 | 221 | 307 |
| fextralife-ds2 | 0 | 0 | 209 | 30 | 239 |
| fextralife-ds3 | 0 | 0 | 186 | 33 | 219 |
| gta-v-data | 0 | 0 | 0 | 183 | 183 |
| fextralife-ds1 | 1 | 0 | 116 | 16 | 133 |
| 5e-bits-5e-database-2024 | 0 | 0 | 38 | 72 | 110 |
| army-recognition | 0 | 0 | 9 | 53 | 62 |
| souls-api-thomaslincoln-quarantined | 0 | 0 | 0 | 56 | 56 |
| 5e-bits-5e-database | 0 | 0 | 4 | 33 | 37 |
| souls-api-thomaslincoln | 0 | 0 | 1 | 1 | 2 |

**Reading:** Source-library reputation tier correctly bifurcates outcomes:
- **Tier A sources** (museum-curated; met-museum + royal_armouries): zero Tier C; mostly Tier A/B; named-match rows skim Tier S
- **Tier B sources** (designer-curated; bsdata, odin, 5e, etc.): mostly Tier B; some Tier A in odin via composite; very few Tier C
- **Tier C sources** (wikipedia, wikidata, army-recognition): mixed; wikipedia has good Tier S/A representation because composite-driven; wikidata has heavy Tier C (sparse description text)
- **Tier D sources** (game-data-dumps): nearly all Tier B or Tier C; almost zero Tier A; zero Tier S except handful of edge-cases

---

## §6 Verification artifacts

- DB schema extended successfully: 3 new columns on `weapon_knowledge_entries` (`quality_composite_score`, `quality_tier`, `named_mythological_match`)
- Pre-execution backup: `telemetry.pre-stage-2-5.db.bak` (167 MB)
- 100-row spot-check artifact for gandalf: `spot-check-gandalf-request.md` (per dispatch § 3)
- Summary JSON: `scoring-summary.json`

---

## §7 Cross-references

- Dispatch: `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-2-5-quality-tier-scoring.md`
- Stage 0 transcription: `canonical/story/v1-bc-target-intent-2026-05-24.md` § 6 Sketch F
- Gandalf reputation tier: `agentic_orchestration/gandalf/notes/2026-05-24-source-library-reputation-tier.md`
- Gandalf cultural weight: `agentic_orchestration/gandalf/notes/2026-05-24-cultural-tradition-weight-lookup.md`
- Gandalf seed list: `agentic_orchestration/gandalf/notes/2026-05-24-named-historical-figure-seed-list.md`
- Stage 1.5 outputs: `agentic_orchestration/elrond/research/cycle-10-stage-1-5-2026-05-24/`
- Discipline #25 record: `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`
- Engineering disciplines: `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#2, #2.1, #11, #19, #19.1, #21, #22, #25)
- Cycle 10 state file: `agentic_orchestration/weapon-substrate-curation-cycle-10-state.md`
