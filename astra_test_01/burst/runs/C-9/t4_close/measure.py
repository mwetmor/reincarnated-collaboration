#!/usr/bin/env python3
"""C-9 T4 close-out: every number, for every route, in one pass.

    python3 measure.py            # writes drift.json
    python3 measure.py --routes kling,hydra

ROUTES.  Four candidates animated the SAME input (fal_t4/knight_E_ref_1024.png
driven by fal_t4/knight_carrywalk_E_drive.mp4), plus two rows that are not
candidates and are here to make the candidates readable:

  drive   the Meshy carry-walk render that drove them.  One unlit texture on
          one rigged mesh: its identity CANNOT drift, so whatever it scores is
          this instrument's FLOOR, exactly as the 512 px render's ~1.9 was the
          floor in T1/T2.  It is also the ground truth for the GAIT -- the
          cadence and the foot contact every route was asked to reproduce.
  astra   the knight's per-frame Astra paint (knight3d walk E, 12 frames).
          This is the row test 4 is compared against: it is the route Matt
          rejected, on this exact complaint -- "his helmet/head morph once each
          second whenever he turns his head".

MEASURED PER ROUTE
  1 helm drift        frame-to-frame, and every frame against the reference
                      still (identity drift), over the helm alone
  2 body drift        the same two, over the whole figure
  3 foot slide        horizontal excursion of a ground-contact point while it
                      is in contact, with the body's own translation removed
  4 cadence           strides per second, against the drive's
  5 pollaxe rigidity  haft length variation, straightness, angle steadiness
  6 loop seam         last frame against first, against the consecutive median
  7 cost and time     from the job files

The negative control is a SHUFFLED frame order, read on the frame-to-frame
numbers: consecutive frames being more alike than distant ones is drift with
temporal structure; the two collapsing together is a sequence with no temporal
structure to find -- which is what a floor looks like.
"""
import argparse
import json
import math
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import t4lib as L

R = L.RUNS
HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(R, "fal_t4", "knight_E_ref_1024.png")


def route_defs():
    def seq(d, pat, n, start=0):
        return [os.path.join(R, d, pat % i) for i in range(start, start + n)]
    return {
        "kling": dict(kind="green", fps=30.0, label="Kling v3 Pro (motion-control)",
                      frames=seq("fal_t4/kling_frames", "k_%04d.png", 150, 1)),
        "hydra": dict(kind="alpha", fps=64 / 2.9166666666666665,
                      label="Ludo transfer-motion, hydra",
                      frames=seq("ludo_t4/tm_hydra", "individual_frame_urls_%03d.webp", 64)),
        "forge": dict(kind="alpha", fps=42 / 2.9240274234693877,
                      label="Ludo transfer-motion, forge",
                      frames=seq("ludo_t4/tm_forge", "individual_frame_urls_%03d.webp", 42)),
        "anim": dict(kind="alpha", fps=36 / 2.875,
                     label="Ludo animate-sprite, text prompt 'walking'",
                     frames=seq("ludo_t4/anim_hydra", "individual_frame_urls_%03d.webp", 36)),
        "drive": dict(kind="alpha", fps=30.0, label="FLOOR: Meshy carry-walk render (the drive)",
                      frames=seq("fal_t4/drive", "d_%04d.png", 150)),
        # sprites_astra_a, not sprites_fit_astra_a: the paint AS DELIVERED, before
        # the fit resample. The resample smooths, and smoothing is the direction
        # that flatters a drift score -- the benchmark row should not be handed
        # that. Figure height 236 px against 212 px fitted.
        "render3d": dict(kind="alpha", fps=20.7,
                         label="FLOOR at the Astra row's resolution: the raw 3D render of "
                               "the same knight3d walk E cycle",
                         frames=seq("knight3d/out/sprites_fit/walk/E", "walk_E_%02d.png", 12)),
        "astra": dict(kind="alpha", fps=20.7, label="BENCHMARK: Astra per-frame paint (knight3d walk E)",
                      frames=seq("knight3d/out/sprites_astra_a/walk/E", "walk_E_%02d.png", 12)),
    }


# --------------------------------------------------------------------------
# per-frame extraction
# --------------------------------------------------------------------------
def haft_fit(g):
    """Length, angle and STRAIGHTNESS of the pollaxe haft.

    The weapon mask is haft + axe head, and the head holds more pixels than
    the haft does, so a PCA over the whole weapon fits the BLADE.  The haft is
    isolated first as the part of the weapon that the same disk opening which
    severed it from the body also erases: haft = weapon AND NOT opening(weapon).
    A line is then fitted by PCA and refitted once with pixels further than 4%
    of its length from it dropped, which sheds the spike and the butt cap.

    straightness_pct = RMS perpendicular distance / length, in percent.  A
    rigid pole is straight; a haft that bows or swims between frames is not.
    """
    w = g["weapon"]
    if w.sum() < 50:
        return None
    haft = w & ~ndi.binary_opening(w, L.disk(max(2, g["open_w"])))
    lab, n = ndi.label(haft)
    if n == 0:
        return None
    sz = ndi.sum(haft, lab, range(1, n + 1))
    haft = np.isin(lab, [i + 1 for i, s in enumerate(sz) if s >= 0.25 * sz.max()])
    ys, xs = np.nonzero(haft)
    if len(ys) < 50:
        return None
    pts = np.stack([xs, ys], 1).astype(float)
    for _ in range(2):
        c = pts.mean(0)
        u, s, vt = np.linalg.svd(pts - c, full_matrices=False)
        ax = vt[0]
        t = (pts - c) @ ax
        perp = (pts - c) @ vt[1]
        length = float(t.max() - t.min())
        keep = np.abs(perp) <= 0.04 * max(length, 1.0)
        if keep.sum() < 50:
            break
        pts = pts[keep]
    c = pts.mean(0)
    u, s, vt = np.linalg.svd(pts - c, full_matrices=False)
    ax = vt[0]
    t = (pts - c) @ ax
    perp = (pts - c) @ vt[1]
    length = float(t.max() - t.min())
    ang = math.degrees(math.atan2(abs(ax[0]), abs(ax[1])))   # 0 = vertical
    return dict(len_pct_H=100.0 * length / g["H"],
                angle_from_vertical_deg=ang,
                straightness_pct=100.0 * float(np.sqrt((perp ** 2).mean())) / max(length, 1.0),
                px=int(len(pts)))


def runs_of(cols, minw):
    """Contiguous runs of True, at least minw wide; returns their centres."""
    out, i, n = [], 0, len(cols)
    while i < n:
        if cols[i]:
            j = i
            while j + 1 < n and cols[j + 1]:
                j += 1
            if j - i + 1 >= minw:
                out.append(0.5 * (i + j))
            i = j + 1
        else:
            i += 1
    return out


BOTTOM_FRAC = 0.14        # of figure height, kept per frame for the foot pass


def extract(cfg):
    """ONE pass over a route's frames.  Nothing full-resolution is retained:
    what survives is a 96 px helm crop, a 256 px body crop, a 64 px pose thumb,
    the bottom BOTTOM_FRAC of the silhouette as a packed bool, and scalars.
    (Kling's frames are 1440 px and there are 150 of them; a second decode pass
    over those, only to find the feet, cost more than it was worth.)"""
    recs = []
    for i, p in enumerate(cfg["frames"]):
        g = L.frame_geometry(p, cfg["kind"])
        if g is None:
            continue
        hp, hm, _ = L.helm_patch(g)
        bp, bm, bbox = L.body_patch(g)
        xs = np.nonzero(g["body"].sum(0))[0]
        r = L.crop_pad(g["rgb"], *bbox)
        mm = L.crop_pad(g["body"].astype(np.uint8), *bbox).astype(bool)
        sr, sm = L.resample(r, mm, 64)
        nb = max(3, int(BOTTOM_FRAC * g["H"]))
        bot = g["body"][max(0, g["sole"] - nb + 1):g["sole"] + 1]
        recs.append(dict(i=i, helm=hp.astype(np.float32), helm_m=hm,
                         body=bp.astype(np.float32), body_m=bm,
                         small=(sr * sm[..., None]).astype(np.float32),
                         H=g["H"], crown=g["crown"], sole=g["sole"],
                         neck=g["neck"], cx=float(xs.mean()),
                         helm_h_native=g["neck"] - g["crown"],
                         haft=haft_fit(g),
                         bottom=np.packbits(bot, axis=-1), bot_w=bot.shape[1],
                         bot_top=g["sole"] - bot.shape[0] + 1))
        del g
    return recs


def contacts(recs, band_frac=0.045, min_run_frac=0.020):
    """Feet at the ground, from the bottom band of EACH FRAME's own silhouette.

    A single clip-wide ground line was tried first and does not survive contact
    with the data.  The drive's lowest row wanders over 20 px -- 3.6% of figure
    height -- because the render carries vertical root motion, so a band pinned
    to the clip's 95th-percentile sole was BELOW the figure for 25 of 70 frames
    and returned no contact at all for them.  The per-frame band returns one or
    two runs for every frame of every route, and the two-run frames are exactly
    the double-support ones: the reading is legible instead of sparse.

    What it costs: the band follows the figure's bob, so a foot is "in contact"
    when it is the LOWEST thing, not when it is at a fixed ground height.  In a
    walk those coincide except around toe-off, and the slip measure below is
    about the shape of the track rather than its absolute height."""
    H = float(np.median([r["H"] for r in recs]))
    minw = max(2, int(min_run_frac * H))
    band = max(1, int(band_frac * H))
    out = []
    for r in recs:
        bot = np.unpackbits(r["bottom"], axis=-1, count=r["bot_w"]).astype(bool)
        lo = max(0, bot.shape[0] - 1 - band)
        out.append(runs_of(bot[lo:].sum(0) > 0, minw))
    return out


# --------------------------------------------------------------------------
# the measurements
# --------------------------------------------------------------------------
def pair_series(recs, key, order=None):
    n = len(recs)
    order = order if order is not None else list(range(n))
    vals, shifts = [], []
    for k in range(1, n):
        a, b = recs[order[k]], recs[order[k - 1]]
        v, dy, dx, ov = L.residual(a[key], a[key + "_m"], b[key], b[key + "_m"])
        vals.append(v)
        shifts.append((dy, dx))
    return vals, shifts


PHASE_STEPS = 12          # the common sampling: one twelfth of a stride


def lag_series(recs, key, lag):
    """Drift between frames LAG apart, rather than adjacent ones."""
    out = []
    for k in range(lag, len(recs)):
        a, b = recs[k], recs[k - lag]
        out.append(L.residual(a[key], a[key + "_m"], b[key], b[key + "_m"])[0])
    return out


def vs_ref(recs, key, ref):
    out = []
    for r in recs:
        v, dy, dx, ov = L.residual(r[key], r[key + "_m"], ref[key], ref[key + "_m"])
        out.append(v)
    return out


def worst_pairs(vals, k=3):
    """vals[j] is the step from frame j to frame j+1."""
    idx = np.argsort(vals)[::-1][:k]
    return [dict(frames=[int(i), int(i + 1)], value=round(float(vals[i]), 2))
            for i in idx]


def worst_pairs_lag(vals, lag, k=3):
    """vals[j] is the step from frame j to frame j+lag."""
    idx = np.argsort(vals)[::-1][:k]
    return [dict(frames=[int(i), int(i + lag)], value=round(float(vals[i]), 2))
            for i in idx]


def worst_frames(vals, k=3):
    idx = np.argsort(vals)[::-1][:k]
    return [dict(frame=int(i), value=round(float(vals[i]), 2)) for i in idx]


DEPTH_GATE = 0.80          # D(min)/mean(D) above this = no repeat found
TRAVEL_GATE = 5.0          # % of figure height over the clip: below this, in-place


def cadence(recs, fps):
    """Stride period from the whole-frame repeat, not from foot separation.

    measure_strides.py's finding, reused: a walk's two halves are near-mirrors,
    so a silhouette cannot tell one stride from two.  The pollaxe, the far arm
    and the tabard do NOT mirror, so the masked crop repeats once per STRIDE.

        D(p) = mean |frame_i - frame_{i+p}| over every available pair

    is measured NON-cyclically -- Kling's 150 frames are not a whole number of
    strides and wrapping them would compare the end of one stride against the
    middle of another.

    THE ANSWER CAN BE "NO REPEAT IN RANGE", and saying so matters.  A clip that
    holds exactly one stride has no interior minimum at all: D just climbs to
    p = n/2 and comes back.  The first version of this returned p = 5 with a
    depth ratio of 0.987 for the 12-frame Astra cell -- a confident number off
    a profile with no dip in it, on a clip that is one stride BY CONSTRUCTION.
    So a minimum shallower than DEPTH_GATE is reported as not found, and the
    clip length is used as the period with the substitution declared.

    THE FUNDAMENTAL IS THE SMALLEST QUALIFYING MINIMUM, NOT THE DEEPEST.  The
    drive's profile dips at 17, 34, 50, 68, 84, 102, 119, 136 -- harmonics --
    and the DEEPEST is 119, because render_drive.py wrapped a ~4 s Meshy clip
    to fill 5 s and frames 119 apart are literally the same frame.  Taking the
    deepest returned a stride period of 3.97 s for a walking figure and did not
    look like an error.

    THEN THE MIRROR CHECK, which is measure_strides.py's finding and is why 17
    is also wrong.  Half a stride is a near-mirror of the other half, so D dips
    at the STEP as well as at the stride.  The drive carries no weapon and its
    tabard is near-symmetric, so its step dip is strong.  Verified by eye on
    frames 0/8/17/25/34: frame 34 matches frame 0 and frame 17 is the opposite
    phase.  So a candidate p is doubled while D(2p) is clearly lower than D(p):
    a real half-period always has a better match one octave up.
    """
    S = np.stack([r["small"] for r in recs])
    n = len(S)
    ps = list(range(3, max(4, n - 3) + 1))
    D = np.array([float(np.abs(S[:n - p] - S[p:]).mean()) for p in ps])
    mean = float(D.mean())
    at = {p: float(d) for p, d in zip(ps, D)}
    cands = [ps[k] for k in range(1, len(D) - 1)
             if D[k] <= D[k - 1] and D[k] <= D[k + 1] and D[k] < DEPTH_GATE * mean]
    found = bool(cands)
    doubled = []
    if found:
        period = min(cands)
        while 2 * period in at and at[2 * period] < 0.90 * at[period]:
            doubled.append(2 * period)
            period = 2 * period
    else:
        period = n
    depth = at.get(period, float(D.min())) / mean
    return dict(period_frames=int(period), fps=round(float(fps), 3),
                stride_period_s=round(period / fps, 4),
                strides_per_s=round(fps / period, 3),
                strides_in_clip=round(n / period, 2),
                repeat_found=bool(found),
                depth_ratio=round(float(depth), 3),
                local_minima=[int(c) for c in cands],
                doubled_to=doubled,
                source=("smallest qualifying minimum of D(p)"
                        + (", doubled past the step mirror to %d" % period
                           if doubled else "")
                        if found else
                        "NO repeat in range (no local minimum below %.2f x mean); "
                        "the clip is treated as ONE stride and the period is its "
                        "length" % DEPTH_GATE),
                profile={str(p): round(float(d), 3) for p, d in zip(ps, D)})


MIN_FRAMES_PER_STRIDE = 16


def foot_slide(recs, runs, period):
    """Does the planted foot hold the ground, or does it skate under the body?

    WHAT "PLANTED" MEANS HERE, because the obvious measure is the wrong one.
    These clips walk IN PLACE, so a correctly planted foot is NOT stationary:
    the ground passes under it, and it tracks BACKWARD at a constant speed --
    the gait speed -- for the whole of its contact.  Measuring the foot's raw
    excursion therefore scores a perfect walk as a large slide, which is what
    the first version of this did.

    What a slide actually looks like is DEPARTURE FROM THAT STRAIGHT LINE: a
    foot that stalls, jerks, reverses or is re-drawn somewhere else.  So each
    contact track's x (minus the body's own translation, so a clip that does
    travel is handled the same way) is fitted with a straight line, and

        slip_rms_pct_H = RMS residual about that line, in % of figure height

    is the number.  Zero is a foot nailed to the passing ground.  The fitted
    slope is reported too as contact_travel: it should be the same for every
    contact in the clip, so its spread across tracks catches the other failure
    -- one foot keeping up with the gait while the other does not.

    The drive row is the reference value: it is a rigged mesh, so its slip is
    whatever this measurement costs on a walk that is correct by construction.

    WHICH TRACKS COUNT.  Both feet are tracked, but only the PLANTED ones are
    scored, and "planted" is decided from the data rather than assumed: the
    backward direction is the sign of the median per-frame contact step, which
    the planted phase wins because a foot is down for more of the cycle than it
    is up.  The swing foot is excluded -- it is SUPPOSED to travel fast and
    curve, and scoring it would bury the planted foot's numbers in noise.

    THE BODY'S OWN TRANSLATION is subtracted only if the clip actually travels.
    The silhouette's column centroid is not a root: on the drive it swings
    +-3.5% of figure height with the arms while the trend over 70 frames is
    -3.4%, so subtracting it frame by frame ADDS limb swing to the feet.  A
    straight line is fitted to it instead, and only that trend is removed, and
    only when it exceeds TRAVEL_GATE over the clip.
    """
    if period < MIN_FRAMES_PER_STRIDE:
        return dict(measurable=False, frames_per_stride=int(period),
                    note="NOT MEASURABLE at %d frames per stride (needs >= %d). "
                         "Each foot is down for only 6-7 frames and the two cross "
                         "within the linking tolerance, so the tracker welds them "
                         "into one track spanning the whole clip and returns a slip "
                         "number for an object that is not a foot. Reported as not "
                         "measurable rather than as 10.6%% of figure height."
                         % (period, MIN_FRAMES_PER_STRIDE))
    H = float(np.median([r["H"] for r in recs]))
    cxs = np.array([r["cx"] for r in recs])
    t_all = np.arange(len(cxs), dtype=float)
    slope = float(np.polyfit(t_all, cxs, 1)[0])
    travels = abs(slope) * len(cxs) / H > TRAVEL_GATE
    base = slope * t_all if travels else np.zeros_like(t_all)

    def link(tol):
        tracks, live, steps = [], [], []
        for k, rs in enumerate(runs):
            adj = [x - base[k] for x in rs]
            used, nxt = set(), []
            for tr in live:
                cand = [(abs(x - tr["x"][-1]), j, x) for j, x in enumerate(adj)
                        if j not in used and abs(x - tr["x"][-1]) < tol]
                if cand:
                    _, j, x = min(cand)
                    used.add(j)
                    steps.append(x - tr["x"][-1])
                    tr["x"].append(x)
                    nxt.append(tr)
                else:
                    tracks.append(tr)
            for j, x in enumerate(adj):
                if j not in used:
                    nxt.append(dict(start=k, x=[x]))
            live = nxt
        return tracks + live, steps

    # THE TOLERANCE HAS TO COME FROM THE CLIP, not from a constant.  A foot's
    # travel per frame is set by frames-per-stride, and that ranges from 12
    # (the Astra cell) to 34 (the drive) across these rows: a fixed 0.08 x H
    # linked nothing at all on the 12-frame cells (0 tracks) while being loose
    # enough on the drive to weld the two feet into one 41-frame track.  So a
    # generous first pass measures the typical step, and the real pass uses
    # three times that, bounded either side.
    _, probe = link(0.25 * H)
    if not probe:
        return dict(measurable=False, tracks=0,
                    note="no contact run was linked across two frames")
    typ = float(np.median(np.abs(probe)))
    tol = float(np.clip(3.0 * typ, 0.04 * H, 0.25 * H))
    tracks, steps = link(tol)
    if not steps:
        return dict(measurable=False, tracks=0,
                    note="no contact run was linked across two frames")
    backward = 1.0 if float(np.median(steps)) >= 0 else -1.0

    out = []
    for tr in tracks:
        if len(tr["x"]) < 4:
            continue
        rel = np.array(tr["x"]) - tr["x"][0]
        t = np.arange(len(rel), dtype=float)
        A = np.stack([t, np.ones_like(t)], 1)
        coef, *_ = np.linalg.lstsq(A, rel, rcond=None)
        res = rel - A @ coef
        out.append(dict(start=int(tr["start"]), frames=int(len(rel)),
                        planted=bool(coef[0] * backward > 0),
                        slip_rms_pct_H=round(float(np.sqrt((res ** 2).mean())) / H * 100, 2),
                        travel_pct_H=round(float(coef[0] * (len(rel) - 1)) * backward / H * 100, 2)))
    planted = [t for t in out if t["planted"]]
    if not planted:
        return dict(measurable=False, tracks=len(out), planted_tracks=0,
                    note="no contact moved with the gait for 4 frames",
                    per_track=out)
    sl = np.array([t["slip_rms_pct_H"] for t in planted])
    tv = np.array([t["travel_pct_H"] for t in planted])
    return dict(measurable=True, tracks=len(out), planted_tracks=len(planted),
                body_translates=bool(travels),
                body_trend_pct_H_over_clip=round(slope * len(cxs) / H * 100, 2),
                contact_frames_median=int(np.median([t["frames"] for t in planted])),
                slip_rms_pct_H_median=round(float(np.median(sl)), 2),
                slip_rms_pct_H_p90=round(float(np.percentile(sl, 90)), 2),
                slip_rms_pct_H_max=round(float(sl.max()), 2),
                planted_travel_pct_H_median=round(float(np.median(tv)), 2),
                planted_travel_spread_pct_H=round(float(np.percentile(tv, 90) -
                                                        np.percentile(tv, 10)), 2),
                per_track=out)


HAFT_MIN_LEN_PCT_H = 40.0     # a pollaxe haft is longer than 40% of the figure


def pollaxe(recs):
    """A GATE FIRST, because the un-gated version returned numbers for a figure
    that is not holding anything.  The drive carries no weapon, and the disk
    opening still finds thin things -- fingers, a foot, the tabard's edge --
    so a haft was "found" in all 150 frames with a length CV of 69% and a
    median length of 19% of figure height.  Nothing there was a pollaxe.  A
    haft is rejected unless it is at least HAFT_MIN_LEN_PCT_H long, and a route
    whose frames mostly fail that is reported as carrying no rigid weapon."""
    hs = [r["haft"] for r in recs
          if r["haft"] and r["haft"]["len_pct_H"] >= HAFT_MIN_LEN_PCT_H]
    if len(hs) < max(4, 0.5 * len(recs)):
        return dict(frames_with_haft=len(hs), frames=len(recs),
                    note="NO rigid weapon: fewer than half the frames hold a "
                         "straight structure at least %.0f%% of figure height"
                         % HAFT_MIN_LEN_PCT_H)
    ln = np.array([h["len_pct_H"] for h in hs])
    an = np.array([h["angle_from_vertical_deg"] for h in hs])
    st = np.array([h["straightness_pct"] for h in hs])
    dang = np.abs(np.diff(an))
    return dict(frames_with_haft=len(hs),
                len_pct_H_median=round(float(np.median(ln)), 1),
                len_cv_pct=round(float(100 * ln.std() / max(ln.mean(), 1e-6)), 1),
                len_pct_H_range=[round(float(ln.min()), 1), round(float(ln.max()), 1)],
                straightness_pct_median=round(float(np.median(st)), 2),
                straightness_pct_p90=round(float(np.percentile(st, 90)), 2),
                angle_deg_median=round(float(np.median(an)), 1),
                angle_deg_std=round(float(an.std()), 2),
                d_angle_deg_p90=round(float(np.percentile(dang, 90)), 2),
                d_angle_deg_max=round(float(dang.max()), 2))


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--routes", default="kling,hydra,forge,anim,drive,render3d,astra")
    ap.add_argument("--out", default=os.path.join(HERE, "drift.json"))
    args = ap.parse_args()

    defs = route_defs()
    ref_g = L.frame_geometry(REF, "green")
    rhp, rhm, _ = L.helm_patch(ref_g)
    rbp, rbm, _ = L.body_patch(ref_g)
    ref = dict(helm=rhp.astype(np.float32), helm_m=rhm,
               body=rbp.astype(np.float32), body_m=rbm)
    ref_meta = dict(figure_h_px=ref_g["H"], helm_h_px=ref_g["neck"] - ref_g["crown"],
                    haft=haft_fit(ref_g))
    del ref_g

    rng = np.random.default_rng(7)
    rep = dict(
        what="C-9 test 4: which video route holds the knight's identity frame to frame",
        instrument=dict(
            base="meshy_t2/scripts/21_drift.py (T1/T2 low-pass drift)",
            kept=["gaussian sigma %.1f px, mask-normalised" % L.BLUR_SIGMA,
                  "%d px silhouette erosion" % L.ERODE_PX,
                  "mean |dRGB| in 0-255 over the shared silhouette",
                  "shuffled frame order as the negative control",
                  "a sequence that cannot drift as the floor"],
            changed=dict(
                why="21_drift.py compensates for the animation with a POS GUIDE -- "
                    "the rest-pose bind position under each pixel, baked per vertex "
                    "before skinning. It exists only for frames we rendered ourselves "
                    "from a rigged mesh. Kling and Ludo return video: no mesh, no bind "
                    "pose, no pos pass, so the nearest-neighbour-in-pos-space match "
                    "cannot be computed at all. The input is missing, not the method "
                    "disputed.",
                substitution="2D rigid registration: the crop is placed on the part's "
                             "own position each frame, resampled to a common size, and "
                             "the best integer translation within +-%d px is searched "
                             "before the residual is taken. Rotation is deliberately "
                             "NOT absorbed -- the complaint was that the helm morphs "
                             "WHEN THE HEAD TURNS, and a rotation-free registration "
                             "would explain away the frames the test exists to catch."
                             % L.SHIFT,
                also_new="scale normalisation. Kling returns 1440 px, Ludo 310-454 px, "
                         "the still 1024 px; blurring all of them by 3 px would "
                         "low-pass Ludo four times as hard as Kling and hand Ludo a "
                         "lower score for free. Every helm crop is resampled to %d px "
                         "of helm and every body crop to %d px of figure BEFORE the "
                         "blur." % (L.HELM_H, L.BODY_H),
                validation="see validate_fallback.py -- the 2D fallback and the "
                           "original pos-matched instrument are run on the SAME "
                           "sequence (the knight's Astra walk E, the one candidate "
                           "with pos guides on disk) and compared."),
            helm_region="crown row to the NECK PINCH, found per frame from the body's "
                        "own row-width profile (the profile rises across the helm, "
                        "falls to a minimum at the gorget, rises into the shoulders). "
                        "The box is square, 1.5x the helm height, centred on the helm's "
                        "column centroid: it MOVES with the helm and does not RESIZE.",
            weapon_split="disk opening of radius ~1.6% of mask height. A 1xN "
                         "HORIZONTAL opening (build_knight_frames.py's rule) is wrong "
                         "here and was caught by probing: Kling re-stages the pollaxe "
                         "at a lean, and a diagonal bar's horizontal runs are far wider "
                         "than its thickness, so the horizontal opening left most of "
                         "Kling's haft inside the body (6.9k weapon px against the "
                         "still's 27.3k) and returned a confident wrong answer."),
        reference_still=dict(path="fal_t4/knight_E_ref_1024.png", **ref_meta),
        drive=dict(path="fal_t4/knight_carrywalk_E_drive.mp4",
                   frames=150, fps=30.0, seconds=5.0),
        routes={})

    CANDIDATES = ("kling", "hydra", "forge", "anim")
    for name in args.routes.split(","):
        cfg = defs[name]
        sys.stderr.write("== %s (%d frames)\n" % (name, len(cfg["frames"])))
        recs = extract(cfg)
        runs = contacts(recs)
        n = len(recs)

        hv, hs = pair_series(recs, "helm")
        bv, bs = pair_series(recs, "body")
        cad = cadence(recs, cfg["fps"])
        lag = max(1, int(round(cad["period_frames"] / float(PHASE_STEPS))))
        hlag = lag_series(recs, "helm", lag) if lag > 1 else hv
        blag = lag_series(recs, "body", lag) if lag > 1 else bv
        order = list(rng.permutation(n))
        hv_sh, _ = pair_series(recs, "helm", order=order)
        bv_sh, _ = pair_series(recs, "body", order=order)
        hr = vs_ref(recs, "helm", ref)
        br = vs_ref(recs, "body", ref)

        seam_h = L.residual(recs[0]["helm"], recs[0]["helm_m"],
                            recs[-1]["helm"], recs[-1]["helm_m"])[0]
        seam_b = L.residual(recs[0]["body"], recs[0]["body_m"],
                            recs[-1]["body"], recs[-1]["body_m"])[0]
        S = np.stack([r["small"] for r in recs])
        pose_step = float(np.abs(S[1:] - S[:-1]).mean())
        pose_seam = float(np.abs(S[0] - S[-1]).mean())

        rep["routes"][name] = dict(
            label=cfg["label"], frames=n, fps=round(cfg["fps"], 3),
            seconds=round(n / cfg["fps"], 3),
            native=dict(figure_h_px_median=int(np.median([r["H"] for r in recs])),
                        helm_h_px_median=int(np.median([r["helm_h_native"] for r in recs]))),
            helm_drift_frame_to_frame=dict(**(L.stats(hv) or {}),
                                           worst=worst_pairs(hv),
                                           shuffled=L.stats(hv_sh)),
            helm_drift_vs_reference_still=dict(
                **(L.stats(hr) or {}), worst=worst_frames(hr),
                comparable=name in CANDIDATES,
                note=("" if name in CANDIDATES else
                      "NOT a candidate and NOT comparable: this row never started "
                      "from that still, so what is measured here is two different "
                      "pictures of a knight. Reported only as a scale marker -- it "
                      "is what 'a different figure entirely' costs on this "
                      "instrument.")),
            body_drift_frame_to_frame=dict(**(L.stats(bv) or {}),
                                           worst=worst_pairs(bv),
                                           shuffled=L.stats(bv_sh)),
            body_drift_vs_reference_still=dict(
                **(L.stats(br) or {}), worst=worst_frames(br),
                comparable=name in CANDIDATES),
            registration_shift_px=dict(
                helm_max_abs=[int(np.abs(np.array([s[0] for s in hs])).max()),
                              int(np.abs(np.array([s[1] for s in hs])).max())],
                note="dy,dx at %d px of helm height; hitting the +-%d cap means the "
                     "part moved further than the search and the residual is an "
                     "upper bound" % (L.HELM_H, L.SHIFT)),
            helm_drift_phase_matched=dict(
                **(L.stats(hlag) or {}), lag_frames=int(lag),
                worst=worst_pairs_lag(hlag, lag),
                why="THE HEADLINE NUMBER, and the reason the raw frame-to-frame "
                    "column cannot be read straight across the table. Adjacent "
                    "frames are not the same amount of ANIMATION in every row: the "
                    "Astra cell holds a whole stride in 12 frames, the drive takes "
                    "34, so the Astra row's neighbours are three times further "
                    "apart in pose and the 2D registration has three times as much "
                    "pose change to fail to absorb. Measured, not assumed: the raw "
                    "floor is 1.01 at 34 frames per stride and 8.20 at 12. So every "
                    "row is also measured at a lag of one twelfth of ITS OWN stride, "
                    "which is the same pose increment everywhere."),
            body_drift_phase_matched=dict(**(L.stats(blag) or {}),
                                          lag_frames=int(lag)),
            cadence=cad,
            foot_slide=foot_slide(recs, runs, cad["period_frames"]),
            pollaxe=pollaxe(recs),
            loop_seam=dict(
                helm_last_to_first=round(float(seam_h), 2),
                helm_consecutive_median=round(float(np.median(hv)), 2),
                helm_seam_ratio=round(float(seam_h / max(np.median(hv), 1e-6)), 2),
                body_last_to_first=round(float(seam_b), 2),
                body_consecutive_median=round(float(np.median(bv)), 2),
                body_seam_ratio=round(float(seam_b / max(np.median(bv), 1e-6)), 2),
                pose_seam_ratio=round(float(pose_seam / max(pose_step, 1e-6)), 2),
                note="1.0 = the wrap is as smooth as an ordinary step; high = a visible "
                     "jump at the loop point"),
        )
        del recs, S

    with open(args.out, "w") as f:
        json.dump(rep, f, indent=1)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
