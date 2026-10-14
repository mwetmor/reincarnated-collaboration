#!/usr/bin/env python3
"""C-13 stage 6 (KP-431) — D2 monster attack rating and hit chance against the Sorceress NODEX sheet, R1 (Hell, alvl 85,
players-1), per type and per attack slot, split by role (melee / ranged-physical / caster).

Read-only. Inputs: d2_enemy_quantities.json, d2_skill_damage.json (this packet); MonStats.txt, Missiles.txt (raw/).

Laws (all cited in README § 13):
  H1 CtH = clamp(2*alvl*floor(100*AR/(AR+Def)) / (alvl+dlvl), 5, 95), integer   D2MOO SUnitDmg.cpp SUNITDMG_IsHitSuccessful;
     Basin Attack; J4a F05. alvl = monster level (85 at R1; bosses n/a here), dlvl = clvl 90.
  H2 monster AR = attack TH (MonStats xxTH(H) x MonLvl L-TH(H)/100) + 5*Dex(0) + tohit, x(1+tohit%); champion +49 %.
  H3 defence: melee -> Def + vs-melee bonus (0); missile -> Def + vs-missile bonus (Spirit +250)    IsHitSuccessful L(bMissile)
  H4 a missile rolls to hit only if Missiles.txt ToHit is set; otherwise it auto-hits (100 %, no clamp)  MissMode.cpp L5058
  H5 a running player is hit by melee without a roll (GetResultFlags PLRMODE_RUN) — reported, not applied.
Role per attack: an A1/A2/S1 slot with no MissA1/MissA2/MissS1 missile = MELEE (rolls vs melee defence), even on a
  rangedtype monster; a slot that fires a missile = RANGED-PHYSICAL if that missile has ToHit set (rolls vs missile
  defence), else CASTER; every damaging monster SKILL (stage 3) whose missile has no ToHit = CASTER (auto-hit).
"""
from __future__ import annotations

import csv
import json
import statistics
import sys
from pathlib import Path

PKT = Path(__file__).resolve().parents[1]
RAW = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/datamine-acquisition/d2/raw")
DEF_LO, DEF_MID, DEF_HI = 1060, 1203, 1347        # NODEX_quests sheet (sorc_defense_sheet.json), KP-428 default
VS_MISSILE = 250                                  # Spirit ac-miss
CLVL, ALVL = 90, 85
CHAMP_TOHIT = 49


def rd(n):
    with open(RAW / n, encoding="latin-1", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def cth(ar, d, alvl=ALVL, dlvl=CLVL):
    if ar <= 0:
        return None
    f = 100 * ar // (ar + d) if ar + d > 0 else 100
    return max(5, min(95, 2 * alvl * f // (alvl + dlvl)))


def wq(pairs):
    rep = []
    for v, w in pairs:
        if v is not None:
            rep += [v] * int(w)
    rep.sort()
    if not rep:
        return None
    if len(rep) == 1:
        return {"n": 1, "median": rep[0], "p25": rep[0], "p75": rep[0], "min": rep[0], "max": rep[0]}
    qs = statistics.quantiles(rep, n=4, method="inclusive")
    return {"n": len(rep), "median": statistics.median(rep), "p25": qs[0], "p75": qs[2], "min": rep[0], "max": rep[-1]}


def main(out: Path):
    ms = {r["Id"]: r for r in rd("MonStats.txt") if r["Id"]}
    mi = {r["Missile"]: r for r in rd("Missiles.txt") if r["Missile"]}
    d2 = json.loads((PKT / "d2_enemy_quantities.json").read_text())["rules"]["R1_alvl85_all"]
    sk = {(r["id"], r["alvl"]): r for r in json.loads((PKT / "d2_skill_damage.json").read_text())["rules"]["R1_alvl85_all"]["rows"]}
    rows, attacks = [], []
    for r in d2["rows"]:
        m = ms[r["id"]]
        ranged = m.get("rangedtype", "").strip() == "1"
        per = []
        for slot, a in r["attacks"].items():
            dmg = r["per_attack"][slot]["total_mid"]
            if a["ar"] <= 0 and dmg <= 0:
                continue
            miss = (m.get(f"Miss{slot}") or "").strip()
            if ranged and miss:
                tohit = mi.get(miss, {}).get("ToHit", "").strip() not in ("", "0")
                role = "ranged_physical" if tohit else "caster"
            else:
                role = "melee"          # a slot with no MissXX missile is a melee swing, even on a rangedtype monster
            if role == "melee":
                h = {k: cth(a["ar"], d) for k, d in (("def_lo", DEF_LO), ("def_mid", DEF_MID), ("def_hi", DEF_HI))}
            elif role == "ranged_physical":
                h = {k: cth(a["ar"], d + VS_MISSILE) for k, d in (("def_lo", DEF_LO), ("def_mid", DEF_MID), ("def_hi", DEF_HI))}
            else:
                h = {"def_lo": 100, "def_mid": 100, "def_hi": 100}
            hc = cth(a["ar"] * (100 + CHAMP_TOHIT) // 100, DEF_MID + (VS_MISSILE if role == "ranged_physical" else 0),
                     alvl=ALVL + 2) if role != "caster" else 100
            per.append({"slot": slot, "role": role, "missile": miss or None, "ar": a["ar"], "dmg_mid": dmg,
                        "hit_pct": h, "hit_pct_champion_def_mid": hc})
        for s in sk[(r["id"], r["alvl"])]["skills"]:
            if s["damaging"] and not s["stream"]:
                per.append({"slot": "skill:" + s["skill"], "role": "caster", "missile": s["path"], "ar": None,
                            "dmg_mid": s["per_hit_mid"], "hit_pct": {"def_lo": 100, "def_mid": 100, "def_hi": 100},
                            "hit_pct_champion_def_mid": 100})
        if not per:
            continue
        best = max(per, key=lambda x: x["dmg_mid"])
        rolling = [x for x in per if x["role"] != "caster"]
        rows.append({"id": r["id"], "alvl": r["alvl"], "slot_weight": r["slot_weight"], "rangedtype": ranged,
                     "type_role": best["role"], "best_attack": best["slot"],
                     "best_attack_hit_pct_def_mid": best["hit_pct"]["def_mid"],
                     "max_ar": max((x["ar"] for x in rolling if x["ar"]), default=None),
                     "max_ar_hit_pct_def_mid": max((x["hit_pct"]["def_mid"] for x in rolling if x["ar"]), default=None),
                     "attacks": per})
        for x in per:
            attacks.append({"id": r["id"], "slot_weight": r["slot_weight"], **x})

    def dist(rowset, f, weighted):
        return wq([(f(x), x["slot_weight"] if weighted else 1) for x in rowset])

    summary = {}
    for role in ("melee", "ranged_physical", "caster", "all"):
        tr = [x for x in rows if role == "all" or x["type_role"] == role]
        at = [x for x in attacks if role == "all" or x["role"] == role]
        summary[role] = {
            "n_types_by_best_attack_role": len(tr), "n_attacks": len(at),
            "type_best_attack_hit_pct_def_mid": {"equal": dist(tr, lambda x: x["best_attack_hit_pct_def_mid"], False),
                                                 "slot": dist(tr, lambda x: x["best_attack_hit_pct_def_mid"], True)},
            "attack_AR": {"equal": dist([a for a in at if a["ar"]], lambda x: x["ar"], False)},
            "attack_hit_pct_def_lo_mid_hi": {k: dist([a for a in at if a["ar"] or a["role"] == "caster"], (lambda kk: lambda x: x["hit_pct"][kk])(k), False)
                                              for k in ("def_lo", "def_mid", "def_hi")},
            "attack_hit_pct_champion_def_mid": dist(at, lambda x: x["hit_pct_champion_def_mid"], False),
        }
    doc = {"law": "LoD 1.13, Hell, alvl 85, players-1; defender = Sorceress NODEX_quests (KP-428 default), clvl 90",
           "defence": {"lo": DEF_LO, "mid": DEF_MID, "hi": DEF_HI, "vs_missile_extra": VS_MISSILE},
           "grades": {"AR per slot": "DATAMINED (MonStats x MonLvl, MODEL-VERIFIED scaling)",
                      "hit chance": "MODEL-VERIFIED law (D2MOO + Basin + J4a F05) applied to DATAMINED inputs; values INFERRED (computed)",
                      "role split": "DATAMINED flags (rangedtype, MissA1/A2/S1, Missiles.ToHit) + MODEL-VERIFIED H4",
                      "champion row": "INFERRED lower-bound form: AR x1.49 at alvl+2 for the level term only (TH not re-looked-up at +2)"},
           "notes": ["casters auto-hit: 100 %, unclamped (H4); they are NOT blockable unless the missile carries physical damage",
                     "a running Sorceress is hit by melee without a roll (H5) — not applied in these figures",
                     "block (NODEX 3 %) applies after a successful hit roll and is not folded in"],
           "summary": summary, "rows": rows}
    out.write_text(json.dumps(doc, indent=1))
    for role, v in summary.items():
        e = v["type_best_attack_hit_pct_def_mid"]["equal"]; a = v["attack_AR"]["equal"]
        hm = v["attack_hit_pct_def_lo_mid_hi"]["def_mid"]
        print(role, "types", v["n_types_by_best_attack_role"], "attacks", v["n_attacks"],
              "| type hit% median", e and e["median"], e and [e["p25"], e["p75"], e["min"], e["max"]],
              "| attack AR", a and round(a["median"]), a and [round(a["p25"]), round(a["p75"])],
              "| attack hit% mid", hm and hm["median"], hm and [hm["p25"], hm["p75"], hm["min"], hm["max"]])


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else PKT / "d2_hit_chance_r1.json")
