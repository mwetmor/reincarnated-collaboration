#!/usr/bin/env python3
"""Q2/Q3: joint exact-match solve. For each body, M(L) over integer L; find M where many bodies agree."""
import math
from collections import defaultdict
BODIES = {  # name: (curve, own_lifemod, measured, camera_level_or_None)
 "Zantarin        (nemesis_01)":       (lambda L:(L*42)**1.5+20000, 0.0, 3722896, 109),
 "Aleksander      (nemesis_01)":       (lambda L:(L*42)**1.5+20000, 0.0, 3722896, 109),
 "Kubacabra P1    (nem3phase_01)":     (lambda L:(L*36)**1.5+16000, 0.0, 2955796, 109),
 "Galakros        (colossusgalakros)": (lambda L:(L*33)**1.5+500,   0.0, 2295755, 106),
 "Bileeater       (bloater_b01)":      (lambda L:(L*27)**1.33+150, 50.0,  484095, 112),
 "DeathRevenant   (hero_standard_01)": (lambda L:(L*11)**1.50-20,   0.0,  468504, 109),
 "Aleksndr Shard  (clustersummon)":    (lambda L:(L*4)**1.5+100,    0.0,  103912, 109),
 "SkeletalArcher  (skeletonfodder_01)":(lambda L:(L*5.6)**1.28+24,  0.0,   41237, 109),
}
print("== A. M implied at the CAMERA-READ level (global M = required - own/100) ==")
for n,(f,own,meas,cl) in BODIES.items():
    b=f(cl); M=meas/b
    print(f"  {n:36s} L={cl}  base={b:14,.3f}  M_tot={M:10.6f}  M_glob(=M_tot-own/100)={M-own/100:10.6f}")

print("\n== B. exact-integer-level scan: for each body, which integer L gives a 'round' global M? ==")
grid=defaultdict(list)
for n,(f,own,meas,cl) in BODIES.items():
    for L in range(95,145):
        M=meas/f(L)-own/100
        grid[n].append((L,M))
# find M values (2dp) hit by the most bodies
votes=defaultdict(set)
for n,lst in grid.items():
    for L,M in lst:
        votes[round(M,2)].add((n,L))
best=sorted(votes.items(), key=lambda kv:-len(kv[1]))[:12]
for M,s in best:
    print(f"   M_glob={M:8.2f}  bodies={len(s)}  " + " | ".join(f"{n.split()[0]}@{L}" for n,L in sorted(s)))
