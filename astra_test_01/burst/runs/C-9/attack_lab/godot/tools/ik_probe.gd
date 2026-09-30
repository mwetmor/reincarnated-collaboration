extends SceneTree
func _initialize() -> void:
	create_timer(60.0).timeout.connect(func(): quit(4))
	print("[ik] engine %s" % Engine.get_version_info()["string"])
	var mods := ClassDB.get_inheriters_from_class("SkeletonModifier3D")
	mods.sort()
	print("[ik] SkeletonModifier3D inheriters: %s" % str(mods))
	for c in ["TwoBoneIK3D", "ChainIK3D", "FABRIK3D", "CCDIK3D", "JacobianIK3D", "SplineIK3D", "IKModifier3D", "SkeletonIK3D", "LookAtModifier3D"]:
		print("[ik]   %-16s exists=%s" % [c, str(ClassDB.class_exists(c))])
	var sk_methods := []
	for m in ClassDB.class_get_method_list("Skeleton3D", true):
		var n: String = m["name"]
		if n.contains("advance") or n.contains("modifier"): sk_methods.append(n)
	print("[ik] Skeleton3D modifier API: %s" % str(sk_methods))
	for c in ["TwoBoneIK3D", "SkeletonIK3D"]:
		if not ClassDB.class_exists(c): continue
		var props := []
		for p in ClassDB.class_get_property_list(c, true):
			props.append(String(p["name"]))
		var meths := []
		for m in ClassDB.class_get_method_list(c, true):
			meths.append(String(m["name"]))
		print("[ik] %s props: %s" % [c, str(props)])
		print("[ik] %s methods: %s" % [c, str(meths)])
	quit(0)
