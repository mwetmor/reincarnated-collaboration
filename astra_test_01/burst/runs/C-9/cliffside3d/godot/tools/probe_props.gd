extends SceneTree
func _initialize():
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 40: await process_frame
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var px := Vector2(1896.01, 2765.0)          # tree_living_a's anchor
	var plane: Vector3 = CliffWorld.canvas_to_plane(px, scene.right, scene.up)
	print("guide-plane point depth: %.3f" % plane.dot(scene.fwd))
	# every hit along the ray, nearest first, so "the first surface" is not assumed
	var from: Vector3 = plane - scene.fwd * 150.0
	var excl := []
	for n in 6:
		var q := PhysicsRayQueryParameters3D.create(from, from + scene.fwd * 400.0)
		q.exclude = excl
		var h := space.intersect_ray(q)
		if h.is_empty():
			break
		var p: Vector3 = h["position"]
		var col = h["collider"]
		print("  hit %d: depth %8.3f   collider %s   owner %s" %
			[n, p.dot(scene.fwd), col.name, col.get_parent().name])
		excl.append(h["rid"])
	var props = scene.get_node_or_null(^"Props")
	var t0 := props.get_child(0) as MeshInstance3D
	print("card depth: %.3f  (PROP_BIAS applied)" % t0.global_position.dot(scene.fwd))
	quit(0)
