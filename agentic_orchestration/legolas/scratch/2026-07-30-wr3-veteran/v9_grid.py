#!/usr/bin/env python3
"""V9 - THE FOUR-CELL PRIMORDIAN PAYLOAD GRID.
{boss cl 13 / rank 4, boss cl 18 / rank 5} x {Veteran own-stage, Veteran pooled}, under S2_FULL.
Post-mitigation against the measured referent gear (d7/d8 model). READ-ONLY.

Operator (reproduces the ratified pins A-WAVE-1 / A-BLIZ-1 to 0.01 - see the header check):
    delivered = raw x MIT[component] x (1 + comp_mod/100) x TOTAL_FACTOR
    TOTAL_FACTOR = (1 + sum(pool offensiveTotalDamageModifier)/100) x (1 + pak/100) [x (1+vet/100)]
"""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
a=ArzArchive(ROOT/"database/database.arz")
R=lambda n: a.read_record(n)

# ---------------- player mitigation, M from the equipped set (d7) ----------------
ARMOR_ABSORB=0.70
MIT={"Physical":1-ARMOR_ABSORB,"Cold":0.86,"Aether":0.82,"Chaos":0.92,"Life":0.92,
     "Poison":0.75,"Bleeding":0.90,"Fire":1.00,"Lightning":1.00,"Pierce":1.00}
POOL_HUMAN=759.0

# ---------------- records ----------------
BOSS=R("records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr")
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

PAK_TOTAL   = PAK['offensiveTotalDamageModifier'][0]     # -25 Normal/1p
PAK_SLOWCOLD= PAK['offensiveSlowColdModifier'][0]        # -38
VET_TOTAL   = VET['offensiveTotalDamageModifier']        # +40
VET_PHYS    = VET['offensivePhysicalModifier']           # +10

def regime(cl, veteran):
    """veteran in {'none','own','pooled'}; returns (TOTAL_FACTOR, phys_mod%, dot_cold_mod%)"""
    pool_total = g(AB05,'offensiveTotalDamageModifier',cl) + g(DTA,'offensiveTotalDamageModifier',(cl//25)+2)
    pool_phys  = g(AB05,'offensivePhysicalModifier',cl)    + g(DTA,'offensivePhysicalModifier',(cl//25)+2)
    vt = 0.0; vp = 0.0
    if veteran=='pooled': pool_total += VET_TOTAL; pool_phys += VET_PHYS
    if veteran=='own':    vt = VET_TOTAL;          vp = VET_PHYS
    f = (1+pool_total/100.0)*(1+PAK_TOTAL/100.0)*(1+vt/100.0)
    return f, pool_phys+vp+ (pool_phys*0 if veteran!='own' else 0.0), PAK_SLOWCOLD, pool_total, vt, vp

def phys_mult(cl, veteran):
    pool_phys = g(AB05,'offensivePhysicalModifier',cl) + g(DTA,'offensivePhysicalModifier',(cl//25)+2)
    if veteran=='pooled': return 1+(pool_phys+VET_PHYS)/100.0
    if veteran=='own':    return (1+pool_phys/100.0)*(1+VET_PHYS/100.0)
    return 1+pool_phys/100.0

def deliver(raw, comp, cl, veteran, extra_mod=0.0):
    f,_,_,_,_,_ = regime(cl,veteran)
    m = MIT[comp]*(1+extra_mod/100.0)*f
    if comp=="Physical": m *= phys_mult(cl,veteran)
    return raw*m

# ---------------- HEADER CHECK: reproduce the ratified pins ----------------
print("="*112)
print("HEADER CHECK - reproduce the charter's ratified pins from records + gear (no Veteran, cl 18, rank 5)")
print("="*112)
for lbl,rec,rk in (("A-WAVE-1",WAVE,5),("A-BLIZ-1",BLIZ,5)):
    p=g(rec,'offensivePhysicalMin',rk); c=g(rec,'offensiveColdMin',rk)
    ice=g(ARMR,'offensiveColdModifier',5)
    s0 = p*MIT["Physical"] + c*MIT["Cold"]*(1+ice/100)
    s1 = s0*(1+PAK_TOTAL/100)
    s2 = deliver(p,"Physical",18,'none') + deliver(c,"Cold",18,'none',ice)
    print(f"  {lbl}: S0 {s0:7.2f}   S1 {s1:7.2f}   S2 {s2:7.2f}")
print("  charter: A-WAVE-1 345.32 / 258.99 / 91.37   |   A-BLIZ-1 173.61 / 130.21 / 45.93")
p=g(RING,'offensivePhysicalMin',5); c=g(RING,'offensiveColdMin',5)
print(f"  A-NOVA-2 S1_PAK far band (x1.4, no icearmor) = "
      f"{(p*MIT['Physical']+c*MIT['Cold'])*(1+PAK_TOTAL/100)*1.4:7.2f}   charter: 269.66")
print()

# ---------------- payload table, raw, by rank ----------------
print("="*112); print("RAW PAYLOADS - rank 4 vs rank 5, and the charLevel-keyed melee"); print("="*112)
print(f"  {'ability / field':46s} {'r4':>9s} {'r5':>9s}")
for lbl,rec,ks in (("primordian_frigidring (nova, per prong)",RING,
                    ['offensivePhysicalMin','offensiveColdMin','offensiveSlowColdMin','offensiveSlowColdDurationMin',
                     'offensiveFreezeMin','offensiveFreezeMax']),
                   ("primordian_wave",WAVE,['offensivePhysicalMin','offensiveColdMin','offensiveSlowColdMin',
                     'offensiveSlowDamageMultMin','offensiveSlowDamageMultDurationMin']),
                   ("chillbane_blizzard (per drop)",BLIZ,['offensivePhysicalMin','offensiveColdMin',
                     'offensiveSlowTotalSpeedMin','offensiveSlowTotalSpeedDurationMin']),
                   ("primordian_icearmor",ARMR,['damageAbsorptionPercent','characterAttackSpeedModifier',
                     'offensiveColdModifier','retaliationSlowColdMin','skillActiveDuration','skillCooldownTime']),
                   ("primordian_passive (flat cold rider)",PASS,['offensiveColdMin','offensiveColdMax'])):
    print(f"  {lbl}")
    for k in ks:
        print(f"    {k:44s} {g(rec,k,4):9.1f} {g(rec,k,5):9.1f}")
print(f"  damagebase_physical04 (melee, rank = charLevel)")
for k in ['offensivePhysicalMin','offensivePhysicalMax']:
    print(f"    {k:44s} {g(MELE,k,13):9.1f} {g(MELE,k,18):9.1f}   <- cl13 / cl18")
print()

# ---------------- the composite factors ----------------
print("="*112); print("COMPOSITE OUTGOING FACTORS"); print("="*112)
print(f"  {'cell':34s} {'poolTotal%':>10s} {'pak%':>6s} {'vetStage%':>9s} {'FACTOR':>8s} {'physMult':>9s}")
CELLS=[]
for cl,rk in ((13,4),(18,5)):
    for vet in ('none','own','pooled'):
        f,_,_,pt,vt,_=regime(cl,vet)
        CELLS.append((cl,rk,vet,f))
        print(f"  cl {cl:2d} / rank {rk} / Veteran {vet:7s} {pt:10.1f} {PAK_TOTAL:6.1f} {vt:9.1f} {f:8.4f} {phys_mult(cl,vet):9.4f}")
print()

# ---------------- THE GRID ----------------
ICE=lambda rk: g(ARMR,'offensiveColdModifier',rk)
def kit(cl,rk,vet,icearmor):
    ice = ICE(rk) if icearmor else 0.0
    out={}
    # nova, per prong, three distance bands
    p=g(RING,'offensivePhysicalMin',rk); c=g(RING,'offensiveColdMin',rk)
    base = deliver(p,"Physical",cl,vet) + deliver(c,"Cold",cl,vet,ice)
    for lab,scale in (("nova close band (r<2.5, 50%, x2 prongs)",0.5*2),
                      ("nova mid band   (2.5-9.0, 100%)",1.0),
                      ("nova FAR band   (9.0-20, 140%)",1.4)):
        out[lab]=base*scale
    out["nova cold DoT / 2.0 s"] = g(RING,'offensiveSlowColdMin',rk)*MIT["Cold"]*(1+ice/100)* \
                                   regime(cl,vet)[0]*(1+PAK_SLOWCOLD/100)
    out["nova freeze (s)"] = None
    # wave
    p=g(WAVE,'offensivePhysicalMin',rk); c=g(WAVE,'offensiveColdMin',rk)
    out["wave impact"] = deliver(p,"Physical",cl,vet) + deliver(c,"Cold",cl,vet,ice)
    out["wave cold DoT / 3.0 s"] = g(WAVE,'offensiveSlowColdMin',rk)*MIT["Cold"]*(1+ice/100)* \
                                   regime(cl,vet)[0]*(1+PAK_SLOWCOLD/100)
    # blizzard
    p=g(BLIZ,'offensivePhysicalMin',rk); c=g(BLIZ,'offensiveColdMin',rk)
    out["blizzard per drop"] = deliver(p,"Physical",cl,vet) + deliver(c,"Cold",cl,vet,ice)
    # melee: damagebase_physical04 keyed on charLevel; passive cold rider at skill rank
    pmin=g(MELE,'offensivePhysicalMin',cl); pmax=g(MELE,'offensivePhysicalMax',cl)
    cmin=g(PASS,'offensiveColdMin',rk);     cmax=g(PASS,'offensiveColdMax',rk)
    out["melee swing MIN"] = deliver(pmin,"Physical",cl,vet)+deliver(cmin,"Cold",cl,vet,ice)
    out["melee swing MAX"] = deliver(pmax,"Physical",cl,vet)+deliver(cmax,"Cold",cl,vet,ice)
    # icearmor retaliation rider
    out["icearmor retaliation / 2.0 s"] = g(ARMR,'retaliationSlowColdMin',rk)*MIT["Cold"]* \
        regime(cl,vet)[0]*(1+PAK['retaliationTotalDamageModifier'][0]/100)* \
        (1+(VET['retaliationTotalDamageModifier']/100 if vet!='none' else 0))
    return out

ORDER=["nova close band (r<2.5, 50%, x2 prongs)","nova mid band   (2.5-9.0, 100%)",
       "nova FAR band   (9.0-20, 140%)","nova cold DoT / 2.0 s","wave impact","wave cold DoT / 3.0 s",
       "blizzard per drop","melee swing MIN","melee swing MAX","icearmor retaliation / 2.0 s"]

for icearmor in (True,False):
    print("="*112)
    print(f"THE FOUR-CELL GRID - S2_FULL + Veteran, post-mitigation, icearmor {'UP (+28% cold)' if icearmor else 'DOWN'}")
    print("="*112)
    hdr=[("cl13/r4 own",13,4,'own'),("cl13/r4 pooled",13,4,'pooled'),
         ("cl18/r5 own",18,5,'own'),("cl18/r5 pooled",18,5,'pooled'),
         ("cl18/r5 NOvet",18,5,'none')]
    tabs={h[0]:kit(h[1],h[2],h[3],icearmor) for h in hdr}
    print(f"  {'delivered damage':38s} " + " ".join(f"{h[0]:>14s}" for h in hdr))
    for k in ORDER:
        row=" ".join(f"{tabs[h[0]][k]:14.2f}" if tabs[h[0]][k] is not None else f"{'-':>14s}" for h in hdr)
        print(f"  {k:38s} {row}")
    print(f"  {'-- WORST SINGLE HIT':38s} " +
          " ".join(f"{max(v for kk,v in tabs[h[0]].items() if v is not None and 'DoT' not in kk and 'retal' not in kk):14.2f}" for h in hdr))
    print(f"  {'-- worst / player pool 759':38s} " +
          " ".join(f"{100*max(v for kk,v in tabs[h[0]].items() if v is not None and 'DoT' not in kk and 'retal' not in kk)/POOL_HUMAN:13.1f}%" for h in hdr))
    print()
