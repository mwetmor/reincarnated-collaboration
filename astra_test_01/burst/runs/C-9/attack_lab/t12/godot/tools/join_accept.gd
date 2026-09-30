extends SceneTree
# JOIN-1 HOLD ACCEPTANCE -- the barbarian's two-weapon hold (sword main hand, axe off hand) as the JOIN
# cell renderer composes it (join1_render/scripts/render_cells.gd, the agreed layer list): the body GLB
# loaded at runtime (GLTFDocument, as the renderer does), the pieces bound to its skeleton, the kit's
# morphs, and per state the base clip under the spec's layers -- filtered Blend2s, list order, the spec's
# weights and time rules ("pose" = frame 0 held, "clip" = the base clip's time, or the phase map
# {c_base, c_layer}: t_layer = fposmod(t/T_base - c_base + c_layer, 1) * T_layer).
# Sampled at t_i = i*T/N (N = JOIN_N, default 48; the renderer's 12 are every 4th). Per frame, per weapon:
#   GUARD      the T12 predicate, OUTBOARD being his right for the main hand and his LEFT for the off hand:
#              tilt 30-60 deg from vertical, the haft forward and outboard, the head outboard of the fist,
#              |edge heading| <= 45 deg (the edge: the weapon's edge marker, +Z of its bone)
#   PEN        guard_accept.gd's instrument, per weapon: every 4th vertex, INSIDE = odd crossings along all six
#              axis directions against the posed, CPU-skinned body with its morphs; ITS holding hand's fist
#              excluded geometrically, and any point that hand encloses on all six sides; HAND CONTACT (the
#              pommel ruling) -- the butt inside its own holding hand, <= 2 cm -- counted apart
#   CLEAR      the two weapons' nearest approach (every 8th vertex of each), metres
#   READ       per JOIN direction (S SW W NW N NE E SE: the character turned 90 - bearing under the fixed camera,
#              pitch 52.95, 151.34 px/m -- the renderer's own), each weapon's grip-to-far-end length on screen, px
# env: JOIN_SPEC (join_hold.json), JOIN_OUT, JOIN_LABEL, JOIN_N, JOIN_STATES (state=clip,...; default the spec's)
const DIRS := ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]
const BEARING := {"S": 90.0, "SW": 135.0, "W": 180.0, "NW": 225.0, "N": 270.0, "NE": 315.0, "E": 0.0, "SE": 45.0}
const F := Vector3(0, 0, 1)
const U := Vector3(0, 1, 0)
const R := Vector3(-1, 0, 0)
const PPM_RENDER := 151.33680669505316
const PITCH_DEG := 52.9535411256029
const HAND_CONTACT_M := 0.02
const SIX := [Vector3.UP, Vector3.DOWN, Vector3.LEFT, Vector3.RIGHT, Vector3.FORWARD, Vector3.BACK]
var spec: Dictionary
var who: Node3D
var skel: Skeleton3D
var ap: AnimationPlayer
var tree: AnimationTree
var body: MeshInstance3D
var proxy: MeshInstance3D
var s_ := 1.0
var weapons := []
var markers := {}
var llist := []
var tri_dom := PackedInt32Array()
var tri_w := {}      # hand bone name -> PackedFloat32Array of per-triangle mean weight
var wd_ms := 0

func _initialize() -> void:
	wd_ms = Time.get_ticks_msec() + 1800000
	spec = JSON.parse_string(FileAccess.get_file_as_string(OS.get_environment("JOIN_SPEC")))
	var label: String = OS.get_environment("JOIN_LABEL") if OS.has_environment("JOIN_LABEL") else "?"
	var n: int = int(OS.get_environment("JOIN_N")) if OS.has_environment("JOIN_N") else 48
	var bspec: Dictionary = spec["body"]
	who = _load_glb(String(bspec["glb"] if bspec.has("glb") else bspec["path"])); root.add_child(who)
	skel = who.find_children("*", "Skeleton3D", true, false)[0]
	ap = who.find_children("*", "AnimationPlayer", true, false)[0]
	for p in (spec["pieces_list"] if spec.has("pieces_list") else spec["pieces"]):
		_bind(String(p))
	for mi in who.find_children("*", "MeshInstance3D", true, false):
		if (mi as MeshInstance3D).find_blend_shape_by_name("grip_R") >= 0:
			body = mi
	for k in spec.get("morphs", {}):
		if String(k).begins_with("_"): continue
		var i := body.find_blend_shape_by_name(String(k))
		if i >= 0: body.set_blend_shape_value(i, float(spec["morphs"][k]))
	for i in 3: await process_frame
	s_ = skel.global_transform.basis.get_scale().x
	_build_tree()
	_body()
	for wspec in spec["weapons"]:
		weapons.append(_weapon(wspec))
	var states: Dictionary = spec["states_measured"]
	if OS.has_environment("JOIN_STATES"):
		states = {}
		for kv in OS.get_environment("JOIN_STATES").split(","):
			var pr := kv.split("=")
			states[pr[0]] = pr[1]
	var out := {"label": label, "spec": OS.get_environment("JOIN_SPEC"), "n": n, "states": {}}
	for st in states:
		var clip := String(states[st])
		var T := ap.get_animation(clip).length
		var rows := []
		for i in n:
			if Time.get_ticks_msec() > wd_ms: print("[join] WATCHDOG"); quit(4); return
			var t := T * float(i) / float(n)
			_pose(st, clip, t)
			rows.append(_measure(t))
		out["states"][st] = _summarise(st, clip, T, rows)
	var f := FileAccess.open(OS.get_environment("JOIN_OUT") if OS.has_environment("JOIN_OUT") else "/tmp/join_accept.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " ")); f.close()
	quit(0)

func _load_glb(path: String) -> Node3D:
	var doc := GLTFDocument.new(); var st := GLTFState.new()
	var err := doc.append_from_file(path, st)
	if err != OK:
		print("[join] glTF load failed: " + path); quit(3)
	return doc.generate_scene(st)

func _bind(path: String) -> void:
	var src := _load_glb(path)
	for n in src.find_children("*", "Node3D", true, false):
		var par := n.get_parent()
		if par is BoneAttachment3D and not (n is MeshInstance3D) and not (n is Skeleton3D):
			markers[String(n.name)] = {"bone": String((par as BoneAttachment3D).bone_name), "local": (n as Node3D).transform}
	for m in src.find_children("*", "MeshInstance3D", true, false):
		var mi := m as MeshInstance3D
		if mi.mesh == null: continue
		var local := mi.transform; var skin := mi.skin
		mi.owner = null; mi.get_parent().remove_child(mi)
		skel.add_child(mi)
		mi.transform = local; mi.skin = skin; mi.skeleton = NodePath("..")
	src.queue_free()

func _build_tree() -> void:
	for nm in ap.get_animation_list():
		ap.get_animation(nm).loop_mode = Animation.LOOP_NONE
	ap.stop()
	tree = AnimationTree.new(); ap.get_parent().add_child(tree)
	tree.anim_player = tree.get_path_to(ap)
	var bt := AnimationNodeBlendTree.new()
	var a_clip := AnimationNodeAnimation.new(); a_clip.animation = String(spec["states_measured"].values()[0])
	var seek := AnimationNodeTimeSeek.new()
	bt.add_node("clip", a_clip); bt.add_node("seek", seek); bt.connect_node("seek", 0, "clip")
	var prev := "seek"
	llist = spec.get("layers", [])
	for ly in llist:
		var nm := String(ly["name"])
		var act := ap.get_animation(String(ly["action"]))
		if act == null:
			print("[join] layer action not in the GLB: " + String(ly["action"])); quit(3); return
		var an := AnimationNodeAnimation.new(); an.animation = String(ly["action"])
		var ls := AnimationNodeTimeSeek.new()
		var b2 := AnimationNodeBlend2.new(); b2.filter_enabled = true
		var nf := 0
		var skp := String(act.track_get_path(0).get_concatenated_names()) if act.get_track_count() > 0 else ""
		var have := []
		for i in act.get_track_count():
			have.append(String(act.track_get_path(i).get_concatenated_subnames()))
		for bn in ly["bones"]:
			# FROM THE NAMES, not the action's tracks: the importer drops a track equal to the rest pose
			# (remove_immutable_tracks) -- the neutral wrist -- and a filtered bone the action lacks blends to REST
			b2.set_filter_path(NodePath("%s:%s" % [skp, bn]), true); nf += 1
		var missing := []
		for bn in ly["bones"]:
			if not (String(bn) in have): missing.append(bn)
		if missing.size() > 0:
			print("[join] layer %s: the imported action has no track for %s (equal to rest, dropped on import) -- filtered anyway: it blends to rest" % [ly["name"], str(missing)])
		bt.add_node("la_" + nm, an); bt.add_node("ls_" + nm, ls); bt.connect_node("ls_" + nm, 0, "la_" + nm)
		bt.add_node("LL_" + nm, b2)
		bt.connect_node("LL_" + nm, 0, prev); bt.connect_node("LL_" + nm, 1, "ls_" + nm)
		prev = "LL_" + nm
		print("[join] layer %s: %s, %d tracks filtered, weight %s, states %s, time %s" % [nm, ly["action"], nf, ly.get("weight", 1.0), ly.get("states", []), ly.get("time", "pose")])
	bt.connect_node("output", 0, prev)
	tree.tree_root = bt
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	tree.active = true

func _pose(state: String, clip: String, t: float) -> void:
	((tree.tree_root as AnimationNodeBlendTree).get_node("clip") as AnimationNodeAnimation).animation = clip
	for ly in llist:
		var nm := String(ly["name"])
		var on2: bool = state in ly.get("states", [])
		tree.set("parameters/LL_%s/blend_amount" % nm, float(ly.get("weight", 1.0)) if on2 else 0.0)
		var tm = ly.get("time", "pose")
		var tl := 0.0
		if typeof(tm) == TYPE_DICTIONARY:
			var Tb := ap.get_animation(clip).length
			var Tl := ap.get_animation(String(ly["action"])).length
			tl = fposmod(t / Tb - float(tm["c_base"]) + float(tm["c_layer"]), 1.0) * Tl
		elif String(tm) == "clip":
			tl = t
		tree.set("parameters/ls_%s/seek_request" % nm, tl)
	tree.set("parameters/seek/seek_request", t)
	tree.advance(0.0)
	skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)

func _body() -> void:
	var arr := body.mesh.surface_get_arrays(0)
	var verts: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
	var bones = arr[Mesh.ARRAY_BONES]; var wts = arr[Mesh.ARRAY_WEIGHTS]
	var nb: int = int(bones.size() / verts.size())
	var ix: PackedInt32Array = arr[Mesh.ARRAY_INDEX]
	var ntri: int = ix.size() / 3
	for hand in ["RightHand", "LeftHand"]:
		var hb := -1
		for i in body.skin.get_bind_count():
			if _bname(body.skin, i) == hand: hb = i
		var wv := PackedFloat32Array(); wv.resize(verts.size())
		for vi in verts.size():
			var w := 0.0
			for j in nb:
				if int(bones[vi * nb + j]) == hb: w += float(wts[vi * nb + j])
			wv[vi] = w
		var tw := PackedFloat32Array(); tw.resize(ntri)
		for t in ntri:
			tw[t] = (wv[ix[3 * t]] + wv[ix[3 * t + 1]] + wv[ix[3 * t + 2]]) / 3.0
		tri_w[hand] = tw
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

func _weapon(wspec: Dictionary) -> Dictionary:
	var bname := String(wspec["bone"]); var hand := String(wspec["hand"])
	var mi: MeshInstance3D = null; var bind := Transform3D()
	for m in skel.get_children():
		if not (m is MeshInstance3D) or (m as MeshInstance3D).skin == null or m == proxy or m == body: continue
		var sk: Skin = (m as MeshInstance3D).skin
		for i in sk.get_bind_count():
			if _bname(sk, i) != bname: continue
			var arr := (m as MeshInstance3D).mesh.surface_get_arrays(0)
			var bones = arr[Mesh.ARRAY_BONES]; var wts = arr[Mesh.ARRAY_WEIGHTS]
			var nb: int = int(bones.size() / (arr[Mesh.ARRAY_VERTEX] as PackedVector3Array).size())
			var s := 0.0; var tot := 0.0
			for q in bones.size():
				tot += float(wts[q])
				if int(bones[q]) == i: s += float(wts[q])
			if s / maxf(tot, 1e-9) > 0.9:
				mi = m; bind = sk.get_bind_pose(i)
	if mi == null:
		print("[join] no piece on " + bname); quit(3); return {}
	var bi := skel.find_bone(bname)
	var verts: PackedVector3Array = mi.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
	var allp := []
	var c := Vector3.ZERO
	for v in verts:
		var p: Vector3 = bind * v; allp.append(p); c += p
	c /= float(allp.size())
	var xx := 0.0; var xy := 0.0; var xz := 0.0; var yy := 0.0; var yz := 0.0; var zz := 0.0
	for p in allp:
		var d: Vector3 = p - c
		xx += d.x * d.x; xy += d.x * d.y; xz += d.x * d.z; yy += d.y * d.y; yz += d.y * d.z; zz += d.z * d.z
	var ax := Vector3(1, 1, 1).normalized()
	for it in 80:
		ax = Vector3(xx * ax.x + xy * ax.y + xz * ax.z, xy * ax.x + yy * ax.y + yz * ax.z, xz * ax.x + yz * ax.y + zz * ax.z).normalized()
	var mk: Dictionary = markers[String(wspec["edge_marker"])]
	var edge_l: Vector3 = (mk["local"] as Transform3D).origin
	if (edge_l - c).dot(ax) < 0.0: ax = -ax
	var H: Vector3 = ax
	var E: Vector3 = ((edge_l - c) - (edge_l - c).dot(H) * H).normalized()
	var grip_l: Vector3 = c + H * (-c).dot(H)
	var head_l: Vector3 = c + H * (edge_l - c).dot(H)
	var pts := PackedVector3Array(); var cpts := PackedVector3Array()
	var smax := -1e9; var smin := 1e9
	for i in allp.size():
		var sp: float = ((allp[i] as Vector3) - grip_l).dot(H); smax = maxf(smax, sp); smin = minf(smin, sp)
		if i % 4 == 0: pts.append(allp[i])
		if i % 8 == 0: cpts.append(allp[i])
	# THE FIST: its holding hand's vertices in the weapon bone's rest frame
	var barr := proxy.mesh.surface_get_arrays(0)
	var bv: PackedVector3Array = barr[Mesh.ARRAY_VERTEX]
	var bb = barr[Mesh.ARRAY_BONES]; var bw = barr[Mesh.ARRAY_WEIGHTS]
	var nbb: int = int(bb.size() / bv.size())
	var hb := -1
	for i in body.skin.get_bind_count():
		if _bname(body.skin, i) == hand: hb = i
	var to_w: Transform3D = skel.get_bone_rest(bi).affine_inverse() * body.skin.get_bind_pose(hb)
	var lo := 1e9; var hi := -1e9
	for vi in bv.size():
		var w := 0.0
		for j in nbb:
			if int(bb[vi * nbb + j]) == hb: w += float(bw[vi * nbb + j])
		if w <= 0.5: continue
		var q: Vector3 = to_w * bv[vi]
		var sa: float = (q - grip_l).dot(H)
		if ((q - grip_l) - sa * H).length() * s_ > 0.06: continue
		lo = minf(lo, sa); hi = maxf(hi, sa)
	var rs := []
	for pl in pts:
		var sa2: float = (pl - grip_l).dot(H)
		if absf(sa2) * s_ < 0.03: rs.append(((pl - grip_l) - sa2 * H).length())
	rs.sort()
	var r_haft: float = float(rs[int(rs.size() * 0.9)]) if rs.size() > 4 else 0.02 / s_
	var side: float = 1.0 if String(wspec["side"]) == "R" else -1.0
	print("[join] %s on %s (%s): %d vertices, the haft %.3f m below the grip and %.3f above; the fist %.3f..%+.3f m, haft radius %.4f m; edge marker %s"
		% [wspec["name"], bname, hand, verts.size(), -smin * s_, smax * s_, (lo - 0.01 / s_) * s_, (hi + 0.01 / s_) * s_, r_haft * s_, wspec["edge_marker"]])
	return {"name": String(wspec["name"]), "bone": bi, "hand": hand, "side": side, "R": R * side, "H": H, "E": E, "grip_l": grip_l,
			"head_l": head_l, "len": smax, "pts": pts, "cpts": cpts, "fist_s": [lo - 0.01 / s_, hi + 0.01 / s_], "fist_r": r_haft + 0.01 / s_}

func _bname(sk: Skin, i: int) -> String:
	# a runtime-imported skin may bind by BONE INDEX (no name): fall back to the skeleton's bone name
	var nm := String(sk.get_bind_name(i))
	if nm == "" and sk.get_bind_bone(i) >= 0:
		nm = skel.get_bone_name(sk.get_bind_bone(i))
	return nm

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

func _measure(t: float) -> Dictionary:
	var baked: ArrayMesh = proxy.bake_mesh_from_current_skeleton_pose()
	var tm: TriangleMesh = baked.generate_triangle_mesh()
	var bx: AABB = baked.get_aabb()
	var row := {"t": t, "w": {}}
	var world := []
	for w in weapons:
		var g: Transform3D = skel.get_bone_global_pose(int(w["bone"]))
		var gb: Basis = g.basis.orthonormalized()
		var h: Vector3 = (gb * (w["H"] as Vector3)).normalized(); var e: Vector3 = (gb * (w["E"] as Vector3)).normalized()
		var RS: Vector3 = w["R"]
		var grip: Vector3 = (g * (w["grip_l"] as Vector3)) * s_
		var head: Vector3 = (g * (w["head_l"] as Vector3)) * s_
		var m := {"tilt": rad_to_deg(h.angle_to(U)), "fwd": h.dot(F), "out": h.dot(RS), "head_out": (head - grip).dot(RS),
				  "edge": rad_to_deg(atan2(e.dot(RS), e.dot(F)))}
		m["guard"] = float(m["tilt"]) >= 30.0 and float(m["tilt"]) <= 60.0 and float(m["fwd"]) > 0.0 and float(m["out"]) > 0.0 \
			and float(m["head_out"]) > 0.0 and absf(float(m["edge"])) <= 45.0
		# READ: the grip-to-far-end vector on screen, per JOIN direction
		var v: Vector3 = gb * ((w["H"] as Vector3) * float(w["len"])) * s_
		var a := deg_to_rad(PITCH_DEG)
		var cr := Vector3(1, 0, 0); var cu := Vector3(0, cos(a), -sin(a))
		var rd := {}
		for dn in DIRS:
			var vr: Vector3 = Basis(Vector3.UP, deg_to_rad(90.0 - float(BEARING[dn]))) * v
			rd[dn] = Vector2(vr.dot(cr), vr.dot(cu)).length() * PPM_RENDER
		m["read_px"] = rd
		# PEN (and the hand class), guard_accept.gd's instrument with this weapon's own hand
		var tw: PackedFloat32Array = tri_w[String(w["hand"])]
		var inside := 0; var depth := 0.0; var hand_n := 0; var hand_d := 0.0; var parts := {}
		var H: Vector3 = w["H"]; var gl: Vector3 = w["grip_l"]
		for pl in (w["pts"] as PackedVector3Array):
			var sa: float = (pl - gl).dot(H)
			var ra: float = ((pl - gl) - sa * H).length()
			if sa >= float(w["fist_s"][0]) and sa <= float(w["fist_s"][1]) and ra <= float(w["fist_r"]): continue
			var p: Vector3 = g * pl
			if not bx.has_point(p): continue
			var odd := true; var near := 1e9; var in_hand := true; var fn := -1; var fu := -1
			for d in SIX:
				var c: Array = _cross(tm, p, d)
				if int(c[0]) % 2 == 0:
					odd = false; break
				if float(c[2]) < near: fn = int(c[1])
				near = minf(near, float(c[2]))
				if d == Vector3.UP: fu = int(c[1])
				if int(c[1]) < 0 or float(tw[int(c[1])]) <= 0.5: in_hand = false
			if not odd or in_hand: continue
			var zone: String = "butt" if sa < 0.0 else ("head" if ra * s_ > 0.03 else "haft")
			if zone == "butt" and fn >= 0 and float(tw[fn]) > 0.5 and near * s_ <= HAND_CONTACT_M:
				hand_n += 1; hand_d = maxf(hand_d, near * s_); continue
			inside += 1; depth = maxf(depth, near * s_)
			parts[zone] = int(parts.get(zone, 0)) + 1
		m["pen"] = inside; m["pen_depth"] = depth; m["pen_parts"] = parts; m["hand_n"] = hand_n; m["hand_depth"] = hand_d
		row["w"][w["name"]] = m
		var wp := PackedVector3Array()
		for pl in (w["cpts"] as PackedVector3Array): wp.append((g * pl) * s_)
		world.append(wp)
	# CLEAR: the nearest approach of the two weapons
	var best := 1e9
	if world.size() == 2:
		for a2 in (world[0] as PackedVector3Array):
			for b2 in (world[1] as PackedVector3Array):
				var d2: float = a2.distance_squared_to(b2)
				if d2 < best: best = d2
	row["clear_m"] = sqrt(best)
	return row

func _summarise(st: String, clip: String, T: float, rows: Array) -> Dictionary:
	var out := {"clip": clip, "T_s": T, "frames": rows.size(), "weapons": {}}
	var clear := 1e9; var clear_t := 0.0
	for r in rows:
		if float(r["clear_m"]) < clear: clear = float(r["clear_m"]); clear_t = float(r["t"])
	out["clear_min_m"] = clear; out["clear_min_t"] = clear_t
	for w in weapons:
		var nm := String(w["name"])
		var ok := 0; var ok12 := 0; var n12 := 0; var pmax := 0; var pfr := 0; var dmax := 0.0; var hmax := 0; var hfr := 0; var hdep := 0.0
		var cols := {"tilt": [], "fwd": [], "out": [], "head_out": [], "edge": []}
		var readmin := {}
		var parts := {}
		for i in rows.size():
			var m: Dictionary = rows[i]["w"][nm]
			if bool(m["guard"]): ok += 1
			if i % 4 == 0:
				n12 += 1
				if bool(m["guard"]): ok12 += 1
			for k in cols: (cols[k] as Array).append(float(m[k]))
			pmax = maxi(pmax, int(m["pen"])); dmax = maxf(dmax, float(m["pen_depth"]))
			if int(m["pen"]) > 0: pfr += 1
			hmax = maxi(hmax, int(m["hand_n"])); hdep = maxf(hdep, float(m["hand_depth"]))
			if int(m["hand_n"]) > 0: hfr += 1
			for kk in (m["pen_parts"] as Dictionary): parts[kk] = int(parts.get(kk, 0)) + int(m["pen_parts"][kk])
			for dn in DIRS:
				var px: float = float(m["read_px"][dn])
				readmin[dn] = minf(float(readmin.get(dn, 1e9)), px)
		var o := {"pass_frac": float(ok) / float(rows.size()), "pass_frac_renderer_12": float(ok12) / float(maxi(n12, 1)),
				  "pen_max": pmax, "pen_frames": pfr, "pen_depth_m": dmax, "pen_parts": parts,
				  "hand_contact_max": hmax, "hand_contact_frames": hfr, "hand_contact_depth_m": hdep,
				  "read_min_px": readmin, "length_m": float(w["len"]) * s_}
		var worst := 1e9; var wd := ""
		for dn in DIRS:
			if float(readmin[dn]) < worst: worst = float(readmin[dn]); wd = dn
		o["read_worst_px"] = worst; o["read_worst_dir"] = wd
		for k in cols:
			var v: Array = cols[k]; v.sort(); o[k] = float(v[v.size() / 2]); o[k + "_range"] = [float(v[0]), float(v[-1])]
		out["weapons"][nm] = o
		print("[join] %-6s %-5s %-10s guard %3d%% (renderer's 12: %3d%%) | tilt %4.1f fwd %+.2f out %+.2f head out %+.2f edge %+4.0f (medians; tilt %.0f..%.0f, edge %+.0f..%+.0f) | pen worst %d (%.3f m), %d of %d frames %s | hand contact %d (%.3f m) | read worst %.0f px (%s) of %.0f"
			% [st, nm, clip, int(round(100.0 * o["pass_frac"])), int(round(100.0 * o["pass_frac_renderer_12"])), o["tilt"], o["fwd"], o["out"], o["head_out"], o["edge"],
			   (o["tilt_range"] as Array)[0], (o["tilt_range"] as Array)[1], (o["edge_range"] as Array)[0], (o["edge_range"] as Array)[1],
			   pmax, dmax, pfr, rows.size(), JSON.stringify(parts), hmax, hdep, worst, wd, float(w["len"]) * s_ * PPM_RENDER])
	print("[join] %-6s clear: the weapons' nearest approach %.3f m (t %.3f s)" % [st, clear, clear_t])
	return out
