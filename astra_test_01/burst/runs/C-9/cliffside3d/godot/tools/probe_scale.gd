extends SceneTree
# C-9 R-C9-69: reconcile the three heights. mesh.get_aabb() is LOCAL to the MeshInstance;
# bone poses are in the RIG's units and the Skeleton3D's transform converts them. If those
# two chains disagree the stride is in one unit and the figure scale in another, and the
# only number that settles it is the one the camera sees.
const MODEL := "res://models/T8-barbarian.glb"
func _initialize():
	var glb := (load(MODEL) as PackedScene).instantiate()
	root.add_child(glb)
	await process_frame
	var skel: Skeleton3D = null
	var mesh: MeshInstance3D = null
	for n in glb.find_children("*", "", true, false):
		if n is Skeleton3D: skel = n
		elif n is MeshInstance3D and mesh == null: mesh = n
	print("glb root  scale %s" % str(glb.global_transform.basis.get_scale().snappedf(0.0001)))
	print("mesh node scale %s   local aabb size %s" %
		[str(mesh.global_transform.basis.get_scale().snappedf(0.0001)),
		 str(mesh.get_aabb().size.snappedf(0.0001))])
	var wa: AABB = mesh.global_transform * mesh.get_aabb()
	print("mesh WORLD aabb  min %s  size %s" % [str(wa.position.snappedf(0.0001)), str(wa.size.snappedf(0.0001))])
	print("skel node scale %s" % str(skel.global_transform.basis.get_scale().snappedf(0.0001)))
	for b in ["Hips", "Head", "head_end", "LeftToeBase"]:
		var i := skel.find_bone(b)
		if i < 0: continue
		var w: Vector3 = skel.global_transform * skel.get_bone_global_pose(i).origin
		print("  bone %-12s pose %s -> world %s" %
			[b, str(skel.get_bone_global_pose(i).origin.snappedf(0.01)), str(w.snappedf(0.0001))])
	quit(0)
