extends SceneTree
## C-9 R-C9-143 (lane EOR2): THE DARK KNIGHT AS THE kc2 EFFECT HAS TO SEE HIM. Per physics frame of one Eye of
## Reckoning channel: the mace head's bearing about his root (unwrapped -> spin direction and rev period), the mace's
## outermost reach and the source's contact band (kc2_player_channel.gd measure_contact_band: the vertices within 0.99
## of the max reach -> mean height, half-extent), his standing height, and the spin clip's track layout. drax.
##   Godot --path godot --headless --script tools/probe_eor2.gd -- --as-web --c warlord --out FILE.json
func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var out := String(args[args.find("--out") + 1])
	var scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)
	while not scene.ready_done:
		await process_frame
	var v = scene.get("veil")
	while v != null and v.has_method("stage_done") and not v.stage_done():
		await process_frame
	var k = scene.knight
	scene.place_knight(0.8, -1.2, "S")
	for f in 40:
		await physics_frame
	var sk: Skeleton3D = k._skel
	var rig: Node3D = k._rig
	var top := sk.find_bone("head_end")
	if top < 0:
		top = sk.find_bone("Head")
	var h: float = (sk.global_transform * sk.get_bone_global_rest(top).origin).y - rig.global_transform.origin.y
	var wb := sk.find_bone("weapon_r")
	var chain := []
	var i := wb
	while i >= 0:
		chain.append(sk.get_bone_name(i))
		i = sk.get_bone_parent(i)
	# the mace's vertices in weapon_r's own space, at bind (whirlwind_channel._weapon_head_local's way)
	var rest := sk.get_bone_global_rest(wb)
	var pieces: Dictionary = (k.get("gear") as Dictionary).get("_pieces", {})
	var pts := PackedVector3Array()
	var piece_names := []
	for nm in pieces:
		if not (pieces[nm] is Array):
			continue
		if not (String(nm).contains("mace") or String(nm).contains("maul") or String(nm).contains("hammer")):
			continue
		piece_names.append(String(nm))
		for mi in (pieces[nm] as Array):
			var m := mi as MeshInstance3D
			if m == null or m.mesh == null:
				continue
			for si in m.mesh.get_surface_count():
				for vv in (m.mesh.surface_get_arrays(si)[Mesh.ARRAY_VERTEX] as PackedVector3Array):
					pts.append(rest.affine_inverse() * (m.transform * vv))
	var anim: AnimationPlayer = k._anim
	var loop_nm := "eor_spin_loop" if anim.has_animation("eor_spin_loop") else "eor_spin"
	var tracks := []
	var lp := anim.get_animation(loop_nm)
	for ti in lp.get_track_count():
		tracks.append([str(lp.track_get_path(ti)), lp.track_get_type(ti)])
	var rows := []
	var ok: bool = k.try_strike("bash")
	var prev_b := 0.0
	var acc := 0.0
	var first := true
	for f in 200:
		await process_frame
		var o: Vector3 = rig.global_transform.origin
		var wx := sk.global_transform * sk.get_bone_global_pose(wb)
		var r_max := 0.0
		var qs := []
		for p in pts:
			var q: Vector3 = wx * p - o
			var r := Vector2(q.x, q.z).length()
			qs.append([r, q.y, q.x, q.z])
			r_max = maxf(r_max, r)
		var n := 0
		var sy := 0.0
		var y_lo := 1e9
		var y_hi := -1e9
		var sx := 0.0
		var sz := 0.0
		for q in qs:
			if float(q[0]) < r_max * 0.99:
				continue
			n += 1
			sy += float(q[1])
			sx += float(q[2])
			sz += float(q[3])
			y_lo = minf(y_lo, float(q[1]))
			y_hi = maxf(y_hi, float(q[1]))
		var b := atan2(sx, sz)
		if first:
			first = false
		else:
			acc += wrapf(b - prev_b, -PI, PI)
		prev_b = b
		rows.append({"t_ms": Time.get_ticks_msec(), "r_max": snappedf(r_max, 1e-4), "band_n": n,
			"band_y": snappedf(sy / maxf(n, 1), 1e-4), "band_half": snappedf(0.5 * (y_hi - y_lo), 1e-4),
			"bearing_acc_deg": snappedf(rad_to_deg(acc), 0.1), "root": [snappedf(o.x, 1e-3), snappedf(o.z, 1e-3)],
			"state": scene.whirl.fx.state_name() if scene.whirl != null else ""})
	var res := {"h_char": h, "weapon_bone_chain": chain, "mace_pieces": piece_names, "mace_verts": pts.size(),
		"anims": anim.get_animation_list(), "loop": loop_nm, "loop_len": lp.length, "loop_tracks": tracks.size(),
		"loop_tracks_head": tracks.slice(0, 8), "skel_path": str(k.get_path_to(sk)), "anim_root": str(anim.root_node),
		"skel_scale": sk.global_transform.basis.get_scale(), "rig_scale": rig.global_transform.basis.get_scale(),
		"press_ok": ok, "rows": rows}
	var fo := FileAccess.open(out, FileAccess.WRITE)
	fo.store_string(JSON.stringify(res, " "))
	fo.close()
	print("[probe_eor2] wrote ", out)
	quit(0)
