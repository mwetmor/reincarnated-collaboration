extends SceneTree
# C-9: the transitions, measured.
#
# WHAT A SLIDING FOOT ACTUALLY IS. Not "the animation rate disagrees with the ground speed"
# -- that is a proxy. A planted foot is a foot that does not move, because the ground does
# not move. So the test is the stance foot's travel IN WORLD SPACE while it is planted: if
# the blend and the body agree, it is zero; if they disagree by any amount, for any reason,
# it shows up here without having to be predicted first.
#
# The stop time is measured the same way -- from the frame the key is released to the frame
# the pose stops changing -- rather than from the smoothing constant, which is what the code
# intends rather than what it does.
#
#   Godot --path godot --resolution 800x450 --script tools/probe_transitions.gd -- [--out D]

const DT := 1.0 / 24.0
const SPOT := Vector2(2285.62, 2407.32)

var scene
var lines: Array[String] = []


func say(s: String) -> void:
	print(s)
	lines.append(s)


func _initialize() -> void:
	var out := ProjectSettings.globalize_path("user://trans")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out)
	Engine.physics_ticks_per_second = 24
	scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60:
		await process_frame
	var k = scene.knight
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--tau="):
			k.CYCLE_TAU_S = float(a.substr(6))
			print("  [A/B] CYCLE_TAU_S = %.3f s" % k.CYCLE_TAU_S)
	if "--no-sync" in OS.get_cmdline_user_args():
		k.sync_group = false
		print("  [A/B] SYNC GROUP OFF -- pre-sync behaviour, same instrument")
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	var skel: Skeleton3D = k._skel
	var anim: AnimationPlayer = k._anim
	var report := {}

	# ---- 0. the corrected idle: is the Hips scale track gone? ---------------
	var idle := anim.get_animation("idle")
	var hip_scale := "no scale track"
	for i in idle.get_track_count():
		if idle.track_get_type(i) == Animation.TYPE_SCALE_3D \
				and String(idle.track_get_path(i).get_concatenated_subnames()) == "Hips":
			var v: Vector3 = idle.scale_track_interpolate(i, 0.0)
			hip_scale = "scale track present, value %s" % str(v.snappedf(0.0001))
	say("[0] the idle's Hips: %s" % hip_scale)
	report["idle_hips"] = hip_scale

	# ---- 1. a rigid span across the three clips ----------------------------
	# NOT the screen silhouette: at 52.95 deg fore-aft extent projects 0.798 screen-metres
	# per metre against stature's 0.603, so a stride moves the silhouette by a fifth without
	# the man changing size at all. A bone span is rigid by construction.
	say("")
	say("[1] RIGID SPANS across the clips (a bone span cannot be moved by a stride)")
	var ls := skel.find_bone("LeftShoulder")
	var rs := skel.find_bone("RightShoulder")
	var hd := skel.find_bone("Head")
	var he := skel.find_bone("head_end")
	var spans := {}
	anim.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	k._tree.active = false
	anim.active = true
	for clip in ["idle", "walk", "run"]:
		anim.play(clip)
		var a := anim.get_animation(clip)
		var n := int(round(a.length * 24.0))
		var sh := 0.0
		var hl := 0.0
		for i in n:
			anim.seek(a.length * float(i) / float(n), true, true)
			await process_frame
			sh += (skel.get_bone_global_pose(ls).origin - skel.get_bone_global_pose(rs).origin).length()
			hl += (skel.get_bone_global_pose(hd).origin - skel.get_bone_global_pose(he).origin).length()
		spans[clip] = {"shoulder_span": snappedf(sh / float(n), 0.0001),
					   "head_length": snappedf(hl / float(n), 0.0001)}
		say("    %-5s shoulder span %.4f   head length %.4f" %
			[clip, spans[clip]["shoulder_span"], spans[clip]["head_length"]])
	var base: float = float(spans["idle"]["shoulder_span"])
	for clip in ["walk", "run"]:
		var d: float = (float(spans[clip]["shoulder_span"]) / maxf(base, 1e-9) - 1.0) * 100.0
		say("    %-5s shoulder span is %+.2f%% of idle's" % [clip, d])
	report["rigid_spans"] = spans
	anim.active = false
	k._tree.active = true
	anim.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS

	# ---- 2. stopping, and whether the feet slide while it happens ----------
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	for run in [false, true]:
		var g := CliffWorld.ground_at(space, SPOT, scene.right, scene.up, scene.fwd)
		k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.05
		k.velocity = Vector3.ZERO
		for i in 30:
			k.drive_dir(Vector2(1, 0), run, DT)
			await physics_frame
		var top: float = k.speed_px_s()
		# release, and watch
		# WHEN HAS HE STOPPED? Not "when the pose stops changing": idle BREATHES, so that
		# threshold is never crossed and the first run of this reported -1 frames. The ramp
		# ends when the smoothed ground speed reaches zero, which is the quantity the
		# transition is actually about; the pose then converges onto idle's own cycle.
		var frames := 0
		var slides := []
		var foot_lows := []
		var prev_foot := Vector3.ZERO
		var prev_h := 1e9
		var prev_low := -1
		var settled := -1
		var prev_pose := _pose(skel)
		while frames < 60:
			k.drive_dir(Vector2.ZERO, false, DT)
			await physics_frame
			frames += 1
			var lf: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone("LeftToeBase")).origin
			var rf: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone("RightToeBase")).origin
			var low: int = 0 if lf.y <= rf.y else 1
			var foot: Vector3 = lf if low == 0 else rf
			# PLANTED, not merely lower. At a run the swinging foot can be the lower of the
			# two for a frame and it travels 0.22 m in that frame -- which is a foot moving
			# at 5 m/s, correctly, and not a slide. A planted foot is one at the bottom of
			# its own range, so the range is collected first and the filter applied after.
			foot_lows.append(foot.y - k.global_position.y)
			# ON THE FLOOR, or there is no planted foot to measure. Walking him in one
			# direction for 86 frames at up to 6.4 m/s takes him off the plateau: the body
			# was travelling 0.569 m per frame where its speed says 0.084, which is a fall,
			# and the "planted" foot was falling with it. Every spike over 0.25 m in the
			# first run of this was that, not a blend artefact.
			var h: float = foot.y - k.global_position.y
			# BOTH ENDS of the pair must be on the ground. Checking only the current frame
			# counts the frame a foot lands on: at 6.4 m/s that foot was 0.4 m behind and
			# airborne one frame earlier, so its "travel" is the swing, measured correctly,
			# and it is not a slide. Ground contact in a 24 fps run lasts 2-3 frames, so
			# there are real planted PAIRS -- they just have to be asked for.
			if low == prev_low and k.is_on_floor():
				slides.append([(foot - prev_foot).length(), h, prev_h])
			prev_low = low
			prev_foot = foot
			prev_h = h
			var pose := _pose(skel)
			if settled < 0 and k.speed_px_s() <= 0.0:
				settled = frames
			prev_pose = pose
			if settled > 0 and frames > settled + 4:
				break
		foot_lows.sort()
		var floor_y: float = foot_lows[0] if foot_lows.size() > 0 else 0.0
		var planted := []
		for s in slides:
			if float(s[1]) <= floor_y + 0.03 and float(s[2]) <= floor_y + 0.03 \
					and absf(float(s[1]) - float(s[2])) <= 0.010:
				planted.append(float(s[0]))
		planted.sort()
		var med: float = planted[planted.size() / 2] if planted.size() > 0 else 0.0
		var worst: float = planted[-1] if planted.size() > 0 else 0.0
		var label := "run" if run else "walk"
		say("")
		say("[2] STOPPING FROM %s (top speed %.1f canvas px/s)" % [label.to_upper(), top])
		say("    key released -> pose at rest: %d frames = %.2f s" % [settled, float(settled) * DT])
		say("    planted-foot travel while stopping: median %.4f m, worst %.4f m per frame  (%d planted frames of %d)"
			% [med, worst, planted.size(), slides.size()])
		report["stop_from_" + label] = {"top_px_s": snappedf(top, 0.1), "frames": settled,
			"seconds": snappedf(float(settled) * DT, 0.01),
			"planted_foot_median_m": snappedf(med, 0.0001),
			"planted_foot_worst_m": snappedf(worst, 0.0001),
			"planted_frames": planted.size(), "sampled_frames": slides.size(),
			"planted_mm_sorted": planted.map(func(x): return snappedf(x * 1000.0, 0.1))}
		say("    every planted pair, mm: %s" % str(planted.map(func(x): return snappedf(x * 1000.0, 0.1))))

	# ---- 2b. the walk<->run change, which is where the 219 mm frame lived ---
	say("")
	say("[2b] WALK -> RUN -> WALK, held at each, planted-foot travel throughout")
	var g2 := CliffWorld.ground_at(space, SPOT, scene.right, scene.up, scene.fwd)
	k.global_position = (g2["position"] as Vector3) + Vector3.UP * 0.05
	k.velocity = Vector3.ZERO
	var legs := [["walk", false, 22, 1.0], ["run", true, 26, 1.0],
				 ["walk", false, 22, -1.0], ["run", true, 26, -1.0]]
	var sl := []
	var lows := []
	var pl := -1
	var pf := Vector3.ZERO
	var ph := 1e9
	for leg in legs:
		for i in int(leg[2]):
			k.drive_dir(Vector2(float(leg[3]), 0), bool(leg[1]), DT)
			await physics_frame
			var lf: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone("LeftToeBase")).origin
			var rf: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone("RightToeBase")).origin
			var low: int = 0 if lf.y <= rf.y else 1
			var foot: Vector3 = lf if low == 0 else rf
			lows.append(foot.y - k.global_position.y)
			var h2: float = foot.y - k.global_position.y
			if low == pl and k.is_on_floor():
				sl.append([(foot - pf).length(), h2, ph, String(leg[0])])
			pl = low
			pf = foot
			ph = h2
	lows.sort()
	var fy: float = lows[0] if lows.size() > 0 else 0.0
	var planted2 := []
	for s in sl:
		if float(s[1]) <= fy + 0.03 and float(s[2]) <= fy + 0.03 \
				and absf(float(s[1]) - float(s[2])) <= 0.010:
			planted2.append(float(s[0]))
	planted2.sort()
	var m2: float = planted2[planted2.size() / 2] if planted2.size() > 0 else 0.0
	var w2: float = planted2[-1] if planted2.size() > 0 else 0.0
	say("    planted-foot travel: median %.4f m, worst %.4f m per frame  (%d planted of %d)"
		% [m2, w2, planted2.size(), sl.size()])
	report["walk_run_walk"] = {"planted_median_m": snappedf(m2, 0.0001),
		"planted_worst_m": snappedf(w2, 0.0001), "planted_frames": planted2.size(),
		"sampled_frames": sl.size(),
		"planted_mm_sorted": planted2.map(func(x): return snappedf(x * 1000.0, 0.1))}
	say("    every planted pair, mm: %s" % str(planted2.map(func(x): return snappedf(x * 1000.0, 0.1))))

	# ---- 3. the attack fade ------------------------------------------------
	say("")
	say("[3] THE ATTACK")
	var fired: bool = k.try_attack()
	var on := 0
	var f := 0
	while f < 80:
		k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
		f += 1
		if k.attacking():
			on += 1
		elif on > 0:
			break
	say("    fired=%s, one-shot active for %d frames = %.2f s (clip is %.2f s + %.2f s fade out)"
		% [fired, on, float(on) * DT, float(k._clip_len.get("attack", 0.0)),
		   float((k.cfg.get("transitions", {}) as Dictionary).get("attack_fade_out_s", 0.0))])
	report["attack_active_s"] = snappedf(float(on) * DT, 0.01)

	var fh := FileAccess.open(out + "/transitions.json", FileAccess.WRITE)
	fh.store_string(JSON.stringify(report, " "))
	fh.close()
	var gh := FileAccess.open(out + "/transitions.txt", FileAccess.WRITE)
	gh.store_string("\n".join(lines) + "\n")
	gh.close()
	print("[trans] -> ", out)
	quit(0)


func _delta(a: PackedFloat32Array, b: PackedFloat32Array) -> float:
	"""How far the whole pose moved between two frames, as one number: the RMS of every
	bone's displacement. `the pose stopped changing` needs a threshold and this is the
	quantity it is a threshold on."""
	var s := 0.0
	for i in mini(a.size(), b.size()):
		var d: float = a[i] - b[i]
		s += d * d
	return sqrt(s / maxf(float(a.size()), 1.0))


func _pose(skel: Skeleton3D) -> PackedFloat32Array:
	var o := PackedFloat32Array()
	for b in skel.get_bone_count():
		var p: Vector3 = skel.get_bone_global_pose(b).origin
		o.append(p.x)
		o.append(p.y)
		o.append(p.z)
	return o
