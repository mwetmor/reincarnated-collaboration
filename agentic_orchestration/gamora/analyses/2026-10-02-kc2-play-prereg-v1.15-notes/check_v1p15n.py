#!/usr/bin/env python3
"""KC2-PLAY · prereg v1.15 NOTES · aggregate the five census runs (gamora, 2026-10-02).

Inputs: census/census_<ARM>.json.gz (from census_v1p15n.py); v1.14's committed bare traces (inertness) and
results_v1p14.json (the 12-trajectory collapse); v1.15's results_v1p15.json (TA-X-30 face facts).
Run: python3 check_v1p15n.py [--ingest <scratch dir>] -> results_v1p15n.json; exit 2 on a guard failure or a broken
inertness check (a STOP: nothing is filed from it).
"""
import gzip
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
V114 = HERE.parent / "2026-10-02-kc2-play-prereg-v1.14"
V115 = HERE.parent / "2026-10-02-kc2-play-prereg-v1.15"
ARMS = ["M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL"]
if len(sys.argv) > 2 and sys.argv[1] == "--ingest":
    (HERE / "census").mkdir(exist_ok=True)
    for a in ARMS:
        (HERE / "census" / f"census_{a}.json.gz").write_bytes(
            gzip.compress((Path(sys.argv[2]) / f"census_{a}.json").read_bytes(), mtime=0))
L = lambda p: json.loads(gzip.decompress(p.read_bytes()))
C = {a: L(HERE / "census" / f"census_{a}.json.gz") for a in ARMS}
R = {}
# --- guard of record + inertness against v1.14's bare runs
R["guard"] = {a: {"complete": C[a]["guard_of_record"]["cell_check"]["complete"],
                  "truncated_salts": C[a]["guard_of_record"]["cell_check"]["truncated_salts"],
                  "cell_reasons": C[a]["guard_of_record"]["cell_check"]["cell_reasons"],
                  "max_ticks (G2 cap)": C[a]["guard_of_record"]["cell_check"]["max_ticks"],
                  "tick_cap_s": C[a]["guard_of_record"]["cell_check"]["tick_cap_s"]} for a in ARMS}
R["guard_module_sha256"] = sorted({C[a]["guard_of_record"]["sha256"] for a in ARMS})
inert = {}
for a in ARMS:
    bare = L(V114 / "oracle_trace" / f"bare_{a}.json.gz")
    for s in range(5):
        inert[f"{a}|{s}"] = C[a]["salts"][str(s)]["rows_sha256"] == bare["run_one_salts"][str(s)]["rows_sha256"]
R["inert_vs_v1.14_bare (capture rows)"] = f"{sum(inert.values())}/25"
stop = not all(v["complete"] for v in R["guard"].values()) or not all(inert.values())
# --- TA-X-13 corrected classifier (leg A = all ten waves on every cell: no cell dies before w160)
crit = Counter()
crit_cell = {}
for a in ARMS:
    for s in range(5):
        cc = Counter()
        for k, n in C[a]["salts"][str(s)]["crit_by_wave_class"].items():
            cc[k.split("|")[1]] += n
        crit_cell[f"{a}|{s}"] = dict(cc)
        crit.update(cc)
R["TA-X-13"] = {"total_by_class": dict(crit), "per_cell": crit_cell,
                "player_rows_crit (in scope)": crit.get("player", 0),
                "player_summon_ps_ (out of scope)": crit.get("player_summon", 0),
                "monster (roster + pet)": crit.get("monster_roster", 0) + crit.get("monster_pet", 0),
                "other": crit.get("other", 0),
                "ps_ per cell range": [min(c.get("player_summon", 0) for c in crit_cell.values()),
                                       max(c.get("player_summon", 0) for c in crit_cell.values())]}
# --- TA-X-21 live round( sites, all arms
hits = Counter()
for a in ARMS:
    for s in range(5):
        hits.update(C[a]["salts"][str(s)]["round_site_hits_all_waves"])
scanned = {x["site"]: x for x in C["M-POL-2"]["round_sites_scanned"]}
BASIS = {"threat.py", "deferred_arrival.py", "dot_timeline.py", "control_application.py"}   # v1.2 § F.2a
GD = {"gd_engagement.py", "gd_reposition.py"}                                               # KP-248 ruling
CITED_V114 = {"threat.py:1613", "threat.py:1774", "threat.py:1813", "threat.py:2182"}
tab = []
for site, x in sorted(scanned.items(), key=lambda kv: (kv[0].split(":")[0], int(kv[0].split(":")[1]))):
    f = site.split(":")[0]
    scope = "row basis (v1.2 four modules)" if f in BASIS else ("GD fold (KP-248)" if f in GD else "outside the row's modules")
    tab.append({"site": site, "hits_25_cells": hits.get(site, 0), "live": hits.get(site, 0) > 0, "int_round": x["int_round"],
                "scope": scope, "cited_in_v1.14": site in CITED_V114, "text": x["text"]})
inscope = [t for t in tab if t["scope"] != "outside the row's modules"]
R["TA-X-21"] = {"sites": tab, "files_sha256": C["M-POL-2"]["round_site_files_sha256"],
                "live_in_scope": [t["site"] for t in inscope if t["live"]],
                "dead_in_scope": [t["site"] for t in inscope if not t["live"]],
                "dead_v1.14_cited": [t["site"] for t in tab if t["cited_in_v1.14"] and not t["live"]],
                "live_gd": [t["site"] for t in tab if t["scope"].startswith("GD") and t["live"]],
                "every_live_in_scope_is_int_round": all(t["int_round"] for t in inscope if t["live"]),
                "live_outside_scope": [t["site"] for t in tab if t["scope"] == "outside the row's modules" and t["live"]],
                "files_equal_across_arms": len({json.dumps(C[a]["round_site_files_sha256"], sort_keys=True) for a in ARMS}) == 1}
# --- INFO-3 divisor reachability
dr = C["M-POL-2"]["divisor_reachability"]
R["divisor"] = {"n_roster_profiles": dr["n_roster_profiles"], "n_pet_profiles": dr["n_pet_profiles"],
                "SlowChaos_SlowAether_rows_per_arm": {a: len(C[a]["divisor_reachability"]["chaos_aether_rows"]) for a in ARMS},
                "dot_types_present": sorted(k for k in dr["rows_by_type"] if k.startswith("Slow"))}
MODEL = Path("/Users/admin/Games/reincarnated-engine/src/reincarnated/output/"
             "kc2-model-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143/model")
R["divisor"]["pack_offense_text_hits"] = {f: (MODEL / f).read_text().count('"SlowChaos"') + (MODEL / f).read_text().count('"SlowAether"')
                                          for f in ("monster_offense.json", "monsters.json")}
# --- face facts: the 12-trajectory collapse and TA-X-30 clamp facts
r14 = json.loads((V114 / "results_v1p14.json").read_text())
dig = defaultdict(list)
for k, c in r14["cells"].items():
    dig[c["digest"]].append((k, c["terminal"]))
R["trajectories"] = {"distinct": len(dig),
                     "clearing": sum(1 for v in dig.values() if v[0][1] == "cleared_w160"),
                     "dying": sum(1 for v in dig.values() if v[0][1] != "cleared_w160"),
                     "classes": sorted([sorted(x[0] for x in v) for v in dig.values()])}
r15 = json.loads((V115 / "results_v1p15.json").read_text())
_per = C["M0"]["period"]
R["longest_wave_ticks_25_cells (v1.14 traces)"] = round(max(float(v) for c in r14["cells"].values()
                                                           for v in c["regime"]["wave_s"].values()) / _per)
R["TA-X-30_face"] = {"clamp_calls_W1": sum(r15["cells"][f"W1|{s}"]["TA-X-30(b) R-G4-V311"]["arena_clamp_calls"] for s in range(5)),
                     "non_waypoint_pursue_steps": r15["TA-X-30(a')"]["op_classes"].get("PURSUE", 0),
                     "clipped_steps": r15["TA-X-30(a')"]["clipped"] + r15["TA-X-30(a')"]["pet_moved_clipped_shorter"]}
R["STOP"] = stop
(HERE / "results_v1p15n.json").write_text(json.dumps(R, indent=1, sort_keys=True) + "\n")
print(json.dumps({k: v for k, v in R.items() if k not in ("TA-X-13", "TA-X-21")}, default=str)[:1500])
print("TA-X-13", {k: v for k, v in R["TA-X-13"].items() if k != "per_cell"})
print("TA-X-21 live in scope", R["TA-X-21"]["live_in_scope"], "dead", R["TA-X-21"]["dead_in_scope"],
      "int_round", R["TA-X-21"]["every_live_in_scope_is_int_round"])
sys.exit(2 if stop else 0)
