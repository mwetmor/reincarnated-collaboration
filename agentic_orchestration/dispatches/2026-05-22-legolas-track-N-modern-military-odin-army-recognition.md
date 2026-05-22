# Dispatch — legolas — Track N: Modern Military (ODIN US Army TRADOC + Army Recognition + Wikipedia Firearms supplement)

**Date:** 2026-05-22
**Author:** knight-rider (hive-mind orchestrator)
**For:** legolas
**Pattern:** B
**Status:** FIRING (Wave-3)
**DISCOVERY anchor:** scout-flagged modern military gap-fill — ODIN is US gov public domain; Army Recognition + globalmilitary.net are AMBER-probe candidates

---

## Required reading
1. Mission doc
2. DISCOVERY CSV rows for ODIN, Army Recognition, globalmilitary.net

---

## Task

Modern military weapon coverage. Multi-source — robots-verify each before crawl. Insert with appropriate `source_library` per source.

### Sources (priority order)

| source_library | Source | Pre-action | Expected |
|---|---|---|---|
| `odin-army-tradoc` | `odin.tradoc.army.mil` (US Army Worldwide Equipment Guide) | Robots-verify first; expected GREEN as US gov public domain | 1K-5K |
| `army-recognition` | `armyrecognition.com/military-products/army/weapons` | Robots-verify | 500-2K |
| `globalmilitary-net` | `globalmilitary.net/firearms/` | Robots-verify | 200-1K |
| `small-arms-survey-db` | `smallarmssurvey.org/databases` | Robots-verify + probe what's public | 0-500 |

### Pipeline

For each source:
1. Fetch `robots.txt` with research-agent UA; check ClaudeBot Disallow
2. If RED: log + drop
3. If AMBER: probe one sample weapon page; if returns 200 with structured content, proceed as GREEN-with-caution at 5s/request
4. If GREEN: crawl per source's site structure (index → per-weapon page), normalize, insert

### Discipline #20

- ODIN is US gov; expected fully GREEN as public-domain federal work
- Other 3 sources are AMBER pending robots probe; defer to next-wave if RED
- All probes use research-agent UA; NEVER ClaudeBot

### Discipline #19

One script per source (or consolidated multi-source script with per-source modules); fire each as nohup; return PIDs + paths.

### Discipline #1

Math note: `track-N-math-note.md`. Per-source robots-status outcome + crawl wall-time + yield estimate.

### Acceptance

| # | Criterion |
|---|---|
| 1 | All 4 sources robots-verified + dispositioned in math note |
| 2 | ODIN crawl fired if GREEN; ≥500 modern military rows from ODIN alone |
| 3 | ≥800 total rows across all GREEN sources in Track N |
| 4 | RED/AMBER sources logged with disposition reason |
| 5 | JSON summary at canonical path |

---

**Signed:** knight-rider (Wave-3 fire 2026-05-22)
