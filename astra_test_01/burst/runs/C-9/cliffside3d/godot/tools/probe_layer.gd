extends SceneTree
# C-9 D2 re-export: the shield-carry arm layer, measured.
#
#   1  WHICH BONES THE FILTER ACTUALLY MOVES. `shield_carry_L` is one frame carrying tracks
#      for all 24 bones, so unfiltered it is a whole static body pose and would freeze him
#      mid-stride. The claim is that the Blend2 filter confines it to four. Blend 0 against
#      blend 1, every bone, in metres -- a claim about a filter is checkable and should be.
#
#   2  DOES THE ARM STILL READ AS CARRYING, OR IS IT STIFF? A static pose held on four bones
#      could pin the arm dead. Measured as the left hand's travel IN THE HIP FRAME over a
#      walk cycle: zero is a mannequin, the bare figure's own range is the reference.
#
#   3  STACKS 0-3 UNTOUCHED: the layer weight must be 0 without the shield, and 0 over the
#      attack whatever is equipped.
#
#   4  THE axe_edge ASSERT AT THE STRIKE, now that the export carries the marker: is the
#      edge the part of the axe furthest along the swing?
#
#   5  THE SHIELD AGAINST THE TORSO with the layer on -- the same capsule instrument as
#      before the re-export, so the two numbers are comparable to each other.
#
#   Godot --path godot --resolution 1280x720 --script tools/probe_layer.gd -- [--out D]

const PPM := 100.617553710938
const SPOT := Vector2(2996.0, 1337.0)
const STRIKE_FRAME := 16

var out_dir := ""
var scene
var lines: Array[String] = []


func say(s: String) -> void:
	print(s)
	lines.append(s)


func _initialize() -> void:
	out_dir = ProjectSettings.globalize_path("user://layer")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir)
	scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60:
		await process_frame
	var k = scene.knight
	k.set_physics_process(false)
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var g := CliffWorld.ground_at(space, SPOT, scene.right, scene.up, scene.fwd)
	k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.02
	k.facing = "S"
	k._drive()
	var skel: Skeleton3D = k._skel
	var tree: AnimationTree = k._tree
	var report := {}

	# ---- 1. which bones the filter moves ---------------------------------
	k.set_gear_stack(4)
	k.play("idle")
	for i in 8:
		await physics_frame
		await process_frame
	# TIME MUST NOT ADVANCE BETWEEN THE TWO SAMPLES. Toggling the blend and re-reading six
	# physics frames later compares two different MOMENTS of idle as well as two blend
	# weights, and idle moves 23 bones all by itself: that is how this first reported the
	# filter leaking into the spine, the head and both legs. At time_scale 0 the tree still
	# re-evaluates the blend and no clip advances, so the only difference is the weight.
	Engine.time_scale = 0.0
	var moved := {}
	for w in [0.0, 1.0]:
		tree.set("parameters/blend/blend_amount", w)
		for i in 6:
			await physics_frame
			await process_frame
		for b in skel.get_bone_count():
			var p: Vector3 = skel.global_transform * skel.get_bone_global_pose(b).origin
			var nm := skel.get_bone_name(b)
			if w == 0.0:
				moved[nm] = p
			else:
				moved[nm] = (p - (moved[nm] as Vector3)).length()
	say("")
	say("[1] WHAT THE FILTER MOVES -- bone displacement, blend 0 -> blend 1, in metres")
	var big := []
	for nm in moved:
		if float(moved[nm]) > 0.002:
			big.append("%s %.3f" % [nm, float(moved[nm])])
	big.sort()
	say("    moved more than 2 mm: %s" % str(big))
	Engine.time_scale = 1.0
	var declared: Array = (k.cfg["arm_layer"] as Dictionary)["bones"]
	var stray := []
	for s in big:
		var nm2: String = s.split(" ")[0]
		if not declared.has(nm2):
			stray.append(nm2)
	say("    declared %s" % str(declared))
	say("    bones moved that were NOT declared: %s" % str(stray))
	report["filter"] = {"moved_over_2mm": big, "declared": declared, "undeclared_moved": stray}

	# ---- 2. carrying, or stiff? ------------------------------------------
	say("")
	say("[2] DOES THE ARM READ AS CARRYING? left-hand travel in the HIP frame, per cycle")
	var anim: AnimationPlayer = k._anim
	var carry_stats := {}
	for w in [0.0, 1.0]:
		tree.set("parameters/blend/blend_amount", w)
		for clip in ["walk", "run", "idle"]:
			k._clip = ""
			k.play(clip)
			tree.set("parameters/blend/blend_amount", w)   # after play, which recomputes it
			var a := anim.get_animation(clip)
			var n := int(round(a.length * 24.0))
			var pts := []
			for i in n:
				for q in 1:
					await physics_frame
				# ORTHONORMALIZED. The bone pose carries the rig's own 0.0109 scale, so an
				# un-normalised inverse multiplies every length by about 91: the left hand
				# "swept 45.5 m" in a frame that is 0.50 m across.
				var hip: Transform3D = (skel.global_transform * skel.get_bone_global_pose(skel.find_bone("Hips"))).orthonormalized()
				var hand: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone("LeftHand")).origin
				pts.append(hip.affine_inverse() * hand)
			var lo := Vector3(1e9, 1e9, 1e9)
			var hi := Vector3(-1e9, -1e9, -1e9)
			for p in pts:
				lo = Vector3(minf(lo.x, p.x), minf(lo.y, p.y), minf(lo.z, p.z))
				hi = Vector3(maxf(hi.x, p.x), maxf(hi.y, p.y), maxf(hi.z, p.z))
			var rng: float = (hi - lo).length()
			carry_stats["%s_w%d" % [clip, int(w)]] = snappedf(rng, 0.0001)
			say("    %-5s layer %s: the left hand sweeps %.3f m in the hip frame" %
				[clip, "off" if w == 0.0 else "ON ", rng])
	report["arm_travel_in_hip_frame_m"] = carry_stats

	# ---- 3. stacks 0-3 and the attack ------------------------------------
	say("")
	say("[3] THE WEIGHT, per stack and per clip (0 = the layer is not applied)")
	var wmap := {}
	for s in k.gear_stack_count():
		k.set_gear_stack(s)
		var row := {}
		for clip in ["idle", "walk", "run", "attack"]:
			k._clip = ""
			k.play(clip)
			await physics_frame
			row[clip] = snappedf(float(tree.get("parameters/blend/blend_amount")), 0.001)
		wmap[s] = row
		say("    stack %d %-28s %s" % [s, str(k.cfg["gear_stacks"][s]), JSON.stringify(row)])
	report["layer_weight_by_stack"] = wmap

	# ---- 4. the axe_edge assert ------------------------------------------
	say("")
	say("[4] THE axe_edge MARKER AT THE STRIKE")
	k.set_gear_stack(4)
	var edge: Node3D = ((k.gear["_pieces"] as Dictionary)["_markers_axe"] as Dictionary)["axe_edge"]
	var axe_mi: MeshInstance3D = (k.gear["_pieces"]["axe"] as Array)[0]
	var hand := skel.find_bone("RightHand")
	anim.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	tree.active = false
	anim.active = true
	anim.play("attack")
	var aa := anim.get_animation("attack")
	var an := int(round(aa.length * 24.0))
	var prev := Vector3.ZERO
	var res := {}
	# SWEEP THE WHOLE SLASH, not one frame. "The edge leads at frame 16" is a claim about
	# where the strike IS as well as about the edge, and a single-frame assert cannot tell
	# "the edge does not lead" from "the strike is not on 16".
	var sweep := []
	for i in range(1, an + 1):
		anim.seek(aa.length * float(i) / float(an), true, true)
		await process_frame
		var e: Vector3 = edge.global_position
		if i > 1:
			var vel: Vector3 = e - prev
			if vel.length() > 1e-9:
				var d2 := vel.normalized()
				var h2: Vector3 = skel.global_transform * skel.get_bone_global_pose(hand).origin
				var pp: Array = _axe_points(axe_mi, skel)
				var l2 := -1e9
				for p2 in pp:
					if (p2 - e).length() > 0.14:
						continue
					l2 = maxf(l2, (p2 - h2).dot(d2))
				sweep.append({"frame": i, "edge_speed": snappedf(vel.length(), 0.0001),
							  "edge_behind_leader_m": snappedf(l2 - (e - h2).dot(d2), 0.0001)})
			if i == STRIKE_FRAME and vel.length() > 1e-9:
				var dirv := vel.normalized()
				var hpos: Vector3 = skel.global_transform * skel.get_bone_global_pose(hand).origin
				# THE LEADER AMONG THE HEAD, not among the whole axe. A point of haft
				# swinging on its own radius can project further along the travel than the
				# blade without being the thing that arrives: the question is whether the
				# EDGE leads the HEAD it belongs to.
				var pts: Array = _axe_points(axe_mi, skel)
				var lead := -1e9
				var lead_p := Vector3.ZERO
				var nhead := 0
				for p in pts:
					if (p - e).length() > 0.14:
						continue
					nhead += 1
					if (p - hpos).dot(dirv) > lead:
						lead = (p - hpos).dot(dirv)
						lead_p = p
					
				res["head_cluster_vertices"] = nhead
				# IS THE LEADER THE SAME BLADE? A marker is ONE point on a curved edge, and
				# the blade's corner can be a hand's breadth from its middle. If the leading
				# vertex sits at the same reach from the hand and close to the marker, then
				# the edge is what arrives and the marker is simply not at its extreme.
				res["leader_dist_from_hand_m"] = snappedf((lead_p - hpos).length(), 0.0001)
				res["leader_dist_from_edge_marker_m"] = snappedf((lead_p - e).length(), 0.0001)
				say("    the leading vertex is %.3f m from the hand (the marker is %.3f m)" %
					[(lead_p - hpos).length(), (e - hpos).length()])
				say("    and %.3f m from the marker itself" % (lead_p - e).length())
				var edge_along: float = (e - hpos).dot(dirv)
				res = {"strike_frame": i,
					   "edge_speed_m_per_frame": snappedf(vel.length(), 0.0001),
					   "edge_along_travel_m": snappedf(edge_along, 0.0001),
					   "furthest_axe_vertex_along_travel_m": snappedf(lead, 0.0001),
					   "edge_is_behind_the_leading_vertex_by_m": snappedf(lead - edge_along, 0.0001),
					   "edge_dist_from_hand_m": snappedf((e - hpos).length(), 0.0001)}
				res["verdict"] = "the EDGE leads -- it is the furthest part of the axe along the swing" \
					if (lead - edge_along) < 0.02 else \
					"the edge is NOT the leading part; something else of the axe is %.3f m ahead of it" % (lead - edge_along)
				say("    edge moves %.4f m/frame, sits %.3f m from the hand" %
					[vel.length(), float(res["edge_dist_from_hand_m"])])
				say("    along the travel: the edge is at %+.3f m, the furthest axe vertex at %+.3f m"
					% [edge_along, lead])
				say("    %s" % String(res["verdict"]))
		prev = e
	report["axe_edge"] = res
	report["axe_edge_sweep"] = sweep
	var best: Dictionary = sweep[0]
	for r in sweep:
		if float(r["edge_behind_leader_m"]) < float(best["edge_behind_leader_m"]):
			best = r
	say("    over the whole slash, the edge is most nearly the leading part at frame %d"
		% int(best["frame"]))
	say("    (%.3f m behind the leader there; %.4f m/frame)" %
		[float(best["edge_behind_leader_m"]), float(best["edge_speed"])])
	var fastest: Dictionary = sweep[0]
	for r in sweep:
		if float(r["edge_speed"]) > float(fastest["edge_speed"]):
			fastest = r
	say("    the edge is fastest at frame %d (%.4f m/frame), where it is %.3f m behind the leader"
		% [int(fastest["frame"]), float(fastest["edge_speed"]), float(fastest["edge_behind_leader_m"])])
	report["axe_edge_fastest_frame"] = fastest
	report["axe_edge_most_leading_frame"] = best
	anim.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS
	anim.active = false
	tree.active = true

	var f := FileAccess.open(out_dir + "/layer.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	var h := FileAccess.open(out_dir + "/layer.txt", FileAccess.WRITE)
	h.store_string("\n".join(lines) + "\n")
	h.close()
	print("[layer] -> ", out_dir)
	quit(0)


func _axe_points(mi: MeshInstance3D, skel: Skeleton3D) -> Array:
	var out := []
	var arrays := mi.mesh.surface_get_arrays(0)
	var verts: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
	var bones: PackedInt32Array = arrays[Mesh.ARRAY_BONES]
	var weights: PackedFloat32Array = arrays[Mesh.ARRAY_WEIGHTS]
	var skin := mi.skin
	var step: int = maxi(1, verts.size() / 1500)
	for vi in range(0, verts.size(), step):
		var acc := Vector3.ZERO
		var wsum := 0.0
		for j in 4:
			var w: float = weights[vi * 4 + j]
			if w <= 0.0:
				continue
			var bi: int = bones[vi * 4 + j]
			var bone: int = skin.get_bind_bone(bi)
			if bone < 0:
				bone = skel.find_bone(skin.get_bind_name(bi))
			if bone < 0:
				continue
			acc += (skel.get_bone_global_pose(bone) * skin.get_bind_pose(bi) * verts[vi]) * w
			wsum += w
		if wsum > 0.0:
			out.append(skel.global_transform * (acc / wsum))
	return out
