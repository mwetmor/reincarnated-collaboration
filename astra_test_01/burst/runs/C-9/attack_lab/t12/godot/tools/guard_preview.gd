extends SceneTree
# A LOOK at the solved weapon channel before anything is baked: the solved weapon_r keys are put
# on the clips IN MEMORY (a rotation track per clip), and each pose is shot BEFORE (the mount
# alone) and AFTER (the guard): the play camera at game scale, and a close-up of his right hand.
# env: SOLVE (json), POSES (clip@t,...), STILL_OUT (png)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
func _initialize() -> void:
	create_timer(300.0).timeout.connect(func(): print("[preview] WATCHDOG"); quit(4))
	var sun := DirectionalLight3D.new(); sun.rotation_degrees = Vector3(-50, 30, 0); root.add_child(sun)
	var we := WorldEnvironment.new(); var env := Environment.new()
	env.background_mode = Environment.BG_COLOR; env.background_color = Color(0.16, 0.17, 0.19)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR; env.ambient_light_color = Color(0.8, 0.8, 0.8)
	we.environment = env; root.add_child(we)
	var k = load("res://scripts/knight.gd").new()
	k.setup(RIGHT, UP, FWD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	k.global_position = Vector3(0, 0.02, 0)
	k.facing = "S"
	k._drive(0.0)
	for i in 3: await process_frame
	var skel: Skeleton3D = k._skel
	var ap: AnimationPlayer = k._anim
	(k._tree as AnimationTree).active = false
	for c in skel.get_children():
		if c is SkeletonModifier3D: (c as SkeletonModifier3D).active = false
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var sol = JSON.parse_string(FileAccess.get_file_as_string(OS.get_environment("SOLVE")))
	var wr: Dictionary = sol["weapon_r"]
	# the skeleton's track path prefix, from an existing track
	var probe := ap.get_animation("walk_armed")
	var prefix := ""
	for t in probe.get_track_count():
		var pth := String(probe.track_get_path(t))
		if pth.ends_with(":RightHand"): prefix = pth.substr(0, pth.length() - "RightHand".length())
	var poses: PackedStringArray = OS.get_environment("POSES").split(",")
	var svs := []; var cams := []; var labs := []
	for i in 2:
		var sv := SubViewport.new(); sv.size = Vector2i(480, 540); sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(sv)
		var c := Camera3D.new(); c.projection = Camera3D.PROJECTION_ORTHOGONAL; c.near = 0.1; c.far = 400.0
		sv.add_child(c); c.current = true
		var lb := Label.new(); lb.position = Vector2(6, 6); lb.add_theme_font_size_override("font_size", 15)
		lb.add_theme_color_override("font_color", Color(1, 1, 1))
		var sb := StyleBoxFlat.new(); sb.bg_color = Color(0, 0, 0, 0.6); lb.add_theme_stylebox_override("normal", sb)
		sv.add_child(lb)
		svs.append(sv); cams.append(c); labs.append(lb)
	var sheet := Image.create(480 * 4, 540 * poses.size(), false, Image.FORMAT_RGB8)
	for pi in poses.size():
		var pr: PackedStringArray = poses[pi].split("@")
		var clip := pr[0]; var t := float(pr[1])
		for mode in 2:
			var a := ap.get_animation(clip if not clip.begins_with("tree_") else "walk_armed")
			var ti := a.find_track(NodePath(prefix + "weapon_r"), Animation.TYPE_ROTATION_3D)
			if ti >= 0: a.remove_track(ti)
			if mode == 1 and wr.has(clip) and not clip.begins_with("tree_"):
				ti = a.add_track(Animation.TYPE_ROTATION_3D)
				a.track_set_path(ti, NodePath(prefix + "weapon_r"))
				var ts: Array = wr[clip]["times"]; var qs: Array = wr[clip]["quats"]
				for j in ts.size():
					var q: Array = qs[j]
					a.rotation_track_insert_key(ti, float(ts[j]), Quaternion(q[0], q[1], q[2], q[3]))
			if clip.begins_with("tree_"):
				var gait: String = clip.substr(5)
				var up_clip: String = "walk_armed" if gait == "walk" else "run_armed"
				var a2 := ap.get_animation(up_clip)
				var ti2 := a2.find_track(NodePath(prefix + "weapon_r"), Animation.TYPE_ROTATION_3D)
				if ti2 >= 0: a2.remove_track(ti2)
				if mode == 1 and wr.has(up_clip):
					ti2 = a2.add_track(Animation.TYPE_ROTATION_3D)
					a2.track_set_path(ti2, NodePath(prefix + "weapon_r"))
					var ts2: Array = wr[up_clip]["times"]; var qs2: Array = wr[up_clip]["quats"]
					for j in ts2.size():
						var q2: Array = qs2[j]
						a2.rotation_track_insert_key(ti2, float(ts2[j]), Quaternion(q2[0], q2[1], q2[2], q2[3]))
				ap.active = false
				var tr: AnimationTree = k._tree
				tr.active = true
				tr.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
				k.global_position = Vector3(0, 0.02, 0)
				for j in int(t):
					k.drive_dir(Vector2(0, 1), gait == "run", 1.0 / 24.0)
					tr.advance(1.0 / 24.0)
				skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)
				tr.active = false
				ap.active = true
			else:
				ap.play(clip); ap.seek(t, true, true)
				skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)
			var tgt: Vector3 = k.global_position + Vector3(0, 0.95, 0)
			(cams[0] as Camera3D).size = 3.0
			(cams[0] as Camera3D).look_at_from_position(tgt - FWD * 60.0, tgt, UP)
			var hand: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone("RightHand")).origin
			(cams[1] as Camera3D).size = 0.9
			(cams[1] as Camera3D).look_at_from_position(hand - FWD * 60.0, hand, UP)
			(labs[0] as Label).text = "%s @ %.2f  %s  play camera" % [clip, t, "BEFORE (mount)" if mode == 0 else "AFTER (weapon_r guard)"]
			(labs[1] as Label).text = "close-up, his right hand"
			for f in 3: await RenderingServer.frame_post_draw
			for i in 2:
				var im: Image = (svs[i] as SubViewport).get_texture().get_image(); im.convert(Image.FORMAT_RGB8)
				sheet.blit_rect(im, Rect2i(0, 0, 480, 540), Vector2i(480 * (mode * 2 + i), 540 * pi))
	sheet.save_png(OS.get_environment("STILL_OUT"))
	print("[preview] ok")
	quit(0)
