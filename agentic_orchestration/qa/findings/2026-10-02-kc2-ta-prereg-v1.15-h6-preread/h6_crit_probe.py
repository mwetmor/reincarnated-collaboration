#!/usr/bin/env python3
"""H-6 (jack-ryan): TA-X-13 classifier probe. Runs the oracle of record (V311-FULL + graded_arm) for one arm and salts,
read-only; dumps every is_crit row's source/target ids and the id spaces (roster `w…`, player-summon `ps_…`, pets) so the
crit's SIDE is read off the oracle's own actor tables, not inferred from an id prefix. Usage: h6_crit_probe.py ARM OUT"""
import json, os, sys
from collections import Counter
OUT = os.path.abspath(sys.argv[2]); ARM = sys.argv[1]
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"; sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/admin/Games/reincarnated-engine/src"); os.chdir("/Users/admin/Games/reincarnated-engine/src")
from reincarnated.simulation.kc2 import run as kr
from reincarnated.simulation.kc2 import summons as sm
from reincarnated.simulation.scripts import gamora_kc2_c11_lethality_decomposition_2026_09_29 as c11
from reincarnated.simulation.scripts import gamora_kc2_play_c11a_fold_pricing_2026_09_30 as FP
from reincarnated.simulation.scripts import gamora_kc2_play_v3p11_oracle_2026_10_02 as V311
CUR = {"rec": False, "salt": None}
OUTD = {"crit": Counter(), "examples": [], "pet_id_examples": [], "actor_id_examples": [], "ps_ids_in_pet_actors": 0,
        "ps_ids_in_actors": 0, "player_summon_registry": Counter(), "event_types_by_ps_source": Counter()}
_ra = c11.run_arm
def _arm(runner, a, salt, period):
    CUR["rec"], CUR["salt"] = True, salt
    try: return _ra(runner, a, salt, period)
    finally: CUR["rec"] = False
c11.run_arm = _arm
_sw = kr.simulate_wave
def sw(*a, **kw):
    r = _sw(*a, **kw)
    if not CUR["rec"]: return r
    pets = {p["actor_id"]: p for p in r.pet_actors}
    acts = {x["actor_id"]: x for x in r.actors}
    if len(OUTD["pet_id_examples"]) < 5: OUTD["pet_id_examples"] += [[k, v.get("record_path"), v.get("owner_id")] for k, v in list(pets.items())[:2]]
    if len(OUTD["actor_id_examples"]) < 3: OUTD["actor_id_examples"] += list(acts)[:1]
    OUTD["ps_ids_in_pet_actors"] += sum(1 for k in pets if k.startswith(sm.SUMMON_ID_PREFIX))
    OUTD["ps_ids_in_actors"] += sum(1 for k in acts if k.startswith(sm.SUMMON_ID_PREFIX))
    for x in r.rows_as_dicts():
        s = str(x.get("source_id") or ""); t = str(x.get("target_id") or "")
        if s.startswith("ps_"): OUTD["event_types_by_ps_source"][str(x.get("event_type"))] += 1
        if x.get("is_crit"):
            side = ("player" if s == "player" else "pet_table" if s in pets else "roster_table" if s in acts
                    else "ps_prefix_not_in_tables" if s.startswith("ps_") else "other:" + s[:6])
            OUTD["crit"][f"src={side}|tgt={'player' if t == 'player' else t[:3]}"] += 1
            if len(OUTD["examples"]) < 8 and s.startswith("ps_"):
                OUTD["examples"].append({k: x.get(k) for k in ("event_type", "source_id", "target_id", "damage_source_tag", "is_crit", "amount", "damage_type")}
                                        | {"pet_row": pets.get(s)})
    return r
kr.simulate_wave = sw
res = V311.run_one("V311-FULL", (0, 1, 2, 3, 4), FP._period(), arm=ARM)
json.dump(OUTD, open(OUT, "w"), indent=1, default=str)
print(json.dumps({k: v for k, v in OUTD.items() if k != "examples"}, default=str)[:1500]); print(json.dumps(OUTD["examples"][:3], default=str)[:1500])
