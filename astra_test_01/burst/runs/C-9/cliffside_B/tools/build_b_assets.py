#!/usr/bin/env python3
"""C-9: build the Illuminated-register ("B") texture set for the cliffside A/B build.

Reads the painted B art from runs/C-9/artifacts/ (READ-ONLY, conductor-owned) and
writes Godot-ready PNGs into this project's parallax/tiles_b/ and parallax/layers_b/,
plus parallax/layers_b/offsets.json.

  plate   CS9-band/foreground.png        5376x4096 RGBA, STRAIGHT ALPHA, already
          matted (ground + rock + the ported sunset cloud band under the cliffs).
          NO green key -- it arrives with its own alpha.  Split on the H1 tile grid:
             tiles_b/tile_0_0.png    (0,0,4096,4096)
             tiles_b/tile_4096_0.png (4096,0,1280,4096)
  sky     CS9-assembly/L10_layer_sky_single.png   opaque, no key
  far     CS9-assembly/L10_layer_far_fixed.png    #00ff00 above the horizon -> key
  forest  CS9-assembly/FG10 panels (3x3, assembled here) or L10_layer_forest.png
                                                  #00ff00 above the treeline -> key
  mist    CS9-assembly/L10_layer_mist.png         light on black -> alpha=luminance,
                                                  capped at the H1 mist's own 220/255

ASPECT, NOT STRETCH.  The previous build resized every B layer to the H1 layer's exact
pixel size, which stretched sky and forest ~1.6x vertically because the painted art has
a different aspect from the H1 art.  This build scales each layer to the H1 layer's
WIDTH ONLY and keeps its aspect, then compensates with a per-style VERTICAL OFFSET so
the B layer's horizon lands on the same screen row the H1 layer's horizon did.  The
offset is written to offsets.json and applied by scripts/style_toggle.gd to the layer
Sprite2D's own position (A = 0, B = offsets.json), so the Parallax2D scroll maths,
camera, walkable.json and collision are untouched and the swap is reversible.

HORIZON.  For a layer with a keyed sky above it (far, forest) and for the mist, the
horizon is the first row whose opaque coverage (alpha > 128) crosses 50% -- the ridge
line, the treeline, the top of the mist bank.  The sky layer is opaque everywhere and
has no such row in either register, so it is BOTTOM-ALIGNED instead: the sky's bottom
edge is where the land begins, and both registers' skies are full-bleed sunsets.  Both
B sky and B far/forest/mist end up a superset or a near-superset of the H1 span in the
direction that matters, and the plate (z=0) covers anything short at the bottom.

Green key: greenness d = G - max(R,B); ramp opaque at d<=0.08, transparent at d>=0.25,
which sits in the empty gap of the measured bimodal distribution and keeps the painted
antialiased fringe as partial alpha rather than a hard cut.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

PROJ = Path(__file__).resolve().parent.parent
ART = PROJ.parent / "artifacts"
SRC = ART / "CS9-assembly"
BAND = ART / "CS9-band"
A_LAYERS = PROJ / "parallax" / "layers"
OUT_TILES = PROJ / "parallax" / "tiles_b"
OUT_LAYERS = PROJ / "parallax" / "layers_b"

KEY_LO, KEY_HI = 0.08, 0.25
DESPILL_AT = 0.02
MIST_ALPHA_CAP = 220 / 255.0

# FG10 forest: 3x3 grid of 1536x1024 panels at step 1280x768 over 4096x2560
FG10_GRID = (3, 3)
FG10_PANEL = (1536, 1024)
FG10_STEP = (1280, 768)
FG10_CANVAS = (4096, 2560)


def load_rgb(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(np.float32) / 255.0


def green_key(rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    d = g - np.maximum(r, b)
    alpha = np.clip((KEY_HI - d) / (KEY_HI - KEY_LO), 0.0, 1.0)
    out = rgb.copy()
    spill = d > DESPILL_AT
    out[..., 1] = np.where(spill, np.maximum(r, b) + np.minimum(d, DESPILL_AT), g)
    rgba = np.dstack([out, alpha])
    rgba[alpha <= 0.0, :3] = 0.0
    return rgba


def to_img(rgba):
    return Image.fromarray((np.clip(rgba, 0, 1) * 255.0 + 0.5).astype(np.uint8), "RGBA")


def horizon(img):
    """First row whose opaque coverage crosses 50%, or -1 if the layer never does."""
    a = np.asarray(img.convert("RGBA"))[..., 3]
    cov = (a > 128).mean(1)
    hit = np.nonzero(cov > 0.5)[0]
    return int(hit.min()) if len(hit) else -1


def assemble_fg10():
    """-> (PIL RGB 4096x2560, list of panel paths) or (None, missing) if incomplete."""
    picks, missing = [], []
    for r in range(FG10_GRID[1]):
        for c in range(FG10_GRID[0]):
            found = None
            for suffix in ("-r1", ""):        # a repaint wins over the first pass
                p = ART / f"FG10-{c}_{r}{suffix}" / f"FG10-{c}_{r}.png"
                if p.exists():
                    found = p
                    break
            if found is None:
                missing.append(f"FG10-{c}_{r}")
            else:
                picks.append((c, r, found))
    if missing:
        return None, missing
    canvas = Image.new("RGB", FG10_CANVAS, (0, 255, 0))
    for c, r, p in picks:                      # row-major, later over earlier
        panel = Image.open(p).convert("RGB")
        if panel.size != FG10_PANEL:
            panel = panel.resize(FG10_PANEL, Image.LANCZOS)
        canvas.paste(panel, (c * FG10_STEP[0], r * FG10_STEP[1]))
    return canvas, [str(p.relative_to(ART)) for _, _, p in picks]


def main():
    OUT_TILES.mkdir(parents=True, exist_ok=True)
    OUT_LAYERS.mkdir(parents=True, exist_ok=True)
    report = {}

    # ---- plate: already matted, no key ------------------------------------
    print("plate: CS9-band/foreground.png (straight alpha, no key)")
    plate = Image.open(BAND / "foreground.png").convert("RGBA")
    assert plate.size == (5376, 4096), f"plate is {plate.size}, expected (5376, 4096)"
    for name, x0, x1 in (("tile_0_0.png", 0, 4096), ("tile_4096_0.png", 4096, 5376)):
        cut = plate.crop((x0, 0, x1, 4096))
        cut.save(OUT_TILES / name)
        a = np.asarray(cut)[..., 3]
        print(f"  {name:<18} {cut.size[0]}x{cut.size[1]}  "
              f"alpha0 {(a <= 0).mean():.3f}  alpha1 {(a >= 254).mean():.3f}")
    del plate

    # ---- forest source -----------------------------------------------------
    fg10, info = assemble_fg10()
    if fg10 is not None:
        forest_src, forest_note = fg10, f"FG10 3x3 assembled ({len(info)} panels)"
    else:
        forest_src, forest_note = Image.open(SRC / "L10_layer_forest.png").convert("RGB"), \
            f"L10_layer_forest.png FALLBACK (FG10 incomplete: missing {', '.join(info)})"
    print("forest source:", forest_note)
    report["forest_source"] = forest_note

    # ---- parallax layers ---------------------------------------------------
    jobs = [
        ("sky.png", Image.open(SRC / "L10_layer_sky_single.png").convert("RGB"),
         "L10_layer_sky_single.png", "opaque"),
        ("far_ruins.png", Image.open(SRC / "L10_layer_far_fixed.png").convert("RGB"),
         "L10_layer_far_fixed.png", "key"),
        ("forest_valley.png", forest_src, forest_note, "key"),
        ("mist.png", Image.open(SRC / "L10_layer_mist.png").convert("RGB"),
         "L10_layer_mist.png", "mist"),
    ]
    offsets = {}
    print("layers (scaled to the H1 WIDTH, aspect preserved):")
    for role, src_img, src_name, mode in jobs:
        rgb = np.asarray(src_img).astype(np.float32) / 255.0
        if mode == "opaque":
            rgba = np.dstack([rgb, np.ones(rgb.shape[:2], np.float32)])
        elif mode == "key":
            rgba = green_key(rgb)
        else:
            lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
            alpha = np.minimum(lum, MIST_ALPHA_CAP)
            colour = rgb / np.maximum(lum, 1.0 / 255.0)[..., None]
            rgba = np.dstack([np.clip(colour, 0, 1), alpha])
            rgba[alpha <= 0.0, :3] = 0.0
        img = to_img(rgba)
        del rgb, rgba

        a_img = Image.open(A_LAYERS / role)
        aw, ah = a_img.size
        sw, sh = img.size
        tw, th = aw, int(round(aw * sh / sw))          # WIDTH match, aspect kept
        img = img.resize((tw, th), Image.LANCZOS)
        img.save(OUT_LAYERS / role)

        ha, hb = horizon(a_img), horizon(img)
        if ha <= 0 and hb <= 0:
            dy = ah - th                               # fully opaque: bottom-align
            rule = "bottom-aligned (no horizon row in either register)"
        else:
            dy = ha - hb
            rule = f"horizon A row {ha} <- B row {hb}"
        offsets[role.replace(".png", "")] = float(dy)
        print(f"  {role:<18} {src_name}")
        print(f"      {sw}x{sh} -> {tw}x{th}   (H1 {aw}x{ah}, aspect kept, "
              f"{'taller' if th > ah else 'shorter'} by {abs(th - ah)})")
        print(f"      {rule}  ->  B sprite y offset {dy:+.0f}")
        del img, a_img

    (OUT_LAYERS / "offsets.json").write_text(json.dumps(
        {"note": "per-style vertical offset for the B parallax layer sprites; "
                 "A is always 0. Written by tools/build_b_assets.py.",
         "offsets": offsets, **report}, indent=1))
    print("wrote", OUT_LAYERS / "offsets.json")
    print("done ->", OUT_TILES, OUT_LAYERS)


if __name__ == "__main__":
    sys.exit(main())
