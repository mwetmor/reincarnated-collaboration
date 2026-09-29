extends SceneTree
# What is the FLOOR? Play each locomotion clip alone, at its own authored rate, with the
# body advanced at exactly that clip's stride-derived speed -- no blending, no sync group,
# nothing this session wrote. Whatever stance-foot travel remains is the CLIP's, and no
# runtime blend can go below it. That is the number a target has to be compared against.
const DT := 1.0 / 24.0
const SPOT := Vector2(2285.62, 2407.32)
func _initialize():
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60: await process_frame
	Engine.physics_ticks_per_second = 24
	var k = scene.knight
	k.set_physics_process(false)
	var skel: Skeleton3D = k._skel
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var lt := skel.find_bone("LeftToeBase")
	var rt := skel.find_bone("RightToeBase")
	for spec in [["walk", false], ["run", true]]:
		var g := CliffWorld.ground_at(space, SPOT, scene.right, scene.up, scene.fwd)
		k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.05
		k.velocity = Vector3.ZERO
		# reach steady state at this gait, then sample two full cycles
		for i in 14:
			k.drive_dir(Vector2(1, 0), bool(spec[1]), DT)
			await physics_frame
		var pl := -1
		var pf := Vector3.ZERO
		var ph := 1e9
		var pb: Vector3 = k.global_position
		var rows := []
		for i in 44:
			k.drive_dir(Vector2(-1.0 if i >= 22 else 1.0, 0), bool(spec[1]), DT)
			await physics_frame
			var lf: Vector3 = skel.global_transform * skel.get_bone_global_pose(lt).origin
			var rf: Vector3 = skel.global_transform * skel.get_bone_global_pose(rt).origin
			var low: int = 0 if lf.y <= rf.y else 1
			var foot: Vector3 = lf if low == 0 else rf
			var h: float = foot.y - k.global_position.y
			if low == pl and k.is_on_floor():
				rows.append([(foot - pf).length(), h, ph])
			pl = low; pf = foot; ph = h; pb = k.global_position
		if rows.size() == 0:
			print("  %s: NO GROUNDED PAIRS -- he left the plateau" % spec[0]); continue
		var mn := 1e9
		for r in rows: mn = minf(mn, float(r[1]))
		# the single best pair in each cycle: the frame the clip actually plants
		var best := []
		var all := []
		for r in rows:
			all.append(float(r[0]))
			if float(r[1]) <= mn + 0.03 and float(r[2]) <= mn + 0.03:
				best.append(float(r[0]))
		all.sort(); best.sort()
		print("  %s: speed %.1f px/s, %d pairs" % [spec[0], k.speed_px_s(), rows.size()])
		print("     ALL lower-foot pairs:  min %.4f  median %.4f  max %.4f m/frame" %
			[all[0], all[all.size()/2], all[-1]])
		if best.size() > 0:
			print("     band-planted pairs:    n=%d  min %.4f  median %.4f  max %.4f m/frame" %
				[best.size(), best[0], best[best.size()/2], best[-1]])
		# how still does the stillest foot in each cycle get?
		var under := 0
		for a in all:
			if a < 0.010: under += 1
		print("     pairs under 10 mm: %d of %d   (floor_y %.4f)" % [under, all.size(), mn])
	quit(0)
