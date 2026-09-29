#!/usr/bin/env python3
"""C-9 meshy_t2 step 17: held-out error against the frames Astra painted.

    python3 scripts/23_heldout.py --sets x=sprites_x y=sprites_y paint=sprites_t2

Drift says whether a sequence is STEADY. It does not say whether it is RIGHT:
a sequence that propagates one key perfectly is perfectly steady and could
still have the wrong pose everywhere. So the second number is accuracy against
the painting that was actually made, on frames the propagation never saw.

  E and SE   Astra painted every frame, so every frame except the key is
             held out. This is the real test.
  the six    only two frames were painted. The key is one of them; the OTHER
             one is the held-out frame -- one sample per direction, but an
             honest one, and it is the frame furthest in time from the key.

Error is mean |dRGB| in 0-255 inside the render's own silhouette, so the matte
edge is not being scored. Reported next to the drift so the trade is visible:
propagating harder buys steadiness and costs fidelity to the paint.
"""
import argparse, json, os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "out")
WORK = os.path.join(ROOT, "work")
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
PAINTED = ["E", "SE"]
CLIPS = {"idle": 12, "walk": 12, "run": 8, "attack": 12}


def mask_of(clip, d, i):
    p = os.path.join(OUT, clip, "guides_mask", d, "mask_%s_%02d.png" % (d, i))
    return np.asarray(Image.open(p).convert("RGBA"))[..., 3] > 128


def rgb_of(path):
    return np.asarray(Image.open(path).convert("RGBA")).astype(np.float64)[..., :3]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sets", nargs="+", required=True)
    ap.add_argument("--out", default=os.path.join(WORK, "heldout.json"))
    args = ap.parse_args()
    chosen = json.load(open(os.path.join(WORK, "chosen.json")))
    rep = dict(note="mean |dRGB| 0-255 vs the Astra-painted frame, inside the "
                    "render mask, on frames the propagation did not see",
               sets={})
    plans = {}
    for s in args.sets:
        name, root = s.split("=", 1)
        pf = os.path.join(WORK, "onekey_plan_%s.json" % name.upper())
        plans[name] = json.load(open(pf)) if os.path.exists(pf) else None
        rep["sets"][name] = dict(root=root, dirs={})
    print("%-6s %-7s %-4s %7s %7s %6s" % ("set", "clip", "dir", "n", "MAE", "key"))
    for name, root in (s.split("=", 1) for s in args.sets):
        plan = plans[name]
        for clip, n in CLIPS.items():
            for d in DIRS:
                src = chosen.get(clip, {})
                if d in PAINTED:
                    v = src.get(d)
                    if not v:
                        continue
                    pr = os.path.join(ROOT, "paint_%s" % v, clip, d)
                    held = list(range(n))
                else:
                    k = src.get("keys")
                    v = (k.get(d) if isinstance(k, dict) else k)
                    if not v:
                        continue
                    pr = os.path.join(ROOT, "paint_%s" % v, clip, d)
                    held = [0, n // 2]
                key = None
                if plan:
                    e = plan["keys"].get("%s/%s" % (clip, d)) or plan["keys"].get(d)
                    if e and e["src_clip"] == clip:
                        key = e["src_frame"]
                errs = []
                for i in held:
                    if i == key:
                        continue
                    gp = os.path.join(pr, "%s_%s_%02d.png" % (clip, d, i))
                    sp = os.path.join(root, clip, d, "%s_%s_%02d.png" % (clip, d, i))
                    if not (os.path.exists(gp) and os.path.exists(sp)):
                        continue
                    m = ndi.binary_erosion(mask_of(clip, d, i), np.ones((5, 5)))
                    if m.sum() < 50:
                        continue
                    errs.append(float(np.abs(rgb_of(sp)[m] - rgb_of(gp)[m]).mean()))
                if not errs:
                    continue
                rep["sets"][name]["dirs"]["%s/%s" % (clip, d)] = dict(
                    n=len(errs), mae=round(float(np.mean(errs)), 2),
                    mae_max=round(float(np.max(errs)), 2), key=key)
                print("%-6s %-7s %-4s %7d %7.2f %6s"
                      % (name, clip, d, len(errs), float(np.mean(errs)),
                         ("f%02d" % key) if key is not None else "-"))
    for name in rep["sets"]:
        vals = [v["mae"] for v in rep["sets"][name]["dirs"].values()]
        if vals:
            rep["sets"][name]["mae_mean"] = round(float(np.mean(vals)), 2)
            rep["sets"][name]["mae_max"] = round(float(np.max(vals)), 2)
            print("%-6s OVERALL mean %.2f  max %.2f"
                  % (name, rep["sets"][name]["mae_mean"], rep["sets"][name]["mae_max"]))
    json.dump(rep, open(args.out, "w"), indent=1)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
