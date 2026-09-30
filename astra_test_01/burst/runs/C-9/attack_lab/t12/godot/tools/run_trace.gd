extends SceneTree
# THE STEADY RUN, frame by frame, as tools/speed_split.gd drives it (the open item: its planted-foot
# slide median rose 14 -> 23 mm/frame from T12_8 to T12_9). Unarmed (stack 0) and armed (the full kit),
# figure scale 1.0, 1/24 s: 24 standing steps, 96 run steps; rows from step 36 on, as the probe does.
# Per row: the run clip's playback position, the walk/run weight, the locked cycle, ts_run's scale,
# the body, and both toes (world). Offline, the rows are compared with the raw clip sampled at the
# same position (nb_d2 scratch analysis).
# env: KNIGHT, KNIGHT_CHARACTER, TRACE_LABEL, TRACE_OUT
const DT := 1.0 / 24.0
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
var k
var skel: Skeleton3D
var tree: AnimationTree

func _initialize() -> void:
	var label: String = OS.get_environment("TRACE_LABEL") if OS.has_environment("TRACE_LABEL") else "?"
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
	var lt := skel.find_bone("LeftToeBase"); var rt := skel.find_bone("RightToeBase")
	var out := {"label": label, "run_clip": String(k._roles.get("run", "")), "run_len": float(k.get("_run_len")),
				"walk_len": float(k.get("_walk_len")), "skel_global": _tx(skel.global_transform)}
	for st in [["unarmed", 0], ["armed", k.gear_stack_count() - 1]]:
		k.set_gear_stack(int(st[1]))
		k.global_position = Vector3(0, 0.03, 0); k.velocity = Vector3.ZERO
		for i in 24: _step(Vector2.ZERO, false)
		var rows := []
		for i in 96:
			_step(Vector2(1, 0), true)
			if i >= 36:
				var g := skel.global_transform
				rows.append({"pos": float(tree.get("parameters/a_run/current_position")), "w": float(tree.get("parameters/bl_wr/blend_amount")),
							 "cyc": float(k.get("_cycle_len")), "ts": float(tree.get("parameters/ts_run/scale")),
							 "body": _v(k.global_position), "lt": _v(g * skel.get_bone_global_pose(lt).origin), "rt": _v(g * skel.get_bone_global_pose(rt).origin),
							 "skel": _tx(g)})
		out[st[0]] = rows
		for i in 36: _step(Vector2.ZERO, false)
	var f := FileAccess.open(OS.get_environment("TRACE_OUT") if OS.has_environment("TRACE_OUT") else "/tmp/run_trace.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out)); f.close()
	print("[trace] %s: run clip %s (%.4f s), %d rows per state" % [label, out["run_clip"], float(out["run_len"]), 60])
	quit(0)

func _step(dir: Vector2, run: bool) -> void:
	k.drive_dir(dir, run, DT)
	tree.advance(DT)
	skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)

func _v(p: Vector3) -> Array:
	return [p.x, p.y, p.z]

func _tx(t: Transform3D) -> Array:
	return [t.basis.x.x, t.basis.x.y, t.basis.x.z, t.basis.y.x, t.basis.y.y, t.basis.y.z, t.basis.z.x, t.basis.z.y, t.basis.z.z, t.origin.x, t.origin.y, t.origin.z]
