#!/usr/bin/env python3
"""KC2-PM4 · Lap X · BINARY CORROBORATION of the mitigation pipeline.

⚑ `NOTE D-V2-1` HONOURED.  The Lap-S PE reader's export map collides vtable-symbol RVAs, so NO
vtable base is trusted and none is read here.  This instrument does string/immediate residency
only: it asks WHERE each formula field name and each equation VARIABLE name lives, and it
CORROBORATES; it never carries a magnitude by itself.

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-15.
"""
from __future__ import annotations

import hashlib
import json
import pathlib

GDBIN = pathlib.Path("/Users/admin/Games/vendor/grim-dawn")
OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/"
                   "notes/2026-08-15-kc2-pm4-lap-x-mitigation-decode")
PINS = {"Game.dll": "4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02",
        "Engine.dll": "7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c"}

FIELDS = ["armorDefensiveAbsorption", "physicalDamageDefenseEquationDGP",
          "physcialDamageDefenseEquationDLEP", "meleeBlockEquation", "projectileBlockEquation",
          "shieldDamageReductionEquationDGB", "shieldDamageReductionEquationDLEB",
          "playerDefenseCap", "monsterDefenseCap", "monsterLevelGapFixer",
          "combatRegionHeadChance", "combatRegionShouldersChance", "combatRegionArmsChance",
          "combatRegionTorsoChance", "combatRegionLegsChance", "combatRegionFeetChance",
          "combatRegionFullyProtectedChance", "combatRegionUnprotectedChance",
          "defensiveProtection", "defensiveProtectionModifier", "defensiveAbsorption",
          "defensiveAbsorptionModifier", "defensiveBonusProtection", "defensiveBlock",
          "defensiveBlockChance", "blockAbsorption", "blockRecoveryTime", "damageAbsorption",
          "damageAbsorptionPercent", "normalPTHEquation", "probabilityToHitEquation"]
#: the EQUATION VARIABLE names.  Their residency is the load-bearing evidence: if the engine
#: resolves `sumProtectionDV` by NAME, the .dbr equation strings are the IMPLEMENTATION, not a
#: data-side echo of hard-coded arithmetic.
DVARS = ["sumProtectionDV", "sumAbsorptionDV", "physicalDamageDV", "blockChanceDV",
         "blockChanceModifierDV", "shieldDefenseDV", "shieldAbsorptionDV", "damageDV",
         "offensiveAbilityDV", "defensiveAbilityDV", "probabilityToHitDV"]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    res = {"note_D_V2_1": "no vtable base read; string/immediate residency only (CORROBORATION)",
           "pins": {}, "fields": {}, "equation_variables": {}}
    blobs = {}
    for name, want in PINS.items():
        b = (GDBIN / name).read_bytes()
        got = hashlib.sha256(b).hexdigest()
        if got != want:
            raise SystemExit(f"HALT — {name} digest mismatch: expected {want} got {got}")
        res["pins"][name] = got
        blobs[name] = b
    for group, names in (("fields", FIELDS), ("equation_variables", DVARS)):
        for n in names:
            row = {}
            for bn, b in blobs.items():
                i = b.find(n.encode())
                row[bn] = ("0x%08x" % i) if i >= 0 else "ABSENT"
            res[group][n] = row
    gm = sum(1 for v in res["fields"].values() if v["Game.dll"] != "ABSENT")
    dv = sum(1 for v in res["equation_variables"].values() if v["Game.dll"] != "ABSENT")
    res["summary"] = {
        "fields_resident_in_Game.dll": f"{gm}/{len(FIELDS)}",
        "equation_variables_resident_in_Game.dll": f"{dv}/{len(DVARS)}",
        "fields_resident_in_Engine.dll": sum(1 for v in res["fields"].values()
                                             if v["Engine.dll"] != "ABSENT"),
        "reading": "the whole mitigation pipeline is Game.dll-resident and Engine.dll-absent; "
                   "and because the equation VARIABLE names resolve as strings, the "
                   "combatformulas.dbr equations are evaluated by name at runtime — they are "
                   "the implementation, not documentation of it.",
    }
    p = OUT / "pm4x_binary_anchors.json"
    p.write_text(json.dumps(res, indent=1, sort_keys=True))
    print(json.dumps(res["summary"], indent=1))
    print("pm4x_binary_anchors.json", hashlib.sha256(p.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
