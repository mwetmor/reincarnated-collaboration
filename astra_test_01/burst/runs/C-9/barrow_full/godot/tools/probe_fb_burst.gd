extends SceneTree
## C-9 R-C9-110 -- HER FIRE BALL'S BURST in stills, for the before/after of ?fb=c75. drax.
##   Godot --path godot --resolution 1920x1080 --fixed-fps 60 --script tools/probe_fb_burst.gd -- --as-web --c sorceress --out DIR [--fb c75]
## She casts the Fire Ball (east); a still at each of AT ticks after the burst spawns, and the burst's screen point.
const AT := [0, 2, 4, 6, 8, 10, 12, 16, 20, 26, 34, 44]


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var out_dir := String(args[args.find("--out") + 1])
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
	var fb = scene.spell_fx.fire_ball
	while not fb.warmed:
		await process_frame
	var spot := ["-1.0", "-0.5", "E"]
	if args.has("--spot"):
		spot = String(args[args.find("--spot") + 1]).split(",")
	scene.place_knight(float(spot[0]), float(spot[1]), String(spot[2]))
	for f in 30:
		await physics_frame
	if args.has("--turn"):
		# TURN HER as the film does: a few steps toward the aim (her rig faces where she walks), a beat
		var tv := String(args[args.find("--turn") + 1]).split(",")
		var dv := Vector2(float(tv[0]), float(tv[1])).normalized()
		for f in 8:
			scene.knight.drive_dir(dv, false, 1.0 / 60.0)
			await process_frame
		for f in 18:
			scene.knight.drive_dir(Vector2.ZERO, false, 1.0 / 60.0)
			await process_frame
	scene.knight.try_strike("slash")
	var rows := []
	var k := 0
	var g := -1
	for f in 600:
		await RenderingServer.frame_post_draw
		if g < 0:
			for i in fb.casts.size():
				if not (fb.casts[i] as Dictionary).is_empty():
					g = i
		if g < 0:
			continue
		var c: Dictionary = fb.casts[g]
		if c.is_empty() or not c.has("impact_at"):
			continue
		var b := int(c.get("tick", 0)) - int(fb.impact_tick)
		if k < AT.size() and b >= int(AT[k]):
			var img := root.get_texture().get_image()
			var name := "b_%02d.png" % int(AT[k])
			img.save_png(out_dir.path_join(name))
			var sp: Vector2 = scene.cam.unproject_position(c["impact_at"])
			rows.append({"file": name, "tick_after_spawn": b, "at": AT[k], "impact_px": [sp.x, sp.y]})
			k += 1
		if k >= AT.size():
			break
	var f2 := FileAccess.open(out_dir.path_join("burst_frames.json"), FileAccess.WRITE)
	f2.store_string(JSON.stringify({"frames": rows, "tighten": bool(fb.tighten)}, " "))
	f2.close()
	print("[fb_burst] %d stills tighten=%s -> %s" % [rows.size(), str(fb.tighten), out_dir])
	quit(0)
