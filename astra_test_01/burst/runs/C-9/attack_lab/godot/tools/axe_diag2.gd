extends SceneTree
# AXE HOLD, part 2 -- where the tilt comes from, and what the strikes themselves do.
#
# The haft's direction on screen is  forearm (global) x wrist (hand-local rotation) x mount
# (the haft's fixed direction in the hand's frame). Each factor is swapped for a reference
# value while the other two stay as the clip has them:
#   wrist  actual | UNLOCKED (the clip before the carry lock, recovered by inverting the lock's
#          slerp: the lock is  q = slerp(src, T, alpha)  with T the unarmed idle's mean wrist and
#          alpha per clip from the export manifest) | FULL LOCK (q = T) | NEUTRAL (the rest wrist)
#   mount  actual | SQUARE (the haft turned in the fist, in the plane of haft and hand axis,
#          until it crosses the hand at 90 deg -- how a fist holds a haft)
# Frame: skeleton space, forward +Z, up +Y, his right -X (manifest facing/his_right).
const F := Vector3(0, 0, 1)
const U := Vector3(0, 1, 0)
const R := Vector3(-1, 0, 0)
const LOCK_ALPHA := {"idle_armed": 0.75, "walk_armed": 0.45, "run_armed": 0.60}
var k
var skel: Skeleton3D
var ap: AnimationPlayer
var s_ := 1.0
var hb := -1
var fb := -1
var H := Vector3.ZERO
var E := Vector3.ZERO
var Ah := Vector3.ZERO          # the hand's own axis (forearm -> hand at rest), hand-local
var H_sq := Vector3.ZERO
var E_sq := Vector3.ZERO
var head_l := Vector3.ZERO
var grip_l := Vector3.ZERO
var T := Quaternion.IDENTITY    # the carry lock's target
var R0 := Quaternion.IDENTITY   # rest wrist
var lines := []

func say(s: String) -> void:
	lines.append(s); print(s)

func _initialize() -> void:
	create_timer(600.0).timeout.connect(func(): push_error("WATCHDOG"); quit(4))
	k = load("res://scripts/knight.gd").new()
	k.setup(Vector3.RIGHT, Vector3.UP, Vector3.FORWARD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	for i in 4: await process_frame
	skel = k._skel
	ap = k._anim
	s_ = skel.global_transform.basis.get_scale().x
	hb = skel.find_bone("RightHand")
	fb = skel.find_bone("RightForeArm")
	R0 = skel.get_bone_rest(hb).basis.get_rotation_quaternion()
	_axe()
	T = _mean_track_rot("idle", "RightHand")
	(k._tree as AnimationTree).active = false
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	say("[diag] mount: haft %.1f deg from the hand axis (90 = square); square mount = the haft turned %.1f deg in the fist"
		% [rad_to_deg(H.angle_to(Ah)), rad_to_deg(H.angle_to(H_sq))])
	say("[diag] carry-lock target T (the unarmed idle's mean wrist): %.1f deg from the rest wrist"
		% rad_to_deg(T.angle_to(R0)))
	var out := {}
	# ---- 1. the four holds, and the 2 x 4 decomposition ------------------------------
	say("")
	say("[diag] clip        | tilt from vertical (deg), mean haft direction: fwd/out/up  -- by wrist x mount")
	for clip in ["idle_armed", "walk_armed", "run_armed", "block"]:
		var rows := _sample(clip, 24.0)
		out[clip] = _summ(rows)
		var al: float = float(LOCK_ALPHA.get(clip, 0.0))
		for w in ["actual", "unlocked", "full_lock", "neutral"]:
			if w == "unlocked" and al <= 0.0: continue
			if w == "full_lock" and al <= 0.0: continue
			var line := "[diag] %-11s wrist %-9s" % [clip, w]
			for m in ["actual", "square"]:
				var key := "h_%s_%s" % [w, m]
				var d := _mean_dir(rows, key)
				line += " | mount %-6s tilt %5.1f (med %5.1f, %3.0f..%3.0f) dir f%+.2f o%+.2f u%+.2f edge %+5.0f" % [
					m, rad_to_deg(d.angle_to(U)), _med(rows, "tilt_" + w + "_" + m), _lo(rows, "tilt_" + w + "_" + m), _hi(rows, "tilt_" + w + "_" + m),
					d.dot(F), d.dot(R), d.dot(U), _med(rows, "edge_" + w + "_" + m)]
			say(line)
		var s: Dictionary = out[clip]
		say("[diag] %-11s head vs fist: out %+.3f fwd %+.3f up %+.3f m | head vs spine midline: out %+.3f m | axe head to his skull %.3f m, to his sternum %.3f m | haft toward his chest (cos) %+.2f | wrist %.1f deg from rest (lock target %.1f)"
			% [clip, s["head_out"], s["head_fwd"], s["head_up"], s["head_mid_out"], s["to_skull"], s["to_chest"], s["toward_chest"], s["wrist_from_rest"], rad_to_deg(T.angle_to(R0))])
	# ---- 2. the strikes: ready and wind-up ------------------------------------------
	say("")
	for clip in ["attack", "attack_chop", "shield_bash"]:
		var rows2 := _sample(clip, 24.0)
		# impact = peak edge speed; wind-up = the slowest edge frame between the start of
		# the motion and the impact (the top of the back-swing); ready = frame 0
		var imp := 0
		for i in rows2.size():
			if float(rows2[i]["edge_speed"]) > float(rows2[imp]["edge_speed"]): imp = i
		var start := 0
		for i in range(1, imp):
			if float(rows2[i]["hand_speed"]) > 0.6: start = i; break
		var wind := start
		for i in range(start, imp):
			if float(rows2[i]["edge_speed"]) < float(rows2[wind]["edge_speed"]): wind = i
		for tag in [["ready", 0], ["moving", start], ["wind-up", wind], ["impact", imp]]:
			var r: Dictionary = rows2[int(tag[1])]
			say("[diag] %-11s %-7s t=%.2f tilt %5.1f dir f%+.2f o%+.2f | head vs fist out %+.3f fwd %+.3f up %+.3f | edge %+5.0f | hand %.2f m/s edge %.2f m/s"
				% [clip, String(tag[0]), float(r["t"]), float(r["tilt_actual_actual"]), float(r["fwd"]), float(r["out"]),
				   float(r["head_out"]), float(r["head_fwd"]), float(r["head_up"]), float(r["edge_actual_actual"]),
				   float(r["hand_speed"]), float(r["edge_speed"])])
		var tl := ""
		for i in range(0, mini(rows2.size(), imp + 3), 2 if clip != "attack_chop" else 5):
			var r: Dictionary = rows2[i]
			tl += " %.2f:t%.0f/f%+.1f/o%+.1f/e%+.0f/v%.1f" % [float(r["t"]), float(r["tilt_actual_actual"]), float(r["fwd"]), float(r["out"]), float(r["edge_actual_actual"]), float(r["hand_speed"])]
		say("[diag] %-11s timeline t:tilt/fwd/out/edge/hand-speed%s" % [clip, tl])
		out[clip] = {"impact_t": float(rows2[imp]["t"]), "wind_t": float(rows2[wind]["t"]), "start_t": float(rows2[start]["t"]),
					 "rows": rows2.map(func(r): return {"t": r["t"], "tilt": r["tilt_actual_actual"], "fwd": r["fwd"], "out": r["out"],
						"edge": r["edge_actual_actual"], "head_out": r["head_out"], "hand_speed": r["hand_speed"], "edge_speed": r["edge_speed"]})}
	var outp: String = OS.get_environment("LAB_OUT") if OS.has_environment("LAB_OUT") else "/tmp/axe2.json"
	var f := FileAccess.open(outp, FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " ")); f.close()
	var g := FileAccess.open(outp.replace(".json", ".txt"), FileAccess.WRITE)
	g.store_string("\n".join(lines) + "\n"); g.close()
	quit(0)

func _mean_track_rot(clip: String, bone: String) -> Quaternion:
	var a := ap.get_animation(clip)
	var acc := Vector4.ZERO
	var ref := Quaternion.IDENTITY
	var have := false
	for t in a.get_track_count():
		if a.track_get_type(t) != Animation.TYPE_ROTATION_3D: continue
		if String(a.track_get_path(t).get_concatenated_subnames()) != bone: continue
		for i in a.track_get_key_count(t):
			var q: Quaternion = a.track_get_key_value(t, i)
			if not have: ref = q; have = true
			var v := Vector4(q.x, q.y, q.z, q.w)
			if v.dot(Vector4(ref.x, ref.y, ref.z, ref.w)) < 0.0: v = -v
			acc += v
	acc = acc.normalized()
	return Quaternion(acc.x, acc.y, acc.z, acc.w)

func _axe() -> void:
	var mi: MeshInstance3D = (k.gear["_pieces"]["axe"] as Array)[0]
	var sk: Skin = mi.skin
	var bind := Transform3D()
	for i in sk.get_bind_count():
		if String(sk.get_bind_name(i)) == "RightHand": bind = sk.get_bind_pose(i)
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
	var gh: Transform3D = skel.get_bone_global_rest(hb)
	var gf: Transform3D = skel.get_bone_global_rest(fb)
	Ah = (gh.basis.inverse() * (gh.origin - gf.origin)).normalized()
	H_sq = (H - H.dot(Ah) * Ah).normalized()
	var q := Quaternion(H, H_sq)
	E_sq = (q * E).normalized()

func _pow(q: Quaternion, p: float) -> Quaternion:
	if q.w < 0.0: q = -q
	var ang: float = 2.0 * acos(clampf(q.w, -1.0, 1.0))
	if ang < 1e-7: return Quaternion.IDENTITY
	var axis := Vector3(q.x, q.y, q.z).normalized()
	return Quaternion(axis, ang * p)

func _sample(clip: String, fps: float) -> Array:
	var a := ap.get_animation(clip)
	var n: int = maxi(int(round(a.length * fps)), 1)
	ap.play(clip)
	var rows := []
	var al: float = float(LOCK_ALPHA.get(clip, 0.0))
	var prev_hand := Vector3.INF
	var prev_edge := Vector3.INF
	var chest := skel.find_bone("Spine01")
	var skull := skel.find_bone("Head")
	var spine := skel.find_bone("Spine")
	for i in n + 1:
		var t: float = a.length * float(i) / float(n)
		ap.seek(t, true, true)
		var g: Transform3D = skel.get_bone_global_pose(hb)
		var bf: Basis = skel.get_bone_global_pose(fb).basis.orthonormalized()
		var qa: Quaternion = skel.get_bone_pose_rotation(hb)
		var wr := {"actual": qa, "neutral": R0}
		if al > 0.0:
			wr["full_lock"] = T
			wr["unlocked"] = qa * _pow(qa.inverse() * T, -al / (1.0 - al))
		var r := {"t": t}
		for w in wr.keys():
			var hbasis: Basis = bf * Basis(wr[w] as Quaternion)
			for m in ["actual", "square"]:
				var hv: Vector3 = (hbasis * (H if m == "actual" else H_sq)).normalized()
				var ev: Vector3 = (hbasis * (E if m == "actual" else E_sq)).normalized()
				r["h_%s_%s" % [w, m]] = hv
				r["tilt_%s_%s" % [w, m]] = rad_to_deg(hv.angle_to(U))
				r["edge_%s_%s" % [w, m]] = rad_to_deg(atan2(ev.dot(R), ev.dot(F)))
		var h: Vector3 = r["h_actual_actual"]
		var head: Vector3 = (g * head_l) * s_
		var fist: Vector3 = (g * grip_l) * s_
		var d: Vector3 = head - fist
		var mid: Vector3 = skel.get_bone_global_pose(spine).origin * s_
		var ch: Vector3 = skel.get_bone_global_pose(chest).origin * s_
		var sk_: Vector3 = skel.get_bone_global_pose(skull).origin * s_
		var tc: Vector3 = ch - fist
		r["fwd"] = h.dot(F); r["out"] = h.dot(R)
		r["head_out"] = d.dot(R); r["head_fwd"] = d.dot(F); r["head_up"] = d.dot(U)
		r["head_mid_out"] = (head - mid).dot(R)
		r["to_skull"] = (head - sk_).length(); r["to_chest"] = (head - ch).length()
		r["toward_chest"] = h.dot(tc.normalized())
		r["wrist_from_rest"] = rad_to_deg(qa.angle_to(R0))
		var edge_p: Vector3 = head
		var hand_p: Vector3 = g.origin * s_
		r["hand_speed"] = 0.0 if prev_hand == Vector3.INF else (hand_p - prev_hand).length() * fps
		r["edge_speed"] = 0.0 if prev_edge == Vector3.INF else (edge_p - prev_edge).length() * fps
		prev_hand = hand_p; prev_edge = edge_p
		rows.append(r)
	return rows

func _mean_dir(rows: Array, key: String) -> Vector3:
	var acc := Vector3.ZERO
	for r in rows: acc += (r[key] as Vector3)
	return acc.normalized()

func _col(rows: Array, key: String) -> Array:
	var v := rows.map(func(r): return float(r[key])); v.sort(); return v

func _med(rows: Array, key: String) -> float:
	var v := _col(rows, key); return float(v[v.size() / 2])

func _lo(rows: Array, key: String) -> float:
	return float(_col(rows, key)[0])

func _hi(rows: Array, key: String) -> float:
	return float(_col(rows, key)[-1])

func _summ(rows: Array) -> Dictionary:
	var o := {}
	for key in ["head_out", "head_fwd", "head_up", "head_mid_out", "to_skull", "to_chest", "toward_chest", "wrist_from_rest"]:
		o[key] = _med(rows, key)
	for key in ["tilt_actual_actual", "edge_actual_actual"]:
		o[key] = _med(rows, key)
		o[key + "_range"] = [_lo(rows, key), _hi(rows, key)]
	var d := _mean_dir(rows, "h_actual_actual")
	o["mean_dir"] = [d.dot(F), d.dot(R), d.dot(U)]
	return o
