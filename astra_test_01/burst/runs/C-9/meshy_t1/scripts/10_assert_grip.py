#!/usr/bin/env python3
"""C-9 meshy_t1: ASSERT the gauntlet is actually on the haft (R-C9-61 blocker 1).

    python3 scripts/10_assert_grip.py [state ...]

"The grip is not visible" is a claim about pixels, so it is tested on pixels.
The part-ID guide already colours every pixel by its dominant bone, and the
weapon carries a reserved flat colour, so for each frame and direction:

    do the RIGHT-HAND pixels touch the WEAPON pixels?

Adjacency, not overlap: a gauntlet closed round a haft occludes it, so the two
regions meet at a boundary rather than intersecting. A frame passes if any
right-hand pixel lies within `REACH` px of a weapon pixel.

Frames where the hand is genuinely hidden (fewer than MIN_HAND hand pixels
visible, e.g. the far side in W) are counted separately as OCCLUDED rather
than failed -- scoring them as failures would punish a correct pose for being
behind the body.
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
T1 = os.path.dirname(HERE)
OUT = os.environ.get("K3D_OUT") or os.path.join(T1, "out")
SUB = os.environ.get("K3D_SUB", "")
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
REACH = 3
MIN_HAND = 12


def srgb(c):
    """Blender writes a FLOAT_COLOR attribute through an Emission shader into
    an sRGB PNG, so the stored bone colour is LINEAR and the pixel is ENCODED.
    Matching the linear value against the pixel finds nothing -- and the check
    then reports every frame as 'occluded', which reads like a pose failure and
    is a colour-space bug in the instrument. Encode before comparing."""
    c = np.asarray(c, float)
    return np.where(c <= 0.0031308, c * 12.92,
                    1.055 * np.power(np.clip(c, 1e-8, None), 1 / 2.4) - 0.055)


def close(a, b, tol=10):
    return (np.abs(a.astype(int) - np.array(b, int)).max(-1) <= tol)


def main():
    states = sys.argv[1:] or ["walk", "run", "idle"]
    rep = {"note": __doc__.strip().splitlines()[0], "reach_px": REACH,
           "min_hand_px": MIN_HAND, "states": {}}
    for st in states:
        sd = (SUB or st)
        rp = os.path.join(OUT, sd, "render_%s.json" % st)
        if not os.path.exists(rp):
            continue
        r = json.load(open(rp))
        bc = r["guides"]["bone_colours"]
        hand = [int(round(v * 255)) for v in srgb(bc.get("RightHand", [0, 0, 0]))]
        n = r["frames"]
        tot = ok = occ = 0
        per = {}
        for d in (os.environ.get("K3D_DIRS", "").split(",") if os.environ.get("K3D_DIRS") else DIRS):
            pd = os.path.join(OUT, sd, "guides_part", d)
            wd = os.path.join(OUT, sd, "weapon", d)
            g = b = o = 0
            for i in range(n):
                pp = os.path.join(pd, "part_%s_%02d.png" % (d, i))
                wp = os.path.join(wd, "weapon_%s_%02d.png" % (d, i))
                if not (os.path.exists(pp) and os.path.exists(wp)):
                    continue
                P = np.asarray(Image.open(pp).convert("RGB"))
                W = np.asarray(Image.open(wp).convert("RGBA"))[..., 3] > 8
                Hm = close(P, hand)
                tot += 1
                if Hm.sum() < MIN_HAND:
                    o += 1; occ += 1; continue
                near = ndi.binary_dilation(W, np.ones((2 * REACH + 1,) * 2))
                if (Hm & near).any():
                    g += 1; ok += 1
                else:
                    b += 1
            per[d] = dict(pass_=g, fail=b, occluded=o, frames=n)
        rep["states"][st] = dict(per_dir=per, frames_total=tot, passed=ok,
                                 occluded=occ, failed=tot - ok - occ,
                                 pass_rate_of_visible=round(ok / max(tot - occ, 1), 4))
        print("  %-6s %3d frames: PASS %3d  FAIL %3d  occluded %3d   (%.0f %% of visible)"
              % (st, tot, ok, tot - ok - occ, occ,
                 100 * ok / max(tot - occ, 1)))
        bad = [d for d, v in per.items() if v["fail"]]
        if bad:
            print("         failing dirs: " + ", ".join(
                "%s(%d)" % (d, per[d]["fail"]) for d in bad))
    json.dump(rep, open(os.path.join(T1, "work", "grip_assert.json"), "w"), indent=1)
    print("wrote work/grip_assert.json")


main()
