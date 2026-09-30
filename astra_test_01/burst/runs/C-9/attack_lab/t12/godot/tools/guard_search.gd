extends SceneTree
# T12 rank 3 -- THE GUARD, chosen per clip so the axe turns in the fist AS LITTLE AS IT CAN.
#
# weapon_r's rest is the mount (the square seat): the haft runs along the fist's channel. Any
# weapon_r rotation turns the haft OUT of that channel, through the fingers -- the one thing the
# grip morph cannot follow. A guard fixed at one world angle (45 deg, forward and out equally)
# needed a median 87-179 deg turn in the fist (solve1). So, per HOLD clip, the guard is searched:
#   haft tilt 35-55 deg, azimuth 10-80 deg (forward -> outboard), edge heading -40..+40 deg,
# riding the chest frame-by-frame (weapon_r_local = (chest^-1 hand)^-1 x guard_in_chest -- the
# arm chain only), and the choice is the smallest median HAFT DEFLECTION out of the channel among
# guards that keep the predicate on >= 95% of the clip's frames.
#   IDLE: frames of every armed clip are scanned for a pose whose MOUNTED axe is already at guard
# with the fist in front of him -- fixed as the new idle's arms, the axe needs no turn at all.
#   STRIKES: slow frames hold the idle's guard (the fade from standing has nothing to turn), fast
# frames roll the mounted axe about its haft until the edge lies along the head's travel.
# env: SOLVE_OUT (json)
const F := Vector3(0, 0, 1)
const U := Vector3(0, 1, 0)
const R := Vector3(-1, 0, 0)
const HOLD := ["walk_armed", "run_armed", "run_armed_L", "run_armed_R", "strafe_L_armed", "strafe_R_armed", "block"]
const SPLIT := {"walk_armed": ["walk", false], "run_armed": ["run", true]}
const STRIKES := ["attack", "attack_chop"]
const ARMS := ["LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand", "RightShoulder", "RightArm", "RightForeArm", "RightHand"]
const IDLE_SOURCES := ["walk_armed", "idle_armed", "run_armed_R", "run_armed_L", "shield_bash", "block", "strafe_R_armed", "strafe_L_armed"]
var k
var skel: Skeleton3D
var ap: AnimationPlayer
var tree: AnimationTree
var s_ := 1.0
var hb := -1
var wb := -1
var chb := -1
var W_rest := Transform3D()
var head_w := Vector3.ZERO
var lines := []

func say(s: String) -> void:
	lines.append(s); print(s)

func _initialize() -> void:
	create_timer(1500.0).timeout.connect(func(): print("[guard] WATCHDOG"); quit(4))
	k = load("res://scripts/knight.gd").new()
	k.setup(Vector3.RIGHT, Vector3.UP, Vector3.FORWARD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	for i in 4: await process_frame
	skel = k._skel; ap = k._anim; tree = k._tree
	s_ = skel.global_transform.basis.get_scale().x
	hb = skel.find_bone("RightHand"); wb = skel.find_bone("weapon_r"); chb = skel.find_bone("Spine")
	for c in skel.get_children():
		if c is SkeletonModifier3D: (c as SkeletonModifier3D).active = false
	W_rest = skel.get_bone_rest(wb)
	_axe()
	# ---- mean chest: through the TREE for the split gaits ------------------------------------
	var mean_chest := {}
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	for clip in SPLIT.keys():
		var g: Array = SPLIT[clip]
		k.global_position = Vector3(0, 0.03, 0)
		var qs := []
		for i in 96:
			k.drive_dir(Vector2(1, 0), bool(g[1]), 1.0 / 24.0)
			tree.advance(1.0 / 24.0)
			if i >= 48: qs.append(_q(skel.get_bone_global_pose(chb).basis))
		for i in 36:
			k.drive_dir(Vector2.ZERO, false, 1.0 / 24.0); tree.advance(1.0 / 24.0)
		mean_chest[clip] = _qmean(qs)
	tree.active = false
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var out := {"weapon_r": {}}
	var chosen := {}
	# ---- HOLD clips: search the guard ----------------------------------------------------------
	for clip in HOLD:
		var times := _key_times(clip)
		var C := []; var Hd := []
		ap.play(clip)
		for t in times:
			ap.seek(t, true, true)
			C.append(skel.get_bone_global_pose(chb).basis.orthonormalized())
			Hd.append(skel.get_bone_global_pose(hb).basis.orthonormalized())
		var Cm: Basis = Basis(mean_chest[clip]) if mean_chest.has(clip) else Basis(_qmean(C.map(func(b): return _q(b))))
		var best := {}
		for tilt in [35.0, 40.0, 45.0, 50.0, 55.0]:
			for az in [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0]:
				var h: Vector3 = (F * cos(deg_to_rad(az)) + R * sin(deg_to_rad(az))) * sin(deg_to_rad(tilt)) + U * cos(deg_to_rad(tilt))
				for psi in [-40.0, -30.0, -20.0, -10.0, 0.0, 10.0, 20.0, 30.0, 40.0]:
					var d: Vector3 = F * cos(deg_to_rad(psi)) + R * sin(deg_to_rad(psi))
					var e: Vector3 = (d - d.dot(h) * h).normalized()
					var B := Basis(h.cross(e).normalized(), h, e)
					var r := _score(B, Cm, C, Hd)
					if float(r["pass"]) < 0.95: continue
					if best.is_empty() or float(r["defl_med"]) < float(best["defl_med"]):
						best = r; best["tilt"] = tilt; best["az"] = az; best["psi"] = psi; best["B"] = B
		if best.is_empty():
			say("[guard] %-15s NO guard in the grid keeps the predicate on 95%% of frames" % clip)
			continue
		chosen[clip] = best
		out["weapon_r"][clip] = {"times": times, "quats": (best["qs"] as Array).map(func(q): return [q.x, q.y, q.z, q.w]),
								 "guard": {"tilt": best["tilt"], "azimuth": best["az"], "edge_heading": best["psi"]}}
		say("[guard] %-15s guard tilt %2.0f az %2.0f edge %+3.0f | predicate %3.0f%% | haft out of the channel median %4.1f p90 %4.1f deg, whole turn median %5.1f"
			% [clip, float(best["tilt"]), float(best["az"]), float(best["psi"]), 100.0 * float(best["pass"]), float(best["defl_med"]), float(best["defl_p90"]), float(best["turn_med"])])
	# ---- IDLE: a pose whose mounted axe is already at guard, fist in front -----------------------
	var cands := []
	for clip in IDLE_SOURCES:
		var times2 := _key_times(clip)
		ap.play(clip)
		for t in times2:
			ap.seek(t, true, true)
			var hg: Transform3D = skel.get_bone_global_pose(hb)
			var wg: Basis = (hg.basis.orthonormalized() * W_rest.basis.orthonormalized())
			var h2: Vector3 = (wg * Vector3.UP).normalized(); var e2: Vector3 = (wg * Vector3.BACK).normalized()
			var tilt2: float = rad_to_deg(h2.angle_to(U)); var ed: float = rad_to_deg(atan2(e2.dot(R), e2.dot(F)))
			if tilt2 < 35.0 or tilt2 > 55.0 or h2.dot(F) < 0.15 or h2.dot(R) < 0.15 or absf(ed) > 35.0: continue
			var cg: Transform3D = skel.get_bone_global_pose(chb)
			var fist: Vector3 = ((hg * W_rest).origin - cg.origin) * s_
			if fist.dot(F) < 0.10: continue
			cands.append({"clip": clip, "t": t, "tilt": tilt2, "fwd": h2.dot(F), "out": h2.dot(R), "edge": ed,
						  "fist_fwd": fist.dot(F), "fist_out": fist.dot(R), "fist_up": fist.dot(U)})
	cands.sort_custom(func(a, b): return absf(float(a["tilt"]) - 45.0) + absf(float(a["edge"])) * 0.3 < absf(float(b["tilt"]) - 45.0) + absf(float(b["edge"])) * 0.3)
	say("[guard] idle: %d frames of the armed clips hold the MOUNTED axe at guard with the fist in front; best 8:" % cands.size())
	for c in cands.slice(0, 8):
		say("[guard]   %-15s t=%.3f tilt %.1f fwd %+.2f out %+.2f edge %+.0f | fist fwd %+.2f out %+.2f up %+.2f m of the chest"
			% [String(c["clip"]), float(c["t"]), float(c["tilt"]), float(c["fwd"]), float(c["out"]), float(c["edge"]), float(c["fist_fwd"]), float(c["fist_out"]), float(c["fist_up"])])
	var idle_B := Basis()
	if cands.size() > 0:
		var pick: Dictionary = cands[0]
		if OS.has_environment("IDLE_PICK"):
			var ps: PackedStringArray = OS.get_environment("IDLE_PICK").split("@")
			for c in cands:
				if String(c["clip"]) == ps[0] and absf(float(c["t"]) - float(ps[1])) < 1e-3: pick = c
		ap.play(String(pick["clip"])); ap.seek(float(pick["t"]), true, true)
		var arms := {}
		for bn in ARMS:
			var q5: Quaternion = skel.get_bone_pose_rotation(skel.find_bone(bn))
			arms[bn] = [q5.x, q5.y, q5.z, q5.w]
		# the new idle: the unarmed idle, those arms; the guard = that frame's own mounted axe in
		# the chest frame, riding the idle's chest -> weapon_r turns only by the idle's breathing
		var cg0: Basis = skel.get_bone_global_pose(chb).basis.orthonormalized()
		var wg0: Basis = skel.get_bone_global_pose(hb).basis.orthonormalized() * W_rest.basis.orthonormalized()
		var g_in_chest: Basis = cg0.inverse() * wg0
		var times3 := _key_times("idle")
		ap.play("idle")
		var C3 := []; var H3 := []
		for t in times3:
			ap.seek(t, true, true)
			for bn in ARMS:
				var a2: Array = arms[bn]
				skel.set_bone_pose_rotation(skel.find_bone(bn), Quaternion(a2[0], a2[1], a2[2], a2[3]))
			C3.append(skel.get_bone_global_pose(chb).basis.orthonormalized())
			H3.append(skel.get_bone_global_pose(hb).basis.orthonormalized())
		var Cm3: Basis = Basis(_qmean(C3.map(func(b): return _q(b))))
		idle_B = Cm3 * g_in_chest
		var r3 := _score(idle_B, Cm3, C3, H3)
		out["weapon_r"]["idle_guard"] = {"times": times3, "quats": (r3["qs"] as Array).map(func(q): return [q.x, q.y, q.z, q.w]),
										 "arms_from": "%s@%.4f" % [String(pick["clip"]), float(pick["t"])], "arms": arms}
		say("[guard] idle_guard      arms from %s @ %.3f s | predicate %3.0f%% | haft out of the channel median %4.1f p90 %4.1f deg"
			% [String(pick["clip"]), float(pick["t"]), 100.0 * float(r3["pass"]), float(r3["defl_med"]), float(r3["defl_p90"])])
	# ---- STRIKES -----------------------------------------------------------------------------------
	for clip in STRIKES:
		var times4 := _key_times(clip)
		ap.play(clip)
		var hands := []; var heads := []
		for t in times4:
			ap.seek(t, true, true)
			var hg2: Transform3D = skel.get_bone_global_pose(hb)
			hands.append(hg2); heads.append((hg2 * W_rest) * head_w)
		var sp := []
		for i in times4.size():
			var i0: int = maxi(i - 1, 0); var i1: int = mini(i + 1, times4.size() - 1)
			sp.append(((heads[i1] as Vector3) - (heads[i0] as Vector3)).length() * s_ / maxf(float(times4[i1]) - float(times4[i0]), 1e-6))
		var pk := 0.0
		for v in sp: pk = maxf(pk, float(v))
		var qs4 := []
		var nfull := 0; var nguard := 0
		for i in times4.size():
			var hbs: Basis = (hands[i] as Transform3D).basis.orthonormalized()
			var q_guard: Quaternion = _q(hbs.inverse() * idle_B)
			var Wm: Basis = hbs * W_rest.basis.orthonormalized()
			var h4: Vector3 = (Wm * Vector3.UP).normalized(); var em: Vector3 = (Wm * Vector3.BACK).normalized()
			var i0: int = maxi(i - 1, 0); var i1: int = mini(i + 1, times4.size() - 1)
			var v4: Vector3 = (heads[i1] as Vector3) - (heads[i0] as Vector3)
			var u4: Vector3 = v4 - v4.dot(h4) * h4
			var q_lead: Quaternion = W_rest.basis.get_rotation_quaternion()
			if u4.length() > 1e-9:
				u4 = u4.normalized()
				q_lead = _q(hbs.inverse() * Basis(h4, atan2(em.cross(u4).dot(h4), em.dot(u4))) * Wm)
			var x: float = clampf((float(sp[i]) / maxf(pk, 1e-6) - 0.15) / 0.20, 0.0, 1.0)
			var bw: float = x * x * (3.0 - 2.0 * x)
			if bw >= 0.999: nfull += 1
			if bw <= 0.001: nguard += 1
			if q_guard.dot(q_lead) < 0.0: q_lead = -q_lead
			qs4.append(q_guard.slerp(q_lead, bw))
		out["weapon_r"][clip] = {"times": times4, "quats": qs4.map(func(q): return [q.x, q.y, q.z, q.w])}
		say("[guard] %-15s %3d keys | edge-leading on %d frames, the idle's guard on %d, blended between" % [clip, times4.size(), nfull, nguard])
	var f := FileAccess.open(OS.get_environment("SOLVE_OUT") if OS.has_environment("SOLVE_OUT") else "/tmp/guard.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out)); f.close()
	var g2 := FileAccess.open((OS.get_environment("SOLVE_OUT") if OS.has_environment("SOLVE_OUT") else "/tmp/guard.json").replace(".json", ".txt"), FileAccess.WRITE)
	g2.store_string("\n".join(lines) + "\n"); g2.close()
	quit(0)

func _score(B: Basis, Cm: Basis, C: Array, Hd: Array) -> Dictionary:
	var Bc: Basis = Cm.inverse() * B
	var ok := 0
	var defl := []; var turn := []; var qs := []
	var ch_l: Vector3 = (W_rest.basis * Vector3.UP).normalized()
	var qr: Quaternion = W_rest.basis.get_rotation_quaternion()
	for i in C.size():
		var wgl: Basis = (C[i] as Basis) * Bc
		var hw: Vector3 = (wgl * Vector3.UP).normalized(); var ew: Vector3 = (wgl * Vector3.BACK).normalized()
		var tl: float = rad_to_deg(hw.angle_to(U))
		if tl >= 30.0 and tl <= 60.0 and hw.dot(F) > 0.0 and hw.dot(R) > 0.0 and absf(rad_to_deg(atan2(ew.dot(R), ew.dot(F)))) <= 45.0:
			ok += 1
		var loc: Basis = (Hd[i] as Basis).inverse() * wgl
		var q: Quaternion = _q(loc)
		qs.append(q)
		defl.append(rad_to_deg((loc * Vector3.UP).normalized().angle_to(ch_l)))
		turn.append(rad_to_deg(q.angle_to(qr)))
	defl.sort(); turn.sort()
	return {"pass": float(ok) / float(C.size()), "defl_med": float(defl[defl.size() / 2]), "defl_p90": float(defl[int(defl.size() * 0.9)]),
			"turn_med": float(turn[turn.size() / 2]), "qs": qs}

func _q(b: Basis) -> Quaternion:
	return b.orthonormalized().get_rotation_quaternion()

func _key_times(clip: String) -> Array:
	var a := ap.get_animation(clip)
	for t in a.get_track_count():
		if a.track_get_type(t) == Animation.TYPE_ROTATION_3D and String(a.track_get_path(t).get_concatenated_subnames()) == "RightHand":
			var ts := []
			for i in a.track_get_key_count(t): ts.append(a.track_get_key_time(t, i))
			return ts
	return []

func _qmean(qs: Array) -> Quaternion:
	var ref: Quaternion = qs[0]
	var acc := Vector4.ZERO
	for q in qs:
		var v := Vector4(q.x, q.y, q.z, q.w)
		if v.dot(Vector4(ref.x, ref.y, ref.z, ref.w)) < 0.0: v = -v
		acc += v
	acc = acc.normalized()
	return Quaternion(acc.x, acc.y, acc.z, acc.w)

func _axe() -> void:
	var mi: MeshInstance3D = (k.gear["_pieces"]["axe"] as Array)[0]
	var bind := Transform3D()
	for i in mi.skin.get_bind_count():
		if String(mi.skin.get_bind_name(i)) == "weapon_r": bind = mi.skin.get_bind_pose(i)
	var verts: PackedVector3Array = mi.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
	var hi := -1e9
	for v in verts: hi = maxf(hi, (bind * v).y)
	head_w = Vector3(0, hi * 0.85, 0)
