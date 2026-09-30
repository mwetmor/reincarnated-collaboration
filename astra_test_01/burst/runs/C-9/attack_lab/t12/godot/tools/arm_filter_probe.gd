extends SceneTree
# T12_11 SHIELD ARM LAYER, DECLARED-SET FILTER -- does anything change under the EDITOR import? Two knights (KNIGHTS env,
# comma list of res:// scripts), the same character file and body. For each: the arm layer's Blend2 ("blend") filter as
# built -- every path of every clip, filtered or not -- and the left arm's pose through the tree, frame by frame, over
# idle, walk, run and block (1/60 s). CASE guard: the running configuration (arm_layer_armed = shield_guard_L). CASE carry:
# arm_layer_armed erased from the config and the clip set re-applied (_apply_clip_set), so the retired shield_carry_L
# is the layer -- the clip whose shoulder and wrist tracks a runtime import drops.
# env: KNIGHTS, KNIGHT_CHARACTER (knight_t12_10.gd reads it), PROBE_OUT
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
const ARM := ["LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand"]
const DT := 1.0 / 60.0

func _initialize() -> void:
	var ground := StaticBody3D.new()
	ground.collision_layer = CliffWorld.TERRAIN_BIT
	var cs := CollisionShape3D.new(); var box := BoxShape3D.new(); box.size = Vector3(4000, 1, 4000)
	cs.shape = box; cs.position = Vector3(0, -0.5, 0); ground.add_child(cs); root.add_child(ground)
	var out := {}
	var ki := 0
	for kp in OS.get_environment("KNIGHTS").split(","):
		ki += 1
		for case_ in ["guard", "carry"]:
			var k = load(kp).new()
			k.setup(RIGHT, UP, FWD, 1.0)
			root.add_child(k)
			for i in 6: await process_frame
			k.set_physics_process(false)
			if k.has_method("trail_step"): k.trail_auto = false
			k.set_gear_stack(k.gear_stack_count() - 1)
			for i in 4: await process_frame
			if case_ == "carry":
				(k.cfg as Dictionary).erase("arm_layer_armed")
				k._apply_clip_set()
			var tree: AnimationTree = k._tree
			tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
			var bt := tree.tree_root as AnimationNodeBlendTree
			var b2 := bt.get_node("blend") as AnimationNodeBlend2
			var carry := String((bt.get_node("carry") as AnimationNodeAnimation).animation)
			var filt := []
			var ap: AnimationPlayer = k._anim
			var seen := {}
			for cn in ap.get_animation_list():
				var a := ap.get_animation(cn)
				for i in a.get_track_count():
					var p := String(a.track_get_path(i))
					if seen.has(p): continue
					seen[p] = true
					if b2.is_path_filtered(NodePath(p)): filt.append(p)
			filt.sort()
			var skel: Skeleton3D = k._skel
			var poses := []
			# the SAME phase for every knight: the tree was running on its own until the manual switch -- every clip back to 0
			k.global_position = Vector3(0, 0.03, 0); k.velocity = Vector3.ZERO
			tree.active = false
			tree.active = true
			var plan := [[Vector2.ZERO, false, false, 1.0], [Vector2(1, 0), false, false, 2.0], [Vector2(1, 0), true, false, 2.0], [Vector2.ZERO, false, false, 0.7], [Vector2.ZERO, false, true, 1.5], [Vector2.ZERO, false, false, 0.8]]
			for st in plan:
				k.set_block(bool(st[2]))
				for j in int(round(float(st[3]) / DT)):
					k.drive_dir(st[0], bool(st[1]), DT)
					tree.advance(DT)
					skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)
					var row := []
					for bn in ARM:
						var q := skel.get_bone_global_pose(skel.find_bone(bn)).basis.orthonormalized().get_rotation_quaternion()
						row.append([q.x, q.y, q.z, q.w])
					poses.append(row)
			out["%d:%s|%s" % [ki, kp, case_]] = {"layer_clip": carry, "filtered_paths": filt, "poses": poses}
			print("[armf] %s %s: layer '%s', %d filtered paths %s, %d frames" % [kp, case_, carry, filt.size(), str(filt), poses.size()])
			k.queue_free()
			for i in 3: await process_frame
	var f := FileAccess.open(OS.get_environment("PROBE_OUT"), FileAccess.WRITE)
	f.store_string(JSON.stringify(out)); f.close()
	quit(0)
