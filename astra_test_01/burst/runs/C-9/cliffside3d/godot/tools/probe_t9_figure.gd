extends SceneTree
# C-9 T9: WHICH NUMBER IS THE MAN?
#
# T9-0 reports 123.3 canvas px at figure scale 1.0. probe_t9_scale.gd, using what looks
# like the same code, got 104.3. Both ran clean. At most one is right, and every prop size
# in T9-1a is quoted against it.
#
# The suspect is the idiom both scripts share:
#     for n in k.find_children("*", "Skeleton3D", true, false): skel = n
# which keeps the LAST Skeleton3D in the tree, not the body's. knight.gd holds the body's
# as `_skel` and builds the gear onto it; if any gear piece brings its own Skeleton3D, the
# last one found is a piece of armour and `find_bone("head_end")` on it returns -1 --
# whereupon get_bone_global_pose(-1) still returns something, and the measurement is of
# nothing in particular, cleanly.
#
# So: enumerate EVERY Skeleton3D, say which of them even has a head_end, and measure each.
# Then measure the thing the question is actually about -- the height of his SILHOUETTE,
# from the union of his visible meshes' AABBs -- which needs no bone to be named correctly.
#
#   Godot --path godot --resolution 1920x1080 --script tools/probe_t9_figure.gd

const PPM := 100.617553710938
const PITCH_COS := 0.602462407085
const STAND := Vector2(3380.0, 1120.0)

var scene
var report := {}


func _initialize() -> void:
	var vp := SubViewport.new()
	vp.size = Vector2i(1920, 1080)
	vp.own_world_3d = false
	root.add_child(vp)
	scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60:
		await process_frame
	var k = scene.knight
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var g := CliffWorld.ground_at(space, STAND, scene.right, scene.up, scene.fwd)
	k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.02
	k.facing = "NE"
	k.state = "idle"
	k._drive()
	for i in 12:
		await physics_frame
		await process_frame

	var skels: Array[Node] = k.find_children("*", "Skeleton3D", true, false)
	report["skeleton_count"] = skels.size()
	report["body_skel_path"] = String(k.get_path_to(k._skel)) if k._skel != null else "<null>"

	for s in [1.0, 1.25177951388889]:
		k.set_figure_scale(s)
		for i in 12:
			await physics_frame
			await process_frame
		var foot_y: float = k.global_position.y
		var rows := []
		for n in skels:
			var sk := n as Skeleton3D
			var b := sk.find_bone("head_end")
			var row := {"path": String(k.get_path_to(sk)), "bones": sk.get_bone_count(),
						"has_head_end": b >= 0, "is_body_skel": sk == k._skel}
			if b >= 0:
				var top: Vector3 = sk.global_transform * sk.get_bone_global_pose(b).origin
				row["head_end_canvas_px"] = snappedf(absf(
					CliffWorld.canvas_of(top, scene.right, scene.up).y
					- CliffWorld.canvas_of(Vector3(top.x, foot_y, top.z), scene.right, scene.up).y), 0.1)
			else:
				# what the "last skeleton" idiom actually measures when head_end is absent
				var o: Vector3 = sk.global_transform * sk.get_bone_global_pose(-1).origin
				row["bone_minus_1_canvas_px"] = snappedf(absf(
					CliffWorld.canvas_of(o, scene.right, scene.up).y
					- CliffWorld.canvas_of(Vector3(o.x, foot_y, o.z), scene.right, scene.up).y), 0.1)
			rows.append(row)

		# THE SILHOUETTE, which is what "how tall does he look" means and which needs no
		# bone to be spelled right. Union of every visible mesh AABB he owns.
		var top_y := -1e9
		var bot_y := 1e9
		var nmesh := 0
		for m in k.find_children("*", "MeshInstance3D", true, false):
			var mi := m as MeshInstance3D
			if not mi.is_visible_in_tree() or mi.mesh == null:
				continue
			if String(mi.name).findn("outline") >= 0:
				continue
			var ab: AABB = mi.global_transform * mi.get_aabb()
			for c in 8:
				var p := ab.get_endpoint(c)
				top_y = maxf(top_y, p.y)
				bot_y = minf(bot_y, p.y)
			nmesh += 1
		var sil := (top_y - bot_y) * PITCH_COS * PPM
		report["scale_%.5f" % s] = {
			"skeletons": rows, "meshes_counted": nmesh,
			"silhouette_m": snappedf(top_y - bot_y, 0.001),
			"silhouette_canvas_px": snappedf(sil, 0.1),
			"foot_to_mesh_top_m": snappedf(top_y - k.global_position.y, 0.001),
			"foot_to_mesh_top_canvas_px": snappedf((top_y - k.global_position.y) * PITCH_COS * PPM, 0.1),
			"cfg_model_height_m": k.cfg.get("model_height_m", null),
		}
	print(JSON.stringify(report, " "))
	quit(0)
