extends Node3D
## C-9 T10-1b SNOW LAB — the smallest world that can prove the snow layer.
##
## A FLAT floor, two of the Barrow's own obstacles at their own measured coordinates, the
## Barrow's play camera, the Barrow's sun moved to 55 degrees, the Barrow's post stack, the
## Barrow's barbarian in full kit. Everything that is not the snow is copied rather than
## re-invented, so a difference in the frame is a difference in the snow.
##
## WHY THE OBSTACLES CARRY THE BARROW'S REAL COORDINATES rather than a tidy ring: the drop-in
## numbers this lab reports have to be the numbers the integration session pastes. A lab that
## measures a 2 m stone at the origin has measured a stone that does not exist.
##
## THE SUN IS AT 55 DEGREES AND ITS SHADOW BIAS IS NOT THE BARROW'S. paint_stack.winter_sun
## sets shadow_bias 0.13 / shadow_normal_bias 3.0, and its own comment says why: "A
## 17-DEGREE SUN IS THE WORST CASE FOR SHADOW BIAS. Grazing light turns a shadow-map texel of
## size s into a depth error of s/tan(17 deg) = 3.3 s." At 55 degrees 1/tan is 0.70 instead of
## 3.27, so the Barrow's bias is 4.7x more than this sun needs -- and an over-biased shadow
## detaches from its caster exactly at the contact point, which is where a drift meets a
## stone, which is acceptance criterion 2. The bias is therefore rescaled by
## tan(17)/tan(elev) rather than inherited. Reported as `sun` in the run report.

const PS := preload("res://scripts/paint_stack.gd")
const Knight := preload("res://scripts/knight.gd")

# --- the play camera, copied exactly from barrow_world.gd -------------------------
const PPM := 100.617553710938
const PL_PITCH_DEG := 52.95354112560294     # R-C9-68: the measured angle, not a rounded 53
const PL_YAW_DEG := 47.0
const CAM_STANDOFF := 60.0                  # not 220: fog and shadow cascades are measured
											# from the camera and both fail silently far out
const PLAY_M_PER_PX := 1.0 / PPM
const CAM_LIFT_PX := 55.0
const HULL_PX := 1.1
const PROP_SINK_M := 0.02
const SUN_ELEV_DEG := 55.0
const SUN_SCREEN_AZ_DEG := 305.0
const BARROW_SUN_ELEV_DEG := 17.0           # what winter_sun's bias numbers were tuned at

# 34 m and not 28. The play camera's footprint on the ground is a parallelogram whose world-xz
# bounding box is about 23 m across, so a 28 m field showed its own rim in the frame corners
# once the camera parked off-centre -- and with the snow casting shadows the raised rim threw a
# dark band onto the floor beyond it, which reads as a wall at the edge of the world.
const FIELD := Rect2(-17.0, -17.0, 34.0, 34.0)
const FLOOR_Y := 0.0
const WIND := Vector2(0.62, 0.78)
const SPAWN := Vector2(-1.2, 3.2)

var cam: Camera3D
var sun: DirectionalLight3D
var env_node: WorldEnvironment
var post_mat: ShaderMaterial
var post_q: MeshInstance3D
var knight: CharacterBody3D
var snow: SnowField
var right := Vector3.RIGHT
var up := Vector3.UP
var fwd := Vector3.FORWARD

var _fbm: Texture2D
var _paper: Texture2D
var _floor_mi: MeshInstance3D
var _world_mats: Array[ShaderMaterial] = []
var _char_saved := {}
var _props: Array = []
var _parked := false
var _report := {}
var _follow := true


func _ready() -> void:
	var t0 := Time.get_ticks_usec()
	_fbm = PS.make_fbm_texture(512, 7411, 4)
	_paper = PS.make_paper_texture(512)
	_build_camera()
	_build_light_and_air()
	_build_floor()
	_build_obstacles()
	_build_snow()
	await _build_knight()
	_build_post()
	_report["build_ms"] = snappedf((Time.get_ticks_usec() - t0) / 1000.0, 0.1)
	_report["snow_bake"] = snow.bake_report()
	_report["uploads"] = snow.upload_stats()


# =============================================================================
#  CAMERA — barrow_world.gd:196
# =============================================================================
func _build_camera() -> void:
	var p := deg_to_rad(PL_PITCH_DEG)
	var y := deg_to_rad(PL_YAW_DEG)
	var f := Vector3(-sin(y) * cos(p), -sin(p), -cos(y) * cos(p)).normalized()
	cam = Camera3D.new()
	cam.name = "PlayCamera"
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.size = float(_view_height()) / PPM      # 1080 / 100.6176 = 10.7337 m
	cam.near = 0.05
	cam.far = CAM_STANDOFF + 300.0
	add_child(cam)
	cam.look_at_from_position(-f * CAM_STANDOFF, Vector3.ZERO, Vector3.UP)
	cam.current = true
	var b := cam.global_transform.basis
	right = b.x
	up = b.y
	fwd = -b.z
	# the basis is ASSERTED, not assumed: knight.gd converts a canvas-space walk direction
	# into a ground velocity using exactly these three facts about it
	_report["camera"] = {
		"ortho_size_m": snappedf(cam.size, 0.0001),
		"rows": _view_height(),
		"m_per_px": snappedf(cam.size / float(_view_height()), 0.00001),
		"pitch_deg": PL_PITCH_DEG, "yaw_deg": PL_YAW_DEG,
		"assert_right_is_horizontal": snappedf(right.y, 0.00001),
		"assert_up_dot_worldup_minus_cos_pitch": snappedf(
			up.dot(Vector3.UP) - cos(deg_to_rad(PL_PITCH_DEG)), 0.00001),
	}


func _view_height() -> int:
	var vp := get_viewport()
	var h: int = vp.get_visible_rect().size.y if vp != null else 1080
	return h if h > 0 else 1080


func look_at_world(aim: Vector3) -> void:
	cam.look_at_from_position(aim - fwd * CAM_STANDOFF, aim, Vector3.UP)


func _aim_for(pos: Vector3) -> Vector3:
	return pos + up * (CAM_LIFT_PX / PPM)


func park_camera(aim: Vector3, zoom := 1.0) -> void:
	_parked = true
	cam.size = float(_view_height()) / PPM * zoom
	look_at_world(aim)
	_sync_post_scale()


func unpark_camera() -> void:
	_parked = false
	cam.size = float(_view_height()) / PPM
	_sync_post_scale()


func set_follow(on: bool) -> void:
	_follow = on


# =============================================================================
#  SUN AND AIR — barrow_world.gd:262
# =============================================================================
func _build_light_and_air() -> void:
	var lights := Node3D.new()
	lights.name = "Lights"
	add_child(lights)
	sun = PS.winter_sun(SUN_ELEV_DEG, SUN_SCREEN_AZ_DEG)
	# THE BIAS RESCALE. See the header: winter_sun's bias is correct for a 17-degree sun and
	# 4.7x too large for this one, and the symptom lands on the drift-to-stone contact.
	var k: float = tan(deg_to_rad(BARROW_SUN_ELEV_DEG)) / tan(deg_to_rad(SUN_ELEV_DEG))
	var bias0: float = sun.shadow_bias
	var nbias0: float = sun.shadow_normal_bias
	sun.shadow_bias = bias0 * k
	sun.shadow_normal_bias = nbias0 * k
	sun.directional_shadow_max_distance = CAM_STANDOFF + 50.0
	lights.add_child(sun)
	env_node = WorldEnvironment.new()
	env_node.name = "Env"
	# FOG DISTANCES ARE MEASURED FROM THE CAMERA, AND THE CAMERA STANDS OFF 60 m.
	# barrow_environment ships fog_depth_begin 34 / end 205, which are sensible numbers for a
	# camera near the action and put EVERY object in this scene inside the fog ramp -- an
	# orthographic camera does not betray the mistake by changing the picture's framing, so it
	# reads as a washed-out grade rather than as fog measured from the wrong place. Expressed
	# as "ahead of the aim point", the same way barrow_world.gd does it.
	env_node.environment = PS.barrow_environment({
		"fog_height": FLOOR_Y + 1.15,
		"fog_depth_begin": CAM_STANDOFF + 8.0,
		"fog_depth_end": CAM_STANDOFF + 105.0,
	})
	add_child(env_node)
	_report["sun"] = {
		"elev_deg": SUN_ELEV_DEG, "screen_az_deg": SUN_SCREEN_AZ_DEG,
		"energy": snappedf(sun.light_energy, 0.001),
		"bias_rescale_k": snappedf(k, 0.0001),
		"shadow_bias": [snappedf(bias0, 0.001), snappedf(sun.shadow_bias, 0.001)],
		"shadow_normal_bias": [snappedf(nbias0, 0.001), snappedf(sun.shadow_normal_bias, 0.001)],
		"_why": "winter_sun's bias is derived for 17 deg; 1/tan(17)=3.27 vs 1/tan(55)=0.70",
	}


func sun_reads() -> Dictionary:
	var sd := PS.sun_screen_dir(sun, cam)
	return {"screen_dir": [snappedf(sd.x, 0.001), snappedf(sd.y, 0.001)],
			"reads": "upper-left" if sd.x < 0.0 and sd.y > 0.0 else "NOT upper-left"}


# =============================================================================
#  THE FLAT FLOOR — note 1: this, and only this, is what he walks on
# =============================================================================
func _build_floor() -> void:
	var size := 90.0
	var pm := PlaneMesh.new()
	pm.size = Vector2(size, size)
	pm.subdivide_width = 8
	pm.subdivide_depth = 8
	_floor_mi = MeshInstance3D.new()
	_floor_mi.name = "FlatFloor"
	_floor_mi.mesh = pm
	_floor_mi.position = Vector3(0, FLOOR_Y, 0)
	# The ground's OWN procedural snow blend is turned DOWN here, not off: the 3D layer sits
	# on top of it and occludes it everywhere except beyond the field's rim, so leaving the
	# shader coverage at the Barrow's 0.50 would paint a white desert nobody can see under a
	# white layer nobody can see through. Beyond the rim it is the only snow there is.
	# THE FLOOR WEARS THE SAME PAINTED TILE AS THE SNOW, and it did not at first. The first
	# build gave it a flat cool base colour, so the snow field's 28 m rim showed as a hard
	# warm-to-cool boundary running diagonally across the frame -- a straight edge in the
	# middle of a snowfield, which reads as a seam in the world rather than as the edge of a
	# region. Matching the albedo makes the rim invisible even though the geometry still ends
	# there, which is the whole point of the edge taper.
	# WORLD_SHADER samples albedo_tex at UV * tex_scale, and PlaneMesh UV runs 0..1 across the
	# whole 90 m plane, so tex_scale is (plane metres / tile metres) and not a tiling count.
	var tile: Texture2D = null
	if ResourceLoader.exists("res://textures/barrow/snow.png"):
		tile = load("res://textures/barrow/snow.png")
	var m := PS.world_material(_fbm, Color(0.930, 0.902, 0.858), {
		"use_tex": tile != null,
		"tex_scale": size / 3.6,
		"snow_amount": 0.0, "snow_threshold": 0.30, "snow_jitter": 0.20,
		"snow_soft": 0.15, "snow_noise_scale": 0.52,
		"mottle_scale": 0.14, "mottle_amp": 0.075,
		"hatch_scale": 3.1, "hatch_amp": 0.030, "wash_amp": 0.11,
	})
	if tile != null:
		m.set_shader_parameter("albedo_tex", tile)
	_floor_mi.material_override = m
	_world_mats.append(m)
	add_child(_floor_mi)

	var body := StaticBody3D.new()
	body.name = "FloorBody"
	body.collision_layer = CliffWorld.TERRAIN_BIT   # knight.gd masks its ground query to this
	body.collision_mask = 0                         # terrain queries nothing
	var cs := CollisionShape3D.new()
	var box := BoxShape3D.new()
	# A BOX, NOT A WorldBoundaryShape3D and not a trimesh. A flat collider is the whole point
	# of note 1, and a box 2 m thick under the surface cannot be fallen through by a body
	# moving at run speed on a 24 Hz physics tick the way a zero-thickness plane can.
	box.size = Vector3(size, 2.0, size)
	cs.shape = box
	cs.position = Vector3(0, -1.0, 0)
	body.add_child(cs)
	add_child(body)
	_report["floor"] = {"walkable": "flat BoxShape3D, top at y = %.3f" % FLOOR_Y,
						"collision_layer": CliffWorld.TERRAIN_BIT,
						"slope_deg": 0.0, "snow_collision": "none -- the layer is visual only"}


# =============================================================================
#  OBSTACLES — the Barrow's own rows, sized the Barrow's own way
# =============================================================================
func _build_obstacles() -> void:
	var assets: Dictionary = _json("res://data/barrow_assets.json").get("models", {})
	var scene: Dictionary = _json("res://data/barrow_scene_a.json")
	var rows: Array = scene.get("instances", {}).get("height_a_authored", [])
	# stone_tall ships TWO identical rows -- same asset, same xz to the millimetre. Placing
	# both puts two 24k-triangle meshes in the same place: z-fighting on every facet plus the
	# hull pen drawn twice, which reads as a shader fault rather than as duplicated data.
	var seen := {}
	var want := ["stone_tall", "rock_large"]
	for row in rows:
		var cls := String(row.get("asset", ""))
		if not cls in want:
			continue
		var key := "%s@%.3f,%.3f" % [cls, float(row["scene_xz"][0]), float(row["scene_xz"][1])]
		if seen.has(key):
			_report["dropped_duplicate_rows"] = _report.get("dropped_duplicate_rows", [])
			_report["dropped_duplicate_rows"].append(key)
			continue
		seen[key] = true
		_place_prop(cls, assets.get(cls, {}), row)
	_report["obstacles"] = _props.map(func(p): return {
		"class": p["class"], "xz": [snappedf(p["pos"].x, 0.001), snappedf(p["pos"].z, 0.001)],
		"height_m": snappedf(p["height_m"], 0.001), "radius_m": snappedf(p["radius_m"], 0.001),
		"base_y": snappedf(p["pos"].y, 0.001)})


func _place_prop(cls: String, spec: Dictionary, row: Dictionary) -> void:
	var glb := String(spec.get("glb", ""))
	if glb == "" or not ResourceLoader.exists(glb):
		push_error("prop %s: no glb at %s" % [cls, glb])
		return
	var root: Node3D = (load(glb) as PackedScene).instantiate()
	var fit := Node3D.new()
	fit.name = cls
	fit.add_child(root)
	add_child(fit)

	var target := float(row.get("height_m", spec.get("height_m", 1.0)))
	var raw := _aabb_in(fit, root)
	# PITCH BEFORE NORMALISE, in that order, on the RAW unrotated bounds. Every Meshy model is
	# squat by 1/cos(52.95 deg) because its reference sheet was cropped out of a painting at
	# that pitch; correcting after the normalise stretches an already-fixed dimension and
	# makes the model too tall instead of the right shape.
	var pitch := 1.0 / cos(deg_to_rad(PL_PITCH_DEG))
	var sy: float = pitch if bool(spec.get("pitch_correct", true)) else 1.0
	var across := String(spec.get("axis", "height")) == "across"
	var k := 0.0
	if across:
		k = target / maxf(maxf(raw.size.x, raw.size.z), 1e-6)
	else:
		k = target / maxf(raw.size.y * sy, 1e-6)
	root.scale = Vector3(k, k * sy, k)
	# MEASURED IN `fit`'s SPACE, NOT `root`'s, AND THAT DISTINCTION BURIED EVERY STONE.
	# The offset below is written to root.position, which is expressed in fit's space, so the
	# box it is derived from must be too. Measuring in root's OWN space excludes root.scale,
	# so the correction was applied in unscaled model units and then multiplied by the fit
	# scale: the 2.71 m stone sank 0.875 m into the floor and the 1.07 m rock only 0.055 m --
	# every prop wrong, each by a different amount, in proportion to its own scale. It reads
	# as "the snow is too deep" rather than as "the props are in the wrong place", because the
	# thing you see is snow up the side of a stone.
	var b := _aabb_in(fit, root)
	root.position = Vector3(-(b.position.x + b.size.x * 0.5), -b.position.y,
							-(b.position.z + b.size.z * 0.5))
	var fin := _aabb_in(fit, root)
	# THE TURN, AFTER THE SIZING. Godot's AABB is world-axis-aligned, so a square post
	# measured at 45 degrees reports a box sqrt(2) too wide and normalising against it makes
	# the post 30% too thin.
	var yaw = row.get("yaw_deg", null)
	if yaw == null:
		yaw = spec.get("yaw_deg", 0.0)
	fit.rotation.y = deg_to_rad(float(yaw))
	var x := float(row["scene_xz"][0])
	var z := float(row["scene_xz"][1])
	fit.position = Vector3(x, FLOOR_Y - PROP_SINK_M, z)
	var r: float = maxf(maxf(fin.size.x, fin.size.z) * 0.5, 0.05)
	var params := {"snow_threshold": 0.58, "snow_jitter": 0.26, "snow_soft": 0.10,
				   "snow_noise_scale": 1.9, "mottle_scale": 1.5, "mottle_amp": 0.18,
				   "hatch_scale": 9.0, "hatch_amp": 0.07}
	if cls.begins_with("rock"):
		params = {"snow_threshold": 0.58, "snow_jitter": 0.30, "snow_soft": 0.11,
				  "snow_noise_scale": 2.4, "mottle_scale": 2.2, "mottle_amp": 0.18,
				  "hatch_scale": 11.0, "hatch_amp": 0.07}
	var saved: Dictionary = _adopt_prop(fit, HULL_PX / PPM, params)
	for e in saved.get("meshes", []):
		_world_mats.append((e["mi"] as MeshInstance3D).material_override as ShaderMaterial)
	_props.append({"class": cls, "node": fit, "pos": fit.position,
				   "height_m": target, "radius_m": r, "aabb": fin})


func _adopt_prop(node: Node3D, hull_world_m: float, params := {}) -> Dictionary:
	"""A LOCAL adopt_prop, and the reason is a version skew worth stating.

	paint_stack.gd was copied from git HEAD, per the brief, because the live file is mid-edit
	by the integration session. HEAD has no adopt_prop / ground_material / load_tile -- those
	arrived in the worktree during this run. Rather than copy a file that is being written to,
	the twenty lines this lab needs are here, built from the two HEAD helpers that do exist
	(world_material and hull_ink_material). Nothing in scripts/paint_stack.gd is modified.

	`hull_world_m` is DIVIDED BY THE NODE'S OWN SCALE: VERTEX += NORMAL * width happens in
	model space and the fit scale is applied after it, so a stone normalised to 2.71 m from a
	1.0 m export carries a scale of 2.71 and an undivided width draws a line 2.71x too thick
	on exactly the tallest stone in the frame."""
	var saved := {"meshes": [], "inks": []}
	for n in node.find_children("*", "MeshInstance3D", true, false):
		var mi := n as MeshInstance3D
		if mi.mesh == null or String(mi.name).ends_with("_ink"):
			continue
		var tex: Texture2D = null
		var act := mi.get_active_material(0) as BaseMaterial3D
		if act != null:
			tex = act.albedo_texture if act.albedo_texture != null else act.emission_texture
		var p := params.duplicate()
		p["use_tex"] = tex != null
		var ramp := PS.world_material(_fbm, Color(0.62, 0.60, 0.58), p)
		if tex != null:
			ramp.set_shader_parameter("albedo_tex", tex)
		saved["meshes"].append({"mi": mi, "mat": mi.material_override, "ramp": ramp})
		mi.material_override = ramp
		var sc: Vector3 = mi.global_transform.basis.get_scale()
		var s: float = maxf((absf(sc.x) + absf(sc.y) + absf(sc.z)) / 3.0, 1e-6)
		var line := MeshInstance3D.new()
		line.name = String(mi.name) + "_ink"
		line.mesh = mi.mesh
		line.material_override = PS.hull_ink_material(hull_world_m / s, PS.INK)
		line.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		mi.add_child(line)
		saved["inks"].append({"mi": line, "width_model": hull_world_m / s})
	return saved


func _aabb_in(ref: Node3D, from: Node3D) -> AABB:
	"""The bounds of every mesh under `from`, expressed in `ref`'s local space.

	The reference node is a PARAMETER and not `from` itself, because the two answers differ by
	`from`'s own scale and the caller needs whichever space the number it is about to write
	lives in. Excludes *_ink meshes: the hull pen is an inflated copy of the mesh, so measuring
	it would grow every prop by two line widths on every re-measure, compounding."""
	var out := AABB()
	var first := true
	var inv := ref.global_transform.affine_inverse()
	for n in from.find_children("*", "MeshInstance3D", true, false):
		var mi := n as MeshInstance3D
		if mi.mesh == null or String(mi.name).ends_with("_ink"):
			continue
		var w := (inv * mi.global_transform) * mi.mesh.get_aabb()
		out = w if first else out.merge(w)
		first = false
	return out


func obstacle_list() -> Array:
	"""EXACTLY WHAT SnowField.setup() WANTS. This is the call the integration session copies:
	the radius is MEASURED off the fitted AABB rather than computed from raw_aabb_m, because
	the fit applies a pitch correction and a normalise and the raw box knows about neither."""
	var out := []
	for p in _props:
		out.append({"pos": p["pos"], "radius_m": p["radius_m"], "height_m": p["height_m"]})
	return out


# =============================================================================
#  THE SNOW
# =============================================================================
func _build_snow() -> void:
	snow = SnowField.new()
	snow.name = "SnowField"
	add_child(snow)
	snow.setup(FIELD, FLOOR_Y, obstacle_list(), WIND)


func set_snow(on: bool) -> void:
	snow.set_visible_snow(on)


func set_ground_snow(amount: float) -> void:
	for m in _world_mats:
		m.set_shader_parameter("snow_amount", amount)


# =============================================================================
#  THE BARBARIAN — barrow_world.gd:1035
# =============================================================================
func _build_knight() -> void:
	var k: CharacterBody3D = Knight.new()
	k.name = "Knight"
	k.setup(right, up, fwd, 1.0)    # figure_scale 1.0: 1.85 m among stones that are 2.71
	add_child(k)
	knight = k
	await get_tree().physics_frame
	k.set_figure_scale(1.0)
	k.global_position = Vector3(SPAWN.x, FLOOR_Y + 0.03, SPAWN.y)
	k.facing = "NE"
	k.set_gear_stack(k.gear_stack_count() - 1)   # full kit: helmet bracers byrnie mantle axe shield
	_char_saved = PS.adopt_character(k, _fbm, PS.INK, {
		"wash_scale": 2.6, "wash_amp": 0.13, "band_soft": 0.075,
	})
	# THE SNOW FINDS HIS FEET THROUGH HIS SKELETON. No hook in knight.gd, which is owned by a
	# concurrent workstream and is not touched: track() walks the node tree for the
	# Skeleton3D and reads the bone names off the rig.
	snow.track(k)
	look_at_world(_aim_for(k.global_position))
	_report["character"] = {"figure_scale": 1.0, "gear_stack": k.gear_stack,
							"gear_stacks": k.gear_stack_count(), "armed": k.armed()}


func place_knight(x: float, z: float, facing := "NE") -> void:
	knight.global_position = Vector3(x, FLOOR_Y + 0.03, z)
	knight.facing = facing
	knight.velocity = Vector3.ZERO
	look_at_world(_aim_for(knight.global_position))


func canvas_dir_for_world(w: Vector3) -> Vector2:
	"""The inverse of knight.gd's canvas_velocity_to_world, so a scripted route can be written
	in WORLD metres ("walk to the stone") instead of in canvas pixels.

	knight.gd:  world = right * (v.x/PPM) + lz * ((v.y/PPM) / sin(pitch))
	Both `right` and `lz` lie in the xz plane, so this is a 2x2 solve and not an optimisation.
	Driving a world route with a hand-guessed canvas vector is how a route ends up walking
	past its target at a constant small angle -- which looks like a pathing choice."""
	var lz := Vector3(sin(deg_to_rad(PL_YAW_DEG)), 0.0, cos(deg_to_rad(PL_YAW_DEG)))
	var k: float = maxf(-lz.dot(up), 1e-6)          # = sin(pitch)
	var det: float = right.x * lz.z - lz.x * right.z
	if absf(det) < 1e-9:
		return Vector2(0, 1)
	var a: float = (w.x * lz.z - lz.x * w.z) / det
	var b: float = (right.x * w.z - w.x * right.z) / det
	return Vector2(a * PPM, b * k * PPM).normalized()


func walk_toward(target: Vector2, running: bool, dt: float) -> float:
	"""One physics step toward a world xz target. Returns the remaining distance, so the caller
	can stop on arrival rather than on a frame count."""
	var here := Vector2(knight.global_position.x, knight.global_position.z)
	var d := target - here
	if d.length() < 0.12:
		knight.drive_dir(Vector2.ZERO, false, dt)
		return 0.0
	knight.drive_dir(canvas_dir_for_world(Vector3(d.x, 0.0, d.y).normalized()), running, dt)
	return d.length()


func deepest_drift(within_m := 7.0, avoid_obstacles_m := 1.2) -> Dictionary:
	"""Find the deepest reachable drift, so the scripted walk PLOUGHS THROUGH ONE rather than
	being authored to coordinates that a different field seed puts open ground at."""
	var best := {"xz": Vector2.ZERO, "depth_m": 0.0}
	var step := 0.25
	var x := -within_m
	while x <= within_m:
		var z := -within_m
		while z <= within_m:
			var p := Vector2(x, z)
			var ok := true
			for o in _props:
				var c: Vector3 = o["pos"]
				if p.distance_to(Vector2(c.x, c.z)) < float(o["radius_m"]) + avoid_obstacles_m:
					ok = false
					break
			if ok:
				var d := snow.depth_at(p)
				if d > float(best["depth_m"]):
					best = {"xz": p, "depth_m": d}
			z += step
		x += step
	return best


func shallowest_open(within_m := 9.0) -> Dictionary:
	var best := {"xz": Vector2.ZERO, "depth_m": 1e9}
	var step := 0.25
	var x := -within_m
	while x <= within_m:
		var z := -within_m
		while z <= within_m:
			var p := Vector2(x, z)
			var d := snow.depth_at(p)
			if d < float(best["depth_m"]):
				best = {"xz": p, "depth_m": d}
			z += step
		x += step
	return best


func stance_foot_pos() -> Vector3:
	"""The lower foot's world position. The close-up is aimed HERE and not at the body origin:
	aimed at the origin the frame centres on his hips, and in the armed idle the shield hangs
	across his legs from above -- the deliverable called 'his feet in the snow' came back as a
	picture of a shield."""
	var skel: Skeleton3D = _find(knight, "Skeleton3D") as Skeleton3D
	if skel == null:
		return knight.global_position
	var best := Vector3.INF
	for nm in ["LeftToeBase", "RightToeBase", "LeftFoot", "RightFoot"]:
		var i := skel.find_bone(nm)
		if i < 0:
			continue
		var p: Vector3 = skel.global_transform * skel.get_bone_global_pose(i).origin
		if best == Vector3.INF or p.y < best.y:
			best = p
	return knight.global_position if best == Vector3.INF else best


func bone_heights() -> Dictionary:
	"""Ankle, knee and sole in metres above the floor, read out of the live Skeleton3D. These
	are the numbers the sink acceptance is measured AGAINST, so they are measured and not
	assumed: a 1.85 m model's ankle is not 0.10 m up just because a person's is."""
	var skel: Skeleton3D = _find(knight, "Skeleton3D") as Skeleton3D
	if skel == null:
		return {}
	var out := {}
	for nm in ["LeftFoot", "RightFoot", "LeftToeBase", "RightToeBase", "LeftLeg", "RightLeg",
			   "LeftUpLeg", "Hips"]:
		var i := skel.find_bone(nm)
		if i >= 0:
			var p: Vector3 = skel.global_transform * skel.get_bone_global_pose(i).origin
			out[nm] = snappedf(p.y - FLOOR_Y, 0.001)
	# THE SOLE IS READ OFF THE PHYSICS BODY, NOT OFF A MESH AABB, and the first version did the
	# latter. Two things were wrong with it and they pushed opposite ways:
	#   - mesh.get_aabb() on a SKINNED mesh is the REST-POSE bound, not the animated one, so it
	#     does not move when he does;
	#   - it ran over EVERY mesh under him, so the lowest vertex was as likely to be the hem of
	#     the mantle or the rim of the shield as the bottom of a boot.
	# It returned -0.001 m, which looked like a perfect answer and was a coincidence of two
	# errors. The capsule's bottom sits exactly at the body origin (shape.position.y =
	# height/2), and move_and_slide puts that on the floor, so global_position.y IS the sole
	# plane and is_on_floor() is the evidence that it is resting there.
	out["sole_y"] = snappedf(knight.global_position.y - FLOOR_Y, 0.001)
	out["is_on_floor"] = knight.is_on_floor()
	out["bone_count"] = skel.get_bone_count()
	# THE STANCE LEG, not "the left leg". Even in idle the rig has one leg carrying and one
	# lifted: measured live, LeftFoot sat at 0.361 m and RightFoot at 0.298 m, and the knee of
	# the LIFTED leg read 1.10 m -- which made a 0.57 m drift look like it barely passed his
	# shin when the planted knee was half that height. "How deep is it on him" is a question
	# about the leg he is standing on, so it is the MINIMUM of the pair.
	out["ankle_stance_m"] = snappedf(minf(float(out.get("LeftFoot", 9.0)),
										  float(out.get("RightFoot", 9.0))), 0.001)
	out["knee_stance_m"] = snappedf(minf(float(out.get("LeftLeg", 9.0)),
										 float(out.get("RightLeg", 9.0))), 0.001)
	return out


func _find(n: Node, cls: String) -> Node:
	if n.is_class(cls):
		return n
	for c in n.get_children():
		var r := _find(c, cls)
		if r != null:
			return r
	return null


# =============================================================================
#  POST STACK — barrow_world.gd:1072
# =============================================================================
## Which depth operator the ink pass uses. "first" is what git HEAD's POST_SHADER ships;
## "second" is the operator the integration session has adopted in the live file.
var ink_operator := "second"

const POST_PARAMS := {
	"line_px": 1.25,
	"depth_edge_px": 3.0,
	"normal_edge": 1.05,
	"normal_weight": 0.30,
	"ink_gain": 1.15,
}

func _build_post() -> void:
	post_mat = PS.post_material(_paper, PS.INK, POST_PARAMS.duplicate())
	post_mat.set_shader_parameter("ref_m_per_px", PLAY_M_PER_PX)
	set_ink_operator(ink_operator)
	_sync_post_scale()
	post_q = PS.post_quad(cam, post_mat)


# --- THE TWO DEPTH OPERATORS, AND WHY THE INK NUMBER IS REPORTED AGAINST BOTH -----
#
# The ink acceptance ("the snow's soft undulations must NOT grow contour lines") has a
# completely different answer under the two operators, and the copy of paint_stack.gd this lab
# holds is NOT the one the Barrow will ship.
#
#   FIRST DIFFERENCE (git HEAD):  gd = |d11 - d00|, thresh = depth_edge_px*m_per_px
#                                                            + planar*slope_slack
#     A first difference measures HOW FAST depth changes, so a silhouette and a raked slope
#     are the same reading, and the `planar` term exists to subtract the slope's share. That
#     term divides by the view-space normal's z -- which goes to zero at a silhouette, i.e.
#     exactly where it is needed. A SLOPING SNOW SURFACE IS THE CASE THIS OPERATOR IS WORST AT.
#
#   SECOND DIFFERENCE (the live file): gd = |d(u+o) + d(u-o) - 2*d(u)|, thresh = px*m_per_px
#     For ANY plane at ANY rake this is identically zero. Curvature gives a little, a depth
#     DISCONTINUITY gives metres. Smooth snow is structurally near-invisible to it.
#
# Measuring only against HEAD would report a failure caused by an operator that is being
# replaced this week; measuring only against the live one would hide how much of the snow's
# safety is borrowed from someone else's in-flight fix. So both numbers are reported, each
# labelled. The swap below is a surgical substitution on HEAD's own source with an assertion
# that the expected text was found -- it is not a re-implementation, and if HEAD's shader
# changes shape the assert fails loudly instead of silently measuring the wrong thing.
const _FIRST_DIFF_BLOCK := """		float gd = max(abs(d11 - d00), abs(d10 - d01));
		vec3 nc = _nrm(uv);
		// what a locally FLAT surface carrying this normal would produce across the span
		float planar = (abs(nc.x) + abs(nc.y)) / max(abs(nc.z), 0.12) * m_per_px * span_px;
		float thresh = depth_edge_px * m_per_px + planar * slope_slack;"""

const _SECOND_DIFF_BLOCK := """		float dxp = _lin_depth(uv + vec2(o.x, 0.0), INV_PROJECTION_MATRIX);
		float dxm = _lin_depth(uv - vec2(o.x, 0.0), INV_PROJECTION_MATRIX);
		float dyp = _lin_depth(uv + vec2(0.0, o.y), INV_PROJECTION_MATRIX);
		float dym = _lin_depth(uv - vec2(0.0, o.y), INV_PROJECTION_MATRIX);
		float gd = max(abs(dxp + dxm - 2.0 * dc), abs(dyp + dym - 2.0 * dc));
		float thresh = depth_edge_px * m_per_px;"""


func set_ink_operator(which: String) -> void:
	ink_operator = which
	var code: String = PS.POST_SHADER
	if which == "second":
		assert(code.find(_FIRST_DIFF_BLOCK) >= 0,
			"POST_SHADER's first-difference block is not where this swap expects it")
		code = code.replace(_FIRST_DIFF_BLOCK, _SECOND_DIFF_BLOCK)
	var sh := Shader.new()
	sh.code = code
	post_mat.shader = sh
	# a shader swap drops every parameter, so they are re-pushed rather than assumed
	post_mat.set_shader_parameter("paper_tex", _paper)
	post_mat.set_shader_parameter("ink_color", PS.INK)
	post_mat.set_shader_parameter("ref_m_per_px", PLAY_M_PER_PX)
	for k in POST_PARAMS:
		post_mat.set_shader_parameter(k, POST_PARAMS[k])
	_sync_post_scale()


func _sync_post_scale() -> void:
	if post_mat != null:
		post_mat.set_shader_parameter("m_per_px", cam.size / maxf(float(_view_height()), 1.0))


func set_ink(on: bool) -> void:
	post_mat.set_shader_parameter("ink_on", 1.0 if on else 0.0)


func set_grade(on: bool) -> void:
	post_mat.set_shader_parameter("grade_on", 1.0 if on else 0.0)


func set_post_param(k: String, v) -> void:
	post_mat.set_shader_parameter(k, v)


func set_stack(on: bool) -> void:
	# HIDE the quad rather than neutralise it: with ink_on and grade_on at 0 the pass still
	# copies the screen and blits it back -- invisible, and about a millisecond of it, which
	# would land on the "off" side of an A/B and make the measured cost short by exactly the
	# amount being measured.
	post_q.visible = on
	PS.set_character_ramp(_char_saved, on)
	for m in _world_mats:
		m.set_shader_parameter("ramp_mix", 1.0 if on else 0.0)
	snow.material().set_shader_parameter("ramp_mix", 1.0 if on else 0.0)


func report() -> Dictionary:
	var r := _report.duplicate(true)
	r["sun_reads"] = sun_reads()
	return r


# =============================================================================
#  ISOLATION FOR THE INK MASK — show the snow and nothing else, flat
# =============================================================================
var _mask_mat: ShaderMaterial
var _hidden: Array = []

func begin_snow_mask() -> void:
	"""The snow flat magenta, the post pass off, AND NOTHING HIDDEN. What comes back is the set
	of pixels the snow owns -- the denominator of the ink measurement.

	THE MASK IS GREEN AND NOT MAGENTA, and that is not a preference. GODOT'S SHADER-COMPILE-
	ERROR MATERIAL IS MAGENTA. The first version masked on magenta, and when a stray comment
	broke the snow shader the whole layer rendered in Godot's error colour -- so the mask still
	found ~1.97 million "snow" pixels, the ink pass found almost no edges on a flat untextured
	surface, and the run reported 0.24% inked, a passing frame cost, and a control delta that
	had collapsed from 8178 px to 352. Every number came back cleanly and none of them was
	about the snow. Green cannot collide with the error material.

	NOTHING IS HIDDEN, and the first version of this hid everything but the snow. That version
	OVER-COUNTED, and in the one direction that matters: with the stones hidden, snow rendered
	into the pixels the stones occupy, so those pixels entered the mask -- and in the real
	frames they contain a STONE, complete with its hull pen and its silhouette against the sky.
	The instrument was charging the snow for the obstacles' own ink, which criterion 6
	explicitly wants kept ("where an object meets the snow, its own line stays"). Leaving
	everything visible lets the obstacles occlude properly, and the magenta test isolates the
	snow anyway: no painted stone, hide nor sky is (r>128, b>128, g<90)."""
	_hidden.clear()
	post_q.visible = false
	if _mask_mat == null:
		# The mask shader repeats the DISPLACEMENT and drops everything else. It must repeat
		# the displacement exactly -- a flat plane here would mask the wrong pixels along
		# every drift silhouette, and those are precisely the pixels in question.
		var sh := Shader.new()
		sh.code = _flat_snow_shader()
		_mask_mat = ShaderMaterial.new()
		_mask_mat.shader = sh
	# RE-PUSHED EVERY TIME, not only on creation. The ink CONTROL re-bakes the field, which
	# builds NEW field and trail textures; a mask material caching the old ones would mask the
	# pre-control snow and the control would compare two different surfaces.
	for key in ["area_size", "refill_s", "base_depth_m", "residual_m", "berm_frac"]:
		_mask_mat.set_shader_parameter(key, snow.material().get_shader_parameter(key))
	_mask_mat.set_shader_parameter("field_tex", snow.field_texture())
	_mask_mat.set_shader_parameter("trail_tex", snow.trail_texture())
	_mask_mat.set_shader_parameter("now_s", snow.clock())
	snow.surface().material_override = _mask_mat


func end_snow_mask() -> void:
	for n in _hidden:
		(n as Node3D).visible = true
	_hidden.clear()
	post_q.visible = true
	snow.surface().material_override = snow.material()


func rebake_snow(step_m := 0.0, step_x := 0.0) -> void:
	"""Re-bake the field, optionally with a hard step cut across it for the ink control."""
	snow.debug_step_m = step_m
	snow.debug_step_x = step_x
	snow.setup(FIELD, FLOOR_Y, obstacle_list(), WIND)
	snow.track(knight)


func prop_rows() -> Array:
	return _props


func _flat_snow_shader() -> String:
	return """
shader_type spatial;
render_mode unshaded, cull_back;
uniform sampler2D field_tex : filter_linear, repeat_disable;
uniform sampler2D trail_tex : filter_linear, repeat_disable;
uniform vec2 area_size;
uniform float base_depth_m = 0.12;
uniform float residual_m = 0.016;
uniform float berm_frac = 0.38;
uniform float refill_s = 60.0;
uniform float now_s = 0.0;
void vertex() {
	vec4 f = texture(field_tex, UV);
	vec4 t = texture(trail_tex, UV);
	float fade = clamp(1.0 - (now_s - t.g) / max(refill_s, 1e-3), 0.0, 1.0);
	float p = clamp(t.r * fade, 0.0, 1.0);
	float b = clamp(t.b * fade, 0.0, 1.0);
	VERTEX.y += mix(f.r, residual_m, p) + berm_frac * b * f.r;
}
void fragment() { ALBEDO = vec3(0.0, 1.0, 0.0); }
"""


# =============================================================================
#  DRIVING
# =============================================================================
func _physics_process(dt: float) -> void:
	if knight == null or not knight.is_physics_processing():
		return
	var d := Vector2(
		Input.get_action_strength("move_right") - Input.get_action_strength("move_left"),
		Input.get_action_strength("move_down") - Input.get_action_strength("move_up"))
	knight.drive_dir(d, Input.is_action_pressed("run_modifier"), dt)
	if _follow and not _parked:
		look_at_world(_aim_for(knight.global_position))


func _input(e: InputEvent) -> void:
	if e.is_action_pressed("snow_toggle"):
		snow.set_visible_snow(not snow.get_node("SnowSurface").visible)
	elif e.is_action_pressed("ink_toggle"):
		var on: float = post_mat.get_shader_parameter("ink_on")
		set_ink(on < 0.5)
	elif e.is_action_pressed("gear_cycle"):
		knight.cycle_gear()


func _process(_dt: float) -> void:
	if _follow and not _parked and knight != null:
		look_at_world(_aim_for(knight.global_position))


static func _json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var f := FileAccess.open(path, FileAccess.READ)
	var d = JSON.parse_string(f.get_as_text())
	return d if d is Dictionary else {}
