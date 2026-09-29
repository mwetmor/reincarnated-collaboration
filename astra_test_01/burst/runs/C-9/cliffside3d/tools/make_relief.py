#!/usr/bin/env python3
"""C-9 T9-1c: turn the painted cliff into a displacement field.

The near wall is not one flat quad -- it is 73,630 triangles in 38 horizontal bands. What
is wrong with it is not its resolution but its NORMALS: it is an extruded outline, so every
normal is horizontal and points out of the landmass, and a low key from screen-left can only
graze it. That is why 16.21% of the bridge frame lost more than half its light when the
terrain became shaded, while the open hillside -- whose normal does face up toward the key --
lost 0.03%.

So the relief has to come from the one record of what the cliff actually looks like: the
painting. Where the painter put a lit ledge he was describing a face turned toward the key;
where he put a crevice he was describing one turned away. Luminance IS that statement, and
its GRADIENT is the face he meant.

    high-pass, not raw luminance. Raw luminance carries the whole scene's lighting gradient
    -- the cliff is darker at its foot than at its lip across tens of metres -- and
    displacing by that would push the entire foot of the wall backwards without making a
    single crevice. Subtracting a blur leaves only the local relief, which is the part that
    is geometry.

Writes data/relief_v4.png: 8-bit grey at a quarter of the plate's resolution (4 canvas px
per texel, about 4 cm, against relief measured in metres), 128 meaning no displacement.
Clear plate = 128, so nothing is displaced where nothing was painted.

    usage: python3 tools/make_relief.py [--sigma 8] [--down 4]
"""
import argparse
import json
import pathlib
import sys

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

HERE = pathlib.Path(__file__).resolve().parent.parent
PLATE = HERE / "godot" / "plate" / "plate_v4.png"
OUT = HERE / "godot" / "data" / "relief_v4.png"
META = HERE / "godot" / "data" / "relief_v4.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sigma", type=float, default=8.0,
                    help="blur radius of the high-pass, in relief texels")
    ap.add_argument("--down", type=int, default=4, help="canvas pixels per relief texel")
    a = ap.parse_args()

    if not PLATE.exists():
        print(f"no plate at {PLATE}", file=sys.stderr)
        return 2
    im = Image.open(PLATE).convert("RGBA")
    W, H = im.size
    small = im.resize((W // a.down, H // a.down), Image.LANCZOS)
    arr = np.asarray(small, dtype=np.float64) / 255.0
    lum = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    alpha = arr[:, :, 3]

    try:
        from scipy.ndimage import gaussian_filter
    except ImportError:
        print("scipy is required for the high-pass", file=sys.stderr)
        return 3

    # blur only what is painted, or the clear 40% drags the edges of the cliff toward zero
    painted = alpha > 0.5
    filled = np.where(painted, lum, np.nan)
    med = float(np.nanmedian(filled))
    filled = np.where(painted, lum, med)
    base = gaussian_filter(filled, sigma=a.sigma)
    hp = filled - base

    # robust scale: the 95th percentile of |hp| over painted pixels becomes 0.5, so a
    # handful of specular sparkles cannot set the amplitude for the whole cliff
    s = float(np.percentile(np.abs(hp[painted]), 95))
    v = np.clip(hp / max(s * 2.0, 1e-6), -1.0, 1.0)
    v[~painted] = 0.0

    out = np.clip(np.round(128.0 + 127.0 * v), 0, 255).astype(np.uint8)
    Image.fromarray(out, mode="L").save(OUT)
    meta = {
        "source": "plate_v4.png",
        "plate_px": [W, H],
        "relief_px": [W // a.down, H // a.down],
        "canvas_px_per_texel": a.down,
        "highpass_sigma_texels": a.sigma,
        "encoding": "8-bit grey, 128 = no displacement, 0 = -1, 255 = +1",
        "robust_scale_p95_of_abs_highpass": round(s, 5),
        "painted_fraction": round(float(painted.mean()), 4),
        "note": ("multiply by the scene's amplitude and displace along the VIEW direction, "
                 "not the surface normal: under this orthographic camera a displacement "
                 "along fwd changes depth and normals and leaves screen position -- and "
                 "therefore the projected paint and the silhouette -- exactly untouched."),
    }
    META.write_text(json.dumps(meta, indent=1) + "\n")
    print(f"relief -> {OUT}  {W // a.down}x{H // a.down}")
    print(f"  painted {painted.mean() * 100:.1f}% of the canvas")
    print(f"  high-pass p95 |.| = {s:.5f} of full luminance range")
    print(f"  encoded range {out.min()}..{out.max()}, mean {out.mean():.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
