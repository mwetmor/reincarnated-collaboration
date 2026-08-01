#!/usr/bin/env python3
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARCS=[("sm_mod","mods/survivalmode/database/SurvivalMode.arz"),("sm1","survivalmode1/database/SurvivalMode1.arz"),
      ("sm2","survivalmode2/database/SurvivalMode2.arz"),("sm3","survivalmode3/database/SurvivalMode3.arz")]
A={k:ArzArchive(ROOT/p) for k,p in ARCS}
base=ArzArchive(ROOT/"database/database.arz")
def res(path):
    out=None
    for k,_ in ARCS:
        if path in A[k].records: out=(k,A[k].read_record(path))
    if out is None and path in base.records: out=("BASE",base.read_record(path))
    return out

print("### Crucible wave-06 spawn pools, tiers 13/14")
for tier in (13,14):
    grand=[0,0]
    for pp in range(1,7):
        r=res(f"records/proxies/tier{tier:02d}waves/proxy_w06_p{pp:02d}a.dbr")
        if not r: continue
        k,rec=r
        pools=[(rec[f"pool{i}"],rec.get(f"weight{i}",0)) for i in range(1,7) if rec.get(f"pool{i}")]
        mn=[];mx=[]
        for pl,w in pools:
            _,po=res(pl); mn.append(po.get('spawnMin',0)); mx.append(po.get('spawnMax',0))
        print(f" t{tier} p{pp:02d}[{k}] npools={len(pools)} sMin={mn} sMax={mx}")
        grand[0]+=min(mn); grand[1]+=max(mx)
    print(f" --> tier{tier} wave06 Aspirant(Normal) floor={grand[0]} ceiling={grand[1]}\n")

print("### balancingadjustment arrays, all 3 survival difficulties + campaign mp reference")
keys=("spawnMinAdj","spawnMaxAdj","spawnChampionMinAdj","spawnChampionMaxAdj","totalDamageModifier","offensiveAbilityModifier","characterLifeModifier","defensiveAbilityModifier")
for n,tag in [("01","Aspirant/Normal"),("02","Challenger/Elite"),("03","Gladiator/Ultimate")]:
    r=res(f"records/game/balancingadjustment_survivalmode_enemies{n}.dbr")
    k,rec=r
    print(f"\n-- {tag} [{k}] nfields={len(rec)}")
    for key in keys:
        v=rec.get(key)
        if v is None: continue
        if isinstance(v,list):
            print(f"   {key}: len={len(v)}  idx[0,29,49,99,149,169,199] = {[v[i] for i in (0,29,49,99,149,169,199) if i<len(v)]}")
        else: print(f"   {key} = {v}")
r=res("records/game/balancingadjustment_mp+difficulty_enemies01.dbr")
if r:
    k,rec=r; print(f"\n-- CAMPAIGN mp+difficulty_enemies01 [{k}] nfields={len(rec)}")
    for key in keys:
        v=rec.get(key)
        if isinstance(v,list): print(f"   {key}: len={len(v)} idx[0,29,49,99,149,169,199]={[v[i] for i in (0,29,49,99,149,169,199) if i<len(v)]}")
        elif v is not None: print(f"   {key} = {v}")
