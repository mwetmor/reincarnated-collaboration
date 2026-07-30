#!/usr/bin/env python3
"""GAL-CAM: draw the solved camera back onto the footage.

Forward map used everywhere (inverse of gc_surface.py):
    y = y_h + 1 / (C * Z)
    x = px0 + X * A / (C * Z)

If the camera is right, ground circles drawn around the player's anchor come out
as the ellipses the eye already expects, the 12 m ring falls off the bottom of
the frame, and the horizon line sits where no ground is drawn. If it is wrong,
that is visible immediately -- which is the point of drawing it.

Also re-derives the WR1-GAL-3 death-2 separation under this camera, because
GAL-3 measured it under an ORTHOGRAPHIC assumption with an assumed axis ratio
k=0.72, and both of those inputs have now been measured instead of assumed.
"""
import argparse
import json
import math
import os

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.normpath(os.path.join(HERE, "..", "..", "captures",
                                       "2026-07-29-wr1-gal3", "frames"))


class Cam:
    def __init__(self, A, C, y_h, px0):
        self.A, self.C, self.y_h, self.px0 = A, C, y_h, px0

    def to_ground(self, x, y):
        Z = 1.0 / (self.C * (y - self.y_h))
        X = (x - self.px0) / (self.A * (y - self.y_h))
        return X, Z

    def to_screen(self, X, Z):
        y = self.y_h + 1.0 / (self.C * Z)
        x = self.px0 + X * self.A / (self.C * Z)
        return x, y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ring", required=True)
    ap.add_argument("--frame", type=int, default=309000)
    ap.add_argument("--out", required=True)
    ap.add_argument("--px0", type=float, default=960.0)
    ap.add_argument("--xp", type=float, default=962.0)
    ap.add_argument("--yp", type=float, default=595.0)
    ap.add_argument("--rings", type=float, nargs="*",
                    default=[1.6, 3.0, 5.0, 8.0, 12.0])
    args = ap.parse_args()

    R = json.load(open(args.ring))
    cam = Cam(R["solution"]["A"], R["solution"]["C"], R["y_h"], args.px0)
    Xp, Zp = cam.to_ground(args.xp, args.yp)
    print(f"player ground anchor: X={Xp:.3f} Z={Zp:.3f} (Z is distance-like, "
          f"absolute origin arbitrary)")

    p = os.path.join(FRAMES, f"f{args.frame:06d}.png")
    im = Image.open(p).convert("RGB")
    d = ImageDraw.Draw(im)
    cols = [(255, 90, 90), (255, 190, 0), (0, 235, 235), (120, 255, 120),
            (255, 120, 255)]
    for i, r in enumerate(args.rings):
        pts = []
        for a in np.linspace(0, 2 * math.pi, 361):
            X, Z = Xp + r * math.cos(a), Zp + r * math.sin(a)
            if Z <= 0.2:
                continue
            x, y = cam.to_screen(X, Z)
            if -4000 < x < 6000 and -4000 < y < 6000:
                pts.append((x, y))
        if len(pts) > 2:
            d.line(pts + [pts[0]], fill=cols[i % len(cols)], width=3)
            xt, yt = cam.to_screen(Xp, Zp + r)
            d.text((xt + 6, yt - 16), f"{r:g} m", fill=cols[i % len(cols)])
    # metre grid lines parallel to the screen axes, at the player's row
    gxp = cam.A * (args.yp - cam.y_h)
    for m in range(-16, 17, 4):
        x = args.xp + m * gxp
        if 0 <= x < 1920:
            d.line([x, args.yp - 14, x, args.yp + 14], fill=(200, 200, 200), width=2)
            d.text((x - 8, args.yp + 18), f"{m:+d}", fill=(200, 200, 200))
    d.line([0, args.yp, 1919, args.yp], fill=(90, 90, 90), width=1)
    # play-area cut used for the DECISION surface
    for yy, lab in ((60, "HUD cut top"), (950, "HUD cut bottom")):
        d.line([0, yy, 1919, yy], fill=(255, 255, 0), width=2)
        d.text((14, yy + 4), lab, fill=(255, 255, 0))
    d.line([args.xp - 18, args.yp, args.xp + 18, args.yp], fill=(255, 255, 0), width=3)
    d.line([args.xp, args.yp - 18, args.xp, args.yp + 18], fill=(255, 255, 0), width=3)
    d.text((14, 14), f"f{args.frame}  ground-plane rings about the player anchor "
                     f"({args.xp:.0f},{args.yp:.0f})", fill=(255, 255, 255))
    d.text((14, 34), f"g_x={gxp:.1f} px/m at the anchor row; horizon row "
                     f"y_h={cam.y_h:.0f} (off-frame, above)", fill=(255, 255, 255))
    im.save(args.out, quality=93)
    print("wrote", args.out)

    # --- death-2 separation re-derived under the measured camera ---
    caster = (1024.7, 568.5)
    player = (962.0, 602.0)
    Xc, Zc = cam.to_ground(*caster)
    Xq, Zq = cam.to_ground(*player)
    r = math.hypot(Xq - Xc, Zq - Zc)
    print(f"\nWR1-GAL-3 death-2 re-derivation under the measured camera:")
    print(f"  caster ground ({Xc:+.3f},{Zc:+.3f})  player ground "
          f"({Xq:+.3f},{Zq:+.3f})")
    print(f"  separation = {r:.3f} m   (GAL-3 reported 1.257 m under an "
          f"orthographic camera with assumed k=0.72)")
    print(f"  ratio to GAL-3 point estimate: {r/1.2574:.3f}")


if __name__ == "__main__":
    main()
