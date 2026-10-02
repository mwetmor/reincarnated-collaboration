"""Tabulate the v3.11 pass-4 runs and grade them against PREREGISTRATION.md (committed alone before the runs).

usage: python3 grade_pass4.py      (reads pw_*.json + graded_V311-FULL.json beside it; writes tabulated_pw.json +
prereg_grading.json)
"""
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WAVES = [str(w) for w in range(151, 161)]


def row(s):
    i4 = s["instruments311"]
    hist = {}
    for t in s["leg_a_terminals"]:
        hist[str(t)] = hist.get(str(t), 0) + 1
    t160 = i4["time_into_w160"]
    d = [w for w in WAVES[:-1] if s["per_wave"].get(w)]
    return {
        "ratio": s["ratio_vs_referent"], "per_salt": s["per_salt_ratio"], "raised": s["raised"],
        "first_death_waves": hist, "first_death_t_into_wave_s": s["leg_a_t_into_wave_s"],
        "wave_s": {w: v["mean_t_s"] for w, v in s["per_wave"].items()},
        "deaths_by_wave": {w: v["deaths"] for w, v in s["per_wave"].items()},
        "mean_wave_s_151_159": round(sum(s["per_wave"][w]["mean_t_s"] for w in d) / len(d), 2),
        "own_wave_ratio": i4["own_wave_ratio_vs_referent_rate"],
        "w160_n_die": t160["n_died_in_w160"], "w160_mean_t_death_s": t160["mean_t_first_death_in_w160_s"],
        "summon_check": i4["summon_check"],
    }


def main():
    R, FR = {}, {}
    for p in sorted(glob.glob(os.path.join(HERE, "pw_*.json"))):
        d = json.load(open(p))
        for c, v in d["results"].items():
            R[c] = row(v["all"])
            FR[c] = {k: v["fold_reports"].get(k) for k in ("lineup", "mutators")}
    g = []

    def iv(q, val, lo, hi):
        ok = val is not None and lo <= val <= hi
        g.append({"q": q, "value": val, "interval": [lo, hi], "grade": "HIT" if ok else "MISS"})
        return ok

    def cond(q, val, ok):
        g.append({"q": q, "value": val, "grade": "HIT" if ok else "MISS"})

    if "V310-FULL" in R:
        g.append({"q": "control replica ratio", "value": R["V310-FULL"]["ratio"], "known": 1.847,
                  "grade": "REPLICA-EXACT" if abs(R["V310-FULL"]["ratio"] - 1.847) < 5e-4 else "REPLICA-FAILED"})
    fd = lambda r, w: r["first_death_waves"].get(w, 0)
    late = lambda r: sum(v for k, v in r["first_death_waves"].items() if k == "None" or int(k) >= 156)
    if "LU" in R:
        r = R["LU"]
        iv("P1 LU ratio", r["ratio"], 1.15, 1.65)
        cond("P1 LU first deaths (w152<=3, w154<=8, >=8 at w156+ or none, 0-8 none)", r["first_death_waves"],
             fd(r, "152") <= 3 and fd(r, "154") <= 8 and late(r) >= 8 and 0 <= fd(r, "None") <= 8)
        iv("P1 LU w152 s", r["wave_s"]["152"], 22, 45)
        iv("P1 LU w155 s", r["wave_s"]["155"], 14, 28)
        cond("P1 LU w160 (8-20 die; mean t 5-25 s)", [r["w160_n_die"], r["w160_mean_t_death_s"]],
             8 <= r["w160_n_die"] <= 20 and r["w160_mean_t_death_s"] is not None
             and 5 <= r["w160_mean_t_death_s"] <= 25)
    if "MUT" in R:
        r = R["MUT"]
        iv("P2 MUT ratio", r["ratio"], 1.88, 2.15)
        cond("P2 MUT first deaths (w152 8-16; none survive)", r["first_death_waves"],
             8 <= fd(r, "152") <= 16 and fd(r, "None") == 0)
        iv("P2 MUT w152 s", r["wave_s"]["152"], 40, 55)
        iv("P2 MUT w155 s", r["wave_s"]["155"], 19, 27)
        cond("P2 MUT w160 (14-20 die; mean t 3-17 s)", [r["w160_n_die"], r["w160_mean_t_death_s"]],
             14 <= r["w160_n_die"] <= 20 and r["w160_mean_t_death_s"] is not None
             and 3 <= r["w160_mean_t_death_s"] <= 17)
    if "V311-FULL" in R:
        r = R["V311-FULL"]
        iv("P3 V311-FULL ratio", r["ratio"], 1.20, 1.85)
        cond("P3 V311-FULL first deaths (w152<=5; >=6 at w156+ or none; 0-6 none)", r["first_death_waves"],
             fd(r, "152") <= 5 and late(r) >= 6 and 0 <= fd(r, "None") <= 6)
        iv("P3 V311-FULL w152 s", r["wave_s"]["152"], 25, 50)
        iv("P3 V311-FULL w155 s", r["wave_s"]["155"], 15, 30)
        cond("P3 V311-FULL w160 (10-20 die; mean t 4-22 s)", [r["w160_n_die"], r["w160_mean_t_death_s"]],
             10 <= r["w160_n_die"] <= 20 and r["w160_mean_t_death_s"] is not None
             and 4 <= r["w160_mean_t_death_s"] <= 22)
    P4 = {"151": (1.0, 2.0), "152": (1.5, 3.5), "153": (0.7, 1.6), "154": (1.2, 2.2), "155": (1.2, 2.2),
          "156": (1.0, 2.0), "157": (0.3, 1.0), "158": (1.2, 3.0), "159": (1.0, 2.2), "160": (0.9, 2.0)}
    if "LU" in R:
        hits = {w: P4[w][0] <= (R["LU"]["own_wave_ratio"][w] or -1) <= P4[w][1] for w in WAVES}
        cond("P4 LU per-wave own ratio (>=7/10)", {w: [R["LU"]["own_wave_ratio"][w], hits[w]] for w in WAVES},
             sum(hits.values()) >= 7)
    if "MUT" in R and "V310-FULL" in R:
        f = {w: round(R["MUT"]["own_wave_ratio"][w] / R["V310-FULL"]["own_wave_ratio"][w], 3) for w in WAVES}
        cond("P5 MUT per-wave x control in 0.95-1.20 (>=7/10)", f, sum(0.95 <= v <= 1.20 for v in f.values()) >= 7)
    if "V311-FULL" in R and "LU" in R:
        f = {w: round(R["V311-FULL"]["own_wave_ratio"][w] / R["LU"]["own_wave_ratio"][w], 3) for w in WAVES}
        cond("P6 V311 per-wave x LU in 0.95-1.25 (>=7/10)", f, sum(0.95 <= v <= 1.25 for v in f.values()) >= 7)
    if "LU-BC" in R and "LU" in R:
        cond("P7 LU-BC > LU", [R["LU-BC"]["ratio"], R["LU"]["ratio"]], R["LU-BC"]["ratio"] > R["LU"]["ratio"])
    if "LU-RA" in R and "LU" in R:
        cond("P8 LU-RA < LU", [R["LU-RA"]["ratio"], R["LU"]["ratio"]], R["LU-RA"]["ratio"] < R["LU"]["ratio"])
    if all(k in R for k in ("LU-LEECH", "LU-CRUEL", "LU")):
        v = [R["LU-LEECH"]["mean_wave_s_151_159"], R["LU-CRUEL"]["mean_wave_s_151_159"], R["LU"]["mean_wave_s_151_159"]]
        cond("P9 LU-LEECH and LU-CRUEL mean duration > LU", v, v[0] > v[2] and v[1] > v[2])
    if "V311-ASCX" in R and "V311-FULL" in R:
        a, b = R["V311-ASCX"], R["V311-FULL"]
        cond("P10 V311-ASCX within +-3 % and duration <=", [a["ratio"], b["ratio"], a["mean_wave_s_151_159"],
                                                          b["mean_wave_s_151_159"]],
             abs(a["ratio"] / b["ratio"] - 1) <= 0.03 and a["mean_wave_s_151_159"] <= b["mean_wave_s_151_159"])
    if "LU-UNK" in R and "LU" in R:
        cond("P11 LU-UNK within +-6 % of LU", [R["LU-UNK"]["ratio"], R["LU"]["ratio"]],
             abs(R["LU-UNK"]["ratio"] / R["LU"]["ratio"] - 1) <= 0.06)
    if "V311-FULL" in R:
        sc = R["V311-FULL"]["summon_check"]
        n_ref = sum(len(v["referent"]) for v in sc.values())
        n_got = sum(len(v["referent_identities_present"]) for v in sc.values())
        cond("P12 oracle produces fewer referent summon identities than the referent (SEEN-informed)",
             [n_got, n_ref], n_got < n_ref)
    gp = os.path.join(HERE, "graded_V311-FULL.json")
    G = {}
    if os.path.exists(gp):
        d = json.load(open(gp))
        for arm, v in d["results"].items():
            s = v["all"]
            G[arm] = {"ratio": s["ratio_vs_referent"], "terminals": s["leg_a_terminals"],
                      "t_into_wave": s["leg_a_t_into_wave_s"], "leg_b_deaths_per_salt": s["leg_b_deaths_per_salt"]}
        if len(G) == 5:
            rs = [x["ratio"] for x in G.values()]
            mid = sum(rs) / len(rs)
            cond("G1 five arms within +-10 %", rs, all(abs(x / mid - 1) <= 0.10 for x in rs))
            n152 = sum(1 for x in G.values() for t in x["terminals"] if t == 152)
            cond("G2 <= 5 of 25 cells first die in w152", n152, n152 <= 5)
    json.dump({"pw": R, "fold_reports": FR, "graded": G}, open(os.path.join(HERE, "tabulated_pw.json"), "w"), indent=1)
    json.dump({"grading": g, "n_hit": sum(x["grade"] == "HIT" for x in g),
               "n_miss": sum(x["grade"] == "MISS" for x in g)},
              open(os.path.join(HERE, "prereg_grading.json"), "w"), indent=1)
    for x in g:
        print(x["grade"], x["q"], x.get("value"))


if __name__ == "__main__":
    main()
