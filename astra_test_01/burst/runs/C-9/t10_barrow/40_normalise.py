#!/usr/bin/env python3
"""C-9 T10: yaw and true scale for the barrow assets, measured against the painted plates.

    python3 40_normalise.py --probe DIR

Same method as T9: probe_props3d.gd renders each model through the cliff camera's own basis
every 15 degrees, and the yaw whose silhouette best matches the asset's identity plate wins.
The plate is the right target because it is what the guide camera SAW of that object in that
place; relating a generator's turntable axes to the cliff's by algebra is a calculation with
a sign in it that renders perfectly when it is wrong.

THE PITCH CORRECTION CARRIES OVER AND THIS SCENE HAS ITS OWN CHECK FOR IT. The identity
plates are crops of a painting made at the guide camera's 52.95 degrees, so a model built
from them is squat by cos(pitch) = 0.602 and needs a Y stretch of 1.660 -- the T9 finding.
There it was verified against the rail post, whose true size the blockout knew. Here the
check is the LINTEL: a beam measured at 2.28 m long and 1.18 m tall off the same painting
through K. A beam's length is across the screen and so is NOT foreshortened, while its
height is -- so the ratio of the two after correction is a prediction this file can be
wrong about, and says so.
"""
import argparse, json, pathlib
import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
GODOT = HERE.parent / "cliffside3d" / "godot"
PLATES = HERE / "plates"
PITCH_COS = 0.602462172508240

# asset -> (identity plate, true size m, axis, pitch-correct?, forced width m)
OBJECTS = {
    "stone_tall":  ("T10_standing_stone_tall.png",  2.71, "height", True,  None),
    "stone_mid":   ("T10_standing_stone_mid.png",   2.71, "height", True,  None),
    "stone_short": ("T10_standing_stone_short.png", 1.24, "height", True,  None),
    "lintel":      ("T10_barrow_lintel.png",        2.28, "across", True,  None),
    "post":        ("T10_barrow_post.png",          2.04, "height", True,  None),
    "rock_large":  ("T10_rock_outcrop_large.png",   1.84, "height", True,  None),
    "rock_small":  ("T10_rock_outcrop_small.png",   0.54, "height", True,  None),
    # WIDTH FORCED. Both builds come out ~2.35 m across at 3.36 m tall against the
    # concept's measured 1.38 m -- Tripo 2.39, procedural 2.33 -- so the error is not one
    # builder's, and a tree is the one asset where a horizontal squash is defensible.
    "birch":       ("T10_dead_birch.png",           3.36, "height", True,  1.38),
    "juniper":     ("T10_juniper_bush.png",         1.15, "height", True,  None),
}


def mask(p, thr=40):
    a = np.asarray(Image.open(p).convert("RGBA"))
    if a.shape[-1] == 4 and (a[..., 3] < 250).any():
        m = a[..., 3] > 128
    else:                                   # the plates are matted onto #00ff00
        r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
        m = ~((g > 150) & (r < 110) & (b < 110) & (g - np.maximum(r, b) > 80))
    ys, xs = np.nonzero(m)
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def iou(a, b, n=192):
    def fit(m):
        im = Image.fromarray((m * 255).astype(np.uint8))
        s = n / max(m.shape)
        im = im.resize((max(1, round(m.shape[1] * s)), max(1, round(m.shape[0] * s))), Image.BILINEAR)
        o = np.zeros((n, n), bool); q = np.asarray(im) > 127
        y, x = (n - q.shape[0]) // 2, (n - q.shape[1]) // 2
        o[y:y + q.shape[0], x:x + q.shape[1]] = q
        return o
    A, B = fit(a), fit(b)
    u = (A | B).sum()
    return float((A & B).sum() / u) if u else 0.0


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--probe", required=True)
    a = ap.parse_args(); probe = pathlib.Path(a.probe)
    info = json.loads((probe / "props3d_probe.json").read_text())
    models = {}
    for obj, (plate, size_m, axis, pitch, wm) in OBJECTS.items():
        pp = PLATES / plate
        rends = sorted(probe.glob("%s_yaw*.png" % obj))
        if not pp.exists() or not rends:
            print("%-12s no %s" % (obj, "plate" if not pp.exists() else "renders")); continue
        sp = mask(pp)
        sc = sorted(((iou(mask(r), sp), int(r.stem.split("yaw")[1])) for r in rends), reverse=True)
        best_iou, best_y = sc[0]
        raw = info["models"][obj]["raw_aabb_m"]
        models[obj] = {"glb": "res://models/barrow/%s.glb" % obj, "height_m": size_m,
                       "axis": axis, "yaw_deg": float(best_y), "pitch_correct": pitch,
                       "width_m": wm, "matched_plate": plate,
                       "match_iou": round(best_iou, 3),
                       "iou_spread_over_yaw": round(best_iou - sc[-1][0], 3),
                       "raw_aabb_m": raw, "tris": info["models"][obj].get("tris")}
        print("%-12s yaw %3d  IoU %.3f  spread %.3f  raw %s"
              % (obj, best_y, best_iou, models[obj]["iou_spread_over_yaw"], raw))
    # THE LINTEL CHECK: a beam 2.28 m long and 1.18 m tall on the painting. Length is
    # across the screen (not foreshortened), height is (foreshortened by cos pitch), so
    # after the Y stretch the model's own length:height should land near 2.28/1.18 = 1.93.
    if "lintel" in models:
        r = models["lintel"]["raw_aabb_m"]
        raw_ratio = max(r[0], r[2]) / max(r[1], 1e-9)
        corrected = raw_ratio * PITCH_COS
        print("\nlintel pitch check: raw length:height %.2f -> %.2f after the Y stretch; "
              "the painting says %.2f" % (raw_ratio, corrected, 2.28 / 1.18))
        models["lintel"]["pitch_check"] = {"raw_ratio": round(raw_ratio, 3),
                                           "corrected": round(corrected, 3),
                                           "painting": round(2.28 / 1.18, 3)}
    out = {"_what": "C-9 T10 barrow assets: yaw measured against the identity plates, "
                    "true scale from the concept through K = 140.86 px/m.",
           "models": models}
    (GODOT / "data" / "barrow_assets.json").write_text(json.dumps(out, indent=1) + "\n")
    print("-> %s" % (GODOT / "data" / "barrow_assets.json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
