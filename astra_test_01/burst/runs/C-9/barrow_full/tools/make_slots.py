#!/usr/bin/env python3
"""C-9 R-C9-117 -- THE OVERNIGHT VARIANTS AS CHARACTER SLOTS for the painted Barrow's select page. drax.

  python3 tools/make_slots.py            (writes godot/data/slots/*.json and copies the models to godot/models/variants/
                                           and godot/models/warlord/; the GLBs stay gitignored, as every model here)

knight.gd reads its occupant from ONE character file (its _read_cfg); every variant here is such a file, in the
installed files' own shape, pointing at its own body and gear -- the installed knight.gd, character.json, gear.gd,
foot_lock.gd and nb-body.glb are never touched. Each variant is one SLOT (scripts/slots.gd picks it from the URL):

  sorceress  armor  cur | bmc (battle mage, painted: gear_sets/sorceress_battlemage/export_v11)
                         | bmd (battle mage + steel grade: export_v12)          -- her v8 body (the under_battlemage morph)
  barbarian  armor  viking (the page's own) | gladc (champion, painted + colour grade: body_graded + export_graded)
                         | gladb (champion, painted only: body_painted + export_painted)
             hold   (none: the page's own T12_10 body) | t1211 (cliffside3d's installed T12_11) | f25l | f40l
                    (attack_lab/staged/t12_12c: the T12_12b character + the T12_12c bodies) -- WEB ONLY: nothing
                    here touches cliffside3d. These play through attack_lab/staged/t12_11/knight.gd, copied byte for
                    byte to scripts/variants/knight_t12_11.gd (the installed T12_11 knight).
  warlord    the dark knight, wl_e1/export/final_j2 (1.96 m; idle walk run (+ _unarmed) attack hit death warcry; ?eye=ice)
"""
import copy
import hashlib
import json
import pathlib
import shutil

C9 = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9")
G = C9 / "barrow_full/godot"
SL = G / "data/slots"
MV = G / "models/variants"
SL.mkdir(parents=True, exist_ok=True)
MV.mkdir(parents=True, exist_ok=True)
OUT = {}

IMPORT_BODY = """[remap]

importer="scene"
importer_version=1
type="PackedScene"

[params]

nodes/root_type=""
nodes/root_name=""
nodes/root_script=null
nodes/apply_root_scale=true
nodes/root_scale=1.0
nodes/import_as_skeleton_bones=false
nodes/use_name_suffixes=true
nodes/use_node_type_suffixes=true
meshes/ensure_tangents=true
meshes/generate_lods=true
meshes/create_shadow_meshes=true
meshes/light_baking=1
meshes/lightmap_texel_size=0.2
meshes/force_disable_compression=false
skins/use_named_skins=true
animation/import=true
animation/fps=30
animation/trimming=false
animation/remove_immutable_tracks=true
animation/import_rest_as_RESET=false
import_script/path=""
materials/extract=0
materials/extract_format=0
materials/extract_path=""
_subresources={%s}
gltf/naming_version=2
gltf/embedded_image_handling=1
"""
OPT_OFF = '\n"nodes": {\n"PATH:AnimationPlayer": {\n"optimizer/enabled": false\n}\n}\n'


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()[:8]


def put(src, dst, optimizer_off=False):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists() or md5(src) != md5(dst):
        shutil.copyfile(src, dst)
    imp = dst.with_name(dst.name + ".import")
    want = IMPORT_BODY % (OPT_OFF if optimizer_off else "")
    if not imp.exists() or "importer=\"scene\"" not in imp.read_text() or (optimizer_off and "optimizer/enabled" not in imp.read_text()):
        imp.write_text(want)
    return md5(dst)


def jload(p):
    return json.load(open(p))


def jsave(name, d):
    (SL / name).write_text(json.dumps(d, indent=1, ensure_ascii=False))


# ---- SORCERESS: HER DEFAULT LOOK (R-C9-120, 05a300c47): the robe v7 re-skin and the leggings body ---------------
# gear_sets/sorceress_robe/export_r120_ship replaces her pieces in place (so_d7/scene_pkg/character_sorceress.json unchanged)
for f in ("so-body.glb", "robe.glb", "belt.glb", "mantle.glb", "bracers.glb", "circlet.glb", "staff.glb"):
    put(C9 / "gear_sets/sorceress_robe/export_r120_ship" / f, G / "models/sorceress" / f)

# ---- SORCERESS: the battle mage, C (painted) and D (painted + steel grade) -----------------------------------
# R-C9-119/120 (0d418619f / 05a300c47): body119 (the grip_R_wand / grip_L_book morphs, the mirrored cast_fireball_m) and
# the bmc120 / bmd120 gear (the gown re-skin); the open book in the left hand through every clip, the casts included
her = jload(G / "data/character_sorceress.json")
bmm = jload(C9 / "gear_sets/sorceress_battlemage/scene_pkg/gear_manifest_sorceress_battlemage.json")
herm = jload(G / "data/gear_manifest_sorceress.json")
for tag, exp in (("bmc", "export_bmc120"), ("bmd", "export_bmd120")):
    bm = jload(C9 / f"gear_sets/sorceress_battlemage/scene_pkg/character_sorceress_{tag}119_full.json")
    d = MV / f"so_{tag}"
    body = put(C9 / "gear_sets/sorceress_battlemage/body119/so-body_bm119.glb", d / "so-body_bm119.glb")
    pieces = []
    specs = dict(bmm["pieces"])
    specs.setdefault("under_legs", {"file": "under_legs.glb", "mode": "skin"})      # v10's under-layer (s42), not in the manifest
    for name, spec in specs.items():
        src = C9 / "gear_sets/sorceress_battlemage" / exp / spec["file"]
        put(src, d / spec["file"])
        e = {"piece": name, "mode": spec.get("mode", "skin"), "glb": spec["file"]}
        if spec.get("bones"):
            e["bones"] = spec["bones"]
        pieces.append(e)
    man = copy.deepcopy(herm)
    man["_note"] = f"R-C9-117: the battle-mage set {tag.upper()} ({exp}) on her v8 body, in her manifest's shape (tools/make_slots.py)"
    man["body"] = "so-body_bm119.glb"
    man["body_sha256"] = ""
    man["pieces"] = pieces
    man["layer_order"] = bmm.get("layer_order", ["body"] + [p["piece"] for p in pieces])
    jsave(f"gear_so_{tag}.json", man)
    ch = copy.deepcopy(bm)
    ch["_note"] = (f"R-C9-117/119/120: the battle mage {tag.upper()} ({exp}) -- gear_sets/sorceress_battlemage/scene_pkg/"
                   f"character_sorceress_{tag}119_full.json with its paths moved into the page's variant pack. THE BOOK HOLD OVER THE "
                   "CASTS TOO (the lane's integration note: knight.gd's left slot blends over locomotion only): its strike_release -- "
                   "a filtered Blend2 inside each strike's one-shot -- carries book_carry_L on the three left-arm bones through both "
                   "casts (guard_throughout); the wand hand throws the mirrored Fire Ball, so the right arm needs no carry there")
    ch["model"] = f"res://models/variants/so_{tag}/so-body_bm119.glb"
    ch["gear_dir"] = f"res://models/variants/so_{tag}"
    ch["gear_manifest"] = f"res://data/slots/gear_so_{tag}.json"
    full = list(bm["gear_stacks"][-1])
    ch["gear_stacks"] = [[], ["gown", "legs", "under_legs"], ["gown", "legs", "under_legs", "breastplate"],
                         ["gown", "legs", "under_legs", "breastplate", "hood", "gauntlets"], full]
    ch["gear_stacks"] = [[p for p in s if p in full] for s in ch["gear_stacks"]]
    ch["gear_stack_names"] = ["base", "gown + legs", "+ breastplate", "+ hood + gauntlets", "full kit (+wand +grimoire)"]
    ch["sockets"] = "res://data/slots/sockets_so_bm.json"
    ch["strike_release"] = {"pose": "book_carry_L", "bones": ["LeftArm", "LeftForeArm", "LeftHand"],
                            "guard_throughout": ["cast_fireball_m", "cast_meteor"], "at_s": {}, "over_s": 0.08,
                            "_note": "R-C9-119: the open book held through both casts (book_carry_L), as the slot's arm_layer_armed holds it over locomotion"}
    jsave(f"so_{tag}.json", ch)
    OUT[f"so_{tag}"] = {"body_md5": body, "pieces": [p["piece"] for p in pieces]}

# her sockets with the crown on the WAND's tip (0.35 m along weapon_r: the battle-mage manifest's length_m), not the staff's
sk = jload(G / "data/sockets_sorceress.json")
sk["main_tip"] = dict(sk["main_tip"], along_bone_m=0.39,
                      what="the WAND's crystal tip (R-C9-119 sockets_r119: 0.390 m from the fist along the wand): the Meteor's call")
sk["cast_hand_R"] = {"bone": "RightHand", "along_bone_m": 0.07, "what": "the wand hand's palm: the mirrored Fire Ball's spawn (R-C9-119)"}
jsave("sockets_so_bm.json", sk)

# ---- SORCERESS: the ARENA KIT of record (R-C9-133/134), FIXED by R-C9-138/140 -- so_mx/export/ss138a -----------------
# orb staff (right) + shield (left) on the Mixamo Pro Sword and Shield clips; the calmer idle (spine pitch), the staff aimed
# along her facing (hand + forearm twist, the grip untouched), the Fire Ball's orb leading; hood_hair: hood on = hair off.
# ?armor=bm134 (the slot so_bm134); ?armor=bm134&soidle=ss4 the alternate idle (Mixamo sword-and-shield idle 4)
SS = C9 / "so_mx/export/ss152b"   # R-C9-152 option B: ss138a with the hood_hair morph withdrawn, the HOOD CAP over the back/top hair (r152_02 --no-braid) and the hood_braid morph (the braid tucked in while the hood is worn); was ss138a (R-C9-138/140)
d = MV / "so_bm134"
body = put(SS / "so-body_ss152.glb", d / "so-body_ss152.glb")
BM134 = ["gown", "legs", "under_legs", "breastplate", "hood", "gauntlets", "orbstaff", "shield"]
for p_ in BM134:
    put(SS / f"{p_}.glb", d / f"{p_}.glb")
man = copy.deepcopy(herm)
man["_note"] = "R-C9-138: the arena battle mage (so_mx/export/ss138a: orb staff + shield on the Mixamo sword-and-shield clips), in her manifest's shape (tools/make_slots.py)"
man["body"] = "so-body_ss152.glb"
man["body_sha256"] = ""
man["body_shape_keys"] = ["grip_R", "grip_L", "under_battlemage", "hood_braid"]
man["pieces"] = [{"piece": p_, "mode": "skin", "glb": f"{p_}.glb"} for p_ in BM134]
man["layer_order"] = ["body", "gown", "legs", "under_legs", "breastplate", "hood", "gauntlets", "orbstaff", "shield"]
man["shape_key_rules"] = {"grip_R": "1 while the orb staff is worn", "grip_L": "1 while the shield is worn",
                          "under_battlemage": "1 while the gown is worn", "hood_braid": "R-C9-152: 1 while the hood is worn -- the braid below the hood tucked inside her back; the hood piece carries a CAP over the back/top hair (the face and front hair unchanged)"}
JM = jload(C9 / "join1_render/manifests/d2-fire-sorc-bm_clips.json")
man["locomotion_in_place"] = {"rule": "locomotion ships IN PLACE; drive at the foot-lock speed (s18_footlock_contact, the JOIN-1 manifest)",
                              "walk": {"seconds": JM["clips"]["walk"]["seconds"], "speed_m_s": JM["locomotion_in_place"]["walk"]["speed_m_s"]},
                              "run": {"seconds": JM["clips"]["run"]["seconds"], "speed_m_s": JM["locomotion_in_place"]["run"]["speed_m_s"]},
                              "_source": "join1_render/manifests/d2-fire-sorc-bm_clips.json (the walk and run clips are ss134f's, unchanged in their legs)"}
jsave("gear_so_bm134.json", man)
ss = jload(C9 / "so_mx/work/character_sorceress_ss152b.json")
for alt, idle in (("", "idle"), ("_ss4", "idle_ss4")):
    ch = copy.deepcopy(ss)
    ch["model"] = "res://models/variants/so_bm134/so-body_ss152.glb"
    ch["gear_dir"] = "res://models/variants/so_bm134"
    ch["gear_manifest"] = "res://data/slots/gear_so_bm134.json"
    full = ["gown", "legs", "under_legs", "breastplate", "hood", "gauntlets", "orbstaff", "shield"]
    ch["gear_stacks"] = [[], ["gown", "legs", "under_legs"], ["gown", "legs", "under_legs", "breastplate"],
                         ["gown", "legs", "under_legs", "breastplate", "hood", "gauntlets"], [p_ for p_ in full if p_ != "hood"], full]
    # the page starts her on the LAST stack: the full kit, hood ON (hair off); G steps base -> ... -> hood off -> full again
    ch["gear_stack_names"] = ["base", "gown + legs", "+ breastplate", "+ hood + gauntlets", "armed, hood off", "full kit (+orb staff +shield)"]
    ch["sockets"] = "res://data/slots/sockets_so_bm134.json"
    ch["clips"] = dict(ch["clips"], idle=idle)
    ch["clips_armed"] = dict(ch["clips_armed"], idle=idle)
    ch.pop("clips_alt_idle", None)
    ch["_idle"] = idle
    jsave(f"so_bm134{alt}.json", ch)
OUT["so_bm134"] = {"body_md5": body, "pieces": BM134}
sk = jload(G / "data/sockets_sorceress.json")
ORB = {"bone": "weapon_r", "along_bone_m": -0.5689,
       "what": "the ORB: weapon_r - 0.5689 m along +Y (the JOIN-1 kit d2-fire-sorc-bm's main_tip, measured off orbstaff.glb): the Fire Ball's spawn and the Meteor's call"}
sk["main_tip"] = dict(ORB)
sk["orb_tip"] = dict(ORB)
jsave("sockets_so_bm134.json", sk)

# ---- BARBARIAN: the freed champion, C (painted + grade) and B (painted) --------------------------------------
him = jload(G / "data/character.json")
himm = jload(G / "data/gear_manifest.json")
champ = jload(C9 / "gear_sets/barbarian_gladiator/scene_pkg/character_champion_full.json")
CH_PIECES = ["girdle", "kilt", "wraps", "greaves", "chest", "wrists", "helm", "pauldron"]
for tag, bdir, bname, gdir in (("gladc", "body_graded", "nb-body_champion_graded.glb", "export_graded"),
                               ("gladb", "body_painted", "nb-body_champion_painted.glb", "export_painted")):
    d = MV / f"barb_{tag}"
    body = put(C9 / "gear_sets/barbarian_gladiator" / bdir / bname, d / bname)
    for p in CH_PIECES:
        put(C9 / "gear_sets/barbarian_gladiator" / gdir / f"{p}.glb", d / f"{p}.glb")
    man = copy.deepcopy(himm)
    man["_note"] = f"R-C9-117: the freed champion {tag[-1].upper()} ({bdir} + {gdir}), every piece skinned on his 26 joints (gear_sets/barbarian_gladiator)"
    man["body"] = bname
    man["pieces"] = [{"piece": p, "mode": "skin", "glb": f"{p}.glb", "bones": ["skinned"]} for p in CH_PIECES]
    man["layer_order"] = ["body"] + CH_PIECES
    jsave(f"gear_barb_{tag}.json", man)
    ch = copy.deepcopy(him)
    ch["_note"] = (f"R-C9-117: the freed champion gladiator {tag[-1].upper()} -- his character.json with the champion's body and set "
                   "(gear_sets/barbarian_gladiator/scene_pkg/character_champion_full.json). NO WEAPON (Matt, R-C9-105): never armed, so "
                   "he plays his unarmed roles -- and the champion body carries his JOIN moves, so SLASH = the whirlwind, CHOP = the war cry.")
    ch["model"] = f"res://models/variants/barb_{tag}/{bname}"
    ch["gear_dir"] = f"res://models/variants/barb_{tag}"
    ch["gear_manifest"] = f"res://data/slots/gear_barb_{tag}.json"
    ch["gear_stacks"] = [[], ["girdle", "kilt", "wraps"], ["girdle", "kilt", "wraps", "greaves", "wrists"],
                         ["girdle", "kilt", "wraps", "greaves", "wrists", "chest"], CH_PIECES]
    ch["gear_stack_names"] = ["base", "girdle + kilt + wraps", "+ greaves + wrists", "+ chest", "full champion set"]
    ch["armed_when_pieces"] = ["__never__"]
    ch["clips"] = {"idle": "idle", "walk": "walk", "run": "run", "attack": "whirlwind", "chop": "shout"}
    ch["morph_rules"] = champ.get("morph_rules", {"helmet_on": "helm"})
    ch.pop("arm_layer", None)
    jsave(f"barb_{tag}.json", ch)
    OUT[f"barb_{tag}"] = {"body_md5": body}

# ---- BARBARIAN: the axe holds, T12_11 (installed in cliffside3d) and T12_12c F25L / F40L ------------------------
ST = C9 / "attack_lab/staged"
(G / "scripts/variants").mkdir(parents=True, exist_ok=True)
kg = G / "scripts/variants/knight_t12_11.gd"
shutil.copyfile(ST / "t12_11/knight.gd", kg)
assert md5(kg) == "86141f65", md5(kg)
# R-C9-127: T12_12d N25/N40 DROPPED from the ship (Matt prefers the original width); the record of R-C9-122 kept below.
# R-C9-122 (cb0bb334a): T12_12d -- F25L with the legs taken in (N25: -25%, N40: -40% of the excess over hip width) and the
# heel-to-toe walk; its manifest (5fdfc147) carries locomotion_in_place.walk 1.3199 m/s, which the knight prefers
for tag, bsrc, chsrc in (("t1211", "T12_11_trails", "t12_11"), ("f25l", "T12_12c_F25L", "t12_12c"), ("f40l", "T12_12c_F40L", "t12_12c")):
    d = MV / f"barb_{tag}"
    body = put(C9 / "nb_d2/export_staging" / bsrc / "nb-body.glb", d / "nb-body.glb", optimizer_off=True)
    ch = jload(ST / chsrc / "character.json")
    ch["_r_c9_117"] = f"R-C9-117 (web only): attack_lab/staged/{chsrc}/character.json, the body moved to models/variants/barb_{tag}; the six pieces and the manifest are T12_11's (byte-identical gear)"
    ch["model"] = f"res://models/variants/barb_{tag}/nb-body.glb"
    ch["gear_manifest"] = "res://data/slots/gear_t12d.json" if chsrc == "t12_12d" else "res://data/slots/gear_t12.json"
    ch["gear_dir"] = "res://models/gear"
    jsave(f"barb_{tag}.json", ch)
    OUT[f"barb_{tag}"] = {"body_md5": body, "character_md5_src": md5(ST / chsrc / "character.json")}
shutil.copyfile(C9 / "nb_d2/export_staging/T12_11_trails/gear_manifest.json", SL / "gear_t12.json")
assert OUT["barb_t1211"]["body_md5"] == "3e32a9fc" and OUT["barb_f25l"]["body_md5"] == "23e5fde7" and OUT["barb_f40l"]["body_md5"] == "614de31d", OUT

# ---- THE DARK KNIGHT (c=warlord) --------------------------------------------------------------------------------
WD = G / "models/warlord"
FH = C9 / "wl_e1/export/final_k_eor3"  # R-C9-141: eor3 (E1b cf004d7c2) = eor2 with ONLY the body's head crown tucked under the helm shell (POSITION data; every piece byte-identical). Before, R-C9-132/133: final_k_eor with the EXTENDED-ARM spin clips (E1 f734570d2: the fists 0.80 m out, the haft slid 0.20 m through them, the head 1.93 m out). Before, R-C9-127/128: final_k (Mixamo Great Sword set on the narrowed base, painted + graded, bind order = the body; 29faf3a42) + the Eye of Reckoning spin clips eor_spin_start / eor_spin_loop (08abac31b). Before: final_j2 (bind-order fix), final_j (stage J)
for f in ("wl_body.glb", "wl_mace.glb", "wl_chest.glb", "wl_pauldrons.glb", "wl_helm.glb", "wl_helm_ice.glb", "wl_cape.glb"):
    put(FH / f, WD / f)
wl = jload(C9 / "wl_e1/work/character_wl.json")
man = copy.deepcopy(herm)
man["_note"] = "R-C9-117: the dark knight (wl_e1/export/final_k_eor2, 1.96 m; R-C9-127: final_k, the Mixamo Great Sword set; R-C9-128: the Eye of Reckoning spin; R-C9-121: the painted body, the cape fitted, the eye-slit glow, the unarmed clip set), every piece skinned on his own skeleton (wl_e1 e10/e12: the mace on weapon_r at the fist's grip)"
man["body"] = "wl_body.glb"
man["body_sha256"] = ""
man["height_m"] = 1.96
man["body_shape_keys"] = []
man["pieces"] = [{"piece": p, "mode": "skin", "glb": f"{p}.glb", "bones": ["skinned"]} for p in ("wl_mace", "wl_chest", "wl_pauldrons", "wl_helm", "wl_cape")]
man["layer_order"] = ["body", "wl_chest", "wl_pauldrons", "wl_helm", "wl_cape", "wl_mace"]
man["shape_key_rules"] = {}
# film_cfg_h.json's speeds (the E1 lane's foot-lock on final_h's walk and run)
WLM = jload(FH / "wl_manifest.json")
FL = WLM["foot_lock_m_per_s"]          # R-C9-127: final_k's foot-lock speeds (walk 1.073, run 4.062)
man["locomotion_in_place"] = {"rule": "locomotion ships IN PLACE; drive at the foot-lock speed", "walk": {"speed_m_s": FL["walk"]},
                              "run": {"speed_m_s": FL["run"]}, "_source": "wl_e1/export/final_k_eor3/wl_manifest.json foot_lock_m_per_s"}
jsave("gear_warlord.json", man)
# the eye colour (wl_manifest.json eye_variant): ONE helm loaded -- violet (the default) or ice, the piece keeps its name
mani = copy.deepcopy(man)
for pc in mani["pieces"]:
    if pc["piece"] == "wl_helm":
        pc["glb"] = "wl_helm_ice.glb"
jsave("gear_warlord_ice.json", mani)
ch = copy.deepcopy(her)
for k in list(ch.keys()):
    if k.startswith("_") or k in ("casts", "strikes_need_armed", "gear_stack_detail", "layers_knight_lacks", "roles_knight_lacks"):
        ch.pop(k)
ch["_note"] = ("R-C9-117: THE DARK KNIGHT (wl_e1/export/final_k_eor2): his clips idle walk run attack hit death warcry; SLASH = the mace "
               "attack, CHOP = the war cry, BASH = the Eye of Reckoning (R-C9-128: eor_spin_start + eor_spin_loop, the ported whirlwind). Built in her slot's shape: knight.gd plays him as it plays "
               "her; the mace is keyed two-handed in every clip, so no carry layer (the layers name idle with no bones).")
ch["model"] = "res://models/warlord/wl_body.glb"
ch["model_height_m"] = 1.96
# the weapon state (wl_manifest.json weapon_state): armed (the mace shown) idle/walk/run; unarmed (GEAR took the mace)
# the *_unarmed set; attack and the war cry need the mace (their buttons hide with it)
ch["clips"] = {"idle": "idle_unarmed", "walk": "walk_unarmed", "run": "run_unarmed"}
ch["clips_armed"] = {"idle": "idle", "walk": "walk", "run": "run", "attack": "attack", "chop": "warcry"}
ch["roles_knight_lacks"] = {"hit": "hit", "death": "death"}
ch["armed_when_pieces"] = list(wl["armed_when_pieces"])
ch["gear_manifest"] = "res://data/slots/gear_warlord.json"
ch["gear_dir"] = "res://models/warlord"
ch["gear_stacks"] = wl["gear_stacks"]
ch["gear_stack_names"] = wl["gear_stack_names"]
ch["morph_rules"] = {}
ch["arm_layer_armed_R"] = {"action": "idle", "bones": [], "weight": 0.0}
ch["arm_layer_armed"] = {"action": "idle", "bones": []}
ch["upper_armed"] = {"walk": "walk", "run": "run", "bones": []}
ch["strike_release"] = {"pose": "idle", "bones": [], "guard_throughout": [], "at_s": {}, "over_s": 0.12}
ch["walk_px_s"] = round(FL["walk"] * 100.617553710938, 1)
ch["run_px_s"] = round(FL["run"] * 100.617553710938, 1)
ch["eor_spin"] = WLM["eor_spin"]      # R-C9-128: played by slot_knight.gd (eor_chan = start + loops) under the ported effect
ch["foot_lock"] = False
jsave("warlord.json", ch)
chi = copy.deepcopy(ch)
chi["gear_manifest"] = "res://data/slots/gear_warlord_ice.json"
chi["_eye"] = "ice (wl_helm_ice.glb)"
jsave("warlord_ice.json", chi)
OUT["warlord"] = {"pieces": man["pieces"], "walk_px_s": ch["walk_px_s"], "run_px_s": ch["run_px_s"]}
print(json.dumps(OUT, indent=1)[:2000])
