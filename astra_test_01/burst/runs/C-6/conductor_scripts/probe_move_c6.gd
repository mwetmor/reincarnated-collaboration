extends SceneTree
# Conductor proof (C-6 predicate 4): each of the eight input vectors plays its walk cell; Space plays jump; feet stay on walkable ground.
func _initialize():
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	var anim = keeper.get_node("AnimatedSprite2D")
	var data = JSON.parse_string(FileAccess.get_file_as_string(OS.get_environment("WALKABLE")))
	var polys = []
	for p in data["walkable"]:
		var arr = PackedVector2Array()
		for v in p:
			arr.append(Vector2(v[0], v[1]))
		polys.append(arr)
	var start = Vector2(2285.62, 2407.32)
	var tests = [["S", ["move_down"]], ["SW", ["move_down", "move_left"]], ["W", ["move_left"]], ["NW", ["move_up", "move_left"]], ["N", ["move_up"]], ["NE", ["move_up", "move_right"]], ["E", ["move_right"]], ["SE", ["move_down", "move_right"]]]
	for t in tests:
		keeper.global_position = start
		await physics_frame
		var s0 = keeper.global_position
		for a in t[1]:
			Input.action_press(a)
		var off = 0
		var seen = {}
		for f in 90:
			await physics_frame
			seen[anim.animation] = true
			var inside = false
			for poly in polys:
				if Geometry2D.is_point_in_polygon(keeper.global_position, poly):
					inside = true
					break
			if not inside:
				off += 1
		for a in t[1]:
			Input.action_release(a)
		await physics_frame
		print("DIR ", t[0], " moved ", s0.distance_to(keeper.global_position), " frames_off_walkable ", off, " anims ", seen.keys(), " expect walk_", t[0])
	keeper.global_position = start
	await physics_frame
	Input.action_press("jump")
	await physics_frame
	Input.action_release("jump")
	var seen_j = {}
	for f in 40:
		await physics_frame
		seen_j[anim.animation] = true
	print("JUMP anims ", seen_j.keys(), " expect jump_*")
	quit()
