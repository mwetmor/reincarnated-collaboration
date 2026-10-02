#!/usr/bin/env python3
"""KC2-PLAY · prereg v1.15 NOTES companion · CENSUS (gamora, 2026-10-02; jack-ryan H-6 collab fd0851c77, conductor KP-248).
READ-ONLY on the engine. Runs the oracle of record (engine 969fbd8d `scripts/gamora_kc2_play_v3p11_oracle_2026_10_02.py`
run_one("V311-FULL", salts 0-4, period, arm) + v3p8.graded_arm, imported unmodified) on one arm and measures, over leg A:

  * WARN-2 / TA-X-13: crit rows (`is_crit`) by SOURCE CLASS with the corrected classifier: `player` (source_id ==
    "player"), `player_summon` (prefix `summons.SUMMON_ID_PREFIX` = "ps_"), `monster_roster` (an actor id of the wave),
    `monster_pet` (a pet id of the wave), `other`.
  * WARN-3 / TA-X-21: the LIVENESS of every source line containing `round(` in every `simulation/kc2` module, via
    `sys.monitoring` LINE events restricted to those lines (every other location is DISABLEd at first sight; the probe
    returns nothing into the oracle). Hits are counted only inside the recorded waves.
  * INFO-3: the divisor's reachability: every SlowChaos / SlowAether damage row on the roster and pet profiles the run's
    graded loader built (the last `threat.load_profiles` result inside the arm).
  * INFO-4: the shared OBS-1 guard of record (`scripts/gamora_join1_obs1_guard_2026_10_02.py`, engine 9c756081)
    applied to run_one's own result: `cell_check` G1-G3 (G4 N/A: run_one carries no summary layer).

Inertness: the run's capture rows digest is printed per salt; check_v1p15n.py compares it with v1.14's committed
bare-run digests.

Usage: python3 census_v1p15n.py <ARM> <out.json>
"""
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
ENGINE_SRC = "/Users/admin/Games/reincarnated-engine/src"
OUT = os.path.abspath(sys.argv[2])
ARM = sys.argv[1]
sys.path.insert(0, ENGINE_SRC)
os.chdir(ENGINE_SRC)
KC2 = Path(ENGINE_SRC) / "reincarnated/simulation/kc2"

from reincarnated.simulation.kc2 import run as kr  # noqa: E402
from reincarnated.simulation.kc2 import summons as sm  # noqa: E402
from reincarnated.simulation.kc2 import threat as th  # noqa: E402
from reincarnated.simulation.scripts import gamora_kc2_c11_lethality_decomposition_2026_09_29 as c11  # noqa: E402
from reincarnated.simulation.scripts import gamora_kc2_play_c11a_fold_pricing_2026_09_30 as FP  # noqa: E402
from reincarnated.simulation.scripts import gamora_kc2_play_v3p11_oracle_2026_10_02 as V311  # noqa: E402
from reincarnated.simulation.scripts import gamora_join1_obs1_guard_2026_10_02 as G  # noqa: E402

CUR = {"rec": False, "salt": None}
SITES = {}
for p in sorted(KC2.glob("*.py")):
    for i, l in enumerate(p.read_text().splitlines(), 1):
        code = l.split("#", 1)[0]
        if re.search(r"(?<![A-Za-z0-9_.])round\(", code):
            SITES[(str(p), i)] = {"file": p.name, "line": i, "text": l.strip(),
                                  "int_round": "int(round(" in code}
HITS = defaultdict(Counter)        # salt -> (file:line) -> hits
MON = sys.monitoring
TOOL = MON.PROFILER_ID if hasattr(MON, "PROFILER_ID") else 5
MON.use_tool_id(TOOL, "v115n-round-census")


def _line(code, lineno):
    key = (code.co_filename, lineno)
    if key not in SITES:
        return MON.DISABLE
    if CUR["rec"]:
        HITS[str(CUR["salt"])][f"{SITES[key]['file']}:{lineno}"] += 1
    return None


MON.register_callback(TOOL, MON.events.LINE, _line)
CRIT = defaultdict(Counter)
PROFILES = []
_olp = th.load_profiles


def _lp(*a, **kw):
    out = _olp(*a, **kw)
    PROFILES.append(out)
    return out
th.load_profiles = _lp
_real_arm = c11.run_arm


def _arm(runner, a, salt, period):
    CUR["rec"], CUR["salt"] = True, int(salt)
    try:
        return _real_arm(runner, a, salt, period)
    finally:
        CUR["rec"] = False
c11.run_arm = _arm
_true_sw = kr.simulate_wave


def _sw(*a, **kw):
    r = _true_sw(*a, **kw)
    if CUR["rec"]:
        actors = {x["actor_id"] for x in r.actors}
        pets = {p["actor_id"] for p in r.pet_actors}
        C = CRIT[str(CUR["salt"])]
        w = int(r.waves[0]["wave"])
        for x in r.rows_as_dicts():
            if not x.get("is_crit"):
                continue
            s = str(x.get("source_id") or "")
            cls = ("player" if s == "player" else "player_summon" if s.startswith(sm.SUMMON_ID_PREFIX)
                   else "monster_roster" if s in actors else "monster_pet" if s in pets else "other")
            C[f"{w}|{cls}"] += 1
    return r
kr.simulate_wave = _sw


def _rows_of(prof):
    seen = []

    def walk(o, depth=0):
        if depth > 4 or o is None:
            return
        if hasattr(o, "damage_type"):
            seen.append(o)
            return
        if isinstance(o, (list, tuple)):
            for y in o:
                walk(y, depth + 1)
            return
        for nm in ("slots", "rows", "weapon_rows", "auras", "dot_rows"):
            if hasattr(o, nm):
                walk(getattr(o, nm), depth + 1)
    walk(prof)
    return seen


def main():
    period = FP._period()
    MON.set_events(TOOL, MON.events.LINE)
    try:
        res = V311.run_one("V311-FULL", (0, 1, 2, 3, 4), period, arm=ARM)
    finally:
        MON.set_events(TOOL, 0)
        MON.free_tool_id(TOOL)
    guard = G.cell_check(res, (0, 1, 2, 3, 4), period)
    out = {"arm": ARM, "period": period, "guard_of_record": {"module": "scripts/gamora_join1_obs1_guard_2026_10_02.py",
                                                            "sha256": hashlib.sha256(Path(G.__file__).read_bytes()).hexdigest(),
                                                            "cell_check": guard},
           "salts": {}}
    for s in range(5):
        rows = res["salts"][str(s)]["rows"]
        out["salts"][str(s)] = {
            "leg_a_terminal": res["salts"][str(s)]["leg_a_terminal"], "raised": res["salts"][str(s)]["raised"],
            "rows_sha256": hashlib.sha256(json.dumps(rows, sort_keys=True, default=str).encode()).hexdigest(),
            "crit_by_wave_class": dict(CRIT[str(s)]), "round_site_hits_all_waves": dict(HITS[str(s)])}
    out["round_sites_scanned"] = [{"site": f"{v['file']}:{v['line']}", "text": v["text"], "int_round": v["int_round"]}
                                  for v in SITES.values()]
    out["round_site_files_sha256"] = {Path(f).name: hashlib.sha256(Path(f).read_bytes()).hexdigest()
                                      for f in sorted({k[0] for k in SITES})}
    # INFO-3: SlowChaos / SlowAether rows on the profiles the run built (last load inside the run)
    roster, pets = PROFILES[-1][0], PROFILES[-1][1]
    cen = {"n_roster_profiles": len(roster), "n_pet_profiles": len(pets), "rows_by_type": {}, "chaos_aether_rows": []}
    tc = Counter()
    for lab, d in (("roster", roster), ("pet", pets)):
        for rec, p in d.items():
            if p is None:
                continue
            for r in _rows_of(p):
                tc[str(r.damage_type)] += 1
                if r.damage_type in ("SlowChaos", "SlowAether"):
                    cen["chaos_aether_rows"].append([lab, rec, r.damage_type])
    cen["rows_by_type"] = dict(tc)
    out["divisor_reachability"] = cen
    json.dump(out, open(OUT, "w"), indent=1, sort_keys=True, default=str)
    print(f"[v115n] {ARM} guard_complete={guard['complete']} chaos_aether_rows={len(cen['chaos_aether_rows'])}", flush=True)


if __name__ == "__main__":
    main()
