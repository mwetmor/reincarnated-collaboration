extends SceneTree
# THE COST AT 1080p, the way the game runs it: the tree in PHYSICS mode, the skeleton's
# modifiers in their default IDLE mode, real rendering at 1920x1080. Strikes and blocks fired
# in a loop so the lock is actually engaging. LAB_FOOTLOCK=0 for the same run without it.
# Reports frame time (wall clock between frames) and the process-time monitor, both in ms.
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
func _initialize() -> void:
	create_timer(300.0).timeout.connect(func(): push_error("LAB WATCHDOG"); quit(4))
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)   # or every frame reads 16.7 ms
	var ground := StaticBody3D.new()
	ground.collision_layer = CliffWorld.TERRAIN_BIT
	var cs := CollisionShape3D.new(); var box := BoxShape3D.new(); box.size = Vector3(600, 1, 600)
	cs.shape = box; cs.position = Vector3(0, -0.5, 0); ground.add_child(cs); root.add_child(ground)
	var mi := MeshInstance3D.new(); var pm := PlaneMesh.new(); pm.size = Vector2(60, 60); mi.mesh = pm; root.add_child(mi)
	var sun := DirectionalLight3D.new(); sun.rotation_degrees = Vector3(-50, 30, 0); sun.shadow_enabled = true; root.add_child(sun)
	var k: CharacterBody3D = load("res://scripts/knight.gd").new()
	k.setup(RIGHT, UP, FWD, 1.10)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	k.global_position = Vector3(0, 0.02, 0)
	var cam := Camera3D.new(); cam.projection = Camera3D.PROJECTION_ORTHOGONAL; cam.size = 10.8
	root.add_child(cam); cam.current = true
	cam.look_at_from_position(Vector3(0, 1, 0) - FWD * 60.0, Vector3(0, 1, 0), UP)
	var fl = k._foot_lock
	var label: String = "lock %s" % ("ON" if (fl != null and fl.enabled) else "OFF")
	for i in 60: await process_frame      # warm-up: shaders, first draws
	var frame_ms := []
	var proc_ms := []
	var lock_us := []
	var t_prev := Time.get_ticks_usec()
	var seq := ["slash", "block", "bash", "slash"]
	for i in 900:
		var phase: int = (i / 110) % seq.size()
		if i % 110 == 0:
			if seq[phase] == "block": k.set_block(true)
			else: k.try_strike(String(seq[phase]))
		if i % 110 == 70 and k._blocking: k.set_block(false)
		k.drive_dir(Vector2.ZERO, false, 1.0 / 60.0)
		await process_frame
		var now := Time.get_ticks_usec()
		frame_ms.append(float(now - t_prev) / 1000.0)
		t_prev = now
		proc_ms.append(Performance.get_monitor(Performance.TIME_PROCESS) * 1000.0)
		if fl != null: lock_us.append(float(fl.last_us))
	frame_ms.sort(); proc_ms.sort(); lock_us.sort()
	var mean := func(a: Array) -> float: return a.reduce(func(s, x): return s + float(x), 0.0) / maxf(float(a.size()), 1.0)
	print("[cost] %s at %s: frame %.3f ms mean (median %.3f, p95 %.3f) | process %.3f ms mean | planner %.1f us median, %.1f us p95"
		% [label, str(root.get_visible_rect().size), mean.call(frame_ms), float(frame_ms[frame_ms.size() / 2]),
		   float(frame_ms[int(frame_ms.size() * 0.95)]), mean.call(proc_ms),
		   float(lock_us[lock_us.size() / 2]) if lock_us.size() > 0 else 0.0,
		   float(lock_us[int(lock_us.size() * 0.95)]) if lock_us.size() > 0 else 0.0])
	quit(0)
