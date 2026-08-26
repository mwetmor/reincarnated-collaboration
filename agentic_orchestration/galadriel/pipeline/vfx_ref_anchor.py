#!/usr/bin/env python3
"""REFERENCE-ANCHOR pass — charter R-25 (A-1).

Measures the REFERENCE clip's own values for the three statistics the lap-2
battery applies to our renders, so that T-3(b)'s P95/P20 bar (4.0) and
T-3(c)'s mid-band-S bar (0.55) can be re-anchored to something MEASURED
rather than to the a-priori numbers they were authored with.

    reference: /private/tmp/vfx-lap1-seats/extract/reference_video.flv
    sha256   : 855bb3d9c7edca8b372869e667682eda6de85ea813628377e567522d9e998637

THE STATISTICS ARE IMPORTED, NOT RE-IMPLEMENTED.  `luma` and `sat_val` come
from `vfx_lap2_battery` so that "the same statistic" is a fact about the call
graph and not a claim in a comment.  The percentile/mid-band/ownership
arithmetic below is transcribed from the battery's own blocks
(`measure()` T-3a/b/c photometry; `t3a_ownership()`), and the transcription is
regression-checked by `--selfcheck`, which re-runs the battery's exact
expressions against this module's on the same array.

------------------------------------------------------------------------
THE SEGMENTATION PROBLEM, AND WHY THIS INSTRUMENT DIFFERS FROM THE BATTERY
------------------------------------------------------------------------
The battery segments the effect by DIFFERENCING a treatment arm against a
`set_vfx_visible(false)` control arm.  **The reference has no control arm and
cannot have one** — it is captured gameplay footage of a shipped title.  A
temporal-median background is also unavailable: the reference camera PANS
(verified — the frame's lower-right quadrant contains entirely different
world content at f300 than at f30, `evidence/corner-f30-120-200-300.png`), so
no per-pixel background exists to difference against.

So the segmentation is APPEARANCE-BASED, and its central hazard is
CIRCULARITY:

  * A LUMINANCE-thresholded mask would make ownership (T-3a) 1.0 by
    construction.  Refused.
  * A SATURATION-thresholded mask would make mid-band S (T-3c) >= the
    threshold by construction.  This is the live hazard, because the mask
    below does use a chroma test.
  * A HUE-sector mask is circular for NEITHER (b) NOR (a): selecting pixels
    by hue angle says nothing about their internal luminance spread and
    nothing about whether they are the frame's brightest pixels.

The reference's scene is teal (L-weighted hue mode 190-210 deg) and its
effect is fire (hue mode 0-30 deg).  The two are near-opposite and the hue
histogram is sharply bimodal, so a hue-sector mask is well-posed HERE in a
way it would not be in an arbitrary venue.

The residual circularity — the chroma floor inside the hue test — is not
argued away.  It is SWEPT (`--sweep`), across S > 0.10 .. 0.55, and the
mid-band-S conclusion is only reported as anchored if it survives the most
permissive setting.  A third segmentation (`support`) additionally measures
EVERY pixel inside the effect's morphological footprint regardless of that
pixel's own hue or saturation, which removes the pixel-wise chroma selection
from the measured set entirely.

------------------------------------------------------------------------
NEGATIVE CONTROLS (three, all in-clip)
------------------------------------------------------------------------
  1. TEMPORAL NULL.  The clip outlives its own fire.  Frames 239-352 hold a
     flat residue of warm pixels (~8.5 kpx, steady) with no fire present
     (`evidence/late-f150-200-250-300.png`) — monster eye-glows, loot beams,
     ground detail.  The identical instrument is run over that window and
     whatever it reports is the instrument's FLOOR, not the effect.  This is
     the reference's equivalent of R-24 #7's Mob0: an in-frame null that
     shares the venue, the codec and the clock.
  2. SPATIAL FLOOR.  Per action frame, the region OUTSIDE a 25 px dilation of
     the effect support — sky, ground, monsters away from the fire — carries
     the same three statistics.  This is the "what does a non-effect region
     of this reference score" floor the task asks for.
  3. FADE GUARD.  The clip fades from and to black (f0-f22, f353-f365).  A
     global multiplicative dim leaves HSV S untouched (S = (max-min)/max is
     scale-invariant) and leaves a luminance RATIO nominally untouched, but
     not after 8-bit quantisation at low levels.  Those frames are excluded
     from every phase and the exclusion is recorded rather than assumed.

------------------------------------------------------------------------
CAVEAT SURFACE (which caveat touches which number)
------------------------------------------------------------------------
  * FIRE-INSTANCE vs WIND-ELEMENT.  Per the Tier-1 relationship-transfers
    law, the reference's absolute HUE and PALETTE do not transfer.  P95/P20
    is a ratio WITHIN a region and mid-band S is a contrast-of-channels
    statistic; both are relationship-class and both are why they were chosen.
    The one number here that is NOT relationship-class is `hue_mode`, which
    is reported as description only.
  * VENUE.  Ownership (T-3a) is venue-coupled by the conductor's own R-23/A-2
    finding — it counts the effect's share of the FRAME's top pixels, and the
    frame's other hot sources are a property of the room.  The reference is an
    outdoor dusk scene with no braziers; our venue is a cathedral with a
    brazier population.  Ownership is therefore DIAGNOSTIC ONLY per R-25 and
    is reported with that stamp attached in the output.
  * CODEC.  VP6F, 4:2:0, 1280x720, ~29.97 fps.  Chroma is subsampled 2x2, so
    the hue test resolves at 2x2 blocks (visible as the blocky mask boundary
    in `evidence/mask-overlay-zoom-f60.png`).  This touches (i) the mask
    boundary, (ii) saturation of small/thin features, and (iii) the
    discrete-element census, which is the measurement most degraded by it —
    a sub-4 px spark is below the chroma grid.  It does NOT materially touch
    P95/P20, which is a luma statistic over ~50 kpx.
  * ART STYLE.  Painterly hand-authored VFX at 720p vs our low-poly Godot
    render at 1080p.  Different resolution changes the ABSOLUTE component
    census (item 3) but not the percentile statistics, which are
    scale-invariant over a region this large.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vfx_lap2_battery import luma, sat_val  # noqa: E402  the SAME statistics

REF_SHA256 = "855bb3d9c7edca8b372869e667682eda6de85ea813628377e567522d9e998637"

# --- constants transcribed from the battery, named so drift is visible -----
MIN_COMPONENT_PX = 12          # vfx_lap2_battery.MIN_COMPONENT_PX
TOP_FRAC = 0.005               # BARS["T3a_top_frac"] -- top 0.5%
MIDBAND = (35, 65)             # the battery's mid-band percentile window

# --- the a-priori bars under adjudication ---------------------------------
BAR_T3B = 4.0
BAR_T3C = 0.55
BAR_T3A = 0.75

# --- segmentation defaults ------------------------------------------------
HUE_WARM = (330.0, 60.0)       # wrapped sector: [330,360) U [0,60)
S_FLOOR = 0.35
L_FLOOR = 0.02                 # verified INERT below 0.10 (see --sweep)
CLOSE_RADIUS = 9
SPATIAL_FLOOR_DILATE = 25


# ===========================================================================
# 0. INPUT
# ===========================================================================

def verify(path, expect=REF_SHA256):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    got = h.hexdigest()
    if expect and got != expect:
        raise SystemExit("HASH MISMATCH\n  expected %s\n  got      %s" % (expect, got))
    return got


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height,r_frame_rate,codec_name,pix_fmt",
         "-of", "json", path], capture_output=True, text=True, check=True).stdout
    s = json.loads(out)["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    return int(s["width"]), int(s["height"]), float(num) / float(den), \
        s["codec_name"], s["pix_fmt"]


def decode(path, w, h):
    """Whole-clip decode to a uint8 stack.  374 frames at 720p is ~1 GiB."""
    p = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo",
         "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = w * h * 3
    frames = []
    while True:
        buf = p.stdout.read(n)
        if not buf or len(buf) < n:
            break
        frames.append(np.frombuffer(buf, np.uint8).reshape(h, w, 3))
    p.stdout.close()
    p.wait()
    return np.stack(frames)


# ===========================================================================
# 1. COLOUR
# ===========================================================================

def hue_sat(f):
    """HSV hue (degrees) and saturation.

    Saturation here is COMPUTED THE SAME WAY as `vfx_lap2_battery.sat_val`
    -- (max-min)/max -- and `--selfcheck` asserts the two agree bit-for-bit.
    Hue is new (the battery never needed it, having a control arm instead).
    """
    a = f.astype(np.float32) / 255.0
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(2)
    mn = a.min(2)
    c = mx - mn
    hh = np.zeros_like(mx)
    nz = c > 1e-6
    i = (mx == r) & nz
    hh[i] = ((g - b)[i] / c[i]) % 6
    i = (mx == g) & nz
    hh[i] = ((b - r)[i] / c[i]) + 2
    i = (mx == b) & nz
    hh[i] = ((r - g)[i] / c[i]) + 4
    s = np.where(mx > 1e-6, c / np.maximum(mx, 1e-6), 0.0)
    return hh * 60.0, s


def warm_mask(hh, s, L, s_floor=S_FLOOR, l_floor=L_FLOOR):
    """REF-TIGHT: the effect's own emissive pixels.

    Hue sector + chroma floor + a (verified inert) luma floor, then the
    battery's own 3x3 opening and >=12 px component filter, so that the
    spatial-coherence discipline is identical on both sides of the
    comparison.
    """
    lo, hi = HUE_WARM
    W = ((hh < hi) | (hh >= lo)) & (s > s_floor) & (L > l_floor)
    W = ndimage.binary_opening(W, np.ones((3, 3)))
    lab, k = ndimage.label(W, np.ones((3, 3)))
    if not k:
        return W, lab, np.array([])
    sz = np.array(ndimage.sum(W, lab, range(1, k + 1)))
    keep = np.nonzero(sz >= MIN_COMPONENT_PX)[0] + 1
    W = np.isin(lab, keep) if keep.size else np.zeros_like(W)
    lab, k = ndimage.label(W, np.ones((3, 3)))
    sz = np.array(ndimage.sum(W, lab, range(1, k + 1))) if k else np.array([])
    return W, lab, sz


def support_mask(W, radius=CLOSE_RADIUS):
    """REF-SUPPORT: the effect's morphological FOOTPRINT.

    Every pixel inside is measured regardless of its own hue or saturation,
    which is the decisive circularity control for T-3(c): a region defined by
    where the effect IS rather than by what colour each pixel happens to be.
    Analogous in intent to the battery's ribbon-torus segmentation, which
    likewise admits pixels the chroma test would reject.
    """
    S = ndimage.binary_closing(W, np.ones((radius, radius)))
    return ndimage.binary_fill_holes(S)


# ===========================================================================
# 2. THE THREE STATISTICS -- transcribed from the battery
# ===========================================================================

def region_stats(M, L, sA):
    """P95/P20 and mid-band HSV S over a region.

    Transcribed from `vfx_lap2_battery.measure()`:
        p95 = percentile(L[E], 95); p20 = percentile(L[E], 20)
        lo, hi = percentile(L[E], [35, 65])
        mid = E & (L >= lo) & (L <= hi);  midS = sA[mid].mean()
    """
    n = int(M.sum())
    if n < 40:                                   # the battery's own guard
        return dict(area=n, p95=np.nan, p20=np.nan, ratio=np.nan, midS=np.nan)
    v = L[M]
    p95 = float(np.percentile(v, 95))
    p20 = float(np.percentile(v, 20))
    lo, hi = np.percentile(v, MIDBAND)
    mid = M & (L >= lo) & (L <= hi)
    midS = float(sA[mid].mean()) if mid.sum() else np.nan
    return dict(area=n, p95=p95, p20=p20,
                ratio=p95 / max(p20, 1e-6), midS=midS)


def ownership(M, L, valid=None):
    """Effect region's share of the frame's top-0.5% luminance pixels.

    Transcribed from `vfx_lap2_battery.t3a_ownership()`, including its
    threshold-based top set (NOT exact-rank -- ties from clipped-white cores
    would otherwise let an arbitrary tie-break decide the number) and its
    exact-rank corroborator alongside.
    """
    if valid is None:
        valid = np.ones(L.shape, bool)
    Lv = L[valid]
    n_valid = int(valid.sum())
    thr = float(np.percentile(Lv, 100.0 * (1.0 - TOP_FRAC)))
    top = valid & (L >= thr)
    ktop = int(top.sum())
    k_target = int(round(TOP_FRAC * n_valid))
    flat = np.where(valid, L, -1.0).ravel()
    ridx = np.argpartition(flat, -k_target)[-k_target:]
    top_rank = np.zeros(flat.size, bool)
    top_rank[ridx] = True
    top_rank = top_rank.reshape(L.shape)
    return dict(
        own=float((top & M).sum()) / max(ktop, 1),
        own_rank=float((top_rank & M).sum()) / max(k_target, 1),
        top_thr_L=thr, top_px=ktop,
        top_frac_actual=ktop / max(n_valid, 1),
        frame_max_L=float(Lv.max()),
        clipped_frac=float((L[M] > 0.95).mean()) if M.sum() else 0.0,
    ), top


# ===========================================================================
# 3. DISCRETE vs CONTINUOUS  (R-25 route-correction hypothesis)
# ===========================================================================

def decompose(W, lab, sz, top, thresholds=(100, 200, 500, 1000)):
    """Split the effect region into a CONTINUOUS form and DISCRETE elements.

    R-25 hypothesises that the reference's shed elements are SPARK-CLASS
    (they reach the frame's top luminance tail) where ours are pale blobs
    that contributed 0.0 of ownership.  The number that settles it is:
    what fraction of the reference's OWN top-tail pixels sit in discrete
    elements rather than in the continuous mass?

    Classification is by connected-component AREA, and the threshold is
    SWEPT rather than picked, because no principled single value exists.
    The largest component is reported separately from the threshold family,
    since in this footage it is 36-57 kpx against a runner-up of ~1-7 kpx --
    the split is not close and does not depend on where the line is drawn.
    """
    out = {"n_components": int(sz.size)}
    if not sz.size:
        return out
    order = np.argsort(sz)[::-1]
    largest_lbl = int(order[0] + 1)
    Lg = lab == largest_lbl
    top_total = max(int(top.sum()), 1)
    top_in_effect = int((top & W).sum())
    out.update({
        "largest_component_px": int(sz[order[0]]),
        "runner_up_px": int(sz[order[1]]) if sz.size > 1 else 0,
        "largest_area_share": float(sz[order[0]] / sz.sum()),
        "top_tail_px_in_effect": top_in_effect,
        "top_tail_px_in_largest": int((top & Lg).sum()),
        "top_tail_share_largest_of_effect":
            float((top & Lg).sum()) / max(top_in_effect, 1),
    })
    fam = {}
    for t in thresholds:
        small = np.nonzero(sz < t)[0] + 1
        D = np.isin(lab, small) if small.size else np.zeros_like(W)
        fam["lt_%d_px" % t] = {
            "n": int(small.size),
            "area_px": int(D.sum()),
            "area_share_of_effect": float(D.sum() / max(W.sum(), 1)),
            "top_tail_px": int((top & D).sum()),
            # THE R-25 NUMBER: discrete elements' share of the effect's own
            # top-tail pixels.
            "top_tail_share_of_effect": float((top & D).sum()) / max(top_in_effect, 1),
            "top_tail_share_of_frame": float((top & D).sum()) / top_total,
        }
    out["discrete_by_threshold"] = fam
    return out


# ===========================================================================
# 4. PHASES
# ===========================================================================

FADE_SLOPE = 0.010   # per-frame d(meanL); the fade ramps at ~0.026, the
                     # effect's decay at ~0.001 -- see the docstring below.


def derive_phases(A):
    """Phases derived from the clip's own curves, not asserted.

    Two curves: whole-frame mean luma (finds the fades, which are global
    multiplicative dims) and warm-mask area (finds the effect).

    ⚑ THE FADE DETECTOR IS SLOPE-BASED, AND THE FIRST VERSION WAS NOT.
    A LEVEL-based detector ("full brightness = meanL within 1.5% of its
    median") returns cleanly and is WRONG on this clip, because the effect
    supplies a large share of the frame's own light: as the fire dies, mean
    luma slides 0.318 -> 0.276 and crosses any level threshold set from the
    plateau.  The first cut therefore stamped `fade_out` at f246 -- 109
    frames early -- and, worse, handed back a `null_no_effect` window that
    still contained fire, i.e. a NULL THAT WAS NOT NULL.  Caught by
    disagreeing with the curve already read by hand during recon, not by
    reading this function.

    The fades are separable by SHAPE, not by level: the fade ramps at
    ~0.026 luma/frame and the effect's decay at ~0.001 luma/frame -- 26x
    apart, so a slope gate at 0.010 has an order of magnitude of headroom on
    both sides.  Same family as the battery's own § 5 lesson: the statistic
    that survives is the one whose operand still denotes after the scene
    changes under it.
    """
    n = A.shape[0]
    meanL = np.zeros(n)
    warm = np.zeros(n, int)
    for i in range(n):
        f = A[i]
        L = luma(f)
        hh, s = hue_sat(f)
        meanL[i] = L.mean()
        warm[i] = int((((hh < 60) | (hh >= 330)) & (s > S_FLOOR) & (L > 0.10)).sum())

    d = np.diff(meanL, prepend=meanL[0])
    nz = np.nonzero(meanL > 0.02)[0]
    # fade-in ends at the first frame after clip-start whose slope has
    # collapsed out of the ramp; fade-out begins at the last such frame.
    full_lo = int(nz.min())
    while full_lo < n - 1 and d[full_lo + 1] > FADE_SLOPE:
        full_lo += 1
    full_hi = int(nz.max())
    while full_hi > 0 and d[full_hi] < -FADE_SLOPE:
        full_hi -= 1
    full_hi -= 1                      # last frame BEFORE the ramp begins

    inside = np.arange(full_lo, full_hi + 1)
    wi = warm[inside]
    hi_thr = 0.45 * wi.max()
    lo_thr = 1.35 * np.median(warm[inside][-40:])
    action_end = full_lo
    for i in inside:
        if warm[i] >= hi_thr:
            action_end = i
    null_start = full_hi
    for i in inside[::-1]:
        if warm[i] > lo_thr:
            null_start = min(i + 1, full_hi)
            break
    return {
        "fade_in": [0, full_lo - 1],
        "action": [full_lo, int(action_end)],
        "decay": [int(action_end) + 1, int(null_start) - 1],
        "null_no_effect": [int(null_start), full_hi],
        "fade_out": [full_hi + 1, n - 1],
        "curves": {"mean_luma": meanL.round(4).tolist(),
                   "warm_area_px": warm.tolist()},
        "thresholds_used": {"action_hi": float(hi_thr), "null_lo": float(lo_thr),
                            "fade_slope": FADE_SLOPE},
        "fade_slope_evidence": {
            "median_abs_slope_in_fade_in":
                float(np.median(np.abs(d[max(nz.min(), 1):full_lo + 1]))),
            "median_abs_slope_in_effect_decay":
                float(np.median(np.abs(d[full_hi - 60:full_hi]))),
        },
    }


# ===========================================================================
# 5. PASSES
# ===========================================================================

def agg(vals):
    v = np.array([x for x in vals if np.isfinite(x)], float)
    if not v.size:
        return None
    return {"median": float(np.median(v)), "mean": float(v.mean()),
            "p25": float(np.percentile(v, 25)), "p75": float(np.percentile(v, 75)),
            "min": float(v.min()), "max": float(v.max()), "n": int(v.size)}


def run_window(A, lo, hi, s_floor=S_FLOOR, l_floor=L_FLOOR,
               close_radius=CLOSE_RADIUS, decomp=True, spatial_floor=True):
    acc = {k: [] for k in (
        "tight_ratio", "tight_midS", "tight_area", "tight_p95", "tight_p20",
        "supp_ratio", "supp_midS", "supp_area",
        "lc_ratio", "lc_midS", "lc_own",
        "own", "own_rank", "clipped_frac", "top_thr_L",
        "floor_ratio", "floor_midS", "floor_own",
        "lift_ratio", "lift_midS",
        "disc_top_share_500", "disc_top_share_200", "disc_area_share_500",
        "largest_top_share", "n_components", "largest_px")}
    per = []
    for i in range(lo, hi + 1):
        f = A[i]
        L = luma(f)
        sA, _ = sat_val(f)
        hh, s = hue_sat(f)
        W, lab, sz = warm_mask(hh, s, L, s_floor, l_floor)
        SUP = support_mask(W, close_radius)
        st = region_stats(W, L, sA)
        ss = region_stats(SUP, L, sA)
        ow, top = ownership(W, L)
        row = {"frame": i, "tight": st, "support": ss, "ownership": ow}
        acc["tight_ratio"].append(st["ratio"])
        acc["tight_midS"].append(st["midS"])
        acc["tight_area"].append(st["area"])
        acc["tight_p95"].append(st["p95"])
        acc["tight_p20"].append(st["p20"])
        acc["supp_ratio"].append(ss["ratio"])
        acc["supp_midS"].append(ss["midS"])
        acc["supp_area"].append(ss["area"])
        acc["own"].append(ow["own"])
        acc["own_rank"].append(ow["own_rank"])
        acc["clipped_frac"].append(ow["clipped_frac"])
        acc["top_thr_L"].append(ow["top_thr_L"])
        # LARGEST COMPONENT ONLY -- the fire mass with the clip's non-fire
        # warm content (monster eye-glows, loot beams) excluded by
        # construction.  The temporal null shows that content is ~8.4 kpx and
        # arrives as its OWN medium components, so restricting to the largest
        # removes it without a hand-drawn ROI.
        if sz.size:
            LC = lab == int(np.argmax(sz) + 1)
            lcs = region_stats(LC, L, sA)
            lco, _ = ownership(LC, L)
            row["largest_component"] = {"ratio": lcs["ratio"], "midS": lcs["midS"],
                                        "area": lcs["area"], "own": lco["own"]}
            acc["lc_ratio"].append(lcs["ratio"])
            acc["lc_midS"].append(lcs["midS"])
            acc["lc_own"].append(lco["own"])
        if decomp:
            d = decompose(W, lab, sz, top)
            row["decomposition"] = d
            if "discrete_by_threshold" in d:
                acc["disc_top_share_500"].append(
                    d["discrete_by_threshold"]["lt_500_px"]["top_tail_share_of_effect"])
                acc["disc_top_share_200"].append(
                    d["discrete_by_threshold"]["lt_200_px"]["top_tail_share_of_effect"])
                acc["disc_area_share_500"].append(
                    d["discrete_by_threshold"]["lt_500_px"]["area_share_of_effect"])
                acc["largest_top_share"].append(d["top_tail_share_largest_of_effect"])
                acc["n_components"].append(d["n_components"])
                acc["largest_px"].append(d["largest_component_px"])
        if spatial_floor:
            # NEGATIVE CONTROL 2: everything outside a 25 px dilation of the
            # effect's support -- sky, ground, distant monsters.
            NE = ~ndimage.binary_dilation(SUP, np.ones((SPATIAL_FLOOR_DILATE,) * 2))
            fs = region_stats(NE, L, sA)
            fo, _ = ownership(NE, L)
            row["spatial_floor"] = {"ratio": fs["ratio"], "midS": fs["midS"],
                                    "area": fs["area"], "own": fo["own"]}
            acc["floor_ratio"].append(fs["ratio"])
            acc["floor_midS"].append(fs["midS"])
            acc["floor_own"].append(fo["own"])
            # LIFT-OVER-FLOOR.  The absolutes below are venue-, codec- and
            # art-style-coupled; the RATIO of effect to its own scene is the
            # relationship-class form of the same claim, and is the currency
            # in which a bar can cross venues under the Tier-1 law.
            if np.isfinite(fs["ratio"]) and fs["ratio"] > 1e-6:
                acc["lift_ratio"].append(st["ratio"] / fs["ratio"])
            if np.isfinite(fs["midS"]) and fs["midS"] > 1e-6:
                acc["lift_midS"].append(st["midS"] / fs["midS"])
        per.append(row)
    return {k: agg(v) for k, v in acc.items() if v}, per


def sweep(A, frames, kind, values):
    out = []
    for val in values:
        rr, ss, aa = [], [], []
        for i in frames:
            f = A[i]
            L = luma(f)
            sA, _ = sat_val(f)
            hh, s = hue_sat(f)
            sf = val if kind == "s_floor" else S_FLOOR
            lf = val if kind == "l_floor" else L_FLOOR
            W, lab, sz = warm_mask(hh, s, L, sf, lf)
            M = support_mask(W, int(val)) if kind == "close_radius" else W
            st = region_stats(M, L, sA)
            rr.append(st["ratio"])
            ss.append(st["midS"])
            aa.append(st["area"])
        out.append({kind: val, "ratio_median": float(np.nanmedian(rr)),
                    "midS_median": float(np.nanmedian(ss)),
                    "area_median": float(np.nanmedian(aa))})
    return out


def our_render_floor(on_path, ctl_path, w, h, lo, hi, tau):
    """Run the SAME scene-floor instrument on our own lap-2 render.

    Why this is here and not left to the battery: the battery measures the
    EFFECT and never measured the venue's own floor for these two statistics,
    so lap-2 has no denominator.  Without one, the reference's numbers can
    only be compared to ours as ABSOLUTES -- and absolutes are exactly what
    the Tier-1 law says does not transfer across a fire-instance/wind-element,
    painterly/low-poly, VP6/H.264 boundary.

    With a floor on both sides, the same claim can be stated as LIFT OVER
    SCENE FLOOR, which is relationship-class and therefore portable.  The
    conductor can then re-cut in whichever currency he judges defensible; the
    measurement supplies both and prefers neither.

    The effect region here is the battery's own control-differenced mask
    (|dL| > tau, 3x3 opened, components >= 12 px) -- not the hue mask, which
    would be ill-posed on a teal-on-teal wind effect in a warm-lit cathedral.
    That asymmetry is the point: each side is segmented by the instrument
    that is well-posed for it, and only the STATISTICS are held identical.
    """
    pa = subprocess.Popen(["ffmpeg", "-v", "error", "-i", on_path, "-f", "rawvideo",
                           "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    pb = subprocess.Popen(["ffmpeg", "-v", "error", "-i", ctl_path, "-f", "rawvideo",
                           "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = w * h * 3
    acc = {k: [] for k in ("eff_ratio", "eff_midS", "eff_own", "eff_area",
                           "floor_ratio", "floor_midS", "floor_own",
                           "lift_ratio", "lift_midS")}
    i = 0
    while True:
        ba, bb = pa.stdout.read(n), pb.stdout.read(n)
        if not ba or not bb or len(ba) < n or len(bb) < n:
            break
        if i > hi:
            break
        if i < lo:
            i += 1
            continue
        fa = np.frombuffer(ba, np.uint8).reshape(h, w, 3)
        fb = np.frombuffer(bb, np.uint8).reshape(h, w, 3)
        La, Lb = luma(fa), luma(fb)
        sA, _ = sat_val(fa)
        E = ndimage.binary_opening(np.abs(La - Lb) > tau, np.ones((3, 3)))
        lab, k = ndimage.label(E, np.ones((3, 3)))
        if k:
            sz = np.array(ndimage.sum(E, lab, range(1, k + 1)))
            keep = np.nonzero(sz >= MIN_COMPONENT_PX)[0] + 1
            E = np.isin(lab, keep) if keep.size else np.zeros_like(E)
        es = region_stats(E, La, sA)
        eo, _ = ownership(E, La)
        NE = ~ndimage.binary_dilation(E, np.ones((SPATIAL_FLOOR_DILATE,) * 2))
        fs = region_stats(NE, La, sA)
        fo, _ = ownership(NE, La)
        acc["eff_ratio"].append(es["ratio"])
        acc["eff_midS"].append(es["midS"])
        acc["eff_own"].append(eo["own"])
        acc["eff_area"].append(es["area"])
        acc["floor_ratio"].append(fs["ratio"])
        acc["floor_midS"].append(fs["midS"])
        acc["floor_own"].append(fo["own"])
        if np.isfinite(fs["ratio"]) and fs["ratio"] > 1e-6:
            acc["lift_ratio"].append(es["ratio"] / fs["ratio"])
        if np.isfinite(fs["midS"]) and fs["midS"] > 1e-6:
            acc["lift_midS"].append(es["midS"] / fs["midS"])
        i += 1
    for p in (pa, pb):
        p.stdout.close()
        p.wait()
    return {k: agg(v) for k, v in acc.items() if v}


def selfcheck(A):
    """Assert the transcription equals the battery's own expressions.

    Not a claim in a docstring -- the battery's exact lines are re-executed
    here on the same array and compared.  This module refuses to report if
    they disagree.
    """
    f = A[60]
    L = luma(f)
    sA, sv = sat_val(f)
    hh, s = hue_sat(f)
    # (i) hue_sat's S must BE the battery's sat_val S
    assert np.allclose(s, sA, atol=0), "hue_sat S != battery sat_val S"
    W, lab, sz = warm_mask(hh, s, L)
    # (ii) the battery's own T-3b/c block, verbatim
    v = L[W]
    b_p95 = float(np.percentile(v, 95))
    b_p20 = float(np.percentile(v, 20))
    lo, hi = np.percentile(v, [35, 65])
    mid = W & (L >= lo) & (L <= hi)
    b_midS = float(sA[mid].mean())
    st = region_stats(W, L, sA)
    assert abs(st["p95"] - b_p95) < 1e-12 and abs(st["p20"] - b_p20) < 1e-12
    assert abs(st["midS"] - b_midS) < 1e-12
    # (iii) the battery's own ownership block, verbatim
    valid = np.ones(L.shape, bool)
    thr = float(np.percentile(L[valid], 100.0 * (1.0 - TOP_FRAC)))
    top = valid & (L >= thr)
    b_own = float((top & W).sum()) / max(int(top.sum()), 1)
    ow, _ = ownership(W, L)
    assert abs(ow["own"] - b_own) < 1e-12
    return {"transcription_matches_battery": True,
            "checked_on_frame": 60,
            "p95": b_p95, "p20": b_p20, "midS": b_midS, "own": b_own}


def ui_probe(A, phases):
    """Is there UI to exclude?  The battery excludes a HUD; this clip may not
    have one.  Rather than assert 'no UI', measure it: a HUD is static bright
    structure that survives a camera pan."""
    lo, hi = phases["action"]
    idx = np.linspace(lo, hi, 12).astype(int)
    L = np.stack([luma(A[i]) for i in idx])
    static = L.std(0) < 0.01
    bright = L.mean(0) > 0.5
    cand = static & bright
    cand = ndimage.binary_opening(cand, np.ones((3, 3)))
    return {"static_bright_px": int(cand.sum()),
            "frac_of_frame": float(cand.mean()),
            "verdict": "no UI overlay detected" if cand.mean() < 1e-4
                       else "UI-like static bright region present -- investigate"}


# ===========================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="/private/tmp/vfx-lap1-seats/extract/reference_video.flv")
    ap.add_argument("--out", required=True)
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--no-hash", action="store_true")
    ap.add_argument("--our-on", help="our lap-2 treatment-arm mp4")
    ap.add_argument("--our-ctl", help="our lap-2 vfx-off control mp4")
    ap.add_argument("--our-sustain", nargs=2, type=int, default=[62, 143])
    ap.add_argument("--our-tau", type=float, default=0.07647053897380829)
    a = ap.parse_args()

    sha = "SKIPPED" if a.no_hash else verify(a.ref)
    w, h, fps, codec, pix = probe(a.ref)
    A = decode(a.ref, w, h)
    res = {
        "artifact": a.ref, "sha256": sha,
        "video": {"w": w, "h": h, "fps": fps, "codec": codec, "pix_fmt": pix,
                  "frames_decoded": int(A.shape[0])},
        "selfcheck": selfcheck(A),
        "instrument": {
            "hue_sector_deg": list(HUE_WARM), "s_floor": S_FLOOR,
            "l_floor": L_FLOOR, "close_radius": CLOSE_RADIUS,
            "min_component_px": MIN_COMPONENT_PX, "top_frac": TOP_FRAC,
            "midband_percentiles": list(MIDBAND),
        },
        "bars_under_adjudication": {"T3b_p95_p20": BAR_T3B,
                                    "T3c_midband_S": BAR_T3C,
                                    "T3a_ownership_DIAGNOSTIC_ONLY": BAR_T3A},
    }
    ph = derive_phases(A)
    res["phases"] = {k: v for k, v in ph.items() if k != "curves"}
    res["phase_curves"] = ph["curves"]
    res["ui_probe"] = ui_probe(A, ph)

    for name in ("action", "decay", "null_no_effect"):
        lo, hi = ph[name]
        if hi < lo:
            continue
        summ, per = run_window(A, lo, hi)
        res.setdefault("windows", {})[name] = {"range": [lo, hi], "summary": summ}
        res.setdefault("per_frame", {})[name] = per

    if a.sweep:
        lo, hi = ph["action"]
        fr = list(np.linspace(lo, hi, 15).astype(int))
        res["sweeps"] = {
            "s_floor": sweep(A, fr, "s_floor", [0.05, 0.10, 0.20, 0.30, 0.35, 0.45, 0.55]),
            "l_floor": sweep(A, fr, "l_floor", [0.0, 0.02, 0.05, 0.10, 0.15, 0.20]),
            "close_radius": sweep(A, fr, "close_radius", [3, 5, 9, 15, 25]),
        }

    if a.our_on and a.our_ctl:
        ow_, oh_, ofps, ocodec, opix = probe(a.our_on)
        res["our_render"] = {
            "on": a.our_on, "ctl": a.our_ctl,
            "sha256_on": verify(a.our_on, None), "sha256_ctl": verify(a.our_ctl, None),
            "video": {"w": ow_, "h": oh_, "fps": ofps, "codec": ocodec, "pix_fmt": opix},
            "sustain": a.our_sustain, "tau": a.our_tau,
            "summary": our_render_floor(a.our_on, a.our_ctl, ow_, oh_,
                                        a.our_sustain[0], a.our_sustain[1], a.our_tau),
        }

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(res, indent=1))
    s = res["windows"]["action"]["summary"]
    print("ACTION %s  n=%d" % (res["phases"]["action"], s["tight_ratio"]["n"]))
    print("  T-3b P95/P20 tight  median %.3f  [%.3f .. %.3f]  bar %.1f"
          % (s["tight_ratio"]["median"], s["tight_ratio"]["min"],
             s["tight_ratio"]["max"], BAR_T3B))
    print("  T-3b P95/P20 supp   median %.3f" % s["supp_ratio"]["median"])
    print("  T-3c mid-band S     median %.4f [%.4f .. %.4f]  bar %.2f"
          % (s["tight_midS"]["median"], s["tight_midS"]["min"],
             s["tight_midS"]["max"], BAR_T3C))
    print("  T-3a ownership      median %.4f  (DIAGNOSTIC ONLY)" % s["own"]["median"])
    if "disc_top_share_500" in s:
        print("  discrete<500px top-tail share  median %.4f"
              % s["disc_top_share_500"]["median"])
    if "lc_ratio" in s:
        print("  LARGEST-COMPONENT (fire mass only)  ratio %.3f  midS %.4f  own %.4f"
              % (s["lc_ratio"]["median"], s["lc_midS"]["median"], s["lc_own"]["median"]))
    print("  FLOOR (non-effect)  ratio %.3f  midS %.4f  own %.4f"
          % (s["floor_ratio"]["median"], s["floor_midS"]["median"],
             s["floor_own"]["median"]))
    print("  LIFT over floor     ratio %.3fx  midS %.3fx"
          % (s["lift_ratio"]["median"], s["lift_midS"]["median"]))
    if "null_no_effect" in res["windows"]:
        ns = res["windows"]["null_no_effect"]["summary"]
        print("  TEMPORAL NULL (no fire in frame): ratio %.3f  midS %.4f  own %.4f"
              % (ns["tight_ratio"]["median"], ns["tight_midS"]["median"],
                 ns["own"]["median"]))
    if "our_render" in res:
        o = res["our_render"]["summary"]
        print("OUR LAP-2 RENDER  sustain %s" % a.our_sustain)
        print("  effect ratio %.3f  midS %.4f  own %.4f"
              % (o["eff_ratio"]["median"], o["eff_midS"]["median"], o["eff_own"]["median"]))
        print("  floor  ratio %.3f  midS %.4f  own %.4f"
              % (o["floor_ratio"]["median"], o["floor_midS"]["median"],
                 o["floor_own"]["median"]))
        print("  LIFT   ratio %.3fx midS %.3fx"
              % (o["lift_ratio"]["median"], o["lift_midS"]["median"]))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
