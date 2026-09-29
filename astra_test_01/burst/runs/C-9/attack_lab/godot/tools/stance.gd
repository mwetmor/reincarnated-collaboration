extends SceneTree
# What differs between the Axe Stance idle and each strike's first frame? Feet, hip height and
# pelvis YAW, decomposed -- on pristine clips (cache bypassed), rig space, metres at scale 1.0.
# And how far the idle's own feet wander over its loop, because a strike can fire at any phase.
var sk: Skeleton3D
var _idle_len := 0.0
var _idle_phases := []
var ap: AnimationPlayer
var s := 1.0
func _initialize() -> void:
	# WATCHDOG. A SceneTree script whose coroutine dies on an error never reaches quit(), and
	# this one runs under the SHARED heavy lock: on 2026-09-29 a null load killed stance.gd
	# mid-await and it held the lock for ten minutes with the integration build queued behind
	# it. A timer on the main loop fires whether or not the coroutine is alive.
	create_timer(float(OS.get_environment("LAB_WATCHDOG_S")) if OS.has_environment("LAB_WATCHDOG_S") else 240.0).timeout.connect(func(): push_error("LAB WATCHDOG: quitting a hung script"); quit(4))
	var ps := ResourceLoader.load("res://models/gear/nb-body.glb", "", ResourceLoader.CACHE_MODE_IGNORE_DEEP) as PackedScene
	var r := ps.instantiate()
	root.add_child(r)
	await process_frame
	await process_frame
	for n in r.find_children("*", "", true, false):
		if n is Skeleton3D and sk == null: sk = n
		elif n is AnimationPlayer and ap == null: ap = n
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	ap.active = true
	s = sk.global_transform.basis.get_scale().x
	var alt_path: String = ""
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--idle="): alt_path = a.substr(7)
	var idle_clip := "idle_armed"
	if alt_path != "":
		var ps2 := ResourceLoader.load(alt_path, "", ResourceLoader.CACHE_MODE_IGNORE_DEEP) as PackedScene
		var r2 := ps2.instantiate()
		root.add_child(r2)
		await process_frame
		await process_frame
		var sk2: Skeleton3D = null
		var ap2: AnimationPlayer = null
		for n2 in r2.find_children("*", "", true, false):
			if n2 is Skeleton3D and sk2 == null: sk2 = n2
			elif n2 is AnimationPlayer and ap2 == null: ap2 = n2
		ap2.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
		ap2.active = true
		idle_clip = String(ap2.get_animation_list()[0])
		print("CANDIDATE IDLE %s  clip '%s' (%.3f s), rig scale %.6f vs body %.6f"
			% [alt_path.get_file(), idle_clip, ap2.get_animation(idle_clip).length,
			   sk2.global_transform.basis.get_scale().x, s])
		var keep := [sk, ap, s]
		sk = sk2; ap = ap2; s = sk2.global_transform.basis.get_scale().x
		_idle_len = ap.get_animation(idle_clip).length
		_idle_phases = []
		for i in 96:
			_idle_phases.append(_at(idle_clip, _idle_len * float(i) / 96.0))
		sk = keep[0]; ap = keep[1]; s = keep[2]
	# ---- the idle's own wander ---------------------------------------------------------
	var n := 96
	var idle := []
	if alt_path != "":
		idle = _idle_phases
	else:
		for i in n:
			idle.append(_at("idle_armed", ap.get_animation("idle_armed").length * float(i) / float(n)))
	var spread := {}
	for foot in ["L", "R"]:
		var lo := Vector3(1e9, 1e9, 1e9); var hi := -lo
		for p in idle:
			lo = lo.min(p[foot]); hi = hi.max(p[foot])
		spread[foot] = Vector2(hi.x - lo.x, hi.z - lo.z).length()
	# medoid: the idle phase whose feet are nearest, worst-case, to every other phase
	var best := 1e9
	var med := 0
	for i in n:
		var worst := 0.0
		for j in n:
			worst = maxf(worst, maxf(_fd(idle[i]["L"], idle[j]["L"]), _fd(idle[i]["R"], idle[j]["R"])))
		if worst < best:
			best = worst; med = i
	print("%s over its loop:" % idle_clip.to_upper(), "")
	print("  IDLE over its loop: left foot wanders %.3f m, right %.3f m (horizontal extent)" % [spread["L"], spread["R"]])
	print("  medoid phase %d/%d (t=%.3f s): every other phase within %.3f m, worst foot" % [med, n, float(idle[med]["t"]), best])
	var I: Dictionary = idle[med]
	_pr("idle MEDOID", I)
	for clip in ["attack", "attack_chop", "shield_bash", "run_armed"]:
		var a := ap.get_animation(clip)
		for tt in [0.0]:
			if tt > a.length: continue
			var P := _at(clip, tt)
			print("  %-12s t=%.2f  L foot %.3f m  R foot %.3f m from the idle's | hips height %+.3f m | pelvis yaw %+.1f deg"
				% [clip, tt, _fd(P["L"], I["L"]), _fd(P["R"], I["R"]), float(P["hy"]) - float(I["hy"]),
				   wrapf(float(P["yaw"]) - float(I["yaw"]), -180.0, 180.0)])
	quit(0)

func _at(clip: String, t: float) -> Dictionary:
	ap.play(clip)
	ap.seek(t, true, true)
	var L: Vector3 = (_b("LeftFoot") + _b("LeftToeBase")) * 0.5
	var R: Vector3 = (_b("RightFoot") + _b("RightToeBase")) * 0.5
	var lh: Vector3 = _b("LeftUpLeg")
	var rh: Vector3 = _b("RightUpLeg")
	var across := Vector2(lh.x - rh.x, lh.z - rh.z)
	return {"t": t, "L": L, "R": R, "hy": _b("Hips").y, "yaw": rad_to_deg(across.angle())}

func _b(bn: String) -> Vector3:
	return sk.get_bone_global_pose(sk.find_bone(bn)).origin * s

func _fd(a: Vector3, b: Vector3) -> float:
	return Vector2(a.x - b.x, a.z - b.z).length()

func _pr(label: String, P: Dictionary) -> void:
	print("  %s: feet L (%.2f, %.2f) R (%.2f, %.2f), stance width %.2f m, hips %.2f m high, pelvis yaw %.1f deg"
		% [label, (P["L"] as Vector3).x, (P["L"] as Vector3).z, (P["R"] as Vector3).x, (P["R"] as Vector3).z,
		   _fd(P["L"], P["R"]), float(P["hy"]), float(P["yaw"])])
