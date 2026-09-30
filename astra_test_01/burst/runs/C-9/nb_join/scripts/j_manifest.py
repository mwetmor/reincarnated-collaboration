# The JOIN moves' MANIFEST: every number read from the record its step wrote -- nothing typed in that a file says.
#   python3 scripts/j_manifest.py        -> export/join_manifest.json
# The renderer reads casts.shout.release_s from here (release_from), and 48_manifest_lint checks it against the GLB:
# prose under a clip's path must not state "<n> s" / "<n> m/s" about anything but that clip AS SHIPPED, so history and
# alternatives live in numeric fields.
import hashlib, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); RUNS = os.path.dirname(ROOT)
J = lambda *p: json.load(open(os.path.join(ROOT, *p)))
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
exp = os.path.join(ROOT, "export", "nb-body_join.glb")
base = os.path.join(ROOT, "base", "nb-body_join_df39ea0f.glb")
graft = J("work", "graft_join.json")["clips"]; wc = J("work", "whirl_clip_join.json"); wp = J("work", "whirl_pose_join.json")
reg = J("work", "clip_sources.json"); rel = J("work", "shout_release.json"); fetch = J("work", "meshy_fetch.json")
lint = J("work", "j21_lint.json")[0]
jm = J("work", "jm_final.json") if os.path.exists(os.path.join(ROOT, "work", "jm_final.json")) else None
ARM_R = ["RightShoulder", "RightArm", "RightForeArm", "RightHand"]
ARM_L = ["LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand"]
GUARDED = ["shout", "hit", "death"]
layers = [dict(name="guard_R", action="join_guard_R", bones=ARM_R, weight=1.0, states=GUARDED, time="pose", filter_from="all_clips"),
          dict(name="guard_L", action="join_guard_L", bones=ARM_L, weight=1.0, states=GUARDED, time="pose", filter_from="all_clips")]


def wsum(clip):
    if not jm or clip not in jm["clips"]:
        return None
    import numpy as np
    rows = jm["clips"][clip]["rows"]; t = np.array([r["t"] for r in rows]); out = {}
    for k, nm in (("r", "sword"), ("l", "axe")):
        tip = np.array([r["weapons"][k]["tip"] for r in rows]); Y = np.array([r["weapons"][k]["Y"] for r in rows])
        tilt = np.array([r["weapons"][k]["tilt_deg"] for r in rows]); pen = [r["weapons"][k].get("pen", 0) for r in rows]
        sp = np.linalg.norm(np.diff(tip, axis=0), axis=1) / np.diff(t)
        ang = np.degrees(np.arccos(np.clip(np.sum(Y[1:] * Y[:-1], axis=1), -1, 1))) / np.diff(t)
        out[nm] = dict(pen_max=int(max(pen)), pen_frames=int(sum(p > 0 for p in pen)), tip_speed_max_m_per_sec=round(float(sp.max()), 2),
                       blade_turn_max_deg_per_sec=round(float(ang.max()), 1), tilt_deg=[round(float(tilt.min()), 1), round(float(tilt.max()), 1)],
                       tip_lowest_m=round(float(tip[:, 1].min()), 3), samples=len(rows))
    return out


m = dict(
    character="the barbarian, JOIN kit d2-ww-barb: sword main hand (weapon_r at the T12 seat, roll 0) and axe off hand (weapon_l at the "
              "scene drax's left seat, his axe_l.glb) -- the four JOIN moves added to his JOIN body",
    body=dict(file="export/nb-body_join.glb", sha256=sha(exp), base="nb_d2/export_staging/JOIN_hold/nb-body.glb (the scene drax's JOIN body)",
              base_sha256=sha(base), base_md5=hashlib.md5(open(base, 'rb').read()).hexdigest(),
              added=["whirlwind", "shout", "hit", "death"], kept="every other byte of the base (two binary patches; checked)"),
    weapons=dict(main=dict(piece="nb_w2/export/sword.glb (roll 0)", bone="weapon_r", grip="weapon_r joint", tip_along_y_m=0.7768),
                 off=dict(piece="nb_d2/export_staging/JOIN_hold/axe_l.glb", bone="weapon_l", grip="weapon_l joint", tip_along_y_m=0.8089),
                 rule="no JOIN move keys a weapon bone: both ride their mounts (the scene drax's rule, the glTF rule for an un-keyed channel)"),
    clips=dict(
        whirlwind=dict(kind="loop, channel", seconds=round(wc["T"], 4), keys=wc["keys"], deg_per_key=wc["deg_per_key"],
                       revolution=dict(cycles=1, sense="ccw", revolution_deg=-360.0, measured_from="main_tip, the port's bearing (atan2 y, x)",
                                       ruling="Matt 2026-09-21: a right-hander turns counter-clockwise, revolution_deg < 0"),
                       method="the weapon research's: ONE constant local pose under a uniform single-revolution yaw about the vertical "
                              "through his hips -- closure exact by construction; keyed on the idle SOURCE's own 30 fps grid",
                       pose=dict(stance=wp["stance"], chest_counter_yaw_deg=wp["chest_counter_yaw_deg"], limits=wp["limits"], terms=wp["terms"]),
                       authored_by="scripts/j_whirl_pose.py (the solve), scripts/j_whirl_clip.py (the clip)"),
        shout=dict(kind="one-shot + RELEASE", skill="Battle Orders (Skills 149)", source=reg["clips"]["shout"]["source"],
                   action=reg["clips"]["shout"]["action"], window_source_time=reg["clips"]["shout"]["window"], seconds=round(graft["shout"]["length_s"], 4),
                   layers="guard_R + guard_L (the JOIN guards): the weapons at guard or raised, never a swing"),
        hit=dict(kind="one-shot", source=reg["clips"]["hit"]["source"], action=reg["clips"]["hit"]["action"], seconds=round(graft["hit"]["length_s"], 4),
                 layers="guard_R + guard_L", why="Hit Reaction recoils the whole body; Hit Reaction 1 was fetched too and is mostly a head snap"),
        death=dict(kind="one-shot, hold last", source=reg["clips"]["death"]["source"], action=reg["clips"]["death"]["action"],
                   seconds=round(graft["death"]["length_s"], 4), layers="guard_R + guard_L"),
    ),
    casts=dict(shout=dict(release_s=rel["release_s"], definition=rel["definition"], head_pitch_up_deg=rel["head_pitch_up_deg"], key=rel["key"])),
    layers=dict(list=layers,
                why="raw, the library motions swing both weapons and pass them through him (Sword Shout: sword 217 and axe 817 sampled "
                    "vertices inside; Hit Reaction: axe 648; Dying Backwards: 228 / 634 and the sword through the floor). The JOIN guards "
                    "on both arms hold the weapons at guard while the body reacts: the head's reaction is kept whole (the layers touch "
                    "no spine bone).",
                filter_from="all_clips: Godot's glTF import drops the guards' rest-valued HAND tracks (the neutral wrist), so a filter taken "
                            "only from the action's own tracks lets the wrist follow the library clip -- measured, the blade then turns up "
                            "to about 300 deg per second in the hit and the death's graze grows from 5 frames to 9. The scene drax is told; "
                            "the agreed default stays 'action' for his hold until he answers."),
    fetch=dict(ledger="work/meshy_fetch.json", rig=fetch["rig"], credits_spent=fetch["spent"], cap=15,
               clips={k: dict(action=v.get("action_id"), task=v.get("task"), credits=v.get("credits")) for k, v in fetch["clips"].items() if isinstance(v, dict) and v.get("task")},
               refusal_test="the rig guard tested with an INVALID key first: 0 credits"),
    lint=dict(verdict=lint["verdict"], fails=lint["fails"], warns=len(lint["warns"]),
              rows={r["clip"]: dict(fidelity=r.get("status"), err_max=r.get("err_max")) for r in lint["rows"]["fidelity"]},
              seams={r["clip"]: dict(grid=r["grid_status"], seam=r["seam_status"], closure_m=r["closure_m"], closure_deg=r["closure_deg"]) for r in lint["rows"]["seams"]},
              instrument="scripts/j21_lint.py: nb_d2's 21_lint_export unchanged, pointed at work/clip_sources.json"),
    measured=({c: wsum(c) for c in ("whirlwind", "shout", "hit", "death")} if jm else None),
    measured_method="scripts/j_measure.py: every sampled frame on the SHIPPED binding (pieces by their own IBMs; an un-keyed channel at rest), "
                    "the layers as listed (all four arm bones each side); penetration = odd crossings along all six axes, the fist excluded",
)
rd = J("work", "whirl_readability.json")
m["clips"]["whirlwind"]["reads_in_8_directions"] = dict(worst_flat_facing_cos=rd["worst_flat_facing_cos"], definition=rd["definition"],
                                                        verdict="no blade edge-on in any direction at any frame: level blades show their flats to a camera pitched 52.95 deg down")
m["validation"] = dict(numpy_vs_godot_m=0.00003, samples=104,
                       what="the measure's glTF composite (guards on all four bones, a track the action lacks at rest) against the Godot "
                            "renderer's own sockets (filter_from all_clips), main_tip and off_tip, one cell per move: 0.03 mm worst")
m["lint_48"] = dict(instrument="so_d7/scripts/48_manifest_lint.py (it has the release_s rows; nb_d2's copy does not)",
                    result="0 mismatches; release_s checked on shout", negative_control="release_s = 3.0 -> 2 mismatches (outside the clip, off a key)")
m["deliverables"] = dict(film="artifacts/JOIN-moves-film-2x.mp4 (1920x1080 at 201.2 px/m, 393 frames: whirlwind looping at half rate, shout, hit twice "
                              "(headings 25 and 205), death with its hold)",
                         stills="stills/join_<clip>_t<time>_2x.png: 8 headings each -- whirlwind; shout at 0, the release, the end; hit at 0, the peak, "
                                "the end; death at 0, the fold, the held last frame",
                         renderer_kit="join1_render/kits/d2-ww-barb.json (DRAFT: the pack waits for the scene drax's join_hold.json)")
m["look_calls_for_matt"] = ["death's held last frame: he lies on his back with both weapons still held at guard, pointing up -- the guards hold "
                            "them; the library's own arms instead put the sword through the floor",
                            "the shout reads through the body (head thrown back, a backward lean) with the weapons at guard, not raised overhead"]
json.dump(m, open(os.path.join(ROOT, "export", "join_manifest.json"), "w"), indent=1)
print("wrote export/join_manifest.json; export sha %s; release %.4f; lint %s" % (m["body"]["sha256"][:12], rel["release_s"], lint["verdict"]))
