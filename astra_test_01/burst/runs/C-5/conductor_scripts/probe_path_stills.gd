extends SceneTree
# v23 proof: the Keeper beside the necromancer on the path (2650,1950); exact 1920x1080 camera; two stills.
var out_dir = OS.get_environment("PROBE_OUT")
func _initialize():
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_VIEWPORT
	root.content_scale_size = Vector2i(1920, 1080)
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	for spot in [["beside", Vector2(2560, 1990)], ["below", Vector2(2650, 2110)]]:
		keeper.global_position = spot[1]
		for f in 10: await physics_frame
		root.get_texture().get_image().save_png(out_dir + "/path_%s.png" % spot[0])
	print("stills done ", keeper.global_position)
	quit()
