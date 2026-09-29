extends SceneTree
# C-9: he realises 3.36 canvas px per frame where his stride gives 8.40. Is that the
# ground? move_and_slide treats anything steeper than floor_max_angle (45 deg by default)
# as a WALL: the body stops being "on the floor", gravity accumulates, and the horizontal
# velocity is projected against a surface it is supposed to be walking up.
func _initialize():
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 50: await process_frame
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var k = scene.knight
	print("floor_max_angle = %.1f deg" % rad_to_deg(k.floor_max_angle))
	for label in ["tree path", "bridge path", "plateau spawn"]:
		var pts := []
		match label:
			"tree path": pts = [Vector2(1666, 2705), Vector2(1876, 2705), Vector2(2086, 2705)]
			"bridge path": pts = [Vector2(3118, 1472), Vector2(3220, 1230), Vector2(3326, 980)]
			_: pts = [Vector2(2285.62, 2407.32)]
		var s := ""
		for p in pts:
			var from: Vector3 = CliffWorld.canvas_to_plane(p, scene.right, scene.up) - scene.fwd * 150.0
			var q := PhysicsRayQueryParameters3D.create(from, from + scene.fwd * 400.0)
			q.collision_mask = CliffWorld.TERRAIN_BIT
			var h := space.intersect_ray(q)
			if h.is_empty():
				s += "  (no hit)"
				continue
			var n: Vector3 = h["normal"]
			s += "  %.1f deg" % rad_to_deg(acos(clampf(n.dot(Vector3.UP), -1.0, 1.0)))
		print("%-14s slope from vertical:%s" % [label, s])
	quit(0)
