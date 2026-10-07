extends SceneTree
## BV2F lane PH (R-C9-201 (2)): P3's sea with the DEV-5 water's motion layers removed, at the guide (paint) camera, as
## PT's pt_capture_guide.gd frames it (pilot plate 4096 x 2560, guide-window centre, wind held, snowfall hidden):
##   rg_base.png   the water shader re-derived to draw its PAINTED BASE only (swell, ripples, foam dropped)
##   rg_rest.png   the water shader with TIME held at 0 (every motion layer drawn, at rest)
##   rg_red.png    RED: the sea's material replaced by a LIT plane (StandardMaterial3D, the shader's deep_col)
##   Godot --path . --resolution 640x360 --script <abs>/ph_p3_sea.gd -- --out DIR
const GUIDE := Vector2i(4096, 2560)
var out_dir := ""
var vp: SubViewport
var scene


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = Vector2i(1920, 1080)
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/bv2f_pilot_painted.tscn").instantiate()
	scene.skip_character = true
	vp.add_child(scene)
	var waited := 0
	while not scene.ready_done and waited < 3000:
		await process_frame
		waited += 1
	if not scene.ready_done:
		print("[ph_p3_sea] HALT: the scene never finished building")
		quit(3)
		return
	scene.set_hud_visible(false)
	scene.set_overlay(false)
	scene.set_crucible_visible(false)
	for c in scene.get_children():
		if c is CanvasLayer:
			(c as CanvasLayer).visible = false
	RenderingServer.directional_shadow_atlas_set_size(8192, true)
	vp.size = GUIDE
	scene.heather_mat.set_shader_parameter("wind_on", 0.0)
	if scene.snowfall != null:
		scene.snowfall.visible = false
	var gc: Array = scene.layout["frame"]["guide_window"]["centre_uv"]
	scene.park_camera(scene.uv_to_world(float(gc[0]), float(gc[1])), 1.0)
	var wm: ShaderMaterial = scene.water_mat_pt
	var code0: String = wm.shader.code
	var sea: Array = scene._meshes(scene.nodes["ground_sea"])
	# (1) painted base only
	var cb := code0.replace("	ALBEDO = col;\n", "	ALBEDO = base;   // PH R-C9-201: the painted base only\n")
	assert(cb != code0)
	var shb := Shader.new()
	shb.code = cb
	wm.shader = shb
	await _settle()
	await _shot("rg_base")
	# (2) motion layers held at rest (TIME = 0)
	var cr := code0.replace("TIME", "0.0")
	var shr := Shader.new()
	shr.code = cr
	wm.shader = shr
	await _settle()
	await _shot("rg_rest")
	# (3) RED: a lit plane in place of the painted base
	var lit := StandardMaterial3D.new()
	lit.albedo_color = Color(0.13, 0.22, 0.31)
	var saved := {}
	for mi in sea:
		saved[mi] = (mi as GeometryInstance3D).material_override
		(mi as GeometryInstance3D).material_override = lit
	await _settle()
	await _shot("rg_red")
	for mi in saved:
		(mi as GeometryInstance3D).material_override = saved[mi]
	wm.shader.code = code0
	print("[ph_p3_sea] -> %s" % out_dir)
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
	print("[ph_p3_sea] %s.png %dx%d" % [nm, img.get_width(), img.get_height()])
