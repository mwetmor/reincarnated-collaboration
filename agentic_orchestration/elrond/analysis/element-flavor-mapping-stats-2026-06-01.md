# Q18 Flavor-Pool Research — Phase 4 Statistical Analysis Verdict

**STATUS:** CURRENT (PG-2 input)
**Date:** 2026-06-01
**Author:** elrond (data steward + statistical analysis seam)
**Wave:** `WS1A.Q18-flavor-pool-research`
**Phase / phase-gate:** Phase 4 stats verdict → PG-2 (gandalf ratification)
**Authority:** Matt 2026-06-01 "hand to KR to fire the wave" + jack-ryan Phase 4 Gate-1 PASS-with-INFO 2026-06-01 + elrond PG-0 § 5 methodology lock
**Dispatch:** `agentic_orchestration/dispatches/2026-06-01-elrond-cycle-15-ws1a-q18-phase-4-statistical-analysis.md`
**Companion artifacts:**
- `agentic_orchestration/elrond/analysis/q18_flavor_candidates_2026-06-01.db` (transient SQLite, 2 tables: candidates + manifests)
- `agentic_orchestration/elrond/analysis/q18_flavor_ingest_summary_2026-06-01.json`
- `agentic_orchestration/elrond/analysis/q18_flavor_stats_results_2026-06-01.json` (raw per-step machine-readable results)
- `agentic_orchestration/research/scripts/q18_flavor_phase4_analysis.py` (reproducible pipeline)

---

## 0. TL;DR

- **217 rows ingested. 0 schema validation issues.** Ingest matches expected count exactly.
- **Per-primary unique candidate counts** (after dedup on `candidate`): fire=15, water=13, earth=10, wind=35, lightning=12, holy=38, shadow=35, physical=13.
- **T calibration:** T_principal=6 (substrate-led against pool.json allow-list reference; also reporting T_permissive=4 and T_strict=9 for synthesis flexibility).
- **Floor cardinality recommendations at T=6:** fire=8, water=10, earth=3, wind=21, lightning=11, holy=19, shadow=17, physical=9. (Per dispatch § 8: these are EMPIRICAL FLOORS; Phase 5a synthesis curation owns final pool sizing.)
- **7-vs-8 empirical verdict: WEAK-8.** Quantitative axes (rows, unique candidates, tracks_covered=3) satisfy STRONG-8 thresholds, BUT substrate-type concentration analysis shows physical is qualitatively distinct: 0.85 modal share in `mechanical_keyword` vs rotating primaries' 0.32–0.70. Physical surfaces as a **damage-type taxonomy** (pierce / slash / bludgeon / sever / force) — not a sub-element flavor pool. This is the load-bearing empirical signal for Matt's PG-3 architectural commitment.
- **Confidence-degraded primaries:** earth (MEDIUM by rule; 14 rows, 10 unique); physical (HIGH by quantitative rule, but Phase 3 deliberately excluded physical expansion → degraded BY CONSTRUCTION); wind (HIGH by rule, but flag retained per gandalf PG-1 § 2 override surface 1 that wind is structurally under-served — see § 8.3).
- **Borderline candidates:** `lux` (1 row, JRPG_isekai only, score=4) and `celestial` (1 row, JRPG_isekai only, score=4) confirmed SINGLE-TRACK BORDERLINE. Broader borderline audit surfaces 92 additional single-track candidates across all primaries — itemized § 10.
- **F-6 contingency:** NOT FIRED. Data shape is firmly quantitatively-amenable; structured citations, recognizability scores, substrate-type enum, and contamination lists all carry expected signal density.
- **Phase 3 methodology deviation:** legolas-direct executed Phase 3 prompts (Agent tool unavailable). Schema fidelity is excellent (0 validation issues). One structural observation: the expansion sub-agents converged on cleaner schema discipline than Phase 1 samplers (richer notes, more consistent contamination lists). No data-quality concern identified.

**Routing back to KR:** proceed to PG-2 (route stats verdict to gandalf for ratification).

---

## 1. Ingest summary

### 1.1 Row counts

| Source | Files | Rows |
|---|---|---|
| Phase 1 sample | sample-A.jsonl | 48 |
| Phase 1 sample | sample-B.jsonl | 40 |
| Phase 1 sample | sample-C.jsonl | 37 |
| Phase 3 expansion | full-ARPG-wind.jsonl | 14 |
| Phase 3 expansion | full-ARPG-holy.jsonl | 17 |
| Phase 3 expansion | full-JRPG_isekai-shadow.jsonl | 25 |
| Phase 3 expansion | full-JRPG_isekai-holy.jsonl | 16 |
| Phase 3 expansion | full-tabletop_myth-wind.jsonl | 20 |
| **Total** | **8 files** | **217** |

Expected: 217. Actual: 217. Match exact.

### 1.2 Validation

**0 schema validation issues across 217 rows.** All required fields present per PG-0 § 3.1; all enums respected (`primary_element` in 8-set; `track` in 3-set; `recognizability_score` ∈ {1,2,3}).

### 1.3 Per-primary row counts

| Primary | rows | Per track (ARPG / JRPG_isekai / tabletop_myth) |
|---|---|---|
| fire | 17 | 7 / 5 / 5 |
| water | 17 | 7 / 5 / 5 |
| earth | 14 | 6 / 4 / 4 |
| wind | 47 | 19 / 5 / 23 |
| lightning | 16 | 6 / 5 / 5 |
| holy | 49 | 23 / 21 / 5 |
| shadow | 42 | 6 / 31 / 5 |
| physical | 15 | 5 / 5 / 5 |

Expansion concentration reflects gandalf PG-1 ratification scope (wind ARPG+tabletop / holy ARPG+JRPG / shadow JRPG). Physical row count baseline-only (Phase 1 only; Phase 3 deliberately excluded per architectural-commitment routing).

### 1.4 Recognizability + substrate distributions

Recognizability: R=1: 21 (10%), R=2: 103 (47%), R=3: 93 (43%). Strong skew to R=2/R=3 (well-known vocabulary), which is the expected research-yield shape for genre-canonical sampling.

Substrate types: phenomenon 82, mechanical_keyword 36, proper_noun 35, mythological 31, material 28, ailment 4, other 1. Distribution validates the substrate-type enum captures observed variation; the `other` bucket is a single row (negligible noise).

### 1.5 Manifest sidecar load

8 `.manifest.json` files loaded into `manifests` SQLite table. Manifest yield judgments + qualitative narrative preserved for Phase 5 synthesis consumption.

---

## 2. Per-primary candidate frequency distribution

**Method (per PG-0 § 5 + dispatch § 3.3):**
- weight per candidate = sum over rows of (recognizability_score × citation_count)
- Phase 1 + Phase 3 rows combine on (primary, candidate) before scoring
- Rank by citation-weighted score descending, then track_count, then total_citations

### 2.1 Top candidates per primary (cap top 10; full ranking in `q18_flavor_stats_results_2026-06-01.json`)

**fire** (15 unique, 17 rows):

| Rank | Candidate | Score | Tracks | Substrate |
|---|---|---:|---:|---|
| 1 | ember | 12 | 2 | material |
| 2 | cinder | 8 | 2 | material |
| 3 | agi | 6 | 1 | proper_noun |
| 4 | blaze | 6 | 1 | phenomenon |
| 5 | fira | 6 | 1 | proper_noun |
| 6 | ignite | 6 | 1 | ailment |
| 7 | inferno | 6 | 1 | phenomenon |
| 8 | scorch | 6 | 1 | phenomenon |

**water** (13 unique, 17 rows):

| Rank | Candidate | Score | Tracks | Substrate |
|---|---|---:|---:|---|
| 1 | glacial | 8 | 2 | material |
| 2 | tide | 8 | 2 | phenomenon |
| 3 | torrent | 8 | 2 | phenomenon |
| 4 | brine | 6 | 2 | material |
| 5 | aqua | 6 | 1 | material |
| 6 | blizzara | 6 | 1 | proper_noun |
| 7 | bufu | 6 | 1 | proper_noun |
| 8 | chill | 6 | 1 | ailment |
| 9 | frost | 6 | 1 | phenomenon |
| 10 | mist | 6 | 1 | phenomenon |

**earth** (10 unique, 14 rows):

| Rank | Candidate | Score | Tracks | Substrate |
|---|---|---:|---:|---|
| 1 | stone | 18 | 3 | material |
| 2 | quake | 12 | 2 | phenomenon |
| 3 | tremor | 8 | 2 | phenomenon |
| 4 | dust | 4 | 1 | material |
| 5 | loam | 4 | 1 | material |
| 6 | salt | 4 | 1 | material |
| 7 | terra | 4 | 1 | proper_noun |
| 8 | thorn | 4 | 1 | material |

**wind** (35 unique, 47 rows — dataset's deepest):

| Rank | Candidate | Score | Tracks | Substrate |
|---|---|---:|---:|---|
| 1 | tempest | 18 | 2 | phenomenon |
| 2 | cyclone | 16 | 2 | phenomenon |
| 3 | whirlwind | 15 | 2 | phenomenon |
| 4 | gale | 14 | 2 | phenomenon |
| 5 | gust | 14 | 2 | phenomenon |
| 6 | squall | 10 | 2 | phenomenon |
| 7 | zephyr | 10 | 2 | mythological |
| 8 | hurricane | 9 | 1 | phenomenon |
| 9 | tornado | 9 | 1 | phenomenon |
| 10 | vortex | 8 | 1 | phenomenon |

**lightning** (12 unique, 16 rows):

| Rank | Candidate | Score | Tracks | Substrate |
|---|---|---:|---:|---|
| 1 | arc | 12 | 2 | phenomenon |
| 2 | static | 8 | 2 | phenomenon |
| 3 | surge | 8 | 2 | phenomenon |
| 4 | volt | 8 | 2 | mechanical_keyword |
| 5 | bolt | 6 | 1 | phenomenon |
| 6 | lightning | 6 | 1 | phenomenon |
| 7 | shock | 6 | 1 | ailment |
| 8 | spark | 6 | 1 | phenomenon |
| 9 | thundara | 6 | 1 | proper_noun |
| 10 | thunder | 6 | 1 | phenomenon |

**holy** (38 unique, 49 rows):

| Rank | Candidate | Score | Tracks | Substrate |
|---|---|---:|---:|---|
| 1 | divine | 18 | 2 | mechanical_keyword |
| 2 | sacred | 18 | 2 | mechanical_keyword |
| 3 | radiance | 17 | 2 | phenomenon |
| 4 | radiant | 12 | 2 | phenomenon |
| 5 | blessed | 12 | 1 | mythological |
| 6 | resurrection | 9 | 1 | mechanical_keyword |
| 7 | dawn | 8 | 2 | phenomenon |
| 8 | aura | 8 | 1 | phenomenon |
| 9 | seraph | 8 | 1 | mythological |
| 10 | consecrated | 6 | 1 | mechanical_keyword |

**shadow** (35 unique, 42 rows):

| Rank | Candidate | Score | Tracks | Substrate |
|---|---|---:|---:|---|
| 1 | void | 18 | 3 | phenomenon |
| 2 | shade | 12 | 3 | mythological |
| 3 | abyss | 9 | 1 | phenomenon |
| 4 | umbra | 8 | 3 | mythological |
| 5 | wraith | 8 | 2 | mythological |
| 6 | blight | 6 | 1 | phenomenon |
| 7 | death knight | 6 | 1 | proper_noun |
| 8 | drain | 6 | 1 | mechanical_keyword |
| 9 | lich | 6 | 1 | mythological |
| 10 | mamudo | 6 | 1 | proper_noun |

**physical** (13 unique, 15 rows):

| Rank | Candidate | Score | Tracks | Substrate |
|---|---|---:|---:|---|
| 1 | pierce | 12 | 2 | mechanical_keyword |
| 2 | sever | 8 | 2 | mechanical_keyword |
| 3 | bleed | 6 | 1 | ailment |
| 4 | bludgeoning | 6 | 1 | mechanical_keyword |
| 5 | force | 6 | 1 | mechanical_keyword |
| 6 | piercing | 6 | 1 | mechanical_keyword |
| 7 | slash | 6 | 1 | mechanical_keyword |
| 8 | slashing | 6 | 1 | mechanical_keyword |
| 9 | strike | 6 | 1 | mechanical_keyword |
| 10 | crush | 4 | 1 | mechanical_keyword |

### 2.2 Structural observation

Physical's top 10 = **9 mechanical_keyword + 1 ailment**. Every rotating primary's top 10 has at least 3 distinct substrate types. This concentration is § 7's load-bearing signal.

---

## 3. Cross-primary contamination matrix

**Construction (per PG-0 § 5 + dispatch § 3.4):**
For each candidate, the "flex set" = union of (primary_element ∪ cross_primary_contamination) across all rows. Cell (A, B) = count of candidates whose flex set contains both A and B. Symmetric; diagonal=0 by construction.

|              | fire | water | earth | wind | lightning | holy | shadow | physical |
|---           |---:  |---:   |---:   |---:  |---:       |---:  |---:    |---:      |
| **fire**     | 0    | 0     | 1     | 0    | 0         | 1    | 3      | 0        |
| **water**    | 0    | 0     | 0     | 7    | 1         | 1    | 1      | 0        |
| **earth**    | 1    | 0     | 0     | 1    | 0         | 1    | 3      | 0        |
| **wind**     | 0    | 7     | 1     | 0    | 1         | 1    | 0      | 1        |
| **lightning**| 0    | 1     | 0     | 1    | 0         | 1    | 0      | 0        |
| **holy**     | 1    | 1     | 1     | 1    | 1         | 0    | 0      | 0        |
| **shadow**   | 3    | 1     | 3     | 0    | 0         | 0    | 0      | 0        |
| **physical** | 0    | 0     | 0     | 1    | 0         | 0    | 0      | 0        |

### 3.1 Cell narratives

- **water ↔ wind = 7** (largest off-diagonal): substrate genuinely conflates ocean-storm / atmospheric-storm vocabulary. Candidates include `hurricane`, `mist`, `njord`, `notus`, `squall`, `stormtide`, `tempest`. Confirms gandalf PG-1 surface 1 (wind/storm/water conflation across genre canon). Phase 5a synthesis must explicitly choose primary slot per candidate.
- **fire ↔ shadow = 3**: dark-fire vocabulary cluster — `dark flame master`, `hellfire`, `sulphur`. Substrate-honest: necromancer/demonic-fire conflation is genre-canonical.
- **earth ↔ shadow = 3**: decay / blight cluster — `blight`, `decay`, `miasma`. Earth-as-decomposition crosses shadow domain.
- **Light off-diagonal everywhere else** (≤1 count): contamination is concentrated in three specific lanes, not a general pattern. The 8-primary scheme has meaningful separation in 25 of 28 off-diagonal cells.

### 3.2 Physical contamination

Physical contaminates only with wind (1 candidate). The candidate is `force` (D&D damage type, also used as a wind-adjacent kinetic concept). Physical's near-zero contamination row is consistent with its damage-type-taxonomy structure: D&D and PoE physical sub-types (pierce/slash/bludgeon) are explicitly designed for semantic non-overlap with elemental flavor.

---

## 4. Cluster analysis per primary

**Method (per PG-0 § 5 + dispatch § 3.2):**
- Substrate-type clusters per primary (always)
- HDBSCAN keyword-embedding clusters over candidate + substrate_type + sampler_notes corpus, min_cluster_size=2, ONLY where candidate_count ≥ 8 (all 8 primaries qualified)

### 4.1 Substrate-type concentration per primary

| Primary | Modal substrate | Modal share | Distinct substrates | Total candidates |
|---|---|---:|---:|---:|
| fire | material | 0.40 | 5 | 15 |
| water | material | 0.38 | 4 | 13 |
| earth | material | 0.70 | 3 | 10 |
| wind | phenomenon | 0.43 | 5 | 35 |
| lightning | phenomenon | 0.67 | 4 | 12 |
| holy | phenomenon | 0.32 | 5 | 38 |
| shadow | proper_noun | 0.49 | 4 | 35 |
| **physical** | **mechanical_keyword** | **0.85** | **3** | **13** |

**Key reading:**
- Rotating primaries distribute across material / phenomenon / mythological / proper_noun / mechanical_keyword / ailment in varying proportions. Modal shares 0.32–0.70.
- **Physical at 0.85 mechanical_keyword is a sharp outlier.** Distinct substrates count = 3 (mechanical_keyword=11, ailment=1, phenomenon=1) — the most concentrated distribution in the dataset.

### 4.2 Keyword-embedding clusters (HDBSCAN)

HDBSCAN ran on all 8 primaries. Cluster counts (label_counts; label -1 = noise):

- fire: {0:3, 1:5, 2:4, -1:1, 3:2} — 4 substantive clusters + 1 noise. Material vs phenomenon split + proper-noun cluster.
- water: {0:10, 1:2, -1:1} — single dominant cluster (broad water vocabulary) + small JRPG proper-noun cluster.
- earth: {0:5, 1:2, -1:3} — material core + small phenomenon cluster + 3 noise.
- wind: {-1:11, 0:2, 2:3, 3:3, 5:4, 4:8, 1:2, 6:2} — fragmented; 7 clusters + 11 noise. Reflects wind's deep but heterogeneous substrate (storm-flex cluster, deity-proper-noun cluster, atmospheric-phenomenon cluster, ailment-adjacent cluster, etc.).
- lightning: {0:5, 1:6, -1:1} — clean 2-cluster split (phenomenon-electric / mythological-thunder).
- holy: {0:22, -1:5, 3:5, 2:2, 1:4} — one dominant cluster (radiance/divine/sacred family) + 3 sub-clusters (religious-keyword / mythological-being / proper-noun).
- shadow: {-1:7, 3:10, 1:2, 0:5, 6:3, 2:2, 4:2, 5:4} — fragmented; 7 clusters + 7 noise. Reflects the three-canonical-layer competition gandalf flagged at PG-1 (SMT proper-noun / FF mechanical / Solo Leveling phenomenon).
- physical: {0:11, 1:2} — **single dominant cluster (n=11)** + tiny 2-element side cluster. Lowest cluster diversity of any primary.

### 4.3 Cluster reading per gandalf PG-1 surfaces

- **Surface 3 (shadow's three-canonical-layer competition) is confirmed by cluster structure.** Shadow's HDBSCAN has 7 distinct clusters, the most fragmented after wind. SMT proper-nouns (mudo / megido / mamudo), FF mechanical (drain / death), Solo Leveling (shadow exchange / shadow army) form distinct keyword neighborhoods.
- **Wind's fragmentation** reflects both depth (47 rows) and structural conflation with storm/water/lightning. Cluster 4 (n=8) likely is the storm-flex group; cluster 5 (n=4) likely is the Greek deity cluster.
- **Holy's dominant cluster (n=22)** reflects the radiance/divine/sacred semantic anchor — the heaviest concentration of any primary around a single vocabulary family. Useful Phase 5a synthesis signal: holy has a STRONG core + scattered satellites.

---

## 5. Cardinality recommendations per primary

### 5.1 T calibration (substrate-led)

Existing pool at `~/Games/reincarnated-engine/data/seasonal_elements/pool.json` carries the substrate-led calibration anchor:

| Primary | Pool allow-list count | Pool primaries covered |
|---|---:|---|
| fire | 20 | yes |
| water | 11 | yes |
| earth | 22 | yes |
| wind | 7 | yes |
| lightning | — | NO ANCHOR |
| holy | — | NO ANCHOR |
| shadow | — | NO ANCHOR |
| physical | — | NO ANCHOR |

Existing pool covers only 4 primaries. For the other 4 (lightning / holy / shadow / physical), T is applied on dataset-internal calibration only — substrate-led discipline DEGRADED for those primaries (Phase 5a synthesis should treat the T-recommended floor as a research-derived signal, not a pool-anchored mandate, for the unanchored 4).

### 5.2 T value selection

**T_principal = 6.** Rationale:
- A candidate with R=2 + 2 citations from each of 2 tracks contributes weight 2 × (2+2) = 8 ≥ T; clearly meets bar.
- A candidate with R=3 + 2 citations contributes 3 × 2 = 6 = T; borderline meets bar.
- A candidate cited once at R=2 contributes 2; below bar. A candidate cited twice at R=3 contributes 6; at bar.
- This places T at the **two-source-recognizability minimum** — corresponds to "appears in genre canon with at least middling recognizability or in multiple sources with niche recognizability."

Reporting also T_permissive=4 and T_strict=9 for Phase 5a synthesis flexibility.

### 5.3 Floor cardinality per primary

| Primary | Total unique | T_perm (4) | **T_princ (6)** | T_strict (9) | Pool anchor | Confidence |
|---|---:|---:|---:|---:|---:|---|
| fire | 15 | 14 | **8** | 1 | 20 | HIGH |
| water | 13 | 12 | **10** | 0 | 11 | HIGH |
| earth | 10 | 8 | **3** | 2 | 22 | MEDIUM |
| wind | 35 | 28 | **21** | 9 | 7 | HIGH (caveat § 8) |
| lightning | 12 | 12 | **11** | 1 | — | HIGH |
| holy | 38 | 29 | **19** | 6 | — | HIGH |
| shadow | 35 | 23 | **17** | 3 | — | HIGH |
| physical | 13 | 12 | **9** | 1 | — | HIGH (caveat § 8) |

### 5.4 Substrate-led interpretation notes

- **Fire (T6=8 vs pool 20):** dataset floor is below existing pool. Substrate-honest read: existing pool already captured the deep fire vocabulary (32 total entries; 20 allow-list); research dataset sample (Phase 1) was narrower in fire scope. Phase 5a synthesis should treat 8 as the FLOOR from research, with pool's existing 20 as the substrate-honest cardinality target. No vocabulary gap surfaced.
- **Water (T6=10 vs pool 11):** dataset floor closely tracks pool cardinality. Substrate-honest read: water vocabulary is mature; research adds candidates (`tide`, `torrent`, `brine`, `glacial`) but does not radically expand. Possible new additions for synthesis: `aqua`, `frost`, `chill` (cross-track presence).
- **Earth (T6=3 vs pool 22):** dataset floor is dramatically below pool. Substrate-honest read: research was thin on earth-specific vocabulary (Phase 3 did not expand earth; baseline-only sampling). Pool's existing 22 captures the substrate-honest depth. No new earth vocabulary additions warranted from this dataset.
- **Wind (T6=21 vs pool 7):** **dataset floor is 3× existing pool.** Phase 3 expanded wind ARPG + tabletop deliberately; result confirms gandalf PG-1 surface 1 — wind is under-served in the existing pool relative to genre-canonical depth. **The clearest single recommendation surface: pool's wind allow-list should expand toward the dataset's high-confidence candidates** (tempest, cyclone, whirlwind, gale, gust, squall, zephyr, hurricane, tornado, vortex are all top-tier).
- **Lightning (T6=11; no pool anchor):** strong yield; vocabulary spans phenomenon-electric (arc, static, surge, bolt), mythological-thunder (Mjolnir-adjacent), mechanical (volt, shock). Synthesis floor of 11 well-supported.
- **Holy (T6=19; no pool anchor):** deepest yield after wind. The radiance/divine/sacred core is robust; secondary cluster of religion-flagged vocabulary (blessed, consecrated, sanctified) provides Phase 5a synthesis with both core + flex options. Per gandalf PG-1 surface 2: non-religious-coded subset (radiance, dawn, aurora-adjacent) is curated emphasis target.
- **Shadow (T6=17; no pool anchor):** three-canonical-layer competition (SMT / FF / Solo Leveling) confirmed by cluster analysis. Synthesis floor of 17 includes representatives from all three layers. Cross-track-confirmed core (void / shade / umbra) carries highest stability.
- **Physical (T6=9; no pool anchor):** mechanical-keyword dominant. Floor of 9 = D&D damage-type taxonomy variants (pierce/piercing, slash/slashing, bludgeon/bludgeoning, sever, strike, force, crush, bleed). **Substrate-honestly, physical's 9 candidates are not flavor-pool entries; they are mechanical damage-types.** Phase 5a synthesis interpretation: physical doesn't have a "flavor pool" in the same sense as elemental primaries.

---

## 6. Track-source weighting validation

### 6.1 Per-track contribution counts

| Track | Rows | Unique candidates | Total citations | Weighted score | Share |
|---|---:|---:|---:|---:|---:|
| ARPG | 79 | 71 | 165 | 371 | 36.6% |
| JRPG_isekai | 81 | 78 | 152 | 377 | 37.2% |
| tabletop_myth | 57 | 57 | 115 | 265 | 26.2% |

### 6.2 Balance audit

- Tracks balance reasonably on weighted score (36.6 / 37.2 / 26.2%). Raw row count was projected 79/81/57 (close to actuals).
- Tabletop_myth contributes proportionally less to weighted score (26.2%) but per gandalf PG-1 § 5 is the rigor anchor for the contamination matrix. Confirmed: tabletop_myth carries the cleanest D&D formal damage-type vocabulary (pierce/slash/bludgeon/force) which keeps physical primary's row sparse but semantically clean.
- ARPG and JRPG_isekai are near-parity. ARPG's 71 unique candidates are slightly fewer than JRPG's 78 unique — JRPG carries the highest substrate-vocabulary diversity (Solo Leveling shadow + SMT proper-nouns + FF mechanical keywords compound).

### 6.3 Weighting recommendation forward to Phase 5a synthesis

Per gandalf PG-1 § 5 forward note:
- **JRPG_isekai weight slightly elevated** for D10 isekai-provisional positioning (Reincarnated's design lineage).
- **tabletop_myth weight slightly elevated** for contamination-matrix rigor (D&D formal types are designed for semantic separation; reliable cross-check anchor).

Suggested multiplicative weights at Phase 5a synthesis: ARPG=1.0, JRPG_isekai=1.15, tabletop_myth=1.10. **These weights are advisory.** Raw weighted-score (this section) remains the primary input; the weights modulate Phase 5a's relative emphasis when ties occur, not the empirical floor calculation.

### 6.4 Per-track substrate-type biases (observation, not adjustment)

- ARPG biases toward `phenomenon` (skill-name-as-effect) and `mechanical_keyword` (passive/affix vocabulary).
- JRPG_isekai biases toward `proper_noun` (FF/SMT spell-tier names) and `mythological` (deity/being vocabulary in isekai god-pantheons).
- tabletop_myth biases toward `material` (alchemical primes, geological vocab) and `mythological` (Greek/Norse deities). D&D PHB formal damage-types are concentrated here.

This bias pattern is genre-canonical and substrate-honest — not a research methodology artifact.

---

## 7. 7-vs-8 empirical answer

**Verdict: WEAK-8.**

### 7.1 Quantitative axes (would suggest STRONG-8)

| Axis | Physical | Rotating MIN | Rotating MEDIAN | Pass STRONG-8? |
|---|---:|---:|---:|---|
| Rows | 15 | 14 (earth) | — | yes |
| Unique candidates | 13 | 10 (earth) | 15 | yes |
| Weighted score sum | 76 | 62 (earth) | 82 | yes |
| Mean weighted score per candidate | 5.8 | — | — | comparable |
| Tracks covered | 3 (all 3) | — | — | yes (full coverage) |

By the quantitative-only rule, physical satisfies STRONG-8: it surfaces in all three tracks with row counts, candidate diversity, and weighted scores matching or exceeding rotating primaries' minimum.

### 7.2 Qualitative substrate-type axis (drags verdict to WEAK-8)

Substrate-type modal concentration:

| Primary | Modal substrate | Modal share | Distinct substrates |
|---|---|---:|---:|
| fire | material | 0.40 | 5 |
| water | material | 0.38 | 4 |
| earth | material | 0.70 | 3 |
| wind | phenomenon | 0.43 | 5 |
| lightning | phenomenon | 0.67 | 4 |
| holy | phenomenon | 0.32 | 5 |
| shadow | proper_noun | 0.49 | 4 |
| **physical** | **mechanical_keyword** | **0.85** | **3** |

**Physical's modal share of 0.85 mechanical_keyword is a 0.15-pt margin above the next-most-concentrated primary (earth at 0.70).** Distinct substrate count of 3 is the lowest in the dataset.

The substantive content of physical's vocabulary:
- pierce, piercing, slash, slashing, bludgeoning, sever, strike, force, crush, kinetic (mechanical_keyword)
- bleed (ailment)
- impact (one phenomenon-coded entry)

This is **the D&D 5e damage-type taxonomy** (PHB ch.9 damage types: bludgeoning, piercing, slashing, plus force) plus its ARPG analogues (PoE's physical-damage subtypes; Diablo's affix system). It's substrate-honestly a **mechanical damage classification**, not a sub-element flavor vocabulary.

### 7.3 Cluster analysis corroboration

HDBSCAN on physical: one dominant cluster (n=11) + one 2-element side cluster. Lowest cluster diversity in the dataset. The dominant cluster captures the D&D damage-type taxonomy en bloc. Rotating primaries (even earth, the most substrate-concentrated rotating primary) have 2–7 distinct keyword clusters.

### 7.4 Contamination structure

Physical's row in the contamination matrix is near-empty (1 contamination total, with wind via `force`). Rotating primaries average 2.6 contamination cells with content. This is **the opposite of what rotating primaries do** — rotating primaries actively flex/contaminate; physical sits in a semantically-isolated mechanical lane.

### 7.5 Verdict reasoning

The 7-vs-8 question reframed: **does physical have a sub-element flavor pool structurally comparable to fire/water/earth/wind/lightning/holy/shadow?**

- **Quantitatively yes** (it surfaces; it has citations; it has track coverage).
- **Qualitatively no** (the citations resolve to a damage-type taxonomy with 0.85 modal substrate concentration, near-zero contamination, and a single dominant HDBSCAN cluster).

**WEAK-8: physical can be the 8th primary, but its sub-element pool would be a damage-type pool (mechanical, taxonomic, near-semantic-non-overlap) rather than a flavor pool (substrate-diverse, contamination-rich, phenomenon-/material-/mythological-mixed). Phase 5a synthesis and Matt at PG-3 must decide whether this asymmetric structure is acceptable for the 8-element scheme.**

### 7.6 Phase 3 absence caveat

**Phase 3 deliberately excluded physical expansion cells** per gandalf PG-1 § 2 (architectural-commitment territory routed to PG-3). The WEAK-8 verdict is anchored on Phase 1 sample data + cross-track structure only. **It is possible that physical expansion (if it were fired) would surface additional substrate-types not captured in baseline sampling.** Candidate non-mechanical physical vocabulary not yet sampled: `kinetic`, `impact-debris`, `crater`, `weight`, `concussion`, `friction`. Whether such expansion would meaningfully change the 0.85 modal concentration is unknowable without firing.

The empirical answer this dispatch provides is the strongest answer the existing dataset supports.

### 7.7 Decision input for Matt (NOT a recommendation; per dispatch § 8 out-of-scope)

The empirical 7-vs-8 picture for Matt's PG-3:
- **If 8-primary scheme** → physical's sub-pool will look qualitatively different (mechanical-taxonomy), not flavor-pool-shaped.
- **If 7-primary scheme** → physical can route through the existing rotating primaries' kinetic/blunt-flavor overlap (earth's `thorn`, wind's `shear`, water's `torrent`-as-impact) without losing semantic ground.
- **Either choice has substrate evidence.** The data does not by itself force the answer.

---

## 8. Per-primary statistical confidence

| Primary | Rows | Unique | Tracks | Rule confidence | Adjustment | Final |
|---|---:|---:|---:|---|---|---|
| fire | 17 | 15 | 3 | HIGH | — | **HIGH** |
| water | 17 | 13 | 3 | HIGH | — | **HIGH** |
| earth | 14 | 10 | 3 | MEDIUM | pool depth backs synthesis | **MEDIUM** |
| wind | 47 | 35 | 3 | HIGH | gandalf PG-1 § 2 surface 1 caveat | **HIGH (caveat)** |
| lightning | 16 | 12 | 3 | HIGH | no pool anchor | **HIGH** |
| holy | 49 | 38 | 3 | HIGH | religious-coding curation surfacing § 10 | **HIGH** |
| shadow | 42 | 35 | 3 | HIGH | three-layer competition § 4.2 | **HIGH** |
| physical | 15 | 13 | 3 | HIGH | by-construction degraded (no expansion) + WEAK-8 substrate signal | **DEGRADED** |

### 8.1 Earth confidence

Earth is MEDIUM by rule (14 rows, just shy of 15 threshold). Substrate-led discipline applies: existing pool has 22 allow-list earth entries — the substrate is well-anchored despite thin research yield. Synthesis should lean on pool-anchored vocabulary; research adds marginal value to earth.

### 8.2 Wind confidence

Wind is HIGH by quantitative rule (47 rows, 35 unique, all 3 tracks). However, **per gandalf PG-1 § 2 override surface 1**, wind is structurally under-served in source canon — the high yield in THIS research is concentrated in storm-flex vocabulary (tempest, cyclone, whirlwind, gale, gust, squall) which carries the cross-elemental conflation surfaced in § 3 (water↔wind=7 contamination cell). Substrate-honestly: wind has GENUINE depth in the storm-cluster but THIN depth in wind-PURE vocabulary. Phase 5a synthesis should preserve this asymmetry when curating.

### 8.3 Physical confidence — DEGRADED

Physical is HIGH by the row-count quantitative rule but **DEGRADED in this verdict for two reasons:**
1. **By-construction degradation:** Phase 3 deliberately excluded physical expansion. Sample-only depth means substrate not fully probed.
2. **WEAK-8 substrate signal:** the mechanical_keyword concentration (0.85) means even the surfaced candidates are not flavor-pool-shaped; this is a structural fact about the substrate, not a research yield issue.

The combined effect: **physical's 9-candidate T6 floor is well-grounded for what was sampled, but the sampled substrate type does not match the flavor-pool semantic the project's other primaries carry.** Phase 5a synthesis should treat physical's recommendation as a DAMAGE-TYPE-POOL recommendation, not a FLAVOR-POOL recommendation.

---

## 9. Bootstrap stability + acceptance criteria

### 9.1 Bootstrap method

200 iterations of resample-rows-with-replacement per primary. For each candidate above T6 in the base score, measure fraction of iterations where it remains above T6 after resampling. Reports per-candidate stability percentage + per-primary median stability.

### 9.2 Per-primary median stability of above-T candidates

| Primary | Above-T candidates | Median stability |
|---|---:|---:|
| fire | 8 | 0.63 |
| water | 10 | 0.64 |
| earth | 3 | 0.88 |
| wind | 21 | 0.65 |
| lightning | 11 | 0.66 |
| holy | 19 | 0.64 |
| shadow | 17 | 0.64 |
| physical | 9 | 0.65 |

Earth's high median (0.88) reflects its 3-candidate-above-T being all robustly cross-track confirmed (stone in 3 tracks; quake in 2; tremor in 2). Other primaries' medians cluster around 0.63–0.66, which means the average above-T candidate appears above T in ~⅔ of resamples — a typical bootstrap-stability range for citation-sparse datasets. Per-candidate stability values are itemized in `q18_flavor_stats_results_2026-06-01.json`.

### 9.3 Three-track agreement (high-confidence classification)

Acceptance criterion: candidate has score ≥ T6 AND is cited from ≥ 2 of 3 tracks. Per primary:

| Primary | High-confidence candidates | Names (sorted by score) |
|---|---:|---|
| fire | 2 | ember, cinder |
| water | 4 | tide, torrent, glacial, brine |
| earth | 3 | stone, quake, tremor |
| wind | 7 | tempest, cyclone, whirlwind, gale, gust, squall, zephyr |
| lightning | 4 | arc, surge, static, volt |
| holy | 5 | divine, sacred, radiance, radiant, dawn |
| shadow | 4 | void, shade, umbra, wraith |
| physical | 2 | pierce, sever |

**Total: 31 high-confidence candidates across all 8 primaries.** This is the synthesis-curation core; Phase 5a should treat these as the strongest pool-extension recommendations.

### 9.4 Acceptance criterion fire

All 4 acceptance criteria from PG-0 § 3.6:

1. **Variance threshold on bootstrap-stability** → REPORTED (§ 9.2). Median stabilities 0.63–0.88; itemized per-candidate.
2. **Minimum agreement across 3 tracks for high-confidence classification** → REPORTED (§ 9.3). 31 high-confidence candidates surfaced.
3. **Explicit per-primary confidence-degradation naming** → REPORTED (§ 8). Earth=MEDIUM (rule-based), Physical=DEGRADED (by-construction + WEAK-8), wind=HIGH-with-caveat.
4. **Borderline candidate audit** → REPORTED (§ 10).

---

## 10. Borderline candidate audit

### 10.1 Explicit Phase 3 close-note flags

Per Phase 3 close note + dispatch § 2 deliverable 9:

**`lux`:**
- Found: yes
- Tracks: JRPG_isekai only (1 track)
- Primary: holy
- Rows: 1
- Citation-weighted score: 4
- Max recognizability: 2
- **Verdict: SINGLE-TRACK BORDERLINE.** Below T6 threshold; not cross-track confirmed. Recommend Phase 5a synthesis HOLD for designer-judgment OR defer to curation. Substrate-honestly: `lux` is Latin-tier vocabulary that didn't surface in ARPG or tabletop sampling.

**`celestial`:**
- Found: yes
- Tracks: JRPG_isekai only (1 track)
- Primary: holy
- Rows: 1
- Citation-weighted score: 4
- Max recognizability: 2
- **Verdict: SINGLE-TRACK BORDERLINE.** Same shape as lux. NOT confirmed cross-track. Per gandalf PG-1 § 2 surface 2, holy is the most thematically-entangled primary; Phase 5a synthesis owns this curation call.

### 10.2 General borderline (single-track + score 4-8) per primary

Definition: candidate appears in only 1 track AND citation-weighted score is in [4, 8] (above noise floor but below T6 or just at T6).

| Primary | Borderline count | Notable single-track-only candidates |
|---|---:|---|
| fire | 12 | agi, blaze, fira, ignite, inferno, scorch, char, conflagration, crimson |
| water | 8 | aqua, blizzara, bufu, chill, deluge, frost, mist, spume |
| earth | 5 | dust, loam, salt, terra, thorn |
| wind | 19 | aeolus, aero, blast, etc. (most JRPG/tabletop wind vocab is single-track because expansion was concentrated in ARPG + tabletop) |
| lightning | 8 | bolt, lightning, plasma, shock, spark, thundara, thunder |
| holy | 22 | aether, aura, banish, celestial, consecrated, lux, etc. |
| shadow | 18 | blight, dark wisdom, death knight, death lord, decay, etc. |
| physical | 10 | bleed, bludgeoning, crush, force, impact, piercing, slash, slashing, strike |

**Total: 92 single-track borderline candidates across all primaries.** Detailed enumeration in `q18_flavor_stats_results_2026-06-01.json` § `borderline_audit.general_borderline`.

### 10.3 Borderline-audit synthesis-input observation

Single-track borderline does NOT mean "drop." For some primaries (notably wind in tabletop, holy in ARPG), single-track presence reflects the genre-specific vocabulary that gandalf PG-1 § 5 flagged for elevated track weight. Phase 5a synthesis should:

1. Treat 31 high-confidence (§ 9.3) candidates as the core recommendation.
2. Treat single-track borderline as **designer-judgment surfaces**: e.g., `aeolus` is Greek mythological singular-track but exactly the kind of mythological depth tabletop_myth was elevated for.
3. Lux + celestial specifically: defer to Matt at PG-3 if non-religious holy vocabulary is the synthesis priority (per gandalf PG-1 § 2 surface 2). Both are non-religion-coded Latin-tier vocabulary; both are single-track-only by structural sampling artifact (not by substrate scarcity).

---

## 11. Phase 4 contingency assessment

**F-6 (qualitative-collapse fallback) FIRED?: NO.**

The dataset was firmly quantitatively-amenable:
- 0 schema validation issues across 217 rows.
- Recognizability scores distributed across 1/2/3 with healthy spread (10/47/43%).
- Substrate-type enum captured observed variation (6 of 7 enum values populated; `other` is 1 row).
- Citation lists are well-populated (average 1.7 citations per row; max 4).
- Cross-primary contamination lists provided structured 8×8 matrix construction without ad-hoc interpretation.

All 4 dispatch § 2 deliverables produced from structured fields; no qualitative-only-readable signal was load-bearing.

---

## 12. Phase 3 methodology-deviation observation

**Deviation per Phase 3 close note:** legolas-direct executed all 5 Phase 3 expansion prompts because the Agent tool was unavailable in legolas's sub-agent session. Outputs were schema-compliant, cited, and validated.

### 12.1 Data-quality observations

- **Schema fidelity is EXCELLENT.** 0 validation issues across 92 Phase 3 rows (vs 0 issues across 125 Phase 1 rows; parity).
- **Citation density per row** (Phase 3 mean 1.78 cites/row vs Phase 1 mean 1.66 cites/row) — Phase 3 actually marginally HIGHER citation density. Consistent with the deeper-expansion brief.
- **Substrate-type distribution** in Phase 3 rows skews more toward `proper_noun` (consistent with Solo Leveling / SMT expansion brief) and `mythological` (Greek wind deities). Substrate-type enum is faithfully applied.
- **Cross-primary contamination lists** in Phase 3 rows are richer (notably tabletop-wind expansion surfaced 7 water-wind contamination candidates — the matrix's largest off-diagonal cell). Phase 3 sub-agent discipline on contamination flagging was strong.

### 12.2 Concerns or anomalies

**None identified.** The legolas-direct execution path produced data of comparable or higher quality than the sub-agent execution path would have. The deviation does NOT introduce data-quality concerns for downstream Phase 5a synthesis.

### 12.3 Observation for ops surface

The Phase 3 methodology deviation is an ORCHESTRATION-PATH artifact, not a research-quality artifact. Knight-rider and gandalf may wish to capture this as an operational-procedure observation (when Agent tool is unavailable in a sub-agent's session, direct execution by the senior-agent with the methodology already locked is a viable fallback that does not degrade data quality). NOT in this verdict's scope to author that observation; surfacing for orchestration awareness only.

---

## 13. Routing back to KR

Phase 4 statistical analysis complete. Outputs:

- **Primary deliverable:** this stats verdict at `agentic_orchestration/elrond/analysis/element-flavor-mapping-stats-2026-06-01.md`
- **Transient SQLite:** `agentic_orchestration/elrond/analysis/q18_flavor_candidates_2026-06-01.db` (2 tables: candidates, manifests)
- **Ingest summary JSON:** `agentic_orchestration/elrond/analysis/q18_flavor_ingest_summary_2026-06-01.json`
- **Raw per-step results JSON:** `agentic_orchestration/elrond/analysis/q18_flavor_stats_results_2026-06-01.json`
- **Reproducible pipeline:** `agentic_orchestration/research/scripts/q18_flavor_phase4_analysis.py`

**Routing instruction for KR:** **proceed to PG-2 (route stats verdict to gandalf for ratification).** Gandalf PG-2 ratifies this verdict's empirical reads as input to Phase 5a synthesis. Out-of-scope per dispatch § 8: no synthesis curation, no decisions-log entry, no architectural-commitment recommendation on 7-vs-8 (Matt at PG-3 owns that decision).

---

## End of Phase 4 stats verdict.
