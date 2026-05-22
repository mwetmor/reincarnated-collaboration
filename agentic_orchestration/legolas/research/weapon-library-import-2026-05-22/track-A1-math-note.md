# Track A1 Math Note — Wikidata / Wikipedia / Commons
# Discipline #1 (math-before-code)

**Date:** 2026-05-22
**Author:** legolas (scout)
**Mode:** B (systematic extraction)

---

## A1.1 — Wikidata SPARQL Weapon Q-item Extraction

### Addressable universe

Wikidata Q728 (weapon) has an estimated subclass tree of 30,000–80,000 Q-items as of 2026.
The `wdt:P31/wdt:P279*` traversal captures:
- Direct instances of Q728 (e.g., individual named swords)
- Instances of any weapon subclass (rifle, dagger, sword-type, etc.)

Wikidata SPARQL endpoint hard limits:
- Query timeout: 60 seconds (default; configurable up to 120s via query optimizer hints)
- Result-row cap per query: 10,000 rows (hard LIMIT)
- Sustained query rate: no published hard RPS limit; Wikidata bot policy suggests ≤5 req/sec for
  well-behaved bots; we use 1 req/3 sec to be conservative

### Chunking strategy

**Primary strategy: OFFSET pagination with LIMIT 5000**
- Safer than Q-ID range chunking (Q-IDs are non-contiguous; range chunks produce
  highly variable result counts — some chunks empty, some hitting timeout)
- Use `LIMIT 5000 OFFSET N` loop; advance by 5000 per successful response
- At 5000 rows/chunk: 30K total = 6 chunks; 80K total = 16 chunks
- Per-chunk wall time: ~15-45 seconds depending on SPARQL query complexity
  (P18/P495/P571/P186 OPTIONAL fetches add join overhead)
- Conservative estimate: 40s/chunk × 16 chunks = ~11 minutes for 80K entries

**Fallback strategy: Q-ID band chunking**
- If OFFSET pagination times out at large offsets (common in Wikidata for expensive
  traversals), switch to Q-ID band chunks: FILTER(xsd:integer(SUBSTR(STR(?weapon),33)) >= N
  AND xsd:integer(SUBSTR(STR(?weapon),33)) < N+50000)
- Q-IDs currently run to ~Q130M; weapon Q-items are NOT uniformly distributed (most
  historical weapons are in Q1M–Q10M range; fictional weapons in Q10M–Q60M range)
- Band size 50K gives ~2600 bands — overkill; we use 500K bands = 260 bands
- Expected non-empty bands: ~120 (weapons are sparse in the Q-ID space)
- Time per band: ~5-10s (most return 0 results and resolve fast)
- Total time for band strategy: ~20 minutes

**Chosen: OFFSET pagination first; auto-fallback to band chunking on timeout**

### Yield estimation

| Source | Estimate basis | Low | High |
|---|---|---|---|
| Direct Q728 instances | SPARQL count query | 5,000 | 15,000 |
| Named individual weapons (specific swords, guns, etc.) | Wikidata category depth | 10,000 | 30,000 |
| Weapon TYPE Q-items (sword, dagger, etc.) as instances | Cross-class traversal | 5,000 | 20,000 |
| Fictional/game-specific (via P31/P279* to Q728) | Coverage varies by game | 5,000 | 15,000 |
| **Total** | | **25,000** | **80,000** |

**Target for A1.1: 30,000–60,000 entries** (mission target requires chunking to be thorough)

### DB write rate

- Batch size: 200 rows per transaction (WAL mode; lock duration ~5ms per batch)
- At 60K entries: 300 transactions → <2 min write time
- `INSERT OR IGNORE` on `(source_library, source_url)` — unique constraint in schema

---

## A1.2 — Wikipedia Dump Extraction

### Dump file profile

- File: `enwiki-latest-pages-articles.xml.bz2`
- URL: `https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2`
- Compressed size: ~22GB (as of 2026; grows ~2GB/year)
- Uncompressed size: ~85GB
- Download time (100 Mbps connection): ~30 minutes
  Download time (20 Mbps connection): ~2.5 hours
  Download time (10 Mbps connection): ~5 hours
- **Do NOT decompress to disk.** Stream-parse via `bz2.BZ2File` + `xml.etree.ElementTree`
  iterparse. Peak memory: ~200MB (iterparse discards processed nodes; only holding current
  `<page>` element in memory at any time — typically 2-50KB per page)

### Weapon-article subset

Wikipedia `[[Category:Weapons]]` and subcategories contain ~15,000–25,000 articles.
However, the Wikidata A1.1 pass captures en-sitelinks for all Q728 instances.
A1.2 matches by article TITLE (from Wikidata sitelink) against the dump's `<title>` tags.

- Wikidata-linked Wikipedia articles: ~60-70% of A1.1 Q-items have EN sitelinks
  → expected match set: 18,000–42,000 articles
- Articles with `{{Infobox weapon}}`: ~40-60% of matched articles
  → expected infobox rows: 7,000–25,000 with structured fields

### Stream-parse performance

- enwiki dump: ~7M total pages
- Iterparse scans all titles; for non-weapon articles it immediately discards without
  parsing wikitext (title lookup in a Python set is O(1))
- Scan rate: ~10,000 pages/sec on modern hardware
- Total scan time: ~700 seconds = ~12 minutes for full pass
- Per matched page: mwparserfromhell wikitext parse (~1-5ms)
- Total parse time for 42K weapon pages: ~3 minutes
- **Combined A1.2 wall time (excl. download): ~15 minutes**

### Memory profile

- Title set for 60K Wikidata sitelinks: ~3MB (trivial)
- Peak working memory during parse: ~200MB (iterparse + current page wikitext)
- Safely under 4GB; no memory concern

### Match-failure rate

- Wikidata Q-items without EN sitelinks: estimated 30-40% (many are non-English-centric)
- Wikipedia articles with no `{{Infobox weapon}}`: estimated 40-60%
- Articles with no image reference at all: estimated 10-20%
- Net: ~40-50% of A1.1 entries will get Wikipedia enrichment
- Remainder: A1.1 Wikidata description_text is still captured; A1.2 enrichment is additive

---

## A1.3 — Wikimedia Commons Image Metadata Enrichment

### Rate-limit budget

- Wikimedia API etiquette: max 1 req/sec sustained (not published as hard limit;
  recommended in API:Etiquette)
- Daily budget at 1 req/sec: 86,400 calls
- Expected image URLs from A1.1 P18 property: 20,000–40,000
- At 1 req/sec: 20K images = 5.5 hours; 40K images = 11 hours
- **Acceptable: run as overnight background process**
- A1.3 is a point-lookup enrichment pass, not a crawl; each request is a single
  Commons API call returning license + dimensions for one file

### License distribution (expected)

Based on Commons weapon-image population:
- ~25% CC-BY-SA-4.0 or earlier (most Wikipedia infobox images)
- ~15% Public Domain (PD-old, PD-USGov, etc.)
- ~40% CC-BY variants
- ~10% CC0
- ~10% other / unknown

### Failure modes

- 404 on Commons API: file deleted/renamed (log as extraction_error; skip)
- Rate-limit 429: exponential backoff 5s → 10s → 20s → pause 60s → resume
- API response parse failure: log; skip; continue

---

## Summary

| Sub-task | Expected yield | Expected wall time | Risk |
|---|---|---|---|
| A1.1 Wikidata SPARQL | 30K–60K entries | 15–30 min (SPARQL) + 5 min (DB write) | SPARQL timeout on large offsets → fallback to band chunking |
| A1.2 Wikipedia dump | 15K–40K enrichments | 2–5 hours (download) + 15 min (parse) | Bandwidth-bound download; stream-parse is fast |
| A1.3 Commons API | 20K–40K image records | 5–11 hours | Overnight process; rate-limit well within budget |

**Total new `weapon_knowledge_entries` rows: 30K–60K (from A1.1, updated by A1.2)**
**Total new `knowledge_entry_reference_images` rows: 20K–40K (from A1.1 P18 + A1.2 infobox images)**

Mission target contribution from Track A1: 30K–60K entries toward the 100K–200K floor.
Remaining gap (40K–140K) to be covered by Tracks A3, B, G, E, and DISCOVERY next-wave tracks.

---

**Authored by:** legolas (scout)
**Authority:** default (pre-authorized per mission brief §8)
**No jack-ryan Gate-1 required** per mission brief §5.3
