extends SceneTree
# C-5 Packet 85: stand west of the pack, face east, cast the first kit at the nearest dummy; capture every 2nd frame for 3 s (~90 frames at 60 Hz).
var out_dir = OS.get_environment("PROBE_OUT")
func _initialize():
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	keeper.global_position = Vector2(3760, 640)
	Input.action_press("move_right"); await physics_frame; await physics_frame; Input.action_release("move_right")
	for f in 12: await physics_frame
	var n = 0
	for f in 15:
		await physics_frame
		if f % 2 == 0: root.get_texture().get_image().save_png(out_dir + "/cast_%04d.png" % n); n += 1
	Input.action_press("cast"); await physics_frame; Input.action_release("cast")
	for f in 165:
		await physics_frame
		if f % 2 == 0: root.get_texture().get_image().save_png(out_dir + "/cast_%04d.png" % n); n += 1
	print("frames ", n, " feet ", keeper.global_position)
	quit()
