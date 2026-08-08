#!/usr/bin/env python3
"""Q2 CLOSURE TEST: M = 1 + 5.80 + G/100 + armorbaseNN[charLevel-1]/100 , eHP = floor(base*M)."""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged
import math
AB={}
for n in ("01","02","03","04","05"):
    r,p,o=merged(f"records/skills/nonplayerskills/passive/armorbase{n}.dbr")
    AB[n]=r["characterLifeModifier"]
    print(f"armorbase{n} [{p['characterLifeModifier']}] owners={o} len={len(AB[n])} idx104..113={[int(x) for x in AB[n][104:114]]}")
g3,_,_ = merged("records/game/balancingadjustment_survivalmode_enemies03.dbr")
G_ARR=g3["characterLifeModifier"]
d,_,_ = merged("records/game/balancingadjustment_mp+difficulty_enemies01.dbr")
ULT=d["characterLifeModifier"][8]
print(f"\nUltimate/solo pack characterLifeModifier[8] = {ULT}")
print(f"Gladiator array idx158={G_ARR[158]} idx159={G_ARR[159]} idx160={G_ARR[160]}")

BODY = [  # name, curve, armorbase, camera_level, own_lifemod, measured
 ("Zantarin, the Immortal",      lambda L:(L*42)**1.5+20000, "05",109,  0.0,3722896),
 ("Archmage Aleksander",         lambda L:(L*42)**1.5+20000, "05",109,  0.0,3722896),
 ("Kubacabra P1",                lambda L:(L*36)**1.5+16000, "05",109,  0.0,2955796),
 ("Galakros, the Mountain",      lambda L:(L*33)**1.5+500,   "05",106,  0.0,2295755),
 ("Aetherial Bileeater",         lambda L:(L*27)**1.33+150,  "04",112, 50.0, 484095),
 ("Death Revenant",              lambda L:(L*11)**1.50-20,   "05",109,  0.0, 468504),
 ("Aleksander's Shard",          lambda L:(L*4)**1.5+100,    "04",109,  0.0, 103912),
 ("Skeletal Archer",             lambda L:(L*5.6)**1.28+24,  "01",109,  0.0,  41237),
]
for GIDX in (158,159):
    G=G_ARR[GIDX]
    print(f"\n{'='*104}\n  G = characterLifeModifier[{GIDX}] = {G}   (base M0 = 1 + {ULT/100} + {G/100} = {1+ULT/100+G/100})\n{'='*104}")
    print(f"  {'body':30s} {'L':>4} {'AB':>4} {'armor%':>7} {'M':>9} {'base_life':>14} {'predicted':>12} {'measured':>12} {'resid':>10}  {'own-in?':>8}")
    for nm,f,ab,L,own,meas in BODY:
        a=AB[ab][L-1]
        for label,M in (("own OUT",1+ULT/100+G/100+a/100),("own IN ",1+ULT/100+G/100+a/100+own/100)):
            if own==0 and label=="own IN ": continue
            base=f(L); pred=math.floor(base*M)
            ok="EXACT" if pred==meas else f"{(pred-meas)/meas*100:+.4f}%"
            print(f"  {nm:30s} {L:4d} {ab:>4} {a:7.0f} {M:9.4f} {base:14,.3f} {pred:12,d} {meas:12,d} {ok:>10}  {label}")
