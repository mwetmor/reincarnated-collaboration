#!/usr/bin/env python3
"""C-9 T10: the barrow's scene data -- every instance, placed, for BOTH heightfields.

    python3 36_scene_data.py

Writes `barrow_scene_a.json`: a flat list of instances, each with the asset to use, its
position in the SCENE's frame, its true height in metres and a yaw. The render stack reads
it; nothing here builds or lights anything.

THE FRAME CHANGE IS THE WHOLE JOB AND IT IS WHERE THIS WOULD SILENTLY GO WRONG. Three
coordinate systems meet:

  1. the UNPROJECTION frame, in which 23_objects.py solved every object's ground contact;
  2. each heightfield's GRID, whose origin is wherever its own point cloud's min corner
     happened to fall -- and the two heightfields have DIFFERENT origins;
  3. the SCENE, where BarrowStandIn puts the barrow at (0, -4).

So a position is only meaningful with all three named. scene_xz = (world_xz - grid_origin)
+ (MOUND_CENTRE - mound_centre_in_grid). Both heightfields are emitted, because their grid
origins differ by about 0.5 m and quietly using one object list against the other
heightfield would drop every prop half a metre off its own footprint -- which looks like a
placement bug in someone else's code.

SCALE IS SET PER INSTANCE FROM ITS OWN MEASUREMENT, not from the asset's nominal size: the
four standing stones are 2.71, 2.71, 2.12 and 1.24 m and they are three different models,
so each instance carries the height it was measured at and the asset is scaled to it. There
is also one global `stone_scale` multiplier, per Matt's note, so "make the stones taller"
is a one-number change rather than a re-derivation.
"""
from __future__ import annotations

import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
MOUND_CENTRE = (0.0, -4.0)          # matches BarrowStandIn and barrow_heightfield.gd
STONE_SCALE = 1.0                   # Matt's one-number lever: 1.37 would make them 2x him


def asset_for(o: dict) -> tuple[str, str] | None:
    c, h, w = o["class"], o["height_m"], o["width_m"]
    if c == "standing_stones":
        if h >= 2.45:
            return "stone_tall", "tripo"
        return ("stone_mid", "tripo") if h >= 1.7 else ("stone_short", "tripo")
    if c == "barrow_door":
        return ("lintel", "tripo") if w > 1.5 * h else ("post", "tripo")
    if c == "rock_outcrop":
        return ("rock_large", "tripo") if h >= 1.0 else ("rock_small", "tripo")
    if c == "heather":
        # the concept has heather AND juniper; only juniper was built, so heather clumps
        # take the juniper model at their own measured size. Named here rather than hidden:
        # if the difference reads at the play camera it needs its own sheet.
        return "juniper", "tripo"
    return None


def main() -> int:
    objs = json.loads((OUT / "objects_a.json").read_text())
    plates = json.loads((HERE / "asset_plates.json").read_text())
    out = {"variant": "a", "px_per_metre": objs["px_per_metre"],
           "mound_centre_scene_xz": list(MOUND_CENTRE),
           "stone_scale": STONE_SCALE,
           "assets": {k: {"height_m": v["height_m"], "width_m": v["width_m"]}
                      for k, v in plates["assets"].items()},
           "frames": {}, "instances": {}}

    for hf_name in ("height_a_marigold", "height_a_authored"):
        p = OUT / (hf_name + ".json")
        if not p.exists():
            continue
        j = json.loads(p.read_text())
        gx0, gz0 = j["png"].get("world_origin_xz", [0.0, 0.0])
        mc = j.get("mound", {}).get("centre_xz", [0.0, 0.0])
        offx = MOUND_CENTRE[0] - mc[0]
        offz = MOUND_CENTRE[1] - mc[1]
        out["frames"][hf_name] = {"grid_origin_xz": [gx0, gz0],
                                  "mound_centre_in_grid_xz": mc,
                                  "scene_offset_xz": [round(offx, 3), round(offz, 3)],
                                  "formula": "scene = (world - grid_origin) + scene_offset"}
        inst = []
        for o in objs["objects"]:
            a = asset_for(o)
            if a is None:
                continue
            name, src = a
            sx = (o["world_xz"][0] - gx0) + offx
            sz = (o["world_xz"][1] - gz0) + offz
            h = o["height_m"]
            if o["class"] == "standing_stones":
                h *= STONE_SCALE
            inst.append({"asset": name, "source": src,
                         "scene_xz": [round(sx, 3), round(sz, 3)],
                         "height_m": round(h, 3),
                         "measured_class": o["class"],
                         "yaw_deg": o.get("yaw_deg")})
        # THE BIRCHES COME FROM THE PROMPTED MASK, not from SAM2 -- SAM2's 68 automatic
        # proposals never isolated one (best overlap 0.00), so a scene built from the
        # object list alone would have had no trees in it at all. Their ground contact is
        # solved the same way every other object's was.
        import numpy as np
        from PIL import Image
        from scipy import ndimage
        tp = HERE / "work" / "evf_a_trees.png"
        if tp.exists():
            tm = np.asarray(Image.open(tp).convert("L")) > 127
            lab, n = ndimage.label(tm)
            K = objs["px_per_metre"]
            R = (0.681998491287231, -0.731353580951691)
            U = (-0.583728015422821, -0.54433536529541)
            F = (-0.440612882375717, -0.410878270864487)
            SIN_P, COS_P = 0.798147439956665, 0.602462172508240
            for i in range(1, n + 1):
                m = lab == i
                if m.sum() < 300:
                    continue
                ys, xs = np.nonzero(m)
                bh = ys.max() - ys.min() + 1
                base = ys >= ys.max() - max(2, int(bh * 0.03))
                bx, by = float(xs[base].mean()), float(ys[base].mean())
                uu = (bx - 1536 / 2.0) / K
                vv = -(by - 1024 / 2.0) / K
                DD = (COS_P * vv) / SIN_P
                wx = R[0] * uu + U[0] * vv + F[0] * DD
                wz = R[1] * uu + U[1] * vv + F[1] * DD
                inst.append({"asset": "birch", "source": "tripo_or_procedural",
                             "scene_xz": [round((wx - gx0) + offx, 3),
                                          round((wz - gz0) + offz, 3)],
                             "height_m": round(bh / (K * COS_P), 2),
                             "measured_class": "birch (evf mask; SAM2 never found one)",
                             "yaw_deg": None})
        inst.append({"asset": "raven", "source": "t9_reuse",
                     "glb": "runs/C-9/t9_props/reduced/raven.glb",
                     "height_m": 0.28, "perch_on_tallest_stone": True,
                     "note": "the T9 build; perch height comes from the stone it sits on"})
        out["instances"][hf_name] = inst
        counts = {}
        for i in inst:
            counts[i["asset"]] = counts.get(i["asset"], 0) + 1
        print("%-20s offset (%.2f, %.2f)  %d instances  %s"
              % (hf_name, offx, offz, len(inst), counts))

    (OUT / "barrow_scene_a.json").write_text(json.dumps(out, indent=1) + "\n")
    print("-> %s" % (OUT / "barrow_scene_a.json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
