extends SceneTree
## C-9 R-C9-139 -- WHAT THE CHARACTER LIGHT COSTS: the painted Barrow, vsync off and uncapped, the character walking the
## frame-cost loop (barrow_full._frame_cost_mode's four waypoints) in view, EVERY frame's wall time recorded. Run once per
## light (current = the control), alternating, under the phone's renderer. drax.
##   Godot --path godot --resolution 2532x1170 --rendering-method gl_compatibility --rendering-driver opengl3_angle \
##         --script tools/perf_charlight.gd -- --as-web --c <who> [--charlight a|b|c] --out FILE.json [--frames 900]

func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var out_file := String(args[args.find("--out") + 1])
	var n := int(args[args.find("--frames") + 1]) if args.has("--frames") else 900
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	Engine.max_fps = 0
	var scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)
	while not scene.ready_done:
		await process_frame
	var v = scene.get("veil")
	while v != null and not v.stage_done():
		await process_frame
	var k = scene.knight
	k.set_physics_process(false)
	scene.place_knight(0.0, -3.0, "N")
	var loop := [Vector2(4.0, 1.0), Vector2(0.0, 5.0), Vector2(-4.0, 1.0), Vector2(0.0, -3.0)]
	var wi := 0
	var dt := 1.0 / 60.0
	for i in 180:
		k.drive_dir(scene.canvas_dir_uv(scene.knight_uv(), loop[wi]), false, dt)
		await process_frame
	var times := PackedFloat64Array()
	var t_prev := Time.get_ticks_usec()
	for i in n:
		if scene.knight_uv().distance_to(loop[wi]) < 0.6:
			wi = (wi + 1) % loop.size()
		k.drive_dir(scene.canvas_dir_uv(scene.knight_uv(), loop[wi]), false, dt)
		await process_frame
		var t := Time.get_ticks_usec()
		times.append(float(t - t_prev) / 1000.0)
		t_prev = t
	var s := Array(times)
	s.sort()
	var total := 0.0
	for x in s:
		total += float(x)
	var rep := {"who": scene.who, "charlight": scene.charlight, "frames": n, "mean_ms": total / n,
		"p50_ms": s[int(n * 0.5)], "p99_ms": s[int(n * 0.99)], "max_ms": s[n - 1], "over_20ms": s.filter(func(x): return x > 20.0).size(),
		"render": [root.get_texture().get_width(), root.get_texture().get_height()],
		"renderer": RenderingServer.get_current_rendering_method()}
	var f := FileAccess.open(out_file, FileAccess.WRITE)
	f.store_string(JSON.stringify(rep, " "))
	f.close()
	print("[perf_charlight] ", JSON.stringify(rep))
	quit(0)
