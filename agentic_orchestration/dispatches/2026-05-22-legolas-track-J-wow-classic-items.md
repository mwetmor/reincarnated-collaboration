# Dispatch — legolas — Track J: WoW Classic Items (MMO weapons; MIT-licensed GitHub data)

**Date:** 2026-05-22
**Author:** knight-rider (hive-mind orchestrator)
**For:** legolas
**Pattern:** B (small)
**Status:** FIRING (Wave-2)
**DISCOVERY anchor:** scout-flagged MMO genre fill — 3K-8K weapons from `nexus-devs/wow-classic-items` (MIT-licensed structured JSON; Wowhead itself is RED but pre-extracted data is GREEN)

---

## Required reading

1. Mission doc
2. DISCOVERY scout CSV row for `nexus-devs/wow-classic-items`

---

## Task

Clone `https://github.com/nexus-devs/wow-classic-items`. Parse `data/items.json` (or canonical-named equivalent). Filter for weapons (class=Weapon per WoW item classification). Normalize → `source_library='wow-classic-items'`. Insert.

### Pipeline

1. Shallow clone
2. Locate canonical items JSON (likely `data/` directory; README will clarify)
3. Filter rows where item class is weapon-class (WoW uses class codes; `2` is typically Weapon; verify via README or schema docs)
4. Per item:
   - `canonical_name` = item `name`
   - `source_id` = item `id` or `slug`
   - `source_url` = `https://www.wowhead.com/classic/item=<id>` (informational — we don't crawl Wowhead; this is the canonical reference URL)
   - `description_text` = item `description` / `tooltip` / `flavor_text`
   - `structured_properties` = JSON of: damage, speed, dps, slot, subtype (one-hand/two-hand/ranged), required level, item level, quality, source (boss/drop/quest), etc.
   - `cultural_lineage_tags` = `["mmo", "wow-classic", "fantasy-warcraft"]`
   - `license_class` = `MIT` (data extraction is MIT-licensed code; underlying Blizzard names are trademarks but our use is research/educational substrate)
5. INSERT OR IGNORE; batch every 500
6. Clean up `/tmp/track-J/` after

---

## Discipline #19

Script + nohup + return PID. Expected wall <5 min.

---

## Acceptance criteria

| # | Criterion |
|---|---|
| 1 | ≥3,000 weapon rows inserted with `source_library='wow-classic-items'` |
| 2 | JSON summary at canonical path |
| 3 | Script at `scripts/track_j_wow_classic.py` |

---

**Signed:** knight-rider (Wave-2 fire 2026-05-22)
