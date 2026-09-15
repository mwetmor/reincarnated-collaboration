extends SceneTree
# C-5 conductor proof: walk the Keeper through the clearing past the dummies, capturing every 3rd frame for the Packet 84 clip.
var out_dir = OS.get_environment("PROBE_OUT")
func _initialize():
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	keeper.global_position = Vector2(3700, 640)
	for f in 6: await physics_frame
	var n = 0
	var legs = [["move_right", 150], ["move_down", 70], ["move_right", 110], ["move_up", 60]]
	for leg in legs:
		Input.action_press(leg[0])
		for f in leg[1]:
			await physics_frame
			if f % 3 == 0:
				root.get_texture().get_image().save_png(out_dir + "/walk_%04d.png" % n); n += 1
		Input.action_release(leg[0])
		for f in 6: await physics_frame
	print("frames ", n, " final feet ", keeper.global_position)
	quit()
