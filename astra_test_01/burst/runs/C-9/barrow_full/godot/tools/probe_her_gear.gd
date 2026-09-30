extends SceneTree
## C-9 -- HER GEAR, CHECKED IN THE SCENE: every stack shown, her spell buttons and her strike gated on the
## staff. Godot --path godot --rendering-method gl_compatibility --rendering-driver opengl3_angle
##   --resolution 1280x720 --script tools/probe_her_gear.gd -- --as-web --c sorceress --out DIR
var out_dir := ""
func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var i := args.find("--out")
	out_dir = String(args[i + 1]) if i >= 0 else "user://gear"
	DirAccess.make_dir_recursive_absolute(out_dir)
	var scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)
	var w := 0
	while not scene.ready_done and w < 4000:
		await process_frame
		w += 1
	var k = scene.knight
	scene.place_knight(1.5, -1.5, "S")
	var rows := []
	var start: int = k.gear_stack
	for n in k.gear_stack_count() + 1:
		for f in 40:
			await physics_frame
		var labels := []
		if scene.touch != null:
			for b in scene.touch._buttons:
				labels.append(String(b.get("label", "")))
		var ok: bool = k.try_strike("slash")
		for f in 90:
			await physics_frame
		var img := root.get_texture().get_image()
		img.save_png(out_dir.path_join("stack_%d.png" % k.gear_stack))
		rows.append({"stack": k.gear_stack, "name": String((k.cfg.get("gear_stack_names", []) as Array)[k.gear_stack]), "armed": k.armed(),
			"buttons": labels, "slash_struck": ok})
		for f in 120:
			await physics_frame
		# the GEAR press, as the key and the button send it
		var ev := InputEventAction.new()
		ev.action = "gear_cycle"
		ev.pressed = true
		Input.parse_input_event(ev)
		await process_frame
		var ev2 := InputEventAction.new()
		ev2.action = "gear_cycle"
		ev2.pressed = false
		Input.parse_input_event(ev2)
	print("[her_gear] start=%d %s" % [start, JSON.stringify(rows)])
	var f := FileAccess.open(out_dir.path_join("her_gear.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify({"start_stack": start, "rows": rows, "fire_ball_fired": scene.spell_fx.fire_ball.report.get("fired", []).size()}, " "))
	f.close()
	quit(0)
