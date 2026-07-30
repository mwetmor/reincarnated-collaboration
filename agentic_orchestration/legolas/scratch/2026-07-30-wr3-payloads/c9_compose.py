#!/usr/bin/env python3
"""C9 — the C layer. All inputs M from DBR; this file composes them under named operators."""
import math

# ---- M inputs -------------------------------------------------------------
PAK_TOTAL   = -25.0   # balancingadjustment_mp+difficulty_enemies01 slot0 offensiveTotalDamageModifier
PAK_SLOWCOLD= -38.0
PAK_FREEZE  = -20.0
PAK_ATKSPD  = -10.0
PAK_CASTSPD = -8.0
TOTADJ_TOTAL= 8.0     # damage_totaladjuster rank2
TOTADJ_PHYS = 6.0
ARMORBASE   = {16:-75.0, 17:-74.0, 18:-73.0, 19:-72.0}   # armorbase05 offensiveTotalDamageModifier = -91+rank
MELEE       = {16:(123.,155.), 17:(130.,165.), 18:(136.,175.), 19:(144.,183.)}  # damagebase_physical04
PASS_COLD   = (20.,46.)   # primordian_passive rank5 flat cold add

def factor(cl):
    """pool additive, pak a separate multiplicative stage (envelope-note adjudication)."""
    pool = ARMORBASE[cl] + TOTADJ_TOTAL
    return (1+pool/100.0)*(1+PAK_TOTAL/100.0)

print("=== outgoing-damage factor, by boss charLevel ===")
for cl in (16,17,18,19):
    print(f"  charLevel {cl}: pool {ARMORBASE[cl]:+.0f}{TOTADJ_TOTAL:+.0f} = {ARMORBASE[cl]+TOTADJ_TOTAL:+.0f}%  -> ({1+(ARMORBASE[cl]+TOTADJ_TOTAL)/100:.2f}) x (0.75) = x{factor(cl):.4f}")

print("\n=== A. primordian_wave, rank 5 (M base) -> Normal/1p effective (C) ===")
for cl in (18,19):
    f=factor(cl)
    print(f"  charLevel {cl}  (x{f:.4f})")
    print(f"    physical  153.0 -> {153*f:.1f}   (x1.06 pool phys mod -> {153*f*1.06:.1f})")
    print(f"    cold      272.0 -> {272*f:.1f}")
    print(f"    cold DoT   91.0 over 3.0 s -> {91*f*(1+PAK_SLOWCOLD/100):.1f} over 3.0 s")
    print(f"    TOTAL impact (phys+cold)  {153*f*1.06+272*f:.1f}   + DoT {91*f*0.62:.1f}/3s")

print("\n=== B. chillbane_blizzard, rank 5 per drop (M base) -> Normal/1p effective (C) ===")
for cl in (18,19):
    f=factor(cl)
    print(f"  charLevel {cl}  (x{f:.4f})")
    print(f"    physical   76.0 -> {76*f:.1f}   (x1.06 -> {76*f*1.06:.1f})")
    print(f"    cold      137.0 -> {137*f:.1f}")
    print(f"    TOTAL per drop  {76*f*1.06+137*f:.1f}")

print("\n=== D. melee default swing (M base) -> Normal/1p effective (C) ===")
for cl in (16,18,19):
    f=factor(cl); lo,hi=MELEE[cl]
    p_lo,p_hi = lo*f*1.06, hi*f*1.06
    c_lo,c_hi = PASS_COLD[0]*f, PASS_COLD[1]*f
    print(f"  charLevel {cl}: phys {lo:.0f}-{hi:.0f} -> {p_lo:.1f}-{p_hi:.1f} | passive cold {PASS_COLD[0]:.0f}-{PASS_COLD[1]:.0f} -> {c_lo:.1f}-{c_hi:.1f} | TOTAL {p_lo+c_lo:.1f}-{p_hi+c_hi:.1f}")
print("  envelope note L13 cross-tier base-attack band: 35-85  <- corroboration check")

print("\n=== A3. wave geometry (C from M) ===")
W0,W1,D,DEP,T = 3.0,6.0,16.0,1.0,1.4
v=D/T
print(f"  front speed = {D}/{T} = {v:.3f} u/s")
print(f"  dwell inside depth band = {DEP}/{v:.3f} = {DEP/v:.4f} s   (one application; no tick field exists)")
for r in (1.25,4.75,9.0,12.0,16.0):
    hw=(W0+(W1-W0)*r/D)/2
    print(f"    r={r:5.2f} u: half-width {hw:.3f} u | arrival {r/v:.3f} s after release | lateral clear needed {hw+0.32:.2f} u = {(hw+0.32)/7.97:.3f} s @7.97 u/s")

print("\n=== A5/B. animation timings with the Normal/1p pak (C) ===")
for label,keys,frame,animspd in (("wave  TailLashSunder",79,23,0.90),("icearmor BuffQuick",51,25,1.0),("nova  Roar",61,30,1.25)):
    for tag,mod in (("no pak",1.0),("pak atk -10%",0.90),("pak cast -8%",0.92)):
        rate=animspd*mod
        print(f"  {label:22s} {tag:13s} rate {rate:.3f}: release {frame/30/rate:.4f} s, total {(keys-1)/30/rate:.4f} s")
    print()

print("=== B3. blizzard drop mechanics (C from M) ===")
H,V,EXPL,PR = 20.0,24.0,1.0,0.32
print(f"  fall time = dropHeight/projectileVelocity = {H}/{V} = {H/V:.4f} s  (useTrajectory=False -> constant velocity, no gravity accel)")
print(f"  effective hit radius = projectileExplosionRadius {EXPL} + player actorRadius {PR} = {EXPL+PR:.2f} u")
for name,R in (("Reading S1: skillTargetRadius 8.0 = scatter (ADOPTED)",8.0),("Reading S2: dropRadius 15.0 = scatter (alternative)",15.0)):
    p=((EXPL+PR)/R)**2
    pv=1-(1-p)**6
    print(f"  {name}")
    print(f"     per-drop hit p = ({EXPL+PR:.2f}/{R})^2 = {p*100:.2f}%   per 6-drop volley = {pv*100:.1f}%")
    for n in (4,5):
        print(f"     over {n} volleys ({n*6} drops) = {(1-(1-pv)**n)*100:.1f}%")
print(f"  volleys: skillActiveDuration 8.0 / skillTargetInterval 2.0 = 4 intervals -> 4 or 5 volleys, 24-30 drops")
print(f"  player traverse in one fall time: 7.97 x {H/V:.3f} = {7.97*H/V:.2f} u")
