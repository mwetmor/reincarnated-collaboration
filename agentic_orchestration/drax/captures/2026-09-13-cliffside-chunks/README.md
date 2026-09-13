# Cliffside proof: chunk guides, first portion (drax, 2026-09-13)

These are guides for painting the first portion of the cliffside scene under R-C3-44: checkpoint 1 was accepted at the 12.5 % rung (k 0.541386), the vista will be a painted backdrop, and this is the proof step. No painting and no generated images were made. Every file is a crop of the Godot v2 orthographic canvas.

**Sources**
- Scene script: `reincarnated-godot/scripts/cliffside_blockout.gd --v2`
- Chunk script: `scripts/cliffside_chunks.py`
- v2 canvas, meta and follow still: `../2026-09-13-cliffside-blockout/` (`07_ortho_canvas_shaded_v2.png`, `08_ortho_canvas_layer_id_v2.png`, `work/ortho_canvas_v2_fgmask_cut7m.png`, `blockout_meta_v2.json`, `02_follow_plateau_v2_k12p5.png`). The v1 files are untouched.

## What changed in v2 (the re-route)
- **Plateau.** The vista plateau is now a promontory that juts *toward the camera*. Its axis runs almost straight down the screen, its tip rim is near-horizontal on screen, and its 40 m cliff face looks straight at the camera, so the face shows below the rim.
- **Bay.** The near-side landmass is cut back to a 1.2 m rim over s = 6.9–29.9 m, so there is empty space in front of the promontory.
- **Path.** The far-side bulge from v1 is removed. The path still runs onto the plateau, and its back corners sit on the path centreline at s = 20.9 ± 7 m, then continue to the bridge.
- **Rocks.** Rocks that would have been in the bay are dropped.
- **Unchanged.** Camera, k, the 100.6176 px/m ortho scale, the bridge and the background bands.

## Files

| File | What it is |
|---|---|
| `chunk_A_guide.png`, `chunk_B_guide.png` | 1536×1024 crops of the shaded ortho greybox. Every non-foreground pixel is pure **#00ff00**: beyond the cliff edge, cliff face deeper than 7 m below the rim, or off the level |
| `chunk_A_mask.png`, `chunk_B_mask.png` | 8-bit mask: 255 foreground, 0 beyond. It comes from a Godot pass that drops any fragment below −7 m, with anti-aliasing off, so it follows the geometry exactly rather than a colour key |
| `chunk_A_id.png`, `chunk_B_id.png` | Same crop of the flat layer-ID canvas (RGBA, alpha 0 off the level) |
| `shadow_ellipse.png` | Contact shadow: 58×47 px canvas, black, alpha 0.45 at the centre fading smoothly to 0 at the rim |
| `chunks.json` | All numbers below, plus key points in canvas px |

## Numbers
- **Chunk origins (canvas px):** A = (700, 2250), B = (1980, 2250). Each is 1536×1024. They sit side by side with a 256 px overlap: B's left 256 px are the same canvas pixels as A's right 256 px, and I verified the overlap is pixel-identical in the guides.
- **What each chunk holds:** A has the path coming in from lower-left (s ≈ 4–17 m), the bay-start rim and the left of the plateau. B has the plateau, the tip rim, the 7 m band of rock face, the right flank and the bay.
- **Cliff-face cut depth:** **7.0 m below the rim**, which is 424 px of visible rock face at this camera.
- **Scale:** 100.6176 px per metre along screen-x; 80.3076 px per ground metre along screen-y; 60.6183 px per vertical metre.
- **Keeper spawn (on the plateau, 5 m out along the promontory axis):** canvas (2286.0, 2407.4).
  - In chunk **B:** (306.0, 157.4).
  - In chunk A it would be (1586.0, 157.4), which is outside A.
- **A 1.75 m figure = 130.0 px in this ortho.** This is the measured outline of the 1.75 m capsule, the same measure that set the 12.5 % rung at 135 px in perspective. For reference, a bare vertical 1.75 m line is 106.1 px. Put the sprite's feet (bottom-centre of its alpha ≥ 128 box) on the contact point.
- **Contact shadow ellipse:** **55.34 × 44.17 px**. That is a 0.55 m disc on the ground (0.55 × 100.6176 wide, 0.55 × 80.3076 tall), centred on the feet.

## Notes
- **Cliff face shading:** the camera-facing cliff faces are all one flat dark grey, because the light comes from screen upper-left. The ID crop marks the promontory tip face, the bay walls and the bay-start cut wall all as `cliff_rock`. Nothing in the geometry separates "promontory face" from "bay wall".
- **Edge line in A:** a one-pixel light line runs along the bay-start rim edge in A, where the lip meets the wall. It is a shading artefact, not geometry; the mask has no such line.
