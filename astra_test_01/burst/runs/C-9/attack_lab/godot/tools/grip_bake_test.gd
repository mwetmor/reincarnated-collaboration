extends SceneTree
# Does bake_mesh_from_current_skeleton_pose() see the pose a seek just set, or a stale one?
# Manual skinning of sampled vertices from get_bone_global_pose() is the reference.
func _manual(body: MeshInstance3D, skel: Skeleton3D, arr: Array, vi: int) -> Vector3:
	var v: Vector3 = (arr[Mesh.ARRAY_VERTEX] as PackedVector3Array)[vi]
	var bones = arr[Mesh.ARRAY_BONES]; var w = arr[Mesh.ARRAY_WEIGHTS]
	var nb: int = int(bones.size() / (arr[Mesh.ARRAY_VERTEX] as PackedVector3Array).size())
	var acc := Vector3.ZERO; var ws := 0.0
	for j in nb:
		var ww: float = float(w[vi * nb + j])
		if ww <= 0.0: continue
		var bi: int = int(bones[vi * nb + j])
		var b := skel.find_bone(String(body.skin.get_bind_name(bi)))
		acc += (skel.get_bone_global_pose(b) * body.skin.get_bind_pose(bi) * v) * ww; ws += ww
	return acc / ws
func _initialize() -> void:
	create_timer(90.0).timeout.connect(func(): push_error("WATCHDOG"); quit(4))
	var k = load("res://scripts/knight.gd").new()
	k.setup(Vector3.RIGHT, Vector3.UP, Vector3.FORWARD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	for i in 4: await process_frame
	var body: MeshInstance3D = k._mesh
	var skel: Skeleton3D = k._skel
	(k._tree as AnimationTree).active = false
	var ap: AnimationPlayer = k._anim
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var arr := body.mesh.surface_get_arrays(0)
	# a skin whose binds name their bone by INDEX: the bake may not resolve glTF's by-name binds
	var sk2: Skin = body.skin.duplicate()
	var unresolved := 0
	for i in sk2.get_bind_count():
		print_verbose("")
		if sk2.get_bind_bone(i) < 0: unresolved += 1
		sk2.set_bind_bone(i, skel.find_bone(String(sk2.get_bind_name(i))))
	print("[bake] binds with no bone index (by name only): %d of %d" % [unresolved, sk2.get_bind_count()])
	var ids := [1000, 40000, 80000, 120000, 150000]
	for step in [["attack", 0.0], ["attack", 0.7], ["block", 1.0], ["walk_armed", 0.4]]:
		ap.play(String(step[0])); ap.seek(float(step[1]), true, true)
		var bk: ArrayMesh = body.bake_mesh_from_current_skeleton_pose()
		var bv: PackedVector3Array = bk.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
		var errs := []
		for vi in ids: errs.append(snappedf((bv[vi] - _manual(body, skel, arr, vi)).length(), 0.001))
		skel.force_update_all_bone_transforms()
		var bk2: ArrayMesh = body.bake_mesh_from_current_skeleton_pose()
		var bv2: PackedVector3Array = bk2.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
		var errs2 := []
		for vi in ids: errs2.append(snappedf((bv2[vi] - _manual(body, skel, arr, vi)).length(), 0.001))
		skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)
		var bk3: ArrayMesh = body.bake_mesh_from_current_skeleton_pose()
		var bv3: PackedVector3Array = bk3.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
		var errs3 := []
		for vi in ids: errs3.append(snappedf((bv3[vi] - _manual(body, skel, arr, vi)).length(), 0.001))
		print("[bake] %s @ %.2f: bake vs manual skin (units) %s | after force_update %s | after NOTIFICATION_UPDATE_SKELETON %s" % [step[0], step[1], str(errs), str(errs2), str(errs3)])
	quit(0)
