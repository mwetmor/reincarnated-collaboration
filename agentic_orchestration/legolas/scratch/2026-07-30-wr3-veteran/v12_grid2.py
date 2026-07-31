#!/usr/bin/env python3
"""V12 - the grid, extended: PRE-mitigation as well as POST, the third cl-16 reading surfaced by
the U-4 spawn-vs-final ambiguity, and explicit pin re-basing. READ-ONLY."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
a=ArzArchive(ROOT/"database/database.arz"); R=lambda n: a.read_record(n)
ARMOR_ABSORB=0.70
MIT={"Physical":1-ARMOR_ABSORB,"Cold":0.86}
POOL=759.0
RING=R("records/skills/nonplayerskills/bossskills/primordian_frigidring.dbr")
WAVE=R("records/skills/nonplayerskills/bossskills/primordian_wave.dbr")
BLIZ=R("records/skills/nonplayerskills/heroskills/chillbane_blizzard.dbr")
ARMR=R("records/skills/nonplayerskills/bossskills/primordian_icearmor.dbr")
PASS=R("records/skills/nonplayerskills/bossskills/primordian_passive.dbr")
MELE=R("records/skills/nonplayerskills/passive/damagebase_physical04.dbr")
AB05=R("records/skills/nonplayerskills/passive/armorbase05.dbr")
DTA =R("records/skills/nonplayerskills/passive/damage_totaladjuster.dbr")
PAK =R("records/game/balancingadjustment_mp+difficulty_enemies01.dbr")
VET =R("records/game/balancingadjustment_challengemode_enemies01.dbr")
def g(rec,k,rank):
    v=rec.get(k)
    if v is None: return 0.0
    if isinstance(v,list): return float(v[min(rank-1,len(v)-1)])
    return float(v)
PAKT=PAK['offensiveTotalDamageModifier'][0]; PAKSC=PAK['offensiveSlowColdModifier'][0]
VT=VET['offensiveTotalDamageModifier']; VP=VET['offensivePhysicalModifier']

def factors(cl,vet):
    pt=g(AB05,'offensiveTotalDamageModifier',cl)+g(DTA,'offensiveTotalDamageModifier',(cl//25)+2)
    pp=g(AB05,'offensivePhysicalModifier',cl)+g(DTA,'offensivePhysicalModifier',(cl//25)+2)
    if vet=='pooled': return (1+(pt+VT)/100)*(1+PAKT/100), 1+(pp+VP)/100
    if vet=='own':    return (1+pt/100)*(1+PAKT/100)*(1+VT/100), (1+pp/100)*(1+VP/100)
    return (1+pt/100)*(1+PAKT/100), 1+pp/100

CELLS=[("cl13/r4 VET-own",13,4,'own'),("cl13/r4 VET-pool",13,4,'pooled'),
       ("cl16/r5 VET-own",16,5,'own'),("cl16/r5 VET-pool",16,5,'pooled'),
       ("cl18/r5 VET-own",18,5,'own'),("cl18/r5 VET-pool",18,5,'pooled'),
       ("cl18/r5 NO-VET",18,5,'none')]

def kit(cl,rk,vet,mitigate,ice_on):
    F,PM=factors(cl,vet); ice=g(ARMR,'offensiveColdModifier',rk) if ice_on else 0.0
    mp=MIT["Physical"] if mitigate else 1.0
    mc=MIT["Cold"]     if mitigate else 1.0
    def blk(p,c): return p*mp*PM*F + c*mc*(1+ice/100)*F
    o={}
    p=g(RING,'offensivePhysicalMin',rk); c=g(RING,'offensiveColdMin',rk); b=blk(p,c)
    o["nova prong, close band x2 (50% ea)"]=b*1.0
    o["nova prong, mid band (100%)"]=b
    o["nova prong, FAR band (140%)"]=b*1.4
    o["nova cold DoT / 2 s"]=g(RING,'offensiveSlowColdMin',rk)*mc*(1+ice/100)*F*(1+PAKSC/100)
    p=g(WAVE,'offensivePhysicalMin',rk); c=g(WAVE,'offensiveColdMin',rk)
    o["wave impact"]=blk(p,c)
    o["wave cold DoT / 3 s"]=g(WAVE,'offensiveSlowColdMin',rk)*mc*(1+ice/100)*F*(1+PAKSC/100)
    p=g(BLIZ,'offensivePhysicalMin',rk); c=g(BLIZ,'offensiveColdMin',rk)
    o["blizzard per drop"]=blk(p,c)
    o["melee swing MIN"]=blk(g(MELE,'offensivePhysicalMin',cl), g(PASS,'offensiveColdMin',rk))
    o["melee swing MAX"]=blk(g(MELE,'offensivePhysicalMax',cl), g(PASS,'offensiveColdMax',rk))
    return o
ORDER=["nova prong, close band x2 (50% ea)","nova prong, mid band (100%)","nova prong, FAR band (140%)",
       "nova cold DoT / 2 s","wave impact","wave cold DoT / 3 s","blizzard per drop",
       "melee swing MIN","melee swing MAX"]

for mitigate in (True,False):
  for ice_on in (True,False):
    tag=("POST-mitigation (vs measured gear: armor 337 = 70% phys absorb, cold resist 14)" if mitigate
         else "PRE-mitigation  (raw outgoing - the units the charter's melee band 43.1-60.8 uses)")
    print("="*136)
    print(f"{tag}   |   icearmor {'UP (+cold rider)' if ice_on else 'DOWN'}")
    print("="*136)
    T={c[0]:kit(c[1],c[2],c[3],mitigate,ice_on) for c in CELLS}
    print(f"  {'':36s}"+" ".join(f"{c[0]:>16s}" for c in CELLS))
    for k in ORDER:
        print(f"  {k:36s}"+" ".join(f"{T[c[0]][k]:16.2f}" for c in CELLS))
    if mitigate:
        w={c[0]:max(v for kk,v in T[c[0]].items() if 'DoT' not in kk) for c in CELLS}
        print(f"  {'WORST SINGLE HIT':36s}"+" ".join(f"{w[c[0]]:16.2f}" for c in CELLS))
        print(f"  {'/ player pool 759':36s}"+" ".join(f"{100*w[c[0]]/POOL:15.1f}%" for c in CELLS))
        print(f"  {'/ measured worst 260.498':36s}"+" ".join(f"{w[c[0]]/260.498:16.3f}" for c in CELLS))
    print()

print("="*136); print("PIN RE-BASING - the charter's ratified pins under each cell"); print("="*136)
print("  (A-WAVE-1 / A-BLIZ-1 are POST-mitigation with icearmor's cold rider ON - that is how the")
print("   ratified triples 345.32/258.99/91.37 and 173.61/130.21/45.93 were built and reproduced.)")
print()
print(f"  {'pin':30s}{'charter S1 col':>15s}{'charter S2 col':>15s}"+" ".join(f"{c[0]:>16s}" for c in CELLS))
def pin(key,ice):
    return {c[0]: kit(c[1],c[2],c[3],True,ice)[key] for c in CELLS}
rows=[("A-NOVA-2  far band (140%)","nova prong, FAR band (140%)",False,269.66,None),
      ("A-NOVA-2  mid band (100%)","nova prong, mid band (100%)",False,192.61,None),
      ("A-WAVE-1  impact","wave impact",True,258.99,91.37),
      ("A-BLIZ-1  per drop","blizzard per drop",True,130.21,45.93)]
for lab,key,ice,s1,s2 in rows:
    d=pin(key,ice)
    print(f"  {lab:30s}{s1:15.2f}{(f'{s2:15.2f}' if s2 else ' '*15)}"+" ".join(f"{d[c[0]]:16.2f}" for c in CELLS))
print()
mb=[(c[0], kit(c[1],c[2],c[3],False,False)["melee swing MIN"], kit(c[1],c[2],c[3],False,False)["melee swing MAX"]) for c in CELLS]
print(f"  MELEE BAND (pre-mitigation, icearmor down) - charter band 43.1-60.8")
for n,lo,hi in mb: print(f"     {n:20s} {lo:7.2f} - {hi:7.2f}")
