#!/usr/bin/env python3
"""NON-PRODUCTION SCRATCH — 2026-07-30 GD L13 reference envelope (legolas).
Read-only. Re-resolves the G-5a ledger at averagePlayerLevel = 13 and validates
the composition rule against the MEASURED Primordian pool (15,822, from G-7 .gdc).
"""
import importlib.util, pathlib, sys, json

G5A = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
_s = importlib.util.spec_from_file_location("g5a", G5A)
R = importlib.util.module_from_spec(_s); _s.loader.exec_module(R)

APL = 13

def lvN(name):
    r = R.rec(f"records/proxies/{name}.dbr")
    lo = R.evaleq(r.get("minVarianceEquationNormal"), 0)
    hi = R.evaleq(r.get("maxVarianceEquationNormal"), 0)
    # equations are in averagePlayerLevel, not charLevel -> patch eval
    def ev(e):
        if not isinstance(e, str) or not e.strip(): return None
        return eval(e.replace("^", "**"), {"__builtins__": {}},
                    {"averagePlayerLevel": float(APL), "aPL": float(APL)})
    return ev(r.get("minVarianceEquationNormal")), ev(r.get("maxVarianceEquationNormal"))

if sys.argv[1] == "spawn":
    for n in ["lv1_weak","lv1_weak+","lv2_normal","lv2_normal+","lv3_strong","lv3_strong+",
              "lv4_champion","lv5_elitechampion","lv6_hero","lv7_uber hero","lv8_boss"]:
        try:
            lo,hi = lvN(n)
            print(f"{n:24s} min={lo!s:8s} max={hi!s:8s} -> int {int(lo) if lo else None}-{int(hi) if hi else None}")
        except KeyError:
            print(f"{n:24s} MISSING")

elif sys.argv[1] == "primordian":
    # MEASURED anchor: play_stats greatestMonsterKilledLifeAndMana = 15822 at player L13
    p = "records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr"
    m = R.rec(p)
    print("charLevel eq:", m.get("charLevel"), "| classification:", m.get("monsterClassification"))
    print("bio:", m.get("characterAttributeEquations"))
    for spawn in range(13, 20):
        r = R.resolve(p, spawn)
        mana = r["base"].get("characterMana") or 0.0
        print(f"spawn={spawn} charLevel={r['charLevel']:3d} HP={r['hp']:9.1f} "
              f"mana={mana:7.1f} HP+mana={r['hp']+mana:9.1f}  "
              f"dmg={r['dmg_min']:.0f}-{r['dmg_max']:.0f} armor={r['armor']:.0f} "
              f"OA={r['OA']:.0f} DA={r['DA']:.0f}")

elif sys.argv[1] == "table":
    lvl = int(sys.argv[2])
    for p in sys.argv[3:]:
        try: r = R.resolve(p, lvl)
        except KeyError: print(f"MISSING\t{p}"); continue
        mana = r["base"].get("characterMana") or 0.0
        flags = ("W" if r["weaponEquipped"] else "")+("C" if r["dmg_maxClamped"] else "")
        print(f"{R.name_of(r)}\t{p.split('/')[-1]}\tspawn={lvl}\tcharL={r['charLevel']}\t"
              f"HP={r['hp']:.0f}\tHP+mana={r['hp']+mana:.0f}\tdmg={r['dmg_min']:.0f}-{r['dmg_max']:.0f}\t"
              f"armor={r['armor']:.0f}\tOA={r['OA']:.0f}\tDA={r['DA']:.0f}\t"
              f"aspd={r['attackSpeed_eff']:.2f}\trun={r['runSpeed_eff']:.2f}\t"
              f"elem={r.get('dmg_elemental','')}\tctrl={r.get('controller')}\t{flags}")

elif sys.argv[1] == "dump":
    for p in sys.argv[2:]:
        r = R.rec(p)
        print(f"===== {p}")
        for k in sorted(r): print(f"  {k} = {r[k]}")
