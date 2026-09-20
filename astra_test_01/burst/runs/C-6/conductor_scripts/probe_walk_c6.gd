extends SceneTree
# C-6 conductor capture: walk the player across the clearing in the real renderer and save viewport frames (C-5 probe_walk_necro lineage).
var out_dir = OS.get_environment("PROBE_OUT")
func _initialize():
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	keeper.global_position = Vector2(3700, 640)
	for f in 10: await physics_frame
	var n = 0
	var legs = [["", 24], ["move_down", 70], ["move_right", 90], ["move_up", 60], ["move_left", 90], ["", 24]]
	for leg in legs:
		if leg[0] != "": Input.action_press(leg[0])
		for f in leg[1]:
			await physics_frame
			if f % 2 == 0:
				root.get_texture().get_image().save_png(out_dir + "/walk_%04d.png" % n); n += 1
		if leg[0] != "": Input.action_release(leg[0])
		for f in 4: await physics_frame
	print("frames ", n, " final feet ", keeper.global_position)
	quit()
