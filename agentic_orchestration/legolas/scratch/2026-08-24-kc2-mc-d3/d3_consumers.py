#!/usr/bin/env python3
"""D-3 STEP 7 — THE CONSUMERS.  For each decoded controller slot, enumerate every site in
Game.dll `.text` that touches that displacement, resolved to the enclosing exported symbol.
Load itself is excluded (it is the writer).  What remains is the SEMANTICS: the named code that
acts on the parameter.  READ-ONLY."""
from __future__ import annotations
import collections, json, pathlib, struct, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import d3_lib as L, d3_binary as B
OUT = pathlib.Path(__file__).resolve().parent

# slot map: decoded in steps 4b + 5 (+ the hand-read leader/swing regions)
SLOTS = {
    # ── Fleeing
    "FleeBehavior": 0x304, "FleeTarget": 0x308, "maxFleeCount": 0x30c, "FleeTime": 0x310,
    "FleeDelay": 0x314, "fleeDistance": 0x318, "ClearAngerWhenFleeing": 0x31c,
    "FleeChance": 0x2d8, "ResetOriginAfterFleeing": 0x3a4,
    # ── Attacking
    "minSwingPause": 0x2f0, "maxSwingPause": 0x2f4, "swingPauseRoll": 0x2f8,
    "RepositionChance": 0x3b0, "randomRepositionChance": 0x2e0,
    # ── Dodging
    "DodgeChance": 0x2dc, "DodgeDistance": 0x3a8, "MinDodgeDistance": 0x3ac, "DodgeDelay": 0x510,
    # ── SkillUsage
    "BuffSelfBehavior": 0x324, "BuffAllyBehavior": 0x328, "BuffAllyTargeting": 0x32c,
    "DebuffEnemyBehavior": 0x330, "healLeaderHealthPercentage": 0x358,
    "healAllyHealthPercentage": 0x35c,
    # ── Roaming / Patrolling
    "RoamBehavior": 0x320, "RoamDistance": 0x374, "MinRoamDistance": 0x39c,
    "MinTimeBeforeRoam": 0x394, "MaxTimeBeforeRoam": 0x398,
    "WanderDistance": 0x370, "MinWanderDistance": 0x3a0, "TeleportToLeaderDistance": 0x378,
    "ChanceToIdleOnPatrol": 0x37c, "MinPatrolIdleTime": 0x380, "MaxPatrolIdleTime": 0x384,
    # ── Emote
    "randomEmoteChance": 0x514, "randomEmoteMinTime": 0x518, "randomEmoteMaxTime": 0x51c,
    # ── PetBehaviour
    "ignorePetsChance": 0x56c, "ignorePetsInterval": 0x570, "petTargetLevelRange": 0x580,
    "petTargetLeastAttacked": 0x584, "petTargetGreatestHealth": 0x585,
    # ── Sleep
    "ignoreSleepingEnemies": 0x4d9,
    # ── hidden Leader group
    "LeaderBehavior": 0x360, "LeaderDistance": 0x364, "MaxFollowers": 0x368,
    # ── already-decoded context
    "ViewDistance": 0x21c, "PursuitTime": 0x2fc, "MaxPursuitDistance": 0x300,
    "ChanceToRespondToDistressCall": 0x338, "DistressResponseGroup": 0x33c,
    "DistressResponseBehavior": 0x354,
    "RandomAngerChance": 0x390, "RandomAngerEvaluationTime": 0x504,
}


def main():
    pe = L.PE.PE32(L.PE.GD / "Game.dll")
    ordered = B.ordered_exports(pe)
    load_rva = pe.exports()["?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z"]

    res = {}
    for f, disp in sorted(SLOTS.items(), key=lambda x: x[1]):
        syms = collections.Counter()
        for rva in B.disp_sites(pe, disp):
            s = B.enclosing(ordered, rva)
            if s is None:
                continue
            if s[0] == load_rva:
                continue
            syms[s[1]] += 1
        res[f] = dict(slot=hex(disp), consumers=dict(syms.most_common()))
        pretty = [k.split("@GAME")[0].lstrip("?") for k in syms]
        print(f"{f:30s} +{disp:#06x}  {pretty[:8]}")
    json.dump(res, open(OUT / "d3_consumers.json", "w"), indent=2)


if __name__ == "__main__":
    main()
