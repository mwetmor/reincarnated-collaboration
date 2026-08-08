#!/usr/bin/env python3
"""S7 — PE6 band tables: waves 1-93 full, 94-149/161-200 coarse, nemesis map, family-entry decades."""
import json, collections, pathlib, re

W = json.load(open("s4_waves_full.json"))
BY = {w["gwave"]: w for w in W}

def kind_of(p):
    if "/poolsboss" in p: return "BOSS"
    if "/poolshero" in p: return "HERO"
    if "/poolsdevotion" in p: return "DEVO"
    if "/poolsbounty" in p: return "BNTY"
    return "trash"

def wave_view(g, diff="gladiator"):
    w = BY[g]
    pts = sorted(w["points"], key=lambda x: x["pt"])
    pools, fams, kinds = [], collections.Counter(), collections.Counter()
    nem, bosses, heroes = set(), set(), set()
    ptids = []
    for e in pts:
        ptids.append(e["pt"])
        seen = set()
        for o in e["diffs"][diff]:
            if o.get("UNRESOLVED") or o["pool"] in seen: continue
            seen.add(o["pool"])
            k = kind_of(o["pool"]); kinds[k] += 1
            stem = pathlib.Path(o["pool"]).stem
            pools.append((e["pt"], k, stem, o["smin"], o["smax"], o["cch"], o["cmax"]))
            fams[re.sub(r"_t\d$|_hero$|_ambush.*$", "", stem)] += 1
            if "nemesis" in stem or "/nemesis" in o["pool"]:
                nem.add(stem)
                for r in o["roster"]: nem.add(r["name"])
            if k == "BOSS":
                for r in o["roster"]: bosses.add(r["name"])
            if k in ("HERO", "DEVO", "BNTY"):
                for r in o["champroster"] + o["roster"]: heroes.add(r["name"])
    return dict(g=g, tier=w["tier"], wave=w["wave"], pts=ptids, pools=pools, fams=fams,
                kinds=kinds, nem=nem, bosses=bosses, heroes=heroes,
                stat=w[diff], amb=[e for e in pts if e["cls"] == "ProxyAmbush"])

def classify(v):
    k = v["kinds"]
    if v["nem"]: return "NEMESIS"
    if k.get("BOSS") and not k.get("trash"): return "BOSS-ONLY"
    if k.get("BOSS"): return "boss+trash"
    if not k.get("trash") and (k.get("HERO") or k.get("DEVO") or k.get("BNTY")): return "HERO-ONLY"
    if k.get("HERO") or k.get("DEVO") or k.get("BNTY"): return "hero+trash"
    return "trash"

print("=" * 132)
print("BAND A — WAVES 1..93 (Gladiator view). pools column = spawn-point:KIND:pool-stem(spawnMin-spawnMax[,champ%])")
print("=" * 132)
print(f"{'wave':>4} {'t/w':>6} {'pts':>10} {'min':>4} {'max':>4} {'E':>6} {'class':>10}  pools")
for g in range(1, 94):
    v = wave_view(g)
    ps = " · ".join(f"p{pt}:{k[:4]}:{st}({sm:.0f}-{sx:.0f}{f',c{cc:.0f}%' if cc else ''})"
                    for pt, k, st, sm, sx, cc, cm in v["pools"])
    print(f"{g:4d} {v['tier']:2d}/{v['wave']:<3d} {str(v['pts']):>10} {v['stat']['min']:4.0f} "
          f"{v['stat']['max']:4.0f} {v['stat']['E']:6.2f} {classify(v):>10}  {ps}")

print("\n\n" + "=" * 132)
print("NEMESIS MAP — every wave whose Gladiator composition draws from a nemesis_* pool")
print("=" * 132)
nemwaves = []
for g in range(1, 201):
    v = wave_view(g)
    if v["nem"]:
        pools = [f"p{pt}:{st}" for pt, k, st, *_ in v["pools"] if "nemesis" in st]
        names = sorted(n for n in v["nem"] if not n.startswith("nemesis"))
        nemwaves.append((g, pools, names))
        print(f"  wave {g:3d} (t{v['tier']:02d}w{v['wave']:02d})  {', '.join(pools)}")
        print(f"            roster: {', '.join(names)}")
print(f"\n  TOTAL nemesis waves: {len(nemwaves)}  -> {[g for g,_,_ in nemwaves]}")

print("\n\n" + "=" * 132)
print("ZANTARIN MAP — every wave whose Gladiator composition can spawn 'Zantarin, the Immortal'")
print("=" * 132)
zw = []
for g in range(1, 201):
    v = wave_view(g)
    hit = []
    for e in BY[g]["points"]:
        for o in e["diffs"]["gladiator"]:
            if o.get("UNRESOLVED"): continue
            for r in o["roster"] + o["champroster"]:
                if "Zantarin" in (r["name"] or ""):
                    n = len(o["roster"]) or 1
                    hit.append((e["pt"], pathlib.Path(o["pool"]).stem, 1.0 / n))
    if hit:
        zw.append((g, hit))
        pz = 1 - 1.0
        # P(at least one Zantarin) across independent spawn points
        q = 1.0
        for _, _, p in hit: q *= (1 - p)
        print(f"  wave {g:3d}: " + ", ".join(f"p{pt}/{st} p={p:.3f}" for pt, st, p in hit)
              + f"   -> P(Zantarin in wave) = {1-q:.3f}")
print(f"\n  TOTAL waves that can present Zantarin: {len(zw)} -> {[g for g,_ in zw]}")

print("\n\n" + "=" * 132)
print("BAND B — coarse decade summary, waves 1..200 (Gladiator)")
print("=" * 132)
print(f"{'decade':>10} {'Σmin':>6} {'Σmax':>6} {'ΣE':>8} {'classes':<58} new families entering")
seenfam = set()
for d0 in range(1, 201, 10):
    vs = [wave_view(g) for g in range(d0, d0 + 10)]
    cls = collections.Counter(classify(v) for v in vs)
    newf = []
    for v in vs:
        for f in v["fams"]:
            if f not in seenfam:
                seenfam.add(f); newf.append(f)
    print(f"{d0:4d}-{d0+9:<5d} {sum(v['stat']['min'] for v in vs):6.0f} {sum(v['stat']['max'] for v in vs):6.0f} "
          f"{sum(v['stat']['E'] for v in vs):8.2f} {str(dict(cls)):<58} {len(newf)}: {', '.join(newf[:9])}")

print("\n\n" + "=" * 132)
print("SPAWN-POINT OCCUPANCY — which of p01..p06 are defined, per decade")
print("=" * 132)
for d0 in range(1, 201, 10):
    c = collections.Counter()
    for g in range(d0, d0 + 10):
        for pt in wave_view(g)["pts"]: c[pt] += 1
    print(f"  {d0:3d}-{d0+9:3d}: " + "  ".join(f"p{k:02d}={c.get(k,0):2d}/10" for k in range(1, 7)))

print("\n\n" + "=" * 132)
print("AMBUSH (sustained-population) SPAWN POINTS across the Crucible")
print("=" * 132)
n = 0
for g in range(1, 201):
    v = wave_view(g)
    for e in v["amb"]:
        n += 1
        a = e["ambush"]
        print(f"  wave {g:3d} p{e['pt']:02d}: minGrp={a['minGroupSize']} maxGrp={a['maxGroupSize']} "
              f"thresh={a['spawnThreshold']} spawn={a['minSpawnTime']}-{a['maxSpawnTime']}s "
              f"delay={a['minDelayTime']}-{a['maxDelayTime']}s alert={a['alertArea']}")
print(f"  TOTAL ProxyAmbush spawn points: {n}")
