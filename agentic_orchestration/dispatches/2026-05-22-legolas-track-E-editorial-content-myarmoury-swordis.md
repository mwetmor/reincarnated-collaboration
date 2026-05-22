# Dispatch — legolas — Track E: Editorial / Community Sites with Geometry + Cross-Section Detail (MyArmoury, Swordis, ...)

**Date:** 2026-05-22
**Author:** knight-rider (hive-mind orchestrator)
**For:** legolas
**Pattern:** B (long task; robots-verify-first, then crawl-with-delay)
**Status:** ROBOTS-PENDING (Wave 1; fires AFTER robots verification step returns GREEN/GREEN-with-CAUTION)
**Mission:** `agentic_orchestration/weapon-library-import-hive-mind-mission-2026-05-22.md`

---

## Required reading

1. Mission doc (above)
2. Schema: `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` v1.1.0
3. Existing robots-verification log: `agentic_orchestration/logs/2026-05-22-evening-robots-verification.md`

---

## Task

Verify robots-status + license for editorial/community sites with high-quality geometry/cross-section/photographic detail on weapons (especially historical), then crawl GREEN sites with appropriate delays. Insert to `weapon_knowledge_entries` with `source_library='myarmoury'` / `'swordis'` / etc.

### Matt-named seed list

| Source | URL (find canonical) | Matt's note |
|---|---|---|
| MyArmoury | https://myarmoury.com/ | "Geometries and cross sections" — very promising |
| Swordis Global Weapon Index | (find canonical URL — likely swordis.com or similar) | "Looks very promising with geometries and cross sections" |

### Step 0 — robots + license verification (MANDATORY before any crawl)

For each seed site:

1. Fetch `https://<site>/robots.txt` with research-agent UA
2. Check for `User-agent: ClaudeBot` Disallow + `User-agent: anthropic-ai` Disallow
3. Extract Crawl-delay (if any)
4. Fetch site `/about`, `/terms`, `/legal`, `/copyright`, `/credits` (one of these usually exists) to determine content license / reuse permission
5. Record in `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/track-E-robots-verification.md`:
   - URL probed
   - ClaudeBot status
   - Crawl-delay
   - License/reuse statement found (or "not found")
   - Disposition: GREEN / GREEN-with-CAUTION / AMBER / RED
6. Update `agentic_orchestration/weapon-library-import-hive-mind-state.md` Track E row with the verification outcome

### Step 1 — IF GREEN/GREEN-with-CAUTION: fire crawl

For each GREEN/GREEN-with-CAUTION site:

1. Author crawl script: traverse weapon-category index → per-weapon-page extract (title, description, structured properties from infobox if present, image URLs, references/citations)
2. Honor Crawl-delay × 1.5 safety margin
3. Use research-agent UA (`reincarnated-engine/0.1 (research; mhwetmore@gmail.com)`)
4. Insert per-weapon row: `weapon_knowledge_entries` (`source_library='myarmoury'` etc.) + `knowledge_entry_reference_images` for each image URL (URL-only; don't download bytes)
5. Fire as nohup background process; expect long wall-time due to crawl-delay (MyArmoury could be hours; small-site Swordis may be faster)

### Step 2 — IF AMBER: defer + flag

- AMBER sites are NOT crawled in Wave 1
- Log the AMBER status in the verification doc with the specific signal that prompted AMBER
- Flag in hive-mind state file open-blockers for Matt judgment in next briefing

### Step 3 — IF RED: drop

- RED sites are removed from this dispatch's scope
- Log the RED status with the explicit Disallow / Cloudflare / 429 signal that prompted RED
- Add to the canonical RED-source registry (`agentic_orchestration/logs/2026-05-22-evening-robots-verification.md` updates)

---

## Discipline #19 compliance

- Robots-verification step is a short interactive Bash + WebFetch session (no background process; completes in minutes)
- If GREEN crawl fires: nohup background; return PID + log path + JSON summary path to knight-rider; knight-rider polls on-demand
- Logs: `/Users/admin/Games/reincarnated-engine/logs/weapon-library-track-E-<site>.log`
- JSON summaries: `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/summaries/track-E-<site>-wave1.json`

---

## Discipline #20 compliance

- This dispatch is **structured around Discipline #20 first** — no fetch until robots/license verification completes
- Crawl-delay is the floor; we add 50% safety margin
- If sustained 429 mid-crawl: graceful pause + reassess; possible AMBER reclassification
- Track E ROBOTS-PENDING state in the state file UNTIL verification returns

---

## Discipline #1 (math-before-code)

Brief math note (single page):
- For each GREEN site: estimated weapon-entry count × crawl-delay = expected wall time
- Failure modes: site structure change mid-crawl; image hotlink protection; rate-limit escalation
- Bandwidth profile (URL-only image storage keeps this minimal)

Math note: `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/track-E-math-note.md`

---

## Acceptance criteria

| # | Criterion |
|---|---|
| 1 | Robots/license verification documented for MyArmoury + Swordis + every site you add from DISCOVERY |
| 2 | Each GREEN/GREEN-with-CAUTION site fires a crawl (background; need not complete during the dispatch's active phase) |
| 3 | Each crawl writes ≥1 row to `weapon_knowledge_entries` (proves pipeline integrity) — actual yield depends on site |
| 4 | All AMBER + RED sites logged with explicit disposition reason |
| 5 | JSON summaries per site at canonical paths |
| 6 | Hive-mind state file Track E row updated with verification + crawl-fire status |
| 7 | NO crawl initiated against any RED or AMBER site |

---

## Out of scope

- Wave-2 sites surfaced by DISCOVERY scout (those become their own tracks; this dispatch is Matt-seed-list-anchored)
- Aggressive crawl strategies that ignore Crawl-delay
- Negotiating with site owners (deferred; Matt's call if/when)

---

## Cross-references

- Mission: `agentic_orchestration/weapon-library-import-hive-mind-mission-2026-05-22.md`
- DISCOVERY dispatch: `dispatches/2026-05-22-legolas-DISCOVERY-source-scouting.md`
- Existing robots verification: `agentic_orchestration/logs/2026-05-22-evening-robots-verification.md`

---

**Signed:** knight-rider (hive-mind orchestrator; Wave-1 fire 2026-05-22)
