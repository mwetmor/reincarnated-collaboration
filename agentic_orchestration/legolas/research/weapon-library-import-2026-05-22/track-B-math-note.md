# Track B Math Note — 3D Model Imports (Sketchfab + Kenney + OGA)
# Discipline #1 compliance: math-before-code

**Date:** 2026-05-22
**Author:** legolas
**Commission:** dispatches/2026-05-22-legolas-track-B-3d-model-imports-sketchfab-kenney-oga.md

---

## B1 — Sketchfab Data API v3

### Addressable count
- Weapons-military CC-only subset per S3D3C dataset: 2,570 models
- CC0 (license=pd): ~244 (9.5% of 2,570)
- CC-BY (license=by): ~933 (36.3% of 2,570)
- Usable total (CC0 + CC-BY only, excluding CC-BY-SA and NC variants): ~1,177
- Acceptance criteria minimum: 800

### Rate-limit budget
- Sketchfab Data API v3: documented rate limit not explicitly stated in public docs;
  community-established conservative floor is 1 request/2 seconds for unauthenticated access.
- At 1 req/2 sec: 30 req/min = 1,800 req/hour
- Each search page returns 24 models; 1,177 models / 24 per page = ~49 pages
- Metadata pass: 49 page fetches at 2 sec each = ~98 seconds = under 2 minutes
- HOWEVER: cursor pagination may enforce per-cursor wait; actual observed rate may be
  slower. Budget 5x safety margin: 10 minutes for metadata pass.
- API does NOT require authentication for public CC0+CC-BY model browsing/metadata.
  Download URLs require OAuth; we record preview_image_url from thumbnails only (URL-only policy).
- Unauthenticated search: confirmed supported per Sketchfab API docs (no auth required for
  listing/search endpoints; auth required only for download endpoint).

### Request-per-model estimate (metadata only, no download)
- 1 cursor page per 24 models: ceil(1177/24) = 50 pages
- At 2 sec/request: 100 seconds for all pages
- With 5x safety margin for rate limit drift / retry: ~10 minutes wall time for metadata pass
- Retry budget: exponential backoff starting at 5 sec; max 3 retries per page; on sustained
  429 → pause 60 sec and retry.
- Total wall-time estimate: 15-30 minutes (tight; metadata-only, no downloads)

### What counts as a "weapon" vs other asset
- Filter: `categories=weapons-military` — Sketchfab's canonical category slug for weapon models
- Additional filter: `license=by` (CC-BY) and `license=pd` (CC0 / public domain)
- Excludes: CC-BY-SA (license=sa), CC-BY-NC* (license=nc, nc-sa, nc-nd)
- No additional keyword filter needed — the category slug is the scope constraint

### URL-only image policy
- preview_image_url: populated from API response `thumbnails.images[0].url` field
  (or highest-resolution available)
- No thumbnail download; URL stored in weapon_sources.preview_image_url
- download_url: populated from model's `viewerUrl` page URL (not a direct download;
  actual GLB download requires OAuth token — out of scope per dispatch)
- Image bytes: NOT downloaded; URL-only per gandalf commit 7b98231

### Schema mapping
- weapons table: display_name, weapon_subclass (inferred from tags), description (truncated to 500 chars)
- weapon_sources: source_asset_id = Sketchfab model uid; source_url = model page URL;
  preview_image_url from thumbnails; library_id = 1 (sketchfab); license_id from CC map
- Tag inference: Sketchfab tags parsed for weapon_class, tech_level, cultural_lineage heuristics
- readiness_state: 'sim_viability_unverified' (no GLB downloaded yet; secondary substrate)

---

## B2 — Kenney.nl Static ZIPs

### Addressable count
- Dedicated weapon packs enumerated:
  - Medieval RTS: https://kenney.nl/assets/medieval-rts — ~120 assets total; ~80-100 weapons
  - Blaster Kit: https://kenney.nl/assets/blaster-kit — ~40 sci-fi blaster variants
  - Dungeon Kit: https://kenney.nl/assets/dungeon-kit — estimated 10-20 weapon props
  - Pirate Kit: https://kenney.nl/assets/pirate-kit — estimated 5-10 weapons
  - Total estimated: 135-170 weapon models (conservative) to 200-400 (liberal)
- Acceptance criteria minimum: 150

### Rate-limit budget
- Kenney has no robots.txt; no Crawl-delay directive.
- ZIP downloads are static file downloads, not page-by-page crawling.
- 10-20 ZIP downloads at ~5-30 MB each = total ~100-300 MB bandwidth
- No rate-limit concern; these are CDN-served static files.
- Wall-time: dominated by bandwidth; at 10 MB/s: 300 MB / 10 MB/s = 30 seconds network
  + ~30 seconds unzip + ~5 minutes metadata extraction and INSERT
- Total wall-time estimate: 10-30 minutes

### What counts as a "weapon" vs other asset
- Kenney ZIP contents include: models (GLB/OBJ/FBX), textures (PNG), and sometimes
  non-weapon props (crates, terrain, UI elements).
- Filter strategy: filename pattern matching — any file in a /Weapons/ subdirectory OR
  filenames containing weapon-keyword patterns (sword, axe, bow, dagger, mace, spear,
  blaster, gun, rifle, pistol, lance, crossbow, staff, hammer, shield).
- Exclude: architectural pieces, terrain tiles, UI sprites, character bodies (non-weapon).

### URL-only image policy
- Kenney packs do not provide per-asset thumbnail URLs; pack-level screenshots are available
  on the kenney.nl pack page.
- Store pack-page screenshot URL as preview_image_url where available; NULL otherwise.
- No image downloads.

### Schema mapping
- weapons: display_name from filename (stripped extension, de-snakecased), weapon_subclass
  inferred from filename keywords, tech_level from pack context (Medieval RTS = medieval;
  Blaster Kit = sci_fi)
- weapon_sources: source_asset_id = kenney_packname/filename; source_url = pack page URL;
  library_id = 3 (kenney); license_id = 1 (CC0); cost_usd = 0.0; file_format from extension
- readiness_state: 'needs_format_conversion' if OBJ/FBX only; 'ready_to_import' if GLB present
- All Kenney: license = CC0, attribution_required = 0

---

## B3 — Open Game Art (OGA)

### Addressable count
- Total 3D Art + keyword "weapon" entries on OGA: 389
- Estimated usable (CC0 + CC-BY + OGA-BY, excluding GPL): ~120-160 (30-40% of 389)
  based on platform culture estimates. Exact split confirmed only via full crawl.
- GPL entries: ~15-25% of total — REJECT
- CC-BY-NC*: rare on OGA but present — REJECT
- CC-BY-SA: caution; import with game_approved=0 flag per license policy
- OGA-BY: acceptable; treat as CC-BY for game_approved purposes
- Acceptance criteria minimum: 250 inserted rows (including REJECTED rows with extraction_error noting rejection reason)

### Rate-limit budget
- OGA robots.txt: Crawl-delay: 10
- Safety margin 1.5x: minimum 15 seconds between requests
- At 15 sec/request: 4 req/min = 240 req/hour
- 389 entries require: 389 listing pages + list pagination pages (~17 pages at 24/page)
  Total requests: ~406 at 15 sec each = 6,090 seconds = ~101 minutes
- With retry budget: budget 150 minutes (2.5 hours) wall-time
- Retry: on 429 → sleep 60 sec; on 503 → sleep 30 sec; max 3 retries per page
- User-Agent: reincarnated-engine/0.1 (research; mhwetmore@gmail.com)

### Search URL structure
- Listing page: https://opengameart.org/art-search-advanced?keys=weapon&field_art_type_tid%5B%5D=10&page=N
  (field_art_type_tid[]=10 is "3D Art" type filter)
- Entry page: https://opengameart.org/content/<slug>
- Each listing page provides: title, license badge, entry URL
- Entry page provides: full description, download links, format info, license detail, preview image

### What counts as a "weapon" vs other asset
- OGA search is pre-filtered by keyword "weapon" and type "3D Art"; no additional filter
- Some entries may be "weapon pack" submissions containing 5-50+ individual models
  (counted as 1 weapons row per OGA submission, not per-model, per schema design)
- Exclude: audio-only submissions (though 3D Art filter should prevent this)
- Exclude: 2D sprites (again, 3D Art filter handles this)

### License filter at INSERT time
- CC0 → INSERT with license_id=1, readiness_state='sim_viability_unverified'
- CC_BY (3.0 or 4.0) → INSERT with license_id=2, attribution_required=1
- OGA_BY (3.0 or 4.0) → INSERT with license_id=8, attribution_required=1
- GPL2 → extraction_error='REJECTED: GPL2 license incompatible with closed-source product'
- GPL3 → extraction_error='REJECTED: GPL3 license incompatible with closed-source product'
- CC_BY_NC* → extraction_error='REJECTED: non-commercial restriction'
- CC_BY_SA → INSERT with license_id=3; game_approved=0 per policy; flag in notes
- Unknown → extraction_error='REJECTED: license unknown'

### URL-only image policy
- OGA entry pages expose preview images (submission screenshots/renders)
- Store preview image URL in weapon_sources.preview_image_url
- No image download; URL-only

### Schema mapping
- weapons: display_name from entry title; description from entry description (truncated 500 chars)
- weapon_sources: source_asset_id = OGA node ID (extracted from URL slug or page meta);
  source_url = entry URL; library_id = 4 (oga); file_format from download section;
  preview_image_url from first image in submission
- All GPL/NC entries still get a weapons row (display_name, description) but weapon_sources
  extraction_error set; readiness_state = 'rejected'

---

## Summary Table

| Source | Addressable | Usable (game_approved) | Rate limit | Wall-time estimate | Acceptance target |
|---|---|---|---|---|---|
| Sketchfab (B1) | ~2,570 CC models in weapons-military | ~1,177 (CC0+CC-BY) | 1 req/2 sec | 15-30 min | ≥800 inserted |
| Kenney (B2) | ~200-400 models | all (~200-400, CC0) | N/A (ZIP) | 10-30 min | ≥150 inserted |
| OGA (B3) | 389 entries | ~120-160 (post-GPL filter) | 15 sec/req | ~100-150 min | ≥250 inserted (incl. rejected) |

**Total expected weapons rows (across all three):** 1,200-1,800 inserted rows
**Timeline (parallel execution):** Dominated by OGA crawl at ~150 min; Sketchfab and Kenney
complete within that window.

---

**Signed:** legolas
**For:** knight-rider (dispatch oversight); Discipline #1 compliance record
