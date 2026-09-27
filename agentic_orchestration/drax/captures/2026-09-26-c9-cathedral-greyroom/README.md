# C-9 · P2′ — the cathedral grey room on the Crucible arena

**Seat:** drax (presentation seam) · **Date:** 2026-09-26 · **Gate:** **M2 — Matt approves this
grey room BEFORE any cathedral paint** (R-C3-55a).
**Work order:** `agentic_orchestration/dispatches/2026-09-26-drax-c9-cathedral-greyroom.md`
**Governing run text:** `agentic_orchestration/gandalf/notes/2026-09-26-illuminated-archive-run-C-9-charter.md`, phase P2′.

**Nothing was painted. No burst fired. Godot was not launched. Nothing was pushed.**

---

## 1. The one image to look at

`M2_review_cathedral_greyroom.png` — the grey room beside the measured arena trace, the mapping
numbered 1–6 on both halves, and the three things that are open at M2 printed along the bottom.

---

## 2. What is in this directory

| File | What it is |
|---|---|
| `guide.png` | the flat-shaded orthographic guide the painter paints over (scene-builder-workflow § 3 step 1) |
| `id_mask.png` | flat index colours, 17 classes, NEAREST only |
| `depth_mm.png` | uint16, **millimetres of ELEVATION above the arena floor plane** |
| `walkable_mask.png` | white = play space. Clipped 24 px inside the canvas (R-C3-58) |
| `dot_zone_mask.png` | the six rot zones — **the disc the guide and the ID mask carry** |
| `dot_zone_mask_upper_bound.png` | the same six at their raw radius upper bound — an **envelope**, not a claim |
| `greyroom_manifest.json` | every number, every provenance, every declared value, the chunk grid, output digests |
| `M2_review_cathedral_greyroom.png` | the M2 packet image |
| `make_cathedral_greyroom.py` | the generator. Re-runs from the sha-pinned geometry file; no hand-placed pixels anywhere |
| `make_review_image.py` | the review composer |

Deliverables are **mirrored** to `agentic_orchestration/drax/captures/2026-09-26-c9-cathedral-greyroom/`
because `astra_test_01/.gitignore` ignores `*.png`; that mirror is what is committed, matching the
KC2-PLAY arena-guide precedent.

**Re-run:** `python3 make_cathedral_greyroom.py && python3 make_review_image.py`, under the shared
heavy lock. `C9_PPM_SCALE=0.22` runs the whole pipeline small for debugging and writes to `_debug/`;
its outputs are not deliverables and the plate-law cross-check is skipped so you can tell.

---

## 3. The camera and the canvas

| | |
|---|---|
| Camera | the ratified GD `player_lock`: **yaw 47°, pitch α = 52.9535411256°**, orthographic |
| px/m east | **100.617554** → **0.0099386 m/px** |
| px/m south (ground) | **80.307625** → **0.0124521 m/px** |
| px/m up-screen (elevation) | **60.618294** |
| Canvas | **7776 × 7522 px** = **77.285 × 93.665 m** |
| Arena inside it | **57.285 × 76.665 m** at **u = 0.285 m per native minimap px** |

The plate scale is READ from the cliffside plate (`blockout_meta_v2.json :: ortho_canvas_v2`,
R-C3-44), not retyped, and the generator **refuses to run** unless that plate's two independently
ruled px/m figures fall out of α to better than 1e-6. They do.

**On "Keeper scale 130 px at 1080p".** The dispatch names it; it is the **cliffside** convention and
it implies a **2.1446 m** body. KC2-PLAY **KP-18 (a)** already ruled, for this arena, that
`h_fig = 1.9 m` stands and that the 130 px figure is *not* inherited — a register-divergence row,
not a body height. This canvas adopts the **plate scale** (which is what "130 px at 1080p" actually
pins) and the manifest carries **both** figures so neither can be quietly re-quoted as the other.
A 1.9 m figure is **115.175 px** on this plate. Flagged, not silently resolved.

**`u = 0.285`** comes from KC2-PLAY KP-6 (ratified KP-9). The geometry file's own `scale` block
(0.1981, `DERIVED-WEAK`) is **ignored** per the dispatch and Gate-1 WARN-8.

---

## 4. The mapping, and how each row was derived

| # | Arena feature | Cathedral element | Class | Derived from |
|---|---|---|---|---|
| 1 | North corridor + red door (spawn) | Entry through the choir screen into the crossing | `screen_passage` | floor north of `y_join`, inside the passage's own measured x-extent |
| 2 | Central oval | The crossing under the lantern — brightest floor | `crossing` | floor from `y_join` to the choir band |
| 3 | NW / NE lobes | The transept arms | `transept_w` / `transept_e` | floor north of `y_join`, outside that x-extent |
| 4 | Two long thin E/W interior walls | Choir stalls | `choir_stall` | OB-1 (west), OB-2 (east) polygons, **verbatim** |
| 5 | SW / S / SE lobes + the two small S islands | Ambulatory chapels; the altar and a tomb | `ambulatory_floor`, `sanctuary_floor`, `altar`, `tomb` | floor south of the choir band; OB-3 = altar, OB-4 = tomb |
| 6 | Six green DoT zones | Rot-soaked chapel floor — **enterable, never collision, never a pit** | `rot_zone` (walkable) | measured interior point + radius bound, clipped to floor |

Three cuts do all the partitioning, and all three come out of the geometry rather than off a ruler:

- **`y_join`** — the northernmost row whose widest single run of floor reaches **75 %** of the
  arena's widest run. "The transept arms have joined the passage."
- **The screen passage's x-extent** — the ring's own x-extent over the rows that are *corridor
  only*: north of the join, carrying no floor beyond their own widest run. A row that also holds a
  lobe carries more floor than its widest run does, and drops out.
- **The choir band** — the y-extent of OB-1 and OB-2, the two islands the mapping already calls
  choir stalls. The **sanctuary** is the south floor within one bay of OB-3 ∪ OB-4.

Everything below one native pixel is filtered as rasterisation noise, at a grain of **2.5 native
px** — the ring's *own* stated uncertainty (`hard_boundary.uncertainty_native_px`). Without that
filter the arena's very first row reports two runs from a sub-pixel notch at the top vertex and the
passage comes out 7.3 m wide instead of 13.1 m.

---

## 5. Antwerp on a blobby ring — the one structural consequence

Antwerp's interior is a **forest of piers**, in a grid, standing on the floor. **None of them can
stand on this floor**: every pier on the arena floor is a hole in the walkable mask, and the mask is
the measured arena.

So the arcade is pushed **out to the ring line**, and the reading that falls out is the correct one:

```
   the measured ring  =  the arcade line
   inside it          =  nave vessel / crossing / choir / sanctuary / ambulatory  — WALKABLE
   the ring itself    =  a 0.9 m dado (the choir-screen parapet): why the edge IS an edge
   just outside       =  the arcade piers, one per bay
   beyond them        =  aisle (4.5 m) — dead space, and the brief's preferred home for seams
   beyond that        =  outer wall, with radiating chapels every other bay, running off the canvas
```

The only piers inside the play space are the four the arena already has: the two choir stalls and
the altar and the tomb.

**Bay = 6.5645 m**, and it is not a number off the plan. The plan has no scale bar, so nothing metric
is imported from it; what is taken is a **proportion** — Antwerp's square aisle bays, the standard
Gothic double-bay relation, giving bay = ½ the central vessel. The vessel is **measured**: 13.129 m,
the screen passage's own width. **69 bays** around a **449.989 m** ring.

*(Worth noting and not load-bearing: 13.13 m is about Antwerp's own nave-vessel width. Nothing here
depends on that; the number came from the arena.)*

---

## 6. Brief § 4 conventions, and how each is enforced

| Rule | How |
|---|---|
| **Full-bleed, no void, no border** | every pixel of the canvas carries a class. There is no `#00ff00` plate in this mask and no sky — **this interior has none**. Architecture is cut by all four edges. |
| **Near side cut low** | an element is cut to **0.9 m** *iff raising it would occlude play space* — i.e. iff the play floor (plus the dado and aisle that read as its edge) lies within the rise distance NORTH of it. Up-screen is north, so **the near side cuts itself**. There is no list of faces anywhere in the generator. |
| **Back walls exit the frame** | masonry that does not occlude rises **6.0 m** and is cut by the canvas top. 6.0 m is not invented: it is the wall-face elevation allowance already ruled for *this arena* at KC2-PLAY **KP-18 (b)**. |
| **Seams hide in dead space** | the chunk-grid **origin** is chosen by search to put the least walkable floor under the seams — constrained so it can never buy a better seam with an extra row or column. |
| **Walkable = brightest and calmest** | every walkable class is greyer-than-195 in the guide; every non-walkable class is below 140. The lantern is annotated over the crossing centroid. |

**The vault is not on this plate**, deliberately. At 60.6 px/m up-screen a true Antwerp springing
would cover the northern half of the canvas. It belongs on the **Overhead layer (z3)**
(scene-builder-workflow § 3 step 7 / T3l). So does the **choir screen** across the entry: a screen
with a doorway would punch a hole in the walkable mask, so it is painted as an **arch over** the
passage with **no footprint**. Both are annotated on the guide and declared in the manifest.

---

## 7. The three things open at M2

### (a) The rot extent — the one place I made a call

The geometry file gives **interior points (measured)** and **radius UPPER BOUNDS**; extents are
`EXTENT-UNMEASURED` because the ground map M is unrecoverable from the 21 capture stations. An upper
bound is not an estimate, and at the raw bound:

- the six discs cover **46.9 %** of the walkable floor — against brief § 4 *"walkable = brightest and
  calmest"*;
- **and they overlap each other** — against the geometry file's own finding that **six mutually
  distinct zones are demonstrated**.

So the raw bound is inconsistent with the file that supplies it. `k_disjoint = 0.5345` is the largest
uniform scale at which all six stay pairwise disjoint (binding pair **Z-622 / Z-623**) — the largest
value consistent with *both* facts. **`guide.png`, `id_mask.png` and `dot_zone_mask.png` carry
k_disjoint** (**23.5 %** of the floor). The raw bound ships beside them as
`dot_zone_mask_upper_bound.png` and is drawn on the guide as a dashed green **envelope**: the rot is
inside that line, nowhere else.

**This is drax's call, not a measurement. M2 may overrule it in either direction** — and if the real
answer is wanted rather than bounded, the geometry note names two decode paths for the zones.

### (b) Paint cost

**60 chunks** (6 × 10 of 1536 × 1024 with 256 px overlaps) — **60 images per style arm**, 120 for the
A/B, against a run cap of 400 that also has to fund P5's cliffside re-derivation. The conductor may
prefer the **ZOOM-GD precedent** (KP-B1a: paint at 0.752040 × plate and upscale 1.329717 ×), which
brings it to roughly 35 per arm at the cost of a resample. **Conductor's call, not mine** — the grey
room is at plate scale either way, and the manifest carries the chunk rects for both readings.

### (c) What the walkable mask asserts that nobody has demonstrated

The mask makes the whole ring interior walkable, the north corridor included. The geometry file flags
**two arcs (vertices 0–8 and 174–176) as mapped but never walked** — *"the minimap painted this arc
from a distance… its WALKABILITY was never demonstrated by the player's own body. Both runs lie on
the north corridor and its terminal chamber, which Matt approached but did not enter."*

That corridor is exactly what the mapping turns into the **spawn entry**. The grey room treats it as
walkable because the mapping requires it; the trace panel of the review image draws those two arcs
**dashed red** so the assumption is visible rather than buried.

---

## 8. Declared, not decoded

Every metre figure that has no measurement behind it, printed here and in the manifest:

| | m | why |
|---|---|---|
| surround W / E / S | 10.0 | aisle + outer wall + the first chapel; the rest runs off the edge |
| surround N | 7.0 | the back wall exits the top edge — it is cut, not framed |
| dado band | 1.2 | the parapet standing **on** the measured ring. Inner edge load-bearing, outer edge free |
| aisle | 4.5 | dead space |
| aisle wall | 1.5 | masonry skin between aisle and chapels |
| chapel half-depth | 2.5 | radiating / side chapels, every other bay |
| pier | 1.6 | square in plan, just outside the dado |
| near cut | 0.9 | D2-style knee/waist break |
| wall rise | 6.0 | **reused**, not invented — KP-18 (b) for this arena |
| choir stall / altar / tomb | 1.2 / 1.0 / 0.9 | furniture heights |
| lantern radius | 9.0 | **annotation only** — no footprint, no class |
| bay ratio | 0.5 (–) | a proportion off the Antwerp plan; the length it multiplies is measured |

---

## 9. Round-trip

**Not applicable.** No engine contract changes. If `walkable_mask.png` is later swapped into the
KC2-PLAY runtime as a skin over the same geometry (R-KP-0c makes the arena a swappable data object),
that swap is a separate dispatch.
