#!/usr/bin/env python3
"""C-14 — the Sorceress build file: the Maxroll guide's 'Standard' variant (d2planner profile gca1a0l6 set 2),
resolved in LoD 1.13 and turned into her sheet. Read-only.

Inputs: captures/maxroll-d2planner-gca1a0l6.data.json (verbatim planner data), 1.13 tables in
agentic_orchestration/research/datamine-acquisition/d2/raw/ (CharStats, Armor, UniqueItems, Runes, Gems, Properties).

Laws (cited in README § 3): life/mana = J4a F12 pattern with Sorceress CharStats (40 +1/clvl +2/Vit; 35 +2/clvl +2/Energy),
BO = J4a F03 (op 11 on base + flat life, not on item Vitality); defence = item def (ED applies to that item; ac% on a
weapon with no armour class is inert: ItemStatCost op 13) + Dex/4; block = Units.cpp UNITS_GetBlockRate (expansion);
resists: Hell -100, +30 Anya (KP-428), cap 75; FCR/FHR breakpoints: animation packet + J4b.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

PKT = Path(__file__).resolve().parents[1]
RAW = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/datamine-acquisition/d2/raw")
PLAN = PKT / "captures" / "maxroll-d2planner-gca1a0l6.data.json"

SORC_FHR = [(0, 15), (5, 14), (9, 13), (14, 12), (20, 11), (30, 10), (42, 9), (60, 8), (86, 7), (142, 6), (280, 5)]
SORC_FCR = [(0, 13), (9, 12), (20, 11), (37, 10), (63, 9), (105, 8), (200, 7)]


def bp(table, v):
    out = table[0][1]
    for th, fr in table:
        if v >= th:
            out = fr
    return out


def rd(n):
    with open(RAW / n, encoding="latin-1", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def sheet(with_charms: bool, bo_slvl: int | None, plan, clvl=99):
    cs = {r["class"]: r for r in rd("CharStats.txt")}["Sorceress"]
    arm = {r["code"]: r for r in rd("Armor.txt")}
    p = plan["profiles"][1]                                   # 'Standard'
    assert p["name"] == "Standard" and p["level"] == clvl
    alloc = p["stats"]                                        # str 74, vit 431 (points added)
    base = {"str": int(cs["str"]), "dex": int(cs["dex"]), "int": int(cs["int"]), "vit": int(cs["vit"])}
    # item attribute contributions (1.13 rows; max rolls as the planner pins them)
    gear_attr = {"str": 20 + 2 + 10, "dex": 2, "int": 20 + 2, "vit": 22 + 20 + 2 + 10}   # CoH, Shako, WarTrav / Oculus, Shako / Spirit, Oculus, Shako, WarTrav
    charm_attr = {"str": 40, "dex": 40, "int": 40, "vit": 40}                          # Annihilus 20 + Torch 20 each
    item = {k: gear_attr[k] + (charm_attr[k] if with_charms else 0) for k in gear_attr}
    tot = {k: base[k] + alloc.get(k, 0) + item[k] for k in base}
    flat_life = (12 * clvl) // 8 + (7 * 45 if with_charms else 0)        # Shako hp/lvl; 7 GC x 45 life
    base_life = 40 + (clvl - 1) * int(cs["LifePerLevel"]) // 4 + (base["vit"] + alloc["vit"] - base["vit"]) * int(cs["LifePerVitality"]) // 4
    bo_pct = 0 if bo_slvl is None else 35 + 3 * (bo_slvl - 1)
    life = (base_life + flat_life) * (100 + bo_pct) // 100 + item["vit"] * int(cs["LifePerVitality"]) // 4
    flat_mana = 112 + (12 * clvl) // 8                                    # Spirit max mana; Shako mana/lvl
    base_mana = 35 + (clvl - 1) * int(cs["ManaPerLevel"]) // 4 + (base["int"] + alloc.get("int", 0) - base["int"]) * int(cs["ManaPerMagic"]) // 4
    mana = (base_mana + flat_mana) * (100 + 5 + bo_pct) // 100 + item["int"] * int(cs["ManaPerMagic"]) // 4
    # defence (planner-pinned bases; ED per item)
    d_items = {"Harlequin Crest (Shako 141)": 141, "Spirit Monarch (148, no ED)": 148,
               "Chains of Honor (superior Dusk Shroud 468 x1.85)": 468 * 185 // 100,
               "Magefist (12 x1.30 + 10)": 12 * 130 // 100 + 10, "Arachnid Mesh (63 x2.20)": 63 * 220 // 100,
               "War Traveler (48 x2.90)": 48 * 290 // 100}
    defence = sum(d_items.values()) + tot["dex"] // 4
    blk_base = int(cs["BlockFactor"]) + int(arm["uit"]["block"])
    block = max(0, min(75, blk_base * (tot["dex"] - 15) // (2 * clvl)))
    res_gear = {"fire": 20 + 65, "cold": 20 + 65 + 35, "light": 20 + 65 + 35, "poison": 20 + 65 + 35}
    res_charm = 6 * 5 + 5 + 20 + 20                                       # 7 small 5@, Annihilus 20, Torch 20
    resists = {k: min(75, v + (res_charm if with_charms else 0) - 100 + 30) for k, v in res_gear.items()}
    resists_raw = {k: v + (res_charm if with_charms else 0) - 100 + 30 for k, v in res_gear.items()}
    fcr = 30 + 35 + 20 + 20
    fhr = 55 + (5 if with_charms else 0)
    allsk = 2 + 2 + 2 + 1 + (1 if with_charms else 0)                    # Shako, CoH, Spirit, Arachnid, Annihilus
    sorcsk = 3 + (3 if with_charms else 0)                               # Oculus, Torch
    firesk = 1 + 3 + (7 if with_charms else 0)                           # Magefist, amulet, 7 GC
    plus_fire = allsk + sorcsk + firesk
    hard = {"Fire Ball": 20, "Meteor": 20, "Fire Mastery": 20, "Fire Bolt": 20, "Inferno": 20, "Warmth": 1, "Enchant": 3,
            "Frozen Armor": 1}
    slvl = {k: v + plus_fire if k not in ("Frozen Armor",) else v + allsk + sorcsk for k, v in hard.items()}
    slvl["Warmth"] = 1 + plus_fire
    mf = 50 + 50 + 25 + 30 + 25 + 50 + 40 + 40 + 35 + ((6 * 7 + 40) if with_charms else 0)
    return {"with_charms": with_charms, "bo_slvl": bo_slvl, "bo_pct": bo_pct, "clvl": clvl,
            "attributes_total": tot, "attributes_from_items": item, "str_requirement_monarch": int(arm["uit"]["reqstr"]),
            "str_requirement_met": tot["str"] >= int(arm["uit"]["reqstr"]),
            "life": life, "mana": mana, "defence_items": d_items, "defence": defence, "defence_vs_missile": defence + 250,
            "block_pct": block, "block_pct_running": block // 3, "resists_after_hell_anya_capped": resists,
            "resists_uncapped": resists_raw, "fcr": fcr, "fcr_frames": bp(SORC_FCR, fcr), "fhr": fhr,
            "fhr_frames": bp(SORC_FHR, fhr), "fbr": 0, "fbr_frames": 9, "dr_pct": 18, "magic_absorb_flat": 8,
            "plus_skills": {"all": allsk, "sorceress": sorcsk, "fire_tree": firesk, "to_fire_skills_total": plus_fire},
            "slvl": slvl, "mf_pct": mf}


def main(out: Path):
    plan = json.loads(PLAN.read_text())
    # BO level: switch CTA (+6 BO, +1 all) + switch Spirit (+2) + Shako 2 + CoH 2 + Arachnid 1 + Annihilus 1 (charms)
    bo_charms = 6 + 1 + 2 + 2 + 2 + 1 + 1
    bo_nocharm = bo_charms - 1
    res = {
        "variant": "Standard (guide tab 'Standard' = d2planner gca1a0l6 set 2)",
        "bo_slvl_law": "CTA oskill BO 6 + all-skills worn while the swap is active (CTA 1, switch Spirit 2, Shako 2, CoH 2, Arachnid 1, Annihilus 1); +1 more if Battle Command is cast first (guide: 'cast Battle Command 2 times, Battle Orders')",
        "bo_slvl": {"with_charms": bo_charms, "with_charms_after_BC": bo_charms + 1, "no_charms": bo_nocharm,
                    "no_charms_after_BC": bo_nocharm + 1, "planner_own_figure": 14},
        "sheets": {
            "charms_noBO": sheet(True, None, plan),
            "charms_BO": sheet(True, bo_charms + 1, plan),
            "nocharms_noBO": sheet(False, None, plan),
            "nocharms_BO": sheet(False, bo_nocharm + 1, plan),
        },
    }
    out.write_text(json.dumps(res, indent=1))
    for k, s in res["sheets"].items():
        print(k, "BO", s["bo_slvl"], f"+{s['bo_pct']}%", "| life", s["life"], "mana", s["mana"], "def", s["defence"], "/", s["defence_vs_missile"],
              "block", s["block_pct"], "res", s["resists_after_hell_anya_capped"], "raw", s["resists_uncapped"],
              "FCR", s["fcr"], s["fcr_frames"], "FHR", s["fhr"], s["fhr_frames"], "str ok", s["str_requirement_met"], s["attributes_total"],
              "slvl FB", s["slvl"]["Fire Ball"], "Warmth", s["slvl"]["Warmth"], "+fire", s["plus_skills"], "MF", s["mf_pct"])


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else PKT / "sorc_build_sheet.json")
