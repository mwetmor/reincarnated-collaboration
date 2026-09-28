# CA-guides-v2 — cathedral arena GREY BOX: pier arcades, walkable aisles, vault

**Author** drax (presentation seam) · **Run** C-9 · **2026-09-28**
**Authority** **R-C9-53 / CORRIGENDUM-FORWARD 5** (no zoom-out; the indoor feel is carried OVER and AROUND the player) on top of R-C9-43/44/45 and the crack-law corrigenda.
**Supersedes** CA-guides-v1 (`286112bc6`), which stays on disk as the record of the measurement that produced R-C9-53. Nothing painted, no image generated.

**Chain** `tools/spec.py → tools/geom_v2.py → build.gd → tools/post_v2.py`, driven by `build_target.json` so v1 and v2 share one renderer and neither overwrites the other's inputs. Godot 4.6.3 Forward+/Metal, 6 tiles of 4096², **seven passes**: `guide · id · height · fade · id_fade · vault · arch`.

---

## 1 · What changed, and the one idea under it

R-C9-53 settled v1's conflict (1): **no zoom-out.** At plate scale the frame is 19 × 13 m of floor and ~10 m of wall, so the room cannot be shown by widening it — it has to be shown by putting architecture *over* the player (the vault) and *around* him (the piers). v2 builds both, and the measurement says it works: **100 % of reachable camera positions now contain a rising pier, and every framing contains vault.** v1's mid-nave frame was floor and a crater; v2's is a nave.

**The load-bearing production decision: a fading prop is NOT in the plate.** A pier that fades must have floor painted behind it, so the rising pier shafts and the three occluding west-wall bays are rendered in their **own layer** and are absent from the plate. What stays in the plate is a 0.35 m **plinth**, so the painter knows where each pier lands and the walkable mask excludes its footprint. Same for the vault: it is the overhead layer (scroll > 1, edge-anchored, T3p), never the plate.

Measured consequence, and it is large: walkable occlusion falls from v1's **9.304 %** to **3.992 %**, and void inside the frame union is **0.000 %**.

## 2 · The solve, and the walkable residual

The aisles are walkable and count toward the encounter area (R-C9-53 cl. 3), so the whole cruciform limb is play space with pier footprints punched out of it.

```
limb 23.573478 m  =  4.500 aisle + 2.00 pier + 10.573478 vessel + 2.00 pier + 4.500 aisle
```

| | |
|---|---|
| Gross cruciform | 2601.958476 m² |
| − crater | 63.617251 m² |
| − crypt mouth | 24.000000 m² |
| − **40 piers × 4.0 m²** | 160.000000 m² |
| **= net walkable** | **2354.341224 m²** |
| Target (MEASURED, unchanged) | 2354.341224 m² |
| **RESIDUAL** | **−4.547e-13 m²** |

**The pier count depends on the width** — the arms lengthen as the limb narrows — so this is a **fixed point, bisected**, not a quadratic like v1's. Aisle width is pinned at the lineage's own declared **4.5 m** rather than re-invented; the vessel absorbs the remainder at **10.573 m**, and the aisles carry **1007.880 m²**, 43 % of the play space.

**Raster cross-check 2362.320 m² at a 0.20 m cell, |Δ| = 7.98 m².** Larger than v1's 0.42 m² and the reason is the piers, not a disagreement: a 2.0 m pier straddles 10 or 11 cell-centres depending on its phase against the grid, so 40 piers carry ±0.4 m² each. The analytic solve is exact; the raster is a check, at its own resolution.

**Bay rhythm** — "about 6–7 m", chosen by minimising the distance to that band, then to 6.5 m:

| run | pitch |
|---|---|
| nave, south of the crossing | **6.403 m** ✓ |
| chancel, north | **6.423 m** ✓ |
| **transept arms** | **5.589 m** ⚑ |

⚑ **The arms cannot hit the band.** Between the west wall and the crossing pier line they run 22.36 m: 4 bays gives 5.589 m, 3 gives 7.453 m. Neither is in [6, 7]; 5.589 is the nearer. Named, not quietly rounded.

## 3 · Piers

**40 piers, 2.0 m square** — "thick piers you could hide a horse behind" (crack-law § 1, *mass before grace*). The lineage's arcade pier is 1.6 m; this is heavier on purpose. A horse is about 2.4 × 0.8 m, so a 2.0 m square hides one end-on and most of one broadside.

- **36 rising piers** are props with `fade: true`, id class **`nave_pier`**, each with `footprint_m`, `sort_line_y_m` and `height_m` in `registration_v2.json :: props`.
- **4 crossing-corner piers** stay **cut low at 0.9 m**, per the R-C9-53 cl. 4 settlement.
- **3 fading wall bays** — R1-nave-west bays 3, 4 and 5, which hide **6.5 / 46.2 / 93.9 m²** of the west transept arm. Flagged `fade: true`, id class **`wall_rising_fade`**, shipped in the fade layer with the plate carrying the floor behind them. This is v1's conflict (2), settled.
- **Pier height 123 m** in the fade layer. That is not an architectural claim: it is the height at which every pier top projects **above the canvas top**, so no pier crown can enter any frame and the sprite is cut by the canvas edge exactly as a prop leaving frame should be. It is **free**, because the pier is not in the plate and therefore does not size the canvas. The **architectural** pier runs to the vault springing at **26 m**, and that is the figure the overview draws and the props carry as `architectural_springing_m`.

### ⚑ Pier-frame fraction — the number gandalf asked for

Measured over **290 515** reachable camera positions (8 px blocks, sliding 1920 × 1080 window):

| | |
|---|---|
| frames containing a rising pier **or** a rising wall | **290 515 = 100.00 %** |
| frames containing a rising **pier** | **290 515 = 100.00 %** |
| frames containing a pier drawn only to the **vault springing (26 m)** | **290 515 = 100.00 %** |

The third row is the honest one: 100 % is **not** an artifact of the 123 m sprite. A 26 m pier projects 1576 px up-screen and the piers stand 6.4 m apart (≈450 px of screen-x), so from anywhere in the arena at least one pier column crosses the frame. **Target was "most"; it is all of them.**

*(The first cut of this measurement returned 0.00 %. The detector matched **id colours** against the **shaded** fade pass, which carries guide greys — a detector aimed at the wrong pass. The `id_fade` pass exists because of it. Fifth instance on this run of an instrument running cleanly and answering a different question.)*

## 4 · Vault

**55 bays.** Quadripartite: four boundary ribs, two diagonals (the only non-axis-aligned geometry in the grey box — boxes carry an optional `ry` yaw), a cell slab under the crown, and springers down to the pier tops. Rib section 0.7 m.

| | spring | crown |
|---|---|---|
| vessel — nave, chancel, both arms | 26.0 m | 34.0 m |
| aisles | 11.0 m | 14.0 m |
| crossing lantern | 26.0 m | **37.0 m** |

**(a) `overhead_vault_v2_guide.png`** — the vault as the camera sees it, RGBA with the green keyed to alpha, plus `overhead_vault_v2_mask.png`. This is the **ceiling / near layer**: scroll > 1, edge-anchored, y-sorted over the player (T3p — the cut end never on screen). Per chunk as `chunks/<chunk>_vault.png`.

**(b) `floor_light_v2.png`** — greyscale, plate-resolution, walkable only. **A painter's cue; never baked as geometry.** Per chunk as `chunks/<chunk>_light.png`. Model, every term declared:

```
L = 0.18 base
  + 0.62 · shaft        (the sunset beams, with each pier's shadow cut out of them)
  + 0.14 · ambient      (proximity to the window wall)
  − 0.09 · rib banding  (the vault's transverse ribs, at the 6.403 m nave bay pitch)
```

Shafts are projected from the **14 west-wall openings** (open triforium bays, the whole clerestory, and the west-top breach) along the sun direction to the floor; each pier interrupts every beam east of it within its own y-band, which is what makes the shafts *rake between the piers*.

### ⚑ CONFLICT — a real sunset cannot put shafts on this floor

The sun is due **WEST** (screen upper-left, per the register card and F-S1). But a beam entering at height *z* lands *z · cot θ* away:

| sun elevation | where the clerestory-sill (18.5 m) beam lands |
|---|---|
| **12° — a true sunset** | x = **+74.5 m**, i.e. **62.7 m past the east wall — outside the building** |
| **46.07° — solved** | the far (east) edge of the central vessel: shafts rake across the nave floor |

At a low sun, light from high windows lands on the *opposite upper wall*, not the floor — which is what really happens in a cathedral at dusk. **The guide is emitted at the solved 46.07°** so the art is usable, and the number is stated so the register's "low gold shafts raking the floor" is understood as a ~46° sun, not a sunset. If the sunset angle is the thing that must not move, the light has to come from lower openings (the ground arcade, or a breached lower west wall) — that is a design call, not mine.

## 5 · Camera, clamp, crown

Unchanged from v1: ortho, **ppm 100.617553710938**, pitch **52.9535411256029°**, **yaw 45° (camera SE → NW)**. Runtime is a 2D camera 1:1 on the plate, view 1920 × 1080, anchor (962, 595).

| | |
|---|---|
| Plate | **9236 × 8124** |
| Clamp (plate px) | **[0.33, 1205.03, 9234.27, 8122.64]** |
| Rising-wall height | solved **53.990 m**, built **55.0 m** |
| **Crown blocks inside any reachable frame** | **0 — PASS** |
| Walkable on screen | 2268.013 m² of 2362.320 plan — **3.992 % hidden** |
| Void inside the frame union | **0.000 %** |
| id snap, plate and fade | **0** (byte-exact, both) |
| Depth decode | floor median **7999 mm** (expect 8000), wall max **62999** (expect 63000) |

The wall solve covers **the plate's rising walls only** — piers are fade-layer props and do not enter it. Including them the first time drove the requirement to 89.4 m, which is an answer to a question nobody asked: R-C9-53 cl. 3 says the piers rise out of frame from "*almost* any position", and a prop's sprite is cut by its own canvas.

## 6 · Kept from v1 and the settlements

Three pools **Z-618, Z-622, Z-623** (Z-614 and Z-626 off the floor, Z-620 on the chancel apron) · four crossing piers and **R4** (the east arm's north wall) cut low, so the chancel and the empty cross mount stay visible · the north breach stair on the **playable side**, middle flights missing · E-SE-FIRE still derived from the measured **‖p05‖ = 7.16 m** · apron depth 3.0 m derived from the measured walk rate · 7 dark triforium galleries as descend-from-above spawns · 32 openings to the outside · the 57 m→55 m wall as a framing device cropped at 28 m, not a true-scale claim.

## 7 · Outputs

| file | what |
|---|---|
| `ortho_canvas_v2_{guide,id,walkable,window_holes,depth_mm}.png` | the plate, 9236 × 8124. Openings to the outside and un-architected background are flat pure `#00ff00` |
| `fade_layer_v2_{guide,mask}.png` | **RGBA** — the 36 rising piers and the 3 occluding west-wall bays. Absent from the plate by design |
| `overhead_vault_v2_{guide,mask}.png` | **RGBA** — the ceiling / near layer |
| `floor_light_v2.png` | greyscale floor-light guide (vault banding + sunset shafts + pier shadows) |
| `chunks/` + `chunks_v2.json` | 1536 × 1024, 256 px overlap, grid 11 × 8, **79 kept / 9 dropped, 73 inside the clamp**. Seven files per chunk: guide · id · mask · depth · window · **light** · **vault** |
| `overview_flat_v2.png` | 2600 px, plate + piers to the vault springing + vault at 30 %, labelled, compass + scale bar |
| `framing_{south_entry,mid_nave_crossing,near_dais,west_aisle}.png` | **PLATE scale only**, plate + fade + vault at 40 %, with the **T3m pier fade previewed within 6.0 m** of the player |
| `legend_v2.json`, `measurements_v2.json` | 28 id classes; every measurement above plus per-file sha256 |

**Divergence rows owed:** `DIV-nave-piers` (obstacles at the vessel edges the measured open plane did not have — named in R-C9-53 cl. 3), `DIV-aisles-walkable`, `DIV-arm-bay-pitch-5.589`, `DIV-floor-light-sun-46deg`, plus v1's list, which stands.

## 8 · Open, and not mine to close

1. **The sunset angle** (§ 4). 46.07° is a solve, not a ruling.
2. **The T3m fade radius.** 6.0 m is DECLARED for the framing preview — about three body-widths, where a 2 m pier stops reading as a wall. The real parameter belongs to the runtime.
3. **A fading prop needs its own paint.** Because the piers are not in the plate, the dressing pass has to paint 36 pier sprites (or a few and reuse) *and* the floor behind them. That is a burst-count consequence of the fade, and it should be priced before the chunk wave.
4. **The arms' 5.589 m bay** (§ 2).
