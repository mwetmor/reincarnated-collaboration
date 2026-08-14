#!/usr/bin/env python3
"""
pm4t_pricing_2026_08_14.py — RUN KC2-PM4 LAP T, INSTRUMENT I-T2b.

LIMB (b) closing half: convert the decoded roster `characterRunSpeed` scalars into m/s and price
the march against the referent's measured arrival ramp.

ROUTE 1 (decode the unit from the binary) FAILED, as pre-registered (P-B4). What IS decoded:
    `Character::GetRunSpeed(bool)` (Game.dll 0x54750) is percent arithmetic -- its only literals
    are 0.01 / 1.0 / 100.0 -- so it returns a MULTIPLIER, not a world rate.
    `Character::GetSpeed()` (0x5caa0) is `sqrt(vx^2+vy^2+vz^2)` -- a query of the physics
    velocity, not its producer. The scalar->world-rate conversion is not recoverable as a
    literal from the stripped release binary.

ROUTE 2 (player calibration) -- INFERRED-WITH-EVIDENCE, never MEASURED.
    The player's three quantities are all independently measured by earlier laps:
        characterRunSpeed = 0.93                         (Lap R, malepc01/femalepc01, identical)
        modifier          = 135 %  (AT playerRunSpeedCapMax) (Lap R finding 5)
        world speed       = 4.029485 / 3.836070 m/s      (banked at L-38, px-LO / px-HI)
    => K = v_world / (characterRunSpeed x modifier)
    APPLYING K TO MONSTERS ASSUMES PLAYER AND MONSTER SHARE ONE LOCOMOTION CONSTANT.
    That assumption is NAMED and the result is carried as a BRACKET, never a point.

READ-ONLY.
"""
import csv
import json
import pathlib
import statistics as st

OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/notes/2026-08-14-kc2-pm4-lap-t-arrival-decode")

# --- carried constants, each with its emitting lap named (NOTE-9)
PLAYER_RUNSPEED = 0.93            # Lap R  records/creatures/pc/malepc01.dbr
PLAYER_MODIFIER = 1.35            # Lap R  gameengine.dbr :: playerRunSpeedCapMax = 135.0
PLAYER_V = {"px-LO": 4.029485, "px-HI": 3.836070}   # L-38, banked
# --- decoded this lap
MARCH_NEAR = 16.7992              # I-T3c corrected  spawn -> NEAREST patrol point, median
MARCH_RING = 35.8787              # I-T3c corrected  spawn -> patrol-point CENTROID, median
# --- referent, Lap S F-10 (MEASURED, living-plate counts)
REF_T50, REF_T90 = 3.27, 4.97


def main():
    march = json.load(open(OUT / "pm4t_march_summary.json"))
    K = {k: v / (PLAYER_RUNSPEED * PLAYER_MODIFIER) for k, v in PLAYER_V.items()}

    rows, table = [], {}
    for cls, d in march["by_classification"].items():
        c = d["characterRunSpeed"]
        # bodies with characterRunSpeed == 0 are immobile by record; excluded from the march
        # table and counted, never averaged in.
        distinct = [v for v in c["distinct"] if v > 0]
        entry = {"classification": cls, "n_records": d["n_records"],
                 "runspeed_median": c["median"], "runspeed_min_nonzero": min(distinct),
                 "runspeed_max": c["max"], "n_zero_runspeed": c["distinct"].count(0.0)}
        for arm, k in K.items():
            entry[f"m_per_s_median_{arm}"] = round(c["median"] * k, 4)
            entry[f"m_per_s_min_{arm}"] = round(min(distinct) * k, 4)
            entry[f"m_per_s_max_{arm}"] = round(c["max"] * k, 4)
            entry[f"t_march_NEAR_s_{arm}"] = round(MARCH_NEAR / (c["median"] * k), 4)
            entry[f"t_march_RING_s_{arm}"] = round(MARCH_RING / (c["median"] * k), 4)
        rows.append(entry)
        table[cls] = entry

    pooled_med = march["characterRunSpeed_pooled"]["median"]
    arrival = {}
    for arm, k in K.items():
        v = pooled_med * k
        arrival[arm] = {
            "K_m_per_s_per_unit": round(k, 6),
            "pooled_median_runspeed": pooled_med,
            "monster_march_speed_m_per_s": round(v, 4),
            "t_NEAR_s": round(MARCH_NEAR / v, 4),
            "t_RING_s": round(MARCH_RING / v, 4),
            "NEAR_vs_referent_t90": round((MARCH_NEAR / v) / REF_T90, 4),
            "RING_vs_referent_t90": round((MARCH_RING / v) / REF_T90, 4),
        }

    summary = {
        "instrument": "I-T2b",
        "route1_binary_decode": "FAILED as pre-registered (P-B4); see module docstring",
        "route2_calibration": {
            "grade": "INFERRED-WITH-EVIDENCE",
            "named_assumption": "player and monster share one locomotion constant K",
            "player_runspeed": PLAYER_RUNSPEED, "player_modifier": PLAYER_MODIFIER,
            "player_world_speed_m_per_s": PLAYER_V, "K": {k: round(v, 6) for k, v in K.items()},
        },
        "march_distances_m": {"NEAR": MARCH_NEAR, "RING": MARCH_RING,
                              "basis": "I-T3c corrected placement reader, medians over 110 "
                                       "tier-16 spawn points / 18 complete arenas"},
        "referent_ramp_s": {"t50": REF_T50, "t90": REF_T90,
                            "basis": "Lap S F-10, living-plate counts"},
        "arrival_arithmetic": arrival,
        "by_classification": table,
        "no_permanent_modifier_anywhere": {
            "roster_records_with_nonzero_characterRunSpeedModifier":
                len(march["characterRunSpeedModifier_nonzero_records"]),
            "crucible_wave_scaling_runspeed_terms": 0,
            "beacon_runspeed_terms": 0,
        },
    }
    with open(OUT / "pm4t_march_pricing.json", "w") as fh:
        json.dump(summary, fh, indent=2)
    with open(OUT / "pm4t_march_pricing.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print("K (m/s per characterRunSpeed unit):", {k: round(v, 6) for k, v in K.items()})
    print(f"\nreferent ramp: t50 {REF_T50} s   t90 {REF_T90} s")
    print(f"march distances (corrected): NEAR {MARCH_NEAR:.2f} m   RING {MARCH_RING:.2f} m\n")
    for arm, a in arrival.items():
        print(f"  {arm}: monster march {a['monster_march_speed_m_per_s']} m/s | "
              f"t_NEAR {a['t_NEAR_s']} s ({a['NEAR_vs_referent_t90']}x t90) | "
              f"t_RING {a['t_RING_s']} s ({a['RING_vs_referent_t90']}x t90)")
    print("\nper body class (px-LO arm):")
    print(f"  {'class':10s} {'n':>4s} {'runSpd':>7s} {'m/s':>7s} {'tNEAR':>7s} {'tRING':>7s} {'v0':>3s}")
    for r in rows:
        print(f"  {r['classification']:10s} {r['n_records']:4d} {r['runspeed_median']:7.3f} "
              f"{r['m_per_s_median_px-LO']:7.3f} {r['t_march_NEAR_s_px-LO']:7.3f} "
              f"{r['t_march_RING_s_px-LO']:7.3f} {r['n_zero_runspeed']:3d}")


if __name__ == "__main__":
    main()
