#!/usr/bin/env python3
"""C-9: build the Illuminated-register ("B") texture set for the cliffside A/B build.

Reads the painted B art from runs/C-9/artifacts/CS9-assembly/ (read-only) and writes
keyed / split / resized Godot-ready PNGs into this project's parallax/tiles_b/ and
parallax/layers_b/.  Geometry is NOT touched: the plate is painted on the same v4 grid
as the H1 plate, and every layer is resized to the exact H1 size for its role so the
positions and scroll rates already in parallax/parallax.json apply unchanged.

  plate   cliffside_B_plate_preview.png  5376x4096 RGB, flat #00ff00 = void
          -> green-keyed to RGBA + despilled, split on the H1 tile grid:
             tiles_b/tile_0_0.png    (0,0,4096,4096)
             tiles_b/tile_4096_0.png (4096,0,1280,4096)
  sky     layer_sky.png     opaque, no key      -> resize to H1 sky.png size
  far     layer_far.png     #00ff00 above land  -> key  -> resize to H1 far_ruins.png
  forest  layer_forest.png  #00ff00 above trees -> key  -> resize to H1 forest_valley.png
  mist    layer_mist.png    light-on-black      -> alpha=luminance (unpremultiplied,
          capped at the H1 mist's own max alpha of 220/255) -> resize to H1 mist.png

Green key: greenness d = G - max(R,B).  Measured on all three keyed sources the
distribution is cleanly bimodal -- d jumps to ~0.45 (plate) / ~0.35 (far) / ~0.20
(forest) of pixels by d>=0.10 and is flat from there to d>=0.70 -- so the ramp below
(opaque at d<=0.08, transparent at d>=0.25) sits in the empty gap and keeps the
painted antialiased fringe as partial alpha rather than a hard cut.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

PROJ = Path(__file__).resolve().parent.parent
SRC = PROJ.parent / "artifacts" / "CS9-assembly"
A_LAYERS = PROJ / "parallax" / "layers"
OUT_TILES = PROJ / "parallax" / "tiles_b"
OUT_LAYERS = PROJ / "parallax" / "layers_b"

KEY_LO, KEY_HI = 0.08, 0.25      # greenness ramp: <=LO opaque, >=HI fully keyed
DESPILL_AT = 0.02                # despill any pixel greener than this
MIST_ALPHA_CAP = 220 / 255.0     # H1 mist.png's own maximum alpha


def load_rgb(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(np.float32) / 255.0


def green_key(rgb):
    """Tolerant #00ff00 key + light despill. Returns float RGBA in [0,1]."""
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    d = g - np.maximum(r, b)
    alpha = np.clip((KEY_HI - d) / (KEY_HI - KEY_LO), 0.0, 1.0)
    # despill: pull green down toward the other channels wherever it leads them
    out = rgb.copy()
    spill = d > DESPILL_AT
    out[..., 1] = np.where(spill, np.maximum(r, b) + np.minimum(d, DESPILL_AT), g)
    rgba = np.dstack([out, alpha])
    rgba[alpha <= 0.0, :3] = 0.0   # zero the RGB of fully-keyed pixels
    return rgba


def to_img(rgba):
    return Image.fromarray((np.clip(rgba, 0, 1) * 255.0 + 0.5).astype(np.uint8), "RGBA")


def stats(name, rgba):
    a = rgba[..., 3]
    print(f"  {name:<26} {rgba.shape[1]}x{rgba.shape[0]}  "
          f"alpha0 {float((a <= 0.002).mean()):.3f}  "
          f"alpha1 {float((a >= 0.998).mean()):.3f}  "
          f"partial {float(((a > 0.002) & (a < 0.998)).mean()):.4f}")


def main():
    OUT_TILES.mkdir(parents=True, exist_ok=True)
    OUT_LAYERS.mkdir(parents=True, exist_ok=True)

    # ---- plate -> two tiles on the H1 grid -------------------------------
    print("plate:")
    plate = green_key(load_rgb(SRC / "cliffside_B_plate_preview.png"))
    h, w = plate.shape[:2]
    assert (w, h) == (5376, 4096), f"plate is {w}x{h}, expected 5376x4096"
    stats("cliffside_B_plate", plate)
    for name, x0, x1 in (("tile_0_0.png", 0, 4096), ("tile_4096_0.png", 4096, 5376)):
        cut = plate[:, x0:x1]
        to_img(cut).save(OUT_TILES / name)
        stats(f"  -> {name}", cut)
    del plate

    # ---- parallax layers -------------------------------------------------
    # (src file, H1 role file, mode)
    jobs = [
        ("layer_sky.png", "sky.png", "opaque"),
        ("layer_far.png", "far_ruins.png", "key"),
        ("layer_forest.png", "forest_valley.png", "key"),
        ("layer_mist.png", "mist.png", "mist"),
    ]
    print("layers:")
    for src_name, role, mode in jobs:
        rgb = load_rgb(SRC / src_name)
        if mode == "opaque":
            rgba = np.dstack([rgb, np.ones(rgb.shape[:2], np.float32)])
        elif mode == "key":
            rgba = green_key(rgb)
        else:  # mist: painted as light on black -> alpha from luminance
            lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
            alpha = np.minimum(lum, MIST_ALPHA_CAP)
            colour = rgb / np.maximum(lum, 1.0 / 255.0)[..., None]   # unpremultiply
            rgba = np.dstack([np.clip(colour, 0, 1), alpha])
            rgba[alpha <= 0.0, :3] = 0.0
        target = Image.open(A_LAYERS / role).size          # exact H1 size for this role
        img = to_img(rgba)
        src_size = img.size
        if src_size != target:
            img = img.resize(target, Image.LANCZOS)
        img.save(OUT_LAYERS / role)
        stats(f"{src_name} -> {role}",
              np.asarray(img).astype(np.float32) / 255.0)
        print(f"    resized {src_size[0]}x{src_size[1]} -> {target[0]}x{target[1]}")
        del rgb, rgba, img

    print("done ->", OUT_TILES, OUT_LAYERS)


if __name__ == "__main__":
    sys.exit(main())
