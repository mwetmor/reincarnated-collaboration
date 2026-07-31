#!/usr/bin/env python3
"""D8 - POST-MITIGATION reachable ceiling at player level 13, under S0/S1/S2. READ-ONLY.
Mitigation model reconciles the conductor's 269.66 exactly (see header check)."""
import sys, pathlib, re
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
a=ArzArchive(ROOT/"database/database.arz")

# --- player mitigation, M from the equipped set (d7) ---
ARMOR_ABSORB=0.70                       # armor 337 >= every physical component in range
MIT={"Physical":1-ARMOR_ABSORB,"Cold":0.86,"Aether":0.82,"Chaos":0.92,"Life":0.92,
     "Poison":0.75,"Bleeding":0.90,"Fire":1.00,"Lightning":1.00,"Pierce":1.00,
     "Magical":1.00,"Elemental":1.00}
COMPS=list(MIT)

print("RECONCILIATION CHECK vs conductor's handed figure")
p=148*0.75*MIT["Physical"]; c=247*0.75*MIT["Cold"]
print(f"  primordian_frigidring r5 far-band, S1_PAK, post-mitigation = ({p:.2f}+{c:.2f}) x1.4 = {(p+c)*1.4:.2f}")
print(f"  conductor's handed value                                   = 269.66   -> {'MATCH' if abs((p+c)*1.4-269.66)<0.2 else 'MISMATCH'}")
print()

def inst(rec,rank):
    p={}
    for c in COMPS:
        for suf in ("Max","Min"):
            k=f"offensive{c}{suf}"
            if k not in rec: continue
            v=rec[k]
            if isinstance(v,list): v=v[min(rank-1,len(v)-1)]
            if v: p[c]=max(p.get(c,0.0),float(v))
    if "Poison" in p: del p["Poison"]          # poison is a DoT in GD
    return p
def ev(expr,cl):
    if expr is None: return None
    try: return int(eval(str(expr).replace("charLevel",str(cl))))
    except Exception: return None
SPAWN={"Common":13,"Champion":14,"Hero":16,"Quest":17}

rows=[]
for r in a.records:
    if not r.startswith("records/creatures/enemies/"): continue
    if a.record_type(r)!="Monster": continue
    rec=a.read_record(r)
    cls=str(rec.get('monsterClassification') or "Common")
    cl=ev(rec.get('charLevel'), SPAWN.get(cls,13)) or SPAWN.get(cls,13)
    if cl>21: continue                                   # not reachable at player level 13
    ab=None
    for i in range(1,25):
        s=rec.get(f'skillName{i}')
        if s:
            m=re.search(r'armorbase(\d\d)',s)
            if m: ab=int(m.group(1))
    tier='trash' if ab in (1,2) else ('boss' if ab else None)
    if tier is None: continue
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
        band=1.4 if 'ring' in s or 'nova' in s else 1.0     # far-band bonus where a ring/nova exists
        s0=sum(v*MIT[k] for k,v in parts.items())*band
        if best is None or s0>best[0]: best=(s0,s,rk,parts,band)
    if best: rows.append((best[0],best[0]*0.75,best[0]*f2,r,best[1],best[2],cls,cl,ab,best[4]))
rows.sort(reverse=True,key=lambda x:x[1])   # rank by S1

print("="*128)
print("POST-MITIGATION single-event ceiling, base-campaign creatures reachable at player level 13")
print("  measured targets:  greatestDamageReceived 260.498   |   lastHitBy 273.704")
print("="*128)
print(f"  {'S0':>7s} {'S1':>7s} {'S2':>7s}  {'cls':9s} {'cL':>3s} {'AB':>2s}  monster  <- ability")
for s0,s1,s2,r,s,rk,cls,cl,ab,band in rows[:16]:
    print(f"  {s0:7.1f} {s1:7.1f} {s2:7.1f}  {cls:9s} {cl:3d} {ab:2d}  {r.split('enemies/')[-1]:40s} <- {s.split('nonplayerskills/')[-1]:38s} r{rk}{' x1.4' if band>1 else ''}")
print()
for lab,idx in (("S0_NONE",0),("S1_PAK",1),("S2_FULL",2)):
    ceil=max(x[idx] for x in rows)
    who=[x for x in rows if x[idx]==ceil][0]
    for tgt in (260.498,273.704):
        ok = ceil>=tgt
        print(f"  {lab:8s} ceiling {ceil:7.1f}  vs {tgt:7.3f}  ->  {'REACHABLE' if ok else 'UNREACHABLE'}"
              + (f"   (ceiling = {who[3].split('enemies/')[-1]})" if tgt==260.498 else ""))
