# D7 PASS 2 manifest: the pass-1 manifest (export_p1/manifest.json, frozen) brought up to the pass-2
# build in export/, every number read from the JSON its step wrote -- nothing typed in by hand that a
# file already says.
#
#   python3 scripts/s15_manifest_p2.py            -> export/manifest.json
#
# Re-runnable: it always starts from the frozen pass-1 file, never from its own output.
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
        "source": "work/s12_measure_final.json (every 3rd frame); Meteor per-frame in work/s13_verify_perframe.json",
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
json.dump(m, open(os.path.join(ROOT, "export", "manifest.json"), "w"), indent=1)
print("wrote export/manifest.json: staff acceptance %s; speckles isolated pale px %s; lint %s"
      % (m["staff_hold"]["acceptance"]["verdict"], tot, lint["verdict"]))
