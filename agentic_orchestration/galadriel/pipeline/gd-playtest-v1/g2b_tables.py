#!/usr/bin/env python3
"""G-2b -- flatten the decomposition JSONs into the derived tables the note
cites. No new measurement happens here; this is presentation only.

Usage: g2b_tables.py <capturedir>
"""
import csv
import json
import os
import sys

d = sys.argv[1]
dec = json.load(open(os.path.join(d, "g2b-decomposition.json")))
ms = json.load(open(os.path.join(d, "g2b-mergeshare.json")))

# --- gap PMF -----------------------------------------------------------------
with open(os.path.join(d, "g2b-gap-pmf.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["subset", "regime", "gap_s", "count", "pmf",
                "exp_null_expected_std_resid"])
    for subset in ("all", "long_engagements_ge_10s",
                   "short_engagements_lt_10s"):
        for r in ("R1", "R2", "R3"):
            b = dec["d1_gap_structure"][subset][r]
            if b["n"] == 0:
                continue
            for g in b["counts"]:
                w.writerow([subset, r, g, b["counts"][g], b["pmf"][g],
                            b["exp_null_std_resid"][g]])

# --- sensitivity re-segmentation --------------------------------------------
with open(os.path.join(d, "g2b-sensitivity.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["gap_threshold_s", "n_engagements_total", "regime",
                "n_engagements", "kills", "kills_per_engagement",
                "ci95_lo", "ci95_hi", "ratio_vs_R1"])
    for k, v in dec["d1b_sensitivity_resegmentation"].items():
        g = k.replace("gap_gt_", "")
        for r in ("R1", "R2", "R3"):
            b = v[r]
            w.writerow([g, v["n_engagements_total"], r, b["n_engagements"],
                        b["kills"], b["kills_per_engagement"],
                        b["ci95"][0], b["ci95"][1],
                        v[f"ratio_{r}_over_R1"] if r != "R1" else 1.0])

# --- ABC factors -------------------------------------------------------------
with open(os.path.join(d, "g2b-abc-factors.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["burst_threshold_s", "regime", "n_engagements",
                "A_kills_per_event", "A_lo", "A_hi",
                "B_events_per_burst", "B_lo", "B_hi",
                "C_bursts_per_engagement", "C_lo", "C_hi",
                "kills_per_engagement"])
    for bk, blk in dec["abc_decomposition"].items():
        b = bk.replace("burst_b", "")
        for r in ("R1", "R2", "R3"):
            x = blk[r]
            w.writerow([b, r, x["n"]] + x["A_kills_per_event"] +
                       x["B_events_per_burst"] + x["C_bursts_per_engagement"] +
                       [x["kills_per_engagement"][0]])

# --- merge share -------------------------------------------------------------
with open(os.path.join(d, "g2b-mergeshare.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["contrast", "gap_threshold_s", "ratio", "ratio_lo",
                "ratio_hi", "merge_share", "merge_share_lo", "merge_share_hi"])
    for c in ("R1_to_R2", "R2_to_R3", "R1_to_R3"):
        for g in ms["grid_s"]:
            x = ms[c][f"gap_gt_{g}"]
            w.writerow([c, g, x["ratio"], x["ratio_ci95"][0],
                        x["ratio_ci95"][1], x["merge_share"],
                        x["merge_share_ci95"][0], x["merge_share_ci95"][1]])

print("wrote 4 derived tables to", d)
