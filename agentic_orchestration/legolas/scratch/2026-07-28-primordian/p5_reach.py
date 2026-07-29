#!/usr/bin/env python3
"""P5 — reachability. (a) which SR boss-proxy families exist & does Primordian appear in the
'all' (expansions-owned) variants? (b) Crucible tier->wave mapping + survivalinfo. (c) difficulty
scaling tables."""
import sys, pathlib, re, collections
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
gdx2 = ArzArchive(ROOT / "gdx2/database/GDX2.arz")
gdx3 = ArzArchive(ROOT / "gdx3/database/GDX3.arz")
sm   = ArzArchive(ROOT / "mods/survivalmode/database/SurvivalMode.arz")
base = ArzArchive(ROOT / "database/database.arz")

print("#"*84); print("# A — SR: Primordian membership across EVERY boss-proxy family"); print("#"*84)
fam = collections.defaultdict(lambda: [0, 0])   # family -> [n_variants, n_with_primordian]
for rp in sorted(gdx2.records):
    if "endlessdungeon/proxies/proxy_boss/" not in rp or rp.endswith("_blank.dbr"):
        continue
    r = gdx2.read_record(rp)
    pools = [v for k, v in r.items() if k.startswith("pool")]
    hit = any("slith_primordian" in str(v) for v in pools)
    famname = re.sub(r"_\d+\.dbr$", "", rp.split("/")[-1])
    fam[famname][0] += 1
    fam[famname][1] += int(hit)
    if hit:
        fam[famname].append(len(pools))
print(f"{'family':34s} {'variants':>9s} {'w/Primordian':>13s}  poolcount")
for f in sorted(fam):
    v = fam[f]
    print(f"  {f:32s} {v[0]:>9d} {v[1]:>13d}  {v[2] if len(v)>2 else ''}")

# does gdx3 add/override any endlessdungeon boss proxy?
print("\ngdx3 endlessdungeon proxy_boss overrides:")
g3 = [rp for rp in gdx3.records if "endlessdungeon/proxies/proxy_boss/" in rp]
print(f"  count={len(g3)}")
for rp in sorted(g3)[:60]:
    r = gdx3.read_record(rp)
    pools = [v for k, v in r.items() if k.startswith("pool")]
    hit = any("slith_primordian" in str(v) for v in pools)
    print(f"   {'PRIMORDIAN' if hit else '          '} {rp}  (pools={len(pools)})")

print("\n#"*1 + "#"*83); print("# B — who selects a boss-proxy family? (reverse refs on the families Primordian is in)")
print("#"*84)
NEEDLE = ["proxy_bossbaseeasy01", "proxy_bossbasefull02"]
for tag, a in [("gdx2", gdx2), ("gdx3", gdx3)]:
    if not any(any(n in s for n in NEEDLE) for s in a.strings):
        print(f"[{tag}] needle absent"); continue
    for rp in sorted(a.records):
        if "proxy_boss/" in rp:
            continue
        try: r = a.read_record(rp)
        except Exception: continue
        for k, v in r.items():
            for item in (v if isinstance(v, list) else [v]):
                if isinstance(item, str) and any(n in item for n in NEEDLE):
                    print(f"  [{tag}] {rp}\n        {k} = {item}")

print("\n" + "#"*84); print("# C — Crucible survivalinfo + difficulty scaling"); print("#"*84)
for rp in ["records/game/survivalinfo.dbr",
           "records/game/balancingadjustment_survivalmode_enemies01.dbr",
           "records/game/balancingadjustment_survivalmode_enemies02.dbr",
           "records/game/balancingadjustment_survivalmode_enemies03.dbr"]:
    print(f"\n--- [sm] {rp} ---")
    try: r = sm.read_record(rp)
    except KeyError: print("  NOT PRESENT"); continue
    for k in sorted(r):
        v = r[k]
        if isinstance(v, list) and len(v) > 12:
            v = f"[len={len(v)}] {v[:8]} ... {v[-3:]}"
        print(f"  {k:44s} = {v}")

print("\n--- [base] records/game/balancingadjustment_mp+difficulty_enemies01.dbr ---")
r = base.read_record("records/game/balancingadjustment_mp+difficulty_enemies01.dbr")
for k in sorted(r):
    print(f"  {k:44s} = {r[k]}")
