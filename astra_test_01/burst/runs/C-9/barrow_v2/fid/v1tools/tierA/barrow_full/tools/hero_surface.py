#!/usr/bin/env python3
"""C-9 T10-2 step 4 (B): the SURFACE FILE for baking a hero's plate onto its own model -- the
same arrays nb_t8/scripts/t5_06a_surface.py writes, built from the mesh exactly as the blockout
places it (godot/tools/export_hero_meshes.gd, world space). drax.

    python3 tools/hero_surface.py [--size 1024] [--only id,id]

Per real-model hero it writes, under work/ (the bake's ROOT/work, t5_06b_bake.py's convention):
  surf_<id>.npz                 tex_tri, tex_pos, tex_nrm, uv_area, V, TRI, size, vis_<id>_guide
  layout_<id>.json              ONE cell, "guide": the plate's camera (take/plates/plates.json)
  _cells_<id>/cell_guide.png    the plate itself: its alpha is the bake's matte

WHY NOT t5_06a ITSELF: it runs in Blender on the GLB's own frame. Blender's glTF import turns the
axes (Y-up to Z-up), and the hero's world transform -- a yawed root over a NON-UNIFORM fit scale --
lives in the Godot scene, not in the file. Everything below is 06a's arithmetic, in Godot's world
frame, on the placed mesh. Two differences, both stated:
  UV    Godot's v runs down; 06a reads Blender's (v up) and 06b flips its output to match. So v is
        flipped here, and 06b runs byte-identical.
  VIS   06a ray-casts each triangle's centroid toward the camera through a BVH. Here the same
        question is answered by an orthographic depth buffer at 4x the painting's pixels: a
        triangle is seen if it faces the camera (n . view > 0.05, 06a's own threshold) and its
        centroid is the nearest surface at its pixel. Other pieces are not in this file; what
        they hide is taken out by the matte, which is the ID render's own silhouette.
"""
import json, os, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BF = os.path.dirname(HERE)
a = sys.argv[1:]
SIZE = int(a[a.index("--size") + 1]) if "--size" in a else 1024
ONLY = a[a.index("--only") + 1].split(",") if "--only" in a else None
MESH = os.path.join(BF, "work", "meshes")
WORK = os.path.join(BF, "work")
PL = json.load(open(os.path.join(BF, "take", "plates", "plates.json")))
SS = 4                                         # depth-buffer px per painting px


def load(id_):
    h = json.load(open(os.path.join(MESH, id_ + ".json")))
    V = np.fromfile(os.path.join(MESH, id_ + "_V.f32"), np.float32).reshape(-1, 3).astype(np.float64)
    N = np.fromfile(os.path.join(MESH, id_ + "_N.f32"), np.float32).reshape(-1, 3).astype(np.float64)
    UV = np.fromfile(os.path.join(MESH, id_ + "_UV.f32"), np.float32).reshape(-1, 2).astype(np.float64)
    I = np.fromfile(os.path.join(MESH, id_ + "_I.i32"), np.int32).reshape(-1, 3).astype(np.int64)
    return h, V, N, UV, I


def surface(id_):
    h, V, NV, UVg, TRI = load(id_)
    NV /= np.maximum(np.linalg.norm(NV, axis=1)[:, None], 1e-12)
    TUV = np.stack([UVg[:, 0], 1.0 - UVg[:, 1]], 1)[TRI]          # Blender's v, as 06b expects
    TP = TUV * np.array([SIZE, SIZE])
    tex_pos = np.zeros((SIZE, SIZE, 3), np.float32)
    tex_nrm = np.zeros((SIZE, SIZE, 3), np.float32)
    tex_tri = np.full((SIZE, SIZE), -1, np.int64)
    A3, B3, C3 = V[TRI[:, 0]], V[TRI[:, 1]], V[TRI[:, 2]]
    NA, NB, NC = NV[TRI[:, 0]], NV[TRI[:, 1]], NV[TRI[:, 2]]
    for i in range(len(TRI)):                   # 06a's raster, verbatim in effect
        p = TP[i]
        x0 = max(int(np.floor(p[:, 0].min())), 0); x1 = min(int(np.ceil(p[:, 0].max())) + 1, SIZE)
        y0 = max(int(np.floor(p[:, 1].min())), 0); y1 = min(int(np.ceil(p[:, 1].max())) + 1, SIZE)
        if x1 <= x0 or y1 <= y0:
            continue
        X, Y = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
        d = ((p[1, 1] - p[2, 1]) * (p[0, 0] - p[2, 0]) + (p[2, 0] - p[1, 0]) * (p[0, 1] - p[2, 1]))
        if abs(d) < 1e-12:
            continue
        l0 = ((p[1, 1] - p[2, 1]) * (X - p[2, 0]) + (p[2, 0] - p[1, 0]) * (Y - p[2, 1])) / d
        l1 = ((p[2, 1] - p[0, 1]) * (X - p[2, 0]) + (p[0, 0] - p[2, 0]) * (Y - p[2, 1])) / d
        l2 = 1.0 - l0 - l1
        m = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
        if not m.any():
            continue
        yy, xx = np.where(m)
        Yg, Xg = yy + y0, xx + x0
        w0, w1, w2 = l0[m][:, None], l1[m][:, None], l2[m][:, None]
        tex_pos[Yg, Xg] = w0 * A3[i] + w1 * B3[i] + w2 * C3[i]
        n = w0 * NA[i] + w1 * NB[i] + w2 * NC[i]
        tex_nrm[Yg, Xg] = n / np.maximum(np.linalg.norm(n, axis=1)[:, None], 1e-12)
        tex_tri[Yg, Xg] = i
    ON = tex_tri >= 0
    P2 = TP
    uv_area = np.maximum(0.5 * np.abs((P2[:, 1, 0] - P2[:, 0, 0]) * (P2[:, 2, 1] - P2[:, 0, 1]) -
                                      (P2[:, 2, 0] - P2[:, 0, 0]) * (P2[:, 1, 1] - P2[:, 0, 1])), 1e-9)
    fn = np.cross(B3 - A3, C3 - A3)
    fn /= np.maximum(np.linalg.norm(fn, axis=1)[:, None], 1e-12)
    # GODOT WINDS ITS FRONT FACES CLOCKWISE, so the cross product above points INTO the mesh. It
    # is oriented by the triangle's own vertex normals instead, which is convention-free: the
    # first run took the back faces as the seen ones, and the bake's facing test (which reads
    # the texel normals) then rejected 98% of them.
    fn *= np.where(np.einsum("ij,ij->i", fn, NA + NB + NC) < 0, -1.0, 1.0)[:, None]
    cen = (A3 + B3 + C3) / 3.0
    # ---- the camera: the plate's own cell ----
    pl = PL["plates"][id_]
    c = pl["cell"]
    x0c, y0c, wc, hc = c["rect"]
    ppm = float(c["px_per_m"])
    right, up, aim = np.array(c["screen_right"]), np.array(c["screen_up"]), np.array(c["aim"])
    vdir = np.array(c["view_dir"])
    near = V @ vdir                                               # larger = nearer the camera
    sx = ((V - aim) @ right * ppm + wc / 2.0) * SS
    sy = (hc / 2.0 - (V - aim) @ up * ppm) * SS
    W2, H2 = int(wc * SS), int(hc * SS)
    zb = np.full((H2, W2), -np.inf)
    face = (fn @ vdir) > 0.05                                     # 06a's own facing test
    for i in np.where(face)[0]:
        t = TRI[i]
        px, py, pz = sx[t], sy[t], near[t]
        x0 = max(int(np.floor(px.min())), 0); x1 = min(int(np.ceil(px.max())) + 1, W2)
        y0 = max(int(np.floor(py.min())), 0); y1 = min(int(np.ceil(py.max())) + 1, H2)
        if x1 <= x0 or y1 <= y0:
            continue
        X, Y = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
        d = ((py[1] - py[2]) * (px[0] - px[2]) + (px[2] - px[1]) * (py[0] - py[2]))
        if abs(d) < 1e-12:
            continue
        l0 = ((py[1] - py[2]) * (X - px[2]) + (px[2] - px[1]) * (Y - py[2])) / d
        l1 = ((py[2] - py[0]) * (X - px[2]) + (px[0] - px[2]) * (Y - py[2])) / d
        l2 = 1.0 - l0 - l1
        m = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
        if not m.any():
            continue
        z = l0 * pz[0] + l1 * pz[1] + l2 * pz[2]
        sub = zb[y0:y1, x0:x1]
        np.maximum(sub, np.where(m, z, -np.inf), out=sub)
    cx = ((cen - aim) @ right * ppm + wc / 2.0) * SS
    cy = (hc / 2.0 - (cen - aim) @ up * ppm) * SS
    ci = np.clip(cx.astype(int), 0, W2 - 1)
    cj = np.clip(cy.astype(int), 0, H2 - 1)
    tol = 0.01                                                    # 1 cm: one surface, not two
    vis = face & (cen @ vdir >= zb[cj, ci] - tol)
    np.savez(os.path.join(WORK, "surf_%s.npz" % id_), tex_tri=tex_tri.astype(np.int32),
             tex_pos=tex_pos, tex_nrm=tex_nrm, uv_area=uv_area.astype(np.float32),
             V=V.astype(np.float32), TRI=TRI.astype(np.int32), size=np.array([SIZE]),
             **{"vis_%s_guide" % id_: vis})
    json.dump({"px_per_m": ppm, "cells": {"guide": c},
               "_what": "C-9 T10-2: the hero %s's plate as a t5_06b_bake.py sheet: one cell, the play camera" % id_},
              open(os.path.join(WORK, "layout_%s.json" % id_), "w"), indent=1)
    # THE MATTE: the plate's alpha (the piece as the ID render sees it, and its 3 px ring), plus
    # alpha 96 where the piece's OWN projected geometry lies behind another piece. The bake's
    # self-test asks every in-cell vertex to land on the silhouette; a lintel whose ends go into
    # the mound fails it (84% on the first run) against the visible matte alone, although its
    # camera is exact. Texels sampled under alpha 96 take the occluder's paint -- and the camera
    # never turns, so they are exactly the texels the player never sees. They are counted apart.
    from PIL import ImageDraw
    full = Image.new("L", (wc, hc), 0)
    dr = ImageDraw.Draw(full)
    qx = (V - aim) @ right * ppm + wc / 2.0
    qy = hc / 2.0 - (V - aim) @ up * ppm
    for t_ in TRI:
        dr.polygon([(float(qx[k]), float(qy[k])) for k in t_], fill=255)
    full = np.asarray(full) > 0
    plate = np.array(Image.open(os.path.join(BF, "take", pl["file"])).convert("RGBA"))
    hidden = full & (plate[..., 3] == 0)
    plate[..., 3] = np.where(hidden, 96, plate[..., 3])
    os.makedirs(os.path.join(WORK, "_cells_%s" % id_), exist_ok=True)
    Image.fromarray(plate, "RGBA").save(os.path.join(WORK, "_cells_%s" % id_, "cell_guide.png"))
    return {"tris": int(len(TRI)), "uv_coverage_pct": round(100 * float(ON.mean()), 2),
            "tris_facing": int(face.sum()), "tris_seen": int(vis.sum()),
            "silhouette_px_in_cell": int(full.sum()), "hidden_by_another_piece_px": int(hidden.sum())}


def main():
    ids = sorted(f[:-5] for f in os.listdir(MESH) if f.endswith(".json") and not f.startswith("export"))
    if ONLY:
        ids = [i for i in ids if i in ONLY]
    rep = {}
    for id_ in ids:
        rep[id_] = surface(id_)
        print("%-18s %s" % (id_, rep[id_]))
    json.dump(rep, open(os.path.join(WORK, "surface_report.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
