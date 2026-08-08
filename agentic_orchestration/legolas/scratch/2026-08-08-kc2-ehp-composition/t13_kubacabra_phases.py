#!/usr/bin/env python3
"""H3-extension: Kubacabra is a 3-PHASE nemesis with a DIFFERENT bio per phase.
Does phase 2 or 3 supply F3? READ-ONLY."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged

F1, F2, F3 = 3722896.0, 2955796.0, 2295755.0
M = 1 + 5.80 + 3.24            # Ultimate + Gladiator wave-160

print("=" * 104)
print("A — the three Kubacabra phase bios")
print("=" * 104)
eqs = {}
for b in ("bio_boss_nemesis3phase_01", "bio_boss_nemesis3phase_02", "bio_boss_nemesis3phase_03",
          "bio_boss_nemesis2phase_01", "bio_boss_nemesis2phase_02", "bio_boss_nemesis_01"):
    p = f"records/creatures/enemies/bios/{b}.dbr"
    rec, prov, own = merged(p)
    if not rec:
        print(f"   !! ABSENT {p}")
        continue
    eqs[b] = rec["characterLife"]
    print(f"   {b:30s} owners={str(own):22s} characterLife = {rec['characterLife']}")

print("\n" + "=" * 104)
print("B — Kubacabra phase records: charLevel eq + resulting eHP at spawn 106 (lv8_boss+, apl=100)")
print("=" * 104)
SPAWN = 106
PH = ["nemesis_beast_01_p1", "nemesis_beast_01_p2a", "nemesis_beast_01_p2b",
      "nemesis_beast_01_p3a", "nemesis_beast_01_p3b", "nemesis_beast_01_p3c", "nemesis_beast_01_p3d"]
print(f"{'record':26s} {'charLevel eq':22s} {'bio':28s} {'cl':>7s} {'base':>11s} {'eHP (xM=10.04)':>16s}  vs F")
for r in PH:
    p = f"records/creatures/enemies/nemesis/{r}.dbr"
    rec, prov, own = merged(p)
    if not rec:
        print(f"   !! ABSENT {p}")
        continue
    bio = rec["characterAttributeEquations"].split("/")[-1].replace(".dbr", "")
    cl = eval(rec["charLevel"], {}, {"charLevel": float(SPAWN)})
    base = eval(eqs[bio].replace("^", "**"), {}, {"charLevel": cl})
    ehp = base * M
    cmp = ""
    for nm, fv in (("F1", F1), ("F2", F2), ("F3", F3)):
        if abs(ehp / fv - 1) < 0.25:
            cmp += f" {nm} {(ehp/fv-1)*100:+.3f}%"
    print(f"{r:26s} {rec['charLevel']:22s} {bio:28s} {cl:7.2f} {base:>11,.0f} {ehp:>16,.0f} {cmp}")

print("\n" + "=" * 104)
print("C — the same three, with the residual normalised to the F1/F2 offset")
print("=" * 104)
base_nem = eval("((charLevel*42)**1.5)+20000", {}, {"charLevel": 118.6})
off = (base_nem * M) / F1
print(f"   F1 offset factor = {off:.6f}  (prediction is {(off-1)*100:+.4f}% high)")
for nm, fv in (("F1", F1), ("F2", F2), ("F3", F3)):
    print(f"   {nm}: implied base at the SAME offset = {fv*off/M:,.1f}")
