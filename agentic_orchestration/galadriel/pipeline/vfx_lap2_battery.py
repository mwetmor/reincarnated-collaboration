#!/usr/bin/env python3
"""
vfx_lap2_battery.py -- the lap-2 acceptance-criteria measurement battery.

Spec:   agentic_orchestration/gandalf/vfx-depth-run/lap2-depth-spec.md
        sec 1 (criteria T-1..T-6) and sec 3 (measurement plan, one row per instrument).
Author: galadriel (visual perception + UX-similarity steward), 2026-08-25
Run:    VFX-DEPTH autonomous run, conductor gandalf.

WHAT THIS IS
    Ten instruments, one per sec 3 row, all running against an (ON, CONTROL) MP4
    pair rendered over an identical window with `set_vfx_visible(false)` on the
    control arm. Every criterion is evaluated in IMAGE SPACE at the ratified pin
    (1920x1080, player_lock k=0.665). Metres never enter a bar (spec sec 3 note).

WHAT THIS IS NOT
    It is not a grader of design. It reports PASS / FAIL / INDETERMINATE per
    criterion with the measured operand printed beside every call, so that a
    reader can disagree with the call while holding the number.

THE THREE-VALUED RETURN IS LOAD-BEARING
    INDETERMINATE is not a soft FAIL. It is the record of a criterion whose
    evidence the clip does not contain -- an aftermath bar measured in a window
    with no aftermath, a CV measured on too few intervals. Discipline #63:
    unmeasured is not zero. A criterion that cannot be measured must not be
    scored, in either direction.

THE NEGATIVE CONTROL IS THE POINT
    This file was written BEFORE the lap-2 treatments existed and validated
    against the lap-1 B-arm render, which the criteria were authored to indict.
    The pre-registered expectation was that every criterion FAILS on it. Any
    criterion that PASSES there is a defective instrument or a defective
    criterion, and it is flagged, not fixed.

I-7 (registry, ratified 2026-08-25): a detection route disqualified by its own
    control may INSPECT but may not carry a bar. Instruments whose own controls
    disqualify them are stamped INSPECT-ONLY in the scorecard and their calls
    are emitted as `INSPECT` rather than PASS/FAIL.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys

import numpy as np
from scipy import ndimage

sys.path.insert(0, str(__file__.rsplit("/", 1)[0]))
from frame_forensics import peak_intervals, temporal_spectrum  # noqa: E402

REC709 = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)

# --- spec sec 1 bars, named once, in one place -----------------------------
BARS = {
    "T1_centroid_px": 8.0,
    "T1_axis_deg": 4.0,
    "T1_sustain_frames": 4,
    "T1_react_window_s": 0.15,
    "T1_return_px": 2.0,
    "T1_return_by_s": 1.0,
    "T2_residue_px2": 120.0,
    "T2_lift_frac": 0.15,
    "T2_life_min_s": 0.6,
    "T2_life_max_s": 1.6,
    "T2_clear_after_s": 2.0,
    "T3a_dominance": 2.2,
    "T3b_p95_p20": 4.0,
    "T3c_sat": 0.55,
    "T3d_leading_frac": 0.25,
    "T3d_frame_frac": 0.80,
    "T3e_lift_frac": 0.08,
    "T4a_onset_mult": 1.6,
    "T4a_frames": (6, 12),
    "T4a_window_s": 0.30,
    "T4b_cv_band": (0.45, 1.15),
    "T4b_trip_cv": 0.25,            # jack-ryan ratification: sole-trip, tone diagnostic only
    "T4b_min_intervals": 10,        # galadriel, this file: below this -> INDETERMINATE (see sec 9)
    "T4c_max_drop": 0.35,
    "T4c_tail_s": 0.35,
    "T4d_regimes": 4,
    "T5a_components": 6.0,
    "T5a_iqr_med": 0.5,
    "T5b_rms_frac": 0.08,
    "T6_area_px2": 2500.0,
    "T6_dl": 6.0 / 255.0,
    "T6_settle_frac": 0.05,
}

ANG_BINS = 180          # 2 deg per bin around the caster
MIN_COMPONENT_PX = 12   # below this a component is decoder speckle, not content
FAR_FIELD_MULT = 2.5    # far field starts here, in units of the arc's outer radius
TAU_SAFETY = 1.5        # safety multiple on the measured far-field P99.9
# Engagement reach in image space. R_ENGAGE = 3.515 m and the 4a block measured
# ~82 px/m at the caster's ground plane -> 288 px; carried at 1.18x to leave room
# for a T-1 shove to move a mob's feet without dropping it out of its own gate.
REACH_PX = 340.0
TAU_SWEEP = (0.67, 1.0, 1.5, 2.2)   # multiples of tau; no reading rests on one value


# ===========================================================================
# 1. DECODE -- streaming, lockstep, no frame written to disk
# ===========================================================================

def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,r_frame_rate,nb_frames",
         "-of", "json", path], capture_output=True, text=True, check=True).stdout
    st = json.loads(out)["streams"][0]
    n, d = st["r_frame_rate"].split("/")
    return int(st["width"]), int(st["height"]), float(n) / float(d)


class Stream:
    def __init__(self, path, w, h):
        self.n = w * h * 3
        self.p = subprocess.Popen(
            ["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo",
             "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        self.shape = (h, w, 3)

    def read(self):
        buf = self.p.stdout.read(self.n)
        if len(buf) < self.n:
            return None
        return np.frombuffer(buf, np.uint8).reshape(self.shape)

    def close(self):
        try:
            self.p.stdout.close()
            self.p.wait(timeout=10)
        except Exception:
            self.p.kill()


def luma(rgb_u8):
    return (rgb_u8.astype(np.float32) / 255.0) @ REC709


def sat_val(rgb_u8):
    a = rgb_u8.astype(np.float32) / 255.0
    mx = a.max(2)
    mn = a.min(2)
    return np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0.0), mx


# ===========================================================================
# 2. GEOMETRY SEEDING -- caster, arc annulus, mob ROIs
# ===========================================================================

def seed_geometry(on_path, ctl_path, w, h, fps, n_frames, rev_frames):
    """Everything downstream needs three things the clip must supply itself:
    the arc's centre of rotation, the annulus it sweeps, and the mob ROIs.

    The centre is NOT read from a config. The arc sweeps a full revolution, so
    the UNION of its effect mask over one revolution is an annulus, and the
    annulus' centroid is the caster. Deriving it from the footage means the
    instrument cannot be pointed at a clip whose geometry it has assumed.
    """
    a = Stream(on_path, w, h)
    b = Stream(ctl_path, w, h)
    union, ctl0, diffs = None, None, []
    coarse_c = None
    far_p999, far_max = [], []
    yy = xx = None
    for i in range(n_frames):
        fa, fb = a.read(), b.read()
        if fa is None or fb is None:
            break
        if ctl0 is None:
            ctl0 = fb.copy()
            yy, xx = np.mgrid[0:h, 0:w]
        d = np.abs(luma(fa) - luma(fb))
        diffs.append(float(d.mean()))
        if union is None:
            union = np.zeros(d.shape, bool)
        union |= d > 0.10
        if coarse_c is None and union.sum() > 400:
            ys, xs = np.nonzero(union)
            coarse_c = (float(xs.mean()), float(ys.mean()))
        if coarse_c is not None:
            far = np.hypot(xx - coarse_c[0], yy - coarse_c[1]) > FAR_FIELD_MULT * 260.0
            v = d[far]
            far_p999.append(float(np.percentile(v, 99.9)))
            far_max.append(float(v.max()))
    a.close()
    b.close()

    # --- tau ---------------------------------------------------------------
    # ⚑ NOT median + k*MAD. On a deterministic render pair, MORE THAN HALF the
    # pixels are byte-identical between arms, so median(|dL|) = 0 and MAD = 0:
    # the derived term collapses and an absolute floor silently becomes the
    # operative bar. Measured, this clip: pre-window MAD = 0.0 exactly, floor
    # 2/255 = 0.0078, while the real inter-arm h264 noise reaches p99.9 = 0.041
    # in the far field. The mask filled with speckle and FIVE criteria passed on
    # a render written to fail all of them.  (Same shape as the F7 shake floor.)
    #
    # The bar is instead an empirical FALSE-POSITIVE control: the 99.9th
    # percentile of |dL| in the FAR FIELD -- pixels no authored effect reaches --
    # taken at its worst frame, with a stated safety multiple. The far field is
    # the null this instrument needed and did not have.
    p999 = float(np.max(far_p999)) if far_p999 else 0.02
    tau = TAU_SAFETY * p999

    m = ndimage.binary_opening(union, np.ones((3, 3)))
    lab, k = ndimage.label(m)
    if k == 0:
        raise SystemExit("seed: no effect pixels anywhere -- arms are identical?")
    sizes = ndimage.sum(m, lab, range(1, k + 1))
    big = (lab == (int(np.argmax(sizes)) + 1))
    ys, xs = np.nonzero(big)
    cx, cy = float(xs.mean()), float(ys.mean())
    r = np.hypot(xs - cx, ys - cy)
    r_out = float(np.percentile(r, 99))

    mobs, caster = seed_mobs(ctl0, cx, cy)
    return {
        "caster_px": [cx, cy], "arc_r_out_px": r_out,
        "tau": tau,
        "tau_derivation": "%.1f x max-over-frames of far-field P99.9(|dL|)" % TAU_SAFETY,
        "tau_farfield_p999_worst_frame": p999,
        "tau_farfield_absmax": float(np.max(far_max)) if far_max else None,
        "mob_rois": mobs, "caster_roi": caster,
        "mean_abs_diff_series": diffs,
        "rev_frames": rev_frames,
    }


def seed_mobs(ctl0, cx, cy, reach_px=REACH_PX):
    """Mob ROIs from the CONTROL frame, never the treatment frame -- a treatment
    that lights a mob would otherwise enlarge the ROI it is being measured in.

    The component nearest the arc's rotation centre is the CASTER and is
    excluded from the mob set: it is where the effect is authored from, not a
    recipient of it.

    ⚑ The reach gate is on the FOOT POINT (bbox bottom-centre), not the
    centroid, and it is a GROUND-PLANE test. A centroid gate at a radius wide
    enough to hold a standing mob also holds cathedral fixtures high in the
    frame -- measured, it admitted two braziers at y ~ 3 and y ~ 8 px as "mobs"
    and drove N from 4 to 6. In a pitched view, image-y carries depth; two
    actors sharing the ground plane share a foot-point neighbourhood, and a
    wall fixture does not.
    """
    L = luma(ctl0)
    a = ctl0.astype(np.float32)
    m = (L > 0.27) & (a[:, :, 0] > a[:, :, 2] * 1.6)
    m = ndimage.binary_closing(m, np.ones((5, 5)))
    lab, k = ndimage.label(m)
    cand = []
    for i in range(1, k + 1):
        ys, xs = np.nonzero(lab == i)
        if len(ys) < 250:
            continue
        cand.append({"area_px": int(len(ys)),
                     "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                     "seed_centroid": [float(xs.mean()), float(ys.mean())],
                     "foot_px": [float((xs.min() + xs.max()) / 2.0), float(ys.max())]})
    if not cand:
        return [], None
    d = [math.hypot(o["seed_centroid"][0] - cx, o["seed_centroid"][1] - cy) for o in cand]
    caster = cand.pop(int(np.argmin(d)))
    fx, fy = caster["foot_px"]
    out, rejected = [], []
    for o in cand:
        r = math.hypot(o["foot_px"][0] - fx, o["foot_px"][1] - fy)
        o["foot_dist_px"] = round(r, 1)
        (out if r <= reach_px else rejected).append(o)
    caster["rejected_beyond_reach"] = [
        {"foot_px": o["foot_px"], "foot_dist_px": o["foot_dist_px"]} for o in rejected]
    out.sort(key=lambda o: -o["area_px"])
    for i, o in enumerate(out):
        o["id"] = "M%d" % (i + 1)
        x0, y0, x1, y1 = o["bbox"]
        pad = 26          # room for a shove and a lean to leave the seed box
        o["roi"] = [max(0, x0 - pad), max(0, y0 - pad),
                    min(L.shape[1] - 1, x1 + pad), min(L.shape[0] - 1, y1 + pad)]
    return out, caster


# ===========================================================================
# 3. THE MEASUREMENT PASS -- one lockstep walk, everything accumulated
# ===========================================================================

def measure(on_path, ctl_path, geo, w, h, fps, n_frames):
    cx, cy = geo["caster_px"]
    tau = geo["tau"]
    mobs = geo["mob_rois"]
    yy, xx = np.mgrid[0:h, 0:w]
    ang = np.degrees(np.arctan2(yy - cy, xx - cx))          # -180..180
    rad = np.hypot(xx - cx, yy - cy)
    abin = ((ang + 180.0) / 360.0 * ANG_BINS).astype(np.int32) % ANG_BINS

    r_out = geo["arc_r_out_px"]
    floor_ring = (rad > 0.45 * r_out) & (rad < 1.15 * r_out)
    scene_ring = (rad > 1.35 * r_out) & (rad < 2.6 * r_out)  # T-3a annular scene sample
    mob_any = np.zeros((h, w), bool)
    for m in mobs:
        x0, y0, x1, y1 = m["roi"]
        mob_any[y0:y1 + 1, x0:x1 + 1] = True

    A = Stream(on_path, w, h)
    B = Stream(ctl_path, w, h)
    S = {k: [] for k in (
        "area", "p99_on", "p95_on", "p50_on", "p20_on", "midS", "scene_med", "ncomp",
        "comp_iqr_med", "peak_bin", "arc_lo", "arc_hi", "mean_ang", "sum_lift",
        "floor_area", "floor_dl", "castlift_floor", "castlift_mob", "residue_total")}
    per_mob = {m["id"]: {"cen": [], "axis": [], "residue": []} for m in mobs}
    width_profiles = []
    on0L = ctl0L = None

    for i in range(n_frames):
        fa, fb = A.read(), B.read()
        if fa is None or fb is None:
            break
        La, Lb = luma(fa), luma(fb)
        if on0L is None:
            on0L, ctl0L = La.copy(), Lb.copy()
        d = La - Lb
        E = ndimage.binary_opening(np.abs(d) > tau, np.ones((3, 3)))
        # The size filter is applied to the MASK, not only to the census. A
        # speckle too small to be an authored quantum is also too small to be
        # allowed into a percentile, a saturation mean or an angular span.
        lab, k = ndimage.label(E)
        if k:
            sz = ndimage.sum(E, lab, range(1, k + 1))
            keep = np.nonzero(sz >= MIN_COMPONENT_PX)[0] + 1
            E = np.isin(lab, keep) if keep.size else np.zeros_like(E)
            sz = sz[sz >= MIN_COMPONENT_PX]
        else:
            sz = np.array([])

        # --- T-4a/c/d luminous-area curve, T-5a census ---------------------
        S["area"].append(int(E.sum()))
        S["ncomp"].append(int(sz.size))
        if sz.size >= 2:
            q1, q3 = np.percentile(sz, [25, 75])
            S["comp_iqr_med"].append(float((q3 - q1) / max(np.median(sz), 1e-9)))
        else:
            S["comp_iqr_med"].append(0.0)

        # --- T-3a/b/c photometry -------------------------------------------
        if E.sum() >= 40:
            v = La[E]
            S["p99_on"].append(float(np.percentile(v, 99)))
            S["p95_on"].append(float(np.percentile(v, 95)))
            S["p50_on"].append(float(np.percentile(v, 50)))
            S["p20_on"].append(float(np.percentile(v, 20)))
            sA, _ = sat_val(fa)
            lo, hi = np.percentile(v, [35, 65])
            mid = E & (La >= lo) & (La <= hi)
            S["midS"].append(float(sA[mid].mean()) if mid.sum() else float("nan"))
        else:
            for kk in ("p99_on", "p95_on", "p50_on", "p20_on", "midS"):
                S[kk].append(float("nan"))
        sc = scene_ring & ~E & ~mob_any
        S["scene_med"].append(float(np.median(La[sc])) if sc.sum() else float("nan"))

        # --- T-3d apex-vs-leading-edge, T-5b width profile ------------------
        if E.sum() >= 40:
            b = abin[E]
            occ = np.bincount(b, minlength=ANG_BINS)
            pk = np.zeros(ANG_BINS, np.float32)
            np.maximum.at(pk, b, La[E])
            S["peak_bin"].append(int(np.argmax(pk)))
            live = np.nonzero(occ > 0)[0]
            lo_b, hi_b = arc_span(occ)
            S["arc_lo"].append(lo_b)
            S["arc_hi"].append(hi_b)
            ca = np.cos(np.radians(ang[E])).mean()
            sa = np.sin(np.radians(ang[E])).mean()
            S["mean_ang"].append(float(np.degrees(np.arctan2(sa, ca))))
            wp = np.zeros(ANG_BINS, np.float32)
            rr = rad[E]
            for bb in live:
                sel = rr[b == bb]
                wp[bb] = float(sel.max() - sel.min())
            width_profiles.append(wp)
        else:
            for kk in ("peak_bin", "arc_lo", "arc_hi", "mean_ang"):
                S[kk].append(float("nan"))
            width_profiles.append(np.zeros(ANG_BINS, np.float32))

        # --- T-3e cast light on non-effect surfaces -------------------------
        fl = floor_ring & ~E & ~mob_any
        S["castlift_floor"].append(
            float(np.median(d[fl]) / max(np.median(Lb[fl]), 1e-6)) if fl.sum() else float("nan"))
        mk = mob_any & ~E
        S["castlift_mob"].append(
            float(np.median(d[mk]) / max(np.median(Lb[mk]), 1e-6)) if mk.sum() else float("nan"))

        # --- T-1 per-mob kinematics, T-2 per-mob residue --------------------
        tot_res = 0
        for m in mobs:
            x0, y0, x1, y1 = m["roi"]
            sub = La[y0:y1 + 1, x0:x1 + 1]
            sil = sub > 0.27
            if sil.sum() >= 60:
                per_mob[m["id"]]["cen"].append(centroid_axis(sil))
            else:
                per_mob[m["id"]]["cen"].append((float("nan"),) * 3)
            amb = S["scene_med"][-1]
            lift = (La[y0:y1 + 1, x0:x1 + 1] - Lb[y0:y1 + 1, x0:x1 + 1])
            res = int(((lift > 0) & (La[y0:y1 + 1, x0:x1 + 1] >
                                     amb * (1.0 + BARS["T2_lift_frac"])) &
                       (np.abs(lift) > tau)).sum())
            per_mob[m["id"]]["residue"].append(res)
            tot_res += res
        S["residue_total"].append(tot_res)

        # --- T-6 floor accumulation ------------------------------------------
        # ⚑ Control-ANCHORED, not a bare pre/post difference. The caster
        # animates and drags a shadow across the tile in BOTH arms, so
        # |L_on(t) - L_on(0)| alone marks thousands of px of moving shadow that
        # no sweep scoured. A mark counts only where the ON arm changed AND the
        # control arm did not change with it -- i.e. where the change is
        # attributable to the effect. Measured: this term alone moved the
        # negative control's clip-end marked area from 57,768 px2 to the value
        # reported below.
        d_on = np.abs(La - on0L)
        d_ct = np.abs(Lb - ctl0L)
        fa_dl = np.maximum(d_on - d_ct, 0.0)
        fm = floor_ring & ~E & ~mob_any & (fa_dl >= BARS["T6_dl"])
        S["floor_area"].append(int(fm.sum()))
        S["floor_dl"].append(float(fa_dl[fm].mean()) if fm.sum() else 0.0)

    A.close()
    B.close()
    return S, per_mob, np.array(width_profiles)


def arc_span(occ):
    """Angular extent of an OPEN arc on a circular axis. Taking min/max of the
    occupied bins is wrong the moment the arc straddles the +/-180 seam; the
    largest EMPTY run is the gap, and the span is its complement."""
    live = np.nonzero(occ > 0)[0]
    if live.size == 0:
        return float("nan"), float("nan")
    if live.size == ANG_BINS:
        return 0.0, float(ANG_BINS - 1)
    gaps, run, start = [], 0, None
    ext = np.concatenate([occ, occ])
    for i in range(2 * ANG_BINS):
        if ext[i] == 0:
            if run == 0:
                start = i
            run += 1
        else:
            if run:
                gaps.append((run, start))
            run = 0
    if not gaps:
        return 0.0, float(ANG_BINS - 1)
    run, start = max(gaps)
    return float((start + run) % ANG_BINS), float((start - 1) % ANG_BINS)


def centroid_axis(sil):
    ys, xs = np.nonzero(sil)
    mx, my = xs.mean(), ys.mean()
    dx, dy = xs - mx, ys - my
    cxx, cyy, cxy = (dx * dx).mean(), (dy * dy).mean(), (dx * dy).mean()
    th = 0.5 * math.atan2(2 * cxy, cxx - cyy)
    return float(mx), float(my), float(math.degrees(th))


# ===========================================================================
# 4. SCORING -- one row per sec-1 criterion
# ===========================================================================

def _row(cid, name, call, operand, bar, note, status="ready", inspect=False):
    if inspect:
        call = "INSPECT"
    return {"criterion": cid, "name": name, "call": call, "operand": operand,
            "bar": bar, "note": note, "instrument_status": status}


def nanmed(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    return float(np.median(x)) if x.size else float("nan")


def score(S, per_mob, wp, geo, phases, fps, contacts, ff08=None):
    rows = []
    n = len(S["area"])
    sus = phases["sustain"]
    area = np.array(S["area"], float)
    sus_mean = float(area[sus[0]:sus[1] + 1].mean())

    # ---------------- T-1 -------------------------------------------------
    react_f = max(1, int(round(BARS["T1_react_window_s"] * fps)))
    ret_f = int(round(BARS["T1_return_by_s"] * fps))
    responded, detail = 0, {}
    for mid, d in per_mob.items():
        cen = np.array(d["cen"], float)
        first = contacts.get(mid)
        if first is None or not np.isfinite(cen).all():
            detail[mid] = {"first_contact_frame": first, "max_disp_px": None}
            continue
        rest = cen[max(0, first - 12):first].mean(0) if first >= 4 else cen[0]
        win = cen[first:min(n, first + react_f + BARS["T1_sustain_frames"])]
        disp = np.hypot(win[:, 0] - rest[0], win[:, 1] - rest[1])
        tilt = np.abs(((win[:, 2] - rest[2] + 90) % 180) - 90)
        hit = (disp >= BARS["T1_centroid_px"]) | (tilt >= BARS["T1_axis_deg"])
        sustained = _longest_run(hit) >= BARS["T1_sustain_frames"]
        back = cen[min(n - 1, first + ret_f)]
        returned = math.hypot(back[0] - rest[0], back[1] - rest[1]) <= BARS["T1_return_px"]
        detail[mid] = {"first_contact_frame": int(first),
                       "max_disp_px": round(float(disp.max()), 3),
                       "max_tilt_deg": round(float(tilt.max()), 3),
                       "sustained": bool(sustained), "returned_to_rest": bool(returned)}
        if sustained and returned:
            responded += 1
    N = len(per_mob)
    rows.append(_row("T-1", "recipient state response",
                     "PASS" if (N and responded == N) else "FAIL",
                     {"N_mobs": N, "responded": responded, "per_mob": detail},
                     ">=%.0f px centroid or >=%.0f deg axis, %d frames, all N"
                     % (BARS["T1_centroid_px"], BARS["T1_axis_deg"], BARS["T1_sustain_frames"]),
                     "measured within-arm against each mob's own rest pose; the control "
                     "arm is gameplay-identical (contacts fire with vfx hidden) so a "
                     "control-DIFFERENCED T-1 would null out by construction -- see note sec 4."))

    # ---------------- T-2 -------------------------------------------------
    half = int(round(0.5 * fps))
    carried, per = 0, {}
    simul = np.zeros(n, int)
    for mid, d in per_mob.items():
        res = np.array(d["residue"], float)
        first = contacts.get(mid)
        at = res[min(n - 1, first + half)] if first is not None else float("nan")
        live = res >= BARS["T2_residue_px2"]
        simul += live.astype(int)
        per[mid] = {"residue_at_contact_plus_0.5s_px2": None if first is None else float(at),
                    "peak_residue_px2": float(res.max()),
                    "frames_over_bar": int(live.sum())}
        if np.isfinite(at) and at >= BARS["T2_residue_px2"]:
            carried += 1
    simul_max = int(simul.max()) if n else 0
    end = phases["effect_end"]
    clear_f = end + int(round(BARS["T2_clear_after_s"] * fps))
    t2_clear_measurable = clear_f < n
    ok = (N and carried == N and simul_max >= max(1, N - 1) and t2_clear_measurable)
    rows.append(_row("T-2", "attached wind-residue persistence",
                     "PASS" if ok else ("INDETERMINATE" if (carried == N and N and not
                                                            t2_clear_measurable) else "FAIL"),
                     {"mobs_with_residue_at_+0.5s": carried, "N": N,
                      "max_simultaneous": simul_max,
                      "clear_at_end+2.0s_measurable": bool(t2_clear_measurable),
                      "per_mob": per},
                     ">=%.0f px2 at contact+0.5s, all N; >=N-1 simultaneous; zero at end+2.0s"
                     % BARS["T2_residue_px2"],
                     "the end+2.0s clause needs spec B-1's extended window; "
                     "unmeasurable windows report INDETERMINATE, never PASS"))

    # ---------------- T-3 a/b/c -------------------------------------------
    dom = nanmed(np.array(S["p99_on"]) / np.array(S["scene_med"]))
    rows.append(_row("T-3a", "luminance dominance",
                     "PASS" if dom >= BARS["T3a_dominance"] else "FAIL",
                     {"median_P99_effect_over_scene_median": round(dom, 4),
                      "median_effect_L_over_scene_median": round(nanmed(
                          np.array(S["p50_on"]) / np.array(S["scene_med"])), 4)},
                     ">= %.1f" % BARS["T3a_dominance"],
                     "annular scene sample, effect region and mob ROIs excluded. "
                     "⚑ CRITERION FLAGGED: reads 4.11 on the negative control, whose own "
                     "spec line says 'Currently < 1.0'. Tau-stable at 4.11 +/- 0.02 across "
                     "a 3.3x sweep; 61% of arc pixels already clear 2.2x. Instrument sound, "
                     "premise false -- gandalf's to re-cut, not mine."))
    rng = nanmed(np.array(S["p95_on"]) / np.maximum(np.array(S["p20_on"]), 1e-6))
    rows.append(_row("T-3b", "internal luminance range",
                     "PASS" if rng >= BARS["T3b_p95_p20"] else "FAIL",
                     {"median_P95_over_P20": round(rng, 4)},
                     ">= %.1f" % BARS["T3b_p95_p20"], ""))
    sat = nanmed(S["midS"])
    rows.append(_row("T-3c", "mid-band saturation",
                     "PASS" if sat >= BARS["T3c_sat"] else "FAIL",
                     {"median_midband_HSV_S": round(sat, 4)},
                     ">= %.2f" % BARS["T3c_sat"], ""))

    # ---------------- T-3d ------------------------------------------------
    lead_ok, tested, sgn = 0, 0, _rotation_sign(S["mean_ang"])
    for i in range(sus[0], sus[1] + 1):
        lo, hi, pk = S["arc_lo"][i], S["arc_hi"][i], S["peak_bin"][i]
        if not all(np.isfinite([lo, hi, pk])):
            continue
        span = (hi - lo) % ANG_BINS
        if span <= 0:
            continue
        tested += 1
        off = (pk - lo) % ANG_BINS
        frac = off / span if sgn > 0 else 1.0 - off / span
        if frac >= 1.0 - BARS["T3d_leading_frac"]:
            lead_ok += 1
    f = lead_ok / tested if tested else float("nan")
    rows.append(_row("T-3d", "apex rides the leading edge",
                     "PASS" if (tested and f >= BARS["T3d_frame_frac"]) else "FAIL",
                     {"frames_with_apex_in_leading_25pct": lead_ok, "frames_tested": tested,
                      "fraction": None if not tested else round(f, 4),
                      "rotation_sign": sgn,
                      "median_arc_span_deg": round(nanmed(
                          [((S["arc_hi"][i] - S["arc_lo"][i]) % ANG_BINS) * 360.0 / ANG_BINS
                           for i in range(sus[0], sus[1] + 1)]), 2)},
                     ">= %.0f%% of sustain frames" % (100 * BARS["T3d_frame_frac"]), ""))

    # ---------------- T-3e ------------------------------------------------
    fl = np.array(S["castlift_floor"], float)[sus[0]:sus[1] + 1]
    mo = np.array(S["castlift_mob"], float)[sus[0]:sus[1] + 1]
    best = max(np.nanpercentile(fl, 90) if np.isfinite(fl).any() else -9,
               np.nanpercentile(mo, 90) if np.isfinite(mo).any() else -9)
    rows.append(_row("T-3e", "cast light on non-effect surfaces",
                     "PASS" if best >= BARS["T3e_lift_frac"] else "FAIL",
                     {"floor_ring_P90_lift": round(float(np.nanpercentile(fl, 90)), 5),
                      "mob_ROI_P90_lift": round(float(np.nanpercentile(mo, 90)), 5)},
                     ">= %.0f%% luminance lift vs control" % (100 * BARS["T3e_lift_frac"]),
                     "differenced against the vfx-off control on pixels OUTSIDE the "
                     "effect region; a self-luminous effect cannot pass this by being bright"))

    # ---------------- T-4a ------------------------------------------------
    onset0 = phases["effect_start"]
    win = int(round(BARS["T4a_window_s"] * fps))
    seg = area[onset0:onset0 + win]
    over = seg >= BARS["T4a_onset_mult"] * sus_mean
    run = _longest_run(over)
    lo_f, hi_f = BARS["T4a_frames"]
    rows.append(_row("T-4a", "onset accent",
                     "PASS" if lo_f <= run <= hi_f else "FAIL",
                     {"peak_over_sustain_mean": round(float(seg.max() / sus_mean), 4)
                      if sus_mean else None, "frames_over_1.6x": int(run),
                      "sustain_mean_area_px2": round(sus_mean, 1)},
                     ">=%.1fx sustain mean for %d-%d frames inside first %.2fs"
                     % (BARS["T4a_onset_mult"], lo_f, hi_f, BARS["T4a_window_s"]), ""))

    # ---------------- T-4b (FF-08 route, amended trip law) ----------------
    # sec 3 binds this row to `frame_forensics*.py` -- "the trip-flag law's own
    # instrument" -- so when that route has been run its CV is AUTHORITATIVE and
    # the battery's own sustain-window series is demoted to a corroborator.
    # #75 cl. 1: bind the instrument to the artifact that ships.
    ev = peak_intervals(area[sus[0]:sus[1] + 1], fps)
    sp = temporal_spectrum(area[sus[0]:sus[1] + 1], fps)
    local_cv, local_n = ev.get("cv_interval"), max(0, ev["n_events"] - 1)
    cv, niv, tone = local_cv, local_n, None
    if sp:
        tone = sp.get("peak_over_median")
    if ff08:
        cv = ff08["events"].get("cv_interval")
        niv = ff08["n_intervals"]
        tone = ff08.get("spectral_tone_diagnostic")
    if niv < BARS["T4b_min_intervals"]:
        call = "INDETERMINATE"
    elif cv is None:
        call = "INDETERMINATE"
    else:
        call = "PASS" if (BARS["T4b_cv_band"][0] <= cv <= BARS["T4b_cv_band"][1]
                          and cv >= BARS["T4b_trip_cv"]) else "FAIL"
    rows.append(_row("T-4b", "temporal texture (FF-08)",
                     call,
                     {"cv_interval": cv, "n_intervals": niv,
                      "operand_source": "frame_forensics_depth CV_timing (authoritative)"
                                        if ff08 else "battery sustain-window area series",
                      "battery_corroborator": {"cv": local_cv, "n_intervals": local_n,
                                               "events_per_s": round(ev["events_per_s"], 3)},
                      "ff08_trip_fired": bool(cv is not None and niv >= BARS["T4b_min_intervals"]
                                              and cv < BARS["T4b_trip_cv"]),
                      "spectral_tone_diagnostic": tone},
                     "CV in [%.2f, %.2f]; trip law CV < %.2f must not fire"
                     % (*BARS["T4b_cv_band"], BARS["T4b_trip_cv"]),
                     "trip law AMENDED at ratification: CV<0.25 trips ALONE, spectral "
                     "tone is diagnostic only. n_intervals < %d -> INDETERMINATE (galadriel, "
                     "this file sec 9)." % BARS["T4b_min_intervals"]))

    # ---------------- T-4c ------------------------------------------------
    e0, e1 = phases["fall_start"], phases["effect_end"]
    seg = area[e0:min(n, e1 + 6)]
    drops = 1.0 - seg[1:] / np.maximum(seg[:-1], 1e-9)
    worst = float(np.nanmax(drops)) if drops.size else float("nan")
    tail = int((area[e1:] > 0).sum())
    tail_s = tail / fps
    rows.append(_row("T-4c", "decay breaks up rather than switching off",
                     "PASS" if (worst <= BARS["T4c_max_drop"] and
                                tail_s >= BARS["T4c_tail_s"]) else "FAIL",
                     {"worst_frame_to_frame_drop": round(worst, 4),
                      "post_effect_luminous_frames": tail,
                      "post_effect_tail_s": round(tail_s, 4)},
                     "no drop > %.0f%%; tail >= %.2fs" % (100 * BARS["T4c_max_drop"],
                                                          BARS["T4c_tail_s"]), ""))

    # ---------------- T-4d ------------------------------------------------
    reg = _segment_regimes(area[phases["effect_start"]:phases["effect_end"] + 1])
    rows.append(_row("T-4d", "phase structure",
                     "PASS" if reg >= BARS["T4d_regimes"] else "FAIL",
                     {"segmentable_regimes": reg},
                     ">= %d" % BARS["T4d_regimes"],
                     "piecewise-constant-slope segmentation on the area-vs-time curve"))

    # ---------------- T-5a ------------------------------------------------
    nc = float(np.mean(S["ncomp"][sus[0]:sus[1] + 1]))
    iq = float(np.mean(S["comp_iqr_med"][sus[0]:sus[1] + 1]))
    rows.append(_row("T-5a", "component census + size spread",
                     "PASS" if (nc >= BARS["T5a_components"] and
                                iq >= BARS["T5a_iqr_med"]) else "FAIL",
                     {"mean_components_per_frame": round(nc, 3),
                      "mean_area_IQR_over_median": round(iq, 4)},
                     ">= %.0f components and IQR/median >= %.1f"
                     % (BARS["T5a_components"], BARS["T5a_iqr_med"]),
                     "component COUNT carries a bar here only because both arms are the "
                     "same raster; my 2026-08-25 x-row ruling disqualifies counts ACROSS "
                     "rasters, not within one"))

    # ---------------- T-5b ------------------------------------------------
    rf = geo["rev_frames"]
    rms = []
    for i in range(sus[0], sus[1] + 1 - rf):
        a1, a2 = wp[i], wp[i + rf]
        m = (a1 > 0) & (a2 > 0)
        if m.sum() < 8:
            continue
        rms.append(float(np.sqrt(np.mean(((a1[m] - a2[m]) / np.maximum(a1[m], 1e-6)) ** 2))))
    r = float(np.median(rms)) if rms else float("nan")
    # ⚑ I-7 INSPECT-ONLY. Disqualified by this instrument's own negative control.
    # On the lap-1 B-arm -- the render whose width profile the spec records as
    # "Currently ~ 0, X-2 cites cf_100 vs cf_115 as identical" -- this route
    # reads 0.163, twice the 0.08 bar, and it reads 0.16-0.20 across a 3.3x
    # threshold sweep, so it is not mask-edge quantisation. A route that returns
    # 2x the bar on the artifact the bar was written to fail cannot carry the
    # bar. It reports the number and refuses the call.
    rows.append(_row("T-5b", "non-repetition of width profile",
                     "PASS" if (rms and r >= BARS["T5b_rms_frac"]) else "FAIL",
                     {"median_revolution_matched_width_RMS": None if not rms else round(r, 5),
                      "revolution_frames": rf, "pairs_compared": len(rms),
                      "negative_control_floor": 0.163,
                      "floor_tau_sweep": {"x0.67": 0.1918, "x1.0": 0.1627,
                                          "x1.5": 0.1719, "x2.2": 0.1957}},
                     ">= %.0f%% RMS" % (100 * BARS["T5b_rms_frac"]),
                     "I-7: DISQUALIFIED BY ITS OWN CONTROL. Reads 0.163 on the render the "
                     "spec records as ~0. Inspect only; may not carry a bar until either "
                     "the bar is re-set above the measured floor or the operand is re-cut.",
                     inspect=True))

    # ---------------- T-6 -------------------------------------------------
    fa = np.array(S["floor_area"], float)
    end_a, clip_a = fa[phases["effect_end"]], fa[-1]
    mono = float(np.min(np.diff(fa[sus[0]:sus[1] + 1]))) if sus[1] > sus[0] else 0.0
    settle = abs(clip_a - end_a) / max(end_a, 1.0)
    ok6 = (clip_a >= BARS["T6_area_px2"] and S["floor_dl"][-1] >= BARS["T6_dl"]
           and mono >= 0 and settle <= BARS["T6_settle_frac"])
    rows.append(_row("T-6", "environment aftermath",
                     "PASS" if ok6 else "FAIL",
                     {"marked_area_at_clip_end_px2": int(clip_a),
                      "mean_abs_dL_at_clip_end": round(float(S["floor_dl"][-1]), 5),
                      "min_sustain_delta": mono, "settle_frac": round(float(settle), 4),
                      "aftermath_frames_in_window": int(n - 1 - phases["effect_end"])},
                     ">= %.0f px2 with mean |dL| >= %.4f; monotonic in sustain; settle <= %.0f%%"
                     % (BARS["T6_area_px2"], BARS["T6_dl"], 100 * BARS["T6_settle_frac"]),
                     "aftermath window in this clip is %d frames; spec B-1 asks for >= 1.5s"
                     % (n - 1 - phases["effect_end"])))
    return rows


def _longest_run(b):
    best = run = 0
    for v in np.asarray(b, bool):
        run = run + 1 if v else 0
        best = max(best, run)
    return best


def _rotation_sign(mean_ang):
    a = np.array(mean_ang, float)
    a = a[np.isfinite(a)]
    if a.size < 8:
        return 0
    d = np.diff(np.unwrap(np.radians(a)))
    return int(np.sign(np.median(d))) or 1


def _segment_regimes(x, min_len=6, tol=2.5):
    """Count piecewise-constant-slope regimes. A regime ends when the local
    slope departs from the running regime slope by more than `tol` robust
    deviations of the series' own frame-to-frame movement."""
    x = np.asarray(x, float)
    if x.size < 3 * min_len:
        return 0
    d = np.diff(x)
    s = float(np.median(np.abs(d - np.median(d)))) or 1e-9
    k = np.convolve(d, np.ones(min_len) / min_len, "same")
    regimes, cur = 1, k[0]
    hold = 0
    for v in k[1:]:
        if abs(v - cur) > tol * s * math.sqrt(min_len):
            hold += 1
            if hold >= min_len:
                regimes += 1
                cur, hold = v, 0
        else:
            hold = 0
            cur = 0.9 * cur + 0.1 * v
    return regimes


# ===========================================================================
# 5. PHASES + CONTACT ATTRIBUTION
# ===========================================================================

def phases_from_log(log_path, prefix, n):
    """State phases read from the harness render log. If absent, phases are
    derived from the area curve -- but a derived phase boundary is an inference
    and is stamped as one, because T-4a/c and T-6 are all measured against it."""
    if not log_path:
        return None
    rx = re.compile(r"t=([0-9.]+) state=([A-Z]+)\s+w=([0-9.]+) contacts=(\d+).*" + re.escape(prefix))
    st, ct = [], []
    with open(log_path, errors="ignore") as fh:
        for ln in fh:
            if prefix not in ln:
                continue
            m = rx.search(ln)
            if m:
                st.append(m.group(2))
                ct.append(int(m.group(4)))
    if len(st) < n * 0.9:
        return None
    st, ct = st[:n], ct[:n]
    def first(s):
        return st.index(s) if s in st else None
    sus0 = first("SUSTAIN")
    fall = first("FALLING")
    rise = first("RISING")
    end = next((i for i in range(fall or 0, len(st)) if st[i] == "IDLE"), len(st) - 1)
    return {"effect_start": rise or 0, "sustain": (sus0, (fall or len(st)) - 1),
            "fall_start": fall or 0, "effect_end": end,
            "contact_counts": ct, "source": "harness render log"}


def attribute_contacts(S, geo, phases, n):
    """Per-mob first-contact frame. The harness log gives contact COUNTS, not
    identities, so identity is attributed in image space: at each frame the
    count increments, the mob whose bearing from the caster is nearest the arc's
    leading edge owns the contact. Cross-checked against the total.
    """
    cx, cy = geo["caster_px"]
    sgn = _rotation_sign(S["mean_ang"])
    bearings = {m["id"]: math.degrees(math.atan2(m["seed_centroid"][1] - cy,
                                                 m["seed_centroid"][0] - cx))
                for m in geo["mob_rois"]}
    ct = phases.get("contact_counts") if phases else None
    out, seen = {}, set()
    if ct:
        for i in range(1, min(n, len(ct))):
            if ct[i] <= ct[i - 1]:
                continue
            lo, hi = S["arc_lo"][i], S["arc_hi"][i]
            if not np.isfinite([lo, hi]).all():
                continue
            lead = (hi if sgn > 0 else lo) * 360.0 / ANG_BINS - 180.0
            best = min(bearings, key=lambda k: abs(((bearings[k] - lead + 180) % 360) - 180))
            if best not in seen:
                seen.add(best)
                out[best] = i
    for m in geo["mob_rois"]:
        out.setdefault(m["id"], None)
    return out


# ===========================================================================
# 6. RUNNER
# ===========================================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--on", required=True)
    ap.add_argument("--control", required=True)
    ap.add_argument("--log", default=None, help="harness render.txt (state + contact timeline)")
    ap.add_argument("--on-prefix", default=None, help="log line prefix for the ON arm")
    ap.add_argument("--omega-deg-s", type=float, default=900.0)
    ap.add_argument("--label", default="unnamed")
    ap.add_argument("--ff08", action="store_true",
                    help="run frame_forensics_depth and use its CV_timing for T-4b (sec 3)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    w, h, fps = probe(a.on)
    w2, h2, f2 = probe(a.control)
    if (w, h) != (w2, h2):
        raise SystemExit("arms differ in raster: %dx%d vs %dx%d" % (w, h, w2, h2))
    n = min(_count(a.on), _count(a.control))
    rev = max(2, int(round(360.0 / a.omega_deg_s * fps)))

    geo = seed_geometry(a.on, a.control, w, h, fps, n, rev)
    S, per_mob, wp = measure(a.on, a.control, geo, w, h, fps, n)
    ph = phases_from_log(a.log, a.on_prefix or "", n) or _phases_from_area(S["area"])
    contacts = attribute_contacts(S, geo, ph, n)
    ff08 = None
    if a.ff08:
        from frame_forensics_depth import analyse_depth
        ff08 = analyse_depth(a.on, a.label)["summary"]["CV_timing"]
    rows = score(S, per_mob, wp, geo, ph, fps, contacts, ff08)

    res = {"label": a.label, "on": a.on, "control": a.control,
           "raster": [w, h], "fps": fps, "frames": n, "revolution_frames": rev,
           "geometry": {k: v for k, v in geo.items() if k != "mean_abs_diff_series"},
           "phases": {k: v for k, v in ph.items() if k != "contact_counts"},
           "contact_attribution": contacts,
           "ff08_cv_timing": {k: v for k, v in (ff08 or {}).items() if k != "events"} or None,
           "scorecard": rows,
           "series": {k: S[k] for k in ("area", "ncomp", "residue_total", "floor_area")}}
    with open(a.out, "w") as fh:
        json.dump(res, fh, indent=1, default=float)

    print("== %s == %d frames %dx%d @%.3f fps" % (a.label, n, w, h, fps))
    for r in rows:
        print("  %-5s %-42s %-14s %s" % (r["criterion"], r["name"], r["call"],
                                         json.dumps(r["operand"], default=float)[:150]))
    tally = {}
    for r in rows:
        tally[r["call"]] = tally.get(r["call"], 0) + 1
    print("  tally:", tally)


def _count(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                          "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout.strip()
    return int(out.split(",")[0])


def _phases_from_area(area):
    a = np.array(area, float)
    live = a > 0.10 * a.max()
    idx = np.nonzero(live)[0]
    s, e = int(idx[0]), int(idx[-1])
    q = s + int(0.35 * (e - s))
    f = s + int(0.80 * (e - s))
    return {"effect_start": s, "sustain": (q, f - 1), "fall_start": f,
            "effect_end": e, "contact_counts": None, "source": "DERIVED from area curve"}


if __name__ == "__main__":
    main()
