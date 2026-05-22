# Import Strategy — Phased Weapon Library Import Plan
# Priority 5

**Date:** 2026-05-22
**Mode:** A (analytical; strategic recommendation)
**Commissioner:** gandalf, authorized by Matt 2026-05-22 evening
**Commission:** `agentic_orchestration/dispatches/2026-05-22-legolas-weapon-library-import-discovery.md`
**Depends on:** `library-enumeration.md`, `metadata-normalization.md`, `sql-ddl-proposal.md`,
`selection-patterns.md` (all this directory)

---

## Summary

Four-phase import plan spanning approximately 6–10 weeks of elapsed time (after schema
approval). Phase A: schema lock + Kenney/OGA/Smithsonian seed set (100–500 weapons; validates
pipeline; zero-cost). Phase B: Sketchfab CC0+CC-BY + Meshy.ai bulk (2,000–5,000 weapons;
proves API-based bulk import; medieval-European dominance). Phase C: itch.io CC0-tagged packs
+ targeted aesthetic-expansion sources (adds 1,000–3,000 weapons across non-European registers;
completes substrate density map). Phase D: Meshy gap-fill against the density map (fills empty
and sparse substrate regions; on-demand generation). License-tier policy: CC0 is the preferred
tier (20 pts in scoring); CC-BY is accepted (15 pts); CC-BY-SA is conditional (share-alike
complication requires legal review); GPL and CC-NC are hard rejects. Commercial royalty-free
(TurboSquid/CGTrader) is deferred to targeted gap-fill dispatch after Phase D confirms which
specific archetypes remain empty.

---

## 1. Tier Assignments — Final Recommendations

### Tier 1 (Phase A + B — primary import)

| Library | Rationale | Est. weapon count | License class |
|---|---|---|---|
| **Kenney.nl** | CC0; game-ready GLB/FBX; ZIP archive; zero friction; ideal Phase A seed | 200–400 | CC0 |
| **Sketchfab (CC0+CC-BY)** | API; 2,570+ in weapons-military CC category; rich metadata; medieval-EU dominant | 1,000–2,000 usable | CC0 + CC-BY |
| **Meshy.ai library** | CC0; 60K+ weapons; 8-subcategory taxonomy; FBX/GLB/OBJ | 3,000–10,000 targeted | CC0 |

**Tier 1 combined target:** 4,200–12,400 weapons imported and indexed.

### Tier 2 (Phase C — aesthetic expansion + cultural depth)

| Library | Rationale | Est. weapon count | License class |
|---|---|---|---|
| **Open Game Art** | CC0+CC-BY; game-focused; 389 3D entries; license structured; GPL filter required | 150–250 usable | CC0 + CC-BY |
| **Smithsonian Open Access** | CC0; museum-grade cultural metadata; unique non-European coverage | 100–400 | CC0 |
| **itch.io (CC0-tagged only)** | Aesthetic diversity; PSX/voxel/low-poly registers; 986 packs | 200–600 usable | CC0 subset |

**Tier 2 combined target:** 450–1,250 additional weapons imported.

### Tier 3 (Targeted gap-fill only — after Phase D density analysis)

| Library | Rationale | Use case | License class |
|---|---|---|---|
| **TurboSquid** | 42K+ weapons; perpetual royalty-free; no API | Fill specific high-value empty substrate regions | Royalty-free commercial |
| **CGTrader** | 127K+ weapons; perpetual royalty-free; no API | Same as TurboSquid | Royalty-free commercial |
| **RenderHub** | ~100+ free weapons; Extended Use License | Same; smaller friction | Royalty-free commercial |
| **Fab.com** | Unreal-format weapons; perpetual | Specific format-match needs | Royalty-free commercial |
| **Free3D (royalty-free tier)** | 1,605 weapons; personal-use default; commercial tier requires per-model verification | Last resort; low ROI | Royalty-free (verify per model) |

**Tier 3 dispatch trigger:** After Phase D density analysis, knight-rider fires targeted
per-substrate-region dispatches for empty/sparse regions not filled by Meshy gap-fill.

---

## 2. Per-Tier Scale Targets

### Tier 1 scale targets

**Kenney.nl (Phase A seed):**
- Target: ALL available weapon models across all Kenney packs (estimated 200–400 total)
- Acquisition: Full ZIP archive download per pack
- Rationale: 100% CC0, game-ready format, clean normalization — ideal for schema validation
- Cost: $0

**Sketchfab (Phase B API crawl):**
- Target: All CC0 + CC-BY models in weapons-military category (~1,177 models per S3D3C ratios)
- Filter: `downloadable=true & license=by | license=pd & category=weapons-military`
- Rationale: Covers the highest-signal curated 3D source; API makes per-asset metadata
  extraction tractable; focuses on the ~45% game-approved CC subset (~1,177 of 2,570)
- Exclude: CC-BY-SA (share-alike), CC-BY-NC and variants (non-commercial)
- Cost: $0 (OAuth registration required; no per-model fee for CC models)

**Meshy.ai library (Phase B targeted crawl):**
- Target: Swords & Blades (12,287), Polearms (1,064), Bows & Ranged (1,005), Fantasy Weapons (2,021)
  — approximately 16,377 models across the four most relevant fantasy-weapon subcategories
- Initial Phase B scope: top 1,000 by download count in each subcategory = 4,000 targeted
- Exclude: Shields & Armor (32,136 — armor is a separate commission)
- Rationale: CC0 uniform; FBX/GLB/OBJ available; largest fantasy-weapon library; top-downloaded
  models are highest quality within the CC0 pool
- Cost: $0 (per-asset web download; no formal API — web scrape or API exploration required)

### Tier 2 scale targets

**Open Game Art:**
- Target: Full crawl of all 389 3D weapon entries
- Filter post-crawl: reject GPL; keep CC0, CC-BY, OGA-BY
- Cost: $0

**Smithsonian Open Access:**
- Target: All 3D mesh items with object classification matching weapons/arms/military
- API query: `online_media_type=3d_mesh & q=sword OR spear OR axe OR bow OR dagger OR mace`
  (iterate across weapon type terms to enumerate full corpus)
- Registration: api.data.gov free key required before import dispatch
- Cost: $0

**itch.io CC0-tagged packs:**
- Target: Packs tagged "3D" + "Weapons" + "cc0" (itch.io CC0 filter)
- Estimated scope: 50–100 packs × average 5–15 weapons per pack = 250–1,500 weapons
- Manual per-pack license review required before download
- Cost: $0 (free packs only; paid CC0 packs are excluded from Phase C scope)

---

## 3. License-Tier Policy

### Approved licenses (game_approved = 1 in licenses table)

| License | Approval | Condition | Attribution handling |
|---|---|---|---|
| **CC0** | APPROVED — preferred | No conditions | No attribution required; ideal for shipping |
| **CC-BY (3.0 and 4.0)** | APPROVED | Attribution required in game credits | Store attribution_text from source; include in credits screen |
| **OGA-BY** | APPROVED | Attribution to OGA required | Treat as CC-BY; credit OpenGameArt.org |
| **Royalty-Free Commercial (TurboSquid/CGTrader)** | APPROVED — conditional | Purchase required; perpetual commercial use permitted; no resale of model files | Record cost_usd and purchase date; no in-game credit required |
| **Smithsonian CC0 (cultural heritage)** | APPROVED | Smithsonian encourages voluntary attribution | Add "Smithsonian Institution Open Access" to credits as cultural courtesy; not legally required |

### Rejected licenses (game_approved = 0 in licenses table)

| License | Rejection reason | Action |
|---|---|---|
| **GPL 2.0 / GPL 3.0** | Copyleft: would require open-sourcing the game engine | Hard reject; filter at crawl time; set readiness_state='rejected' |
| **CC-BY-SA** | Share-alike: any game containing these assets would need to be released under CC-BY-SA | Hard reject unless legal review confirms game-code/asset separation is sufficient |
| **CC-BY-NC** and variants | Non-commercial restriction; Reincarnated is a shipping commercial product | Hard reject |
| **Free Personal Use Only** | No commercial use permitted (Free3D default tier) | Hard reject unless commercial tier purchased |
| **Editorial Only** | News/academic use restriction | Hard reject |
| **Unknown / no license declared** | Cannot confirm commercial use is permitted | Hard reject until license is confirmed; readiness_state='rejected' |

**CC-BY-SA borderline note:** CC-BY-SA is technically compatible with commercial use but
the share-alike clause creates downstream complication. The consensus in the indie game
community is that CC-BY-SA assets can be used in commercial games as long as the game's
asset files are kept separate and the game code is not itself under CC-BY-SA. Recommend
Matt/lawyer confirmation before any CC-BY-SA models are promoted to game_approved=1.
For now: set cc_by_sa to game_approved=0 and import_tier=3 pending review.

---

## 4. Four-Phase Import Sequence

### Phase A — Schema lock + Tier 1 seed set (estimated 1–2 weeks)

**Goal:** Prove the import pipeline end-to-end with a small, clean dataset before bulk import.

**Steps:**
1. Matt approves schema.sql (this dispatch's output)
2. Run schema.sql against `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
3. Import ALL Kenney weapon packs (ZIP download → unzip → normalize metadata → INSERT into weapons)
   - Kenney Medieval RTS (~120 assets) → 80–100 weapons after filtering non-weapon assets
   - Kenney Blaster Kit (~40 assets) → ~35 weapons
   - Weapons in Kenney Dungeon Kit, Pirate Kit: extract manually on inspection
   - Total Phase A insert: 150–250 weapons
4. Validate schema against real data: check compound indexes, query P1 with sample substrate-vectors,
   confirm density map populates correctly
5. Run P6 density check across all 15 × 7 × 3 = 315 substrate-vector combinations
   → expect MOST to be 'empty' (Kenney covers medieval-European only)
   → confirms Meshy gap-fill will be the primary source for Phase D

**Success criteria:**
- schema.sql runs without errors on target DB
- P1 query returns results for at least 5 distinct substrate-vectors with gear_catalogue_id in [1,2,5,6,11]
- density table populates with correct counts
- At least 3 CC0 models indexed and queryable per gear_catalogue_id=5 (Longbow; best Kenney coverage)

**Estimated compute:** 2–4 hours (ZIP download + normalize + insert + validate)
**Estimated cost:** $0

---

### Phase B — Tier 1 bulk import: Sketchfab + Meshy (estimated 2–4 weeks)

**Goal:** Scale to 4,000–12,000 weapons; prove API-based bulk import; establish medieval-European
density map.

**Sketchfab crawl:**
1. Register OAuth2 application at sketchfab.com/developers
2. Query Data API v3 with filters: `category=weapons-military & license=pd` (CC0) and
   `category=weapons-military & license=by` (CC-BY)
3. Paginate through results (cursor-based pagination); extract metadata per model
4. Download GLB for all models with `readiness_state = 'needs_format_conversion'`
5. Normalize metadata: parse tags for weapon_class, tech_level, cultural_lineage
6. INSERT into weapons + weapon_sources + weapon_aesthetic
7. Rate limit: 1 request per 2 seconds (per Sketchfab API guidelines)
8. Expected crawl time: ~4 hours for 1,177 models at 1 req/2 sec (metadata); downloads separate
9. Expected inserts: 800–1,200 weapons (after filtering for quality)

**Meshy.ai targeted crawl:**
1. Identify Meshy download mechanism (undocumented API or web scrape)
2. Scope: top-1,000 by download count from Swords & Blades + Polearms + Bows & Ranged + Fantasy Weapons
3. Download GLB per model (preferred format for runtime)
4. Normalize: subcategory → weapon_class; model name → weapon_subclass inference
5. Rate limit: 1 request per 3 seconds (conservative; no documented rate limit)
6. Expected crawl time: ~8 hours for 4,000 models
7. Expected inserts: 3,000–4,000 weapons (quality filter applied)

**Phase B success criteria:**
- Total weapons in DB: 3,500–5,000 after Phase B
- Density map: at least 10 of 15 gear_catalogue_ids have weapon_count_ready ≥ 3
- P1 returns ≥ 5 results for (medieval, european, any element, gear_catalogue_id in [1..11])
- License breakdown: ≥60% CC0, ≤35% CC-BY, ≤5% other game_approved

**Estimated compute:** 12–24 hours crawl time total; 1 week elapsed (batched over multiple sessions)
**Estimated cost:** $0

---

### Phase C — Tier 2 aesthetic expansion + cultural diversity (estimated 2–3 weeks)

**Goal:** Fill non-European, non-medieval substrate regions; reduce Meshy gap-fill dependency.

**Open Game Art full crawl:**
1. Scrape all 389 3D weapon entries from search results (pages 1–16 at 24/page)
2. Extract per-submission: title, license, format, download URL
3. Filter: keep CC0, CC-BY, OGA-BY; reject GPL
4. Download and normalize
5. Expected inserts: 120–180 weapons after GPL filter

**Smithsonian Open Access API:**
1. Register api.data.gov key (free; 5-10 minute registration)
2. Query: `online_media_type=3d_mesh & q=sword OR spear OR bow OR axe OR dagger OR mace OR lance OR shield OR armor`
   (iterate per weapon type; combine results)
3. Extract museum metadata fields: object_name, culture, date_range, materials, credit_line
4. Map culture → cultural_lineage; date_range → tech_level
5. Download OBJ or glTF
6. Expected inserts: 100–300 weapons (after non-weapon filter)
7. High-value specific weapons: Japanese katana (National Museum of Asian Art),
   Native American weapons (NMNH), European medieval arms (NMAH), African weapons (NMAFA)

**itch.io CC0 packs:**
1. Browse itch.io filtered to: game-assets, tag-3d, tag-weapons, CC0/Public Domain
2. Review each pack page for license verification
3. Download free CC0-confirmed packs
4. Unpack and normalize per-weapon models
5. Expected inserts: 200–500 weapons

**Phase C success criteria:**
- Total weapons in DB: 4,500–7,000
- Non-European cultural_lineage represented: east_asian ≥ 50, african ≥ 10, south_asian ≥ 10
- Density map: ≥ 12 of 15 gear_catalogue_ids have weapon_count_ready ≥ 3 across at least 3 elements
- Smithsonian weapons indexed with cultural_lineage_confidence = 1.0 (structured field)

**Estimated compute:** 6–12 hours; 2 weeks elapsed
**Estimated cost:** $0

---

### Phase D — Meshy gap-fill (ongoing; on-demand)

**Goal:** Fill remaining empty and sparse substrate regions from the density map with
AI-generated weapons. Not a batch import — on-demand generation triggered by density-routing
in the engine.

**Trigger:** density_tier = 'empty' or 'sparse' for any (element, range, gear_catalogue_id) vector.

**Gap-fill request format (engine → Meshy API):**
```json
{
    "prompt": "<weapon_subclass> weapon, <cultural_lineage> style, <tech_level> era, <tone> aesthetic",
    "format": "glb",
    "negative_prompt": "modern, firearms, cartoon eyes, sci-fi unless tech_level=sci_fi",
    "gear_catalogue_id": 13,
    "substrate_vector": {"element": "holy", "range": "medium"}
}
```

**Post-generation pipeline:**
1. Meshy returns GLB model
2. Insert into weapons with source_library='meshy_generated'
3. Set readiness_state='needs_scale_normalization' (Meshy GLBs need scale check)
4. Run scale normalization pass
5. Update density map
6. If substrate vector now has weapon_count_ready ≥ 3: clear meshy_gapfill_queued flag

**Priority substrate regions for initial gap-fill (post-Phase C expected gaps):**
- gear_catalogue_id = 13 (Censer / Thurible) — confirmed zero in prior Unity survey
- gear_catalogue_id = 14 (Holy Symbol / Icon) — confirmed zero in prior Unity survey
- gear_catalogue_id = 15 (War-Trumpet / Horn) — confirmed zero in prior Unity survey
- Any (non-european, non-east_asian) cultural_lineage for any gear_catalogue_id
- gear_catalogue_id = 7 (Blunderbuss) — thin coverage in fantasy libraries

**Estimated cost per gap-fill:** Meshy Pro subscription ($30/month); generation within
subscription limits; $0 marginal cost per model.

**Estimated total gap-fill volume (post-Phase C):** Based on 315 substrate regions and
Phase C coverage estimates, expected ~80–120 empty/sparse regions requiring gap-fill.

---

## 5. Cross-Phase Timeline Summary

| Phase | Libraries | Est. weeks | Est. weapons added | Cumulative total |
|---|---|---|---|---|
| A (schema + seed) | Kenney | 1–2 | 150–250 | 150–250 |
| B (bulk API) | Sketchfab + Meshy | 2–4 | 3,500–5,000 | 3,650–5,250 |
| C (aesthetic expansion) | OGA + Smithsonian + itch.io | 2–3 | 420–980 | 4,070–6,230 |
| D (gap-fill; ongoing) | Meshy generated | ongoing | 80–120 generated | 4,150–6,350 |

**Total target:** 4,000–6,500 weapons in DB after Phase D initial gap-fill.

---

## 6. Estimated Import Compute and Cost

| Phase | Estimated compute | Wall-clock elapsed | Cost |
|---|---|---|---|
| A | 2–4 hours | 1–2 weeks | $0 |
| B | 12–24 hours | 2–4 weeks | $0 |
| C | 6–12 hours | 2–3 weeks | $0 |
| D (initial) | 4–8 hours generation time | 1–2 weeks | $0 (Meshy Pro subscription) |
| **Total** | **24–48 hours compute** | **7–11 weeks** | **$0** |

Tier 3 targeted gap-fill (if needed): additional compute + per-model procurement cost
from TurboSquid/CGTrader; estimated $50–$200 for 20–40 specific high-value models if
Meshy cannot achieve satisfactory quality for certain substrate regions.

---

## 7. 15-Gear Catalogue vs. Vast Library — Validation

The dispatch context notes that under vast-library framing, the 15-gear catalogue entries
"likely emerge as natural clusters in imported data rather than being pre-imposed." This
commission's findings partially validate and partially complicate this framing:

**Validates:** Libraries naturally cluster on the functional weapon taxonomy. Sketchfab,
Meshy, OGA all have weapon_class distributions that map cleanly to the 15-gear catalogue.
Swords/greatswords, bows, staves, daggers all appear as discrete import clusters with
no forcing required.

**Complicates:** Three catalogue entries (Censer, Holy Symbol, War-Trumpet) have zero
natural presence in any surveyed library — the prior Unity survey confirmed this and it
is consistent with the broader web search. These are not "naturally emerging clusters"
in any 3D library; they are game-design-specific weapon abstractions. They require
Meshy gap-fill by construction, regardless of library scale.

**Implication for gandalf:** The 15-gear catalogue is NOT fully derivable from library
imports. The 12/15 entries that do have library presence will emerge as natural clusters;
the 3 ritual archetypes are design-specific and need the Meshy gap-fill layer as a first-class
substrate source, not a fallback. The vast-library framing is accurate for the melee/ranged/caster
gear families (12 archetypes); the ritual family (3 archetypes) remains hand-curated via Meshy.

---

**Signed (research):** legolas (research scout; Mode A analytical recommendation)
**For:** Matt approval of import strategy + license-tier policy; knight-rider (dispatch sequencing
for phases A–D); rocket (W1.15 import pipeline implementation); gandalf (canonical doc authoring
on vast-library framing + ritual archetype exception).
