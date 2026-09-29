extends SceneTree
# Is the footwork in the SOURCE clip, or does the merge put it there?
# Each Meshy source measured in ITS OWN rig, then the same clip as merged into the body.
func _initialize() -> void:
	create_timer(300.0).timeout.connect(func(): push_error("LAB WATCHDOG"); quit(4))
	var body := await _rig("res://models/gear/nb-body.glb")
	for pair in [["src_axe_stance", "idle_armed_stance"], ["src_walk_fight", "walk_armed"], ["src_axe_chop", "attack_chop"]]:
		var src := await _rig("res://models/%s.glb" % pair[0])
		var sname: String = String((src[1] as AnimationPlayer).get_animation_list()[0])
		_measure("SOURCE %-15s own rig" % pair[0].substr(4), src, sname)
		_measure("MERGED %-15s body rig" % pair[1], body, pair[1])
	quit(0)

func _rig(path: String) -> Array:
	var ps := ResourceLoader.load(path, "", ResourceLoader.CACHE_MODE_IGNORE_DEEP) as PackedScene
	if ps == null:
		push_error("not imported: %s" % path); quit(5); return []
	var r := ps.instantiate()
	root.add_child(r)
	await process_frame
	await process_frame
	var sk: Skeleton3D = r.find_children("*", "Skeleton3D", true, false)[0]
	var ap: AnimationPlayer = r.find_children("*", "AnimationPlayer", true, false)[0]
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	ap.active = true
	return [sk, ap]

func _measure(label: String, rig: Array, clip: String) -> void:
	var sk: Skeleton3D = rig[0]
	var ap: AnimationPlayer = rig[1]
	var s: float = sk.global_transform.basis.get_scale().x
	var a := ap.get_animation(clip)
	var n := int(round(a.length * 24.0))
	ap.play(clip)
	var P := {"LeftToeBase": [], "RightToeBase": []}
	var knee := []
	for i in n + 1:
		ap.seek(a.length * float(i) / float(n), true, true)
		for f in P.keys():
			(P[f] as Array).append(sk.get_bone_global_pose(sk.find_bone(f)).origin * s)
		knee.append(sk.get_bone_pose_rotation(sk.find_bone("LeftUpLeg")))
	var w := []
	for f in P.keys():
		var lo := Vector2(1e9, 1e9); var hi := -lo
		for p in P[f]:
			lo = lo.min(Vector2((p as Vector3).x, (p as Vector3).z)); hi = hi.max(Vector2((p as Vector3).x, (p as Vector3).z))
		w.append((hi - lo).length())
	var turn := 0.0
	for q in knee:
		turn = maxf(turn, rad_to_deg((knee[0] as Quaternion).angle_to(q)))
	print("%s | %5.2f s | feet wander L %.3f R %.3f m | left thigh turns up to %.1f deg" % [label, a.length, float(w[0]), float(w[1]), turn])
