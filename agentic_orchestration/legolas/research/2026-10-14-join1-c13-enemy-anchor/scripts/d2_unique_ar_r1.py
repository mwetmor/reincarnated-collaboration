#!/usr/bin/env python3
"""C-13 stage 7 (KP-432) — (1) mean/mean r_DMG for R1-R4; (2) D2 UNIQUE / superunique / boss attack rating for the R1
areas (Hell, players-1) and hit chance vs the NODEX Sorceress (Def 1,203 melee; 1,453 vs missiles), clvl 90.

Read-only. Inputs: d2_hit_chance_r1.json, r_dmg.json, gd_damage_reconcile.json, d2_skill_damage.json, d2_enemy_quantities.json
(this packet); MonStats, MonLvl, MonUMod, DifficultyLevels, SuperUniques (raw/).

Laws:
  U1 unique & minion: monster level +3, and that level selects the MonLvl attack-rating (and damage) row
     (Basin Unique (monster): "Unique and minion level is base monster level +3: this level is used for chance-to-hit ...
     selecting relevant MonLvl values to calculate base attack rating"; D2MOO UMod4_LevelBonus sets STAT_LEVEL+3).
  U2 Extra Strong (if rolled): unique +tohit% = MonUMod[13].constants 100 x ChampionDamageBonus(H) 66/100 = +66;
     minion +tohit% = MonUMod[12] 50 x 66/100 = +33 (D2MOO UMod5_Strong; DifficultyLevels).
  U3 superunique: level alvl+3 (INFERRED, as unique); fixed mods from SuperUniques.txt Mod1-3 (5 = strong); Hell adds random
     bonuses (Basin) — the random draw is not modelled; both no-strong and strong rows are given.
  U4 boss (Diablo, Baal): MonStats Level(H) (boss flag; D2MOO Monster.cpp L197-201), TH scaled by MonLvl at that level.
  H1/H3/H4 as stage 6 (README § 13): CtH = clamp(2*alvl*floor(100*AR/(AR+Def))/(alvl+dlvl),5,95); +250 vs missiles;
     non-ToHit missiles auto-hit.
"""
from __future__ import annotations

import csv
import json
import statistics
import sys
from pathlib import Path

PKT = Path(__file__).resolve().parents[1]
RAW = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/datamine-acquisition/d2/raw")
DEF_MELEE, DEF_MISSILE, CLVL = 1203, 1453, 90


def rd(n):
    with open(RAW / n, encoding="latin-1", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def i(x, d=0):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return d


def cth(ar, d, alvl, dlvl=CLVL):
    if not ar or ar <= 0:
        return None
    f = 100 * ar // (ar + d)
    return max(5, min(95, 2 * alvl * f // (alvl + dlvl)))


def q(v):
    v = sorted(x for x in v if x is not None)
    if not v:
        return None
    if len(v) == 1:
        return {"n": 1, "median": v[0], "p25": v[0], "p75": v[0], "min": v[0], "max": v[0]}
    qs = statistics.quantiles(v, n=4, method="inclusive")
    return {"n": len(v), "median": statistics.median(v), "p25": qs[0], "p75": qs[2], "min": v[0], "max": v[-1]}


def main(out: Path):
    # (1) mean/mean r_DMG
    g = json.loads((PKT / "gd_damage_reconcile.json").read_text())
    gm = g["engine_native_static_summaries"]["weight_board_actors"]["trash"]["E5_mean_damaging_slot"]
    sd = json.loads((PKT / "d2_skill_damage.json").read_text())
    mm = {}
    for rk, R in sd["rules"].items():
        dm = R["dist_equal"]["mean_hit_mid_all_damaging_attacks"]
        mm[rk] = {"gd_E5_mean_damaging_slot": gm, "d2_mean_damaging_attack": dm,
                  "r_DMG_mean_over_mean": gm["median"] / dm["median"],
                  "iqr_ratio_p25_p25_p75_p75": [gm["p25"] / dm["p25"], gm["p75"] / dm["p75"]]}
    # (2) unique AR
    ms = {r["Id"]: r for r in rd("MonStats.txt") if r["Id"]}
    ml = {i(r["Level"]): r for r in rd("MonLvl.txt") if r["Level"].isdigit()}
    um = rd("MonUMod.txt")
    cdb = i({r["Name"]: r for r in rd("DifficultyLevels.txt")}["Hell"]["ChampionDamageBonus"])
    u_strong = i(um[13]["constants"]) * cdb // 100
    m_strong = i(um[12]["constants"]) * cdb // 100
    assert (u_strong, m_strong) == (66, 33)
    su = {r["Superunique"]: r for r in rd("SuperUniques.txt") if r["Superunique"]}
    hc = json.loads((PKT / "d2_hit_chance_r1.json").read_text())

    def ar_at(mid, lvl, slot):
        m = ms[mid]
        th = i(m[f"{slot}TH(H)"])
        if m.get("noRatio", "").strip() == "1":
            return th
        return th * i(ml[min(lvl, max(ml))]["L-TH(H)"]) // 100

    rows = []
    for r in hc["rows"]:
        base = r["alvl"]
        ul = base + 3
        for a in r["attacks"]:
            if a["role"] == "caster" or not a["ar"]:
                continue
            ar_u = ar_at(r["id"], ul, a["slot"])
            d = DEF_MISSILE if a["role"] == "ranged_physical" else DEF_MELEE
            rows.append({"id": r["id"], "slot": a["slot"], "role": a["role"], "slot_weight": r["slot_weight"],
                         "ar_normal": a["ar"], "ar_unique": ar_u, "ar_unique_extra_strong": ar_u * (100 + u_strong) // 100,
                         "ar_minion": ar_u, "ar_minion_strong": ar_u * (100 + m_strong) // 100,
                         "hit_normal": cth(a["ar"], d, base), "hit_unique": cth(ar_u, d, ul),
                         "hit_unique_extra_strong": cth(ar_u * (100 + u_strong) // 100, d, ul),
                         "hit_minion": cth(ar_u, d, ul)})
    # per type: best (max) hit among rolling attacks
    by = {}
    for x in rows:
        b = by.setdefault(x["id"], {"id": x["id"], "slot_weight": x["slot_weight"], "role": x["role"]})
        for k in ("ar_unique", "ar_unique_extra_strong", "hit_unique", "hit_unique_extra_strong", "hit_normal"):
            b[k] = max(b.get(k) or 0, x[k] or 0)
    types = list(by.values())
    caster_types = sum(1 for r in hc["rows"] if r["type_role"] == "caster") + 4
    special = []
    for name in ("Grand Vizier of Chaos", "Lord De Seis", "Infector of Souls"):
        s = su[name]
        mods = [i(s.get(f"Mod{k}")) for k in (1, 2, 3)]
        strong = 5 in mods
        lvl = 85 + 3
        best = None
        for slot in ("A1", "A2", "S1"):
            ar = ar_at(s["Class"], lvl, slot) if i(ms[s["Class"]][f"{slot}TH(H)"]) else 0
            if ar:
                ar_e = ar * (100 + u_strong) // 100 if strong else ar
                h = cth(ar_e, DEF_MELEE, lvl)
                if best is None or h > best["hit_melee"]:
                    best = {"slot": slot, "ar": ar_e, "hit_melee": h, "hit_vs_missile_def": cth(ar_e, DEF_MISSILE, lvl)}
        special.append({"name": name, "class": s["Class"], "kind": "superunique", "level": lvl, "mods": mods,
                        "extra_strong_fixed": strong, **(best or {})})
    for b in ("diablo", "baalcrab"):
        m = ms[b]
        lvl = i(m["Level(H)"])
        best = None
        for slot in ("A1", "A2", "S1"):
            if i(m[f"{slot}TH(H)"]):
                ar = ar_at(b, lvl, slot)
                h = cth(ar, DEF_MELEE, lvl)
                if best is None or h > best["hit_melee"]:
                    best = {"slot": slot, "ar": ar, "hit_melee": h, "hit_vs_missile_def": cth(ar, DEF_MISSILE, lvl)}
        special.append({"name": b, "kind": "boss", "level": lvl, **(best or {}),
                        "note": "most boss damage is skill-based (auto-hit casters); this row is the melee roll only"})
    doc = {
        "law": "LoD 1.13 Hell players-1; defender NODEX_quests Def 1,203 (1,453 vs missiles), clvl 90",
        "mean_over_mean_r_DMG": mm,
        "unique_mods": {"level_add": 3, "unique_extra_strong_tohit_pct": u_strong, "minion_strong_tohit_pct": m_strong},
        "grades": {"mean/mean r_DMG": "INFERRED (ratio of a MODEL-VERIFIED-composed GD figure and an INFERRED D2 figure)",
                   "unique AR": "DATAMINED inputs; U1 MODEL-VERIFIED (Basin + D2MOO level add); U2 MODEL-VERIFIED (D2MOO + MonUMod)",
                   "superunique level alvl+3": "INFERRED", "Hell random unique bonuses": "NOT MODELLED (both arms given)",
                   "hit chance": "INFERRED (computed; laws MODEL-VERIFIED)"},
        "summary": {
            "attack_AR_unique": q([x["ar_unique"] for x in rows]),
            "attack_AR_unique_extra_strong": q([x["ar_unique_extra_strong"] for x in rows]),
            "type_best_hit_unique": q([t["hit_unique"] for t in types]),
            "type_best_hit_unique_extra_strong": q([t["hit_unique_extra_strong"] for t in types]),
            "type_best_hit_normal_same_types": q([t["hit_normal"] for t in types]),
            "type_best_hit_unique_melee": q([t["hit_unique"] for t in types if t["role"] == "melee"]),
            "type_best_hit_unique_ranged_physical": q([t["hit_unique"] for t in types if t["role"] == "ranged_physical"]),
            "n_types_rolling": len(types), "n_caster_types_autohit": caster_types,
        },
        "superuniques_and_bosses": special,
        "rows": rows,
    }
    out.write_text(json.dumps(doc, indent=1))
    for rk, v in mm.items():
        print(rk, "mean/mean r_DMG %.2f [%.1f-%.1f]" % (v["r_DMG_mean_over_mean"], *v["iqr_ratio_p25_p25_p75_p75"]))
    for k, v in doc["summary"].items():
        print(k, v if not isinstance(v, dict) else (v["median"], v["p25"], v["p75"], v["min"], v["max"]))
    for s in special:
        print(s)


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else PKT / "d2_unique_ar_r1.json")
