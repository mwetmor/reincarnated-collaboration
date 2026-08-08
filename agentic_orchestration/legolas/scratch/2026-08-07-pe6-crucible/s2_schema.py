#!/usr/bin/env python3
"""S2 — PE6 wave-record schema + tier<->wave mapping evidence. READ-ONLY."""
import sys, pathlib, collections, re, json
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
STACK = [("sm_mod", ROOT / "mods/survivalmode/database/SurvivalMode.arz"),
         ("sm1", ROOT / "survivalmode1/database/SurvivalMode1.arz"),
         ("sm2", ROOT / "survivalmode2/database/SurvivalMode2.arz"),
         ("sm3", ROOT / "survivalmode3/database/SurvivalMode3.arz")]
CAMP = [("base", ROOT / "database/database.arz"), ("gdx1", ROOT / "gdx1/database/GDX1.arz"),
        ("gdx2", ROOT / "gdx2/database/GDX2.arz"), ("gdx3", ROOT / "gdx3/database/GDX3.arz")]
M = {}
for k, p in CAMP + STACK:
    a = ArzArchive(p)
    for r in a.records:
        M[r] = (k, a)
def get(p):
    e = M.get(str(p)); return e[1].read_record(str(p)) if e else None
def own(p):
    e = M.get(str(p)); return e[0] if e else None

# ---------- A. field union on spawn-point proxies, split by class
PAT = re.compile(r"^records/proxies/tier(\d+)waves/proxy_w(\d+)_p(\d+)a\.dbr$")
byclass = collections.defaultdict(collections.Counter)
clscount = collections.Counter()
wavepaths = []
for path, (o, a) in M.items():
    m = PAT.match(path)
    if not m: continue
    wavepaths.append(path)
    rec = a.read_record(path)
    cls = a.record_type(path)
    clscount[cls] += 1
    for f in rec: byclass[cls][f] += 1
print("=== spawn-point proxy record classes ===", dict(clscount))
for cls, fc in byclass.items():
    print(f"\n--- class {cls} (n={clscount[cls]}) field union ---")
    for f, c in fc.most_common():
        print(f"   {c:4d}  {f}")

# ---------- B. one full wave record verbatim
sample = "records/proxies/tier16waves/proxy_w10_p01a.dbr"
print(f"\n=== VERBATIM {sample}  (owner={own(sample)}) ===")
rec = get(sample)
for k, v in rec.items(): print(f"   {k} = {v}")

# ---------- C. pool record field union (the second hop)
poolpaths = set()
for path in wavepaths:
    r = get(path)
    for i in range(1, 13):
        p = r.get(f"pool{i}")
        if p: poolpaths.add(str(p))
print(f"\n=== distinct pools referenced by ALL 925 wave proxies: {len(poolpaths)} ===")
unres = [p for p in poolpaths if p not in M]
print(f"unresolved: {len(unres)}", unres[:10])
pfields = collections.Counter(); pcls = collections.Counter()
for p in poolpaths:
    if p not in M: continue
    pr = get(p); pcls[M[p][1].record_type(p)] += 1
    for f in pr: pfields[f] += 1
print("pool classes:", dict(pcls))
print("pool field union (top 60):")
for f, c in pfields.most_common(60): print(f"   {c:4d}  {f}")

# ---------- D. tier<->wave mapping evidence
print("\n=== tier<->global-wave mapping evidence ===")
for p in ["records/game/survivalinfo.dbr", "records/game/gameproxies.dbr"]:
    r = get(p)
    print(f"\n--- {p} owner={own(p)} ---")
    if r:
        for k, v in r.items(): print(f"   {k} = {v}")

# any record with 'tier' in path outside proxies
tierrecs = sorted(x for x in M if "tier" in x.lower() and "/proxies/" not in x and "devotion" not in x.lower())
print(f"\nrecords with 'tier' in path outside proxies/devotion: {len(tierrecs)}")
for x in tierrecs[:60]: print("   ", x, "|", own(x))

# survivalpane / ui
ui = sorted(x for x in M if "survivalpane" in x or "/survival" in x)
print(f"\nsurvival ui/game records: {len(ui)}")
for x in ui[:40]: print("   ", x, "|", own(x))
