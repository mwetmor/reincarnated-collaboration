# Chierit Character Scale Inspection Strip (Corrected) — Companion Notes

**Dispatch:** `2026-05-16-drax-corrected-chierit-composite-v0-20-4`
**Tag:** `drax/v0.20.4-corrected-chierit-composite`
**Generated:** 2026-05-16
**Composite:** `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-corrected.png`

**Cross-references:**
- v0.20.3 (obsolete scale candidates, still useful gap visualization): `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip.png`
- v0.20.2 (monster composite): `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip.png`

---

## Scale-revision rationale

### Why the original v0.20.3 scales (0.25 / 0.35 / 0.45) were wrong

v0.20.3 was built to bracket the current default game scale of 0.35. legolas pixel-scale research (Section 4 of `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md`) identified that at scale 0.35, chierit characters render at approximately 31px — far below the 80-100px HD-2D register target. legolas recommended a scale of approximately 0.91-1.14 as the required correction.

However, legolas's estimate of 31px at 0.35 assumed the full 128px canvas height as the figure content. v0.20.3's empirical measurements showed the actual situation: chierit sprites use a 288x128 canvas per frame, but the character figure occupies only a **sub-region of that canvas** — 34-57px content height concentrated near the bottom of the frame. The remaining canvas area is transparent padding.

This means:
- legolas's estimate: 128px canvas x 0.35 = ~45px rendered (close to actual 45px canvas height, but conflating canvas with figure)
- v0.20.3 measured figure content: 34-57px intrinsic (not 128px) → at 0.35, figure renders at 12-20px actual height
- The HD-2D gap is not 3x (legolas) but closer to 4-8x from the current 0.35 scale

### Why 1.5 / 2.0 / 2.5 were chosen

v0.20.3's per-character content measurements established the precise HD-2D target scale for each character:

| Character | Content_h | Scale for 80px | Scale for 100px |
|---|---|---|---|
| Shadow Stalker | 57 px | 1.40x | 1.75x |
| Light Valkyrie | 53 px | 1.51x | 1.89x |
| Leaf Ranger | 44 px | 1.82x | 2.27x |
| Fire Knight | 44 px | 1.82x | 2.27x |
| Lightning Ronin | 43 px | 1.86x | 2.33x |
| Metal Bladekeeper | 42 px | 1.90x | 2.38x |
| Crystal Mauler | 39 px | 2.05x | 2.56x |
| Water Priestess | 37 px | 2.16x | 2.70x |
| Wind Hashashin | 37 px | 2.16x | 2.70x |
| Ground Monk | 34 px | 2.35x | 2.94x |

The 1.5 / 2.0 / 2.5 bracket was selected to span this variance:
- **1.5x** = lower bracket: catches Shadow Stalker and Light Valkyrie at or near the band floor
- **2.0x** = middle: catches the majority cluster (Metal Bladekeeper, Fire Knight, Lightning Ronin, Leaf Ranger) squarely in band
- **2.5x** = upper bracket: catches Ground Monk, Water Priestess, Wind Hashashin, Crystal Mauler in band

---

## Chierit intrinsic source-sheet dimensions — confirmed (carry-forward from v0.20.3)

All 10 chierit characters use a **uniform 288 x 128 px canvas per frame** (horizontal strip layout; frame 0 at x=0, y=0). No deviation across the set. Character figures are ground-anchored near row 127 of the 128px canvas height.

---

## Per-character HD-2D band results at corrected scales

| Character | Content_h | @ 1.5x figure | @ 2.0x figure | @ 2.5x figure | Band hit |
|---|---|---|---|---|---|
| Metal Bladekeeper | 42 px | 63 px | **84 px (IN BAND)** | 105 px | 2.0x |
| Fire Knight | 44 px | 66 px | **88 px (IN BAND)** | 110 px | 2.0x |
| Water Priestess | 37 px | 56 px | 74 px | **92 px (IN BAND)** | 2.5x |
| Ground Monk | 34 px | 51 px | 68 px | **85 px (IN BAND)** | 2.5x |
| Wind Hashashin | 37 px | 56 px | 74 px | **92 px (IN BAND)** | 2.5x |
| Crystal Mauler | 39 px | 58 px | 78 px | **98 px (IN BAND)** | 2.5x |
| Light Valkyrie | 53 px | **80 px (IN BAND)** | 106 px | 132 px | 1.5x |
| Shadow Stalker | 57 px | **86 px (IN BAND)** | 114 px | 142 px | 1.5x |
| Lightning Ronin | 43 px | 64 px | **86 px (IN BAND)** | 108 px | 2.0x |
| Leaf Ranger | 44 px | 66 px | **88 px (IN BAND)** | 110 px | 2.0x |

**Key finding:** No single uniform scale hits the HD-2D band for all characters simultaneously. The character set naturally separates into three groups:
- **Group A (scale 1.5x hits band):** Shadow Stalker, Light Valkyrie
- **Group B (scale 2.0x hits band):** Metal Bladekeeper, Fire Knight, Lightning Ronin, Leaf Ranger (4 of 10 characters; the central cluster)
- **Group C (scale 2.5x hits band):** Water Priestess, Ground Monk, Wind Hashashin, Crystal Mauler

This finding strongly suggests a per-character scale lookup is needed rather than a single uniform scale. A uniform scale of 2.0x lands 6 of 10 characters near or in band, but Group A characters overshoot (114-106px) and Group C characters undershoot (68-78px).

---

## Viewport implications at these scales

At these scales, the full 288px canvas width renders substantially larger than the current game viewport is designed for. These are load-bearing concerns for any scale decision:

| Scale | Full canvas size (288x128) | Figure width (approx, at content_w ~24-60px) |
|---|---|---|
| 1.5x | 432 x 192 px | 36-90 px figure width |
| 2.0x | 576 x 256 px | 48-120 px figure width |
| 2.5x | 720 x 320 px | 60-150 px figure width |

All cells in this composite apply **horizontal clipping** to the rendered canvas (cells are 280px wide; full-frame canvases at 1.5-2.5x are 432-720px wide). The clipping is symmetric and does not affect the figure content, which is concentrated in the center-right of the frame. The figure renders cleanly within the cell; only the transparent padding regions are clipped.

**Combat-view layout impact:** At 2.5x, a single chierit character's canvas is 720px wide. A typical 800px combat viewport would leave only 80px of horizontal margin if one character is displayed at this scale. Side-by-side player + enemy at 2.5x would require approximately 1440px horizontal canvas — not viable at typical viewport sizes without a camera or layout rethink. At 2.0x the situation improves (576px per canvas) but is still substantial.

**Recommended design path** (for gandalf to evaluate): per-character scale lookup with tighter bounding-box-anchored rendering (render the content bbox region only, not the full 288x128 frame) would allow higher effective scale while keeping the rendered footprint manageable in the viewport.

---

## Rendering anomalies at corrected scales

### 1. Horizontal canvas clipping (all characters, all scales)

At 1.5x the full canvas is 432px wide — already wider than the 280px cell. At 2.0x it is 576px; at 2.5x it is 720px. All composite cells clip the canvas horizontally. This is labeled in each cell as `(h-clipped)` with the full canvas_w noted. The figure content (24-60px intrinsic width) renders entirely within the 280px cell at all scales — only transparent padding is clipped. This is faithful to what would happen in a game viewport that is narrower than the full canvas.

### 2. Pixelation at 2.0x and 2.5x

Rendering uses nearest-neighbor scaling (pixel art mode) to match game rendering. At 2.0x pixels are visually doubled; at 2.5x they become 2-3px blocks. This is expected behavior for nearest-neighbor pixel art scaling and is not a rendering bug. The pixelation is particularly visible on thin details (Shadow Stalker's cape edges, Light Valkyrie's wing tips). Documented per dispatch requirement.

### 3. Ground Monk idle anchor offset (carry-forward from v0.20.3)

Ground Monk's content bottom lands at row 121 (not 127) of the 128px frame — a 6px gap to the frame bottom. At 2.5x this becomes a 15px visible float above the ground line. The ground anchor in the composite is based on the frame bottom, not the content bottom. Ground Monk appears to hover slightly above the ground. This was documented in v0.20.3 and is more visually obvious at the corrected scales.

### 4. Shadow Stalker and Light Valkyrie: above band at 2.0x and 2.5x

Both characters are at or in the band at 1.5x, then exceed the 100px upper ceiling at higher scales:
- Shadow Stalker: 86px (in band) at 1.5x → 114px (above) at 2.0x → 142px (above) at 2.5x
- Light Valkyrie: 80px (just at floor) at 1.5x → 106px (above) at 2.0x → 132px (above) at 2.5x

This confirms Group A characters need 1.5x or close to it, not higher.

### 5. Samurai portrait: not comparable

The GandalfHardcore Samurai portrait (640x640) renders at 960px, 1280px, and 1600px at 1.5x, 2.0x, 2.5x respectively. All three cells show only a clipped portrait fragment. The band comparison is not applicable to portrait images. Samurai handling is option (a) carry-forward from v0.20.3: included and labeled `"portrait only -- no anim sheets (see P6.d sub-commission)"`.

---

## Samurai handling — option (a) carry-forward from v0.20.3

v0.20.3 chose option (a): include Samurai as portrait rather than omit. That decision carries forward unchanged to v0.20.4. The portrait-at-scale comparison is visually present but labeled clearly. When animation sheets are sourced via P6.d, the same content-bbox analysis applied to the 10 chierit characters should be applied to the Samurai animation frames.

---

## Files produced

- `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-corrected.png` — 233.3 KB; 1013 x 5074 px; within 2MB limit
- `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-corrected-notes.md` — this file
- `reincarnated-demo/scripts/generate-chierit-composite-strip-corrected.py` — generator script (Python/PIL, same harness as v0.20.2/v0.20.3)
