extends SceneTree
# Can the two instruments see ANYTHING? A zero from an instrument that cannot see is not a
# zero. Control: the same shield test with the guard layer OFF, which the export says is
# 128 of 1829 inside for the carry pose -- if that also reads 0, the test is blind.
const DT := 1.0 / 24.0
func _initialize():
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60: await process_frame
	Engine.physics_ticks_per_second = 24
	var k = scene.knight
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	for i in 6: k.drive_dir(Vector2.ZERO, false, DT); await physics_frame
	print("gear keys: ", str(k.gear.keys()))
	for key in k.gear.keys():
		if String(key).begins_with("_markers_"):
			print("   %s -> %s" % [key, str((k.gear[key] as Dictionary).keys())])
	var skel: Skeleton3D = k._skel
	print("bones with 'Spine': ")
	for b in skel.get_bone_count():
		var nm := skel.get_bone_name(b)
		if nm.contains("Spine") or nm == "Hips" or nm.contains("Neck"):
			print("   %-12s at %s" % [nm, str((skel.global_transform * skel.get_bone_global_pose(b).origin).snappedf(0.001))])
	var sh: MeshInstance3D = null
	var v = k.gear.get("shield", null)
	if v is Array and v.size() > 0: sh = v[0]
	print("shield mesh: ", sh)
	if sh != null:
		var arr = sh.mesh.surface_get_arrays(0)
		var verts: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
		var xf := sh.global_transform
		var lo := Vector3(1e9,1e9,1e9); var hi := -lo
		for i in range(0, verts.size(), maxi(1, verts.size()/2000)):
			var w: Vector3 = xf * verts[i]
			lo = lo.min(w); hi = hi.max(w)
		print("   shield world AABB  min %s  max %s" % [str(lo.snappedf(0.01)), str(hi.snappedf(0.01))])
		print("   NOTE the shield is a SKINNED mesh: its global_transform is the skeleton's, and")
		print("   its vertices are in REST pose unless the skin is applied -- so a world AABB")
		print("   built this way does NOT follow the animation. That is the defect to check.")
		var hips: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone("Hips")).origin
		print("   hips at %s ; shield centre at %s ; separation %.3f m" %
			[str(hips.snappedf(0.01)), str(((lo+hi)*0.5).snappedf(0.01)), (((lo+hi)*0.5) - hips).length()])
	quit(0)
