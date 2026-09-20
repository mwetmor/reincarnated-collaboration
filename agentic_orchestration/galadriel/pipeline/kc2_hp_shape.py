#!/usr/bin/env python3
"""
kc2_hp_shape.py — KC2-PLAY W1: HP-trace shape statistics for the T-B expected-values table.

Input:  legolas Lap Q per-frame HP trace (committed CSV), NO VIDEO REQUIRED.
Output: JSON of shape statistics, each with an explicit DENOMINATOR definition.

Every statistic here is a re-query of already-measured data (the 'cheapest refuting test'
shape). Nothing is estimated; where the data cannot decide, the row says so.

galadriel, 2026-09-20. Read-only on the input.
"""
import csv
import json
import hashlib
import math
import sys
from collections import Counter

TRACE = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/"
         "notes/2026-08-14-kc2-pm4-lap-q-heal-discriminator/pm4q_hp_trace.csv")

FPS = 60.0


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load(path):
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            rows.append({
                "frame": int(r["frame"]),
                "t": float(r["t_sec"]),
                # frame 10860 (t = 864.0) carries an EMPTY wave label in the source CSV
                # (it sits past the last wave boundary). Mapped to -1 = UNLABELLED and
                # reported, never silently dropped.
                "wave": int(r["wave"]) if r["wave"] != "" else -1,
                "hp": int(r["hp"]),
                "hp_max": int(r["health_max"]),
            })
    return rows


def pct(xs, q):
    """Linear-interpolated percentile on a sorted-able list. q in [0,100]."""
    if not xs:
        return None
    s = sorted(xs)
    if len(s) == 1:
        return float(s[0])
    k = (len(s) - 1) * q / 100.0
    lo = math.floor(k)
    hi = math.ceil(k)
    if lo == hi:
        return float(s[int(k)])
    return float(s[lo]) * (hi - k) + float(s[hi]) * (k - lo)


def describe(xs):
    if not xs:
        return {"n": 0}
    return {
        "n": len(xs),
        "min": round(min(xs), 4),
        "p05": round(pct(xs, 5), 4),
        "p25": round(pct(xs, 25), 4),
        "median": round(pct(xs, 50), 4),
        "p75": round(pct(xs, 75), 4),
        "p95": round(pct(xs, 95), 4),
        "max": round(max(xs), 4),
        "mean": round(sum(xs) / len(xs), 4),
    }


def teeth(rows, prom):
    """
    Saw-tooth decomposition, DECLARED RULE (reproducible; no fitted constant):

      Alternating-extremum walk with prominence gate `prom` (ABSOLUTE HP).
      Walk the series; maintain a running candidate extremum. Confirm a PEAK when
      hp falls `prom` below the running max since the last confirmed trough; confirm a
      TROUGH when hp rises `prom` above the running min since the last confirmed peak.
      A TOOTH is a confirmed (peak -> trough -> next peak) triple.

      depth_hp        = peak.hp - trough.hp                      (ABSOLUTE)
      depth_frac      = depth_hp / peak.hp_max                   (denominator = hp_max AT THE PEAK)
      period_s        = next_peak.t - peak.t                     (peak-to-peak)
      fall_s          = trough.t - peak.t
      recover_s       = next_peak.t - trough.t
      fall_slope      = -depth_hp / fall_s      HP/s (negative)
      recovery_slope  = (next_peak.hp - trough.hp) / recover_s  HP/s (positive)

    The prominence gate is SWEPT, never chosen: the recorder reproduces the sweep.
    """
    if not rows:
        return []
    ext = []          # confirmed extrema: (kind, idx)
    mode = None       # 'up' (seeking a peak) / 'down' (seeking a trough)
    cand = 0
    for i in range(1, len(rows)):
        hp = rows[i]["hp"]
        if mode is None:
            if hp >= rows[cand]["hp"] + prom:
                mode = "up"
                ext.append(("trough", cand))
                cand = i
            elif hp <= rows[cand]["hp"] - prom:
                mode = "down"
                ext.append(("peak", cand))
                cand = i
            elif mode is None and (hp > rows[cand]["hp"] or hp < rows[cand]["hp"]):
                # keep the most extreme in BOTH directions until one gate trips
                pass
            continue
        if mode == "up":
            if hp >= rows[cand]["hp"]:
                cand = i
            elif hp <= rows[cand]["hp"] - prom:
                ext.append(("peak", cand))
                mode = "down"
                cand = i
        else:
            if hp <= rows[cand]["hp"]:
                cand = i
            elif hp >= rows[cand]["hp"] + prom:
                ext.append(("trough", cand))
                mode = "up"
                cand = i

    out = []
    for a in range(len(ext) - 2):
        k0, i0 = ext[a]
        k1, i1 = ext[a + 1]
        k2, i2 = ext[a + 2]
        if not (k0 == "peak" and k1 == "trough" and k2 == "peak"):
            continue
        p0, tr, p1 = rows[i0], rows[i1], rows[i2]
        depth = p0["hp"] - tr["hp"]
        fall_s = tr["t"] - p0["t"]
        rec_s = p1["t"] - tr["t"]
        out.append({
            "t_peak": round(p0["t"], 4),
            "t_trough": round(tr["t"], 4),
            "wave": tr["wave"],
            "peak_hp": p0["hp"],
            "trough_hp": tr["hp"],
            "hp_max_at_peak": p0["hp_max"],
            "depth_hp": depth,
            "depth_frac_of_hp_max": round(depth / p0["hp_max"], 6),
            "period_s": round(p1["t"] - p0["t"], 4),
            "fall_s": round(fall_s, 4),
            "recover_s": round(rec_s, 4),
            "fall_slope_hp_per_s": round(-depth / fall_s, 2) if fall_s > 0 else None,
            "recovery_slope_hp_per_s": round((p1["hp"] - tr["hp"]) / rec_s, 2) if rec_s > 0 else None,
        })
    return out


def main():
    rows = load(TRACE)
    n = len(rows)
    digest = sha256(TRACE)

    # --- frame-grid integrity -------------------------------------------------
    dts = [round(rows[i + 1]["t"] - rows[i]["t"], 6) for i in range(n - 1)]
    dt_counts = Counter(dts)
    frames_contiguous = all(rows[i + 1]["frame"] - rows[i]["frame"] == 1 for i in range(n - 1))

    hp_max_vals = sorted(set(r["hp_max"] for r in rows))
    nominal_max = max(hp_max_vals)

    # --- occupancy: TWO denominators, both shipped ---------------------------
    # D1 "LIVE-MAX":  threshold applied against hp_max AT THAT FRAME
    # D2 "NOMINAL":   threshold applied against the nominal 20,005 throughout
    occ = {}
    for label, thr in [("full", 1.0), ("ge_90", 0.90), ("ge_75", 0.75),
                       ("lt_90", 0.90), ("lt_75", 0.75), ("lt_50", 0.50),
                       ("lt_33", 1.0 / 3.0), ("lt_25", 0.25)]:
        pass  # explicit below for clarity

    def frac(pred):
        c = sum(1 for r in rows if pred(r))
        return {"frames": c, "fraction": round(c / n, 6)}

    occ_live = {
        "at_full": frac(lambda r: r["hp"] >= r["hp_max"]),
        "below_full": frac(lambda r: r["hp"] < r["hp_max"]),
        "below_90pct": frac(lambda r: r["hp"] < 0.90 * r["hp_max"]),
        "below_75pct": frac(lambda r: r["hp"] < 0.75 * r["hp_max"]),
        "below_50pct": frac(lambda r: r["hp"] < 0.50 * r["hp_max"]),
        "below_33pct": frac(lambda r: r["hp"] < r["hp_max"] / 3.0),
        "below_25pct": frac(lambda r: r["hp"] < 0.25 * r["hp_max"]),
    }
    occ_nom = {
        "at_full": frac(lambda r: r["hp"] >= nominal_max),
        "below_full": frac(lambda r: r["hp"] < nominal_max),
        "below_90pct": frac(lambda r: r["hp"] < 0.90 * nominal_max),
        "below_75pct": frac(lambda r: r["hp"] < 0.75 * nominal_max),
        "below_50pct": frac(lambda r: r["hp"] < 0.50 * nominal_max),
        "below_33pct": frac(lambda r: r["hp"] < nominal_max / 3.0),
        "below_25pct": frac(lambda r: r["hp"] < 0.25 * nominal_max),
    }

    # --- frames showing a decrease -------------------------------------------
    dec = sum(1 for i in range(1, n) if rows[i]["hp"] < rows[i - 1]["hp"])
    inc = sum(1 for i in range(1, n) if rows[i]["hp"] > rows[i - 1]["hp"])
    flat = (n - 1) - dec - inc

    # --- deepest excursions ---------------------------------------------------
    by_hp = sorted(rows, key=lambda r: r["hp"])
    # group the deepest into distinct EXCURSIONS: a maximal run below 50% of live max
    excursions = []
    cur = None
    for r in rows:
        below = r["hp"] < 0.50 * r["hp_max"]
        if below and cur is None:
            cur = {"t_start": r["t"], "min_hp": r["hp"], "t_min": r["t"],
                   "wave": r["wave"], "hp_max": r["hp_max"]}
        elif below:
            if r["hp"] < cur["min_hp"]:
                cur["min_hp"] = r["hp"]
                cur["t_min"] = r["t"]
                cur["wave"] = r["wave"]
        elif cur is not None:
            cur["t_end"] = r["t"]
            cur["dur_s"] = round(cur["t_end"] - cur["t_start"], 4)
            cur["min_frac_of_hp_max"] = round(cur["min_hp"] / cur["hp_max"], 6)
            excursions.append(cur)
            cur = None
    if cur is not None:
        cur["t_end"] = rows[-1]["t"]
        cur["dur_s"] = round(cur["t_end"] - cur["t_start"], 4)
        cur["min_frac_of_hp_max"] = round(cur["min_hp"] / cur["hp_max"], 6)
        excursions.append(cur)
    for e in excursions:
        e["t_start"] = round(e["t_start"], 4)
        e["t_end"] = round(e["t_end"], 4)
        e["t_min"] = round(e["t_min"], 4)
    excursions.sort(key=lambda e: e["min_hp"])

    # --- health_max episode ---------------------------------------------------
    hm_eps = []
    cur = None
    for r in rows:
        if r["hp_max"] != nominal_max:
            if cur is None or cur["hp_max"] != r["hp_max"]:
                if cur is not None:
                    cur["t_end"] = r["t"]
                    hm_eps.append(cur)
                cur = {"hp_max": r["hp_max"], "t_start": r["t"], "wave_start": r["wave"]}
            cur["wave_end"] = r["wave"]
        elif cur is not None:
            cur["t_end"] = r["t"]
            hm_eps.append(cur)
            cur = None
    if cur is not None:
        cur["t_end"] = rows[-1]["t"]
        hm_eps.append(cur)
    for e in hm_eps:
        e["dur_s"] = round(e["t_end"] - e["t_start"], 4)
        e["delta_hp"] = e["hp_max"] - nominal_max
        e["delta_pct"] = round(100.0 * (e["hp_max"] - nominal_max) / nominal_max, 4)
        e["t_start"] = round(e["t_start"], 4)
        e["t_end"] = round(e["t_end"], 4)

    # --- saw-tooth sweep ------------------------------------------------------
    sweep = {}
    for prom in (100, 250, 500, 1000, 2000):
        ts = teeth(rows, prom)
        sweep[str(prom)] = {
            "n_teeth": len(ts),
            "rate_per_s": round(len(ts) / (n / FPS), 5),
            "period_s": describe([t["period_s"] for t in ts]),
            "depth_hp": describe([t["depth_hp"] for t in ts]),
            "depth_frac_of_hp_max": describe([t["depth_frac_of_hp_max"] for t in ts]),
            "fall_s": describe([t["fall_s"] for t in ts]),
            "recover_s": describe([t["recover_s"] for t in ts]),
            "fall_slope_hp_per_s": describe([t["fall_slope_hp_per_s"] for t in ts if t["fall_slope_hp_per_s"] is not None]),
            "recovery_slope_hp_per_s": describe([t["recovery_slope_hp_per_s"] for t in ts if t["recovery_slope_hp_per_s"] is not None]),
            "deepest_5": sorted(ts, key=lambda t: -t["depth_hp"])[:5],
        }

    # --- per-wave -------------------------------------------------------------
    per_wave = {}
    waves = sorted(set(r["wave"] for r in rows))
    for w in waves:
        wr = [r for r in rows if r["wave"] == w]
        m = len(wr)
        wt = teeth(wr, 500)
        per_wave[str(w)] = {
            "frames": m,
            "dur_s_from_trace": round(m / FPS, 4),
            "t_first": round(wr[0]["t"], 4),
            "t_last": round(wr[-1]["t"], 4),
            "hp_min": min(r["hp"] for r in wr),
            "hp_max_observed": max(r["hp"] for r in wr),
            "frac_at_full_live": round(sum(1 for r in wr if r["hp"] >= r["hp_max"]) / m, 6),
            "frac_below_50_live": round(sum(1 for r in wr if r["hp"] < 0.5 * r["hp_max"]) / m, 6),
            "frac_decrease": (round(sum(1 for i in range(1, m) if wr[i]["hp"] < wr[i - 1]["hp"]) / (m - 1), 6)
                              if m > 1 else None),
            "n_teeth_prom500": len(wt),
            "median_depth_hp_prom500": describe([t["depth_hp"] for t in wt]).get("median"),
            "median_period_s_prom500": describe([t["period_s"] for t in wt]).get("median"),
        }

    out = {
        "instrument": "galadriel/pipeline/kc2_hp_shape.py",
        "generated": "2026-09-20",
        "source": {
            "path": ("agentic_orchestration/legolas/notes/"
                     "2026-08-14-kc2-pm4-lap-q-heal-discriminator/pm4q_hp_trace.csv"),
            "sha256": digest,
            "lap": "KC2-PM4 Lap Q (legolas), prereg da62709f2887df1e2874f7cc1baa0ef2cd901ea47ce555678b9d4d98c07dfa77",
            "ocr_acceptance": "PC-3 100.00% accepted against the decoded denominator",
        },
        "grid": {
            "rows": n,
            "fps": FPS,
            "t_first": rows[0]["t"],
            "t_last": rows[-1]["t"],
            "span_s": round(rows[-1]["t"] - rows[0]["t"], 4),
            "frames_contiguous": frames_contiguous,
            "dt_distinct": {str(k): v for k, v in sorted(dt_counts.items())},
            "waves": waves,
        },
        "hp_max": {
            "values_observed": hp_max_vals,
            "nominal": nominal_max,
            "episodes_off_nominal": hm_eps,
        },
        "occupancy_denominator_LIVE_MAX": occ_live,
        "occupancy_denominator_NOMINAL_20005": occ_nom,
        "frame_deltas": {
            "n_intervals": n - 1,
            "decrease": dec, "frac_decrease": round(dec / (n - 1), 6),
            "increase": inc, "frac_increase": round(inc / (n - 1), 6),
            "flat": flat, "frac_flat": round(flat / (n - 1), 6),
        },
        "hp_extremes": {
            "hp_min": by_hp[0]["hp"],
            "t_at_hp_min": round(by_hp[0]["t"], 4),
            "wave_at_hp_min": by_hp[0]["wave"],
            "hp_max_observed": by_hp[-1]["hp"],
        },
        "excursions_below_50pct_live": excursions,
        "sawtooth_prominence_sweep_hp": sweep,
        "per_wave": per_wave,
    }
    json.dump(out, sys.stdout, indent=1)
    print()


if __name__ == "__main__":
    main()
