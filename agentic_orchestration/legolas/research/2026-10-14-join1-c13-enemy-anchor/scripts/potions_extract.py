#!/usr/bin/env python3
"""C-13 row 21 (KP-423): D2 LoD 1.13 potion laws + the GD Warlord potion as the KC2 oracle carries it.

Read-only. Inputs:
  captures/potions/Misc.txt                       fabd/diablo2 @ 45112569 code/d2_113_data (fetched 2026-10-14)
  research/datamine-acquisition/d2/raw/Armor.txt  J-S7 local copy of the same pin
  captures/potions/blizzhackers-d2data-belts.json D2R 3.0 mirror (Belts.txt is absent from the 1.13 mirror)
  reincarnated-engine/data/kc2/pm4g_consumables.csv  (sha-pinned by counterplay.py)
  reincarnated.simulation.kc2.counterplay.load_kit()  imported, never modified
Writes: potions.json (packet root).

Usage: PYTHONPATH=/Users/admin/Games/reincarnated-engine/src python3 scripts/potions_extract.py
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

PKT = Path(__file__).resolve().parents[1]
CAP = PKT / "captures" / "potions"
COLLAB = Path("/Users/admin/Games/reincarnated-collaboration")
ENGINE = Path("/Users/admin/Games/reincarnated-engine")
RAW = COLLAB / "agentic_orchestration/research/datamine-acquisition/d2/raw"
FPS = 25

# D2 class multipliers, D2MOO D2Common Items.cpp ITEMS_GetBonusLifeBasedOnClass / ...ManaBasedOnClass
LIFE_MULT = {"amazon": 1.5, "paladin": 1.5, "assassin": 1.5, "barbarian": 2.0,
             "sorceress": 1.0, "necromancer": 1.0, "druid": 1.0}
MANA_MULT = {"sorceress": 2.0, "necromancer": 2.0, "druid": 2.0,
             "amazon": 1.5, "paladin": 1.5, "assassin": 1.5, "barbarian": 1.0}
# Arreat Summit items/potions.shtml tables (captured), the independent check of the code multipliers
ARREAT_HEAL = {"hp1": (30, 45, 60), "hp2": (60, 90, 120), "hp3": (100, 150, 200),
               "hp4": (180, 270, 360), "hp5": (320, 480, 640)}       # (Nec/Sor/Dru, Ama/Pal/Ass, Barb)
ARREAT_MANA = {"mp1": (20, 30, 40), "mp2": (40, 60, 80), "mp3": (80, 120, 160),
               "mp4": (150, 225, 300), "mp5": (250, 375, 500)}       # (Barb, Ass/Ama/Pal, Dru/Nec/Sor)
# PureDiablo diablo-2/potions "Fill Rate" column (captured), the independent check of Misc.txt len
PUREDIABLO_FILL_S = {"hp1": 7.68, "hp2": 6.4, "hp3": 6.84, "hp4": 7.68, "hp5": 10.24}
PUREDIABLO_MANA_FILL_S = 5.12
DISPLAY = {"hp1": "Minor Healing Potion", "hp2": "Light Healing Potion", "hp3": "Healing Potion",
           "hp4": "Greater Healing Potion", "hp5": "Super Healing Potion",
           "mp1": "Minor Mana Potion", "mp2": "Light Mana Potion", "mp3": "Mana Potion",
           "mp4": "Greater Mana Potion", "mp5": "Super Mana Potion",
           "rvs": "Rejuvenation Potion", "rvl": "Full Rejuvenation Potion"}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def tsv(p: Path):
    with open(p, encoding="latin-1", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def double_chance_pct(stat: int) -> float:
    """Exact chance from D2MOO SKILLITEM_pSpell03_Potion: rand()%100 < floor(randLimited(stat)/2).

    randLimited(V) is uniform on 0..V-1; P = E[min(floor(r/2), 100)] / 100. Matches Arreat's closed forms.
    """
    if stat <= 0:
        return 0.0
    return 100.0 * sum(min(r // 2, 100) for r in range(stat)) / (stat * 100.0)


def arreat_double_pct(v: int) -> float:
    if v >= 200:
        return 100.0 * (v - 101) / v
    return (v - 2) / 4 if v % 2 == 0 else (v - 1) * (v - 1) / (4 * v)


def main() -> None:
    log = []
    misc = {r["code"]: r for r in tsv(CAP / "Misc.txt")}
    d2 = {"health": [], "mana": [], "rejuvenation": []}
    for code in ("hp1", "hp2", "hp3", "hp4", "hp5"):
        r = misc[code]
        assert r["pSpell"] == "3" and r["stat1"] == "hpregen" and r["state"] == "healthpot", code
        base, ln = int(r["calc1"]), int(r["len"])
        sor = base * LIFE_MULT["sorceress"]
        a = ARREAT_HEAL[code]
        assert (base * 1.0, base * 1.5, base * 2.0) == tuple(float(x) for x in a), (code, a)
        assert abs(ln / FPS - PUREDIABLO_FILL_S[code]) < 1e-9, (code, ln)
        log.append(f"{code}: Misc calc1={base} len={ln} == Arreat {a} and PureDiablo {PUREDIABLO_FILL_S[code]} s: OK")
        d2["health"].append({
            "code": code, "display": DISPLAY[code], "misc_internal_name": r["name"],
            "total_hp_by_class": {c: base * m for c, m in LIFE_MULT.items()},
            "sorceress_total_hp": sor, "duration_frames": ln, "duration_s": ln / FPS,
            "sorceress_hp_per_frame": sor / ln, "sorceress_hp_per_s": sor * FPS / ln,
            "grade": "MODEL-VERIFIED (Misc.txt DATAMINED + D2MOO pSpell03 + Arreat amounts + PureDiablo durations)"})
    for code in ("mp1", "mp2", "mp3", "mp4", "mp5"):
        r = misc[code]
        assert r["pSpell"] == "3" and r["stat1"] == "manarecovery" and r["state"] == "manapot", code
        base, ln = int(r["calc1"]), int(r["len"])
        a = ARREAT_MANA[code]
        assert (base * 1.0, base * 1.5, base * 2.0) == tuple(float(x) for x in a), (code, a)
        assert abs(ln / FPS - PUREDIABLO_MANA_FILL_S) < 1e-9
        log.append(f"{code}: Misc calc1={base} len={ln} == Arreat {a} and PureDiablo 5.12 s: OK")
        sor = base * MANA_MULT["sorceress"]
        d2["mana"].append({
            "code": code, "display": DISPLAY[code], "misc_internal_name": r["name"],
            "total_mana_by_class": {c: base * m for c, m in MANA_MULT.items()},
            "sorceress_total_mana": sor, "duration_frames": ln, "duration_s": ln / FPS,
            "sorceress_mana_per_frame": sor / ln, "sorceress_mana_per_s": sor * FPS / ln,
            "grade": "MODEL-VERIFIED (Misc.txt DATAMINED + D2MOO pSpell03 + Arreat amounts + PureDiablo durations)"})
    for code in ("rvs", "rvl"):
        r = misc[code]
        assert r["pSpell"] == "5" and r["stat1"] == "hitpoints" and r["stat2"] == "mana", code
        d2["rejuvenation"].append({
            "code": code, "display": DISPLAY[code], "pct_max_life": int(r["calc1"]),
            "pct_max_mana": int(r["calc2"]), "delivery": "instant (len empty -> STATLIST_AddUnitStat, clamped to max)",
            "class_modifier": "none (pSpell05 calls no class-bonus function)",
            "double_chance": "none (pSpell05 has no Vitality/Energy roll)",
            "grade": "MODEL-VERIFIED (Misc.txt DATAMINED + D2MOO pSpell05 + Arreat 'Heals 35%/100% Life and Mana, instantly')"})
        log.append(f"{code}: pSpell 5, {r['calc1']}% life / {r['calc2']}% mana, instant: OK")

    dbl = {v: {"code_exact_pct": round(double_chance_pct(v), 4), "arreat_formula_pct": round(arreat_double_pct(v), 4)}
           for v in (10, 50, 100, 150, 200, 250, 300, 400, 500)}
    for v, row in dbl.items():
        assert abs(row["code_exact_pct"] - row["arreat_formula_pct"]) < 1e-9, (v, row)
    log.append("double-heal chance: code-exact == Arreat closed forms (both branches, stat 10..500): OK")

    armor = {r["code"]: r for r in tsv(RAW / "Armor.txt")}
    ulc = armor["ulc"]
    belts = json.loads((CAP / "blizzhackers-d2data-belts.json").read_text())
    btype = ulc["belt"]
    boxes = belts[btype]["numboxes"] if isinstance(belts, dict) else belts[int(btype)]["numboxes"]
    assert int(btype) == 6 and int(boxes) == 16
    log.append("Spiderweb Sash ulc: Armor.txt belt type 6; belts table numboxes 16 (D2R mirror) == Arreat #Boxes 16 == Basin Rows 4: OK")

    # GD: the oracle's own kit, imported read-only
    from reincarnated.simulation.kc2 import counterplay as cp, fixture as fx
    kits = {L.name: cp.load_kit(potion_limb=L) for L in cp.PotionLimb}
    k = kits["I4_EXCURSION_MAX"]
    hp_max = float(fx.v(fx.MO_PLAYER_HP_MAX))
    inst = k.potion_flat + hp_max * k.potion_pct / 100.0
    hot = hp_max * k.potion_pct_slow / 100.0
    gd = {
        "record": cp.POTION, "hot_modifier_record": cp.POTION_HOT, "display": "Tonic of Mending (+ Sansochromatis HoT modifier, allocated rank 1)",
        "heal_flat": k.potion_flat, "heal_pct_instant": k.potion_pct, "heal_pct_over_time": k.potion_pct_slow,
        "cooldown_s": k.potion_cd_s, "charges": k.potion_charges,
        "actuation_threshold_frac_by_limb": {n: kk.potion_threshold_frac for n, kk in kits.items()},
        "default_limb": "I4_EXCURSION_MAX (load_kit default)",
        "player_hp_max": hp_max,
        "instant_hp": inst, "instant_frac_of_max": inst / hp_max,
        "over_time_hp": hot, "over_time_duration_s_oracle": k.potion_cd_s,
        "over_time_hp_per_s_oracle": hot / k.potion_cd_s,
        "over_time_duration_grade": "MEASURED-ABSENT in the substrate; the oracle spreads it over the 12.0 s cooldown (C-I4-5, its LOWER limb)",
        "total_per_drink_hp": inst + hot, "total_frac_of_max": (inst + hot) / hp_max,
        "healing_increase_note": "Resilience characterHealIncreasePercent +24 % multiplies the potion and ADCtH, not regen (sustain_procs ROW_DISPOSITIONS resilience; D-6)",
        "control_state_gate": "RequestUseItem decoded PERMITTED in every control state; not gated (counterplay docstring, S-5)",
        "use_limit": "cooldown only; the oracle keeps no inventory count",
        "instant_cast_field": "True (pm4g_consumables.csv instant_cast for defaulthealthpotion.dbr)",
        "grade": "MEASURED per the oracle (pm4g_consumables.csv rows, sha pinned in counterplay.py)",
    }
    d2_super_sorc = 320.0
    out = {
        "_what": "C-13 census row 21 (KP-423): D2 LoD 1.13 potion laws + GD Warlord potion as the KC2 oracle carries it",
        "_law": "LoD 1.13 data (fabd/diablo2 @ 45112569deb9384738ccafe5c24ebbb71f41c7c9); code D2MOO @ 5596f5cb (1.10f reconstruction)",
        "d2": {
            **d2,
            "double_fill": {"law": "per drink: chance = P(rand()%100 < floor(randLimited(Vit)/2)) for health (Energy for mana); success doubles the amount; rejuvs excluded",
                            "uses_stat": "current total Vitality / Energy (STAT_VITALITY / STAT_ENERGY incl. items)",
                            "table_pct": dbl,
                            "grade": "MODEL-VERIFIED (D2MOO pSpell03 + Arreat basics/characters.shtml formulas)"},
            "delivery": {
                "frames": "25 fps; total amount <<8 (1/256 points) is laid on a timed stat list (state healthpot/manapot) as a per-frame regen of total/len",
                "second_potion": "same state: duration EXTENDS (remaining + len) and the per-frame rate is recomputed as (new total + remaining old) / (remaining + len). Totals add; the rate does not stack. A smaller potion on top of a larger one SLOWS the fill",
                "second_potion_grade": "MODEL-VERIFIED (D2MOO pSpell03 + Arreat 'will not cause you to replenish life any faster' + PureDiablo averaging example)",
                "cast_interaction": "drinking is an item-use request with no player-mode gate and no animation in the code path (ItemMode.cpp sub_6FC49220); it neither interrupts nor delays a cast",
                "cast_interaction_grade": "INFERRED (single code source, by absence; no community statement found)",
                "hit_cancels": "no: the potion stat list is removed only at its expiry frame; nothing in the damage path (SUnitDmg.cpp) removes healthpot/manapot",
                "hit_cancels_grade": "INFERRED (code by absence; Arreat's advice to 'run away long enough for them to heal fully' is consistent, not explicit)",
                "cooldown": "none in code; the limit is the belt and inventory",
                "cooldown_grade": "INFERRED (no use-delay in pSpell03 or the belt-use path)",
            },
            "belt": {
                "kit_belt": "Arachnid Mesh (unique), base Spiderweb Sash `ulc`",
                "armor_txt_belt_type": int(btype), "numboxes": int(boxes), "rows": int(boxes) // 4, "columns": 4,
                "rules": ["only the bottom row (slots 0-3) is hotkeyed (1-4)",
                          "drinking a bottom-row potion drops the potions above it down that column (ItemMode.cpp sub_6FC49140; PureDiablo 'like a vending machine')",
                          "picking up a potion auto-belts it into a column holding the same potion type, else into an empty bottom slot if Misc.txt autobelt=1 (D2Inventory.cpp INVENTORY_GetFreeBeltSlot; PureDiablo 'Picking up potions restocks the belt')",
                          "inventory potions do NOT refill the belt automatically; shift-click moves them (Arreat potions page)"],
                "capacity_sorc": "16 belt potions, plus any carried in inventory (no hotkey)",
                "grade": "MODEL-VERIFIED for 16 boxes (Armor.txt belt=6 DATAMINED; Arreat elite belts #Boxes 16; Basin Rows 4; numboxes 16 from a D2R 3.0 mirror because Belts.txt is absent from the 1.13 mirror)",
            },
            "class_modifiers_sorceress": {"health": 1.0, "mana": 2.0,
                                          "all_classes_life": LIFE_MULT, "all_classes_mana": MANA_MULT,
                                          "grade": "MODEL-VERIFIED (D2MOO D2Common Items.cpp + Arreat potions tables + Basin Consumable + PureDiablo tables)"},
        },
        "gd": gd,
        "comparison_rows": [
            {"row": "amount", "d2_sorc": f"Super Healing {d2_super_sorc:.0f} HP flat (x2 on a Vitality roll); Rejuv 35 % / Full Rejuv 100 % of max life and mana",
             "gd_warlord": f"{k.potion_flat:.0f} flat + {k.potion_pct:.0f} % max HP instant ({inst:.1f} of {hp_max:.0f}) + {k.potion_pct_slow:.0f} % max HP over time ({hot:.1f})"},
            {"row": "delivery", "d2_sorc": "health/mana: over time (per-frame regen); rejuv: instant",
             "gd_warlord": "instant portion + over-time portion"},
            {"row": "duration", "d2_sorc": "health 6.4-10.24 s by tier (Super 256 frames = 10.24 s); mana 5.12 s; rejuv 0",
             "gd_warlord": "instant: 0; over-time: duration MEASURED-ABSENT, oracle spreads over 12.0 s"},
            {"row": "cooldown / limit", "d2_sorc": "no cooldown; 16 belt slots (4 hotkeyed) + inventory",
             "gd_warlord": f"{k.potion_cd_s:.1f} s cooldown, {k.potion_charges} charge; unlimited uses in the oracle"},
            {"row": "stacking", "d2_sorc": "same-type drinks add totals and extend duration; rate never rises",
             "gd_warlord": "cannot overlap: cooldown 12 s equals the oracle's over-time window"},
            {"row": "interruption", "d2_sorc": "not interrupted by hits; drinking does not interrupt a cast (both INFERRED)",
             "gd_warlord": "RequestUseItem permitted in every control state; instant_cast True"},
            {"row": "actuation", "d2_sorc": "player choice (no data)",
             "gd_warlord": "oracle threshold theta: " + ", ".join(f"{n}={kk.potion_threshold_frac:.4f}" for n, kk in kits.items())},
        ],
        "sources_sha256": {
            "captures/potions/Misc.txt": sha(CAP / "Misc.txt"),
            "raw/Armor.txt": sha(RAW / "Armor.txt"),
            "captures/potions/blizzhackers-d2data-belts.json": sha(CAP / "blizzhackers-d2data-belts.json"),
            "engine data/kc2/pm4g_consumables.csv": sha(ENGINE / "data/kc2/pm4g_consumables.csv"),
            "engine simulation/kc2/counterplay.py": sha(ENGINE / "src/reincarnated/simulation/kc2/counterplay.py"),
            "engine simulation/kc2/sustain_procs.py": sha(ENGINE / "src/reincarnated/simulation/kc2/sustain_procs.py"),
        },
        "verification_log": log,
    }
    (PKT / "potions.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print("\n".join(log))
    print("wrote", PKT / "potions.json")


if __name__ == "__main__":
    main()
