# Dispatch — legolas — Track B: 3D Model Imports (Sketchfab + Kenney + OGA)

**Date:** 2026-05-22 (authored overnight)
**Author:** knight-rider (overnight cascade per Matt 2026-05-22 evening authorization)
**For:** legolas
**Pattern:** B (long task; dedicated session)
**Status:** READY TO FIRE — all three sources GREEN per overnight robots verification
**Required reading first:**
1. `agentic_orchestration/logs/2026-05-22-evening-robots-verification.md`
2. `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/library-enumeration.md` (Sketchfab + Kenney + OGA sections)
3. `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/import-strategy.md`
4. `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` v1.1.0

---

## Context

3D models are SECONDARY substrate per Matt's re-plan. They become reference attachments to knowledge entries via `knowledge_model_attachments`. They populate the existing `weapons` table from legolas's original schema design.

Per overnight robots.txt verification:

| Source | Status | Method |
|---|---|---|
| Sketchfab | **GREEN** | Documented Data API v3 |
| Kenney | **GREEN** (no robots.txt; static downloads) | Static ZIP downloads (~10-20 ZIP files) |
| OGA | **GREEN with Crawl-delay: 10** | Crawl with 10-sec delay |

---

## Sub-task D3 — Sketchfab Data API v3

**Scope:** Per legolas's prior research, ~1,177 CC0+CC-BY weapons in weapons-military category (S3D3C dataset finding: 9.5% CC0 + 36.3% CC-BY of 2,570 total).

**Approach:**
1. Sketchfab Data API v3 docs: https://docs.sketchfab.com/data-api/v3/
2. List models endpoint: `GET https://api.sketchfab.com/v3/models?categories=weapons-military&license=CC0,CC-BY&downloadable=true&cursor=...`
3. Cursor-based pagination; structured JSON response
4. Per result: INSERT `weapons` row with source_library='sketchfab'; appropriate license_class; preview image URL; download URL (if accessible without auth)
5. **Authentication note:** Sketchfab API allows anonymous browsing of public CC0+CC-BY models. Authenticated access would need a Sketchfab API token. The dispatch can operate in anonymous mode for the initial pull.

**Estimated runtime:** 1-4 hours (cursor pagination at conservative rate)

**Discipline #19:** nohup background; logs at `~/Games/reincarnated-engine/logs/model_crawl_sketchfab.log`; JSON summary

---

## Sub-task D4 — Kenney static downloads

**Scope:** ~200-400 CC0 weapons across Kenney's documented asset packs.

**Approach:**
1. Inventory Kenney asset packs at https://kenney.nl/assets (filter by weapon-relevant: "Weapon Pack", "Tower Defense Top-Down" weapons subset, "Pirate Pack" weapons subset, etc.)
2. For each relevant pack: download the static ZIP via documented URL pattern
3. Extract per-pack metadata + per-asset filenames + format inventory (GLB / OBJ / FBX presence)
4. INSERT one `weapons` row per weapon asset with source_library='kenney'; license='CC0'; preview image URL where pack provides one

**Estimated runtime:** 30-60 minutes (download + extract + import)

**Discipline #19:** Foreground OK (under 1 hour); logs + JSON summary

---

## Sub-task D5 — Open Game Art crawl

**Scope:** ~389 OGA weapon entries; mixed CC0/CC-BY/OGA-BY/GPL — filter at import time, REJECT GPL and CC-BY-NC.

**Approach:**
1. OGA listings predictable URL pattern (per legolas research)
2. **Honor 10-second Crawl-delay per robots.txt** (verified tonight)
3. At 10s/request, ~360 requests/hour; ~1-2 hours for full ~389-entry coverage
4. Per entry: parse title, description, license, file format(s), preview image URL
5. License filter at INSERT time:
   - CC0 / CC-BY / OGA-BY → INSERT with appropriate license_class
   - GPL2 / GPL3 → REJECT (incompatible with closed-source product per existing licenses table seed)
   - CC-BY-NC / CC-BY-NC-SA / CC-BY-NC-ND → REJECT (non-commercial)
6. INSERT `weapons` rows with source_library='open_game_art'

**Estimated runtime:** 1-2 hours

**Discipline #19:** nohup background; logs at `~/Games/reincarnated-engine/logs/model_crawl_oga.log`; JSON summary; checkpoint by `MAX(weapon_id)` query

---

## Math-before-code (Discipline #1)

- **Sketchfab API:** sample 10-20 weapon entries via interactive query; characterize response schema; confirm CC0+CC-BY filter behavior; estimate per-call latency
- **Kenney packs:** inventory the URL patterns; confirm static download accessibility
- **OGA:** sample 5-10 entries; characterize HTML extraction reliability; confirm Crawl-delay enforcement on server side

Math note at `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/track-B-math-note.md`.

---

## Acceptance criteria

### D3 (Sketchfab)
- ≥800 `weapons` rows with source_library='sketchfab'
- License correctly classified (CC0 vs CC-BY)
- preview_image_url populated per row

### D4 (Kenney)
- ≥150 `weapons` rows with source_library='kenney'
- All license='CC0'
- License-tier consistency check passes

### D5 (OGA)
- ≥250 `weapons` rows with source_library='open_game_art'
- ≤10% rejected due to GPL or NC license
- 10-sec crawl delay confirmed via log timestamp distribution

### All three
- JSON summary at canonical path per sub-task
- Tag intent: `legolas/v0.2-track-B-3d-model-imports-1`

---

## Cross-seam handoff (Track A ↔ Track B)

The MODEL-TO-KNOWLEDGE-ENTRY ATTACHMENT pass is OUT OF SCOPE for this dispatch. That is a downstream join (Phase 1.5 territory) that fires after Track A knowledge entries AND Track B model entries both populate.

Pattern: knowledge entry "Katana" + Sketchfab model "Japanese Katana 3D" with name-similarity / tag-overlap score ≥ threshold → INSERT `knowledge_model_attachments` row with attachment_source='name-match' + attachment_confidence per scoring.

This is the substrate-pivot architecture's load-bearing join. Out of scope for tonight; called out so legolas doesn't conflate with current dispatch.

---

## Out of scope

- Meshy library crawl (RED per evening probe; only Meshy generation API path remains; that's Phase D gap-fill territory)
- TurboSquid / CGTrader / Fab (Tier 3 commercial; deferred per legolas import-strategy.md)
- itch.io CC0 packs (deferred; lower-priority backfill)
- BlendSwap (.blend-only format overhead per legolas research)
- Smithsonian 3D models (covered under Track A2 museum dispatch via api.data.gov)

---

**Signed:** knight-rider (overnight cascade)
