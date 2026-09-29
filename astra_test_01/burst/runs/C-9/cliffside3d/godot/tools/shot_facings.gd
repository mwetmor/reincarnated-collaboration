extends SceneTree
# C-9 R-C9-69: one still per facing at the play camera, and the height he actually reads.
#
# The 154.4 px in the hand-off is a prediction from the scale rule. What he MEASURES at is
# the silhouette the camera returns, so it is taken here -- with him on and off the same
# frame -- rather than carried forward on trust. The eight facings are the other half:
# a derived yaw that takes the model's forward axis onto the direction each facing MOVES
# in is either right for all eight or wrong for all eight, and eight pictures say which.
#
#   Godot --path godot --resolution 1920x1080 --script tools/shot_facings.gd -- --out D

const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const SPOT := Vector2(2285.62, 2407.32)        # the plateau spawn
const FACINGS := ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]

var out_dir := ""
var scene
var vp: SubViewport
var cam: Camera3D


func _initialize() -> void:
	out_dir = ProjectSettings.globalize_path("user://facings")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = false
	vp.msaa_3d = Viewport.MSAA_4X
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
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var g := CliffWorld.ground_at(space, SPOT, scene.right, scene.up, scene.fwd)
	k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.02
	k.state = "idle"
	scene.look_at_canvas(SPOT + Vector2(0, -60), 0.0, 2.2)
	_mirror()
	for i in 10:
		await physics_frame
		await process_frame

	k.visible = false
	var base := await _grab()
	var rows := []
	for f in FACINGS:
		k.visible = true
		k.facing = f
		k.state = "idle"
		k._drive()
		for i in 6:
			await physics_frame
			await process_frame
		var img := await _grab()
		img.save_png("%s/facing_%s.png" % [out_dir, f])
		var r := _bbox(base, img)
		# THE FIGURE HEIGHT, not the bounding box. A silhouette box around a 3D body seen
		# from 53 degrees is as tall as his outstretched arm reaches, and reading 218 px off
		# it where the scale rule predicts 154.4 says nothing about his size: the rule is
		# about head-to-feet. That is what is reported, and the box beside it.
		var skel: Skeleton3D = null
		for n in k.find_children("*", "Skeleton3D", true, false):
			skel = n
		var he := skel.find_bone("head_end")
		var top: Vector3 = skel.global_transform * skel.get_bone_global_pose(he).origin
		var c_top := CliffWorld.canvas_of(top, scene.right, scene.up)
		var c_foot := CliffWorld.canvas_of(Vector3(top.x, k.global_position.y, top.z),
											scene.right, scene.up)
		var fig: float = absf(c_top.y - c_foot.y)
		rows.append({"facing": f, "screen_bbox": [r.position.x, r.position.y, r.size.x, r.size.y],
					 "figure_height_canvas_px": snappedf(fig, 0.1),
					 "bbox_height_canvas_px": snappedf(r.size.y / 2.2, 0.1)})
		print("  %-3s figure %.1f canvas px   (silhouette box %d x %d screen px)" %
			[f, fig, int(r.size.x), int(r.size.y)])
	var f2 := FileAccess.open(out_dir + "/facings.json", FileAccess.WRITE)
	f2.store_string(JSON.stringify({"spot_canvas_px": [SPOT.x, SPOT.y], "zoom": 2.2,
		"figure_scale": k._figure_scale, "rows": rows,
		"expected_px": 154.4}, " "))
	f2.close()
	print("[facings] -> ", out_dir)
	quit(0)


func _bbox(a: Image, b: Image) -> Rect2:
	var x0 := 1 << 20
	var y0 := 1 << 20
	var x1 := -1
	var y1 := -1
	for y in SHOT.y:
		for x in SHOT.x:
			var p := a.get_pixel(x, y)
			var q := b.get_pixel(x, y)
			if absf(p.r - q.r) + absf(p.g - q.g) + absf(p.b - q.b) > 0.02:
				x0 = mini(x0, x)
				y0 = mini(y0, y)
				x1 = maxi(x1, x)
				y1 = maxi(y1, y)
	if x1 < 0:
		return Rect2()
	return Rect2(x0, y0, x1 - x0 + 1, y1 - y0 + 1)


func _mirror() -> void:
	cam.global_transform = scene.cam.global_transform
	cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))


func _grab() -> Image:
	_mirror()
	for i in 4:
		await process_frame
	return vp.get_texture().get_image()
