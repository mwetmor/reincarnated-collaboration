# Dispatch — legolas — Track A1 Wikipedia FIX (Wave-1.5): Wikidata-anchored ingestion

**Date:** 2026-05-22
**Author:** knight-rider (hive-mind orchestrator)
**For:** legolas
**Pattern:** B (long task; corrective re-ingestion)
**Status:** FIRING (Wave-1.5 — fix-and-replace)
**Triggering issue:** prior A1.2 ingestion (PID 43950, completed 2026-05-22 03:26 UTC) produced 130,334 rows tagged `source_library='wikipedia'` via loose full-dump keyword matching. Spot-check of 35 random rows shows the matcher false-positives on athletes, actors, buildings, songs, train stations, diseases, kings (e.g., "Harry Lempio (German boxer)", "Cast of Thousands (Elbow album)", "Charles III"). Estimated true-positive rate: ~9-12%. The 130K rows are now quarantined under `source_library='wikipedia-unfiltered'` (preserved for audit; excluded from clean views). This dispatch executes the canonical Wikidata-anchored path per the original A1 dispatch § Sub-task A1.2.

---

## Required reading

1. `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/weapon-library-import-hive-mind-mission-2026-05-22.md`
2. `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/weapon-library-import-hive-mind-state.md` (current counts)
3. `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-22-legolas-track-A-wikipedia-wikidata-commons-dump-consumption.md` § Sub-task A1.2 (original spec — read carefully; the implementation deviated here)
4. Your prior script: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/scripts/a1_2_wikipedia_dump_parser.py` (the script that produced the false-positives — understand why before rewriting)

---

## Task

Re-ingest Wikipedia weapon articles using **Wikidata-sitelink-anchored matching** (NOT full-dump keyword matching). Insert results with `source_library='wikipedia'` (the fresh post-quarantine tag).

### Pipeline (canonical)

1. **Build the seed set** from existing `weapon_knowledge_entries` where `source_library='wikidata'`. Each row has a `source_url` (Wikidata Q-page URL) and `source_id` (Q-number). Extract the English Wikipedia sitelink for each Wikidata Q-item via SPARQL (one batch query, fits in single 60s SPARQL request — ~12K entries):
   ```sparql
   SELECT ?weapon ?weaponLabel ?article WHERE {
     ?weapon wdt:P31/wdt:P279* wd:Q728 .
     ?article schema:about ?weapon ;
              schema:isPartOf <https://en.wikipedia.org/> .
     SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
   }
   ```
   Save to `wikidata_sitelinks_v2.json` (which the prior run may already have produced; verify).
2. **Filter Wikipedia dump pass** to only pages whose title matches a Wikidata sitelink article-title from step 1. This drops the dump's 130K+ false-positives to ~10-13K legitimate weapon articles (matches Wikidata weapon-class count).
3. **Per matched page:** stream-parse `<text>` to extract:
   - Plain-text description (first 1-2 paragraphs at least; full body if reasonable to store)
   - Infobox properties via `{{Infobox weapon|...}}`, `{{Infobox firearm|...}}`, `{{Infobox edged weapon|...}}`, `{{Infobox knife|...}}`, `{{Infobox sword|...}}`, etc. (all weapon-related Infobox templates) — parse the templates with `mwparserfromhell`
   - Category list (Wikipedia categories the article belongs to)
   - First image reference (`[[File:...]]` in the body, or infobox `image=` property)
4. **Insert OR UPDATE** behavior — choose ONE:
   - **Preferred:** UPDATE the existing `weapon_knowledge_entries` row (matched by `source_library='wikidata'` AND `source_id=<Q-number>`) to populate `description_text` with the Wikipedia article body, augment `structured_properties` with infobox fields, augment `cultural_lineage_tags` with Wikipedia categories. NO new row inserted.
   - **Alternative:** INSERT a new row with `source_library='wikipedia'` (fresh tag) linking back via shared `source_id`. Use this if normalization makes UPDATE messy.
5. **Image extraction:** for each first-image reference, INSERT into `knowledge_entry_reference_images` (`image_source='wikipedia-infobox'`, `license_class='Commons-various'`) if not already present.

### Fallback: infobox-template-only filter (if Wikidata-sitelink approach is incomplete)

Some weapons in Wikipedia don't have a Wikidata Q-item but DO have a weapon-infobox template. A secondary filter pass: any Wikipedia page in the dump whose text contains `{{Infobox weapon` (or one of the related weapon-infobox templates) is also a weapon page. INSERT these as `source_library='wikipedia'` with NULL `source_id` (no Wikidata link).

Expected combined yield: ~10-15K legitimate Wikipedia weapon entries.

---

## Discipline #19 compliance

- Author script → fire `nohup python a1_2_wikipedia_dump_parser_v2.py > logs/knowledge_crawl_wikipedia_v2.log 2>&1 &` → return immediately
- Dump file `/tmp/enwiki-latest-pages-articles.xml.bz2` already downloaded from prior run; reuse it (don't re-download 22GB)
- Final JSON summary at `/Users/admin/Games/reincarnated-engine/logs/knowledge_crawl_wikipedia_v2_summary.json`

---

## Discipline #1 (math-before-code)

Brief math note revision: `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/track-A1-math-note.md` — append § "Fix v2" with: estimated yield (Wikidata-sitelink seed size + infobox-fallback overlap), expected wall time (parse-only; dump already on disk; ~10-15 min), false-positive root-cause analysis (what the prior loose matcher did wrong), regression-prevention check (how the v2 matcher avoids it).

---

## Discipline #20 compliance

- Same Wikimedia etiquette as the original dispatch
- Research-agent UA only

---

## Acceptance criteria

| # | Criterion |
|---|---|
| 1 | New `source_library='wikipedia'` row count (post-fix) is ≤ 25K (sanity floor: if > 25K, matcher still too loose; investigate) |
| 2 | Spot-check 20 random new `wikipedia` rows: ≥17 of 20 must be legitimately a weapon-page (≥85% true-positive rate) |
| 3 | `wikipedia-unfiltered` rows remain untouched (audit trail preserved) |
| 4 | JSON summary at canonical path |
| 5 | Script at `scripts/a1_2_wikipedia_dump_parser_v2.py` (versioned to preserve audit of prior implementation) |
| 6 | Math note Fix-v2 section appended |

---

## Out of scope

- Touching `wikipedia-unfiltered` rows (leave for downstream filter decisions)
- Re-running A1.1 Wikidata SPARQL (current 12,371 rows are fine)
- Re-running A1.3 Commons enricher (it operates on `wikidata-p18` images and is unaffected)

---

**Signed:** knight-rider (Wave-1.5 fix dispatch)
