"""Tabulate the v3.10 pass-3 runs and grade them against PREREGISTRATION.md (committed alone before the runs).

usage: python3 grade_pass3.py      (reads pw_*.json beside it; writes tabulated_pw.json + prereg_grading.json)
"""
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def row(s):
    ins, i3 = s["instruments"], s["instruments310"]
    steps, sf = ins["body_steps_by_band"], ins["still_frac_by_H2_band_151_160"]
    hist = {}
    for t in s["leg_a_terminals"]:
        hist[str(t)] = hist.get(str(t), 0) + 1
    pc = ins.get("pilot_closing") or {}
    return {
        "ratio": s["ratio_vs_referent"], "per_salt": s["per_salt_ratio"], "raised": s["raised"],
        "first_death_waves": hist, "first_death_t_into_wave_s": s["leg_a_t_into_wave_s"],
        "w152_s": s["per_wave"]["152"]["mean_t_s"], "w155_s": s["per_wave"]["155"]["mean_t_s"],
        "wave_s": {w: v["mean_t_s"] for w, v in s["per_wave"].items()},
        "wave_ratio": {w: v["ratio"] for w, v in s["per_wave"].items()},
        "standing_step_2p46_4p92": ins["still_frac_2p46_4p92m"], "standing_step_by_band": sf,
        "standing_step_inside_2p46": round(sum(sf[i] * steps[i] for i in range(4) if sf[i] is not None)
                                           / max(1, sum(steps[:4])), 4),
        "standing_net_2p46_4p92": i3["net_still_2p46_4p92"], "standing_net_by_band": i3["net_still_frac_by_band"],
        "mode_share_2p46_4p92": i3["mode_share_2p46_4p92"],
        "closing_empty_m_s": (pc.get("empty") or {}).get("mean_closing_nearest_m_s"),
        "closing_occupied_m_s": (pc.get("occupied") or {}).get("mean_closing_nearest_m_s"),
        "disc_empty_fraction": pc.get("disc_empty_fraction"),
        "disc_151_159": ins["disc_occupancy_mean_bodies_per_tick_151_159"],
        "pilot_realised": i3["pilot_realised"],
    }


def main():
    R, FR = {}, {}
    for p in sorted(glob.glob(os.path.join(HERE, "pw_*.json"))):
        d = json.load(open(p))
        for c, v in d["results"].items():
            R[c] = row(v["all"])
            FR[c] = v["fold_reports"]
    g = []

    def iv(q, val, lo, hi):
        ok = val is not None and lo <= val <= hi
        g.append({"q": q, "value": val, "interval": [lo, hi], "grade": "HIT" if ok else "MISS"})
        return ok

    def known(q, val, want, tol=0.0005):
        g.append({"q": q, "value": val, "known": want,
                  "grade": "REPLICA-EXACT" if abs(val - want) <= tol else "REPLICA-FAILED"})

    if "F1-PERSIST" in R:
        f = R["F1-PERSIST"]
        known("P1 F1 ratio", f["ratio"], 2.2808)
        known("P1 F1 standing step", f["standing_step_2p46_4p92"], 0.586)
        known("P1 F1 w152", f["w152_s"], 35.4, 0.05)
    if "F3-RFA" in R:
        f = R["F3-RFA"]
        known("P3 F3 ratio", f["ratio"], 2.381)
        known("P3 F3 w155", f["w155_s"], 22.8, 0.05)
    if "R-SLOT" in R:
        known("replica R-SLOT ratio", R["R-SLOT"]["ratio"], 1.9937)
    if "R-FULL" in R:
        known("replica R-FULL ratio", R["R-FULL"]["ratio"], 2.168)
        known("replica R-FULL standing step", R["R-FULL"]["standing_step_2p46_4p92"], 0.570)
        known("replica R-FULL standing net", R["R-FULL"]["standing_net_2p46_4p92"], 0.595)
    if "V39-FULL" in R:
        known("control ratio", R["V39-FULL"]["ratio"], 2.3037)
        known("control standing step", R["V39-FULL"]["standing_step_2p46_4p92"], 0.575)
        known("control standing net", R["V39-FULL"]["standing_net_2p46_4p92"], 0.479)

    def fd(r):
        h = r["first_death_waves"]
        return h.get("152", 0), h.get("160", 0), h.get("None", 0)

    def block(tag, c, rat, n152, surv, w152, w155, st, nt, cl):
        if c not in R:
            return
        r = R[c]
        iv(f"{tag} {c} ratio", r["ratio"], *rat)
        a, b, s = fd(r)
        if n152 is not None:
            iv(f"{tag} {c} first deaths w152", a, *n152)
        if surv is not None:
            iv(f"{tag} {c} survivors", s, *surv)
        iv(f"{tag} {c} w152 s", r["w152_s"], *w152)
        iv(f"{tag} {c} w155 s", r["w155_s"], *w155)
        iv(f"{tag} {c} standing step", r["standing_step_2p46_4p92"], *st)
        iv(f"{tag} {c} standing net", r["standing_net_2p46_4p92"], *nt)
        iv(f"{tag} {c} closing empty", r["closing_empty_m_s"], *cl)

    block("P2", "F2-SLOT", (1.80, 2.07), (7, 14), (3, 20), (35, 47), (24, 32), (0.51, 0.57), (0.43, 0.50), (0.85, 1.15))
    block("P4", "F24-SLOT-CROWD", (1.85, 2.21), (6, 14), (2, 20), (38, 56), (20, 31), (0.53, 0.61), (0.52, 0.68),
          (0.95, 1.30))
    block("P5", "F5-MOVE", (2.30, 2.65), (14, 20), None, (22, 34), (18, 28), (0.50, 0.61), (0.42, 0.56), (0.85, 1.20))
    block("P6", "V310-NOMOVE", (2.00, 2.25), (6, 13), (1, 7), (44, 62), (18, 26), (0.54, 0.60), (0.55, 0.65),
          (0.85, 1.15))
    if "V310-NOMOVE" in R:
        iv("P6 V310-NOMOVE first deaths w160", fd(R["V310-NOMOVE"])[1], 3, 9)
    block("P7", "V310-FULL", (2.05, 2.45), (6, 15), (0, 6), (33, 55), (17, 26), (0.50, 0.60), (0.50, 0.65),
          (0.85, 1.20))
    if "V310-FULL" in R:
        F = R["V310-FULL"]
        iv("P7 V310-FULL first deaths w160", fd(F)[1], 2, 9)
        iv("P9 standing step above 0.34 by", round(F["standing_step_2p46_4p92"] - 0.34, 4), 0.16, 0.26)
        iv("P9 standing net above 0.34 by", round(F["standing_net_2p46_4p92"] - 0.34, 4), 0.16, 0.31)
        iv("P10 pilot moving fraction", F["pilot_realised"]["moving_fraction_over_0p49_m_s"], 0.74, 0.88)
        iv("P10 pilot mean speed", F["pilot_realised"]["mean_speed_all_ticks_m_s"], 2.3, 3.1)
        iv("P11 closing occupied", F["closing_occupied_m_s"], -0.40, 0.40)
        iv("P12 disc 151-159", F["disc_151_159"], 1.8, 2.8)
        g.append({"q": "P13 w152 and w155 longer than 16.3 / 16.2", "value": [F["w152_s"], F["w155_s"]],
                  "grade": "HIT" if F["w152_s"] > 16.3 and F["w155_s"] > 16.2 else "MISS"})
    if "F1-LAND" in R and "F1-PERSIST" in R:
        L, P = R["F1-LAND"], R["F1-PERSIST"]
        iv("P8 F1-LAND ratio rel F1 (%)", round(100 * (L["ratio"] / P["ratio"] - 1), 2), -2, 2)
    gp = os.path.join(HERE, "graded_V310-FULL.json")
    if os.path.exists(gp):
        G = json.load(open(gp))["results"]
        rat = {a: v["all"]["ratio_vs_referent"] for a, v in G.items()}
        term = {a: v["all"]["leg_a_terminals"] for a, v in G.items()}
        span = max(rat.values()) / min(rat.values())
        g.append({"q": "G1 five graded arms within +/-10 % of each other", "value": rat,
                  "grade": "HIT" if span <= 1.10 else "MISS"})
        n152 = sum(1 for a in term if 152 in term[a])
        g.append({"q": "G2 a w152 first death in >= 3 of 5 arms", "value": term,
                  "grade": "HIT" if n152 >= 3 else "MISS"})
    n = {k: sum(1 for x in g if x["grade"] == k) for k in ("HIT", "MISS", "REPLICA-EXACT", "REPLICA-FAILED")}
    json.dump({"rows": R}, open(os.path.join(HERE, "tabulated_pw.json"), "w"), indent=1)
    json.dump({"grading": g, "counts": n}, open(os.path.join(HERE, "prereg_grading.json"), "w"), indent=1)
    for x in g:
        print(f"{x['grade']:15s} {x['q']:45s} {x['value']}  {x.get('interval', x.get('known'))}")
    print(n)


if __name__ == "__main__":
    main()
