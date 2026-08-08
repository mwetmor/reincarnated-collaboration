#!/usr/bin/env python3
"""
EXACT SOLVE — 2 equations (F1, F2), 2 unknowns (charLevel cl, global multiplier M).
Both fingerprints run through DIFFERENT bio equations, so the system is over-determined
in the sense that a consistent (cl, M) existing at all is itself the evidence.
Then: test the additive prediction M = 1 + 5.80 + 3.24 = 10.04 against the solved M.
READ-ONLY.
"""
import sys, json, pathlib, math
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scipy.optimize import brentq   # noqa

F1, F2, F3 = 3722896.0, 2955796.0, 2295755.0

# DB-CITED equations
life_nem = lambda cl: (cl * 42) ** 1.5 + 20000      # bio_boss_nemesis_01        [sm_mod]
life_kub = lambda cl: (cl * 36) ** 1.5 + 16000      # bio_boss_nemesis3phase_01  [sm1]
life_col = lambda cl: (cl * 33) ** 1.5 + 500        # bio_boss_aetherial_colossusgalakros [sm1]
                                                    # (identical eq on bio_boss_tombguardian [sm2])
life_hero = lambda cl: (cl * 11) ** 1.50 - 20       # bio_hero_standard_01       [sm_mod]

print("=" * 100)
print("STEP 1 — solve F1/F2 for charLevel (M cancels)")
print("=" * 100)
target = F1 / F2
f = lambda cl: life_nem(cl) / life_kub(cl) - target
lo, hi = 20.0, 400.0
print(f"   target F1/F2 = {target:.6f}")
print(f"   ratio at cl=20 : {life_nem(20)/life_kub(20):.6f}")
print(f"   ratio at cl=400: {life_nem(400)/life_kub(400):.6f}")
cl = brentq(f, lo, hi, xtol=1e-9)
print(f"\n   >>> solved charLevel = {cl:.6f}")
M1 = F1 / life_nem(cl)
M2 = F2 / life_kub(cl)
print(f"   >>> M from F1 = {M1:.6f}")
print(f"   >>> M from F2 = {M2:.6f}   (identical by construction — the ratio was the constraint)")

print("\n" + "=" * 100)
print("STEP 2 — the DB-predicted multiplier, and the level it implies")
print("=" * 100)
ULT = 580.0     # balancingadjustment_mp+difficulty_enemies01.characterLifeModifier[8]  (Ultimate, 1 player)
GLAD = 324.0    # balancingadjustment_survivalmode_enemies03.characterLifeModifier[159] (wave 160 Gladiator)
M_add = 1 + ULT / 100 + GLAD / 100
M_mul = (1 + ULT / 100) * (1 + GLAD / 100)
print(f"   ADDITIVE      M = 1 + {ULT/100} + {GLAD/100} = {M_add:.4f}")
print(f"   MULTIPLICATIVE M = (1+{ULT/100})*(1+{GLAD/100}) = {M_mul:.4f}")
print(f"   SOLVED         M = {M1:.4f}")
print(f"   -> additive is off by {(M1/M_add-1)*100:+.3f}% ; multiplicative off by {(M1/M_mul-1)*100:+.1f}%")

for name, M in (("additive 10.04", M_add), ("solved", M1)):
    cl1 = brentq(lambda c: life_nem(c) * M - F1, 20, 400)
    cl2 = brentq(lambda c: life_kub(c) * M - F2, 20, 400)
    print(f"\n   under M={M:.4f}:  cl(from F1) = {cl1:.4f}   cl(from F2) = {cl2:.4f}   "
          f"spread = {abs(cl1-cl2):.4f} levels")

print("\n" + "=" * 100)
print("STEP 3 — what spawn level does the DB predict, and does it match?")
print("=" * 100)
apl = 100
spawn = (apl + 4) + (apl // 50)        # lv8_boss+  [base]
print(f"   lv8_boss+ at apl={apl}: spawn level = (100+4)+(100//50) = {spawn}")
for eq, lbl in (("charLevel*1.1+2", "(charLevel*1.1)+2  [9 of 16 nemeses]"),
                ("charLevel*1", "charLevel*1  [4 nemeses]"),
                ("charLevel*1+2", "charLevel*1+2  [Valdaran]"),
                ("charLevel*1+5", "charLevel*1+5  [Aleksander]")):
    v = eval(eq, {}, {"charLevel": float(spawn)})
    print(f"   {lbl:40s} -> charLevel = {v:.2f}   (floor {math.floor(v)})")

print("\n" + "=" * 100)
print("STEP 4 — F3: what does the solved M require, and which record can supply it?")
print("=" * 100)
for M, lbl in ((M1, "solved"), (M_add, "additive 10.04")):
    need = F3 / M
    print(f"\n   under M={M:.4f}: F3 requires base_life = {need:,.1f}")
    for fn, nm, coef in ((life_nem, "bio_boss_nemesis_01", 42), (life_kub, "bio_boss_nemesis3phase_01", 36),
                         (life_col, "bio_boss_..colossus/tombguardian", 33), (life_hero, "bio_hero_standard_01", 11)):
        try:
            c = brentq(lambda x: fn(x) - need, 1, 2000)
            print(f"       {nm:36s} would need charLevel = {c:.3f}")
        except Exception as ex:
            print(f"       {nm:36s} NO SOLUTION ({ex})")

print("\n   DB-permitted charLevel for the p04 superbosses:")
for lo_, hi_ in ((103, 105),):
    for eq, who in (("charLevel*1+5", "Galakros"), ("charLevel*1", "The Steward")):
        a = eval(eq, {}, {"charLevel": float(lo_)}); b = eval(eq, {}, {"charLevel": float(hi_)})
        print(f"       {who:12s} spawn {lo_}-{hi_} (lv7_uber hero) -> charLevel {a:.0f}-{b:.0f}"
              f"   base_life {life_col(a):,.0f} - {life_col(b):,.0f}"
              f"   -> xM_solved {life_col(a)*M1:,.0f} - {life_col(b)*M1:,.0f}")
print("\n   DB-permitted charLevel for the p06 hero (lv6_hero, spawn 104-105, charLevel+2):")
for s in (104, 105):
    c = s + 2
    print(f"       spawn {s} -> charLevel {c}  base_life {life_hero(c):,.0f}  -> xM_solved {life_hero(c)*M1:,.0f}")
