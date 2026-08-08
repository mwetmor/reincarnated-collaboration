#!/usr/bin/env python3
"""S6 — PE6: (a) werewolf-family confound scan across the whole Crucible composition,
(b) Gladiator balancing adjustment, (c) arena spawn geometry. READ-ONLY."""
import sys, json, pathlib, collections, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ORDER = [("base", ROOT / "database/database.arz"), ("gdx1", ROOT / "gdx1/database/GDX1.arz"),
         ("gdx2", ROOT / "gdx2/database/GDX2.arz"), ("gdx3", ROOT / "gdx3/database/GDX3.arz"),
         ("sm_mod", ROOT / "mods/survivalmode/database/SurvivalMode.arz"),
         ("sm1", ROOT / "survivalmode1/database/SurvivalMode1.arz"),
         ("sm2", ROOT / "survivalmode2/database/SurvivalMode2.arz"),
         ("sm3", ROOT / "survivalmode3/database/SurvivalMode3.arz")]
M = {}
for k, p in ORDER:
    a = ArzArchive(p)
    for r in a.records: M[r] = (k, a)
def get(p):
    e = M.get(str(p)); return e[1].read_record(str(p)) if e else None
def own(p):
    e = M.get(str(p)); return e[0] if e else None

W = json.load(open("s4_waves_full.json"))

# ---------------------------------------------------------------- (a) WEREWOLF CONFOUND SCAN
# Two surfaces. (1) record-path tokens. (2) display-name tokens.
PATH_TOK = ["werewolf", "wereraven", "wereform", "lycan", "shifter", "berserker", "direwolf",
            "wolf", "wendigo", "hypporaven", "raven"]
NAME_TOK = ["werewolf", "wereraven", "were-", "lycan", "wolf", "howl", "wendigo", "raven"]

occ = collections.defaultdict(list)     # token -> [(gwave, pool, monster_record, name)]
allmon = {}                             # monster record -> name
poolmon = collections.defaultdict(set)  # monster record -> set of gwaves
for w in W:
    g = w["gwave"]
    for e in w["points"]:
        seen = set()
        for d in ("aspirant", "challenger", "gladiator"):
            for o in e["diffs"][d]:
                if o.get("UNRESOLVED"): continue
                key = (o["pool"],)
                if key in seen: continue
                seen.add(key)
                for r in o["roster"] + o["champroster"]:
                    allmon[r["rec"]] = r["name"]
                    poolmon[r["rec"]].add(g)
                    lp, ln = r["rec"].lower(), (r["name"] or "").lower()
                    for t in PATH_TOK:
                        if t in lp: occ[t].append((g, o["pool"], r["rec"], r["name"]))
                    for t in NAME_TOK:
                        if t in ln: occ["NAME:" + t].append((g, o["pool"], r["rec"], r["name"]))

print("=" * 100)
print("WEREWOLF-FAMILY CONFOUND SCAN — Crucible composition, all 200 waves, all 3 difficulty views")
print("=" * 100)
print(f"distinct monster records appearing anywhere in the Crucible: {len(allmon)}")
for t in PATH_TOK + ["NAME:" + x for x in NAME_TOK]:
    rows = occ.get(t, [])
    recs = sorted(set(r[2] for r in rows))
    gws = sorted(set(r[0] for r in rows))
    print(f"\n-- token '{t}': {len(rows)} (wave,pool,record) occurrences | {len(recs)} distinct records "
          f"| {len(gws)} distinct waves")
    if not rows: continue
    print(f"   waves: {gws}")
    for rec in recs[:60]:
        print(f"     {allmon[rec]:52s} {rec}   [{own(rec)}]  waves={sorted(poolmon[rec])[:14]}")

# TRUE werewolf check: does GD have ANY record path containing 'werewolf'/'wereraven' at all?
print("\n" + "=" * 100)
print("CORPUS-WIDE: any record whose PATH contains werewolf / wereraven / lycan (whole 8 archives)")
print("=" * 100)
for tok in ("werewolf", "wereraven", "lycan", "shifter"):
    hits = sorted(p for p in M if tok in p.lower())
    print(f"\n  '{tok}': {len(hits)} records")
    for h in hits[:40]: print(f"      {h}  [{own(h)}]")

# ---------------------------------------------------------------- (b) GLADIATOR SCALARS
print("\n" + "=" * 100)
print("GLADIATOR (Ultimate) SURVIVAL BALANCING ADJUSTMENT")
print("=" * 100)
for p in ["records/game/balancingadjustment_survivalmode_enemies01.dbr",
          "records/game/balancingadjustment_survivalmode_enemies02.dbr",
          "records/game/balancingadjustment_survivalmode_enemies03.dbr"]:
    r = get(p)
    print(f"\n--- {p}  [{own(p)}] ---")
    if r is None: print("   MISSING"); continue
    for k, v in sorted(r.items()): print(f"   {k} = {v}")

# ---------------------------------------------------------------- (c) ARENA GEOMETRY
print("\n" + "=" * 100)
print("ARENA / SPAWN GEOMETRY — is it DB-resident?")
print("=" * 100)
for p in sorted(x for x in M if "spawnpoint" in x.lower() or "spawnbeacon" in x.lower()):
    r = get(p)
    print(f"\n--- {p}  [{own(p)}] ---")
    for k, v in sorted(r.items()):
        print(f"   {k} = {v}")
    if p.endswith("tier01spawnpoint01.dbr"): pass
