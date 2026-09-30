extends SceneTree
# GRIP CALIBRATION -- re-seat the axe square in the fist, solve the ONE roll about the haft so
# the edge leads in the strikes' impact windows, and score the result across all 19 clips.
#
# Everything is in the RightHand bone's LOCAL frame -- the frame the skin's bind pose lives in,
# so a grip is exactly  bind' = G * bind  with  G = rotation Q about pivot P. That G is the data
# the manifest carries (one rotation per weapon per hand), and it is the same thing a weapon
# bone's rest offset would be.
#
#   SEAT   the haft is turned in the fist (shortest arc) onto the fist's CHANNEL: the across-palm
#          axis of the hand mesh, found by PCA of the vertices weighted to RightHand -- the
#          D2 pipeline's own hand_frame() construction. Pivot = the point of the current haft
#          nearest the fist's centroid, so the haft still passes through the middle of the fist.
#   ROLL   one angle about the seated haft, closed form: maximise the speed-weighted mean of
#          (edge direction . travel direction perpendicular to the haft) over the impact window
#          of each axe strike (frames at >= 50% of that strike's peak head speed), clips weighted
#          equally.
#   SCORE  per clip, BEFORE (G = identity) and AFTER:
#          - tilt / lean / head vs fist / edge heading (skeleton frame: fwd +Z, up +Y, right -X)
#          - axe-body penetration: every 4th axe vertex, crossing parity along +Y against the
#            POSED body mesh with its morphs (CPU skin bake -> TriangleMesh). The FIST is
#            excluded: a point counts as in the fist when BOTH the first hit above it and the
#            first hit below it are hand triangles (RightHand-dominant) -- the closed hand
#            surrounds it. Anything else inside counts, forearm included.
#          - edge leading, the ledger's instrument (probe_armed_measure._edge: normalize(edge -
#            hand) . normalize(edge travel), frames at >= 20% of peak marker speed; count > 0 and
#            best), plus the physical facing above
#          - wrist reversals (27_armed_carry's rule, 30 fps, 1 deg dead band) -- invariant to the
#            seat by construction, measured anyway -- and haft-tilt reversals (what the eye sees)
#          - fist fit: closed-fist finger vertices to the haft surface
# env: GRIP_MODE=survey|full   GRIP_SEAT=channel|square_bone   LAB_OUT=<json>
const F := Vector3(0, 0, 1)
const U := Vector3(0, 1, 0)
const R := Vector3(-1, 0, 0)
const STRIKES := ["attack", "attack_chop"]
var k
var skel: Skeleton3D
var ap: AnimationPlayer
var s_ := 1.0
var hb := -1
var fb := -1
var body: MeshInstance3D
var proxy: MeshInstance3D
var tri_hand := PackedByteArray()
var tri_bone := PackedInt32Array()
# axe, hand-local
var H := Vector3.ZERO
var E := Vector3.ZERO
var head_l := Vector3.ZERO
var edge_l := Vector3.ZERO
var P := Vector3.ZERO
var pts_l := PackedVector3Array()
var haft_r := 0.0
# hand frame, hand-local
var C_f := Vector3.ZERO
var along := Vector3.ZERO
var channel := Vector3.ZERO
var palm := Vector3.ZERO
var Ah := Vector3.ZERO
var hand_w := 0.0
var fingers_closed := PackedVector3Array()
var lines := []
var out := {}

func say(s: String) -> void:
	lines.append(s); print(s)

func _initialize() -> void:
	create_timer(1500.0).timeout.connect(func(): push_error("WATCHDOG"); quit(4))
	var mode: String = OS.get_environment("GRIP_MODE") if OS.has_environment("GRIP_MODE") else "survey"
	var seat_kind: String = OS.get_environment("GRIP_SEAT") if OS.has_environment("GRIP_SEAT") else "channel"
	k = load("res://scripts/knight.gd").new()
	k.setup(Vector3.RIGHT, Vector3.UP, Vector3.FORWARD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	for i in 4: await process_frame
	skel = k._skel
	ap = k._anim
	body = k._mesh
	s_ = skel.global_transform.basis.get_scale().x
	hb = skel.find_bone("RightHand")
	fb = skel.find_bone("RightForeArm")
	(k._tree as AnimationTree).active = false
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	# RAW CLIPS: every skeleton modifier off, so a forced skeleton update shows the clip and nothing
	# else (with the foot lock's IK live, the bake disagreed with the clip by 2 cm on a leg)
	for c in skel.get_children():
		if c is SkeletonModifier3D:
			(c as SkeletonModifier3D).active = false
	_axe_geom()
	_hand_frame()
	# ---- the seat ----------------------------------------------------------------------
	var gh: Transform3D = skel.get_bone_global_rest(hb)
	var gf: Transform3D = skel.get_bone_global_rest(fb)
	Ah = (gh.basis.inverse() * (gh.origin - gf.origin)).normalized()
	var ch_s := channel if channel.dot(H) >= 0.0 else -channel
	var sq_b := (H - H.dot(Ah) * Ah).normalized()
	say("[grip] hand frame (mesh PCA, RightHand weight > 0.30, %d vertices): along->haft %.1f deg, channel->haft %.1f, palm normal->haft %.1f; bone hand axis->haft %.1f"
		% [int(out.get("hand_vertices", 0)), rad_to_deg(along.angle_to(H)), rad_to_deg(channel.angle_to(H)), rad_to_deg(palm.angle_to(H)), rad_to_deg(Ah.angle_to(H))])
	say("[grip] mesh 'along' is %.1f deg from the bone hand axis; fist width across the channel %.3f m; fist centroid is %.4f m off the haft axis"
		% [rad_to_deg(along.angle_to(Ah)), hand_w * s_, _line_dist(C_f, P, H) * s_])
	say("[grip] seat options: channel (sign toward the current head) -> %.1f deg turn, %.1f deg to the bone hand axis; bone-square -> %.1f deg turn, %.1f deg from the channel"
		% [rad_to_deg(H.angle_to(ch_s)), rad_to_deg(ch_s.angle_to(Ah)), rad_to_deg(H.angle_to(sq_b)), rad_to_deg(sq_b.angle_to(ch_s))])
	var grest: Basis = skel.get_bone_global_rest(hb).basis.orthonormalized()
	say("[grip] at REST, in his frame (fwd +Z, out = his right -X, up +Y): fingers %s, channel(+toward head) %s, palm normal %s"
		% [str(Vector3((grest * along).dot(F), (grest * along).dot(R), (grest * along).dot(U)).snappedf(0.01)),
		   str(Vector3((grest * ch_s).dot(F), (grest * ch_s).dot(R), (grest * ch_s).dot(U)).snappedf(0.01)),
		   str(Vector3((grest * palm).dot(F), (grest * palm).dot(R), (grest * palm).dot(U)).snappedf(0.01))])
	# the thumb side from the mesh: near the wrist the thumb's base makes the hand asymmetric
	# across the channel -- the side with the more vertices close to the wrist is the thumb's
	var near := [0, 0]
	var arr0 := body.mesh.surface_get_arrays(0)
	var v0: PackedVector3Array = arr0[Mesh.ARRAY_VERTEX]
	var bind0 := _bind_of(body.skin, "RightHand")
	var bns = arr0[Mesh.ARRAY_BONES]; var wts = arr0[Mesh.ARRAY_WEIGHTS]
	var nbw: int = int(bns.size() / v0.size())
	var rhb := _bind_index(body.skin, "RightHand")
	var thumbish := Vector3.ZERO
	var cnt := 0
	for vi in v0.size():
		var w := 0.0
		for j in nbw:
			if int(bns[vi * nbw + j]) == rhb: w += float(wts[vi * nbw + j])
		if w < 0.3: continue
		var pl: Vector3 = bind0 * v0[vi]
		var al: float = pl.dot(along)
		if al < C_f.dot(along) - 0.02 / s_:     # the wrist half of the hand
			var sd: float = (pl - C_f).dot(ch_s)
			if sd > 0.0: near[0] += 1
			else: near[1] += 1
	say("[grip] wrist-half hand vertices on the +channel side %d, on the -channel side %d (the thumb's base sits on the heavier side)" % [near[0], near[1]])
	var T_dir: Vector3 = ch_s if seat_kind == "channel" else (-ch_s if seat_kind == "channel_neg" else sq_b)
	var Q1 := Quaternion(H, T_dir)
	var E1: Vector3 = (Q1 * E).normalized()
	var N1: Vector3 = T_dir.cross(E1).normalized()
	# ---- the roll ----------------------------------------------------------------------
	var d_head: float = (head_l - P).dot(H)
	var solve := {}
	var AA := 0.0
	var BB := 0.0
	var before_face := 0.0
	for clip in STRIKES:
		var r := _roll_terms(clip, T_dir, E1, N1, d_head)
		solve[clip] = r
		AA += float(r["A"]); BB += float(r["B"]); before_face += float(r["before"])
	var phi: float = atan2(BB, AA)
	var j0: float = AA / float(STRIKES.size())
	var jphi: float = (AA * cos(phi) + BB * sin(phi)) / float(STRIKES.size())
	say("[grip] roll solve: edge-facing objective (mean over %s, speed-weighted cos in the impact window): before %.3f | seat, no roll %.3f | seat + roll %+.1f deg -> %.3f"
		% [str(STRIKES), before_face / float(STRIKES.size()), j0, rad_to_deg(phi), jphi])
	for clip in STRIKES:
		var r: Dictionary = solve[clip]
		say("[grip]   %-11s window %.2f-%.2f s (%d frames, peak head %.2f m/s at %.2f s): before %.3f, after %.3f"
			% [clip, float(r["w0"]), float(r["w1"]), int(r["n"]), float(r["peak"]), float(r["peak_t"]), float(r["before"]),
			   (float(r["A"]) * cos(phi) + float(r["B"]) * sin(phi))])
	# THE ROLL SWEEP: edge-leading objective vs |edge heading| AT IMPACT (the peak-speed frame),
	# both strikes -- the constraint the conductor set (|heading| <= 45 deg at impact)
	var best_c := -1e9; var best_phi := phi; var sweep := []
	for dd in range(-180, 180, 5):
		var ph: float = deg_to_rad(float(dd))
		var obj := 0.0; var hs := []; var ok := true
		for clip in STRIKES:
			var r: Dictionary = solve[clip]
			obj += float(r["A"]) * cos(ph) + float(r["B"]) * sin(ph)
			var e: Vector3 = (r["e1_pk"] as Vector3) * cos(ph) + (r["n1_pk"] as Vector3) * sin(ph)
			var hd: float = rad_to_deg(atan2(e.dot(R), e.dot(F)))
			var hw := []
			for j in (r["e1s"] as Array).size():
				var ew: Vector3 = (r["e1s"][j] as Vector3) * cos(ph) + (r["n1s"][j] as Vector3) * sin(ph)
				hw.append(absf(rad_to_deg(atan2(ew.dot(R), ew.dot(F)))))
			hw.sort()
			var ef: Vector3 = (r["e1_fw"] as Vector3) * cos(ph) + (r["n1_fw"] as Vector3) * sin(ph)
			hs.append([hd, float(hw[hw.size() / 2]), rad_to_deg(atan2(ef.dot(R), ef.dot(F))), ef.dot(r["u_fw"] as Vector3)])
			if absf(hd) > 45.0: ok = false
		obj /= float(STRIKES.size())
		sweep.append({"roll": dd, "objective": obj, "heading_impact": hs, "ok": ok})
		if ok and obj > best_c: best_c = obj; best_phi = ph
	var line := ""
	for rw in sweep:
		if int(rw["roll"]) % 15 == 0 and int(rw["roll"]) >= -75 and int(rw["roll"]) <= 75:
			line += "\n[grip]     roll %+4d: peak-window lead %+.2f | at furthest forward: heading slash %+4.0f chop %+4.0f, edge-on-travel slash %+.2f chop %+.2f%s" % [int(rw["roll"]), float(rw["objective"]), float(rw["heading_impact"][0][2]), float(rw["heading_impact"][1][2]), float(rw["heading_impact"][0][3]), float(rw["heading_impact"][1][3]), "   <- both |heading| <= 45" if absf(float(rw["heading_impact"][0][2])) <= 45.0 and absf(float(rw["heading_impact"][1][2])) <= 45.0 else ""]
	say("[grip] roll sweep  roll:objective/heading-at-impact slash,chop  (* = both within 45 deg)%s" % line)
	for clip in STRIKES:
		say("[grip]   %-11s BEFORE (current mount): edge heading %+.0f deg at peak speed (%.2f s), %+.0f deg at furthest forward (%.2f s); the head travels at heading %+.0f there"
			% [clip, float(solve[clip]["before_heading_pk"]), float(solve[clip]["peak_t"]), float(solve[clip]["before_heading_fw"]), float(solve[clip]["fw_t"]), float(solve[clip]["travel_heading_fw"])])
	if OS.get_environment("GRIP_ROLL") == "constrained" or OS.get_environment("GRIP_ROLL") == "":
		say("[grip] roll chosen: %+.1f deg (best edge-leading objective %.3f with |heading at impact| <= 45 deg on both strikes; unconstrained best %+.1f)"
			% [rad_to_deg(best_phi), best_c, rad_to_deg(phi)])
		phi = best_phi
		jphi = best_c
	elif OS.get_environment("GRIP_ROLL") != "free":
		phi = deg_to_rad(float(OS.get_environment("GRIP_ROLL")))
		jphi = (AA * cos(phi) + BB * sin(phi)) / float(STRIKES.size())
		say("[grip] roll given: %+.1f deg (objective %.3f)" % [rad_to_deg(phi), jphi])
	out["roll_sweep"] = sweep
	for clip in STRIKES:
		for key in ["e1_pk", "n1_pk", "e1s", "n1s", "e1_fw", "n1_fw", "u_fw"]:
			(solve[clip] as Dictionary).erase(key)
	var Qroll := Quaternion(T_dir, phi)
	var Q: Quaternion = (Qroll * Q1).normalized()
	var G := Transform3D(Basis(Q), P - Q * P)
	var E2: Vector3 = (Q * E).normalized()
	say("[grip] G: rotation %.2f deg about axis %s, pivot %s (hand-local units; %.4f m per unit)"
		% [rad_to_deg(Q.get_angle()), str(Q.get_axis().snappedf(0.0001)), str(P.snappedf(0.001)), s_])
	out["grip"] = {"quat_xyzw": [Q.x, Q.y, Q.z, Q.w], "pivot_hand_local": [P.x, P.y, P.z], "units_m": s_,
				   "seat": seat_kind, "seat_turn_deg": rad_to_deg(H.angle_to(T_dir)), "roll_deg": rad_to_deg(phi),
				   "haft_to_bone_hand_axis_deg": {"before": rad_to_deg(H.angle_to(Ah)), "after": rad_to_deg(T_dir.angle_to(Ah))},
				   "haft_to_mesh_hand_axis_deg": {"before": rad_to_deg(H.angle_to(along)), "after": rad_to_deg(T_dir.angle_to(along))},
				   "objective": {"before": before_face / float(STRIKES.size()), "seat_only": j0, "after": jphi},
				   "haft_after_hand_local": [T_dir.x, T_dir.y, T_dir.z], "edge_after_hand_local": [E2.x, E2.y, E2.z],
				   "solve": solve}
	for clip in ["idle_armed", "walk_armed", "run_armed", "block"]:
		var a2 := ap.get_animation(clip)
		var n2: int = int(round(a2.length * 24.0))
		ap.play(clip)
		var tl := []; var fw := []; var ot := []; var ed := []
		for i in n2 + 1:
			ap.seek(a2.length * float(i) / float(n2), true, true)
			var gb2: Basis = skel.get_bone_global_pose(hb).basis.orthonormalized()
			var hv: Vector3 = (gb2 * T_dir).normalized(); var ev: Vector3 = (gb2 * E2).normalized()
			tl.append(rad_to_deg(hv.angle_to(U))); fw.append(hv.dot(F)); ot.append(hv.dot(R)); ed.append(rad_to_deg(atan2(ev.dot(R), ev.dot(F))))
		tl.sort(); fw.sort(); ot.sort(); ed.sort()
		say("[grip]   hold with this seat: %-11s tilt %5.1f fwd %+.2f out %+.2f edge %+4.0f" % [clip, float(tl[tl.size() / 2]), float(fw[fw.size() / 2]), float(ot[ot.size() / 2]), float(ed[ed.size() / 2])])
	# fist fit
	var ff_b := _fist_fit(P, H)
	var ff_a := _fist_fit(P, T_dir)
	say("[grip] fist fit (closed fist, finger half of the hand, %d vertices): distance to the haft surface median %.4f / p90 %.4f m BEFORE -> %.4f / %.4f m AFTER"
		% [fingers_closed.size(), ff_b[0], ff_b[1], ff_a[0], ff_a[1]])
	out["fist_fit"] = {"before": ff_b, "after": ff_a}
	if mode == "full":
		await _score({"before": Transform3D.IDENTITY, "after": G}, {"before": [H, E], "after": [T_dir, E2]})
	var outp: String = OS.get_environment("LAB_OUT") if OS.has_environment("LAB_OUT") else "/tmp/grip.json"
	var f := FileAccess.open(outp, FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " ")); f.close()
	var g := FileAccess.open(outp.replace(".json", ".txt"), FileAccess.WRITE)
	g.store_string("\n".join(lines) + "\n"); g.close()
	quit(0)

# ---------------------------------------------------------------------------------------
func _line_dist(p: Vector3, a: Vector3, d: Vector3) -> float:
	var v := p - a
	return (v - v.dot(d) * d).length()

func _bind_of(sk: Skin, bone: String) -> Transform3D:
	for i in sk.get_bind_count():
		if String(sk.get_bind_name(i)) == bone: return sk.get_bind_pose(i)
	return Transform3D()

func _bind_index(sk: Skin, bone: String) -> int:
	for i in sk.get_bind_count():
		if String(sk.get_bind_name(i)) == bone: return i
	return -1

func _pca(pts: Array, c: Vector3) -> Array:
	var xx := 0.0; var xy := 0.0; var xz := 0.0; var yy := 0.0; var yz := 0.0; var zz := 0.0
	for p in pts:
		var d: Vector3 = p - c
		xx += d.x * d.x; xy += d.x * d.y; xz += d.x * d.z; yy += d.y * d.y; yz += d.y * d.z; zz += d.z * d.z
	var mv := func(v: Vector3) -> Vector3:
		return Vector3(xx * v.x + xy * v.y + xz * v.z, xy * v.x + yy * v.y + yz * v.z, xz * v.x + yz * v.y + zz * v.z)
	var a := Vector3(1, 0.3, 0.2).normalized()
	for it in 100: a = (mv.call(a) as Vector3).normalized()
	var b := Vector3(0.2, 1, 0.3)
	for it in 100:
		b = mv.call(b) as Vector3
		b = (b - b.dot(a) * a).normalized()
	return [a, b, a.cross(b).normalized()]

func _axe_geom() -> void:
	var mi: MeshInstance3D = (k.gear["_pieces"]["axe"] as Array)[0]
	var bind := _bind_of(mi.skin, "RightHand")
	var verts: PackedVector3Array = mi.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
	var c := Vector3.ZERO
	var all := []
	for v in verts:
		var p: Vector3 = bind * v; all.append(p); c += p
	c /= float(all.size())
	var ax: Vector3 = _pca(all, c)[0]
	var mk: Node3D = (k.gear["_pieces"]["_markers_axe"] as Dictionary)["axe_edge"]
	edge_l = mk.transform.origin
	if (edge_l - c).dot(ax) < 0.0: ax = -ax
	H = ax
	E = ((edge_l - c) - (edge_l - c).dot(H) * H).normalized()
	head_l = c + H * (edge_l - c).dot(H)
	for i in range(0, all.size(), 4): pts_l.append(all[i])
	out["axe_vertices"] = all.size()
	out["axe_sampled"] = pts_l.size()
	# keep c for the pivot (set after the hand frame)
	P = c

func _hand_frame() -> void:
	var arr := body.mesh.surface_get_arrays(0)
	var verts: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
	var bones = arr[Mesh.ARRAY_BONES]
	var weights = arr[Mesh.ARRAY_WEIGHTS]
	var nb: int = int(bones.size() / verts.size())
	var skn: Skin = body.skin
	var rh := _bind_index(skn, "RightHand")
	var bind: Transform3D = skn.get_bind_pose(rh)
	# per-vertex RightHand weight -> per-triangle "hand" flag (mean over its corners > 0.5)
	var wrh := PackedFloat32Array(); wrh.resize(verts.size())
	var dom := PackedInt32Array(); dom.resize(verts.size())
	var pts := []
	var idx_hand := []
	for vi in verts.size():
		var w := 0.0
		var bw := 0.0; var bb := -1
		for j in nb:
			var ww: float = float(weights[vi * nb + j])
			var bi: int = int(bones[vi * nb + j])
			if bi == rh: w += ww
			if ww > bw: bw = ww; bb = bi
		wrh[vi] = w
		dom[vi] = bb
		if w > 0.30:
			pts.append(bind * verts[vi]); idx_hand.append(vi)
	var ix: PackedInt32Array = arr[Mesh.ARRAY_INDEX]
	var nt: int = ix.size() / 3
	tri_hand.resize(nt)
	tri_bone.resize(nt)
	for t in nt:
		var a: int = ix[3 * t]; var b: int = ix[3 * t + 1]; var cc: int = ix[3 * t + 2]
		tri_hand[t] = 1 if (wrh[a] + wrh[b] + wrh[cc]) / 3.0 > 0.5 else 0
		tri_bone[t] = dom[a]
	out["hand_vertices"] = pts.size()
	var c := Vector3.ZERO
	for p in pts: c += p
	c /= float(pts.size())
	C_f = c
	var ev := _pca(pts, c)
	# gearlib.hand_frame: 'along' is whichever of the first two axes points from the wrist to the
	# centroid; the channel is the next one; the palm normal completes the frame
	var a0: Vector3 = ev[0]; var a1: Vector3 = ev[1]
	along = a0 if absf(a0.dot(c)) > absf(a1.dot(c)) else a1
	if along.dot(c) < 0.0: along = -along
	var rest := []
	for v in [ev[0], ev[1], ev[2]]:
		if absf((v as Vector3).dot(along)) < 0.9: rest.append(v)
	channel = (rest[0] as Vector3).normalized() if rest.size() > 0 else ev[2]
	palm = along.cross(channel).normalized()
	var lo := 1e9; var hi := -1e9
	for p in pts:
		var s: float = (p - c).dot(channel); lo = minf(lo, s); hi = maxf(hi, s)
	hand_w = hi - lo
	# pivot: ON THE HAFT at the fist. The PCA line runs through the whole axe's centroid, which
	# the blade's mass pulls off the haft; so the haft's own cross-section at the fist's level
	# is averaged (axe points within 3 cm along the axis of the fist), and the pivot is that.
	var s0: float = (C_f - P).dot(H)
	var sec := Vector3.ZERO
	var ns := 0
	var sec_pts := []
	for p in pts_l:
		if absf((p - P).dot(H) - s0) * s_ < 0.03:
			sec += p; ns += 1; sec_pts.append(p)
	if ns > 8:
		P = sec / float(ns)
	else:
		P = P + H * s0
	# haft radius at the pivot: the thin core (p25 of the radial spread in that section)
	var rs := []
	for p in sec_pts:
		rs.append(_line_dist(p, P, H))
	rs.sort()
	haft_r = float(rs[rs.size() / 4]) if rs.size() > 8 else 0.02 / s_
	# the edge direction and the head point, re-taken from the haft line itself
	E = ((edge_l - P) - (edge_l - P).dot(H) * H).normalized()
	head_l = P + H * (edge_l - P).dot(H)
	out["pivot_section_points"] = ns
	out["haft_radius_m"] = haft_r * s_
	# the CLOSED fist (morphs as equipped) for the fit check, and the proxy for the pose bakes
	var mix: ArrayMesh = body.bake_mesh_from_current_blend_shape_mix()
	var marr := mix.surface_get_arrays(0)
	var mverts: PackedVector3Array = marr[Mesh.ARRAY_VERTEX]
	for vi in idx_hand:
		var p: Vector3 = bind * mverts[vi]
		if (p - Vector3.ZERO).dot(along) > C_f.dot(along):
			fingers_closed.append(p)
	var parr := arr.duplicate()
	parr[Mesh.ARRAY_VERTEX] = mverts
	if marr[Mesh.ARRAY_NORMAL] != null: parr[Mesh.ARRAY_NORMAL] = marr[Mesh.ARRAY_NORMAL]
	var am := ArrayMesh.new()
	var flags := 0
	if nb == 8: flags = Mesh.ARRAY_FLAG_USE_8_BONE_WEIGHTS
	am.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, parr, [], {}, flags)
	proxy = MeshInstance3D.new()
	proxy.mesh = am
	proxy.visible = false
	skel.add_child(proxy)
	proxy.transform = body.transform
	proxy.skin = body.skin
	proxy.skeleton = NodePath("..")
	out["morphs"] = {"grip_R": body.get_blend_shape_value(1) if body.get_blend_shape_count() > 1 else -1.0}

func _fist_fit(p0: Vector3, d: Vector3) -> Array:
	var ds := []
	for p in fingers_closed:
		ds.append(maxf(_line_dist(p, p0, d) - haft_r, 0.0) * s_)
	ds.sort()
	return [snappedf(float(ds[ds.size() / 2]), 0.0001), snappedf(float(ds[int(ds.size() * 0.9)]), 0.0001)]

func _roll_terms(clip: String, T_dir: Vector3, E1: Vector3, N1: Vector3, d_head: float) -> Dictionary:
	var a := ap.get_animation(clip)
	var fps := 48.0
	var n: int = maxi(int(round(a.length * fps)), 2)
	ap.play(clip)
	var rows := []
	for i in n + 1:
		var t: float = a.length * float(i) / float(n)
		ap.seek(t, true, true)
		var g: Transform3D = skel.get_bone_global_pose(hb)
		var gb: Basis = g.basis.orthonormalized()
		var hipo: Vector3 = skel.get_bone_global_pose(skel.find_bone("Hips")).origin
		rows.append({"t": t, "head_a": g * (P + T_dir * d_head), "head_b": g * head_l, "reach": ((g * (P + T_dir * d_head)) - hipo).dot(F),
					 "h_a": (gb * T_dir).normalized(), "h_b": (gb * H).normalized(),
					 "e1": (gb * E1).normalized(), "n1": (gb * N1).normalized(), "e_b": (gb * E).normalized()})
	# speeds, peak, window (contiguous with the peak, >= 50% of it)
	var sp := [0.0]
	for i in range(1, rows.size()):
		sp.append(((rows[i]["head_a"] as Vector3) - (rows[i - 1]["head_a"] as Vector3)).length() * s_ * fps)
	var pk := 0
	for i in sp.size():
		if float(sp[i]) > float(sp[pk]): pk = i
	var i0 := pk
	while i0 > 1 and float(sp[i0 - 1]) >= 0.5 * float(sp[pk]): i0 -= 1
	var i1 := pk
	while i1 < sp.size() - 1 and float(sp[i1 + 1]) >= 0.5 * float(sp[pk]): i1 += 1
	var A := 0.0; var B := 0.0; var W := 0.0; var bef := 0.0; var Wb := 0.0
	for i in range(i0, i1 + 1):
		var v: Vector3 = (rows[i]["head_a"] as Vector3) - (rows[i - 1]["head_a"] as Vector3)
		var h: Vector3 = rows[i]["h_a"]
		var u: Vector3 = v - v.dot(h) * h
		var w: float = u.length()
		if w < 1e-9: continue
		u = u / w
		A += w * (rows[i]["e1"] as Vector3).dot(u)
		B += w * (rows[i]["n1"] as Vector3).dot(u)
		W += w
		var vb: Vector3 = (rows[i]["head_b"] as Vector3) - (rows[i - 1]["head_b"] as Vector3)
		var hbv: Vector3 = rows[i]["h_b"]
		var ub: Vector3 = vb - vb.dot(hbv) * hbv
		if ub.length() > 1e-9:
			bef += ub.length() * (rows[i]["e_b"] as Vector3).dot(ub.normalized())
			Wb += ub.length()
	var e1s := []; var n1s := []
	for i in range(i0, i1 + 1):
		e1s.append(rows[i]["e1"]); n1s.append(rows[i]["n1"])
	var eb: Vector3 = rows[pk]["e_b"]
	# 14_axe_assert's strike: the frame the head reaches FURTHEST FORWARD (a cut's strike)
	var fr := 0
	for i in rows.size():
		if float(rows[i]["reach"]) > float(rows[fr]["reach"]): fr = i
	var ebf: Vector3 = rows[fr]["e_b"]
	var f0: int = clampi(fr - 1, 0, rows.size() - 1); var f1: int = clampi(fr + 1, 0, rows.size() - 1)
	var vfw: Vector3 = (rows[f1]["head_a"] as Vector3) - (rows[f0]["head_a"] as Vector3)
	var hfw: Vector3 = rows[fr]["h_a"]
	var ufw: Vector3 = vfw - vfw.dot(hfw) * hfw
	ufw = ufw.normalized() if ufw.length() > 1e-9 else Vector3.ZERO
	return {"A": A / maxf(W, 1e-9), "B": B / maxf(W, 1e-9), "before": bef / maxf(Wb, 1e-9), "n": i1 - i0 + 1,
			"e1_pk": rows[pk]["e1"], "n1_pk": rows[pk]["n1"], "e1s": e1s, "n1s": n1s,
			"e1_fw": rows[fr]["e1"], "n1_fw": rows[fr]["n1"], "fw_t": float(rows[fr]["t"]), "u_fw": ufw,
			"travel_heading_fw": rad_to_deg(atan2(ufw.dot(R), ufw.dot(F))),
			"before_heading_fw": rad_to_deg(atan2(ebf.dot(R), ebf.dot(F))),
			"before_heading_pk": rad_to_deg(atan2(eb.dot(R), eb.dot(F))),
			"w0": float(rows[i0]["t"]), "w1": float(rows[i1]["t"]), "peak": float(sp[pk]), "peak_t": float(rows[pk]["t"])}

# ---------------------------------------------------------------------------------------
func _crossings(tm: TriangleMesh, p: Vector3, dir: Vector3) -> Array:
	var o := p
	var n := 0
	var first := -1
	for i in 32:
		var r = tm.intersect_ray(o, dir)
		if typeof(r) != TYPE_DICTIONARY or (r as Dictionary).is_empty(): break
		n += 1
		if first < 0: first = int(r["face_index"])
		o = (r["position"] as Vector3) + dir * 0.002
	return [n, first]

func _manual_skin(arr: Array, vi: int) -> Vector3:
	var v: Vector3 = (arr[Mesh.ARRAY_VERTEX] as PackedVector3Array)[vi]
	var bones = arr[Mesh.ARRAY_BONES]; var w = arr[Mesh.ARRAY_WEIGHTS]
	var nb: int = int(bones.size() / (arr[Mesh.ARRAY_VERTEX] as PackedVector3Array).size())
	var acc := Vector3.ZERO; var ws := 0.0
	for j in nb:
		var ww: float = float(w[vi * nb + j])
		if ww <= 0.0: continue
		var bi: int = int(bones[vi * nb + j])
		var b := skel.find_bone(String(body.skin.get_bind_name(bi)))
		acc += (skel.get_bone_global_pose(b) * body.skin.get_bind_pose(bi) * v) * ww; ws += ww
	return acc / ws

func _reversals(seq: Array) -> int:
	var n := 0
	var last := 0
	for i in range(1, seq.size()):
		var d: float = float(seq[i]) - float(seq[i - 1])
		if absf(d) < 1.0: continue
		var s := 1 if d > 0.0 else -1
		if last != 0 and s != last: n += 1
		last = s
	return n

func _score(G: Dictionary, dirs: Dictionary) -> void:
	var clips := ap.get_animation_list()
	if OS.has_environment("GRIP_CLIPS"):
		clips = PackedStringArray(OS.get_environment("GRIP_CLIPS").split(","))
	var table := {}
	var tot_frames := 0
	var t_start := Time.get_ticks_msec()
	# sanity: the TriangleMesh face index must be the bake's triangle order
	ap.play("attack"); ap.seek(0.7, true, true)
	skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)
	var bk: ArrayMesh = proxy.bake_mesh_from_current_skeleton_pose()
	# THE BAKE MUST SEE THE POSE: compare baked vertices with manual skinning from the bone poses
	var barr := body.mesh.surface_get_arrays(0)
	var bvv: PackedVector3Array = bk.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
	var worst := 0.0
	for vi in [1000, 40000, 80000, 120000, 150000]:
		worst = maxf(worst, (bvv[vi] - _manual_skin(barr, vi)).length())
	say("[grip] instrument check: baked body vs manual skinning at attack 0.70 s, worst of 5 vertices %.4f units (%.5f m)" % [worst, worst * s_])
	var tm0: TriangleMesh = bk.generate_triangle_mesh()
	var faces: PackedVector3Array = bk.get_faces()
	var chk := 0; var ok := 0
	for s in 40:
		var o := Vector3(randf_range(-20, 20), -50, randf_range(-15, 15))
		var r = tm0.intersect_ray(o, Vector3.UP)
		if typeof(r) == TYPE_DICTIONARY and not (r as Dictionary).is_empty():
			chk += 1
			var fi: int = int(r["face_index"])
			var a: Vector3 = faces[3 * fi]; var b: Vector3 = faces[3 * fi + 1]; var c: Vector3 = faces[3 * fi + 2]
			var pp: Vector3 = r["position"]
			var nrm := (b - a).cross(c - a).normalized()
			if absf((pp - a).dot(nrm)) < 0.01: ok += 1
	say("[grip] instrument check: %d of %d ray hits lie on the triangle their face_index names (face order = bake order)" % [ok, chk])
	# positive control: a point at the chest must read INSIDE, a point 2 m in front must read outside
	var chest: Vector3 = skel.get_bone_global_pose(skel.find_bone("Spine01")).origin
	var ci: Array = _crossings(tm0, chest, Vector3.UP)
	var co: Array = _crossings(tm0, chest + Vector3(0, 0, 200), Vector3.UP)
	say("[grip] positive control: chest joint crossings %d (%s), 2 m in front %d (%s)"
		% [int(ci[0]), "INSIDE" if int(ci[0]) % 2 == 1 else "outside", int(co[0]), "INSIDE" if int(co[0]) % 2 == 1 else "outside"])
	for clip in clips:
		var a := ap.get_animation(clip)
		var n: int = maxi(int(round(a.length * 24.0)), 1)
		ap.play(clip)
		var per := {}
		for key in G.keys():
			per[key] = {"tilt": [], "fwd": [], "out": [], "hd_out": [], "hd_fwd": [], "hd_up": [], "edge": [], "pen_max": 0,
						"pen_frames": 0, "pen_parts": {}, "marker": [], "hand": [], "tilt30": []}
		var wrist30 := []
		for i in n + 1:
			var t: float = a.length * float(i) / float(n)
			ap.seek(t, true, true)
			skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)
			var g: Transform3D = skel.get_bone_global_pose(hb)
			var gb: Basis = g.basis.orthonormalized()
			var baked: ArrayMesh = proxy.bake_mesh_from_current_skeleton_pose()
			var tm: TriangleMesh = baked.generate_triangle_mesh()
			var box: AABB = baked.get_aabb()
			tot_frames += 1
			for key in G.keys():
				var Gk: Transform3D = G[key]
				var hd: Vector3 = (gb * (dirs[key][0] as Vector3)).normalized()
				var ed: Vector3 = (gb * (dirs[key][1] as Vector3)).normalized()
				var headw: Vector3 = g * (Gk * head_l)
				var fist: Vector3 = g * (Gk * P)
				var dd: Vector3 = (headw - fist) * s_
				var pr: Dictionary = per[key]
				(pr["tilt"] as Array).append(rad_to_deg(hd.angle_to(U)))
				(pr["fwd"] as Array).append(hd.dot(F)); (pr["out"] as Array).append(hd.dot(R))
				(pr["hd_out"] as Array).append(dd.dot(R)); (pr["hd_fwd"] as Array).append(dd.dot(F)); (pr["hd_up"] as Array).append(dd.dot(U))
				(pr["edge"] as Array).append(rad_to_deg(atan2(ed.dot(R), ed.dot(F))))
				(pr["marker"] as Array).append(g * (Gk * edge_l))
				(pr["hand"] as Array).append(g.origin)
				# penetration
				var inside := 0
				for pl in pts_l:
					var p: Vector3 = g * (Gk * pl)
					if p.x < box.position.x or p.x > box.end.x or p.z < box.position.z or p.z > box.end.z or p.y > box.end.y:
						continue
					var up: Array = _crossings(tm, p, Vector3.UP)
					if int(up[0]) % 2 == 0: continue
					var dn: Array = _crossings(tm, p, Vector3.DOWN)
					var fu: int = int(up[1]); var fd: int = int(dn[1])
					if fu >= 0 and fd >= 0 and tri_hand[fu] == 1 and tri_hand[fd] == 1:
						continue
					inside += 1
					var part: String = String(body.skin.get_bind_name(tri_bone[fu])) if fu >= 0 else "?"
					pr["pen_parts"][part] = int(pr["pen_parts"].get(part, 0)) + 1
				if inside > int(pr["pen_max"]): pr["pen_max"] = inside
				if inside > 0: pr["pen_frames"] = int(pr["pen_frames"]) + 1
		# wrist reversals at 30 fps (27_armed_carry's survey), and haft-tilt reversals
		var n30: int = maxi(int(round(a.length * 30.0)), 1)
		var q0 := Quaternion.IDENTITY
		var tilts := {}
		for key in G.keys(): tilts[key] = []
		for i in n30 + 1:
			ap.seek(a.length * float(i) / float(n30), true, true)
			var q: Quaternion = (skel.get_bone_global_pose(fb).basis.orthonormalized().inverse() * skel.get_bone_global_pose(hb).basis.orthonormalized()).get_rotation_quaternion()
			if i == 0: q0 = q
			wrist30.append(rad_to_deg(q0.angle_to(q)))
			var gb2: Basis = skel.get_bone_global_pose(hb).basis.orthonormalized()
			for key in G.keys():
				(tilts[key] as Array).append(rad_to_deg((gb2 * (dirs[key][0] as Vector3)).normalized().angle_to(U)))
		var row := {"len_s": a.length, "frames": n + 1, "wrist_rev": _reversals(wrist30)}
		for key in G.keys():
			var pr: Dictionary = per[key]
			var md := func(k2: String) -> float:
				var v: Array = (pr[k2] as Array).duplicate(); v.sort(); return float(v[v.size() / 2])
			var mdir := Vector3.ZERO
			for i in (pr["tilt"] as Array).size():
				mdir += Vector3(float(pr["out"][i]), 0, float(pr["fwd"][i]))
			# the ledger's edge-leading instrument
			var lead := [0, 0, -1.0]
			var mk: Array = pr["marker"]; var hd2: Array = pr["hand"]
			var mx := 0.0
			for i in range(1, mk.size()): mx = maxf(mx, ((mk[i] as Vector3) - (mk[i - 1] as Vector3)).length())
			for i in range(1, mk.size()):
				var v: Vector3 = (mk[i] as Vector3) - (mk[i - 1] as Vector3)
				if v.length() < mx * 0.2: continue
				lead[1] = int(lead[1]) + 1
				var arm: Vector3 = (mk[i] as Vector3) - (hd2[i] as Vector3)
				if arm.length() < 1e-6 or v.length() < 1e-9: continue
				var l: float = arm.normalized().dot(v.normalized())
				if l > 0.0: lead[0] = int(lead[0]) + 1
				lead[2] = maxf(float(lead[2]), l)
			var tl: Array = (pr["tilt"] as Array).duplicate(); tl.sort()
			row[key] = {"tilt_med": md.call("tilt"), "tilt_lo": float(tl[0]), "tilt_hi": float(tl[-1]),
						"fwd_med": md.call("fwd"), "out_med": md.call("out"),
						"head_out": md.call("hd_out"), "head_fwd": md.call("hd_fwd"), "head_up": md.call("hd_up"),
						"edge_med": md.call("edge"), "pen_max": int(pr["pen_max"]), "pen_frames": int(pr["pen_frames"]),
						"pen_parts": pr["pen_parts"], "lead_count": int(lead[0]), "lead_frames": int(lead[1]), "lead_best": float(lead[2]),
						"tilt_rev": _reversals(tilts[key])}
		table[clip] = row
		var b: Dictionary = row["before"]; var af: Dictionary = row["after"]
		say("[score] %-28s tilt %5.1f->%5.1f  fwd %+.2f->%+.2f out %+.2f->%+.2f  head out %+.2f->%+.2f fwd %+.2f->%+.2f up %+.2f->%+.2f  edge %+4.0f->%+4.0f  pen %d/%df->%d/%df  lead %d/%d %.3f->%d/%d %.3f  wrist rev %d  tilt rev %d->%d"
			% [clip, float(b["tilt_med"]), float(af["tilt_med"]), float(b["fwd_med"]), float(af["fwd_med"]), float(b["out_med"]), float(af["out_med"]),
			   float(b["head_out"]), float(af["head_out"]), float(b["head_fwd"]), float(af["head_fwd"]), float(b["head_up"]), float(af["head_up"]),
			   float(b["edge_med"]), float(af["edge_med"]), int(b["pen_max"]), int(b["pen_frames"]), int(af["pen_max"]), int(af["pen_frames"]),
			   int(b["lead_count"]), int(b["lead_frames"]), float(b["lead_best"]), int(af["lead_count"]), int(af["lead_frames"]), float(af["lead_best"]),
			   int(row["wrist_rev"]), int(b["tilt_rev"]), int(af["tilt_rev"])])
		if int(b["pen_max"]) > 0 or int(af["pen_max"]) > 0:
			say("[score]     penetration by part: before %s | after %s" % [str(b["pen_parts"]), str(af["pen_parts"])])
	out["score"] = table
	say("[grip] scored %d frames in %.1f s" % [tot_frames, (Time.get_ticks_msec() - t_start) / 1000.0])
