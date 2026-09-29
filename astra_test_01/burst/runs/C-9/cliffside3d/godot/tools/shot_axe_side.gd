extends SceneTree
# C-9 D2: settle the axe edge -- one still of the strike, seen PERPENDICULAR TO THE SWING
# PLANE, with three points marked.
#
#   green    axe_edge, the export's own marker
#   magenta  the leading point: the head vertex furthest along the direction of travel
#   cyan     the poll: the head vertex furthest across the haft axis from the edge side
#
# A bearded axe hangs its edge down the haft, so a leading point 0.131 m from the marker
# and 0.08 m nearer the hand is either the beard's toe -- the edge side, which is correct --
# or the poll, which would mean the head is on backwards. Those are distinguishable by
# WHICH SIDE OF THE HAFT AXIS the point falls, and that is measured here as well as drawn.
#
# The haft axis is taken from the geometry rather than assumed: the butt is the axe vertex
# furthest from the edge marker, the head centroid is the mean of the head cluster, and the
# axis runs between them. Points are then signed by their offset across that axis, in the
# direction the edge marker itself lies.
#
#   Godot --path godot --resolution 1920x1080 --script tools/shot_axe_side.gd -- --out D

const SHOT := Vector2i(1920, 1080)
const STRIKE_FRAME := 16
const HEAD_R := 0.14


func _initialize() -> void:
	var out := ProjectSettings.globalize_path("user://axeside")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out)
	var vp := SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = false
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60:
		await process_frame
	var k = scene.knight
	k.set_physics_process(false)
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var g := CliffWorld.ground_at(space, Vector2(2996.0, 1337.0), scene.right, scene.up, scene.fwd)
	k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.02
	k.facing = "S"
	k._drive()
	k.set_gear_stack(4)
	for i in 8:
		await physics_frame
		await process_frame

	# the rule, now that it has been reversed -- printed where it is being relied on
	var wrow := {}
	for clip in ["idle", "walk", "run", "attack"]:
		k._clip = ""
		k.play(clip)
		await physics_frame
		wrow[clip] = snappedf(float(k._tree.get("parameters/blend/blend_amount")), 0.001)
	print("layer weight at stack 4: %s" % JSON.stringify(wrow))

	var skel: Skeleton3D = k._skel
	var anim: AnimationPlayer = k._anim
	var edge: Node3D = ((k.gear["_pieces"] as Dictionary)["_markers_axe"] as Dictionary)["axe_edge"]
	var axe_mi: MeshInstance3D = (k.gear["_pieces"]["axe"] as Array)[0]
	var hand := skel.find_bone("RightHand")

	# POSE BY seek(), NOT BY STEPPING THE TREE. Stepping `for i in fr: await physics_frame`
	# after play() starts the clip wherever the tree happened to be, so "frame 16" was a
	# different pose on two consecutive runs and the leading point moved 0.095 m between
	# them -- once to mid-head, once onto the poll exactly. A verdict that changes per run
	# is not a verdict. seek() on the AnimationPlayer is exact and repeatable.
	#
	# The tree is off for this, so the left arm is not carrying here. That is the shield
	# arm; the axe is in the right hand and the question is only about the axe.
	var tree: AnimationTree = k._tree
	tree.active = false
	anim.active = true
	anim.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	anim.play("attack")
	var aa := anim.get_animation("attack")
	var an := int(round(aa.length * 24.0))
	var pos := []
	for fr in [STRIKE_FRAME - 1, STRIKE_FRAME]:
		anim.seek(aa.length * float(fr) / float(an), true, true)
		await process_frame
		pos.append(edge.global_position)
	var E: Vector3 = pos[1]
	var vel: Vector3 = pos[1] - pos[0]
	var dirv: Vector3 = vel.normalized() if vel.length() > 1e-9 else Vector3.FORWARD
	var H: Vector3 = skel.global_transform * skel.get_bone_global_pose(hand).origin

	var pts := _axe_points(axe_mi, skel)
	# the butt: the axe vertex furthest from the edge marker
	var butt: Vector3 = pts[0]
	for p in pts:
		if (p - E).length() > (butt - E).length():
			butt = p
	# the head cluster and its centroid
	var head := []
	var cen := Vector3.ZERO
	for p in pts:
		if (p - E).length() <= HEAD_R:
			head.append(p)
			cen += p
	cen /= maxf(float(head.size()), 1.0)
	var axis: Vector3 = (cen - butt).normalized()
	# across the haft, in the direction the EDGE lies
	var side: Vector3 = (E - butt) - axis * ((E - butt).dot(axis))
	var blade_dir: Vector3 = side.normalized()

	var lead: Vector3 = head[0]
	var lead_d := -1e9
	for p in head:
		var d: float = (p - H).dot(dirv)
		if d > lead_d:
			lead_d = d
			lead = p
	var poll: Vector3 = head[0]
	var poll_d := 1e9
	for p in head:
		var d: float = (p - butt).dot(blade_dir)
		if d < poll_d:
			poll_d = d
			poll = p

	var e_side: float = (E - butt).dot(blade_dir)
	var l_side: float = (lead - butt).dot(blade_dir)
	var p_side: float = (poll - butt).dot(blade_dir)
	var verdict := ""
	if l_side > 0.5 * e_side:
		verdict = "BLADE SIDE LEADS; the leading point is the beard toe"
	elif l_side < 0.2 * e_side:
		verdict = "THE POLL LEADS -- the head is on backwards"
	else:
		verdict = "the leading point is near the haft axis, on neither side clearly"
	print("")
	print("across the haft axis, measured from the butt, positive = the edge side:")
	print("   axe_edge marker  %+.4f m   (%.3f m from the hand)" % [e_side, (E - H).length()])
	print("   leading point    %+.4f m   (%.3f m from the hand, %.3f m from the marker)" %
		[l_side, (lead - H).length(), (lead - E).length()])
	print("   poll             %+.4f m   (%.3f m from the marker)" % [p_side, (poll - E).length()])
	print("   VERDICT: %s" % verdict)

	print("   butt is %.3f m from the head centroid (a haft, if that is about 0.8)" %
		(cen - butt).length())

	# --- the picture, perpendicular to the swing plane -----------------------
	#
	# THE AXE ALONE. The first version put the camera 2 m along the plane normal with every
	# layer visible, and at that distance his own shoulder is between the lens and the head:
	# the still came back as three coloured dots floating in front of a mantle, with no axe
	# in it at all. The question is about the axe, so the axe is what is rendered -- on its
	# own visual layer, over a transparent background, at two framings.
	var LAYER := 1 << 10
	axe_mi.layers = LAYER
	var N: Vector3 = axis.cross(dirv).normalized()
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.near = 0.01
	cam.far = 50.0
	cam.cull_mask = LAYER
	vp.add_child(cam)
	cam.current = true
	vp.transparent_bg = true
	for m in [[E, Color(0.15, 1.0, 0.25)], [lead, Color(1.0, 0.1, 0.9)], [poll, Color(0.1, 0.9, 1.0)]]:
		var s := MeshInstance3D.new()
		var sp := SphereMesh.new()
		sp.radius = 0.009
		sp.height = 0.018
		s.mesh = sp
		# DRAWN THROUGH THE AXE. Depth-tested, a marker on the far side of the blade is
		# hidden by it -- the first still showed only the poll, which is exactly the one
		# point whose position was not in question.
		var sh := Shader.new()
		sh.code = "shader_type spatial;\nrender_mode unshaded, depth_test_disabled, depth_draw_never, cull_disabled, shadows_disabled;\nuniform vec4 c : source_color;\nvoid fragment() { ALBEDO = c.rgb; }\n"
		var mm := ShaderMaterial.new()
		mm.shader = sh
		mm.set_shader_parameter("c", m[1])
		s.material_override = mm
		s.layers = LAYER
		scene.add_child(s)
		s.global_position = m[0]
	# close on the head, then the whole axe, so the haft-to-head relation is visible too
	for shot in [["head", cen, 0.32], ["whole", (H + cen) * 0.5, 0.75]]:
		cam.size = float(shot[2])
		cam.look_at_from_position((shot[1] as Vector3) + N * 2.0, shot[1] as Vector3, axis)
		for i in 6:
			await process_frame
		vp.get_texture().get_image().save_png("%s/axe_side_%s.png" % [out, String(shot[0])])
	var f := FileAccess.open(out + "/axe_side.json", FileAccess.WRITE)
	f.store_string(JSON.stringify({
		"strike_frame": STRIKE_FRAME,
		"layer_weight_at_stack_4": wrow,
		"across_haft_from_butt_m": {"axe_edge": snappedf(e_side, 0.0001),
			"leading_point": snappedf(l_side, 0.0001), "poll": snappedf(p_side, 0.0001)},
		"leading_point_dist_from_marker_m": snappedf((lead - E).length(), 0.0001),
		"leading_point_dist_from_hand_m": snappedf((lead - H).length(), 0.0001),
		"marker_dist_from_hand_m": snappedf((E - H).length(), 0.0001),
		"verdict": verdict,
		"legend": "green = axe_edge, magenta = the leading point, cyan = the poll"}, " "))
	f.close()
	print("[axeside] -> ", out)
	quit(0)


func _axe_points(mi: MeshInstance3D, skel: Skeleton3D) -> Array:
	var o := []
	var ar := mi.mesh.surface_get_arrays(0)
	var v: PackedVector3Array = ar[Mesh.ARRAY_VERTEX]
	var bo: PackedInt32Array = ar[Mesh.ARRAY_BONES]
	var we: PackedFloat32Array = ar[Mesh.ARRAY_WEIGHTS]
	var sk := mi.skin
	var st: int = maxi(1, v.size() / 3000)
	for i in range(0, v.size(), st):
		var acc := Vector3.ZERO
		var ws := 0.0
		for j in 4:
			var w: float = we[i * 4 + j]
			if w <= 0.0:
				continue
			var bi: int = bo[i * 4 + j]
			var b: int = sk.get_bind_bone(bi)
			if b < 0:
				b = skel.find_bone(sk.get_bind_name(bi))
			if b < 0:
				continue
			acc += (skel.get_bone_global_pose(b) * sk.get_bind_pose(bi) * v[i]) * w
			ws += w
		if ws > 0.0:
			o.append(skel.global_transform * (acc / ws))
	return o
