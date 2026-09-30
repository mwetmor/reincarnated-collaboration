extends SceneTree
# Does Skeleton3D.advance() run the modifiers NOW, or only schedule them? And does forcing the
# deferred update (NOTIFICATION_UPDATE_SKELETON) run them synchronously?
func _initialize() -> void:
	create_timer(60.0).timeout.connect(func(): quit(4))
	var ps := ResourceLoader.load("res://models/gear/nb-body.glb", "", ResourceLoader.CACHE_MODE_IGNORE_DEEP) as PackedScene
	var r := ps.instantiate()
	root.add_child(r)
	await process_frame
	var sk: Skeleton3D = r.find_children("*", "Skeleton3D", true, false)[0]
	sk.modifier_callback_mode_process = Skeleton3D.MODIFIER_CALLBACK_MODE_PROCESS_MANUAL
	var m := SkeletonModifier3D.new()
	m.set_script(load("res://tools/ik_rot45.gd"))
	sk.add_child(m)
	var n := {"c": 0}
	m.modification_processed.connect(func(): n["c"] = int(n["c"]) + 1)
	await process_frame
	var c0: int = int(n["c"])
	sk.advance(1.0 / 96.0)
	var after_advance: int = int(n["c"]) - c0
	sk.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)
	var after_notif: int = int(n["c"]) - c0
	var t0 := Time.get_ticks_usec()
	for i in 200:
		sk.advance(1.0 / 96.0)
		sk.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)
	var us := float(Time.get_ticks_usec() - t0) / 200.0
	print("[ik6] modifier passes: after advance() %d, after + NOTIFICATION_UPDATE_SKELETON %d; 200 forced passes -> %d (%.1f us each)"
		% [after_advance, after_notif, int(n["c"]) - c0 - after_notif, us])
	quit(0)
