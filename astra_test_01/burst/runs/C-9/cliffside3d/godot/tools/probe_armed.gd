extends SceneTree
# Before wiring anything: how long is each new clip, which bones does the guard touch, and
# does mutating AnimationNodeAnimation.animation on a LIVE tree actually re-pose him?
# The last one decides whether an armed/unarmed switch can re-point the existing nodes or
# has to rebuild the tree. `tree.set("parameters/<n>/animation", ...)` silently stores
# nothing -- that is already known -- and this is the OTHER way, which is not the same way.
func _initialize():
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60: await process_frame
	var k = scene.knight
	var ap: AnimationPlayer = k._anim
	var skel: Skeleton3D = k._skel
	print("== CLIP LENGTHS ==")
	for n in ap.get_animation_list():
		var a := ap.get_animation(n)
		print("   %-32s %6.4f s  %3d tracks  loop=%s" % [n, a.length, a.get_track_count(), a.loop_mode])
	print("== GUARD / BLOCK TRACK BONES ==")
	for cn in ["shield_guard_L", "shield_carry_L", "block", "shield_bash", "attack_chop"]:
		if not ap.has_animation(cn): continue
		var a := ap.get_animation(cn)
		var bones := {}
		for i in a.get_track_count():
			bones[String(a.track_get_path(i).get_concatenated_subnames())] = true
		var ks := bones.keys(); ks.sort()
		print("   %-18s %d tracks over %d bones: %s" % [cn, a.get_track_count(), ks.size(),
			str(ks) if ks.size() <= 8 else str(ks.slice(0, 8)) + " ...(%d)" % ks.size()])
	# does a live re-point work?
	print("== LIVE .animation MUTATION ==")
	var tree: AnimationTree = k._tree
	var bt: AnimationNodeBlendTree = tree.tree_root
	var node := bt.get_node("a_idle") as AnimationNodeAnimation
	print("   a_idle currently '%s'" % node.animation)
	k.drive_dir(Vector2.ZERO, false, 1.0 / 24.0)
	await process_frame
	var before := _pose(skel)
	node.animation = "idle_armed"
	for i in 6:
		k.drive_dir(Vector2.ZERO, false, 1.0 / 24.0)
		await process_frame
	var after := _pose(skel)
	var d := 0.0
	for i in before.size(): d = maxf(d, (before[i] - after[i]).length())
	print("   set a_idle.animation = 'idle_armed' -> node reports '%s'" % node.animation)
	print("   largest bone move after 6 frames: %.4f m  => %s" %
		[d, "RE-POSED, live mutation WORKS" if d > 0.01 else "NOTHING MOVED, must rebuild"])
	quit(0)

func _pose(skel: Skeleton3D) -> Array:
	var o := []
	for b in skel.get_bone_count(): o.append(skel.get_bone_global_pose(b).origin)
	return o
