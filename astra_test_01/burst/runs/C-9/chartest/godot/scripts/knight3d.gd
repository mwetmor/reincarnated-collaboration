extends Node2D
# C-9 R-C9-61 (T3): the Meshy knight as a REAL-TIME 3D character inside the 2D scene.
#
# WHAT THIS IS TESTING.  T1 asks "can an AI-3D + auto-rig pipeline produce sprite sheets
# the game can play."  T3 asks the other half: skip the sheets, put the rigged model in
# the running game and let the GPU turn it.  What that buys is every direction and every
# blend for free, instead of 8 directions x N states of baked cells.  What it costs is a
# 3D pipeline in a 2D game, and a look that has to be forced back into the painted
# register rather than arriving there.
#
# HOW IT LIVES IN A 2D SCENE.  A SubViewport renders the model; a Sprite2D shows that
# viewport's texture at the player's position, carrying the KEEPER'S OWN transform.  So
# from the 2D scene's point of view this skin is a sprite like the other two -- same
# node, same offset, same scale, same draw order -- and nothing about movement, collision
# or the camera changes when it is switched on.
#
# LINING UP WITH THE SPRITE VERSION is the whole point of the exercise: pressing K must
# not move or resize the figure.  That is not done by trusting a px/m number -- there are
# two in circulation for this character and they disagree by 6.6% (the dispatch's 117.5,
# from meshy_test/render_anim.py, and the sprite pipeline's own 110.185) -- it is done by
# rendering this camera and MEASURING where the soles and the crown land against the
# sprite cells that are actually in the build.  tools/fit_knight3d_camera.py does that
# fit and writes frames/knight3d_camera.json; this script reads it and asserts nothing.
#
# THE INK LINE is an inverted hull: the mesh drawn a second time, front faces culled,
# every vertex pushed out along its normal.  Under an ORTHOGRAPHIC camera a constant
# world-space push is a constant SCREEN-space width, which is exactly what a drawn line
# is -- no distance falloff to compensate for, and no depth/normal edge pass to run over
# the viewport.  It needs the smooth normals build_knight3d.py bakes in; with split
# normals the hull tears open along every shading seam.

const MODEL := "res://models/knight_t3.glb"
const POLLAXE := "res://models/pollaxe_t3.glb"
const CAMERA_FIT := "res://frames/knight3d_camera.json"

const FIGURE_M := 1.80                # measured in build_knight3d.py, not assumed
const ELEVATION_DEG := 19.77          # the sprite pipeline's fitted camera elevation
const LINE_PX := 1.1                  # ink weight, in output pixels
const LINE_COLOR := Color(0.055, 0.043, 0.063)

# Azimuth per facing, adopted verbatim from the sprite pipeline (knight3d/10_render.py
# AZI) so the two knights are photographed from the same eight places. The SIGN of the
# rotation is the one thing a table cannot settle -- it depends on which way the model
# faces after the glTF y-up conversion -- so it is verified by capture, not by argument.
const AZIMUTH := {
	"S": 0.0, "SE": 45.0, "E": 90.0, "NE": 135.0,
	"N": 180.0, "NW": 225.0, "W": 270.0, "SW": 315.0,
}

# The Keeper's state -> the knight's clip. The knight has no jump and no cast; his swing
# stands in for cast so the CAST button shows something of his own, and jump falls back
# to idle. Both substitutions are announced once on the console rather than left to look
# like a missing animation.
const CLIP_FOR := {
	"idle": "k_idle", "walk": "k_walk", "run": "k_run",
	"cast": "k_attack", "jump": "k_idle",
}

# Cycle lengths to match, in seconds, read from the Keeper's own SpriteFrames by
# tools/fit_knight3d_camera.py. Only walk and run are time-matched: the reason to retime
# a clip is that its stride has to agree with a GROUND SPEED, and idle has no ground
# speed to agree with. Forcing the 4.0 s idle into the Keeper's 2.0 s would double its
# tempo for no reason anyone could point at.
const RETIME := ["k_walk", "k_run"]

# The pollaxe carry. The haft's long axis is the model's local +Y and the HEAD is at
# +Y -- measured off the mesh (radius per slice along the haft jumps from 0.03 m to
# 0.21 m over the top third, where 4,300 of the 8,900 vertices sit), not guessed from a
# symmetric bounding box, which cannot tell a butt-spike from an axe head.
#
# Orientation comes from the BODY, not from the hand bone. Two reasons, and the second
# is the real one:
#   * the hand bone's own axes are a rigging convention nobody here chose, so a local
#     euler against them is a fitted constant with no meaning -- the first attempt,
#     (-100, 0, 0), laid the haft horizontally through the knight's waist;
#   * Meshy's motion library has no WEAPON-CARRY walk. Its 'walking_man' swings both
#     arms freely, so a haft welded to the wrist would windmill. Mounted to the body at
#     the hand's POSITION, it reads as carried. That is a stand-in, and the real fix is
#     upstream: a carry clip, or an additive arm pose over the generic one.
const MOUNT_OFFSET := Vector3(0.0, -0.03, 0.04)   # wrist -> where the fingers close
const CARRY_LEAN_DEG := -12.0         # haft leaned back over the shoulder
const HAFT_GRIP_M := 0.22             # mid-shaft to the grip; puts the butt near the
									  # ground and the head above the helm

var _vp: SubViewport
var _view: Sprite2D
var _cam: Camera3D
var _root: Node3D
var _skel: Skeleton3D
var _mesh: MeshInstance3D
var _outline: MeshInstance3D
var _anim: AnimationPlayer
var _attach: BoneAttachment3D
var _pollaxe: Node3D
var _active := false
var _ok := false
var _ppm := 110.185                   # px per metre of SCREEN height; refitted below
var _sole_row := 398.0
var _view_px := 512
var _aim_up := 0.0                    # metres along camera-up, from the fit
var _clip := ""
var _said := {}
var _facing := "S"
var _keeper_cycle := {}          # clip -> the Keeper's own cycle length, seconds
var _base_len := {}                   # clip -> its own length in seconds


func _ready() -> void:
	_vp = get_node_or_null(^"VP")
	_view = get_node_or_null(^"View")
	if _vp == null or _view == null:
		push_error("knight3d: VP/View missing; 3D skin disabled")
		return
	if not ResourceLoader.exists(MODEL):
		push_warning("knight3d: %s not built; 3D skin disabled" % MODEL)
		return

	_read_fit()
	_vp.size = Vector2i(_view_px, _view_px)
	_vp.own_world_3d = true
	_vp.transparent_bg = true
	_vp.disable_3d = false
	_vp.handle_input_locally = false
	_vp.msaa_3d = Viewport.MSAA_4X          # the ink line is 1.1 px; it needs the AA
	_vp.render_target_update_mode = SubViewport.UPDATE_DISABLED

	var packed: PackedScene = load(MODEL)
	_root = packed.instantiate()
	_vp.add_child(_root)
	_skel = _find(_root, "Skeleton3D") as Skeleton3D
	_mesh = _find(_root, "MeshInstance3D") as MeshInstance3D
	_anim = _find(_root, "AnimationPlayer") as AnimationPlayer
	if _mesh == null:
		push_error("knight3d: no MeshInstance3D in %s" % MODEL)
		return
	if _anim != null:
		# Drive the clip from physics, like the rest of the actor: on the render frame
		# the pose would advance out of step with the body it is standing on.
		_anim.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS
		for n in _anim.get_animation_list():
			_base_len[n] = _anim.get_animation(n).length

	_flatten_shading()
	_add_outline()
	_add_camera()
	_add_pollaxe()
	_view.texture = _vp.get_texture()
	_ok = true
	print("knight3d: ready  clips=%s  %d tris  %.3f px/m  sole row %.1f  line %.2f px"
		% [str(_base_len.keys()), _tris(), _ppm, _sole_row, LINE_PX])


func _read_fit() -> void:
	if not FileAccess.file_exists(CAMERA_FIT):
		push_warning("knight3d: no %s; using unfitted defaults (the figure may not line "
			% CAMERA_FIT + "up with the sprite skin). Run tools/fit_knight3d_camera.py.")
		_aim_up = (_sole_row - _view_px / 2.0) / _ppm
		return
	var j = JSON.parse_string(FileAccess.get_file_as_string(CAMERA_FIT))
	if typeof(j) != TYPE_DICTIONARY:
		return
	_ppm = float(j.get("px_per_m_screen", _ppm))
	_sole_row = float(j.get("sole_row", _sole_row))
	_view_px = int(j.get("view_px", _view_px))
	_aim_up = float(j.get("aim_up_m", (_sole_row - _view_px / 2.0) / _ppm))
	_keeper_cycle = j.get("keeper_cycle_s", {})


func _find(n: Node, cls: String) -> Node:
	if n.get_class() == cls:
		return n
	for c in n.get_children():
		var r := _find(c, cls)
		if r != null:
			return r
	return null


func _tris() -> int:
	var m := _mesh.mesh
	var t := 0
	for s in m.get_surface_count():
		t += m.surface_get_arrays(s)[Mesh.ARRAY_INDEX].size() / 3
	return t


# --- look ---------------------------------------------------------------------
func _flatten_shading() -> void:
	# Unlit, using the model's own baked colour map. The scene's 2D lighting does not
	# reach a 3D subviewport, so a lit material here would be lit by nothing and read as
	# a black cut-out; unlit is not a stylistic preference, it is the only way the
	# painted texture survives the trip.
	var src := _mesh.get_active_material(0) as BaseMaterial3D
	var m := StandardMaterial3D.new()
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.cull_mode = BaseMaterial3D.CULL_BACK
	m.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	if src != null:
		m.albedo_texture = src.albedo_texture
		if src.albedo_texture == null:
			m.albedo_texture = src.emission_texture
	if m.albedo_texture == null:
		push_warning("knight3d: no colour map on the model; the knight will be flat white")
	_mesh.material_override = m


func _model_to_world() -> float:
	# How many world metres one model unit spans, measured off the mesh rather than
	# inferred: this rig is centimetre-scaled at the armature, so a hand-written scale
	# constant here would be wrong by 100x in whichever direction guessed wrong.
	var h := _mesh.get_aabb().size.y
	if h <= 0.0:
		return 1.0
	return (_mesh.global_transform.basis * Vector3(0.0, h, 0.0)).length() / h


func _add_outline() -> void:
	var sh := Shader.new()
	sh.code = """
shader_type spatial;
// Inverted hull. Front faces culled, so only the back of the swollen copy survives,
// and it survives exactly where the real mesh does not cover it -- a rim of constant
// width. depth_draw_opaque keeps the line behind the body rather than over it.
render_mode unshaded, cull_front, depth_draw_opaque, shadows_disabled, ambient_light_disabled;
uniform float width_model = 0.01;
uniform vec4 line_color : source_color = vec4(0.055, 0.043, 0.063, 1.0);
void vertex() {
	VERTEX += normalize(NORMAL) * width_model;
}
void fragment() {
	ALBEDO = line_color.rgb;
}
"""
	var mat := ShaderMaterial.new()
	mat.shader = sh
	mat.set_shader_parameter("line_color", LINE_COLOR)

	_outline = MeshInstance3D.new()
	_outline.name = "InkLine"
	_outline.mesh = _mesh.mesh
	_outline.skin = _mesh.skin
	_mesh.get_parent().add_child(_outline)
	_outline.transform = _mesh.transform
	# Same skeleton, so the hull deforms with the body instead of standing still around
	# a moving figure. The NodePath is set after reparenting or it resolves to nothing.
	if _skel != null:
		_outline.skeleton = _outline.get_path_to(_skel)
	_outline.material_override = mat
	_outline.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_refresh_line_width()


func _refresh_line_width() -> void:
	if _outline == null:
		return
	# 1.1 output pixels -> metres -> model units. Orthographic projection is what makes
	# this a single number: under perspective the same world offset would be a thick
	# line near the camera and a hairline far from it.
	var m_per_px := 1.0 / _ppm
	var w_world := LINE_PX * m_per_px
	var w_model := w_world / maxf(_model_to_world(), 1e-6)
	(_outline.material_override as ShaderMaterial).set_shader_parameter("width_model", w_model)


func _add_camera() -> void:
	_cam = Camera3D.new()
	_cam.name = "Cam"
	_cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	_cam.size = float(_view_px) / _ppm          # metres of screen height
	_cam.near = 0.05
	_cam.far = 60.0
	_vp.add_child(_cam)
	_aim_camera("S")


func _aim_camera(facing: String) -> void:
	_facing = facing
	var az: float = deg_to_rad(float(AZIMUTH.get(facing, 0.0)))
	var el := deg_to_rad(ELEVATION_DEG)
	var d := 20.0
	# The offset from aim to camera. y-up Godot; the model faces +Z after the glTF
	# y-up conversion, so azimuth 0 puts the camera in front of it.
	var off := Vector3(sin(az) * cos(el), sin(el), cos(az) * cos(el)) * d

	# The aim has to sit a measured distance along the camera's OWN up vector for the
	# soles to land on the sprite set's ground row, and that vector depends on where the
	# camera is looking. So: orient once about the origin to read the up vector off the
	# resulting basis, then place for real. Deriving the vector by hand would be a second
	# copy of look_at's convention, free to drift from the first.
	_cam.position = off
	_cam.look_at(Vector3.ZERO, Vector3.UP)
	var up := _cam.global_transform.basis.y
	var aim := up * _aim_up
	_cam.position = aim + off
	_cam.look_at(aim, Vector3.UP)


# --- the pollaxe --------------------------------------------------------------
func _add_pollaxe() -> void:
	if _skel == null or not ResourceLoader.exists(POLLAXE):
		push_warning("knight3d: no skeleton or no pollaxe model; the knight goes unarmed")
		return
	var bone := _skel.find_bone("RightHand")
	if bone < 0:
		push_warning("knight3d: no RightHand bone; the knight goes unarmed")
		return
	_attach = BoneAttachment3D.new()
	_attach.name = "RightHandMount"
	_skel.add_child(_attach)
	_attach.bone_name = "RightHand"
	_pollaxe = (load(POLLAXE) as PackedScene).instantiate()
	# Sibling of the skeleton, not a child of the attachment: the armature is
	# centimetre-scaled, so anything parented under a bone inherits a 0.01 scale and a
	# 22 cm grip offset would become 2.2 mm. The mount transform is copied across each
	# frame with the scale normalised out instead -- see _place_pollaxe().
	_skel.get_parent().add_child(_pollaxe)
	for mi in _pollaxe.find_children("*", "MeshInstance3D", true, false):
		var src := (mi as MeshInstance3D).get_active_material(0) as BaseMaterial3D
		var m := StandardMaterial3D.new()
		m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		if src != null:
			m.albedo_texture = src.albedo_texture if src.albedo_texture != null else src.emission_texture
		(mi as MeshInstance3D).material_override = m
	_place_pollaxe()


func _place_pollaxe() -> void:
	if _pollaxe == null or _attach == null:
		return
	if _skel == null:
		return
	var hand: Vector3 = _attach.global_transform.origin
	# orthonormalized() because this armature is centimetre-scaled: its raw basis carries
	# a 0.01 factor that would shrink the pollaxe to a toothpick.
	var body: Basis = _skel.global_transform.basis.orthonormalized()
	var basis: Basis = body * Basis.from_euler(Vector3(deg_to_rad(CARRY_LEAN_DEG), 0.0, 0.0))
	# The haft's origin is mid-shaft (measured: 1.903 m long, origin within 10% of
	# centre), so mid-shaft sits HAFT_GRIP_M up the haft from the gripping hand.
	var origin: Vector3 = hand + body * MOUNT_OFFSET + basis.y * HAFT_GRIP_M
	_pollaxe.global_transform = Transform3D(basis, origin)


# --- the toggle's interface ----------------------------------------------------
func set_active(on: bool) -> void:
	_active = on and _ok
	visible = _active
	if _vp != null:
		# Stop rendering the 3D entirely when another skin is showing. A SubViewport left
		# on UPDATE_ALWAYS keeps drawing an invisible knight, and the Keeper -- the
		# DEFAULT -- would quietly pay for a feature nobody switched on.
		_vp.render_target_update_mode = (SubViewport.UPDATE_ALWAYS if _active
			else SubViewport.UPDATE_DISABLED)
	if _anim != null and not _active:
		_anim.stop()


func drive(state: String, facing: String) -> void:
	if not _active:
		return
	_aim_camera(facing)
	_place_pollaxe()
	if _anim == null:
		return
	var want: String = String(CLIP_FOR.get(state, "k_idle"))
	if not _base_len.has(want):
		if not _said.has(state):
			print("knight3d: no clip for state ", state, "; holding idle")
			_said[state] = true
		want = "k_idle"
	if want != _clip or not _anim.is_playing():
		if state != "idle" and state != "walk" and state != "run" and not _said.has(state):
			print("knight3d: state ", state, " -> clip ", want, " (the knight has no ", state, ")")
			_said[state] = true
		_clip = want
		_anim.speed_scale = _speed_for(want)
		_anim.play(want, 0.15)


func _speed_for(clip: String) -> float:
	if not RETIME.has(clip) or not _base_len.has(clip):
		return 1.0
	var target := float(_keeper_cycle.get(clip, 0.0))
	if target <= 0.0:
		return 1.0
	return float(_base_len[clip]) / target


# --- calibration hooks --------------------------------------------------------
# tools/fit_knight3d.gd drives the fit THROUGH THIS SCRIPT rather than standing up its
# own camera to measure. A calibration rig that builds its own copy of the thing it is
# calibrating measures the copy, and the copy is free to diverge from what ships.
func set_fit(ppm: float, aim_up_m: float) -> void:
	_ppm = ppm
	_aim_up = aim_up_m
	if _cam != null:
		_cam.size = float(_view_px) / _ppm
	_refresh_line_width()
	_aim_camera(_facing)


func set_armed(on: bool) -> void:
	if _pollaxe != null:
		_pollaxe.visible = on


func play_clip(clip: String, at: float) -> void:
	if _anim == null or not _base_len.has(clip):
		return
	_clip = clip
	_anim.speed_scale = 1.0
	_anim.play(clip)
	_anim.seek(at, true)


func viewport() -> SubViewport:
	return _vp


func clip_length(clip: String) -> float:
	return float(_base_len.get(clip, 0.0))


func status() -> Dictionary:
	return {
		"ok": _ok, "active": _active, "clip": _clip,
		"tris": _tris() if _mesh != null else 0,
		"px_per_m": _ppm, "sole_row": _sole_row, "aim_up_m": _aim_up,
		"cam_size_m": _cam.size if _cam != null else 0.0,
		"line_px": LINE_PX, "armed": _pollaxe != null,
		"clips": _base_len.keys(),
	}
