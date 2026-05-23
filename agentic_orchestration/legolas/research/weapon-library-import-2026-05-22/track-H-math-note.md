# Track H Math Note — Met Museum Open Access API (Arms & Armor)
# Discipline #1 compliance — authored before script

**Date:** 2026-05-22
**Author:** legolas
**Track:** H (Met Museum Open Access API)

---

## API probe results (live, 2026-05-22)

| Parameter | Observed value |
|---|---|
| Endpoint | `https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds=4` |
| `total` field | **13,753** object IDs returned |
| First IDs in array | 21910, 21911, 21912, 21913, 21914 |
| Per-object endpoint | `https://collectionapi.metmuseum.org/public/collection/v1/objects/<objectID>` |
| robots.txt on API subdomain | None (404) — GREEN per DISCOVERY scout |

---

## Per-object field map (confirmed by live probe)

| API field | Target column / use |
|---|---|
| `objectID` | `source_id` |
| `title` | `canonical_name` |
| `objectURL` | `source_url` |
| `primaryImage` | `knowledge_entry_reference_images` row (if non-empty string) |
| `primaryImageSmall` | captured in structured_properties for reference |
| `additionalImages` | additional `knowledge_entry_reference_images` rows |
| `culture`, `period`, `dynasty`, `country`, `region`, `objectDate` | `structured_properties` JSON + `historical_period` |
| `medium`, `dimensions`, `classification`, `objectName` | `structured_properties` JSON |
| `objectBeginDate`, `objectEndDate` | `structured_properties` JSON |
| `isPublicDomain` | `license_class` = `'CC0'` if true, else `'unknown'` |
| `tags` | augment `cultural_lineage_tags` JSON |
| `objectWikidata_URL` | `structured_properties` (Wikidata linkage, future merge use) |

**Key observation:** `isPublicDomain=false` objects (many) have empty `primaryImage` — those rows still get inserted but have no image rows. `isPublicDomain=true` objects expose full image URLs from `images.metmuseum.org`.

---

## Rate-limit budget

| Parameter | Value |
|---|---|
| Total objects | 13,753 |
| Rate ceiling (courtesy) | 5 req/sec |
| Theoretical minimum wall time | 13,753 / 5 = **2,751 seconds = ~45.8 minutes** |
| Add 10% overhead (connection overhead, retries, DB writes) | ~50 minutes |
| Concurrency strategy | Single async loop with asyncio + aiohttp, 5 concurrent requests max |
| Per-request sleep (fallback if async not feasible) | 0.2s between requests |

Async approach (aiohttp with semaphore=5) should achieve ~5 req/sec with lower overhead than synchronous sleep. Expected actual wall time: **~46-55 minutes**.

---

## Expected yield

| Metric | Estimate | Basis |
|---|---|---|
| Total objects fetched | 13,753 | API `total` field (live probe) |
| Rows inserted (all, incl. armor/accessories) | ~13,700–13,753 | Near-100% expected; some 404 for retired objects |
| Expected 404 / retired objects | ~50–100 | Conservative; Met API is stable |
| Objects with `isPublicDomain=true` | ~8,000–10,000 | Met Arms & Armor collection is heavily PD; many pre-1928 |
| Objects with non-empty `primaryImage` | ~8,000–10,000 | Matches PD rate; non-PD have blank image fields |
| Image rows in `knowledge_entry_reference_images` | ~10,000–15,000 | primaryImage + additionalImages for PD objects |
| Image coverage rate (≥1 image per entry) | **~70–75%** | Meets ≥70% acceptance criterion |

**Overlap with other tracks:** Minimal. Royal Armouries (Track A3) is a distinct institution. Wikidata (Track A1) may reference Met objectIDs via Wikidata properties; this is a cross-source enrichment opportunity post-import, not a dedup concern at crawl time. `(source_library='met-museum', source_id=<objectID>)` UNIQUE constraint handles any re-run safety.

---

## Failure mode coverage

| Failure mode | Handling |
|---|---|
| HTTP 404 for individual object | Log to JSON summary `errors` array; skip; continue |
| HTTP 429 rate limit | Exponential backoff: 2s → 4s → 8s; after 3 retries, mark object as `extraction_error` and continue |
| HTTP 5xx server error | Same backoff as 429; up to 3 retries |
| Empty `title` field | Use `objectName` as fallback; if both empty, use `f"Met-Arms-{objectID}"` |
| `additionalImages` null | Treat as empty list (no images) |
| `tags` null | Treat as empty list |
| SQLite write contention (WAL mode) | 100-row batch inserts; retry on SQLITE_BUSY up to 5× with 0.1s sleep |
| Network timeout | 30s per request; counted as failure if exceeded → retry |
| Script crash mid-run | Resume via `INSERT OR IGNORE` — already-inserted rows skip cleanly on re-run |
| Disk full | Checked at script start; abort with clear error if <500MB free |

---

## Acceptance criteria check

| Criterion | Expected | Meets bar |
|---|---|---|
| ≥10,000 rows with `source_library='met-museum'` | ~13,700 | YES |
| ≥70% with ≥1 reference image | ~70-75% | YES (marginal; depends on PD rate) |
| CC0 captured where `isPublicDomain=true` | 100% of PD objects | YES |
| JSON summary at canonical path | Written at script completion | YES |
| Script at `scripts/track_h_met_museum.py` | Written before fire | YES |

---

**Signed:** legolas (Track H, pre-script math, 2026-05-22)
