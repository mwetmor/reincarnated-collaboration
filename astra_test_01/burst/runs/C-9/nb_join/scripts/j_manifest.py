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
moves_only = os.path.join(ROOT, "export", "nb-body_join_b5371921_moves_only.glb")
HOLD_DIR = os.path.join(RUNS, "nb_d2", "export_staging", "JOIN_hold")
base = os.path.join(HOLD_DIR, "nb-body.glb"); hold_p = os.path.join(HOLD_DIR, "join_hold.json"); hold = json.load(open(hold_p))
graft = J("work", "graft_join.json")["clips"]; wc = J("work", "whirl_clip_join.json"); wp = J("work", "whirl_pose_join.json")
reg = J("work", "clip_sources.json"); rel = J("work", "shout_release.json"); fetch = J("work", "meshy_fetch.json")
lint = J("work", "j21_lint.json")[0]
layers = J("work", "layers_moves.json"); clamp = J("work", "death_clamp.json"); rp = J("work", "raise_pose.json")
fps = J("work", "runtime_resample.json")
E = sha(exp)
MEAS = {"whirlwind": "jm_whirl_ship.json", "shout": "jm_rulings.json", "shout_raised": "jm_shout_raised84.json", "hit": "jm_rulings.json",
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
              "scene drax's left seat, his axe_l.glb) -- the four JOIN moves and the shout's raised variant added to his JOIN body",
    body=dict(file="export/nb-body_join.glb", sha256=E,
              base="nb_d2/export_staging/JOIN_hold/nb-body.glb (the scene drax's JOIN body: T12_10 + weapon_l seated for the axe + the six per-state guards)",
              base_sha256=sha(base), base_md5=md5(base), hold_spec="nb_d2/export_staging/JOIN_hold/join_hold.json", hold_spec_sha256=sha(hold_p),
              added=["whirlwind", "shout", "hit", "death", "shout_raise"],
              built=["scripts/j_assemble.py: the three grafts (nb_d2's 55_clip_graft + deroot) and the whirlwind on the base -> "
                     "export/nb-body_join_b5371921_moves_only.glb",
                     "scripts/j_weapon_clamp.py: the death's weapon_r / weapon_l rotation tracks (work/death_clamp.json)",
                     "scripts/j_pose_clip.py: the raised shout pose appended as the clip shout_raise (work/raise_pose.json)"],
              moves_only_sha256=sha(moves_only),
              kept="every base clip byte-identical: the grafts append; the clamp touches only the death's weapon channels"),
    weapons=dict(main=dict(piece="nb_w2/export/sword.glb (roll 0)", bone="weapon_r", grip="weapon_r joint", tip_along_y_m=0.7768),
                 off=dict(piece="nb_d2/export_staging/JOIN_hold/axe_l.glb", bone="weapon_l", grip="weapon_l joint", tip_along_y_m=0.8089),
                 rule="the whirlwind, the shout (both versions) and the hit key no weapon bone: both ride their mounts. The death keys "
                      "weapon_r and weapon_l ROTATION only (the floor clamp: each weapon turned in its grip), the mount's translation kept"),
    states=dict(
        idle=dict(clip="idle_guard", layers="the hold (join_hold.json): guard_R_idle, guard_L_idle"),
        walk=dict(clip="walk", layers="the hold: upper_walk, guard_R_walk, guard_L_walk"),
        run=dict(clip="run", layers="the hold: upper_run, guard_R_run, guard_L_run"),
        whirlwind=dict(clip="whirlwind", layers=[]),
        shout=dict(clip="shout", layers=["guard_R", "guard_L"]),
        shout_raised=dict(clip="shout", layers=["guard_R", "guard_L", "raise"], variant_of="shout",
                          note="a VARIANT for Matt's look, beside the shout: he picks one, and the other leaves the pack"),
        hit=dict(clip="hit", layers=["guard_R", "guard_L"]),
        death=dict(clip="death", layers=["guard_R_death", "guard_L_death"])),
    clips=dict(
        whirlwind=dict(kind="loop, channel", seconds=round(wc["T"], 4), keys=wc["keys"], deg_per_key=wc["deg_per_key"],
                       revolution=dict(cycles=1, sense="ccw", revolution_deg=-360.0, measured_from="main_tip, the port's bearing (atan2 y, x)",
                                       ruling="Matt 2026-09-21: a right-hander turns counter-clockwise, revolution_deg < 0"),
                       method="the weapon research's: ONE constant local pose under a uniform single-revolution yaw about the vertical "
                              "through his hips -- closure exact by construction; keyed on the idle SOURCE's own 30 fps grid",
                       pose=dict(stance=wp["stance"], chest_counter_yaw_deg=wp["chest_counter_yaw_deg"], limits=wp["limits"], terms=wp["terms"],
                                 reused="work/whirl_pose_join.json: the base's idle and both weapon mounts are the same as the pose was solved on"),
                       authored_by="scripts/j_whirl_pose.py (the solve), scripts/j_whirl_clip.py (the clip)"),
        shout=dict(kind="one-shot + RELEASE", skill="Battle Orders (Skills 149)", source=reg["clips"]["shout"]["source"],
                   action=reg["clips"]["shout"]["action"], window_source_time=reg["clips"]["shout"]["window"], seconds=round(graft["shout"]["length_s"], 4),
                   layers="guard_R + guard_L (the idle guards): the weapons at guard; the raised version is states.shout_raised"),
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
        shout_raise=dict(kind="pose (2-key STEP), read at its frame 0 by the layer 'raise'", authored_by="scripts/j_raise_pose.py + scripts/j_pose_clip.py",
                         record="work/raise_pose.json", solved_on=dict(clip=rp["clip"], t_s=rp["t"], under=rp["under"]), cost=rp["cost"], terms=rp["terms"],
                         constraints="grips >= 0.08 m over the top of his head and 0.20 m out from his centre line; blades within 25 deg of "
                                     "vertical leaning OUT (a V); every blade point >= 0.22 m from his head and >= 0.25 m from the other "
                                     "weapon; wrist <= 50 deg, elbow 10-70, clavicle <= 35 from the pose under it")),
    variants=dict(shout_raised=dict(of="shout", clip="shout", layers=["guard_R", "guard_L", "raise"],
                                    raise_curve=LAY["raise"]["weight_curve"]["keys"], at_release=near("shout_raised", rel["release_s"]),
                                    ruling="the conductor, 2026-09-30: both weapons lifted high over the release, at the cry's peak, 0 penetration; "
                                           "the current shout kept beside it; Matt picks at his look")),
    casts=dict(shout=dict(release_s=rel["release_s"], definition=rel["definition"], head_pitch_up_deg=rel["head_pitch_up_deg"], key=rel["key"],
                          applies_to=["shout", "shout_raised"])),
    layers=dict(list=layers, format="join-hold-layers/1 (the scene drax's), bottom to top, matched on the pack STATE name",
                hold=dict(spec="nb_d2/export_staging/JOIN_hold/join_hold.json", layers=[ly["name"] for ly in hold["layers"]], states=hold["states"]),
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
                       "it -- done: states.shout_raised (the layer 'raise'); states.shout unchanged"),
    fetch=dict(ledger="work/meshy_fetch.json", rig=fetch["rig"], credits_spent=fetch["spent"], cap=15,
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
m["locomotion_in_place"]["method"] = ("so_d7/scripts/s18_footlock_contact.py on the hold's own body (nb_d2/export_staging/JOIN_hold/nb-body.glb): "
                                      "the FOOT-LOCK speed by the SCENE's stance rule (the integration drax's t12_10_feet instrument) -- the "
                                      "stance side is the lower toe within 0.03 m of its lowest, the speed that side's foot joint's backward "
                                      "speed, the median over the clip's own key intervals, both feet pooled. For the pack's stride_m_per_cycle "
                                      "(REPORTED per the contract)")
m["locomotion_in_place"]["correction"] = ("the first pack index used s6_footlock's rule (a foot planted in the bottom 25%% of the ankle's own "
                                          "height range; s6_rule_was): it reads a run's landing and lift-off as stance and read his run about "
                                          "%.0f%% slow, so the run's stride was understated by as much. The walk agrees under both rules"
                                          % (100 * (1 - fs6["run"]["foot_lock_speed_m_s"] / fc_["run"]["estimators"][SC_]["keys"]["backward_median"])))
rd = J("work", "whirl_readability.json")
m["clips"]["whirlwind"]["reads_in_8_directions"] = dict(worst_flat_facing_cos=rd["worst_flat_facing_cos"], definition=rd["definition"],
                                                        verdict="no blade edge-on in any direction at any frame: level blades show their flats to a camera pitched 52.95 deg down")
vp = os.path.join(ROOT, "work", "j_validate_pack.json")
if os.path.exists(vp):
    v = json.load(open(vp))
    m["validation"] = {k: v[k] for k in ("what", "pack_raw", "states", "worst_m", "samples") if k in v}
m["lint_48"] = dict(instrument="so_d7/scripts/48_manifest_lint.py (it has the release_s rows; nb_d2's copy does not)",
                    result_file="work/j48_lint.txt")
m["deliverables"] = dict(stills="stills/join2_<state>_t<time>_2x.png: 8 headings each -- the death at the guards' release, mid-fold, the "
                                "landing and the held last frame; shout_raised rising, at the release and lowering; the shout (guard) at the "
                                "release beside it",
                         film="artifacts/JOIN-moves-film-2x-rulings.mp4 (1920x1080 at 2x, 582 frames: the whirlwind looping at half rate; the "
                              "shout, then the shout_raised variant, heading 25; the hit at headings 25 and 205; the death at headings 115 and "
                              "295 with its hold)",
                         pack="join1_pack_draft/d2-ww-barb/matrix_index.json (kit join1_render/kits/d2-ww-barb.json; 8 states x 8 directions, "
                              "64 cells) and join1_pack_draft/d2-ww-barb_contact_sheet_1x.png")
m["look_calls_for_matt"] = [
    "SHOUT: two versions side by side -- 'shout' (weapons held at guard; the cry reads through the body, head thrown back) and "
    "'shout_raised' (both weapons lifted high over his head through the cry, a V, and lowered after). Pick one; the other leaves "
    "the pack.",
    "DEATH (ruled): the guards let go through the fall, the arms go slack with the library motion, and both weapons come to rest "
    "ON the floor beside his hands (measured.death: nothing into him or the floor at any key; the held last frame's lowest points "
    "on the floor)."]
fl = m["measured"]["death"]["sword"]
json.dump(m, open(os.path.join(ROOT, "export", "join_manifest.json"), "w"), indent=1)
print("wrote export/join_manifest.json; export sha %s; release %.4f; lint %s; death sword pen %d at %d keys, floor %.4f m"
      % (E[:12], rel["release_s"], lint["verdict"], fl["pen_max"], fl["pen_keys"], fl["floor_lowest_m"]))
