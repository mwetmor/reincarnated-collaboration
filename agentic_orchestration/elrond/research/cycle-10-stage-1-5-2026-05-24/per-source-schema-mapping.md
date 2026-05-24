# Per-Source Schema Mapping — Cycle 10 Stage 1.5 Structured-Field Extraction

**Author:** elrond (data steward)
**Date:** 2026-05-24
**Dispatch:** `agentic_orchestration/dispatches/2026-05-23-elrond-cycle-10-stage-1-5-per-source-structured-field-extractor.md`
**DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
**Output columns:**
- `extracted_length_value` REAL + `extracted_length_unit` TEXT
- `extracted_weight_value` REAL + `extracted_weight_unit` TEXT
- `extracted_materials` TEXT (comma-separated, free-text preserved)
- `extracted_named_bearer` TEXT (source phrasing preserved per Discipline #11)
- `extracted_provenance_richness` REAL [0.0, 1.0]
- `extracted_historical_use` TEXT (NULL where absent)

---

## §1 Per-source field map (8 rich sources + 3 thin sources mapped)

| Source | Row count | Length signal | Weight signal | Materials signal | Bearer signal (primary) | Bearer signal (secondary) | Provenance fields | Historical-use signal |
|---|---|---|---|---|---|---|---|---|
| **met-museum** | 7,559 | `dimensions` ("L. 21 in. (54.5cm)") | `dimensions` ("Wt. 6 lb. 1 oz. (2750 g)") | `medium` ("Steel, wood, lacquer, gold...") | **`canonical_name` ("Halberd of Archduke Ferdinand II")** | `description_text` | `culture`, `country`, `region`, `objectDate`, `creditLine`, `accessionNumber` | `objectDate` + `creditLine` prose |
| **royal_armouries** | 38,127 | absent (most rows) | absent (most rows) | absent | `description_text` ("Smith and Wesson - 1870") | `canonical_name` ("Made for X") | `place`, `date`, `location_in_museum`, `accession_number` | `description_text` prose |
| **wikipedia** | 8,579 | `length` ("Fixed wooden stock:...") | `weight` ("Without magazine...") | absent (semi-structured prose) | `used_by`, `wars` | `description_text` + `cultural_lineage_tags` | `origin`, `manufacturer`, `used_by`, `wars` | `wars` field; `description_text` prose |
| **wikidata** | 12,371 | absent typically | absent typically | `material` ("leather", "bronze") | `description_text` (sparse) | `cultural_lineage_tags` | `country`, `inception`, `weapon_type` | absent typically |
| **odin-army-tradoc** | 3,998 | `Dimensions.Length` | `Dimensions.Weight` / `Dimensions.Maximum Takeoff Weight` | absent | `System.Manufacturer` (org, not person) | `description_text` (modern military operators) | `System.Manufacturer`, `System.Caliber`, `System.Type` | `Variants` field; modern-military operators in description |
| **osrsbox-db** | 940 | absent | `weight` (game grams) | absent | `description_text` (game lore) | `canonical_name` (named items like "Excalibur") | `members`, `tradeable`, `release_date` | game-lore prose |
| **wow-classic-items** | 4,440 | absent | absent | absent | `description_text` (rare) | `canonical_name` (named items) | `quality`, `requiredLevel`, `class`, `subclass` | absent |
| **cataclysm-dda** | 1,599 | absent | `weight` ("573 mg") | `material` (JSON array; e.g., `["battery"]`) | absent | `canonical_name` | `subtypes`, `flags`, `price` | absent |
| **fextralife-\* (5 sources)** | 966 combined | absent (per-row composite) | `Wgt` column in table-row composite (Elden Ring) | absent | `canonical_name` (named bosses/NPCs) | `description_text` | `extraction_method` mostly table-derived | boss/NPC lore in description |
| **bsdata-warhammer-aos** | 2,185 | absent | absent | absent | `canonical_name` (unit names; not personal bearers) | `description_text` | wargaming unit metadata | absent |
| **nick-aschenbach-dnd-data**, **path-of-exile-repoe**, **diablo2-d2data**, **elden-ring-erdb**, **bloqhead-demigods**, **5e-bits-5e-database**, **gta-v-data**, **army-recognition**, **pf2ools-quarantined**, **souls-api-quarantined** | thin tails | varies | varies | varies | `description_text` / `canonical_name` only | — | thin | thin |

---

## §2 Extraction strategy summary

### §2.1 Length/weight — regex pipeline

Per-source pipeline:

1. **Met Museum:** parse `dimensions` field with regex `\bL\.?\s*[\d.\s/]+(?:in|cm|mm|m)\b` for length and `\bWt\.?\s*[\d.\s/lboz]+(?:g|kg)\b` for weight (preferring the metric form in parens when present).
2. **Wikipedia:** parse `length` and `weight` keys (strip HTML/wiki-cruft `<br />`, `<ref ...>`, etc.; extract first plausible numeric+unit pair). Coverage limited (~39% length-keyed) per pre-execution count.
3. **Odin Army Tradoc:** parse nested `properties.Dimensions.Length` and `properties.Dimensions.Maximum Takeoff Weight` (and similar variants); units in the value string.
4. **OSRSbox:** `weight` is direct numeric in game-grams; treat unit as `"g_game"` (label-not-real-world).
5. **Cataclysm DDA:** `weight` is "573 mg" / "1.2 kg" style; parse value + unit.
6. **Fextralife-* (Elden Ring + DS family):** weight extraction skipped — table-blob format encodes per-item weight in a single composite cell which Phase D's per-row mapping does not isolate. NULL with provenance note.
7. **All others:** NULL.

Output units normalized to `cm` (length) or `g` (weight) where conversion is unambiguous; original-unit preserved as `extracted_length_unit` / `extracted_weight_unit` for downstream visibility.

### §2.2 Materials

- **Met Museum** `medium` → comma-separated string preserved verbatim (e.g., "Steel, wood, lacquer, gold, silver, copper-silver alloy (shibuichi)")
- **Wikidata** `material` → as-is (single material name typically)
- **Cataclysm DDA** `material` → JSON array → comma-separated
- **All others** → NULL

### §2.3 Named bearer (gandalf seed list dependency — half b)

**Multi-pass:**

1. **Pass A — explicit name patterns in `canonical_name`** (Met Museum primary): regex `\b(of|for|Made for|attributed to|belonging to|carried by|owned by|presented to) ([A-Z][\w\-À-ſ]+(?:\s+[A-Z][\w\-À-ſ]+){0,5})` with stopword filter for common non-person tokens ("the", "a", "of", "Pair", "Set", "Part").

2. **Pass B — seed-list match** against canonical_name + description_text + cultural_lineage_tags. Seed list parsed from `agentic_orchestration/gandalf/notes/2026-05-24-named-historical-figure-seed-list.md` per Discipline #19 filesystem-existence poll. Match strategy: substring + word-boundary; require capitalized form to avoid common-word false-match.

3. **Pass C — Sketch F 12 named anchors special handling**: the 12 anchor candidates (Arthur / Roland / Hattori Hanzō / Lu Bu / Thor / Achilles / Cú Chulainn / Moctezuma / Quetzalcoatl / Cleopatra / Karna / Baba Yaga / Gilgamesh) get explicit regex passes with tradition-coherence rep-audit per Discipline #25 (Mode B/C/D filter: e.g., "Excalibur" must trace to an Arthurian-tradition row not an "M982 Excalibur" artillery shell).

**Source phrasing preserved verbatim** in `extracted_named_bearer` (Discipline #11). Downstream canonical-form curation is out-of-scope here.

### §2.4 Provenance richness (composite metric)

Per-row 0.0-1.0 score based on density of attribution-relevant fields:

| Source | Provenance signal fields | Max-score conditions |
|---|---|---|
| met-museum | `culture` + `country` + `period` + `objectDate` + `creditLine` + `accessionNumber` | All 6 populated → 1.0 |
| royal_armouries | `place` + `date` + `accession_number` + `location_in_museum` | All 4 → 1.0 |
| wikipedia | `origin` + `manufacturer` + `used_by` + `wars` | All 4 → 1.0 (real-world weapons); pure-mythological gets 0.3-0.5 based on `cultural_lineage_tags` density |
| odin-army-tradoc | `System.Manufacturer` + `System.Type` + `System.Caliber` | All 3 → 1.0 |
| wikidata | `country` + `inception` + `material` | All 3 → 1.0 |
| osrsbox / wow / cataclysm / fextralife / etc. | structured-game-data; default low (0.1-0.3) | 0.3 max — not historically-provenant |

### §2.5 Historical use

- **Met Museum:** `objectDate` + `creditLine` concatenated (e.g., "dated 1598; John Stoneacre Ellis Collection, Gift of Mrs. Ellis...")
- **Wikipedia:** `wars` field verbatim (e.g., "Vietnam War, Iran-Iraq War, Gulf War")
- **Odin Army Tradoc:** `Variants.*` field (when present; indicates lineage of upgrades / historical-use)
- **All others:** NULL

---

## §3 Per-source coverage projection (pre-execution)

| Source | length% | weight% | materials% | bearer% | provenance% | historical_use% | Notes |
|---|---|---|---|---|---|---|---|
| met-museum | ~75% | ~76% | ~95% | ~13% (999/7559) + seed-list contributions | ~80% (multi-field) | ~70% | GOLD source for all axes |
| royal_armouries | ~5% | ~5% | ~0% | ~5% (description-driven) | ~60% (place+date+accession) | ~10% | Provenance OK; structured fields thin |
| wikipedia | ~39% (3396/8579) | ~39% | ~0% | ~55% (used_by 4791) + seed-list contributions | ~50% | ~30% (wars-keyed) | Mixed real-world + mythological |
| wikidata | ~0% | ~0% | ~25% | ~5% (sparse description) | ~40% (country+inception) | ~0% | Substrate-thin; structured-thin |
| odin-army-tradoc | ~70% | ~70% | ~0% | ~0% (org-only) | ~80% | ~30% | Modern-military; no person-bearers |
| osrsbox-db | ~0% | ~80% | ~0% | ~3% (Excalibur etc.) | ~20% | ~20% | Game data |
| wow-classic-items | ~0% | ~0% | ~0% | ~2% | ~5% | ~0% | Item-thin |
| cataclysm-dda | ~0% | ~60% | ~30% | ~0% | ~10% | ~0% | Post-apocalyptic; thin |
| fextralife-* | ~0% | ~0% | ~0% | ~10% (boss-name attrib) | ~5% | ~10% | Composite-blob format limits per-item extraction |

**Aggregate populated row count projection:**
- Length: ~8K rows (Met 5.7K + Wikipedia 3.3K + Odin 2.8K, less overlap)
- Weight: ~10K rows
- Materials: ~10K rows (Met 7.5K + Wikidata 3K + Cataclysm 0.5K)
- Provenance: ~50K rows have NON-zero score (most sources contribute >0.05)
- Named bearer: TARGET ≥500 (1.5K-3K projected if seed list covers Sketch F 12 anchors + ~500 historical persons spanning broadly-fictionalized traditions)

---

## §4 Cross-references

- Dispatch: `agentic_orchestration/dispatches/2026-05-23-elrond-cycle-10-stage-1-5-per-source-structured-field-extractor.md`
- Stage 0 output: `canonical/story/v1-bc-target-intent-2026-05-24.md` §§ 4 + 6
- Rep-audit pattern: `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`
- Phase D schema lineage: `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/MIGRATION.md`
- Stage 1 parallel (`proxy_*` columns; no collision): `agentic_orchestration/dispatches/2026-05-23-elrond-cycle-10-stage-1-cheap-proxy-mechanical-fingerprint.md`
