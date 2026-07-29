#!/usr/bin/env python3
"""probe5 — locate the mastery-tier threshold data.
(a) all skill*/tier*/require*/level* field names on the Oathkeeper mastery record
(b) per-skill (skillTier, skillMasteryLevelRequired, skillMaxLevel) census for playerclass09
(c) global string-table scan for any field-name-shaped token containing 'ier'/'equire'
Read-only."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [ROOT / "database/database.arz", ROOT / "gdx1/database/GDX1.arz",
        ROOT / "gdx2/database/GDX2.arz", ROOT / "gdx3/database/GDX3.arz"]
archives = {p.name: ArzArchive(p) for p in ARZS}

M = "records/skills/playerclass09/_classtraining_class09.dbr"
print("=== (a) mastery-record fields matching tier/require/level/max/skill ===")
for name, a in archives.items():
    if M not in a.records:
        continue
    rec = a.read_record(M)
    for k in sorted(rec):
        if re.search(r"(tier|Tier|equire|Level|level|Max|max)", k):
            v = rec[k]
            s = f"[n={len(v)}] {v[:6]}...{v[-3:]}" if isinstance(v, list) else repr(v)
            print(f"  {name:14s} {k:40s} {s}")
    print()

print("=== (b) playerclass09 skill census: tier / masteryLevelRequired / maxLevel ===")
# GDX2 is the Oathkeeper home; GDX3 may override.
rows = {}
for name in ("database.arz", "GDX2.arz", "GDX3.arz"):
    a = archives[name]
    for r in sorted(a.records):
        if not r.startswith("records/skills/playerclass09/"):
            continue
        rec = a.read_record(r)
        if "skillTier" not in rec and "skillMasteryLevelRequired" not in rec:
            continue
        rows[r] = (name, rec.get("skillTier"), rec.get("skillMasteryLevelRequired"),
                   rec.get("skillMaxLevel"), rec.get("skillUltimateLevel"), rec.get("Class"))
for r in sorted(rows, key=lambda x: (rows[x][1] if rows[x][1] is not None else -1, x)):
    name, tier, mlr, mx, ult, cls = rows[r]
    print(f"  tier={tier!s:>4}  masteryLvlReq={mlr!s:>4}  max={mx!s:>4} ult={ult!s:>4}  "
          f"{r.split('/')[-1]:44s} [{cls}]  <-{name}")

print("\n=== (c) string-table tokens looking like tier/requirement field names ===")
toks = set()
for name, a in archives.items():
    for s in a.strings:
        if len(s) < 40 and "/" not in s and "." not in s and re.search(r"(Tier|Require|MasteryLevel)", s):
            toks.add(s)
for t in sorted(toks):
    print("  ", t)
