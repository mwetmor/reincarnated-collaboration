# T10 — seam repairs: three tiles, three EDIT canvases

Measured by `30_seam_test.py`: roll the tile by half its width and half its height so every
edge that will meet a neighbour meets itself in a cross through the middle, then compare the
step energy across that cross against **the same statistic on the tile's own interior
lines**. A busy rock tile and a smooth snow tile are then judged on the same question — *is
there more discontinuity at the wrap than this material has anywhere else?* — and a seamless
tile scores about 1.0 whatever it is made of. Control leg, run every time: the same tile with
a forced brightness step scores **10.26**, so the instrument can see a seam.

Full numbers in `t10_barrow/seam_report.json`.

## Passing — no edit needed

| tile | pick | worst ratio |
|---|---|---|
| `T10T-path` | **b** | 1.20 |
| `T10T-heather` | **b** | 1.43 |
| `T10T-ice` | **a** | 1.48 |

## Failing — canvases ready in `t10_barrow/seam/`

| tile | pick | vertical wrap | horizontal wrap | canvas |
|---|---|---|---|---|
| `T10T-snow-r1` | **a** | 1.60 | 1.68 | `T10T-snow-r1_a_rolled.png` |
| `T10T-rock` | **b** | 1.71 | 1.48 | `T10T-rock_b_rolled.png` |
| `T10T-bark` | **a** | **1.86** | **0.81** | `T10T-bark_a_rolled.png` |

**Bark is a one-axis repair, and that matters.** `bark_a` scores **0.81 horizontally —
cleaner across its wrap than it is anywhere in its own interior** — and 1.86 vertically. A
trunk is wrapped *around* by the horizontal axis and repeated *along* its length by the
vertical one, so only the vertical seam is ever seen as a ring around the trunk. Ask for the
horizontal line of the cross only, and leave the vertical line alone: it is already better
than the material.

---

## The brief for each (one EDIT call per tile)

> IMAGE 1 is a seamless ground-material tile that has been **rolled by half its width and
> half its height**, which brings its four outer edges together into a **cross through the
> middle of the picture**. Along that cross the material does not line up: the pattern stops
> and restarts, and there is a visible join.
>
> Use image_gen in EDIT mode on IMAGE 1 and deliver ONE image, the same size, that is
> IMAGE 1 with **the join along that cross painted out**, so the surface runs continuously
> straight through the middle in both directions — the same grain, the same scale of detail,
> the same colour, with no line, no ridge, no band and no blur where the join was.
>
> **EVERYTHING ELSE IS UNCHANGED, pixel for pixel.** Do not repaint, restyle, recolour,
> sharpen or move anything away from the cross. Do not add any new feature, object, crack,
> footprint or mark. Do not darken or lighten any region: the tile carries **no light** —
> no direction, no shadow, no occlusion, no vignette, and no corner brighter than another.
> The repair is a few centimetres of material either side of the join and nothing more.
>
> The four OUTER edges of the image must also stay exactly as they are — they are the
> middle of the tile once it is rolled back, and moving them would put a new seam where
> there is none now.

**Per tile, the one extra line:**

- **`T10T-snow-r1_a`** — *the material is windblown snow: fine granular white with faint
  parallel wind ripples and small crescent drifts. Carry the ripple direction straight
  through the join rather than letting it change angle across it.*
- **`T10T-rock_b`** — *the material is fractured grey granite with a slanting bedding, hairline
  cracks and patches of grey-green and rust-orange lichen. Carry the bedding angle and the
  crack directions through the join; do not end a crack at the line or start one on it.*
- **`T10T-bark_a`** — ***repair the HORIZONTAL line of the cross only.** The vertical line is
  already seamless and must not be touched. The material is chalk-white birch bark peeling
  in papery curls, banded with black lenticel scars. Carry the bands straight across.*

**Retry only if** the join is still visible, a new feature appeared, any region away from the
cross changed, the outer edges moved, or light or shadow was introduced. Never retry for
overall colour.

## After they return

Roll each one back by the same offset and re-run `30_seam_test.py`. Both numbers, before and
after, go into `seam_report.json`, so a tile that was accepted on the second pass says so.
Then all six are resampled from their native 1254² to **1024²** — done last, because
resampling changes the seam statistic slightly and the measurement should be of the tile
that was painted, not of a resize of it.
