#!/usr/bin/env python3
"""BV2F LV Phase 1'' (R-C9-206): MEASURE the cave-arch build's own mouth -- rays straight into its FRONT (+Z -> -Z) on a
5 cm grid; a ray that runs more than DEEP m into the piece before it meets rock is in the mouth. Reports the mouth's clear
width, its clear height above its floor, the floor height and the depth reached, as fractions of the build's AABB, so
make_bv2art.py scales the piece for a 7 m mouth (ONE uniform scale).   -> fid/lv/kit2/cave_mouth.json (+ a depth map png)
    python3 fid/lv/tools/lv_kit2_measure.py"""
import json, os, struct
import numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__)); LV = os.path.dirname(HERE)
GLB = os.path.normpath(os.path.join(LV, "..", "..", "..", "barrow_full", "godot", "data", "bv2f", "models", "cavearch.glb"))
DEEP = 1.5


def load(p):
    b = open(p, "rb").read()
    n = struct.unpack("<I", b[12:16])[0]
    J = json.loads(b[20:20 + n]); off = 20 + n
    bl = struct.unpack("<I", b[off:off + 4])[0]; B = b[off + 8:off + 8 + bl]
    tris = []
    for node in J["nodes"]:
        if "mesh" not in node:
            continue
        for pr in J["meshes"][node["mesh"]]["primitives"]:
            a = J["accessors"][pr["attributes"]["POSITION"]]; bv = J["bufferViews"][a["bufferView"]]
            P = np.frombuffer(B, "<f4", a["count"] * 3, bv.get("byteOffset", 0) + a.get("byteOffset", 0)).reshape(-1, 3)
            if "translation" in node or "scale" in node:
                P = P * np.array(node.get("scale", [1, 1, 1])) + np.array(node.get("translation", [0, 0, 0]))
            ia = J["accessors"][pr["indices"]]; ibv = J["bufferViews"][ia["bufferView"]]
            dt = {5125: "<u4", 5123: "<u2"}[ia["componentType"]]
            I = np.frombuffer(B, dt, ia["count"], ibv.get("byteOffset", 0) + ia.get("byteOffset", 0)).reshape(-1, 3)
            tris.append(P[I])
    return np.concatenate(tris)


T = load(GLB).astype(np.float64)
lo, hi = T.reshape(-1, 3).min(0), T.reshape(-1, 3).max(0)
step = 0.05
xs = np.arange(lo[0], hi[0], step); ys = np.arange(lo[1], hi[1], step)
depth = np.full((len(ys), len(xs)), np.inf)
z0 = hi[2] + 1.0
v0, v1, v2 = T[:, 0], T[:, 1], T[:, 2]
e1, e2 = v1 - v0, v2 - v0
# ray dir (0, 0, -1): Moller-Trumbore with d = -z; per ray, test only triangles whose xy-bbox holds it
tx0 = T[:, :, 0].min(1); tx1 = T[:, :, 0].max(1); ty0 = T[:, :, 1].min(1); ty1 = T[:, :, 1].max(1)
d = np.array([0.0, 0.0, -1.0])
for j, y in enumerate(ys):
    rowsel = (ty0 <= y) & (ty1 >= y)
    if not rowsel.any():
        continue
    E1, E2, V0 = e1[rowsel], e2[rowsel], v0[rowsel]
    X0, X1 = tx0[rowsel], tx1[rowsel]
    pv = np.cross(d, E2); det = (E1 * pv).sum(1)
    for i, x in enumerate(xs):
        sel = (X0 <= x) & (X1 >= x) & (np.abs(det) > 1e-12)
        if not sel.any():
            continue
        o = np.array([x, y, z0])
        tv = o - V0[sel]; inv = 1.0 / det[sel]
        u = (tv * pv[sel]).sum(1) * inv
        q = np.cross(tv, E1[sel]); v = (q * d).sum(1) * inv
        t = (q * E2[sel]).sum(1) * inv
        ok = (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 0)
        if ok.any():
            depth[j, i] = t[ok].min() - 1.0          # metres behind the front plane (z = hi[2])
D = np.where(np.isinf(depth), np.nan, depth)
mouth = np.nan_to_num(D, nan=0.0) > DEEP
# THE MOUTH, in the vertical slice dz behind the front: a point (x, y) of that slice is OPEN when the ray from the front at
# (x, y) runs deeper than dz (it met no rock before the slice). Column by column, from the lowest open cell up, the first
# open run with ROCK ABOVE it is the arch's clear height there (a run reaching the top is the set-back crest, not a mouth).
H = hi[1] - lo[1]
prof = {}
best = np.zeros(D.shape, bool)
for dz in (0.5, 1.0, 1.5, 2.5):
    deep = np.nan_to_num(D, nan=0.0) > dz
    rock = ~np.isnan(D) & ~deep
    runs = {}
    for i in range(len(xs)):
        col = deep[:, i]
        j = 0
        while j < len(ys) and not col[j]:
            j += 1
        if j >= len(ys) or j * step > 0.3 * H:
            continue
        k = j
        while k < len(ys) and col[k]:
            k += 1
        if k < len(ys) and rock[k:, i].any():
            runs[i] = (j, k)
    if not runs:
        prof[dz] = {"clear_h_m": 0.0}
        continue
    hts = {i: (k - j) * step for i, (j, k) in runs.items()}
    ic = max(hts, key=hts.get)
    ch = hts[ic]
    cols = [i for i in sorted(hts) if abs(i - ic) * step < 6.0]
    prof[dz] = {"clear_h_m": round(ch, 3), "floor_m": round(runs[ic][0] * step, 3), "apex_x_frac": round(ic * step / (hi[0] - lo[0]), 4),
                "width_at_2m_m": round(sum(1 for i in cols if hts[i] >= 2.0) * step, 3), "width_at_half_m": round(sum(1 for i in cols if hts[i] >= ch / 2) * step, 3)}
    if dz == 1.0:
        for i, (j, k) in runs.items():
            best[j:k, i] = True
m = prof[1.0]
res = {"_what": __doc__.split("\n")[0], "glb": os.path.relpath(GLB, LV), "aabb_m": [float(x) for x in (hi - lo)],
       "method": "front rays on a 5 cm grid; the slice dz behind the front is open where a ray runs deeper than dz; per column the first open run with rock above = the clear height",
       "profile_by_slice_m": {str(k): v for k, v in prof.items()}, "mouth_clear_h_m": m["clear_h_m"], "mouth_width_at_2m_m": m["width_at_2m_m"],
       "floor_frac": round(m["floor_m"] / H, 4), "mouth_h_frac": round(m["clear_h_m"] / H, 4), "apex_x_frac": m["apex_x_frac"],
       "front_view_max_depth_m": round(float(np.nanmax(D)), 3)}
os.makedirs(os.path.join(LV, "kit2"), exist_ok=True)
json.dump(res, open(os.path.join(LV, "kit2", "cave_mouth.json"), "w"), indent=1)
img = np.clip(np.nan_to_num(D, nan=-1) / max(1e-6, np.nanmax(D)), 0, 1)
rgb = (np.dstack([img, img, img]) * 255).astype(np.uint8)
rgb[best] = [255, 0, 255]
Image.fromarray(rgb[::-1]).save(os.path.join(LV, "kit2", "cave_mouth_depth.png"))
print(res)
