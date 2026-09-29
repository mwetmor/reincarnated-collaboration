extends SceneTree
# C-9 T7-A: is the character GLB centred on its own origin?
#
# The "in front of a post" sweep put the stand-in at the post's exact canvas x and measured
# 0% of the post covered -- and a second probe, which happened not to drive his facing,
# found him 1.5 m away from where the first one did. A 180 deg yaw that MOVES a body is a
# body that is not on its own axis of rotation.
func _initialize():
	var glb := (load("res://models/knight_t3.glb") as PackedScene).instantiate()
	root.add_child(glb)
	await process_frame
	var ab := AABB()
	var first := true
	for m in glb.find_children("*", "MeshInstance3D", true, false):
		var mi := m as MeshInstance3D
		if mi.mesh == null:
			continue
		var a: AABB = mi.get_aabb()
		# into the GLB root's own space
		var t: Transform3D = glb.global_transform.affine_inverse() * mi.global_transform
		var w := AABB(t * a.position, Vector3.ZERO)
		for i in 8:
			w = w.expand(t * a.get_endpoint(i))
		ab = w if first else ab.merge(w)
		first = false
		print("  mesh %-24s aabb pos %s size %s" % [mi.name, str(a.position.snappedf(0.001)), str(a.size.snappedf(0.001))])
	print("")
	print("combined, in GLB-local metres:")
	print("  min %s   max %s   size %s" % [str(ab.position.snappedf(0.001)),
		 str((ab.position + ab.size).snappedf(0.001)), str(ab.size.snappedf(0.001))])
	var cx := ab.position.x + ab.size.x * 0.5
	var cz := ab.position.z + ab.size.z * 0.5
	print("  horizontal centre (%.3f, %.3f) m  -> off-axis by %.3f m" % [cx, cz, Vector2(cx, cz).length()])
	print("  lowest point y = %.3f m  (0 = feet on the origin plane)" % ab.position.y)
	quit(0)
