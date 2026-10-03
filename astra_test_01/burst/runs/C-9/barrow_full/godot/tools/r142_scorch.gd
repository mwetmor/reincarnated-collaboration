extends SceneTree
## C-9 R-C9-142 -- THE METEOR'S SCORCH ON WHAT STANDS NEAR IT: stills and its cost. drax.
##   STILLS  Godot --path godot --rendering-method gl_compatibility --rendering-driver opengl3_angle --resolution 1280x720 \
##             --script tools/r142_scorch.gd -- --as-web --c sorceress --v5 b --stills OUTDIR
##           a Meteor next to a standing stone (ring_p155), between birches (G1), on the tarn ice; each shot at the impact
##           (+0.12 s, the glow and the shake), +1.6 s (the char held) and +4.5 s (fading): PNGs, the play camera's own angle
##   PERF    ... --resolution 844x390 --disable-vsync --max-fps 0 --script tools/r142_scorch.gd -- --as-web --c sorceress --v5 b \
##             --perf FILE.json
##           4 Meteors in a row (1.2 s apart) by the stone, the cairn and the birches; ABBA blocks, scorch ON vs the matched
##           control (the same 4 casts with the scorch detached: meteor_fx.scorch = null); every frame's own time
var scene
var mfx
var args: PackedStringArray


func _arg(k: String) -> String:
	var i := args.find(k)
	return String(args[i + 1]) if i >= 0 and i + 1 < args.size() else ""


func _initialize() -> void:
	args = OS.get_cmdline_user_args()
	scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)
	_run.call_deferred()


func _frames(n: int) -> void:
	for i in n:
		await process_frame


func _wait_s(s: float) -> void:
	var t0 := Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < int(s * 1000.0):
		await process_frame


func _spot_near(id: String, extra: float) -> Vector3:
	"""A ground point on the CAMERA's side of a piece, `extra` m out from its bounds."""
	var n: Node3D = scene.nodes[id]
	var wb: AABB = n.global_transform * scene._node_aabb(n)
	var c := wb.get_center()
	var back: Vector3 = scene.cam.global_transform.basis.z
	var d := Vector3(back.x, 0.0, back.z).normalized()
	var r := 0.5 * Vector2(wb.size.x, wb.size.z).length()
	var p := c + d * (r * 0.6 + extra)
	p.y = 0.0
	return p


func _between(a: String, b: String) -> Vector3:
	var pa: Vector3 = (scene.nodes[a] as Node3D).global_position
	var pb: Vector3 = (scene.nodes[b] as Node3D).global_position
	var p := (pa + pb) * 0.5
	p.y = 0.0
	return p


func _ice_spot() -> Vector3:
	var best := Vector3.INF
	var n_ice := 0
	var sum := Vector3.ZERO
	for x in range(-40, 41):
		for z in range(-40, 41):
			var p := Vector3(float(x), 0.0, float(z))
			if String(scene.ground_class(p)) == "ice":
				n_ice += 1
				sum += p
	if n_ice > 0:
		best = sum / float(n_ice)
		if String(scene.ground_class(best)) != "ice":
			for x in range(-40, 41):
				for z in range(-40, 41):
					var p2 := Vector3(float(x), 0.0, float(z))
					if String(scene.ground_class(p2)) == "ice" and (best == Vector3.INF or p2.distance_to(sum / float(n_ice)) < 3.0):
						return p2
	return best


func _cast_wait_impact(target: Vector3) -> void:
	var n0: int = (mfx.report["impacts"] as Array).size()
	mfx.cast(target)
	while (mfx.report["impacts"] as Array).size() == n0:
		await process_frame


func _run() -> void:
	while not bool(scene.ready_done):
		await process_frame
	var v = scene.get("veil")
	while v != null and not v.stage_done():
		await process_frame
	mfx = scene.meteor_fx
	while mfx == null or not bool(mfx.warmed):
		await process_frame
		mfx = scene.meteor_fx
	scene.set_hud_visible(false)
	for c in scene.get_children():
		if c is CanvasLayer:
			(c as CanvasLayer).visible = false
	await _frames(30)
	var out := {"renderer": RenderingServer.get_current_rendering_method(), "size": [root.size.x, root.size.y],
		"v5_word": String(mfx.report.get("v5_word", "")), "scorch": mfx.scorch.report if mfx.scorch != null else {}}
	if args.has("--stills"):
		await _stills(_arg("--stills"), out)
	elif args.has("--perf"):
		await _perf(_arg("--perf"), out)
	quit(0)


func _shot(path: String) -> void:
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(path)


func _stills(dir: String, out: Dictionary) -> void:
	DirAccess.make_dir_recursive_absolute(dir)
	scene.place_knight(-14.0, -16.0, "E")         # out of the shots
	var shots := {"stone": _spot_near("ring_p155", 0.9), "birches": _between("G1_birch_1", "G1_birch_2"), "ice": _ice_spot()}
	out["shots"] = {}
	for k in ["stone", "birches", "ice"]:
		var p: Vector3 = shots[k]
		if p == Vector3.INF:
			out["shots"][k] = {"error": "no ice found"}
			continue
		p.y = 0.0
		scene.park_camera(p, 2.0)
		await _frames(20)
		var rec := {"target": [snappedf(p.x, 0.01), snappedf(p.z, 0.01)], "ground": String(scene.ground_class(p))}
		await _cast_wait_impact(p)
		var t_imp := Time.get_ticks_msec()
		await _wait_s(0.12)
		await _shot("%s/r142_%s_a_impact.png" % [dir, k])
		await _wait_s(1.6 - float(Time.get_ticks_msec() - t_imp) / 1000.0)
		await _shot("%s/r142_%s_b_char.png" % [dir, k])
		await _wait_s(4.5 - float(Time.get_ticks_msec() - t_imp) / 1000.0)
		await _shot("%s/r142_%s_c_fading.png" % [dir, k])
		rec["scorch_hit"] = mfx.scorch.report.get("last_hit", {}) if mfx.scorch != null else {}
		rec["crater"] = mfx.crater4.report.get("last_start", {}) if mfx.crater4 != null else {}
		out["shots"][k] = rec
		await _wait_s(8.0)
	var f := FileAccess.open(dir + "/r142_stills.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " "))
	f.close()
	print("[r142] stills ", JSON.stringify(out["shots"]))


func _perf(path: String, out: Dictionary) -> void:
	scene.place_knight(-14.0, -16.0, "E")
	var spots := [_spot_near("ring_p155", 0.8), _spot_near("cairn_1", 0.6), _between("G1_birch_1", "G1_birch_2"),
		_between("G1_birch_4", "G1_birch_5")]
	var centre := Vector3.ZERO
	for s in spots:
		centre += s
	centre /= 4.0
	scene.park_camera(centre, 1.0)
	await _frames(120)
	var sz = mfx.scorch
	# --cold: ONE block, the process's first 4 casts (the cold first use), as configured (?scorch=0 is the control)
	var order := [sz != null] if args.has("--cold") else ["prime", true, false, false, true, true, false, false, true]
	var blocks: Array = []
	for on_v in order:
		var prime := typeof(on_v) == TYPE_STRING
		var on: bool = true if prime else bool(on_v)
		mfx.scorch = sz if on else null
		var dts: Array = []
		var at_s: Array = []
		var last := Time.get_ticks_usec()
		var t0 := last
		var next_cast := 0
		var hits: Array = []
		while Time.get_ticks_usec() - t0 < 11_000_000:
			var el := float(Time.get_ticks_usec() - t0) / 1e6
			if next_cast < 4 and el >= 1.2 * float(next_cast):
				mfx.cast(spots[next_cast])
				next_cast += 1
			await process_frame
			var now := Time.get_ticks_usec()
			dts.append(float(now - last) / 1000.0)
			at_s.append(float(now - t0) / 1e6)
			last = now
		var worst: Array = []
		for j in dts.size():
			if float(dts[j]) > 16.0:
				worst.append([snappedf(float(at_s[j]), 0.001), snappedf(float(dts[j]), 0.01)])
		if prime:
			blocks.append({"prime": true, "max_ms": dts.max(), "frames_over_16": worst})
			await _wait_s(7.0)
			continue
		if on and sz != null:
			hits = sz.hits.slice(-4)
		var s2 := dts.duplicate()
		s2.sort()
		var mean := 0.0
		for d in dts:
			mean += d
		mean /= dts.size()
		blocks.append({"scorch": on, "frames": dts.size(), "mean_ms": mean, "p95_ms": s2[int(s2.size() * 0.95)],
			"max_ms": s2.back(), "over_20ms": dts.filter(func(x): return x > 20.0).size(), "frames_over_16": worst,
			"objects_hit": hits.map(func(h): return (h["objects"] as Array).map(func(o): return o["id"]))})
		await _wait_s(2.0)
	mfx.scorch = sz
	var agg := func(on: bool, k: String, red: String) -> float:
		var v := 0.0
		var n := 0
		for b in blocks:
			if not b.has("prime") and bool(b["scorch"]) == on:
				v = maxf(v, float(b[k])) if red == "max" else v + float(b[k])
				n += 1
		return v if red == "max" else v / maxf(n, 1)
	out["spots"] = spots.map(func(p): return [snappedf(p.x, 0.01), snappedf(p.z, 0.01)])
	out["blocks"] = blocks
	out["mean_on_ms"] = agg.call(true, "mean_ms", "mean")
	out["mean_off_ms"] = agg.call(false, "mean_ms", "mean")
	out["delta_ms"] = float(out["mean_on_ms"]) - float(out["mean_off_ms"])
	out["max_on_ms"] = agg.call(true, "max_ms", "max")
	out["max_off_ms"] = agg.call(false, "max_ms", "max")
	out["over_20_on"] = agg.call(true, "over_20ms", "mean")
	out["over_20_off"] = agg.call(false, "over_20ms", "mean")
	var f := FileAccess.open(path, FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " "))
	f.close()
	print("[r142] perf ", JSON.stringify({"on": out["mean_on_ms"], "off": out["mean_off_ms"], "delta": out["delta_ms"],
		"max_on": out["max_on_ms"], "max_off": out["max_off_ms"], "over20_on": out["over_20_on"], "over20_off": out["over_20_off"]}))
