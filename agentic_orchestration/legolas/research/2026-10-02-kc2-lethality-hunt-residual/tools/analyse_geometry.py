"""Standoff instruments: landed by hit distance, and the H-2 range-profile functional (moving vs
still bodies by distance band), oracle arm vs referent (Lap H-2 FOOTAGE)."""
import csv
import json
import sys

H2 = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/"
      "2026-08-13-kc2-pm4-lap-h2-video-match/pm4h2_d1_range_profile.csv")
DB = ("0-1.5", "1.5-2.5", "2.5-3.5", "3.5-5", "5-7.5", "7.5-11.5", "11.5-16", "16+")


def ref_bands():
    R = list(csv.DictReader(open(H2)))
    return [{"band_gpx": r["band"], "band_m": f"{float(r['lo'])/122:.2f}-{float(r['hi'])/122:.2f}",
             "still_frac": float(r["still_frac"]), "n_frames": int(r["n_frames"])} for r in R]


def summarise(path):
    d = json.load(open(path))
    dh = [0.0] * len(DB)
    mb = None
    tot = 0.0
    for s, rr in d["rows"].items():
        for r in rr:
            if r["wave"] > 159:
                continue
            for i, v in enumerate(r["ext"]["landed_by_hit_distance"]):
                dh[i] += v
            m = r["ext"]["mover_band_moving_still"]
            if mb is None:
                mb = [[0, 0] for _ in m]
            for i, (a, b) in enumerate(m):
                mb[i][0] += a
                mb[i][1] += b
    T = sum(dh)
    cum = 0.0
    med = None
    for i, v in enumerate(dh):
        cum += v
        if med is None and cum >= T / 2:
            med = DB[i]
    return {"arm": d["arm"], "ratio": d["summary"]["ratio_vs_referent"],
            "landed_share_by_hit_distance_m": {DB[i]: round(dh[i] / T, 3) for i in range(len(DB))},
            "median_hit_distance_band": med,
            "share_beyond_5m": round(sum(dh[5:]) / T + dh[4] / T, 3),
            "share_beyond_7p5m": round(sum(dh[5:]) / T, 3),
            "still_frac_by_band": [round(b / (a + b), 3) if (a + b) else None for a, b in mb],
            "body_steps_by_band": [a + b for a, b in mb]}


if __name__ == "__main__":
    out = {"referent_H2": ref_bands(), "arms": [summarise(p) for p in sys.argv[2:]]}
    json.dump(out, open(sys.argv[1], "w"), indent=1)
    print("referent still_frac:", [b["still_frac"] for b in out["referent_H2"]])
    for a in out["arms"]:
        print(a["arm"], a["ratio"], "median band", a["median_hit_distance_band"], ">5m", a["share_beyond_5m"],
              ">7.5m", a["share_beyond_7p5m"])
        print("   dist shares", a["landed_share_by_hit_distance_m"])
        print("   still_frac", a["still_frac_by_band"], "steps", a["body_steps_by_band"])
