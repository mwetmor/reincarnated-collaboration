# The Frost King's Barrow, full area: the blockout spec (T10-2, step 1)

> **STATUS:** CURRENT, **v2** (corrected after the first blockout, commit `1e4cf69c2`; see § 6). Author gandalf (SCENEWRIGHT + SPEC-AUTHOR), 2026-09-29, Run C-9 Phase 2.
> **Authority:** R-C9-75 (Matt: *"Yes, please set up the full scene that way"*): blockout first, painted over chunk by chunk, then built. R-C9-74 rules bind: flat play floors, elevation only by architected steps.
> **Gate:** Matt reviews the top-down map and walks the greybox **before any painting**.

## 1 · Frame and units

- **Units are true metres.** Every asset keeps its measured size (stone_tall 2.71 m, stone_mid 2.71 m, stone_short 1.24 m, lintel 2.28 m across, post 2.04 m, rock_large 1.84 m, birch 3.36 m, juniper 1.15 m, the barbarian 1.85 m).
- **Layout coordinates (u, v)** lie on the ground:
  - **+u** is screen-right and **+v** is up-screen (away from the camera), both taken from the play camera's own basis projected onto the ground and normalised;
  - the origin (0, 0) is the layout origin; **the arena is centred at (0, 1)**;
  - world = origin + u·û + v·v̂.
  - θ below is measured clockwise from +v.
- **Guide window (v2): the 4 × 4 chunk grid**, 1536 × 1024 canvases at a 1280 × 768 stride = **5376 × 3328 px**. At the play camera's scale (100.6176 px/m across, 80.3076 px per ground metre up-screen) that is 53.43 × 41.44 m, centred at (−2, −3.0): **u ∈ [−28.72, +24.72], v ∈ [−23.72, +17.72]**.
- **Why 4 × 4:** the camera is centred on him. Every walkable point needs at least half a screen of painted world around it: 9.54 m across and 6.72 m up-screen. The 3 × 3 window left up to 7 m of unpainted world in frame at the edges.
- **The margin beyond the play bounds is scenery,** non-walkable and flat: outcrops, tree lines, scrub, the tarn's far shore, the mound's back.

## 2 · The four beats (bottom to top, the way he walks it)

1. **The Approach.** He enters at the bottom edge (−3, −16) on a trodden path that curves up to the ring's entrance.
2. **The Tarn**, on the left, is the first fight: flat, walkable ice with a rocky far shore.
3. **The Ring** is the main arena: about 7 m of open snow inside ten standing stones.
4. **The Door.** The barrow mound closes the top of the area, with its carved lintel door at floor level, facing the camera.

## 3 · Placements

| Piece | Class | (u, v) m | Notes |
|---|---|---|---|
| Mound | structure | centre (0, 13) | Footprint 12 × 9 m, rise **about 4.0 m**, kerbed. **Non-walkable.** It runs past the window's top edge (v 17.72) |
| Door | lintel on 2 posts | on the centre line, **set into the mound's face** | The lintel faces −v. The mound's surface stands **≥ 0.3 m above the lintel's top** over the whole passage roof, so the door reads as a way INTO the mound, not a gate in front of it (as in the concept). A **stone-lined cutting**, ≥ 1.6 m wide with its floor at y = 0, runs from the mound's foot to the door. The walkable area ends at the door threshold; the 3 steps down beyond it are scenery for a later interior |
| Ring stones ×14 | stones | circle r = 9 about (0, 2), θ = ±35°, ±55°, ±75°, ±95°, ±115°, ±135°, ±155° (spacing ≈ 3.1 m) | ±155° stone_tall (the **gate stones**); ±135° stone_mid; ±115° stone_short; ±95° stone_tall, except **−95°, fallen and lying outward**; ±75° stone_mid; ±55° stone_tall; ±35° stone_short, at the mound's foot. Carved faces toward −v, turned up to 30° toward the ring's axis. Ten stones 5.6 m apart did not read as a ring |
| Raven | raven | on the +55° stone | |
| **Arena** | open | r ≤ 7 about (0, 1) | Nothing placed; drifts ≤ 0.2 m |
| **Path** | trodden | (0, −6.2) → (−1, −10) → (−3, −16), 4 m wide | Path ground; nothing placed on it |
| **Tarn** | ice | ellipse centre (**−13.5**, −5), 12 × 9 m | Flat and walkable; no snow. West and south-west rim is shore rock (non-walkable); the east side is open to step on |
| Outcrops ×8 | rock masses | (17, −12), (18, −3), (17, 6), (10, −15), (−19, −13), (−19, 4), (−13, 13), (13, 13) | Layered masses, 4–6 m footprint, 1.5–3 m tall; the boundary. Primitives until an outcrop model exists |
| Cover outcrop | rock mass | (**−12.5, 4.7**) | 3 × 2 m, 1.4 m tall: cover for the tarn fight. Moved so the gap to the fallen stone is about 2.1 m, not a 0.98 m squeeze |
| Birch groves | birch | G1 (7, −11) ×5 · G2 (−10, 9.5) ×4 · G3 (13, −6) ×4 · G4 (10, 12) ×3 | Groves, not rows. G2 and G4 close the gaps beside the mound |
| Fallen tree | kit log (stand-in) | (−7, −12) | Lies along the tarn's near shore, about 5 m (two logs end to end) |
| Grave markers ×2 | kit shield-on-spears | (−7, 11), (7, 11) | Beside the mound's flanks |
| Cairns ×3 | kit cairn | (2.5, −9), (−5, −14), (−16, 1) | Waymarkers on the path and the tarn's north shore |
| Juniper and heather | tinted ground zones | 2–3 m skirts round every outcrop; under the groves; the mound's base outside the ring; the tarn's far shore | **Never** in the arena, on the path, on the ice, or in the ring entrance |
| Play bounds | colliders | a polygon through the outcrops and thickets, with the entry gap at (−5…−1, −16) | The edge must read as land (rock, trees), not a wall |

Resolved while drafting v1: the third cairn moved out of the arena to the tarn's shore.

## 4 · The greybox as a paint-over guide

- **Hero pieces:** the real models (the welded ones in `t10_barrow/reduced_v2/`, and the kit) in **flat grey**, so the painter paints their true silhouettes.
- **Outcrops and the mound:** primitives.
- **Ground:** snow light warm grey, path a darker brown-grey band, ice pale blue-grey, shrub zones muted green-brown patches.
- **Light and ink:** the Barrow's 55° sun with soft shadows, and the one pen, so the painter can read the forms.
- **Scale:** the barbarian at the arena centre, painted.

## 5 · Deliverables (step 1), and what is measured

1. **`barrow_full_layout.json`:** every placement (u, v, world transform, class, size), the regions (arena, path, ice, shrub zones), and the bounds polygon.
2. **A top-down map:** labelled, with a 5 m grid and the 3 × 3 chunk grid overlaid.
3. **The greybox at the play camera:**
   - the full 4096 × 2560 guide;
   - two play-screen stills (the ring arena and the tarn) with him for scale.
4. **A playable greybox app** (him, armed, walking the layout): `C-9 Barrow blockout.app`.
5. **The guide staged as a `guided_paint.py` config. Not fired;** painting waits for Matt's look.

**Acceptance:**
- every placement within 0.05 m of this spec, or the deviation reported with its reason;
- a flood fill from the entry reaches the arena, the ice and the door, and nothing walkable leaves the bounds;
- the mound is non-walkable; the passage floor at the door is y = 0;
- the arena is clear to r 7, the path is clear at 4 m, and the ring entrance is ≥ 6 m;
- a 1 m marker in the guide measures 100.6 px across;
- **(v2) no squeezes:** every gap between obstacles in the walkable area is either < 0.70 m (his capsule cannot pass) or ≥ 1.4 m;
- **(v2) camera margin:** with the camera centred on him at every reachable cell, 0 px of the frame falls outside the window;
- **(v2) the door:** the mound's surface is ≥ 0.3 m above the lintel's top over the passage roof, and the door's face is visible at the play camera from the arena centre.

## 6 · v2 corrections (from the first blockout's own findings; the spec was wrong, not the build)

| v1 defect (measured by the blockout drax) | v2 |
|---|---|
| The door at (0, 7.5) stood 6.31 m from the arena centre, inside the r 7 the spec also asked for | Mound centre (0, 11) → (0, 13); the door is set into the mound's face |
| The lintel's top at 3.19 m stood above the mound's 2.59 m peak, so the passage could not be roofed and read as a free-standing gate | Rise 2.6 → about 4.0 m; the mound covers the lintel by ≥ 0.3 m |
| The mound stopped 1.44 m short of the window's top edge | 12 × 9 m footprint, running past the top edge |
| The ±40° stones stood 0.24 m from the mound's foot (the v1 1.2 m figure was measured along v only) | Replaced by the 14-stone ring |
| The −125° stone put 0.15 m² of its footprint on the ice | Tarn centre moved 0.5 m west |
| A 0.98 m squeeze between the fallen stone and the cover outcrop | Cover outcrop to (−12.5, 4.7); the "no squeezes" rule added |
| Up to 7 m of unpainted world in frame at the edges | 4 × 4 window with half-screen margins |
| Two arena centres (origin vs (0, 1)) | The arena is at (0, 1); the origin is only the origin |

*— gandalf, 2026-09-29. Anchors: R-C9-73, R-C9-74, R-C9-75; `2026-09-29-a-world-that-fits-the-barbarian-verdict.md` § 6–8.*
