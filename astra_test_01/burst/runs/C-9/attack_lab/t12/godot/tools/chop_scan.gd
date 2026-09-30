extends SceneTree
# CHOP CANDIDATES, scanned raw: per frame of each clip (24 fps), the axe head's speed, its reach
# forward of the hips, its height, the edge along the travel (the axe as mounted -- weapon_r at
# rest unless the clip keys it), the haft's tilt, and the axe's penetration of the body (the
# acceptance's instrument; no release -- the clip owns the arm). Then every SWING: a local speed
# peak >= 50% of the clip's highest, its window (contiguous >= 50% of that peak) and its strike
# frame (furthest forward of the hips inside the window).
# env: SCAN "clip,clip,..."; SCAN_OUT (json)
const F := Vector3(0, 0, 1)
const U := Vector3(0, 1, 0)
const R := Vector3(-1, 0, 0)
const PX_PER_M := 77.8
const PITCH_DEG := 52.9535411256029
var k
var skel: Skeleton3D
var ap: AnimationPlayer
var body: MeshInstance3D
var s_ := 1.0
var ab := -1
var H := Vector3.UP
var E := Vector3.BACK
var head_l := Vector3.ZERO
var grip_l := Vector3.ZERO
var pts := PackedVector3Array()
var proxy: MeshInstance3D
var tri_hand := PackedByteArray()

func _initialize() -> void:
	var clips: PackedStringArray = (OS.get_environment("SCAN") if OS.has_environment("SCAN") else "cand_092").split(",", false)
	var ground := StaticBody3D.new()
	ground.collision_layer = CliffWorld.TERRAIN_BIT
	var cs := CollisionShape3D.new(); var box := BoxShape3D.new(); box.size = Vector3(4000, 1, 4000)
	cs.shape = box; cs.position = Vector3(0, -0.5, 0); ground.add_child(cs); root.add_child(ground)
	k = load("res://scripts/knight.gd").new()
	k.setup(Vector3(0.681998491287231, 0.0, -0.731353580951691), Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541), Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487), 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	for i in 4: await process_frame
	skel = k._skel; ap = k._anim; body = k._mesh
	(k._tree as AnimationTree).active = false
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	s_ = skel.global_transform.basis.get_scale().x
	_axe()
	_body()
	for i in 4: await process_frame
	var out := {}
	for clip in clips:
		out[clip] = _scan(clip)
	var f := FileAccess.open(OS.get_environment("SCAN_OUT") if OS.has_environment("SCAN_OUT") else "/tmp/scan.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " ")); f.close()
	quit(0)

func _scan(clip: String) -> Dictionary:
	var a := ap.get_animation(clip)
	if a == null:
		print("[scan] no clip %s" % clip); return {}
	var n: int = int(round(a.length * 24.0))
	ap.play(clip)
	var rows := []
	var hipb := skel.find_bone("Hips")
	for i in n + 1:
		var t: float = a.length * float(i) / float(n)
		ap.seek(t, true, true)
		var g: Transform3D = skel.get_bone_global_pose(ab)
		var gb: Basis = g.basis.orthonormalized()
		var h: Vector3 = (gb * H).normalized(); var e: Vector3 = (gb * E).normalized()
		var head: Vector3 = (g * head_l) * s_
		var hip: Vector3 = skel.get_bone_global_pose(hipb).origin * s_
		rows.append({"t": t, "head": head, "h": h, "e": e, "reach": (head - hip).dot(F), "hy": head.y, "tilt": rad_to_deg(h.angle_to(U)), "pen": _pen()})
	var sp := []
	for i in rows.size():
		var i0: int = maxi(i - 1, 0); var i1: int = mini(i + 1, rows.size() - 1)
		sp.append(((rows[i1]["head"] as Vector3) - (rows[i0]["head"] as Vector3)).length() / maxf(float(rows[i1]["t"]) - float(rows[i0]["t"]), 1e-6))
	var cs := []
	for i in rows.size():
		var i0: int = maxi(i - 1, 0); var i1: int = mini(i + 1, rows.size() - 1)
		var v: Vector3 = (rows[i1]["head"] as Vector3) - (rows[i0]["head"] as Vector3)
		var hh: Vector3 = rows[i]["h"]
		var u: Vector3 = v - v.dot(hh) * hh
		cs.append((rows[i]["e"] as Vector3).dot(u.normalized()) if u.length() > 1e-9 else 0.0)
	var top := 0.0
	for x in sp: top = maxf(top, float(x))
	var swings := []
	for i in range(1, sp.size() - 1):
		if float(sp[i]) >= float(sp[i - 1]) and float(sp[i]) > float(sp[i + 1]) and float(sp[i]) >= 0.5 * top:
			var w0 := i; var w1 := i
			while w0 > 0 and float(sp[w0 - 1]) >= 0.5 * float(sp[i]): w0 -= 1
			while w1 < sp.size() - 1 and float(sp[w1 + 1]) >= 0.5 * float(sp[i]): w1 += 1
			var sf := w0
			for j in range(w0, w1 + 1):
				if float(rows[j]["reach"]) > float(rows[sf]["reach"]): sf = j
			var num := 0.0; var den := 0.0; var pen := 0
			for j in range(w0, w1 + 1):
				num += float(sp[j]) * float(cs[j]); den += float(sp[j]); pen = maxi(pen, int(rows[j]["pen"]))
			# the screen arc of this swing, per cell
			var arcs := []
			for kk in 8:
				var y := deg_to_rad(47.0 + 45.0 * float(kk)); var th := deg_to_rad(PITCH_DEG)
				var fh := Vector3(sin(y), 0, cos(y))
				var dv := (fh * cos(th) + Vector3(0, -1, 0) * sin(th)).normalized()
				var rr := fh.cross(Vector3.UP).normalized(); var uu := rr.cross(dv).normalized()
				var tot := 0.0
				for j in range(w0 + 1, w1 + 1):
					var dd: Vector3 = (rows[j]["head"] as Vector3) - (rows[j - 1]["head"] as Vector3)
					tot += Vector2(dd.dot(rr), dd.dot(uu)).length() * PX_PER_M
				arcs.append(tot)
			arcs.sort()
			var dup := false
			for s in swings:
				if int(s["w0"]) == w0: dup = true
			if not dup:
				swings.append({"peak_t": float(rows[i]["t"]), "peak_m_s": float(sp[i]), "w0": w0, "w1": w1, "window": [float(rows[w0]["t"]), float(rows[w1]["t"])],
							   "strike_t": float(rows[sf]["t"]), "cos_strike": float(cs[sf]), "cos_mean": num / maxf(den, 1e-9),
							   "head_drop_m": float(rows[w0]["hy"]) - float(rows[w1]["hy"]), "reach_strike": float(rows[sf]["reach"]),
							   "arc_min_px": float(arcs[0]), "arc_max_px": float(arcs[-1]), "pen_max": pen})
	print("[scan] %-10s %.3f s, %d frames, top head speed %.2f m/s" % [clip, a.length, rows.size(), top])
	var line := ""
	for i in rows.size():
		if i % 2 == 0:
			line += " %.2f:%.1f/%+.2f/%s" % [float(rows[i]["t"]), float(sp[i]), float(rows[i]["hy"]), str(int(rows[i]["pen"]))]
	print("[scan]   t:speed/head height/pen %s" % line)
	for s in swings:
		print("[scan]   SWING peak %.3f s (%.2f m/s) window %.3f-%.3f s, strike %.3f s: edge along the travel %+.2f at the strike, %+.2f over the swing; head drops %+.2f m; reach %+.2f m; screen arc %3.0f-%3.0f px; pen %d"
			% [float(s["peak_t"]), float(s["peak_m_s"]), float(s["window"][0]), float(s["window"][1]), float(s["strike_t"]), float(s["cos_strike"]), float(s["cos_mean"]),
			   float(s["head_drop_m"]), float(s["reach_strike"]), float(s["arc_min_px"]), float(s["arc_max_px"]), int(s["pen_max"])])
	var slim := []
	for i in rows.size():
		slim.append({"t": float(rows[i]["t"]), "speed": float(sp[i]), "hy": float(rows[i]["hy"]), "reach": float(rows[i]["reach"]), "cos": float(cs[i]), "tilt": float(rows[i]["tilt"]), "pen": int(rows[i]["pen"])})
	return {"length_s": a.length, "top_m_s": top, "swings": swings, "rows": slim}

func _axe() -> void:
	var mi: MeshInstance3D = (k.gear["_pieces"]["axe"] as Array)[0]
	var bind := Transform3D()
	for i in mi.skin.get_bind_count():
		if String(mi.skin.get_bind_name(i)) == "weapon_r": bind = mi.skin.get_bind_pose(i)
	ab = skel.find_bone("weapon_r")
	var verts: PackedVector3Array = mi.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
	var c := Vector3.ZERO; var all := []
	for v in verts:
		var q: Vector3 = bind * v; all.append(q); c += q
	c /= float(all.size())
	for i in range(0, all.size(), 4): pts.append(all[i])
	var mk: Node3D = (k.gear["_pieces"]["_markers_axe"] as Dictionary)["axe_edge"]
	var edge_l: Vector3 = mk.transform.origin
	var att := mk.get_parent() as BoneAttachment3D
	if att != null and skel.find_bone(att.bone_name) != ab:
		edge_l = skel.get_bone_global_rest(ab).affine_inverse() * (skel.get_bone_global_rest(skel.find_bone(att.bone_name)) * edge_l)
	H = Vector3.UP
	E = ((edge_l - c) - (edge_l - c).dot(H) * H).normalized()
	head_l = c + H * (edge_l - c).dot(H)
	grip_l = c + H * (-c).dot(H)

func _body() -> void:
	var arr := body.mesh.surface_get_arrays(0)
	var verts: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
	var bones = arr[Mesh.ARRAY_BONES]; var weights = arr[Mesh.ARRAY_WEIGHTS]
	var nb: int = int(bones.size() / verts.size())
	var rh := -1
	for i in body.skin.get_bind_count():
		if String(body.skin.get_bind_name(i)) == "RightHand": rh = i
	var wrh := PackedFloat32Array(); wrh.resize(verts.size())
	for vi in verts.size():
		var w := 0.0
		for j in nb:
			if int(bones[vi * nb + j]) == rh: w += float(weights[vi * nb + j])
		wrh[vi] = w
	var ix: PackedInt32Array = arr[Mesh.ARRAY_INDEX]
	tri_hand.resize(ix.size() / 3)
	for t in ix.size() / 3:
		tri_hand[t] = 1 if (wrh[ix[3 * t]] + wrh[ix[3 * t + 1]] + wrh[ix[3 * t + 2]]) / 3.0 > 0.5 else 0
	var mix: ArrayMesh = body.bake_mesh_from_current_blend_shape_mix()
	var parr := arr.duplicate()
	parr[Mesh.ARRAY_VERTEX] = mix.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
	var am := ArrayMesh.new()
	am.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, parr, [], {}, Mesh.ARRAY_FLAG_USE_8_BONE_WEIGHTS if nb == 8 else 0)
	proxy = MeshInstance3D.new(); proxy.mesh = am; proxy.visible = false
	proxy.skin = body.skin; proxy.skeleton = NodePath("..")
	skel.add_child(proxy); proxy.transform = body.transform

func _cross(tm: TriangleMesh, p: Vector3, d: Vector3) -> Array:
	var o := p; var n := 0; var first := -1
	for i in 32:
		var r = tm.intersect_ray(o, d)
		if typeof(r) != TYPE_DICTIONARY or (r as Dictionary).is_empty(): break
		n += 1
		if first < 0: first = int(r["face_index"])
		o = (r["position"] as Vector3) + d * 0.002
	return [n, first]

func _pen() -> int:
	skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)
	var baked: ArrayMesh = proxy.bake_mesh_from_current_skeleton_pose()
	if baked == null: return -1
	var tm: TriangleMesh = baked.generate_triangle_mesh()
	var bx: AABB = baked.get_aabb()
	var g: Transform3D = skel.get_bone_global_pose(ab)
	var inside := 0
	for pl in pts:
		var p: Vector3 = g * pl
		if p.x < bx.position.x or p.x > bx.end.x or p.z < bx.position.z or p.z > bx.end.z or p.y > bx.end.y: continue
		var up: Array = _cross(tm, p, Vector3.UP)
		var dn: Array = _cross(tm, p, Vector3.DOWN)
		if int(up[0]) % 2 == 0 or int(dn[0]) % 2 == 0: continue
		if int(up[1]) >= 0 and int(dn[1]) >= 0 and tri_hand[int(up[1])] == 1 and tri_hand[int(dn[1])] == 1: continue
		inside += 1
	return inside
