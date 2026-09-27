extends SceneTree
# C-9: capture the SAME camera framing in both registers.  Needs a real window
# (Godot cannot rasterise under --headless), so run it without --headless:
#   Godot --path . --resolution 1920x1080 --script tools/capture_ab.gd
# Output dir comes from the CAP_OUT environment variable.
#
# The Keeper is left at the scene's own start position -- this is the exact frame
# Matt sees the instant the build opens.  B is captured first (the build starts in
# B), then toggle() flips the register with the camera and the player untouched.

func _shot(path: String) -> void:
	for i in 20:
		await process_frame
	await RenderingServer.frame_post_draw
	var img: Image = root.get_texture().get_image()
	if img.get_width() != 1920 or img.get_height() != 1080:
		img.resize(1920, 1080, Image.INTERPOLATE_LANCZOS)
	var err := img.save_png(path)
	print("capture %s  %dx%d  err=%d" % [path, img.get_width(), img.get_height(), err])


func _initialize():
	var out := OS.get_environment("CAP_OUT")
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	print("keeper at ", keeper.global_position, "  style ", scene.style_name())
	await _shot(out + "/C-9_cliffside_B_illuminated.png")
	var swapped: int = scene.toggle()
	print("toggled -> ", scene.style_name(), "  textures swapped ", swapped)
	await _shot(out + "/C-9_cliffside_A_h1.png")
	quit()
