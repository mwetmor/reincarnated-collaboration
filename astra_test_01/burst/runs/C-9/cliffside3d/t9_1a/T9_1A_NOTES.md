# T9-1a — the prop model sheets: layouts, identity plates and the brief note per sheet

Eight props, **five objects**: the four rail posts are four instances of one rail post and
get one model, yawed differently per instance. Three sheets, grouped so that everything on
a sheet is near enough the same size to share a scale.

| sheet | objects | identity plate (IMAGE 1) | sheet size / grid |
|---|---|---|---|
| **T9P-A** | the scorched snag (`bridge_obj_01_a`) | `t9_1a/T9P-A_identity.png` | 1024×1536 portrait, 2×2 |
| **T9P-B** | the rail post (`bridge_post_0…3`), the burnt stump (`bridge_obj_01_c`) | `t9_1a/T9P-B_identity.png` | 1536×1024 landscape, 4 cols × 2 rows |
| **T9P-C** | the coil of rope (`bridge_obj_02_a`), the perched raven (`raven_perched`) | `t9_1a/T9P-C_identity.png` | 1536×1024 landscape, 4 cols × 2 rows |

IMAGE 2 on every sheet is `runs/C-9/artifacts/inputs/nb_style_ref_matt.png` — the same hand
the barbarian was painted in, so the props he stands among come from the same hand.

**True scale, and where each number comes from.** The painting and the geometry disagree
about how big a prop is, and the disagreement is measurable rather than guessed: the rail
posts exist in both. `cliffside_blockout.gd:659` builds them 0.22 × **1.20** × 0.22 m; the
painted post is 110 sprite px, which under `(h/PPM)/cos(pitch)` is **1.81 m**. The painting
draws its props **1.512×** larger than the geometry they stand on. Applied to the props
that have no blockout twin, that factor is an *inference from one measured class* — stated
so it can be overruled. The raven is the exception: 1.512 still leaves it 0.60 m, and a
raven is 0.28 m, so the bird is scaled from life.

| prop | painted implies | true target | on screen at true scale |
|---|---|---|---|
| rail post | 1.81 m h | **1.20 m h, 0.22 × 0.22 m** (blockout) | 72.7 px |
| scorched snag | 4.27 m h, 2.19 m span | **2.80 m h, 1.45 m span** | 170 px |
| burnt stump | 1.17 m h | **0.80 m h, 0.55 m across** | 48 px |
| coil of rope | 0.94 m across | **0.62 m across, 0.15 m high** | 62 px across |
| perched raven | 0.91 m h | **0.28 m h, 0.50 m long** (from life) | 17 px |
| *the barbarian, for comparison* | — | 1.85 m at figure scale 1.0 | **112.1 px** |

---

## The clause that is common to all three sheets

> **Why this sheet exists, so you can judge your own result.** A 3D model is built from
> these four views, placed in a cliffside level, and **lit there by a real sun**. So two
> things decide whether the sheet works.
>
> **One object in four views, not four objects.** The same silhouette, the same colour,
> the same bark or grain or feather, the same every mark, seen from four sides. Any
> disagreement between the views becomes a seam in the model or a hole in it.
>
> **Paint the surface, not the lighting.** Soft, even, shadowless light from nowhere in
> particular. No key light, no bright side and dark side, no rim light, no cast shadow, no
> shadow on the ground, no glow, no ambient dark gathering in the cracks. Tone comes from
> the object's own colours and from the pen hatching, never from a light direction. This is
> the same albedo rule the terrain is being repainted under: light that is painted in
> happens twice when the engine lights it.
>
> **SHEET.** Flat pure #00ff00, nothing else in the background. The four views of one
> object sit at exactly the same scale, on one ground line, each filling most of its cell.
> Column order left to right is **FRONT** (facing the viewer), **RIGHT SIDE** (in profile,
> facing the viewer's right), **BACK** (seen from behind), **LEFT SIDE** (in profile,
> facing the viewer's left). No ground, no shadow, no text, no labels, no cell borders, no
> other objects, and nothing overlapping anything.
>
> **STYLE**: the REGISTER CARD governs line, washes, light and plate; its manuscript-subject
> clause does not apply to these props, whose subject is set by this brief. Paint in IMAGE
> 2's hand — warm dark-brown ink line of varying weight, transparent washes that pool and
> granulate, fine hatching in the shadows, cream paper highlights.

---

## T9P-A — the scorched snag

**Sheet:** ONE 1024×1536 **portrait** sheet, 2×2. Top-left FRONT, top-right RIGHT SIDE,
bottom-left BACK, bottom-right LEFT SIDE.

> **THE OBJECT** — a burnt dead tree, shown in IMAGE 1 as it is painted in the level. A
> heavy trunk, about twice a man's height, broken off high into three or four jagged
> splintered spires; deeply furrowed charred bark in plated grey-brown ridges; a long
> vertical split down the front of the trunk that glows **orange-hot at its lower end like
> a live ember**; two thick bare branches forking out left and right at mid-height, each
> breaking into bare twigs; flared buttress roots at the base. Standing with it, part of
> the same group: **two small bare dead saplings**, a taller one on its left and a smaller
> one on its right, thin stems with a few bare twigs, rooted in the same ground.
>
> **THE EMBER STAYS.** The glowing split is the object's own light, not the sun's — keep
> it, exactly where IMAGE 1 puts it, in every view where that face of the trunk is turned
> toward the viewer, and absent from the views where it is not. Everything else about the
> lighting goes: no warm key down one side, no dark side, no shadow under the roots.
>
> Keep the saplings in all four views, in the same places relative to the trunk, so the
> four views are four views of one group. The twigs are thin — draw them with a clear
> unbroken ink line rather than as a soft mass, and keep a gap of green between every twig
> and everything behind it.

## T9P-B — the rail post and the burnt stump

**Sheet:** ONE 1536×1024 **landscape** sheet, 4 columns × 2 rows. **Top row: the rail
post**, four views. **Bottom row: the burnt stump**, four views. Each row is one object at
one scale on one ground line; the row's four views fill most of the row's height.

> **TOP ROW — THE RAIL POST.** A single square-section timber post from a rope-bridge rail,
> shown in IMAGE 1 (which shows the same post as it is painted at four places in the level
> — it is **one post**, not four). Weathered warm-brown squared timber, roughly hewn, with
> strong vertical grain, splits and old knots down each face; the top is cut to a shallow
> **chamfered pyramid** with a split across it; the foot is plain, cut square, with a
> little wear and chipping. No rope, no rail, no nails, no ironwork, nothing tied to it,
> nothing at its foot. Four faces, so the FRONT and BACK views differ only in their grain
> and their damage, and the two SIDE views likewise — keep the post itself identical in
> all four, and let only the grain and the chips differ.
>
> **BOTTOM ROW — THE BURNT STUMP.** A low broken tree stump, about knee-high, shown in
> IMAGE 1: charred dark grey-brown bark in ragged vertical plates, splayed roots gripping
> out at the base, the trunk snapped off raggedly at the top, and inside the hollow top a
> **small orange ember glow**. **The ember stays** — it is the stump's own light — in every
> view where the hollow is visible. No sun, no dark side, no shadow on the ground.

## T9P-C — the coil of rope and the perched raven

**Sheet:** ONE 1536×1024 **landscape** sheet, 4 columns × 2 rows. **Top row: the coil of
rope**, four views. **Bottom row: the raven**, four views. Each row is one object at one
scale on one ground line.

> **TOP ROW — THE COIL OF ROPE.** A heavy hemp bridge rope coiled flat on the ground and
> left there, shown in IMAGE 1: five or six loops of thick two-strand ochre-tan rope, laid
> in a flattened ring with the hole of the coil open at the centre, the free end tucked
> under the outermost loop. Every strand and its twist drawn with the pen line.
> **These four views are seen from about 25° ABOVE**, the same slight elevation in all
> four, not from dead level — a flat coil seen from dead level is a line, and the model
> needs to see the top of it from every side. Same coil, same loops, same free end, in all
> four. No ground, no shadow, nothing under it or beside it.
>
> **BOTTOM ROW — THE RAVEN.** A single raven standing, shown in IMAGE 1: a big-bodied
> common raven with a heavy curved black beak slightly parted, shaggy throat hackles, a
> long wedge-shaped tail, folded wings, and strong scaled feet. **The bird alone** — no
> post, no branch, no rock, nothing under its feet; IMAGE 1 shows it gripping a post top
> and that post is **not** part of this object.
>
> **The painted bird carries a hot orange rim light along its back, nape and tail. That rim
> is the sun and it goes.** Without it, do not let the raven become a black silhouette:
> paint it as the register card asks — a **dark blue-grey to slate-black** bird at a
> moderate value, with every feather group, every hackle, the wing coverts, the primaries
> and the tail drawn in ink line and hatching, and pale cream catching on the edges of the
> feathers as paper highlight rather than as reflected light. The beak, legs and feet
> darker still. FRONT is the bird facing the viewer head-on, BACK is directly behind it;
> the two profiles show its full length. Head level and forward in all four, the same
> posture in all four.
