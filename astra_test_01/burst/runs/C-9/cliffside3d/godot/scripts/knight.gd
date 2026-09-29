extends CharacterBody3D
## C-9 R-C9-66 — a character in the true-3D cliffside, at the WORLD CAMERA'S REAL ANGLE.
##
## Matt, R-C9-68, verbatim: "Use the real 53 degree angle." So the character is a real
## object seen by the player_lock camera at its own 52.95 deg pitch -- it occludes and
## is occluded per pixel, the lights reach it, and it turns as it walks, with no
## eight-direction set to pick from and no flat card to sort.
##
## The alternative that was going to be built alongside -- rendering the character by
## its own camera at the 19.77 deg the approved art is PAINTED at, then compositing it
## as a card -- is dropped on that ruling. Worth recording what it would have cost, in
## case the question returns: a composited card is flat, so it carries ONE depth for the
## whole figure, and a rock that should hide a walker's legs while leaving his head in
## view has to hide all of him or none. Real 3D has no such problem. What real 3D costs
## instead is that the world camera sees a figure from 33 degrees higher than any
## painted frame contains -- helm crowns and shoulder tops nobody has drawn.
##
## THE OCCUPANT IS A STAND-IN. R-C9-69 replaces it with a Norse barbarian whose sheet is
## being painted now. The Meshy knight is here to check scale, ground contact, occlusion
## and light, and is deliberately not polished.

const PPM := 100.617553710938
const CHAR_LAYER := 4
const WALK_PX_S := 247.0          # parallax.json movement, the Keeper's own
const RUN_PX_S := 494.0
const CHARACTER := "res://data/character.json"
# preloaded rather than referenced by class_name: a global class is only visible once the
# editor's class cache has been rebuilt, and an exported app that loads before that has a
# character with no gear and no error anybody sees.
const CharGear := preload("res://scripts/gear.gd")
const LINE_PX := 1.1

## THE SLOT IS SWAPPABLE, and nothing below names the knight.
##
## Who stands here is data/character.json: a GLB path, the four clip ROLES the scene
## drives, and an optional hand prop. The T8 barbarian arrives as a textured, rigged GLB
## with idle/walk/run/attack, so he replaces one string in that file. The scale he stands
## at is data/figure.json's measured 1.25178 -- a property of this painted world's metric,
## not of the model -- so it carries across the swap unchanged.
var cfg := {}
var _roles := {}

var right := Vector3.RIGHT
var up := Vector3.UP
var fwd := Vector3.FORWARD
var facing := "S"
var state := "idle"

var _rig: Node3D
var _skel: Skeleton3D
var _anim: AnimationPlayer
var _mesh: MeshInstance3D
var _outline: MeshInstance3D
var _pollaxe: Node3D
var _attach: BoneAttachment3D
var _socket_basis := Basis()
var _socket_offset := Vector3.ZERO
var _clip := ""
var _clip_len := {}
var _figure_scale := 1.0
var _forward_axis := Vector3(0, 0, -1)
var gear := {}
var gear_stack := 0
var _tree: AnimationTree
var _loco_node: AnimationNodeBlendSpace1D
var _speed := 0.0
var _move_dir := Vector2(0, 1)
var _yaw_cur := 0.0
var _yaw_init := false
var _layer_on := false
var _attack_t := 0.0


func setup(r: Vector3, u: Vector3, f: Vector3, figure_scale: float) -> void:
	right = r
	up = u
	fwd = f
	_figure_scale = figure_scale


func _ready() -> void:
	# He stands ON the terrain layer and is not ON it: CliffWorld.ground_at masks to the
	# terrain, so his own body can never answer the question "where is the ground".
	collision_layer = 1
	collision_mask = CliffWorld.TERRAIN_BIT
	var shape := CollisionShape3D.new()
	var cap := CapsuleShape3D.new()
	cap.height = float(cfg.get("model_height_m", 1.8)) * _figure_scale
	cap.radius = 0.35 * _figure_scale
	shape.shape = cap
	shape.position = Vector3(0, cap.height * 0.5, 0)
	add_child(shape)

	cfg = _read_cfg()
	var model := String(cfg.get("model", "res://models/knight_t3.glb"))
	if not ResourceLoader.exists(model):
		push_error("character: no model at %s" % model)
		return
	_rig = (load(model) as PackedScene).instantiate()
	_rig.scale = Vector3.ONE * _figure_scale
	add_child(_rig)
	_skel = _find(_rig, "Skeleton3D") as Skeleton3D
	_mesh = _find(_rig, "MeshInstance3D") as MeshInstance3D
	_anim = _find(_rig, "AnimationPlayer") as AnimationPlayer
	if _anim != null:
		_anim.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS
		for n in _anim.get_animation_list():
			_clip_len[n] = _anim.get_animation(n).length
	var fa = cfg.get("forward_axis", null)
	if fa != null:
		_forward_axis = Vector3(float(fa[0]), 0.0, float(fa[2])).normalized()
	_bind_roles()
	# A walk that stops at the end of its 25 frames is not a walk. glTF carries no loop
	# flag, so Godot imports every clip as one-shot and the ones that cycle are named here.
	for n in cfg.get("loop", []):
		var real := String(_roles.get(String(n), String(n)))
		if _anim != null and _clip_len.has(real):
			_anim.get_animation(real).loop_mode = Animation.LOOP_LINEAR
	_style()
	_add_outline()
	_read_socket()
	_add_pollaxe()
	_set_layer(_rig, CHAR_LAYER)
	_build_gear()
	_build_anim_tree()
	play(_roles.get("idle", ""))
	_drive()


func _build_anim_tree() -> void:
	"""The shield-carry arm layer, as an AnimationTree Blend2 filtered to four bones.

	`shield_carry_L` is ONE FRAME and it carries tracks for all 24 bones -- measured,
	tools/probe_gear2.gd -- so it is a whole static body pose, not an arm pose. Blended
	unfiltered it would freeze him mid-stride. The filter is what makes it an arm layer,
	and the four paths are taken from the clip's OWN track list rather than composed from
	bone names, so a path that does not exist in the clip cannot be filtered by accident."""
	var spec: Dictionary = cfg.get("arm_layer", {})
	var action := String(spec.get("action", ""))
	if _anim == null or action == "" or not _clip_len.has(action):
		return
	var want: Array = spec.get("bones", [])
	var ca := _anim.get_animation(action)
	var bt := AnimationNodeBlendTree.new()

	# LOCOMOTION IS A BLEND SPACE ON GROUND SPEED, not a clip chosen by a state name. The
	# snap Matt saw is what a state switch looks like: idle and walk are different poses and
	# nothing crosses between them, so the body teleports from one to the other inside a
	# frame. A blend space has no switch -- the pose IS a function of how fast he is
	# actually travelling, and the smoothing on that speed is what gives a human beat to
	# starting and stopping.
	var loco := AnimationNodeBlendSpace1D.new()
	var tr: Dictionary = cfg.get("transitions", {})
	var wsp := float(cfg.get("walk_px_s", WALK_PX_S))
	var rsp := float(cfg.get("run_px_s", RUN_PX_S))
	loco.min_space = 0.0
	loco.max_space = rsp
	for pair in [[String(_roles.get("idle", "idle")), 0.0],
				 [String(_roles.get("walk", "walk")), wsp],
				 [String(_roles.get("run", "run")), rsp]]:
		var an := AnimationNodeAnimation.new()
		an.animation = String(pair[0])
		loco.add_blend_point(an, float(pair[1]))
	# PHASE SYNC, so the feet do not scissor while the blend crosses from walk to run: the
	# walk cycle is 25 frames and the run is 16, and two clips of different length left to
	# run on their own clocks meet at whatever phases they happen to be in.
	if "sync" in loco:
		loco.set("sync", true)
		print("anim tree: blend space sync = %s" % str(loco.get("sync")))
	else:
		print("anim tree: this AnimationNodeBlendSpace1D has NO sync property")

	# THE ATTACK IS A ONE-SHOT OVER THE TOP, not a fourth blend point. It is not a speed, it
	# interrupts, and it has to fade in and back out to whatever he was doing.
	var shot := AnimationNodeOneShot.new()
	shot.fadein_time = float(tr.get("attack_fade_in_s", 0.10))
	shot.fadeout_time = float(tr.get("attack_fade_out_s", 0.25))
	var atk := AnimationNodeAnimation.new()
	atk.animation = String(_roles.get("attack", "attack"))

	var b2 := AnimationNodeBlend2.new()
	b2.filter_enabled = true
	var filtered := 0
	for i in ca.get_track_count():
		var pth: NodePath = ca.track_get_path(i)
		if want.has(String(pth.get_concatenated_subnames())):
			b2.set_filter_path(pth, true)
			filtered += 1
	var carry := AnimationNodeAnimation.new()
	carry.animation = action

	bt.add_node("loco", loco, Vector2(0, 0))
	bt.add_node("atk", atk, Vector2(0, 140))
	bt.add_node("oneshot", shot, Vector2(240, 40))
	bt.add_node("carry", carry, Vector2(240, 220))
	bt.add_node("blend", b2, Vector2(470, 100))
	bt.connect_node("oneshot", 0, "loco")
	bt.connect_node("oneshot", 1, "atk")
	bt.connect_node("blend", 0, "oneshot")
	bt.connect_node("blend", 1, "carry")
	bt.connect_node("output", 0, "blend")
	_loco_node = loco
	_tree = AnimationTree.new()
	_tree.name = "AnimTree"
	_tree.tree_root = bt
	_anim.get_parent().add_child(_tree)
	_tree.anim_player = _tree.get_path_to(_anim)
	_tree.root_node = _tree.get_path_to(_anim.get_node(_anim.root_node))
	_tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS
	_tree.active = true
	_anim.active = false
	print("anim tree: loco blend space 0/%.1f/%.1f px/s, attack one-shot %.2f/%.2f s, arm layer '%s' filtered to %d of %d tracks"
		% [wsp, rsp, shot.fadein_time, shot.fadeout_time, action, filtered, ca.get_track_count()])


func _layer_weight(clip: String) -> float:
	"""1 whenever the shield is carried, over every clip INCLUDING the attack.

	THE EXPORT'S MANIFEST SAYS THE OPPOSITE and it is worth reading here rather than
	silently disagreeing with it: `do NOT apply it over attack -- the slash uses the right
	arm and the left must swing free`. Reversed by design call on this scene's own
	measurements. Without the layer the shield is 0.249 m inside his torso through the
	slash -- 1107 of 2439 sampled vertices -- and with it 54 at 0.067 m. A free-swinging
	left arm is only free if it is not holding a shield; a shield-bearer keeps his guard up
	while he strikes with the other hand.

	`never_over` is still honoured, and is now empty: the exclusion is data, not code, so
	the next reversal is one line of JSON and not a hunt through a method."""
	var spec: Dictionary = cfg.get("arm_layer", {})
	if _tree == null or not _layer_on:
		return 0.0
	for never in spec.get("never_over", []):
		if clip == String(_roles.get(String(never), String(never))):
			return 0.0
	return 1.0


func _build_gear() -> void:
	if _skel == null or String(cfg.get("gear_manifest", "")) == "":
		return
	var ms: float = maxf(_mesh.global_transform.basis.get_scale().x, 1e-9)
	gear = CharGear.build(_skel, String(cfg["gear_manifest"]), String(cfg.get("gear_dir", "")),
						  _figure_scale, ms)
	set_gear_stack(0)
	print("gear: %s" % JSON.stringify(gear.get("_report", {})))


func gear_stack_count() -> int:
	return (cfg.get("gear_stacks", []) as Array).size()


func set_gear_stack(i: int) -> void:
	"""Five stacks, cumulative: base / +helmet+bracers / +byrnie / +mantle / +axe+shield.

	The helmet_on morph FOLLOWS THE HELMET and nothing else changes with it. It compresses
	the crown hair so the helmet has somewhere to sit; leaving it at 0 under a helmet is a
	head of hair through a steel cap, and setting it without one is a dent in a bare skull."""
	var stacks: Array = cfg.get("gear_stacks", [])
	if stacks.is_empty() or gear.is_empty():
		return
	gear_stack = posmod(i, stacks.size())
	var on: Array = stacks[gear_stack]
	CharGear.show_pieces(gear, on)
	for morph in (cfg.get("morph_rules", {}) as Dictionary):
		_set_morph(String(morph), String(cfg["morph_rules"][morph]) in on)
	# the arm layer follows the SHIELD, so stacks 0-3 are untouched by it
	_layer_on = String((cfg.get("arm_layer", {}) as Dictionary).get("when_piece", "shield")) in on
	if _tree != null:
		_tree.set("parameters/blend/blend_amount", _layer_weight(_clip))


func cycle_gear() -> void:
	set_gear_stack(gear_stack + 1)


func _set_morph(want: String, on: bool) -> void:
	"""helmet_on compresses the crown under the helmet; grip_R and grip_L close the fists
	round the haft and the grip bar. The rig has 24 bones and NO FINGER BONES, so a morph is
	the only way a hand can close -- which is why an open flat hand was what Matt saw."""
	if want == "" or _mesh == null or _mesh.mesh == null:
		return
	for i in _mesh.mesh.get_blend_shape_count():
		if String(_mesh.mesh.get_blend_shape_name(i)) == want:
			_mesh.set_blend_shape_value(i, 1.0 if on else 0.0)
			return


func _read_cfg() -> Dictionary:
	if not FileAccess.file_exists(CHARACTER):
		return {}
	var j = JSON.parse_string(FileAccess.get_file_as_string(CHARACTER))
	return j if typeof(j) == TYPE_DICTIONARY else {}


func _bind_roles() -> void:
	"""Bind idle/walk/run/attack to whatever this GLB's clips are called.

	Declared names first, then the role word itself, then any clip that CONTAINS the role
	word, then idle. A rigged model that names its clips for what they do therefore drops
	in with no edit at all, and one that does not is one line of JSON -- neither needs a
	change to this script, which is the point of the slot."""
	var want: Dictionary = cfg.get("clips", {})
	var have := _clip_len.keys()
	for role in ["idle", "walk", "run", "attack"]:
		var pick := ""
		var declared := String(want.get(role, ""))
		if declared != "" and _clip_len.has(declared):
			pick = declared
		elif _clip_len.has(role):
			pick = role
		else:
			for n in have:
				if String(n).to_lower().contains(role):
					pick = String(n)
					break
		_roles[role] = pick
	if String(_roles.get("idle", "")) == "" and have.size() > 0:
		_roles["idle"] = String(have[0])
	for role in ["walk", "run", "attack"]:
		if String(_roles.get(role, "")) == "":
			_roles[role] = _roles["idle"]
	print("character: %s  clips %s -> %s" %
		[String(cfg.get("model", "?")).get_file(), str(have), str(_roles)])


func set_figure_scale(s: float) -> void:
	"""TRUE SCALE, on demand. 1.25178 is the painted world's own metric -- the art draws a
	person larger than the world's metres say -- and T9-0 asks what he looks like at 1.0,
	a 1.85 m man among props modelled at true size. The capsule and the ink width follow,
	or he keeps a collider and a line built for a bigger man."""
	_figure_scale = s
	var shape := get_child(0) as CollisionShape3D
	if shape != null and shape.shape is CapsuleShape3D:
		var cap := shape.shape as CapsuleShape3D
		cap.height = float(cfg.get("model_height_m", 1.8)) * s
		cap.radius = 0.35 * s
		shape.position = Vector3(0, cap.height * 0.5, 0)
	if _outline != null and _mesh != null:
		var ms: float = maxf(_mesh.global_transform.basis.get_scale().x, 1e-9) / maxf(_rig.scale.x, 1e-9)
		(_outline.material_override as ShaderMaterial).set_shader_parameter("width_model",
			(float(cfg.get("outline_px", LINE_PX)) / PPM) / maxf(s * ms, 1e-9))
	_drive()


func _find(n: Node, cls: String) -> Node:
	if n.get_class() == cls:
		return n
	for c in n.get_children():
		var r := _find(c, cls)
		if r != null:
			return r
	return null


func _set_layer(n: Node, layer: int) -> void:
	if n is VisualInstance3D:
		(n as VisualInstance3D).layers = layer
	for c in n.get_children():
		_set_layer(c, layer)


func _style() -> void:
	# LIT here, unlike the T3 skin. In the 2D scene the knight was composited into a
	# painting and had to carry his own light; here he is the one object in a real
	# scene with real lights, and the whole point of item 4 is to see whether that
	# makes him sit IN the painting rather than on top of it.
	var src := _mesh.get_active_material(0) as BaseMaterial3D
	var m := StandardMaterial3D.new()
	m.albedo_texture = src.albedo_texture if src != null and src.albedo_texture != null \
		else (src.emission_texture if src != null else null)
	m.roughness = 0.62
	m.metallic = 0.25
	_mesh.material_override = m
	_mesh.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON


func _add_outline() -> void:
	var sh := Shader.new()
	sh.code = """
shader_type spatial;
render_mode unshaded, cull_front, depth_draw_opaque, shadows_disabled;
uniform float width_model = 0.01;
uniform vec4 line_color : source_color = vec4(0.055, 0.043, 0.063, 1.0);
void vertex() { VERTEX += normalize(NORMAL) * width_model; }
void fragment() { ALBEDO = line_color.rgb; }
"""
	var mat := ShaderMaterial.new()
	mat.shader = sh
	# 1.1 output px, in metres, in model units. The world camera is orthographic at a
	# known px/m, so this is one number and not a distance-dependent one.
	var w_world := float(cfg.get("outline_px", LINE_PX)) / PPM
	# The shader offsets VERTEX, which is in the MESH's own units -- and a rig authored in
	# centimetres arrives with a 0.0109 scale on its mesh node, so a width in metres would
	# come out a hundredth of the line it should be. Measure the mesh's own scale instead
	# of assuming the model is in metres.
	var ms: float = maxf(_mesh.global_transform.basis.get_scale().x, 1e-9)
	mat.set_shader_parameter("width_model", w_world / maxf(_figure_scale * ms, 1e-9))
	_outline = MeshInstance3D.new()
	_outline.name = "InkLine"
	_outline.mesh = _mesh.mesh
	_outline.skin = _mesh.skin
	_mesh.get_parent().add_child(_outline)
	_outline.transform = _mesh.transform
	if _skel != null:
		_outline.skeleton = _outline.get_path_to(_skel)
	_outline.material_override = mat
	_outline.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF


func _read_socket() -> void:
	var prop: Dictionary = cfg.get("prop", {})
	var path := String(prop.get("socket", ""))
	if path == "" or not FileAccess.file_exists(path):
		return
	var j = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(j) != TYPE_DICTIONARY:
		return
	# The same change of basis and half-turn the chartest build needed: the socket was
	# fitted in Blender (Z-up) and this runtime is Y-up, so its rotation is conjugated
	# rather than applied, and the two number the haft's ends oppositely.
	var C := Basis.from_euler(Vector3(-PI / 2.0, 0.0, 0.0))
	var e = j.get("rotation_euler_xyz_deg", [0, 0, 0])
	var rb := Basis.from_euler(Vector3(deg_to_rad(float(e[0])), deg_to_rad(float(e[1])),
									   deg_to_rad(float(e[2]))))
	_socket_basis = C * rb * C.inverse() * Basis.from_euler(Vector3(PI, 0.0, 0.0))
	var o = j.get("offset", [0, 0, 0])
	var s = j.get("scale", [1, 1, 1])
	var k: float = maxf(float(s[0]), 1e-6)
	_socket_offset = C * Vector3(float(o[0]) / k, float(o[1]) / k, float(o[2]) / k)


func _add_pollaxe() -> void:
	var prop: Dictionary = cfg.get("prop", {})
	var model := String(prop.get("model", ""))
	var bone := String(prop.get("bone", "RightHand"))
	if _skel == null or model == "" or not ResourceLoader.exists(model):
		return
	if _skel.find_bone(bone) < 0:
		return
	_attach = BoneAttachment3D.new()
	_skel.add_child(_attach)
	_attach.bone_name = bone
	_pollaxe = (load(model) as PackedScene).instantiate()
	_skel.get_parent().add_child(_pollaxe)
	for mi in _pollaxe.find_children("*", "MeshInstance3D", true, false):
		var src := (mi as MeshInstance3D).get_active_material(0) as BaseMaterial3D
		var m := StandardMaterial3D.new()
		if src != null:
			m.albedo_texture = src.albedo_texture if src.albedo_texture != null else src.emission_texture
		m.roughness = 0.7
		(mi as MeshInstance3D).material_override = m
	_set_layer(_pollaxe, CHAR_LAYER)


func _place_pollaxe() -> void:
	if _pollaxe == null or _attach == null:
		return
	var t := _attach.global_transform
	var b: Basis = t.basis.orthonormalized()
	_pollaxe.global_transform = Transform3D(b * _socket_basis * _figure_scale,
											t.origin + b * _socket_offset * _figure_scale)


func _azimuth_for(f: String) -> float:
	var t := {"S": 0.0, "SE": 45.0, "E": 90.0, "NE": 135.0,
			  "N": 180.0, "NW": 225.0, "W": 270.0, "SW": 315.0}
	return float(t.get(f, 0.0))


# --- movement, in CANVAS pixels ------------------------------------------------
func canvas_velocity_to_world(v_px: Vector2) -> Vector3:
	"""A canvas-space velocity as a velocity on the ground.

	The 2D route moves 247 px/s in CANVAS pixels, and the canvas is an elevated
	orthographic view, so a metre of ground travelled up-screen is foreshortened while a
	metre travelled across-screen is not. Moving the body at a fixed metres-per-second
	would therefore travel visibly slower up the screen than across it. Solving for the
	ground vector whose PROJECTION is the wanted canvas velocity keeps the feel the 2D
	route has: level-local +x is exactly the guide camera's right, and level-local +z
	projects onto its up at -sin(pitch)."""
	var a := v_px.x / PPM
	var lz := Vector3(sin(deg_to_rad(47.0)), 0.0, cos(deg_to_rad(47.0)))
	var k := -lz.dot(up)                       # = sin(pitch)
	var b := (v_px.y / PPM) / maxf(k, 1e-6)
	return right * a + lz * b


func attacking() -> bool:
	if _tree != null:
		return bool(_tree.get("parameters/oneshot/active"))
	return _attack_t > 0.0


func try_attack() -> bool:
	"""Start the slash if one is not already running. No re-trigger mid-swing: the clip's
	own length IS the cooldown, which is also the only honest answer available -- an
	AnimationNodeAnimation restarts when its clip NAME changes, so re-selecting `attack`
	while attack is playing would not restart it and the input would silently do nothing."""
	if attacking():
		return false
	if _tree != null:
		_tree.set("parameters/oneshot/request", AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE)
		return true
	_attack_t = float(_clip_len.get(String(_roles.get("attack", "attack")), 1.5))
	return true


func _physics_process(dt: float) -> void:
	if Input.is_action_just_pressed("attack"):
		try_attack()
	drive_dir(Vector2(
		Input.get_action_strength("move_right") - Input.get_action_strength("move_left"),
		Input.get_action_strength("move_down") - Input.get_action_strength("move_up")),
		Input.is_action_pressed("run_modifier"), dt)


func drive_dir(dir: Vector2, running: bool, dt: float, hold := "") -> void:
	"""One step of movement from a CANVAS direction, with a human beat on either end.

	ONE SPEED DRIVES BOTH THE BODY AND THE BLEND, and that is the whole of the no-slide
	guarantee. If the animation blended on the key and the body moved at the key, a ramp
	would still be honest; but if either smoothed and the other did not, the feet would
	slide for exactly as long as the ramp lasted. So the smoothed speed is the only speed:
	the body travels at it and the blend space is positioned at it.

	Accel and decel have different time constants because starting and stopping do not feel
	alike -- and because stopping from a run has further to come down than stopping from a
	walk, an exponential gives the run the longer stop for free."""
	var tr: Dictionary = cfg.get("transitions", {})
	var want := 0.0
	if dir.length() > 0.01:
		dir = dir.normalized()
		_move_dir = dir
		want = float(cfg.get("run_px_s", RUN_PX_S)) if running \
			else float(cfg.get("walk_px_s", WALK_PX_S))
	if attacking():
		want = 0.0                       # the slash roots him, as before
	var tau: float = float(tr.get("accel_tau_s", 0.10)) if want > _speed \
		else float(tr.get("decel_tau_s", 0.15))
	_speed += (want - _speed) * (1.0 - exp(-dt / maxf(tau, 1e-4)))
	if want <= 0.0 and _speed < float(tr.get("stop_snap_px_s", 5.0)):
		_speed = 0.0                     # an exponential never arrives; a walker does
	if _tree != null:
		_tree.set("parameters/loco/blend_position", _speed)
	# the state name is kept for the capture tools that read it
	if attacking():
		state = "attack"
	elif _speed <= 0.0:
		state = "idle"
	elif _speed > float(cfg.get("walk_px_s", WALK_PX_S)) * 1.2:
		state = "run"
	else:
		state = "walk"
	if hold != "":
		state = hold
	if _move_dir.length() > 0.01:
		facing = _facing_for(_move_dir)
	var v := canvas_velocity_to_world(_move_dir * _speed)
	velocity = Vector3(v.x, velocity.y - 18.0 * dt, v.z)
	# MOVE_AND_SLIDE PICKS ITS OWN DELTA, and which one it picks depends on WHERE IT IS
	# CALLED FROM: the physics delta inside a physics frame, the PROCESS delta outside one.
	# Compensating for whichever it is about to use makes one call mean one `dt` of travel.
	var implicit: float = get_physics_process_delta_time() if Engine.is_in_physics_frame() \
		else get_process_delta_time()
	var boost: float = dt / maxf(implicit, 1e-6)
	velocity *= boost
	move_and_slide()
	velocity /= boost
	if is_on_floor():
		velocity.y = 0.0
	_drive(dt)
	_place_pollaxe()


func speed_px_s() -> float:
	return _speed


func _facing_for(d: Vector2) -> String:
	var ang := rad_to_deg(atan2(-d.y, d.x))
	var names := ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]
	var i := int(round(ang / 45.0)) % 8
	if i < 0:
		i += 8
	return names[i]


func _drive(dt := 0.0) -> void:
	"""The yaw, turned rather than snapped.

	A facing that jumps 45 degrees in a frame is the same defect as a pose that jumps: the
	eye cannot read it as movement. The target comes from the direction he is actually
	travelling when he is travelling, and from the facing name when he is not, so a tool
	that sets `facing` directly still turns him."""
	var wf: Vector3
	if _move_dir.length() > 0.01 and _speed > 0.0:
		wf = canvas_velocity_to_world(_move_dir)
	else:
		wf = canvas_velocity_to_world(_canvas_dir_for(facing))
	wf.y = 0.0
	if wf.length() < 1e-6:
		wf = Vector3.FORWARD
	wf = wf.normalized()
	var mf: Vector3 = _forward_axis
	var target: float = atan2(wf.x, wf.z) - atan2(mf.x, mf.z)
	if not _yaw_init:
		_yaw_cur = target
		_yaw_init = true
	elif dt > 0.0:
		var tau: float = float((cfg.get("transitions", {}) as Dictionary).get("turn_tau_s", 0.12))
		_yaw_cur = lerp_angle(_yaw_cur, target, clampf(1.0 - exp(-dt / maxf(tau, 1e-4)), 0.0, 1.0))
	else:
		_yaw_cur = target
	var yaw := Basis(Vector3.UP, _yaw_cur)
	_rig.global_transform = Transform3D(yaw.scaled(Vector3.ONE * _figure_scale), global_position)


func _canvas_dir_for(f: String) -> Vector2:
	"""The canvas direction a facing name means -- the exact inverse of _facing_for."""
	var names := ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]
	var i := names.find(f)
	if i < 0:
		i = 6
	var a := deg_to_rad(float(i) * 45.0)
	return Vector2(cos(a), -sin(a))


func play(clip: String) -> void:
	# ROLE OR CLIP NAME, either works: the scene and the capture tools drive "c_walk" by
	# habit, and a swapped-in model may not have a clip by that name. A role is resolved
	# through the binding; anything else is taken as a literal clip name.
	if _roles.has(clip):
		clip = String(_roles[clip])
	elif _anim != null and not _clip_len.has(clip):
		for role in _roles:
			if String(_roles[role]) != "" and String(clip).contains(role):
				clip = String(_roles[role])
				break
	if _anim == null or not _clip_len.has(clip):
		return
	var w := _layer_weight(clip)
	if _tree != null:
		_tree.set("parameters/blend/blend_amount", w)
	if clip == _clip:
		return
	_clip = clip
	if _tree != null:
		# The tools drive this by clip name; the tree is driven by speed and a one-shot.
		# Translate rather than make every caller learn the new shape.
		var atk_name := String(_roles.get("attack", "attack"))
		if clip == atk_name:
			try_attack()
		else:
			var sp := 0.0
			if clip == String(_roles.get("walk", "walk")):
				sp = float(cfg.get("walk_px_s", WALK_PX_S))
			elif clip == String(_roles.get("run", "run")):
				sp = float(cfg.get("run_px_s", RUN_PX_S))
			_speed = sp
			_tree.set("parameters/loco/blend_position", sp)
	elif _tree == null:
		_anim.speed_scale = 1.0
		_anim.play(clip, 0.15)


func status() -> Dictionary:
	return {"facing": facing, "state": state, "clip": _clip,
			"figure_scale": _figure_scale, "pos": [global_position.x, global_position.y, global_position.z]}
