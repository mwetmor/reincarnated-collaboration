#!/usr/bin/env python3
"""Tie-order follow-up: re-derive the same-frame ordering facts (incoming hit
vs her action frame) and the post-delay recast stamp from the pinned captures.

Read-only. Run with:  python3 -I verify_tie_order.py
Writes tie_order_facts.json; exits non-zero on a missing anchor or a broken
ordering assertion.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, "captures")
failures = []


def find(fname, needle, after=0):
    with open(os.path.join(CAP, fname), encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            if i > after and needle in line:
                return i
    failures.append(f"anchor missing: {fname}: {needle!r} (after L{after})")
    return None


EV = "d2moo-D2Game-GAME-Event.cpp"
GM = "d2moo-D2Game-GAME-Game.cpp"
A = {}

# 1. Per-frame order inside GAME_UpdateProgress
A["UpdateProgress_def"] = (GM, "void __fastcall GAME_UpdateProgress(D2GameStrc* pGame)", 0)
A["frame_increment"] = (GM, "++pGame->dwGameFrame;", 1789)
A["iterate_events_call"] = (GM, "    EVENT_IterateEvents(pGame);", 1789)
A["IterateEvents_def"] = (EV, "void __fastcall EVENT_IterateEvents(D2GameStrc* pGame)", 0)
A["bucket_missile_inf"] = (EV, "EVENT_ExecuteMissileEvents(pGame, pTimerQueue, pTimerQueue->pInfinite[nMissileEventIdx], 0);", 0)
A["bucket_missile_slot"] = (EV, "EVENT_ExecuteMissileEvents(pGame, pTimerQueue, pTimerQueue->pHead[nMissileEventIdx][pTimerQueue->nArrayIndex], 1);", 0)
A["bucket_player_inf"] = (EV, "EVENT_ExecutePlayerEvents(pGame, pTimerQueue, pTimerQueue->pInfinite[nPlayerEventIdx], 0);", 0)
A["bucket_player_slot"] = (EV, "EVENT_ExecutePlayerEvents(pGame, pTimerQueue, pTimerQueue->pHead[nPlayerEventIdx][pTimerQueue->nArrayIndex], 1);", 0)
A["bucket_monster_inf"] = (EV, "EVENT_ExecuteMonsterEvents(pGame, pTimerQueue, pTimerQueue->pInfinite[nMonsterEventIdx], 0);", 0)
A["bucket_monster_slot"] = (EV, "EVENT_ExecuteMonsterEvents(pGame, pTimerQueue, pTimerQueue->pHead[nMonsterEventIdx][pTimerQueue->nArrayIndex], 1);", 0)
A["slot_exact_frame_match"] = (EV, "if (pTimer->nExpireFrame == pGame->dwGameFrame)", 0)
A["infinite_timer_expire_minus1"] = (EV, "pNewTimer->nExpireFrame = -1;", 0)
A["infinite_list_select"] = (EV, "return &pGame->pTimerQueue->pInfinite[nIndex];", 0)
A["infinite_push_head"] = (EV, "*ppEventTimer = pNewTimer;", 500)

# 2. Missile hits: per-frame infinite event -> collision -> damage -> GetHit
A["missile_per_frame_timer"] = ("d2moo-D2Game-MISSILES-Missiles.cpp", "sub_6FC35570(pGame, pMissile, EVENTTYPE_MODECHANGE, 0, 0);", 0)
A["missile_event_handler"] = ("d2moo-D2Game-MISSILES-MissMode.cpp", "void __fastcall MISSMODE_SrvDoHandler(D2GameStrc* pGame, D2UnitStrc* pMissile, D2C_EventTypes nEventType)", 0)
A["missile_basic_collision"] = ("d2moo-D2Game-MISSILES-MissMode.cpp", "return MISSMODE_HandleMissileCollision(pGame, pMissile);", 4864)
A["missile_damage_exec"] = ("d2moo-D2Game-MISSILES-MissMode.cpp", "SUNITDMG_ExecuteMissileDamage(pGame, pOwner, pDefender, pDamage);", 0)

# 3. Melee hits: monster action-frame event -> SrvDo001 -> damage now
SK = "d2moo-D2Game-Skills.cpp"
A["SrvDo001_def"] = (SK, "int32_t __fastcall SKILLS_SrvDo001_Attack_LeftHandSwing(", 0)
A["SrvDo001_alloc_combat"] = (SK, "SUNITDMG_AllocCombat(pGame, pUnit, pTarget, &damage, 128);", 2025)
A["SrvDo001_apply_now"] = (SK, "SUNITDMG_DrainItemDurability(pGame, pUnit, pTarget, 0);", 2025)
DM = "d2moo-D2Game-UNIT-SUnitDmg.cpp"
A["melee_exec_fn"] = (DM, "void __fastcall SUNITDMG_DrainItemDurability(", 0)
A["melee_exec_damage"] = (DM, "SUNITDMG_ExecuteMissileDamage(pGame, pAttacker, pDefender, &damageCopy);", 2283)
A["damage_exec_fn"] = (DM, "void __fastcall SUNITDMG_ExecuteMissileDamage(", 0)
A["player_gethit_trigger"] = (DM, "sub_6FC817D0(pGame, pUnit, nullptr, 4, pDamage->dwDmgTotal, 0, 0);", 1934)
A["monster_event_dispatch"] = ("d2moo-D2Game-MONSTER-MonsterMode.cpp", "void __fastcall MONSTERMODE_EventHandler(", 0)

# 4. Her action frame and its cancellation
A["player_event_dispatch"] = ("d2moo-PlrModes.cpp", "void __fastcall sub_6FC81600(", 0)
A["gethit_start_deletes_events"] = ("d2moo-PlrModes.cpp", "void __fastcall PLRMODE_StartXY_GetHit(", 0)
A["delete_per_frame_events"] = ("d2moo-D2Game-UNIT-SUnit.cpp", "void __fastcall D2GAME_DeletePlayerPerFrameEvents_6FCBCE50(", 0)

# 5. Recast stamp: packets are a separate locked entry, processed between frames
A["net_entry"] = (GM, "void __fastcall GAME_ProcessNetworkMessages()", 0)
A["net_dispatch"] = (GM, "CCMD_ProcessClientMessage(buffer, nSize);", 1694)
A["ccmd_def"] = ("d2moo-D2Game-GAME-CCmd.cpp", "void __fastcall CCMD_ProcessClientMessage(void* pData, int32_t nPacketSize)", 0)
A["ccmd_immediate_handler"] = ("d2moo-D2Game-GAME-CCmd.cpp", "D2GAME_PACKET_Handler_6FC89320(pGame, pPlayer, pPacket, nPacketSize)", 0)
A["lock_by_client"] = (GM, "D2GameStrc* __fastcall GAME_GetGameByClientId(int32_t nClientId)", 0)
A["lock_game_cs"] = (GM, "D2_LOCK(pGame->lpCriticalSection);", 2435)
A["cast_req_handler"] = ("d2moo-D2Game-PLAYER-PlrMsg.cpp", "int32_t __fastcall sub_6FC83340(", 0)
A["cast_req_usable_only"] = ("d2moo-D2Game-PLAYER-PlrMsg.cpp", "if (nSkillUseState == SKILLUSTATE_USABLE)", 812)
A["delay_check_blocked"] = ("d2moo-D2Common-D2Skills.cpp", "return SKILLUSTATE_BLOCKED;", 0)
A["sched_from_current_frame"] = ("d2moo-D2Game-UNIT-SUnit.cpp", "    int32_t nFrame = pGame->dwGameFrame;", 1466)
A["sched_first_step_plus1"] = ("d2moo-D2Game-UNIT-SUnit.cpp", "            ++nFrame;", 1473)
A["setdelay_expire"] = (SK, "const int32_t nExpireFrame = nDelay + pGame->dwGameFrame;", 0)
A["removestate_handler"] = ("d2moo-D2Game-MONSTER-MonsterMode.cpp", "STATLIST_UpdateStatListsExpiration(pUnit, pGame->dwGameFrame);", 0)
A["expire_le"] = ("d2moo-D2Common-D2StatList.cpp", "if (pCurrent->dwExpireFrame <= nFrame)", 0)

anchors = {k: {"file": f, "needle": n, "line": find(f, n, after)} for k, (f, n, after) in A.items()}


def L(k):
    return anchors[k]["line"]


checks = {
    "frame_increment_before_events": (L("frame_increment") or 0) < (L("iterate_events_call") or 0),
    "missile_before_player_before_monster": (L("bucket_missile_inf") or 0) < (L("bucket_missile_slot") or 0)
        < (L("bucket_player_inf") or 0) < (L("bucket_player_slot") or 0)
        < (L("bucket_monster_inf") or 0) < (L("bucket_monster_slot") or 0),
    "melee_damage_applied_inside_SrvDo001": (L("SrvDo001_def") or 0) < (L("SrvDo001_alloc_combat") or 0)
        < (L("SrvDo001_apply_now") or 0),
    "gethit_trigger_inside_damage_exec": (L("damage_exec_fn") or 0) < (L("player_gethit_trigger") or 0)
        < (L("melee_exec_fn") or 0),
    "net_entry_separate_from_update": (L("net_entry") or 0) < (L("UpdateProgress_def") or 0),
}
for k, ok in checks.items():
    if not ok:
        failures.append(f"check failed: {k}")

facts = {
    "d2moo_anchors": anchors,
    "checks": checks,
    "captures_sha256": {fn: hashlib.sha256(open(os.path.join(CAP, fn), "rb").read()).hexdigest()
                        for fn in sorted({a["file"] for a in anchors.values()})},
    "failures": failures,
}
out = os.path.join(HERE, "tie_order_facts.json")
with open(out, "w") as f:
    json.dump(facts, f, indent=1, sort_keys=True)
    f.write("\n")
print(f"wrote {out}; failures={len(failures)}")
for x in failures:
    print("  FAIL", x)
sys.exit(1 if failures else 0)
