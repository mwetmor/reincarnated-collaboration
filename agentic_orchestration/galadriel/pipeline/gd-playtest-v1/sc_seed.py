#!/usr/bin/env python3
"""SHADOW-CAL instrument SC-6: seeded shadow measurement on a single frame.

The automatic route (SC-1/SC-5) needs a figure to TRANSLATE through the world
before a median plate can reveal it, and this fixture spends most of its 1h53m
standing still in menus.  SC-6 drops that requirement: a human names the ground
contact point of a figure, and the instrument does everything after that --
segmentation against a LOCAL floor level, ground-plane unprojection, azimuth,
length, height, occlusion ratio -- and renders an overlay so the segmentation
can be judged rather than trusted.

The seeding is manual; NO measured quantity is.  Every seed's overlay is kept as
evidence, including the ones that were thrown out.
"""
import argparse
import json
import math
import os

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

import sc_cam


def local_floor(L, cx, cy, r_px, r_in_frac=1.15, r_out_frac=2.2):
    """Unshadowed floor level from an ANNULUS around the seed.

    The first version took the 70th percentile of a DISC centred on the figure.
    That disc contains the figure, its shadow and any VFX, so on fogged ground
    the "floor" landed above most real floor pixels and the segmenter returned
    the whole neighbourhood.  An annulus outside the shadow's reach, read at the
    MEDIAN, is the level the shadow should be compared against.
    """
    yy, xx = np.ogrid[:L.shape[0], :L.shape[1]]
    d2 = (xx - cx) ** 2 + (yy - cy) ** 2
    ann = (d2 >= (r_in_frac * r_px) ** 2) & (d2 <= (r_out_frac * r_px) ** 2)
    disc = d2 <= r_px ** 2
    if ann.sum() < 800:
        return float(np.median(L[disc])), disc, ann
    return float(np.median(L[ann])), disc, ann


def measure(frame_rgb, seed_xy, cam, r_m=4.0, k_shadow=0.78, base_xy=None,
            top_y=None, min_px=150):
    a = np.asarray(frame_rgb, np.float32)
    L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    cx, cy = seed_xy
    g0 = cam.unproject_ground([[float(cx), float(cy)]])
    # radius in px: convert r_m of ground along +X at this row
    p1 = cam.project(np.array([[g0[0] + r_m, 0.0, g0[2]]]))
    r_px = float(abs(p1[0] - cx))
    floor, disc, ann = local_floor(L, cx, cy, r_px)

    dark = (L < k_shadow * floor) & disc
    dark = ndimage.binary_opening(dark, np.ones((3, 3)))
    dark = ndimage.binary_closing(dark, np.ones((5, 5)))
    lab, n = ndimage.label(dark)
    if n == 0:
        return None
    sid = lab[int(round(cy)), int(round(cx))]
    if sid == 0:                      # seed not inside a dark blob: take nearest
        d, idx = ndimage.distance_transform_edt(lab == 0, return_indices=True)
        sid = lab[idx[0][int(cy), int(cx)], idx[1][int(cy), int(cx)]]
    if sid == 0:
        return None
    m = lab == sid
    if m.sum() < min_px:
        return None

    ys, xs = np.nonzero(m)
    # geometry is referenced to the FIGURE's ground contact when one is given;
    # the seed only chooses which dark blob is the shadow
    if base_xy is not None:
        gb = cam.unproject_ground([[float(base_xy[0]), float(base_xy[1])]])
        origin = np.array([gb[0], gb[2]])
    else:
        gb = None
        origin = np.array([g0[0], g0[2]])
    g = cam.unproject_ground(np.stack([xs, ys], 1).astype(float))
    d = g[:, [0, 2]] - origin
    rad = np.hypot(d[:, 0], d[:, 1])
    tip = d[rad >= np.quantile(rad, 0.99)].mean(0)
    cen = d.mean(0)
    inner = L[m]
    frac = float(m.sum()) / max(disc.sum(), 1)
    return {
        "seed": [float(cx), float(cy)],
        "floor_luma": floor,
        "disc_fill": frac,
        "shadow_px": int(m.sum()),
        "shadow_luma_med": float(np.median(inner)),
        "rho_vs_local_floor": float(np.median(inner) / floor),
        "len_m": float(np.hypot(*tip)),
        "az_tip": float(math.degrees(math.atan2(tip[1], tip[0]))),
        "az_cen": float(math.degrees(math.atan2(cen[1], cen[0]))),
        "cen_len_m": float(np.hypot(*cen)),
        "r_px": r_px,
        "base_px": list(base_xy) if base_xy is not None else None,
        "h_m": (float(cam.solve_height((gb[0], gb[2]), top_y))
                if (base_xy is not None and top_y is not None) else None),
        "ratio": (float(np.hypot(*tip) / cam.solve_height((gb[0], gb[2]), top_y))
                  if (base_xy is not None and top_y is not None) else None),
        "mask": m,
    }


def overlay(frame_rgb, res, out, box_pad=170):
    a = np.asarray(frame_rgb, np.float32).copy()
    for r in res:
        if r is None:
            continue
        a[r["mask"]] = a[r["mask"]] * 0.35 + np.array([255, 40, 40]) * 0.65
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for r in res:
        if r is None:
            continue
        cx, cy = r["seed"]
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], outline=(0, 255, 0), width=2)
        if r.get("base_px"):
            bx, by = r["base_px"]
            d.ellipse([bx - 7, by - 7, bx + 7, by + 7], outline=(0, 255, 255), width=3)
            d.line([bx, by, cx, cy], fill=(0, 255, 255), width=2)
        d.text((cx + 10, cy + 6),
               f"az {r['az_tip']:.0f}  L {r['len_m']:.2f}m  rho {r['rho_vs_local_floor']:.2f}",
               fill=(255, 255, 0))
    im.save(out, quality=93)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame", required=True)
    ap.add_argument("--seeds", type=float, nargs="+", required=True,
                    help="x1 y1 x2 y2 ...")
    ap.add_argument("--r", type=float, default=4.0)
    ap.add_argument("--k", type=float, default=0.78)
    ap.add_argument("--base", type=float, nargs="+", default=None,
                    help="bx1 by1 bx2 by2 ... figure ground-contact per seed")
    ap.add_argument("--top", type=float, nargs="+", default=None,
                    help="screen row of each figure's top")
    ap.add_argument("--out", default=None)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    cam = sc_cam.nominal()
    im = Image.open(a.frame).convert("RGB")
    seeds = list(zip(a.seeds[::2], a.seeds[1::2]))
    bases = (list(zip(a.base[::2], a.base[1::2])) if a.base else [None] * len(seeds))
    tops = a.top if a.top else [None] * len(seeds)
    res = [measure(im, s, cam, r_m=a.r, k_shadow=a.k, base_xy=b, top_y=tp)
           for s, b, tp in zip(seeds, bases, tops)]
    for s, r in zip(seeds, res):
        if r is None:
            print(f"  seed {s}  NO BLOB")
            continue
        print(f"  seed ({s[0]:6.0f},{s[1]:6.0f})  px {r['shadow_px']:6d}  "
              f"az {r['az_tip']:+7.1f}  L {r['len_m']:5.2f} m  "
              f"floor {r['floor_luma']:5.1f}  shadow {r['shadow_luma_med']:5.1f}  "
              f"rho {r['rho_vs_local_floor']:.3f}" +
              (f"  h {r['h_m']:.2f} m  L/h {r['ratio']:.3f}"
               if r.get("ratio") else ""))
    if a.out:
        overlay(im, res, a.out)
        print("  ->", a.out)
    if a.json:
        json.dump([{k: v for k, v in r.items() if k != "mask"}
                   for r in res if r], open(a.json, "w"))
