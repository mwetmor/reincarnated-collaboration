#!/usr/bin/env python3
"""KC2-PLAY · prereg v1.14 · STATIC DERIVATIONS + PINS (gamora, 2026-10-02). READ-ONLY on the engine and the packs.

Every expected value prereg v1.14 carries that is NOT read off a fight trace is derived here, by script, from the
v3.11 packs and the v3.11 ORACLE OF RECORD (engine `969fbd8d`, `scripts/gamora_kc2_play_v3p11_oracle_2026_10_02.py`,
imported unmodified). No port output is read. Digests are computed, never typed; the only typed constants are the
v1.13 values each derivation is COMPARED to (to print the v1.13 -> v1.14 delta), and star-lord's KP-235 pin prefixes
(checked as prefixes of what is computed here).

Run:  python3 derive_v1p14.py   -> writes derive_v1p14.json beside itself; prints a summary; exit 0 iff every
      self-check holds (a failed self-check is a STOP, not a value).
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import struct
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
HOME = Path.home() / "Games"
ENGINE = HOME / "reincarnated-engine"
COLLAB = HOME / "reincarnated-collaboration"
SRC = ENGINE / "src"
OUT = SRC / "reincarnated/output"
MODEL = OUT / "kc2-model-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143"
REFP = OUT / "kc2-reference-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143"
MODEL371 = OUT / "kc2-model-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247"
RECEIPT = OUT / "kc2-baton-v3-cut-receipt-v3p11-20261002_192143.json"
ORACLE_SCRIPT = SRC / "reincarnated/simulation/scripts/gamora_kc2_play_v3p11_oracle_2026_10_02.py"
MIGRATION = SRC / "reincarnated/export/MIGRATION.md"
X8 = SRC / "reincarnated/simulation/output/kc2-lifted-rows-KC2PLAY-SEALLAP-W1-c2-energy-fold-20260928_232836.json"
WALK_BARE_SL = OUT / "kc2-v3p11-POST-bare-WALK-20261002_192143.json"     # star-lord's, CROSS-REFERENCE only
HERE = Path(__file__).resolve().parent
ENGINE_REV = "969fbd8d"
WAVES = list(range(151, 161))

#: star-lord KP-235 / MIGRATION § 3 pin PREFIXES (checked as prefixes of the computed digests)
SL = {"model_pack": "99711727", "reference_pack": "af58ef40", "input_closure_v3p11": "073d57cd",
      "oracle_inputs_v3p11": "8c56d2a0", "v3p11_all": "8dad7a2d", "v3p11_closure_all": "00786a3d",
      "v3p11_hand_all": "5b7a6a53"}
#: v1.13 values, for the delta column ONLY
V113 = {"V11-P06-1": [5, 5, 5, 4, 4, 5, 5, 5, 5, 4], "P06-KEY": [0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        "TA-X-10_bound": 43.758085029822276, "TA-X-17_extents": 8.0,
        "TA-X-18_bits": ["c00fffffffffffde", "be9777a5cf72cec6"],
        "TA-X-09_rowset": "0e826ee093b98767901271c95e918a19e1c6d5b8a8663c99c87d8ced17086e78",
        "TA-X-21_sites": [1561, 1681, 1714, 2052],
        "TA-X-27d": [139, 97],
        "POOL-466": "33c886a11f91db1143c791ffcf9d95f7e7614e423373235231733c994c5c157b",
        "SWING-456": "706a61d55dc6621814fc923d7428c5b263a95ebb00e9786d12f35dd385a7a4c0",
        "NONSWING-10": "00b4cb0e24b43e591a2e30200979725801aad1e7c1f9b7764ebef67461816e10",
        "FALLBACK-158": "e8114efaa8fa678db6a26bb6e4ffb926fc2c1a15a978e3d589cf918ff17ae6cb",
        "TA-X-29e": {"w159": 3.207764, "w160": 4.980316},
        "TA-X-29e_walk": [3.353866, 1.768566, 1.899330, 2.994929, 1.927777, 2.846875, 1.979824, 1.592632,
                          3.207764, 4.980316],
        "P-i": "cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e",
        "kit_channel_radius_m": 3.0}
FAIL = []


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fsha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def q91(o) -> str:
    return sha(json.dumps(o, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8"))


def setd(s) -> str:
    return sha("\n".join(sorted(s)).encode("utf-8"))


def check(name: str, ok: bool) -> bool:
    if not ok:
        FAIL.append(name)
    return ok


R: dict = {"engine_rev": ENGINE_REV}

# ================================================================================================ A · PACKS
def pack(d: Path, sub: str) -> dict:
    pm = json.loads((d / "manifest.json").read_text())
    pl, bad = [], []
    for m in pm["members"]:
        p = d / m["path"]
        g = fsha(p)
        if g != m["sha256"] or p.stat().st_size != m["bytes"]:
            bad.append(m["path"])
        pl.append(f"{m['path']}  {g}")
    disk = sorted(str(p.relative_to(d)) for p in (d / sub).rglob("*") if p.is_file())
    return {"digest": sha("\n".join(sorted(pl)).encode("utf-8")), "manifest_digest": pm["pack_digest"],
            "n": len(pm["members"]), "member_failures": bad,
            "disk_equals_manifest": disk == sorted(m["path"] for m in pm["members"]),
            "cross_pin": (pm.get("cross_pin") or {}).get("model_pack_digest"),
            "manifest_file": fsha(d / "manifest.json"),
            "members": {m["path"]: {"sha256": fsha(d / m["path"]), "bytes": (d / m["path"]).stat().st_size}
                        for m in pm["members"]}}


mp, rp = pack(MODEL, "model"), pack(REFP, "reference")
R["packs"] = {"model": mp, "reference": rp}
check("model pack self", not mp["member_failures"] and mp["disk_equals_manifest"] and mp["digest"] == mp["manifest_digest"])
check("reference pack self", not rp["member_failures"] and rp["disk_equals_manifest"]
      and rp["digest"] == rp["manifest_digest"])
check("cross_pin", rp["cross_pin"] == mp["digest"])
check("SL model PACK prefix", mp["digest"].startswith(SL["model_pack"]))
check("SL reference PACK prefix", rp["digest"].startswith(SL["reference_pack"]))
check("SL input_closure_v3p11", mp["members"]["model/input_closure_v3p11.json"]["sha256"].startswith(SL["input_closure_v3p11"]))
check("SL oracle_inputs_v3p11", mp["members"]["model/oracle_inputs_v3p11.json"]["sha256"].startswith(SL["oracle_inputs_v3p11"]))

# ROWSETs, star-lord's law (Q91 over {"<member>:<rowset>": rows}), re-implemented from the pack bytes
model = {m: json.loads((MODEL / m).read_text()) for m in mp["members"] if m.endswith(".json")}
KEY = "⚑ v3p11_rows"
hand = {}
for m, t in sorted(model.items()):
    if m == "model/input_closure_v3p11.json" or not isinstance(t, dict) or KEY not in t:
        continue
    for k, v in sorted(t[KEY].items()):
        hand[f"{m}:{k}"] = v
clos = dict(model["model/input_closure_v3p11.json"][KEY])
allrs = dict(hand)
for k, v in clos.items():
    allrs[f"model/input_closure_v3p11.json:{k}"] = v
R["rowsets"] = {"v3p11_all": q91(allrs), "v3p11_closure_all": q91(clos), "v3p11_hand_all": q91(hand),
                "n_hand_rowsets": len(hand), "n_closure_rowsets": len(clos),
                "n_hand_rows": sum(len(v) for v in hand.values()), "n_closure_rows": sum(len(v) for v in clos.values())}
for k in ("v3p11_all", "v3p11_closure_all", "v3p11_hand_all"):
    check(f"SL ROWSET {k}", R["rowsets"][k].startswith(SL[k]))
R["documents"] = {"receipt": fsha(RECEIPT), "oracle_script": fsha(ORACLE_SCRIPT), "MIGRATION.md": fsha(MIGRATION),
                  "x8 (P-n.2)": fsha(X8)}
rc = json.loads(RECEIPT.read_text())
R["receipt_verdict"] = rc.get("verdict")

# the pack is ADDITIVE over v3.7.1: every v3.7.1 top-level key of every shared member is byte-equal (Q91)
add = {}
for m in sorted(model):
    p371 = MODEL371 / m
    if not p371.exists() or m.startswith("model/input_closure"):
        continue
    a = json.loads(p371.read_text())
    b = model[m]
    if not isinstance(a, dict):
        continue
    add[m] = {"changed_v371_keys": sorted(k for k in a if k in b and q91(a[k]) != q91(b[k])),
              "removed": sorted(k for k in a if k not in b), "added": sorted(k for k in b if k not in a)}
R["additive_over_v371"] = add
check("additive (only meta headers moved)", all(not v["removed"] and (not v["changed_v371_keys"] or m == "model/meta.json")
                                              for m, v in add.items()))

# ================================================================================================ B · a8 (v3.11): arms
a8 = model["model/input_closure_v3p11.json"][KEY]["a8_composition_calls_v3p11"]
jobs = defaultdict(list)
for row in a8:
    jobs[row["value"]["job"]].append(row)


def a8_rowset(rows) -> str:
    return sha(json.dumps(sorted(rows, key=lambda r: r["id"]), sort_keys=True, separators=(",", ":"),
                          default=str).encode())


FIGHT = ("M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL")
fight_callees = [{r["value"]["callee"] for r in jobs[j]} for j in FIGHT]
setup_C = sorted(r["id"] for r in jobs["setup"] if not any(r["value"]["callee"] in fc for fc in fight_callees))
setup_T = sorted(r["id"] for r in jobs["setup"] if all(r["value"]["callee"] in fc for fc in fight_callees))
R["a8"] = {"n": len(a8), "jobs": {j: {"n": len(v), "rowset": a8_rowset(v),
                                      "ids": [min(r["id"] for r in v), max(r["id"] for r in v)]}
                                  for j, v in sorted(jobs.items())},
           "setup_partition": {"C (shared config)": setup_C, "T (probe instance)": setup_T,
                               "neither": sorted(set(r["id"] for r in jobs["setup"]) - set(setup_C) - set(setup_T))}}
# the callees that DISTINGUISH each arm (present in that job, absent from at least one other fight job)
allc = Counter(c for fc in fight_callees for c in fc)
R["a8"]["distinguishing_callees"] = {j: sorted(c for c in fc if allc[c] < 5) for j, fc in zip(FIGHT, fight_callees)}


def argval(row, name):
    a = row["value"]["args"].get(name)
    return None if a is None else {"explicit": a.get("explicit"), "value": a.get("value")}


key_ctor = {}
for j in FIGHT:
    d = {}
    for r in jobs[j]:
        c = r["value"]["callee"]
        short = c.split("reincarnated.simulation.")[-1]
        if c.endswith("ChannelPolicyFold.__init__"):
            d.setdefault(short, []).append(argval(r, "armed"))
        elif c.endswith("ArenaFold.__init__"):
            d.setdefault(short, []).append({"armed": argval(r, "armed"), "avoidance": argval(r, "avoidance")})
        elif c.endswith("run_cell"):
            d.setdefault(short, []).append({"seat": argval(r, "seat"), "arena": (r["value"]["args"].get("arena") or {}).get("explicit")})
        elif c.endswith("threat.load_profiles"):
            d.setdefault(short, []).append(sorted(k for k, v in r["value"]["args"].items() if v.get("explicit")))
    key_ctor[j] = d
R["a8"]["arm_keys"] = key_ctor
R["a8"]["callees_per_arm"] = {j: sorted(Counter(r["value"]["callee"].split("reincarnated.simulation.")[-1] for r in jobs[j]).items())
                              for j in FIGHT}

# ================================================================================================ C · the oracle
sys.path.insert(0, str(SRC))
cwd = os.getcwd()
os.chdir(SRC)
from reincarnated.export.kc2_baton_v3p5p1_schema import pool466, derive_oracle_speeds, partition  # noqa: E402
from reincarnated.simulation.kc2 import wave_engine as we  # noqa: E402
from reincarnated.simulation.kc2 import referent_lineup as rl  # noqa: E402
from reincarnated.simulation.kc2 import threat as th  # noqa: E402
from reincarnated.simulation.kc2 import pool_lift as PL  # noqa: E402
from reincarnated.simulation.kc2 import offense as ofs  # noqa: E402
from reincarnated.simulation.kc2 import winner_surface as WS  # noqa: E402
from reincarnated.simulation.kc2 import c11a_corrections as C11  # noqa: E402
from reincarnated.simulation.kc2 import locomotion as lo  # noqa: E402
from reincarnated.simulation.kc2 import arena_fold as af  # noqa: E402
from reincarnated.simulation.kc2.spawn_structure import SpawnStructureFold, ScatterLaw, RngRepr  # noqa: E402
from reincarnated.simulation.scripts import gamora_kc2_upn5_global_magnitude_lift_2026_09_29 as u5  # noqa: E402
from reincarnated.simulation.scripts import gamora_kc2_play_v3p10_oracle_2026_10_02 as V310  # noqa: E402
from reincarnated.simulation.scripts import gamora_kc2_play_v3p11_oracle_2026_10_02 as V311  # noqa: E402

# ---- C.1 TA-X-16: the vector, from the LINE-UP FOLD's own pools (Matt Q96.1 grain: KEY), cross-checked
ws_rows = model["model/waves.json"]["pools"]["wave_spawn"]
keys_on = {w: sorted({r["spawn_point"] for r in ws_rows if r["global_wave"] == w}) for w in WAVES}
v11 = [len([p for p in keys_on[w] if p != 6]) for w in WAVES]
p06 = [int(6 in keys_on[w]) for w in WAVES]
lu_keys = {w: sorted(int(k) for k in rl.REFERENT_LINEUP[w]) for w in WAVES}
lu_vec = [len(lu_keys[w]) for w in WAVES]
off_keys = {w: sorted(int(k) for k in we.pools_for(w, bonus_spawns_enabled=False)) for w in WAVES}
on_keys = {w: sorted(int(k) for k in we.pools_for(w, bonus_spawns_enabled=True)) for w in WAVES}
rcp = model["model/rng_contract.json"]
pack_v11 = [r for r in rcp["⚑ v3p2_rows"]["v11_release_schedule_and_scatter"] if r["id"] == "V11-P06-1"][0]["value"]
# every line-up spec resolves to EXACTLY ONE pool alternative at its point, p06 OFF (the fold raises otherwise)
resolve_ok = True
for w in WAVES:
    for sp, specs in rl.REFERENT_LINEUP[w].items():
        for s in specs:
            try:
                rl.resolve_alternative(w, sp, s)
            except Exception:                       # noqa: BLE001
                resolve_ok = False
R["TA-X-16"] = {
    "law_v1.14": "LU-KEYS[w] = |keys of referent_lineup.REFERENT_LINEUP[w]| (the fought board's spawn-point keys), w = 151..160",
    "LU-KEYS": lu_vec, "LU-KEYS_sets": {str(w): lu_keys[w] for w in WAVES},
    "V11-P06-1 (waves.json, incumbent roll)": v11, "P06-KEY": p06, "sum_LU": sum(lu_vec), "sum_V11": sum(v11),
    "checks": {
        "LU key set == pools_for(w, False) key set, every wave": all(lu_keys[w] == off_keys[w] for w in WAVES),
        "LU vector == V11-P06-1 (waves.json)": lu_vec == v11,
        "V11-P06-1 == the pack's V11-P06-1 row": v11 == pack_v11["active_points_per_wave_151_160"],
        "no key 6 in any LU wave": all(6 not in lu_keys[w] for w in WAVES),
        "pools_for(w, True) minus pools_for(w, False) == {6} iff P06-KEY": all(
            sorted(set(on_keys[w]) - set(off_keys[w])) == ([6] if p06[i] else []) for i, w in enumerate(WAVES)),
        "every LU spec resolves to exactly one alternative (p06 OFF)": resolve_ok,
        "equals v1.13's vector": lu_vec == V113["V11-P06-1"] and p06 == V113["P06-KEY"]}}
check("TA-X-16 derivation", all(R["TA-X-16"]["checks"].values()))

# ---- C.2 TA-X-27(d): the pack census (unchanged rows) + the line-up's CONDITIONED randint pairs (information)
pairs = defaultdict(dict)
for r in model["model/waves.json"]["pools"]["wave_spawn_count"]:
    if 151 <= r["global_wave"] <= 160:
        pairs[(r["global_wave"], r["spawn_point"], r["pool_record"], r.get("pool_kind"))][r["bound"]] = r["value"]
plist = [(int(pairs[k]["min"]), int(pairs[k]["max"])) for k in sorted(pairs)]
R["TA-X-27d"] = {"pairs": len(plist), "degenerate": sum(1 for lo_, hi in plist if lo_ == hi),
                 "equals_v1.13": [len(plist), sum(1 for lo_, hi in plist if lo_ == hi)] == V113["TA-X-27d"]}

# ---- C.3 TA-X-09 / TA-X-20 / TA-X-17 extents / P-i
mr = model["model/math_rules.json"]
FIVE = ["RULE-CHANNEL-MOVEMENT", "RULE-RELEASE-TYPE-A", "RULE-RELEASE-TYPE-B",
        "RULE-CAST-INTERRUPT-BINDING-EXCLUSIVITY", "RULE-DMG-APPLIED"]
vecs = [tv for r in mr["rules"] if r.get("rule_id") in FIVE for tv in r.get("test_vectors", [])]
R["TA-X-09"] = {"n": len(vecs), "rowset": q91(vecs), "math_rules_file": mp["members"]["model/math_rules.json"]["sha256"],
                "equals_v1.13": q91(vecs) == V113["TA-X-09_rowset"]}
kit = model["model/player_kit.json"]
R["TA-X-20"] = {"kit_channel_radius_m": kit["channel"]["radius_m"]["value"],
                "player_kit_file": mp["members"]["model/player_kit.json"]["sha256"]}
arena = model["model/arena.json"]
R["TA-X-17"] = {"placement_extents_m (arena.json)": arena["placement_extents_m"]["value"],
                "lo.PLACEMENT_EXTENTS_M": float(lo.PLACEMENT_EXTENTS_M) if hasattr(lo, "PLACEMENT_EXTENTS_M") else None}
pi = ENGINE / "data/kc2/pm4p_leech_resistance.csv"
with open(pi, newline="") as fh:
    lrows = list(csv.DictReader(fh))
R["TA-X-26"] = {"P-i": fsha(pi), "P-i_equals_v1.13": fsha(pi) == V113["P-i"], "rows": len(lrows),
                "records": len({r.get("record") or r.get("record_path") or r.get(list(r)[0]) for r in lrows})}

# ---- C.4 TA-X-18: the oracle's own scatter fold, u1 = u2 = 0.5
class _Half:
    def random(self):
        return 0.5


off = SpawnStructureFold(scatter=ScatterLaw.POLAR_UNIFORM_RHO, rng_repr=RngRepr.CONTINUOUS).offset(_Half())
R["TA-X-18"] = {"value": [repr(x) for x in off], "bits": [struct.pack(">d", x).hex() for x in off]}
R["TA-X-18"]["equals_v1.13"] = R["TA-X-18"]["bits"] == V113["TA-X-18_bits"]

# ---- C.5 TA-X-21: the oracle's live round( sites (threat.py at the oracle rev)
tl = (SRC / "reincarnated/simulation/kc2/threat.py").read_text().splitlines()
sites = [(i + 1, l.strip()) for i, l in enumerate(tl) if "round(" in l]
R["TA-X-21"] = {"threat_py": fsha(SRC / "reincarnated/simulation/kc2/threat.py"), "round_sites": sites,
                "all_int_round": all("int(round(" in l for _, l in sites),
                "line_numbers_equal_v1.13": [n for n, _ in sites] == V113["TA-X-21_sites"]}

# ---- C.6 (geometry): read off the W1 trace (ArenaFold.wall_block, the oracle's own derivation) in check_v1p14.py

# ---- C.7 the v3.11 GRADED LOADER (inside the oracle's own contexts): set digests + the TA-X-29(e) walk
tree = {"model/waves.json": model["model/waves.json"]}
pool, routes_agree = pool466(tree)
mtree = {m: t for m, t in model.items()}
spd = derive_oracle_speeds(mtree)
part = partition(spd)
fb = [k for k in part if len(part[k]) == 158]
assert fsha(X8) == "cc361a3fea3e24e55fdf0c8c8eaf52bcc0c729c7de0563d3c84dd0dc21202960", "P-n.2"
f = V311.Folds311("V311-FULL")
walk = {}
with V310.v3p10_oracle(f.v310), V311.v3p11_oracle(f):
    profiles, _pets, _rep = th.load_profiles(
        dot_corrections=True, pet_special_gates=None, winner_surface=WS.WinnerSurfaceFold.from_x8(str(X8)),
        pool_lift=PL.load(), c11a=C11.C11aLoader(scope=C11.AuraScope.CLASS))
    cs = {}
    for k, v in profiles.items():
        s_ = v.can_swing
        cs[k.lower()] = bool(s_() if callable(s_) else s_)
    for w in WAVES:
        rs: set = set()
        for _pt, alts in we.pools_for(w, bonus_spawns_enabled=True).items():
            for a in alts:
                rs |= set(a.roster_records or ())
                rs |= set(a.champ_records or ())
                if a.proxy_record:
                    rs.add(a.proxy_record)
        cands = sorted(x for x in rs if x)
        fw = u5.resolver(w)
        m_inst = ofs.fold_at(w, to_hit=True, attack_speed=True).instant_mult
        on_tot = off_tot = 0.0
        recs, unpriced, n_id = {}, [], 0
        for rec in cands:
            prof = profiles.get(rec)
            if prof is None:
                unpriced.append(rec)
                continue
            mm = u5.price_record_at_wave(prof, fw, m_inst)
            if mm is None:
                continue
            on_tot += mm["sum_fold_on"]
            off_tot += mm["sum_fold_off"]
            if not (mm["folds_attr"] or mm["folds_own"]):
                n_id += 1
            recs[rec] = {k: mm[k] for k in ("ratio", "sum_fold_on", "sum_fold_off", "folds_attr", "folds_own")}
        walk[str(w)] = {"M_inst": round(m_inst, 6), "n_candidates": len(cands), "n_priced": len(recs),
                        "n_identity_path_priced": n_id, "unpriced_no_profile": unpriced,
                        "ratio": (round(on_tot / off_tot, 6) if off_tot > 0 else None), "records": recs}
swing = {r for r in pool if cs.get(r)}
nonswing = pool - swing
R["sets"] = {"POOL-466": {"n": len(pool), "digest": setd(pool), "routes_agree": routes_agree},
             "SWING (v3.11 graded loader)": {"n": len(swing), "digest": setd(swing)},
             "NONSWING (v3.11 graded loader)": {"n": len(nonswing), "digest": setd(nonswing), "members": sorted(nonswing)},
             "FALLBACK": {"n": len(part[fb[0]]) if fb else None, "digest": setd(part[fb[0]]) if fb else None},
             "partition": {k: len(v) for k, v in part.items()}, "march_base": spd.get("march_base"),
             "equals_v1.13": {"POOL-466": setd(pool) == V113["POOL-466"], "SWING-456": setd(swing) == V113["SWING-456"],
                              "NONSWING-10": setd(nonswing) == V113["NONSWING-10"],
                              "FALLBACK-158": bool(fb) and setd(part[fb[0]]) == V113["FALLBACK-158"]}}
R["TA-X-29e"] = {"walk": walk, "ten_ratios": [walk[str(w)]["ratio"] for w in WAVES],
                 "v1.13_ten_ratios": V113["TA-X-29e_walk"],
                 "w159": walk["159"]["ratio"], "w160": walk["160"]["ratio"]}
if WALK_BARE_SL.exists():
    sl = json.loads(WALK_BARE_SL.read_text())
    slw = (sl.get("cells") or sl).get("waves") if isinstance(sl, dict) else None
    if slw is None:
        def _find(o):
            if isinstance(o, dict):
                if "waves" in o and isinstance(o["waves"], dict) and "159" in o["waves"]:
                    return o["waves"]
                for v in o.values():
                    x = _find(v)
                    if x is not None:
                        return x
            return None
        slw = _find(sl)
    R["TA-X-29e"]["star-lord POST-bare-WALK (cross-reference)"] = {
        "file": fsha(WALK_BARE_SL),
        "ten_ratios": [slw[str(w)]["supply_weighted_fold_ratio"] for w in WAVES] if slw else None}
    R["TA-X-29e"]["equals star-lord's bare walk"] = (slw is not None and [slw[str(w)]["supply_weighted_fold_ratio"]
                                                                          for w in WAVES] == R["TA-X-29e"]["ten_ratios"])

# ---- C.8 TA-X-29(c): the oracle's M_inst per wave against the pack's z3 rows (unchanged rows)
mo = model["model/monster_offense.json"]
z3 = {r["value"]["wave"]: r["value"]["M_inst"] for r in mo["⚑ v3p4p2_rows"]["z3_wave_damage_modifier_check"]}
R["TA-X-29c"] = {str(w): [round(ofs.fold_at(w, to_hit=True, attack_speed=True).instant_mult, 9), z3.get(w)] for w in WAVES}
# ---- C.9 the oracle's scope pointers on the v3.11 pack (cg1): which carried laws the V311-FULL folds govern
cg1 = []
for m, t in model.items():
    if isinstance(t, dict) and KEY in t:
        for r in t[KEY].get("cg1_scope_pointers", []):
            cg1.append({"member": m, "id": r.get("id"), "targets": (r.get("value") or {}).get("target_row_id")
                        or (r.get("value") or {}).get("targets") or r.get("key"),
                        "text": json.dumps(r.get("value"), ensure_ascii=False)[:400]})
R["cg1_scope_pointers"] = cg1
os.chdir(cwd)

# ================================================================================================ D · engine provenance
head = subprocess.run(["git", "-C", str(ENGINE), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
mods = sorted({m.__file__ for n, m in list(sys.modules.items()) if n.startswith("reincarnated") and getattr(m, "__file__", None)})
bad = []
for p in mods:
    rel = os.path.relpath(p, ENGINE)
    blob = subprocess.run(["git", "-C", str(ENGINE), "show", f"{ENGINE_REV}:{rel}"], capture_output=True).stdout
    if sha(blob) != fsha(Path(p)):
        bad.append(rel)
R["engine"] = {"HEAD": head, "modules_imported": len(mods), "modules_differing_from_blob": bad,
               "porcelain_oracle_tree": subprocess.run(
                   ["git", "-C", str(ENGINE), "status", "--porcelain", "--", "src/reincarnated/simulation/kc2",
                    "src/reincarnated/export", "data/kc2"], capture_output=True, text=True).stdout.strip()}
check("engine HEAD is the oracle rev", head.startswith(ENGINE_REV))
check("every imported engine module == its blob at 969fbd8d", not bad)

R["self_check_failures"] = FAIL
(HERE / "derive_v1p14.json").write_text(json.dumps(R, indent=1, sort_keys=True, default=str, ensure_ascii=False) + "\n")
print("packs", mp["digest"][:16], rp["digest"][:16], "rowsets", {k: v[:8] for k, v in R["rowsets"].items() if isinstance(v, str)})
print("TA-X-16", R["TA-X-16"]["LU-KEYS"], R["TA-X-16"]["checks"])
print("TA-X-27d", R["TA-X-27d"], "TA-X-09", R["TA-X-09"]["equals_v1.13"], "TA-X-18", R["TA-X-18"])
print("TA-X-21", [n for n, _ in sites])
print("sets", {k: (v["n"], v["digest"][:8]) for k, v in R["sets"].items() if isinstance(v, dict) and "digest" in v},
      R["sets"]["equals_v1.13"], "NONSWING", R["sets"]["NONSWING (v3.11 graded loader)"]["members"])
print("TA-X-29e", R["TA-X-29e"]["ten_ratios"], "SL equal:", R["TA-X-29e"].get("equals star-lord's bare walk"))
print("a8", {j: (v["n"], v["rowset"][:8]) for j, v in R["a8"]["jobs"].items()}, R["a8"]["setup_partition"])
print("engine", R["engine"]["HEAD"][:8], "modules", R["engine"]["modules_imported"], "differ", bad)
print("SELF-CHECK FAILURES:", FAIL)
sys.exit(1 if FAIL else 0)
