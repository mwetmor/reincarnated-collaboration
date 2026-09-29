extends Node3D
## C-9 T10 — THE FROST KING'S BARROW: the render stack, on a generated world, with him in it.
##
## Matt picked this world from the three concept paintings and asked for a FULLY GENERATED
## pipeline -- no Synty kit, nothing bought. So everything on screen here is either code
## (the terrain, the stones, the rocks, the birches, the noise, the paper, the flake, the
## sky) or the barbarian's own painted export. Nothing else.
##
## THIS SCENE IS NEW AND THE CLIFFSIDE SCENES ARE NOT TOUCHED. It shares the project, the
## character slot (data/character.json), knight.gd, gear.gd and the camera law, and it shares
## NOTHING with cliffside3d.tscn -- no plate, no canvas coordinates, no projector, no
## parallax layers. The cliffside works in CANVAS PIXELS on a 5376x4096 painting; the barrow
## works in METRES, because there is no painting to register against. What both must agree
## on is the CAMERA, and that agreement is asserted rather than assumed (see _build_camera).
##
## knight.gd AND gear.gd ARE UNTOUCHED, ON PURPOSE. A concurrent workstream is adding his
## armed motion set to both. Everything this scene does to him -- the watercolour ramp on his
## paint, the one pen on his hull line -- is done from OUTSIDE, by walking his public node
## tree in PaintStack.adopt_character. There is no hook in knight.gd and none is needed.
##
## KEYS: arrows/WASD move · Shift run · Space/click attack · G gear · [ ] size
##       V  the whole look stack off and on (the A/B)
##       N  the snow layer only
##       C  the falling snow and the ridge gust
##       K  the ink pass only

const PPM := 100.617553710938                  # px per metre across the screen, the project's own
const PL_PITCH_DEG := 52.95354112560294         # R-C9-68: the real angle, not a rounded 53
const PL_YAW_DEG := 47.0
const CHAR_LAYER := 4
const CAM_LIFT_PX := 55.0                       # he sits this far below frame centre, as the 2D route puts him
const SPAWN := Vector2(-7.2, 9.0)               # metres: in the basin's lip, looking up at the ring

# HOW FAR BACK THE ORTHOGRAPHIC CAMERA SITS, and why it is a named number rather than a
# large round one picked to be safely clear of everything.
#
# An orthographic camera's standoff does not change the picture: the projection has no
# perspective divide, so moving it back only moves what the near plane clips. The first
# version parked it 220 m back for exactly that reason. TWO THINGS ARE MEASURED FROM THE
# CAMERA AND BOTH WERE THEREFORE WRONG, silently:
#
#   DEPTH FOG. Every surface in the scene was ~219 m from the camera (measured,
#     tools/probe_terrain.gd), past fog_depth_end at 205 m, so the whole world rendered as
#     flat fog colour. This is the cliffside's own recorded defect from the opposite side --
#     "it was 200 m of haze over the whole plate" -- and it arrived here by a different route.
#   SHADOW CASCADES. directional_shadow_max_distance was 95 m against geometry at 219 m, so
#     NOTHING cast a shadow at all. Not a soft shadow, not a wrong shadow: none.
#
# So the standoff is as small as the geometry allows, and the fog and shadow distances are
# expressed as "ahead of the aim point" and added to it. The terrain's AABB half-extent
# along the view direction is 44.1 m (probe_terrain), so 60 m leaves ~16 m of clearance.
const CAM_STANDOFF := 60.0
const PLAY_M_PER_PX := 1.0 / PPM          # the play camera's metres per pixel, the ink's reference
const FOG_BEGIN_AHEAD := 8.0
const FOG_END_AHEAD := 105.0
const SHADOW_REACH_AHEAD := 50.0

var cam: Camera3D
var sun: DirectionalLight3D
var env_node: WorldEnvironment
var world                                       # BarrowStandIn, possibly delegating heights
var knight: CharacterBody3D

var right := Vector3.RIGHT
var up := Vector3.UP
var fwd := Vector3.FORWARD

var fbm: ImageTexture
var paper: ImageTexture
var flake: ImageTexture
var post_mat: ShaderMaterial
var post_q: MeshInstance3D
var _world_mats: Array[ShaderMaterial] = []
var _groups: Array = []
var _char_saved := {}
var snowfall: GPUParticles3D
var gust: GPUParticles3D

# THE WORLD WITHOUT HIM. Set before the node enters the tree. The stack's world side --
# ramp, snow, ink, fog, grade, paper -- does not depend on the character in any way, and
# knight.gd is owned by a concurrent workstream that will sometimes leave it un-parseable
# for a few minutes at a time. Being able to build, look at and measure the world half
# during those minutes is the difference between waiting and working.
@export var skip_character := false

# WHICH GROUND. "stand_in" is this seam's own procedural hill; the other two are the sibling
# drax's MEASURED barrow heightfields, which ship with an interface deliberately identical to
# BarrowStandIn's so the swap is one line and the comparison at the play camera is of the
# GROUND rather than of two different scenes.
#
# It defaults to the stand-in and that is not a preference. The render stack is what this
# session is answerable for, and it has to be measurable against a surface that does not
# change between runs; the heightfields were still being re-derived while this was written.
# The stack itself needs NO change either way -- every shader here reads world position and
# world normal off whatever geometry it is handed.
@export_enum("stand_in", "heightfield_authored", "heightfield_marigold")
var terrain_source := "stand_in"
var stack_on := true
var snow_on := true
var particles_on := true
var ink_on := true
var report := {}
var _hud: Label
var _size_step := 0
var _gust_t := 0.0


func _ready() -> void:
	world = BarrowStandIn.new()
	_build_camera()
	_build_light_and_air()
	_build_surfaces()
	_build_particles()
	if skip_character:
		var a := Vector3(SPAWN.x, world.height_at(SPAWN.x, SPAWN.y) + 1.2, SPAWN.y)
		look_at_world(a)
		snowfall.global_position = a + up * 9.0 - fwd * 6.0
	else:
		await _build_knight()
	_build_post()
	_build_hud()
	report["stand_in"] = world.report
	_apply_stack()


# --- the camera law -----------------------------------------------------------
func _build_camera() -> void:
	"""ONE CAMERA, and the same one. R-C9-68 fixed it: orthographic, pitch 52.95354112560294,
	yaw 47, and `size` in METRES OF SCREEN HEIGHT -- which is why it is divided by the ACTUAL
	viewport rows and not by a nominal 1080. A run whose window came back 972 rows tall once
	rendered the cliffside 10% small, silently.

	THE BASIS IS ASSERTED, NOT ASSUMED. knight.gd converts a canvas-space walk direction into
	a ground velocity using three facts about this frame: that `right` is horizontal, that
	`up` spends cos(pitch) of itself on the world vertical, and that the level-local +Z axis
	(sin 47, 0, cos 47) projects onto `up` at exactly -sin(pitch). If any of the three is
	false here, he walks at the wrong speed up-screen and nothing says so. They are checked
	below and the residuals go in the report."""
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
	cam.cull_mask = 0xFFFFF
	add_child(cam)
	cam.look_at_from_position(-f * CAM_STANDOFF, Vector3.ZERO, Vector3.UP)
	cam.current = true
	var b := cam.global_transform.basis
	right = b.x
	up = b.y
	fwd = -b.z
	var lz := Vector3(sin(y), 0.0, cos(y))
	report["camera"] = {
		"projection": "orthogonal",
		"pitch_deg": PL_PITCH_DEG,
		"yaw_deg": PL_YAW_DEG,
		"ortho_size_m": snappedf(cam.size, 0.0001),
		"viewport_rows": _view_height(),
		"px_per_m_screen_x": snappedf(PPM, 0.0001),
		"px_per_vertical_m": snappedf(PPM * cos(p), 0.0001),
		"px_per_ground_m_up_screen": snappedf(PPM * sin(p), 0.0001),
		"assert_right_is_horizontal": snappedf(absf(right.y), 1e-9),
		"assert_up_dot_worldup_minus_cos_pitch": snappedf(up.dot(Vector3.UP) - cos(p), 1e-9),
		"assert_levelZ_on_up_plus_sin_pitch": snappedf(-lz.dot(up) - sin(p), 1e-9),
		"assert_levelZ_perp_right": snappedf(lz.dot(right), 1e-9),
	}


func _view_height() -> int:
	var vp := get_viewport()
	var h: int = vp.get_visible_rect().size.y if vp != null else 1080
	return h if h > 0 else 1080


func look_at_world(aim: Vector3) -> void:
	cam.look_at_from_position(aim - fwd * CAM_STANDOFF, aim, Vector3.UP)


func _sync_post_scale() -> void:
	"""The ink pass's thresholds are in pixels and need the camera's metres-per-pixel to
	become metres. It changes whenever the zoom or the viewport does, so it is pushed here
	rather than read once at build -- a stale value is exactly how the threshold ends up
	right at one zoom and wrong at every other."""
	if post_mat != null and cam != null:
		post_mat.set_shader_parameter("m_per_px", cam.size / maxf(float(_view_height()), 1.0))


# --- rule 3: one real light, and the air around it ---------------------------
func _build_light_and_air() -> void:
	var lights := Node3D.new()
	lights.name = "Lights"
	add_child(lights)
	sun = PaintStack.winter_sun(17.0, 305.0)
	lights.add_child(sun)
	env_node = WorldEnvironment.new()
	env_node.name = "Env"
	# fog distances are VIEW distances, so they carry the camera's standoff; see CAM_STANDOFF
	env_node.environment = PaintStack.barrow_environment({
		"fog_depth_begin": CAM_STANDOFF + FOG_BEGIN_AHEAD,
		"fog_depth_end": CAM_STANDOFF + FOG_END_AHEAD,
	})
	sun.directional_shadow_max_distance = CAM_STANDOFF + SHADOW_REACH_AHEAD
	add_child(env_node)
	var sd := PaintStack.sun_screen_dir(sun, cam)
	var e := sun.global_transform.basis.z
	report["light"] = {
		"_one_light": "a single DirectionalLight3D; no fill, no rim, no per-object light",
		"elevation_deg": snappedf(rad_to_deg(asin(clampf(e.y, -1.0, 1.0))), 0.01),
		"colour_srgb": [sun.light_color.r, sun.light_color.g, sun.light_color.b],
		"energy": sun.light_energy,
		"shadows": sun.shadow_enabled,
		"shadow_blur": sun.shadow_blur,
		"screen_dir_from_sun": {"x_right": snappedf(sd.x, 0.001), "y_up": snappedf(sd.y, 0.001),
			"reads": "upper-left" if sd.x < 0.0 and sd.y > 0.0 else "NOT upper-left"},
		"ambient": {"colour": [env_node.environment.ambient_light_color.r,
							   env_node.environment.ambient_light_color.g,
							   env_node.environment.ambient_light_color.b],
					"energy": env_node.environment.ambient_light_energy,
					"_why": "blue sky ambient; also the floor under the shadow band, so nothing is black"},
		"fog": {"mode": "depth", "begin_m": env_node.environment.fog_depth_begin,
				"end_m": env_node.environment.fog_depth_end,
				"density": env_node.environment.fog_density,
				"height_m": env_node.environment.fog_height,
				"height_density": env_node.environment.fog_height_density,
				"colour": [env_node.environment.fog_light_color.r,
						   env_node.environment.fog_light_color.g,
						   env_node.environment.fog_light_color.b]},
	}


# --- the world's surfaces, all on the one shading model ----------------------
func _build_surfaces() -> void:
	# TIMED, because every texture in this scene is GENERATED IN GDSCRIPT AT LOAD and that is
	# cold-start cost Matt pays staring at a black window. If it grows past a second or two
	# the sizes come down or the generation moves to a thread; either way it has to be a
	# number before it can be a decision.
	var t0 := Time.get_ticks_msec()
	fbm = PaintStack.make_fbm_texture(512, 7411, 4)
	paper = PaintStack.make_paper_texture(512)
	flake = PaintStack.make_flake_texture(24)
	var t_tex := Time.get_ticks_msec() - t0
	# The mottle is DELIBERATELY FAINT on the ground. At amp 0.16 over 5 m features it read
	# as camouflage rather than snow -- large soft dark patches that the eye takes for dirt,
	# because a watercolour wash on snow varies in VALUE by a few percent, not by fifteen.
	var ground := PaintStack.world_material(fbm, Color(0.300, 0.268, 0.232), {
		"snow_threshold": 0.50, "snow_jitter": 0.34, "snow_soft": 0.15,
		"snow_noise_scale": 0.52, "mottle_scale": 0.14, "mottle_amp": 0.075,
		"hatch_scale": 3.1, "hatch_amp": 0.035, "wash_amp": 0.11,
	})
	var stone := PaintStack.world_material(fbm, Color(0.520, 0.512, 0.548), {
		"snow_threshold": 0.58, "snow_jitter": 0.26, "snow_soft": 0.10,
		"snow_noise_scale": 1.9, "mottle_scale": 1.5, "mottle_amp": 0.18,
		"hatch_scale": 9.0, "hatch_amp": 0.07,
	})
	var rock := PaintStack.world_material(fbm, Color(0.455, 0.435, 0.412), {
		"snow_threshold": 0.58, "snow_jitter": 0.30, "snow_soft": 0.11,
		"snow_noise_scale": 2.4, "mottle_scale": 2.2, "mottle_amp": 0.18,
		"hatch_scale": 11.0, "hatch_amp": 0.07,
	})
	var wood := PaintStack.world_material(fbm, Color(0.640, 0.625, 0.590), {
		"snow_threshold": 0.74, "snow_jitter": 0.20, "snow_soft": 0.08,
		"snow_noise_scale": 3.2, "mottle_scale": 5.0, "mottle_amp": 0.24,
		"hatch_scale": 22.0, "hatch_amp": 0.10,
	})
	_world_mats = [ground, stone, rock, wood]
	var t1 := Time.get_ticks_msec()
	var terr := _build_ground(ground)
	var props: Dictionary = world.build_props(self, stone, rock, wood)
	report["build_ms"] = {"generated_textures": t_tex,
						  "terrain_and_props": Time.get_ticks_msec() - t1,
						  "_all_procedural": "no purchased or downloaded asset is loaded here"}
	# grouped by MATERIAL, because that is what the snow measurement needs: each group's
	# threshold and jitter are its own, and a single averaged share over four different
	# parameter sets would be a number about nothing.
	var tree_meshes: Array = []
	for t in props["trees"]:
		for m in (t as Node3D).find_children("*", "MeshInstance3D", true, false):
			tree_meshes.append(m)
	_groups = [
		{"name": "terrain", "mat": ground, "meshes": [terr]},
		{"name": "standing_stones", "mat": stone, "meshes": props["stones"]},
		{"name": "rocks", "mat": rock, "meshes": props["rocks"]},
		{"name": "birches", "mat": wood, "meshes": tree_meshes},
	]
	_report_real_terrain()


func _build_ground(mat: Material) -> MeshInstance3D:
	"""The stand-in's surface, or the sibling's heightfield, drawn by whichever owns it --
	and in BOTH cases the props are placed through `world.height_at`, which delegates. A prop
	placed by one height function onto a surface drawn by another is a floating rock, and it
	is the kind of floating rock that gets read as a physics bug."""
	if terrain_source == "stand_in":
		report["terrain_source"] = {"kind": "stand_in", "_": "procedural, this seam's own"}
		return world.build_terrain(self, mat)
	var stem := "height_a_authored" if terrain_source == "heightfield_authored" else "height_a_marigold"
	var png := "res://data/%s.png" % stem
	var meta := "res://data/%s.json" % stem
	if not (FileAccess.file_exists(png) and FileAccess.file_exists(meta)
			and ResourceLoader.exists("res://scripts/barrow_heightfield.gd")):
		report["terrain_source"] = {"kind": "stand_in", "_fallback_from": terrain_source,
			"_why": "heightfield or its reader is not in the project"}
		return world.build_terrain(self, mat)
	var hf = load("res://scripts/barrow_heightfield.gd").new(png, meta)
	world.height_source = hf
	report["terrain_source"] = {"kind": terrain_source, "png": png,
		"reader_report": hf.report if "report" in hf else {}}
	return hf.build_terrain(self, mat)


func _report_real_terrain() -> void:
	"""THE SIBLING'S MEASURED BARROW GROUND: what is present, and what is in use.

	A sibling drax derived the barrow ground from the concept painting as a 16-bit
	heightfield PNG plus a JSON of what its levels mean, and shipped `barrow_heightfield.gd`
	with an interface DELIBERATELY identical to BarrowStandIn's -- height_at, normal_at,
	build_terrain, place_on_ground, the same TERRAIN_BIT, EXTENT and CELL -- so the swap is
	one line. `terrain_source` is that line. Two heightfields ship: `authored` (2.37 m of
	relief, nothing over 70 degrees) and `marigold` (4.00 m, derived by monocular depth).

	The stack itself needs NO change for either: every shader here reads world position and
	world normal off whatever geometry it is handed, and neither the ramp nor the snow layer
	nor the ink pass knows which heightfield it is standing on.
	"""
	var png := "res://data/height_a_marigold.png"
	var meta := "res://data/height_a_marigold.json"
	var reader := "res://scripts/barrow_heightfield.gd"
	report["real_terrain"] = {
		"heightfield_png_present": FileAccess.file_exists(png),
		"heightfield_meta_present": FileAccess.file_exists(meta),
		"reader_script_in_project": FileAccess.file_exists(reader),
		"selected": terrain_source,
		"in_use": false,
		"stack_changes_needed_to_adopt": "none -- the shaders read world position and world normal",
		"scene_changes_needed_to_adopt": "swap world.build_terrain(self, ground) for the reader, and source height_at from it",
	}


func _build_particles() -> void:
	var air := Node3D.new()
	air.name = "Air"
	add_child(air)
	snowfall = PaintStack.snowfall(flake, Vector3(46, 28, 46), 1700)
	air.add_child(snowfall)
	gust = PaintStack.ridge_gust(flake, 420)
	air.add_child(gust)
	# on the crest, where the ridge actually is, found from the height function rather than
	# eyeballed off a still
	var gx := 15.0
	var gz := -14.0
	gust.position = Vector3(gx, world.height_at(gx, gz) + 0.10, gz)
	gust.rotation = Vector3(0.0, deg_to_rad(-28.0), 0.0)


# --- him ----------------------------------------------------------------------
func _build_knight() -> void:
	var k: CharacterBody3D = preload("res://scripts/knight.gd").new()
	k.name = "Knight"
	# TRUE SCALE. 1.25178 exists because the painted cliffside draws a person larger than its
	# own metres; this world has no painting to match, so rule 5 applies unopposed and he is
	# 1.85 m among stones that are 3.5 m.
	k.setup(right, up, fwd, 1.0)
	add_child(k)
	knight = k
	await get_tree().physics_frame
	k.set_figure_scale(1.0)
	k.global_position = Vector3(SPAWN.x, world.height_at(SPAWN.x, SPAWN.y) + 0.03, SPAWN.y)
	k.facing = "NE"
	var steps: Array = k.cfg.get("scale_steps", [])
	for i in steps.size():
		if absf(float(steps[i]) - 1.0) < 1e-6:
			_size_step = i
	# HIS PAINT UNDER THE SAME RAMP, done from outside knight.gd.
	_char_saved = PaintStack.adopt_character(k, fbm, PaintStack.INK, {
		"wash_scale": 2.6, "wash_amp": 0.13, "band_soft": 0.075,
	})
	report["character"] = {
		"model": String(k.cfg.get("model", "?")),
		"figure_scale": 1.0,
		"height_m": k.cfg.get("model_height_m", 1.85),
		"meshes_under_ramp": (_char_saved.get("meshes", []) as Array).size(),
		"hull_ink_meshes_retinted": (_char_saved.get("inks", []) as Array).size(),
		"_ramp_note": "the SAME light() as the world; only the albedo source differs",
	}
	look_at_world(_aim_for(k.global_position))


func _aim_for(pos: Vector3) -> Vector3:
	return pos + up * (CAM_LIFT_PX / PPM)


# --- the screen-space pass ----------------------------------------------------
func _build_post() -> void:
	post_mat = PaintStack.post_material(paper, PaintStack.INK, {
		"line_px": 1.25,
		"depth_edge_px": 3.4,
		"normal_edge": 0.60,
		"normal_weight": 0.85,
		"ink_gain": 1.15,
		"ref_m_per_px": PLAY_M_PER_PX,
	})
	_sync_post_scale()
	post_q = PaintStack.post_quad(cam, post_mat)
	report["ink"] = {
		"one_pen": {"colour_srgb": [PaintStack.INK.r, PaintStack.INK.g, PaintStack.INK.b],
					"hex": "#%02X%02X%02X" % [int(round(PaintStack.INK.r * 255.0)),
											  int(round(PaintStack.INK.g * 255.0)),
											  int(round(PaintStack.INK.b * 255.0))]},
		"screen_space": {"operator": "Roberts cross on linear depth and the view-space normal buffer",
						 "line_px": 1.25, "depth_edge_m": 0.055, "normal_edge": 0.60},
		"hull": "kept on the character and RE-ISSUED in the same colour with fog_disabled, so the two lines are one pen",
	}


# --- the A/B ------------------------------------------------------------------
func _apply_stack() -> void:
	"""V. What the stack IS, in one place: the ramp, the ink, the grade and the paper. Snow
	and the falling flakes have their OWN keys, because turning them off changes what the
	world is made of rather than how it is lit, and folding them into the A/B would make the
	comparison answer two questions at once."""
	for m in _world_mats:
		m.set_shader_parameter("ramp_mix", 1.0 if stack_on else 0.0)
	PaintStack.set_character_ramp(_char_saved, stack_on)
	post_mat.set_shader_parameter("ink_on", 1.0 if (stack_on and ink_on) else 0.0)
	post_mat.set_shader_parameter("grade_on", 1.0 if stack_on else 0.0)
	# HIDDEN, not merely neutralised. With the stack off the pass would still copy the screen
	# and blit it back -- invisible, and about a millisecond of it. Leaving it running would
	# put that millisecond into the "stack off" side of the frame-cost comparison, so the
	# measured cost OF THE STACK would be short by exactly the amount the stack costs.
	if post_q != null:
		post_q.visible = stack_on
	var env := env_node.environment
	env.fog_enabled = stack_on
	_update_hud()


func set_stack(on: bool) -> void:
	stack_on = on
	_apply_stack()


func set_snow(on: bool) -> void:
	snow_on = on
	for m in _world_mats:
		m.set_shader_parameter("snow_amount", 1.0 if on else 0.0)
	_update_hud()


func set_particles(on: bool) -> void:
	particles_on = on
	snowfall.emitting = on
	gust.emitting = on
	snowfall.visible = on
	gust.visible = on
	_update_hud()


func set_ink(on: bool) -> void:
	ink_on = on
	post_mat.set_shader_parameter("ink_on", 1.0 if (stack_on and on) else 0.0)
	_update_hud()


func set_post_param(key: String, value) -> void:
	post_mat.set_shader_parameter(key, value)


func set_world_param(key: String, value) -> void:
	for m in _world_mats:
		m.set_shader_parameter(key, value)


func step_size(d: int) -> void:
	if knight == null:
		return
	var steps: Array = knight.cfg.get("scale_steps", [])
	if steps.is_empty():
		return
	_size_step = clampi(_size_step + d, 0, steps.size() - 1)
	knight.set_figure_scale(float(steps[_size_step]))
	# the hull line's width was just recomputed by knight.gd into ITS OWN shader parameter
	# name, which this scene's re-issued material shares, so nothing else is needed here --
	# but the material is a different instance, so the value has to be carried across.
	_resync_ink_width()
	_update_hud()


func _resync_ink_width() -> void:
	"""knight.gd's set_figure_scale writes `width_model` on whatever material is on the
	outline mesh. Since this scene REPLACED that material with its own instance, the write
	lands on this instance -- the parameter name is identical -- and nothing is lost. Checked
	rather than trusted: the widths are reported so a size step that silently stopped
	updating the line shows up as a frozen number."""
	var w := []
	for e in _char_saved.get("inks", []):
		var m := ((e["mi"]) as MeshInstance3D).material_override as ShaderMaterial
		if m != null:
			var v = m.get_shader_parameter("width_model")
			w.append(snappedf(float(v), 1e-6) if v != null else -1.0)
	report["ink_width_model_now"] = w


# --- play ---------------------------------------------------------------------
func _process(dt: float) -> void:
	if knight == null:
		return
	look_at_world(_aim_for(knight.global_position))
	# the emission box travels with the view, or half the snow falls off screen
	snowfall.global_position = knight.global_position + up * 9.0 - fwd * 6.0
	# the gust, pulsed: a gust is an event, and a constant fountain is not one
	_gust_t += dt
	var pulse: float = maxf(0.0, sin(_gust_t * 0.42) - 0.45) / 0.55
	gust.amount_ratio = clampf(pulse, 0.0, 1.0) if particles_on else 0.0
	_update_hud()


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
	_hud.text = ("WASD move · Shift run · Space attack · G gear (%d/%d: %s) · [ ] size (%.2f)"
		+ "   ‖   V stack (%s) · K ink (%s) · N snow (%s) · C air (%s)") \
		% [n + 1, total, nm, fs, "ON" if stack_on else "OFF", "on" if ink_on else "off",
		   "on" if snow_on else "off", "on" if particles_on else "off"]


# --- what the capture tool needs -----------------------------------------------
# All of it small, all of it here rather than reached into from tools/, so a later session
# changing the scene can see what the measurements depend on.
func park_camera(aim: Vector3, zoom := 1.0) -> void:
	"""Stop following him and hold one frame. A measurement taken while the camera is easing
	toward a target measures the ease."""
	set_process(false)
	cam.size = (float(_view_height()) / PPM) / maxf(zoom, 1e-3)
	_sync_post_scale()
	look_at_world(aim)
	if snowfall != null:
		snowfall.global_position = aim + up * 9.0 - fwd * 6.0


func unpark_camera() -> void:
	cam.size = float(_view_height()) / PPM
	_sync_post_scale()
	set_process(true)


func set_hud_visible(on: bool) -> void:
	var l := get_node_or_null(^"HUD") as CanvasLayer
	if l != null:
		l.visible = on


func set_hull_ink_visible(on: bool) -> void:
	"""Hide the character's HULL pen alone, leaving the screen-space pen and everything else
	untouched. Differencing a frame against this one is how the hull line's delivered colour
	is isolated for the ΔE against the screen-space line -- each pen measured by the pixels
	it actually painted, rather than by guessing which dark pixels belong to which pass."""
	for e in _char_saved.get("inks", []):
		((e["mi"]) as MeshInstance3D).visible = on


func freeze_pose(on: bool) -> void:
	"""Stop the skeleton advancing between captures.

	set_physics_process(false) stops the CONTROLLER, not the AnimationTree: the tree runs on
	its own callback and keeps stepping the idle, so he moves a few pixels between two
	consecutive shots. Every measurement in this run is a SUBTRACTION OF TWO FRAMES, and a
	few pixels of drift is not noise there -- it turns his entire silhouette into "changed",
	which inflated the hull line's measured width and left real ink pixels outside the ink
	mask, so the frame's darkest pixel came back as ink that the mask had not caught.
	Reached from outside; knight.gd is untouched."""
	var mode := AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL if on \
		else AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS
	for n in knight.find_children("*", "AnimationMixer", true, false):
		(n as AnimationMixer).callback_mode_process = mode


func set_pens(on: bool) -> void:
	"""BOTH pens off together, in delivered conditions (grade and paper still on). The pair
	stack_on / pens_off is what the ink mask must come from: the ink is the darkest thing in
	the frame BY DESIGN, so a min-luma test that has not excluded exactly those pixels is
	measuring the pen and calling it a shadow."""
	set_ink(on)
	set_hull_ink_visible(on)


func set_grade(on: bool) -> void:
	post_mat.set_shader_parameter("grade_on", 1.0 if on else 0.0)


func set_ramp_on_character(on: bool) -> void:
	PaintStack.set_character_ramp(_char_saved, on)


func use_original_character_materials(on: bool) -> void:
	"""His materials exactly as knight.gd built them -- the third state, and the real
	"before". See PaintStack.restore_character for why ramp_mix = 0 is not the same thing."""
	if on:
		PaintStack.restore_character(_char_saved)
	else:
		PaintStack.reapply_character(_char_saved, PaintStack.INK)


func set_ramp_on_world(on: bool) -> void:
	for m in _world_mats:
		m.set_shader_parameter("ramp_mix", 1.0 if on else 0.0)


func set_fog(on: bool) -> void:
	env_node.environment.fog_enabled = on


func place_knight(x: float, z: float, facing := "NE") -> void:
	knight.global_position = Vector3(x, world.height_at(x, z) + 0.03, z)
	knight.velocity = Vector3.ZERO
	knight.facing = facing
	knight._drive()


func snow_report() -> Dictionary:
	return PaintStack.measure_snow(_groups, fbm.get_image(), 0.5)


func character_screen_rect() -> Rect2:
	"""Where he is on screen, from his own bones rather than from a silhouette difference --
	a difference also catches the shadow he throws, which is how T9 once measured a 104 px man
	at 195 px."""
	var lo := Vector2(1e9, 1e9)
	var hi := Vector2(-1e9, -1e9)
	for n in knight.find_children("*", "Skeleton3D", true, false):
		var sk := n as Skeleton3D
		for b in sk.get_bone_count():
			var p := cam.unproject_position(sk.global_transform * sk.get_bone_global_pose(b).origin)
			lo = lo.min(p)
			hi = hi.max(p)
	return Rect2(lo, hi - lo)


func _unhandled_input(e: InputEvent) -> void:
	if e.is_action_pressed("gear_cycle") and knight != null:
		knight.cycle_gear()
		_update_hud()
	elif e.is_action_pressed("size_down"):
		step_size(-1)
	elif e.is_action_pressed("size_up"):
		step_size(1)
	elif e is InputEventKey and (e as InputEventKey).pressed and not (e as InputEventKey).echo:
		# V, N, C and K are read as RAW KEYS rather than added to project.godot's [input]
		# map. project.godot is shared with the cliffside scenes and a concurrent workstream;
		# an additive edit there is small but it is not zero, and this costs nothing.
		match (e as InputEventKey).physical_keycode:
			KEY_V: set_stack(not stack_on)
			KEY_N: set_snow(not snow_on)
			KEY_C: set_particles(not particles_on)
			KEY_K: set_ink(not ink_on)
