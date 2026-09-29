extends SceneTree
# Block1, read off the clip: where is the RAISE, where is the PEAK, what does the TAIL do?
# The shield hand's height and reach over time, rig space, metres, pristine clip.
func _initialize() -> void:
	create_timer(180.0).timeout.connect(func(): push_error("LAB WATCHDOG"); quit(4))
	var ps := ResourceLoader.load("res://models/gear/nb-body.glb", "", ResourceLoader.CACHE_MODE_IGNORE_DEEP) as PackedScene
	var r := ps.instantiate()
	root.add_child(r)
	await process_frame
	await process_frame
	var sk: Skeleton3D = r.find_children("*", "Skeleton3D", true, false)[0]
	var ap: AnimationPlayer = r.find_children("*", "AnimationPlayer", true, false)[0]
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	ap.active = true
	var s: float = sk.global_transform.basis.get_scale().x
	var a := ap.get_animation("block")
	var n := int(round(a.length * 24.0))
	ap.play("block")
	var lh := sk.find_bone("LeftHand")
	var la := sk.find_bone("LeftArm")
	var sp := sk.find_bone("Spine02")
	var rows := []
	for i in n + 1:
		var t: float = a.length * float(i) / float(n)
		ap.seek(t, true, true)
		var h: Vector3 = sk.get_bone_global_pose(lh).origin * s
		var c: Vector3 = sk.get_bone_global_pose(sp).origin * s
		var up_arm: Vector3 = (sk.get_bone_global_pose(lh).origin - sk.get_bone_global_pose(la).origin) * s
		rows.append([t, h.y, Vector2(h.x - c.x, h.z - c.z).length(), h])
	var ymax := -1e9; var imax := 0
	for i in rows.size():
		if float(rows[i][1]) > ymax:
			ymax = float(rows[i][1]); imax = i
	# the raise ends when the hand is within 2 cm of its peak height for the first time
	var iraise := imax
	for i in rows.size():
		if float(rows[i][1]) >= ymax - 0.02:
			iraise = i; break
	print("BLOCK1 %.3f s, %d frames at 24 fps" % [a.length, n])
	print("  shield hand height: start %.3f m, peak %.3f m at t=%.3f s (frame %d); within 2 cm of peak first at t=%.3f s"
		% [float(rows[0][1]), ymax, float(rows[imax][0]), imax, float(rows[iraise][0])])
	var hold_end := imax
	for i in range(imax, rows.size()):
		if float(rows[i][1]) >= ymax - 0.05: hold_end = i
		else: break
	print("  stays within 5 cm of peak until t=%.3f s; end height %.3f m" % [float(rows[hold_end][0]), float(rows[-1][1])])
	var line := ""
	for i in range(0, rows.size(), 3):
		line += "%.2f:%.2f " % [float(rows[i][0]), float(rows[i][1])]
	print("  timeline t:height  " + line)
	print("  start->peak hand travel %.3f m; peak->end %.3f m; start<->end %.3f m"
		% [((rows[imax][3] as Vector3) - (rows[0][3] as Vector3)).length(),
		   ((rows[-1][3] as Vector3) - (rows[imax][3] as Vector3)).length(),
		   ((rows[-1][3] as Vector3) - (rows[0][3] as Vector3)).length()])
	quit(0)
