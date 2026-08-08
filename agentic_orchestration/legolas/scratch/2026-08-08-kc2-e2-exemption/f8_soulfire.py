#!/usr/bin/env python3
"""F-8 RIDER -- Soulfire cost-record re-read. READ-ONLY.

Adjudicate, from the record + its template + its localisation tags ONLY:
  Q1  is skillManaCost 3-20 a per-interval INCREMENT or a TOTAL cost?
  Q2  does the cost gate on PROJECTILE LAUNCHES or on DAMAGE INTERVALS?
  Q3  what does the rank table hold at total rank 15?
Mirror of the P-E1 3.1 unit-decomposition discipline.  Cite verbatim; conclude nothing the
record + template do not state.
"""
import sys, pathlib, collections, re, json
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
from gd_arc_reader_2026_07_26 import ArcArchive, parse_tag_file

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
def get(p):
    return ARC[WHERE[p][-1]].read_record(p) if p in WHERE else None
def rt(p):
    return ARC[WHERE[p][-1]].record_type(p) if p in WHERE else None

TAGS = {}
for arc in sorted(ROOT.rglob("[Tt]ext_[Ee][Nn].arc")):
    try: A = ArcArchive(arc)
    except Exception: continue
    for name in A.names():
        if not name.lower().endswith(".txt"): continue
        try: d = parse_tag_file(A.read_file(name))
        except Exception: continue
        for k, v in d:
            TAGS.setdefault(k, (v, f"{arc.parent.parent.name}/{name}"))
print(f"loaded {len(TAGS)} localisation tags\n")

REC = "records/skills/playerclass09/eyeofreckoning2.dbr"
BASE = "records/skills/playerclass09/eyeofreckoning1.dbr"

for path in (REC, BASE):
    r = get(path)
    print("=" * 108)
    print(f"{path}   archives={WHERE[path]}   Class={r.get('Class')!r}  recordType={rt(path)!r}")
    print(f"   templateName = {r.get('templateName')!r}   fields={len(r)}")
    print("=" * 108)
    for k in sorted(r):
        v = r[k]
        if isinstance(v, list) and len(v) > 8:
            print(f"   {k:38s} [{len(v):2d}] = {v}")
        else:
            print(f"   {k:38s}      = {v!r}")
    print()

# ---------------------------------------------------------------- Q3 rank table
print("=" * 108)
print("Q3  RANK TABLE at total rank 15   (arrays are 1-based by rank; python index = rank-1)")
print("=" * 108)
r2 = get(REC); r1 = get(BASE)
def col(rec, f):
    v = rec.get(f)
    return v if isinstance(v, list) else ([v] if v is not None else [])
FIELDS = [f for f in sorted(r2) if isinstance(r2[f], list) and len(r2[f]) > 1]
print(f"  rank-scaled fields on eyeofreckoning2 ({len(FIELDS)}): array lengths "
      f"{sorted(set(len(r2[f]) for f in FIELDS))}")
print(f"\n  {'field':40s} {'len':>4s} {'r13':>9s} {'r14':>9s} {'r15':>9s} {'r16':>9s} {'r22(max)':>9s}")
for f in FIELDS:
    v = r2[f]
    def at(k):
        return f"{v[k-1]}" if 1 <= k <= len(v) else "-"
    print(f"  {f:40s} {len(v):4d} {at(13):>9s} {at(14):>9s} {at(15):>9s} {at(16):>9s} {at(len(v)):>9s}")

mc = r2.get("skillManaCost")
print(f"\n  skillManaCost FULL = {mc}")
if isinstance(mc, list):
    print(f"  len={len(mc)}  rank15 -> mc[14] = {mc[14]}   max rank{len(mc)} -> {mc[-1]}")

# ---------------------------------------------------------------- Q1/Q2 tags
print("\n" + "=" * 108)
print("Q1/Q2  LOCALISATION -- every tag the two records point at, VERBATIM")
print("=" * 108)
seen = set()
for path, rec in ((REC, r2), (BASE, r1)):
    print(f"\n  --- {path} ---")
    for k in sorted(rec):
        v = rec[k]
        if not isinstance(v, str): continue
        if not (v.startswith("tag") or "Description" in k or k in ("skillDisplayName", "FileDescription")):
            continue
        if v in TAGS:
            txt, src = TAGS[v]
            print(f"    {k:28s} {v:34s} [{src}]\n        {txt!r}")
            seen.add(v)
        elif v.startswith("tag"):
            print(f"    {k:28s} {v:34s} <TAG NOT FOUND>")

# neighbouring description sub-tags (Crate splits long descriptions across ...A/...B/...C)
print("\n  --- neighbouring sub-tags of the same stems ---")
stems = set()
for v in seen:
    stems.add(re.sub(r"[A-Z]?$", "", v))
for stem in sorted(stems):
    for k in sorted(TAGS):
        if k.startswith(stem) and k not in seen:
            print(f"    {k:38s} {TAGS[k][0]!r}")

# ---------------------------------------------------------------- the 'per damage interval' tag family
print("\n" + "=" * 108)
print("Q1/Q2  EVERY tag in the corpus containing 'per damage interval' / 'Energy Cost'")
print("=" * 108)
pat = re.compile(r"per damage interval|Energy Cost", re.I)
hits = [(k, v[0], v[1]) for k, v in TAGS.items() if pat.search(v[0] or "")]
print(f"  {len(hits)} tags match")
for k, v, src in sorted(hits):
    print(f"    {k:40s} [{src}]\n        {v!r}")
