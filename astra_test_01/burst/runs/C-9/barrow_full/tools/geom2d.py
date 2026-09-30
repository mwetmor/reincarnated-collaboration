"""C-9 T10-2: the 2D geometry both the layout's pre-build check and finalize's measurement use.

One implementation, imported by both, so a squeeze the pre-check finds and a squeeze the
acceptance measures are found by the same arithmetic. Polygons are lists of (u, v) tuples,
open (the first point is not repeated), convex or not.
"""
import math


def rot(p, a):
    c, s = math.cos(a), math.sin(a)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def open_poly(poly):
    poly = [tuple(p) for p in poly]
    if len(poly) > 1 and poly[0] == poly[-1]:
        poly = poly[:-1]
    return poly


def hull2d(pts):
    pts = sorted(set((round(p[0], 6), round(p[1], 6)) for p in pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def circle_poly(c, r, n=16):
    return [(c[0] + r * math.cos(2 * math.pi * k / n), c[1] + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def seg_closest(p, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2))
    q = (ax + t * dx, ay + t * dy)
    return math.hypot(p[0] - q[0], p[1] - q[1]), q


def seg_pt(p, a, b):
    return seg_closest(p, a, b)[0]


def in_poly(p, poly):
    x, y = p
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xi:
                inside = not inside
    return inside


def seg_x(a, b, c, d):
    def o(p, q, s):
        return (q[0] - p[0]) * (s[1] - p[1]) - (q[1] - p[1]) * (s[0] - p[0])
    return (o(a, b, c) * o(a, b, d) < 0) and (o(c, d, a) * o(c, d, b) < 0)


def edges(poly, closed=True):
    n = len(poly)
    return [(poly[i], poly[(i + 1) % n]) for i in range(n if closed else n - 1)]


def dist_poly_pt(poly, p):
    if len(poly) >= 3 and in_poly(p, poly):
        return 0.0
    return min(seg_pt(p, a, b) for a, b in edges(poly))


def closest_pair(P, Q, q_closed=True):
    """(distance, point on P, point on Q). Zero, with a shared point, if they touch or overlap."""
    if len(Q) >= 3 and q_closed:
        for p in P:
            if in_poly(p, Q):
                return 0.0, p, p
    if len(P) >= 3:
        for q in Q:
            if in_poly(q, P):
                return 0.0, q, q
    EP = edges(P)
    EQ = edges(Q, q_closed)
    for a, b in EP:
        for c, d in EQ:
            if seg_x(a, b, c, d):
                return 0.0, a, a
    best = (1e18, None, None)
    for p in P:
        for c, d in EQ:
            dd, q = seg_closest(p, c, d)
            if dd < best[0]:
                best = (dd, p, q)
    for q in Q:
        for a, b in EP:
            dd, p = seg_closest(q, a, b)
            if dd < best[0]:
                best = (dd, p, q)
    return best


def dist_poly_poly(P, Q, q_closed=True):
    if not P or not Q:
        return None
    return closest_pair(P, Q, q_closed)[0]


def centroid_area(poly):
    A = cx = cy = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        c = x1 * y2 - x2 * y1
        A += c
        cx += (x1 + x2) * c
        cy += (y1 + y2) * c
    A *= 0.5
    if abs(A) < 1e-12:
        return (sum(p[0] for p in poly) / n, sum(p[1] for p in poly) / n), 0.0
    return (cx / (6 * A), cy / (6 * A)), abs(A)


def thick_segment(a, b, half_t):
    d = (b[0] - a[0], b[1] - a[1])
    L = math.hypot(*d) or 1.0
    n = (-d[1] / L * half_t, d[0] / L * half_t)
    return [(a[0] + n[0], a[1] + n[1]), (b[0] + n[0], b[1] + n[1]), (b[0] - n[0], b[1] - n[1]), (a[0] - n[0], a[1] - n[1])]


SQUEEZE_LO = 0.70     # his capsule's diameter: below this he cannot pass
SQUEEZE_HI = 1.40     # the spec's comfortable width
CAPSULE_R = 0.35


def signed_area(poly):
    return 0.5 * sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))


def boundary_samples(poly, step):
    """Points every `step` m round the outline, each with its edge's OUTWARD normal."""
    out = []
    ccw = signed_area(poly) > 0
    for a, b in edges(poly):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L < 1e-9:
            continue
        ex, ey = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        nrm = (ey, -ex) if ccw else (-ey, ex)
        n = max(1, int(math.ceil(L / step)))
        for k in range(n):
            t = (k + 0.5) / n
            out.append(((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), nrm))
    return out


def nearest_on(poly, p):
    if len(poly) >= 3 and in_poly(p, poly):
        return 0.0, p
    best = (1e18, None)
    for a, b in edges(poly):
        d, q = seg_closest(p, a, b)
        if d < best[0]:
            best = (d, q)
    return best


def squeezes(obstacles, stand_in_gap, lo=SQUEEZE_LO, hi=SQUEEZE_HI, step=0.1):
    """THE NO-SQUEEZE RULE: every gap between two obstacles in the walkable area is < lo or >= hi.

    PROFILED, and PER OBJECT. Every `step` m round each obstacle's outline, the gap is the
    distance to the NEAREST OTHER OBJECT -- nearest over all of that object's pieces (a mound is
    48 rim boxes, a cutting and a facade; a rock is three slabs). The first version compared
    pieces pair by pair and so measured a stone against one rim box while another box of the
    same mound stood 0.4 m closer: a gap that does not exist, reported as a squeeze.

    A sample counts only if its gap FACES the other object (see below). A width w in [lo, hi)
    counts where his capsule can STAND IN the gap: stand_in_gap(u, v, w)
    at the gap's midpoint. So a gap whose narrow end is walled off is judged by the part he can
    reach, and a dead-end notch he can step into counts. `obstacles` is a list of (group,
    polygon); one group is one object."""
    groups = {}
    for g, poly in obstacles:
        xs = [q[0] for q in poly]
        ys = [q[1] for q in poly]
        groups.setdefault(g, []).append((poly, (min(xs), max(xs), min(ys), max(ys))))
    seen = {}
    for gi, polys in groups.items():
        for poly, _ in polys:
            for p, nrm in boundary_samples(poly, step):
                best = (1e18, None, None)
                for gj, pj in groups.items():
                    if gj == gi:
                        continue
                    for poly2, b in pj:
                        if p[0] < b[0] - hi or p[0] > b[1] + hi or p[1] < b[2] - hi or p[1] > b[3] + hi:
                            continue
                        d, q = nearest_on(poly2, p)
                        if d < best[0]:
                            best = (d, q, gj)
                d, q, gj = best
                if q is None or d < lo or d >= hi:
                    continue
                # A GAP FACES ITS OTHER SIDE: the segment must leave this outline within 60 deg of
                # its outward normal. A far-side sample measures THROUGH its own object, and a
                # wall meeting a rock at a corner measures ALONG the wall -- neither is a gap,
                # and the first two versions of this instrument reported both as squeezes.
                if (q[0] - p[0]) * nrm[0] + (q[1] - p[1]) * nrm[1] < 0.5 * d:
                    continue
                m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
                if not stand_in_gap(m[0], m[1], d):
                    continue
                key = tuple(sorted((gi, gj)))
                if key not in seen or d < seen[key]["gap_m"]:
                    seen[key] = {"a": key[0], "b": key[1], "gap_m": round(d, 3), "at_uv": [round(m[0], 2), round(m[1], 2)]}
    return sorted(seen.values(), key=lambda x: x["gap_m"])


def stand_radius(w, slack):
    """How far from a gap's midpoint his centre can be while standing in a gap of width w."""
    return max(w / 2.0 - CAPSULE_R, 0.0) + slack
