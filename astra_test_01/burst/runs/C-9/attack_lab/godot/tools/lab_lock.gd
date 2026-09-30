extends SceneTree
# FOOT LOCK ACCEPTANCE. Every number is read from the pose AS SHOWN -- after the IK -- which
# FootLock.Orient records at the end of each skeleton pass. LAB_FOOTLOCK=0 runs the identical
# instrument with the lock never engaging: the "before".
#   in_fade    world path length of each foot over [0, 0.12] s, max over feet (the brief's metric)
#   slide      the same, counting only frames where that toe is ON THE GROUND at both ends --
#              a glide; a lifted step does not count, and a lock should leave nothing here
#   lift       highest a moving foot's toe rises during the transition (a step lifts)
#   in_strike  planted-foot slide per 1/24 s inside the strike body, after the transition
#   impact     fire -> the weapon hand's peak speed (searched from 0.45 s)
#   cost       skeleton pass (Skeleton3D.advance) in microseconds, and the lock's own share
const DT := 1.0 / 96.0
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
const GROUND_H := 0.07
var k: CharacterBody3D
var tree: AnimationTree
var skel: Skeleton3D
var fl
var adv_us := []
var _d0 := {}

func _initialize() -> void:
	create_timer(float(OS.get_environment("LAB_WATCHDOG_S")) if OS.has_environment("LAB_WATCHDOG_S") else 900.0).timeout.connect(func(): push_error("LAB WATCHDOG"); quit(4))
	var ground := StaticBody3D.new()
	ground.collision_layer = CliffWorld.TERRAIN_BIT
	var cs := CollisionShape3D.new(); var box := BoxShape3D.new(); box.size = Vector3(2000, 1, 2000)
	cs.shape = box; cs.position = Vector3(0, -0.5, 0); ground.add_child(cs); root.add_child(ground)
	k = load("res://scripts/knight.gd").new()
	k.setup(RIGHT, UP, FWD, 1.10)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	tree = k._tree
	skel = k._skel
	fl = k._foot_lock
	if fl == null:
		push_error("no foot lock on this knight"); quit(5); return
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	skel.modifier_callback_mode_process = Skeleton3D.MODIFIER_CALLBACK_MODE_PROCESS_MANUAL
	k.set_gear_stack(k.gear_stack_count() - 1)
	k.global_position = Vector3(0, 0.02, 0)
	var label: String = OS.get_environment("LAB_LABEL") if OS.has_environment("LAB_LABEL") else "?"
	var idle_len: float = float(k._clip_len.get("idle_armed", 6.0))
	var out := {"label": label, "lock_enabled": bool(fl.enabled)}
	for which in ["slash", "chop", "bash", "block"]:
		var rows := []
		for ph in 8:
			await _settle(idle_len * float(ph) / 8.0)
			rows.append(_trial(which))
		var runrows := []
		for ph in 4:
			await _settle(0.0)
			for i in int((1.0 + 0.8333 * float(ph) / 4.0) / DT):
				_step(Vector2(1, 0), true)
			runrows.append(_trial(which))
		out[which] = {"idle": rows, "run": runrows}
		var f := func(rr: Array, key: String) -> Array:
			var v := rr.map(func(r): return float(r[key])); v.sort(); return v
		var fi: Array = f.call(rows, "in_fade"); var si: Array = f.call(rows, "slide"); var li: Array = f.call(rows, "lift")
		var fr: Array = f.call(runrows, "in_fade"); var sr: Array = f.call(runrows, "slide")
		var ss: Array = f.call(rows, "in_strike"); var so: Array = f.call(rows, "out_slide")
		var worst: Dictionary = rows[0]
		for r in rows:
			if float(r["in_fade"]) > float(worst["in_fade"]): worst = r
		print("[lock]   %s worst idle phase: in-fade %.3f, reach-releases %d, landings %d | run reach %s land %s"
			% [which, float(worst["in_fade"]), int(worst["reach"]), int(worst["land"]),
			   str(runrows.map(func(r): return int(r["reach"]))), str(runrows.map(func(r): return int(r["land"])))])
		print("[lock] %-11s %-5s IDLE in-fade %.3f/%.3f slide %.3f/%.3f lift max %.3f | RUN in-fade %.3f/%.3f slide %.3f/%.3f | in-strike %.1f mm/f | fade-out slide %.3f | impact %.3f s"
			% [label, which, float(fi[4]), float(fi[-1]), float(si[4]), float(si[-1]), float(li[-1]),
			   float(fr[2]), float(fr[-1]), float(sr[2]), float(sr[-1]), float(ss[-1]), float(so[-1]), float(rows[0]["impact"])])
	adv_us.sort()
	out["skeleton_advance_us"] = {"median": adv_us[adv_us.size() / 2], "p95": adv_us[int(adv_us.size() * 0.95)], "n": adv_us.size()}
	print("[lock] %s skeleton pass: median %d us, p95 %d us over %d passes" % [label, int(adv_us[adv_us.size() / 2]), int(adv_us[int(adv_us.size() * 0.95)]), adv_us.size()])
	print("[lock] %s lock decisions (last 12): %s" % [label, str(fl.events.slice(-12))])
	var fo := FileAccess.open(OS.get_environment("LAB_OUT") if OS.has_environment("LAB_OUT") else "/tmp/lock.json", FileAccess.WRITE)
	fo.store_string(JSON.stringify(out, " "))
	fo.close()
	quit(0)

func _step(dir: Vector2, run: bool) -> void:
	k.drive_dir(dir, run, DT)
	tree.advance(DT)
	# advance() only SCHEDULES the modifier pass (it runs at the next frame's deferred update);
	# this loop never yields a frame, so without the notification no modifier ever ran and every
	# "shown" position froze -- the first run of this read all zeros (ik_probe6: 0 passes after
	# advance(), exactly 1 after the notification).
	var t0 := Time.get_ticks_usec()
	skel.advance(DT)
	skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)
	adv_us.append(Time.get_ticks_usec() - t0)

func _feet() -> Array:
	# AS SHOWN: the Orient modifier's record, post-IK
	return [fl.st["L"]["shown_toe"], fl.st["R"]["shown_toe"], fl.st["L"]["shown"], fl.st["R"]["shown"]]

func _settle(phase: float) -> void:
	var g := 0
	while (k.attacking() or k.speed_px_s() > 0.0 or k.get("_block_phase") != "off") and g < 3000:
		_step(Vector2.ZERO, false); g += 1
	for i in 60:
		_step(Vector2.ZERO, false)
	var cur: float = float(tree.get("parameters/a_idle/current_position"))
	var need: float = fposmod(phase - cur, float(k._clip_len.get("idle_armed", 6.0)))
	for i in int(need / DT):
		_step(Vector2.ZERO, false)
	k.global_position = Vector3(0, 0.02, 0)
	k.velocity = Vector3.ZERO
	for i in 2:
		_step(Vector2.ZERO, false)
	await process_frame

func _trial(which: String) -> Dictionary:
	var ground: float = k.global_position.y
	_d0 = {"reach": int(fl.reach_releases), "land": int(fl.landings)}
	var prev: Array = _feet()
	var hand_bone: String = "LeftHand" if which in ["bash", "block"] else "RightHand"
	var ph: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone(hand_bone)).origin
	if which == "block":
		k.set_block(true)
	elif not k.try_strike(which):
		push_error("strike %s did not fire" % which)
	var in_fade := [0.0, 0.0, 0.0, 0.0]
	var slide := [0.0, 0.0, 0.0, 0.0]
	var lift := 0.0
	var moved := [0.0, 0.0]
	var best := 0.0
	var best_t := 0.0
	var in_strike := []
	var out_slide := 0.0
	var t := 0.0
	var g := 0
	var clip_len: float = float(k._strike_len) if which != "block" else 1.2
	var released := false
	var t_rel := 0.0
	while g < int(12.0 / DT):
		if which == "block" and t >= 1.0 and not released:
			k.set_block(false); released = true; t_rel = t
		if which != "block" and not k.attacking() and t > 0.3:
			break
		if which == "block" and released and k.get("_block_phase") == "off" and t > t_rel + 0.8:
			break
		_step(Vector2.ZERO, false)
		t += DT; g += 1
		var cur: Array = _feet()
		for i in 4:
			var a: Vector3 = prev[i]; var b: Vector3 = cur[i]
			if a == Vector3.INF or b == Vector3.INF: continue
			var d: float = (b - a).length()
			var toe_a: Vector3 = prev[i % 2]; var toe_b: Vector3 = cur[i % 2]
			var on_ground: bool = toe_a.y - ground <= GROUND_H and toe_b.y - ground <= GROUND_H
			if t <= 0.12 + 1e-6:
				in_fade[i] = float(in_fade[i]) + d
				if on_ground: slide[i] = float(slide[i]) + d
			if t <= 0.45 and i < 2:
				moved[i] = float(moved[i]) + d
				lift = maxf(lift, toe_b.y - ground)
			# fade-out: from the strike's fade-out start (or the block's release) to 0.5 s after
			var out_start: float = (clip_len - 0.25) if which != "block" else t_rel
			if (which != "block" or released) and t >= out_start and t <= out_start + 0.5 and on_ground:
				if i < 2:
					out_slide += d
		# inside the strike body, well past the transition and before its fade-out
		if which != "block" and t >= 0.45 and t <= clip_len - 0.30:
			for i in 2:
				var a2: Vector3 = prev[i]; var b2: Vector3 = cur[i]
				if a2.y - ground <= 0.03 and b2.y - ground <= 0.03:
					in_strike.append((b2 - a2).length() * 1000.0 * (1.0 / 24.0) / DT)
		prev = cur
		var h: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone(hand_bone)).origin
		var sp: float = (h - ph).length() / DT
		ph = h
		if t >= 0.45 and sp > best:
			best = sp; best_t = t
	in_strike.sort()
	var diag := {"reach": int(fl.reach_releases) - int(_d0["reach"]), "land": int(fl.landings) - int(_d0["land"])}
	var moved_far: bool = maxf(float(moved[0]), float(moved[1])) > 0.10
	return {"in_fade": maxf(maxf(float(in_fade[0]), float(in_fade[1])), maxf(float(in_fade[2]), float(in_fade[3]))),
			"slide": maxf(maxf(float(slide[0]), float(slide[1])), maxf(float(slide[2]), float(slide[3]))),
			"lift": lift if moved_far else 0.0,
			"in_strike": float(in_strike[int(in_strike.size() * 0.95)]) if in_strike.size() > 0 else 0.0,
			"out_slide": out_slide, "impact": best_t, "reach": diag["reach"], "land": diag["land"]}
