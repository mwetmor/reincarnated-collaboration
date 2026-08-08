#!/usr/bin/env python3
"""FINAL: (a) prove wave 159 cannot produce the F1/F2 bio pair; (b) high-precision closure table."""
import sys, pathlib, json, csv
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, index

OUT = pathlib.Path(__file__).parent

print("=" * 104)
print("A — wave 159 roster: which bios? (rules out 'the footage was wave 159')")
print("=" * 104)
for wave, tier, w in ((159, 16, 9), (160, 16, 10)):
    bios = {}
    for p in sorted(x for x in index() if f"tier{tier:02d}waves/proxy_w{w:02d}_" in x):
        rec, _, _ = merged(p)
        for k, v in rec.items():
            if k.startswith("pool") and isinstance(v, str):
                pool, _, _ = merged(v)
                for f, mv in pool.items():
                    if (f.startswith("name") or f.startswith("nameChampion")) and isinstance(mv, str):
                        m, _, _ = merged(mv)
                        b = m.get("characterAttributeEquations")
                        if b:
                            bios.setdefault(b.split("/")[-1], []).append(mv.split("/")[-1])
    print(f"\n   wave {wave}: {len(bios)} distinct bios across the whole board")
    for b in sorted(bios):
        mark = "  <== F1/F2 bio" if b in ("bio_boss_nemesis_01.dbr", "bio_boss_nemesis3phase_01.dbr") else ""
        print(f"      {b:38s} n={len(bios[b])}{mark}")

print("\n" + "=" * 104)
print("B — HIGH-PRECISION closure")
print("=" * 104)
F1, F2, F3 = 3722896.0, 2955796.0, 2295755.0
ULT = 580.0
APL = 100
SPAWN_BOSS = (APL + 4) + (APL // 50)                 # lv8_boss+   -> 106
SPAWN_UBER_MIN, SPAWN_UBER_MAX = (APL + 3), (APL + 3) + (APL // 50)   # lv7_uber hero -> 103..105
CL_NEM = 1.1 * SPAWN_BOSS + 2                        # (charLevel*1.1)+2 -> 118.6
CL_GAL_MAX = SPAWN_UBER_MAX + 5                      # charLevel*1+5 -> 110
CL_STE_MAX = SPAWN_UBER_MAX                          # charLevel*1   -> 105

base_nem = (CL_NEM * 42) ** 1.5 + 20000
base_kub = (CL_NEM * 36) ** 1.5 + 16000
base_gal = (CL_GAL_MAX * 33) ** 1.5 + 500
base_ste = (CL_STE_MAX * 33) ** 1.5 + 500

print(f"   lv8_boss+  spawn = (100+4)+(100//50) = {SPAWN_BOSS}   -> nemesis charLevel (x1.1)+2 = {CL_NEM}")
print(f"   lv7_uber   spawn = {SPAWN_UBER_MIN}..{SPAWN_UBER_MAX}  -> Galakros(+5) {SPAWN_UBER_MIN+5}..{CL_GAL_MAX}"
      f" | Steward(x1) {SPAWN_UBER_MIN}..{CL_STE_MAX}")
print(f"\n   base_life  bio_boss_nemesis_01        @{CL_NEM}  = {base_nem:,.3f}")
print(f"   base_life  bio_boss_nemesis3phase_01  @{CL_NEM}  = {base_kub:,.3f}")
print(f"   base_life  bio_..colossusgalakros     @{CL_GAL_MAX}  = {base_gal:,.3f}")
print(f"   base_life  bio_boss_tombguardian      @{CL_STE_MAX}  = {base_ste:,.3f}")

rows = []
for lbl, G, note in (("wave-160 cell (idx 159)", 324.0, "U-8 convention: wave = idx+1"),
                     ("wave-159 cell (idx 158)", 322.0, "index-by-completed-waves reading")):
    M = 1 + ULT / 100 + G / 100
    print(f"\n   -- Gladiator characterLifeModifier = {G:.0f}  ->  M = 1 + 5.80 + {G/100:.2f} = {M:.4f}   [{note}]")
    for nm, fv, base, who in (("F1", F1, base_nem, "nemesis, (charLevel*1.1)+2 group, bio_boss_nemesis_01"),
                              ("F2", F2, base_kub, "Kubacabra (nemesis_beast_01_p1), bio_boss_nemesis3phase_01"),
                              ("F3", F3, base_gal, "Galakros @cl110 (p04), bio_..colossusgalakros"),
                              ("F3'", F3, base_ste, "The Steward @cl105 (p04), bio_boss_tombguardian")):
        pred = base * M
        print(f"      {nm:3s} measured {fv:>11,.0f}   predicted {pred:>11,.1f}   "
              f"residual {(pred/fv-1)*100:+8.4f}%   [{who}]")
        rows.append({"gladiator_cell": lbl, "G": G, "M": M, "fingerprint": nm, "measured": fv,
                     "predicted": round(pred, 2), "residual_pct": round((pred / fv - 1) * 100, 4),
                     "assignment": who})

    # back-solved exact M
    print(f"      exact-M demanded: F1 -> {F1/base_nem:.6f} (G={(F1/base_nem-1-5.80)*100:.3f})   "
          f"F2 -> {F2/base_kub:.6f} (G={(F2/base_kub-1-5.80)*100:.3f})")

with open(OUT / "t19_closure.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

print("\n" + "=" * 104)
print("C — F3 gap, stated exactly")
print("=" * 104)
for G in (324.0, 322.0):
    M = 1 + ULT / 100 + G / 100
    need = F3 / M
    import math
    cl_need = ((need - 500) ** (2 / 3)) / 33
    print(f"   G={G:.0f} (M={M:.2f}): F3 requires base_life {need:,.1f} -> charLevel {cl_need:.3f} on the "
          f"(charLevel*33)^1.5+500 curve")
    print(f"      DB-permitted: Galakros {SPAWN_UBER_MIN+5}..{CL_GAL_MAX}  |  Steward {SPAWN_UBER_MIN}..{CL_STE_MAX}"
          f"   -> shortfall {cl_need-CL_GAL_MAX:+.2f} levels vs Galakros max")
print("\nwrote t19_closure.csv")
