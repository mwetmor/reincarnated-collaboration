extends SceneTree
# C-9 D2: the manifest lists ten bracer objects. Eight of them came back with a zero-size
# AABB. Empty meshes cost nothing and hide nothing, but "ten pieces" in a manifest and two
# meshes on a body is a difference worth knowing before it is reported as working.
func _initialize():
	for f in ["bracers", "helmet", "axe", "shield", "byrnie", "mantle"]:
		var p := (load("res://models/gear/" + f + ".glb") as PackedScene).instantiate()
		root.add_child(p)
		await process_frame
		var total := 0
		var line := ""
		for m in p.find_children("*", "MeshInstance3D", true, false):
			var mi := m as MeshInstance3D
			var v := 0
			var t := 0
			for s in mi.mesh.get_surface_count():
				var a := mi.mesh.surface_get_arrays(s)
				v += (a[Mesh.ARRAY_VERTEX] as PackedVector3Array).size()
				var ix = a[Mesh.ARRAY_INDEX]
				t += (ix.size() / 3) if ix != null else 0
			total += t
			line += "  %s:%dv/%dt" % [mi.name, v, t]
		print("%-8s %2d objects, %6d triangles total%s" %
			[f, p.find_children("*", "MeshInstance3D", true, false).size(), total,
			 line if f == "bracers" else ""])
		p.queue_free()
		await process_frame
	quit(0)
