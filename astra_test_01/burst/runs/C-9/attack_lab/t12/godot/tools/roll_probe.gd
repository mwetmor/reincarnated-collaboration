extends SceneTree
# LAB PROBE: at chosen frames of a clip (raw), the axe's penetration as a function of weapon_r's
# ROLL about the haft (the one free angle a strike's channel has) and of a small TURN of the haft
# in the fist (about the two axes across the haft), with the edge along the travel reported for
# each roll. weapon_r's local rotation = rest * turn * roll (the channel's own form: rest * roll).
# env: PROBE "clip:t,clip:t,..."  PROBE_TURNS "0,10,20"
const U := Vector3(0, 1, 0)
var k
var skel: Skeleton3D
var ap: AnimationPlayer
var body: MeshInstance3D
var s_ := 1.0
var wb := -1
var W_rest := Transform3D()
var head_l := Vector3.ZERO
var E := Vector3.BACK
var pts := PackedVector3Array()
var proxy: MeshInstance3D
var tri_hand := PackedByteArray()

func _initialize() -> void:
	var specs: PackedStringArray = OS.get_environment("PROBE").split(",", false)
	var turns: PackedStringArray = (OS.get_environment("PROBE_TURNS") if OS.has_environment("PROBE_TURNS") else "0").split(",", false)
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
	wb = skel.find_bone("weapon_r"); W_rest = skel.get_bone_rest(wb)
	_axe(); _body()
	for i in 4: await process_frame
	for spec in specs:
		var clip := spec.split(":")[0]; var t := float(spec.split(":")[1])
		var a := ap.get_animation(clip)
		ap.play(clip)
		# the travel at t (central difference over 1/24 s), with the channel as baked
		ap.seek(maxf(t - 1.0 / 24.0, 0.0), true, true)
		var h0: Vector3 = skel.get_bone_global_pose(wb) * head_l
		ap.seek(minf(t + 1.0 / 24.0, a.length), true, true)
		var h1: Vector3 = skel.get_bone_global_pose(wb) * head_l
		ap.seek(t, true, true)
		var baked_q: Quaternion = skel.get_bone_pose_rotation(wb)
		var base_pen := _pen()
		var six := _pen6()
		var line := "[probe] %s @ %.3f: as baked %d (2 rays), %d inside by all 6 rays, %d by 5+ of 6 | depth of the 6-ray points %s" % [clip, t, base_pen, int(six[0]), int(six[1]), str(six[2])]
		if OS.get_environment("PROBE_SIX_ONLY") == "1":
			print(line); continue
		for ts in turns:
			var tdeg := float(ts)
			for ax in ([Vector3.RIGHT, Vector3.BACK, Vector3.LEFT, Vector3.FORWARD] if tdeg > 0.0 else [Vector3.RIGHT]):
				var best := ""
				var clear := []
				for rd in range(-180, 180, 15):
					var q: Quaternion = (W_rest.basis * Basis(ax, deg_to_rad(tdeg)) * Basis(Vector3.UP, deg_to_rad(float(rd)))).get_rotation_quaternion()
					skel.set_bone_pose_rotation(wb, q)
					var p := _pen()
					var g: Transform3D = skel.get_bone_global_pose(wb)
					var hh: Vector3 = (g.basis * Vector3.UP).normalized(); var e: Vector3 = (g.basis * E).normalized()
					var v: Vector3 = h1 - h0; var u: Vector3 = v - v.dot(hh) * hh
					var c: float = e.dot(u.normalized()) if u.length() > 1e-9 else 0.0
					if p == 0: clear.append("%d(%+.2f)" % [rd, c])
				line += " turn %.0f about %s: clear at %s |" % [tdeg, str(ax), " ".join(clear) if clear.size() > 0 else "none"]
		skel.set_bone_pose_rotation(wb, baked_q)
		print(line)
	quit(0)

func _axe() -> void:
	var mi: MeshInstance3D = (k.gear["_pieces"]["axe"] as Array)[0]
	var bind := Transform3D()
	for i in mi.skin.get_bind_count():
		if String(mi.skin.get_bind_name(i)) == "weapon_r": bind = mi.skin.get_bind_pose(i)
	var verts: PackedVector3Array = mi.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
	var c := Vector3.ZERO; var all := []
	for v in verts:
		var q: Vector3 = bind * v; all.append(q); c += q
	c /= float(all.size())
	for i in range(0, all.size(), 4): pts.append(all[i])
	var mk: Node3D = (k.gear["_pieces"]["_markers_axe"] as Dictionary)["axe_edge"]
	var edge_l: Vector3 = mk.transform.origin
	var att := mk.get_parent() as BoneAttachment3D
	if att != null and skel.find_bone(att.bone_name) != wb:
		edge_l = skel.get_bone_global_rest(wb).affine_inverse() * (skel.get_bone_global_rest(skel.find_bone(att.bone_name)) * edge_l)
	E = ((edge_l - c) - (edge_l - c).dot(Vector3.UP) * Vector3.UP).normalized()
	head_l = c + Vector3.UP * (edge_l - c).dot(Vector3.UP)

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
	var g: Transform3D = skel.get_bone_global_pose(wb)
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

func _pen6() -> Array:
	# INSIDE by crossing parity along all six axis directions: a closed body gives an odd count in
	# every direction for a point inside it; a hole or an overlap in the mesh fools one or two rays,
	# not six. [all six odd, >= 5 of 6 odd, the nearest surface over the six for the all-six points]
	skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)
	var baked: ArrayMesh = proxy.bake_mesh_from_current_skeleton_pose()
	var tm: TriangleMesh = baked.generate_triangle_mesh()
	var bx: AABB = baked.get_aabb()
	var g: Transform3D = skel.get_bone_global_pose(wb)
	var n6 := 0; var n5 := 0; var depths := []
	for pl in pts:
		var p: Vector3 = g * pl
		if not bx.has_point(p): continue
		var odd := 0; var near := 1e9
		for d in [Vector3.UP, Vector3.DOWN, Vector3.LEFT, Vector3.RIGHT, Vector3.FORWARD, Vector3.BACK]:
			var o := p; var n := 0
			for i in 32:
				var r = tm.intersect_ray(o, d)
				if typeof(r) != TYPE_DICTIONARY or (r as Dictionary).is_empty(): break
				if n == 0: near = minf(near, ((r["position"] as Vector3) - p).length())
				n += 1
				o = (r["position"] as Vector3) + d * 0.002
			if n % 2 == 1: odd += 1
		if odd == 6:
			n6 += 1; depths.append(snappedf(near * s_, 0.001))
		if odd >= 5: n5 += 1
	depths.sort()
	return [n6, n5, depths.slice(maxi(depths.size() - 3, 0))]
