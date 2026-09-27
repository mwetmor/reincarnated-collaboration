extends SceneTree
# C-9 probe R-C9-34: record the E-facing knight four times over -- GROK walk, RIG walk,
# GROK idle, RIG idle -- from the SAME spot with the same camera, so the two can be
# compared without the background moving underneath the comparison.
#
# MUST run with a real window (Godot cannot rasterise under --headless) AND with
# --fixed-fps, which pins every frame's delta regardless of how long the readback and
# the JPG encode take.  Without it the capture is real-time-coupled: the animations
# advance by the wall-clock cost of saving a frame, and the movie plays back at the
# wrong speed while every individual frame looks correct.
#
#   Godot --path . --resolution 1920x1080 --fixed-fps 30 --script tools/record_rig_ab.gd
#   REC_OUT      frame directory
#   REC_FPS      must match --fixed-fps (default 30)
#   REC_WALK     seconds per walk leg (default 3.5)
#   REC_IDLE     seconds per idle leg (default 3.0)
#   REC_POS      "x,y" start (default 2450,2100 -- verified DRIFT 0.00 px by
#                tools/loop_dryrun.gd, so the walk stays on open ground)

var _label: Label


func _initialize():
	var out := OS.get_environment("REC_OUT")
	var fps := 30
	if OS.get_environment("REC_FPS") != "":
		fps = int(OS.get_environment("REC_FPS"))
	var walk_s := 3.5
	if OS.get_environment("REC_WALK") != "":
		walk_s = float(OS.get_environment("REC_WALK"))
	var idle_s := 3.0
	if OS.get_environment("REC_IDLE") != "":
		idle_s = float(OS.get_environment("REC_IDLE"))
	var pos := Vector2(2450, 2100)
	if OS.get_environment("REC_POS") != "":
		var xy := OS.get_environment("REC_POS").split(",")
		pos = Vector2(float(xy[0]), float(xy[1]))

	DirAccess.make_dir_recursive_absolute(out)
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	var knight = keeper.get_node(^"KnightSprite")
	_build_label(scene)

	var wf := int(round(walk_s * fps))
	var idf := int(round(idle_s * fps))
	print("record_rig_ab: style %s   %d fps   move %d frames   idle %d frames   total %d"
		% [scene.style_name(), fps, wf, idf, 4 * wf + 2 * idf])

	var n := 0
	# Matt's full comparison: the same spot, four times over, walk then run.
	for leg in [["GROK", "walk", wf], ["RIG", "walk", wf],
				["GROK", "run", wf], ["RIG", "run", wf],
				["GROK", "idle", idf], ["RIG", "idle", idf]]:
		_set_mode(scene, knight, String(leg[0]))
		keeper.velocity = Vector2.ZERO
		keeper.global_position = pos
		await physics_frame
		_label.text = "  E-facing knight   —   %s   —   %s" % [leg[0], String(leg[1]).to_upper()]
		# settle, uncaptured, so the first saved frame is not a half-built one
		for i in 6:
			await process_frame
		var moving: bool = String(leg[1]) != "idle"
		if moving:
			Input.action_press("move_right")
		if String(leg[1]) == "run":
			Input.action_press("run_modifier")
		for f in int(leg[2]):
			await process_frame
			await RenderingServer.frame_post_draw
			var img: Image = root.get_texture().get_image()
			if img.get_width() != 1920 or img.get_height() != 1080:
				img.resize(1920, 1080, Image.INTERPOLATE_LANCZOS)
			img.save_jpg(out + "/f_%04d.jpg" % n, 0.92)
			n += 1
		if String(leg[1]) == "run":
			Input.action_release("run_modifier")
		if moving:
			Input.action_release("move_right")
		await physics_frame
		print("  %-4s %-4s -> facing %s   knight cell %s   rig %s   at %s"
			% [leg[0], leg[1], keeper.facing, knight.animation,
			   str(knight.call("rig_showing")), str(keeper.global_position)])

	print("record_rig_ab: %d frames -> %s" % [n, out])
	quit()


func _set_mode(scene, knight, want: String) -> void:
	# scene.rig_mode() is the authority; flip until it agrees rather than assuming a
	# starting state.  Two toggles is the cap: a third would mean the toggle is inert,
	# and recording ten seconds of the wrong mode with the right caption is worse than
	# stopping.
	for i in 3:
		if String(scene.rig_mode()) == want:
			return
		scene.toggle_rig()
	push_error("record_rig_ab: cannot reach mode %s (stuck at %s)" % [want, scene.rig_mode()])


func _build_label(scene) -> void:
	var canvas := CanvasLayer.new()
	canvas.layer = 200
	scene.add_child(canvas)
	var panel := ColorRect.new()
	panel.color = Color(0, 0, 0, 0.55)
	panel.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	panel.offset_bottom = 62.0
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	canvas.add_child(panel)
	_label = Label.new()
	_label.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	_label.offset_top = 12.0
	_label.add_theme_font_size_override("font_size", 34)
	_label.add_theme_color_override("font_color", Color(1, 0.96, 0.86))
	_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	canvas.add_child(_label)
