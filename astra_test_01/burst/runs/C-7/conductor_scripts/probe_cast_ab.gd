extends SceneTree
# C-7 A/B capture probe (conductor capture tool, not production code): like probe_cast_dir.gd but CASTS casts spaced CAST_GAP_FRAMES apart,
# capturing every 2nd frame for CAPTURE_FRAMES after the first cast (default 3 casts, 270-frame gap = 4.5 s, 1020 frames = 17 s).
var out_dir = OS.get_environment("PROBE_OUT")
var cycles = int(OS.get_environment("KIT_CYCLES"))
var sx = float(OS.get_environment("START_X")); var sy = float(OS.get_environment("START_Y"))
var faces = OS.get_environment("FACE").split(",")
var casts = int(OS.get_environment("CASTS")) if OS.get_environment("CASTS") != "" else 3
var gap = int(OS.get_environment("CAST_GAP_FRAMES")) if OS.get_environment("CAST_GAP_FRAMES") != "" else 270
var total = int(OS.get_environment("CAPTURE_FRAMES")) if OS.get_environment("CAPTURE_FRAMES") != "" else 1020
func _init():
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_VIEWPORT
	root.content_scale_size = Vector2i(1920, 1080)
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	keeper.global_position = Vector2(sx, sy)
	keeper.vfx_force_touch_device = true
	for i in cycles:
		Input.action_press("vfx_cycle"); await physics_frame; Input.action_release("vfx_cycle"); await physics_frame; await physics_frame
	for a in faces: Input.action_press(a)
	await physics_frame; await physics_frame
	for a in faces: Input.action_release(a)
	for f in 12: await physics_frame
	var n = 0
	for f in 6:
		await physics_frame
		if f % 2 == 0:
			root.get_texture().get_image().save_png(out_dir + "/cast_%04d.png" % n); n += 1
	var done = 0
	for f in total:
		if f % gap == 0 and done < casts:
			Input.action_press("cast"); await physics_frame; Input.action_release("cast"); done += 1
		await physics_frame
		if f % 2 == 0:
			root.get_texture().get_image().save_png(out_dir + "/cast_%04d.png" % n); n += 1
	var label = scene.find_child("Label", true, false)
	print("frames ", n, " casts ", done, " feet ", keeper.global_position, " facing ", keeper.facing, " label ", label.text if label else "none")
	quit()
