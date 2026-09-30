extends SceneTree
# T12 (c) ACCEPTANCE -- the weapon gate's table, measured on what the scene shows. It writes the
# table nb_d2/scripts/53_weapon_gate.py reads.
#   HOLD STATES, through the TREE: idle, walk, run, block and both strafes, driven as the game
#   drives him (drive_dir / set_block), two loops of each (the block: 2 s held)
#   STRIKES, raw: the slash and the chop own every bone while they run, so the clip IS the strike
# The axe is carried by whatever bone its vertices are weighted to (weapon_r after T12, RightHand
# before). Per row:
#   pass_frac  the guard predicate: tilt 30-60 deg from vertical, haft forward and outboard, head
#              outboard of the fist, |edge heading| <= 45 deg -- the fraction of frames
#   fist turn  weapon_r's haft against its rest, in the hand's frame: the haft leaving the fist's
#              channel (median / p90; 0 by construction when the axe is rigid in the hand)
#   arc        the axe head's screen path per loop, per play-camera cell (8 cells, 77.8 px/m)
#   pen        axe vertices INSIDE the posed body (every 4th vertex; odd crossing parity along all
#              SIX axis directions against the CPU-skinned body with its morphs), the FIST excluded
#              geometrically (the stretch of haft the closed hand wraps, from the hand mesh): the
#              worst frame's count, its depth (the nearest surface), and how many frames have any
#   edge       strikes: the EDGE ALONG THE TRAVEL (the edge direction against the head's travel
#              with the along-haft part removed) at the STRIKE FRAME -- the furthest forward of
#              the hips INSIDE THE ACTIVE SWING (the frames contiguous with the head's peak speed
#              at >= 50% of it) -- and speed-weighted over the swing. The edge's heading against
#              his forward is reported for information (gate change, coordinator 2026-09-30: the
#              slash is a lateral sweep). The old whole-clip strike frame is reported beside it.
# env: KNIGHT (res:// script), ACCEPT_LABEL, ACCEPT_OUT (json), ACCEPT_EDGE (the edge marker; default axe_edge)
const DT := 1.0 / 24.0
# the STRIKE step (T12_11): ACCEPT_STRIKE_FPS=<n> fires the strikes at 1/n s -- a lab sweep of PEN at the
# game's own tick (60 Hz) or finer; unset, the gate's 1/24 s, as every table before it
var SDT := DT
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
var ap: AnimationPlayer
var body: MeshInstance3D
var s_ := 1.0
var ab := -1               # the bone the axe's vertices are weighted to
var bind := Transform3D()
var W_rest := Transform3D()
var H := Vector3.UP
var E := Vector3.BACK
var head_l := Vector3.ZERO
var grip_l := Vector3.ZERO
var pts := PackedVector3Array()
var proxy: MeshInstance3D
var tri_hand := PackedByteArray()
var tri_bone := PackedInt32Array()
var label := ""
var wd_ms := 0

func _initialize() -> void:
	wd_ms = Time.get_ticks_msec() + 3000000
	label = OS.get_environment("ACCEPT_LABEL") if OS.has_environment("ACCEPT_LABEL") else "?"
	if OS.has_environment("ACCEPT_STRIKE_FPS"):
		SDT = 1.0 / float(OS.get_environment("ACCEPT_STRIKE_FPS"))
		print("[accept] LAB: strikes stepped at 1/%s s" % OS.get_environment("ACCEPT_STRIKE_FPS"))
	var kp: String = OS.get_environment("KNIGHT") if OS.has_environment("KNIGHT") else "res://scripts/knight.gd"
	var ground := StaticBody3D.new()
	ground.collision_layer = CliffWorld.TERRAIN_BIT
	var cs := CollisionShape3D.new(); var box := BoxShape3D.new(); box.size = Vector3(4000, 1, 4000)
	cs.shape = box; cs.position = Vector3(0, -0.5, 0); ground.add_child(cs); root.add_child(ground)
	k = load(kp).new()
	k.setup(RIGHT, UP, FWD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	for i in 4: await process_frame
	skel = k._skel; tree = k._tree; ap = k._anim; body = k._mesh
	if OS.has_environment("ACCEPT_WEIGHT") and k.cfg.has("arm_layer_armed_R"):
		# LAB ONLY: the guard layer's weight overridden (the knight reads the spec every frame)
		(k.cfg["arm_layer_armed_R"] as Dictionary)["weight"] = float(OS.get_environment("ACCEPT_WEIGHT"))
		print("[accept] LAB: arm_layer_armed_R weight = %s" % OS.get_environment("ACCEPT_WEIGHT"))
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var mods := 0
	for c in skel.get_children():
		if c is SkeletonModifier3D and (c as SkeletonModifier3D).active: mods += 1
	s_ = skel.global_transform.basis.get_scale().x
	_axe()
	_body()
	_fist()
	# the proxy's skin registers with the skeleton on a later frame; a bake before that returns null
	for i in 4: await process_frame
	for i in 24: _step(Vector2.ZERO, false)
	_instrument()
	print("[accept] %s knight=%s model=%s axe on %s; active skeleton modifiers %d (the pose read is the animated one)"
		% [label, kp.get_file(), String(k.cfg.get("model", "")), skel.get_bone_name(ab), mods])
	var out := {"label": label, "knight": kp, "model": String(k.cfg.get("model", "")), "axe_bone": skel.get_bone_name(ab),
				"source": "tree", "bones": skel.get_bone_count(), "clips": {}}
	var states: PackedStringArray = (OS.get_environment("ACCEPT_STATES") if OS.has_environment("ACCEPT_STATES") else "idle,walk,run,block,strafe_l,strafe_r").split(",", false)
	var strikes: PackedStringArray = (OS.get_environment("ACCEPT_STRIKES") if OS.has_environment("ACCEPT_STRIKES") else "slash,chop,bash").split(",", false)
	for st in states:
		if Time.get_ticks_msec() > wd_ms: print("[accept] WATCHDOG"); quit(4); return
		var r := _hold(st)
		out["clips"][st] = r
		print("[accept] %-8s %-9s hand contact (pommel in its own hand, <= 2 cm) %d pts max %.3f m on %d frames | the wrist off its rest (neutral) %.1f / %.1f / %.1f deg (median / p90 / max)" % [label, st, int(r["hand_contact_max"]), float(r["hand_contact_depth_m"]), int(r["hand_contact_frames"]), float(r["wrist_med"]), float(r["wrist_p90"]), float(r["wrist_max"])])
		print("[accept] %-8s %-9s guard %3d%% | fist turn %4.1f/%4.1f deg | arc %3.0f-%3.0f px/loop | pen worst %d (%.3f m deep), frames %d of %d %s | tilt %4.1f fwd %+.2f out %+.2f head out %+.2f edge %+4.0f (medians) | %s %.3f s x%d"
			% [label, st, int(round(100.0 * float(r["pass_frac"]))), float(r["turn_med"]), float(r["turn_p90"]), float(r["arc_min"]), float(r["arc_max"]),
			   int(r["pen_max"]), float(r["pen_depth_m"]), int(r["pen_frames"]), int(r["frames"]), JSON.stringify(r["pen_parts"]), float(r["tilt"]), float(r["fwd"]), float(r["out"]),
			   float(r["head_out"]), float(r["edge"]), String(r["clip"]), float(r["loop_s"]), int(r["loops"])])
	# STRIKES, through the TREE (what the scene shows: the one-shot, its fades, the recovery
	# release) unless ACCEPT_STRIKE_MODE=raw; either way the clip is also sampled RAW, and the tree's
	# active swing is compared with it frame for frame (the release must leave the swing unchanged).
	# ACCEPT_CHOP=<clip> re-points the chop (lab: a candidate), ACCEPT_REL=<clip>:<s>,... sets its
	# release (strike_release.at_s).
	var smode: String = OS.get_environment("ACCEPT_STRIKE_MODE") if OS.has_environment("ACCEPT_STRIKE_MODE") else "tree"
	var bt := tree.tree_root as AnimationNodeBlendTree
	if OS.has_environment("ACCEPT_CHOP") and bt.has_node("a_chop"):
		var cand := OS.get_environment("ACCEPT_CHOP")
		(bt.get_node("a_chop") as AnimationNodeAnimation).animation = cand
		k._roles["chop"] = cand
		print("[accept] LAB: the chop re-pointed at '%s' (%.3f s)" % [cand, float(k._clip_len.get(cand, -1.0))])
	if OS.has_environment("ACCEPT_REL") and k.cfg.has("strike_release"):
		for kv in OS.get_environment("ACCEPT_REL").split(",", false):
			((k.cfg["strike_release"] as Dictionary)["at_s"] as Dictionary)[kv.split(":")[0]] = float(kv.split(":")[1])
		print("[accept] LAB: release at %s" % JSON.stringify(k.cfg["strike_release"]["at_s"]))
	if k.has_method("_apply_strike_release"):
		k._apply_strike_release()
	var srows := {}
	var skey := {}
	for key in strikes:
		if Time.get_ticks_msec() > wd_ms: print("[accept] WATCHDOG"); quit(4); return
		if not bt.has_node("a_" + key): continue
		var clip := String((bt.get_node("a_" + key) as AnimationNodeAnimation).animation)
		skey[clip] = key
		if smode == "tree":
			srows[clip] = _strike_tree(key, clip)
	tree.active = false
	# the tree lets go of the skeleton on its own frame: switching the player on under it at once
	# crashed Godot (signal 11 in AnimationPlayer.play, after two tree strikes, 2026-09-30)
	for i in 3: await process_frame
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	for i in 2: await process_frame
	for clip in skey:
		if Time.get_ticks_msec() > wd_ms: print("[accept] WATCHDOG"); quit(4); return
		var raw := _strike_raw(clip, smode == "raw")
		var rows: Array = srows[clip] if smode == "tree" else raw
		var e_raw: Dictionary = _strike_metrics(raw)["edge_lead"]
		var r2 := _strike_metrics(rows, e_raw["swing"])
		r2["strike_key"] = String(skey[clip])
		r2["mode"] = smode
		r2["length_s"] = ap.get_animation(clip).length
		# the swing, tree against raw: the axe head's largest separation over the swing's frames, the
		# raw clip sampled at the tree's own frame times
		var dev := 0.0; var n_dev := 0; var edev := 0.0
		var e0: Dictionary = e_raw
		for rr in rows:
			var tr: float = float(rr["t"])
			if tr < float(e0["swing"][0]) - 1e-3 or tr > float(e0["swing"][1]) + 1e-3: continue
			ap.play(clip); ap.seek(tr, true, true)
			var q := _frame()
			dev = maxf(dev, ((rr["head"] as Vector3) - (q["head"] as Vector3)).length())
			edev = maxf(edev, rad_to_deg((rr["e"] as Vector3).angle_to(q["e"] as Vector3)))
			n_dev += 1
		r2["swing_vs_raw"] = {"raw_edge": e0, "head_dev_m": dev, "edge_dev_deg": edev, "frames": n_dev}
		out["clips"][clip] = r2
		var e: Dictionary = r2["edge_lead"]
		print("[accept] %-8s %-5s %-14s [%s] EDGE along the travel at the strike (%.3f s) %+.2f, over the swing (%.3f-%.3f s) %+.2f | heading %+4.0f (info) | swing vs raw: head %.4f m, edge %.2f deg over %d frames (raw %+.2f/%+.2f, %.3f-%.3f s) | swing arc %3.0f-%3.0f px, peak step %.1f px | fist turn in the swing %4.1f/%4.1f | pen worst %d (%.3f m), frames %d of %d %s"
			% [label, String(skey[clip]), clip, smode, float(e["strike_t"]), float(e["on_travel_strike"]), float(e["swing"][0]), float(e["swing"][1]), float(e["swing_mean"]),
			   float(e["heading_strike"]), dev, edev, n_dev, float(e0["on_travel_strike"]), float(e0["swing_mean"]), float(e0["swing"][0]), float(e0["swing"][1]),
			   float(r2["swing_arc_min"]), float(r2["swing_arc_max"]), float(r2["step_max"]), float(r2["turn_med"]), float(r2["turn_max"]),
			   int(r2["pen_max"]), float(r2["pen_depth_m"]), int(r2["pen_frames"]), int(r2["frames"]), JSON.stringify(r2["pen_parts"])])
		if (r2["pen_t"] as Array).size() > 0:
			print("[accept] %-8s %-14s penetrating frames (t, points, depth m): %s" % [label, clip, JSON.stringify(r2["pen_t"])])
	var f := FileAccess.open(OS.get_environment("ACCEPT_OUT") if OS.has_environment("ACCEPT_OUT") else "/tmp/accept.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " ")); f.close()
	quit(0)

func _axe() -> void:
	var mi: MeshInstance3D = (k.gear["_pieces"]["axe"] as Array)[0]
	var arr := mi.mesh.surface_get_arrays(0)
	var verts: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
	var bones = arr[Mesh.ARRAY_BONES]; var weights = arr[Mesh.ARRAY_WEIGHTS]
	var nb: int = int(bones.size() / verts.size())
	var wsum := {}
	var tot := 0.0
	for vi in verts.size():
		for j in nb:
			var w: float = float(weights[vi * nb + j])
			if w <= 0.0: continue
			var bi: int = int(bones[vi * nb + j])
			wsum[bi] = float(wsum.get(bi, 0.0)) + w; tot += w
	var bb := -1
	for bi in wsum:
		if bb < 0 or float(wsum[bi]) > float(wsum[bb]): bb = int(bi)
	var bname := String(mi.skin.get_bind_name(bb))
	bind = mi.skin.get_bind_pose(bb)
	ab = skel.find_bone(bname)
	W_rest = skel.get_bone_rest(ab)
	print("[accept] the axe: %d vertices, %.4f of the skin weight on '%s'" % [verts.size(), float(wsum[bb]) / maxf(tot, 1e-9), bname])
	var c := Vector3.ZERO
	var all := []
	for v in verts:
		var p: Vector3 = bind * v; all.append(p); c += p
	c /= float(all.size())
	for i in range(0, all.size(), 4): pts.append(all[i])
	var xx := 0.0; var xy := 0.0; var xz := 0.0; var yy := 0.0; var yz := 0.0; var zz := 0.0
	for p in all:
		var d: Vector3 = p - c
		xx += d.x * d.x; xy += d.x * d.y; xz += d.x * d.z; yy += d.y * d.y; yz += d.y * d.z; zz += d.z * d.z
	var ax := Vector3(1, 1, 1).normalized()
	for it in 80:
		ax = Vector3(xx * ax.x + xy * ax.y + xz * ax.z, xy * ax.x + yy * ax.y + yz * ax.z, xz * ax.x + yz * ax.y + zz * ax.z).normalized()
	# ACCEPT_EDGE: the edge marker's name (default axe_edge; the JOIN sword in the axe slot carries sword_edge)
	var mk_name: String = OS.get_environment("ACCEPT_EDGE") if OS.has_environment("ACCEPT_EDGE") else "axe_edge"
	var mk: Node3D = (k.gear["_pieces"]["_markers_axe"] as Dictionary)[mk_name]
	print("[accept] edge marker '%s' at %s in its bone's frame" % [mk_name, str(mk.transform.origin)])
	var edge_l: Vector3 = mk.transform.origin
	var att := mk.get_parent() as BoneAttachment3D
	if att != null and skel.find_bone(att.bone_name) != ab:
		edge_l = skel.get_bone_global_rest(ab).affine_inverse() * (skel.get_bone_global_rest(skel.find_bone(att.bone_name)) * edge_l)
	if (edge_l - c).dot(ax) < 0.0: ax = -ax
	H = ax
	E = ((edge_l - c) - (edge_l - c).dot(H) * H).normalized()
	head_l = c + H * (edge_l - c).dot(H)
	grip_l = c + H * (-c).dot(H)
	# GRIP_SLIDE_M (lab only): the axe slid along its haft in the fist -- + moves the grip toward the
	# butt ("choke down"): the whole axe translates +d along the haft, relative to the hand
	if OS.has_environment("GRIP_SLIDE_M"):
		var dsl: float = float(OS.get_environment("GRIP_SLIDE_M")) / s_
		for i in all.size(): all[i] = (all[i] as Vector3) + H * dsl
		for i in pts.size(): pts[i] = pts[i] + H * dsl
		head_l += H * dsl
		print("[accept] LAB: the axe slid %.3f m along the haft (toward the head), the grip that much nearer the butt" % (dsl * s_))
	var smin := 1e9; var smax := -1e9
	for p in all:
		var sp: float = ((p as Vector3) - grip_l).dot(H); smin = minf(smin, sp); smax = maxf(smax, sp)
	print("[accept] the haft runs %.3f m below the grip and %.3f m above it" % [-smin * s_, smax * s_])
	if bname == "weapon_r":
		print("[accept] instrument: the axe's own axes against weapon_r's -- haft (PCA) to +Y %.2f deg, edge (marker) to +Z %.2f deg; the grip point %.4f m from the bone's origin"
			% [rad_to_deg(H.angle_to(Vector3.UP)), rad_to_deg(E.angle_to(Vector3.BACK)), grip_l.length() * s_])

func _body() -> void:
	var arr := body.mesh.surface_get_arrays(0)
	var verts: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
	var bones = arr[Mesh.ARRAY_BONES]; var weights = arr[Mesh.ARRAY_WEIGHTS]
	var nb: int = int(bones.size() / verts.size())
	var rh := -1
	for i in body.skin.get_bind_count():
		if String(body.skin.get_bind_name(i)) == "RightHand": rh = i
	var wrh := PackedFloat32Array(); wrh.resize(verts.size())
	var dom := PackedInt32Array(); dom.resize(verts.size())
	for vi in verts.size():
		var w := 0.0; var bw := 0.0; var bbi := -1
		for j in nb:
			var ww: float = float(weights[vi * nb + j]); var bi: int = int(bones[vi * nb + j])
			if bi == rh: w += ww
			if ww > bw: bw = ww; bbi = bi
		wrh[vi] = w; dom[vi] = bbi
	var ix: PackedInt32Array = arr[Mesh.ARRAY_INDEX]
	tri_hand.resize(ix.size() / 3); tri_bone.resize(ix.size() / 3)
	for t in ix.size() / 3:
		tri_hand[t] = 1 if (wrh[ix[3 * t]] + wrh[ix[3 * t + 1]] + wrh[ix[3 * t + 2]]) / 3.0 > 0.5 else 0
		tri_bone[t] = dom[ix[3 * t]]
	var mix: ArrayMesh = body.bake_mesh_from_current_blend_shape_mix()
	var marr := mix.surface_get_arrays(0)
	var parr := arr.duplicate()
	parr[Mesh.ARRAY_VERTEX] = marr[Mesh.ARRAY_VERTEX]
	if marr[Mesh.ARRAY_NORMAL] != null: parr[Mesh.ARRAY_NORMAL] = marr[Mesh.ARRAY_NORMAL]
	var am := ArrayMesh.new()
	am.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, parr, [], {}, Mesh.ARRAY_FLAG_USE_8_BONE_WEIGHTS if nb == 8 else 0)
	proxy = MeshInstance3D.new(); proxy.mesh = am; proxy.visible = false
	proxy.skin = body.skin; proxy.skeleton = NodePath("..")
	skel.add_child(proxy); proxy.transform = body.transform

func _instrument() -> void:
	# the bake must see the pose, the face index must be the bake's order, and parity must work
	skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)
	var bk: ArrayMesh = proxy.bake_mesh_from_current_skeleton_pose()
	var barr := proxy.mesh.surface_get_arrays(0)   # the proxy's own vertices: the morphs are in them
	var bvv: PackedVector3Array = bk.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
	var worst := 0.0
	for vi in [1000, bvv.size() / 4, bvv.size() / 2, (3 * bvv.size()) / 4, bvv.size() - 7]:
		worst = maxf(worst, (bvv[vi] - _manual_skin(barr, vi)).length())
	var tm0: TriangleMesh = bk.generate_triangle_mesh()
	var faces: PackedVector3Array = bk.get_faces()
	var chk := 0; var ok := 0
	var bx: AABB = bk.get_aabb()
	for s in 40:
		var o := Vector3(randf_range(bx.position.x, bx.end.x), bx.position.y - 1.0, randf_range(bx.position.z, bx.end.z))
		var r = tm0.intersect_ray(o, Vector3.UP)
		if typeof(r) == TYPE_DICTIONARY and not (r as Dictionary).is_empty():
			chk += 1
			var fi: int = int(r["face_index"])
			var a: Vector3 = faces[3 * fi]; var b: Vector3 = faces[3 * fi + 1]; var c: Vector3 = faces[3 * fi + 2]
			if absf(((r["position"] as Vector3) - a).dot((b - a).cross(c - a).normalized())) < 0.01: ok += 1
	var chest: Vector3 = skel.get_bone_global_pose(skel.find_bone("Spine01")).origin
	var ci: Array = _cross(tm0, chest, Vector3.UP)
	var co: Array = _cross(tm0, chest + F * (2.0 / s_), Vector3.UP)
	print("[accept] instrument: bake vs manual skinning worst %.5f m; %d of %d ray hits on the triangle their face_index names; chest joint %s, 2 m in front %s"
		% [worst * s_, ok, chk, "INSIDE" if int(ci[0]) % 2 == 1 else "outside(!)", "INSIDE(!)" if int(co[0]) % 2 == 1 else "outside"])

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

func _cross(tm: TriangleMesh, p: Vector3, d: Vector3) -> Array:
	var o := p; var n := 0; var first := -1; var dist := -1.0
	for i in 32:
		var r = tm.intersect_ray(o, d)
		if typeof(r) != TYPE_DICTIONARY or (r as Dictionary).is_empty(): break
		n += 1
		if first < 0:
			first = int(r["face_index"]); dist = ((r["position"] as Vector3) - p).length()
		o = (r["position"] as Vector3) + d * 0.002
	return [n, first, dist]

var pen_depth := 0.0   # the last _pen call's deepest inside point (m): the nearest surface over the rays
# HAND CONTACT (coordinator ruling 2026-09-30, the pommel ruling): a butt/pommel point inside the HOLDING hand -- the
# nearest surface over the six rays a hand-dominant triangle -- no deeper than HAND_CONTACT_M is grip contact, not
# penetration. Counted apart (hand_n / hand_depth per _pen call); into the body (hips, thigh) it is still penetration.
const HAND_CONTACT_M := 0.02
var hand_n := 0
var hand_depth := 0.0
var fist_s := [0.0, 0.0]   # the closed fist's extent ALONG THE HAFT (axe-bone units), from the hand mesh
var fist_r := 0.0          # the haft's radius at the grip, plus a margin (axe-bone units)
const DIRS := [Vector3.UP, Vector3.DOWN, Vector3.LEFT, Vector3.RIGHT, Vector3.FORWARD, Vector3.BACK]

func _fist() -> void:
	"""THE FIST, geometrically: the stretch of haft the closed hand wraps. The hand's own vertices
	(RightHand weight > 0.5, the grip morph in) are put in the axe bone's rest frame; their extent
	along the haft, within 6 cm of its axis, is the fist, +1 cm each side. An axe point inside that
	stretch and within the haft's radius (+1 cm) is in the hand by construction."""
	var arr := proxy.mesh.surface_get_arrays(0)
	var verts: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
	var bones = arr[Mesh.ARRAY_BONES]; var weights = arr[Mesh.ARRAY_WEIGHTS]
	var nb: int = int(bones.size() / verts.size())
	var rh := -1
	for i in body.skin.get_bind_count():
		if String(body.skin.get_bind_name(i)) == "RightHand": rh = i
	var to_axe: Transform3D = body.skin.get_bind_pose(rh)
	if skel.get_bone_name(ab) != "RightHand":
		to_axe = skel.get_bone_rest(ab).affine_inverse() * to_axe
	var lo := 1e9; var hi := -1e9
	for vi in verts.size():
		var w := 0.0
		for j in nb:
			if int(bones[vi * nb + j]) == rh: w += float(weights[vi * nb + j])
		if w <= 0.5: continue
		var q: Vector3 = to_axe * verts[vi]
		var sa: float = (q - grip_l).dot(H)
		if ((q - grip_l) - sa * H).length() * s_ > 0.06: continue
		lo = minf(lo, sa); hi = maxf(hi, sa)
	var rs := []
	for pl in pts:
		var sa2: float = (pl - grip_l).dot(H)
		if absf(sa2) * s_ < 0.03: rs.append(((pl - grip_l) - sa2 * H).length())
	rs.sort()
	var r_haft: float = float(rs[int(rs.size() * 0.9)]) if rs.size() > 4 else 0.02 / s_
	fist_s = [lo - 0.01 / s_, hi + 0.01 / s_]
	fist_r = r_haft + 0.01 / s_
	print("[accept] the fist: %.3f..%+.3f m along the haft from the grip (the hand mesh, +1 cm), haft radius %.4f m (+1 cm)"
		% [float(fist_s[0]) * s_, float(fist_s[1]) * s_, r_haft * s_])

func _pen(parts: Dictionary) -> int:
	# INSIDE = an odd number of crossings along ALL SIX axis directions. Two opposite rays (the
	# first instrument) were fooled by the body mesh itself -- overlapping layers and open seams
	# at the wrist and the raised arm read as inside -- at up to 8.7 cm "deep" in points six rays
	# put outside (attack_lab probe, 2026-09-30); a closed body answers odd in every direction.
	# The fist is excluded geometrically (_fist), and so is any point the right hand encloses on all
	# six sides (its first hit every way a RightHand-dominant triangle). Parts: the axe zone and
	# the first bone hit above.
	skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)
	var baked: ArrayMesh = proxy.bake_mesh_from_current_skeleton_pose()
	var tm: TriangleMesh = baked.generate_triangle_mesh()
	var bx: AABB = baked.get_aabb()
	var g: Transform3D = skel.get_bone_global_pose(ab)
	var inside := 0
	pen_depth = 0.0
	hand_n = 0; hand_depth = 0.0
	for pl in pts:
		var sa: float = (pl - grip_l).dot(H)
		var ra: float = ((pl - grip_l) - sa * H).length()
		if sa >= float(fist_s[0]) and sa <= float(fist_s[1]) and ra <= fist_r: continue
		var p: Vector3 = g * pl
		if not bx.has_point(p): continue
		var odd := true; var near := 1e9; var fu := -1; var in_hand := true; var fn := -1
		for d in DIRS:
			var c: Array = _cross(tm, p, d)
			if int(c[0]) % 2 == 0:
				odd = false; break
			if float(c[2]) < near: fn = int(c[1])
			near = minf(near, float(c[2]))
			if d == Vector3.UP: fu = int(c[1])
			if int(c[1]) < 0 or tri_hand[int(c[1])] == 0: in_hand = false
		if not odd: continue
		# ...and a point the RIGHT HAND encloses on all six sides is in the hand whatever the fist
		# stretch says (the butt's knob against the heel of the palm)
		if in_hand: continue
		var zone: String = "butt" if sa < 0.0 else ("head" if ra * s_ > 0.03 else "haft")
		# the pommel against the heel of ITS OWN hand, within 2 cm: grip contact (the named class), not penetration
		if zone == "butt" and fn >= 0 and tri_hand[fn] == 1 and near * s_ <= HAND_CONTACT_M:
			hand_n += 1; hand_depth = maxf(hand_depth, near * s_)
			continue
		inside += 1
		pen_depth = maxf(pen_depth, near * s_)
		var part: String = "%s:%s" % [zone, String(body.skin.get_bind_name(tri_bone[fu])) if fu >= 0 else "?"]
		parts[part] = int(parts.get(part, 0)) + 1
	return inside

func _frame() -> Dictionary:
	var g: Transform3D = skel.get_bone_global_pose(ab)
	var gb: Basis = g.basis.orthonormalized()
	var h: Vector3 = (gb * H).normalized(); var e: Vector3 = (gb * E).normalized()
	var head: Vector3 = (g * head_l) * s_
	var d: Vector3 = head - (g * grip_l) * s_
	var turn := 0.0
	if skel.get_bone_name(ab) == "weapon_r":
		var loc: Basis = skel.get_bone_pose(ab).basis.orthonormalized()
		turn = rad_to_deg((loc * Vector3.UP).normalized().angle_to((W_rest.basis.orthonormalized() * Vector3.UP).normalized()))
	# THE WRIST: the holding hand's local rotation off its rest (the guard's neutral wrist is the rest)
	var hb := skel.get_bone_parent(ab)
	var wrist := rad_to_deg(skel.get_bone_pose_rotation(hb).angle_to(skel.get_bone_rest(hb).basis.get_rotation_quaternion()))
	return {"tilt": rad_to_deg(h.angle_to(U)), "fwd": h.dot(F), "out": h.dot(R), "head_out": d.dot(R),
			"edge": rad_to_deg(atan2(e.dot(R), e.dot(F))), "turn": turn, "head": head, "h": h, "e": e, "wrist": wrist}

func _guard(m: Dictionary) -> bool:
	return float(m["tilt"]) >= 30.0 and float(m["tilt"]) <= 60.0 and float(m["fwd"]) > 0.0 and float(m["out"]) > 0.0 \
		and float(m["head_out"]) > 0.0 and absf(float(m["edge"])) <= 45.0

func _step(dir: Vector2, run: bool) -> void:
	k.drive_dir(dir, run, DT)
	tree.advance(DT)

func _strafe_input(side: String) -> Vector2:
	# the canvas direction along his strafe direction NOW, found without stepping him
	var sd: Vector3 = k._strafe_dir(side)
	var want: Vector3 = (Basis(Vector3.UP, float(k.get("_yaw_cur"))) * sd).normalized()
	var best := -2.0; var pick := Vector2.ZERO
	for a in 720:
		var dd := Vector2(cos(deg_to_rad(0.5 * a)), sin(deg_to_rad(0.5 * a)))
		var w3: Vector3 = k.canvas_velocity_to_world(dd); w3.y = 0.0
		if w3.length() < 1e-6: continue
		var c: float = w3.normalized().dot(want)
		if c > best: best = c; pick = dd
	return pick

func _clip_len(role: String, fallback: float) -> Array:
	var cn := String(k._roles.get(role, ""))
	return [cn, float(k._clip_len.get(cn, fallback))]

func _cam_axes(kk: int) -> Array:
	var y := deg_to_rad(47.0 + 45.0 * float(kk)); var th := deg_to_rad(PITCH_DEG)
	var fh := Vector3(sin(y), 0, cos(y))
	var dv := (fh * cos(th) + Vector3(0, -1, 0) * sin(th)).normalized()
	var rr := fh.cross(Vector3.UP).normalized()
	return [rr, rr.cross(dv).normalized()]

func _hold(st: String) -> Dictionary:
	k.set_block(false)
	for i in 48: _step(Vector2.ZERO, false)
	k.global_position = Vector3(0, 0.03, 0); k.velocity = Vector3.ZERO
	var dir := Vector2.ZERO; var run := false; var loops := 2
	var cl: Array = ["", 4.0]
	match st:
		"idle":
			cl = _clip_len("idle", 4.0)
		"walk", "run":
			run = st == "run"; dir = Vector2(0, 1)
			for i in 48: _step(dir, run)
			cl = [String(k._roles.get(st, "")), float(k.get("_cycle_len"))]
		"block":
			k.set_block(true); for i in 36: _step(Vector2.ZERO, false)
			cl = _clip_len("block", 2.0); cl[1] = 2.0; loops = 1
		"strafe_l", "strafe_r":
			k.set_block(true); for i in 24: _step(Vector2.ZERO, false)
			dir = _strafe_input("l" if st == "strafe_l" else "r")
			for i in 36: _step(dir, false)
			cl = _clip_len(st, 2.4583)
	var n: int = int(round(float(cl[1]) * float(loops) / DT))
	var ok := 0; var turns := []; var heads := []; var pmax := 0; var pfr := 0; var parts := {}; var dmax := 0.0
	var hmax := 0; var hfr := 0; var hdep := 0.0
	var cols := {"tilt": [], "fwd": [], "out": [], "head_out": [], "edge": []}
	var wrists := []
	for i in n:
		_step(dir, run)
		var m := _frame()
		if _guard(m): ok += 1
		turns.append(float(m["turn"])); heads.append(m["head"]); wrists.append(float(m["wrist"]))
		for key in cols: (cols[key] as Array).append(float(m[key]))
		var p := _pen(parts)
		pmax = maxi(pmax, p); dmax = maxf(dmax, pen_depth)
		if p > 0: pfr += 1
		hmax = maxi(hmax, hand_n); hdep = maxf(hdep, hand_depth)
		if hand_n > 0: hfr += 1
	k.set_block(false)
	turns.sort(); wrists.sort()
	var out := {"clip": String(cl[0]), "loop_s": float(cl[1]), "loops": loops, "frames": n, "pass_frac": float(ok) / float(n),
				"turn_med": float(turns[turns.size() / 2]), "turn_p90": float(turns[int(turns.size() * 0.9)]),
				"pen_max": pmax, "pen_frames": pfr, "pen_parts": parts, "pen_depth_m": dmax,
				"hand_classed": true, "hand_contact_max": hmax, "hand_contact_frames": hfr, "hand_contact_depth_m": hdep,
				"wrist_med": float(wrists[wrists.size() / 2]), "wrist_p90": float(wrists[int(wrists.size() * 0.9)]), "wrist_max": float(wrists[-1])}
	for key in cols:
		var v: Array = cols[key]; v.sort(); out[key] = float(v[v.size() / 2])
	var arcs := []
	for kk in 8:
		var ax: Array = _cam_axes(kk)
		var tot := 0.0
		for i in range(1, heads.size()):
			var dd: Vector3 = (heads[i] as Vector3) - (heads[i - 1] as Vector3)
			tot += Vector2(dd.dot(ax[0]), dd.dot(ax[1])).length() * PX_PER_M
		arcs.append(tot / float(loops))
	arcs.sort()
	out["arc_min"] = float(arcs[0]); out["arc_max"] = float(arcs[-1])
	return out

func _row(t: float) -> Dictionary:
	var m := _frame()
	m["reach"] = ((m["head"] as Vector3) - skel.get_bone_global_pose(skel.find_bone("Hips")).origin * s_).dot(F)
	m["t"] = t
	var parts := {}
	m["pen"] = _pen(parts)
	m["pen_depth"] = pen_depth
	m["pen_parts"] = parts
	m["hand_n"] = hand_n; m["hand_depth"] = hand_depth
	return m

func _strike_tree(key: String, clip: String) -> Array:
	"""Fire the strike from a settled guard and record every frame until its one-shot ends; t is the
	clip's own position (parameters/a_<key>/current_position) at that frame."""
	k.set_block(false)
	for i in 48: _step(Vector2.ZERO, false)
	k.global_position = Vector3(0, 0.03, 0); k.velocity = Vector3.ZERO
	var rows := []
	if not k.try_strike(key):
		print("[accept] %s: try_strike refused" % key)
		return rows
	var has_rel := (tree.tree_root as AnimationNodeBlendTree).has_node("rel_" + key)
	for i in int(round(14.0 / SDT)):
		k.drive_dir(Vector2.ZERO, false, SDT)
		tree.advance(SDT)
		if not bool(tree.get("parameters/os_%s/active" % key)):
			break
		var m := _row(float(tree.get("parameters/a_%s/current_position" % key)))
		m["rel"] = float(tree.get("parameters/rel_%s/blend_amount" % key)) if has_rel else 0.0
		rows.append(m)
	for i in 6: _step(Vector2.ZERO, false)
	return rows

func _strike_raw(clip: String, with_pen: bool) -> Array:
	var a := ap.get_animation(clip)
	var n: int = int(round(a.length * 24.0))
	ap.play(clip)
	var rows := []
	for i in n + 1:
		var t: float = a.length * float(i) / float(n)
		ap.seek(t, true, true)
		if with_pen:
			rows.append(_row(t))
		else:
			var m := _frame()
			m["reach"] = ((m["head"] as Vector3) - skel.get_bone_global_pose(skel.find_bone("Hips")).origin * s_).dot(F)
			m["t"] = t; m["pen"] = 0; m["pen_depth"] = 0.0; m["pen_parts"] = {}; m["hand_n"] = 0; m["hand_depth"] = 0.0
			rows.append(m)
	return rows

func _strike_metrics(rows: Array, win := []) -> Dictionary:
	# the head's speed (central difference, as the residual solve took it) and the active swing --
	# the clip's own (detected on the RAW clip and passed in as `win`, [t0, t1]) when given: through
	# the tree the fade-in is a fast move of the head from the guard into the clip's first pose,
	# and it is not a swing
	var sp := []
	for i in rows.size():
		var i0: int = maxi(i - 1, 0); var i1: int = mini(i + 1, rows.size() - 1)
		sp.append(((rows[i1]["head"] as Vector3) - (rows[i0]["head"] as Vector3)).length() / maxf(float(rows[i1]["t"]) - float(rows[i0]["t"]), 1e-6))
	var pk := 0
	for i in sp.size():
		if float(sp[i]) > float(sp[pk]): pk = i
	var w0 := pk; var w1 := pk
	while w0 > 0 and float(sp[w0 - 1]) >= 0.5 * float(sp[pk]): w0 -= 1
	while w1 < sp.size() - 1 and float(sp[w1 + 1]) >= 0.5 * float(sp[pk]): w1 += 1
	if win.size() == 2:
		w0 = -1; w1 = -1
		for i in rows.size():
			var ti: float = float(rows[i]["t"])
			if ti >= float(win[0]) - 1e-3 and ti <= float(win[1]) + 1e-3:
				if w0 < 0: w0 = i
				w1 = i
		if w0 < 0:
			w0 = 0; w1 = 0
		pk = w0
		for i in range(w0, w1 + 1):
			if float(sp[i]) > float(sp[pk]): pk = i
	var cs := []
	for i in rows.size():
		var i0: int = maxi(i - 1, 0); var i1: int = mini(i + 1, rows.size() - 1)
		var v: Vector3 = (rows[i1]["head"] as Vector3) - (rows[i0]["head"] as Vector3)
		var h: Vector3 = rows[i]["h"]
		var u: Vector3 = v - v.dot(h) * h
		cs.append((rows[i]["e"] as Vector3).dot(u.normalized()) if u.length() > 1e-9 else 0.0)
	var sf := w0
	for i in range(w0, w1 + 1):
		if float(rows[i]["reach"]) > float(rows[sf]["reach"]): sf = i
	var gf := 0
	for i in rows.size():
		if float(rows[i]["reach"]) > float(rows[gf]["reach"]): gf = i
	var num := 0.0; var den := 0.0; var tsw := []
	for i in range(w0, w1 + 1):
		num += float(sp[i]) * float(cs[i]); den += float(sp[i]); tsw.append(float(rows[i]["turn"]))
	tsw.sort()
	var steps := []; var sarcs := []
	for kk in 8:
		var ax: Array = _cam_axes(kk)
		var pk2 := 0.0; var sa := 0.0
		for i in range(1, rows.size()):
			var dd: Vector3 = (rows[i]["head"] as Vector3) - (rows[i - 1]["head"] as Vector3)
			var px: float = Vector2(dd.dot(ax[0]), dd.dot(ax[1])).length() * PX_PER_M
			pk2 = maxf(pk2, px)
			if i > w0 and i <= w1: sa += px
		steps.append(pk2); sarcs.append(sa)
	steps.sort(); sarcs.sort()
	var ok := 0; var pmax := 0; var pfr := 0; var dmax := 0.0; var parts := {}; var pen_t := []
	var hmax := 0; var hfr := 0; var hdep := 0.0
	for r in rows:
		if _guard(r): ok += 1
		hmax = maxi(hmax, int(r.get("hand_n", 0))); hdep = maxf(hdep, float(r.get("hand_depth", 0.0)))
		if int(r.get("hand_n", 0)) > 0: hfr += 1
		var p: int = int(r["pen"])
		pmax = maxi(pmax, p); dmax = maxf(dmax, float(r["pen_depth"]))
		if p > 0:
			pfr += 1
			pen_t.append([snappedf(float(r["t"]), 0.001), p, snappedf(float(r["pen_depth"]), 0.0001)])
		for kk in (r["pen_parts"] as Dictionary):
			parts[kk] = int(parts.get(kk, 0)) + int(r["pen_parts"][kk])
	return {"frames": rows.size(), "pass_frac": float(ok) / float(maxi(rows.size(), 1)), "pen_max": pmax, "pen_frames": pfr, "pen_parts": parts,
			"hand_classed": true, "hand_contact_max": hmax, "hand_contact_frames": hfr, "hand_contact_depth_m": hdep,
			"pen_depth_m": dmax, "pen_t": pen_t, "step_max": float(steps[-1]), "swing_arc_min": float(sarcs[0]), "swing_arc_max": float(sarcs[-1]),
			"turn_med": float(tsw[tsw.size() / 2]), "turn_max": float(tsw[-1]), "t_first": float(rows[0]["t"]), "t_last": float(rows[-1]["t"]),
			"edge_lead": {"strike_t": float(rows[sf]["t"]), "on_travel_strike": float(cs[sf]), "heading_strike": float(rows[sf]["edge"]),
						  "swing": [float(rows[w0]["t"]), float(rows[w1]["t"])], "swing_mean": num / maxf(den, 1e-9), "peak_t": float(rows[pk]["t"]),
						  "strike_global_t": float(rows[gf]["t"]), "on_travel_global": float(cs[gf]), "heading_global": float(rows[gf]["edge"])}}
