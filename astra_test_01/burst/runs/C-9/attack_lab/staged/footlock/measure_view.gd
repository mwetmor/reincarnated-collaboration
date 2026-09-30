extends SceneTree
# How much world does a scene show, fullscreen, under the project's stretch settings?
#   Godot --path godot --fullscreen --script tools/measure_view.gd -- --scene res://scenes/X.tscn
# The scene is added to the ROOT window -- a SubViewport would ignore the project's stretch.
# Both scenes use an orthographic camera, KEEP_HEIGHT, cam.size = visible height / PPM.
func _initialize() -> void:
	create_timer(240.0).timeout.connect(func(): push_error("WATCHDOG"); quit(4))
	var path := "res://scenes/cliffside3d.tscn"
	var a := OS.get_cmdline_user_args()
	for i in a.size():
		if a[i] == "--scene" and i + 1 < a.size(): path = a[i + 1]
	var sc = load(path).instantiate()
	root.add_child(sc)
	for i in 90: await process_frame
	var cam: Camera3D = root.get_camera_3d()
	var vis: Vector2 = root.get_visible_rect().size
	var win: Vector2i = DisplayServer.window_get_size()
	var scr: Vector2i = DisplayServer.screen_get_size()
	var aspect: float = vis.x / maxf(vis.y, 1.0)
	var fwd: Vector3 = -cam.global_transform.basis.z
	var pitch: float = asin(clampf(-fwd.y, -1.0, 1.0))
	var h: float = cam.size if cam.keep_aspect == Camera3D.KEEP_HEIGHT else cam.size / aspect
	var w: float = h * aspect
	print("[view] %s | screen %s window %s | stretch mode %s aspect %s | visible (logical) %s | ortho %s, pitch %.2f deg"
		% [path.get_file(), str(scr), str(win), str(ProjectSettings.get_setting("display/window/stretch/mode")),
		   str(ProjectSettings.get_setting("display/window/stretch/aspect")), str(vis), "KEEP_HEIGHT" if cam.keep_aspect == Camera3D.KEEP_HEIGHT else "KEEP_WIDTH", rad_to_deg(pitch)])
	print("[view] %s | visible world %.1f x %.1f m on screen; ground footprint %.1f x %.1f m"
		% [path.get_file(), w, h, w, h / maxf(sin(pitch), 1e-3)])
	quit(0)
