# L8 HOLY glyph — candidate composition + coherence read

**Date:** 2026-07-28
**Author:** galadriel (visual-perception seam)
**Status:** CURRENT — evidence for Matt ruling
**Authority:** Matt-authorized parallel thread, L8 holy-glyph closure cell
**Companion:** `agentic_orchestration/gandalf/notes/2026-07-28-l8-glyph-hud-eye/contact_sheet.png` (eye-pass reference)
**Artifacts:** `agentic_orchestration/galadriel/captures/2026-07-28-l8-holy-glyph/`

> **No recommendation ranking in this note.** Matt rules between images. What follows is construction lineage + measured coherence, not preference.

---

## 1. The gap

Five of the six L8 HUD glyphs are ruled from `INTERFACE_Fantasy_Warrior_HUD/Source_Sprites/Sprites/`:

| Slot | Sprite | Path (relative to `Sprites/`) |
|---|---|---|
| freeze | snowflake | `Icons_Status/ICON_FantasyWarrior_Status_Cold01_*.png` |
| physical | sword | `Icons_Status/ICON_FantasyWarrior_Status_Attack01_*.png` |
| consecrate | ritual circle | `FX/SPR_FX_FantasyWarrior_RitualCircle01.png` |
| knockback | bold arrow (rotated) | `Icons_Status/ICON_FantasyWarrior_Status_Down01_*.png` |
| shadow | cursed eye | `Icons_Status/ICON_FantasyWarrior_Status_Cursed02_*.png` |
| air | triple spiral | `Icons_Elements/ICON_FantasyWarrior_Element_Air02_*.png` |

HOLY has no pack glyph. Confirmed by exhaustive filename search across all 16 sprite subdirs for
`*holy* *light* *sun* *divine* *star*`: the only returns are `FX/SPR_FX_FantasyWarrior_Beams01.png`
(a soft vertical light-shaft FX plate — no silhouette, no glyph read), `Icons_Map/ICON_..._Map_Star01_*`
(a plain 5-point map pin star), and `FX/SPR_FX_FantasyWarrior_Sparkle01.png` (a soft 4-point lens flare,
gradient-based, not a flat silhouette). None is a HOLY glyph. The winged `Element_Air01` emblem is
retired/collides. **The gap is real.**

---

## 2. Style contract — measured, not asserted

Measured over the ruled five plus `Fire01` / `Earth02` / `Fortified01` (alpha>128 mask on the `_Clean` layer):

| Sprite | canvas | ink coverage | bbox w×h | stroke half-width (dt p50 / p90) |
|---|---|---|---|---|
| Cold01 (freeze) | 256×256 | 25.2% | 194×222 | 4.5 / 8.1 |
| Attack01 (physical) | 256×256 | 15.1% | 204×203 | 7.1 / 16.3 |
| Down01 (knockback) | 256×256 | 21.4% | 143×184 | 12.8 / 29.1 |
| Cursed02 (shadow) | 256×256 | 24.7% | 212×170 | 5.4 / 14.8 |
| Air02 (air) | 256×256 | 20.9% | 212×207 | 4.0 / 7.1 |
| Fire01 | 256×256 | 27.2% | 218×195 | 6.0 / 13.0 |
| Earth02 | 256×256 | 23.3% | 196×205 | 5.0 / 10.3 |
| Fortified01 | 256×256 | 23.1% | 222×224 | 5.4 / 10.4 |

Derived contract, which all three candidates were built to:

- **Canvas** 256×256 RGBA; fill is pure `(255,255,255)` with shape carried entirely in alpha.
- **Extent** bbox 194–222 px on the long axis (76–87% of canvas); 16–31 px margin.
- **Ink coverage** 15–27% of canvas.
- **Stroke** median half-width 4–7 px (≈ 8–14 px limbs), with chunky masses to 25–30 px half-width.
- **Faceted, not smooth.** Every curve in the pack is a straight-segment polygon. `Cursed02`'s eye outer
  ring is an angular hexagon; `Air02`'s spirals are cut segments; `Fire01` is faceted. Candidate rings are
  drawn as 12–14-gons, never circles.
- **Negative space as separator.** `Cold01`, `Ice01`, `Air02` all use interior gaps to keep the mass legible.
- **Three layers per icon.** `_Clean` (white silhouette, transparent), `_Stroke` (same silhouette + dilated
  dark-grey sticker halo, ≈14 px), `_Underlay` (same silhouette + soft offset drop-shadow, down-right).
  All three generated per candidate. Measured off `Cold01`: Stroke bbox grows 194×222 → 222×252;
  Underlay grows to 206×234, offset ≈ +6,+5.

`RitualCircle01` (consecrate) is deliberately **outside** this contract — 800×800, 12.0% coverage,
stroke half-width 1.4 px. It is fine line-art from the FX layer, not the bold-glyph layer. Noted because it
constrains the HOLY design space: see § 4 collision read.

---

## 3. Candidates

All three are drawn (not photo-composited) at 4× supersample then Lanczos-downsampled to
256×256, which reproduces the pack's anti-aliased vector-export edge. Rings are faceted
polygons — 12-gon and 14-gon — never true circles, because nothing in the pack is a true
circle. Each ships the full three-layer set.

Generator: `agentic_orchestration/galadriel/pipeline/l8-holy-glyph-compose.py`
Scorer: `agentic_orchestration/galadriel/pipeline/l8-holy-glyph-score.py`

### H-A — "Radiant Disc"

`candidates/ICON_Holy_H-A_radiant-disc_{Clean,Stroke,Underlay}.png`
Direction (a) radiant sunburst, executed through direction (b) pack-parts lineage.

**Construction lineage.** A hollow faceted 12-gon ring (r_out 64, r_in 38) with eight
tapered rays at 45° spacing, detached from the ring by a 12 px negative-space gap.
- Ray geometry is taken from the outer burst of `Icons_Status/..._Status_Fortified01`, which
  is the only bold-glyph-weight radiant form the pack contains.
- Ring/ray radial proportion is taken from `FantasyWarrior/SPR_FantasyWarrior_Tracery_Circle04`
  — a thin gold sun-ring from the tracery layer, redrawn here at glyph stroke weight.
- The **detached** rays are the deliberate departure. Fortified01's burst is one connected
  solid star; separating the rays with a gap is Cold01 / Air02 / Ice01 DNA and is what keeps
  H-A from reading as a recolour of Fortified01.

**Measured:** coverage 19.5%, bbox 208×208, stroke half-width p50 5.0 / p90 11.0. All inside contract.

### H-B — "Ascendant Halo"

`candidates/ICON_Holy_H-B_ascendant-halo_{Clean,Stroke,Underlay}.png`
Direction (c) halo mark distinct from the retired Air01 emblem.

**Construction lineage.** A faceted 14-gon lozenge ring (a halo seen near-edge-on, r 66×30
outer / 45×12 inner) above five descending light shafts.
- The ring uses `Cursed02`'s angular-hexagon-ring logic, squashed vertically into perspective.
- The shafts abstract `FX/SPR_FX_FantasyWarrior_Beams01` — the pack's soft light-shaft plate —
  into flat chunky silhouettes. Widths and bottom edges are **uneven and staggered** exactly as
  Beams01's shafts are uneven, which is what keeps the group off a solid flaring cone.
- No wings, no feathers, no plumes: that is the whole point of the separation from `Element_Air01`.
- Shafts flare *downward* rather than rising. Upward-tapering blades were tried first and
  discarded: they collided with `Element_Earth02`'s leaf-blade cluster.

**Measured:** coverage 20.1%, bbox 187×203, stroke half-width p50 5.0 / p90 9.0. All inside contract.

### H-C — "Dawn Rise"

`candidates/ICON_Holy_H-C_dawn-rise_{Clean,Stroke,Underlay}.png`
Direction (b) composed-from-pack-parts, resolved into a sunrise mark.

**Construction lineage.** A solid faceted half-dome (upper half of a 14-gon, r 58) with a
seven-ray fan spreading from the dome centre at 0°, ±28°, ±56°, ±80°, ray reach falling
172 → 158 → 126 → 105 so the fan reads as light climbing off a horizon.
- Dome is `FX/SPR_FX_FantasyWarrior_HalfCircle01` — the pack's arc plate — resolved from a
  soft gradient arc into a flat faceted solid.
- Rays are the same Beams01-derived tapered shafts as H-B, re-aimed radially.
- **Contains no closed ring at all.** That is deliberate: it is the furthest of the three
  from the consecrate ritual-circle.
- Silhouette family is asymmetric-vertical, which is where `Attack01` and `Down01` already live.

**Measured:** coverage 21.6%, bbox 214×214, stroke half-width p50 5.4 / p90 13.0. All inside contract.

### What was deliberately not offered

**No cross / crucifix variant, including a "fantasy-generic" one.** Not a register judgement —
an evidence one. `Icons_Status/ICON_FantasyWarrior_Status_Health02_Clean.png` is already a bold
flat plus/cross in this exact icon family, meaning HEALTH. Any cross-form HOLY glyph would
collide with a pack-native meaning inside the same sprite set, at the same weight, at the same
size. That is a harder collision than any of the ones the brief asked me to avoid. If Matt
wants the cross direction anyway, it should be ruled *against Health02*, not against the L8 six,
and I would want to re-run the collision matrix with Health02 added.

---

## 4. Coherence read — measured

Two independent measures, both run against the six ruled glyphs, plus the **family's own
pairwise spread** as the reference band. The band matters more than the raw numbers: the
question is not "is HOLY distinct in the abstract", it is "is HOLY at least as distinct as the
glyphs Matt has already accepted alongside each other".

**dHash-32 Hamming distance** (992 bits, computed on the *dark-composited 32 px render* —
i.e. what the eye actually gets at HUD size). Lower = more confusable.

| candidate | freeze | physical | consecrate | knockback | shadow | air | **min** |
|---|---|---|---|---|---|---|---|
| H-A radiant-disc | 320 | 319 | 390 | 267 | 297 | 346 | **267** |
| H-B ascendant-halo | 328 | 301 | 420 | 275 | 327 | 358 | **275** |
| H-C dawn-rise | 351 | 326 | 439 | 290 | 334 | 351 | **290** |

**bbox-normalised mask IoU @64** (each alpha mask cropped to its own bbox and rescaled, so this
is pure silhouette overlap, scale-independent). Higher = more confusable.

| candidate | freeze | physical | consecrate | knockback | shadow | air | **max** |
|---|---|---|---|---|---|---|---|
| H-A radiant-disc | 0.234 | 0.186 | 0.087 | 0.387 | **0.480** | 0.255 | **0.480** |
| H-B ascendant-halo | 0.282 | 0.186 | 0.087 | **0.437** | 0.290 | 0.238 | **0.437** |
| H-C dawn-rise | 0.320 | 0.216 | 0.058 | **0.375** | 0.306 | 0.233 | **0.375** |

**The family's own spread**, pairwise among the six already-ruled glyphs:

| | min | median | max |
|---|---|---|---|
| dHash | **252** (physical ↔ knockback) | 347 | 417 |
| IoU | 0.056 | 0.195 | **0.493** (knockback ↔ shadow) |

**Read.** Every candidate's worst case is inside the band the ruled six already occupy. The
tightest structural pair currently shipping is sword-vs-arrow at dHash 252; no candidate gets
closer to anything than 267. The highest silhouette overlap currently shipping is arrow-vs-eye
at IoU 0.493; no candidate exceeds 0.480. **On the collision question, all three clear.**

The ordering within that band is consistent across both measures, and it runs the same way each
time: H-C is the most separated, H-B next, H-A the tightest. H-A's specific pressure point is
`shadow` (IoU 0.480) — the cursed eye and the radiant disc are both compact centred ring-in-mass
forms, and at 32 px they occupy nearly the same footprint. They are not confusable in *meaning*
(one is an eye, one is a sun) but they are the closest silhouette pair the set would contain.
H-B's and H-C's pressure point is `knockback` — all three are vertically-organised masses.

**Consecrate is not a collision risk for any candidate**, which was the a-priori worry given the
"circle-alone = consecrate" guard. dHash 390 / 420 / 439 are the three *largest* distances in the
whole matrix, and IoU 0.087 / 0.087 / 0.058 the three smallest. The reason is structural, not
lucky: `RitualCircle01` is 800 px of 1.4 px-half-width line-art at 12% coverage. It is a different
*drawing weight*, not just a different shape, so a bold ring cannot converge on it.

### Legibility at HUD size

Component-count survival across the ladder (256 / 64 / 48 / 32 / 24 px) is stable for all three —
no candidate loses a part. But part-count is the wrong question; the right one is whether the
*gaps* survive. Measuring the "mush" fraction (share of visible pixels landing in the ambiguous
alpha band 64–192, i.e. neither solid ink nor solid ground):

| glyph | @48 | @32 | @24 |
|---|---|---|---|
| H-A radiant-disc | 26.6 | **36.0** | **47.4** |
| H-B ascendant-halo | 27.8 | **38.0** | **44.1** |
| H-C dawn-rise | 24.3 | 30.1 | 35.4 |
| *air* (ruled, mushiest) | 29.0 | 33.2 | 40.0 |
| *freeze* (ruled) | 27.7 | 29.4 | 31.2 |
| *shadow* (ruled) | 21.3 | 29.0 | 33.5 |
| *physical* (ruled) | 18.6 | 19.6 | 20.5 |
| *knockback* (ruled) | 9.0 | 17.4 | 21.2 |

At 48 px all three sit inside the ruled band (9.0–29.0). At 32 px — the stated target — **H-C is
inside the band (30.1 vs air's 33.2 ceiling); H-A at 36.0 and H-B at 38.0 are above it.** At 24 px
H-A and H-B are above the ruled ceiling by 7.4 and 4.1 points respectively. The eye agrees with the
number: on the size-ladder strips, H-B's shafts begin to smear together at 24 px and H-A's ray tips
thin out. Nothing here is a *failure* — the ruled `air` glyph is itself only 3 points crisper than
H-A at 32 px — but if the HUD ever renders these below 32 px, H-A and H-B are the two that will
soften first. That is a fact about them, not a verdict on them.

---

## 5. Artifacts

| what | path |
|---|---|
| Contact sheet (ruled six + 3 candidates + 32 px strip, dark-composited) | `agentic_orchestration/galadriel/captures/2026-07-28-l8-holy-glyph/contact_sheet.png` |
| H-A three-layer card + size ladder | `.../2026-07-28-l8-holy-glyph/layers_H-A_radiant-disc.png` |
| H-B three-layer card + size ladder | `.../2026-07-28-l8-holy-glyph/layers_H-B_ascendant-halo.png` |
| H-C three-layer card + size ladder | `.../2026-07-28-l8-holy-glyph/layers_H-C_dawn-rise.png` |
| Ship-ready PNGs (9 files: 3 candidates × Clean/Stroke/Underlay, 256×256 RGBA) | `.../2026-07-28-l8-holy-glyph/candidates/` |
| Donor-parts study sheet (what the pack actually contains) | `.../2026-07-28-l8-holy-glyph/work/study_parts.png` |
| Pack three-layer reference (Cold01) | `.../2026-07-28-l8-holy-glyph/work/layers_cold01.png` |
| Generator (reproducible; all geometry is code) | `agentic_orchestration/galadriel/pipeline/l8-holy-glyph-compose.py` |
| Scorer (reproduces every number in § 4) | `agentic_orchestration/galadriel/pipeline/l8-holy-glyph-score.py` |

Both scripts are deterministic and take no arguments. Re-running them reproduces the candidates
and the matrices exactly.

---

## 6. Mirror

The pack has a sword for the blow, an eye for the curse, a spiral for the wind, a flake for the
cold, and a whole mandala for the consecration. It has no light. Twenty-two FX plates, and the
nearest thing to holiness in the whole set is a soft grey shaft with no edge to it — a glow
someone drew to sit *behind* a thing, never to be the thing.

That absence is not an oversight in the pack. It is the shape of what the pack was for. And it
means the HOLY glyph is the first mark in this HUD that the project has to say in its own voice
rather than borrow. Three ways to say it are laid out on the sheet, all three built from parts
the pack already owns, all three measurably inside the family they must join.

Which of them is holy is not a thing the Mirror can measure. That one is Matt's.

