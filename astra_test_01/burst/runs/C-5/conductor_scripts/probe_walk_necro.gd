extends SceneTree
# C-6 conductor proof: walk the Keeper in a loop around the necromancer master prop at (3840,720) so Matt can judge scale/register in the real scene.
var out_dir = OS.get_environment("PROBE_OUT")
func _initialize():
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	keeper.global_position = Vector2(3700, 800)
	for f in 8: await physics_frame
	var n = 0
	# approach from the SW, pass in front (south), circle east, behind (north), back west, end beside it
	var legs = [["move_right", 120], ["move_up", 55], ["move_left", 130], ["move_down", 55], ["move_right", 60]]
	for leg in legs:
		Input.action_press(leg[0])
		for f in leg[1]:
			await physics_frame
			if f % 3 == 0:
				root.get_texture().get_image().save_png(out_dir + "/walk_%04d.png" % n); n += 1
		Input.action_release(leg[0])
		for f in 6: await physics_frame
	root.get_texture().get_image().save_png(out_dir + "/final_beside.png")
	print("frames ", n, " final feet ", keeper.global_position)
	quit()
