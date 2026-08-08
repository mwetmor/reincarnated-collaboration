#!/usr/bin/env python3
"""F3 residual: deep read of the p04 superboss path. READ-ONLY."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, index, find, read

print("=" * 106)
print("A — p04 pool records, ALL fields (are there pool2 / legendary overrides?)")
print("=" * 106)
for p in ("records/proxies/poolsbossgdx1/aetherialcolossus_galakros.dbr",
          "records/proxies/poolsbossgdx2/korvaaktombguardian.dbr",
          "records/proxies/tier16waves/proxy_w10_p04a.dbr"):
    rec, prov, own = merged(p)
    print(f"\n-- {p}  owners={own}")
    for f in sorted(rec):
        print(f"     {f:44s} = {str(rec[f])[:78]:78s} [{prov[f]}]")

print("\n" + "=" * 106)
print("B — Galakros record: per-archive diff of the HP-relevant fields")
print("=" * 106)
P = "records/creatures/enemies/boss&quest/aetherialcolossus_galakros.dbr"
KEYS = ("charLevel", "characterAttributeEquations", "characterLife", "characterLifeModifier",
        "monsterClassification", "minLevel", "maxLevel", "Class")
for k in index()[P.lower()]:
    r, _ = read(P, which=k)
    print(f"   [{k}] " + "  ".join(f"{a}={r.get(a)!r}" for a in KEYS))

print("\n" + "=" * 106)
print("C — Galakros bio: per-archive diff")
print("=" * 106)
B = "records/creatures/enemies/bios/bio_boss_aetherial_colossusgalakros.dbr"
for k in index()[B.lower()]:
    r, _ = read(B, which=k)
    print(f"   [{k}] characterLife = {r.get('characterLife')!r}")
B2 = "records/creatures/enemies/bios/bio_boss_tombguardian.dbr"
for k in index()[B2.lower()]:
    r, _ = read(B2, which=k)
    print(f"   [{k}] (tombguardian) characterLife = {r.get('characterLife')!r}")

print("\n" + "=" * 106)
print("D — any OTHER record in the corpus referencing the galakros/tombguardian pools")
print("=" * 106)
for tok in ("aetherialcolossus_galakros", "korvaaktombguardian"):
    hits = []
    for p in index():
        if "/proxies/" not in p:
            continue
        rec, prov, own = merged(p)
        for f, v in rec.items():
            if isinstance(v, str) and tok in v.lower():
                hits.append((p, f, v))
    print(f"\n   {tok}: {len(hits)} proxy references")
    for h in hits[:24]:
        print(f"      {h[0]:58s} {h[1]:14s} -> {h[2].split('/')[-1]}")

print("\n" + "=" * 106)
print("E — hero bios with extra health (is the p06 slot maybe not bio_hero_standard_01?)")
print("=" * 106)
for b in sorted(p for p in index() if "bio_hero" in p):
    rec, prov, own = merged(b)
    print(f"   {b.split('/')[-1]:44s} {str(rec.get('characterLife')):34s} [{own}]")
