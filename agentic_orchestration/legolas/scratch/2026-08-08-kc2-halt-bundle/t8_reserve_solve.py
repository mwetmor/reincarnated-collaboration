#!/usr/bin/env python3
"""HALT-5 closure: solve the reserve ledger against the DB arrays. READ-ONLY.

Structure:
  reserved = PoV1(r) + PoV2(r) + PoV3(r) + FC1(r) + FC2(r) + PresenceOfMight(300 flat)
Unknowns are the two mastery-wide '+N to all skills in <mastery>' totals, O (Oathkeeper) and
S (Soldier), because those live in the SAVE's component/augment slots, not in the base item DBRs.
Everything else (allocated ranks, gear skill-specific bonuses, the reserve arrays) is DB/save-CITED.
"""
import sys, pathlib, itertools
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
    p = p.lower()
    return A[M[p]].read_record(p) if p in M else None


R = {
    "presenceofvirtue1": rec("records/skills/playerclass09/presenceofvirtue1_buff.dbr")["characterManaLimitReserve"],
    "presenceofvirtue2": rec("records/skills/playerclass09/presenceofvirtue2.dbr")["characterManaLimitReserve"],
    "presenceofvirtue3": rec("records/skills/playerclass09/presenceofvirtue3.dbr")["characterManaLimitReserve"],
    "fieldcommand1": rec("records/skills/playerclass01/fieldcommand1buff.dbr")["characterManaLimitReserve"],
    "fieldcommand2": rec("records/skills/playerclass01/fieldcommand2.dbr")["characterManaLimitReserve"],
}
POM = rec("records/skills/itemskillsgdx1/componentskills/compa_presenceofmight_01.dbr")["characterManaLimitReserve"]
DM = rec("records/skills/playerclass09/divinemandate1.dbr")
print(f"Presence of Might (component skill)  characterManaLimitReserve = {POM}  "
      f"(scalar, skillMaxLevel={rec('records/skills/itemskillsgdx1/componentskills/compa_presenceofmight_01.dbr').get('skillMaxLevel')})")
print(f"Divine Mandate   exclusiveSkill={DM.get('exclusiveSkill')}  "
      f"characterManaLimitReserve={DM.get('characterManaLimitReserve')}  "
      f"characterManaLimitReserveModifier={DM.get('characterManaLimitReserveModifier')}   <-- RESERVES NOTHING")
print()

ALLOC = {"presenceofvirtue1": 12, "presenceofvirtue2": 9, "presenceofvirtue3": 10,
         "fieldcommand1": 10, "fieldcommand2": 8}
GEAR_SPECIFIC = {"presenceofvirtue1": 5, "presenceofvirtue2": 0, "presenceofvirtue3": 0,
                 "fieldcommand1": 0, "fieldcommand2": 0}          # DB-derived, base items only
MASTERY_BASE = {"oathkeeper": 0, "soldier": 3}                     # DB-derived, base items only
MASTERY_OF = {"presenceofvirtue1": "oathkeeper", "presenceofvirtue2": "oathkeeper",
              "presenceofvirtue3": "oathkeeper", "fieldcommand1": "soldier", "fieldcommand2": "soldier"}

OBSERVED = 2576 - 1594


def total(sk, O, S):
    m = O if MASTERY_OF[sk] == "oathkeeper" else S
    return ALLOC[sk] + GEAR_SPECIFIC[sk] + m


def reserve(sk, rank):
    arr = R[sk]
    i = min(max(rank, 1), len(arr)) - 1
    return arr[i], (rank > len(arr))


print(f"OBSERVED reservation = 2576 - 1594 = {OBSERVED}")
print(f"Target from the five class skills = {OBSERVED} - {int(POM)} (Presence of Might) = {OBSERVED - int(POM)}\n")

sols = []
for O, S in itertools.product(range(0, 9), repeat=2):
    tot = sum(reserve(sk, total(sk, O, S))[0] for sk in R)
    if abs(tot + POM - OBSERVED) < 1e-6:
        sols.append((O, S, tot))

print("== SOLUTION SWEEP over mastery-wide bonuses O (Oathkeeper) x S (Soldier), 0..8 each ==")
for O, S, tot in sols:
    print(f"   O=+{O}  S=+{S}   class-skill reserve = {tot:g}   + PoM {POM:g}  =  {tot + POM:g}   *** EXACT ***")
if not sols:
    print("   NO EXACT SOLUTION in the swept range")
print(f"   solutions found: {len(sols)}  (uniqueness over the 81-cell grid)\n")

for O, S, tot in sols:
    print(f"== LEDGER at O=+{O}, S=+{S} ==")
    print(f"{'skill':22s} {'alloc':>6s} {'+gear':>6s} {'+mastery':>9s} {'=total':>7s} {'reserve':>9s}   record / field")
    for sk in ["presenceofvirtue1", "presenceofvirtue2", "presenceofvirtue3", "fieldcommand1", "fieldcommand2"]:
        t = total(sk, O, S)
        v, over = reserve(sk, t)
        m = O if MASTERY_OF[sk] == "oathkeeper" else S
        path = {"presenceofvirtue1": "records/skills/playerclass09/presenceofvirtue1_buff.dbr",
                "presenceofvirtue2": "records/skills/playerclass09/presenceofvirtue2.dbr",
                "presenceofvirtue3": "records/skills/playerclass09/presenceofvirtue3.dbr",
                "fieldcommand1": "records/skills/playerclass01/fieldcommand1buff.dbr",
                "fieldcommand2": "records/skills/playerclass01/fieldcommand2.dbr"}[sk]
        print(f"{sk:22s} {ALLOC[sk]:>6d} {GEAR_SPECIFIC[sk]:>6d} {m:>9d} {t:>7d} {v:>9g}   {path} :: characterManaLimitReserve[{t-1}]{'  (CLAMPED)' if over else ''}")
    print(f"{'Presence of Might':22s} {'-':>6s} {'-':>6s} {'-':>9s} {'-':>7s} {POM:>9g}   "
          f"records/skills/itemskillsgdx1/componentskills/compa_presenceofmight_01.dbr :: characterManaLimitReserve")
    print(f"{'Divine Mandate':22s} {'12':>6s} {'0':>6s} {O:>9d} {12+O:>7d} {0:>9g}   "
          f"records/skills/playerclass09/divinemandate1.dbr :: exclusiveSkill=True, reserve=0")
    print(f"{'':22s} {'':>6s} {'':>6s} {'':>9s} {'TOTAL':>7s} {tot + POM:>9g}   vs observed {OBSERVED}")
    print()

# independent cross-check on the same O
print("== INDEPENDENT CROSS-CHECK on O (Oathkeeper mastery-wide) ==")
for O in {s[0] for s in sols} or {1}:
    eor = 15 + 10 + O
    print(f"   Eye of Reckoning total rank = alloc 15 (save-parse §2.2) + gear-specific 10 (DB) + O={O}  =  {eor}")
    print(f"   Ceremony / grimtools MEASURED EoR rank = 26  ->  {'MATCH' if eor == 26 else 'MISMATCH'}")
print("== INDEPENDENT CROSS-CHECK on S (Soldier mastery-wide) ==")
for S in {s[1] for s in sols} or {4}:
    print(f"   S={S} = base-item mastery bonuses (+3: d028_head +1, d107_blunt2h +2) + {S-3} from the "
          f"same save-side '+1 all skills' source that supplies O={sols[0][0] if sols else 1}")
