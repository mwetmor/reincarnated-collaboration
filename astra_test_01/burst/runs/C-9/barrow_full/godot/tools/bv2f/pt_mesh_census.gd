extends SceneTree
## BV2F PT (R-C9-268 item 2): which meshes carry the frame's primitives -- every visible GeometryInstance3D in the built
## pilot, its triangle count (x instances for a MultiMesh), its shadow-casting mode and its material. Read-only.
##   Godot --path . --resolution 640x360 --script res://tools/bv2f/pt_mesh_census.gd -- <scene> <OUT>
var scene
func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	scene = load(a[0]).instantiate()
	root.add_child(scene)
	_run(a[1])

func _tris(m: Mesh) -> int:
	var t := 0
	if m == null:
		return 0
	for s in m.get_surface_count():
		var arr := m.surface_get_arrays(s)
		var idx = arr[Mesh.ARRAY_INDEX]
		t += (idx.size() / 3) if idx != null and idx.size() > 0 else (arr[Mesh.ARRAY_VERTEX].size() / 3)
	return t

func _run(out: String) -> void:
	var w := 0
	while not scene.ready_done and w < 4000:
		await process_frame
		w += 1
	var rows := []
	var stack := [scene]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if n is GeometryInstance3D and (n as Node3D).is_visible_in_tree():
			var g := n as GeometryInstance3D
			var tris := 0
			var inst := 1
			if g is MeshInstance3D:
				tris = _tris((g as MeshInstance3D).mesh)
			elif g is MultiMeshInstance3D and (g as MultiMeshInstance3D).multimesh != null:
				var mm := (g as MultiMeshInstance3D).multimesh
				inst = mm.instance_count if mm.visible_instance_count < 0 else mm.visible_instance_count
				tris = _tris(mm.mesh) * inst
			else:
				continue
			rows.append({"path": str(scene.get_path_to(g)), "tris": tris, "instances": inst,
						 "shadow": g.cast_shadow, "aabb_size": [snappedf(g.get_aabb().size.x, 0.1), snappedf(g.get_aabb().size.z, 0.1)]})
	rows.sort_custom(func(x, y): return x["tris"] > y["tris"])
	var tot := 0
	var tot_sh := 0
	for r in rows:
		tot += int(r["tris"])
		if int(r["shadow"]) != 0:
			tot_sh += int(r["tris"])
	var f := FileAccess.open(out.path_join("mesh_census.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify({"total_tris": tot, "shadow_casting_tris": tot_sh, "n": rows.size(), "rows": rows}, " "))
	f.close()
	print("[census] total ", tot, " shadow-casting ", tot_sh, " n ", rows.size())
	quit(0)
