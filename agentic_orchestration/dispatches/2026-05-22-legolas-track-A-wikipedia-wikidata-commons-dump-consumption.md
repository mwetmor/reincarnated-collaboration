# Dispatch — legolas — Track A1: Wikipedia + Wikidata + Wikimedia Commons via Bulk Dumps

**Date:** 2026-05-22 (authored overnight)
**Author:** knight-rider (overnight cascade per Matt 2026-05-22 evening authorization)
**For:** legolas (research scout; Mode B systematic crawl-equivalent via dump consumption)
**Pattern:** B (long task; dedicated session)
**Status:** PENDING — ready for legolas to pick up next session
**Required reading first:**
1. `agentic_orchestration/skill_handoff_2026-05-22-evening.md` (full evening context)
2. `agentic_orchestration/weapon-library-import-orchestration-plan-2026-05-22.md` § RE-PLAN
3. `agentic_orchestration/logs/2026-05-22-evening-robots-verification.md` (THIS DISPATCH'S EMPIRICAL ANCHOR)
4. `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` v1.1.0 (knowledge-first amendment)

---

## Context

Per overnight robots.txt verification: **Wikipedia bot policy explicitly directs substantial-volume consumers to bulk dumps rather than page-by-page API crawl.** ClaudeBot is NOT in Wikipedia/Wikidata/Commons robots.txt Disallow list, but the bot policy itself says: *"Bots that download substantial portions of Wikipedia's content by requesting many individual pages are not permitted. When such content is required, download database dumps instead."*

This dispatch routes Wikipedia/Wikidata/Commons knowledge extraction through the **canonical bulk-dump path**, not via API page-fetching. Dump consumption is allowed, expected, and standard practice for academic + research workloads.

---

## Task

Populate the `weapon_knowledge_entries` + `knowledge_entry_reference_images` tables in `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` with weapon-class entries extracted from Wikipedia + Wikidata + Wikimedia Commons bulk dumps.

### Sub-task A1.1 — Wikidata weapon Q-item extraction (FIRST; most structured)

**Why first:** Wikidata is the cleanest structured source. Each weapon has a typed Q-item with property graph (P31 instance-of weapon classes; P361 part-of; P186 made-from-material; P571 inception date; P495 country-of-origin; P18 reference image link to Commons).

**Approach:**
1. Use the Wikidata SPARQL endpoint at https://query.wikidata.org/sparql (or download a Wikidata JSON dump from https://dumps.wikimedia.org/wikidatawiki/entities/ if SPARQL volume becomes a problem — dump is ~100GB compressed, so SPARQL is preferred for this slice).
2. SPARQL query template (adapt as needed):
   ```sparql
   SELECT ?weapon ?weaponLabel ?description ?image ?country ?countryLabel ?inception ?material ?materialLabel
   WHERE {
     ?weapon wdt:P31/wdt:P279* wd:Q728 .  # instance of (any subclass of) weapon
     OPTIONAL { ?weapon schema:description ?description . FILTER(LANG(?description) = "en") }
     OPTIONAL { ?weapon wdt:P18 ?image . }
     OPTIONAL { ?weapon wdt:P495 ?country . }
     OPTIONAL { ?weapon wdt:P571 ?inception . }
     OPTIONAL { ?weapon wdt:P186 ?material . }
     SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
   }
   LIMIT 5000
   ```
   (You may need to chunk by Q-item ID range to stay within the 60-second SPARQL timeout. Pattern: `FILTER(?weapon >= wd:Q1000 && ?weapon < wd:Q2000)` etc. Build the chunking loop.)
3. Per result row:
   - INSERT into `weapon_knowledge_entries` with source_library='wikidata'
   - Parse structured_properties JSON (country, inception, materials, etc.)
   - Where `?image` URL present: INSERT into `knowledge_entry_reference_images` (image_source='wikidata-p18'; license_class='Commons-various')
4. Target output: 2,000-5,000 Wikidata weapon entries
5. Runtime: tens of minutes to a few hours (SPARQL has rate limits — be conservative)

### Sub-task A1.2 — Wikipedia article extraction (SECOND; richer descriptive text)

**Why second:** Wikipedia articles have richer prose; less structured but more semantic substrate. The article-to-Q-item mapping is via the sitelink in Wikidata (already extracted in A1.1).

**Approach:**
1. For each Wikidata entry that has a Wikipedia EN sitelink, fetch the corresponding Wikipedia article via **bulk dump** (NOT api.php page-by-page):
   - Download the latest `enwiki-latest-pages-articles.xml.bz2` from https://dumps.wikimedia.org/enwiki/latest/ (~20GB compressed; ~80GB uncompressed)
   - Stream-parse the XML; for each `<page>` whose title matches a Wikidata sitelink, extract:
     - `<text>` (wikitext body — convert to plain text or markdown; libraries like `mwparserfromhell` work well)
     - Infobox properties (parse `{{Infobox weapon|...}}` template; many fields are normalizable)
     - Categories (list of `[[Category:...]]` tags)
     - First image reference (`[[File:...|...]]`)
2. UPDATE `weapon_knowledge_entries` rows (matched by Wikidata Q-link): populate `description_text` + augment `structured_properties` with infobox fields + augment `cultural_lineage_tags` from Categories.
3. For each first-image-reference: INSERT `knowledge_entry_reference_images` (image_source='wikipedia-infobox'; license_class='Commons-various')
4. Runtime: dump download is bandwidth-bound (~hours on consumer broadband); parsing ~hour for the weapon subset.

### Sub-task A1.3 — Wikimedia Commons image metadata enrichment (THIRD; image license + dimensions)

**Why third:** Reference images point to Commons files. Need license + dimension metadata to populate `knowledge_entry_reference_images` properly (CC0 vs CC-BY-SA vs PD; width_px / height_px).

**Approach:**
1. Use the Wikimedia Commons API endpoint pattern (allowed per Wikimedia policy for image-metadata queries — these are point lookups, not bulk crawl):
   ```
   https://commons.wikimedia.org/w/api.php?action=query&titles=File:Katana.png&prop=imageinfo&iiprop=url|size|extmetadata&format=json
   ```
2. For each `knowledge_entry_reference_images` row with `image_url LIKE '%commons.wikimedia.org%'`:
   - Call the API
   - Parse extmetadata.LicenseShortName (CC0 / CC-BY-SA-4.0 / PD-etc.) into `license_class`
   - Parse imageinfo.width / .height into `width_px` / `height_px`
3. Honor the API etiquette: max 1 req/sec sustained; descriptive User-Agent header per Wikimedia API:Etiquette guidance (`reincarnated-engine/0.1 (knight-rider research; mhwetmore@gmail.com)`)
4. Runtime: at 1 req/sec, ~3 hours for 10K image lookups.

---

## Discipline #19 compliance (mandatory)

This is a long-running workstream. Honor:

- **Run as OS-level background processes** (`nohup python script.py > log 2>&1 &` or `Bash(run_in_background=true)`); structure as resumable jobs
- **Checkpoint via DB row INSERTs**: each entry committed individually or in small batches; on script restart, query `MAX(id)` per source_library to resume
- **Status via direct sqlite3 one-shot queries**, NOT agent monitoring:
  ```bash
  sqlite3 /Users/admin/Games/reincarnated-loadout/data/telemetry.db \
    "SELECT source_library, COUNT(*) FROM weapon_knowledge_entries GROUP BY source_library;"
  ```
- **JSON summary on completion** at `~/Games/reincarnated-engine/logs/knowledge_crawl_wikipedia_wikidata_commons_summary.json` with: per-sub-task entries-imported, failures, runtime-seconds, errors-list, sample-entries
- **NO Agent invocations to "watch" or "monitor"** — that's Discipline #19 violation
- **Logs** at `~/Games/reincarnated-engine/logs/knowledge_crawl_wikidata.log`, `knowledge_crawl_wikipedia.log`, `knowledge_crawl_commons.log`

---

## Math-before-code (Discipline #1)

Before writing the SPARQL chunking logic OR the dump-parser pipeline, draft a math note covering:
- **SPARQL query result-size distribution** — how many Q-items typically returned per Q-range chunk; how often timeouts hit; chunk-size that keeps queries under 60s
- **Dump streaming memory profile** — what's the resident-memory expectation for streaming `enwiki-latest-pages-articles.xml.bz2`; does it fit comfortably under 4GB?
- **Match-failure rate estimation** — how many Wikidata entries lack EN-Wikipedia sitelinks (unmappable for A1.2); how many Wikipedia articles have no infobox (lossy for A1.2)
- **Image API rate-limit budget** — at 1 req/sec, ~86K calls/day; if 10K images need enriching, well within budget

The math note lands at `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/track-A1-math-note.md`. Author it BEFORE writing scripts.

Then jack-ryan Gate 1 review (knight-rider mediates).

---

## Acceptance criteria

| # | Criterion |
|---|---|
| 1 | ≥2,000 weapon_knowledge_entries rows with `source_library='wikidata'` |
| 2 | ≥1,500 of those have `description_text` populated from Wikipedia article body |
| 3 | ≥70% of entries have ≥1 reference image |
| 4 | ≥30% of entries have a canonical (primary) reference image flagged |
| 5 | License metadata captured per image (CC0 / CC-BY-SA / PD distinguishable) |
| 6 | JSON summary artifact at canonical path |
| 7 | All scripts checked into `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/scripts/` (or appropriate code location) |
| 8 | NO ClaudeBot User-Agent header used in any HTTP call — use descriptive research-agent UA per Wikimedia etiquette |

---

## Out of scope (do NOT do these)

- Fandom-hosted game wikis (most are AMBER per robots verification; deferred to Matt review)
- Independent game wikis blocked at robots.txt (poewiki.net, OSRS wiki, warcraft.wiki.gg, etc. — all RED per verification)
- Fextralife Dark Souls (GREEN-with-CAUTION; deferred to Matt judgement on the precaution policy)
- TVTropes (AMBER → likely RED per probe)
- IMFDB (RED via Cloudflare block)
- Smithsonian (separate Track A2 dispatch; gated on Matt SMITHSONIAN_API_KEY)
- Royal Armouries (separate Track A3 dispatch)
- 3D model imports (separate Track B dispatches D3/D4/D5)
- Pattern 6 axis discovery (Phase 2 work; gated on knowledge entries imported)
- Clustering (Phase 3 work; gated on Phase 2)

---

## Cross-seam coordination

This dispatch produces data in the loadout-app DB (`/Users/admin/Games/reincarnated-loadout/data/telemetry.db`). Drax owns the loadout app's runtime. If schema queries or DB-shape concerns arise, route through knight-rider → drax. No MIGRATION.md needed (greenfield DB; drax has not yet wired anything to read it).

---

## Tag intent

On completion: `legolas/v0.2-track-A1-knowledge-crawl-wikidata-wikipedia-commons-1` (seam-prefixed; not Matt-promoted).

---

**Signed:** knight-rider (overnight cascade; this is a Pattern-B dispatch authored for legolas next-session pickup; NOT fired tonight because the runnable code does not yet exist and authoring it is legolas's job)
