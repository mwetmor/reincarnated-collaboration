# CA-guides-v3 — the CANONICAL cathedral arena guide set

**Author** drax · **Run** C-9 · **2026-09-28** · **Authority R-C9-55** (Matt, the middle option), on R-C9-53 / Corrigenda 3–5 / R-C9-43/44/45 and the crack-law corrigenda.
**This is the set the establishing painting — bake-off round 3, Astra vs Sol — is painted over.** It supersedes CA-guides-v2 and the v2{a,b,c,d,z} treatment set. Nothing painted, no image generated.

> **Matt, verbatim:** *"Make the ruined pillars look as if they've crumbled due to the fighting and blasts of magic and fire. The broken pieces should be visible nearby somewhere but not covering the floor."*

**Chain** `tools/spec.py → tools/geom_v3.py <break_fraction> → build.gd → tools/post_v3.py`. Godot 4.6.3 Forward+/Metal, 6 tiles of 4096², seven passes: `guide · id · height · fade · id_fade · vault · arch`.

---

## 1 · The numbers of record

| | | target |
|---|---|---|
| **Floor hidden within 12 m, fade at 6 m, opacity-weighted** | **21.33 %** | ~20 % ✓ |
| of which fully opaque | 18.24 % | |
| with no fade at all | 25.30 % | |
| **Vault floor coverage** (thin transverse ribs) | **6.20 %** | thin ✓ |
| **Pier-in-frame** (the indoor read) | **99.82 %** | kept ✓ |
| **Walkable residual** | **−4.547e-13 m²** | exact ✓ |
| Crown test (plate walls in any reachable frame) | **0 blocks — PASS** | |
| Debris pixels overlapping a walkable pixel | **0** (asserted, plan **and** pixel) | 0 ✓ |

For the ladder: the v2 baseline was **51.51 %**, the all-ruined variant b **16.74 %**, the all-ghost variant d **29.12 %**. v3 sits where it was asked to.

Room unchanged: limb **23.573478 m** = 4.500 aisle + 2.00 pier + 10.573478 vessel + 2.00 + 4.500, **40 piers**, walkable **2354.341224 m²** against the measured target, plate **9236 × 8124**, chunks **11 × 8, 79 kept / 9 dropped, 73 inside the clamp**.

## 2 · The ruin

**Break fraction 0.35 — 13 of 36 rising piers broken.** Chosen by running the metric at 0.35 and 0.50: 0.50 gives 16.69 % hidden but leaves only **1.76 %** vault coverage (26 of 55 bays), which is the failure mode variant b had. 0.35 lands on the 20 % target *and* keeps the ceiling.

- **Which piers break is MEASURED, not chosen.** Every pier carries `hides_walkable_at_full_height_m2` — the walkable area it hides from the camera at full height. They are ranked and broken **from the top down**, so the ones that fall are exactly the ones whose loss buys the most visibility (R-C9-55 cl. 1).
- **Heights vary 2–7 m and never repeat**: a golden-ratio low-discrepancy sequence, then a pass that pushes any two neighbouring piers at least 0.8 m apart, so no run of the arcade repeats a height.
- **Survivors use the graded ghost (variant d)**: solid to 4 m, then **0.60 / 0.30 / 0.12** opacity by height. The base is what the player must read as an obstacle; the upper shaft is what hides distant floor and also what carries the indoor read. Each band is its own id class (`nave_pier`, `pier_ghost_1..3`) with the opacity in `legend.json`, so the runtime retunes without a rebuild.
- **Vault: only the bays that lost TWO supports fall.** A bay standing on four piers does not come down when it loses one. **18 of 55 fell; 37 stand** — most of the vault, as asked. Still ribs and springers only, 0.45 m section, no filled cells.

## 3 · Broken tops — the silhouette is in the geometry

The break is **jagged and blasted, never a clean cut**, and it is modelled, so the painter has a silhouette to follow rather than a rule to interpret: the 2 m section is diced into a 4 × 4 grid of 0.5 m cells, each ending at its own height within the top 1.0 m, biased **lower on the crossing-facing side** — the blast came from the demon gate at the crossing, so that is the face it took.

**The blasted crown is its own id class: `pier_break` (id `#FF5A28`), 459 717 px in the fade layer.** Scorch, soot and shatter are **PAINT**, not geometry; this class is where the brief calls for them. The brief line to carry: *fire-blackened and shattered at the break, clean stone below it, and the break edge pale and fresh inside* (crack law § 3 rule 7 — recency).

## 4 · Debris

**39 pieces** — drums (1.10 m), capitals (1.40 m), vault stones (0.80 m) — **3 per broken pier**, each within **9 m of its own pier**, each a **PROP** in `registration_v3.json :: props` with `footprint_m`, `height_m`, `sort_line_y_m` and `from_pier_m`, and its own id class **`debris`** (`#BE7832`).

**"Not covering the floor" is enforced, not eyeballed.** A piece is accepted only if **every** cell under its whole footprint is non-walkable dead space — the pier plinth footprints, the margins under the arcade arches, the crater rim, and against the cut-low walls. Asserted twice and both pass:

- **in plan**, before anything renders: walkable cells under a debris footprint = **0** (hard `assert`);
- **on pixels**, after the render: debris pixels overlapping a walkable pixel = **0** (hard `assert`).

Debris also *hides* very little: **9.68 m²**, 0.41 % of the walkable floor.

⚑ **DIVERGENCE `DIV-debris-no-talus`.** This **overrides crack-law rule 4's talus cone**. A cone at the angle of repose spills onto the floor by construction — that is what a real rubble pile does — and readability wins. Recorded, not silent. The painter still gets the *direction*: every piece carries `from_pier_m`, so the pile reads as having come off that pier.

## 5 · Outputs

| file | what |
|---|---|
| `ortho_canvas_v2guide.png` · `ortho_canvas_id.png` · `ortho_canvas_walkable.png` · `ortho_canvas_window_holes.png` · `ortho_canvas_depth_mm.png` | the plate, 9236 × 8124. Openings to the outside and un-architected background are flat pure `#00ff00`. Depth: `elevation_m = value/1000 − 8.000` |
| `fade_layerguide.png` / `fade_layermask.png` | RGBA — the pier shafts (banded by opacity), the blasted crowns, and the 3 occluding west-wall bays. **Absent from the plate by design**: a fading prop must have floor painted behind it |
| `overhead_vaultguide.png` / `overhead_vaultmask.png` | RGBA — the ceiling layer, scroll > 1, edge-anchored (T3p) |
| `floor_light.png` | greyscale — **the mask for the T3q runtime additive light layer** (R-C9-53 follow-up: the plate floor is painted soft and even; drama is the engine's). Shafts at the declared artistic **46.07°** |
| `chunks/` + `chunks.json` | 1536 × 1024, 256 px overlap, seven files per chunk: guide · id · mask · depth · window · light · vault |
| `overview_flat.png` | 2600 px, labelled, compass + scale bar |
| `framing_{south_entry,mid_nave_crossing,near_dais,west_aisle}.png` | the four **plate-scale** framings, plate + fade + vault at 40 %, T3m fade previewed within 6 m |
| `legend.json` · `measurements.json` | 33 id classes with per-band ghost opacities; every measurement above plus per-file sha256 |

Carried in unchanged: three pools (Z-618, Z-622, Z-623) · crossing piers and R4 cut low · the north breach stair on the playable side · E-SE-FIRE at the measured ‖p05‖ = 7.16 m · apron depth 3.0 m from the measured walk rate · 7 dark triforium galleries as descend-from-above spawns · walls 55 m as a framing device cropped at 28 m.

## 6 · Two defects this build found in itself

**⚑ The legend's list POSITION and its `index` FIELD had diverged, and it silenced an assertion.** `snap()` returns a legend list position; `IDX[name]` returns the index field. Inserting new classes ahead of older ones broke the identity between them, so `cls == IDX["debris"]` (32) compared against positions that stop at 27 — **always False**. The debris assertion dutifully reported **"0 pixels"** for 54 boxes that were rendering perfectly, and the blasted crowns reported 0 as well. *An assertion that cannot see what it is asserting about passes for the wrong reason, which is worse than failing.* Position == index is now an invariant, enforced by an `assert` in the generator.

**Consequence for the v2 treatment set, disclosed:** the same divergence shifted the ghost-opacity lookup by one class in the **composite images** of CA-guides-v2{a,b,c,d,z}. **The measurement table is unaffected** — the occlusion metric reads the geometry-derived `occl_*.npz` and the walkable mask, whose ids are all below the divergence point — but the *framings and overviews* of those five rendered their ghosts at a neighbouring band's opacity. Re-rendering them is one command if the archive should match the numbers.

**⚑ `(sel & dead).all()` is not "every cell under the footprint is dead".** It is an `all()` over the whole window, false whenever anything outside the footprint is walkable — i.e. always. Debris placement reported **"0 pieces"** as though no site existed. The predicate is `dead[sel].all()`. Third instrument this session that ran cleanly and answered a different question.

*(Also, smaller: placement tested unrounded centres while the record stored rounded ones, and a 0.5 mm shift flipped cells on the footprint boundary — the assertion fired on pieces placement had just cleared. Centres are rounded before testing now.)*

## 7 · Open

1. **Break fraction 0.35 is a tuned choice**, not a derivation — tuned against the ~20 % target with the vault as the constraint. 0.50 and 0.65 are one argument away.
2. **The ghost opacities (0.60 / 0.30 / 0.12) and the 6 m fade radius are DECLARED.** Both belong to the runtime and both ship as data.
3. **The opacity weighting in the metric is a model of legibility, not a measurement of it.** The honest test is Matt looking at the four framings.
4. **`south_entry` has no vault in frame** — bays near the south end fell with their piers. Diegetically right, and the one framing where the ceiling does not carry the indoor read; the piers do.
