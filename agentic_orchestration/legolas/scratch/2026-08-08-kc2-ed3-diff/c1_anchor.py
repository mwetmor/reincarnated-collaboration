#!/usr/bin/env python3
"""PART C — anchor the multiplier stack on galadriel's MEASURED Haraxis HP, then test
candidate seats for the 42,798 / 43,548 pair. Edition-II pin (fixture substrate). READ-ONLY."""
import sys, re, math, csv, collections
sys.path.insert(0, ".")
import lib2
E2 = lib2.E2

def ev(expr, L):
    """Evaluate a GD attribute equation in charLevel."""
    s = expr.replace("^", "**").replace("charLevel", f"({L})")
    return eval(s, {"__builtins__": {}}, {})

def life_eq(monpath):
    r, _ = E2.merged(monpath)
    if not r: return None
    bp = r.get("characterAttributeEquations")
    if not bp: return None
    b, _ = E2.merged(bp if isinstance(bp, str) else bp[0])
    if not b or "characterLife" not in b: return None
    return b["characterLife"], r.get("charLevel", "charLevel*1"), r.get("monsterClassification"), bp

def lvl_of(base_L, charlevel_expr):
    return ev(charlevel_expr, base_L)

# ---- 1. ANCHOR: Haraxis, MEASURED max HP 2,050,807, plate level 108 -------------
H = "records/creatures/enemies/boss&quest/aetherialfleshshaper_haraxis.dbr"
eq, cl, cls, bp = life_eq(H)
L_draw = 103.0                      # lv7_uber hero MIN at averagePlayerLevel=100
L_eff  = lvl_of(L_draw, cl)         # charLevel*1+5
base   = ev(eq, L_eff)
MEAS   = 2_050_807
print(f"HARAXIS  bio={bp}")
print(f"  life eq            : {eq}")
print(f"  charLevel expr     : {cl}")
print(f"  lv7 draw (apl=100) : min 103.0  max {103+100/50}")
print(f"  effective charLevel: {L_eff}   (plate read 108 -> MATCH)" )
print(f"  base life(L_eff)   : {base:,.1f}")
print(f"  MEASURED max HP    : {MEAS:,}")
print(f"  IMPLIED TOTAL MULT : {MEAS/base:.6f}")
M = MEAS / base
print(f"  survival w152 scalar (1+308/100) = 4.08 ; residual = {M/4.08:.6f}")
for Ld in (103.0, 104.0, 105.0):
    Le = lvl_of(Ld, cl); b = ev(eq, Le)
    print(f"    if draw {Ld}: charLevel {Le} base {b:,.1f}  implied mult {MEAS/b:.4f}")

# ---- 2. Every body reachable on w152, HP at the anchored multiplier -------------
CSV = "/Users/admin/Games/reincarnated-engine/data/kc2/pe6_crucible_wave_pools_v2.csv"
rows = [r for r in csv.DictReader(open(CSV)) if int(r["global_wave"]) == 152]
mons = set()
for r in rows:
    for c in ("roster_records", "champ_records"):
        for x in (r.get(c) or "").split("|"):
            if x.strip(): mons.add(x.strip().lower())
EXTRA = ["records/creatures/enemies/swampcrab_a00_summon.dbr",
         "records/creatures/enemies/swampcrab_b01_summon.dbr",
         "records/creatures/enemies/swampcrab_c01_summon.dbr",
         "records/creatures/enemies/springscrab_a00_summon.dbr",
         "records/creatures/enemies/aetherialcorruption_c01_summon.dbr",
         "records/creatures/enemies/aetherialcorruption_b02_summon.dbr",
         "records/creatures/enemies/trap_brambletrap_a01.dbr",
         "records/creatures/enemies/trap_icespike_hero_a01.dbr",
         "records/creatures/enemies/trap_lightningspike_hero_a01.dbr"]
for d in E2.find("summondevourers"): print("  devourer skill found:", d)
for d in E2.find("chthoniandevourer"): EXTRA.append(d)
mons |= {e for e in EXTRA if e in E2.idx}

TARGET = (42798, 43548)
print(f"\n=== w152 bodies: HP at anchored mult {M:.4f}, level sweep 100..110 ===")
hits = []
tab = []
for p in sorted(mons):
    got = life_eq(p)
    if not got: continue
    eq2, cl2, cls2, _ = got
    for Ld in [x/2 for x in range(200, 222)]:
        Le = lvl_of(Ld, cl2)
        hp = ev(eq2, Le) * M
        tab.append((p, cls2, Ld, Le, hp))
        for t in TARGET:
            if abs(hp - t) / t < 0.004:
                hits.append((p, cls2, Ld, Le, hp, t))
print(f"  candidates scanned: {len(mons)}   near-hits (<0.4%): {len(hits)}")
for p, c, Ld, Le, hp, t in hits:
    print(f"   {t:>7,}  <-  {hp:11,.0f}  {c:<10} draw {Ld:6.1f} eff {Le:6.1f}  {p}")
