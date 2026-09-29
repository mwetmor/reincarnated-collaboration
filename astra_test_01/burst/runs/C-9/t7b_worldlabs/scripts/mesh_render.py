#!/usr/bin/env python3
"""T7-B: render Marble's collider GLB through OUR game camera, with a z-buffer.

Splats have no depth test, so a Gaussian cloud viewed from outside its bubble needs
a hand-tuned near plane and still smears.  The collider mesh is opaque triangles, so
a z-buffer gives the UNAMBIGUOUS answer to "what shape is this, from our camera".

Camera law is render_splats.player_lock_basis() -- R-C9-68's orthographic view at
pitch 52.95354112560294 deg, yaw 47 deg.

Modes
  vcol   vertex colours (Marble's collider carries COLOR_0, no UVs)
  slope  tilt-from-horizontal ramp: green = walkable (<30 deg), red = wall (>60 deg)
  depth  view-space depth ramp
All modes multiply in a lambert term from a fixed key light so form reads.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from numba import njit

import glb_probe
from render_splats import PL_PITCH_DEG, PL_YAW_DEG, player_lock_basis


@njit(cache=True, fastmath=True)
def _zraster(sx, sy, sz, col, tris, W, H, zbuf, out, idbuf):
    for t in range(tris.shape[0]):
        i0, i1, i2 = tris[t, 0], tris[t, 1], tris[t, 2]
        x0, y0, z0 = sx[i0], sy[i0], sz[i0]
        x1, y1, z1 = sx[i1], sy[i1], sz[i1]
        x2, y2, z2 = sx[i2], sy[i2], sz[i2]
        minx = int(min(x0, min(x1, x2)))
        maxx = int(max(x0, max(x1, x2))) + 1
        miny = int(min(y0, min(y1, y2)))
        maxy = int(max(y0, max(y1, y2))) + 1
        if maxx <= 0 or maxy <= 0 or minx >= W or miny >= H:
            continue
        if minx < 0: minx = 0
        if miny < 0: miny = 0
        if maxx > W: maxx = W
        if maxy > H: maxy = H
        d = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(d) < 1e-12:
            continue
        inv = 1.0 / d
        for py in range(miny, maxy):
            fy = py + 0.5
            for px in range(minx, maxx):
                fx = px + 0.5
                l0 = ((y1 - y2) * (fx - x2) + (x2 - x1) * (fy - y2)) * inv
                l1 = ((y2 - y0) * (fx - x2) + (x0 - x2) * (fy - y2)) * inv
                l2 = 1.0 - l0 - l1
                if l0 < 0.0 or l1 < 0.0 or l2 < 0.0:
                    continue
                z = l0 * z0 + l1 * z1 + l2 * z2
                if z >= zbuf[py, px]:
                    continue
                zbuf[py, px] = z
                idbuf[py, px] = t
                out[py, px, 0] = l0 * col[i0, 0] + l1 * col[i1, 0] + l2 * col[i2, 0]
                out[py, px, 1] = l0 * col[i0, 1] + l1 * col[i1, 1] + l2 * col[i2, 1]
                out[py, px, 2] = l0 * col[i0, 2] + l1 * col[i1, 2] + l2 * col[i2, 2]


def vertex_colors(js, bin_, nv):
    cols = []
    for m in js.get("meshes", []):
        for p in m.get("primitives", []):
            if "COLOR_0" in p.get("attributes", {}):
                c = glb_probe.accessor(js, bin_, p["attributes"]["COLOR_0"]).astype(np.float64)
                acc = js["accessors"][p["attributes"]["COLOR_0"]]
                if acc["componentType"] == 5121:
                    c = c / 255.0
                elif acc["componentType"] == 5123:
                    c = c / 65535.0
                cols.append(c[:, :3])
    return np.vstack(cols) if cols else np.ones((nv, 3)) * 0.7


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("glb")
    ap.add_argument("--out", required=True)
    ap.add_argument("--res", default="1920x1080")
    ap.add_argument("--size", type=float, default=0.0)
    ap.add_argument("--center", default="")
    ap.add_argument("--yaw", type=float, default=PL_YAW_DEG)
    ap.add_argument("--pitch", type=float, default=PL_PITCH_DEG)
    ap.add_argument("--mode", default="vcol", choices=["vcol", "slope", "depth"])
    ap.add_argument("--stats", default="")
    a = ap.parse_args()

    js, bin_ = glb_probe.read_glb(a.glb)
    V, F = glb_probe.gather(js, bin_)
    V = V * np.array([1.0, -1.0, -1.0])        # marble_raw_opencv -> Y up
    C = vertex_colors(js, bin_, len(V))
    if len(C) != len(V):
        C = np.ones((len(V), 3)) * 0.7

    lo, hi = V.min(0), V.max(0)
    ctr = (lo + hi) * 0.5
    if a.center:
        ctr = np.array([float(v) for v in a.center.split(",")])
    size_m = a.size if a.size > 0 else float(np.max(hi - lo)) * 1.05

    fwd, upc, rgt = player_lock_basis(a.yaw, a.pitch)
    Rv = np.stack([rgt, upc, fwd])
    W, H = (int(v) for v in a.res.lower().split("x"))
    v = (V - ctr) @ Rv.T
    ppm = H / size_m
    sx = W * 0.5 + v[:, 0] * ppm
    sy = H * 0.5 - v[:, 1] * ppm
    sz = v[:, 2]

    p0, p1, p2 = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    n = np.cross(p1 - p0, p2 - p0)
    nl = np.linalg.norm(n, axis=1, keepdims=True)
    nn = n / np.maximum(nl, 1e-12)
    if a.mode == "slope":
        tilt = np.degrees(np.arccos(np.clip(np.abs(nn[:, 1]), 0, 1)))
        # green (walkable) -> yellow -> red (wall)
        tt = np.clip(tilt / 75.0, 0, 1)
        fc = np.stack([tt, 1.0 - 0.6 * tt, 0.15 + 0.0 * tt], 1)
        C = np.zeros((len(V), 3))
        cnt = np.zeros(len(V))
        for k in range(3):
            np.add.at(C, F[:, k], fc)
            np.add.at(cnt, F[:, k], 1.0)
        C /= np.maximum(cnt, 1)[:, None]
    elif a.mode == "depth":
        d = sz.copy()
        C = np.repeat(((d - d.min()) / max(1e-9, d.ptp()))[:, None], 3, 1)
        C = 1.0 - C

    # key light along the camera's own forward, softened; keeps form readable
    lam = np.abs(nn @ (-fwd))
    shade = 0.45 + 0.55 * lam
    Cv = np.zeros((len(V), 3)); cnt = np.zeros(len(V))
    for k in range(3):
        np.add.at(Cv, F[:, k], C[F[:, k]] * shade[:, None])
        np.add.at(cnt, F[:, k], 1.0)
    Cv /= np.maximum(cnt, 1)[:, None]

    zbuf = np.full((H, W), 1e30)
    idb = np.full((H, W), -1, np.int64)
    out = np.zeros((H, W, 3))
    out[:] = np.array([0.055, 0.06, 0.085])
    _zraster(np.ascontiguousarray(sx), np.ascontiguousarray(sy), np.ascontiguousarray(sz),
             np.ascontiguousarray(np.clip(Cv, 0, 1)), np.ascontiguousarray(F.astype(np.int64)),
             W, H, zbuf, out, idb)
    from PIL import Image
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)).save(a.out)
    st = {"glb": a.glb, "mode": a.mode, "res": [W, H], "size_m": size_m, "ppm": ppm,
          "center": [round(float(x), 3) for x in ctr], "yaw_deg": a.yaw, "pitch_deg": a.pitch,
          "triangles": int(len(F)), "pixels_covered_frac": float((idb >= 0).mean())}
    print(json.dumps(st, indent=1))
    if a.stats:
        Path(a.stats).write_text(json.dumps(st, indent=1))


if __name__ == "__main__":
    main()
