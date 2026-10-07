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

const PILOT_U0 := -33.57573954303182
const PILOT_V1 := 22.36993715728635
const PILOT_PX := Vector2(4096.0, 2560.0)
## the pilot's painted data, RELATIVE to PaintedWorld.data_dir() (res://data/painted/) so v1's loaders read it unchanged
const PILOT_REL := "../bv2f/pilot/painted/"
const PILOT_MANIFEST := "res://data/bv2f/pilot/painted/manifest.json"


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
		for mi in _meshes(root):
			_paint_mesh(mi, mat_paint, true)
		n["projected"] += 1
	# anything static not registered as a piece (the ground class meshes, bounds) wears the painting too
	for gi in level.find_children("*", "MeshInstance3D", true, false):
		var mi := gi as MeshInstance3D
		if mi.layers != PaintedWorld.LAYER_PAINTED and not String(mi.name).ends_with("_ink") and mi.visible:
			_paint_mesh(mi, mat_paint, false)
	for ink in _prop_inks:
		(ink as MeshInstance3D).visible = false
		n["inks_hidden"] += 1
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
	_build_painted_heather(vman, lit, shadow_mul)
	if vman.has("snow"):
		_build_painted_snow(vman, painting, lit, shadow_mul)
	var flake := PaintStack.make_flake_texture()
	snowfall = PaintStack.snowfall(flake, Vector3(46, 28, 46), 1700)
	snowfall.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(snowfall)
	n["frame_rebound_materials"] = _rebind_frame(self)
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
	print("[bv2f_pilot] painted: files_ok=%d bad=%s projected=%d baked=%d (meshes %d) bakes_missing=%s rebound=%d" % [
		ok, str(bad), n["projected"], n["baked"], n["baked_meshes"], str(n["bakes_missing"]), n["frame_rebound_materials"]])
