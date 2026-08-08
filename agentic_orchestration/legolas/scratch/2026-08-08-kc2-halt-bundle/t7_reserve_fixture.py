#!/usr/bin/env python3
"""HALT-5: fixture-specific reserve ledger. Sweeps (i) allocated skills, (ii) the 16 gear pieces and
every skill they grant, (iii) component/augment skills, (iv) devotion nodes. READ-ONLY."""
import sys, pathlib, re, json, collections
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

HERE = pathlib.Path(__file__).parent
ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
STACK = [("base", ROOT / "database/database.arz"), ("gdx1", ROOT / "gdx1/database/GDX1.arz"),
         ("gdx2", ROOT / "gdx2/database/GDX2.arz"), ("gdx3", ROOT / "gdx3/database/GDX3.arz")]
M, ARCH = {}, {}
for k, p in STACK:
    a = ArzArchive(p); ARCH[k] = a
    for r in a.records:
        M[r] = k


def rec(path):
    if not path:
        return None
    p = str(path).lower().replace("\\", "/")
    k = M.get(p)
    return ARCH[k].read_record(p) if k else None


CENSUS = json.load(open(HERE / "t6_reserve_census.json"))
RES = set(CENSUS)

# ---- (i) allocated skills, save-parse § 2.2 (allocated ranks) ----
ALLOC = {
    "records/skills/playerclass01/_classtraining_class01.dbr": 46,
    "records/skills/playerclass01/warcry1.dbr": 12, "records/skills/playerclass01/warcry2.dbr": 12,
    "records/skills/playerclass01/fieldcommand1.dbr": 10, "records/skills/playerclass01/fieldcommand2.dbr": 8,
    "records/skills/playerclass01/passive1.dbr": 6, "records/skills/playerclass01/passive2.dbr": 1,
    "records/skills/playerclass01/passive3.dbr": 8, "records/skills/playerclass01/passive4.dbr": 1,
    "records/skills/playerclass01/blitz1.dbr": 1, "records/skills/playerclass01/blitz2.dbr": 1,
    "records/skills/playerclass01/fightingspirit1.dbr": 1, "records/skills/playerclass01/willtolive1.dbr": 1,
    "records/skills/playerclass09/_classtraining_class09.dbr": 50,
    "records/skills/playerclass09/eyeofreckoning1.dbr": 15, "records/skills/playerclass09/eyeofreckoning2.dbr": 12,
    "records/skills/playerclass09/presenceofvirtue1.dbr": 12, "records/skills/playerclass09/presenceofvirtue2.dbr": 9,
    "records/skills/playerclass09/presenceofvirtue3.dbr": 10, "records/skills/playerclass09/divinemandate1.dbr": 12,
    "records/skills/playerclass09/summon_celestialguardian1.dbr": 1,
    "records/skills/playerclass09/summon_celestialguardian2_petmodifier.dbr": 12,
    "records/skills/playerclass09/ascension1.dbr": 1, "records/skills/playerclass09/ascension2.dbr": 1,
    "records/skills/playerclass09/viremight1.dbr": 1, "records/skills/playerclass09/viremight2.dbr": 1,
    "records/skills/playerclass09/viremight3.dbr": 1, "records/skills/playerclass09/passive02.dbr": 2,
}

print("== (i) ALLOCATED PLAYER-CLASS SKILLS — reserve check ==")
print("   (each skill's own record AND its _buff / linked buffSkillName record)")
seen = set()


def scan_skill(p, why, rank=None):
    r = rec(p)
    if r is None:
        print(f"   !! MISSING {p}")
        return []
    out = []
    for f in ("characterManaLimitReserve", "characterManaLimitReserveModifier"):
        v = r.get(f)
        if isinstance(v, list) and any(abs(x) > 1e-9 for x in v):
            out.append((p, f, v, why, rank))
        elif isinstance(v, (int, float)) and abs(v) > 1e-9:
            out.append((p, f, v, why, rank))
    return out


found = []
for p, rk in sorted(ALLOC.items()):
    r = rec(p)
    if r is None:
        print(f"   !! MISSING {p}")
        continue
    found += scan_skill(p, "allocated", rk)
    # follow buff links
    for lf in ("buffSkillName", "petSkillName", "skillActivatedAuraName"):
        tgt = r.get(lf)
        if isinstance(tgt, str) and tgt.endswith(".dbr"):
            found += scan_skill(tgt, f"allocated->{lf}", rk)
    # sibling _buff convention
    sib = p.replace(".dbr", "_buff.dbr")
    if sib in M:
        found += scan_skill(sib, "allocated->_buff", rk)

for p, f, v, why, rk in found:
    if isinstance(v, list):
        print(f"   {p}\n      {f}  [{len(v)}]  alloc_rank={rk}  full={[int(x) if float(x).is_integer() else x for x in v]}")
    else:
        print(f"   {p}\n      {f} = {v}  alloc_rank={rk}")

print("\n   Divine Mandate explicit check:")
for p in ["records/skills/playerclass09/divinemandate1.dbr", "records/skills/playerclass09/divinemandate1_buff.dbr",
          "records/skills/playerclass09/divinemandate2.dbr"]:
    r = rec(p)
    if r is None:
        print(f"      {p}: NOT IN CORPUS")
        continue
    print(f"      {p}: Class={r.get('Class')} exclusiveSkill={r.get('exclusiveSkill')} "
          f"reserve={r.get('characterManaLimitReserve')} reserveMod={r.get('characterManaLimitReserveModifier')} "
          f"skillActiveManaCost={r.get('skillActiveManaCost')}")

# ---- (ii) the 16 gear pieces ----
GEAR = [l.strip() for l in open("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                                "legolas/scratch/2026-08-07-pe1-eor/equipped.txt") if l.strip()]
print(f"\n== (ii) GEAR — {len(GEAR)} records, item-granted skills swept ==")
gskills = []
for g in GEAR:
    r = rec(g)
    if r is None:
        print(f"   !! MISSING {g}")
        continue
    grants = []
    for f in sorted(r):
        if not re.search(r"skillName|itemSkill", f, re.I):
            continue
        v = r[f]
        if isinstance(v, str) and v.endswith(".dbr"):
            grants.append((f, v))
        elif isinstance(v, list):
            for x in v:
                if isinstance(x, str) and x.endswith(".dbr"):
                    grants.append((f, x))
    tag = r.get("itemNameTag") or r.get("description") or ""
    print(f"   {g}  [{tag}]  grants={len(grants)}")
    for f, s in grants:
        gskills.append((g, f, s))
        hit = scan_skill(s, f"gear:{pathlib.Path(g).stem}")
        # follow one link level
        sr = rec(s)
        if sr:
            for lf in ("buffSkillName", "petSkillName"):
                t = sr.get(lf)
                if isinstance(t, str) and t.endswith(".dbr"):
                    hit += scan_skill(t, f"gear:{pathlib.Path(g).stem}->{lf}")
        for h in hit:
            print(f"        *** RESERVE HIT: {h[0]}  {h[1]} = {h[2]}")
        print(f"        {f} -> {s}{'  [RESERVE-BEARING]' if s in RES else ''}")

print(f"\n   total item-granted skill references: {len(gskills)}")
print(f"   intersect with the 82-record reserve census: "
      f"{sorted({s for _, _, s in gskills} & RES) or 'NONE'}")

# ---- (iii) devotion nodes ----
print("\n== (iii) DEVOTION — 55 allocated nodes; reserve census intersect ==")
dev = [p for p in RES if "/devotion" in p]
print(f"   reserve-bearing devotion records in the whole DB: {dev or 'NONE'}")

# ---- (iv) components / augments ----
print("\n== (iv) COMPONENTS + AUGMENTS on the fixture ==")
for g in GEAR:
    r = rec(g)
    if r is None:
        continue
    for f in sorted(r):
        if re.search(r"augment|component|relic|enchant", f, re.I) and isinstance(r[f], str) and r[f].endswith(".dbr"):
            print(f"   {pathlib.Path(g).stem}: {f} -> {r[f]}")
