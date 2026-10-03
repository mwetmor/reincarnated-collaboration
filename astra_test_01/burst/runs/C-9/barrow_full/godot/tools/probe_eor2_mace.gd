extends SceneTree
## C-9 R-C9-143 (lane EOR2): how the dark knight's mace hangs -- its node path, transforms, skin, AABB -- so the
## kc2 port measures the real steel. drax.
func _initialize() -> void:
	var scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)
	while not scene.ready_done:
		await process_frame
	var k = scene.knight
	for f in 10:
		await process_frame
	var sk: Skeleton3D = k._skel
	var wb := sk.find_bone("weapon_r")
	var pieces: Dictionary = (k.get("gear") as Dictionary).get("_pieces", {})
	for mi in (pieces.get("wl_mace", []) as Array):
		var m := mi as MeshInstance3D
		var aabb := m.mesh.get_aabb()
		print("MACE path=", k.get_path_to(m), " parent=", m.get_parent().name, " skel_np=", m.skeleton, " skin=", m.skin != null,
			" xf=", m.transform, " gxf=", m.global_transform, " aabb=", aabb, " skel_gxf=", sk.global_transform,
			" wr_rest=", sk.get_bone_global_rest(wb), " wr_pose_g=", sk.global_transform * sk.get_bone_global_pose(wb))
		if m.skin != null:
			for b in m.skin.get_bind_count():
				print("  bind ", b, " ", m.skin.get_bind_name(b), " ", m.skin.get_bind_bone(b))
		var arr: Array = m.mesh.surface_get_arrays(0)
		var bones = arr[Mesh.ARRAY_BONES]
		var w = arr[Mesh.ARRAY_WEIGHTS]
		print("  bones_sample=", (bones as PackedInt32Array).slice(0, 8) if bones != null else null, " w=", (w as PackedFloat32Array).slice(0, 8) if w != null else null)
	print("HEADLOCAL ", scene.whirl.fx.get("_head_local") if scene.whirl != null else null, " report=", JSON.stringify(scene.whirl.report()) if scene.whirl != null else "")
	quit(0)
