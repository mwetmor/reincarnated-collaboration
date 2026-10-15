#!/usr/bin/env python3
"""Re-derive the Meteor cast-delay facts from the pinned captures.

Read-only. Run with:  python3 -I verify_meteor_delay.py
Writes meteor_delay_facts.json next to this script and exits non-zero if any
anchor is missing or any value differs from the expected one.
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


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def tsv_row(path, key):
    with open(path, encoding="latin-1") as f:
        rows = list(csv.reader(f, delimiter="\t"))
    head = rows[0]
    for r in rows[1:]:
        if r and r[0] == key:
            return dict(zip(head, r))
    raise KeyError(key)


def expect(label, got, want):
    ok = got == want
    if not ok:
        failures.append(f"{label}: got {got!r}, want {want!r}")
    return {"value": got, "expected": want, "ok": ok}


def anchor(fname, needle):
    """Return the 1-based line number of the first line containing needle."""
    path = os.path.join(CAP, fname)
    with open(path, encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            if needle in line:
                return i
    failures.append(f"anchor missing: {fname}: {needle!r}")
    return None


facts = {}

# --- LoD 1.13 Skills.txt / Missiles.txt (fabd/diablo2 @ 45112569) -----------
sk = tsv_row(os.path.join(RAW, "Skills.txt"), "Meteor")
facts["lod113_skills_meteor"] = {
    "Id": expect("Id", sk["Id"], "56"),
    "delay": expect("delay", sk["delay"], "30"),
    "srvstfunc": expect("srvstfunc", sk["srvstfunc"], ""),
    "srvdofunc": expect("srvdofunc", sk["srvdofunc"], "28"),
    "srvmissile": expect("srvmissile", sk["srvmissile"], ""),
    "srvmissilea": expect("srvmissilea", sk["srvmissilea"], "meteorcenter"),
    "usemanaondo": expect("usemanaondo", sk["usemanaondo"], ""),
    "interrupt": expect("interrupt", sk["interrupt"], "1"),
    "anim": expect("anim", sk["anim"], "SC"),
    "perdelay": expect("perdelay", sk["perdelay"], ""),
}
mc = tsv_row(os.path.join(RAW, "Missiles.txt"), "meteorcenter")
facts["lod113_missiles_meteorcenter"] = {
    "Range": expect("meteorcenter.Range", mc["Range"], "60"),
    "Size": expect("meteorcenter.Size", mc["Size"], "1"),
}

# --- D2R 3.x skills.json (blizzhackers/d2data, captured copy) ----------------
with open(os.path.join(CAP, "d2data", "skills.json")) as f:
    d2r = json.load(f)
rows = list(d2r.values()) if isinstance(d2r, dict) else d2r
m = [r for r in rows if r.get("skill") == "Meteor"][0]
facts["d2r_skills_meteor"] = {
    "localdelay": expect("d2r localdelay", m.get("localdelay"), 30),
    "globaldelay": expect("d2r globaldelay", m.get("globaldelay"), None),
    "delay_column_present": expect("d2r has no plain delay col",
                                   "delay" in m, False),
    "srvstfunc": expect("d2r srvstfunc", m.get("srvstfunc"), None),
    "srvdofunc": expect("d2r srvdofunc", m.get("srvdofunc"), 28),
    "usemanaondo": expect("d2r usemanaondo", m.get("usemanaondo"), None),
}

# --- D2MOO @ 5596f5cb anchors (file, needle) -> line ------------------------
A = {
    "SetDelay_def": ("d2moo-D2Game-Skills.cpp",
                     "void __fastcall D2GAME_SKILLS_SetDelay_6FD11C00("),
    "SetDelay_expire": ("d2moo-D2Game-Skills.cpp",
                        "const int32_t nExpireFrame = nDelay + pGame->dwGameFrame;"),
    "SetDelay_players_only": ("d2moo-D2Game-Skills.cpp",
                              "if (pUnit && !pUnit->dwUnitType && nDelay)"),
    "Handler_def": ("d2moo-D2Game-Skills.cpp",
                    "int32_t __fastcall D2GAME_SKILLS_Handler_6FD12BA0("),
    "Handler_nResult_gate": ("d2moo-D2Game-Skills.cpp", "    if (!nResult)"),
    "Handler_mana_at_do": ("d2moo-D2Game-Skills.cpp",
                           "if (!gpSkillSrvStartFnTable_6FD408B0[pSkillsTxtRecord->wSrvStartFunc] || pSkillsTxtRecord->dwFlags[1] & gdwBitMasks[SKILLSFLAGINDEX2_USEMANAONDO])"),
    "Handler_delay_eval": ("d2moo-D2Game-Skills.cpp",
                           "const int32_t nDelay = SKILLS_EvaluateSkillFormula(pUnit, pSkillsTxtRecord->dwDelay, nSkillId, nSkillLevel);"),
    "Start_def": ("d2moo-D2Game-Skills.cpp",
                  "int32_t __fastcall sub_6FD12950("),
    "Start_no_stfunc_return": ("d2moo-D2Game-Skills.cpp",
                               "SkillStartFunc pfSkillStart = gpSkillSrvStartFnTable_6FD408B0[pSkillsTxtRecord->wSrvStartFunc];"),
    "DoFrame_wrapper": ("d2moo-D2Game-Skills.cpp",
                        "void __fastcall sub_6FD13410("),
    "Meteor_do_func": ("d2moo-SkillSor.cpp",
                       "int32_t __fastcall SKILLS_SrvDo028_Meteor_Blizzard_Eruption_BaalTaunt_Catapult("),
    "Meteor_point_check": ("d2moo-D2Game-Skills.cpp",
                           "int32_t __fastcall sub_6FD15340("),
    "Meteor_collide_mask5": ("d2moo-D2Game-Skills.cpp",
                             "return !COLLISION_CheckMaskWithSizeXY(pRoom, nX, nY, pMissilesTxtRecord->nSize, pMissilesTxtRecord->nSize, 5u);"),
    "CreateMissile_def": ("d2moo-D2Game-Skills.cpp",
                          "D2UnitStrc* __fastcall D2GAME_CreateMissile_6FD115E0("),
    "CreateMissile_range100": ("d2moo-D2Game-Skills.cpp",
                               "if (UNITS_GetDistanceToCoordinates(pUnit, x, y) > 100)"),
    "CheckSkillDelay_def": ("d2moo-D2Common-D2Skills.cpp",
                            "BOOL __fastcall SKILLS_CheckSkillDelay("),
    "UseState_blocked": ("d2moo-D2Common-D2Skills.cpp",
                         "return SKILLUSTATE_BLOCKED;"),
    "CastAtXY_msg": ("d2moo-D2Game-PLAYER-PlrMsg.cpp",
                     "int32_t __fastcall sub_6FC83340("),
    "ModeChange_event_sched": ("d2moo-D2Game-UNIT-SUnit.cpp",
                               "EVENT_SetEvent(pGame, pUnit, EVENTTYPE_MODECHANGE, nFrame, nEvent, nParam);"),
    "DeletePerFrameEvents": ("d2moo-D2Game-UNIT-SUnit.cpp",
                             "void __fastcall D2GAME_DeletePlayerPerFrameEvents_6FCBCE50("),
    "PlrEvent_dispatch": ("d2moo-PlrModes.cpp",
                          "void __fastcall sub_6FC81600("),
    "PlrActionFrame": ("d2moo-PlrModes.cpp",
                       "int32_t __fastcall sub_6FC80EE0("),
    "StartXY_Cast": ("d2moo-PlrModes.cpp",
                     "void __fastcall PLRMODE_StartXY_AttackCastThrowKickSpecialSequence("),
    "StartXY_GetHit": ("d2moo-PlrModes.cpp",
                       "void __fastcall PLRMODE_StartXY_GetHit("),
    "StartXY_Block": ("d2moo-PlrModes.cpp",
                      "void __fastcall PLRMODE_StartXY_Block("),
    "Interrupt_flag_gate": ("d2moo-PlrModes.cpp",
                            "if (!(pUsedSkillsTxtRecord->dwFlags[0] & gdwBitMasks[SKILLSFLAGINDEX_INTERRUPT]))"),
    "Cast_allows_gethit_block": ("d2moo-PlrModes.cpp",
                                 "nMode == PLRMODE_GETHIT || nMode == PLRMODE_BLOCK"),
    "Player_gethit_trigger": ("d2moo-D2Game-UNIT-SUnitDmg.cpp",
                              "sub_6FC817D0(pGame, pUnit, nullptr, 4, pDamage->dwDmgTotal, 0, 0);"),
    "RemoveState_handler": ("d2moo-D2Game-MONSTER-MonsterMode.cpp",
                            "STATLIST_UpdateStatListsExpiration(pUnit, pGame->dwGameFrame);"),
    "Expire_le": ("d2moo-D2Common-D2StatList.cpp",
                  "if (pCurrent->dwExpireFrame <= nFrame)"),
    "Event_REMOVESTATE_12": ("d2moo-D2Game-GAME-Event.h",
                             "EVENTTYPE_REMOVESTATE = 12,"),
    "Collide_wall_1": ("d2moo-D2Common-D2Collision.h", "COLLIDE_WALL = 0x0001,"),
    "Collide_missile_barrier_4": ("d2moo-D2Common-D2Collision.h",
                                  "COLLIDE_MISSILE_BARRIER = 0x0004,"),
    "PlrMode_enum_start": ("d2moo-D2Common-Units-Player.h", "enum D2C_PlayerModes"),
    "PlrMode_CAST": ("d2moo-D2Common-Units-Player.h", "PLRMODE_CAST,"),
    "Txt_interrupt_bit": ("d2moo-D2Common-DataTbls-SkillsTbls.cpp",
                          "{ \"interrupt\", TXTFIELD_BIT, 31, 4, NULL },"),
}
facts["d2moo_anchors"] = {k: {"file": f, "line": anchor(f, n), "needle": n}
                          for k, (f, n) in A.items()}

# Negative search: nothing clears the skill delay except expiry / unit teardown.
neg = {}
for fname in sorted(os.listdir(CAP)):
    if not fname.startswith("d2moo-"):
        continue
    with open(os.path.join(CAP, fname), encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            if "STATE_SKILLDELAY" in line:
                neg.setdefault(fname, []).append(i)
facts["state_skilldelay_refs_in_captures"] = neg

facts["inputs"] = {
    "Skills.txt": sha(os.path.join(RAW, "Skills.txt")),
    "Missiles.txt": sha(os.path.join(RAW, "Missiles.txt")),
}
facts["captures_sha256"] = {}
for root, _, files in os.walk(CAP):
    for fn in sorted(files):
        p = os.path.join(root, fn)
        facts["captures_sha256"][os.path.relpath(p, CAP)] = sha(p)

facts["failures"] = failures
out = os.path.join(HERE, "meteor_delay_facts.json")
with open(out, "w") as f:
    json.dump(facts, f, indent=1, sort_keys=True)
    f.write("\n")
print(f"wrote {out}; failures={len(failures)}")
for x in failures:
    print("  FAIL", x)
sys.exit(1 if failures else 0)
