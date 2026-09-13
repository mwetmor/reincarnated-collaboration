extends SceneTree
# Conductor proof: drive the Keeper with input actions headless; verify movement and that collision keeps feet on walkable ground.
func _initialize():
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	var data = JSON.parse_string(FileAccess.get_file_as_string(OS.get_environment("WALKABLE")))
	var polys = []
	for p in data["walkable"]:
		var arr = PackedVector2Array()
		for v in p:
			arr.append(Vector2(v[0], v[1]))
		polys.append(arr)
	var tests = [["move_up", 900, Vector2(2285.62, 2407.32)], ["move_left", 900, Vector2(2285.62, 2407.32)], ["move_down", 900, Vector2(2285.62, 2407.32)], ["move_right", 1500, Vector2(2285.62, 2407.32)], ["move_right", 900, Vector2(5200, 900)], ["move_right", 900, Vector2(5200, 1373)], ["move_down", 900, Vector2(1900, 3900)], ["move_left", 900, Vector2(200, 3000)], ["move_up", 900, Vector2(4600, 120)], ["move_up", 1200, Vector2(3015, 1240)]]
	for t in tests:
		keeper.global_position = t[2]
		await physics_frame
		var start = keeper.global_position
		var off = 0
		Input.action_press(t[0])
		for f in t[1]:
			await physics_frame
			var inside = false
			for poly in polys:
				if Geometry2D.is_point_in_polygon(keeper.global_position, poly):
					inside = true
					break
			if not inside:
				off += 1
		Input.action_release(t[0])
		await physics_frame
		print(t[0], " start ", start, " end ", keeper.global_position, " moved ", start.distance_to(keeper.global_position), " frames_off_walkable ", off, " anim ", keeper.get_node("AnimatedSprite2D").animation)
	quit()
