#!/usr/bin/env python3
"""gd_boundary_extract2.py — hard boundary (outer ring + interior obstructions).

Input is the per-shot-vote footprint probability p (gd_footprint_vote.py).
GD's minimap paints WALKED/WALKABLE floor only; walls and impassable rim are not
painted.  So the arena's hard geometry is: the outer contour of the terrain
component the player's own track lies in, PLUS the contours of the holes inside
it (the inner wall ring and its pillars), all of which the Godot runtime clamp
must respect.
"""
from __future__ import annotations

import collections
import json
import os

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
P_MIN = 0.65
OBS_MIN = 3
MIN_HOLE_AREA = 60          # minimap px^2 -- below this is speckle, not a wall


def label(m):
    lab = -np.ones(m.shape, int)
    cur = 0
    sizes = []
    for y in range(m.shape[0]):
        for x in range(m.shape[1]):
            if m[y, x] and lab[y, x] < 0:
                q = collections.deque([(y, x)])
                lab[y, x] = cur
                n = 0
                while q:
                    cy, cx = q.popleft()
                    n += 1
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < m.shape[0] and 0 <= nx < m.shape[1] \
                                and m[ny, nx] and lab[ny, nx] < 0:
                            lab[ny, nx] = cur
                            q.append((ny, nx))
                sizes.append(n)
                cur += 1
    return lab, sizes


def trace(m, start, outer=True):
    nb = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    contour = [start]
    cur = start
    bdir = 6
    for _ in range(500000):
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
        return list(pts)
    P = np.array(pts, float)
    a, b = P[0], P[-1]
    ab = b - a
    n = np.hypot(*ab)
    d = np.hypot(*(P - a).T) if n < 1e-9 else np.abs(np.cross(ab, P - a)) / n
    i = int(np.argmax(d))
    if d[i] > eps:
        return rdp(pts[:i + 1], eps)[:-1] + rdp(pts[i:], eps)
    return [pts[0], pts[-1]]


def main():
    import sys
    sys.setrecursionlimit(100000)
    p = np.load(os.path.join(HERE, "gd-footprint-p.npy"))
    obs = np.load(os.path.join(HERE, "gd-footprint-obs.npy"))
    meta = json.load(open(os.path.join(HERE, "gd-arena-mosaic-meta.json")))
    ox, oy, W, H = meta["ox"], meta["oy"], meta["W"], meta["H"]
    m = (p > P_MIN) & (obs >= OBS_MIN)

    lab, sizes = label(m)
    seeds = {lab[int(round(t[1] + oy)), int(round(t[0] + ox))] for t in meta["track"]}
    seeds.discard(-1)
    print("track sits in component(s):", sorted(seeds),
          "sizes:", [sizes[s] for s in sorted(seeds)])
    main_lab = max(seeds, key=lambda s: sizes[s])
    m = lab == main_lab
    print("arena component area:", int(m.sum()), "minimap px^2")

    # holes: background components not connected to the canvas border
    bg = ~m
    blab, bsizes = label(bg)
    border = set(blab[0, :]) | set(blab[-1, :]) | set(blab[:, 0]) | set(blab[:, -1])
    med = np.load(os.path.join(HERE, "gd-arena-mosaic-med.npy"))
    holes = []
    icons = []
    for i in range(len(bsizes)):
        if i in border or bsizes[i] < MIN_HOLE_AREA:
            continue
        px = med[blab == i]
        R, G, B = px[:, 0].mean(), px[:, 1].mean(), px[:, 2].mean()
        # HUD icons (the teal pedestal gems) sit ON TOP of the painted map and
        # so read as unpainted to the terrain classifier.  They are bright and
        # blue-dominant; real unpainted void is dark and neutral/warm.
        if B > 70 and B > R * 1.3:
            icons.append((i, bsizes[i], (round(R, 1), round(G, 1), round(B, 1))))
            continue
        holes.append(i)
    print(f"HUD-icon holes rejected (bright + blue-dominant): {len(icons)}", icons)
    print(f"interior obstruction components >= {MIN_HOLE_AREA}px: {len(holes)}",
          sorted((bsizes[i] for i in holes), reverse=True)[:20])
    for i, _, _ in icons:                     # icons are floor, not obstruction
        m |= (blab == i)

    # fill sub-threshold speckle holes back into the floor
    for i in range(len(bsizes)):
        if i not in border and bsizes[i] < MIN_HOLE_AREA:
            m |= (blab == i)

    ys, xs = np.nonzero(m)
    sy = ys.min(); sx = xs[ys == sy].min()
    outer = trace(m, (sy, sx))
    outer_poly = rdp([(c[1], c[0]) for c in outer], 1.5)
    print("outer contour:", len(outer), "px ->", len(outer_poly), "vertices")

    hole_polys = []
    for i in holes:
        hm = (blab == i)
        hy, hx = np.nonzero(hm)
        s = (hy.min(), hx[hy == hy.min()].min())
        c = trace(hm, s)
        hp = rdp([(q[1], q[0]) for q in c], 1.5)
        if len(hp) >= 4:
            hole_polys.append((int(bsizes[i]), hp))
    hole_polys.sort(key=lambda z: -z[0])
    print("hole polygons:", [(a, len(b)) for a, b in hole_polys])

    out = dict(
        outer=[[round(x - ox, 2), round(y - oy, 2)] for x, y in outer_poly],
        holes=[dict(area_px=a,
                    vertices=[[round(x - ox, 2), round(y - oy, 2)] for x, y in b])
               for a, b in hole_polys],
        area_px=int(m.sum()), p_min=P_MIN, obs_min=OBS_MIN)
    json.dump(out, open(os.path.join(HERE, "gd-arena-boundary2.json"), "w"), indent=1)
    np.save(os.path.join(HERE, "gd-arena-floor-mask.npy"), m)

    S = 4
    med = np.load(os.path.join(HERE, "gd-arena-mosaic-med.npy"))
    vis = Image.fromarray(np.clip(med * 2.2, 0, 255).astype(np.uint8)).resize(
        (W * S, H * S), Image.LANCZOS)
    d = ImageDraw.Draw(vis)
    d.line([(x * S, y * S) for x, y in outer_poly] +
           [(outer_poly[0][0] * S, outer_poly[0][1] * S)], fill=(255, 50, 50), width=3)
    for a, b in hole_polys:
        d.line([(x * S, y * S) for x, y in b] + [(b[0][0] * S, b[0][1] * S)],
               fill=(255, 170, 0), width=2)
    inzone = {614, 618, 620, 622, 623, 626}
    for i, t in enumerate(meta["track"]):
        n = meta["shots"][i]
        x, y = (t[0] + ox) * S, (t[1] + oy) * S
        col = (60, 255, 60) if n in inzone else (0, 220, 255)
        d.ellipse([x - 8, y - 8, x + 8, y + 8], outline=col, width=3)
        d.text((x + 10, y - 6), str(n), fill=col)
    vis.save(os.path.join(HERE, "gd-arena-boundary2.png"))


if __name__ == "__main__":
    main()
