extends SceneTree
## BV2F LV debug: where a placed model's highest vertices sit, in the sim frame (level-local x, y).
##   Godot --path godot --script tools/bv2f/inspect_model.gd -- <node id>
func _initialize() -> void:
	var id := OS.get_cmdline_user_args()[0]
	var vp := SubViewport.new()
	vp.size = Vector2i(320, 180)
	vp.own_world_3d = true
	root.add_child(vp)
	var scene = load("res://scenes/bv2f_barrow_v2.tscn").instantiate()
	scene.skip_character = true
	vp.add_child(scene)
	var w := 0
	while not scene.ready_done and w < 1500:
		await process_frame
		w += 1
	var n: Node3D = scene.nodes[id]
	var inv: Transform3D = scene.level.global_transform.affine_inverse()
	var pts := []
	for mi in n.find_children("*", "MeshInstance3D", true, false):
		var m := mi as MeshInstance3D
		if String(m.name).ends_with("_ink"):
			continue
		var arr = m.mesh.surface_get_arrays(0)
		var vs: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
		var xf: Transform3D = inv * m.global_transform
		for k in range(0, vs.size(), 7):
			pts.append(xf * vs[k])
	pts.sort_custom(func(a, b): return a.y > b.y)
	var top := []
	for k in 20:
		top.append([snappedf(pts[k].x, 0.01), snappedf(pts[k].z, 0.01), snappedf(pts[k].y, 0.01)])
	var lo := Vector3(INF, INF, INF)
	var hi := -lo
	for p in pts:
		lo = lo.min(p)
		hi = hi.max(p)
	print("[inspect] %s highest (sim x, y, z): %s" % [id, str(top.slice(0, 8))])
	print("[inspect] %s bbox sim x %.2f..%.2f y %.2f..%.2f z %.2f..%.2f" % [id, lo.x, hi.x, lo.z, hi.z, lo.y, hi.y])
	quit(0)
