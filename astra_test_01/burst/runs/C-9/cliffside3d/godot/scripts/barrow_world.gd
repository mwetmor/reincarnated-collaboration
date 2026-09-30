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
const LOD_THRESHOLD_PX := 2.0

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
	# THE MESH-LOD ERROR THRESHOLD, 1 px -> 2 px, and it is the frame budget's lever.
	# T10-1b's dressing put the frame at 16.83 ms against 16.7 (tools/probe_cost.gd). Measured
	# per asset, every Tripo instance cost ~25 us WHATEVER ITS SIZE ON SCREEN -- a 0.4 m rock as
	# much as a 1.6 m one -- while the 272-face procedural heather cost ~1 us: vertex work, in
	# four passes, on meshes whose imported LODs the default 1 px threshold barely uses. At
	# 2 px: 15.98 ms. At 4: 14.83. At 8: 14.28. Two pixels of silhouette error sits under the
	# 1.1 px hull pen and the paper grain; four is the next lever if the budget tightens.
	get_viewport().mesh_lod_threshold = LOD_THRESHOLD_PX
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
	_build_play_bounds()
	_build_snow()
	_build_post()
	_build_hud()
	_check_key_collisions()
	report["stand_in"] = world.report
	_apply_stack()
	# THE FOOT LOCK, COUNTED (T10-1d): knight.gd builds a FootLock node under his skeleton only
	# when character.json says "foot_lock": true, and prints nothing either way -- so the app's
	# launch log carries the count, and tools/build_app_barrow.sh fails a build that is not 0
	# (the lock was rolled back after "he drops to the floor as if drunk", R-C9-86)
	var fl := 0
	if knight != null:
		for n in knight.find_children("FootLock*", "", true, false):
			fl += 1
	print("[barrow] foot_lock nodes=%d" % fl)
	report["foot_lock_nodes"] = fl


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
	# THE NEAR PLANE SITS 22 m SHORT OF THE AIM, not at 0.05, and the shadow reach follows the
	# zoom (_shadow_reach) instead of a fixed 110 m. The HYPOTHESIS was that the directional
	# shadow is fitted from near to max distance and that 0.05..110 m put every prop in the scene
	# into the shadow pass every frame. MEASURED, it bought nothing: 16.95 ms before, 16.99 after
	# (tools/probe_cost.gd, ABAB, spreads 0.05/0.11) -- so either the fit does not work that way
	# or the pass was not the cost. It is kept because it is correct (the frame sits at 60 +- 4 m
	# of view depth, nothing is nearer than ~48 m) and it concentrates the map's resolution; it
	# is NOT claimed as a saving.
	cam.near = CAM_STANDOFF - 22.0
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
	# THE DOT SCREEN, FIXED (T10-1d). T10-1c found a regular 2-px dot grid along every shadow
	# edge, widest on the mound's flank: the soft filter's per-pixel rotated kernel makes a noisy
	# penumbra, and the ramp's band edges (slope 10) thresholded that noise into a halftone.
	# The coordinator's call: apply the cast shadow AFTER the bands (PaintStack's RAMP_BODY,
	# shadow_after_bands), and it is the bigger half -- 2x2 checker energy on the flank 5.88 ->
	# 3.85 at the same filter. The rest is the filter's own noise, now unamplified, as a faint
	# stipple in wide penumbrae; Soft MEDIUM takes it to 1.95 against 1.6 with no shadow at all
	# (Soft High 1.62), and keeps the stones' shadow shapes (Ultra smudged them). Measured in
	# one run: Low 16.65, Medium 16.91 (+0.26 ms), High 17.64 ms. set_shadow_after_bands(false)
	# puts back BOTH halves -- T10-1c's ramp and Soft Low -- so its A/B is T10-1c's shadow.
	RenderingServer.directional_soft_shadow_filter_set_quality(SHADOW_FILTER_T10_1D)
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
	sun.directional_shadow_max_distance = _shadow_reach(1.0)
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
	var fbm_img := PaintStack.make_fbm_image(512, 7411, 4)
	fbm = ImageTexture.create_from_image(fbm_img)
	paper = PaintStack.make_paper_texture(512)
	flake = PaintStack.make_flake_texture(24)
	var t_tex := Time.get_ticks_msec() - t0
	# the fbm as raw bytes, for the snow mask's patch noise: mip level 0 is the first 512*512*3
	# of an RGB8 image, and it is THIS image, not a readback of the texture made from it
	_fbm_bytes = fbm_img.get_data()
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
		# THE MOUND GETS ITS OWN COPY of the ground material, and the copy KEEPS its snow layer.
		# Under the 3D snow field the ground's layer goes to 0 -- that layer is the milky veil --
		# but the mound stands up out of the field, so with the ground's material it would come
		# out bare tile from crown to foot. Same tiles, same splat, same ramp; only snow_amount
		# differs, which is the one thing that has to.
		var mound_mat := ground.duplicate() as ShaderMaterial
		# PATCHIER THAN THE FLOOR WAS: a higher threshold with a wide jitter, so the crown holds
		# snow and the flanks break up -- a uniform white dome shows none of its 20-30 cm lumps,
		# because a lump reads by the light and the snow boundary across it, not by an outline
		mound_mat.set_shader_parameter("snow_threshold", 0.90)
		mound_mat.set_shader_parameter("snow_jitter", 0.60)
		mound_mat.set_shader_parameter("snow_soft", 0.12)
		_mound = _build_mound(mound_mat)
		_world_mats.append(mound_mat)
	var t_terr := Time.get_ticks_msec() - t1

	# THE REAL BARROW, OR THE STAND-IN'S HILL -- never a mixture. The 70 placements were
	# emitted against a NAMED ground; using them on the other one puts every prop half a
	# metre off its own footprint (T10_HANDOFF, the two grids' origins differ by 0.45, 0.36 m).
	var t2 := Time.get_ticks_msec()
	var groups: Array = []
	if (_hf != null or _flat != null) and FileAccess.file_exists(SCENE_JSON):
		groups = _build_scene_props(stone, rock, wood)
		var dres := _build_density()
		_pending_drifts = dres.get("drifts", [])
		# T10-1c, in dependency order: fill the unpainted play area from the splat, lay the
		# outcrops low, open the shore (on the FINAL footprints), then instance what is left
		report["fill"] = _fill_by_splat()
		report["rocks_laid"] = _lay_rocks_low()
		report["shore"] = _open_shore_gaps()
		report["rock_height_check"] = rock_height_check()
		if use_instancing:
			report["instancing"] = _instance_props()
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
			_splat_img = splat.get("img") if splat.get("img") != null else _splat.get_image()
			# THE BYTES THE FAST LOOKUPS READ. Declared, never filled, for one run: every one of
			# 22,500 mask cells came back "snow" at depth 0.981, the tarn got full snow, and
			# nothing errored -- _splat_w_fast returns pure snow when its cache is empty, by
			# design, for the area outside the painting. The per-class tally is what caught it.
			_splat_bytes = _splat_img.get_data()
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
const PASSAGE_SOFT := 0.80         # a sloped cutting, not a cliff: at 0.35 the passage walls
								   # read as one lit vertical plane across the mound
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
	# A PERFECT DOME READS AS A TENT, and 7 cm of wobble did not stop it (T10-1b: "more relief,
	# 20-30 cm lumps, not 7 cm"). Three octaves, the largest 0.14 m at a 4.6 m wavelength, so
	# the crown carries two or three real humps and a hollow; peak excursion 0.26 m. Faded out
	# at the rim by `u` so the foot still meets the floor, and clamped at zero so a trough near
	# the rim cannot dig below it. Deterministic (sin, no RNG): one capture, one mound.
	h += (sin(x * 1.37 + z * 0.61 + 0.4) * 0.14 + sin(x * 2.9 - z * 2.3 + 1.1) * 0.09
		+ sin(x * 5.13 - z * 4.41) * 0.03) * u
	h = maxf(h, 0.0)
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


# =============================================================================
#  T10-1b — THE SNOW HE STEPS THROUGH, THE EDGE OF THE WORLD, AND THE DRESSING
# =============================================================================
# The coordinator's calls after stills 1, 3, 5 and 10 (verbatim intent):
#   1. the milky veil is NOT the fog -- it is the ground's own FBM snow blend. SnowField in,
#      the ground's snow_amount to 0 under it, height fog off in the play area.
#   2. snow depth follows the splat: snow full, heather thin with tussocks through, rock thin
#      and patchy, path trodden thin, ice none.
#   3. bound the play area: the island plus a margin, invisible colliders, the boundary
#      dressed densely so the edge reads as land.
#   4. density inside from the kit, three scales, a clear combat floor and a path to the door.
#   5. heather its own snow rule.  6. the mound 20-30 cm lumps and drift skirts.

const PLAY_MARGIN_M := 2.0
const SNOW_AREA_M := 34.0
const WIND := Vector2(0.62, 0.78)
const DENSITY_SEED := 20260929
# THE COMBAT FLOOR IS WHERE THE PAINTING ALREADY PUT OPEN GROUND. The splat's path class is a
# blob at x 2.6..5.7, z -0.7..3.6 -- trodden, open, and exactly where he spawns. It is not a
# circle picked to look tidy; it is the one place in the concept nobody drew anything on.
# RE-CENTRED ON THE PAINTING'S OWN CLEARING. The first circle, (4.3, 0.5) r 2.5, was read off
# the splat's path blob and reached x 6.8 -- into the painting's right-hand outcrop, rejecting
# eleven painted rocks there. The clearing the painting has is the open snow round the figure,
# and the figure's painted base unprojects to (3.48, 0.28).
const COMBAT_C := Vector2(3.48, 0.28)
const COMBAT_R := 2.1
const DOOR_MOUTH := Vector2(2.7, -2.9)
# ON THE ICE MARGIN, not beside it: (1.6, 3.0) sat between three of the scene list's own shore
# rocks (rock_small at (1.96, 3.00), (1.64, 2.16), a birch at (1.62, 3.46)), and the return leg
# stopped 0.95 m short of it against one. The concept's shore rocks stay where it painted them.
# THE WALK STARTS ON THE TARN'S SHORE, INSIDE THE SHORE ROCKS -- and that is a finding, not a
# preference. The painting lines the tarn with rocks, and T10's list places them: a birch and
# four small rocks from (1.62, 3.46) to (0.50, 0.66), with gaps between their colliders of
# 0.06, 0.24, 0.55 and 0.61 m. His capsule is 0.70 m across. Two routes through them were
# tried and measured: the first slid along a rock 0.95 m short of the ice; the second wedged
# in the 0.61 m gap for five legs. The concept's shore stays as painted; the walk begins where
# the ice is in view over the rocks.
const TARN_EDGE := Vector2(2.6, 1.7)
const CORRIDOR_R := 0.7
# THE RETURN LEG'S DRIFT, fixed rather than searched for: it is a waypoint of the walk, so
# the ground round it and the legs to and from it are cleared of props like the other
# corridors -- a painted rock across the return leg would stop him dead in the movie.
const WALK_DRIFT := Vector2(2.9, 0.9)
# WHERE HE STOPS AT THE DOOR: on the threshold, clear of the posts. DOOR_MOUTH (2.7, -2.9) is
# the passage mouth and it is BEHIND the door posts from the clearing, so a walk aimed at it
# slid along a post for 329 frames and never arrived. He fights facing the door, from here.
const DOOR_STOP := Vector2(3.4, -1.6)       # 0.35 m east of the first try: rock_small at
											 # (2.66, -0.98) grazed the approach by 0.14 m
# THE WAY OUT OF THE DOOR GOES EAST FIRST: a scene-list rock_small at (2.66, -0.98) lies 0.10 m
# off the straight line from the door to the drift.
const DOOR_BYPASS := Vector2(3.6, -0.6)
# PER-CLASS SNOW. `mul` scales the depth, `patch` is how much of the class is BARE (compared
# against a noise field, so the bare share is measured afterwards rather than asserted),
# `trod` tints it as walked-on. snow full; path thin and trodden so it reads as a path; rock
# thin and patchy; heather thin and MORE patchy, so its warm tile survives and the tussocks
# stand out of it; ice none, so the tarn stays bare ice.
const SNOW_BY_CLASS := {
	"snow":    {"mul": 1.00, "patch": 0.00, "trod": 0.00},
	"path":    {"mul": 0.36, "patch": 0.12, "trod": 0.85},
	"rock":    {"mul": 0.45, "patch": 0.46, "trod": 0.00},
	"heather": {"mul": 0.22, "patch": 0.70, "trod": 0.00},
	"ice":     {"mul": 0.00, "patch": 0.00, "trod": 0.00},
}

var snow: SnowField
var fog_on := false
var _density_root: Node3D
var _density_report := {}
var _splat_bytes := PackedByteArray()
var _fbm_bytes := PackedByteArray()
var _walk_drift := Vector2.ZERO
var _veil_before := false
var _pending_drifts: Array = []
var _clearing_rejects: Array = []


func _play_rect() -> Rect2:
	"""The walkable area: the painted square plus PLAY_MARGIN_M on every side."""
	return Rect2(_splat_origin - Vector2(PLAY_MARGIN_M, PLAY_MARGIN_M),
				 _splat_size + Vector2(PLAY_MARGIN_M, PLAY_MARGIN_M) * 2.0)


func _build_play_bounds() -> void:
	"""FOUR INVISIBLE WALLS on the ground's own collision layer, so move_and_slide stops him at
	the edge of the dressed land rather than letting him walk into 30 m of empty snow. Invisible
	because the edge is supposed to read as land -- rocks, birches, drifts -- not as a fence;
	the dressing along the boundary is what the eye sees, the wall is what the body meets."""
	var r := _play_rect()
	var body := StaticBody3D.new()
	body.name = "PlayBounds"
	body.collision_layer = BarrowFlat.TERRAIN_BIT
	body.collision_mask = 0
	add_child(body)
	var t := 0.6
	var h := 3.0
	var specs := [
		[Vector3(r.position.x + r.size.x * 0.5, h * 0.5, r.position.y - t * 0.5), Vector3(r.size.x + 2 * t, h, t)],
		[Vector3(r.position.x + r.size.x * 0.5, h * 0.5, r.end.y + t * 0.5), Vector3(r.size.x + 2 * t, h, t)],
		[Vector3(r.position.x - t * 0.5, h * 0.5, r.position.y + r.size.y * 0.5), Vector3(t, h, r.size.y)],
		[Vector3(r.end.x + t * 0.5, h * 0.5, r.position.y + r.size.y * 0.5), Vector3(t, h, r.size.y)],
	]
	for s in specs:
		var cs := CollisionShape3D.new()
		var b := BoxShape3D.new()
		b.size = s[1]
		cs.shape = b
		cs.position = s[0]
		body.add_child(cs)
	report["play_bounds"] = {"rect_xz": [snappedf(r.position.x, 0.01), snappedf(r.position.y, 0.01),
		snappedf(r.size.x, 0.01), snappedf(r.size.y, 0.01)], "margin_m": PLAY_MARGIN_M,
		"walls": 4, "_": "invisible; the dressing is what the eye meets, the wall what the body meets"}


func _splat_w_fast(x: float, z: float) -> PackedFloat32Array:
	"""The five class weights at (x, z) -- snow, path, rock, heather, ice -- off the SAME packed
	weight image the ground shader samples, read as bytes (not Image.get_pixel, which allocates
	a Color per call) and relaxed to pure snow outside the painted square exactly as the shader
	relaxes it."""
	var w := PackedFloat32Array([1.0, 0.0, 0.0, 0.0, 0.0])
	if _splat_bytes.is_empty() or _splat_img == null:
		return w
	var iw := _splat_img.get_width()
	var ih := _splat_img.get_height()
	var u: float = (x - _splat_origin.x) / _splat_size.x
	var v: float = (z - _splat_origin.y) / _splat_size.y
	var dx: float = maxf(maxf(-u, u - 1.0), 0.0) * _splat_size.x
	var dz: float = maxf(maxf(-v, v - 1.0), 0.0) * _splat_size.y
	var t: float = clampf(sqrt(dx * dx + dz * dz) / 6.0, 0.0, 1.0)
	t = t * t * (3.0 - 2.0 * t)
	if t >= 1.0:
		return w
	var px: int = clampi(int(clampf(u, 0.0, 1.0) * float(iw - 1)), 0, iw - 1)
	var pz: int = clampi(int(clampf(v, 0.0, 1.0) * float(ih - 1)), 0, ih - 1)
	var o := (pz * iw + px) * 4
	var f := 1.0 - t
	var r := float(_splat_bytes[o]) / 255.0 * f
	var g := float(_splat_bytes[o + 1]) / 255.0 * f
	var b := float(_splat_bytes[o + 2]) / 255.0 * f
	var a := float(_splat_bytes[o + 3]) / 255.0 * f
	w[1] = r
	w[2] = g
	w[3] = b
	w[4] = a
	w[0] = maxf(1.0 - (r + g + b + a), 0.0)
	return w


func _noise01(x: float, z: float, scale: float, ch := 1) -> float:
	"""The fbm texture's channel `ch` at (x, z) * scale, wrapped, nearest -- off the bytes."""
	if _fbm_bytes.is_empty():
		return 0.5
	var n := 512
	var u := fposmod(x * scale, 1.0)
	var v := fposmod(z * scale, 1.0)
	var i: int = clampi(int(u * float(n)), 0, n - 1)
	var j: int = clampi(int(v * float(n)), 0, n - 1)
	return float(_fbm_bytes[(j * n + i) * 3 + ch]) / 255.0


func _dist_to_seg(p: Vector2, a: Vector2, b: Vector2) -> float:
	var ab := b - a
	var t: float = clampf((p - a).dot(ab) / maxf(ab.length_squared(), 1e-9), 0.0, 1.0)
	return p.distance_to(a + ab * t)


func _in_clear(p: Vector2, pad := 0.0) -> bool:
	"""The combat floor and the two corridors -- to the door, and from the tarn edge."""
	if p.distance_to(COMBAT_C) < COMBAT_R + pad:
		return true
	if _dist_to_seg(p, COMBAT_C, DOOR_MOUTH) < CORRIDOR_R + pad:
		return true
	if _dist_to_seg(p, TARN_EDGE, COMBAT_C) < CORRIDOR_R + pad:
		return true
	if _dist_to_seg(p, WALK_DRIFT, TARN_EDGE) < CORRIDOR_R + pad:
		return true
	if _dist_to_seg(p, DOOR_STOP, DOOR_BYPASS) < CORRIDOR_R + pad:
		return true
	if _dist_to_seg(p, DOOR_BYPASS, WALK_DRIFT) < CORRIDOR_R + pad:
		return true
	if p.distance_to(WALK_DRIFT) < 1.0 + pad:
		return true
	return false


func _clear_zone_discs() -> Array:
	var out := [{"c": COMBAT_C, "r": COMBAT_R}]
	for seg in [[COMBAT_C, DOOR_MOUTH], [TARN_EDGE, COMBAT_C]]:
		# (the return legs are cleared of PROPS in _in_clear but NOT of drifts: the drift is
		# the point of the return leg)
		var a: Vector2 = seg[0]
		var b: Vector2 = seg[1]
		var n: int = maxi(int(ceil(a.distance_to(b) / 0.6)), 1)
		for k in n + 1:
			out.append({"c": a.lerp(b, float(k) / float(n)), "r": CORRIDOR_R})
	return out


func _snow_mask_grid() -> Dictionary:
	"""THE SNOW FOLLOWS THE SPLAT, precomputed on a 0.1 m grid over the painted square and its
	6 m relax band, and handed to SnowField as arrays. Outside it the field is full snow.

	Patchiness is a threshold on an independent noise channel (G, so it does not correlate with
	the ramp's wash in R): a class with patch 0.52 goes BARE wherever the noise is under 0.52,
	with a 0.08 soft edge. fbm is not uniform -- it bunches round 0.5 -- so the bare share each
	class actually gets is MEASURED here and reported, not read off the constant."""
	var cell := 0.1
	var org := _splat_origin - Vector2(6.5, 6.5)
	var size := _splat_size + Vector2(13.0, 13.0)
	var nx := int(ceil(size.x / cell)) + 1
	var nz := int(ceil(size.y / cell)) + 1
	var mul := PackedFloat32Array()
	var trod := PackedFloat32Array()
	mul.resize(nx * nz)
	trod.resize(nx * nz)
	var names: Array = SPLAT_CLASSES
	var cls_cells := [0, 0, 0, 0, 0]
	var cls_bare := [0, 0, 0, 0, 0]
	var cls_mul := [0.0, 0.0, 0.0, 0.0, 0.0]
	for j in nz:
		var z := org.y + float(j) * cell
		for i in nx:
			var x := org.x + float(i) * cell
			var w := _splat_w_fast(x, z)
			var nv := _noise01(x, z, 0.09, 1) * 0.7 + _noise01(x, z, 0.31, 2) * 0.3
			var m := 0.0
			var tr := 0.0
			var top := 0
			for c in 5:
				if w[c] > w[top]:
					top = c
				var spec: Dictionary = SNOW_BY_CLASS[names[c]]
				var keep := smoothstep(float(spec["patch"]) - 0.08, float(spec["patch"]) + 0.08, nv) \
					if float(spec["patch"]) > 0.0 else 1.0
				m += w[c] * float(spec["mul"]) * keep
				tr += w[c] * float(spec["trod"])
			# THE PATH TO THE DOOR is trodden whatever the splat says under it: a corridor the
			# player is meant to take has to look like one, and the painting's path class stops
			# a metre short of the passage.
			# THE TARN IS BARE: ice suppresses the snow faster than its blend weight alone, so
			# the 0.35 m feather of the splat does not leave a skin of snow over the shore ice.
			m *= clampf(1.0 - w[4] * 1.6, 0.0, 1.0)
			var dd := _dist_to_seg(Vector2(x, z), COMBAT_C, DOOR_MOUTH)
			if dd < CORRIDOR_R:
				var k := 1.0 - smoothstep(CORRIDOR_R * 0.55, CORRIDOR_R, dd)
				m = lerpf(m, minf(m, 0.36), k)
				tr = maxf(tr, 0.85 * k)
			mul[j * nx + i] = m
			trod[j * nx + i] = tr
			# the per-class tally, inside the painted square only
			var u := (x - _splat_origin.x) / _splat_size.x
			var v := (z - _splat_origin.y) / _splat_size.y
			if u >= 0.0 and u <= 1.0 and v >= 0.0 and v <= 1.0:
				cls_cells[top] += 1
				cls_mul[top] += m
				if m * 0.12 < 0.015:
					cls_bare[top] += 1
	var per := {}
	for c in 5:
		per[names[c]] = {"cells": cls_cells[c],
			"mean_depth_mul": snappedf(cls_mul[c] / maxf(float(cls_cells[c]), 1.0), 0.001),
			"bare_share_base_layer": snappedf(float(cls_bare[c]) / maxf(float(cls_cells[c]), 1.0), 0.001),
			"spec": SNOW_BY_CLASS[names[c]]}
	report["snow_by_class"] = per
	return {"origin": org, "cell_m": cell, "nx": nx, "nz": nz, "mul": mul, "trod": trod}


# --- density ------------------------------------------------------------------
func _est_radius(cls: String, h: float, man: Dictionary, kit: Dictionary) -> float:
	"""Footprint radius BEFORE placing, to reject overlaps without building and discarding
	nodes. From the manifests' own raw proportions and the same pitch stretch the placement
	applies, so it agrees with the fitted AABB to within the model's own asymmetry."""
	if kit.has(cls):
		return float(kit[cls].get("footprint_radius_m", 0.5)) * (h / maxf(float(kit[cls].get("height_m", h)), 1e-3))
	var s: Dictionary = man.get(cls, {})
	var raw: Array = s.get("raw_aabb_m", [1.0, 1.0, 1.0])
	var py := 1.0 / cos(deg_to_rad(PL_PITCH_DEG)) if bool(s.get("pitch_correct", true)) else 1.0
	var k: float = h / maxf(float(raw[1]) * py, 1e-4)
	return maxf(float(raw[0]), float(raw[2])) * k * 0.5


func _free_at_scaled(p: Vector2, r: float, taken: Array, k: float) -> bool:
	for q in taken:
		if p.distance_to(q["c"]) < (r + float(q["r"])) * k:
			return false
	return true


func _free_at(p: Vector2, r: float, taken: Array, pad: float) -> bool:
	for q in taken:
		if p.distance_to(q["c"]) < r + float(q["r"]) + pad:
			return false
	return true


func _build_density() -> Dictionary:
	"""THE PAINTING'S DRESSING, THEN THE BOUNDARY.

	Inside the painted square the density target is the concept painting itself (the
	coordinator's refinement): every row of data/barrow_dress_a.json -- the outcrops packed
	from rock_large along each painted outcrop's base, the junipers where the growth is dark,
	the heather where it is warm, the dead birches, the fallen trunk -- placed through the same
	_place_prop as the 70, and REJECTED where it would overlap something already standing (the
	70 came from the same painting, so the dress and the list meet at the same outcrops), where
	it would stand on the tarn's ice, or where it would block the combat clearing.

	Outside it, the BOUNDARY: walked at 1.5 m steps, a cluster at most steps, straddling the
	line, with a drift at each -- so the invisible wall is met among rocks and birches, and the
	edge reads as land.

	Deterministic: one seed, so two captures are one scene."""
	var rng := RandomNumberGenerator.new()
	rng.seed = DENSITY_SEED
	var man := {}
	if FileAccess.file_exists(ASSETS_JSON):
		var mj = JSON.parse_string(FileAccess.get_file_as_string(ASSETS_JSON))
		if typeof(mj) == TYPE_DICTIONARY:
			man = mj.get("models", {})
	var kit := {}
	if FileAccess.file_exists("res://data/kit_assets.json"):
		var kj = JSON.parse_string(FileAccess.get_file_as_string("res://data/kit_assets.json"))
		if typeof(kj) == TYPE_DICTIONARY:
			for k in kj.get("models", {}):
				var e: Dictionary = kj["models"][k]
				if String(e.get("status", "")) == "keep" and ResourceLoader.exists(String(e.get("glb", ""))):
					kit[k] = e
	var pitch := 1.0 / cos(deg_to_rad(PL_PITCH_DEG))
	if _density_root == null:
		_density_root = Node3D.new()
		_density_root.name = "Density"
		add_child(_density_root)
	var saved_root := _props_root
	_props_root = _density_root            # _place_prop parents under _props_root

	var taken := []
	for root in [saved_root, _density_root]:
		for nm in prop_names_of(root):
			var n := root.get_node(NodePath(String(nm))) as Node3D
			var rec: Dictionary = _place_report.get(String(nm), {})
			var sz: Array = rec.get("local_size_m", [0.5, 0.5, 0.5])
			taken.append({"c": Vector2(n.global_position.x, n.global_position.z),
						  "r": maxf(float(sz[0]), float(sz[2])) * 0.5})
	taken.append({"c": MOUND_XZ, "r": MOUND_R})
	var pr := _play_rect()
	var ctr := [3000]                      # an Array: a lambda captures an int BY VALUE
	var counts := {"painted": 0, "boundary": 0, "priority": 0}
	var placed_priority := []
	var outcrop_drops := []
	var by_asset := {}
	var skips := {"overlap": 0, "ice": 0, "clearing": 0, "outside": 0, "missing": 0}
	var drifts := []

	var place := func(cls: String, p: Vector2, h: float, yaw: float, tier: String, wm: float) -> bool:
		# the dress calls the kit's heather_clump "heather_base": it is the heather's BODY here
		var kc := "heather_clump" if cls == "heather_base" else cls
		var r := _est_radius(kc, h, man, kit)
		var taken_skip_mound := false
		if tier == "priority":
			# the edge outcrops and the snag: placed FIRST and not rejected for crowding -- they
			# are what the crowded rocks were standing in for
			if _splat_w_fast(p.x, p.y)[4] > 0.6:
				skips["ice"] += 1
				return false
		elif tier == "painted":
			if not pr.has_point(p):
				skips["outside"] += 1
				return false
			if _in_clear(p, 0.0):
				skips["clearing"] += 1
				_clearing_rejects.append({"asset": cls, "xz": [snappedf(p.x, 0.01), snappedf(p.y, 0.01)]})
				return false
			if _splat_w_fast(p.x, p.y)[4] > 0.6:
				skips["ice"] += 1
				return false
			# THE MOUND CARRIES HEATHER: in the painting it is a heather-covered hill with snow
			# on it, and the mound disc in `taken` had kept every tussock off it -- a bare white
			# dome, which is most of why it read as a tent
			if (cls == "heather" or cls == "heather_base") and p.distance_to(MOUND_XZ) < MOUND_R:
				taken_skip_mound = true
			# PAINTED PIECES PACK. An outcrop is rocks touching and overlapping rocks, and heather
			# grows in the gaps between them; the painting's rows come at 0.6-0.75 m spacing and
			# the first test here -- 60% of this footprint against the neighbours' full one --
			# rejected 162 of 250 of them, which is the painting thinned back to T10's sparsity.
			# Rejected now only when two centres nearly coincide: under 45% of their radii summed.
			# SHRUBS GROW AMONG THE ROCKS: in the painting every outcrop is laced with juniper and
			# heather, so a shrub is rejected only when it nearly coincides with something
			var k_pack := 0.25 if (cls in ["juniper", "heather", "heather_base"]) else 0.45
			var against: Array = taken if not taken_skip_mound else taken.filter(
				func(q): return (q["c"] as Vector2) != MOUND_XZ)
			if not _free_at_scaled(p, r, against, k_pack):
				skips["overlap"] += 1
				return false
		else:
			if _in_clear(p, r * 0.5) or _splat_w_fast(p.x, p.y)[4] > 0.25:
				return false
			if not _free_at(p, r, taken, 0.12):
				return false
		var spec: Dictionary = kit[kc] if kit.has(kc) else man.get(cls, {})
		var glb := String(spec.get("glb", "res://models/barrow/%s.glb" % cls))
		if not ResourceLoader.exists(glb):
			skips["missing"] += 1
			return false
		var pc: bool = bool(spec.get("pitch_correct", true)) and not kit.has(kc)
		ctr[0] += 1
		var e := _place_prop(cls, glb, {"pitch_correct": pc, "yaw_deg": yaw,
				"width_m": spec.get("width_m", null), "height_m": spec.get("height_m", h)},
			{}, {"scene_xz": [p.x, p.y], "height_m": h, "yaw_deg": yaw, "width_mul": wm},
			h, false, pitch, int(ctr[0]))
		if e.is_empty():
			return false
		taken.append({"c": p, "r": maxf(float(e["size_m"][0]), float(e["size_m"][2])) * 0.5})
		counts[tier] += 1
		by_asset[cls] = int(by_asset.get(cls, 0)) + 1
		if tier == "priority":
			placed_priority.append({"asset": cls, "c": p,
				"r": maxf(float(e["size_m"][0]), float(e["size_m"][2])) * 0.5, "node": e["node"]})
		return true

	# ---- T10-1d: THE EDGE OUTCROPS AND THE SNAG FIRST ------------------------------------
	for row in _dress:
		var pc2 := String(row.get("asset", ""))
		if not (pc2 in PRIORITY_DRESS):
			continue
		var xz2: Array = row.get("scene_xz", [0.0, 0.0])
		place.call(pc2, Vector2(float(xz2[0]), float(xz2[1])), float(row.get("height_m", 1.0)),
			float(row.get("yaw_deg", 0.0)), "priority", 1.0)
	# THE OUTCROPS REPLACE WHAT WAS PACKED WHERE THEY STAND: a rock the scene list or an earlier
	# pass put inside an outcrop's footprint is dropped -- by name, in the report
	for oc in placed_priority:
		if String(oc["asset"]) != "outcrop_a":
			continue
		for rt in [saved_root, _density_root]:
			for nm2 in prop_names_of(rt):
				var n3 := rt.get_node_or_null(NodePath(String(nm2))) as Node3D
				if n3 == null or n3 == oc["node"]:
					continue
				var a3 := String(_place_report.get(String(nm2), {}).get("asset", ""))
				if not (a3 in ["rock_large", "rock_small"]):
					continue
				var c3 := Vector2(n3.global_position.x, n3.global_position.z)
				if c3.distance_to(oc["c"]) < float(oc["r"]) * 0.85:
					outcrop_drops.append({"prop": String(nm2), "asset": a3,
						"outcrop_xz": [snappedf((oc["c"] as Vector2).x, 0.01), snappedf((oc["c"] as Vector2).y, 0.01)]})
					taken = taken.filter(func(q): return (q["c"] as Vector2).distance_to(c3) > 0.01)
					_drop_prop({"node": n3})

	# ---- THE PAINTING --------------------------------------------------------
	var wanted := {}
	for row in _dress:
		if bool(row.get("priority", false)):
			continue                          # the stones, already placed first
		var cls := String(row.get("asset", ""))
		if cls in PRIORITY_DRESS:
			continue                          # placed above
		wanted[cls] = int(wanted.get(cls, 0)) + 1
		var xz: Array = row.get("scene_xz", [0.0, 0.0])
		var yaw = row.get("yaw_deg", null)
		place.call(cls, Vector2(float(xz[0]), float(xz[1])), float(row.get("height_m", 1.0)),
			float(yaw) if yaw != null else rng.randf() * 360.0, "painted",
			float(row.get("width_mul", 1.0)))

	# ---- the BOUNDARY: dense, straddling the line, with a drift at each cluster ----
	var per := 2.0 * (pr.size.x + pr.size.y)
	var steps := int(per / 1.5)
	# T10-1d: the kit's outcrop where the boundary had rock_large clusters (they read as shards),
	# and its boulder, three-rock cluster, stump and dead tree among the rest
	var pool := ["outcrop_a", "rock_small", "boulder", "birch", "juniper", "rocks",
				 "dead_tree", "log", "cairn", "outcrop_a", "juniper", "stump"]
	for s2 in steps:
		var along := float(s2) / float(steps) * per
		var edge_p: Vector2
		var inward: Vector2
		if along < pr.size.x:
			edge_p = Vector2(pr.position.x + along, pr.position.y)
			inward = Vector2(0, 1)
		elif along < pr.size.x + pr.size.y:
			edge_p = Vector2(pr.end.x, pr.position.y + (along - pr.size.x))
			inward = Vector2(-1, 0)
		elif along < 2.0 * pr.size.x + pr.size.y:
			edge_p = Vector2(pr.end.x - (along - pr.size.x - pr.size.y), pr.end.y)
			inward = Vector2(0, -1)
		else:
			edge_p = Vector2(pr.position.x, pr.end.y - (along - 2.0 * pr.size.x - pr.size.y))
			inward = Vector2(1, 0)
		if rng.randf() > 0.8:
			continue
		var tangent := Vector2(inward.y, -inward.x)
		var base := edge_p + inward * rng.randf_range(-0.5, 0.9) + tangent * rng.randf_range(-0.5, 0.5)
		for k2 in rng.randi_range(1, 3):
			var cls3: String = pool[rng.randi() % pool.size()]
			if not kit.has(cls3) and not man.has(cls3):
				continue
			var off := Vector2(rng.randf_range(-0.8, 0.8), rng.randf_range(-0.8, 0.8))
			var hh3: float
			match cls3:
				# the outcrop at a third to a half of its 2.29 m: 1.7-2.5 m across the boundary
				"outcrop_a": hh3 = 2.2888 * rng.randf_range(0.30, 0.50)
				"dead_tree": hh3 = 2.5 * rng.randf_range(0.85, 1.15)
				"rock_large": hh3 = rng.randf_range(0.9, 1.6) * rng.randf_range(0.85, 1.15)
				"rock_small": hh3 = rng.randf_range(0.35, 0.75) * rng.randf_range(0.85, 1.15)
				"birch": hh3 = rng.randf_range(2.2, 3.4)
				"juniper": hh3 = rng.randf_range(0.8, 1.3)
				_: hh3 = float(kit.get(cls3, {}).get("height_m", 1.0)) * rng.randf_range(0.92, 1.08)
			place.call(cls3, base + off, hh3, rng.randf() * 360.0, "boundary", 1.0)
		drifts.append({"c": base - inward * 0.4, "r": rng.randf_range(1.0, 1.7),
					   "h": rng.randf_range(0.28, 0.55), "squash": rng.randf_range(1.2, 2.0),
					   "rot": atan2(tangent.y, tangent.x)})

	_props_root = saved_root
	_density_report = {"seed": DENSITY_SEED, "placed": counts, "by_asset": by_asset,
		"painted_rows_wanted": wanted, "painted_rows_skipped": skips,
		"clearing_rejects": _clearing_rejects,
		"boundary_drifts": drifts.size(), "kit_used": kit.keys(),
		"priority_placed": placed_priority.map(func(q): return {"asset": q["asset"],
			"xz": [snappedf((q["c"] as Vector2).x, 0.01), snappedf((q["c"] as Vector2).y, 0.01)],
			"footprint_r_m": snappedf(float(q["r"]), 0.01)}),
		"rocks_dropped_under_outcrops": outcrop_drops}
	report["density"] = _density_report
	return {"drifts": drifts}


func prop_names_of(root: Node) -> Array:
	var o := []
	if root != null:
		for c in root.get_children():
			o.append(String((c as Node).name))
	return o


func _build_snow() -> void:
	"""THE SNOW FIELD: every ground-standing prop is an obstacle, radius from its FITTED AABB,
	and the mound is one too; the depth follows the splat; the combat floor and the corridors
	take no open-ground drift; the boundary takes the drifts _build_density laid out; and one
	deliberate drift lies across the return route from the door, so the walk goes through it."""
	var t0 := Time.get_ticks_msec()
	snow = SnowField.new()
	snow.name = "SnowField"
	snow.fbm_tex = fbm
	snow.snow_tint = SNOW_TINT
	snow.depth_grid = _snow_mask_grid()
	snow.clear_zones = _clear_zone_discs()
	var drifts: Array = _pending_drifts.duplicate()
	# THE WALK'S DRIFT, at its fixed waypoint (see WALK_DRIFT): the return leg wades it.
	_walk_drift = WALK_DRIFT
	# UNMASKED: it lies on the painting's path class, where the splat mask would thin any drift
	# to a third -- and a drift he does not have to wade is not the drift the walk is for
	drifts.append({"c": _walk_drift, "r": 1.25, "h": 0.55, "squash": 1.5,
				   "rot": atan2(WIND.y, WIND.x), "unmasked": true})
	snow.extra_piles = drifts
	var obstacles := []
	for root in [_props_root, _density_root]:
		if root == null:
			continue
		for n in root.get_children():
			var node := n as Node3D
			var rec: Dictionary = _place_report.get(String(node.name), {})
			if String(rec.get("asset", "")) in ["raven", "heather", "heather_base"] or rec.is_empty():
				# HEATHER IS NOT AN OBSTACLE (T10-1c). A skirt round every tussock laid 0.12 m of
				# snow over the base of each and turned heather ground into lumpy white; the
				# painting's heather stands in thin snow with its warm tops showing, which is what
				# the heather class's own depth mask already gives it.
				continue
			var sz: Array = rec.get("local_size_m", [0.5, 0.5, 0.5])
			obstacles.append({"pos": node.global_position,
							  "radius_m": maxf(float(sz[0]), float(sz[2])) * 0.5,
							  "height_m": float(sz[1])})
	obstacles.append({"pos": Vector3(MOUND_XZ.x, 0.0, MOUND_XZ.y), "radius_m": MOUND_R,
					  "height_m": MOUND_RISE})
	# THE WARM TOPS SHOWING: each heather clump in a scoop of thin snow, capped at
	# HEATHER_SNOW_FRAC of its own height (SnowField.thin_zones)
	var thin := []
	for root in [_props_root, _density_root]:
		if root == null:
			continue
		for n in root.get_children():
			var node := n as Node3D
			var rec: Dictionary = _place_report.get(String(node.name), {})
			if not (String(rec.get("asset", "")) in ["heather", "heather_base"]):
				continue
			var sz: Array = rec.get("local_size_m", [0.4, 0.35, 0.4])
			thin.append({"c": Vector2(node.global_position.x, node.global_position.z),
						 "r": maxf(float(sz[0]), float(sz[2])) * 0.5 * 0.8, "feather": 0.18,
						 "max_d": float(sz[1]) * HEATHER_SNOW_FRAC})
	snow.thin_zones = thin
	var pr := _play_rect()
	var ctr := pr.get_center()
	snow.setup(Rect2(ctr - Vector2(SNOW_AREA_M, SNOW_AREA_M) * 0.5, Vector2(SNOW_AREA_M, SNOW_AREA_M)),
			   0.0, obstacles, WIND)
	add_child(snow)
	if knight != null:
		snow.track(knight)
	for k in _heather_mats:
		BarrowHeather.bind_snow(_heather_mats[k], snow, WIND)
	_ground_mat.set_shader_parameter("snow_amount", 0.0)
	var br := snow.bake_report()
	br["obstacles"] = obstacles.size()
	br["walk_drift_xz"] = [snappedf(_walk_drift.x, 0.01), snappedf(_walk_drift.y, 0.01)]
	br["walk_drift_depth_m"] = snappedf(snow.depth_at(_walk_drift), 0.001)
	br["build_ms"] = Time.get_ticks_msec() - t0
	br["area_xz"] = [snappedf(ctr.x - SNOW_AREA_M * 0.5, 0.01), snappedf(ctr.y - SNOW_AREA_M * 0.5, 0.01),
					 SNOW_AREA_M, SNOW_AREA_M]
	report["snow_field"] = br


# --- the A/B hooks ------------------------------------------------------------------
func set_veil_before(on: bool) -> void:
	"""THE 17:20 LOOK, for the before/after: the ground's own FBM snow blend back on, the 3D
	snow field hidden, and the height fog as it shipped. Everything else -- pose, camera, grade,
	pens, props -- identical, so the pair isolates exactly the veil."""
	_veil_before = on
	if _ground_mat != null:
		_ground_mat.set_shader_parameter("snow_amount", 1.0 if on else (0.0 if snow != null else 1.0))
	if snow != null:
		snow.set_visible_snow(not on)
	fog_on = on
	_apply_stack()


func set_snowfield_visible(on: bool) -> void:
	if snow != null:
		snow.set_visible_snow(on)


func set_density_visible(on: bool) -> void:
	"""The dressing on or off, for the cost attribution: EVERY repeated prop (all instanced
	classes, scene list included) plus the density root's own nodes (the painted stones). The
	same set is removed whether the props are drawn as MultiMeshes or one node each -- the
	per-instance cost comparison is a subtraction over one set, or it is not a comparison."""
	_density_visible = on
	if _density_root != null:
		_density_root.visible = on
	_apply_draw_mode()


func body_centroid() -> Vector3:
	"""WHERE HIS BODY IS, which is not always where his node is.

	Measured this pass (tools/drax_pos.gd): in the unarmed idle his Hips sit 0.02 m from his
	node; in the ARMED idle -- full kit, no input, his own physics loop -- they sit 1.35 m away
	in +z and 0.2 m higher, and stay there. It is inside the armed animation in knight.gd, which
	this seam does not edit. It is also why last pass's stills had him up-left of where he
	stood. So the captures aim at, and place, THIS -- the centroid of his bones -- rather than
	the node, and report the offset."""
	if knight == null:
		return Vector3.ZERO
	var acc := Vector3.ZERO
	var n := 0
	for s in knight.find_children("*", "Skeleton3D", true, false):
		var sk := s as Skeleton3D
		for b in sk.get_bone_count():
			acc += sk.global_transform * sk.get_bone_global_pose(b).origin
			n += 1
	return acc / float(maxi(n, 1)) if n > 0 else knight.global_position


# heather is SHRUB for coverage, but gets its own colour (magenta) so its rendered colour can
# be sampled apart from the junipers' -- the warmth measurement needs heather alone
const ID_COLOURS := {"stone": Color(1, 0, 0), "rock": Color(0, 1, 0), "shrub": Color(0, 0, 1),
					 "tree": Color(1, 1, 0), "heather": Color(1, 0, 1)}
const ID_CLASS := {"stone_tall": "stone", "stone_mid": "stone", "stone_short": "stone",
				   "lintel": "stone", "post": "stone", "rock_large": "rock", "rock_small": "rock",
				   "cairn": "rock", "juniper": "shrub", "heather": "heather", "birch": "tree",
				   "log": "tree",
				   # T10-1d kit: the skull is in no painted class -- an occluder, not a class
				   "outcrop_a": "rock", "boulder": "rock", "rocks": "rock", "heather_base": "heather",
				   "dead_tree": "tree", "stump": "tree"}
var _id_saved := []


func set_class_id_view(on: bool, occluders := false) -> void:
	"""THE COVERAGE INSTRUMENT'S RENDER: every prop in its class colour, unshaded, on black,
	and nothing else -- no ground, no snow, no mound, no him, no pens, no grade. The painting is
	segmented into the same four classes once (tools/barrow_paint_dress.py), and the coverage of
	a class is the share of the painting's pixels of that class that a 3D object of that class
	covers in this frame. Every change is recorded with an explicit kind and restored exactly."""
	if on:
		_id_saved.clear()
		for root in [_props_root, _density_root]:
			if root == null:
				continue
			for nm in prop_names_of(root):
				var node := root.get_node(NodePath(String(nm))) as Node3D
				var cls := String(ID_CLASS.get(String(_place_report.get(String(nm), {}).get("asset", "")), ""))
				for mi in node.find_children("*", "MeshInstance3D", true, false):
					var m := mi as MeshInstance3D
					_id_saved.append({"kind": "mesh", "n": m, "mat": m.material_override, "vis": m.visible})
					if _instancing_on and (_hidden_meshes.has(m) or _instanced_inks.has(m)):
						m.visible = false
						continue
					if String(m.name).ends_with("_ink"):
						m.visible = false
						continue
					if cls == "":
						# IN NO PAINTED CLASS (the skull): in the occluded frame it still hides what
						# is behind it, so it is drawn black; in the T10-1b frame it is left out
						if occluders:
							m.material_override = _id_black()
						else:
							m.visible = false
						continue
					m.material_override = _id_material(cls, String(m.name) == "HeatherCard")
		for mmi in _mmis:
			var mm := mmi as MultiMeshInstance3D
			var cls2 := String(ID_CLASS.get(String(mm.get_meta("asset", "")), ""))
			_id_saved.append({"kind": "mesh", "n": mm, "mat": mm.material_override, "vis": mm.visible})
			if cls2 == "":
				if occluders:
					mm.material_override = _id_black()
				else:
					mm.visible = false
				continue
			mm.material_override = _id_material(cls2, String(mm.get_meta("part", "")) == "cards")
		for l in _mm_inks:
			_id_saved.append({"kind": "node", "n": l, "vis": (l as Node3D).visible})
			(l as Node3D).visible = false
		# OCCLUDERS (T10-1c): with `occluders` the ground, the mound, the snow and him are drawn
		# BLACK instead of hidden -- so a prop's pixels are the ones the eye can see, not the
		# ones under a snowdrift. Without it, the T10-1b instrument, kept for continuity: the
		# heather's buried bases counted as heather, and its "colour" was sampled from snow.
		var hide := [snowfall, gust, post_q]
		if not occluders:
			hide.append_array([knight, _mound, snow])
			hide.append_array(find_children("BarrowGround", "MeshInstance3D", true, false))
		else:
			var black := _id_black()
			var occ := []
			if _mound != null:
				occ.append(_mound)
			occ.append_array(find_children("BarrowGround", "MeshInstance3D", true, false))
			if knight != null:
				occ.append_array(knight.find_children("*", "MeshInstance3D", true, false))
			for o in occ:
				var g := o as GeometryInstance3D
				_id_saved.append({"kind": "mesh", "n": g, "mat": g.material_override, "vis": g.visible})
				if String(g.name).ends_with("_ink") or String(g.name) == "InkLine":
					g.visible = false
				else:
					g.material_override = black
			if snow != null:
				snow.set_id_black(true)
				_id_saved.append({"kind": "snow_black"})
		for n in hide:
			if n != null:
				_id_saved.append({"kind": "node", "n": n, "vis": (n as Node3D).visible})
				(n as Node3D).visible = false
		var env := env_node.environment
		_id_saved.append({"kind": "env", "bg": env.background_mode, "col": env.background_color,
						  "fog": env.fog_enabled})
		env.background_mode = Environment.BG_COLOR
		env.background_color = Color(0, 0, 0)
		env.fog_enabled = false
	else:
		for s in _id_saved:
			match String(s["kind"]):
				"mesh":
					(s["n"] as GeometryInstance3D).material_override = s["mat"]
					(s["n"] as Node3D).visible = bool(s["vis"])
				"node":
					(s["n"] as Node3D).visible = bool(s["vis"])
				"snow_black":
					if snow != null:
						snow.set_id_black(false)
				"env":
					var env := env_node.environment
					env.background_mode = s["bg"]
					env.background_color = s["col"]
					env.fog_enabled = s["fog"]
		_id_saved.clear()


# A CARD'S ID IS ITS CLASS COLOUR IN ITS OWN ALPHA: a plain StandardMaterial3D would either
# fill the whole quad (no scissor) or multiply the class colour by the painting's pixels
const ID_CARD_SHADER := """
shader_type spatial;
render_mode unshaded, cull_disabled, shadows_disabled;
uniform sampler2D card_tex : filter_linear_mipmap;
uniform vec3 id_col = vec3(1.0, 0.0, 1.0);
void fragment() {
	ALBEDO = id_col;
	ALPHA = texture(card_tex, UV).a;
	ALPHA_SCISSOR_THRESHOLD = 0.5;
}
"""
var _id_mats := {}
var _id_card_shader: Shader


func _id_material(cls: String, card: bool) -> Material:
	var key := cls + ("|card" if card else "")
	if _id_mats.has(key):
		return _id_mats[key]
	var c: Color = ID_COLOURS[cls]
	var m: Material
	if card:
		if _id_card_shader == null:
			_id_card_shader = Shader.new()
			_id_card_shader.code = ID_CARD_SHADER
		var sm := ShaderMaterial.new()
		sm.shader = _id_card_shader
		sm.set_shader_parameter("card_tex", _heather_card_tex)
		sm.set_shader_parameter("id_col", Vector3(c.r, c.g, c.b))
		m = sm
	else:
		var st := StandardMaterial3D.new()
		st.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		st.albedo_color = c
		if cls == "heather" and heather_two_sided and heather_mode == "blobs":
			st.cull_mode = BaseMaterial3D.CULL_DISABLED      # as the beauty draws it
		m = st
	_id_mats[key] = m
	return m


func _id_black() -> StandardMaterial3D:
	if not _id_mats.has("_black"):
		var b := StandardMaterial3D.new()
		b.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		b.albedo_color = Color(0, 0, 0)
		_id_mats["_black"] = b
	return _id_mats["_black"]


func walk_waypoints() -> Dictionary:
	return {"tarn_edge": TARN_EDGE, "door": DOOR_STOP, "drift": _walk_drift,
			"combat_c": COMBAT_C, "bypass": DOOR_BYPASS,
			"route": _route(),
			"fight_at": _route().find(DOOR_STOP),
			"unreached": _route_unreached}


func _route() -> Array:
	"""On the ice, through the first opened shore gap, the clearing, the door (the fight),
	east round the rock at the threshold, the drift, and back out onto the ice through the
	second gap -- or the T10-1b route if the shore could not be opened."""
	if not _route_cache.is_empty():
		return _route_cache
	var base: Array
	if _shore_route.size() < 2:
		base = [TARN_EDGE, COMBAT_C, DOOR_STOP, DOOR_BYPASS, _walk_drift, TARN_EDGE]
	else:
		var g1: Dictionary = _shore_route[0]
		var g2: Dictionary = _shore_route[1]
		# on the ice at the first gap, out onto the ice at the second: the grid chooses the
		# way through each, since the shore is otherwise a wall
		base = [g1["a"], COMBAT_C, DOOR_STOP, DOOR_BYPASS, _walk_drift, g2["a"]]
	# EVERY LEG IS CHECKED AGAINST THE COLLIDERS, and a blocked one gets a detour found by
	# search rather than a waypoint typed in: the dressing is dense and deterministic, and a
	# hand-placed waypoint is right for exactly one placement of it.
	# EACH LEG IS A PATH ON THE NAVIGATION GRID, string-pulled back to the fewest waypoints
	# that keep line of sight -- so a leg that would clip a rock bends round it, and a leg the
	# grid cannot complete is reported rather than walked into a wall.
	var g := _nav_grid(_collider_list())
	var out := [base[0]]
	_route_unreached = []
	for i in range(1, base.size()):
		var a: Vector2 = out[out.size() - 1]
		var b: Vector2 = base[i]
		if _leg_clearance(a, b) >= 0.05:
			out.append(b)
			continue
		var path := _nav_path(g, a, b)
		if path.is_empty():
			_route_unreached.append([snappedf(b.x, 0.01), snappedf(b.y, 0.01)])
			out.append(b)
			continue
		var k := 0
		while k < path.size() - 1:
			var far := k + 1
			for j in range(path.size() - 1, k, -1):
				if _leg_clearance(path[k], path[j]) >= 0.02:
					far = j
					break
			if far < path.size() - 1:
				out.append(path[far])
			k = far
		out.append(b)
	_route_cache = out
	return out


var _route_unreached: Array = []


var _route_cache: Array = []
var _colliders_cache: Array = []


func _colliders() -> Array:
	if not _colliders_cache.is_empty():
		return _colliders_cache
	for root in [_props_root, _density_root]:
		if root == null:
			continue
		for c in root.get_children():
			var node := c as Node3D
			var rec: Dictionary = _place_report.get(String(node.name), {})
			if String(rec.get("asset", "")) in ["heather", "raven", ""]:
				continue
			var sz: Array = rec.get("local_size_m", [0.4, 0.4, 0.4])
			_colliders_cache.append({"p": Vector2(node.global_position.x, node.global_position.z),
									 "r": maxf(float(sz[0]), float(sz[2])) * 0.42})
	_colliders_cache.append({"p": MOUND_XZ, "r": MOUND_R})
	return _colliders_cache


func _leg_clearance(a: Vector2, b: Vector2) -> float:
	"""Metres between his capsule (0.35 m radius) and the nearest collider along a leg."""
	var worst := 99.0
	for c in _colliders():
		worst = minf(worst, _dist_to_seg(c["p"], a, b) - float(c["r"]) - 0.35)
	return worst


func _detour(a: Vector2, b: Vector2) -> Vector2:
	"""The via point, on a 0.25 m grid within 2.5 m of the leg's midpoint, that maximises the
	worse of its two sub-legs' clearances -- INF if none clears."""
	var mid := (a + b) * 0.5
	var best := Vector2.INF
	var best_c := 0.05
	for j in range(-10, 11):
		for i in range(-10, 11):
			var v := mid + Vector2(float(i), float(j)) * 0.25
			if not _play_rect().has_point(v):
				continue
			var c := minf(_leg_clearance(a, v), _leg_clearance(v, b))
			if c > best_c:
				best_c = c
				best = v
	return best


# =============================================================================
#  T10-1c — INSTANCING, LOW ROCKS, WARMTH, THE SHORE
# =============================================================================
const INSTANCED := ["heather", "juniper", "rock_small", "rock_large", "birch", "log", "cairn", "shield",
					"heather_base", "outcrop_a", "dead_tree", "boulder", "rocks", "stump", "skull"]
# triangle targets for the instanced copies (BarrowInstancer.decimate); heather is not reduced
# -- it is 544 triangles and the point this pass is to make it DENSER, not sparser
const LOD_TARGETS := {"rock_small": 700, "rock_large": 1400, "juniper": 2400, "birch": 4000,
					  "heather": 100000, "log": 1500, "cairn": 1500, "shield": 1500,
					  "heather_base": 1500, "outcrop_a": 3000, "dead_tree": 2500, "boulder": 1200,
					  "rocks": 1500, "stump": 1200, "skull": 1500}
const CHUNK_M := 7.0
# THE HEATHER'S CHUNK IS THE WHOLE PLAY AREA (T10-1d): 493 tufts in 10 variants over 7 m chunks
# were 87 MultiMeshes -- 87 draws in each of four passes, for ~5 copies apiece -- and the
# heather cost 2.3 ms whatever its triangle count (cutting stems by a third moved nothing).
const CHUNK_BY_ASSET := {"heather": 24.0}
# NO UPRIGHT ROCK CROWDS. The acceptance is 0 non-ring rocks taller than 1.2 m within 10 m of
# the ring; the rocks are laid to 1.1 m at most so the jitter cannot reach it.
const ROCK_MAX_H := 1.2
const ROCK_LOW_H := 0.85
# THE LIT SNOW, GRADED ONTO THE PAINTING'S. Sampled, not chosen: the painting's lit snow is
# Lab (91.79, 2.10, 9.97) and the T10-1b render's was (88.90, 3.77, 13.50) -- dE 4.85, inside
# the 5 the coordinator asked for by a hair, and wrong in the direction Matt's eye caught:
# darker and yellower ("cream"). Per-channel ratio of the two in LINEAR light.
const SNOW_TINT := Color(1.026, 1.101, 1.174)
# THE HEATHER, pulled onto the painting's heather: Lab (45.41, 11.13, 24.01), a saturated rust.
# Per-channel ratio in LINEAR light, painting over render, multiplied into the tint -- with the
# render side measured on the heather the eye can SEE (the occluded ID frame). The first tint,
# (0.68, 0.544, 0.384), was derived from pixels that were mostly snow over buried sprigs, so it
# corrected the snow. Iterated on the visible pixels, one change measured at a time:
#   bodies under the clumps     render Lab (40.11, 7.07, 4.96)    dE 20.2 -> tint (1.114, 0.670, 0.233)
#   + hard shadows, that tint   render Lab (42.58, 13.54, 18.87)  dE 6.35
#   + snow scoops, that tint    render Lab (41.86, 13.88, 20.04)  dE 6.00 -> tint below
const HEATHER_TINT := Vector3(1.249, 0.840, 0.243)
# the painting's juniper: Lab (28.03, 5.42, 5.81), a dark olive. Same derivation, visible pixels:
#   first measured              render Lab (37.03, 4.36, -6.88) -- the ramp's blue-violet shadow
#                               on a pale texture -- dE 15.7 -> tint (0.330, 0.211, 0.161)
#   + scoops, that tint         render Lab (29.41, 4.95, -2.25)   dE 8.19 -> (0.350, 0.188, 0.101)
#   that tint                   render Lab (28.87, 5.82, 0.54)    dE 5.34
# and the ratio stops converging on BLUE, because blue is not all albedo: two tints give two
# rendered values, and the line through them (render_b = 0.0406 + 0.16 * tint_b) says 0.041 of
# the juniper's blue comes from what is round it -- blue-shadowed snow in the edge pixels, the
# wash -- whatever its own colour. Fitted per channel on that line instead of by ratio:
const JUNIPER_TINT := Vector3(0.354, 0.163, 0.020)
# a heather "clump" is tussocks turned 40 degrees apart and offset, over a body (HEATHER_CORE):
# one tussock is 544 triangles of blades a pixel wide at the play camera, and alone it reads as
# a pale scribble over the snow behind it. Extra meshes under the SAME prop, so the node and
# instanced versions draw identical content and the A/B stays honest.
# 4 -> 2 once the body carried the mass: the blades had become the frame's biggest line --
# 2,020 tussocks, 2.42 ms of 17.87 (probe_cost, asset_inst_no_heather) -- for a fringe.
const HEATHER_CLUMP := 2
# THE CLUMP'S BODY. Tussocks of pixel-wide blades cannot hold a colour: at the painting's
# framing the heather the eye could see came back cool grey, Lab (45.6, 4.0, -2.3), 0.2% of it
# warm by the painting's own rule, while its texture is rust (Lab 56, 9, 21) -- thin blades
# over bright snow under 4x MSAA, lit mostly by the ramp's blue-violet shadow band. The
# painting's tufts are a MASS of rust with sprigs at the edge. So
# each clump gets a low lumpy dome of the tussock's own painted texture, under the blades:
# CORE_W of the clump's width, CORE_H of its height, base on the tussocks' base. Same
# material, same tint, same snow rule as the blades -- one more instance per clump.
# (exported so a probe can build the T10-1b-shaped heather in the same code for a baseline)
@export var heather_core := true
# TWO-SIDED BLADES: OFF, measured. Drawn two-sided, the blades turned away from the camera come
# back (the GLB authors them doubleSided) -- worth it while the blades were the only thing
# carrying the heather's colour, and +0.46 to +0.58 ms of frame (probe_cost,
# diag_heather_one_sided, three runs) once the bodies carry it. The fringe halves; the warm
# read does not move (visible-pixel dE measured both ways). Left as a switch, not deleted.
@export var heather_two_sided := false
# T10-1d: THE HEATHER'S REPRESENTATION. "stems": generated sprig sprays (BarrowHeather);
# "cards": the painting's own tufts cut out as alpha cards (tools/barrow_heather_cards.py);
# "blobs": T10-1c's tussocks over a body, kept for the before/after. Chosen by measurement.
@export var heather_mode := "stems"
# build BOTH stems and cards on every clump with one set hidden: the in-run A/B for the choice
@export var heather_ab := false
# the fill outside the painting: "patches" (T10-1d) or "even" (T10-1c's grid), for the A/B
@export var heather_fill := "patches"
const HEATHER_CARDS_JSON := "res://data/heather_cards.json"
const HEATHER_CARDS_PNG := "res://textures/barrow/heather_cards.png"
# the grade on each representation's albedo: the per-channel LINEAR ratio of the painting's
# heather (Lab 45.41, 11.13, 24.01, rust pixels) to the render's visible heather pixels,
# multiplied in and re-measured: stems (1,1,1) dE 13.2 -> (1.371, 1.109, 0.702) 3.8 ->
# darker stem bases, (1.489, 1.182, 0.616) 4.7 -> leaner sprays 4.9 -> below; cards (1,1,1)
# 15.8 -> (1.408, 1.130, 0.638) 1.2
const HEATHER_STEM_MUL := Vector3(1.622, 1.254, 0.534)
const HEATHER_CARD_MUL := Vector3(1.408, 1.130, 0.638)
var _heather_mats := {}
var _heather_cards: Array = []
var _heather_card_tex: Texture2D
var _heather_rep := ""
const CORE_W := 0.56
const CORE_H := 0.58
# THE HANDOFF'S HEATHER ROWS ARE PATCHES, NOT PLANTS. barrow_scene_a.json lists 19 "heather"
# at 0.81-2.19 m: the measured extent of a heather REGION in the painting. Sized as one tussock
# each, they were 2 m sprays of blades (read as dead bushes); given a body under the blades,
# 53 of them became 1-2.7 m brown mounds (measured, drax_dbg_core). A row over this height is
# drawn as a patch of painting-scale clumps over its measured extent instead.
const HEATHER_PATCH_ABOVE_M := 0.6
# the directional shadow filter this scene runs with (see _build_light_and_air)
const SHADOW_FILTER_T10_1D := RenderingServer.SHADOW_QUALITY_SOFT_MEDIUM
# dress rows placed first and never rejected for crowding (T10-1d)
const PRIORITY_DRESS := ["outcrop_a", "dead_tree"]
# the snow at a heather clump, at most this share of the clump's height (see _build_snow)
const HEATHER_SNOW_FRAC := 0.2
const PATCH_CLUMP_M := 0.28
static var _core_mesh: ArrayMesh
const SHORE_GAP_M := 1.2

@export var use_instancing := true
var _instanced_root: Node3D
var _mmis: Array = []
var _mm_inks: Array = []
var _mm_members := {}
var _instanced_inks := {}
var _hidden_meshes: Array = []
var _instancing_on := false
var _rock_up := {}
var _rock_pose_up := false
var _shore_moves: Array = []
var _shore_route: Array = []
var _fill_report := {}


func _lay_rocks_low() -> Dictionary:
	"""EVERY rock_large ON ITS SIDE, AT MOST 1.1 m, SUNK. The painting's outcrops are low layered
	slabs; packed upright, rock_large read as a crowd of extra standing stones and the ring was
	lost in it. Until an outcrop model exists (held on budget) the same model is tipped 78-102
	degrees onto its side -- the pitch stretch applied in MODEL space first, so the stretched
	axis stays the model's own height and does not become a length -- sized to the lower of 70%
	of its painted height and 1.1 m, and sunk 12% of that into the ground so it reads as bedrock
	breaking the surface rather than a boulder set on it. rock_small is already low and is only
	checked. The upright pose is RECORDED first, for the before/after."""
	var rng := RandomNumberGenerator.new()
	rng.seed = 8813
	var pitch := 1.0 / cos(deg_to_rad(PL_PITCH_DEG))
	var n := 0
	for root in [_props_root, _density_root]:
		if root == null:
			continue
		for c in root.get_children():
			var node := c as Node3D
			var rec: Dictionary = _place_report.get(String(node.name), {})
			if String(rec.get("asset", "")) != "rock_large":
				continue
			var fit := node.get_node_or_null("fit") as Node3D
			if fit == null or fit.get_child_count() == 0:
				continue
			var ups := []
			for mi in node.find_children("*", "MeshInstance3D", true, false):
				if not String(mi.name).ends_with("_ink"):
					ups.append((mi as MeshInstance3D).global_transform)
			_rock_up[String(node.name)] = ups
			var glb := fit.get_child(0) as Node3D
			fit.remove_child(glb)
			var lie := Node3D.new()
			lie.name = "lie"
			var stretch := Node3D.new()
			stretch.name = "stretch"
			fit.add_child(lie)
			lie.add_child(stretch)
			stretch.add_child(glb)
			# CHUNKIER: the pitch stretch is 1.66 on the model's height; laid down that height is a
			# LENGTH, and at the full stretch each slab came out 2:1 -- a fallen pillar, which is
			# the one thing an outcrop must not look like next to a stone ring
			stretch.scale = Vector3(1.0, pitch * 0.62, 1.0)
			lie.rotation = Vector3(deg_to_rad(rng.randf_range(80.0, 100.0)), 0.0,
								   deg_to_rad(rng.randf_range(-8.0, 8.0)))
			# STRATA: every slab in a 3 m cell shares one bearing, +-12 degrees, so a cluster
			# reads as layered bedrock rather than a spill of pieces crossing each other
			var cell_seed: int = int(floor(node.global_position.x / 3.0)) * 7919 \
				+ int(floor(node.global_position.z / 3.0)) * 104729
			node.rotation.y = deg_to_rad(float(absi(cell_seed) % 180) + rng.randf_range(-12.0, 12.0))
			fit.scale = Vector3.ONE
			fit.position = Vector3.ZERO
			var raw := _node_aabb(node)
			var want: float = minf(float(rec.get("target_m", 1.0)) * rng.randf_range(0.45, 0.65), ROCK_LOW_H)
			want = maxf(want, 0.3)
			var k: float = want / maxf(raw.size.y, 1e-6)
			fit.scale = Vector3(k, k, k)
			var b := _node_aabb(node)
			fit.position = Vector3(-(b.position.x + b.size.x * 0.5), -b.position.y,
								   -(b.position.z + b.size.z * 0.5))
			var fin := _node_aabb(node)
			var xz := Vector2(node.global_position.x, node.global_position.z)
			var g := _ground_under(xz.x, xz.y, maxf(fin.size.x, fin.size.z) * 0.5)
			node.global_position = Vector3(xz.x, float(g["lo"]) - PROP_SINK_M - 0.12 * fin.size.y, xz.y)
			var body := node.get_node_or_null("obstacle") as StaticBody3D
			if body != null and body.get_child_count() > 0:
				var cs := body.get_child(0) as CollisionShape3D
				var cy := cs.shape as CylinderShape3D
				if cy != null:
					cy.radius = maxf(maxf(fin.size.x, fin.size.z) * 0.42, 0.08)
					cy.height = maxf(fin.size.y, 0.2)
					cs.position = Vector3(0.0, cy.height * 0.5, 0.0)
			rec["local_size_m"] = [snappedf(fin.size.x, 0.001), snappedf(fin.size.y, 0.001),
								   snappedf(fin.size.z, 0.001)]
			rec["target_m"] = snappedf(want, 0.001)
			rec["laid_low"] = true
			_place_report[String(node.name)] = rec
			n += 1
	return {"rock_large_laid_low": n}


func rock_height_check() -> Dictionary:
	"""THE ACCEPTANCE: non-ring rocks taller than 1.2 m within 10 m of the ring. The ring is
	every megalith actually built (scene list and painted); a rock's height is its built local
	bounding height above its own base, which for a sunk rock over-states what shows."""
	var ring := []
	var rocks := []
	for root in [_props_root, _density_root]:
		if root == null:
			continue
		for c in root.get_children():
			var node := c as Node3D
			var rec: Dictionary = _place_report.get(String(node.name), {})
			var a := String(rec.get("asset", ""))
			var p := Vector2(node.global_position.x, node.global_position.z)
			if a in MEGALITH:
				ring.append(p)
			elif a in ["rock_large", "rock_small", "cairn"]:
				rocks.append({"name": String(node.name), "p": p,
							  "h": float(rec.get("local_size_m", [0, 0, 0])[1])})
	var bad := []
	var tallest := 0.0
	for r in rocks:
		var d := 1e9
		for q in ring:
			d = minf(d, (r["p"] as Vector2).distance_to(q))
		if d <= 10.0:
			tallest = maxf(tallest, float(r["h"]))
			if float(r["h"]) > ROCK_MAX_H:
				bad.append({"name": r["name"], "h": snappedf(float(r["h"]), 0.01), "dist_m": snappedf(d, 0.01)})
	return {"ring_stones": ring.size(), "rocks_within_10m": rocks.size(), "tallest_m": snappedf(tallest, 0.01),
			"over_1_2m": bad, "_pass": bad.is_empty()}


const NAV_CELL := 0.2
const CAPSULE_R := 0.35


func _collider_list(moved: Dictionary = {}) -> Array:
	"""Every solid prop's collider as {p, r}, with `moved` (node -> new xz) applied -- the
	shore search costs a candidate's moves WITHOUT making them."""
	var out := []
	for root in [_props_root, _density_root]:
		if root == null:
			continue
		for c in root.get_children():
			var node := c as Node3D
			var rec: Dictionary = _place_report.get(String(node.name), {})
			if String(rec.get("asset", "")) in ["heather", "heather_base", "raven", ""]:
				continue
			var sz: Array = rec.get("local_size_m", [0.4, 0.4, 0.4])
			var p := Vector2(node.global_position.x, node.global_position.z)
			if moved.has(node):
				p = moved[node]
			out.append({"p": p, "r": maxf(float(sz[0]), float(sz[2])) * 0.42})
	# THE MOUND'S WALL, NOT ITS RIM: the ring of boxes stands at R - 0.18 and each box's outer
	# corners reach ~R + 0.12 -- the heather film's walk stopped against one that the old R disc
	# said he cleared (T10-1d). + 0.15 is the corner radius, so a path this list clears, he clears.
	out.append({"p": MOUND_XZ, "r": MOUND_R + 0.15})
	return out


func _nav_grid(cols: Array) -> Dictionary:
	"""The play area on a 0.2 m grid, a cell blocked where his capsule would touch a collider."""
	var pr := _play_rect()
	var nx := int(ceil(pr.size.x / NAV_CELL))
	var nz := int(ceil(pr.size.y / NAV_CELL))
	var blk := PackedByteArray()
	blk.resize(nx * nz)
	blk.fill(0)
	for c in cols:
		var cp: Vector2 = c["p"]
		var rr: float = float(c["r"]) + CAPSULE_R
		var i0: int = maxi(int(floor((cp.x - rr - pr.position.x) / NAV_CELL)), 0)
		var i1: int = mini(int(ceil((cp.x + rr - pr.position.x) / NAV_CELL)), nx - 1)
		var j0: int = maxi(int(floor((cp.y - rr - pr.position.y) / NAV_CELL)), 0)
		var j1: int = mini(int(ceil((cp.y + rr - pr.position.y) / NAV_CELL)), nz - 1)
		for j in range(j0, j1 + 1):
			var z: float = pr.position.y + (float(j) + 0.5) * NAV_CELL
			for i in range(i0, i1 + 1):
				var x: float = pr.position.x + (float(i) + 0.5) * NAV_CELL
				if Vector2(x, z).distance_to(cp) < rr:
					blk[j * nx + i] = 1
	return {"nx": nx, "nz": nz, "org": pr.position, "blk": blk}


func _nav_cell(g: Dictionary, p: Vector2) -> int:
	var i := int(floor((p.x - (g["org"] as Vector2).x) / NAV_CELL))
	var j := int(floor((p.y - (g["org"] as Vector2).y) / NAV_CELL))
	if i < 0 or j < 0 or i >= int(g["nx"]) or j >= int(g["nz"]):
		return -1
	return j * int(g["nx"]) + i


func _nav_path(g: Dictionary, a: Vector2, b: Vector2) -> Array:
	"""Breadth-first over free cells, 8-connected; [] if b cannot be reached from a."""
	var nx: int = g["nx"]
	var nz: int = g["nz"]
	var blk: PackedByteArray = g["blk"]
	var s := _nav_cell(g, a)
	var e := _nav_cell(g, b)
	if s < 0 or e < 0 or blk[s] == 1 or blk[e] == 1:
		return []
	var prev := PackedInt32Array()
	prev.resize(nx * nz)
	prev.fill(-2)
	prev[s] = -1
	var q := PackedInt32Array([s])
	var head := 0
	var dirs := [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
	while head < q.size():
		var cur := q[head]
		head += 1
		if cur == e:
			break
		var ci := cur % nx
		var cj := cur / nx
		for d in dirs:
			var ni: int = ci + int(d[0])
			var nj: int = cj + int(d[1])
			if ni < 0 or nj < 0 or ni >= nx or nj >= nz:
				continue
			var k := nj * nx + ni
			if blk[k] == 1 or prev[k] != -2:
				continue
			prev[k] = cur
			q.append(k)
	if prev[e] == -2:
		return []
	var cells := []
	var c2 := e
	while c2 != -1:
		cells.push_front(c2)
		c2 = prev[c2]
	var org: Vector2 = g["org"]
	var pts := []
	for k in cells:
		pts.append(org + (Vector2(float(k % nx), float(k / nx)) + Vector2(0.5, 0.5)) * NAV_CELL)
	return pts


func _open_shore_gaps() -> Dictionary:
	"""TWO GAPS OF AT LEAST 1.2 m IN THE PAINTED SHORE, by moving the FEWEST rocks the LEAST.

	Candidate crossings are rays from the tarn's centroid, every 4 degrees, on the side that
	faces the clearing. Each ray's crossing is a 1.2 m-wide corridor from 0.9 m out on the ice
	to 1.8 m inland of the shore. A collider blocks it if it comes within (its radius + 0.6 m)
	of the corridor's centre line; the move that clears it is along the shore, away from the
	line, by exactly the shortfall. Every candidate is costed -- props moved first, total
	distance second -- and the two cheapest crossings at least 3 m apart are opened. Heather is
	walked through and does not block."""
	var ctr := Vector2(-1.33, 4.75)
	var cands := []
	for deg in range(-110, 25, 4):
		var th := deg_to_rad(float(deg))
		var dir := Vector2(cos(th), sin(th))
		var shore := Vector2.INF
		for s in 120:
			var q := ctr + dir * (0.1 * float(s))
			if _splat_w_fast(q.x, q.y)[4] < 0.5:
				shore = q
				break
		if shore == Vector2.INF:
			continue
		# THE CORRIDOR RUNS INLAND UNTIL IT CONNECTS. A 1.3 m cut through the shore row can open
		# onto a pocket walled in by the next row; each bearing is costed at four inland lengths,
		# and the connectivity check below takes the cheapest one that reaches the clearing.
		for inland in [1.3, 2.0, 2.8, 3.6]:
			var cnd := _shore_candidate(deg, dir, shore, inland)
			if cnd.is_empty():
				break                             # a longer cut through the same bar is no better
			cands.append(cnd)
	cands.sort_custom(func(x, y): return x["moves"].size() < y["moves"].size() \
		or (x["moves"].size() == y["moves"].size() and float(x["total"]) < float(y["total"])))
	return _choose_shore_gaps(cands)


func _shore_candidate(deg: int, dir: Vector2, shore: Vector2, inland: float) -> Dictionary:
	"""One corridor, 0.9 m out on the ice to `inland` m past the shore: the rocks (and junipers)
	in it and the least move along the shore that clears each. Empty if it leaves the play area
	or needs a tree, a kit piece or a ring stone moved."""
	var a := shore - dir * 0.9
	var b := shore + dir * inland
	if not _play_rect().has_point(b):
		return {}
	var moves := []
	var total := 0.0
	var touches_ring := false
	for root in [_props_root, _density_root]:
		if root == null:
			continue
		for c in root.get_children():
			var node := c as Node3D
			var rec: Dictionary = _place_report.get(String(node.name), {})
			var asset := String(rec.get("asset", ""))
			if asset in ["heather", "raven", ""]:
				continue
			var sz: Array = rec.get("local_size_m", [0.4, 0.4, 0.4])
			var r: float = maxf(float(sz[0]), float(sz[2])) * 0.42
			var p := Vector2(node.global_position.x, node.global_position.z)
			var need: float = r + SHORE_GAP_M * 0.5 - _dist_to_seg(p, a, b)
			if need <= 0.0:
				continue
			# THE RING DOES NOT MOVE. The first run of this search pushed a painted standing
			# stone 0.18 m to open a crossing; a corridor that needs a megalith moved is
			# not a candidate at all.
			# AND ONLY THE SHORE'S LOOSE DRESSING MOVES: rocks, and the junipers that grow among
			# them. Tried rocks-only first (the brief says "shore rocks"): after the heather
			# patches re-rolled the dressing, every rocks-only gap but one opened onto a pocket
			# walled by junipers, at every inland length, and only ONE crossing could be made.
			# Trees, the kit's keep pieces and the ring never move; each juniper move is
			# reported by name like the rocks'.
			if asset in MEGALITH or not (asset in ["rock_small", "rock_large", "juniper", "boulder", "rocks", "stump"]):
				touches_ring = true
				break
			# along the shore (perpendicular to the corridor), away from its centre line
			var side := Vector2(-dir.y, dir.x)
			var s2 := signf((p - a).dot(side))
			if s2 == 0.0:
				s2 = 1.0
			moves.append({"node": node, "from": p, "to": p + side * s2 * (need + 0.02),
						  "d": need + 0.02})
			total += need + 0.02
	if touches_ring:
		return {}
	return {"deg": deg, "a": a, "b": b, "shore": shore, "moves": moves, "total": total,
			"inland_m": inland}


func _choose_shore_gaps(cands: Array) -> Dictionary:
	# A CROSSING MUST CONNECT. The first version tested only the corridor itself, and its
	# cheapest gap opened onto a pocket walled in by the next row of rocks -- a door into a
	# cupboard. Each candidate's moves are applied VIRTUALLY and the gap is kept only if the
	# navigation grid reaches from its ice end, through it, to the clearing.
	var chosen := []
	var rejected_pocket := 0
	var rejected_at := []
	for cnd in cands:
		var ok := true
		for ch in chosen:
			if (cnd["shore"] as Vector2).distance_to(ch["shore"]) < 2.0:
				ok = false
		if not ok:
			continue
		var moved := {}
		for ch in chosen:
			for m in ch["moves"]:
				moved[m["node"]] = m["to"]
		for m in cnd["moves"]:
			moved[m["node"]] = m["to"]
		var g := _nav_grid(_collider_list(moved))
		if _nav_path(g, cnd["a"], COMBAT_C).is_empty():
			rejected_pocket += 1
			rejected_at.append(int(cnd["deg"]))
			continue
		chosen.append(cnd)
		if chosen.size() >= 2:
			break
	var report_moves := []
	for ch in chosen:
		for m in ch["moves"]:
			var node := m["node"] as Node3D
			var to: Vector2 = m["to"]
			node.global_position = Vector3(to.x, node.global_position.y, to.y)
			report_moves.append({"prop": String(node.name),
				"asset": String(_place_report.get(String(node.name), {}).get("asset", "")),
				"from_xz": [snappedf((m["from"] as Vector2).x, 0.01), snappedf((m["from"] as Vector2).y, 0.01)],
				"to_xz": [snappedf(to.x, 0.01), snappedf(to.y, 0.01)],
				"moved_m": snappedf(float(m["d"]), 0.01), "gap": int(ch["deg"])})
	_shore_moves = report_moves
	_shore_route = chosen
	return {"gaps_opened": chosen.size(), "gap_width_m": SHORE_GAP_M,
			"crossings": chosen.map(func(ch): return {"bearing_deg_from_tarn_centre": ch["deg"],
				"corridor_inland_m": ch["inland_m"],
				"shore_xz": [snappedf((ch["shore"] as Vector2).x, 0.01), snappedf((ch["shore"] as Vector2).y, 0.01)],
				"props_moved": (ch["moves"] as Array).size(), "total_m": snappedf(float(ch["total"]), 0.01)}),
			"moves": report_moves, "candidates_costed": cands.size(),
			"candidates_rejected_as_pockets": rejected_pocket,
			"pockets_at_bearing_deg": rejected_at,
			"cheapest_candidates": cands.slice(0, 6).map(func(c): return {"deg": c["deg"],
				"inland_m": c["inland_m"], "moves": (c["moves"] as Array).size(),
				"total_m": snappedf(float(c["total"]), 0.01)})}


func _fill_by_splat() -> Dictionary:
	if heather_fill == "even":
		return _fill_by_splat_even()
	return _fill_by_splat_patches()


func _fill_by_splat_patches() -> Dictionary:
	"""THE SCATTER THE PAINTING DOES NOT REACH -- IN PATCHES (T10-1d).

	The painting shows about 11 x 9 m of ground; the play area is 19 x 19. Outside the painting's
	own footprint the ground's classes are still the painting's -- the splat map extends its
	plan -- but T10-1c filled the splat's heather class on an even 0.42 m grid, and an even
	scatter of clumps over open snow is the "evenly spread golden popcorn" the coordinator
	flagged. The painting's heather GATHERS: at stone bases, along outcrops, over the mound, in
	patches with open snow between them (tools/barrow_heather_stats.py: the painting's heather
	sits a median 0.07 screen-m from a stone, rock or tree; T10-1c's twice that). So:

	  HEATHER  patch centres on a 1.6 m jittered grid where the splat says heather, kept at 0.85
	           near an anchor (a stone, rock, outcrop, tree, or the mound's rim -- within 1.4 m)
	           and at 0.28 in the open; each patch 0.45-1.4 m across its radius, clumps at 0.30 m
	           with the chance of one falling off as (r / R)^2 toward the edge, taller at the
	           heart; a painted base (the kit's heather_clump) at the heart of half the big ones
	  RUBBLE   where it says rock: rock_small as before, and the kit's minor scatter -- the
	           boulder, the three-rock cluster, the stump -- in among it
	  SKULL    one, lying in open snow on the far side of the tarn from the clearing
	One seed; deterministic."""
	var rng := RandomNumberGenerator.new()
	rng.seed = 55173
	var man := {}
	if FileAccess.file_exists(ASSETS_JSON):
		var mj = JSON.parse_string(FileAccess.get_file_as_string(ASSETS_JSON))
		if typeof(mj) == TYPE_DICTIONARY:
			man = mj.get("models", {})
	var kit := {}
	if FileAccess.file_exists("res://data/kit_assets.json"):
		var kj = JSON.parse_string(FileAccess.get_file_as_string("res://data/kit_assets.json"))
		if typeof(kj) == TYPE_DICTIONARY:
			for k in kj.get("models", {}):
				var ke: Dictionary = kj["models"][k]
				if String(ke.get("status", "")) == "keep" and ResourceLoader.exists(String(ke.get("glb", ""))):
					kit[k] = ke
	var pitch := 1.0 / cos(deg_to_rad(PL_PITCH_DEG))
	var fp: Array = _paint_frame.get("footprint_xz", [])
	var poly := PackedVector2Array()
	for v in fp:
		poly.append(Vector2(float(v[0]), float(v[1])))
	var taken := []
	var anchors := []
	for root in [_props_root, _density_root]:
		for c in root.get_children():
			var node := c as Node3D
			var rec: Dictionary = _place_report.get(String(node.name), {})
			var sz: Array = rec.get("local_size_m", [0.4, 0.4, 0.4])
			var q := {"c": Vector2(node.global_position.x, node.global_position.z),
					  "r": maxf(float(sz[0]), float(sz[2])) * 0.5}
			taken.append(q)
			if not (String(rec.get("asset", "")) in ["heather", "heather_base", "raven", ""]):
				anchors.append(q)
	taken.append({"c": MOUND_XZ, "r": MOUND_R})
	var saved := _props_root
	_props_root = _density_root
	var pr := _play_rect()
	var counts := {}
	var idc := [5000]                      # an Array: a lambda captures an int BY VALUE
	var place_kit := func(cls: String, p: Vector2, h: float, yaw: float) -> Dictionary:
		var kc := "heather_clump" if cls == "heather_base" else cls
		var spec: Dictionary = kit[kc] if kit.has(kc) else man.get(cls, {})
		var glb := String(spec.get("glb", "res://models/barrow/%s.glb" % cls))
		if not ResourceLoader.exists(glb):
			return {}
		idc[0] += 1
		var pc: bool = bool(spec.get("pitch_correct", true)) and not kit.has(kc)
		var e := _place_prop(cls, glb, {"pitch_correct": pc, "yaw_deg": yaw,
				"width_m": spec.get("width_m", null), "height_m": spec.get("height_m", h)}, {},
			{"scene_xz": [p.x, p.y], "height_m": h, "yaw_deg": yaw}, h, false, pitch, int(idc[0]))
		if not e.is_empty():
			taken.append({"c": p, "r": maxf(float(e["size_m"][0]), float(e["size_m"][2])) * 0.5})
			counts[cls] = int(counts.get(cls, 0)) + 1
		return e

	# ---- 1. HEATHER, IN PATCHES ------------------------------------------------------
	var patches := []
	var pstep := 1.6
	var y := pr.position.y + pstep * 0.5
	var row_i := 0
	while y < pr.end.y:
		var x := pr.position.x + pstep * 0.5 + (pstep * 0.5 if row_i % 2 == 1 else 0.0)
		while x < pr.end.x:
			var p := Vector2(x + rng.randf_range(-0.5, 0.5), y + rng.randf_range(-0.5, 0.5))
			x += pstep
			if poly.size() >= 3 and Geometry2D.is_point_in_polygon(p, poly):
				continue                          # the painting's own dressing is already there
			if _in_clear(p, 0.3):
				continue
			var w := _splat_w_fast(p.x, p.y)
			if w[4] > 0.2 or w[3] < 0.45:
				continue
			var near := _near_anchor(p, anchors, 1.4)
			if rng.randf() > (0.85 if near else 0.28):
				continue
			patches.append({"c": p, "r": rng.randf_range(0.45, 1.25) * (1.15 if near else 0.85), "near": near})
		y += pstep * 0.87
		row_i += 1
	var clumps := 0
	for pa in patches:
		var c: Vector2 = pa["c"]
		var R := float(pa["r"])
		if R > 0.8 and rng.randf() < 0.5 and not _in_clear(c, 0.2):
			var across := rng.randf_range(0.5, 0.9)
			place_kit.call("heather_base", c, 0.3812 * across / 0.75, rng.randf_range(-35.0, 35.0))
		var s := 0.30
		var gy := -R
		var gi := 0
		while gy <= R:
			var gx := -R + (s * 0.5 if gi % 2 == 1 else 0.0)
			while gx <= R:
				var q := c + Vector2(gx + rng.randf_range(-0.1, 0.1), gy + rng.randf_range(-0.1, 0.1))
				gx += s
				var d := q.distance_to(c) / R
				if d > 1.0 or rng.randf() > 0.95 * (1.0 - d * d):
					continue
				if _in_clear(q, 0.1) or _splat_w_fast(q.x, q.y)[4] > 0.2:
					continue
				if not _free_at(q, 0.08, anchors, 0.02):
					continue                      # not inside a rock
				idc[0] += 1
				if rng.randf() < 0.05:
					place_kit.call("juniper", q, rng.randf_range(0.8, 1.2), rng.randf() * 360.0)
					continue
				var h := lerpf(0.30, 0.13, d) * rng.randf_range(0.85, 1.15)
				# the glb matters only to heather_mode "blobs" (T10-1c's tussocks, the before/after)
				var e := _place_prop("heather", String(man.get("heather", {}).get("glb", "res://models/barrow/heather.glb")),
									 {}, {}, {"scene_xz": [q.x, q.y], "height_m": h}, h, false, pitch, int(idc[0]))
				if not e.is_empty():
					clumps += 1
					counts["heather"] = int(counts.get("heather", 0)) + 1
			gy += s * 0.87
			gi += 1

	# ---- 2. RUBBLE, and the kit's minor scatter in among it -------------------------
	var rstep := 0.9
	y = pr.position.y + rstep * 0.5
	row_i = 0
	while y < pr.end.y:
		var x := pr.position.x + rstep * 0.5 + (rstep * 0.5 if row_i % 2 == 1 else 0.0)
		while x < pr.end.x:
			var p := Vector2(x + rng.randf_range(-0.25, 0.25), y + rng.randf_range(-0.25, 0.25))
			x += rstep
			if poly.size() >= 3 and Geometry2D.is_point_in_polygon(p, poly):
				continue
			if _in_clear(p, 0.3):
				continue
			var w := _splat_w_fast(p.x, p.y)
			if w[4] > 0.2 or w[2] < 0.5:
				continue
			if rng.randf() > 0.34:
				continue
			var u := rng.randf()
			var cls := "rock_small"
			var h := rng.randf_range(0.25, 0.55)
			if u < 0.12:
				cls = "boulder"
				h = 0.3003 * rng.randf_range(0.8, 1.3)
			elif u < 0.24:
				cls = "rocks"
				h = 0.5108 * rng.randf_range(0.85, 1.15)
			elif u < 0.30:
				cls = "stump"
				h = 0.30 * rng.randf_range(0.9, 1.25)
			var kc2 := cls if kit.has(cls) or cls == "rock_small" else "rock_small"
			var r := _est_radius(kc2, h, man, kit)
			if not _free_at_scaled(p, r, taken, 0.55):
				continue
			place_kit.call(kc2, p, h, rng.randf() * 360.0)
		y += rstep * 0.87
		row_i += 1

	# ---- 3. THE SKULL: one, in open snow on the far side of the tarn --------------------
	var skull_at := []
	if kit.has("skull"):
		var tarn := Vector2(-1.33, 4.75)
		var far := (tarn - COMBAT_C).normalized()
		var target := tarn + far * 4.0
		var best := Vector2.INF
		var bd := INF
		var sy := pr.position.y + 0.25
		while sy < pr.end.y:
			var sx := pr.position.x + 0.25
			while sx < pr.end.x:
				var p := Vector2(sx, sy)
				sx += 0.5
				var w := _splat_w_fast(p.x, p.y)
				if w[4] > 0.05 or w[0] < 0.6 or _in_clear(p, 0.5):
					continue
				if not _free_at(p, 0.75, taken, 0.4):
					continue
				var dd := p.distance_to(target)
				if dd < bd:
					bd = dd
					best = p
			sy += 0.5
		if best != Vector2.INF:
			var e2: Dictionary = place_kit.call("skull", best, 0.4836, 205.0)
			if not e2.is_empty():
				skull_at = [snappedf(best.x, 0.01), snappedf(best.y, 0.01)]
	_props_root = saved
	return {"placed": counts, "heather_patches": patches.size(),
			"heather_patches_near_an_anchor": patches.filter(func(q): return bool(q["near"])).size(),
			"heather_clumps": clumps, "skull_xz": skull_at,
			"_outside": "the painting's own footprint (dressed from the painting)"}


func _fill_by_splat_even() -> Dictionary:
	"""T10-1c's FILL, kept for the before/after of T10-1d's patches (heather_fill = "even"): an
	even grid over the splat's heather class. THE SCATTER THE PAINTING DOES NOT REACH. The painting shows about 11 x 9 m of ground;
	the play area is 19 x 19. Outside the painting's own footprint the ground's classes are
	still the painting's -- the splat map extends its plan -- so the fill follows the splat:
	heather where it says heather, low rubble where it says rock, a juniper now and then in
	both, and nothing on snow, ice, the clearing or the corridors. One seed; deterministic."""
	var rng := RandomNumberGenerator.new()
	rng.seed = 55173
	var man := {}
	if FileAccess.file_exists(ASSETS_JSON):
		var mj = JSON.parse_string(FileAccess.get_file_as_string(ASSETS_JSON))
		if typeof(mj) == TYPE_DICTIONARY:
			man = mj.get("models", {})
	var pitch := 1.0 / cos(deg_to_rad(PL_PITCH_DEG))
	var fp: Array = _paint_frame.get("footprint_xz", [])
	var poly := PackedVector2Array()
	for v in fp:
		poly.append(Vector2(float(v[0]), float(v[1])))
	var taken := []
	for root in [_props_root, _density_root]:
		for c in root.get_children():
			var node := c as Node3D
			var rec: Dictionary = _place_report.get(String(node.name), {})
			var sz: Array = rec.get("local_size_m", [0.4, 0.4, 0.4])
			taken.append({"c": Vector2(node.global_position.x, node.global_position.z),
						  "r": maxf(float(sz[0]), float(sz[2])) * 0.5})
	taken.append({"c": MOUND_XZ, "r": MOUND_R})
	var saved := _props_root
	_props_root = _density_root
	var pr := _play_rect()
	var counts := {}
	var idx := 5000
	var step := 0.42
	var y := pr.position.y + step * 0.5
	while y < pr.end.y:
		var x := pr.position.x + step * 0.5 + (step * 0.5 if int(y / step) % 2 == 1 else 0.0)
		while x < pr.end.x:
			var p := Vector2(x + rng.randf_range(-0.15, 0.15), y + rng.randf_range(-0.15, 0.15))
			x += step
			if poly.size() >= 3 and Geometry2D.is_point_in_polygon(p, poly):
				continue                          # the painting's own dressing is already there
			if _in_clear(p, 0.2):
				continue
			var w := _splat_w_fast(p.x, p.y)
			if w[4] > 0.2 or w[0] > 0.55:
				continue                          # ice, and open snow, stay open
			var cls := ""
			var h := 0.0
			if w[3] > 0.5:
				cls = "juniper" if rng.randf() < 0.07 else "heather"
				h = rng.randf_range(0.8, 1.2) if cls == "juniper" else rng.randf_range(0.4, 0.8)
			elif w[2] > 0.5:
				if rng.randf() > 0.34:
					continue
				cls = "rock_small" if rng.randf() < 0.85 else "heather"
				h = rng.randf_range(0.25, 0.55) if cls == "rock_small" else rng.randf_range(0.4, 0.7)
			else:
				continue
			var r := _est_radius(cls, h, man, {})
			if not _free_at_scaled(p, r, taken, 0.55):
				continue
			var spec: Dictionary = man.get(cls, {})
			var glb := String(spec.get("glb", "res://models/barrow/%s.glb" % cls))
			if not ResourceLoader.exists(glb):
				continue
			idx += 1
			var e := _place_prop(cls, glb, {"pitch_correct": bool(spec.get("pitch_correct", true)),
					"yaw_deg": rng.randf() * 360.0, "width_m": spec.get("width_m", null),
					"height_m": spec.get("height_m", h)}, {},
				{"scene_xz": [p.x, p.y], "height_m": h, "yaw_deg": rng.randf() * 360.0}, h, false, pitch, idx)
			if e.is_empty():
				continue
			taken.append({"c": p, "r": maxf(float(e["size_m"][0]), float(e["size_m"][2])) * 0.5})
			counts[cls] = int(counts.get(cls, 0)) + 1
		y += step * 0.87
	_props_root = saved
	return {"placed": counts, "grid_m": step, "_outside": "the painting's own footprint (dressed from the painting)"}


func _near_anchor(p: Vector2, anchors: Array, d: float) -> bool:
	"""Within d of a stone, rock, outcrop, tree or kit piece -- or of the mound's rim."""
	for a in anchors:
		if p.distance_to(a["c"]) - float(a["r"]) < d:
			return true
	return absf(p.distance_to(MOUND_XZ) - MOUND_R) < d


func _instance_props() -> Dictionary:
	"""Hide every repeated prop's own meshes and draw them as MultiMeshes instead. The per-prop
	nodes STAY -- their transforms, colliders, snow obstacles, reports and verification all
	still read them -- so instancing is a toggle (set_instancing) and its cost is measured as
	a subtraction inside one run, same props, same frame."""
	var t0 := Time.get_ticks_msec()
	var entries := []
	var mat_by_key := {}
	for root in [_props_root, _density_root]:
		if root == null:
			continue
		for c in root.get_children():
			var node := c as Node3D
			var rec: Dictionary = _place_report.get(String(node.name), {})
			var cls := String(rec.get("asset", ""))
			if not (cls in INSTANCED):
				continue
			var ups: Array = _rock_up.get(String(node.name), [])
			var k := 0
			for mi in node.find_children("*", "MeshInstance3D", true, false):
				var m := mi as MeshInstance3D
				if String(m.name).ends_with("_ink"):
					_instanced_inks[m] = true
					continue
				var key := "%s|%d" % [cls, m.mesh.get_instance_id()]
				if not mat_by_key.has(key):
					mat_by_key[key] = m.material_override
				var s3 := m.global_transform.basis.get_scale()
				entries.append({"key": key, "asset": cls, "mesh": m.mesh, "mat": mat_by_key[key],
					"part": "core" if String(m.name) == "HeatherCore" else String(m.get_meta("part", "")),
					"xf": m.global_transform, "xf_up": ups[k] if k < ups.size() else m.global_transform,
					"hull_world_m": _hull_for(cls) / PPM, "scale": (absf(s3.x) + absf(s3.y) + absf(s3.z)) / 3.0,
					"shadow": m.cast_shadow != GeometryInstance3D.SHADOW_CASTING_SETTING_OFF})
				_hidden_meshes.append(m)
				k += 1
	_instanced_root = Node3D.new()
	_instanced_root.name = "Instanced"
	add_child(_instanced_root)
	var res := BarrowInstancer.build(_instanced_root, entries, CHUNK_M, PaintStack.INK, LOD_TARGETS,
		CHUNK_BY_ASSET)
	_mmis = res["mmis"]
	_mm_inks = res["inks"]
	# the per-chunk member lists, in instance order, for the rock A/B
	var groups := {}
	for e in entries:
		var cpos: Vector3 = (e["xf"] as Transform3D).origin
		var ck := "MM_%s_%d_%d" % [String(e["key"]).replace("|", "_"), int(floor(cpos.x / CHUNK_M)),
								   int(floor(cpos.z / CHUNK_M))]
		if not groups.has(ck):
			groups[ck] = []
		groups[ck].append(e)
	_mm_members = groups
	set_instancing(true)
	var inst_total := 0
	for a in res["per_asset"]:
		inst_total += int(res["per_asset"][a]["instances"])
	return {"instances": inst_total, "per_asset": res["per_asset"], "mmi_draws": _mmis.size(),
			"ink_draws": _mm_inks.size(), "chunk_m": CHUNK_M, "build_ms": Time.get_ticks_msec() - t0}


func set_instancing(on: bool) -> void:
	"""The A/B for T10-1c item 1: the repeated props as MultiMeshes (on), or as one node each
	(off) -- the same props, the same transforms, the same materials."""
	_instancing_on = on and not _mmis.is_empty()
	_apply_draw_mode()


var _density_visible := true
var _asset_hidden := {}


func set_asset_visible(asset: String, on: bool) -> void:
	"""One repeated asset on or off in WHICHEVER mode is drawing it -- its MultiMesh chunks
	and their pens, or its per-prop meshes and theirs -- for the per-asset cost table."""
	if on:
		_asset_hidden.erase(asset)
	else:
		_asset_hidden[asset] = true
	_apply_draw_mode()


func set_instanced_pens_visible(on: bool) -> void:
	for l in _mm_inks:
		(l as MultiMeshInstance3D).visible = on


var _cores_hidden := false


func set_heather_cores_visible(on: bool) -> void:
	"""The heather clumps' bodies on or off, in whichever mode draws them -- the cost of the
	warmth change measured as a subtraction inside one run."""
	_cores_hidden = not on
	_apply_draw_mode()


func _apply_draw_mode() -> void:
	var nodes_on := _density_visible and not _instancing_on
	for m in _hidden_meshes:
		if is_instance_valid(m):
			(m as MeshInstance3D).visible = nodes_on and not _asset_hidden.has(_asset_of(m)) \
				and not (_cores_hidden and String((m as Node).name) == "HeatherCore") \
				and _rep_shown(String((m as Node).get_meta("part", "")))
	for m in _instanced_inks:
		if is_instance_valid(m):
			(m as MeshInstance3D).visible = nodes_on and not _asset_hidden.has(_asset_of(m))
	if _instanced_root != null:
		_instanced_root.visible = _density_visible and _instancing_on
	for m in _mmis + _mm_inks:
		(m as MultiMeshInstance3D).visible = not _asset_hidden.has(String(m.get_meta("asset", ""))) \
			and not (_cores_hidden and String(m.get_meta("part", "")) == "core") \
			and _rep_shown(String(m.get_meta("part", "")))


func _rep_shown(part: String) -> bool:
	if not heather_ab or not (part == "stems" or part == "cards"):
		return true
	return part == (_heather_rep if _heather_rep != "" else heather_mode)


func _asset_of(n: Node) -> String:
	"""The asset of the prop a mesh belongs to: walk up to the prop root, read its report."""
	var cur := n
	while cur != null and cur.get_parent() != _props_root and cur.get_parent() != _density_root:
		cur = cur.get_parent()
	if cur == null:
		return ""
	return String(_place_report.get(String(cur.name), {}).get("asset", ""))


func set_rock_pose(upright: bool) -> void:
	"""The A/B for T10-1c item 2: every rock_large as T10-1b stood it (upright, painted height)
	or laid low. Swaps the instance transforms in place; the per-prop nodes, colliders and snow
	are the low version throughout, so this is a picture of the POSE and nothing else."""
	_rock_pose_up = upright
	for mmi in _mmis + _mm_inks:
		var m := mmi as MultiMeshInstance3D
		if String(m.get_meta("asset", "")) != "rock_large":
			continue
		var nm := String(m.name).trim_suffix("_ink")
		var mem: Array = _mm_members.get(nm, [])
		for i in mini(mem.size(), m.multimesh.instance_count):
			m.multimesh.set_instance_transform(i, mem[i]["xf_up"] if upright else mem[i]["xf"])


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


func _drop_prop(e: Dictionary) -> void:
	"""FREE A PLACED PROP AND EVERYTHING THAT STILL POINTS AT IT. A plain queue_free() left its
	hull-pen meshes in _prop_inks and its ramp in _world_mats; the next set_hull_ink_visible
	hit a freed object and stopped halfway down the list, so the pen-isolation frames hid
	SOME of the props' pens and not others -- and nothing said so except a SCRIPT ERROR in a
	capture log. The pens are removed from the list before the node goes."""
	var node := e["node"] as Node3D
	var dead := {}
	for mi in node.find_children("*_ink", "MeshInstance3D", true, false):
		dead[mi] = true
	var kept: Array = []
	for mi in _prop_inks:
		if not dead.has(mi):
			kept.append(mi)
	_prop_inks = kept
	var mats := {}
	for mi in node.find_children("*", "MeshInstance3D", true, false):
		var mo := (mi as MeshInstance3D).material_override
		if mo != null:
			mats[mo] = true
	var wm: Array[ShaderMaterial] = []
	for m in _world_mats:
		if not mats.has(m):
			wm.append(m)
	_world_mats = wm
	_place_report.erase(String(node.name))
	node.queue_free()


var _dress: Array = []


func _load_dress() -> Array:
	var path := "res://data/barrow_dress_a.json"
	if not FileAccess.file_exists(path):
		return []
	var d = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(d) != TYPE_DICTIONARY:
		return []
	report["dress_source"] = {"file": path, "counts": d.get("counts", {}), "frame": d.get("frame", {}),
		"_how": "tools/barrow_paint_dress.py -- the concept painting segmented once; stones annotated by hand"}
	_paint_frame = d.get("frame", {})
	return d.get("instances", [])


var _paint_frame := {}


func _inside_painted_stone(e: Dictionary, stones: Array) -> Dictionary:
	"""Is this prop's centre inside a painted stone's footprint (0.8 of its radius)."""
	var x := float(e["scene_xz"][0])
	var z := float(e["scene_xz"][1])
	for q in stones:
		var r: float = maxf(float(q["size_m"][0]), float(q["size_m"][2])) * 0.5 * 0.8
		var d := Vector2(x - float(q["scene_xz"][0]), z - float(q["scene_xz"][1])).length()
		if d < r:
			return {"asset": q["asset"], "d": d}
	return {}


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
			# NO SNOW ON HEATHER: 1.05 was not "no snow" -- the threshold WANDERS by the jitter,
			# 1.05 +- 0.12 reaches 0.93, and blade tips facing straight up catch it. Raised to
			# 1.5 for "the warm tops showing". MEASURED, IT WAS NOT WHY THE HEATHER WAS PALE:
			# dE 34.55 -> 34.49, nothing. That was buried sprigs sampled as heather and the
			# ramp's cool shadow on pixel-wide blades -- see HEATHER_CORE, the snow scoops
			# (HEATHER_SNOW_FRAC) and the visible-pixel instrument (set_class_id_view).
			return {"snow_threshold": 1.5, "snow_jitter": 0.0, "snow_soft": 0.05,
					"snow_noise_scale": 3.0, "mottle_scale": 4.0, "mottle_amp": 0.18,
					"hatch_scale": 18.0, "hatch_amp": 0.08, "mesh_mark": 0.25,
					"tex_tint": HEATHER_TINT, "_two_sided": heather_two_sided}
		"raven":
			# NO SNOW ON THE BIRD. 2.0 is above any achievable n.up, which is how this shader
			# says "never" -- and it says it through the same parameter as everything else
			# rather than through a second code path.
			return {"snow_threshold": 2.0, "snow_jitter": 0.0, "snow_soft": 0.05,
					"mottle_scale": 6.0, "mottle_amp": 0.10, "hatch_scale": 24.0}
		"juniper":
			# THE PAINTING'S JUNIPER IS DARK: a dark green-brown clump with a dusting on top. On
			# the birch rule its twiggy mesh -- mostly small up-facing faces -- took snow on
			# nearly all of them and came out pale grey, the opposite of what it is there for.
			# (and 1.02 +- 0.09 reached 0.93 too: the same wandering threshold. Raised with the
			# heather's, and like the heather's it moved nothing measurable -- the juniper's
			# colour was the tint's job; see JUNIPER_TINT)
			return {"snow_threshold": 1.5, "snow_jitter": 0.0, "snow_soft": 0.05,
					"snow_noise_scale": 3.2, "mottle_scale": 5.0, "mottle_amp": 0.20,
					"hatch_scale": 22.0, "hatch_amp": 0.08, "mesh_mark": 0.25,
					"tex_tint": JUNIPER_TINT}
		"birch":
			return {"snow_threshold": 0.92, "snow_jitter": 0.20, "snow_soft": 0.08,
					"snow_noise_scale": 3.2, "mottle_scale": 5.0, "mottle_amp": 0.24,
					"hatch_scale": 22.0, "hatch_amp": 0.10, "mesh_mark": 0.25}
		"heather_base":
			# the painted clump: no snow of its own (its texture carries crumbs), and a tone per
			# instance so a patch of them is not one colour repeated
			return {"snow_threshold": 1.5, "snow_jitter": 0.0, "snow_soft": 0.05,
					"snow_noise_scale": 3.0, "mottle_scale": 4.0, "mottle_amp": 0.14,
					"hatch_scale": 18.0, "hatch_amp": 0.06, "mesh_mark": 0.25, "tone_jitter": 0.28}
		"outcrop_a":
			# THE OUTCROP'S TEXTURE IS ITS SNOW: painted ledges, mean sRGB 0.72. At 0.80 the layer
			# whited it into a boulder (d_look1); it adds none
			return {"snow_threshold": 1.5, "snow_jitter": 0.0, "snow_soft": 0.05,
					"snow_noise_scale": 2.0, "mottle_scale": 1.6, "mottle_amp": 0.16,
					"hatch_scale": 9.0, "hatch_amp": 0.07}
		"boulder", "rocks":
			# painted snow caps too; the layer adds a little on the flattest tops
			return {"snow_threshold": 0.95, "snow_jitter": 0.20, "snow_soft": 0.10,
					"snow_noise_scale": 2.0, "mottle_scale": 1.6, "mottle_amp": 0.16,
					"hatch_scale": 9.0, "hatch_amp": 0.07}
		"dead_tree":
			return {"snow_threshold": 0.92, "snow_jitter": 0.20, "snow_soft": 0.08,
					"snow_noise_scale": 3.2, "mottle_scale": 5.0, "mottle_amp": 0.24,
					"hatch_scale": 22.0, "hatch_amp": 0.10, "mesh_mark": 0.25}
		"stump", "skull":
			return {"snow_threshold": 0.78, "snow_jitter": 0.22, "snow_soft": 0.09,
					"snow_noise_scale": 3.0, "mottle_scale": 4.0, "mottle_amp": 0.20,
					"hatch_scale": 18.0, "hatch_amp": 0.08}
		"rock_large", "rock_small":
			# 0.58 -> 0.72 (T10-1c): laid on their sides, the rocks' broad faces point up and at
			# 0.58 they came out as white slabs; the painting's outcrops are grey-brown lichen
			# ledges with snow on the ledges, Lab (45.0, 4.7, 10.4)
			return {"snow_threshold": 0.72, "snow_jitter": 0.30, "snow_soft": 0.11,
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
		"heather", "birch", "juniper", "dead_tree", "heather_base":
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
	_density_root = Node3D.new()
	_density_root.name = "Density"
	add_child(_density_root)

	var by_class := {}
	var rep_mat := {}
	var placed := []
	var skipped := []
	var seen := {}
	var tris := 0
	var idx := 0

	# THE PAINTED STONES GO IN FIRST, and they win. Nine of the painting's twelve standing
	# stones were never placed (T10's segmentation found four), and two rows of the scene list
	# sit ON painted stones: a birch on the big carved spiral stone -- the same mask bleed as
	# T10_HANDOFF fault 5 -- and a small rock on the snow-capped stone in front of the door.
	# Placed first, the stones are what the interpenetration rule below tests the old rows
	# against, so those two drop out by the same rule that already drops birches inside stones.
	_dress = _load_dress()
	var painted_stones := []
	var painted_idx := 0
	var saved_root := _props_root
	_props_root = _density_root
	for row in _dress:
		if not bool(row.get("priority", false)):
			continue
		var cls0 := String(row.get("asset", ""))
		var spec0: Dictionary = man.get(cls0, {})
		var glb0 := String(spec0.get("glb", "res://models/barrow/%s.glb" % cls0))
		if not ResourceLoader.exists(glb0):
			continue
		# THEIR OWN COUNTER. Sharing `idx` renamed every scene-list node that came after them --
		# stone_tall_03 became stone_tall_12 -- and the capture's scale still, which asks for
		# stone_tall_03 by name, silently fell back to a hand-typed position beside no stone.
		painted_idx += 1
		var e0 := _place_prop(cls0, glb0, spec0, sizes, row,
			float(row.get("height_m", 1.5)) * stone_scale, false, pitch, 2000 + painted_idx)
		if not e0.is_empty():
			painted_stones.append(e0)
			tris += int(e0["tris"])
	_props_root = saved_root
	placed.append_array(painted_stones)
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
		if cls == "heather" and target > HEATHER_PATCH_ABOVE_M:
			for e2 in _place_heather_patch(glb, spec, sizes, row, target, pitch, idx):
				placed.append(e2)
				tris += int(e2["tris"])
				if not by_class.has(cls):
					by_class[cls] = []
				by_class[cls].append(e2["node"])
				if not rep_mat.has(cls):
					rep_mat[cls] = e2["mat"]
			continue
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
		var hit_p := _inside_painted_stone(e, painted_stones)
		if not hit_p.is_empty() and cls != "heather":
			skipped.append({"asset": cls, "at": e["scene_xz"],
							"why": "stands on a PAINTED standing stone -- the painting has a stone here, not a %s" % cls,
							"gap_m": snappedf(float(hit_p["d"]), 0.001)})
			_drop_prop(e)
			continue
		if DROP_INTERPENETRATING and cls != "heather":
			var hit := _overlaps_placed(e, placed)
			if not hit.is_empty():
				skipped.append({"asset": cls, "at": e["scene_xz"],
								"why": "footprint centre inside %s -- upstream mask overlap"
									% String(hit["asset"]),
								"gap_m": snappedf(float(hit["d"]), 0.001)})
				_drop_prop(e)
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
		"heather_patches": _patches,
		"placement": _place_report,
	}
	return groups


var _patches: Array = []


func _place_heather_patch(glb: String, spec: Dictionary, sizes: Dictionary, row: Dictionary,
		extent: float, pitch: float, idx: int) -> Array:
	"""One handoff heather row as a PATCH: clumps of painting scale (0.35-0.55 m) on a
	sunflower spiral over the row's measured extent, skipping ice and the combat clearing as
	the painted dress does. Deterministic in the row's index. See HEATHER_PATCH_ABOVE_M."""
	var xz: Array = row.get("scene_xz", [0.0, 0.0])
	var c := Vector2(float(xz[0]), float(xz[1]))
	var rad := extent * 0.5
	var n := clampi(int(round(pow(rad / PATCH_CLUMP_M, 2.0))), 2, 12)
	var out := []
	var skipped_here := 0
	for j in n:
		var f := sqrt((float(j) + 0.5) / float(n)) * rad * 0.85
		var a := float(j) * 2.39996 + float(idx) * 0.7
		var p := c + Vector2(cos(a), sin(a)) * f
		if _in_clear(p, 0.0) or _splat_w_fast(p.x, p.y)[4] > 0.6:
			skipped_here += 1
			continue
		var h := 0.14 + 0.16 * fposmod(float(j) * 0.618 + float(idx) * 0.37, 1.0)
		var r2 := row.duplicate()
		r2["scene_xz"] = [p.x, p.y]
		r2["height_m"] = h
		var e := _place_prop("heather", glb, spec, sizes, r2, h, false, pitch, 8000 + idx * 20 + j)
		if not e.is_empty():
			out.append(e)
	_patches.append({"row_xz": [snappedf(c.x, 0.001), snappedf(c.y, 0.001)],
					 "extent_m": snappedf(extent, 0.01), "clumps": out.size(),
					 "skipped_ice_or_clearing": skipped_here})
	return out


func _load_heather_cards() -> void:
	if not FileAccess.file_exists(HEATHER_CARDS_JSON) or not ResourceLoader.exists(HEATHER_CARDS_PNG):
		return
	var j = JSON.parse_string(FileAccess.get_file_as_string(HEATHER_CARDS_JSON))
	if typeof(j) != TYPE_DICTIONARY:
		return
	_heather_cards = j.get("tiles", [])
	_heather_card_tex = load(HEATHER_CARDS_PNG)


func _heather_material(cards: bool) -> ShaderMaterial:
	"""ONE material per representation, shared by every clump -- so the MultiMesh draws each
	representation's chunks with one bind, and the wind clock is one uniform to push."""
	var key := "cards" if cards else "stems"
	if _heather_mats.has(key):
		return _heather_mats[key]
	var m := BarrowHeather.material(fbm, cards, {
		"albedo_mul": HEATHER_CARD_MUL if cards else HEATHER_STEM_MUL, "mesh_mark": 0.25})
	if cards and _heather_card_tex != null:
		m.set_shader_parameter("card_tex", _heather_card_tex)
	m.set_shader_parameter("wind_dir", WIND.normalized())
	_heather_mats[key] = m
	_world_mats.append(m)
	return m


func _place_heather(row: Dictionary, target: float, idx: int) -> Dictionary:
	"""T10-1d: ONE HEATHER CLUMP AS A SPRAY -- generated stems, or one of the painting's own
	tufts as a card, or both (heather_ab). No yaw: sprays and cards are built facing the fixed
	camera. Height is the clump's scale (+-15% by index); the variant and the card tile come
	from the index, so a capture is repeatable. Walked through: no collider, no snow skirt."""
	var xz: Array = row.get("scene_xz", [0.0, 0.0])
	var x := float(xz[0])
	var z := float(xz[1])
	var hh := target * (0.85 + 0.30 * fposmod(float(idx) * 0.6180339, 1.0))
	var root := Node3D.new()
	root.name = "heather_%02d" % idx
	_props_root.add_child(root)
	var reps := ["stems", "cards"] if heather_ab else [heather_mode]
	var tris := 0
	var mat = null
	var across := 0.0
	for rep in reps:
		var mesh: ArrayMesh = null
		var s := hh
		if rep == "cards":
			if _heather_cards.is_empty():
				_load_heather_cards()
			if _heather_cards.is_empty():
				continue
			var tile: Dictionary = _heather_cards[int(fposmod(float(idx) * 5.0 + 1.0, float(_heather_cards.size())))]
			mesh = BarrowHeather.card_mesh(tile)
			# A CARD IS SIZED ON SCREEN, where it was cut: to the painted tuft's own screen height
			# where the row carries it (the dress), else ~1.8x the tuft's height -- a low tuft's
			# screen extent is mostly its DEPTH (0.6 h + 0.8 d, with d ~ 1.5 h)
			var scr := float(row.get("screen_h_m", 1.8 * hh))
			s = scr * (hh / maxf(target, 1e-3)) / maxf(float(tile["h_m"]), 1e-3)
		else:
			mesh = BarrowHeather.spray_mesh(int(fposmod(float(idx) * 7.0 + 3.0, float(BarrowHeather.VARIANTS))))
		var mi := MeshInstance3D.new()
		mi.name = "HeatherCard" if rep == "cards" else "HeatherStems"
		mi.mesh = mesh
		mi.scale = Vector3.ONE * s
		mi.material_override = _heather_material(rep == "cards")
		mi.set_meta("part", rep)
		root.add_child(mi)
		tris += mesh.surface_get_array_index_len(0) / 3
		if mat == null:
			mat = mi.material_override
		var ab := mesh.get_aabb()
		across = maxf(across, maxf(ab.size.x, ab.size.z) * s)
	var g := _ground_under(x, z, maxf(across * 0.5, 0.05))
	root.global_position = Vector3(x, float(g["lo"]) - 0.01, z)
	var rec := {"node": root, "mat": mat, "tris": tris, "asset": "heather",
			"size_m": [snappedf(across, 0.001), snappedf(hh, 0.001), snappedf(across, 0.001)],
			"target_m": snappedf(target, 0.001), "across": false,
			"scene_xz": [x, z], "yaw_deg": 0.0, "ground": g, "top_y": root.global_position.y + hh}
	_place_report[String(root.name)] = {
		"asset": "heather", "concept_height_m": snappedf(target, 0.001), "target_m": snappedf(hh, 0.001),
		"sized_by": "height", "local_size_m": rec["size_m"], "yaw_deg": 0.0,
		"ground_spread_m": snappedf(float(g["spread"]), 0.001), "rep": heather_mode if not heather_ab else "ab"}
	return rec


func set_heather_wind(on: bool) -> void:
	for k in _heather_mats:
		(_heather_mats[k] as ShaderMaterial).set_shader_parameter("wind_on", 1.0 if on else 0.0)


func set_heather_push(on: bool) -> void:
	for k in _heather_mats:
		(_heather_mats[k] as ShaderMaterial).set_shader_parameter("push_on", 1.0 if on else 0.0)


func set_heather_representation(rep: String) -> void:
	"""heather_ab only: which of the two built representations draws."""
	_heather_rep = rep
	_apply_draw_mode()


func set_shadow_after_bands(on: bool) -> void:
	"""The A/B for T10-1d item 1: the T10-1d shadow (on) -- the cast shadow applied after the
	bands, through Soft Medium -- or T10-1c's (off): before the bands, through Soft Low. On
	every lit surface: the world, the snow, him."""
	RenderingServer.directional_soft_shadow_filter_set_quality(SHADOW_FILTER_T10_1D if on
		else RenderingServer.SHADOW_QUALITY_SOFT_LOW)
	var v := 1.0 if on else 0.0
	for m in _world_mats:
		m.set_shader_parameter("shadow_after_bands", v)
	if snow != null and snow.material() != null:
		snow.material().set_shader_parameter("shadow_after_bands", v)
	PaintStack.set_character_param(_char_saved, "shadow_after_bands", v)


static func _heather_core_mesh() -> ArrayMesh:
	"""A unit tuft: NOT a dome. A dome read as a pom-pom (look13: round golden blobs, the hue
	right and the shape wrong); the painting's tufts are SHEAVES -- sprigs rising from a narrow
	foot and splaying out, a ragged rim, a low crown. So: foot radius 0.55, flaring to 1.0 at the
	rim, the rim ragged (a per-vertex hash, in and out) and uneven in height, the
	crown closing low inside it. Four small incommensurate harmonics on the outline so no two
	yaws look alike (one strong 7-lobe term drew a star, look9). ~250 triangles, one shared mesh.
	Clockwise from outside, Godot's front face; UVs planar from above, so the heather tile lies
	across the crown the way it lies on the ground."""
	if _core_mesh != null:
		return _core_mesh
	var seg := 24
	# (radius, height, serration, height jitter) per ring, foot to crown
	var prof := [[0.55, 0.0, 0.0, 0.0], [0.80, 0.34, 0.04, 0.0], [0.97, 0.68, 0.10, 0.04],
				 [1.00, 0.90, 0.22, 0.12], [0.52, 0.99, 0.08, 0.05]]
	var ring_pts := []
	for ri in prof.size():
		var pr: Array = prof[ri]
		var row := []
		for si in seg:
			var th := TAU * float(si) / float(seg)
			var hsh := fposmod(sin(float(si) * 12.9898 + float(ri) * 78.233) * 43758.5453, 1.0) - 0.5
			# IRREGULAR, not alternating: an in/out/in/out rim drew a saw-blade rosette (look14)
			var serr := hsh * 1.6
			var lobe := 1.0 + 0.07 * sin(th * 3.0 + 0.4) + 0.06 * sin(th * 5.0 + 1.3) \
				+ 0.05 * sin(th * 8.0 + 2.2) + 0.04 * sin(th * 13.0 + 0.9)
			var r := float(pr[0]) * lobe * (1.0 + float(pr[2]) * serr)
			var y := float(pr[1]) * (1.0 + float(pr[3]) * (serr + hsh))
			row.append(Vector3(cos(th) * r, y, sin(th) * r))
		ring_pts.append(row)
	var top := Vector3(0.0, 0.97, 0.0)
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var tris := []
	for ri in prof.size() - 1:
		for si in seg:
			var a: Vector3 = ring_pts[ri][si]
			var b: Vector3 = ring_pts[ri][(si + 1) % seg]
			var c: Vector3 = ring_pts[ri + 1][si]
			var d: Vector3 = ring_pts[ri + 1][(si + 1) % seg]
			tris.append_array([a, b, c, b, d, c])
	var last: Array = ring_pts[prof.size() - 1]
	for si in seg:
		tris.append_array([last[si], last[(si + 1) % seg], top])
	for q in tris:
		var v3: Vector3 = q
		st.set_uv(Vector2(v3.x, v3.z) * 0.17 + Vector2(0.5, 0.5))
		st.add_vertex(v3)
	st.index()
	st.generate_normals()
	_core_mesh = st.commit()
	return _core_mesh


func _place_prop(cls: String, glb: String, spec: Dictionary, sizes: Dictionary,
		row: Dictionary, target: float, across: bool, pitch: float, idx: int) -> Dictionary:
	if cls == "heather" and heather_mode != "blobs":
		return _place_heather(row, target, idx)
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
	if cls == "heather" and HEATHER_CLUMP > 1:
		for ci in range(1, HEATHER_CLUMP):
			var extra := ps.instantiate() as Node3D
			extra.rotation = Vector3(0.0, deg_to_rad(40.0 * float(ci) + float(idx % 7) * 11.0), 0.0)
			var ang := float(ci) * 2.4 + float(idx) * 0.7
			# offsets in the raw model's own units (a tussock is ~1 unit across before sizing)
			extra.position = Vector3(cos(ang) * 0.22, 0.0, sin(ang) * 0.22)
			extra.scale = Vector3.ONE * (0.82 + 0.09 * float(ci))
			fit.add_child(extra)
	if cls == "heather" and heather_core:
		# inside the tussocks' own bounds, so the clump is sized and seated exactly as before
		var tb := _node_aabb(root)
		var tex: Texture2D = null
		for n in fit.find_children("*", "MeshInstance3D", true, false):
			var am := (n as MeshInstance3D).get_active_material(0) as BaseMaterial3D
			if am != null and am.albedo_texture != null:
				tex = am.albedo_texture
				break
		if tex != null and tb.size.y > 0.0:
			var core := MeshInstance3D.new()
			core.name = "HeatherCore"
			core.mesh = _heather_core_mesh()
			var cw := maxf(tb.size.x, tb.size.z) * CORE_W * 0.5
			core.scale = Vector3(cw, tb.size.y * CORE_H, cw)
			core.position = Vector3(tb.position.x + tb.size.x * 0.5, tb.position.y,
									tb.position.z + tb.size.z * 0.5)
			var tm := StandardMaterial3D.new()
			tm.albedo_texture = tex
			core.material_override = tm
			fit.add_child(core)
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

	# 3b. the painted stones' +-10%: a WIDTH variation, so the painted height -- the ruler
	# reading -- stays exactly as measured while the three models stop reading as three copies
	var wm := float(row.get("width_mul", 1.0))
	if absf(wm - 1.0) > 1e-4:
		fit.scale = Vector3(fit.scale.x * wm, fit.scale.y, fit.scale.z * wm)

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
	if not (cls in ["heather", "heather_base", "raven"]):
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
	# (Small props DO still cast. Turning shadows off below 0.65 m was tried as a budget cut and
	# measured at 16.97 -> 16.98 ms -- nothing -- because the cost is per-instance vertex work in
	# every pass, not the shadow pass; see LOD_THRESHOLD_PX for the lever that was.)
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
	# THE SCENE LIST'S OWN MEGALITHS ONLY. The painted stones are placed first now, and one of
	# them -- the big carved spiral stone, 2.83 m -- is taller than the serpent stone (2.71 m),
	# so "the tallest" moved the raven off the stone the painting puts it on.
	var best = null
	for e in placed:
		if (e["node"] as Node3D).get_parent() != _props_root:
			continue
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
		var n := prop_node(String(nm))
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
	"""Every placed prop -- the scene list's AND the dressing's. The density root was added in
	T10-1b; a verification that walked only the first root would pass a floating rock in the
	second without ever looking at it."""
	var o := []
	for root in [_props_root, _density_root]:
		if root != null:
			for c in root.get_children():
				o.append(String((c as Node).name))
	return o


func prop_node(nm: String) -> Node3D:
	for root in [_props_root, _density_root]:
		if root != null:
			var n := root.get_node_or_null(NodePath(nm)) as Node3D
			if n != null:
				return n
	return null


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
	# FOG OFF BY DEFAULT (T10-1b). Still 10 of the 17:20 set -- the fog off -- was nearly
	# identical to still 1, and the coordinator read the veil as the ground's own FBM snow
	# blend, not the fog. It was bought for a hollow the floor no longer has; it is kept only
	# as the `fog_on` switch the veil before/after uses to reproduce the old look.
	env.fog_enabled = stack_on and fog_on
	_update_hud()


func set_stack(on: bool) -> void:
	stack_on = on
	_apply_stack()


func set_snow(on: bool) -> void:
	"""N. The snow: the 3D field AND the props' own snow layer. The GROUND's shader layer
	stays at 0 whenever the field exists -- it is the milky veil the field replaces, and
	turning it back on here would put both under one key."""
	snow_on = on
	for m in _world_mats:
		if m == _ground_mat and snow != null:
			continue
		m.set_shader_parameter("snow_amount", 1.0 if on else 0.0)
	if snow != null:
		snow.set_visible_snow(on)
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
func _physics_process(_dt: float) -> void:
	# THE HEATHER'S WIND RUNS ON THE SNOW'S CLOCK: one time for the trail it reads and the gusts
	# it bends to, and a captured film is as deterministic as the snow is. Pushed HERE and not in
	# _process: park_camera() stops _process to hold a frame, the heather film parks the camera,
	# and the wind froze with it -- the first film measured 0.14 px of sway at p90.
	if snow != null and not _heather_mats.is_empty():
		var tw := snow.clock()
		for k in _heather_mats:
			(_heather_mats[k] as ShaderMaterial).set_shader_parameter("wind_time", tw)


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
func _shadow_reach(zoom: float) -> float:
	"""How far past the camera the shadow map must reach for this zoom: the standoff, the
	frame's own half-depth on the ground (screen height / tan(pitch) / 2, so 4.05 m at the play
	zoom), and 6 m for casters just outside the frame whose shadows fall in (0.70x a 3.4 m birch
	is 2.4 m). The old fixed 110 m put the whole scene in the shadow pass."""
	var half_depth: float = (float(_view_height()) / PPM / maxf(zoom, 1e-3)) \
		/ tan(deg_to_rad(PL_PITCH_DEG)) * 0.5
	return CAM_STANDOFF + half_depth + 6.0


func park_camera(aim: Vector3, zoom := 1.0) -> void:
	"""Stop following him and hold one frame. A measurement taken while the camera is easing
	toward a target measures the ease."""
	set_process(false)
	cam.size = (float(_view_height()) / PPM) / maxf(zoom, 1e-3)
	if sun != null:
		sun.directional_shadow_max_distance = _shadow_reach(zoom)
	_sync_post_scale()
	look_at_world(aim)
	if snowfall != null:
		snowfall.global_position = aim + up * 9.0 - fwd * 6.0


func unpark_camera() -> void:
	cam.size = float(_view_height()) / PPM
	if sun != null:
		sun.directional_shadow_max_distance = _shadow_reach(1.0)
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
		if is_instance_valid(mi):
			# a prop drawn by its MultiMesh keeps its own pen hidden -- showing it here would
			# draw that prop's line twice
			(mi as MeshInstance3D).visible = on and not (_instancing_on and _instanced_inks.has(mi))
	for l in _mm_inks:
		(l as Node3D).visible = on and _instancing_on


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
	fog_on = on
	env_node.environment.fog_enabled = stack_on and on


func place_knight(x: float, z: float, facing := "NE") -> void:
	knight.global_position = Vector3(x, world.height_at(x, z) + 0.03, z)
	knight.velocity = Vector3.ZERO
	knight.facing = facing
	knight._drive()


func snow_report() -> Dictionary:
	# the groups were gathered when the scene list was placed; props dropped since (T10-1d: the
	# rocks under the edge outcrops) are freed, and a freed mesh in the list stopped the
	# measurement with "Trying to cast a freed object" -- so the living ones only
	for g in _groups:
		g["meshes"] = (g["meshes"] as Array).filter(func(m): return is_instance_valid(m))
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
