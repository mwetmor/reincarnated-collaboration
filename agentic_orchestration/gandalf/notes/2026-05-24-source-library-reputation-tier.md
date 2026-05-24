# Source-Library Reputation Tier Lookup — Cycle 10 Stage 2.5 Input

**Date:** 2026-05-24
**Author:** gandalf (story-and-design steward)
**Consumer:** elrond Stage 2.5 quality-composite scoring script (signal weight 0.20 per dispatch § 2)
**Substrate:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` (89,841 rows; 25 distinct source_library values; enumerated 2026-05-24)
**Companion docs:**
- `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-2-5-quality-tier-scoring.md` (consumer dispatch)
- `agentic_orchestration/elrond/research/cycle-10-stage-1-5-2026-05-24/per-source-coverage.md` (empirical per-source variance — informs tier-assignment with structurally-honest data)
- `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` (Discipline #25 semantic-layer rep-audit; especially relevant for Mode-C contamination in odin-army-tradoc)

---

## 0. TL;DR

25 source_library values present in `weapon_knowledge_entries`. Distribution: **Tier A (museum-curated, score 1.0): 2 sources, 45,686 rows (50.9%)**; **Tier B (designer-curated commercial/editorial, score 0.7): 5 sources, 7,018 rows (7.8%)**; **Tier C (community-scraped, score 0.4): 3 sources, 21,012 rows (23.4%)**; **Tier D (game-data-dump, score 0.2): 15 sources, 16,125 rows (17.9%)**.

Two empirical-data refinements over Stage 1.5 verdict:
- **Royal Armouries kept at Tier A despite Stage 1.5 "structured-thin, prov_avg=0.947"** — institutional museum curation + provenance-rich qualifies for Tier A baseline. Description-richness signal (Stage 1.5 signal 2) carries the structured-thinness penalty separately; reputation-tier should not double-discount.
- **odin-army-tradoc kept at Tier B but flagged for downstream** — operational/manufacturer documentation has editorial pipeline (Tier B equivalent for military-modern) but per Stage 1.5 §1 footnote² carries Mode-C naming-allusion contamination at 1.5% bearer-match rate. Discipline #25 routes this contamination at consumption (cultural-lineage gate); reputation tier remains B.

**Tier 3 cultural-sensitivity gating is NOT enforced at this lookup** — that lives in the cultural-tradition weight lookup (companion file). This lookup answers ONLY "how much do I trust the source's editorial pipeline."

---

## 1. Lookup table (load-bearing — structured-data block parseable by Stage 2.5 scoring script)

```yaml
# source_library_reputation_tier.yaml
# Each entry: source_library → reputation_tier (A/B/C/D) → numeric_score (1.0/0.7/0.4/0.2)
# Consumer: elrond Stage 2.5 score_quality_composite.py
# Signal weight in composite: 0.20 (per dispatch § 2)

sources:

  # ---------- TIER A — museum-curated (numeric_score: 1.0) ----------

  - source_library: "met-museum"
    reputation_tier: "A"
    numeric_score: 1.0
    reasoning: |
      Metropolitan Museum of Art curatorial catalogue. Institutional scholarly
      provenance, named-bearer attribution (43.6% canonical_name length-rich;
      70.6% weight populated; 98.9% materials populated per Stage 1.5).
      Confirmed GOLD standard.

  - source_library: "royal_armouries"
    reputation_tier: "A"
    numeric_score: 1.0
    reasoning: |
      Royal Armouries Museum (Leeds / Tower of London). Institutional curation
      with prov_avg=0.947 (highest of any source). Structured-fields thin
      (length/weight/materials all 0.0% populated) but provenance-rich;
      description-richness signal handles structural-thinness penalty
      separately. Reputation tier is editorial-pipeline trust, not field
      density — Tier A holds.

  # ---------- TIER B — designer-curated commercial / editorial (numeric_score: 0.7) ----------

  - source_library: "odin-army-tradoc"
    reputation_tier: "B"
    numeric_score: 0.7
    reasoning: |
      ODIN (Operational Environment Data Integration Network) — U.S. Army TRADOC
      operational/manufacturer documentation. Editorial pipeline equivalent
      for military-modern register. 48.0% length-rich; 49.8% historical_use
      populated. NOTE per Stage 1.5 §1 footnote²: Mode-C naming-allusion
      contamination flagged in 1.5% of bearer-extracted rows (Russian "Sadko
      Truck"; Ukrainian "Baba Yagas UAV"); Discipline #25 handles at
      consumption time. Tier B remains correct for editorial trust.

  - source_library: "5e-bits-5e-database-2024"
    reputation_tier: "B"
    numeric_score: 0.7
    reasoning: |
      D&D 5e 2024-edition official rules subset; commercial TTRPG with editorial
      pipeline (Wizards of the Coast official mechanics). Small (110 rows) but
      authoritative within genre.

  - source_library: "5e-bits-5e-database"
    reputation_tier: "B"
    numeric_score: 0.7
    reasoning: |
      D&D 5e pre-2024-edition official rules subset; commercial TTRPG editorial
      pipeline. 37 rows.

  - source_library: "pf2ools-pf2ools-data-quarantined"
    reputation_tier: "B"
    numeric_score: 0.7
    reasoning: |
      Pathfinder 2e community-tools data (pf2ools). Paizo PF2e has editorial
      pipeline at source; community tool wraps it. Quarantined flag in source
      name suggests Phase D quarantine treatment — preserve at B for editorial
      pedigree; composite score's other signals (provenance richness) will
      down-weight low-content rows. 688 rows.

  - source_library: "bsdata-warhammer-aos"
    reputation_tier: "B"
    numeric_score: 0.7
    reasoning: |
      BSData Warhammer Age of Sigmar tournament army-list data. Games Workshop
      IP with strong editorial pipeline at source; community-maintained
      datafile wrapper. 2,185 rows. Notable Fate-genre adjacency (Warhammer
      AoS is a Fate-aesthetic-neighbor for fantasy-generic content).

  # ---------- TIER C — community-scraped (numeric_score: 0.4) ----------

  - source_library: "wikipedia"
    reputation_tier: "C"
    numeric_score: 0.4
    reasoning: |
      English Wikipedia article scrape. Community-edited with variable rigor;
      historical_use coverage at 69.3% (highest non-museum); 14.7% length-rich
      (good). Community-scraped tier reflects editorial-pipeline variance, not
      content quality per row — the composite's description-richness and
      provenance-richness signals identify high-quality individual Wikipedia
      rows from low-quality.

  - source_library: "wikidata"
    reputation_tier: "C"
    numeric_score: 0.4
    reasoning: |
      Wikidata structured-data scrape. Community-contributed with bot-assisted
      curation; 6.8% materials populated (best of community sources). Lower
      narrative content than Wikipedia (0% length-rich, 0% historical_use)
      offset by structured-data density. Tier C consistent with Wikipedia.

  - source_library: "army-recognition"
    reputation_tier: "C"
    numeric_score: 0.4
    reasoning: |
      Army-Recognition.com weapon-specification scrape. Community/journalistic
      site for military-modern register. 62 rows; modern-military focus.
      Tier C reflects journalistic-source pedigree (not museum, not commercial
      editorial pipeline).

  # ---------- TIER D — game-data-dump (numeric_score: 0.2) ----------

  - source_library: "nick-aschenbach-dnd-data"
    reputation_tier: "D"
    numeric_score: 0.2
    reasoning: |
      Community-aggregated D&D weapon-name dump. Names like "Abominable Club",
      "Abyssal Bane Battleaxe" — RPG fantasy-name conventions; no editorial
      pipeline beyond list-maintenance. fantasy_generic lineage dominant.
      6,297 rows. Useful for fantasy_generic Pan-Fantasy bucket sourcing
      (Sketch D ~20% allocation).

  - source_library: "wow-classic-items"
    reputation_tier: "D"
    numeric_score: 0.2
    reasoning: |
      World of Warcraft Classic item-database extract. Game-data-dump; no
      editorial pipeline for our purposes (Blizzard editorial is internal,
      not surfaced as catalog metadata). 4,440 rows. fantasy_generic Pan-
      Fantasy bucket source.

  - source_library: "cataclysm-dda"
    reputation_tier: "D"
    numeric_score: 0.2
    reasoning: |
      Cataclysm: Dark Days Ahead game-data extract. Open-source game with
      community maintainers; weight/materials populated (60.6% / 58.6% per
      Stage 1.5) but minimal narrative editorial. Tier D for our naming-
      attribution purposes; structured-fields signal pulls these rows up
      separately in composite.

  - source_library: "osrsbox-db"
    reputation_tier: "D"
    numeric_score: 0.2
    reasoning: |
      Old School RuneScape item database extract. Game-data-dump; 98.9% weight
      populated. Editorial pipeline at Jagex is internal. 940 rows.

  - source_library: "diablo2-d2data"
    reputation_tier: "D"
    numeric_score: 0.2
    reasoning: |
      Diablo II item-data extract. Game-data-dump. 521 rows. Notable genre-
      pedigree for ARPG-tradition reference (Diablo lineage is design-DNA
      for Reincarnated per author backstory) but no editorial metadata
      pipeline surfaced.

  - source_library: "path-of-exile-repoe"
    reputation_tier: "D"
    numeric_score: 0.2
    reasoning: |
      Path of Exile RePoE data extract. Game-data-dump; strong genre-pedigree
      (PoE is design reference for skill-system § 5-8) but raw data-dump
      treatment at metadata level. 494 rows.

  - source_library: "fextralife-elden-ring"
    reputation_tier: "D"
    numeric_score: 0.2
    reasoning: |
      Fextralife community wiki scrape for Elden Ring. Community-scraped
      fan-wiki; treat as game-data-dump tier (lower than Wikipedia community
      tier — fan-wiki editorial discipline is weaker). 375 rows.

  - source_library: "bloqhead-demigods"
    reputation_tier: "D"
    numeric_score: 0.2
    reasoning: |
      Demigods/Elden Ring extract (Academy Glintstone Staff, Antspur Rapier
      class of canonical_names — From Software fantasy-naming convention).
      Game-data-dump tier; fantasy_generic Pan-Fantasy bucket source.
      320 rows.

  - source_library: "elden-ring-erdb"
    reputation_tier: "D"
    numeric_score: 0.2
    reasoning: |
      Elden Ring Database (ERDB) extract. Game-data-dump. 307 rows.

  - source_library: "fextralife-ds2"
    reputation_tier: "D"
    numeric_score: 0.2
    reasoning: |
      Fextralife community wiki scrape for Dark Souls 2. Same tier as Elden
      Ring fextralife. 239 rows.

  - source_library: "fextralife-ds3"
    reputation_tier: "D"
    numeric_score: 0.2
    reasoning: |
      Fextralife community wiki scrape for Dark Souls 3. 219 rows.

  - source_library: "gta-v-data"
    reputation_tier: "D"
    numeric_score: 0.2
    reasoning: |
      GTA V weapon-data extract. Game-data-dump; modern-firearms register;
      183 rows. Pan-Fantasy applicability low; v1_scope inclusion unlikely
      but Tier D reflects metadata-pipeline state.

  - source_library: "fextralife-ds1"
    reputation_tier: "D"
    numeric_score: 0.2
    reasoning: |
      Fextralife community wiki scrape for Dark Souls 1. 133 rows.

  - source_library: "souls-api-thomaslincoln-quarantined"
    reputation_tier: "D"
    numeric_score: 0.2
    reasoning: |
      Quarantined Dark Souls API mirror. Phase D quarantine treatment.
      56 rows. Game-data-dump tier maintained.

  - source_library: "souls-api-thomaslincoln"
    reputation_tier: "D"
    numeric_score: 0.2
    reasoning: |
      Non-quarantined Dark Souls API mirror remnant. 2 rows. Game-data-dump.

# ---------- distribution summary ----------
distribution_summary:
  tier_A_count: 2
  tier_A_row_total: 45686
  tier_A_row_pct: 50.9
  tier_B_count: 5
  tier_B_row_total: 7018
  tier_B_row_pct: 7.8
  tier_C_count: 3
  tier_C_row_total: 21012
  tier_C_row_pct: 23.4
  tier_D_count: 15
  tier_D_row_total: 16125
  tier_D_row_pct: 17.9
  total_sources: 25
  total_rows: 89841
```

---

## 2. Discipline notes

### 2.1 Why Royal Armouries is Tier A despite structured-field thinness

Per Stage 1.5 §1 empirical table: Royal Armouries has length%=0.0, wt%=0.0, mat%=0.0 — appears "structured-thin" relative to Met Museum's 43.6%/70.6%/98.9%. BUT prov_avg=0.947 (highest of any source) reflects rich provenance metadata that Stage 1.5's structured-field extractor doesn't capture (provenance lives in description prose, not weight-fields).

Reputation tier is editorial-pipeline trust — Royal Armouries' editorial pipeline is institutional museum curation, identical category to Met Museum. The structured-field-thinness penalty applies separately via Stage 2.5's description-richness signal (weight 0.15) and extracted-provenance-richness signal (weight 0.10). Reputation tier should not double-discount.

### 2.2 Why odin-army-tradoc is Tier B not Tier C

ODIN is U.S. Army TRADOC operational documentation — government editorial pipeline with structured publishing standards. This is distinct from journalistic / community sources (Army-Recognition.com is at Tier C). The Mode-C naming-allusion contamination is a Discipline #25 consumption-time issue, not an editorial-pipeline issue — flagged here for downstream awareness, not used to demote tier.

### 2.3 Why Fextralife wikis are Tier D not Tier C

Wikipedia is community-edited with Wikimedia Foundation editorial standards (sourcing requirements, NPOV, etc.). Fextralife fan-wikis have lower editorial discipline — community-maintained game-companion content. Treating them as Tier D (game-data-dump-equivalent) reflects this. Their content quality varies; individual high-quality rows surface via composite's other signals.

### 2.4 TTRPG sources at Tier B

D&D 5e and PF2 official rule sources have commercial editorial pipelines (Wizards / Paizo). These are designer-curated. BSData Warhammer AoS sits in the same category (Games Workshop IP). The Pan-Fantasy bucket per Sketch D draws heavily from this tier for fantasy_generic forms — Tier B reflects this is acceptable Pan-Fantasy sourcing material.

### 2.5 Sketch D § 4.3 substrate-enrichment composability

This reputation-tier lookup is consumed in conjunction with the cultural-tradition weight lookup at composite-scoring time. A row from Met Museum (Tier A, score 1.0) carrying middle_eastern cultural_lineage_canonical (Tier 2 Fate-genre boost candidate per Sketch D § 4.3) gets BOTH signals — reputation × cultural-tradition multiply through their respective weights (0.20 × 1.0 + 0.05 × 0.7 for example). The two lookups are compositional, not redundant.

---

## 3. Cross-references

- Consumer dispatch: `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-2-5-quality-tier-scoring.md`
- Empirical input: `agentic_orchestration/elrond/research/cycle-10-stage-1-5-2026-05-24/per-source-coverage.md`
- Discipline reference: `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#11 preserve-source-phrasing; #25 semantic-layer rep-audit)
- Companion lookup: `agentic_orchestration/gandalf/notes/2026-05-24-cultural-tradition-weight-lookup.md`

---

## 4. Sign-off

**Author:** gandalf (story-and-design steward)
**For:** Cycle 10 Stage 2.5 quality-composite scoring input. All 25 source_library values present in substrate enumerated with reputation_tier + numeric_score + reasoning. Tier 1/2/3 cultural-sensitivity gating intentionally NOT enforced at this layer (lives in companion cultural-tradition weight lookup). Empirical row-coverage validates Tier A captures ~51% of substrate (Royal Armouries + Met Museum dominate), Tier B at ~8%, Tier C at ~23%, Tier D at ~18%. Row counts arithmetic-verified: 45,686 + 7,018 + 21,012 + 16,125 = 89,841.
