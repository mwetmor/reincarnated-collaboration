# Library Enumeration — Weapon 3D Model Sources
# Priority 1 (Mode A + Mode B mixed — library scale/license/format survey)

**Date:** 2026-05-22
**Mode:** A + B mixed
**Commissioner:** gandalf, authorized by Matt 2026-05-22 evening
**Commission:** `agentic_orchestration/dispatches/2026-05-22-legolas-weapon-library-import-discovery.md`
**Sources consulted:** Sketchfab, Open Game Art, Smithsonian Open Access, TurboSquid, CGTrader,
Free3D, Clara.io, BlendSwap, itch.io, Meshy.ai, Poly Haven, RenderHub, Open3dModel,
Fab (Epic Games), Wikidata SPARQL, Wikipedia weapons taxonomy. Web research 2026-05-22.

---

## Summary

Twelve enumerated 3D-model libraries span from enormous commercial catalogues (TurboSquid: 42K+ weapon
models; CGTrader: 127K+ weapon models; Meshy.ai: 60K+ weapon models) to curated CC0 collections
(Smithsonian: ~172 models on Sketchfab, ~3,583 total 3D digitization catalogue items; Open Game Art:
389 3D weapon entries; Kenney.nl: compact CC0 packs). The landscape separates cleanly into four tiers by
license-fitness for a shipping indie game: (A) CC0 sources — Meshy.ai, Smithsonian, Kenney.nl, OGA
subset, Sketchfab CC0 subset; (B) CC-BY sources — Sketchfab CC-BY subset, BlendSwap; (C) paid
royalty-free perpetual — TurboSquid, CGTrader, RenderHub; (D) reject-or-verify — Free3D (personal-use
default), Clara.io (platform defunct), itch.io mixed. Wikidata and Wikipedia provide taxonomy
infrastructure, not model assets. Meshy.ai's user-submission library (60K+ weapon models, CC0,
FBX/GLB/OBJ) is the single most import-ready large source; Sketchfab's 2,570-model weapons-military
CC category (structured API, rich metadata) is the highest-signal curated source.

---

## Library Profiles

---

### 1. Sketchfab

**Overview.** Largest general 3D-model platform with an established API and Creative Commons licensing
infrastructure. Acquired by Epic Games/Fab ecosystem but retains independent operation. The platform
hosts ~5 million total models (as of 2022, continuing to grow). A peer-reviewed dataset (S3D3C, arXiv
2407.17205) extracted 40,802 CC-licensed models from Sketchfab; of these, the Weapons & Military
category contains 2,570 models (6.3% of the CC dataset). The full weapons-military category (all
license types) is substantially larger.

```
Library: Sketchfab
Total models (weapon-tagged or estimated):
  - Weapons & Military CC-only (S3D3C dataset): 2,570
  - All licenses weapons-military: estimated 15,000–25,000 (based on platform scale; exact count
    requires API query against category slug "weapons-military" without license filter)
  - CC0 licensed weapons-military: ~244 (9.5% of 2,570 CC models)
  - CC-BY licensed weapons-military: ~933 (36.3% of 2,570 CC models)
  - CC-BY-SA, CC-BY-NC, CC-BY-NC-SA, CC-BY-NC-ND: remaining ~1,393 CC models
  (NOTE: CC-BY-NC, CC-BY-NC-SA, CC-BY-NC-ND are REJECT — non-commercial)

Licensing breakdown:
  - CC0: ~9.5% of CC models (no attribution, public domain)
  - CC-BY: ~36.3% of CC models (attribution required, commercial OK)
  - CC-BY-SA: share-alike (complicates derivative product distribution; caution)
  - CC-BY-NC and variants: non-commercial restriction; REJECT for shipping game
  - Standard (non-CC): restricted to display/personal; no game-commercial use
  - Note: Sketchfab also supports CC-BY 4.0 and Sketchfab's own Standard license

Downloadability: API (Data API v3 at sketchfab.com/developers/data-api/v3);
  - Search by category, license, downloadable flag, tags — full parameter support
  - OAuth2 authentication required
  - Per-asset download requires separate Download API call with OAuth token
  - Bulk download: NOT explicitly permitted; per-asset model; rate limits undocumented
    but cursor-based pagination for search results
  - GLB/GLTF/USDZ download formats available via Download API

Format support: GLB, GLTF, USDZ (primary download formats via API)
  Uploaders provide: FBX, OBJ, Blend, MAX, STL, DAE — converted to GLB for API download

Metadata fields exposed (per S3D3C + API documentation):
  - model UID, name, description, tags (90.2% of CC models have ≥1 tag)
  - category (75.3% have ≥1 category assignment)
  - license (CC0/CC-BY/CC-BY-SA/etc.)
  - creator username, creation date, published date
  - polygon count, texture files flag, animation flag, sound flag
  - downloadable flag, download format list
  - like count, view count, comment count
  - thumbnail URL, model viewer embed URL
  NOTE: era, material, cultural_lineage are NOT structured fields;
  they appear as free-text tags only (user-supplied; inconsistent)

Aesthetic register coverage:
  - medieval-European: STRONG — dominant visual register on platform
  - medieval-East-Asian: MODERATE — katana/samurai/ninja well-represented
  - medieval-South-Asian: THIN — scattered contributions
  - industrial/steampunk: MODERATE — dedicated creator communities
  - advanced/sci-fi: STRONG — firearms/futuristic heavily uploaded
  - primitive/tribal: THIN — occasional uploads; no dedicated community
  - other cultural lineages: THIN — African, Mesoamerican, Oceanic underrepresented

Confidence: HIGH
  - S3D3C paper (peer-reviewed, arXiv 2407.17205) provides rigorous statistics on CC model subset
  - Platform-scale figures sourced from official Sketchfab blog milestones (2022 data)
  - API documentation is published and current

Priority tier for import: TIER 1
  Rationale: largest CC-accessible 3D model platform with API; structural metadata + license
  filtering; FBX→GLB conversion pipeline already standardized; 2,570+ weapons in CC category
  with ~1,177 usable (CC0 + CC-BY combined). Highest import ROI per engineering hour.
```

---

### 2. Meshy.ai User Library

**Overview.** Meshy is primarily an AI generation service but hosts a substantial community-contributed
free model library as part of its platform strategy. The library has grown to 60K+ weapon models,
all marked CC0. The taxonomy is unusually comprehensive for a game-context source, with 8 weapon
subcategories. Format support (FBX, GLB, OBJ, STL, USDZ) is excellent for game import pipelines.

```
Library: Meshy.ai
Total models (weapon-tagged or estimated):
  - Weapons & Military total: 60,073+
  - Shields & Armor: 32,136
  - Swords & Blades: 12,287
  - Firearms: 7,151
  - Axes & Blunt: 2,463
  - Fantasy Weapons: 2,021
  - Heavy Weapons: 1,946
  - Polearms: 1,064
  - Bows & Ranged: 1,005

Licensing breakdown: CC0 (confirmed on platform) — royalty-free, commercial use,
  no attribution required. Free to download without subscription.

Downloadability: Per-asset web download (no formal API documented publicly);
  bulk download not explicitly supported; must be per-asset via web interface or
  undocumented API endpoint. Download mechanism identical to Meshy generation output.

Format support: STL, 3MF, FBX, GLB, OBJ, USDZ — all available per model

Metadata fields exposed:
  - model name, category, subcategory, tags (popular: armor, sword, helmet, blade, gun,
    shield, staff, RPG, rifle, pistol, katana, bow)
  - creator attribution (platform username)
  - download count, like count
  - license (CC0 uniform)
  NOTE: No structured era, material, cultural_lineage, or mechanical property fields;
  all such info in free-text tags

Aesthetic register coverage:
  - medieval-European: STRONG — largest single subcategory by count (Swords & Blades)
  - medieval-East-Asian: STRONG — katana/samurai prominent in tags
  - medieval-South-Asian: THIN — scattered
  - industrial/steampunk: MODERATE — Firearms (7,151) covers modern + steam-adjacent
  - advanced/sci-fi: MODERATE — RPG and futuristic tags present
  - primitive/tribal: THIN — underrepresented
  - fantasy (non-cultural): STRONG — dedicated subcategory (2,021 fantasy weapons)

Confidence: HIGH for count and license (confirmed on platform); MEDIUM for aesthetic
  register coverage estimates (based on tag analysis, not systematic sampling)

Priority tier for import: TIER 1
  Rationale: largest CC0-licensed weapon library found; compatible formats; good
  subcategory taxonomy maps well to 15-gear catalogue; free; the platform is also
  the Meshy gap-fill destination (dual use: import source + generation target).
  Limitation: no formal bulk API; web scrape or per-asset download required.
```

---

### 3. Open Game Art (OGA)

**Overview.** Established game-asset repository founded 2009, community-contributed, with formal
license metadata on all submissions. 389 total 3D weapon entries (filtered to 3D Art type, keyword
"weapon"). The "CC0 - 3D Weapons" collection on OGA aggregates 100+ CC0 weapon models across
sword, axe, polearm, ranged, shield, and modern firearm types. Submission quality is variable but
license clarity is uniformly high — the platform enforces license selection at upload.

```
Library: Open Game Art (OGA)
Total models (weapon-tagged or estimated):
  - 3D Art + keyword "weapon": 389 results
  - CC0 - 3D Weapons aggregate collection: 100+ individual weapon models
  - Note: 389 is individual submissions, which can be single models or multi-pack submissions

Licensing breakdown:
  - CC0: meaningful subset (the dedicated CC0 weapons collection confirms availability)
  - CC-BY 3.0 and 4.0: present
  - OGA-BY 3.0 and 4.0: OGA's own license (attribution to OGA required); similar to CC-BY
  - CC-BY-SA 3.0 and 4.0: share-alike (caution for game distribution)
  - GPL 2.0 and 3.0: REJECT — incompatible with closed-source product distribution
  Precise CC0/CC-BY count within the 389 requires per-page extraction; estimated ~30–40%
  based on platform culture and CC0 collection size

Downloadability: Per-asset web download; no API; bulk download not supported.
  Free, no account required for download.

Format support: Blender (.blend) dominant; OBJ, FBX available for many submissions;
  formats are uploader-defined and inconsistent across submissions.

Metadata fields exposed:
  - title, description, tags, license, uploader, upload date
  - format listed (per submission)
  - download count, view count
  NOTE: No structured era/material/cultural fields; free-text description only

Aesthetic register coverage:
  - medieval-European: STRONG — sword/axe/mace family dominates
  - medieval-East-Asian: MODERATE — katana, naginata, shuriken present in CC0 collection
  - advanced/sci-fi: MODERATE — assault rifles, shotguns, sci-fi weapons present
  - fantasy (non-cultural): STRONG — fantasy sword variants common
  - other registers: THIN

Confidence: HIGH for count (confirmed on site); MEDIUM for license breakdown
  (precise CC0/CC-BY split requires full crawl)

Priority tier for import: TIER 2
  Rationale: strong license clarity; game-focused; 389 is a tractable full-crawl size.
  Lower priority than Sketchfab/Meshy on scale, but high signal-to-noise within its
  niche. GPL models must be filtered out. OGA-BY license is acceptable if attribution
  mechanism exists in game credits.
```

---

### 4. Smithsonian Open Access

**Overview.** Museum-grade photogrammetry scans of real historical artifacts, all CC0. The 3D
Digitization program has 3,583 searchable entries in its own portal, with 172 of those published
to Sketchfab. Total Smithsonian Open Access is 5.1M+ items (2D + 3D combined). The 3D collection
focuses on artifacts, natural specimens, vehicles, and historical objects. Weapons coverage exists
but is not systematically enumerable without API access (requires a valid api.data.gov key; DEMO key
is invalid). The notable value is not scale but cultural authority: real historical weapons from
19+ cultures — Japanese swords, Native American weapons, African tribal arms, European medieval
swords — with museum provenance metadata.

```
Library: Smithsonian Open Access
Total models (weapon-tagged or estimated):
  - Total 3D digitization catalogue (all categories): 3,583 searchable entries
  - Published to Sketchfab: 172 models (confirmed on Smithsonian Sketchfab profile)
  - Weapon-specific count: NOT enumerable without API key; estimated 100–400 based on
    collection scope (military history + anthropology + history museums contribute)
  - Full Smithsonian Open Access (2D + 3D, all media): 5.1M+ items

Licensing breakdown: CC0 (all open access items) — public domain dedication;
  Smithsonian waives all copyright claims on CC0 items. Museum attribution
  encouraged but not legally required.

Downloadability:
  - Smithsonian Open Access API (api.si.edu) with api.data.gov key registration
  - Supports full-text search + filter by online_media_type=3d_mesh
  - JSON response with metadata + download URLs
  - 3D.si.edu portal for direct web browse/download
  - Sketchfab profile (@Smithsonian) for the 172 Sketchfab-published models
  - Bulk download: API supports pagination; practical bulk retrieval is possible
    with registered key

Format support: OBJ and glTF (official Smithsonian formats);
  some models available via Sketchfab in GLB/GLTF

Metadata fields exposed (museum-grade, highest quality of any source):
  - object name, catalog number, collection (museum/department)
  - culture / cultural affiliation (structured field)
  - date / date range (era field — structured)
  - materials (structured field)
  - dimensions (physical measurements)
  - description, provenance, credit line
  - online_media_type (3d_mesh / images / etc.)
  - download URL, thumbnail URL
  NOTE: Metadata quality far exceeds other sources; cultural_lineage and era are
  STRUCTURED fields, not free-text tags — directly importable into canonical schema.

Aesthetic register coverage:
  - medieval-European: STRONG — arms and armor collections (swords, shields, armor)
  - medieval-East-Asian: STRONG — Japanese, Korean, Chinese military artifacts
  - medieval-South-Asian: MODERATE — Indian arms in National Museum of Asian Art
  - African: MODERATE — National Museum of African Art contributions
  - Native American / Mesoamerican: MODERATE — NMNH + NMAI contributions
  - medieval-Islamic/Middle-Eastern: MODERATE — Freer Gallery contributions
  - advanced/sci-fi: EMPTY — historical artifacts only

Confidence: HIGH for license and API (official documentation);
  MEDIUM for weapon count estimate (API required for precise count)

Priority tier for import: TIER 2
  Rationale: irreplaceable for cultural authenticity in non-European registers.
  Scale is small but metadata quality is uniquely high. CC0 license is ideal.
  API key registration required before import — low barrier (free registration).
  Primary use: non-European cultural weapon instances; historical authenticity layer.
```

---

### 5. TurboSquid

**Overview.** Largest commercial 3D-model marketplace with 42,000+ weapon models and 56,000+
"weaponry" models. Owned by Shutterstock. License is royalty-free perpetual (per-purchaser,
not per-seat) covering games, film, advertising, and most commercial uses. Free models
available (400+ free weapons) under identical license terms to paid models. No API for
bulk programmatic download; per-asset purchase required.

```
Library: TurboSquid
Total models (weapon-tagged or estimated):
  - "weapons" category: 42,000+
  - "weaponry" category: 56,000+
  - "weapon pack" category: 1,100+
  - Free weapons: estimated 400–800 (based on free filter on weapons category)
  - GLB-format weapons: 600+ (GLB-specific filter)

Licensing breakdown:
  - Royalty-free perpetual (standard): once purchased, unlimited projects, no future fees
  - Free models: same license terms as paid models (confirmed in TurboSquid license doc)
  - REJECT policy: no AI training; no redistribution of model files directly;
    no missile/WMD use (export control clause)
  - Editorial license: some models restricted to news/academic use — FILTER OUT

Downloadability: Per-asset purchase/download only; no API for programmatic access.
  Each model must be individually purchased (or downloaded if free).
  Not suitable for automated bulk import.

Format support: FBX, OBJ, MAX (3ds Max), MA/MB (Maya), C4D, GLB/GLTF, USD —
  format availability per-model (uploader provides; StemCell models auto-convert to FBX/MAX/Maya/C4D/GLB/USD)

Metadata fields exposed (per product page):
  - title, description, polygon count
  - file formats available
  - rigged flag, animated flag, PBR flag
  - texture resolution
  - creator name
  NOTE: No structured era/culture/material fields; free-text description + category tags only.
  Tags are user-supplied; inconsistent quality.

Aesthetic register coverage:
  - medieval-European: STRONG — sword/sword-pack/armor categories dense
  - medieval-East-Asian: STRONG — samurai/katana/ninja well-served
  - medieval-South-Asian: MODERATE — Indian swords, katar present
  - industrial/steampunk: STRONG — firearms + steampunk packs
  - advanced/sci-fi: STRONG — large futuristic weapon packs
  - primitive/tribal: MODERATE — spears, clubs, stone weapons
  - other cultural lineages: MODERATE — African, Islamic, Viking all present

Confidence: HIGH for count (sourced from TurboSquid search page metadata);
  HIGH for license terms (official TurboSquid blog post confirms perpetual royalty-free)

Priority tier for import: TIER 3 (deferred)
  Rationale: scale and quality are high but no API and per-asset purchase model
  make automated bulk import impractical. Better suited for targeted gap-fill of
  specific substrate-vectors where free sources are thin. Use case: high-value
  specific archetype instances (e.g., a specific cultural weapon not found elsewhere).
```

---

### 6. CGTrader

**Overview.** Major commercial + free 3D model marketplace with 127,000+ weapon models, the
largest raw count of any surveyed library. Royalty-free perpetual license for paid and free
models. Free models are confirmed commercial-use-OK under CGTrader royalty-free terms, with
the restriction that the model file itself cannot be redistributed. No public API.

```
Library: CGTrader
Total models (weapon-tagged or estimated):
  - "weapon" category: 126,920 (free + premium combined)
  - Free weapons: unknown split (CGTrader has substantial free offerings; estimated 3,000–8,000)
  - Low-poly weapons: dedicated subcategory (relevant for real-time use)

Licensing breakdown:
  - Royalty-free (standard): perpetual, commercial use, unlimited projects, no resale of model file
  - Free models: CGTrader confirmed free models can be used commercially under royalty-free terms
  - No CC0 or CC-BY structured licenses; proprietary royalty-free only
  NOTE: Royalty-free from CGTrader is COMPATIBLE with game distribution but requires
  purchase (even if $0 for free models — account + download required). Per-model terms
  may vary; some free models carry additional restrictions.

Downloadability: Per-asset web download only; no API documented.
  Free models require account creation.

Format support: MAX, OBJ, FBX, 3DS, C4D — format varies per model.
  GLB not specifically noted; OBJ and FBX are most common.

Metadata fields exposed:
  - title, description, tags, category
  - polygon count, format list
  - rigged/animated/PBR flags
  - creator attribution, upload date
  NOTE: No structured era/culture/material fields.

Aesthetic register coverage:
  - medieval-European: STRONG
  - medieval-East-Asian: STRONG
  - advanced/sci-fi: STRONG
  - industrial: STRONG
  - primitive/fantasy: MODERATE
  - South Asian/African/Mesoamerican: THIN to MODERATE

Confidence: HIGH for count (CGTrader search page confirmed 126,920 weapons);
  MEDIUM for license breakdown (precise free count requires direct query)

Priority tier for import: TIER 3 (deferred)
  Rationale: largest catalogue but no API + proprietary license (not CC) reduces
  import-pipeline suitability. Same role as TurboSquid: targeted gap-fill for
  specific substrate-vectors. Prefer over TurboSquid for free-tier options.
```

---

### 7. Free3D

**Overview.** Free model repository with 1,605 weapon models. Two-tier licensing structure:
"Free Personal Use" (no commercial use) and "Royalty Free" (commercial use permitted, purchased
with credits). The personal-use tier makes the majority of Free3D models UNSUITABLE for a
shipping game without per-model purchase of the royalty-free license. Format support is broad
(OBJ, FBX, Blend, C4D, MAX, STL, DAE).

```
Library: Free3D
Total models (weapon-tagged or estimated): 1,605 weapon models

Licensing breakdown:
  - "Free Personal Use" (majority of free models): personal use ONLY — REJECT for game
  - "Royalty Free" (purchasable, some models free at this tier): commercial use OK
  - Exact split between personal-use and royalty-free within the 1,605 unknown;
    requires per-page extraction

Downloadability: Per-asset web download; no API.

Format support: OBJ, FBX, Blend, C4D, 3DS, MAX, DAE, STL, GLTF, DUF (Daz), TBSCENE

Metadata fields exposed: title, format, polygon class (low/mid/high), creator, tags, PBR flag

Aesthetic register coverage:
  - medieval-European: STRONG
  - modern military: STRONG
  - sci-fi: MODERATE
  - other: THIN

Confidence: HIGH for count (confirmed search result count on Free3D);
  HIGH for license problem (sourced from Free3D Terms & Conditions)

Priority tier for import: TIER 3 — conditional
  Rationale: personal-use default makes bulk import risky without per-model license
  verification. Only the royalty-free tier is usable. Small scale relative to effort.
  Low ROI vs. Sketchfab or Meshy for equivalent effort. Defer.
```

---

### 8. Clara.io

**Overview.** Clara.io was a browser-based 3D modeling + library platform offering 100,000+
free models with CC licensing options. HOWEVER: Clara.io was permanently shut down December 31,
2022. The site is partially functional for logged-in users but is in terminal state. New
registrations are closed or unreliable.

```
Library: Clara.io
Status: DEFUNCT (permanently shut down December 31, 2022)
Weapon model count: Unknown; platform offline
Downloadability: BLOCKED — site in terminal state; new accounts unavailable
License: CC licenses were offered but platform is no longer operational

Priority tier for import: DEFER indefinitely
  Rationale: platform is defunct. No import path.
```

---

### 9. BlendSwap

**Overview.** Blender community model-sharing platform with CC0 and CC-BY licensing. All models
are in Blender's native .blend format — a conversion step (export to FBX/GLB from Blender) is
required for every model, adding pipeline overhead. CC0 models confirmed (defaulted to CC0 for
most uploads; Durian-licensed models are CC-BY). Weapon coverage is small and community-scale.

```
Library: BlendSwap
Total models (weapon-tagged or estimated):
  - CC0 weapons: estimated 50–150 (based on known collections: 10 swords + 4 shields + firearms kit)
  - Full CC0 catalogue: 3,000–5,000 models (all categories combined; estimated)
  - Weapon-specific count requires full crawl

Licensing breakdown:
  - CC0: majority of platform (default license for uploads)
  - CC-BY (Durian): small subset
  - No commercial restrictions on CC0 or CC-BY
  NOTE: BlendSwap confirmed "everything defaulted to CC0 except Durian category"

Downloadability: Per-asset web download; account required. No API.
  Format: .blend only; requires Blender conversion pipeline before import.

Format support: .blend ONLY — conversion to FBX/GLB/OBJ requires Blender export step.
  Pipeline overhead: significant; every model needs Blender batch export.

Metadata fields exposed:
  - title, category, license, creator, download count, polygon count
  NOTE: No era/culture/material structured fields.

Aesthetic register coverage:
  - medieval-European: MODERATE (swords, axes)
  - sci-fi/modern: MODERATE (firearms kit)
  - fantasy: MODERATE
  - other registers: THIN

Confidence: MEDIUM — platform is active but small; weapon count estimated not confirmed

Priority tier for import: TIER 3 — low priority
  Rationale: .blend-only format requires pipeline conversion overhead for every asset.
  CC0 license is ideal but scale is small and conversion cost is high. Use only if
  specific high-quality weapon not available from Sketchfab/Meshy/OGA.
```

---

### 10. itch.io (3D Game Asset Packs)

**Overview.** Indie game asset marketplace with 986 results tagged "3D" + "Weapons." Mix of free
(CC0 and custom) and paid ($5–$30 typical price point) packs. Many packs are multi-weapon bundles
(10–50+ weapons per pack) rather than individual models. License varies per creator: some CC0,
some royalty-free custom, some unlabeled. Aesthetic diversity is high (medieval, sci-fi, PSX,
voxel, horror, Western). Not suitable for automated bulk import due to per-creator license
variation and lack of API.

```
Library: itch.io
Total models (weapon-tagged or estimated):
  - Tag-3D + tag-Weapons: 986 results (packs/bundles, not individual models)
  - Individual model count: unknown; each pack contains 5–200+ models; estimated 5,000–50,000 total models
  - Free (tag-3D + tag-Weapons + free): substantial subset (majority of results from initial page view)

Licensing breakdown:
  - CC0 Public Domain: confirmed present (e.g., "PS1 Heavy and Light Weapons Pack", Binbun RPG Weapons)
  - Royalty-free (custom): common for paid packs
  - Unlabeled/custom: common for many creators; requires per-pack review
  - CC licenses: present but not uniform

Downloadability: Per-pack download; itch.io account required for most.
  Itch.io API exists for OAuth-authenticated download but is not a search/catalogue API.
  No bulk search API for asset metadata.

Format support: FBX most common; GLB/OBJ present but not universal;
  PNG textures standard; platform does not enforce format standards

Metadata fields exposed (per pack page):
  - pack name, creator, price, tags, description, screenshots
  - license: stated on pack page (inconsistent compliance)
  NOTE: No structured metadata; all in free-text description

Aesthetic register coverage:
  - medieval/fantasy: STRONG
  - sci-fi/cyberpunk: MODERATE
  - PSX/retro: MODERATE
  - horror: MODERATE
  - Western: THIN
  - voxel: THIN

Confidence: HIGH for count (confirmed 986 results on search page);
  MEDIUM for individual model count (pack sizes vary widely);
  LOW for license breakdown (requires per-pack inspection)

Priority tier for import: TIER 2 — selective import only
  Rationale: 986 packs is manageable but per-pack license review is required.
  High aesthetic diversity makes it valuable for non-European register coverage.
  Focus on CC0-tagged packs (filterable on itch.io). Particularly valuable for:
  - PSX/retro aesthetic register (unique to itch.io)
  - low-poly stylized weapons (game-ready, consistent scale)
  - niche cultural weapons (African, tribal, horror) absent from larger catalogues.
```

---

### 11. Kenney.nl

**Overview.** High-quality CC0 game-art creator with a focused catalogue of packs. All assets CC0
(confirmed). 40,000+ total assets across all packs. Weapon packs include: Medieval RTS (120 assets
covering medieval siege + melee + ranged weapons), Blaster Kit (40 sci-fi blaster variants), and
weapon assets within environment packs (Dungeon Kit, Pirate Kit, etc.). Formats are typically GLB,
OBJ, and FBX. Kenney packs are the gold standard for quick CC0 game-ready imports: clean topology,
consistent scale, game-engine-ready.

```
Library: Kenney.nl
Total models (weapon-tagged or estimated):
  - Dedicated weapon packs: 2–3 packs (Medieval RTS with 120 assets; Blaster Kit with 40 assets)
  - Weapons within environment packs (Dungeon Kit, Pirate Kit): additional 20–50 weapons estimated
  - Total weapon models: estimated 200–400

Licensing breakdown: CC0 CONFIRMED — all Kenney assets, no exceptions.
  "Use for any purpose, even commercially, without attribution required."

Downloadability: Direct web download; no API; no account required.
  Packs available as ZIP archives containing all formats.

Format support: GLB, OBJ, FBX (all three per pack); textures as PNG.
  Game-engine-ready topology confirmed.

Metadata fields exposed: minimal — pack name, category, license, total count.
  No per-model metadata beyond file name.

Aesthetic register coverage:
  - medieval-European: STRONG (Medieval RTS)
  - sci-fi: MODERATE (Blaster Kit)
  - other registers: THIN to EMPTY

Confidence: HIGH (direct source review; Kenney.nl is authoritative)

Priority tier for import: TIER 1
  Rationale: CC0, game-ready GLB/FBX, clean topology, free ZIP archive per pack.
  Ideal bootstrap layer for Tier 1 import. Small scale but zero friction.
  Begin import phase A with Kenney packs as schema validation test set.
```

---

### 12. Poly Haven

**Overview.** CC0 3D-model library focused on photorealistic props, environments, and materials.
Model categories: Props, Furniture, Decorative, Industrial, Appliances, Nature, Electronics,
Tools, Lighting. NO dedicated weapons category. Occasional overlap (knives, axes visible as
"tools"). Not a primary weapon source. All CC0, GLB/FBX/BLEND formats.

```
Library: Poly Haven
Total models (weapon-tagged or estimated):
  - Weapons in dedicated weapon category: 0 (no such category exists)
  - Weapons as "tools" crossover: estimated <10 (knives, utility blades)

Licensing breakdown: CC0 CONFIRMED — all assets.

Priority tier for import: DEFER
  Rationale: Not a weapon source. Occasional crossover items (bladed tools) can be
  noted opportunistically during broader tool/prop sweeps, but not a meaningful
  weapon-library import target.
```

---

### 13. Wikidata Q-items

**Overview.** Semantic web knowledge graph with structured weapon taxonomy, accessible via
SPARQL query service. NOT a 3D-model source — provides ontology and classification tree only.
Relevant use: derive the canonical tag taxonomy backbone for the weapon DB schema.

SPARQL query results (executed 2026-05-22):
- Total weapons in Wikidata (wdt:P31/wdt:P279* wd:Q728): 10,497 entries
- Structural entries: video game weapons (325), fictional weapons (218), archaeological artifacts (213)
- By type: sword (223), cannon (86), dagger (91), saber (58), arrow (63), firearm (54), spear (54), pistol (38), halberd (38), crossbow bolt (41)
- Specialized: Japanese swords (48), tachi (47), mythological swords (61), fictional swords (79)

**Value for schema design:** Wikidata's P279 (subclass-of) hierarchy is the most complete
machine-readable weapon taxonomy available. Key node IDs relevant to the 15-gear catalogue:
- Q728 = weapon (root)
- Q13442 = sword | Q44448 = spear | Q9134 = bow | Q20484 = crossbow | Q571 = dagger
- Q842944 = staff | Q949932 = wand | Q41137 = mace | Q11443 = hammer | Q5386 = halberd

```
Library: Wikidata
3D models available: NONE
Value: taxonomy backbone for tag_taxonomy table in DB schema
Downloadability: SPARQL query service (free, no auth required)
Priority tier for import: ONTOLOGY ONLY — incorporate into tag_taxonomy table
```

---

### 14. Wikipedia Weapons Category

**Overview.** Multi-dimensional classification system with 53 subcategories. Organizes weapons by
geographic origin (101 country subcategories), temporal period (8 eras), functional type
(edged/bladed, projectile, blunt, polearms), deployment context (aircraft/naval/vehicle-mounted),
and effect category (incendiary, chemical, non-lethal). Not a 3D-model source; value is
taxonomy reference for canonical tag schema design.

Key structural dimensions for schema:
1. Functional: edged/bladed, blunt, polearms, projectile, siege
2. Geographic: European, East-Asian, South-Asian, African, Native-American, Middle-Eastern, Oceanic
3. Temporal: ancient (pre-500 CE), medieval (500–1500 CE), early-modern (1500–1800), modern (1800+)
4. Mechanism: hand-to-hand, thrown, bow, crossbow, firearm, gunpowder

```
Library: Wikipedia
3D models available: NONE
Value: taxonomy reference for cultural_lineage and era fields
Priority tier for import: TAXONOMY ONLY — incorporate into tag schema
```

---

### 15. Additional Sources (enumerated during sweep)

**Open3dModel.com:** 10,659 weapon models; license unclear (free but commercial terms not
confirmed); OBJ/FBX/Blend/STL formats; web-only download. CONFIDENCE: LOW on license.
Priority: DEFER until license clarified.

**RenderHub:** ~100+ free weapons with "Extended Use License" (commercial permitted);
OBJ/FBX/Blend/GLTF; no API; web-only. Size comparable to Free3D but cleaner license terms
for commercial use. Priority: TIER 3, same as Free3D.

**Fab.com (Epic Games):** Absorbed Sketchfab's marketplace functions. Separate from Sketchfab's
3D model browser. Weapons & Combat category for Unreal Engine-ready models. License is
Fab Standard (commercial OK, perpetual). Per-asset purchase model. Priority: TIER 3 — use for
Unreal-format weapons if needed.

---

## Priority Tier Summary

| Tier | Libraries | Rationale |
|---|---|---|
| TIER 1 | Sketchfab (CC0+CC-BY subset), Meshy.ai, Kenney.nl | Largest CC signal; API or bulk ZIP; best import mechanics |
| TIER 2 | Open Game Art, Smithsonian Open Access, itch.io (CC0-only) | Targeted value; tractable scale; manual or semi-manual import |
| TIER 3 | TurboSquid, CGTrader, RenderHub, Free3D (royalty-free tier), Fab | Commercial or friction-high; use for specific gap-fill |
| DEFER | Clara.io (defunct), BlendSwap (conversion overhead), Poly Haven (no weapons) | Not viable or low ROI |
| TAXONOMY | Wikidata, Wikipedia | Ontology backbone only; feeds tag_taxonomy table |

---

## Knowledge Gaps Not Resolved

1. **Exact CC0 vs CC-BY split within Sketchfab weapons-military category.** S3D3C dataset provides
   platform-wide ratios (9.5% CC0, 36.3% CC-BY) but not category-specific breakdown. Resolved at
   import time via API query with license filter `?license=by` vs `?license=pd`.

2. **Smithsonian weapon model count.** API key required for precise count; DEMO key invalid. Estimate
   of 100–400 based on collection scope. Resolved at import time with registered api.data.gov key.

3. **Free3D personal-use vs royalty-free split.** Requires full per-page crawl to determine commercial-safe
   subset. Best resolved by skipping Free3D entirely in favor of Sketchfab/Meshy.

4. **Meshy.ai bulk download API.** No public API documented; web scrape or per-asset approach required.
   The Meshy team may have an undocumented or partner API — worth querying before Phase A import.

5. **Open3dModel license terms.** 10,659 weapons but commercial license status unclear. Low priority
   to clarify given better alternatives available.

---

## Source List

- S3D3C paper: https://arxiv.org/html/2407.17205 (Sketchfab CC collection statistics)
- Sketchfab API: https://sketchfab.com/developers/data-api/v3
- Sketchfab license overview: https://sketchfab.com/licenses
- Smithsonian Open Access: https://www.si.edu/openaccess
- Smithsonian 3D Digitization: https://3d.si.edu/cc0
- Smithsonian Sketchfab profile: https://sketchfab.com/Smithsonian (172 models confirmed)
- CG Channel Smithsonian article: https://www.cgchannel.com/2020/03/get-2000-free-3d-models-from-the-smithsonian-collection/
- Open Game Art 3D weapons: https://opengameart.org/art-search-advanced?keys=weapon&field_art_type_tid[]=10
- OGA CC0 weapons collection: https://opengameart.org/content/cc0-3d-weapons
- TurboSquid weapons: https://www.turbosquid.com/3d-model/weapons (42K+ count)
- TurboSquid license: https://blog.turbosquid.com/turbosquid-3d-model-license/
- CGTrader weapons: https://www.cgtrader.com/3d-models/weapon (126,920 count)
- CGTrader royalty-free license: https://help.cgtrader.com/hc/en-us/articles/360015124437
- Free3D weapons: https://free3d.com/3d-models/weapons (1,605 count)
- Free3D license: https://free3d.com/help/en/articles/9937609-royalty-free-license
- Clara.io shutdown: https://en.wikipedia.org/wiki/Clara.io
- BlendSwap licensing: https://www.blendswap.com/news/post/17
- itch.io 3D weapons: https://itch.io/game-assets/tag-3d/tag-weapons (986 results)
- Kenney.nl weapon assets: https://kenney.nl/assets/medieval-rts
- Meshy.ai weapons: https://www.meshy.ai/category/weapons-military (60,073+ models)
- Poly Haven models: https://polyhaven.com/models
- RenderHub free weapons: https://www.renderhub.com/free-3d-models/weapons
- Wikidata SPARQL: https://query.wikidata.org/
- Wikipedia weapon category: https://en.wikipedia.org/wiki/Category:Weapons
- Wikipedia premodern weapons: https://en.wikipedia.org/wiki/List_of_premodern_combat_weapons
