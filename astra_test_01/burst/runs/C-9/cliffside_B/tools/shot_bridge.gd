extends SceneTree
# C-9 v3: still captures at the bridge's west landing, for checking the new B
# background placement and the two still figures against the knight.
#   SHOT_OUT   directory      SHOT_POS "x,y" (default the bridge west landing)
#   SHOT_STYLE "B" or "A"     SHOT_FACE  a move action to face before the shot
func _initialize():
	var out := OS.get_environment("SHOT_OUT")
	var pos := Vector2(2700, 1500)
	if OS.get_environment("SHOT_POS") != "":
		var xy := OS.get_environment("SHOT_POS").split(",")
		pos = Vector2(float(xy[0]), float(xy[1]))
	DirAccess.make_dir_recursive_absolute(out)
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	if OS.get_environment("SHOT_STYLE") == "A":
		scene.toggle_rig() if false else scene.toggle()
	keeper.velocity = Vector2.ZERO
	keeper.global_position = pos
	# SHOT_ONLY=<layer>: hide everything except one parallax layer, so its placement can
	# be read off the frame instead of inferred from Parallax2D's scroll maths.
	var only := OS.get_environment("SHOT_ONLY")
	if only != "":
		for n in ["Layer_sky", "Layer_far_ruins", "Layer_forest_valley", "Layer_mist"]:
			var ln = scene.get_node_or_null(NodePath(n))
			if ln != null:
				ln.visible = (n == "Layer_" + only)
		for n in ["Foreground_0", "Foreground_1", "Shadows", "Overhead", "Near_0", "Air", "Actors"]:
			var fn = scene.get_node_or_null(NodePath(n))
			if fn != null and n != "Actors":
				fn.visible = false
			elif fn != null:
				for c in fn.get_children():
					if c is CanvasItem and String(c.name) != "Keeper":
						c.visible = false

	var face := OS.get_environment("SHOT_FACE")
	if face != "":
		Input.action_press(face)
		for i in 12:
			await physics_frame
		Input.action_release(face)
	for i in 12:
		await process_frame
	await RenderingServer.frame_post_draw
	var img: Image = root.get_texture().get_image()
	var nm := OS.get_environment("SHOT_NAME")
	if nm == "":
		nm = "shot"
	img.save_png("%s/%s.png" % [out, nm])
	print("shot: style %s  rig %s  keeper %s  figures %d/%d active -> %s/%s.png"
		% [scene.style_name(), scene.rig_mode(), str(keeper.global_position),
		   scene.active_figure_count(), scene.figure_count(), out, nm])
	quit()
