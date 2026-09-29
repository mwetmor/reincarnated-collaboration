extends SceneTree
# Where does each clip put his FEET relative to the rig origin? The origin is where the
# scene stands him, so a clip whose feet are centred a metre away is drawn a metre away
# from his own capsule -- and a blend into or out of it drags him across the ground.
# Raw clips (cache bypassed), rig space, metres at figure scale 1.0.
func _initialize() -> void:
	var ps := ResourceLoader.load("res://models/gear/nb-body.glb", "", ResourceLoader.CACHE_MODE_IGNORE_DEEP) as PackedScene
	var r := ps.instantiate()
	root.add_child(r)
	# the node must be IN the tree before its transform exists -- reading it in
	# _initialize without a frame returned nothing and every clip printed the same row
	await process_frame
	await process_frame
	var sk: Skeleton3D = null
	var ap: AnimationPlayer = null
	for n in r.find_children("*", "", true, false):
		if n is Skeleton3D and sk == null: sk = n
		elif n is AnimationPlayer and ap == null: ap = n
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	ap.active = true
	var s: float = sk.global_transform.basis.get_scale().x
	var lt := sk.find_bone("LeftToeBase")
	var rt := sk.find_bone("RightToeBase")
	var lf := sk.find_bone("LeftFoot")
	var rf := sk.find_bone("RightFoot")
	var hp := sk.find_bone("Hips")
	print("  %-28s %-26s %-26s %s" % ["clip", "FEET midpoint from origin", "HIPS from origin", "feet mid at frame 0"])
	for name in ap.get_animation_list():
		var a := ap.get_animation(name)
		ap.play(name)
		var n := 48
		var fsum := Vector2.ZERO
		var fmax := 0.0
		var hsum := Vector2.ZERO
		var f0 := Vector2.ZERO
		for i in n:
			ap.seek(a.length * float(i) / float(n), true, true)
			var m: Vector3 = (sk.get_bone_global_pose(lf).origin + sk.get_bone_global_pose(rf).origin
							  + sk.get_bone_global_pose(lt).origin + sk.get_bone_global_pose(rt).origin) * 0.25 * s
			var h: Vector3 = sk.get_bone_global_pose(hp).origin * s
			var mf := Vector2(m.x, m.z)
			if i == 0: f0 = mf
			fsum += mf
			fmax = maxf(fmax, mf.length())
			hsum += Vector2(h.x, h.z)
		var fm := fsum / float(n)
		var hm := hsum / float(n)
		print("  %-28s mean %.3f m (%+.3f,%+.3f)   mean %.3f m (%+.3f,%+.3f)   %.3f m" % [name, fm.length(), fm.x, fm.y, hm.length(), hm.x, hm.y, f0.length()])
	quit(0)
