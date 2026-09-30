#!/usr/bin/env python3
"""C-9 T10-2 step 4 (B): DATA FILES ONLY, wired into nothing that ships. drax.

    python3 tools/heather_instances.py [--seed 7]

1. THE HEATHER, as MultiMesh instances placed FROM the painted tufts (take/masks/density_uv.png:
   R heather cover, G shrub cover, per 0.1 m of ground). Candidates on a 0.15 m jittered grid are
   kept with probability  cover x (0.15 m)^2 / (instance SCREEN footprint), so the instances cover the
   ground the painting covered -- no more, which is what keeps the level from showing heather
   twice -- then thinned so no two stand closer than 0.6 of a diameter. Heather: a 0.30 m spray
   (the painted single tufts measure 0.19 m median, and a patch is several). Shrub: a 0.45 m
   clump (the painting's dark juniper). Sprays face the fixed camera, so heather has no yaw;
   shrubs are 3D models and take a seeded yaw.
   -> take/build/heather_instances.json : per instance [u, v, x, z, diameter_m, yaw_deg], by class
2. THE GROUND MATERIAL'S INPUT: take/ground/splat_world.png as the blockout ground shader reads
   its splat -- PNG bytes in a .bin, the SAME encoding and frame as godot/data/barrow_full_splat.bin
   (RGBA8, R path, G rock, B shrub, A ice, snow = 1 - sum; world xz, 70 m at 0.05 m/px).
   -> take/build/barrow_full_splat_painted.bin, and its sha256 in the report. To wire it (NOT
   done here): replace godot/data/barrow_full_splat.bin and set the layout's regions.splat.sha256.
"""
import hashlib, io, json, math, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
BF = os.path.dirname(HERE)
a = sys.argv[1:]
SEED = int(a[a.index("--seed") + 1]) if "--seed" in a else 7
L = json.load(open(os.path.join(BF, "barrow_full_layout.json")))
TM = json.load(open(os.path.join(BF, "take", "masks", "tufts.json")))
U0, U1 = TM["frame"]["u"]
V0, V1 = TM["frame"]["v"]
RES = float(TM["frame"]["px_per_m"])
YAW = math.radians(float(L["frame"]["camera"]["yaw_deg"]))
U_HAT = np.array([math.cos(YAW), 0.0, -math.sin(YAW)])
V_HAT = np.array([-math.sin(YAW), 0.0, -math.cos(YAW)])
STEP = 0.15
KINDS = {"heather": {"channel": 0, "diameter_m": 0.30, "height_m": 0.30, "yaw": False},
         "shrub": {"channel": 1, "diameter_m": 0.45, "height_m": 0.35, "yaw": True}}
PITCH = math.radians(float(L["frame"]["camera"]["pitch_deg"]))
# THE COVER IS SCREEN AREA, set on the ground: density_uv counts painted PIXELS at 1 / (px per m
# across x px per ground m up) each. An instance's share of that is its SCREEN footprint in the
# same units -- its width x (its height x cos/sin(pitch) + its depth) -- not its ground disc: a
# 0.30 m spray shows 0.158 of them against a 0.071 m^2 disc, and counting discs put 2.2x the
# painted heather on the ground.
H_OVER_V = math.cos(PITCH) / math.sin(PITCH)


def main():
    rng = np.random.default_rng(SEED)
    D = np.asarray(Image.open(os.path.join(BF, "take", "masks", "density_uv.png"))).astype(np.float32) / 255.0
    gv, gu = D.shape[:2]
    out = {"_what": "C-9 T10-2 step 4 (B): heather MultiMesh instances placed FROM the painted tufts -- data only, wired into nothing",
           "frame": {"u": [U0, U1], "v": [V0, V1], "world_from_uv": L["frame"]["world_from_uv"],
                     "columns": ["u", "v", "x", "z", "diameter_m", "yaw_deg"],
                     "_y": "every instance stands on the flat floor, y = 0"},
           "seed": SEED, "classes": {}}
    for name, k in KINDS.items():
        cov = ndimage.uniform_filter(D[..., k["channel"]], size=3)          # ~0.3 m, the sampling scale
        area_i = k["diameter_m"] * (k["height_m"] * H_OVER_V + k["diameter_m"])
        us = np.arange(U0 + STEP / 2, U1, STEP)
        vs = np.arange(V0 + STEP / 2, V1, STEP)
        UU, VV = np.meshgrid(us, vs)
        UU = UU + rng.uniform(-0.5, 0.5, UU.shape) * STEP
        VV = VV + rng.uniform(-0.5, 0.5, VV.shape) * STEP
        ci = np.clip(((UU - U0) * RES).astype(int), 0, gu - 1)
        cj = np.clip(((V1 - VV) * RES).astype(int), 0, gv - 1)
        p = np.clip(cov[cj, ci] * STEP ** 2 / area_i, 0.0, 1.0)
        keep = rng.random(p.shape) < p
        pts = np.stack([UU[keep], VV[keep]], 1)
        # thin: greedy, in a seeded random order, no two closer than 0.6 of a diameter
        order = rng.permutation(len(pts))
        pts = pts[order]
        tree = cKDTree(pts)
        alive = np.ones(len(pts), bool)
        for i in range(len(pts)):
            if not alive[i]:
                continue
            for j in tree.query_ball_point(pts[i], 0.6 * k["diameter_m"]):
                if j > i:
                    alive[j] = False
        pts = pts[alive]
        xz = pts[:, :1] * U_HAT[[0, 2]] + pts[:, 1:] * V_HAT[[0, 2]]
        yaw = rng.uniform(0, 360, len(pts)) if k["yaw"] else np.zeros(len(pts))
        inst = np.column_stack([pts, xz, np.full(len(pts), k["diameter_m"]), yaw])
        painted_m2 = float(D[..., k["channel"]].sum()) / RES ** 2
        placed_m2 = len(pts) * area_i
        out["classes"][name] = {"count": int(len(pts)), "diameter_m": k["diameter_m"], "height_m": k["height_m"],
                                "painted_cover_screen_m2": round(painted_m2, 2),
                                "instances_screen_m2": round(placed_m2, 2),
                                "instances": np.round(inst, 4).tolist()}
        print("%-7s %4d instances, %.1f m^2 of screen footprint for %.1f m^2 of painted cover"
              % (name, len(pts), placed_m2, painted_m2))
    os.makedirs(os.path.join(BF, "take", "build"), exist_ok=True)
    json.dump(out, open(os.path.join(BF, "take", "build", "heather_instances.json"), "w"))
    # ---- the ground material's input --------------------------------------------------
    im = Image.open(os.path.join(BF, "take", "ground", "splat_world.png")).convert("RGBA")
    buf = io.BytesIO()
    im.save(buf, "PNG")
    b = buf.getvalue()
    open(os.path.join(BF, "take", "build", "barrow_full_splat_painted.bin"), "wb").write(b)
    sha = hashlib.sha256(b).hexdigest()
    old = open(os.path.join(BF, "godot", "data", "barrow_full_splat.bin"), "rb").read()
    rep = {"file": "take/build/barrow_full_splat_painted.bin", "sha256": sha, "bytes": len(b),
           "replaces": "godot/data/barrow_full_splat.bin (sha256 %s) -- NOT replaced" % hashlib.sha256(old).hexdigest(),
           "to_wire": "copy over godot/data/barrow_full_splat.bin and set barrow_full_layout.json regions.splat.sha256 to the new sha256 (the scene checks it at load)"}
    json.dump({"heather": {k: {kk: vv for kk, vv in v.items() if kk != "instances"} for k, v in out["classes"].items()},
               "ground_splat": rep}, open(os.path.join(BF, "take", "build", "data_report.json"), "w"), indent=1)
    print("ground splat: %s  sha256 %s" % (rep["file"], sha[:16]))


if __name__ == "__main__":
    main()
