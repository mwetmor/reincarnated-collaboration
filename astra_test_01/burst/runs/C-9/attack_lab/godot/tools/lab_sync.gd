extends SceneTree
# Do the block and strafe clips run off their ends while nobody is blocking?
# blk and strf are Blend2s with sync = true, which ADVANCES an input even at zero weight,
# and neither the block clip nor the strafes are in the loop list. If so, by the time he
# blocks or side-steps, the clip is parked on its last frame: a frozen strafe slides the
# body over still legs, and the block shows wherever Block1 happens to end.
const DT := 1.0 / 24.0
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
func _initialize() -> void:
	# WATCHDOG. A SceneTree script whose coroutine dies on an error never reaches quit(), and
	# this one runs under the SHARED heavy lock: on 2026-09-29 a null load killed stance.gd
	# mid-await and it held the lock for ten minutes with the integration build queued behind
	# it. A timer on the main loop fires whether or not the coroutine is alive.
	create_timer(float(OS.get_environment("LAB_WATCHDOG_S")) if OS.has_environment("LAB_WATCHDOG_S") else 240.0).timeout.connect(func(): push_error("LAB WATCHDOG: quitting a hung script"); quit(4))
	var ground := StaticBody3D.new()
	ground.collision_layer = CliffWorld.TERRAIN_BIT
	var cs := CollisionShape3D.new(); var box := BoxShape3D.new(); box.size = Vector3(600, 1, 600)
	cs.shape = box; cs.position = Vector3(0, -0.5, 0); ground.add_child(cs); root.add_child(ground)
	var k: CharacterBody3D = load("res://scripts/knight.gd").new()
	k.setup(RIGHT, UP, FWD, 1.10)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	var tree: AnimationTree = k._tree
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	k.set_gear_stack(k.gear_stack_count() - 1)
	k.global_position = Vector3(0, 0.02, 0)
	var skel: Skeleton3D = k._skel
	var sl: String = String(k._roles.get("strafe_l", ""))
	var bl: String = String(k._roles.get("block", ""))
	print("[sync] strafe_l '%s' %.3f s loop=%d | block '%s' %.3f s loop=%d" % [sl, float(k._clip_len.get(sl, 0.0)),
		k._anim.get_animation(sl).loop_mode, bl, float(k._clip_len.get(bl, 0.0)), k._anim.get_animation(bl).loop_mode])
	for i in int(4.0 / DT):
		k.drive_dir(Vector2.ZERO, false, DT); tree.advance(DT)
	print("[sync] after 4 s standing: a_strafe at %.3f s, a_block at %.3f s" % [
		float(tree.get("parameters/a_strafe/current_position")), float(tree.get("parameters/a_block/current_position"))])
	k.set_block(true)
	var pb0: float = float(tree.get("parameters/a_block/current_position"))
	for i in 12:
		k.drive_dir(Vector2.ZERO, false, DT); tree.advance(DT)
	print("[sync] block pressed: a_block %.3f s -> %.3f s after 0.5 s (a clip that is PLAYING moves)" % [
		pb0, float(tree.get("parameters/a_block/current_position"))])
	# strafe toward his left for 3 s
	# EIGHT directions, not four: the canvas basis is rotated ~47 deg against the world, so
	# four cardinals can all miss a 0.6 cone -- which is why the first run never strafed
	var left_canvas := Vector2.ZERO
	var best := 0.0
	for j in 8:
		var d := Vector2.from_angle(TAU * float(j) / 8.0)
		var wdir: Vector3 = k.canvas_velocity_to_world(d).normalized()
		var loc: Vector3 = (Basis(Vector3.UP, k._yaw_cur).inverse() * wdir).normalized()
		var dd: float = loc.dot(k._strafe_dir("l"))
		if dd > best:
			best = dd
			left_canvas = d
	print("[sync] strafe-left input %s, cos %.2f to his left" % [str(left_canvas), best])
	var feet := []
	var body0: Vector3 = k.global_position
	var prev := Vector3.ZERO
	var legs_moved := 0.0
	var prevpose := Transform3D()
	for i in int(3.0 / DT):
		k.drive_dir(left_canvas, false, DT); tree.advance(DT)
		if i < 3:
			var wd: Vector3 = k.canvas_velocity_to_world(left_canvas).normalized()
			var lc: Vector3 = (Basis(Vector3.UP, k._yaw_cur).inverse() * wd).normalized()
			print("[sync]   frame %d: blocking=%s strafing=%s side=%s w=%.2f dot_l=%.2f dir_l=%s dir_r=%s speed=%.1f" % [i,
				str(k._blocking), str(k._strafing), k._strafe_side, k._strafe_w, lc.dot(k._strafe_dir("l")),
				str(k._strafe_dir("l")), str(k._strafe_dir("r")), k.speed_px_s()])
		var lf: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone("LeftToeBase")).origin
		var rf: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone("RightToeBase")).origin
		var lo: Vector3 = lf if lf.y <= rf.y else rf
		if i > 0: feet.append((lo - prev).length() * 1000.0)
		prev = lo
		var pose: Transform3D = skel.get_bone_pose(skel.find_bone("LeftUpLeg"))
		if i > 0: legs_moved += rad_to_deg(pose.basis.get_rotation_quaternion().angle_to(prevpose.basis.get_rotation_quaternion()))
		prevpose = pose
	feet.sort()
	print("[sync] strafing=%s for 3 s: body moved %.3f m; lower foot median %.1f mm/frame; left thigh rotated %.1f deg total; a_strafe at %.3f s"
		% [str(k._strafing), (k.global_position - body0).length(), float(feet[feet.size() / 2]), legs_moved,
		   float(tree.get("parameters/a_strafe/current_position"))])
	quit(0)
