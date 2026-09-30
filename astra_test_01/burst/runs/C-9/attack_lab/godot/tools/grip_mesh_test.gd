extends SceneTree
# INSTRUMENT CHECK for the penetration test: is the blend-shape-mix bake in the base vertex order,
# and is crossing parity along +Y consistent with -Y and +X on this body mesh?
func _cross(tm: TriangleMesh, p: Vector3, d: Vector3) -> int:
	var o := p; var n := 0
	for i in 64:
		var r = tm.intersect_ray(o, d)
		if typeof(r) != TYPE_DICTIONARY or (r as Dictionary).is_empty(): break
		n += 1; o = (r["position"] as Vector3) + d * 0.002
	return n
func _initialize() -> void:
	create_timer(300.0).timeout.connect(func(): push_error("WATCHDOG"); quit(4))
	var k = load("res://scripts/knight.gd").new()
	k.setup(Vector3.RIGHT, Vector3.UP, Vector3.FORWARD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	for i in 4: await process_frame
	var body: MeshInstance3D = k._mesh
	(k._tree as AnimationTree).active = false
	var ap: AnimationPlayer = k._anim
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	ap.play("idle_armed"); ap.seek(0.5, true, true)
	var arr := body.mesh.surface_get_arrays(0)
	var mix: ArrayMesh = body.bake_mesh_from_current_blend_shape_mix()
	var marr := mix.surface_get_arrays(0)
	var bv: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
	var mv: PackedVector3Array = marr[Mesh.ARRAY_VERTEX]
	print("base verts %d idx %d | mix verts %d idx %s bones %s" % [bv.size(), (arr[Mesh.ARRAY_INDEX] as PackedInt32Array).size(), mv.size(),
		str((marr[Mesh.ARRAY_INDEX] as PackedInt32Array).size() if marr[Mesh.ARRAY_INDEX] != null else -1), str(marr[Mesh.ARRAY_BONES] != null)])
	var same := 0; var moved := 0; var far := 0.0
	for i in mini(bv.size(), mv.size()):
		var d: float = (bv[i] - mv[i]).length()
		if d < 1e-4: same += 1
		else: moved += 1; far = maxf(far, d)
	print("mix vs base, same index: %d identical, %d moved (max %.3f units)" % [same, moved, far])
	print("blend shapes: ", body.get_blend_shape_count(), " values ", range(body.get_blend_shape_count()).map(func(i): return body.get_blend_shape_value(i)))
	# parity consistency on the plain skinned body (no proxy)
	var baked: ArrayMesh = body.bake_mesh_from_current_skeleton_pose()
	var tm: TriangleMesh = baked.generate_triangle_mesh()
	var box: AABB = baked.get_aabb()
	print("baked aabb ", box)
	var agree := 0; var n := 0; var ins := 0; var dis := {"up_dn": 0, "up_x": 0}
	seed(7)
	for s in 3000:
		var p := box.position + Vector3(randf() * box.size.x, randf() * box.size.y, randf() * box.size.z)
		var u := _cross(tm, p, Vector3.UP) % 2
		var dn := _cross(tm, p, Vector3.DOWN) % 2
		var x := _cross(tm, p, Vector3.RIGHT) % 2
		n += 1
		if u == dn and u == x: agree += 1
		if u != dn: dis["up_dn"] += 1
		if u != x: dis["up_x"] += 1
		if u == 1 and dn == 1 and x == 1: ins += 1
	print("parity on the skinned body, %d random points in its box: all three directions agree %d (%.1f%%); up!=down %d, up!=x %d; unanimous inside %d"
		% [n, agree, 100.0 * agree / n, dis["up_dn"], dis["up_x"], ins])
	quit(0)
