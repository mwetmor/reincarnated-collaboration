extends SceneTree
# C-9 D2 gate G3: the three measures on the full kit, in the scene, at the play camera.
#
#   1  POKE-THROUGH, worst frame of each clip. A pixel is poke-through when, INSIDE a
#      garment's own silhouette, the full render differs from the garment-only render --
#      that is the body winning the depth test somewhere a garment covers. Three renders
#      settle it and one of them is free: E (nobody there) is fixed per camera.
#          garment mask = G != E          poke = (F != G) AND (G != E)
#      Scanned at 320x180 over every frame, then the worst frame re-counted at 1920x1080,
#      because a poke of forty pixels does not survive a six-fold downscale and a report
#      that says "none" because it could not see any is the failure mode this run keeps
#      finding.
#
#   2  THE AXE EDGE LEADING AT THE STRIKE. No marker names the edge, so the question is
#      put as one the geometry can answer: at the strike, which end of the axe is FURTHEST
#      FORWARD along the swing? Take the axe's own vertices in world space, take the swing
#      velocity of the head between neighbouring frames, and measure how far from the hand
#      the leading vertex sits. Leading vertex at the head end = the edge leads; leading
#      vertex at the butt = he is hitting with the haft.
#
#   3  THE SHIELD NOT CLIPPING THE TORSO. The same poke instrument, restricted to the
#      shield: torso pixels inside the shield's silhouette are the torso coming through it.
#
#   Godot --path godot --resolution 1920x1080 --script tools/probe_kit.gd -- [--out D]

const SHOT := Vector2i(1920, 1080)
const SCAN := Vector2i(320, 180)
const PPM := 100.617553710938
const SPOT := Vector2(2996.0, 1337.0)        # the flat by the post, where the attack lands
const AIM := Vector2(2996.0, 1290.0)
const ZOOM := 3.0
const STRIKE_FRAME := 16

var out_dir := ""
var scene
var vp: SubViewport
var cam: Camera3D
var lines: Array[String] = []


func say(s: String) -> void:
	print(s)
	lines.append(s)


func _initialize() -> void:
	out_dir = ProjectSettings.globalize_path("user://kit")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = false
	vp.msaa_3d = Viewport.MSAA_DISABLED
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 50:
		await process_frame
	cam = Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.near = scene.cam.near
	cam.far = scene.cam.far
	cam.cull_mask = scene.cam.cull_mask
	vp.add_child(cam)
	cam.current = true

	var k = scene.knight
	k.set_physics_process(false)
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var g := CliffWorld.ground_at(space, SPOT, scene.right, scene.up, scene.fwd)
	k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.02
	k.facing = "S"
	k._drive()
	k.set_gear_stack(4)                       # the full kit
	scene.look_at_canvas(AIM, 0.0, ZOOM)
	_mirror()
	for i in 10:
		await physics_frame
		await process_frame

	var anim: AnimationPlayer = k._anim
	anim.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var report := {}
	report["poke_through"] = await _poke(k, anim)
	report["axe_at_strike"] = await _axe(k, anim)
	report["shield_vs_torso"] = await _shield(k, anim)

	var f := FileAccess.open(out_dir + "/kit.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	var h := FileAccess.open(out_dir + "/kit.txt", FileAccess.WRITE)
	h.store_string("\n".join(lines) + "\n")
	h.close()
	print("[kit] -> ", out_dir)
	quit(0)


# --- which meshes are which -------------------------------------------------
func _body_meshes(k) -> Array:
	return [k._mesh, k._mesh.get_meta("ink", null)] if k._mesh.has_meta("ink") else [k._mesh]


func _gear_meshes(k, only := "") -> Array:
	var out := []
	for name in (k.gear["_pieces"] as Dictionary):
		if only != "" and name != only:
			continue
		for mi in (k.gear["_pieces"][name] as Array):
			out.append(mi)
			var ink = (mi as MeshInstance3D).get_meta("ink", null)
			if ink != null:
				out.append(ink)
	return out


func _show(arr: Array, on: bool) -> void:
	for m in arr:
		if m != null:
			(m as MeshInstance3D).visible = on


# --- 1. poke-through --------------------------------------------------------
func _poke(k, anim: AnimationPlayer) -> Dictionary:
	"""Is the BODY outside the SHELL that is supposed to cover it?

	The first version of this counted, in screen space, body pixels drawn in front of a
	garment inside its silhouette -- and reported 4-7%, which sounded like a lot until the
	worst frames were saved and looked at. They are clean. What it had counted was his own
	forearm and his shield crossing his chest, which is a body part in front of a garment
	and is not poke-through at all. A screen test cannot tell "the mail pierces the shoulder"
	from "his arm is in front of the mail", because both are body pixels over garment pixels.

	Poke-through is a statement about SURFACES: the body is outside the shell. So the torso
	is unrolled about its own spine -- height along the spine, angle around it -- and in each
	cell the FURTHEST body vertex is compared with the NEAREST garment vertex. Body beyond
	garment in a cell is the body poking out of it, and the excess is in millimetres, which
	is the unit the export was authored in (the byrnie a 5 mm shell, the mantle 8 mm).
	O(vertices) per frame, so every frame of every clip is checked rather than a sample."""
	say("")
	say("[1] POKE-THROUGH -- geometric, body-vertex against garment shell")
	say("    %-8s %-7s %7s %9s %12s %8s" %
		["garment", "clip", "frames", "cells_out", "worst_mm", "frame"])
	var skel: Skeleton3D = k._skel
	var hips := skel.find_bone("Hips")
	var neck := skel.find_bone("neck")
	var body_mi: MeshInstance3D = k._mesh
	var out := {}
	for garment in ["byrnie", "mantle"]:
		var gm: MeshInstance3D = (k.gear["_pieces"][garment] as Array)[0]
		var per := {}
		for clip in ["idle", "walk", "run", "attack"]:
			anim.play(clip)
			var a := anim.get_animation(clip)
			var n := int(round(a.length * 24.0))
			var worst_cells := 0
			var worst_mm := 0.0
			var worst_f := 0
			for i in range(0, n + 1):
				anim.seek(a.length * float(i) / float(n), true, true)
				await process_frame
				var axis_a: Vector3 = skel.global_transform * skel.get_bone_global_pose(hips).origin
				var axis_b: Vector3 = skel.global_transform * skel.get_bone_global_pose(neck).origin
				var basis: Basis = (skel.global_transform * skel.get_bone_global_pose(hips)).basis.orthonormalized()
				var bod := _cells(_world_points(body_mi, TORSO_BONES), axis_a, axis_b, basis, true)
				var gar := _cells(_world_points(gm), axis_a, axis_b, basis, false)
				var cells := 0
				var mm := 0.0
				for key in gar:
					if not bod.has(key):
						continue
					var excess: float = float(bod[key]) - float(gar[key])
					if excess > 0.0:
						cells += 1
						mm = maxf(mm, excess * 1000.0)
				if mm > worst_mm:
					worst_mm = mm
					worst_cells = cells
					worst_f = i
			say("    %-8s %-7s %7d %9d %12.2f %8d" %
				[garment, clip, n, worst_cells, worst_mm, worst_f])
			per[clip] = {"frames": n, "worst_frame": worst_f,
						 "cells_with_body_outside": worst_cells,
						 "worst_excess_mm": snappedf(worst_mm, 0.01)}
		out[garment] = per
	return out


const CELLS_H := 10
const CELLS_A := 12
const TORSO_BONES := ["Hips", "Spine", "Spine01", "Spine02", "neck",
					  "LeftShoulder", "RightShoulder"]


func _cells(pts: Array, a: Vector3, b: Vector3, basis: Basis, want_max: bool) -> Dictionary:
	"""Unroll points about the spine: cell (height band, angle band) -> radius.

	`want_max` takes the furthest radius in each cell (the body, at its most outward) and
	`false` the nearest (the garment, at its most inward). Comparing those two is the
	tightest honest statement the sampling supports."""
	var out := {}
	var ab := b - a
	var len2: float = maxf(ab.length_squared(), 1e-9)
	for p in pts:
		var tpar: float = clampf((p - a).dot(ab) / len2, 0.0, 1.0)
		if tpar <= 0.02 or tpar >= 0.98:
			continue                       # ends of the spine: hips and head, not torso
		var r: Vector3 = p - (a + ab * tpar)
		var rad: float = r.length()
		var ang: float = atan2(r.dot(basis.z), r.dot(basis.x))
		var key: int = int(tpar * float(CELLS_H)) * 100 \
			+ int((ang + PI) / TAU * float(CELLS_A)) % CELLS_A
		if out.has(key):
			out[key] = maxf(float(out[key]), rad) if want_max else minf(float(out[key]), rad)
		else:
			out[key] = rad
	return out


# --- 2. the axe at the strike ----------------------------------------------
func _axe(k, anim: AnimationPlayer) -> Dictionary:
	say("")
	say("[2] THE AXE AT THE STRIKE (attack frame %d)" % STRIKE_FRAME)
	var axe: MeshInstance3D = (k.gear["_pieces"]["axe"] as Array)[0]
	var skel: Skeleton3D = k._skel
	var hand := skel.find_bone("RightHand")
	anim.play("attack")
	var a := anim.get_animation("attack")
	var n := int(round(a.length * 24.0))
	var rows := []
	var prev_head := Vector3.ZERO
	var head_idx := -1
	var res := {}
	for i in range(maxi(STRIKE_FRAME - 2, 0), mini(STRIKE_FRAME + 3, n + 1)):
		anim.seek(a.length * float(i) / float(n), true, true)
		await process_frame
		var pts: Array = _world_points(axe)
		var hpos: Vector3 = skel.global_transform * skel.get_bone_global_pose(hand).origin
		# the head is the far cluster from the hand
		# ONE vertex, held across frames. Recomputing "whichever vertex is furthest from
		# the hand" every frame and differencing gives the gap between two DIFFERENT
		# vertices, not a velocity: it reported 0.93 m per frame, which is 22 m/s of axe.
		# The sample set is index-stable, so the head vertex chosen once stays the same
		# point of steel all the way through the swing.
		if head_idx < 0:
			var best := -1.0
			for vi in pts.size():
				var d: float = (pts[vi] - hpos).length()
				if d > best:
					best = d
					head_idx = vi
		var far: Vector3 = pts[head_idx]
		var vel: Vector3 = (far - prev_head) if i > STRIKE_FRAME - 2 else Vector3.ZERO
		prev_head = far
		if i == STRIKE_FRAME and vel.length() > 1e-6:
			var dirv: Vector3 = vel.normalized()
			# HEAD AGAINST BUTT along the direction of travel. "Which vertex is furthest
			# forward" was the wrong question: on a swing about the hand the haft is nearly
			# perpendicular to the travel, so every point of it projects to about the same
			# place and the winner is noise. Whether the HEAD leads the BUTT is not noise.
			var butt: Vector3 = pts[0]
			for pv in pts:
				if (pv - hpos).length() < (butt - hpos).length():
					butt = pv
			var head_along: float = (far - hpos).dot(dirv)
			var butt_along: float = (butt - hpos).dot(dirv)
			var haft: Vector3 = (far - hpos).normalized()
			var ang: float = rad_to_deg(acos(clampf(haft.dot(dirv), -1.0, 1.0)))
			res = {
				"strike_frame": i,
				"tracked_head_vertex_speed_m_per_frame": snappedf(vel.length(), 0.0001),
				"head_reach_from_hand_m": snappedf((far - hpos).length(), 0.0001),
				"head_extent_along_travel_m": snappedf(head_along, 0.0001),
				"butt_extent_along_travel_m": snappedf(butt_along, 0.0001),
				"head_leads_butt_by_m": snappedf(head_along - butt_along, 0.0001),
				"haft_to_travel_deg": snappedf(ang, 0.1),
			}
			# WHICH SIDE OF THE HAFT THE BLADE IS ON. An axe head is asymmetric -- blade one
			# way, poll the other -- so the honest question at a strike where the haft is
			# 92.7 deg to the travel (a clean swing about the hand, not a thrust) is which
			# side of the haft line the head's mass extends toward. Forward = the edge
			# arrives first. This cannot name the sharp edge itself: nothing in the export
			# marks it, and a vertex group or an empty on the blade would make it exact.
			# THE HEAD, not the head and half the haft. 0.6 x reach put the cluster's
			# boundary 0.51 m from the hand on a 0.85 m axe, so "how far the head extends
			# forward and back of the haft" was measuring the haft. The head of an axe is a
			# hand's breadth of steel: take vertices within 0.12 m of the furthest point.
			var fwd_ext := 0.0
			var back_ext := 0.0
			var nhead := 0
			for pv in pts:
				if (pv - far).length() > 0.12:
					continue
				nhead += 1
				var along: float = (pv - far).dot(dirv)
				fwd_ext = maxf(fwd_ext, along)
				back_ext = minf(back_ext, along)
			res["head_cluster_vertices"] = nhead
			res["head_extends_forward_m"] = snappedf(fwd_ext, 0.0001)
			res["head_extends_back_m"] = snappedf(back_ext, 0.0001)
			res["verdict"] = ("the blade mass is FORWARD of the haft -- the edge arrives first"
				if fwd_ext > absf(back_ext) else
				"the blade mass is BEHIND the haft -- the poll arrives first")
			say("    head cluster (%d verts) extends %+.3f m forward and %+.3f m back of the haft"
				% [nhead, fwd_ext, back_ext])
			say("    tracked head vertex: %.4f m per frame, reach %.3f m from the hand" %
				[vel.length(), float(res["head_reach_from_hand_m"])])
			say("    along the travel: head %+.3f m, butt %+.3f m  ->  head leads by %+.3f m" %
				[head_along, butt_along, head_along - butt_along])
			say("    haft to travel %.1f deg (90 = a clean swing about the hand)" % ang)
			say("    %s" % String(res["verdict"]))
		rows.append({"frame": i, "head_dist_m": snappedf((far - hpos).length(), 0.0001),
					 "head_step_m": snappedf(vel.length(), 0.0001)})
	res["swept"] = rows
	return res


var sample_n := 6000
func _world_points(mi: MeshInstance3D, only_bones: Array = []) -> Array:
	"""The mesh's vertices in world space, at the pose it is in.

	Skinned, so the mesh arrays are BIND-space: each vertex goes through its bones. Taking
	the AABB instead would answer a question about a box, and a box has no edge."""
	var out := []
	var skel := mi.get_node(mi.skeleton) as Skeleton3D
	var arrays := mi.mesh.surface_get_arrays(0)
	var verts: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
	var bones: PackedInt32Array = arrays[Mesh.ARRAY_BONES]
	var weights: PackedFloat32Array = arrays[Mesh.ARRAY_WEIGHTS]
	var skin := mi.skin
	var stride := 4
	# DENSITY MATTERS HERE. The cell test compares the furthest body vertex in a cell with
	# the NEAREST garment vertex in the same cell, so a cell holding one stray hem vertex
	# reports a shell that is not there: at 400 samples of a 26,000-vertex byrnie it claimed
	# 216 mm of chest outside the mail over a render that is clean. 6000 fills the cells.
	var step: int = maxi(1, verts.size() / int(sample_n))
	for vi in range(0, verts.size(), step):
		var acc := Vector3.ZERO
		var wsum := 0.0
		if not only_bones.is_empty():
			# DOMINANT BONE FILTER. Without it "the body" includes his forearms, and a
			# forearm held across the chest sits at a torso height and a torso angle with a
			# radius far outside a mail shirt -- which is how this reported a metre of
			# poke-through over a render that is clean. A shirt can only be pierced by the
			# torso it is on.
			var best_w := -1.0
			var best_b := -1
			for j in stride:
				var w0: float = weights[vi * stride + j]
				if w0 > best_w:
					best_w = w0
					best_b = bones[vi * stride + j]
			var nm := ""
			if best_b >= 0:
				var rb: int = skin.get_bind_bone(best_b)
				if rb < 0:
					rb = skel.find_bone(skin.get_bind_name(best_b))
				if rb >= 0:
					nm = skel.get_bone_name(rb)
			if not only_bones.has(nm):
				continue
		for j in stride:
			var w: float = weights[vi * stride + j]
			if w <= 0.0:
				continue
			var bi: int = bones[vi * stride + j]
			# A glTF skin binds by NAME, not index: get_bind_bone returns -1 and
			# get_bone_global_pose(-1) errors out on every vertex. Resolve the name.
			var bind: Transform3D = skin.get_bind_pose(bi)
			var bone: int = skin.get_bind_bone(bi)
			if bone < 0:
				bone = skel.find_bone(skin.get_bind_name(bi))
			if bone < 0:
				continue
			var pose: Transform3D = skel.get_bone_global_pose(bone)
			acc += (pose * bind * verts[vi]) * w
			wsum += w
		if wsum > 0.0:
			out.append(skel.global_transform * (acc / wsum))
	return out


# --- 3. the shield against the torso ---------------------------------------
func _shield(k, anim: AnimationPlayer) -> Dictionary:
	say("")
	say("[3] THE SHIELD AGAINST THE TORSO")
	say("    GEOMETRIC, not screen-space. A screen test counts every body pixel drawn in")
	say("    front of the shield, and his own arm crossing it is most of them -- the first")
	say("    run of this reported 21-37% 'torso through the shield' and what it had found")
	say("    was a forearm doing exactly what a forearm does. Clipping is a question about")
	say("    volumes: are shield vertices INSIDE the torso? So the torso is boxed from its")
	say("    own spine bones and the shield's vertices are tested against that box.")
	var shield_mi: MeshInstance3D = (k.gear["_pieces"]["shield"] as Array)[0]
	var skel: Skeleton3D = k._skel
	var spine := []
	for b in ["Hips", "Spine", "Spine01", "Spine02", "neck"]:
		var i := skel.find_bone(b)
		if i >= 0:
			spine.append(i)
	var out := {}
	say("    torso = a capsule of radius %.3f m about the spine, turning with him" %
		(0.20 * float(k._figure_scale)))
	say("    %-8s %7s %10s %12s %10s" %
		["clip", "frames", "verts_in", "worst_depth_m", "worst_fr"])
	for clip in ["idle", "walk", "run", "attack"]:
		anim.play(clip)
		var a := anim.get_animation(clip)
		var n := int(round(a.length * 24.0))
		var worst_in := 0
		var worst_depth := 0.0
		var worst_f := 0
		var sampled := 0
		for i in range(0, n + 1):
			anim.seek(a.length * float(i) / float(n), true, true)
			await process_frame
			# A CAPSULE ABOUT THE SPINE, not a world-axis box. The body is yawed 47 deg or
			# more in this level, so an AABB around the spine plus padding is a box the
			# torso rattles around inside -- the first version of this counted 198 of 407
			# shield vertices "inside the torso" and what most of them were inside was the
			# corner of a box that is not a man. A capsule turns with him.
			var axis_a: Vector3 = skel.global_transform * skel.get_bone_global_pose(spine[0]).origin
			var axis_b: Vector3 = skel.global_transform * skel.get_bone_global_pose(spine[-1]).origin
			var radius: float = 0.20 * float(k._figure_scale)
			var ab: Vector3 = axis_b - axis_a
			var len2: float = maxf(ab.length_squared(), 1e-9)
			var pts: Array = _world_points(shield_mi)
			sampled = pts.size()
			var inside := 0
			var deepest := 0.0
			for p in pts:
				var tpar: float = clampf((p - axis_a).dot(ab) / len2, 0.0, 1.0)
				var d: float = radius - (p - (axis_a + ab * tpar)).length()
				if d > 0.0:
					inside += 1
					deepest = maxf(deepest, d)
			if inside > worst_in:
				worst_in = inside
				worst_depth = deepest
				worst_f = i
		anim.seek(a.length * float(worst_f) / float(n), true, true)
		await process_frame
		_mirror()
		for q in 3:
			await process_frame
		vp.get_texture().get_image().save_png("%s/shield_%s_f%02d.png" % [out_dir, clip, worst_f])
		say("    %-8s %7d %10d %12.4f %10d   (of %d sampled shield vertices)" %
			[clip, n, worst_in, worst_depth, worst_f, sampled])
		out[clip] = {"frames": n, "shield_vertices_sampled": sampled,
					 "worst_vertices_inside_torso_box": worst_in,
					 "worst_intrusion_depth_m": snappedf(worst_depth, 0.0001),
					 "worst_frame": worst_f}
	return out


func _ne(a: Color, b: Color) -> bool:
	return absf(a.r - b.r) + absf(a.g - b.g) + absf(a.b - b.b) > 0.02


func _mirror() -> void:
	cam.global_transform = scene.cam.global_transform
	cam.size = float(vp.size.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))


func _grab() -> Image:
	_mirror()
	for i in 3:
		await process_frame
	return vp.get_texture().get_image()
