extends Node
## THE STAFF HOLD, wired the way the play build should wire it (D7 pass 2; the T12 method, legolas
## Part 6). One helper, used by the film AND the stills, so what is filmed and what is counted are
## the same pose.
##
## LAYERS -- the barbarian's armed-speed split (speedsplit_patch.py): a FILTERED Blend2 whose input 1
## owns the filtered bones outright at weight 1.
##   clip      the clip's pose: legs, hips, root, the left arm -- everything no filter takes
##   carry     `staff_carry_R`, a held pose (s12_carry.py): the staff arm set so the SEATED shaft
##             stands upright at her right, and the spine it was solved on
##   up_full   Blend2 filtered to the NINE carry bones           idle / walk / run
##   up_arm    Blend2 filtered to the FOUR staff-arm bones       cast_fireball -- thrown from the
##             free LEFT hand, so the spine stays the clip's and the torso still drives the throw
##   up_chest_arm  Blend2 filtered to Spine02 + the staff arm    hit (2026-09-30, the JOIN-1 pack
##             review): the staff stays inside the idle carry's lean (8.25 deg worst against the
##             idle's 10.81) while her head still turns 94% as far as the raw clip's. The full carry
##             froze the flinch; the arm alone leaned the staff 21.75 deg (so_d7 s17_hit_flinch.py)
##   death     takes NEITHER, by decision: she falls with the staff
##   cast_meteor takes NEITHER: its staff motion is BAKED into the clip's own weapon_r track
##             (s13_meteor_track.py), because it depends on the pose frame by frame
## GRIP     grip_R = 1 while the staff is held. grip_L = 1 only while the off-hand IK is on.
## OFF HAND TwoBoneIK3D LeftArm -> LeftForeArm -> LeftHand onto a point IK_UP_SHAFT_M up the
##          shaft, per clip (IK_ON). OFF everywhere it ships: OFF for the Fire Ball by the brief;
##          OFF for the Meteor because the shaft is out of the left arm's reach in every frame of
##          that clip (s12_measure --perframe: nearest 0.697 m against a 0.504 m arm).
const CARRY_BONES := ["Spine02", "Spine01", "Spine", "neck", "Head",
		"RightShoulder", "RightArm", "RightForeArm", "RightHand"]
const ARM_BONES := ["RightShoulder", "RightArm", "RightForeArm", "RightHand"]
const CHEST_ARM_BONES := ["Spine02", "RightShoulder", "RightArm", "RightForeArm", "RightHand"]
const LAYER := {"idle": "full", "walk": "full", "run": "full",
		"cast_fireball": "arm", "cast_meteor": "none", "hit": "chest_arm", "death": "none"}
const IK_ON := {"idle": false, "walk": false, "run": false,
		"cast_fireball": false, "cast_meteor": false, "hit": false, "death": false}
const LOOPS := ["idle", "walk", "run", "staff_carry_R"]
const ONCE := ["cast_fireball", "cast_meteor", "hit", "death"]
const IK_UP_SHAFT_M := 0.25       # the off hand's point on the shaft, above the right fist
const PALM_M := 0.07              # wrist to palm: the IK's virtual end, so the PALM meets the shaft

var root: Node3D
var ap: AnimationPlayer
var tree: AnimationTree
var skel: Skeleton3D
var body: MeshInstance3D
var ik: TwoBoneIK3D
var ik_target: Marker3D
var ik_pole: Marker3D
var clip := ""
var undress_keys := true      # false: leave every under_<g> morph at 0 (the A/B test of the morphs)
var filtered := {"full": 0, "arm": 0, "chest_arm": 0}

func setup(r: Node3D, manual := false) -> void:
	root = r
	ap = root.find_child("AnimationPlayer", true, false)
	skel = root.find_children("*", "Skeleton3D", true, false)[0]
	for c in LOOPS:
		if ap.has_animation(c):
			ap.get_animation(c).loop_mode = Animation.LOOP_LINEAR
	for c in ONCE:
		if ap.has_animation(c):
			ap.get_animation(c).loop_mode = Animation.LOOP_NONE
	ap.stop()
	tree = AnimationTree.new()
	tree.name = "StaffTree"
	ap.get_parent().add_child(tree)
	tree.anim_player = tree.get_path_to(ap)
	var bt := AnimationNodeBlendTree.new()
	var a_clip := AnimationNodeAnimation.new(); a_clip.animation = "idle"
	# TWO carry nodes: a blend tree lets a node's output feed ONE input only (connect_node refuses
	# a second use -- "output == p_output_node"), and a tree with an unfed input poses nothing at all
	var a_carry := AnimationNodeAnimation.new(); a_carry.animation = "staff_carry_R"
	var a_carry2 := AnimationNodeAnimation.new(); a_carry2.animation = "staff_carry_R"
	var a_carry3 := AnimationNodeAnimation.new(); a_carry3.animation = "staff_carry_R"
	var seek := AnimationNodeTimeSeek.new()
	var up_full := AnimationNodeBlend2.new(); up_full.filter_enabled = true
	var up_arm := AnimationNodeBlend2.new(); up_arm.filter_enabled = true
	var up_chest_arm := AnimationNodeBlend2.new(); up_chest_arm.filter_enabled = true
	bt.add_node("clip", a_clip, Vector2(0, 0))
	bt.add_node("seek", seek, Vector2(160, 0))
	bt.add_node("carry", a_carry, Vector2(0, 160))
	bt.add_node("carry2", a_carry2, Vector2(160, 160))
	bt.add_node("up_full", up_full, Vector2(320, 0))
	bt.add_node("up_arm", up_arm, Vector2(480, 0))
	bt.add_node("carry3", a_carry3, Vector2(320, 160))
	bt.add_node("up_chest_arm", up_chest_arm, Vector2(640, 0))
	bt.connect_node("seek", 0, "clip")
	bt.connect_node("up_full", 0, "seek")
	bt.connect_node("up_full", 1, "carry")
	bt.connect_node("up_arm", 0, "up_full")
	bt.connect_node("up_arm", 1, "carry2")
	bt.connect_node("up_chest_arm", 0, "up_arm")
	bt.connect_node("up_chest_arm", 1, "carry3")
	bt.connect_node("output", 0, "up_chest_arm")
	# filter paths from a clip's OWN tracks (as _apply_upper does): the exact NodePaths the mixer uses
	var an := ap.get_animation("idle")
	for i in an.get_track_count():
		var pth: NodePath = an.track_get_path(i)
		var bone := String(pth.get_concatenated_subnames())
		if bone in CARRY_BONES:
			up_full.set_filter_path(pth, true); filtered["full"] += 1
		if bone in ARM_BONES:
			up_arm.set_filter_path(pth, true); filtered["arm"] += 1
		if bone in CHEST_ARM_BONES:
			up_chest_arm.set_filter_path(pth, true); filtered["chest_arm"] += 1
	tree.tree_root = bt
	if manual:
		tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	tree.active = true
	for mi in root.find_children("*", "MeshInstance3D", true, false):
		if (mi as MeshInstance3D).find_blend_shape_by_name("grip_R") >= 0:
			body = mi
	_wire_ik()
	print("[staff] tree on '%s': up_full %d tracks (%d bones), up_arm %d tracks (%d bones), up_chest_arm %d tracks (%d bones); body '%s' grip_R %d grip_L %d"
		% [ap.name, filtered["full"], CARRY_BONES.size(), filtered["arm"], ARM_BONES.size(), filtered["chest_arm"], CHEST_ARM_BONES.size(),
		   body.name if body else "?", body.find_blend_shape_by_name("grip_R") if body else -1,
		   body.find_blend_shape_by_name("grip_L") if body else -1])

func _wire_ik() -> void:
	ik_target = Marker3D.new(); ik_target.name = "OffHandTarget"; root.add_child(ik_target)
	ik_pole = Marker3D.new(); ik_pole.name = "OffHandPole"; root.add_child(ik_pole)
	ik = TwoBoneIK3D.new()
	ik.name = "OffHandIK"
	skel.add_child(ik)
	ik.set_setting_count(1)
	ik.set_root_bone_name(0, "LeftArm")
	ik.set_middle_bone_name(0, "LeftForeArm")
	ik.set_end_bone_name(0, "LeftHand")
	ik.set_extend_end_bone(0, true)
	ik.set_end_bone_length(0, PALM_M / _skel_scale())
	ik.set_target_node(0, ik.get_path_to(ik_target))
	ik.set_pole_node(0, ik.get_path_to(ik_pole))
	ik.active = false

func _skel_scale() -> float:
	return skel.global_transform.basis.get_scale().x

func bone_world(bn: String) -> Transform3D:
	return skel.global_transform * skel.get_bone_global_pose(skel.find_bone(bn))

## the shaft at this instant, in world: grip point and unit direction to the crown (+Y of weapon_r)
func shaft() -> Array:
	var w := bone_world("weapon_r")
	return [w.origin, (w.basis * Vector3.UP).normalized()]

## place the IK's target on the shaft and its pole down, back and out from her left elbow
func aim_ik() -> void:
	var s := shaft()
	ik_target.global_position = (s[0] as Vector3) + (s[1] as Vector3) * IK_UP_SHAFT_M
	var e := bone_world("LeftForeArm").origin
	var b := root.global_transform.basis.orthonormalized()
	ik_pole.global_position = e + b * Vector3(0.30, -0.30, -0.20)

func play(c: String, t := 0.0) -> void:
	clip = c
	var bt := tree.tree_root as AnimationNodeBlendTree
	(bt.get_node("clip") as AnimationNodeAnimation).animation = c
	var lay := String(LAYER.get(c, "none"))
	tree.set("parameters/up_full/blend_amount", 1.0 if lay == "full" else 0.0)
	tree.set("parameters/up_arm/blend_amount", 1.0 if lay == "arm" else 0.0)
	tree.set("parameters/up_chest_arm/blend_amount", 1.0 if lay == "chest_arm" else 0.0)
	tree.set("parameters/seek/seek_request", t)
	var on := bool(IK_ON.get(c, false))
	ik.active = on
	grips(on)

func grips(ik_on: bool) -> void:
	if body:
		body.set_blend_shape_value(body.find_blend_shape_by_name("grip_R"), 1.0)
		body.set_blend_shape_value(body.find_blend_shape_by_name("grip_L"), 1.0 if ik_on else 0.0)
		dress(["robe", "mantle", "belt", "bracers"] if undress_keys else [])

## the UNDER-GARMENT morphs (s9_assemble --under): under_<g> = 1 while garment g is worn. The film
## and the stills wear the full costume, so every one is on. A build without them is unaffected.
func dress(worn := ["robe", "mantle", "belt", "bracers"]) -> void:
	if body == null:
		return
	for g in ["robe", "mantle", "belt", "bracers"]:
		var i := body.find_blend_shape_by_name("under_" + g)
		if i >= 0:
			body.set_blend_shape_value(i, 1.0 if g in worn else 0.0)

## evaluate NOW (manual mode): the tree, the IK's target from that pose, then the skeleton and
## its modifiers -- the order the barbarian's probes use (speed_split.gd::_step)
func evaluate(dt := 0.0) -> void:
	tree.advance(dt)
	aim_ik()
	skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)
