extends SceneTree
# capability check: TriangleMesh scripting API + CPU skin bake, and their cost
func _initialize() -> void:
	create_timer(120.0).timeout.connect(func(): push_error("WATCHDOG"); quit(4))
	print("TriangleMesh class exists: ", ClassDB.class_exists("TriangleMesh"))
	for m in ClassDB.class_get_method_list("TriangleMesh", true):
		print("  TriangleMesh.", m["name"])
	print("bake method: ", ClassDB.class_has_method("MeshInstance3D", "bake_mesh_from_current_skeleton_pose"))
	var k = load("res://scripts/knight.gd").new()
	k.setup(Vector3.RIGHT, Vector3.UP, Vector3.FORWARD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	var mi: MeshInstance3D = k._mesh
	var t0 := Time.get_ticks_usec()
	var baked: ArrayMesh = mi.bake_mesh_from_current_skeleton_pose()
	var t1 := Time.get_ticks_usec()
	var faces: PackedVector3Array = baked.get_faces()
	var t2 := Time.get_ticks_usec()
	var tm := TriangleMesh.new()
	var ok = tm.create_from_faces(faces)
	var t3 := Time.get_ticks_usec()
	print("bake %.1f ms, faces %d (%.1f ms), TriangleMesh build %s %.1f ms" % [(t1 - t0) / 1000.0, faces.size() / 3, (t2 - t1) / 1000.0, str(ok), (t3 - t2) / 1000.0])
	var hits := 0
	var t4 := Time.get_ticks_usec()
	for i in 2000:
		var r = tm.intersect_ray(Vector3(randf_range(-0.3, 0.3), randf_range(0.2, 1.6), randf_range(-0.2, 0.2)), Vector3.UP)
		if r is Dictionary and not (r as Dictionary).is_empty(): hits += 1
	var t5 := Time.get_ticks_usec()
	print("2000 rays %.1f ms, %d hit; sample result %s" % [(t5 - t4) / 1000.0, hits, str(tm.intersect_ray(Vector3(0, 1.0, 0), Vector3.UP))])
	print("mesh global xf ", mi.global_transform, "  skel global ", k._skel.global_transform)
	quit(0)
