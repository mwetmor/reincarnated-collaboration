extends SceneTree
# THE GUARD LAYER, measured through the TREE (what the scene shows) -- idle, walk, run, block and
# both strafes, the axe guard layer (blend_r) at each weight of WEIGHTS, weapon_r as keyed (at
# rest until the channel is baked). Per state and weight:
#   predicate  the guard predicate on the axe as drawn (tilt 30-60, haft forward and outboard,
#              head outboard of the fist, |edge heading| <= 45), % of frames
#   finish     what weapon_r must still turn to hold the guard, per frame (the FIST TURN: the haft
#              leaving the fist's channel), two ways: to the nearest point of the predicate with a
#              5 deg margin ("to region"), and to the guard the pose holds, riding the chest ("to
#              guard"); median and p90, and the roll about the haft the edge needs
#   arc        the axe head's screen path per loop at the play camera, worst of the 8 cells (px)
# env: WEIGHTS ("0,0.5,1"), STATES_OUT (json; with DUMP=1 the per-frame record for the residual
# solve: source clip, its time, the hand and chest bases)
const DT := 1.0 / 24.0
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
const F := Vector3(0, 0, 1)
const U := Vector3(0, 1, 0)
const R := Vector3(-1, 0, 0)
const PX_PER_M := 77.8
const PITCH_DEG := 52.9535411256029
var k
var skel: Skeleton3D
var tree: AnimationTree
var s_ := 1.0
var hb := -1
var wb := -1
var chb := -1
var head_l := Vector3.ZERO
var guard_c := Basis()          # the axe in the chest frame at weight 1 (the pose's own hold)
var region := []

func _initialize() -> void:
	var wd := Time.get_ticks_msec() + 1500000
	create_timer(1500.0).timeout.connect(func(): print("[states] WATCHDOG"); quit(4))
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
	skel = k._skel; tree = k._tree
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	for c in skel.get_children():
		if c is SkeletonModifier3D: (c as SkeletonModifier3D).active = false
	s_ = skel.global_transform.basis.get_scale().x
	hb = skel.find_bone("RightHand"); wb = skel.find_bone("weapon_r"); chb = skel.find_bone("Spine")
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
	# the guard the pose holds: the axe in the chest frame, with the layer at 1 and standing
	(k.cfg["arm_layer_armed_R"] as Dictionary)["weight"] = 1.0
	for i in 60: _step(Vector2.ZERO, false)
	guard_c = skel.get_bone_global_pose(chb).basis.orthonormalized().inverse() * skel.get_bone_global_pose(wb).basis.orthonormalized()
	var weights: PackedStringArray = (OS.get_environment("WEIGHTS") if OS.has_environment("WEIGHTS") else "0,0.5,1").split(",")
	var dump: bool = OS.get_environment("DUMP") == "1"
	var out := {}
	for ws in weights:
		var w := float(ws)
		(k.cfg["arm_layer_armed_R"] as Dictionary)["weight"] = w
		var res := {}
		for st in ["idle", "walk", "run", "block", "strafe_l", "strafe_r"]:
			if Time.get_ticks_msec() > wd: print("[states] WATCHDOG"); quit(4); return
			res[st] = _state(st, dump)
		out[ws] = res
		var line := "[states] w=%.2f" % w
		for st in res.keys():
			var r: Dictionary = res[st]
			line += " | %s pred %3.0f%% turn->region %4.1f/%4.1f ->guard %4.1f/%4.1f roll %4.1f arc %3.0f" % [st, 100.0 * float(r["pred"]), float(r["reg_med"]), float(r["reg_p90"]), float(r["gd_med"]), float(r["gd_p90"]), float(r["roll_med"]), float(r["arc"])]
		print(line)
	var f := FileAccess.open(OS.get_environment("STATES_OUT") if OS.has_environment("STATES_OUT") else "/tmp/states.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out)); f.close()
	quit(0)

func _step(dir: Vector2, run: bool) -> void:
	k.drive_dir(dir, run, DT)
	tree.advance(DT)

func _settle() -> void:
	k.set_block(false)
	for i in 48: _step(Vector2.ZERO, false)

func _strafe_input(side: String) -> Vector2:
	# the canvas direction that points along his strafe direction NOW -- found without stepping
	# him (a non-strafing input turns him, and chasing it never lands on his right)
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


func _state(st: String, dump: bool) -> Dictionary:
	_settle()
	k.global_position = Vector3(0, 0.03, 0); k.velocity = Vector3.ZERO
	var n := 0
	var src := ""
	var dir := Vector2.ZERO
	var run := false
	match st:
		"idle":
			n = 96; src = "a_idle"
		"walk":
			dir = Vector2(0, 1); for i in 48: _step(dir, false)
			n = int(round(float(k.get("_cycle_len")) / DT)); src = "a_walk_u"
		"run":
			dir = Vector2(0, 1); run = true; for i in 48: _step(dir, true)
			n = int(round(float(k.get("_cycle_len")) / DT)); src = "a_run_u"
		"block":
			k.set_block(true); for i in 36: _step(Vector2.ZERO, false)
			n = 48; src = "a_block"
		"strafe_l", "strafe_r":
			k.set_block(true); for i in 24: _step(Vector2.ZERO, false)
			dir = _strafe_input("l" if st == "strafe_l" else "r")
			for i in 36: _step(dir, false)
			n = int(round(2.4583 / DT)); src = "a_strafe"
	var ok := 0
	var reg := []; var gd := []; var rolls := []
	var heads := []
	var rec := []
	var chest_q := []
	for i in n:
		_step(dir, run)
		var wg: Basis = skel.get_bone_global_pose(wb).basis.orthonormalized()
		var cg: Basis = skel.get_bone_global_pose(chb).basis.orthonormalized()
		var h: Vector3 = (wg * Vector3.UP).normalized(); var e: Vector3 = (wg * Vector3.BACK).normalized()
		var tl: float = rad_to_deg(h.angle_to(U)); var hd: float = rad_to_deg(atan2(e.dot(R), e.dot(F)))
		if tl >= 30.0 and tl <= 60.0 and h.dot(F) > 0.0 and h.dot(R) > 0.0 and absf(hd) <= 45.0: ok += 1
		# to region: the nearest haft with the margin; then the roll the edge needs (to +-40)
		var best := -2.0; var ht := h
		for c in region:
			var d: float = h.dot(c)
			if d > best: best = d; ht = c
		var inside: bool = tl >= 35.0 and tl <= 55.0 and h.dot(F) >= 0.1 and h.dot(R) >= 0.1
		var arc: float = 0.0 if inside else rad_to_deg(h.angle_to(ht))
		var q := Quaternion(h, ht) if not inside else Quaternion.IDENTITY
		var e2: Vector3 = (q * e).normalized()
		var hd2: float = rad_to_deg(atan2(e2.dot(R), e2.dot(F)))
		var roll: float = maxf(0.0, absf(hd2) - 40.0)
		reg.append(arc); rolls.append(roll)
		# to guard: the pose's own hold, riding the chest
		var gw: Basis = cg * guard_c
		gd.append(rad_to_deg(h.angle_to((gw * Vector3.UP).normalized())))
		heads.append((skel.get_bone_global_pose(wb) * head_l) * s_)
		var cq: Quaternion = cg.get_rotation_quaternion()
		chest_q.append([cq.x, cq.y, cq.z, cq.w])
		if dump:
			rec.append({"t": float(tree.get("parameters/%s/current_position" % src)),
						"hand": _bq(skel.get_bone_global_pose(hb).basis), "chest": _bq(cg), "wr": _bq(wg)})
	reg.sort(); gd.sort(); rolls.sort()
	var arc_worst := 0.0
	for kk in 8:
		var y := deg_to_rad(47.0 + 45.0 * float(kk)); var th := deg_to_rad(PITCH_DEG)
		var fh := Vector3(sin(y), 0, cos(y))
		var dv := (fh * cos(th) + Vector3(0, -1, 0) * sin(th)).normalized()
		var rr := fh.cross(Vector3.UP).normalized(); var uu := rr.cross(dv).normalized()
		var tot := 0.0
		for i in range(1, heads.size()):
			var dd: Vector3 = (heads[i] as Vector3) - (heads[i - 1] as Vector3)
			tot += Vector2(dd.dot(rr), dd.dot(uu)).length() * PX_PER_M
		arc_worst = maxf(arc_worst, tot)
	var qsum := Vector4.ZERO; var qref := Quaternion.IDENTITY; var first := true
	for i in range(0, 1):
		pass
	var out := {"pred": float(ok) / float(n), "reg_med": float(reg[reg.size() / 2]), "reg_p90": float(reg[int(reg.size() * 0.9)]),
				"gd_med": float(gd[gd.size() / 2]), "gd_p90": float(gd[int(gd.size() * 0.9)]), "roll_med": float(rolls[rolls.size() / 2]),
				"arc": arc_worst, "frames": n, "src": src, "chest_q": chest_q}
	if dump: out["rec"] = rec
	k.set_block(false)
	return out

func _bq(b: Basis) -> Array:
	var q: Quaternion = b.orthonormalized().get_rotation_quaternion()
	return [q.x, q.y, q.z, q.w]
