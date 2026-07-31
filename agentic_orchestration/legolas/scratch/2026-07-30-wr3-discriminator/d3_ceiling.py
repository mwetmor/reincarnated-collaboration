#!/usr/bin/env python3
"""D3 - absolute single-event payload ceiling across the L13-reachable monster-skill corpus,
composed under S0_NONE / S1_PAK / S2_FULL. READ-ONLY."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS=[ROOT/"database/database.arz",ROOT/"gdx1/database/GDX1.arz",ROOT/"gdx2/database/GDX2.arz",ROOT/"gdx3/database/GDX3.arz"]
ars=[(p.name,ArzArchive(p)) for p in ARZS]

# instantaneous damage components (NOT the Slow* DoT family)
COMPS=["Physical","Pierce","Fire","Cold","Lightning","Aether","Chaos","Life","Magical","Elemental","Poison"]
def payload(rec, rank):
    """max instantaneous payload at 1-based rank; uses Max where it exists and is non-zero, else Min."""
    tot=0.0; parts={}
    for c in COMPS:
        for suf in ("Max","Min"):
            k=f"offensive{c}{suf}"
            if k not in rec: continue
            v=rec[k]
            if isinstance(v,list):
                v=v[min(rank-1,len(v)-1)]
            if v: parts[c]=max(parts.get(c,0.0),float(v))
    # Poison in GD is a DoT (has DurationMin); drop it from the instantaneous sum
    inst={k:v for k,v in parts.items() if k!="Poison"}
    return sum(inst.values()), inst

MAXRANK=6   # charLevel/4+1 at charLevel<=19  ->  rank 5; +1 headroom
rows=[]
seen=set()
for nm,a in ars:
    for r in a.records:
        if not r.startswith("records/skills/nonplayerskills/"): continue
        if r in seen: continue
        seen.add(r)
        rec=a.read_record(r)
        cls=rec.get("Class") or ""
        if not str(cls).startswith("Skill_"): continue
        best=0.0; bestrank=None; bestparts=None
        for rk in range(1,MAXRANK+1):
            t,p=payload(rec,rk)
            if t>best: best,bestrank,bestparts=t,rk,p
        if best>0: rows.append((best,r,bestrank,bestparts,cls,nm))
rows.sort(reverse=True, key=lambda x:x[0])

# --- regime factors (charLevel-dependent pool damper + pak) ---
def fac(regime, cl, tier):
    """tier: 'trash' -> armorbase01/02 (-56+rank); 'boss' -> armorbase03-06 (-91+rank)"""
    if regime=="S0": return 1.0
    if regime=="S1": return 0.75
    ab = (-56+cl) if tier=="trash" else (-91+cl)
    adj = 8.0
    return (1+(ab+adj)/100.0)*0.75

print("="*90)
print("REGIME FACTORS  (pool additive, pak multiplicative -- envelope-note operator)")
print("="*90)
for tier,cl in (("trash",13),("trash",16),("boss",16),("boss",18),("boss",19)):
    print(f"  {tier:5s} charLevel {cl:2d}:  S0 x1.0000   S1 x0.7500   S2 x{fac('S2',cl,tier):.4f}")

TARGETS=[("greatestDamageReceived",260.498),("lastHitBy",273.704)]
print()
print("="*90)
print("INVERSE ARITHMETIC -- raw single-event payload REQUIRED to land the measured numbers")
print("="*90)
for label,val in TARGETS:
    print(f"  {label} = {val}")
    for tier,cl in (("trash",13),("boss",18)):
        for reg in ("S0","S1","S2"):
            f=fac(reg,cl,tier)
            print(f"      {reg}  {tier:5s} cl{cl}: needs raw {val/f:8.1f}   (factor x{f:.4f})")
    print()

print("="*90)
print("TOP 20 RAW SINGLE-EVENT PAYLOADS, whole nonplayerskills corpus, ranks 1-6")
print("="*90)
for best,r,rk,parts,cls,nm in rows[:20]:
    ps=" ".join(f"{k}{v:.0f}" for k,v in sorted(parts.items(),key=lambda x:-x[1]))
    print(f"  {best:8.1f}  r{rk}  {r.split('nonplayerskills/')[-1]:58s} {ps}")

print()
print("="*90)
print("PRIMORDIAN + WARDEN + PLAGUE WALKER kit, raw and composed")
print("="*90)
KIT=[("primordian_frigidring","records/skills/nonplayerskills/bossskills/primordian_frigidring.dbr",5,"boss",18,1.4),
     ("primordian_wave","records/skills/nonplayerskills/bossskills/primordian_wave.dbr",5,"boss",18,1.0),
     ("chillbane_blizzard","records/skills/nonplayerskills/heroskills/chillbane_blizzard.dbr",5,"boss",18,1.0),
     ("aethersmash_warden","records/skills/nonplayerskills/attackradius/aethersmash_warden.dbr",5,"boss",19,1.0),
     ("aetherwave_warden","records/skills/nonplayerskills/path/aetherwave_warden.dbr",5,"boss",19,1.0),
     ("aetherarc_warden","records/skills/nonplayerskills/path/aetherarc_warden.dbr",5,"boss",19,1.0),
     ("aetherstreak_warden2","records/skills/nonplayerskills/path/aetherstreak_warden2.dbr",5,"boss",19,1.0),
     ("wardenspikes1","records/skills/nonplayerskills/bossskills/wardenspikes1.dbr",5,"boss",19,1.0),
     ("zombie_barf (PlagueWalker)","records/skills/nonplayerskills/path/zombie_barf.dbr",4,"trash",13,1.0),
     ("poisongib_zombie (PW)","records/skills/nonplayerskills/attackprojectile/poisongib_zombie.dbr",4,"trash",13,1.0),
     ("acidpool1 (PW)","records/skills/nonplayerskills/aoe/acidpool1.dbr",4,"trash",13,1.0)]
def get(n):
    for nm,a in ars:
        if n in a.records: return a.read_record(n)
    return None
print(f"  {'ability':30s} {'raw':>8s} {'band':>5s} {'S0':>8s} {'S1':>8s} {'S2':>8s}   components")
for lbl,rn,rk,tier,cl,band in KIT:
    rec=get(rn)
    if rec is None: print(f"  {lbl:30s}  RECORD NOT FOUND {rn}"); continue
    raw,parts=payload(rec,rk)
    ps=" ".join(f"{k}{v:.0f}" for k,v in sorted(parts.items(),key=lambda x:-x[1]))
    print(f"  {lbl:30s} {raw:8.1f} {band:5.2f} {raw*band:8.1f} {raw*0.75*band:8.1f} {raw*fac('S2',cl,tier)*band:8.1f}   {ps}")
