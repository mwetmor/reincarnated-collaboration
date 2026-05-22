# Dispatch — legolas — Track L: Fextralife Soulslike Bundle (DS1/DS2/DS3/BB/ER)

**Date:** 2026-05-22
**Author:** knight-rider (hive-mind orchestrator)
**For:** legolas
**Pattern:** B
**Status:** FIRING (Wave-3)
**DISCOVERY anchor:** scout flagged Fextralife as GREEN-with-caution (ClaudeBot absent from robots; only GPTBot blocked). ~1,500 weapons across 5 soulslike titles.

---

## Required reading
1. `agentic_orchestration/weapon-library-import-hive-mind-mission-2026-05-22.md`
2. `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/discovery-wave1.csv` (Fextralife rows)

---

## Task

Crawl Fextralife soulslike weapon catalogues. Normalize per-title. Per-page schema: name, image URL(s), weapon-type, scaling stats, requirements, lore text, drop locations.

### Per-title subdomain + index path

| source_library | Subdomain | Catalogue index | Expected |
|---|---|---|---|
| `fextralife-ds1` | `darksouls.wiki.fextralife.com` | `/Weapons` | ~120 |
| `fextralife-ds2` | `darksouls2.wiki.fextralife.com` | `/Weapons` | ~220 |
| `fextralife-ds3` | `darksouls3.wiki.fextralife.com` | `/Weapons` | ~190 |
| `fextralife-bloodborne` | `bloodborne.wiki.fextralife.com` | `/Weapons` | ~25 |
| `fextralife-elden-ring` | `eldenring.wiki.fextralife.com` | `/Weapons` | ~408 |

### Pipeline per title

1. Fetch index page; parse weapon list (anchor links)
2. Per weapon: fetch page; parse infobox-equivalent + body
3. Normalize → `weapon_knowledge_entries` with title-specific source_library, image URLs (URL-only), `cultural_lineage_tags=["soulslike", "<title>"]`, `genre_appearances=["fantasy-soulslike"]`
4. INSERT OR IGNORE; batch every 50

### Discipline #20

- Fextralife is GREEN-with-caution; ClaudeBot is absent (not Disallowed but not explicitly Allowed) 
- Use research-agent UA (`reincarnated-engine/0.1 (research; mhwetmore@gmail.com)`); NOT ClaudeBot
- No documented Crawl-delay; default to 1 req/sec sustained (~30 min total wall for 1.5K weapons across 5 titles)
- If observe 429: back off exponential; sustained 429 → pause + flag

### Discipline #19

Author script → nohup background → return PID + paths.

### Discipline #1

Brief math note: `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/track-L-math-note.md`

### Acceptance

| # | Criterion |
|---|---|
| 1 | ≥1,000 rows total across 5 source_library tags |
| 2 | Each title has ≥1 row (proves per-title pipeline works) |
| 3 | License `editorial_only` or `fan-wiki` (Fextralife content is fan-curated; not CC-licensed) |
| 4 | JSON summary at canonical path |

---

**Signed:** knight-rider (Wave-3 fire 2026-05-22)
