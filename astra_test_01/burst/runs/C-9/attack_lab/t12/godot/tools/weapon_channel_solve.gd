extends SceneTree
# T12 rank 3: THE WEAPON CHANNEL, solved per frame for weapon_r and written as rotation keys.
#
# weapon_r's rest is the MOUNT (the square seat, roll 0): origin at the grip, +Y along the haft to
# the head, +Z toward the edge. A rotation track on it turns the axe ABOUT THE GRIP, whatever the
# wrist does, so the arm keeps its motion and the weapon keeps its angle.
#
#   HOLD clips (walk_armed, run_armed, run_armed_L/R, strafe_L/R_armed, block): the axe at GUARD in
#   the CHEST frame. The guard is set per clip so that at the clip's MEAN chest orientation -- the
#   one the viewer sees, i.e. through the tree for the split gaits -- the haft is 45 deg from
#   vertical, leaning forward and outboard equally, with the edge facing his forward; frame by
#   frame it then rides the chest. weapon_r_local(t) = (chest^-1 hand)(t)^-1 x guard_in_chest --
#   which depends on the ARM CHAIN ONLY, so it stays right under the speed split's unarmed hips.
#   STRIKES (attack, attack_chop): slow frames hold the guard (in his frame, so the fade from the
#   locomotion guard has nothing to turn); fast frames roll the mounted axe about its haft until
#   the EDGE lies along the head's travel; blended by the head's speed (smoothstep, 15-35% of the
#   clip's peak). The haft's own path is the clip's: the strike still peaks where it did.
#   IDLE: the new armed idle (the unarmed idle's legs and breathing, both arms fixed from a clean
#   armed frame) is solved like a hold clip, from `IDLE_ARMS` = clip@t.
# env: SOLVE_OUT (json), IDLE_ARMS (clip@t, optional)
const F := Vector3(0, 0, 1)
const U := Vector3(0, 1, 0)
const R := Vector3(-1, 0, 0)
const HOLD := ["walk_armed", "run_armed", "run_armed_L", "run_armed_R", "strafe_L_armed", "strafe_R_armed", "block"]
const SPLIT := {"walk_armed": ["walk", false], "run_armed": ["run", true]}
const STRIKES := ["attack", "attack_chop"]
const ARMS := ["LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand", "RightShoulder", "RightArm", "RightForeArm", "RightHand"]
var k
var skel: Skeleton3D
var ap: AnimationPlayer
var tree: AnimationTree
var s_ := 1.0
var hb := -1
var wb := -1
var chb := -1
var W_rest := Transform3D()
var head_w := Vector3.ZERO       # the head point in weapon_r's frame
var B_star := Basis()            # the guard in his frame: columns X, Y = haft, Z = edge
var out := {}
var lines := []

func say(s: String) -> void:
	lines.append(s); print(s)

func _initialize() -> void:
	create_timer(1200.0).timeout.connect(func(): print("[solve] WATCHDOG"); quit(4))
	k = load("res://scripts/knight.gd").new()
	k.setup(Vector3.RIGHT, Vector3.UP, Vector3.FORWARD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	for i in 4: await process_frame
	skel = k._skel
	ap = k._anim
	tree = k._tree
	s_ = skel.global_transform.basis.get_scale().x
	hb = skel.find_bone("RightHand"); wb = skel.find_bone("weapon_r"); chb = skel.find_bone("Spine")
	if wb < 0:
		print("[solve] no weapon_r on this rig"); quit(5); return
	for c in skel.get_children():
		if c is SkeletonModifier3D: (c as SkeletonModifier3D).active = false
	W_rest = skel.get_bone_rest(wb)
	_axe()
	var h_star := (F * 0.5 + R * 0.5 + U * sqrt(0.5)).normalized()
	var e_star := (F - F.dot(h_star) * h_star).normalized()
	B_star = Basis(h_star.cross(e_star).normalized(), h_star, e_star)
	say("[solve] guard in his frame: haft tilt %.1f deg, fwd %+.2f out %+.2f; edge heading %+.1f deg"
		% [rad_to_deg(h_star.angle_to(U)), h_star.dot(F), h_star.dot(R), rad_to_deg(atan2(e_star.dot(R), e_star.dot(F)))])
	# ---- mean chest per hold clip: through the TREE for the split gaits, raw for the rest -----
	var mean_chest := {}
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	for clip in SPLIT.keys():
		var g: Array = SPLIT[clip]
		k.global_position = Vector3(0, 0.03, 0)
		var qs := []
		for i in 96:
			k.drive_dir(Vector2(1, 0), bool(g[1]), 1.0 / 24.0)
			tree.advance(1.0 / 24.0)
			if i >= 48: qs.append(skel.get_bone_global_pose(chb).basis.orthonormalized().get_rotation_quaternion())
		for i in 36:
			k.drive_dir(Vector2.ZERO, false, 1.0 / 24.0); tree.advance(1.0 / 24.0)
		mean_chest[clip] = _qmean(qs)
	tree.active = false
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	for clip in HOLD:
		if SPLIT.has(clip): continue
		var qs2 := []
		for t in _key_times(clip):
			ap.play(clip); ap.seek(t, true, true)
			qs2.append(skel.get_bone_global_pose(chb).basis.orthonormalized().get_rotation_quaternion())
		mean_chest[clip] = _qmean(qs2)
	# ---- HOLD clips ------------------------------------------------------------------------
	var solved := {}
	for clip in HOLD:
		var Bc: Basis = Basis(mean_chest[clip] as Quaternion).inverse() * B_star
		var times := _key_times(clip)
		var qs3 := []
		var dev := []
		ap.play(clip)
		for t in times:
			ap.seek(t, true, true)
			var cb: Basis = skel.get_bone_global_pose(chb).basis.orthonormalized()
			var hbs: Basis = skel.get_bone_global_pose(hb).basis.orthonormalized()
			var q: Quaternion = (hbs.inverse() * cb * Bc).orthonormalized().get_rotation_quaternion()
			qs3.append(q)
			dev.append(rad_to_deg(q.angle_to(W_rest.basis.get_rotation_quaternion())))
		solved[clip] = {"times": times, "quats": qs3.map(func(q): return [q.x, q.y, q.z, q.w])}
		dev.sort()
		say("[solve] %-15s %3d keys | the axe turned in the fist from its mount by median %.0f deg, p90 %.0f" % [clip, times.size(), float(dev[dev.size() / 2]), float(dev[int(dev.size() * 0.9)])])
	# ---- STRIKES -----------------------------------------------------------------------------
	for clip in STRIKES:
		var times2 := _key_times(clip)
		ap.play(clip)
		var hands := []; var heads := []
		for t in times2:
			ap.seek(t, true, true)
			var hg: Transform3D = skel.get_bone_global_pose(hb)
			hands.append(hg)
			heads.append((hg * W_rest) * head_w)
		var sp := []
		for i in times2.size():
			var i0: int = maxi(i - 1, 0); var i1: int = mini(i + 1, times2.size() - 1)
			sp.append(((heads[i1] as Vector3) - (heads[i0] as Vector3)).length() * s_ / maxf(float(times2[i1]) - float(times2[i0]), 1e-6))
		var pk := 0.0
		for v in sp: pk = maxf(pk, float(v))
		var qs4 := []
		var lead := []
		for i in times2.size():
			var hbs2: Basis = (hands[i] as Transform3D).basis.orthonormalized()
			var q_guard: Quaternion = (hbs2.inverse() * B_star).orthonormalized().get_rotation_quaternion()
			var Wm: Basis = hbs2 * W_rest.basis.orthonormalized()
			var h: Vector3 = (Wm * Vector3.UP).normalized()
			var em: Vector3 = (Wm * Vector3.BACK).normalized()
			var i0: int = maxi(i - 1, 0); var i1: int = mini(i + 1, times2.size() - 1)
			var v: Vector3 = (heads[i1] as Vector3) - (heads[i0] as Vector3)
			var u: Vector3 = v - v.dot(h) * h
			var q_lead: Quaternion = W_rest.basis.get_rotation_quaternion()
			if u.length() > 1e-9:
				u = u.normalized()
				var phi: float = atan2(em.cross(u).dot(h), em.dot(u))
				q_lead = (hbs2.inverse() * Basis(h, phi) * Wm).orthonormalized().get_rotation_quaternion()
			var x: float = clampf((float(sp[i]) / maxf(pk, 1e-6) - 0.15) / 0.20, 0.0, 1.0)
			var b: float = x * x * (3.0 - 2.0 * x)
			if q_guard.dot(q_lead) < 0.0: q_lead = -q_lead
			qs4.append(q_guard.slerp(q_lead, b))
			lead.append(b)
		solved[clip] = {"times": times2, "quats": qs4.map(func(q): return [q.x, q.y, q.z, q.w])}
		var nfull := lead.filter(func(b): return float(b) >= 0.999).size()
		say("[solve] %-15s %3d keys | peak head speed %.2f m/s; edge-leading weight 1 on %d frames, guard on %d" % [clip, times2.size(), pk, nfull, lead.filter(func(b): return float(b) <= 0.001).size()])
	# ---- IDLE: the unarmed idle's body, the arms fixed from a clean armed frame --------------
	var ia: String = OS.get_environment("IDLE_ARMS") if OS.has_environment("IDLE_ARMS") else ""
	if ia != "":
		var pr: PackedStringArray = ia.split("@")
		ap.play(pr[0]); ap.seek(float(pr[1]), true, true)
		var arms := {}
		for bn in ARMS:
			var q5: Quaternion = skel.get_bone_pose_rotation(skel.find_bone(bn))
			arms[bn] = [q5.x, q5.y, q5.z, q5.w]
		# the idle's frames with those arms: chest from the idle, hand = chest x fixed arm chain
		var times3 := _key_times("idle")
		ap.play("idle")
		var qs_c := []
		var hic := []
		for t in times3:
			ap.seek(t, true, true)
			for bn in ARMS:
				var a2: Array = arms[bn]
				skel.set_bone_pose_rotation(skel.find_bone(bn), Quaternion(a2[0], a2[1], a2[2], a2[3]))
			var cb2: Basis = skel.get_bone_global_pose(chb).basis.orthonormalized()
			qs_c.append(cb2.get_rotation_quaternion())
			hic.append(cb2.inverse() * skel.get_bone_global_pose(hb).basis.orthonormalized())
		var Bc2: Basis = Basis(_qmean(qs_c)).inverse() * B_star
		var qs6 := []
		for i in times3.size():
			qs6.append(((hic[i] as Basis).inverse() * Bc2).orthonormalized().get_rotation_quaternion())
		solved["idle_guard"] = {"times": times3, "quats": qs6.map(func(q): return [q.x, q.y, q.z, q.w]), "arms_from": ia, "arms": arms}
		say("[solve] idle_guard      %3d keys | the unarmed idle, arms fixed from %s" % [times3.size(), ia])
	out["weapon_r"] = solved
	out["guard_his_frame"] = {"haft": [B_star.y.x, B_star.y.y, B_star.y.z], "edge": [B_star.z.x, B_star.z.y, B_star.z.z]}
	var f := FileAccess.open(OS.get_environment("SOLVE_OUT") if OS.has_environment("SOLVE_OUT") else "/tmp/solve.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out)); f.close()
	quit(0)

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
	var c := Vector3.ZERO
	var all := []
	for v in verts:
		var p: Vector3 = bind * v; all.append(p); c += p
	c /= float(all.size())
	# the haft in weapon_r's frame should be +Y (the mount's construction): check it
	var xx := 0.0; var xy := 0.0; var xz := 0.0; var yy := 0.0; var yz := 0.0; var zz := 0.0
	for p in all:
		var d: Vector3 = p - c
		xx += d.x * d.x; xy += d.x * d.y; xz += d.x * d.z; yy += d.y * d.y; yz += d.y * d.z; zz += d.z * d.z
	var ax := Vector3(0, 1, 0)
	for it in 60:
		ax = Vector3(xx * ax.x + xy * ax.y + xz * ax.z, xy * ax.x + yy * ax.y + yz * ax.z, xz * ax.x + yz * ax.y + zz * ax.z).normalized()
	if ax.y < 0.0: ax = -ax
	var hi := -1e9
	for p in all: hi = maxf(hi, (p as Vector3).dot(ax))
	head_w = ax * hi * 0.85
	say("[solve] the haft in weapon_r's frame is %.2f deg off +Y (the mount's construction); head point %.3f m out along it"
		% [rad_to_deg(ax.angle_to(Vector3.UP)), head_w.length() * s_])
