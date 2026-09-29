extends SceneTree
# Does the armed wiring exist, and does every new input actually reach the pose?
const DT := 1.0 / 24.0
func _initialize():
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60: await process_frame
	Engine.physics_ticks_per_second = 24
	var k = scene.knight
	k.set_physics_process(false)
	var tree: AnimationTree = k._tree
	var bt: AnimationNodeBlendTree = tree.tree_root
	print("== GRAPH ==")
	var names := []
	for n in bt.get_node_list(): names.append(String(n))
	names.sort()
	print("   nodes: ", str(names))
	print("   strikes: ", str(k._strikes))
	print("== UNARMED (stack %d) ==  armed=%s" % [k.gear_stack, k.armed()])
	print("   idle '%s' walk '%s' run '%s'  walk_px_s %.1f  run_px_s %.1f  layer '%s'" %
		[k._roles.get("idle",""), k._roles.get("walk",""), k._roles.get("run",""),
		 k.walk_px_s(), k.run_px_s(), k._layer_spec().get("action","")])
	print("   chop fires when unarmed? ", k.try_strike("chop"), "   bash? ", k.try_strike("bash"))
	k.set_block(true); print("   block engages when unarmed? ", k.blocking()); k.set_block(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	for i in 4: 
		k.drive_dir(Vector2.ZERO, false, DT); await physics_frame
	print("== ARMED (stack %d) ==  armed=%s" % [k.gear_stack, k.armed()])
	print("   idle '%s' walk '%s' run '%s'  walk_px_s %.1f  run_px_s %.1f  layer '%s'" %
		[k._roles.get("idle",""), k._roles.get("walk",""), k._roles.get("run",""),
		 k.walk_px_s(), k.run_px_s(), k._layer_spec().get("action","")])
	print("   loop modes: idle=%d walk=%d run=%d (1 = LOOP_LINEAR)" %
		[k._anim.get_animation(k._roles["idle"]).loop_mode,
		 k._anim.get_animation(k._roles["walk"]).loop_mode,
		 k._anim.get_animation(k._roles["run"]).loop_mode])
	print("== PARAMETERS PRESENT ==")
	var live := {}
	for pl in tree.get_property_list(): live[String(pl["name"])] = true
	for want in ["parameters/bl_iw/blend_amount", "parameters/bl_wr/blend_amount",
				 "parameters/ts_walk/scale", "parameters/ts_run/scale",
				 "parameters/seek_run/seek_request", "parameters/blend/blend_amount",
				 "parameters/blk/blend_amount", "parameters/os_slash/request",
				 "parameters/os_chop/request", "parameters/os_bash/request"]:
		print("   %-38s %s" % [want, "OK" if live.has(want) else "*** MISSING ***"])
	print("== EACH INPUT REACHES THE POSE ==")
	for which in ["slash", "chop", "bash"]:
		var p0 := _pose(k._skel)
		var ok: bool = k.try_strike(which)
		var moved := 0.0
		for i in 10:
			k.drive_dir(Vector2.ZERO, false, DT); await physics_frame
			moved = maxf(moved, _diff(p0, _pose(k._skel)))
		print("   %-6s fired=%s  active=%s  largest bone move %.4f m" %
			[which, ok, k.attacking(), moved])
		while k.attacking():
			k.drive_dir(Vector2.ZERO, false, DT); await physics_frame
	var pb := _pose(k._skel)
	k.set_block(true)
	var frames := 0
	var settle := -1
	for i in 20:
		k.drive_dir(Vector2.ZERO, false, DT); await physics_frame
		frames += 1
		if settle < 0 and k._block_w >= 0.999: settle = frames
	print("   block  weight %.3f after %d frames, reached 1.0 at frame %s = %.3f s, bone move %.4f m" %
		[k._block_w, frames, str(settle), float(settle) * DT, _diff(pb, _pose(k._skel))])
	k.set_block(false)
	quit(0)

func _pose(skel: Skeleton3D) -> Array:
	var o := []
	for b in skel.get_bone_count():
		o.append(skel.global_transform * skel.get_bone_global_pose(b).origin)
	return o
func _diff(a: Array, b: Array) -> float:
	var d := 0.0
	for i in a.size(): d = maxf(d, (a[i] - b[i]).length())
	return d
