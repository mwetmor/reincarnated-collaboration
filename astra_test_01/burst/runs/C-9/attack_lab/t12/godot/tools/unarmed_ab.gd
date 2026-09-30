extends SceneTree
# Is the UNARMED barbarian untouched by the split? The installed knight and the split knight,
# side by side, the same inputs, unarmed (stack 0): every bone's position compared per frame.
const DT := 1.0 / 24.0
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
func _initialize() -> void:
	create_timer(300.0).timeout.connect(func(): push_error("WATCHDOG"); quit(4))
	var ground := StaticBody3D.new()
	ground.collision_layer = CliffWorld.TERRAIN_BIT
	var cs := CollisionShape3D.new(); var box := BoxShape3D.new(); box.size = Vector3(4000, 1, 4000)
	cs.shape = box; cs.position = Vector3(0, -0.5, 0); ground.add_child(cs); root.add_child(ground)
	var ks := []
	for p in ["res://scripts/knight_before.gd", "res://scripts/knight.gd"]:
		var k = load(p).new()
		k.setup(RIGHT, UP, FWD, 1.0)
		root.add_child(k)
		ks.append(k)
	for i in 6: await process_frame
	for i in 2:
		ks[i].set_physics_process(false)
		ks[i].set_gear_stack(0)
		ks[i].global_position = Vector3(float(i) * 5.0, 0.03, 0)
		(ks[i]._tree as AnimationTree).callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var worst := 0.0
	var n := 0
	for seg in [[24, Vector2.ZERO, false], [96, Vector2(1, 0), false], [96, Vector2(1, 0), true], [36, Vector2.ZERO, false],
				[22, Vector2(1, 0), false], [26, Vector2(1, 0), true], [22, Vector2(1, 0), false], [26, Vector2(1, 0), true]]:
		for j in int(seg[0]):
			for i in 2:
				ks[i].drive_dir(seg[1], bool(seg[2]), DT)
				(ks[i]._tree as AnimationTree).advance(DT)
			var s0: Skeleton3D = ks[0]._skel; var s1: Skeleton3D = ks[1]._skel
			for b in s0.get_bone_count():
				var p0: Vector3 = s0.get_bone_global_pose(b).origin
				var p1: Vector3 = s1.get_bone_global_pose(b).origin
				worst = maxf(worst, (p0 - p1).length() * s0.global_transform.basis.get_scale().x)
			n += 1
	print("[unarmed_ab] %d frames: worst bone-position difference installed vs split, unarmed = %.6f m" % [n, worst])
	quit(0)
