extends SceneTree
## barrow_v2 paint lane (BVP, drax): the WHOLE SITE at the arena camera on the plate grid, in tiles.
##
##   Godot --path godot --resolution 640x360 --script tools/bvp_capture.gd -- \
##         --mode guide|ids --frame ../paint/frame_bvp.json --out DIR [--ground PNG] [--ids-json PATH]
##
## The plate grid is paint/frame_bvp.json (tools/bvp_frame.py): plate_X = P*x + X0,
## plate_Y = P*sin(a)*y - P*cos(a)*z + Y0, orthographic, pitch a, ZERO yaw. Each 2048 tile is one
## SubViewport render (not clamped by the screen), its camera centred on the tile's centre pixel:
## keep_height, size = rows / P, rotation (-a, 0, 0), target on the z = 0 plane at
## (x, y) = ((cx - X0) / P, (cy - Y0) / (P sin a)).
##
##   guide  the greybox as built, no labels, no walker, no anchor dots; --ground swaps the ground
##          texture for the guide's own (no rings, no floor outline: the walkable edge is not a line)
##   ids    every cutout piece in its own flat colour, everything else black, unlit, no AA.
##          --ids-json lists [{"idx": i, "match": [feature ids...]}]; a mesh belongs to the first
##          group whose feature footprint contains its AABB centre (or whose name it carries).
##          Colour: R = (i % 16) * 16 + 8, G = (i / 16) * 16 + 8, B = 200 (the barrow_full code).
## Writes DIR/<mode>_tXX_YY.png per tile + DIR/<mode>_tiles.json.

const TILE := 2048

var mode := "guide"
var frame_path := ""
var out_dir := ""
var ground_png := ""
var ids_json := ""
var vp: SubViewport
var cam: Camera3D
var scene
var fr: Dictionary
var layout: Dictionary


func _arg(args: PackedStringArray, k: String, d: String) -> String:
	for i in args.size():
		if args[i] == k and i + 1 < args.size():
			return args[i + 1]
	return d


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	mode = _arg(args, "--mode", "guide")
	frame_path = _arg(args, "--frame", "")
	out_dir = _arg(args, "--out", "")
	ground_png = _arg(args, "--ground", "")
	ids_json = _arg(args, "--ids-json", "")
	if frame_path == "" or out_dir == "":
		print("[bvp] HALT: --frame and --out are required")
		quit(2)
		return
	fr = JSON.parse_string(FileAccess.get_file_as_string(frame_path))
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = Vector2i(TILE, TILE)
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_DISABLED if mode == "ids" else Viewport.MSAA_4X
	vp.screen_space_aa = Viewport.SCREEN_SPACE_AA_DISABLED
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/barrow_v2_greybox.tscn").instantiate()
	vp.add_child(scene)
	_run.call_deferred()


func _hide_aids() -> void:
	for n in scene.find_children("*", "Label3D", true, false):
		(n as Node3D).visible = false
	if scene.get("walker") != null:
		scene.walker.visible = false
	for n in scene.find_children("*", "MeshInstance3D", true, false):
		var mi := n as MeshInstance3D
		if mi.mesh is CylinderMesh and (mi.mesh as CylinderMesh).height <= 0.05:
			mi.visible = false                  # the anchor dots and the start mark


var _cands: Array = []          # [area, id, PackedVector2Array] of the features the groups name, smallest first


func _feature_hit(p: Vector2) -> String:
	for c in _cands:
		if Geometry2D.is_point_in_polygon(p, c[2]):
			return String(c[1])
	return ""


func _prep_cands(groups: Array) -> void:
	var want := {}
	for g in groups:
		for m in g["match"]:
			want[String(m)] = true
	for f in layout["features"]:
		if not want.has(String(f["id"])):
			continue
		var poly := PackedVector2Array()
		for q in f["footprint"]:
			poly.append(Vector2(float(q[0]), float(q[1])))
		var ar := 0.0
		for i in poly.size():
			ar += poly[i].x * poly[(i + 1) % poly.size()].y - poly[(i + 1) % poly.size()].x * poly[i].y
		_cands.append([absf(ar) / 2.0, String(f["id"]), poly])
	_cands.sort_custom(func(a, b): return a[0] < b[0])


func _apply_ids() -> Dictionary:
	var groups: Array = JSON.parse_string(FileAccess.get_file_as_string(ids_json))
	_prep_cands(groups)
	var env_nodes: Array = scene.find_children("*", "WorldEnvironment", true, false)
	for wn in env_nodes:
		var env: Environment = (wn as WorldEnvironment).environment
		env.background_mode = Environment.BG_COLOR
		env.background_color = Color(0, 0, 0)
		env.fog_enabled = false
		env.glow_enabled = false
		env.adjustment_enabled = false
		env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
		env.tonemap_exposure = 1.0
	var black := StandardMaterial3D.new()
	black.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	black.albedo_color = Color(0, 0, 0)
	black.cull_mode = BaseMaterial3D.CULL_DISABLED
	var hits := {}
	for n in scene.find_children("*", "MeshInstance3D", true, false):
		var mi := n as MeshInstance3D
		if not mi.visible:
			continue
		var bb: AABB = mi.global_transform * mi.get_aabb()
		var c := bb.get_center()
		var fid := String(mi.name) if String(mi.name) != "" and _is_feature(String(mi.name)) else _feature_hit(Vector2(c.x, c.z))
		var gi := -1
		for g in groups:
			var m: Array = g["match"]
			if fid in m or (bb.end.y <= 0.05 and bb.position.y <= -1.0 and "@cliff" in m) or ("@stair" in m and String(mi.name).begins_with("stair")):
				gi = int(g["idx"])
				break
		if gi < 0:
			mi.material_override = black
			continue
		var mat := StandardMaterial3D.new()
		mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		mat.cull_mode = BaseMaterial3D.CULL_DISABLED
		mat.albedo_color = Color8((gi % 16) * 16 + 8, (gi / 16) * 16 + 8, 200)
		mi.material_override = mat
		hits[gi] = int(hits.get(gi, 0)) + 1
	return hits


func _is_feature(name: String) -> bool:
	for f in layout["features"]:
		if String(f["id"]) == name:
			return true
	return false


func _swap_ground() -> void:
	var img := Image.load_from_file(ground_png)
	var tex := ImageTexture.create_from_image(img)
	var n_sw := 0
	for n in scene.find_children("*", "MeshInstance3D", true, false):
		var mi := n as MeshInstance3D
		var m = mi.material_override
		if m is StandardMaterial3D and (m as StandardMaterial3D).albedo_texture != null:
			var m2 := (m as StandardMaterial3D).duplicate() as StandardMaterial3D
			m2.albedo_texture = tex
			mi.material_override = m2
			n_sw += 1
	print("[bvp] ground swapped on %d meshes" % n_sw)


func _run() -> void:
	for i in 30:
		await process_frame
	if scene.cam == null:
		print("[bvp] HALT: the scene never built its camera")
		quit(3)
		return
	layout = scene.layout
	scene.free_cam = true
	_hide_aids()
	var info := {"mode": mode, "tile": TILE, "tiles": []}
	if mode == "ids":
		info["groups_hit"] = _apply_ids()
	elif ground_png != "":
		_swap_ground()
	cam = Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	var a := deg_to_rad(float(fr["pitch_deg"]))
	cam.rotation = Vector3(-a, 0.0, 0.0)
	cam.near = 1.0
	cam.far = 500.0
	vp.add_child(cam)
	cam.make_current()
	var P := float(fr["px_per_m"])
	var X0 := float(fr["origin_px"][0])
	var Y0 := float(fr["origin_px"][1])
	var W := int(fr["size_px"][0])
	var H := int(fr["size_px"][1])
	cam.size = float(TILE) / P
	for ty in int(ceil(float(H) / TILE)):
		for tx in int(ceil(float(W) / TILE)):
			var cx := tx * TILE + TILE / 2.0
			var cy := ty * TILE + TILE / 2.0
			var x := (cx - X0) / P
			var y := (cy - Y0) / (P * sin(a))
			cam.position = Vector3(x, 0.0, y) + Vector3(0.0, sin(a), cos(a)) * 150.0
			for k in 4:
				await process_frame
			await RenderingServer.frame_post_draw
			var img := vp.get_texture().get_image()
			var p := out_dir.path_join("%s_t%02d_%02d.png" % [mode, tx, ty])
			img.save_png(p)
			info["tiles"].append({"file": p.get_file(), "tx": tx, "ty": ty, "px": [tx * TILE, ty * TILE], "target_m": [x, y]})
			print("[bvp] %s tile %d,%d target (%.3f, %.3f) -> %s" % [mode, tx, ty, x, y, p.get_file()])
	var f := FileAccess.open(out_dir.path_join("%s_tiles.json" % mode), FileAccess.WRITE)
	f.store_string(JSON.stringify(info, " "))
	f.close()
	print("[bvp] done %s: %d tiles" % [mode, info["tiles"].size()])
	quit(0)
