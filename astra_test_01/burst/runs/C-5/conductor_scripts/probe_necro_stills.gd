extends SceneTree
# Stills: Keeper standing at four points around the necromancer prop (3840,720) — camera-scale comparison shots.
var out_dir = OS.get_environment("PROBE_OUT")
func _initialize():
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	var spots = {"south": Vector2(3840, 800), "west": Vector2(3740, 730), "east": Vector2(3940, 730), "north": Vector2(3840, 650)}
	for k in spots:
		keeper.global_position = spots[k]
		for f in 10: await physics_frame
		root.get_texture().get_image().save_png(out_dir + "/necro_%s.png" % k)
	print("stills done")
	quit()
