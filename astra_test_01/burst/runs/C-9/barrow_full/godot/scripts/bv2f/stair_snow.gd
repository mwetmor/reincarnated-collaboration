extends RefCounted
## BV2F lane PT, DEV-22 (R-C9-216): THE STAIR'S TREAD SNOW -- true 3D snow on each tread top of the sea-cave stair,
## bare stone fronts (sketch A's look), his footprints and puffs as he climbs. It is DEV-18's terrain snow
## (scripts/bv2f/snow_field_terrain.gd, v1's SnowField subclassed, v1's snow_field.gd untouched) as a SECOND field over
## the stair alone, fed the grids fid/pt/tools/stair_snow_prep.py writes (data/bv2f/stair_snow/): depth on the tread
## tops only (the fronts are cut), the ground height = each tread's top. Same depth, shader and footprints as the
## terrain snow. Painted (the full site, later): pass the painting -- PaintedWorld.snow_shader_code(), its base the
## painting beneath, as the pilot's terrain snow. Unpainted (LV's blockout, the test): v1's own snow shader.

const SNOW_TERRAIN := preload("res://scripts/bv2f/snow_field_terrain.gd")
const DATA := "res://data/bv2f/stair_snow/"
## the walk surface is a ramp through the nosings (LV's route.walk_boxes stair_ramp): mid-tread his foot stands up to
## about half a rise over the tread top -- the stamp's lift test is widened to that (v1's 0.13 for flat ground)
const LIFT_MAX_M := 0.30


static func _f32(path: String, want: String, rep: Dictionary) -> PackedFloat32Array:
	var ok := FileAccess.get_sha256(path) == want
	rep[path] = {"sha256_ok": ok}
	if not ok:
		push_error("stair_snow: %s sha mismatch" % path)
		return PackedFloat32Array()
	return FileAccess.get_file_as_bytes(path).to_float32_array()


static func build(parent: Node, knight: Node3D, fbm: Texture2D, wind: Vector2, painted := {}, data := DATA) -> SnowField:
	"""The stair's snow field, added under `parent`, tracking `knight`. `painted` = {} (v1's shader) or
	{"paint_tex": Texture2D, "lit": Texture2D, "shadow_mul": Vector3, "u_hat": Vector3, "v_hat": Vector3,
	 "g_frame": Vector3, "g_size": Vector2} (the painting's snow, PaintedWorld's projection re-bound to that frame)."""
	var j = JSON.parse_string(FileAccess.get_file_as_string(data + "stair_snow.json"))
	if typeof(j) != TYPE_DICTIONARY:
		push_error("stair_snow: no %sstair_snow.json" % data)
		return null
	var man: Dictionary = j
	var rep := {}
	var nx := int(man["nx"])
	var nz := int(man["nz"])
	var grid := _f32(data + String(man["grid"]["file"]), String(man["grid"]["sha256"]), rep)
	var gh := _f32(data + String(man["ground_h"]["file"]), String(man["ground_h"]["sha256"]), rep)
	if grid.size() != 2 * nx * nz or gh.size() != nx * nz:
		push_error("stair_snow: grid sizes %d / %d, want %d / %d" % [grid.size(), gh.size(), 2 * nx * nz, nx * nz])
		return null
	var ar: Array = man["area_xz"]
	var origin := Vector2(float(ar[0]), float(ar[1]))
	var s: SnowField = SNOW_TERRAIN.new()
	s.name = "StairSnow"
	s.set_ground_height(gh, origin, float(man["cell_m"]), nx, nz)
	s.lift_max_m = LIFT_MAX_M
	s.fbm_tex = fbm
	s.field_px = int(man["field_px"])
	s.trail_px = 1024
	s.grid_quad_m = float(man.get("grid_quad_m", 0.04))
	var prof_try: PackedStringArray = OS.get_environment("BV2F_PROF_TRY").split(",", false)   # R-C9-254 profiling only
	if prof_try.has("staircoarse"):
		s.grid_quad_m *= 2.0
	s.windrow_count = 0
	s.pile_count = 0
	s.cast_shadows = false
	s.depth_grid = {"origin": origin, "cell_m": float(man["cell_m"]), "nx": nx, "nz": nz,
					"mul": grid.slice(0, nx * nz), "trod": grid.slice(nx * nz, 2 * nx * nz)}
	if not painted.is_empty():
		s.shader_code_override = PaintedWorld.snow_shader_code()
	s.setup(Rect2(origin.x, origin.y, float(ar[2]), float(ar[3])), 0.0, [], wind)
	parent.add_child(s)
	if knight != null and not prof_try.has("stairnotrack"):
		s.track(knight)
	if not painted.is_empty():
		var m := s.material()
		m.set_shader_parameter("paint_tex", painted["paint_tex"])
		PaintedWorld.bind_projection(m, painted["lit"], painted["shadow_mul"], painted["u_hat"], painted["v_hat"])
		if painted.has("g_frame"):
			m.set_shader_parameter("g_frame", painted["g_frame"])
			m.set_shader_parameter("g_size", painted["g_size"])
		s.surface().layers = PaintedWorld.LAYER_ON_PAINT
	s.set_meta("dev22", {"treads": man["treads"], "source": man["source"], "loads": rep, "bake": s.bake_report()})
	return s
