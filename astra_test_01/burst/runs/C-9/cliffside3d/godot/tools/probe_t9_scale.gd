extends SceneTree
# C-9 T9: the three things T9-1a and T9-1b are standing on, measured in the scene rather
# than derived on paper.
#
#  1. THE RAIL POSTS EXIST TWICE. cliffside_blockout.gd builds a 1.20 m post box AND the
#     painter painted a post into the plate at the same spot. On paper the painted one is
#     1.72-1.81 m, so a true-scale 3D post would leave a stub of painted post standing
#     above it. Paper is not the scene: measure both, on the canvas, in pixels.
#  2. THE FIGURE. T9-0 reports 123.3 canvas px at scale 1.0, while 1.85 m through this
#     projection is 112. One of those is a label and one is a measurement; every prop size
#     in T9-1a is quoted against it, so it has to be the measurement.
#  3. WHAT THE TERRAIN ACTUALLY COVERS. The chasm's cloud bank is plate content with no
#     geometry under it, which is why it rides the unlit backdrop quad and is never
#     double-lit -- the albedo repaint must leave it alone. That is an argument from
#     reading world.gd. Render the bridge frame with the foreground shown and hidden and
#     let the difference say it instead.
#
#   Godot --path godot --resolution 1920x1080 --script tools/probe_t9_scale.gd -- --out DIR

const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const PITCH_COS := 0.602462407085
const AIM := Vector2(3459.88, 1027.18)
const STAND := Vector2(3380.0, 1120.0)

var out_dir := ""
var scene
var vp: SubViewport
var cam: Camera3D
var report := {}


func _initialize() -> void:
	out_dir = ProjectSettings.globalize_path("user://t9probe")
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
	for i in 60:
		await process_frame
	cam = Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.near = scene.cam.near
	cam.far = scene.cam.far
	cam.cull_mask = scene.cam.cull_mask
	vp.add_child(cam)
	cam.current = true

	report["px_per_vertical_m"] = snappedf(PPM * PITCH_COS, 0.001)

	# ---- 1. the blockout's rail posts, on the canvas ------------------------
	var posts := []
	for m in scene.level.find_children("*", "MeshInstance3D", true, false):
		var mi := m as MeshInstance3D
		if not String(mi.name).begins_with("bridge_post"):
			continue
		var ab: AABB = mi.global_transform * mi.get_aabb()
		var lo := ab.position
		var hi := ab.position + ab.size
		# the post's own vertical extent, projected: top and bottom of the same column
		var mid := Vector3((lo.x + hi.x) * 0.5, 0.0, (lo.z + hi.z) * 0.5)
		var c_bot := CliffWorld.canvas_of(Vector3(mid.x, lo.y, mid.z), scene.right, scene.up)
		var c_top := CliffWorld.canvas_of(Vector3(mid.x, hi.y, mid.z), scene.right, scene.up)
		posts.append({"node": String(mi.name),
					  "mesh_size_m": [snappedf(ab.size.x, 0.001), snappedf(ab.size.y, 0.001),
									  snappedf(ab.size.z, 0.001)],
					  "canvas_foot": [snappedf(c_bot.x, 0.1), snappedf(c_bot.y, 0.1)],
					  "canvas_px_tall": snappedf(absf(c_top.y - c_bot.y), 0.1),
					  "visible": mi.visible, "layers": mi.layers})
	posts.sort_custom(func(a, b): return a["canvas_foot"][0] < b["canvas_foot"][0])
	report["blockout_rail_posts"] = posts

	# the painted post CARDS, as built
	var cards := []
	var props: Node = scene.get_node_or_null(^"Props")
	if props != null:
		for c in props.get_children():
			var mi := c as MeshInstance3D
			if mi == null or not String(mi.name).begins_with("bridge_post"):
				continue
			var q := mi.mesh as QuadMesh
			var anc: Vector2 = mi.get_meta("anchor_px")
			var r: Rect2 = mi.get_meta("rect_px")
			cards.append({"node": String(mi.name), "anchor_px": [anc.x, anc.y],
						  "sprite_px": [r.size.x, r.size.y],
						  "card_m": [snappedf(q.size.x, 0.001), snappedf(q.size.y, 0.001)],
						  "canvas_px_tall": snappedf(q.size.y * PITCH_COS * PPM, 0.1)})
	cards.sort_custom(func(a, b): return a["anchor_px"][0] < b["anchor_px"][0])
	report["painted_post_cards"] = cards
	if not posts.is_empty() and not cards.is_empty():
		var g: float = float(posts[0]["canvas_px_tall"])
		var worst := 0.0
		for c in cards:
			worst = maxf(worst, float(c["canvas_px_tall"]) - g)
		report["painted_post_stub_above_true_post_px"] = snappedf(worst, 0.1)

	# ---- 2. the figure, measured the way T9-0 measured it -------------------
	var k = scene.knight
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var g0 := CliffWorld.ground_at(space, STAND, scene.right, scene.up, scene.fwd)
	k.global_position = (g0["position"] as Vector3) + Vector3.UP * 0.02
	k.facing = "NE"
	k.state = "idle"
	k._drive()
	var skel: Skeleton3D = null
	for n in k.find_children("*", "Skeleton3D", true, false):
		skel = n
	var he := skel.find_bone("head_end")
	var fig := {}
	for s in [1.0, 1.25177951388889]:
		k.set_figure_scale(s)
		for i in 8:
			await physics_frame
			await process_frame
		var top: Vector3 = skel.global_transform * skel.get_bone_global_pose(he).origin
		var ct := CliffWorld.canvas_of(top, scene.right, scene.up)
		var cf := CliffWorld.canvas_of(Vector3(top.x, k.global_position.y, top.z),
									   scene.right, scene.up)
		var px := absf(ct.y - cf.y)
		fig["scale_%.5f" % s] = {"canvas_px": snappedf(px, 0.1),
								 "implied_world_m": snappedf(px / (PPM * PITCH_COS), 0.001)}
	report["figure"] = fig
	k.set_figure_scale(1.0)

	# ---- 3. what the terrain covers in the bridge frame ---------------------
	scene.set_lit(true)
	k.set_figure_scale(1.0)
	k.visible = false
	scene.look_at_canvas(AIM, 0.0, 1.0)
	for i in 10:
		await physics_frame
		await process_frame
	await _shot("t9probe_fg_on")
	for mi in scene._fg:
		mi.visible = false
	for i in 6:
		await process_frame
	await _shot("t9probe_fg_off")
	for mi in scene._fg:
		mi.visible = true

	var f := FileAccess.open(out_dir + "/t9probe.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("[t9probe] -> %s" % out_dir)
	print(JSON.stringify(report, " "))
	quit(0)


func _mirror() -> void:
	cam.global_transform = scene.cam.global_transform
	cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))


func _shot(nm: String) -> void:
	_mirror()
	for i in 4:
		await process_frame
	vp.get_texture().get_image().save_png("%s/%s.png" % [out_dir, nm])
