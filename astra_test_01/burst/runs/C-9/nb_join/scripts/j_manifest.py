# The JOIN moves' MANIFEST: every number read from the record its step wrote -- nothing typed in that a file says.
#   python3 scripts/j_manifest.py        -> export/join_manifest.json
# The renderer reads casts.shout.release_s from here (release_from), and 48_manifest_lint checks it against the GLB:
# prose under a clip's path (or naming a clip) must not state "<n> s" / "<n> m/s" about anything but that clip AS
# SHIPPED, so times, history and alternatives live in NUMERIC fields (a weight curve's keys, a flick's t_s).
#
# Refuses a stale record: every measurement must name the export's own sha256, the clamp record the sha of the GLB it
# clamped, and the scene drax's hold spec the md5 of the body this export was built on.
import hashlib, json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); RUNS = os.path.dirname(ROOT)
J = lambda *p: json.load(open(os.path.join(ROOT, *p)))
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()
exp = os.path.join(ROOT, "export", "nb-body_join.glb")
moves_only = os.path.join(ROOT, "export", "nb-body_join_cf7ceb43_moves_only.glb")       # R-C9-115: rebased on the JOIN hold v4 (this lane's)
HOLD_DIR = os.path.join(ROOT, "export_hold_v4")
base = os.path.join(HOLD_DIR, "nb-body.glb"); hold_p = os.path.join(HOLD_DIR, "join_hold.json"); hold = json.load(open(hold_p))
graft = J("work", "graft_join.json")["clips"]
w2, w2c, w2p, w2l = J("work", "whirl_v2.json"), J("work", "whirl_v2_check.json"), J("work", "whirl_v2_pose.json"), J("work", "whirl_v2_library_try_check.json")
w1c = J("work", "whirl_v1_check.json"); wcr, wcl = J("work", "warcry_v6.json"), J("work", "warcry_v6_clamp.json"); wc4 = J("work", "warcry_v4.json"); xc = J("work", "cross_check_shout.json")
wc5 = J("work", "warcry_v5.json"); xw = J("work", "cross_check_whirlwind.json"); w4v = J("work", "whirl_v4_check.json")
w3, w3c, w3p = J("work", "whirl_v3.json"), J("work", "whirl_v3_check.json"), J("work", "whirl_v3_pose.json")
w4, w4c, w4p = J("work", "whirl_v8.json"), J("work", "whirl_v8_check.json"), J("work", "whirl_v8_pose_A.json")    # v8 (the names kept)
w7c = J("work", "whirl_v7_check.json"); tipF25, tipF40, tipF30 = J("work", "hold_v4_tip_F25.json"), J("work", "hold_v4_tip_F40.json"), J("work", "hold_v4_tip_F30.json")
atk, atkx, atkc = J("work", "attack_a1_candidate.json"), J("work", "cross_check_attack_candidate.json"), J("work", "attack_a1_candidate_clamp.json")
w7b, w7bx, w7bj = J("work", "whirl_v7_B_check.json"), J("work", "cross_check_whirlwind_v7B.json"), J("work", "joint_lint_whirlwind_v7B.json")
w6c = J("work", "whirl_v6_check.json")
xw5 = J("work", "cross_check_whirlwind_v5.json")
wc3 = J("work", "warcry_v3.json"); jl = J("work", "joint_lint.json")
wc2 = J("work", "warcry_v2.json")
reg = J("work", "clip_sources.json"); fetch = J("work", "meshy_fetch.json")
lint = J("work", "j21_lint.json")[0]
layers = J("work", "layers_moves.json"); clamp = J("work", "death_clamp.json")
fps = J("work", "runtime_resample.json")
E = sha(exp)
MEAS = {"whirlwind": "jm_whirl_ship.json", "shout": "jm_rulings.json", "hit": "jm_rulings.json",
        "death": "jm_rulings_death68.json"}
meas = {}
for st, f in MEAS.items():
    d = J("work", f)
    if d.get("body_sha256") != E:
        sys.exit("STALE: work/%s measured %s, the export is %s" % (f, str(d.get("body_sha256"))[:12], E[:12]))
    meas[st] = d["clips"][st]
if clamp.get("body_sha256") != sha(moves_only):
    sys.exit("STALE: work/death_clamp.json clamped %s, not %s" % (str(clamp.get("body_sha256"))[:12], os.path.basename(moves_only)))
if hold["body"]["md5"] != md5(base):
    sys.exit("STALE: join_hold.json names body md5 %s, the base is %s" % (hold["body"]["md5"], md5(base)))
ARM = {"r": "sword", "l": "axe"}
LAY = {ly["name"]: ly for ly in layers}


def wsum(st):
    rec = meas[st]; rows = rec["rows"]; t = np.array([r["t"] for r in rows]); out = dict(samples=len(rows), clip=rec["clip"])
    for k, nm in ARM.items():
        W = [r["weapons"][k] for r in rows]
        tip = np.array([w["tip"] for w in W]); Y = np.array([w["Y"] for w in W]); tilt = np.array([w["tilt_deg"] for w in W])
        low = np.array([w["lowest_y"] for w in W]); pen = [w.get("pen", 0) for w in W]
        sp = np.linalg.norm(np.diff(tip, axis=0), axis=1) / np.diff(t)
        ang = np.degrees(np.arccos(np.clip(np.sum(Y[1:] * Y[:-1], axis=1), -1, 1))) / np.diff(t); ia = int(ang.argmax())
        out[nm] = dict(pen_max=int(max(pen)), pen_keys=int(sum(p > 0 for p in pen)), pen_tested_max=int(max(w.get("pen_tested", 0) for w in W)),
                       pen_at_t_s=[round(float(t[i]), 4) for i, p in enumerate(pen) if p > 0],
                       floor_lowest_m=round(float(low.min()), 4), floor_lowest_at_t_s=round(float(t[int(low.argmin())]), 4),
                       tip_speed_max_m_per_sec=round(float(sp.max()), 2),
                       blade_turn_max_deg_per_sec=round(float(ang.max()), 1), blade_turn_max_between_t_s=[round(float(t[ia]), 4), round(float(t[ia + 1]), 4)],
                       tilt_deg=[round(float(tilt.min()), 1), round(float(tilt.max()), 1)], tip_lowest_m=round(float(tip[:, 1].min()), 3),
                       tip_highest_m=round(float(tip[:, 1].max()), 3),
                       last=dict(t_s=round(float(t[-1]), 4), lowest_m=round(float(low[-1]), 4), tilt_deg=round(float(tilt[-1]), 1)))
    return out


def near(st, ts):
    rows = meas[st]["rows"]; r = min(rows, key=lambda r_: abs(r_["t"] - ts))
    return dict(t_s=r["t"], **{nm: dict(tip_y_m=round(r["weapons"][k]["tip"][1], 3), grip_y_m=round(r["weapons"][k]["grip"][1], 3),
                                        tilt_deg=r["weapons"][k]["tilt_deg"]) for k, nm in ARM.items()})


m = dict(
    character="the barbarian, JOIN kit d2-ww-barb: sword main hand (weapon_r at the T12 seat, roll 0) and axe off hand (weapon_l at the "
              "scene drax's left seat, his axe_l.glb) -- the four JOIN moves added to his JOIN body; the war cry and the whirlwind are v4 "
              "(Matt, 2026-09-30)",
    body=dict(file="export/nb-body_join.glb", sha256=E,
              base="nb_d2/export_staging/JOIN_hold_v2/nb-body.glb (the scene drax's JOIN body v2, b91df5a7a: the weapon fists out to about 0.78 of the shoulder half-width; only the six guard clips differ from v1)",
              base_sha256=sha(base), base_md5=md5(base), hold_spec="nb_d2/export_staging/JOIN_hold_v2/join_hold.json", hold_spec_sha256=sha(hold_p),
              added=["whirlwind", "shout", "hit", "death"],
              built=["scripts/j_assemble.py: the three grafts (nb_d2's 55_clip_graft + deroot) and the whirlwind on the base -> "
                     "export/nb-body_join_b5371921_moves_only.glb",
                     "scripts/j_weapon_clamp.py: the death's weapon_r / weapon_l rotation tracks (work/death_clamp.json)",
                     "v2: scripts/j_whirl3.py wrote the whirlwind (authored, work/whirl_v2.json); scripts/j_warcry.py wrote the shout "
                     "(composed from Meshy 388 + 49, work/warcry_v2.json) and dropped the v1 clip shout_raise; scripts/j_weapon_clamp.py "
                     "keyed the shout's weapon_r / weapon_l rotation tracks (work/warcry_v2_clamp.json)",
                     "v3: scripts/j_whirl4.py wrote the whirlwind (a feet-on-ground pivot, work/whirl_v3.json; arms from "
                     "scripts/j_whirl_pose.py, work/whirl_v3_pose.json); scripts/j_warcry.py wrote the shout trimmed to one elbow drop "
                     "(work/warcry_v3.json); scripts/j_weapon_clamp.py re-keyed its weapon tracks (work/warcry_v3_clamp.json)",
                     "v4 REBASE (the conductor, 2026-09-30): scripts/j_carry_clips.py carried hit and death (unclamped) from the v1 "
                     "moves-only file onto the v2 hold body -> export/nb-body_join_9346f3de_moves_only.glb (the node layouts asserted "
                     "identical); scripts/j_weapon_clamp.py re-clamped the death against the v2 guards (work/death_clamp.json); "
                     "scripts/j_whirl5.py wrote the whirlwind v4 (work/whirl_v4.json; arms work/whirl_v4_pose.json); scripts/j_warcry.py "
                     "--speed 1.5 wrote the shout v4 (work/warcry_v4.json); scripts/j_weapon_clamp.py its weapon tracks "
                     "(work/warcry_v4_clamp.json)"],
              moves_only_sha256=sha(moves_only),
              kept="every base clip byte-identical: the grafts append; the clamp touches only the death's weapon channels"),
    weapons=dict(main=dict(piece="nb_w2/export/sword.glb (roll 0)", bone="weapon_r", grip="weapon_r joint", tip_along_y_m=0.7768),
                 off=dict(piece="nb_d2/export_staging/JOIN_hold_v2/axe_l.glb (byte-identical to v1's)", bone="weapon_l", grip="weapon_l joint", tip_along_y_m=0.8089),
                 rule="the whirlwind and the hit key no weapon bone: both ride their mounts. The death and the shout key weapon_r and "
                      "weapon_l ROTATION only (each weapon turned in its grip: the death's to the floor, the shout's clear of him), the "
                      "mount's translation kept"),
    states=dict(
        idle=dict(clip="idle_guard", layers="the hold (join_hold.json): guard_R_idle, guard_L_idle"),
        walk=dict(clip="walk", layers="the hold: upper_walk, guard_R_walk, guard_L_walk"),
        run=dict(clip="run", layers="the hold: upper_run, guard_R_run, guard_L_run"),
        whirlwind=dict(clip="whirlwind", layers=[]),
        shout=dict(clip="shout", layers=["guard_R_shout", "guard_L_shout"]),
        hit=dict(clip="hit", layers=["guard_R", "guard_L"]),
        death=dict(clip="death", layers=["guard_R_death", "guard_L_death"])),
    clips=dict(
        whirlwind=dict(kind="loop, channel", version=8, seconds=round(w4["cycle"]["T"], 4), keys=w4["cycle"]["keys"],
                       revolution=dict(cycles=1, sense="ccw", revolution_deg=w4c["revolution_deg"], measured_from="main_tip, the port's bearing (atan2 y, x)",
                                       rev_per_s=w4["cycle"]["rev_per_s"], ruling="Matt 2026-09-21: a right-hander turns counter-clockwise, revolution_deg < 0"),
                       v8=dict(ruling="R-C9-115 (+ R-C9-108's recipe)", what="v7's recipe exactly (one stance frame, the same A 15/15 arm "
                               "edits, a rigid spin at 3.75 rev/s, no solver) taken from the JOIN hold v4 F25 stance (the weapon tips 25 deg more forward)",
                               pose="work/whirl_v8_pose_A.json", before=w4p["before"], after=w4p["after"],
                               edges_flats_now=dict(edges=w4c["edges"], flats_to_camera=w4c["flats_to_camera"]),
                               edges_flats_v7=dict(edges=w7c["edges"], flats_to_camera=w7c["flats_to_camera"]),
                               note="measured only: the forward tips did NOT improve the edge / flat rows -- they worsened (the sword's lead "
                                    "0.66 -> 0.58, the axe still trails; worst flat 0.03 -> 0.01): a forward-pitched guard spun about the "
                                    "vertical presents its flats edge-on to more headings"),
                       v7=dict(ruling="R-C9-108", direction="Matt: 'The arms are crazy in the whirlwind v6. Please ultra think through how we "
                                                             "can simply use a slightly extended version of the current battle stance'",
                               recipe="NO SOLVER: one frame of his battle stance (the JOIN hold v3 idle: idle_guard at its half-second mark + the hold's "
                                      "guard layers at weight 1); both arms extended by two edits, mirrored -- the upper arm raised forward "
                                      "about his shoulder line, the elbow opened about its own hinge -- every other bone untouched, the hand "
                                      "and weapon riding with the forearm; the whole character spun rigidly (scripts/j_whirl7_pose.py, "
                                      "scripts/j_whirl5.py --no-head)",
                               variant_A=dict(shoulder_deg=15, elbow_deg=15, shipped=True, before=w4p["before"], after=w4p["after"],
                                              no_crossed_arms=dict(verdict=xw["verdict"], screen_frames_failing=xw["screen_frames_failing"], least_side_m=xw["least_side_m"])),
                               variant_B=dict(shoulder_deg=25, elbow_deg=25, shipped=False, pose="work/whirl_v7_pose_B.json",
                                              joint_limits=w7bj["moves"]["whirlwind"]["verdict"], no_crossed_arms=w7bx["verdict"],
                                              penetration="0 (work/jm_whirl_v7B.json)", edges=w7b["edges"], flats_to_camera=w7b["flats_to_camera"]),
                               stance_pose="work/whirl_v7_pose_stance.json",
                               contract_rows_now_failing=dict(edges=w4c["edges"], flats_to_camera=w4c["flats_to_camera"],
                                                              why="measured, not tuned (the ruling): the battle stance holds the weapons for "
                                                                  "a guard, not for a spin -- an X, the hafts up and outboard -- so the sword's "
                                                                  "edge leads at cos 0.66 and the axe's edge TRAILS (cos -0.79), and from some "
                                                                  "headings a blade is seen edge-on (worst |flat . view| 0.03 sword, 0.13 axe); "
                                                                  "the stance frozen without the edits measures the same (0.71 / -0.83; 0.08 / 0.15)"),
                               v6_for_comparison=dict(edges=w6c["edges"], flats_to_camera=w6c["flats_to_camera"])),
                       v6=dict(direction="Matt 2026-09-30: 'Whirlwind speed is good but the arms are crossed'; the conductor: each hand "
                                         "at about his shoulder half-width along the shoulder line, forearms roughly parallel, never converging; "
                                         "blades out front, a shallow V, never converging",
                               instrument=dict(script="scripts/j_cross_check.py v2", added="elbows on their own sides, and a SCREEN test: the "
                                               "forearms and blades projected through the play camera at the 8 headings, FAIL if any pair "
                                               "crosses (forearm x forearm, forearm x the other blade, blade x blade)",
                                               v5_now=dict(verdict=xw5["verdict"], screen_frames_failing=xw5["screen_frames_failing"],
                                                           elbow_least_side_m=xw5["least_side_m"]["elbow_R"],
                                                           why="v5's elbows sat ON his centreline (right elbow -0.01 m) with the wrists 0.13 m "
                                                               "out: the forearms crossed in an X in front of his chest; v1 of the check saw only "
                                                               "the wrists and passed it"),
                                               record="work/cross_check_whirlwind_v5.json"),
                               no_crossed_arms=dict(verdict=xw["verdict"], least_side_m=xw["least_side_m"], screen_frames_failing=xw["screen_frames_failing"],
                                                    record="work/cross_check_whirlwind.json"),
                               pose="j_whirl_pose.py --fist-side 1.0 (the FIST -- the weapon joint -- at his shoulder half-width along "
                                    "the levelled shoulder line: the JOIN hold v3's width, 75e4d79db, measured in this frame its fists average "
                                    "1.01) --elbow-side-min 0.65 --forearm-par 0.06 (forearms roughly parallel) --splay 8 (each blade 8 deg "
                                    "out) --edge-min 0.995",
                               fist_side_measured="(the v6 record: work/whirl_v6_pose.json, terms.*.grip_side / half_w)",
                               fist_1_15_variant=dict(pose="work/whirl_v6_pose_fist1.15_variant.json", note="solved with --grip-y-w 600: the "
                                                      "fists measure 1.16, grips at 1.20 m (raised), flats >= 0.515; one rebuild with "
                                                      "scripts/j_whirl5.py if Matt picks 1.15"),
                               tradeoff="at 1.0 the solver cannot also raise the grips to 1.20 m: they sit at 1.01-1.03 m and the flats' worst "
                                        "is 0.466 (v4-v6a: >= 0.5)"),
                       v5=dict(direction="Matt 2026-09-30 (his notes on 'the war cry' v4 were meant for the whirlwind): no crossed "
                                         "arms; the feet just his battle stance / idle; faster",
                               no_crossed_arms=dict(verdict=xw["verdict"], least_side_m=xw["least_side_m"], record="work/cross_check_whirlwind.json",
                                                    v4_was="left wrist 0.025 m from his centreline (in front of his sternum): v4 matched "
                                                           "the hold's FIST fraction, measured along the Spine bone's own axis, which is "
                                                           "twisted against his shoulder line; v5 holds each grip 0.16-0.22 m off the "
                                                           "shoulder midpoint in the shoulder frame (j_whirl_pose.py --grip-side)"),
                               feet="his idle_guard stance exactly (the solved pose takes its legs from idle_guard at its half-second mark, turned rigidly)",
                               speed=dict(v4_rev_per_s=3.0, v5_rev_per_s=w4["cycle"]["rev_per_s"],
                                          why="1.25x, not 1.2x: a loop on the 30 fps grid is 9 keys (3.75 rev/s) or 10 (3.33); 1.2x "
                                              "(3.6 rev/s) is 8.33 frames"),
                               v4_check=dict(edges=w4v["edges"], flats_to_camera=w4v["flats_to_camera"])),
                       direction=("Matt 2026-09-30, on v3: a normal battle stance with normal planted feet and normal arms at about "
                                  "shoulder width; the balls-of-the-feet spin did not look great; the blade tilt bent the elbows backwards; "
                                  "the spin about 3x faster; the blades pointed more upward, about halfway between v3's outstretched "
                                  "arms and a normal battle stance, not completely out"),
                       method=w4["method"], params=w4["params"],
                       authored_by="scripts/j_whirl7_pose.py on the JOIN hold v4 F25 body (the pose, no solver: work/whirl_v8_pose_A.json), scripts/j_whirl5.py --no-head (the spin)",
                       stance=dict(clip="idle_guard (his battle stance), its pose at the half-second mark", feet="both flat and planted where the stance puts "
                                   "them; the whole body turns as one (the conductor: accepted)", chest="squared to his forward (Spine02)"),
                       arms=dict(rule="v7: the stance's own arms, each extended by two edits (see v7); no solver",
                                 earlier="v4-v6 solved the arms per target (work/whirl_v4_pose.json, whirl_v5_pose.json, whirl_v6_pose.json)",
                                 sword_double_edged="the sword is double-edged (nb_w2/scripts/w5_measure.py): the checker reads either edge"),
                       head=dict(rule="v7: the stance's own head, untouched (j_whirl5.py --no-head)", **w4["head"]),
                       checked=dict(instrument="scripts/j_whirl_check.py --double-edged weapon_r (work/whirl_v8_check.json)", closure_m=w4c["closure_m"],
                                    hips_orbit_m=w4c["hips_orbit_m"], edges=w4c["edges"], flats_to_camera=w4c["flats_to_camera"]),
                       joint_limits=jl["moves"]["whirlwind"],
                       v3_for_comparison=dict(record="work/whirl_v3_check.json", seconds=round(w3["cycle"]["T"], 4), ball_orbit=w3["ball_orbit"],
                                              edges=w3c["edges"], why_replaced="Matt: the balls-of-feet spin; the blade tilt bent the elbows "
                                                                              "backwards (the joint lint: right elbow -36 deg, hyperextended)"),
                       v2_for_comparison=dict(record="work/whirl_v2_check.json", planted_slide=w2c["planted_slide"],
                                              scene_rule_stance_slide=w2c["stance_slide"], head_vs_travel_deg=w2c["head_vs_travel_deg"],
                                              why_replaced="Matt: the paddle-turn footwork read badly; the head spotting read badly"),
                       v1_for_comparison=dict(record="work/whirl_v1_check.json", scene_rule_stance_slide=w1c["stance_slide"],
                                              head_vs_travel_deg=w1c["head_vs_travel_deg"],
                                              why="v1 turned one constant pose on a turntable: its feet circled with it"),
                       library_tried=dict(clips=["Meshy 238 Axe Spin Attack", "Meshy 91 Double Blade Spin"], script="scripts/j_whirl2.py",
                                          record="work/whirl_v2_library_try.json", check="work/whirl_v2_library_try_check.json",
                                          stance_slide=w2l["stance_slide"], edges=w2l["edges"], hips_orbit_m=w2l["hips_orbit_m"],
                                          why_not="238 is a single pivot-and-kick attack: the body orbits the pivot foot and the trail leg "
                                                  "swings 0.5 m high; looped and foot-locked its feet still slid and the orbit sent the "
                                                  "blades along their own length. 91 kneels, leaps and travels 2 m. So the footwork is "
                                                  "authored with IK, as the dispatch's fallback allows")),
        shout=dict(kind="one-shot + RELEASE", version=6, skill="Battle Orders (Skills 149)", seconds=round(wcr["T"], 4), keys=wcr["keys"],
                   v6=dict(direction="Matt 2026-09-30 after v5: 'a bit too fast on the warcry.. and the hands weren't crossed, and the "
                                     "feet should just be whatever battle stance/idle is.. I meant to provide all of those recommendations "
                                     "for whirlwind'", arms="v4's (the v5 blade turn from the first key and the wrist cap dropped)",
                           speed="v4's 1.5x (the speed he approved)", legs="v5's: idle_guard held, planted",
                           v5_for_comparison=dict(record="work/warcry_v5.json", seconds=wc5["T"], release_s=wc5["release"]["t_s"])),
                   direction="Matt 2026-09-30 (v5): his arms are crossed now, and the legs are a bit too wide of a stance; speed it up even a "
                             "bit more. (v4: stop earlier -- lower the elbows and then end it, no fist pumps; about 1.5x speed)",
                   legs=dict(source=wcr.get("legs_from"), why="his battle stance (idle_guard), held: the library flex clip's straddle was "
                                                              "0.56 m side to side; the stance's feet are 0.30 m apart across his facing, "
                                                              "staggered; planted, no slide"),
                   no_crossed_arms=dict(instrument=xc["instrument"], verdict=xc["verdict"], least_side_m=xc["least_side_m"], tips_crossed_at_t=xc["tips_crossed_at_t"],
                                        screen_crossings_at_t=[t_ for t_, _ in xc["screen_crossings"]],
                                note="v6 restores v4's arms on purpose (Matt: the hands were not crossed): the WRISTS and elbows stay on "
                                     "their own sides; during the fling from guard the BLADES cross on screen (the check's v2 screen test "
                                     "FAILs those keys) exactly as in v4 -- reported to the conductor, not changed here",
                                        definition=xc["definition"], record="work/cross_check_shout.json",
                                        fix="the blades turned up and OUT from the first key (v4: only through the flex), each turn capped "
                                            "inside the joint lint's wrist limits; his guard held at full weight over the fling's first four "
                                            "keys (layers.list guard_*_shout), where the v4-timed fling leaned the sword tip 0.12 m across him"),
                   v4_for_comparison=dict(record="work/warcry_v4.json", seconds=wc4["T"], release_s=wc4["release"]["t_s"], speed=wc4.get("speed")),
                   speed=wcr.get("speed"), authored_time_maps=wcr.get("authored"),
                   v3_for_comparison=dict(record="work/warcry_v3.json", seconds=wc3["T"], release_s=wc3["release"]["t_s"], flex_map=wc3["flex_map"]),
                   v2_for_comparison=dict(record="work/warcry_v2.json", seconds=wc2["T"], flex_map=wc2["flex_map"]),
                   sources=reg["clips"]["shout"]["sources"], composed_by="scripts/j_warcry.py --speed 1.5 --legs-from idle_guard@0.5 (work/warcry_v6.json)",
                   time_maps=dict(flex=wcr["flex_map"], sky=wcr["sky_map"], sky_weight=wcr["sky_weight"]),
                   head_back_deg=wcr["head_back_deg"], weapons_up_and_out=wcr["weapons_up_and_out"],
                   layers="guard_R_shout + guard_L_shout: his idle guards at the start and the end only (weight curve), so he rises out of "
                          "his guard and settles back into it",
                   joint_limits=jl["moves"]["shout"],
                   weapon_clamp=dict(record="work/warcry_v6_clamp.json", clamped_keys=wcl["clamped_keys"], restored=wcl["smoothing"]["restored"],
                                     inside_after_max=wcl["inside_after_max"])),
        hit=dict(kind="one-shot", source=reg["clips"]["hit"]["source"], action=reg["clips"]["hit"]["action"], seconds=round(graft["hit"]["length_s"], 4),
                 layers="guard_R + guard_L", why="Hit Reaction recoils the whole body; Hit Reaction 1 was fetched too and is mostly a head snap"),
        death=dict(kind="one-shot, hold last", source=reg["clips"]["death"]["source"], action=reg["clips"]["death"]["action"],
                   seconds=round(graft["death"]["length_s"], 4),
                   layers="guard_R_death + guard_L_death: the idle guards, blended OUT across the fall by their weight curves "
                          "(layers.list: the keys are [t_s, weight]), so his arms go slack with the library motion",
                   guards_out_curve=LAY["guard_R_death"]["weight_curve"]["keys"],
                   weapon_clamp=dict(record="work/death_clamp.json", instrument="scripts/j_weapon_clamp.py", clamped_glb_sha256=clamp["body_sha256"],
                                     params=clamp["params"], keys=clamp["keys"], clamped_keys=clamp["clamped_keys"],
                                     inside_after_max=clamp["inside_after_max"], lowest_after_min_m=clamp["lowest_after_min"],
                                     restored=clamp["smoothing"]["restored"], smoothing=clamp["smoothing"]["method"],
                                     what="each weapon PIVOTS IN ITS GRIP, per key, by the smallest turn that puts its lowest point on the floor "
                                          "(y 0) and no tested vertex inside his posed body; keyed as weapon_r / weapon_l rotation tracks on the "
                                          "death's own keys, the mount's translation kept -- so the last frame is a dead man with his weapons "
                                          "fallen beside his hands")),
    ),
    casts=dict(shout=dict(release_s=wcr["release"]["t_s"], definition=wcr["release"]["definition"], key=wcr["release"]["key"],
                          fists_over_head_m=wcr["release"]["fists_over_head_m"])),
    layers=dict(list=layers, format="join-hold-layers/1 (the scene drax's), bottom to top, matched on the pack STATE name",
                hold=dict(spec="nb_d2/export_staging/JOIN_hold_v2/join_hold.json", layers=[ly["name"] for ly in hold["layers"]], states=hold["states"]),
                weight_curve="ADDITIVE to the agreed format: {keys: [[t, w], ...]} on the base clip's time, smoothstep between keys, held beyond "
                             "the ends; the blend amount is weight x curve(t). A layer without one is at its weight throughout "
                             "(render_cells.gd _curve, j_film.gd _curve, j_measure.py curve -- one rule in all three)",
                blend_rule="Godot's: filtered Blend2 nodes bottom to top, then the AnimationMixer accumulating each contribution relative "
                           "to the bone's rest (rot = rest . prod slerp(I, rest^-1 . q_k, w_k)). It equals slerp(clip, layer, w) only at "
                           "w 0 and 1; in a weight curve's ramp the two differ by centimetres. scripts/j_blend.py reproduces it for the "
                           "measure and the clamp (validation: the renderer's own sockets).",
                filter_from="all_clips: every listed bone is filtered; a bone the action lacks blends to REST (Godot's glTF import drops "
                            "rest-valued tracks -- the guards' neutral wrist -- so a filter from the action's own tracks lets the wrist "
                            "follow the library clip). The scene drax's hold uses the same rule",
                why="raw, the library motions swing both weapons and pass them through him (Sword Shout: sword 217 and axe 817 sampled "
                    "vertices inside; Hit Reaction: axe 648; Dying Backwards: 228 / 634 and the sword through the floor). The guards hold "
                    "the weapons while the body reacts: the head's reaction is kept whole (the layers touch no spine bone)."),
    rulings=dict(by="the conductor (gandalf), 2026-09-30, on the two look calls of bd118a67d",
                 death="a corpse holding both weapons up at guard reads as a bug: blend BOTH guard layers out across the fall (the arms go "
                       "slack with the library motion); a weapon floor clamp turns weapon_r and weapon_l so blades and hafts lie ON the "
                       "ground, not through it -- done: layers guard_R_death / guard_L_death + clips.death.weapon_clamp",
                 shout="build a variant with both weapons lifted high over the release, 0 penetration; keep the current version beside "
                       "it -- done then; SUPERSEDED by Matt's v2 direction (below)",
                 v2=dict(by="Matt, 2026-09-30, relayed by the conductor (R-C9-92)",
                         war_cry="raised, arms wider, an obviously muscle-flexing motion: arms outstretched to the sky, then pumping muscles "
                                 "with a slight elbow lower during the pump -- done: clips.shout (v2), replacing shout and shout_raised",
                         whirlwind="a double baseball swing, a battle stance, good footwork that shows a real spin, the head following "
                                   "the direction of travel -- done then: clips.whirlwind (v2); SUPERSEDED by v3"),
                 v3=dict(by="Matt, 2026-09-30, relayed by the conductor",
                         war_cry="keep the raise, the shout and the first elbow drop; remove the pumps after it -- done then: clips.shout (v3); "
                                 "SUPERSEDED by v4",
                         whirlwind="weapons held out in front, blades angled into the spin; the footwork by text to animation or a "
                                   "feet-on-ground pivot; the head toward the blades, tilted toward the spin -- done: clips.whirlwind (v3), "
                                   "the pivot (text-to-motion not run: refused by the session's permission system)",
                         hands="the weapon hands out toward shoulder width, not crossed in (the guards and the hold are the scene drax's)"),
                 tips_forward=dict(ruling="R-C9-115", said="Get the axe and sword's blade/tip pointed more forward. That should be needed for "
                                   "all attacks and walking/running stance and carry forward to whirlwind as well",
                                   done="the JOIN hold v4 F25 (this lane: export_hold_v4/, scripts/j_hold_tip.py) -- the body's six guard "
                                        "poses rebased onto it (idle / walk / run layers, and the guards of hit, death and the war cry); "
                                        "the whirlwind v8 from its stance"),
                 whirlwind_v7=dict(by="Matt, 2026-09-30; the conductor's ruling R-C9-108", said="The arms are crazy in the whirlwind v6 ... "
                                   "simply use a slightly extended version of the current battle stance",
                                   done="clips.whirlwind (v7, variant A): one stance frame + two arm edits + a rigid spin; no solver"),
                 whirlwind_v6=dict(by="Matt, 2026-09-30, relayed by the conductor", said="Whirlwind speed is good but the arms are crossed",
                                   done="clips.whirlwind (v6): wrists at the shoulder half-width, forearms opening outward, blades a shallow V"),
                 v6=dict(by="Matt, 2026-09-30, relayed by the conductor: his v5 notes were for the whirlwind",
                         war_cry="v4's arms and speed (1.5x), v5's battle-stance legs -- done: clips.shout (v6)",
                         whirlwind="no crossed arms, the feet his idle stance, faster -- done: clips.whirlwind (v5), 3.75 rev/s"),
                 v5=dict(by="Matt, 2026-09-30, relayed by the conductor",
                         war_cry="no crossed arms, a narrower stance, a bit faster -- done: clips.shout (v5) at 1.8x, his battle-stance "
                                 "legs, the wrists and blade tips on their own sides at every key (clips.shout.no_crossed_arms)"),
                 v4=dict(by="Matt, 2026-09-30, relayed by the conductor",
                         war_cry="stop earlier: the elbows lowered, then end -- no pumps; about 1.5x speed -- done: clips.shout (v4), "
                                 "played at 1.5x (clips.shout.seconds; the authored timing in clips.shout.authored_time_maps); release_s re-derived on the new keys",
                         whirlwind="a normal battle stance, feet flat and planted, arms at about shoulder width, natural elbows; the blades "
                                   "pitched up about halfway to the guard; no tilt at wrist or elbow; about 3x faster -- done: clips.whirlwind "
                                   "(v4), three revolutions per second",
                         joint_limits="a JOINT LIMITS lint row for every move this lane owns -- done: scripts/j_joint_lint.py, "
                                      "work/joint_lint.json, joint_limits on each clip",
                         rebase="onto the JOIN hold v2 body 9346f3de (b91df5a7a); idle, walk and run re-rendered from it")),
    fetch=dict(ledger="work/meshy_fetch.json", rig=fetch["rig"], credits_spent=fetch["spent"], cap_per_task=15,
               v2_task=dict(credits=sum((fetch["clips"][k].get("credits") or 0) for k in ("wc_flex_show_muscles", "wc_motivational_cheer",
                                                                                         "ww_axe_spin_attack", "ww_double_blade_spin")),
                            cap=15, clips=["wc_flex_show_muscles (388)", "wc_motivational_cheer (49)", "ww_axe_spin_attack (238)", "ww_double_blade_spin (91)"]),
               clips={k: dict(action=v.get("action_id"), task=v.get("task"), credits=v.get("credits")) for k, v in fetch["clips"].items() if isinstance(v, dict) and v.get("task")},
               refusal_test="the rig guard tested with an INVALID key first: 0 credits", rulings_spend=0),
    lint=dict(verdict=lint["verdict"], fails=lint["fails"], warns=len(lint["warns"]),
              rows={r["clip"]: dict(fidelity=r.get("status"), err_max=r.get("err_max")) for r in lint["rows"]["fidelity"]},
              seams={r["clip"]: dict(grid=r["grid_status"], seam=r["seam_status"], closure_m=r["closure_m"], closure_deg=r["closure_deg"]) for r in lint["rows"]["seams"]},
              new_warns=[w for w in lint["warns"] if "'whirlwind'" in w or "'shout" in w or "'hit'" in w or "'death'" in w],
              instrument="scripts/j21_lint.py: nb_d2's 21_lint_export unchanged, pointed at work/clip_sources.json"),
    runtime_resampling=fps,
    measured={st: wsum(st) for st in MEAS},
    measured_method="scripts/j_measure.py on the export (each record names its sha256): every sampled frame on the SHIPPED binding "
                    "(pieces by their own IBMs; an un-keyed channel at rest), the layers as listed at weight x weight_curve(t), blended by "
                    "Godot's mixer rule (scripts/j_blend.py), rotation keys slerped; "
                    "penetration = odd crossings along all six axes, every 4th weapon vertex, the grip in the fist excluded; the floor "
                    "is y 0 (floor_lowest_m: a weapon's lowest vertex, negative = below it)",
)
fc_ = J("work", "footlock_contact_walk_run.json"); fs6 = J("work", "footlock_walk_run.json")["clips"]
SC_ = "scene: stance by the lower toe (3 cm), that side's ANKLE speed"
m["locomotion_in_place"] = {c: dict(seconds=round(fc_[c]["seconds"], 4), speed_m_s=fc_[c]["estimators"][SC_]["keys"]["backward_median"],
                                    stance_intervals=fc_[c]["estimators"][SC_]["keys"]["samples"],
                                    dense_60hz=fc_[c]["estimators"][SC_]["dense"]["backward_median"],
                                    s6_rule_was=fs6[c]["foot_lock_speed_m_s"])
                            for c in ("walk", "run")}
m["locomotion_in_place"]["method"] = ("so_d7/scripts/s18_footlock_contact.py on the hold's own body (nb_d2/export_staging/JOIN_hold/nb-body.glb, v1; its walk and run clips are identical in v2): "
                                      "the FOOT-LOCK speed by the SCENE's stance rule (the integration drax's t12_10_feet instrument) -- the "
                                      "stance side is the lower toe within 0.03 m of its lowest, the speed that side's foot joint's backward "
                                      "speed, the median over the clip's own key intervals, both feet pooled. For the pack's stride_m_per_cycle "
                                      "(REPORTED per the contract)")
m["locomotion_in_place"]["correction"] = ("the first pack index used s6_footlock's rule (a foot planted in the bottom 25%% of the ankle's own "
                                          "height range; s6_rule_was): it reads a run's landing and lift-off as stance and read his run about "
                                          "%.0f%% slow, so the run's stride was understated by as much. The walk agrees under both rules"
                                          % (100 * (1 - fs6["run"]["foot_lock_speed_m_s"] / fc_["run"]["estimators"][SC_]["keys"]["backward_median"])))
m["clips"]["whirlwind"]["reads_in_8_directions"] = dict(worst_flat_facing_cos=w4c["flats_to_camera"],
                                                        definition="|flat normal . view| over the 8 contract directions and 120 samples a "
                                                                   "cycle (scripts/j_whirl_check.py)")
vp = os.path.join(ROOT, "work", "j_validate_pack.json")
if os.path.exists(vp):
    v = json.load(open(vp))
    m["validation"] = {k: v[k] for k in ("what", "pack_raw", "states", "worst_m", "samples") if k in v}
m["lint_48"] = dict(instrument="so_d7/scripts/48_manifest_lint.py (it has the release_s rows; nb_d2's copy does not)",
                    result_file="work/j48_lint.txt")
m["deliverables"] = dict(stills="stills/join5_<clip>_t<time>_2x.png and _1x.png: 8 headings each -- the war cry at its sky and its "
                                "elbow drop, the whirlwind through its revolution",
                         films=["artifacts/JOIN-v4-moves-film-2x.mp4 (play speed: the war cry, the whirlwind looping, 2 headings)",
                                "artifacts/JOIN-v4-moves-film-2x-quarter.mp4 (the same at a quarter speed)"],
                         war_cry_v5=dict(film="artifacts/JOIN-v5-warcry-film-2x.mp4 (play speed, 2 headings)", stills="stills/join6_shout_t<sky 0.3, drop 0.9667, settle 1.1667>_1x/_2x.png, 8 headings"),
                         v6=dict(films=["artifacts/JOIN-v6-warcry-film-2x.mp4", "artifacts/JOIN-v5-whirlwind-film-2x.mp4"], stills="stills/join7_* (8 headings)"),
                         whirlwind_v6=dict(film="artifacts/JOIN-v6-whirlwind-film-2x.mp4", stills="stills/join8_whirlwind_* (8 headings)", compare="artifacts/JOIN-whirlwind-v5-vs-v6-heading1-t0.png"),
                         whirlwind_v7=dict(sheet="artifacts/JOIN-whirlwind-v7-stance-A-B-8headings.png (frozen)", film="artifacts/JOIN-v7-whirlwind-A-then-B-film-2x.mp4"),
                         hold_v4=dict(sheet="artifacts/JOIN-hold-v4-tips-forward-v3-F25-F40-8headings.png"), whirlwind_v8=dict(film="artifacts/JOIN-v8-whirlwind-film-2x.mp4"),
                         timing=["artifacts/JOIN-timing-wc-authored-vs-D2-law.mp4", "artifacts/JOIN-timing-at-authored-vs-D2-law.mp4"],
                         pack="join1_pack_draft/d2-ww-barb/matrix_index.json -- DRAFT; whirlwind and shout re-rendered, shout_raised retired")
m["look_calls_for_matt"] = [
    "WAR CRY v6: v4's arms and blades at v4's 1.5x (1.40 s), on his battle-stance legs held and planted.",
    "WHIRLWIND v8: v7's recipe from the hold v4 F25 stance (the tips 25 deg more forward) -- spun as one at 3.75 rev/s.",
    "HOLD v4 F25 (R-C9-115): both weapon tips swung 25 deg toward his forward at the wrist, in idle, walk and run."]
m["hold_v4"] = dict(ruling="R-C9-115", spec="nb_join/export_hold_v4/join_hold.json", tool="scripts/j_hold_tip.py",
                    tip_forward_definition=tipF25["forward"] + ": the angle between each weapon's grip->tip axis and it",
                    v3=tipF25["v3"], F25=tipF25["out"], F40=tipF40["out"], F30=tipF30["out"],
                    verdicts=dict(F25="PASS: wrist 25 deg off neutral (<= 30), weapons >= 0.34 m apart, j_cross_check v2 PASS in idle / walk / run, joint lint PASS",
                                  F40="FAILS the 30-deg wrist rule (40 deg off neutral); its gap, cross check and joint lint pass",
                                  F30="the most forward that passes the wrist rule at the wrist alone (30 deg)"),
                    fists="moved inward by the wrist turn (the grip sits 0.09 m off the wrist): idle R 0.84 -> 0.69, L 1.18 -> 1.01 of the half-width",
                    records=["work/hold_v4_tip_F25.json", "work/hold_v4_tip_F40.json", "work/hold_v4_tip_F30.json", "work/cross_check_hold_v4_*.json", "work/joint_lint_hold_v4_*.json"])
m["normal_attack_candidate"] = dict(status="NOT SHIPPED: it fails j_cross_check v2 (the conductor: stop and report)",
                                    route="Route 1, 0 credits: chop_overhead_92 (Meshy 92) trimmed to its single chop + held, start and end in the hold v4 guard",
                                    tool="scripts/j_attack.py", record="work/attack_a1_candidate.json", contact=atk["contact"],
                                    cross_check=dict(verdict=atkx["verdict"], screen_frames_failing=atkx["screen_frames_failing"], keys=atkx["keys"],
                                                     least_side_m=atkx["least_side_m"]),
                                    why="the chop is diagonal: it comes down from over his right shoulder across his body to his left hip -- the "
                                        "right wrist ends 0.30 m past his centreline, and the sword crosses the guarding axe on screen from the "
                                        "wind-up on",
                                    clamp=dict(clamped_keys=atkc["clamped_keys"], inside_after_max=atkc["inside_after_max"]))
m["joint_limits"] = dict(instrument=jl["instrument"], limits_deg=jl["limits_deg"], learned=dict(jl["learned"], axes="(in work/joint_lint.json)"),
                         moves={c: dict(verdict=r["verdict"], failing_frames=r["failing_frames"], frames=r["frames"], worst=r["worst"])
                                for c, r in jl["moves"].items()},
                         control_library={c: dict(verdict=r["verdict"], failing_frames=r["failing_frames"]) for c, r in jl["control_library"].items()},
                         negative_control=jl.get("negative_control"), record="work/joint_lint.json")
fl = m["measured"]["death"]["sword"]
json.dump(m, open(os.path.join(ROOT, "export", "join_manifest.json"), "w"), indent=1)
print("wrote export/join_manifest.json; export sha %s; release %.4f; lint %s; death sword pen %d at %d keys, floor %.4f m"
      % (E[:12], wcr["release"]["t_s"], lint["verdict"], fl["pen_max"], fl["pen_keys"], fl["floor_lowest_m"]))
