extends SceneTree
# THE WEAPON CHANNEL, solved on the clips AS THE SCENE BLENDS THEM (the tree, the split, the axe
# guard layer at its configured weight) and keyed on each SOURCE clip's own time:
#   walk -> walk_armed, run -> run_armed (the split's upper clips), strafe_l/_r -> strafe_L/R_armed.
# Per frame: the smallest turn of the haft into the guard predicate with a 5 deg margin (tilt
# 35-55, forward and outboard >= 0.1) -- 0 when it is already inside -- and the roll about the
# haft that brings the edge within 40 deg of his forward. Resampled onto a uniform key grid of the
# clip, wrapped (the clips loop).
#   STRIKES (attack, attack_chop), raw: weapon_r at its rest (the mount) when the head is slow;
# when fast, the mounted axe rolled about its haft until the edge lies along the head's travel;
# blended by the head's speed (smoothstep over 15-35% of the clip's peak). Keyed on the clip's
# frames. The haft never leaves the fist's channel in a strike: only its roll changes.
# env: RESID_OUT (json)
const DT := 1.0 / 24.0
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
const F := Vector3(0, 0, 1)
const U := Vector3(0, 1, 0)
const R := Vector3(-1, 0, 0)
var k
var skel: Skeleton3D
var tree: AnimationTree
var ap: AnimationPlayer
var s_ := 1.0
var hb := -1
var wb := -1
var W_rest := Transform3D()
var head_l := Vector3.ZERO
var region := []

func _initialize() -> void:
	create_timer(1500.0).timeout.connect(func(): print("[resid] WATCHDOG"); quit(4))
	var ground := StaticBody3D.new()
	ground.collision_layer = CliffWorld.TERRAIN_BIT
	var cs := CollisionShape3D.new(); var box := BoxShape3D.new(); box.size = Vector3(4000, 1, 4000)
	cs.shape = box; cs.position = Vector3(0, -0.5, 0); ground.add_child(cs); root.add_child(ground)
	k = load("res://scripts/knight.gd").new()
	k.setup(RIGHT, UP, FWD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	for i in 4: await process_frame
	skel = k._skel; tree = k._tree; ap = k._anim
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	for c in skel.get_children():
		if c is SkeletonModifier3D: (c as SkeletonModifier3D).active = false
	s_ = skel.global_transform.basis.get_scale().x
	hb = skel.find_bone("RightHand"); wb = skel.find_bone("weapon_r")
	W_rest = skel.get_bone_rest(wb)
	var mi: MeshInstance3D = (k.gear["_pieces"]["axe"] as Array)[0]
	var bind := Transform3D()
	for i in mi.skin.get_bind_count():
		if String(mi.skin.get_bind_name(i)) == "weapon_r": bind = mi.skin.get_bind_pose(i)
	var hi := -1e9
	for v in (mi.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX] as PackedVector3Array): hi = maxf(hi, (bind * v).y)
	head_l = Vector3(0, hi * 0.85, 0)
	for tilt in range(35, 56):
		for az in range(10, 81):
			var h: Vector3 = (F * cos(deg_to_rad(az)) + R * sin(deg_to_rad(az))) * sin(deg_to_rad(tilt)) + U * cos(deg_to_rad(tilt))
			if h.dot(F) >= 0.1 and h.dot(R) >= 0.1: region.append(h)
	var out := {"weapon_r": {}, "weight": float((k.cfg["arm_layer_armed_R"] as Dictionary)["weight"])}
	for spec in [["walk", "walk_armed", "a_walk_u"], ["run", "run_armed", "a_run_u"],
				 ["strafe_l", "strafe_L_armed", "a_strafe"], ["strafe_r", "strafe_R_armed", "a_strafe"]]:
		var r := await _loco(String(spec[0]), String(spec[1]), String(spec[2]))
		out["weapon_r"][spec[1]] = r
		print("[resid] %-15s %3d keys from %3d frames | turn into the guard median %.1f p90 %.1f deg, roll median %.1f; %d%% of frames needed none"
			% [String(spec[1]), (r["times"] as Array).size(), int(r["frames"]), float(r["turn_med"]), float(r["turn_p90"]), float(r["roll_med"]), int(100.0 * float(r["zero_frac"]))])
	tree.active = false
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	for clip in ["attack", "attack_chop"]:
		var r2 := _strike(clip)
		out["weapon_r"][clip] = r2
		print("[resid] %-15s %3d keys | edge rolled onto the travel on %d frames, the mount on %d; roll max %.0f deg" % [clip, (r2["times"] as Array).size(), int(r2["full"]), int(r2["rest"]), float(r2["roll_max"])])
	var f := FileAccess.open(OS.get_environment("RESID_OUT") if OS.has_environment("RESID_OUT") else "/tmp/resid.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out)); f.close()
	quit(0)

func _step(dir: Vector2, run: bool) -> void:
	k.drive_dir(dir, run, DT)
	tree.advance(DT)

func _strafe_input(side: String) -> Vector2:
	var sd: Vector3 = k._strafe_dir(side)
	var want: Vector3 = (Basis(Vector3.UP, float(k.get("_yaw_cur"))) * sd).normalized()
	var best := -2.0; var pick := Vector2.ZERO
	for a in 720:
		var d := Vector2(cos(deg_to_rad(0.5 * a)), sin(deg_to_rad(0.5 * a)))
		var w3: Vector3 = k.canvas_velocity_to_world(d); w3.y = 0.0
		if w3.length() < 1e-6: continue
		var c: float = w3.normalized().dot(want)
		if c > best: best = c; pick = d
	return pick

func _residual(hg: Basis) -> Array:
	# [local weapon_r rotation, the haft's turn (deg), the roll (deg)]
	var wg: Basis = hg * W_rest.basis.orthonormalized()
	var h: Vector3 = (wg * Vector3.UP).normalized(); var e: Vector3 = (wg * Vector3.BACK).normalized()
	var tl: float = rad_to_deg(h.angle_to(U))
	var inside: bool = tl >= 35.0 and tl <= 55.0 and h.dot(F) >= 0.1 and h.dot(R) >= 0.1
	var q := Quaternion.IDENTITY
	var turn := 0.0
	if not inside:
		var best := -2.0; var ht := h
		for c in region:
			var d: float = h.dot(c)
			if d > best: best = d; ht = c
		q = Quaternion(h, ht)
		turn = rad_to_deg(h.angle_to(ht))
	var h2: Vector3 = (q * h).normalized(); var e2: Vector3 = (q * e).normalized()
	var hd: float = rad_to_deg(atan2(e2.dot(R), e2.dot(F)))
	var roll := 0.0
	if absf(hd) > 40.0:
		# the SMALLEST roll about the haft that brings |heading| within 40; failing that, the roll
		# that gets it nearest
		var bestr := 999.0; var fallback := 0.0; var fall_h := 999.0
		for dd in range(-180, 181, 2):
			var e3: Vector3 = (Quaternion(h2, deg_to_rad(float(dd))) * e2).normalized()
			var h3: float = absf(rad_to_deg(atan2(e3.dot(R), e3.dot(F))))
			if h3 <= 40.0 and absf(float(dd)) < absf(bestr): bestr = float(dd)
			if h3 < fall_h: fall_h = h3; fallback = float(dd)
		if bestr > 360.0: bestr = fallback
		q = Quaternion(h2, deg_to_rad(bestr)) * q
		roll = absf(bestr)
	var wl: Basis = hg.inverse() * Basis(q) * wg
	return [wl.orthonormalized().get_rotation_quaternion(), turn, roll]

func _loco(st: String, clip: String, node: String) -> Dictionary:
	k.set_block(false)
	for i in 48: _step(Vector2.ZERO, false)
	k.global_position = Vector3(0, 0.03, 0); k.velocity = Vector3.ZERO
	var dir := Vector2.ZERO; var run := false
	match st:
		"walk":
			dir = Vector2(0, 1); for i in 48: _step(dir, false)
		"run":
			dir = Vector2(0, 1); run = true; for i in 48: _step(dir, true)
		"strafe_l", "strafe_r":
			k.set_block(true); for i in 24: _step(Vector2.ZERO, false)
			dir = _strafe_input("l" if st == "strafe_l" else "r")
			for i in 36: _step(dir, false)
	var alen: float = ap.get_animation(clip).length
	var samples := []
	var turns := []; var rolls := []; var zeros := 0
	# enough frames to visit the whole source clip at least twice
	var n: int = int(ceil(2.2 * alen / DT)) if st.begins_with("strafe") else 120
	for i in n:
		_step(dir, run)
		var t: float = fposmod(float(tree.get("parameters/%s/current_position" % node)), alen)
		var r := _residual(skel.get_bone_global_pose(hb).basis.orthonormalized())
		samples.append([t, r[0]])
		turns.append(float(r[1])); rolls.append(float(r[2]))
		if float(r[1]) <= 0.0 and float(r[2]) <= 0.0: zeros += 1
	k.set_block(false)
	# resample onto the clip's own 24 fps key grid: for each key, the nearest sample in clip time
	var nk: int = int(round(alen * 24.0))
	var times := []; var quats := []
	for j in nk + 1:
		var tk: float = alen * float(j) / float(nk)
		var best := 1e9; var qb := Quaternion.IDENTITY
		var tw: float = fposmod(tk, alen)
		for sm in samples:
			var dtm: float = absf(float(sm[0]) - tw)
			dtm = minf(dtm, alen - dtm)
			if dtm < best: best = dtm; qb = sm[1]
		times.append(tk); quats.append([qb.x, qb.y, qb.z, qb.w])
	turns.sort(); rolls.sort()
	return {"times": times, "quats": quats, "frames": n, "turn_med": float(turns[turns.size() / 2]),
			"turn_p90": float(turns[int(turns.size() * 0.9)]), "roll_med": float(rolls[rolls.size() / 2]), "zero_frac": float(zeros) / float(n)}

func _strike(clip: String) -> Dictionary:
	# THE STRIKE'S ROLL. Only the ACTIVE SWING matters -- the frames contiguous with the head's peak
	# speed at >= 50% of it: the charged chop's raise, sway and wind-up are not cuts, and edge-leading
	# them spun the blade 170-177 deg in the fist mid-charge. So: one constant roll for the whole clip
	# (the swing's speed-weighted mean -- it changes inside the 0.1 s fade-in, under the arm's own
	# move into the strike), and inside the swing the exact roll that lays the edge along the travel,
	# ramped over 2 frames at each side. The haft never leaves the fist's channel: roll only.
	var a := ap.get_animation(clip)
	var n: int = int(round(a.length * 24.0))
	ap.play(clip)
	var hands := []; var heads := []; var times := []
	for i in n + 1:
		var t: float = a.length * float(i) / float(n)
		ap.seek(t, true, true)
		var hg: Transform3D = skel.get_bone_global_pose(hb)
		hands.append(hg); heads.append((hg * W_rest) * head_l); times.append(t)
	var sp := []
	for i in times.size():
		var i0: int = maxi(i - 1, 0); var i1: int = mini(i + 1, times.size() - 1)
		sp.append(((heads[i1] as Vector3) - (heads[i0] as Vector3)).length() * s_ / maxf(float(times[i1]) - float(times[i0]), 1e-6))
	var pk := 0
	for i in sp.size():
		if float(sp[i]) > float(sp[pk]): pk = i
	var w0 := pk; var w1 := pk
	while w0 > 0 and float(sp[w0 - 1]) >= 0.5 * float(sp[pk]): w0 -= 1
	while w1 < sp.size() - 1 and float(sp[w1 + 1]) >= 0.5 * float(sp[pk]): w1 += 1
	var need := []
	for i in times.size():
		var hbs: Basis = (hands[i] as Transform3D).basis.orthonormalized()
		var Wm: Basis = hbs * W_rest.basis.orthonormalized()
		var h: Vector3 = (Wm * Vector3.UP).normalized(); var em: Vector3 = (Wm * Vector3.BACK).normalized()
		var i0: int = maxi(i - 1, 0); var i1: int = mini(i + 1, times.size() - 1)
		var v: Vector3 = (heads[i1] as Vector3) - (heads[i0] as Vector3)
		var u: Vector3 = v - v.dot(h) * h
		need.append(atan2(em.cross(u.normalized()).dot(h), em.dot(u.normalized())) if u.length() > 1e-9 else 0.0)
	var cx := 0.0; var cy := 0.0
	for i in range(w0, w1 + 1):
		cx += float(sp[i]) * cos(float(need[i])); cy += float(sp[i]) * sin(float(need[i]))
	var base: float = atan2(cy, cx)
	var quats := []; var rmax := 0.0
	for i in times.size():
		var ww := 0.0
		if i >= w0 and i <= w1: ww = 1.0
		elif i >= w0 - 2 and i < w0: ww = float(i - (w0 - 3)) / 3.0
		elif i > w1 and i <= w1 + 2: ww = float((w1 + 3) - i) / 3.0
		var dlt: float = wrapf(float(need[i]) - base, -PI, PI)
		var roll: float = base + ww * dlt
		rmax = maxf(rmax, absf(rad_to_deg(roll)))
		var q: Quaternion = (W_rest.basis.orthonormalized() * Basis(Vector3.UP, roll)).orthonormalized().get_rotation_quaternion()
		quats.append([q.x, q.y, q.z, q.w])
	print("[resid] %-15s the swing %.3f-%.3f s (peak %.3f s); constant roll %+.0f deg, inside the swing %+.0f..%+.0f"
		% [clip, float(times[w0]), float(times[w1]), float(times[pk]), rad_to_deg(base),
		   rad_to_deg(base + wrapf(float(need.slice(w0, w1 + 1).min()) - base, -PI, PI)), rad_to_deg(base + wrapf(float(need.slice(w0, w1 + 1).max()) - base, -PI, PI))])
	return {"times": times, "quats": quats, "full": w1 - w0 + 1, "rest": 0, "roll_max": rmax,
			"swing": [float(times[w0]), float(times[w1])], "base_roll_deg": rad_to_deg(base)}
