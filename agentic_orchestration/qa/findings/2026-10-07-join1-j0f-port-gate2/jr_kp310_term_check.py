"""jack-ryan, KP-310 delta Gate-2: term-for-term check of the port's computed wave/pet values against the
SEALED oracle's own functions, over the WHOLE pack table (waves 151-170, every family, every pet), not only
the graded referent.

Independent of drax's code: the port's expressions are transcribed here from the KP-310 diff (godot 256b3e4,
kc2rt_offense_fold.gd / kc2rt_v3p6p1.gd) as Python double arithmetic in the same operand order; the oracle's
values come from IMPORTING the sealed oracle (worktree of kc2/referent-v1-sealed-r2-oracle -> 969fbd8d)
unmodified, PYTHONDONTWRITEBYTECODE, and the worktree is checked clean before and after by the caller.

Also answers "does the M_dot change move anything graded": for every (wave, family) it reports whether the
old literal and the computed value give the same (om - 1.0), which is the only way M_dot enters the V311
CompositionFold DoT row (gd_composition.py:176), and separately the raw-om path (DOT_LEECH_TYPES / the
non-composition path) where no absorption occurs.

usage: PYTHONDONTWRITEBYTECODE=1 python3 -B jr_kp310_term_check.py <sealed_engine_worktree> <model_pack_dir> <out.json>
"""
import json, struct, sys, pathlib

wt, pack_dir, out_path = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3]
sys.dont_write_bytecode = True
sys.path.insert(0, wt + "/src")
from reincarnated.simulation.kc2 import offense as O          # noqa: E402
from reincarnated.simulation.kc2 import threat as T           # noqa: E402

hx = lambda x: struct.pack(">d", x).hex()


def ulps(a, b):
    ia = struct.unpack(">q", struct.pack(">d", a))[0]
    ib = struct.unpack(">q", struct.pack(">d", b))[0]
    return ib - ia


def rows_by_prefix(prefixes):
    found = {}
    for p in sorted((pack_dir / "model").glob("*.json")):
        def walk(o):
            if isinstance(o, dict):
                rid = o.get("id")
                if isinstance(rid, str) and rid.startswith(prefixes) and "value" in o:
                    found.setdefault(rid, (p.name, o))
                    return
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(json.loads(p.read_text()))
    return found


R = rows_by_prefix(("S1-DMGMULT-W", "S1-DOTMULT-W", "H2-ASW-", "H1-OAW-", "H1-OA-", "H1-CONST"))
wave_tab = O.load_wave_damage()
out = {"inputs": {"sealed_worktree": wt, "pack_dir": str(pack_dir)}, "M_inst": [], "M_dot": [],
       "ASW": [], "OAW": [], "pet_OA": [], "summary": {}}

# ---- M_inst: port 1.0 + float(sum_total_damage_modifier_pct) / 100.0 ----
for rid, (_, row) in sorted(R.items()):
    if not rid.startswith("S1-DMGMULT-W"):
        continue
    v = row["value"]; w = int(v["wave"])
    port = 1.0 + float(v["sum_total_damage_modifier_pct"]) / 100.0
    orc = wave_tab[w].instant_mult
    lit = float(v["M_inst"])
    out["M_inst"].append({"wave": w, "port": hx(port), "oracle": hx(orc), "port_eq_oracle": port == orc,
                          "literal": hx(lit), "literal_ulps_vs_oracle": ulps(orc, lit),
                          "pack_operand_eq_csv": float(v["sum_total_damage_modifier_pct"]) == wave_tab[w].sum_total_pct})

# ---- M_dot: port s = D_pct + U_offensiveSlowAllTypes_pct; 1.0 + s / 100.0 ----
for rid, (_, row) in sorted(R.items()):
    if not rid.startswith("S1-DOTMULT-W"):
        continue
    v = row["value"]; w = int(v["wave"]); u = float(v["U_offensiveSlowAllTypes_pct"])
    fams = sorted(v["per_family"])
    for fam in fams:
        cell = v["per_family"][fam]
        port = 1.0 + (float(cell["D_pct"]) + u) / 100.0
        orc = wave_tab[w].dot_mult(fam)
        lit = float(cell["M_dot"])
        out["M_dot"].append({
            "wave": w, "family": fam, "port_eq_oracle": port == orc, "port": hx(port), "oracle": hx(orc),
            "literal": hx(lit), "literal_ulps_vs_oracle": ulps(orc, lit),
            "om_minus_1_equal_literal_vs_oracle": (lit - 1.0) == (orc - 1.0),
            "operands_eq_csv": float(cell["D_pct"]) == wave_tab[w].d_dot_pct[fam] and u == wave_tab[w].u_dot_pct})
    out["summary"].setdefault("dot_family_sets", {})[str(w)] = {
        "pack": fams, "oracle_DOT_FAMILY_COLUMN": sorted(O.DOT_FAMILY_COLUMN),
        "equal": fams == sorted(O.DOT_FAMILY_COLUMN),
        "unmodified_in_pack": sorted(set(fams) & set(O.DOT_FAMILY_UNMODIFIED))}

# ---- H2 attack speed / H1-OAW adds ----
for rid, (_, row) in sorted(R.items()):
    v = row["value"]
    if rid.startswith("H2-ASW-"):
        w = int(v["wave"])
        port = 1.0 + (float(v["D_characterAttackSpeedModifier_pct"]) + float(v["U_characterAttackSpeedModifier_pct"])) / 100.0
        orc = wave_tab[w].attack_speed_mult
        out["ASW"].append({"wave": w, "port_eq_oracle": port == orc, "literal_eq_oracle": float(v["attack_speed_mult"]) == orc})
    elif rid.startswith("H1-OAW-"):
        w = int(v["wave"])
        pf = float(v["D_characterOffensiveAbility_pct"]) + float(v["U_characterOffensiveAbility_pct"])
        pm = float(v["D_characterOffensiveAbilityModifier_pct"]) + float(v["U_characterOffensiveAbilityModifier_pct"])
        out["OAW"].append({"wave": w, "flat_eq": pf == wave_tab[w].oa_flat_add, "mod_eq": pm == wave_tab[w].oa_modifier_add,
                           "literal_flat_eq": float(v["oa_flat_add"]) == wave_tab[w].oa_flat_add,
                           "literal_mod_eq": float(v["oa_modifier_add"]) == wave_tab[w].oa_modifier_add})

# ---- pet OA (threat.py:355-366, 1183-1190) ----
c = R["H1-CONST"][1]["value"]
lf, tail = float(c["OA_LEVEL_FACTOR"]), float(c["OA_FLAT_TAIL"])
out["summary"]["H1_CONST_eq_oracle"] = {"OA_LEVEL_FACTOR": lf == T.OA_LEVEL_FACTOR, "OA_FLAT_TAIL": tail == T.OA_FLAT_TAIL}
for rid, (_, row) in sorted(R.items()):
    if not rid.startswith("H1-OA-"):
        continue
    v = row["value"]; rec = str(v["record"])
    base, lvl = float(v["pet_offensive_ability"]), int(v["level"])
    p_eff = (base + 0.0 + float(lvl) * lf) * (1.0 + 0.0 / 100.0) + tail
    p_pre = base + 0.0 + float(lvl) * lf
    o_eff, o_lvl = T._pet_oa_folded(rec)
    o_pre = T.oa_pre_modifier(oa_base=float(T._f(T._pet_index().get(rec) or {}, "pet_offensive_ability") or 0.0), level=o_lvl)
    out["pet_OA"].append({"record": rec, "eff_eq": p_eff == o_eff, "pre_eq": p_pre == o_pre, "level_eq": lvl == o_lvl,
                          "literal_eff_eq": float(v["oa_eff"]) == o_eff, "oa_modifier_pct_literal": float(v["oa_modifier_pct"])})

S = out["summary"]
S["M_inst"] = {"n": len(out["M_inst"]), "port_eq_oracle": sum(r["port_eq_oracle"] for r in out["M_inst"]),
               "literal_ne_oracle_waves": [r["wave"] for r in out["M_inst"] if r["literal_ulps_vs_oracle"] != 0],
               "operand_eq_csv": sum(r["pack_operand_eq_csv"] for r in out["M_inst"])}
S["M_dot"] = {"n": len(out["M_dot"]), "port_eq_oracle": sum(r["port_eq_oracle"] for r in out["M_dot"]),
              "literal_ne_oracle": sum(r["literal_ulps_vs_oracle"] != 0 for r in out["M_dot"]),
              "literal_ulps_range": [min(r["literal_ulps_vs_oracle"] for r in out["M_dot"]),
                                     max(r["literal_ulps_vs_oracle"] for r in out["M_dot"])],
              "om_minus_1_differs_waves": sorted({r["wave"] for r in out["M_dot"] if not r["om_minus_1_equal_literal_vs_oracle"]}),
              "om_minus_1_differs_cells": [(r["wave"], r["family"]) for r in out["M_dot"] if not r["om_minus_1_equal_literal_vs_oracle"]],
              "operands_eq_csv": sum(r["operands_eq_csv"] for r in out["M_dot"])}
S["ASW"] = {"n": len(out["ASW"]), "port_eq_oracle": sum(r["port_eq_oracle"] for r in out["ASW"]),
            "literal_eq_oracle": sum(r["literal_eq_oracle"] for r in out["ASW"])}
S["OAW"] = {"n": len(out["OAW"]), "port_eq_oracle": sum(r["flat_eq"] and r["mod_eq"] for r in out["OAW"]),
            "literal_eq_oracle": sum(r["literal_flat_eq"] and r["literal_mod_eq"] for r in out["OAW"])}
S["pet_OA"] = {"n": len(out["pet_OA"]), "eff_eq": sum(r["eff_eq"] for r in out["pet_OA"]),
               "pre_eq": sum(r["pre_eq"] for r in out["pet_OA"]), "level_eq": sum(r["level_eq"] for r in out["pet_OA"]),
               "literal_eff_eq": sum(r["literal_eff_eq"] for r in out["pet_OA"]),
               "oa_modifier_pct_literal_nonzero": sum(r["oa_modifier_pct_literal"] != 0.0 for r in out["pet_OA"])}
json.dump(out, open(out_path, "w"), indent=1, sort_keys=True)
print(json.dumps(S, indent=1, sort_keys=True))
