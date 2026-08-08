#!/usr/bin/env python3
"""FALSIFICATION TEST: under M = 10.04 + armorbase[L-1]/100 and floor(), which integer L match EXACTLY?"""
import sys, pathlib, math
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged
AB={n:merged(f"records/skills/nonplayerskills/passive/armorbase{n}.dbr")[0]["characterLifeModifier"] for n in ("01","02","03","04","05")}
M0 = 1 + 580/100 + 324/100
BODY = [
 ("Zantarin, the Immortal",  lambda L:(L*42)**1.5+20000,"05",3722896,109),
 ("Archmage Aleksander",     lambda L:(L*42)**1.5+20000,"05",3722896,109),
 ("Kubacabra P1",            lambda L:(L*36)**1.5+16000,"05",2955796,109),
 ("Galakros, the Mountain",  lambda L:(L*33)**1.5+500,  "05",2295755,106),
 ("Aetherial Bileeater",     lambda L:(L*27)**1.33+150, "04", 484095,112),
 ("Death Revenant",          lambda L:(L*11)**1.50-20,  "05", 468504,109),
 ("Aleksander's Shard",      lambda L:(L*4)**1.5+100,   "04", 103912,109),
 ("Skeletal Archer",         lambda L:(L*5.6)**1.28+24, "01",  41237,109),
]
print(f"M0 = 1 + 5.80 + 3.24 = {M0}\n")
print(f"{'body':26s} {'camera L':>8}  exact-matching integer L in [80,160]")
for nm,f,ab,meas,cam in BODY:
    hits=[L for L in range(80,161) if math.floor(f(L)*(M0+AB[ab][L-1]/100))==meas]
    flag = "UNIQUE+CAMERA" if hits==[cam] else ("contains camera" if cam in hits else "!! CAMERA NOT A SOLUTION")
    print(f"{nm:26s} {cam:8d}  {hits}   <- {flag}")
print("\n== also scan the free-M version: which (L, M0') pairs are exact? (M0' over ALL Gladiator cells) ==")
G=merged("records/game/balancingadjustment_survivalmode_enemies03.dbr")[0]["characterLifeModifier"]
for nm,f,ab,meas,cam in BODY[:1]+BODY[3:4]:
    sols=[]
    for gi,g in enumerate(G):
        for L in range(80,161):
            if math.floor(f(L)*(1+5.8+g/100+AB[ab][L-1]/100))==meas: sols.append((gi,int(g),L))
    print(f"  {nm}: {len(sols)} (gladiator-index, G, L) exact solutions; those with G=324: {[s for s in sols if s[1]==324]}")
