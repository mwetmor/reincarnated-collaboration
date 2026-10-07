# DEV-18 — heather and snow on the terrain: measurement and patch proposal (lane PT, R-C9-192). NOT APPLIED.

## Measured (`dev18_measure.json`, figure `dev18_tufts_flat_green_slope_red.jpg`)
- **31.1% of the pilot's painted tuft pixels** (142,529 of 457,641) lie on sloped ground (|terrain| ≥ 0.03 m) and got **no 3D heather**. The pilot prep's h = 0 back-projection classified 33.2%.
- By ground class:
  - shrub patches: 104,442 px;
  - the mound flank: 31,028 px;
  - snow: 7,059 px.
- By chunk: 0_0 is 100% sloped, 1_0 90%, 2_0 and 0_2 21%, 1_2 6%; the ring and wreck chunks are 0%. This is the northern rise at u -24..-6, v 17..22.
- **The slopes are gentle:** ground height under the sloped tufts is 0.06 m at p10, 0.18 m at p50 and 2.3 m at p90.
- **The snow:** 12.7% of walkable land (snow, path, shrub) is sloped and has no snow field. There he leaves no prints; the painting's snow shows. P9's trail coverage of walkable snow would count that land as uncovered.

## Proposal (diffs in this folder)
- **(a) `a_bv2f_prep_heather_and_snow_on_terrain.diff`** (PT's `bv2f_prep.py`, opt-in config flags):
  - `heather_on_terrain`: every land tuft is a candidate. Each spray stands on the true ground point under its footprint centre: the view ray meets the heightfield, found as a 12-step fixed point h ← terrain(uv(px, h + spray_h/2)). The row gains column 7, the ground height; v1's columns 0–6 are unchanged.
  - `snow_on_terrain`: v1's snow-by-class depth applies on all land. A ground-height grid `snow_ground_h.bin` in the depth grid's own layout is written and sha-recorded in the manifest.
- **(b) `b_bv2f_pilot_heather_y.diff`** (PT's `bv2f_pilot.gd`): v1's `_build_painted_heather` (barrow_full.gd:2292–2346) is copied with ONE marked line changed: the spray's y is `row[7] − 0.01` when present, otherwise v1's −0.01.
- **(c) `c_snow_field_terrain_copy.diff`**: a pilot-only COPY of v1's `snow_field.gd` as `scripts/bv2f/snow_field_terrain.gd`. v1's file is untouched. Four marked lines:
  - a `ground_h_tex` RF texture plus `ground_h_on`;
  - in the vertex shader, `VERTEX.y += h + ground_h_on * texture(ground_h_tex, UV).r`, so the field's plane UV is the grid.

  With no ground height it is v1's field exactly. The painted snow shader is `PaintedWorld.snow_shader_code()`, derived from v1's `SnowField.SHADER`. The pilot's dress therefore applies the same two shader edits to that override code as asserted string swaps (one more marked line pair in `bv2f_pilot.gd`).

## Dry run of (a) (`proposal_dryrun.json`; outputs in scratch, nothing applied)
- v1's counts are unchanged: 236 heather, 30 shrub. Tuft cells covered: heather 0.3708 (current 0.3756), shrub 0.2285 (0.2925). The pool is larger and the counts are the same.
- 26.7% of sprays move onto sloped ground: p90 0.25 m, max 3.53 m.

## Open for the ruling
1. **Counts:** keep v1's density-derived counts (as proposed), or let the larger pool raise them through `heather_instances.py` on the full density? The latter is a Tier-A input change, not a code change.
2. **Snow lighting:** the snow's normal ignores the terrain slope (v1's shader shades the field as flat). On the painted path the base colour is the painting, so the visible effect is limited to his prints' relief. This needs a look on the mound flank before it is relied on.
3. **Acceptance:** P9 trail coverage on walkable snow (≥ 0.99) re-measured with (c); P8 heather precision re-measured with (a).
