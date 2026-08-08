#!/usr/bin/env python3
"""HALT-1/2/8/9-semantics: crack templates.arc fully, index every Variable block by DBR field name.
templates.arc lives ONLY in the Edition-I full-install tree; the Edition-II pin ships no .arc for
database/. Provenance is disclosed in the note. READ-ONLY."""
import sys, pathlib, re, json
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive

HERE = pathlib.Path(__file__).parent
OUT = HERE / "tpl"
OUT.mkdir(exist_ok=True)
P = pathlib.Path("/Users/admin/Games/vendor/grim-dawn/database/templates.arc")
a = ArcArchive(P)
names = a.names()
print(f"templates.arc: {len(names)} files  version={a.version}  src={P}")

BLOCK = re.compile(r"Variable\s*\{(.*?)\}", re.S)
KV = re.compile(r'(\w+)\s*=\s*"(.*?)"', re.S)

index = {}          # varName -> list of dicts
raw = {}
for n in names:
    try:
        payload = a.read_file(n).decode("utf-8", "replace")
    except Exception as e:
        print(f"!! {n}: {e}")
        continue
    raw[n] = payload
    (OUT / pathlib.Path(n).name).write_text(payload, errors="replace")
    for m in BLOCK.finditer(payload):
        d = dict(KV.findall(m.group(1)))
        key = d.get("name", "")
        index.setdefault(key, []).append({"tpl": pathlib.Path(n).name, **d})

print(f"extracted {len(raw)} .tpl  ->  {OUT}")
print(f"distinct Variable names: {len(index)}")
json.dump(index, open(HERE / "t4_tpl_index.json", "w"), indent=0)

# FoA-freshness probe: does this PRE-FoA templates.arc know the 1.3.0.0 fields?
print("\n== FoA-FRESHNESS PROBE on the pre-FoA templates.arc ==")
for f in ["defensiveCrowdControl", "defensiveCrowdControlMaxResist", "conversionInType",
          "conversionPercentage", "characterManaLimitReserve", "characterManaLimitReserveModifier",
          "projectilePeriod", "delayMovement", "skillActiveDuration", "offensiveSlowPhysicalModifier",
          "defensivePercentCurrentLife", "defensiveConvert", "retaliationTotalDamageModifier",
          "offensiveTotalDamageModifier", "offensivePhysicalModifier", "armorDefensiveAbsorption",
          "playerRunSpeedCapMax", "characterRunSpeed", "characterRunSpeedModifier"]:
    hits = index.get(f, [])
    print(f"  {f:38s} {'PRESENT' if hits else 'ABSENT ':8s} ({len(hits)} tpl block(s)): "
          + ", ".join(sorted({h['tpl'] for h in hits})[:6]))
