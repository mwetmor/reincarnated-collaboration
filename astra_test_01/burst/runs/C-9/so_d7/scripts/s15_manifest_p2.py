# D7 PASS 2 manifest: the pass-1 manifest (export_p1/manifest.json, frozen) brought up to the pass-2
# build in export/, every number read from the JSON its step wrote -- nothing typed in by hand that a
# file already says.
#
#   python3 scripts/s15_manifest_p2.py            -> export/manifest.json
#
# Re-runnable: it always starts from the frozen pass-1 file, never from its own output.
#
# 2026-09-30, the JOIN-1 pack review (conductor): two fixes at the source, folded in at the end -- the run RE-CUT on
# its source's own cycle (s17_run_cycle.py; its seconds, foot-lock speed and staff acceptance re-measured) and a
# staff layer on HIT (s17_hit_*.json, s17_hit_flinch.json). Then the WALK re-cut the same way (s17_run_cycle.py
# --clip walk), and every clip's window on its source measured and noted (s17_clip_windows.py -> clip_windows).
# THEN V2 (conductor, 2026-09-30, after v1's pack was declared): the idle, hit, death and both casts re-cut the same way
# (s17_run_cycle.py --oneshot; the de-root re-derived on each new window; the Meteor's staff re-baked by s13), release_s
# re-derived on the shipped keys (s18_release.py), the staff layers re-measured (s18_*), and the walk's and run's foot-lock
# taken by the scene's stance rule (s18_footlock_contact.py) -- s6's bottom-25% ankle rule read her run 15% slow.
# History goes in NUMERIC fields: 48_manifest_lint reads
# every "<n> s" and "<n> m/s" in prose under a clip's path as a claim about the clip AS SHIPPED.
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
W = lambda *p: os.path.join(ROOT, "work", *p)
J = lambda *p: json.load(open(W(*p)))
sys.path.insert(0, HERE)
L = __import__('21_lint_export')

m = json.load(open(os.path.join(ROOT, "export_p1", "manifest.json")))
asm = J("s9_assemble_p2i.json")
wb = J("s9_weapon_bones_p2i.json")
met = J("s13_meteor_track.json")
acc = J("s12_measure_final.json")
metv = J("s13_verify.json")
metpf = J("s12_meteor_perframe.json")
ik = J("s13_ik_probe.json")
cnt = J("s11_counts_final.json")
dots = J("s11_dots_final.json")
fetch = J("meshy_fetch.json")
lint = L.lint(os.path.join(ROOT, "export", "so-body.glb"))

m["character"] = m["character"] + " -- PASS 2 (gandalf, D7 pass 2)"
m["clips"] = sorted(set(m["clips"]) | {"staff_carry_R"})
m["clip_selection"]["idle"] = "idle"
m["clip_selection"]["staff"] = "see staff_hold: T12 mount on weapon_r, filtered carry layer, grips, off-hand IK"
m["idle_swap"] = {
    "now": "Meshy library 11 'Idle 1' (fetched as idle11)",
    "was": "Meshy library 0 'Idle', which yaws the hips 96 deg over its loop -- a turn-in-place, not an idle",
    "measured": "idle11: 5 mm root travel, 5.5 deg hips yaw; two other calm idles fetched and not used (243, 249)",
    "merge": J("s6_merge_p2.json").get("idle"),
}

cs = {k: v for k, v in acc.items()}
# the run was re-cut (s17_run_cycle.py): its row is re-measured on the re-cut clip, same instrument, same carry
cs["run"] = J("s17_run_staff.json")["run"]
cs["walk"] = J("s17_walk_staff.json")["walk"]                    # and the walk, re-cut after it (same instrument)
def row(key):
    r = cs[key]
    return dict(tilt_max_deg=r["tilt_max_deg"], tip_path_px_worst=r["tip_path_px_worst"],
                staff_in_body=r["staff_in_body_worst"], staff_in_body_by_part=r["staff_in_body_by_part"])
m["staff_hold"] = {
    "method": "the T12 method (legolas Part 6): the MOUNT on weapon_r (seat + roll), an UPPER-BODY carry layer "
              "over the clips' legs/hips/root, grips by morph, off-hand TwoBoneIK3D with a per-clip enable",
    "mount": {"script": "52_weapon_bones.py --roll 0 --body so-body --weapon staff.glb",
              "seat_turn_deg": 87.6, "haft_to_hand_axis_deg": [162.1, 90.0], "fist_centroid_off_haft_m": 0.0045,
              "rest": "weapon_r rest = W: +Y along the shaft to the crown, the shaft seated in the fist CHANNEL "
                      "(gearlib.hand_frame's across-palm axis, the axis grip_R closes round)",
              "grip_along_shaft": "the MIDDLE: the staff runs -0.871 .. +0.877 m along weapon_r +Y"},
    "carry_layer": {
        "clip": "staff_carry_R",
        "how": "a FILTERED Blend2 at weight 1 -- the barbarian's armed-speed split (speedsplit_patch.py). Input 0 the "
               "clip, input 1 staff_carry_R; the filter takes each listed bone's tracks from the carry, everything "
               "else from the clip. Filter paths are taken from the clip's own tracks. A blend tree lets a node's "
               "output feed ONE input, so a second Blend2 needs its own staff_carry_R node (film/staff_layer.gd).",
        "filter_bones_full": asm["staff_carry_R"]["filter_bones"],
        "filter_bones_arm": ["RightShoulder", "RightArm", "RightForeArm", "RightHand"],
        "per_clip": {"idle": "full", "walk": "full", "run": "full",
                     "cast_fireball": "arm -- thrown from the free LEFT hand; the spine stays the clip's so the torso still drives the throw",
                     "cast_meteor": "none -- its staff motion is BAKED into the clip's own weapon_r tracks (see meteor)",
                     "hit": "none -- NOT measured", "death": "none -- NOT measured (the raw clip's staff may cross the ground)"},
        "authored": asm["staff_carry_R"]["authored"],
        "reference_impl": "film/staff_layer.gd",
    },
    "grips": {
        "grip_R": dict(asm["grips"]["grip_R"], rule="1 while the staff is held (every clip)"),
        "grip_L": dict(asm["grips"]["grip_L"], rule="1 only while the off-hand IK is ON -- i.e. never in the shipped clips"),
    },
    "off_hand_ik": {
        "node": "TwoBoneIK3D (Godot 4.6.3 settings API: set_setting_count(1), set_root/middle/end_bone_name)",
        "bones": {"root": "LeftArm", "middle": "LeftForeArm", "end": "LeftHand"},
        "end": "extend_end_bone, end_bone_length 0.07 m (wrist to palm) -- the PALM meets the shaft",
        "target": "0.25 m up the shaft from the right fist (weapon_r origin + 0.25 m along its +Y)",
        "pole": "0.30 out, 0.30 down, 0.20 back from the left elbow, in her frame",
        "enable_per_clip": {"idle": False, "walk": False, "run": False, "cast_fireball": False, "cast_meteor": False,
                            "hit": False, "death": False},
        "why_meteor_off": "the shaft is OUT OF REACH in every frame of Meshy 127: nearest shaft band %.3f m from the left "
                          "shoulder against a %.3f m arm (median %.0f%% of reach), reachable at 0 of %d frames (Blender, "
                          "world joints). Godot's own solver agrees: with the IK forced ON the palm stays %.3f-%.3f m short. "
                          "A two-handed Meteor needs a source clip in which the hands meet; the library has none chosen, "
                          "and text-to-motion is closed by T33."
                          % (min(x["shoulder_to_band_m"] for x in metpf["off_hand_to_shaft"]),
                             metpf["off_hand_to_shaft"][0]["reach_m"],
                             100 * sorted(x["shoulder_to_band_m"] / x["reach_m"] for x in metpf["off_hand_to_shaft"])[len(metpf["off_hand_to_shaft"]) // 2],
                             len(metpf["off_hand_to_shaft"]),
                             min(r["palm_short_ik_on_m"] for r in ik if r["clip"] == "cast_meteor"),
                             max(r["palm_short_ik_on_m"] for r in ik if r["clip"] == "cast_meteor")),
        "proof_it_works": "enabled where the shaft IS in reach (idle/walk/run/Fire Ball instants), the palm lands on the "
                          "target exactly (0.000 m short) -- work/s13_ik_probe.json",
        "probe": ik,
        "note": "the solved pose exists only INSIDE Skeleton3D's update: read it in `skeleton_updated`, not after",
    },
    "acceptance": {
        "rule": "tilt <= 20 deg in idle/walk/run; crown's screen path per loop <= 60 px at the play camera (worst of "
                "4 headings); no staff-body penetration (the grip region, 0.10 m round the fist, reported apart)",
        "idle": row("idle"), "walk": row("walk"), "run": row("run"),
        "verdict": "PASS" if all(cs[k]["tilt_max_deg"] <= 20 and cs[k]["tip_path_px_worst"] <= 60 and cs[k]["staff_in_body_worst"] == 0
                                 for k in ("idle", "walk", "run")) else "FAIL",
        "cast_fireball_arm_only": row("cast_fireball (STAFF ARM carry only)"),
        "cast_meteor": row("cast_meteor (raw clip, no carry)"),
        "source": "work/s12_measure_final.json (every 3rd frame); Meteor per-frame in work/s13_verify_perframe.json; "
                  "the run and the walk re-measured on their re-cut clips (2026-09-30): work/s17_run_staff.json, "
                  "work/s17_walk_staff.json",
    },
    "meteor": {
        "intent": "unchanged: Meshy 127, she raises the staff and drives it down; release_s unchanged",
        "rotation": "weapon_r track baked into cast_meteor (s13_meteor_track.py): SEATED while the fist is high (a shaft "
                    "across the raised fist clears the arm and head), turned toward UPRIGHT as the fist comes down "
                    "(w = smoothstep of fist height, shoulder -> hips), leaning %s deg to her RIGHT as she crouches "
                    "(a forward lean ran the staff through her thighs)" % met["rule"]["lean_deg"],
        "ground": "a weapon_r TRANSLATION track slides the staff up through the hand in the slam so the butt meets "
                  "the snow (at most 3 cm in) -- the fist reaches 0.22 m and the grip is mid-staff, which had put the "
                  "butt 0.62 m underground. Only in the slam: in the opening stance it stays up to 8.5 cm in the snow, "
                  "because sliding there put the butt's knob 6.8 cm into her shin (measured, then removed)",
        "turn_deg_range": [min(k["turn_deg"] for k in met["keys"]), max(k["turn_deg"] for k in met["keys"])],
        "slide_m_max": max(k["slide_m"] for k in met["keys"]),
        "remaining_contact": "grazes only: %s (per-frame, every frame)" % "; ".join(
            "%s" % x for x in ["t=0.12 s RightUpLeg 5 verts 1.13 cm", "t=0.17 s RightUpLeg 2 verts 0.49 cm",
                               "t=1.71 s LeftToeBase 2 verts 0.84 cm"]),
        "measured_inside_worst": metv["cast_meteor (raw clip, no carry)"]["staff_in_body_worst"],
        "compare": "pass 1's orientation had 638 staff verts inside her; seated throughout 103; upright throughout 32",
        "other_clips": "every other clip carries one-key weapon_r rotation and translation tracks at REST, so the staff "
                       "resets when the Meteor ends",
    },
}

byclip = {}
for k, r in cnt["per_still"].items():
    c, h, s = k.split(" ")
    byclip.setdefault(c, {"1x": 0, "2x": 0})["1x" if s == "s1" else "2x"] += r["isolated_speckle_px"]
tot = {s: sum(v[s] for v in byclip.values()) for s in ("1x", "2x")}
m["speckles"] = {
    "instrument": "scripts/s11_count.py on film/stills.gd: beauty + unshaded ID pass (body red, garments blue), 5 clips "
                  "x 4 headings (25/115/205/295) at t = 1.0 s, posed THROUGH the staff layer, 1x and 2x. A speckle = an "
                  "ISOLATED pale (min channel > 170) body patch <= 6*sc^2 px with >= 75% garment round it; patches within "
                  "2*sc px of a large visible-body region (a designed opening's edge) are reported apart",
    "scale": "a 1920x1080 OFFSCREEN SubViewport -- 100.6 px/m at 1x, 201.2 at 2x. The window cannot be 1080 rows on "
             "this 1080-line display (it clamps to 971), so every earlier pass-2 still ran at 0.90x the play scale "
             "(90.5 px/m); those numbers are superseded, not comparable",
    "isolated_pale_px": tot, "by_clip": byclip,
    "what_they_are": dots["dots"],
    "classification": "s11_dots.py: depth passes (body alone / garments alone) say whether the garment behind a dot is "
                      "within 3 cm (a POKE) or the far side of her (a GAP in the near cloth). 3D-located: the Fire Ball "
                      "gaps sit on the robe's FRONT SPLIT, the costume's own opening onto the cream underdress, which "
                      "the throw's lunge parts into a one-pixel line; the run's 2x pair are one 0.8 mm poke and one "
                      "pixel 4.9 cm from the front split's edge. Idle, walk and the Meteor: 0 at both scales",
    "fixes_this_pass": ["mesh-graph closing (--close 6) in the isolation: robe small loops 958 -> 65, mantle 1307 -> 18, belt 114 -> 6",
                        "hem overlap: every garment boundary extended along the surface (robe 6 mm, mantle/belt 4 mm)",
                        "UV SEAMS WELDED before decimation (s9_assemble WELD=1): glTF cuts a piece at every seam and the "
                        "decimator thinned each side independently, opening hairline cracks; robe verts %d -> %d before "
                        "decimation, boundary loops 215 -> 83" % (asm["welded"]["robe"]["verts_before"], asm["welded"]["robe"]["verts_after"])],
    "tried_and_rejected": {
        "under_garment_morphs": "s14_poke.py + s9_assemble --under: per-garment body morphs pulling hidden body in by the "
                                "measured poke depth (+4 mm). Measured pokes fell (idle 73 -> 28 verts), but the only "
                                "effect on the stills was one NEW isolated dot (a 3.7 mm-thin sheet of body at a vertex the "
                                "morph pulled 4.3 cm, in the Fire Ball's back view), and they cost 7.6 MB of dense morph normals. Not shipped.",
        "hem_12mm": "robe hem overlap 12 mm: the Fire Ball's front-split line closed, but new dots opened in the idle (1x 2 px, 2x 12 px)",
        "double_sided_garments": "no change to any dot: none is a culled face",
    },
}
fid = J("s16_clip_fidelity.json")
m["clip_fidelity"] = {
    "question": "does each shipped clip still move like the Meshy clip it came from? (asked after the T12 drax found "
                "nb_d2's 33_assemble action merge re-framing every bone's motion)",
    "method": "scripts/s16_clip_fidelity.py: pure glTF evaluation, every joint's position in the HIPS' own frame "
              "(which removes the root processing), divided by the rest hips-to-head in the same units",
    "result": fid,
    "verdict": "FAITHFUL: every clip within %.4f hips-to-head of its source (her clips were fetched for HER rig, so "
               "the body's rest and each clip's rest are the same, and a pose-space action move is exact)"
               % max(v["err_max"] for v in fid.values()),
}
m["gear"]["pieces"] = asm["pieces"]
m["gear"]["welded"] = asm["welded"]
m["lint"] = {"verdict": lint["verdict"], "fails": lint["fails"], "warns": len(lint.get("warns", [])),
             "warn_text": lint.get("warns", [])}
m["budget_pass2"] = {"meshy_credits": {"spent": fetch["spent"] - 33, "cap": 20, "what": "3 calm library idles x 3 (11, 243, 249)"},
                     "fal_usd": {"spent": 0.0, "cap": 0.50}, "astra": {"spent": 0, "cap": 4}}
m["film_pass2"] = {
    "files": ["artifacts/D7p2-film-playscale.mp4", "artifacts/D7p2-film-2x.mp4"],
    "plan": json.load(open(os.path.join(ROOT, "film", "shot2.json")))["plan"],
    "scale": "RENDERED at scale: 960x540 at 100.6 px/m, and 1920x1080 at 201.2 px/m over the same world extent",
    "capture": "film/film2.gd renders into an offscreen SubViewport and pipes raw frames to ffmpeg (x264, crf 16), "
               "stepping exactly 1/30 s per frame -- no Movie Maker, which records at the project window size and "
               "RESCALES the real viewport",
    "layers": "film/staff_layer.gd: carry per clip, grip_R = 1, IK wired and OFF",
    "pass1_defects_found": ["the walk played ONE second and froze: the glTF import leaves every clip LOOP_NONE and "
                            "pass 1 never set a loop mode (frames 3.5 s and 5.5 s differ by 28 px of 518,400)",
                            "pass 1's '2x' was a lanczos enlargement of the 1x pixels, not a 2x render",
                            "pass 1 was captured through a window this display cannot open at 1080 rows; its scale was "
                            "not verified then and is not claimed now"],
}

# ---- JOIN-1 pack review (conductor, 2026-09-30): the run's loop seam and hit's staff, fixed at the source ----
m["character"] = m["character"] + " + JOIN-1 pack review fixes (2026-09-30: the run and the walk re-cut on their source cycles; a staff layer on hit)"
rc, flr = J("s17_run_cycle.json"), J("s17_run_footlock.json")["clips"]["run"]
cb, ca = J("s17_closure_before.json")["run"], J("s17_closure_after.json")["run"]
fck = J("s17_footlock_check.json")
was = next(v["run"] for k, v in fck.items() if k.startswith("export_p2k/"))
now = next(v["run"] for k, v in fck.items() if k.startswith("export/"))
m["locomotion_in_place"]["run"] = {
    "seconds": round(rc["new"]["duration_s"], 4),
    "speed_m_s": flr["foot_lock_speed_m_s"],
    "planted_intervals": flr["planted_intervals"],
    "caution": "only %d planted intervals (a run's contacts are brief; interquartile spread %.3f): still the widest estimate here"
               % (flr["planted_intervals"], flr["spread_m_s"]),
    "recut": {
        "why": "the JOIN-1 pack's run cells popped at the wrap (in-figure closure 35.7 against idle and walk at about 2), and the "
               "3D game's run pops at the same wrap: the clip's last pose was not its first",
        "cause": "the D7 merge sampled Blender frames 0..18 at 24 fps from a source keyed at 30 fps whose cycle runs from its "
                 "first key to its 23rd and closes EXACTLY there. The merge began one source frame early (a clamped hold on "
                 "the first key) and stopped half a source frame before the cycle closed",
        "fix": "scripts/s17_run_cycle.py: the run re-cut on the source's own cycle -- every channel at the source's own keys "
               "(no resampling), shifted to start at 0, the last key set to the first; the Hips keep the export's constant "
               "re-ground offset; weapon_r keeps its one-key rest tracks. A binary patch of so-body.glb: every other clip, "
               "mesh and joint byte-identical (checked). The pre-re-cut export is kept in export_p2k/",
        "was": {"duration": 0.75, "keys": 19, "key_rate_fps": 24, "foot_lock_speed": was["at_keys"]["speed_m_s"],
                "planted_intervals": was["at_keys"]["intervals"]},
        "now": {"duration": round(rc["new"]["duration_s"], 4), "keys": rc["new"]["keys"], "key_rate_fps": 30,
                "source_cycle": rc["source"]["cycle_s"]},
        "closure_before": cb, "closure_after": ca,
        "closure_method": "scripts/s17_loop_closure.py: pose(0) against pose(T), every skin joint, glTF world metres",
        "fidelity": "the re-cut run IS the source's keys: 0.0000 hips-to-head from Meshy's clip at all %d (s16, aligned one "
                    "source frame in)" % rc["new"]["keys"],
        "foot_lock_sampling": "the estimator is unchanged (median backward velocity of a foot planted at both ends of an "
                              "interval) and is taken at the CLIP'S OWN KEYS -- s6_footlock now samples the action's key "
                              "times, which on every 24 fps clip are the integer frames it always sampled (walk and the "
                              "pre-re-cut run reproduce exactly). On the re-cut clip a 24 fps grid reads between its keys "
                              "and gave %.3f; a dense 480 fps sampling gives %.3f now and %.3f before: the motion's speed "
                              "did not change, only which instants were sampled (work/s17_footlock_check.json)"
                              % (now["at_24fps"]["speed_m_s"], now["dense_480"]["speed_m_s"], was["dense_480"]["speed_m_s"]),
    },
}
m["fps_note"] = ("every clip is keyed at 24 fps EXCEPT the run and the walk, which since their 2026-09-30 re-cuts carry Meshy's "
                 "own 30 fps keys (22 and 29 intervals per cycle): a 24 fps grid cannot close a cycle 17.6 or 23.2 frames long, "
                 "and the source's keys close it exactly")
m["film_pass2"]["recut_note"] = ("filmed with the pre-re-cut run and walk clips and their speeds (plan); see "
                                  "locomotion_in_place.run.recut and locomotion_in_place.walk.recut")

hl, hf, ha, hc = J("s17_hit_layers.json"), J("s17_hit_full.json"), J("s17_hit_armonly.json"), J("s17_hit_spine02arm.json")
flin, iref = J("s17_hit_flinch.json")["options"], J("s17_idle_ref.json")["idle"]
def hrow(r, fl):
    return dict(tilt_max_deg=r["tilt_max_deg"], tilt_mean_deg=r["tilt_mean_deg"], staff_in_body=r["staff_in_body_worst"],
                staff_in_body_by_part=r["staff_in_body_by_part"], tip_path_px_worst=r["tip_path_px_worst"],
                head_turn_deg=fl["head_snap_deg"], head_turn_kept=fl.get("head_snap_kept"),
                head_travel_hips_frame_m=fl["head_reaction_m"], head_travel_world_m=fl["head_world_m"], bones=fl["bones"])
opts = {"raw": hrow(hl["hit (raw clip, no carry)"], flin["raw"]), "arm": hrow(ha["hit (STAFF ARM carry only)"], flin["arm"]),
        "chest_arm": hrow(hc["hit (STAFF ARM carry only)"], flin["chest_arm"]), "full": hrow(hf["hit"], flin["full"])}
ch = m["staff_hold"]["carry_layer"]
ch["filter_bones_chest_arm"] = flin["chest_arm"]["bones"]
ch["per_clip"]["hit"] = ("chest_arm -- Spine02 + the staff arm: the staff stays inside the idle carry's lean (%.2f deg worst, "
                         "idle %.2f) while her head still turns %.0f%% as far as the raw clip's (see hit_layer_choice)"
                         % (opts["chest_arm"]["tilt_max_deg"], iref["tilt_max_deg"], 100 * opts["chest_arm"]["head_turn_kept"]))
ch["per_clip"]["death"] = ("none -- by decision (conductor, 2026-09-30): she falls with the staff. NOT measured (the raw "
                           "clip's staff may cross the ground)")
ch["hit_layer_choice"] = {
    "asked": "a staff layer on hit so the staff stays inside the idle carry's range while her body reacts; the arm-only "
             "layer if the full carry kills the flinch (conductor, JOIN-1 pack review, 2026-09-30)",
    "range": "the idle carry's lean: worst %.2f deg from vertical, mean %.2f (work/s17_idle_ref.json)" % (iref["tilt_max_deg"], iref["tilt_mean_deg"]),
    "flinch": "the upper body's own reaction -- the head's turn and travel IN THE HIPS' FRAME (scripts/s17_hit_flinch.py, every "
              "frame); the stagger of the hips and legs is the clip's under every option",
    "options": opts,
    "chosen": "chest_arm",
    "why": "the full carry kills the flinch (the head's turn goes from %.1f deg to 0) and still leans the staff %.2f deg, past "
           "the idle's, with %d staff vertices in her right leg; the arm-only layer keeps the whole flinch but leans the staff "
           "%.2f deg, about twice the idle's worst; Spine02 + the arm holds it to %.2f deg and keeps %.0f%% of the head's turn. "
           "chest_arm is a THIRD option, not one of the two named -- chosen for the stated goal, for the conductor to rule on"
           % (opts["raw"]["head_turn_deg"], opts["full"]["tilt_max_deg"], opts["full"]["staff_in_body"],
              opts["arm"]["tilt_max_deg"], opts["chest_arm"]["tilt_max_deg"], 100 * opts["chest_arm"]["head_turn_kept"]),
    "graze": "chest_arm: one sampled staff vertex 5 mm into RightLeg in ONE frame of 41 (frame 12; every frame checked, "
             "work/s17_hit_chest_arm_everyframe.txt) -- sub-pixel at the pack's 151 px/m; the nearest hit cell sample falls "
             "at frame 11.4, between a clear frame 11 and frame 12",
    "before_after": "worst angle from vertical in hit: %.2f deg raw (no layer), %.2f deg with chest_arm"
                    % (opts["raw"]["tilt_max_deg"], opts["chest_arm"]["tilt_max_deg"]),
}
m["staff_hold"]["acceptance"]["hit_chest_arm"] = {k: opts["chest_arm"][k] for k in ("tilt_max_deg", "tilt_mean_deg", "staff_in_body", "staff_in_body_by_part", "tip_path_px_worst")}
m["staff_hold"]["acceptance"]["hit_note"] = "hit is a one-shot and is not held to the loop rule; measured against the idle carry's lean (carry_layer.hit_layer_choice)"

# ---- the WALK (conductor, 2026-09-30, after the pack review): the same merge window, re-cut the same way ----
wc, flw = J("s17_walk_cycle.json"), J("s17_walk_footlock.json")["clips"]["walk"]
wcb, wca = J("s17_walk_closure_before.json")["walk"], J("s17_walk_closure_after.json")["walk"]
wfk = J("s17_walk_footlock_check.json")
wwas = next(v["walk"] for k, v in wfk.items() if k.startswith("export_p4run/"))
wnow = next(v["walk"] for k, v in wfk.items() if k.startswith("export/"))
wsrc = next(v["walk"] for k, v in wfk.items() if k.startswith("anims/"))
cw, cwb = J("s17_clip_windows.json"), J("s17_clip_windows_before.json")
m["locomotion_in_place"]["walk"] = {
    "seconds": round(wc["new"]["duration_s"], 4),
    "speed_m_s": flw["foot_lock_speed_m_s"],
    "planted_intervals": flw["planted_intervals"],
    "recut": {
        "why": "the run's merge window again, showing as a HITCH rather than a seam: the shipped walk held the source's first pose "
               "for one 30 fps source frame, so its first key interval played at a fifth of real speed once per cycle -- driven "
               "at the foot-lock speed, her planted foot skated there. Found with the run's fix; dispatched by the conductor",
        "cause": "the D7 merge sampled Blender frames 0..24 at 24 fps from a source keyed at 30 fps whose cycle runs from its "
                 "first key to its 30th and closes there. It began one source frame early (a clamped hold on the first key) and "
                 "ended exactly at the close, so the loop closed and the hold hid inside the first interval",
        "fix": "scripts/s17_run_cycle.py --clip walk: re-cut on the source's own cycle, as the run. Every channel is classified "
               "against the export first: %d faithful to the source, the Hips translation's constant re-ground offset re-applied, "
               "and the Hips SCALE kept at the export's 1 -- Meshy's walk carries a constant 1.1765 there, which the D7 hygiene "
               "stripped (clip_hygiene), and copying the source would have undone it. Every other clip, mesh and joint "
               "byte-identical (checked). The export as it stood after the run's re-cut, old walk included, is kept in "
               "export_p4run/" % wc["channels_classified"]["counts"].get("faithful", 0),
        "was": {"duration": 1.0, "keys": 25, "key_rate_fps": 24, "foot_lock_speed": wwas["at_keys"]["speed_m_s"],
                "planted_intervals": wwas["at_keys"]["intervals"], "first_interval_speed": cwb["walk"]["first_interval_speed"]},
        "now": {"duration": round(wc["new"]["duration_s"], 4), "keys": wc["new"]["keys"], "key_rate_fps": 30,
                "source_cycle": wc["source"]["cycle_s"], "first_interval_speed": cw["walk"]["first_interval_speed"]},
        "channels_classified": wc["channels_classified"]["counts"],
        "closure_before": wcb, "closure_after": wca,
        "closure_method": "scripts/s17_loop_closure.py: pose(0) against pose(T), every skin joint, glTF world metres",
        "fidelity": "the re-cut walk IS the source's keys: 0.0000 hips-to-head from Meshy's clip at all %d (s16, aligned one "
                    "source frame in)" % wc["new"]["keys"],
        "foot_lock_sampling": "at the clip's own keys (s6_footlock), %d planted intervals. Dense 480 fps sampling gives %.3f now "
                              "and %.3f before -- the held first interval pulled the old median down. Meshy's own file reads "
                              "%.3f because it still carries the 1.1765 Hips scale: %.3f / 1.1765 = %.3f "
                              "(work/s17_walk_footlock_check.json)"
                              % (flw["planted_intervals"], wnow["dense_480"]["speed_m_s"], wwas["dense_480"]["speed_m_s"],
                                 wsrc["at_keys"]["speed_m_s"], wsrc["at_keys"]["speed_m_s"], wsrc["at_keys"]["speed_m_s"] / 1.1765),
    },
}
WNOTE = {
    "idle": "Keeps the D7 merge's window: the source's first pose is held for one 30 fps source frame before its motion starts, "
            "and the clip ends one source frame before its source's cycle closes. The idle moves so little that neither shows: "
            "the loop closes to 0.6 mm (in-figure closure about 2). Left as is by decision (conductor, 2026-09-30).",
    "walk": "Re-cut on its source's own cycle (2026-09-30, s17_run_cycle.py --clip walk): no hold, and the loop closes exactly. "
            "The old walk held its first pose for one source frame, playing its first key interval at a fifth of real speed "
            "once per cycle (a hitch; see locomotion_in_place.walk.recut).",
    "run": "Re-cut on its source's own cycle (2026-09-30, s17_run_cycle.py): no hold, and the loop closes exactly. The old run "
           "began one source frame early and stopped half a frame short of its close, so it popped at the wrap (see "
           "locomotion_in_place.run.recut).",
    "hit": "Keeps the D7 merge's window: the source's first pose is held for one 30 fps source frame, so the shipped clip's "
           "first key interval plays at a fifth of real speed before the reaction runs at full speed. Harmless in a one-shot; "
           "left as is by decision (conductor, 2026-09-30).",
    "death": "Keeps the D7 merge's window: the first pose is held for one 30 fps source frame (the first key interval at a fifth "
             "of real speed), and the clip ends half a source frame before its source's last key, where she already lies "
             "still. Harmless; left as is by decision (conductor, 2026-09-30).",
    "cast_fireball": "Keeps the D7 merge's window: the first pose is held for one 30 fps source frame (the first key interval "
                     "at a fifth of real speed) and the clip ends one source frame before its source's last key. release_s "
                     "is measured on the shipped clip, so the release is unaffected. Found with the walk's re-cut, not in the "
                     "conductor's list; left as is.",
    "cast_meteor": "Keeps the D7 merge's window: the first pose is held for one 30 fps source frame (the first key interval "
                   "at a fifth of real speed) and the clip ends one source frame before its source's last key. release_s is "
                   "measured on the shipped clip, so the release is unaffected. Found with the walk's re-cut, not in the "
                   "conductor's list; left as is.",
}
m["clip_windows"] = {
    "method": "scripts/s17_clip_windows.py: each shipped clip's key window against its Meshy source -- the time map MEASURED "
              "(joints in the hips' frame, export against source at both candidate alignments), the hold at the start, the "
              "share of the first key interval that moves, the cut at the end, and loop closure. After the walk's re-cut: "
              "work/s17_clip_windows.json; before it: work/s17_clip_windows_before.json",
    "decision": "the run and the walk were re-cut (they loop, and it showed); the idle, hit, death and both casts keep the "
                "merge's window -- the idle's is sub-millimetre and a one-shot's held first interval is harmless (conductor, "
                "2026-09-30). Recorded here and carried into the JOIN-1 index as state notes, so the next reader does not "
                "re-find them",
    "clips": {c: dict(cw[c], note=WNOTE[c]) for c in cw},
}

# ---- V2 (conductor, 2026-09-30): every remaining clip on its source's own keys; release_s, staff and foot-lock re-derived ----
V2C = ("idle", "hit", "death", "cast_fireball", "cast_meteor")
rc2 = {c: J("s18_recut_%s.json" % c) for c in V2C}
rel = J("s18_release.json"); r2, r1, rsrc = rel["export/so-body.glb"], rel["export_v1pack/so-body.glb"], rel["sources"]
m["character"] = m["character"] + " + v2 (2026-09-30: every clip on its Meshy source's own 30 fps keys; release_s re-derived; the foot-lock by the scene's stance rule)"
m["v2"] = {
    "what": "the sorceress's clips v2 -- supersedes the export v1's pack was rendered from (kept in export_v1pack/ with its manifest)",
    "why": "v1's idle, hit, death and both casts were baked at 24 fps from 0 with shipped time = source time: each began with a "
           "clamped hold on the source's first key (its first key interval at a fifth of speed), and Godot's runtime glTF path "
           "re-samples every track at 30 fps, so a 24 fps clip renders as its bake (the Fire Ball's forearm 5.0 deg off its own "
           "keyed pose at the release frame, the Meteor's 3.6; nb_join/scripts/j_runtime_resample.py). On the source's own keys "
           "the bake is key-for-key",
    "recut": {c: {"mode": rc2[c]["mode"], "keys": rc2[c]["new"]["keys"], "duration": rc2[c]["new"]["duration_s"], "hips_model": rc2[c]["hips"]["model"],
                  "hips_old_window_rebuilt_worst_units": rc2[c]["hips"].get("old_window_rebuilt_worst_units"),
                  "channels": rc2[c]["channels_classified"]["counts"], "weapon_tracks_dropped_for_rebake": rc2[c]["weapon_tracks_dropped_for_rebake"],
                  "prior_accessors_byte_identical": rc2[c]["prior_accessors_byte_identical"], "record": "work/s18_recut_%s.json" % c}
              for c in V2C},
    "hips_rule": "hit and death were DE-ROOTED in the D7 hygiene (45_deroot_trim: the first-to-last line of the hips' horizontal path taken "
                 "out, the residual's mean on the rest position). s17 now finds that the old offset is that line (the old window rebuilt "
                 "from the source to within the recut records' hips_old_window_rebuilt_worst_units) and RE-DERIVES it on the new window, "
                 "so the re-cut clip's net travel is zero again; transplanting the old offsets would have left the new window's travel in. "
                 "The idle's offset is the same rule at a tenth of a millimetre; the casts' is constant (their start moved to rest)",
    "meteor_staff": "the Meteor's baked staff track was keyed on the OLD clock: kept, it would play one source frame late against the "
                    "re-cut body. Dropped and re-baked by s13_meteor_track.py on the new keys (same rule: lean 30, butt on the ground)",
    "runtime_resampling": "work/s18_runtime_resample.json: every clip passes Godot 4.6.3's runtime bake key-for-key (none re-sampled)",
}
for c in ("cast_fireball", "cast_meteor"):
    ck = m["casts"][c]
    ck["release_s"] = r2[c]["release_s"]
    ck["release_derivation"] = {
        "method": "scripts/s18_release.py: s5_casts.py's estimator (%s) on the SHIPPED clip's own keys, pure glTF evaluation"
                  % ("the leading hand's peak forward speed; release = the key ending the fastest interval" if c == "cast_fireball"
                     else "the hand's highest point over the head, then the fastest downward interval; release = its ending key"),
        "key": r2[c]["release_key"], "keys": r2[c]["keys"], "hand": r2[c]["hand"],
        "on_the_source": {"file": rsrc[c]["file"], "release_source_time": rsrc[c]["release_s"], "first_key": rsrc[c]["first_key_s"],
                          "on_the_recut_clock": rsrc[c]["release_on_recut_clock_s"]},
        "v1": {"manifest_release": 0.9167 if c == "cast_fireball" else 1.625, "same_estimator_on_v1_keys": r1[c]["release_s"],
               "why_they_differ": "s5 read the Meshy file in Blender at 24 fps integer frames and counted from frame 1 (the source's "
                                  "first key sits at frame 0.8, rounded up), so v1's number was one 24 fps frame EARLY on v1's own clip"},
    }
# the foot-lock: the scene's stance rule (s18_footlock_contact.py), at the clip's own keys, both feet pooled
flc, ref = J("s18_footlock_contact.json"), J("s18_scene_feet_ref.json")
SC = "scene: stance by the lower toe (3 cm), that side's ANKLE speed"
for c in ("walk", "run"):
    e = flc[c]["estimators"]; lk = m["locomotion_in_place"][c]
    was = lk["speed_m_s"]
    lk["speed_m_s"] = e[SC]["keys"]["backward_median"]
    lk["planted_intervals"] = e[SC]["keys"]["samples"]
    lk["foot_lock_v2"] = {
        "rule": "the stance side = the lower TOE, within 0.03 m of that toe's lowest; the speed = that side's FOOT joint's backward "
                "speed in her in-place frame; the median over the clip's own key intervals, both feet pooled -- the instrument of "
                "the integration drax's t12_10_feet (godot/tools/capture_painted.gd --feet), so the scene's ratio is 1.0 by construction",
        "keys": e[SC]["keys"], "dense_60hz": e[SC]["dense"],
        "s6_rule_was": {"speed": was, "keys": e["s6 (ankles, bottom 25%)"]["keys"], "dense_60hz": e["s6 (ankles, bottom 25%)"]["dense"]},
        "scene_measured_v1_clip": {"asked": ref["sorceress"][c]["asked_m_s"], "foot_lock": ref["sorceress"][c]["foot_lock_m_s"],
                                   "ratio": ref["sorceress"][c]["ratio_foot_lock_over_asked"], "record": ref["path"], "sha256": ref["sha256"]},
        "offline_replication_of_the_scene": round(e[SC]["dense"]["backward_median"] / ref["sorceress"][c]["foot_lock_m_s"], 4),
        "predicted_scene_ratio": round(ref["sorceress"][c]["foot_lock_m_s"] / e[SC]["keys"]["backward_median"], 3),
        "record": "work/s18_footlock_contact.json",
    }
m["locomotion_in_place"]["run"]["caution"] = ("a run's stance is short: %d stance intervals at the clip's own keys (%d at 60 Hz, which agree "
                                              "to %.1f%%)" % (flc["run"]["estimators"][SC]["keys"]["samples"], flc["run"]["estimators"][SC]["dense"]["samples"],
                                                              100 * abs(flc["run"]["estimators"][SC]["dense"]["backward_median"] / flc["run"]["estimators"][SC]["keys"]["backward_median"] - 1)))
m["locomotion_in_place"]["method"] = ("Meshy's walk and run are in place AT SOURCE, so travel over duration gives about 0. The STANCE foot slides "
                                      "back at exactly her ground speed; the median of that is the speed (v2: the scene's stance rule, "
                                      "locomotion_in_place.<clip>.foot_lock_v2)")
m["locomotion_in_place"]["why_v2"] = {
    "found": "the integration drax drove her on the phone page at v1's run speed and her stance foot moved at 1.148 times it (skating); "
             "the walk read 1.019",
    "cause": "THE MEASURE, not the clip or the in-place bake. s6_footlock counted a foot as planted in the bottom 25% of the ANKLE's "
             "own height range; a run's ankle swings high, so that band takes in the landing and the lift-off, where the ankle is "
             "not yet locked, and a dozen samples move the median with the sampling (s6_rule_was: its keys and a dense sampling "
             "differ by several percent). Stance by the lower toe (the scene's rule) isolates the locked phase; walk and run then "
             "agree dense and at the keys",
    "not_the_clip": "the run is its Meshy source's own keys (clip_fidelity 0.0000), the hips' net travel over the loop is zero "
                    "(work/s18_footlock_contact.json hips_net_travel_m)",
    "not_the_bake": "the D7 de-root removed a line of 4 mm over the run (s6_deroot_p2.json); nothing of the run's travel is left in it",
    "also_the_barbarian": "the same s6 rule is 57_footlock.py's (T12_10's gear manifest); on his JOIN body the scene's rule reads his run "
                          "about a third faster than s6's -- flagged to the lane that owns it; the JOIN pack's own stride uses the scene rule",
}
# staff: the layers re-measured on the re-cut clips (same instrument, the combined file re-cut the same way)
st = {"idle": J("s18_staff_idle.json")["idle"], "fb": J("s18_staff_fireball.json")["cast_fireball (STAFF ARM carry only)"],
      "met": J("s18_meteor_verify.json")["cast_meteor (raw clip, no carry)"], "death": J("s18_staff_death_raw.json")["death (raw clip, no carry)"]}
acc_ = m["staff_hold"]["acceptance"]
acc_["idle"] = row_ = dict(tilt_max_deg=st["idle"]["tilt_max_deg"], tip_path_px_worst=st["idle"]["tip_path_px_worst"],
                           staff_in_body=st["idle"]["staff_in_body_worst"], staff_in_body_by_part=st["idle"]["staff_in_body_by_part"])
acc_["verdict"] = "PASS" if all(acc_[k]["tilt_max_deg"] <= 20 and acc_[k]["tip_path_px_worst"] <= 60 and acc_[k]["staff_in_body"] == 0
                                for k in ("idle", "walk", "run")) else "FAIL"
acc_["cast_fireball_arm_only"] = dict(tilt_max_deg=st["fb"]["tilt_max_deg"], tip_path_px_worst=st["fb"]["tip_path_px_worst"],
                                      staff_in_body=st["fb"]["staff_in_body_worst"], staff_in_body_by_part=st["fb"]["staff_in_body_by_part"])
acc_["cast_meteor"] = dict(tilt_max_deg=st["met"]["tilt_max_deg"], tip_path_px_worst=st["met"]["tip_path_px_worst"],
                           staff_in_body=st["met"]["staff_in_body_worst"], staff_in_body_by_part=st["met"]["staff_in_body_by_part"])
acc_["death_raw_info"] = dict(tilt_max_deg=st["death"]["tilt_max_deg"], staff_in_body=st["death"]["staff_in_body_worst"],
                              staff_in_body_by_part=st["death"]["staff_in_body_by_part"],
                              note="no layer by decision (she falls with the staff); measured for the record, not held to a rule")
acc_["source"] = acc_["source"] + "; v2 (2026-09-30): idle, the Fire Ball, the Meteor and death re-measured on the re-cut clips -- work/s18_staff_*.json, work/s18_meteor_verify.json"
h2 = {"raw": J("s18_hit_raw.json")["hit (raw clip, no carry)"], "arm": J("s18_hit_arm.json")["hit (STAFF ARM carry only)"],
      "chest_arm": J("s18_hit_chest_arm.json")["hit (STAFF ARM carry only)"], "full": J("s18_hit_full.json")["hit"]}
fl2 = J("s18_hit_flinch.json")["options"]
opts2 = {k: hrow(h2[k], fl2[k]) for k in h2}
ch["hit_layer_choice"]["options"] = opts2
ch["hit_layer_choice"]["range"] = "the idle carry's lean: worst %.2f deg from vertical, mean %.2f (v2: work/s18_staff_idle.json)" % (st["idle"]["tilt_max_deg"], st["idle"]["tilt_mean_deg"])
ch["hit_layer_choice"]["v2"] = ("re-measured on the re-cut hit (the same four layers, the same instrument): chest_arm holds the staff to "
                                "%.2f deg and keeps %.0f%% of the head's turn; the choice stands" % (opts2["chest_arm"]["tilt_max_deg"], 100 * opts2["chest_arm"]["head_turn_kept"]))
ch["hit_layer_choice"]["graze"] = ("chest_arm: one sampled staff vertex 3.9 mm into RightLeg in ONE frame (every frame checked, "
                                   "work/s18_hit_chest_arm_everyframe.txt) -- sub-pixel at the pack's 151 px/m")
ch["hit_layer_choice"]["before_after"] = ("worst angle from vertical in hit: %.2f deg raw (no layer), %.2f deg with chest_arm"
                                          % (opts2["raw"]["tilt_max_deg"], opts2["chest_arm"]["tilt_max_deg"]))
ch["per_clip"]["hit"] = ("chest_arm -- Spine02 + the staff arm: the staff stays inside the idle carry's lean (%.2f deg worst, idle %.2f) while "
                         "her head still turns %.0f%% as far as the raw clip's (see hit_layer_choice)"
                         % (opts2["chest_arm"]["tilt_max_deg"], st["idle"]["tilt_max_deg"], 100 * opts2["chest_arm"]["head_turn_kept"]))
acc_["hit_chest_arm"] = {k: opts2["chest_arm"][k] for k in ("tilt_max_deg", "tilt_mean_deg", "staff_in_body", "staff_in_body_by_part", "tip_path_px_worst")}
mt2 = J("s18_meteor_track.json")
met_ = m["staff_hold"]["meteor"]
met_["turn_deg_range"] = [min(k["turn_deg"] for k in mt2["keys"]), max(k["turn_deg"] for k in mt2["keys"])]
met_["slide_m_max"] = max(k["slide_m"] for k in mt2["keys"])
met_["measured_inside_worst"] = st["met"]["staff_in_body_worst"]
met_["remaining_contact"] = "grazes only, every frame checked: two frames near the start, at most 1.3 cm (work/s18_meteor_verify_perframe.txt)"
met_["v2"] = "re-baked by s13 on the re-cut keys (%d, the source's own), the same rule and the same range as v1's bake" % len(mt2["keys"])
# windows: every clip now on its source's keys
cw2 = J("s18_clip_windows.json")
NOTE2 = ("Re-cut on its Meshy source's own keys (v2, 2026-09-30, s17_run_cycle.py%s): no held first pose (first interval x%.2f), no "
         "cut at the end, and Godot's runtime bake reproduces every key (work/s18_runtime_resample.json).")
for c in cw2:
    f_ = " --oneshot" if c in ("hit", "death", "cast_fireball", "cast_meteor") else (" --clip %s" % c if c != "run" else "")
    WNOTE[c] = NOTE2 % (f_, cw2[c]["first_interval_speed"])
WNOTE["cast_fireball"] += " release_s re-derived on these keys (casts.cast_fireball.release_derivation)."
WNOTE["cast_meteor"] += " release_s re-derived on these keys; the staff track re-baked on them (staff_hold.meteor.v2)."
m["clip_windows"] = {
    "method": m["clip_windows"]["method"] + "; v2: work/s18_clip_windows.json (before v2: work/s18_clip_windows_before.json)",
    "decision": "v2 (conductor, 2026-09-30): every clip re-cut on its source's own keys -- the run and the walk first, then the idle, "
                "hit, death and both casts",
    "clips": {c: dict(cw2[c], note=WNOTE[c]) for c in cw2},
}
m["fps_note"] = ("v2: every clip is keyed on its Meshy source's own 30 fps keys (staff_carry_R is a 2-key pose): a 24 fps grid cannot "
                 "hold a 30 fps source's keys, and Godot's runtime bake at 30 fps then reproduces each key exactly")
m["film_pass2"]["recut_note"] = ("filmed before the re-cuts (the run and walk, then v2's idle, hit, death and casts) and at the old "
                                  "speeds; see clip_windows and v2")
json.dump(m, open(os.path.join(ROOT, "export", "manifest.json"), "w"), indent=1)
print("wrote export/manifest.json: staff acceptance %s; speckles isolated pale px %s; lint %s"
      % (m["staff_hold"]["acceptance"]["verdict"], tot, lint["verdict"]))
