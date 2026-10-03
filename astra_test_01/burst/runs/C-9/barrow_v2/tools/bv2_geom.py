"""barrow_v2 (lane BX): plain-python 2D geometry for the layout and its validator.

Sim frame throughout: +x east, +y SOUTH, metres, origin = player start (0, 0).
No third-party geometry library (shapely is not installed on this host); every routine here is
small enough to read, and the validator's negative control exercises the containment paths.
"""
import math

TAU = 2.0 * math.pi


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points):
    """Andrew's monotone chain. Returns the hull CCW in a y-up sense (i.e. signed area > 0 in the
    raw (x, y) numbers). Collinear points are dropped."""
    pts = sorted(set((float(p[0]), float(p[1])) for p in points))
    if len(pts) <= 2:
        return pts
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def signed_area(poly):
    s = 0.0
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        s += x0 * y1 - x1 * y0
    return s / 2.0


def area(poly):
    return abs(signed_area(poly))


def extents(poly):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return {"x_min": min(xs), "x_max": max(xs), "y_min": min(ys), "y_max": max(ys),
            "width_x": max(xs) - min(xs), "depth_y": max(ys) - min(ys)}


def is_convex(poly, eps=1e-9):
    n = len(poly)
    sgn = 0
    for i in range(n):
        c = cross(poly[i], poly[(i + 1) % n], poly[(i + 2) % n])
        if abs(c) <= eps:
            continue
        s = 1 if c > 0 else -1
        if sgn == 0:
            sgn = s
        elif s != sgn:
            return False
    return True


def point_in_poly(p, poly):
    """Even-odd ray cast; boundary points may go either way (callers use clearances)."""
    x, y = p
    inside = False
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        if (y0 > y) != (y1 > y):
            xi = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            if xi > x:
                inside = not inside
    return inside


def dist_point_seg(p, a, b):
    ax, ay = a
    bx, by = b
    px, py = p
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    qx, qy = ax + t * dx, ay + t * dy
    return math.hypot(px - qx, py - qy)


def dist_to_boundary(p, poly):
    n = len(poly)
    return min(dist_point_seg(p, poly[i], poly[(i + 1) % n]) for i in range(n))


def signed_clearance(p, poly):
    """+ distance to the boundary if inside, - if outside."""
    d = dist_to_boundary(p, poly)
    return d if point_in_poly(p, poly) else -d


def disc_clearance(c, r, poly):
    """Smallest gap between a disc and the outside of `poly`: >= 0 means the disc is entirely
    inside (exact for any simple polygon: inside iff the centre is inside and no edge comes
    within r)."""
    return signed_clearance(c, poly) - r


def segs_intersect(p1, p2, q1, q2):
    d1 = cross(q1, q2, p1)
    d2 = cross(q1, q2, p2)
    d3 = cross(p1, p2, q1)
    d4 = cross(p1, p2, q2)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True

    def on(a, b, c):
        return min(a[0], b[0]) - 1e-12 <= c[0] <= max(a[0], b[0]) + 1e-12 and \
            min(a[1], b[1]) - 1e-12 <= c[1] <= max(a[1], b[1]) + 1e-12
    if d1 == 0 and on(q1, q2, p1):
        return True
    if d2 == 0 and on(q1, q2, p2):
        return True
    if d3 == 0 and on(p1, p2, q1):
        return True
    if d4 == 0 and on(p1, p2, q2):
        return True
    return False


def seg_seg_dist(p1, p2, q1, q2):
    if segs_intersect(p1, p2, q1, q2):
        return 0.0
    return min(dist_point_seg(p1, q1, q2), dist_point_seg(p2, q1, q2),
               dist_point_seg(q1, p1, p2), dist_point_seg(q2, p1, p2))


def seg_poly_dist(a, b, poly):
    """0 if the segment touches/crosses/lies inside the polygon, else the gap."""
    if point_in_poly(a, poly) or point_in_poly(b, poly):
        return 0.0
    n = len(poly)
    return min(seg_seg_dist(a, b, poly[i], poly[(i + 1) % n]) for i in range(n))


def poly_poly_gap(P, Q):
    """0 if the polygons overlap or touch, else the separation."""
    if any(point_in_poly(p, Q) for p in P) or any(point_in_poly(q, P) for q in Q):
        return 0.0
    n, m = len(P), len(Q)
    return min(seg_seg_dist(P[i], P[(i + 1) % n], Q[j], Q[(j + 1) % m])
               for i in range(n) for j in range(m))


def poly_inside_clearance(P, Q):
    """Min signed clearance of P's vertices and edges inside Q (>= 0: P entirely inside Q,
    assuming Q has no vertex inside P, which holds when Q is convex and P's vertices are inside)."""
    return min(signed_clearance(p, Q) for p in P)


def ellipse_poly(cx, cy, a, b, rot_deg=0.0, n=48):
    r = math.radians(rot_deg)
    cr, sr = math.cos(r), math.sin(r)
    out = []
    for k in range(n):
        t = TAU * k / n
        x, y = a * math.cos(t), b * math.sin(t)
        out.append((cx + x * cr - y * sr, cy + x * sr + y * cr))
    return out


def rect_poly(cx, cy, length, width, rot_deg=0.0):
    """Rectangle with `length` along the local x axis rotated by rot_deg (sim frame: rot measured
    from +x toward +y, i.e. clockwise on a north-up map)."""
    r = math.radians(rot_deg)
    ux, uy = math.cos(r), math.sin(r)
    vx, vy = -uy, ux
    hl, hw = length / 2.0, width / 2.0
    return [(cx + sx * hl * ux + sy * hw * vx, cy + sx * hl * uy + sy * hw * vy)
            for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]


def offset_hull(points, r, n=96):
    """Convex hull of points buffered by r (Minkowski sum with a disc, sampled every 360/n deg;
    the chord sag at n=96 is r*(1-cos(1.875 deg)) = 0.00054 r)."""
    cloud = [(x + r * math.cos(TAU * k / n), y + r * math.sin(TAU * k / n))
             for (x, y) in points for k in range(n)]
    return convex_hull(cloud)


def compass_deg(x, y):
    """Bearing clockwise from north in the sim frame (+y south, so north = -y)."""
    return math.degrees(math.atan2(x, -y)) % 360.0


def rnd(v, k=4):
    if isinstance(v, (list, tuple)):
        return [rnd(e, k) for e in v]
    return round(float(v), k)
