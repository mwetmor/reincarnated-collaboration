extends SceneTree
# C-5 v23 proof: simulate a touch device (vfx_force_touch_device), park the mouse BEHIND the Keeper, cycle to kit 8 (v2), face east, cast — the burst must land forward at the dummies, never behind. Captures every frame at the exact 1920x1080 camera.
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
	keeper.vfx_force_touch_device = true
	Input.warp_mouse(Vector2(200, 1000))  # bottom-left = behind and below (where the CAST button sits)
	for i in cycles:
		Input.action_press("vfx_cycle"); await physics_frame; Input.action_release("vfx_cycle"); await physics_frame; await physics_frame
	Input.action_press("move_right"); await physics_frame; await physics_frame; Input.action_release("move_right")
	for f in 12: await physics_frame
	var n = 0
	for f in 8:
		await physics_frame
		root.get_texture().get_image().save_png(out_dir + "/cast_%04d.png" % n); n += 1
	Input.action_press("cast"); await physics_frame; Input.action_release("cast")
	for f in 150:
		await physics_frame
		root.get_texture().get_image().save_png(out_dir + "/cast_%04d.png" % n); n += 1
	var label = scene.find_child("Label", true, false)
	print("frames ", n, " feet ", keeper.global_position, " facing ", keeper.facing, " label ", label.text if label else "none")
	quit()
