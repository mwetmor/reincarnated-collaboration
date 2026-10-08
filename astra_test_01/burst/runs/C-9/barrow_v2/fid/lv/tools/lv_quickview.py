#!/usr/bin/env python3
"""BV2F LV (R-C9-226): a QUICK software view of the art level -- no Godot, no lock -- for iterating on the composition:
the terrain (drawn classes), the carved section (per-class meshes) and every slab, flat-shaded in class tints (one sun,
upper-left), painter-sorted, in the PLAY camera's projection (pitch 52.95, screen up = +v; y = v sin p + z cos p) or straight
down. A check drawing only; the stills of record come from Godot.
    python3 lv_quickview.py u0 v0 u1 v1 [--ppm 24] [--top] [--out name.png]"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
LV = os.path.dirname(HERE)
BF = os.path.normpath(os.path.join(LV, "..", "..", "..", "barrow_full", "godot", "data", "bv2f", "art"))
a = sys.argv[1:]
u0, v0, u1, v1 = map(float, a[:4])
ppm = float(a[a.index("--ppm") + 1]) if "--ppm" in a else 24.0
top = "--top" in a
out = a[a.index("--out") + 1] if "--out" in a else "quickview.png"
P_ = math.radians(52.95354112560294)
SP, CP = (1.0, 0.0) if top else (math.sin(P_), math.cos(P_))
L = json.load(open(os.path.join(BF, "level.json")))
sim = L["sim"]
tint = L["tints_srgb"]
names = L["classes"]


def col(n):
    t = tint.get(n, "#ff00ff")
    if isinstance(t, str):
        return np.array([int(t[1:3], 16), int(t[3:5], 16), int(t[5:7], 16)], float)
    return np.array([255 * c for c in t[:3]], float)


SUN = np.array([-0.45, 0.35, 0.82])
SUN /= np.linalg.norm(SUN)
tris, cols = [], []


def add(T, cname):
    """T: (M, 3, 3) in (u, v, z)"""
    if len(T) == 0:
        return
    keep = (T[..., 0].max(1) > u0 - 2) & (T[..., 0].min(1) < u1 + 2) & (T[..., 1].max(1) > v0 - 6) & (T[..., 1].min(1) < v1 + 6)
    T = T[keep]
    n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    n = np.where(n[:, 2:3] < 0, -n, n) if cname not in ("rock", "wet_rock", "rime", "passage_dark") else n
    lam = np.clip(0.55 + 0.6 * np.abs(n @ SUN), 0.35, 1.25)
    c = col(cname)
    tris.append(T)
    cols.append(np.clip(c[None, :] * lam[:, None], 0, 255))


# terrain (drawn classes only), two triangles per cell, the class of the cell's centre
hf = sim["heightfield"]
H, W = hf["shape"]
ex = hf["extent_sim_m"]
hp = hf["px_per_m"]
Z = np.fromfile(os.path.join(BF, hf["file"]), "<f4").reshape(H, W)
C = np.asarray(Image.open(os.path.join(BF, "classes.png")))
cp = sim["classes_png"]["px_per_m"]
us = ex["x0"] + np.arange(W) / hp
vs = -(ex["y0"] + np.arange(H) / hp)
i0, i1 = max(0, int((u0 - 2 - ex["x0"]) * hp)), min(W - 1, int((u1 + 2 - ex["x0"]) * hp))
j0, j1 = max(0, int((-(v1 + 6) - ex["y0"]) * hp)), min(H - 1, int((-(v0 - 6) - ex["y0"]) * hp))
for j in range(j0, j1):
    for i in range(i0, i1):
        cu, cv = us[i] + 0.5 / hp, vs[j] - 0.5 / hp
        ci = int((cu - ex["x0"]) * cp)
        cj = int((-cv - ex["y0"]) * cp)
        if not (0 <= cj < C.shape[0] and 0 <= ci < C.shape[1]):
            continue
        k = int(C[cj, ci])
        if k == 0:
            continue
        p00 = (us[i], vs[j], Z[j, i]); p10 = (us[i + 1], vs[j], Z[j, i + 1]); p01 = (us[i], vs[j + 1], Z[j + 1, i]); p11 = (us[i + 1], vs[j + 1], Z[j + 1, i + 1])
        add(np.array([[p00, p10, p11], [p00, p11, p01]]), names[k])
# the sea plane
sz = sim["sea_z"]
sq_ = []
for gu in np.arange(u0 - 3, u1 + 3, 1.0):
    for gv in np.arange(v0 - 8, v1 + 8, 1.0):
        sq_ += [[(gu, gv, sz), (gu + 1, gv, sz), (gu + 1, gv + 1, sz)], [(gu, gv, sz), (gu + 1, gv + 1, sz), (gu, gv + 1, sz)]]
add(np.array(sq_), "sea")
# the carved section
for cname, ent in sim.get("carved", {}).get("files", {}).items():
    raw = np.fromfile(os.path.join(BF, ent["file"]), "<f4").reshape(-1, 6)[:, :3].reshape(-1, 3, 3)
    add(np.stack([raw[..., 0], -raw[..., 2], raw[..., 1]], axis=-1).astype(float), cname)
# slabs: top + sides
for gid, g in sim.get("slabs", {}).items():
    T = []
    for it in g["items"]:
        p = [(q[0], -q[1]) for q in it["poly"]]
        z0, z1 = it["z0"], it["z1"]
        c = (sum(q[0] for q in p) / len(p), sum(q[1] for q in p) / len(p))
        for k in range(len(p)):
            a_, b_ = p[k], p[(k + 1) % len(p)]
            T.append([(c[0], c[1], z1), (a_[0], a_[1], z1), (b_[0], b_[1], z1)])
            T.append([(a_[0], a_[1], z0), (b_[0], b_[1], z0), (b_[0], b_[1], z1)])
            T.append([(a_[0], a_[1], z0), (b_[0], b_[1], z1), (a_[0], a_[1], z1)])
    add(np.array(T, float), g["class"])
T = np.concatenate(tris)
CC = np.concatenate(cols)
depth = (T[..., 1].mean(1) * CP - T[..., 2].mean(1) * SP) if not top else T[..., 2].mean(1) * -1
order = np.argsort(-depth) if not top else np.argsort(-depth)
Wp, Hp = int((u1 - u0) * ppm), int((v1 - v0) * SP * ppm + 6 * CP * ppm)
im = Image.new("RGB", (Wp, Hp), (20, 30, 50))
d = ImageDraw.Draw(im)
yt = v1 * SP + 2.0 * CP
for k in order:
    t = T[k]
    pts = [((q[0] - u0) * ppm, (yt - (q[1] * SP + q[2] * CP)) * ppm) for q in t]
    c = tuple(int(x) for x in CC[k])
    d.polygon(pts, fill=c, outline=c)
im.save(os.path.join(LV, "M1pp", out))
print(os.path.join(LV, "M1pp", out), im.size, len(T))
