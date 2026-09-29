#!/usr/bin/env python3
"""C-9 T9-1a: choose each model's yaw against its PAINTED SPRITE, and write props3d.json.

    python3 13_normalise.py --probe DIR

probe_props3d.gd renders every model through the cliff camera's own basis at 15-degree
steps. This compares each of those silhouettes against the silhouette of the sprite the
painter drew of that prop standing in that place, and keeps the yaw that matches best.

The painted sprite is the right target and not merely a convenient one: it is what the
guide camera SAW, so a model that matches it is a model standing the way the painting says
this object stands. The alternative -- relating the generator's turntable axes to the
cliff's basis by algebra -- is a calculation with a sign in it that renders perfectly when
it is wrong.

Silhouettes are compared after scaling each to a common box, so this measures SHAPE and not
the sizes, which are set separately and from metres.
"""
import argparse
import json
import pathlib

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
GODOT = HERE.parent / "cliffside3d" / "godot"
PROPS = GODOT / "props"

# model -> (painted sprite, true size in metres, which axis that size is on)
OBJECTS = {
    "post":  ("bridge_post_0",   1.20, "height"),   # the blockout's own post, exactly
    "snag":  ("bridge_obj_01_a", 2.93, "height"),
    "stump": ("bridge_obj_01_c", 0.80, "height"),
    "rope":  ("bridge_obj_02_a", 0.65, "across"),
    "raven": ("raven_perched",   0.28, "height"),
}
# prop instance in props.json -> (model, extra yaw, perch)
INSTANCES = {
    "bridge_obj_01_a": ("snag", 0.0, None),
    "bridge_obj_01_c": ("stump", 0.0, None),
    "bridge_obj_02_a": ("rope", 0.0, None),
    "bridge_post_0": ("post", 0.0, None),
    "bridge_post_1": ("post", 90.0, None),
    "bridge_post_2": ("post", 180.0, None),
    "bridge_post_3": ("post", 270.0, None),
    "raven_perched": ("raven", 0.0, ("bridge_post_3", 1.20)),
}


def mask(p: pathlib.Path, alpha_thresh: int = 128) -> np.ndarray:
    a = np.asarray(Image.open(p).convert("RGBA"))[..., 3] > alpha_thresh
    ys, xs = np.nonzero(a)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def iou_scaled(a: np.ndarray, b: np.ndarray, n: int = 192) -> float:
    def fit(m):
        im = Image.fromarray((m * 255).astype(np.uint8))
        s = n / max(m.shape)
        im = im.resize((max(1, round(m.shape[1] * s)), max(1, round(m.shape[0] * s))),
                       Image.BILINEAR)
        o = np.zeros((n, n), bool)
        q = np.asarray(im) > 127
        y, x = (n - q.shape[0]) // 2, (n - q.shape[1]) // 2
        o[y:y + q.shape[0], x:x + q.shape[1]] = q
        return o

    A, B = fit(a), fit(b)
    u = (A | B).sum()
    return float((A & B).sum() / u) if u else 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", required=True)
    a = ap.parse_args()
    probe = pathlib.Path(a.probe)
    info = json.loads((probe / "props3d_probe.json").read_text())

    models = {}
    for obj, (sprite, size_m, axis) in OBJECTS.items():
        sp = mask(PROPS / "assets" / ("%s.png" % sprite), 40)
        rends = sorted(probe.glob("%s_yaw*.png" % obj))
        if not rends:
            print("%-6s no renders" % obj)
            continue
        scores = []
        for r in rends:
            y = int(r.stem.split("yaw")[1])
            scores.append((iou_scaled(mask(r), sp), y))
        scores.sort(reverse=True)
        best_iou, best_y = scores[0]
        spread = best_iou - scores[-1][0]
        raw = info["models"][obj]["raw_aabb_m"]
        models[obj] = {
            "glb": "res://models/props/%s.glb" % obj,
            "height_m": size_m, "axis": axis, "yaw_deg": float(best_y),
            "matched_sprite": sprite, "match_iou": round(best_iou, 3),
            "iou_spread_over_yaw": round(spread, 3),
            "raw_aabb_m": raw, "tris": info["models"][obj].get("tris"),
        }
        print("%-6s yaw %3d  IoU %.3f vs %-16s  spread over yaw %.3f  raw aabb %s  tris %s"
              % (obj, best_y, best_iou, sprite, spread, raw, info["models"][obj].get("tris")))
        if spread < 0.05:
            print("        (shape is near yaw-invariant -- any yaw is as good; the pick is free)")

    insts = {}
    for name, (m, extra, perch) in INSTANCES.items():
        if m not in models:
            continue
        rec = {"model": m, "yaw_deg": extra}
        if perch:
            rec["perch_on"], rec["perch_height_m"] = perch
        insts[name] = rec

    out = {
        "_what": "C-9 T9-1a: the bridge slice's props as real models, at TRUE scale.",
        "_scale": ("The rail post is the blockout's own 1.20 m (cliffside_blockout.gd:659). "
                   "The others come from the painted sprite divided by 1.457 -- the measured "
                   "ratio between the four painted posts (1.72-1.81 m) and the geometry they "
                   "stand on. The raven does not obey it: 1.457 still leaves a 0.62 m bird, "
                   "so it is scaled from life at 0.28 m."),
        "_yaw": ("Measured, not assumed: probe_props3d.gd renders each model through the "
                 "cliff camera's basis every 15 degrees and 13_normalise.py keeps the yaw "
                 "whose silhouette best matches the painted sprite."),
        "models": models, "instances": insts,
    }
    (GODOT / "data" / "props3d.json").write_text(json.dumps(out, indent=1) + "\n")
    print("-> %s" % (GODOT / "data" / "props3d.json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
