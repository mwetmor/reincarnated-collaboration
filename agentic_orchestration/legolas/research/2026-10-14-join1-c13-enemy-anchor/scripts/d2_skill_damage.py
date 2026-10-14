#!/usr/bin/env python3
"""C-13 / KP-428 (1) — D2 monster SKILL damage per landed hit for the R1..R4 populations (LoD 1.13, Hell, players-1).

Read-only. Inputs: d2_enemy_quantities.json (this packet) and the 1.13 txt tables (raw/: MonStats, MonLvl, Skills,
Missiles, DifficultyLevels).

Code laws (D2MOO @ 5596f5cb, captured in captures/):
  S1 skill level = MonStats SkNlvl + DifficultyLevels.MonsterSkillBonus (Hell 7)        Monster.cpp L246-262
  S2 level bracket bonus: lvl 2-8 L1/lvl; 9-16 L2; 17-22 L3; 23-28 L4; 29+ L5            D2Skills.cpp L2459-2486
  S3 skill phys  = (MinDam + bracket(MinLevDam)) << HitShift  [+ SrcDam/128 x owner weapon dmg]   D2Skills.cpp L2490-2620
     skill elem  = (EMin + bracket(EMinLev)) << HitShift                                   D2Skills.cpp L2623-2717
  S4 missile: if Missiles.Skill is blank -> the missile's own MinDamage/EMin(+brackets)<<HitShift, + SrcDamage/128 x owner
     dmg; else the named skill's S3 damage                                                  Missile.cpp L466-760, L1001-
  S5 owner weapon damage for a monster = the MonStats attack column of the skill's mode (A1/A2/S1), MonLvl-scaled
     (MonsterTbls.cpp CalculateMonsterStatsByLevel). Mode->column mapping for S2..S4 modes is INFERRED (-> S1 if
     present, else A1).
  Champion +66 % damage applies to skill damage too (STAT_DAMAGEPERCENT feeds missile nDamagePercent, Missile.cpp
  L697-712) — applied only in the champion figure.
Units: values << HitShift are 1/256 points; whole points = x / 256.
NOT evaluated: DmgSymPerCalc/EDmgSymPerCalc formulas (flagged per skill if present).
"""
from __future__ import annotations

import csv
import json
import statistics
import sys
from pathlib import Path

PKT = Path(__file__).resolve().parents[1]
RAW = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/datamine-acquisition/d2/raw")
HELL_SKILL_BONUS_EXPECTED = 7

# Skills whose damage is delivered as a per-frame stream / field (not a single landed hit) — DECLARED list.
STREAM = {"MegademonInferno", "FetishInferno", "Imp Inferno", "VampireFirewall", "CountessFirewall", "MonBlizzard",
          "Mosquito", "RegurgitatorEat"}
MODECOL = {"A1": "A1", "A2": "A2", "S1": "S1"}
# Skills whose MinDam/MaxDam fields are not hit damage (curse parameters / ally heal) — DECLARED.
NONDAMAGING = {"Blood Mana", "Healing Vortex"}
# srvdofunc 148 (DoomKnightMissile): missile = srvmissilea + the monster's random component[10] (SkillMonst.cpp
# L2119-2155) -> undeadmissile1..4 (poison / fire / cold / physical). Component distribution unknown -> equal (INFERRED).
DOOMKNIGHT_VARIANTS = ["undeadmissile1", "undeadmissile2", "undeadmissile3", "undeadmissile4"]


def rd(n):
    with open(RAW / n, encoding="latin-1", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def i(x, d=0):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return d


def bracket(lvl, L):
    L = [i(x) for x in L]
    if lvl <= 1:
        return 0
    if lvl > 28:
        return 7 * L[0] + L[4] * (lvl - 28) + 6 * (L[2] + L[3]) + 8 * L[1]
    if lvl > 22:
        return 7 * L[0] + L[3] * (lvl - 22) + 6 * L[2] + 8 * L[1]
    if lvl > 16:
        return 7 * L[0] + L[2] * (lvl - 16) + 8 * L[1]
    if lvl > 8:
        return 7 * L[0] + L[1] * (lvl - 8)
    return L[0] * (lvl - 1)


def q(v):
    v = sorted(x for x in v if x is not None)
    if not v:
        return None
    if len(v) == 1:
        return {"n": 1, "median": v[0], "p25": v[0], "p75": v[0], "min": v[0], "max": v[0]}
    qs = statistics.quantiles(v, n=4, method="inclusive")
    return {"n": len(v), "median": statistics.median(v), "p25": qs[0], "p75": qs[2], "min": v[0], "max": v[-1]}


def main(out: Path):
    sk = {r["skill"]: r for r in rd("Skills.txt") if r["skill"]}
    mi = {r["Missile"]: r for r in rd("Missiles.txt") if r["Missile"]}
    ms = {r["Id"]: r for r in rd("MonStats.txt") if r["Id"]}
    dl = {r["Name"]: r for r in rd("DifficultyLevels.txt")}
    bonus = i(dl["Hell"]["MonsterSkillBonus"])
    assert bonus == HELL_SKILL_BONUS_EXPECTED
    d2 = json.loads((PKT / "d2_enemy_quantities.json").read_text())

    def skill_damage(sname, lvl, owner_attacks):
        s = sk[sname]
        hs = i(s["HitShift"])
        mode_col = None
        out = {"skill": sname, "level": lvl, "srvdofunc": s["srvdofunc"], "stream": sname in STREAM}
        missiles = [s[c] for c in ("srvmissile", "srvmissilea", "srvmissileb", "srvmissilec") if s[c]]
        flags = []
        if s.get("DmgSymPerCalc", "").strip() or s.get("EDmgSymPerCalc", "").strip():
            flags.append("skill DmgSymPerCalc/EDmgSymPerCalc present, NOT evaluated")

        def own_skill():
            pmin = (i(s["MinDam"]) + bracket(lvl, [s[f"MinLevDam{k}"] for k in range(1, 6)])) << hs
            pmax = (i(s["MaxDam"]) + bracket(lvl, [s[f"MaxLevDam{k}"] for k in range(1, 6)])) << hs
            emin = (i(s["EMin"]) + bracket(lvl, [s[f"EMinLev{k}"] for k in range(1, 6)])) << hs
            emax = (i(s["EMax"]) + bracket(lvl, [s[f"EMaxLev{k}"] for k in range(1, 6)])) << hs
            return pmin / 256, pmax / 256, emin / 256, emax / 256, s["EType"], i(s["SrcDam"])

        def own_missile(m):
            x = mi[m]
            h = i(x["HitShift"])
            pmin = (i(x["MinDamage"]) + bracket(lvl, [x[f"MinLevDam{k}"] for k in range(1, 6)])) << h
            pmax = (i(x["MaxDamage"]) + bracket(lvl, [x[f"MaxLevDam{k}"] for k in range(1, 6)])) << h
            emin = (i(x["EMin"]) + bracket(lvl, [x[f"MinELev{k}"] for k in range(1, 6)])) << h
            emax = (i(x["Emax"]) + bracket(lvl, [x[f"MaxELev{k}"] for k in range(1, 6)])) << h
            if x.get("DmgSymPerCalc", "").strip() or x.get("EDmgSymPerCalc", "").strip():
                flags.append(f"missile {m} DmgSymPerCalc present, NOT evaluated")
            return pmin / 256, pmax / 256, emin / 256, emax / 256, x["EType"], i(x["SrcDamage"])

        path = "skill"
        if sname == "DoomKnightMissile":
            vals = []
            for vm in DOOMKNIGHT_VARIANTS:
                v = own_missile(vm)
                vals.append((vm, v))
            hits = [(vm, v) for vm, v in vals if v[4] != "pois"]
            pmin = sum(v[0] for _, v in hits) / len(hits); pmax = sum(v[1] for _, v in hits) / len(hits)
            emin = sum(v[2] for _, v in hits) / len(hits); emax = sum(v[3] for _, v in hits) / len(hits)
            et, src = "mixed(fire|cold|phys)", 0
            path = "srvdo148: mean of hit variants undeadmissile2-4 (poison variant 1 is a DoT, reported in flags)"
            flags.append("variant component distribution unknown; equal weight over the 3 hit variants (INFERRED)")
            pv = vals[0][1]
            flags.append(f"poison variant undeadmissile1: per-frame {(pv[2]+pv[3])/2:.3f} pts (HitShift 0) over ELen frames")
            out.update({"path": path, "phys_min": pmin, "phys_max": pmax, "srcdam_128": 0, "srcdam_part_mid": 0.0,
                        "elem_type": et, "elem_min": emin, "elem_max": emax,
                        "per_hit_mid": (pmin + pmax) / 2 + (emin + emax) / 2, "damaging": True, "flags": flags})
            return out
        if missiles and mi.get(missiles[0]) is not None and not mi[missiles[0]]["Skill"].strip():
            pmin, pmax, emin, emax, et, src = own_missile(missiles[0])
            path = f"missile:{missiles[0]}"
            # follow a sub/explosion missile that carries damage when the first carries none (e.g. bolt -> explode)
            if pmin == pmax == emin == emax == 0:
                for sub in (mi[missiles[0]].get("ExplosionMissile"), mi[missiles[0]].get("SubMissile1"),
                            mi[missiles[0]].get("HitSubMissile1")):
                    if sub and sub in mi and not mi[sub]["Skill"].strip():
                        a = own_missile(sub)
                        if any(a[:4]):
                            pmin, pmax, emin, emax, et, src = a
                            path += f"->{sub}"
                            break
        else:
            pmin, pmax, emin, emax, et, src = own_skill()
            if missiles:
                path = f"skill(via missile {missiles[0]} with Skill set)"
        src_part = 0.0
        if src and src not in (-1, 255):
            # owner weapon damage of the skill's mode (S5)
            col = owner_attacks.get("S1") or owner_attacks.get("A1")
            if col:
                src_part = src / 128 * (col["phys_min"] + col["phys_max"]) / 2
                flags.append("srcdam uses the S1 (else A1) MonStats column as owner weapon damage (INFERRED mode map)")
        phys_mid = (pmin + pmax) / 2 + src_part
        elem_mid = (emin + emax) / 2
        if et == "pois":
            flags.append("poison element is a DoT (per-frame over ELen), excluded from per-hit; elem value is per frame")
            elem_mid_hit = 0.0
        else:
            elem_mid_hit = elem_mid
        if path.startswith("missile:") and mi[missiles[0]]["HitShift"].strip() == "" and (emin or emax or pmin or pmax):
            flags.append("missile HitShift blank (=0): value is on the 1/256 scale as coded — suspiciously low, UNVERIFIED")
        dmg = (phys_mid + elem_mid_hit) > 0 and sname not in NONDAMAGING
        out.update({"path": path, "phys_min": pmin, "phys_max": pmax, "srcdam_128": src, "srcdam_part_mid": src_part,
                    "elem_type": et, "elem_min": emin, "elem_max": emax,
                    "per_hit_mid": phys_mid + elem_mid_hit, "damaging": dmg, "flags": flags})
        if sname in NONDAMAGING:
            out["note"] = "declared non-damaging (MinDam/MaxDam are parameters of a curse / ally heal)"
        if out["stream"]:
            out["per_frame_mid"] = out["per_hit_mid"]
            out["per_second_mid"] = out["per_hit_mid"] * 25
            out["note"] = "stream/field damage: per_hit_mid is PER FRAME of contact; excluded from per-landed-hit figures"
        return out

    result = {"law": "LoD 1.13 Hell players-1", "hell_monster_skill_bonus": bonus, "rules": {}}
    for rk, R in d2["rules"].items():
        rows = []
        for r in R["rows"]:
            m = ms[r["id"]]
            skills = []
            for k in range(1, 9):
                sn = (m.get(f"Skill{k}") or "").strip()
                lv = i(m.get(f"Sk{k}lvl"))
                if sn and lv > 0 and sn in sk:
                    sd = skill_damage(sn, lv + bonus, r["attacks"])
                    sd["mode"] = m.get(f"Sk{k}mode", "")
                    skills.append(sd)
            melee = [p["total_mid"] for p in r["per_attack"].values()]
            sk_hit = [s["per_hit_mid"] for s in skills if s["damaging"] and not s["stream"]]
            all_hits = [x for x in melee + sk_hit if x and x > 0]
            rows.append({"id": r["id"], "alvl": r["alvl"], "slot_weight": r["slot_weight"],
                         "melee_best_mid": r["max_attack_total_mid"],
                         "skills": skills,
                         "skill_best_hit_mid": max(sk_hit) if sk_hit else None,
                         "best_hit_mid_all_attacks": max(all_hits) if all_hits else None,
                         "mean_hit_mid_all_damaging_attacks": (sum(all_hits) / len(all_hits)) if all_hits else None,
                         "stream_skills_per_second": {s["skill"]: s["per_second_mid"] for s in skills if s["stream"] and s["damaging"]}})
        def wrep(field):
            rep = []
            for x in rows:
                if x[field] is not None:
                    rep += [x[field]] * x["slot_weight"]
            return q(rep)
        result["rules"][rk] = {
            "rows": rows,
            "dist_equal": {f: q([x[f] for x in rows]) for f in ("melee_best_mid", "skill_best_hit_mid",
                                                               "best_hit_mid_all_attacks", "mean_hit_mid_all_damaging_attacks")},
            "dist_slot": {f: wrep(f) for f in ("best_hit_mid_all_attacks", "mean_hit_mid_all_damaging_attacks")},
            "n_types": len(rows),
            "n_types_with_damaging_skill_hit": sum(1 for x in rows if x["skill_best_hit_mid"]),
            "n_types_with_stream_skill": sum(1 for x in rows if x["stream_skills_per_second"]),
        }
    out.write_text(json.dumps(result, indent=1))
    for rk, R in result["rules"].items():
        e = R["dist_equal"]
        f = lambda d: "None" if d is None else f"{d['median']:.0f} [{d['p25']:.0f}-{d['p75']:.0f}] ({d['min']:.0f}-{d['max']:.0f})"
        print(rk, "types", R["n_types"], "w/ skill hit", R["n_types_with_damaging_skill_hit"], "w/ stream", R["n_types_with_stream_skill"])
        for k, v in e.items():
            print("   ", k, f(v))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else PKT / "d2_skill_damage.json")
