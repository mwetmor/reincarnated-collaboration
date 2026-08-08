#!/usr/bin/env python3
"""proxyPoolEquation + template annotations for charLevel / ignoreGameBalance / characterLife*.
templates.arc lives ONLY in the Edition-I tree -> TPL-CITED (Edition-I, freshness-probed). READ-ONLY."""
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from t0_lib import merged, index

print("=" * 100)
print("A — proxyPoolEquation records (present on p04 pools, absent on p01/p02/p03)")
print("=" * 100)
for p in sorted(x for x in index() if "proxypoolequation" in x):
    rec, prov, own = merged(p)
    print(f"\n-- {p}  owners={own}")
    for f in sorted(rec):
        print(f"     {f:38s} = {str(rec[f])[:80]}   [{prov[f]}]")

print("\n" + "=" * 100)
print("B — does each wave-160 pool carry proxyPoolEquation?")
print("=" * 100)
for tag, p in (("p01", "records/proxies/poolsboss/nemesis_all.dbr"),
               ("p02", "records/proxies/poolsbossgdx1/nemesis_all_noaetherialvanguard.dbr"),
               ("p03", "records/proxies/poolsbossgdx1/nemesis_wendigooraetherialvanguard.dbr"),
               ("p04a", "records/proxies/poolsbossgdx1/aetherialcolossus_galakros.dbr"),
               ("p04b", "records/proxies/poolsbossgdx2/korvaaktombguardian.dbr"),
               ("p06", "records/proxies/poolsherogdx1/wendigocannibal_hero.dbr")):
    rec, _, _ = merged(p)
    print(f"   {tag:5s} proxyPoolEquation = {rec.get('proxyPoolEquation')!r}   "
          f"ignoreGameBalance = {rec.get('ignoreGameBalance')!r}")

print("\n" + "=" * 100)
print("C — TEMPLATE annotations (Edition-I templates.arc, freshness-probed)")
print("=" * 100)
from gd_arc_reader_2026_07_26 import ArcArchive          # noqa
ARC = pathlib.Path("/Users/admin/Games/vendor/grim-dawn/database/templates.arc")
arc = ArcArchive(ARC)
names = list(arc.entries)
print(f"   templates.arc: {len(names)} entries")

WANT = ("charLevel", "ignoreGameBalance", "characterLifeModifier", "characterLifeMultModifier",
        "characterLife", "monsterClassification", "proxyPoolEquation",
        "minVarianceEquationNormal", "maxVarianceEquationNormal", "spawnMinModifier")


def dump(entry):
    raw = arc.read(entry)
    try:
        txt = raw.decode("utf-8", "replace")
    except Exception:
        return None
    return txt


# freshness probe first
probe = ["defensiveCrowdControl", "conversionPercentage", "retaliationTotalDamageModifier",
         "offensiveTotalDamageModifier", "armorDefensiveAbsorption"]
found = {p: 0 for p in probe}
blobs = {}
for n in names:
    t = dump(n)
    if not t:
        continue
    blobs[n] = t
    for p in probe:
        if p in t:
            found[p] += 1
print(f"   FRESHNESS PROBE (1.3.0.0-era field names present?): "
      + ", ".join(f"{k}:{v}" for k, v in found.items()))

for w in WANT:
    hits = [n for n, t in blobs.items() if f'"{w}"' in t or f"variable\n{{" in t and w in t]
    hits = [n for n in hits if w in blobs[n]]
    print(f"\n   -- {w}: appears in {len(hits)} templates; showing first 2 variable blocks")
    shown = 0
    for n in hits:
        t = blobs[n]
        for m in re.finditer(r"Variable\s*\{[^{}]*\}", t, re.S | re.I):
            blk = m.group(0)
            if re.search(r'name\s*=\s*"%s"' % re.escape(w), blk):
                one = " | ".join(x.strip() for x in blk.splitlines()
                                 if x.strip() and x.strip() not in ("Variable", "{", "}"))
                print(f"      [{n.split('/')[-1]}] {one[:420]}")
                shown += 1
                break
        if shown >= 2:
            break
