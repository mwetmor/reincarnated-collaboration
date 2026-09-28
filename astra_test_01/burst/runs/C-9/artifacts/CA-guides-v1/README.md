# CA-guides-v1 — the CATHEDRAL ARENA GREY BOX and its painting guides

**Author** drax (presentation seam) · **Run** C-9 · **2026-09-27**
**Authority** R-C9-43 / R-C9-44 (Corrigendum-Forward 3, indoors) · R-C9-45 (Corrigendum-Forward 4, the arena sitting) · crack-law doc Corrigenda 2 § 2 and 4 · `rdr-art-illuminated-archive-brief.md` § 3 / § 4.
**Gate** Matt / gandalf approve this grey box BEFORE any cathedral paint. Nothing was painted and no image was generated: this is geometry and renders of geometry.

**Grey box project** `astra_test_01/burst/runs/C-9/cathedral_greybox/` — Godot 4.6.3, Forward+/Metal, SubViewport readback, rendered in 6 tiles of 4096². `cathedral_greybox.tscn` is the baked scene; `tools/spec.py` → `tools/geom.py` → `build.gd` → `tools/post.py` is the whole chain, and every number in it is stamped MEASURED / DERIVED / RULED / DECLARED in `cathedral_spec.json`.

---

## 1 · Camera and scale

| | |
|---|---|
| Projection | orthographic, the cliffside plate law |
| **ppm (plate)** | **100.617553710938 px/m** — MEASURED, `blockout_meta_v2.json :: ortho_canvas_v2.px_per_m_screen_x` (R-C3-44) |
| Pitch α | **52.9535411256029°** — MEASURED |
| px/m along the view axis | 80.307624764688 = ppm·sin α |
| px/m of elevation | 60.618293603727 = ppm·cos α |
| **Yaw** | **45.0°, camera in the SOUTH-EAST looking NORTH-WEST** (R-C9-45 cl.1) |
| Screen right | NE · Screen up | NW and elevation |
| Free cross-check | ppm·sin α and ppm·cos α reproduce the cliffside's own independently authored px/m pair to **0.0** and **8.5e-14 px** |

**Yaw is a compass word, not a number, in the ruling.** SE is exactly 45°, and 45° is the only yaw at which the two rising walls present equally and the two cut-low walls recede equally — the symmetric condition the ruling describes. The GD runtime's own `yaw 47°` is a yaw in referent axes, which carry no compass; it is not inherited.

**Figure height — the conflict is carried, not resolved** (as the greyroom manifest already carried it): the cliffside convention is **a person 130 px**, which at this ppm implies a **2.1446 m** body; KC2-PLAY's ruled `h_fig` is **1.9 m**, which is **115.175 px**. This grey box adopts the PLATE SCALE (which is what "130 px" pins) and states both.

**Runtime camera** (MEASURED, `cliffside_B/parallax/parallax.json`): a **2D camera 1:1 on the plate**, view 1920×1080, player anchored at **(962, 595)**, walk 247 px/s = 2.4548 m/s.

## 2 · The room

Room size comes from encounter math, not from pictures (brief § 3). Both measured quantities are **reused unchanged** from `crucible-arena-geometry-v1.json` (sha `68d895d757…`):

| | |
|---|---|
| Extent | **57.285 m E–W × 76.665 m N–S** (MEASURED) |
| Walkable area | **2354.3412243939315 m²** (MEASURED) |
| Plan | cruciform; origin = the **crossing centre**; nave S→N; nave : chancel = 2 : 1 |
| bbox | x ∈ [−28.6425, +28.6425], y ∈ [−51.110, +25.555] |
| **Limb width** | **21.767787 m** — **DERIVED, not chosen** |
| Gross cruciform | 2441.9585 m² − crater 63.6173 − crypt mouth 24.0000 = **2354.3412 m²**, residual **0.000e+00** |
| Raster check | 2353.920 m² at a 0.20 m cell (|Δ| 0.4212 m² = pure quantisation) |

The limb width **solves** `extent_NS·w + extent_EW·w − w² − crater − crypt = the measured walkable area`. Piers do not subtract: their inner face sits exactly on the limb edge (the lineage's own architecture — the dado's *"inner edge = the measured ring and is load-bearing"*), so they stand outside the walkable and ship as **prop footprints** (Crack-law Corr. 2 § 2), 21 of them in `registration.json :: props`.

**⚑ CONFLICT — the measured central-vessel width does not survive.** The lineage's `central_vessel_width_m = 13.128922 m`; the cruciform needs **21.767787 m**. That figure is `derived_from_geometry`, i.e. read off the referent blob's own shape — a picture-derived number, which brief § 3 explicitly subordinates to encounter math. The two MEASURED invariants (extent, walkable area) are both held exactly; the shape-derived one cannot be. Named here, not resized silently.

**Elevation.** Ground arcade 0–12 m · triforium 12–17 m · clerestory 17–26 m · vault springing 26 m. Near side cut at **0.90 m** (the lineage's D2 knee break). Dais +1.2 m, y ∈ [14, 21]; apse y ∈ [21, 25.555]; empty cross mount 3.6 × 6.0 m on the apse wall at 14–20 m.

**The rise rule is DERIVED, and no list of faces exists in the generator.** An element rises iff raising it hides no more walkable floor than cutting it to the knee would (tolerance 0.5 m²) — which is the reason *both* corrigenda give for cutting a side low. Rising: **R2 chancel-west, R3 west-transept-north, R5 west-transept-end, R6 apse**. Cut low: south façade, both transept south walls, the nave/chancel east arcade, the east transept end wall. Measured costs are in `measurements_v1.json :: rise_test`.

Two elements were moved off the rising list **by measurement, and both are recorded, not silent**:

- **R4, the east transept arm's north wall → CUT LOW.** By compass it is a north face, but it is the **east arm's** wall and R-C9-45 cl.1 cuts EAST low. Raising it hides **106.760 m² of chancel floor** *and hides the EMPTY CROSS MOUNT* — the scene's declared landmark (R-C9-45 cl.2 / F-S3) — behind its own face. Verified: with it raised, `cross_mount_empty` rendered **zero pixels**.
- **All four crossing piers → CUT LOW (DECLARED, overrulable).** Three fail the rise test outright (53.6–69.6 m² each). The fourth passes only because the test measures hidden *floor*, and what that one hides is the **apse wall and the cross mount on it**. One rising crossing pier out of four is an artifact of the camera azimuth, not architecture, so the set is cut as a set.

## 3 · The clamp, and the crown clearance

**Clamp** (plate px, the rect the 1920×1080 window can occupy): **[0.47, 1199.46, 9106.36, 8026.21]** on a **9108 × 8028** plate. Its form is identical to the cliffside runtime's own `camera.limits`: camera centre = player plate px − (anchor − view/2).

**⚑ The declared 34 m wall FAILED, and the pixel test is what caught it.** "30+ m, true scale" was a DECLARED guess. Solving Corrigendum 3 cl. 1's own clause —

```
h  >  [ px_per_m_along_view · (s_player − s_crown) + anchor_y ] / px_per_m_elevation  +  z_player
```

maximised over every (crown, player) pair that can share a 1920×1080 frame — gives **55.585 m required**. Built at **57.0 m**.

*(The first solve returned 54.94 m and the pixel test still found 269 crown blocks in frame. The solver had sampled each wall footprint's two **diagonals**; the binding crown sits on the footprint's **inner edge**, which no diagonal passes through. A crown is a rectangle, so the rectangle is now sampled. Same shape as the other instrument failures on this run: it ran cleanly and answered a different question.)*

**Crown clearance, MEASURED on pixels, not argued:**

| | |
|---|---|
| Crown pixels on the plate | 293 527 (4 916 blocks of 8 px) |
| **Crown blocks inside ANY reachable frame** | **0 — PASS** |
| Highest building point that ever lands in a frame | **56.003 m** |
| Crown | 57.000 m → **clearance 0.997 m** |
| Analytic bound | anchor 595 px ÷ 60.6183 px/elevation-m = **9.8155 m** of wall above the player's own plan position, and less as the wall recedes |

**Void (un-architected background) inside the union of reachable frames: 0.000 %.** The plate is full-bleed everywhere the camera can go.

**Walkable occlusion: 9.304 %.** Plan 2353.920 m² → 2134.900 m² on screen. Per class in `measurements_v1.json`. The residue is the cut-low walls' own 0.68 m shadow (inherent to a knee-height break at this pitch) plus the re-entrant corners.

## 4 · ⚑ WHAT I COULD NOT SATISFY

**(a) The three-storey elevation is never on screen at plate scale. This is the headline.**

A 1080-tall frame with the anchor at row 595 shows **9.8155 m of elevation** above the player's own plan position — and less as the wall recedes. The triforium starts at **12 m**. **So the triforium, the clerestory, the open bays, the west-top breach and every window hole are outside the frame at every camera position the clamp allows.** Corrigendum 3 § 1 ("the walls rise out of the frame") and Corrigendum 3 § 5 ("windows on the upper floors show the outside world") cannot both hold at ppm 100.6176.

Worse, and measured: **the two nave walls cannot both be on screen.** A 1080-tall frame covers **13.448 m** of ground along the view axis; the nave's two walls are **15.392 m** apart along it. `framing_mid_nave_crossing_plate.png` is the proof — at mid-nave the runtime frame contains **floor and the crater and nothing else** (highest building point in frame: **0.01 m**).

The zoom that would fix each thing, with the person height it implies:

| to bring into frame | ppm | person |
|---|---|---|
| both nave walls | 87.911 | 114 px |
| triforium sill (12 m) | 82.301 | 106 px |
| **clerestory sill (17 m)** | **58.095** | **75 px** |
| clerestory head (26 m) | 37.985 | 49 px |

**I built and guided the full elevation anyway**, so that a zoom ruling costs nothing: the plate carries the arcade, triforium and clerestory up to 28 m, the window-hole mask is populated, and every chunk is flagged `in_camera_clamp`. **67 of 73 chunks are inside the clamp; 6 are not** and carry only upper-storey masonry — paint those only if the zoom ruling changes. Each framing ships twice: `…_plate.png` (1:1, what the runtime does today) and `…_fit.png` (ppm 58.095, where the room reads). **This is a ruling for Matt/gandalf; I have not taken it.**

**(b) A rising west wall hides part of the west transept arm, and no configuration avoids it.** R1 (the nave's west arcade) at full height hides **156.640 m²** of the west arm — a re-entrant-corner effect that neither corrigendum contemplates. R-C9-45 cl. 1 rules the WEST wall rising; the functional test would demote it, which would leave the crossing open to the west and destroy the indoor reading. **I built it rising (the ruling) and report the cost.** `tools/geom.py --functional` builds the other branch; its rise table is in `registration.json`.

**(c) 57 m walls are not "true scale."** Corrigendum 3 cl. 1 asks for walls "built tall enough that no crown is visible" *and* the brief says "true scale, 30+ m nave". Beauvais, the tallest vault ever raised, is 48 m. The solve needs **55.585 m**. Everything above ~28 m is invisible to every camera position, so it costs nothing in paint — the plate is cropped at 28 m elevation and the wall simply runs off the top, which is Corrigendum 3's own stated mechanism ("painted to the plate's top edge"). But the *number* is not a true-scale nave and should not be reported as one.

**(d) The north chancel breach's broken stair was invisible where the ruling put it.** Outside the apse wall it sits behind 57 m of masonry and rendered **zero pixels**. It is now built on the **playable side**, descending from the breach into the chancel with the middle two flights missing — which is what "broken stairs the monsters leap and the player cannot cross" means, and the only placement in which it can be seen at all.

**(e) Pool radii are an upper bound scaled by a drax call, not a measurement.** See § 6. Two verdicts flip at the raw upper bound.

## 5 · Entrances, aprons, spawns

All one-way (Corr. 4 cl. 3): broken ground the monsters leap and the player cannot cross. Beyond the apron the terrain is impassable, so no tick is authored there.

| id | kind | position (m) | apron |
|---|---|---|---|
| **E-CRYPT** | hole in the floor by the cut-low **east** wall, 6.0 × 4.0 m | (24.0, 0.0) | blue fire |
| **E-SE-FIRE** | the near ambush, a breach in the **south façade**, 4.0 m | **(6.875, −51.110)** | real fire |
| **E-N-CHANCEL** | ground-level breach beside the **apse**, 4.0 m, with a broken stair | (−7.0, 25.555) | blue fire |
| **SG-… ×5** | dark triforium galleries on the rising walls — **descend-from-above** | listed in `registration.json :: spawn_galleries` | blue fire landing apron (DECLARED) |

**E-SE-FIRE is DERIVED from measurement, not placed by eye.** The player spawn is DECLARED 2.0 m inside the south door on the nave axis, at (0, −49.110). The decoded near-ambush distance is **‖p05‖ = 7.16 m** (KP-66 Class 3 / Corr. 4 cl. 2, *"the 7 m ambush at t = 4 s"*). Solving for a position on the façade reproduces it **exactly**: distance from spawn = **7.160000 m**.

**Apron depth 3.0 m — DERIVED**, not picked: at the measured walk rate (247 px/s ÷ ppm = 2.4548 m/s) a 3.0 m apron is crossed in **1.222 s**, about one D-LIFT-1/2 tick, against a ~6 s death. Crossable, not campable. Apron = `dilate(mouth, 3.0 m) ∩ walkable`, so it wraps only the playable side. Blue-fire apron 309.28 m², fire apron 32.72 m², both marked in the id mask.

Triforium bays alternate **open to the outside** (even bay) / **dark gallery** (odd bay); the dark ones are the descend-from-above spawns and each is listed with its centre, band and width. The **clerestory is entirely open, tracery kept** (mullions are their own id class). The **west wall's top is breached** over bays 1–3 of R1 (R-C9-44): triforium, clerestory and the wall above them are gone there and read as pure `#00ff00`; the lower arcade is intact.

## 6 · Pool registration

**The transform is DERIVED, not chosen.** (a) The re-ruling (Crack-law Corr. 2 § 2) puts the **apse north and the entry south**, so the measured frame is yawed. (b) The bbox 57.285 × 76.665 is **not square**, so ±90° cannot map bbox onto bbox. (c) 0° keeps the apse in the south and is refuted by (a). **180° is forced.** With both frames carrying the same measured extent, the translation is fixed by corner coincidence:

```
X_arena = −x_measured + 0.712500      Y_arena = y_measured − 22.325000
```

bbox-corner residual **3.553e-15 m**.

**Overlap, never proximity** (Corr. 2 § 2 — the instrument that teleported a pool 14 m onto a brazier used centroid distance). Every disc is rasterised at 0.20 m and intersected with (i) the walkable floor and (ii) the entrance mouths and their aprons.

| pool | arena (m) | r_disjoint | ∩ walkable | ∩ ruled entrance | **verdict** |
|---|---|---|---|---|---|
| Z-614 | (19.237, −26.600) | 6.276 | 0.000 | 0.000 | **DROP — off floor** |
| Z-618 | (19.807, 13.870) | 6.703 | 32.040 | 0.000 | **KEEP** |
| Z-620 | (2.707, 20.995) | 7.282 | 144.320 | 6.000 | **DROP — coincides with E-N-CHANCEL** |
| Z-622 | (−13.252, 5.890) | 3.549 | 39.840 | 0.000 | **KEEP** |
| Z-623 | (−18.383, 16.150) | 7.922 | 23.080 | 0.000 | **KEEP** |
| Z-626 | (−20.378, −24.320) | 5.515 | 0.000 | 0.000 | **DROP — off floor** |

**Three survive** as candidate burning-pitch spills on the nave/transept floor — which is R-C9-45 cl. 3's *"the aprons plus a FEW pools"*. They are painted into the walkable mask as `pool_candidate` (73.415 m² on screen) and stay walkable.

**⚑ Two things the instrument does NOT settle, and they are stated rather than buried:**

1. **My first cut dropped all six**, because I had counted the landing aprons I invented under the six dark triforium galleries as "entrances". Which bays are dark is **my** alternating rule, and those aprons blanket the foot of both rising walls — so letting them decide the pool question is an instrument answering a question it does not address. **The verdict of record counts only the three RULED entrance mouths and their aprons.** Counted with my declared gallery aprons, Z-618 (70.800 m²), Z-622 (1.320 m²) and Z-623 (84.480 m²) would all drop instead — i.e. **every surviving pool's verdict depends on a construct of mine**. Both columns are in `registration.json`.
2. **The radii are an upper bound × k_disjoint = 0.5345**, which is drax's call (greyroom manifest), not a measurement; only the **interior points** are measured. Recomputed at the raw upper bound, **Z-614, Z-618 and Z-626 all flip** (`verdict_flips_at_upper_bound: true`). Nothing here asserts that the six measured green zones and the six decoded spawn points are the same six objects — Corr. 4 § 6 says that is UNTESTED and this build does not test it.

**Divergence rows owed** (nothing dropped silently): `DIV-pool-Z614-off-floor`, `DIV-pool-Z626-off-floor`, `DIV-pool-Z620-coincides-E-N-CHANCEL`, `DIV-central-vessel-width` (13.129 → 21.768 m), `DIV-R4-cut-low`, `DIV-crossing-piers-cut-low`, `DIV-wall-rise-57m`, `DIV-upper-storeys-out-of-frame`.

## 7 · Outputs

| file | what |
|---|---|
| `ortho_canvas_v1_guide.png` | 9108 × 8028 shaded ortho plate. Every opening to the OUTSIDE and every un-architected background pixel is **flat pure `#00ff00`** → alpha → the Parallax2D stack shows through |
| `ortho_canvas_v1_id.png` | flat index colours, 23 classes, NEAREST only. Readback measured **byte-exact** (max distance from a legend colour = **0**) |
| `ortho_canvas_v1_walkable.png` | white = walkable. The crater is a hazard and **not** walkable; aprons and pools **are** |
| `ortho_canvas_v1_window_holes.png` | the separate window-hole mask: id class `opening_to_outside` only. `void_outside_frame` (0,200,0) is background and is **not** a window |
| `ortho_canvas_v1_depth_mm.png` | uint16. **`elevation_m = value/1000 − 8.000`**; floor plane reads **8000**, crown 65000, `not_foreground` 65535. Verified against known geometry: floor median **7999**, wall max **64999** (1 mm of 8-bit quantisation) |
| `chunks/` + `chunks_v1.json` | **1536 × 1024 chunks, 256 px overlaps**, grid 11 × 7, **73 kept / 4 dropped**, paint order row-major with `paint_after` on left+above neighbours. Each chunk ships guide / id / mask / depth / **window**. Each carries `in_camera_clamp` — **67 true, 6 false** |
| `legend_v1.json` | id colours, guide greys, walkable flag, window-hole rule |
| `overview_flat_v1.png` | 2600 × 2291 flat-shaded overview, labelled, with compass and scale bar |
| `framing_{south_entry,mid_nave_crossing,near_dais}_{plate,fit}.png` | in-game framing at 1:1 (what the runtime shows today) and at ppm 58.095 (where the room reads) |
| `measurements_v1.json` | every measurement above, plus per-file sha256 |

**Depth-format divergence, declared:** the cliffside's *"mm below local rim"* has no referent indoors, and the arena-guide lineage already declared *"mm of elevation"*. That convention cannot encode the crypt, which goes **6 m below the floor plane**, so the datum drops 8 m and the floor plane reads 8000.

**Bare.** No dressing, no pews, no bodies, no props, no floor damage — floor damage is the painter's, per the crack law as a principle in the prompt (Crack-law Corr. 3).

## 8 · Defects this build found in its own instruments

Four, all of the same shape — *an instrument that ran cleanly and answered a different question* — and all caught by measuring rather than reading the exit code:

1. **The depth shader.** `ALBEDO` written from a shader is treated as linear and sRGB-encoded on output, so a raw byte/255 does not survive the round trip: the floor's 42 came back as **113**, and the floor decoded to **13.34 m** instead of 0. `StandardMaterial3D.albedo_color` is unaffected because Godot already decodes it — which is exactly why the id pass round-tripped byte-exact *and hid the problem*. Fixed by emitting the sRGB-decoded value.
2. **The crown instrument.** The first version compared "topmost masonry row on the plate" with "highest reachable frame top". The plate is cropped to the walls, so the first number is 0 by construction and the comparison is meaningless. Replaced by a sliding-window maximum over every camera position the clamp allows.
3. **The crown solver's sampling** (§ 3) — diagonals, not the rectangle.
4. **The rise test's probe** — a centre ray, which misses everything an element's *width* hides. Replaced by a footprint sweep; that is what surfaced R4.

Plus two geometry defects the renders caught and the numbers would not have: the rooms-beyond ceiling occluding the nave (the rise rule applies to ceilings too, not just walls), and the raised dais built as a floating slab with the background showing through under its south face as a green stripe across the chancel.
