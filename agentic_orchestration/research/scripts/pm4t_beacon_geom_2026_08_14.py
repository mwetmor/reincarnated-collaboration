#!/usr/bin/env python3
"""
pm4t_beacon_geom_2026_08_14.py — RUN KC2-PM4 LAP T, INSTRUMENT I-T1b.

LIMB (a), geometry half: given that the beacon aura is a `skillTargetRadius = 8.0` m passive
(instrument I-T1), decide from Lap S's measured placement rows:

  (1) which tier-16 spawn points fall inside a beacon aura at all;
  (2) whether the five beacon auras per arena OVERLAP (which is what makes the stacking rule
      matter -- if they are disjoint, stacking is MOOT and P-A5 is settled by geometry rather
      than by decoding an engine rule);
  (3) how far a marching pack travels before it LEAVES the aura.

Basis: `pm4s_arena_placements.csv` (Lap S, MEASURED; ground distance in the (x,z) plane per
Lap S § 2.1 -- y is the vertical axis).

READ-ONLY.
"""
import csv
import json
import math
import pathlib
import statistics as st

LAPS = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes")
PLACEMENTS = LAPS / "2026-08-14-kc2-pm4-lap-s-arena-advance" / "pm4s_arena_placements.csv"
OUT = LAPS / "2026-08-14-kc2-pm4-lap-t-arrival-decode"

AURA_R = 8.0            # spawnbeacon_aura_buff.dbr :: skillTargetRadius   (I-T1, MEASURED)
SCATTER = 8.0           # proxy placementExtents                            (Lap S F-2, MEASURED)

TIER16_SPAWN = {
    "records/scriptentities/tier16spawnpoint01.dbr",
    "records/scriptentities/spawnpoint02.dbr",
    "records/scriptentities/spawnpoint03.dbr",
    "records/scriptentities/spawnpoint04.dbr",
    "records/scriptentities/spawnpoint05.dbr",
    "records/scriptentities/spawnpoint06.dbr",
}
BEACONS = {f"records/scriptentities/spawnbeacon_0{i}.dbr" for i in range(1, 6)}
PATROL = "records/controllers/controlobjects/patrolpoint_01.dbr"


def d2(a, b):
    return math.hypot(a[0] - b[0], a[2] - b[2])


def main():
    rows = list(csv.DictReader(open(PLACEMENTS)))
    arenas = {}
    for r in rows:
        key = (r["archive"], r["map"])
        p = (float(r["x"]), float(r["y"]), float(r["z"]))
        arenas.setdefault(key, {"spawn": [], "beacon": [], "patrol": []})
        if r["dbr"] in TIER16_SPAWN:
            arenas[key]["spawn"].append((r["dbr"], p))
        elif r["dbr"] in BEACONS:
            arenas[key]["beacon"].append((r["dbr"], p))
        elif r["dbr"] == PATROL:
            arenas[key]["patrol"].append((r["dbr"], p))

    per_arena, cover_rows = [], []
    all_nearest, all_pairwise, n_covered, n_spawn = [], [], 0, 0
    for key in sorted(arenas):
        a = arenas[key]
        sp, bc, pt = a["spawn"], a["beacon"], a["patrol"]
        if not sp or not bc:
            continue
        centroid = (st.mean(p[0] for _, p in pt), 0.0, st.mean(p[2] for _, p in pt)) if pt else None

        covered = 0
        for sname, s in sp:
            nearest = min(d2(s, b) for _, b in bc)
            all_nearest.append(nearest)
            inside = nearest <= AURA_R
            covered += inside
            n_spawn += 1
            n_covered += inside
            # how far can a body scattered at `SCATTER` from this spawn point still be in aura?
            march_to_ring = d2(s, centroid) if centroid else None
            cover_rows.append({
                "archive": key[0], "map": key[1], "spawn_point": sname,
                "nearest_beacon_m": round(nearest, 4),
                "inside_aura": inside,
                "aura_exit_along_march_m": round(max(0.0, AURA_R - nearest), 4),
                "march_to_patrol_centroid_m": round(march_to_ring, 4) if march_to_ring else "",
                "aura_fraction_of_march": (round(max(0.0, AURA_R - nearest) / march_to_ring, 6)
                                           if march_to_ring else ""),
            })

        pair = [d2(b1, b2) for i, (_, b1) in enumerate(bc) for _, b2 in [x for x in bc][i + 1:]]
        all_pairwise += pair
        per_arena.append({
            "archive": key[0], "map": key[1],
            "n_spawn": len(sp), "n_beacon": len(bc), "n_patrol": len(pt),
            "spawn_covered_by_aura": covered,
            "beacon_pairwise_min_m": round(min(pair), 4) if pair else "",
            "auras_overlap": (min(pair) < 2 * AURA_R) if pair else "",
        })

    summary = {
        "instrument": "I-T1b",
        "aura_radius_m": AURA_R,
        "pack_scatter_m": SCATTER,
        "basis": "pm4s_arena_placements.csv (Lap S, MEASURED); ground distance in (x,z)",
        "arenas": len(per_arena),
        "tier16_spawn_points": n_spawn,
        "spawn_points_inside_a_beacon_aura": n_covered,
        "spawn_to_nearest_beacon_m": {
            "min": round(min(all_nearest), 4), "median": round(st.median(all_nearest), 4),
            "mean": round(st.mean(all_nearest), 4), "max": round(max(all_nearest), 4),
        },
        "beacon_pairwise_separation_m": {
            "min": round(min(all_pairwise), 4), "median": round(st.median(all_pairwise), 4),
            "max": round(max(all_pairwise), 4),
        },
        "any_two_auras_overlap": min(all_pairwise) < 2 * AURA_R,
        "overlap_threshold_m": 2 * AURA_R,
        "aura_exit_along_march_m": {
            "median": round(st.median([r["aura_exit_along_march_m"] for r in cover_rows]), 4),
            "max": round(max(r["aura_exit_along_march_m"] for r in cover_rows), 4),
        },
        "aura_fraction_of_march": {
            "median": round(st.median([r["aura_fraction_of_march"] for r in cover_rows
                                       if r["aura_fraction_of_march"] != ""]), 6),
            "max": round(max(r["aura_fraction_of_march"] for r in cover_rows
                             if r["aura_fraction_of_march"] != ""), 6),
        },
        "per_arena": per_arena,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "pm4t_beacon_coverage.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cover_rows[0].keys()))
        w.writeheader()
        w.writerows(cover_rows)
    with open(OUT / "pm4t_beacon_geometry.json", "w") as fh:
        json.dump(summary, fh, indent=2)

    print(json.dumps({k: v for k, v in summary.items() if k != "per_arena"}, indent=2))
    print("\nper-arena:")
    for a in per_arena:
        print(f"  {a['archive']}:{a['map']}  spawn={a['n_spawn']} beacon={a['n_beacon']} "
              f"covered={a['spawn_covered_by_aura']}  beacon_pair_min={a['beacon_pairwise_min_m']} "
              f"overlap={a['auras_overlap']}")


if __name__ == "__main__":
    main()
