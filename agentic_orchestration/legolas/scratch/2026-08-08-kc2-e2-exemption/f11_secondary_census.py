#!/usr/bin/env python3
"""F-8 RIDER / part 4 -- CONTROL CENSUS.  READ-ONLY.
Does ANY SkillSecondary_* record in the corpus declare skillManaCost?
  - if none do  -> secondary skills structurally never carry their own cost (family law)
  - if some do  -> Soulfire's omission is a per-record authoring choice
Plus: who points AT eyeofreckoning2 (the parent linkage), and the EoR/Soulfire cost-hook trace.
"""
import sys, pathlib, re, collections
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ORDER = [("base", "database/database.arz"), ("gdx1", "gdx1/database/GDX1.arz"),
         ("gdx2", "gdx2/database/GDX2.arz"), ("gdx3", "gdx3/database/GDX3.arz"),
         ("sm_mod", "mods/survivalmode/database/SurvivalMode.arz"),
         ("sm1", "survivalmode1/database/SurvivalMode1.arz"),
         ("sm2", "survivalmode2/database/SurvivalMode2.arz"),
         ("sm3", "survivalmode3/database/SurvivalMode3.arz")]
ARC, WHERE = {}, collections.defaultdict(list)
for k, rel in ORDER:
    ARC[k] = ArzArchive(ROOT / rel)
    for r in ARC[k].records:
        WHERE[r].append(k)

print("=" * 104)
print("CONTROL CENSUS: every SkillSecondary_* record and whether it declares skillManaCost")
print("=" * 104)
byclass = collections.defaultdict(lambda: [0, 0])
withcost = []
for p, ks in WHERE.items():
    r = ARC[ks[-1]].read_record(p)
    c = str(r.get("Class") or "")
    if not c.startswith("SkillSecondary"):
        continue
    has = "skillManaCost" in r
    byclass[c][1 if has else 0] += 1
    if has: withcost.append((p, c, r["skillManaCost"]))
tot = [0, 0]
print(f"  {'Class':52s} {'no cost':>8s} {'HAS cost':>9s}")
for c in sorted(byclass):
    v = byclass[c]; tot[0] += v[0]; tot[1] += v[1]
    print(f"  {c:52s} {v[0]:8d} {v[1]:9d}")
print(f"  {'TOTAL':52s} {tot[0]:8d} {tot[1]:9d}")
if withcost:
    print("\n  records that DO declare it:")
    for p, c, v in sorted(withcost)[:40]:
        print(f"    {p:70s} {c:44s} {v}")
else:
    print("\n  ZERO SkillSecondary_* records in the corpus declare skillManaCost.")

# also: the whole playerclass09 skill family, cost column
print("\n" + "=" * 104)
print("playerclass09 (Oathkeeper) skill records -- Class + skillManaCost presence")
print("=" * 104)
for p in sorted(x for x in WHERE if x.startswith("records/skills/playerclass09/")):
    r = ARC[WHERE[p][-1]].read_record(p)
    mc = r.get("skillManaCost")
    tag = ("ABSENT" if mc is None else
           f"len={len(mc)} [{min(mc):g}..{max(mc):g}]" if isinstance(mc, list) else str(mc))
    print(f"  {pathlib.Path(p).stem:34s} {str(r.get('Class'))[:44]:46s} skillManaCost={tag}")

# parent linkage: who references eyeofreckoning2?
print("\n" + "=" * 104)
print("PARENT LINKAGE -- records that reference eyeofreckoning2.dbr")
print("=" * 104)
TGT = "records/skills/playerclass09/eyeofreckoning2.dbr"
n = 0
for p, ks in WHERE.items():
    r = ARC[ks[-1]].read_record(p)
    for k, v in r.items():
        if isinstance(v, str) and v.lower() == TGT:
            print(f"  {p:78s} .{k} = {v}")
            n += 1
        elif isinstance(v, list) and any(isinstance(x, str) and str(x).lower() == TGT for x in v):
            print(f"  {p:78s} .{k}[] contains target")
            n += 1
print(f"  ({n} references)")
