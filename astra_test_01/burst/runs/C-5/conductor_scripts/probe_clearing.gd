extends SceneTree
# Conductor proof: load cliffside, teleport the Keeper to sample feet positions, capture the viewport.
var points = [Vector2(3904, 640), Vector2(3700, 760), Vector2(4250, 520), Vector2(4450, 900), Vector2(2285.62, 2407.32)]
var out_dir = OS.get_environment("PROBE_OUT")
func _initialize():
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	var keeper = scene.find_child("Keeper", true, false)
	var cam = scene.find_child("Camera2D", true, false)
	print("keeper ", keeper, " cam ", cam, " spawn ", keeper.global_position if keeper else null)
	for i in points.size():
		keeper.global_position = points[i]
		for f in 6:
			await process_frame
		var img = root.get_texture().get_image()
		img.save_png(out_dir + "/probe_%d.png" % i)
		var sc = cam.get_screen_center_position()
		print("point ", i, " feet ", points[i], " screen_center ", sc)
		for n in ["Layer_sky", "Layer_far_ruins", "Layer_forest_valley", "Layer_mist"]:
			var l = scene.get_node(n)
			print("  ", n, " pos ", l.position, " global ", l.global_position, " screen_offset ", l.screen_offset)
	quit()
