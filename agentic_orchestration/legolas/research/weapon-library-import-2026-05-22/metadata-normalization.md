# Metadata Normalization — Canonical Tag Schema + Per-Library Mapping
# Priority 2

**Date:** 2026-05-22
**Mode:** A (analytical synthesis)
**Commissioner:** gandalf, authorized by Matt 2026-05-22 evening
**Commission:** `agentic_orchestration/dispatches/2026-05-22-legolas-weapon-library-import-discovery.md`
**Build-on:** `library-enumeration.md` (this directory), `gear-substrate-rule-table-v1-2026-05-22.md`,
`canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md`

---

## Summary

Each surveyed library exposes a different native metadata surface. Sketchfab and Meshy expose
free-text tags + structural category/subcategory. Smithsonian exposes museum-grade structured
fields (culture, date, material, dimensions, provenance). OGA, BlendSwap, itch.io expose
minimal metadata with free-text description. TurboSquid/CGTrader expose commercial fields
(polygon count, format, PBR flag, price). The canonical schema proposed here unifies them
into three layers: (A) sim-property fields (range, geometry, tempo, charge, accuracy, rhythm
— drive substrate-vector matching), (B) aesthetic-tuple fields (tech_level × tone ×
cultural_lineage — drive cohesion-judge thematic identity), (C) source provenance fields
(library, asset_id, license, URLs — drive import pipeline compliance). The most critical
normalization challenge is tech_level and cultural_lineage: both require inference from
free-text tags for most sources, with only Smithsonian providing structured equivalents.

---

## 1. Canonical Tag Schema

### 1.1 Sim-property fields (mechanical; drive substrate-vector matching)

These fields determine whether a weapon is mechanically coherent with a given substrate-vector.
They are the primary query predicates for weapon selection at generation time.

| Field | Type | Values / Range | Source | Notes |
|---|---|---|---|---|
| `range_class` | ENUM | `melee` / `medium` / `ranged` / `indirect` | inferred from weapon type | Maps to range_profile axis (≤3 / 3–8 / ≥8 units); indirect = tome/summoner weapons |
| `geometry_class` | ENUM | `point` / `line` / `arc_sweep` / `scatter` / `area_aura` / `cone_aoe` / `beam` / `indirect` | inferred from weapon type | Per 9-type BDI geometry palette (canonical/09-geometry-palette-discussion.md) |
| `tempo_class` | ENUM | `fast` / `measured` / `slow` / `channeled` | inferred from weapon type | Timing axis: fast (daggers/chakram) / measured (wand/spear/bow) / slow (greatsword/staff/blunderbuss) / channeled (staff charge, orb cast) |
| `charge_class` | ENUM | `instant` / `short_charge` / `long_charge` / `channeled` | inferred from weapon type | Sub-dimension of tempo; relevant for orbs/staffs/censers |
| `accuracy_class` | ENUM | `precision` / `spread` / `area` | inferred from weapon type | Precision (wand/bow/dagger) / spread (blunderbuss) / area (orb/censer/horn) |
| `rhythm_class` | ENUM | `single_hit` / `multi_hit` / `burst` / `sustained` | inferred from weapon type | Single (greatsword/crossbow/blunderbuss) / multi (daggers/chakram) / burst (wand/orb) / sustained (channeled staff/censer) |
| `stat_affinity` | ENUM | `STR` / `INT` / `WIS` / `mixed` | inferred from weapon type + element family | Per element_biases.py:28 canonical; gear_rule_table informs defaults |

### 1.2 Aesthetic-tuple fields (thematic; drive cohesion-judge identity)

These fields determine aesthetic coherence with the generated class's identity.

| Field | Type | Values | Source | Notes |
|---|---|---|---|---|
| `tech_level` | ENUM | `primitive` / `ancient` / `medieval` / `early_modern` / `industrial` / `advanced` / `sci_fi` / `fantasy` | inferred from visual/tags | temporal-technology axis; not strictly historical — "fantasy" allows anachronistic tech |
| `tone` | ENUM | `heroic` / `grim` / `sacred` / `profane` / `arcane` / `brutal` / `elegant` / `utility` | inferred from tags/style | thematic mood; maps to BDI τ-field resonance clusters |
| `cultural_lineage` | ENUM | `european` / `east_asian` / `south_asian` / `middle_eastern` / `african` / `mesoamerican` / `native_american` / `oceanic` / `fictional` / `cross_cultural` / `unknown` | inferred or structured (Smithsonian) | primary cultural identity of the weapon design; "fictional" = wholly invented |
| `style_register` | ENUM | `realistic` / `stylized` / `low_poly` / `cartoon` / `hand_painted` / `photorealistic` / `voxel` | inferred from visual/tags/source | visual presentation style; affects cohesion-judge style-coherence assessment |

### 1.3 Mechanical type fields (weapon classification; drive gear catalogue matching)

| Field | Type | Values | Source | Notes |
|---|---|---|---|---|
| `weapon_class` | ENUM | `sword` / `dagger` / `polearm` / `bow` / `crossbow` / `firearm` / `thrown` / `staff` / `wand` / `orb` / `tome` / `hammer_mace` / `axe` / `shield` / `ritual_instrument` / `other` | inferred from weapon type | First-order classification; maps to BDI gear catalogue |
| `weapon_subclass` | TEXT | e.g., `greatsword`, `katana`, `longbow`, `flintlock_pistol`, `thurible` | inferred | Free-text sub-classification for fine-grained matching |
| `gear_catalogue_match` | INTEGER (FK) | 1–15 (maps to 15-gear catalogue IDs) | rule-derived | Which of the 15 canonical gear archetypes this weapon maps to; NULL if no clear match |

### 1.4 Source provenance fields (per-library import tracking)

| Field | Type | Values | Source | Notes |
|---|---|---|---|---|
| `source_library` | ENUM | `sketchfab` / `meshy` / `oga` / `smithsonian` / `turbosquid` / `cgtrader` / `free3d` / `blendswap` / `itchio` / `kenney` / `renderhub` / `fab` / `meshy_generated` / `other` | from import pipeline | The originating library |
| `source_asset_id` | TEXT | Library-native asset identifier | from library API/page | Unique ID within source library (Sketchfab UID, OGA nid, etc.) |
| `source_url` | TEXT | Full URL to asset page | from library | Canonical URL for attribution compliance |
| `preview_image_url` | TEXT | Thumbnail URL | from library | For UI display and visual matching |
| `download_url` | TEXT | Direct download URL | from library API | May be API-authenticated; stored separately from public URL |
| `license` | ENUM | `CC0` / `CC_BY` / `CC_BY_SA` / `CC_BY_NC` / `royalty_free_commercial` / `editorial_only` / `unknown` | from library | License as mapped from library-native terms |
| `license_url` | TEXT | URL to license text | from library | Attribution compliance link |
| `attribution_required` | BOOLEAN | true/false | from license | true for CC-BY and similar |
| `attribution_text` | TEXT | Required attribution string | from library | For CC-BY models |
| `cost_usd` | REAL | 0.0 = free | from library | Acquisition cost; 0 for free |
| `crawl_date` | TEXT | ISO 8601 date | from import pipeline | When this record was extracted |

### 1.5 Asset-readiness fields (import pipeline state)

| Field | Type | Values | Notes |
|---|---|---|---|
| `file_format` | ENUM | `FBX` / `GLB` / `GLTF` / `OBJ` / `BLEND` / `MAX` / `DAE` / `USD` / `other` | Format of source file; may differ from download format |
| `converted_format` | ENUM | `FBX` / `GLB` / `OBJ` / `none` | Format after pipeline conversion (target: GLB for runtime) |
| `readiness_state` | ENUM | `ready_to_import` / `needs_format_conversion` / `needs_scale_normalization` / `needs_texture_bake` / `needs_meshy_regenerate` / `sim_viability_unverified` / `rejected` | Import pipeline state machine |
| `poly_class` | ENUM | `low` / `mid` / `high` / `unknown` | Polygon density classification |
| `has_textures` | BOOLEAN | true/false | Whether textures are bundled with model |
| `has_rig` | BOOLEAN | true/false | Whether model is rigged (usually false for weapons) |
| `verified_for_sim` | BOOLEAN | true/false | Whether sim-viability has been confirmed by rocket |
| `scale_normalized` | BOOLEAN | true/false | Whether model has been normalized to canonical units |

### 1.6 Substrate-vector matching fields (query predicates; derived at import time)

These fields are computed / inferred at import time and stored for fast query. They translate
the mechanical and aesthetic fields into the substrate-vector space.

| Field | Type | Notes |
|---|---|---|
| `dominant_element_affinity` | TEXT (comma-sep enum) | Which elements this weapon pairs well with per BDI ω-table; e.g., "fire,water" for an orb |
| `omega_score_cache` | REAL | Precomputed ω-score for best element match (updated when ω-table is calibrated) |
| `range_profile_match` | ENUM | `melee` / `medium` / `ranged` — maps directly to substrate range_profile axis |

---

## 2. Per-Library Normalization Mapping

### 2.1 Sketchfab → Canonical

| Canonical field | Sketchfab native | Mapping | Lossiness |
|---|---|---|---|
| `weapon_class` | category = "weapons-military"; tags (free-text) | Parse tags: sword/dagger/bow/staff/wand/hammer/etc. | LOSSY — tag inconsistency; many models untagged by type |
| `weapon_subclass` | tags, model name | Parse model name + tags | LOSSY — free-text inference |
| `gear_catalogue_match` | none | Rule-derived from weapon_class + range_class + tempo_class | DERIVED |
| `range_class` | tags, model name | Inference from weapon_class | LOSSY |
| `geometry_class` | none | Inference from weapon_class | LOSSY |
| `tempo_class` | none | Inference from weapon_class | LOSSY |
| `tech_level` | tags: "medieval", "fantasy", "sci-fi", "modern", "historical" | Tag keyword match | MODERATE — common tags present but inconsistent |
| `tone` | tags: "dark", "heroic", "fantasy", "realistic", etc. | Tag keyword match | LOSSY |
| `cultural_lineage` | tags: "japanese", "samurai", "viking", "african", etc. | Tag keyword match | LOSSY — undertagged |
| `style_register` | tags: "low-poly", "cartoon", "realistic", "hand-painted"; thumbnail | Tag keyword match | MODERATE |
| `source_library` | — | Fixed: "sketchfab" | CLEAN |
| `source_asset_id` | model UID (API field: uid) | Direct copy | CLEAN |
| `source_url` | viewerUrl or "https://sketchfab.com/3d-models/{uid}" | Direct | CLEAN |
| `preview_image_url` | thumbnails.images[0].url | Direct | CLEAN |
| `license` | license.label (CC0/CC-BY/CC-BY-SA/etc.) | Map to enum | CLEAN — structured field |
| `attribution_required` | license.label != "CC0" | Derived | CLEAN |
| `crawl_date` | — | Set at crawl time | CLEAN |
| `file_format` | formats available | API returns available format list | CLEAN |

**Sketchfab gap summary:** Mechanical properties (geometry_class, tempo_class, charge_class,
accuracy_class, rhythm_class) cannot be structurally retrieved — they require inference from
weapon_class. Cultural_lineage and tech_level are free-text tags with inconsistent application.
An NLP/keyword-matching pass at import time fills these gaps probabilistically.

---

### 2.2 Meshy.ai → Canonical

| Canonical field | Meshy native | Mapping | Lossiness |
|---|---|---|---|
| `weapon_class` | subcategory (Swords & Blades / Firearms / Polearms / Bows & Ranged / etc.) | Map subcategory to weapon_class enum | MODERATE — subcategory is higher-level than weapon_class |
| `range_class` | subcategory | Derived: Swords=melee, Polearms=medium, Bows & Ranged=ranged, Firearms=ranged | MODERATE |
| `tech_level` | tags, model name | Keyword inference | LOSSY |
| `cultural_lineage` | tags (katana→east_asian; samurai→east_asian; etc.) | Keyword inference | LOSSY |
| `style_register` | implied by source context (community 3D models) | Inferred from thumbnail + tags | LOSSY |
| `source_library` | — | Fixed: "meshy" | CLEAN |
| `source_asset_id` | Meshy internal model ID | Extract from URL or API | CLEAN IF API accessible |
| `license` | — | Fixed: "CC0" (platform-wide; confirmed) | CLEAN |
| `file_format` | FBX/GLB/OBJ/STL/USDZ | API or download page | CLEAN |

**Meshy gap summary:** No structured era, culture, or tone fields. Subcategory taxonomy is the
strongest structural signal. Model names (often user-supplied, descriptive) are the best source
for weapon_subclass inference. Heavy inference load but CC0 cleanness compensates.

---

### 2.3 Smithsonian Open Access → Canonical

| Canonical field | Smithsonian native | Mapping | Lossiness |
|---|---|---|---|
| `weapon_class` | object_name, topic tags | Parse object_name for weapon type | MODERATE |
| `cultural_lineage` | culture field (structured) | Direct map to cultural_lineage enum | CLEAN — Smithsonian culture field is rich and structured |
| `tech_level` | date / date_range (structured) | Map to era: pre-500CE→ancient, 500–1500→medieval, 1500–1800→early_modern, 1800+→industrial | CLEAN for dated objects; LOSSY for undated |
| `tone` | none | Not available; default to "utility" for museum artifacts | LOSSY — no aesthetic tone in museum metadata |
| `style_register` | none structured; inferred from photogrammetry scan | Default: "realistic" (all Smithsonian models are photogrammetry scans) | CLEAN as default |
| `source_library` | — | Fixed: "smithsonian" | CLEAN |
| `source_asset_id` | id field in API response | Direct copy | CLEAN |
| `source_url` | record_link field | Direct | CLEAN |
| `license` | — | Fixed: "CC0" (all open access items) | CLEAN |
| `attribution_text` | credit_line field (structured) | Direct copy | CLEAN |
| `file_format` | — | Default: "OBJ" or "GLTF" per Smithsonian download spec | CLEAN |

**Smithsonian advantage summary:** cultural_lineage and era are the TWO MOST LOSSY fields for
all other sources, but CLEAN and structured in Smithsonian. The inverse gap: tone and
style_register, which other sources can approximate, are absent in museum metadata.
Smithsonian is uniquely valuable for cross-cultural authenticity but needs aesthetic
inference at import time.

---

### 2.4 Open Game Art → Canonical

| Canonical field | OGA native | Mapping | Lossiness |
|---|---|---|---|
| `weapon_class` | title + tags | Keyword parse | MODERATE — OGA has inconsistent tag discipline |
| `license` | license field (structured) | Map: CC0→CC0; CC-BY→CC_BY; GPL→reject; OGA-BY→CC_BY (OGA-BY terms compatible with commercial) | CLEAN — OGA enforces license selection |
| `file_format` | format field (structured per submission) | Direct map | CLEAN for most; LOSSY for multi-format submissions |
| `source_library` | — | Fixed: "oga" | CLEAN |
| `cultural_lineage` | tags | Keyword inference | LOSSY |
| `tech_level` | tags | Keyword inference | LOSSY |

**OGA gap summary:** License is the cleanest field (formally selected at upload); everything
else is free-text inference. GPL models must be filtered at import (reject condition).
OGA-BY is interpretable as CC-BY for game purposes (credit OGA in attribution).

---

### 2.5 itch.io → Canonical

| Canonical field | itch.io native | Mapping | Lossiness |
|---|---|---|---|
| `weapon_class` | pack name + description | Keyword inference | LOSSY — packs contain multiple weapon types |
| `license` | per-pack description | Extract from description text; confirm CC0 via "CC0 Public Domain" tag | LOSSY — many packs don't explicitly state license |
| `tech_level` | tags (medieval/sci-fi/fantasy/etc.) | Tag keyword match | MODERATE |
| `style_register` | tags (low-poly/voxel/PSX/cartoon/etc.) | Tag keyword match | MODERATE — itch.io has good style tags |
| `file_format` | pack description, screenshots | Parse description text | LOSSY |
| `source_library` | — | Fixed: "itchio" | CLEAN |

**itch.io gap summary:** Most metadata lives in free-text pack descriptions. Packs contain
multiple weapons of mixed types — individual weapon rows require unpacking after download.
Only import CC0-tagged packs (use itch.io CC0 filter) to avoid license ambiguity.

---

### 2.6 Kenney.nl → Canonical

| Canonical field | Kenney native | Mapping | Lossiness |
|---|---|---|---|
| `weapon_class` | filename (e.g., "sword_a.glb", "bow_b.obj") | Parse filename | CLEAN — Kenney uses consistent naming conventions |
| `license` | — | Fixed: "CC0" (platform-wide) | CLEAN |
| `tech_level` | pack theme (Medieval RTS → medieval; Blaster Kit → sci_fi) | Pack-level derivation | CLEAN at pack level; weapon-level is implicit |
| `cultural_lineage` | pack theme | Pack-level: Medieval RTS → european; Blaster Kit → fictional | CLEAN at pack level |
| `style_register` | — | Fixed: "low_poly" (Kenney house style) | CLEAN |
| `file_format` | pack contents (GLB, OBJ, FBX) | Direct | CLEAN |
| `source_library` | — | Fixed: "kenney" | CLEAN |

**Kenney advantage summary:** Best normalization mapping of any source for what it covers.
Pack-level metadata propagates cleanly to all weapons within the pack. Ideal for
import pipeline validation (Phase A schema testing set) due to normalization cleanliness.

---

### 2.7 TurboSquid / CGTrader → Canonical (for Tier 3 selective import)

| Canonical field | Commercial libraries | Mapping | Lossiness |
|---|---|---|---|
| `license` | TurboSquid: "Royalty-Free" perpetual; CGTrader: "Royalty-Free" | Map to: "royalty_free_commercial" | CLEAN |
| `file_format` | explicit per product listing | Direct | CLEAN |
| `poly_class` | polygon count field | Map: <5K=low, 5–50K=mid, >50K=high | CLEAN |
| `style_register` | tags: "low-poly", "PBR", "photorealistic" | Tag match | MODERATE |
| `weapon_class` | title + category tags | Keyword inference | MODERATE |
| `cultural_lineage`, `tech_level` | title + free-text tags | Keyword inference | LOSSY |
| `cost_usd` | price field | Direct | CLEAN |

---

## 3. Ontology Reference — Wikidata as Backbone

Wikidata's weapon Q-item tree (root Q728, subclass-of P279) provides the most complete
machine-readable weapon taxonomy. The `weapon_class` enum in the canonical schema maps
to Wikidata Q-items, enabling ontology queries for related types. Proposed mappings:

| Canonical weapon_class | Wikidata Q-item | Notes |
|---|---|---|
| sword | Q13442 | Covers all sword subtypes |
| dagger | Q571 | Daggers, stilettos, dirks |
| polearm | Q44448 (spear) + Q5386 (halberd) | Compound class |
| bow | Q9134 | Includes longbow, recurve, composite |
| crossbow | Q20484 | Crossbows and arbalests |
| firearm | Q841628 | All gunpowder projectile weapons |
| thrown | Q1148715 | Throwing weapons (chakram, shuriken) |
| staff | Q842944 | Magical staves (no direct Wikidata Q for magical staff) |
| wand | Q949932 | Wands (no direct Q; Q949932 is "divining rod" — proxy) |
| orb | none | Fictional; no Wikidata equivalent |
| tome | Q49848 (book) | Grimoires as a book subclass |
| hammer_mace | Q41137 (mace) + Q11443 (hammer) | Compound class |
| axe | Q42948 | Axes including battle axe |
| shield | Q131529 | Defensive equipment |
| ritual_instrument | Q220659 (incense burner) | Proxy for censer/thurible |

**Wikidata gap:** Fantasy and fictional weapon types (orb, wand as magic item, censer as
weapon) have no clean Wikidata equivalents. The `weapon_class` enum must extend beyond
Wikidata's ontology for the 15-gear catalogue coverage.

---

## 4. Gaps and Lossy Mappings — Consolidated

| Field | Sources with CLEAN mapping | Sources with LOSSY mapping | Gap notes |
|---|---|---|---|
| `weapon_class` | Kenney (filename parse), Meshy (subcategory), Smithsonian (object_name) | Sketchfab (tags only), OGA (tags), itch.io (pack description) | Acceptable; keyword parse covers >80% of cases; remainder via manual review queue |
| `cultural_lineage` | Smithsonian (structured culture field) | ALL others (free-text inference) | Most critical lossy mapping; requires NLP pass at import time for non-Smithsonian sources |
| `tech_level` / `era` | Smithsonian (date field), Kenney (pack-level), itch.io tags | Sketchfab (inconsistent tags), Meshy (tags), TurboSquid (title), OGA (tags) | Moderate lossiness; "medieval" is the most common tag; fantasy and sci-fi relatively cleanly tagged |
| `tone` | None (all sources) | ALL sources | Tone is never a structured field; always inferred from tags + visual style. Acceptable initial default: "heroic" for fantasy packs, "utility" for Smithsonian, "grim" for dark/dungeon-tagged models |
| `geometry_class` | None (all sources) | ALL sources | Always inferred from weapon_class; never directly sourced. Must be derived from weapon_class → geometry_class inference table (proposed in selection-patterns.md) |
| `license` | Smithsonian (CC0 fixed), Kenney (CC0 fixed), Meshy (CC0 fixed), Sketchfab (API field), OGA (structured upload field) | itch.io (free-text), TurboSquid/CGTrader (proprietary enum mapping required) | License is the highest-priority clean field; most major sources handle it well |
| `gear_catalogue_match` | None (all sources) | ALL sources | Always rule-derived from (weapon_class × range_class × stat_affinity); never sourced directly. This is an inference layer added at import time by the import pipeline. |

---

**Signed (research):** legolas (research scout; Mode A analytical)
**For:** canonical tag schema specification for weapon DB import; per-library normalization
mapping for rocket/drax import pipeline implementation; gaps documented for import strategy calibration.
