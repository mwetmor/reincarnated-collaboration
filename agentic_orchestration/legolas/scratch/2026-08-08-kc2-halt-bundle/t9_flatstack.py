#!/usr/bin/env python3
"""HALT-4: enumerate the fixture's flat + % damage stack from the base-item DBRs and the active
buffs, then test candidate application orderings against the sheet windows. READ-ONLY."""
import sys, pathlib, re, collections
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
A = {k: ArzArchive(ROOT / p) for k, p in
     [("base", "database/database.arz"), ("gdx1", "gdx1/database/GDX1.arz"),
      ("gdx2", "gdx2/database/GDX2.arz"), ("gdx3", "gdx3/database/GDX3.arz")]}
M = {}
for k, a in A.items():
    for r in a.records:
        M[r] = k


def rec(p):
    p = str(p).lower()
    return A[M[p]].read_record(p) if p in M else None


def at(v, rank):
    if isinstance(v, list):
        return v[min(max(rank, 1), len(v)) - 1] if v else 0.0
    return v if isinstance(v, (int, float)) else 0.0


GEAR = [l.strip() for l in open("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                                "legolas/scratch/2026-08-07-pe1-eor/equipped.txt") if l.strip()]

FLAT = ["offensivePhysicalMin", "offensivePhysicalMax", "offensiveBonusPhysicalMin",
        "offensiveBonusPhysicalMax", "offensiveFireMin", "offensiveFireMax"]
PCT = ["offensivePhysicalModifier", "offensiveTotalDamageModifier", "offensiveFireModifier",
       "offensiveCritDamageModifier"]

acc = collections.Counter()
src = collections.defaultdict(list)
WEAPON = "records/items/gearweapons/melee2h/d107_blunt2h.dbr"
for g in GEAR:
    r = rec(g)
    if r is None:
        continue
    for f in FLAT + PCT:
        v = at(r.get(f), 1)
        if abs(v) > 1e-9:
            tag = "WEAPON-BASE" if (g == WEAPON and f in ("offensivePhysicalMin", "offensivePhysicalMax")) else "gear"
            acc[(tag, f)] += v
            src[f].append((pathlib.Path(g).stem, v))

print("== FLAT + % DAMAGE, base-item DBRs only (components/augments live in the save and are INVISIBLE here) ==")
for f in FLAT + PCT:
    tot = sum(v for (t, ff), v in acc.items() if ff == f)
    print(f"  {f:34s} total {tot:9.1f}   from {src[f]}")

# active buffs the sheet composes in
BUFFS = {
    "records/skills/playerclass09/divinemandate1.dbr": 13,
    "records/skills/playerclass09/presenceofvirtue1_buff.dbr": 18,
    "records/skills/playerclass09/presenceofvirtue2.dbr": 10,
    "records/skills/playerclass09/presenceofvirtue3.dbr": 11,
    "records/skills/playerclass01/fieldcommand1buff.dbr": 14,
    "records/skills/playerclass01/fieldcommand2.dbr": 12,
    "records/skills/itemskillsgdx1/componentskills/compa_presenceofmight_01.dbr": 1,
}
print("\n== ACTIVE-BUFF damage contributions (at the HALT-5-solved total ranks) ==")
bacc = collections.Counter()
for p, rk in BUFFS.items():
    r = rec(p)
    if r is None:
        print(f"   !! MISSING {p}")
        continue
    row = {f: at(r.get(f), rk) for f in FLAT + PCT if abs(at(r.get(f), rk)) > 1e-9}
    if row:
        print(f"   {p}  @rank {rk}: {row}")
        for f, v in row.items():
            bacc[f] += v

print("\n== EoR SKILL-SIDE, rank 26 ==")
eor = rec("records/skills/playerclass09/eyeofreckoning1.dbr")
for f in ["weaponDamagePct", "offensivePhysicalMin", "offensivePhysicalMax", "offensiveFireMin",
          "offensiveFireMax", "offensivePhysicalModifier", "offensiveTotalDamageModifier",
          "skillManaCost", "skillTargetRadius", "skillActiveDuration", "delayMovement"]:
    v = eor.get(f)
    print(f"   {f:34s} = {at(v, 26) if isinstance(v, list) else v}"
          f"{'   [array len ' + str(len(v)) + ']' if isinstance(v, list) else ''}")

for mp in ["records/skills/itemskillsgdx2/skillmodifiers/upgradedgdx2/mace2h_d107_eyeofreckoning.dbr",
           "records/skills/itemskillsgdx2/skillmodifiers/legendary/hands_d206_eyeofreckoning.dbr",
           "records/skills/itemskillsgdx1/skillmodifiers/upgradedgdx1/head_d028_warcry.dbr",
           "records/skills/itemskillsgdx2/skillmodifiers/upgradedgdx2/head_d028_eyeofreckoning.dbr",
           "records/skills/itemskillsgdx2/skillmodifiers/upgradedgdx2/set_d025_eyeofreckoning.dbr"]:
    r = rec(mp)
    print(f"\n   -- {mp}")
    if r is None:
        print("      NOT IN CORPUS")
        continue
    for f in sorted(r):
        if not re.search(r"^(offensive|conversion|weaponDamage|itemSkillModifierControl|skillTarget|retaliation)", f):
            continue
        v = r[f]
        if isinstance(v, list):
            v = f"[{len(v)}] {v[0]}..{v[-1]}"
        if v in (0, 0.0, "", None):
            continue
        print(f"      {f:38s} = {v}")

# ---- ordering test ----
print("\n\n== ORDERING TEST vs the sheet windows ==")
SHEET_WEAPON = (16972, 40930)
SHEET_EOR = (43691, 59761)
PCT_PHYS = 396.0       # ceremony note line 210, in-game composed
WDP = 0.64             # spec § 1.3
SKILL_FLAT = (324.0, 344.0)   # spec § 1.3 composed flat, all physical after conversion

print(f"   sheet Weapon Damage = {SHEET_WEAPON}   sheet EoR per hit = {SHEET_EOR}")
print(f"   composed %Physical (ceremony §D) = +{PCT_PHYS}%  ->  x{1+PCT_PHYS/100:.2f}")
print()
print("   MODEL A  EoR = weaponDamagePct x sheetWeaponDamage + skillFlat x (1+%Phys)")
a = (WDP * SHEET_WEAPON[0] + SKILL_FLAT[0] * (1 + PCT_PHYS / 100),
     WDP * SHEET_WEAPON[1] + SKILL_FLAT[1] * (1 + PCT_PHYS / 100))
print(f"            predicts {a[0]:,.0f} - {a[1]:,.0f}   vs sheet {SHEET_EOR[0]:,} - {SHEET_EOR[1]:,}"
      f"   ratio sheet/pred = {SHEET_EOR[0]/a[0]:.2f} / {SHEET_EOR[1]/a[1]:.2f}")
print("   MODEL B  EoR = weaponDamagePct x (sheetWeaponDamage + skillFlat x (1+%Phys))")
b = (WDP * (SHEET_WEAPON[0] + SKILL_FLAT[0] * (1 + PCT_PHYS / 100)),
     WDP * (SHEET_WEAPON[1] + SKILL_FLAT[1] * (1 + PCT_PHYS / 100)))
print(f"            predicts {b[0]:,.0f} - {b[1]:,.0f}   ratio sheet/pred = {SHEET_EOR[0]/b[0]:.2f} / {SHEET_EOR[1]/b[1]:.2f}")
print()
print("   RESIDUAL SOLVE — assume EoR = WDP x sheetWeaponDamage + X, solve X at each end:")
x0 = SHEET_EOR[0] - WDP * SHEET_WEAPON[0]
x1 = SHEET_EOR[1] - WDP * SHEET_WEAPON[1]
print(f"      X_min = {x0:,.0f}   X_max = {x1:,.0f}   spread {x1/x0:.4f}")
print(f"      a flat term is near-constant across the weapon's min/max -> the residual IS a flat term")
print(f"      implied raw skill-side flat at x{1+PCT_PHYS/100:.2f}:  {x0/(1+PCT_PHYS/100):,.0f} - {x1/(1+PCT_PHYS/100):,.0f}")
print(f"      spec §1.3 composed flat is {SKILL_FLAT} -> short by "
      f"{x0/(1+PCT_PHYS/100)/SKILL_FLAT[0]:.1f}x / {x1/(1+PCT_PHYS/100)/SKILL_FLAT[1]:.1f}x")
print()
print("   WEAPON-LINE CONSISTENCY: solve (base_min+F)*Mult = 16972, (base_max+F)*Mult = 40930")
bmin, bmax = 144.0, 740.0
Mult = (SHEET_WEAPON[1] - SHEET_WEAPON[0]) / (bmax - bmin)
F = SHEET_WEAPON[0] / Mult - bmin
print(f"      with weapon base {bmin}-{bmax} (d107_blunt2h offensivePhysicalMin/Max):")
print(f"      Mult = {Mult:.3f}  (i.e. +{100*(Mult-1):.0f}% total)   F = {F:.1f} flat")
print(f"      the ceremony's composed %Physical is +{PCT_PHYS}% = x{1+PCT_PHYS/100:.2f} -> "
      f"UNEXPLAINED residual multiplier x{Mult/(1+PCT_PHYS/100):.2f}")
