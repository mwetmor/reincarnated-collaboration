extends SceneTree
# C-9 D2 re-export: the shield against the torso WITH the arm layer on, by the same capsule
# instrument used before it, so the two numbers mean the same thing and can be subtracted.
const SPOT := Vector2(2996.0, 1337.0)
func _initialize():
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60: await process_frame
	var k = scene.knight
	k.set_physics_process(false)
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var g := CliffWorld.ground_at(space, SPOT, scene.right, scene.up, scene.fwd)
	k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.02
	k.facing = "S"; k._drive(); k.set_gear_stack(4)
	for i in 8: await physics_frame
	var skel: Skeleton3D = k._skel
	var tree: AnimationTree = k._tree
	var shield: MeshInstance3D = (k.gear["_pieces"]["shield"] as Array)[0]
	var hips := skel.find_bone("Hips")
	var neck := skel.find_bone("neck")
	var radius: float = 0.20 * float(k._figure_scale)
	var out := {}
	print("capsule radius %.3f m about the spine, same instrument as before the re-export" % radius)
	print("  %-8s %-6s %9s %14s %9s" % ["clip", "layer", "verts_in", "worst_depth_m", "worst_fr"])
	for clip in ["idle", "walk", "run", "attack"]:
		for w in [0.0, 1.0]:
			k._clip = ""; k.play(clip)
			tree.set("parameters/blend/blend_amount", w)
			var a: Animation = k._anim.get_animation(clip)
			var n := int(round(a.length * 24.0))
			var worst := 0; var deep := 0.0; var wf := 0; var sampled := 0
			for i in n:
				await physics_frame
				tree.set("parameters/blend/blend_amount", w)
				var A: Vector3 = skel.global_transform * skel.get_bone_global_pose(hips).origin
				var B: Vector3 = skel.global_transform * skel.get_bone_global_pose(neck).origin
				var ab := B - A
				var l2: float = maxf(ab.length_squared(), 1e-9)
				var pts: Array = _pts(shield, skel)
				sampled = pts.size()
				var inside := 0; var dd := 0.0
				for p in pts:
					var tp: float = clampf((p - A).dot(ab) / l2, 0.0, 1.0)
					var d: float = radius - (p - (A + ab * tp)).length()
					if d > 0.0:
						inside += 1; dd = maxf(dd, d)
				if inside > worst:
					worst = inside; deep = dd; wf = i
			print("  %-8s %-6s %9d %14.4f %9d   (of %d sampled)" %
				[clip, "off" if w == 0.0 else "ON", worst, deep, wf, sampled])
			out["%s_%s" % [clip, "off" if w == 0.0 else "on"]] = \
				{"verts_inside": worst, "worst_depth_m": snappedf(deep, 0.0001),
				 "worst_frame": wf, "sampled": sampled}
	var f := FileAccess.open(ProjectSettings.globalize_path("user://shield2.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " ")); f.close()
	quit(0)

func _pts(mi: MeshInstance3D, skel: Skeleton3D) -> Array:
	var o := []
	var ar := mi.mesh.surface_get_arrays(0)
	var v: PackedVector3Array = ar[Mesh.ARRAY_VERTEX]
	var bo: PackedInt32Array = ar[Mesh.ARRAY_BONES]
	var we: PackedFloat32Array = ar[Mesh.ARRAY_WEIGHTS]
	var sk := mi.skin
	var st: int = maxi(1, v.size() / 1864)
	for i in range(0, v.size(), st):
		var acc := Vector3.ZERO; var ws := 0.0
		for j in 4:
			var w: float = we[i * 4 + j]
			if w <= 0.0: continue
			var bi: int = bo[i * 4 + j]
			var b: int = sk.get_bind_bone(bi)
			if b < 0: b = skel.find_bone(sk.get_bind_name(bi))
			if b < 0: continue
			acc += (skel.get_bone_global_pose(b) * sk.get_bind_pose(bi) * v[i]) * w
			ws += w
		if ws > 0.0: o.append(skel.global_transform * (acc / ws))
	return o
