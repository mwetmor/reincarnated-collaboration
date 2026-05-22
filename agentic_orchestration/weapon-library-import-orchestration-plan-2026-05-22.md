# Weapon Library Import — Orchestration Plan for Knight-Rider + Hive

**Date:** 2026-05-22 (evening; teed up for tomorrow's knight-rider session)
**Author:** gandalf (planner; not orchestrator — knight-rider owns execution sequencing)
**For:** knight-rider (orchestrator) + hive specialists (legolas, rocket, galadriel, drax)
**Authority:** Matt 2026-05-22 evening — explicit "tee up for knight-rider and the hive mind. This is structural work."
**Estimated duration:** 1-3 weeks across phases; longer if Meshy bulk path requires partner outreach + onboarding
**Discipline:** #19 RATIFIED 2026-05-22 — all long-running phases as background processes; no Agent-tool monitoring; status via direct Bash + DB queries; JSON summary artifacts as cross-session continuity

---

---

## 🎯 COMPLETENESS MANDATE — 2026-05-22 LATEST (Matt principled directive)

**"I do NOT want to leave a single weapon un-turned."**

Per Matt 2026-05-22 latest evening directive: **finding all the weapons is the single gate removal that lets this engine fulfill its design principle of coherence and distinctness engine for serial content production.**

The 15-30K estimate from prior re-plan is the FIRST-PASS BASELINE, not the target. The target is COMPLETENESS across all weapon-knowledge repositories — real-world historical + TTRPG mechanical + video game canon + anime/manga + movie/TV + folklore/mythology + speculative fiction.

**Why this is structural, not nice-to-have:**

If the imported substrate covers only English-language Wikipedia + major Fandom-hosted game wikis (the easy-to-crawl sources), the substrate is biased toward Western-fantasy-ARPG canon. Pattern 6 axis discovery on this biased subset will discover Western-fantasy-ARPG-shaped axes. Coherence + distinctness as engine output will reflect that bias permanently.

Completeness across cultures + periods + genres + media types is what makes substrate-as-cohesion genuinely culture-and-genre-agnostic at the architectural level. **Pictures are optional** — knowledge entries without images can be loaded later via gap-fill or matched against the eventual ChatGPT/Meshy generation pipeline. The completeness gate is on the KNOWLEDGE coverage, not the visual coverage.

**Real "every weapon" scope (realistic):**

| Category | Estimated count | Source families |
|---|---|---|
| Real-world historical weapons | 5,000-20,000 | Wikipedia (multi-language); Wikidata; museums (Royal Armouries / Met Museum / Smithsonian / Hermitage / British Museum / Tokyo National / Cairo Museum / INAH); academic archaeology databases; specialty references (Stone's Glossary; Oakeshott typology; Asian weapon catalogues; African weapon archives; Mesoamerican atlatl databases) |
| TTRPG mechanical weapons | 2,000-5,000 | D&D SRD (3.5e + 5e); Pathfinder; GURPS; Savage Worlds; Warhammer 40K + Fantasy; Shadowrun; Cyberpunk RED; lesser-known systems |
| Video game weapons | 10,000-30,000 | PoE wiki; D2/D3/D4 wikis; Last Epoch; Grim Dawn; Dark Souls / Elden Ring series; Monster Hunter (all); WoW; FFXIV; ESO; Skyrim wiki; FF series wikis; Mass Effect; Borderlands; modern indie ARPGs |
| Anime/manga weapons | 5,000-15,000 | Bleach (zanpakutō); Demon Slayer (nichirin); SAO; One Piece; Naruto; Fate series; Berserk; Vagabond; isekai-genre wikis broadly |
| Movie/TV weapons | 2,000-5,000 | IMFDB; LOTR wikis; Star Wars wikis; Star Trek wikis; Marvel; DC; etc. |
| Folklore + mythology | 200-500 | Wikipedia mythology categories; specific traditions (Norse, Greek, Egyptian, Hindu, Japanese, Celtic, Mesopotamian, etc.) |
| Speculative fiction | 1,000-3,000 | Sci-fi novel weapons; fantasy novel weapons; lesser-canonical works |
| **TOTAL realistic completeness target** | **25,000-78,000** | |

This is achievable through structured multi-pass crawls + targeted gap-fill, NOT overnight in one pass.

**Multi-pass strategy:**

| Pass | Scope | Owner |
|---|---|---|
| **First-pass (running tonight)** | Big-name sources: Wikipedia (English) + Wikidata + top 8-10 game wikis + D&D 5e SRD + Smithsonian + TVTropes + IMFDB + top anime wikis. ~15-30K entries baseline. | knight-rider (running) |
| **Second-pass (tomorrow+)** | Multi-language Wikipedia (Japanese; Chinese; Spanish; French; German — capture culture-specific weapons); additional game wikis (Final Fantasy series; ESO; Skyrim; Mass Effect; Borderlands; etc.); additional TTRPG SRDs (Pathfinder; GURPS; Warhammer); additional anime/manga wikis | knight-rider tomorrow |
| **Third-pass (mid-week)** | Museum collections (Royal Armouries; Met Museum; Hermitage; British Museum; Tokyo National; etc. via their open data APIs); specialty academic references (Stone's Glossary; Oakeshott typology if digitized) | knight-rider |
| **Fourth-pass (gap-fill)** | After Pattern 6 axis discovery on first 3 passes' data reveals coverage gaps (cultures/regions/genres underrepresented); targeted crawls for gap regions | gandalf + Matt + knight-rider |
| **Manual curation pass** | Edge cases that crawls can't reach (specific folklore weapons; legendary weapons; lesser-known fiction); gandalf + Matt designer reviews + manual entries | gandalf + Matt |

**Acceptance criteria for completeness:**

- ≥50K weapon knowledge entries indexed (target lower bound; ideal 75K+)
- ≥10 distinct cultural lineages represented (European; East-Asian; South-Asian; Mesoamerican; African; Middle-Eastern; Pacific; Arctic; Mesopotamian; fictional-hybrid; etc.)
- ≥6 distinct historical periods (prehistoric; ancient; medieval; early-modern; industrial; modern; post-singularity-fictional)
- ≥8 distinct genre-canons (historical; D&D-fantasy; ARPG-canon; isekai; sci-fi; superhero; horror; comedic)
- Wikidata Q-item coverage: ≥80% of all weapon-tagged Q-items imported
- Major game wikis: ≥90% of weapon-page coverage per top-10 wikis

**Pictures are optional** at completeness check; knowledge coverage is the gate. Image gap-fill happens later.

**Knight-rider extension message sent** (per same conversation; knight-rider's running commission expanded to incorporate completeness mandate; tomorrow's knight-rider session takes over after first-pass completes).

### Image Download — Descriptor-Gated Decision Pass (Matt 2026-05-22 latest)

Per Matt 2026-05-22 latest evening: **Pass 1 captures image URLs + license metadata; an explicit downstream pass evaluates each image and decides whether to download based on descriptors.** This is storage-aware, license-aware, quality-aware procurement — not bulk-download-everything.

**The decision logic per image** (post-Pass-1; runs as a separate dispatch):

```
For each row in knowledge_entry_reference_images:
  IF license_class IN ('GPL', 'CC-BY-NC', 'restricted', 'unknown'):
    SKIP — license incompatible with our intended use; flag for legal review
  ELIF width_px < 256 OR height_px < 256:
    SKIP — resolution too low for reference-image quality validation
  ELIF descriptor_relevance_score < 0.5:
    SKIP — image descriptor doesn't match weapon entry well enough
  ELIF NOT is_canonical AND existing_canonical_count_for_entry >= 1:
    SKIP — entry already has canonical; this is supplementary; defer to bandwidth pass
  ELIF storage_used_total > storage_budget:
    SKIP — over budget; flag for review
  ELSE:
    DOWNLOAD — fetch image_url with attribution credit if CC-BY*; store local_path; update row
```

**Descriptor-relevance score** computed by:
- Image caption text similarity to weapon canonical_name (embedding-based; threshold ~0.5)
- Image source authority weight (museum > game wiki > fan upload)
- Image age/freshness (newer is preferred for game-canon; older is preferred for historical-authenticity)

**License-tier policy:**

| License | Download? | Use? |
|---|---|---|
| CC0 | YES | Free use including commercial; no attribution required |
| CC-BY | YES | Free use with attribution; auto-generate attribution credit |
| CC-BY-SA | YES (download); CONDITIONAL (use) | Download for reference; check share-alike compatibility before commercial use (per CC-BY-SA legal review carry) |
| Public Domain | YES | Free use; museum metadata note recommended |
| Fair-use (TVTropes-style) | NO download | Reference only; never redistribute |
| Restricted / unclear | NO download | Flag for legal review |
| GPL / proprietary | NO download | Incompatible |

**Storage budget — REVISED (Matt 2026-05-22 latest):**

The original ~30-35GB full-canonical-download estimate is too much disk pressure for a dev machine. Phased approach instead:

| Phase | Approach | Disk cost | When triggered |
|---|---|---|---|
| **v1 default** | **URL-only**; capture metadata; fetch on-demand for any picture-use | **0 GB** | Starting state — no automatic download |
| **v1 thumbnail cache (if needed)** | Download canonical-image thumbnails (256x256-512x512, ~50KB each × 50K = ~2.5GB); embeddings computed on thumbnails; full-res still URL | ~2.5 GB | If URL-only on-demand fetching becomes workflow bottleneck (>12hr clustering pass; designer-review latency etc.) |
| **v1.1+ archival** | Selective full-res download of CC0/CC-BY canonical images only (~10-15GB of license-clean assets) | ~10-15 GB | Long-term substrate stability (link-rot insurance); not v1 concern |

**Why URL-only is the v1 default:**

- Pattern 6 axis discovery embedding extraction works on URL-fetched-then-discarded thumbnails (cheap; one-time cost per weapon)
- Cluster post-labeling visual inspection works via gallery-thumbnail + URL click-through
- ChatGPT image-gen prompt reference accepts URL pass-through (no local file needed)
- Galadriel visual-similarity validation fetches on-demand at validation time
- Engine never displays reference images (dev-time tooling only)

**Engine never needs reference images locally.** Reference images are dev-time validation + Pattern-6-axis-discovery tooling. Runtime engine consumes the converged weapon-model output (3D meshes via Unity), not reference photos.

**Storage path (when downloads do happen):**
`~/Games/reincarnated-loadout/data/weapon_reference_images/<source_library>/<weapon_id>/<image_hash>.<ext>`

**This download pass becomes a separate dispatch** authored when Pass 1 completes:

| Dispatch | Owner | When |
|---|---|---|
| **D-IMG-DOWNLOAD** | knight-rider next session (or rocket if treated as engine-side ETL) | After Pass 1 completes; reads `knowledge_entry_reference_images` table; applies descriptor-gated decision logic; downloads selectively |
| Duration | 4-8 hours background process | Per-image fetch with rate-limit + license-attribution + checkpoint |
| Discipline #19 | OS-level background; JSON summary artifact; resume-on-failure via downloaded-list checkpoint | Per canonical pattern |

**Agents can make the decision autonomously** based on the descriptor logic above; Matt holds gate on bulk legal-review cases (CC-BY-SA commercial; restricted-unclear). Default policy is permissive on CC0/CC-BY; conservative on CC-BY-SA/fair-use.

Note: the field naming above is illustrative; the actual schema column names follow what legolas already designed plus the `descriptor_relevance_score` field which may need adding.

---

## ⚠️ MAJOR RE-PLAN — 2026-05-22 LATE EVENING (Matt correction)

**The prior plan (below this re-plan section) targeted 3D MODEL libraries as primary substrate. That was wrong-target.** Matt's actual ask, clarified late evening: **deep weapon knowledge data** (text + structured properties + cultural/historical/genre context) is the primary substrate Pattern 6 axis discovery wants. 3D models become *visual reference attachments* to knowledge entries, not the primary substrate.

**Knowledge sources (PRIMARY; re-planned Track A):**

| Source | Format | Crawl viability | Estimated entries |
|---|---|---|---|
| **Wikipedia weapons categories** | REST API; structured infoboxes | Documented; crawler-friendly | ~5,000-15,000 entries |
| **Wikidata weapon Q-items** | SPARQL endpoint; CC0 | Documented; ideal | ~2,000-5,000 entries with rich property graphs |
| **Game wikis (Fandom-hosted)** | MediaWiki API per wiki | Crawler-friendly (verify per-wiki robots.txt) | ~2,000-10,000 across PoE/D3/D4/Last Epoch/Dark Souls/Monster Hunter/WoW/Bleach/SAO |
| **D&D / Pathfinder SRD** | Open Game License; static | Free; documented | ~100-200 weapons with rich mechanical taxonomy |
| **Royal Armouries / Met Museum / Smithsonian** | Various open APIs | Open data; museum-grade | ~5,000-10,000 historical weapons |
| **TVTropes weapon tropes** | Crawler-friendly; CC-BY-SA | Verify robots.txt | Fictional-genre taxonomy enrichment |
| **IMFDB** (Internet Movie Firearms Database) | Crawler-friendly | Verify robots.txt | Movies/TV weapon canon |
| **Anime/manga weapon wikis** | Mostly Fandom-hosted | Crawler-friendly | Isekai-relevant substrate enrichment |

**Total realistic target: ~15,000-30,000 weapon knowledge entries** with rich textual + structured property data. ~50-200MB of substrate data.

**Pattern 6 axis discovery operates on knowledge features.** Discovered axes (from PCA / factor analysis on knowledge-feature vectors) will be substantive: edged-vs-blunt; one-vs-two-handed; melee-vs-projectile; cultural-lineage; historical-vs-fictional; ceremonial-vs-utility; genre-anchored. These are real substrate dimensions, not "long-vs-short" geometric artifacts.

**3D model libraries (SECONDARY; original plan; reframed Track B):**

Sketchfab + Kenney + OGA + Smithsonian models become VISUAL REFERENCE ATTACHMENTS to knowledge entries (many-to-many: one knowledge entry may have N model references; one model may render N knowledge entries). The original 11-dispatch plan below (D1-D11) still applies for Track B but at REDUCED PRIORITY.

**Phase D Meshy generation gap-fill becomes the canonical visual pipeline** when knowledge entries lack model coverage:

```
Weapon knowledge entry (rich text + properties)
   ↓
ChatGPT image-gen (prompted from knowledge data; T-pose-isolated; plain background; per canonical character-image specs adapted for weapon-props)
   ↓
Meshy image-to-3D (mesh + PBR textures)
   ↓
Meshy rigging+animation (if needed; most weapons are static-attach)
   ↓
Unity assembly (parented to RightHand bone; VFX attached per canonical galadriel § 8 rules)
```

This is the SAME pipeline already validated for characters (Canary work earlier today); adapted for weapons.

**Schema additions needed:**

```sql
-- Knowledge repository (PRIMARY substrate)
CREATE TABLE weapon_knowledge_entries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  canonical_name TEXT NOT NULL,                      -- "Katana", "Hammerdin Concentration Hammer", etc.
  source_library TEXT NOT NULL,                       -- "wikipedia" / "wikidata" / "poe-wiki" / "smithsonian" / etc.
  source_url TEXT NOT NULL,                           -- canonical entry URL
  source_id TEXT,                                     -- library-specific ID
  description_text TEXT,                              -- main entry text
  structured_properties JSON,                         -- infobox/property data (period, country, length, weight, etc.)
  cultural_lineage_tags JSON,                         -- free-text array (from structured fields where available)
  historical_period TEXT,
  genre_appearances JSON,                             -- array: "historical", "fantasy", "sci-fi", "anime", etc.
  related_entries JSON,                               -- canonical_names of related/derived weapons
  license_class TEXT,                                  -- per-source license (CC-BY-SA for Wikipedia; CC0 for Wikidata; etc.)
  imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  -- Pattern 6 features (post-import pass)
  text_embedding BLOB,                                 -- sentence-transformer / similar
  structured_feature_vector BLOB,                      -- numeric properties as vector
  derived_axis_loadings BLOB,                          -- post-axis-discovery
  cluster_id INTEGER REFERENCES clusters(id)
);

-- Join table: knowledge ↔ models
CREATE TABLE knowledge_model_attachments (
  knowledge_entry_id INTEGER REFERENCES weapon_knowledge_entries(id),
  weapon_id INTEGER REFERENCES weapons(id),  -- the existing weapons table (3D models)
  attachment_confidence REAL,                 -- 0-1; how well does this model match this knowledge entry?
  attachment_source TEXT,                     -- "manual" / "name-match" / "embedding-similarity" / "post-Meshy-gen"
  PRIMARY KEY (knowledge_entry_id, weapon_id)
);

-- Canonical entry merging across sources
CREATE TABLE knowledge_entry_canonical_merge (
  canonical_id INTEGER PRIMARY KEY AUTOINCREMENT,
  canonical_name TEXT NOT NULL UNIQUE,
  merged_entry_ids JSON,                       -- array of weapon_knowledge_entries.id merged into this canonical
  merge_strategy TEXT,                          -- "name-exact-match" / "synonym-resolution" / "manual"
  merge_confidence REAL
);
```

**Updated overnight cascade (3 parallel tracks):**

| Track | Owner | Scope | Status |
|---|---|---|---|
| **A — Knowledge Crawls (PRIMARY)** | knight-rider orchestrating; legolas executing | Wikipedia + Wikidata + game wikis + SRD + museum data; per-source robots.txt verification first | Authorized; fires after re-plan commit |
| **B — 3D Model Imports (SECONDARY)** | knight-rider orchestrating; legolas executing | Sketchfab + Kenney + OGA (pending OGA robots.txt); attached to knowledge entries via name-match where possible | Authorized; fires after Track A starts |
| **C — Canonical Doc Authoring** | gandalf sub-agent | Six vestigial-pattern audit doc + stat-derivation doc + gear-heavy-promotion doc + hive-mind-protocol elevation | Authorized; fires in parallel |
| **D — Discipline #20 Authoring** | jack-ryan | robots.txt + Claude-agent directive respect canonical discipline | Authorized per Matt overnight fire-cascade approval |

**Pre-flight check additions:**

| # | Check | What |
|---|---|---|
| P0.8 | Per-source robots.txt verification | For EACH crawl target: fetch `robots.txt`; verify `User-agent: ClaudeBot` and `User-agent: anthropic-ai` are NOT Disallow-listed; if blocked, source routes to non-Claude implementation or skip |
| P0.9 | Per-source TOS check | For each source: fetch ToS; verify automated-research-access compatible (Wikipedia/Wikidata are explicit OK; Fandom-hosted wikis generally OK; museum APIs are explicit OK; TVTropes worth checking; IMFDB worth checking) |

### MEMO FOR LEGOLAS — prioritize sources with reference images (Matt 2026-05-22 late evening)

**Why this matters:** later in the pipeline, we'll generate weapon visuals via ChatGPT image-gen → Meshy mesh-gen. We need **reference images for validation** — to check whether our generated output matches authoritative reference photos. Without these, we have no quality validation loop for the gap-fill visual pipeline.

**Most knowledge sources have images already; capture them as first-class data:**

| Source | Image availability | What's captured |
|---|---|---|
| **Wikipedia** | Almost always; Commons-licensed (CC-BY-SA / CC0 / PD) | Main infobox image; gallery images; per-section illustrations |
| **Wikidata** | Property P18 (`image`) links to Commons | Single canonical image per weapon Q-item |
| **Wikimedia Commons** | Direct image repository; license metadata structured | Multiple-angle photos when available |
| **Smithsonian / Royal Armouries / Met Museum** | Museum-grade photos with structured metadata | High-quality reference photos; CC0 or public-domain in most cases |
| **Game wikis (Fandom-hosted)** | In-game weapon renders / item icons / 3D viewer captures | Per-weapon visual identity; rendered in-game-canon style |
| **D&D Beyond / Pathfinder SRD** | Illustration art per weapon entry | Stylized fantasy renders; CC-BY for SRD subset |
| **TVTropes** | Example images per weapon-trope page | Mixed; usually fair-use stills |
| **IMFDB** | Movie/TV screenshots showing weapons in context | Usage examples; fair-use stills |
| **Anime/manga wikis** | Character holding weapons; canonical art | Genre-canonical visual references |

**Schema addition required** (legolas applies in Track A schema authoring):

```sql
-- Reference image attachment per knowledge entry
CREATE TABLE knowledge_entry_reference_images (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  knowledge_entry_id INTEGER REFERENCES weapon_knowledge_entries(id),
  image_url TEXT NOT NULL,
  image_source TEXT,                          -- "wikipedia-infobox" / "wikidata-p18" / "fandom-render" / "museum-photo" / etc.
  license_class TEXT,                          -- CC0 / CC-BY-SA / PD / fair-use / etc.
  is_canonical BOOL,                           -- 1 if this is the primary/canonical reference; 0 otherwise
  image_caption TEXT,
  image_local_path TEXT,                       -- post-download (NULL if remote-only)
  width_px INTEGER,
  height_px INTEGER,
  imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_reference_image_entry ON knowledge_entry_reference_images(knowledge_entry_id);
CREATE INDEX idx_reference_image_canonical ON knowledge_entry_reference_images(knowledge_entry_id, is_canonical);
```

**Acceptance criteria for Track A crawl (per legolas)**: ≥70% of knowledge entries with at least one reference image; ≥30% with canonical (primary) image marked; license metadata captured per image.

**Downstream use case (Phase D Meshy gap-fill validation loop):**

```
Reference images for weapon knowledge entry
    ↓ (used as visual ground truth)
ChatGPT image-gen produces synthetic weapon image
    ↓ (comparison: galadriel visual-similarity scoring)
PASS → feed to Meshy image-to-3D
FAIL → re-prompt ChatGPT with adjusted parameters; iterate
    ↓
Meshy 3D mesh
    ↓ (comparison: galadriel preview-image similarity to reference)
PASS → ready for Unity assembly
FAIL → re-iterate or route to alternative source
```

This validation loop is the canonical answer to "how do we know Meshy generation produced the right katana?" — we compare against authoritative reference photos captured during Track A. Without reference images, we have no objective quality signal.

**This memo becomes a Track A acceptance criterion.** Knowledge entries WITHOUT reference image coverage rank lower in cluster confidence and route to manual review.

### FIELD EXTRACTION COMPLETENESS SPEC — read by EVERY agent doing weapon-knowledge crawls (Matt 2026-05-22 latest)

**META RULE:** Capture every available field per source. If a field doesn't have an explicit column in `weapon_knowledge_entries`, add it to the `structured_properties` JSON blob with the source's native field name. **Every piece of data is potential Pattern-6-axis-discovery fuel.** Bias toward MORE fields, not fewer. A 50-field entry is better than a 5-field entry. A 100-field entry is better than 50.

**Anti-pattern (DO NOT DO):** "Extract canonical_name + description + image_url and move on." That's the 3-column failure mode. Pattern 6 axis discovery on 3 fields produces ~2-3 axes that won't span the substrate space meaningfully.

**Correct pattern:** Extract everything the source exposes. Map known fields to schema columns where defined; dump everything else into `structured_properties` JSON. Future axis-discovery work can mine the JSON for additional features without re-crawling.

---

#### Per-source field-extraction checklists

**Wikipedia (weapons category articles):**

Infobox fields (most articles have ~15-30 of these):
- `name`, `image_caption`, `type`, `place_of_origin`, `service_period`, `used_by`, `wars`, `designer`, `design_date`, `manufacturer`, `production_date`, `number_built`, `unit_cost`, `variants`
- `weight`, `length`, `barrel_length`, `width`, `height`, `crew`, `caliber`, `barrels`, `action`, `rate_of_fire`, `velocity`, `effective_range`, `maximum_range`, `feed`, `sights`
- For melee: `blade_length`, `blade_type`, `hilt_type`, `grip_type`, `pommel_type`, `crossguard_type`, `handed`, `edge_count`, `point_type`
- For ranged: `projectile`, `propellant`, `arrow_head_type`, `bow_type`, `draw_weight`
- Cross-references: `related_weapons`, `predecessor`, `successor`

Article body text:
- Lead paragraph (definition + dominant context)
- History section (period + cultural context + evolution)
- Design section (mechanical + material specifics)
- Variants section
- In popular culture section (genre appearances)
- See also section (related entry links)
- Categories (Wikipedia category tags — explicit taxonomy signals)
- Cross-language links (per-language Wikipedia versions — culture-specific context)

Section structure metadata:
- Article length
- Section count
- Reference count
- Edit count / page age (proxies for canonical-ness)
- Languages available (proxy for cross-cultural significance)

---

**Wikidata (weapon Q-items):**

Every available property. The high-value properties for axis discovery:

- `P31` (instance of) — which weapon-class Q-items
- `P279` (subclass of) — hierarchical taxonomy
- `P18` (image) — Commons image URL
- `P27` (country of origin)
- `P176` (manufacturer)
- `P186` (material)
- `P571` (inception date / period start)
- `P576` (dissolution date / period end)
- `P5008` (on focus list of Wikimedia project) — encyclopedia-canonicity proxy
- `P361` (part of) / `P527` (has part) — composition
- `P138` (named after)
- `P1535` (used by) — wielders / military units / classes
- `P607` (conflicts) — wars / battles
- `P2048` (height) / `P2049` (width) / `P2067` (mass) — dimensional properties
- `P462` (color)
- `P462` (material)
- `P101` (field of work)
- `P31` family — all hierarchical classifications
- `P460` (said to be the same as) — synonym/canonical-merge candidates
- `P937` (work location)
- `P189` (location of discovery, for archaeological weapons)
- `P195` (collection, for museum-held weapons)

Plus: ALL labels in ALL languages (en, ja, zh, es, fr, de, ar, ru, ko, hi, pt at minimum). Cross-language label coverage is itself an axis.

---

**Wikimedia Commons (image metadata):**

For every reference image identified:
- File URL + dimensions + format
- License (CC0 / CC-BY / CC-BY-SA / PD)
- Author / uploader
- Source description / caption
- Categories the image is in (Commons categorization tags)
- Date created
- EXIF if present (camera; lens; etc. — quality signals)

---

**Game wikis (Fandom-hosted: PoE / D2 / D3 / D4 / Last Epoch / Dark Souls / Elden Ring / Monster Hunter / WoW / FF series / etc.):**

Per-weapon stats:
- Weapon name + canonical name in-game
- Weapon class / type / category (game-specific taxonomy)
- Base damage (single value OR min-max range)
- Damage types (physical / fire / cold / lightning / poison / etc. — per-game)
- Attack speed / cast time / cooldown
- Crit chance / multiplier
- Range / area-of-effect
- Required level
- Required stats (STR/DEX/INT/etc.)
- Item rarity / tier
- Sockets / mod slots
- Implicit modifiers
- Possible explicit modifiers
- Unique modifiers (for unique weapons)
- Set membership
- Drop sources / vendors
- Recipe / crafting requirements
- Patch introduced / patch changes
- Comparable weapons

Per-weapon flavor/lore:
- Flavor text / lore description
- In-game character associations
- Quest / story relevance
- Visual description (color; size; ornamentation cues)
- In-game preview image / icon URL

Meta data:
- Wiki page edit count (canonical-ness proxy)
- Comments count (community attention proxy)
- Cross-references to related weapons / build guides

---

**Anime/manga wikis (Fandom-hosted: Bleach / Demon Slayer / SAO / One Piece / Fate / Berserk / etc.):**

Per-weapon entry:
- Weapon name (original-language + romanized + translated)
- Wielder character(s) — primary + secondary
- First appearance (chapter/episode + arc/saga name)
- Weapon type (zanpakutō / nichirin-blade / sacred-treasure / etc. — series-specific)
- Power/ability description (multi-paragraph; the "ban-kai" / "true form" etc.)
- Origin story / how-acquired
- Special techniques / named-attacks list
- Material / components / forging-method
- Symbolic meaning / character-arc significance
- Visual descriptors (color; pattern; size; ornamentation)
- Power-tier ranking (within-series strength comparison if available)
- Cross-references to wielder character entries

---

**Museum collections (Smithsonian / Royal Armouries / Met / Hermitage / British Museum / Tokyo National / Cairo / INAH):**

Per-artifact:
- Catalog ID + collection name
- Object name (curator-assigned)
- Culture (structured field — this is the load-bearing one)
- Period / dating + dating method
- Geographic origin (region + specific site if archaeological)
- Material composition
- Dimensions (length, width, depth, weight)
- Provenance / acquisition history
- Curator description (multi-paragraph contextual text)
- Image URLs (museum-photo + multi-angle when available)
- License (mostly CC0 for U.S. federal museums; varies for others)
- Related-objects cross-references within the same collection
- Bibliographic references / academic citations

---

**TTRPG SRDs (D&D 5e / Pathfinder / GURPS / Warhammer / etc.):**

Per-weapon entry:
- Name + category (Simple / Martial / Exotic / etc.)
- Damage dice + damage type
- Properties (versatile / finesse / two-handed / heavy / light / loading / reach / thrown / etc.)
- Weight + cost (in-game currency)
- Special rules / mechanical interactions
- Cultural-flavor description text
- Edition/version (3.5e / 5e / etc.)

---

**TVTropes weapon-tropes:**

Per-trope page:
- Trope name
- Description text
- Per-example weapon mentions (across media)
- Genre tags
- Sub-tropes / parent tropes (hierarchical)
- Cross-references to other tropes

---

**IMFDB (Internet Movie Firearms Database):**

Per-weapon entry:
- Weapon name (real-world canonical)
- Manufacturer / model details
- Real-world specs (caliber / capacity / etc.)
- Films/TV-shows it appears in (with character/scene references)
- Image URLs from movie screenshots
- Historical accuracy notes

---

#### Default-extraction-rule (FOR EVERY SOURCE)

If you encounter a field not in the per-source checklist above, **CAPTURE IT TO `structured_properties` JSON BLOB anyway** with the source's native field name. The checklists are minimum coverage, not maximum. Source-specific fields (like Smithsonian's `creator_role` or Wikipedia's `category` lists) become valid axis-discovery features even if not enumerated above.

#### Acceptance criteria for field-extraction completeness

Per knowledge entry:
- **Minimum: 15 populated fields** (description + 14 structured properties / metadata fields)
- **Target: 30+ populated fields** for sources with rich infoboxes (Wikipedia / Wikidata / major game wikis)
- **Aspirational: 50+ populated fields** for museum-held artifacts with full curatorial metadata

Per source-library aggregate:
- Per-source coverage statistic: mean field-count per entry; flag sources whose mean < 10 for re-crawl with enhanced field extraction
- Cross-source canonical merging: when merging entries across libraries (e.g., "katana" in Wikipedia + Wikidata + Smithsonian + multiple game wikis), unify into single canonical entry with union of all captured fields. Multi-source provenance preserved.

#### Rationale — why this matters for Pattern 6 axis discovery

PCA / factor analysis on N features per weapon produces meaningful axes ONLY if N is large enough to span the substrate space. With ~3-5 features per weapon, you discover maybe 2-3 axes. With ~30-50 features per weapon, you discover 8-15 meaningful axes that span culture × period × mechanics × genre × scale × material × use-context × tactical-role.

**Bias toward MORE during extraction.** Storage cost is trivial (JSON blobs are flexible). Axis-discovery cost of UNDER-extraction is permanent — you'd have to re-crawl every source to add fields later.

**Original plan below this section remains as Track B reference (3D model import workstream); it is not deleted but it is no longer primary.**

---

## 0. TL;DR (ORIGINAL — SUPERSEDED BY RE-PLAN ABOVE; KEPT AS TRACK B REFERENCE)

Build out the **gear-substrate** as a vast queryable weapon library populating the greenfield SQLite DB at `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`. Sequence eleven dispatches across five operational phases. Final-state output: ~2,000-6,500 weapons indexed with rich metadata (mechanical properties + descriptive tags + source provenance + BDI ω-scores), clustered into emergent gear-substrate groups, semantically labeled by gandalf + Matt for player-facing thematic identity, ready for engine consumption via substrate-vector queries.

**Key sequencing constraints:**

1. **Phase 0 (schema lock) blocks all others** — DB must have tables before imports run
2. **Phase 1 imports run in parallel** — different libraries; no contention
3. **Phase 2 (BDI ω seeding) must complete before Phase 3 clustering** — clustering uses ω-scores as features
4. **Phase 4 (cluster naming) requires Matt + gandalf design call** — not automatable
5. **Phase 5 (validation) runs after cluster_id populated** — galadriel visual-coherence + rocket substrate-density precomputation

**Critical decision gate at Phase 1 start:** Meshy API probe outcome determines whether Phase 1A (Meshy bulk) is API-driven enumeration, API-driven scrape-with-auth, or skipped entirely (use Meshy only for Phase D generation gap-fill). Resolve via probe BEFORE knight-rider authors Phase 1A dispatch.

---

## 1. Pre-flight checks (knight-rider runs FIRST thing tomorrow)

Before authoring any dispatches, verify operational state:

| # | Check | How | Resolution path if failing |
|---|---|---|---|
| **P0.1** | `MESHY_API_KEY` env var persists across shell sessions | `echo "${MESHY_API_KEY:0:4}"` in a fresh terminal | Matt adds `export MESHY_API_KEY="..."` to `~/.zshrc`; re-source |
| **P0.2** | Meshy API probe — verify key auth + library endpoint availability | Probe script in `skill_handoff_2026-05-22-evening.md` § 6.1 | If library endpoints all 404: pivot Phase 1A to skip Meshy bulk (use generation API for Phase D only); if some 200s: pivot to API-driven enumeration |
| **P0.3** | DB greenfield state confirmed | `sqlite3 /Users/admin/Games/reincarnated-loadout/data/telemetry.db ".tables"` returns empty | If non-empty: matt-briefing — schema migration plan needed |
| **P0.4** | `schema.sql` ready at canonical path | `ls -la /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` | (already verified 562 lines 2026-05-22 evening) |
| **P0.5** | Smithsonian `api.data.gov` API key registered | Matt confirms; key in `SMITHSONIAN_API_KEY` env var (parallel to MESHY pattern) | Matt registers at https://api.data.gov/signup/ (free; takes ~5 min); blocks Phase 1E only |
| **P0.6** | CC-BY-SA legal review status | Matt confirms commercial compatibility status | If unclear: matt-briefing — `game_approved` flag stays `0` for CC-BY-SA pending; doesn't block Phase 1 |
| **P0.7** | Meshy partner-tier outreach status (per skill_handoff C3) | Matt confirms whether outreach email has been sent | Non-blocking; if response comes back during Phase 1 with library-browse access, pivot Phase 1A scope |

**P0.1 + P0.2 are blocking for Phase 1A.** Other P0 items have specific blocking scopes; resolve in parallel.

---

## 2. Phase-by-phase plan

### Phase 0 — Schema Lock + Cluster Table Amendment (D1)

**Owner:** knight-rider direct (operational; ~5 min)
**Dependencies:** P0.3, P0.4
**Duration:** ~5 min
**Discipline:** N/A (foreground operational)

**What it does:**

1. Amend `schema.sql` with `cluster_id` + `clusters` + `cluster_membership` table additions (per Pattern-5 vestigial retirement in skill_handoff § 1.2)
2. Run `sqlite3 /Users/admin/Games/reincarnated-loadout/data/telemetry.db < schema.sql` to create tables
3. Verify schema with `.schema` query
4. Commit the amended `schema.sql` to repo

**Cluster table amendment spec** (knight-rider hands to legolas if structural review needed first):

```sql
-- Adds to schema.sql (or amends existing weapons table)

ALTER TABLE weapons ADD COLUMN cluster_id INTEGER REFERENCES clusters(id);

CREATE TABLE clusters (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  label TEXT NOT NULL,                     -- semantic label assigned post-clustering (e.g., "Eastern-curved-blade-family")
  dominant_axes_description TEXT,          -- what makes this cluster distinct (free text per gandalf+Matt review)
  parent_cluster_id INTEGER REFERENCES clusters(id),  -- hierarchical clustering support
  cluster_algorithm_version TEXT,          -- tracks which clustering pass produced this cluster
  cluster_seed INTEGER,                    -- reproducibility
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cluster_membership (
  weapon_id INTEGER REFERENCES weapons(id),
  cluster_id INTEGER REFERENCES clusters(id),
  confidence_score REAL,                   -- 0.0-1.0; for multi-cluster membership cases
  PRIMARY KEY (weapon_id, cluster_id)
);

CREATE INDEX idx_weapons_cluster ON weapons(cluster_id);
CREATE INDEX idx_cluster_membership_cluster ON cluster_membership(cluster_id);
CREATE INDEX idx_cluster_membership_weapon ON cluster_membership(weapon_id);
```

**Acceptance criteria:**
- All 12 tables (9 original + 3 cluster tables) present per `.schema` query
- Compound index on `weapons(gear_catalogue_id, range_class, tech_level, cultural_lineage, readiness_state)` confirmed
- `substrate_density` precomputed table empty but ready
- Commit hash recorded in CHANGELOG

---

### Phase 1 — Library Imports (D2-D6; PARALLEL across sources)

**Owner:** legolas (primarily; possibly split across legolas + rocket for parallelism)
**Dependencies:** Phase 0 complete; P0.1+P0.2 resolved for D2
**Duration:** Variable per source (hours to days)
**Discipline:** #19 — ALL long-running imports are background processes; status via DB COUNT queries; JSON summary artifacts as final-act

**Five parallel sub-dispatches:**

#### D2 — Meshy Library Import (most variable; depends on P0.2 outcome)

| P0.2 outcome | D2 dispatch scope |
|---|---|
| **All library endpoints 404** | D2 is **deferred** entirely — Meshy stays in Phase D generation-only role; Phase 1 sources from D3-D6 only; Phase target shrinks to ~1,700-2,400 weapons |
| **Some 200s found** | D2 fires using discovered endpoints — API-driven structured enumeration; rate-limit-aware batching; ~hours runtime; resume-on-failure via DB checkpointing |
| **Partner outreach succeeded** | D2 fires using partner-tier endpoints; possibly higher scale |

**D2 dispatch template (knight-rider authors when probe outcome known):**

```
Target: import N weapons from Meshy library to weapons table
Subscope per weapon: model_id, title, description, tags (free-text array), 
  preview_url, download_url, mesh_format, license_class, author, dimensions,
  poly_count, raw_metadata_blob (full API response)
Rate limit: respect Meshy documented limits with exponential backoff
Checkpoint: after each batch of 100, write progress to DB + log
Resume: on restart, query MAX(meshy_model_id) from weapons WHERE source_library='meshy';
  resume from there
Background: nohup python scripts/meshy_import.py > logs/meshy_import.log 2>&1 &
Summary: logs/meshy_import_summary.json on completion (per Discipline #19)
```

#### D3 — Sketchfab Data API v3 Crawl

**Scope:** ~1,177 CC0+CC-BY weapons in weapons-military category per legolas's S3D3C dataset finding.

**Discipline #19 compliance:**
- Background process (`nohup` or `Bash(run_in_background=true)`)
- Sketchfab API has documented pagination; cursor-based; resumable
- Rate limits: respect documented thresholds
- Output: rows in `weapons` table with `source_library='sketchfab'`
- Summary: `logs/sketchfab_import_summary.json`

**Estimated duration:** 1-4 hours

#### D4 — Kenney Static Downloads

**Scope:** ~200-400 CC0 weapons from Kenney.nl asset packs.

**Approach:** Static ZIP download per asset pack; per-pack metadata in README files; manual-curation-light import script that walks downloaded ZIPs + extracts per-weapon metadata.

**Estimated duration:** 30-60 minutes (download + extract + import).

#### D5 — Open Game Art Crawl

**Scope:** ~389 OGA weapon entries (mixed CC0/CC-BY/OGA-BY/GPL — filter accordingly).

**Approach:** Predictable URL patterns; crawl with backoff + license-filter at import time; reject GPL + CC-NC.

**Estimated duration:** 1-2 hours.

#### D6 — Smithsonian Open Access (gated on P0.5)

**Scope:** ~100-400 weapons (precise count needs `api.data.gov` key); CC0 museum-grade with structured `culture` metadata field — **uniquely authoritative for non-European cultural_lineage population.**

**Approach:** Smithsonian Open Access API (api.data.gov); structured queries by object_type + culture; downloadable subset filtered by `online_media: True`.

**Estimated duration:** 1-2 hours after key registration (P0.5).

**Phase 1 total parallel duration:** depends on slowest-running import; likely 4-8 hours total wall time if D2 is API-driven; 2-4 hours if D2 is skipped.

---

### Phase 1.5 — Feature Extraction Per Weapon (D7a; FAST)

**Owner:** rocket (or legolas Mode A)
**Dependencies:** Phase 1 imports complete (or substantially — ≥80%)
**Duration:** 1-2 hours
**Discipline:** #1 (math-before-code on feature-extraction methodology) + #11 (empirical inspection on sample before full run)

**What it does:**

For each imported weapon, extract a wide feature vector. **No pre-imposed axes** — extract everything measurable:

| Feature class | Examples |
|---|---|
| **Geometric features** | poly count, dimensions (x/y/z), bounding-box aspect ratio, curvature estimates (where computable), ornamentation density (vertex distribution variance), symmetry score |
| **Visual features** | preview image embedding (vision-language model — e.g., CLIP-style); color palette histogram; perceptual visual-similarity vector |
| **Semantic features** | description text embedding; tag co-occurrence vector; subcategory one-hot |
| **Source metadata** | library origin, author, license_class, structured tags (Smithsonian `culture` field; Meshy subcategory) |
| **Computed mechanical estimates** | range estimate from geometry (long vs short); two-handed-likely vs one-handed; weight-class estimate |

Output: wide feature matrix stored as JSON blob on each `weapons` row OR in a separate `weapon_features` table.

### Phase 2 — Axis Discovery + BDI ω-Table Seeding Pass (D7b + D7c)

**Owner:** rocket (with legolas if statistical methodology research needed)
**Dependencies:** Phase 1.5 complete
**Duration:** 1-3 days (axis discovery is the variable-duration step)
**Discipline:** #1 (math-before-code — statistical methodology spec'd before run) + #11 (empirical inspection — interpret derived axes for soundness) + Pattern 6 honored (no axis pre-imposition)

**Sub-phase D7b — Statistical axis discovery (per Pattern 6; this evening's 6th vestigial retirement):**

Per Matt 2026-05-22 evening canonical call: **the aesthetic axes and the geometrical/mathematical mechanical variables must be DERIVED from a statistically significant sample, NOT pre-imposed.** This is the sixth vestigial-pattern retirement of the evening (categorical pre-imposition at the AXIS level).

Statistical methodology candidates:
- **PCA (Principal Component Analysis)** — linear; produces orthogonal axes explaining variance; interpretable when top components align with intuitive meaning
- **Factor Analysis** — identifies latent factors; more interpretable than raw PCA for semantic axes
- **UMAP / t-SNE** — non-linear; good for visualization + cluster prep but less interpretable as canonical axes
- **Sparse PCA / NMF** — produces sparse loadings; more interpretable axis-definitions
- **Mixed-effects: PCA on geometric/mechanical features + Factor Analysis on semantic/visual features** — separates axis-discovery for the two substrate halves

**Sample-size guidance:**
- PCA: minimum 5-10× sample per feature; for 50 features → 250-500 weapons minimum
- Factor analysis: minimum 200-300 for stable factor loadings
- **Recommended sample for stable axis discovery: 1,000-2,000 weapons** (achievable from D3-D6 alone; doesn't require D2 success)

**Output of D7b:**
- Discovered aesthetic axes (e.g., 4-8 principal components from visual+semantic feature analysis)
- Discovered mechanical axes (e.g., 4-8 principal components from geometric+source-metadata feature analysis)
- Per-axis interpretation (gandalf + Matt review the axis loadings; assign semantic labels)
- Replaces the pre-imposed `(tech_level / tone / cultural_lineage)` + `(range / geometry / timing / charge / accuracy / rhythm)` taxonomies with data-derived axis-sets

**Sub-phase D7c — BDI ω-table seeding (was Phase 2 in original plan):**

Now operates against the **derived axes** from D7b, not pre-imposed dimensions. Each weapon's ω-score per element is computed against the derived-axis basis vectors, not against the pre-imposed taxonomy.

Per-weapon: identify top-3 element affinities + record best ω-magnitude. Serialized into `dominant_element_affinities` JSON column.

**Why this matters now (not later):** clustering (Phase 3) uses the discovered axes as feature inputs. Without D7b, clustering operates on raw features (less interpretable) OR on pre-imposed axes (vestigial pattern survives).

**Acceptance criteria (D7b + D7c combined):**
- ≥1,000 weapons in sample (achievable from D3-D6)
- Discovered axes have ≥80% cumulative variance explained at top-8 components
- Axis interpretations gandalf + Matt-reviewed for soundness
- ω-scores populated per weapon

**What it does:**

Populate `dominant_element_affinities` + `best_omega_score` columns on `weapons` table from BDI ω-table per `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md`.

For each weapon row, compute ω-score against each of 7 elements (fire / water / earth / wind / lightning / holy / shadow):
- ω is the BDI mechanical-overlap measure between gear and element
- Per-weapon: identify top-3 element affinities + record best ω-magnitude
- Deserialized into `dominant_element_affinities` as JSON array `[{element, omega_score}, ...]`

**Why this matters now (not later):** per legolas's findings, `dominant_element_affinities` column MUST be seeded before Phase D (clustering) for density-routing-by-element to function correctly. Clustering uses ω-scores as one of its feature inputs.

**Acceptance criteria:**
- ≥99% of weapon rows have non-null `dominant_element_affinities`
- Sample inspection (gandalf reviews ~20 random weapons): ω-scores feel right (canonical pairings like holy+censer score high; novel pairings like holy+blunderbuss score low-but-positive)
- Summary: `logs/bdi_seeding_summary.json`

---

### Phase 3 — Clustering Analysis (D8)

**Owner:** legolas (Mode A analytical) OR rocket (if ML library access cleaner via rocket); decision at dispatch time
**Dependencies:** Phase 2 complete
**Duration:** 1-2 days (analytical research + multi-algorithm cluster pass + interpretation)
**Discipline:** #1 (math-before-code on clustering algorithm choice) + #11 (empirical inspection on cluster outputs before lock)

**What it does:**

Multi-dimensional clustering on the imported weapons. Feature space:
- **Mechanical properties:** range, geometry, timing, charge, accuracy, rhythm (canonical 6 dimensions)
- **BDI ω-scores per element:** 7 dimensions (per Phase 2 seeding)
- **Geometric features:** poly count, dimensions, ornamentation density (extractable from mesh metadata)
- **Semantic features:** tag/description embedding via vision-language model (preview image embedding + text embedding fusion)

**Algorithm options to evaluate** (per gandalf's prior conversation):
- Hierarchical clustering (cluster tree; multi-granularity)
- HDBSCAN (density-based; produces noise-points; good for catalogues with outliers)
- k-means with multiple k values (k=15, 30, 50, 100; benchmark stability)
- Hybrid (semantic + geometric features fused; per gandalf's recommendation)

**Deliverable per algorithm pass:**
- Cluster assignments per weapon
- Cluster dominant-axes characterization (what makes each cluster distinct)
- Cluster statistics (size, density, separation)
- Reproducibility seed + algorithm version recorded

**Output:**
- Populates `cluster_id` on `weapons` table (single dominant cluster)
- Populates `cluster_membership` table (multi-cluster with confidence scores)
- Populates `clusters` table (cluster registry with dominant_axes_description)

**Acceptance criteria:**
- ≥3 algorithm passes complete with comparable cluster structures
- Inter-rater reliability check (do hierarchical + HDBSCAN agree on dominant cluster centroids?)
- Cluster count in target range (50-150 clusters at recommended granularity)
- Summary: `logs/clustering_analysis_summary.json` with per-cluster sample weapons + dominant-axes

---

### Phase 4 — Cluster Semantic Labeling (D9; design call)

**Owner:** gandalf + Matt design call (~2-3 hours; possibly across multiple sittings)
**Dependencies:** Phase 3 complete
**Duration:** ~2-3 hours focused design time
**Discipline:** Pattern recognition design work; not automatable

**What it does:**

Review the top-N clusters (by size + distinctness) from Phase 3. For each:
- Inspect sample weapons (5-10 representatives)
- Identify the cluster's gestalt — what makes weapons in this cluster feel like a coherent family?
- Assign a semantic label (e.g., "Eastern-curved-blade-family", "Industrial-firearm-family", "Ornate-ceremonial-staff-family")
- Optionally assign secondary tags (aesthetic-tuple vocabulary: tech_level / tone / cultural_lineage)
- Note whether this cluster matches a hypothesis from the original 15-entry catalogue (Greatsword cluster? Wand cluster?) OR represents an unexpected emergent category

**Output:**
- Updates `clusters.label` for each reviewed cluster
- Updates `clusters.dominant_axes_description` with reviewed-and-refined text
- Possibly authors `canonical/story/emergent-cluster-catalogue-2026-05-XX.md` capturing the labeled clusters as canonical Reincarnated gear-substrate vocabulary

**Acceptance criteria:**
- ≥80% of weapons (by row count) are members of a labeled cluster
- Cluster labels are player-meaningful (designer-test: would a player understand "katana-family" vs "obscure-cluster-17")
- Cross-references back to original 15-entry catalogue (which entries emerged as clusters? which didn't?)

---

### Phase 5 — Validation + Substrate-Density Precomputation (D10 + D11; PARALLEL)

#### D10 — Galadriel Visual Coherence Validation

**Owner:** galadriel
**Dependencies:** Phase 4 complete (cluster labels assigned)
**Duration:** 4-8 hours
**Discipline:** #11 (empirical inspection of visual coherence per cluster)

**What it does:**

Run computer-vision similarity scoring on the preview images of weapons within each labeled cluster. Outputs:
- Per-cluster visual cohesion score (do members look like they belong together?)
- Outlier flagging (weapons assigned to a cluster but visually distinct — candidate misclassifications)
- Cross-cluster confusion analysis (which cluster pairs have weapons that could plausibly belong to either?)

**Acceptance criteria:**
- ≥75% of clusters have visual cohesion score above threshold (per Discipline #17 calibration)
- Outlier weapons flagged with confidence scores; ≤5% require reassignment
- Summary: `logs/galadriel_cluster_validation_summary.json`

#### D11 — Substrate-Density Precomputation

**Owner:** rocket
**Dependencies:** Phase 4 complete; D10 can run in parallel
**Duration:** 1-2 hours
**Discipline:** #1 (math-before-code on density-aggregation formula)

**What it does:**

Populate the precomputed `substrate_density` table per legolas's schema design. For each substrate-vector tuple (element × range × cluster_id), compute:
- Count of weapons matching the tuple
- Best-ω-score for the tuple
- Aesthetic-coverage map (which tech/tone/culture descriptive tags are represented)
- Density classification: dense / medium / sparse / empty (with thresholds calibrated per Discipline #17)

**Output:** `substrate_density` table populated; engine queries return O(1) density check + routing decision.

**Acceptance criteria:**
- All non-empty substrate-vector tuples have density entries
- Sample inspection (rocket reviews ~20 random tuples): density classifications feel right
- Summary: `logs/substrate_density_summary.json`

---

## 3. Decision gates

Knight-rider holds dispatches at these gates pending Matt input:

| Gate | When | What blocks | Resolution |
|---|---|---|---|
| **G1 — Meshy API probe outcome** | Before D2 fires | Phase 1A scope | P0.2 probe + Matt confirmation of which D2 variant fires |
| **G2 — CC-BY-SA legal review** | Before any commercial-publish use of imported assets | `game_approved` flag policy | Matt confirms CC-BY-SA commercial-compatible OR keeps `game_approved=0` for those assets |
| **G3 — Cluster semantic labeling kickoff** | After Phase 3 completes | Phase 4 design call timing | Matt schedules ~2-3 hours with gandalf for the labeling session |
| **G4 — Phase D Meshy generation gap-fill priority** | Mid-Phase-5 once density map populated | Priority ranking for Meshy generation targets | Matt + gandalf review density map; identify priority targets; knight-rider authors Phase D dispatches |

---

## 4. Discipline #19 compliance — explicit per-phase

| Phase | Discipline #19 compliance pattern |
|---|---|
| **Phase 0** | Foreground operational; no babysit needed (single `sqlite3` invocation) |
| **Phase 1 D2-D6** | All as `nohup` background processes; status via `sqlite3 ... SELECT COUNT(*) FROM weapons WHERE source_library=?` direct queries; JSON summary as final-act; resume-on-failure via DB checkpoint queries |
| **Phase 2 D7** | Foreground if <1 hour; background if larger sample; status via row update count queries |
| **Phase 3 D8** | Background (Mode A analytical + ML clustering can run multi-hour); status via algorithm version in `clusters` table; JSON summary as final-act |
| **Phase 4 D9** | Foreground interactive (design call; not automatable) |
| **Phase 5 D10 D11** | Background each; status via summary file existence |

**No phase requires Agent invocations for monitoring.** All long-running work is OS-level background; all status checks are direct one-shot Bash + SQL queries.

---

## 5. Cross-session continuity artifacts

Every dispatch produces a JSON summary at a known path. The summary acts as cross-session continuity if the orchestrator session ends mid-phase:

| Phase | Summary artifact path |
|---|---|
| Phase 0 | `agentic_orchestration/logs/schema_lock_summary.json` |
| D2 | `~/Games/reincarnated-engine/logs/meshy_import_summary.json` |
| D3 | `~/Games/reincarnated-engine/logs/sketchfab_import_summary.json` |
| D4 | `~/Games/reincarnated-engine/logs/kenney_import_summary.json` |
| D5 | `~/Games/reincarnated-engine/logs/oga_import_summary.json` |
| D6 | `~/Games/reincarnated-engine/logs/smithsonian_import_summary.json` |
| D7 | `~/Games/reincarnated-engine/logs/bdi_seeding_summary.json` |
| D8 | `~/Games/reincarnated-engine/logs/clustering_analysis_summary.json` |
| D9 | `canonical/story/emergent-cluster-catalogue-2026-05-XX.md` (canonical doc IS the artifact) |
| D10 | `agentic_orchestration/galadriel/logs/cluster_validation_summary.json` |
| D11 | `~/Games/reincarnated-engine/logs/substrate_density_summary.json` |

Next-session orchestrator can recover state by reading these files + querying `weapons` and `clusters` table counts.

---

## 6. Recommended knight-rider kickoff sequence

**Tomorrow morning's first knight-rider session:**

1. **Read** this plan + the `skill_handoff_2026-05-22-evening.md` for full context
2. **Resolve P0.1 + P0.2** with Matt (env var persist + probe; ~5 min Matt time)
3. **Fire Phase 0 (D1)** — schema lock; ~5 min
4. **Author and fire Phase 1 parallel dispatches** (D2-D6 per probe outcome from G1):
   - D2: Meshy (per G1 outcome)
   - D3: Sketchfab API
   - D4: Kenney static
   - D5: OGA crawl
   - D6: Smithsonian (gated on P0.5)
5. **Monitor Phase 1 via direct DB COUNT queries** (Discipline #19-compliant; no babysit)
6. **When ≥80% imports complete:** fire D7 (BDI ω seeding)
7. **When D7 completes:** fire D8 (clustering analysis)
8. **When D8 completes:** schedule G3 (cluster labeling design call) with Matt
9. **After D9:** fire D10 + D11 in parallel
10. **On phase completion:** author CHANGELOG entry; mark phase done in this plan doc

---

## 7. Open questions for Matt (review before kickoff)

| # | Question | Default if no response |
|---|---|---|
| Q1 | If Meshy API probe shows library-browse endpoints exist BUT under partner-tier (not Pro): proceed with partner-tier outreach + wait, OR start with D3-D6 + Meshy-generation-only Phase D? | Start with D3-D6 in parallel; partner outreach runs in background; pivot Phase 1A if outreach succeeds |
| Q2 | CC-BY-SA legal review: when can it complete? Blocks game_approved=1 for those assets but doesn't block import. | `game_approved=0` for CC-BY-SA assets pending review; revisit at Phase 6 (pre-cutover) |
| Q3 | Clustering algorithm preference (hierarchical / HDBSCAN / k-means / hybrid)? | gandalf-recommended **hybrid (semantic + geometric)** with hierarchical clustering output for multi-granularity |
| Q4 | Cluster count target — 50? 100? 150? | Default 75-100 (gandalf intuition; refinable post-Phase-3) |
| Q5 | Phase 4 design call format — single 2-3 hour session, or split into multiple 30-45 min sessions across days? | Default: split across days for designer-craft reasons; clusters benefit from sleep between reviews |
| Q6 | Galadriel visual validation (D10) — full population or sampled? | Sampled (50-100 weapons per cluster) for time efficiency; full only if outlier flagging surfaces concerns |

---

## 8. Estimated timeline

| Phase | Duration (wall) | Active Matt time |
|---|---|---|
| Phase 0 (schema lock) | 5 min | 0 |
| Phase 1 (imports parallel) | 4-8 hours wall time; up to 1 day if Meshy bulk path engaged | ~30 min for P0 checks + dispatch authoring review |
| Phase 2 (BDI ω seeding) | 1-2 hours | 0 (rocket-owned) |
| Phase 3 (clustering analysis) | 1-2 days | 0 (legolas/rocket-owned) |
| Phase 4 (cluster labeling) | 2-3 hours focused (could span days) | **2-3 hours active Matt time** |
| Phase 5 (validation + density) | 4-8 hours parallel | 0 (galadriel + rocket-owned) |
| **Total wall time** | **~1-2 weeks** | **~3-4 hours active Matt time** |

---

## 9. What this delivers

When all phases complete:

| Deliverable | What it enables |
|---|---|
| **~2,000-6,500 weapons indexed in DB** | Engine-side substrate-vector queries return candidate weapon sets |
| **50-150 semantically-labeled clusters** | Cohesion-judge reads cluster identity for thematic naming; profile flags reference cluster labels |
| **BDI ω-scores populated** | Density-routing-by-element functional; cohesion-judge prompts grounded |
| **Substrate-density precomputed** | O(1) density-check + routing-decision per generation cycle |
| **Phase D ready** | Knight-rider can fire Meshy generation gap-fill dispatches against the density map's sparse regions |
| **Profile A asset pipeline operational** | Reincarnated v1 spirit-form library generation has a real substrate to query |

This is the structural work that turns gear-substrate from a hand-authored 15-entry sketch into a substrate-as-cohesion-coherent emergent system.

---

## 10. Cross-references

### 10.1 Canonical foundation
- `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` — Variant C lock + vast-library framing
- `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` — Profile A pipeline (skeleton; finalization tomorrow)
- `canonical/story/gear-substrate-rule-table-v1-2026-05-22.md` — 15-entry catalogue (now demoted to prediction; emergent clusters supersede)
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` — BDI formalism (Phase 2 input)

### 10.2 Research foundation
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/findings-summary.md` — five headline findings + four open carries
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` — ready-to-run DDL
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/selection-patterns.md` — 7 parameterized query templates for engine consumption

### 10.3 Session context
- `agentic_orchestration/skill_handoff_2026-05-22-evening.md` — full evening-session capture
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 19 — Discipline #19 (RATIFIED 2026-05-22; applies throughout this plan)

### 10.4 Pending canonical work (gandalf tomorrow morning)
- `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` — five vestigial-pattern retirements
- `canonical/story/stat-derivation-from-bc-convergence-2026-05-22.md` — BC-axis-derived stats
- `canonical/story/gear-heavy-promotion-2026-05-22.md` — LITE→HEAVY + vast-library pivot

---

**Signed:** gandalf (planner; not orchestrator)
**For:** knight-rider's tomorrow-morning session to take ownership of execution sequencing; hive specialists (legolas / rocket / galadriel / drax) to consume per-phase dispatches when authored.

**Knight-rider:** when you pick this up, read § 1 pre-flight checks first; resolve P0.1 + P0.2 with Matt; then sequence dispatches per § 2. This plan is the spine; you author the per-phase dispatches against it. Hold gates G1-G4 for Matt input.

**Matt:** when knight-rider engages tomorrow, your ~3-4 hours of active time concentrates at:
- Pre-flight check resolution (~30 min)
- Phase 4 cluster semantic labeling (~2-3 hours)
- Decision-gate inputs (G1-G4; ~30 min spread across the workstream)

The road continues to walk itself. The Mirror is ready to see what emerges from 60K weapons or 2K weapons, whichever the morning surfaces.
