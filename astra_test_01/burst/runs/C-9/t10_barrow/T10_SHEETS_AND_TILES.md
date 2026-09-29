# T10 — the Frost King's Barrow: asset sheets and ground tiles, for gandalf to fire

Concept **variant a** (the terrain numbers that chose it are in
`t10_barrow/out/height_a_marigold.json` and `height_b_marigold.json`). Scale bar: the barbarian at **1.85 m**
measures 157 screen px, so **K = 140.86 px/m**. Every size below is a ruler reading off the
concept through K — `height_m = px / (K · cos 52.9536°)`, `width_m = px / K`. **No depth
model is involved in any of them**, so none of them carries the terrain's 1.71× calibration
spread.

Identity plates are in `t10_barrow/plates/`, cut from the concept at native resolution and
matted onto flat #00ff00. Manifest: `t10_barrow/asset_plates.json`.

| sheet | assets | true size | plate |
|---|---|---|---|
| **T10P-A** | standing stone, tall — two carvings | 2.71 m × 0.72 m | `T10_standing_stone_tall.png`, `T10_standing_stone_mid.png` |
| **T10P-B** | barrow lintel; barrow post | 2.28 m long × 1.18 m; 2.04 m × 0.52 m | `T10_barrow_lintel.png`, `T10_barrow_post.png` |
| **T10P-C** | rock outcrop, large; rock outcrop, small | 1.84 m × 0.75 m; 0.54 m × 0.73 m | `T10_rock_outcrop_large.png`, `T10_rock_outcrop_small.png` |
| **T10P-D** | dead birch — **Tripo sheet plus a procedural fallback** | 3.36 m × 1.38 m | `T10_dead_birch.png` |
| **T10P-E** | standing stone, short; juniper bush | 1.24 m × 0.64 m; 1.15 m × 0.87 m | `T10_standing_stone_short.png`, `T10_juniper_bush.png` |

The **raven** is not on a sheet: reuse the T9 build, `runs/C-9/t9_props/reduced/raven.glb`,
0.28 m. The **barbarian** is not an asset; he is the ruler.

---

## The clause common to every sheet

> **Why this sheet exists.** A 3D model is built from these four views, placed in a snowbound
> level, and **lit there by a real sun**. The world is being built the way the character was
> built, so the same two things decide whether the sheet works.
>
> **One object in four views, not four objects.** The same silhouette, the same stone, the
> same carving, the same every mark, seen from four sides. The two profiles are each other's
> mirror — that is the one constraint a drawing cannot fake and a multiview build cannot
> recover from.
>
> **Paint the surface, not the lighting.** Soft, even, shadowless light from nowhere in
> particular. No key, no bright side and dark side, no rim light, no cast shadow, no shadow
> on the ground, no ambient dark gathering in the cracks. Tone comes from the object's own
> colours and from the pen hatching. Light that is painted in happens twice when the engine
> lights it — that is the whole finding of T9.
>
> **SNOW IS PAINTED AS SURFACE COLOUR, NOT AS LIGHT.** Where the concept shows a cap of snow
> on a stone or a rock, paint it: cream-white, granular, with its own soft edge and the pen
> line around it. It is the object's albedo, the same as its lichen. A shader adds snow to
> upward faces on top of this, so paint what is *there*, not what the sun does to it.
>
> **SHEET.** Flat pure #00ff00, nothing else. The four views of one object at exactly the
> same scale, on one ground line, each filling most of its cell. Columns left to right:
> **FRONT**, **RIGHT SIDE** (profile, facing the viewer's right), **BACK**, **LEFT SIDE**.
> No ground, no shadow, no text, no labels, no cell borders, no other objects, nothing
> overlapping.
>
> **STYLE:** the REGISTER CARD governs line, washes, light and plate; its manuscript-subject
> clause does not apply. Paint in IMAGE 2's hand (`inputs/nb_style_ref_matt.png`) — the same
> hand the barbarian is painted in.

---

## T10P-A — the standing stones (two variants, one scale)

**Sheet:** 1536×1024 landscape, 4 columns × 2 rows. Top row the first stone, bottom row the
second; each row is one stone in four views at one scale.

> **THE OBJECT.** A tall upright standing stone of weathered grey-green granite, about one
> and a half times a man's height, set in the ground: a rough four-sided pillar, wider at
> the base, its top broken and irregular, its faces pitted and flecked with pale lichen.
> Down the face of each stone, cut into the rock and filled with **dark red ochre**, is a
> panel of Norse knotwork — IMAGE 1 shows an interlaced **serpent or beast**, IMAGE 2 a
> **spiral and wheel** device. Keep each stone's own carving, on its own front face, and
> absent from the back.
> **A cap of wind-packed snow sits on the top** and in the deeper cuts of the carving. Paint
> it as surface. No snow on the underside of an overhang.
> The two stones are the same kind of stone and the same height; they differ in their
> outline, their breakage and their carving. Do not make them twins and do not make them
> two different materials.

## T10P-B — the barrow door: lintel and post

**Sheet:** 1536×1024 landscape, 4 columns × 2 rows. Top row the **lintel**, bottom row the
**post**.

> **TOP ROW — THE LINTEL.** A massive single slab of grey granite laid flat as the beam over
> a barrow doorway: about two and a quarter metres long, roughly a metre deep front to back,
> its ends rough-broken, its top surface flat and weathered. Its **whole front face** carries
> a continuous band of deep-cut Norse knotwork in dark red ochre — interlaced serpents
> running out from a central **wheel cross**. The back face is plain, undressed rock. A ridge
> of snow lies along the top edge.
> **These four views are the LINTEL ALONE** — no posts, no doorway, no mound, nothing under
> it or beside it.
>
> **BOTTOM ROW — THE POST.** One of the two upright jambs: a squared granite pillar about two
> metres tall and half a metre across, its inner face dressed flat, its outer face rough.
> The front face carries a vertical panel of the same dark red ochre knotwork, a plaited band
> running its full height. Snow caught on its top and in the carving. **The post alone** — no
> lintel, no second post, no doorway opening.

## T10P-C — the rock outcrops

**Sheet:** 1536×1024 landscape, 4 columns × 2 rows. Top row the **large outcrop**, bottom row
the **small** one.

> **TOP ROW — THE LARGE OUTCROP.** A shoulder of bare bedrock breaking up through the snow,
> about the height of a man's chest and three quarters of a metre across: fractured grey
> granite in blocky angular steps, its bedding running at a slant, faces mottled with
> grey-green and rust-orange lichen, moss in the deeper cracks. A thick cap of snow across
> its upper surfaces and lodged in every ledge.
>
> **BOTTOM ROW — THE SMALL OUTCROP.** The same rock, lower and wider — a half-buried slab
> about knee height and three quarters of a metre across, one flat face tilted up out of the
> snow, its edges rounded by weather. The same lichen, the same snow, the same stone.
> These two must read as the same rock in the same place, one large and one small.

## T10P-D — the dead birch (**and its fallback**)

**Sheet:** 1024×1536 **portrait**, 2×2. Top-left FRONT, top-right RIGHT SIDE, bottom-left
BACK, bottom-right LEFT SIDE.

> **THE OBJECT.** A dead mountain birch, wind-bent, about twice a man's height: two or three
> slender trunks rising from one root, their bark chalk-white and peeling in papery curls,
> banded with black scars and knot-eyes. All the branches are **bare** — no leaves, no buds —
> dividing and re-dividing into fine twigs, everything leaning the same way as if pushed by
> years of one wind. Snow lodged along the upper side of the thicker limbs and in the fork.
> **The twigs are the whole difficulty.** Draw them with a clear unbroken ink line rather than
> as a soft mass, and keep a gap of green between every twig and everything behind it.

> **FALLBACK, and I would like it built either way — Tripo is the weak tool here.** The T9
> snag was the worst of five models at 0.484 silhouette IoU against its own sprite, and a
> bare birch is that problem doubled: a photogrammetric reconstructor turns fine twigs into
> lumps or loses them. So alongside the Tripo build:
>
> **PROCEDURAL BIRCH — Blender Sapling / geometry nodes, with an Astra bark tile.** The trunk
> and branch skeleton come from Sapling's `Black Tupelo` or `Weeping Willow` preset re-tuned
> (3 levels, no leaves, strong `attractUp` negative and a wind-lean applied as a bend), which
> gives exact, clean, arbitrarily thin twigs and a controllable silhouette. It needs ONE
> Astra image instead of a sheet: a **seamless 1024² birch-bark albedo tile** — chalk-white
> peeling bark, black lenticel scars and knot-eyes, painted flat with no light — wrapped
> round the trunks by cylindrical UV. The branch ends take the same tile at a smaller scale.
> That gives a birch whose geometry is exact and whose surface is in our hand, at zero Tripo
> risk. **Judge the two by silhouette IoU against the concept's own birch**, the same test
> that found the snag, and keep the winner.

## T10P-E — the short stone and the juniper

**Sheet:** 1536×1024 landscape, 4 columns × 2 rows. Top row the **short stone**, bottom row
the **juniper**.

> **TOP ROW — THE SHORT STANDING STONE.** A stump of a standing stone barely waist-high on a
> man, broad and squat: the same grey-green lichened granite as the tall ones, its top broken
> off level and rough, leaning slightly. A faint worn remnant of red ochre carving on its
> front face — much more eroded than the tall stones, only a trace of the pattern left. Snow
> across its broken top.
>
> **BOTTOM ROW — THE JUNIPER BUSH.** A low sprawling mountain juniper about knee-to-waist
> high and a little under a metre across: a dense tangle of short stiff branches radiating
> from a low centre, dark blue-green needles in tight prickly sprays, dead grey-brown twigs
> showing through inside, a scatter of dusty blue berries. It grows wider than it is tall and
> hugs the ground. Snow caught in the top of the mass, not under it. **The bush alone** — no
> rock, no ground, no snowdrift beneath it.

---

# The ground tiles — five seamless 1024² albedo tiles

All five: **1024×1024, seamless and tiling in both directions, flat top-down, albedo only.**

> **COMMON CLAUSE.** This is a ground material tile for a 3D level, seen from directly above
> and tiling edge to edge in both directions. **It carries colour and material and nothing
> else**: no light direction, no cast shadow, no ambient occlusion in the hollows, no vignette,
> no highlight, no gradient across the tile. The renderer lights it. Painted in the REGISTER
> CARD's hand — transparent washes that pool and granulate, fine pen hatching where the
> surface has texture, cream paper left bare for the palest areas — but **even across the
> whole square**, with no corner darker or lighter than another. Fill the frame: no border,
> no margin, no text, no object sitting on the surface, no footprints unless the tile is the
> path. The pattern must not show an obvious repeat or a recognisable single feature that
> would betray the tiling.

1. **T10T-snow** — fresh windblown snow. Near-white, faintly blue in the hollows, with the
   soft parallel ripples and small crescent drifts that wind leaves; a dry granular surface,
   a few tiny grass tips and grit specks breaking through.
2. **T10T-path** — trodden snow. The same snow compacted and walked over: **overlapping
   bootprints in every direction**, edges crushed and re-frozen, the surface greyer, harder
   and more level than fresh snow, with a little grit and dead grass trodden up into it.
3. **T10T-rock** — bare granite. Fractured grey stone with a slant bedding, blocky angular
   faces, hairline cracks, grey-green and **rust-orange lichen** in irregular patches, dark
   moss in the deeper seams.
4. **T10T-ice** — frozen tarn. Pale blue-green lake ice seen from above: a network of white
   **pressure cracks and healed fractures** dividing it into irregular plates, frozen bubbles
   and feathery white frost blooms, deeper blue where the ice is clear and thick.
5. **T10T-heather** — dead winter grass and heather. Matted ochre and straw-brown grass
   pressed flat, with wiry dark heather stems, small rust-red leaves and a few bleached seed
   heads; a little dry snow caught among the stems.

## The seam method, before any of them is accepted

1. **Wrap test, free and automatic.** Roll the returned tile by half its width and half its
   height (`np.roll(img, (512, 512))`), which brings all four edges together into a cross
   through the middle. Measure the gradient energy along that cross against the local
   average away from it. **A seamless tile scores about 1.0; a visible seam scores well above
   it.** The threshold is set by measurement, not taste: the same statistic is computed on an
   interior line of the same tile to give the null.
2. **If it fails**, do not re-fire the whole tile — fire an **Astra EDIT of the ROLLED
   image**, asking only that the cross of mismatched material through the middle be painted
   out so the surface runs continuously across it, everything else untouched. Then roll it
   back by the same offset and re-run the wrap test. The edit is on the rolled image
   precisely because that is where the seam is *in the middle of the canvas*, which is the
   one place a painter can work on it.
3. **Both numbers go in the record** — before and after — so a tile that was accepted on the
   second try says so.
