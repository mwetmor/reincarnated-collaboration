#!/usr/bin/env python3
"""D9 - S2_FULL's BEST CASE: rank by S2, add the 8%-chance +35% physical proc and a generous
weapon allowance, and ask whether S2 can reach 260.498 at all. READ-ONLY."""
import sys, pathlib, re
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
a=ArzArchive(ROOT/"database/database.arz")
ARMOR_ABSORB=0.70
MIT={"Physical":1-ARMOR_ABSORB,"Cold":0.86,"Aether":0.82,"Chaos":0.92,"Life":0.92,
     "Bleeding":0.90,"Fire":1.00,"Lightning":1.00,"Pierce":1.00,"Magical":1.00,"Elemental":1.00}
COMPS=list(MIT)
WEAPON_RAW=80.0     # generous 1h weapon physical roll at monster level ~16-21, x1.3 weaponScale
PHYS_PROC=1.35      # damagebase_physical0N offensivePhysicalModifier, 8% chance

def inst(rec,rank):
    p={}
    for c in COMPS:
        for suf in ("Max","Min"):
            k=f"offensive{c}{suf}"
            if k not in rec: continue
            v=rec[k]
            if isinstance(v,list): v=v[min(rank-1,len(v)-1)]
            if v: p[c]=max(p.get(c,0.0),float(v))
    return p
def ev(e,cl):
    if e is None: return None
    try: return int(eval(str(e).replace("charLevel",str(cl))))
    except Exception: return None
SPAWN={"Common":13,"Champion":14,"Hero":16,"Quest":17,"Boss":17}
rows=[]
for r in a.records:
    if not r.startswith("records/creatures/enemies/"): continue
    if a.record_type(r)!="Monster": continue
    rec=a.read_record(r)
    cls=str(rec.get('monsterClassification') or "Common")
    cl=ev(rec.get('charLevel'), SPAWN.get(cls,13)) or SPAWN.get(cls,13)
    if cl>21: continue
    ab=None
    for i in range(1,25):
        s=rec.get(f'skillName{i}')
        if s:
            m=re.search(r'armorbase(\d\d)',s)
            if m: ab=int(m.group(1))
    if ab is None: continue
    tier='trash' if ab in (1,2) else 'boss'
    dm=(-56+cl) if tier=='trash' else (-91+cl)
    f2=(1+(dm+8)/100.0)*0.75
    best=None
    for i in range(1,25):
        s=rec.get(f'skillName{i}')
        if not s or s not in a.records: continue
        srec=a.read_record(s)
        if not str(srec.get('Class','')).startswith('Skill_'): continue
        rk=max(1, ev(rec.get(f'skillLevel{i}'), cl) or 1)
        parts=inst(srec,rk)
        if not parts: continue
        band=1.4 if ('ring' in s or 'nova' in s) else 1.0
        parts=dict(parts)
        parts["Physical"]=parts.get("Physical",0.0)*PHYS_PROC + WEAPON_RAW
        val=sum(v*MIT[k] for k,v in parts.items())*band
        if best is None or val*f2>best[0]: best=(val*f2, val*0.75, val, s, rk, band)
    if best: rows.append((best[0],best[1],best[2],r,best[3],best[4],cls,cl,ab))
rows.sort(reverse=True,key=lambda x:x[0])
print("="*126)
print("S2_FULL BEST CASE  (ranked by S2; +35% physical proc AND +80 raw weapon granted to EVERY entry)")
print("  targets: greatestDamageReceived 260.498 | lastHitBy 273.704")
print("="*126)
print(f"  {'S2':>7s} {'S1':>7s} {'S0':>7s}  {'cls':9s} {'cL':>3s} {'AB':>2s}  monster <- ability")
for s2,s1,s0,r,s,rk,cls,cl,ab in rows[:14]:
    print(f"  {s2:7.1f} {s1:7.1f} {s0:7.1f}  {cls:9s} {cl:3d} {ab:2d}  {r.split('enemies/')[-1]:38s} <- {s.split('nonplayerskills/')[-1]:38s} r{rk}")
c2=max(x[0] for x in rows); c1=max(x[1] for x in rows); c0=max(x[2] for x in rows)
print()
print(f"  S2_FULL best-case ceiling = {c2:7.1f}  -> 260.498 {'REACHABLE' if c2>=260.498 else 'UNREACHABLE'} | 273.704 {'REACHABLE' if c2>=273.704 else 'UNREACHABLE'}")
print(f"  S1_PAK  best-case ceiling = {c1:7.1f}  -> 260.498 {'REACHABLE' if c1>=260.498 else 'UNREACHABLE'} | 273.704 {'REACHABLE' if c1>=273.704 else 'UNREACHABLE'}")
print(f"  S0_NONE best-case ceiling = {c0:7.1f}  -> 260.498 {'REACHABLE' if c0>=260.498 else 'UNREACHABLE'} | 273.704 {'REACHABLE' if c0>=273.704 else 'UNREACHABLE'}")
print()
print(f"  shortfall of S2 against greatestDamageReceived: {260.498-c2:+.1f}  ({100*(260.498-c2)/260.498:+.1f}% of the measured value)")
