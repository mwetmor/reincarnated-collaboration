#!/usr/bin/env python3
"""P10 - campaign gameproxies difficulty scaler + named-location probe + endlessdungeon(SR) + monstertotem. READ-ONLY."""
import sys, pathlib, collections, re, json
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
CAMP=[("base",ROOT/"database/database.arz"),("gdx1",ROOT/"gdx1/database/GDX1.arz"),
      ("gdx2",ROOT/"gdx2/database/GDX2.arz"),("gdx3",ROOT/"gdx3/database/GDX3.arz")]
M={}
for k,p in CAMP:
    a=ArzArchive(p)
    for r in a.records: M[r]=(k,a)
def get(p):
    e=M.get(p); return e[1].read_record(p) if e else None

print("### campaign records/game/gameproxies.dbr (difficulty density scaler)")
for k,p in CAMP:
    a=ArzArchive(p)
    if "records/game/gameproxies.dbr" in a.records:
        rec=a.read_record("records/game/gameproxies.dbr")
        print(f"  [{k}]")
        for kk,vv in sorted(rec.items()): print(f"     {kk} = {vv}")

print("\n### NAMED-LOCATION TOKEN PROBE (path substring match over records/proxies/)")
TOK={"wardens/burrwitch":["warden","burrwitch"],"cronley":["cronley"],"portvalbury":["portvalbury","valbury"],
     "bastionofchaos":["bastionofchaos"],"stepsoftorment":["stepsoftorment"],"fleshworks":["fleshwork"],
     "ancientgrove":["ancientgrove","grove"],"tombofheretic":["heretic"],"shatteredrealm":["shatteredrealm","endlessdungeon","sr_"],
     "wightmire":["wightmire"],"malmouth":["malmouth"],"twinfalls":["twinfalls"],"depraved sanctuary":["depraved","sanctuary"],
     "steelcap":["steelcap"],"hiddenpath":["hiddenpath"],"crown hill":["crownhill"],"darkvale":["darkvale"],
     "gloomwald":["gloomwald"],"korvan":["korvan"],"asterkarn":["asterkarn"]}
prox=[r for r in M if r.startswith("records/proxies/")]
for label,toks in TOK.items():
    hits=[r for r in prox if any(t in r.lower() for t in toks)]
    print(f"  {label:22s} -> {len(hits)} proxy-tree records")

print("\n### endlessdungeon top-level tree (gdx2/gdx3) - Shattered Realm")
for k,p in [("gdx2",ROOT/"gdx2/database/GDX2.arz"),("gdx3",ROOT/"gdx3/database/GDX3.arz")]:
    a=ArzArchive(p)
    ed=[r for r in a.records if r.startswith("records/endlessdungeon/")]
    print(f"  [{k}] n={len(ed)}")
    seg=collections.Counter(r.split("/")[2] for r in ed)
    print("      seg2:",dict(seg.most_common(20)))
    cl=collections.Counter(str(a.read_record(r).get('Class')) for r in ed)
    print("      Class:",dict(cl.most_common(20)))

print("\n### monstertotem tree (gdx2/gdx3)")
for k,p in [("gdx2",ROOT/"gdx2/database/GDX2.arz"),("gdx3",ROOT/"gdx3/database/GDX3.arz")]:
    a=ArzArchive(p)
    mt=[r for r in a.records if "monstertotem" in r]
    print(f"  [{k}] n={len(mt)}  sample: {mt[:3]}")
    cl=collections.Counter(str(a.read_record(r).get('Class')) for r in mt)
    print("      Class:",dict(cl))
