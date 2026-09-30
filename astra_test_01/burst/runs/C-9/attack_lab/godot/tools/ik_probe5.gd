extends SceneTree
func _initialize() -> void:
	create_timer(60.0).timeout.connect(func(): quit(4))
	var v := []
	for m in ClassDB.class_get_method_list("SkeletonModifier3D", true):
		var n: String = m["name"]
		if n.begins_with("_"): v.append(n)
	print("[ik5] SkeletonModifier3D virtuals/private: %s" % str(v))
	print("[ik5] Skeleton3D default modifier mode: %d (0=physics 1=idle 2=manual)" % Skeleton3D.new().modifier_callback_mode_process)
	quit(0)
