#!/usr/bin/env python3
"""C-13 — D2 home-endgame enemy population and per-monster quantities (LoD 1.13, Hell, players-1).

Read-only. Inputs: the J-S7 tables (sha-pinned) plus MonUMod/SuperUniques/MonStats2 from the same
fabd/diablo2 @ 45112569 mirror (agentic_orchestration/research/datamine-acquisition/d2/raw/).

Laws used (every one cited in README § 2 with its sources):
  L1 monster level: Hell expansion, non-boss & non-NoRatio -> area MonLvl3Ex; boss/NoRatio -> MonStats Level(H)
     (D2MOO Monster.cpp L197-201).
  L2 stat = MonStats(H) value x MonLvl[mlvl].L-xx(H) / 100 (integer), except NoRatio rows use the raw value
     (D2MOO MonsterTbls.cpp DATATBLS_CalculateMonsterStatsByLevel; offset 3 = the L- expansion columns).
  L3 HP at players-1: no player-count bonus (MONSTER_GetHpBonus(1) = 0).
  L4 champion (Hell): life +100% of base-level life; level +2 for AR/damage MonLvl lookup; +damage% =
     100 x ChampionDamageBonus/100 = +66; +tohit% = 75 x 66/100 = +49 (MonUMod constants rows 6,10,11;
     DifficultyLevels; D2MOO UMod2/UMod16; Basin Champion).
     unique (Hell): life +100%; level +3 for AR/damage; Extra Strong (if rolled) +150x0.66=+99 dmg%, +100x0.66=+66 AR%.
     minion (Hell): life +50%; level +3.
"""
from __future__ import annotations

import csv
import hashlib
import json
import statistics
import sys
from pathlib import Path

RAW = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/datamine-acquisition/d2/raw")
FILES = ["MonStats.txt", "MonLvl.txt", "Levels.txt", "DifficultyLevels.txt", "MonUMod.txt", "SuperUniques.txt",
         "MonStats2.txt"]
J_S7_PINS = {
    "MonStats.txt": "973eedacd121f724f6dca1c7201750f6a4e60480c3d536ef5a9cb36853d38193",
    "MonLvl.txt": "7624abe33673f8bf4f243de141fb387a1d78f1192466ace49ac8b3c175fa4df8",
    "Levels.txt": "3163b66ea391b1e51a4ead54d7f3465d7fdc4fe6f3385f098826c9bb6cca837b",
    "DifficultyLevels.txt": "aaa1a5d93df8c62707cf05308d82418ae7058ac1ac15ac768331f2abe440ff88",
}
MODE = {"4": "A1", "5": "A2", "8": "S1", "9": "S2", "10": "S3", "11": "S4", "7": "SC", "6": "BL"}
RESF = [("phys", "ResDm(H)"), ("magic", "ResMa(H)"), ("fire", "ResFi(H)"), ("light", "ResLi(H)"),
        ("cold", "ResCo(H)"), ("poison", "ResPo(H)")]

# --- population rules (README § 1) -------------------------------------------------------------
# ⚑ Column set (L2b). Default "ladder" = single-player/ladder `L-` columns (the primary, unchanged). "classic" = the
#   non-ladder Battle.net columns for the two quantities that differ (Basin MonLvl: Hell life and defence; attack
#   rating, damage and experience are identical in all versions): HP(H) and AC(H). Selected by argv[2].
COLSET = sys.argv[2] if len(sys.argv) > 2 else "ladder"
assert COLSET in ("ladder", "classic")
HPCOL, ACCOL = ("L-HP(H)", "L-AC(H)") if COLSET == "ladder" else ("HP(H)", "AC(H)")

RULES = {
    "R1_alvl85_all": {"desc": "every Hell area at the maximum area level 85 (Levels.txt MonLvl3Ex == 85)",
                      "select": lambda r: r["MonLvl3Ex"] == "85"},
    "R2_chaos_sanctum": {"desc": "Chaos Sanctum only (Id 108, alvl 85)", "select": lambda r: r["Id"] == "108"},
    "R3_worldstone_throne": {"desc": "Worldstone Keep 1-3 + Throne of Destruction (Ids 128-131, alvl 85)",
                             "select": lambda r: r["Id"] in {"128", "129", "130", "131"}},
    "R4_alvl81plus": {"desc": "every Hell area at alvl >= 81 (the broad Hell endgame band)",
                      "select": lambda r: r["MonLvl3Ex"].isdigit() and int(r["MonLvl3Ex"]) >= 81},
}
# Named bosses/superuniques that belong to a rule's content (SuperUniques.txt names; Level(H) for bosses).
RULE_BOSSES = {
    "R2_chaos_sanctum": {"bosses": ["diablo"],
                         "superuniques": ["Grand Vizier of Chaos", "Lord De Seis", "Infector of Souls"]},
    # Baal's five wave bosses (Colenzo, Achmel, Bartuc, Ventar, Lister) are NOT rows of SuperUniques.txt or
    # boss-flagged MonStats rows in 1.13; their spawn is hard-coded (UNRESOLVED here, README § 1.3).
    "R3_worldstone_throne": {"bosses": ["baalcrab"], "superuniques": []},
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(name: str):
    with open(RAW / name, encoding="latin-1", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def i(x, d=0):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return d


def ratio(r: int, v: int) -> int:
    """DATATBLS_ApplyRatio(r, v, 100) — integer, as D2MOO; v may be negative."""
    return (r * v) // 100 if v >= 0 else -((r * -v) // 100)


def q(vals):
    v = sorted(x for x in vals if x is not None)
    if not v:
        return None
    if len(v) == 1:
        return {"n": 1, "median": v[0], "p25": v[0], "p75": v[0], "min": v[0], "max": v[0]}
    qs = statistics.quantiles(v, n=4, method="inclusive")
    return {"n": len(v), "median": statistics.median(v), "p25": qs[0], "p75": qs[2], "min": v[0], "max": v[-1]}


def wq(pairs):
    """Weighted quantiles by repetition (weights are small integers: slot counts)."""
    rep = []
    for v, w in pairs:
        if v is not None:
            rep += [v] * int(w)
    return q(rep)


def main(out: Path):
    for f, h in J_S7_PINS.items():
        got = sha(RAW / f)
        assert got == h, f"J-S7 pin broken: {f} {got}"
    ms = {r["Id"]: r for r in read("MonStats.txt") if r["Id"] and r["Id"] != "Expansion"}
    ml = {i(r["Level"]): r for r in read("MonLvl.txt") if r["Level"].isdigit()}
    lv = [r for r in read("Levels.txt") if r["Id"].isdigit()]
    dl = {r["Name"]: r for r in read("DifficultyLevels.txt")}
    um = read("MonUMod.txt")
    su = {r["Superunique"]: r for r in read("SuperUniques.txt") if r["Superunique"]}
    ms2 = {r["Id"]: r for r in read("MonStats2.txt") if r["Id"]}

    # Cross-check vs Basin MonLvl ("Ladder and single-player" tables = the L- columns), captured raw.
    b85 = {"L-AC(H)": 1651, "L-TH(H)": 3408, "L-HP(H)": 6182, "L-DM(H)": 96, "AC(H)": 1403, "HP(H)": 4637}
    b88 = {"L-AC(H)": 1704, "L-TH(H)": 3522, "L-HP(H)": 6527, "L-DM(H)": 100, "AC(H)": 1448, "HP(H)": 4895}
    for lvl, ref in ((85, b85), (88, b88)):
        for col, v in ref.items():
            assert i(ml[lvl][col]) == v, f"MonLvl {lvl} {col} {ml[lvl][col]} != Basin {v}"
    hell = dl["Hell"]
    cdb = i(hell["ChampionDamageBonus"])
    const = {k: i(um[k]["constants"]) for k in range(len(um)) if um[k].get("constants", "") != ""}
    umod = {
        "champion_hp_pct_H": const[6], "unique_hp_pct_H": const[9], "minion_hp_pct_H": const[3],
        "champion_dmg_pct": const[11] * cdb // 100, "champion_tohit_pct": const[10] * cdb // 100,
        "unique_strong_dmg_pct": const[15] * cdb // 100, "unique_strong_tohit_pct": const[13] * cdb // 100,
        "ChampionDamageBonus_H": cdb, "ResistPenalty_H": i(hell["ResistPenalty"]),
    }
    assert umod["champion_hp_pct_H"] == 100 and umod["unique_hp_pct_H"] == 100 and umod["minion_hp_pct_H"] == 50
    assert umod["champion_dmg_pct"] == 66 and umod["champion_tohit_pct"] == 49

    def flag(m, c):
        return m.get(c, "").strip() in ("1",)

    def mstats(mid: str, alvl: int, lvl_add: int = 0):
        m = ms[mid]
        boss = flag(m, "boss") or flag(m, "primeevil")
        noratio = flag(m, "noRatio")
        base_lvl = i(m["Level(H)"]) if (boss or noratio) else alvl
        L = ml[min(base_lvl, max(ml))]
        La = ml[min(base_lvl + lvl_add, max(ml))]
        def r_(col_ml, val, row):
            return val if noratio else ratio(i(row[col_ml]), val)
        hp_min, hp_max = r_(HPCOL, i(m["MinHP(H)"]), L), r_(HPCOL, i(m["MaxHP(H)"]), L)
        ac = r_(ACCOL, i(m["AC(H)"]), L)
        attacks = {}
        for slot in ("A1", "A2", "S1"):
            mn, mx, th = i(m[f"{slot}MinD(H)"]), i(m[f"{slot}MaxD(H)"]), i(m[f"{slot}TH(H)"])
            if mn or mx or th:
                attacks[slot] = {"phys_min": r_("L-DM(H)", mn, La), "phys_max": r_("L-DM(H)", mx, La),
                                 "ar": r_("L-TH(H)", th, La)}
        elems = []
        for k in (1, 2, 3):
            t = m.get(f"El{k}Type", "").strip()
            if not t:
                continue
            elems.append({"mode": MODE.get(m.get(f"El{k}Mode", "").strip(), m.get(f"El{k}Mode", "")),
                          "type": t, "pct": i(m.get(f"El{k}Pct(H)")),
                          "min": r_("L-DM(H)", i(m.get(f"El{k}MinD(H)")), La),
                          "max": r_("L-DM(H)", i(m.get(f"El{k}MaxD(H)")), La),
                          "dur_frames": i(m.get(f"El{k}Dur(H)"))})
        # per-attack expected total: phys mid + sum(pct x elemental mid) for elementals bound to that mode
        per_attack = {}
        for slot, a in attacks.items():
            e = sum(x["pct"] / 100 * (x["min"] + x["max"]) / 2 for x in elems if x["mode"] == slot)
            per_attack[slot] = {"phys_mid": (a["phys_min"] + a["phys_max"]) / 2, "elem_expected": e,
                                "total_mid": (a["phys_min"] + a["phys_max"]) / 2 + e, "ar": a["ar"]}
        skills = [(m.get(f"Skill{k}", ""), i(m.get(f"Sk{k}lvl"))) for k in range(1, 9) if m.get(f"Skill{k}", "").strip()]
        s2 = ms2.get(m.get("MonStatsEx", "") or mid, {})
        return {
            "id": mid, "name_str": m["NameStr"], "base_mlvl": base_lvl, "lvl_add": lvl_add, "boss": boss,
            "noRatio": noratio, "hp_min": hp_min, "hp_max": hp_max, "hp_mid": (hp_min + hp_max) / 2,
            "defense": ac, "attacks": attacks, "elemental": elems, "per_attack": per_attack,
            "max_attack_total_mid": max((p["total_mid"] for p in per_attack.values()), default=None),
            "max_attack_ar": max((a["ar"] for a in attacks.values()), default=None),
            "res": {k: i(m[c]) for k, c in RESF},
            "immune": [k for k, c in RESF if i(m[c]) >= 100],
            "aidel_H_frames": i(m["aidel(H)"]), "velocity": i(m["Velocity"]), "run": i(m["Run"]),
            "isMelee": flag(m, "isMelee"), "rangedtype": flag(m, "rangedtype"),
            "skills_H": skills, "ToBlock_H": i(m["ToBlock(H)"]), "Drain_H": i(m["Drain(H)"]),
            "sizeX": i(s2.get("SizeX")), "sizeY": i(s2.get("SizeY")), "MeleeRng": i(s2.get("MeleeRng")),
        }

    out_rules = {}
    for rk, rule in RULES.items():
        areas = [r for r in lv if rule["select"](r)]
        slots = []
        for r in areas:
            for k in range(1, 26):
                v = (r.get(f"nmon{k}") or "").strip()
                if v:
                    slots.append((int(r["Id"]), r["LevelName"], i(r["MonLvl3Ex"]), v))
        missing = sorted({s[3] for s in slots if s[3] not in ms})
        rows = []
        for (aid, aname, alvl, mid) in slots:
            if mid not in ms:
                continue
            rows.append({"area_id": aid, "area": aname, "alvl": alvl, **mstats(mid, alvl)})
        # distinct (type, alvl) rows with slot weight
        agg = {}
        for r in rows:
            key = (r["id"], r["alvl"])
            agg.setdefault(key, {"row": r, "w": 0})["w"] += 1
        uniq = [v["row"] | {"slot_weight": v["w"]} for v in agg.values()]

        def dist(field, sub=None, rowset=uniq, weighted=False):
            get = (lambda r: r[field]) if sub is None else (lambda r: r[field][sub])
            if weighted:
                return wq([(get(r), r["slot_weight"]) for r in rowset])
            return q([get(r) for r in rowset])

        res_d = {}
        for k, _ in RESF:
            vals = [r["res"][k] for r in uniq]
            res_d[k] = {"dist_equal": q(vals), "n_immune": sum(1 for v in vals if v >= 100),
                        "n_types": len(vals),
                        "after_kit_pierce_0": "monster resists are NOT reduced by the Hell ResistPenalty (that penalty is player-side)"}
        champ = []
        uniq_m = []
        for r in uniq:
            if r["boss"]:
                continue
            c = mstats(r["id"], r["alvl"], lvl_add=2)
            u = mstats(r["id"], r["alvl"], lvl_add=3)
            champ.append({"id": r["id"], "alvl": r["alvl"],
                          "hp_mid": r["hp_mid"] * (100 + umod["champion_hp_pct_H"]) / 100,
                          "max_attack_total_mid": None if c["max_attack_total_mid"] is None else c["max_attack_total_mid"] * (100 + umod["champion_dmg_pct"]) / 100,
                          "max_attack_ar": None if c["max_attack_ar"] is None else c["max_attack_ar"] * (100 + umod["champion_tohit_pct"]) / 100})
            uniq_m.append({"id": r["id"], "alvl": r["alvl"],
                           "hp_mid": r["hp_mid"] * (100 + umod["unique_hp_pct_H"]) / 100,
                           "max_attack_total_mid_no_strong": u["max_attack_total_mid"],
                           "max_attack_total_mid_extra_strong": None if u["max_attack_total_mid"] is None else u["max_attack_total_mid"] * (100 + umod["unique_strong_dmg_pct"]) / 100,
                           "max_attack_ar_no_strong": u["max_attack_ar"]})
        bosses = []
        rb = RULE_BOSSES.get(rk, {})
        for b in rb.get("bosses", []):
            bosses.append({"kind": "boss", **mstats(b, 85)})
        for sname in rb.get("superuniques", []):
            s = su.get(sname)
            if not s:
                bosses.append({"kind": "superunique", "name": sname, "status": "NOT FOUND in SuperUniques.txt"})
                continue
            base = mstats(s["Class"], 85, lvl_add=3)
            bosses.append({"kind": "superunique", "name": sname, "class": s["Class"],
                           "mods": [s.get("Mod1"), s.get("Mod2"), s.get("Mod3")],
                           "hp_mid_with_unique_bonus": base["hp_mid"] * (100 + umod["unique_hp_pct_H"]) / 100,
                           "level_note": "superunique level = alvl+3 (INFERRED: Basin Unique page applies +3 to uniques; superunique placement level not code-read)",
                           **{k: base[k] for k in ("hp_mid", "defense", "max_attack_total_mid", "max_attack_ar", "res", "immune")}})
        out_rules[rk] = {
            "desc": rule["desc"],
            "areas": [{"id": int(r["Id"]), "name": r["LevelName"], "alvl": i(r["MonLvl3Ex"]),
                       "nmon": [r[f"nmon{k}"] for k in range(1, 26) if (r.get(f"nmon{k}") or "").strip()]} for r in areas],
            "n_areas": len(areas), "n_slots": len(slots), "n_distinct_type_alvl": len(uniq),
            "missing_monstats_ids": missing,
            "distributions_normal": {
                "weighting_note": "equal = one vote per distinct (MonStats Id, alvl); slot = weighted by Levels.txt nmon slot occurrences",
                "hp_mid": {"equal": dist("hp_mid"), "slot": dist("hp_mid", weighted=True)},
                "defense": {"equal": dist("defense"), "slot": dist("defense", weighted=True)},
                "max_attack_total_mid": {"equal": dist("max_attack_total_mid"), "slot": dist("max_attack_total_mid", weighted=True)},
                "max_attack_ar": {"equal": dist("max_attack_ar"), "slot": dist("max_attack_ar", weighted=True)},
                "aidel_H_frames": {"equal": dist("aidel_H_frames")},
                "resists": res_d,
            },
            "distributions_champion": {"hp_mid": q([c["hp_mid"] for c in champ]),
                                       "max_attack_total_mid": q([c["max_attack_total_mid"] for c in champ]),
                                       "max_attack_ar": q([c["max_attack_ar"] for c in champ])},
            "distributions_unique": {"hp_mid": q([u["hp_mid"] for u in uniq_m]),
                                     "max_attack_total_mid_no_strong": q([u["max_attack_total_mid_no_strong"] for u in uniq_m]),
                                     "max_attack_total_mid_extra_strong": q([u["max_attack_total_mid_extra_strong"] for u in uniq_m])},
            "bosses_and_superuniques": bosses,
            "rows": sorted(uniq, key=lambda r: (r["alvl"], r["id"])),
        }

    doc = {
        "commission": "C-13 enemy anchor (JOIN-1, KP-420/421/423)", "law": "LoD 1.13 expansion, Hell, players-1",
        **({"column_set": "classic (non-ladder Battle.net): HP(H), AC(H)"} if COLSET == "classic" else {}),
        "source": "fabd/diablo2 @ 45112569deb9384738ccafe5c24ebbb71f41c7c9 code/d2_113_data",
        "file_sha256": {f: sha(RAW / f) for f in FILES},
        "umod_hell": umod,
        "grades": {
            "per-monster MonStats/MonLvl values": "DATAMINED",
            "scaling laws L1-L4": "MODEL-VERIFIED (D2MOO 1.10f code + Basin; see README § 2)",
            "per_attack elem_expected (pct x mid)": "INFERRED (expected value of the El%-chance add; El mode binding read from MonStats El*Mode)",
            "monster SKILL damage (Skill1-8)": "NOT COMPUTED (listed only; needs Skills.txt monster calcs per skill)",
            "attack/cast rate": "UNKNOWN (AnimData.d2 frame counts are not in the txt tables; aidel(H) is AI think delay, a proxy only)",
            "superunique level alvl+3": "INFERRED",
        },
        "rules": out_rules,
    }
    out.write_text(json.dumps(doc, indent=1, default=str))
    for rk, r in out_rules.items():
        d = r["distributions_normal"]
        print(rk, "areas", r["n_areas"], "types", r["n_distinct_type_alvl"], "missing", r["missing_monstats_ids"])
        for f in ("hp_mid", "defense", "max_attack_total_mid", "max_attack_ar"):
            e = d[f]["equal"]
            print(f"   {f}: median {e['median']:.0f} IQR {e['p25']:.0f}-{e['p75']:.0f} range {e['min']:.0f}-{e['max']:.0f}")
        fr = d["resists"]["fire"]
        print(f"   fire res: median {fr['dist_equal']['median']} IQR {fr['dist_equal']['p25']}-{fr['dist_equal']['p75']} immune {fr['n_immune']}/{fr['n_types']}")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("d2_enemy_quantities.json"))
