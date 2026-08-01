#!/usr/bin/env python3
"""P14 - verify SR floorTotal semantics: does a literal commonProxies field exist? spawn adj values? SR pool min/max split. READ-ONLY."""
import sys, pathlib, collections, statistics as st
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
g2=ArzArchive(ROOT/"gdx2/database/GDX2.arz")

print("### full field-name union for EndlessDungeonGenerator - is there a literal 'commonProxies'?")
fu=collections.Counter()
for r in g2.records:
    rec=g2.read_record(r)
    if str(rec.get('Class'))=='EndlessDungeonGenerator':
        for k in rec: fu[k]+=1
names=sorted(fu)
print("  fields:", names)
print("  'commonProxies' present as literal field:", 'commonProxies' in fu)
print("  proxy-count-ish fields:", [k for k in names if 'roxies' in k or 'roxy' in k])

print("\n### spawn adjustment values in SR difficultyscaling")
for r in sorted(g2.records):
    if "endlessdungeon/difficultyscaling/balanceadjustment" in r:
        rec=g2.read_record(r)
        print(f"  {r.split('/')[-1]}: spawnMinAdj={rec.get('spawnMinAdj')} spawnMaxAdj={rec.get('spawnMaxAdj')} "
              f"spawnChampionMaxAdj={rec.get('spawnChampionMaxAdj')}")

print("\n### SR poolsbasic spawnMin/spawnMax split (n, distributions)")
mn=[];mx=[]
for r in sorted(g2.records):
    if "endlessdungeon/proxies/poolsbasic" in r:
        rec=g2.read_record(r)
        if rec.get('spawnMin') is None: continue
        mn.append(float(rec['spawnMin'])); mx.append(float(rec['spawnMax']))
print(f"  n={len(mn)} spawnMin: {dict(sorted(collections.Counter(mn).items()))}")
print(f"           spawnMax: {dict(sorted(collections.Counter(mx).items()))}")
print(f"  mean min={sum(mn)/len(mn):.2f} mean max={sum(mx)/len(mx):.2f}")

print("\n### SR poolshero / poolsboss spawn fields")
for tag in ("poolshero","poolsboss"):
    vals=[]
    for r in sorted(g2.records):
        if f"endlessdungeon/proxies/{tag}" in r:
            rec=g2.read_record(r)
            vals.append((rec.get('spawnMin'),rec.get('spawnMax'),rec.get('championChance'),rec.get('championMax')))
    print(f"  {tag}: n={len(vals)} distinct (sMin,sMax,cChance,cMax)={dict(collections.Counter(vals).most_common(6))}")

print("\n### ProxyEndless count by subtree (gdx2)")
c=collections.Counter()
for r in g2.records:
    if str(g2.read_record(r).get('Class'))=='ProxyEndless':
        c[r.split('/')[3] if r.count('/')>3 else r]+=1
print("  ",dict(c.most_common(15)))
