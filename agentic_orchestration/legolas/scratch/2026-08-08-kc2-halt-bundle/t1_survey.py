#!/usr/bin/env python3
"""HALT-9 step 1: full field survey of balancingadjustment_survivalmode_enemies0{1,2,3}. READ-ONLY."""
import sys, pathlib, json, collections
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
STACK = [("base", ROOT / "database/database.arz"),
         ("gdx1", ROOT / "gdx1/database/GDX1.arz"),
         ("gdx2", ROOT / "gdx2/database/GDX2.arz"),
         ("gdx3", ROOT / "gdx3/database/GDX3.arz"),
         ("sm_mod", ROOT / "mods/survivalmode/database/SurvivalMode.arz"),
         ("sm1", ROOT / "survivalmode1/database/SurvivalMode1.arz"),
         ("sm2", ROOT / "survivalmode2/database/SurvivalMode2.arz"),
         ("sm3", ROOT / "survivalmode3/database/SurvivalMode3.arz")]

RECS = {"aspirant": "records/game/balancingadjustment_survivalmode_enemies01.dbr",
        "challenger": "records/game/balancingadjustment_survivalmode_enemies02.dbr",
        "gladiator": "records/game/balancingadjustment_survivalmode_enemies03.dbr"}

# which archives contain each record (owner audit)
owners = collections.defaultdict(list)
archives = {}
for k, p in STACK:
    a = ArzArchive(p)
    archives[k] = a
    s = set(a.records)
    for diff, rp in RECS.items():
        if rp in s:
            owners[diff].append(k)

print("== OWNER AUDIT (which archive(s) contain the record) ==")
for diff, rp in RECS.items():
    print(f"  {diff:12s} {rp}  -> owners={owners[diff]}")
print()

out = {}
for diff, rp in RECS.items():
    win = owners[diff][-1]          # last-wins overlay order
    r = archives[win].read_record(rp)
    out[diff] = {"winning_archive": win, "rec": r}
    print(f"== {diff.upper()} ({win}) : {len(r)} total fields ==")

# classify fields
def nonzero(v):
    if isinstance(v, list):
        return any(abs(x) > 1e-9 for x in v if isinstance(x, (int, float)))
    if isinstance(v, (int, float)):
        return abs(v) > 1e-9
    if isinstance(v, str):
        return v.strip() not in ("", "0")
    return v is not None

rows = []
allfields = sorted(set().union(*[set(out[d]["rec"].keys()) for d in RECS]))
for f in allfields:
    rec = {}
    for d in RECS:
        v = out[d]["rec"].get(f)
        rec[d] = v
    rows.append((f, rec))

print("\n== FIELD INVENTORY ==")
print(f"{'field':52s} {'type':10s} {'len':>5s}  nz(A/C/G)   flat?(A/C/G)   idx0->idx99->idx199 (Gladiator)")
summary = []
for f, rec in rows:
    v3 = rec["gladiator"]
    typ = type(v3).__name__
    ln = len(v3) if isinstance(v3, list) else ""
    nz = "".join("Y" if nonzero(rec[d]) else "-" for d in ("aspirant", "challenger", "gladiator"))
    flat = ""
    for d in ("aspirant", "challenger", "gladiator"):
        v = rec[d]
        if isinstance(v, list) and v:
            flat += "F" if len(set(v)) == 1 else "R"
        else:
            flat += "s"
    tail = ""
    if isinstance(v3, list) and len(v3) >= 200:
        tail = f"{v3[0]} -> {v3[99]} -> {v3[199]}"
    elif isinstance(v3, list):
        tail = f"len{len(v3)}: {v3[:3]}...{v3[-1]}"
    else:
        tail = str(v3)
    print(f"{f:52s} {typ:10s} {str(ln):>5s}  {nz:9s}   {flat:9s}      {tail}")
    summary.append({"field": f, "type": typ, "len": ln, "nz": nz, "flat": flat})

json.dump({d: {k: v for k, v in out[d]["rec"].items()} for d in RECS},
          open("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-08-08-kc2-halt-bundle/t1_raw.json", "w"),
          indent=0, default=str)
print("\nwrote t1_raw.json")
