#!/usr/bin/env python3
"""V4 - density + champion/hero mechanics: Act-1 pool census and Normal-vs-Veteran deltas. READ-ONLY."""
import sys, pathlib, re, statistics as st
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
a=ArzArchive(ROOT/"database/database.arz")

# --- A. area001 region proxies -> which pools do they use? ---
print("="*110); print("A. AREA001 (Act 1) region proxies naming wightmire/burrwitch, and the pools they draw"); print("="*110)
pools=set()
for r in sorted(a.records):
    if not r.startswith("records/proxies/area001/"): continue
    rec=a.read_record(r)
    if str(rec.get('Class'))!='Proxy': continue
    if not any(t in r.lower() for t in ("wightmire","slith","burrwitch","lowercrossing","act1")): continue
    ps=[rec.get(f'pool{i}') for i in range(1,9) if rec.get(f'pool{i}')]
    ws=[rec.get(f'poolWeight{i}') for i in range(1,9)]
    print(f"  {r.split('area001/')[-1]:52s} spawnMin={rec.get('spawnMin')} spawnMax={rec.get('spawnMax')}")
    for p in ps:
        print(f"        -> {p}")
        pools.add(p)
print()

# --- B. full field dump of one representative Act-1 slith pool ---
print("="*110); print("B. FULL DUMP - the Act-1 slith trash pools"); print("="*110)
cands=[p for p in sorted(a.records) if p.startswith("records/proxies/pools/") and "slith" in p.lower()]
for p in cands:
    rec=a.read_record(p)
    print(f"\n  {p}   ({len(rec)} fields)")
    print(f"     spawnMin={rec.get('spawnMin')} spawnMax={rec.get('spawnMax')}  "
          f"championChance={rec.get('championChance')} championMin={rec.get('championMin')} championMax={rec.get('championMax')}")
    for i in range(1,13):
        n=rec.get(f'name{i}')
        if n: print(f"        common  w={str(rec.get(f'weight{i}')):5s} limit={str(rec.get(f'limit{i}')):5s} "
                    f"lv={str(rec.get(f'levelVarianceEquation{i}','')).split('/')[-1]:22s} {n.split('enemies/')[-1]}")
    for i in range(1,13):
        n=rec.get(f'nameChampion{i}')
        if n: print(f"        CHAMP   w={str(rec.get(f'weightChampion{i}')):5s} limit={str(rec.get(f'limitChampion{i}')):5s} "
                    f"minPL={str(rec.get(f'minPlayerLevelChampion{i}')):5s} "
                    f"lv={str(rec.get(f'levelVarianceEquationChampion{i}','')).split('/')[-1]:22s} {n.split('enemies/')[-1]}")

# --- C. census over ALL pool records that carry champion machinery ---
print()
print("="*110); print("C. CENSUS - every proxy pool with championChance (whole base DB)"); print("="*110)
rows=[]
for r in sorted(a.records):
    if not r.startswith("records/proxies/"): continue
    rec=a.read_record(r)
    cc=rec.get('championChance')
    if not cc: continue
    smin=rec.get('spawnMin') or 0; smax=rec.get('spawnMax') or 0
    cmin=rec.get('championMin') or 0; cmax=rec.get('championMax') or 0
    nchamp=sum(1 for i in range(1,13) if rec.get(f'nameChampion{i}'))
    nhero=sum(1 for i in range(1,13) if str(rec.get(f'nameChampion{i}') or '').find('/hero/')>=0)
    wtot=sum(int(rec.get(f'weightChampion{i}') or 0) for i in range(1,13) if rec.get(f'nameChampion{i}'))
    whero=sum(int(rec.get(f'weightChampion{i}') or 0) for i in range(1,13)
              if str(rec.get(f'nameChampion{i}') or '').find('/hero/')>=0)
    rows.append((r,float(cc),smin,smax,cmin,cmax,nchamp,nhero,wtot,whero))
print(f"  pools with championChance: {len(rows)}")
ccs=[x[1] for x in rows]
print(f"  championChance: min {min(ccs)}  median {st.median(ccs)}  mean {sum(ccs)/len(ccs):.2f}  max {max(ccs)}")
from collections import Counter
print("  championChance distribution:", dict(sorted(Counter(ccs).items())))
print("  championMax distribution   :", dict(sorted(Counter(x[5] for x in rows).items())))
print("  championMin distribution   :", dict(sorted(Counter(x[4] for x in rows).items())))
print("  spawnMax  distribution     :", dict(sorted(Counter(x[3] for x in rows).items())))
print("  spawnMin  distribution     :", dict(sorted(Counter(x[2] for x in rows).items())))
hw=[x[9]/x[8] for x in rows if x[8]]
print(f"  hero share of champion-roster WEIGHT: n={len(hw)} mean {sum(hw)/len(hw)*100:.1f}%  median {st.median(hw)*100:.1f}%")
print()

# --- D. Act-1 subset (the referent's world): pools reachable at low player level ---
print("="*110); print("D. ACT-1 subset  (pools referenced by area001 proxies)"); print("="*110)
a1=set()
for r in sorted(a.records):
    if not r.startswith("records/proxies/area001/"): continue
    rec=a.read_record(r)
    for i in range(1,9):
        p=rec.get(f'pool{i}')
        if p: a1.add(p)
sub=[x for x in rows if x[0] in a1]
print(f"  area001 proxies reference {len(a1)} distinct pools; {len(sub)} of them carry championChance")
if sub:
    ccs=[x[1] for x in sub]
    print(f"  championChance: min {min(ccs)} median {st.median(ccs)} mean {sum(ccs)/len(ccs):.2f} max {max(ccs)}")
    print("  distribution:", dict(sorted(Counter(ccs).items())))
    print("  championMax :", dict(sorted(Counter(x[5] for x in sub).items())))
    print("  spawnMin/Max:", dict(sorted(Counter((x[2],x[3]) for x in sub).items())))
    hw=[x[9]/x[8] for x in sub if x[8]]
    if hw: print(f"  hero weight share: mean {sum(hw)/len(hw)*100:.1f}% median {st.median(hw)*100:.1f}%")
    print("\n  per-pool rows:")
    print(f"   {'pool':56s} {'cc%':>5s} {'sMin':>4s} {'sMax':>4s} {'cMin':>4s} {'cMax':>4s} {'#ch':>3s} {'#hero':>5s} {'heroW%':>6s}")
    for r,cc,smin,smax,cmin,cmax,nc,nh,wt,wh in sorted(sub):
        print(f"   {r.split('proxies/')[-1]:56s} {cc:5.0f} {smin:4d} {smax:4d} {cmin:4d} {cmax:4d} {nc:3d} {nh:5d} "
              f"{(100*wh/wt if wt else 0):6.1f}")
