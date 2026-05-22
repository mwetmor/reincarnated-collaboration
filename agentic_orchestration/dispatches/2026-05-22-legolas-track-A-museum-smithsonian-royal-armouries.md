# Dispatch — legolas — Track A2 + A3: Museum Knowledge Crawls (Smithsonian API + Royal Armouries)

**Date:** 2026-05-22 (authored overnight)
**Author:** knight-rider (overnight cascade per Matt 2026-05-22 evening authorization)
**For:** legolas
**Pattern:** B (long task; dedicated session)
**Status:** PARTIAL-BLOCK — Smithsonian portion gated on Matt providing `SMITHSONIAN_API_KEY`; Royal Armouries portion ready to fire
**Required reading first:**
1. `agentic_orchestration/logs/2026-05-22-evening-robots-verification.md`
2. `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` v1.1.0
3. `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/library-enumeration.md` (museum entries section)

---

## Context

Per overnight robots.txt verification:

| Source | Status |
|---|---|
| Smithsonian si.edu (site crawl) | **RED** — explicit ClaudeBot Disallow |
| Smithsonian Open Access **via api.data.gov API** | **GREEN** — API path is the authorized route |
| Royal Armouries royalarmouries.org | **GREEN with 20-sec Crawl-delay required** |
| Met Museum metmuseum.org (site crawl) | **RED** — explicit ClaudeBot Disallow (Met Open Access API is separate and not probed tonight; out of scope) |

Two museum sources viable. Both populate the `weapon_knowledge_entries` table with culturally-diverse historical-weapon entries — the substrate-region the Wikipedia/Wikidata pull is weakest on.

---

## Sub-task A2 — Smithsonian Open Access via api.data.gov

**STATUS: BLOCKED pending Matt providing `SMITHSONIAN_API_KEY` env var (per skill_handoff C4 carry).**

**Approach (when unblocked):**
1. Register at https://api.data.gov/signup/ (Matt-side; ~5 min)
2. `export SMITHSONIAN_API_KEY="..."` in shell (persist to `~/.zshrc` per the canonical env-var pattern; same as MESHY_API_KEY discipline)
3. Smithsonian Open Access API base: `https://api.si.edu/openaccess/api/v1.0/`
4. Query pattern (per https://edan.si.edu/openaccess/apidocs/):
   ```
   GET https://api.si.edu/openaccess/api/v1.0/search?api_key=$KEY&q=object_type:weapon&rows=100&start=0
   ```
5. Paginate via `start` offset; structured response with `culture` field (the uniquely-authoritative-for-non-European-cultural-register field per legolas's prior research)
6. Per result: INSERT `weapon_knowledge_entries` row with source_library='smithsonian'; rich structured_properties; cultural_lineage_tags from `culture` field; museum image URL(s) into `knowledge_entry_reference_images` (license CC0)
7. Target: 100-400 weapon entries
8. Runtime: ~1 hour at conservative API pacing

**Discipline #19 compliance:** nohup background; logs at `~/Games/reincarnated-engine/logs/knowledge_crawl_smithsonian.log`; JSON summary at `~/Games/reincarnated-engine/logs/knowledge_crawl_smithsonian_summary.json`

---

## Sub-task A3 — Royal Armouries direct crawl

**STATUS: READY TO FIRE** (no Matt-side blocker; robots.txt verification GREEN with Crawl-delay: 20)

**Approach:**
1. Discover entry-point pattern: Royal Armouries collections at https://royalarmouries.org/collection/ — survey site structure to find weapon-category listing URLs
2. Use a standard HTTPS GET pattern (NOT Claude-agent User-Agent; use a descriptive research UA: `reincarnated-engine-research/0.1 (mhwetmore@gmail.com)`)
3. **CRITICAL: honor Crawl-delay: 20 (20 seconds between requests)** — this is non-negotiable per robots.txt
4. At 20s/request, throughput is ~180 requests/hour = ~1,000-4,000 entries possible over a 6-24 hour run
5. Parse each entry page: title, description, structured fields (period, country, material, dimensions where present), image URL
6. INSERT into `weapon_knowledge_entries` with source_library='royal_armouries'; INSERT image URLs to `knowledge_entry_reference_images` (license per page; many Royal Armouries items have non-CC licenses — capture them honestly; do NOT default to permissive)

**Estimated yield:** 200-1,000 weapon entries (slow but high-quality cultural register coverage)

**Discipline #19 compliance:** nohup background; logs at `~/Games/reincarnated-engine/logs/knowledge_crawl_royal_armouries.log`; JSON summary at `~/Games/reincarnated-engine/logs/knowledge_crawl_royal_armouries_summary.json`; checkpoint by `MAX(id)` query

**Runtime warning:** This is a multi-hour to overnight job. Plan around it accordingly. Resumable from checkpoint on restart.

---

## Math-before-code (Discipline #1)

Before writing the crawl scripts:
- **Royal Armouries:** sample 5-10 entry-page URLs; characterize HTML structure (consistent template?); estimate per-page useful-field-extraction rate; estimate total catalogue size from any sitemap or category-pagination metadata
- **Smithsonian (when unblocked):** confirm API response schema; sample 10 weapon entries; characterize cultural-tag distribution to validate the "uniquely authoritative for non-European registers" hypothesis

Math note at `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/track-A2-A3-math-note.md`.

---

## Acceptance criteria

### A2 (Smithsonian) — when unblocked
- ≥100 weapon_knowledge_entries with source_library='smithsonian'
- ≥70% of those have ≥1 reference image with CC0 license
- ≥50% have non-European cultural_lineage_tags populated
- JSON summary at canonical path

### A3 (Royal Armouries)
- ≥200 weapon_knowledge_entries with source_library='royal_armouries'
- License metadata captured per image (do NOT default to CC0)
- 20-sec crawl delay confirmed via timestamp distribution in log
- JSON summary at canonical path

---

## Out of scope

- Met Museum (separate dispatch; needs Met Open Access API probe first)
- British Museum / Victoria & Albert (not probed tonight)
- Smithsonian site-direct crawl (RED per robots; API only)
- Any source where ClaudeBot is Disallow-listed

---

## Tag intent

- A2 completion: `legolas/v0.2-track-A2-knowledge-crawl-smithsonian-1`
- A3 completion: `legolas/v0.2-track-A3-knowledge-crawl-royal-armouries-1`

---

**Signed:** knight-rider (overnight cascade)
