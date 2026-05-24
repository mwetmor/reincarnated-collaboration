# Cultural-Tradition Weight Lookup — Cycle 10 Stage 2.5 Input (Fate-Genre Story/Feel Rubric)

**Date:** 2026-05-24
**Author:** gandalf (story-and-design steward)
**Consumer:** elrond Stage 2.5 quality-composite scoring script (signal weight 0.05 per dispatch § 2)
**Substrate:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` (89,841 rows; 14 distinct cultural_lineage_canonical values; enumerated 2026-05-24)
**Companion docs:**
- `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-2-5-quality-tier-scoring.md` (consumer dispatch)
- `canonical/story/v1-bc-target-intent-2026-05-24.md` § 4 Sketch D + § 6 Sketch F (Tier 1/2/3 cultural-sensitivity stratification)
- `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` (Discipline #25 — Mode-B contamination empirically affects 4 of 5 marginal lineages)
- `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` (Fate-genre as story/feel reference)
- Companion lookup: `agentic_orchestration/gandalf/notes/2026-05-24-source-library-reputation-tier.md`

---

## 0. TL;DR

14 cultural_lineage_canonical values present in `weapon_knowledge_entries`. Distribution (Fate-genre story/feel weight × Tier 1/2/3 cultural-sensitivity):

| Tier | Count | Weight range | Lineages |
|---|---|---|---|
| **Tier 1 broadly-fictionalized (Fate-rich)** | 3 | 0.7-1.0 | european / east_asian / fantasy_generic |
| **Tier 1 broadly-fictionalized (Fate-moderate)** | 1 | 0.5 | cross_cultural |
| **Tier 2 substrate-thin Fate-genre-boost candidates** | 3 | 0.5-0.7 | middle_eastern / south_asian / southeast_asian |
| **Tier 3 EXCLUDED (per Sketch F § 6.3)** | 6 | 0.0 | north_american_indigenous / arctic_circumpolar / oceanic / mesoamerican / south_american_indigenous / african |
| **Unlabeled / passthrough** | 1 | 0.4 | unknown |

**Critical Discipline #25 rep-audit flag:** the 5 Tier 3 indigenous lineages plus `african` ALL show Mode-B (geographic-region-of-origin) contamination per marginal-lineage-tagging-pattern record. Empirical register-split confirms: south_american_indigenous has 25/216 military_modern; arctic_circumpolar 30/56 military_modern; oceanic 22/41 military_modern; mesoamerican 8/97 military_modern; african 53/563 military_modern. Tier 3 exclusion (weight=0.0) AND `excluded_from_tier_s: true` flag prevent these from auto-include via named-mythological-match path — regardless of any apparent named-bearer match these rows might surface, downstream cultural-sensitivity discipline holds.

**Critical Discipline #25 rep-audit flag for fantasy_generic:** the 17,165-row fantasy_generic pool has Pass-A bearer suppression already enforced at Stage 1.5 extraction time (per per-source-coverage.md §1 footnote¹). High Fate-genre weight (1.0) is justified — Pan-Fantasy bucket is RICH (~24.8% substrate, ~20% target form-share per Sketch D § 4.3). Names like "Greataxe of Agonizing Paralysis" are NOT person-attributions; they are fictional-attribute-naming convention. Weight 1.0 reflects story/feel value; named-mythological-match path still gates correctly via Pass-A suppression.

---

## 1. Lookup table (load-bearing — structured-data block parseable by Stage 2.5 scoring script)

```yaml
# cultural_tradition_weight.yaml
# Each entry: cultural_lineage_canonical → fate_genre_weight (0.0-1.0) + tier (1/2/3) + excluded_from_tier_s flag
# Consumer: elrond Stage 2.5 score_quality_composite.py
# Signal weight in composite: 0.05 (per dispatch § 2)

cultural_traditions:

  # ---------- Tier 1 broadly-fictionalized — Fate-genre RICH (weight 0.7-1.0) ----------

  - cultural_lineage_canonical: "european"
    fate_genre_weight: 1.0
    tier: 1
    excluded_from_tier_s: false
    reasoning: |
      Broadest Fate-genre coverage: Arthurian (Excalibur, Caliburn, Galatine,
      Round Table cast), Carolingian (Roland's Durandal, Olivier's Hauteclere,
      Charlemagne's Joyeuse), Norse (Mjolnir, Gram, Gungnir), Greek (Achilles,
      Heracles, Theseus), Celtic (Cú Chulainn's Gáe Bolg, Fragarach), Slavic
      (Baba Yaga, Koshchei). 28,595 rows / 40.1% substrate — RICH. Sketch D
      § 4.1 ~18% v1 form-share for medieval/Arthurian/Carolingian alone, plus
      Norse (~10%), Greek (~8%), Celtic (~6%), Slavic (~3%) subsets.

  - cultural_lineage_canonical: "east_asian"
    fate_genre_weight: 1.0
    tier: 1
    excluded_from_tier_s: false
    reasoning: |
      Japanese mythology + folklore (Kusanagi-no-Tsurugi, Ame-no-Habakiri,
      Muramasa, Masamune), Chinese Three Kingdoms (Lu Bu's Sky Piercer Halberd,
      Guan Yu's Green Dragon Crescent Blade, Zhao Yun's Dragon Spear), wuxia
      tradition. Strong Fate-genre precedent: Hattori Hanzō, Sengoku-era
      figures broadly-fictionalized; Mushoku Tensei / Solo Leveling reference
      pool. 16,102 rows / 23.0% substrate — RICH. Sketch D ~15% v1 form-share.

  - cultural_lineage_canonical: "fantasy_generic"
    fate_genre_weight: 1.0
    tier: 1
    excluded_from_tier_s: false
    reasoning: |
      Pan-Fantasy bucket — engine-named-original space; cross-cultural hybrid
      forms; D&D-tradition naming + Souls-tradition naming + WoW-tradition
      naming. RICH at 17,165 rows / 24.8% substrate; Sketch D § 4.3 calls for
      ~20% target form-share (HEFTY allocation). Pass-A bearer suppression
      enforced at Stage 1.5 (per per-source-coverage.md §1 footnote¹) — fictional-
      attribute names like "Greataxe of Agonizing Paralysis" do NOT trigger
      named-mythological-match path. High weight = high Fate-genre story/feel
      value (cross-cultural hybrids ARE Fate-aesthetic-coherent).

  - cultural_lineage_canonical: "cross_cultural"
    fate_genre_weight: 0.7
    tier: 1
    excluded_from_tier_s: false
    reasoning: |
      Hellenistic-cross / Custer-with-Art-of-War / Caesar-with-Greek-philosophy
      hybrid space per Sketch D § 4.4. 1,672 rows / 2.4% substrate. Fate-genre
      hybrid space is moderate-precedent (Fate/Apocrypha cross-cultural Servant
      pairings; Reincarnation War Rift mechanic per Fate-trajectory doc).
      Lower weight than fantasy_generic because the cross-cultural tag captures
      more uncertain blends, but still Tier 1 by sensitivity stratification.

  # ---------- Tier 2 substrate-thin Fate-genre-boost candidates (weight 0.5-0.7) ----------

  - cultural_lineage_canonical: "middle_eastern"
    fate_genre_weight: 0.7
    tier: 1
    excluded_from_tier_s: false
    reasoning: |
      Egyptian mythology (Anubis, Set, Cleopatra Tier 2 historical), Persian
      Shahnameh (Rustam, Esfandiyar), Mesopotamian (Gilgamesh, Enkidu, Marduk,
      Ishtar — Tier 1 mythological). Moderate Fate-genre presence (Gilgamesh
      is a foundational Fate Servant). 1,650 rows / 2.3% substrate — THIN;
      Sketch D § 4.3 calls for boost via targeted crawl (~5-7% target form-
      share vs 2.3% current). Empirical: 1,223 historical / 426 military_modern
      — moderate Mode-B contamination but historical-Mode-A signal dominates.
      Weight 0.7 reflects strong Fate-precedent + substrate-thin boost-priority.

  - cultural_lineage_canonical: "south_asian"
    fate_genre_weight: 0.7
    tier: 1
    excluded_from_tier_s: false
    reasoning: |
      Vedic / Hindu mythology (Karna's Vasavi Shakti, Arjuna's Gandiva, Rama's
      bow, Shiva's Trishula, Indra's Vajra). Strong Fate-genre presence (Karna
      + Arjuna are foundational Fate/Apocrypha Servants). 1,538 rows / 1.8%
      substrate — THIN; Sketch D § 4.3 calls for boost (~5-6% target form-
      share). Empirical register split: 1,387 historical / 147 military_modern
      — historical signal dominates. Per per-source-coverage.md §6 footnote:
      Mode-C over-catching via real-Indian-military "Agni" missile namesake
      pattern; Discipline #25 spot-check filters. Weight 0.7.

  - cultural_lineage_canonical: "southeast_asian"
    fate_genre_weight: 0.5
    tier: 1
    excluded_from_tier_s: false
    reasoning: |
      Khmer / Thai / Burmese / Vietnamese / Indonesian / Malay weapon traditions
      (kris, parang, dha, golok, mandau, kampilan). Moderate substrate at 872
      rows / 1.2%. Lower Fate-genre precedent than south_asian or east_asian
      (Fate has Yan Qing / Souther but limited Southeast Asian Servant pool)
      but broadly-fictionalizable through Indianized polity influence and
      maritime trade syncretism. Not flagged in Sketch D § 4.3 as Tier 2 boost
      candidate explicitly but substrate-thin and Fate-genre-eligible. Weight
      0.5 reflects moderate story/feel value.

  # ---------- Unlabeled / passthrough (weight 0.4) ----------

  - cultural_lineage_canonical: "unknown"
    fate_genre_weight: 0.4
    tier: 1
    excluded_from_tier_s: false
    reasoning: |
      Unlabeled lineage. 21,242 rows / 23.6% substrate. Per empirical inspection:
      19,119 of these have register='unknown' (i.e., totally unlabeled at both
      register AND lineage layers — primarily fantasy/RPG-data-dump sources
      lacking metadata); 2,109 historical / 14 military_modern. Most are TTRPG
      data-dump rows where lineage couldn't be confidently assigned. Cannot
      Tier-3-exclude these as a class (they ARE eligible for Tier S via top-1%
      composite path; only the named-mythological-match path requires lineage-
      tier gating). Weight 0.4 reflects "composite-score-driven; let other
      signals sort." Tier 1 by default (no cultural-sensitivity violation
      possible with unknown lineage).

  # ---------- TIER 3 EXCLUDED — cultural-sensitivity per Sketch F § 6.3 (weight 0.0) ----------

  - cultural_lineage_canonical: "north_american_indigenous"
    fate_genre_weight: 0.0
    tier: 3
    excluded_from_tier_s: true
    reasoning: |
      EXCLUDED per Sketch F § 6.3 cultural-sensitivity stratification + Q-B
      verdict § 3.2 + n-am-indigenous-no-cluster-disposition record. 32 rows
      / 0.04% substrate — substrate-thin with ~0-1 of 29 pool cultural items
      (clean-control case per marginal-lineage-tagging-pattern record).
      v1.1+ deferred per 02-roadmap § 3.8. excluded_from_tier_s blocks named-
      mythological-match auto-include path.

  - cultural_lineage_canonical: "arctic_circumpolar"
    fate_genre_weight: 0.0
    tier: 3
    excluded_from_tier_s: true
    reasoning: |
      EXCLUDED per Sketch F § 6.3 (Inuit / Arctic Circumpolar — Sámi / Yupik /
      Aleut / Chukchi traditions). 56 rows / 0.06% substrate. Per arctic-
      circumpolar-marginal-lineage-disposition record: ~0 cultural items in
      88.2%-pure Cluster 24 (cleanest Mode-B positive control — Russian 2S1
      Gvozdika SPH, Swedish RBS-70 MANPADS, French Mistral 3). Empirical
      register split: 30 military_modern / 21 historical / 5 fantasy — Mode-B
      dominant. EXCLUDED from Tier S; v1.1+ deferred.

  - cultural_lineage_canonical: "oceanic"
    fate_genre_weight: 0.0
    tier: 3
    excluded_from_tier_s: true
    reasoning: |
      EXCLUDED per Sketch F § 6.3 (Pacific Islander / Polynesian / Māori /
      Aboriginal Australian). 41 rows / 0.05% substrate. Per oceanic-marginal-
      lineage-disposition record: compounding failure (coverage gap + Mode-B
      tagging artifact + lineage-vocabulary over-collapse covering 4-5 distinct
      cultural families). Empirical register split: 22 military_modern / 19
      historical — Mode-B dominant. EXCLUDED from Tier S; v1.1+ deferred.

  - cultural_lineage_canonical: "mesoamerican"
    fate_genre_weight: 0.0
    tier: 3
    excluded_from_tier_s: true
    reasoning: |
      EXCLUDED per Sketch F § 6.3 cultural-sensitivity (Aztec / Maya / Olmec
      / Mixtec / Zapotec). 97 rows / 0.1% substrate. Per mesoamerican-marginal-
      lineage-disposition record: ~12-15 cultural Pre-Columbian items
      (macuahuitl, Hummingbird Bloodletter, Macehead) scattered across 5
      clusters; lineage tag dominated by modern Mexican arms (Mendoza, Cabañas,
      Zaragoza). Empirical: 89 historical / 8 military_modern. NOTE: Sketch D
      § 4.1 allocates ~4% v1 form-share for Moctezuma-summoning-Quetzalcoatl
      named-mythological pattern per Matt's vision — this is Tier 2 person +
      Tier 1 nested mythological, allocated via gandalf seed list match path
      (cultural_lineage tag agnostic). Tier 3 exclusion at THIS substrate-
      lineage-tag layer is correct; named-mythological-match against gandalf
      seed list operates on canonical_name match + alias matching, not on
      cultural_lineage tag.

  - cultural_lineage_canonical: "south_american_indigenous"
    fate_genre_weight: 0.0
    tier: 3
    excluded_from_tier_s: true
    reasoning: |
      EXCLUDED per Sketch F § 6.3 cultural-sensitivity (Andean / Mapuche /
      Quechua / Guaraní / Amazonian). 216 rows / 0.24% substrate. Per south-
      american-indigenous-marginal-lineage-disposition record: ~2 of 290 pool
      cultural items (Tumi only); 94.4%-pure Cluster 87 dominated by modern
      Argentine/Brazilian/Chilean military firearms (Mode-B starkest case).
      Empirical: 191 historical / 25 military_modern (note: historical tag
      includes 19th-20th-century Latin American military arms, NOT only Pre-
      Columbian). EXCLUDED from Tier S; v1.1+ deferred.

  - cultural_lineage_canonical: "african"
    fate_genre_weight: 0.0
    tier: 3
    excluded_from_tier_s: true
    reasoning: |
      EXCLUDED per Sketch F § 6.3 cultural-sensitivity (Sub-Saharan African
      cultural traditions — Yoruba, Zulu, Maasai, Ashanti, Bantu families).
      563 rows / 0.63% substrate. Empirical register split: 510 historical /
      53 military_modern — better Mode-A signal than the 5 indigenous-rare
      lineages (less acute Mode-B contamination) BUT cultural-sensitivity
      stratification per Sketch F § 6.3 holds: sub-Saharan African traditions
      are explicitly Tier-3-excluded for v1 LLM-naming pool. North African
      content (Egyptian) sits under middle_eastern lineage tag, not african
      — so excluding african at Tier 3 does NOT exclude Egyptian. v1.1+
      deferred per 02-roadmap § 3.8.

# ---------- distribution summary ----------
distribution_summary:
  total_lineages_present: 14
  tier_1_count: 8
  tier_1_row_total: 88836
  tier_1_row_pct: 98.9
  tier_3_excluded_count: 6
  tier_3_excluded_row_total: 1005
  tier_3_excluded_row_pct: 1.1
  weight_1_0_lineages: 3
  weight_0_7_lineages: 3
  weight_0_5_lineages: 1
  weight_0_4_lineages: 1
  weight_0_0_lineages: 6
  total_rows: 89841
  # Empirical sanity: 98.9% of substrate is Tier 1 (broadly-fictionalized + cross_cultural +
  # Tier 2 boost candidates + unknown passthrough); 1.1% is Tier 3 excluded indigenous /
  # sub-Saharan-African lineages. The unknown passthrough subset (21,242 rows / 23.6%) carries
  # the Fate-genre uncertainty surface — composite score's other signals (description richness,
  # source reputation, etc.) do the sorting for unknown-lineage rows.
```

---

## 2. Discipline notes

### 2.1 Why Tier 3 exclusion is weight=0.0 AND `excluded_from_tier_s: true`

These are independent enforcement gates:
- `fate_genre_weight: 0.0` zeros the Stage 2.5 cultural-tradition signal contribution to composite score
- `excluded_from_tier_s: true` blocks the named-mythological-match path to Tier S auto-include even if a Tier 3 row would otherwise match a seed-list entry

Together they ensure Tier 3 rows cannot reach Tier S via EITHER (a) high composite score driven by cultural-tradition signal OR (b) named-mythological-match auto-include. A Tier 3 row CAN still reach Tier S via top-1% composite score driven by OTHER signals (museum-curated + provenance-rich + image-present + cluster-central), which is correct — quality-of-row is independent of cultural-sensitivity-of-tag at the composite layer. The cultural-sensitivity gate at v1_scope inclusion is a Stage 3 design-call decision, not a Stage 2.5 scoring decision.

### 2.2 Why fantasy_generic is weight 1.0 and Tier 1 (not Tier 2 boost)

fantasy_generic at 24.8% substrate is OVER-represented relative to Sketch D § 4.3 target (~15-18%). The composite signal weight at 0.05 is small; the larger sourcing-discipline lives at Stage 3 composition policy (Sketch D § 4.3 calls for TRIM of fantasy_generic). Stage 2.5 honestly reflects "this lineage has Fate-genre story/feel value" with weight 1.0; Stage 3 honestly reflects "we still want less than 25% of v1_scope to be fantasy_generic" via composition policy. Don't conflate scoring with composition.

### 2.3 Why mesoamerican is Tier 3 excluded but Sketch D § 4.1 still allocates ~4% v1 form-share

Sketch D § 4.1 mesoamerican allocation is for the Moctezuma-Quetzalcoatl Tier 2 person + Tier 1 nested mythological pattern per Matt's vision (canonical/story/v1-bc-target-intent-2026-05-24.md § 6.1). This is gandalf seed-list-driven, operating on canonical_name match + alias matching at Phase 5 cohesion-coalescence layer — NOT on `cultural_lineage_canonical` tag matching at Stage 2.5 scoring layer.

The Tier 3 exclusion at this lookup correctly prevents the auto-include path firing for mesoamerican-tagged substrate rows (which empirically are 89 modern-Mexican-military + 8-15 cultural Pre-Columbian, dominantly Mode-B contamination). A Quetzalcoatl-anchored form generated at Phase 5 reaches its substrate weapons via a DIFFERENT path — Stage 3 composition policy targeted-sample within mesoamerican Mode-A subset OR substrate-enrichment crawl per Sketch D § 4.3.

### 2.4 Discipline #25 semantic-layer rep-audit applied

This lookup's Tier 3 exclusion list is THE direct empirical application of Discipline #25 at the cultural-tradition curation layer. The marginal-lineage-tagging-pattern record's substrate evidence (4 of 5 indigenous lineages show Mode-B contamination; cleanest control in arctic_circumpolar with 88.2%-pure cluster of Russian/Swedish/French missile systems) is exactly what would corrupt a naive "weight by lineage richness" approach — substrate richness in these lineages is RICHNESS-OF-CONTAMINATION, not richness-of-cultural-tradition. Weight 0.0 is the correct response.

### 2.5 Rep-audit flag returned to knight-rider

Two rep-audit concerns surfaced during this curation:
1. **`african` lineage** — empirical register split (510 historical / 53 military_modern) shows BETTER Mode-A signal than the 5 indigenous-rare lineages, but Sketch F § 6.3 Tier 3 exclusion holds for sub-Saharan African cultural sensitivity. This is the closest call in the lookup; flagging in case Stage 3 design call revisits the Tier 1/2/3 boundary for african. **Recommendation: keep Tier 3 exclusion for v1; revisit at v1.1+ per 02-roadmap § 3.8.**
2. **`unknown` lineage** — 19,119 of 21,242 unknown-lineage rows have register='unknown' (totally unlabeled metadata); these are predominantly TTRPG data-dump rows. Weight 0.4 lets composite score's other signals sort, which is correct, but a TTRPG-data-dump row labeled unknown/unknown is structurally low-quality on most other signals too — so unknown-lineage rows will tend toward Tier C anyway. No design intervention needed; flagging for empirical-distribution awareness at the 100-row spot-check.

---

## 3. Cross-references

- Consumer dispatch: `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-2-5-quality-tier-scoring.md`
- Sketch D + F source: `canonical/story/v1-bc-target-intent-2026-05-24.md` § 4 + § 6
- Rep-audit empirical evidence: `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`
- Tier 3 individual records: `canonical/story/{n-am-indigenous,south-american-indigenous,arctic-circumpolar,oceanic,mesoamerican}-marginal-lineage-disposition-2026-05-23.md`
- Discipline #25 reference: `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- Companion lookup: `agentic_orchestration/gandalf/notes/2026-05-24-source-library-reputation-tier.md`

---

## 4. Sign-off

**Author:** gandalf (story-and-design steward)
**For:** Cycle 10 Stage 2.5 quality-composite scoring input. All 14 cultural_lineage_canonical values present in substrate enumerated with fate_genre_weight (0.0-1.0) + tier (1/2/3) + excluded_from_tier_s flag + reasoning. Tier 3 exclusions (6 lineages — north_american_indigenous, arctic_circumpolar, oceanic, mesoamerican, south_american_indigenous, african) enforce Sketch F § 6.3 cultural-sensitivity stratification AND Discipline #25 semantic-layer rep-audit against empirically-confirmed Mode-B contamination. Two rep-audit edge-case concerns surfaced to knight-rider (african boundary close-call; unknown high-volume passthrough).
