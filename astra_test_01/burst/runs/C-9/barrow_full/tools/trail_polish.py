#!/usr/bin/env python3
"""C-9 T10-2 step 4 polish -- HIS SNOW TRAIL, MEASURED: the first shading against the polish. drax.

    python3 tools/trail_polish.py [--capture captures/painted/trail]

Reads the frames godot/tools/capture_painted.gd --trail wrote -- one walk over open arena snow, the
camera parked over it, the SAME trail shot in both shadings:
  trail_untouched.png  the ground before he walked
  trail_mode0.png      the first version: the base sampled at the displaced surface, the snow's cool
                       press tint, the ramp's full per-channel ratio clamped at 2
  trail_mode1.png      the polish: the base is the painting at the undisturbed surface, the ramp
                       adds only the relief -- the dent toward the painter's shadow colour, the
                       berm lifted without clipping a channel
  trail_id.png         where the trail is: press in red, berm in green
Two measures, sRGB 0-255, per channel:
  SAME PIXELS: the trail against the same pixels before he walked (the tone jump the trail makes)
  NEARBY: the trail's mean against the untouched snow 12-40 px round it, in the same frame, less
          the same two regions' difference in the untouched frame (the painting's own)
Writes take/build/trail_polish.json and take/build/trail_polish.png (untouched / first / polish).
"""
import argparse
import json
import os

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

BF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--capture", default=os.path.join(BF, "captures", "painted", "trail"))
    a = ap.parse_args()
    rd = lambda n: np.asarray(Image.open(os.path.join(a.capture, n)).convert("RGB")).astype(np.float64)
    U, M0, M1, ID = rd("trail_untouched.png"), rd("trail_mode0.png"), rd("trail_mode1.png"), rd("trail_id.png")
    press = ID[..., 0] > 8
    berm = (ID[..., 1] > 8) & ~press
    trail = press | berm
    ring = ndimage.binary_dilation(trail, iterations=40) & ~ndimage.binary_dilation(trail, iterations=12)
    lum = lambda x: x @ np.array([0.2126, 0.7152, 0.0722])
    out = {"_what": "C-9 T10-2 step 4 polish: his snow trail against the untouched painted snow, the first shading and the polish",
           "trail_px": {"all": int(trail.sum()), "press": int(press.sum()), "berm": int(berm.sum())}, "ring_px": int(ring.sum())}
    for nm, M in (("first_version", M0), ("polish", M1)):
        rec = {}
        for mk, mm in (("trail", trail), ("press", press), ("berm", berm)):
            d = M[mm] - U[mm]
            rec["same_pixels_" + mk] = {"mean_signed_rgb": [round(float(x), 2) for x in d.mean(0)],
                                        "mean_abs": round(float(np.abs(d).mean()), 2),
                                        "luminance_signed": round(float(lum(d).mean()), 2),
                                        "warmth_r_minus_b_signed": round(float((d[:, 0] - d[:, 2]).mean()), 2)}
        # THE ROPE: trail pixels brighter than the snow was (the lit berm) and near-white ones
        dl = lum(M[trail]) - lum(U[trail])
        rec["rope"] = {"share_of_trail_brighter_by_8_or_more": round(float((dl >= 8).mean()), 4),
                       "share_of_trail_at_or_over_248_in_every_channel": round(float((M[trail].min(-1) >= 248).mean()), 4),
                       "untouched_share_at_or_over_248": round(float((U[trail].min(-1) >= 248).mean()), 4)}
        near = (M[trail].mean(0) - M[ring].mean(0)) - (U[trail].mean(0) - U[ring].mean(0))
        rec["nearby"] = {"trail_minus_ring_rgb": [round(float(x), 2) for x in near],
                         "abs_mean": round(float(np.abs(near).mean()), 2)}
        out[nm] = rec
    json.dump(out, open(os.path.join(BF, "take", "build", "trail_polish.json"), "w"), indent=1)
    # the still: the trail's box, three rows
    ys, xs = np.nonzero(trail)
    x0, x1 = max(int(xs.min()) - 40, 0), min(int(xs.max()) + 40, U.shape[1])
    y0, y1 = max(int(ys.min()) - 40, 0), min(int(ys.max()) + 40, U.shape[0])
    w, h = x1 - x0, y1 - y0
    pic = Image.new("RGB", (w, 3 * h + 2 * 26 + 26), (255, 255, 255))
    dr = ImageDraw.Draw(pic)
    for i, (lbl, arr) in enumerate((("untouched painted snow", U), ("the first shading (film, 12 s)", M0),
                                    ("the polish: the painting's base, the ramp's relief only", M1))):
        y = i * (h + 26)
        dr.text((6, y + 6), lbl, fill=(40, 40, 40))
        pic.paste(Image.fromarray(arr[y0:y1, x0:x1].astype(np.uint8)), (0, y + 24))
    pic.save(os.path.join(BF, "take", "build", "trail_polish.png"))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
