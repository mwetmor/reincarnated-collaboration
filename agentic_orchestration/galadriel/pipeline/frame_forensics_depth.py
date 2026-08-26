#!/usr/bin/env python3
"""
frame_forensics_depth.py -- the SEVEN depth-feature families + CV timing.

Run:      VFX-DEPTH RUN, wave W-E1 (galadriel, parallel non-godot arm)
Charter:  gandalf/notes/2026-08-25-vfx-depth-run-charter.md   (sec 4 core loop; R-8, R-10)
Author:   galadriel
Date:     2026-08-25

WHAT THIS ADDS to frame_forensics.py
    frame_forensics.py answers "how much transient content, how often, how many
    pieces, what colour, is the camera moving." It cannot answer any of the seven
    families the charter names. This module adds operators for:

      F1  hot white / bright LEADING HEAD
      F2  intensity gradient along length (hot head -> cool tail)
      F3  variable width along length
      F4  spark shedding (detached satellites with outward drift)
      F5  embedding in a smoke / dust volume
      F6  terrain response: (a) persistent scar   (b) impact-moment distortion flash
      F7  screen-shake / quake  (camera layer -- R-10)
      CV  timing irregularity, with the trip-flag rule

DESIGN LAW INHERITED FROM THE FIRST READING, AND IT IS NOT DECORATION
    (a) NOTHING HERE GRADES. Every operator emits a number and its own null /
        control reading beside it. A family reads PRESENT only where the measured
        value clears the control by a stated margin.
    (b) EVERY "ABSENT" IS SUSPECT UNTIL THE OPERATOR HAS A POSITIVE CONTROL.
        sec 2.3 of the first reading: a blind operator and an absent phenomenon
        produce the same reading. So this module ships `synth_controls()` and no
        ABSENT is reportable for a family whose control has not fired.
    (c) THE PLATE BLINDS EVERY MASK SERIES TO STEADY CONTENT (first reading
        sec 5.1). F5 (smoke) and F6a (scar) are the two families this blindness
        lands on hardest, and BOTH are therefore measured against a LONG-BASELINE
        plate rather than the +/-4-frame local plate. That is the whole reason
        this module keeps a decimated luma stack in memory.
    (d) R-10's TRIP-WIRE: a chartered shake must be MODELLED by the pan-null, not
        defeated by it. The affine camera fit ALREADY absorbs a shake into `tx/ty`
        exactly as it absorbs a pan -- which is precisely why the shake detector
        reads the fitted translation SERIES and looks for its high-frequency
        component, instead of looking for shake in the residual (where it is not).
"""

from __future__ import annotations

import json
import math
import subprocess
import sys

import numpy as np
from scipy import ndimage

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from frame_forensics import (  # noqa: E402
    REC709, luma, rgb_to_hsv, stream_frames, probe, local_plate,
    _flow_pass, n_eff, temporal_spectrum, peak_intervals, PLATE_HALFWIN,
)

SMALL = (320, 180)          # raster of the retained long-baseline luma stack
SCAR_LAG_S = 1.0            # how long after an impact a scar must still be there
HALO_K_LO = 2.0             # halo band lower edge, in noise_mad units
CORE_MIN_PX = 40            # below this the frame has no measurable structure


# ===========================================================================
# geometry helpers
# ===========================================================================

def principal_axis(ys, xs, wgt):
    """Weighted PCA of a point set. Returns (cx, cy, ax, ay, lam1, lam2)."""
    tot = float(wgt.sum())
    cx = float((wgt * xs).sum() / tot)
    cy = float((wgt * ys).sum() / tot)
    dx = xs - cx
    dy = ys - cy
    sxx = float((wgt * dx * dx).sum() / tot)
    syy = float((wgt * dy * dy).sum() / tot)
    sxy = float((wgt * dx * dy).sum() / tot)
    tr = sxx + syy
    det = sxx * syy - sxy * sxy
    disc = max(tr * tr / 4.0 - det, 0.0)
    lam1 = tr / 2.0 + math.sqrt(disc)
    lam2 = tr / 2.0 - math.sqrt(disc)
    if abs(sxy) > 1e-9:
        ax, ay = lam1 - syy, sxy
    else:
        ax, ay = (1.0, 0.0) if sxx >= syy else (0.0, 1.0)
    n = math.hypot(ax, ay) or 1.0
    return cx, cy, ax / n, ay / n, lam1, max(lam2, 0.0)


def weighted_slope(s, v, wgt):
    """Weighted least-squares slope of v on s. Returns nan on a degenerate s."""
    tot = float(wgt.sum())
    if tot <= 0:
        return float("nan")
    sm = float((wgt * s).sum() / tot)
    vm = float((wgt * v).sum() / tot)
    ss = float((wgt * (s - sm) ** 2).sum() / tot)
    if ss < 1e-9:
        return float("nan")
    sv = float((wgt * (s - sm) * (v - vm)).sum() / tot)
    return sv / ss


# ===========================================================================
# F1 / F2 / F3 -- head, gradient, width, on the dominant transient structure
# ===========================================================================

def shape_features(mask, adelta, val, sat, lead_vec):
    """Head / gradient / width on the LARGEST connected component of the mask.

    `lead_vec` is the camera-compensated displacement of the effect centroid
    since the previous frame. It is the ONLY thing that can tell a head from a
    tail: without a direction of travel, "leading" is not defined and the
    operator must refuse rather than pick an end. It refuses by returning
    lead_known=False and leaving every head/tail figure as nan.
    """
    lab, k = ndimage.label(mask)
    if k == 0:
        return None
    sizes = np.bincount(lab.ravel())[1:]
    core_id = int(np.argmax(sizes)) + 1
    core = (lab == core_id)
    if core.sum() < CORE_MIN_PX:
        return None

    ys, xs = np.nonzero(core)
    wgt = adelta[core].astype(np.float64)
    cx, cy, ax, ay, lam1, lam2 = principal_axis(ys, xs, wgt)

    s = (xs - cx) * ax + (ys - cy) * ay          # along the axis
    u = -(xs - cx) * ay + (ys - cy) * ax         # across it
    span = float(s.max() - s.min())
    out = {
        "core_px": int(core.sum()),
        "core_massfrac": float(wgt.sum() / max(adelta[mask].sum(), 1e-9)),
        "elongation": float(math.sqrt(lam1 / max(lam2, 1e-6))),
        "axis_span_px": span,
        "lead_known": False,
    }

    # ---- F3: variable width, measured as the profile of the perpendicular
    # extent in 8 bins along the axis. A primitive of constant thickness (a
    # ribbon, a bar, a smooth crescent of fixed stroke) reads cv_width near 0.
    if span > 8:
        edges = np.linspace(s.min(), s.max(), 9)
        widths = []
        for i in range(8):
            sel = (s >= edges[i]) & (s < edges[i + 1] if i < 7 else s <= edges[i + 1])
            if sel.sum() >= 3:
                widths.append(float(u[sel].max() - u[sel].min()))
            else:
                widths.append(float("nan"))
        wv = np.array(widths, dtype=np.float64)
        gw = np.isfinite(wv) & (wv > 0)
        out["width_profile"] = [None if not np.isfinite(x) else round(float(x), 2)
                                for x in wv]
        out["cv_width"] = (float(wv[gw].std() / wv[gw].mean())
                           if gw.sum() >= 4 and wv[gw].mean() > 0 else float("nan"))
    else:
        out["width_profile"] = None
        out["cv_width"] = float("nan")

    # ---- F1 / F2 need a direction of travel.
    lvx, lvy = lead_vec if lead_vec is not None else (float("nan"),) * 2
    if np.isfinite(lvx) and math.hypot(lvx, lvy) >= 0.75:
        sgn = 1.0 if (lvx * ax + lvy * ay) >= 0 else -1.0
        sl = s * sgn                              # +sl now points forward
        out["lead_known"] = True
        out["lead_speed_px"] = float(math.hypot(lvx, lvy))

        q = np.quantile(sl, [0.20, 0.80])
        head = sl >= q[1]
        tail = sl <= q[0]
        vh, vt = val[core][head], val[core][tail]
        sh, st = sat[core][head], sat[core][tail]
        wh, wt = wgt[head], wgt[tail]
        if head.sum() >= 8 and tail.sum() >= 8:
            out["head_val"] = float((wh * vh).sum() / wh.sum())
            out["tail_val"] = float((wt * vt).sum() / wt.sum())
            out["head_sat"] = float((wh * sh).sum() / wh.sum())
            out["tail_sat"] = float((wt * st).sum() / wt.sum())
            out["head_val_p95"] = float(np.quantile(vh, 0.95))
            # "hot WHITE": high value AND low saturation. Either alone is not it.
            out["head_white_frac"] = float(((vh > 0.80) & (sh < 0.30)).mean())
            out["tail_white_frac"] = float(((vt > 0.80) & (st < 0.30)).mean())
            out["head_tail_val_ratio"] = float(out["head_val"] /
                                               max(out["tail_val"], 1e-6))
            # F3 taper: is the head narrower or wider than the tail?
            if span > 8:
                hw = float(u[head].max() - u[head].min())
                tw = float(u[tail].max() - u[tail].min())
                out["head_tail_width_ratio"] = float(hw / max(tw, 1e-6))
        # ---- F2: gradient of value along the normalised axis. Negative slope =
        # bright at the head, dim at the tail, which is the charter's phrasing.
        sn = sl / max(span, 1e-6)
        out["val_slope_along_axis"] = weighted_slope(sn, val[core], wgt)
        out["sat_slope_along_axis"] = weighted_slope(sn, sat[core], wgt)
    return out


# ===========================================================================
# F1r / F2r -- the RADIAL variant of head and gradient
# ===========================================================================

def radial_shape_features(mask, adelta, val, sat):
    """Hot CORE vs cool PERIPHERY, for payloads that are bursts rather than streaks.

    ⚑ WHY THIS EXISTS. F1/F2 as first written ask "is the LEADING END of an
      elongated form hotter than the trailing end." That question is not merely
      unanswered for a meteor, a nova, an aura or a ground slam -- it is
      ILL-POSED, because those payloads have no leading end. The axis-conditioning
      gate correctly refuses them, but it refuses them with the SAME `n/e` it
      gives to a clip whose core is round only because scene contamination made
      it round. Two different causes, one indistinguishable output.

      Measured against that: at the D3 Meteor and D3 Hammer-of-the-Ancients
      impact frames the eye sees an unmistakable hot bright core with a cooler
      periphery, while the matrix says `n/e`. The instrument was not seeing an
      absence; it was asking the wrong question in the wrong coordinate.

    Same code path as shape_features, one coordinate changed: distance from the
    mass centroid instead of position along the principal axis. Requires NO
    direction of travel, so it is evaluable on stationary effects -- which is
    exactly the class the axial operator cannot reach.
    """
    lab, k = ndimage.label(mask)
    if k == 0:
        return None
    sizes = np.bincount(lab.ravel())[1:]
    core = (lab == int(np.argmax(sizes)) + 1)
    if core.sum() < CORE_MIN_PX:
        return None
    ys, xs = np.nonzero(core)
    wgt = adelta[core].astype(np.float64)
    tot = float(wgt.sum())
    cx = float((wgt * xs).sum() / tot)
    cy = float((wgt * ys).sum() / tot)
    r = np.hypot(xs - cx, ys - cy)
    rmax = float(r.max())
    if rmax < 4:
        return None
    rn = r / rmax
    q = np.quantile(rn, [0.20, 0.80])
    inner = rn <= q[0]
    outer = rn >= q[1]
    if inner.sum() < 8 or outer.sum() < 8:
        return None
    v, s_ = val[core], sat[core]
    wi, wo = wgt[inner], wgt[outer]
    return {
        "r_core_val": float((wi * v[inner]).sum() / wi.sum()),
        "r_edge_val": float((wo * v[outer]).sum() / wo.sum()),
        "r_core_sat": float((wi * s_[inner]).sum() / wi.sum()),
        "r_edge_sat": float((wo * s_[outer]).sum() / wo.sum()),
        # "hot WHITE core": bright AND desaturated, the same predicate F1 uses
        "r_core_white_frac": float(((v[inner] > 0.80) & (s_[inner] < 0.30)).mean()),
        "r_edge_white_frac": float(((v[outer] > 0.80) & (s_[outer] < 0.30)).mean()),
        # negative slope = bright at the centre, dim at the rim
        "r_val_slope": weighted_slope(rn, v, wgt),
        "r_sat_slope": weighted_slope(rn, s_, wgt),
        "r_extent_px": rmax,
    }


# ===========================================================================
# F4 -- spark shedding
# ===========================================================================

def satellite_features(mask, adelta):
    """Detached small components and how far out they sit.

    A spark is not merely 'a small bright thing'. It is a small bright thing
    that has SEPARATED. So the operator reports both the satellite mass share
    and the satellites' distance from the core, normalised by the core's own
    radius -- a fleck sitting on the core's shoulder is texture; a fleck at 3x
    the core radius has been shed.
    """
    lab, k = ndimage.label(mask)
    empty = {"sat_count": 0, "sat_massfrac": 0.0, "sat_mean_dist_norm": float("nan"),
             "sat_max_dist_norm": float("nan"), "n_components": int(k)}
    if k < 2:
        return empty
    sizes = np.bincount(lab.ravel())[1:].astype(np.float64)
    core_id = int(np.argmax(sizes)) + 1
    core_sz = sizes[core_id - 1]

    # ⚑ MIN_SPARK_PX, added after the control run and after the run STALLED.
    # Two defects, one cause. (i) The F4 control read 1,141 "satellites" on the
    # scar clip, which contains no sparks at all -- single-pixel speckle from
    # background texture crossing tau was being counted as shed material, and
    # `sat_count` was measuring compression noise. (ii) `center_of_mass` was
    # being asked for EVERY component; on a busy reference frame that is tens of
    # thousands of labels and the run did not finish a single clip in ten
    # minutes. A 1-px bright dot at 720p is not a distinguishable spark under
    # any decode this corpus contains, so requiring 4 px both cleans the
    # descriptor and bounds the cost. The cap is a SECOND bound, reported.
    MIN_SPARK_PX = 4
    SAT_CAP = 400
    idx = np.arange(1, k + 1)
    small = idx[(idx != core_id) & (sizes <= 0.05 * core_sz)
                & (sizes >= MIN_SPARK_PX)]
    if small.size == 0:
        return empty
    capped = bool(small.size > SAT_CAP)
    if capped:
        small = small[np.argsort(-sizes[small - 1])[:SAT_CAP]]
    coms = ndimage.center_of_mass(mask, lab, list(map(int, [core_id, *small])))
    cy, cx = coms[0]
    core_r = math.sqrt(core_sz / math.pi)
    d = np.array([math.hypot(c[1] - cx, c[0] - cy) for c in coms[1:]]) / max(core_r, 1.0)
    return {
        "sat_count": int(small.size),
        "sat_massfrac": float(sizes[small - 1].sum() / sizes.sum()),
        "sat_mean_dist_norm": float(np.mean(d)),
        "sat_max_dist_norm": float(np.max(d)),
        "n_components": int(k),
        "sat_capped": capped,
        "min_spark_px": MIN_SPARK_PX,
    }


# ===========================================================================
# F5 -- smoke / dust volume embedding
# ===========================================================================

def halo_features(hard, adelta, sat, val, noise_mad):
    """The LOW-amplitude band around the hard mask.

    Smoke is defined here operationally as: content that is (i) above the noise
    floor but well below the effect's own novelty bar, (ii) spatially CONTIGUOUS
    with the effect, (iii) desaturated, and (iv) SOFT -- low gradient energy per
    unit area relative to the core. Property (iv) is what separates a smoke
    volume from a swarm of dim sparks, and without it the operator would call
    every faint speck field a smoke plume.
    """
    lo = HALO_K_LO * max(noise_mad, 0.5)
    hi = 6.0 * max(noise_mad, 0.5)
    band = (adelta >= lo) & (adelta < hi)
    if not hard.any():
        return {"halo_area_ratio": float("nan"), "halo_sat": float("nan"),
                "halo_adjacent_frac": float("nan"), "halo_softness": float("nan")}
    # distance transform rather than 12 binary_dilation iterations: identical
    # result, one pass instead of twelve, and the run has 25 clips to get through
    near = ndimage.distance_transform_edt(~hard) <= 12
    halo = band & near & (~hard)
    if halo.sum() < 32:
        return {"halo_area_ratio": float(halo.sum() / max(hard.sum(), 1)),
                "halo_sat": float("nan"), "halo_adjacent_frac": float("nan"),
                "halo_softness": float("nan")}
    gy, gx = np.gradient(adelta)
    gmag = np.hypot(gx, gy)
    core_g = float(gmag[hard].mean()) if hard.any() else float("nan")
    halo_g = float(gmag[halo].mean())
    return {
        "halo_area_ratio": float(halo.sum() / max(hard.sum(), 1)),
        "halo_sat": float(sat[halo].mean()),
        "halo_val": float(val[halo].mean()),
        "halo_adjacent_frac": float(halo.sum() / max(band.sum(), 1)),
        # >1 means the halo is SOFTER than the core, which is the smoke signature
        "halo_softness": float(core_g / max(halo_g, 1e-6)),
    }


# ===========================================================================
# F6a -- persistent terrain scar, on a LONG baseline
# ===========================================================================

def scar_series(small_stack, shifts, impact_idx, fps, noise_mad,
                lag_s=SCAR_LAG_S, small_wh=SMALL):
    """Does the ground still differ from its pre-event self, a second later?

    ⚑ THIS CANNOT BE DONE ON THE LOCAL PLATE AND THAT IS THE POINT. A persistent
      scar is, by construction, STEADY -- so within a few frames it becomes part
      of the +/-4-frame plate and every mask-based series goes blind to it
      (first reading sec 5.1). The only way to see it is to compare against a
      baseline from BEFORE the event, motion-compensated over ~30-60 frames.

    Compensation is integer-shift only, so the figure carries sub-pixel
    registration error; that error is charged against the operator by measuring
    the SAME quantity at a control lag on a pre-event pair, and reporting both.
    """
    sw, sh = small_wh
    n = len(small_stack)
    lag = int(round(lag_s * fps))
    pre_i = impact_idx - int(round(0.35 * fps))
    post_i = impact_idx + lag
    if pre_i < 2 or post_i >= n:
        return None
    sx = sw / 1280.0

    def diff(i, j):
        dx = int(round((shifts[j][0] - shifts[i][0]) * sx))
        dy = int(round((shifts[j][1] - shifts[i][1]) * sx))
        a = small_stack[i]
        b = np.roll(np.roll(small_stack[j], -dy, axis=0), -dx, axis=1)
        v = max(abs(dx), 1), max(abs(dy), 1)
        c = np.abs(a - b)[v[1]:sh - v[1], v[0]:sw - v[0]]
        return c

    d_post = diff(pre_i, post_i)
    ctrl_j = pre_i - lag
    if ctrl_j < 0:
        return None
    d_ctrl = diff(ctrl_j, pre_i)
    tau = 6.0 * max(noise_mad, 0.5)
    return {
        "impact_idx": int(impact_idx),
        "scar_frac": float((d_post >= tau).mean()),
        "control_frac": float((d_ctrl >= tau).mean()),
        "scar_over_control": float((d_post >= tau).mean() /
                                   max((d_ctrl >= tau).mean(), 1e-6)),
        "lag_s": lag_s,
    }


# ===========================================================================
# F7 -- screen shake, from the fitted camera translation series
# ===========================================================================

def shake_features(tx, ty, div, fps, med_win=9):
    """Shake = the HIGH-FREQUENCY component of the fitted camera translation.

    ⚑ R-10 trip-wire, discharged by construction. A pan and a shake both land in
      the affine fit's `tx/ty` -- so looking for shake in the RESIDUAL (where the
      pan-null looked) would find nothing, and would find nothing whether or not
      a shake was there. The separation is not pan-vs-residual, it is SMOOTH-vs-
      IMPULSIVE within the same translation series. A pan is a low-frequency
      ramp; an impact shake is a spike with a short decay. A running median is
      the smoothing kernel because it is the one that a spike does NOT drag.
    """
    tx = np.asarray(tx, float)
    ty = np.asarray(ty, float)
    g = np.isfinite(tx) & np.isfinite(ty)
    if g.sum() < 24:
        return None
    tx, ty = tx[g], ty[g]
    sm_x = ndimage.median_filter(tx, size=med_win, mode="nearest")
    sm_y = ndimage.median_filter(ty, size=med_win, mode="nearest")
    hx, hy = tx - sm_x, ty - sm_y
    hp = np.hypot(hx, hy)
    base = float(np.median(hp))
    mad = float(np.median(np.abs(hp - base))) or 1e-9
    # ⚑ ABSOLUTE FLOOR, added after the control run. On a byte-stable clip the
    # high-frequency MAD collapses to ~0, so a derived-only bar becomes 0.000 and
    # EVERY nonzero frame counts as a shake event -- the detector would report
    # shake on a still camera. Half a pixel of camera displacement is not a
    # quake at any raster we work at, so the bar is floored there. The derived
    # term still governs whenever the clip has real camera noise.
    #
    # ⚑ RULED 2026-08-25 (galadriel) on drax's G-5 flag -- his six camnull legs
    # returned shake_bar_px == 0.5000 on ALL SIX, i.e. entirely floor-governed,
    # with N3-high at 88% of the bar. Ruling, in four clauses:
    #   1. The VALUE STANDS at 0.5. Downward is refuted (mad collapsed to the
    #      1e-9 fallback on 7/7 measured legs); upward is unsupported by any
    #      datum, since nothing on the ladder crossed it.
    #   2. Its ROLE is a DEGENERACY GUARD, not a parallax-rejection bar, and it
    #      now says so in the output rather than leaving it to be inferred from
    #      behaviour. `bar_is_floor_governed` reports when the guard is acting
    #      as the operative bar -- a job no measurement gave it.
    #   3. Its DOMAIN is relief- and speed-conditional. The ladder validates
    #      relief <= 10 m and pan <= ~4.6 px/frame; the residual roughly doubles
    #      per relief rung (0.097/0.126/0.232/0.423), so 88% is about one rung
    #      of headroom. OUTSIDE the envelope F7 reports INDETERMINATE, never
    #      ABSENT (#63: an unmeasured zero must not wear a verdict).
    #   4. `hf_to_pan_ratio` is PROMOTED to primary discriminant -- see below.
    bar = max(base + 6.0 * mad, 0.5)
    floor_governed = bool(base + 6.0 * mad <= 0.5)
    spikes = np.nonzero(hp >= bar)[0]
    dv = np.asarray(div, float)
    dv = dv[np.isfinite(dv)]
    out = {
        "pan_mean_px": float(np.hypot(sm_x, sm_y).mean()),
        "hf_median_px": base,
        "hf_mad_px": mad,
        "hf_p99_px": float(np.quantile(hp, 0.99)),
        "hf_max_px": float(hp.max()),
        "shake_bar_px": float(bar),
        "shake_bar_role": "DEGENERACY GUARD (clause 2); corroborating, not primary",
        "bar_is_floor_governed": floor_governed,
        "n_shake_frames": int(len(spikes)),
        "shake_frame_frac": float(len(spikes) / len(hp)),
        "hf_to_pan_ratio": float(np.quantile(hp, 0.99) /
                                 max(np.hypot(sm_x, sm_y).mean(), 1e-6)),
    }
    # ⚑ CLAUSE 4 -- PRIMARY F7 DISCRIMINANT. The absolute residual is a function
    # of whatever pan rate a clip happens to have, and the G-5 ladder swept ONE
    # speed; so an absolute-px bar cannot travel to a reference clip with its own
    # camera speed and its own pose. This ratio is dimensionless in pan rate and
    # therefore does travel. Bar MEASURED, not chosen:
    #   nulls  0.026 0.034 0.060 0.076 0.093 (G-5 ladder) + 0.095 (cathedral
    #          static-cam, galadriel's 7th null, 2026-08-25)
    #   P1-shake, 3.0 px authored                                        1.034
    # Empty band 0.095 -> 1.034 with nothing in it; geometric centre 0.313.
    # Bar 0.30 = 3.2x above the loudest null, 3.4x below the positive.
    # ⚑ PROVISIONAL ON THE POSITIVE SIDE: n = 1 amplitude, at 6x the floor.
    #   Sensitivity between 0.5 px and 3.0 px authored is UNMEASURED.
    # ⚑ ENVELOPE (clause 3): validated for pan <= 4.6 px/frame at player_lock
    #   k=0.665 with relief <= 10 m. Outside it, INDETERMINATE, never ABSENT.
    out["f7_primary_bar"] = 0.30
    out["f7_call"] = ("PRESENT" if out["hf_to_pan_ratio"] >= 0.30 else
                      ("ABSENT" if out["pan_mean_px"] <= 4.6 else "INDETERMINATE"))
    out["f7_envelope"] = {"validated_pan_px_per_frame_max": 4.6,
                          "validated_relief_m_max": 10.0,
                          "validated_pose": "player_lock k=0.665",
                          "pose_transfer": "CONDITIONAL -- re-render the null near "
                                           "the reference pose before transferring"}
    if dv.size:
        dmed = float(np.median(dv))
        dmad = float(np.median(np.abs(dv - dmed))) or 1e-9
        out["div_median"] = dmed
        out["div_max_z"] = float(np.abs(dv - dmed).max() / dmad)
    return out


# ===========================================================================
# THE RUN
# ===========================================================================

def analyse_depth(path, label, w=1280, h=720, fps=30.0, grid=8):
    meta = probe(path)
    meta.update({"label": label, "analysis_w": w, "analysis_h": h,
                 "analysis_fps": fps, "tile_grid": grid})
    models, resids, oks, centres, shifts = _flow_pass(path, w, h, fps, grid)
    nframes = len(models)
    meta["n_frames_analysed"] = nframes

    # ---- pass 1: derive the noise floor exactly as frame_forensics does, and
    # simultaneously retain the decimated luma stack F6a needs.
    ring, ringsh, delta_meds, plate_samples = [], [], [], []
    small_stack = []
    for i, frame in enumerate(stream_frames(path, w, h, fps)):
        L = luma(frame)
        small_stack.append(np.asarray(
            L[:(h // SMALL[1]) * SMALL[1], :(w // SMALL[0]) * SMALL[0]]
            .reshape(SMALL[1], h // SMALL[1], SMALL[0], w // SMALL[0])
            .mean(axis=(1, 3)), dtype=np.float32))
        ring.append(L); ringsh.append(shifts[i])
        if len(ring) > 2 * PLATE_HALFWIN + 1:
            ring.pop(0); ringsh.pop(0)
        if len(ring) == 2 * PLATE_HALFWIN + 1 and (i % 6 == 0):
            pl = local_plate(ring, ringsh, PLATE_HALFWIN)
            delta_meds.append(float(np.median(np.abs(ring[PLATE_HALFWIN] - pl))))
            plate_samples.append(pl[::4, ::4].copy())
    noise_mad = float(np.median(delta_meds)) if delta_meds else 1.0
    plate_pool = (np.concatenate([p.ravel() for p in plate_samples])
                  if plate_samples else np.array([0.0]))
    tau_novelty = 6.0 * max(noise_mad, 0.5)
    tau_spec = float(np.quantile(plate_pool, 0.9995))
    derived = {"noise_mad_luma": noise_mad, "tau_novelty": tau_novelty,
               "tau_spec": tau_spec}

    # ---- pass 2
    S = {k: [] for k in (
        "t", "idx", "novel_frac", "spec_mass", "core_px", "elongation",
        "cv_width", "head_tail_val_ratio", "head_white_frac", "tail_white_frac",
        "head_sat", "tail_sat", "val_slope_along_axis", "head_tail_width_ratio",
        "sat_count", "sat_massfrac", "sat_mean_dist_norm",
        "halo_area_ratio", "halo_sat", "halo_softness",
        "cam_tx", "cam_ty", "cam_div", "radial_coh_near", "radial_coh_far",
        "resid_near", "resid_bg", "lead_known", "centroid_x", "centroid_y",
        "r_core_white_frac", "r_edge_white_frac", "r_val_slope", "r_sat_slope",
        "r_core_sat", "r_edge_sat")}

    ring, ringsh, idxs = [], [], []
    prev_cen = None
    for i, frame in enumerate(stream_frames(path, w, h, fps)):
        ring.append((frame.copy(), luma(frame)))
        ringsh.append(shifts[i]); idxs.append(i)
        if len(ring) > 2 * PLATE_HALFWIN + 1:
            ring.pop(0); ringsh.pop(0); idxs.pop(0)
        if len(ring) < 2 * PLATE_HALFWIN + 1:
            continue
        c = PLATE_HALFWIN
        ci = idxs[c]
        cf, L = ring[c]
        pl = local_plate([lu for (_, lu) in ring], ringsh, c)
        adelta = np.abs(L - pl)
        m = adelta >= tau_novelty
        hh, ss, vv = rgb_to_hsv(cf)

        S["t"].append(ci / fps); S["idx"].append(ci)
        S["novel_frac"].append(float(m.mean()))
        spec = L >= tau_spec
        S["spec_mass"].append(float(np.clip(L[spec] - tau_spec, 0, None).sum()
                                    / L.size) if spec.any() else 0.0)

        # camera-compensated centroid motion -> the lead vector for F1/F2
        if m.any():
            ys, xs = np.nonzero(m)
            cen = (float(xs.mean()), float(ys.mean()))
        else:
            cen = (float("nan"), float("nan"))
        S["centroid_x"].append(cen[0]); S["centroid_y"].append(cen[1])
        lead = None
        if prev_cen is not None and np.isfinite(cen[0]) and np.isfinite(prev_cen[0]):
            mdl_prev = models[ci] if ci < len(models) else None
            ctx = mdl_prev["tx"] if mdl_prev else 0.0
            cty = mdl_prev["ty"] if mdl_prev else 0.0
            lead = (cen[0] - prev_cen[0] + ctx, cen[1] - prev_cen[1] + cty)
        prev_cen = cen

        sh = shape_features(m, adelta, vv, ss, lead) if m.any() else None
        if sh:
            for k in ("core_px", "elongation", "cv_width", "head_tail_val_ratio",
                      "head_white_frac", "tail_white_frac", "head_sat",
                      "tail_sat", "val_slope_along_axis",
                      "head_tail_width_ratio"):
                S[k].append(sh.get(k, float("nan")))
            S["lead_known"].append(bool(sh.get("lead_known", False)))
        else:
            for k in ("core_px", "elongation", "cv_width", "head_tail_val_ratio",
                      "head_white_frac", "tail_white_frac", "head_sat",
                      "tail_sat", "val_slope_along_axis",
                      "head_tail_width_ratio"):
                S[k].append(float("nan"))
            S["lead_known"].append(False)

        rs = radial_shape_features(m, adelta, vv, ss) if m.any() else None
        for k in ("r_core_white_frac", "r_edge_white_frac", "r_val_slope",
                  "r_sat_slope", "r_core_sat", "r_edge_sat"):
            S[k].append(rs.get(k, float("nan")) if rs else float("nan"))

        sat = satellite_features(m, adelta) if m.any() else None
        for k in ("sat_count", "sat_massfrac", "sat_mean_dist_norm"):
            S[k].append(sat[k] if sat else float("nan"))

        hal = halo_features(m, adelta, ss, vv, noise_mad) if m.any() else None
        for k in ("halo_area_ratio", "halo_sat", "halo_softness"):
            S[k].append(hal[k] if hal else float("nan"))

        mdl, rr, ok = models[ci], resids[ci], oks[ci]
        if mdl is None or rr is None or centres is None:
            for k in ("cam_tx", "cam_ty", "cam_div", "radial_coh_near",
                      "radial_coh_far", "resid_near", "resid_bg"):
                S[k].append(float("nan"))
        else:
            rx, ry = rr
            rmag = np.hypot(rx, ry)
            ex, ey = (cen if np.isfinite(cen[0]) else (w / 2.0, h / 2.0))
            d = np.hypot(centres[:, 0] - ex, centres[:, 1] - ey)
            diag = float(np.hypot(w, h))
            near = ok & (d <= 0.20 * diag)
            far = ok & (d > 0.35 * diag)
            S["cam_tx"].append(mdl["tx"]); S["cam_ty"].append(mdl["ty"])
            S["cam_div"].append(mdl["divergence"])
            S["resid_near"].append(float(np.nanmedian(rmag[near]))
                                   if near.sum() else float("nan"))
            S["resid_bg"].append(float(np.nanmedian(rmag[far]))
                                 if far.sum() else float("nan"))

            def _radial(sel):
                if sel.sum() < 4:
                    return float("nan")
                vx, vy = rx[sel], ry[sel]
                px = centres[sel, 0] - ex
                py = centres[sel, 1] - ey
                rn = np.hypot(px, py); vn = np.hypot(vx, vy)
                gg = (rn > 1e-6) & (vn > 1e-6) & np.isfinite(vn)
                if gg.sum() < 4:
                    return float("nan")
                return float(np.mean((vx[gg] * px[gg] + vy[gg] * py[gg])
                                     / (rn[gg] * vn[gg])))
            S["radial_coh_near"].append(_radial(near))
            S["radial_coh_far"].append(_radial(far))

    # ---- derived summaries -------------------------------------------------
    def q(key, p):
        a = np.asarray(S[key], float)
        a = a[np.isfinite(a)]
        return float(np.quantile(a, p)) if a.size else float("nan")

    spec = np.asarray(S["spec_mass"], float)
    ev = peak_intervals(spec, fps)
    sp = temporal_spectrum(spec, fps)

    # F6b: the IMPACT-MOMENT distortion flash. R-8's amendment, and it is
    # measured ONLY at impact frames -- a whole-clip average washes a 3-frame
    # flash out entirely, which is exactly what the -0.023 whirlwind figure did.
    rn = np.asarray(S["radial_coh_near"], float)
    rf = np.asarray(S["radial_coh_far"], float)
    rrn = np.asarray(S["resid_near"], float)
    impact_idx = int(np.nanargmax(spec)) if np.isfinite(spec).any() else 0
    win = slice(max(impact_idx - 3, 0), min(impact_idx + 4, len(rn)))
    def _absmax(a):
        a = a[np.isfinite(a)]
        return float(np.abs(a).max()) if a.size else float("nan")
    impact = {
        "impact_frame_idx": int(S["idx"][impact_idx]) if S["idx"] else None,
        "impact_t_s": float(S["t"][impact_idx]) if S["t"] else None,
        "radial_near_at_impact": _absmax(rn[win]),
        "radial_far_at_impact": _absmax(rf[win]),
        "radial_near_clip_absmax": _absmax(rn),
        "radial_near_clip_median": float(np.nanmedian(rn)) if np.isfinite(rn).any() else float("nan"),
        "resid_near_at_impact": float(np.nanmax(rrn[win])) if np.isfinite(rrn[win]).any() else float("nan"),
        "resid_near_clip_median": float(np.nanmedian(rrn)) if np.isfinite(rrn).any() else float("nan"),
        "validated_lens_signature": [0.51, 0.99],
    }

    scar = scar_series(small_stack, shifts, S["idx"][impact_idx] if S["idx"] else 0,
                       fps, noise_mad)
    shake = shake_features(S["cam_tx"], S["cam_ty"], S["cam_div"], fps)

    summary = {
        "F1_head": {
            "head_tail_val_ratio_p90": q("head_tail_val_ratio", 0.90),
            "head_tail_val_ratio_med": q("head_tail_val_ratio", 0.50),
            "head_white_frac_p90": q("head_white_frac", 0.90),
            "tail_white_frac_p90": q("tail_white_frac", 0.90),
            "lead_known_frac": float(np.mean(S["lead_known"])) if S["lead_known"] else 0.0,
        },
        "F2_gradient": {
            "val_slope_med": q("val_slope_along_axis", 0.50),
            "val_slope_p10": q("val_slope_along_axis", 0.10),
            "val_slope_p90": q("val_slope_along_axis", 0.90),
            "head_sat_med": q("head_sat", 0.50),
            "tail_sat_med": q("tail_sat", 0.50),
        },
        "F3_width": {
            "cv_width_med": q("cv_width", 0.50),
            "cv_width_p90": q("cv_width", 0.90),
            "head_tail_width_ratio_med": q("head_tail_width_ratio", 0.50),
            "elongation_med": q("elongation", 0.50),
        },
        "F1r_radial_core": {
            "core_white_frac_p90": q("r_core_white_frac", 0.90),
            "edge_white_frac_p90": q("r_edge_white_frac", 0.90),
            "val_slope_med": q("r_val_slope", 0.50),
            "sat_slope_med": q("r_sat_slope", 0.50),
            "core_sat_med": q("r_core_sat", 0.50),
            "edge_sat_med": q("r_edge_sat", 0.50),
        },
        "F4_sparks": {
            "sat_count_med": q("sat_count", 0.50),
            "sat_count_p90": q("sat_count", 0.90),
            "sat_massfrac_p90": q("sat_massfrac", 0.90),
            "sat_dist_norm_p90": q("sat_mean_dist_norm", 0.90),
        },
        "F5_smoke": {
            "halo_area_ratio_med": q("halo_area_ratio", 0.50),
            "halo_area_ratio_p90": q("halo_area_ratio", 0.90),
            "halo_sat_med": q("halo_sat", 0.50),
            "halo_softness_med": q("halo_softness", 0.50),
        },
        "F6a_scar": scar,
        "F6b_impact_distortion": impact,
        "F7_shake": shake,
        # ⚑ TRIP LAW AMENDED 2026-08-25 at registry ratification (jack-ryan,
        # qa/findings/2026-08-25-vfx-registry-ratification.md sec 1(b)).
        # WAS: CV < 0.25 AND dominant tone > 1000x median -- a CONJUNCT.
        # NOW: CV < 0.25 TRIPS ALONE. The spectral tone is DEMOTED to a recorded
        # diagnostic. The conjunct never once added a trip across the measured
        # matrix; its entire observed effect was to suppress two calls
        # (OURS_blink at 945x, OURS_teleport at 473x) that this instrument's own
        # operator then made by hand. A condition whose only effect is to veto
        # its owner's correct calls is not a gate.
        #
        # ⚑ MINIMUM-INTERVAL RULE, set here by galadriel per the ratification's
        # explicit remit ("the threshold itself is galadriel's to set"). Derived,
        # not chosen: SE(CV)/CV ~ 1/sqrt(2n). To separate the 0.25 bar from the
        # reference corpus floor of 0.449 at 2 sigma needs relative SE <=
        # (0.449-0.25)/2/0.449 = 0.222, hence n >= 10 intervals. Below that the
        # row is INDETERMINATE and is NEVER a PASS (Discipline #63). Recorded
        # consequence: OURS_ground_slam's six events fall below this line, which
        # is consistent with its having been inspected rather than passed.
        "CV_timing": {
            "events": ev, "spectrum": sp,
            "n_intervals": max(0, int(ev.get("n_events") or 0) - 1),
            "min_intervals_rule": 10,
            "indeterminate": bool(max(0, int(ev.get("n_events") or 0) - 1) < 10
                                  or ev.get("cv_interval") is None),
            "trip_flag": bool(ev.get("cv_interval") is not None
                              and max(0, int(ev.get("n_events") or 0) - 1) >= 10
                              and ev["cv_interval"] < 0.25),
            "spectral_tone_diagnostic": (None if sp is None
                                         else sp.get("peak_over_median")),
            "trip_law": "CV < 0.25 SOLE-TRIP; tone diagnostic only; "
                        "n_intervals < 10 -> INDETERMINATE",
        },
    }
    return {"meta": meta, "derived": derived, "summary": summary, "series": S}


# ===========================================================================
# SYNTHETIC POSITIVE CONTROLS -- no ABSENT is reportable without these
# ===========================================================================

def _write_synth(path, frames, fps=30):
    h, w = frames[0].shape[:2]
    p = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for f in frames:
        p.stdin.write(f.astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()


def synth_controls(outdir, w=1280, h=720, n=120, fps=30):
    """Four synthetics with known ground truth, written to outdir.

    comet   -- bright WHITE head, cooling saturated tail, tapering width, sparks
    bar     -- constant-width, constant-intensity travelling bar (the NULL for
               F1/F2/F3/F4): a smooth primitive, which is precisely what our own
               clean-room whirlwind was measured to be
    smoke   -- the bar, embedded in a soft desaturated volume (F5 positive)
    shake   -- a STATIC scene with an impulse-decay camera displacement at frame
               60 (F7 positive), plus a smooth pan (F7 null)
    """
    import os
    os.makedirs(outdir, exist_ok=True)
    rng = np.random.default_rng(11)
    bg = (rng.normal(40, 9, (h, w, 3))).clip(0, 90)
    # give the background real texture so phase correlation is evaluable
    for _ in range(400):
        cy, cx = rng.integers(0, h), rng.integers(0, w)
        r = int(rng.integers(6, 40))
        yy, xx = np.ogrid[:h, :w]
        d = (yy - cy) ** 2 + (xx - cx) ** 2 <= r * r
        bg[d] += rng.normal(0, 22, 3)
    bg = bg.clip(0, 120)
    yy, xx = np.mgrid[0:h, 0:w]

    def comet_frame(cx, cy, taper, sparks, smoke=False):
        f = bg.copy()
        L = 220.0
        for k in range(60):
            t = k / 59.0
            px = cx - t * L
            rad = (3.0 + 16.0 * t) if taper else 9.0
            d2 = (xx - px) ** 2 + (yy - cy) ** 2
            g = np.exp(-d2 / (2 * rad * rad))
            if taper:
                inten = 255.0 * (1.0 - t) ** 1.6
                col = np.array([1.0, 1.0 - 0.75 * t, 1.0 - 0.95 * t])
            else:
                inten = 190.0
                col = np.array([1.0, 0.55, 0.15])
            for c in range(3):
                f[..., c] += inten * col[c] * g
        if sparks:
            for _ in range(26):
                a = rng.uniform(0, 2 * np.pi)
                r = rng.uniform(30, 150)
                sx, sy = cx - rng.uniform(0, 190) + r * np.cos(a) * 0.3, cy + r * np.sin(a)
                d2 = (xx - sx) ** 2 + (yy - sy) ** 2
                f += (235.0 * np.exp(-d2 / 6.0))[..., None]
        if smoke:
            d2 = (xx - (cx - 110)) ** 2 + ((yy - cy) * 1.7) ** 2
            f += (26.0 * np.exp(-d2 / (2 * 105.0 ** 2)))[..., None]
        return f.clip(0, 255)

    for name, taper, sparks, smoke in (("comet", True, True, False),
                                       ("bar", False, False, False),
                                       ("smoke", False, False, True)):
        fr = [comet_frame(180 + 7.0 * i, h // 2, taper, sparks, smoke)
              for i in range(n)]
        _write_synth(f"{outdir}/synth_{name}.mp4", fr, fps)

    # F7: static + impulse shake, and a smooth pan as the null
    base = bg.copy()
    for _ in range(300):
        cy, cx = rng.integers(0, h), rng.integers(0, w)
        r = int(rng.integers(3, 18))
        d = (yy - cy) ** 2 + (xx - cx) ** 2 <= r * r
        base[d] += rng.normal(0, 30, 3)
    base = base.clip(0, 255)
    shake_fr, pan_fr = [], []
    for i in range(n):
        k = i - 60
        amp = 14.0 * math.exp(-max(k, 0) / 4.0) if k >= 0 else 0.0
        dx = int(round(amp * math.cos(2.4 * k))) if k >= 0 else 0
        dy = int(round(amp * math.sin(3.1 * k))) if k >= 0 else 0
        shake_fr.append(np.roll(np.roll(base, dy, 0), dx, 1))
        pan_fr.append(np.roll(base, int(round(6.0 * i)), 1))
    _write_synth(f"{outdir}/synth_shake.mp4", shake_fr, fps)
    _write_synth(f"{outdir}/synth_pan.mp4", pan_fr, fps)
    return [f"{outdir}/synth_{k}.mp4"
            for k in ("comet", "bar", "smoke", "shake", "pan")]


if __name__ == "__main__":
    out = analyse_depth(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "clip")
    print(json.dumps(out["summary"], indent=2, default=str))
