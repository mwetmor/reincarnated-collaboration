extends SceneTree
## BV2F PT (R-C9-272 (a)): groundtiles LOOK-NEUTRALITY, frozen static still-diff. One process, BV2F_PROF_TRY=groundtiles
## (tiles built, originals hidden). Per P11 view, with time held still (Engine.time_scale 0: the snow clock, the reeds'
## wind clock and every _process step stop; heather wind_on 0), him and the falling snow hidden:
##   A  = tiles shown           B = the ORIGINAL meshes shown (tiles hidden)          A2 = tiles again
## --cut rocklod: the same with the rock LOD meshes (A, A2) against their originals (B).
## A vs A2 = the same-build noise of this exact capture (what TIME-driven shaders still move); B vs A = the cut.
##   Godot --path . --resolution 640x360 --script res://tools/bv2f/pt_tiles_ab.gd -- --spec <views.json> --out DIR
const PLAY := Vector2i(1920, 1080)
var vp: SubViewport
var scene

func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	var spec: String = a[a.find("--spec") + 1]
	var out: String = a[a.find("--out") + 1]
	if a.has("--cut"):
		cut = a[a.find("--cut") + 1]   # R-C9-272 (b): "rocklod" = A/A2 the LOD meshes, B the original meshes
	DirAccess.make_dir_recursive_absolute(out)
	vp = SubViewport.new()
	vp.size = PLAY
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/bv2f_pilot_painted.tscn").instantiate()
	vp.add_child(scene)
	_run(JSON.parse_string(FileAccess.get_file_as_string(spec))["views"], out)

var cut := "groundtiles"

func _lods(on: bool) -> int:
	var n := 0
	var stack := [scene.level]
	while not stack.is_empty():
		var nd: Node = stack.pop_back()
		for c in nd.get_children():
			stack.append(c)
		if nd is MeshInstance3D and nd.has_meta("lod_mesh"):
			(nd as MeshInstance3D).mesh = nd.get_meta("lod_mesh") if on else nd.get_meta("lod_orig")
			n += 1
	return n

var _dev5_shared := {}
var _dev5_permat := {}

func _dev5(shared_on: bool) -> int:
	# R-C9-317: A = the shared instance-uniform floe material (as built); B = one per-floe material, phase as a uniform
	var n := 0
	var stack := [scene]
	while not stack.is_empty():
		var nd: Node = stack.pop_back()
		for c in nd.get_children():
			stack.append(c)
		if nd is MeshInstance3D and nd.has_meta("bob_phase"):
			var mi := nd as MeshInstance3D
			if not _dev5_shared.has(mi):
				_dev5_shared[mi] = mi.material_override
				var m: ShaderMaterial = (mi.material_override as ShaderMaterial).duplicate()
				var sh := Shader.new(); sh.code = preload("res://scripts/bv2f/pt_water.gd").floe_shader_code()
				m.shader = sh
				m.set_shader_parameter("bob_phase", float(mi.get_meta("bob_phase")))
				_dev5_permat[mi] = m
			mi.material_override = _dev5_shared[mi] if shared_on else _dev5_permat[mi]
			n += 1
	return n

func _tiles(show: bool) -> int:
	if cut == "dev5":
		return _dev5(show)
	if cut == "rocklod":
		return _lods(show)
	var n := 0
	for root in scene.level.get_children():
		if not String(root.name).begins_with("ground_"):
			continue
		var has := false
		for c in root.get_children():
			if String(c.name).begins_with("tile_"):
				(c as Node3D).visible = show
				has = true
				n += 1
		if has:
			(root.get_node("mesh") as Node3D).visible = not show
	return n

func _settle(n: int) -> void:
	for i in n:
		await process_frame

func _shot(path: String) -> void:
	await _settle(3)
	await RenderingServer.frame_post_draw
	vp.get_texture().get_image().save_png(path)

func _run(views: Array, out: String) -> void:
	var w := 0
	while not scene.ready_done and w < 3000:
		await process_frame
		w += 1
	scene.set_hud_visible(false)
	scene.set_overlay(false)
	scene.set_crucible_visible(false)
	for c in scene.get_children():
		if c is CanvasLayer:
			(c as CanvasLayer).visible = false
	if scene.snowfall != null:
		scene.snowfall.visible = false
	if scene.knight != null:
		scene.knight.visible = false
	if scene.heather_mat != null:
		scene.heather_mat.set_shader_parameter("wind_on", 0.0)
	var rep := {"tiles": _tiles(true), "views": []}
	Engine.time_scale = 0.0
	for s in views:
		var cc: Array = s["camera_centre_ground_uv"]
		scene.park_camera(scene.uv_to_world(float(cc[0]), float(cc[1]), 0.0), 1.0)
		await _settle(6)
		var nm := String(s["name"])
		_tiles(true)
		await _shot(out.path_join(nm + "_A.png"))
		_tiles(false)
		await _shot(out.path_join(nm + "_B.png"))
		_tiles(true)
		await _shot(out.path_join(nm + "_A2.png"))
		rep["views"].append(nm)
	Engine.time_scale = 1.0
	var f := FileAccess.open(out.path_join("tiles_ab.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(rep))
	f.close()
	print("[tiles_ab] ", JSON.stringify(rep))
	quit(0)
