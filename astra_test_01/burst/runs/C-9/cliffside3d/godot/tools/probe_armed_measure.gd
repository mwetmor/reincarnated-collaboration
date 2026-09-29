extends SceneTree
# The four measures the brief asks for, on the armed set.
const DT := 1.0 / 24.0
const SPOT := Vector2(2285.62, 2407.32)
const PPM := 100.617553710938
var RAD := 0.20
var rep := {}
func _initialize():
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60: await process_frame
	Engine.physics_ticks_per_second = 24
	var k = scene.knight
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	var skel: Skeleton3D = k._skel
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var g := CliffWorld.ground_at(space, SPOT, scene.right, scene.up, scene.fwd)
	k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.05
	k.velocity = Vector3.ZERO
	print("armed=%s  walk %.1f px/s  run %.1f px/s  strafe %.1f px/s" %
		[k.armed(), k.walk_px_s(), k.run_px_s(), k.strafe_px_s()])

	# ---- 1. THE SHIELD AGAINST THE TORSO, with the guard up -----------------------
	# A SPINE CAPSULE THAT TURNS WITH HIM, not a world-axis box: his torso is not axis
	# aligned and a box around it counts his own arm.
	var shield: MeshInstance3D = _find_piece(k, "shield")
	print("")
	print("[1] SHIELD vs TORSO, armed, guard up  (export's own guard figure: 12 of 1829)")
	if shield == null:
		print("    shield mesh not found")
	else:
		for leg in [["idle", Vector2.ZERO, false], ["walk", Vector2(1, 0), false],
					["run", Vector2(1, 0), true],
					["idle NO-GUARD (control)", Vector2.ZERO, false]]:
			if String(leg[0]).begins_with("idle NO"):
				k._tree.set("parameters/blend/blend_amount", 0.0)
			for i in 26:
				k.drive_dir(leg[1], bool(leg[2]), DT)
				await physics_frame
			var worst := 0
			var deep := 0.0
			var sampled := 0
			for f in 12:
				k.drive_dir(leg[1], bool(leg[2]), DT)
				await physics_frame
				var r := _inside(skel, shield)
				sampled = int(r[1])
				if int(r[0]) > worst:
					worst = int(r[0])
					deep = float(r[2])
			print("    %-24s worst %d of %d sampled inside the torso capsule, deepest %.4f m"
				% [String(leg[0]), worst, sampled, deep])
			rep["shield_" + String(leg[0])] = {"inside": worst, "sampled": sampled,
				"deepest_m": snappedf(deep, 0.0001)}

	# ---- 2. THE AXE EDGE, on both attacks ------------------------------------------
	# IS THE INSTRUMENT ABLE TO SEE? A zero from a test that cannot see is not a zero. Sweep
	# the capsule radius: if the count responds, the geometry is real and "0 at 0.20 m" is a
	# result. Also check the posed shield is where his left hand is, which is what proves
	# the one-bone skinning above is being applied at all.
	if shield != null:
		var lh: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone("LeftHand")).origin
		var arr2 := shield.mesh.surface_get_arrays(0)
		var vv: PackedVector3Array = arr2[Mesh.ARRAY_VERTEX]
		var xf2 := _skin(skel, shield, "LeftHand")
		var c := Vector3.ZERO
		var cn := 0
		for i in range(0, vv.size(), maxi(1, vv.size() / 500)):
			c += xf2 * vv[i]; cn += 1
		c /= float(maxi(cn, 1))
		print("")
		print("[1b] INSTRUMENT CHECK")
		print("    posed shield centroid %s, his LeftHand %s, apart %.3f m  (a shield on his hand)"
			% [str(c.snappedf(0.01)), str(lh.snappedf(0.01)), (c - lh).length()])
		for r in [0.20, 0.30, 0.40, 0.55]:
			RAD = r
			var rr := _inside(skel, shield)
			print("    capsule radius %.2f m -> %4d of %d inside" % [r, int(rr[0]), int(rr[1])])
		RAD = 0.20
	print("")
	print("[2] AXE EDGE LEADING  (does the edge arrive ahead of the haft?)")
	for which in [["slash", "attack"], ["chop", "chop"]]:
		var clip := String(k._roles.get(String(which[1]), ""))
		if clip == "":
			continue
		var r := await _edge(k, skel, clip)
		print("    %-5s '%s': edge leads on %d of %d sampled frames, best margin %.4f m at phase %.2f"
			% [String(which[0]), clip, int(r[0]), int(r[1]), float(r[2]), float(r[3])])
		rep["edge_" + String(which[0])] = {"clip": clip, "leads": int(r[0]), "frames": int(r[1]),
			"best_margin_m": snappedf(float(r[2]), 0.0001), "at_phase": snappedf(float(r[3]), 0.01)}
	var f := FileAccess.open(ProjectSettings.globalize_path("user://armed.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(rep, " "))
	f.close()
	quit(0)

func _find_piece(k, want: String) -> MeshInstance3D:
	# gear is {"_pieces": {name: [MeshInstance3D]}, "_report": ..., "layer_order": ...}.
	# Reading k.gear[want] directly finds nothing and returns a clean zero, which is how
	# the first run of this reported "0 of 2439 inside" for an instrument that was not
	# looking at a shield at all.
	var pieces: Dictionary = k.gear.get("_pieces", {})
	var v = pieces.get(want, null)
	if v is Array and v.size() > 0 and v[0] is MeshInstance3D:
		return v[0]
	return null

func _skin(skel: Skeleton3D, m: MeshInstance3D, want: String) -> Transform3D:
	"""The one-bone skinning matrix, taken from the mesh's OWN Skin resource.

	The shield is a SKINNED mesh bound 100% to LeftHand (export manifest: zero vertices with
	more than one group, minimum weight 1.0000), and a skinned mesh's global_transform is
	the SKELETON's -- its vertices sit in bind space and do not follow the animation, so
	they have to be posed by hand for any test to move with him.

	THE BIND MATRIX IS THE SKIN'S, NOT THE BONE'S REST. Using get_bone_global_rest() put the
	shield 1.168 m from his hand, at ankle height, and the penetration count then did not
	respond to ANY capsule radius from 0.20 m to 0.55 m -- a test that cannot see returning
	a clean zero. And the bind is found by NAME: glTF skins bind by name, so get_bind_bone()
	returns -1 here and find_bone(get_bind_name(i)) is the only thing that resolves."""
	var skin := m.skin
	if skin == null:
		return skel.global_transform
	for i in skin.get_bind_count():
		var bn := String(skin.get_bind_name(i))
		var b := skel.find_bone(bn) if bn != "" else skin.get_bind_bone(i)
		if b >= 0 and skel.get_bone_name(b) == want:
			return skel.global_transform * (skel.get_bone_global_pose(b) * skin.get_bind_pose(i))
	return skel.global_transform


func _inside(skel: Skeleton3D, m: MeshInstance3D) -> Array:
	# the spine as a capsule, in world space, turning with him
	var a: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone("Hips")).origin
	var b: Vector3 = skel.global_transform * skel.get_bone_global_pose(skel.find_bone("Spine02")).origin
	if skel.find_bone("Spine02") < 0:
		b = skel.global_transform * skel.get_bone_global_pose(skel.find_bone("Spine")).origin
	var rad := RAD
	var mesh := m.mesh
	if mesh == null: return [0, 0, 0.0]
	var arr := mesh.surface_get_arrays(0)
	var verts: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
	var xf := _skin(skel, m, "LeftHand")
	var n := 0
	var deep := 0.0
	var step: int = maxi(1, verts.size() / 1829)
	var sampled := 0
	for i in range(0, verts.size(), step):
		var w: Vector3 = xf * verts[i]
		sampled += 1
		var ab := b - a
		var tt: float = clampf((w - a).dot(ab) / maxf(ab.length_squared(), 1e-9), 0.0, 1.0)
		var d: float = (w - (a + ab * tt)).length()
		if d < rad:
			n += 1
			deep = maxf(deep, rad - d)
	return [n, sampled, deep]

func _edge(k, skel: Skeleton3D, clip: String) -> Array:
	# THE REAL MARKER, not a guessed transform. gear.gd recreates axe.glb's `axe_edge`
	# Node3D on the body's own skeleton under a RightHand BoneAttachment3D, so its
	# global_position IS the edge and nothing has to be reconstructed from the manifest.
	#
	# DETERMINISTIC: AnimationPlayer.seek, not stepping the tree. Stepping the tree made the
	# strike pose differ between runs and flipped this verdict once already.
	var ap: AnimationPlayer = k._anim
	var tree: AnimationTree = k._tree
	var mk: Node3D = null
	var pieces: Dictionary = k.gear.get("_pieces", {})
	if pieces.has("_markers_axe"):
		mk = (pieces["_markers_axe"] as Dictionary).get("axe_edge", null)
	if mk == null:
		print("    *** axe_edge marker NOT FOUND -- this test can see nothing ***")
		return [-1, 0, 0.0, 0.0]
	var was: bool = tree.active
	tree.active = false
	ap.active = true
	var a := ap.get_animation(clip)
	var n := int(round(a.length * 24.0))
	var hand := skel.find_bone("RightHand")
	ap.play(clip)
	var pos := []
	var hands := []
	for i2 in n + 1:
		ap.seek(a.length * float(i2) / float(n), true, true)
		await process_frame
		pos.append(mk.global_position)
		hands.append(skel.global_transform * skel.get_bone_global_pose(hand).origin)
	tree.active = was
	ap.active = not was
	# the SWING is where the edge is actually moving; a verdict taken over the whole clip
	# is mostly a verdict about him standing still holding an axe.
	var spd := []
	var mx := 0.0
	for i3 in range(1, pos.size()):
		var v: Vector3 = pos[i3] - pos[i3 - 1]
		spd.append(v.length())
		mx = maxf(mx, v.length())
	var leads := 0
	var counted := 0
	var best := -1.0
	var at := 0.0
	for i4 in range(1, pos.size()):
		if spd[i4 - 1] < mx * 0.2:
			continue
		counted += 1
		var v: Vector3 = pos[i4] - pos[i4 - 1]
		var arm: Vector3 = pos[i4] - hands[i4]
		if arm.length() < 1e-5 or v.length() < 1e-5:
			continue
		var lead: float = arm.normalized().dot(v.normalized())
		if lead > 0.0:
			leads += 1
		if lead > best:
			best = lead
			at = float(i4) / float(n)
	return [leads, counted, best, at]
