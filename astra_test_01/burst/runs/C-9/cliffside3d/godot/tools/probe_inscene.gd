extends SceneTree
# C-9 R-C9-69: he renders 218 canvas px where the scale rule predicts 154.4, and he stands
# on one leg. Both are questions about the LIVE rig, not about the file, so ask the rig.
const PPM := 100.617553710938
func _initialize():
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60: await process_frame
	var k = scene.knight
	var skel: Skeleton3D = null
	var anim: AnimationPlayer = null
	for n in k.find_children("*", "", true, false):
		if n is Skeleton3D: skel = n
		elif n is AnimationPlayer: anim = n
	print("figure_scale      %.5f" % k._figure_scale)
	print("rig global scale  %s" % str(k.get_child(1).global_transform.basis.get_scale().snappedf(0.0001)))
	print("skel global scale %s" % str(skel.global_transform.basis.get_scale().snappedf(0.00001)))
	print("current clip      '%s'   playing=%s  pos=%.3f" %
		[k._clip, str(anim.is_playing()), anim.current_animation_position])
	var body_y: float = k.global_position.y
	for b in ["head_end", "Head", "Hips", "LeftToeBase", "RightToeBase"]:
		var i := skel.find_bone(b)
		if i < 0: continue
		var w: Vector3 = skel.global_transform * skel.get_bone_global_pose(i).origin
		print("  %-12s world y %.4f   (%.4f above the body origin)" % [b, w.y, w.y - body_y])
	# what the camera makes of that height
	var he := skel.find_bone("head_end")
	var top: Vector3 = skel.global_transform * skel.get_bone_global_pose(he).origin
	var foot := Vector3(top.x, body_y, top.z)
	var c_top := CliffWorld.canvas_of(top, scene.right, scene.up)
	var c_foot := CliffWorld.canvas_of(foot, scene.right, scene.up)
	print("head_end to feet projects to %.1f canvas px  (rule says 150.2135 x 1.85/1.80 = 154.4)"
		% absf(c_top.y - c_foot.y))
	# and over the idle clip, does a foot leave the ground?
	for clip in ["idle", "walk", "run", "attack"]:
		anim.play(clip)
		var a := anim.get_animation(clip)
		var n := int(round(a.length * 24.0))
		var lo := 1e9
		var hi := -1e9
		var gap := 0.0
		for i in n + 1:
			anim.seek(a.length * float(i) / float(n), true, true)
			await process_frame
			var l: float = (skel.global_transform * skel.get_bone_global_pose(skel.find_bone("LeftToeBase")).origin).y - body_y
			var r: float = (skel.global_transform * skel.get_bone_global_pose(skel.find_bone("RightToeBase")).origin).y - body_y
			lo = minf(lo, minf(l, r))
			hi = maxf(hi, maxf(l, r))
			gap = maxf(gap, absf(l - r))
		print("  %-7s %3d fr: lower foot %.3f..%.3f m above the origin, feet up to %.3f m apart vertically"
			% [clip, n, lo, hi, gap])
	quit(0)
