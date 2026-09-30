extends SceneTree
# LOOP SEAMS: how far each looping clip's last pose is from its first (the wrap), against a
# typical frame-to-frame step inside the clip -- a loop is seamless when the wrap is no bigger.
func _initialize() -> void:
	create_timer(120.0).timeout.connect(func(): push_error("WATCHDOG"); quit(4))
	var k = load("res://scripts/knight.gd").new()
	k.setup(Vector3.RIGHT, Vector3.UP, Vector3.FORWARD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	var skel: Skeleton3D = k._skel
	var ap: AnimationPlayer = k._anim
	(k._tree as AnimationTree).active = false
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var bones := ["Spine02", "Spine01", "Spine", "RightArm", "RightForeArm", "RightHand", "LeftArm", "Hips"]
	for clip in ["idle_armed", "walk_armed", "run_armed", "walk", "run", "idle"]:
		var a := ap.get_animation(clip)
		var n: int = int(round(a.length * 24.0))
		ap.play(clip)
		var poses := []
		for i in n + 1:
			ap.seek(a.length * float(i) / float(n), true, true)
			var p := {}
			for b in bones: p[b] = skel.get_bone_pose_rotation(skel.find_bone(b))
			poses.append(p)
		var line := "[seam] %-11s %.3f s:" % [clip, a.length]
		for b in bones:
			var st := []
			for i in range(1, poses.size()): st.append(rad_to_deg((poses[i - 1][b] as Quaternion).angle_to(poses[i][b])))
			st.sort()
			var wrap: float = rad_to_deg((poses[-1][b] as Quaternion).angle_to(poses[0][b]))
			line += " %s wrap %.1f (p95 step %.1f)" % [b, wrap, float(st[int(st.size() * 0.95)])]
		print(line)
	quit(0)
