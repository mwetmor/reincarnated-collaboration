#!/usr/bin/env python3
"""Q2: break the (L,M) degeneracy. Step 1 -- is the ratio test actually informative?"""
from decimal import Decimal, getcontext
getcontext().prec=40
import math
def nem(L):  return (L*42)**1.5 + 20000
def kub(L):  return (L*36)**1.5 + 16000
def gal(L):  return (L*33)**1.5 + 500
F1=3722896.0; F2=2955796.0; F3=2295755.0
print("== SENSITIVITY AUDIT of the prior note's 'ratio agreement' evidence ==")
print(" measured F1/F2 =", F1/F2)
for L in (100,104,106,108,109,110,112,115,118.6,120,125,130,140,150):
    print(f"   L={L:7.2f}  nem/kub ratio = {nem(L)/kub(L):.8f}   (M from F1 = {F1/nem(L):.6f}, from F2 = {F2/kub(L):.6f}, spread={abs(F1/nem(L)-F2/kub(L))/(F1/nem(L))*100:.4f}%)")
print("\n  ratio asymptote (42/36)^1.5 =", (42/36)**1.5)
print("  => the two-curve 'agreement' is NEARLY AUTOMATIC. Solving the ratio:")
lo,hi=90.0,200.0
for _ in range(200):
    mid=(lo+hi)/2
    if nem(mid)/kub(mid) < F1/F2: lo=mid
    else: hi=mid
Lstar=(lo+hi)/2
print(f"   ratio-solve L* = {Lstar:.6f}   M = {F1/nem(Lstar):.8f} / {F2/kub(Lstar):.8f}")
# sensitivity: perturb F1 by +-1 (one unit in the last digit is EXACT here, but model error is not)
for d in (-30,-10,-1,0,1,10,30):
    lo,hi=80.0,250.0
    tgt=(F1+d)/F2
    for _ in range(200):
        mid=(lo+hi)/2
        if nem(mid)/kub(mid) < tgt: lo=mid
        else: hi=mid
    print(f"   F1 perturbed by {d:+4d} (={abs(d)/F1*100:.5f}%) -> L* = {(lo+hi)/2:.4f}")
