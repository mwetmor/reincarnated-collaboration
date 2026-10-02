extends SceneTree
## C-9 R-C9-128: what the WHIRLWIND clip actually does with the hands -- per physics frame of one strike, the hands'
## world positions about the character's root, their bearing (unwrapped), the head height. The 3D clean-room
## whirlwind (reincarnated-godot wwcr_whirlwind.gd) SPUN THE RIG itself at 900 deg/s; here the clip owns the body, so
## the port has to read the sweep off the bones. drax.
##   Godot --path godot ... --script tools/probe_ww_clip.gd -- --as-web --c barbarian --armor gladc --out FILE.json
func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var out := String(args[args.find("--out") + 1])
	var scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)
	while not scene.ready_done:
		await process_frame
	var v = scene.get("veil")
	while v != null and not v.stage_done():
		await process_frame
	var k = scene.knight
	scene.place_knight(-1.0, -0.5, "S")
	k.facing = "S"
	for f in 40:
		await physics_frame
	var sk: Skeleton3D = k._skel
	var names := []
	for i in sk.get_bone_count():
		names.append(sk.get_bone_name(i))
	var want := ["RightHand", "LeftHand", "Head", "Hips", "RightForeArm", "LeftForeArm"]
	var idx := {}
	for w in want:
		for i in names.size():
			if String(names[i]).ends_with(w):
				idx[w] = i
				break
	var rows := []
	var ok: bool = k.try_strike("slash")
	var t := 0.0
	for f in 360:
		await physics_frame
		t += 1.0 / 60.0
		var o: Vector3 = k.global_position
		var row := {"t": snappedf(t, 0.001), "attacking": k.attacking(), "root": [o.x, o.y, o.z]}
		for w in idx:
			var p: Vector3 = sk.global_transform * sk.get_bone_global_pose(idx[w]).origin
			row[w] = [snappedf(p.x - o.x, 0.001), snappedf(p.y - o.y, 0.001), snappedf(p.z - o.z, 0.001)]
		rows.append(row)
		if not k.attacking() and t > 1.0:
			break
	var rep := {"strike_ok": ok, "bones": idx, "clip_len": k._strike_len, "rows": rows, "skel_scale": sk.global_transform.basis.get_scale().x}
	var fa := FileAccess.open(out, FileAccess.WRITE)
	fa.store_string(JSON.stringify(rep))
	fa.close()
	print("[wwclip] ok=%s len=%.3f rows=%d" % [ok, k._strike_len, rows.size()])
	quit(0)
