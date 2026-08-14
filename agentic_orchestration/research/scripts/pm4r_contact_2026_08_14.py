#!/usr/bin/env python3
"""KC2-PM4 Lap R — LIMB A/B JOIN: the referent's CONTACT OCCUPANCY from the nameplate census.

This is the measurement that maps most directly onto the simulation's own `dry_fraction`
definition ("fraction of ticks with no body in the player's kill disc"), because it asks the
same question of the referent's pixels: at each 60 fps instant, is there a LIVING BODY inside
the player's contact ring?

  MEASURED QUANTITY : fraction of 60 fps instants with ZERO living monster nameplates within
                      R_CONTACT ground px of the player's plate anchor.
  BOUND DIRECTION   : a nameplate PROVES a living body; its absence does NOT prove absence
                      (occlusion, VFX saturation, plate-suppressed bodies).  Every count is a
                      LOWER BOUND on bodies -> the dry fraction here is an UPPER BOUND on the
                      referent's true dry fraction.  ONE-DIRECTIONAL, declared.

Source: Lap H-2 nameplate census (98,794 monster plates + 10,316 player rows over 11,039 frames
at 60 fps, whole fight 683-866 s), pinned at sha256 28e7d9df...f7df.

READ-ONLY.  OUTCOME-FIREWALLED.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.
"""
from __future__ import annotations

import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from pm4r_lib_2026_08_14 import (                                             # noqa: E402
    OUT, K_GROUND, FIGHT_T0, FIGHT_T1, WAVE_START, WAVE_END,
    R_CONTACT_GPX, R_CONTACT_SENSITIVITY, wave_of, sha256,
)

PLATES = OUT / "method" / "plates60_lapH2.npy"
PLATES_SHA = "28e7d9dfcdff9316ccde86fd116d55655f8fa0436cd06b95b38d3cd1ff7cf7df"


def main():
    got = sha256(PLATES)
    assert got == PLATES_SHA, f"HALT (GL-6): plates60 digest {got}"
    print("=" * 100)
    print("KC2-PM4 LAP R — CONTACT OCCUPANCY from the nameplate census")
    print("=" * 100)
    print(f"  EXACT  {got}  plates60_lapH2.npy")

    R = np.load(PLATES)
    P = {}
    for r in R[R[:, 1] == 1]:
        if abs(r[2] - 960) < 50 and abs(r[3] - 429) < 16:
            P[round(r[0], 4)] = (r[2], r[3])
    M = R[R[:, 1] == 0]
    bym = {}
    for r in M:
        bym.setdefault(round(r[0], 4), []).append((r[2], r[3]))

    times = sorted(t for t in P if FIGHT_T0 <= t <= FIGHT_T1)
    print(f"\n  instants with a detected PLAYER plate in 683-864 s : {len(times)}")
    print(f"  (Lap H-2 player-plate coverage 94.6 % of 60 fps frames; instants without a player "
          f"plate are EXCLUDED, not imputed)")

    res = {"n_instants": len(times), "span": [FIGHT_T0, FIGHT_T1],
           "source": str(PLATES), "source_sha256": got,
           "bound_direction": "plate absence does not prove body absence -> counts are LOWER "
                              "bounds -> dry fraction is an UPPER BOUND"}

    counts = {}
    for RC in R_CONTACT_SENSITIVITY:
        c = np.empty(len(times), dtype=np.int32)
        for i, t in enumerate(times):
            pl = P[t]
            bl = bym.get(t, ())
            c[i] = sum(1 for x, y in bl
                       if np.hypot(x - pl[0], (y - pl[1]) / K_GROUND) <= RC)
        counts[RC] = c
        dry = float((c == 0).mean())
        print(f"\n  R_CONTACT = {RC:.0f} ground px")
        print(f"    DRY (zero living plates in ring) : {int((c==0).sum())}/{len(c)} = {dry:.4f}")
        print(f"    occupancy  mean {c.mean():.2f}  median {np.median(c):.0f}  "
              f"p90 {np.percentile(c,90):.0f}  max {c.max()}")
        res[f"R{int(RC)}"] = dict(
            dry_fraction=round(dry, 6), n_dry=int((c == 0).sum()), n=len(c),
            mean_occupancy=round(float(c.mean()), 4),
            median_occupancy=float(np.median(c)),
            p90_occupancy=float(np.percentile(c, 90)),
            max_occupancy=int(c.max()),
        )

    # ── THE FULL RADIUS CURVE ────────────────────────────────────────────────────────────────
    # R_CONTACT is the single most sensitive choice in this measurement, so the whole curve is
    # published rather than one rung.  The ground-px -> metre conversion is Lap H-2's DECLARED
    # GAP (OBS-H2-9); three candidate anchors are carried in the findings, each with its own
    # named assumption, and NONE is ruled here.  The curve lets the consumer pick the radius.
    print("\n  DRY-FRACTION vs CONTACT RADIUS (the full curve — no rung is preferred)")
    print(f"    {'R_gpx':>7} {'dry_frac':>9} {'mean_occ':>9} {'med_occ':>8} {'longest_dry_s':>14}")
    curve = []
    for RC in (60, 80, 100, 120, 150, 180, 220, 260, 300, 350, 400, 450, 500, 600, 800):
        cc = np.empty(len(times), dtype=np.int32)
        for i, t in enumerate(times):
            pl = P[t]
            cc[i] = sum(1 for x, y in bym.get(t, ())
                        if np.hypot(x - pl[0], (y - pl[1]) / K_GROUND) <= RC)
        d = cc == 0
        rr, i2 = [], 0
        taa = np.asarray(times)
        while i2 < len(d):
            if not d[i2]:
                i2 += 1
                continue
            j = i2
            while j + 1 < len(d) and d[j + 1] and (taa[j + 1] - taa[j]) < 0.05:
                j += 1
            rr.append(float(taa[j] - taa[i2]))
            i2 = j + 1
        row = dict(R_gpx=RC, dry_fraction=round(float(d.mean()), 6),
                   mean_occupancy=round(float(cc.mean()), 4),
                   median_occupancy=float(np.median(cc)),
                   n_dry_runs=len(rr),
                   longest_dry_run_s=round(max(rr), 4) if rr else 0.0)
        curve.append(row)
        print(f"    {RC:>7} {row['dry_fraction']:>9.4f} {row['mean_occupancy']:>9.2f} "
              f"{row['median_occupancy']:>8.0f} {row['longest_dry_run_s']:>14.2f}")
    res["radius_curve"] = curve

    # dry RUNS at the primary radius
    c = counts[R_CONTACT_GPX]
    ta = np.asarray(times)
    dry = c == 0
    runs, i = [], 0
    while i < len(dry):
        if not dry[i]:
            i += 1
            continue
        j = i
        while j + 1 < len(dry) and dry[j + 1] and (ta[j + 1] - ta[j]) < 0.05:
            j += 1
        runs.append((float(ta[i]), float(ta[j]), float(ta[j] - ta[i])))
        i = j + 1
    runs_s = sorted(runs, key=lambda z: -z[2])
    print(f"\n  dry RUNS at R={R_CONTACT_GPX:.0f} : {len(runs)} runs; longest "
          f"{runs_s[0][2]:.2f} s @ t={runs_s[0][0]:.2f} (wave {wave_of(runs_s[0][0])})")
    print("  ten longest dry runs:")
    for r in runs_s[:10]:
        print(f"    t={r[0]:8.2f} .. {r[1]:8.2f}   {r[2]:6.2f} s   wave {wave_of(r[0])}")
    res["dry_runs_primary"] = dict(
        n_runs=len(runs),
        longest_s=round(runs_s[0][2], 4),
        longest_t=round(runs_s[0][0], 3),
        longest_wave=wave_of(runs_s[0][0]),
        median_run_s=round(float(np.median([r[2] for r in runs])), 4),
        ten_longest=[dict(t_start=round(r[0], 3), t_end=round(r[1], 3),
                          duration_s=round(r[2], 4), wave=wave_of(r[0])) for r in runs_s[:10]],
        total_dry_s=round(float(sum(r[2] for r in runs)), 3),
    )

    # per wave
    print(f"\n  per-wave contact occupancy (R={R_CONTACT_GPX:.0f}):")
    print(f"    {'wave':>5} {'span_s':>8} {'n':>6} {'dry_frac':>9} {'mean_occ':>9} "
          f"{'med_occ':>8} {'max':>5} {'longest_dry_s':>14}")
    pw = []
    for w in sorted(WAVE_START):
        a, b = WAVE_START[w], WAVE_END[w]
        m = (ta >= a) & (ta < b)
        if not m.any():
            continue
        cc = c[m]
        wr = [r for r in runs if a <= r[0] < b]
        row = dict(wave=w, t_start=a, t_end=round(b, 3), span_s=round(b - a, 3),
                   n_instants=int(m.sum()),
                   dry_fraction=round(float((cc == 0).mean()), 6),
                   mean_occupancy=round(float(cc.mean()), 3),
                   median_occupancy=float(np.median(cc)),
                   max_occupancy=int(cc.max()),
                   longest_dry_run_s=round(max((r[2] for r in wr), default=0.0), 4))
        pw.append(row)
        print(f"    {w:>5} {row['span_s']:>8.1f} {row['n_instants']:>6} "
              f"{row['dry_fraction']:>9.4f} {row['mean_occupancy']:>9.2f} "
              f"{row['median_occupancy']:>8.0f} {row['max_occupancy']:>5} "
              f"{row['longest_dry_run_s']:>14.2f}")
    res["per_wave"] = pw

    # final-200-ticks analogue: the last 200 * (sim tick) -- reported instead as the final
    # 10 % and the final 20 s of the referent's fight, both stated plainly as NOT the sim's
    # window (the sim's tick length is not a referent quantity and is not imported).
    for tag, t0 in (("final_20s", FIGHT_T1 - 20.0), ("final_10pct", FIGHT_T1 - 18.1)):
        m = ta >= t0
        res[tag] = dict(t_start=round(float(t0), 2), n=int(m.sum()),
                        dry_fraction=round(float((c[m] == 0).mean()), 6),
                        mean_occupancy=round(float(c[m].mean()), 3))
        print(f"\n  {tag} (t >= {t0:.1f}): dry {res[tag]['dry_fraction']:.4f}, "
              f"mean occupancy {res[tag]['mean_occupancy']:.2f}")

    # ── GROUND-PIXEL -> METRE anchors (Lap H-2 OBS-H2-9's DECLARED GAP, revisited) ───────────
    # NOT RULED here.  Three candidate anchors are computed, each with its assumption named.
    # Lap H-2 declined the conversion because its two candidates DISAGREED.  These are new.
    print("\n  GROUND-PIXEL -> METRE anchors (candidates; NOT ruled — Lap H-2 OBS-H2-9)")
    anchors = []

    # (a) the player's own ground decal vs the player's own actorRadius
    #     Lap H-2 OBS-H2-8: decal 80 x 43 px at t=683.500 -> half-major = 40 ground px.
    #     Lap F Q4: records/creatures/pc/{male,female}pc01.dbr actorRadius = 0.32, scale = 1.05.
    #     ASSUMPTION: the drawn ground decal's radius equals the collision actorRadius.
    for label, rad in (("LO radius = actorRadius", 0.3199999928474426),
                       ("HI radius = actorRadius x scale", 0.3199999928474426 * 1.0499999523162842)):
        anchors.append(dict(anchor="a_player_ground_decal", variant=label,
                            gpx_per_m=round(40.0 / rad, 3),
                            assumption="drawn ground decal radius == collision actorRadius",
                            grade="INDICATIVE"))

    # (c) cross-calibration of two INDEPENDENT instruments: the FCT presence stream and the
    #     nameplate geometry.  Find R* where the plate dry fraction equals the FCT dry fraction
    #     (0.165289 measured at 0.5 s cadence), then set R* == EoR skillTargetRadius 3.0 m.
    #     ASSUMPTION: "no player-side damage landed" ~ "no body inside the EoR target radius".
    #     TWO-SIDED BIAS, both named: FCT-lifetime dilation pushes R* DOWN; pet/proc/DoT damage
    #     from outside the ring pushes R* UP.  Graded INDICATIVE, never MEASURED.
    FCT_DRY = 0.165289
    xs = [c["R_gpx"] for c in curve]
    ys = [c["dry_fraction"] for c in curve]
    rstar = None
    for i in range(len(xs) - 1):
        if ys[i] >= FCT_DRY >= ys[i + 1]:
            f = (ys[i] - FCT_DRY) / (ys[i] - ys[i + 1])
            rstar = xs[i] + f * (xs[i + 1] - xs[i])
            break
    if rstar:
        anchors.append(dict(anchor="c_fct_x_plate_cross_calibration",
                            variant=f"R*={rstar:.1f} gpx == EoR skillTargetRadius 3.0 m",
                            gpx_per_m=round(rstar / 3.0, 3),
                            assumption="'no player-side damage landed' ~ 'no body inside 3.0 m'; "
                                       "two-sided bias (FCT dilation down, pet/proc reach up)",
                            grade="INDICATIVE"))
    for a in anchors:
        print(f"    {a['anchor']:<34} {a['variant']:<42} -> {a['gpx_per_m']:7.1f} gpx/m")
    vals = [a["gpx_per_m"] for a in anchors]
    print(f"    -> BRACKET {min(vals):.1f} .. {max(vals):.1f} gpx/m  "
          f"(spread {100*(max(vals)-min(vals))/np.mean(vals):.1f} % of the mean)")
    res["metre_anchors"] = anchors
    res["metre_anchor_bracket_gpx_per_m"] = [round(min(vals), 2), round(max(vals), 2)]

    # what the sim's OWN pre-existing constant maps to, under the bracket
    print("\n  the sim's D_ENGAGE_M = 2.400 m, converted through the bracket, and the referent's "
          "dry fraction there:")
    conv = []
    for gpm in (min(vals), float(np.mean(vals)), max(vals)):
        R = 2.400 * gpm
        # measure directly at that radius rather than interpolating the curve
        cc = np.empty(len(times), dtype=np.int32)
        for i, t in enumerate(times):
            pl = P[t]
            cc[i] = sum(1 for x, y in bym.get(t, ())
                        if np.hypot(x - pl[0], (y - pl[1]) / K_GROUND) <= R)
        d = cc == 0
        rr, i2, taa = [], 0, np.asarray(times)
        while i2 < len(d):
            if not d[i2]:
                i2 += 1
                continue
            j = i2
            while j + 1 < len(d) and d[j + 1] and (taa[j + 1] - taa[j]) < 0.05:
                j += 1
            rr.append(float(taa[j] - taa[i2]))
            i2 = j + 1
        row = dict(gpx_per_m=round(gpm, 2), R_gpx=round(R, 1),
                   dry_fraction=round(float(d.mean()), 6),
                   mean_occupancy=round(float(cc.mean()), 4),
                   n_dry_runs=len(rr),
                   longest_dry_run_s=round(max(rr), 4) if rr else 0.0)
        conv.append(row)
        print(f"    {gpm:7.1f} gpx/m -> R = {R:6.1f} gpx : dry {row['dry_fraction']:.4f}  "
              f"mean occupancy {row['mean_occupancy']:.2f}  "
              f"longest dry run {row['longest_dry_run_s']:.2f} s "
              f"({row['n_dry_runs']} runs)")
    res["at_sim_d_engage_2400mm"] = conv

    pathlib.Path("/tmp/pm4r/contact.json").write_text(json.dumps(res, indent=2, default=str))
    print("\ncontact.json written")


if __name__ == "__main__":
    main()
