"""READ-ONLY OBS-1 retro-audit witness: re-run V311-FULL (pw salts 0-19 + the 5 graded arms, salts 0-4) through
V11.run_one UNMODIFIED, with an innermost observer on kr.simulate_wave that records each wave's RAW outcome before
upn4 rewrites a death-ended wave to 'cleared'. Compares the re-run summary to the committed artifact."""
import json, sys, time
from reincarnated.simulation.kc2 import run as kr
from reincarnated.simulation.scripts import gamora_kc2_c11_lethality_decomposition_2026_09_29 as c11
from reincarnated.simulation.scripts import gamora_kc2_play_c11a_fold_pricing_2026_09_30 as FP
from reincarnated.simulation.scripts import gamora_kc2_play_v3p8_oracle_2026_10_02 as V8
from reincarnated.simulation.scripts import gamora_kc2_play_v3p11_oracle_2026_10_02 as V11
P4 = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/analyses/2026-10-02-kc2-v3p11-oracle-pass4/"
period = FP._period()
cur = {"salt": None}
obs = {}
real_sw = kr.simulate_wave
real_ra = c11.run_arm
def ra(runner, arm, salt, per):
    cur["salt"] = salt
    obs.setdefault(salt, [])
    return real_ra(runner, arm, salt, per)
def ob(*a, **kw):
    r = real_sw(*a, **kw)
    w = r.waves[0]
    obs[cur["salt"]].append({"wave": int(w["wave"]), "outcome": w.get("outcome"), "term": w.get("termination_reason"),
                             "t_s": round(float(w["t_end_s"]) - float(w["t_start_s"]), 3)})
    return r
KEYS = ("ratio_vs_referent", "per_salt_ratio", "leg_a_terminals", "leg_b_death_waves", "t_s_151_159", "n_survive_160")
def one(arm, salts, ref):
    obs.clear()
    kr.simulate_wave = ob; c11.run_arm = ra
    try:
        res = V11.run_one("V311-FULL", salts, period, arm=arm)
    finally:
        kr.simulate_wave = real_sw; c11.run_arm = real_ra
    s = V11.summarise(res, salts)
    match = {k: s[k] == ref[k] for k in KEYS}
    per = {}
    for sl in salts:
        seat = [x for x in obs[sl] if 151 <= x["wave"] <= 160]
        waves = [x["wave"] for x in seat]
        w160 = next((x for x in seat if x["wave"] == 160), None)
        rows = res["salts"][str(sl)]["rows"]
        per[sl] = {"n_seat_calls": len(seat), "waves_151_160_complete": waves == list(range(151, 161)),
                   "n_rows_banked": len([r for r in rows if 151 <= r["wave"] <= 160]),
                   "non_clear_non_death": [x for x in seat if x["outcome"] not in ("cleared", "player_death")],
                   "w160_outcome": None if w160 is None else w160["outcome"], "w160_t_s": None if w160 is None else w160["t_s"],
                   "leg_a_terminal": s["leg_a_terminals"][salts.index(sl)]}
    return {"arm": arm, "salts": list(salts), "summary_matches_artifact": match, "per_salt": per}
out = {"artifact_class": "NOT-A-GRADED-RUN — OBS-1 retro-audit witness (read-only re-run, oracle unmodified)", "runs": []}
t0 = time.time()
pw = json.load(open(P4 + "pw_A.json"))["results"]["V311-FULL"]["all"]
out["runs"].append(dict(one("M-POL-2", tuple(range(20)), pw), source="pw_A.json:V311-FULL"))
print(f"[{time.time()-t0:.0f}s] pw done", file=sys.stderr, flush=True)
gr = json.load(open(P4 + "graded_V311-FULL.json"))["results"]
for arm in V8.GRADED_ARMS:
    out["runs"].append(dict(one(arm, (0, 1, 2, 3, 4), gr[arm]["all"]), source=f"graded_V311-FULL.json:{arm}"))
    print(f"[{time.time()-t0:.0f}s] {arm} done", file=sys.stderr, flush=True)
json.dump(out, open(sys.argv[1], "w"), indent=1, default=str)
