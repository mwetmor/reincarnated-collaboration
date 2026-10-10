extends "res://scripts/slot_knight.gd"
## C-9 BV2F ARENA (R-C9-383 item 2) -- THE WARLORD AS THE LIVE 3D RIG, `-- --arena-hero 3d` (A/B; default sprite).
##
## The walk scene's own dark knight (data/slots/warlord.json through slot_knight.gd -> sorceress_knight.gd -> knight.gd,
## unchanged), driven by the ARENA instead of the keyboard: the arena's capsule is the body (its position is copied
## here every frame; this node never moves itself and collides with nothing), and KC2's events pick the clips:
##   movement      the proxy's real ground velocity -> knight.gd's own walk/run blend at the render rate (the no-slide
##                 speed rule: the blend is positioned at the speed he is actually moving)
##   channel       eor_begin / eor_end (slot_knight's spin clip over the tree)
##   Charge        the eor4x `charge` slide, warped onto the dash (grafted at load from the eor4x export, below)
##   Haste         the run at HASTE_RATE (the tree's time scale)
##   Battle Cry    the `chop` strike = his warcry (warlord.json clips_armed)
##   slash         the `slash` strike = his attack
##   hit / death   a red flash on the rig / the `death` clip, held
##   Might         a red RIM (fresnel) on every mesh -- the 3D twin of the sprite's outline
## The clock is the AnimationTree's at the render rate, so every pose is smooth -- the point of the A/B.

const Paths = preload("res://scripts/arena/arena_paths.gd")
static var EOR4X_GLB: String = Paths.eor4x_glb()      # R-C9-391: a REQUIRED input of the shared build (raw bytes)
const HASTE_RATE := 1.3
const RIM_SHADER := """
shader_type spatial;
render_mode unshaded, blend_add, depth_draw_never, cull_back, shadows_disabled;
uniform vec4 col : source_color = vec4(0.95, 0.04, 0.02, 1.0);
uniform float strength = 0.0;
uniform float flash = 0.0;
void fragment() {
	float f = pow(1.0 - clamp(dot(normalize(NORMAL), normalize(VIEW)), 0.0, 1.0), 2.2);
	ALBEDO = col.rgb * (f * strength * 1.6 + flash * 0.55);
	ALPHA = 1.0;
}
"""

var ext_pos := Vector3.ZERO
var ext_vel := Vector3.ZERO
var haste := false
var dead := false
var graft_report := {}
var _override_clip := ""
var _override_until := 0.0
var _override_t := 0.0
var _rim_mat: ShaderMaterial = null
var _rim_on := false
var _flash_t := 0.0
var might_until := 0.0
var _clock := 0.0


func _ready() -> void:
	super()
	collision_layer = 0
	collision_mask = 0
	_graft_eor4x()


## The two eor4x clips the walk scene's body lacks (charge, battlecry), read off the eor4x export (same rig, same
## exporter: same track paths) into this AnimationPlayer's library.
func _graft_eor4x() -> void:
	if _anim == null or not FileAccess.file_exists(EOR4X_GLB):
		graft_report = {"error": "no eor4x export at " + EOR4X_GLB}
		return
	var doc := GLTFDocument.new()
	var st := GLTFState.new()
	if doc.append_from_buffer(Paths.bytes(EOR4X_GLB), "", st) != OK:
		graft_report = {"error": "gltf read"}
		return
	var root := doc.generate_scene(st)
	var ap := _find(root, "AnimationPlayer") as AnimationPlayer
	var lib := _anim.get_animation_library("")
	var got := []
	if ap != null and lib != null:
		for nm in ["charge", "battlecry"]:
			if ap.has_animation(nm) and not _anim.has_animation(nm):
				var a: Animation = ap.get_animation(nm).duplicate(true)
				_deroot_xz(a)
				lib.add_animation(nm, a)
				_clip_len[nm] = a.length
				got.append(nm)
	root.free()
	graft_report = {"grafted": got}


## In place, as the arena moves him: the root bone's ground translation held at its first key (height kept).
static func _deroot_xz(a: Animation) -> void:
	for ti in a.get_track_count():
		if a.track_get_type(ti) != Animation.TYPE_POSITION_3D:
			continue
		var n := a.track_get_key_count(ti)
		if n == 0:
			continue
		var p0: Vector3 = a.track_get_key_value(ti, 0)
		for k in n:
			var p: Vector3 = a.track_get_key_value(ti, k)
			a.track_set_key_value(ti, k, Vector3(p0.x, p.y, p0.z))
		return                                  # the first position track is the root's


## Clips the tree does not carry (charge, death): played on the AnimationPlayer with the tree paused, then handed back.
func play_override(clip: String, dur: float, hold := false) -> void:
	if _anim == null or not _anim.has_animation(clip):
		return
	_override_clip = clip
	_override_t = 0.0
	_override_until = INF if hold else maxf(dur, 0.05)
	if _tree != null:
		_tree.active = false
	_anim.play(clip)
	_anim.speed_scale = (float(_clip_len.get(clip, dur)) / maxf(dur, 0.05)) if not hold else 1.0


func _end_override() -> void:
	_override_clip = ""
	_anim.speed_scale = 1.0
	_anim.stop()
	if _tree != null:
		_tree.active = true


## R-C9-392: the mace head, world -- the weapon bone's origin plus MACE_LEN along its +Y (the haft axis, grip -> head;
## eor_spin's own law: "the head = weapon_r origin + its +Y"). Falls back to his hand height in front of him.
const MACE_LEN := 1.05
var _wbone := -2
func mace_head() -> Vector3:
	if _skel == null:
		return global_position + Vector3.UP * 1.3
	if _wbone == -2:
		_wbone = -1
		for nm in ["weapon_r", "Weapon_R", "weapon.R", "hand_r", "RightHand", "mixamorig:RightHand"]:
			var i := _skel.find_bone(nm)
			if i >= 0:
				_wbone = i
				break
	if _wbone < 0:
		return global_position + Vector3.UP * 1.3
	var t: Transform3D = _skel.global_transform * _skel.get_bone_global_pose(_wbone)
	return t.origin + t.basis.y.normalized() * MACE_LEN


func strike(which: String) -> bool:
	if dead or _override_clip != "":
		return false
	return try_strike(which)


func die() -> void:
	dead = true
	eor_end()
	play_override("death", 0.0, true)


func flash_red() -> void:
	_flash_t = 0.18


func _physics_process(dt: float) -> void:
	# slot_knight's spin blend (its own _physics_process minus knight.gd's keyboard drive)
	if _eor_ok:
		_eor_w = move_toward(_eor_w, 1.0 if _eor_on else 0.0, dt / EOR_FADE_S)
		_tree.set("parameters/eor_blend/blend_amount", _eor_w)
	if _override_clip != "":
		_override_t += dt
		if _override_t >= _override_until:
			_end_override()
	arena_drive(dt)


## World velocity -> knight.gd's CANVAS velocity (the inverse of canvas_velocity_to_world) -> its own blend + yaw.
func world_to_canvas(v3: Vector3) -> Vector2:
	var v := Vector3(v3.x, 0.0, v3.z)
	var lz := Vector3(sin(deg_to_rad(47.0)), 0.0, cos(deg_to_rad(47.0)))
	var kk := -lz.dot(up)
	var r2 := Vector2(right.x, right.z)
	var l2 := Vector2(lz.x, lz.z)
	var det := r2.x * l2.y - r2.y * l2.x
	if absf(det) < 1e-6:
		return Vector2.ZERO
	var a := (v.x * l2.y - v.z * l2.x) / det
	var b := (r2.x * v.z - r2.y * v.x) / det
	return Vector2(a * PPM, b * PPM * maxf(kk, 1e-6))


func face_world(w: Vector3) -> void:
	var c := world_to_canvas(w)
	if c.length() > 1e-4:
		_move_dir = c.normalized()
		facing = _facing_for(_move_dir)


func arena_drive(dt: float) -> void:
	var cv := world_to_canvas(ext_vel)
	var want := cv.length()
	if want > 1.0:
		_move_dir = cv.normalized()
	if dead or attacking() or _eor_on:
		want = 0.0 if not _eor_on else want
	_foot_lock_tick(want)
	# the speed he IS moving at (the arena moved the body): no smoothing beyond a short ease, so the feet hold
	_speed = move_toward(_speed, want, maxf(want, _speed) * dt / 0.06)
	if _tree != null and _override_clip == "":
		_set_loco(_speed, dt)
		if haste:
			for tsn in ["ts_walk", "ts_run"]:
				_tree.set("parameters/%s/scale" % tsn, float(_tree.get("parameters/%s/scale" % tsn)) * HASTE_RATE)
	if _move_dir.length() > 0.01:
		facing = _facing_for(_move_dir)
	_drive(dt)
	_place_pollaxe()


func _process(dt: float) -> void:
	_clock += dt
	global_position = ext_pos
	# Might's rim and the hit flash: one overlay on every mesh, only while either shows
	var rim := _clock < might_until and not dead
	_flash_t = maxf(0.0, _flash_t - dt)
	var want_on := rim or _flash_t > 0.0
	if want_on != _rim_on:
		_set_rim(want_on)
	if _rim_on:
		_rim_mat.set_shader_parameter("strength", (0.75 + 0.25 * sin(_clock * TAU * 1.6)) if rim else 0.0)
		_rim_mat.set_shader_parameter("flash", _flash_t / 0.18)


func _set_rim(on: bool) -> void:
	if _rim_mat == null:
		var sh := Shader.new()
		sh.code = RIM_SHADER
		_rim_mat = ShaderMaterial.new()
		_rim_mat.shader = sh
	for n in find_children("*", "MeshInstance3D", true, false):
		var mi := n as MeshInstance3D
		if String(mi.name).ends_with("_ink") or String(mi.name) == "InkLine":
			continue
		mi.material_overlay = _rim_mat if on else null
	_rim_on = on
