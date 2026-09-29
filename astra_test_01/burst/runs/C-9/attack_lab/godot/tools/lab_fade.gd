extends SceneTree
# FOOT SWING INSIDE THE FADE, across the idle's whole loop and across the run cycle.
# One knight per process (the lab switches mutate shared clips once); each strike is fired at
# N idle phases and M run phases, and the tree is run to the end of the strike between trials.
#   in-fade swing  path length of each foot in the world over [0, 0.12] s, max over feet
#   glide          the same over [0, lead + 0.12] s: where a lead-in PUTS the motion it moves
#   impact         time from fire to the weapon hand's peak world speed
const DT := 1.0 / 96.0
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
var k: CharacterBody3D
var tree: AnimationTree
var skel: Skeleton3D
var _traced := false

func _initialize() -> void:
	create_timer(float(OS.get_environment("LAB_WATCHDOG_S")) if OS.has_environment("LAB_WATCHDOG_S") else 600.0).timeout.connect(func(): push_error("LAB WATCHDOG"); quit(4))
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
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	k.set_gear_stack(k.gear_stack_count() - 1)
	k.global_position = Vector3(0, 0.02, 0)
	var label: String = OS.get_environment("LAB_LABEL") if OS.has_environment("LAB_LABEL") else "?"
	var lead := {}
	if OS.has_environment("LAB_LEADIN"):
		for item in OS.get_environment("LAB_LEADIN").split(","):
			var kv: PackedStringArray = item.split(":")
			lead[kv[0]] = float(kv[1])
	var idle_len: float = float(k._clip_len.get("idle_armed", 6.0))
	var out := {"label": label, "idle_len": idle_len}
	for which in ["slash", "chop", "bash"]:
		var clip: String = String(k._roles.get({"slash": "attack", "chop": "chop", "bash": "bash"}[which], ""))
		var L: float = float(lead.get(clip, 0.0))
		var rows := []
		for ph in 8:
			await _settle_idle(idle_len * float(ph) / 8.0)
			rows.append(await _trial(which, false, L))
		var runrows := []
		for ph in 4:
			runrows.append(await _run_trial(which, L, 1.0 + 0.8333 * float(ph) / 4.0))
		var imp: float = float(rows[0][2])
		var sw := rows.map(func(r): return float(r[0]))
		var gl := rows.map(func(r): return float(r[1]))
		var rsw := runrows.map(func(r): return float(r[0]))
		sw.sort(); gl.sort(); rsw.sort()
		out[which] = {"lead_s": L, "idle_in_fade_m": sw, "idle_glide_m": gl, "run_in_fade_m": rsw, "impact_s": imp}
		print("[fade] %-9s %-5s lead %.3f s | from IDLE in-fade swing: median %.3f worst %.3f m (8 phases) | glide worst %.3f m | from RUN in-fade: median %.3f worst %.3f m | impact %.3f s"
			% [label, which, L, float(sw[4]), float(sw[-1]), float(gl[-1]), float(rsw[2]), float(rsw[-1]), imp])
	var f := FileAccess.open(OS.get_environment("LAB_OUT") if OS.has_environment("LAB_OUT") else "/tmp/fade.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " "))
	f.close()
	quit(0)

func _step(dir: Vector2, run: bool) -> void:
	k.drive_dir(dir, run, DT)
	tree.advance(DT)

func _settle_idle(phase: float) -> void:
	# stand still until nothing is running, then walk the idle to the requested phase
	var g := 0
	while (k.attacking() or k.speed_px_s() > 0.0) and g < 2000:
		_step(Vector2.ZERO, false); g += 1
	for i in 60:
		_step(Vector2.ZERO, false)
	var cur: float = float(tree.get("parameters/a_idle/current_position"))
	var idle_len: float = float(k._clip_len.get("idle_armed", 6.0))
	var need: float = fposmod(phase - cur, idle_len)
	var n := int(need / DT)
	for i in n:
		_step(Vector2.ZERO, false)
	k.global_position = Vector3(0, 0.02, 0)
	k.velocity = Vector3.ZERO
	await process_frame

func _feet() -> Array:
	return [skel.global_transform * skel.get_bone_global_pose(skel.find_bone("LeftToeBase")).origin,
			skel.global_transform * skel.get_bone_global_pose(skel.find_bone("RightToeBase")).origin,
			skel.global_transform * skel.get_bone_global_pose(skel.find_bone("LeftFoot")).origin,
			skel.global_transform * skel.get_bone_global_pose(skel.find_bone("RightFoot")).origin]

func _trial(which: String, _run: bool, L: float) -> Array:
	var prev: Array = _feet()
	var hand_bone: String = "LeftHand" if which == "bash" else "RightHand"
	var ph: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone(hand_bone)).origin
	if not k.try_strike(which):
		push_error("strike %s did not fire" % which)
	var tot := [0.0, 0.0, 0.0, 0.0]
	var inf := 0.0
	var glide := 0.0
	var best := 0.0
	var best_t := 0.0
	var t := 0.0
	var g := 0
	var trace: bool = OS.has_environment("LAB_TRACE") and not _traced
	if trace:
		_traced = true
		print("[trace] %s fired; body %s; idle pos %.3f" % [which, str(k.global_position.snappedf(0.001)), float(tree.get("parameters/a_idle/current_position"))])
	while (k.attacking() or t < 0.2) and g < int(12.0 / DT):
		_step(Vector2.ZERO, false)
		t += DT; g += 1
		var cur: Array = _feet()
		if trace and t <= 0.16:
			var hips: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone("Hips")).origin
			print("[trace] t=%.3f body %s hips %s | LToe step %5.1f mm RToe %5.1f LFoot %5.1f RFoot %5.1f | LToe at %s"
				% [t, str(k.global_position.snappedf(0.001)), str(hips.snappedf(0.001)),
				   ((cur[0] as Vector3) - (prev[0] as Vector3)).length() * 1000.0,
				   ((cur[1] as Vector3) - (prev[1] as Vector3)).length() * 1000.0,
				   ((cur[2] as Vector3) - (prev[2] as Vector3)).length() * 1000.0,
				   ((cur[3] as Vector3) - (prev[3] as Vector3)).length() * 1000.0,
				   str((cur[0] as Vector3).snappedf(0.001))])
		for i in 4:
			tot[i] = float(tot[i]) + ((cur[i] as Vector3) - (prev[i] as Vector3)).length()
		prev = cur
		var m: float = maxf(maxf(float(tot[0]), float(tot[1])), maxf(float(tot[2]), float(tot[3])))
		if t <= 0.12 + 1e-6:
			inf = m
		if t <= L + 0.12 + 1e-6:
			glide = m
		var h: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone(hand_bone)).origin
		var sp: float = (h - ph).length() / DT
		ph = h
		# IMPACT is the strike's own peak, not the fade: the first version found the hand's
		# fastest moment on the first frame after firing whenever the stance gap was large
		if t >= 0.45 and sp > best:
			best = sp; best_t = t
	return [inf, glide, best_t]

func _run_trial(which: String, L: float, run_s: float) -> Array:
	await _settle_idle(0.0)
	for i in int(run_s / DT):
		_step(Vector2(1, 0), true)
	var r: Array = await _trial(which, false, L)
	return r
