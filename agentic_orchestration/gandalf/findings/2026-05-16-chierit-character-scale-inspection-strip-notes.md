# Chierit Character Scale Inspection Strip — Companion Notes

**Dispatch:** `2026-05-16-drax-chierit-composite-scale-inspection-strip`
**Tag:** `drax/v0.20.3-gandalf-chierit-composite-scale-strip`
**Generated:** 2026-05-16
**Composite:** `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip.png`
**Cross-reference:** `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip.png`

---

## Chierit intrinsic source-sheet dimensions — confirmed

All 10 chierit characters use a **uniform 288 x 128 px canvas per frame**. This is empirically confirmed by reading each character's `metadata.json` and extracting the first idle frame. No deviation across the set.

Key architectural note: chierit sheets are **horizontal strips** (not grids). Frame 0 sits at `x=0, y=0, width=288, height=128`.

---

## The HD-2D target band gap — primary finding

This is the load-bearing finding of this composite. The HD-2D register (Sea of Stars / Octopath Traveler / Eiyuden Chronicle) targets **80-100 px rendered figure height**. Chierit sprites use a 288 x 128 canvas, but the **character figure occupies only a sub-region of that canvas** — mostly concentrated in the lower-right quadrant with significant transparent padding surrounding the figure.

### Content bounding box measurements (idle first frame, opaque pixels only)

| Character | Intrinsic canvas | Figure content_h | Figure content_w | Figure y-range (of 128px) |
|---|---|---|---|---|
| Metal Bladekeeper | 288 x 128 | 42 px | 45 px | rows 85-127 |
| Fire Knight | 288 x 128 | 44 px | 60 px | rows 83-127 |
| Water Priestess | 288 x 128 | 37 px | 28 px | rows 90-127 |
| Ground Monk | 288 x 128 | 34 px | 24 px | rows 87-121 |
| Wind Hashashin | 288 x 128 | 37 px | 34 px | rows 90-127 |
| Crystal Mauler | 288 x 128 | 39 px | 43 px | rows 88-127 |
| Light Valkyrie | 288 x 128 | 53 px | 51 px | rows 74-127 |
| Shadow Stalker | 288 x 128 | 57 px | 60 px | rows 70-127 |
| Lightning Ronin | 288 x 128 | 43 px | 36 px | rows 84-127 |
| Leaf Ranger | 288 x 128 | 44 px | 49 px | rows 83-127 |

The character figure is always ground-anchored at or near row 127 (the bottom of the canvas). The top of the figure varies by character height.

### Current scale (0.35) rendered figure heights

At the current game scale `0.35`, chierit characters render at these figure heights:

- Metal Bladekeeper: **15 px** (33% below HD-2D 80px floor)
- Fire Knight: **15 px**
- Water Priestess: **13 px**
- Ground Monk: **12 px** (smallest figure — most hunched pose)
- Wind Hashashin: **13 px**
- Crystal Mauler: **14 px**
- Light Valkyrie: **19 px** (tallest at 0.35, due to armor/wings raising content top)
- Shadow Stalker: **20 px** (tallest at 0.35, due to cape/silhouette extending higher)
- Lightning Ronin: **15 px**
- Leaf Ranger: **15 px**

**None of the three scale candidates (0.25 / 0.35 / 0.45) bring any chierit character into the 80-100 px HD-2D target band.**

### Scale required to hit the HD-2D target band

The required scale to render chierit figures at 80-100 px content height:

| Character | Content_h | Scale for 80px | Scale for 100px | Band midpoint |
|---|---|---|---|---|
| Shadow Stalker | 57 px | 1.40x | 1.75x | 1.58x |
| Light Valkyrie | 53 px | 1.51x | 1.89x | 1.70x |
| Leaf Ranger | 44 px | 1.82x | 2.27x | 2.05x |
| Fire Knight | 44 px | 1.82x | 2.27x | 2.05x |
| Lightning Ronin | 43 px | 1.86x | 2.33x | 2.09x |
| Metal Bladekeeper | 42 px | 1.90x | 2.38x | 2.14x |
| Crystal Mauler | 39 px | 2.05x | 2.56x | 2.31x |
| Water Priestess | 37 px | 2.16x | 2.70x | 2.43x |
| Wind Hashashin | 37 px | 2.16x | 2.70x | 2.43x |
| Ground Monk | 34 px | 2.35x | 2.94x | 2.65x |

At the 0.35 current scale, the full 128px canvas height renders at 45px — the figure inside is only 12-20px. To reach the HD-2D band, the scale needs to increase approximately **4-8x from current** (0.35 → ~1.5-2.9x).

**Implication for the game viewport:** The full 288x128 canvas at scale 2.0 renders at 576x256 px, which would dominate a typical 800-600 game viewport. The HD-2D register may require either (a) a higher-resolution viewport design, (b) accepting smaller chierit figures and tuning the HD-2D target downward for the Reincarnated register, or (c) sourcing chierit exports with tighter content bounds and less canvas padding. This decision is out of scope for this composite (per dispatch); flagged for gandalf's recommendation.

---

## Composite rendering notes

### All 10 chierit characters: uniform behavior

All 10 characters behave identically in the scale comparison: 288x128 full frame, figure in lower portion of canvas, ground anchor at frame bottom (row 127). The composite shows a **yellow horizontal line** at the actual figure top for each cell. The green HD-2D band (80-100px zone) is drawn above the ground anchor. The gap between the yellow figure-top line and the lower green guideline (80px mark) visualizes how far below the target each character renders.

### Ground-anchor alignment across characters

The figure bottom is at or near row 127 of 128 for most characters. Ground Monk's content tops out at row 121 (7px gap to frame bottom) — this means ground-monk has a slight float relative to other characters in the composite. The visual difference is minor at these scales.

### Shadow Stalker and Light Valkyrie — tallest figures

Shadow Stalker (57px content_h) and Light Valkyrie (53px content_h) are the tallest chierit figures in idle pose, primarily due to silhouette elements extending higher (Shadow Stalker's hood/cape, Light Valkyrie's armor wings). They need the smallest scale increase to reach the HD-2D band (~1.4-1.9x vs ~2.0-2.9x for shorter characters).

### Ground Monk — smallest figure

Ground Monk (34px content_h) is the smallest chierit figure. Seated/meditative idle pose compresses the figure. This character will require the highest scale increase (~2.4-2.9x) to reach the HD-2D band. Also note: Ground Monk's content bottom is at row 121, not 127 — it floats 6px above the frame bottom, meaning ground alignment in the composite is slightly inaccurate for this character (figure appears to hover). Minor at small scales; becomes visible at higher scales.

---

## Samurai handling — option (a) chosen

**Decision: Option (a) — include Samurai as portrait.**

Rationale: the portrait-at-scale comparison is ergonomically useful to gandalf even though Samurai has no animation sheets. It answers "how would the Samurai portrait look at these scales?" and surfaces the 640x640 portrait-to-game-sprite size discrepancy visually. Omission (option b) loses this information; option (a) costs nothing (one extra row, labeled clearly).

Samurai portrait file used: `Samurai 640x640 Portrait1.png` (640x640 RGBA, confirmed).

Rendered portrait heights at each scale:
- `@ 0.25` → 160 px (above HD-2D target; portrait fills cell)
- `@ 0.35` → 224 px (clipped at top by cell boundary)
- `@ 0.45` → 288 px (clipped substantially)

The Samurai portrait at 0.25 scale (160px) lands significantly above the HD-2D target band (80-100px). However, a portrait is not an animation sprite — its canvas proportions differ entirely from chierit's 288x128 game-character format. Labeled prominently in composite: `"portrait only — no anim sheets — see P6.d sub-commission"`. When animation sheets are sourced (P6.d), the character figure within those sheets will need the same content-bbox analysis applied here.

---

## Rendering anomalies

1. **Ground Monk idle anchor offset**: Ground Monk's idle content bottom lands at row 121 (not 127). This means the ground-monk figure floats ~6px above the physical ground anchor in the composite. At 0.35 scale this is ~2px visual gap — barely noticeable. At higher scales (1.5-2.5x) this would become an obvious float and would require anchor adjustment or content-bbox-anchored rendering.

2. **Samurai portrait overwrites HD-2D band at 0.35 and 0.45**: The 640x640 portrait scaled to 224px and 288px exceeds the cell's 250px sprite area height. The sprite is clipped at the cell top. The HD-2D band guidelines are drawn on top of the sprite (green lines visible over the portrait). This is intentional — the band is the primary visual reference.

3. **Frame canvas dominates over figure**: At scales 0.25/0.35/0.45, what you see in the composite cells is the full 288x128 canvas scaled — but the character figure is a small pixel cluster at the bottom of that canvas. The yellow figure-top line shows where the character actually ends. This is faithful to how the game renders sprites (full canvas is the rendering unit, not just the content bbox). The visual impression correctly shows that chierit figures are very small at these scales.

---

## Cross-reference to monster composite

Monster composite: `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip.png`

In the monster composite, the **chierit Fire Knight at 0.35 was used as the player reference** column. That composite confirmed Fire Knight renders at **45px full-frame height** at scale 0.35. From this character composite, we now know the Fire Knight figure inside that 45px frame is only **15px tall** (content bounding box: 44px intrinsic, scaled by 0.35).

For gandalf's scale recommendations: monster sizes in the monster composite should be evaluated against figure height (15px for the player character at 0.35), not the 45px full-frame height. Monsters were shown at scales 0.20/0.28/0.35 — those are full-frame renderings as well. The monster metadata uses the full frame dimensions (e.g., Evil Eye 64x64, Sword Warrior 280x280), and for monsters the figure typically fills more of the frame than chierit characters do (less transparent padding). A content-bbox pass on the monster set would give a clearer comparison, but that was not in scope for this dispatch.

---

## Files produced

- `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip.png` — 158.5 KB; 833 x 3744 px; within 2MB limit
- `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-notes.md` — this file
- `reincarnated-demo/scripts/generate-chierit-composite-strip.py` — generator script (Python/PIL, same approach as v0.20.2 monster composite)
