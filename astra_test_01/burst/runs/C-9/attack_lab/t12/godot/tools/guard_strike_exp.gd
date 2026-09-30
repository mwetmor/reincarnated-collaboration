extends SceneTree
# LAB EXPERIMENT (not staged): what if a strike did NOT own the axe arm for its whole length?
# The strikes are one-shots that own every bone; the seated axe then goes where the clip's hand
# points it -- through his left leg in the chop's crouch (0-3.5 s), through his shield arm in the
# slash's follow-through (0.79-0.83 s). Here the right arm (RightShoulder..RightHand) and weapon_r
# are held at the GUARD (axe_guard_R, weapon_r at its rest) with weight g(t), composed on the raw
# clip frame by frame (slerp of local rotations, as a filtered Blend2 does):
#   g = 1 before T0, smoothstep to 0 at T1 (the strike takes the arm), 0 through the swing, and
#   back up to 1 over [T2, T3] after it (the arm returns to guard).
# Per frame: the axe's penetration (the acceptance's instrument: every 4th vertex, two agreeing
# vertical rays, the fist excluded) and the guard predicate. The swing's edge is untouched (g = 0).
# env: EXP "clip:T0:T1:T2:T3;..." (times in s; T2 = T3 = -1 for no return)
const F := Vector3(0, 0, 1)
const U := Vector3(0, 1, 0)
const R := Vector3(-1, 0, 0)
const ARM := ["RightShoulder", "RightArm", "RightForeArm", "RightHand"]
var k
var skel: Skeleton3D
var ap: AnimationPlayer
var body: MeshInstance3D
var s_ := 1.0
var wb := -1
var bind := Transform3D()
var H := Vector3.UP
var E := Vector3.BACK
var grip_l := Vector3.ZERO
var head_l := Vector3.ZERO
var pts := PackedVector3Array()
var proxy: MeshInstance3D
var tri_hand := PackedByteArray()
var guard := {}

func _initialize() -> void:
	var specs: PackedStringArray = (OS.get_environment("EXP") if OS.has_environment("EXP") else "attack_chop:3.2:3.7:-1:-1").split(";")
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
	wb = skel.find_bone("weapon_r")
	_axe()
	_body()
	for i in 4: await process_frame
	ap.play("axe_guard_R"); ap.seek(0.0, true, true)
	for b in ARM: guard[b] = skel.get_bone_pose_rotation(skel.find_bone(b))
	for spec in specs:
		var p: PackedStringArray = spec.split(":")
		_run(p[0], float(p[1]), float(p[2]), float(p[3]), float(p[4]))
	quit(0)

func _g(t: float, t0: float, t1: float, t2: float, t3: float) -> float:
	if t <= t0: return 1.0
	if t < t1: return 1.0 - smoothstep(t0, t1, t)
	if t2 < 0.0 or t <= t2: return 0.0
	if t < t3: return smoothstep(t2, t3, t)
	return 1.0

func _run(clip: String, t0: float, t1: float, t2: float, t3: float) -> void:
	var a := ap.get_animation(clip)
	var n: int = int(round(a.length * 24.0))
	ap.play(clip)
	var pen_frames := 0; var worst := 0; var ok := 0; var line := []
	for i in n + 1:
		var t: float = a.length * float(i) / float(n)
		ap.seek(t, true, true)
		var g := _g(t, t0, t1, t2, t3)
		if g > 0.0:
			for b in ARM:
				var bi := skel.find_bone(b)
				skel.set_bone_pose_rotation(bi, skel.get_bone_pose_rotation(bi).slerp(guard[b], g))
			var rr: Quaternion = skel.get_bone_rest(wb).basis.get_rotation_quaternion()
			skel.set_bone_pose_rotation(wb, skel.get_bone_pose_rotation(wb).slerp(rr, g))
		var p := _pen()
		if p > 0:
			pen_frames += 1; worst = maxi(worst, p); line.append("%.2f:%d" % [t, p])
		var gb: Basis = skel.get_bone_global_pose(wb).basis.orthonormalized()
		var h: Vector3 = (gb * H).normalized(); var e: Vector3 = (gb * E).normalized()
		var tl: float = rad_to_deg(h.angle_to(U))
		if g >= 0.999 and tl >= 30.0 and tl <= 60.0 and h.dot(F) > 0.0 and h.dot(R) > 0.0 and absf(rad_to_deg(atan2(e.dot(R), e.dot(F)))) <= 45.0: ok += 1
	print("[exp] %-11s guard until %.2f s, the clip's arm by %.2f s%s: penetration on %d of %d frames (worst %d) %s | guard predicate on %d held frames"
		% [clip, t0, t1, (", back to guard %.2f-%.2f s" % [t2, t3]) if t2 >= 0.0 else "", pen_frames, n + 1, worst, " ".join(line.slice(0, 40)), ok])

func _axe() -> void:
	var mi: MeshInstance3D = (k.gear["_pieces"]["axe"] as Array)[0]
	for i in mi.skin.get_bind_count():
		if String(mi.skin.get_bind_name(i)) == "weapon_r": bind = mi.skin.get_bind_pose(i)
	var verts: PackedVector3Array = mi.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
	var c := Vector3.ZERO; var all := []
	for v in verts:
		var q: Vector3 = bind * v; all.append(q); c += q
	c /= float(all.size())
	for i in range(0, all.size(), 4): pts.append(all[i])
	H = Vector3.UP; E = Vector3.BACK

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
