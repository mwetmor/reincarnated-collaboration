extends SceneTree
# T12 rank 2b: THE GUARD FRAME, from Meshy's Combat_Stance (action 89, fetched onto his own rig).
# The axe is placed by the STAGED MOUNT (nb_d2/export_staging/T12_2_mount/weapon_mount.json: the
# square seat, roll 0) -- its haft, edge and head carried in RightHand's frame by the grip G.
# Every frame of the stance is scored by the guard predicate (tilt 30-60 deg, haft forward and
# outboard, head outboard of the fist, |edge heading| <= 45 deg) and by the ARM TRAVEL into the
# three strike starts (hand + axe head, relative to the chest, in metres at our rig's scale).
# The chosen frame's wrist (RightHand in RightForeArm) is the new carry-lock target.
# env: PICK_OUT (json), MOUNT (weapon_mount.json path)
const F := Vector3(0, 0, 1)
const U := Vector3(0, 1, 0)
const R := Vector3(-1, 0, 0)
var H := Vector3.ZERO
var E := Vector3.ZERO
var head_l := Vector3.ZERO
var grip_l := Vector3.ZERO

func _initialize() -> void:
	create_timer(300.0).timeout.connect(func(): print("[pick] WATCHDOG"); quit(4))
	var k = load("res://scripts/knight.gd").new()
	k.setup(Vector3.RIGHT, Vector3.UP, Vector3.FORWARD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	for i in 4: await process_frame
	var skel: Skeleton3D = k._skel
	var ap: AnimationPlayer = k._anim
	(k._tree as AnimationTree).active = false
	for c in skel.get_children():
		if c is SkeletonModifier3D: (c as SkeletonModifier3D).active = false
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	_axe(k, skel)
	# THE MOUNT: G in RightHand's local frame
	var mp: String = OS.get_environment("MOUNT")
	var mj = JSON.parse_string(FileAccess.get_file_as_string(mp))
	var Gm: Array = mj["G"]
	var G := Transform3D(Basis(Vector3(Gm[0][0], Gm[1][0], Gm[2][0]), Vector3(Gm[0][1], Gm[1][1], Gm[2][1]), Vector3(Gm[0][2], Gm[1][2], Gm[2][2])),
						 Vector3(Gm[0][3], Gm[1][3], Gm[2][3]))
	var Hm: Vector3 = (G.basis * H).normalized()
	var Em: Vector3 = (G.basis * E).normalized()
	var headm: Vector3 = G * head_l
	var gripm: Vector3 = G * grip_l
	var s_: float = skel.global_transform.basis.get_scale().x
	var hb := skel.find_bone("RightHand"); var ch := skel.find_bone("Spine")
	# the strike starts, ours, relative to the chest (m)
	var starts := {}
	for st in ["attack", "attack_chop", "shield_bash"]:
		ap.play(st); ap.seek(0.0, true, true)
		var g: Transform3D = skel.get_bone_global_pose(hb)
		var c0: Vector3 = skel.get_bone_global_pose(ch).origin
		starts[st] = [(g.origin - c0) * s_, (g * headm - c0) * s_]
	var our_h: float = (skel.get_bone_global_rest(skel.find_bone("Head")).origin - skel.get_bone_global_rest(skel.find_bone("Hips")).origin).length() * s_
	# THE STANCE, on its own skeleton (the same rig, Meshy's own 1.70 m scale)
	var sc := (load("res://models/anims/combat_stance.glb") as PackedScene).instantiate()
	root.add_child(sc)
	var sk2: Skeleton3D = null; var ap2: AnimationPlayer = null
	for n in sc.find_children("*", "", true, false):
		if n is Skeleton3D and sk2 == null: sk2 = n
		elif n is AnimationPlayer and ap2 == null: ap2 = n
	ap2.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var s2: float = sk2.global_transform.basis.get_scale().x
	var their_h: float = (sk2.get_bone_global_rest(sk2.find_bone("Head")).origin - sk2.get_bone_global_rest(sk2.find_bone("Hips")).origin).length() * s2
	var k2: float = our_h / maxf(their_h, 1e-6)
	var hb2 := sk2.find_bone("RightHand"); var fb2 := sk2.find_bone("RightForeArm"); var ch2 := sk2.find_bone("Spine")
	var clip: String = ap2.get_animation_list()[0]
	var a := ap2.get_animation(clip)
	var n: int = int(round(a.length * 24.0))
	ap2.play(clip)
	# is his forward +Z on this rig too? toes vs ankles at rest
	var toe: Vector3 = sk2.get_bone_global_rest(sk2.find_bone("LeftToeBase")).origin - sk2.get_bone_global_rest(sk2.find_bone("LeftFoot")).origin
	print("[pick] stance '%s' %.2f s, %d frames; rig height scale ours/theirs %.4f; toe direction at rest %s (forward is +Z)"
		% [clip, a.length, n + 1, k2, str(toe.normalized().snappedf(0.01))])
	var rows := []
	for i in n + 1:
		var t: float = a.length * float(i) / float(n)
		ap2.seek(t, true, true)
		var g2: Transform3D = sk2.get_bone_global_pose(hb2)
		var c2: Vector3 = sk2.get_bone_global_pose(ch2).origin
		var gb: Basis = g2.basis.orthonormalized()
		var h: Vector3 = (gb * Hm).normalized()
		var e: Vector3 = (gb * Em).normalized()
		var head_rel: Vector3 = (g2 * headm - c2) * s2 * k2
		var hand_rel: Vector3 = (g2.origin - c2) * s2 * k2
		var fist: Vector3 = (g2 * gripm - c2) * s2 * k2
		var d: Vector3 = head_rel - fist
		var ok: bool = rad_to_deg(h.angle_to(U)) >= 30.0 and rad_to_deg(h.angle_to(U)) <= 60.0 and h.dot(F) > 0.0 and h.dot(R) > 0.0 \
			and d.dot(R) > 0.0 and absf(rad_to_deg(atan2(e.dot(R), e.dot(F)))) <= 45.0
		var travel := 0.0
		var per := {}
		for st in starts.keys():
			var dd: float = (hand_rel - (starts[st][0] as Vector3)).length() + (head_rel - (starts[st][1] as Vector3)).length()
			per[st] = snappedf(dd, 0.001); travel += dd
		var wrist: Quaternion = sk2.get_bone_pose_rotation(hb2)
		rows.append({"t": t, "tilt": rad_to_deg(h.angle_to(U)), "fwd": h.dot(F), "out": h.dot(R), "head_out": d.dot(R),
					 "edge": rad_to_deg(atan2(e.dot(R), e.dot(F))), "pass": ok, "travel": travel, "per": per,
					 "wrist": [wrist.x, wrist.y, wrist.z, wrist.w]})
	var passing := rows.filter(func(r): return bool(r["pass"]))
	passing.sort_custom(func(x, y): return float(x["travel"]) < float(y["travel"]))
	var line := ""
	for i in range(0, rows.size(), 3):
		var r: Dictionary = rows[i]
		line += " %.2f:t%.0f/f%+.1f/o%+.1f/e%+.0f%s" % [float(r["t"]), float(r["tilt"]), float(r["fwd"]), float(r["out"]), float(r["edge"]), "*" if bool(r["pass"]) else ""]
	print("[pick] timeline (the staged mount; * = guard) %s" % line)
	print("[pick] %d of %d frames pass the guard predicate" % [passing.size(), rows.size()])
	for r in passing.slice(0, 5):
		print("[pick]   t=%.3f tilt %.1f fwd %+.2f out %+.2f head out %+.3f edge %+.0f | arm travel %.3f m %s"
			% [float(r["t"]), float(r["tilt"]), float(r["fwd"]), float(r["out"]), float(r["head_out"]), float(r["edge"]), float(r["travel"]), str(r["per"])])
	var best: Dictionary = passing[0] if passing.size() > 0 else {}
	# and for scale: the same arm travel from today's idle_armed (its median frame)
	ap.play("idle_armed")
	var tr_idle := []
	var ia := ap.get_animation("idle_armed")
	for i in 25:
		ap.seek(ia.length * float(i) / 24.0, true, true)
		var g: Transform3D = skel.get_bone_global_pose(hb)
		var c0: Vector3 = skel.get_bone_global_pose(ch).origin
		var tr := 0.0
		for st in starts.keys():
			tr += ((g.origin - c0) * s_ - (starts[st][0] as Vector3)).length() + ((g * headm - c0) * s_ - (starts[st][1] as Vector3)).length()
		tr_idle.append(tr)
	tr_idle.sort()
	print("[pick] for scale: arm travel into the three strike starts from today's idle_armed (mounted axe): median %.3f m" % float(tr_idle[12]))
	var f := FileAccess.open(OS.get_environment("PICK_OUT") if OS.has_environment("PICK_OUT") else "/tmp/pick.json", FileAccess.WRITE)
	f.store_string(JSON.stringify({"clip": clip, "chosen": best, "passing": passing.size(), "frames": rows.size(), "rows": rows,
								   "idle_armed_travel_median": float(tr_idle[12])}, " ")); f.close()
	quit(0)

func _axe(k, skel: Skeleton3D) -> void:
	var mi: MeshInstance3D = (k.gear["_pieces"]["axe"] as Array)[0]
	var bind := Transform3D()
	for i in mi.skin.get_bind_count():
		if String(mi.skin.get_bind_name(i)) == "RightHand": bind = mi.skin.get_bind_pose(i)
	var verts: PackedVector3Array = mi.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
	var c := Vector3.ZERO
	var all := []
	for v in verts:
		var p: Vector3 = bind * v; all.append(p); c += p
	c /= float(all.size())
	var xx := 0.0; var xy := 0.0; var xz := 0.0; var yy := 0.0; var yz := 0.0; var zz := 0.0
	for p in all:
		var d: Vector3 = p - c
		xx += d.x * d.x; xy += d.x * d.y; xz += d.x * d.z; yy += d.y * d.y; yz += d.y * d.z; zz += d.z * d.z
	var ax := Vector3(1, 1, 1).normalized()
	for it in 60:
		ax = Vector3(xx * ax.x + xy * ax.y + xz * ax.z, xy * ax.x + yy * ax.y + yz * ax.z, xz * ax.x + yz * ax.y + zz * ax.z).normalized()
	var mk: Node3D = (k.gear["_pieces"]["_markers_axe"] as Dictionary)["axe_edge"]
	var edge_l: Vector3 = mk.transform.origin
	if (edge_l - c).dot(ax) < 0.0: ax = -ax
	H = ax
	E = ((edge_l - c) - (edge_l - c).dot(H) * H).normalized()
	head_l = c + H * (edge_l - c).dot(H)
	grip_l = c + H * (-c).dot(H)
