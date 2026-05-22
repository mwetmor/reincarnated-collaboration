# Dispatch — legolas — Track M: GitHub Tabletop + Supplemental Bundle (Pf2ools + Warhammer + 5e-2024 + Souls + MTG-WoW supplements)

**Date:** 2026-05-22
**Author:** knight-rider (hive-mind orchestrator)
**For:** legolas
**Pattern:** B
**Status:** FIRING (Wave-3)
**DISCOVERY anchor:** scout-flagged GREEN GitHub-hosted data repos covering tabletop + missing 5e edition + soulslike supplement

---

## Required reading
1. Mission doc
2. `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/discovery-wave1.csv`

---

## Task

Clone + parse + insert 5 supplemental GitHub data repos. ALL via raw.githubusercontent.com CDN where possible (no clone needed).

### Per-source mapping

| source_library | Repo | Genre | Expected |
|---|---|---|---|
| `pf2ools-pf2ools-data` | `Pf2ools/pf2ools-data` | Pathfinder 2e | ~200 weapons |
| `5e-bits-5e-database-2024` | `5e-bits/5e-database` (2024 dir, `src/2024/`) | D&D 5e 2024 edition | ~50 weapons |
| `bsdata-warhammer-aos` | `BSData/warhammer-age-of-sigmar` | Tabletop fantasy | ~500-1K weapons |
| `souls-api-thomaslincoln` | `ThomasLincoln/Souls_API` | Dark Souls (alt to fextralife) | ~200 |
| `kaggle-ds3-weapons` (skip if requires Kaggle auth) | Kaggle Dark Souls III weapons CSV | Soulslike | ~200 |

### Per-source pipeline

For each repo:
1. Probe README to locate canonical data path
2. Fetch JSON/YAML/CSV via raw.githubusercontent.com (preferred) or shallow clone if URL-fetch fails
3. Parse + normalize → INSERT OR IGNORE batch 500
4. License from LICENSE file (default: `unknown` if missing)

### Edge cases

- 5e-bits 2024 edition shares the SAME repo as the existing Track G ingestion (which used main branch). Add the `src/2024/` items via separate source_library tag to avoid collision.
- BSData Warhammer AoS: uses Battlescribe XML schema; parse `*.cat` (catalogue) files for unit weapon profiles
- Kaggle: skip if API key required; this is the lowest-priority entry
- ThomasLincoln/Souls_API: unknown license; record as `unknown` per schema

### Discipline #19

One consolidated script `track_m_supplemental_bundle.py`; fire nohup; return PID + paths.

### Discipline #1

Math note: `track-M-math-note.md` — per-source yield + license + parse-strategy.

### Acceptance

| # | Criterion |
|---|---|
| 1 | ≥800 total rows across all 5 source_library tags |
| 2 | At least 3 of 5 sources contribute rows (the others can fail gracefully if data structure unclear) |
| 3 | JSON summary at canonical path |
| 4 | License per source recorded |

---

**Signed:** knight-rider (Wave-3 fire 2026-05-22)
