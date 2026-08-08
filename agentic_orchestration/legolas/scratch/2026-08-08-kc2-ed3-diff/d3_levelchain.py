#!/usr/bin/env python3
"""D3 — the level chain: pool -> levelVarianceEquation -> proxy formula -> record charLevel.
Edition-II pin (fixture substrate). READ-ONLY."""
import sys
sys.path.insert(0, ".")
import lib2
E2 = lib2.E2

def dump(p, keys=None):
    r, ow = E2.merged(p)
    if r is None:
        print(f"   [ABSENT] {p}"); return {}
    print(f"   {p}  owners={ow}")
    if keys is None:
        for k in sorted(r):
            print(f"       {k:34s} = {r[k]}")
    else:
        for k in keys:
            if k in r: print(f"       {k:34s} = {r[k]}")
    return r

print("=== A. lv proxy formulas (records/proxies/lv*.dbr) ===")
for p in sorted(E2.find("records/proxies/lv")):
    r,_ = E2.merged(p)
    ks = {k:v for k,v in r.items() if "level" in k.lower() or "Equation" in k}
    print(f"   {p}\n       {ks}")

print("\n=== B. hero pools on w152 ===")
for p in ["records/proxies/poolsherogdx1/basilisk_hero.dbr",
          "records/proxies/poolsherogdx1/swampcrab_hero.dbr",
          "records/proxies/poolsherogdx3/thornedhorrorfrost_hero.dbr"]:
    dump(p)

print("\n=== C. the hero/boss records themselves ===")
for p in ["records/creatures/enemies/hero/basilisk_h02.dbr",
          "records/creatures/enemies/hero/basilisk_h03.dbr",
          "records/creatures/enemies/hero/swampcrab_h03.dbr",
          "records/creatures/enemies/hero/swampcrab_h04.dbr",
          "records/creatures/enemies/hero/aetherialcorruption_h02.dbr",
          "records/creatures/enemies/boss&quest/aetherialfleshshaper_haraxis.dbr",
          "records/creatures/enemies/swampcrab_a00_summon.dbr"]:
    dump(p, ["description","monsterClassification","charLevel","characterAttributeEquations",
             "levelVarianceEquation1","levelVarianceEquation"])
