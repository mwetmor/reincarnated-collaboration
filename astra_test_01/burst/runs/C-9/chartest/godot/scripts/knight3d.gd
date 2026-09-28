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

# Azimuth per facing, adopted from the sprite pipeline (knight3d/10_render.py AZI) so
# the two knights are photographed from the same eight places.
#
# AZIMUTH_SIGN is the correction Matt caught on the live route: "with the Meshy version,
# E and W are inverted." The table was right and the sense of rotation was not.
#
# The shape of the error names its own fix. A reversed rig forward is a 180 deg offset
# and swaps BOTH axes: E with W and N with S. What was on the route swapped E and W
# while N and S stayed correct -- verified by where the pollaxe lands, since it is in
# the RIGHT hand and so appears on the viewer's left from the front and on the right
# from behind, which is what the captures show. Only a SIGN flip does that: az -> -az
# fixes E (90) and W (270) while leaving S (0) and N (180) untouched.
#
# My first facing check compared the three skins at ONE direction, saw them agree, and
# called the convention settled. Agreement at a single direction cannot tell "all
# correct" from "all mirrored" -- and an E/W swap is invisible to it by construction.
# tools/facing_probe.gd now walks all eight, and facing_screen_x() below lets the check
# be an assertion rather than a look.
const AZIMUTH_SIGN := -1.0
const AZIMUTH := {
	"S": 0.0, "SE": 45.0, "E": 90.0, "NE": 135.0,
	"N": 180.0, "NW": 225.0, "W": 270.0, "SW": 315.0,
}

# The Keeper's state -> the knight's clip. The knight has no jump and no cast; his swing
# stands in for cast so the CAST button shows something of his own, and jump falls back
# to idle. Both substitutions are announced once on the console rather than left to look
# like a missing animation.
# Two clip sets. The weapon decides which locomotion is right: Meshy's motion library
# swings both arms free, which is correct unarmed and windmills a polearm; the
# text-to-motion CARRY clips hold the right hand at chest height for one. The attack
# exists once and serves both.
const CLIP_ARMED := {
	"idle": "c_idle", "walk": "c_walk", "run": "c_run",
	"cast": "k_attack", "jump": "c_idle",
}
const CLIP_BARE := {
	"idle": "k_idle", "walk": "k_walk", "run": "k_run",
	"cast": "k_attack", "jump": "k_idle",
}

# Cycle lengths to match, in seconds, read from the Keeper's own SpriteFrames by
# tools/fit_knight3d_camera.py. Only walk and run are time-matched: the reason to retime
# a clip is that its stride has to agree with a GROUND SPEED, and idle has no ground
# speed to agree with. Forcing the 4.0 s idle into the Keeper's 2.0 s would double its
# tempo for no reason anyone could point at.
const RETIME := ["k_walk", "k_run", "c_walk", "c_run"]

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
# The pollaxe socket, read from meshy_t1/work/socket_pollaxe.json -- the knight3d
# session's MEASURED bone-space transform, including the blade bearing they fitted so
# the axe fan reads wide from the directions the player sees most. Reused rather than
# re-derived: two sessions fitting the same grip independently is two answers.
#
# Read at runtime, not transcribed, so their re-fit reaches this build by re-running.
const SOCKET_JSON := "res://frames/socket_pollaxe.json"
const HAFT_LEN_M := 1.903      # measured in build_knight3d.py, head at local +Y

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
var _socket_basis := Basis()
var _socket_offset := Vector3.ZERO
var _armed := true
var _clip_len := {}              # clip -> ONE STRIDE in seconds, measured at build time
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

	if FileAccess.file_exists("res://frames/knight_t3_clips.json"):
		var cj = JSON.parse_string(FileAccess.get_file_as_string("res://frames/knight_t3_clips.json"))
		if typeof(cj) == TYPE_DICTIONARY:
			_clip_len = cj.get("clips", {})
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
	var az: float = deg_to_rad(AZIMUTH_SIGN * float(AZIMUTH.get(facing, 0.0)))
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
	_read_socket()
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


func _read_socket() -> void:
	if not FileAccess.file_exists(SOCKET_JSON):
		push_warning("knight3d: no %s; the pollaxe will sit at the bare hand origin"
			% SOCKET_JSON)
		return
	var j = JSON.parse_string(FileAccess.get_file_as_string(SOCKET_JSON))
	if typeof(j) != TYPE_DICTIONARY:
		return
	# The socket was FITTED IN BLENDER, which is Z-up; Godot and the exported glTF are
	# Y-up. Applying its euler and its offset as written puts the axe head at the
	# knight's knee -- upright, near the hand, and upside down, which is what a rotation
	# applied in the wrong frame looks like when the frames differ by one axis swap.
	#
	# Blender (x, y, z) maps to glTF (x, z, -y), which is a -90 deg turn about X. A
	# POINT is carried by that map; a ROTATION has to be conjugated by it, C*R*C_inv,
	# or it is a rotation about the wrong axes. The same C also carries the weapon's own
	# long axis, which is Blender Z in their frame and glTF Y in mine -- so one change of
	# basis settles the bone frame and the weapon frame together, rather than two
	# separate hand-fitted corrections that could each be wrong in a compensating way.
	var C := Basis.from_euler(Vector3(-PI / 2.0, 0.0, 0.0))
	var e = j.get("rotation_euler_xyz_deg", [0, 0, 0])
	var r_blender := Basis.from_euler(Vector3(
		deg_to_rad(float(e[0])), deg_to_rad(float(e[1])), deg_to_rad(float(e[2]))))
	# END-FOR-END. After the change of basis the haft sits upright and through the fist
	# -- both assertions pass -- with the axe head 80 px BELOW it, in all eight
	# directions. The socket file and this build number the haft's ends oppositely:
	# `grip_below_fraction` says their grip is measured DOWN from the head, while the
	# head in pollaxe_t3.glb is at local +Y (measured: the per-slice radius along the
	# haft goes 0.03 m -> 0.21 m over the top third). A half turn about the weapon's own
	# X puts the head up without disturbing where the haft crosses the hand.
	#
	# It also leaves their fitted blade bearing intact: that fit maximises the apparent
	# fan width |sin(a-b)|, which is unchanged by a half turn.
	#
	# "Upright" could not have caught this -- an inverted pollaxe is exactly as vertical
	# as a carried one, and the angle check passed on all eight while the head was at the
	# knight's knee. Hence a separate assertion for which END is up.
	_socket_basis = C * r_blender * C.inverse() * Basis.from_euler(Vector3(PI, 0.0, 0.0))
	var o = j.get("offset", [0, 0, 0])
	# The file states its own units through `scale`: ~100 means the offset is in the
	# armature's centimetres. Dividing by it makes this a length in metres rather than a
	# number that happens to be right on one rig.
	var s = j.get("scale", [1, 1, 1])
	var k: float = maxf(float(s[0]), 1e-6)
	_socket_offset = C * Vector3(float(o[0]) / k, float(o[1]) / k, float(o[2]) / k)
	print("knight3d: socket offset %s m, euler %s deg (from %s)"
		% [str(_socket_offset), str(e), SOCKET_JSON])


func _place_pollaxe() -> void:
	"""Mount the pollaxe on the RIGHT-HAND bone: position AND rotation.

	The first version took only the hand's POSITION and got its orientation from the
	body, because the motion library's free-swinging arms would have windmilled a haft
	welded to the wrist. With the carry clips that reason is gone -- the hand is
	authored holding a polearm -- and a socket that ignores the wrist cannot follow it,
	which is what "the poleaxe floats near the character awkwardly" looks like.

	The bone's basis is orthonormalized because this armature is centimetre-scaled: its
	raw basis carries a 0.01 factor that would shrink the pollaxe to a toothpick. The
	socket offset is therefore applied in METRES, converted from the file's own
	centimetre units by its declared scale, rather than inherited."""
	if _pollaxe == null or _attach == null:
		return
	var t := _attach.global_transform
	var b: Basis = t.basis.orthonormalized()
	var basis: Basis = b * _socket_basis
	_pollaxe.global_transform = Transform3D(basis, t.origin + b * _socket_offset)


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
	var set_now: Dictionary = CLIP_ARMED if (_armed and _pollaxe != null) else CLIP_BARE
	var want: String = String(set_now.get(state, set_now.get("idle", "k_idle")))
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
	"""Match the Keeper's cadence per STRIDE, not per clip.

	The library walk is one stride in 1.03 s; the carry walk is three in 3.37 s. Scaling
	whole clips onto her 0.58 s stride would run the carry walk at nearly six times
	speed. frames/knight_t3_clips.json carries the stride length measured at build time
	from a foot's vertical track, so the runtime does not re-derive it and cannot
	disagree with the file it shipped from."""
	if not RETIME.has(clip):
		return 1.0
	var stride := float((_clip_len.get(clip, {}) as Dictionary).get("seconds", 0.0))
	if stride <= 0.0:
		stride = float(_base_len.get(clip, 0.0))
	var key := "k_run" if clip.ends_with("run") else "k_walk"
	var target := float(_keeper_cycle.get(key, 0.0))
	if target <= 0.0 or stride <= 0.0:
		return 1.0
	return stride / target


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
	_armed = on
	if _pollaxe != null:
		_pollaxe.visible = on
	_clip = ""        # force the clip set to be re-picked on the next drive()


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


# --- measurements, so facing and weapon can be ASSERTED rather than eyeballed --------
func _forward_world() -> Vector3:
	"""Which way the body is actually pointing, derived from the FEET.

	Not from a bone's local axis: which axis of a hand or a hip means "forward" is a
	rigging convention this project did not choose and cannot check. Toes point the way
	a person walks, so ankle->toe is a direction with a real referent, and averaging the
	two feet cancels the stride. Horizontal component only -- a raised foot tilts up."""
	if _skel == null:
		return Vector3.ZERO
	var sum := Vector3.ZERO
	for pair in [["RightFoot", "RightToeBase"], ["LeftFoot", "LeftToeBase"]]:
		var a := _skel.find_bone(pair[0])
		var b := _skel.find_bone(pair[1])
		if a < 0 or b < 0:
			continue
		var pa: Vector3 = (_skel.global_transform * _skel.get_bone_global_pose(a)).origin
		var pb: Vector3 = (_skel.global_transform * _skel.get_bone_global_pose(b)).origin
		var d := pb - pa
		d.y = 0.0
		if d.length() > 1e-5:
			sum += d.normalized()
	return Vector3.ZERO if sum.length() < 1e-5 else sum.normalized()


func facing_check() -> Dictionary:
	"""Where the body points, in the CAMERA's terms -- which is how a player reads it.

	screen_x > 0 means the figure faces screen-right; toward_camera > 0 means it faces
	out of the screen. Those two signs pin all eight directions without an image."""
	if _cam == null:
		return {}
	var f := _forward_world()
	if f == Vector3.ZERO:
		return {"ok": false, "why": "no foot bones to derive forward from"}
	var b := _cam.global_transform.basis
	return {"ok": true, "facing": _facing,
			"screen_x": snappedf(f.dot(b.x), 0.001),
			"toward_camera": snappedf(f.dot(b.z), 0.001)}


func weapon_check() -> Dictionary:
	"""Is the pollaxe actually IN THE FIST, and does it stand up?

	Both measured analytically off the transforms and projected through the camera --
	no image analysis, so it is exact and cheap enough to run every frame of a probe.
	  haft_deg_from_vertical  the angle of the haft as drawn
	  grip_miss_px            how far the hand sits from the haft's line, on screen
	A haft that floats beside the hand and a haft that lies across the body are two
	different faults and this reports them separately."""
	if _pollaxe == null or _attach == null or _cam == null:
		return {"ok": false, "why": "unarmed"}
	var b := _cam.global_transform.basis
	var h: Vector3 = _pollaxe.global_transform.basis.y.normalized()
	var sx := h.dot(b.x)
	var sy := h.dot(b.y)
	var deg := rad_to_deg(atan2(absf(sx), absf(sy)))
	# screen-space distance from the hand to the haft's infinite line
	var hand: Vector3 = _attach.global_transform.origin
	var mid: Vector3 = _pollaxe.global_transform.origin
	var d := hand - mid
	var p := Vector2(d.dot(b.x), d.dot(b.y))
	var u := Vector2(sx, sy)
	var miss := 0.0
	if u.length() > 1e-6:
		u = u.normalized()
		miss = absf(p.x * u.y - p.y * u.x) * _ppm
	# Is the AXE HEAD at the top? "Upright" alone cannot tell a carried pollaxe from an
	# upside-down one -- both are vertical, and the angle check passed on all eight
	# directions while the head was down by the knight's knee. The head is at the
	# weapon's local +Y (measured: the radius per slice along the haft jumps from 0.03 m
	# to 0.21 m over the top third), so its height above the fist is the question.
	var head: Vector3 = mid + h * (HAFT_LEN_M * 0.5)
	var head_px := (head - hand).dot(b.y) * _ppm
	return {"ok": true, "haft_deg_from_vertical": snappedf(deg, 0.01),
			"grip_miss_px": snappedf(miss, 0.01),
			"head_above_fist_px": snappedf(head_px, 0.01), "clip": _clip}


func status() -> Dictionary:
	return {
		"ok": _ok, "active": _active, "clip": _clip,
		"tris": _tris() if _mesh != null else 0,
		"px_per_m": _ppm, "sole_row": _sole_row, "aim_up_m": _aim_up,
		"cam_size_m": _cam.size if _cam != null else 0.0,
		"line_px": LINE_PX, "armed": _pollaxe != null,
		"clips": _base_len.keys(),
	}
