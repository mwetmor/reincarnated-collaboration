# T9-1b — the albedo repaint: canvases and the brief note per canvas

Three canvases, each an **exact 1536×1024 crop of `godot/plate/plate_v4.png` at native
resolution**. Between them they cover every painted pixel of the measured bridge frame
(plate x 2500–4420, y 487–1567) and of that frame plus a 200 px margin — **0 painted
pixels fall outside them**, asserted in `tools/cut_albedo_canvases.py` on every cut.

| id | canvas | plate rect | clear | overlaps |
|---|---|---|---|---|
| `top` | `canvas/t9_albedo_top.png` | x 3120–4656, y 103–1127 | 22.45 % | `bot_left` 440×200, `bot_right` 1296×200 |
| `bot_left` | `canvas/t9_albedo_bot_left.png` | x 2024–3560, y 927–1951 | 28.61 % | `top` 440×200, `bot_right` 200×1024 |
| `bot_right` | `canvas/t9_albedo_bot_right.png` | x 3360–4896, y 927–1951 | 1.98 % | `top` 1296×200, `bot_left` 200×1024 |

Alpha masks in `mask/`, per-canvas layout in `layout/`, the grid in `t9_albedo_grid.json`.
Drop returns in `t9_1b/painted/` as `t9_albedo_<id>.png` and run
`python3 tools/reassemble_albedo.py` (run `--self-test` first; it passes).

**Why there are three and not four.** A 2×2 grid over frame+margin puts 92 % flat green in
the top-left canvas — an Astra call spent on the void. The top canvas is slid left to
x 3120 instead, which swallows the plateau lip the 2×2 grid would have split down the
middle, and the void is simply not covered, because the void has nothing to repaint.

---

## The clause that is common to all three

> This canvas is a native-resolution crop of the approved painted cliffside. The repaint
> is an **albedo** pass: this world is about to be lit by a real sun in the engine, and
> anything the sun will do must come out of the paint first, or it happens twice.
>
> **REMOVE three things.** (1) The **key light** — the low warm sun from screen upper-left
> and every trace of its direction: the gold on the slopes that face it, the violet-indigo
> on the faces turned away, the whole bright-side/dark-side split on every rock, post,
> plank, tuft and stone. (2) Every **cast shadow** — the long shadows the rail posts throw
> across the ground, the shadow under the bridge deck, the shadows thrown by boulders,
> grass clumps and the cliff lip, and every shadow one thing drops on another. (3) The
> painted **ambient occlusion** — the dark that gathers in cracks and joints, under
> overhangs, in the seams between rock columns, at the base of every grass tuft, pebble
> and post where it meets the ground.
>
> **KEEP four things, exactly.** (1) **Local colour**: sand stays that sand, grass stays
> that green, rock stays that pale grey, wood stays that brown — the hue and the material
> of every surface are unchanged, only the light on them goes. (2) **Material and texture
> detail**: every grain, crack, pebble, flower, blade, moss patch, plank joint and nail
> head stays, at exactly the detail it has now. (3) **Every edge's position**: not one
> contour, silhouette, joint, boundary or line moves by a single pixel. (4) The **drawn
> ink line and its hatching**, which after the light is gone are what still carry the
> form — they are the darkest marks in the picture and they stay.
>
> What comes back should read as this same painting seen under **flat, even, shadowless
> light**: one even mid-tone per material across its whole area, form held by the pen line
> and the hatching rather than by a light direction. Pale, not bleached; no area goes to
> white and no area stays black.
>
> **NO NEW OBJECTS.** Nothing is added, nothing is restyled, nothing is recoloured,
> sharpened, softened or moved. **THE GREEN IS A KEYING PLATE**: flat pure #00ff00 marks
> where the painting is transparent. Leave every green pixel exactly that green; do not
> extend paint into it and do not let paint retreat from it — its ragged boundary is the
> transparency mask and it must not move.
>
> **REGISTRATION IS IMMOVABLE.** Deliver exactly 1536×1024, same framing, every feature on
> the pixel it is on now. This image goes back onto a 5376×4096 plate by phase correlation
> and is checked to the pixel; a crop, a pan, a zoom or a rescale cannot be recovered.

---

## `top` — the far plateau, the bridge's east landing, two rail posts

The east side of the chasm: the bridge's far landing and the first two deck planks at
lower-left, the open sandy path sweeping up to the right, banks of grass, scrub and small
white and yellow flowers along the top and right, and the layered rock lip of the cliff
running top-to-bottom through the left third, with flat green beyond it where the chasm
opens. The painted light here is at its most explicit: the sand reads warm gold across its
whole sweep and cools to grey-violet where it turns away, the rock lip has deep shadow
banked in every ledge and crack, each grass clump sits in its own pool of dark, and **each
of the two rail posts throws a long, hard shadow across the sand to its right** — those
two shadows are the most conspicuous single thing to remove in this canvas. Take the key,
the cast shadows and the ambient occlusion out of all of it; leave the sand its own
colour, the grass its own green, the rock its own pale grey, every pebble, blade and
flower exactly where it sits, and the deck planks their own brown with every joint, nail
and split unchanged. The green at the left is the chasm: it does not move.

**Plus, on this canvas only — remove the two rail posts themselves.** `bridge_post_3`
stands at canvas (541–582, 449–553) at the deck's far corner, and `bridge_post_2` at
(781–824, 628–733) further down the lip. Remove each post, its shadow and the dark it
casts at its own foot, and continue the ground behind it exactly as painted beside it —
same sand, same grass, same stones, same rock ledges, running on naturally with no gap, no
patch and no new object. *(Why: the posts are rebuilt as real 3D props at the blockout's
true 1.20 m. The painted posts stand 1.81 m — 1.512× the geometry they sit on — so if they
stay in the plate, 37 screen pixels of painted post stand above every real one.)*

## `bot_left` — the near plateau, the bridge's west landing, two rail posts, the chasm edge

The west side: the open sandy plateau filling the lower two-thirds, the bridge's near
landing and deck running up to the top-right corner, two rail posts at the deck's corners,
scrub and yellow-flowered grass banding the lip, the west cliff face falling away at the
right in pale vertical strata, and at the bottom-right the chasm's cloud bank against flat
green. The painted key runs the same way — the sand warm where it faces the light and cool
where it does not, the cliff face banked in shadow, a dark rim under every grass clump and
stone, **and both posts throwing shadows to their right across the sand**. Remove the key,
the cast shadows and the ambient occlusion from the plateau, the lip, the cliff face, the
deck and the grass. Keep the sand's colour, the grass's green, the stone's grey, the deck's
brown and every pebble, blade, flower, crack and plank joint precisely where it is.

**Leave the cloud bank in the chasm exactly as it is** — every wisp, every fold, its warm
pink and lilac, and above all the ragged edge where it meets the green. It is not ground,
it is never touched by the engine's sun, and its boundary is a transparency mask.

**Plus, on this canvas only — remove the two rail posts themselves.** `bridge_post_1` at
canvas (954–992, 215–320) and `bridge_post_0` at (1196–1235, 391–501), each with its
shadow and the dark at its foot, continuing the deck edge and the ground behind exactly as
painted beside them. Same reason as `top`.

## `bot_right` — the east chasm wall, the plateau above it, the cloud bank

The tall east wall of the chasm: great pale columns of rock, fissured and ledged, running
from the plateau's edge down out of frame, with meadow grass, scrub and small flowers on
the plateau above at the right, a corner of the bridge deck at the top-left, and the
chasm's cloud bank filling the left. **This canvas carries most of the darkness the whole
step exists to remove**: the deep shadow banked between every rock column, the black in
every fissure, the violet-indigo under the plateau's overhanging lip, and the dark rim
under every ledge and every clump of grass on top. All of it is painted light, and all of
it goes — the rock keeps its own pale grey-buff colour across its entire face, every
column, crack, ledge, tuft of moss and trailing plant stays exactly where it is and
exactly as detailed, and the pen line and hatching stay as the only dark marks. The
plateau's grass keeps its green and all its flowers; the deck corner keeps its brown.

**Leave the cloud bank exactly as it is**, every fold and its whole ragged boundary
against the green, for the same reason as `bot_left`. There are **no rail posts on this
canvas** — nothing is to be removed here.
