#!/usr/bin/env python3
"""C-9 R-C9-40: measure the holes the rig's own motion opens, and map them back into
the plate that has to cover them.

WHY.  Three rounds of reasoning about where a 2D cutout leg ought to come apart -- a
disc here, a measured overlap there -- each closed some of the gap and left the
enclosed-hole measure stuck around 12-28 rig px.  Every one of those fills was built
from a model of the seam (two masks, rotated against each other) rather than from the
drawing itself, and the model kept missing: a gap that is OPEN in a two-plate test is
CLOSED, and therefore a hole, once the other leg, the tabard and the far side are in
the picture.  The test kept passing and the knight kept coming apart.

So this measures the thing itself.  It rasterises the shipped scene frame by frame,
finds the background that is enclosed by figure -- which is what "the leg has detached"
means in pixels -- and transforms each such pixel back through the bone it belongs to,
into the SEED coordinates the plates are cut from.  The union over every frame of every
clip is exactly the region that plate must own, and nothing more.  build_knight_rig_E.py
reads it back and paints it with the still's own pixels at those coordinates, so at the
painted pose the fill lies on what it covers and is invisible.

Which plate grows, per joint (armour overlaps one way: cuisse over poleyn over greave
over sabaton, so the upper plate is the one in front and the one that should hide a
seam):
    hip    -> the THIGH.  The parts in front of it are cloth; a steel fill in the
              tabard would be a lie the moment the hem swung.
    knee   -> the THIGH (the poleyn is in front of the greave).
    ankle  -> the SHIN (the greave is in front of the sabaton).  Filling the sabaton
              instead would change its sole, which is the curve the heel-toe roll is
              solved against -- the fill would move the ground.

Run:  build -> harvest -> build -> harvest ... until it reports 0 new px.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_rig_E import Rig, hole_mask, joint_frames, joint_gap, PROJ   # noqa: E402

OUT = PROJ / "frames" / "knight_rig_gapfill.npz"

# joint -> (bone path, the sprite/plate that grows, the bone whose frame it grows in)
ROUTE = {
    # THE HIP IS NOT A PLATE PROBLEM.  Harvesting it into the thigh asked the thigh to
    # carry 150 seed px of material ABOVE its own pivot -- which would swing out from
    # under the tabard as a steel slab, and which in the still is blue cloth anyway.
    # What actually opens there is the SLOT: the tabard is two hanging flaps with the
    # body showing between them, the torso plate stops 22 px below the hip, and below
    # that the slot is covered by nothing but the legs.  Part the legs and you see
    # through the man.  So the hip's holes go to a BACKDROP -- one rigid piece on the
    # hip bone, drawn behind everything, which is what is inside the tabard.
    "hip_near":   ("Skel/hip/leg_n_th", "body_backdrop", "Skel/hip"),
    "hip_far":    ("Skel/hip/leg_f_th", "body_backdrop", "Skel/hip"),
    "knee_near":  ("Skel/hip/leg_n_th/leg_n_sh", "leg_near_thigh", "Skel/hip/leg_n_th"),
    "knee_far":   ("Skel/hip/leg_f_th/leg_f_sh", "leg_far_thigh", "Skel/hip/leg_f_th"),
    "ankle_near": ("Skel/hip/leg_n_th/leg_n_sh/leg_n_ft", "leg_near_shin",
                   "Skel/hip/leg_n_th/leg_n_sh"),
    "ankle_far":  ("Skel/hip/leg_f_th/leg_f_sh/leg_f_ft", "leg_far_shin",
                   "Skel/hip/leg_f_th/leg_f_sh"),
}
BPOS = {"Skel/hip": ("hip", False),
        "Skel/hip/leg_n_th": ("hip", False), "Skel/hip/leg_f_th": ("hip", True),
        "Skel/hip/leg_n_th/leg_n_sh": ("knee", False),
        "Skel/hip/leg_f_th/leg_f_sh": ("knee", True)}
JOINT_R = 26.0       # rig px; a hole further than this from every joint is not a joint


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zoom", type=float, default=4.0)
    ap.add_argument("--n", type=int, default=64)
    ap.add_argument("--grow", type=int, default=5, help="seed px of dilation")
    a = ap.parse_args()

    rep = json.loads((PROJ / "frames" / "knight_rig_E.json").read_text())
    tr = rep["transform"]
    s, sole = tr["seed_to_cell"], rep["seed"]["sole"]
    x_off = tr["ref_foot_cx_cell"] - tr["pivot_cell"][0]
    seed_cx = tr["seed_foot_cx"]
    Jr = rep["joints_rig"]
    far = rep["far_side"]["offset_rig_px"]

    def bpos(name):
        j, isfar = BPOS[name]
        p = Jr[j]
        return (p[0] + far[0], p[1] + far[1]) if isfar else (p[0], p[1])

    def to_seed(q):
        return ((q[0] - x_off) / s + seed_cx, q[1] / s + sole)

    rig = Rig()
    H, W = 1536, 1024                             # seed canvas (seed_E.png)
    acc = {k: np.zeros((H, W), bool) for k in
           ("body_backdrop", "leg_near_thigh", "leg_far_thigh",
            "leg_near_shin", "leg_far_shin")}
    origin = (200, 560)
    total_hole_px = 0
    worst = {}
    for clip in ("walk", "run", "idle"):
        L = rig.anims[clip]["length"]
        N = a.n if clip != "idle" else 16
        for i in range(N):
            t = L * i / N
            canvas, mk = rig.render(clip, t, zoom=a.zoom, origin=origin, size=(460, 700))
            alpha = np.zeros(canvas.shape[:2], bool)
            for k, v in mk.items():
                if k != "hand_pollaxe":
                    alpha |= v
            poses = rig.pose(clip, t)
            # HARVEST WHAT THE PROBE MEASURES.  Earlier this collected enclosed holes,
            # which is not the same set as "transparent where the limb's own axis runs"
            # and is not monotone -- filling it opened new holes and the loop oscillated.
            # These are exactly the pixels the axis measure counts, so filling them can
            # only lower that measure, and the loop terminates.
            pts = []
            for tag in ("n", "f"):
                for _seg, jp, u, r in joint_frames(poses, tag):
                    _g, p2 = joint_gap(alpha, jp, u, a.zoom, origin, R=r, want_pts=True)
                    pts.extend(p2)
            if not pts:
                continue
            pts = np.asarray(pts)
            rx, ry = pts[:, 0], pts[:, 1]
            # nearest joint
            best_d = np.full(rx.shape, 1e9)
            best_k = np.full(rx.shape, -1, np.int32)
            keys = list(ROUTE)
            for ki, k in enumerate(keys):
                M = poses[ROUTE[k][0]]
                d = np.hypot(rx - M[0, 2], ry - M[1, 2])
                m = d < best_d
                best_d[m], best_k[m] = d[m], ki
            take = (best_d <= JOINT_R) & (best_k >= 0)
            total_hole_px += int(take.sum())
            for ki, k in enumerate(keys):
                sel = take & (best_k == ki)
                if not sel.any():
                    continue
                plate, frame = ROUTE[k][1], ROUTE[k][2]
                Minv = np.linalg.inv(poses[frame])
                bp = bpos(frame)
                v = Minv @ np.stack([rx[sel], ry[sel], np.ones(sel.sum())])
                sx, sy = to_seed((v[0] + bp[0], v[1] + bp[1]))
                ix = np.clip(np.round(sx).astype(np.int32), 0, W - 1)
                iy = np.clip(np.round(sy).astype(np.int32), 0, H - 1)
                acc[plate][iy, ix] = True
                worst[k] = max(worst.get(k, 0), int(sel.sum()))

    # ACCUMULATE.  Each pass measures the gaps of the build in front of it, so writing
    # the harvest fresh each time removes last pass's fill at the same moment it adds
    # this pass's -- and the loop oscillates between two states instead of converging
    # (it did: hip 1.0 -> 2.7 -> 1.0 over three passes, each one "an improvement").
    # Unioned, the fill only grows and the measure only falls, so the loop terminates.
    prev = dict(np.load(OUT)) if OUT.exists() else {}
    for k in acc:
        if k in prev:
            acc[k] = acc[k] | prev[k].astype(bool)
    out = {}
    for k, m in acc.items():
        if m.any():
            m = ndimage.binary_dilation(m, np.ones((a.grow, a.grow), bool))
            m = ndimage.binary_closing(m, np.ones((9, 9), bool))
        out[k] = m
        ys, xs = np.nonzero(m)
        print("  %-16s %6d seed px%s" % (k, m.sum(),
              "  rows %d..%d cols %d..%d" % (ys.min(), ys.max(), xs.min(), xs.max())
              if m.any() else ""))
    print("  holes attributed to a joint, summed over frames: %d canvas px" % total_hole_px)
    print("  worst single frame per joint:", {k: v for k, v in sorted(worst.items())})
    np.savez_compressed(OUT, **{k: v for k, v in out.items()})
    print("wrote", OUT)


if __name__ == "__main__":
    main()
