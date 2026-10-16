#!/usr/bin/env python3
"""KP-500: re-derive 'no D2 player confusion / convert state' from captures.

Read-only. Run with:  python3 -I verify_kp500.py
Writes kp500_facts.json; exits non-zero on a missing anchor or a table
check that fails.
"""
import csv
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, "captures")
RAW = os.path.normpath(os.path.join(HERE, "..", "..", "..", "research",
                                    "datamine-acquisition", "d2", "raw"))
failures = []


def find(fname, needle, after=0):
    with open(os.path.join(CAP, fname), encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            if i > after and needle in line:
                return i
    failures.append(f"anchor missing: {fname}: {needle!r}")
    return None


NEC = "d2moo-D2Game-SKILLS-SkillNec.cpp"
A = {
    # states that exist
    "STATE_CONVERSION": ("d2moo-D2Common-D2States.h", "STATE_CONVERSION,", 0),
    "STATE_ATTRACT": ("d2moo-D2Common-D2States.h", "STATE_ATTRACT,", 0),
    "STATE_CONFUSE": ("d2moo-D2Common-D2States.h", "STATE_CONFUSE,", 0),
    # Confuse: per-target callback rejects non-monsters
    "Confuse_dofunc": (NEC, "int32_t __fastcall SKILLS_SrvDo061_Confuse(", 0),
    "Confuse_target_cb": (NEC, "int32_t __fastcall sub_6FD0C060(D2UnitStrc* pUnit, void* pArg)", 0),
    "Confuse_monster_only": (NEC, "if (!pUnit || pUnit->dwUnitType != UNIT_MONSTER || STATLIST_GetUnitAlignment(pUnit) != UNIT_ALIGNMENT_EVIL || !sub_6FCBD900(pParam->pGame, pParam->pUnit, pUnit) || SUNIT_IsDead(pUnit) || !sub_6FD15190(pUnit, AISPECIALSTATE_TERROR))", 0),
    # Attract: target and radius both gated by the AI-switch check
    "Attract_dofunc": (NEC, "int32_t __fastcall SKILLS_SrvDo059_Attract(", 0),
    "Attract_target_gate": (NEC, "|| !sub_6FD15190(pTargetUnit, AISPECIALSTATE_INVALID)", 0),
    "Attract_radius_cb": (NEC, "int32_t __fastcall sub_6FD0BDA0(D2UnitStrc* pUnit, void* pArg)", 0),
    "Attract_radius_gate": (NEC, "&& sub_6FD15190(pUnit, AISPECIALSTATE_INVALID)", 0),
    # AI-curse callback (Dim Vision / Terror) also monster-only
    "AiCurse_cb": (NEC, "int32_t __fastcall sub_6FD0B450(D2UnitStrc* pUnit, void* pArgs)", 0),
    "AiCurse_monster_only": (NEC, "if (!pUnit || pUnit->dwUnitType != UNIT_MONSTER || STATLIST_GetUnitAlignment(pUnit) == UNIT_ALIGNMENT_NEUTRAL)", 0),
    # the shared gate
    "SwitchAi_wrapper": ("d2moo-D2Game-SKILLS-Skills.cpp", "int32_t __fastcall sub_6FD15190(D2UnitStrc* pUnit, D2C_AiSpecialState nAiSpecialState)", 0),
    "CanUnitSwitchAi": ("d2moo-D2Game-AI-AiUtil.cpp", "BOOL __fastcall AIUTIL_CanUnitSwitchAi(D2UnitStrc* pUnit, D2C_AiSpecialState nAiSpecialState)", 0),
    "CanUnitSwitchAi_monster_only": ("d2moo-D2Game-AI-AiUtil.cpp", "if (!pUnit || pUnit->dwUnitType != UNIT_MONSTER ", 1323),
    # Conversion (Paladin)
    "Conversion_dofunc": ("d2moo-D2Game-SKILLS-SkillPal.cpp", "int32_t __fastcall SKILLS_SrvDo079_Conversion(", 0),
    "Conversion_monster_only": ("d2moo-D2Game-SKILLS-SkillPal.cpp", "pTarget->dwUnitType == UNIT_MONSTER && STATLIST_GetUnitAlignment(pTarget) == UNIT_ALIGNMENT_EVIL && sub_6FD15190(pTarget, AISPECIALSTATE_TERROR)", 0),
    # Mind Blast conversion (Assassin)
    "MindBlast_cb": ("d2moo-D2Game-SKILLS-SkillAss.cpp", "int32_t __fastcall SKILLS_AuraCallback_MindBlast(", 0),
    "MindBlast_monster_only": ("d2moo-D2Game-SKILLS-SkillAss.cpp", "if (pUnit && pUnit->dwUnitType == UNIT_MONSTER && !MONSTERS_GetHirelingTypeId(pUnit)", 0),
    "MindBlast_sets_conversion": ("d2moo-D2Game-SKILLS-SkillAss.cpp", "STATLIST_SetState(pConversionStatList, STATE_CONVERSION);", 0),
    # AI special-state table (no confuse/convert player path)
    "AiStates_enum": ("d2moo-D2Game-AI-AiStates.h", "enum D2C_AiSpecialState : uint32_t", 0),
    # player-side control analogues that DO exist
    "Stun_nonmonster": ("d2moo-D2Game-UNIT-SUnitDmg.cpp", "if (!pDefender || pDefender->dwUnitType != UNIT_MONSTER)", 1325),
    "Stun_cap_250": ("d2moo-D2Game-UNIT-SUnitDmg.cpp", "nStunLength = std::min(nStunLength, 250);", 1325),
    "Stun_state_set": ("d2moo-D2Game-UNIT-SUnitDmg.cpp", "STATLIST_SetState(pNewStatList, STATE_STUNNED);", 1325),
    "Stunned_player_forced_gethit": ("d2moo-D2Game-UNIT-SUnitDmg.cpp", "if (STATLIST_GetStatListFromUnitAndState(pUnit, STATE_STUNNED) || !sub_6FCC1870(pUnit, pDamage, pDamage->dwHitClass))", 1934),
    "Freeze_fn": ("d2moo-D2Game-UNIT-SUnitDmg.cpp", "void __fastcall SUNITDMG_ApplyFreezeState(D2UnitStrc* pAttacker, D2UnitStrc* pDefender, int32_t nFreezeLength)", 0),
    "Freeze_player_becomes_cold": ("d2moo-D2Game-UNIT-SUnitDmg.cpp", "if (nDefenderType == UNIT_PLAYER)", 1645),
}
anchors = {k: {"file": f, "needle": n, "line": find(f, n, a)} for k, (f, n, a) in A.items()}

# --- Table checks ------------------------------------------------------------
CONTROL_STATES = {"confuse", "attract", "conversion", "terror", "dimvision", "taunt"}
CONTROL_DOFUNCS = {"51", "59", "61", "79"}

with open(os.path.join(RAW, "Skills.txt"), encoding="latin-1") as f:
    rows = list(csv.reader(f, delimiter="\t"))
h = rows[0]
ix = {c: i for i, c in enumerate(h)}
lod_control = []
for r in rows[1:]:
    if not r:
        continue
    if r[ix["auratargetstate"]] in CONTROL_STATES or r[ix["srvdofunc"]] in CONTROL_DOFUNCS:
        lod_control.append({"skill": r[0], "Id": r[ix["Id"]], "charclass": r[ix["charclass"]],
                            "auratargetstate": r[ix["auratargetstate"]], "srvdofunc": r[ix["srvdofunc"]]})
lod_names = {x["skill"] for x in lod_control}
if any(not x["charclass"] for x in lod_control):
    failures.append("a monster-only (no charclass) skill carries a control state")

with open(os.path.join(RAW, "MonStats.txt"), encoding="latin-1") as f:
    mrows = list(csv.reader(f, delimiter="\t"))
mh = mrows[0]
skcols = [i for i, c in enumerate(mh) if c.startswith("Skill") and c[5:].isdigit()]
lod_mon_hits = [(r[0], mh[i], r[i]) for r in mrows[1:] for i in skcols if i < len(r) and r[i] in lod_names]
if len(skcols) != 8:
    failures.append(f"MonStats.txt skill columns: {len(skcols)} (expected 8)")
if lod_mon_hits:
    failures.append(f"LoD monsters carry control skills: {lod_mon_hits[:5]}")

d2r_sk = json.load(open(os.path.join(CAP, "d2data", "skills.json")))
d2r_sk = list(d2r_sk.values()) if isinstance(d2r_sk, dict) else d2r_sk
d2r_control = [{"skill": r.get("skill"), "charclass": r.get("charclass"),
                "auratargetstate": r.get("auratargetstate"), "srvdofunc": r.get("srvdofunc")}
               for r in d2r_sk
               if r.get("auratargetstate") in CONTROL_STATES or str(r.get("srvdofunc")) in CONTROL_DOFUNCS]
d2r_names = {x["skill"] for x in d2r_control}
if any(not x["charclass"] for x in d2r_control):
    failures.append("D2R: a monster-only skill carries a control state")
d2r_ms = json.load(open(os.path.join(CAP, "d2data", "monstats.json")))
d2r_ms = list(d2r_ms.values()) if isinstance(d2r_ms, dict) else d2r_ms
d2r_mon_hits = [(m.get("Id"), k, v) for m in d2r_ms for k, v in m.items()
                if k.startswith("Skill") and k[5:].isdigit() and v in d2r_names]
if d2r_mon_hits:
    failures.append(f"D2R monsters carry control skills: {d2r_mon_hits[:5]}")


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


facts = {
    "d2moo_anchors": anchors,
    "lod113_control_skills": lod_control,
    "lod113_monstats_rows": len(mrows) - 1,
    "lod113_monsters_with_control_skills": lod_mon_hits,
    "d2r_control_skills": d2r_control,
    "d2r_monstats_rows": len(d2r_ms),
    "d2r_monsters_with_control_skills": d2r_mon_hits,
    "inputs": {"Skills.txt": sha(os.path.join(RAW, "Skills.txt")),
               "MonStats.txt": sha(os.path.join(RAW, "MonStats.txt"))},
    "captures_sha256": {os.path.relpath(os.path.join(r, f), CAP): sha(os.path.join(r, f))
                        for r, _, fs in os.walk(CAP) for f in sorted(fs)},
    "failures": failures,
}
out = os.path.join(HERE, "kp500_facts.json")
with open(out, "w") as f:
    json.dump(facts, f, indent=1, sort_keys=True)
    f.write("\n")
print(f"wrote {out}; failures={len(failures)}")
for x in failures:
    print("  FAIL", x)
sys.exit(1 if failures else 0)
