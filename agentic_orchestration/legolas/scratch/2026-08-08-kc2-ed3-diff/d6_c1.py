#!/usr/bin/env python3
"""D6 — B-KC2-C1 decomposition on TWO anchors. Edition-II pin. READ-ONLY."""
import sys, math
sys.path.insert(0,".")
import lib2
E2 = lib2.E2

def ev(expr, L):
    return eval(str(expr).replace("^","**").replace("charLevel", f"({L})"), {"__builtins__":{}}, {})

def life_eq(p):
    r,_ = E2.merged(p); bp = r["characterAttributeEquations"]
    b,_ = E2.merged(bp if isinstance(bp,str) else bp[0])
    return b["characterLife"], r.get("charLevel"), r.get("monsterClassification"), bp

HAR = "records/creatures/enemies/boss&quest/aetherialfleshshaper_haraxis.dbr"
CRA = "records/creatures/enemies/swampcrab_a00_summon.dbr"
heq, hcl, hcls, hbio = life_eq(HAR)
ceq, ccl, ccls, cbio = life_eq(CRA)
print(f"HARAXIS  eq={heq}  charLevel={hcl}  cls={hcls}\n         bio={hbio}")
print(f"CRABLING eq={ceq}  charLevel={ccl}  cls={ccls}\n         bio={cbio}")

HAR_HP = 2_050_807
SURV = 1 + 308/100     # w152 survival characterLifeModifier = +308 %
print(f"\nw152 survival characterLifeModifier = +308 %  -> x{SURV}")

print("\n=== ANCHOR 1 — Haraxis, plate 108 ===")
hb = ev(heq, 108)
hM = HAR_HP / hb
print(f"  base life(108)   = {hb:,.2f}")
print(f"  implied mult     = {hM:.6f}")
print(f"  residual /4.08   = {hM/SURV:.6f}")

print("\n=== ANCHOR 2 — Ugdenbog Crabling, plate levels {107,108}, HP set {42798,43548} ===")
print(f"  {'L':>4} {'base':>12} {'M(42798)':>11} {'M(43548)':>11} {'res42798':>10} {'res43548':>10}")
for L in (105,106,107,108,109,110):
    b = ev(ceq, L)
    print(f"  {L:>4} {b:>12,.2f} {42798/b:>11.4f} {43548/b:>11.4f} {42798/b/SURV:>10.4f} {43548/b/SURV:>10.4f}")

print("\n=== ASSIGNMENT TEST (item 3) — which pairing reproduces ONE shared multiplier? ===")
b107, b108 = ev(ceq,107), ev(ceq,108)
print(f"  base ratio  b108/b107          = {b108/b107:.6f}   ({(b108/b107-1)*100:.3f} %)")
print(f"  measured HP ratio 43548/42798  = {43548/42798:.6f}   ({(43548/42798-1)*100:.3f} %)")
print(f"  monotone  (107<-42798, 108<-43548): M107={42798/b107:.4f}  M108={43548/b108:.4f}  spread={abs(42798/b107-43548/b108)/(42798/b107)*100:.3f} %")
print(f"  inverted  (107<-43548, 108<-42798): M107={43548/b107:.4f}  M108={42798/b108:.4f}  spread={abs(43548/b107-42798/b108)/(43548/b107)*100:.3f} %")

print("\n=== WHAT LEVEL PAIR WOULD the HP pair need, at ONE shared multiplier? ===")
for M in (hM, hM/1.0):
    for hp in (42798, 43548):
        b = hp / M
        L = ((b-25)**(1/1.28))/6
        print(f"   M={M:.4f}  HP={hp:,}  -> required charLevel {L:.4f}")

print("\n=== the two-body Δ under a shared multiplier: what integer ΔL is needed? ===")
for L1 in range(103,110):
    b1 = ev(ceq,L1)
    for dL in (1,2,3):
        b2 = ev(ceq, L1+dL)
        print(f"   L {L1}->{L1+dL}: base ratio {(b2/b1-1)*100:6.3f} %", end="")
    print()
