extends SceneTree
## C-9 R-C9-121: THE EYE GLOW'S COST. The dark knight in the painted Barrow, standing, the play camera; four blocks of
## frames ABBA with his eye nodes (and their per-frame flicker) on and off, plus an A/A control (off, off) so the
## noise floor is on the record beside the delta. vsync off; frame time = the wall-clock between process frames. drax.
##   Godot --path godot --resolution 1920x1080 --rendering-method gl_compatibility --rendering-driver opengl3_angle \
##         --script tools/probe_eye_cost.gd -- --as-web --c warlord --out FILE.json
const N := 600


func _block(eyes, on: bool) -> float:
	for n in eyes.nodes:
		(n as Node3D).visible = on
	eyes.set_process(on)
	for f in 30:
		await process_frame
	var t0 := Time.get_ticks_usec()
	for f in N:
		await process_frame
	return float(Time.get_ticks_usec() - t0) / 1000.0 / N


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var out := String(args[args.find("--out") + 1])
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	var scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)
	while not scene.ready_done:
		await process_frame
	var v = scene.get("veil")
	while v != null and not v.stage_done():
		await process_frame
	for f in 120:
		await process_frame
	var eyes = scene.eyes
	if eyes == null or eyes.nodes.size() != 2:
		push_error("no eye nodes")
		quit(2)
		return
	var on := []
	var off := []
	var aa := []
	for pat in [true, false, false, true, true, false, false, true]:
		var ms: float = await _block(eyes, pat)
		(on if pat else off).append(ms)
	for i in 4:
		aa.append(await _block(eyes, false))
	var mean := func(a: Array) -> float:
		var s := 0.0
		for x in a:
			s += x
		return s / a.size()
	var aa_d: float = mean.call([aa[0], aa[3]]) - mean.call([aa[1], aa[2]])
	var rep := {"renderer": RenderingServer.get_current_rendering_method(), "frames_per_block": N,
		"on_ms": on, "off_ms": off, "delta_ms": mean.call(on) - mean.call(off),
		"aa_off_ms": aa, "aa_delta_ms": aa_d, "eye_nodes": eyes.nodes.size()}
	var f := FileAccess.open(out, FileAccess.WRITE)
	f.store_string(JSON.stringify(rep, " "))
	f.close()
	print("EYE COST delta %.3f ms (A/A %.3f ms) on %s" % [rep["delta_ms"], aa_d, rep["renderer"]])
	quit(0)
