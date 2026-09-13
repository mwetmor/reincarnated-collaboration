## 2. Register card (FROZEN for the run; extracted verbatim into `astra_test_01/burst/REGISTER_CARD.md` by T0)

```
REGISTER CARD — Run C-1 — v1.1 (H1 re-freeze, C-2 step 3; R-23 / R-29) — do not reinterpret; every line is a constraint
STYLE (H1 — ruled R-23; supersedes v1.0 STYLE in pixels, never in identity text): HAND-DRAWN painted 2D
  in the manner of a modern hand-animated action game — a confident dark contour line drawn by hand
  with visible taper and varying weight, painted fills in clean planes inside the line, restrained
  texture; the line carries the pose. Every frame should look like one frame of hand-drawn animation,
  not a rendered illustration. Not pixel art. Not cel-shaded. F04 CLARITY keepers: clean material
  planes, restrained surface texture, readable small silhouettes, no conspicuous brush/pixel grain.
  Environmental richness and local light-spill on floors/walls in the F03 manner.
  Exhibits of the ruled register (EVIDENCE, never generation references — the register is text-carried):
  runs/C-1/artifacts/K4-gen-H1/k4_H1_{1,2}.png (figure), K6-male-H1/k6_male_H1_{1,2}.png (in-world),
  K7-H1-foundry/k7_H1_foundry.png + K7-H1-aery/k7_H1_aery.png (rooms, dialect). VFX edge language:
  run_03/evidence/vfx_style_match.png.
SCREEN (R-23): the default screen is the ARPG-language world — elevated ~45° camera, cold key, warm
  accents only — in the classic isometric-ARPG band. Hades-language framing (steep ~60° arena, bold
  ground pattern, jewel-toned light) is a LEVEL DIALECT inside H1, never the default. On-screen
  character height 17 % of 1080p (corpus centre). SCALE is a post-process, never a prompt instruction.
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

