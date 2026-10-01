"""legolas 2026-10-01 -- p05 spawn-position counterfactual. NOT-A-GRADED-RUN. READ-ONLY.
Imports gamora's C-11a fold-pricing harness (PW-FOLDED = the x3.17 oracle state, v1.8 seat cell)
and C-11's per-wave capture, unmodified on disk. In-process only: (1) wraps c11._capture to add a
per-spawn-point landed-damage census; (2) per arm, wraps CitedArenaGeometry.emitter_xy so that
spawn point 5 returns an override position. Nothing on disk in the engine is written.
"""
import json, math, sys, time, hashlib
from collections import defaultdict
from reincarnated.simulation.scripts import gamora_kc2_play_c11a_fold_pricing_2026_09_30 as FP
from reincarnated.simulation.scripts import gamora_kc2_c11_lethality_decomposition_2026_09_29 as c11
from reincarnated.simulation.kc2 import locomotion as lo

REF = 1605.6
W9 = set(range(151, 160))
ARMS = {
    "PACK": None,                               # pack/oracle as shipped: p05 = (-6.821, 2.175), r 7.16 m
    "TRUE-A": (-8.245, -5.824),                 # sm1/survivalworld_a spawnpoint05, v3 labels, r 10.10 m
    "TRUE-E": (0.112, -0.009),                  # sm1/survivalworld_e spawnpoint05, r 0.11 m (nearest candidate)
    "RING-33": (-33.0*math.cos(math.radians(17.69)), 33.0*math.sin(math.radians(17.69))),  # NOT GD: p05 pushed to ring radius on its pack bearing
}
base_cap = c11._capture
def cap(r):
    out = base_cap(r)
    w = r.waves[0]; t0 = float(w["t_start_s"])
    actors = {a["actor_id"]: a for a in r.actors}
    by_sp = defaultdict(float); by_sp10 = defaultdict(float); first_hit = {}
    for x in r.rows_as_dicts():
        if x["event_type"] not in ("damage_dealt", "dot_tick") or x["target_id"] != "player":
            continue
        a = float(x["damage_applied"] or 0.0)
        if a <= 0: continue
        sid = x["source_id"]; act = actors.get(sid)
        sp = act["spawn_point_id"] if act else "summon/other"
        t = float(x["t_s"]) - t0
        by_sp[sp] += a
        if t < 10.0: by_sp10[sp] += a
        first_hit[sp] = min(first_hit.get(sp, 1e9), t)
    n_sp = defaultdict(int); xy = defaultdict(list)
    for a in r.actors:
        n_sp[a.get("spawn_point_id")] += 1
        if a.get("spawn_point_id") == "p05": xy["p05"].append((a["spawn_x"], a["spawn_y"], a.get("spawn_t_s")))
    out["by_sp"] = dict(by_sp); out["by_sp_first10s"] = dict(by_sp10)
    out["first_hit_t_by_sp"] = {k: round(v, 3) for k, v in first_hit.items()}
    out["n_bodies_by_sp"] = dict(n_sp)
    if xy["p05"]:
        out["p05_spawn_centroid"] = (round(sum(p[0] for p in xy["p05"])/len(xy["p05"]), 2),
                                     round(sum(p[1] for p in xy["p05"])/len(xy["p05"]), 2))
        out["p05_spawn_t"] = sorted({round(float(p[2] or 0), 3) for p in xy["p05"]})
    return out
c11._capture = cap

real_exy = lo.CitedArenaGeometry.emitter_xy
def run(arm, salts, period):
    ov = ARMS[arm]
    def exy(self, spawn_point, tier=None):
        if ov is not None and int(spawn_point) == 5:
            return ov
        return real_exy(self, spawn_point, tier)
    lo.CitedArenaGeometry.emitter_xy = exy
    try:
        return FP.run_arm("PW-FOLDED", salts, period)
    finally:
        lo.CitedArenaGeometry.emitter_xy = real_exy

def summarise(res, salts):
    rows = [r for s in salts for r in res["salts"][str(s)]["rows"] if r["wave"] in W9]
    T = sum(r["t_s"] for r in rows); L = sum(r["landed"] for r in rows)
    sp = defaultdict(float); n = defaultdict(int)
    for r in rows:
        for k, v in r["by_sp"].items(): sp[k] += v
        for k, v in r["n_bodies_by_sp"].items(): n[k] += v
    per_wave = defaultdict(lambda: {"t": 0.0, "L": 0.0, "L_p05": 0.0, "L10": 0.0, "L10_p05": 0.0, "n": 0})
    for r in rows:
        pw = per_wave[r["wave"]]; pw["t"] += r["t_s"]; pw["L"] += r["landed"]; pw["n"] += 1
        pw["L_p05"] += r["by_sp"].get("p05", 0.0)
        pw["L10"] += sum(r["by_sp_first10s"].values()); pw["L10_p05"] += r["by_sp_first10s"].get("p05", 0.0)
    deaths = [res["salts"][str(s)]["leg_a_terminal"] for s in salts]
    return {"salts": list(salts), "landed_hp_per_s_151_159": round(L/T, 1), "ratio_vs_referent": round(L/T/REF, 3),
            "t_s": round(T, 2), "landed_share_by_sp": {k: round(v/L, 4) for k, v in sorted(sp.items())},
            "bodies_by_sp": dict(sorted(n.items(), key=lambda kv: str(kv[0]))),
            "leg_a_terminals": deaths,
            "mean_death_wave": round(sum(d["wave"] for d in deaths if d.get("wave"))/max(1, sum(1 for d in deaths if d.get("wave"))), 2),
            "per_wave": {w: {"n_salt_rows": v["n"], "landed_hp_per_s": round(v["L"]/v["t"], 1) if v["t"] else None,
                              "p05_share_of_landed": round(v["L_p05"]/v["L"], 4) if v["L"] else None,
                              "first10s_p05_share": round(v["L10_p05"]/v["L10"], 4) if v["L10"] else None}
                         for w, v in sorted(per_wave.items())}}

if __name__ == "__main__":
    salts = tuple(range(int(sys.argv[1]))) if len(sys.argv) > 1 else (0, 1, 2, 3, 4)
    arms = sys.argv[2].split(",") if len(sys.argv) > 2 else list(ARMS)
    period = FP._period()
    out = {"artifact_class": "NOT-A-GRADED-RUN. legolas diagnostic counterfactual. Engine read-only; in-process wraps only.",
           "harness": "gamora_kc2_play_c11a_fold_pricing_2026_09_30.run_arm('PW-FOLDED') + c11._capture",
           "control": {"expect_landed_hp_per_s_salts_0_4": 5090.3, "expect_ratio": 3.17,
                       "expect_terminals_salts_0_4": [[156, 7.184], [152, 4.408], [155, 7.02], [152, 7.184], [152, 6.122]]},
           "referent_intake_hp_per_s_151_159": REF, "tick_period_s": period, "arms_xy_p05": ARMS, "results": {}, "raw_p05_meta": {}}
    t0 = time.time()
    for a in arms:
        res = run(a, salts, period)
        out["results"][a] = summarise(res, salts)
        if len(salts) > 5: out["results"][a + "@salts0-4"] = summarise(res, tuple(s for s in salts if s < 5))
        out["raw_p05_meta"][a] = sorted({(r["wave"], str(r.get("p05_spawn_centroid")), str(r.get("p05_spawn_t")))
                                         for s in salts for r in res["salts"][str(s)]["rows"] if r.get("p05_spawn_centroid")})[:12]
        print(a, json.dumps({k: out["results"][a][k] for k in ("landed_hp_per_s_151_159", "ratio_vs_referent", "mean_death_wave", "landed_share_by_sp")}), file=sys.stderr, flush=True)
    out["wall_s"] = round(time.time() - t0, 1)
    p = sys.argv[3] if len(sys.argv) > 3 else "p05_counterfactual_out.json"
    json.dump(out, open(p, "w"), indent=1, default=str)
    print("wrote", p, file=sys.stderr)
