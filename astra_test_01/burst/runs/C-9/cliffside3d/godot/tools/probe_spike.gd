extends SceneTree
# Which frame carries the 1.1 m foot step, and what else is happening on it?
const DT := 1.0 / 24.0
const SPOT := Vector2(2285.62, 2407.32)
func _initialize():
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60: await process_frame
	Engine.physics_ticks_per_second = 24
	var k = scene.knight
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	var skel: Skeleton3D = k._skel
	var tree: AnimationTree = k._tree
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var g := CliffWorld.ground_at(space, SPOT, scene.right, scene.up, scene.fwd)
	k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.05
	k.velocity = Vector3.ZERO
	var lt := skel.find_bone("LeftToeBase")
	var rt := skel.find_bone("RightToeBase")
	var pl := -1
	var pf := Vector3.ZERO
	var pbody: Vector3 = k.global_position
	var f := 0
	print("  fr  leg    speed     a      w   tsW   tsR  runpos  low  footd  bodyd (expect bodyd=speed/24/100.6)")
	for leg in [["walk", false, 22, 1.0], ["run", true, 26, 1.0],
				["walk", false, 22, -1.0], ["run", true, 26, -1.0]]:
		for i in int(leg[2]):
			k.drive_dir(Vector2(float(leg[3]), 0), bool(leg[1]), DT)
			await physics_frame
			f += 1
			var lf: Vector3 = skel.global_transform * skel.get_bone_global_pose(lt).origin
			var rf: Vector3 = skel.global_transform * skel.get_bone_global_pose(rt).origin
			var low: int = 0 if lf.y <= rf.y else 1
			var foot: Vector3 = lf if low == 0 else rf
			var fd: float = (foot - pf).length() if (low == pl and k.is_on_floor()) else -1.0
			var bd: float = (k.global_position - pbody).length()
			if fd > 0.05 or f % 12 == 0:
				print("  %3d  %-5s %6.1f  %.3f  %.3f  %.3f  %.3f  %6.3f   %d  %6.3f %6.3f%s" %
					[f, String(leg[0]), k.speed_px_s(),
					 float(tree.get("parameters/bl_iw/blend_amount")),
					 float(tree.get("parameters/bl_wr/blend_amount")),
					 float(tree.get("parameters/ts_walk/scale")),
					 float(tree.get("parameters/ts_run/scale")),
					 float(tree.get("parameters/a_run/current_position")),
					 low, fd, bd, "   <--" if fd > 0.05 else ""])
			pl = low
			pf = foot
			pbody = k.global_position
	quit(0)
