extends SceneTree
## BV2F lane PT (R-C9-201): PH's P10 measurement (fid/ph/harness/godot/ph_life.gd _perf, its loop and its segment:
## 180 lead-in frames of him walking, then 900 measured frames, vsync off, uncapped) with a FULL FRAME TRACE from the
## scene's creation: every frame's wall ms, process / physics ms, draw calls, primitives, his uv, and markers --
## scene_added, warmup (the scene's own report: start/end ms), ready_done, control_start (first frame he is driven),
## measure_start / measure_end. The measured p99 is computed exactly as ph_life does.
##   BV2F_VARIANT=art Godot --path godot --resolution 1920x1080 --script res://tools/bv2f/pt_perf_trace.gd -- --out DIR [--view u,v]

var out_dir := ""
var view := Vector2.ZERO
var scene
var trace := []
var marks := {}
var frame := 0
var t0 := 0
var t_prev := 0


func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	for i in a.size():
		if a[i] == "--out" and i + 1 < a.size():
			out_dir = a[i + 1]
		if a[i] == "--view" and i + 1 < a.size():
			var p := a[i + 1].split(",")
			view = Vector2(float(p[0]), float(p[1]))
	DirAccess.make_dir_recursive_absolute(out_dir)
	t0 = Time.get_ticks_usec()
	t_prev = t0
	scene = load("res://scenes/bv2f_pilot_painted.tscn").instantiate()
	root.add_child(scene)
	marks["scene_added_ms"] = (Time.get_ticks_usec() - t0) / 1000.0
	while not scene.ready_done:
		await _tick("load")
	marks["ready_done_frame"] = frame
	marks["ready_done_ms"] = (Time.get_ticks_usec() - t0) / 1000.0
	marks["warmup"] = scene.report.get("painted", {}).get("pieces", {}).get("warmup", {})
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	Engine.max_fps = 0
	var k = scene.knight
	k.set_physics_process(false)
	var c: Vector2 = view
	var loop := [c + Vector2(4.0, 1.0), c + Vector2(0.0, 5.0), c + Vector2(-4.0, 1.0), c + Vector2(0.0, -3.0)]
	scene.place_knight(loop[3].x, loop[3].y, "N")
	var wi := 0
	var dt := 1.0 / 60.0
	marks["control_start_frame"] = frame + 1
	for i in 180:
		k.drive_dir(scene.canvas_dir_uv(scene.knight_uv(), loop[wi]), false, dt)
		await _tick("leadin")
	marks["measure_start_frame"] = frame + 1
	var times := PackedFloat64Array()
	for i in 900:
		if scene.knight_uv().distance_to(loop[wi]) < 0.6:
			wi = (wi + 1) % loop.size()
		k.drive_dir(scene.canvas_dir_uv(scene.knight_uv(), loop[wi]), false, dt)
		times.append(await _tick("measure"))
	marks["measure_end_frame"] = frame
	var s := Array(times)
	s.sort()
	var n := 900
	var spikes := []
	for e in trace:
		if e["seg"] == "measure" and float(e["ms"]) > 16.7:
			spikes.append(e)
	var rep := {"marks": marks, "measured": {"p50_ms": s[int(n * 0.5)], "p99_ms": s[int(n * 0.99)], "max_ms": s[n - 1],
		"frames_over_16_7": spikes.size()}, "spikes": spikes,
		"render": [root.get_texture().get_width(), root.get_texture().get_height()], "trace": trace}
	var f := FileAccess.open(out_dir.path_join("trace.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(rep))
	f.close()
	print("[trace] " + JSON.stringify({"marks": marks, "measured": rep["measured"]}))
	quit(0)


func _tick(seg: String) -> float:
	await process_frame
	frame += 1
	var t := Time.get_ticks_usec()
	var ms := float(t - t_prev) / 1000.0
	t_prev = t
	var e := {"f": frame, "seg": seg, "ms": snappedf(ms, 0.001), "t_ms": snappedf((t - t0) / 1000.0, 0.1),
		"proc": snappedf(Performance.get_monitor(Performance.TIME_PROCESS) * 1000.0, 0.01),
		"phys": snappedf(Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS) * 1000.0, 0.01),
		"dc": int(Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)),
		"prim": int(Performance.get_monitor(Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME))}
	if scene != null and scene.get("ready_done") and scene.knight != null:
		var uv: Vector2 = scene.knight_uv()
		e["uv"] = [snappedf(uv.x, 0.01), snappedf(uv.y, 0.01)]
	trace.append(e)
	return ms
