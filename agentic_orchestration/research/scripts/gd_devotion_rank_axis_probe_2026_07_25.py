#!/usr/bin/env python3
"""
gd_devotion_rank_axis_probe_2026_07_25.py — GATE 1 of the devotion payload banking run.

PURPOSE: resolve, EMPIRICALLY AND FROM HELD RECORDS ONLY, what the array axis on devotion
payload records MEANS. Probe §4.3 flagged the contradiction: celestial powers carry
`skillMaxLevel = 1` yet their damage arrays have 20 entries, and max array depth across the
whole lane is 48. Banking rows whose `rank` column carries an unlabelled semantic silently
poisons every payload number downstream. So: resolve first, bank second.

READ-ONLY. Opens .arz via ArzArchive; does not open corpus.db at all.

RUN: python3 agentic_orchestration/research/scripts/gd_devotion_rank_axis_probe_2026_07_25.py
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


def section(t):
    print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


# ---------------------------------------------------------------- E1
def e1_length_distribution():
    section("E1 — array-length distribution, by record class")
    bylen = collections.Counter()
    byclass = collections.defaultdict(collections.Counter)
    for r in DEV:
        try:
            rec = read(r)
        except Exception:
            continue
        cls = rec.get("Class") or ars[union[r]].record_type(r) or "?"
        for k, v in rec.items():
            if isinstance(v, list) and len(v) > 1:
                bylen[len(v)] += 1
                byclass[cls][len(v)] += 1
    print("  array length -> count of (record,field) pairs, whole devotion lane:")
    for L, n in sorted(bylen.items()):
        print(f"    len={L:3d}  {n:6d}")
    print("\n  per record Class (top lengths):")
    for cls, c in sorted(byclass.items(), key=lambda x: -sum(x[1].values()))[:12]:
        print(f"    {cls:34s} {dict(sorted(c.items()))}")


# ---------------------------------------------------------------- E2
def e2_where_is_48():
    section("E2 — WHERE does length 48 come from? (probe §4.3 'at least one lane differs')")
    hits = collections.Counter()
    example = {}
    for r in DEV:
        try:
            rec = read(r)
        except Exception:
            continue
        for k, v in rec.items():
            if isinstance(v, list) and len(v) >= 30:
                hits[(len(v), k)] += 1
                example.setdefault((len(v), k), (r, rec.get("Class"), v[:4], v[-2:]))
    for (L, k), n in sorted(hits.items(), key=lambda x: (-x[0][0], -x[1]))[:25]:
        r, cls, head, tail = example[(L, k)]
        print(f"    len={L:3d} n={n:4d}  {k:34s} [{cls}] {r}")
        print(f"                head={head} tail={tail}")


# ---------------------------------------------------------------- E3
def e3_skillexp_uniform():
    section("E3 — is `skillExperienceLevels` a PER-POWER table or ONE SHARED table?")
    tables = collections.Counter()
    per_power = {}
    for r in DEV:
        try:
            rec = read(r)
        except Exception:
            continue
        if not rec.get("templateAutoCast"):
            continue
        xp = rec.get("skillExperienceLevels")
        if isinstance(xp, list) and xp:
            tables[json.dumps(xp)] += 1
            per_power[r] = xp
    print(f"  celestial powers with an XP table : {len(per_power)}")
    print(f"  DISTINCT XP tables among them     : {len(tables)}")
    for t, n in tables.most_common(3):
        v = json.loads(t)
        print(f"    n={n:3d} len={len(v)}  head={v[:5]} tail={v[-3:]}")
    if len(tables) == 1:
        print("  => ONE SHARED TABLE. The axis is a GLOBAL progression scale, not a per-power rank.")


# ---------------------------------------------------------------- E4
def e4_xp_vs_player_levels():
    section("E4 — does the XP table match the PLAYER LEVEL xp curve? (does index k == char level?)")
    cands = [r for r in union if "experiencelevel" in r.lower() or "playerlevel" in r.lower()
             or r.endswith("levels.dbr")]
    print(f"  candidate level-table records held: {len(cands)}")
    for c in cands[:12]:
        try:
            rec = read(c)
        except Exception:
            continue
        arrs = {k: v for k, v in rec.items() if isinstance(v, list) and len(v) > 5}
        print(f"    {c}  [{rec.get('Class')}] arrays: "
              f"{ {k: len(v) for k, v in arrs.items()} }")
        for k, v in list(arrs.items())[:3]:
            print(f"        {k}: head={v[:6]} tail={v[-3:]}")
    # the devotion XP table itself
    xp = None
    for r in DEV:
        try:
            rec = read(r)
        except Exception:
            continue
        if rec.get("templateAutoCast") and rec.get("skillExperienceLevels"):
            xp = rec["skillExperienceLevels"]; break
    print(f"\n  devotion skillExperienceLevels ({len(xp)}): {xp}")
    # compare vs a player XP curve if one is found
    for c in cands:
        try:
            rec = read(c)
        except Exception:
            continue
        for k, v in rec.items():
            if isinstance(v, list) and len(v) >= 20 and all(isinstance(x, (int, float)) for x in v):
                pre = v[:len(xp)]
                if pre == xp:
                    print(f"  !! EXACT PREFIX MATCH: devotion XP table == first {len(xp)} of "
                          f"{c}:{k} (len {len(v)})")
                elif set(xp) & set(v):
                    ov = sorted(set(xp) & set(v))[:5]
                    print(f"  ~ overlap with {c}:{k} (len {len(v)}): {len(set(xp) & set(v))} shared "
                          f"values e.g. {ov}")
                    idx = [v.index(x) for x in xp if x in v][:6]
                    print(f"    positions of devotion-XP values inside that table: {idx}")


# ---------------------------------------------------------------- E5
def e5_maxlevel_uniformity():
    section("E5 — skillMaxLevel / skillUltimateLevel across the 65 celestial powers")
    c = collections.Counter()
    arr_lens = collections.Counter()
    for r in DEV:
        try:
            rec = read(r)
        except Exception:
            continue
        if not rec.get("templateAutoCast"):
            continue
        c[(rec.get("skillMaxLevel"), rec.get("skillUltimateLevel"))] += 1
        ls = {len(v) for k, v in rec.items()
              if isinstance(v, list) and len(v) > 1 and k != "skillTemplates"
              and k != "skillBlackList" and all(isinstance(x, (int, float)) for x in v)}
        arr_lens[tuple(sorted(ls))] += 1
    print("  (skillMaxLevel, skillUltimateLevel) -> n powers:")
    for k, n in c.most_common():
        print(f"    {k} -> {n}")
    print("\n  set of numeric-array lengths present per power -> n powers:")
    for k, n in arr_lens.most_common(10):
        print(f"    {k} -> {n}")


# ---------------------------------------------------------------- E6
def e6_stars_per_constellation():
    section("E6 — stars per constellation vs array depth (is the axis 'points in constellation'?)")
    cons = [r for r in union
            if r.startswith("records/ui/skills/devotion/constellations/")
            and "_background" not in r and r.count("/") == 5]
    print(f"  constellation records: {len(cons)}")
    starcounts = collections.Counter()
    shown = 0
    for c in sorted(cons):
        try:
            rec = read(c)
        except Exception:
            continue
        skills = [k for k in rec if k.lower().startswith("devotionskill") or k.lower() == "skillname"]
        n_star = 0
        for k in rec:
            if k.startswith("devotionButton") or k.startswith("skillName"):
                if rec[k]:
                    n_star += 1
        starcounts[n_star] += 1
        if shown < 4:
            print(f"    {c}")
            for k, v in sorted(rec.items()):
                if v not in (0, 0.0, "", False, None):
                    print(f"        {k} = {v!r}")
            shown += 1
    print(f"\n  star-count histogram (fields matching devotionButton*/skillName*): {dict(sorted(starcounts.items()))}")


# ---------------------------------------------------------------- E7
def e7_ui_node_join():
    section("E7 — UI node -> behaviour record join, and what the UI node says about levels")
    ui = [r for r in union if r.startswith("records/ui/skills/devotion/")
          and "constellations" not in r]
    print(f"  UI devotion records: {len(ui)}")
    shown = 0
    for r in sorted(ui):
        try:
            rec = read(r)
        except Exception:
            continue
        if rec.get("skillName") and shown < 3:
            print(f"    {r}")
            for k, v in sorted(rec.items()):
                if v not in (0, 0.0, "", False, None):
                    print(f"        {k} = {v!r}")
            shown += 1


# ---------------------------------------------------------------- E8
def e8_tree_record():
    section("E8 — _devotiontree.dbr: does the tree authorize a level axis?")
    tr = [r for r in union if "devotiontree" in r.lower()]
    for t in tr:
        rec = read(t)
        print(f"  {t}  [{rec.get('Class')}]  {len(rec)} fields")
        keys = sorted(rec)
        interesting = [k for k in keys if any(s in k.lower() for s in
                       ("level", "exp", "rank", "point", "affinity", "tier", "max"))]
        for k in interesting[:40]:
            v = rec[k]
            if isinstance(v, list):
                print(f"      {k} = len {len(v)} head={v[:6]}")
            else:
                print(f"      {k} = {v!r}")
        print(f"      (all field-name prefixes: "
              f"{sorted({k[:14] for k in keys})[:20]})")


# ---------------------------------------------------------------- E9
def e9_passive_vs_power_depth():
    section("E9 — Skill_Passive star nodes: what array depth do THEY carry?")
    c = collections.Counter()
    ex = {}
    for r in DEV:
        try:
            rec = read(r)
        except Exception:
            continue
        cls = rec.get("Class") or ""
        if cls != "Skill_Passive":
            continue
        ls = {len(v) for k, v in rec.items()
              if isinstance(v, list) and k not in ("skillTemplates", "skillBlackList")
              and all(isinstance(x, (int, float)) for x in v)}
        c[tuple(sorted(ls))] += 1
        ex.setdefault(tuple(sorted(ls)), r)
    for k, n in c.most_common(10):
        print(f"    lens={k} -> {n} passives   e.g. {ex[k]}")


if __name__ == "__main__":
    e1_length_distribution()
    e2_where_is_48()
    e3_skillexp_uniform()
    e4_xp_vs_player_levels()
    e5_maxlevel_uniformity()
    e6_stars_per_constellation()
    e7_ui_node_join()
    e8_tree_record()
    e9_passive_vs_power_depth()
