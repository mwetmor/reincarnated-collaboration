#!/usr/bin/env python3
"""REFERENCE-ANCHOR pass on the TRUE REFERENT -- charter R-29.

Supersedes the R-27/R-25 pass, which measured the WRONG referent (D3 2012
master, sha 855bb3d9...).  The forms of R-27 survive per R-28; its CONSTANTS
die.  This module re-derives them from:

    seatsafe-A-src837-863.mp4   26 s, source t 837-863
    seatsafe-B-src1056-1081.mp4 25 s, source t 1056-1081
    (D4 S14 Whirlwind Barbarian, Cliptis KaMPoPywM40, h264 1080p60, audio
     stripped, three fixed-position black masks)

THE STATISTICS ARE IMPORTED, NOT RE-IMPLEMENTED.  `region_stats`, `ownership`,
`decompose` and `agg` come from `vfx_ref_anchor` (the R-27 module), which in
turn imports `luma` and `sat_val` from `vfx_lap2_battery`.  So "the same
statistic as R-27, which is the same statistic as the lap-2 battery" is a fact
about the call graph across all three passes, not a claim in a comment.

===========================================================================
⚑ WHY THE R-27 SEGMENTATION COULD NOT BE REUSED, AND HOW THAT WAS ESTABLISHED
===========================================================================
R-27 segmented the reference by HUE SECTOR.  That was well-posed there for a
stated reason: the D3 clip's scene was TEAL (L-weighted hue mode 190-210 deg)
and its effect was FIRE (mode 0-30 deg), sharply bimodal and near-opposite.

**That premise is FALSE on the true referent, and it was measured before any
anchor number was taken.**  `vfx_true_recon.py` reports, over 260/250 sampled
frames:

    warm-sector share of chromatic luminance   A 0.836   B 0.800
    L-weighted hue mode                        A 25 deg  B 25 deg
    warm-mask area (R-27's exact rule)         A 561,610 px median  (~33% of frame)

The venue is a warm sandstone dungeon.  R-27's warm-hue mask selects a THIRD
OF THE FRAME here.  Applying it unchanged would have returned confident
numbers measuring the room.  That is this run's recurring failure shape -- the
check runs and the check is not the check -- caught this time by refusing to
run the instrument before re-establishing its premise.

Two replacements were considered and one was rejected on measurement:

  * MOTION-COMPENSATED TEMPORAL MEDIAN (the closest analogue of the battery's
    control arm).  REJECTED, on two independent grounds, both measured
    (`vfx_true_camtest.py`):
      (i)  the camera does not admit a global-translation model.  Phase
           correlation returns a peak/second-peak ratio of 1.24 (A) / 1.42 (B)
           -- i.e. essentially no isolated peak -- and registration improves
           the background residual by only 1.21-1.23x.  This is the same tell
           that produced a confident (0,0) global shift on a translating
           camera in lap-2 (measure note § 5, seventh instance).
      (ii) the camera is player-locked and the effect is centred on the
           player, so the effect occupies the SAME image region continuously.
           A temporal median over any window long enough to be a background
           would contain the effect.  (ii) alone is fatal and does not depend
           on (i).

  * RED-CHROMA SECTOR (adopted).  Direct pixel probing (`vfx_true_probe.py`)
    on named rectangles gives the separation the hue sector no longer has:

        region              chroma (max-min)   hue      S
        WW disc, lit         0.573             14 deg   0.744
        sandstone floor      0.200             23 deg   0.536
        torch flame          0.325             24 deg   0.562
        gold damage text     0.278             36 deg   0.424
        gold training dummy  0.20-0.30         20-33    0.40-0.44
        mob health bar       0.21-0.28         12 deg   0.64-0.84
        HUD resource orb     0.310             26 deg   0.812   (masked as HUD)
        HUD health globe     0.310            330 deg   0.710   (masked as HUD)

    So the effect is separated by being simultaneously RED-SHIFTED (hue < 20
    deg where the venue sits at 22-27) and HIGH-CHROMA (C > 0.35 where the
    venue's warm content tops out near 0.33).

CIRCULARITY, AND WHAT IS DONE ABOUT IT
--------------------------------------
A chroma test is a saturation-family test, so it IS circular for the mid-band-S
statistic -- the same hazard R-27 named and swept.  Three defences, all of them
R-27's, carried forward unchanged:
  1. the chroma floor is SWEPT across 0.15 .. 0.55 and the (c) conclusion is
     only reported as anchored if it survives the most permissive setting;
  2. an EFF-SUPPORT segmentation measures every pixel inside the effect's
     morphological footprint REGARDLESS of that pixel's own chroma, removing
     pixel-wise chroma selection from the measured set entirely;
  3. the in-clip TEMPORAL NULL runs the identical chroma-selected instrument
     on frames where the effect is absent, giving the instrument's own
     SELECTION FLOOR -- the honest limit on any (c) claim.
A chroma test is NOT circular for P95/P20 (a luminance ratio within a region)
nor for ownership (a rank statistic against the whole frame).

CONFOUNDS THIS REFERENT HAS AND THE OLD ONE DID NOT
---------------------------------------------------
  * A full Diablo IV HUD, several of whose elements are large, saturated and
    warm.  Handled by a HUD mask whose boxes are VERIFIED against the
    temporal-std map (static structure) rather than asserted.
  * Damage-number spam, mob nameplates and mob health bars, overlaid on the
    play area and therefore not croppable.  Handled by a best-effort text/bar
    detector, reported as a SEPARATE ARM -- raw numbers are reported too, per
    the re-anchor brief, so the reader can see what the masking costs.
  * S14 Dust-Devil procs riding alongside the core whirlwind (legolas RT-4:
    subtractable).  Handled by connected-component separation from the core
    disc, reported with and without.
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
# The SAME statistics, by import, across battery -> R-27 -> R-29.
from vfx_ref_anchor import MIDBAND, MIN_COMPONENT_PX, TOP_FRAC  # noqa: E402
from vfx_ref_anchor import agg, decompose, ownership, region_stats  # noqa: E402
from vfx_lap2_battery import luma, sat_val  # noqa: E402
from vfx_true_recon import BLACK_MASKS, frames, hue_sat, probe, valid_map  # noqa: E402

# --- our own venue's floor, measured in the R-27 pass § R6 -----------------
# These are OUR side and are unaffected by the referent swap: they were taken
# from `plk06650_cathedral_fxon/fxctl` (cc815bcf / fd1b9f65), which R-28 did
# not touch.  They are the denominators the lift-form and sign-form bars are
# expressed against.
OURS_LAP2 = {
    "effect_ratio": 2.352, "floor_ratio": 2.257, "lift_ratio": 1.060,
    "effect_midS": 0.2906, "floor_midS": 0.6225, "lift_midS": 0.466,
    "effect_own": 0.4017, "floor_own": 0.4367, "lift_own": 0.92,
    "top_tail_share_of_self": 0.0930,
    "source": "R-27 note § R6; artifacts cc815bcf… / fd1b9f65…",
}

# --- segmentation defaults, all swept ------------------------------------
HUE_HI = 20.0          # red-shifted sector: [340,360) U [0,20)
HUE_LO = 340.0
C_FLOOR = 0.35         # chroma = max-min, in 0..1
L_FLOOR = 0.05
CLOSE_RADIUS = 9
SPATIAL_FLOOR_DILATE = 25
BURST_PX = 2000        # largest red component >= this  => BURST frame
NULL_PX = 100          # largest red component <= this  => in-clip NULL frame

# --- HUD boxes.  DERIVED from the temporal-std map, not asserted. ---------
# Each box is the bounding structure of a large low-variance component in
# `Lstd_{A,B}.npy` (see vfx_true_recon), padded, plus the two ANIMATED HUD
# elements (health globe, resource orb) which are not low-variance and are
# therefore located by inspection and recorded here as such.
HUD_BOXES = [
    ("boss_bar",        660,    0,  620,  105, "static comp x682 y4 w558 h84 (B) / x686 w562 (A)"),
    ("minimap_zone",   1430,    0,  490,  345, "static comp x1456 y4 w460 h368 (A)"),
    ("party_frames",      0,  400,  310,  145, "static comps x10 y420 w49 h92; x68 y430/480 w115 h30"),
    ("buff_row",        540,  815,  430,   62, "static comp x771 y835 w149 h84 (A)"),
    ("skill_bar",       480,  860,  935,  220, "static comp x496 y877 w894 h196 (both clips)"),
    ("health_globe",    370,  855,  275,  225, "ANIMATED - by inspection; partial static comps x404 y948/993"),
    ("resource_orb",   1225,  855,  275,  225, "ANIMATED - by inspection (mirror of health_globe)"),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def hud_map(h, w):
    H = np.zeros((h, w), bool)
    for _, x, y, ww, hh, _ in HUD_BOXES:
        H[max(0, y):min(h, y + hh), max(0, x):min(w, x + ww)] = True
    return H


def chroma(f):
    a = f.astype(np.float32) / 255.0
    return a.max(2) - a.min(2)


def coherent(M, min_px=MIN_COMPONENT_PX):
    """The battery's own 3x3 opening + >=12 px component filter, so the
    spatial-coherence discipline is identical on both sides of every
    comparison in this run."""
    M = ndimage.binary_opening(M, np.ones((3, 3)))
    lab, k = ndimage.label(M, np.ones((3, 3)))
    if not k:
        return np.zeros_like(M), np.zeros(M.shape, int), np.array([])
    sz = np.array(ndimage.sum(M, lab, range(1, k + 1)))
    keep = np.nonzero(sz >= min_px)[0] + 1
    M = np.isin(lab, keep) if keep.size else np.zeros_like(M)
    lab, k = ndimage.label(M, np.ones((3, 3)))
    sz = np.array(ndimage.sum(M, lab, range(1, k + 1))) if k else np.array([])
    return M, lab, sz


def drop_bar_shaped(M, lab, sz):
    """Reject components shaped like a Diablo IV mob HEALTH BAR.

    ⚑ FOUND BY OVERLAY, NOT BY NUMBER, AND IT CONTRADICTS THIS MODULE'S OWN
    EARLIER REASONING.  The `clutter_mask` docstring argues that health bars
    cannot enter the effect mask because their chroma (0.21-0.28 at the three
    rectangles first probed) is below the 0.35 floor.  The overlay shows
    otherwise: at A t=2.10 the aux components sit squarely on the "Boss
    Training Dummy" bars.  The probe sampled three bars; the clip contains
    many, at varying fill and varying background, and the FULL red segment of
    a nearly-undamaged bar does clear 0.35.

    Measured contamination before this filter, eight burst frames across both
    clips: 0.0% / 0.0% / 0.0% / 0.0% / 10.6% / 13.7% / 15.7% / 17.4% of the
    effect region.  Not negligible, and biased -- bars are flat, uniform and
    mid-luminance, so they DEPRESS P95/P20 and RAISE mid-band S.

    The rule is SHAPE, not colour, because shape is what a bar has and a
    disc-sweep does not: bounding box <= 20 px tall, >= 55 px wide, aspect
    >= 4, and >= 45% filled (a solid rectangle, not a thin arc that happens to
    lie flat).  The rejected area is reported per frame so the filter's cost
    is visible rather than assumed.
    """
    if not sz.size:
        return M, lab, sz, 0
    objs = ndimage.find_objects(lab)
    kill = []
    for k, sl in enumerate(objs):
        if sl is None:
            continue
        hh_ = sl[0].stop - sl[0].start
        ww_ = sl[1].stop - sl[1].start
        n = int((lab[sl] == k + 1).sum())
        if hh_ <= 20 and ww_ >= 55 and ww_ / max(hh_, 1) >= 4.0 and n / max(hh_ * ww_, 1) > 0.45:
            kill.append(k + 1)
    if not kill:
        return M, lab, sz, 0
    K = np.isin(lab, kill)
    dropped = int(K.sum())
    M = M & ~K
    lab, k = ndimage.label(M, np.ones((3, 3)))
    sz = np.array(ndimage.sum(M, lab, range(1, k + 1))) if k else np.array([])
    return M, lab, sz, dropped


def eff_tight(hh, C, L, region, hue_hi=HUE_HI, hue_lo=HUE_LO,
              c_floor=C_FLOOR, l_floor=L_FLOOR):
    raw = ((hh < hue_hi) | (hh >= hue_lo)) & (C > c_floor) & (L > l_floor) & region
    M, lab, sz = coherent(raw)
    M, lab, sz, dropped = drop_bar_shaped(M, lab, sz)
    return M, lab, sz, dropped


def eff_support(M, radius=CLOSE_RADIUS):
    S = ndimage.binary_closing(M, np.ones((radius, radius)))
    return ndimage.binary_fill_holes(S)


# ---------------------------------------------------------------------------
# In-frame confounds: damage numbers, nameplate text, mob health bars.
# BEST-EFFORT, and labelled as such.  Reported as a separate arm so the cost
# of the masking is visible rather than baked in.
# ---------------------------------------------------------------------------
TEXT_CONTRAST = 0.30      # L - grey_erosion(L, 15x15)
TEXT_LEVEL = 0.35


def clutter_mask(f, L, sA, hhue, C):
    """BEST-EFFORT damage-number / nameplate-text mask.

    DISCRIMINATOR: Diablo IV draws its damage numbers and nameplates as bright
    glyphs with a HARD DARK OUTLINE.  So the tell is not brightness and not
    hue -- both of which the sandstone venue also has -- but a bright pixel
    with a much darker pixel within ~7 px.  `L - grey_erosion(L, 15x15)`
    measures exactly that, and broad bright scene regions (lit floor, walls,
    the effect disc itself) score near zero on it by construction.

    ⚑ A FIRST VERSION OF THIS FUNCTION FIRED ACROSS THE WHOLE FLOOR AND WAS
    CAUGHT BY THE OVERLAY, NOT BY THE NUMBER.  It carried a second sub-detector
    for mob health bars -- `(S > 0.45) & (C > 0.10)` opened with a (1,31)
    element to keep only wide-thin structure.  The Training Grounds sandstone
    is itself saturated (S p50 0.54-0.58, measured), and horizontal runs of it
    are certainly 31 px wide, so the detector selected 238,078 px -- 13% of the
    frame -- and read, on the overlay, as magenta confetti across the entire
    venue.  Every statistic downstream would have been computed on the
    complement of that.  The sub-detector is DELETED rather than tuned, for a
    stated reason: health bars cannot affect any number this pass reports.
    They are DIM (measured L p50 0.145 / 0.232) so they cannot enter a
    top-0.5% tail whose threshold is L >= 0.47, and their chroma (0.21-0.28)
    is below the 0.35 effect floor so they cannot enter the effect mask.
    A mask that removes nothing measurable is not worth its false positives.

    Verified cost/benefit at six burst frames across both clips:
      covers 0.867 of the frame's top-0.5% tail, for 6.7% of the scene area,
      and removes 4.1-10.5% of the effect region as collateral.
    """
    er = ndimage.grey_erosion(L, size=(15, 15))
    text = (L - er > TEXT_CONTRAST) & (L > TEXT_LEVEL)
    text = ndimage.binary_dilation(ndimage.binary_opening(text, np.ones((2, 2))),
                                   np.ones((9, 9)))
    bars = np.zeros_like(text)      # deliberately empty; see docstring
    return text, text, bars


def dust_devil_split(lab, sz, L):
    """legolas RT-4 subtractability, applied.

    The core Whirlwind disc is the barbarian's own sweep and is, in every
    burst frame inspected, the LARGEST red component by an order of magnitude.
    S14 Dust-Devil procs are separate mobile whorls; if they carry red chroma
    at all they arrive as their OWN components, spatially detached.  So the
    split available to a connectivity-only instrument is:

        CORE  = largest component
        AUX   = every other component  (dust-devil candidates + spill)

    ⚑ WHAT THIS CANNOT DO -- stated, because the brief asks for a
    separability verdict and a verdict has to carry its limit: a dust devil
    that OVERLAPS the core disc in image space is absorbed into the largest
    component and is not separable by connectivity.  The number below
    therefore bounds DETACHED dust-devil contribution, not dust-devil
    contribution.  Same limit R-27 § R1 recorded for discrete elements.
    """
    if not sz.size:
        return None, None, {}
    j = int(np.argmax(sz))
    core = lab == (j + 1)
    aux = (lab > 0) & ~core
    return core, aux, {
        "core_px": int(sz[j]),
        "aux_px": int(aux.sum()),
        "aux_n_components": int(sz.size - 1),
        "aux_share_of_effect": float(aux.sum() / max(sz.sum(), 1)),
        "runner_up_px": int(np.sort(sz)[-2]) if sz.size > 1 else 0,
        "core_to_runner_up": float(sz[j] / max(np.sort(sz)[-2], 1)) if sz.size > 1 else float("inf"),
    }


def palette_region(hh, C, L, region, M_tight):
    """Region for the PALETTE question, selected WITHOUT using hue.

    ⚑ The tight mask selects on hue, so a hue histogram over it is circular by
    construction -- it can only ever report hues inside [340,20).  (The smoke
    run did exactly that: p10/p50/p90 = 10.5 / 14.9 / 17.5 deg, i.e. the mask's
    own window, reported as though it were a measurement of the effect.)

    So the palette is measured over a CHROMA-ONLY selection -- C > floor, no
    hue test at all -- restricted to the connected components that overlap the
    tight mask.  Hue is then free to land wherever the effect actually is, and
    the only thing that chose the pixels is "this is a chromatic part of the
    thing the tight mask found".
    """
    raw = (C > C_FLOOR) & (L > L_FLOOR) & region
    M, lab, sz = coherent(raw)
    M, lab, sz, _ = drop_bar_shaped(M, lab, sz)
    if not sz.size:
        return np.zeros_like(M)
    hit = np.unique(lab[M_tight & (lab > 0)])
    return np.isin(lab, hit[hit > 0]) if hit.size else np.zeros_like(M)


def palette(f, M, nbins=72):
    """DESCRIPTIVE ONLY (never an anchor -- Tier-1: the instance does not
    transfer).  L-weighted hue histogram over the effect region + the region's
    dominant RGB triplets."""
    if M.sum() < 40:
        return None
    hh, s = hue_sat(f)
    L = luma(f)
    hv, Lv, sv = hh[M], L[M], s[M]
    H = np.zeros(nbins)
    np.add.at(H, np.clip((hv / (360.0 / nbins)).astype(int), 0, nbins - 1), Lv)
    H = H / max(H.sum(), 1)
    hw = np.where(hv > 180, hv - 360, hv)
    q = (f[M].astype(int) // 32) * 32 + 16
    key = q[:, 0] * 65536 + q[:, 1] * 256 + q[:, 2]
    u, cnt = np.unique(key, return_counts=True)
    o = np.argsort(cnt)[::-1][:5]
    return {
        "hue_hist_L_weighted": H.round(5).tolist(),
        "hue_bin_deg": 360.0 / nbins,
        "hue_p10": float(np.percentile(hw, 10)), "hue_p50": float(np.median(hw)),
        "hue_p90": float(np.percentile(hw, 90)),
        "S_p50": float(np.median(sv)), "L_p50": float(np.median(Lv)),
        "top_rgb_quantised": [[int(u[k] // 65536), int((u[k] // 256) % 256), int(u[k] % 256),
                               round(float(cnt[k] / cnt.sum()), 4)] for k in o],
    }


# ===========================================================================
def prep(f):
    """Per-frame arrays shared by BOTH arms (raw and UI-masked), so the two
    arms are guaranteed to be reading identical pixels and the run costs one
    decode + one clutter pass rather than two."""
    L = luma(f)
    sA, _ = sat_val(f)
    hh, _ = hue_sat(f)
    C = chroma(f)
    clutter, _, _ = clutter_mask(f, L, sA, hh, C)
    return L, sA, hh, C, clutter


def measure_frame(f, V, HUD, use_clutter, c_floor=C_FLOOR, hue_hi=HUE_HI,
                  l_floor=L_FLOOR, close_radius=CLOSE_RADIUS, want_palette=False,
                  pre=None):
    L, sA, hh, C, clutter_all = pre if pre is not None else prep(f)

    region = V & ~HUD
    clutter = None
    if use_clutter:
        clutter = clutter_all
        region = region & ~clutter

    E, lab, sz, bar_px = eff_tight(hh, C, L, region, hue_hi=hue_hi, c_floor=c_floor, l_floor=l_floor)
    SUP = eff_support(E, close_radius)
    core, aux, dd = dust_devil_split(lab, sz, L)

    valid = region                       # ownership denominator = the scene
    st = region_stats(E, L, sA)
    ss = region_stats(SUP, L, sA)
    ow, top = ownership(E, L, valid)
    row = {"tight": st, "support": ss, "ownership": ow,
           "largest_px": int(sz.max()) if sz.size else 0,
           "n_components": int(sz.size),
           "bar_shaped_px_dropped": int(bar_px)}
    if clutter is not None:
        row["clutter_px"] = int(clutter.sum())
    if core is not None:
        cs = region_stats(core, L, sA)
        co, _ = ownership(core, L, valid)
        row["core"] = {"ratio": cs["ratio"], "midS": cs["midS"], "area": cs["area"],
                       "own": co["own"]}
        if aux.sum() >= 40:
            as_ = region_stats(aux, L, sA)
            row["aux"] = {"ratio": as_["ratio"], "midS": as_["midS"], "area": as_["area"]}
        row["dust_devil_split"] = dd
    # SPATIAL FLOOR (negative control 2): scene outside a 25 px dilation of
    # the effect's support.  Same instrument, pointed at the room.
    NE = region & ~ndimage.binary_dilation(SUP, np.ones((SPATIAL_FLOOR_DILATE,) * 2))
    fs = region_stats(NE, L, sA)
    fo, _ = ownership(NE, L, valid)
    row["spatial_floor"] = {"ratio": fs["ratio"], "midS": fs["midS"],
                            "area": fs["area"], "own": fo["own"]}
    row["decomposition"] = decompose(E, lab, sz, top) if sz.size else {}
    if want_palette:
        PR = palette_region(hh, C, L, region, E)
        row["palette"] = palette(f, PR)                    # hue FREE (de-circularised)
        row["palette_hue_selected"] = palette(f, E)        # hue-selected, for contrast
        row["palette_region_px"] = int(PR.sum())
    row["_top_tail_share_of_self"] = (
        float((top & E).sum()) / max(int(E.sum()), 1) if E.sum() else 0.0)
    return row


ACC_KEYS = ("tight_ratio", "tight_midS", "tight_area", "supp_ratio", "supp_midS",
            "core_ratio", "core_midS", "core_area", "core_own",
            "aux_ratio", "aux_midS", "aux_area",
            "own", "own_rank", "clipped_frac",
            "floor_ratio", "floor_midS", "floor_own",
            "lift_ratio", "lift_midS", "lift_own",
            "share_of_self", "largest_px", "n_components", "clutter_px", "bar_px",
            "aux_share", "core_to_runner_up",
            "disc_top_share_500", "largest_top_share")


def accumulate(rows):
    acc = {k: [] for k in ACC_KEYS}
    for r in rows:
        acc["tight_ratio"].append(r["tight"]["ratio"])
        acc["tight_midS"].append(r["tight"]["midS"])
        acc["tight_area"].append(r["tight"]["area"])
        acc["supp_ratio"].append(r["support"]["ratio"])
        acc["supp_midS"].append(r["support"]["midS"])
        acc["own"].append(r["ownership"]["own"])
        acc["own_rank"].append(r["ownership"]["own_rank"])
        acc["clipped_frac"].append(r["ownership"]["clipped_frac"])
        acc["largest_px"].append(r["largest_px"])
        acc["n_components"].append(r["n_components"])
        acc["share_of_self"].append(r["_top_tail_share_of_self"])
        if "clutter_px" in r:
            acc["clutter_px"].append(r["clutter_px"])
        acc["bar_px"].append(r.get("bar_shaped_px_dropped", 0))
        f = r["spatial_floor"]
        acc["floor_ratio"].append(f["ratio"])
        acc["floor_midS"].append(f["midS"])
        acc["floor_own"].append(f["own"])
        if np.isfinite(f["ratio"]) and f["ratio"] > 1e-6 and np.isfinite(r["tight"]["ratio"]):
            acc["lift_ratio"].append(r["tight"]["ratio"] / f["ratio"])
        if np.isfinite(f["midS"]) and f["midS"] > 1e-6 and np.isfinite(r["tight"]["midS"]):
            acc["lift_midS"].append(r["tight"]["midS"] / f["midS"])
        if f["own"] > 1e-9:
            acc["lift_own"].append(r["ownership"]["own"] / f["own"])
        if "core" in r:
            acc["core_ratio"].append(r["core"]["ratio"])
            acc["core_midS"].append(r["core"]["midS"])
            acc["core_area"].append(r["core"]["area"])
            acc["core_own"].append(r["core"]["own"])
            acc["aux_share"].append(r["dust_devil_split"]["aux_share_of_effect"])
            acc["core_to_runner_up"].append(r["dust_devil_split"]["core_to_runner_up"])
        if "aux" in r:
            acc["aux_ratio"].append(r["aux"]["ratio"])
            acc["aux_midS"].append(r["aux"]["midS"])
            acc["aux_area"].append(r["aux"]["area"])
        d = r.get("decomposition") or {}
        if "discrete_by_threshold" in d:
            acc["disc_top_share_500"].append(
                d["discrete_by_threshold"]["lt_500_px"]["top_tail_share_of_effect"])
            acc["largest_top_share"].append(d["top_tail_share_largest_of_effect"])
    return {k: agg(v) for k, v in acc.items() if v}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clip", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--stride", type=int, default=6)
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--evidence")
    a = ap.parse_args()

    w, h, fps, codec, pix = probe(a.clip)
    V = valid_map(h, w)
    HUD = hud_map(h, w)

    res = {
        "artifact": a.clip, "tag": a.tag, "sha256": sha256(a.clip),
        "video": {"w": w, "h": h, "fps": fps, "codec": codec, "pix_fmt": pix},
        "supersedes": {"pass": "R-27 / R-25 A-1",
                       "wrong_referent_sha256": "855bb3d9c7edca8b372869e667682eda6de85ea813628377e567522d9e998637",
                       "reason": "charter R-28 -- referent identity defect"},
        "black_masks": [{"name": n, "x": x, "y": y, "w": ww, "h": hh} for n, x, y, ww, hh in BLACK_MASKS],
        "hud_boxes": [{"name": n, "x": x, "y": y, "w": ww, "h": hh, "derivation": d}
                      for n, x, y, ww, hh, d in HUD_BOXES],
        "coverage": {"valid_frac": float(V.mean()),
                     "hud_frac_of_valid": float((HUD & V).sum() / V.sum()),
                     "scene_frac_of_frame": float((V & ~HUD).mean())},
        "instrument": {"hue_sector_deg": [HUE_LO, HUE_HI], "chroma_floor": C_FLOOR,
                       "l_floor": L_FLOOR, "close_radius": CLOSE_RADIUS,
                       "min_component_px": MIN_COMPONENT_PX, "top_frac": TOP_FRAC,
                       "midband_percentiles": list(MIDBAND),
                       "burst_px": BURST_PX, "null_px": NULL_PX,
                       "stride": a.stride,
                       "statistics_imported_from": "vfx_ref_anchor <- vfx_lap2_battery"},
        "ours_lap2_denominators": OURS_LAP2,
    }

    ev = Path(a.evidence) if a.evidence else None
    if ev:
        ev.mkdir(parents=True, exist_ok=True)

    rows_raw, rows_msk, frame_idx = [], [], []
    pal_frames = []
    for i, f in frames(a.clip, w, h, stride=a.stride):
        pre = prep(f)
        r_raw = measure_frame(f, V, np.zeros_like(HUD), False, want_palette=False, pre=pre)
        r_msk = measure_frame(f, V, HUD, True, want_palette=True, pre=pre)
        r_raw["frame"] = r_msk["frame"] = i
        rows_raw.append(r_raw)
        rows_msk.append(r_msk)
        frame_idx.append(i)
        if r_msk["largest_px"] >= BURST_PX and len(pal_frames) < 400:
            pal_frames.append((i, r_msk.get("palette"), r_msk.get("palette_hue_selected")))

    big = np.array([r["largest_px"] for r in rows_msk])
    burst = np.nonzero(big >= BURST_PX)[0]
    nullw = np.nonzero(big <= NULL_PX)[0]
    res["phases"] = {
        "n_sampled": len(rows_msk),
        "burst_frames": int(burst.size), "null_frames": int(nullw.size),
        "burst_frac": float(burst.size / max(len(rows_msk), 1)),
        "null_frac": float(nullw.size / max(len(rows_msk), 1)),
        "burst_frame_indices": [frame_idx[k] for k in burst],
        "null_frame_indices": [frame_idx[k] for k in nullw],
        "definition": "largest red-chroma component >= %d px (BURST) / <= %d px (NULL); "
                      "the presence statistic is NOT one of the three anchored statistics"
                      % (BURST_PX, NULL_PX),
    }

    res["windows"] = {}
    for name, sel in (("burst", burst), ("null", nullw), ("all", np.arange(len(rows_msk)))):
        if not len(sel):
            continue
        res["windows"][name] = {
            "ui_masked": accumulate([rows_msk[k] for k in sel]),
            "raw_no_ui_masking": accumulate([rows_raw[k] for k in sel]),
        }

    # ---- palette over burst frames --------------------------------------
    if pal_frames:
        HH = np.zeros(72)
        HHc = np.zeros(72)
        hp = []
        for _, p, pc in pal_frames:
            if p:
                HH += np.array(p["hue_hist_L_weighted"])
                hp.append((p["hue_p10"], p["hue_p50"], p["hue_p90"], p["S_p50"], p["L_p50"]))
            if pc:
                HHc += np.array(pc["hue_hist_L_weighted"])

        hp = np.array(hp)
        res["palette_burst"] = {
            "n_frames": len(pal_frames),
            "hue_hist_L_weighted_effect": (HH / max(HH.sum(), 1)).round(5).tolist(),
            "hue_hist_L_weighted_hue_selected_CIRCULAR": (HHc / max(HHc.sum(), 1)).round(5).tolist(),
            "hue_bin_deg": 5.0,
            "hue_p10_median": float(np.median(hp[:, 0])),
            "hue_p50_median": float(np.median(hp[:, 1])),
            "hue_p90_median": float(np.median(hp[:, 2])),
            "S_p50_median": float(np.median(hp[:, 3])),
            "L_p50_median": float(np.median(hp[:, 4])),
            "top_rgb_quantised_last_frame": pal_frames[-1][1]["top_rgb_quantised"] if pal_frames[-1][1] else None,
            "STAMP": "DESCRIPTIVE ONLY -- Tier-1: the instance does not transfer",
        }

    # ---- sweeps ----------------------------------------------------------
    if a.sweep and burst.size:
        sel = [frame_idx[k] for k in burst]
        pick = set(np.array(sel)[np.linspace(0, len(sel) - 1, min(12, len(sel))).astype(int)].tolist())
        sw = {"chroma_floor": [], "hue_hi": [], "l_floor": [], "close_radius": []}
        cache = {}
        for i, f in frames(a.clip, w, h, stride=1):
            if i in pick:
                cache[i] = f
            if len(cache) == len(pick):
                break
        pc = {i: prep(f) for i, f in cache.items()}
        for cval in (0.15, 0.20, 0.25, 0.30, 0.35, 0.45, 0.55):
            rr = [measure_frame(f, V, HUD, True, c_floor=cval, pre=pc[i]) for i, f in cache.items()]
            A_ = accumulate(rr)
            sw["chroma_floor"].append({"c_floor": cval,
                                       "ratio": A_["tight_ratio"]["median"],
                                       "midS": A_["tight_midS"]["median"],
                                       "area": A_["tight_area"]["median"],
                                       "own": A_["own"]["median"]})
        for hv in (12.0, 16.0, 20.0, 25.0, 30.0, 40.0):
            rr = [measure_frame(f, V, HUD, True, hue_hi=hv, pre=pc[i]) for i, f in cache.items()]
            A_ = accumulate(rr)
            sw["hue_hi"].append({"hue_hi": hv, "ratio": A_["tight_ratio"]["median"],
                                 "midS": A_["tight_midS"]["median"],
                                 "area": A_["tight_area"]["median"]})
        for lv in (0.0, 0.05, 0.10, 0.15, 0.20):
            rr = [measure_frame(f, V, HUD, True, l_floor=lv, pre=pc[i]) for i, f in cache.items()]
            A_ = accumulate(rr)
            sw["l_floor"].append({"l_floor": lv, "ratio": A_["tight_ratio"]["median"],
                                  "midS": A_["tight_midS"]["median"],
                                  "area": A_["tight_area"]["median"]})
        for rv in (3, 5, 9, 15, 25):
            rr = [measure_frame(f, V, HUD, True, close_radius=rv, pre=pc[i]) for i, f in cache.items()]
            A_ = accumulate(rr)
            sw["close_radius"].append({"close_radius": rv,
                                       "supp_ratio": A_["supp_ratio"]["median"],
                                       "supp_midS": A_["supp_midS"]["median"]})
        res["sweeps"] = sw

    # ---- ALTERNATIVE SEGMENTATION FORMS + DILATION LADDER ----------------
    # The (b) conclusion is the one that moves most between referents, so it
    # is reported on every region this pass can construct -- including R-27's
    # own S-floor form -- rather than on the adopted one alone.
    if burst.size:
        sel = [frame_idx[k] for k in burst]
        pick = set(np.array(sel)[np.linspace(0, len(sel) - 1, min(10, len(sel))).astype(int)].tolist())
        forms = {k: [] for k in ("chroma_035_adopted", "chroma_020", "R27form_S035",
                                 "R27form_S035_hue30")}
        ladder = {d: [] for d in (0, 5, 10, 20, 40)}
        floors = []
        for i, f in frames(a.clip, w, h, stride=1):
            if i not in pick:
                continue
            L, sA, hh, C, cl = prep(f)
            reg = V & ~HUD & ~cl
            red = (hh < HUE_HI) | (hh >= HUE_LO)
            cand = {
                "chroma_035_adopted": red & (C > 0.35) & (L > L_FLOOR),
                "chroma_020": red & (C > 0.20) & (L > L_FLOOR),
                "R27form_S035": red & (sA > 0.35) & (L > L_FLOOR),
                "R27form_S035_hue30": ((hh < 30) | (hh >= HUE_LO)) & (sA > 0.35) & (L > L_FLOOR),
            }
            base_sup = None
            for nm, raw in cand.items():
                M, lab, sz = coherent(raw & reg)
                M, lab, sz, _ = drop_bar_shaped(M, lab, sz)
                st = region_stats(M, L, sA)
                forms[nm].append((st["area"], st["ratio"], st["midS"]))
                if nm == "chroma_035_adopted":
                    base_sup = eff_support(M)
            for d in ladder:
                Rg = (ndimage.binary_dilation(base_sup, np.ones((2 * d + 1,) * 2)) & reg) if d else (base_sup & reg)
                ladder[d].append(region_stats(Rg, L, sA)["ratio"])
            NE = reg & ~ndimage.binary_dilation(base_sup, np.ones((SPATIAL_FLOOR_DILATE,) * 2))
            fs = region_stats(NE, L, sA)
            floors.append((fs["ratio"], fs["midS"]))
            if len(floors) == len(pick):
                break
        res["segmentation_forms"] = {
            "n_frames": len(floors),
            "forms": {nm: {"area_median": float(np.median([v[0] for v in vals])),
                           "ratio_median": float(np.nanmedian([v[1] for v in vals])),
                           "midS_median": float(np.nanmedian([v[2] for v in vals]))}
                      for nm, vals in forms.items() if vals},
            "dilation_ladder_ratio": {("support+%d" % d): float(np.nanmedian(v))
                                      for d, v in ladder.items() if v},
            "scene_floor": {"ratio_median": float(np.nanmedian([v[0] for v in floors])),
                            "midS_median": float(np.nanmedian([v[1] for v in floors]))},
            "note": "R27form_S035_hue30 selects ~300-400 kpx (a third of the frame) on "
                    "this referent and is reported as INADMISSIBLE, not as an estimate.",
        }

    # ---- per-frame series (compact) --------------------------------------
    res["series"] = {
        "frame": frame_idx,
        "largest_px": big.tolist(),
        "tight_ratio": [round(r["tight"]["ratio"], 4) if np.isfinite(r["tight"]["ratio"]) else None for r in rows_msk],
        "tight_midS": [round(r["tight"]["midS"], 4) if np.isfinite(r["tight"]["midS"]) else None for r in rows_msk],
        "own": [round(r["ownership"]["own"], 4) for r in rows_msk],
        "clutter_px": [r.get("clutter_px", 0) for r in rows_msk],
    }

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(res, indent=1))

    # ---- print -----------------------------------------------------------
    def show(win, arm):
        s = res["windows"][win][arm]
        def g(k):
            v = s.get(k)
            return v["median"] if v else float("nan")
        n = s["tight_ratio"]["n"] if s.get("tight_ratio") else 0
        print("  %-6s %-18s n=%-4d TIGHT ratio %6.3f midS %6.4f own %6.4f | SUPP ratio %6.3f midS %6.4f | floor %6.3f / %6.4f / %6.4f | LIFT %6.3fx / %6.3fx / %6.2fx"
              % (win, arm, n, g("tight_ratio"), g("tight_midS"), g("own"),
                 g("supp_ratio"), g("supp_midS"),
                 g("floor_ratio"), g("floor_midS"), g("floor_own"),
                 g("lift_ratio"), g("lift_midS"), g("lift_own")))

    print("[%s] %s  n=%d sampled  BURST %d (%.3f)  NULL %d (%.3f)"
          % (a.tag, res["sha256"][:12], len(rows_msk), burst.size,
             burst.size / len(rows_msk), nullw.size, nullw.size / len(rows_msk)))
    print("  HUD covers %.3f of valid; scene = %.3f of frame"
          % (res["coverage"]["hud_frac_of_valid"], res["coverage"]["scene_frac_of_frame"]))
    for win in ("burst", "null", "all"):
        if win in res["windows"]:
            for arm in ("ui_masked", "raw_no_ui_masking"):
                show(win, arm)
    if "burst" in res["windows"]:
        s = res["windows"]["burst"]["ui_masked"]
        if "core_ratio" in s:
            print("  CORE (largest comp only)  ratio %.3f  midS %.4f  area %.0f  own %.4f"
                  % (s["core_ratio"]["median"], s["core_midS"]["median"],
                     s["core_area"]["median"], s["core_own"]["median"]))
        if "aux_ratio" in s:
            print("  AUX  (detached comps)     ratio %.3f  midS %.4f  area %.0f  share %.4f  core/runner-up %.1fx"
                  % (s["aux_ratio"]["median"], s["aux_midS"]["median"], s["aux_area"]["median"],
                     s["aux_share"]["median"], s["core_to_runner_up"]["median"]))
        if "share_of_self" in s:
            print("  share-of-self (top-tail px / effect area)  %.4f   [ours lap-2: %.4f]"
                  % (s["share_of_self"]["median"], OURS_LAP2["top_tail_share_of_self"]))
    if "palette_burst" in res:
        p = res["palette_burst"]
        print("  PALETTE (descriptive) hue p10/p50/p90 %.1f / %.1f / %.1f deg   S %.3f  L %.3f"
              % (p["hue_p10_median"], p["hue_p50_median"], p["hue_p90_median"],
                 p["S_p50_median"], p["L_p50_median"]))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
