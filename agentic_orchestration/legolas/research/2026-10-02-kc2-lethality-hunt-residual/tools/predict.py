"""PRE-REGISTRATION calculator (run BEFORE any counterfactual of the decoded AI rule).

Inputs: the decoded rule (Game.dll Ed IV, this leg + D-3 + D-11), DATAMINED per-record values
(swing pause, Ed II; GD fire ranges, pack v3.8 CSV), the oracle's own swing periods / tick clock,
and the CONTROL run's attribution (landed by record / skill per wave). No counterfactual output
is read. Writes the numbers the prediction file quotes."""
import csv
import json
import math
import pickle
import sys
from collections import defaultdict
from statistics import median

H = ("/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/"
     "ac232ef8-034a-45e4-8e9f-65834cd599f9/scratchpad/hunt2")
TPS = 49 / 4          # oracle tick clock (period 4/49 s), read off the control run
ASPD = 1.11           # oracle's per-wave attack-speed multiplier at w151-170 (offense fold)
REF = 1605.6

sp = json.load(open(f"{H}/out/swing_pause_table.json"))["records"]
timing = {r["record"]: r for r in csv.DictReader(open(f"{H}/eng/data/kc2/pm2_tg2_monster_timing.csv"))}
fr = list(csv.DictReader(open(f"{H}/eng/data/kc2/kc2_gd_fire_range_v3p8.csv")))
slot_of_skill = {}
for r in fr:
    slot_of_skill[(r["record"].split("/")[-1], r["skill"].split("/")[-1])] = r["slot"]
basic_R = {r["record"]: float(r["gd_use_range_m_HI"]) for r in fr if r["slot"] == "basic" and r["gd_use_range_m_HI"]}
spec_R = defaultdict(list)
for r in fr:
    if r["slot"].startswith("special") and r["gd_use_range_m_HI"]:
        spec_R[r["record"]].append(float(r["gd_use_range_m_HI"]))


def cadence_factor(rec):
    """oracle cycle / GD cycle for one record's swings. Oracle: n ticks. GD: max(n, ceil(p*TPS))
    with p ~ U{min_ms..max_ms}/1000 (IGenerate, inclusive integers), averaged exactly."""
    t = timing.get(rec)
    s = sp.get(rec, {})
    if not t or not t.get("basic_swing_period_s") or s.get("minSwingPause") is None:
        return None
    per = float(t["basic_swing_period_s"])
    n = max(1, int(round(per / ASPD * TPS)))
    lo, hi = int(float(s["minSwingPause"]) * 1000), int(float(s["maxSwingPause"]) * 1000)
    if hi < lo:
        hi = lo
    tot = 0.0
    for ms in range(lo, hi + 1):
        tot += max(n, math.ceil(ms / 1000.0 * TPS - 1e-9))
    gd = tot / (hi - lo + 1)
    return n / gd


ctrl = json.load(open(f"{H}/out/CTRL.json"))
D = pickle.load(open(f"{H}/out/probe_s0.pkl", "rb"))
rec_by_short = {}
for w, d in D.items():
    for a in d["actors"]:
        rec_by_short[a["record_path"].split("/")[-1]] = a["record_path"]
    for p in d["wave"].get("pets") or []:
        rec_by_short[p["record_path"].split("/")[-1]] = p["record_path"]
pet_rec = {}
for w, d in D.items():
    for p in d["wave"].get("pets") or []:
        pet_rec[p["actor_id"]] = p["record_path"]

aura_skills = {r["skill"].split("/")[-1] for r in fr if r["slot"] == "initial"}

out = {"per_wave": {}, "per_record_factor": {}}
L_all = T_all = L_pred_all = 0.0
for w in range(151, 161):
    L = T = Lp = 0.0
    for s, rr in ctrl["rows"].items():
        for r in rr:
            if r["wave"] != w:
                continue
            T += r["t_s"]
            for k, v in r["ext"]["landed_by_skill"].items():
                pass
            # landed by record is complete; skill map is top-25 only -> use record grain,
            # removing aura-skill landed (not swing-gated) using the skill grain where listed
            aura_land = defaultdict(float)
            for k, v in r["ext"]["landed_by_skill"].items():
                rs, sk = k.split(":", 1)
                if sk in aura_skills:
                    aura_land[rs] += v
            for rs, v in r["ext"]["landed_by_record"].items():
                full = rec_by_short.get(rs) or pet_rec.get(rs)
                f = cadence_factor(full) if full else None
                a = aura_land.get(rs, 0.0)
                L += v
                Lp += a + (v - a) * (f if f is not None else 1.0)
    out["per_wave"][w] = {"ctrl_rate": round(L / T, 1), "pred_rate_SP_first_order": round(Lp / T, 1),
                          "mult": round(Lp / L, 4)}
    if w < 160:
        L_all += L; T_all += T; L_pred_all += Lp
out["ratio_ctrl"] = round(L_all / T_all / REF, 4)
out["ratio_pred_SP_first_order"] = round(L_pred_all / T_all / REF, 4)
for rs, full in sorted(rec_by_short.items()):
    f = cadence_factor(full)
    if f is not None:
        out["per_record_factor"][rs] = round(f, 4)

# standoff distribution over the fixed roster (actors, salt-invariant), waves 151-160
st = {"basic_R_by_wave": {}, "all": []}
for w, d in sorted(D.items()):
    Rs = [basic_R.get(a["record_path"]) for a in d["actors"]]
    Rs = [x for x in Rs if x is not None]
    st["basic_R_by_wave"][w] = {"n": len(Rs), "median": round(median(Rs), 2) if Rs else None,
                                "frac_gt_4m": round(sum(x > 4 for x in Rs) / len(Rs), 3) if Rs else None,
                                "frac_gt_8m": round(sum(x > 8 for x in Rs) / len(Rs), 3) if Rs else None,
                                "max": max(Rs) if Rs else None}
    st["all"] += Rs
A = st["all"]
st["pooled"] = {"n": len(A), "median": round(median(A), 2), "frac_gt_4m": round(sum(x > 4 for x in A) / len(A), 3),
                "frac_gt_8m": round(sum(x > 8 for x in A) / len(A), 3),
                "quantiles_10_50_90": [round(sorted(A)[int(q * (len(A) - 1))], 2) for q in (0.1, 0.5, 0.9)]}
spec_all = []
for w, d in sorted(D.items()):
    for a in d["actors"]:
        spec_all += spec_R.get(a["record_path"], [])
st["special_R_pooled"] = {"n": len(spec_all), "median": round(median(spec_all), 2),
                          "frac_gt_4m": round(sum(x > 4 for x in spec_all) / len(spec_all), 3)}
del st["all"]
out["standoff"] = st

# share of control landed by slot class (basic / special / other) - for the selection-order claim
cls = defaultdict(float)
tot = 0.0
for s, rr in ctrl["rows"].items():
    for r in rr:
        if r["wave"] > 159:
            continue
        for k, v in r["ext"]["landed_by_skill"].items():
            rs, sk = k.split(":", 1)
            sl = slot_of_skill.get((rs, sk))
            cls[(sl or "unmapped").rstrip("12345")] += v
            tot += v
out["ctrl_top25_landed_share_by_slot"] = {k: round(v / tot, 3) for k, v in sorted(cls.items(), key=lambda kv: -kv[1])}
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(json.dumps({k: out[k] for k in ("ratio_ctrl", "ratio_pred_SP_first_order")}))
print(json.dumps(out["per_wave"]))
print(json.dumps(out["standoff"]["pooled"]), json.dumps(out["standoff"]["special_R_pooled"]))
print(json.dumps(out["ctrl_top25_landed_share_by_slot"]))
