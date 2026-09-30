extends SceneTree
# THE STANDING PER-CLIP WEAPON TABLE (T12 rank 6, checks 2-4) -- every clip of the GLB, raw (the
# AnimationPlayer seeked, the tree and every skeleton modifier off), the axe carried by whichever
# bone its skin binds (RightHand today, weapon_r after the rebind):
#   HOLD      the guard predicate, per frame: tilt 30-60 deg from vertical, haft forward > 0 and
#             outboard > 0, head outboard of the fist, |edge heading| <= 45 deg; medians and the
#             fraction of frames that pass. Skeleton frame: forward +Z, up +Y, his right -X.
#   EDGE      on the strikes: the ledger's instrument (probe_armed_measure._edge -- normalize(edge
#             - hand) . normalize(edge travel) on frames at >= 20% of peak marker speed: frames
#             leading, best margin), the edge's facing along the head's travel in the impact
#             window (>= 50% of peak head speed), and the edge heading at the impact frame.
#   ARC       the axe head's screen path through the combat-lane camera (orthographic, pitch
#             52.9535 deg, 77.8 px per metre = a 1.8 m figure at 140 px), for the eight direction
#             cells (camera yaw 47 + k x 45 deg off his forward): total path per clip and the
#             peak single-frame step (24 fps), min-max across the cells.
# env: TABLE_OUT (json), TABLE_LABEL
const F := Vector3(0, 0, 1)
const U := Vector3(0, 1, 0)
const R := Vector3(-1, 0, 0)
const PX_PER_M := 77.8
const PITCH_DEG := 52.9535411256029
const STRIKES := ["attack", "attack_chop"]
var k
var skel: Skeleton3D
var ap: AnimationPlayer
var s_ := 1.0
var bone := -1
var hand := -1
var H := Vector3.ZERO
var E := Vector3.ZERO
var head_l := Vector3.ZERO
var grip_l := Vector3.ZERO
var edge_l := Vector3.ZERO

func _initialize() -> void:
	var wd := Time.get_ticks_msec() + 900000
	# a coroutine that dies on an error never reaches quit(): a main-loop timer still fires
	create_timer(900.0).timeout.connect(func(): print("[table] WATCHDOG"); quit(4))
	var label: String = OS.get_environment("TABLE_LABEL") if OS.has_environment("TABLE_LABEL") else "?"
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
	hand = skel.find_bone("RightHand")
	(k._tree as AnimationTree).active = false
	for c in skel.get_children():
		if c is SkeletonModifier3D:
			(c as SkeletonModifier3D).active = false
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	_axe()
	var table := {}
	for clip in ap.get_animation_list():
		if Time.get_ticks_msec() > wd:
			print("[table] WATCHDOG"); quit(4); return
		table[String(clip)] = _clip(String(clip))
	var out := {"label": label, "axe_bone": skel.get_bone_name(bone), "bones": skel.get_bone_count(),
				"predicate": "tilt 30-60 deg, haft fwd > 0, haft out > 0, head outboard > 0, |edge| <= 45 deg",
				"arc": "combat-lane camera, ortho, pitch %.4f deg, %.1f px/m, yaw 47 + k*45 deg" % [PITCH_DEG, PX_PER_M],
				"clips": table}
	var f := FileAccess.open(OS.get_environment("TABLE_OUT") if OS.has_environment("TABLE_OUT") else "/tmp/table.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " ")); f.close()
	for clip in table.keys():
		var r: Dictionary = table[clip]
		var e := ""
		if r.has("edge_lead"):
			var ed: Dictionary = r["edge_lead"]
			e = " | EDGE leads %d/%d best %.3f, facing (peak window) %.3f, heading at peak %+.0f; at the cut's strike (%.2f s) heading %+.0f, edge on travel %+.2f" % [int(ed["leads"]), int(ed["frames"]), float(ed["best"]), float(ed["facing"]), float(ed["heading_impact"]), float(ed["strike_t"]), float(ed["heading_strike"]), float(ed["on_travel_strike"])]
		print("[table] %-9s %-28s tilt %5.1f fwd %+.2f out %+.2f head out %+.3f edge %+5.0f | pass %3d%% | arc %4.0f-%4.0f px, peak step %5.1f px%s"
			% [label, clip, float(r["tilt"]), float(r["fwd"]), float(r["out"]), float(r["head_out"]), float(r["edge"]),
			   int(round(100.0 * float(r["pass_frac"]))), float(r["arc_min"]), float(r["arc_max"]), float(r["step_max"]), e])
	quit(0)

func _axe() -> void:
	var mi: MeshInstance3D = (k.gear["_pieces"]["axe"] as Array)[0]
	var bind := Transform3D()
	for i in mi.skin.get_bind_count():
		var n := String(mi.skin.get_bind_name(i))
		if n == "weapon_r" or (n == "RightHand" and bone < 0):
			bind = mi.skin.get_bind_pose(i); bone = skel.find_bone(n)
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
	edge_l = mk.transform.origin
	# the marker's attachment may be a different bone from the skin's (hand vs weapon bone):
	# express it in the skin bone's frame
	var att := mk.get_parent() as BoneAttachment3D
	if att != null and skel.find_bone(att.bone_name) != bone:
		var ab := skel.find_bone(att.bone_name)
		edge_l = skel.get_bone_global_rest(bone).affine_inverse() * (skel.get_bone_global_rest(ab) * edge_l)
	if (edge_l - c).dot(ax) < 0.0: ax = -ax
	H = ax
	E = ((edge_l - c) - (edge_l - c).dot(H) * H).normalized()
	head_l = c + H * (edge_l - c).dot(H)
	grip_l = c + H * (-c).dot(H)

func _cam_axes(yaw_deg: float) -> Array:
	var y := deg_to_rad(yaw_deg); var th := deg_to_rad(PITCH_DEG)
	var fh := Vector3(sin(y), 0, cos(y))
	var d := (fh * cos(th) + Vector3(0, -1, 0) * sin(th)).normalized()
	var r := fh.cross(Vector3.UP).normalized()
	var u := r.cross(d).normalized()
	return [r, u]

func _clip(clip: String) -> Dictionary:
	var a := ap.get_animation(clip)
	var n: int = maxi(int(round(a.length * 24.0)), 1)
	ap.play(clip)
	var rows := []
	for i in n + 1:
		ap.seek(a.length * float(i) / float(n), true, true)
		var g: Transform3D = skel.get_bone_global_pose(bone)
		var h: Vector3 = (g.basis * H).normalized()
		var e: Vector3 = (g.basis * E).normalized()
		var head: Vector3 = (g * head_l) * s_
		var fist: Vector3 = (g * grip_l) * s_
		var d: Vector3 = head - fist
		var hipo: Vector3 = skel.get_bone_global_pose(skel.find_bone("Hips")).origin * s_
		rows.append({"reach": (head - hipo).dot(F), "tilt": rad_to_deg(h.angle_to(U)), "fwd": h.dot(F), "out": h.dot(R), "head_out": d.dot(R),
					 "edge": rad_to_deg(atan2(e.dot(R), e.dot(F))), "head": head, "e": e, "h": h,
					 "marker": (g * edge_l) * s_, "hand": skel.get_bone_global_pose(hand).origin * s_})
	var md := func(key: String) -> float:
		var v := rows.map(func(r): return float(r[key])); v.sort(); return float(v[v.size() / 2])
	var ok := 0
	for r in rows:
		if float(r["tilt"]) >= 30.0 and float(r["tilt"]) <= 60.0 and float(r["fwd"]) > 0.0 and float(r["out"]) > 0.0 \
				and float(r["head_out"]) > 0.0 and absf(float(r["edge"])) <= 45.0:
			ok += 1
	var out := {"frames": rows.size(), "tilt": md.call("tilt"), "fwd": md.call("fwd"), "out": md.call("out"),
				"head_out": md.call("head_out"), "edge": md.call("edge"), "pass_frac": float(ok) / float(rows.size())}
	# ARC per cell
	var arcs := []; var steps := []
	for kk in 8:
		var ax: Array = _cam_axes(47.0 + 45.0 * float(kk))
		var tot := 0.0; var pk := 0.0
		for i in range(1, rows.size()):
			var dv: Vector3 = (rows[i]["head"] as Vector3) - (rows[i - 1]["head"] as Vector3)
			var px: float = Vector2(dv.dot(ax[0]), dv.dot(ax[1])).length() * PX_PER_M
			tot += px; pk = maxf(pk, px)
		arcs.append(tot); steps.append(pk)
	arcs.sort(); steps.sort()
	out["arc_min"] = float(arcs[0]); out["arc_max"] = float(arcs[-1]); out["step_max"] = float(steps[-1])
	# EDGE on the strikes
	if clip in STRIKES:
		var mx := 0.0
		for i in range(1, rows.size()): mx = maxf(mx, ((rows[i]["marker"] as Vector3) - (rows[i - 1]["marker"] as Vector3)).length())
		var leads := 0; var cnt := 0; var best := -1.0
		for i in range(1, rows.size()):
			var v: Vector3 = (rows[i]["marker"] as Vector3) - (rows[i - 1]["marker"] as Vector3)
			if v.length() < mx * 0.2: continue
			cnt += 1
			var arm: Vector3 = (rows[i]["marker"] as Vector3) - (rows[i]["hand"] as Vector3)
			if arm.length() < 1e-6 or v.length() < 1e-9: continue
			var l: float = arm.normalized().dot(v.normalized())
			if l > 0.0: leads += 1
			best = maxf(best, l)
		var sp := [0.0]
		for i in range(1, rows.size()): sp.append(((rows[i]["head"] as Vector3) - (rows[i - 1]["head"] as Vector3)).length())
		var pk2 := 0
		for i in sp.size():
			if float(sp[i]) > float(sp[pk2]): pk2 = i
		var i0 := pk2; var i1 := pk2
		while i0 > 1 and float(sp[i0 - 1]) >= 0.5 * float(sp[pk2]): i0 -= 1
		while i1 < sp.size() - 1 and float(sp[i1 + 1]) >= 0.5 * float(sp[pk2]): i1 += 1
		var fs := 0.0; var ws := 0.0
		for i in range(maxi(i0, 1), i1 + 1):
			var v2: Vector3 = (rows[i]["head"] as Vector3) - (rows[i - 1]["head"] as Vector3)
			var hh: Vector3 = rows[i]["h"]
			var uu: Vector3 = v2 - v2.dot(hh) * hh
			if uu.length() < 1e-9: continue
			fs += uu.length() * (rows[i]["e"] as Vector3).dot(uu.normalized()); ws += uu.length()
		# THE CUT'S STRIKE (14_axe_assert): the frame the head reaches furthest forward of the hips
		var fr := 0
		for i in rows.size():
			if float(rows[i]["reach"]) > float(rows[fr]["reach"]): fr = i
		var fa: int = clampi(fr - 1, 0, rows.size() - 1); var fb: int = clampi(fr + 1, 0, rows.size() - 1)
		var vf: Vector3 = (rows[fb]["head"] as Vector3) - (rows[fa]["head"] as Vector3)
		var hf: Vector3 = rows[fr]["h"]
		var uf: Vector3 = vf - vf.dot(hf) * hf
		var on_travel: float = (rows[fr]["e"] as Vector3).dot(uf.normalized()) if uf.length() > 1e-9 else 0.0
		out["edge_lead"] = {"leads": leads, "frames": cnt, "best": best, "facing": fs / maxf(ws, 1e-9),
					   "heading_impact": float(rows[pk2]["edge"]), "impact_t": a.length * float(pk2) / float(n),
					   "strike_t": a.length * float(fr) / float(n), "heading_strike": float(rows[fr]["edge"]), "on_travel_strike": on_travel}
	return out
