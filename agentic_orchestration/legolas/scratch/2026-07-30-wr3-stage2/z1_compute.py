#!/usr/bin/env python3
"""Z1 — WR3 stage-2 referent arithmetic. All inputs MEASURED above; operators named. READ-ONLY."""
FPS = 30.0
def dur(keys): return (keys - 1) / FPS          # validated: key[N-1] duplicates key[0]

PAK_ATK = 0.90   # balancingadjustment_mp+difficulty_enemies01: characterAttackSpeedModifier -10 (Normal,1p)
PAK_RUN = 0.82   # ... characterRunSpeedModifier -18
PAK_CAST = 0.92  # ... characterSpellCastSpeedModifier -8

print("=== T2a  Primordian melee swing (anm_slith unarmedAttackAnim1/2/3) ===")
variants = [  # (label, keys, contact_frame, animSpeed, weight)
    ("attack_01", 41, 13, 1.20, 40),
    ("attack_02", 51, 20, 1.25, 40),
    ("attack_01", 41, 13, 1.05, 20),
]
for pak, tag in ((1.0, "no-pak"), (PAK_ATK, "pak -10%")):
    W = tot = wu = 0.0
    print(f"-- {tag}")
    for lab, keys, cf, spd, w in variants:
        r = spd * 1.0 * pak                      # x characterAttackSpeed = 1.0
        w_up = cf / FPS / r; t = dur(keys) / r; rec = t - w_up
        print(f"   {lab:10s} w={w:3d}% rate={r:5.3f}  windup={w_up:.4f}s  total={t:.4f}s  recovery={rec:.4f}s")
        W += w; wu += w * w_up; tot += w * t
    wu /= W; tot /= W
    print(f"   WEIGHTED windup={wu:.4f}s  total={tot:.4f}s  recovery={tot-wu:.4f}s")
    print(f"   + swing pause U(0.30,0.40) mean 0.35 -> cycle={tot+0.35:.4f}s  rooted fraction={tot/(tot+0.35):.3f}")

print("\n=== T2b  Primordian nova (primordian_frigidring -> 'Roar' -> slith01_cast_buff_01 @1.25) ===")
for pak, tag in ((1.0,"no-pak"), (PAK_ATK,"pak atk -10%"), (PAK_CAST,"pak cast -8%")):
    r = 1.25 * pak
    print(f"   {tag:14s} rate={r:5.4f}  release(RightHandHit f30)={30/FPS/r:.4f}s  "
          f"swipe(f25)={25/FPS/r:.4f}s  total={dur(61)/r:.4f}s")
print(f"   cadence gates: specialAttack2Chance 80%, Delay 6.0s, Timeout 3.0s, Range MediumRange")

print("\n=== T1  Evade, human form 1h-melee (sHandedEvadeAnim @1.30) ===")
r = 1.30
print(f"   clip hero01_unarmed_dodge01: {29} keys -> {dur(29):.4f}s raw -> {dur(29)/r:.4f}s at 1.30x")
print(f"   StartJump f2   raw {2/FPS:.4f}s -> {2/FPS/r:.4f}s")
print(f"   StopJump/Hit/AllowInterrupt f13 raw {13/FPS:.4f}s -> {13/FPS/r:.4f}s")
print(f"   motion window f2->f13 = {11/FPS:.4f}s raw -> {11/FPS/r:.4f}s")
print(f"   root motion 11.000 u ; skill waveDistance(max range) 10.0 u")
print(f"   dash rate anim {11.0/(11/FPS/r):.3f} u/s ; capped-to-10 {10.0/(11/FPS/r):.3f} u/s")
print(f"   cooldown 3.0 s, cooldownCharges 1, characterRunSpeedModifier +250")

print("\n=== T3  Speeds ===")
PLAYER_BASE, PLAYER_CRS = 6.858/dur(25), 0.93
SLITH_BASE,  PRIM_CRS   = 10.0839/dur(35), 0.85
WARD_BASE,   W1, W2     = 5.000/dur(30), 1.15, 1.40
print(f"   anim bases (root motion / clip duration): player {PLAYER_BASE:.4f} u/s  "
      f"slith {SLITH_BASE:.4f} u/s  warden {WARD_BASE:.4f} u/s")
pA = PLAYER_BASE*PLAYER_CRS
for lab, base, crs in (("Primordian", SLITH_BASE, PRIM_CRS), ("Warden ph.1", WARD_BASE, W1), ("Warden ph.2", WARD_BASE, W2)):
    mA = base*crs*PAK_RUN
    mB = crs*PAK_RUN
    print(f"   {lab:12s}  MODEL-A player {pA:.4f} : boss {mA:.4f} u/s -> ratio {pA/mA:.4f}   |   "
          f"MODEL-B 0.93 : {mB:.4f} -> ratio {PLAYER_CRS/mB:.4f}")
print(f"   our fixture 5.75 : 4.025 m/s -> ratio {5.75/4.025:.4f}")
