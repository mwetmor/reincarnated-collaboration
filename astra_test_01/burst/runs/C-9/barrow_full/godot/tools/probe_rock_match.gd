extends SceneTree
## C-9 MIX v2 -- B'S DARKENED ROCK AGAINST A'S PAINTED HEAD, measured at the play camera. drax.
##   Godot --path godot --resolution 1920x1080 --script tools/probe_rock_match.gd -- --c sorceress --out DIR
## She casts the Meteor (the default: MIX v2; with -- --meteor mix1, A's painted head for the reference); every frame of the fall a still and the rock's screen point
## (Camera3D.unproject_position of the owner slot's rock), written to DIR/rock_frames.json for
## tools/rock_match.py, which sets the same measure on lane A's baked head frames.
var out_dir := ""
func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var i := args.find("--out")
	out_dir = String(args[i + 1])
	DirAccess.make_dir_recursive_absolute(out_dir)
	var scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)
	var w := 0
	while not scene.ready_done and w < 4000:
		await process_frame
		w += 1
	scene.set_hud_visible(false)
	for c in scene.get_children():
		if c is CanvasLayer:
			(c as CanvasLayer).visible = false
	scene.place_knight(-1.0, -0.5, "E")
	for f in 30:
		await physics_frame
	var k = scene.knight
	k.try_strike("chop")
	var mfx = scene.meteor_fx
	var rows := []
	var n := 0
	for f in 300:
		await RenderingServer.frame_post_draw
		var sl: Dictionary = {}
		for s in mfx.pool:
			if bool(s.get("active", false)):
				sl = s
		# the fall window: B's rock (MIX v2) or A's painted head (?meteor=mix1, its node from rock_at)
		var tt: float = float(sl.get("t", -1.0)) if not sl.is_empty() else -1.0
		if sl.is_empty() or tt < mfx.T_FALL0 or tt >= mfx.T_IMPACT:
			if n > 0:
				break
			continue
		var rp: Vector3
		if mfx.mix2:
			rp = (sl["rock"] as MeshInstance3D).global_position
		else:
			var ra: Dictionary = mfx.proj_a.rock_at(int(sl.get("pa", -1)))
			if ra.is_empty():
				continue
			rp = ra["pos"]
		var sp: Vector2 = scene.cam.unproject_position(rp)
		var img := root.get_texture().get_image()
		var name := "fall_%03d.png" % n
		img.save_png(out_dir.path_join(name))
		var r_px: float = (scene.cam.unproject_position(rp + scene.cam.global_transform.basis.x.normalized() * mfx.ROCK_R) - sp).length()
		rows.append({"file": name, "t": float(sl["t"]), "rock_px": [sp.x, sp.y], "rock_r_px": r_px,
			"vp": [img.get_width(), img.get_height()]})
		n += 1
		await process_frame
	var f2 := FileAccess.open(out_dir.path_join("rock_frames.json"), FileAccess.WRITE)
	f2.store_string(JSON.stringify({"frames": rows, "mode": "mix2" if mfx.mix2 else ("mix1" if mfx.mix else "other")}, " "))
	f2.close()
	print("[rock] %d fall frames -> %s" % [rows.size(), out_dir])
	quit(0)
