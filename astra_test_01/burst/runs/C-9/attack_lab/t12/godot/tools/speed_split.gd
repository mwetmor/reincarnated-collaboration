extends SceneTree
# ARMED SPEED -- Matt: "even the run speed slows way down when I put on the axe/shield."
# One knight, driven through the tree the way the game drives it, unarmed (stack 0) and armed
# (the full kit), at figure scale 1.0 on flat ground, 1/24 s steps:
#   speed     the body's measured ground speed (displacement / time) in steady walk and run
#   slide     planted-foot travel per frame -- the transitions probe's own test (the lower toe,
#             the same foot two frames running, both near the floor): steady walk, steady run,
#             and the walk -> run -> walk -> run crossover
#   seam      the waist: Spine02's rotation relative to Hips, its per-frame step (p95, max, in
#             deg per 1/24 s), and the chest's horizontal twist off the hips (median, range)
#   hold      the axe: tilt from vertical, lean fwd/out, head outboard of the fist, edge
#             heading -- skeleton frame, forward +Z, up +Y, his right -X
# env: SPLIT_LABEL, SPLIT_OUT
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
var H := Vector3.ZERO
var E := Vector3.ZERO
var head_l := Vector3.ZERO
var grip_l := Vector3.ZERO
var bi := {}

func _initialize() -> void:
	var wd_ms := Time.get_ticks_msec() + 600000
	var label: String = OS.get_environment("SPLIT_LABEL") if OS.has_environment("SPLIT_LABEL") else "?"
	var ground := StaticBody3D.new()
	ground.collision_layer = CliffWorld.TERRAIN_BIT
	var cs := CollisionShape3D.new(); var box := BoxShape3D.new(); box.size = Vector3(4000, 1, 4000)
	cs.shape = box; cs.position = Vector3(0, -0.5, 0); ground.add_child(cs); root.add_child(ground)
	k = load("res://scripts/knight.gd").new()
	k.setup(RIGHT, UP, FWD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	skel = k._skel
	tree = k._tree
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	for bn in ["Hips", "Spine02", "Spine", "LeftToeBase", "RightToeBase", "RightHand"]:
		bi[bn] = skel.find_bone(bn)
	var out := {"label": label}
	for st in [["unarmed", 0], ["armed", k.gear_stack_count() - 1]]:
		k.set_gear_stack(int(st[1]))
		if st[0] == "armed":
			_axe()
		k.global_position = Vector3(0, 0.03, 0)
		k.velocity = Vector3.ZERO
		out[st[0]] = await _run_state(String(st[0]))
		if Time.get_ticks_msec() > wd_ms:
			print("[split] WATCHDOG"); quit(4); return
	var f := FileAccess.open(OS.get_environment("SPLIT_OUT") if OS.has_environment("SPLIT_OUT") else "/tmp/split.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " ")); f.close()
	for s in ["unarmed", "armed"]:
		var o: Dictionary = out[s]
		print("[split] %-8s %-7s walk %.3f m/s (%.1f px/s) run %.3f m/s (%.1f px/s) | slide walk %.1f/%.1f run %.1f/%.1f cross %.1f/%.1f/%.1f mm (%d pairs) | seam step walk %.1f/%.1f run %.1f/%.1f cross %.1f/%.1f deg, pop (ang. accel) walk %.1f/%.1f run %.1f/%.1f cross %.1f/%.1f | twist walk %+.1f (%.1f..%.1f) run %+.1f (%.1f..%.1f)"
			% [label, s, float(o["walk"]["speed_m_s"]), float(o["walk"]["speed_px_s"]), float(o["run"]["speed_m_s"]), float(o["run"]["speed_px_s"]),
			   float(o["walk"]["slide_med_mm"]), float(o["walk"]["slide_max_mm"]), float(o["run"]["slide_med_mm"]), float(o["run"]["slide_max_mm"]),
			   float(o["cross"]["slide_med_mm"]), float(o["cross"]["slide_p95_mm"]), float(o["cross"]["slide_max_mm"]), int(o["cross"]["slide_pairs"]),
			   float(o["walk"]["seam_p95"]), float(o["walk"]["seam_max"]), float(o["run"]["seam_p95"]), float(o["run"]["seam_max"]),
			   float(o["cross"]["seam_p95"]), float(o["cross"]["seam_max"]),
			   float(o["walk"]["acc_p95"]), float(o["walk"]["acc_max"]), float(o["run"]["acc_p95"]), float(o["run"]["acc_max"]),
			   float(o["cross"]["acc_p95"]), float(o["cross"]["acc_max"]),
			   float(o["walk"]["twist_med"]), float(o["walk"]["twist_lo"]), float(o["walk"]["twist_hi"]),
			   float(o["run"]["twist_med"]), float(o["run"]["twist_lo"]), float(o["run"]["twist_hi"])])
		if s == "armed":
			for g in ["walk", "run"]:
				var h: Dictionary = o[g]["hold"]
				print("[split] %-8s armed   %s hold: tilt %.1f deg, lean fwd %+.2f out %+.2f, head outboard %+.3f m, edge %+.0f deg | predicate frames %d of %d"
					% [label, g, float(h["tilt"]), float(h["fwd"]), float(h["out"]), float(h["head_out"]), float(h["edge"]), int(h["pass"]), int(h["n"])])
	print("[split] %s ratio armed/unarmed: walk %.3f run %.3f" % [label,
		float(out["armed"]["walk"]["speed_m_s"]) / maxf(float(out["unarmed"]["walk"]["speed_m_s"]), 1e-6),
		float(out["armed"]["run"]["speed_m_s"]) / maxf(float(out["unarmed"]["run"]["speed_m_s"]), 1e-6)])
	quit(0)

func _axe() -> void:
	var mi: MeshInstance3D = (k.gear["_pieces"]["axe"] as Array)[0]
	var bind := Transform3D()
	var bone_name := "RightHand"
	for i in mi.skin.get_bind_count():
		var n := String(mi.skin.get_bind_name(i))
		if n == "RightHand" or n == "weapon_r":
			bind = mi.skin.get_bind_pose(i); bone_name = n
	bi["axe_bone"] = skel.find_bone(bone_name)
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

func _step(dir: Vector2, run: bool) -> void:
	k.drive_dir(dir, run, DT)
	tree.advance(DT)
	skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)

func _sample() -> Dictionary:
	var g := skel.global_transform
	var lf: Vector3 = g * skel.get_bone_global_pose(bi["LeftToeBase"]).origin
	var rf: Vector3 = g * skel.get_bone_global_pose(bi["RightToeBase"]).origin
	var sp: Quaternion = skel.get_bone_pose_rotation(bi["Spine02"])
	var hips_b: Basis = skel.get_bone_global_pose(bi["Hips"]).basis.orthonormalized()
	var chest_b: Basis = skel.get_bone_global_pose(bi["Spine"]).basis.orthonormalized()
	# horizontal forward of each, from the rig's own +Z at rest
	var rest_h: Basis = skel.get_bone_global_rest(bi["Hips"]).basis.orthonormalized()
	var rest_c: Basis = skel.get_bone_global_rest(bi["Spine"]).basis.orthonormalized()
	var fh: Vector3 = hips_b * (rest_h.inverse() * F); fh.y = 0.0
	var fc: Vector3 = chest_b * (rest_c.inverse() * F); fc.y = 0.0
	var tw: float = rad_to_deg(atan2(fh.normalized().cross(fc.normalized()).y, fh.normalized().dot(fc.normalized())))
	var s := {"body": k.global_position, "lf": lf, "rf": rf, "sp": sp, "twist": tw,
			  "w": float(tree.get("parameters/bl_wr/blend_amount")), "a": float(tree.get("parameters/bl_iw/blend_amount")),
			  "cyc": float(k.get("_cycle_len")), "uw": float(tree.get("parameters/a_walk_u/current_position")) if k.get("_upper_on") != null else -1.0,
			  "ur": float(tree.get("parameters/a_run_u/current_position")) if k.get("_upper_on") != null else -1.0}
	if bi.has("axe_bone") and k.armed():
		var hg: Transform3D = skel.get_bone_global_pose(int(bi["axe_bone"]))
		var h: Vector3 = (hg.basis * H).normalized()
		var e: Vector3 = (hg.basis * E).normalized()
		var d: Vector3 = (hg * head_l - hg * grip_l) * g.basis.get_scale().x
		s["hold"] = {"tilt": rad_to_deg(h.angle_to(U)), "fwd": h.dot(F), "out": h.dot(R), "head_out": d.dot(R),
					 "edge": rad_to_deg(atan2(e.dot(R), e.dot(F)))}
	return s

func _run_state(name: String) -> Dictionary:
	for i in 24: _step(Vector2.ZERO, false)
	var res := {}
	for gait in [["walk", false], ["run", true]]:
		var rows := []
		for i in 96:
			_step(Vector2(1, 0), bool(gait[1]))
			if i >= 36: rows.append(_sample())
		res[gait[0]] = _summarise(rows)
		for i in 36: _step(Vector2.ZERO, false)
	# THE CROSSOVER, four times from four different standing phases, ONE direction (a 180 deg
	# turn swings a planted foot round the body and is not a gait-blend slide), pairs pooled
	var pooled := []
	var seam_steps := []
	var seam_acc := []
	for rep in 4:
		for i in 7 * rep + 5: _step(Vector2.ZERO, false)
		var rows2 := []
		for leg in [[22, false], [26, true], [22, false], [26, true]]:
			for i in int(leg[0]):
				_step(Vector2(1, 0), bool(leg[1]))
				rows2.append(_sample())
		var sm := _summarise(rows2)
		# WHERE IS THE BIGGEST POP: the seam's angular acceleration by frame, with the weights
		var vv := []
		for i in range(1, rows2.size()):
			var dq: Quaternion = (rows2[i - 1]["sp"] as Quaternion).inverse() * (rows2[i]["sp"] as Quaternion)
			if dq.w < 0.0: dq = -dq
			vv.append(Vector3(dq.x, dq.y, dq.z) * 2.0)
		var worst := 0.0; var wi := 0
		for i in range(1, vv.size()):
			var aa: float = rad_to_deg(((vv[i] as Vector3) - (vv[i - 1] as Vector3)).length())
			if aa > worst: worst = aa; wi = i + 1
		var ctx := []
		for j in range(maxi(wi - 2, 0), mini(wi + 2, rows2.size())):
			ctx.append("f%d w%.2f a%.2f cyc%.3f uw%.2f ur%.2f" % [j, float(rows2[j]["w"]), float(rows2[j]["a"]), float(rows2[j]["cyc"]), float(rows2[j]["uw"]), float(rows2[j]["ur"])])
		print("[split]   %s rep %d worst pop %.1f at frame %d: %s" % [name, rep, worst, wi, " | ".join(ctx)])
		pooled.append_array(sm["slides"])
		seam_steps.append_array(sm["steps"])
		seam_acc.append_array(sm["acc"])
		for i in 36: _step(Vector2.ZERO, false)
	pooled.sort(); seam_steps.sort(); seam_acc.sort()
	res["cross"] = {"slide_med_mm": float(pooled[pooled.size() / 2]), "slide_p95_mm": float(pooled[int(pooled.size() * 0.95)]),
					"slide_max_mm": float(pooled[-1]), "slide_pairs": pooled.size(),
					"seam_p95": float(seam_steps[int(seam_steps.size() * 0.95)]), "seam_max": float(seam_steps[-1]),
					"acc_p95": float(seam_acc[int(seam_acc.size() * 0.95)]), "acc_max": float(seam_acc[-1])}
	return res

func _summarise(rows: Array) -> Dictionary:
	var n := rows.size()
	var disp: Vector3 = (rows[-1]["body"] as Vector3) - (rows[0]["body"] as Vector3)
	disp.y = 0.0
	var spd: float = disp.length() / (float(n - 1) * DT)
	# planted-foot travel (the transitions probe's rule)
	var lows := []
	for r in rows:
		lows.append(minf((r["lf"] as Vector3).y, (r["rf"] as Vector3).y) - (r["body"] as Vector3).y)
	lows.sort()
	var fy: float = float(lows[0])
	var sl := []
	for i in range(1, n):
		var a: Dictionary = rows[i - 1]; var b: Dictionary = rows[i]
		var la: bool = (a["lf"] as Vector3).y <= (a["rf"] as Vector3).y
		var lb: bool = (b["lf"] as Vector3).y <= (b["rf"] as Vector3).y
		if la != lb: continue
		var pa: Vector3 = a["lf"] if la else a["rf"]
		var pb: Vector3 = b["lf"] if lb else b["rf"]
		var ha: float = pa.y - (a["body"] as Vector3).y
		var hb: float = pb.y - (b["body"] as Vector3).y
		if ha <= fy + 0.03 and hb <= fy + 0.03 and absf(ha - hb) <= 0.010:
			sl.append((pb - pa).length() * 1000.0)
	sl.sort()
	var steps := []
	var vel := []
	for i in range(1, n):
		var qa: Quaternion = rows[i - 1]["sp"]; var qb: Quaternion = rows[i]["sp"]
		var dq: Quaternion = qa.inverse() * qb
		if dq.w < 0.0: dq = -dq
		vel.append(Vector3(dq.x, dq.y, dq.z) * 2.0)
		steps.append(rad_to_deg(qa.angle_to(qb)))
	var acc := []
	for i in range(1, vel.size()):
		acc.append(rad_to_deg(((vel[i] as Vector3) - (vel[i - 1] as Vector3)).length()))
	var steps_raw := steps.duplicate()
	steps.sort()
	acc.sort()
	var tws := rows.map(func(r): return float(r["twist"])); tws.sort()
	var out := {"speed_m_s": spd, "speed_px_s": float(k.speed_px_s()), "frames": n,
				"slide_med_mm": float(sl[sl.size() / 2]) if sl.size() > 0 else -1.0, "slide_max_mm": float(sl[-1]) if sl.size() > 0 else -1.0,
				"slide_pairs": sl.size(), "seam_p95": float(steps[int(steps.size() * 0.95)]), "seam_max": float(steps[-1]),
				"acc_p95": float(acc[int(acc.size() * 0.95)]) if acc.size() > 0 else 0.0, "acc_max": float(acc[-1]) if acc.size() > 0 else 0.0,
				"slides": sl, "steps": steps_raw, "acc": acc,
				"twist_med": float(tws[tws.size() / 2]), "twist_lo": float(tws[0]), "twist_hi": float(tws[-1])}
	if rows[0].has("hold"):
		var keys := ["tilt", "fwd", "out", "head_out", "edge"]
		var hold := {}
		for key in keys:
			var v := rows.map(func(r): return float(r["hold"][key])); v.sort()
			hold[key] = float(v[v.size() / 2])
		var ok := 0
		for r in rows:
			var h: Dictionary = r["hold"]
			if float(h["tilt"]) >= 30.0 and float(h["tilt"]) <= 60.0 and float(h["fwd"]) > 0.0 and float(h["out"]) > 0.0 \
					and float(h["head_out"]) > 0.0 and absf(float(h["edge"])) <= 45.0:
				ok += 1
		hold["pass"] = ok; hold["n"] = n
		out["hold"] = hold
	return out
