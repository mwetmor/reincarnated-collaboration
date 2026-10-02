#!/usr/bin/env python3
"""KC2-PLAY · H-6 pre-read (jack-ryan, 2026-10-02) · the gate's verdict over its OWN probe outputs (h6_gate_probe.py).

Reads probe_<ARM>.json (+ probe_round_M-POL-2.json when present) beside itself; recomputes, independently of gamora's
check_v1p14.py / check_v1p15.py, the rows the gate re-measures; writes h6_gate_results.json. No port output is read.

Run: python3 h6_gate_check.py
"""
import json
import os
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARMS = ["M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL"]
SALTS = ["0", "1", "2", "3", "4"]
WAVES = list(range(151, 161))
P = {a: json.loads((HERE / f"probe_{a}.json").read_text()) for a in ARMS}

sys.path.insert(0, "/Users/admin/Games/reincarnated-engine/src")
_cwd = os.getcwd()
os.chdir("/Users/admin/Games/reincarnated-engine/src")
from reincarnated.simulation.kc2 import referent_lineup as rl  # noqa: E402
from reincarnated.export.kc2_baton_v3p5p1_schema import pool466  # noqa: E402
MODEL = Path("/Users/admin/Games/reincarnated-engine/src/reincarnated/output/"
             "kc2-model-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143/model")
WJ = json.loads((MODEL / "waves.json").read_text())
POOL, _ = pool466({"model/waves.json": WJ})
os.chdir(_cwd)

R = {"inputs": {a: {"wall_s": P[a]["wall_s"]} for a in ARMS}}

# ---- 1 · completeness: the SHARED OBS-1 guard + the gate's innermost observer
comp = {}
for a in ARMS:
    g = P[a]["obs1_guard"]
    for s in SALTS:
        x = P[a]["salts"][s]
        oc = x["waves"]
        death = next((w[0] for w in oc if w[1] == "player_death"), None)
        ok_obs = ([w[0] for w in oc] == WAVES and not x["exceptions"] and x["raised"] is None
                  and all((w[1], w[2]) in (("cleared", "board_empty"), ("player_death", "player_died")) for w in oc))
        leg = x["leg_a"] or {}
        ok_leg = (leg.get("wave") == death) if death else (leg.get("wave") is None and oc[-1][1:3] == ["cleared", "board_empty"])
        comp[f"{a}|{s}"] = {"shared_guard_G1_G2": g["per_salt"][s]["complete"], "gate_observer": ok_obs, "leg_a_consistent": ok_leg,
                            "terminal": death or "cleared_w160", "max_wave_ticks": max(w[4] - w[3] for w in oc),
                            "complete": g["per_salt"][s]["complete"] and ok_obs and ok_leg}
R["completeness"] = {"per_cell": comp, "n_complete": sum(c["complete"] for c in comp.values()),
                     "shared_guard_G3_per_arm": {a: not P[a]["obs1_guard"]["cell_reasons"] for a in ARMS},
                     "shared_guard_module_sha256": P["W1"]["obs1_guard_module_sha256"],
                     "tick_cap": [P["W1"]["obs1_guard"]["max_ticks"], P["W1"]["obs1_guard"]["tick_cap_s"]],
                     "G4": "N/A: run_one returns no summary layer (keys %s)" % P["W1"]["run_one_keys"]}

# ---- 2 · trajectories, TA-X-01/03/04/05/06 relations
D = {(a, s): P[a]["salts"][s]["traj_digest"] for a in ARMS for s in SALTS}
rel = lambda x, y: [D[(x, s)] == D[(y, s)] for s in SALTS]
R["trajectories"] = {"distinct": len(set(D.values())),
                     "TA-X-03 M-POL-2-NULL==M0": rel("M-POL-2-NULL", "M0"),
                     "TA-X-04 W1-NULL==M-POL-2": rel("W1-NULL", "M-POL-2"),
                     "TA-X-05 M-POL-2==M0": rel("M-POL-2", "M0"),
                     "TA-X-06 W1==M-POL-2": rel("W1", "M-POL-2"),
                     "distinct_dying": len({D[k] for k in D if comp[f"{k[0]}|{k[1]}"]["terminal"] != "cleared_w160"}),
                     "distinct_clearing": len({D[k] for k in D if comp[f"{k[0]}|{k[1]}"]["terminal"] == "cleared_w160"})}

# ---- 3 · TA-X-30(a') by the gate's rule; (b') clamp stops; the clip limb
t30, opc = Counter(), Counter()
for a in ARMS:
    for s in SALTS:
        t30.update(P[a]["salts"][s]["t30"])
        opc.update(P[a]["salts"][s]["op_class"])
R["TA-X-30(a') gate rule"] = {"totals": dict(t30), "operand_classes": dict(opc),
                              "holds": t30.get("fail", 0) == 0,
                              "non_waypoint_pursue_steps_with_op=reach(1-1e-9)": opc.get("pursue_reach_in_pack", 0)}
R["TA-X-30(b') clamp"] = {f"{a}|{s}": {"clamp_calls": P[a]["salts"][s]["clamp_calls"],
                                       "clamp_returned_True (a stop)": P[a]["salts"][s]["clamp_true"],
                                       "stops beyond op": P[a]["salts"][s]["clamp_true_player_target_nonwp_beyond_op"],
                                       "arena_armed": bool(P[a]["salts"][s]["arena"] and P[a]["salts"][s]["arena"][0][1])}
                          for a in ARMS for s in SALTS}
R["TA-X-30(b') summary"] = {"cells_with_any_clamp_stop": sum(1 for v in R["TA-X-30(b') clamp"].values() if v["clamp_returned_True (a stop)"]),
                            "W1_clamp_calls": sum(v["clamp_calls"] for k, v in R["TA-X-30(b') clamp"].items() if k.startswith("W1|")),
                            "holds": all(v["stops beyond op"] == 0 for v in R["TA-X-30(b') clamp"].values())}
R["clip limb"] = {"max_admissible_travel calls (25 cells)": sum(P[a]["salts"][s]["clip_calls"] for a in ARMS for s in SALTS),
                  "steps shortened by the clip": sum(P[a]["salts"][s]["clip_shortened_steps"] for a in ARMS for s in SALTS)}

# ---- 4 · TA-X-29(b') divisor reachability
R["TA-X-29(b') divisor"] = {
    "SlowChaos/SlowAether DoT rows composed (25 cells)": sum(P[a]["salts"][s]["chaos_aether"].get("rows", 0) for a in ARMS for s in SALTS),
    "of which divisor-eligible": sum(P[a]["salts"][s]["chaos_aether"].get("divisor_eligible", 0) for a in ARMS for s in SALTS),
    "SlowChaos/SlowAether DoT rows on ANY loaded roster or pet profile": len(P["W1"]["chaos_aether_dot_rows_on_loaded_profiles"]),
    "profiles scanned (roster, pets)": [P["W1"]["n_profiles_seen"], P["W1"].get("n_pet_profiles_seen")],
    "dot rows by type (25 cells)": dict(sum((Counter(P[a]["salts"][s]["dot_by_type"]) for a in ARMS for s in SALTS), Counter()))}

# ---- 5 · independent re-measures
LU = [len(rl.REFERENT_LINEUP[w]) for w in WAVES]
rows = {}
ok16 = ok15 = ok13 = ok12 = ok24 = ok25 = True
bad = []
for a in ARMS:
    for s in SALTS:
        x = P[a]["salts"][s]
        for i, w in enumerate(WAVES):
            k = x["lu_keys"].get(str(w))
            if k is None or len(k["fold_keys"]) != LU[i] or 6 in k["fold_keys"] or k["bonus"] is not False \
                    or not set(k["fought_points"]) <= set(k["fold_keys"]):
                ok16 = False
                bad.append(["16", a, s, w])
        for key in x["spawn_t"]:
            pt, t = key.split("@")
            if not ((pt in ("p01", "p02", "p03", "p04") and float(t) == 0.0) or (pt == "p05" and float(t) == 4.0)):
                ok15 = False
                bad.append(["15a", a, s, key])
        if any(src.startswith("player") for src in x["crit_sources"]):
            ok13 = False
        if x["pool_tags"]:
            ok12 = False
        if x["phase_model"] != ["PhaseModel.ENGAGE"]:
            ok24 = False
        if any(r.lower() not in POOL for r in x["records"]):
            ok25 = False
rows["TA-X-16 (LU-KEYS from REFERENT_LINEUP, no key 6, bonus off, every wave played)"] = {"LU-KEYS": LU, "holds": ok16}
rows["TA-X-15(a) (p01-p04 at 0.0 s, p05 at 4.0 s)"] = ok15
rows["TA-X-13 (no crit row sourced by the player)"] = {"holds": ok13, "crit_source_prefixes": sorted({k for a in ARMS for s in SALTS for k in P[a]["salts"][s]["crit_sources"]})[:12]}
rows["TA-X-12 (no 'pool' damage tag)"] = ok12
rows["TA-X-24 (phase ENGAGE)"] = ok24
rows["TA-X-25 (every fought record in POOL-466; membership only)"] = {"holds": ok25, "pool466_size": len(POOL)}
w1 = [P["W1"]["salts"][s] for s in SALTS]
rows["TA-X-10 (W1 max body / spawn radius vs the oracle's own r_wall)"] = {
    "max_body_r": max(x["max_body_r"] for x in w1), "max_spawn_r": max(x["max_spawn_r"] for x in w1),
    "oracle_r_wall_m": w1[0]["arena"][0][3], "prereg_bound": 43.71638147965161,
    "holds": max(max(x["max_body_r"], x["max_spawn_r"]) for x in w1) <= 43.71638147965161 and w1[0]["arena"][0][3] == 43.71638147965161}
rows["TA-X-11 (0 player / 0 body wall clamps, W1 + W1-NULL)"] = all(
    sum(r[4] for r in P[a]["salts"][s]["arena"]) == 0 and sum(r[5] for r in P[a]["salts"][s]["arena"]) == 0
    for a in ("W1", "W1-NULL") for s in SALTS)
rows["bad_examples"] = bad[:10]
R["independent_rows"] = rows

rp = HERE / "probe_round_M-POL-2.json"
if rp.exists():
    Q = json.loads(rp.read_text())
    R["TA-X-21 round-site liveness (M-POL-2, salts 0-4, line tracer)"] = Q["round_site_hits (trace_round mode only)"]
    R["TA-X-21 trace run reproduces the untraced run"] = all(
        Q["salts"][s]["traj_digest"] == P["M-POL-2"]["salts"][s]["traj_digest"] for s in SALTS)

(HERE / "h6_gate_results.json").write_text(json.dumps(R, indent=1, sort_keys=True, default=str) + "\n")
for k, v in R.items():
    if k in ("inputs",):
        continue
    if k == "completeness":
        print(k, {kk: vv for kk, vv in v.items() if kk != "per_cell"})
    elif k == "TA-X-30(b') clamp":
        continue
    else:
        print(k, json.dumps(v, default=str)[:700])
