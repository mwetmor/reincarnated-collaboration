#!/usr/bin/env python3
"""N5 — nova star geometry arithmetic. All inputs MEASURED from DBR; this file is the C layer."""
import math
N=16; ROT=360.0; R_PROJ=0.10; R_PLAYER=0.32; R_BOSS=0.45
EXPL=1.5; VEL=14.0; DIST=12.0
step=ROT/N; half=step/2
print(f"prongs N={N}  arc={ROT}  spacing={step}deg  half-gap={half}deg")
print(f"flight time to max range = {DIST}/{VEL} = {DIST/VEL:.4f} s")
print(f"min standable radius (boss {R_BOSS} + player {R_PLAYER}) = {R_BOSS+R_PLAYER:.2f} u\n")
for name,thr in (("COLLISION reading  (proj actorRadius 0.10 + player 0.32)", R_PROJ+R_PLAYER),
                 ("SPLASH reading     (explosionRadius 1.50 + player 0.32)", EXPL+R_PLAYER)):
    rcrit = thr/math.sin(math.radians(half))
    print(f"--- {name}: threat half-width {thr:.2f} u")
    print(f"    gaps CLOSE below r = {thr:.2f}/sin({half}deg) = {rcrit:.3f} u")
    print(f"    {'r':>5} {'chord sep':>10} {'clear gap':>10} {'safe arc half-ang':>18} {'safe arc len':>13}")
    for r in (1,2,2.5,3,4,5,6,8,10,12):
        chord=2*r*math.sin(math.radians(half))
        gap=chord-2*thr
        s=thr/r
        if s>=1 or r<rcrit: ang=float('nan')
        else: ang=half-math.degrees(math.asin(s))
        arc=math.radians(ang)*r if ang==ang else float('nan')
        print(f"    {r:5.1f} {chord:10.3f} {gap:10.3f} {ang:18.2f} {arc:13.3f}")
    print()
print("double-hit (two adjacent prongs both intersect player disc), COLLISION reading:")
thr=R_PROJ+R_PLAYER
print(f"  worst case (player mid-gap, dtheta={half}deg): both hit while r <= {thr/math.sin(math.radians(half)):.3f} u")
print(f"  best case  (player on a prong, neighbour dtheta={step}deg): both hit while r <= {thr/math.sin(math.radians(step)):.3f} u")
print(f"  => double-hit band = [{R_BOSS+R_PLAYER:.2f}, {thr/math.sin(math.radians(half)):.2f}] u (phase-dependent lower bound {thr/math.sin(math.radians(step)):.2f})")
print("\nradial-outrun check (player speed 7.97 u/s Model A, from prior extraction):")
for r0 in (2,5,8):
    need=(DIST-r0)/(DIST/VEL)
    print(f"  standing at r={r0}: must cover {DIST-r0:.1f} u in {DIST/VEL:.3f} s -> {need:.2f} u/s required vs 7.97 available -> {'POSSIBLE' if need<=7.97 else 'IMPOSSIBLE'}")
print("\nangular-dodge cost from on-prong to mid-gap (COLLISION reading):")
for r in (3,5,8,10):
    s=(R_PROJ+R_PLAYER)/r
    ang=half-math.degrees(math.asin(s))
    print(f"  r={r:4.1f}: need lateral arc >= {math.radians(math.degrees(math.asin(s)))*r:.3f} u to clear a prong; full mid-gap = {math.radians(half)*r:.3f} u; at 7.97 u/s = {math.radians(half)*r/7.97:.3f} s")
