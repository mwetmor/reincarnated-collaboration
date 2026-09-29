extends SceneTree
# An armed idle should stand planted. Measure three candidates on the same instrument:
#   ORIGINAL  idle_armed (Meshy 85 Axe Stance) as shipped
#   DAMPED    the same, hips' horizontal excursion scaled about its mean so it stays <= 0.10 m
#   BREATHE   Meshy 335 "Axe Breathe and Look Around" (fetched in W1, never used)
# For each: hips' horizontal distance from rest, how far each foot wanders, and PLANTED-FOOT
# SLIDE -- a foot within 2 cm of its lowest on two consecutive frames that still moves. A
# damped hip path cannot be free: a planted foot's position is hips + leg, so every
# millimetre taken off the hips' travel is a millimetre the planted foot now slides.
func _initialize() -> void:
	create_timer(240.0).timeout.connect(func(): push_error("LAB WATCHDOG"); quit(4))
	var body := await _rig("res://models/gear/nb-body.glb")
	var br := await _rig("res://models/axe_breathe.glb")
	if (body[1] as AnimationPlayer).has_animation("idle_armed_stance"):
		_measure("B idle_armed (planted, merged)", body, "idle_armed")
		_measure("B idle_armed_stance (kept)", body, "idle_armed_stance")
	else:
		var a: Animation = (body[1] as AnimationPlayer).get_animation("idle_armed")
		_measure("ORIGINAL idle_armed", body, "idle_armed")
		var k := _damp(a, body[0], 0.10)
		_measure("DAMPED   idle_armed (x%.3f)" % k, body, "idle_armed")
		var bname: String = String((br[1] as AnimationPlayer).get_animation_list()[0])
		_measure("BREATHE  axe_breathe", br, bname)
	quit(0)

func _rig(path: String) -> Array:
	var ps := ResourceLoader.load(path, "", ResourceLoader.CACHE_MODE_IGNORE_DEEP) as PackedScene
	if ps == null:
		push_error("could not load %s -- is it imported?" % path)
		quit(5)
		return []
	var r := ps.instantiate()
	root.add_child(r)
	await process_frame
	await process_frame
	var sk: Skeleton3D = null
	var ap: AnimationPlayer = null
	for n in r.find_children("*", "", true, false):
		if n is Skeleton3D and sk == null: sk = n
		elif n is AnimationPlayer and ap == null: ap = n
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	ap.active = true
	return [sk, ap]

func _damp(a: Animation, sk: Skeleton3D, limit_m: float) -> float:
	var tr := -1
	for i in a.get_track_count():
		if a.track_get_type(i) == Animation.TYPE_POSITION_3D and String(a.track_get_path(i).get_concatenated_subnames()) == "Hips":
			tr = i
	var n := a.track_get_key_count(tr)
	var mean := Vector3.ZERO
	for i in n: mean += a.track_get_key_value(tr, i)
	mean /= float(n)
	var mpu: float = sk.global_transform.basis.get_scale().x
	var rest: Vector3 = sk.get_bone_rest(sk.find_bone("Hips")).origin
	var mx := 0.0
	for i in n:
		var v: Vector3 = a.track_get_key_value(tr, i)
		mx = maxf(mx, Vector2(v.x - rest.x, v.z - rest.z).length() * mpu)
	var k: float = minf(1.0, limit_m / maxf(mx, 1e-9))
	for i in n:
		var v2: Vector3 = a.track_get_key_value(tr, i)
		a.track_set_key_value(tr, i, Vector3(rest.x + (v2.x - rest.x) * k, v2.y, rest.z + (v2.z - rest.z) * k))
	return k

func _measure(label: String, rig: Array, clip: String) -> void:
	var sk: Skeleton3D = rig[0]
	var ap: AnimationPlayer = rig[1]
	var s: float = sk.global_transform.basis.get_scale().x
	var a := ap.get_animation(clip)
	var n := int(round(a.length * 24.0))
	ap.play(clip)
	var rest: Vector3 = sk.get_bone_rest(sk.find_bone("Hips")).origin
	var hmax := 0.0
	var feet := {"LeftToeBase": [], "RightToeBase": []}
	for i in n + 1:
		ap.seek(a.length * float(i) / float(n), true, true)
		var h: Vector3 = sk.get_bone_global_pose(sk.find_bone("Hips")).origin
		hmax = maxf(hmax, Vector2(h.x - rest.x, h.z - rest.z).length() * s)
		for f in feet.keys():
			(feet[f] as Array).append(sk.get_bone_global_pose(sk.find_bone(f)).origin * s)
	var wander := []
	var slide := []
	var slide_total := 0.0
	for f in feet.keys():
		var P: Array = feet[f]
		var lo := 1e9
		var bb_lo := Vector2(1e9, 1e9)
		var bb_hi := Vector2(-1e9, -1e9)
		for p in P:
			lo = minf(lo, (p as Vector3).y)
			bb_lo = bb_lo.min(Vector2((p as Vector3).x, (p as Vector3).z))
			bb_hi = bb_hi.max(Vector2((p as Vector3).x, (p as Vector3).z))
		wander.append((bb_hi - bb_lo).length())
		for i in range(1, P.size()):
			var p0: Vector3 = P[i - 1]
			var p1: Vector3 = P[i]
			var band: float = float(OS.get_environment("LAB_BAND")) if OS.has_environment("LAB_BAND") else 0.02
			if p0.y <= lo + band and p1.y <= lo + band:
				var d: float = Vector2(p1.x - p0.x, p1.z - p0.z).length()
				slide.append(d * 1000.0)
				slide_total += d
	slide.sort()
	print("%-32s %.2f s | hips from rest <= %.3f m | feet wander L %.3f R %.3f m | planted-foot slide median %.1f, worst %.1f mm/frame, total %.3f m over %d planted frames"
		% [label, a.length, hmax, float(wander[0]), float(wander[1]),
		   float(slide[slide.size() / 2]) if slide.size() > 0 else -1.0,
		   float(slide[-1]) if slide.size() > 0 else -1.0, slide_total, slide.size()])
