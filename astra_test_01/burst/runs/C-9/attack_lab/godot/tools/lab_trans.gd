extends SceneTree
# The transitions numbers, in the lab, on flat ground -- the same planted-foot instrument
# as cliffside3d/tools/probe_transitions.gd (same foot, both ends in contact, height
# unchanged, on the floor), stepped at 1/24 s like the numbers it is compared with. The
# cliffside scene cannot be run while the integration build is in there, so before/after
# is measured HERE, both sides with this one instrument.
const DT := 1.0 / 24.0
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
var k: CharacterBody3D
var skel: Skeleton3D
var tree: AnimationTree
var out := {}

func _initialize() -> void:
	# WATCHDOG. A SceneTree script whose coroutine dies on an error never reaches quit(), and
	# this one runs under the SHARED heavy lock: on 2026-09-29 a null load killed stance.gd
	# mid-await and it held the lock for ten minutes with the integration build queued behind
	# it. A timer on the main loop fires whether or not the coroutine is alive.
	create_timer(float(OS.get_environment("LAB_WATCHDOG_S")) if OS.has_environment("LAB_WATCHDOG_S") else 240.0).timeout.connect(func(): push_error("LAB WATCHDOG: quitting a hung script"); quit(4))
	var ground := StaticBody3D.new()
	ground.collision_layer = CliffWorld.TERRAIN_BIT
	var cs := CollisionShape3D.new()
	var box := BoxShape3D.new()
	box.size = Vector3(600, 1, 600)
	cs.shape = box
	cs.position = Vector3(0, -0.5, 0)
	ground.add_child(cs)
	root.add_child(ground)
	k = load("res://scripts/knight.gd").new()
	k.setup(RIGHT, UP, FWD, 1.10)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	skel = k._skel
	tree = k._tree
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	k.set_gear_stack(k.gear_stack_count() - 1)
	print("[trans] armed=%s walk %.1f run %.1f px/s" % [str(k.armed()), k.walk_px_s(), k.run_px_s()])
	for run in [false, true]:
		await _place()
		for i in 30:
			_step(Vector2(1, 0), run)
		var rows := []
		var settled := -1
		var n := 0
		var pl := -1
		var pf := Vector3.ZERO
		var ph := 1e9
		while n < 60:
			_step(Vector2.ZERO, false)
			n += 1
			var r := _foot()
			if int(r[0]) == pl and k.is_on_floor():
				rows.append([((r[1] as Vector3) - pf).length(), float(r[2]), ph])
			pl = int(r[0]); pf = r[1]; ph = float(r[2])
			if settled < 0 and k.speed_px_s() <= 0.0:
				settled = n
			if settled > 0 and n > settled + 4:
				break
		var res := _planted(rows)
		res["stop_s"] = snappedf(float(settled) * DT, 0.01)
		out["stop_from_" + ("run" if run else "walk")] = res
		print("[trans] stop from %s: %.2f s, planted median %.1f mm, worst %.1f mm (%d of %d)"
			% ["run" if run else "walk", float(settled) * DT, float(res["median_mm"]), float(res["worst_mm"]), int(res["n"]), rows.size()])
	await _place()
	var rows2 := []
	var pl2 := -1
	var pf2 := Vector3.ZERO
	var ph2 := 1e9
	for leg in [[false, 22, 1.0], [true, 26, 1.0], [false, 22, -1.0], [true, 26, -1.0]]:
		for i in int(leg[1]):
			_step(Vector2(float(leg[2]), 0), bool(leg[0]))
			var r2 := _foot()
			if int(r2[0]) == pl2 and k.is_on_floor():
				var tv: float = ((r2[1] as Vector3) - pf2).length()
				rows2.append([tv, float(r2[2]), ph2])
				if tv > 0.25:
					print("[trans]   big pair: leg %s frame %d, %.1f mm, speed %.1f px/s, w %.3f, dh %.4f" % [
						"run" if bool(leg[0]) else "walk", i, tv * 1000.0, k.speed_px_s(),
						float(tree.get("parameters/bl_wr/blend_amount")), absf(float(r2[2]) - ph2)])
			pl2 = int(r2[0]); pf2 = r2[1]; ph2 = float(r2[2])
	var res2 := _planted(rows2)
	out["walk_run_walk"] = res2
	print("[trans] walk<->run: planted median %.1f mm, worst %.1f mm (%d of %d)"
		% [float(res2["median_mm"]), float(res2["worst_mm"]), int(res2["n"]), rows2.size()])
	var f := FileAccess.open(String(OS.get_cmdline_user_args()[0]) if OS.get_cmdline_user_args().size() > 0 else "/tmp/lab_trans.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " "))
	f.close()
	quit(0)

func _place() -> void:
	k.global_position = Vector3(0, 0.02, 0)
	k.velocity = Vector3.ZERO
	for i in 3:
		_step(Vector2.ZERO, false)
	await process_frame

func _step(dir: Vector2, run: bool) -> void:
	k.drive_dir(dir, run, DT)
	tree.advance(DT)

func _foot() -> Array:
	var lf: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone("LeftToeBase")).origin
	var rf: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone("RightToeBase")).origin
	var low: int = 0 if lf.y <= rf.y else 1
	var foot: Vector3 = lf if low == 0 else rf
	return [low, foot, foot.y - k.global_position.y]

func _planted(rows: Array) -> Dictionary:
	var lo := 1e9
	for r in rows:
		lo = minf(lo, float(r[1]))
	var p := []
	for r in rows:
		if float(r[1]) <= lo + 0.03 and float(r[2]) <= lo + 0.03 and absf(float(r[1]) - float(r[2])) <= 0.010:
			p.append(float(r[0]) * 1000.0)
	p.sort()
	return {"median_mm": snappedf(float(p[p.size() / 2]) if p.size() > 0 else -1.0, 0.1),
			"worst_mm": snappedf(float(p[-1]) if p.size() > 0 else -1.0, 0.1), "n": p.size(),
			"all_mm": p.map(func(x): return snappedf(x, 0.1))}
