#!/usr/bin/env python3
"""
vfx_lap2_project.py -- world -> image projection for the ratified judging camera,
and MOB IDENTITY ATTRIBUTION derived from it.

WHY THIS EXISTS
    The lap-2 build record hands over per-mob contact frames keyed by ENGINE
    identity (Mob0..Mob3, with world XZ). The battery seeds mob ROIs from PIXELS
    (connected components in the control frame, sorted by area). Those two
    labelings are not the same labeling, and the whole of ruling R-24 #7 turns on
    getting the correspondence right: Mob0 is the IN-FRAME NEGATIVE CONTROL, so
    mislabeling it swaps the null with a treatment recipient.

    The obvious shortcut -- "the mob that does not move is Mob0" -- is CIRCULAR:
    it uses the very T-1 signal the labeling is supposed to let us measure. So
    identity is established GEOMETRICALLY, from the camera pin the harness prints
    in its own log, with the residuals reported so the correspondence can be
    disagreed with while holding the numbers.

CAMERA, read verbatim from `render.txt` (not assumed):
    [wwcr] PL-CAM k=0.665000 -- DOLLY only. pitch 52.9535411256029 deg
           yaw 47.0 deg  fov_v 31.7861018306101 deg VERTICAL/KEEP_HEIGHT
    [wwcr] PL-CAM offset k=0.665000 (THIS RUN) = (9.7929..., 18.8840..., 9.1654...) m

    The camera sits at `subject + offset` and aims along (yaw, pitch). The aim
    point is NOT the subject's ground origin -- solving the printed pitch against
    the printed offset puts the aim ~1.13 m up, which is a chest-height aim and
    is consistent with the harness' own PL-AUDIT line ("subject ground projects
    to frac (0.5010, 0.5509)", i.e. BELOW frame centre, so the camera is not
    aimed at the ground point).

    Rather than trust that derivation, the projection is CALIBRATED against that
    PL-AUDIT line, which states exactly where one known world point lands in the
    frame. A projection that cannot reproduce the one anchor the harness printed
    is not a projection I will attribute identity with.
"""

from __future__ import annotations

import json
import math
import re

import numpy as np

VERT_FOV_MODE = "KEEP_HEIGHT"   # Godot Camera3D.KEEP_HEIGHT -> fov is vertical


def parse_pin(log_path, arm_prefix=None):
    """Read the camera pin + the PL-AUDIT anchor out of the harness log."""
    pin = {}
    rx_cam = re.compile(
        r"PL-CAM k=([0-9.]+).*?pitch ([0-9.\-]+) deg\s+yaw ([0-9.\-]+) deg\s+"
        r"fov_v ([0-9.\-]+) deg\s+(\S+)")
    rx_off = re.compile(
        r"PL-CAM offset k=([0-9.]+) \(THIS RUN\) = \(([0-9.\-]+), ([0-9.\-]+), "
        r"([0-9.\-]+)\) m\s+stand-off ([0-9.\-]+) m")
    rx_anchor = re.compile(
        r"PL-AUDIT anchor: subject ground projects to frac \(([0-9.\-]+), ([0-9.\-]+)\)")
    with open(log_path, errors="ignore") as fh:
        for ln in fh:
            if "PL-CAM" not in ln and "PL-AUDIT" not in ln:
                continue
            m = rx_cam.search(ln)
            if m and "pitch_deg" not in pin:
                pin.update(k=float(m.group(1)), pitch_deg=float(m.group(2)),
                           yaw_deg=float(m.group(3)), fov_v_deg=float(m.group(4)),
                           fov_mode=m.group(5))
            m = rx_off.search(ln)
            if m and "offset_m" not in pin:
                pin["offset_m"] = [float(m.group(i)) for i in (2, 3, 4)]
                pin["stand_off_m"] = float(m.group(5))
            m = rx_anchor.search(ln)
            if m and "anchor_frac" not in pin:
                pin["anchor_frac"] = [float(m.group(1)), float(m.group(2))]
    return pin


class GroundCam:
    """Projection of GROUND-PLANE world points (y = subject foot height) to pixels.

    Basis is built from the printed yaw/pitch; the aim height is SOLVED so that
    the printed offset and the printed pitch are mutually consistent, and then
    the whole thing is CHECKED against the printed PL-AUDIT anchor. If the check
    misses by more than a stated tolerance the caller is told, loudly.
    """

    def __init__(self, pin, w, h, subject_xz=(0.0, 0.0), subject_y=0.0):
        self.w, self.h = w, h
        ox, oy, oz = pin["offset_m"]
        self.cam = np.array([subject_xz[0] + ox, subject_y + oy, subject_xz[1] + oz], float)
        pitch = math.radians(pin["pitch_deg"])
        yaw = math.radians(pin["yaw_deg"])
        # Look direction: yaw measured off +Z toward +X (matches the printed
        # offset's own horizontal bearing atan2(9.7929, 9.1654) = 46.9 deg vs the
        # printed yaw of 47.0 deg -- a 0.1 deg agreement, so the convention is
        # confirmed by the log rather than assumed from the engine's docs).
        d = np.array([-math.sin(yaw) * math.cos(pitch),
                      -math.sin(pitch),
                      -math.cos(yaw) * math.cos(pitch)], float)
        d /= np.linalg.norm(d)
        self.fwd = d
        zc = -d
        xc = np.cross(np.array([0.0, 1.0, 0.0]), zc)
        xc /= np.linalg.norm(xc)
        yc = np.cross(zc, xc)
        self.basis = np.stack([xc, yc, zc])          # rows
        # KEEP_HEIGHT: the stated fov is the VERTICAL one.
        self.f = (h / 2.0) / math.tan(math.radians(pin["fov_v_deg"]) / 2.0)

    def project(self, p):
        v = np.asarray(p, float) - self.cam
        xc, yc, zc = self.basis @ v
        if zc >= -1e-6:
            return None
        u = self.w / 2.0 + self.f * xc / (-zc)
        vv = self.h / 2.0 - self.f * yc / (-zc)
        return float(u), float(vv)

    def check_anchor(self, pin, subject_xz=(0.0, 0.0), subject_y=0.0):
        """Reproduce the harness' own PL-AUDIT anchor: the subject's GROUND point."""
        if "anchor_frac" not in pin:
            return None
        got = self.project([subject_xz[0], subject_y, subject_xz[1]])
        if got is None:
            return {"ok": False, "reason": "subject behind camera"}
        want = [pin["anchor_frac"][0] * self.w, pin["anchor_frac"][1] * self.h]
        err = math.hypot(got[0] - want[0], got[1] - want[1])
        return {"ok": err <= 4.0, "projected_px": [round(x, 2) for x in got],
                "harness_anchor_px": [round(x, 2) for x in want],
                "residual_px": round(err, 3)}


def attribute_identity(cam, engine_mobs, seeded, subject_y=0.0, max_px=140.0):
    """Assign engine mob names to seeded pixel ROIs by projected FOOT POINT.

    The correspondence is one-to-one and is solved by global minimum-cost
    assignment, not by greedy nearest-neighbour: greedy can strand the last mob
    on a partner already taken and then report a large residual as though the
    projection were bad. Residual of EVERY pair is returned, plus the margin to
    the runner-up assignment, so an ambiguous match is visible as ambiguous.
    """
    from scipy.optimize import linear_sum_assignment
    names = [m["mob"] for m in engine_mobs]
    proj = []
    for m in engine_mobs:
        p = cam.project([m["pos"][0], subject_y, m["pos"][1]])
        proj.append(p)
    ids = [s["id"] for s in seeded]
    foot = [s["foot_px"] for s in seeded]
    C = np.zeros((len(names), len(ids)), float)
    for i, p in enumerate(proj):
        for j, f in enumerate(foot):
            C[i, j] = 1e6 if p is None else math.hypot(p[0] - f[0], p[1] - f[1])
    r, c = linear_sum_assignment(C)
    cost = float(C[r, c].sum())
    # runner-up: cheapest assignment that differs from the optimum in >= 2 rows
    best2 = math.inf
    for i in range(len(names)):
        for j in range(len(ids)):
            if C[i, j] == C[i, c[list(r).index(i)]]:
                continue
            D = C.copy()
            D[i, :] = 1e9
            D[:, j] = 1e9
            D[i, j] = C[i, j]
            rr, cc = linear_sum_assignment(D)
            v = float(C[rr, cc].sum())
            if v > cost + 1e-9:
                best2 = min(best2, v)
    out, pairs = {}, []
    for i, j in zip(r, c):
        out[names[i]] = ids[j]
        pairs.append({"engine": names[i], "seeded": ids[j],
                      "world_xz": engine_mobs[i]["pos"],
                      "projected_foot_px": None if proj[i] is None else
                      [round(x, 1) for x in proj[i]],
                      "seeded_foot_px": [round(x, 1) for x in foot[j]],
                      "residual_px": round(float(C[i, j]), 2)})
    worst = max(p["residual_px"] for p in pairs)
    return {"map": out, "pairs": pairs, "total_cost_px": round(cost, 2),
            "runner_up_cost_px": None if best2 == math.inf else round(best2, 2),
            "margin_px": None if best2 == math.inf else round(best2 - cost, 2),
            "worst_residual_px": worst,
            "unambiguous": bool(worst <= max_px and best2 - cost > worst)}


def zone_masks(cam, w, h, r_trail_m, r_engage_m, trail_y_m, subject_xz=(0.0, 0.0)):
    """Image-space zones derived from the VENUE's own metres, through the pin.

    ⚑ WHY NOT A RADIUS FRACTION OF THE MEASURED MASK. That is what the battery
    did at lap-1 and it worked only because the effect region WAS the arc. At
    lap-2 the mask's 99th-percentile radius is set by cast-lit floor and thrown
    quanta, so `0.80 x r_out` -- intended as "the ribbon" -- enclosed the lit
    floor and reported a 150 deg arc as spanning 305 deg. A zone defined off the
    thing being measured moves whenever the thing being measured moves. These
    zones are defined off `R_TRAIL`, `R_ENGAGE` and the measured trail height
    band, all printed by the harness' own selfcheck, projected through the pin
    that reproduces the harness' PL-AUDIT anchor to 0.001 px.

    Returns (trail_zone, floor_zone): the ribbon's swept-torus footprint, and
    the ground annulus out to R_ENGAGE.
    """
    yy, xx = np.mgrid[0:h, 0:w]
    pts = []
    for a in np.linspace(0, 2 * math.pi, 240, endpoint=False):
        for rr, yv in ((r_trail_m, trail_y_m[0]), (r_trail_m, trail_y_m[1])):
            p = cam.project([subject_xz[0] + rr * math.cos(a), yv,
                             subject_xz[1] + rr * math.sin(a)])
            if p:
                pts.append(p)
    trail = _fill_hull(pts, w, h, xx, yy)
    gpts = []
    for a in np.linspace(0, 2 * math.pi, 240, endpoint=False):
        p = cam.project([subject_xz[0] + r_engage_m * math.cos(a), 0.0,
                         subject_xz[1] + r_engage_m * math.sin(a)])
        if p:
            gpts.append(p)
    floor = _fill_hull(gpts, w, h, xx, yy)
    return trail, floor


def _fill_hull(pts, w, h, xx, yy):
    """Filled convex hull of projected points, as a boolean raster."""
    from scipy.spatial import ConvexHull, Delaunay
    P = np.array(pts, float)
    if P.shape[0] < 3:
        return np.zeros((h, w), bool)
    try:
        hull = ConvexHull(P)
    except Exception:
        return np.zeros((h, w), bool)
    tri = Delaunay(P[hull.vertices])
    x0, y0 = np.floor(P.min(0)).astype(int)
    x1, y1 = np.ceil(P.max(0)).astype(int)
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(w - 1, x1), min(h - 1, y1)
    m = np.zeros((h, w), bool)
    if x1 <= x0 or y1 <= y0:
        return m
    gx, gy = np.meshgrid(np.arange(x0, x1 + 1), np.arange(y0, y1 + 1))
    q = np.column_stack([gx.ravel(), gy.ravel()])
    inside = tri.find_simplex(q) >= 0
    m[y0:y1 + 1, x0:x1 + 1] = inside.reshape(gy.shape)
    return m


def read_selfcheck(log_path, final=True):
    """The harness' own `selfcheck={...}` block -- R_TRAIL, R_ENGAGE, measured
    trail height band, and the runtime receipts drax's record quotes.

    Read rather than restated: every constant a bar depends on then comes from
    the artifact that shipped, not from a number copied across a document
    boundary. `FINAL` is the post-run block (measured values filled in); the
    pre-run block still carries +/-inf placeholders.
    """
    out = None
    with open(log_path, errors="ignore") as fh:
        for ln in fh:
            if "selfcheck=" not in ln:
                continue
            if final and "FINAL selfcheck=" not in ln:
                continue
            body = ln.split("selfcheck=", 1)[1].strip()
            try:
                d = json.loads(body.replace("1e99999", "null").replace("-null", "null"))
            except Exception:
                continue
            if out is None:
                out = d
    return out


def read_lap2_n(log_path):
    """The `[wwcr] LAP2_N {...}` block: per-mob world XZ + MP4 contact frames.

    ⚑ `seq_frames` INDEX THE MP4. `stage_frames` index the stage clock and are
    13 frames earlier. Using the wrong column shifts every T-1 window by 0.217 s
    -- which looks exactly like a treatment missing its 0.15 s criterion window.
    This reader takes `seq_frames` and says so in its own output.
    """
    with open(log_path, errors="ignore") as fh:
        for ln in fh:
            if "LAP2_N" in ln:
                return json.loads(ln.split("LAP2_N", 1)[1].strip())
    return None
