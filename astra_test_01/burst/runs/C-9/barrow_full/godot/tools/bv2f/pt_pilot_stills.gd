extends SceneTree
## BV2F lane PT (R-C9-191): play-camera stills of the BUILT, PAINTED pilot -- the recipe of PT's v1 stills
## (fid/pc/tools/pc_stills.gd, itself capture_painted.gd's _stills: painted scene, 1920x1080 SubViewport, MSAA 4x,
## HUD/overlay/crucible off, him placed, 30 frames standing, settle 4, shot) -- plus, per still, an ID PASS at the
## SAME camera (capture_ids.gd's code: everything black unlit, each placement its own colour, him black) for PH's
## class masks (fid/ph/pilot_p11_spec.json).
##   BV2F_VARIANT=art Godot --path godot --resolution 640x360 --script res://tools/bv2f/pt_pilot_stills.gd -- \
##       --spec <views.json: {"views":[{"name","knight_uv":[u,v],"facing"}]}> --out DIR [--no-ids] [--v1]
## --v1: the same views on v1's painted Barrow (res://scenes/barrow_painted.tscn) for the side-by-side.

const PLAY := Vector2i(1920, 1080)
const DT := 1.0 / 60.0

var out_dir := ""
var spec := ""
var do_ids := true
var v1 := false
var vp: SubViewport
var scene
var rep := {}


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
		if args[i] == "--spec" and i + 1 < args.size():
			spec = args[i + 1]
		if args[i] == "--no-ids":
			do_ids = false
		if args[i] == "--v1":
			v1 = true
	if out_dir == "" or spec == "":
		print("[pt_stills] HALT: --out DIR and --spec FILE are required")
		quit(2)
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	var views: Array = JSON.parse_string(FileAccess.get_file_as_string(spec))["views"]
	vp = SubViewport.new()
	vp.size = PLAY
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/barrow_painted.tscn" if v1 else "res://scenes/bv2f_pilot_painted.tscn").instantiate()
	scene.skip_character = false
	vp.add_child(scene)
	var waited := 0
	while not scene.ready_done and waited < 3000:
		await process_frame
		waited += 1
	if not scene.ready_done:
		print("[pt_stills] HALT: the scene never finished building")
		quit(3)
		return
	rep["painted"] = scene.report.get("painted", {})
	scene.set_hud_visible(false)
	scene.set_overlay(false)
	scene.set_crucible_visible(false)
	for c in scene.get_children():
		if c is CanvasLayer:
			(c as CanvasLayer).visible = false
	rep["renderer"] = {"method": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name()}
	var k = scene.knight
	var out := {}
	var cams := {}
	for s in views:
		var nm := String(s["name"])
		var kuv: Array = s["knight_uv"]
		scene.place_knight(float(kuv[0]), float(kuv[1]), String(s.get("facing", "S")))
		for i in 30:
			k.drive_dir(Vector2.ZERO, false, DT)
			await physics_frame
		await _settle(4)
		# R-C9-232: the frame is the SPEC's (P11's plate frame), not wherever the camera's follow of him puts it -- on the
		# repaint's blockout he can stand below the ground plane (the cove shelf), which lifts the follow camera's centre off
		# the plate and shows unpainted ground. Parked at the spec's ground centre (h = 0) when the spec gives one.
		if s.has("camera_centre_ground_uv"):
			var cc: Array = s["camera_centre_ground_uv"]
			# R-C9-384: optional per-view "zoom" (v1's park_camera zoom: 1.0 = 100.6 px/m; 0.752 = KC2's ZOOM-GD 75.67 px/m)
			scene.park_camera(scene.uv_to_world(float(cc[0]), float(cc[1])), float(s.get("zoom", 1.0)))
			await _settle(2)
		await _shot(nm)
		var at: Vector2 = scene.knight_uv()
		var cam: Camera3D = scene.cam
		cams[nm] = cam.global_transform
		var o: Vector3 = cam.global_position
		var fwd: Vector3 = -cam.global_transform.basis.z
		out[nm] = {"knight_uv": [snappedf(at.x, 0.001), snappedf(at.y, 0.001)], "facing": s.get("facing", "S"),
			"camera": {"position_world": [snappedf(o.x, 0.001), snappedf(o.y, 0.001), snappedf(o.z, 0.001)],
				"forward_world": [snappedf(fwd.x, 0.0001), snappedf(fwd.y, 0.0001), snappedf(fwd.z, 0.0001)],
				"projection": "orthogonal", "ortho_size_m": snappedf(cam.size, 0.0001), "centre_ground_uv": _centre_uv(cam)},
			"png": nm + ".png", "px": [PLAY.x, PLAY.y]}
	if do_ids:
		await _id_pass(views, cams, out)
	rep["views"] = out
	rep["_what"] = "BV2F PT stills (%s): painted, 1920x1080, MSAA 4x, pc_stills.gd recipe" % ("v1 barrow_painted" if v1 else "bv2f pilot")
	var f := FileAccess.open(out_dir.path_join("views.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(rep, " "))
	f.close()
	print("[pt_stills] -> %s" % out_dir)
	quit(0)


func _id_pass(views: Array, cams: Dictionary, out: Dictionary) -> void:
	## capture_ids.gd's own colouring (frozen Tier-B capture_ids.gd:61-105), at each still's camera
	scene.set_markers(false)
	scene.set_stack(false)
	scene.set_process(false)
	if scene.snowfall != null:
		scene.snowfall.visible = false
	var env: Environment = scene.env_node.environment
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0, 0, 0)
	env.fog_enabled = false
	env.glow_enabled = false
	env.adjustment_enabled = false
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	env.tonemap_exposure = 1.0
	var black := StandardMaterial3D.new()
	black.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	black.albedo_color = Color(0, 0, 0)
	# the PAINTED scene's dynamic layers are not pieces and lie OVER the ground: v1's capture_ids ran on the unpainted
	# scene, which has none of them -- hidden here, so the ID pass sees the ground classes they stand on
	if scene.get("snow") != null and scene.snow != null:
		(scene.snow as Node3D).visible = false
	for mm in scene.find_children("*", "MultiMeshInstance3D", true, false):
		(mm as GeometryInstance3D).visible = false
	for n in scene.find_children("*", "GeometryInstance3D", true, false):
		var gi := n as GeometryInstance3D
		if gi is GPUParticles3D or gi is Label3D:
			gi.visible = false
			continue
		if String(gi.name).ends_with("_ink"):
			gi.visible = false
			continue
		gi.material_override = black
		gi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var ids := {}
	var order: Array = scene.nodes.keys()
	order.sort()
	var idx := 0
	for id in order:
		idx += 1
		var col := Color8((idx % 16) * 16 + 8, int(idx / 16) * 16 + 8, 200)
		var m := StandardMaterial3D.new()
		m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		m.albedo_color = col
		m.cull_mode = BaseMaterial3D.CULL_DISABLED
		for mi in (scene.nodes[id] as Node).find_children("*", "GeometryInstance3D", true, false):
			if String(mi.name).ends_with("_ink") or mi is Label3D or mi is GPUParticles3D:
				continue
			(mi as GeometryInstance3D).material_override = m
		var cls := "?"
		if scene.get("built") != null and (scene.built as Dictionary).has(id):
			cls = String(scene.built[id].get("class", "?"))
		ids[str(idx)] = {"id": id, "class": cls}
	var vpm := vp.msaa_3d
	vp.msaa_3d = Viewport.MSAA_DISABLED
	for s in views:
		var nm := String(s["name"])
		scene.cam.global_transform = cams[nm]
		await _settle(3)
		await _shot(nm + ".ids")
	vp.msaa_3d = vpm
	var f := FileAccess.open(out_dir.path_join("ids_table.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify({"code": "R = (i % 16) * 16 + 8, G = (i / 16) * 16 + 8, B = 200; 0 = other (him, heather sprays, snow field)", "ids": ids}, " "))
	f.close()


func _centre_uv(cam: Camera3D) -> Array:
	var c := Vector2(PLAY.x * 0.5, PLAY.y * 0.5)
	var o := cam.project_ray_origin(c)
	var d := cam.project_ray_normal(c)
	if absf(d.y) < 1e-6:
		return []
	var p := o + d * (-o.y / d.y)
	var uv: Vector2 = scene.world_to_uv(p)
	return [snappedf(uv.x, 0.001), snappedf(uv.y, 0.001)]


func _settle(n := 8) -> void:
	for i in n:
		await physics_frame
		await process_frame
	RenderingServer.force_draw()
	await process_frame


func _shot(nm: String) -> void:
	for i in 3:
		await process_frame
	var img: Image = vp.get_texture().get_image()
	img.save_png(out_dir.path_join(nm + ".png"))
	print("[pt_stills] %s.png %dx%d" % [nm, img.get_width(), img.get_height()])
