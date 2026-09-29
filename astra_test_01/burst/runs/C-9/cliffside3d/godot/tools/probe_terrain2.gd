extends SceneTree
# Which winding is VISIBLE from the play camera? Not which one matches a convention I
# remember -- the convention is the thing I would get backwards. Build the same grid both
# ways, render each from above with backface culling on, and count the pixels it covers.
const R := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const U := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const F := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)

func _initialize() -> void:
	var w := BarrowHeightfield.new("res://data/height_a_authored.png",
								   "res://data/height_a_authored.json")
	var vp := SubViewport.new(); vp.size = Vector2i(320, 320); vp.own_world_3d = true
	vp.transparent_bg = true; vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL; cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.size = 18.0; cam.near = 0.05; cam.far = 400.0
	vp.add_child(cam); cam.current = true
	cam.global_transform = Transform3D(Basis(R, U, -F), Vector3(0, 0, -2) - F * 120.0)
	for order in [[0, 1, 2], [0, 2, 1]]:
		var n := 60
		var verts := PackedVector3Array(); var idx := PackedInt32Array()
		verts.resize((n + 1) * (n + 1))
		for j in n + 1:
			for i in n + 1:
				var x := -9.0 + float(i) * 0.3
				var z := -11.0 + float(j) * 0.3
				verts[j * (n + 1) + i] = Vector3(x, w.height_at(x, z), z)
		for j in n:
			for i in n:
				var k := j * (n + 1) + i
				var t1 := [k, k + n + 1, k + n + 2]
				var t2 := [k, k + n + 2, k + 1]
				for t in [t1, t2]:
					idx.append(t[order[0]]); idx.append(t[order[1]]); idx.append(t[order[2]])
		var arr := []; arr.resize(Mesh.ARRAY_MAX)
		arr[Mesh.ARRAY_VERTEX] = verts; arr[Mesh.ARRAY_INDEX] = idx
		var mesh := ArrayMesh.new(); mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
		var mat := StandardMaterial3D.new()
		mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		mat.albedo_color = Color(1, 0, 0)
		mat.cull_mode = BaseMaterial3D.CULL_BACK      # the default: this is the question
		var mi := MeshInstance3D.new(); mi.mesh = mesh; mi.material_override = mat
		vp.add_child(mi)
		for i in 4: await process_frame
		var img := vp.get_texture().get_image()
		var cov := 0
		for y in range(0, 320, 2):
			for x in range(0, 320, 2):
				if img.get_pixel(x, y).a > 0.5: cov += 1
		print("[wind] order %s -> %d of %d sampled pixels covered (%.1f%%)"
			% [str(order), cov, 160 * 160, 100.0 * cov / (160 * 160)])
		mi.queue_free(); await process_frame
	quit(0)
