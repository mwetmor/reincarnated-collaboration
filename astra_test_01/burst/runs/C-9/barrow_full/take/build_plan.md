# The Barrow, step 4: the build plan (T10-2)

> drax, 2026-09-30, for the conductor. Step 4 part A: the plan. Part B (the free prep) runs against it; its measured numbers are in § 8.
> Inputs: the accepted paint-over (sha256 `eecb42661af490dd…`), step 3's 54 plates (`take/plates/plates.json`), the tuft density (`take/masks/density_uv.png`) and the ground layout (`take/ground/`).

## 1 · The fact the plan rests on

The play camera is orthographic, with a fixed direction: pitch 52.95°, yaw 47°. It pans with him, but it never turns.

Under an orthographic camera, two things depend only on the view direction: which faces of a static piece face the camera, and what hides them.

**So the painted view is the complete in-game view of every static hero.** A surface the painting does not show is one the player never sees. The only exception is what the knight himself moves, like snow.

Two consequences:
- A plate can be worn by projection, with nothing left for the player to discover unpainted. The "unseen" texels a bake fills (§ 8) are texels no camera in the game ever shows.
- What the 3D geometry must get right is its **silhouette and depth**. That covers:
  - where the pen line falls;
  - the shape of its cast shadow;
  - where he is hidden when he walks behind it.
  Its hidden faces only need to exist.

## 2 · What wears each plate (54)

- **25 real models** already stand at their blockout transforms: the Tripo stones, the lintel, the posts and the raven, plus the kit's cairn, log and shield. Each plate is baked onto the model's own UVs, with the character's method, unchanged (§ 5).
- **29 primitives:** the mound, 18 outcrops and 10 shore rocks. They are flat-shaded stacked slabs with no UVs (§ 3).

| plate | class | geometry that wears it | tris | painted px |
|---|---|---|---:|---:|
| `mound` | mound | primitive: the procedural dome, kerb and passage (`_build_mound`) | — | 680231 |
| `door_lintel` | lintel | real model `models/barrow/lintel.glb` | 9998 | 16553 |
| `door_post_L` | post | real model `models/barrow/post.glb` | 9998 | 3662 |
| `door_post_R` | post | real model `models/barrow/post.glb` | 9998 | 4235 |
| `grave_marker_E` | shield | real model `models/barrow/kit/shield.glb` | 7998 | 6483 |
| `grave_marker_W` | shield | real model `models/barrow/kit/shield.glb` | 7998 | 6480 |
| `ring_m155` | stone_tall | real model `models/barrow/stone_tall.glb` | 9999 | 10466 |
| `ring_m55` | stone_tall | real model `models/barrow/stone_tall.glb` | 9999 | 10460 |
| `ring_m95` | stone_tall | real model `models/barrow/stone_tall.glb` | 9999 | 16970 |
| `ring_p155` | stone_tall | real model `models/barrow/stone_tall.glb` | 9999 | 9261 |
| `ring_p55` | stone_tall | real model `models/barrow/stone_tall.glb` | 9999 | 9210 |
| `ring_p95` | stone_tall | real model `models/barrow/stone_tall.glb` | 9999 | 9266 |
| `ring_m135` | stone_mid | real model `models/barrow/stone_mid.glb` | 9998 | 11731 |
| `ring_m75` | stone_mid | real model `models/barrow/stone_mid.glb` | 9998 | 11727 |
| `ring_p135` | stone_mid | real model `models/barrow/stone_mid.glb` | 9998 | 11015 |
| `ring_p75` | stone_mid | real model `models/barrow/stone_mid.glb` | 9998 | 11016 |
| `ring_m115` | stone_short | real model `models/barrow/stone_short.glb` | 9998 | 5813 |
| `ring_m35` | stone_short | real model `models/barrow/stone_short.glb` | 9998 | 5824 |
| `ring_p115` | stone_short | real model `models/barrow/stone_short.glb` | 9998 | 6340 |
| `ring_p35` | stone_short | real model `models/barrow/stone_short.glb` | 9998 | 6341 |
| `raven` | raven | real model `models/barrow/raven.glb` | 9998 | 143 |
| `fallen_tree_log_A` | log | real model `models/barrow/kit/log.glb` | 7998 | 6989 |
| `fallen_tree_log_B` | log | real model `models/barrow/kit/log.glb` | 7998 | 7049 |
| `cairn_1` | cairn | real model `models/barrow/kit/cairn.glb` | 7998 | 6732 |
| `cairn_2` | cairn | real model `models/barrow/kit/cairn.glb` | 7998 | 5996 |
| `cairn_3` | cairn | real model `models/barrow/kit/cairn.glb` | 7998 | 6732 |
| `cover_outcrop` | outcrop | primitive: 2 stacked slabs, flat-shaded, no UVs | 64 | 49161 |
| `margin_outcrop_1` | outcrop | primitive: 3 stacked slabs, flat-shaded, no UVs | 96 | 151288 |
| `margin_outcrop_2` | outcrop | primitive: 3 stacked slabs, flat-shaded, no UVs | 96 | 139656 |
| `margin_outcrop_3` | outcrop | primitive: 3 stacked slabs, flat-shaded, no UVs | 96 | 126243 |
| `margin_outcrop_4` | outcrop | primitive: 3 stacked slabs, flat-shaded, no UVs | 96 | 106901 |
| `margin_outcrop_5` | outcrop | primitive: 3 stacked slabs, flat-shaded, no UVs | 96 | 131895 |
| `margin_outcrop_6` | outcrop | primitive: 3 stacked slabs, flat-shaded, no UVs | 96 | 125214 |
| `margin_outcrop_7` | outcrop | primitive: 3 stacked slabs, flat-shaded, no UVs | 96 | 153496 |
| `margin_outcrop_8` | outcrop | primitive: 3 stacked slabs, flat-shaded, no UVs | 96 | 150606 |
| `margin_outcrop_9` | outcrop | primitive: 3 stacked slabs, flat-shaded, no UVs | 96 | 125115 |
| `outcrop_1` | outcrop | primitive: 3 stacked slabs, flat-shaded, no UVs | 96 | 138401 |
| `outcrop_2` | outcrop | primitive: 3 stacked slabs, flat-shaded, no UVs | 96 | 180225 |
| `outcrop_3` | outcrop | primitive: 3 stacked slabs, flat-shaded, no UVs | 96 | 138736 |
| `outcrop_4` | outcrop | primitive: 3 stacked slabs, flat-shaded, no UVs | 96 | 108640 |
| `outcrop_5` | outcrop | primitive: 3 stacked slabs, flat-shaded, no UVs | 96 | 125732 |
| `outcrop_6` | outcrop | primitive: 3 stacked slabs, flat-shaded, no UVs | 96 | 163108 |
| `outcrop_7` | outcrop | primitive: 3 stacked slabs, flat-shaded, no UVs | 96 | 157008 |
| `outcrop_8` | outcrop | primitive: 3 stacked slabs, flat-shaded, no UVs | 96 | 122721 |
| `shore_rock_1` | shore_rock | primitive: 2 stacked slabs, flat-shaded, no UVs | 56 | 8898 |
| `shore_rock_2` | shore_rock | primitive: 1 stacked slabs, flat-shaded, no UVs | 28 | 17188 |
| `shore_rock_3` | shore_rock | primitive: 2 stacked slabs, flat-shaded, no UVs | 56 | 7542 |
| `shore_rock_4` | shore_rock | primitive: 1 stacked slabs, flat-shaded, no UVs | 28 | 12649 |
| `shore_rock_5` | shore_rock | primitive: 2 stacked slabs, flat-shaded, no UVs | 56 | 11772 |
| `shore_rock_6` | shore_rock | primitive: 1 stacked slabs, flat-shaded, no UVs | 28 | 14940 |
| `shore_rock_7` | shore_rock | primitive: 2 stacked slabs, flat-shaded, no UVs | 56 | 10287 |
| `shore_rock_8` | shore_rock | primitive: 1 stacked slabs, flat-shaded, no UVs | 28 | 15353 |
| `shore_rock_9` | shore_rock | primitive: 2 stacked slabs, flat-shaded, no UVs | 56 | 16680 |
| `shore_rock_bridge` | shore_rock | primitive: 1 stacked slabs, flat-shaded, no UVs | 28 | 14207 |

## 3 · The 29 primitives: routes, costs, risks

**(i) Keep the silhouette, refine it procedurally, project the plate: free.**

How it works:
- **UV = the camera's projection.** Each vertex takes its painting pixel as its UV, so the plate *is* the texture, with no bake. Faces the camera never sees (backs, bottoms) take the plate's `fill_srgb_for_unseen`.
- **Refinement: a procedural subdivision and displacement of each slab's side walls, pushing the silhouette onto the painted rock's own outline.** That outline is the plate's rock-against-snow edge, found per plate exactly as step 3 found the tufts. The floor contact and the slab tops are kept.
- **The mound gets the same treatment.** The dome and passage stay as built, and the painted kerb-stone ring becomes a displaced band.

Risk against the overlay (step 5): **the lowest.**
- The geometry is the greybox the painter painted over. The ID silhouettes sit on the painted edges to within a few px, as the verification image shows.
- What is left:
  - (a) The painted outline is irregular where the greybox edge is straight. That is a pen line and coverage error of 1–4 px along each edge, which the refinement closes.
  - (b) The painter heaped snow against the rocks on *ground* pixels. That snow belongs to the 3D snow field, not to the rock, and it will read as a coverage difference until the snow is built.

**(ii) A paid image-to-3D build from each plate: about $0.40 each on fal (Tripo). 29 × $0.40 = $11.60.**

Risk: **the highest per piece.**
- A reconstruction from one painted view rebuilds the silhouette rather than keeping it. T6 measured 0.84–0.88 silhouette IoU for *multiview* builds, and one view is worse.
- Each result must be re-fitted to its footprint, height and pose. Wherever the new silhouette leaves the painted one, the projected plate puts rock on snow or snow on rock, and both count against coverage.
- It also brings 29 imports, fits and collider rebuilds.

**(iii) A few shared built variants across the 18 outcrops,** e.g. 4 outcrop builds and 2 shore-rock builds: 6 × $0.40 = $2.40.

Risk: **the worst for the overlay.**
- The 18 outcrops differ in footprint, height and number of steps (2–4 slabs), so they cannot share 4 silhouettes.
- Every instance would wear a plate painted on a different shape. Per-instance scaling narrows the gap, but a 3-step plate still will not fit a 2-step rock.

**Recommendation: route (i) for all 29 primitives. Total fal cost: $0.00.** Routes (ii) and (iii) spend money to make the silhouette *less* like the painting.

## 4 · The open design question: the painted light

The plates are the painting, so the painter's light and cast shadows are in them. That touches the verdict's rule 2 (albedo-only paint) and rule 3 (one real light).

There are two ways to wear them:
- **Unlit.** This reproduces the painting exactly. It keeps one light only if his cast shadow is applied as a shadow-only multiply.
- **Under the ramp.** This lights the plates twice: a painted shadow side darkens again.

§ 8's mini overlay measures both against the painting. **This is a design call for gandalf and Matt, not a build detail.** Either way, the geometry and the bakes in this plan are the same.

## 5 · The 25 real models

Each plate is baked onto the model's own UVs by `nb_t8/scripts/t5_06b_bake.py`, byte-identical and copied to `tools/`:
- one sheet (the painting), one cell (the plate's camera), and the plate's alpha as the matte;
- weight = density × facing⁴, averaged in linear light;
- unseen texels filled inside their UV island.

The surface file the bake reads comes from `tools/hero_surface.py`. It builds the same arrays as `t5_06a_surface.py`, but in the Godot world frame, and from the meshes exactly as the blockout places them (`godot/tools/export_hero_meshes.gd`). Blender's glTF import would change the axis convention, so it is not used.

Each instance gets its own texture: six `stone_tall` placements means six bakes of one mesh.

## 6 · Heather and the ground

- **Heather:** a MultiMesh instance list sampled from `density_uv.png`, so the 3D heather stands where the painting put heather (§ 8, B2). It is placed *from* the painted tufts and never on top of them, so the level does not show heather twice.
- **Ground:** `splat_world.png` becomes the ground shader's splat, in the blockout's own `barrow_full_splat.bin` encoding (§ 8, B2). The design splat is kept outside the painted window and under the heroes.

## 7 · What step 5 will measure, and what waits

Step 5 measures per-class coverage per chunk against the painting's own classes. It uses step 3's classifiers:
- rock, stone and wood (the heroes, via the ID render);
- heather and shrub;
- trees;
- ice, path and snow.

**On hold until the conductor's word:** any paid build, assembling the full step-4 scene, any change in `cliffside3d`, and any app or web build.

## 8 · Measured (step 4 part B)

### B1 · The 25 real models, baked (`tools/bake_heroes.py`, report `take/build/bake_report.json`)

The bake ran as `tools/t5_06b_bake.py`, byte-identical to `nb_t8/scripts/t5_06b_bake.py` (checked by sha256 at every run), with 1024 px textures. **All 25 baked.**

The bake's own self-test holds for every piece: 99.89–100% of the vertices that project into the cell land on the silhouette. So the stored camera reproduces the ID render.

| piece | unseen before fill | **unseen after fill** | painted from an occluder |
|---|---:|---:|---:|
| `cairn_1` | 65.1% | **35.8%** | 0.00% |
| `cairn_2` | 69.0% | **36.6%** | 0.00% |
| `cairn_3` | 65.2% | **35.9%** | 0.00% |
| `door_lintel` | 73.1% | **43.1%** | 2.14% |
| `door_post_L` | 70.7% | **41.5%** | 3.77% |
| `door_post_R` | 68.0% | **34.5%** | 1.98% |
| `fallen_tree_log_A` | 65.7% | **34.5%** | 0.00% |
| `fallen_tree_log_B` | 68.9% | **40.8%** | 0.00% |
| `grave_marker_E` | 59.6% | **28.6%** | 0.00% |
| `grave_marker_W` | 59.5% | **28.6%** | 0.00% |
| `raven` | 78.5% | **59.8%** | 0.00% |
| `ring_m115` | 60.8% | **36.5%** | 0.00% |
| `ring_m135` | 69.9% | **38.2%** | 0.00% |
| `ring_m155` | 63.2% | **32.0%** | 0.00% |
| `ring_m35` | 60.9% | **36.7%** | 0.00% |
| `ring_m55` | 63.3% | **32.2%** | 0.00% |
| `ring_m75` | 70.0% | **37.6%** | 0.00% |
| `ring_m95` | 63.2% | **37.7%** | 0.00% |
| `ring_p115` | 61.6% | **40.0%** | 0.00% |
| `ring_p135` | 65.2% | **28.4%** | 0.00% |
| `ring_p155` | 66.0% | **36.4%** | 0.00% |
| `ring_p35` | 61.8% | **41.0%** | 0.00% |
| `ring_p55` | 66.0% | **36.5%** | 0.16% |
| `ring_p75` | 65.3% | **28.4%** | 0.00% |
| `ring_p95` | 66.0% | **35.5%** | 0.00% |

**Unseen after fill: median 36.5%, maximum 59.8% (the raven).** The character bake's figure was 0.44%, but it had a ring of cameras; the heroes have one.

What is left bare is each piece's back and underside: whole UV islands that no camera paints. Per § 1, it is also never on screen.

"Painted from an occluder" counts texels behind another piece: the lintel's ends in the mound, the posts behind the lintel, and ring_p55 under its raven. They took the occluder's paint, and they are never on screen either.

Three fixes were needed for the surface file, all in `hero_surface.py`; the bake itself was never touched:
- **Godot winds its front faces clockwise.** The face normals are therefore oriented by the vertex normals. The first run took the back faces as the seen ones and left 98% of the texels unpainted.
- **The UV v axis is flipped** to the convention the bake's final flip expects.
- **The matte adds, at alpha 96, the piece's own geometry where another piece hides it.** The lintel had failed the self-test at 84% against the visible silhouette alone, although its camera was exact.

### B2 · Data files, wired into nothing (`tools/heather_instances.py`, report `take/build/data_report.json`)

- **Heather MultiMesh instances** (`take/build/heather_instances.json`). 954 heather sprays (0.30 m) and 23 shrub clumps (0.45 m) are placed FROM `density_uv.png`. Their screen footprint is 150.7 and 7.4 m², against the painting's 166.2 and 10.0 m² of cover. Each row is `[u, v, x, z, diameter_m, yaw_deg]`; heather sprays face the camera, so they take no yaw.
  - **The density raster was re-made on the way.** Step 3 set every tuft pixel down on its merged patch's lowest row, so the first sample missed the clumps. Each pixel now sits on the ground under it at a tuft's half-height (0.15 m).
  - **Cover is counted as screen area.** An instance is counted by its screen footprint, not its ground disc; counting discs put 2.2× the painted heather down.
- **The ground material's input** (`take/build/barrow_full_splat_painted.bin`, sha256 `706cc6447a91514d`). It uses the exact encoding and frame of `godot/data/barrow_full_splat.bin` and is **not swapped in**. To wire it, replace that file and set the layout's `regions.splat.sha256`. Painted splat shares: snow 63.9%, path 2.1%, shrub 32.3%, ice 1.7%. The design splat was 55.7 / 1.7 / 40.9 / 1.7.

### B3 · The mini overlay (`godot/tools/mini_overlay.gd` + `tools/mini_overlay.py`, `take/build/mini_overlay.png` / `.json`)

Four baked heroes were rendered at the guide camera and set against the painting at the same pixels, inside each piece's silhouette eroded by 2 px. The values are mean |difference| per channel, 0–255.

| piece | unlit (the bake alone) | lit (the bake as the ramp's albedo, under the sun) | lit, signed R/G/B |
|---|---:|---:|---|
| `door_lintel` | 12.6 | 40.9 | -58/-42/-21 |
| `fallen_tree_log_A` | 15.0 | 32.1 | -35/-31/-23 |
| `grave_marker_W` | 15.2 | 43.6 | -62/-43/-22 |
| `ring_p155` | 19.1 | 46.3 | -57/-48/-32 |

**Unlit: 15.5. Lit: 40.7.**

- **Unlit, the projection holds.** What is left is the bake's resampling blur and the blockout's own pen drawing over the texture (the stone's facet creases).
- **Lit, the painted light is lit a second time.** Every piece comes out 20–62 levels darker per channel, and bluer. That is § 4's question, measured: wear the plates unlit (with his shadow as a shadow-only multiply), or de-light them before they are worn.

### Scratch that can go (not deleted, per the rules)

`work/` holds 972 MB of regenerable intermediates:
- `surf_*.npz` (25 × 28 MB);
- `bakes/*_raw.npy` and `*_wsum.npy`;
- `meshes/*.f32` / `*.i32`;
- `overlay/*.png`.

Keep the textures `work/bakes/<id>.png` if the bakes are wanted without a re-run (about 35 MB). Everything else is rebuilt by:
`export_hero_meshes.gd` → `bake_heroes.py` → `mini_overlay.gd` / `mini_overlay.py`.
