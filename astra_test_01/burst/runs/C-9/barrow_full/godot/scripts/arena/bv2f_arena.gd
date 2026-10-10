extends "res://scripts/bv2f/bv2f_pilot.gd"
## C-9 BV2F ARENA (R-C9-345/347/348) -- the full painted barrow_v2 site (bv2f_pilot.gd on site_ph3, inherited unchanged:
## the same level, paint, camera -- ortho, pitch 52.95354, yaw 47 -- light, water, heather and snow) HOSTING the KC2
## wave fight (scripts/arena/arena_mode.gd). A THIN SCENE THAT EXTENDS THE WALK: scenes/bv2f_pilot_painted.tscn is not
## touched and its default behaviour is unchanged; this scene (scenes/bv2f_arena.tscn) differs only by
##   * the site pinned to site_ph3 (the arena's coordinates are that level's),
##   * no 3D knight (skip_character): the hero is the KC2 warlord, driven by the KC2 controls,
##   * the walk's own HUD hidden and its keys (R/H/N/...) handed to the fight.


func _init() -> void:
	# the arena is laid out on site_ph3's level: pin it whatever BV2F_PILOT says
	pilot_set = "site_ph3"
	PILOT_PX = PILOT_WINDOWS["site_ph3"]
	PILOT_REL = "../bv2f/%s/painted/" % pilot_set
	PILOT_MANIFEST = "res://data/bv2f/%s/painted/manifest.json" % pilot_set
	PILOT_LEVEL_DIR = "res://data/bv2f/%s/level/" % pilot_set
	BV2F_DATA = PILOT_LEVEL_DIR


var arena: Node3D = null


func _ready() -> void:
	await super._ready()
	set_hud_visible(false)
	# R-C9-353 (Matt: the load "stays ... in the bottom-right corner ... where all you see is the lack of map"): the
	# pilot's shader warm-up ends parked on the LAST view of its grid (the window's far corner), and the fight's
	# session then loads for seconds in front of it. So: the camera goes to the warlord's start NOW, under a plain
	# "loading the fight" card, and two frames are presented before the session opens.
	var j: Variant = JSON.parse_string(FileAccess.get_file_as_string("res://data/arena/barrow_arena.json"))
	if typeof(j) == TYPE_DICTIONARY:
		var t: Array = (j as Dictionary)["fight_centre_sim"]
		set_process(false)
		look_at_world(aim_for(uv_to_world(float(t[0]), -float(t[1]), floor_y_at(float(t[0]), -float(t[1])))))
	var card := CanvasLayer.new()
	card.layer = 120
	var lb := Label.new()
	lb.text = "Loading the fight..."
	lb.add_theme_font_size_override("font_size", 28)
	lb.add_theme_color_override("font_color", Color(1, 0.93, 0.8))
	lb.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.8))
	lb.set_anchors_preset(Control.PRESET_CENTER)
	lb.position = Vector2(-120, -20)
	card.add_child(lb)
	add_child(card)
	await get_tree().process_frame
	await get_tree().process_frame
	arena = load("res://scripts/arena/arena_mode.gd").new()
	arena.name = "Arena"
	add_child(arena)
	arena.setup(self)
	card.queue_free()
	print("[bv2f_arena] site %s, arena %s" % [pilot_set, "up" if arena.fatal == "" else "REFUSED: " + String(arena.fatal)])


func _unhandled_input(e: InputEvent) -> void:
	if arena != null:
		arena.handle_input(e)


func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_CLOSE_REQUEST and arena != null:
		arena._close_recording("window_closed")


# ============================================================================================================
# R-C9-368 (Matt: "the exact barrow_v1's snow ... especially with the snow drifts/banks"): THE ARENA'S SNOW = THE
# INSTALLED BARROW'S (cliffside3d godot/scripts/barrow_world.gd, "barrow v1"), not the painted pilot's.
#   FINDING: the painted Barrow (barrow_full.gd _build_painted_snow) DROPPED v1's drift system on purpose ("no
#   windrows, piles or skirts -- a drift the painting does not show would hide his legs"), and the pilot's DEV-18 is a
#   FAITHFUL copy of that painted function + terrain height. So v2 lost the drifts with the painted v1, not in DEV-18.
#   Depth is the same law (base 0.12 m x SNOW_BY_CLASS) -- but v2's field spans 86.2 m on the same 768 px (11.2 cm a
#   texel; v1 34 m on 512 = 6.6 cm) and its trail 86.2 m on 1024 px (8.4 cm; v1 3.3 cm), so prints and ploughs were
#   drawn 2.5x coarser and read shallow.
#   THE ARENA (variant-side; the walk scene's _build_painted_snow is untouched): v1's SnowField law -- its default
#   windrows and piles at v1's DENSITY (counts scaled by the area ratio), a drift SKIRT on every obstacle (v1's rule:
#   every placed prop and the mound; here every rock, stone, post, log, the mast, and the buildings' footprints
#   as a chain of 1.5 m discs), lee tails down the Barrow's wind -- on v2's own depth grid and terrain, at v1's texel
#   density over the fight's square (SNOW_AREA_M around the fight centre).
# ============================================================================================================
const ARENA_SNOW_AREA_M := 72.0
const V1_SNOW_AREA_M := 34.0
const V1_WINDROWS := 10
const V1_PILES := 15
const V1_FIELD_PX_PER_M := 512.0 / 34.0
const V1_TRAIL_PX_PER_M := 1024.0 / 34.0
const V1_SNOW_TINT := Color(1.026, 1.101, 1.174)    # barrow_world.gd SNOW_TINT
const V1_SNOW_TILE := "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/cliffside3d/godot/textures/barrow/snow.png"
## THE FEATHER (R-C9-368 defect a: walls of snow): v2's depth grid comes off a discrete class map, so it steps 1 -> 0 in
## one 0.1 m cell at every class edge, and v1's law then extrudes a vertical face there; it also lays full depth right
## up to terrain steps and ledges. So, before the field bakes: no snow where the ground itself is steep (a ramp from
## STEEP_LO to STEEP_HI rise-per-metre), then the depth multiplier box-blurred FEATHER_M (two passes, ~ a tent) so
## every edge -- class edges, steps, ledges -- runs out to nothing.
const STEEP_LO := 0.35
const STEEP_HI := 0.75
const FEATHER_M := 0.7
## R-C9-371: inside the excluded features (the mound, the wreck basin) the snow leaves the slopes sooner -- the mound's
## flank carried a smooth stretched sheet of snow over its heather (a "bank" by eye); the flat ground is unchanged
const ZONE_STEEP_LO := 0.15
const ZONE_STEEP_HI := 0.35
const SNOW_OBSTACLE_IDS := ["ring_stones", "slope_stones", "ring_fallen", "logs", "wreck_mast", "door_post_L", "door_post_R",
	"talus", "gully_rock", "crags", "sea_stacks", "palisade", "ledge_rocks"]
const SNOW_BUILDING_IDS := ["longhall", "fallen_gable"]
## R-C9-371 (Matt: "odd snow banks ... to the left and right of the barrow and to the right of the shipwreck"): FOUND by
## baking with each drift source dropped (`--arenasnow-drop`, stills in captures/snow_banks/): the bank left of the barrow
## door and the one over the cobbles right of the wreck were the AABB-RIM SKIRT CHAINS of barrow_front and wreck (a
## rotated wreck's AABB rim runs metres off its hull, out over the basin's edge); the door posts' and ring stones' skirts
## and random windrows/piles added to the barrow's flanks. So the LARGE TERRAIN FEATURES are EXCLUDED, structurally:
## barrow_front and wreck lay no rim chain, and inside these discs (barrow sim centre, radius m) no obstacle lays a skirt
## and no windrow or pile is placed. The depth grid's own base snow is unchanged.
const SNOW_EXCLUDE := [
	{"id": "mound", "c": Vector2(2.0, -21.0), "r": 11.5},          # barrow_front (2, -22.36), 15 x 10.5, + its lobe
	{"id": "wreck_basin", "c": Vector2(-27.1, -2.9), "r": 10.0},   # the wreck (13 x 4.6, rot 32.5) and its basin
]
var arena_snow_report := {}


func _build_painted_snow(man: Dictionary, ground_tex: Texture2D, lit: Texture2D, shadow_mul: Vector3) -> void:
	var sn: Dictionary = man["snow"]
	var g: Dictionary = sn["grid"]
	var buf := PaintedWorld.load_f32_bin(String(g["file"]), String(g["sha256"]), paint["loads"])
	var nx := int(g["nx"])
	var nz := int(g["nz"])
	if buf.size() != 2 * nx * nz:
		push_error("bv2f_arena: the snow grid is %d floats, not %d" % [buf.size(), 2 * nx * nz])
		return
	var go: Array = g["origin_xz"]
	snow = SNOW_TERRAIN.new()
	var ghd: Dictionary = sn.get("ground_h", {})
	if not ghd.is_empty():
		var ghb := PaintedWorld.load_f32_bin(String(ghd["file"]), String(ghd["sha256"]), paint["loads"])
		snow.set_ground_height(ghb, Vector2(float(go[0]), float(go[1])), float(g["cell_m"]), nx, nz)
	snow.name = "SnowField"
	snow.fbm_tex = fbm
	# v1's texel density over the fight's square
	# THE FIELD SPANS THE SITE'S OWN SNOW AREA (manifest area_xz): the depth grid and the terrain-height grid
	#   (DEV-18's ground_h_tex, sampled by the mesh UV) are laid over exactly that square -- a different square
	#   misreads the ground height and floats slabs of snow (the first try did).
	var ar: Array = sn["area_xz"]
	var side := float(ar[2])
	snow.field_px = int(ceil(side * V1_FIELD_PX_PER_M / 64.0)) * 64
	# a whole number of SnowField's 128 px trail tiles, or it falls back to ONE tile re-sent whole on every print (a
	#   27 MB upload per footstep: the first build's 1%-low of 11.8 fps)
	snow.trail_px = int(round(side * V1_TRAIL_PX_PER_M / 128.0)) * 128
	# v1's drift system at v1's density (its defaults over its 34 m square)
	var k_area := (side * side) / (V1_SNOW_AREA_M * V1_SNOW_AREA_M)
	snow.windrow_count = int(round(V1_WINDROWS * k_area))
	snow.pile_count = int(round(V1_PILES * k_area))
	# R-C9-371 diagnosis knob: `-- --arenasnow-drop windrows+piles+props+bld` bakes without those drift sources
	var drop := Slots.arg("arenasnow-drop")
	if "windrows" in drop:
		snow.windrow_count = 0
	if "piles" in drop:
		snow.pile_count = 0
	snow.cast_shadows = false
	var mul := buf.slice(0, nx * nz)
	var ghb2: PackedFloat32Array = snow.ground_h_buf
	var zones: Array = []
	for z in SNOW_EXCLUDE:
		var zc: Vector2 = z["c"]
		var zw := uv_to_world(zc.x, -zc.y, 0.0)
		zones.append({"c": Vector2(zw.x, zw.z), "r": float(z["r"])})
	_feather_depth(mul, ghb2, nx, nz, float(g["cell_m"]), Vector2(float(go[0]), float(go[1])), zones)
	snow.depth_grid = {"origin": Vector2(float(go[0]), float(go[1])), "cell_m": float(g["cell_m"]),
					   "nx": nx, "nz": nz, "mul": mul, "trod": buf.slice(nx * nz, 2 * nx * nz)}
	# v1's SURFACE GRAIN: v1's snow tile (cliffside3d godot/textures/barrow/snow.png, read in place). barrow_full has
	#   no res://textures/barrow/snow.png, so SnowField's own fallback drew the snow with NO tile -- the flat "cotton"
	var st := Image.load_from_file(V1_SNOW_TILE)
	if st != null and not st.is_empty():
		st.generate_mipmaps()
		snow.snow_tile = ImageTexture.create_from_image(st)
	else:
		push_warning("[bv2f_arena] v1 snow tile not found at %s" % V1_SNOW_TILE)
	snow.thin_zones = paint.get("_thin_zones", [])
	paint.erase("_thin_zones")
	# v1's OWN snow surface (its lit shader and SNOW_TINT) by default: the painted override wears the flat painting
	#   and the drifts below it read only as edges. `-- --arenasnow painted` keeps the painted surface with the drifts.
	var painted_surface := Slots.arg("arenasnow") == "painted"
	if painted_surface:
		snow.shader_code_override = PaintedWorld.snow_shader_code()
	else:
		snow.snow_tint = _snow_white_tint()
		var shard := _shard_cull_code(SnowField.SHADER)
		if shard != "":
			snow.shader_code_override = shard
	snow.clear_zones = zones
	var obstacles := _arena_snow_obstacles(drop, zones)
	snow.setup(Rect2(float(ar[0]), float(ar[1]), float(ar[2]), float(ar[3])), 0.0, obstacles, WIND)
	add_child(snow)
	if painted_surface:
		var smat := snow.material()
		smat.set_shader_parameter("paint_tex", ground_tex)
		PaintedWorld.bind_projection(smat, lit, shadow_mul, u_hat, v_hat)
		snow.surface().layers = PaintedWorld.LAYER_ON_PAINT
	if snow.shader_code_override.contains("shard_rise_m"):
		var sm := snow.material()
		sm.set_shader_parameter("shard_step_uv", Vector2(snow.grid_quad_m / float(ar[2]), snow.grid_quad_m / float(ar[3])))
		var kr := Slots.arg("arenasnow-shard")
		sm.set_shader_parameter("shard_rise_m", float(kr) if kr != "" else SHARD_RISE_M)
	if heather_mat != null:
		BarrowHeather.bind_snow(heather_mat, snow, WIND)
	if reed_mat != null:
		BarrowHeather.bind_snow(reed_mat, snow, WIND)
	var br := snow.bake_report()
	arena_snow_report = {"area_m": side, "field_px": snow.field_px, "trail_px": snow.trail_px,
		"windrows": snow.windrow_count, "piles": snow.pile_count, "obstacles": obstacles.size(),
		"windrows_placed": br.get("windrows_placed"), "piles_placed": br.get("piles_placed"),
		"surface": "painted" if painted_surface else "v1 lit, white tint %s" % str(snow.snow_tint),
		"mean_depth_m": br.get("mean_depth_m"), "bake_ms": br.get("ms", br.get("bake_ms"))}
	paint["snow"] = arena_snow_report
	print("[bv2f_arena] snow (v1 law): " + JSON.stringify(arena_snow_report))


## R-C9-371 (Matt: "make it snow white"): v1's lit snow kept (its relief, its blue-violet shade from the world ramp), its
## tint re-balanced so the LIT flat snow reads neutral white instead of cream. Measured on stills (top half of a flat
## patch's pixels): v1 tint (235, 228, 220) cream-grey; the walk scene's painted snow (250, 237, 225). Knob for the eye:
## `-- --arenasnow-tint r,g,b`. Route: v1 lit + neutral white tint (the painted surface would carry the painting's warm cream).
const ARENA_SNOW_WHITE := Color(1.17, 1.36, 1.58)     # lit flat snow measured (247, 247, 248); shade (209, 217, 233)


func _snow_white_tint() -> Color:
	var k := Slots.arg("arenasnow-tint")
	if k != "":
		var q := k.split(",")
		if q.size() == 3:
			return Color(float(q[0]), float(q[1]), float(q[2]))
	return ARENA_SNOW_WHITE


## THE SHARDS (conductor, after R-C9-371: "thin pale shards on the cliff and rock edges near the door posts"): the
## snow surface is a grid of grid_quad_m quads lifted by the terrain height at each vertex, so where the ground jumps
## within one quad (a cliff lip, a rock's edge) a quad stands near vertical and wears the snow -- a stretched pale
## sheet. Culled: each vertex measures the ground's largest rise to its four grid neighbours, and a fragment whose
## interpolated rise exceeds SHARD_RISE_M is discarded (`-- --arenasnow-shard m` to tune). Arena-only: the walk
## scene's shader is untouched (the swap is applied to the arena's own copy of v1's SHADER, each anchor asserted).
const SHARD_RISE_M := 0.35


static func _shard_cull_code(code: String) -> String:
	var anchors := ["varying vec3 v_world;\n", "\tv_press = p;\n", "void fragment() {\n"]
	for a in anchors:
		if code.count(a) != 1:
			push_warning("[bv2f_arena] shard cull: anchor %s found %d times -- not applied" % [a.strip_edges(), code.count(a)])
			return ""
	code = code.replace("varying vec3 v_world;\n", "uniform vec2 shard_step_uv = vec2(0.002);\nuniform float shard_rise_m = 0.35;\nvarying float v_rise;\nvarying vec3 v_world;\n")
	code = code.replace("\tv_press = p;\n", "\tfloat g0 = ground_h_on * textureLod(ground_h_tex, UV, 0.0).r;\n" +
		"\tfloat ge = ground_h_on * textureLod(ground_h_tex, UV + vec2(shard_step_uv.x, 0.0), 0.0).r;\n" +
		"\tfloat gw = ground_h_on * textureLod(ground_h_tex, UV - vec2(shard_step_uv.x, 0.0), 0.0).r;\n" +
		"\tfloat gn = ground_h_on * textureLod(ground_h_tex, UV + vec2(0.0, shard_step_uv.y), 0.0).r;\n" +
		"\tfloat gs = ground_h_on * textureLod(ground_h_tex, UV - vec2(0.0, shard_step_uv.y), 0.0).r;\n" +
		"\tv_rise = max(max(abs(ge - g0), abs(gw - g0)), max(abs(gn - g0), abs(gs - g0)));\n\tv_press = p;\n")
	code = code.replace("void fragment() {\n", "void fragment() {\n\tif (v_rise > shard_rise_m) { discard; }\n")
	return code


func _arena_snow_obstacles(drop: String = "", zones: Array = []) -> Array:
	var out: Array = []
	for id_any in nodes.keys():
		var id := String(id_any)
		var base := id.split("__")[0].rstrip("0123456789_")
		var is_prop := SNOW_OBSTACLE_IDS.has(base)
		var is_bld := SNOW_BUILDING_IDS.has(base)
		if not (is_prop or is_bld):
			continue
		if (is_prop and "props" in drop) or (is_bld and "bld" in drop):
			continue
		var root: Node3D = nodes[id]
		var ab := AABB()
		var first := true
		for mi in _meshes(root):
			var m3 := mi as MeshInstance3D
			if m3.mesh == null:
				continue
			var b: AABB = m3.global_transform * m3.mesh.get_aabb()
			ab = b if first else ab.merge(b)
			first = false
		if first or ab.size.y < 0.2:
			continue
		var ctr := Vector2(ab.get_center().x, ab.get_center().z)
		var excluded := false
		for z in zones:
			if ctr.distance_to(z["c"]) < float(z["r"]):
				excluded = true
		if excluded:
			continue
		if is_prop and maxf(ab.size.x, ab.size.z) < 3.0:
			out.append({"pos": Vector3(ab.get_center().x, ab.position.y, ab.get_center().z),
				"radius_m": maxf(ab.size.x, ab.size.z) * 0.5, "height_m": minf(ab.size.y, 3.0)})
			continue
		# a long footprint (a building, a long log run): its base as a chain of 1.5 m discs along its AABB rim
		var x0 := ab.position.x
		var x1 := ab.end.x
		var z0 := ab.position.z
		var z1 := ab.end.z
		var pts: Array = []
		var n_x := maxi(1, int(ceil((x1 - x0) / 1.5)))
		var n_z := maxi(1, int(ceil((z1 - z0) / 1.5)))
		for i in n_x + 1:
			var x := lerpf(x0, x1, float(i) / float(n_x))
			pts.append(Vector2(x, z0))
			pts.append(Vector2(x, z1))
		for i in range(1, n_z):
			var z := lerpf(z0, z1, float(i) / float(n_z))
			pts.append(Vector2(x0, z))
			pts.append(Vector2(x1, z))
		for p in pts:
			out.append({"pos": Vector3(p.x, ab.position.y, p.y), "radius_m": 0.75, "height_m": minf(ab.size.y, 3.0)})
	return out



func _feather_depth(mul: PackedFloat32Array, gh: PackedFloat32Array, nx: int, nz: int, cell: float,
		origin: Vector2 = Vector2.ZERO, zones: Array = []) -> void:
	if gh.size() == nx * nz:
		for j in range(1, nz - 1):
			for i in range(1, nx - 1):
				var k := j * nx + i
				var gx := (gh[k + 1] - gh[k - 1]) / (2.0 * cell)
				var gz := (gh[k + nx] - gh[k - nx]) / (2.0 * cell)
				var g := sqrt(gx * gx + gz * gz)
				var lo := STEEP_LO
				var hi := STEEP_HI
				if not zones.is_empty() and g > ZONE_STEEP_LO:
					var at := origin + Vector2(float(i), float(j)) * cell
					for z in zones:
						if at.distance_to(z["c"]) < float(z["r"]):
							lo = ZONE_STEEP_LO
							hi = ZONE_STEEP_HI
				if g > lo:
					mul[k] *= 1.0 - smoothstep(lo, hi, g)
	var r := maxi(1, int(round(FEATHER_M / cell)))
	for _pass in 2:
		_box_rows(mul, nx, nz, r)
		_box_cols(mul, nx, nz, r)


static func _box_rows(a: PackedFloat32Array, nx: int, nz: int, r: int) -> void:
	var tmp := PackedFloat32Array()
	tmp.resize(nx)
	var w := 1.0 / float(2 * r + 1)
	for j in nz:
		var base := j * nx
		var acc := 0.0
		for i in range(-r, r + 1):
			acc += a[base + clampi(i, 0, nx - 1)]
		for i in nx:
			tmp[i] = acc * w
			acc += a[base + mini(i + r + 1, nx - 1)] - a[base + maxi(i - r, 0)]
		for i in nx:
			a[base + i] = tmp[i]


static func _box_cols(a: PackedFloat32Array, nx: int, nz: int, r: int) -> void:
	var tmp := PackedFloat32Array()
	tmp.resize(nz)
	var w := 1.0 / float(2 * r + 1)
	for i in nx:
		var acc := 0.0
		for j in range(-r, r + 1):
			acc += a[clampi(j, 0, nz - 1) * nx + i]
		for j in nz:
			tmp[j] = acc * w
			acc += a[mini(j + r + 1, nz - 1) * nx + i] - a[maxi(j - r, 0) * nx + i]
		for j in nz:
			a[j * nx + i] = tmp[j]
