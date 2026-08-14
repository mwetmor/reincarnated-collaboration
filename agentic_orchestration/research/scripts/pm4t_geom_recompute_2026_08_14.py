#!/usr/bin/env python3
"""
pm4t_geom_recompute_2026_08_14.py — RUN KC2-PM4 LAP T, INSTRUMENT I-T3c.

Recomputes Lap S's F-3 / F-4 / F-5 and Lap T's beacon geometry from the CORRECTED placement
reader (`pm4t_map_v2_2026_08_14.py`), and diffs them against Lap S's published numbers.

Lap S's numbers were produced by a reader that dropped every GUID-bearing placement record
(defect `D-T-3`). These are the repaired values. Both are printed side by side; no Lap S artifact
is modified.

Patrol points are taken from the head-section `PatrolPoint_Attack` group, which the corrected
reader has now shown to be byte-identical (residual 0.000 m) to the GUID-matched placement rows --
so the choice between the two structures, which was `D-I19-3`, is now moot.

READ-ONLY.
"""
import csv
import json
import math
import pathlib
import statistics as st
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pm4t_map_v2_2026_08_14 as V
from gd_arc_reader_2026_07_26 import ArcArchive

OUT = V.OUT
TIER16 = {"records/scriptentities/tier16spawnpoint01.dbr"} | {
    f"records/scriptentities/spawnpoint0{i}.dbr" for i in range(2, 7)}
BEACONS = {f"records/scriptentities/spawnbeacon_0{i}.dbr" for i in range(1, 6)}
AURA_R = 8.0

# Lap S published values, for the side-by-side (NOT re-derived here; quoted)
LAPS_F3 = {"min": 3.56, "median": 37.03, "mean": 34.36, "max": 51.42, "n": 114}
LAPS_F4 = {"min": 0.65, "median": 17.07, "mean": 16.09, "max": 37.51}


def g(a, b):
    return math.hypot(a[0] - b[0], a[2] - b[2])


def main():
    per_arena, f3, f4, f5, beac = [], [], [], [], []
    rows = []
    for arc_rel in V.MAP_ARCS:
        arc = ArcArchive(V.VENDOR / arc_rel)
        for name in sorted(n for n in arc.names() if n.endswith(".map")):
            b = arc.read_file(name)
            pl, declared, tsize, guid_rows, halt = V.read_placements_v2(b)
            gname, fname, head = V.read_head_group(b)
            complete = (len(pl) == declared)
            P = [(h["x"], h["y"], h["z"]) for h in head
                 if h["dbr"].lower().endswith("patrolpoint_01.dbr")]
            S = [(r["x"], r["y"], r["z"]) for r in pl if r["dbr"].lower() in TIER16]
            B = [(r["x"], r["y"], r["z"]) for r in pl if r["dbr"].lower() in BEACONS]
            if not P or not S:
                per_arena.append({"arc": arc_rel, "map": name, "complete": complete,
                                  "note": "insufficient geometry", "n_spawn": len(S),
                                  "n_patrol": len(P), "n_beacon": len(B)})
                continue
            cen = (st.mean(p[0] for p in P), 0.0, st.mean(p[2] for p in P))
            d_cen = [g(s, cen) for s in S]
            d_near = [min(g(s, p) for p in P) for s in S]
            pair = [g(S[i], S[j]) for i in range(len(S)) for j in range(i + 1, len(S))]
            nb = [min(g(s, x) for x in B) for s in S] if B else []
            f3 += d_cen
            f4 += d_near
            if pair:
                f5.append(max(pair))
            beac += nb
            for i, s in enumerate(S):
                rows.append({"archive": arc_rel, "map": name, "complete": complete,
                             "spawn_x": s[0], "spawn_z": s[2],
                             "to_patrol_centroid_m": round(d_cen[i], 4),
                             "to_nearest_patrol_m": round(d_near[i], 4),
                             "to_nearest_beacon_m": round(nb[i], 4) if nb else "",
                             "inside_beacon_aura": (nb[i] <= AURA_R) if nb else ""})
            per_arena.append({
                "arc": arc_rel, "map": name, "complete": complete,
                "n_spawn": len(S), "n_patrol": len(P), "n_beacon": len(B),
                "centroid_med": round(st.median(d_cen), 4),
                "nearest_med": round(st.median(d_near), 4),
                "pairwise_max": round(max(pair), 4) if pair else None,
                "spawn_in_aura": sum(1 for x in nb if x <= AURA_R) if nb else 0,
            })

    def desc(v):
        return {"n": len(v), "min": round(min(v), 4), "median": round(st.median(v), 4),
                "mean": round(st.mean(v), 4), "max": round(max(v), 4)}

    summary = {
        "instrument": "I-T3c",
        "patrol_source": "head-section PatrolPoint_Attack group (== GUID-matched placement rows, residual 0.000 m)",
        "F3_spawn_to_patrol_centroid_CORRECTED": desc(f3),
        "F3_lapS_published": LAPS_F3,
        "F4_spawn_to_nearest_patrol_CORRECTED": desc(f4),
        "F4_lapS_published": LAPS_F4,
        "F5_spawn_pairwise_max_per_arena": desc(f5),
        "beacon_spawn_to_nearest_beacon": desc(beac) if beac else None,
        "spawn_points_inside_beacon_aura": sum(1 for x in beac if x <= AURA_R),
        "spawn_points_total": len(beac),
        "per_arena": per_arena,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "pm4t_geometry_corrected.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(OUT / "pm4t_geometry_corrected.json", "w") as fh:
        json.dump(summary, fh, indent=2)

    print(json.dumps({k: v for k, v in summary.items() if k != "per_arena"}, indent=2))
    print("\nper-arena (complete parses only marked True):")
    for a in per_arena:
        print(f"  {a['arc'].split('/')[0]}:{a['map']:26s} ok={str(a['complete']):5s} "
              f"spawn={a.get('n_spawn')} patrol={a.get('n_patrol')} beacon={a.get('n_beacon')} "
              f"cen_med={a.get('centroid_med')} near_med={a.get('nearest_med')} "
              f"in_aura={a.get('spawn_in_aura')}")


if __name__ == "__main__":
    main()
