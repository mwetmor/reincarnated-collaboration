extends SceneTree
# C-5 Packet 87: stand west of the pack, cycle the VFX picker KIT_CYCLES times, face east, cast at the nearest dummy; capture EVERY frame at the exact 1920x1080 camera for ~2.5 s.
var out_dir = OS.get_environment("PROBE_OUT")
var cycles = int(OS.get_environment("KIT_CYCLES"))
func _initialize():
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_VIEWPORT
	root.content_scale_size = Vector2i(1920, 1080)
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	keeper.global_position = Vector2(3760, 640)
	for i in cycles:
		Input.action_press("vfx_cycle"); await physics_frame; Input.action_release("vfx_cycle"); await physics_frame; await physics_frame
	Input.action_press("move_right"); await physics_frame; await physics_frame; Input.action_release("move_right")
	for f in 12: await physics_frame
	var n = 0
	for f in 10:
		await physics_frame
		root.get_texture().get_image().save_png(out_dir + "/cast_%04d.png" % n); n += 1
	Input.action_press("cast"); await physics_frame; Input.action_release("cast")
	for f in 150:
		await physics_frame
		root.get_texture().get_image().save_png(out_dir + "/cast_%04d.png" % n); n += 1
	var label = scene.find_child("Label", true, false)
	print("frames ", n, " feet ", keeper.global_position, " label ", label.text if label else "none")
	quit()
