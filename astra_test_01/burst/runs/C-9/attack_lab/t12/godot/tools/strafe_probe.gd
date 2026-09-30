extends SceneTree
# T12_10 STRAFE PROBE -- the strafes as the scene plays them: guard up (the strafe is a blocking move),
# one knight driven the way guard_accept.gd drives it (the canvas direction along his strafe
# direction), full kit, figure scale 1.0, 1/24 s steps, 7 s per side, the first 1.5 s dropped.
#   speed      the body's measured ground speed along the strafe (m/s), against the speed knight.gd
#              was asked for (strafe_px_s) -- and the clip's own FOOT-LOCK as the scene plays it: the
#              median backward speed of a planted foot RELATIVE TO THE BODY (57_footlock.py's rule:
#              the foot joints' bottom 25% of height is contact). Equal = the feet are pinned.
#   slide      the support toe's world travel per frame (mm): SUPPORT = the lower toe, same foot both
#              frames (58_loop_blend.py's rule); PROBE = speed_split.gd's pair rule (lower toe within
#              3 cm of the lowest, height change <= 1 cm)
#   wrap       the clip's loop point as played: the largest joint step across the frame where the
#              clip's position wraps, against the median step (1.0 = a normal frame; >> 1 = a pop)
# env: KNIGHT (res:// script), KNIGHT_CHARACTER (knight_sword.gd reads it), PROBE_LABEL, PROBE_OUT
const DT := 1.0 / 24.0
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
var k
var skel: Skeleton3D
var tree: AnimationTree
var bi := {}
const JOINTS := ["Hips", "Spine", "Head", "LeftHand", "RightHand", "LeftFoot", "RightFoot", "LeftToeBase", "RightToeBase"]

func _initialize() -> void:
	var label: String = OS.get_environment("PROBE_LABEL") if OS.has_environment("PROBE_LABEL") else "?"
	var ground := StaticBody3D.new()
	ground.collision_layer = CliffWorld.TERRAIN_BIT
	var cs := CollisionShape3D.new(); var box := BoxShape3D.new(); box.size = Vector3(4000, 1, 4000)
	cs.shape = box; cs.position = Vector3(0, -0.5, 0); ground.add_child(cs); root.add_child(ground)
	k = load(OS.get_environment("KNIGHT") if OS.has_environment("KNIGHT") else "res://scripts/knight.gd").new()
	k.setup(RIGHT, UP, FWD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	skel = k._skel; tree = k._tree
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	for bn in JOINTS: bi[bn] = skel.find_bone(bn)
	k.set_gear_stack(k.gear_stack_count() - 1)
	for i in 4: await process_frame
	var out := {"label": label, "figure_scale": float(k.get("_figure_scale"))}
	for side in ["l", "r"]:
		k.global_position = Vector3(0, 0.03, 0); k.velocity = Vector3.ZERO
		k.set_block(false)
		for i in 24: _step(Vector2.ZERO)
		k.set_block(true)
		for i in 24: _step(Vector2.ZERO)
		var dir := _strafe_input(side)
		var clip := String(k._roles.get("strafe_" + side, ""))
		var rows := []
		for i in 168:
			_step(dir)
			if i >= 36: rows.append(_sample())
		out[side] = _summarise(rows, side, clip)
		var r: Dictionary = out[side]
		print("[strafe] %-8s strafe_%s %-15s %.4f s | body %.3f m/s, asked %.1f px/s = %.3f m/s | in-scene foot-lock %.3f m/s (feet pinned at %.0f%% of the body speed) | support slide med %.1f p95 %.1f max %.1f mm (%d) | probe %d pairs med %.1f | wrap step %.2fx the median (%d wraps)"
			% [label, side, clip, float(r["clip_len"]), float(r["body_m_s"]), float(r["asked_px_s"]), float(r["asked_m_s"]), float(r["footlock_m_s"]),
			   100.0 * float(r["footlock_m_s"]) / maxf(float(r["body_m_s"]), 1e-6), float(r["support_med_mm"]), float(r["support_p95_mm"]),
			   float(r["support_max_mm"]), int(r["support_n"]), int(r["probe_n"]), float(r["probe_med_mm"]), float(r["wrap_frac"]), int(r["wraps"])])
		k.set_block(false)
		for i in 24: _step(Vector2.ZERO)
	var f := FileAccess.open(OS.get_environment("PROBE_OUT") if OS.has_environment("PROBE_OUT") else "/tmp/strafe_probe.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " ")); f.close()
	quit(0)

func _step(dir: Vector2) -> void:
	k.drive_dir(dir, false, DT)
	tree.advance(DT)
	skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)

func _strafe_input(side: String) -> Vector2:
	# guard_accept.gd's: the canvas direction along his strafe direction NOW
	var sd: Vector3 = k._strafe_dir(side)
	var want: Vector3 = (Basis(Vector3.UP, float(k.get("_yaw_cur"))) * sd).normalized()
	var best := -2.0; var pick := Vector2.ZERO
	for a in 720:
		var dd := Vector2(cos(deg_to_rad(0.5 * a)), sin(deg_to_rad(0.5 * a)))
		var w3: Vector3 = k.canvas_velocity_to_world(dd); w3.y = 0.0
		if w3.length() < 1e-6: continue
		var c: float = w3.normalized().dot(want)
		if c > best: best = c; pick = dd
	return pick

func _sample() -> Dictionary:
	var g := skel.global_transform
	var s := {"body": k.global_position, "pos": float(tree.get("parameters/a_strafe/current_position")), "asked": float(k.strafe_px_s())}
	for bn in JOINTS:
		s[bn] = g * skel.get_bone_global_pose(bi[bn]).origin
	return s

func _summarise(rows: Array, side: String, clip: String) -> Dictionary:
	var n := rows.size()
	var disp: Vector3 = (rows[-1]["body"] as Vector3) - (rows[0]["body"] as Vector3); disp.y = 0.0
	var dirw: Vector3 = disp.normalized()
	var body_v: float = disp.length() / (DT * float(n - 1))
	# the foot-lock as played: planted foot joints (their bottom 25%), velocity RELATIVE TO THE BODY
	var vs := []
	for fb in ["LeftFoot", "RightFoot"]:
		var lo := 1e9; var hi := -1e9
		for r in rows:
			var y: float = (r[fb] as Vector3).y - (r["body"] as Vector3).y
			lo = minf(lo, y); hi = maxf(hi, y)
		var thr: float = lo + 0.25 * (hi - lo)
		for i in range(1, n):
			var a: Dictionary = rows[i - 1]; var b: Dictionary = rows[i]
			var ya: float = (a[fb] as Vector3).y - (a["body"] as Vector3).y
			var yb: float = (b[fb] as Vector3).y - (b["body"] as Vector3).y
			if ya <= thr and yb <= thr:
				var rel: Vector3 = ((b[fb] as Vector3) - (b["body"] as Vector3)) - ((a[fb] as Vector3) - (a["body"] as Vector3))
				vs.append(-rel.dot(dirw) / DT)
	vs.sort()
	var fl: float = float(vs[vs.size() / 2]) if vs.size() > 0 else 0.0
	# slides
	var fy := 1e9
	for r in rows: fy = minf(fy, minf((r["LeftToeBase"] as Vector3).y, (r["RightToeBase"] as Vector3).y) - (r["body"] as Vector3).y)
	var sup := []; var prb := []
	for i in range(1, n):
		var a: Dictionary = rows[i - 1]; var b: Dictionary = rows[i]
		var la: bool = (a["LeftToeBase"] as Vector3).y <= (a["RightToeBase"] as Vector3).y
		var lb: bool = (b["LeftToeBase"] as Vector3).y <= (b["RightToeBase"] as Vector3).y
		if la != lb: continue
		var pa: Vector3 = a["LeftToeBase"] if la else a["RightToeBase"]
		var pb: Vector3 = b["LeftToeBase"] if lb else b["RightToeBase"]
		var d: Vector3 = pb - pa; d.y = 0.0
		sup.append(d.length() * 1000.0)
		var ha: float = pa.y - (a["body"] as Vector3).y; var hb: float = pb.y - (b["body"] as Vector3).y
		if ha <= fy + 0.03 and hb <= fy + 0.03 and absf(ha - hb) <= 0.010: prb.append(d.length() * 1000.0)
	sup.sort(); prb.sort()
	# the wrap: joint steps relative to the body, at the frames where the clip position goes backwards
	var steps := []; var wraps := []
	for i in range(1, n):
		var a2: Dictionary = rows[i - 1]; var b2: Dictionary = rows[i]
		var mx := 0.0
		for bn in JOINTS:
			var ra: Vector3 = (a2[bn] as Vector3) - (a2["body"] as Vector3)
			var rb: Vector3 = (b2[bn] as Vector3) - (b2["body"] as Vector3)
			mx = maxf(mx, (rb - ra).length())
		steps.append(mx)
		if float(b2["pos"]) < float(a2["pos"]): wraps.append(mx)
	var st2 := steps.duplicate(); st2.sort()
	var med: float = float(st2[st2.size() / 2])
	var wmax := 0.0
	for w in wraps: wmax = maxf(wmax, float(w))
	var asked: float = float(rows[n / 2]["asked"])
	return {"clip": clip, "clip_len": float(k._clip_len.get(clip, 0.0)), "frames": n, "body_m_s": body_v,
			"asked_px_s": asked, "asked_m_s": asked / (float(k.PPM) * float(k.get("_figure_scale"))),
			"footlock_m_s": fl, "footlock_n": vs.size(),
			"support_med_mm": float(sup[sup.size() / 2]) if sup.size() > 0 else -1.0,
			"support_p95_mm": float(sup[int(sup.size() * 0.95)]) if sup.size() > 0 else -1.0,
			"support_max_mm": float(sup[-1]) if sup.size() > 0 else -1.0, "support_n": sup.size(),
			"probe_n": prb.size(), "probe_med_mm": float(prb[prb.size() / 2]) if prb.size() > 0 else -1.0,
			"step_med_m": med, "wrap_frac": wmax / maxf(med, 1e-9), "wraps": wraps.size()}
