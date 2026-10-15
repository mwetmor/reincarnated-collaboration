#!/usr/bin/env python3
"""KP-481 follow-up: re-derive mana-debit timing facts for Meteor, Fire Ball,
Fire Bolt and Static Field from the pinned captures.

Read-only. Run with:  python3 -I verify_mana_debit.py
Writes mana_debit_facts.json next to this script; exits non-zero on any
missing anchor or unexpected table value.
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

# Columns that can bear on WHEN (or WHETHER) mana is debited, per the D2MOO
# handler/start/consume code (see README-KP481-mana-debit.md section C).
TIMING_COLS = ["srvstfunc", "srvdofunc", "srvmissile", "usemanaondo",
               "startmana", "AttackNoMana", "LineOfSight", "interrupt",
               "minmana", "manashift", "mana", "lvlmana", "decquant",
               "periodic", "InTown"]
EXPECT_LOD = {
    "Fire Bolt":    {"Id": "36", "srvstfunc": "", "srvdofunc": "", "srvmissile": "firebolt",
                     "usemanaondo": "", "startmana": "", "AttackNoMana": "", "LineOfSight": "",
                     "interrupt": "1"},
    "Fire Ball":    {"Id": "47", "srvstfunc": "", "srvdofunc": "", "srvmissile": "fireball",
                     "usemanaondo": "", "startmana": "", "AttackNoMana": "", "LineOfSight": "",
                     "interrupt": "1"},
    "Static Field": {"Id": "42", "srvstfunc": "", "srvdofunc": "20", "srvmissile": "",
                     "usemanaondo": "", "startmana": "", "AttackNoMana": "", "LineOfSight": "4",
                     "interrupt": "1"},
    "Meteor":       {"Id": "56", "srvstfunc": "", "srvdofunc": "28", "srvmissile": "",
                     "usemanaondo": "", "startmana": "", "AttackNoMana": "", "LineOfSight": "4",
                     "interrupt": "1"},
}
EXPECT_D2R = {  # blizzhackers/d2data json: absent columns come back as None
    "Fire Bolt":    {"srvstfunc": None, "srvdofunc": None, "srvmissile": "firebolt",
                     "usemanaondo": None, "startmana": None, "LineOfSight": None},
    "Fire Ball":    {"srvstfunc": None, "srvdofunc": None, "srvmissile": "fireball",
                     "usemanaondo": None, "startmana": None, "LineOfSight": None},
    "Static Field": {"srvstfunc": None, "srvdofunc": 20, "srvmissile": None,
                     "usemanaondo": None, "startmana": None, "LineOfSight": 4},
    "Meteor":       {"srvstfunc": None, "srvdofunc": 28, "srvmissile": None,
                     "usemanaondo": None, "startmana": None, "LineOfSight": 4},
}


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def anchor(fname, needle):
    with open(os.path.join(CAP, fname), encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            if needle in line:
                return i
    failures.append(f"anchor missing: {fname}: {needle!r}")
    return None


facts = {"lod113": {}, "d2r": {}}

with open(os.path.join(RAW, "Skills.txt"), encoding="latin-1") as f:
    rows = list(csv.reader(f, delimiter="\t"))
head = rows[0]
by_name = {r[0]: dict(zip(head, r)) for r in rows[1:] if r}
for name, exp in EXPECT_LOD.items():
    row = by_name[name]
    facts["lod113"][name] = {c: row.get(c, "<nocol>") for c in ["Id"] + TIMING_COLS}
    for c, want in exp.items():
        if row.get(c) != want:
            failures.append(f"LoD {name}.{c}: got {row.get(c)!r} want {want!r}")

with open(os.path.join(CAP, "d2data", "skills.json")) as f:
    d2r = json.load(f)
d2r_rows = list(d2r.values()) if isinstance(d2r, dict) else d2r
for name, exp in EXPECT_D2R.items():
    row = [r for r in d2r_rows if r.get("skill") == name][0]
    facts["d2r"][name] = {c: row.get(c) for c in TIMING_COLS}
    for c, want in exp.items():
        if row.get(c) != want:
            failures.append(f"D2R {name}.{c}: got {row.get(c)!r} want {want!r}")

S = "d2moo-D2Game-Skills.cpp"
A = {
    # start path (mode start, a5 = 0)
    "Start_def": (S, "int32_t __fastcall sub_6FD12950("),
    "Start_mana_sufficiency_check": (S, "if (!pSkillsTxtRecord || !a5 && !sub_6FD10CE0(pUnit))"),
    "Start_LOS_gate": (S, "if (pSkillsTxtRecord->nLineOfSight != SKILLSLOS_NONE)"),
    "Start_LOS_mask_flying": (S, "nCollisionMask = COLLIDE_DOOR | COLLIDE_MISSILE_BARRIER;"),
    "Start_LOS_fail_return": (S, "if (!D2Common_11026(nX, nY, pUnit, nCollisionMask))"),
    "Start_stfunc_lookup": (S, "SkillStartFunc pfSkillStart = gpSkillSrvStartFnTable_6FD408B0[pSkillsTxtRecord->wSrvStartFunc];"),
    "Start_debit_if_stfunc": (S, "const int32_t nResult = pfSkillStart(pGame, pUnit, nSkillId, nSkillLevel);"),
    "Start_fail_forces_neutral": (S, "sub_6FC817D0(pGame, pUnit, 0, 5, 0, 0, 1);"),
    "StartTable_index0_null": (S, "constexpr SkillStartFunc gpSkillSrvStartFnTable_6FD408B0[] ="),
    "DoTable_def": (S, "static const SkillDoFunc gpSkillSrvDoFnTable_6FD40A20[] ="),
    # action-frame handler (a5 = 1)
    "Handler_def": (S, "int32_t __fastcall D2GAME_SKILLS_Handler_6FD12BA0("),
    "Handler_usemanaondo_check": (S, "if (nDoFunc < 0 || nDoFunc >= std::size(gpSkillSrvDoFnTable_6FD40A20) || bLivingUnit && pSkillsTxtRecord->dwFlags[1] & gdwBitMasks[SKILLSFLAGINDEX2_USEMANAONDO] && !sub_6FD10CE0(pUnit))"),
    "Handler_dofunc_call": (S, "nResult = pDoFunc(pGame, pUnit, nSkillId, nSkillLevel);"),
    "Handler_srvmissile_branch": (S, "const int32_t nSrvMissile = pSkillsTxtRecord->wSrvMissile;"),
    "Handler_srvmissile_create": (S, "sub_6FD11420(pGame, pSkillsTxtRecord->wSrvMissile, pUnit, nSkillId, nSkillLevel, nX, nY, nTargetX, nTargetY, 0);"),
    "Handler_srvmissile_nResult1": (S, "        nResult = 1;\n"),
    "Handler_nResult_gate": (S, "    if (!nResult)"),
    "Handler_a5_gate": (S, "    if (a5)"),
    "Handler_debit_at_do": (S, "if (!gpSkillSrvStartFnTable_6FD408B0[pSkillsTxtRecord->wSrvStartFunc] || pSkillsTxtRecord->dwFlags[1] & gdwBitMasks[SKILLSFLAGINDEX2_USEMANAONDO])"),
    "DoFrame_wrapper": (S, "void __fastcall sub_6FD13410("),
    # missile creator used by the srvmissile path
    "MissileCreator_def": (S, "D2UnitStrc* __fastcall sub_6FD11420("),
    "MissileCreator_zero_target_fail": (S, "if (!missileParams.nTargetX || !missileParams.nTargetY)"),
    # mana consume
    "Consume_def": (S, "int32_t __fastcall D2GAME_SKILLMANA_Consume_6FD10A50("),
    "Consume_level_gt1": (S, "if (nSkillLevel > 1)"),
    "Consume_insufficient_noop": (S, "if (STATLIST_UnitGetStatValue(pPlayer, STAT_MANA, 0) < nManaCost)"),
    "Consume_debit": (S, "STATLIST_AddUnitStat(pPlayer, STAT_MANA, -nManaCost, 0);"),
    "ManaCheck_def": (S, "int32_t __fastcall sub_6FD10CE0("),
    # Static Field do-func
    "StaticField_def": ("d2moo-SkillSor.cpp", "int32_t __fastcall SKILLS_SrvDo020_StaticField("),
    "StaticField_aura_walk": ("d2moo-SkillSor.cpp", "sub_6FD0FE80(pGame, pUnit, 0, 0, nAuraRange, pSkillsTxtRecord->dwAuraFilter, SKILLS_AuraCallback_StaticField, &staticField, 0, __FILE__, __LINE__);"),
    # Meteor do-func (for comparison)
    "Meteor_def": ("d2moo-SkillSor.cpp", "int32_t __fastcall SKILLS_SrvDo028_Meteor_Blizzard_Eruption_BaalTaunt_Catapult("),
    # player-mode plumbing
    "StartXY_Cast": ("d2moo-PlrModes.cpp", "void __fastcall PLRMODE_StartXY_AttackCastThrowKickSpecialSequence("),
    "StartXY_Neutral": ("d2moo-PlrModes.cpp", "void __fastcall PLRMODE_StartXY_Neutral("),
    "StartXY_GetHit": ("d2moo-PlrModes.cpp", "void __fastcall PLRMODE_StartXY_GetHit("),
    "StartXY_Block": ("d2moo-PlrModes.cpp", "void __fastcall PLRMODE_StartXY_Block("),
    "Interrupt_flag_gate": ("d2moo-PlrModes.cpp", "if (!(pUsedSkillsTxtRecord->dwFlags[0] & gdwBitMasks[SKILLSFLAGINDEX_INTERRUPT]))"),
    "DeletePerFrameEvents": ("d2moo-D2Game-UNIT-SUnit.cpp", "void __fastcall D2GAME_DeletePlayerPerFrameEvents_6FCBCE50("),
    # common / tables
    "LOS_raytrace": ("d2moo-D2Common-D2Skills.cpp", "BOOL __stdcall D2Common_11026(int nX, int nY, D2UnitStrc* pUnit, uint16_t nColMask)"),
    "GetSkillLevel_bonus": ("d2moo-D2Common-D2Skills.cpp", "if (bBonus && pSkill->nOwnerGUID == D2UnitInvalidGUID)"),
    "StartStat_startmana": ("d2moo-D2Common-D2Skills.cpp", "BOOL __fastcall D2Common_SKILLMANA_CheckStartStat_6FDB1400("),
    "LOS_enum_flying4": ("d2moo-D2Common-DataTbls-SkillsTbls.h", "SKILLSLOS_PLAYER_FLYING = 4,"),
    "Collide_door": ("d2moo-D2Common-D2Collision.h", "COLLIDE_DOOR = 0x0800,"),
    "Collide_missile_barrier": ("d2moo-D2Common-D2Collision.h", "COLLIDE_MISSILE_BARRIER = 0x0004,"),
    "Txt_srvstfunc": ("d2moo-D2Common-DataTbls-SkillsTbls.cpp", "{ \"srvstfunc\", TXTFIELD_WORD, 0, 44, NULL },"),
    "Txt_srvdofunc": ("d2moo-D2Common-DataTbls-SkillsTbls.cpp", "{ \"srvdofunc\", TXTFIELD_WORD, 0, 46, NULL },"),
    "Txt_srvmissile": ("d2moo-D2Common-DataTbls-SkillsTbls.cpp", "{ \"srvmissile\", TXTFIELD_NAMETOWORD, 0, 70, &sgptDataTables->pMissilesLinker },"),
    "Txt_lineofsight": ("d2moo-D2Common-DataTbls-SkillsTbls.cpp", "{ \"lineofsight\", TXTFIELD_BYTE, 0, 399, NULL },"),
    "Txt_usemanaondo": ("d2moo-D2Common-DataTbls-SkillsTbls.cpp", "{ \"usemanaondo\", TXTFIELD_BIT, 37, 4, NULL },"),
    "Txt_startmana": ("d2moo-D2Common-DataTbls-SkillsTbls.cpp", "{ \"startmana\", TXTFIELD_WORD, 0, 388, NULL },"),
    "Txt_AttackNoMana": ("d2moo-D2Common-DataTbls-SkillsTbls.cpp", "{ \"AttackNoMana\", TXTFIELD_BIT, 28, 4, NULL },"),
    "Missile_create_from_params": ("d2moo-D2Game-MISSILES-Missiles.cpp", "D2UnitStrc* __fastcall MISSILES_CreateMissileFromParams("),
}


def anchor_multi(fname, needle):
    if "\n" not in needle:
        return anchor(fname, needle)
    # needle with trailing newline: match whole line
    want = needle.rstrip("\n")
    with open(os.path.join(CAP, fname), encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            if line.rstrip("\n") == want and i > 2500:  # the handler's srvmissile branch
                return i
    failures.append(f"anchor missing: {fname}: {needle!r}")
    return None


facts["d2moo_anchors"] = {k: {"file": f, "line": anchor_multi(f, n), "needle": n.rstrip("\n")}
                          for k, (f, n) in A.items()}

# Structural check: start-function table index 0 is nullptr (empty srvstfunc).
with open(os.path.join(CAP, S), encoding="utf-8") as f:
    lines = f.readlines()
i0 = facts["d2moo_anchors"]["StartTable_index0_null"]["line"]
if i0:
    first = [l.strip() for l in lines[i0:i0 + 3] if l.strip() not in ("{",)]
    facts["start_table_index0"] = first[0]
    if first[0] != "nullptr,":
        failures.append(f"start table index 0 is {first[0]!r}, not nullptr")
d0 = facts["d2moo_anchors"]["DoTable_def"]["line"]
if d0:
    first = [l.strip() for l in lines[d0:d0 + 3] if l.strip() not in ("{",)]
    facts["do_table_index0"] = first[0]
    if first[0] != "nullptr,":
        failures.append(f"do table index 0 is {first[0]!r}, not nullptr")

# Order inside the handler: do-func < srvmissile create < nResult gate < a5 < debit
order_keys = ["Handler_def", "Handler_dofunc_call", "Handler_srvmissile_create",
              "Handler_srvmissile_nResult1", "Handler_nResult_gate", "Handler_a5_gate",
              "Handler_debit_at_do"]
ls = [facts["d2moo_anchors"][k]["line"] for k in order_keys]
facts["handler_order_lines"] = dict(zip(order_keys, ls))
if None in ls or ls != sorted(ls):
    failures.append(f"handler order not monotonic: {ls}")

facts["inputs"] = {"Skills.txt": sha(os.path.join(RAW, "Skills.txt"))}
facts["failures"] = failures
out = os.path.join(HERE, "mana_debit_facts.json")
with open(out, "w") as f:
    json.dump(facts, f, indent=1, sort_keys=True)
    f.write("\n")
print(f"wrote {out}; failures={len(failures)}")
for x in failures:
    print("  FAIL", x)
sys.exit(1 if failures else 0)
