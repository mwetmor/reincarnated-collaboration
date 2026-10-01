# R-C9-119: the battle mage's character slot with the NEW props (variant C = bmc119, D = bmd119), derived from
# scene_pkg/character_sorceress_battlemage.json. Regenerate, don't edit.   python3 s54_make_pkg119.py
import json, copy
S = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/gear_sets/sorceress_battlemage'
src = json.load(open(S + '/scene_pkg/character_sorceress_battlemage.json'))
m = json.load(open(S + '/props119/mount/mount.json'))
carry = json.load(open(S + '/work/book_carry_L.json'))
for var in ("bmc119", "bmd119"):
    ch = copy.deepcopy(src)
    ch.update({
        "model": "res://models/sorceress_%s/so-body_bm119.glb" % var,
        "gear_dir": "res://models/sorceress_%s" % var,
        "clips_armed": dict(src["clips_armed"], attack="cast_fireball_m"),
        "casts": {"cast_fireball_m": {"slot": "attack", "release_s": 0.9, "socket": "cast_hand_R"},
                  "cast_meteor": {"slot": "chop", "release_s": 1.6333, "socket": "cast_hand_meteor"},
                  "_note": ("R-C9-119: the Fire Ball is MIRRORED (s46) so the WAND hand throws and the book stays open in the left; "
                            "release_s re-derived on the mirrored clip's RIGHT hand (its fastest forward interval ends at 0.9000 s; "
                            "the original's left hand at 0.9333 -- one key, the rig's 2.3 cm rest asymmetry)")},
        "morph_rules": {"grip_R_wand": "wand", "grip_L_book": "grimoire", "under_battlemage": "gown"},
        "_morph_note": ("grip_R_wand closes her right fist through the wand's grip (to 33 mm round its 23 mm leather grip); "
                        "grip_L_book cups the left fingers under the book's spine (to 32 mm). The GAUNTLETS carry both keys too: "
                        "set each key on every worn mesh that has it."),
        "armed_when_pieces": ["wand"],
        "arm_layer_armed": {"action": "book_carry_L", "bones": ["LeftArm", "LeftForeArm", "LeftHand"], "weight": 1.0,
                            "when_piece": "grimoire", "clips": "ALL (idle, walk, run, cast_fireball_m, cast_meteor)",
                            "_note": ("THE BOOK HOLD: her left arm holds the open grimoire to read (hand at chest height, palm under the "
                                      "spine, the book tilted 40 deg up toward her face) through EVERY clip, the casts included -- a "
                                      "filtered Blend2 over exactly these three bones. knight.gd's left slot blends over LOCOMOTION only; "
                                      "the integration needs it over the strike one-shots too (or the book drops in the casts).")},
        "strike_release": dict(src["strike_release"], guard_throughout=[], _r119="the mirrored Fire Ball throws with the wand hand: no right-arm carry over it"),
        "book_carry_measured": {k: carry[k] for k in ("tilt_deg", "achieved_centre", "elbow_flex_deg", "wrist_deviation_deg",
                                                       "upper_arm_from_vertical_deg", "within_limits")},
        "sockets_r119": {"cast_hand_R": {"bone": "RightHand", "along_bone_m": 0.07, "what": "the wand hand's palm: the mirrored Fire Ball's spawn"},
                         "wand_tip": {"what": "the wand's crystal tip, %.3f m from the fist centre along the wand axis" % m["wand"]["crystal_tip_from_fist_m"]}},
    })
    json.dump(ch, open(S + '/scene_pkg/character_sorceress_%s.json' % var, 'w'), indent=1)
    full = dict(ch, gear_stacks=[ch["gear_stacks"][-1]], gear_stack_names=[ch["gear_stack_names"][-1]])
    json.dump(full, open(S + '/scene_pkg/character_sorceress_%s_full.json' % var, 'w'), indent=1)
    print("wrote character_sorceress_%s(.json, _full.json)" % var)
