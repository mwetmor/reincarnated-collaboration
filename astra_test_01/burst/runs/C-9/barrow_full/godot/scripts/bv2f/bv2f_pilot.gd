extends "res://scripts/bv2f/bv2f_level.gd"
## BV2F lane PT, Phase 2' (R-C9-191): THE PILOT -- the bv2art level (LV's bv2f_level.gd, inherited unchanged) with
##   (1) the PILOT WINDOW as its guide window (cols 0-2 x rows 0-2 of the 5 x 5 grid: plate px [0, 0, 4096, 2560]),
##       so v1's frozen capture tools (capture_ids, ...) frame exactly the pilot painting;
##   (2) ONE ID PER INSTANCE (always; env BV2F_UNGROUP kept for the record) (LV groups instanced slots into one ID each, for the full site's
##       256-colour limit; the pilot's take needs every real model's own silhouette -- DEV-16 is decided on this count);
##   (3) painted = true: dressed in the PILOT PAINTING by v1's own rule (barrow_full.gd _dress_painted): ground and
##       primitives wear the painting by projection, real models wear their game-camera bakes (t5_06b_bake), all
##       unlit on LAYER_PAINTED under the paint sun; him and the 3D heather / snow lit by the sun; v1's wind and snowfall.
## v1's projection is uniform-driven (PaintedWorld.PROJ_UNIFORMS): v1's frame constants are re-bound to the pilot's.

var water_mat_pt: ShaderMaterial = null   # BV2F-PT DEV-5
var reed_mat: ShaderMaterial = null   # BV2F-PT DEV-21
## DEV-21 (R-C9-205): the reeds' wind -- taller and laxer than the heather's sprays, so more sway and a stronger gust
## (BarrowHeather's heather: sway 0.020 m, gust 0.050 m at ~0.35 m). Stated here, for the conductor's review.
const REED_WIND := {"sway_amp": 0.030, "sway_hz": 0.35, "gust_amp": 0.090, "tone_jitter": 0.0, "hue_jitter": 0.0}
const SETTLE_FRAMES := 30   # BV2F-PT R-C9-201
const PILOT_U0 := -33.57573954303182
const PILOT_V1 := 22.36993715728635
const PILOT_PX := Vector2(4096.0, 2560.0)
## the pilot's painted data, RELATIVE to PaintedWorld.data_dir() (res://data/painted/) so v1's loaders read it unchanged
const PILOT_REL := "../bv2f/pilot/painted/"
const PILOT_MANIFEST := "res://data/bv2f/pilot/painted/manifest.json"
const SNOW_TERRAIN := preload("res://scripts/bv2f/snow_field_terrain.gd")   # BV2F-PT DEV-18
const PT_WATER := preload("res://scripts/bv2f/pt_water.gd")   # BV2F-PT DEV-5


## R-C9-205: the pilot reads ITS OWN level, pinned -- data/bv2f/pilot/level/ = LV's art level as the pilot was painted
## over (level.json sha c861f9092f23, terrain_h 2d9fbf243d77); LV's data/bv2f/art/ is being rebuilt in place
const PILOT_LEVEL_DIR := "res://data/bv2f/pilot/level/"


func _init() -> void:
	BV2F_DATA = PILOT_LEVEL_DIR


func _pilot_window() -> Dictionary:
	var p := deg_to_rad(PaintedWorld.PITCH_DEG)
	var w := PILOT_PX.x / PPM
	var h := PILOT_PX.y / (PPM * sin(p))
	return {"centre_uv": [PILOT_U0 + w / 2.0, PILOT_V1 - h / 2.0], "u": [PILOT_U0, PILOT_U0 + w],
			"v": [PILOT_V1 - h, PILOT_V1], "px": [int(PILOT_PX.x), int(PILOT_PX.y)],
			"_": "BV2F PT pilot window (cols 0-2 x rows 0-2 of bv2art)"}


func _read_json(path: String) -> Dictionary:
	var d := super._read_json(path)
	if path == LAYOUT_JSON and d.has("frame"):
		d["frame"]["guide_window"] = _pilot_window()
	return d


func _build_crucible() -> void:
	super._build_crucible()
	# the pilot is ALWAYS one id per instance: its take, its bakes and its painted dress are per instance
	# (124 ids site-wide <= v1's 256-colour ID code: DEV-16 not opened)
	_ungroup()


func _ungroup() -> void:
	var gids: Array = _groups.keys()
	var keep := []
	for e in layout["placements"]:
		if not gids.has(String(e["id"])):
			keep.append(e)
	layout["placements"] = keep
	var n := 0
	for gid in gids:
		var g: Node3D = _groups[gid]
		var cls := String(built[gid]["class"]) if built.has(gid) else "?"
		nodes.erase(gid)
		built.erase(gid)
		for ch in g.get_children():
			_register(String(gid) + "__" + String(ch.name), ch as Node3D, cls, "instance:" + String(gid))
			n += 1
	report["ungrouped"] = {"groups": gids.size(), "instances": n, "ids_total": nodes.size()}


# --- the painted pilot (v1's _dress_painted, on the pilot's data and frame) ---------------------------------------

func _rebind_frame(root: Node) -> int:
	## every material built on v1's PROJ_UNIFORMS gets the pilot frame (v1's are compiled-in defaults)
	var n := 0
	var mats := []
	for gi in root.find_children("*", "GeometryInstance3D", true, false):
		var m = (gi as GeometryInstance3D).material_override
		if m is ShaderMaterial and not mats.has(m):
			mats.append(m)
	if heather_mat != null and not mats.has(heather_mat):
		mats.append(heather_mat)
	for m in mats:
		var sm := m as ShaderMaterial
		if sm.shader == null:
			continue
		var has := false
		for u in sm.shader.get_shader_uniform_list():
			if String(u["name"]) == "g_frame":
				has = true
				break
		if has:
			sm.set_shader_parameter("g_frame", Vector3(PILOT_U0, PILOT_V1, PPM))
			sm.set_shader_parameter("g_size", PILOT_PX)
			n += 1
	return n


func _is_real_model(node: Node) -> bool:
	## a GLB model (LV's _place_box / _place_beam with a loaded model) carries bv2f_fit; primitives do not
	return node.has_meta("bv2f_fit")


func _dress_painted() -> void:
	var t0 := Time.get_ticks_msec()
	var j = JSON.parse_string(FileAccess.get_file_as_string(PILOT_MANIFEST))
	var man: Dictionary = j if typeof(j) == TYPE_DICTIONARY else {}
	var loads := {}
	paint = {"manifest": PILOT_MANIFEST, "loads": loads, "ground_variant": "as_painted"}
	if man.is_empty():
		push_error("bv2f_pilot: no manifest at %s" % PILOT_MANIFEST)
		paint["error"] = "no manifest"
		return
	var sm: Array = man["shadow_mul"]["linear"]
	var shadow_mul := Vector3(float(sm[0]), float(sm[1]), float(sm[2]))
	var painting := PaintedWorld.load_png_bin(PILOT_REL + String(man["painting"]["file"]), String(man["painting"]["sha256"]), true, loads)
	var lit := PaintedWorld.load_png_bin(PILOT_REL + String(man["lit"]["file"]), String(man["lit"]["sha256"]), false, loads)
	_paint_tex = {"painting": painting, "ground": painting, "lit": lit}
	var mat_paint := PaintedWorld.painted_material(painting, true, lit, shadow_mul, u_hat, v_hat)
	var n := {"projected": 0, "baked": 0, "baked_meshes": 0, "bakes_missing": [], "inks_hidden": 0}
	var bakes: Dictionary = man["bakes"]
	for id in nodes:
		var root: Node3D = nodes[id]
		if bakes.has(id):
			var b: Dictionary = bakes[id]
			var tex := PaintedWorld.load_png_bin(PILOT_REL + String(b["file"]), String(b["sha256"]), true, loads)
			var mat := PaintedWorld.painted_material(tex, false, lit, shadow_mul, u_hat, v_hat)
			for mi in _meshes(root):
				_paint_mesh(mi, mat, true)
				n["baked_meshes"] += 1
			n["baked"] += 1
			continue
		if _is_real_model(root) and bool(man.get("bake_all_real_models", true)) and (man.get("real_models_in_window", []) as Array).has(id):
			n["bakes_missing"].append(id)
		# v1's rule (barrow_full.gd _dress_painted): the GROUND does not cast (it is lit by the paint sun only, which takes
		# no static caster); the mound and every piece do. bv2art registers its terrain class meshes as pieces, so the
		# first pilot build cast the whole terrain into the sun's shadow map (1.4 M primitives a frame) -- R-C9-199
		var casts := not (built.has(id) and String(built[id].get("piece", "")) == "ground" and String(id) != "ground_mound")
		for mi in _meshes(root):
			_paint_mesh(mi, mat_paint, casts)
		n["projected"] += 1
	# anything static not registered as a piece (the ground class meshes, bounds) wears the painting too
	for gi in level.find_children("*", "MeshInstance3D", true, false):
		var mi := gi as MeshInstance3D
		if mi.layers != PaintedWorld.LAYER_PAINTED and not String(mi.name).ends_with("_ink") and mi.visible:
			_paint_mesh(mi, mat_paint, false)
	for ink in _prop_inks:
		(ink as MeshInstance3D).visible = false
		n["inks_hidden"] += 1
	_dress_water(man, painting, lit, shadow_mul, loads, n)   # BV2F-PT DEV-5
	# THE TWO SUNS -- v1's code, verbatim in effect (barrow_full.gd _dress_painted)
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
	paint_sun.directional_shadow_mode = DirectionalLight3D.SHADOW_ORTHOGONAL
	paint_sun.directional_shadow_max_distance = CAM_STANDOFF + 8.0
	paint_sun.shadow_blur = 0.6
	PaintStack.post_set(post_mat, "painted_exclude", 1.0)
	# v1's heather + snow + snowfall builders, on the pilot manifest (its file entries are PILOT_REL-relative)
	var vman := man.duplicate(true)
	vman["heather"]["file"] = PILOT_REL + String(man["heather"]["file"])
	if vman.has("snow"):
		vman["snow"]["grid"]["file"] = PILOT_REL + String(man["snow"]["grid"]["file"])
		if (man["snow"] as Dictionary).has("ground_h"):   # BV2F-PT DEV-18
			vman["snow"]["ground_h"]["file"] = PILOT_REL + String(man["snow"]["ground_h"]["file"])
	_build_painted_heather(vman, lit, shadow_mul)
	if man.has("reeds"):   # BV2F-PT DEV-21
		_build_painted_reeds(man, lit, shadow_mul, loads)
	if vman.has("snow"):
		_build_painted_snow(vman, painting, lit, shadow_mul)
	var flake := PaintStack.make_flake_texture()
	snowfall = PaintStack.snowfall(flake, Vector3(46, 28, 46), 1700)
	snowfall.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(snowfall)
	n["frame_rebound_materials"] = _rebind_frame(self)
	n["warmup"] = _warm_pipelines()   # BV2F-PT R-C9-200
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
	paint["ms"] = Time.get_ticks_msec() - t0
	report["painted"] = paint
	print("[bv2f_pilot] painted: files_ok=%d bad=%s projected=%d baked=%d (meshes %d) bakes_missing=%s rebound=%d water=%s snow_ground_h=%s" % [
		ok, str(bad), n["projected"], n["baked"], n["baked_meshes"], str(n["bakes_missing"]), n["frame_rebound_materials"],
		str(n.get("water")), str(snow != null and snow.get("ground_h_tex") != null)])
	print("[bv2f_pilot] warmup: " + JSON.stringify(n.get("warmup", {})))


# --- DEV-18 (R-C9-193, applied): v1's _build_painted_heather (barrow_full.gd:2292-2346) COPIED, ONE line changed (marked) ------
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
			mm.set_instance_transform(k, Transform3D(Basis().scaled(Vector3.ONE * hh), Vector3(float(r[0]), (float(r[7]) if r.size() > 7 else 0.0) - 0.01, float(r[1]))))   # BV2F-PT DEV-18: the spray on its ground height
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


func _build_painted_snow(man: Dictionary, ground_tex: Texture2D, lit: Texture2D, shadow_mul: Vector3) -> void:  # BV2F-PT DEV-18: v1's barrow_full.gd _build_painted_snow COPIED, marked lines changed
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
	snow = SNOW_TERRAIN.new()   # BV2F-PT DEV-18: v1's SnowField, on the terrain (scripts/bv2f/snow_field_terrain.gd)
	var ghd: Dictionary = sn.get("ground_h", {})   # BV2F-PT DEV-18
	if not ghd.is_empty():   # BV2F-PT DEV-18
		var ghb := PaintedWorld.load_f32_bin(String(ghd["file"]), String(ghd["sha256"]), paint["loads"])   # BV2F-PT DEV-18
		snow.set_ground_height(ghb, Vector2(float(go[0]), float(go[1])), float(g["cell_m"]), nx, nz)   # BV2F-PT DEV-18
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
	if reed_mat != null:   # BV2F-PT DEV-21: his push-aside, the heather's
		BarrowHeather.bind_snow(reed_mat, snow, WIND)
	var br := snow.bake_report()
	paint["snow"] = {"area_xz": ar, "field_px": snow.field_px, "trail_px": snow.trail_px,
					 "bare_frac_under_cut": br.get("bare_frac_under_cut"), "mean_depth_m": br.get("mean_depth_m"),
					 "thin_zones": br.get("thin_zones"), "bake_ms": br.get("ms", br.get("bake_ms"))}


# --- DEV-5 (R-C9-194): the animated water over the painted sea, the floes riding the swell -------------------------
func _dress_water(man: Dictionary, painting: Texture2D, lit: Texture2D, shadow_mul: Vector3, loads: Dictionary, n: Dictionary) -> void:
	if not man.has("water") or not nodes.has("ground_sea"):
		n["water"] = "none"
		return
	var w: Dictionary = man["water"]
	var sdf := PaintedWorld.load_png_bin(PILOT_REL + String(w["sdf"]["file"]), String(w["sdf"]["sha256"]), false, loads)
	var wm := ShaderMaterial.new()
	var sh := Shader.new()
	sh.code = PT_WATER.WATER_SHADER
	wm.shader = sh
	wm.set_shader_parameter("paint_tex", painting)
	wm.set_shader_parameter("noise_tex", fbm)
	wm.set_shader_parameter("water_sdf", sdf)
	var r: Array = w["sdf"]["rect_xz"]
	wm.set_shader_parameter("sdf_rect", Vector4(float(r[0]), float(r[1]), float(r[2]), float(r[3])))
	wm.set_shader_parameter("g_u_hat", u_hat)
	wm.set_shader_parameter("g_v_hat", v_hat)
	var p := deg_to_rad(PaintedWorld.PITCH_DEG)
	wm.set_shader_parameter("g_frame", Vector3(PILOT_U0, PILOT_V1, PPM))
	wm.set_shader_parameter("g_px_per", Vector2(PPM * sin(p), PPM * cos(p)))
	wm.set_shader_parameter("g_size", PILOT_PX)
	wm.set_shader_parameter("paint_mix", 0.75)         # R-C9-197: R-C9-159's own value (the water Matt accepted as moving)
	var ns := 0
	for mi in _meshes(nodes["ground_sea"]):
		mi.material_override = wm
		mi.layers = PaintedWorld.LAYER_PAINTED
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		ns += 1
	var fsh := PaintedWorld._shader("bv2f_floes", PT_WATER.floe_shader_code())
	var nf := 0
	for id in nodes:
		if not String(id).begins_with("blobs_shore_ice__"):
			continue
		var fm := ShaderMaterial.new()
		fm.shader = fsh
		fm.set_shader_parameter("paint_tex", painting)
		fm.set_shader_parameter("project_uv", true)
		fm.set_shader_parameter("painted_mark", PaintedWorld.PAINTED_MARK)
		PaintedWorld.bind_projection(fm, lit, shadow_mul, u_hat, v_hat)
		fm.set_shader_parameter("bob_phase", fposmod(float(nf) * 0.6180339, 1.0))
		for mi in _meshes(nodes[id]):
			_paint_mesh(mi, fm, false)
		nf += 1
	water_mat_pt = wm
	n["water"] = {"sea_meshes": ns, "floes_bobbing": nf}


# --- R-C9-200: the load-time pipeline warm-up -------------------------------------------------------------------
# --- DEV-21 (R-C9-205 (1)): THE REEDS -- the painting's own reed tufts as cards, on their ground, in the gusts ---------
static func _swap21(code: String, a: String, b: String, what: String) -> String:
	assert(code.count(a) == 1, "reed_shader_code: '%s' found %d times, not once" % [what, code.count(a)])
	return code.replace(a, b)


static func reed_shader_code() -> String:
	"""BarrowHeather's vertex (wind, gusts, his push-aside) UNCHANGED but for three asserted swaps, and the PAINTED
	surface's fragment + light (PaintedWorld.PAINTED_SHADER): a card IS the painting's own reed pixels (fid/pt/tools/
	reeds.py), so at rest it draws the painting exactly; only the wind and his wading move it. Times his shadow.
	  1. render_mode: no ambient, no fog (the painting is the light), both faces;
	  2. one unit quad for every card: the instance's basis carries the card's size (CAM_RIGHT x w, CAM_UP x h), so the
	     wind's world offset goes back through the inverse basis (BarrowHeather scales uniformly: d / s);
	  3. the card's atlas rectangle from INSTANCE_CUSTOM."""
	var v: String = BarrowHeather._SHADER_FUNCS
	v = _swap21(v, "	VERTEX += d / s;", "	VERTEX += inverse(mat3(MODEL_MATRIX)) * d;", "vertex offset")
	v = _swap21(v, "v_col = COLOR.rgb;", "v_col = COLOR.rgb;\n\tUV = mix(INSTANCE_CUSTOM.xy, INSTANCE_CUSTOM.zw, UV);", "uv")
	var head := _swap21(BarrowHeather._SHADER_HEAD, "render_mode specular_disabled, cull_back;",
		"render_mode specular_disabled, cull_disabled, ambient_light_disabled, fog_disabled;", "render_mode")
	return head + PaintStack.RAMP_UNIFORMS + BarrowHeather._SHADER_UNIFORMS + PaintedWorld.PROJ_UNIFORMS \
		+ "uniform float painted_mark = 0.0;\nuniform bool reed_probe = false;\n" + PaintStack.RAMP_BODY \
		+ PaintedWorld.PROJ_FUNCS + v + """
void fragment() {
	vec4 tx = texture(card_tex, UV);
	ALBEDO = reed_probe ? vec3(0.0) : tx.rgb;
	EMISSION = reed_probe ? vec3(8.0, 0.0, 8.0) : vec3(0.0);
	ALPHA = tx.a;
	ALPHA_SCISSOR_THRESHOLD = 0.5;
	ROUGHNESS = painted_mark;
}

void light() {
	DIFFUSE_LIGHT += his_shadow(ATTENUATION, v_world);
}
"""


func _build_painted_reeds(man: Dictionary, lit: Texture2D, shadow_mul: Vector3, loads: Dictionary) -> void:
	var r: Dictionary = man["reeds"]
	var atlas := PaintedWorld.load_png_bin(PILOT_REL + String(r["atlas"]["file"]), String(r["atlas"]["sha256"]), true, loads)
	var jp := PaintedWorld.data_dir() + PILOT_REL + String(r["file"])
	var ok_sha := FileAccess.get_sha256(jp) == String(r["sha256"])
	loads[PILOT_REL + String(r["file"])] = {"path": jp, "sha256_ok": ok_sha}
	var j = JSON.parse_string(FileAccess.get_file_as_string(jp))
	var rows: Array = j["rows"] if typeof(j) == TYPE_DICTIONARY else []
	if atlas == null or rows.is_empty() or not ok_sha:
		push_error("bv2f_pilot: DEV-21 reeds not built (atlas %s, rows %d, json sha %s)" % [str(atlas != null), rows.size(), str(ok_sha)])
		paint["reeds"] = {"error": true}
		return
	var sh := Shader.new()
	sh.code = reed_shader_code()
	reed_mat = ShaderMaterial.new()
	reed_mat.shader = sh
	reed_mat.set_shader_parameter("card_tex", atlas)
	reed_mat.set_shader_parameter("gust_noise", fbm)
	reed_mat.set_shader_parameter("wash_noise", fbm)
	reed_mat.set_shader_parameter("mottle_noise", fbm)
	reed_mat.set_shader_parameter("painted_mark", PaintedWorld.PAINTED_MARK)
	for k in REED_WIND:
		reed_mat.set_shader_parameter(k, REED_WIND[k])
	reed_mat.set_shader_parameter("wind_dir", WIND.normalized())
	# the instrument: BV2F_REED_PROBE=1 draws every card flat magenta (reed_probe), to see where they are and that they draw
	reed_mat.set_shader_parameter("reed_probe", OS.get_environment("BV2F_REED_PROBE") == "1")
	PaintedWorld.bind_projection(reed_mat, lit, shadow_mul, u_hat, v_hat)
	# ONE unit quad, local x across (0..1), y up (0..1); UV2.x the height fraction (the sway's weight)
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = PackedVector3Array([Vector3(0, 0, 0), Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(1, 1, 0)])
	arr[Mesh.ARRAY_NORMAL] = PackedVector3Array([Vector3(0, 0, 1), Vector3(0, 0, 1), Vector3(0, 0, 1), Vector3(0, 0, 1)])
	arr[Mesh.ARRAY_COLOR] = PackedColorArray([Color.WHITE, Color.WHITE, Color.WHITE, Color.WHITE])
	arr[Mesh.ARRAY_TEX_UV] = PackedVector2Array([Vector2(0, 1), Vector2(1, 1), Vector2(0, 0), Vector2(1, 0)])
	arr[Mesh.ARRAY_TEX_UV2] = PackedVector2Array([Vector2(0, 0), Vector2(0, 0), Vector2(1, 0), Vector2(1, 0)])
	arr[Mesh.ARRAY_INDEX] = PackedInt32Array([0, 1, 2, 1, 3, 2])
	var quad := ArrayMesh.new()
	quad.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.use_custom_data = true
	mm.use_colors = true
	mm.mesh = quad
	mm.instance_count = rows.size()
	var cr := BarrowHeather.CAM_RIGHT
	var cu := BarrowHeather.CAM_UP
	var cf := BarrowHeather.CAM_FWD
	var thin := []
	for i in rows.size():
		var q: Array = rows[i]
		# [x, z, ground_h, w_m, h_m, base_u, below_m, u0, v0, u1, v1]: the foot on its ground; the card in the camera plane
		var w := float(q[3])
		var h := float(q[4])
		var foot := Vector3(float(q[0]), float(q[2]), float(q[1]))
		var o := foot - cr * (w * float(q[5])) - cu * float(q[6])
		mm.set_instance_transform(i, Transform3D(Basis(cr * w, cu * h, cf), o))
		mm.set_instance_custom_data(i, Color(float(q[7]), float(q[8]), float(q[9]), float(q[10])))
		mm.set_instance_color(i, Color(1, 1, 1, 1))
		# v1's heather rule for the snow round a clump (HEATHER_SNOW_FRAC: capped at 20% of its height), on the
		# card's world height -- uncapped, the field's 3D snow buried all but the cards' tips (first probe render)
		thin.append({"c": Vector2(foot.x, foot.z), "r": maxf(0.5 * w, 0.15), "feather": 0.18,
					 "max_d": h * cu.y * HEATHER_SNOW_FRAC})
	var zones: Array = paint.get("_thin_zones", [])
	zones.append_array(thin)
	paint["_thin_zones"] = zones
	var mmi := MultiMeshInstance3D.new()
	mmi.name = "Reeds"
	mmi.multimesh = mm
	mmi.material_override = reed_mat
	mmi.layers = PaintedWorld.LAYER_ON_PAINT
	mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(mmi)
	paint["reeds"] = {"cards": rows.size(), "wind": REED_WIND}
	print("[bv2f_pilot] reeds: %d cards (DEV-21), aabb %s" % [rows.size(), str(mm.get_aabb())])


func _physics_process(dt: float) -> void:
	super._physics_process(dt)
	# DEV-21: the reeds' wind on the snow's clock, as v1 runs the heather's
	if snow != null and reed_mat != null:
		reed_mat.set_shader_parameter("wind_time", snow.clock())


func _warm_pipelines() -> Dictionary:
	"""Every pilot pipeline drawn ONCE during load, before control: the play camera swept over the pilot window (each
	material, the water + foam, the floes, the heather, the snow, the pen, both suns' shadow passes, him) with
	RenderingServer.force_draw(false) -- frames rendered and never presented -- so no first-sight compile lands in
	play (R-C9-199 run 1: cold pipelines, a real stutter). Also one snow puff of each kind (its particle pipeline)
	under the camera. Desktop only (the web page has warm_veil.gd). The camera returns to following him after."""
	if PaintStack.is_web() or cam == null:
		return {"skipped": true}
	var t0 := Time.get_ticks_msec()
	var p := deg_to_rad(PaintedWorld.PITCH_DEG)
	var w := PILOT_PX.x / PPM
	var h := PILOT_PX.y / (PPM * sin(p))
	var views := []
	var nu := int(ceil(w / 14.0))
	var nv := int(ceil(h / 7.5))
	for j in nv + 1:
		for i in nu + 1:
			views.append(Vector2(PILOT_U0 + w * float(i) / float(nu), PILOT_V1 - h * float(j) / float(nv)))
	if knight != null:
		views.append(knight_uv())
	var n_draws := 0
	for v in views:
		park_camera(uv_to_world(v.x, v.y), 1.0)
		if snow != null and snow.has_method("_puff") and v == views[0]:   # one of each, at the window's far corner (off his screen)
			var at := uv_to_world(v.x, v.y, floor_y_at(v.x, v.y))
			snow._puff(at, Vector2(0, 1), 0.05, false)
			snow._puff(at, Vector2(0, 1), 0.4, true)
		for k in 2:
			RenderingServer.force_draw(false, 0.0)
			n_draws += 1
	unpark_camera()
	return {"views": views.size(), "draws": n_draws, "ms": Time.get_ticks_msec() - t0}


# --- R-C9-201: the load tail and the first footprint, absorbed BEFORE control ----------------------------------------
func _ready() -> void:
	"""v1's _ready runs unchanged (it ends by setting ready_done). The pilot then takes control back for a short SETTLE
	of real frames before handing over: the first presented frames after a 10 s load carry the load's tail (55-95 ms in
	the R-C9-201 trace), his first footsteps (stamp + trail upload) took 18-24 ms, and PH saw 28-31 ms when he first
	stopped. All of it runs here first, hidden, off his screen. No look change."""
	# F-2 (R-C9-205): THE LOAD VEIL -- the presented frames of the load (his rig, the settle) sit under a plain cover
	# that leaves before control; captures wait for ready_done, which is set only after the veil is gone
	var veil: CanvasLayer = null
	if painted and not PaintStack.is_web():
		veil = CanvasLayer.new()
		veil.name = "PilotLoadVeil"
		veil.layer = 127
		var rect := ColorRect.new()
		rect.color = Color(0.93, 0.92, 0.89)
		rect.set_anchors_preset(Control.PRESET_FULL_RECT)
		veil.add_child(rect)
		add_child(veil)
	await super._ready()
	if not painted or PaintStack.is_web():
		if veil != null:
			veil.queue_free()
		return
	ready_done = false
	var t0 := Time.get_ticks_msec()
	var n := 0
	# R-C9-201 (PH's cluster at ~3.3 s, first fresh run: the moment he first STOPS): every first-time path of his
	# movement runs here, HIDDEN, east of the pilot window (uv 11.5..15.5, 15.5: snow, flat, in the snow field; outside
	# the window, every P11 still, the start loop and the film), while the presented frames show the start view --
	# walk, run, stop, walk, stop -- his locomotion blends, foot locks, real footprints and puffs (they refill in 60 s).
	# Then he is back at spawn, as v1 placed him.
	var k = knight
	if k != null:
		var sp: Array = layout["knight"]["spawn_uv"]
		var spawn := Vector2(float(sp[0]), float(sp[1]))
		park_camera(uv_to_world(spawn.x, spawn.y), 1.0)
		var was_phys: bool = k.is_physics_processing()
		k.set_physics_process(false)
		k.visible = false
		place_knight(11.5, 15.5, "E")   # snow, flat, in the snow field, OUTSIDE the pilot window, every still, the start loop and the film
		var dt := 1.0 / 60.0
		var plan := [[Vector2(1, 0), false, 20], [Vector2(1, 0), true, 20], [Vector2.ZERO, false, 15],
					 [Vector2(1, 0), false, 30], [Vector2.ZERO, false, 15]]
		for step in plan:
			for f in int(step[2]):
				k.drive_dir((step[0] as Vector2).normalized() if step[0] != Vector2.ZERO else Vector2.ZERO, bool(step[1]), dt)
				await get_tree().physics_frame
				await get_tree().process_frame
				n += 1
		place_knight(spawn.x, spawn.y, String(layout["knight"].get("spawn_facing", "S")))
		for f in 90:   # every locomotion blend back to v1's idle
			k.drive_dir(Vector2.ZERO, false, dt)
			await get_tree().physics_frame
			await get_tree().process_frame
			n += 1
		# his DRIVE STATE back to knight.gd's initial values (_move_dir persists after a stop and re-derives `facing`
		# on every drive -- the settle's east walk would otherwise turn him east at spawn)
		# F-2: assert the six knight.gd fields exist before resetting them (a knight.gd that renames one must fail loud)
		var init_vals := {"_move_dir": Vector2(0, 1), "_speed": 0.0, "_strafing": false, "_strafe_w": 0.0,
						  "_strafe_side": "l", "_yaw_init": false}
		var missing := []
		for fld in init_vals:
			if not (fld in k):
				missing.append(fld)
		if missing.is_empty():
			for fld in init_vals:
				k.set(fld, init_vals[fld])
		else:
			push_error("bv2f_pilot: knight.gd lacks %s -- drive state NOT reset" % str(missing))
		report["settle_knight_fields_missing"] = missing
		place_knight(spawn.x, spawn.y, String(layout["knight"].get("spawn_facing", "S")))
		for f in 10:
			k.drive_dir(Vector2.ZERO, false, dt)
			await get_tree().physics_frame
			await get_tree().process_frame
			n += 1
		k.visible = true
		k.set_physics_process(was_phys)
		unpark_camera()
	for i in SETTLE_FRAMES:
		await get_tree().process_frame
		n += 1
	# F-2: the settle's prints and ploughs (east of the pilot window, ground the full-site painting will cover) are
	# CLEARED -- the field starts as v1's does, untrodden
	if snow != null:
		snow.clear_trail()
	if veil != null:
		veil.queue_free()
		await get_tree().process_frame
	report["settle"] = {"frames": n, "ms": Time.get_ticks_msec() - t0}
	print("[bv2f_pilot] settle: " + JSON.stringify(report["settle"]))
	ready_done = true
