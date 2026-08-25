#!/usr/bin/env python3
"""gd_boundary_extract.py — hard-boundary polygon from the registered mosaic.

The mapped-terrain overlay on the GD minimap is warm and brighter than the
transparent void, where the live world view bleeds through.  Segment on
score = luminance + 1.5*(R-B), keep the component the player's own track lies
in, close pinholes, then walk the outer contour and simplify.
"""
from __future__ import annotations

import collections
import json
import os

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
THRESH = 25.0


def close_open(m, r_close=3, r_open=2):
    def disc(r):
        y, x = np.mgrid[-r:r + 1, -r:r + 1]
        return (x * x + y * y) <= r * r

    def dil(a, se):
        out = np.zeros_like(a)
        R = se.shape[0] // 2
        ys, xs = np.nonzero(se)
        for y, x in zip(ys, xs):
            dy, dx = y - R, x - R
            out |= np.roll(np.roll(a, dy, 0), dx, 1)
        return out

    def ero(a, se):
        return ~dil(~a, se)
    m = ero(dil(m, disc(r_close)), disc(r_close))
    m = dil(ero(m, disc(r_open)), disc(r_open))
    return m


def largest_component_containing(m, seeds):
    seen = np.zeros(m.shape, bool)
    q = collections.deque()
    for sx, sy in seeds:
        if m[sy, sx] and not seen[sy, sx]:
            seen[sy, sx] = True
            q.append((sy, sx))
    while q:
        cy, cx = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < m.shape[0] and 0 <= nx < m.shape[1] and m[ny, nx] \
                    and not seen[ny, nx]:
                seen[ny, nx] = True
                q.append((ny, nx))
    return seen


def fill_holes(m):
    out = ~m
    seen = np.zeros(m.shape, bool)
    q = collections.deque()
    for x in range(m.shape[1]):
        for y in (0, m.shape[0] - 1):
            if out[y, x] and not seen[y, x]:
                seen[y, x] = True; q.append((y, x))
    for y in range(m.shape[0]):
        for x in (0, m.shape[1] - 1):
            if out[y, x] and not seen[y, x]:
                seen[y, x] = True; q.append((y, x))
    while q:
        cy, cx = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < m.shape[0] and 0 <= nx < m.shape[1] and out[ny, nx] \
                    and not seen[ny, nx]:
                seen[ny, nx] = True; q.append((ny, nx))
    return m | (~seen & out)


def trace_contour(m):
    """Moore-neighbour boundary walk of the outer contour."""
    ys, xs = np.nonzero(m)
    sy = ys.min()
    sx = xs[ys == sy].min()
    start = (sy, sx)
    nb = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    contour = [start]
    cur = start
    bdir = 6
    for _ in range(400000):
        found = False
        for k in range(8):
            d = (bdir + 1 + k) % 8
            ny, nx = cur[0] + nb[d][0], cur[1] + nb[d][1]
            if 0 <= ny < m.shape[0] and 0 <= nx < m.shape[1] and m[ny, nx]:
                bdir = (d + 4) % 8
                cur = (ny, nx)
                contour.append(cur)
                found = True
                break
        if not found:
            break
        if cur == start and len(contour) > 3:
            break
    return contour


def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    a, b = np.array(pts[0], float), np.array(pts[-1], float)
    ab = b - a
    n = np.hypot(*ab)
    P = np.array(pts, float)
    if n < 1e-9:
        d = np.hypot(*(P - a).T)
    else:
        d = np.abs(np.cross(np.tile(ab, (len(P), 1)), P - a)) / n
    i = int(np.argmax(d))
    if d[i] > eps:
        return rdp(pts[:i + 1], eps)[:-1] + rdp(pts[i:], eps)
    return [pts[0], pts[-1]]


def main():
    med = np.load(os.path.join(HERE, "gd-arena-mosaic-med.npy"))
    cnt = np.load(os.path.join(HERE, "gd-arena-mosaic-cnt.npy"))
    meta = json.load(open(os.path.join(HERE, "gd-arena-mosaic-meta.json")))
    ox, oy = meta["ox"], meta["oy"]
    score = med.mean(axis=2) + 1.5 * (med[:, :, 0] - med[:, :, 2])
    m = (score > THRESH) & (cnt >= 1)
    m = close_open(m)
    seeds = [(int(round(t[0] + ox)), int(round(t[1] + oy))) for t in meta["track"]]
    m = largest_component_containing(m, seeds)
    m = fill_holes(m)
    print("footprint area (minimap px^2):", int(m.sum()))

    # coverage check: does the footprint touch unobserved canvas?
    unob = (cnt == 0)
    edge = m & ~np.roll(m, 1, 0) | m & ~np.roll(m, -1, 0) | \
        m & ~np.roll(m, 1, 1) | m & ~np.roll(m, -1, 1)
    touch = int((edge & (np.roll(unob, 1, 0) | np.roll(unob, -1, 0) |
                         np.roll(unob, 1, 1) | np.roll(unob, -1, 1))).sum())
    print("boundary px adjacent to UNOBSERVED canvas:", touch)
    # coverage margin: min observation count along the boundary
    bc = cnt[edge]
    print("obs count along boundary: min", int(bc.min()), "median", int(np.median(bc)))

    contour = trace_contour(m)
    print("raw contour px:", len(contour))
    pts = [(c[1], c[0]) for c in contour]
    for eps in (1.0, 1.5, 2.0, 3.0):
        print(f"  rdp eps={eps}: {len(rdp(pts, eps))} vertices")
    poly = rdp(pts, 1.5)
    arena = [[round(p[0] - ox, 2), round(p[1] - oy, 2)] for p in poly]
    np.save(os.path.join(HERE, "gd-arena-footprint-mask.npy"), m)
    json.dump(dict(vertices_minimap_px=arena, area_px=int(m.sum()),
                   thresh=THRESH, boundary_touches_unobserved=touch,
                   boundary_min_obs=int(bc.min())),
              open(os.path.join(HERE, "gd-arena-boundary.json"), "w"), indent=1)

    S = 4
    vis = Image.fromarray(np.clip(med * 2.2, 0, 255).astype(np.uint8)).resize(
        (meta["W"] * S, meta["H"] * S), Image.LANCZOS)
    d = ImageDraw.Draw(vis)
    d.line([(p[0] * S, p[1] * S) for p in poly] + [(poly[0][0] * S, poly[0][1] * S)],
           fill=(255, 60, 60), width=3)
    for i, t in enumerate(meta["track"]):
        x, y = (t[0] + ox) * S, (t[1] + oy) * S
        d.ellipse([x - 7, y - 7, x + 7, y + 7], outline=(0, 255, 255), width=3)
        d.text((x + 9, y - 6), str(meta["shots"][i]), fill=(0, 255, 255))
    vis.save(os.path.join(HERE, "gd-arena-boundary.png"))
    print("vertices:", len(poly))


if __name__ == "__main__":
    main()
