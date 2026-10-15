import json, hashlib, pathlib, importlib.util, sys, collections
C = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration")
E = pathlib.Path("/Users/admin/Games/reincarnated-engine")
BFp = C / "legolas/research/2026-10-14-join1-c14-sorc-build-file/build_file_standard_verbatim.json"
SHp = C / "legolas/research/2026-10-14-join1-c14-sorc-build-file/sorc_build_sheet.json"
STp = C / "gamora/analyses/2026-10-14-join1-j4b-d2-stamping/stamping_table.json"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
BF = json.loads(BFp.read_text())["profile"]
names = {"36": "Fire Bolt", "37": "Warmth", "40": "Frozen Armor", "41": "Inferno", "42": "Static Field", "43": "Telekinesis",
         "46": "Blaze", "47": "Fire Ball", "51": "Fire Wall", "52": "Enchant", "54": "Teleport", "56": "Meteor", "61": "Fire Mastery"}
skills = {names[k]: v for k, v in BF["skills"].items()}
prog = collections.Counter(names[k] for k in BF["skillProgression"])
hard = {k: skills[k] + prog.get(k, 0) for k in skills}
st = {r["numeric_key"]: r["source_value"] for r in json.loads(STp.read_text())["rows"]}
st_ok = all(st[f"v_hardpoints_skill{int(k):03d}"] == v for k, v in BF["skills"].items())
SH = json.loads(SHp.read_text())["sheets"]["charms_BO"]
bonus = {k: SH["slvl"][k] - SH["hard_points_verbatim"][k] for k in SH["slvl"]}
slvl = {k: hard[k] + bonus[k] + 1 for k in SH["slvl"]}
spec = importlib.util.spec_from_file_location("v4f", E / "src/reincarnated/export/kc2_rulebook_pack_v4_final.py")
M = importlib.util.module_from_spec(spec); sys.modules["v4f"] = M; spec.loader.exec_module(M)
K = M.load_layer(E / "src/reincarnated/output/kc2-rulebook-pack-v4-20261014_233315", M.KIT, config="JOIN")
pack_blvl = {k[5:]: v["value"] for k, v in K.items() if k.startswith("blvl.")}
pack_slvl = {k[5:]: v["value"] for k, v in K.items() if k.startswith("slvl.")}
snake = lambda s: s.lower().replace(" ", "_")
res = {
    "ruling": "KP-444 (collab 2e679e429): skillProgression IS SPENT; hard points = profile.skills + skillProgression (110)",
    "inputs": {"build_file_standard_verbatim.json": sha(BFp), "sorc_build_sheet.json (stage 5, live)": sha(SHp),
               "stamping_table.json (gamora v2, 591ebde87)": sha(STp)},
    "profile_skills_sum": sum(skills.values()), "skillProgression_n": len(BF["skillProgression"]), "skillProgression": dict(prog),
    "hard_points_KP444": hard, "hard_points_sum": sum(hard.values()),
    "stamping_v2_hardpoint_rows_equal_profile_skills": st_ok,
    "pack_blvl_equals_KP444": all(pack_blvl[snake(k)] == v for k, v in hard.items()),
    "slvl_rederived_from_stage5_sheet_bonus_plus_KP444_hard_plus_BC1": {k: slvl[k] for k in ("Fire Bolt", "Inferno", "Enchant", "Fire Ball", "Meteor", "Fire Mastery", "Warmth", "Frozen Armor", "Static Field", "Teleport")},
    "pack_slvl_equals_rederived": all(pack_slvl[snake(k)] == slvl[k] for k in pack_slvl and [] or ("Fire Bolt", "Inferno", "Enchant", "Fire Ball", "Meteor", "Fire Mastery", "Warmth", "Frozen Armor", "Static Field", "Teleport")),
    "synergies_KP444": {"fire_ball_pct": 14 * (hard["Fire Bolt"] + hard["Meteor"]), "meteor_pct": 5 * (hard["Fire Bolt"] + hard["Fire Ball"]),
                        "burning_ground_pct": 3 * hard["Inferno"]},
    "pack_synergies": {"fire_ball": K["fire_ball"]["value"]["synergy_pct"], "meteor": K["meteor"]["value"]["synergy_pct"],
                       "meteor_pyre": K["meteor_pyre"]["value"]["synergy_pct"]},
}
res["pack_synergies_equal"] = list(res["pack_synergies"].values()) == list(res["synergies_KP444"].values())
print(json.dumps(res, indent=1))
