extends SceneTree
# The run stop is the last leg above target. Which frames carry it, and is the foot
# the probe calls "planted" actually on the ground on BOTH frames of the pair?
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
	var tree: AnimationTree = k._tree
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var g := CliffWorld.ground_at(space, SPOT, scene.right, scene.up, scene.fwd)
	k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.05
	k.velocity = Vector3.ZERO
	var lt := skel.find_bone("LeftToeBase")
	var rt := skel.find_bone("RightToeBase")
	for i in 30: 
		k.drive_dir(Vector2(1, 0), true, DT)
		await physics_frame
	var rows := []
	var pl := -1
	var pf := Vector3.ZERO
	var ph := 1e9
	var pb: Vector3 = k.global_position
	for i in 20:
		k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
		var lf: Vector3 = skel.global_transform * skel.get_bone_global_pose(lt).origin
		var rf: Vector3 = skel.global_transform * skel.get_bone_global_pose(rt).origin
		var low: int = 0 if lf.y <= rf.y else 1
		var foot: Vector3 = lf if low == 0 else rf
		var h: float = foot.y - k.global_position.y
		rows.append([i, k.speed_px_s(), float(tree.get("parameters/bl_iw/blend_amount")),
			float(tree.get("parameters/bl_wr/blend_amount")), low,
			(foot - pf).length() if low == pl else -1.0, (k.global_position - pb).length(),
			h, ph, lf.y - k.global_position.y, rf.y - k.global_position.y])
		pl = low; pf = foot; ph = h; pb = k.global_position
	var mn := 1e9
	for r in rows: mn = minf(mn, float(r[7]))
	print("  floor_y (lowest foot height above root over the leg) = %.4f m" % mn)
	print("  fr  speed     a      w  low  footd  bodyd     h   prev_h  planted?   Lh     Rh")
	for r in rows:
		var ok: bool = float(r[5]) >= 0.0 and float(r[7]) <= mn + 0.03 and float(r[8]) <= mn + 0.03
		print("  %2d %6.1f  %.3f  %.3f   %d %6.3f %6.3f %6.3f %8.3f   %-8s %6.3f %6.3f" %
			[r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], minf(float(r[8]), 9.999),
			 "YES" if ok else "no", r[9], r[10]])
	quit(0)
