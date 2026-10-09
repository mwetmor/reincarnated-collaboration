extends SceneTree
## BV2F lane PT (R-C9-191): v1's tools/export_hero_meshes.gd COPIED, three marked changes (BV2F-PT): the scene is the
## pilot (res://scenes/bv2f_pilot.tscn, BV2F_UNGROUP=1), the guide size is the pilot plate, and the REAL set is every id
## whose node carries LV's bv2f_fit meta (a placed GLB model) that the pilot ID render shows (--ids FILE, one per line).
## C-9 T10-2 step 4 (B): the real-model heroes' meshes in WORLD space, exactly as the blockout
## places them -- the input to tools/hero_surface.py, which builds the surface file the
## character's projection bake (t5_06b_bake.py) reads. drax.
##
##   Godot --path godot --resolution 640x360 --script tools/export_hero_meshes.gd -- --out DIR
##
## Why from the running scene and not from the GLB: each hero stands under a fit node with a
## NON-UNIFORM scale (the pitch stretch, e.g. the lintel's 2.28 x 3.78 x 2.28) under a yawed root.
## The placed mesh is the one the painting was made over; re-deriving that transform elsewhere is
## a second derivation of one thing, and the bake's self-test would be testing the copy.
##
## Per piece, into --out:
##   <id>.json      header: counts, the original albedo texture, the world AABB, and the piece's
##                  own screen rect under the guide camera (the plate's rect must contain it)
##   <id>_V.f32     world vertices (n x 3)       <id>_N.f32  world normals (n x 3)
##   <id>_UV.f32    UVs, GODOT convention (v down) (n x 2)     <id>_I.i32  triangle indices

var GUIDE := Vector2i(6656, 4096) if OS.get_environment("BV2F_PILOT") == "site_ph3" else Vector2i(4096, 2560)   # BV2F-PT: the pilot plate; R-C9-322: the full site plate for site_ph3
var REAL_IDS := []                      # BV2F-PT: from --ids

var out_dir := ""
var vp: SubViewport
var scene


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
		if args[i] == "--ids" and i + 1 < args.size():   # BV2F-PT
			for ln in FileAccess.get_file_as_string(args[i + 1]).split("\n"):
				if ln.strip_edges() != "":
					REAL_IDS.append(ln.strip_edges())
	if out_dir == "":
		print("[meshes] HALT: --out DIR is required")
		quit(2)
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = GUIDE
	vp.own_world_3d = true
	vp.render_target_update_mode = SubViewport.UPDATE_ONCE
	root.add_child(vp)
	scene = load("res://scenes/bv2f_pilot.tscn").instantiate()   # BV2F-PT
	scene.skip_character = true
	vp.add_child(scene)
	var waited := 0
	while not scene.ready_done and waited < 1500:
		await process_frame
		waited += 1
	if not scene.ready_done:
		print("[meshes] HALT: the scene never finished building")
		quit(3)
		return
	var gw: Dictionary = scene.layout["frame"]["guide_window"]
	var gc: Array = gw["centre_uv"]
	scene.park_camera(scene.uv_to_world(float(gc[0]), float(gc[1])), 1.0)
	await process_frame
	var cam: Camera3D = scene.cam
	var n_done := 0
	var n_overlap := 0   # BV2F-PT R-C9-326
	for e in scene.layout["placements"]:
		var id := String(e["id"])
		if not REAL_IDS.has(id) or not scene.nodes.has(id) or not (scene.nodes[id] as Node).has_meta("bv2f_fit"):   # BV2F-PT
			continue
		var Vs := PackedFloat32Array()
		var Ns := PackedFloat32Array()
		var UVs := PackedFloat32Array()
		var Is := PackedInt32Array()
		var tex := ""
		var lo := Vector3(INF, INF, INF)
		var hi := -lo
		var rmin := Vector2(INF, INF)
		var rmax := -rmin
		var surfaces := 0
		for mi in scene._meshes(scene.nodes[id]):
			var m := mi as MeshInstance3D
			var xf: Transform3D = m.global_transform
			var nb: Basis = xf.basis.inverse().transposed()
			var mat = m.material_override
			if tex == "" and mat is ShaderMaterial:
				var t = (mat as ShaderMaterial).get_shader_parameter("albedo_tex")
				if t is Texture2D:
					tex = (t as Texture2D).resource_path
			for s in m.mesh.get_surface_count():
				var arr: Array = m.mesh.surface_get_arrays(s)
				var v: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
				# BV2F-PT R-C9-322: a surface may carry NO normal / UV / index array (Nil): read as empty (-> skipped below)
				var nrm: PackedVector3Array = arr[Mesh.ARRAY_NORMAL] if arr[Mesh.ARRAY_NORMAL] != null else PackedVector3Array()
				var uv: PackedVector2Array = arr[Mesh.ARRAY_TEX_UV] if arr[Mesh.ARRAY_TEX_UV] != null else PackedVector2Array()
				var ix: PackedInt32Array = arr[Mesh.ARRAY_INDEX] if arr[Mesh.ARRAY_INDEX] != null else PackedInt32Array()
				if uv.size() != v.size():
					print("[meshes] %s surface %d has no UVs -- skipped" % [id, s])
					continue
				var base := Vs.size() / 3
				for k in v.size():
					var p: Vector3 = xf * v[k]
					Vs.append_array([p.x, p.y, p.z])
					var q: Vector3 = (nb * nrm[k]).normalized() if nrm.size() == v.size() else Vector3.UP
					Ns.append_array([q.x, q.y, q.z])
					UVs.append_array([uv[k].x, uv[k].y])
					lo = lo.min(p)
					hi = hi.max(p)
					var sp := cam.unproject_position(p)
					rmin = rmin.min(sp)
					rmax = rmax.max(sp)
				if ix.is_empty():
					for k in v.size():
						Is.append(base + k)
				else:
					for k in ix.size():
						Is.append(base + ix[k])
				surfaces += 1
		# BV2F-PT R-C9-326: the summed UV area of every exported triangle; > 1.0 = UVs OVERLAP (two surfaces sharing 0..1,
		# e.g. LV's procedural post: shaft + tip) -- a bake then holds only one of them; reported, never fixed here
		var uv_area := 0.0
		for t in range(0, Is.size(), 3):
			var p0 := Vector2(UVs[Is[t] * 2], UVs[Is[t] * 2 + 1])
			var p1 := Vector2(UVs[Is[t + 1] * 2], UVs[Is[t + 1] * 2 + 1])
			var p2 := Vector2(UVs[Is[t + 2] * 2], UVs[Is[t + 2] * 2 + 1])
			uv_area += absf((p1 - p0).cross(p2 - p0)) * 0.5
		if uv_area > 1.0:
			print("[meshes] UV OVERLAP %s: summed UV area %.3f > 1.0 (a bake holds only part of it)" % [id, uv_area])
			n_overlap += 1
		_raw("%s/%s_V.f32" % [out_dir, id], Vs.to_byte_array())
		_raw("%s/%s_N.f32" % [out_dir, id], Ns.to_byte_array())
		_raw("%s/%s_UV.f32" % [out_dir, id], UVs.to_byte_array())
		_raw("%s/%s_I.i32" % [out_dir, id], Is.to_byte_array())
		var f := FileAccess.open("%s/%s.json" % [out_dir, id], FileAccess.WRITE)
		f.store_string(JSON.stringify({"id": id, "class": e["class"], "glb": e.get("glb", ""),
			"surfaces": surfaces, "verts": Vs.size() / 3, "tris": Is.size() / 3,
			"uv_area_sum": snappedf(uv_area, 0.001), "uv_overlap": uv_area > 1.0,   # BV2F-PT R-C9-326
			"albedo_texture": tex, "uv_convention": "godot (v down)",
			"aabb_world": [[lo.x, lo.y, lo.z], [hi.x, hi.y, hi.z]],
			"screen_rect_px": [rmin.x, rmin.y, rmax.x - rmin.x, rmax.y - rmin.y]}, " "))
		n_done += 1
	print("[meshes] %d real-model heroes exported to %s; %d with UV OVERLAP (R-C9-326)" % [n_done, out_dir, n_overlap])   # BV2F-PT R-C9-326
	quit(0)


func _raw(path: String, bytes: PackedByteArray) -> void:
	var f := FileAccess.open(path, FileAccess.WRITE)
	f.store_buffer(bytes)
