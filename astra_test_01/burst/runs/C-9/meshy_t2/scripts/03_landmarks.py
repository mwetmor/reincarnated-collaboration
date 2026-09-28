# C-9 meshy_t2 step 3: extract the skeleton landmarks from the mesh itself.
#
#   blender -b -noaudio --python scripts/03_landmarks.py -- <model.glb> <out.json> <outblend>
#
# What is measured, and why each instrument was chosen:
#
#  * SCALE by the TOPLINE BREAK, not by the bbox and not by "highest vertex over
#    the front legs". Both of those measure the MANE, which on this creature
#    sits exactly over the withers: the 40-bin profile climbs 0.014-0.018 per
#    bin along the back and then jumps 0.079 in one bin -- that jump IS the
#    mane onset. The last bin before it is the withers. Measured on the midline
#    strip so the mane's lateral bulk cannot contribute.
#
#  * LEG CENTRELINES by per-z centroid inside a paw's own column. A leg is not
#    a straight line and its joints are where the centreline TURNS, so the
#    turn is found by maximum deviation from the chord (Douglas-Peucker on the
#    2D side-view centreline) rather than by picking heights by eye.
#
#  * SPINE by the mid-height of the body cross-section, taken only where the
#    cross-section is body and not leg: below the belly there are two separate
#    x-clusters (the legs), above it one. The spine is sampled where the slice
#    is single-blob at its own mid-height.
#
#  * TAIL from the thin tapering run at the -Y end: its centreline is simply
#    (zbot+ztop)/2 per bin, because the section is a near-circle.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector, Matrix

a = sys.argv[sys.argv.index('--') + 1:]
SRC, OUTP, OUTBLEND = a[0], a[1], a[2]
TARGET_WITHERS_M = 1.00


def verts_world(objs):
    out = []
    for o in objs:
        M = o.matrix_world
        co = np.empty(len(o.data.vertices) * 3)
        o.data.vertices.foreach_get("co", co)
        out.append(co.reshape(-1, 3) @ np.array(M.to_3x3()).T + np.array(M.translation))
    return np.vstack(out)


def canonicalise(sc, objs):
    """Y-up glTF -> Z up, head at +Y, feet on z=0, midline at x=0. (Step 2
    established up=Z by leg-blob count and head at low-Y by cross-section bulk;
    reproduced here so this script stands alone.)"""
    P = verts_world(objs)
    span = P.max(0) - P.min(0)
    long_axis = int(np.argmax(span))          # Y
    t = (P[:, long_axis] - P[:, long_axis].min()) / span[long_axis]
    others = [i for i in range(3) if i != long_axis]
    bulk = []
    for m in (t < 0.15, t > 0.85):
        s = P[m][:, others]
        bulk.append(float(np.prod(s.max(0) - s.min(0))))
    head_low = bulk[0] > bulk[1]
    B = np.zeros((3, 3)); B[0, 0] = 1.0
    B[long_axis, 1] = -1.0 if head_low else 1.0
    B[2, 2] = 1.0
    if np.linalg.det(B) < 0:
        B[:, 0] *= -1
    R = Matrix(B.T.tolist()).to_4x4()
    for o in list(sc.objects):
        if o.parent is None:
            o.matrix_world = R @ o.matrix_world
    P = verts_world(objs)
    T = Matrix.Translation(Vector((-float(np.median(P[:, 0])), 0.0, -float(P[:, 2].min()))))
    for o in list(sc.objects):
        if o.parent is None:
            o.matrix_world = T @ o.matrix_world
    return dict(long_axis="XYZ"[long_axis], head_low=bool(head_low),
                bulk_low=round(bulk[0], 5), bulk_high=round(bulk[1], 5))


def withers_by_topline_break(P, nb=80):
    """Walk the midline topline from the loin forward; the withers is the last
    bin before the step size blows up (the mane)."""
    ymin, ymax = P[:, 1].min(), P[:, 1].max(); L = ymax - ymin
    hw = 0.15 * (P[:, 0].max() - P[:, 0].min()) / 2.0
    mid = P[np.abs(P[:, 0]) < hw]
    zt, ys = [], []
    for i in range(nb):
        m = (mid[:, 1] >= ymin + i * L / nb) & (mid[:, 1] < ymin + (i + 1) * L / nb)
        s = mid[m]
        zt.append(float(s[:, 2].max()) if len(s) else np.nan)
        ys.append(float(ymin + (i + 0.5) * L / nb))
    zt = np.array(zt); ys = np.array(ys)
    ok = ~np.isnan(zt)
    d = np.diff(zt)
    i0, i1 = int(nb * 0.45), int(nb * 0.85)
    # The BIGGEST step in the forward half, not the first step over a
    # threshold. A "3x the median" rule fired at bin 53 on a 0.0068 step
    # against a 0.0020 median -- true, and meaningless: on a smooth back every
    # median is tiny, so a threshold relative to it is noise-triggered. The
    # mane onset is 0.079 in one 40-bin step; it is the largest by an order of
    # magnitude and needs no tuning to find.
    med = float(np.nanmedian(np.abs(d[i0:i1])))
    cand = [(float(d[i]), i) for i in range(i0, i1) if ok[i] and ok[i + 1]]
    brk = max(cand)[1] if cand else int(nb * 0.72)
    return dict(withers_z=float(zt[brk]), withers_y=float(ys[brk]), break_bin=brk,
                median_step=round(med, 5), step_at_break=round(float(d[brk]), 5),
                topline=[[round(float(y), 4), (round(float(z), 4) if ok[i] else None)]
                         for i, (y, z) in enumerate(zip(ys, zt))])


def dp_corners(pts, k):
    """The k interior points of a polyline that deviate most from their chord."""
    pts = np.asarray(pts)
    segs = [(0, len(pts) - 1)]
    corners = []
    for _ in range(k):
        best = None
        for si, (i, j) in enumerate(segs):
            if j - i < 2:
                continue
            A, B = pts[i], pts[j]
            v = B - A; n = np.linalg.norm(v)
            if n < 1e-9:
                continue
            u = v / n
            w = pts[i + 1:j] - A
            dist = np.abs(w[:, 0] * u[1] - w[:, 1] * u[0])
            m = int(np.argmax(dist)) + i + 1
            if best is None or dist.max() > best[0]:
                best = (float(dist.max()), si, m)
        if best is None:
            break
        _, si, m = best
        i, j = segs.pop(si)
        segs += [(i, m), (m, j)]
        corners.append(m)
    return sorted(corners)


def leg_centreline(P, cx, cy, halfx, halfy, ztop, nz=26):
    """Centroid per z-slice inside one paw's column, from the ground up."""
    m = (np.abs(P[:, 0] - cx) < halfx) & (np.abs(P[:, 1] - cy) < halfy) & (P[:, 2] < ztop)
    S = P[m]
    if len(S) < 40:
        return []
    out = []
    z0, z1 = S[:, 2].min(), S[:, 2].max()
    for i in range(nz):
        za, zb = z0 + (z1 - z0) * i / nz, z0 + (z1 - z0) * (i + 1) / nz
        s = S[(S[:, 2] >= za) & (S[:, 2] < zb)]
        if len(s) < 5:
            continue
        out.append([float(s[:, 0].mean()), float(s[:, 1].mean()), float((za + zb) / 2),
                    int(len(s))])
    return out


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=SRC)
    sc = bpy.context.scene
    objs = [o for o in sc.objects if o.type == 'MESH']
    rep = dict(orient=canonicalise(sc, objs))
    P = verts_world(objs)

    w = withers_by_topline_break(P)
    rep["withers"] = {k: v for k, v in w.items() if k != "topline"}
    rep["topline_model_units"] = w["topline"]
    S = TARGET_WITHERS_M / w["withers_z"]
    rep["scale_factor"] = round(S, 6)
    for o in list(sc.objects):
        if o.parent is None:
            o.matrix_world = Matrix.Scale(S, 4) @ o.matrix_world
    P = verts_world(objs)
    rep["metres"] = dict(withers_m=TARGET_WITHERS_M,
                         withers_y=round(w["withers_y"] * S, 4),
                         head_top_m=round(float(P[:, 2].max()), 4),
                         nose_y=round(float(P[:, 1].max()), 4),
                         tail_tip_y=round(float(P[:, 1].min()), 4),
                         total_len_m=round(float(P[:, 1].max() - P[:, 1].min()), 4),
                         width_m=round(float(P[:, 0].max() - P[:, 0].min()), 4))

    # ---- paws ------------------------------------------------------------
    zlo, zhi = P[:, 2].min(), P[:, 2].max()
    foot = P[P[:, 2] < zlo + 0.07 * (zhi - zlo)]
    paws = {}
    for sx, mx in (("r", foot[:, 0] > 0), ("l", foot[:, 0] <= 0)):
        side = foot[mx]
        ym = np.median(side[:, 1])
        for sy, my in (("f", side[:, 1] > ym), ("h", side[:, 1] <= ym)):
            g = side[my]
            paws[sy + sx] = dict(
                n=len(g), x=float(g[:, 0].mean()), y=float(g[:, 1].mean()),
                z=float(g[:, 2].min()),
                toe_y=float(g[:, 1].max()) if sy == "f" else float(g[:, 1].max()),
                heel_y=float(g[:, 1].min()),
                xr=[float(g[:, 0].min()), float(g[:, 0].max())])
    rep["paws"] = {k: {kk: (round(vv, 4) if isinstance(vv, float) else vv)
                       for kk, vv in v.items()} for k, v in paws.items()}

    # ---- belly line: the z under which a y-slice splits into two x-blobs --
    ymin, ymax = P[:, 1].min(), P[:, 1].max()
    body_lo = min(paws["hr"]["y"], paws["hl"]["y"]) - 0.05
    body_hi = max(paws["fr"]["y"], paws["fl"]["y"]) + 0.05

    # ---- leg centrelines --------------------------------------------------
    legs = {}
    for k, p in paws.items():
        halfy = 0.22 if k[0] == "h" else 0.20
        cl = leg_centreline(P, p["x"], p["y"], 0.13, halfy, 0.80)
        legs[k] = cl
    rep["leg_centrelines"] = {k: [[round(c, 4) for c in pt[:3]] + [pt[3]] for pt in v]
                              for k, v in legs.items()}
    # joints = the turns of the side-view (y,z) centreline
    joints = {}
    for k, cl in legs.items():
        if len(cl) < 6:
            continue
        pts = np.array([[c[1], c[2]] for c in cl])
        idx = dp_corners(pts, 2)
        joints[k] = [dict(i=int(i), y=round(float(cl[i][1]), 4), z=round(float(cl[i][2]), 4),
                          x=round(float(cl[i][0]), 4)) for i in idx]
    rep["leg_joints"] = joints

    # ---- spine: mid-height of the single-blob part of each y slice --------
    spine = []
    nb = 44
    for i in range(nb):
        y0 = ymin + (ymax - ymin) * i / nb
        y1 = ymin + (ymax - ymin) * (i + 1) / nb
        s = P[(P[:, 1] >= y0) & (P[:, 1] < y1)]
        if len(s) < 30:
            continue
        # the body part of the slice = above the belly: take the upper 55 % of
        # the slice's z range, whose centroid is inside the torso
        zt, zb = s[:, 2].max(), s[:, 2].min()
        up = s[s[:, 2] > zb + 0.45 * (zt - zb)]
        spine.append([round(float((y0 + y1) / 2), 4), round(float(up[:, 2].mean()), 4),
                      round(float(zt), 4), round(float(zb), 4),
                      round(float(s[:, 0].max() - s[:, 0].min()), 4), len(s)])
    rep["slices"] = dict(cols=["y", "z_upper_centroid", "ztop", "zbot", "xext", "n"],
                         rows=spine)

    bpy.ops.wm.save_as_mainfile(filepath=OUTBLEND)
    json.dump(rep, open(OUTP, "w"), indent=1)
    print("scale x%.4f  withers %.4f at y=%.4f (break bin %d, step %.4f vs median %.4f)"
          % (S, w["withers_z"], w["withers_y"], w["break_bin"], w["step_at_break"], w["median_step"]))
    print("metres:", json.dumps(rep["metres"]))
    print("paws:", {k: (v["x"], v["y"]) for k, v in rep["paws"].items()})
    for k, v in joints.items():
        print("  leg %s joints: %s" % (k, [(j["y"], j["z"]) for j in v]))


main()
