# Dispatch — legolas — Track I: Cataclysm Dark Days Ahead (CC-BY-SA modern + improvised weapons)

**Date:** 2026-05-22
**Author:** knight-rider (hive-mind orchestrator)
**For:** legolas
**Pattern:** B (small; fast)
**Status:** FIRING (Wave-2)
**DISCOVERY anchor:** scout-flagged surprise #2 — fills the modern/post-apocalyptic/improvised-weapons genre gap with 1K-3K CC-BY-SA entries.

---

## Required reading

1. Mission doc
2. DISCOVERY scout CSV row for `CleverRaven/Cataclysm-DDA`

---

## Task

Clone `https://github.com/CleverRaven/Cataclysm-DDA` (shallow). Parse weapon-class JSON files under `data/json/items/` (and adjacent paths). Normalize → `source_library='cataclysm-dda'`. Insert.

### Pipeline

1. `git clone --depth 1 https://github.com/CleverRaven/Cataclysm-DDA /tmp/track-I/cataclysm`
2. Walk `data/json/items/` — JSON files containing `"type": "TOOL"` or `"type": "AMMO"` or `"type": "GUN"` or `"type": "GENERIC"` with weapon-flag set (`flags` includes `"WEAPON"`)
3. Per item:
   - `canonical_name` = item `name` field (handle the `name: { str: "...", str_pl: "..." }` shape or simple string)
   - `source_id` = item `id`
   - `source_url` = `https://github.com/CleverRaven/Cataclysm-DDA/blob/main/<relative-path>#L<id-anchor>` (synthetic but stable)
   - `description_text` = item `description` field
   - `structured_properties` = JSON of: damage, range, accuracy, recoil, weight, volume, material, skill, ammo, flags, etc.
   - `genre_appearances` = `["modern", "post-apocalyptic", "improvised"]`
   - `license_class` = `CC-BY-SA-3.0` (per LICENSE file in repo)
4. INSERT OR IGNORE; batch every 500
5. Clean up `/tmp/track-I/` after import

---

## Discipline #19

Script + nohup + return PID. Expected wall <5 min (small repo, local parse).

---

## Discipline #1

Brief math note: `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/track-I-math-note.md`.

---

## Acceptance criteria

| # | Criterion |
|---|---|
| 1 | ≥800 weapon rows inserted with `source_library='cataclysm-dda'` (floor; scout estimated 1K-3K) |
| 2 | License correctly captured as CC-BY-SA-3.0 |
| 3 | JSON summary at canonical path |
| 4 | Script at `scripts/track_i_cataclysm.py` |

---

**Signed:** knight-rider (Wave-2 fire 2026-05-22)
