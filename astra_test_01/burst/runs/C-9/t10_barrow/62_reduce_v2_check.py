#!/usr/bin/env python3
"""C-9 T10-1c: prove the re-reduced barrow assets are drop-in, and say what they cost.

    python3 62_reduce_v2_check.py [asset ...]

Three questions, asked of three files each -- the CURRENT file in the Godot project, the
UNREDUCED Tripo build it came from, and the new reduction in reduced_v2/.

1. IS IT DROP-IN? `barrow_assets.json` applies a yaw, a Y stretch and a target size to
   whatever GLB it finds, so a replacement only works if it has the same origin,
   orientation and raw scale as the file it replaces. That is an AABB identity, and it is
   checked as one: min and max corner against the current file, in glTF axes, reported as
   a delta in metres rather than as a yes.

2. WHAT DID THE CRACK COST, AND WHAT DOES THE FIX RECOVER? Open edges -- edges used by
   exactly ONE triangle -- before and after, gandalf's instrument, run on all three files
   so the UNREDUCED build's own count is the floor the fix is measured against. A number
   that only appears for the new file would be a number with nothing to be better than.

3. DID THE FIX COST SILHOUETTE? IoU of the new reduction against the UNREDUCED build
   through the play camera, 12 azimuths at pitch 52.954. Welding before decimating moves
   vertices that the old method could not move, so it is entitled to change the outline;
   this is the measurement that says by how much.
"""
import json
import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
C9 = HERE.parent
GODOT = C9 / "cliffside3d" / "godot" / "models" / "barrow"
V2 = HERE / "reduced_v2"
WORK = HERE / "kit_work" / "v2"
PLAY_PITCH = 52.95354112560294
BARROW = json.loads((C9 / "cliffside3d" / "godot" / "data" /
                     "barrow_assets.json").read_text())["models"]

ASSETS = {
    "stone_tall": HERE / "builds" / "stone_tall.glb",
    "stone_mid": HERE / "builds" / "stone_mid.glb",
    "stone_short": HERE / "builds" / "stone_short.glb",
    "lintel": HERE / "builds" / "lintel.glb",
    "post": HERE / "builds" / "post.glb",
    "rock_large": HERE / "builds" / "rock_large.glb",
    "rock_small": HERE / "builds" / "rock_small.glb",
    "birch": HERE / "builds" / "birch.glb",
    "juniper": HERE / "builds" / "juniper.glb",
    "raven": C9 / "t9_props" / "builds" / "raven.glb",
}


def open_edges(paths):
    r = subprocess.run(["blender", "--background", "--python", str(HERE / "61_open_edges.py"),
                        "--"] + [str(p) for p in paths], check=True, capture_output=True,
                       text=True)
    line = [l for l in r.stdout.splitlines() if l.startswith("[openjson]")][0]
    return {pathlib.Path(d["file"]).name + "|" + str(pathlib.Path(d["file"]).parent.name): d
            for d in json.loads(line[len("[openjson] "):])}


def probe(glb, out):
    if out.exists() and list(out.glob("*_stats.json")):
        return
    out.mkdir(parents=True, exist_ok=True)
    subprocess.run(["blender", "--background", "--python", str(HERE / "54_kit_probe.py"),
                    "--", str(glb), str(out), str(PLAY_PITCH), "30", "512"],
                   check=True, capture_output=True)


def sil(p):
    return np.asarray(Image.open(p).convert("RGBA"))[..., 3] > 128


def iou(a, b, n=256):
    def fit(m):
        ys, xs = np.nonzero(m)
        m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        s = n / max(m.shape)
        q = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).resize(
            (max(1, round(m.shape[1] * s)), max(1, round(m.shape[0] * s))),
            Image.BILINEAR)) > 127
        o = np.zeros((n, n), bool)
        y, x = (n - q.shape[0]) // 2, (n - q.shape[1]) // 2
        o[y:y + q.shape[0], x:x + q.shape[1]] = q
        return o
    A, B = fit(a), fit(b)
    u = (A | B).sum()
    return float((A & B).sum() / u) if u else 0.0


def main() -> int:
    want = sys.argv[1:] or list(ASSETS)
    WORK.mkdir(parents=True, exist_ok=True)
    rows = {}
    for a in want:
        src, cur, new = ASSETS[a], GODOT / ("%s.glb" % a), V2 / ("%s.glb" % a)
        if not new.exists():
            print("%-12s reduced_v2 missing" % a)
            continue
        e = open_edges([cur, src, new])
        ec, es, en = (e["%s.glb|%s" % (a, p)] for p in (cur.parent.name, src.parent.name,
                                                        new.parent.name))
        # THE CURRENT FILE IS PROBED TOO, and that is not thoroughness for its own sake.
        # "The new birch scores 0.9364 against the unreduced build" is a number with nothing
        # to be better than. Welding lets the decimator collapse edges the old method could
        # not touch, so it is entitled to move the outline -- whether that is a gain or a
        # cost is only readable against what the file being replaced scored.
        probe(src, WORK / ("%s_src" % a))
        probe(new, WORK / ("%s_new" % a))
        probe(cur, WORK / ("%s_cur" % a))
        d1 = {int(p.stem.split("az")[1]): p for p in (WORK / ("%s_src" % a)).glob("*_az*.png")}
        d2 = {int(p.stem.split("az")[1]): p for p in (WORK / ("%s_new" % a)).glob("*_az*.png")}
        d3 = {int(p.stem.split("az")[1]): p for p in (WORK / ("%s_cur" % a)).glob("*_az*.png")}
        ks = sorted(set(d1) & set(d2) & set(d3))
        xs = [iou(sil(d1[k]), sil(d2[k])) for k in ks]
        cs = [iou(sil(d1[k]), sil(d3[k])) for k in ks]
        dmin = max(abs(en["aabb_min_gltf"][i] - ec["aabb_min_gltf"][i]) for i in range(3))
        dmax = max(abs(en["aabb_max_gltf"][i] - ec["aabb_max_gltf"][i]) for i in range(3))
        # UNITS. These GLBs sit at Tripo's raw scale -- max dimension 1.0 -- and
        # barrow_assets.json scales them at load. So a corner delta here is in RAW UNITS,
        # not metres, and the first version of this file labelled it "_m". Converted with
        # the asset's own target size so the number that gets quoted is the one that is
        # actually seen in the scene.
        bm_ = BARROW.get(a, {})
        tgt, axis = bm_.get("height_m"), bm_.get("axis", "height")
        raw = en["size_gltf"]
        denom = max(raw[0], raw[2]) if axis == "across" else raw[1]
        if tgt and denom:
            k_ = tgt / denom * (1.660 if bm_.get("pitch_correct") else 1.0)
        else:
            k_ = None
        rows[a] = {
            "source_build": str(src.relative_to(C9)),
            "tris": {"current": ec["tris"], "unreduced": es["tris"], "v2": en["tris"]},
            "open_edges": {"current": ec["open_edges"], "unreduced": es["open_edges"],
                           "v2": en["open_edges"]},
            "pieces": {"current": ec["pieces"], "unreduced": es["pieces"], "v2": en["pieces"]},
            "edges_3plus": {"current": ec["edges_3plus"], "unreduced": es["edges_3plus"],
                            "v2": en["edges_3plus"]},
            "iou_vs_unreduced_play": {"v2_mean": round(float(np.mean(xs)), 4),
                                      "v2_min": round(float(np.min(xs)), 4),
                                      "current_mean": round(float(np.mean(cs)), 4),
                                      "current_min": round(float(np.min(cs)), 4),
                                      "worst_az": int(ks[int(np.argmin(xs))]), "n": len(ks)},
            "aabb_gltf_current": [ec["aabb_min_gltf"], ec["aabb_max_gltf"]],
            "aabb_gltf_v2": [en["aabb_min_gltf"], en["aabb_max_gltf"]],
            "aabb_max_corner_delta_raw_units": {"min_corner": round(dmin, 6),
                                                "max_corner": round(dmax, 6)},
            "aabb_max_corner_delta_scene_mm": (None if k_ is None else
                                               round(max(dmin, dmax) * k_ * 1000, 3)),
            "drop_in": bool(max(dmin, dmax) < 0.005),
        }
        r = rows[a]
        print("%-12s open %6d -> %6d (unreduced %5d) | pieces %5d -> %5d (unreduced %d) | "
              "tris %6d | IoU vs unreduced: v2 %.4f (min %.4f) current %.4f | "
              "AABB delta %.5f raw = %s mm in scene  %s"
              % (a, ec["open_edges"], en["open_edges"], es["open_edges"],
                 ec["pieces"], en["pieces"], es["pieces"], en["tris"],
                 r["iou_vs_unreduced_play"]["v2_mean"], r["iou_vs_unreduced_play"]["v2_min"],
                 r["iou_vs_unreduced_play"]["current_mean"], max(dmin, dmax),
                 r["aabb_max_corner_delta_scene_mm"],
                 "DROP-IN" if r["drop_in"] else "** AABB MOVED **"))
    f = V2 / "reduce_v2_report.json"
    old = json.loads(f.read_text()) if f.exists() else {}
    old.update(rows)
    f.write_text(json.dumps({"_what": "C-9 T10-1c: the nine barrow assets (and the raven) "
                                      "re-reduced with a weld-by-distance pass before the "
                                      "decimate. Open edges are gandalf's instrument: edges "
                                      "used by exactly one triangle, after welding at 1e-5.",
                             "_weld_tolerance": 1e-5,
                             "_drop_in_test": "max AABB corner delta vs the current Godot "
                                              "file < 0.005 in the GLB's own RAW units "
                                              "(Tripo normalises the max dimension to 1.0); "
                                              "the scene-millimetre column applies each "
                                              "asset's own target size and Y stretch from "
                                              "barrow_assets.json.",
                             "assets": old.get("assets", {}) | rows}, indent=1) + "\n")
    print("-> %s" % f)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
