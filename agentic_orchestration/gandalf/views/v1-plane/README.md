# V1 Plane View — Q19 Plane-Lock Decision Instrument

**Purpose:** One-shot decision instrument for Matt's Q19 plane-lock ruling. Renders both candidate
atlas planes (A = spec 15-cell grid, B = Matt's mock 8-column structure) with all corpus kits
placed, so the ruling is empirical.

**Generated:** 2026-07-12 by synthetic team.

---

## Artifacts

| File | Description |
|---|---|
| `plane_view_v1.png` | Side-by-side render of Plane A and Plane B — 150dpi, dark background, suitable for screen and print review |
| `plane_view_v1.svg` | Same render as vector SVG — scalable, zoomable |
| `occupancy-stats.md` | Per-plane occupancy: occupied/empty cells, per-cell counts, max pileup, concentration (HHI), roster-45 spread |
| `rollup-tables.md` | 24→5 geometry rollup table (Plane A) + Plane B delivery-family mapping table; judgment flags inline; SVG column/row structure extracted verbatim |
| `delta-findings.md` | Top 10 structural disagreements between planes, ranked by kit count affected; no recommendation — plane-lock read is gandalf's |
| `render_v1_plane.py` | Python render script (matplotlib); re-runnable against corpus.db |
| `generate_deliverables.py` | Generates occupancy-stats.md, rollup-tables.md, delta-findings.md |

---

## Input sources

1. `agentic_orchestration/research/curated/corpus.db` — verified corpus DB (463 combat kits, 9 mint, 37 negatives, 45 roster)
2. `agentic_orchestration/gandalf/notes/2026-07-11-atlas-chart-renderer-spec.md` §2.1–§2.4 — Plane A definition
3. `matt_notes_handoff_docs/reap-die-rise-atlas-chart-mock.svg` — Matt's mock (Plane B); column/row text extracted verbatim
4. `canonical/current-to-end-state/substrate-coordinates.md` — Axis 2 definitions grounding the geometry rollup

---

## Plane A summary (spec, 15 cells)

```
              SINGLE    CHAIN   SMALL-AOE  LARGE-AOE  MULTI-SPAWN
INSTANT         86       65        31         174          49
WIND-UP          3        2         0           9           2
CHANNEL          3        5        18           5           2
```

- 14 / 15 cells occupied; 1 empty frontier: `wind-up × small_aoe`
- 9 kits UNMAPPED below grid (teleport=3, NULL=6)
- HHI concentration: 0.222

## Plane B summary (mock, 24 cells)

```
         PROJ  ORBITAL  NOVA  ZONE  BEAM  MELEE  SUMMON  RING
SNAP      109     32    157     8     0     50      49     0
WIND-UP     3      0      9     0     0      2       2     0
CHANNEL     6     12      5     3     3      2       2     0
```

- 17 / 24 cells occupied; 7 empty frontiers (all RING column empty; BEAM/ZONE starved in wind-up)
- 9 kits UNMAPPED (same set as Plane A)
- HHI concentration: 0.208 (slightly more even than Plane A due to MELEE/BEAM/ORBITAL separation)

---

## Key structural disagreement

**Plane A `large_aoe` (188 kits) vs Plane B `NOVA`/`ORBITAL` split:**
Plane B distinguishes delivery *mechanism* (orbital rotation vs nova burst) while Plane A measures
dispersion *outcome* (footprint width). Kits that look similar in outcome are separated by how they
*move* in Plane B. 188 kits affected — the largest single axis of disagreement between planes.

---

## Provenance / data notes

- Plane A rows = `commit_val` from `canon_corpus` (413 instant, 33 channel, 16 wind-up, 1 NULL→instant)
- Plane A cols = 24→5 rollup per `geometry_value` from `canon_engine_key`; see `rollup-tables.md`
- Plane B rows = `SNAP/WIND-UP/CHANNEL` from Matt's SVG mock, mapped to same commit enum
- Plane B cols = delivery-family columns from Matt's SVG mock; overlap between NOVA/ZONE and ORBITAL/RING resolved by first-listed priority in render
- Roster-45: only 5 kits have `commit_slot` pinned (`_` = unknown for remaining 40); committed kits placed; 40 shown as UNMAPPED/commit-unknown in stats
- Negatives (37): have no `canon_engine_key` entry; rendered in UNMAPPED strip only, not in grid
- Mint kits (9): placed in grid by commit+geometry same as corpus; rendered as ★ star markers
