# Dispatch — legolas — Track H: Met Museum Open Access API (Arms & Armor)

**Date:** 2026-05-22
**Author:** knight-rider (hive-mind orchestrator)
**For:** legolas
**Pattern:** B
**Status:** FIRING (Wave-2)
**DISCOVERY anchor:** scout flagged this as the #1 highest-value GREEN find — 13,753 CC0 Arms & Armor objects via `collectionapi.metmuseum.org` (separate subdomain from the RED `metmuseum.org`; no robots.txt on the API subdomain; explicit CC0 license)

---

## Required reading

1. `agentic_orchestration/weapon-library-import-hive-mind-mission-2026-05-22.md`
2. Met Museum API docs: https://metmuseum.github.io/
3. The DISCOVERY scout's flag for Track H (see scout return; CSV at `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/discovery-wave1.csv`)

---

## Task

Query the Met Museum Open Access API for all Arms & Armor department objects (`departmentId=4`). Normalize to `weapon_knowledge_entries` with `source_library='met-museum'`. Insert reference image URLs (URL-only).

### Pipeline

1. **Department search:** `GET https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds=4` returns full list of object IDs (~13,753).
2. **Per-object fetch:** `GET https://collectionapi.metmuseum.org/public/collection/v1/objects/<objectID>` returns the rich metadata:
   - `title` → `canonical_name`
   - `objectURL` → `source_url`
   - `objectID` → `source_id`
   - `primaryImage`, `additionalImages` → `knowledge_entry_reference_images` rows (URL-only)
   - `culture`, `period`, `dynasty`, `country`, `region`, `medium`, `dimensions`, `objectDate` → `structured_properties` JSON + populate `historical_period`
   - `isPublicDomain` true → `license_class='CC0'`
   - `tags` → augment `cultural_lineage_tags`
3. **Rate limit:** Met API has no documented rate limit but be courteous — 80 req/sec is the de facto ceiling for collection APIs; cap at 5 req/sec for safety. Total runtime at 5 req/sec for 13,753 objects = ~46 min.

### Filter

Not every Arms & Armor object is a weapon proper (some are armor, regalia, accessories). Insert ALL of them as `source_library='met-museum'` — the schema treats this as inclusive substrate; downstream filtering by `tags` or `medium` is the consumer's responsibility. This is consistent with mission § 3 ("record what we found").

---

## Database write protocol

SQLite WAL mode; `INSERT OR IGNORE` on `(source_library='met-museum', source_id=<objectID>)`. Batch every 100 inserts.

---

## Discipline #19

Author script → fire `nohup python track_h_met_museum.py > logs/weapon-library-track-H.log 2>&1 &` → return immediately with PID + path + JSON summary path. Expected wall ~46 min at 5 req/sec.

---

## Discipline #20

The API subdomain `collectionapi.metmuseum.org` has no robots.txt (404 verified by DISCOVERY scout). Use research-agent UA. The main `metmuseum.org` site is RED but that's irrelevant to the API.

---

## Discipline #1

Brief math note: `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/track-H-math-note.md`. Cover: rate-limit budget, expected yield (13,753 ± dedup with Royal Armouries/Wikidata which is minimal for Met objects), failure modes (object-fetch 404 for retired objects; partial metadata).

---

## Acceptance criteria

| # | Criterion |
|---|---|
| 1 | ≥10,000 rows inserted with `source_library='met-museum'` (floor; if API returns fewer, log discrepancy) |
| 2 | ≥70% have ≥1 reference image URL |
| 3 | License correctly captured as CC0 where `isPublicDomain=true` |
| 4 | JSON summary at canonical path |
| 5 | Script at `scripts/track_h_met_museum.py` |

---

**Signed:** knight-rider (Wave-2 fire 2026-05-22)
