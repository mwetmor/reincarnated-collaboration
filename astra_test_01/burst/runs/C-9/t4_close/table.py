#!/usr/bin/env python3
"""C-9 T4 close-out: render drift.json as the markdown tables in REPORT.md.

    python3 table.py            # prints; paste into REPORT.md

Generated rather than transcribed, so the report cannot disagree with the JSON.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = ["kling", "hydra", "forge", "anim", "drive", "render3d", "astra"]
NICE = {"kling": "**Kling v3 Pro** motion-control",
        "hydra": "**Ludo** transfer-motion, hydra",
        "forge": "**Ludo** transfer-motion, forge",
        "anim": "**Ludo** animate-sprite, text 'walking'",
        "drive": "_floor_ · the Meshy drive render",
        "render3d": "_floor_ · raw 3D render, 12-frame cell",
        "astra": "_benchmark_ · Astra per-frame paint"}
COST = {"kling": ("$0.84", "180 s"), "hydra": ("15 cr", "347 s"),
        "forge": ("10 cr", "293 s"), "anim": ("9 cr", "501 s"),
        "drive": ("3 cr*", "6 s"), "render3d": ("--", "--"),
        "astra": ("Astra seat", "~1 h/cell")}


def g(d, *ks, default="--"):
    for k in ks:
        if not isinstance(d, dict) or k not in d:
            return default
        d = d[k]
    return d


def f(v, n=2):
    return "--" if v in (None, "--") else ("%.*f" % (n, v))


def main():
    rep = json.load(open(os.path.join(HERE, "drift.json")))
    R = rep["routes"]
    names = [n for n in ORDER if n in R]

    print("### Table 1 — identity: does the helm hold?\n")
    print("| route | frames · fps | helm px | helm drift, **phase-matched** (lag=1/12 stride) med / p90 / max | helm drift raw f2f med | shuffled control | helm vs the still (min / med) | whole figure vs the still (min / med) |")
    print("|---|---|---|---|---|---|---|---|")
    for n in names:
        r = R[n]
        pm = r["helm_drift_phase_matched"]
        raw = r["helm_drift_frame_to_frame"]
        hr = r["helm_drift_vs_reference_still"]
        br = r["body_drift_vs_reference_still"]
        cmp_ok = hr.get("comparable", True)
        print("| %s | %d · %.1f | %d | **%s** / %s / %s | %s | %s | %s | %s |" % (
            NICE[n], r["frames"], r["fps"], g(r, "native", "helm_h_px_median"),
            f(pm["median"]), f(pm["p90"]), f(pm["max"]), f(raw["median"]),
            f(g(raw, "shuffled", "median")),
            ("%s / %s" % (f(hr["min"]), f(hr["median"]))) if cmp_ok else "n/a",
            ("%s / %s" % (f(br["min"]), f(br["median"]))) if cmp_ok else "n/a"))

    print("\n### Table 2 — walk quality, loop, cost\n")
    print("| route | cadence (strides/s) | vs drive | foot slip RMS (% fig. h) med / p90 | planted travel (% fig. h) | pollaxe: haft len CV · straightness · dAngle p90 | loop seam (body, 1.0 = clean) | cost | wall time |")
    print("|---|---|---|---|---|---|---|---|---|")
    dsp = g(R, "drive", "cadence", "strides_per_s", default=None)
    for n in names:
        r = R[n]
        c = r["cadence"]
        fs = r["foot_slide"]
        po = r["pollaxe"]
        ls = r["loop_seam"]
        sps = c["strides_per_s"]
        ratio = ("%.2fx" % (sps / dsp)) if dsp else "--"
        if not c["repeat_found"]:
            sps_s = "%.2f †" % sps
        else:
            sps_s = "%.2f" % sps
        if fs.get("measurable"):
            foot = "%s / %s" % (f(fs["slip_rms_pct_H_median"]),
                                f(fs["slip_rms_pct_H_p90"]))
            trav = f(fs["planted_travel_pct_H_median"], 1)
        else:
            foot, trav = "n/m ‡", "n/m ‡"
        if "note" in po and "NO rigid weapon" in po.get("note", ""):
            pol = "no weapon"
        else:
            pol = "%.1f%% · %.2f%% · %.2f°" % (po["len_cv_pct"],
                                               po["straightness_pct_median"],
                                               po["d_angle_deg_p90"])
        cost, wall = COST.get(n, ("--", "--"))
        print("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            NICE[n], sps_s, ratio, foot, trav, pol,
            f(ls["body_seam_ratio"]), cost, wall))

    print("\n† no repeat found in the clip; the clip is one stride and the "
          "period is its length.")
    print("‡ not measurable: fewer than 16 frames per stride, see drift.json.")
    print("\\* the drive is our own Meshy text-to-motion carry walk (10 cr to "
          "generate + 3 cr to apply), not a per-clip cost of this test.")

    fb = os.path.join(HERE, "fallback_check.json")
    if os.path.exists(fb):
        d = json.load(open(fb))
        print("\n### Table 3 — is the 2D fallback the same instrument? "
              "(both run on the knight's 12-frame Astra walk E)\n")
        print("| sequence | pos-matched body | pos-matched **head** | 2D body | 2D **head** |")
        print("|---|---|---|---|---|")
        for k, v in d["rows"].items():
            print("| %s | %s | %s | %s | %s |" % (
                k, f(g(v, "pos_matched", "body", "median")),
                f(g(v, "pos_matched", "head", "median")),
                f(g(v, "two_d", "body", "median")),
                f(g(v, "two_d", "head", "median"))))

    sn = os.path.join(HERE, "sensitivity.json")
    if os.path.exists(sn):
        d = json.load(open(sn))
        print("\n### Table 4 — what a drift number means "
              "(a known break, injected into the drive's helm)\n")
        print("| injected per-frame change | helm drift med | p90 |")
        print("|---|---|---|")
        for k, v in d["rows"].items():
            print("| %s | %s | %s |" % (k, f(v["median"]), f(v["p90"])))


if __name__ == "__main__":
    main()
