#!/usr/bin/env python3
"""PART C re-seat. Multiplier-free: every w152 multiplier cancels in a within-wave HP ratio,
so anchor on galadriel's MEASURED Haraxis HP and solve each candidate's required level."""
import sys, csv, math
sys.path.insert(0, "."); import lib2
E2 = lib2.E2
def ev(e, L): return eval(e.replace("^","**").replace("charLevel",f"({L})"), {"__builtins__":{}}, {})
def info(p):
    r,_ = E2.merged(p)
    if not r or r.get("Class")!="Monster": return None
    bp = r.get("characterAttributeEquations")
    if not bp: return None
    b,_ = E2.merged(bp if isinstance(bp,str) else bp[0])
    if not b or "characterLife" not in b: return None
    return b["characterLife"], r.get("charLevel","charLevel*1"), r.get("monsterClassification")

HAR_HP, PAIR = 2_050_807, (42798, 43548)
heq, hcl, _ = info("records/creatures/enemies/boss&quest/aetherialfleshshaper_haraxis.dbr")

# w152 roster (pools only) + the summon bodies the L-58 chain actually produces on w152
rows=[r for r in csv.DictReader(open("/Users/admin/Games/reincarnated-engine/data/kc2/pe6_crucible_wave_pools_v2.csv")) if int(r["global_wave"])==152]
mons=set()
for r in rows:
    for c in ("roster_records","champ_records"):
        for x in (r.get(c) or "").split("|"):
            if x.strip(): mons.add(x.strip().lower())
print("w152 rostered records:", len(mons))
print("chthonian* on w152 roster:", sorted(p for p in mons if "chthonian" in p) or "NONE")
SUM=["swampcrab_a00_summon","swampcrab_b01_summon","swampcrab_c01_summon","springscrab_a00_summon",
     "aetherialcorruption_c01_summon","aetherialcorruption_b02_summon","aetherialcolossus_c02_summon",
     "trap_brambletrap_a01","trap_icespike_hero_a01","trap_lightningspike_hero_a01"]
for s in SUM:
    p="records/creatures/enemies/%s.dbr"%s
    if p in E2.idx: mons.add(p)

# spawn-count adjusters at w152
sa,_=E2.merged("records/game/balancingadjustment_survivalmode_enemies03.dbr")
print("w152 spawn adj -> spawnMinAdj=%s spawnMaxAdj=%s spawnChampionMinAdj=%s spawnChampionMaxAdj=%s"
      % (sa["spawnMinAdj"][151], sa["spawnMaxAdj"][151], sa["spawnChampionMinAdj"][151], sa["spawnChampionMaxAdj"][151]))

print("\n=== required level per candidate, for Haraxis draw 103.0 (eff 108) and 103.99 (eff 108.99) ===")
print(f"{'candidate':<52}{'tier':<10}{'p':>5}  req.L @108   req.L @108.99   lv6_hero[104,105]?")
for p in sorted(mons):
    g = info(p)
    if not g: continue
    eq, cl, tier = g
    if tier != "Common": continue
    out=[]
    for hL in (108.0, 108.99):
        hbase = ev(heq, hL)
        for t in PAIR:
            need = hbase * t / HAR_HP
            # invert ((L*k)^e)+c
            m=eq.replace("^","**")
            try:
                import re
                mm=re.match(r"\(\(charLevel\*([\d.]+)\)\*\*([\d.]+)\)\+([\d.]+)$", m)
                if not mm: out.append(None); continue
                k,e,c=map(float,mm.groups())
                Leff=((need-c)**(1/e))/k
                base_draw = Leff - (float(cl.split("+")[1]) if "+" in cl else 0.0)
                out.append(base_draw)
            except Exception: out.append(None)
    if any(o is None for o in out): continue
    ok = any(104.0 <= o <= 105.0 for o in out)
    pex = eq.split("**")[-1].split(")")[0] if "**" in eq.replace("^","**") else "?"
    print(f"{p.replace('records/creatures/enemies/',''):<52}{tier:<10}{pex:>5}  {out[0]:6.2f}/{out[1]:6.2f}   {out[2]:6.2f}/{out[3]:6.2f}   {'YES' if ok else 'no'}")
