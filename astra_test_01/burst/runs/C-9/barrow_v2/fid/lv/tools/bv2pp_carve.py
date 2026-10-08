#!/usr/bin/env python3
"""BV2F LV (Matt R-C9-212/214, conductor R-C9-213): the SEA-CAVE SECTION as ONE eroded rock mass, CARVED -- subtractive only.

The rock is a signed-distance field over a box in the route frame (t along the straight face, s seaward, z up), negative
inside rock:
  * the BODY: the level's own terrain (clifftop, headland, the cliff face to the sea floor), its faces eroded by noise in s
    that varies along t and slowly in z -- columns, buttresses and recesses, sharp vertical cracks, snow ledges (setbacks
    every ~1.6 m of height);
  * minus the COVE the sea cut into the cliff (rounded west end, its back wall worn; its floor the LANDING above the water,
    the sea in its mouth);
  * minus the CAVE worn into the cove's back wall (a rounded arch narrowing as it recedes; flat ice-lined floor);
  * minus the STAIR, a groove cut into the cove's right-hand (east) wall along the face: stepped treads, the inland wall
    the cliff's own rock, a LOW BROKEN UNCUT LIP (knee-high) left standing on the sea side.
Meshed by marching tetrahedra (numpy, no extra libraries) and classed per triangle: rock, wet_rock (below the high-water
line), rime (the line itself), tide_ice (the landing + cave floor), snow (tread tops, ledges and the clifftop),
passage_dark (deep inside the cave)."""
import math

import numpy as np
from scipy import ndimage

# the 6 tetrahedra of a cube (corners: 0 (0,0,0) 1 (1,0,0) 2 (1,1,0) 3 (0,1,0) 4 (0,0,1) 5 (1,0,1) 6 (1,1,1) 7 (0,1,1))
CORNERS = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]])
TETS = [(0, 5, 1, 6), (0, 1, 2, 6), (0, 2, 3, 6), (0, 3, 7, 6), (0, 7, 4, 6), (0, 4, 5, 6)]


def smooth_noise(shape, scale_vox, rng, sigma_axes=None):
    a = rng.standard_normal(shape)
    sig = sigma_axes if sigma_axes is not None else [scale_vox] * len(shape)
    a = ndimage.gaussian_filter(a, sig, mode="wrap")
    return a / (a.std() + 1e-9)


def march(f, origin, step):
    """marching tetrahedra on f (negative inside); returns triangles (M, 3, 3) in world units, each wound so its normal points
    OUT of the solid (toward +f)"""
    nx, ny, nz = f.shape
    fc = np.stack([f[c[0]:nx - 1 + c[0], c[1]:ny - 1 + c[1], c[2]:nz - 1 + c[2]] for c in CORNERS], axis=-1)
    act = np.nonzero((fc.min(-1) < 0) & (fc.max(-1) >= 0))
    base = np.stack(act, axis=-1).astype(np.float64)
    vals = fc[act]                                            # (K, 8)
    tris = []
    for tet in TETS:
        tv = vals[:, tet]                                     # (K, 4)
        tp = base[:, None, :] + CORNERS[list(tet)][None, :, :]   # (K, 4, 3)
        inside = tv < 0
        cnt = inside.sum(1)

        def edge(i, j, sel):
            a, b = tv[sel, i], tv[sel, j]
            w = (a / (a - b))[:, None]
            return tp[sel, i] + (tp[sel, j] - tp[sel, i]) * w
        for k_in in (1, 3):
            sel = np.nonzero(cnt == k_in)[0]
            if not len(sel):
                continue
            ins = inside[sel] if k_in == 1 else ~inside[sel]
            lone = np.argmax(ins, axis=1)
            others = np.array([[j for j in range(4) if j != l] for l in range(4)])[lone]
            p = [None, None, None]
            for q in range(3):
                a_i = lone
                b_i = others[:, q]
                av = tv[sel, a_i]
                bv = tv[sel, b_i]
                w = (av / (av - bv))[:, None]
                pa = tp[sel, a_i]
                pb = tp[sel, b_i]
                p[q] = pa + (pb - pa) * w
            tris.append(np.stack(p, axis=1))
        sel = np.nonzero(cnt == 2)[0]
        if len(sel):
            ins = inside[sel]
            order = np.argsort(~ins, axis=1, kind="stable")       # the two inside first
            i0, i1, o0, o1 = order[:, 0], order[:, 1], order[:, 2], order[:, 3]

            def e(a_i, b_i):
                av = tv[sel, a_i]
                bv = tv[sel, b_i]
                w = (av / (av - bv))[:, None]
                return tp[sel, a_i] + (tp[sel, b_i] - tp[sel, a_i]) * w
            p00, p01, p11, p10 = e(i0, o0), e(i0, o1), e(i1, o1), e(i1, o0)
            tris.append(np.stack([p00, p01, p11], axis=1))
            tris.append(np.stack([p00, p11, p10], axis=1))
    T = np.concatenate(tris) * step + origin
    return T


def orient(T, grad_fn):
    n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
    g = grad_fn(T.mean(1))
    flip = (n * g).sum(1) < 0
    T[flip] = T[flip][:, [0, 2, 1]]
    n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
    ln = np.linalg.norm(n, axis=1)
    keep = ln > 1e-9
    return T[keep], n[keep] / ln[keep, None]


def build(P):
    """P: dict -- frame (o, d), box t0 t1 s0 s1 z0 z1, step, H(t, s) sampler (vectorized), the cove / cave / stair spec.
    Returns {"tris": (M,3,3) in (u, v, z), "normals", "cls": per-tri class index, "classes": [...], "treads": [...],
    "footprint": function (u, v) -> bool}"""
    rng = np.random.default_rng(212)
    st = P["step"]
    ts = np.arange(P["t0"], P["t1"] + 1e-6, st)
    ss = np.arange(P["s0"], P["s1"] + 1e-6, st)
    zs = np.arange(P["z0"], P["z1"] + 1e-6, st)
    nt, ns, nz = len(ts), len(ss), len(zs)
    T3, S3, Z3 = np.meshgrid(ts, ss, zs, indexing="ij")
    # --- the eroded BODY: the terrain sampled at an s shifted by face noise (columns / cracks / setbacks) ---
    fade = np.clip(np.minimum(T3 - P["t0"], P["t1"] - T3) / 3.0, 0, 1) * np.clip((S3 - P["s0"]) / 3.0, 0, 1)
    col = smooth_noise((nt, 1, max(2, nz // 6)), 1.0, rng, [3.0 / st * 0.2, 0.0, 1.0])
    col = ndimage.zoom(col, (1, 1, nz / col.shape[2]), order=1)[:, :, :nz]
    crack = smooth_noise((nt,), 1.0, rng, [0.25 / st])
    crack = np.clip(np.abs(crack) - 1.6, 0, None)[:, None, None] * 2.2      # rare sharp vertical cracks
    ledge = 0.3 * np.floor((Z3 - P["z0"]) / 1.6 + 0.3 * np.sin(T3 * 0.9))                 # setbacks: snow ledges every ~1.6 m of height
    ds = (0.55 * col + 0.22 * np.sin(T3 * 2.1 + 0.4) + crack + ledge) * fade
    Hs = P["H"](T3, S3 + ds)                                  # the terrain at the shifted s
    f = Z3 - Hs                                                # < 0 inside rock
    # --- the COVE (minus) ---
    c = P["cove"]
    tb = np.clip((T3 - c["t_w"]) / c["round_w"], 0, 1)
    colz = ndimage.zoom(smooth_noise((nt, 1, max(2, nz // 5)), 1.0, rng, [2.0 / st * 0.2, 0.0, 1.0]), (1, 1, nz / max(2, nz // 5)), order=1)[:, :, :nz]
    s_back = c["s_back"] * np.sqrt(1 - (1 - tb) ** 2) - 0.35 * np.abs(colz)               # the back wall: columnar, worn
    in_cove = (T3 >= c["t_w"] - 0.01) & (T3 <= c["t_e"]) & (S3 > s_back)
    edge_s = c["s_edge"] + 0.45 * np.sin(T3 * 0.9 + 0.3) + 0.25 * np.sin(T3 * 2.3 + 1.1) + 0.12 * np.sin(T3 * 5.1)     # a ragged, wave-cut ledge edge
    floor = np.where(S3 < edge_s, P["landing_z"], P["z_floor"] - 1.0)
    # the walls undercut by the waves just above the water (a notch 0.6 m deep at the high-water line)
    notch = 0.6 * np.exp(-((Z3 - P["high_water"]) / 0.6) ** 2)
    t_w_n = c["t_w"] + 0.4 * np.sin(S3 * 1.3 + 0.5) + 0.2 * np.sin(Z3 * 0.9)
    d_cove = np.maximum(np.maximum(s_back - notch - S3, floor - Z3), np.maximum(t_w_n - T3 - notch, T3 - c["t_e"]))
    # --- the CAVE (minus): a rounded arch receding from the back wall, narrowing, floor flat at the landing ---
    cv = P["cave"]
    depth = np.clip(cv["s_mouth"] - S3, 0, None)
    k = 1.0 - 0.5 * np.clip(depth / cv["depth"], 0, 1)
    hw = cv["w"] / 2 * k
    hh = cv["h"] * k
    zz = np.clip(Z3 - P["landing_z"], 0, None)
    ell = ((T3 - cv["t"]) / hw) ** 2 + (zz / hh) ** 2 - 1.0
    d_cave = np.maximum(np.maximum(ell * hw * 0.5, P["landing_z"] - Z3), np.maximum(S3 - (cv["s_mouth"] + 1.0), (cv["s_mouth"] - cv["depth"]) - S3))
    d_cave = np.maximum(d_cave, Z3 - (Hs - 1.3))              # never through the roof: 1.3 m of rock stays over the tunnel
    d_cave = d_cave + 0.12 * smooth_noise((nt, ns, nz), 1.0, rng, [0.6 / st] * 3) * np.clip((Z3 - P["landing_z"] - 0.5) / 0.5, 0, 1)
    # --- the STAIR groove (minus), its uncut lip left on the sea side ---
    sp = P["stair"]
    # each tread's front edge wanders across the width (+-6 cm) and each riser row is broken by worn notches -- cut stone, not planks
    wob = -(0.05 + 0.03 * np.sin(S3 * 1.9 + 0.7) + 0.02 * np.sin(S3 * 4.7 + T3 * 0.9))      # fronts only ever set BACK (no nosing above the walk plane)
    tq = np.clip((T3 - sp["t_foot"] + wob) / sp["tread"], -1, sp["n_tr"])
    i_tr = np.floor(tq)
    tread_z = np.where(T3 < sp["t_foot"], P["landing_z"], np.where(T3 > sp["t_top"], sp["crest"], P["landing_z"] + (i_tr + 1) * sp["rise"]))
    on_fl = (T3 >= sp["t_foot"]) & (T3 <= sp["t_top"])
    tread_z = tread_z - on_fl * (0.02 * (np.abs(np.sin(S3 * 3.1 + i_tr * 1.7))) + 0.04 * (np.sin(S3 * 0.8 + i_tr * 2.3) > 0.7))   # worn dishes and chipped blocks
    s_in_w = sp["s_in"] - 0.4 * np.abs(colz)                   # the groove's inland wall: the cliff's own columns (only ever deeper)
    in_g = (S3 >= sp["s_in"]) & (S3 <= sp["s_lip"]) & (T3 >= sp["t_foot"] - 0.6) & (T3 <= sp["t_land"])
    d_groove = np.maximum.reduce([tread_z - Z3, s_in_w - S3, S3 - sp["s_lip"], (sp["t_foot"] - 0.6) - T3, T3 - sp["t_land"]])
    brk = (np.sin(T3 * 1.9 + 0.5) + 0.6 * np.sin(T3 * 4.3)) > 0.95                  # a few breaks in the lip
    lip_top = tread_z + np.where(brk, 0.05, sp["lip_h"] + 0.12 * np.sin(T3 * 3.7))
    d_lip = np.maximum.reduce([lip_top - Z3, sp["s_lip"] - S3, S3 - sp["s_face"], (sp["t_foot"] - 0.6) - T3, T3 - sp["t_land"]])
    cut = np.minimum.reduce([d_cove, d_cave, d_groove, d_lip])
    f = np.maximum(f, -cut)
    f[:, :, 0] = np.minimum(f[:, :, 0], -0.1)                  # closed underneath (below the sea floor)
    origin = np.array([ts[0], ss[0], zs[0]])
    # the WALK HEIGHT of every column: its lowest rock -> air transition (the cave's floor under its roof, the landing, the
    # treads, the clifftop) -- what the level's floor_y_at answers inside the carved footprint
    solid = f < 0
    first_air = np.argmax(~solid[:, :, 1:] & solid[:, :, :-1], axis=2)
    fa0 = np.take_along_axis(f, first_air[..., None], 2)[..., 0]
    fa1 = np.take_along_axis(f, (first_air + 1)[..., None], 2)[..., 0]
    walk_h = zs[0] + (first_air + fa0 / (fa0 - fa1 + 1e-9)) * st

    def grad_fn(p):
        q = (p - origin) / st
        g = np.stack(np.gradient(f), axis=0)
        return np.stack([ndimage.map_coordinates(g[a], q.T, order=1, mode="nearest") for a in range(3)], axis=1)
    T = march(f, origin, st)
    T, Nn = orient(T, grad_fn)
    # --- classes per triangle ---
    cen = T.mean(1)
    tt, sv, zv = cen[:, 0], cen[:, 1], cen[:, 2]
    up = Nn[:, 2]
    names = ["rock", "wet_rock", "rime", "tide_ice", "snow", "passage_dark"]
    cls = np.zeros(len(T), np.int8)
    in_cave_deep = (sv < cv["s_mouth"] - 0.9) & (np.abs(tt - cv["t"]) < cv["w"] / 2 + 0.6) & (zv < P["landing_z"] + cv["h"])
    cls[(zv < P["high_water"] - 0.06) & (up < 0.75)] = 1
    cls[(np.abs(zv - P["high_water"]) <= 0.08) & (up < 0.75)] = 2
    landing = (np.abs(zv - P["landing_z"]) < 0.08) & (up > 0.8)
    cls[landing] = 3
    treadtop = (up > 0.8) & (tt >= sp["t_foot"] - 0.05) & (tt <= sp["t_top"] + 0.05) & (sv >= sp["s_in"]) & (sv <= sp["s_lip"])
    cls[treadtop] = 4
    topsnow = (up > 0.55) & (zv > P["landing_z"] + 0.5) & ~treadtop
    cls[topsnow] = 4
    cls[in_cave_deep & ~landing] = 5
    # the tread outlines (for PT's snow layer): each tread's top as a polygon in the frame
    treads = []
    for i in range(sp["n_tr"]):
        ta, tb_ = sp["t_foot"] + i * sp["tread"], sp["t_foot"] + (i + 1) * sp["tread"]
        treads.append({"id": "tread_%02d" % i, "z_m": round(P["landing_z"] + (i + 1) * sp["rise"], 4),
                       "outline_ts": [[round(ta, 3), sp["s_in"]], [round(tb_, 3), sp["s_in"]], [round(tb_, 3), sp["s_lip"]], [round(ta, 3), sp["s_lip"]]]})
    return {"tris_ts": T, "normals_ts": Nn, "cls": cls, "classes": names, "treads": treads, "walk_h": walk_h, "grid_ts": (ts, ss)}
