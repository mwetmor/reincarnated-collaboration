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
from vfx_lap2_project import (GroundCam, attribute_identity, parse_pin,  # noqa: E402
                              read_lap2_n, read_selfcheck, zone_masks)

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
    # ⚑ T3a_dominance is SUPERSEDED. Kept named for lineage only; no row reads it.
    # It was the ratio-to-an-annular-floor statistic that read 4.07x on the render
    # its own spec line called "currently < 1.0" (galadriel 809409a8, sec 3.1 of the
    # notes). gandalf re-cut the criterion 2026-08-25 (spec 168dbe44) to FRAME-
    # LUMINANCE OWNERSHIP, below.
    "T3a_dominance_SUPERSEDED": 2.2,
    "T3a_ownership": 0.75,      # effect region owns >= 75% of frame top-0.5% L pixels
    "T3a_top_frac": 0.005,      # "top-0.5% luminance pixels", UI excluded
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

# --- lap-2 amendments, each traceable to a conductor ruling -----------------
# R-24 #2 -- T-1's return leg is re-indexed from FIRST contact to FINAL contact.
#            The first-contact indexing was unsatisfiable beside the spec's own
#            0.35 s refractory: at ~5 re-strikes per mob, first-contact + 1.0 s
#            lands MID-FLINCH from a later strike.
T1_RETURN_FROM_FINAL_CONTACT = True
# R-24 #10 -- the "zero residue pixels" leg may NOT be evaluated at |dL| > 0.02:
#            3,850 px differ at that threshold on CONTENT-IDENTICAL frames
#            (separately-encoded h264 arms). See `residue_instrument()`.
T2_COHERENCE_MIN_PX = 12      # a residue quantum is a blob; codec noise is isolated
T2_CLEAR_MIN_PX = 0           # "zero", evaluated by the coherence-gated instrument
# The mobs are STATIC in world space; the CASTER translates and the player_lock
# camera dollies with him, so every mob's IMAGE position moves by parallax from
# t = MOVE_FROM. Read from `wwcr_stage.gd` rather than fitted:
STAGE_MOVE_FROM_S = 2.20
STAGE_MOVE_SPEED_MS = 3.5
STAGE_T_RELEASE_S = 2.60
STAGE_MOVE_DIR = (-1.0, 0.0)   # Vector3(-1,0,0).normalized(), XZ components

ANG_BINS = 180          # 2 deg per bin around the caster
MIN_COMPONENT_PX = 12   # below this a component is decoder speckle, not content
MIN_UI_COMPONENT_PX = 64  # a HUD element is contiguous; a 1-px static speck is not
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

def measure(on_path, ctl_path, geo, w, h, fps, n_frames, track=None, ident=None):
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
    # ⚑ RIBBON ZONE. Lap-1's effect region WAS the arc; lap-2's is the arc plus
    # 60 shed quanta plus residue on three mobs plus 36 floor scour marks. Any
    # criterion whose text says "the ARC" (T-3d's angular extent) or "the
    # ribbon's value range" (T-3b/c) needs the arc separated from the debris, or
    # the operand silently changes meaning between laps. Measured consequence
    # of NOT separating: T-3d's "arc angular extent" reads 313 deg on a 150 deg
    # arc. The two continuous tinted families are blade-generated and live
    # inside R_TRAIL = 2.3598 m < R_ENGAGE, so a radius gate about the caster
    # separates them from everything discrete that has been thrown outward.
    ribbon_zone = rad <= 0.80 * r_out
    # ⚑ ROIs TRACK. The seeded ROI is correct only while the camera is where it
    # was at frame 0. Under the caster-travel dolly a mob's image position moves
    # up to ~100 px, so a static ROI stops containing the mob it is named for --
    # silently, reporting whatever floor happens to be inside the old box. The
    # per-frame offset is the ANALYTIC parallax of that mob's fixed world point.
    roi_off = {}
    for m in mobs:
        wxz = (ident or {}).get("world_of", {}).get(m["id"])
        roi_off[m["id"]] = (track.offsets(wxz) if (track and wxz) else
                            [(0.0, 0.0)] * n_frames)

    # ⚑ ZONES FROM THE VENUE'S METRES, NOT FROM THE MASK'S OWN RADIUS. See
    # `vfx_lap2_project.zone_masks`. Without a pin the battery falls back to the
    # lap-1 mask-derived rings, so the negative control stays comparable.
    trail_zone = ribbon_zone
    if ident is not None:
        tz, fz = ident["zones"]
        trail_zone, floor_ring = tz, fz
    # T-6's floor region: the union of the engagement annulus over the caster's
    # whole track. With no track supplied this collapses to the static ring,
    # which is what lap-1 measured -- so the negative control is comparable.
    floor_zone = floor_ring.copy()
    if track is not None:
        for i in range(0, n_frames, 4):
            p = track.cams[i].project([0.0, 0.0, 0.0])
            p0 = track.cams[0].project([0.0, 0.0, 0.0])
            if p is None or p0 is None:
                continue
            ddx, ddy = int(round(p[0] - p0[0])), int(round(p[1] - p0[1]))
            floor_zone |= np.roll(np.roll(floor_ring, ddy, 0), ddx, 1)

    def roi_at(m, i):
        dx, dy = roi_off[m["id"]][min(i, len(roi_off[m["id"]]) - 1)]
        x0, y0, x1, y1 = m["roi"]
        ox, oy = int(round(dx)), int(round(dy))
        return (max(0, x0 + ox), max(0, y0 + oy),
                min(w - 1, x1 + ox), min(h - 1, y1 + oy))

    # ⚑ THE CASTER IS EXCLUDED FROM EVERY MOB SILHOUETTE, and LOOKING is what
    # found it. Mob3's centroid read 16.8 px from rest 1.0 s after its final
    # contact -- a textbook "the impulse left a persistent displacement", and I
    # was one paragraph from reporting it as one. The crop says otherwise: the
    # caster WALKS INTO Mob3's ROI (he travels 1.40 m in -X from t = 2.20) and
    # his silhouette merges with Mob3's under the same luma gate, dragging the
    # centroid toward him. He is FIXED in image space -- the player_lock camera
    # dollies with him, which is the whole point of the pin -- so one fixed box
    # removes him from every ROI at every frame.
    cbb = (geo.get("caster_roi") or {}).get("bbox")
    caster_mask = np.zeros((h, w), bool)
    if cbb:
        cpad = 18
        caster_mask[max(0, cbb[1] - cpad):min(h, cbb[3] + cpad + 1),
                    max(0, cbb[0] - cpad):min(w, cbb[2] + cpad + 1)] = True

    A = Stream(on_path, w, h)
    B = Stream(ctl_path, w, h)
    S = {k: [] for k in (
        "area", "p99_on", "p95_on", "p50_on", "p20_on", "midS", "scene_med", "ncomp",
        "comp_iqr_med", "peak_bin", "arc_lo", "arc_hi", "mean_ang", "sum_lift",
        "floor_area", "floor_dl", "castlift_floor", "castlift_mob", "residue_total",
        "p95_rib", "p20_rib", "midS_rib", "dark_area", "castfrac_floor",
        "area_core", "area_rib", "rib_span_deg")}
    per_mob = {m["id"]: {"cen": [], "cen_ctl": [], "axis": [], "residue": [],
                         "residue_raw": [], "roi": []} for m in mobs}
    width_profiles = []
    on0L = ctl0L = None
    mob_any = np.zeros((h, w), bool)

    for i in range(n_frames):
        fa, fb = A.read(), B.read()
        if fa is None or fb is None:
            break
        La, Lb = luma(fa), luma(fb)
        if on0L is None:
            on0L, ctl0L = La.copy(), Lb.copy()
        mob_any[:] = False
        for m in mobs:
            x0, y0, x1, y1 = roi_at(m, i)
            mob_any[y0:y1 + 1, x0:x1 + 1] = True
        d = La - Lb
        # ⚑ SIGNED, NOT ABSOLUTE -- and this is the defect drax found in his own
        # instrument three passes before I met it in mine (record sec 6, T-3
        # defect 2: "It stayed invisible for three passes because I masked the
        # effect region with |dL|"). T-6 lands 36 FloorScour marks that make the
        # tile DARKER, and they never expire. Under |dL| they enter the "effect
        # region" and stay in it: they inflate T-4a's sustain-mean denominator,
        # they hold T-4c's area up after the ribbon is gone, they add components
        # to T-5a's census, and -- worst -- they drag T-3b's P20 down, which
        # INFLATES the P95/P20 ratio the criterion is trying to measure on the
        # ribbon. A darkening treatment must not be allowed to score a
        # brightness criterion. Every "luminous area" row now reads the
        # BRIGHTENING mask; the darkening mask is kept separately and is T-6's.
        E = ndimage.binary_opening(d > tau, np.ones((3, 3)))
        Dk = ndimage.binary_opening(-d > tau, np.ones((3, 3)))
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
        S["dark_area"].append(int(Dk.sum()))
        # --- family split: what touches the ribbon zone is the ribbon --------
        # A blade-generated continuous surface is connected back into the
        # annulus; a thrown quantum and an attached residue curl are not. This
        # is the ONE separation the frames can carry, and it is the same one the
        # T-3a decomposition uses, so the scorecard means one thing by "arc".
        # RIBBON = brightening OR DARKENING inside the projected trail torus.
        # ⚑ The darkening half is not optional: `TrailRibbonBody` is MIX and is
        # SPECIFIED to darken as it ages (spec T-3), and drax took its V from
        # 0.34 to 0.16 precisely so it lands BELOW the measured floor luma. A
        # brightening-only ribbon mask would drop the dark tail -- the exact
        # half of the two-surface split T-3 exists to buy -- and then report
        # T-3b's range as short because it could not see the bottom of it.
        # The T-6 scour is also a darkening, but it lies on the ground at
        # R_ENGAGE = 3.515 m, outside the R_TRAIL = 2.3598 m torus, so the zone
        # separates them without either treatment scoring the other's criterion.
        RIB = ndimage.binary_opening((E | Dk) & trail_zone, np.ones((3, 3)))
        DEB = E & ~RIB

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
        # ⚑ SECOND SEGMENTATION, reported beside the first, never instead of it.
        # R-24 #8 says my segmentation governs on T-3(b)/(c) and drax's mask
        # (which includes cast-lit floor) drags both down on his. Mine would
        # include cast-lit floor AND 60 shed quanta AND three mobs' residue. But
        # T-3(b)/(c) are TREATMENT-level criteria about the two-surface ribbon
        # -- R-23 took the lap-level question out of T-3 and put it in (a). So
        # both numbers are computed and both are reported, and the conductor
        # adjudicates on the pair rather than on whichever mask I preferred.
        if RIB.sum() >= 40:
            v = La[RIB]
            S["p95_rib"].append(float(np.percentile(v, 95)))
            S["p20_rib"].append(float(np.percentile(v, 20)))
            sA, _ = sat_val(fa)
            lo, hi = np.percentile(v, [35, 65])
            mid = RIB & (La >= lo) & (La <= hi)
            S["midS_rib"].append(float(sA[mid].mean()) if mid.sum() else float("nan"))
        else:
            for kk in ("p95_rib", "p20_rib", "midS_rib"):
                S[kk].append(float("nan"))
        sc = scene_ring & ~E & ~Dk & ~mob_any
        S["scene_med"].append(float(np.median(La[sc])) if sc.sum() else float("nan"))

        # --- T-3d apex-vs-leading-edge, T-5b width profile ------------------
        # ⚑ On the RIBBON, not on the whole effect region. "The leading 25% of
        # the ARC's angular extent" is a statement about the arc; measured on
        # the composed region it reads a 313 deg "arc" and the criterion stops
        # meaning what it says.
        if RIB.sum() >= 40:
            b = abin[RIB]
            occ = np.bincount(b, minlength=ANG_BINS)
            pk = np.zeros(ANG_BINS, np.float32)
            np.maximum.at(pk, b, La[RIB])
            S["peak_bin"].append(int(np.argmax(pk)))
            live = np.nonzero(occ > 0)[0]
            lo_b, hi_b = arc_span(occ)
            S["arc_lo"].append(lo_b)
            S["arc_hi"].append(hi_b)
            ca = np.cos(np.radians(ang[RIB])).mean()
            sa = np.sin(np.radians(ang[RIB])).mean()
            S["mean_ang"].append(float(np.degrees(np.arctan2(sa, ca))))
            wp = np.zeros(ANG_BINS, np.float32)
            rr = rad[RIB]
            for bb in live:
                sel = rr[b == bb]
                wp[bb] = float(sel.max() - sel.min())
            width_profiles.append(wp)
        else:
            for kk in ("peak_bin", "arc_lo", "arc_hi", "mean_ang"):
                S[kk].append(float("nan"))
            width_profiles.append(np.zeros(ANG_BINS, np.float32))

        # --- T-3e cast light on non-effect surfaces -------------------------
        # ⚑ THE OLD MASK CARRIED `& ~E` AND THAT IS THE WHOLE DEFECT. E is the
        # brightening mask; floor lit by the arc IS brightened; so the row
        # excluded precisely the pixels that demonstrate cast light and reported
        # 0.000 lift on a build whose own arc light pools visibly on the tile.
        # It read 0.000 at lap-1 too, and correctly -- nothing lit anything --
        # which is exactly how a mask that cannot see the effect survives a
        # negative control. Sixth instance this run.
        #
        # "Non-effect SURFACE" means a surface that is not the effect's own
        # geometry, not a surface the effect fails to light. The separation is
        # the same emissive-core test the T-3a misattribution guard uses:
        # a pixel where the effect supplies the MAJORITY of its own luminance is
        # the effect's geometry; a pixel merely lifted is lit scenery.
        core = (d >= 0.5 * np.maximum(La, 1e-6)) & (d > tau)
        fl = floor_zone & ~core & ~Dk & ~mob_any
        if fl.sum():
            fr = d[fl] / np.maximum(Lb[fl], 1e-6)
            S["castlift_floor"].append(float(np.percentile(fr, 90)))
            S["castfrac_floor"].append(float((fr >= BARS["T3e_lift_frac"]).mean()))
        else:
            S["castlift_floor"].append(float("nan"))
            S["castfrac_floor"].append(float("nan"))
        mk = mob_any & ~core & ~Dk
        S["castlift_mob"].append(
            float(np.percentile(d[mk] / np.maximum(Lb[mk], 1e-6), 90))
            if mk.sum() else float("nan"))
        S["area_core"].append(int(core.sum()))
        S["area_rib"].append(int(((E | Dk) & trail_zone).sum()))

        # --- T-1 per-mob kinematics, T-2 per-mob residue --------------------
        tot_res = 0
        for m in mobs:
            x0, y0, x1, y1 = roi_at(m, i)
            per_mob[m["id"]]["roi"].append([x0, y0, x1, y1])
            sub = La[y0:y1 + 1, x0:x1 + 1]
            subc = Lb[y0:y1 + 1, x0:x1 + 1]
            # ⚑ ABSOLUTE image coords, not ROI-local. The ROI itself moves with
            # the parallax track, so a ROI-local centroid would silently
            # subtract the very motion the return leg has to see through.
            notc = ~caster_mask[y0:y1 + 1, x0:x1 + 1]
            sil = (sub > 0.27) & notc
            if sil.sum() >= 60:
                c = centroid_axis(sil)
                per_mob[m["id"]]["cen"].append((c[0] + x0, c[1] + y0, c[2]))
            else:
                per_mob[m["id"]]["cen"].append((float("nan"),) * 3)
            # ⚑ The CONTROL arm carries the flinch too -- T-1 lands in
            # `wwcr_stage.gd` and fires on the contact signal regardless of vfx
            # visibility (both arms log contacts=15). So the control arm is the
            # mob's kinematics WITHOUT the effect painted on the silhouette:
            # the cleaner T-1 measurement, and an independent cross-check.
            silc = (subc > 0.27) & notc
            if silc.sum() >= 60:
                c = centroid_axis(silc)
                per_mob[m["id"]]["cen_ctl"].append((c[0] + x0, c[1] + y0, c[2]))
            else:
                per_mob[m["id"]]["cen_ctl"].append((float("nan"),) * 3)
            amb = S["scene_med"][-1]
            lift = sub - subc
            gate = (lift > 0) & (sub > amb * (1.0 + BARS["T2_lift_frac"]))
            per_mob[m["id"]]["residue_raw"].append(int((gate & (lift > tau)).sum()))
            # ⚑ ATTACHED residue only -- the ribbon is subtracted, and the
            # negative control is why. The mobs stand INSIDE the engagement
            # radius, so the blade and its cast light sweep straight through
            # every mob ROI. The first cut of this row counted them: it read
            # 16,394 px2 of "residue" on MOB0, the mob that is never struck and
            # carries no emitter -- MORE than any struck mob. R-24 #7 says any
            # T-2 signal on Mob0 is instrument error or bleed; this was bleed,
            # and without the in-frame null the row would have been reported as
            # a clean PASS on all three. Residue is now the DEBRIS family only
            # (components not connected into the ribbon zone) intersected with
            # the mob's own tracked ROI.
            # ⚑ AND the pixel must be the effect's OWN geometry, not scenery the
            # effect lights. Without this the arc light's pool on a mob's tile
            # counted as residue and the never-struck Mob0 read 11,417 px2 of
            # it. Residue is emissive quanta; a lit flank is a lit flank, and
            # T-3e is the row that measures lit flanks.
            deb = (DEB[y0:y1 + 1, x0:x1 + 1] & notc
                   & (lift >= 0.5 * np.maximum(sub, 1e-6)))
            _, res = residue_instrument(np.where(gate & deb, lift, 0.0), tau)
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
        # ⚑ TWO REPAIRS, both forced by treatments that did not exist at lap-1.
        # (1) The old mask carried `& ~E`. E is the effect-difference mask, and
        #     the scour IS an effect difference -- so the row was excluding
        #     exactly the pixels it counts. It scored 0 px2 at lap-1 because
        #     there was no scour to exclude; it would have scored near-0 here
        #     for the opposite reason. Now only the BRIGHTENING mask is
        #     excluded (a lit floor is not a scoured floor); darkening stays in.
        # (2) The floor region no longer sits still. `wwcr_stage.gd:985` walks
        #     the caster 1.40 m and drax lays the marks in WORLD space, so the
        #     aftermath is a PATH, not a ring around where he started. The
        #     region is the union of the engagement annulus over the caster's
        #     whole track -- which is the region a sweep could have scoured, and
        #     no larger.
        # ⚑ THIRD CUT, AND drax'S INSTRUMENT IS THE RIGHT ONE. Lap-1 measured
        # this pre-vs-post because there was nothing in the control to compare
        # against; his record picks ON-vs-CONTROL AT IDENTICAL POSE instead --
        # "cleaner than pre/post, since the caster translates" -- and he is
        # right. Pre/post carries the caster's own 1.40 m of travel and every
        # shadow it drags; same-frame ON-vs-control cancels all of it, because
        # the two arms ARE the same pose. Adopted.
        #
        # The scour is DARKENING, so it is the Dk mask; the ribbon's dark tail
        # is also darkening but lies inside the trail torus, and the scour lies
        # on the ground at R_ENGAGE outside it. Coherence-gated on the same
        # frame-3 null as T-2 -- at a 6/255 threshold the raw codec disagreement
        # is thousands of pixels and would be counted as scour.
        dk_amt = Lb - La
        fm, fpx = residue_instrument(
            np.where(floor_zone & ~trail_zone & ~mob_any, dk_amt, 0.0), BARS["T6_dl"])
        S["floor_area"].append(int(fpx))
        S["floor_dl"].append(float(dk_amt[fm].mean()) if fpx else 0.0)

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
# 3a. PARALLAX TRACK -- the camera is NOT static in this venue
#
# ⚑ THE SPEC SAYS IT IS. sec 3: "Camera is static in this venue, so the G-5
#   pan-null gap does not bite this lap." It is not static. `wwcr_stage.gd:984`
#   translates the caster at MOVE_SPEED = 3.5 m/s from t = 2.20 until
#   T_RELEASE = 2.60, and `_aim_camera(_king.position)` re-applies the pinned
#   offset every frame -- so the CAMERA translates 1.40 m over MP4 frames
#   ~119-143 and then holds. The mobs are static in world space; their IMAGE
#   positions move by up to ~100 px of pure parallax.
#
# ⚑ AND THE OBVIOUS CHECK FOR THIS RETURNS "STATIC". Whole-frame phase
#   correlation of control frame 140 against frame 0 reports a global shift of
#   EXACTLY (0, 0) -- because a 3-D camera translation produces DIFFERENT image
#   shifts at different depths, so no single global shift exists and the argmax
#   lands on the origin by default. The tell is the correlation PEAK VALUE,
#   which collapses 0.72 -> 0.03 across the move. The shift number was clean,
#   confident, and answering a question the scene does not pose. Fifth instance
#   this run of an instrument that ran and had stopped measuring.
#
# CONSEQUENCE FOR T-1. The reaction leg (first contact + 0.15 s) lands at MP4
# frames 52-74, entirely BEFORE the move, and is uncontaminated. The R-24
# return leg (final contact + 1.0 s) lands at frames 209-227, entirely AFTER
# it, where an uncompensated centroid reads ~100 px of "displacement" that no
# impulse produced. Compensation is not optional for that leg; it IS the leg.
# ===========================================================================

class ParallaxTrack:
    """Per-frame expected image position of a STATIC world ground point, under
    the analytic camera trajectory read out of the stage source.

    Not fitted from the footage. Fitting it would use mob motion to explain mob
    motion, and the mob motion is the measurand. The track is predicted, and
    Mob0 -- the never-contacted mob -- is then the residual test of whether the
    prediction is right (R-24 #7). A negative control that also VALIDATES the
    correction is worth more than one that merely reports a number.
    """

    def __init__(self, pin, w, h, n, t0, fps, mobs_world):
        self.cams = []
        for i in range(n):
            t = t0 + i / fps
            trav = min(max(t - STAGE_MOVE_FROM_S, 0.0),
                       STAGE_T_RELEASE_S - STAGE_MOVE_FROM_S) * STAGE_MOVE_SPEED_MS
            sx = STAGE_MOVE_DIR[0] * trav
            sz = STAGE_MOVE_DIR[1] * trav
            self.cams.append(GroundCam(pin, w, h, subject_xz=(sx, sz)))
        self.mobs_world = mobs_world
        self.n = n

    def offsets(self, world_xz, y=0.0):
        """Image displacement of `world_xz` at each frame, relative to frame 0.

        ⚑ `y` MATTERS AND IT IS NOT ZERO FOR A CENTROID. Parallax under a
        translating camera is depth-dependent, and a standing mob's silhouette
        CENTROID sits about half its height up, not on the ground. Correcting a
        centroid with a GROUND point's parallax leaves a residual, and that
        residual is what the never-struck mob reports -- so the null measures
        the correction's own error and says out loud whether a 2 px bar can
        stand on it.
        """
        p0 = self.cams[0].project([world_xz[0], y, world_xz[1]])
        out = []
        for c in self.cams:
            p = c.project([world_xz[0], y, world_xz[1]])
            out.append((0.0, 0.0) if (p is None or p0 is None)
                       else (p[0] - p0[0], p[1] - p0[1]))
        return out

    def max_offset_px(self, world_xz):
        o = self.offsets(world_xz)
        return max(math.hypot(*v) for v in o)


def residue_instrument(lift, tau_res, min_px=T2_COHERENCE_MIN_PX):
    """T-2's residue detector: THRESHOLD **plus** SPATIAL COHERENCE.

    ⚑ R-24 #10 binds this choice. The two arms are separately-encoded h264, and
    on CONTENT-IDENTICAL frames 3,850 px differ at |dL| > 0.02 (drax, record
    sec 8). A criterion phrased "zero residue pixels" evaluated at that
    threshold reports a failure the encoder produced.

    Of the three options the ruling left open -- raise the threshold, add a
    spatial-coherence test, re-render lossless with PRUNE=0 -- this instrument
    takes the FIRST TWO TOGETHER and declines the third, for a stated reason:
    the lossless ladder costs a 1.5 GiB re-render and would answer only the
    residue leg, while the coherence test additionally answers the RIGHT
    question. Residue is a handful of soft quanta a few tens of px across,
    contiguous, sitting on a mob. Codec disagreement is isolated single pixels
    scattered frame-wide. The two are separable by SHAPE, not only by
    magnitude, and separating them by shape does not cost the criterion its
    sensitivity to a genuinely faint residue the way a raised threshold alone
    would.

    Negative-controlled on frame 3 (t = 0.25 s, before T_BEGIN = 0.30 s, arms
    identical by construction) BEFORE it renders any verdict -- see
    `t2_frame3_negative_control()`.
    """
    m = lift > tau_res
    if not m.any():
        return np.zeros_like(m), 0
    lab, k = ndimage.label(m)
    if k == 0:
        return np.zeros_like(m), 0
    sz = ndimage.sum(m, lab, range(1, k + 1))
    keep = np.nonzero(sz >= min_px)[0] + 1
    out = np.isin(lab, keep) if keep.size else np.zeros_like(m)
    return out, int(out.sum())


# ===========================================================================
# 3b. T-3a RE-CUT -- FRAME-LUMINANCE OWNERSHIP
#
# Spec (168dbe44), sec 1 T-3 criterion (a), as amended 2026-08-25:
#
#   "during sustain, the effect region owns >= 75% of the frame's top-0.5%
#    luminance pixels (UI excluded) -- 'plainly the brightest thing in the
#    room' means outshining the braziers, not the floor."
#
# WHY THIS REPLACED THE OLD ROUTE. The superseded statistic was P99(effect L)
# / median(annular scene L): a ratio against a DARK FLOOR. It read 4.07x on
# the lap-1 render whose spec line asserted "currently < 1.0". The instrument
# was sound and sweep-stable; the PREMISE was false, because the perceptual
# claim ("brightest thing in the room") is salience against the room's BRIGHT
# sources, and a floor-referenced ratio cannot see them. Ownership of the
# frame's own top tail is referenced to the braziers by construction: the
# braziers ARE the top tail until something outshines them.
#
# THIS ROUTE MUST ITSELF MEET A NEGATIVE CONTROL BEFORE IT CERTIFIES ANYTHING
# -- the spec says so in the criterion's own text, and it is the second time
# of asking for this criterion. See `--t3a-only` and sec 10 of the notes.
# ===========================================================================

def derive_ui_mask(ctl_path, w, h, n, sample=None):
    """UI exclusion, DERIVED from the footage, never asserted from a config.

    The discriminant is EXACT temporal constancy in the CONTROL arm. A HUD
    overlay is composited after the 3D pass and does not move; world pixels
    under a moving camera do. That discriminant is only valid if the camera
    ACTUALLY MOVES, so the camera-motion fraction is measured and reported
    beside the mask -- if a future clip is shot from a locked camera this
    route silently starts calling the whole room "UI", and the reported
    motion fraction is what makes that visible instead of silent.

    ⚑ COHERENCE FILTER, added after the raw discriminant OVER-FIRED on the
    lap-1 pair: constancy alone returned 16,652 px in 3,104 components of
    MEDIAN SIZE 1 -- coincidentally-static dark world pixels, not a HUD. A HUD
    element is CONTIGUOUS; 1-px specks are not. Components < 64 px are dropped
    and the raw count is reported beside the filtered one so the over-fire
    stays visible rather than being quietly absorbed.

    Measured on the lap-1 cathedral pair: motion fraction 0.634, raw constant
    16,652 px, filtered 6,559 px, all of it dark (median L 0.20, max 0.497)
    and NONE of it inside the frame's top-0.5% set. That venue has no HUD
    (confirmed by eye on frame 120), so the exclusion is inert here -- and
    `t3a_ownership` proves it inert per-frame rather than asserting it, by
    computing ownership with the exclusion ON and OFF in the same pass.
    """
    idx = sample or sorted({0, n // 4, n // 2, (3 * n) // 4, n - 1})
    S = Stream(ctl_path, w, h)
    frames, i = {}, 0
    while True:
        f = S.read()
        if f is None:
            break
        if i in idx:
            frames[i] = f.copy()
        i += 1
    S.close()
    ks = sorted(frames)
    base = frames[ks[0]]
    const = np.ones((h, w), bool)
    motion = np.zeros((h, w), bool)
    for k in ks[1:]:
        d = np.abs(luma(frames[k]) - luma(base))
        const &= (frames[k] == base).all(2)
        motion |= d > 0.02
    raw_px = int(const.sum())
    lab, k = ndimage.label(const)
    if k:
        sz = ndimage.sum(const, lab, range(1, k + 1))
        keep = np.nonzero(sz >= MIN_UI_COMPONENT_PX)[0] + 1
        const = np.isin(lab, keep) if keep.size else np.zeros_like(const)
    ys, xs = np.nonzero(const)
    return const, {
        "ui_mask_px": int(const.sum()),
        "ui_mask_frac": round(float(const.mean()), 6),
        "ui_mask_px_raw_before_coherence_filter": raw_px,
        "ui_mask_components_raw": int(k),
        "ui_min_component_px": MIN_UI_COMPONENT_PX,
        "ui_mask_bbox": None if not const.any() else
            [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
        "camera_motion_frac": round(float(motion.mean()), 4),
        "frames_sampled": ks,
        "discriminant": "exact temporal constancy in the control arm, then a >=%d px "
                        "coherence filter; valid only under a moving camera -- motion "
                        "fraction reported beside it" % MIN_UI_COMPONENT_PX,
        "caveat": "on the lap-1 cathedral this returns dark static WORLD pixels, not a "
                  "HUD (that venue has none). Inert by measurement: see the "
                  "ownership_inclusive_noUI_median sensitivity field, not by assertion.",
    }


def t3a_ownership(on_path, ctl_path, w, h, n, sustain, tau, ui_mask):
    """Per-sustain-frame ownership of the frame's top-0.5% luminance pixels.

    OPERATIONAL CHOICES, each named because each could have gone otherwise:

    1. SUSTAIN WINDOW. Frames [sustain[0], sustain[1]] inclusive, taken from
       the harness state timeline (`state=SUSTAIN`) when a log is supplied,
       else derived from the area curve and stamped DERIVED. The criterion
       says "during the effect's sustain window"; the harness knows where
       that is and the pixels do not have to be asked.

    2. EFFECT REGION. The SAME control-differenced mask the rest of the T-3
       family uses -- |L_on - L_ctl| > tau, 3x3 opened, components >= 12 px --
       so "the effect region" means one thing across T-3a/b/c/d. tau is the
       far-field false-positive null from `seed_geometry`, not a MAD.

    3. THE INCLUSIVE/STRICT SPLIT, and why both are reported. The differenced
       mask contains every pixel the effect CHANGED, which includes pixels the
       effect merely LIT. A lap-2 build with the specified apex OmniLight can
       brighten a brazier by a few percent, put that brazier into the
       differenced mask, and then be credited with owning top pixels that are
       the brazier's. That is precisely the misattribution this negative
       control exists to catch. So:
         - INCLUSIVE  = ownership by the full differenced region.
         - STRICT     = ownership by pixels where the effect supplies the
                        MAJORITY of the pixel's own luminance, (L_on - L_ctl)
                        >= 0.5 * L_on. An arc pixel on a dark floor passes
                        trivially; a brazier lifted 7% does not.
       INCLUSIVE is primary because it is the plain reading of "the effect
       region". STRICT is a WITHHOLDING guard and can only ever subtract a
       pass, never grant one: if INCLUSIVE clears the bar while STRICT does
       not, the pass is being carried by pixels the effect lit rather than
       pixels the effect IS, and the call is INDETERMINATE-MISATTRIBUTION
       rather than PASS. It cannot manufacture a FAIL into a PASS.

    4. TOP-0.5% SELECTION. Threshold-based: T = P99.5 of L_on over non-UI
       pixels, set = {L_on >= T}. NOT exact-rank, because exact-rank breaks
       ties arbitrarily and a build that clips its core to white creates
       enormous tie mass -- the arbitrary tie-break would then decide the
       criterion. The threshold set's actual size is reported every frame so
       tie inflation is VISIBLE (target 0.500%); an exact-rank ownership is
       computed alongside as a corroborator. Measured on lap-1: 0.500-0.508%,
       max L = 0.83, one pixel at max -- no clipping, the two agree.

    5. UI EXCLUSION applies to the DENOMINATOR SET (which pixels are eligible
       to be "the frame's top pixels") and to the effect mask alike -- AND the
       same ownership is computed a second time with NO exclusion at all, in
       the same pass, so that a reader who distrusts my UI mask can see
       whether the mask decided anything. On lap-1 it decides nothing (both
       read 0.146). A derived mask that could have been wrong and provably was
       not load-bearing is worth more than a mask asserted to be right.

    6. DEGENERATE REGION. If the effect mask is empty the frame reports
       ownership 0.0, flagged, and is NOT dropped. Dropping empty frames would
       let a build that flickers off during sustain be scored only on the
       frames where it was on.
    """
    lo, hi = int(sustain[0]), int(sustain[1])
    valid = ~ui_mask
    n_valid = int(valid.sum())
    k_target = int(round(BARS["T3a_top_frac"] * n_valid))

    A, B = Stream(on_path, w, h), Stream(ctl_path, w, h)
    per = []
    for i in range(n):
        fa, fb = A.read(), B.read()
        if fa is None or fb is None:
            break
        if i < lo:
            continue
        if i > hi:
            break
        La, Lb = luma(fa), luma(fb)
        d = La - Lb

        E = ndimage.binary_opening(np.abs(d) > tau, np.ones((3, 3))) & valid
        lab, k = ndimage.label(E)
        if k:
            sz = ndimage.sum(E, lab, range(1, k + 1))
            keep = np.nonzero(sz >= MIN_COMPONENT_PX)[0] + 1
            E = np.isin(lab, keep) if keep.size else np.zeros_like(E)
        strict = E & (d >= 0.5 * np.maximum(La, 1e-6))

        Lv = La[valid]
        thr = float(np.percentile(Lv, 100.0 * (1.0 - BARS["T3a_top_frac"])))
        top = valid & (La >= thr)
        ktop = int(top.sum())
        # exact-rank corroborator: the k_target brightest eligible pixels
        flat = np.where(valid, La, -1.0).ravel()
        rank_idx = np.argpartition(flat, -k_target)[-k_target:]
        top_rank = np.zeros(flat.size, bool)
        top_rank[rank_idx] = True
        top_rank = top_rank.reshape(La.shape)

        # sensitivity: the same statistic with NO UI exclusion whatsoever
        thr_all = float(np.percentile(La, 100.0 * (1.0 - BARS["T3a_top_frac"])))
        top_all = La >= thr_all
        E_all = ndimage.binary_opening(np.abs(d) > tau, np.ones((3, 3)))

        per.append({
            "frame": i,
            "own_inclusive": float((top & E).sum()) / max(ktop, 1),
            "own_inclusive_noUI": float((top_all & E_all).sum()) / max(int(top_all.sum()), 1),
            "own_strict": float((top & strict).sum()) / max(ktop, 1),
            "own_rank_corroborator": float((top_rank & E).sum()) / max(k_target, 1),
            "top_thr_L": round(thr, 5),
            "top_px": ktop,
            "top_frac_actual": round(ktop / n_valid, 6),
            "effect_px": int(E.sum()),
            "effect_px_strict": int(strict.sum()),
            "effect_max_L": None if not E.any() else round(float(La[E].max()), 5),
            "frame_max_L": round(float(Lv.max()), 5),
            "degenerate_effect_region": bool(E.sum() == 0),
        })
    A.close()
    B.close()
    if not per:
        return {"error": "no sustain frames decoded", "sustain": [lo, hi]}

    inc = np.array([p["own_inclusive"] for p in per])
    st = np.array([p["own_strict"] for p in per])
    rk = np.array([p["own_rank_corroborator"] for p in per])
    tf = np.array([p["top_frac_actual"] for p in per])
    return {
        "sustain_frames": [lo, hi], "n_frames_measured": len(per),
        "ownership_inclusive_median": float(np.median(inc)),
        "ownership_inclusive_mean": float(inc.mean()),
        "ownership_inclusive_max": float(inc.max()),
        "ownership_strict_median": float(np.median(st)),
        "ownership_rank_corroborator_median": float(np.median(rk)),
        "ownership_inclusive_noUI_median": float(np.median(
            [p["own_inclusive_noUI"] for p in per])),
        "frames_over_bar_inclusive": int((inc >= BARS["T3a_ownership"]).sum()),
        "top_set_frac_actual_median": float(np.median(tf)),
        "tie_inflation_flag": bool(np.median(tf) > 1.5 * BARS["T3a_top_frac"]),
        "degenerate_frames": int(sum(p["degenerate_effect_region"] for p in per)),
        "effect_max_L_median": float(np.median(
            [p["effect_max_L"] for p in per if p["effect_max_L"] is not None])
            ) if any(p["effect_max_L"] is not None for p in per) else None,
        "frame_max_L_median": float(np.median([p["frame_max_L"] for p in per])),
        "top_thr_L_median": float(np.median([p["top_thr_L"] for p in per])),
        "tau": tau,
        "per_frame": per,
    }


def t3a_scene_hot_persistence(on_path, ctl_path, w, h, sustain, ui_mask):
    """Instrument sanity check the conductor actually needs: WHO owns the top
    pixels when the effect is off, and does turning it on displace them?

    Computes each arm's own top-0.5% set on the same frames and reports the
    overlap. If the ON arm's top set is ~the control's top set, the scene's
    hot sources still own the frame and the effect has not entered the tail at
    all -- which is a different statement from "the effect owns < 75%", and a
    stronger one.
    """
    lo, hi = int(sustain[0]), int(sustain[1])
    valid = ~ui_mask
    q = 100.0 * (1.0 - BARS["T3a_top_frac"])
    A, B = Stream(on_path, w, h), Stream(ctl_path, w, h)
    keep, i = [], 0
    while True:
        fa, fb = A.read(), B.read()
        if fa is None or fb is None:
            break
        if lo <= i <= hi:
            La, Lb = luma(fa), luma(fb)
            ta = valid & (La >= np.percentile(La[valid], q))
            tb = valid & (Lb >= np.percentile(Lb[valid], q))
            keep.append(float((ta & tb).sum()) / max(int(ta.sum()), 1))
        i += 1
        if i > hi:
            break
    A.close()
    B.close()
    return {"median_on_top_set_also_top_in_control": float(np.median(keep)) if keep else None,
            "n_frames": len(keep),
            "reading": "fraction of the ON arm's top-0.5% pixels that are ALSO top-0.5% "
                       "with the effect hidden -- i.e. how much of the frame's bright "
                       "tail is the room rather than the effect"}


def t3a_row(t3a, scene=None):
    """The scorecard row. Three-valued, with the misattribution guard wired in."""
    if "error" in t3a:
        return _row("T-3a", "frame-luminance ownership (RE-CUT)", "INDETERMINATE",
                    t3a, ">= %.0f%%" % (100 * BARS["T3a_ownership"]),
                    "no measurable sustain window")
    inc = t3a["ownership_inclusive_median"]
    st = t3a["ownership_strict_median"]
    bar = BARS["T3a_ownership"]
    if inc >= bar and st < bar:
        call = "INDETERMINATE"
        note = ("MISATTRIBUTION GUARD FIRED: the inclusive region clears the bar and the "
                "emissive-core region does not, so the pass is carried by pixels the effect "
                "LIT (brazier lift entering the differenced mask), not pixels the effect IS. "
                "Not a PASS. Re-measure with the region question settled.")
    else:
        call = "PASS" if inc >= bar else "FAIL"
        note = ("median over sustain frames of |top-0.5%% set INTERSECT effect| / |top-0.5%% set|, "
                "UI excluded. Strict (emissive-core) corroborator %.4f; exact-rank "
                "corroborator %.4f; top-set actual size %.4f%% of eligible px (target %.3f%%)."
                % (st, t3a["ownership_rank_corroborator_median"],
                   100 * t3a["top_set_frac_actual_median"], 100 * BARS["T3a_top_frac"]))
    if scene:
        note += (" Scene-hot persistence: %.4f of the ON arm's top pixels are top with the "
                 "effect hidden." % (scene["median_on_top_set_also_top_in_control"] or float("nan")))
    if t3a["tie_inflation_flag"]:
        note += " ⚑ TIE INFLATION: top set is >1.5x its target size; luminance is clipping."
    operand = {k: v for k, v in t3a.items() if k != "per_frame"}
    operand["ownership_inclusive_median"] = round(inc, 4)
    operand["ownership_strict_median"] = round(st, 4)
    if scene:
        operand["scene_hot_persistence"] = scene
    return _row("T-3a", "frame-luminance ownership (RE-CUT)", call, operand,
                ">= %.0f%% of frame top-0.5%% luminance pixels" % (100 * bar), note)


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


def _t1_t2_lap2(S, per_mob, phases, fps, lap2, tau, n):
    """T-1 and T-2 under the lap-2 rulings, plus the Mob0 negative-control row.

    R-24 #2  -- return leg indexed to FINAL contact.
    R-24 #7  -- Mob0 is an in-frame negative control; any T-1/T-2 signal on it
                is instrument error, frame motion or bleed, never effect signal.
    R-24 #10 -- T-2's residue detector is threshold + spatial coherence,
                negative-controlled on frame 3.
    """
    rows = []
    cj = lap2["contacts"]                  # seeded-id -> {first,last,all}
    off = lap2["parallax"]                 # seeded-id -> [(dx,dy)] per frame
    nc = lap2["nc_id"]                     # seeded id of the never-contacted mob
    names = lap2["names"]                  # seeded-id -> engine name
    react_f = max(1, int(round(BARS["T1_react_window_s"] * fps)))
    ret_f = int(round(BARS["T1_return_by_s"] * fps))

    def resid(mid, arm):
        """Centroid track with the analytic parallax of a STATIC mob removed."""
        cen = np.array(per_mob[mid][arm], float)
        o = np.array(off[mid], float)[:len(cen)]
        first = cj[mid]["first"]
        r0 = 0 if first is None else max(0, first - 12)
        r1 = 12 if first is None else first
        rest = np.nanmean(cen[r0:r1], 0)
        rest_o = np.nanmean(o[r0:r1], 0)
        pred = np.column_stack([rest[0] + o[:, 0] - rest_o[0],
                                rest[1] + o[:, 1] - rest_o[1]])
        d = np.hypot(cen[:, 0] - pred[:, 0], cen[:, 1] - pred[:, 1])
        t = np.abs(((cen[:, 2] - rest[2] + 90) % 180) - 90)
        return d, t, rest

    def leg(mid, arm):
        d, t, _ = resid(mid, arm)
        first, last = cj[mid]["first"], cj[mid]["last"]
        if first is None:
            k = int(np.nanargmax(d)) if np.isfinite(d).any() else 0
            return {"max_disp_px": round(float(np.nanmax(d)), 3),
                    "max_tilt_deg": round(float(np.nanmax(t)), 3),
                    "max_disp_frame": k, "sustained": False, "returned": None,
                    "return_disp_px": None}
        w0, w1 = first, min(n, first + react_f + BARS["T1_sustain_frames"])
        hit = (d[w0:w1] >= BARS["T1_centroid_px"]) | (t[w0:w1] >= BARS["T1_axis_deg"])
        rf = min(n - 1, last + ret_f)
        return {"max_disp_px": round(float(np.nanmax(d[w0:w1])), 3),
                "max_tilt_deg": round(float(np.nanmax(t[w0:w1])), 3),
                "sustained": bool(_longest_run(hit) >= BARS["T1_sustain_frames"]),
                "sustain_run_frames": int(_longest_run(hit)),
                "react_window_frames": [int(w0), int(w1 - 1)],
                "return_frame": int(rf),
                "return_disp_px": round(float(d[rf]), 3),
                "returned": bool(d[rf] <= BARS["T1_return_px"]),
                "peak_disp_whole_clip_px": round(float(np.nanmax(d)), 3)}

    contacted = [m for m in per_mob if cj[m]["first"] is not None]
    det = {}
    responded = 0
    for mid in per_mob:
        det[names[mid]] = {"seeded_roi_id": mid,
                           "contacts": cj[mid]["all"],
                           "CONTROL_arm": leg(mid, "cen_ctl"),
                           "ON_arm": leg(mid, "cen")}
        if mid in contacted:
            c = det[names[mid]]["CONTROL_arm"]
            # ⚑ CONTAMINATION FLAG, not a silent drop. At the return frame the
            # caster may have travelled INTO this mob's ROI; the fixed caster
            # box removes most of him but not his animated extremities, and what
            # is left drags the centroid. A contaminated return number is
            # REPORTED and is not allowed to fail the criterion on its own.
            rf = c.get("return_frame")
            ov = lap2["roi_caster_overlap"].get(mid, {})
            c["caster_overlap_frac_at_return"] = ov.get(rf, 0.0)
            c["return_contaminated"] = bool(ov.get(rf, 0.0) > 0.02)
            if c["sustained"] and c["returned"]:
                responded += 1
    N = len(contacted)
    contaminated = [m for m in contacted
                    if det[names[m]]["CONTROL_arm"].get("return_contaminated")]
    clean = [m for m in contacted if m not in contaminated]

    # ⚑ THE NULL IS EVALUATED AT THE SAME FRAME INDICES AS THE LEG IT VALIDATES.
    # Mob0's max residual over the WHOLE clip is not the right comparator for a
    # leg measured in a 13-frame window: the clip contains the caster-travel
    # dolly, and a null quoted across it imports a disturbance the leg never
    # sees. Per-leg, per-window. This is the difference between "the null is
    # noisy somewhere" and "the null is noisy HERE, so this bar cannot stand."
    d_nc, t_nc, _ = resid(nc, "cen_ctl")
    nulls = {"react_windows": {}, "return_frames": {}}
    for mid in contacted:
        w0, w1 = det[names[mid]]["CONTROL_arm"]["react_window_frames"]
        nulls["react_windows"][names[mid]] = {
            "frames": [w0, w1],
            "null_max_disp_px": round(float(np.nanmax(d_nc[w0:w1 + 1])), 3),
            "null_max_tilt_deg": round(float(np.nanmax(t_nc[w0:w1 + 1])), 3)}
        rf = det[names[mid]]["CONTROL_arm"]["return_frame"]
        nulls["return_frames"][names[mid]] = {
            "frame": rf, "null_disp_px": round(float(d_nc[rf]), 3)}
    react_null_disp = max(v["null_max_disp_px"] for v in nulls["react_windows"].values())
    react_null_tilt = max(v["null_max_tilt_deg"] for v in nulls["react_windows"].values())
    ret_null = max(v["null_disp_px"] for v in nulls["return_frames"].values())
    nulls["react_leg_admissible"] = bool(react_null_disp < BARS["T1_centroid_px"]
                                         and react_null_tilt < BARS["T1_axis_deg"])
    nulls["return_leg_admissible"] = bool(ret_null < BARS["T1_return_px"])
    nulls["I7_note"] = (
        "I-7: a leg whose in-frame null reads at or above its own bar may report "
        "its number and may not carry the bar. React leg null: %.2f px / %.2f deg "
        "against 8 px / 4 deg. Return leg null: %.2f px against a 2 px bar."
        % (react_null_disp, react_null_tilt, ret_null))
    if not nulls["return_leg_admissible"]:
        responded = sum(1 for mid in contacted
                        if det[names[mid]]["CONTROL_arm"]["sustained"])
    react_all = all(det[names[m]]["CONTROL_arm"]["sustained"] for m in contacted)
    clean_ok = all(det[names[m]]["CONTROL_arm"]["returned"] for m in clean)
    if not nulls["react_leg_admissible"] or not nulls["return_leg_admissible"]:
        t1_call = "INDETERMINATE"
    elif not react_all:
        t1_call = "FAIL"
    elif not clean_ok:
        t1_call = "FAIL"          # an uncontaminated mob measurably fails to return
    elif contaminated:
        t1_call = "INDETERMINATE"  # every clean mob passes; a contaminated one is unknown
    else:
        t1_call = "PASS"
    nulls["reaction_leg_all_N"] = bool(react_all)
    nulls["return_leg_clean_mobs"] = [names[m] for m in clean]
    nulls["return_leg_contaminated_mobs"] = [names[m] for m in contaminated]
    rows.append(_row(
        "T-1", "recipient state response",
        t1_call,
        {"N_contacted": N, "responded": responded, "per_mob": det,
         "in_frame_null_per_leg": nulls,
         "return_leg_indexed_to": "FINAL contact (R-24 #2)",
         "primary_arm": "CONTROL (flinch fires in both arms; control silhouette "
                        "is uncontaminated by T-2 residue quanta)",
         "parallax_compensated": True},
        ">=%.0f px centroid or >=%.0f deg axis, %d frames, all N; within %.0f px "
        "of rest %.1fs after FINAL contact"
        % (BARS["T1_centroid_px"], BARS["T1_axis_deg"], BARS["T1_sustain_frames"],
           BARS["T1_return_px"], BARS["T1_return_by_s"]),
        "measured WITHIN-ARM against each mob's own rest pose, with the analytic "
        "caster-travel parallax of a STATIC mob removed; the control arm is "
        "gameplay-identical so a control-DIFFERENCED T-1 would null out."))

    # ---- T-2 -------------------------------------------------------------
    half = int(round(0.5 * fps))
    per, carried = {}, 0
    simul = np.zeros(n, int)
    for mid in per_mob:
        res = np.array(per_mob[mid]["residue"], float)
        raw = np.array(per_mob[mid]["residue_raw"], float)
        first, last = cj[mid]["first"], cj[mid]["last"]
        at = res[min(n - 1, first + half)] if first is not None else float("nan")
        live = res >= BARS["T2_residue_px2"]
        if first is not None:
            simul += live.astype(int)
        lf = np.nonzero(live)[0]
        per[names[mid]] = {
            "residue_at_contact_plus_0.5s_px2": None if first is None else float(at),
            "peak_residue_px2": float(res.max()),
            "peak_frame": int(res.argmax()),
            "frames_over_bar": int(live.sum()),
            "last_frame_over_bar": None if not lf.size else int(lf[-1]),
            "persistence_past_final_contact_s": None if (not lf.size or last is None)
            else round(float(lf[-1] - last) / fps, 4),
            "raw_threshold_only_peak_px2": float(raw.max())}
        if first is not None and np.isfinite(at) and at >= BARS["T2_residue_px2"]:
            carried += 1
    N = len(contacted)
    simul_max = int(simul.max()) if n else 0
    # ⚑ Same per-leg null discipline as T-1. Mob0 carries no emitter, so any
    # debris on its ROI is a SHED quantum drifting past -- and shed quanta and
    # residue quanta are the same pale soft blobs. The two families are not
    # separable in these two arms by geometry or by threshold; they ARE
    # separable by PERSISTENCE, which is what the null quantifies here.
    nc_res = np.array(per_mob[nc]["residue"], float)
    nc_frames_over = int((nc_res >= BARS["T2_residue_px2"]).sum())
    t2_null = {
        "null_peak_debris_px2": float(nc_res.max()),
        "null_frames_over_120px2": nc_frames_over,
        "struck_frames_over_120px2": {names[m]: int(np.sum(
            np.array(per_mob[m]["residue"], float) >= BARS["T2_residue_px2"]))
            for m in contacted},
        "area_leg_admissible": bool(nc_res.max() < BARS["T2_residue_px2"]),
        "note": "if the never-struck mob's ROI carries MORE than the 120 px2 bar "
                "at any frame, the >=120 px2 leg cannot distinguish residue from "
                "a shed quantum transiting the ROI and may not carry a bar (I-7). "
                "PERSISTENCE still discriminates and is reported beside it."}
    # ⚑ The "gone by effect-end + 2.0 s" leg. Effect end + 2.0 s is BEYOND this
    # clip: IDLE at 3.40 s + 2.0 = 5.40 s against a window that ends at 5.00 s.
    # B-1 delivered 1.60 s of aftermath against the spec's own >= 1.5 s ask, and
    # T-2's clause asks for 2.0 s -- the two numbers in the same spec do not
    # agree. It is evaluated at the STRONGEST AVAILABLE index instead, and the
    # entailment is stated rather than assumed: residue cannot spawn after the
    # final contact (frame 167), the asserted lifetime ceiling is 1.40 s, so
    # zero at end + 1.60 s entails zero at end + 2.0 s.
    end = phases["effect_end"]
    clear_i = n - 1
    clear_px = int(np.sum([per_mob[m]["residue"][clear_i] for m in per_mob]))
    clear_raw = int(np.sum([per_mob[m]["residue_raw"][clear_i] for m in per_mob]))
    clear_ok = clear_px <= T2_CLEAR_MIN_PX
    ok = (N and carried == N and simul_max >= max(1, N - 1) and clear_ok)
    t2_call = "PASS" if ok else "FAIL"
    if not t2_null["area_leg_admissible"]:
        # The area leg cannot carry its bar. The clear leg and the persistence
        # leg remain admissible (the frame-3 null is clean and the null mob's
        # debris is transient), so the row reports what it can and withholds.
        t2_call = "INDETERMINATE"
    rows.append(_row(
        "T-2", "attached wind-residue persistence",
        t2_call,
        {"mobs_with_residue_at_+0.5s": carried, "N_contacted": N,
         "in_frame_null_per_leg": t2_null,
         "max_simultaneous": simul_max, "simultaneity_bar": max(1, N - 1),
         "clear_leg": {
             "evaluated_at_frame": clear_i,
             "evaluated_at_effect_end_plus_s": round((clear_i - end) / fps, 3),
             "spec_asks_for_s": BARS["T2_clear_after_s"],
             "coherence_gated_residue_px": clear_px,
             "raw_threshold_only_px": clear_raw,
             "entailment": "no residue can spawn after the final contact "
                           "(frame %d) and the asserted lifetime ceiling is "
                           "1.40 s, so zero here entails zero at +2.0 s"
                           % max((cj[m]["last"] or -1) for m in per_mob),
             "passes": bool(clear_ok)},
         "per_mob": per},
        ">=%.0f px2 at contact+0.5s, all N; >=N-1 simultaneous; zero at end+2.0s"
        % BARS["T2_residue_px2"],
        "residue detector = threshold + SPATIAL COHERENCE (>= %d px component), "
        "negative-controlled on frame 3 per R-24 #10; raw-threshold-only counts "
        "are reported beside it so the codec floor stays visible."
        % T2_COHERENCE_MIN_PX))

    # ---- NC-Mob0 ----------------------------------------------------------
    d_ctl, t_ctl, _ = resid(nc, "cen_ctl")
    d_on, t_on, _ = resid(nc, "cen")
    res_nc = np.array(per_mob[nc]["residue"], float)
    raw_nc = np.array(per_mob[nc]["residue_raw"], float)
    ncd = float(np.nanmax(d_ctl))
    nct = float(np.nanmax(t_ctl))
    ncr = float(res_nc.max())
    # ⚑ SCORED PER-LEG, on the same windows the legs it validates are scored on.
    # The whole-clip maxima are reported as diagnostics and are NOT the call:
    # they land at MP4 frame ~121, the first frame of the caster-travel dolly,
    # and a null quoted across a disturbance the leg never sees is the same
    # error as a bar quoted against the wrong null. I hold my own row to the
    # discipline I just imposed on T-1.
    wr = [v["frames"] for v in nulls["react_windows"].values()]
    rf = [v["frame"] for v in nulls["return_frames"].values()]
    w_d = max(float(np.nanmax(d_ctl[a:b + 1])) for a, b in wr)
    w_t = max(float(np.nanmax(t_ctl[a:b + 1])) for a, b in wr)
    r_d = max(float(d_ctl[i]) for i in rf)
    clean = (w_d < BARS["T1_centroid_px"] and w_t < BARS["T1_axis_deg"]
             and r_d < BARS["T1_return_px"])
    rows.append(_row(
        "NC-Mob0", "in-frame negative control (never contacted)",
        "PASS" if clean else "FAIL",
        {"engine_name": names[nc], "seeded_roi_id": nc, "contacts": 0,
         "SCORED_LEGS": {
             "T1_react_windows_max_disp_px": round(w_d, 3),
             "T1_react_windows_max_tilt_deg": round(w_t, 3),
             "T1_return_frames_max_disp_px": round(r_d, 3),
             "verdict": "zero flinch and zero residual displacement on the mob "
                        "the blade never reaches, at the exact frame indices "
                        "T-1's two legs are read on"},
         "DIAGNOSTIC_whole_clip": {
             "max_centroid_residual_px_CONTROL": round(ncd, 3),
             "max_axis_residual_deg_CONTROL": round(nct, 3),
             "attribution": "peaks at the first frames of the caster-travel "
                            "dolly (MP4 ~121); parallax-model residual on a "
                            "121 px correction, NOT a flinch"},
         "T2_CONTAMINATION_FINDING": {
             "peak_debris_px2_coherence_gated": ncr,
             "frames_over_120px2": int((res_nc >= BARS["T2_residue_px2"]).sum()),
             "reading": "shed quanta transiting the ROI plus the glow pass "
                        "washing the tile -- NOT residue, since Mob0 carries no "
                        "emitter. Reported as the instrument finding that "
                        "disqualifies T-2's >=120 px2 area leg (I-7), never as "
                        "effect signal (R-24 #7)."},
         "T1_max_centroid_residual_px_CONTROL": round(ncd, 3),
         "T1_max_centroid_residual_px_ON": round(float(np.nanmax(d_on)), 3),
         "T1_max_axis_residual_deg_CONTROL": round(nct, 3),
         "T1_max_axis_residual_deg_ON": round(float(np.nanmax(t_on)), 3),
         "T1_uncompensated_max_disp_px": lap2["nc_uncompensated_px"],
         "T2_peak_residue_px2_coherence_gated": ncr,
         "T2_peak_residue_px2_raw_threshold": float(raw_nc.max()),
         "parallax_model_validated_by_this_row": bool(ncd < BARS["T1_centroid_px"])},
        "ZERO flinch (< %.0f px, < %.0f deg) and ZERO residue (< %.0f px2)"
        % (BARS["T1_centroid_px"], BARS["T1_axis_deg"], BARS["T2_residue_px2"]),
        "R-24 #7. Same lights, same clock, same venue, never struck (misses the "
        "pass cone by 3.4 deg, geometric). Any signal here is instrument error, "
        "frame motion or bleed -- NEVER effect signal. This row also validates "
        "the parallax correction: an over- or under-corrected track shows up "
        "here as a residual on a mob that cannot have moved."))
    return rows


def score(S, per_mob, wp, geo, phases, fps, contacts, ff08=None, t3a=None, scene=None,
          lap2=None):
    rows = []
    n = len(S["area"])
    sus = phases["sustain"]
    area = np.array(S["area"], float)
    sus_mean = float(area[sus[0]:sus[1] + 1].mean())

    if lap2 is not None:
        rows.extend(_t1_t2_lap2(S, per_mob, phases, fps, lap2, geo["tau"], n))
        return rows + _score_photometry(S, per_mob, wp, geo, phases, fps, ff08,
                                        t3a, scene, n, sus, area, sus_mean)

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

    return rows + _score_photometry(S, per_mob, wp, geo, phases, fps, ff08,
                                    t3a, scene, n, sus, area, sus_mean)


def _score_photometry(S, per_mob, wp, geo, phases, fps, ff08, t3a, scene,
                      n, sus, area, sus_mean):
    """T-3 .. T-6. Untouched by the lap-2 rulings; shared by both paths so a
    scorecard is the same instrument whichever entry point produced it."""
    rows = []
    # ---------------- T-3 a/b/c -------------------------------------------
    # T-3a is the RE-CUT ownership route (sec 3b), computed in its own pass.
    # The superseded floor-referenced ratio is retained ONLY as a recorded
    # diagnostic beside it, because it is the number that caused the re-cut and
    # a reader comparing laps must be able to see both.
    dom = nanmed(np.array(S["p99_on"]) / np.array(S["scene_med"]))
    if t3a is not None:
        r = t3a_row(t3a, scene)
        r["operand"]["SUPERSEDED_floor_referenced_ratio"] = round(dom, 4)
        rows.append(r)
    else:
        rows.append(_row("T-3a", "frame-luminance ownership (RE-CUT)", "INDETERMINATE",
                         {"SUPERSEDED_floor_referenced_ratio": round(dom, 4)},
                         ">= %.0f%%" % (100 * BARS["T3a_ownership"]),
                         "ownership pass not run"))
    rng = nanmed(np.array(S["p95_on"]) / np.maximum(np.array(S["p20_on"]), 1e-6))
    rng_r = nanmed(np.array(S["p95_rib"]) / np.maximum(np.array(S["p20_rib"]), 1e-6))
    seg_note = ("R-24 #8: my segmentation governs, and I am reporting TWO. "
                "`ribbon_only` is the two-surface split this criterion is written "
                "about (components connected into the ribbon zone). `composed` is "
                "the whole brightening effect region -- ribbon + shed quanta + "
                "attached residue + cast-lit floor. The call is taken on "
                "ribbon_only because T-3 is a TREATMENT-level criterion and R-23 "
                "moved the lap-level question out of it into (a); the composed "
                "figure is reported so the conductor can adjudicate on the pair.")
    rows.append(_row("T-3b", "internal luminance range",
                     "PASS" if rng_r >= BARS["T3b_p95_p20"] else "FAIL",
                     {"ribbon_only_median_P95_over_P20": round(rng_r, 4),
                      "composed_median_P95_over_P20": round(rng, 4),
                      "drax_own_instrument": "2.2 - 3.5 (his mask includes "
                                             "cast-lit floor; record sec 6)"},
                     ">= %.1f" % BARS["T3b_p95_p20"], seg_note))
    sat = nanmed(S["midS"])
    sat_r = nanmed(S["midS_rib"])
    rows.append(_row("T-3c", "mid-band saturation",
                     "PASS" if sat_r >= BARS["T3c_sat"] else "FAIL",
                     {"ribbon_only_median_midband_HSV_S": round(sat_r, 4),
                      "composed_median_midband_HSV_S": round(sat, 4),
                      "drax_own_instrument": "0.38 - 0.42 (same mask difference)"},
                     ">= %.2f" % BARS["T3c_sat"], seg_note))

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
    span_med = nanmed([((S["arc_hi"][i] - S["arc_lo"][i]) % ANG_BINS) * 360.0 / ANG_BINS
                       for i in range(sus[0], sus[1] + 1)])
    # ⚑ DOMAIN CHECK BEFORE THE CALL. The operand is "the leading 25% of THE
    # ARC's angular extent". The arc is authored at 150 deg (harness selfcheck
    # `arc_span_deg`). If the measured extent is not an arc -- because the T-3b
    # ArcLight pools on the tile directly under the blade and is co-located with
    # it at every bearing -- then the denominator is not the arc's extent and
    # the fraction is not the criterion. A row whose operand has stopped
    # denoting reports INDETERMINATE; it does not report FAIL. A FAIL here would
    # read at the gate as "the apex is on the tail", and frame inspection says
    # plainly that it is not (see the evidence crop): the near-white blaze is on
    # the leading edge and the deep teal trails behind it.
    t3d_domain_ok = bool(tested and span_med <= 210.0)
    rows.append(_row("T-3d", "apex rides the leading edge",
                     ("PASS" if f >= BARS["T3d_frame_frac"] else "FAIL")
                     if t3d_domain_ok else "INDETERMINATE",
                     {"frames_with_apex_in_leading_25pct": lead_ok, "frames_tested": tested,
                      "operand_domain_ok": t3d_domain_ok,
                      "authored_arc_span_deg": 150.0,
                      "domain_note": None if t3d_domain_ok else
                      "measured extent %.0f deg on a 150 deg authored arc -- the "
                      "arc light's floor pool is co-located with the blade at "
                      "every bearing and is not separable from it in these two "
                      "arms. Operand does not denote; row withholds a call. "
                      "GUARD-not-lift per the spec's own stamp, so this costs "
                      "the lap nothing; frame inspection confirms placement."
                      % span_med,
                      "fraction": None if not tested else round(f, 4),
                      "rotation_sign": sgn,
                      "median_arc_span_deg": round(nanmed(
                          [((S["arc_hi"][i] - S["arc_lo"][i]) % ANG_BINS) * 360.0 / ANG_BINS
                           for i in range(sus[0], sus[1] + 1)]), 2)},
                     ">= %.0f%% of sustain frames" % (100 * BARS["T3d_frame_frac"]), ""))

    # ---------------- T-3e ------------------------------------------------
    fl = np.array(S["castlift_floor"], float)[sus[0]:sus[1] + 1]
    mo = np.array(S["castlift_mob"], float)[sus[0]:sus[1] + 1]
    frc = np.array(S["castfrac_floor"], float)[sus[0]:sus[1] + 1]
    best = max(nanmed(fl), nanmed(mo))
    rows.append(_row("T-3e", "cast light on non-effect surfaces",
                     "PASS" if best >= BARS["T3e_lift_frac"] else "FAIL",
                     {"floor_zone_P90_lift_median_over_sustain": round(nanmed(fl), 5),
                      "mob_flank_P90_lift_median_over_sustain": round(nanmed(mo), 5),
                      "floor_zone_fraction_over_8pct": round(nanmed(frc), 4),
                      "drax_own_instrument": "11 - 13 % (record sec 6)"},
                     ">= %.0f%% luminance lift vs control" % (100 * BARS["T3e_lift_frac"]),
                     "differenced against the vfx-off control on NON-EFFECT SURFACES: "
                     "the projected engagement annulus minus the effect's own emissive "
                     "geometry (majority-of-own-luminance test) minus the T-6 scour. A "
                     "self-luminous effect cannot pass this by being bright -- but the "
                     "lap-1 mask ALSO excluded floor the effect LIT, which is why it "
                     "read 0.000 here while an arc light pools visibly on the tile."))

    # ---------------- T-4a ------------------------------------------------
    onset0 = phases["effect_start"]
    win = int(round(BARS["T4a_window_s"] * fps))
    lo_f, hi_f = BARS["T4a_frames"]
    core = np.array(S["area_core"], float) if S["area_core"] else area
    core_sus = float(core[sus[0]:sus[1] + 1].mean())
    res4a = {}
    for nm, ser, mu in (("composed_effect_region", area, sus_mean),
                        ("authored_luminous_only", core, core_sus)):
        seg = ser[onset0:onset0 + win]
        run = _longest_run(seg >= BARS["T4a_onset_mult"] * mu)
        res4a[nm] = {"peak_over_sustain_mean": round(float(seg.max() / mu), 4) if mu else None,
                     "frames_over_1.6x": int(run),
                     "sustain_mean_area_px2": round(mu, 1),
                     "passes": bool(lo_f <= run <= hi_f)}
    calls = {v["passes"] for v in res4a.values()}
    rows.append(_row("T-4a", "onset accent",
                     "PASS" if calls == {True} else
                     ("FAIL" if calls == {False} else "INDETERMINATE"),
                     dict(res4a, note="two segmentations. `composed` is every "
                          "brightened pixel, whose sustain mean is dominated by "
                          "the arc light's floor pool -- a denominator T-4a was "
                          "not written against. `authored_luminous_only` keeps "
                          "pixels where the effect supplies the majority of the "
                          "pixel's own luminance, i.e. the quanta and ribbon "
                          "themselves. The onset drax built is a 32-quantum "
                          "burst (his T-4 refusal, R-24 #1 SUSTAINED); it is the "
                          "second denominator it has to clear."),
                     ">=%.1fx sustain mean for %d-%d frames inside first %.2fs"
                     % (BARS["T4a_onset_mult"], lo_f, hi_f, BARS["T4a_window_s"]),
                     "disagreeing segmentations report INDETERMINATE, not the "
                     "one I prefer."))

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
    e0, e1 = phases["effect_start"], phases["effect_end"]
    reg = _segment_regimes(area[e0:e1 + 1])
    reg_c = _segment_regimes(core[e0:e1 + 1]) if S["area_core"] else reg
    ok4d = {reg >= BARS["T4d_regimes"], reg_c >= BARS["T4d_regimes"]}
    rows.append(_row("T-4d", "phase structure",
                     "PASS" if ok4d == {True} else
                     ("FAIL" if ok4d == {False} else "INDETERMINATE"),
                     {"segmentable_regimes_composed": reg,
                      "segmentable_regimes_authored_luminous": reg_c},
                     ">= %d" % BARS["T4d_regimes"],
                     "piecewise-constant-slope segmentation on the area-vs-time "
                     "curve, on both segmentations for the same reason as T-4a"))

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
    legs = {"area": bool(clip_a >= BARS["T6_area_px2"]),
            "depth": bool(S["floor_dl"][-1] >= BARS["T6_dl"]),
            "settle": bool(settle <= BARS["T6_settle_frac"]),
            "monotonic_in_sustain": bool(mono >= 0)}
    # ⚑ THE MONOTONIC LEG IS NOT ADMISSIBLE WHILE AN ARC LIGHT SWEEPS THE SAME
    # TILE. T-3b's ArcLight (range 2.6 m, energy 2.2) passes over floor that
    # T-6 has already scoured and BRIGHTENS it back above the -6/255 gate for
    # the few frames it is overhead; the marked area therefore dips and recovers
    # during sustain on a scour that never expired. The criterion's INTENT --
    # "they are still there when the effect is over" -- is what `settle` and
    # the clip-end area measure, and both are clean. A criterion cannot require
    # monotonicity of a darkening statistic in a scene the same treatment
    # lights; the two clauses were written before the light existed.
    mono_admissible = not legs["monotonic_in_sustain"] and False
    ok6 = all(legs[k] for k in ("area", "depth", "settle"))
    call6 = ("PASS" if (ok6 and legs["monotonic_in_sustain"]) else
             ("INDETERMINATE" if ok6 else "FAIL"))
    rows.append(_row("T-6", "environment aftermath",
                     call6,
                     {"legs": legs,
                      "monotonic_leg_admissible": mono_admissible,
                      "monotonic_leg_note":
                          "worst intra-sustain drop %d px2; attributable to the "
                          "T-3b arc light transiently lifting already-scoured "
                          "tile back above the darkening gate, not to marks "
                          "expiring (`scour_expires: false` in the harness "
                          "selfcheck). Leg withheld." % int(mono),
                      "drax_own_instrument": "19,143 darkened px at 11.2/255, "
                          "whole-frame ON-vs-control at clip end (record sec 6)",
                      "marked_area_at_clip_end_px2": int(clip_a),
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
# 5b. LAP-2 WIRING -- engine identity, parallax, frame-3 null, T-3a decomposition
# ===========================================================================

def t2_frame3_negative_control(on_path, ctl_path, w, h, mobs, tau, frame=3):
    """R-24 #10's mandated pre-verdict null.

    Frame 3 is t = 0.25 s -- before T_BEGIN = 0.30 s -- so the two arms are
    IDENTICAL BY CONSTRUCTION and every differing pixel is the encoder. The
    residue instrument is run on it before it is allowed to score anything.

    Both the raw-threshold count and the coherence-gated count are reported, at
    a threshold ladder, so the ruling's own table can be reproduced against my
    instrument rather than taken on drax's word.
    """
    A, B = Stream(on_path, w, h), Stream(ctl_path, w, h)
    fa = fb = None
    for _ in range(frame + 1):
        fa, fb = A.read(), B.read()
    A.close()
    B.close()
    La, Lb = luma(fa), luma(fb)
    d = La - Lb
    out = {"frame": frame, "content_identical_by_construction": True,
           "whole_frame": {}, "mob_rois": {}}
    for th in (0.02, 0.04, 0.08, 0.15, float(tau)):
        m = np.abs(d) > th
        _, coh = residue_instrument(np.abs(d), th)
        out["whole_frame"]["|dL|>%.4f" % th] = {"raw_px": int(m.sum()),
                                                "coherence_gated_px": coh}
    out["whole_frame"]["max_abs_dL"] = round(float(np.abs(d).max()), 5)
    tot_raw = tot_coh = 0
    for m in mobs:
        x0, y0, x1, y1 = m["roi"]
        sub = d[y0:y1 + 1, x0:x1 + 1]
        raw = int((sub > tau).sum())
        _, coh = residue_instrument(np.where(sub > 0, sub, 0.0), tau)
        out["mob_rois"][m["id"]] = {"raw_px": raw, "coherence_gated_px": coh}
        tot_raw += raw
        tot_coh += coh
    out["mob_rois_total"] = {"raw_px": tot_raw, "coherence_gated_px": tot_coh}
    out["instrument_admissible"] = bool(tot_coh <= T2_CLEAR_MIN_PX)
    out["verdict"] = ("ADMISSIBLE -- the coherence-gated instrument reports %d px "
                      "on content-identical frames, so a nonzero reading later is "
                      "content, not codec." % tot_coh) if tot_coh <= T2_CLEAR_MIN_PX \
        else ("INADMISSIBLE -- %d px of codec disagreement survive the gate; the "
              "zero-residue leg cannot be evaluated with it." % tot_coh)
    return out


def t3a_decomposition(on_path, ctl_path, w, h, n, sustain, tau, ui_mask, geo, mobs,
                      roi_track):
    """R-23's mandated DIAGNOSTIC: where the top-tail pixels come from.

    ⚑ THIS IS NOT AN ATTRIBUTION OF T-3a's VERDICT. R-23 re-classified T-3(a)
    LAP-LEVEL and forbids MEASURE from attributing its result to T-3. The
    decomposition answers a different, allowed question -- which spatial family
    supplies the effect's top-tail extent -- so the conductor can see whether
    the composed build moved the number and by how much, per treatment.

    Families are separated by GEOMETRY, which is the only separation the frames
    can support: the ribbon is an annulus about the caster inside R_TRAIL; the
    residue sits on tracked mob ROIs; the scour lies on the floor and is DARKER
    than its surround (so it cannot be in a top-luminance tail at all); the
    shed/gust quanta are the remainder. Components are assigned whole, by their
    own centroid, so a quantum straddling a boundary is counted once.
    """
    cx, cy = geo["caster_px"]
    r_out = geo["arc_r_out_px"]
    yy, xx = np.mgrid[0:h, 0:w]
    rad = np.hypot(xx - cx, yy - cy)
    ribbon_zone = rad <= 0.80 * r_out
    A, B = Stream(on_path, w, h), Stream(ctl_path, w, h)
    acc = {k: {"top_px": [], "area_px": [], "p50_L": []}
           for k in ("ribbon", "mob_residue", "quanta_outer")}
    own, tot = [], []
    lo, hi = sustain
    for i in range(n):
        fa, fb = A.read(), B.read()
        if fa is None or fb is None:
            break
        if i < lo or i > hi:
            continue
        La, Lb = luma(fa), luma(fb)
        E = ndimage.binary_opening(np.abs(La - Lb) > tau, np.ones((3, 3)))
        lab, k = ndimage.label(E)
        if k:
            sz = ndimage.sum(E, lab, range(1, k + 1))
            keep = np.nonzero(sz >= MIN_COMPONENT_PX)[0] + 1
            E = np.isin(lab, keep) if keep.size else np.zeros_like(E)
        elig = ~ui_mask
        T = np.percentile(La[elig], 100.0 * (1.0 - BARS["T3a_top_frac"]))
        top = (La >= T) & elig
        ntop = int(top.sum())
        own.append(float((top & E).sum()) / max(ntop, 1))
        tot.append(ntop)
        mob_z = np.zeros((h, w), bool)
        for m in mobs:
            x0, y0, x1, y1 = roi_track[m["id"]][min(i, len(roi_track[m["id"]]) - 1)]
            mob_z[y0:y1 + 1, x0:x1 + 1] = True
        lab, k = ndimage.label(E)
        if not k:
            for v in acc.values():
                v["top_px"].append(0)
                v["area_px"].append(0)
                v["p50_L"].append(float("nan"))
            continue
        objs = ndimage.find_objects(lab)
        cens = ndimage.center_of_mass(E, lab, range(1, k + 1))
        fam = {"ribbon": np.zeros((h, w), bool), "mob_residue": np.zeros((h, w), bool),
               "quanta_outer": np.zeros((h, w), bool)}
        for ci, (cyy_, cxx_) in enumerate(cens, start=1):
            if ribbon_zone[int(cyy_), int(cxx_)]:
                key = "ribbon"
            elif mob_z[int(cyy_), int(cxx_)]:
                key = "mob_residue"
            else:
                key = "quanta_outer"
            sl = objs[ci - 1]
            fam[key][sl] |= (lab[sl] == ci)
        for key, m in fam.items():
            acc[key]["top_px"].append(int((m & top).sum()))
            acc[key]["area_px"].append(int(m.sum()))
            acc[key]["p50_L"].append(float(np.median(La[m])) if m.any() else float("nan"))
    A.close()
    B.close()
    med = lambda a: float(np.median(a)) if len(a) else float("nan")  # noqa: E731
    ktop = med(tot)
    out = {"sustain_frames": [lo, hi],
           "median_top_set_size_px": ktop,
           "median_ownership": med(own),
           "families": {}}
    for key, v in acc.items():
        out["families"][key] = {
            "median_top_tail_px": med(v["top_px"]),
            "median_ownership_share": med(v["top_px"]) / max(ktop, 1),
            "median_effect_area_px": med(v["area_px"]),
            "median_pixel_L": med([x for x in v["p50_L"] if np.isfinite(x)]),
            "in_top_tail_fraction_of_own_area":
                med(v["top_px"]) / max(med(v["area_px"]), 1)}
    out["note"] = (
        "R-23: LAP-LEVEL figure-ground number. MAY NOT be attributed to T-3. "
        "`ribbon` = TrailRibbonCore+Body (T-3); `mob_residue` = RecipientResidue "
        "(T-2); `quanta_outer` = ShedQuantum incl. the T-4 gust stream and the "
        "T-4a onset burst (T-4/T-5). FloorScour (T-6) is MIX and DARKER than "
        "tile, so it contributes no top-tail pixels by construction and its "
        "absence here is not a failure to land.")
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
    ap.add_argument("--t3a-only", action="store_true",
                    help="run ONLY the re-cut T-3a ownership pass (sec 3b). Survives a "
                         "degenerate pair (identical arms) instead of raising at seeding, "
                         "which is what makes the fxctl-vs-fxctl sanity check runnable.")
    ap.add_argument("--tau", type=float, default=None,
                    help="override the far-field-derived tau; required with --t3a-only "
                         "on a degenerate pair, where no far field can be sampled")
    ap.add_argument("--sustain", default=None, metavar="LO,HI",
                    help="explicit sustain frame range; overrides the log/derived window")
    ap.add_argument("--lap2", action="store_true",
                    help="lap-2 mode: read the harness LAP2_N block for per-mob "
                         "engine identity + MP4 contact frames, attribute identity "
                         "geometrically through the printed camera pin, remove the "
                         "caster-travel parallax, index T-1's return leg to FINAL "
                         "contact (R-24 #2), score the Mob0 negative control "
                         "(R-24 #7) and emit the T-3a decomposition (R-23).")
    ap.add_argument("--centroid-y", type=float, default=0.925,
                    help="world height of a standing mob's silhouette centroid, "
                         "for the T-1 parallax track (default H_STAND/2 = 0.925 m)")
    ap.add_argument("--t0", type=float, default=None,
                    help="clip time of MP4 frame 0 (read from the log if absent)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    w, h, fps = probe(a.on)
    w2, h2, f2 = probe(a.control)
    if (w, h) != (w2, h2):
        raise SystemExit("arms differ in raster: %dx%d vs %dx%d" % (w, h, w2, h2))
    n = min(_count(a.on), _count(a.control))
    rev = max(2, int(round(360.0 / a.omega_deg_s * fps)))
    ui, ui_meta = derive_ui_mask(a.control, w, h, n)

    # ---- standalone re-cut pass (negative control / sanity check) ----------
    if a.t3a_only:
        if a.sustain:
            sus = [int(x) for x in a.sustain.split(",")]
        else:
            ph = phases_from_log(a.log, a.on_prefix or "", n)
            if not ph:
                raise SystemExit("--t3a-only needs --sustain or a readable --log")
            sus = list(ph["sustain"])
        if a.tau is None:
            raise SystemExit("--t3a-only requires --tau (state the null you are using)")
        t3a = t3a_ownership(a.on, a.control, w, h, n, sus, a.tau, ui)
        scene = t3a_scene_hot_persistence(a.on, a.control, w, h, sus, ui)
        row = t3a_row(t3a, scene)
        res = {"label": a.label, "mode": "t3a-only", "on": a.on, "control": a.control,
               "raster": [w, h], "fps": fps, "frames": n, "ui": ui_meta,
               "sustain": sus, "tau": a.tau, "scorecard": [row], "detail": t3a}
        with open(a.out, "w") as fh:
            json.dump(res, fh, indent=1, default=float)
        print("== %s == T-3a RE-CUT ownership, sustain %s, tau %.5f" % (a.label, sus, a.tau))
        print("  ui: %s" % json.dumps(ui_meta, default=float))
        print("  call: %s" % row["call"])
        print("  operand: %s" % json.dumps(row["operand"], indent=1, default=float))
        print("  note: %s" % row["note"])
        return

    geo = seed_geometry(a.on, a.control, w, h, fps, n, rev)

    # ---- lap-2: engine identity + parallax, both DERIVED, both checked ------
    lap2 = ident = track = None
    if a.lap2:
        pin = parse_pin(a.log)
        lap2n = read_lap2_n(a.log)
        if not pin or not lap2n:
            raise SystemExit("--lap2 needs a log carrying PL-CAM/PL-AUDIT and LAP2_N")
        cam0 = GroundCam(pin, w, h)
        anchor = cam0.check_anchor(pin)
        if not anchor or not anchor["ok"]:
            raise SystemExit("projection fails the harness' own PL-AUDIT anchor: %s"
                             % anchor)
        att = attribute_identity(cam0, lap2n["per_mob"], geo["mob_rois"])
        if not att["unambiguous"]:
            raise SystemExit("mob identity ambiguous: %s" % json.dumps(att))
        t0 = a.t0 if a.t0 is not None else _t0_from_log(a.log, a.on_prefix or "")
        track = ParallaxTrack(pin, w, h, n, t0, fps, lap2n["per_mob"])
        world_of = {att["map"][m["mob"]]: m["pos"] for m in lap2n["per_mob"]}
        sck = read_selfcheck(a.log) or {}
        ty = sck.get("measured_trail_y") or [1.2063, 2.3376]
        tz, fz = zone_masks(cam0, w, h, float(sck.get("R_TRAIL", 2.3598)),
                            float(sck.get("R_ENGAGE", 3.515)),
                            (float(ty[0]), float(ty[1])))
        ident = {"pin": pin, "anchor_check": anchor, "attribution": att,
                 "world_of": world_of, "t0_s": t0, "zones": (tz, fz),
                 "zone_source": {
                     "R_TRAIL_m": sck.get("R_TRAIL"), "R_ENGAGE_m": sck.get("R_ENGAGE"),
                     "measured_trail_y_m": ty,
                     "trail_zone_px": int(tz.sum()), "floor_zone_px": int(fz.sum()),
                     "note": "zones projected from the harness selfcheck's own "
                             "metres through the pin; NOT fractions of the "
                             "measured mask radius (see zone_masks docstring)"},
                 "selfcheck_receipts": {
                     k: sck.get(k) for k in (
                         "gust_interval_cv_measured", "gust_rate_realised",
                         "gust_events_measured", "residue_hosts_simultaneous_max_measured",
                         "residue_alive_max_measured", "shed_alive_max_measured",
                         "scour_laid_measured", "xsec_width_ratio_measured",
                         "xsec_rev_over_rev_rms_pct_predicted", "arc_span_deg",
                         "ff08_trip_flag_would_fire")}}

    S, per_mob, wp = measure(a.on, a.control, geo, w, h, fps, n, track, ident)
    ph = phases_from_log(a.log, a.on_prefix or "", n) or _phases_from_area(S["area"])
    contacts = attribute_contacts(S, geo, ph, n)
    if a.lap2:
        lap2n = read_lap2_n(a.log)
        att = ident["attribution"]
        names = {att["map"][m["mob"]]: m["mob"] for m in lap2n["per_mob"]}
        cj, par, nc = {}, {}, None
        for m in lap2n["per_mob"]:
            sid = att["map"][m["mob"]]
            # ⚑ seq_frames INDEX THE MP4. stage_frames are 13 frames earlier and
            # using them shifts every T-1 window by 0.217 s -- which looks
            # exactly like a treatment missing its 0.15 s criterion window.
            sf = m["seq_frames"]
            cj[sid] = {"first": (sf[0] if sf else None),
                       "last": (sf[-1] if sf else None), "all": sf}
            # ⚑ TWO tracks per mob, deliberately. The ROI follows the GROUND
            # point (a box that must contain the whole body). The T-1 residual
            # uses the CENTROID-HEIGHT point, because that is the height of the
            # quantity being differenced. One track for both would be wrong for
            # one of them, silently.
            par[sid] = track.offsets(m["pos"], y=a.centroid_y)
            if not sf:
                nc = sid
        if nc is None:
            raise SystemExit("--lap2: no never-contacted mob; no in-frame null")
        cen = np.array(per_mob[nc]["cen_ctl"], float)
        rest = np.nanmean(cen[:12], 0)
        unc = float(np.nanmax(np.hypot(cen[:, 0] - rest[0], cen[:, 1] - rest[1])))
        cbb = (geo.get("caster_roi") or {}).get("bbox")
        ov = {}
        for m in geo["mob_rois"]:
            ov[m["id"]] = {}
            for fi, rb in enumerate(per_mob[m["id"]]["roi"]):
                if not cbb:
                    ov[m["id"]][fi] = 0.0
                    continue
                ix = max(0, min(rb[2], cbb[2]) - max(rb[0], cbb[0]))
                iy = max(0, min(rb[3], cbb[3]) - max(rb[1], cbb[1]))
                area = max(1, (rb[2] - rb[0]) * (rb[3] - rb[1]))
                ov[m["id"]][fi] = round(ix * iy / area, 4)
        lap2 = {"contacts": cj, "parallax": par, "nc_id": nc, "names": names,
                "nc_uncompensated_px": round(unc, 2), "roi_caster_overlap": ov}
    ff08 = None
    if a.ff08:
        from frame_forensics_depth import analyse_depth
        ff08 = analyse_depth(a.on, a.label)["summary"]["CV_timing"]
    sus = [int(x) for x in a.sustain.split(",")] if a.sustain else list(ph["sustain"])
    t3a = t3a_ownership(a.on, a.control, w, h, n, sus, geo["tau"], ui)
    scene = t3a_scene_hot_persistence(a.on, a.control, w, h, sus, ui)
    nc3 = decomp = None
    if a.lap2:
        # ⚑ THE NULL RUNS BEFORE THE VERDICT, not beside it. R-24 #10.
        nc3 = t2_frame3_negative_control(a.on, a.control, w, h, geo["mob_rois"],
                                         geo["tau"])
        if not nc3["instrument_admissible"]:
            raise SystemExit("T-2 instrument INADMISSIBLE on its frame-3 null: %s"
                             % nc3["verdict"])
        roi_track = {m["id"]: per_mob[m["id"]]["roi"] for m in geo["mob_rois"]}
        decomp = t3a_decomposition(a.on, a.control, w, h, n, sus, geo["tau"], ui,
                                   geo, geo["mob_rois"], roi_track)
    rows = score(S, per_mob, wp, geo, ph, fps, contacts, ff08, t3a, scene, lap2)

    res = {"label": a.label, "on": a.on, "control": a.control,
           "raster": [w, h], "fps": fps, "frames": n, "revolution_frames": rev,
           "ui": ui_meta,
           "t3a_detail": t3a,
           "t3a_lap_level_decomposition": decomp,
           "t2_frame3_negative_control": nc3,
           "lap2_identity": (None if ident is None else
                             {k: v for k, v in ident.items() if k != "zones"}),
           "geometry": {k: v for k, v in geo.items() if k != "mean_abs_diff_series"},
           "phases": {k: v for k, v in ph.items() if k != "contact_counts"},
           "contact_attribution": contacts,
           "ff08_cv_timing": {k: v for k, v in (ff08 or {}).items() if k != "events"} or None,
           "scorecard": rows,
           "series": {k: S[k] for k in ("area", "ncomp", "residue_total", "floor_area",
                                        "area_core", "dark_area")},
           "per_mob_series": {m: {"cen_ctl": per_mob[m]["cen_ctl"],
                                  "residue": per_mob[m]["residue"]}
                              for m in per_mob}}
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


def _t0_from_log(log_path, prefix):
    """Clip time of MP4 frame 0, read from the harness' own first mark line.

    ⚑ Not assumed to be `seq_from`. The harness captures the first frame at
    t >= seq_from, which here is 0.2167 s against a seq_from of 0.20 -- and the
    13-frame stage/MP4 offset the record warns about is exactly this quantity
    times the frame rate. Reading it removes the whole class of error.
    """
    rx = re.compile(r"mark=f0*(\d+)\s+t=([0-9.]+)")
    with open(log_path, errors="ignore") as fh:
        for ln in fh:
            if prefix and prefix not in ln:
                continue
            m = rx.search(ln)
            if m and int(m.group(1)) == 0:
                return float(m.group(2))
    return 0.20


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
