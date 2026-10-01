extends Node3D
## C-9 T10-2 step 1 -- THE FROST KING'S BARROW, FULL AREA, AS A GAMEPLAY BLOCKOUT.
##
## Contract: gandalf's 2026-09-29-barrow-full-area-blockout-spec.md. R-C9-74: one flat play
## floor, elevation only by architected steps. R-C9-75: blockout first, painted over chunk by
## chunk. R-C9-73: fully generated -- nothing here is bought; every surface is code or the
## project's own generated models.
##
## EVERYTHING IS READ FROM data/barrow_full_layout.json, which tools/make_layout.py writes from
## the spec table. This file decides NOTHING about where things go. It builds what the layout
## says, in true metres, through the play camera's own ground basis, and it can say back what
## it built (build_records) so the placements can be checked against the table by measurement.
##
## THE ENCODING (spec § 4): the real models in FLAT GREY so the painter paints their true
## silhouettes; outcrops, shore rock and the mound as primitives; the ground in four flat tints
## (snow, path, ice, shrub) off a generated splat; the Barrow's 55-degree sun with soft shadows;
## the ONE pen -- paint_stack's screen-space ink pass exactly as it is at HEAD, plus the hull
## pen on the solid models and on him. No grade, no paper, no fog, no falling snow: those are
## the look, and this is the layout.
##
## knight.gd, gear.gd, foot_lock.gd, character.json AND nb-body.glb ARE BYTE COPIES OF THE
## INSTALLED ONES (cliffside3d at 4bef708a2: the armed-speed split, the foot-lock rollback) AND
## ARE NOT EDITED. paint_stack.gd, snow_field.gd and barrow_heather.gd are the installed copies
## too, with two marked additions for the painted Barrow (the pen's painted mark; the snow's
## shader hook).
##
## PAINTED (T10-2 step 4, `painted = true`, scenes/barrow_painted.tscn): the SAME build -- every
## collider, every transform, exactly as the blockout makes them -- then DRESSED in the painting
## (_dress_painted): the conductor's ruling "the painting is the world's light and its ink".
##
## KEYS: arrows/WASD move · Shift run · Space/LMB slash · X chop · C bash · B/RMB block ·
##       G gear · [ ] size   (the standard controls, from the HEAD input map)
##       V  the look stack (ramp + ink) off and on
##       K  the ink pass only
##       O  the layout overlay: bounds, arena, path band, tarn, mound foot, ring
##       U  the camera clamp to the painted window (OFF by default in v2 -- see _clamp_aim)
##
##   THE VIEW IS LOCKED TO 16:9 (project.godot: stretch canvas_items, aspect keep, base
##   1920 x 1080). Every window shows the same 19.1 x 13.4 m of ground; a wider or taller
##   screen gets bars. --view-check measures it from inside the running app.

const LAYOUT_JSON := "res://data/barrow_full_layout.json"
const PPM := 100.617553710938
const PL_PITCH_DEG := 52.95354112560294
const PL_YAW_DEG := 47.0
const CHAR_LAYER := 4
const CAM_LIFT_PX := 55.0
# The same standoff and shadow reach as barrow_world at HEAD, for the reasons written there: an
# orthographic standoff does not change the picture, but the shadow distance is measured from
# the camera, and 60 + 50 m is the pair known to put every caster inside the shadow map.
const CAM_STANDOFF := 60.0
const SHADOW_REACH_AHEAD := 50.0
const PLAY_M_PER_PX := 1.0 / PPM
const SUN_ELEV_DEG := 55.0
const SUN_SCREEN_AZ_DEG := 305.0
const HULL_PX := 1.1
const LINE_PX := 1.25             # the screen-space pen, in FRAME px (1920 x 1080); see _sync_post_scale
# knight.gd masks its body and its ground ray to CliffWorld.TERRAIN_BIT, which is 1 << 1.
# PaintStack.TERRAIN_BIT is the same number; both are asserted in _ready.
const TERRAIN_BIT := 1 << 1
const PROP_SINK_M := 0.02
const FLOOR_EXTENT := 46.0
const FLOOR_CELL := 2.0
const MOUND_CELL := 0.1
const LOW_M := 1.9                 # a footprint "at his height": what a 1.85 m man walks into
const RAW_KEYS := {"V": KEY_V, "K": KEY_K, "O": KEY_O, "U": KEY_U, "R": KEY_R, "H": KEY_H, "N": KEY_N}

var layout := {}
var cam: Camera3D
var sun: DirectionalLight3D
var env_node: WorldEnvironment
var knight: CharacterBody3D
var right := Vector3.RIGHT
var up := Vector3.UP
var fwd := Vector3.FORWARD
var u_hat := Vector3(cos(deg_to_rad(47.0)), 0.0, -sin(deg_to_rad(47.0)))
var v_hat := Vector3(-sin(deg_to_rad(47.0)), 0.0, -cos(deg_to_rad(47.0)))
var level: Node3D                  # local +x = u_hat, local -z = v_hat, local +y = up
var props_root: Node3D             # unrotated: models carry WORLD yaws from the manifests
var fbm: ImageTexture
var paper: ImageTexture
var post_mat: ShaderMaterial
var post_q: MeshInstance3D
var ground_mat: ShaderMaterial
var world_mats: Array[ShaderMaterial] = []
var _prop_inks: Array = []
var _char_saved := {}
var nodes := {}                    # placement id -> root Node3D
var built := {}                    # placement id -> what the build step knows about it
var report := {}
var stack_on := true
var ink_on := true
var clamp_on := false               # spec v2: the 4 x 4 window's margin makes the clamp unnecessary
var crucible_on := true              # the wave-arena marks: ON in the app, R hides them
var _crucible: Node3D
var _door_saved := {}
var overlay_on := false
var ready_done := false
var _overlay: Node3D
var _markers: Node3D
var _hud: Label
var _size_step := 0
var _tint := {}

@export var skip_character := false
## the painted Barrow: the blockout, dressed in the painting (see _dress_painted)
@export var painted := false
## the ground's painting: "as_painted" (the painting itself: its tufts stay, the 3D heather stands
## on them) or "inpainted" (the tufts taken out). The overlay check chose: on the painted tufts'
## pixels as_painted differs by 8.9, inpainted by 69.6 -- a juniper filled from the snow round it is
## a grey smear, and the 3D sprays cover 34% of what the painter painted (take/build/overlay_check.json)
@export var ground_variant := "as_painted"
var paint := {}                    # what the painted dress loaded, measured, and built
var paint_sun: DirectionalLight3D
## WHO WALKS THE PAINTED BARROW: "barbarian" (the default) or "sorceress" (?c=sorceress on the
## phone page; -- --c sorceress on the desktop). The blockout keeps him.
var who := "barbarian"
var spell_fx: Node3D
var meteor_fx: Node3D               # LANE B: her Meteor, 3D first (?meteor=b; scripts/meteor_fx.gd)
var touch                             # barrow_touch.gd, on the web or a touchscreen
var veil                              # warm_veil.gd, on the phone page
var _her_spell_buttons: Array = []    # FIRE BALL and METEOR, shown only while she holds the staff
var snow: SnowField
var snowfall: GPUParticles3D
var heather_mat: ShaderMaterial
var _heather_mmi: Array = []
var _paint_tex := {}
const WIND := Vector2(0.62, 0.78)   # the installed Barrow's (the wind the snow's streaks lie along)


func _ready() -> void:
	var t0 := Time.get_ticks_msec()
	if PaintStack.is_web():
		# THE WARMING VEIL (the phone page): the loading look stays up until the first draws have compiled
		veil = load("res://scripts/warm_veil.gd").new()
		veil.name = "WarmVeil"
		add_child(veil)
		veil.setup(self)
	layout = _read_json(LAYOUT_JSON)
	if layout.is_empty():
		push_error("barrow_full: no layout at %s" % LAYOUT_JSON)
		print("[barrow_full] FAILED: no layout")
		return
	assert(TERRAIN_BIT == PaintStack.TERRAIN_BIT and TERRAIN_BIT == CliffWorld.TERRAIN_BIT)
	for k in (layout["tints_srgb"] as Dictionary):
		var c: Array = layout["tints_srgb"][k]
		_tint[k] = Color(float(c[0]), float(c[1]), float(c[2]))
	_build_camera()
	_build_light_and_air()
	var t_tex := Time.get_ticks_msec()
	fbm = PaintStack.make_fbm_texture(512, 7411, 4)
	paper = PaintStack.make_paper_texture(512)
	t_tex = Time.get_ticks_msec() - t_tex
	level = Node3D.new()
	level.name = "Level"
	add_child(level)
	level.transform = Transform3D(Basis(u_hat, Vector3.UP, -v_hat), Vector3.ZERO)
	props_root = Node3D.new()
	props_root.name = "Props"
	add_child(props_root)
	_assert_level_frame()
	var t_b := Time.get_ticks_msec()
	_build_ground()
	_build_mound()
	_build_placements()
	_build_bounds()
	_build_overlay()
	_build_crucible()
	t_b = Time.get_ticks_msec() - t_b
	if skip_character:
		look_at_world(Vector3.ZERO)
	else:
		await _build_knight()
	_build_post()
	if painted:
		_dress_painted()
		set_crucible_visible(false)
	_build_hud()
	if painted and (PaintStack.is_web() or DisplayServer.is_touchscreen_available()):
		# THE THUMB STICK AND THE FOUR STRIKES (the installed Barrow's barrow_touch.gd), through the
		# input actions knight.gd reads. AFTER the HUD: the controls hide the keyboard's hint bar
		# when they show, and the first phone page drew it under them -- added before it existed
		var tc = load("res://scripts/barrow_touch.gd").new()
		add_child(tc)
		touch = tc
		if who == "sorceress":
			_touch_for_her(tc)
		elif who == "warlord" or slot.begins_with("barb_glad"):
			_touch_for_strikes(tc)
	if who == "sorceress":
		_build_fx_label()
	_check_key_collisions()
	_apply_stack()
	clamp_on = bool(layout.get("camera_clamp_default", false))
	report["build_ms"] = {"total": Time.get_ticks_msec() - t0, "generated_textures": t_tex,
						  "world": t_b}
	if MeteorFx.wanted(self):
		# LANE B METEOR (her page, ?meteor=b): built once here, warmed over the next frames, then it prints
		# "[meteor_b] armed". Without ?meteor=b nothing of it exists and nothing above has changed.
		meteor_fx = MeteorFx.attach(self)
	if veil != null:
		# the level's first draw, staged a few shaders per frame under the veil (warm_veil.gd)
		veil.stage_level(self)
	ready_done = true
	# ONE LINE ON STDOUT: the exported app's launch probe greps for it. The pck fence proves the
	# FILES shipped; only the running scene can say it built from them.
	print("[barrow_full] built placements=%d splat_ok=%s build_ms=%d" % [
		nodes.size(), str(report.get("ground", {}).get("splat_sha256_matches_layout", false)),
		int(report["build_ms"]["total"])])
	# AND THE VIEW IT WILL BE SEEN THROUGH: the launch probe checks this line as well.
	print("[barrow_full] view stretch=%s aspect=%s base=%dx%d" % _view_lock())
	if painted:
		# AND WHAT IT WORE: the launch probe greps this line. Every texture is read off its raw
		# bytes from the pck and its sha256 checked against the manifest by the running scene.
		print("[barrow_painted] " + _paint_launch_line())
		if PaintStack.is_web():
			# THE PHONE PAGE'S OWN LINE: tools/build_web_painted.sh's launch fence and the browser
			# test read it -- what it loaded, what it built, and what the web path did
			var cl: Dictionary = paint.get("compat_light", {})
			var pt: Dictionary = paint.get("loads", {}).get("painting.webp.bin", paint.get("loads", {}).get("painting.bin", {}))
			print("[barrow_painted] web: %s | painting_px=%s pen=%s ambient_moved=%s painted_no_ambient=%s colour=%s msaa=%d scale3d=%.2f" % [
				_paint_launch_line(), str(pt.get("px", "?")),
				"depth-only+stencil" if PaintStack.is_compatibility() else "full",
				str(cl.get("ramp_materials_set", "-")), str(cl.get("painted_no_ambient_by_design", "-")),
				JSON.stringify(paint.get("compat_color", {})), int(get_viewport().msaa_3d),
				get_viewport().scaling_3d_scale] + _her_line())
	get_viewport().size_changed.connect(_sync_post_scale)
	if "--frame-cost" in OS.get_cmdline_user_args():
		_frame_cost_mode()
	elif "--view-check" in OS.get_cmdline_user_args():
		_view_check_mode()


func _read_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var j = JSON.parse_string(FileAccess.get_file_as_string(path))
	return j if typeof(j) == TYPE_DICTIONARY else {}


# --- the frame ----------------------------------------------------------------------------
func _build_camera() -> void:
	"""barrow_world's camera law, unchanged: orthographic, pitch 52.95354112560294, yaw 47, size
	in metres of screen height over the FRAME's rows -- the viewport's visible rect, which the
	16:9 lock holds at 1080 in every window (a 2560 x 1440 fullscreen render included), so the
	frame is the same ground everywhere. Then the (u, v) ground basis is
	TAKEN FROM THIS CAMERA -- the spec says so -- and checked against the analytic one."""
	var p := deg_to_rad(PL_PITCH_DEG)
	var y := deg_to_rad(PL_YAW_DEG)
	var f := Vector3(-sin(y) * cos(p), -sin(p), -cos(y) * cos(p)).normalized()
	cam = Camera3D.new()
	cam.name = "PlayCamera"
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.size = float(_view_height()) / PPM
	cam.near = 0.05
	cam.far = CAM_STANDOFF + 300.0
	add_child(cam)
	cam.look_at_from_position(-f * CAM_STANDOFF, Vector3.ZERO, Vector3.UP)
	cam.current = true
	var b := cam.global_transform.basis
	right = b.x
	up = b.y
	fwd = -b.z
	var ua := Vector3(cos(y), 0.0, -sin(y))
	var va := Vector3(-sin(y), 0.0, -cos(y))
	var ul := Vector3(right.x, 0.0, right.z).normalized()
	var vl := Vector3(up.x, 0.0, up.z).normalized()
	u_hat = ul
	v_hat = vl
	report["camera"] = {
		"projection": "orthogonal", "pitch_deg": PL_PITCH_DEG, "yaw_deg": PL_YAW_DEG,
		"ortho_size_m": snappedf(cam.size, 0.0001), "viewport_rows": _view_height(),
		"px_per_m_screen_x": snappedf(PPM, 0.0001),
		"px_per_ground_m_up_screen": snappedf(PPM * sin(p), 0.0001),
		"ground_basis": {
			"u_hat_live": _v3(ul), "v_hat_live": _v3(vl),
			"u_hat_analytic": _v3(ua), "v_hat_analytic": _v3(va),
			"residual_u": (ul - ua).length(), "residual_v": (vl - va).length(),
			"u_dot_v": ul.dot(vl),
			"_used": "the LIVE basis, as the spec defines (u, v); the analytic one is the check"},
	}


func _assert_level_frame() -> void:
	var b := level.global_transform.basis
	report["level_frame"] = {
		"local_x_minus_u_hat": (b.x - u_hat).length(), "local_minus_z_minus_v_hat": (-b.z - v_hat).length(),
		"det": b.determinant(),
		"_": "the Level node carries the (u, v) frame: local (u, h, -v). Primitives are built in it."}


func _view_height() -> int:
	var vp := get_viewport()
	var h: int = int(vp.get_visible_rect().size.y) if vp != null else 1080
	return h if h > 0 else 1080


func _view_width() -> int:
	var vp := get_viewport()
	var w: int = int(vp.get_visible_rect().size.x) if vp != null else 1920
	return w if w > 0 else 1920


func uv_to_world(u: float, v: float, h := 0.0) -> Vector3:
	return u_hat * u + v_hat * v + Vector3(0.0, h, 0.0)


func world_to_uv(p: Vector3) -> Vector2:
	return Vector2(p.dot(u_hat), p.dot(v_hat))


func _L(u: float, h: float, v: float) -> Vector3:
	return Vector3(u, h, -v)


func look_at_world(aim: Vector3) -> void:
	cam.look_at_from_position(aim - fwd * CAM_STANDOFF, aim, Vector3.UP)


func _sync_post_scale() -> void:
	"""The pen's metres per px from the FRAME (1080 rows, which cam.size is set from), and its
	span in RENDER px scaled to match. Under the 16:9 lock, fullscreen on a 3440 x 1440 display
	renders the same 1920 x 1080 frame at 2560 x 1440: the same ground, px 4/3 finer.
	paint_stack's span is in render px, so without this the screen-space line would be 1.25
	render px -- 0.94 of a frame px -- while the hull ink, which is in metres, stays 1.1 frame
	px: two weights, set by the monitor. With it, the span covers the same metres at any
	resolution, the thresholds (in metres) mean the same thing, and the line keeps its weight."""
	if post_mat != null and cam != null:
		PaintStack.post_set(post_mat, "m_per_px", cam.size / maxf(float(_view_height()), 1.0))
		PaintStack.post_set(post_mat, "line_px", LINE_PX * _render_scale())


func _render_scale() -> float:
	"""Render px per frame px: 1.0 in a 1920 x 1080 window or a capture SubViewport, 4/3
	fullscreen at 1440 -- the scale of the viewport's final transform.

	NOT THE TEXTURE'S SIZE. Under canvas_items, fullscreen on the 3440 x 1440 display, the root
	viewport's texture REPORTS 3414 x 1920 while the image it yields is 2560 x 1440
	(tools/probe_view.gd, frame by frame): the reported size is the render size times the 2D
	stretch. The first version of this function read it, returned 16/9 instead of 4/3, and drew
	the pen 2.22 render px wide -- cleanly, with no error. The root Window's `size` is no better:
	it is the OS window, bars included."""
	var vp := get_viewport()
	if vp == null:
		return 1.0
	var s := vp.get_final_transform().get_scale().y
	return s if s > 0.0 else 1.0


func _render_px() -> Vector2i:
	"""The px actually drawn, from the frame and the final transform (see _render_scale)."""
	var vr := get_viewport().get_visible_rect().size
	return Vector2i(roundi(vr.x * _render_scale()), roundi(vr.y * _render_scale()))


func _view_lock() -> Array:
	var w := get_tree().root
	var modes := {Window.CONTENT_SCALE_MODE_DISABLED: "disabled",
				  Window.CONTENT_SCALE_MODE_CANVAS_ITEMS: "canvas_items",
				  Window.CONTENT_SCALE_MODE_VIEWPORT: "viewport"}
	var aspects := {Window.CONTENT_SCALE_ASPECT_IGNORE: "ignore", Window.CONTENT_SCALE_ASPECT_KEEP: "keep",
					Window.CONTENT_SCALE_ASPECT_KEEP_WIDTH: "keep_width",
					Window.CONTENT_SCALE_ASPECT_KEEP_HEIGHT: "keep_height",
					Window.CONTENT_SCALE_ASPECT_EXPAND: "expand"}
	return [String(modes.get(w.content_scale_mode, str(w.content_scale_mode))),
			String(aspects.get(w.content_scale_aspect, str(w.content_scale_aspect))),
			w.content_scale_size.x, w.content_scale_size.y]


func _v3(v: Vector3) -> Array:
	return [snappedf(v.x, 1e-6), snappedf(v.y, 1e-6), snappedf(v.z, 1e-6)]


# --- rule 3: one real light ---------------------------------------------------------------
func _build_light_and_air() -> void:
	var lights := Node3D.new()
	lights.name = "Lights"
	add_child(lights)
	sun = PaintStack.winter_sun(SUN_ELEV_DEG, SUN_SCREEN_AZ_DEG)
	lights.add_child(sun)
	sun.directional_shadow_max_distance = CAM_STANDOFF + SHADOW_REACH_AHEAD
	env_node = WorldEnvironment.new()
	env_node.name = "Env"
	env_node.environment = PaintStack.barrow_environment({})
	# NO FOG IN THE BLOCKOUT. The mist is part of the look; a guide the painter reads for
	# silhouettes and ground classes is clearer without a height term lifting every foot.
	env_node.environment.fog_enabled = false
	add_child(env_node)
	var sd := PaintStack.sun_screen_dir(sun, cam)
	report["light"] = {"elevation_deg": SUN_ELEV_DEG, "screen_azimuth_deg": SUN_SCREEN_AZ_DEG,
		"energy": sun.light_energy, "shadows": sun.shadow_enabled, "shadow_blur": sun.shadow_blur,
		"shadow_bias": sun.shadow_bias, "shadow_normal_bias": sun.shadow_normal_bias,
		"shadow_max_distance": sun.directional_shadow_max_distance,
		"screen_dir_from_sun": {"x_right": snappedf(sd.x, 0.001), "y_up": snappedf(sd.y, 0.001)},
		"fog": "off (blockout)", "grade_and_paper": "off (blockout)"}


func _flat_params(mark := 1.0) -> Dictionary:
	# flat: no mottle, no hatch, no wash in the light ramp, no snow layer
	return {"snow_amount": 0.0, "mottle_amp": 0.0, "hatch_amp": 0.0, "wash_amp": 0.0,
			"mesh_mark": mark}


func _flat_tex(c: Color) -> ImageTexture:
	var img := Image.create(4, 4, false, Image.FORMAT_RGB8)
	img.fill(c)
	img.generate_mipmaps()
	return ImageTexture.create_from_image(img)


# --- helpers for built geometry -----------------------------------------------------------
func _tri(vs: PackedVector3Array, ns: PackedVector3Array, a: Vector3, b: Vector3, c: Vector3,
		n: Vector3) -> void:
	# Godot's front face is CLOCKWISE seen from the front, so (b-a)x(c-a) must point AWAY from
	# the side the normal faces. Enforced per triangle rather than trusted: barrow_flat records
	# a ground that rendered 0 of 25,600 pixels because a hand-written order was reversed.
	if (b - a).cross(c - a).dot(n) > 0.0:
		var t := b
		b = c
		c = t
	vs.append(a)
	vs.append(b)
	vs.append(c)
	ns.append(n)
	ns.append(n)
	ns.append(n)


func _tri_n(vs: PackedVector3Array, ns: PackedVector3Array, a: Vector3, b: Vector3, c: Vector3,
		na: Vector3, nb: Vector3, nc: Vector3) -> void:
	if (b - a).cross(c - a).dot(na + nb + nc) > 0.0:
		var t := b
		b = c
		c = t
		var tn := nb
		nb = nc
		nc = tn
	vs.append(a)
	vs.append(b)
	vs.append(c)
	ns.append(na)
	ns.append(nb)
	ns.append(nc)


func _mesh(vs: PackedVector3Array, ns: PackedVector3Array, mat: Material, nm: String,
		parent: Node3D, shadows := true) -> MeshInstance3D:
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = vs
	arr[Mesh.ARRAY_NORMAL] = ns
	var m := ArrayMesh.new()
	m.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	var mi := MeshInstance3D.new()
	mi.name = nm
	mi.mesh = m
	mi.material_override = mat
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON if shadows \
		else GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	parent.add_child(mi)
	return mi


func _body(parent: Node3D, nm: String) -> StaticBody3D:
	var b := StaticBody3D.new()
	b.name = nm
	b.collision_layer = TERRAIN_BIT
	b.collision_mask = 0
	parent.add_child(b)
	return b


func _box(parent: Node3D, u0: float, u1: float, v0: float, v1: float, y0: float, y1: float) -> void:
	var cs := CollisionShape3D.new()
	var bx := BoxShape3D.new()
	bx.size = Vector3(u1 - u0, y1 - y0, v1 - v0)
	cs.shape = bx
	cs.position = _L((u0 + u1) * 0.5, (y0 + y1) * 0.5, (v0 + v1) * 0.5)
	parent.add_child(cs)


func _box_rot(parent: Node3D, mid: Vector2, length: float, thick: float, y0: float, y1: float,
		ang: float) -> void:
	"""A box whose long axis runs along direction `ang` in the (u, v) plane (from +u toward +v).
	rotation.y = ang turns local +x to (cos, 0, -sin) in the Level frame, which is (u, v) =
	(cos, sin) because the Level's local z is -v."""
	var cs := CollisionShape3D.new()
	var bx := BoxShape3D.new()
	bx.size = Vector3(length, y1 - y0, thick)
	cs.shape = bx
	cs.position = _L(mid.x, (y0 + y1) * 0.5, mid.y)
	cs.rotation = Vector3(0.0, ang, 0.0)
	parent.add_child(cs)


func _breaks(lo: float, hi: float, step: float, extra: Array) -> PackedFloat32Array:
	var s := {}
	var x := lo
	while x <= hi + 1e-6:
		s[snappedf(x, 1e-4)] = true
		x += step
	for e in extra:
		s[snappedf(float(e), 1e-4)] = true
	var a := s.keys()
	a.sort()
	return PackedFloat32Array(a)


# --- the ground ---------------------------------------------------------------------------
func _build_ground() -> void:
	"""The flat floor at y = 0 (R-C9-74), wearing the four tints through paint_stack's OWN
	ground shader: flat-colour 'tiles' and a splat generated from the layout's regions. The
	floor is built in the (u, v) frame so the passage behind the door can be cut out of it
	exactly -- the three steps go DOWN, below the floor, and a floor drawn over them would hide
	them."""
	var tiles := {"snow": _flat_tex(_tint["snow"]), "path": _flat_tex(_tint["path"]),
				  "rock": _flat_tex(_tint["rock"]), "heather": _flat_tex(_tint["shrub"]),
				  "ice": _flat_tex(_tint["ice"])}
	var sp: Dictionary = layout["regions"]["splat"]
	var splat := _load_splat(sp)
	ground_mat = PaintStack.ground_material(fbm, tiles, splat, {
		"snow_amount": 0.0, "mottle_amp": 0.0, "hatch_amp": 0.0, "wash_amp": 0.0,
		"detile_mix": 0.0, "tile_m": 2.5, "tile_tint": 1.0,
		"splat_origin": Vector2(float(sp["origin_xz"][0]), float(sp["origin_xz"][1])),
		"splat_size": Vector2(float(sp["size_m"][0]), float(sp["size_m"][1])),
		"splat_relax_m": 3.0,
	})
	world_mats.append(ground_mat)
	var pa: Dictionary = _mound_spec()["passage"]
	var hw := float(pa["half_w"])
	var pv0 := float(pa["v0"])
	var pv1 := float(pa["v_end"])
	var us := _breaks(-FLOOR_EXTENT, FLOOR_EXTENT, FLOOR_CELL, [-hw, hw])
	var vs := _breaks(-FLOOR_EXTENT, FLOOR_EXTENT, FLOOR_CELL, [pv0, pv1])
	var V := PackedVector3Array()
	var N := PackedVector3Array()
	for j in vs.size() - 1:
		for i in us.size() - 1:
			var uc := (us[i] + us[i + 1]) * 0.5
			var vc := (vs[j] + vs[j + 1]) * 0.5
			if absf(uc) < hw and vc > pv0 and vc < pv1:
				continue
			var a := _L(us[i], 0.0, vs[j])
			var b := _L(us[i + 1], 0.0, vs[j])
			var c := _L(us[i + 1], 0.0, vs[j + 1])
			var d := _L(us[i], 0.0, vs[j + 1])
			_tri(V, N, a, b, c, Vector3.UP)
			_tri(V, N, a, c, d, Vector3.UP)
	var mi := _mesh(V, N, ground_mat, "Ground", level)
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	# ONE collider box, top face at y = 0. v1 cut the passage out of it so he could walk down
	# the steps; in v2 the passage is scenery behind the facade's collider, so nothing reaches
	# the hole and the floor can stay whole.
	var body := _body(level, "FloorBody")
	var E := FLOOR_EXTENT
	_box(body, -E, E, -E, E, -2.0, 0.0)
	report["ground"]["floor"] = {"y": 0.0, "extent_m": E * 2.0, "triangles": V.size() / 3,
		"collider": "1 box, top face at y = 0",
		"passage_hole_uv_visual_only": {"u": [-hw, hw], "v": [pv0, pv1]}}


func _load_splat(sp: Dictionary) -> ImageTexture:
	"""The weight map off its RAW bytes, never through the importer: an importer that decided
	this was a 3D texture would compress it, and a lossy weight is a different ground class.
	The sha256 is checked against the one make_layout.py recorded, so a stale or foreign PNG
	says so instead of drawing the wrong tarn."""
	report["ground"] = {}
	var path := String(sp.get("file", sp.get("png", "")))
	if not FileAccess.file_exists(path):
		push_error("barrow_full: splat %s missing" % path)
		report["ground"]["splat_error"] = "missing " + path
		return null
	var img := Image.new()
	var err := img.load_png_from_buffer(FileAccess.get_file_as_bytes(path))
	var sha := FileAccess.get_sha256(path)
	report["ground"]["splat"] = path
	report["ground"]["splat_sha256_matches_layout"] = sha == String(sp.get("sha256", ""))
	report["ground"]["splat_px"] = [img.get_width(), img.get_height()]
	if err != OK:
		push_error("barrow_full: splat decode failed (%d)" % err)
		return null
	return ImageTexture.create_from_image(img)


# --- the mound and the door's passage -----------------------------------------------------
var _mound_cache := {}


func _mound_spec() -> Dictionary:
	# CACHED: dome_h calls this five times per mound vertex (the height and its central
	# differences), ~45 k calls over a 56-row list -- measured as most of a 4.8 s build.
	if not _mound_cache.is_empty():
		return _mound_cache
	for e in layout["placements"]:
		if String(e["id"]) == "mound":
			_mound_cache = e
			return e
	return {}


func dome_h(u: float, v: float) -> float:
	"""The mound's height above the floor at (u, v); zero outside its ellipse."""
	var m := _mound_spec()
	var c := Vector2(float(m["uv"][0]), float(m["uv"][1]))
	var a := float(m["semi_axes"][0])
	var b := float(m["semi_axes"][1])
	var du := (u - c.x) / a
	var dv := (v - c.y) / b
	var r2 := du * du + dv * dv
	if r2 >= 1.0:
		return 0.0
	var w := 1.0 - r2
	# SMOOTH (no wobble: through the ramp it read as brushwork), and with a TOE: the kerb's rise
	# spread over the outer toe_rho of the radius so it is not a one-cell cliff (see the layout).
	var t := clampf((1.0 - sqrt(r2)) / float(m.get("toe_rho", 0.0001)), 0.0, 1.0)
	return maxf(float(m["rise_m"]) * pow(w, float(m["exponent"])) * t * t * (3.0 - 2.0 * t), 0.0)


func passage_floor(v: float) -> float:
	"""The passage floor's height at v: the threshold at y = 0, then three 0.2 m steps down."""
	var pa: Dictionary = _mound_spec()["passage"]
	var y := 0.0
	for r in pa["risers_v"]:
		if v >= float(r) - 1e-6:
			y -= float(pa["riser_m"])
	return y


func floor_y_at(_u: float, _v: float) -> float:
	"""Where his feet go: y = 0 everywhere he can reach (R-C9-74). The passage's steps are
	scenery behind the facade (spec v2)."""
	return 0.0


func mound_foot_v(u: float) -> float:
	var m := _mound_spec()
	var a := float(m["semi_axes"][0])
	var b := float(m["semi_axes"][1])
	return float(m["uv"][1]) - b * sqrt(maxf(0.0, 1.0 - pow((u - float(m["uv"][0])) / a, 2.0)))


func _build_mound() -> void:
	"""THE BARROW, v2: a kerbed dome 12 x 9 m about (0, 13), and the door SET INTO IT -- a
	stone-lined cutting from the foot to a facade, the lintel and posts standing a hand proud of
	the facade, the mound's surface over the lintel, a dark passage beyond it stepping down as
	scenery. Nothing here is walkable but the cutting's floor, at y = 0."""
	var m := _mound_spec()
	var c := Vector2(float(m["uv"][0]), float(m["uv"][1]))
	var a := float(m["semi_axes"][0])
	var b := float(m["semi_axes"][1])
	var rise := float(m["rise_m"])
	var cu: Dictionary = m["cutting"]
	var pa: Dictionary = m["passage"]
	var chw := float(cu["half_w"])
	var cwt := float(cu["wall_t"])
	var vf := float(cu["v_facade"])
	var ft := float(cu["facade_t"])
	var phw := float(pa["half_w"])
	var pv1 := float(pa["v_end"])
	var ceil_y := float(pa["ceiling_y"])
	var root := Node3D.new()
	root.name = "mound"
	level.add_child(root)
	nodes["mound"] = root
	# the dome: a 0.1 m grid aligned so the cutting's edges (u +-1.3, v 10.5) are grid lines
	var u0 := snappedf(c.x - a - 0.2, MOUND_CELL)
	var v0 := snappedf(c.y - b - 0.2, MOUND_CELL)
	var nu := int(round((2.0 * a + 0.4) / MOUND_CELL))
	var nv := int(round((2.0 * b + 0.4) / MOUND_CELL))
	var H := PackedFloat32Array()
	var NR := PackedVector3Array()
	var GU := PackedFloat32Array()
	var GV := PackedFloat32Array()
	H.resize((nu + 1) * (nv + 1))
	NR.resize((nu + 1) * (nv + 1))
	GU.resize((nu + 1) * (nv + 1))
	GV.resize((nu + 1) * (nv + 1))
	var e := MOUND_CELL
	var rho := func(u: float, v: float) -> float:
		return sqrt(pow((u - c.x) / a, 2.0) + pow((v - c.y) / b, 2.0))
	for j in nv + 1:
		for i in nu + 1:
			var u := u0 + float(i) * e
			var v := v0 + float(j) * e
			var k := j * (nu + 1) + i
			var r: float = rho.call(u, v)
			var nu_ := u
			var nv_ := v
			# THE FOOT FOLLOWS THE ELLIPSE, NOT THE GRID (a kerbed profile rises inside one cell,
			# so a grid foot is a staircase): a vertex just outside the foot slides onto it.
			if r >= 1.0:
				var near := false
				for dj in [-1, 0, 1]:
					for di in [-1, 0, 1]:
						if float(rho.call(u + float(di) * e, v + float(dj) * e)) < 1.0:
							near = true
				if near:
					u = c.x + (u - c.x) / r
					v = c.y + (v - c.y) / r
					nu_ = c.x + (u - c.x) * 0.995
					nv_ = c.y + (v - c.y) * 0.995
			GU[k] = u
			GV[k] = v
			H[k] = dome_h(u, v)
			var hu := (dome_h(nu_ + e, nv_) - dome_h(nu_ - e, nv_)) / (2.0 * e)
			var hv := (dome_h(nu_, nv_ + e) - dome_h(nu_, nv_ - e)) / (2.0 * e)
			NR[k] = Vector3(-hu, 1.0, hv).normalized()
	var V := PackedVector3Array()
	var N := PackedVector3Array()
	for j in nv:
		for i in nu:
			var uc := u0 + (float(i) + 0.5) * e
			var vc := v0 + (float(j) + 0.5) * e
			if absf(uc) < chw and vc < vf:
				continue                                  # the cutting is open to the sky
			var k00 := j * (nu + 1) + i
			var k10 := k00 + 1
			var k01 := k00 + nu + 1
			var k11 := k01 + 1
			if H[k00] < 0.003 and H[k10] < 0.003 and H[k01] < 0.003 and H[k11] < 0.003:
				continue
			var p00 := _L(GU[k00], H[k00], GV[k00])
			var p10 := _L(GU[k10], H[k10], GV[k10])
			var p01 := _L(GU[k01], H[k01], GV[k01])
			var p11 := _L(GU[k11], H[k11], GV[k11])
			_tri_n(V, N, p00, p10, p11, NR[k00], NR[k10], NR[k11])
			_tri_n(V, N, p00, p11, p01, NR[k00], NR[k11], NR[k01])
	# ITS OWN TINT (ratified on v1): on snow, in the ground's material, it vanished
	var mound_mat := PaintStack.world_material(fbm, _tint.get(String(m.get("tint", "mound")), _tint["snow"]), _flat_params())
	world_mats.append(mound_mat)
	_mesh(V, N, mound_mat, "MoundMesh", root)
	var tris := V.size() / 3

	# THE CUTTING'S LINING AND THE FACADE: stone, primitive grey. Each wall face rises from the
	# floor to the dome's own height at that point, so the lining meets the mound's surface
	# with no gap; the facade is the mound's cut face around the door, open where the door is.
	var stone := PaintStack.world_material(fbm, _tint["primitive_grey"], _flat_params())
	world_mats.append(stone)
	var SV := PackedVector3Array()
	var SN := PackedVector3Array()
	var vstart := snappedf(mound_foot_v(chw) - 0.05, e)
	for s in [-1.0, 1.0]:
		var v := vstart
		while v < vf - 1e-6:
			var va := v
			var vb := minf(v + e, vf)
			var ta := dome_h(s * chw, va)
			var tb := dome_h(s * chw, vb)
			if ta > 0.0 or tb > 0.0:
				_tri(SV, SN, _L(s * chw, 0.0, va), _L(s * chw, 0.0, vb), _L(s * chw, tb, vb), Vector3(-s, 0, 0))
				_tri(SV, SN, _L(s * chw, 0.0, va), _L(s * chw, tb, vb), _L(s * chw, ta, va), Vector3(-s, 0, 0))
			v += e
	var nuq := int(round(2.0 * chw / e))
	for q in nuq:
		var ua := -chw + float(q) * e
		var ub := ua + e
		var um := (ua + ub) * 0.5
		var ybot := ceil_y if absf(um) < phw else 0.0     # the door's opening is left open
		var ha := dome_h(ua, vf)
		var hb := dome_h(ub, vf)
		_tri(SV, SN, _L(ua, ybot, vf), _L(ub, ybot, vf), _L(ub, hb, vf), Vector3(0, 0, 1))
		_tri(SV, SN, _L(ua, ybot, vf), _L(ub, hb, vf), _L(ua, ha, vf), Vector3(0, 0, 1))
	_mesh(SV, SN, stone, "CuttingAndFacade", root)

	# THE PASSAGE BEYOND THE DOOR: scenery for a later interior -- dark, three 0.2 m steps down
	var dark := PaintStack.world_material(fbm, _tint["passage_dark"], _flat_params())
	world_mats.append(dark)
	var PV := PackedVector3Array()
	var PN := PackedVector3Array()
	var edges: Array = [vf]
	for r in pa["risers_v"]:
		edges.append(float(r))
	edges.append(pv1)
	for q in edges.size() - 1:
		var va := float(edges[q])
		var vb := float(edges[q + 1])
		var y := passage_floor(va + 0.01)
		_tri(PV, PN, _L(-phw, y, va), _L(phw, y, va), _L(phw, y, vb), Vector3.UP)
		_tri(PV, PN, _L(-phw, y, va), _L(phw, y, vb), _L(-phw, y, vb), Vector3.UP)
		if q > 0:
			var yup := passage_floor(va - 0.01)
			_tri(PV, PN, _L(-phw, y, va), _L(phw, y, va), _L(phw, yup, va), Vector3(0, 0, 1))
			_tri(PV, PN, _L(-phw, y, va), _L(phw, yup, va), _L(-phw, yup, va), Vector3(0, 0, 1))
		for s in [-1.0, 1.0]:
			_tri(PV, PN, _L(s * phw, y, va), _L(s * phw, y, vb), _L(s * phw, ceil_y, vb), Vector3(-s, 0, 0))
			_tri(PV, PN, _L(s * phw, y, va), _L(s * phw, ceil_y, vb), _L(s * phw, ceil_y, va), Vector3(-s, 0, 0))
	var yend := passage_floor(pv1 - 0.01)
	_tri(PV, PN, _L(-phw, yend, pv1), _L(phw, yend, pv1), _L(phw, ceil_y, pv1), Vector3(0, 0, 1))
	_tri(PV, PN, _L(-phw, yend, pv1), _L(phw, ceil_y, pv1), _L(-phw, ceil_y, pv1), Vector3(0, 0, 1))
	_mesh(PV, PN, dark, "Passage", root)

	# COLLIDERS: the rim ring (the cutting's mouth left open), the cutting's walls, the facade.
	# Non-walkable by collider, not by slope (barrow_world's rule, ratified).
	var body := _body(root, "MoundWall")
	var nseg := 48
	var kept := 0
	for s in nseg:
		var t0 := TAU * float(s) / float(nseg)
		var t1 := TAU * float(s + 1) / float(nseg)
		var p0 := Vector2(c.x + a * 0.97 * cos(t0), c.y + b * 0.97 * sin(t0))
		var p1 := Vector2(c.x + a * 0.97 * cos(t1), c.y + b * 0.97 * sin(t1))
		var mid := (p0 + p1) * 0.5
		if absf(mid.x) < chw + cwt and mid.y < c.y:
			continue
		_box_rot(body, mid, p0.distance_to(p1) + 0.3, 0.3, 0.0, rise, atan2(p1.y - p0.y, p1.x - p0.x))
		kept += 1
	var vw := mound_foot_v(chw + cwt) - 0.3
	_box(body, chw, chw + cwt, vw, vf + ft, 0.0, rise)
	_box(body, -chw - cwt, -chw, vw, vf + ft, 0.0, rise)
	_box(body, -chw - cwt, chw + cwt, vf, vf + ft, 0.0, rise)
	var cover := INF
	var uu := -1.14
	while uu <= 1.14 + 1e-6:
		var vv := vf
		while vv <= pv1 + 1e-6:
			cover = minf(cover, dome_h(uu, vv))
			vv += 0.1
		uu += 0.1
	report["mound"] = {"centre_uv": [c.x, c.y], "semi_axes_m": [a, b], "rise_m": rise,
		"exponent": float(m["exponent"]), "triangles": tris,
		"rim_wall_boxes": kept, "rim_wall_boxes_left_open_for_the_cutting": nseg - kept,
		"cutting": {"half_w": chw, "v": [snappedf(mound_foot_v(chw), 0.001), vf], "floor_y": 0.0,
					"facade_v": vf},
		"passage": {"half_w": phw, "v": [vf, pv1], "bottom_y": passage_floor(pv1 - 0.01), "walkable": false},
		"dome_min_over_passage_roof_m": snappedf(cover, 0.001),
		"back_foot_v": c.y + b, "peak_y": dome_h(c.x, c.y)}


# --- the placements -----------------------------------------------------------------------
func _build_placements() -> void:
	var later := []
	var t0 := Time.get_ticks_msec()
	for e in layout["placements"]:
		var kind := String(e["kind"])
		if kind == "structure":
			continue
		if kind == "primitive":
			_place_primitive(e)
		elif e.has("perch_on") or e.has("stack_on"):
			later.append(e)
		else:
			_place_model(e)
	for e in later:
		_place_model(e)
	report["placements_ms"] = Time.get_ticks_msec() - t0


func _meshes(root: Node) -> Array:
	var out := []
	for n in root.find_children("*", "MeshInstance3D", true, false):
		var mi := n as MeshInstance3D
		if mi.mesh == null or String(mi.name).ends_with("_ink"):
			continue
		out.append(mi)
	return out


func _node_aabb(root: Node3D) -> AABB:
	"""Bounds in ROOT's own space, ink excluded (barrow_world's _node_aabb)."""
	var out := AABB()
	var first := true
	var inv := root.global_transform.affine_inverse()
	for mi in _meshes(root):
		var b: AABB = (inv * (mi as MeshInstance3D).global_transform) * (mi as MeshInstance3D).mesh.get_aabb()
		if first:
			out = b
			first = false
		else:
			out = out.merge(b)
	return out


func world_verts(root: Node3D) -> PackedVector3Array:
	var out := PackedVector3Array()
	for mi in _meshes(root):
		var m := mi as MeshInstance3D
		var t := m.global_transform
		for s in m.mesh.get_surface_count():
			var arrs := m.mesh.surface_get_arrays(s)
			var vv: PackedVector3Array = arrs[Mesh.ARRAY_VERTEX]
			for p in vv:
				out.append(t * p)
	return out


func _place_model(e: Dictionary) -> void:
	var id := String(e["id"])
	var glb := String(e["glb"])
	var ps := load(glb) as PackedScene
	if ps == null:
		push_error("barrow_full: cannot load %s for %s" % [glb, id])
		built[id] = {"error": "cannot load " + glb}
		return
	var root := Node3D.new()
	root.name = id
	props_root.add_child(root)
	var fit := Node3D.new()
	fit.name = "fit"
	root.add_child(fit)
	fit.add_child(ps.instantiate())
	# SIZE FROM THE LOADED AABB (the brief), pitch stretch BEFORE the normalise (T10_HANDOFF)
	var raw := _node_aabb(root)
	var pitch := 1.0 / cos(deg_to_rad(PL_PITCH_DEG))
	var sy := pitch if bool(e.get("pitch_correct", false)) else 1.0
	var target := float(e["target_m"])
	var k := 0.0
	if String(e.get("axis", "height")) == "across":
		k = target / maxf(maxf(raw.size.x, raw.size.z), 1e-6)
	else:
		k = target / maxf(raw.size.y * sy, 1e-6)
	fit.scale = Vector3(k, k * sy, k)
	var forced = e.get("width_m", null)
	if forced != null and float(forced) > 0.0:
		var cur := maxf(maxf(raw.size.x, raw.size.z) * k, 1e-6)
		var wk := float(forced) / cur
		fit.scale = Vector3(fit.scale.x * wk, fit.scale.y, fit.scale.z * wk)
	var b := _node_aabb(root)
	fit.position = Vector3(-(b.position.x + b.size.x * 0.5), -b.position.y, -(b.position.z + b.size.z * 0.5))
	if String(e["class"]) == "birch":
		# A TREE STANDS WHERE ITS TRUNK IS, not where its crown's box is centred. The trunk base
		# is the centroid of the vertices in the bottom 0.25 m; it goes on the placement point.
		var lowc := Vector3.ZERO
		var nlow := 0
		var inv := root.global_transform.affine_inverse()
		for mi in _meshes(root):
			var t: Transform3D = inv * (mi as MeshInstance3D).global_transform
			for s in (mi as MeshInstance3D).mesh.get_surface_count():
				var vv: PackedVector3Array = (mi as MeshInstance3D).mesh.surface_get_arrays(s)[Mesh.ARRAY_VERTEX]
				for p in vv:
					var q := t * p
					if q.y < 0.25:
						lowc += q
						nlow += 1
		if nlow > 0:
			lowc /= float(nlow)
			fit.position -= Vector3(lowc.x, 0.0, lowc.z)
	var fin := _node_aabb(root)
	var yaw := float(e.get("yaw_world_deg", 0.0))
	var basis := Basis(Vector3.UP, deg_to_rad(yaw))
	var tip = e.get("tip", null)
	if tip != null:
		# FALLEN, LYING OUTWARD: the yaw has already turned the carved face to the ring's centre;
		# turning +90 about (up x d) lays +Y onto the outward radial d and that face ends up.
		var o: Array = tip["outward_uv"]
		var d := (u_hat * float(o[0]) + v_hat * float(o[1])).normalized()
		basis = Basis(Vector3(d.z, 0.0, -d.x), PI * 0.5) * basis
	var at := Vector3.ZERO
	var perch := ""
	if e.has("perch_on"):
		perch = String(e["perch_on"])
		var stone := nodes.get(perch, null) as Node3D
		var top := _top_point(stone) if stone != null else Vector3.ZERO
		at = top - Vector3(0.0, 0.04, 0.0)
	elif e.has("stack_on"):
		var lo := INF
		for pid in e["stack_on"]:
			var pn := nodes.get(String(pid), null) as Node3D
			if pn != null:
				lo = minf(lo, _top_point(pn).y)
		var uv: Array = e["uv"]
		at = uv_to_world(float(uv[0]), float(uv[1]), (lo if lo < INF else 2.0) - 0.03)
	else:
		var uv: Array = e["uv"]
		at = uv_to_world(float(uv[0]), float(uv[1]), -PROP_SINK_M)
	root.global_transform = Transform3D(basis, at)
	if tip != null:
		var vv := world_verts(root)
		var lo := INF
		for p in vv:
			lo = minf(lo, p.y)
		var gp := root.global_position
		gp.y -= lo + float(tip.get("sink_m", 0.05))
		root.global_position = gp
	var ncol := _add_collider(root, e)
	var saved := PaintStack.adopt_prop(root, fbm, PaintStack.INK, float(e.get("hull_px", HULL_PX)) / PPM,
									   _flat_params(float(e.get("mesh_mark", 1.0))))
	var tris := 0
	for s in saved.get("meshes", []):
		var mat: ShaderMaterial = s["ramp"]
		# FLAT GREY: the painted albedo is switched off, so the painter paints the true
		# silhouette and not the Tripo texture's own idea of the stone
		mat.set_shader_parameter("use_tex", false)
		mat.set_shader_parameter("base_color", _tint["hero_grey"])
		world_mats.append(mat)
		var mi := (s["mi"]) as MeshInstance3D
		if mi.mesh is ArrayMesh:
			for q in mi.mesh.get_surface_count():
				tris += (mi.mesh as ArrayMesh).surface_get_array_index_len(q) / 3
	for s in saved.get("inks", []):
		_prop_inks.append(s["mi"])
	nodes[id] = root
	built[id] = {"loaded_aabb_m": _v3(raw.size), "k": snappedf(k, 1e-6),
				 "fit_scale": _v3(fit.scale), "fit_offset": _v3(fit.position),
				 "size_m_local": _v3(fin.size), "target_m": target,
				 "sized_by": String(e.get("axis", "height")),
				 "pitch_stretch": snappedf(sy, 1e-6), "yaw_world_deg": yaw,
				 "tipped": tip != null, "perched_on": perch, "colliders": ncol, "tris": tris,
				 "hull_pen_px": float(e.get("hull_px", HULL_PX))}


func _top_point(root: Node3D) -> Vector3:
	var best := Vector3(0.0, -INF, 0.0)
	for p in world_verts(root):
		if p.y > best.y:
			best = p
	return best


func _add_collider(root: Node3D, e: Dictionary) -> int:
	var kind := String(e.get("collider", "hull"))
	if kind == "none":
		return 0
	var body := _body(root, "obstacle")
	if kind == "trunk":
		var cs := CollisionShape3D.new()
		var cy := CylinderShape3D.new()
		cy.radius = float(e.get("trunk_r", 0.22))
		cy.height = 2.4
		cs.shape = cy
		cs.position = Vector3(0.0, 1.2, 0.0)
		body.add_child(cs)
		return 1
	# THE MODEL'S OWN CONVEX HULL, with the fit's non-uniform scale BAKED INTO THE POINTS: the
	# physics server does not support a non-uniformly scaled shape, and the pitch stretch makes
	# every Barrow model one.
	var n := 0
	var inv := root.global_transform.affine_inverse()
	for mi in _meshes(root):
		var sh := (mi as MeshInstance3D).mesh.create_convex_shape(true, false)
		if sh == null:
			continue
		var rel: Transform3D = inv * (mi as MeshInstance3D).global_transform
		var pts := PackedVector3Array()
		for p in (sh as ConvexPolygonShape3D).points:
			pts.append(rel * p)
		var cvx := ConvexPolygonShape3D.new()
		cvx.points = pts
		var cs := CollisionShape3D.new()
		cs.shape = cvx
		body.add_child(cs)
		n += 1
	return n


func _place_primitive(e: Dictionary) -> void:
	"""Layered rock masses: stacked slabs, each an irregular convex polygon extruded with a
	tapered top. Flat-shaded, primitive grey, and solid: one convex collider per slab."""
	var id := String(e["id"])
	var root := Node3D.new()
	root.name = id
	level.add_child(root)
	var mat := PaintStack.world_material(fbm, _tint["primitive_grey"], _flat_params())
	world_mats.append(mat)
	var body := _body(root, "obstacle")
	var V := PackedVector3Array()
	var N := PackedVector3Array()
	for layer in e["layers"]:
		var poly: Array = layer["poly_uv"]
		var y0 := float(layer["y0"])
		var y1 := float(layer["y1"])
		var ts := float(layer["top_scale"])
		var cen := Vector2.ZERO
		for p in poly:
			cen += Vector2(float(p[0]), float(p[1]))
		cen /= float(poly.size())
		var B := PackedVector3Array()
		var T := PackedVector3Array()
		for p in poly:
			var q := Vector2(float(p[0]), float(p[1]))
			B.append(_L(q.x, y0, q.y))
			var qt := cen + (q - cen) * ts
			T.append(_L(qt.x, y1, qt.y))
		var n := B.size()
		var c3 := _L(cen.x, (y0 + y1) * 0.5, cen.y)
		for i in range(1, n - 1):
			_tri(V, N, T[0], T[i], T[i + 1], Vector3.UP)
			_tri(V, N, B[0], B[i], B[i + 1], Vector3.DOWN)
		for i in n:
			var a := B[i]
			var b := B[(i + 1) % n]
			var c := T[(i + 1) % n]
			var d := T[i]
			var nr := (b - a).cross(d - a).normalized()
			if nr.dot((a + b) * 0.5 - c3) < 0.0:
				nr = -nr
			_tri(V, N, a, b, c, nr)
			_tri(V, N, a, c, d, nr)
		var cvx := ConvexPolygonShape3D.new()
		var pts := PackedVector3Array(B)
		pts.append_array(T)
		cvx.points = pts
		var cs := CollisionShape3D.new()
		cs.shape = cvx
		body.add_child(cs)
	_mesh(V, N, mat, "mass", root)
	nodes[id] = root
	# the BUILT base centroid -- the polygon's AREA centroid, as the layout centres it (a vertex
	# average of an irregular polygon sits up to 0.05 m off it) -- read back through the Level's
	# transform into world: the placement check measures this, not the number it was built from
	var base: Array = e["layers"][0]["poly_uv"]
	var ar := 0.0
	var cx := 0.0
	var cz := 0.0
	for i in base.size():
		var p0 := Vector2(float(base[i][0]), float(base[i][1]))
		var p1 := Vector2(float(base[(i + 1) % base.size()][0]), float(base[(i + 1) % base.size()][1]))
		var cr := p0.x * p1.y - p1.x * p0.y
		ar += cr
		cx += (p0.x + p1.x) * cr
		cz += (p0.y + p1.y) * cr
	ar *= 0.5
	var bc := level.global_transform * _L(cx / (6.0 * ar), 0.0, cz / (6.0 * ar))
	built[id] = {"layers": (e["layers"] as Array).size(), "tris": V.size() / 3,
				 "height_m": float(e.get("height_m", 0.0)), "base_centroid_world": _v3(bc)}


# --- the bounds ---------------------------------------------------------------------------
func _build_bounds() -> void:
	"""Invisible walls on every edge of the bounds polygon. The EDGE reads as land because an
	outcrop straddles every vertex, G2/G4 and the mound close the top, and the scrub band the
	layout adds lies along every other stretch -- the wall is where the land already stops."""
	var bd: Dictionary = layout["bounds"]
	var poly: Array = bd["polygon_uv"]
	var body := _body(level, "Bounds")
	var total := 0.0
	for i in poly.size():
		var p := Vector2(float(poly[i][0]), float(poly[i][1]))
		var q := Vector2(float(poly[(i + 1) % poly.size()][0]), float(poly[(i + 1) % poly.size()][1]))
		var d := q - p
		_box_rot(body, (p + q) * 0.5, d.length() + 0.3, 0.3, 0.0, 3.0, atan2(d.y, d.x))
		total += d.length()
	report["bounds"] = {"edges": poly.size(), "perimeter_m": snappedf(total, 0.01),
		"entry_edge": "closed by an exit wall at the frame's bottom edge (the eventual level transition)"}


# --- the layout overlay (O) ---------------------------------------------------------------
func _ribbon(pts: Array, closed: bool, col: Color, w: float, parent: Node3D) -> void:
	var V := PackedVector3Array()
	var N := PackedVector3Array()
	var n := pts.size()
	for i in (n if closed else n - 1):
		var p: Vector2 = pts[i]
		var q: Vector2 = pts[(i + 1) % n]
		var d := (q - p).normalized()
		var o := Vector2(-d.y, d.x) * (w * 0.5)
		var y := 0.012
		_tri(V, N, _L(p.x - o.x, y, p.y - o.y), _L(q.x - o.x, y, q.y - o.y), _L(q.x + o.x, y, q.y + o.y), Vector3.UP)
		_tri(V, N, _L(p.x - o.x, y, p.y - o.y), _L(q.x + o.x, y, q.y + o.y), _L(p.x + o.x, y, p.y + o.y), Vector3.UP)
	var m := StandardMaterial3D.new()
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.albedo_color = col
	_mesh(V, N, m, "ribbon", parent, false)


func _ellipse_pts(c: Vector2, a: float, b: float, n := 96) -> Array:
	var out := []
	for i in n:
		var t := TAU * float(i) / float(n)
		out.append(Vector2(c.x + a * cos(t), c.y + b * sin(t)))
	return out


func _build_overlay() -> void:
	_overlay = Node3D.new()
	_overlay.name = "LayoutOverlay"
	level.add_child(_overlay)
	var R: Dictionary = layout["regions"]
	var bp := []
	for p in layout["bounds"]["polygon_uv"]:
		bp.append(Vector2(float(p[0]), float(p[1])))
	_ribbon(bp, true, Color(0.85, 0.12, 0.10), 0.10, _overlay)
	var ac: Array = R["arena"]["centre_uv"]
	_ribbon(_ellipse_pts(Vector2(float(ac[0]), float(ac[1])), float(R["arena"]["r"]), float(R["arena"]["r"])),
			true, Color(0.15, 0.30, 0.90), 0.08, _overlay)
	var rc: Array = R["ring"]["centre_uv"]
	_ribbon(_ellipse_pts(Vector2(float(rc[0]), float(rc[1])), float(R["ring"]["r"]), float(R["ring"]["r"])),
			true, Color(0.40, 0.40, 0.45), 0.05, _overlay)
	var ic: Array = R["ice"]["centre_uv"]
	_ribbon(_ellipse_pts(Vector2(float(ic[0]), float(ic[1])), float(R["ice"]["axes_m"][0]) * 0.5,
						 float(R["ice"]["axes_m"][1]) * 0.5), true, Color(0.10, 0.55, 0.75), 0.06, _overlay)
	var m := _mound_spec()
	_ribbon(_ellipse_pts(Vector2(float(m["uv"][0]), float(m["uv"][1])), float(m["semi_axes"][0]),
						 float(m["semi_axes"][1])), true, Color(0.50, 0.30, 0.12), 0.06, _overlay)
	# the path band's two edges
	var pp: Array = R["path"]["extended_off_frame_uv"]
	var hwp := float(R["path"]["width_m"]) * 0.5
	for side in [-1.0, 1.0]:
		var edge := []
		for i in pp.size():
			var p := Vector2(float(pp[i][0]), float(pp[i][1]))
			var dprev := Vector2.ZERO
			var dnext := Vector2.ZERO
			if i > 0:
				dprev = (p - Vector2(float(pp[i - 1][0]), float(pp[i - 1][1]))).normalized()
			if i < pp.size() - 1:
				dnext = (Vector2(float(pp[i + 1][0]), float(pp[i + 1][1])) - p).normalized()
			var d := (dprev + dnext).normalized()
			edge.append(p + Vector2(-d.y, d.x) * hwp * side)
		_ribbon(edge, false, Color(0.45, 0.30, 0.15), 0.06, _overlay)
	_overlay.visible = overlay_on


func set_overlay(on: bool) -> void:
	overlay_on = on
	if _overlay != null:
		_overlay.visible = on
	_update_hud()


# --- THE CRUCIBLE (Matt): spawn circles, the boss gate, the player station -----------------
func _decal(pts: Array, closed: bool, col: Color, w: float, parent: Node3D, y := 0.012) -> void:
	"""A flat, opaque, unshaded ribbon on the floor. OPAQUE on purpose: the one-pen pass reads
	the screen as it stood after the opaque pass, so anything drawn transparent would be painted
	over by it."""
	var V := PackedVector3Array()
	var N := PackedVector3Array()
	var n := pts.size()
	for i in (n if closed else n - 1):
		var p: Vector2 = pts[i]
		var q: Vector2 = pts[(i + 1) % n]
		var d := (q - p).normalized()
		var o := Vector2(-d.y, d.x) * (w * 0.5)
		_tri(V, N, _L(p.x - o.x, y, p.y - o.y), _L(q.x - o.x, y, q.y - o.y), _L(q.x + o.x, y, q.y + o.y), Vector3.UP)
		_tri(V, N, _L(p.x - o.x, y, p.y - o.y), _L(q.x + o.x, y, q.y + o.y), _L(p.x + o.x, y, p.y + o.y), Vector3.UP)
	var m := StandardMaterial3D.new()
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.albedo_color = col
	_mesh(V, N, m, "decal", parent, false)


func _flat_label(txt: String, at: Vector2, col: Color, px_size: float, parent: Node3D) -> Label3D:
	"""Text painted flat on the ground, reading upright at the play camera: its x along +u, its
	up along +v, its face up. ALPHA-CUT, so it draws in the opaque pass (see _decal)."""
	var l := Label3D.new()
	l.text = txt
	l.font_size = 96
	l.pixel_size = px_size
	l.outline_size = 22
	l.modulate = col
	l.outline_modulate = Color(PaintStack.INK.r, PaintStack.INK.g, PaintStack.INK.b, 1.0)
	l.alpha_cut = Label3D.ALPHA_CUT_DISCARD
	l.shaded = false
	l.double_sided = false
	l.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	l.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	l.transform = Transform3D(Basis(Vector3(1, 0, 0), Vector3(0, 0, -1), Vector3(0, 1, 0)), _L(at.x, 0.02, at.y))
	parent.add_child(l)
	return l


func _build_crucible() -> void:
	var cr: Dictionary = layout.get("crucible", {})
	_crucible = Node3D.new()
	_crucible.name = "Crucible"
	level.add_child(_crucible)
	if cr.is_empty():
		return
	var rune: Color = _tint["rune"]
	var st: Array = cr["station"]["uv"]
	var station := Vector2(float(st[0]), float(st[1]))
	for s in cr["spawns"]:
		var c := Vector2(float(s["uv"][0]), float(s["uv"][1]))
		var r := float(s["r_m"])
		# the rune ring: a 0.12 m band at r 1.5, twelve rune marks inside it
		_decal(_ellipse_pts(c, r - 0.06, r - 0.06, 72), true, rune, 0.12, _crucible)
		for k in 12:
			var a := TAU * float(k) / 12.0
			var d := Vector2(cos(a), sin(a))
			var tdir := Vector2(-d.y, d.x)
			var p0 := c + d * (r - 0.30)
			if k % 3 == 0:
				_decal([p0 - tdir * 0.10, p0 + d * 0.16, p0 + tdir * 0.10, p0 - d * 0.02], true, rune, 0.05, _crucible)
			else:
				_decal([p0 - d * 0.06, p0 + d * 0.12], false, rune, 0.05, _crucible)
		var to_station := (station - c).normalized()
		_flat_label(String(s["id"]), c + to_station * (r + 0.55), rune, 0.0075, _crucible)
	var bg: Dictionary = cr["boss_gate"]
	var gv := float(bg["uv"][1])
	var ghw := float(bg["width_m"]) * 0.5
	var boss: Color = _tint["boss"]
	_decal([Vector2(-ghw, gv), Vector2(ghw, gv)], false, boss, 0.22, _crucible)
	for k in 2:
		var off := 0.55 + 0.45 * float(k)
		_decal([Vector2(-0.75, gv - off + 0.30), Vector2(0.0, gv - off - 0.10), Vector2(0.75, gv - off + 0.30)], false, boss, 0.14, _crucible)
	_flat_label("BOSS GATE", Vector2(0.0, gv - 1.75), boss, 0.0060, _crucible)
	var stc: Color = _tint["station"]
	_decal(_ellipse_pts(station, 0.75, 0.75, 48), true, stc, 0.08, _crucible)
	_decal([station + Vector2(-0.55, 0.0), station + Vector2(0.55, 0.0)], false, stc, 0.06, _crucible)
	_decal([station + Vector2(0.0, -0.55), station + Vector2(0.0, 0.55)], false, stc, 0.06, _crucible)
	_flat_label("STATION", station + Vector2(0.0, -1.35), stc, 0.0055, _crucible)
	_crucible.visible = crucible_on


func set_crucible_visible(on: bool) -> void:
	crucible_on = on
	if _crucible != null:
		_crucible.visible = on
	_update_hud()


# --- calibration markers (the capture tool's instrument, never in a delivered frame) -------
func set_markers(on: bool) -> Dictionary:
	if _markers != null:
		_markers.queue_free()
		_markers = null
	if not on:
		return {}
	_markers = Node3D.new()
	_markers.name = "Markers"
	level.add_child(_markers)
	var spec := {
		# ALL FOUR ON OPEN, UNSHADOWED ARENA SNOW. The first set put v_1m 0.9 m from the -125
		# stone, inside its shadow: the background beyond one end was shadow and beyond the other
		# was not, and the bar read 0.36 px long -- the instrument failed its own 2x proof.
		"u_1m": {"from": Vector2(-3.5, -2.5), "to": Vector2(-2.5, -2.5), "rgb": Color(1.0, 0.0, 1.0)},
		"u_2m": {"from": Vector2(1.5, -2.5), "to": Vector2(3.5, -2.5), "rgb": Color(0.0, 1.0, 1.0)},
		"v_1m": {"from": Vector2(-4.0, 2.5), "to": Vector2(-4.0, 3.5), "rgb": Color(1.0, 1.0, 0.0)},
		"v_2m": {"from": Vector2(3.5, 2.0), "to": Vector2(3.5, 4.0), "rgb": Color(0.0, 1.0, 0.0)},
	}
	for k in spec:
		var a: Vector2 = spec[k]["from"]
		var b: Vector2 = spec[k]["to"]
		var d := (b - a).normalized()
		var o := Vector2(-d.y, d.x) * 0.06
		var V := PackedVector3Array()
		var N := PackedVector3Array()
		var y := 0.004
		_tri(V, N, _L(a.x - o.x, y, a.y - o.y), _L(b.x - o.x, y, b.y - o.y), _L(b.x + o.x, y, b.y + o.y), Vector3.UP)
		_tri(V, N, _L(a.x - o.x, y, a.y - o.y), _L(b.x + o.x, y, b.y + o.y), _L(a.x + o.x, y, a.y + o.y), Vector3.UP)
		var m := StandardMaterial3D.new()
		m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		m.albedo_color = spec[k]["rgb"]
		_mesh(V, N, m, k, _markers, false)
	var out := {}
	for k in spec:
		out[k] = {"from_uv": [spec[k]["from"].x, spec[k]["from"].y], "to_uv": [spec[k]["to"].x, spec[k]["to"].y],
				  "length_m": (spec[k]["to"] - spec[k]["from"]).length(),
				  "rgb": [spec[k]["rgb"].r, spec[k]["rgb"].g, spec[k]["rgb"].b], "width_m": 0.12}
	return out


# --- him ----------------------------------------------------------------------------------
func _character_choice() -> String:
	"""?c=sorceress on the web page's URL, `-- --c sorceress` on the desktop; the barbarian otherwise.
	Only the painted Barrow chooses."""
	if not painted:
		return "barbarian"
	var c := PaintStack.web_query("c")
	var args := OS.get_cmdline_user_args()
	var i := args.find("--c")
	if c == "" and i >= 0 and i + 1 < args.size():
		c = String(args[i + 1])
	c = c.to_lower()
	return c if c in ["sorceress", "warlord"] else "barbarian"      # R-C9-117: the dark knight (?c=warlord) too


var slot := ""                     # R-C9-117: the select page's variant (scripts/slots.gd); "" = the page's own character
var slot_report := {}


func _build_knight() -> void:
	who = _character_choice()
	# R-C9-117: A VARIANT SLOT (the select page's armor / hold, or the dark knight): its own character file, read by
	# its own knight script through the one method that opens it; its models fetched as their own pack on the page
	slot = Slots.choose(who)
	if slot != "":
		slot_report = await Slots.fetch_pack(self, slot)
		if not FileAccess.file_exists(String(Slots.SLOTS[slot]["path"])):
			push_error("slot %s: its character file is missing (%s)" % [slot, str(slot_report)])
			slot_report["error"] = "missing"
			slot = "" if who != "warlord" else slot
	# HER, THROUGH knight.gd UNCHANGED: sorceress_knight.gd overrides only the method that opens the
	# character file (so_d7/scene_pkg's slot, in character.json's own shape)
	var ks: Script = load(String(Slots.SLOTS[slot]["script"])) if slot != "" else (load("res://scripts/sorceress_knight.gd") if who == "sorceress" else preload("res://scripts/knight.gd"))
	var k: CharacterBody3D = ks.new()
	if slot != "":
		k.slot_path = String(Slots.SLOTS[slot]["path"])
	k.name = "Knight"
	k.setup(right, up, fwd, 1.0)
	add_child(k)
	knight = k
	await get_tree().physics_frame
	k.set_figure_scale(1.0)
	# ARMED: the full kit, axe and shield (the brief: "him, armed") -- and hers, the staff included
	if who in ["sorceress", "warlord"] or slot.begins_with("barb_glad"):
		k.set_gear_stack(k.gear_stack_count() - 1)
	else:
		k.set_gear_stack(int(layout["knight"].get("gear_stack", 4)))
	var steps: Array = k.cfg.get("scale_steps", [])
	for i in steps.size():
		if absf(float(steps[i]) - 1.0) < 1e-6:
			_size_step = i
	var sp: Array = layout["knight"]["spawn_uv"]
	place_knight(float(sp[0]), float(sp[1]), String(layout["knight"].get("spawn_facing", "N")))
	# HIS PAINT UNDER THE SAME RAMP, from outside knight.gd (barrow_world's call, unchanged)
	_char_saved = PaintStack.adopt_character(k, fbm, PaintStack.INK, {
		"wash_scale": 2.6, "wash_amp": 0.13, "band_soft": 0.075,
	})
	if who == "sorceress":
		# HER TWO SPELLS (spell_fx.gd), fired at each cast's release time, from its socket: the FIRE BALL is
		# cliffside's kit, baked (fire_ball_fx.gd); the METEOR is still the placeholder
		spell_fx = load("res://scripts/spell_fx.gd").new()
		spell_fx.name = "SpellFx"
		add_child(spell_fx)
		spell_fx.setup(k, k.cfg, _read_json(String(Slots.SLOTS[slot].get("sockets", "res://data/sockets_sorceress.json")) if slot != "" else "res://data/sockets_sorceress.json"))
		# THE FIRE BALL'S BUDGET RUN (?perf=fb on the page, -- --perf fb on desktop): perf_fireball.gd
		var perf := PaintStack.web_query("perf")
		var pa := OS.get_cmdline_user_args()
		if perf == "" and pa.find("--perf") >= 0 and pa.find("--perf") + 1 < pa.size():
			perf = String(pa[pa.find("--perf") + 1])
		if perf in ["fb", "fbc", "ma", "mac"]:
			var pn = load("res://scripts/perf_fireball.gd").new()
			pn.name = "PerfFireBall"
			add_child(pn)
			pn.start(self, 20, perf == "fb" or perf == "ma", "chop" if perf.begins_with("ma") else "slash")
	report["character"] = {"who": who, "model": String(k.cfg.get("model", "?")), "figure_scale": 1.0,
		"height_m": k.cfg.get("model_height_m", 1.85), "gear_stack": k.gear_stack,
		"meshes_under_ramp": (_char_saved.get("meshes", []) as Array).size(),
		"spawn_uv": sp}
	look_at_world(_camera_aim())


func place_knight(u: float, v: float, facing := "N") -> void:
	if knight == null:
		return
	knight.global_position = uv_to_world(u, v, floor_y_at(u, v) + 0.03)
	knight.velocity = Vector3.ZERO
	knight.facing = facing
	knight._drive()


func aim_for(pos: Vector3) -> Vector3:
	return pos + up * (CAM_LIFT_PX / PPM)


func _clamp_aim(aim: Vector3) -> Vector3:
	"""THE CAMERA STOPS AT THE PAINTED WINDOW (U; off by default in v2). The frame's centre is
	held inside the window shrunk by half a frame on each side -- exactly the set of frames the
	painting can fill. In v2 the camera margin already holds from every reachable cell, so this
	never engages in play; it is kept for comparison and for any screen the lock does not cover.

	THE WINDOW'S OWN EDGES, NOT A SYMMETRIC BOX. v1's window was centred on the origin and this
	clamped to +-(edge - half frame). v2's window is centred at (-2, -3), and the symmetric
	clamp held the camera 4.0 m short of the left edge and 6.0 m short of the bottom one."""
	var t := aim.y / maxf(-fwd.y, 1e-6)
	var g := aim + fwd * t                               # the aim's ground point along the view
	var uv := world_to_uv(g)
	var gw: Dictionary = layout["frame"]["guide_window"]
	var fu := float(_view_width()) * 0.5 / PPM
	var fv := float(_view_height()) * 0.5 / (PPM * sin(deg_to_rad(PL_PITCH_DEG)))
	var ulo := float(gw["u"][0]) + fu
	var uhi := float(gw["u"][1]) - fu
	var vlo := float(gw["v"][0]) + fv
	var vhi := float(gw["v"][1]) - fv
	var cu := clampf(uv.x, ulo, uhi) if ulo <= uhi else (ulo + uhi) * 0.5
	var cv := clampf(uv.y, vlo, vhi) if vlo <= vhi else (vlo + vhi) * 0.5
	return uv_to_world(cu, cv)


func _camera_aim() -> Vector3:
	var a := aim_for(knight.global_position) if knight != null else Vector3.ZERO
	return _clamp_aim(a) if clamp_on else a


# --- the one pen --------------------------------------------------------------------------
func _build_post() -> void:
	# THE WEB PEN'S THRESHOLD, 3 -> 6 px of depth break (the installed Barrow's, measured there: the
	# depth-only pen has no snow mark, and the snow's cut edges drew as outlines at 3)
	post_mat = PaintStack.post_material(paper, PaintStack.INK, {
		"line_px": LINE_PX, "depth_edge_px": 6.0 if PaintStack.is_compatibility() else 3.0, "normal_edge": 1.05, "normal_weight": 0.30,
		"ink_gain": 1.15, "ref_m_per_px": PLAY_M_PER_PX,
		"grade_on": 0.0,
	})
	_sync_post_scale()
	post_q = PaintStack.post_quad(cam, post_mat)
	report["ink"] = {"one_pen_hex": "#%02X%02X%02X" % [int(round(PaintStack.INK.r * 255.0)),
					 int(round(PaintStack.INK.g * 255.0)), int(round(PaintStack.INK.b * 255.0))],
		"screen_space": {"line_px": LINE_PX, "depth_edge_px": 3.0, "normal_edge": 1.05, "normal_weight": 0.30,
						 "line_px_is": "frame px (1920 x 1080); the span in render px is LINE_PX x render rows / 1080",
						 "source": "paint_stack.gd at HEAD, unmodified"},
		"hull": "1.1 px on him and on every solid model; none on the birches (the thin-mesh rule)",
		"grade_and_paper": "off"}


func _apply_stack() -> void:
	for m in world_mats:
		m.set_shader_parameter("ramp_mix", 1.0 if stack_on else 0.0)
	PaintStack.set_character_ramp(_char_saved, stack_on)
	PaintStack.post_set(post_mat, "ink_on", 1.0 if (stack_on and ink_on) else 0.0)
	PaintStack.post_set(post_mat, "grade_on", 0.0)
	if post_q != null:
		post_q.visible = stack_on and ink_on
	_update_hud()


func set_stack(on: bool) -> void:
	stack_on = on
	_apply_stack()


func set_ink(on: bool) -> void:
	ink_on = on
	_apply_stack()


# --- play ---------------------------------------------------------------------------------
func _process(_dt: float) -> void:
	if knight == null or not ready_done:
		return
	var aim := _camera_aim()
	look_at_world(aim)
	if snowfall != null:
		snowfall.global_position = aim + up * 9.0 - fwd * 6.0


func _build_hud() -> void:
	var layer := CanvasLayer.new()
	layer.name = "HUD"
	add_child(layer)
	var bar := ColorRect.new()
	bar.color = Color(PaintStack.INK.r, PaintStack.INK.g, PaintStack.INK.b, 0.72)
	bar.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	bar.offset_top = -26.0
	bar.offset_bottom = 0.0
	layer.add_child(bar)
	_hud = Label.new()
	_hud.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_hud.offset_top = -24.0
	_hud.offset_bottom = -2.0
	_hud.offset_left = 10.0
	_hud.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_hud.add_theme_font_size_override("font_size", 14)
	_hud.add_theme_color_override("font_color", Color(0.94, 0.93, 0.90))
	layer.add_child(_hud)
	_update_hud()


func _update_hud() -> void:
	if _hud == null:
		return
	var n := 0
	var total := 0
	var nm := "-"
	var fs := 1.0
	if knight != null:
		n = knight.gear_stack
		total = knight.gear_stack_count()
		var names: Array = knight.cfg.get("gear_stack_names", [])
		if n < names.size():
			nm = String(names[n])
		fs = knight._figure_scale
	_hud.text = ("PAINTED" if painted else "BLOCKOUT") + (("  ·  SORCERESS: Space Fire Ball · X Meteor" if knight == null or knight.armed() else "  ·  SORCERESS: no staff, no spells (G for her gear)") if who == "sorceress" else "") + ("  ·  WASD move · Shift run · Space slash · X chop · C bash · B block · G gear (%d/%d: %s) · [ ] size (%.2f)"
		+ "   ‖   V stack (%s) · K ink (%s) · O overlay (%s) · R crucible marks (%s) · U camera clamp (%s)") \
		% [n + 1, total, nm, fs, "on" if stack_on else "off", "on" if ink_on else "off",
		   "on" if overlay_on else "off", "on" if crucible_on else "off", "on" if clamp_on else "off"]
	if painted:
		var hv: bool = _heather_mmi.is_empty() or (_heather_mmi[0] as Node3D).visible
		_hud.text += "  · H heather (%s) · N snowfall (%s)" % ["on" if hv else "off",
			"on" if (snowfall != null and snowfall.visible) else "off"]


func _touch_for_her(tc) -> void:
	"""HER BUTTONS (the coordinator): SLASH is the Fire Ball, CHOP the Meteor; BASH and BLOCK are hidden --
	she has no shield. GEAR steps her five stacks, base body to full kit (so_d7/scene_pkg, GEAR), and her
	two spell buttons show only while she is armed(): the staff is in the last stack only. The same
	actions underneath."""
	var keep := []
	_her_spell_buttons.clear()
	for b in tc._buttons:
		var lb := String(b.get("label", ""))
		if lb in ["BASH", "BLOCK"]:
			continue
		if lb == "SLASH":
			b["label"] = "FIRE BALL"
			_her_spell_buttons.append(b)
			continue
		elif lb == "CHOP":
			b["label"] = "METEOR"
			_her_spell_buttons.append(b)
			continue
		keep.append(b)
	tc._buttons = keep
	_touch_her_armed()


func _touch_for_strikes(tc) -> void:
	"""R-C9-117: THE DARK KNIGHT'S BUTTONS (and the unarmed champion's): SLASH is his attack (the champion's whirlwind),
	CHOP his war cry; BASH and BLOCK hidden -- neither has a shield. GEAR as his."""
	var keep := []
	var names := {"SLASH": "ATTACK", "CHOP": "WAR CRY"} if who == "warlord" else {"SLASH": "WHIRLWIND", "CHOP": "WAR CRY"}
	for b in tc._buttons:
		var lb := String(b.get("label", ""))
		if lb in ["BASH", "BLOCK"]:
			continue
		if names.has(lb):
			b["label"] = names[lb]
		keep.append(b)
	tc._buttons = keep


func _touch_her_armed() -> void:
	"""Her spell buttons follow the staff: shown while knight.armed(), re-checked after every GEAR press."""
	if touch == null or who != "sorceress":
		return
	var tc = touch
	var keep := []
	for b in tc._buttons:
		if not _her_spell_buttons.has(b):
			keep.append(b)
	if knight == null or knight.armed():      # she starts in the full kit, as he does
		keep.append_array(_her_spell_buttons)
	tc._buttons = keep
	if tc._overlay != null:
		tc._overlay.queue_redraw()


func _build_fx_label() -> void:
	"""The placeholder, SAID on screen: her spells are stand-ins until her VFX are made."""
	var layer := CanvasLayer.new()
	layer.name = "FxLabel"
	layer.layer = 21
	add_child(layer)
	var l := Label.new()
	l.text = "METEOR EFFECT: PAINTED KIT (LANE A)" if spell_fx != null and spell_fx.meteor_a != null else "METEOR EFFECT: PLACEHOLDER"
	l.add_theme_font_size_override("font_size", 22)
	l.add_theme_color_override("font_color", Color(1.0, 0.86, 0.6, 0.9))
	l.add_theme_color_override("font_outline_color", Color(0.1, 0.07, 0.05, 0.9))
	l.add_theme_constant_override("outline_size", 6)
	l.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	l.offset_left = -420.0
	l.offset_right = -24.0
	l.offset_top = 20.0
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	layer.add_child(l)


func set_hud_visible(on: bool) -> void:
	var l := get_node_or_null(^"HUD") as CanvasLayer
	if l != null:
		l.visible = on


func step_size(d: int) -> void:
	if knight == null:
		return
	var steps: Array = knight.cfg.get("scale_steps", [])
	if steps.is_empty():
		return
	_size_step = clampi(_size_step + d, 0, steps.size() - 1)
	knight.set_figure_scale(float(steps[_size_step]))
	_update_hud()


func _unhandled_input(e: InputEvent) -> void:
	if e.is_action_pressed("gear_cycle") and knight != null:
		knight.cycle_gear()
		_touch_her_armed()
		_update_hud()
	elif e.is_action_pressed("size_down"):
		step_size(-1)
	elif e.is_action_pressed("size_up"):
		step_size(1)
	elif e is InputEventKey and (e as InputEventKey).pressed and not (e as InputEventKey).echo:
		match (e as InputEventKey).physical_keycode:
			KEY_V: set_stack(not stack_on)
			KEY_K: set_ink(not ink_on)
			KEY_O: set_overlay(not overlay_on)
			KEY_U:
				clamp_on = not clamp_on
				_update_hud()
			KEY_R: set_crucible_visible(not crucible_on)
			KEY_H:
				for mmi in _heather_mmi:
					(mmi as Node3D).visible = not (mmi as Node3D).visible
				_update_hud()
			KEY_N:
				if snowfall != null:
					snowfall.visible = not snowfall.visible
					snowfall.emitting = snowfall.visible
				_update_hud()


func _check_key_collisions() -> void:
	"""barrow_world's check: are V, K, O, U spoken for by a PROJECT action on the bare key?"""
	var project := {}
	var builtin := {}
	for action in InputMap.get_actions():
		for ev in InputMap.action_get_events(action):
			var ke := ev as InputEventKey
			if ke == null:
				continue
			var code: int = ke.physical_keycode if ke.physical_keycode != 0 else ke.keycode
			var bare: bool = not (ke.ctrl_pressed or ke.alt_pressed or ke.meta_pressed
								  or ke.shift_pressed or ke.command_or_control_autoremap)
			for name in RAW_KEYS:
				if code != RAW_KEYS[name] or not bare:
					continue
				if String(action).begins_with("ui_"):
					builtin[name] = String(action)
				else:
					project[name] = String(action)
					push_warning("barrow_full: key %s also drives project action '%s'" % [name, action])
	report["key_collisions"] = {"raw_keys": {"V": "stack", "K": "ink", "O": "overlay", "U": "camera clamp", "R": "crucible marks",
								"H": "3D heather (painted)", "N": "falling snow (painted)"},
		"clashes_with_project_actions": project, "bare_builtin_ui_informational": builtin,
		"_clear": project.is_empty()}


# --- what the capture tool needs ----------------------------------------------------------
func park_camera(aim: Vector3, zoom := 1.0) -> void:
	set_process(false)
	cam.size = (float(_view_height()) / PPM) / maxf(zoom, 1e-3)
	_sync_post_scale()
	look_at_world(aim)


func unpark_camera() -> void:
	cam.size = float(_view_height()) / PPM
	_sync_post_scale()
	set_process(true)


func set_topdown(centre_uv: Vector2, height_m: float) -> void:
	"""Straight down, screen-right = +u and screen-up = +v: the map's base render."""
	set_process(false)
	var c := uv_to_world(centre_uv.x, centre_uv.y)
	cam.size = height_m
	cam.look_at_from_position(c + Vector3.UP * CAM_STANDOFF, c, v_hat)
	_sync_post_scale()


func freeze_pose(on: bool) -> void:
	if knight == null:
		return
	var mode := AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL if on \
		else AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS
	for n in knight.find_children("*", "AnimationMixer", true, false):
		(n as AnimationMixer).callback_mode_process = mode


func character_screen_rect() -> Rect2:
	var lo := Vector2(1e9, 1e9)
	var hi := Vector2(-1e9, -1e9)
	for n in knight.find_children("*", "Skeleton3D", true, false):
		var sk := n as Skeleton3D
		for b in sk.get_bone_count():
			var p := cam.unproject_position(sk.global_transform * sk.get_bone_global_pose(b).origin)
			lo = lo.min(p)
			hi = hi.max(p)
	return Rect2(lo, hi - lo)


func canvas_dir_uv(from: Vector2, to: Vector2) -> Vector2:
	"""A ground direction in (u, v) as the canvas direction knight.gd drives on. His map is
	world = right*(vx/PPM) + lz*((vy/PPM)/sin(pitch)), with right = u_hat and lz = -v_hat, so
	the canvas vector for a ground step (du, dv) is (du, -dv*sin(pitch))."""
	var d := to - from
	if d.length() < 1e-6:
		return Vector2.ZERO
	return Vector2(d.x, -d.y * sin(deg_to_rad(PL_PITCH_DEG))).normalized()


func knight_uv() -> Vector2:
	return world_to_uv(knight.global_position)


func build_records() -> Dictionary:
	"""EVERYTHING THE SCENE BUILT, in world and (u, v), measured off the built meshes: where
	each piece stands, its full transform, its size, and its ground footprint -- the convex
	hull of its vertices, once for all of them and once for those under 1.9 m (what a 1.85 m
	man can walk into). Heavy (every vertex of every model), so it runs on request only."""
	var out := {}
	for id in nodes:
		var root := nodes[id] as Node3D
		var rec: Dictionary = built.get(id, {}).duplicate()
		var t := root.global_transform
		rec["world_origin"] = _v3(t.origin)
		rec["world_basis_columns"] = [_v3(t.basis.x), _v3(t.basis.y), _v3(t.basis.z)]
		var vv := world_verts(root)
		var lo := INF
		var hi := -INF
		var all := PackedVector2Array()
		var low := PackedVector2Array()
		for p in vv:
			lo = minf(lo, p.y)
			hi = maxf(hi, p.y)
			var q := world_to_uv(p)
			all.append(q)
			if p.y <= LOW_M:
				low.append(q)
		rec["y_min"] = snappedf(lo, 0.001)
		rec["y_max"] = snappedf(hi, 0.001)
		rec["verts"] = vv.size()
		rec["footprint_uv_all"] = _hull_arr(all)
		rec["footprint_uv_low"] = _hull_arr(low)
		var o := world_to_uv(t.origin)
		rec["origin_uv"] = [snappedf(o.x, 0.0001), snappedf(o.y, 0.0001)]
		out[id] = rec
	return out


func _group_of(n: Node) -> String:
	"""Which placement a collider belongs to: the node directly under Props or Level."""
	var cur := n
	while cur != null and cur.get_parent() != null:
		var par := cur.get_parent()
		if par == props_root or par == level:
			var nm := String(cur.name)
			return "bounds" if nm == "Bounds" else nm
		cur = par
	return "?"


func collider_footprints() -> Array:
	"""EVERY OBSTACLE HE CAN WALK INTO, as ground polygons: each collision shape on the terrain
	layer (the floor excepted), cut to the slab his capsule occupies (y 0.05 to 1.9) and projected
	to (u, v). What the no-squeeze instrument measures between -- the colliders themselves, not
	the meshes' idea of them."""
	var out := []
	for n in find_children("*", "StaticBody3D", true, false):
		var sb := n as StaticBody3D
		if (sb.collision_layer & TERRAIN_BIT) == 0 or String(sb.name) == "FloorBody":
			continue
		var grp := _group_of(sb)
		for ch in sb.get_children():
			var cs := ch as CollisionShape3D
			if cs == null or cs.shape == null:
				continue
			var t: Transform3D = cs.global_transform
			var pts := PackedVector3Array()
			var lo := INF
			var hi := -INF
			if cs.shape is BoxShape3D:
				var h: Vector3 = (cs.shape as BoxShape3D).size * 0.5
				for sx in [-1.0, 1.0]:
					for sy in [-1.0, 1.0]:
						for sz in [-1.0, 1.0]:
							var w := t * Vector3(h.x * sx, h.y * sy, h.z * sz)
							pts.append(w)
							lo = minf(lo, w.y)
							hi = maxf(hi, w.y)
			elif cs.shape is CylinderShape3D:
				var cy := cs.shape as CylinderShape3D
				for k in 16:
					var a := TAU * float(k) / 16.0
					for sy in [-1.0, 1.0]:
						var w := t * Vector3(cy.radius * cos(a), cy.height * 0.5 * sy, cy.radius * sin(a))
						pts.append(w)
						lo = minf(lo, w.y)
						hi = maxf(hi, w.y)
			elif cs.shape is ConvexPolygonShape3D:
				for p in (cs.shape as ConvexPolygonShape3D).points:
					var w := t * p
					lo = minf(lo, w.y)
					hi = maxf(hi, w.y)
					if w.y <= LOW_M:
						pts.append(w)
			if hi < 0.05 or lo > LOW_M or pts.size() < 3:
				continue
			var p2 := PackedVector2Array()
			for w in pts:
				p2.append(world_to_uv(w))
			out.append({"group": grp, "poly": _hull_arr(p2)})
	return out


func set_door_mask(mode: String) -> void:
	"""THE DOOR-VISIBILITY INSTRUMENT. "mask": the door frame's (lintel's and posts') surfaces
	that face the camera side (-v) render pure magenta, unlit; everything else as it is.
	"alone": the same, with every other visible thing hidden. "off": put it all back."""
	var door_ids := ["door_lintel", "door_post_L", "door_post_R"]
	if mode == "off":
		for mi in _door_saved.get("mats", {}):
			(mi as MeshInstance3D).material_override = _door_saved["mats"][mi]
		for nd in _door_saved.get("hidden", []):
			(nd as Node3D).visible = true
		for mi in _prop_inks:
			(mi as MeshInstance3D).visible = true
		if post_q != null:
			post_q.visible = stack_on and ink_on
		_door_saved = {}
		return
	if _door_saved.is_empty():
		var sh := Shader.new()
		sh.code = """
shader_type spatial;
render_mode unshaded, cull_back, shadows_disabled, fog_disabled;
uniform vec3 face_dir = vec3(0.0, 0.0, 1.0);
varying vec3 wn;
void vertex() { wn = normalize((MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz); }
void fragment() { ALBEDO = dot(normalize(wn), face_dir) > 0.3 ? vec3(1.0, 0.0, 1.0) : vec3(0.06, 0.06, 0.06); }
"""
		var mat := ShaderMaterial.new()
		mat.shader = sh
		mat.set_shader_parameter("face_dir", -v_hat)
		var mats := {}
		for id in door_ids:
			for mi in _meshes(nodes[id]):
				mats[mi] = (mi as MeshInstance3D).material_override
				(mi as MeshInstance3D).material_override = mat
		_door_saved = {"mats": mats, "hidden": []}
		for mi in _prop_inks:
			(mi as MeshInstance3D).visible = false
		if post_q != null:
			post_q.visible = false
	if mode == "alone":
		var hide := []
		for ch in level.get_children():
			if (ch as Node3D).visible:
				hide.append(ch)
		for ch in props_root.get_children():
			if not (String(ch.name) in door_ids) and (ch as Node3D).visible:
				hide.append(ch)
		if knight != null and knight.visible:
			hide.append(knight)
		for nd in hide:
			(nd as Node3D).visible = false
		_door_saved["hidden"] = hide


func _hull_arr(pts: PackedVector2Array) -> Array:
	if pts.size() < 3:
		return []
	var h := Geometry2D.convex_hull(pts)
	var a := []
	for p in h:
		a.append([snappedf(p.x, 0.0001), snappedf(p.y, 0.0001)])
	return a


# --- the app's own frame cost (--frame-cost) ----------------------------------------------
func _frame_cost_mode() -> void:
	"""Run from the EXPORTED app: `.../MacOS/<exe> -- --frame-cost`. He walks a loop round the
	ring with vsync off and the wall clock is divided by the frames drawn -- the only instrument
	that measured anything in barrow_world's capture (the GPU counter read 0.00)."""
	await get_tree().process_frame
	knight.set_physics_process(false)
	Engine.max_fps = 0
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	place_knight(0.0, -3.0, "N")
	var loop := [Vector2(4.0, 1.0), Vector2(0.0, 5.0), Vector2(-4.0, 1.0), Vector2(0.0, -3.0)]
	var wi := 0
	var dt := 1.0 / 60.0
	for i in 90:
		knight.drive_dir(canvas_dir_uv(knight_uv(), loop[wi]), false, dt)
		await get_tree().process_frame
	var n := 600
	var t0 := Time.get_ticks_usec()
	for i in n:
		if knight_uv().distance_to(loop[wi]) < 0.6:
			wi = (wi + 1) % loop.size()
		knight.drive_dir(canvas_dir_uv(knight_uv(), loop[wi]), false, dt)
		await get_tree().process_frame
	var ms := float(Time.get_ticks_usec() - t0) / 1000.0 / float(n)
	# viewport = the FRAME (1920 x 1080 under the lock); render = the px actually drawn; window =
	# the OS window, bars included. The first two differ fullscreen on a wider screen.
	# render = the size of the IMAGE the viewport yields (one readback, after the timing) -- the
	# texture's reported size is not the px drawn under canvas_items (see _render_scale).
	var img_sz := get_viewport().get_texture().get_image().get_size()
	var ws := DisplayServer.window_get_size()
	print("[barrow_full] frame_cost ms_per_frame=%.2f fps=%.1f viewport=%dx%d frames=%d render=%dx%d window=%dx%d" % [
		ms, 1000.0 / maxf(ms, 1e-3), _view_width(), _view_height(), n,
		img_sz.x, img_sz.y, ws.x, ws.y])
	get_tree().quit()


# --- the app's own view check (--view-check) ----------------------------------------------
func _view_check_mode() -> void:
	"""Run from the EXPORTED app: `.../MacOS/<exe> [--fullscreen] -- --view-check --cells
	"name:u,v;..." [--clamp on|off] [--out DIR] [--tag T]`. THE FRAME, MEASURED BY THE CAMERA
	ITSELF: at each cell he is placed and the camera follows as in play; a ray through each
	corner of the visible frame is intersected with the floor -- the ground the frame actually
	shows. Reported in metres, and in the guide window's px (the guide and the play camera are
	one projection at one scale, so a corner's ground point IS its guide px). Negative px =
	that much margin inside the window."""
	var args := OS.get_cmdline_user_args()
	var cells := []
	var out_dir := ""
	var tag := "view"
	for i in args.size():
		var a := String(args[i])
		if i + 1 >= args.size():
			break
		var nxt := String(args[i + 1])
		if a == "--cells":
			for tok in nxt.split(";", false):
				var kv := tok.split(":")
				var xy := kv[1].split(",")
				cells.append([kv[0], float(xy[0]), float(xy[1])])
		elif a == "--out":
			out_dir = nxt
		elif a == "--tag":
			tag = nxt
		elif a == "--clamp":
			clamp_on = nxt == "on"
	# THE WINDOW SETTLES FIRST: a --fullscreen window on macOS animates into its own Space over
	# several hundred ms, and measuring during it measures a window that is not the one played.
	var stable := 0
	var last := Vector2i.ZERO
	var waited := 0
	while waited < 900 and stable < 45:
		await get_tree().process_frame
		waited += 1
		var s := DisplayServer.window_get_size()
		stable = stable + 1 if s == last else 0
		last = s
	var gw: Dictionary = layout["frame"]["guide_window"]
	var u0 := float(gw["u"][0])
	var v1 := float(gw["v"][1])
	var W := float(gw["px"][0])
	var H := float(gw["px"][1])
	var px_up := PPM * sin(deg_to_rad(PL_PITCH_DEG))
	var rt := get_viewport().get_texture()
	var ws := DisplayServer.window_get_size()
	var ss := DisplayServer.screen_get_size()
	var vr := get_viewport().get_visible_rect().size
	var lock := _view_lock()
	var img_sz := rt.get_image().get_size()          # the px drawn, read off the image itself
	var ft := get_viewport().get_final_transform()
	var res := {"tag": tag, "window_px": [ws.x, ws.y], "screen_px": [ss.x, ss.y],
		"window_mode": DisplayServer.window_get_mode(), "frames_waited_for_the_window": waited,
		"render_px": [img_sz.x, img_sz.y], "render_px_from_the_final_transform": [_render_px().x, _render_px().y],
		"texture_reported_size_NOT_the_render": [rt.get_width(), rt.get_height()],
		"final_transform": {"scale": snappedf(ft.get_scale().y, 0.0001), "origin_px": [ft.origin.x, ft.origin.y]},
		"frame_px": [int(vr.x), int(vr.y)],
		"bars_px_each_side": [(ws.x - img_sz.x) / 2, (ws.y - img_sz.y) / 2],
		"stretch": {"mode": lock[0], "aspect": lock[1], "base": [lock[2], lock[3]]},
		"cam_size_m": snappedf(cam.size, 0.0001), "line_px_render": snappedf(LINE_PX * _render_scale(), 0.0001),
		"clamp_on": clamp_on, "clamp_key": "U" if RAW_KEYS.has("U") else "", "cells": {}}
	for c in cells:
		place_knight(float(c[1]), float(c[2]), "N")
		for k in 12:
			await get_tree().process_frame
		var at := world_to_uv(knight.global_position)
		var g := {}
		for corner in ["TL", "TR", "BL", "BR"]:
			var sp := Vector2(0.0 if corner.ends_with("L") else vr.x, 0.0 if corner.begins_with("T") else vr.y)
			var o := cam.project_ray_origin(sp)
			var d := cam.project_ray_normal(sp)
			g[corner] = world_to_uv(o + d * (-o.y / d.y))
		var x := func(q: Vector2) -> float: return (q.x - u0) * PPM
		var y := func(q: Vector2) -> float: return (v1 - q.y) * px_up
		var rec := {"cell_uv": [c[1], c[2]], "him_uv": [snappedf(at.x, 0.001), snappedf(at.y, 0.001)],
			"frame_ground_uv": {}, 
			"extent_m": {"across": snappedf((g["TR"] - g["TL"]).length(), 0.0001),
						 "up_screen_ground": snappedf((g["TL"] - g["BL"]).length(), 0.0001)},
			"px_outside_by_side": {
				"left_px": snappedf(-minf(x.call(g["TL"]), x.call(g["BL"])), 0.1),
				"right_px": snappedf(maxf(x.call(g["TR"]), x.call(g["BR"])) - W, 0.1),
				"bottom_px": snappedf(maxf(y.call(g["BL"]), y.call(g["BR"])) - H, 0.1),
				"top_px": snappedf(-minf(y.call(g["TL"]), y.call(g["TR"])), 0.1)}}
		for corner in g:
			rec["frame_ground_uv"][corner] = [snappedf(g[corner].x, 0.001), snappedf(g[corner].y, 0.001)]
		if out_dir != "":
			var img := rt.get_image()
			var path := out_dir.path_join("%s_%s.png" % [tag, String(c[0])])
			rec["still"] = path if img.save_png(path) == OK else "save failed"
		res["cells"][String(c[0])] = rec
	print("[barrow_full] view_check " + JSON.stringify(res))
	get_tree().quit()


# =============================================================================
#  THE PAINTED BARROW (T10-2 step 4): the blockout above, dressed in the painting
# =============================================================================
const HEATHER_SNOW_FRAC := 0.2      # the installed Barrow's: a clump's snow capped at 20% of its height
const WEB_SHADOW_NORMAL_BIAS := 1.0  # the installed Barrow's (barrow_world, swept on Compatibility)


func _dress_painted() -> void:
	"""NOTHING BUILT ABOVE MOVES. Every collider and every transform is the blockout's own, so
	the walkable area, the no-squeeze rule and the camera margin are the blockout's by
	construction (and re-measured: tools/accept_painted.py). What changes is what each surface
	wears, which sun reaches it, and what stands on it:
	  the painted pieces (ground, mound, 29 primitives, 33 birches: the painting, projected; the
	    25 real models: their bakes) -- unlit, no pen, layer LAYER_PAINTED, lit by the paint sun;
	  the sun lights him and everything dynamic, every caster in its shadow (b);
	  the paint sun lights the painting, HIS shadow the only one in it (a, c);
	  the 3D heather and the 3D snow wear the painting too, under the ramp, on LAYER_ON_PAINT."""
	var t0 := Time.get_ticks_msec()
	var man := PaintedWorld.read_manifest()
	var loads := {}
	paint = {"manifest": PaintedWorld.MANIFEST, "loads": loads, "ground_variant": ground_variant}
	if man.is_empty():
		push_error("barrow_painted: no manifest at %s" % PaintedWorld.MANIFEST)
		paint["error"] = "no manifest"
		return
	var sm: Array = man["shadow_mul"]["linear"]
	var shadow_mul := Vector3(float(sm[0]), float(sm[1]), float(sm[2]))
	var painting := PaintedWorld.load_png_bin(String(man["painting"]["file"]), String(man["painting"]["sha256"]), true, loads)
	var gk := "ground_" + ground_variant
	# as_painted, the ground IS the painting's file: one decode, one texture, one sha check
	var ground_tex: Texture2D = painting if String(man[gk]["file"]) == String(man["painting"]["file"]) \
		else PaintedWorld.load_png_bin(String(man[gk]["file"]), String(man[gk]["sha256"]), true, loads)
	paint["ground_file"] = String(man[gk]["file"])
	var lit := PaintedWorld.load_png_bin(String(man["lit"]["file"]), String(man["lit"]["sha256"]), false, loads)
	_paint_tex = {"painting": painting, "ground": ground_tex, "lit": lit}
	var mat_paint := PaintedWorld.painted_material(painting, true, lit, shadow_mul, u_hat, v_hat)
	var mat_ground := PaintedWorld.painted_material(ground_tex, true, lit, shadow_mul, u_hat, v_hat)
	var n := {"ground": 0, "mound": 0, "primitives": 0, "birches": 0, "baked": 0, "baked_meshes": 0,
			  "inks_hidden": 0, "bakes_missing": []}
	_paint_mesh(level.get_node_or_null(^"Ground") as MeshInstance3D, mat_ground, false)
	n["ground"] = 1
	for mi in _meshes(nodes["mound"]):
		_paint_mesh(mi, mat_paint, true)
		n["mound"] += 1
	var bakes: Dictionary = man["bakes"]
	for e in layout["placements"]:
		var id := String(e["id"])
		if id == "mound" or not nodes.has(id):
			continue
		if String(e["kind"]) == "primitive" or String(e.get("class", "")) == "birch":
			for mi in _meshes(nodes[id]):
				_paint_mesh(mi, mat_paint, true)
			n["birches" if String(e.get("class", "")) == "birch" else "primitives"] += 1
			continue
		if not bakes.has(id):
			n["bakes_missing"].append(id)
			continue
		var b: Dictionary = bakes[id]
		var tex := PaintedWorld.load_png_bin(String(b["file"]), String(b["sha256"]), true, loads)
		var mat := PaintedWorld.painted_material(tex, false, lit, shadow_mul, u_hat, v_hat)
		for mi in _meshes(nodes[id]):
			_paint_mesh(mi, mat, true)
			n["baked_meshes"] += 1
		n["baked"] += 1
	for ink in _prop_inks:
		(ink as MeshInstance3D).visible = false
		n["inks_hidden"] += 1
	# THE TWO SUNS (PaintedWorld's header; tools/probe_paint_light.gd -- and on the phone's renderer
	# too: work/probe/probe_paint_light_compat.json, Compatibility on ANGLE/Metal, the same answer)
	if PaintStack.is_compatibility():
		# the installed Barrow's measured web bias: Compatibility's shadow lookup acnes at 0.15
		sun.shadow_normal_bias = WEB_SHADOW_NORMAL_BIAS
	var paint_layers := PaintedWorld.LAYER_PAINTED | PaintedWorld.LAYER_ON_PAINT
	var dyn := PaintedWorld.ALL_LAYERS & ~paint_layers
	sun.light_cull_mask = dyn
	sun.shadow_caster_mask = PaintedWorld.ALL_LAYERS
	paint_sun = sun.duplicate() as DirectionalLight3D
	paint_sun.name = "PaintSun"
	paint_sun.light_cull_mask = paint_layers
	paint_sun.shadow_caster_mask = dyn
	sun.get_parent().add_child(paint_sun)
	paint_sun.global_transform = sun.global_transform
	# HIS SHADOW, SHARP ENOUGH TO BE HIS (tools/capture_painted.gd --shadow-test, measured on open
	# sunlit snow, his shadow term on against off): at the sun's own setting -- one orthogonal map
	# over 110 m, blur 1.7, now sharing the atlas with a second light -- his shadow came out a pale
	# smear, core only 0.67/0.74/0.93 of the snow against the painter's 0.42/0.55/0.89, and a
	# halftone dither over it. The painted world lies 53-65 m from the camera (standoff 60 m, the
	# frame's ground +-7.4 m up-screen x cos(pitch), the tallest piece 3.4 m), so the paint sun's map
	# stops at 68 m and blurs at 0.6: core 0.46/0.58/0.90 -- the painter's own shadow value -- in the
	# shape of a man. (8192 px of atlas reached 0.42/0.55/0.89 and was not needed.) The sun keeps its
	# installed 1.7: the stones' shadows on HIM are soft, as painted.
	paint_sun.directional_shadow_mode = DirectionalLight3D.SHADOW_ORTHOGONAL
	paint_sun.directional_shadow_max_distance = CAM_STANDOFF + 8.0
	paint_sun.shadow_blur = 0.6
	# THE PEN: off the painted pieces (their mark), on everything else as installed
	PaintStack.post_set(post_mat, "painted_exclude", 1.0)
	_build_painted_heather(man, lit, shadow_mul)
	_build_painted_snow(man, ground_tex, lit, shadow_mul)
	var flake := PaintStack.make_flake_texture()
	snowfall = PaintStack.snowfall(flake, Vector3(46, 28, 46), 1700)
	snowfall.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(snowfall)
	var ok := 0
	var bad := []
	for k in loads:
		if bool(loads[k].get("sha256_ok", false)) and not loads[k].has("error"):
			ok += 1
		else:
			bad.append(k)
	paint["pieces"] = n
	paint["files_ok"] = ok
	paint["files_bad"] = bad
	paint["shadow_mul_linear"] = sm
	paint["suns"] = {"sun": {"cull": sun.light_cull_mask, "casters": sun.shadow_caster_mask},
					 "paint_sun": {"cull": paint_sun.light_cull_mask, "casters": paint_sun.shadow_caster_mask}}
	if PaintStack.is_compatibility():
		# THE INSTALLED BARROW'S WEB PATH, unchanged in kind (barrow_world, R-C9-83): one pen on him
		# -- the depth-only web pen draws him, so his hull is hidden rather than doubled -- the ambient
		# moved into the sun's pass (Compatibility sums a shadowed light's pass after sRGB-encoding
		# each; the painted surfaces take no ambient at all), and the albedo maths' colour space
		for e in _char_saved.get("inks", []):
			var hm = e.get("mi")
			if hm is Node3D and is_instance_valid(hm):
				(hm as Node3D).visible = false
		var cl := PaintStack.move_ambient_into_light(self, env_node.environment)
		# the painted surfaces are "lit without the ramp" BY DESIGN: ambient_light_disabled, the
		# painting is their light -- counted apart, so a real omission would still show
		var painted_n := 0
		var other := []
		for w in cl.get("lit_without_ramp", []):
			if String(w).contains("ShaderMaterial"):
				painted_n += 1
			else:
				other.append(w)
		cl["lit_without_ramp"] = other
		cl["painted_no_ambient_by_design"] = painted_n
		paint["compat_light"] = cl
		paint["compat_color"] = PaintStack.web_color_space(self)
	if PaintStack.is_web():
		# THE PHONE'S TUNING LEVERS, off the page URL, as the installed Barrow's: ?msaa=0|2|4|8 and
		# ?scale3d=0.25..1.0 (the 3D drawn smaller and scaled up; the thumb controls stay sharp)
		var qm := PaintStack.web_query("msaa")
		if qm != "":
			var msaa_by := {"0": Viewport.MSAA_DISABLED, "2": Viewport.MSAA_2X, "4": Viewport.MSAA_4X,
				"8": Viewport.MSAA_8X}
			get_viewport().msaa_3d = msaa_by.get(qm, get_viewport().msaa_3d)
		var qs := PaintStack.web_query("scale3d")
		if qs != "" and qs.is_valid_float():
			get_viewport().scaling_3d_scale = clampf(float(qs), 0.25, 1.0)
		paint["web_levers"] = {"msaa_3d": get_viewport().msaa_3d, "scaling_3d_scale": get_viewport().scaling_3d_scale}
	paint["ms"] = Time.get_ticks_msec() - t0
	report["painted"] = paint


func _paint_mesh(mi: MeshInstance3D, mat: ShaderMaterial, casts: bool) -> void:
	if mi == null:
		return
	mi.material_override = mat
	mi.layers = PaintedWorld.LAYER_PAINTED
	# A PAINTED PIECE STILL CASTS -- for the SUN, onto him (b). The paint sun takes no caster on
	# this layer (its shadow_caster_mask), so none of it reaches the painted world (c).
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON if casts \
		else GeometryInstance3D.SHADOW_CASTING_SETTING_OFF


func _build_painted_heather(man: Dictionary, lit: Texture2D, shadow_mul: Vector3) -> void:
	"""The 954 heather sprays and 23 shrub clumps (take/build/heather_instances.json, placed FROM
	the painting's tufts), as BarrowHeather's generated sprays in six MultiMeshes -- one per
	variant, variant and +-15% height by index as the installed Barrow picks them. Each carries
	the painting beneath it as its colour (INSTANCE_CUSTOM)."""
	var hj = JSON.parse_string(FileAccess.get_file_as_string(PaintedWorld.data_dir() + String(man["heather"]["file"])))
	var rows: Array = hj["rows"] if typeof(hj) == TYPE_DICTIONARY else []
	var am: Array = man["heather"]["albedo_mul"]
	heather_mat = PaintedWorld.heather_material(fbm, Vector3(float(am[0]), float(am[1]), float(am[2])),
		lit, shadow_mul, u_hat, v_hat)
	heather_mat.set_shader_parameter("wind_dir", WIND.normalized())
	var by_var := []
	for v in BarrowHeather.VARIANTS:
		by_var.append([])
	for i in rows.size():
		by_var[int(fposmod(float(i) * 7.0 + 3.0, float(BarrowHeather.VARIANTS)))].append(i)
	var thin := []
	var tris := 0
	for v in BarrowHeather.VARIANTS:
		var mesh := BarrowHeather.spray_mesh(v)
		var ab := mesh.get_aabb()
		var mm := MultiMesh.new()
		mm.transform_format = MultiMesh.TRANSFORM_3D
		mm.use_custom_data = true
		# INSTANCE COLOURS ON, EVERY ONE WHITE. The phone's renderer reads a MultiMesh's vertex COLOR as
		# BLACK when it has no instance colours (tools/probe_mm_custom.gd: Compatibility 0/0/0 where
		# Forward+ reads the vertex's own; with white instance colours both read the vertex's) -- and
		# a spray's whole colour, stem to sprig, is in its vertices: every spray drew black on the web
		mm.use_colors = true
		mm.mesh = mesh
		mm.instance_count = (by_var[v] as Array).size()
		for k in (by_var[v] as Array).size():
			var i: int = by_var[v][k]
			var r: Array = rows[i]
			# [x, z, height_m, class (0 heather, 1 shrub), mul r, g, b]
			var hh := float(r[2]) * (0.85 + 0.30 * fposmod(float(i) * 0.6180339, 1.0))
			mm.set_instance_transform(k, Transform3D(Basis().scaled(Vector3.ONE * hh), Vector3(float(r[0]), -0.01, float(r[1]))))
			mm.set_instance_custom_data(k, Color(float(r[4]), float(r[5]), float(r[6]), 1.0))
			mm.set_instance_color(k, Color(1, 1, 1, 1))
			thin.append({"c": Vector2(float(r[0]), float(r[1])), "r": maxf(ab.size.x, ab.size.z) * hh * 0.5 * 0.8,
						 "feather": 0.18, "max_d": hh * HEATHER_SNOW_FRAC})
		var mmi := MultiMeshInstance3D.new()
		mmi.name = "Heather_%d" % v
		mmi.multimesh = mm
		mmi.material_override = heather_mat
		mmi.layers = PaintedWorld.LAYER_ON_PAINT
		mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		add_child(mmi)
		_heather_mmi.append(mmi)
		tris += mesh.surface_get_array_index_len(0) / 3 * mm.instance_count
	paint["heather"] = {"instances": rows.size(), "multimeshes": _heather_mmi.size(), "tris": tris,
						"albedo_mul": am}
	paint["_thin_zones"] = thin


func _build_painted_snow(man: Dictionary, ground_tex: Texture2D, lit: Texture2D, shadow_mul: Vector3) -> void:
	"""THE INSTALLED SNOW FIELD, flat: his ankle-deep layer where the painting's ground is snow,
	thinner on the path and the heather, none on the ice (the depth grid, from the painted splat);
	no windrows, piles or skirts -- a drift the painting does not show would hide his legs in snow
	that looks flat. It wears the ground's painting (PaintedWorld.snow_shader_code): untouched, it
	IS the painting; where he walks, his prints take the ramp."""
	var sn: Dictionary = man["snow"]
	var g: Dictionary = sn["grid"]
	var buf := PaintedWorld.load_f32_bin(String(g["file"]), String(g["sha256"]), paint["loads"])
	var nx := int(g["nx"])
	var nz := int(g["nz"])
	if buf.size() != 2 * nx * nz:
		push_error("barrow_painted: the snow grid is %d floats, not %d" % [buf.size(), 2 * nx * nz])
		paint["snow_error"] = "grid size"
		return
	var go: Array = g["origin_xz"]
	snow = SnowField.new()
	snow.name = "SnowField"
	snow.fbm_tex = fbm
	snow.field_px = int(sn["field_px"])
	snow.trail_px = int(sn["trail_px"])
	snow.windrow_count = 0
	snow.pile_count = 0
	snow.cast_shadows = false
	snow.depth_grid = {"origin": Vector2(float(go[0]), float(go[1])), "cell_m": float(g["cell_m"]),
					   "nx": nx, "nz": nz, "mul": buf.slice(0, nx * nz), "trod": buf.slice(nx * nz, 2 * nx * nz)}
	snow.thin_zones = paint.get("_thin_zones", [])
	paint.erase("_thin_zones")
	snow.shader_code_override = PaintedWorld.snow_shader_code()
	var ar: Array = sn["area_xz"]
	snow.setup(Rect2(float(ar[0]), float(ar[1]), float(ar[2]), float(ar[3])), 0.0, [], WIND)
	add_child(snow)
	if knight != null:
		snow.track(knight)
	var smat := snow.material()
	smat.set_shader_parameter("paint_tex", ground_tex)
	PaintedWorld.bind_projection(smat, lit, shadow_mul, u_hat, v_hat)
	snow.surface().layers = PaintedWorld.LAYER_ON_PAINT
	if heather_mat != null:
		BarrowHeather.bind_snow(heather_mat, snow, WIND)
	var br := snow.bake_report()
	paint["snow"] = {"area_xz": ar, "field_px": snow.field_px, "trail_px": snow.trail_px,
					 "bare_frac_under_cut": br.get("bare_frac_under_cut"), "mean_depth_m": br.get("mean_depth_m"),
					 "thin_zones": br.get("thin_zones"), "bake_ms": br.get("ms", br.get("bake_ms"))}


func _physics_process(_dt: float) -> void:
	# THE HEATHER'S WIND RUNS ON THE SNOW'S CLOCK (the installed Barrow's rule, and its reason:
	# pushed here, not in _process, which park_camera() stops)
	if snow != null and heather_mat != null:
		heather_mat.set_shader_parameter("wind_time", snow.clock())


func _meteor_a_word() -> String:
	"""LANE A: the painted kit, baked -- its atlas, as the Fire Ball's word says its own."""
	var at: Dictionary = spell_fx.meteor_a.report.get("atlas", {})
	return "painted(lane_a,pages=%d,frames=%d,impact_sets=%d,sha_ok)" % [int(at.get("pages", 0)), int(at.get("frames", 0)), int(at.get("impact_sets", 0))]


func _her_line() -> String:
	"""HER PART OF THE LAUNCH LINE: whether her animation tree is VALID (every AnimationNodeAnimation
	names a clip she has -- an invalid tree applies no pose at all, see sorceress_knight.gd), which
	clipless nodes were filled, and the placeholder spells' casts and release times."""
	if who != "sorceress" or knight == null:
		return ""
	var bad := 0
	var bt := knight._tree.tree_root as AnimationNodeBlendTree if knight._tree != null else null
	if bt != null:
		for nm in bt.get_node_list():
			var n = bt.get_node(nm)
			if n is AnimationNodeAnimation and not knight._anim.has_animation((n as AnimationNodeAnimation).animation):
				bad += 1
	var sp := []
	var fb := "none"
	if spell_fx != null:
		for slot in ["attack", "chop"]:
			var c: Dictionary = spell_fx.casts_by_slot.get(slot, {})
			if not c.is_empty():
				sp.append("%s@%s" % [c["clip"], str(c["release_s"])])
		var fbr: Dictionary = spell_fx.report.get("fire_ball", {})
		if spell_fx.fire_ball != null:
			var at: Dictionary = fbr.get("atlas", {})
			fb = "baked(pages=%d,px=%dx%d,frames=%d,impact_sets=%d,sha_ok)" % [int(at.get("pages", 0)), int((at.get("px", [0, 0]) as Array)[0]),
				int((at.get("px", [0, 0]) as Array)[1]), int(at.get("frames", 0)), int(at.get("impact_sets", 0))]
			if bool(spell_fx.fire_ball.tighten):
				fb += "+c75"                    # ?fb=c75 (R-C9-110): the burst tightened to 0.75
		else:
			fb = "FAILED(%s)" % String(fbr.get("error", "?"))
	return " | sorceress_tree=%s clipless=%s spells=%s fire_ball=%s meteor=%s" % ["valid" if (bt != null and bad == 0) else "INVALID",
		",".join(PackedStringArray(knight.clipless_filled)), ",".join(PackedStringArray(sp)), fb,
		(("mix4(fall=lane_b_core,impact=lane_a,burn=crater_v4,warp=post,ring=off,shadow=%s,fall_s=%.2f)" % ["on" if meteor_fx.shadow_on else "off", meteor_fx.T_IMPACT]) if meteor_fx.mix4 and meteor_fx.burst_a != null and meteor_fx.crater4 != null else ("mix3(fall=lane_b_core,impact=lane_a,burn=crater,warp=post,ring=off,shadow=%s)" % ("on" if meteor_fx.shadow_on else "off")) if meteor_fx.mix3 and meteor_fx.burst_a != null and meteor_fx.crater != null else ("mix2(fall=lane_b_dark,impact=lane_a,burn=cinders,ring=off,rock_shadow=%s)" % ("on" if meteor_fx.shadow_on else "off")) if meteor_fx.mix2 and meteor_fx.burst_a != null else (("mix(fall=lane_a,impact=lane_b,ring=off,rock_shadow=%s)" % ("on" if meteor_fx.shadow_on else "off")) if meteor_fx.mix and meteor_fx.proj_a != null else "3d(lane_b)")) if meteor_fx != null else (_meteor_a_word() if spell_fx != null and spell_fx.meteor_a != null else "placeholder")]      # LANE B / LANE A


func _paint_launch_line() -> String:
	"""What the running scene READ, each file off its raw bytes in the pck with its sha256 checked
	against the manifest: the painting (the ground, the mound and the 28 primitives wear it), the
	light map, the 25 bakes (the real models' plates), the snow's grid."""
	var n: Dictionary = paint.get("pieces", {})
	var loads: Dictionary = paint.get("loads", {})
	var ok := func(rel: String) -> bool:
		var r: Dictionary = loads.get(rel, {})
		return bool(r.get("sha256_ok", false)) and not r.has("error")
	var bakes_ok := 0
	for k in loads:
		if String(k).begins_with("bakes/") and ok.call(String(k)):
			bakes_ok += 1
	var prim := int(n.get("primitives", 0)) + (1 if int(n.get("mound", 0)) > 0 else 0)
	return ("who=" + who + " slot=" + (slot if slot != "" else "own") + " " + "loaded_from_pck files_sha_ok=%d/%d painting_ok=%s ground=%s(%s)_ok=%s lit_ok=%s snow_grid_ok=%s "
		+ "| plates: bakes=%d/25 on the real models, painting on primitives=%d/29 (the mound + 28) "
		+ "| birches=%d inks_hidden=%d heather=%d snow=%s ms=%d") % [
		int(paint.get("files_ok", 0)), loads.size(), str(ok.call("painting.bin")),
		String(paint.get("ground_file", "?")), ground_variant, str(ok.call(String(paint.get("ground_file", "?")))),
		str(ok.call("lit.bin")), str(ok.call("snow_grid.bin")), bakes_ok, prim,
		int(n.get("birches", 0)), int(n.get("inks_hidden", 0)),
		int(paint.get("heather", {}).get("instances", 0)), str(snow != null), int(paint.get("ms", 0))]
