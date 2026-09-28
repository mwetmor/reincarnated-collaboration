#!/usr/bin/env python3
"""C-9 knight3d: a small deterministic triangle rasteriser.

Used for three things that must agree with each other exactly:
  * baking the UV atlas (which texel is which point on the body),
  * the per-view depth buffers that decide VISIBILITY when projecting paint,
  * the per-frame depth/normal buffers the ink pass draws its line from.

Doing all three with one rasteriser is the point. M-a's 6.6 % surprise came
from two pieces of geometry code that were supposed to agree and did not.
"""
import numpy as np


def raster(tris_xy, tris_z, attrs, W, H, backface_cull=False):
    """Z-buffer rasterise.

    tris_xy : (N,3,2) pixel coordinates
    tris_z  : (N,3)   depth, SMALLER = nearer
    attrs   : (N,3,K) per-vertex attributes to interpolate (or None)
    returns  zbuf (H,W) float (inf where empty), idbuf (H,W) int (-1 empty),
             abuf (H,W,K) float, bary (H,W,3) float
    """
    N = len(tris_xy)
    K = attrs.shape[2] if attrs is not None else 0
    zbuf = np.full((H, W), np.inf, np.float64)
    idbuf = np.full((H, W), -1, np.int32)
    abuf = np.zeros((H, W, K), np.float64) if K else None
    bbuf = np.zeros((H, W, 3), np.float64)

    for i in range(N):
        p = tris_xy[i]
        x0 = int(np.floor(p[:, 0].min())); x1 = int(np.ceil(p[:, 0].max()))
        y0 = int(np.floor(p[:, 1].min())); y1 = int(np.ceil(p[:, 1].max()))
        x0 = max(x0, 0); y0 = max(y0, 0); x1 = min(x1, W - 1); y1 = min(y1, H - 1)
        if x1 < x0 or y1 < y0:
            continue
        ax, ay = p[0]; bx, by = p[1]; cx, cy = p[2]
        den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(den) < 1e-12:
            continue
        if backface_cull and den > 0:
            continue
        xs = np.arange(x0, x1 + 1) + 0.5
        ys = np.arange(y0, y1 + 1) + 0.5
        X, Y = np.meshgrid(xs, ys)
        l0 = ((by - cy) * (X - cx) + (cx - bx) * (Y - cy)) / den
        l1 = ((cy - ay) * (X - cx) + (ax - cx) * (Y - cy)) / den
        l2 = 1.0 - l0 - l1
        m = (l0 >= -1e-9) & (l1 >= -1e-9) & (l2 >= -1e-9)
        if not m.any():
            continue
        z = l0 * tris_z[i, 0] + l1 * tris_z[i, 1] + l2 * tris_z[i, 2]
        sub = zbuf[y0:y1 + 1, x0:x1 + 1]
        win = m & (z < sub)
        if not win.any():
            continue
        sub[win] = z[win]
        idbuf[y0:y1 + 1, x0:x1 + 1][win] = i
        bb = bbuf[y0:y1 + 1, x0:x1 + 1]
        bb[win, 0] = l0[win]; bb[win, 1] = l1[win]; bb[win, 2] = l2[win]
        if K:
            a = (l0[..., None] * attrs[i, 0] + l1[..., None] * attrs[i, 1]
                 + l2[..., None] * attrs[i, 2])
            abuf[y0:y1 + 1, x0:x1 + 1][win] = a[win]
    return zbuf, idbuf, abuf, bbuf


def tri_normals(tri_v):
    n = np.cross(tri_v[:, 1] - tri_v[:, 0], tri_v[:, 2] - tri_v[:, 0])
    L = np.linalg.norm(n, axis=1, keepdims=True)
    return n / np.maximum(L, 1e-12)


def kabsch(A, B):
    """Rigid transform (R, t) with B ~= A @ R.T + t, for equal-length clouds."""
    ca, cb = A.mean(0), B.mean(0)
    H = (A - ca).T @ (B - cb)
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1, 1, d]) @ U.T
    return R, cb - R @ ca
