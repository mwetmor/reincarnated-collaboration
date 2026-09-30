extends SceneTree
func _initialize() -> void:
	create_timer(90.0).timeout.connect(func(): quit(4))
	for variant in ["control_rot45", "ik_no_pole", "ik_pole_node", "ik_pole_dir"]:
		var ps := ResourceLoader.load("res://models/gear/nb-body.glb", "", ResourceLoader.CACHE_MODE_IGNORE_DEEP) as PackedScene
		var r := ps.instantiate()
		root.add_child(r)
		await process_frame
		var sk: Skeleton3D = r.find_children("*", "Skeleton3D", true, false)[0]
		sk.modifier_callback_mode_process = Skeleton3D.MODIFIER_CALLBACK_MODE_PROCESS_MANUAL
		var foot := sk.find_bone("LeftFoot")
		var before: Vector3 = sk.global_transform * sk.get_bone_global_pose(foot).origin
		var m: SkeletonModifier3D
		if variant == "control_rot45":
			m = SkeletonModifier3D.new()
			m.set_script(load("res://tools/ik_rot45.gd"))
			sk.add_child(m)
		else:
			var tgt := Node3D.new(); root.add_child(tgt)
			tgt.global_position = before + Vector3(0.25, 0.20, 0.0)
			var ik := TwoBoneIK3D.new()
			sk.add_child(ik)
			ik.setting_count = 1
			ik.set_root_bone_name(0, "LeftUpLeg"); ik.set_middle_bone_name(0, "LeftLeg"); ik.set_end_bone_name(0, "LeftFoot")
			ik.set_target_node(0, ik.get_path_to(tgt))
			if variant == "ik_pole_node":
				var pole := Node3D.new(); root.add_child(pole)
				var knee: Vector3 = sk.global_transform * sk.get_bone_global_pose(sk.find_bone("LeftLeg")).origin
				pole.global_position = knee + Vector3(0, 0, 1.0)
				ik.set_pole_node(0, ik.get_path_to(pole))
			elif variant == "ik_pole_dir":
				ik.set_pole_direction(0, 4)
			m = ik
		var st := {"in_sig": Vector3.INF}
		m.modification_processed.connect(func(): st["in_sig"] = sk.global_transform * sk.get_bone_global_pose(foot).origin)
		sk.advance(1.0 / 60.0)
		await process_frame
		var s: Vector3 = st["in_sig"]
		print("[ik4] %-14s foot moved %.3f m in the signal (%s -> %s)" % [variant, (s - before).length() if s != Vector3.INF else -1.0, str(before.snappedf(0.001)), str(s.snappedf(0.001))])
		r.queue_free()
		await process_frame
	quit(0)
