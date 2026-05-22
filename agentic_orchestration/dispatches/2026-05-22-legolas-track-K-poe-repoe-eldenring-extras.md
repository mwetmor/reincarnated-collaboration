# Dispatch — legolas — Track K: PoE RePoE + Elden Ring + Diablo II + GTA-V (multi-source ARPG / open-world bundle)

**Date:** 2026-05-22
**Author:** knight-rider (hive-mind orchestrator)
**For:** legolas
**Pattern:** B
**Status:** FIRING (Wave-2)
**DISCOVERY anchor:** scout-flagged ARPG + open-world genre fills, all GREEN GitHub-hosted with permissive licenses

---

## Required reading

1. Mission doc
2. DISCOVERY scout CSV rows for: `brather1ng/RePoE`, `EldenRingDatabase/erdb`, `deliton/eldenring-api`, `blizzhackers/d2data`, `DurtyFree/gta-v-data-dumps`

---

## Task

Clone the following 5 repos in parallel (or serial; whichever your script prefers). Parse each per its canonical weapon-data file. Normalize → `source_library` per source. Insert.

### Per-source mapping

| source_library | Repo | Genre tag | Expected yield |
|---|---|---|---|
| `path-of-exile-repoe` | brather1ng/RePoE | `fantasy-arpg-poe` | 1K-5K (base_items.json + per-mod data) |
| `elden-ring-erdb` | EldenRingDatabase/erdb (and deliton fallback) | `fantasy-soulslike-elden-ring` | 200-400 |
| `diablo2-d2data` | blizzhackers/d2data | `fantasy-arpg-d2` | 500-1K |
| `gta-v-data` | DurtyFree/gta-v-data-dumps | `modern-open-world-gta` | 200-500 (weapons subset) |

### Per-source pipeline

For each repo:
1. Shallow clone
2. Locate canonical weapon-data file(s) per repo's README
3. Per weapon entry: extract canonical_name, structured_properties (game-specific stats), description, license tier from LICENSE file
4. INSERT OR IGNORE with `source_library` per the table above; batch 500
5. Clean up tmp dir after

---

## Discipline #19

Script + nohup + return PID. Expected wall <15 min for all 5 repos serial.

---

## Acceptance criteria

| # | Criterion |
|---|---|
| 1 | ≥1,500 total weapon rows inserted across all 5 source_library tags |
| 2 | Per-repo JSON summary inside aggregate JSON at `summaries/track-K-wave1.json` |
| 3 | Script at `scripts/track_k_multi_arpg.py` |
| 4 | License per repo recorded correctly |

---

**Signed:** knight-rider (Wave-2 fire 2026-05-22)
