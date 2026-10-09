#!/usr/bin/env python3
"""BV2F LV (conductor R-C9-226 item 1; Matt R-C9-212/214): the SEA-CAVE SECTION, carved -- subtractive only -- from the cliff
as a VERTICAL ERODED ROCK-COLUMN mass, like the kit cliff east of it.

Signed-distance field over a box in the route frame (t along the straight face, s seaward, z up), negative inside rock:
  * the BODY: the clifftop (the level's terrain, its headland over the cave) standing on a 2D plan whose edge follows
    COLUMN CELLS (a jittered Voronoi tiling, ~1.7 m columns): every face is vertical, polygonal, split by sharp vertical
    cracks between the columns; columns near an edge stand at their own heights (snow-capped ledges, a stepped knoll over
    the cave); a wave-cut notch at the high-water line. The plan = the land minus a SHALLOW COVE the sea cut into the face
    (rounded back corners; its walls the same columns);
  * the LANDING: a small flat tide-iced ledge just above the water at the cave mouth (ragged seaward edge); the rest of the
    cove floor is the sea, reaching into the mouth's west side;
  * minus the CAVE: a wave-worn arch in the cove's back wall, narrowing as it recedes (axis angled inland-west, away from
    the stone ring), flat ice floor;
  * minus the STAIR CLEFT cut from the cove's back-right corner straight INLAND (up-screen at the play camera, its risers
    facing the camera, as sketch A draws it), between walls of the same columns; its floor a smooth bed under the tread
    BLOCKS (built by the caller as separate stones), a flat pad at the top flush with the clifftop. (The cove's E part is
    deeper -- the stair's foot alcove -- so monsters 5 m wide pass from the mouth to the foot on a small ledge.)
Outside a mask round these features the field IS the terrain (the caller draws the terrain there; the two overlap in a
band and agree). Meshed by marching tetrahedra (numpy only) and classed per triangle."""
import math

import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree

from bv2pp_carve import march, orient


def sdf2(mask, st):
    """signed distance (m) of a 2D boolean region: negative inside"""
    din = ndimage.distance_transform_edt(mask) * st
    dout = ndimage.distance_transform_edt(~mask) * st
    return np.where(mask, -din + 0.5 * st, dout - 0.5 * st)


def build(P):
    rng = np.random.default_rng(226)
    st = P["step"]
    ts = np.arange(P["t0"], P["t1"] + 1e-6, st)
    ss = np.arange(P["s0"], P["s1"] + 1e-6, st)
    zs = np.arange(P["z0"], P["z1"] + 1e-6, st)
    nt, ns, nz = len(ts), len(ss), len(zs)
    T2, S2 = np.meshgrid(ts, ss, indexing="ij")
    cv, cove, ld, sp = P["cave"], P["cove"], P["landing"], P["stair"]
    LZ = P["landing_z"]
    # ---------------- the MASK: the features (+ margin) are the core; 2 m of blend round it ----------------
    core = np.zeros(T2.shape, bool)
    for (a0, a1, b0, b1) in P["core_rects"]:
        core |= (T2 >= a0) & (T2 <= a1) & (S2 >= b0) & (S2 <= b1)
    if "core_fn" in P:
        core |= P["core_fn"](T2, S2)
    d_core = ndimage.distance_transform_edt(~core) * st
    mask = np.clip(1.0 - d_core / 2.0, 0.0, 1.0)
    wmod = np.clip((mask - 0.6) / 0.3, 0.0, 1.0)              # the column modulation: full in the core, none by 1.2 m outside
    # ---------------- the clifftop and the nominal plan ----------------
    Htop = P["H"](T2, S2)
    land = Htop > P["land_thr"]
    # the cove (the sea's cut): rounded back corners, open to the sea
    # the cove: a union of rounded rectangles open to the sea (the back wall can step: deeper where the stair's foot is)
    r = cove["round_r"]
    in_cove = np.zeros(T2.shape, bool)
    for (ta_, tb_, sb_) in cove["parts"]:
        qt = np.clip(T2, ta_ + r, tb_ - r)
        qs = np.maximum(S2, sb_ + r)
        in_cove |= (np.hypot(T2 - qt, S2 - qs) < r) & (T2 >= ta_) & (T2 <= tb_)
    rock_nom = land & ~in_cove
    # the clifftop height carried out to the very edge (the face's own top, not the heightfield's drop)
    inner = sdf2(land, st) < -1.4
    _, (ii, jj) = ndimage.distance_transform_edt(~inner, return_indices=True)
    Hext = np.where(inner, Htop, Htop[ii, jj])
    # ---------------- the COLUMNS ----------------
    sd = []
    sp_c = P["col_spacing"]
    for a in np.arange(P["t0"], P["t1"] + sp_c, sp_c):
        for b in np.arange(P["s0"], P["s1"] + sp_c, sp_c):
            sd.append((a + rng.uniform(-0.42, 0.42) * sp_c, b + rng.uniform(-0.42, 0.42) * sp_c))
    sd = np.array(sd)
    tree = cKDTree(sd)
    dd, kk = tree.query(np.c_[T2.ravel(), S2.ravel()], k=2)
    F1, F2 = dd[:, 0].reshape(T2.shape), dd[:, 1].reshape(T2.shape)
    near = kk[:, 0].reshape(T2.shape)
    half = (F2 - F1) / 2.0                                     # ~ distance to the crack between two columns
    it_ = np.clip(((sd[:, 0] - P["t0"]) / st).round().astype(int), 0, nt - 1)
    is_ = np.clip(((sd[:, 1] - P["s0"]) / st).round().astype(int), 0, ns - 1)
    sd_nom = sdf2(rock_nom, st)
    seed_sd = sd_nom[it_, is_]
    rock_seed = seed_sd < 0.0
    # the stair's lip band stays rock (the low uncut lip on the groove's sea side; a few columns still break it)
    rock_vor = rock_seed[near] & (sd_nom < 1.4)               # never more than 1.4 m proud of the nominal face
    rock_vor &= ~(in_cove & (sd_nom > 0.1))                  # the cove floor stays clear: its columns only ever recess the walls
    sdv = sdf2(rock_vor, st)
    sd_2 = wmod * sdv + (1.0 - wmod) * sd_nom
    # sharp vertical CRACKS between the columns, ~0.9 m into the face, only where a face is
    crack = np.minimum(0.12 - half, 0.9 + sd_2)
    sd_2 = np.where((wmod > 0.5) & (sd_2 > -1.2), np.maximum(sd_2, crack), sd_2)
    # every column near an edge stands at its own height: snow-capped ledges stepping down to the face; over the headland the
    # columns step with the knoll (each one flat-topped)
    seed_top = Hext[it_, is_]
    near_edge = sdv[it_, is_] > -2.6
    drop = np.where(near_edge, rng.uniform(0.0, 1.35, len(sd)), 0.0)
    if "erode_ok" in P:
        # R-C9-294: the erosion only where its pixels may change (outside the pilot, or inside the declared rects): a 0..1
        # weight per grid cell from the caller, judged at the cell's OLD top (a lowered top only moves down on screen)
        E = P["erode_ok"](T2, S2, Hext)
    else:
        E = np.ones(T2.shape)
    E_seed = E[it_, is_]
    drop = drop * (1.0 - (1.0 - P.get("drop_scale", 1.0)) * E_seed)     # R-C9-290: lower steps between the columns (same draws)
    drop = np.where(rng.random(len(sd)) < 0.3, drop * 0.25, drop)
    in_head = P["head_mask"](sd[:, 0], sd[:, 1])
    # over the knoll a column is never lower than the ground it stands for (the arch's roof is measured off it): its top is the
    # highest clifftop in its cell, and it does not drop
    cell_max = np.asarray(ndimage.maximum(Hext, labels=near, index=np.arange(len(sd))))
    drop = np.where(in_head, 0.0, drop)
    top_col = np.where(in_head, cell_max, seed_top - drop)
    stepped = near_edge | in_head
    top_c = np.where(stepped[near], top_col[near], Hext)
    if P.get("head_smooth"):
        # R-C9-325 (1): over the knoll the rock is ONE rounded mass (no flat-topped column blocks standing over the arch): the
        # clifftop's local maximum (1 m) softened (0.7 m) -- never below the ground it stands for, so the roof still measures off it
        hm = P["head_mask"](T2, S2)
        hsm = ndimage.gaussian_filter(ndimage.maximum_filter(Hext, size=int(round(1.0 / st)) | 1), 0.7 / st)
        hw_ = ndimage.gaussian_filter(hm.astype(float), 0.6 / st)
        top_c = top_c + hw_ * (np.maximum(hsm, Hext) - top_c)
    wz = P["walk_zone"]
    in_walk = (T2 >= wz[0]) & (T2 <= wz[1]) & (S2 >= wz[2]) & (S2 <= wz[3])
    if P.get("top_blur_m", 0.0) > 0:
        # R-C9-290: the column tops ERODED -- the stepped per-column tops softened (no squared steps), each top domed a little
        # toward its crack; never above the stepped top (the arch's roof is measured off it)
        top_s = ndimage.gaussian_filter(top_c, P["top_blur_m"] / st)
        dome = 0.18 * np.clip(1.0 - half / 0.6, 0.0, 1.0) ** 1.5
        top_c = top_c + E * (np.minimum(top_c, top_s) - dome * wmod - top_c)
    top2 = np.where(in_walk, Hext, wmod * top_c + (1.0 - wmod) * Hext)
    # ---------------- the 3D field ----------------
    out = {}
    f = np.empty((nt, ns, nz), np.float32)
    hw = P["high_water"]
    face_band = (wmod > 0.0) & (sd_2 > -1.6)
    land2 = P["landing_fn"](T2, S2)                           # R-C9-228: the small iced ledge (gully floor + the cave mouth's floor)
    sd_land = sdf2(land2, st)
    for k, z in enumerate(zs):
        notch = 0.45 * math.exp(-((z - hw) / 0.5) ** 2)
        fa_ = z - top2
        fb_ = sd_2 + np.where(face_band, notch * wmod, 0.0)
        rr_ = P.get("round_r", 0.0) * wmod * E
        if P.get("round_r", 0.0) > 0:
            # R-C9-290: the column tops' edges ROUNDED (a round intersection of the top and the face, radius round_r): eroded
            # shoulders, so the snow (classed by slope) ends in a soft curve, never a step or a vertical snow face
            ua_ = np.maximum(fa_ + rr_, 0.0)
            ub_ = np.maximum(fb_ + rr_, 0.0)
            body = np.where(rr_ > 1e-3, np.minimum(-rr_, np.maximum(fa_, fb_)) + np.hypot(ua_, ub_), np.maximum(fa_, fb_))
        else:
            body = np.maximum(fa_, fb_)
        lnd = np.maximum(z - LZ, sd_land)
        f[:, :, k] = np.minimum(np.minimum(body, lnd), z - P["z_floor"])
    T3, S3, Z3 = np.meshgrid(ts, ss, zs, indexing="ij")
    # ---------------- the CAVE (minus): an arch along an axis angled inland-west ----------------
    ax = np.array(cv["axis"], float)
    ax /= np.linalg.norm(ax)
    a_ = (T3 - cv["t"]) * ax[0] + (S3 - cv["s_mouth"]) * ax[1]          # along the axis (inland positive)
    c_ = (T3 - cv["t"]) * -ax[1] + (S3 - cv["s_mouth"]) * ax[0]          # across
    dep = np.clip(a_, 0, None)
    kk3 = 1.0 - 0.5 * np.clip(dep / cv["depth"], 0, 1)
    hw3 = cv["w"] / 2 * kk3
    hh3 = cv["h"] * kk3
    zz = np.clip(Z3 - LZ, 0, None)
    ell = (c_ / hw3) ** 2 + (zz / hh3) ** 2 - 1.0
    d_cave = np.maximum(np.maximum(ell * hw3 * 0.5, LZ - Z3), np.maximum(-a_ - cv.get("front", 1.2), a_ - cv["depth"]))
    d_cave = np.maximum(d_cave, Z3 - (top2[:, :, None] - 1.3))           # never through the roof: 1.3 m of rock over it
    wobble = ndimage.gaussian_filter(rng.standard_normal((nt, ns, nz)), 0.6 / st)
    wobble /= wobble.std() + 1e-9
    d_cave = d_cave + 0.12 * wobble * np.clip((Z3 - LZ - 0.5) / 0.5, 0, 1)
    # the sea reaches into the mouth's west side: a water channel below the landing's level, west of the landing's edge
    chan = np.full(d_cave.shape, 9.0)                          # R-C9-228: no cut channel -- the sea meets the mouth at the face
    if cv.get("brow"):
        # R-C9-325 (1) (Matt): NO SLABS CANTILEVERED OVER THE MOUTH. In front of the arch's roof line the rock above the roof
        # level is cut back along a face that LEANS INLAND with height (a brow): nothing stands proud over the void. In plan the
        # cut is a parabola (deepest on the axis, meeting the cave's front limit at +-hw_b), so it blends into the face with no
        # notch; below the roof level the arch (d_cave) is unchanged, so the mouth, the landing and the exit route stay as built
        bw = cv["brow"]
        hwb = cv["w"] / 2 + bw.get("w_pad", 0.5)
        # its floor is the ARCH's own curve (0.3 m under the ellipse's crown line, never under the roof level or 0.3 m over the
        # landing) -- so no thin sheet survives between the arch's crown and the roof level in front of the lip
        z_sp3 = top2[:, :, None] - 1.3
        z_arch = LZ + hh3 * np.sqrt(np.clip(1.0 - (c_ / hw3) ** 2, 0.0, 1.0)) - 0.3
        z_lo = np.maximum(np.minimum(z_sp3 - 0.2, z_arch), LZ + 0.3)
        a_lim = bw["a_face"] + bw["lean"] * np.clip(Z3 - z_sp3, 0, None) - (bw["a_face"] + cv.get("front", 1.2)) * (c_ / hwb) ** 2
        d_brow = np.maximum.reduce([a_ - a_lim, np.abs(c_) - hwb, z_lo - Z3, -a_ - cv.get("front", 1.2)])
        chan = np.minimum(chan, d_brow)
        if __import__("os").environ.get("LV_DBG"):
            print("[dbg] brow cut cells", int((d_brow < 0).sum()), "a_lim@c0", float(np.median(a_lim[np.abs(c_) < 0.3])), "zsp med", float(np.median(z_sp3)))
        del a_lim, d_brow, z_sp3, z_arch, z_lo
    # ---------------- the STAIR CLEFT (minus): cut from the cove's back-right corner straight INLAND (up-screen, its risers facing
    # the camera, as sketch A draws it) between rock columns; a bed under the tread blocks (built by the caller), a flat pad at
    # the top flush with the clifftop ----------------
    s_f, s_t, s_l = sp["s_foot"], sp["s_top"], sp["s_land"]
    plane = LZ + ((s_f + sp["tread"]) - S3) * sp["rise"] / sp["tread"]
    bed = np.where(S3 < s_t, sp["top_z"], np.maximum(LZ, plane - sp["bed_below"]))
    def wall_wob(t_edge):
        ie = int(round((t_edge - P["t0"]) / st))
        hc = half[ie, :][None, :, None] if 0 <= ie < nt else 0.5
        return 0.35 * np.clip(1.0 - hc / 0.25, 0, 1) + 0.12 * np.sin(Z3 * 1.3 + S3 * 0.7)
    t_wl = sp["t0"] - wall_wob(sp["t0"])
    t_wr = sp["t1"] + wall_wob(sp["t1"])
    d_groove = np.maximum.reduce([bed - Z3, t_wl - T3, T3 - t_wr, s_l - S3, S3 - sp.get("s_open", s_f + 0.6)])
    d_lip = np.full(d_groove.shape, 9.0)
    cut = np.minimum.reduce([d_cave, chan, d_groove, d_lip])
    f = np.maximum(f, -cut).astype(np.float64)
    del wobble, a_, c_, ell, chan, d_groove, d_lip, plane, bed
    f[:, :, 0] = np.minimum(f[:, :, 0], -0.1)
    origin = np.array([ts[0], ss[0], zs[0]])
    solid = f < 0
    first_air = np.argmax(~solid[:, :, 1:] & solid[:, :, :-1], axis=2)
    fa0 = np.take_along_axis(f, first_air[..., None], 2)[..., 0]
    fa1 = np.take_along_axis(f, (first_air + 1)[..., None], 2)[..., 0]
    walk_h = zs[0] + (first_air + fa0 / (fa0 - fa1 + 1e-9)) * st
    g = np.stack(np.gradient(f), axis=0)

    def grad_fn(p):
        q = (p - origin) / st
        return np.stack([ndimage.map_coordinates(g[a], q.T, order=1, mode="nearest") for a in range(3)], axis=1)
    T = march(f, origin, st)
    T, Nn = orient(T, grad_fn)
    cen = T.mean(1)
    # keep only the triangles inside the mask (outside it the terrain is drawn; they agree in the blend band)
    mi = np.clip(((cen[:, 0] - P["t0"]) / st).round().astype(int), 0, nt - 1)
    mj = np.clip(((cen[:, 1] - P["s0"]) / st).round().astype(int), 0, ns - 1)
    keep = (mask[mi, mj] > 0.3) & (cen[:, 2] > P["z_floor"] + 0.05)
    T, Nn, cen = T[keep], Nn[keep], cen[keep]
    tt, sv, zv = cen[:, 0], cen[:, 1], cen[:, 2]
    up = Nn[:, 2]
    names = ["rock", "wet_rock", "rime", "tide_ice", "snow", "passage_dark"]
    cls = np.zeros(len(T), np.int8)
    a_t = (tt - cv["t"]) * ax[0] + (sv - cv["s_mouth"]) * ax[1]
    c_t = (tt - cv["t"]) * -ax[1] + (sv - cv["s_mouth"]) * ax[0]
    k_t = 1.0 - 0.5 * np.clip(a_t / cv["depth"], 0, 1)
    in_cave_deep = (a_t > 0.9) & (a_t < cv["depth"] + 0.6) & (np.abs(c_t) < cv["w"] / 2 * k_t + 0.4) & (zv < LZ + cv["h"] * k_t + 0.3)
    cls[(zv < hw - 0.06) & (up < 0.75)] = 1
    cls[(np.abs(zv - hw) <= 0.09) & (up < 0.75)] = 2
    landing = (np.abs(zv - LZ) < 0.08) & (up > 0.8)
    if P.get("ledge_rock"):
        # R-C9-315/319 W2: the exit ledge reads as a ROCK ledge (not a pale-blue tide-ice field that paints as shallow water):
        # its top is wet rock, with a thin RIME edge (0.35 m, pale ice tint) along its rim; the geometry and the walk are unchanged
        sdl = ndimage.map_coordinates(sd_land, [(tt - P["t0"]) / st, (sv - P["s0"]) / st], order=1, mode="nearest")
        cls[landing] = 1
        cls[landing & (sdl > -0.35)] = 3       # the thin rime edge in the pale tide-ice tint (keeps the carved_tide_ice id: the pins' id order)
    else:
        cls[landing] = 3
    in_groove = (tt >= sp["t0"] - 0.5) & (tt <= sp["t1"] + 0.5) & (sv >= s_t - 0.05) & (sv <= s_f + 0.6)
    if "erode_ok" in P:
        Et = ndimage.map_coordinates(E, [(tt - P["t0"]) / st, (sv - P["s0"]) / st], order=1, mode="nearest")
        snow_up_t = np.where(Et > 0.01, P.get("snow_up", 0.55), 0.55)
    else:
        snow_up_t = P.get("snow_up", 0.55)
    topsnow = (up > snow_up_t) & (zv > LZ + 0.5) & ~in_groove     # R-C9-290: thin conformal caps on the gentle tops only
    cls[topsnow] = 4
    pad = (up > 0.8) & (sv < s_t) & (sv >= s_l - 0.3) & (tt >= sp["t0"] - 0.5) & (tt <= sp["t1"] + 0.5)
    cls[pad] = 4
    if cv.get("dark_east_wall") is False:
        # R-C9-325 (2) (Matt, "the black rectangle right of the sea cave"): the cave's EAST side wall (c > 0, seen face-on through
        # the gap right of the arch) was classed passage_dark over its full height -- a tall black slot. Only the cave's depth
        # (its back, under the roof) stays dark; that wall reads as rock (in the arch's shadow)
        in_cave_deep &= ~(c_t > cv["w"] / 2 * k_t - 0.9)
    cls[in_cave_deep & ~landing] = 5
    out.update({"tris_ts": T, "normals_ts": Nn, "cls": cls, "classes": names, "walk_h": walk_h, "grid_ts": (ts, ss), "mask": mask, "wmod": wmod,
                "top2": top2, "sd_plan": sd_2})
    return out
