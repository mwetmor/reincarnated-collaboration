#!/usr/bin/env python3
"""C-9 T10-1d: what the re-reduction actually costs the frame, counted per INSTANCE.

    python3 64_scene_budget.py

A per-asset triangle budget is not a scene budget, and on this scene the difference is the
whole argument. barrow_scene_a.json places 70 props, and they are not evenly spread:

    rock_small  27 instances       birch  11 instances       everything else  1 to 4

So rock_small is 52% of the scene's triangles and birch is 21% -- together three quarters
of it -- while stone_mid, which gets the same budget in a per-asset table, is 2%. A gate
applied per asset spends the same on a prop placed once as on a prop placed 27 times.

That matters for the birch specifically. It is the one asset whose silhouette does not
survive decimation (bare twigs: every collapse eats one), so it is the one asking for MORE
triangles -- and it is also the one multiplied by eleven. Each 10k of birch budget costs
110k scene triangles; each 10k of stone_mid budget costs 10k. This file prints both columns
so the trade is made on the second one.
"""
import collections
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
C9 = HERE.parent
SCENE = C9 / "cliffside3d" / "godot" / "data" / "barrow_scene_a.json"
LADDER = HERE / "kit_work" / "ladder" / "tri_ladder.json"
# what is in the Godot project today
CURRENT = {"stone_tall": 24000, "stone_mid": 24000, "stone_short": 23998, "lintel": 23999,
           "post": 24000, "rock_large": 24000, "rock_small": 23999, "birch": 23999,
           "juniper": 24000, "raven": 30000, "heather": 272}


def main() -> None:
    inst = json.loads(SCENE.read_text())["instances"]["height_a_authored"]
    n = collections.Counter(i["asset"] for i in inst)
    lad = json.loads(LADDER.read_text()) if LADDER.exists() else {}
    rows, tc, tn = [], 0, 0
    for a, k in n.most_common():
        cur = CURRENT.get(a)
        if cur is None:
            rows.append((a, k, None, None, None, None, None))
            continue
        r = lad.get(a)
        new = r["picked_tris"] if r else cur
        iou = (r["curve"][str(new)]["mean"] if r else None)
        tc += k * cur
        tn += k * new
        rows.append((a, k, cur, new, k * cur, k * new, iou))
    print("%-12s %4s %8s %8s %12s %12s %9s %8s"
          % ("asset", "n", "cur", "new", "scene cur", "scene new", "IoU", "saved"))
    for a, k, cur, new, sc, sn, iou in rows:
        if cur is None:
            print("%-12s %4d   (procedural / not in the reduce set)" % (a, k))
            continue
        print("%-12s %4d %8d %8d %12d %12d %9s %8d"
              % (a, k, cur, new, sc, sn, ("%.4f" % iou) if iou else "-", sc - sn))
    print("%-12s %4d %8s %8s %12d %12d %9s %8d  (%.0f%% of the prop triangles)"
          % ("TOTAL", sum(n.values()), "", "", tc, tn, "", tc - tn,
             100.0 * (tc - tn) / max(tc, 1)))
    out = HERE / "reduced_v2" / "scene_budget.json"
    out.write_text(json.dumps(
        {"_what": "C-9 T10-1d: prop triangles in barrow_scene_a.json (height_a_authored, "
                  "70 instances) before and after the welded re-reduction, counted per "
                  "instance rather than per asset.",
         "instances": dict(n), "current_total": tc, "new_total": tn,
         "rows": [{"asset": a, "instances": k, "tris_current": c, "tris_new": nw,
                   "scene_current": sc, "scene_new": sn, "iou_vs_unreduced": io}
                  for a, k, c, nw, sc, sn, io in rows if c is not None]}, indent=1) + "\n")
    print("-> %s" % out)


if __name__ == "__main__":
    main()
