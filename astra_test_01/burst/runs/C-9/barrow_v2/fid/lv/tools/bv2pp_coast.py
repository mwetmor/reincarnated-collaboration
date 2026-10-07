#!/usr/bin/env python3
"""BV2F LV Phase 1'' (R-C9-204/205/206): geometry helpers for the coast, the water and the ice -- curving chains,
irregular polygons, Voronoi ice plates and floes. Imported by make_bv2art.py (no outputs of its own).
All coordinates are v1's (u, v) metres."""
import math

import numpy as np
from scipy.spatial import Voronoi


def resample(chain, step):
    out = [chain[0]]
    acc = 0.0
    for a, b in zip(chain[:-1], chain[1:]):
        L = math.dist(a, b)
        t = step - acc
        while t <= L:
            out.append((a[0] + (b[0] - a[0]) * t / L, a[1] + (b[1] - a[1]) * t / L))
            t += step
        acc = (acc + L) % step
    if math.dist(out[-1], chain[-1]) > 1e-6:
        out.append(chain[-1])
    return out


def wiggle(chain, amp, step=1.0, taper=4.0, keep=None):
    """resample `chain` at `step` and push each point sideways by amp(s) (s = arc length); the two ends taper to 0 over
    `taper` m; keep(s) in [0, 1] scales the push (0 = keep the line straight there)"""
    pts = resample(chain, step)
    s_acc = [0.0]
    for a, b in zip(pts[:-1], pts[1:]):
        s_acc.append(s_acc[-1] + math.dist(a, b))
    total = s_acc[-1]
    out = []
    for i, p in enumerate(pts):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, len(pts) - 1)]
        d = (b[0] - a[0], b[1] - a[1])
        n = math.hypot(*d) or 1.0
        nrm = (-d[1] / n, d[0] / n)
        s = s_acc[i]
        w = min(1.0, s / taper, (total - s) / taper)
        if keep is not None:
            w *= keep(s)
        o = amp(s) * w
        out.append((p[0] + nrm[0] * o, p[1] + nrm[1] * o))
    return out, s_acc


def area(poly):
    return 0.5 * abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(poly, poly[1:] + poly[:1])))


def centroid(poly):
    x = sum(p[0] for p in poly) / len(poly)
    y = sum(p[1] for p in poly) / len(poly)
    return (x, y)


def ccw(poly):
    s = sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(poly, poly[1:] + poly[:1]))
    return poly if s > 0 else poly[::-1]


def clip_poly(poly, a, b):
    """Sutherland-Hodgman against the half-plane left of a->b"""
    def inside(p):
        return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= 0

    def cut(p, q):
        dx, dy = q[0] - p[0], q[1] - p[1]
        ex, ey = b[0] - a[0], b[1] - a[1]
        den = ex * dy - ey * dx
        if abs(den) < 1e-12:
            return q
        t = (ex * (a[1] - p[1]) - ey * (a[0] - p[0])) / den
        return (p[0] + dx * t, p[1] + dy * t)
    out = []
    for i, p in enumerate(poly):
        q = poly[(i + 1) % len(poly)]
        if inside(p):
            out.append(p)
            if not inside(q):
                out.append(cut(p, q))
        elif inside(q):
            out.append(cut(p, q))
    return out


def clip_to_box(poly, box):
    u0, v0, u1, v1 = box
    for a, b in (((u0, v0), (u1, v0)), ((u1, v0), (u1, v1)), ((u1, v1), (u0, v1)), ((u0, v1), (u0, v0))):
        poly = clip_poly(poly, a, b)
        if len(poly) < 3:
            return []
    return poly


def voronoi_cells(seeds, box):
    u0, v0, u1, v1 = box
    w, h = u1 - u0, v1 - v0
    far = [(u0 - 3 * w, v0 - 3 * h), (u1 + 3 * w, v0 - 3 * h), (u1 + 3 * w, v1 + 3 * h), (u0 - 3 * w, v1 + 3 * h)]
    vor = Voronoi(np.array(list(seeds) + far))
    cells = []
    for i in range(len(seeds)):
        reg = vor.regions[vor.point_region[i]]
        if not reg or -1 in reg:
            cells.append([])
            continue
        poly = ccw([tuple(vor.vertices[k]) for k in reg])
        cells.append(clip_to_box(poly, box))
    return cells


def shrink(poly, d):
    """move every vertex toward the centroid by d metres (a crack gap of ~2d between neighbours)"""
    c = centroid(poly)
    out = []
    for p in poly:
        r = math.dist(p, c)
        if r <= d + 0.05:
            return []
        f = (r - d) / r
        out.append((c[0] + (p[0] - c[0]) * f, c[1] + (p[1] - c[1]) * f))
    return out


def scale_about(poly, f):
    c = centroid(poly)
    return [(c[0] + (p[0] - c[0]) * f, c[1] + (p[1] - c[1]) * f) for p in poly]


def roughen(poly, rng, amp, seg=0.8):
    """subdivide each edge into ~seg m pieces and push the new points in/out by up to amp (irregular, broken edges)"""
    out = []
    for i, a in enumerate(poly):
        b = poly[(i + 1) % len(poly)]
        L = math.dist(a, b)
        n = max(1, int(L / seg))
        nx, ny = (b[1] - a[1]) / (L or 1), -(b[0] - a[0]) / (L or 1)
        for k in range(n):
            t = k / n
            o = 0.0 if k == 0 else rng.uniform(-amp, amp)
            out.append((a[0] + (b[0] - a[0]) * t + nx * o, a[1] + (b[1] - a[1]) * t + ny * o))
    return out


def blob(centre, radii, rng, n=48, amp=0.18, lobes=(2, 3, 5)):
    """an organic closed outline: an ellipse whose radius is modulated by a few low harmonics"""
    ph = [rng.uniform(0, 2 * math.pi) for _ in lobes]
    am = [amp * rng.uniform(0.5, 1.0) / (1 + 0.4 * i) for i in range(len(lobes))]
    out = []
    for k in range(n):
        t = 2 * math.pi * k / n
        f = 1.0 + sum(a * math.sin(l * t + p) for a, l, p in zip(am, lobes, ph))
        out.append((centre[0] + radii[0] * f * math.cos(t), centre[1] + radii[1] * f * math.sin(t)))
    return out


def jitter_seeds(box, spacing, rng, keep):
    u0, v0, u1, v1 = box
    out = []
    v = v0 + spacing / 2
    row = 0
    while v < v1:
        u = u0 + (spacing / 2 if row % 2 else 0.0)
        while u < u1:
            p = (u + rng.uniform(-0.38, 0.38) * spacing, v + rng.uniform(-0.38, 0.38) * spacing)
            if keep(p):
                out.append(p)
            u += spacing
        v += spacing * 0.87
        row += 1
    return out


def point_in_poly(p, poly):
    x, y = p
    inside = False
    for (ax, ay), (bx, by) in zip(poly, poly[1:] + poly[:1]):
        if (ay > y) != (by > y) and x < ax + (y - ay) * (bx - ax) / (by - ay):
            inside = not inside
    return inside
