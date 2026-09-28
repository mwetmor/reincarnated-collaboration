# C-9 meshy_t2 step 4a: the numbers the skeleton is built from.
#
#   blender -b -noaudio --python scripts/04_measure_rig.py -- <model.glb> <out.json>
#
# Every landmark below is MEASURED. Where anatomy supplies a proportion the
# mesh cannot show (the shoulder joint and the hip are buried inside solid
# muscle, so no surface centroid finds them), the proportion is applied to
# MEASURED endpoints and the choice is recorded in the output as `from`:
# "measured" or "anatomical".
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("04_measure_rig.py")][0])))
import t2lib as T

a = sys.argv[sys.argv.index('--') + 1:]
SRC, OUTP = a[0], a[1]


def largest_gap_split(vals):
    s = np.sort(vals)
    if len(s) < 4:
        return float(np.median(s))
    g = np.diff(s)
    i = int(np.argmax(g))
    return float((s[i] + s[i + 1]) / 2)


def main():
    sc, objs, info = T.load_canonical(bpy, SRC)
    obj = objs[0]
    P = T.verts_world(objs)
    rep = dict(canonical=info)

    # ---- paws, split on the LARGEST Y GAP, not the median ------------------
    # A median split forces the two groups to equal size, so it cut through the
    # front paw and handed 'fr' vertices at y = -0.24 (heel_y came back as a
    # hind-paw value). The paws are separated by ~0.9 m of empty air; the
    # largest gap finds that and cannot cut a paw in half.
    zlo, zhi = P[:, 2].min(), P[:, 2].max()
    foot = P[P[:, 2] < zlo + 0.07 * (zhi - zlo)]
    ysplit = largest_gap_split(foot[:, 1])
    paws = {}
    for sy, my in (("f", foot[:, 1] > ysplit), ("h", foot[:, 1] <= ysplit)):
        band = foot[my]
        xsplit = largest_gap_split(band[:, 0])
        for sx, mx in (("r", band[:, 0] > xsplit), ("l", band[:, 0] <= xsplit)):
            g = band[mx]
            paws[sy + sx] = dict(n=int(len(g)),
                                 x=float(g[:, 0].mean()), y=float(g[:, 1].mean()),
                                 z=float(g[:, 2].min()),
                                 toe_y=float(g[:, 1].max()), heel_y=float(g[:, 1].min()),
                                 x_lo=float(g[:, 0].min()), x_hi=float(g[:, 0].max()))
    rep["paw_split"] = dict(y=round(ysplit, 4))
    rep["paws"] = {k: {kk: round(vv, 4) if isinstance(vv, float) else vv
                       for kk, vv in v.items()} for k, v in paws.items()}

    # ---- leg columns: the per-z centroid, all the way into the body --------
    cols = {}
    for k, p in paws.items():
        m = (np.abs(P[:, 0] - p["x"]) < 0.10) & (np.abs(P[:, 1] - p["y"]) < 0.26)
        S = P[m]
        rows = []
        for i in range(34):
            za, zb = i * 0.90 / 34, (i + 1) * 0.90 / 34
            s = S[(S[:, 2] >= za) & (S[:, 2] < zb)]
            if len(s) < 6:
                continue
            rows.append([round(float((za + zb) / 2), 4), round(float(s[:, 0].mean()), 4),
                         round(float(s[:, 1].mean()), 4),
                         round(float(s[:, 1].max() - s[:, 1].min()), 4), int(len(s))])
        cols[k] = rows
    rep["leg_columns"] = dict(cols=["z", "x", "y", "y_extent", "n"], data=cols)

    # ---- the man's head, by TEXTURE WARMTH --------------------------------
    C = T.vertex_colours_from_texture(obj)
    rep["texture_sampled"] = C is not None
    warm_idx = None
    if C is not None:
        warm = (C[:, 0] - C[:, 2]) > 0.09
        # keep only the largest connected component of the warm set, so stray
        # warm texels on the body (the pale belly, the claws) do not count
        me = obj.data
        ne = len(me.edges)
        ev = np.empty(ne * 2, dtype=np.int32)
        me.edges.foreach_get("vertices", ev)
        ev = ev.reshape(-1, 2)
        keep = warm[ev[:, 0]] & warm[ev[:, 1]]
        adj = {}
        for u, v in ev[keep]:
            adj.setdefault(int(u), []).append(int(v))
            adj.setdefault(int(v), []).append(int(u))
        seen = set(); best = []
        for v0 in list(adj.keys()):
            if v0 in seen:
                continue
            st = [v0]; seen.add(v0); comp = []
            while st:
                x = st.pop(); comp.append(x)
                for y in adj[x]:
                    if y not in seen:
                        seen.add(y); st.append(y)
            if len(comp) > len(best):
                best = comp
        warm_idx = np.array(sorted(best), dtype=np.int64)
        H = P[warm_idx]
        rep["head_island"] = dict(
            n_warm=int(warm.sum()), n_component=int(len(warm_idx)),
            bbox_lo=[round(float(v), 4) for v in H.min(0)],
            bbox_hi=[round(float(v), 4) for v in H.max(0)],
            centroid=[round(float(v), 4) for v in H.mean(0)])
        # the FLESH sub-island (the face proper): redder still, and it is the
        # part that must not squash
        flesh = (C[:, 0] - C[:, 2]) > 0.22
        fi = np.where(flesh)[0]
        if len(fi):
            F = P[fi]
            rep["face_flesh"] = dict(n=int(len(fi)),
                                     bbox_lo=[round(float(v), 4) for v in F.min(0)],
                                     bbox_hi=[round(float(v), 4) for v in F.max(0)],
                                     centroid=[round(float(v), 4) for v in F.mean(0)])
        # is there a JAW to rig? A jaw needs a mouth OPENING or at least a
        # crease; look for a dark band across the face at mouth height.
        if len(fi):
            F = P[fi]
            lum = C[fi].mean(1)
            zr = F[:, 2].max() - F[:, 2].min()
            bands = []
            for i in range(10):
                m = (F[:, 2] >= F[:, 2].min() + i * zr / 10) & \
                    (F[:, 2] < F[:, 2].min() + (i + 1) * zr / 10)
                if m.sum() > 5:
                    bands.append([i, round(float(lum[m].mean()), 4), int(m.sum())])
            rep["face_luminance_bands"] = bands
        np.save(os.path.join(os.path.dirname(OUTP), "head_island.npy"), warm_idx)

    # ---- belly line, where no leg is in the way ---------------------------
    ymin, ymax = P[:, 1].min(), P[:, 1].max()
    belly = []
    for i in range(44):
        y0 = ymin + (ymax - ymin) * i / 44; y1 = ymin + (ymax - ymin) * (i + 1) / 44
        s = P[(P[:, 1] >= y0) & (P[:, 1] < y1)]
        if len(s) < 20:
            continue
        mid = s[np.abs(s[:, 0]) < 0.05]
        if len(mid) < 5:
            continue
        belly.append([round(float((y0 + y1) / 2), 4), round(float(mid[:, 2].min()), 4),
                      round(float(mid[:, 2].max()), 4), int(len(mid))])
    rep["midline_profile"] = dict(cols=["y", "zbot", "ztop", "n"], data=belly)

    # ---- the tail, as a centreline ---------------------------------------
    tail_start = min(paws["hr"]["heel_y"], paws["hl"]["heel_y"]) - 0.02
    tl = []
    for i in range(24):
        y0 = ymin + (tail_start - ymin) * i / 24; y1 = ymin + (tail_start - ymin) * (i + 1) / 24
        s = P[(P[:, 1] >= y0) & (P[:, 1] < y1)]
        if len(s) < 5:
            continue
        r = float(max(s[:, 0].max() - s[:, 0].min(), s[:, 2].max() - s[:, 2].min()) / 2)
        tl.append([round(float((y0 + y1) / 2), 4), round(float(s[:, 0].mean()), 4),
                   round(float(s[:, 2].mean()), 4), round(r, 4), int(len(s))])
    rep["tail_centreline"] = dict(cols=["y", "x", "z", "radius", "n"], data=tl,
                                  scan_to_y=round(tail_start, 4))

    json.dump(rep, open(OUTP, "w"), indent=1)
    print("scale x%.4f  withers y=%.3f" % (info["scale_factor"], info["withers_y_m"]))
    print("paws:", {k: (round(v["x"], 3), round(v["y"], 3), round(v["toe_y"], 3)) for k, v in rep["paws"].items()})
    if "head_island" in rep:
        print("head island: %d verts  bbox %s..%s" % (rep["head_island"]["n_component"],
              rep["head_island"]["bbox_lo"], rep["head_island"]["bbox_hi"]))
    if "face_flesh" in rep:
        print("face flesh : %d verts  bbox %s..%s" % (rep["face_flesh"]["n"],
              rep["face_flesh"]["bbox_lo"], rep["face_flesh"]["bbox_hi"]))
    for k in ("fr", "fl", "hr", "hl"):
        print("leg", k, [(r[0], r[2]) for r in cols[k][::4]])


main()
