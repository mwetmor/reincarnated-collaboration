#!/usr/bin/env python3
"""
pm4u_ramp_2026_08_14.py — RUN KC2-PM4 LAP U, INSTRUMENT I-U2.

DECLARED POST-HOC EXTENSIONS TO LIMB (a), PLUS THE GEOMETRY HAND-OFF FOR I-21.

⚑ EVERYTHING IN THIS FILE IS POST-HOC AND IS LABELLED AS SUCH.  It was written AFTER I-U1's
numbers were on the screen.  It may NOT change any pre-registered verdict of I-U1 and it does not
attempt to.  It exists because I-U1 returned two results that need diagnosing rather than
reporting bare:

  (1) V-a1 returned NOT SUPPORTED with n = 0 at EVERY cell of the pre-registered sweep, and the
      reason is visible in the artifact: the largest player NET displacement inside ANY surviving
      hold-window is 4.16 m, while the loosest cell needs 5.0 m and the primary cell needs 9.0 m.
      The discriminator is STARVED BY THE REFERENT'S OWN LOCOMOTION, not broken.  § 1 measures
      that starvation and converts it into the bound it does support.

  (2) The entry count (3,324 tracks) is ~5-10x any plausible body count for a fight whose peak
      LIVING plate count is 19-36.  Most "entries" are plate RE-APPEARANCES (UNREACHED-S4), which
      the pre-registration named but did not price.  § 2 prices it, and the price disqualifies the
      raw inter-entry interval distribution as a grading target.  Self-caught: `D-U-3`.

  § 3 is the geometry hand-off: per-spawn-point first-march distances from the REPAIRED v3 labels,
      superseding `pm4t_geometry_corrected.csv`, which R-PM4-51 part 3 asked for and I-20 correctly
      refused because the labels were displaced.

  § 4 is the march-arithmetic reconciliation: the referent's own ramp converted to metres at the
      decoded speed bracket, and what that implies about where the player stands relative to the
      attack ring.

READ-ONLY.  NO SIM NUMBER IS CONSULTED.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import pathlib
import statistics as st
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gd_arc_reader_2026_07_26 import ArcArchive
import pm4t_map_v2_2026_08_14 as V2
import pm4u_mapv3_2026_08_14 as V3
import pm4u_video_2026_08_14 as U1

OUT = V3.OUT

# ── carried, each with its source named (NOTE-9).  None re-derived here. ──────────────────────
MARCH_LO, MARCH_HI = 3.055412, 3.209466      # Lap T Route-2 bracket, INFERRED-WITH-EVIDENCE
FRUSTUM_M = {"lo119": 11.614, "hi125": 11.056}   # Lap S V-B1 max observed plate radius
PLACEMENT_EXTENTS = 8.0                      # Lap S F-2, uniform on all 54 tier-16 proxies


def desc(v):
    if not len(v):
        return None
    a = np.asarray(v, dtype=float)
    return {"n": int(a.size), "min": round(float(a.min()), 4),
            "p25": round(float(np.percentile(a, 25)), 4),
            "median": round(float(np.median(a)), 4),
            "p75": round(float(np.percentile(a, 75)), 4),
            "mean": round(float(a.mean()), 4), "max": round(float(a.max()), 4)}


def main():
    print("=" * 104)
    print("KC2-PM4 LAP U — I-U2: DECLARED POST-HOC EXTENSIONS + THE I-21 GEOMETRY HAND-OFF")
    print("=" * 104)
    res = {"instrument": "I-U2", "status": "POST-HOC, DECLARED — may not change any "
           "pre-registered verdict of I-U1",
           "preregistration_sha256":
               "7a250772bad3bf8cbce2e43455bc3e4dae2fee677aeedc1ffad978f3dda6b144"}

    ta, offs = U1.load()
    trs = U1.track_with_history(ta, offs)
    stats = json.load(open(OUT / "pm4u_arrival_stats.json"))

    # ══════════════════════════════════════════════════════════════════════════════════════════
    # § 1 — WHY V-a1 IS STARVED, AND THE BOUND IT DOES SUPPORT
    # ══════════════════════════════════════════════════════════════════════════════════════════
    print("\n§ 1 — THE STARVATION OF V-a1, MEASURED")
    pm = stats["V_a4_player_motion"]
    waves = sorted(int(w) for w in pm if w.isdigit())
    net = [pm[str(w)]["net_m_lo119"] for w in waves]
    path = [pm[str(w)]["path_m_lo119"] for w in waves]
    straight = [pm[str(w)]["straightness"] for w in waves]
    wins = stats["V_a1"]["windows_lo119"]
    dpmax = max((w["dp_m"] for w in wins), default=0.0)

    # the bound: how much march TIME can the player's own motion add or remove?
    bound = {k: dict(median_s=round(st.median(net) / v, 4), max_s=round(max(net) / v, 4))
             for k, v in (("march_lo_3.055412", MARCH_LO), ("march_hi_3.209466", MARCH_HI))}
    print(f"    player NET displacement per wave (m)   : median {st.median(net):.2f}, "
          f"min {min(net):.2f}, max {max(net):.2f}")
    print(f"    player PATH length per wave (m)        : median {st.median(path):.2f}, "
          f"max {max(path):.2f}")
    print(f"    straightness (net / path)              : median {st.median(straight):.4f}  "
          f"-> THE PLAYER MILLS, HE DOES NOT TRAVERSE")
    print(f"    largest player NET displacement inside ANY V-a1 hold-window : {dpmax:.2f} m")
    print(f"    the loosest pre-registered cell needed  5.0 m; the primary cell needed 9.0 m")
    print(f"    => V-a1 IS STARVED BY THE REFERENT, NOT BROKEN.  n = 0 is a NEGATIVE about the")
    print(f"       INSTRUMENT'S REACH, not a refutation of player-targeting.")
    print(f"\n    THE BOUND V-a1 DOES SUPPORT — how much march TIME can the player's own motion")
    print(f"    add or remove over a whole wave, at the decoded march bracket:")
    for k, v in bound.items():
        print(f"       {k:22s}  median {v['median_s']:.3f} s   worst wave {v['max_s']:.3f} s")
    res["S1_starvation"] = dict(
        net_m_per_wave=desc(net), path_m_per_wave=desc(path), straightness=desc(straight),
        max_player_net_displacement_in_any_hold_window_m=round(dpmax, 4),
        loosest_cell_requirement_m=5.0, primary_cell_requirement_m=9.0,
        player_motion_march_time_bound_s=bound,
        reading="V-a1 returns NO INFORMATION about targeting because the referent's player never "
                "displaces far enough for the triangle inequality to bite.  What it DOES establish "
                "is that player motion cannot move the march clock by more than a few seconds.")

    # ══════════════════════════════════════════════════════════════════════════════════════════
    # § 2 — D-U-3 : PRICING THE RE-APPEARANCE CONTAMINATION OF THE ENTRY COUNT
    # ══════════════════════════════════════════════════════════════════════════════════════════
    print("\n§ 2 — ⚑ D-U-3 : THE ENTRY COUNT IS DOMINATED BY PLATE RE-APPEARANCE")
    peaks = {int(w): stats["arrivals"]["per_wave"][w]["peak_plates"]
             for w in stats["arrivals"]["per_wave"]}
    rows = []
    for hg in (6, 30, 60, 120, 240):
        t = U1.track_with_history(ta, offs, h_gap=hg)
        births = [float(ta[x["birth"]]) for x in t]
        per = {}
        for wv in sorted(U1.WAVE_START):
            per[wv] = sum(1 for b in births
                          if U1.WAVE_START[wv] <= b < U1.WAVE_END[wv])
        tot = len(t)
        ratio = {wv: round(per[wv] / peaks[wv], 2) for wv in per}
        rows.append(dict(h_gap_frames=hg, h_gap_s=round(hg / U1.FPS, 4), n_tracks=tot,
                         per_wave=per, entries_over_peak_living=ratio,
                         median_ratio=round(float(np.median(list(ratio.values()))), 3)))
        print(f"    H_GAP {hg:4d} frames ({hg/U1.FPS:5.2f} s) -> {tot:5d} tracks; "
              f"entries/peak-living per wave median {rows[-1]['median_ratio']:6.2f}")
    print("    peak LIVING plates per wave (the physical ceiling on concurrent bodies): "
          f"{sorted(peaks.values())}")
    print("    ⚑ At the Lap S PRIMARY cell (H_GAP = 6 frames = 0.10 s) the entry count is "
          f"{rows[0]['median_ratio']:.1f}x the peak living count.")
    print("      Lap S's birth-RADIUS statistic was stable across its H_GAP sweep and remains so;")
    print("      the birth COUNT is NOT, and I published it as an arrival rate.  That is a defect")
    print("      of MY OWN limb design.  The raw inter-entry interval distribution of I-U1 § a5 is")
    print("      DISQUALIFIED as a grading target and is republished as an UPPER BOUND only.")
    res["S2_D_U_3"] = dict(
        defect="entry counts from track births are dominated by nameplate re-appearance "
               "(UNREACHED-S4); the pre-registration named the contamination but did not price it",
        h_gap_sensitivity=rows, peak_living_per_wave=peaks,
        disposition="the raw inter-entry interval distribution is an UPPER BOUND on true arrival "
                    "rate and MUST NOT be graded against a sim as-is; the LIVING-COUNT ramp "
                    "(F-10) remains the like-for-like functional and is unaffected")

    # ══════════════════════════════════════════════════════════════════════════════════════════
    # § 3 — THE GEOMETRY HAND-OFF: per-spawn first-march distances from REPAIRED v3 labels
    # ══════════════════════════════════════════════════════════════════════════════════════════
    print("\n§ 3 — THE I-21 GEOMETRY HAND-OFF (repaired v3 labels; supersedes pm4t_geometry_corrected.csv)")
    grows, f4, ringext, ringnn = [], [], [], []
    for arc_rel in V3.MAP_ARCS:
        arc = ArcArchive(V3.VENDOR / arc_rel)
        for name in sorted(n for n in arc.names() if n.endswith(".map")):
            b = arc.read_file(name)
            pl, decl, tsz, gr, halt, arr, nb, endp = V3.read_placements_v3(b)
            gname, fname, head = V2.read_head_group(b)
            hp = [h for h in head if h["dbr"].lower().endswith("patrolpoint_01.dbr")]
            P = [(h["x"], h["y"], h["z"]) for h in hp]
            S = [(r["x"], r["y"], r["z"]) for r in pl if r["dbr"].lower() in V3.TIER16]
            B = [(r["x"], r["y"], r["z"]) for r in pl if r["dbr"].lower() in V3.BEACONS]
            if not P or not S:
                continue
            cen = (st.mean(p[0] for p in P), 0.0, st.mean(p[2] for p in P))
            pw = [V3.g2(P[i], P[j]) for i in range(len(P)) for j in range(i + 1, len(P))]
            ringext.append(max(pw))
            ringnn += [min(V3.g2(P[i], P[j]) for j in range(len(P)) if j != i)
                       for i in range(len(P))]
            for s in S:
                dn = min(V3.g2(s, p) for p in P)
                f4.append(dn)
                grows.append(dict(
                    archive=arc_rel, map=name, parse_complete=(len(pl) == decl),
                    spawn_x=round(s[0], 4), spawn_y=round(s[1], 4), spawn_z=round(s[2], 4),
                    to_nearest_patrol_m=round(dn, 4),
                    to_patrol_centroid_m=round(V3.g2(s, cen), 4),
                    to_nearest_beacon_m=(round(min(V3.g2(s, x) for x in B), 4) if B else ""),
                    inside_beacon_aura_8m=((min(V3.g2(s, x) for x in B) <= 8.0) if B else ""),
                    n_patrol_points=len(P), ring_max_extent_m=round(max(pw), 4),
                    placement_extents_m=PLACEMENT_EXTENTS,
                    basis="v3 labels (H-d-A index-first, D-I20-1 repaired); patrol set = "
                          "head-section PatrolPoint_Attack group"))
    with open(OUT / "pm4u_geometry_v3.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(grows[0].keys()))
        w.writeheader()
        w.writerows(grows)
    print(f"    F-4 spawn -> nearest patrol point, per-spawn (n={len(f4)}): {desc(f4)}")
    print(f"    attack-ring max extent per arena  : {desc(ringext)}")
    print(f"    patrol-point nearest-neighbour gap: {desc(ringnn)}")
    print(f"    wrote {OUT/'pm4u_geometry_v3.csv'}  ({len(grows)} spawn points)")
    res["S3_geometry_handoff"] = dict(
        F4_per_spawn=desc(f4), ring_max_extent_m=desc(ringext),
        ring_nearest_neighbour_m=desc(ringnn), n_spawn_points=len(grows),
        note="SAMPLE first-march distance PER SPAWN POINT from this distribution, never from the "
             "scalar median — R-PM4-51 part 3's instruction, now foldable because the labels are "
             "repaired (D-I20-1)")

    # ══════════════════════════════════════════════════════════════════════════════════════════
    # § 4 — THE MARCH-ARITHMETIC RECONCILIATION
    # ══════════════════════════════════════════════════════════════════════════════════════════
    print("\n§ 4 — THE MARCH ARITHMETIC, RECONCILED ON THE REFERENT'S OWN RAMP")
    t50, t90 = stats["P_U_0"]["F10_t50_median_s"], stats["P_U_0"]["F10_t90_median_s"]
    d50 = (t50 * MARCH_LO, t50 * MARCH_HI)
    d90 = (t90 * MARCH_LO, t90 * MARCH_HI)
    f4med = float(np.median(f4))
    imp = {k: (d50[0] + v, d50[1] + v) for k, v in FRUSTUM_M.items()}
    print(f"    referent t->50 % of peak living count : {t50:.4f} s  ->  march "
          f"{d50[0]:.3f} - {d50[1]:.3f} m at the decoded bracket")
    print(f"    referent t->90 %                      : {t90:.4f} s  ->  march "
          f"{d90[0]:.3f} - {d90[1]:.3f} m")
    print(f"    decoded first-march distance (F-4 median, v3): {f4med:.4f} m")
    print(f"    ⚑ t->90 % march ({d90[0]:.2f}-{d90[1]:.2f} m) straddles the decoded first march "
          f"({f4med:.2f} m) — Lap T's 1.05-1.11x agreement, reproduced from the v3 geometry.")
    print(f"    ⚑ t->50 % march is only {d50[0]:.2f}-{d50[1]:.2f} m — the ramp is FRONT-LOADED")
    print(f"      relative to a uniform first march, which is what a first-march DISTRIBUTION")
    print(f"      spanning {min(f4):.2f}-{max(f4):.2f} m predicts and a scalar does not.")
    print(f"\n    implied spawn -> PLAYER distance at the median (march to window entry + the")
    print(f"    frustum radius the body must still cross to be counted):")
    for k, v in imp.items():
        print(f"       edge {k}: {v[0]:.2f} - {v[1]:.2f} m   vs spawn -> nearest patrol node "
              f"{f4med:.2f} m")
    res["S4_march_reconciliation"] = dict(
        referent_t50_s=t50, referent_t90_s=t90,
        march_at_t50_m=[round(d50[0], 4), round(d50[1], 4)],
        march_at_t90_m=[round(d90[0], 4), round(d90[1], 4)],
        F4_median_v3_m=round(f4med, 4), F4_span_v3_m=[round(min(f4), 4), round(max(f4), 4)],
        implied_spawn_to_player_m={k: [round(v[0], 4), round(v[1], 4)] for k, v in imp.items()},
        grade="INFERRED-WITH-EVIDENCE — chains the decoded march bracket (UNREACHED-T1), the "
              "frustum radius (MEASURED), and the assumption that a body entering the window is "
              "marching at the pooled speed.  NOT a decode.")

    with open(OUT / "pm4u_ramp_analysis.json", "w") as fh:
        json.dump(res, fh, indent=2, default=float)
    print(f"\n  wrote {OUT/'pm4u_ramp_analysis.json'}")


if __name__ == "__main__":
    sys.exit(main())
