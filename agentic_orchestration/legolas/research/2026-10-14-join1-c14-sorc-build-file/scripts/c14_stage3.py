#!/usr/bin/env python3
"""C-14 stage 3 (KP-437; derived from the stage-2 script) — PRIMARY tables WITH Frozen Armor at slvl 16 (BC always on): (1) re-run the C-13 stage-6/7 hit-chance tables against the BUILD-FILE sheet (Def 1,472 melee /
1,722 missile, clvl 99), plus a Frozen-Armor-on sensitivity; (2) BO/BC slvl and durations; (3) Frozen Armor law values;
(4) Oculus / Hellfire Torch proc data. Read-only.

Inputs: ../2026-10-14-join1-c13-enemy-anchor/{d2_hit_chance_r1.json, d2_unique_ar_r1.json} (per-attack AR rows, unchanged
inputs), raw/ Skills.txt, UniqueItems.txt, MonStats/MonLvl (via the C-13 rows). Laws: README § 6 (stage 2).
"""
from __future__ import annotations

import csv
import json
import statistics
import sys
from pathlib import Path

PKT = Path(__file__).resolve().parents[1]
C13 = PKT.parent / "2026-10-14-join1-c13-enemy-anchor"
RAW = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/datamine-acquisition/d2/raw")
CLVL = 99
DEF_M, DEF_MS = 1472, 1722           # build file (sorc_build_sheet.json, charms; BO does not change defence)
FA_SLVL = 16                         # 1 hard + 8 all + 6 sorc + 1 Battle Command (KP-437: BC and FA always on)


def rd(n):
    with open(RAW / n, encoding="latin-1", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def cth(ar, d, alvl, dlvl=CLVL):
    if not ar or ar <= 0:
        return None
    return max(5, min(95, 2 * alvl * (100 * ar // (ar + d)) // (alvl + dlvl)))


def q(v):
    v = sorted(x for x in v if x is not None)
    if not v:
        return None
    if len(v) == 1:
        return {"n": 1, "median": v[0], "p25": v[0], "p75": v[0], "min": v[0], "max": v[0]}
    qs = statistics.quantiles(v, n=4, method="inclusive")
    return {"n": len(v), "median": statistics.median(v), "p25": qs[0], "p75": qs[2], "min": v[0], "max": v[-1]}


def wq(pairs):
    rep = []
    for v, w in pairs:
        if v is not None:
            rep += [v] * int(w)
    return q(rep)


def main(out: Path):
    sk = {r["Id"]: r for r in rd("Skills.txt")}
    fa = sk["40"]
    p = {k: int(fa[f"Param{k}"]) for k in range(1, 9) if fa[f"Param{k}"]}
    fa_def_pct = p[1] + (FA_SLVL - 1) * p[2]                    # ln12
    fa_dur_frames = p[3] + (FA_SLVL - 1) * p[4]                 # ln34 (+ synergy blvl x par7 = 0)
    fa_frz_frames = p[5] + (FA_SLVL - 1) * p[6]                 # calc1 = ln56 x (100 + synergy x par8)/100 = ln56
    defs = {"PRIMARY_buildfile_FrozenArmor16": (DEF_M * (100 + fa_def_pct) // 100, DEF_M * (100 + fa_def_pct) // 100 + 250),
            "sens_no_FrozenArmor": (DEF_M, DEF_MS)}
    hc = json.loads((C13 / "d2_hit_chance_r1.json").read_text())
    ua = json.loads((C13 / "d2_unique_ar_r1.json").read_text())
    tables = {}
    for dk, (dm, dms) in defs.items():
        rows = []
        for r in hc["rows"]:
            per = []
            for a in r["attacks"]:
                if a["role"] == "caster":
                    per.append({"slot": a["slot"], "role": "caster", "ar": None, "dmg_mid": a["dmg_mid"], "hit": 100, "hit_champ": 100})
                    continue
                d = dms if a["role"] == "ranged_physical" else dm
                per.append({"slot": a["slot"], "role": a["role"], "ar": a["ar"], "dmg_mid": a["dmg_mid"],
                            "hit": cth(a["ar"], d, 85), "hit_champ": cth(a["ar"] * 149 // 100, d, 87)})
            best = max(per, key=lambda x: x["dmg_mid"])
            rows.append({"id": r["id"], "slot_weight": r["slot_weight"], "type_role": best["role"], "best_hit": best["hit"],
                         "best_hit_champ": best["hit_champ"], "attacks": per})
        urows = []
        for x in ua["rows"]:
            d = dms if x["role"] == "ranged_physical" else dm
            urows.append({"id": x["id"], "slot": x["slot"], "role": x["role"],
                          "hit_unique": cth(x["ar_unique"], d, 88), "hit_unique_es": cth(x["ar_unique_extra_strong"], d, 88)})
        ubest = {}
        for x in urows:
            b = ubest.setdefault(x["id"], {"hit_unique": 0, "hit_unique_es": 0, "role": x["role"]})
            b["hit_unique"] = max(b["hit_unique"], x["hit_unique"] or 0)
            b["hit_unique_es"] = max(b["hit_unique_es"], x["hit_unique_es"] or 0)
        named = []
        for s in ua["superuniques_and_bosses"]:
            named.append({"name": s["name"], "level": s["level"], "ar": s.get("ar"),
                          "hit_melee": cth(s.get("ar"), dm, s["level"]), "hit_vs_missile_def": cth(s.get("ar"), dms, s["level"])})
        summ = {}
        for role in ("melee", "ranged_physical", "caster", "all"):
            tr = [x for x in rows if role == "all" or x["type_role"] == role]
            summ[role] = {"n_types": len(tr),
                          "type_best_hit_equal": q([x["best_hit"] for x in tr]),
                          "type_best_hit_slot": wq([(x["best_hit"], x["slot_weight"]) for x in tr]),
                          "type_best_hit_champion_equal": q([x["best_hit_champ"] for x in tr])}
        tables[dk] = {"defence_melee": dm, "defence_missile": dms, "dlvl": CLVL, "normal_and_champion": summ,
                      "unique_type_best": {"no_ES": q([b["hit_unique"] for b in ubest.values()]),
                                           "ES": q([b["hit_unique_es"] for b in ubest.values()]),
                                           "melee_no_ES": q([b["hit_unique"] for b in ubest.values() if b["role"] == "melee"])},
                      "named": named, "rows": rows, "unique_rows": urows}
    # (2) BO / BC
    swap_items = {"Call to Arms (switch weapon)": {"all_skills": 1, "oskill_BO": 6, "oskill_BC": 6},
                  "Spirit Monarch (switch shield)": {"all_skills": 2},
                  "Harlequin Crest": {"all_skills": 2}, "Chains of Honor": {"all_skills": 2},
                  "Arachnid Mesh": {"all_skills": 1}, "Annihilus (charm)": {"all_skills": 1},
                  "not applying: Magefist (+1 fire), amulet (+3 fire), 7 GC (+1 fire), Hellfire Torch (+3 sorc), Oculus (main hand, swapped out)": {}}
    allsk = sum(v.get("all_skills", 0) for v in swap_items.values())
    bo_noBC = 6 + allsk
    bo_BC = bo_noBC + 1
    bc_first = 6 + allsk
    bc_second = bc_first + 1
    bo = sk["149"]; bc = sk["155"]
    dur = lambda base, step, lvl: int(base) + int(step) * (lvl - 1)
    bo_block = {
        "swap_items_plus_skills": swap_items, "all_skills_on_swap": allsk,
        "BO_slvl_without_BC": bo_noBC, "BO_slvl_after_BC": bo_BC,
        "BO_pct_without_BC": 35 + 3 * (bo_noBC - 1), "BO_pct_after_BC": 35 + 3 * (bo_BC - 1),
        "BO_duration_s_without_BC": dur(bo["Param1"], bo["Param2"], bo_noBC) / 25,
        "BO_duration_s_after_BC": dur(bo["Param1"], bo["Param2"], bo_BC) / 25,
        "BO_synergy_term": "(Shout.blvl + Battle Command.blvl) x 125 frames = 0: blvl counts hard points, and the Sorceress has none",
        "BC_slvl_first_cast": bc_first, "BC_slvl_second_cast": bc_second,
        "BC_duration_s_second_cast": dur(bc["Param1"], bc["Param2"], bc_second) / 25,
        "planner_figure": "14 / +74 %: equals 6 + 8, i.e. the planner omits ONE +1 source (Annihilus or one of the +2s counted as +1) — not reproducible from its data",
    }
    fa_block = {"slvl": FA_SLVL, "slvl_note": "1 hard + 8 all-skills + 6 Sorceress skills (Oculus 3, Torch 3) + 1 Battle Command (always on, KP-437)",
                "defence_pct": fa_def_pct, "duration_frames": fa_dur_frames, "duration_s": fa_dur_frames / 25,
                "freeze_length_frames_base": fa_frz_frames, "freeze_length_s_base": fa_frz_frames / 25,
                "freeze_law": "on damagedinmelee with physical damage > 0 (D2MOO SkillSor.cpp EventFunc02_FrozenArmor), apply freeze length = "
                              "30 + 3x(slvl-1) frames (calc1 = ln56, synergy 0). Freeze length FREEZES normal and minion monsters and only CHILLS "
                              "champions, uniques, superuniques and bosses (Basin Freeze length; C-13 KP-426 laws); length x (100 - target cold res)/100, "
                              "then /4 in Hell (DifficultyLevels MonsterFreezeDivisor 4); cold-immune targets are unaffected"}
    for res in (0, 33, 50):
        fa_block[f"freeze_s_vs_normal_Hell_res{res}"] = round(fa_frz_frames * (100 - res) / 100 / 4 / 25, 3)
    procs = {
        "Oculus": {"property": "gethit-skill (UniqueItems par 54 min 25 max 1)", "skill": "Teleport (Skills Id 54)", "chance_pct": 25, "level": 1,
                   "trigger": "When Struck: hit by melee, or by a missile applying weapon/monster damage (NOT by missiles that apply only their own or skill damage) — Basin When Struck",
                   "effect": "Teleport cast with the user as caster and no player-chosen target (Basin lists it as cast 'on the user'); the destination comes from the skill's target resolution (D2MOO SrvDo027 uses the target XY) — the destination rule for an untargeted cast is UNVERIFIED here"},
        "Hellfire Torch": {"property": "hit-skill (UniqueItems par 197 min 5 max 10)", "skill": "DiabWall (Skills Id 197) = Diablo's Firestorm", "chance_pct": 5, "level": 10,
                           "trigger": "On Striking: only a WEAPON attack that is not missed/blocked/dodged triggers it (Basin On Striking)",
                           "effect_for_this_kit": "Fire Ball / Meteor are spells, not weapon attacks, so the Torch Firestorm effectively NEVER fires for this kit (INFERRED from the trigger law)"},
    }
    doc = {"law": "LoD 1.13, Hell, players-1; build-file sheet (KP-436: Standard, BO always on, mercs out)",
           "supersedes": "C-13 README § 13 (stage 6) and § 14.2 (stage 7) NO-DEX hit tables",
           "grades": {"hit chance": "INFERRED (computed) through MODEL-VERIFIED laws on DATAMINED AR",
                      "BO/BC slvl": "INFERRED (oskill + all-skills law: Basin Oskill; CTA Runes.txt)",
                      "BO/BC/FA durations and FA values": "DATAMINED (Skills.txt params) via MODEL-VERIFIED calc forms",
                      "freeze/chill rule": "MODEL-VERIFIED (D2MOO event + Basin)", "procs": "DATAMINED (UniqueItems) + SECONDARY (Basin triggers)"},
           "hit_tables": tables, "battle_orders": bo_block, "frozen_armor": fa_block, "procs": procs}
    out.write_text(json.dumps(doc, indent=1))
    for dk, t in tables.items():
        s = t["normal_and_champion"]
        print(dk, t["defence_melee"], t["defence_missile"])
        for role in s:
            e = s[role]["type_best_hit_equal"]; c = s[role]["type_best_hit_champion_equal"]
            print("  ", role, s[role]["n_types"], "normal", e and (e["median"], e["p25"], e["p75"], e["min"], e["max"]),
                  "slot", s[role]["type_best_hit_slot"] and s[role]["type_best_hit_slot"]["median"], "champ", c and (c["median"], c["p25"], c["p75"]))
        u = t["unique_type_best"]
        print("   unique", (u["no_ES"]["median"], u["no_ES"]["p25"], u["no_ES"]["p75"], u["no_ES"]["min"], u["no_ES"]["max"]),
              "ES", (u["ES"]["median"], u["ES"]["p25"], u["ES"]["p75"], u["ES"]["min"], u["ES"]["max"]))
        for n in t["named"]:
            print("   ", n)
    print(json.dumps(bo_block, indent=0)[:900])
    print({k: v for k, v in fa_block.items() if k != "freeze_law"})


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else PKT / "c14_stage3.json")
