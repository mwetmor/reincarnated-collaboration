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
## KEYS: arrows/WASD move · Shift run · Space slash · X chop · C bash · B/RMB block · G gear · [ ] size
##       V  the whole look stack off and on (the A/B)
##       N  the snow layer only
##       J  the falling snow and the ridge gust
##       K  the ink pass only
##
## The MARIGOLD ground stays reachable through the `terrain_source` export on this node --
## the toggle it shipped with. It is not on a key: swapping the ground rebuilds the terrain
## mesh AND all 70 placements (they are emitted per frame and the two frames differ by
## (0.45, 0.36) m), so a key that did it would be a two-second freeze pretending to be a view
## option, and a key that did half of it would be silently wrong.
##
## THE FOUR LOOK KEYS ARE V N J K AND THE CHOICE IS MEASURED, not picked. _check_key_collisions
## reads the live InputMap; the run that chose these is in the report as `key_collisions`.
## `C` was the air toggle and became `shield_bash` when the armed motion set landed -- one
## press hid the snow AND swung the shield. `M` was its replacement and collides with Godot's
## own `ui_focus_mode`; `J` does not collide with anything, modified or not.

const PPM := 100.617553710938                  # px per metre across the screen, the project's own
const PL_PITCH_DEG := 52.95354112560294         # R-C9-68: the real angle, not a rounded 53
const PL_YAW_DEG := 47.0
const CHAR_LAYER := 4
const CAM_LIFT_PX := 55.0                       # he sits this far below frame centre, as the 2D route puts him
# WHERE HE STANDS, IN THE PAINTED 15 m AND NOT BESIDE IT. The old spawn (-7.2, 9.0) was a
# landmark of the stand-in's basin; on the measured ground the concept square runs x -4.43
# to 10.57 and z -7.56 to 7.44, so that point is off the painting entirely -- he would have
# started on blank relaxed moor with the whole barrow behind the camera. (5.6, 1.6) is about
# 7 m downhill of the mound at (0, -4), which puts the door, the ring and the tarn up-screen:
# the frame reaches ~6.7 m along (-0.73, -0.68) from him at the play zoom.
const SPAWN := Vector2(4.2, -0.3)

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
# HOW FAR ABOVE THE FLOOR THE MIST TOPS OUT. 1.15 m was tuned against a hollow the player
# walked down INTO -- the mist filled the low ground and the mound stood out of it. On a flat
# floor (R-C9-74) there is no low ground, so 1.15 m put every surface in the scene inside the
# fog and the whole frame came back milky: measured on look_play, the delivered frame's mean
# luma was up and the tiles that this pass exists to show were washing out under it.
# 0.55 m is a mist he wades in rather than one he is inside: his boots and the rocks' feet
# take it, his head and the standing stones do not.
const BASIN_MIST_M := 0.55

# --- T10: the real barrow ------------------------------------------------------
const SCENE_JSON := "res://data/barrow_scene_a.json"
const ASSETS_JSON := "res://data/barrow_assets.json"
const SPLAT_PNG := "res://data/splat_ids_a_marigold.png"
const TILE_DIR := "res://textures/barrow/"
# THE SPLAT CLASS ORDER, in one place. T10_HANDOFF states it as snow->0 path->1 rock->2
# heather->3 ice->4; barrow_heightfield's own JSON calls class 3 "grass". Same class, two
# names, and the tile file is heather.png -- so the list below is the only order this scene
# uses and everything else indexes through it.
const SPLAT_CLASSES := ["snow", "path", "rock", "heather", "ice"]
# METRES PER TILE REPEAT. Chosen off the tiles' own feature scale, not off a round number:
# rock's crack polygons are ~150 px and a granite slab is ~0.35 m; heather's sprigs are ~90 px
# and a sprig is ~0.22 m; ice's plates are ~180 px and a tarn plate ~0.45 m. All three put
# 1024 px at 2.3-2.6 m, so 2.5 m, which also means a tile spans a quarter of the barbarian's
# stride and can be checked against him in the frame.
const TILE_M := 2.5
const SPLAT_BLUR_PX := 7          # 0.35 m of soft border at the splat's 0.05 m/px
const HULL_PX := 1.1              # the character's own outline_px; the props get the same pen
# THE SUN, RAISED (R-C9-74 note 3). 17 degrees threw shadows 3.27x their caster's height; 55
# throws them at 1/tan(55) = 0.700x, under the 0.8x the ruling asks for. The azimuth is kept:
# at 55 degrees his own shadow falls 1.30 m from his feet toward screen lower-right, clear of
# his figure, so there is no reason to move it and one change at a time is the rule.
const SUN_ELEV_DEG := 55.0
const SUN_SCREEN_AZ_DEG := 305.0
# How far a prop is pushed into the ground below its LOWEST footprint sample. Small and not
# zero: the terrain is faceted at 0.55 m quads, so a base sitting exactly on the sampled
# height still shows daylight under one corner when the quad tilts between samples.
const PROP_SINK_M := 0.02

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

var _hf = null                     # BarrowHeightfield, when a measured ground is selected
var _flat = null                   # BarrowFlat, the R-C9-74 default
var _mound: MeshInstance3D
var _tiles := {}                   # splat-class name -> ImageTexture
var _splat: ImageTexture
var _splat_img: Image              # the CPU copy, for the snow measurement's keep factor
var _splat_origin := Vector2.ZERO  # world xz of the splat's (0,0) corner
var _splat_size := Vector2(15.0, 15.0)
var _ground_mat: ShaderMaterial
var _props_root: Node3D
var _prop_inks: Array = []         # every prop hull-pen mesh, for the capture's isolation
var _scene_list := []
var _tallest_stone: Node3D
var _place_report := {}

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
#
# DEFAULT IS FLAT, per R-C9-74. Matt, on the 15:20 build: "The hills are probably not great
# for gameplay as they may confuse combat. I would stay away from non-flat ground other than
# the occasional stairway/etc."
#
# The authored heightfield WAS the default for about an hour of this session and the swap
# cost one line, which is the whole point of the three grounds sharing an interface. What did
# NOT come for free is everything the relief was carrying: the barrow mound, the rock
# outcrops and the tarn were all terrain, and on a flat floor they have to be structures and
# props. See _build_mound and _surface_y -- the props still stand on the mound, the PLAYER
# does not.
#
# All three of the others stay selectable. `heightfield_authored` is the ground the 70
# placements were emitted for and the one this pass measured first; it is one export away.
@export_enum("flat", "stand_in", "heightfield_authored", "heightfield_marigold")
var terrain_source := "flat"
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
	# THE GROUND IS CHOSEN BEFORE THE AIR, and the order is the fix for a real defect rather
	# than tidiness. The fog's height is read FROM the terrain (see _build_light_and_air), and
	# the heightfield used to be attached inside _build_surfaces -- which runs after. So the
	# mist level came off the STAND-IN's hill while the frame showed the measured barrow, and
	# the two differ by 1.4 m at the hollow. It returned a number, the number was plausible,
	# and it was a number about a surface that was no longer in the scene.
	_select_ground()
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
	_check_key_collisions()
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
	sun = PaintStack.winter_sun(SUN_ELEV_DEG, SUN_SCREEN_AZ_DEG)
	lights.add_child(sun)
	env_node = WorldEnvironment.new()
	env_node.name = "Env"
	# HEIGHT FOG ONLY, AND ITS HEIGHT IS THE HOLLOW'S OWN. The mist has to sit in the hollow
	# the player can walk down into, so the level is read from the terrain rather than picked
	# -- a hand-picked world Y stops being the hollow's rim the moment the ground changes.
	#
	# READ FROM THE GROUND IN USE, AND NOT FROM A NAMED POINT. The first version sampled
	# BarrowStandIn.BASIN_CENTRE, which is a landmark of the PROCEDURAL hill and means nothing
	# on the measured heightfield -- the authored barrow's low ground is its tarn, 11 m away
	# from where the stand-in's basin is. So the floor is the 10th percentile of the ground
	# over the concept's own 15 m square, sampled on a 48x48 grid: the level most of the low
	# ground actually sits at, on whichever surface is loaded, with no landmark to go stale.
	var floor_m := _hollow_floor()
	env_node.environment = PaintStack.barrow_environment({
		"fog_height": floor_m + BASIN_MIST_M,
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
		"shadow": {"bias": sun.shadow_bias, "normal_bias": sun.shadow_normal_bias,
				   "blur": sun.shadow_blur,
				   "length_per_caster_height": snappedf(1.0 / tan(deg_to_rad(SUN_ELEV_DEG)), 0.001),
				   "_bias_sweep": "tools/probe_shadow.gd -- no measurable acne at any normal_bias 0.0..3.0 on the mound",
				   "_requirement": "<= 0.8 x the caster's height (R-C9-74)",
				   "was_at_17_deg": snappedf(1.0 / tan(deg_to_rad(17.0)), 0.001)},
		"ambient": {"colour": [env_node.environment.ambient_light_color.r,
							   env_node.environment.ambient_light_color.g,
							   env_node.environment.ambient_light_color.b],
					"energy": env_node.environment.ambient_light_energy,
					"_why": "blue sky ambient; also the floor under the shadow band, so nothing is black"},
		"fog": {"mode": "exponential, HEIGHT TERM ONLY",
				"distance_density": env_node.environment.fog_density,
				"_distance_off_because": "it changed 0.0% of the play frame; the frame is 13 m deep",
				"height_world_y": snappedf(env_node.environment.fog_height, 0.01),
				"height_density": env_node.environment.fog_height_density,
				"hollow_floor_y": snappedf(floor_m, 0.01),
				"_hollow_floor_from": "p10 of the ground in use over the concept's 15 m square, 48x48 samples",
				"colour": [env_node.environment.fog_light_color.r,
						   env_node.environment.fog_light_color.g,
						   env_node.environment.fog_light_color.b]},
	}


# --- which ground, chosen before anything reads it ---------------------------
func _select_ground() -> void:
	"""Attach the measured heightfield to `world` so EVERY height_at in this scene -- the
	fog's, the props', his spawn, the gust's -- comes off the surface that is actually drawn.

	The fallback is loud on purpose. A missing heightfield used to fall back to the stand-in
	with one line in a JSON nobody opens, which is a scene that looks finished and is showing
	a different world from the one its props were placed for."""
	if terrain_source == "flat":
		_flat = BarrowFlat.new()
		world.height_source = _flat
		report["terrain_source"] = {"kind": "flat", "stem": "height_a_authored",
			"_": "R-C9-74: one flat walkable level. The stem is the FRAME the 70 placements "
				+ "are read from -- their xz is unchanged by the floor being flat, and using "
				+ "the marigold list here would move every prop by (0.45, 0.36) m."}
		print("[barrow] ground=flat")
		return
	if terrain_source == "stand_in":
		report["terrain_source"] = {"kind": "stand_in", "_": "procedural, this seam's own"}
		return
	var stem := "height_a_authored" if terrain_source == "heightfield_authored" else "height_a_marigold"
	var png := "res://data/%s.png" % stem
	var meta := "res://data/%s.json" % stem
	if not (FileAccess.file_exists(png) and FileAccess.file_exists(meta)
			and ResourceLoader.exists("res://scripts/barrow_heightfield.gd")):
		push_warning("barrow: %s missing; FALLING BACK TO THE STAND-IN GROUND" % png)
		report["terrain_source"] = {"kind": "stand_in", "_fallback_from": terrain_source,
			"_why": "heightfield or its reader is not in the project"}
		return
	_hf = load("res://scripts/barrow_heightfield.gd").new(png, meta)
	world.height_source = _hf
	report["terrain_source"] = {"kind": terrain_source, "png": png, "stem": stem,
		"reader_report": _hf.report if "report" in _hf else {}}
	# ONE LINE ON STDOUT, because this is the fact the exported .app has to be checked for.
	# The pck fence in build_app_barrow.sh proves the FILE shipped; only the running app can
	# say the file was read, and a launch probe can grep for this.
	print("[barrow] ground=%s" % terrain_source)


func _hollow_floor() -> float:
	"""The level the low ground sits at, on whichever surface is loaded: the 10th percentile
	of the height over the concept's own 15 m square. A minimum would follow one pothole; a
	mean would sit above the tarn it is supposed to fill."""
	var c := _concept_centre()
	var hs := PackedFloat32Array()
	for j in 48:
		for i in 48:
			var x: float = c.x + (float(i) / 47.0 - 0.5) * _splat_size.x
			var z: float = c.y + (float(j) / 47.0 - 0.5) * _splat_size.y
			hs.append(world.height_at(x, z))
	var a := Array(hs)
	a.sort()
	return float(a[int(float(a.size()) * 0.10)])


func _concept_centre() -> Vector2:
	"""Where the painted 15 m square sits in scene metres. From the frame block of
	barrow_scene_a.json when it is readable, because that file's `scene_offset_xz` IS the
	transform the 70 instances were emitted through -- deriving it a second way here is how
	the ground and the props end up half a metre apart."""
	return _splat_origin + _splat_size * 0.5


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
	var t_tile := Time.get_ticks_msec()
	_load_ground_textures()
	t_tile = Time.get_ticks_msec() - t_tile

	# THE GROUND'S SNOW PARAMETERS ARE UNCHANGED AND ITS COVERAGE IS NOT. At threshold 0.50
	# with jitter 0.34, every up-facing triangle in the scene came back covered -- the whole
	# frame was a white desert and the tiles underneath it would have been invisible. The
	# layer is kept exactly as tuned and scaled per splat class in the shader instead, so
	# `N` still turns the same drift on and off and the classes still read through it.
	var ground := PaintStack.ground_material(fbm, _tiles, _splat, {
		"snow_threshold": 0.50, "snow_jitter": 0.34, "snow_soft": 0.15,
		"snow_noise_scale": 0.52, "mottle_scale": 0.14, "mottle_amp": 0.075,
		"hatch_scale": 3.1, "hatch_amp": 0.035, "wash_amp": 0.11,
		"tile_m": TILE_M, "detile_mix": 0.35,
		"splat_origin": _splat_origin, "splat_size": _splat_size, "splat_relax_m": 6.0,
		"snow_keep_snow": 1.0,
		"snow_keep_path_rock_heather_ice": Vector4(0.45, 0.30, 0.22, 0.25),
	})
	_ground_mat = ground
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
	# THE MOUND WEARS THE GROUND'S OWN MATERIAL, so it takes the splat class that the painting
	# assigns to the barrow's footprint and the same snow layer as the floor around it. One
	# material, one tile scale, one drift: a mound with its own material would be a second
	# ground pretending to be a structure.
	if _flat != null:
		_mound = _build_mound(ground)
	var t_terr := Time.get_ticks_msec() - t1

	# THE REAL BARROW, OR THE STAND-IN'S HILL -- never a mixture. The 70 placements were
	# emitted against a NAMED ground; using them on the other one puts every prop half a
	# metre off its own footprint (T10_HANDOFF, the two grids' origins differ by 0.45, 0.36 m).
	var t2 := Time.get_ticks_msec()
	var groups: Array = []
	if (_hf != null or _flat != null) and FileAccess.file_exists(SCENE_JSON):
		groups = _build_scene_props(stone, rock, wood)
	else:
		var props: Dictionary = world.build_props(self, stone, rock, wood)
		var tree_meshes: Array = []
		for t in props["trees"]:
			for m in (t as Node3D).find_children("*", "MeshInstance3D", true, false):
				tree_meshes.append(m)
		groups = [
			{"name": "standing_stones", "mat": stone, "meshes": props["stones"]},
			{"name": "rocks", "mat": rock, "meshes": props["rocks"]},
			{"name": "birches", "mat": wood, "meshes": tree_meshes},
		]
		report["props"] = {"source": "stand_in procedural"}
	report["build_ms"] = {"generated_textures": t_tex, "ground_tiles_and_splat": t_tile,
						  "terrain_mesh": t_terr,
						  "props": Time.get_ticks_msec() - t2,
						  "_all_procedural": "no purchased or downloaded asset is loaded here"}
	# grouped by MATERIAL, because that is what the snow measurement needs: each group's
	# threshold and jitter are its own, and a single averaged share over four different
	# parameter sets would be a number about nothing. The terrain also carries the per-class
	# `keep` factor, as a Callable, so the CPU measures what the GPU draws.
	var terr_meshes: Array = [terr]
	if _mound != null:
		terr_meshes.append(_mound)
	_groups = [{"name": "terrain", "mat": ground, "meshes": terr_meshes,
				"amount_scale": Callable(self, "snow_keep_at")}]
	_groups.append_array(groups)


func _load_ground_textures() -> void:
	"""The six tiles and the splat, off real files rather than through the importer.

	The splat's world placement comes from barrow_scene_a.json's OWN frame block -- the same
	`scene_offset_xz` the 70 instances were emitted through. Derived a second way here it
	would be 0.45 m out for the authored frame and nothing would say so; the instances would
	sit half a metre off the ground classes they were classified from."""
	var missing := []
	for c in SPLAT_CLASSES:
		var p: String = TILE_DIR + c + ".png"
		if not FileAccess.file_exists(p):
			missing.append(p)
			continue
		_tiles[c] = PaintStack.load_tile(p)
	var stem := "height_a_authored" if terrain_source != "heightfield_marigold" else "height_a_marigold"
	var frame := {}
	if FileAccess.file_exists(SCENE_JSON):
		var sj = JSON.parse_string(FileAccess.get_file_as_string(SCENE_JSON))
		if typeof(sj) == TYPE_DICTIONARY:
			_scene_list = sj.get("instances", {}).get(stem, [])
			frame = sj.get("frames", {}).get(stem, {})
	if frame.has("scene_offset_xz"):
		_splat_origin = Vector2(float(frame["scene_offset_xz"][0]), float(frame["scene_offset_xz"][1]))
	var splat := {}
	if FileAccess.file_exists(SPLAT_PNG):
		# SNOW IS THE IMPLIED CLASS. See PaintStack.splat_weight_texture: four 8-bit channels
		# put all their rounding error on the fifth, and snow is the one already near 1.
		splat = PaintStack.splat_weight_texture(SPLAT_PNG, SPLAT_CLASSES.size(), SPLAT_BLUR_PX, 0)
		_splat = splat.get("tex")
		if _splat != null:
			_splat_img = _splat.get_image()
	else:
		missing.append(SPLAT_PNG)
	report["ground_textures"] = {
		"tiles": _tiles.keys(), "missing": missing,
		"tile_m": TILE_M,
		"_tile_m_why": "1024 px over 2.5 m = 410 px/m; the tiles' own features (rock slab 0.35 m, heather sprig 0.22 m, ice plate 0.45 m) all put 1024 px at 2.3-2.6 m",
		"mipmaps": "generated at load; the shipped .import files are all mipmaps/generate=false",
		"splat": splat.get("report", {}),
		"splat_origin_xz": [_splat_origin.x, _splat_origin.y],
		"splat_size_m": [_splat_size.x, _splat_size.y],
		"_splat_origin_from": "barrow_scene_a.json frames.%s.scene_offset_xz -- the same transform the 70 instances were emitted through" % stem,
		"scene_list_instances": _scene_list.size(),
	}


func splat_keep_at(x: float, z: float) -> float:
	"""How much of the world-space drift the ground holds at (x, z): the shader's `keep`, on
	the CPU, off the same blurred weight image the GPU samples. Used by the snow measurement
	and by nothing else -- so there is one splat lookup in this scene, not two."""
	if _splat_img == null:
		return 1.0
	var u: float = (x - _splat_origin.x) / maxf(_splat_size.x, 1e-6)
	var v: float = (z - _splat_origin.y) / maxf(_splat_size.y, 1e-6)
	var dx: float = maxf(maxf(-u, u - 1.0), 0.0) * _splat_size.x
	var dz: float = maxf(maxf(-v, v - 1.0), 0.0) * _splat_size.y
	var t: float = clampf(sqrt(dx * dx + dz * dz) / 6.0, 0.0, 1.0)
	t = t * t * (3.0 - 2.0 * t)
	var px: int = clampi(int(clampf(u, 0.0, 1.0) * float(_splat_img.get_width() - 1)), 0,
						 _splat_img.get_width() - 1)
	var pz: int = clampi(int(clampf(v, 0.0, 1.0) * float(_splat_img.get_height() - 1)), 0,
						 _splat_img.get_height() - 1)
	var c := _splat_img.get_pixel(px, pz)
	var w_snow: float = clampf(1.0 - (c.r + c.g + c.b + c.a), 0.0, 1.0)
	var w0: float = lerpf(w_snow, 1.0, t)
	var f: float = 1.0 - t
	var keeps := Vector4(0.45, 0.30, 0.22, 0.25)
	var num: float = 1.0 * w0 + keeps.x * c.r * f + keeps.y * c.g * f + keeps.z * c.b * f \
		+ keeps.w * c.a * f
	var den: float = maxf(w0 + (c.r + c.g + c.b + c.a) * f, 1e-4)
	return num / den


func snow_keep_at(p: Vector3) -> float:
	return splat_keep_at(p.x, p.z)


func _build_ground(mat: Material) -> MeshInstance3D:
	"""The stand-in's surface, or the measured heightfield, drawn by whichever owns it -- and
	in BOTH cases the props are placed through `world.height_at`, which delegates. A prop
	placed by one height function onto a surface drawn by another is a floating rock, and it
	is the kind of floating rock that gets read as a physics bug."""
	if _flat != null:
		return _flat.build_terrain(self, mat)
	if _hf != null:
		return _hf.build_terrain(self, mat)
	return world.build_terrain(self, mat)




# --- the barrow itself, now that the floor is flat ---------------------------
# R-C9-74: "The barrow mound becomes a non-walkable structure at the edge, with its door at
# floor level." On the heightfield the mound was 1.70 m of terrain at scene (0, -4) and the
# player could walk over it. Here it is a MESH ON the floor with its own collision, and the
# floor under it stays at y = 0.
#
# The geometry is the authored heightfield's own numbers -- centre (0, -4), radius 2.6 m,
# rise 1.70 m, straight out of height_a_authored.json's `mound` block -- with one thing
# added: an ENTRANCE PASSAGE cut from the rim to the centre along the door's own bearing.
# Without it the lintel at (1.779, -3.512) sits 1.84 m from the centre, which is 1.20 m up
# the dome, and the door frame is buried to its shoulders in the mound it is the door of.
const MOUND_XZ := Vector2(0.0, -4.0)
const MOUND_R := 2.6
const MOUND_RISE := 1.70
const MOUND_CELL := 0.12
const PASSAGE_HALF_W := 1.10
const PASSAGE_SOFT := 0.35
const WALL_SEGMENTS := 16          # the blocking wall, as boxes, with the passage left open


var _door_dir_cache := Vector2.ZERO


func _door_dir() -> Vector2:
	"""The door's bearing from the mound's centre, from the LINTEL's own placement rather
	than from a constant -- the passage has to point at the door that is actually built, and
	if the scene list ever moves the door the passage follows it.

	CACHED, and the reason is a measured hang rather than tidiness: _mound_h calls this, the
	mound's 3,721 vertices call _mound_h five times each for the central-difference normal,
	and the uncached version scanned all 70 rows of the scene list every time. 1.3 million
	dictionary lookups to answer one question that cannot change during a run -- the probe
	did not finish in ten minutes, which reads as a hang rather than as an O(n) loop nested
	three deep."""
	if _door_dir_cache != Vector2.ZERO:
		return _door_dir_cache
	for r in _scene_list:
		if String(r.get("asset", "")) == "lintel":
			var xz: Array = r.get("scene_xz", [1.0, 0.0])
			var d := Vector2(float(xz[0]), float(xz[1])) - MOUND_XZ
			if d.length() > 0.2:
				_door_dir_cache = d.normalized()
				return _door_dir_cache
	_door_dir_cache = Vector2(1.0, 0.0)
	return _door_dir_cache


func _mound_h(x: float, z: float) -> float:
	"""The mound's own height above the floor at (x, z). Zero outside it and zero in the
	passage, so a prop placed through _surface_y lands on whichever of the two it is over."""
	var d := Vector2(x, z) - MOUND_XZ
	var r := d.length()
	if r >= MOUND_R:
		return 0.0
	var u: float = clampf(1.0 - pow(r / MOUND_R, 2.0), 0.0, 1.0)
	var h: float = MOUND_RISE * pow(u, 1.15)
	# A PERFECT DOME READS AS A TENT. 7 cm of two-octave wobble, faded out at the rim so the
	# foot still meets the floor cleanly, is enough to make it a mound of earth. Deterministic
	# (sin/cos, no RNG) so two runs of the capture are the same picture.
	h += (sin(x * 2.31 + z * 1.07) * 0.045 + sin(x * 5.13 - z * 4.41) * 0.025) * u
	var dd := _door_dir()
	var along := d.dot(dd)
	var lat: float = absf(d.x * dd.y - d.y * dd.x)
	var side: float = smoothstep(PASSAGE_HALF_W, PASSAGE_HALF_W + PASSAGE_SOFT, lat)
	var depth: float = smoothstep(-0.30, 0.55, along)
	return h * lerpf(1.0, side, depth)


func _surface_y(x: float, z: float) -> float:
	"""WHAT A PROP STANDS ON, which is not the same as what the PLAYER walks on. The floor is
	flat and the mound is a structure; a rock emitted at a point inside the mound's footprint
	belongs on the mound, not buried under it. Six of the 68 are in that position."""
	return world.height_at(x, z) + _mound_h(x, z)


func _build_mound(mat: Material) -> MeshInstance3D:
	var half: int = int(ceil((MOUND_R + 0.2) / MOUND_CELL))
	var n := half * 2
	var verts := PackedVector3Array()
	var norms := PackedVector3Array()
	var uvs := PackedVector2Array()
	var idx := PackedInt32Array()
	verts.resize((n + 1) * (n + 1))
	norms.resize((n + 1) * (n + 1))
	uvs.resize((n + 1) * (n + 1))
	for j in n + 1:
		var z: float = MOUND_XZ.y + (float(j) - float(half)) * MOUND_CELL
		for i in n + 1:
			var x: float = MOUND_XZ.x + (float(i) - float(half)) * MOUND_CELL
			var k := j * (n + 1) + i
			verts[k] = Vector3(x, _mound_h(x, z), z)
			# the normal from the height function by central difference, at the cell size --
			# the same way the heightfield reader does it, so the two surfaces shade alike
			var e := MOUND_CELL
			var hx := _mound_h(x + e, z) - _mound_h(x - e, z)
			var hz := _mound_h(x, z + e) - _mound_h(x, z - e)
			norms[k] = Vector3(-hx, 2.0 * e, -hz).normalized()
			uvs[k] = Vector2(x, z) * 0.25
	for j in n:
		for i in n:
			var k := j * (n + 1) + i
			idx.append_array([k, k + n + 2, k + n + 1, k, k + 1, k + n + 2])
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = verts
	arr[Mesh.ARRAY_NORMAL] = norms
	arr[Mesh.ARRAY_TEX_UV] = uvs
	arr[Mesh.ARRAY_INDEX] = idx
	var mesh := ArrayMesh.new()
	mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	var mi := MeshInstance3D.new()
	mi.name = "BarrowMound"
	mi.mesh = mesh
	mi.material_override = mat
	add_child(mi)

	# NON-WALKABLE, AND BY THE COLLIDER RATHER THAN BY THE SLOPE. The dome's steepest face is
	# 36 degrees and move_and_slide's floor_max_angle is 45, so a trimesh of this mesh would
	# be a ramp he strolls up -- which is the exact thing R-C9-74 removed. The wall is a ring
	# of boxes standing on the rim, with the segments spanning the entrance LEFT OUT so he can
	# walk into the passage and stand in the doorway.
	var body := StaticBody3D.new()
	body.name = "MoundWall"
	body.collision_layer = BarrowFlat.TERRAIN_BIT
	body.collision_mask = 0
	mi.add_child(body)
	var dd := _door_dir()
	var door_a := atan2(dd.y, dd.x)
	var skip: float = asin(clampf(PASSAGE_HALF_W / MOUND_R, 0.0, 0.999))
	var kept := 0
	for s in WALL_SEGMENTS:
		var a: float = TAU * float(s) / float(WALL_SEGMENTS)
		if absf(wrapf(a - door_a, -PI, PI)) < skip:
			continue
		var cs := CollisionShape3D.new()
		var b := BoxShape3D.new()
		var seg: float = TAU * MOUND_R / float(WALL_SEGMENTS)
		b.size = Vector3(seg * 1.25, MOUND_RISE, 0.45)
		cs.shape = b
		cs.position = Vector3(MOUND_XZ.x + cos(a) * (MOUND_R - 0.18), MOUND_RISE * 0.5,
							  MOUND_XZ.y + sin(a) * (MOUND_R - 0.18))
		cs.rotation = Vector3(0.0, -a, 0.0)
		body.add_child(cs)
		kept += 1
	report["mound"] = {
		"centre_xz": [MOUND_XZ.x, MOUND_XZ.y], "radius_m": MOUND_R, "rise_m": MOUND_RISE,
		"_numbers_from": "height_a_authored.json mound block",
		"triangles": n * n * 2,
		"entrance_bearing_deg": snappedf(rad_to_deg(door_a), 0.1),
		"entrance_from": "the lintel's own placement in the scene list",
		"passage_half_width_m": PASSAGE_HALF_W,
		"passage_floor_y_at_door": snappedf(_mound_h(1.779, -3.512), 0.001),
		"_door_at_floor_level": _mound_h(1.779, -3.512) < 0.02,
		"wall_boxes": kept, "wall_boxes_omitted_for_the_entrance": WALL_SEGMENTS - kept,
		"_non_walkable_by": "a vertical-sided box ring, not by slope -- the dome's steepest face is 36 deg and floor_max_angle is 45",
	}
	return mi


# --- the real barrow: 70 placements, the measured way ------------------------
# The scene list in barrow_scene_a.json is 70 instances emitted FOR A NAMED GROUND. Three
# rules from T10_HANDOFF govern every one of them and each has a silent failure:
#
#   PITCH. Every Tripo model is squat by cos(52.9536 deg) = 0.602, because its reference
#     sheet was cropped out of a painting at that pitch. The Y stretch of 1.660 goes on
#     BEFORE the normalise, not after -- after it, the normalise has already fixed the wrong
#     dimension and the stretch makes the model too tall instead of the right shape.
#   YAW. Measured per model by silhouette match, not assumed. Applied as a Y rotation AFTER
#     sizing, because Godot's AABB is world-axis-aligned: a square post measured at 45 deg
#     reports a box sqrt(2) too wide and normalising against it makes the post 30% too thin.
#   FRAME. `scene = (world - grid_origin) + scene_offset`, and the two grids' origins differ
#     by (0.45, 0.36) m. The list used against the wrong ground puts every prop half a metre
#     off its own footprint -- which looks like a placement style, not like an error.
const PROP_CLASS_TO_SCENE_ASSET := {
	"stone_tall": "standing_stone_tall", "stone_mid": "standing_stone_mid",
	"stone_short": "standing_stone_short", "lintel": "barrow_lintel",
	"post": "barrow_post", "rock_large": "rock_outcrop_large",
	"rock_small": "rock_outcrop_small", "birch": "dead_birch", "juniper": "juniper_bush",
}
# which assets the `stone_scale` lever moves: the megalithic set, not the scatter
const MEGALITH := ["stone_tall", "stone_mid", "stone_short", "lintel", "post"]
# see the note at the skip site: two of the eleven birches are inside a megalith
const DROP_INTERPENETRATING := true


func _overlaps_placed(e: Dictionary, placed: Array) -> Dictionary:
	"""A TREE STANDING INSIDE A MEGALITH, and only that.

	THE FIRST VERSION OF THIS RULE WAS "any prop centre inside any prop's footprint" and it
	dropped TWELVE instances INCLUDING THE BARROW DOOR -- the lintel sits 0.49 m from a small
	rock, which is what props on a moor do. A rule that removes the one object the whole scene
	is named after, and reports it under a heading that says "upstream mask overlap", is a
	worse fault than the two trees it was written for.

	So it is narrow on purpose, and the narrowness is the specification: the emitted fault is
	a BIRCH mask that bled onto the megalith BEHIND it (T10_HANDOFF fault 5 -- SAM2 found no
	birch at all and the eleven are a union of five EVF prompts). Rocks touching stones are
	not that fault and are not touched. 0.55 of the megalith's own footprint radius, so the
	tree has to be well inside it rather than beside it."""
	if not (String(e["asset"]) in ["birch", "juniper"]):
		return {}
	var x := float(e["scene_xz"][0])
	var z := float(e["scene_xz"][1])
	for q in placed:
		if not (String(q["asset"]) in MEGALITH):
			continue
		var r: float = maxf(float(q["size_m"][0]), float(q["size_m"][2])) * 0.5 * 0.55
		var dx := x - float(q["scene_xz"][0])
		var dz := z - float(q["scene_xz"][1])
		var d := sqrt(dx * dx + dz * dz)
		if d < r:
			return {"asset": q["asset"], "d": d}
	# AN EMPTY DICTIONARY, NOT null. An untyped `return null` beside a `return {...}` makes
	# GDScript infer the function's type as null, and every later subscript of the result is
	# a PARSE error -- the whole script fails to load, and the only symptom at the call site
	# is a probe that never reaches its own quit().
	return {}


func _prop_params(cls: String) -> Dictionary:
	"""The snow layer's parameters per prop class. Separate from the base colours because the
	props keep THEIR OWN painted albedo (use_tex) -- what a class needs from this scene is how
	much snow settles on it, not what colour it is."""
	match cls:
		"heather":
			# a tussock is sprigs, not a slab: snow sits in it rather than on it. `mesh_mark`
			# 0.25 tells the screen-space pen this is THIN -- see PaintStack's POST_SHADER.
			return {"snow_threshold": 1.05, "snow_jitter": 0.24, "snow_soft": 0.09,
					"snow_noise_scale": 3.0, "mottle_scale": 4.0, "mottle_amp": 0.18,
					"hatch_scale": 18.0, "hatch_amp": 0.08, "mesh_mark": 0.25}
		"raven":
			# NO SNOW ON THE BIRD. 2.0 is above any achievable n.up, which is how this shader
			# says "never" -- and it says it through the same parameter as everything else
			# rather than through a second code path.
			return {"snow_threshold": 2.0, "snow_jitter": 0.0, "snow_soft": 0.05,
					"mottle_scale": 6.0, "mottle_amp": 0.10, "hatch_scale": 24.0}
		"birch", "juniper":
			return {"snow_threshold": 0.92, "snow_jitter": 0.20, "snow_soft": 0.08,
					"snow_noise_scale": 3.2, "mottle_scale": 5.0, "mottle_amp": 0.24,
					"hatch_scale": 22.0, "hatch_amp": 0.10, "mesh_mark": 0.25}
		"rock_large", "rock_small":
			return {"snow_threshold": 0.58, "snow_jitter": 0.30, "snow_soft": 0.11,
					"snow_noise_scale": 2.4, "mottle_scale": 2.2, "mottle_amp": 0.18,
					"hatch_scale": 11.0, "hatch_amp": 0.07}
		_:
			return {"snow_threshold": 0.58, "snow_jitter": 0.26, "snow_soft": 0.10,
					"snow_noise_scale": 1.9, "mottle_scale": 1.5, "mottle_amp": 0.18,
					"hatch_scale": 9.0, "hatch_amp": 0.07}


func _hull_for(cls: String) -> float:
	"""THE HULL PEN'S WIDTH FOR A CLASS, in screen pixels at the play camera, and ZERO for the
	three that cannot carry one.

	The pen is an inflate-and-cull-front hull, so it needs the mesh to have an INSIDE that is
	thicker than the line. A standing stone is 0.6 m across and a 1.1 px line at the play
	camera is 11 mm of world -- 2% of it, a rim. A heather tussock's sprigs and a birch's
	twigs are a few millimetres across, so the same line is wider than the thing it is
	outlining and the inflated copy closes over it. Measured by eye on look_play at 1920x1080:
	every birch and every tussock rendered as a solid black blot with no internal structure at
	all, while the identical pen on the stones beside them is a clean 1 px contour.

	This is the T9 failure from the other side -- there it was an OPEN mesh (a wall skirt with
	no inside at all) and here it is a THIN one -- and the answer is the same: those meshes get
	the screen-space pass, which has no such failure mode, and the solid ones keep the hull.
	R-C9-74 note 5's "one pen, one weight" is unaffected: it is the same colour and the same
	nominal width, drawn by the pass that can draw it."""
	match cls:
		"heather", "birch", "juniper":
			return 0.0
		_:
			return HULL_PX


func _node_aabb(root: Node3D) -> AABB:
	"""The node's own bounds in ITS OWN space, ink meshes excluded. Excluded because the hull
	pen is an inflated copy of the mesh: measuring it would grow every prop by two line widths
	per re-measure, compounding."""
	var out := AABB()
	var first := true
	var inv := root.global_transform.affine_inverse()
	for n in root.find_children("*", "MeshInstance3D", true, false):
		var mi := n as MeshInstance3D
		if mi.mesh == null or String(mi.name).ends_with("_ink"):
			continue
		var b: AABB = (inv * mi.global_transform) * mi.mesh.get_aabb()
		if first:
			out = b
			first = false
		else:
			out = out.merge(b)
	return out


func _ground_under(x: float, z: float, r: float) -> Dictionary:
	"""The height to stand a prop of footprint radius `r` on: the LOWEST of its centre and
	four rim samples, so a base on a slope is buried on the uphill side rather than floating
	on the downhill one. Returns the spread too -- a prop whose footprint spans 40 cm of
	relief is a prop the eye will see standing on a corner."""
	var hs := [_surface_y(x, z)]
	for a in [0.0, 0.25, 0.5, 0.75]:
		var t: float = a * TAU
		hs.append(_surface_y(x + cos(t) * r, z + sin(t) * r))
	var lo: float = hs[0]
	var hi: float = hs[0]
	for h in hs:
		lo = minf(lo, float(h))
		hi = maxf(hi, float(h))
	return {"lo": lo, "hi": hi, "centre": float(hs[0]), "spread": hi - lo}


func _build_scene_props(stone_mat: ShaderMaterial, rock_mat: ShaderMaterial,
		wood_mat: ShaderMaterial) -> Array:
	var man := {}
	if FileAccess.file_exists(ASSETS_JSON):
		var mj = JSON.parse_string(FileAccess.get_file_as_string(ASSETS_JSON))
		if typeof(mj) == TYPE_DICTIONARY:
			man = mj.get("models", {})
	var sizes := {}
	var stone_scale := 1.0
	if FileAccess.file_exists(SCENE_JSON):
		var sj = JSON.parse_string(FileAccess.get_file_as_string(SCENE_JSON))
		if typeof(sj) == TYPE_DICTIONARY:
			sizes = sj.get("assets", {})
			stone_scale = float(sj.get("stone_scale", 1.0))
	var pitch := 1.0 / cos(deg_to_rad(PL_PITCH_DEG))

	_props_root = Node3D.new()
	_props_root.name = "BarrowProps"
	add_child(_props_root)

	var by_class := {}
	var rep_mat := {}
	var placed := []
	var skipped := []
	var seen := {}
	var tris := 0
	var idx := 0
	for row in _scene_list:
		var cls := String(row.get("asset", ""))
		idx += 1
		if cls == "raven":
			continue                                  # perched last, on the stone it sits on
		# TWO ROWS OF THE LIST ARE EXACT DUPLICATES of two others -- one heather at
		# (-1.251, -0.322) and one stone_tall at (3.639, -4.742), same asset, same xz, same
		# height. Placing both puts two identical meshes in the same millimetre: z-fighting
		# on every facet and a hull pen drawn twice, which reads as a shader fault rather than
		# as a duplicated row. 70 listed, 68 distinct, and the count is in the report so the
		# gap between them is visible rather than absorbed.
		var xz0: Array = row.get("scene_xz", [0.0, 0.0])
		var key := "%s|%.3f|%.3f|%.3f" % [cls, float(xz0[0]), float(xz0[1]),
										  float(row.get("height_m", 0.0))]
		if seen.has(key):
			skipped.append({"asset": cls, "at": [float(xz0[0]), float(xz0[1])],
							"why": "exact duplicate of an earlier row in the list"})
			continue
		seen[key] = true
		var spec: Dictionary = man.get(cls, {})
		var glb := String(spec.get("glb", "res://models/barrow/%s.glb" % cls))
		if not ResourceLoader.exists(glb):
			skipped.append({"asset": cls, "glb": glb, "why": "not in the project"})
			continue
		var target := float(row.get("height_m", spec.get("height_m", 1.0)))
		var across := String(spec.get("axis", "height")) == "across"
		if cls in MEGALITH:
			target *= stone_scale
		if across:
			# THE LINTEL IS SIZED BY ITS LENGTH AND NOT BY ITS HEIGHT, and that is the one
			# dimension in this whole set that the painting gives unforeshortened: a beam
			# lying across the screen is not raked. Its height then comes out of the model's
			# own corrected ratio and is CHECKED against the plan's 1.18 m below.
			var sk := String(PROP_CLASS_TO_SCENE_ASSET.get(cls, ""))
			target = float(sizes.get(sk, {}).get("width_m", spec.get("height_m", 2.28))) * stone_scale
		var e := _place_prop(cls, glb, spec, sizes, row, target, across, pitch, idx)
		if e.is_empty():
			skipped.append({"asset": cls, "glb": glb, "why": "no mesh in the glb"})
			continue
		# TWO BIRCHES STAND INSIDE A MEGALITH and it is an upstream mask overlap, not a
		# placement bug: birch #2 at (3.631, -4.741) is 8 mm from stone_tall at
		# (3.639, -4.742), and birch #7 at (1.538, -1.674) is 83 mm from a barrow post. The
		# handoff already says where this comes from -- the 11 birches are a union of five
		# EVF prompts, SAM2 found none, and the union bled onto the stones behind them.
		#
		# DROPPED, NOT RENDERED, and this is a presentation-side override of emitted data. A
		# tree growing through a standing stone is the first thing anyone looking at this
		# frame would see and the last thing they would read as "the concept says so". It is
		# one flag and it names both parties in the report, so it is reversible in one line
		# and the upstream fault is visible rather than papered over.
		# TODO(drax): remove when the T10 birch list is re-cut against a second sheet
		# (T10_HANDOFF fault 2 already queues that sheet).
		if DROP_INTERPENETRATING and cls != "heather":
			var hit := _overlaps_placed(e, placed)
			if not hit.is_empty():
				skipped.append({"asset": cls, "at": e["scene_xz"],
								"why": "footprint centre inside %s -- upstream mask overlap"
									% String(hit["asset"]),
								"gap_m": snappedf(float(hit["d"]), 0.001)})
				(e["node"] as Node3D).queue_free()
				continue
		placed.append(e)
		tris += int(e["tris"])
		if not by_class.has(cls):
			by_class[cls] = []
		by_class[cls].append(e["node"])
		if not rep_mat.has(cls):
			rep_mat[cls] = e["mat"]

	_perch_raven(man, sizes, pitch, placed, by_class, rep_mat)

	# GROUPED THE WAY THE SNOW MEASUREMENT NEEDS: one entry per set of snow parameters, which
	# is per class-family and not per asset -- the five megaliths share a threshold, so
	# reporting them separately would be five copies of one number.
	var fam := {"standing_stones": ["stone_tall", "stone_mid", "stone_short", "lintel", "post"],
				"rocks": ["rock_large", "rock_small"],
				"birches": ["birch", "juniper"],
				"heather": ["heather"],
				"raven": ["raven"]}
	var groups := []
	for g in fam:
		var meshes := []
		var mat = null
		for c in fam[g]:
			for n in by_class.get(c, []):
				for m in (n as Node3D).find_children("*", "MeshInstance3D", true, false):
					if not String((m as MeshInstance3D).name).ends_with("_ink"):
						meshes.append(m)
			if mat == null and rep_mat.has(c):
				mat = rep_mat[c]
		if meshes.is_empty() or mat == null:
			continue
		groups.append({"name": g, "mat": mat, "meshes": meshes})

	var counts := {}
	for c in by_class:
		counts[c] = (by_class[c] as Array).size()
	report["props"] = {
		"source": SCENE_JSON, "frame": report.get("terrain_source", {}).get("stem", "?"),
		"listed": _scene_list.size(), "placed": placed.size(), "skipped": skipped,
		"by_asset": counts, "triangles": tris,
		"hull_pen_meshes": _prop_inks.size(),
		"stone_scale": stone_scale,
		"_stone_scale": "Matt's lever, applied to %s; 1.37 makes the stones twice his height" % str(MEGALITH),
		"pitch_stretch_applied": snappedf(pitch, 0.0001),
		"placement": _place_report,
	}
	return groups


func _place_prop(cls: String, glb: String, spec: Dictionary, sizes: Dictionary,
		row: Dictionary, target: float, across: bool, pitch: float, idx: int) -> Dictionary:
	var ps := load(glb) as PackedScene
	if ps == null:
		return {}
	var root := Node3D.new()
	root.name = "%s_%02d" % [cls, idx]
	_props_root.add_child(root)
	var fit := Node3D.new()
	fit.name = "fit"
	root.add_child(fit)
	fit.add_child(ps.instantiate())
	var raw := _node_aabb(root)
	if raw.size.y <= 0.0 and raw.size.x <= 0.0:
		root.queue_free()
		return {}

	# 1. pitch, 2. normalise -- in that order, on the RAW (unrotated) bounds
	var sy := pitch if bool(spec.get("pitch_correct", true)) else 1.0
	var k := 0.0
	if across:
		k = target / maxf(maxf(raw.size.x, raw.size.z), 1e-6)
	else:
		k = target / maxf(raw.size.y * sy, 1e-6)
	fit.scale = Vector3(k, k * sy, k)

	# 3. the birch's forced width -- a stated non-uniform squash, scaled with the instance.
	# The manifest forces 1.38 m at the canonical 3.36 m tree; a 1.44 m one gets 1.38 * 1.44
	# / 3.36, because a forced ABSOLUTE width would make every short birch a bush.
	var forced = spec.get("width_m", null)
	if forced != null and float(forced) > 0.0:
		var nominal := maxf(float(spec.get("height_m", target)), 1e-6)
		var want := float(forced) * (target / nominal)
		var cur := maxf(maxf(raw.size.x, raw.size.z) * k, 1e-6)
		var wk := want / cur
		fit.scale = Vector3(fit.scale.x * wk, fit.scale.y, fit.scale.z * wk)

	# 4. centre the footprint on the origin and put the base at y = 0
	var b := _node_aabb(root)
	fit.position = Vector3(-(b.position.x + b.size.x * 0.5), -b.position.y,
						   -(b.position.z + b.size.z * 0.5))
	var fin := _node_aabb(root)

	# 5. the turn, AFTER the sizing
	var yaw = row.get("yaw_deg", null)
	if yaw == null:
		yaw = spec.get("yaw_deg", null)
	if yaw == null:
		# heather has no measured yaw ("any yaw" in the handoff). Deterministic per index, so
		# two runs of the capture are the same picture -- a random yaw makes every A/B pair a
		# comparison of two scenes.
		yaw = float((idx * 137) % 360)
	root.rotation.y = deg_to_rad(float(yaw))

	# 6. on the ground
	var xz: Array = row.get("scene_xz", [0.0, 0.0])
	var x := float(xz[0])
	var z := float(xz[1])
	var r: float = maxf(maxf(fin.size.x, fin.size.z) * 0.5, 0.05)
	var g := _ground_under(x, z, r)
	root.global_position = Vector3(x, float(g["lo"]) - PROP_SINK_M, z)

	# AN OBSTACLE, NOT SCENERY. R-C9-74: "The outcrops become rock obstacles, not raised
	# ground." On the flat floor they no longer stop him by being a hill, so they stop him by
	# being solid: one vertical-sided cylinder per prop, at 0.42 of the footprint so he brushes
	# past rather than bumping into thin air. Heather is walked through -- it is 80 cm of
	# twigs -- and the raven is on top of a stone.
	if cls != "heather" and cls != "raven":
		var body := StaticBody3D.new()
		body.name = "obstacle"
		body.collision_layer = BarrowFlat.TERRAIN_BIT
		body.collision_mask = 0
		var cs := CollisionShape3D.new()
		var cy := CylinderShape3D.new()
		cy.radius = maxf(maxf(fin.size.x, fin.size.z) * 0.42, 0.08)
		cy.height = maxf(fin.size.y, 0.2)
		cs.shape = cy
		cs.position = Vector3(0.0, cy.height * 0.5, 0.0)
		body.add_child(cs)
		root.add_child(body)

	var saved := PaintStack.adopt_prop(root, fbm, PaintStack.INK, _hull_for(cls) / PPM,
									   _prop_params(cls))
	var mat = null
	var tris := 0
	for e in saved.get("meshes", []):
		if mat == null:
			mat = e["ramp"]
		_world_mats.append(e["ramp"])
		var mi := (e["mi"]) as MeshInstance3D
		if mi.mesh != null:
			for s in mi.mesh.get_surface_count():
				# surface_get_arrays COPIES every array in the surface -- vertices, normals,
				# UVs, weights, the lot. Called once per prop mesh over 1.2 M triangles that
				# is hundreds of megabytes of allocation to learn a number the mesh already
				# knows. ArrayMesh reports the index count directly.
				tris += (mi.mesh as ArrayMesh).surface_get_array_index_len(s) / 3 \
					if mi.mesh is ArrayMesh else 0
	for e in saved.get("inks", []):
		_prop_inks.append(e["mi"])
	var rec := {"node": root, "mat": mat, "tris": tris, "asset": cls,
			"size_m": [snappedf(fin.size.x, 0.001), snappedf(fin.size.y, 0.001),
					   snappedf(fin.size.z, 0.001)],
			"target_m": snappedf(target, 0.001), "across": across,
			"scene_xz": [x, z], "yaw_deg": float(yaw),
			"ground": g, "top_y": root.global_position.y + fin.size.y}
	# WHAT THIS PROP WAS ASKED FOR, kept BY NODE NAME. The check used to re-find the concept
	# height by matching the node's world xz back against the list -- and two rows sit 8 mm
	# apart (a birch and a standing stone), so the stone's 2.71 m was checked against the
	# birch's 3.02 m and reported as a 10% sizing error in a prop that was exactly right.
	# A verification that re-derives its own expected value can find a fault that is entirely
	# its own; this one is handed the number the placement actually used.
	_place_report[String(root.name)] = {
		"asset": cls, "concept_height_m": snappedf(float(row.get("height_m", target)), 0.001),
		"target_m": snappedf(target, 0.001), "sized_by": "across" if across else "height",
		"local_size_m": rec["size_m"], "yaw_deg": float(yaw),
		"ground_spread_m": snappedf(float(g["spread"]), 0.001),
	}
	return rec


func _perch_raven(man: Dictionary, sizes: Dictionary, pitch: float, placed: Array,
		by_class: Dictionary, rep_mat: Dictionary) -> void:
	"""The T9 raven, on the tallest stone that was actually built -- found by measuring the
	placed instances' tops, not by looking up which asset is nominally tallest. `stone_tall`
	is nominally 2.71 m, but the instance list carries its own per-instance heights and the
	lever scales them, so the nominal answer and the built answer can differ."""
	var row := {}
	for r in _scene_list:
		if String(r.get("asset", "")) == "raven":
			row = r
	if row.is_empty():
		return
	var best = null
	for e in placed:
		if String(e["asset"]) in MEGALITH and (best == null or float(e["top_y"]) > float(best["top_y"])):
			best = e
	if best == null:
		return
	_tallest_stone = best["node"]
	var glb := "res://models/barrow/raven.glb"
	if not ResourceLoader.exists(glb):
		report["raven"] = {"placed": false, "why": "%s not in the project" % glb}
		return
	var e2 := _place_prop("raven", glb, {"pitch_correct": true, "yaw_deg": 200.0}, sizes,
						  {"scene_xz": best["scene_xz"], "height_m": float(row.get("height_m", 0.28))},
						  float(row.get("height_m", 0.28)), false, pitch, 999)
	if e2.is_empty():
		return
	var n := e2["node"] as Node3D
	n.global_position = Vector3(float(best["scene_xz"][0]), float(best["top_y"]) - 0.04,
								float(best["scene_xz"][1]))
	if not by_class.has("raven"):
		by_class["raven"] = []
	by_class["raven"].append(n)
	if not rep_mat.has("raven"):
		rep_mat["raven"] = e2["mat"]
	report["raven"] = {"placed": true, "on": String(_tallest_stone.name),
					   "perch_top_y": snappedf(float(best["top_y"]), 0.01),
					   "stone_height_m": snappedf(float(best["size_m"][1]), 0.01)}


func verify_placements(names: Array) -> Dictionary:
	"""THE THREE-INSTANCE CHECK, BY THE NUMBERS AND NOT BY EYE ALONE.

	For each named prop: the gap between the bottom of its mesh AABB and the terrain height
	under it (must be <= 0 -- a positive gap is a floating prop), the gap at four rim points,
	and the built size against what the concept says it should be. The ratio is the test: a
	prop 1.66x too tall is one whose pitch stretch ran twice, and 0.60x is one that never ran.

	Verified on a known case first: a node lifted 0.5 m must report a 0.5 m gap."""
	var out := {"_defn": {
		"base_gap_m": "mesh AABB min y MINUS terrain height at the prop's own xz; <= 0 is on the ground",
		"height_ratio": "built height / the concept's height for that instance; 1.0 is right, 1.66 and 0.60 are the two pitch-stretch failures",
	}, "props": {}}
	if _props_root == null:
		return out
	# the instrument, on a case whose answer is known by construction
	var probe := Node3D.new()
	_props_root.add_child(probe)
	probe.global_position = Vector3(0.0, _surface_y(0.0, 0.0) + 0.5, 0.0)
	out["instrument_check_node_lifted_0.5m"] = snappedf(
		probe.global_position.y - _surface_y(0.0, 0.0), 0.0001)
	probe.queue_free()
	for nm in names:
		var n := _props_root.get_node_or_null(NodePath(String(nm))) as Node3D
		if n == null:
			out["props"][String(nm)] = {"_": "not found"}
			continue
		var b := _node_aabb(n)
		var wb := n.global_transform * b
		var gx := n.global_position.x
		var gz := n.global_position.z
		var r: float = maxf(maxf(wb.size.x, wb.size.z) * 0.5, 0.05)
		var rim := []
		for a in [0.0, 0.25, 0.5, 0.75]:
			var t: float = a * TAU
			rim.append(snappedf(wb.position.y - _surface_y(gx + cos(t) * r, gz + sin(t) * r), 0.001))
		var rec: Dictionary = _place_report.get(String(nm), {})
		var want := float(rec.get("concept_height_m", 0.0))
		var sized := String(rec.get("sized_by", "height"))
		# THE FOOTPRINT IS THE UNROTATED ONE. Godot's AABB is world-axis-aligned, so the
		# lintel -- a 2.28 m beam turned -47 degrees -- reports a 2.07 x 1.99 box in world
		# space, and checking THAT against the plan's 2.28 m across says the beam is 9% short
		# when it is exact. This is the same trap T10_HANDOFF names on the sizing side,
		# arriving on the verification side: the built size is read from the node's own local
		# bounds, and the world box is reported beside it so the two can be seen to differ.
		var local: Array = rec.get("local_size_m", [wb.size.x, wb.size.y, wb.size.z])
		var across_built: float = maxf(float(local[0]), float(local[2]))
		var perched: bool = String(rec.get("asset", "")) == "raven"
		var entry := {
			"asset": rec.get("asset", "?"),
			"world_xz": [snappedf(gx, 0.001), snappedf(gz, 0.001)],
			"built_size_m_local": local,
			"world_axis_aligned_box_m": [snappedf(wb.size.x, 0.001), snappedf(wb.size.y, 0.001),
										 snappedf(wb.size.z, 0.001)],
			"yaw_deg": rec.get("yaw_deg", 0.0),
			"sized_by": sized,
			"concept_height_m": snappedf(want, 0.001),
			"terrain_y_under": snappedf(_surface_y(gx, gz), 0.001),
			"floor_y_under": snappedf(world.height_at(gx, gz), 0.001),
			"mound_y_under": snappedf(_mound_h(gx, gz), 0.001),
			"base_gap_m": snappedf(wb.position.y - _surface_y(gx, gz), 0.001),
			"rim_gaps_m": rim,
			"ground_spread_under_footprint_m": rec.get("ground_spread_m", null),
			"on_ground": perched or (wb.position.y - _surface_y(gx, gz)) <= 0.001,
			"perched_by_design": perched,
		}
		if want > 0.0:
			entry["height_ratio"] = snappedf(float(local[1]) / want, 0.001)
		if sized == "across":
			entry["across_built_m"] = snappedf(across_built, 0.001)
			entry["across_target_m"] = rec.get("target_m", null)
			entry["across_ratio"] = snappedf(across_built / maxf(float(rec.get("target_m", 1.0)), 1e-6), 0.001)
		out["props"][String(nm)] = entry
	return out


func prop_names() -> Array:
	var o := []
	if _props_root != null:
		for c in _props_root.get_children():
			o.append(String((c as Node).name))
	return o


func prop_node(nm: String) -> Node3D:
	if _props_root == null:
		return null
	return _props_root.get_node_or_null(NodePath(nm)) as Node3D


func _build_particles() -> void:
	var air := Node3D.new()
	air.name = "Air"
	add_child(air)
	snowfall = PaintStack.snowfall(flake, Vector3(46, 28, 46), 1700)
	air.add_child(snowfall)
	gust = PaintStack.ridge_gust(flake, 420)
	air.add_child(gust)
	# UP-SCREEN AND BEYOND THE BARROW, so the gust reads as weather crossing the far ground
	# rather than as a fountain beside him. The old point (15, -14) was on the stand-in's
	# ridge; the measured ground has no ridge there -- it is relaxed flat moor 8 m outside the
	# painting, and a gust rising off flat nothing is the kind of detail that reads as a bug.
	var gx := -2.6
	var gz := -7.4
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
		"depth_edge_px": 3.0,
		"normal_edge": 1.05,
		"normal_weight": 0.30,
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
		"screen_space": {"operator": "second difference of linear depth (silhouette) + Roberts on the view-space normal buffer (crease)",
						 "line_px": 1.25, "depth_edge_px": 3.0, "normal_edge": 1.05,
						 "normal_weight": 0.30},
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
		+ "   ‖   V stack (%s) · K ink (%s) · N snow (%s) · J air (%s)") \
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


func set_char_hull_visible(on: bool) -> void:
	"""HIS hull pen alone, leaving the PROPS' hulls drawn. The props got the same pen in this
	pass, so `set_hull_ink_visible` now hides 68 stones' outlines as well as his -- which is
	right for the one-pen colour check and wrong for the question R-C9-74 note 5 asks, which
	is how wide the line around HIM is. Two functions because they are two measurements."""
	for e in _char_saved.get("inks", []):
		((e["mi"]) as MeshInstance3D).visible = on


func ink_shadow_audit() -> Dictionary:
	"""NO INK OR HULL MESH CASTS A SHADOW (R-C9-74 note 3, acceptance 3). Asserted by walking
	the tree rather than by trusting the two places that set it: HULL_INK_SHADER declares
	`shadows_disabled` and every ink MeshInstance3D is built with cast_shadow OFF, and a mesh
	that had neither would throw an inflated silhouette onto the ground -- a shadow slightly
	too big for its caster, which is exactly the artefact that is hard to attribute."""
	var n := 0
	var bad := []
	for mi in find_children("*", "MeshInstance3D", true, false):
		var m := mi as MeshInstance3D
		if not (String(m.name).ends_with("_ink") or String(m.name) == "InkLine"):
			continue
		n += 1
		if m.cast_shadow != GeometryInstance3D.SHADOW_CASTING_SETTING_OFF:
			bad.append(String(m.name))
	return {"ink_meshes": n, "casting_a_shadow": bad, "_pass": bad.is_empty()}


func set_hull_ink_visible(on: bool) -> void:
	"""Hide the character's HULL pen alone, leaving the screen-space pen and everything else
	untouched. Differencing a frame against this one is how the hull line's delivered colour
	is isolated for the ΔE against the screen-space line -- each pen measured by the pixels
	it actually painted, rather than by guessing which dark pixels belong to which pass."""
	for e in _char_saved.get("inks", []):
		((e["mi"]) as MeshInstance3D).visible = on
	# AND THE PROPS' PENS. They are the same pen on the same rule, so a "hull ink" measurement
	# that hid only his would attribute every stone's outline to the screen-space pass -- the
	# two populations would be mixed in one number and the number would look fine.
	for mi in _prop_inks:
		(mi as MeshInstance3D).visible = on


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


func set_char_exclude(on: bool) -> void:
	"""Whether the SCREEN-SPACE pen skips him (R-C9-74 note 5). Off is the 15:20 build's
	behaviour -- both pens on him at once -- and it exists only so the before and the after
	are two frames of ONE run rather than two runs: the pair is subtracted to isolate the
	pixels the second pen was adding to his outline, which is the whole quantity in question."""
	post_mat.set_shader_parameter("char_exclude", 1.0 if on else 0.0)


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


const RAW_KEYS := {"V": KEY_V, "N": KEY_N, "J": KEY_J, "K": KEY_K}


func _check_key_collisions() -> void:
	"""ASK THE INPUT MAP WHETHER THESE KEYS ARE ALREADY SPOKEN FOR.

	This scene reads V/N/M/K as RAW physical keycodes rather than adding actions to the
	shared project.godot. That keeps it out of a file a concurrent workstream is editing --
	and it means a key that LATER becomes an action collides silently, firing both this
	scene's toggle and the action's handler on one press, with nothing anywhere saying so.
	That is not hypothetical: `C` was this scene's air toggle and became `shield_bash`
	(keycode 67) when the armed motion set landed, so one keypress hid the snow AND swung
	the shield. Caught by the coordinator, not by the code.

	So the code checks. Every action in the InputMap is scanned for a key event matching one
	of ours, and a hit is a pushed warning plus a line in the report -- which is what makes
	the next clash cost a glance at the JSON instead of a confused bug report."""
	var project := {}
	var builtin := {}
	var modified := {}
	for action in InputMap.get_actions():
		for ev in InputMap.action_get_events(action):
			var ke := ev as InputEventKey
			if ke == null:
				continue
			var code: int = ke.physical_keycode if ke.physical_keycode != 0 else ke.keycode
			# MODIFIERS COUNT, and the first version of this check ignored them -- which is
			# how it reported V clashing with `ui_paste` and M with `ui_focus_mode`. Those
			# actions are Ctrl+V and Ctrl+M: a BARE V press does not fire either, so a bare
			# key is only taken if some action wants it bare. Ignoring the modifier makes the
			# check pessimistic, and a check that cries wolf on two of four keys is a check
			# whose next real finding gets waved through. Modified matches are still listed --
			# under their own heading, where they are information and not an alarm.
			var bare: bool = not (ke.ctrl_pressed or ke.alt_pressed or ke.meta_pressed
								  or ke.shift_pressed or ke.command_or_control_autoremap)
			for name in RAW_KEYS:
				if code != RAW_KEYS[name]:
					continue
				if not bare:
					modified[name] = "%s (modified)" % String(action)
					continue
				# THE TWO KINDS ARE NOT THE SAME KIND OF PROBLEM. A PROJECT action on one of
				# these keys double-fires with gameplay -- that is the `shield_bash` case and
				# it is a defect. Godot's own `ui_*` defaults only reach a focused Control,
				# and this scene has none (the HUD is a Label and a ColorRect, neither
				# focusable), so they are reported and not warned about. Listing them anyway,
				# because "no clashes" would be a lie and the day a focusable Control appears
				# is the day V starts pasting.
				if String(action).begins_with("ui_"):
					builtin[name] = String(action)
				else:
					project[name] = String(action)
					push_warning("barrow: key %s also drives project action '%s'" % [name, action])
	report["key_collisions"] = {
		"raw_keys": {"V": "stack", "N": "snow", "J": "air", "K": "ink"},
		"clashes_with_project_actions": project,
		"clashes_with_builtin_ui_actions_informational": builtin,
		"same_key_but_only_with_a_modifier_informational": modified,
		"_clear_of_project_actions": project.is_empty(),
		"_clear_of_bare_key_clashes_of_any_kind": project.is_empty() and builtin.is_empty(),
		"_history": "C was this scene's air toggle and became shield_bash (67); M was its replacement and Godot binds Ctrl+M to ui_focus_mode. J is bare-free.",
	}


func _unhandled_input(e: InputEvent) -> void:
	if e.is_action_pressed("gear_cycle") and knight != null:
		knight.cycle_gear()
		_update_hud()
	elif e.is_action_pressed("size_down"):
		step_size(-1)
	elif e.is_action_pressed("size_up"):
		step_size(1)
	elif e is InputEventKey and (e as InputEventKey).pressed and not (e as InputEventKey).echo:
		# V, N, J and K are read as RAW KEYS rather than added to project.godot's [input]
		# map. project.godot is shared with the cliffside scenes and a concurrent workstream;
		# an additive edit there is small but it is not zero, and this costs nothing.
		match (e as InputEventKey).physical_keycode:
			KEY_V: set_stack(not stack_on)
			KEY_N: set_snow(not snow_on)
			KEY_J: set_particles(not particles_on)
			KEY_K: set_ink(not ink_on)
