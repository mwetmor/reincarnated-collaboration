extends SceneTree
# T9-1c: what is the near cliff wall made of? Subdividing and displacing it needs to know
# whether it is one quad or an extruded outline, and where its boundary edges are.
func _initialize():
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60: await process_frame
	for mi in scene._fg:
		var n := String((mi as MeshInstance3D).name)
		if not (n.contains("wall") or n.contains("top")): continue
		var m := (mi as MeshInstance3D).mesh
		var a := m.surface_get_arrays(0)
		var v: PackedVector3Array = a[Mesh.ARRAY_VERTEX]
		var ix = a[Mesh.ARRAY_INDEX]
		var nm = a[Mesh.ARRAY_NORMAL]
		var ab: AABB = (mi as MeshInstance3D).global_transform * (mi as MeshInstance3D).get_aabb()
		print("%-24s verts %6d  tris %6d  surfaces %d  normals=%s" %
			[n, v.size(), (ix.size()/3) if ix != null else 0, m.get_surface_count(), nm != null])
		print("    world aabb  min %s  size %s" % [str(ab.position.snappedf(0.01)), str(ab.size.snappedf(0.01))])
		# how many distinct Y values -- a flat top or a varying one
		var ys := {}
		for p in v: ys[snappedf(p.y, 0.01)] = true
		var k := ys.keys(); k.sort()
		print("    distinct Y: %d  -> %s" % [k.size(), str(k.slice(0, 6))])
		# boundary edges: edges used by exactly one triangle
		if ix != null:
			var cnt := {}
			for t in range(0, ix.size(), 3):
				for e in 3:
					var i0: int = ix[t + e]
					var i1: int = ix[t + (e + 1) % 3]
					var key := "%d_%d" % [mini(i0, i1), maxi(i0, i1)]
					cnt[key] = int(cnt.get(key, 0)) + 1
			var b := 0
			for key in cnt:
				if int(cnt[key]) == 1: b += 1
			print("    boundary edges %d of %d" % [b, cnt.size()])
	quit(0)
