extends SceneTree
# Does the in-memory weapon_r track do what the solve intended? For a few frames: the intended
# world haft (hand x solved local x +Y), the skeleton's weapon_r after the seek, and the axe's own
# vertices (its skin, posed) -- three readings that must agree.
const U := Vector3(0, 1, 0)
func _initialize() -> void:
	create_timer(120.0).timeout.connect(func(): print("[check] WATCHDOG"); quit(4))
	var k = load("res://scripts/knight.gd").new()
	k.setup(Vector3.RIGHT, Vector3.UP, Vector3.FORWARD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	for i in 4: await process_frame
	var skel: Skeleton3D = k._skel
	var ap: AnimationPlayer = k._anim
	(k._tree as AnimationTree).active = false
	for c in skel.get_children():
		if c is SkeletonModifier3D: (c as SkeletonModifier3D).active = false
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var sol = JSON.parse_string(FileAccess.get_file_as_string(OS.get_environment("SOLVE")))
	var wr: Dictionary = sol["weapon_r"]
	var hb := skel.find_bone("RightHand"); var wb := skel.find_bone("weapon_r")
	var a := ap.get_animation("block")
	var prefix := ""
	for t in a.get_track_count():
		var pth := String(a.track_get_path(t))
		if pth.ends_with(":RightHand"): prefix = pth.substr(0, pth.length() - "RightHand".length())
	print("[check] prefix '%s'; weapon_r parent %s; rest %s" % [prefix, skel.get_bone_name(skel.get_bone_parent(wb)), str(skel.get_bone_rest(wb))])
	var ti := a.add_track(Animation.TYPE_ROTATION_3D)
	a.track_set_path(ti, NodePath(prefix + "weapon_r"))
	var ts: Array = wr["block"]["times"]; var qs: Array = wr["block"]["quats"]
	for j in ts.size():
		var q: Array = qs[j]
		a.rotation_track_insert_key(ti, float(ts[j]), Quaternion(q[0], q[1], q[2], q[3]))
	var mi: MeshInstance3D = (k.gear["_pieces"]["axe"] as Array)[0]
	var bind := Transform3D()
	for i in mi.skin.get_bind_count():
		if String(mi.skin.get_bind_name(i)) == "weapon_r": bind = mi.skin.get_bind_pose(i)
	var verts: PackedVector3Array = mi.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
	for j in [10, 40, 80]:
		var t: float = float(ts[j])
		ap.play("block"); ap.seek(t, true, true)
		var q: Array = qs[j]
		var qq := Quaternion(q[0], q[1], q[2], q[3])
		var hg: Basis = skel.get_bone_global_pose(hb).basis.orthonormalized()
		var intended: Vector3 = (hg * Basis(qq) * Vector3.UP).normalized()
		var actual_local: Quaternion = skel.get_bone_pose_rotation(wb)
		var wg: Transform3D = skel.get_bone_global_pose(wb)
		var bone_haft: Vector3 = (wg.basis.orthonormalized() * Vector3.UP).normalized()
		# the axe's own long axis, posed: first and last vertices along its bind +Y
		var lo := Vector3.ZERO; var hi := Vector3.ZERO; var ylo := 1e9; var yhi := -1e9
		for v in verts:
			var p: Vector3 = bind * v
			if p.y < ylo: ylo = p.y; lo = p
			if p.y > yhi: yhi = p.y; hi = p
		var mesh_haft: Vector3 = ((wg * hi) - (wg * lo)).normalized()
		print("[check] block t=%.3f | local key vs pose: %.2f deg | haft tilt: intended %.1f, bone %.1f, mesh %.1f deg | intended vs mesh %.2f deg"
			% [t, rad_to_deg(qq.angle_to(actual_local)), rad_to_deg(intended.angle_to(U)), rad_to_deg(bone_haft.angle_to(U)), rad_to_deg(mesh_haft.angle_to(U)), rad_to_deg(intended.angle_to(mesh_haft))])
	quit(0)
