extends SceneTree
## BV2F lane PT (R-C9-191): the BUILT pilot at the guide (paint) camera, as played -- v1's capture_painted.gd --guide
## recipe, its _guide() COPIED (marked BV2F-PT changes: the pilot plate size, the pilot painted scene, one ground variant):
## render_guide.png (him absent, falling snow hidden, the wind held), heather_colour.png, heather_mask.png. PH's P3/P8 input.
##   BV2F_VARIANT=art Godot --path godot --resolution 640x360 --script res://tools/bv2f/pt_capture_guide.gd -- --out DIR

const GUIDE := Vector2i(4096, 2560)   # BV2F-PT: the pilot plate
const PLAY := Vector2i(1920, 1080)

var out_dir := ""
var vp: SubViewport
var scene
var rep := {}


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	if out_dir == "":
		print("[pt_guide] HALT: --out DIR is required")
		quit(2)
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = PLAY
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/bv2f_pilot_painted.tscn").instantiate()   # BV2F-PT
	scene.skip_character = true
	vp.add_child(scene)
	var waited := 0
	while not scene.ready_done and waited < 3000:
		await process_frame
		waited += 1
	if not scene.ready_done:
		print("[pt_guide] HALT: the scene never finished building")
		quit(3)
		return
	rep["painted"] = scene.report.get("painted", {})
	scene.set_hud_visible(false)
	scene.set_overlay(false)
	scene.set_crucible_visible(false)
	for c in scene.get_children():
		if c is CanvasLayer:
			(c as CanvasLayer).visible = false
	await _guide()
	var f := FileAccess.open(out_dir.path_join("capture_guide.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(rep, " "))
	f.close()
	print("[pt_guide] -> %s" % out_dir)
	quit(0)


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
	print("[pt_guide] %s.png %dx%d" % [nm, img.get_width(), img.get_height()])


func _guide() -> void:
	RenderingServer.directional_shadow_atlas_set_size(8192, true)
	vp.size = GUIDE
	scene.heather_mat.set_shader_parameter("wind_on", 0.0)
	if scene.snowfall != null:
		scene.snowfall.visible = false
	var gw: Dictionary = scene.layout["frame"]["guide_window"]
	var gc: Array = gw["centre_uv"]
	scene.park_camera(scene.uv_to_world(float(gc[0]), float(gc[1])), 1.0)
	await _settle()
	await _shot("render_guide")   # BV2F-PT: the pilot ships as_painted only (its ground IS the painting)
	# THE HEATHER, ALONE WHERE IT IS SEEN: every painted surface black, the snow black (its own
	# id mode), the heather white by emission -- one frame, same camera, same depth
	var saved := {}
	for mi in scene.find_children("*", "MeshInstance3D", true, false):
		var m := (mi as MeshInstance3D).material_override as ShaderMaterial
		if m != null and m.shader != null and m.shader.code.contains("uniform bool id_black"):
			m.set_shader_parameter("id_black", true)
			saved[m] = true
	scene.snow.set_id_black(true)
	# BV2F-PT (R-C9-196): the animated water and the floes are not pieces of v1's id_black set -- drawn BLACK for the heather
	# shots (hiding them exposed the grey background, which reads as heather), and the background black too
	var blk := StandardMaterial3D.new()
	blk.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	blk.albedo_color = Color(0, 0, 0)
	var hid := {}
	for id in scene.nodes:
		if String(id) == "ground_sea" or String(id).begins_with("blobs_shore_ice__"):
			for mi in scene._meshes(scene.nodes[id]):
				hid[mi] = (mi as GeometryInstance3D).material_override
				(mi as GeometryInstance3D).material_override = blk
	var env: Environment = scene.env_node.environment
	var bg_mode := env.background_mode
	var bg_col := env.background_color
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0, 0, 0)
	scene.post_q.visible = false
	# AND ITS COLOUR, alone: the sprays as drawn, over black -- with the mask's coverage this is the
	# stems' own colour, unmixed with the ground between them (the grade is calibrated on it)
	await _settle()
	await _shot("heather_colour")
	scene.heather_mat.set_shader_parameter("id_white", true)
	await _settle()
	await _shot("heather_mask")
	for m in saved:
		(m as ShaderMaterial).set_shader_parameter("id_black", false)
	scene.snow.set_id_black(false)
	for mi in hid:   # BV2F-PT (R-C9-196)
		(mi as GeometryInstance3D).material_override = hid[mi]
	env.background_mode = bg_mode
	env.background_color = bg_col
	scene.heather_mat.set_shader_parameter("id_white", false)
	scene.post_q.visible = true
	scene.heather_mat.set_shader_parameter("wind_on", 1.0)
	rep["guide"] = {"px": [GUIDE.x, GUIDE.y], "centre_uv": gc, "variants": ["as_painted"], "shadow_atlas_px": 8192,
		"wind": "held still for the overlay", "falling_snow": "hidden for the overlay", "him": "absent (the guide's barbarian was painted out)"}
	vp.size = PLAY
	scene.unpark_camera()
	if scene.snowfall != null:
		scene.snowfall.visible = true


