extends SceneTree
# Does TwoBoneIK3D move a leg, and HOW do I read the result -- get_bone_global_pose after
# skel.advance(), the modification_processed signal, or a ModifierBoneTarget3D?
func _initialize() -> void:
	create_timer(90.0).timeout.connect(func(): quit(4))
	for c in ["TwoBoneIK3D", "SkeletonModifier3D", "ModifierBoneTarget3D"]:
		var ms := []
		for m in ClassDB.class_get_method_list(c, true):
			var n: String = m["name"]
			if n.begins_with("set_") or n in ["advance"]:
				var args := []
				for a in m["args"]: args.append("%s:%s" % [a["name"], type_string(int(a["type"]))])
				ms.append("%s(%s)" % [n, ", ".join(args)])
		print("[ik2] %s: %s" % [c, "; ".join(ms)])
	var sigs := []
	for s in ClassDB.class_get_signal_list("Skeleton3D", false): sigs.append(String(s["name"]))
	for s in ClassDB.class_get_signal_list("SkeletonModifier3D", false): sigs.append("mod:" + String(s["name"]))
	print("[ik2] signals: %s" % str(sigs))
	var ps := ResourceLoader.load("res://models/gear/nb-body.glb", "", ResourceLoader.CACHE_MODE_IGNORE_DEEP) as PackedScene
	var r := ps.instantiate()
	root.add_child(r)
	await process_frame
	var sk: Skeleton3D = r.find_children("*", "Skeleton3D", true, false)[0]
	sk.modifier_callback_mode_process = Skeleton3D.MODIFIER_CALLBACK_MODE_PROCESS_MANUAL
	var foot := sk.find_bone("LeftFoot")
	var before: Vector3 = sk.global_transform * sk.get_bone_global_pose(foot).origin
	var tgt := Node3D.new(); root.add_child(tgt)
	tgt.global_position = before + Vector3(0.25, 0.20, 0.0)
	var ik := TwoBoneIK3D.new()
	sk.add_child(ik)
	ik.setting_count = 1
	ik.set_root_bone_name(0, "LeftUpLeg"); ik.set_middle_bone_name(0, "LeftLeg"); ik.set_end_bone_name(0, "LeftFoot")
	ik.set_target_node(0, ik.get_path_to(tgt))
	var mbt := ModifierBoneTarget3D.new()
	sk.add_child(mbt)
	mbt.set("bone_name", "LeftFoot")
	var got := {"sig": Vector3.INF}
	sk.skeleton_updated.connect(func(): got["sig"] = sk.global_transform * sk.get_bone_global_pose(foot).origin)
	sk.advance(1.0 / 60.0)
	await process_frame
	var after_pose: Vector3 = sk.global_transform * sk.get_bone_global_pose(foot).origin
	print("[ik2] target %s | foot before %s" % [str(tgt.global_position.snappedf(0.001)), str(before.snappedf(0.001))])
	print("[ik2]   get_bone_global_pose after advance: %s  (moved %.3f m)" % [str(after_pose.snappedf(0.001)), (after_pose - before).length()])
	print("[ik2]   inside skeleton_updated:           %s" % str((got["sig"] as Vector3).snappedf(0.001)))
	print("[ik2]   ModifierBoneTarget3D:              %s  (moved %.3f m)" % [str(mbt.global_position.snappedf(0.001)), (mbt.global_position - before).length()])
	quit(0)
