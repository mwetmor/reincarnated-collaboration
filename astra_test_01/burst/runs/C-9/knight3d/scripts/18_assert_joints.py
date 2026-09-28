#!/usr/bin/env python3
"""C-9 knight3d: ASSERT the joints hold, on RENDERS, every frame (R-C9-58).

Matt: "the bones/frame isn't rigged well around the legs and the feet look
chopped up." Geometry that overlaps in the parameters can still open on screen
once a bend puts one piece behind another, so the test is run where the defect
was seen: on the rendered frame.

Per joint, per frame, per gait:
  PARTED   are the joint's pieces still ONE connected region on screen? If
           they overlap or touch, yes; if a bend has opened them, the union
           splits in two and `separation_px` measures how far.
  HOLE     a CREVICE PUNCTURE: background enclosed by the silhouette, lying
           wholly inside the joint's disc, touching this joint's own pieces,
           and small. The size bound is not cosmetic -- in a profile view the
           void BETWEEN the two legs is enclosed by the body above and the
           feet below, so a plain enclosed-background count calls the gap
           between a man's legs a defect, and did (882 px on walk frame 3).

  (First written as "background inside the CONVEX HULL of the two pieces",
  which fires on every bent joint by construction: the hull of a bend spans
  its concave side, and that side is legitimately background. It reported
  39 479 gap pixels on a walk whose joints had not parted at all. The hull was
  the wrong region; connectivity is the question.)
  PLUG     pixels inside the hull whose luma is far below the median luma of
           the two pieces -- the ink pass filling a crevice black, which reads
           as a chopped-up joint even when no pixel is missing.

Both are counted at the SUPERSAMPLED resolution the frames are rendered at,
because a one-pixel gap at 512 is four at 2048 and it is the 2048 that says
whether the pieces actually touch.
"""
import json, math, os, sys
import numpy as np
from scipy import ndimage as ndi
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import knight_proxy as kp
import pose as PS
from raster import raster

K3 = os.path.dirname(HERE); OUT = os.path.join(K3, "out"); WORK = os.path.join(K3, "work")
FRAME, SS = 512, 4
PX_PER_M = 198.33333333333334 / 1.80

JOINTS = [("knee_L", ["cuisse_L", "poleyn_L", "greave_L"], "LeftLeg", 1.9),
          ("knee_R", ["cuisse_R", "poleyn_R", "greave_R"], "RightLeg", 1.9),
          ("ankle_L", ["greave_L", "sabaton_L"], "LeftFoot", 1.7),
          ("ankle_R", ["greave_R", "sabaton_R"], "RightFoot", 1.7),
          ("toe_L", ["sabaton_L", "sabaton_toe_L"], "LeftToeBase", 1.5),
          ("toe_R", ["sabaton_R", "sabaton_toe_R"], "RightToeBase", 1.5),
          ("hip_L", ["fauld", "cuisse_L"], "LeftUpLeg", 1.7),
          ("hip_R", ["fauld", "cuisse_R"], "RightUpLeg", 1.7)]


def hull_fill(mask):
    if mask.sum() < 3:
        return mask
    return ndi.binary_fill_holes(ndi.binary_closing(mask, np.ones((3, 3))))


def convex_fill(pts, shape):
    from scipy.spatial import ConvexHull
    from PIL import Image as I, ImageDraw
    if len(pts) < 3:
        return np.zeros(shape, bool)
    try:
        h = ConvexHull(pts)
    except Exception:
        return np.zeros(shape, bool)
    im = I.new("1", (shape[1], shape[0]), 0)
    ImageDraw.Draw(im).polygon([tuple(pts[v][::-1]) for v in h.vertices], fill=1)
    return np.asarray(im, bool)


def main():
    fit = json.load(open(os.path.join(WORK, "fit_result.json")))
    theta = fit["theta_elevation_deg"]
    p = dict(kp.DEFAULTS); p.update(fit["params"])
    pl = kp.layered(p)
    idx = json.load(open(os.path.join(OUT, "parts_index.json")))
    A = np.load(os.path.join(OUT, "mesh_atlas.npz"), allow_pickle=True)
    tri_v0 = A["tri_v"].astype(np.float64); tri_id = A["tri_id"]
    names = [str(n) for n in A["names"]]
    pb = {n: idx["parts"][n]["bone"] for n in names}
    pk = {n: idx["parts"][n]["kind"] for n in names}
    Jr = kp.joints(pl)
    W = H = FRAME * SS
    scale = PX_PER_M * SS
    tx = FRAME / 2 * SS

    rep = {"note": __doc__.strip().splitlines()[0], "gaits": {}}
    worst = 0
    for gait in ("walk", "run"):
        pre = os.environ.get("K3D_ANIM", "anim")
        spr = os.environ.get("K3D_SPRITEDIR", "sprites")
        rsuf = "_fit" if pre != "anim" else ""
        f = os.path.join(OUT, "%s_%s.npz" % (pre, gait))
        if not os.path.exists(f):
            continue
        z = np.load(f, allow_pickle=True)
        nm = [str(x) for x in z["names"]]; rn = [str(x) for x in z["rot_names"]]
        rj = json.load(open(os.path.join(OUT, "render_%s%s.json" % (gait, rsuf))))
        ty = (rj["sole_y"] + rj["ground_calibration_px"]) * SS
        per = []
        for i in range(len(z["joints"])):
            Jp = {k: z["joints"][i][j] for j, k in enumerate(nm)}
            ov = {k: z["rots"][i][j].astype(np.float64) for j, k in enumerate(rn)}
            T = PS.bone_transforms(Jr, Jp, ov)
            V = PS.pose_tris(tri_v0, tri_id, names, pb, pk, T, pl)
            r_, u_ = kp.basis(90.0, theta); c_ = kp.cam_dir(90.0, theta)
            flat = V.reshape(-1, 3)
            xy = np.stack([flat @ r_ * scale + tx, -(flat @ u_) * scale + ty], -1)
            xy = xy.reshape(len(V), 3, 2); zz = (-(flat @ c_)).reshape(len(V), 3)
            at = np.zeros((len(V), 3, 1)); at[:, :, 0] = tri_id[:, None]
            zb, ib, ab, _ = raster(xy, zz, at, W, H)
            solid = ib >= 0
            pid = np.where(solid, tri_id[np.clip(ib, 0, len(V) - 1)], -1)
            frame = {}
            for jname, pieces, bone, rad in JOINTS:
                ids = [names.index(x) for x in pieces if x in names]
                jp = Jp.get(bone)
                if jp is None:
                    continue
                jx = float(jp @ r_) * scale + tx
                jy = -float(jp @ u_) * scale + ty
                rr = rad * p["poleyn_r"] * scale
                Y, X = np.ogrid[:H, :W]
                disc = ((X - jx) ** 2 + (Y - jy) ** 2) <= rr * rr
                mine = np.isin(pid, ids) & disc
                if mine.sum() < 20:
                    frame[jname] = dict(parted=False, sep_px=0, hole=0,
                                        plug=0, region=0, skipped=True)
                    continue
                # Connectivity is tested through the WHOLE silhouette, not
                # through the two pieces alone: at the hip the tabard covers
                # the join, so fauld-plus-cuisse pixels are two blobs on screen
                # while the figure has no break at all. Tested the narrow way
                # first, it called every hip "parted" with a 70 px separation
                # that was simply the tabard lying across it.
                lab, ncomp = ndi.label(solid & disc, structure=np.ones((3, 3)))
                ids_here = set(np.unique(lab[mine])) - {0}
                parted = len(ids_here) > 1
                sep = 0.0
                if parted:
                    two = sorted(ids_here,
                                 key=lambda c: -int(((lab == c) & mine).sum()))[:2]
                    a = np.argwhere((lab == two[0]) & mine)
                    b = np.argwhere((lab == two[1]) & mine)
                    step = max(1, len(a) // 400), max(1, len(b) // 400)
                    d = np.sqrt(((a[::step[0], None, :] - b[None, ::step[1], :]) ** 2).sum(-1))
                    sep = float(d.min())
                region = mine
                encl = ndi.binary_fill_holes(solid) & ~solid
                hl, hn = ndi.label(encl, structure=np.ones((3, 3)))
                hole = 0
                near = ndi.binary_dilation(mine, np.ones((5, 5)))
                for hcomp in range(1, hn + 1):
                    m_ = hl == hcomp
                    a_ = int(m_.sum())
                    if a_ < 4 or a_ > 600:
                        continue
                    if not (m_ & disc).any() or (m_ & ~disc).any():
                        continue
                    if (m_ & near).any():
                        hole += a_
                lum = np.zeros((H, W))
                # luma is taken from the rendered frame's own pixels
                img = np.asarray(Image.open(os.path.join(
                    OUT, spr, gait, "E", "%s_E_%02d.png" % (gait, i))).convert("RGBA"))
                big = np.kron(img[..., :3], np.ones((SS, SS, 1), np.uint8))[:H, :W]
                lum = big @ np.array([0.299, 0.587, 0.114])
                med = float(np.median(lum[mine])) if mine.any() else 0.0
                plug = int((ndi.binary_dilation(mine, np.ones((5, 5))) & solid
                            & (lum < med - 78)).sum())
                frame[jname] = dict(parted=bool(parted), sep_px=round(sep, 1),
                                    hole=hole, plug=plug, region=int(mine.sum()))
                worst = max(worst, sep if parted else 0.0)
            per.append(frame)
        rep["gaits"][gait] = per
        npart = sum(1 for fr in per for v in fr.values() if v.get("parted"))
        tot_h = sum(v["hole"] for fr in per for v in fr.values())
        tot_p = sum(v["plug"] for fr in per for v in fr.values())
        print("  %-4s %2d frames   parted joints %d   holes %d px   dark-plug %d px"
              % (gait, len(per), npart, tot_h, tot_p))
        bad = [(i, k, v) for i, fr in enumerate(per) for k, v in fr.items()
               if v.get("parted") or v["hole"] > 0 or v["plug"] > 120]
        for i, k, v in bad[:12]:
            print("      frame %02d  %-8s parted=%s sep %5.1f  hole %4d  plug %4d"
                  % (i, k, v.get("parted"), v.get("sep_px", 0), v["hole"], v["plug"]))
    rep["worst_separation_px_at_%dx" % SS] = worst
    with open(os.path.join(OUT, "joint_assert%s.json"
                           % ("_fit" if os.environ.get("K3D_ANIM", "anim") != "anim"
                              else "")), "w") as f:
        json.dump(rep, f, indent=1)
    print("worst joint separation %.1f px at %dx supersample (=%.2f px at 512)"
          % (worst, SS, worst / SS))
    print("wrote", os.path.join(OUT, "joint_assert.json"))


main()
