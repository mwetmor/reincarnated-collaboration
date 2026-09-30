extends SceneTree
func _initialize() -> void:
	create_timer(90.0).timeout.connect(func(): quit(4))
	for mode in ["IDLE", "MANUAL"]:
		var ps := ResourceLoader.load("res://models/gear/nb-body.glb", "", ResourceLoader.CACHE_MODE_IGNORE_DEEP) as PackedScene
		var r := ps.instantiate()
		root.add_child(r)
		await process_frame
		var sk: Skeleton3D = r.find_children("*", "Skeleton3D", true, false)[0]
		var foot := sk.find_bone("LeftFoot")
		var before: Vector3 = sk.global_transform * sk.get_bone_global_pose(foot).origin
		var tgt := Node3D.new(); root.add_child(tgt)
		tgt.global_position = before + Vector3(0.25, 0.20, 0.0)
		var ik := TwoBoneIK3D.new()
		sk.add_child(ik)
		ik.setting_count = 1
		ik.set_root_bone_name(0, "LeftUpLeg"); ik.set_middle_bone_name(0, "LeftLeg"); ik.set_end_bone_name(0, "LeftFoot")
		ik.set_target_node(0, ik.get_path_to(tgt))
		var st := {"ran": 0, "in_sig": Vector3.INF}
		ik.modification_processed.connect(func():
			st["ran"] = int(st["ran"]) + 1
			st["in_sig"] = sk.global_transform * sk.get_bone_global_pose(foot).origin)
		var up := {"n": 0}
		sk.skeleton_updated.connect(func(): up["n"] = int(up["n"]) + 1)
		if mode == "MANUAL":
			sk.modifier_callback_mode_process = Skeleton3D.MODIFIER_CALLBACK_MODE_PROCESS_MANUAL
			for i in 3:
				sk.advance(1.0 / 60.0)
				await process_frame
		else:
			for i in 5:
				await process_frame
		var after: Vector3 = sk.global_transform * sk.get_bone_global_pose(foot).origin
		print("[ik3] %s: modifier ran %d times, skeleton_updated %d | foot before %s, IN the signal %s (moved %.3f m), after the frame %s"
			% [mode, int(st["ran"]), int(up["n"]), str(before.snappedf(0.001)), str((st["in_sig"] as Vector3).snappedf(0.001)),
			   ((st["in_sig"] as Vector3) - before).length() if st["in_sig"] != Vector3.INF else -1.0, str(after.snappedf(0.001))])
		print("[ik3]   target world %s, ik path %s valid=%s" % [str(tgt.global_position.snappedf(0.001)), str(ik.get_target_node(0)), str(ik.get_node_or_null(ik.get_target_node(0)) != null)])
		r.queue_free()
		await process_frame
	quit(0)
