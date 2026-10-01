extends SceneTree
## C-9 MIX v3 -- THE CRATER AND THE WARP, in stills at the play camera. drax.
##   Godot --path godot --resolution 1920x1080 --fixed-fps 60 --script tools/probe_crater.gd -- --as-web --c sorceress --out DIR [--casts N]
## She casts the Meteor (the default, MIX v3) N times (default 1), a little apart; stills at fixed times from each
## impact (the warp's frames round it, the burst, the crater cooling, the cooled crater) and the impact's screen
## point, to DIR/crater_frames.json.
var AT := [-0.10, -0.05, -0.0167, 0.0, 0.05, 0.12, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0]
var out_dir := ""


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	out_dir = String(args[args.find("--out") + 1])
	if args.has("--at-list"):
		AT = Array(String(args[args.find("--at-list") + 1]).split(",")).map(func(x): return float(x))
	var casts := 1
	if args.has("--casts"):
		casts = int(args[args.find("--casts") + 1])
	DirAccess.make_dir_recursive_absolute(out_dir)
	var scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)
	while not scene.ready_done:
		await process_frame
	var v = scene.get("veil")
	while v != null and not v.stage_done():
		await process_frame
	scene.set_hud_visible(false)
	for c in scene.get_children():
		if c is CanvasLayer:
			(c as CanvasLayer).visible = false
	var mfx = scene.meteor_fx
	var cr = mfx.crater if mfx.crater != null else mfx.get("crater4")     # MIX v3's crater or v4's
	while not mfx.warmed or (cr != null and not cr.warmed):
		await process_frame
	var rows := []
	var spots := [[-1.0, -0.5, "E"], [-1.6, 0.6, "E"], [0.2, 1.2, "N"], [-0.4, -1.6, "S"], [0.8, -0.2, "W"]]
	for n in casts:
		var sp: Array = spots[n % spots.size()]
		scene.place_knight(float(sp[0]), float(sp[1]), String(sp[2]))
		for f in 30:
			await physics_frame
		scene.knight.try_strike("chop")
		var sl: Dictionary = {}
		while sl.is_empty():
			await process_frame
			for s in mfx.pool:
				if bool(s.get("active", false)):
					sl = s
		var k := 0
		var t_imp: float = mfx.T_IMPACT
		var tg: Vector3 = sl["target"]
		var t := -9.0
		var after := -1                     # frames since the impact (fixed fps 60): the slot ends at 3 s, the crater lives on
		while k < AT.size():
			await RenderingServer.frame_post_draw
			if after < 0:
				t = float(sl["t"]) - t_imp
				if t >= 0.0:
					after = 0
			else:
				after += 1
				t = maxf(t, 0.0) + 1.0 / 60.0 if after > 0 else t
			if t + 1e-4 >= float(AT[k]):
				var img := root.get_texture().get_image()
				var name := "c%d_%02d.png" % [n, k]
				img.save_png(out_dir.path_join(name))
				var sp2: Vector2 = scene.cam.unproject_position(tg)
				rows.append({"cast": n, "file": name, "t": t, "at": AT[k], "target_px": [sp2.x, sp2.y],
					"r_px": (scene.cam.unproject_position(tg + scene.cam.global_transform.basis.x.normalized() * mfx.MIX3_CRATER_R) - sp2).length(),
					"craters_live": cr.live_count() if cr != null else 0,
					"crater_start": cr.report.get("last_start", {}) if cr != null else {}})
				k += 1
			await process_frame
	var f2 := FileAccess.open(out_dir.path_join("crater_frames.json"), FileAccess.WRITE)
	f2.store_string(JSON.stringify({"frames": rows, "mode": "mix4" if mfx.get("mix4") else ("mix3" if mfx.mix3 else "other"),
		"crater_report": cr.report if cr != null else {}}, " "))
	f2.close()
	if cr != null:
		for sl in cr.slots:
			print("[crater] slot live=%s visible=%s at=%s age=%.2f" % [sl["live"], (sl["mi"] as MeshInstance3D).visible, (sl["mi"] as MeshInstance3D).global_position, float(sl["age"])])
	print("[crater] %d stills -> %s" % [rows.size(), out_dir])
	quit(0)
