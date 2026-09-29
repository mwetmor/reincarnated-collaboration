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
	cap.height = 1.8 * _figure_scale
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
	play(_roles.get("idle", ""))


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
	_set_morph("helmet" in on)


func cycle_gear() -> void:
	set_gear_stack(gear_stack + 1)


func _set_morph(on: bool) -> void:
	var want := String(cfg.get("morph_with_helmet", ""))
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


func _physics_process(dt: float) -> void:
	drive_dir(Vector2(
		Input.get_action_strength("move_right") - Input.get_action_strength("move_left"),
		Input.get_action_strength("move_down") - Input.get_action_strength("move_up")),
		Input.is_action_pressed("run_modifier"), dt)


func drive_dir(dir: Vector2, running: bool, dt: float, hold := "") -> void:
	"""One step of movement from a CANVAS direction.

	Split out of _physics_process so the capture tools can walk him the way the player
	does -- at his own speed, over the real ground, with move_and_slide -- instead of
	teleporting him frame to frame. A teleported body is the one thing that cannot show
	whether the feet slide, which is the whole reason the speeds were taken from the
	clips' stride in the first place."""
	# FROM THE CLIPS, not from the Keeper's numbers. A speed chosen independently of the
	# animation is a foot slide by construction; these come from the stance foot's own
	# travel per cycle (tools/probe_stride.gd) and are written into character.json.
	var speed: float = float(cfg.get("run_px_s", RUN_PX_S)) if running \
		else float(cfg.get("walk_px_s", WALK_PX_S))
	if dir.length() > 0.01:
		dir = dir.normalized()
		facing = _facing_for(dir)
		state = "run" if running else "walk"
	else:
		dir = Vector2.ZERO
		state = "idle"
	if hold != "":
		state = hold
	var v := canvas_velocity_to_world(dir * speed)
	velocity = Vector3(v.x, velocity.y - 18.0 * dt, v.z)
	# MOVE_AND_SLIDE PICKS ITS OWN DELTA, and which one it picks depends on WHERE IT IS
	# CALLED FROM: the physics delta inside a physics frame, the PROCESS delta outside one.
	# A capture loop that renders between ticks calls it from a process frame, so a body
	# asked for 201.7 canvas px/s walked 80.7 -- exactly 24/60 of it, the render delta over
	# the physics delta -- and the feet slid by that factor. It looked like slope loss and
	# was not: the ground along both paths measures 0.0 deg from horizontal. Compensating
	# for whichever delta it is about to use makes one call mean one `dt` of travel, from
	# anywhere.
	var implicit: float = get_physics_process_delta_time() if Engine.is_in_physics_frame() \
		else get_process_delta_time()
	var boost: float = dt / maxf(implicit, 1e-6)
	velocity *= boost
	move_and_slide()
	velocity /= boost
	if is_on_floor():
		velocity.y = 0.0
	_drive()
	_place_pollaxe()


func _facing_for(d: Vector2) -> String:
	var ang := rad_to_deg(atan2(-d.y, d.x))
	var names := ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]
	var i := int(round(ang / 45.0)) % 8
	if i < 0:
		i += 8
	return names[i]


func _drive() -> void:
	play(String(_roles.get(state, _roles.get("idle", ""))))
	# In TRUE 3D the body itself turns; there is no eight-direction set to pick from.
	#
	# The yaw is DERIVED, not tabulated. It takes the model's own forward axis onto the
	# world direction that this facing MOVES in -- through canvas_velocity_to_world, the
	# same map the movement uses -- so the body cannot face one way and travel another, and
	# a swapped-in model needs no constant here. The previous form added a flat 180 deg,
	# which is one model's convention written into the scene.
	var wf := canvas_velocity_to_world(_canvas_dir_for(facing))
	wf.y = 0.0
	if wf.length() < 1e-6:
		wf = Vector3.FORWARD
	wf = wf.normalized()
	var mf: Vector3 = _forward_axis
	var yaw := Basis(Vector3.UP, atan2(wf.x, wf.z) - atan2(mf.x, mf.z))
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
	if _anim == null or not _clip_len.has(clip) or clip == _clip:
		return
	_clip = clip
	_anim.speed_scale = 1.0
	_anim.play(clip, 0.15)


func status() -> Dictionary:
	return {"facing": facing, "state": state, "clip": _clip,
			"figure_scale": _figure_scale, "pos": [global_position.x, global_position.y, global_position.z]}
