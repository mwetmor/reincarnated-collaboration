extends SceneTree
## BV2F lane PT (R-C9-199): THE PILOT'S FRAME SPLIT at a view -- PH's P10 loop (fid/ph/harness/godot/ph_life.gd _perf:
## vsync off, uncapped, him walking a 4-point loop round the view) with Godot's own monitors per frame (process, physics,
## render CPU/GPU of the root viewport, draw calls, primitives), then an ABLATION: each component switched off alone for
## the same frames, so its cost is the difference. Read-only on the level (toggles are restored); writes only --out.
##   BV2F_VARIANT=art Godot --path godot --resolution 1920x1080 --script res://tools/bv2f/pt_perf_split.gd -- --out DIR [--view u,v] [--frames N]

var out_dir := ""
var view := Vector2(0.0, 0.0)
var frames := 600
var scene
var k
var loop := []
var wi := 0


func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	for i in a.size():
		if a[i] == "--out" and i + 1 < a.size():
			out_dir = a[i + 1]
		if a[i] == "--view" and i + 1 < a.size():
			var p := a[i + 1].split(",")
			view = Vector2(float(p[0]), float(p[1]))
		if a[i] == "--frames" and i + 1 < a.size():
			frames = int(a[i + 1])
	DirAccess.make_dir_recursive_absolute(out_dir)
	scene = load("res://scenes/bv2f_pilot_painted.tscn").instantiate()
	root.add_child(scene)
	var w := 0
	while not scene.ready_done and w < 3000:
		await process_frame
		w += 1
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	Engine.max_fps = 0
	RenderingServer.viewport_set_measure_render_time(root.get_viewport_rid(), true)
	k = scene.knight
	k.set_physics_process(false)
	loop = [view + Vector2(4.0, 1.0), view + Vector2(0.0, 5.0), view + Vector2(-4.0, 1.0), view + Vector2(0.0, -3.0)]
	scene.place_knight(loop[3].x, loop[3].y, "N")
	for i in 180:
		_step()
		await process_frame
	var rep := {"view_uv": [view.x, view.y], "frames": frames, "configs": {}}
	var configs := ["base", "no_water", "no_floes", "no_heather", "no_snow_field", "no_snowfall", "no_sun_shadows",
		"no_paint_sun_shadows", "no_pen", "no_baked_models", "base_again"]
	for c in configs:
		var undo := _apply(c)
		for i in 60:
			_step()
			await process_frame
		rep["configs"][c] = await _measure()
		_undo(undo)
		print("[split] %s %s" % [c, JSON.stringify(rep["configs"][c])])
	var b: Dictionary = rep["configs"]["base"]
	var gains := {}
	for c in configs:
		if c.begins_with("base"):
			continue
		gains[c] = {"mean_ms_saved": snappedf(float(b["mean_ms"]) - float(rep["configs"][c]["mean_ms"]), 0.01),
			"p99_ms_saved": snappedf(float(b["p99_ms"]) - float(rep["configs"][c]["p99_ms"]), 0.01),
			"gpu_ms_saved": snappedf(float(b["gpu_ms"]) - float(rep["configs"][c]["gpu_ms"]), 0.01)}
	rep["saved_vs_base"] = gains
	rep["renderer"] = RenderingServer.get_current_rendering_method()
	rep["adapter"] = RenderingServer.get_video_adapter_name()
	rep["render_px"] = [root.get_texture().get_width(), root.get_texture().get_height()]
	var f := FileAccess.open(out_dir.path_join("perf_split.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(rep, " "))
	f.close()
	quit(0)


func _step() -> void:
	if scene.knight_uv().distance_to(loop[wi]) < 0.6:
		wi = (wi + 1) % loop.size()
	k.drive_dir(scene.canvas_dir_uv(scene.knight_uv(), loop[wi]), false, 1.0 / 60.0)


func _measure() -> Dictionary:
	var vr := root.get_viewport_rid()
	var wall := PackedFloat64Array()
	var cpu := 0.0
	var gpu := 0.0
	var proc := 0.0
	var phys := 0.0
	var dc := 0.0
	var prim := 0.0
	var t_prev := Time.get_ticks_usec()
	for i in frames:
		_step()
		await process_frame
		var t := Time.get_ticks_usec()
		wall.append(float(t - t_prev) / 1000.0)
		t_prev = t
		cpu += RenderingServer.viewport_get_measured_render_time_cpu(vr) + RenderingServer.get_frame_setup_time_cpu()
		gpu += RenderingServer.viewport_get_measured_render_time_gpu(vr)
		proc += Performance.get_monitor(Performance.TIME_PROCESS) * 1000.0
		phys += Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS) * 1000.0
		dc += Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)
		prim += Performance.get_monitor(Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME)
	var s := Array(wall)
	s.sort()
	var tot := 0.0
	for x in s:
		tot += float(x)
	var n := float(frames)
	return {"mean_ms": snappedf(tot / n, 0.01), "p50_ms": snappedf(s[int(n * 0.5)], 0.01), "p99_ms": snappedf(s[int(n * 0.99)], 0.01),
		"render_cpu_ms": snappedf(cpu / n, 0.01), "gpu_ms": snappedf(gpu / n, 0.01), "process_ms": snappedf(proc / n, 0.01),
		"physics_ms": snappedf(phys / n, 0.01), "draw_calls": int(dc / n), "primitives": int(prim / n)}


func _apply(c: String) -> Array:
	var u := []
	match c:
		"no_water":
			for mi in scene._meshes(scene.nodes["ground_sea"]):
				u.append([mi, "visible", mi.visible])
				mi.visible = false
		"no_floes":
			for id in scene.nodes:
				if String(id).begins_with("blobs_shore_ice__"):
					for mi in scene._meshes(scene.nodes[id]):
						u.append([mi, "visible", mi.visible])
						mi.visible = false
		"no_heather":
			for mm in scene._heather_mmi:
				u.append([mm, "visible", mm.visible])
				mm.visible = false
		"no_snow_field":
			if scene.snow != null:
				u.append([scene.snow, "visible", scene.snow.visible])
				scene.snow.visible = false
		"no_snowfall":
			if scene.snowfall != null:
				u.append([scene.snowfall, "visible", scene.snowfall.visible])
				scene.snowfall.visible = false
		"no_sun_shadows":
			u.append([scene.sun, "shadow_enabled", scene.sun.shadow_enabled])
			scene.sun.shadow_enabled = false
		"no_paint_sun_shadows":
			if scene.paint_sun != null:
				u.append([scene.paint_sun, "shadow_enabled", scene.paint_sun.shadow_enabled])
				scene.paint_sun.shadow_enabled = false
		"no_pen":
			u.append([scene.post_q, "visible", scene.post_q.visible])
			scene.post_q.visible = false
		"no_baked_models":
			for id in scene.nodes:
				var nd = scene.nodes[id]
				if nd.has_meta("bv2f_fit"):
					u.append([nd, "visible", nd.visible])
					nd.visible = false
	return u


func _undo(u: Array) -> void:
	for e in u:
		(e[0] as Object).set(e[1], e[2])
