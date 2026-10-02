"""Tabulate the arms and grade the pre-registration (b816e68e4). usage: python3 rj_pack.py <out_dir_with_arm_json> <results.json>"""
import json
import math
import os
import statistics as st
import sys

ARMS = ["CTRL", "RJ-RFA", "RJ-SLOT", "RJ-CROWD", "RJ-PERSIST", "RJ-CORE", "RJ-FULL"]
REF = {"standing": 0.34, "closing": 0.92, "w152": 16.3, "w155": 16.2}


def t95(xs):
    n = len(xs)
    if n < 2:
        return None
    m = st.mean(xs)
    s = st.stdev(xs)
    tc = {19: 2.093, 4: 2.776}.get(n - 1, 2.0)
    return [round(m - tc * s / math.sqrt(n), 4), round(m + tc * s / math.sqrt(n), 4)]


def row(d):
    s = d["summary"]
    ins = s["instruments"]
    steps = ins["body_steps_by_band"]
    sf = ins["still_frac_by_H2_band_151_160"]
    inside = sum(sf[i] * steps[i] for i in range(4) if sf[i] is not None) / max(1, sum(steps[:4]))
    term = s["leg_a_terminals"]
    hist = {}
    for t in term:
        hist[str(t)] = hist.get(str(t), 0) + 1
    pc = ins.get("pilot_closing") or {}
    tel = d["rj_tel"]
    n = len(d["salts"])
    return {
        "ratio": s["ratio_vs_referent"], "per_salt": s["per_salt_ratio"],
        "first_death_waves": hist, "first_death_t_into_wave_s": s["leg_a_t_into_wave_s"],
        "w152_s": s["per_wave"]["152"]["mean_t_s"], "w155_s": s["per_wave"]["155"]["mean_t_s"],
        "wave_s": {w: v["mean_t_s"] for w, v in s["per_wave"].items()},
        "wave_ratio": {w: v["ratio"] for w, v in s["per_wave"].items()},
        "standing_step_2p46_4p92": ins["still_frac_2p46_4p92m"],
        "standing_step_by_band": sf, "body_steps_by_band": steps,
        "standing_step_inside_2p46": round(inside, 4),
        "standing_net_2p46_4p92": d["rj_modes"]["net_still_2p46_4p92"],
        "standing_net_by_band": d["rj_modes"]["net_still_frac_by_band"],
        "mode_share_2p46_4p92": d["rj_modes"]["mode_share_2p46_4p92"],
        "closing_empty_m_s": (pc.get("empty") or {}).get("mean_closing_nearest_m_s"),
        "disc_empty_fraction": pc.get("disc_empty_fraction"),
        "disc_151_159": ins["disc_occupancy_mean_bodies_per_tick_151_159"],
        "disc_by_wave": ins["disc_occupancy_by_wave"],
        "tel_per_salt": {k: round(v / n, 2) for k, v in tel.items()},
    }


def grade(R):
    F, C = R["RJ-FULL"], R["RJ-CORE"]
    c = R["CTRL"]
    g = []

    def iv(name, val, lo, hi):
        g.append({"q": name, "value": val, "interval": [lo, hi],
                  "grade": "HIT" if (val is not None and lo <= val <= hi) else "MISS"})
    iv("Q1 standing step 2.46-4.92 (RJ-FULL)", F["standing_step_2p46_4p92"], 0.38, 0.52)
    iv("Q1b standing step 2.46-4.92 (RJ-CORE)", C["standing_step_2p46_4p92"], 0.36, 0.50)
    iv("Q2 standing net 2.46-4.92", F["standing_net_2p46_4p92"], 0.50, 0.70)
    iv("Q3 w152 mean duration s", F["w152_s"], 22, 34)
    iv("Q4 w155 mean duration s", F["w155_s"], 18, 30)
    fw = F["first_death_waves"]
    n152, n160 = fw.get("152", 0), fw.get("160", 0)
    other = sum(v for k, v in fw.items() if k not in ("152", "160", "None"))   # survivors are not deaths
    g.append({"q": "Q5 first deaths: w152 4-12, w160 4-12, >=1 outside {152,160}", "value": fw,
              "grade": "HIT" if (4 <= n152 <= 12 and 4 <= n160 <= 12 and other >= 1) else "MISS",
              "parts": {"w152": [n152, 4 <= n152 <= 12], "w160": [n160, 4 <= n160 <= 12], "other": [other, other >= 1]}})
    iv("Q6 ratio (RJ-FULL)", F["ratio"], 1.50, 2.25)
    iv("Q6 ratio (RJ-CORE)", C["ratio"], 1.50, 2.25)
    iv("Q7 closing empty disc m/s", F["closing_empty_m_s"], 0.70, 1.10)
    iv("Q8 disc occupancy 151-159", F["disc_151_159"], 1.8, 2.8)
    iv("Q9 standing step inside 2.46", F["standing_step_inside_2p46"], 0.80, 0.97)
    dec = {"RJ-RFA": ((-0.04, -0.005), (-6, 0)), "RJ-SLOT": ((-0.18, -0.05), (-30, -3)),
           "RJ-CROWD": ((-0.02, 0.02), (-4, 4)), "RJ-PERSIST": ((0.0, 0.03), (-4, 4))}
    for a, ((slo, shi), (rlo, rhi)) in dec.items():
        ds = round(R[a]["standing_step_2p46_4p92"] - c["standing_step_2p46_4p92"], 4)
        dr = round(100 * (R[a]["ratio"] / c["ratio"] - 1), 2)
        g.append({"q": f"Q10 {a} d-standing", "value": ds, "interval": [slo, shi],
                  "grade": "HIT" if slo <= ds <= shi else "MISS"})
        g.append({"q": f"Q10 {a} d-ratio %", "value": dr, "interval": [rlo, rhi],
                  "grade": "HIT" if rlo <= dr <= rhi else "MISS"})
    gap = round(F["standing_step_2p46_4p92"] - REF["standing"], 4)
    g.append({"q": "Q11a RJ-FULL standing above 0.34 by +0.04..+0.18", "value": gap, "interval": [0.04, 0.18],
              "grade": "HIT" if 0.04 <= gap <= 0.18 else "MISS"})
    g.append({"q": "Q11b w152 and w155 longer than 16.3 / 16.2 s", "value": [F["w152_s"], F["w155_s"]],
              "grade": "HIT" if F["w152_s"] > REF["w152"] and F["w155_s"] > REF["w155"] else "MISS"})
    tp = F["tel_per_salt"]
    iv("Q12 attack-RFAs per salt", tp.get("rfa_attack", 0.0), 6, 20)
    iv("Q12 WaitToAttack entries per salt", tp.get("wta_entries", 0.0), 100, 300)
    iv("Q12 LostSlot per salt", tp.get("lost_slot", 0.0), 60, 250)
    return g


def main():
    d0, outp = sys.argv[1], sys.argv[2]
    R, raw = {}, {}
    for a in ARMS:
        p = os.path.join(d0, f"arm_{a}.json")
        if not os.path.exists(p):
            continue
        raw[a] = json.load(open(p))
        R[a] = row(raw[a])
    c = R["CTRL"]
    for a in R:
        dr = [x - y for x, y in zip(R[a]["per_salt"], c["per_salt"])]
        R[a]["paired_d_ratio_vs_ctrl"] = {"mean": round(st.mean(dr), 4), "t95": t95(dr)}
    out = {"artifact_class": "NOT-A-GRADED-RUN — legolas reposition/jostle counterfactual (v3.9 oracle, seed-9, "
                             "salts 0-19); graded against PREREGISTRATION.md (b816e68e4)",
           "referent": REF, "arms": R}
    if all(a in R for a in ("CTRL", "RJ-FULL", "RJ-CORE", "RJ-RFA", "RJ-SLOT", "RJ-CROWD", "RJ-PERSIST")):
        out["grading"] = grade(R)
        out["score"] = {"HIT": sum(1 for x in out["grading"] if x["grade"] == "HIT"),
                        "MISS": sum(1 for x in out["grading"] if x["grade"] == "MISS")}
    json.dump(out, open(outp, "w"), indent=1)
    for a in R:
        r = R[a]
        print(f"{a:11s} x{r['ratio']:.4f} d={r['paired_d_ratio_vs_ctrl']} deaths={r['first_death_waves']} "
              f"w152={r['w152_s']} w155={r['w155_s']} stand={r['standing_step_2p46_4p92']} "
              f"net={r['standing_net_2p46_4p92']} in={r['standing_step_inside_2p46']} "
              f"close={r['closing_empty_m_s']} disc={r['disc_151_159']}")
    if "grading" in out:
        for x in out["grading"]:
            print(x["grade"], x["q"], x["value"], x.get("interval"))
        print(out["score"])


if __name__ == "__main__":
    main()
