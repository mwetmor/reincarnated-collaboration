## 2. Register card (FROZEN for the run; extracted verbatim into `astra_test_01/burst/REGISTER_CARD.md` by T0)

```
REGISTER CARD — Run C-1 — v1.0 — do not reinterpret; every line is a constraint
STYLE: painted 2D, illustrated, high-res. Not pixel art. Not cel-shaded. F04 CLARITY: clean
  material planes, restrained surface texture, readable small silhouettes, no conspicuous
  brush/pixel grain (Matt: "F01 and F02 seem to show too many brush strokes or pixels").
  Environmental richness and local light-spill on floors/walls in the F03 manner.
  Anchors: E07V/art/F04.png (figures + observatory), E07V/art/F03.png (light/detail),
  run_03/evidence/vfx_style_match.png (painted VFX edge language).
LIGHT: single key from SCREEN UPPER-LEFT, fixed for every frame of every direction; the light
  never rotates with the character. Deep cool low-value ambient; readable shadows, never pure
  black. Slight rim on the key-facing silhouette edge. Spell light is the ONLY warm/saturated
  source and appears only on cast frames. NO floor shadows in sprite frames.
CAMERA: projection C (Godot-informed elevated three-quarter; constants in
  astra_test_01/design/experiments/E01/projection-candidates.json → "C"). All 8 directions are
  the same camera with the CHARACTER rotated. Directions in this order: S SW W NW N NE E SE.
  NO MIRRORING. Weapon stays in the same anatomical hand in every direction.
CANVAS: every delivered frame 512×512, feet pivot at (256,400), S-idle standing height ≈ 240 px.
  Generation happens on 2×2 sheets (1254² native → 627-px cells); frames are registered
  by uniform downscale + translation only (no per-frame scale, no upscaling — ever).
PLATE: all generated art on flat pure #00ff00; matting is done by frozen tools, never in-prompt.
FACTION F04 — Keepers of Hours: ceremonial armor, arcane instruments, deliberate ornamental
  geometry; monumental stonework, fractured observatories. Blue / ivory / brass. No source-game
  names, no copied characters.
FORBIDDEN in prompts: "Diablo", "Last Epoch", any studio/franchise/character name; "pixel art";
  "3D render"; "cel shaded".
```

**Two pre-registered instrument refinements (no bar lowered; both reported):**
- **G2** reports two quantities: the *root anchor* (atlas pivot, ±4 px literal gate) and the *planted-sole contact* trajectory (run_02's own recommendation). The literal gate stays literal.
- **G6b** is registered beside the literal G6: seam MAD ≤ *median* internal adjacent-pair MAD. **G6 (literal) remains the recorded brief gate; G6b is a second instrument.** Whether G6b becomes the shipping bar is **Matt's ruling at the first-loop milestone** — not the conductor's, and never a rescue of a failing candidate.

