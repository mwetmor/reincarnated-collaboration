extends SceneTree
## BV2F lane LV, M1 packet: play-camera stills of the barrow_v2 level (scenes/bv2f_barrow_v2.tscn) at v1's OWN play
## camera and zoom (orthographic, pitch 52.95354, yaw 47, 100.6 px/m across = the 19.1 x 13.4 m window, M0(c)).
## Him at each spot, the camera on him exactly as in play (_camera_aim), 1920 x 1080. Not a paint-pipeline tool.
##   Godot --path godot --resolution 640x360 --script tools/bv2f/m1_stills.gd -- --out DIR --spec SPEC.json
## SPEC: [{"name": "...", "uv": [u, v], "facing": "N"}, ...]   (u = sim x, v = -sim y)

const PLAY := Vector2i(1920, 1080)
const DT := 1.0 / 60.0
var vp: SubViewport
var scene


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var out_dir := ""
	var spec_p := ""
	for i in args.size():
		if args[i] == "--out":
			out_dir = args[i + 1]
		if args[i] == "--spec":
			spec_p = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir)
	var spec = JSON.parse_string(FileAccess.get_file_as_string(spec_p))
	vp = SubViewport.new()
	vp.size = PLAY
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/bv2f_barrow_v2.tscn").instantiate()
	vp.add_child(scene)
	var waited := 0
	while not scene.ready_done and waited < 1500:
		await process_frame
		waited += 1
	scene.set_hud_visible(false)
	var k = scene.knight
	var rep := []
	for s in spec:
		if s.has("topdown"):
			var td: Array = s["topdown"]
			vp.size = Vector2i(2400, 2240)
			scene.sun.shadow_enabled = false
			scene.set_topdown(Vector2(float(td[0]), float(td[1])), float(td[2]))
			for i in 8:
				await process_frame
			RenderingServer.force_draw()
			await process_frame
			vp.get_texture().get_image().save_png("%s/%s.png" % [out_dir, s["name"]])
			rep.append({"name": s["name"], "topdown": td, "px": [2400, 2240], "px_per_m": 2240.0 / float(td[2])})
			scene.sun.shadow_enabled = true
			vp.size = PLAY
			print("[m1] %s" % s["name"])
			continue
		scene.freeze_pose(false)
		scene.place_knight(float(s["uv"][0]), float(s["uv"][1]), String(s.get("facing", "S")))
		for i in 12:
			k.drive_dir(Vector2.ZERO, false, DT)
			await physics_frame
		scene.freeze_pose(true)
		if s.has("aim_uv"):        # R-C9-177 (d): the frame ON the hero object, him at the disc edge for scale
			var au: Array = s["aim_uv"]
			scene.park_camera(scene.uv_to_world(float(au[0]), float(au[1]), float(s.get("aim_h", 0.0))), 1.0)
		else:
			scene.park_camera(scene._camera_aim(), 1.0)
		for i in 8:
			await process_frame
		RenderingServer.force_draw()
		await process_frame
		var img: Image = vp.get_texture().get_image()
		img.save_png("%s/%s.png" % [out_dir, s["name"]])
		rep.append({"name": s["name"], "uv": s["uv"], "him_uv": [scene.knight_uv().x, scene.knight_uv().y]})
		print("[m1] %s" % s["name"])
	var f := FileAccess.open("%s/stills.json" % out_dir, FileAccess.WRITE)
	f.store_string(JSON.stringify({"camera": "v1 play camera (barrow_full.gd), 1920x1080, park_camera(_camera_aim)", "stills": rep}, " "))
	f.close()
	quit(0)
