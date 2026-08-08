#!/usr/bin/env python3
"""Query the .tpl index for the HALT fields. Prints Crate's own annotations verbatim. READ-ONLY."""
import json, pathlib, sys

HERE = pathlib.Path(__file__).parent
IDX = json.load(open(HERE / "t4_tpl_index.json"))

WANT = sys.argv[1:] if len(sys.argv) > 1 else [
    # HALT-2
    "delayMovement", "characterRunSpeed", "characterRunSpeedModifier",
    "playerRunSpeedCapMax", "playerRunSpeedCapMin", "absoluteRunSpeedCapMax",
    # HALT-8
    "projectilePeriod", "projectileExplosionRadius",
    # HALT-1
    "skillActiveDuration", "skillLifeBonus", "defensiveBlockAmountModifier",
    # HALT-6 / HALT-3
    "armorDefensiveAbsorption", "playerDefenseCap", "damageMagnitude", "absMaxDamageScaling",
    "monsterDefenseCap", "playerReflectCap",
    # HALT-9 semantics
    "offensiveTotalDamageModifier", "offensivePhysicalModifier", "offensiveSlowPhysicalModifier",
    "defensivePercentCurrentLife", "defensiveConvert", "retaliationTotalDamageModifier",
    "offensiveCritDamageModifier", "skillCooldownReduction",
    "spawnChampionMinAdj", "spawnChampionMaxAdj",
]

for f in WANT:
    hits = IDX.get(f, [])
    print(f"\n### {f}   ({len(hits)} block(s))")
    if not hits:
        print("    NAMED-ABSENT from templates.arc")
        continue
    seen = set()
    for h in hits:
        sig = (h.get("tpl"), h.get("description", ""), h.get("type", ""), h.get("class", ""),
               h.get("defaultValue", ""), h.get("value", ""))
        if sig in seen:
            continue
        seen.add(sig)
        print(f"    tpl={h.get('tpl')}")
        print(f"      class        = {h.get('class','')!r}")
        print(f"      type         = {h.get('type','')!r}")
        print(f"      description  = {h.get('description','')!r}")
        print(f"      defaultValue = {h.get('defaultValue','')!r}")
        if h.get("value"):
            print(f"      value        = {h.get('value')!r}")
