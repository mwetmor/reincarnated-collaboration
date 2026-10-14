#!/usr/bin/env python3
"""C-13 — (a) the Sorceress's D2 defensive sheet at clvl 90 (LoD 1.13); (b) the GD/D2 enemy ratio table;
(c) the yard->metre anchor set. Read-only. Inputs: d2_enemy_quantities.json, gd_enemy_quantities.json (this packet),
the D2 1.13 txt tables (raw/), reincarnated-engine/data/kc2/pm4o_oa_da.csv (read-only).

Every law used here is cited in README §§ 2, 5, 6, 7 with >= 2 sources.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
import sys
from pathlib import Path

PKT = Path(__file__).resolve().parents[1]
RAW = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/datamine-acquisition/d2/raw")
PM4O = Path("/Users/admin/Games/reincarnated-engine/data/kc2/pm4o_oa_da.csv")


def rd(name):
    with open(RAW / name, encoding="latin-1", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def wquant(pairs, qs=(0.25, 0.5, 0.75)):
    pairs = sorted((v, w) for v, w in pairs if v is not None and w > 0)
    tot = sum(w for _, w in pairs)
    out, acc, k = [], 0.0, 0
    for q in qs:
        target = q * tot
        acc = 0.0
        for v, w in pairs:
            acc += w
            if acc >= target - 1e-9:
                out.append(v)
                break
    return {"p25": out[0], "median": out[1], "p75": out[2], "min": pairs[0][0], "max": pairs[-1][0],
            "weight_total": tot, "n": len(pairs)}


# ------------------------------------------------------------------------------------------------
# (a) Sorceress sheet
# ------------------------------------------------------------------------------------------------
def sorc_sheet():
    cs = {r["class"]: r for r in rd("CharStats.txt")}["Sorceress"]
    arm = {r["code"]: r for r in rd("Armor.txt")}
    base = {k: int(cs[k]) for k in ("str", "dex", "int", "vit")}
    clvl = 90
    pts_levels = (clvl - 1) * int(cs["StatPerLevel"])           # 445
    pts_quest = 15                                               # Lam Esen x3 difficulties (5 each) — ASSUMED done
    block_factor = int(cs["BlockFactor"])                        # 20
    monarch = arm["uit"]
    shield_block = int(monarch["block"])                         # 22
    item_attr = {"str": 20 + 5 + 2, "dex": 5 + 2, "vit": 22 + 5 + 2}   # CoH / Mara / Shako ; Spirit vit 22
    str_need = int(monarch["reqstr"])                            # 156 (Monarch); Archon Plate 103, Shako 50
    str_spend = max(0, str_need - item_attr["str"] - base["str"])
    blk_base = block_factor + shield_block                       # no +block on Spirit/any pinned item

    def block_pct(dex_total):
        v = blk_base * (dex_total - 15) // (2 * clvl)
        return max(0, min(75, v))

    dex_for_max = 15 + math.ceil(75 * 2 * clvl / blk_base)
    profiles = {}
    for name, dex_spend in (("MAXBLOCK", max(0, dex_for_max - item_attr["dex"] - base["dex"])), ("NODEX", 0)):
        for quest in (True, False):
            pts = pts_levels + (pts_quest if quest else 0)
            vit_spend = pts - str_spend - dex_spend
            dex_t = base["dex"] + dex_spend + item_attr["dex"]
            vit_t = base["vit"] + vit_spend + item_attr["vit"]
            life = 40 + (clvl - 1) * int(cs["LifePerLevel"]) // 4 + (vit_t - base["vit"]) * int(cs["LifePerVitality"]) // 4 \
                + (12 * clvl) // 8                               # Harlequin hp/lvl param 12 = 1.5/clvl
            dex_def = dex_t // 4

            def rng(lo, hi, ed_lo=0, ed_hi=0, flat=0):
                return (lo * (100 + ed_lo) // 100 + flat, hi * (100 + ed_hi) // 100 + flat)
            items = {
                "Spirit Monarch (uit, no ED)": rng(int(monarch["minac"]), int(monarch["maxac"])),
                "Harlequin Crest (uap, no ED)": rng(int(arm["uap"]["minac"]), int(arm["uap"]["maxac"])),
                "Magefist (tgl, +20-30% ED, +10)": rng(int(arm["tgl"]["minac"]), int(arm["tgl"]["maxac"]), 20, 30, 10),
                "Arachnid Mesh (ulc, +90-120% ED)": rng(int(arm["ulc"]["minac"]), int(arm["ulc"]["maxac"]), 90, 120),
                "Chains of Honor on Archon Plate (utp, +70% ED) [BASE UNPINNED: reference choice]": rng(int(arm["utp"]["minac"]), int(arm["utp"]["maxac"]), 70, 70),
            }
            d_lo = sum(v[0] for v in items.values()) + dex_def
            d_hi = sum(v[1] for v in items.values()) + dex_def
            key = f"{name}_{'quests' if quest else 'noquests'}"
            profiles[key] = {
                "stat_points": pts, "str_spend": str_spend, "dex_spend": dex_spend, "vit_spend": vit_spend,
                "totals": {"str": base["str"] + str_spend + item_attr["str"], "dex": dex_t, "vit": vit_t},
                "life": life, "life_note": "no Battle Orders/CTA, no +life charms (unpinned)",
                "defense_items": items, "defense_from_dex": dex_def,
                "defense_total_range": [d_lo, d_hi], "defense_vs_missile_extra": 250,
                "block_pct_stationary_or_walking": block_pct(dex_t),
                "block_pct_running": block_pct(dex_t) // 3,
            }
    res_lo = {"fire": 65 + 20, "cold": 65 + 20 + 35, "light": 65 + 20 + 35, "poison": 65 + 20 + 35}
    res_hi = {"fire": 65 + 30, "cold": 65 + 30 + 35, "light": 65 + 30 + 35, "poison": 65 + 30 + 35}
    resists = {}
    for anya in (0, 30):
        resists[f"anya_{anya}"] = {k: [min(75, res_lo[k] - 100 + anya), min(75, res_hi[k] - 100 + anya)] for k in res_lo}
    return {
        "clvl": clvl,
        "gear_resolution": "kit-record items resolved in 1.13 tables (J4b § 3): Eschuta's Temper | Spirit Monarch | Chains of Honor | Harlequin Crest (Flickering Flame has no 1.13 row) | Magefist | Arachnid Mesh | Mara's Kaleidoscope",
        "resist_sources": "CoH res-all 50 + Um rune (armor) 15 = 65; Mara 20-30; Spirit runes in a shield: Tal res-pois 35, Thul res-cold 35, Ort res-ltng 35 (Amn thorns 14) — NO fire res on Spirit",
        "hell_resist_penalty": -100, "resist_cap": 75,
        "resists_after_hell_penalty": resists,
        "damage_reduced_pct": 18, "dr_sources": "Harlequin red-dmg% 10 + Ber rune (armor) red-dmg% 8; player DR% cap 50",
        "magic_absorb_flat": [3, 8],
        "block_law": {"formula": "min(75, (BlockFactor + shield block + item block) x (Dex - 15) / (2 x clvl)); /3 while running (after the cap)",
                      "BlockFactor_sorceress": block_factor, "monarch_block": shield_block, "block_base": blk_base,
                      "dex_for_75pct_at_clvl90": dex_for_max},
        "fbr": {"pinned_FBR": 0, "block_anim_ticks_at_FBR0": 9, "seconds": 0.36,
                "law": "ticks = ceil(256*5/floor(256*(50+EFBR)/100) - 1) (animation packet § 3.4)"},
        "profiles": profiles,
        "stat_allocation_rule": "str to Monarch req (156) net of item str; MAXBLOCK = dex to 75% block; NODEX = base dex; remainder to vit; energy base. The kit record pins NO attributes, so both profiles are INFERRED",
    }


def d2_hit_chance(ar, defense, alvl, dlvl):
    if ar + defense <= 0:
        return 95
    f = 100 * ar // (ar + defense)
    return max(5, min(95, 2 * alvl * f // (alvl + dlvl)))


def main(out_dir: Path):
    d2 = json.loads((PKT / "d2_enemy_quantities.json").read_text())
    gd = json.loads((PKT / "gd_enemy_quantities.json").read_text())
    sheet = sorc_sheet()

    # GD role split (BOARD weights = n_actors_this_wave; REF weights = pin counts)
    cells = gd["per_cell"].values()
    def gdq(field, roles, wkey="weight_board_actors"):
        return wquant([(c.get(field), c.get(wkey) or 0) for c in cells if c.get("role") in roles])
    roles = {"trash": {"trash"}, "champion-hero": {"champion-hero"}, "boss+nemesis": {"boss", "nemesis"},
             "all": {"trash", "champion-hero", "boss", "nemesis"}}
    gdsplit = {}
    for wkey in ("weight_board_actors", "weight_ref_bodies"):
        gdsplit[wkey] = {rk: {f: gdq(f, rs, wkey) for f in ("hp_lo", "dmg_folded_basic_hit", "dmg_folded_max_slot",
                                                             "dmg_raw_basic_hit", "OA_best", "DA_best", "armor",
                                                             "swing_period_s")}
                         for rk, rs in roles.items()}
    # GD monster-vs-Warlord hit chance (m2p) from the measured board
    with open(PM4O, newline="") as fh:
        pm4o = [r for r in csv.DictReader(fh) if r["row_kind"] == "monster"]
    m2p_hit = wquant([(float(r["m2p_p_hit_pct"]), float(r["n_actors_this_wave"])) for r in pm4o])
    m2p_pth = wquant([(float(r["m2p_pth_effective"]), float(r["n_actors_this_wave"])) for r in pm4o])

    # D2 anchors (R1 default) and alternates
    ratio = {}
    for rk in ("R1_alvl85_all", "R2_chaos_sanctum", "R3_worldstone_throne", "R4_alvl81plus"):
        R = d2["rules"][rk]
        dn = R["distributions_normal"]
        dc = R["distributions_champion"]
        gb = gdsplit["weight_board_actors"]
        def pr(gdv, d2v):
            return None if not d2v else gdv / d2v
        bosses = [b for b in R["bosses_and_superuniques"] if b.get("hp_mid")]
        ratio[rk] = {
            "HP_trash_vs_normal": {"gd_median": gb["trash"]["hp_lo"]["median"], "d2_median": dn["hp_mid"]["equal"]["median"],
                                   "ratio_median": pr(gb["trash"]["hp_lo"]["median"], dn["hp_mid"]["equal"]["median"]),
                                   "ratio_p25_p75": [pr(gb["trash"]["hp_lo"]["p25"], dn["hp_mid"]["equal"]["p25"]),
                                                     pr(gb["trash"]["hp_lo"]["p75"], dn["hp_mid"]["equal"]["p75"])],
                                   "d2_slot_weighted_median": dn["hp_mid"]["slot"]["median"]},
            "HP_championhero_vs_champion": {"gd_median": gb["champion-hero"]["hp_lo"]["median"], "d2_median": dc["hp_mid"]["median"],
                                            "ratio_median": pr(gb["champion-hero"]["hp_lo"]["median"], dc["hp_mid"]["median"])},
            "HP_boss_vs_boss_superunique": None if not bosses else {
                "gd_median": gb["boss+nemesis"]["hp_lo"]["median"],
                "d2_values": {(b.get("id") or b.get("name")): b.get("hp_mid_with_unique_bonus") or b["hp_mid"] for b in bosses},
                "d2_median": statistics.median([b.get("hp_mid_with_unique_bonus") or b["hp_mid"] for b in bosses]),
                "ratio_median": pr(gb["boss+nemesis"]["hp_lo"]["median"], statistics.median([b.get("hp_mid_with_unique_bonus") or b["hp_mid"] for b in bosses]))},
            "DMG_trash_basic_vs_normal_maxattack": {"gd_median_folded": gb["trash"]["dmg_folded_basic_hit"]["median"],
                                                    "gd_median_raw": gb["trash"]["dmg_raw_basic_hit"]["median"],
                                                    "d2_median": dn["max_attack_total_mid"]["equal"]["median"],
                                                    "ratio_median_folded": pr(gb["trash"]["dmg_folded_basic_hit"]["median"], dn["max_attack_total_mid"]["equal"]["median"]),
                                                    "ratio_median_raw": pr(gb["trash"]["dmg_raw_basic_hit"]["median"], dn["max_attack_total_mid"]["equal"]["median"]),
                                                    "ratio_p25_p75_folded": [pr(gb["trash"]["dmg_folded_basic_hit"]["p25"], dn["max_attack_total_mid"]["equal"]["p25"]),
                                                                             pr(gb["trash"]["dmg_folded_basic_hit"]["p75"], dn["max_attack_total_mid"]["equal"]["p75"])]},
            "AR_vs_OA_RAW_NUMBERS_FLAGGED": {"gd_OA_median_trash": gb["trash"]["OA_best"]["median"],
                                             "d2_AR_median_normal": dn["max_attack_ar"]["equal"]["median"],
                                             "ratio_median": pr(gb["trash"]["OA_best"]["median"], dn["max_attack_ar"]["equal"]["median"])},
            "DEF_vs_DA_RAW_NUMBERS_FLAGGED": {"gd_DA_median_trash": gb["trash"]["DA_best"]["median"],
                                              "d2_def_median_normal": dn["defense"]["equal"]["median"],
                                              "ratio_median": pr(gb["trash"]["DA_best"]["median"], dn["defense"]["equal"]["median"])},
            "RES_fire": {"d2": dn["resists"]["fire"], "gd_note": "GD BOARD/REF fire res: median 0, p75 25, range -20..80, no >= 100 cell (gd_notes.md)"},
        }

    # Hit-chance outcomes (the flagged pairs expressed in each game's own law)
    sp = sheet["profiles"]
    hit = {}
    for pk in ("MAXBLOCK_quests", "NODEX_quests"):
        dlo, dhi = sp[pk]["defense_total_range"]
        dmid = (dlo + dhi) // 2
        r1 = d2["rules"]["R1_alvl85_all"]
        ars = [(r["max_attack_ar"], r["slot_weight"]) for r in r1["rows"] if r["max_attack_ar"]]
        normal = wquant([(d2_hit_chance(a, dmid, 85, 90), w) for a, w in ars])
        champ = wquant([(d2_hit_chance(a * 149 // 100, dmid, 87, 90), w) for a, w in ars])  # AR at +2 lvl not re-looked-up: lower bound
        hit[pk] = {"sorc_defense_mid": dmid, "d2_normal_melee_hit_pct": normal, "d2_champion_melee_hit_pct_lowerbound": champ,
                   "then_block_pct": sp[pk]["block_pct_stationary_or_walking"]}
    hit["gd_monster_vs_warlord"] = {"m2p_p_hit_pct": m2p_hit, "m2p_pth_effective": m2p_pth,
                                    "source": "pm4o_oa_da.csv m2p_* columns (BOARD, body-weighted)"}

    # yard -> metre anchors
    anchors = {
        "literal_yard": {"m_per_yd": 0.9144, "grade": "DEFINITIONAL (label-literal; neither game states it in-world)"},
        "body_radius": {"gd_human_actorRadius_m": [0.38, 0.40], "d2_player_footprint": "COLLISION_UNIT_SIZE_SMALL (1 subtile); 1 subtile = 2/3 yd -> half-width 1/3 yd",
                        "m_per_yd": 0.39 / (1 / 3), "grade": "INFERRED (D2 footprint-as-diameter is an assumption; GD radius DATAMINED pm4_body_radii.csv)"},
        "melee_reach": {"gd_meleeTargetDistance_m": 2.4, "d2_player_melee_reach_subtiles": "weapon melee range + 1 (Units.cpp IsInMeleeRange: range + bonus + 1 >= distance)",
                        "d2_reach_yd_assumed": 2.0, "m_per_yd": 2.4 / 2.0,
                        "grade": "INFERRED (D2 reach in subtiles depends on weapon rangeadder; 3 subtiles = 2 yd assumed for a 1-handed reach)"},
        "run_speed": {"gd_warlord_moving_speed_m_s": 4.55, "d2_base_run_yd_s": 9, "m_per_yd": 4.55 / 9,
                      "grade": "INFERRED (Basin reads CharStats RunVelocity 9 as yd/s; GD figure is the pilot's measured moving speed with gear, not a base)"},
        "sensitivity_set_m_per_yd": [0.67, 0.9144, 1.0, 1.17, 1.2, 1.5],
        "radii_in_metres": {str(k): {"fire_ball_2.667yd": round(8 / 3 * k, 3), "meteor_4yd": round(4 * k, 3),
                                     "ww_search_3.333yd": round(10 / 3 * k, 3)} for k in (0.67, 0.9144, 1.0, 1.17, 1.2, 1.5)},
    }

    (out_dir / "sorc_defense_sheet.json").write_text(json.dumps(sheet, indent=1))
    (out_dir / "ratio_table.json").write_text(json.dumps({
        "gd_role_split": gdsplit, "ratios_gd_over_d2": ratio, "hit_chance_in_each_law": hit,
        "yard_metre_anchors": anchors,
        "inputs_sha256": {"d2_enemy_quantities.json": sha(PKT / "d2_enemy_quantities.json"),
                          "gd_enemy_quantities.json": sha(PKT / "gd_enemy_quantities.json"),
                          "pm4o_oa_da.csv": sha(PM4O)},
    }, indent=1))
    # print headline
    r = ratio["R1_alvl85_all"]
    print("HP trash/normal", round(r["HP_trash_vs_normal"]["ratio_median"], 1), r["HP_trash_vs_normal"]["ratio_p25_p75"])
    print("HP champ", round(r["HP_championhero_vs_champion"]["ratio_median"], 1))
    print("DMG folded", round(r["DMG_trash_basic_vs_normal_maxattack"]["ratio_median_folded"], 1), "raw", round(r["DMG_trash_basic_vs_normal_maxattack"]["ratio_median_raw"], 1))
    print("OA/AR", round(r["AR_vs_OA_RAW_NUMBERS_FLAGGED"]["ratio_median"], 3), "DA/DEF", round(r["DEF_vs_DA_RAW_NUMBERS_FLAGGED"]["ratio_median"], 3))
    for k in ("R2_chaos_sanctum", "R3_worldstone_throne", "R4_alvl81plus"):
        print(k, "HP", round(ratio[k]["HP_trash_vs_normal"]["ratio_median"], 1), "DMG", round(ratio[k]["DMG_trash_basic_vs_normal_maxattack"]["ratio_median_folded"], 1),
              "boss", ratio[k]["HP_boss_vs_boss_superunique"] and round(ratio[k]["HP_boss_vs_boss_superunique"]["ratio_median"], 1))
    for pk, v in sheet["profiles"].items():
        print(pk, "life", v["life"], "def", v["defense_total_range"], "block", v["block_pct_stationary_or_walking"], v["totals"])
    print("res", sheet["resists_after_hell_penalty"])
    for pk in ("MAXBLOCK_quests", "NODEX_quests"):
        print(pk, "D2 hit% normal", hit[pk]["d2_normal_melee_hit_pct"]["median"], "champ>=", hit[pk]["d2_champion_melee_hit_pct_lowerbound"]["median"])
    print("GD m2p hit%", m2p_hit, "gd trash", {f: gdsplit['weight_board_actors']['trash'][f]['median'] for f in ('hp_lo','dmg_folded_basic_hit','OA_best','DA_best','armor','swing_period_s')})


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else PKT)
