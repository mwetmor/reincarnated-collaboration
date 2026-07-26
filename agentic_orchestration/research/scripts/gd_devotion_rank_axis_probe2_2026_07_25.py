#!/usr/bin/env python3
"""
gd_devotion_rank_axis_probe2_2026_07_25.py — GATE 1, round 2 (the decisive tests).

Round 1 (`gd_devotion_rank_axis_probe_2026_07_25.py`) established:
  - the "48" is `skillTemplates` (a boilerplate STRING array), not a rank axis;
  - payload-array lengths cluster at {10, 15, 20, 25};
  - `skillExperienceLevels` is NOT one shared table — there are 4 distinct tables,
    with lengths {10?, 15, 20, 25} matching the payload clusters;
  - 500/502 devotion `Skill_Passive` star nodes carry NO arrays at all.

Round 2 tests the hypothesis directly:
  H: the array axis is the power's own SKILL-EXPERIENCE LEVEL — an auto-levelling tier
     driven by accumulated skill XP — and NOT a player-bought rank, NOT devotion points,
     NOT constellation stars.

READ-ONLY.
"""
import sys, pathlib, collections, json

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from gd_arz_adapter_2026_07_24 import ArzArchive  # noqa: E402

BASE = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARCH = ["database/database.arz", "gdx1/database/GDX1.arz",
        "gdx2/database/GDX2.arz", "gdx3/database/GDX3.arz"]
ars = {a: ArzArchive(BASE / a) for a in ARCH}
union = {}
for a in ARCH:
    for r in ars[a].records:
        union[r] = a
read = lambda p: ars[union[p]].read_record(p)
DEV = sorted(r for r in union if r.startswith("records/skills/devotion/"))
STR_ARRAYS = {"skillTemplates", "skillBlackList", "characterRacialProfile"}


def numeric_arrays(rec):
    return {k: v for k, v in rec.items()
            if isinstance(v, list) and len(v) > 1 and k not in STR_ARRAYS
            and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in v)}


def section(t):
    print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


# ---------------------------------------------------------------- E10 (DECISIVE)
def e10_len_equals_xptable():
    section("E10 [DECISIVE] — per power: does len(payload array) == len(skillExperienceLevels)?")
    agree = disagree = noxp = 0
    mismatches = []
    xplen_hist = collections.Counter()
    for r in DEV:
        try:
            rec = read(r)
        except Exception:
            continue
        if not rec.get("templateAutoCast"):
            continue
        xp = rec.get("skillExperienceLevels")
        na = numeric_arrays(rec)
        if not isinstance(xp, list) or not xp:
            noxp += 1
            continue
        xplen_hist[len(xp)] += 1
        lens = {len(v) for v in na.values()}
        if not lens:
            continue
        if lens == {len(xp)}:
            agree += 1
        else:
            disagree += 1
            mismatches.append((r, len(xp), sorted(lens),
                               {k: len(v) for k, v in na.items() if len(v) != len(xp)}))
    print(f"  powers where EVERY numeric payload array length == len(skillExperienceLevels): {agree}")
    print(f"  powers with at least one differing length                                    : {disagree}")
    print(f"  powers with no XP table                                                      : {noxp}")
    print(f"  len(skillExperienceLevels) histogram across powers: {dict(sorted(xplen_hist.items()))}")
    print("\n  MISMATCHES (all):")
    for r, xl, lens, off in mismatches:
        print(f"    {r}\n        xp_len={xl} array_lens={lens} offenders={off}")


# ---------------------------------------------------------------- E11
def e11_xp_table_identity():
    section("E11 — the distinct XP tables, in full, and which powers use which")
    tabs = collections.defaultdict(list)
    for r in DEV:
        try:
            rec = read(r)
        except Exception:
            continue
        if not rec.get("templateAutoCast"):
            continue
        xp = rec.get("skillExperienceLevels")
        if isinstance(xp, list) and xp:
            tabs[json.dumps(xp)].append(r)
    for t, rs in sorted(tabs.items(), key=lambda x: -len(x[1])):
        v = json.loads(t)
        print(f"\n  TABLE len={len(v)}  used by {len(rs)} powers")
        print(f"    {v}")
        print(f"    e.g. {rs[:3]}")
    # is each table a SUFFIX/PREFIX of another? (i.e. same curve, truncated)
    vals = [json.loads(t) for t in tabs]
    vals.sort(key=len, reverse=True)
    print("\n  nesting check (is the shorter table a TAIL-slice of the longer?):")
    longest = vals[0]
    for v in vals[1:]:
        tail = longest[-len(v):]
        head = longest[:len(v)]
        print(f"    len={len(v):3d}  == head of longest? {head == v}   == tail of longest? {tail == v}"
              f"   first-elem={v[0]} longest-first={longest[0]}")


# ---------------------------------------------------------------- E12
def e12_control_class_skills():
    section("E12 — CONTROL: do PLAYER-CLASS skills carry skillExperienceLevels? (they must not, if H holds)")
    cls = [r for r in union if r.startswith("records/skills/playerclass")]
    have = 0
    tot = 0
    ex = []
    for r in cls:
        try:
            rec = read(r)
        except Exception:
            continue
        if "skillMaxLevel" not in rec:
            continue
        tot += 1
        if isinstance(rec.get("skillExperienceLevels"), list) and rec["skillExperienceLevels"]:
            have += 1
            if len(ex) < 5:
                ex.append(r)
    print(f"  player-class skill records with a skillMaxLevel field : {tot}")
    print(f"    of which carry a non-empty skillExperienceLevels    : {have}   e.g. {ex}")
    # the FoI anchor
    foi = "records/skills/playerclass07/purifyingflame1.dbr"
    if foi in union:
        rec = read(foi)
        na = numeric_arrays(rec)
        print(f"\n  FoI anchor {foi}:")
        print(f"    skillMaxLevel={rec.get('skillMaxLevel')} skillUltimateLevel={rec.get('skillUltimateLevel')} "
              f"skillExperienceLevels={'PRESENT' if rec.get('skillExperienceLevels') else 'ABSENT'}")
        print(f"    numeric array lengths: {sorted({len(v) for v in na.values()})}")


# ---------------------------------------------------------------- E13
def e13_item_skill_control():
    section("E13 — CONTROL: item-granted proc skills (itemskills lane) — same axis?")
    its = [r for r in union if r.startswith("records/skills/itemskills")][:4000]
    have = tot = 0
    lens = collections.Counter()
    ex = []
    for r in its:
        try:
            rec = read(r)
        except Exception:
            continue
        if "skillMaxLevel" not in rec:
            continue
        tot += 1
        xp = rec.get("skillExperienceLevels")
        if isinstance(xp, list) and xp:
            have += 1
            lens[len(xp)] += 1
            if len(ex) < 3:
                ex.append((r, rec.get("skillMaxLevel"),
                           sorted({len(v) for v in numeric_arrays(rec).values()})))
    print(f"  itemskills records with skillMaxLevel : {tot}")
    print(f"    with skillExperienceLevels          : {have}  len-hist={dict(lens)}")
    for e in ex:
        print(f"    {e}")


# ---------------------------------------------------------------- E14
def e14_the_60_outlier():
    section("E14 — the skillMaxLevel=60 outlier among the 65 powers")
    for r in DEV:
        try:
            rec = read(r)
        except Exception:
            continue
        if not rec.get("templateAutoCast"):
            continue
        if rec.get("skillMaxLevel") not in (None, 1):
            print(f"  {r}  Class={rec.get('Class')}  FileDescription={rec.get('FileDescription')!r}")
            print(f"    skillMaxLevel={rec.get('skillMaxLevel')} skillUltimateLevel={rec.get('skillUltimateLevel')}")
            xp = rec.get("skillExperienceLevels")
            print(f"    skillExperienceLevels len={len(xp) if isinstance(xp,list) else None}")
            print(f"    numeric array lens={sorted({len(v) for v in numeric_arrays(rec).values()})}")
            print(f"    templateAutoCast={rec.get('templateAutoCast')}")


# ---------------------------------------------------------------- E15
def e15_devotiontree_nonskilllevel():
    section("E15 — _devotiontree.dbr: non-`skillLevel` fields (what the tree actually declares)")
    rec = read("records/skills/devotion/_devotiontree.dbr")
    others = {k: v for k, v in rec.items() if not k.startswith("skillLevel")}
    pref = collections.Counter()
    for k in others:
        pref[''.join(c for c in k if not c.isdigit())] += 1
    print(f"  total fields {len(rec)}; non-skillLevel {len(others)}")
    print(f"  de-numbered field-name families: {dict(pref)}")
    sn = sorted([k for k in others if k.startswith("skillName")],
                key=lambda x: int(x[9:] or 0))
    print(f"  skillName* count: {len(sn)}; first 5 -> "
          f"{[(k, rec[k]) for k in sn[:5]]}")
    nonzero_lvl = [k for k, v in rec.items() if k.startswith("skillLevel") and v not in ('0', 0)]
    print(f"  skillLevel* entries that are NOT '0': {len(nonzero_lvl)} -> {nonzero_lvl[:10]}")


# ---------------------------------------------------------------- E16
def e16_monotonicity():
    section("E16 — do the payload arrays grow monotonically along the axis? (a level axis should)")
    mono = nonmono = 0
    bad = []
    for r in DEV:
        try:
            rec = read(r)
        except Exception:
            continue
        if not rec.get("templateAutoCast"):
            continue
        for k, v in numeric_arrays(rec).items():
            if all(v[i] <= v[i + 1] for i in range(len(v) - 1)):
                mono += 1
            else:
                nonmono += 1
                if len(bad) < 8:
                    bad.append((r.split("/")[-1], k, v[:6]))
    print(f"  monotonic non-decreasing arrays : {mono}")
    print(f"  non-monotonic arrays            : {nonmono}")
    for b in bad:
        print(f"    {b}")


if __name__ == "__main__":
    e10_len_equals_xptable()
    e11_xp_table_identity()
    e12_control_class_skills()
    e13_item_skill_control()
    e14_the_60_outlier()
    e15_devotiontree_nonskilllevel()
    e16_monotonicity()
