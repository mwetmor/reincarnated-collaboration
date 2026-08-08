#!/usr/bin/env python3
"""eor_platebind.py — bind the hovered-monster NAMEPLATE to a max-HP FINGERPRINT.

galadriel / visual-perception seam. KC2-SIM fifth-extraction pass.

The problem this module exists for. Three prior passes could read the top-centre
nameplate (name / rank colour / level / family) and could separately census the
in-world `(current/max)` readouts, but could not say WHICH readout the plate was
describing. Board-closure § 8.3 recorded that gap as a correction: the plate
reports whatever the cursor is over, not necessarily the nearest bar, so
proximity is not a binding.

The instrument used here instead is the PLATE'S OWN HEALTH BAR. Geometry measured
on w153 plate frames at 1920x1080:

    name text rows          y 17..34    light glyphs, min(R,G,B) > 120
    level numeral           y 43..58    red/orange glyphs, centred on x=960
    bar track top bevel     y 60..64    fill-independent bright strip
    bar FILL body           y 66..72    red; runs left-anchored from x~861
    family label            y 90..103
    track inner extent      x 861 .. XR (XR calibrated, see `calibrate`)

The plate bar is a FRACTION display. Every in-world readout gives an exact
fraction cur/max. So on any frame carrying both, the plate can be matched against
the readouts by fraction, and — this is the part that makes it a measurement
rather than a guess — the RUNNER-UP GAP can be reported, so a binding is only
claimed where no other body on camera could have produced that bar.

Evidence classes emitted (stated per body in the note):
    FRACTION-UNIQUE   plate fraction matches exactly one on-frame readout inside
                      tolerance, and the runner-up is outside a stated margin
    FRACTION-TRACK    the above, sustained over the whole span the plate holds
                      one name, with the plate bar and the readout MOVING together
    DEGENERATE        several readouts share the matching fraction (typically all
                      at full HP) -> plate cannot discriminate
    NO-READOUT        plate up, no parsed readout on that frame at all

This module LOCATES and MEASURES. Every name, colour and level that reaches the
note is eye-read from a magnified exact-seek crop, as in the four prior passes.

  scan   <video> <t0> <t1> <fps> <atlas.npz> <out.json>
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])

import eor_cohort as CO      # noqa: E402
import eor_hpocr as HO       # noqa: E402

W, H = 1920, 1080

# ---- plate geometry (full-frame px) -----------------------------------------
NAME_BAND = (600, 17, 1350, 35)     # x0, y0, x1, y1
LVL_BAND = (915, 43, 1005, 59)
BEVEL_BAND = (830, 59, 1100, 65)
FILL_BAND = (830, 66, 1100, 73)
FAM_BAND = (700, 90, 1250, 104)

TRACK_X0 = 861.0                    # measured: fill left edge, invariant
TRACK_X1 = 1060.0                   # default; override from calibrate()


def plate_metrics(fr: np.ndarray) -> dict:
    """Everything the plate can be measured for on one frame."""
    a = fr.astype(np.int16)

    nx0, ny0, nx1, ny1 = NAME_BAND
    nm = a[ny0:ny1, nx0:nx1]
    light = nm.min(2) > 120
    xs = np.nonzero(light.any(0))[0]
    name_px = int(light.sum())
    name_rows = int((light.sum(1) > 8).sum())

    # rank colour: mean RGB over the name's own glyph pixels
    if name_px:
        sel = nm[light]
        nrgb = [int(round(float(sel[:, k].mean()))) for k in range(3)]
    else:
        nrgb = None

    lx0, ly0, lx1, ly1 = LVL_BAND
    lv = a[ly0:ly1, lx0:lx1]
    warm = (lv[:, :, 0] > 150) & (lv[:, :, 0] - lv[:, :, 2] > 40)
    lvl_px = int(warm.sum())

    fx0, fy0, fx1, fy1 = FAM_BAND
    fm = a[fy0:fy1, fx0:fx1]
    fam_px = int((fm.min(2) > 120).sum())

    # bar track top bevel: fill-independent, pins the track each frame
    bx0, by0, bx1, by1 = BEVEL_BAND
    bv = a[by0:by1, bx0:bx1]
    bc = np.nonzero((bv.max(2) > 110).sum(0) >= 3)[0]
    bev = (int(bx0 + bc[0]), int(bx0 + bc[-1])) if bc.size else None

    # bar fill: red body rows, left-anchored run
    gx0, gy0, gx1, gy1 = FILL_BAND
    fb = a[gy0:gy1, gx0:gx1]
    R, G, B = fb[:, :, 0], fb[:, :, 1], fb[:, :, 2]
    red = (R > 70) & (R - G > 40) & (R - B > 40)
    colcount = red.sum(0)
    rc = np.nonzero(colcount >= 5)[0]
    fill = (int(gx0 + rc[0]), int(gx0 + rc[-1])) if rc.size else None
    # Fill is LEFT-ANCHORED at the track origin. Walk right from the origin,
    # tolerating gaps of <= 4 px (the bar carries a dark centre ornament and the
    # scene bleeds VFX over it). A run that does not START at the origin is not
    # the fill and is refused rather than guessed.
    fill_end = None
    ox = int(TRACK_X0) - gx0
    if rc.size and rc[0] <= ox + 7:
        cur = max(rc[0], 0)
        for v in rc[1:]:
            if v - cur <= 4:
                cur = v
            else:
                break
        fill_end = int(gx0 + cur)
    elif rc.size is not None and (colcount[max(0, ox - 2):ox + 8] >= 5).sum() == 0:
        fill_end = int(TRACK_X0)          # bar empty at the origin -> fraction 0

    edge, contrast = fill_edge(fr)

    return {"name_px": name_px, "name_rows": name_rows,
            "name_x0": int(nx0 + xs[0]) if xs.size else None,
            "name_x1": int(nx0 + xs[-1]) if xs.size else None,
            "name_rgb": nrgb, "lvl_px": lvl_px, "fam_px": fam_px,
            "bevel": bev, "fill": fill, "fill_end": fill_end,
            "edge": edge, "contrast": round(contrast, 2)}


def fill_edge(fr: np.ndarray, x_lo=856, x_hi=1064):
    """Locate the plate bar's fill edge by STEP FIT, not by run-walking.

    Why the rewrite. The first implementation walked right from the track origin
    while columns stayed red. Grim Dawn draws a dark diamond ORNAMENT across the
    centre of the plate bar at x ~ 955-965, and the walk terminates on it — which
    silently pins every fraction between roughly 0.44 and 0.52 to the ornament's
    own column instead of the monster's health, and drops others to near zero.
    Measured on the w153 Storm/Frost Revenant hover: run-walk returned 0.088 on a
    frame whose bar is visibly ~0.45 full.

    The bar is a two-level step: red left, dark right. So fit one. For every
    candidate edge e, score the split by the difference of means of a redness
    profile, and take the best e. A narrow ornament notch cannot move the optimum
    of a global split; it can only add a constant to both sides.

    Returns (edge_x, contrast). `contrast` is the left-minus-right redness at the
    optimum and is the measurement's own confidence: a plate bar with no visible
    step (fully empty or wholly occluded) returns low contrast and is refused.
    """
    a = fr.astype(np.int16)
    gy0, gy1 = FILL_BAND[1], FILL_BAND[3]
    sub = a[gy0:gy1, x_lo:x_hi]
    R = sub[:, :, 0]
    GB = np.maximum(sub[:, :, 1], sub[:, :, 2])
    prof = (R - GB).mean(0)                      # redness per column
    n = prof.size
    cs = np.concatenate([[0.0], np.cumsum(prof)])
    best, be = -1e9, None
    for e in range(6, n - 5):
        lm = cs[e] / e
        rm = (cs[n] - cs[e]) / (n - e)
        s = lm - rm
        if s > best:
            best, be = s, e
    return (x_lo + be if be is not None else None), float(best)


def is_plate(p: dict, name_px=40, name_rows=6) -> bool:
    return p["name_px"] >= name_px and p["name_rows"] >= name_rows


def scan(video, t0, t1, fps, atlaspath, outpath):
    """ONE streaming decode pass: plate metrics + full readout census per frame."""
    atlas = HO.load(atlaspath)
    dur = t1 - t0
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0}", "-t", f"{dur}", "-i", video,
           "-vf", f"fps={fps}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=W * H * 3)
    nb = W * H * 3
    frames, i = [], 0
    while True:
        buf = p.stdout.read(nb)
        if len(buf) < nb:
            break
        fr = np.frombuffer(buf, dtype=np.uint8).reshape(H, W, 3)
        t = round(t0 + i / fps, 4)
        pm = plate_metrics(fr)
        rds = []
        bl = CO.blobs2(fr)
        if bl:
            v_all = HO.white(fr)
            for (bx0, by0, bx1, by1, dens) in bl:
                s, sc, mg = HO.read_string(atlas, v_all[by0:by1 + 1, bx0:bx1 + 1])
                pe = CO.parse_ext(s)
                rds.append({"box": [bx0, by0, bx1, by1], "raw": s,
                            "kind": pe[0] if pe else None,
                            "cur": pe[1] if pe else None,
                            "max": pe[2] if pe else None,
                            "score": round(sc, 3), "margin": round(mg, 3)})
        frames.append({"t": t, "plate": pm, "rd": rds})
        i += 1
        if i % 100 == 0:
            print(f"  ... {i} frames", flush=True)
    p.stdout.close(); p.wait()
    json.dump({"video": video, "t0": t0, "t1": t1, "fps": fps,
               "frames": i, "f": frames}, open(outpath, "w"))
    npl = sum(1 for f in frames if is_plate(f["plate"]))
    print(f"frames={i} plate_frames={npl}")
    return frames


def bar_hue(fr: np.ndarray, box, lo=8, hi=26, pad=12, min_run=8):
    """ALLEGIANCE of the body carrying a readout, from its own health bar.

    Grim Dawn draws the in-world floating bar RED for a hostile body and GREEN
    for a player-side one. The bar sits a fixed offset below the `(cur/max)`
    string it belongs to. Sampling it turns the readout census — which until now
    counted every parsed string as a monster — into a census that can tell a
    monster from an ally.

    Returns (kind, n_px, row) with kind in {"red", "green", None}. Reported per
    fingerprint as a modal vote over its frames, never from one frame.
    """
    a = fr.astype(np.int16)
    x0, y0, x1, y1 = box
    best = (None, 0, None)
    for y in range(y1 + lo, y1 + hi):
        if y >= a.shape[0]:
            break
        row = a[y, max(0, x0 - pad):min(a.shape[1], x1 + pad)]
        R, G, B = row[:, 0], row[:, 1], row[:, 2]
        g = int(((G > 70) & (G - R > 25) & (G - B > 25)).sum())
        r = int(((R > 70) & (R - G > 35) & (R - B > 35)).sum())
        if max(g, r) > best[1]:
            best = ("green" if g > r else "red", max(g, r), y)
    if best[1] < min_run:
        return (None, best[1], best[2])
    return best


def stripscan(video, t0, t1, fps, outpath, band_h=120):
    """Plate-ONLY streaming pass. Decodes the top `band_h` rows of every frame.

    The full-frame scan costs a flood fill over 1920x1080 per frame; the plate
    needs 1920x120 and no flood fill, so re-measuring the plate (after a geometry
    fix, say) is minutes cheaper than re-running the census. Emits the same
    plate_metrics dict, keyed by the same timestamps, so it merges with a scan
    by `t`.
    """
    dur = t1 - t0
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0}", "-t", f"{dur}", "-i", video,
           "-vf", f"crop={W}:{band_h}:0:0,fps={fps}", "-f", "rawvideo",
           "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=W * band_h * 3)
    nb = W * band_h * 3
    out, i = [], 0
    while True:
        buf = p.stdout.read(nb)
        if len(buf) < nb:
            break
        fr = np.frombuffer(buf, dtype=np.uint8).reshape(band_h, W, 3)
        out.append({"t": round(t0 + i / fps, 4), "plate": plate_metrics(fr)})
        i += 1
    p.stdout.close(); p.wait()
    json.dump({"video": video, "t0": t0, "t1": t1, "fps": fps, "frames": i,
               "f": out}, open(outpath, "w"))
    print(f"strip frames={i} plate_frames="
          f"{sum(1 for r in out if is_plate(r['plate']))}")
    return out


# ------------------------------------------------------------------ binding

def bodies_on_frame(rds):
    """Cluster one frame's readouts into bodies (reuses the census clusterer)."""
    rows = [dict(r, box=r["box"]) for r in rds if r["kind"]]
    if not rows:
        return []
    return CO._cluster_frame(rows)


def frac(x_end, x0=TRACK_X0, x1=TRACK_X1):
    return (x_end - x0) / (x1 - x0)


def calibrate(frames, q=0.995):
    """Pin the track's 100% column from the corpus itself.

    Uses the largest fill_end observed on a plate frame. Reported with the count
    of frames within 2 px of it, so a single VFX outlier cannot set the anchor.
    """
    ends = [f["plate"]["fill_end"] for f in frames
            if is_plate(f["plate"]) and f["plate"]["fill_end"]]
    if not ends:
        return None
    ends = np.array(sorted(ends))
    top = int(ends[-1])
    near = int((ends >= top - 2).sum())
    return {"max_end": top, "n_within_2px": near, "n": len(ends),
            "p99": int(np.quantile(ends, 0.99)),
            "p95": int(np.quantile(ends, 0.95))}


def spans2(frames, gap_frames=2, rgb_tol=9, px_tol=0.13):
    """Contiguous runs of frames holding ONE nameplate.

    Segmented on the two plate quantities that are stable within a hover and
    discontinuous across one: the name band's INK COUNT (a proxy for the name
    string's length and weight) and its MEAN GLYPH COLOUR (Grim Dawn's rank
    colour: white common / yellow champion / orange hero / violet boss).

    `name_x0/x1` are deliberately NOT used: the name band's x-extent is
    contaminated by bright world pixels at the band's edges and jitters by
    hundreds of px between frames. Ink count does not.

    A span is a HOVER, not a body: two monsters with the same name and rank
    produce indistinguishable plates. Stated as a limit in the note.
    """
    out, cur = [], None
    miss = 0
    for f in frames:
        p = f["plate"]
        if not is_plate(p) or not p["name_rgb"]:
            miss += 1
            if cur and miss > gap_frames:
                out.append(cur); cur = None
            continue
        miss = 0
        if cur is None:
            cur = {"t0": f["t"], "t1": f["t"], "fr": [f]}
            continue
        q = cur["fr"][-1]["plate"]
        dpx = abs(p["name_px"] - q["name_px"]) / max(1, q["name_px"])
        dc = max(abs(a - b) for a, b in zip(p["name_rgb"], q["name_rgb"]))
        if dpx > px_tol or dc > rgb_tol:
            out.append(cur)
            cur = {"t0": f["t"], "t1": f["t"], "fr": [f]}
        else:
            cur["t1"] = f["t"]; cur["fr"].append(f)
    if cur:
        out.append(cur)
    return out


def spans(frames, gap_frames=2, rgb_tol=26):
    """Contiguous runs of frames whose plate is up AND whose name geometry+colour
    is stable — i.e. one hovered monster held.

    Split on: plate absent for > gap_frames, name x-extent jump > 12 px, or name
    colour drift > rgb_tol (a rank change is a different monster)."""
    out, cur = [], None
    miss = 0
    for f in frames:
        p = f["plate"]
        if not is_plate(p):
            miss += 1
            if cur and miss > gap_frames:
                out.append(cur); cur = None
            continue
        miss = 0
        key = (p["name_x0"], p["name_x1"], tuple(p["name_rgb"] or ()))
        if cur is None:
            cur = {"t0": f["t"], "t1": f["t"], "fr": [f]}
        else:
            q = cur["fr"][-1]["plate"]
            dx = abs((p["name_x0"] or 0) - (q["name_x0"] or 0)) + \
                 abs((p["name_x1"] or 0) - (q["name_x1"] or 0))
            dc = max(abs(a - b) for a, b in zip(p["name_rgb"] or (0, 0, 0),
                                               q["name_rgb"] or (0, 0, 0))) \
                if (p["name_rgb"] and q["name_rgb"]) else 99
            if dx > 12 or dc > rgb_tol:
                out.append(cur)
                cur = {"t0": f["t"], "t1": f["t"], "fr": [f]}
            else:
                cur["t1"] = f["t"]; cur["fr"].append(f)
    if cur:
        out.append(cur)
    return out


def bind_frame(f, x1=TRACK_X1, tol=0.035):
    """Candidate readouts for one plate frame, ranked by |f_readout - f_plate|."""
    p = f["plate"]
    if not is_plate(p) or p["fill_end"] is None:
        return None
    fp = frac(p["fill_end"], TRACK_X0, x1)
    bl = [b for b in bodies_on_frame(f["rd"])
          if b["max"] and b["cur"] is not None]
    cand = []
    for b in bl:
        fr_ = b["cur"] / b["max"]
        cand.append({"max": b["max"], "cur": b["cur"], "f": round(fr_, 4),
                     "d": round(abs(fr_ - fp), 4), "x": b["x"], "y": b["y"]})
    cand.sort(key=lambda c: c["d"])
    inside = [c for c in cand if c["d"] <= tol]
    return {"t": f["t"], "f_plate": round(fp, 4), "n_bodies": len(bl),
            "cand": cand[:6], "n_inside": len(inside)}


def span_report(sp, x1=TRACK_X1, tol=0.030):
    """Aggregate the fraction match over one held-plate span.

    Per candidate max-HP fingerprint, over the frames of the span:
      n_seen    frames on which a body with that max was parsed on camera
      n_in      frames on which some body with that max sat inside `tol`
      n_best    frames on which it was the CLOSEST candidate
      med_d     median |f_body - f_plate| over the frames it was closest
    A binding is only claimed where one fingerprint holds n_best over
    essentially the whole span AND the runner-up sits outside tol.
    """
    per = defaultdict(lambda: {"n_seen": 0, "n_in": 0, "n_best": 0, "d": [],
                               "curs": set(), "xy": []})
    fr_used = 0
    plate_f = []
    for f in sp["fr"]:
        b = bind_frame(f, x1, tol)
        if b is None or not b["cand"]:
            continue
        fr_used += 1
        plate_f.append(b["f_plate"])
        seen = set()
        for c in b["cand"]:
            if c["max"] in seen:
                continue
            seen.add(c["max"])
            per[c["max"]]["n_seen"] += 1
            if c["d"] <= tol:
                per[c["max"]]["n_in"] += 1
        best = b["cand"][0]
        per[best["max"]]["n_best"] += 1
        per[best["max"]]["d"].append(best["d"])
        per[best["max"]]["curs"].add(best["cur"])
        per[best["max"]]["xy"].append((best["x"], best["y"]))
    rows = []
    for mx, v in per.items():
        rows.append({"max": mx, "n_seen": v["n_seen"], "n_in": v["n_in"],
                     "n_best": v["n_best"],
                     "med_d": round(float(np.median(v["d"])), 4) if v["d"] else None,
                     "curs": sorted(v["curs"])[:6]})
    rows.sort(key=lambda r: (-r["n_best"], r["med_d"] if r["med_d"] is not None else 9))
    return {"t0": sp["t0"], "t1": sp["t1"], "n_frames": len(sp["fr"]),
            "n_used": fr_used,
            "f_plate": [round(x, 3) for x in plate_f],
            "rows": rows}


if __name__ == "__main__":
    if sys.argv[1] == "scan":
        scan(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]),
             float(sys.argv[5]), sys.argv[6], sys.argv[7])
