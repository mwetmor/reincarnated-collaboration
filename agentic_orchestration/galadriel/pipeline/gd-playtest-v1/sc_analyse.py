#!/usr/bin/env python3
"""SHADOW-CAL: pool the harvested figure/shadow pairs and answer (a)-(d).

(a) azimuth constancy   - circular mean + circular sd of the ground-plane cast
                          direction, overall and per area/window/screen-region
(b) shadow-length ratio - L_tip / h, corrected by the SC-C2 control bias
(c) contrast            - occlusion ratio rho = median(L_frame / L_plate) inside
                          the shadow, against the local ground illumination.
                          rho is albedo-free by construction: numerator and
                          denominator are the SAME pixels.
(d) secondary lobes     - count of distinct shadow lobes attached to one figure,
                          and lobe-2 azimuth separation
"""
import argparse
import json
import math

import numpy as np

RATIO_BIAS = -0.0420      # SC-C2, base=bottom_q top=col_q tip=q99
RATIO_SD = 0.0919
AZ_RMS = 2.63             # deg, SC-C2


def circ(deg):
    a = np.radians(np.asarray(deg, float))
    C, S = np.cos(a).mean(), np.sin(a).mean()
    R = math.hypot(C, S)
    mean = math.degrees(math.atan2(S, C))
    sd = math.degrees(math.sqrt(-2 * math.log(R))) if R > 1e-9 else float("nan")
    return mean, sd, R


def wrap(d):
    return (np.asarray(d, float) + 180) % 360 - 180


def load(paths):
    P = []
    for p in paths:
        d = json.load(open(p))
        P += d["pairs"]
    return P


def rows(pairs, min_lobe_px=250, min_fig_px=500, hmin=0.6, hmax=4.5):
    out = []
    for f in pairs:
        if f["fig_px"] < min_fig_px:
            continue
        if not (hmin <= f["h_m"] <= hmax):
            continue
        L = f["lobes"][0]
        if L["px"] < min_lobe_px:
            continue
        out.append({
            "t": f["t"], "win": f.get("window_t"),
            "x": f["base_px"][0], "y": f["base_px"][1],
            "h": f["h_m"], "fig_px": f["fig_px"],
            "az": L["az_tip"], "az_cen": L["az_cen"],
            "len": L["len_m"], "ratio": L["len_m"] / f["h_m"],
            "rho": L["rho"], "Lf": L["Lf"], "Lb": L["Lb"],
            "Lring": f.get("L_ring", float("nan")),
            "nlobe": len([z for z in f["lobes"] if z["px"] >= min_lobe_px]),
            "lobe_px": L["px"],
            "lobes": f["lobes"],
        })
    return out


def report(R):
    az = np.array([r["az"] for r in R])
    m, sd, Rl = circ(az)
    print(f"n = {len(R)} figure/shadow pairs")
    print(f"\n(a) AZIMUTH  circular mean {m:+.2f} deg   circular sd {sd:.2f} deg  "
          f"(resultant {Rl:.4f})")
    d = wrap(az - m)
    print(f"    |dev| percentiles  50% {np.percentile(np.abs(d),50):.1f}  "
          f"90% {np.percentile(np.abs(d),90):.1f}  max {np.abs(d).max():.1f} deg")
    print(f"    instrument floor (SC-C2, noiseless masks): {AZ_RMS:.2f} deg rms")
    wins = sorted(set(r["win"] for r in R))
    print(f"    per window (n>=3):")
    for w in wins:
        s = [r["az"] for r in R if r["win"] == w]
        if len(s) < 3:
            continue
        mm, ss, _ = circ(s)
        print(f"      t={w:8.1f}  n={len(s):3d}  mean {mm:+7.2f}  sd {ss:5.2f}")

    rat = np.array([r["ratio"] for r in R])
    cor = rat / (1 + RATIO_BIAS)
    print(f"\n(b) SHADOW-LENGTH RATIO  L/h")
    print(f"    raw     median {np.median(rat):.3f}   mean {rat.mean():.3f}   "
          f"sd {rat.std():.3f}   IQR {np.percentile(rat,25):.3f}-{np.percentile(rat,75):.3f}")
    print(f"    bias-corrected (SC-C2 {100*RATIO_BIAS:+.1f}%): median "
          f"{np.median(cor):.3f}  mean {cor.mean():.3f}")
    e = math.degrees(math.atan(1 / np.median(cor)))
    print(f"    implied light elevation above horizon: {e:.1f} deg")

    rho = np.array([r["rho"] for r in R])
    Lb = np.array([r["Lb"] for r in R])
    print(f"\n(c) OCCLUSION RATIO rho = L_shadow / L_same-pixels-unshadowed")
    print(f"    median {np.median(rho):.3f}  IQR {np.percentile(rho,25):.3f}-"
          f"{np.percentile(rho,75):.3f}")
    q = np.percentile(Lb, [0, 25, 50, 75, 100])
    print(f"    vs local ground brightness L_plate (quartiles):")
    for i in range(4):
        s = (Lb >= q[i]) & (Lb <= q[i + 1])
        if s.sum() < 3:
            continue
        print(f"      L_plate {q[i]:5.1f}-{q[i+1]:5.1f}  n={s.sum():3d}  "
              f"rho {np.median(rho[s]):.3f}   absolute contrast "
              f"{np.median(Lb[s]-np.array([r['Lf'] for r in R])[s]):5.1f} luma")
    if len(rho) > 6:
        cc = np.corrcoef(Lb, rho)[0, 1]
        print(f"    Pearson r(L_plate, rho) = {cc:+.3f}")

    nl = np.array([r["nlobe"] for r in R])
    print(f"\n(d) LOBES per figure: " +
          "  ".join(f"{k}:{int((nl==k).sum())}" for k in sorted(set(nl))))
    multi = [r for r in R if r["nlobe"] >= 2]
    if multi:
        sep = []
        for r in multi:
            a0 = r["lobes"][0]["az_tip"]
            a1 = r["lobes"][1]["az_tip"]
            sep.append(abs(wrap(a1 - a0)))
        sep = np.array(sep)
        print(f"    second-lobe azimuth separation: median {np.median(sep):.1f} deg, "
              f"n={len(sep)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", nargs="+", required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    P = load(a.json)
    R = rows(P)
    report(R)
    if a.out:
        json.dump([{k: v for k, v in r.items() if k != "lobes"} for r in R],
                  open(a.out, "w"))
