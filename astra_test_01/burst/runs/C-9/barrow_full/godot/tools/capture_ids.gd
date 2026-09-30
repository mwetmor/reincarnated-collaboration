extends SceneTree
## C-9 T10-2 step 3: THE GUIDE VIEW AS AN ID RENDER -- which placement every pixel of the
## paint-over shows. drax.
##
##   Godot --path godot --resolution 640x360 --script tools/capture_ids.gd -- --out DIR
##
## The painting was made OVER the guide (capture_blockout.gd's guide.png, 5376 x 3328), so the
## guide's camera is the painting's camera. This renders the same frame with every placement in
## its own flat colour and everything else black: no light, no fog, no ink, no MSAA, no him.
## Each hero's painted look is then cut by its own geometry, not by a guess at its colour
## (tools/take_from_paint.py).
##
## THE CODE: placement index i (1-based, in the order of ids.json) is written as
##   R = (i % 16) * 16 + 8,  G = (i / 16) * 16 + 8,  B = 200
## -- values 16 apart, so the sRGB round trip's +-1 cannot move a pixel to another piece.
##
## Writes into --out:
##   ids.png     5376 x 3328, the ID render
##   ids.json    index -> placement id, class, piece, colour; plus the instrument check: every
##               placement's ground point projected by the camera against the layout's own
##               px_from_uv formula (the two must agree to a fraction of a pixel)

const GUIDE := Vector2i(5376, 3328)

var out_dir := ""
var vp: SubViewport
var scene


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	if out_dir == "":
		print("[ids] HALT: --out DIR is required")
		quit(2)
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = GUIDE
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_DISABLED
	vp.screen_space_aa = Viewport.SCREEN_SPACE_AA_DISABLED
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/barrow_full.tscn").instantiate()
	scene.skip_character = true
	vp.add_child(scene)
	var waited := 0
	while not scene.ready_done and waited < 1500:
		await process_frame
		waited += 1
	if not scene.ready_done:
		print("[ids] HALT: the scene never finished building")
		quit(3)
		return
	scene.set_hud_visible(false)
	scene.set_overlay(false)
	scene.set_crucible_visible(false)
	scene.set_markers(false)
	scene.set_stack(false)                       # hides the screen-space pen's quad
	var env: Environment = scene.env_node.environment
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0, 0, 0)
	env.fog_enabled = false
	env.glow_enabled = false
	env.adjustment_enabled = false
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	env.tonemap_exposure = 1.0
	# EVERYTHING black and unlit first: the ground, the bounds, anything a placement is not
	var black := StandardMaterial3D.new()
	black.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	black.albedo_color = Color(0, 0, 0)
	for n in scene.find_children("*", "GeometryInstance3D", true, false):
		var gi := n as GeometryInstance3D
		if gi is GPUParticles3D or gi is Label3D:
			gi.visible = false
			continue
		if String(gi.name).ends_with("_ink"):
			gi.visible = false                   # the hull pen: the geometry's own silhouette only
			continue
		gi.material_override = black
		gi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	# ...then each placement in its own colour
	var ids := {}
	var order: Array = scene.nodes.keys()
	order.sort()
	var idx := 0
	var by_id := {}
	for e in scene.layout["placements"]:
		by_id[String(e["id"])] = e
	for id in order:
		idx += 1
		var col := Color8((idx % 16) * 16 + 8, int(idx / 16) * 16 + 8, 200)
		var m := StandardMaterial3D.new()
		m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		m.albedo_color = col
		m.cull_mode = BaseMaterial3D.CULL_DISABLED
		var n_mesh := 0
		for mi in (scene.nodes[id] as Node).find_children("*", "GeometryInstance3D", true, false):
			if String(mi.name).ends_with("_ink") or mi is Label3D or mi is GPUParticles3D:
				continue
			(mi as GeometryInstance3D).material_override = m
			n_mesh += 1
		var e: Dictionary = by_id.get(String(id), {})
		ids[str(idx)] = {"id": id, "class": e.get("class", "?"), "piece": e.get("piece", "?"),
			"rgb": [col.r8, col.g8, col.b8], "meshes": n_mesh}
	# THE GUIDE'S OWN CAMERA: centred on the window's centre, zoom 1, as capture_blockout.gd
	var gw: Dictionary = scene.layout["frame"]["guide_window"]
	var gc: Array = gw["centre_uv"]
	scene.park_camera(scene.uv_to_world(float(gc[0]), float(gc[1])), 1.0)
	for i in 10:
		await physics_frame
		await process_frame
	RenderingServer.force_draw()
	await process_frame
	# the instrument check: camera projection against the layout's px_from_uv formula
	var u0 := float(gw["u"][0])
	var v1 := float(gw["v"][1])
	var cam: Camera3D = scene.cam
	var worst := 0.0
	var n_chk := 0
	for id in order:
		var e: Dictionary = by_id.get(String(id), {})
		if not e.has("uv") or e["uv"] == null:
			continue
		var uv: Array = e["uv"]
		var p: Vector3 = scene.uv_to_world(float(uv[0]), float(uv[1]))
		var s := cam.unproject_position(p)
		var fx := (float(uv[0]) - u0) * 100.617553710938
		var fy := (v1 - float(uv[1])) * 80.3076
		worst = maxf(worst, Vector2(fx, fy).distance_to(s))
		n_chk += 1
	for i in 3:
		await process_frame
	var img: Image = vp.get_texture().get_image()
	if img.get_width() != GUIDE.x or img.get_height() != GUIDE.y:
		print("[ids] SIZE MISMATCH: %dx%d" % [img.get_width(), img.get_height()])
		quit(4)
		return
	img.save_png("%s/ids.png" % out_dir)
	var f := FileAccess.open("%s/ids.json" % out_dir, FileAccess.WRITE)
	f.store_string(JSON.stringify({
		"_what": "C-9 T10-2 step 3: the guide view (5376 x 3328, capture_blockout's camera) as an ID render",
		"code": "R = (i % 16) * 16 + 8, G = (i / 16) * 16 + 8, B = 200; ground and everything else 0",
		"placements": ids,
		"instrument_check": {"placements_checked": n_chk, "worst_px_camera_vs_formula": snappedf(worst, 0.001),
			"formula": "x = (u - u0) * 100.617553710938, y = (v1 - v) * 80.3076 at h = 0"},
	}, " "))
	print("[ids] ids.png 5376x3328, %d placements, camera vs px_from_uv worst %.3f px over %d points" % [
		idx, worst, n_chk])
	quit(0)
