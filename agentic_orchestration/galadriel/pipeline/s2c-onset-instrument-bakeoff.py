#!/usr/bin/env python3
# ============================================================================
# galadriel — § 1.2 test (3) REPLACEMENT INSTRUMENT BAKE-OFF
#
# Occasioned by drax's HALT on tranche 3A pair 1 (dash_attack vs blink):
# the § 1.2 test-(3) shape metric runs on a COVERAGE fraction
# |lit ∩ body-disc| / |body-disc| that is bounded above by 1 and REACHES its
# ceiling on `blink`. A clipped ramp forces its rise into the pre-saturation
# frames and reads as a STEP.
#
# This script does NOT re-capture. It re-reads the frames already on disk in
# ~/Games/reincarnated-godot/harness_logs/s2c_rows12_2026-08-25/ (fx-on and
# matched _novfx control, per frame, per stage, per row) and computes SEVERAL
# CANDIDATE onset metrics on the SAME regions the sealed instrument used, so
# they can be compared against a stated acceptance test.
#
# ACCEPTANCE TEST (knight-rider's proposal, evaluated not assumed):
#   CROSS-STAGE INVARIANCE — a shape metric on a fixed row with a fixed
#   authored effect must return approximately the same value on `arena` and
#   `cathedral`.
#
# READ-ONLY against reincarnated-godot. Writes only under galadriel/.
# ============================================================================
import json, os, re, sys
from collections import defaultdict

import numpy as np
from PIL import Image

CAP = "/Users/admin/Games/reincarnated-godot/harness_logs/s2c_rows12_2026-08-25"
FRAME_W, FRAME_H = 1920, 1080
BYVALUE_DELTA = 4  # the sealed instrument's screen; reproduced exactly

# Rec.709 luma. Named once. "Luminance" is not "mean of channels" and the
# difference is not decorative — green carries 71% of perceived brightness,
# and these effects are not grey.
LUMA = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)

PAIRS = [
    # (row, stage, fx-on prefix, fx-off prefix)
    ("dash_attack", "arena",     "clip_da_arena",     "clip_da_arena_novfx"),
    ("dash_attack", "cathedral", "clip_da_cathedral", "clip_da_cathedral_novfx"),
    ("blink",       "arena",     "clip_bl_arena",     "clip_bl_arena_novfx"),
    ("blink",       "cathedral", "clip_bl_cathedral", "clip_bl_cathedral_novfx"),
]


def parse_log(path):
    """Per-arm SERIES emissions, keyed by --prefix banner. Same rule as the
    sealed gate: log POSITION ties an emission to its arm."""
    arms, cur = {}, None
    for line in open(path, errors="replace"):
        m = re.match(r"^=== (.*) ===\s*$", line)
        if m:
            pm = re.search(r"--prefix=(\S+)", m.group(1))
            cur = pm.group(1) if pm else None
            if cur:
                arms.setdefault(cur, [])
            continue
        if cur is None:
            continue
        if line.startswith("[s2a] SERIES "):
            arms[cur].append(json.loads(line[len("[s2a] SERIES "):]))
    return arms


def body_disc(b):
    """IDENTICAL to the sealed gate's body_disc(). The gate never re-derives
    the camera; neither does the replacement. Changing the REGION at the same
    time as the METRIC would make the comparison below uninterpretable."""
    fx, fy = b["foot"]
    hx, hy = b["head"]
    return (fx + hx) / 2.0, (fy + hy) / 2.0, 0.5 * b["h_px"]


def disc_mask_bbox(cx, cy, r):
    """Disc as (mask, y0, y1, x0, x1) over a bounding box, for speed."""
    x0 = max(0, int(np.floor(cx - r)));  x1 = min(FRAME_W, int(np.ceil(cx + r)) + 1)
    y0 = max(0, int(np.floor(cy - r)));  y1 = min(FRAME_H, int(np.ceil(cy + r)) + 1)
    if x1 <= x0 or y1 <= y0:
        return None, 0, 0, 0, 0
    ys, xs = np.ogrid[y0:y1, x0:x1]
    m = (xs - cx) ** 2 + (ys - cy) ** 2 <= r * r
    return m, y0, y1, x0, x1


def measure(on_prefix, off_prefix, series):
    """Per body, per frame: BOTH the sealed coverage fraction AND the
    candidate intensity quantities, from the same pixels in the same call.
    Computing them together is the point — it removes 'different run' as an
    explanation for any divergence."""
    out = defaultdict(list)
    i = 0
    while True:
        pon = os.path.join(CAP, "%s_f%04d.png" % (on_prefix, i))
        poff = os.path.join(CAP, "%s_f%04d.png" % (off_prefix, i))
        if not (os.path.exists(pon) and os.path.exists(poff)):
            break
        on = np.asarray(Image.open(pon).convert("RGB"), dtype=np.float32)
        off = np.asarray(Image.open(poff).convert("RGB"), dtype=np.float32)
        for b in series[i]["bodies"]:
            cx, cy, r = body_disc(b)
            m, y0, y1, x0, x1 = disc_mask_bbox(cx, cy, r)
            n = 0 if m is None else int(m.sum())
            if n == 0:
                out[b["name"]].append({"i": i, "t": series[i]["t"], "region_px": 0,
                                       "cov": None, "addlum": None, "abslum": None})
                continue
            sub_on = on[y0:y1, x0:x1]
            sub_off = off[y0:y1, x0:x1]
            d = sub_on - sub_off
            # sealed screen: any channel delta >= 4, as a COVERAGE fraction
            cov = float((np.abs(d).max(axis=2) >= BYVALUE_DELTA)[m].sum()) / n
            # candidate: MEAN ADDED LUMA over the region (rectified positive)
            dl = (d * LUMA).sum(axis=2)
            addlum = float(np.clip(dl, 0, None)[m].sum()) / n
            abslum = float(np.abs(dl)[m].sum()) / n
            out[b["name"]].append({"i": i, "t": series[i]["t"], "region_px": n,
                                   "cov": cov, "addlum": addlum, "abslum": abslum,
                                   "peak_px_lum": float(np.clip(dl, 0, None)[m].max())})
        i += 1
    return dict(out)


# ---------------------------------------------------------------------------
# CANDIDATE SHAPE METRICS. Each takes (values, times) and returns a scalar or
# None. None means UNEVALUABLE and is a legitimate output.
# ---------------------------------------------------------------------------
def step_concentration(v, t=None):
    """The SEALED metric: max positive frame-to-frame rise / sum of positive
    rises. Reproduced here so the bake-off contains its own baseline."""
    v = np.asarray(v, dtype=float)
    if len(v) < 3:
        return None
    d = np.diff(v)
    pos = d[d > 0]
    if pos.sum() <= 0:
        return None
    return float(pos.max() / pos.sum())


def rise_time_1090(v, t):
    """CANDIDATE C — ONSET DURATION IN SECONDS.

    Time from the last frame below 10% of peak to the first frame at/above 90%
    of peak, on the approach to the peak. This asks the question the law
    actually asks ('does it turn on all at once, or over time') on the TIME
    axis rather than the value axis, so a compressive distortion of the value
    axis cannot move it as long as the 10% and 90% crossings are still ordered
    correctly. Units: seconds. SMALL = STEP, LARGE = RAMP.
    """
    v = np.asarray(v, dtype=float)
    t = np.asarray(t, dtype=float)
    if len(v) < 3:
        return None
    pk = float(v.max())
    if pk <= 0:
        return None
    k = int(np.argmax(v))
    lo, hi = 0.10 * pk, 0.90 * pk
    i_hi = next((j for j in range(k + 1) if v[j] >= hi), None)
    if i_hi is None:
        return None
    i_lo = None
    for j in range(i_hi, -1, -1):
        if v[j] <= lo:
            i_lo = j
            break
    if i_lo is None:
        return None
    return float(t[i_hi] - t[i_lo])


def measure_report(vals, times, floor=None):
    v = [x for x in vals if x is not None]
    t = [tt for x, tt in zip(vals, times) if x is not None]
    if len(v) < 3:
        return {"status": "UNEVALUABLE-TOO-FEW-FRAMES"}
    peak = float(max(v))
    r = {"peak": peak,
         "step_conc": step_concentration(v),
         "rise_1090_s": rise_time_1090(v, t)}
    if floor is not None and peak < floor:
        r["status"] = "UNEVALUABLE-BELOW-FLOOR"
    return r


def main():
    arms = parse_log(os.path.join(CAP, "render.txt"))
    results = {}
    for row, stage, pon, poff in PAIRS:
        sys.stderr.write("measuring %s @ %s ...\n" % (row, stage))
        series = arms[pon]
        per_body = measure(pon, poff, series)
        results[(row, stage)] = per_body
    out = {}
    for (row, stage), per_body in results.items():
        out.setdefault(row, {})[stage] = {}
        for name, pts in per_body.items():
            times = [p["t"] for p in pts]
            out[row][stage][name] = {
                "n": len(pts),
                "COVERAGE_sealed": measure_report([p["cov"] for p in pts], times),
                "ADDLUM_candidate": measure_report([p["addlum"] for p in pts], times),
                "cov_frames_ge_099": sum(1 for p in pts if p["cov"] is not None and p["cov"] >= 0.99),
                "peak_px_lum": max([p.get("peak_px_lum", 0.0) or 0.0 for p in pts]),
                "series": [{"i": p["i"], "t": p["t"], "cov": p["cov"],
                            "addlum": p["addlum"], "abslum": p["abslum"]} for p in pts],
            }
    dst = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "s2c-onset-instrument-bakeoff.json")
    json.dump(out, open(dst, "w"), indent=1)
    print("wrote", dst)


if __name__ == "__main__":
    main()
