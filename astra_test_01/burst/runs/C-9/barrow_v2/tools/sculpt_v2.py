"""barrow_v2 BIOME-SCULPT (R-C9-149a, Matt): the greybox carries the land's real shape.

Matt: "I'm concerned about the grey box.. it doesn't seem to take into account the biomes that will be
covering it... everything looks man made and square."

This module turns the validated plan into sculpted geometry, deterministically (fixed seeds):
  * organic_floor()   the walkable edge: the disc hull + 1 m as an INNER bound, bulging outward per biome
                      (N barrow toe + drifts, W ragged shingle/ice shore, S broken cliff lip with bites and
                      spurs, E/SE trodden yard edge against snowbanks); zero bulge where the stair lands
  * build()           the terrain heightfield (0 on the floor, relief outside), rocks, groves, the ruined
                      man-made pieces as beams/blobs, and the walk-over ground detail inside the floor

Everything that is rendered is emitted as data (layout["sculpt"]) so the validator can prove it: beams
and blobs taller than walk-over must lie outside the floor; the heightfield must be exactly 0 on it.
Sim frame: +x east, +y SOUTH, z up.
"""
import math
import os

import numpy as np

import bv2_geom as G

TAU = 2 * math.pi
EXT = {"x0": -62.0, "x1": 66.0, "y0": -74.0, "y1": 62.0}
HF_PPM = 2.0                    # heightfield samples per metre (0.5 m grid)
SEA_FLOOR_Z = -7.8              # under the sea plane (-7.5, R-C9-154)
WALKOVER = 0.35                 # interior ground detail never exceeds this (the validator's limit is 0.40)
FLAT_MAX = 0.15                 # R-C9-155: the floor (and the exit lanes) carry only flat marks + sparse tufts <= this
TUFT_CAP_PER_M2 = 0.015         # R-C9-155: sparse -- at most 1.5 tufts per 100 m2 of floor
STRUCT_BEAMS = {"door_post", "lintel", "capstone", "kerb_step", "keel", "rib", "plank", "rail", "stem", "mast", "post", "rafter",
                "fallen", "plate", "ridge", "board", "porch_post", "porch_post_front", "porch_eave_side", "porch_eave",
                "porch_ridge", "porch_board", "finial", "gable_plank", "door_leaf", "gable_rafter", "gable_collar",
                "brazier_stand", "stake", "birch"}
STRUCT_BLOBS = {"head", "finial_head", "door_dark", "rubble", "bowl", "flame", "crown", "stone"}


# ------------------------------------------------------------------ small helpers
def unit(x, y):
    L = math.hypot(x, y)
    return (x / L, y / L)


class Noise:
    """Deterministic smooth 2D value noise as a sum of random-phase plane waves."""

    def __init__(self, seed, n=7, base_wl=9.0):
        r = np.random.default_rng(seed)
        self.k = []
        for i in range(n):
            wl = base_wl / (1.7 ** i)
            ang = r.uniform(0, TAU)
            self.k.append((math.cos(ang) * TAU / wl, math.sin(ang) * TAU / wl, r.uniform(0, TAU), 0.62 ** i))
        self.norm = sum(k[3] for k in self.k)

    def __call__(self, x, y):
        s = 0.0
        for kx, ky, ph, a in self.k:
            s = s + a * np.sin(kx * x + ky * y + ph)
        return s / self.norm          # about [-1, 1]


def resample(poly, step):
    out = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        L = math.dist(a, b)
        k = max(1, int(math.ceil(L / step)))
        for j in range(k):
            t = j / k
            out.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
    return out


def poly_mask(poly, X, Y):
    inside = np.zeros(X.shape, dtype=bool)
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        if y0 == y1:
            continue
        cond = (y0 > Y) != (y1 > Y)
        xi = x0 + (Y - y0) * (x1 - x0) / (y1 - y0)
        inside ^= cond & (xi > X)
    return inside


def dist_to_poly_edges(poly, X, Y):
    d = np.full(X.shape, np.inf)
    n = len(poly)
    for i in range(n):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % n]
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy or 1e-12
        t = np.clip(((X - ax) * dx + (Y - ay) * dy) / L2, 0, 1)
        d = np.minimum(d, np.hypot(X - (ax + t * dx), Y - (ay + t * dy)))
    return d


def polyline_dist(pl, X, Y):
    d = np.full(np.shape(X), np.inf)
    for (ax, ay), (bx, by) in zip(pl[:-1], pl[1:]):
        dx, dy = bx - ax, by - ay
        t = np.clip(((X - ax) * dx + (Y - ay) * dy) / (dx * dx + dy * dy), 0, 1)
        d = np.minimum(d, np.hypot(X - (ax + t * dx), Y - (ay + t * dy)))
    return d


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def compass(x, y):
    return (np.degrees(np.arctan2(x, -y)) + 360.0) % 360.0


def sector_w(c, lo, hi, feather=18.0):
    """1 inside the compass sector [lo, hi] (wrapping), falling to 0 over `feather` degrees."""
    c = np.asarray(c, dtype=float)
    mid = (lo + (((hi - lo) % 360.0) / 2.0)) % 360.0
    half = ((hi - lo) % 360.0) / 2.0
    d = np.abs(((c - mid) + 180.0) % 360.0 - 180.0)
    return np.clip(1.0 - (d - half) / feather, 0.0, 1.0)


# ------------------------------------------------------------------ 1. the organic walkable edge
def organic_floor(disc_hull, protect_pts, p03, seed=149):
    """Bulge the disc hull OUTWARD per biome. `protect_pts`: list of (x, y, radius_m, cap_m) where the bulge
    is capped (cap 0 = flush with the hull: the stair's landing; small caps at the deliverers' doors).
    Returns (polygon, offsets, info)."""
    pts = resample(disc_hull, 0.5)
    n = len(pts)
    # outward vertex normals (the hull is CCW in raw numbers; outward = right of the travel direction)
    nrm = []
    for i in range(n):
        a, b = pts[i - 1], pts[(i + 1) % n]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty) or 1.0
        nx, ny = ty / L, -tx / L
        if nx * pts[i][0] + ny * pts[i][1] < 0:
            nx, ny = -nx, -ny
        nrm.append((nx, ny))
    s = np.arange(n) * 0.5
    P = np.array(pts)
    c = compass(P[:, 0], P[:, 1])
    r = np.random.default_rng(seed)
    ph = r.uniform(0, TAU, 12)
    north = np.clip(1.3 + 0.9 * np.sin(s / 6.5 + ph[0]) + 0.5 * np.sin(s / 2.4 + ph[1]) + 0.25 * np.sin(s / 1.1 + ph[2]), 0.15, None)
    west = np.clip(1.6 + 1.0 * np.sin(s / 3.3 + ph[3]) + 0.75 * np.sin(s / 1.35 + ph[4]) + 0.45 * np.sin(s / 0.62 + ph[5]), 0.1, None)
    sq = np.sin(s / 2.9 + ph[6])
    south = np.clip(1.2 + 1.5 * np.sign(sq) * np.abs(sq) ** 0.35 + 0.5 * np.sin(s / 1.05 + ph[7]) + 0.3 * np.sin(s / 0.55 + ph[8]), 0.0, None)
    east = np.clip(0.28 + 0.18 * np.sin(s / 1.8 + ph[9]) + 0.12 * np.sin(s / 0.8 + ph[10]), 0.02, None)
    wN = sector_w(c, 300, 60)
    wW = sector_w(c, 205, 300)
    wS = sector_w(c, 150, 205)
    wE = sector_w(c, 60, 150)
    wsum = wN + wW + wS + wE + 1e-9
    f = (north * wN + west * wW + south * wS + east * wE) / wsum
    # protection: within radius R of a protect point the bulge is capped, feathered over 4 m of arc
    for (px, py, R, cap) in protect_pts:
        d = np.hypot(P[:, 0] - px, P[:, 1] - py)
        w = np.clip(1.0 - (d - R) / 4.0, 0.0, 1.0)
        f = f * (1 - w) + np.minimum(f, cap) * w
    # light smoothing (3-tap), never inward
    f = np.clip((np.roll(f, 1) + 2 * f + np.roll(f, -1)) / 4.0, 0.0, None)
    for (px, py, R, cap) in protect_pts:
        d = np.hypot(P[:, 0] - px, P[:, 1] - py)
        f = np.where(d <= R, np.minimum(f, cap), f)
    out = [(pts[i][0] + nrm[i][0] * f[i], pts[i][1] + nrm[i][1] * f[i]) for i in range(n)]
    info = {"resample_m": 0.5, "n_vertices": n, "bulge_m": {"min": round(float(f.min()), 3), "max": round(float(f.max()), 3),
                                                            "mean": round(float(f.mean()), 3)},
            "biomes": {"N": "barrow toe and drifts: 0.15-2.8 m", "W": "ragged shingle/ice shore, high-frequency: 0.1-3.5 m",
                       "S": "broken cliff lip, square-wave bites and spurs: 0-3.4 m", "E/SE": "trodden hall-yard edge: 0.02-0.58 m"},
            "protected": [{"at": [round(px, 3), round(py, 3)], "radius_m": R, "cap_m": cap} for (px, py, R, cap) in protect_pts]}
    return out, f, info


# ------------------------------------------------------------------ 2. the build
class Builder:
    def __init__(self, L, ctx):
        self.L = L
        self.ctx = ctx
        self.blobs = []
        self.beams = []
        self.features = []
        self.rng = np.random.default_rng(1491)
        # R-C9-155 ("v1 method"): structures are MODEL SLOTS now (layout["models"]). Their procedural beams and
        # blobs are no longer rendered; the few that carry placement (stakes, birches, stones) are CAPTURED
        # as slot instances instead.
        self.captured = {}
        self.cluster_rocks = {}
        w = int(round((EXT["x1"] - EXT["x0"]) * HF_PPM)) + 1
        hgt = int(round((EXT["y1"] - EXT["y0"]) * HF_PPM)) + 1
        self.gx = EXT["x0"] + np.arange(w) / HF_PPM
        self.gy = EXT["y0"] + np.arange(hgt) / HF_PPM
        self.X, self.Y = np.meshgrid(self.gx, self.gy)
        self.H = None

    # ---- feature/geometry emitters ----
    def feat(self, fid, kind, poly, z0, z1, blocks, note, **kw):
        d = {"id": fid, "kind": kind, "footprint": G.rnd(poly), "z_bottom_m": round(float(z0), 4), "z_top_m": round(float(z1), 4),
             "blocks_movement": blocks, "blocks_sight": blocks and z1 > 0.4, "render": "sculpt", "note": note,
             "placement": "OUTSIDE the walkable edge" if blocks else "INSIDE the floor (walk-over)"}
        d.update(kw)
        self.features.append(d)

    def blob(self, kind, c, rx, ry, top, base, rot, rgb, proto="rock", fid=None, blocks=None, note=""):
        """An ellipsoid (rx, ry horizontal) whose visible part runs from `base` to `top`; centre sits
        so the ellipsoid's equator is at max(base, top - 2*rz) (half-buried for low ground detail)."""
        if kind in STRUCT_BLOBS:
            self.captured.setdefault(kind, []).append({"c": [round(c[0], 3), round(c[1], 3)], "r": [round(rx, 3), round(ry, 3)],
                                                       "top": round(float(top), 3), "base": round(float(base), 3), "rot": round(float(rot), 2)})
            return None
        rz = max(0.02, (top - base))
        cz = top - rz if kind not in ("crown",) else top - rz
        b = {"k": kind, "c": [round(c[0], 3), round(c[1], 3)], "cz": round(float(cz), 3), "r": [round(rx, 3), round(ry, 3), round(float(rz), 3)],
             "rot": round(rot, 2), "rgb": [round(v, 3) for v in rgb], "proto": proto, "top": round(float(top), 3)}
        self.blobs.append(b)
        if fid:
            poly = G.ellipse_poly(c[0], c[1], rx, ry, rot, 16)
            self.feat(fid, kind, poly, base, top, top > WALKOVER if blocks is None else blocks, note)
        return b

    def beam(self, a, b, w, t, rgb, kind="timber", xh=None):
        """A box from a to b (its length axis), w across (horizontal, perpendicular to the length; or along
        the hint `xh` for vertical members), t the remaining (roughly vertical) extent."""
        d = {"k": kind, "a": [round(v, 3) for v in a], "b": [round(v, 3) for v in b], "w": round(w, 3), "t": round(t, 3),
             "rgb": [round(v, 3) for v in rgb]}
        if kind in STRUCT_BEAMS:
            self.captured.setdefault(kind, []).append(d)
            return
        if xh is not None:
            d["xh"] = [round(xh[0], 4), round(xh[1], 4)]
        self.beams.append(d)

    def hz(self, x, y):
        fx = (x - EXT["x0"]) * HF_PPM
        fy = (y - EXT["y0"]) * HF_PPM
        i0 = int(np.clip(math.floor(fx), 0, self.H.shape[1] - 2))
        j0 = int(np.clip(math.floor(fy), 0, self.H.shape[0] - 2))
        tx, ty = fx - i0, fy - j0
        h00, h10 = self.H[j0, i0], self.H[j0, i0 + 1]
        h01, h11 = self.H[j0 + 1, i0], self.H[j0 + 1, i0 + 1]
        return float((h00 * (1 - tx) + h10 * tx) * (1 - ty) + (h01 * (1 - tx) + h11 * tx) * ty)

    # ---- the heightfield ----
    def terrain(self):
        L, c = self.L, self.ctx
        X, Y = self.X, self.Y
        floor = L["floor"]["polygon"]
        inF = poly_mask(floor, X, Y)
        dF = dist_to_poly_edges(floor, X, Y)
        dout = np.where(inF, 0.0, dF)
        land = poly_mask(L["land"]["polygon"], X, Y)
        ice = poly_mask(L["shore_ice"]["polygon"], X, Y) & ~land
        cmp_ = compass(X, Y)
        n1, n2, n3 = Noise(11, 7, 26.0), Noise(12, 6, 9.0), Noise(13, 5, 3.5)
        wN = sector_w(cmp_, 300, 60, 25)
        wW = sector_w(cmp_, 205, 300, 20)
        wE = sector_w(cmp_, 60, 150, 20)
        # rolling snow slopes rising away from the edge, with wind-sculpted drifts
        roll = smoothstep(0.0, 18.0, dout) * (3.2 + 2.4 * n1(X, Y) + 0.8 * n2(X, Y))
        drift_dir = np.sin((X * 0.42 + Y * 0.91) / 2.6 + 2.0 * n2(X, Y))
        drifts = 0.75 * np.clip(drift_dir, 0, None) ** 3 * smoothstep(0.6, 4.0, dout)
        hN = roll + drifts
        # the west: shingle beach falling to the shore ice
        hW = -0.45 * smoothstep(0.0, 6.0, dout) + 0.08 * n3(X, Y) * smoothstep(0.0, 2.0, dout)
        # the east: the yard -- a trodden flat with a snowbank berm against the edge, then slopes
        bank = 0.95 * np.exp(-((dout - 1.9) / 0.85) ** 2) * (0.75 + 0.25 * n3(X, Y))
        for gx_, gy_ in c["bank_gaps"]:
            bank = bank * np.clip((np.hypot(X - gx_, Y - gy_) - 4.0) / 2.5, 0, 1)
        hE = 0.12 * n3(X, Y) * smoothstep(0, 2, dout) + bank + smoothstep(14.0, 30.0, dout) * (2.4 + 1.4 * n1(X, Y))
        ws = wN + wW + wE + 1e-9
        H = (hN * wN + hW * wW + hE * wE) / ws
        H = np.where(land, H, SEA_FLOOR_Z)
        # the barrow: a weathered grassy mound with an irregular outline and a cut passage
        m = c["mound"]
        dx, dy = X - m["c"][0], Y - m["c"][1]
        cr, sr = math.cos(math.radians(m["rot"])), math.sin(math.radians(m["rot"]))
        u = (dx * cr + dy * sr) / m["a"]
        v = (-dx * sr + dy * cr) / m["b"]
        th = np.arctan2(v, u)
        rad = 1.0 + 0.07 * np.sin(3 * th + 0.4) + 0.05 * np.sin(5 * th + 1.9) + 0.03 * np.sin(9 * th)
        rho = np.hypot(u, v) / rad
        mound = m["rise"] * np.clip(1 - rho ** 2, 0, None) ** 0.55 * (1 + 0.06 * n2(X, Y)) + 0.25 * np.clip(1 - rho, 0, 1) * n3(X, Y)
        H = np.where(land, np.maximum(H, mound), H)
        # the passage: cut into the mound behind the door
        pd = c["passage"]
        du = (X - pd["c"][0]) * pd["u"][0] + (Y - pd["c"][1]) * pd["u"][1]
        dv = (X - pd["c"][0]) * pd["v"][0] + (Y - pd["c"][1]) * pd["v"][1]
        cut = (np.abs(dv) <= pd["half_w"]) & (du >= -0.6) & (du <= pd["len"])
        H = np.where(cut, np.minimum(H, 0.0), H)
        # (R-C9-154) the forecourt before the door: levelled flat, the full width of the portal + kerb
        fc = (np.abs(dv) <= pd.get("forecourt_half_w", 0)) & (du >= -pd.get("forecourt_back", 0)) & (du <= 0.4)
        H = np.where(fc & land, np.minimum(H, 0.0), H)
        # the mound's face either side of the portal is cut back to a steep revetted face
        face = (np.abs(dv) <= pd.get("forecourt_half_w", 0) + 4.0) & (du > 0.4) & (du < 2.5)
        H = np.where(face & land & ~cut, np.minimum(H, 1.2 + (du - 0.4) * 2.6), H)
        # the hall stands on a levelled yard
        hall = poly_mask(c["hall_pad"], X, Y)
        H = np.where(hall & land, np.minimum(H, 0.05), H)
        # shore ice (W): a shelf at -0.45 with pressure texture, its seaward edge breaking down to the water
        # over ~7 m (no vertical ice wall); and the land's own coast (outside the S cliff) slopes into the sea
        ice_poly = L["shore_ice"]["polygon"]
        d_ice_edge = dist_to_poly_edges(ice_poly, X, Y)
        d_land_edge = dist_to_poly_edges(L["land"]["polygon"], X, Y)
        ice_h = -0.45 + 0.05 * n3(X, Y) + (SEA_FLOOR_Z + 0.45) * (1 - smoothstep(0.0, 9.0, d_ice_edge)) * smoothstep(1.5, 4.0, d_land_edge)
        H = np.where(ice, ice_h, H)
        coast = land & ~inF & ~((cmp_ > 140) & (cmp_ < 220))
        H = np.where(coast, SEA_FLOOR_Z + (H - SEA_FLOOR_Z) * smoothstep(0.0, 7.0, d_land_edge), H)
        # the south: a broken cliff. Sea cells near the lip get ledges at random tiers (fractured faces)
        sea_near = (~land) & (~ice) & (dout < 2.2) & (cmp_ > 105) & (cmp_ < 250)
        # (R-C9-154) no ledge tiers in front of the cave, the ledge or the stair: they must read clear
        for zq in c.get("clear_zones", []):
            sea_near &= ~(poly_mask(zq, X, Y) | (dist_to_poly_edges(zq, X, Y) < 3.0))
        tier = n2(X * 0.6, Y * 0.6) + 0.25 * n3(X * 0.5, Y * 0.5)      # broad, contiguous ledges (not per-cell teeth)
        ledge_h = np.where(tier > 0.35, -2.0, np.where(tier > -0.1, -4.3, SEA_FLOOR_Z))
        ledge_h = np.where(dout < 1.2, ledge_h, np.where(tier > 0.55, -5.6, SEA_FLOOR_Z))
        H = np.where(sea_near, ledge_h, H)
        # the stair: the ledge at sea level, the flight and landing carved out (their own geometry fills them)
        st = L["stair"]
        led = poly_mask(st["bottom_landing"]["polygon"], X, Y)
        H = np.where(led, st["bottom_landing"]["z_m"] - 0.15, H)        # just under the ledge prism (no z-fight)
        for part in ("flight", "top_landing"):
            msk = poly_mask(st[part]["polygon"], X, Y)
            H = np.where(msk, SEA_FLOOR_Z, H)
        wall = poly_mask(c["wall_rock"], X, Y)
        H = np.where(wall, SEA_FLOOR_Z, H)
        # (R-C9-155) the exit lanes are trodden flat ground where they run outside the floor
        for ln in L.get("lanes", []):
            lm = poly_mask(ln["polygon"], X, Y) | (dist_to_poly_edges(ln["polygon"], X, Y) < 0.6)
            H = np.where(lm & ~inF & (H > -1.0), np.minimum(H, 0.05), H)
        # the floor and a 0.35 m apron are exactly flat at 0 (the sim's plane)
        flat = inF | (dF <= 0.35)
        H = np.where(flat & (land | inF), 0.0, H)
        H = np.where(inF, 0.0, H)
        self.H = H.astype(np.float32)
        self.inF = inF
        self.land = land
        return H

    # ---- dressing ----
    def rock(self, c, size, top_frac, rgb, fid, note, z0=None, sink=0.35, proto="rock"):
        z0 = self.hz(*c) if z0 is None else z0
        rx = size * self.rng.uniform(0.75, 1.25)
        ry = size * self.rng.uniform(0.6, 1.0)
        top = z0 + size * top_frac
        base = z0 - size * sink
        self.blob("rock", c, rx, ry, top, base, float(self.rng.uniform(0, 180)), rgb, proto, fid, True, note)

    def outside_ok(self, c, r, margin=1.0):
        """True when a disc of radius r + margin at c is clear of the floor."""
        floor = self.L["floor"]["polygon"]
        ok = G.disc_clearance(c, r + margin, floor) < 0 and not G.point_in_poly(c, floor) and \
            G.dist_to_boundary(c, floor) > r + margin
        for ln in self.L.get("lanes", []):
            if not ok:
                break
            q = ln["polygon"]
            ok = (not G.point_in_poly(c, q)) and G.dist_to_boundary(c, q) > r + 0.6
        return ok

    def dressing(self):
        L, c, rng = self.L, self.ctx, self.rng
        floor = L["floor"]["polygon"]
        ROCK = (0.50, 0.49, 0.47)
        DARK = (0.17, 0.14, 0.12)
        TIMBER = (0.34, 0.25, 0.17)
        CHAR = (0.13, 0.11, 0.10)
        # -- rock outcrops and boulder clusters on the slopes (outside the floor) --
        k = 0
        for ci, (cx, cy, n, size) in enumerate(c["rock_clusters"]):
            for j in range(n):
                p = (cx + rng.normal(0, size * 1.3), cy + rng.normal(0, size * 1.3))
                s_ = size * rng.uniform(0.45, 1.1)
                if not self.outside_ok(p, s_ * 1.3, 1.0):
                    continue
                k += 1
                self.rock(p, s_, rng.uniform(0.5, 1.1), tuple(np.clip(np.array(ROCK) + rng.normal(0, 0.035), 0, 1)),
                          f"rock_{k}", "rock outcrop / boulder cluster on the slopes, outside the edge")
                self.cluster_rocks.setdefault(ci, []).append(self.blobs[-1])
        # -- the cliff foot: fallen boulders at sea level --
        st = L["stair"]
        keep = [st[k]["polygon"] for k in ("flight", "top_landing", "bottom_landing")]

        def clear_of_stair(p, r):
            return all((not G.point_in_poly(p, q)) and G.dist_to_boundary(p, q) > r + 2.5 for q in keep)
        for (px, py) in c["cliff_foot_rocks"]:
            s_ = rng.uniform(0.6, 1.4)
            if self.outside_ok((px, py), s_ * 1.3, 0.3) and clear_of_stair((px, py), s_ * 1.3):
                k += 1
                self.rock((px, py), s_, 0.8, ROCK, f"rock_{k}", "fallen boulder at the cliff foot", z0=-4.5)
        # -- the sea-cave mouth's rock frame (R-C9-154): rough jambs at both ends and a broken rock brow
        #    across the top, hugging the face, so the dark opening reads as a mouth in the cliff --
        fr = c.get("cave_frame", [])
        if fr:
            zl = L["stair"]["bottom_landing"]["z_m"]
            for end in (fr[0], fr[-1]):
                (px, py), (nx, ny) = end
                for k in range(3):
                    q = (px + nx * (0.75 + 0.2 * k), py + ny * (0.75 + 0.2 * k))
                    self.blob("rock", q, 0.7, 0.55, zl + 2.4 * (k + 1), zl - 0.3 + 2.2 * k, float(rng.uniform(0, 180)), ROCK, "rock")
            for i in range(2, len(fr) - 2, 5):              # a broken brow of a few long, flat slabs
                (px, py), (nx, ny) = fr[i]
                q = (px + nx * 0.75, py + ny * 0.75)
                ang = math.degrees(math.atan2(nx, -ny))
                self.blob("rock", q, 1.6, 0.55, -0.05, -0.85, ang + float(rng.normal(0, 6)), tuple(np.array(ROCK) * 0.9), "slab")
        # -- ice floes off the shelf --
        for i, (px, py) in enumerate(c["floes"]):
            self.blob("floe", (px, py), rng.uniform(1.0, 2.6), rng.uniform(0.8, 2.0), -4.25, -4.6, float(rng.uniform(0, 180)),
                      (0.80, 0.86, 0.92), "slab", f"floe_{i + 1}", True, "ice floe on the open water")
        # -- groves: birch (pale trunks, twiggy crowns) and juniper masses --
        t = 0
        for gi, (gx_, gy_, kind, n, spread) in enumerate(c["groves"]):
            for j in range(n):
                p = (gx_ + rng.normal(0, spread), gy_ + rng.normal(0, spread))
                cr_ = 1.8 if kind == "birch" else rng.uniform(0.9, 1.6)
                if not self.outside_ok(p, cr_, 2.5):
                    continue
                t += 1
                z0 = self.hz(*p)
                if kind == "birch":
                    ht = rng.uniform(6.0, 9.0)
                    lean = rng.normal(0, 0.25, 2)
                    self.beam((p[0], p[1], z0 - 0.3), (p[0] + lean[0], p[1] + lean[1], z0 + ht), 0.28, 0.28, (0.86, 0.84, 0.80), "birch")
                    self.captured["birch"][-1]["grove"] = gi
                    for q in range(3):
                        zc = z0 + ht * rng.uniform(0.62, 0.95)
                        o = rng.normal(0, 0.5, 2)
                        rr = rng.uniform(1.1, 1.9)
                        self.blob("crown", (p[0] + lean[0] * 0.8 + o[0], p[1] + lean[1] * 0.8 + o[1]), rr, rr * 0.9, zc + rr * 0.8, zc - rr * 0.8,
                                  float(rng.uniform(0, 180)), (0.55, 0.47, 0.40), "crown")
                    self.feat(f"birch_{t}", "tree", G.ellipse_poly(p[0], p[1], cr_ + 0.6, cr_ + 0.6, 0, 16), z0, z0 + ht, True,
                              "birch (bare winter crown), outside the edge")
                else:
                    ht = rng.uniform(1.2, 2.6)
                    self.blob("juniper", p, cr_, cr_ * rng.uniform(0.7, 1.0), z0 + ht, z0 - 0.2, float(rng.uniform(0, 180)),
                              (0.20, 0.27, 0.20), "crown", f"juniper_{t}", True, "juniper mass, outside the edge")
        # -- the barrow: stone door (posts + lintel), the dark passage, kerb stones, standing stones --
        # (R-C9-154) the King's door, MONUMENTAL: massive uprights + lintel framing the clear opening, the
        # deep dark passage, a paved forecourt and a stepped kerb either side
        pd = c["passage"]
        dc = pd["door"]
        u, v = pd["u"], pd["v"]
        BW = pd["barrow"]
        STONE = (0.47, 0.46, 0.43)
        hw_o = BW["open_w"] / 2
        for sgn in (-1, 1):
            off = sgn * (hw_o + BW["post_w"] / 2 + 0.003)
            b0 = (dc[0] + v[0] * off + u[0] * BW["post_d"] / 2, dc[1] + v[1] * off + u[1] * BW["post_d"] / 2)
            self.beam((b0[0], b0[1], -0.4), (b0[0], b0[1], BW["open_h"] + 0.05), BW["post_w"], BW["post_d"], STONE, "door_post", xh=v)
        lz = BW["open_h"] + BW["lintel_t"] / 2
        lc = (dc[0] + u[0] * BW["post_d"] / 2, dc[1] + u[1] * BW["post_d"] / 2)
        span = hw_o + BW["post_w"] + 0.4
        self.beam((lc[0] - v[0] * span, lc[1] - v[1] * span, lz), (lc[0] + v[0] * span, lc[1] + v[1] * span, lz),
                  BW["post_d"] + 0.3, BW["lintel_t"], (0.43, 0.42, 0.39), "lintel")
        # a capstone course above the lintel, stepped back
        self.beam((lc[0] - v[0] * (span - 0.8) + u[0] * 0.5, lc[1] - v[1] * (span - 0.8) + u[1] * 0.5, lz + 1.05),
                  (lc[0] + v[0] * (span - 0.8) + u[0] * 0.5, lc[1] + v[1] * (span - 0.8) + u[1] * 0.5, lz + 1.05),
                  BW["post_d"], 0.8, (0.45, 0.44, 0.41), "capstone")
        plen = BW["passage_len"] + BW["post_d"] - 0.3
        pdc = (dc[0] + u[0] * (0.3 + plen / 2), dc[1] + u[1] * (0.3 + plen / 2))
        self.blob("dark", pdc, plen / 2, hw_o + 0.05, BW["open_h"], -0.1, math.degrees(math.atan2(u[1], u[0])), DARK, "box")
        # forecourt flagstones (flush) and the stepped kerb: two courses curving back either side
        fb = pd.get("forecourt_back", 2.0)
        for i in range(int(pd["forecourt_half_w"] * 2 / 1.1)):
            for j in range(int(fb / 1.0)):
                q = (dc[0] - u[0] * (j + 0.5) + v[0] * (-pd["forecourt_half_w"] + 0.55 + i * 1.1) + rng.normal(0, 0.05),
                     dc[1] - u[1] * (j + 0.5) + v[1] * (-pd["forecourt_half_w"] + 0.55 + i * 1.1) + rng.normal(0, 0.05))
                if self.outside_ok(q, 0.5, 0.0):
                    self.blob("flag", q, 0.5, 0.45, 0.10, -0.1, math.degrees(math.atan2(u[1], u[0])) + rng.normal(0, 4),
                              (0.55 + rng.normal(0, 0.03),) * 3, "slab")
        for sgn in (-1, 1):
            for tier, (back, ht) in enumerate(((0.2, 0.55), (1.3, 1.15))):
                for k in range(6):
                    lat0 = sgn * (pd["forecourt_half_w"] - 0.2 + k * 1.55 + tier * 0.3)
                    q0 = (dc[0] + u[0] * (back + k * 0.55) + v[0] * lat0, dc[1] + u[1] * (back + k * 0.55) + v[1] * lat0)
                    q1 = (q0[0] + v[0] * sgn * 1.45, q0[1] + v[1] * sgn * 1.45)
                    z0 = min(self.hz(*q0), self.hz(*q1))
                    if self.outside_ok(q0, 0.8, 0.2) and self.outside_ok(q1, 0.8, 0.2):
                        self.beam((q0[0], q0[1], z0 - 0.2 + ht / 2), (q1[0], q1[1], z0 - 0.2 + ht / 2), 0.9, ht + 0.4,
                                  (0.48 + rng.normal(0, 0.02),) * 3, "kerb_step")
        m = c["mound"]
        for i in range(22):
            th = TAU * i / 22 + rng.normal(0, 0.05)
            cr_, sr_ = math.cos(math.radians(m["rot"])), math.sin(math.radians(m["rot"]))
            uu, vv = math.cos(th) * m["a"] * 1.0, math.sin(th) * m["b"] * 1.0
            p = (m["c"][0] + uu * cr_ - vv * sr_, m["c"][1] + uu * sr_ + vv * cr_)
            if self.outside_ok(p, 0.8, 0.8) and math.dist(p, dc) > pd["forecourt_half_w"] + 6.0:
                self.rock(p, rng.uniform(0.5, 0.8), 0.9, (0.47, 0.47, 0.45), f"kerb_{i + 1}", "kerb stone round the mound's toe")
        for i, (p, ht) in enumerate(c["standing_stones"]):
            z0 = self.hz(*p)
            self.blob("stone", p, 0.55, 0.42, z0 + ht, z0 - 0.4, float(rng.uniform(0, 180)), (0.44, 0.44, 0.43), "tall",
                      f"standing_stone_{i + 1}", True, "standing stone on the barrow slope (stands up, so outside the edge)")
        # -- the wreck: heeled, broken, ice-locked --
        w = c["wreck"]
        ax_ = (math.cos(math.radians(w["rot"])), math.sin(math.radians(w["rot"])))
        lat = (-ax_[1], ax_[0])
        if lat[0] < 0:
            lat = (-lat[0], -lat[1])          # +lat = toward the floor (east): the high, rail side
        heel = math.radians(18.0)
        Lh = w["length"]

        def hullpt(s_, side, hfrac):
            """s_ in [0,1] bow->stern; side -1 low (west) / +1 high (east); hfrac in [0,1] keel->gunwale."""
            half = 2.3 * math.sqrt(max(0.0, 1 - (2 * s_ - 1) ** 2)) ** 0.8
            y_l = side * half * math.sin(hfrac * math.pi / 2)
            z_l = 1.7 * hfrac - 0.2
            yl2 = y_l * math.cos(heel) - z_l * math.sin(heel) * -1
            zl2 = y_l * math.sin(heel) + z_l * math.cos(heel)
            a_ = (s_ - 0.5) * Lh
            return (w["c"][0] + ax_[0] * a_ + lat[0] * yl2, w["c"][1] + ax_[1] * a_ + lat[1] * yl2, w["z"] + zl2)
        self.beam(hullpt(0.02, 0, 0), hullpt(0.98, 0, 0), 0.35, 0.35, TIMBER, "keel")
        for i in range(13):
            s_ = 0.06 + i * 0.07
            broken = i >= 10 and i % 2 == 0
            for side in (-1, 1):
                p0, p1, p2 = hullpt(s_, side, 0), hullpt(s_, side, 0.55), hullpt(s_, side, 1.0 if not broken else 0.7)
                self.beam(p0, p1, 0.18, 0.2, TIMBER, "rib")
                self.beam(p1, p2, 0.16, 0.18, TIMBER, "rib")
        for hf in (0.35, 0.7):
            for s0, s1 in ((0.04, 0.45), (0.5, 0.78)):
                self.beam(hullpt(s0, -1, hf), hullpt(s1, -1, hf), 0.08, 0.32, (0.38, 0.28, 0.19), "plank")
        self.beam(hullpt(0.05, 1, 1.0), hullpt(0.62, 1, 1.0), 0.2, 0.22, (0.40, 0.29, 0.19), "rail")
        bow = hullpt(0.0, 0, 0.2)
        self.beam(bow, (bow[0] - ax_[0] * 0.9, bow[1] - ax_[1] * 0.9, bow[2] + 2.4), 0.3, 0.3, TIMBER, "stem")
        self.blob("head", (bow[0] - ax_[0] * 1.2, bow[1] - ax_[1] * 1.2), 0.45, 0.3, bow[2] + 3.0, bow[2] + 2.2, 0, (0.30, 0.20, 0.13), "rock")
        mid = hullpt(0.45, 0, 0)
        self.beam(mid, (mid[0] - lat[0] * 1.5 + ax_[0] * 1.0, mid[1] - lat[1] * 1.5 + ax_[1] * 1.0, mid[2] + 5.0), 0.26, 0.26, TIMBER, "mast")
        for i in range(9):
            s_ = rng.uniform(0, 1)
            p = hullpt(s_, rng.choice([-1, 1]), 0)
            self.blob("ice", (p[0] + rng.normal(0, 0.8), p[1] + rng.normal(0, 0.8)), rng.uniform(1.0, 2.0), rng.uniform(0.7, 1.4), -0.15, -0.6,
                      float(rng.uniform(0, 180)), (0.82, 0.88, 0.93), "slab")
        # -- the hall: a charred, sagging, half-fallen timber frame, ONE building; porch on the great door --
        hl = c["hall"]
        A0, ane, nT, Dp = hl["sw"], hl["ane"], hl["nT"], hl["door"]
        Lhall, Dd = hl["length"], hl["depth"]

        def hp(s_, d_, z):          # s_ along the hall from its SW end, d_ outward from the west wall
            return (A0[0] + ane[0] * s_ + nT[0] * d_, A0[1] + ane[1] * s_ + nT[1] * d_, z)
        bays = np.arange(hl["gable_len"], Lhall + 0.01, 2.6)
        ridge_z = []
        for i, s_ in enumerate(bays):
            sag = 0.9 * math.sin(math.pi * (s_ - bays[0]) / (bays[-1] - bays[0] + 1e-9))
            fallen = s_ < hl["gable_len"] + 7.5            # the SW third has lost its roof
            for d_ in (0.0, Dd):
                hpost = 3.3 - (rng.uniform(0.6, 1.8) if (fallen and rng.uniform() < 0.6) else rng.uniform(0, 0.25))
                lean = rng.normal(0, 0.12, 2)
                self.beam(hp(s_, d_, -0.1), (hp(s_, d_, 0)[0] + lean[0], hp(s_, d_, 0)[1] + lean[1], hpost), 0.32, 0.32, CHAR, "post")
            rz = 6.4 - sag
            ridge_z.append(rz)
            if not fallen or i % 3 == 0:
                for d_ in (0.0, Dd):
                    self.beam(hp(s_, d_, 3.2), hp(s_, Dd / 2, rz), 0.22, 0.26, CHAR, "rafter")
            elif rng.uniform() < 0.7:          # fallen rafters, lying askew in the hall
                self.beam(hp(s_ + rng.normal(0, 0.4), 1.0, 0.15), hp(s_ + rng.normal(0, 0.8), Dd - 1.2, rng.uniform(0.4, 1.6)), 0.22, 0.24, CHAR, "fallen")
        for d_ in (0.0, Dd):
            self.beam(hp(bays[0] + 7.5, d_, 3.25), hp(bays[-1], d_, 3.15), 0.26, 0.3, CHAR, "plate")
        k0 = int(np.searchsorted(bays, hl["gable_len"] + 7.5))
        for i in range(k0, len(bays) - 1):
            self.beam(hp(bays[i], Dd / 2, ridge_z[i]), hp(bays[i + 1], Dd / 2, ridge_z[i + 1]), 0.28, 0.3, CHAR, "ridge")
        # surviving roof boards on the SE (camera-facing) slope of the NE bays, burnt through in patches
        for i in range(k0, len(bays) - 1):
            for j in range(5):
                if rng.uniform() < 0.35:
                    continue
                f0 = j / 5
                z_a = 3.2 + (ridge_z[i] - 3.2) * (1 - f0)
                d_a = Dd / 2 + (Dd / 2) * f0
                self.beam(hp(bays[i] + 0.1, d_a, z_a), hp(bays[i + 1] - 0.1, d_a, z_a), Dd / 2 / 5 * 1.25, 0.06, (0.22, 0.18, 0.14), "board")
        # back wall planks (SE wall, faces the camera), gappy and charred
        for s_ in np.arange(bays[0] + 7.5, Lhall, 0.55):
            if rng.uniform() < 0.3:
                continue
            ht = rng.uniform(1.4, 3.1)
            self.beam(hp(s_, Dd + 0.05, -0.1), hp(s_, Dd + 0.05, ht), 0.5, 0.12, (0.20, 0.16, 0.13), "plank", xh=ane)
        # the porch on the great door (BVP's form, GROWN by R-C9-154): front posts frame the clear opening;
        # eaves above it; the ridge runs OUT toward p04's patch and rises above the hall's roofline; carved
        # crossed finials on its outer gable; the doors stand open; braziers either side of a stone apron
        nin = (-nT[0], -nT[1])
        pc = hl["porch"]
        s_p = hl["door_s"] + pc["shift_ne"]
        hw, dep = pc["width"] / 2, pc["depth"]
        PW = 0.42
        for sv in (-1, 1):
            off = sv * (pc["open_w"] / 2 + PW / 2)
            for dd, role in ((0.25, "porch_post"), (dep - 0.25, "porch_post_front")):
                b0 = hp(s_p + off, -dd, 0.0)
                self.beam((b0[0], b0[1], -0.1), (b0[0], b0[1], pc["eave"]), PW, PW, TIMBER, role, xh=ane)
            self.beam(hp(s_p + sv * hw, 0.0, pc["eave"] + 0.15), hp(s_p + sv * hw, -dep - 0.5, pc["eave"] + 0.15), 0.26, 0.3, TIMBER, "porch_eave_side")
        fe = hp(s_p - hw, -dep + 0.25, pc["eave"] + 0.15)
        fe2 = hp(s_p + hw, -dep + 0.25, pc["eave"] + 0.15)
        self.beam(fe, fe2, 0.3, 0.3, TIMBER, "porch_eave")              # the front lintel beam over the opening
        self.beam(hp(s_p, 0.3, pc["ridge"]), hp(s_p, -dep - 0.5, pc["ridge"]), 0.3, 0.32, TIMBER, "porch_ridge")
        for sv in (-1, 1):
            for dd in np.linspace(0.0, dep + 0.5, 8):
                self.beam(hp(s_p + sv * (hw + 0.3), -dd, pc["eave"] + 0.05), hp(s_p, -dd, pc["ridge"] + 0.05), 0.5, 0.07, (0.31, 0.23, 0.15), "porch_board")
            # carved crossed finials: the barge boards cross at the apex and rise ~1.2 m above the ridge
            a_ = hp(s_p + sv * (hw + 0.3), -dep - 0.5, pc["eave"])
            b_ = hp(s_p - sv * 0.9, -dep - 0.5, pc["ridge"] + 1.25)
            self.beam(a_, b_, 0.18, 0.42, (0.28, 0.19, 0.12), "finial")
            hd = hp(s_p - sv * 1.0, -dep - 0.5, 0.0)
            self.blob("finial_head", (hd[0], hd[1]), 0.32, 0.22, pc["ridge"] + 1.55, pc["ridge"] + 1.05, 0, (0.30, 0.20, 0.12), "rock")
        # gable infill above the opening (planks between the eave beam and the barge boards)
        for k in range(5):
            f0 = (k + 0.5) / 5
            z_ = pc["eave"] + 0.3 + (pc["ridge"] - pc["eave"] - 0.4) * f0
            half = hw * (1 - f0)
            self.beam(hp(s_p - half, -dep + 0.3, z_), hp(s_p + half, -dep + 0.3, z_), 0.08, 0.5, (0.33, 0.24, 0.16), "gable_plank")
        # the doorway in the wall (dark, the full clear opening) and the two leaves swung open into the porch
        dd_ = hp(s_p, 0.02, 0.0)
        self.blob("door_dark", (dd_[0], dd_[1]), pc["open_w"] / 2, 0.10, pc["open_h"], -0.1, math.degrees(math.atan2(ane[1], ane[0])), DARK, "box")
        for sv in (-1, 1):
            hinge = hp(s_p + sv * pc["open_w"] / 2, -0.05, 0.0)
            leaf_end = hp(s_p + sv * (pc["open_w"] / 2 + 0.25), -pc["open_w"] / 2 + 0.1, 0.0)
            self.beam((hinge[0], hinge[1], pc["open_h"] / 2), (leaf_end[0], leaf_end[1], pc["open_h"] / 2), 0.14, pc["open_h"] - 0.1, (0.36, 0.25, 0.15), "door_leaf")
        # the stone apron (flush flags) and the braziers
        apron = c["apron"]
        ax0, ax1, bx1 = apron[0], apron[1], apron[2]
        for i in range(6):
            for j in range(2):
                fi, fj = (i + 0.5) / 6, (j + 0.5) / 2
                q = (ax0[0] + (ax1[0] - ax0[0]) * fi + (bx1[0] - ax1[0]) * fj, ax0[1] + (ax1[1] - ax0[1]) * fi + (bx1[1] - ax1[1]) * fj)
                self.blob("flag", q, 0.52, 0.34, 0.12, -0.1, math.degrees(math.atan2(ane[1], ane[0])) + rng.normal(0, 5),
                          (0.52 + rng.normal(0, 0.03),) * 3, "slab")
        for bc in c["braziers"]:
            self.beam((bc[0], bc[1], -0.1), (bc[0], bc[1], 1.5), 0.28, 0.28, (0.15, 0.13, 0.12), "brazier_stand")
            self.blob("bowl", bc, 0.55, 0.55, 1.85, 1.35, 0, (0.18, 0.16, 0.15), "slab")
            self.blob("flame", bc, 0.38, 0.38, 2.3, 1.7, 0, (0.98, 0.55, 0.15), "crown")
        # the fallen gable: the hall's own SW end, the A-frame fallen outward and lying on its rubble
        gl = hl["gable_len"]
        for d_ in (0.4, Dd - 0.4):
            self.beam(hp(gl * 0.2, d_, 0.2), hp(gl * 0.95, Dd / 2, 2.6), 0.3, 0.3, CHAR, "gable_rafter")
        for zf in (0.6, 1.2, 1.8):
            self.beam(hp(gl * 0.3 + zf * 0.6, 0.7 + zf * 0.6, zf * 0.9), hp(gl * 0.3 + zf * 0.6, Dd - 0.7 - zf * 0.6, zf * 0.9), 0.2, 0.25, CHAR, "gable_collar")
        for i in range(10):
            p = hp(rng.uniform(0.3, gl), rng.uniform(0.6, Dd - 0.6), 0)
            self.blob("rubble", (p[0], p[1]), rng.uniform(0.6, 1.2), rng.uniform(0.4, 0.9), rng.uniform(0.4, 1.1), -0.2, float(rng.uniform(0, 180)),
                      (0.16, 0.13, 0.11), "rock")
        # -- the palisade: leaning, gapped stakes along each run --
        for (a_, b_) in c["palisade_runs"]:
            Lr = math.dist(a_, b_)
            n_ = int(Lr / 0.48)
            for i in range(n_):
                if rng.uniform() < 0.22:
                    continue
                t_ = (i + 0.5) / n_
                p = (a_[0] + t_ * (b_[0] - a_[0]), a_[1] + t_ * (b_[1] - a_[1]))
                z0 = self.hz(*p)
                ht = rng.uniform(1.9, 3.2)
                lean = rng.normal(0, 0.18, 2)
                self.beam((p[0], p[1], z0 - 0.3), (p[0] + lean[0], p[1] + lean[1], z0 + ht), 0.22, 0.22, (0.27, 0.20, 0.14), "stake")
        # -- the stone circle: weathered, sunken stones (replace the slabs) --
        for s in c["circle_stones"]:
            ht = s["z_top_m"]
            cx_, cy_ = s["c"]
            self.blob("stone", (cx_, cy_), s["len"] / 2, s["wid"] / 2, ht, -0.25, s["rot"], (0.55, 0.55, 0.52), "rock")

    # ---- walk-over ground detail inside the floor ----
    def ground_detail(self):
        """R-C9-155 CLEAN FLOOR (the v1 Barrow's rule): the walkable floor carries only FLAT marks --
        footprint trails along the lanes and the path, wind ripples, cracks in the stream/mere ice -- and a
        SPARSE scatter of small tufts (<= FLAT_MAX, under TUFT_CAP_PER_M2, never in a lane)."""
        L, rng = self.L, self.rng
        floor = L["floor"]["polygon"]
        mere = L["mere"]["polygon"]
        lanes = [ln["polygon"] for ln in L.get("lanes", [])]
        counts = {}
        k = 0

        def on_floor(p, r):
            return G.point_in_poly(p, floor) and G.dist_to_boundary(p, floor) > r + 0.3

        def mark(kind, p, rx, ry, top, rot, rgb, proto="slab"):
            nonlocal k
            k += 1
            counts[kind] = counts.get(kind, 0) + 1
            self.blob(kind, p, rx, ry, top, -0.05, rot, rgb, proto, f"gd_{k}", False, "flat mark (R-C9-155 clean floor)")
        # footprint trails: down every lane and along the worn path
        trails = [ln["centreline"] for ln in L.get("lanes", [])] + [L["path"]["polyline"]]
        for tr in trails:
            for (ax_, ay_), (bx_, by_) in zip(tr[:-1], tr[1:]):
                Ls = math.dist((ax_, ay_), (bx_, by_))
                if Ls < 1e-6:
                    continue
                tx_, ty_ = (bx_ - ax_) / Ls, (by_ - ay_) / Ls
                for t_ in np.arange(0.4, Ls, 0.75):
                    side = 1 if int(t_ / 0.75) % 2 else -1
                    p = (ax_ + tx_ * t_ - ty_ * side * 0.18 + rng.normal(0, 0.12), ay_ + ty_ * t_ + tx_ * side * 0.18 + rng.normal(0, 0.12))
                    if on_floor(p, 0.2):
                        mark("footprint", p, 0.16, 0.08, 0.015, math.degrees(math.atan2(ty_, tx_)), (0.80, 0.80, 0.80))
        # wind ripples on the open snow (long, thin, aligned with the prevailing wind)
        x0, x1 = min(q[0] for q in floor), max(q[0] for q in floor)
        y0, y1 = min(q[1] for q in floor), max(q[1] for q in floor)
        for _ in range(900):
            p = (rng.uniform(x0, x1), rng.uniform(y0, y1))
            if not on_floor(p, 1.5) or G.point_in_poly(p, mere):
                continue
            if counts.get("ripple", 0) >= 120:
                break
            mark("ripple", p, rng.uniform(1.2, 2.8), 0.1, 0.03, 28.0 + rng.normal(0, 6), (0.95, 0.95, 0.94))
        # cracks in the mere ice
        for _ in range(400):
            p = (rng.uniform(x0, x1), rng.uniform(y0, y1))
            if counts.get("crack", 0) >= 45:
                break
            if G.point_in_poly(p, mere) and on_floor(p, 1.0):
                mark("crack", p, rng.uniform(1.0, 3.2), 0.04, 0.012, float(rng.uniform(0, 180)), (0.62, 0.72, 0.82))
        # sparse tufts: <= FLAT_MAX tall, under the density cap, never in a lane or on the ice
        cap = int(TUFT_CAP_PER_M2 * G.area(floor))
        tries = 0
        while counts.get("tuft", 0) < cap and tries < 5000:
            tries += 1
            p = (rng.uniform(x0, x1), rng.uniform(y0, y1))
            if not on_floor(p, 0.4) or G.point_in_poly(p, mere) or math.hypot(*p) < 3.0:
                continue
            if any(G.point_in_poly(p, q) or G.dist_to_boundary(p, q) < 0.6 for q in lanes):
                continue
            r_ = rng.uniform(0.15, 0.3)
            mark("tuft", p, r_, r_ * 0.8, rng.uniform(0.08, FLAT_MAX), float(rng.uniform(0, 180)),
                 tuple(np.clip(np.array((0.55, 0.47, 0.36)) + rng.normal(0, 0.04), 0, 1)), "crown")
        counts["_tuft_cap"] = cap
        return counts


def write_heightfield(H, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    H.astype("<f4").tofile(path)
