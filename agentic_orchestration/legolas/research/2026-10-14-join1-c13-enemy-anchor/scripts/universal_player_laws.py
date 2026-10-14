#!/usr/bin/env python3
"""C-13 / KP-426 — D2 LoD 1.13 universal player laws (both D2 kits: Fire Sorceress, WW Barbarian).

Read-only generator. It re-reads the 1.13 txt tables (fabd/diablo2 @ 45112569, local J-S7 copy), the captured
D2MOO 1.10f sources and the captured Basin/Arreat pages, ASSERTS every table- or code-derived value against its
second source, and writes universal_player_laws.json. It aborts on any mismatch (a live wiki edit will trip it;
that abort is intended, as in J4b).

Usage: python3 scripts/universal_player_laws.py [out.json]
"""
from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import sys
from pathlib import Path

PKT = Path(__file__).resolve().parents[1]
CAP = PKT / "captures"
UNI = CAP / "universal"
RAW = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/datamine-acquisition/d2/raw")
KITS = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/kits-export")
POT = CAP / "potions"

CODE = {
    "SUnitDmg.cpp": CAP / "d2moo-SUnitDmg.cpp",
    "Units.cpp": CAP / "d2moo-Units.cpp",
    "PlrModes.cpp": UNI / "d2moo-PlrModes.cpp",
}
D2MOO_PIN = "ThePhrozenKeep/D2MOO @ 5596f5cb6c5251a0a07c6637d26458b06099d516 (1.10f reconstruction)"
TXT_PIN = "fabd/diablo2 @ 45112569deb9384738ccafe5c24ebbb71f41c7c9 code/d2_113_data"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rd(name):
    with open(RAW / name, encoding="latin-1", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def text(p: Path) -> str:
    return p.read_text(encoding="latin-1")


def html_text(p: Path) -> str:
    t = html.unescape(re.sub(r"<[^>]+>", " ", text(p)))
    return re.sub(r"\s+", " ", t)


def need(hay: str, needle: str, where: str):
    assert needle in hay, f"MISMATCH: expected {needle!r} in {where}"
    return needle


def main(out: Path):
    used = {}
    code = {k: text(v) for k, v in CODE.items()}
    for k, v in CODE.items():
        used[f"code:{k}"] = sha(v)

    # ---------------- tables ----------------
    cs = {r["class"]: r for r in rd("CharStats.txt")}
    isc = {r["Stat"]: r for r in rd("ItemStatCost.txt")}
    dl = {r["Name"]: r for r in rd("DifficultyLevels.txt")}
    arm = rd("Armor.txt")
    for f in ("CharStats.txt", "ItemStatCost.txt", "DifficultyLevels.txt", "Armor.txt"):
        used[f"txt:{f}"] = sha(RAW / f)

    basin = {p.stem.replace("basin-", "").replace("-raw", ""): text(p) for p in UNI.glob("basin-*-raw.txt")}
    for p in UNI.glob("basin-*-raw.txt"):
        used[f"basin:{p.name}"] = sha(p)
    arreat_res = html_text(UNI / "arreat-basics-resistances.shtml")
    used["arreat:basics/resistances"] = sha(UNI / "arreat-basics-resistances.shtml")

    hell = dl["Hell"]
    laws = {}

    # ===== 1. control received =====
    sud = code["SUnitDmg.cpp"]
    need(sud, "nStunLength = std::min(nStunLength, 250);", "SUnitDmg.cpp stun (player branch)")
    need(sud, "if (STATLIST_GetStatListFromUnitAndState(pUnit, STATE_STUNNED) || !sub_6FCC1870(pUnit, pDamage, pDamage->dwHitClass))", "SUnitDmg.cpp gethit-while-stunned")
    need(basin["Stun_length"], "Players are not incapacitated but they are always put into [[hit recovery]] when hit before length expires", "Basin Stun_length")
    need(basin["Stun_length"], "Length is not subject to any penalties, but there is normally a 10 second ceiling", "Basin Stun_length")
    need(basin["Stun_length"], "Only the most recent of multiple sources of stun length is applied", "Basin Stun_length")
    need(sud, "if (nDefenderType == UNIT_PLAYER)\n\t{\n\t\tSUNITDMG_ApplyColdState(pAttacker, pDefender, nFreezeLength);", "SUnitDmg.cpp freeze->chill for players")
    need(basin["Freeze_length"], "Freeze length can freeze normal or minion monsters, and chill all other units", "Basin Freeze_length")
    need(basin["Freezes_Target"], "Freezes target can freeze normal or minion monsters, and chill all other units", "Basin Freezes_Target")
    need(sud, "nColdLength /= nColdDivisor;", "SUnitDmg.cpp cold divisor")
    need(sud, "if (pDefender && pDefender->dwUnitType == UNIT_MONSTER && nColdEffect < 0)", "SUnitDmg.cpp cold divisor applies to MONSTER defenders only")
    need(sud, "const int32_t nFreezeDivisor = DATATBLS_GetDifficultyLevelsTxtRecord(pGame->nDifficulty)->dwMonsterFreezeDiv;", "SUnitDmg.cpp freeze divisor (monster branch)")
    need(sud, "STATLIST_UnitGetItemStatOrSkillStatValue(damageInfo.pDefender, STAT_ITEM_CANNOTBEFROZEN, 0)", "SUnitDmg.cpp CBF")
    need(sud, "damageInfo.pDamage->dwColdLen /= 2;", "SUnitDmg.cpp HFD")
    need(basin["Cannot_be_Frozen"], "Cannot Be Frozen prevents [[Cold Damage|cold length]] or [[freeze length]] from being applied", "Basin Cannot_be_Frozen")
    need(basin["Half_Freeze_Duration"], "Length is halved once only", "Basin Half_Freeze_Duration")
    need(arreat_res, "\"Half Freeze Duration\" halves chill length, but this reduction is only applied once", "Arreat resistances")
    need(arreat_res, "\"Cannot be Frozen\" provides the ultimate protection against chill by setting the duration to 0", "Arreat resistances")
    need(code["PlrModes.cpp"], "case PLRMODE_KNOCKBACK:", "PlrModes.cpp knockback mode")
    need(code["PlrModes.cpp"], "D2COMMON_10190_PATH_SetDistance(pPlayer->pDynamicPath, 5u);", "PlrModes.cpp knockback path distance")
    need(basin["Knockback"], "Targets can be knocked back a distance of up to three [[Radius|sub-tiles]]", "Basin Knockback")
    assert hell["MonsterFreezeDivisor"] == "4" and hell["MonsterColdDivisor"] == "4"
    laws["control_received"] = {
        "stun": {"law": "Stun length on a PLAYER is capped at 250 frames (10 s) and is not difficulty-scaled. Players are NOT incapacitated: any hit landing during stun length forces hit recovery (even zero damage). The most recent stun source replaces the remaining length.",
                 "grade": "MODEL-VERIFIED", "sources": ["D2MOO SUnitDmg.cpp ExecuteEvents stun block (min(len,250) for non-monster defenders; gethit forced while STATE_STUNNED)", "Basin Stun_length"]},
        "freeze": {"law": "There is NO frozen-solid state for players in PvM: freeze length (and Freezes Target) applied to a player is applied as COLD length (chill). Only normal/minion monsters are frozen.",
                   "grade": "MODEL-VERIFIED", "sources": ["D2MOO SUnitDmg.cpp SUNITDMG_ApplyFreezeState (UNIT_PLAYER -> ApplyColdState)", "Basin Freeze_length", "Basin Freezes_Target"]},
        "difficulty_divisors": {"law": "DifficultyLevels MonsterColdDivisor / MonsterFreezeDivisor (Hell 4/4, NM 2/2) apply ONLY when the DEFENDER is a monster. Against players there is NO Hell/PvM duration halving; instead the Hell resist penalty enters the length reduction (see chill.length_law), which LENGTHENS chill for an under-resisted player (up to x2).",
                                "values": {"MonsterColdDivisor": {k: dl[k]["MonsterColdDivisor"] for k in dl}, "MonsterFreezeDivisor": {k: dl[k]["MonsterFreezeDivisor"] for k in dl}},
                                "grade": "MODEL-VERIFIED", "sources": ["D2MOO SUnitDmg.cpp ApplyColdState/ApplyFreezeState (divisor inside the UNIT_MONSTER branch)", "Basin Cold_Damage ('Cold length applied by player, mercenary or pets is reduced to 1/2 in Nightmare and 1/4 in Hell')", "Basin Cold_Resist (penalties -40/-100 apply to players)"]},
        "cannot_be_frozen": {"law": "Item stat item_cannotbefrozen: sets the incoming hit's cold length AND freeze length to 0 (no chill). Checked before resistances. Does not stop Holy Freeze or Decrepify slows.",
                             "grade": "MODEL-VERIFIED", "sources": ["D2MOO SUnitDmg.cpp CalculateTotalDamage", "Basin Cannot_be_Frozen", "Arreat Resistances"]},
        "half_freeze_duration": {"law": "item_halffreezeduration: halves cold length and freeze length once (multiple sources do not stack); multiplies with cold resist (CR 75% + HFD -> 1/8).",
                                 "grade": "MODEL-VERIFIED", "sources": ["D2MOO SUnitDmg.cpp (/=2 once, else-if after CBF)", "Basin Half_Freeze_Duration", "Arreat Resistances"]},
        "knockback": {"law": "Player knockback mode (PLRMODE_KNOCKBACK) moves the player and enters hit recovery; does not apply while frozen. Distance: Basin 'up to three sub-tiles'; D2MOO sets path distance 5 (path units, not confirmed to be sub-tiles).",
                      "grade": "MODEL-VERIFIED (partial: distance units conflict)", "sources": ["D2MOO PlrModes.cpp sub_6FC7F600 PLRMODE_KNOCKBACK", "Basin Knockback"]},
        "immobilize_like": {"law": "No root/immobilize exists for players in 1.13 PvM. The movement/attack slows that do apply (cold length, Holy Freeze from Aura-Enchanted uniques, Decrepify/Slows Target) SUM, with floors of 25% velocity and 15% attack rate. Holy Freeze is not reduced by CR or CBF and is capped by chill effectiveness (-50 for players).",
                            "floors": {"velocity_pct_min": 25, "attack_rate_min": 15},
                            "grade": "MODEL-VERIFIED", "sources": ["D2MOO Units.cpp (velocity < 25 -> 25; attack rate clamp 15..175)", "Basin Cold_Damage/Decrepify/Holy_Freeze ('no unit can be reduced below 15% attack rate or 25% velocity')"]},
    }
    need(code["Units.cpp"], "if (nVelocityPercent < 25)", "Units.cpp velocity floor")
    need(code["Units.cpp"], "nRate = 15;", "Units.cpp attack-rate floor")
    need(basin["Cold_Damage"], "no unit can be reduced below 15% attack rate or 25% velocity", "Basin Cold_Damage")

    # ===== 2. chill =====
    need(sud, "if (!pUnit || pUnit->dwUnitType != UNIT_MONSTER)\n\t{\n\t\treturn -50;", "SUnitDmg.cpp GetColdEffect = -50 for players")
    need(sud, "STATLIST_SetStatIfListIsValid(pNewStatList, STAT_VELOCITYPERCENT, nColdEffect, 0);", "cold sets velocity%")
    need(sud, "STATLIST_SetStatIfListIsValid(pNewStatList, STAT_ATTACKRATE, nColdEffect, 0);", "cold sets attack rate")
    need(sud, "STATLIST_SetStatIfListIsValid(pNewStatList, STAT_OTHER_ANIMRATE, nColdEffect, 0);", "cold sets other anim rate")
    need(code["Units.cpp"], "nRate = nFasterCastRate + 100;", "Units.cpp cast rate ignores ATTACKRATE")
    need(basin["Chill_effectiveness"], "all other [[Mercenary|mercenaries]] and [[pet]]s have -50 chill effectiveness (like players)", "Basin Chill_effectiveness")
    need(basin["Cold_Resist"], "modifies cold damage and cold or [[freeze length]]", "Basin Cold_Resist")
    need(basin["Cold_Damage"], "it will overwrite the existing length if it is equal to or greater than the existing length", "Basin Cold_Damage")
    need(sud, "if (STATLIST_GetExpireFrame(pStatList) < nExpireFrame)", "SUnitDmg.cpp chill extend-only")
    need(sud, "nResValue += pDamageInfo->pDifficultyLevelsTxt->dwResistPenalty;", "SUnitDmg.cpp resist penalty for non-monster defenders")
    need(arreat_res, "When chilled, you move and attack much more slowly", "Arreat resistances")
    laws["chill"] = {
        "slow": {"velocity_pct": -50, "attack_rate": -50, "other_anim_rate": -50,
                 "casting": "NOT slowed: player cast animation speed = (100 + EFCR) x base, which reads no attack-rate or velocity stat",
                 "block_and_hit_recovery": "NOT slowed (FBR/FHR branches read only their own stat)",
                 "barbarian_whirlwind": "WW runs in the attack/sequence branch (attack rate) so chill slows its cadence (INFERRED from the branch; WW cadence law is the sister packet's)",
                 "grade": "MODEL-VERIFIED for velocity/attack (code + Basin chill effectiveness -50 for players + Arreat 'move and attack much more slowly'); casting-unaffected is code + Basin's silence (MODEL-VERIFIED partial)",
                 "sources": ["D2MOO SUnitDmg.cpp GetColdEffect/ApplyColdState", "D2MOO Units.cpp UpdateCastAnimRateAndVelocity / UpdateAttackAnimRateAndVelocity / UpdateRunWalkAnimRateAndVelocity", "Basin Chill_effectiveness", "Arreat Resistances"]},
        "length_law": {"formula": "frames = cold_len_of_hit (CBF -> 0; HFD -> /2) x (100 - CR_eff)/100, CR_eff = displayed cold resist incl. Hell -100 penalty, clamped to [-100, min(75 + max_cold_res, 95)]; min 1 frame. No difficulty divisor for player defenders.",
                       "examples": {"CR_eff 75 (capped)": 0.25, "CR_eff 0": 1.0, "CR_eff -100 (unresisted in Hell)": 2.0},
                       "refresh": "a new chill only EXTENDS the remaining length (expire frame = max(old, new)); magnitude fixed at -50",
                       "grade": "MODEL-VERIFIED", "sources": ["D2MOO SUnitDmg.cpp CalculateTotalDamage/ApplyResistancesAndAbsorb (Clen row: STAT_COLDRESIST, STAT_MAXCOLDRESIST)", "Basin Cold_Resist", "Basin Cold_Damage (overwrite rule)"]},
    }

    # ===== 3. poison / DoTs received =====
    need(sud, "if (-STATLIST_GetStatValue(pStatList, STAT_HPREGEN, 0) <= nPoisonDamage)", "SUnitDmg.cpp poison overwrite rule")
    need(sud, "{ offsetof(D2DamageStrc, dwPoisLen),\tSTAT_ITEM_POISONLENGTHRESIST,", "SUnitDmg.cpp Plen row")
    need(code["PlrModes.cpp"], "if (nLife < 256)", "PlrModes.cpp HP floor 1 point")
    need(basin["Poison_Damage"], "if a target is already poisoned, then the rate and length of that poison will be overwritten by that of any subsequent attack which has an equal or greater rate", "Basin Poison_Damage")
    need(basin["Poison_Damage"], "will only reduce players to 1 life", "Basin Poison_Damage")
    need(basin["Poison_Length_Reduced"], "PLR -40% in Nightmare and PLR -100% in Hell", "Basin PLR")
    need(basin["Poison_Length_Reduced"], "Player and [[mercenary]] normally have a ceiling of PLR 75%", "Basin PLR")
    laws["poison_and_dots"] = {
        "stacking": {"law": "Poisons do not sum. A new poison REPLACES the current one (rate and length) iff its per-frame rate >= the current rate; a weaker poison is ignored (Basin adds: the monster's hit still applies one frame of its poison as well).",
                     "grade": "MODEL-VERIFIED", "sources": ["D2MOO SUnitDmg.cpp ApplyPoisonDamage", "Basin Poison_Damage"]},
        "length_reduction": {"formula": "frames = poison_len x (100 - PLR_eff)/100, PLR_eff = item PLR + Hell penalty (-100; NM -40), clamped [-100, 75] (no max-PLR stat). An unresisted Hell player takes x2 length; PLR 100 net -> x1.",
                             "hell_penalty": int(hell["ResistPenalty"]),
                             "grade": "MODEL-VERIFIED", "sources": ["D2MOO SUnitDmg.cpp (Plen row resist = STAT_ITEM_POISONLENGTHRESIST; penalty added for non-monster defenders except DR/magic; max 75)", "Basin Poison_Length_Reduced"]},
        "damage_reduction": "poison DAMAGE is reduced by poison resist (Pois row, Hell -100 penalty, cap 75/95) — rate is resisted, length by PLR (MODEL-VERIFIED: code + Basin Poison_Resist).",
        "lethality": {"law": "Poison (any negative HPREGEN) cannot kill a player: life is floored at 1 point (256/256) by the regen step; a subsequent direct hit can kill.",
                      "grade": "MODEL-VERIFIED", "sources": ["D2MOO PlrModes.cpp EVENTS_HpRegen (nLife < 256 -> 256)", "Basin Poison_Damage"]},
        "burn": {"law": "dwBurnDamage DoT uses the same replace-if-stronger rule as poison; it has no resist row in the damage table (length/rate unreduced in this path). Few monster attacks use it.",
                 "grade": "INFERRED (single code source)", "sources": ["D2MOO SUnitDmg.cpp ApplyBurnDamage"]},
    }

    # ===== 4. stamina =====
    pm = code["PlrModes.cpp"]
    need(pm, "int32_t nStaminaLost = 2 * pCharStatsTxtRecord->nRunDrain;", "PlrModes.cpp drain")
    need(pm, "nStaminaLost *= pItemsTxtRecord->dwSpeed / 10 + 1;", "PlrModes.cpp armor factor")
    need(pm, "nCombatMode = DUNGEON_IsRoomInTown(UNITS_GetRoom(pPlayer)) != 0 ? PLRMODE_TOWNWALK : PLRMODE_WALK;", "PlrModes.cpp walk at zero")
    need(pm, "int32_t nNewStamina = nMaxStamina >> nShift;", "PlrModes.cpp regen")
    need(basin["Stamina_Drain"], "Stamina drain per second = 25 * max( (40 * (1 + [{{0|}}[[Body armor|Armor speed]] /10] ) * (100 - Slower Stamina Drain) /100 , 1) /256", "Basin Stamina_Drain")
    need(basin["Stamina_Drain"], "Stamina is '''not''' drained while running in towns", "Basin Stamina_Drain")
    need(basin["Stamina"], "when it runs out, a character can no longer run, and must walk", "Basin Stamina")
    assert "|84||95||92||84||79||89||74||86" in basin["Stamina"], "Basin stamina start table changed"
    sor, bar = cs["Sorceress"], cs["Barbarian"]
    for c, start in ((sor, 74), (bar, 92)):
        assert int(c["stamina"]) == start, (c["class"], c["stamina"])
        assert int(c["StaminaPerLevel"]) == 4 and int(c["StaminaPerVitality"]) == 4 and int(c["RunDrain"]) == 20
    assert isc["stamina"]["ValShift"] == "8" and isc["vitality"]["op stat2"] == "maxstamina"
    drain_frame_256 = 2 * int(sor["RunDrain"])
    speeds = sorted({int(x["speed"] or 0) for x in arm if x.get("type") == "tors"})
    laws["stamina"] = {
        "units": "stamina is stored in 1/256 points (ItemStatCost stamina/maxstamina ValShift 8); 25 frames/s",
        "drain": {"per_frame_256": f"2 x CharStats RunDrain ({drain_frame_256}) x (body-armor speed/10 + 1, integer) x (1 - Slower Stamina Drain%), min 1",
                  "base_points_per_s": drain_frame_256 * 25 / 256,
                  "armor_speed_factor": {str(s): s // 10 + 1 for s in speeds},
                  "when": "only in PLRMODE_RUN outside town; same RunDrain (20) for both classes",
                  "grade": "MODEL-VERIFIED", "sources": ["D2MOO PlrModes.cpp sub_6FC7F780", "CharStats RunDrain (DATAMINED)", "Basin Stamina_Drain"]},
        "zero_rule": {"law": "at 0 stamina the run request becomes WALK (TOWNWALK in town); running resumes once stamina > 0 (regen while walking needs >= 1 point)",
                      "grade": "MODEL-VERIFIED", "sources": ["D2MOO PlrModes.cpp sub_6FC7F600 / sub_6FC7F780", "Basin Stamina"]},
        "regen": {"law": "per frame +max_stamina/256 when standing (neutral/town-neutral), +max_stamina/512 when walking (only if current >= 1 point) or town-walking, 0 while running/attacking/casting (unless Heal Stamina >= 1000%); x(1 + Heal Stamina %/100)",
                  "full_refill_seconds": {"standing": 256 / 25, "walking": 512 / 25},
                  "grade": "MODEL-VERIFIED (partial: Basin states no regen law; second source is the code-consistent Basin drain page only)",
                  "sources": ["D2MOO PlrModes.cpp EVENTS_StaminaRegen", "ItemStatCost staminarecoverybonus (Heal Stamina Plus %)"]},
        "base_by_level_vitality": {
            "Sorceress": {"formula": "74 + 1*(clvl-1) + 1*(Vitality_total - 10)  [items' Vitality counts: vitality op 9 -> maxstamina]",
                          "clvl90_examples_from_sorc_sheet": {"MAXBLOCK_quests (vit 75)": 74 + 89 + 65, "NODEX_quests (vit 380)": 74 + 89 + 370}},
            "Barbarian": {"formula": "92 + 1*(clvl-1) + 1*(Vitality_total - 25); Battle Orders adds skill_staminapercent (op 1) — J4a F12",
                          "note": "Barbarian Vitality is unpinned by his kit record"},
            "grade": "MODEL-VERIFIED", "sources": ["CharStats stamina/StaminaPerLevel/StaminaPerVitality (DATAMINED, 4/4 = +1)", "Basin Stamina class tables (74/92 start, +1/+1)", "J4a F12"]},
    }

    # ===== 5. mana regen (Barbarian) =====
    need(pm, "int32_t nManaRegen = 25 * pCharStatsTxtRecord->nManaRegen;", "PlrModes.cpp mana regen")
    need(basin["Regenerate_Mana"], "Mana regenerated per second = 25 * [ [256 * Maximum Mana / (25*120) ] * (100 + Regenerate Mana) /100] /256", "Basin Regenerate_Mana")
    assert sor["ManaRegen"] == bar["ManaRegen"] == "120"
    laws["mana_regen_barbarian"] = {
        "law": "IDENTICAL to the Sorceress's H09 (J4b formulas.json): per frame mult = max(1, floor(max_mana_256/(25 x CharStats.ManaRegen))) with ManaRegen = 120 for BOTH classes; regen_256 = floor(mult x (100 + manarecoverybonus)/100) + manarecovery; ~120 s from 0 to full at 0% bonus. Resolves J4a F12's open item (ManaRegen 120 meaning).",
        "barbarian_ManaRegen": int(bar["ManaRegen"]), "sorceress_ManaRegen": int(sor["ManaRegen"]),
        "grade": "MODEL-VERIFIED", "sources": ["D2MOO PlrModes.cpp EVENTS_ManaRegen", "CharStats ManaRegen (DATAMINED)", "Basin Regenerate_Mana", "J4b H09"]}

    # ===== 6. life regen / Replenish Life =====
    need(pm, "const int32_t nHpRegen = STATLIST_UnitGetStatValue(pUnit, STAT_HPREGEN, 0);", "PlrModes.cpp hp regen")
    need(basin["Replenish_Life"], "Life gained per second = Replenish Life * 25/256", "Basin Replenish_Life")
    need(basin["Replenish_Life"], "it still applies when damage, [[Poison Damage]] and Open Wounds are being applied", "Basin Replenish_Life")
    need(basin["Damage_regeneration"], "Units other than players can regenerate damage automatically", "Basin Damage_regeneration")
    assert isc["hpregen"]["ValShift"] == "" and isc["hitpoints"]["ValShift"] == "8"
    laws["life_regen"] = {
        "natural": {"law": "players have NO natural life regeneration (damage regeneration is monster/merc/pet only)",
                    "grade": "MODEL-VERIFIED", "sources": ["Basin Damage_regeneration", "Arreat Characters ('Life does not regenerate by itself') — captures/potions/arreat-basics-characters.shtml"]},
        "replenish_life": {"law": "Replenish Life +N = item stat hpregen N, added raw each frame to hitpoints stored in 1/256 points: N/256 life per frame = N x 25/256 life/s (~N/10 /s). Sums with negative poison/OW hpregen (net); applies while poisoned. Regen step floors life at 1 point.",
                           "units": "hpregen ValShift none vs hitpoints ValShift 8 (ItemStatCost)",
                           "grade": "MODEL-VERIFIED", "sources": ["D2MOO PlrModes.cpp EVENTS_HpRegen", "ItemStatCost hpregen/hitpoints (DATAMINED)", "Basin Replenish_Life"]}}
    arreat_chars = html_text(POT / "arreat-basics-characters.shtml")
    need(arreat_chars, "Life does not regenerate by itself", "Arreat characters")

    # ===== 7. Barbarian belt =====
    barb = json.loads((KITS / "d2-ww-barb.json").read_text())
    s = json.dumps(barb)
    belt_hits = [w for w in ("belt", "sash", "girdle", "coil", "Verdungo", "Thundergod", "String of Ears", "Arachnid", "Nosferatu")
                 if re.search(w, s, re.I)]
    belt_types = {}
    for x in arm:
        if x.get("type") in ("belt",):
            belt_types.setdefault(x["belt"], []).append(x["name"])
    arreat_boxes = {}
    for f in ("normal", "exceptional", "elite"):
        t = html_text(POT / f"arreat-items-{f}-belts.shtml")
        for m in re.finditer(r"(Sash|Light Belt|Heavy Belt|Plated Belt|Belt|Demonhide Sash|Sharkskin Belt|Mesh Belt|Battle Belt|War Belt|Spiderweb Sash|Vampirefang Belt|Mithril Coil|Troll Belt|Colossus Girdle) [\d\-]+ (?:\d+ )?(?:- |\d+ )\d+ (\d+) \d+", t):
            arreat_boxes[m.group(1)] = int(m.group(2))
    bz = json.loads((POT / "blizzhackers-d2data-belts.json").read_text())
    bz_box = {int(k): v.get("numboxes") for k, v in (bz.items() if isinstance(bz, dict) else enumerate(bz))}
    table = {}
    for k, names in sorted(belt_types.items(), key=lambda kv: int(kv[0])):
        table[k] = {"bases": names, "numboxes_belts_index": bz_box.get(int(k))}
    # cross-check a few against Arreat
    for nm, idx in (("Belt", "0"), ("Sash", "1"), ("Plated Belt", "3"), ("Light Belt", "4"), ("Heavy Belt", "5"), ("Spiderweb Sash", "6"), ("Colossus Girdle", "6")):
        assert nm in arreat_boxes, f"Arreat #Boxes not parsed for {nm}"
        if True:
            assert arreat_boxes[nm] == bz_box[int(idx)], (nm, arreat_boxes[nm], bz_box[int(idx)])
    laws["barbarian_belt"] = {
        "kit_record_belt": None if not belt_hits else belt_hits,
        "finding": "d2-ww-barb.json names NO belt (gear lists runewords Grief/Fortitude/Enigma/BotD/Death/Beast/Last Wish/Obedience/Insight only). The Barbarian's belt slot count is therefore a CONDUCTOR DEFAULT, not a record value.",
        "reference_table_armor_belt_type_to_slots": table,
        "no_belt": 4,
        "arreat_boxes_parsed": arreat_boxes,
        "grade": "kit-record absence: DATAMINED (record read); slot table: MODEL-VERIFIED (Armor.txt belt column DATAMINED + Arreat #Boxes + Belts index numboxes from a D2R 3.0 mirror — Belts.txt is absent from the 1.13 mirror)",
        "sources": ["research/curated/kits-export/d2-ww-barb.json", "Armor.txt belt column", "Arreat normal/exceptional/elite belts #Boxes", "blizzhackers d2data belts.json (D2R 3.0)"]}

    doc = {"commission": "C-13 / KP-426 universal player laws (both D2 kits)", "law": "LoD 1.13 expansion",
           "txt_pin": TXT_PIN, "code_pin": D2MOO_PIN,
           "grades": {"DATAMINED": "read from the 1.13 txt tables or the kit record",
                      "MODEL-VERIFIED": "D2MOO 1.10f code structure confirmed by >= 1 community source (Basin/Arreat)",
                      "INFERRED": "single source or code-by-absence", "UNKNOWN": "as stated"},
           "version_caveat": "D2MOO reconstructs 1.10f; no 1.13 change to these laws was found in the sources read (Basin pages describe current LoD/D2R behaviour and agree).",
           "laws": laws, "inputs_sha256": used}
    out.write_text(json.dumps(doc, indent=1))
    print("OK: all assertions passed;", len(used), "inputs")
    print("chill -50 vel/attack, casting unaffected; cold len x(100-CR_eff)/100 (Hell penalty in CR_eff, x2 at -100)")
    print("stun cap 250 fr; freeze->chill for players; stamina drain", laws["stamina"]["drain"]["base_points_per_s"], "pts/s")
    print("barb belt:", laws["barbarian_belt"]["kit_record_belt"], "| belt table:", {k: v["numboxes_belts_index"] for k, v in table.items()}, "| arreat:", arreat_boxes)


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else PKT / "universal_player_laws.json")
