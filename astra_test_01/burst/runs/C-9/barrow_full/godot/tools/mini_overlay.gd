extends SceneTree
## C-9 T10-2 step 4 (B): ONE mini overlay check -- a few baked heroes rendered at the guide
## camera, cropped at their plates, for tools/mini_overlay.py to set against the painting. drax.
##
##   Godot --path godot --resolution 640x360 --script tools/mini_overlay.gd -- --out DIR \
##         --ids ring_p155,door_lintel,grave_marker_W,fallen_tree_log_A --bakes ABS_DIR
##
## Two renders of the guide frame, cropped per piece (with a margin), nothing else kept:
##   unlit_<id>.png   the piece wears its bake UNSHADED: the projection alone, which the painting
##                    must match wherever the piece is seen (the bake's own test, as a render)
##   lit_<id>.png     the piece wears its bake as the ALBEDO of the blockout's own ramp material
##                    (snow layer and mottle off, so the only change is the light) under its sun:
##                    the painted light, lit a second time -- the design question § 4 of the plan
## The rest of the scene stays as the blockout draws it.

const GUIDE := Vector2i(5376, 3328)
const MARGIN := 12

var out_dir := ""
var bakes := ""
var ids: Array = []
var vp: SubViewport
var scene


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
		if args[i] == "--bakes" and i + 1 < args.size():
			bakes = args[i + 1]
		if args[i] == "--ids" and i + 1 < args.size():
			ids = Array(args[i + 1].split(","))
	if out_dir == "" or bakes == "" or ids.is_empty():
		print("[overlay] HALT: --out, --bakes and --ids are required")
		quit(2)
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	var plates: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(
		ProjectSettings.globalize_path("res://") + "../take/plates/plates.json"))["plates"]
	vp = SubViewport.new()
	vp.size = GUIDE
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
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
		print("[overlay] HALT: the scene never finished building")
		quit(3)
		return
	scene.set_hud_visible(false)
	scene.set_overlay(false)
	scene.set_crucible_visible(false)
	scene.set_markers(false)
	var gw: Dictionary = scene.layout["frame"]["guide_window"]
	var gc: Array = gw["centre_uv"]
	scene.park_camera(scene.uv_to_world(float(gc[0]), float(gc[1])), 1.0)
	# the bakes, as textures (mipmapped: a 1024 texture lands on ~100 px of screen)
	var tex := {}
	for id in ids:
		var img := Image.load_from_file("%s/%s.png" % [bakes, id])
		if img == null or img.is_empty():
			print("[overlay] HALT: no bake for %s" % id)
			quit(4)
			return
		img.generate_mipmaps()
		tex[id] = ImageTexture.create_from_image(img)
	# ---- 1. unlit: the projection alone ----
	var saved := {}
	for id in ids:
		for mi in scene._meshes(scene.nodes[id]):
			saved[mi] = (mi as MeshInstance3D).material_override
			var m := StandardMaterial3D.new()
			m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
			m.albedo_texture = tex[id]
			m.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
			(mi as MeshInstance3D).material_override = m
	await _settle()
	_crops("unlit", plates)
	# ---- 2. lit: the bake as the ramp's albedo, under the blockout's own sun ----
	for mi in saved:
		var rm = saved[mi]
		if rm is ShaderMaterial:
			var r2 := (rm as ShaderMaterial).duplicate() as ShaderMaterial
			var id := ""
			for k in ids:
				if (scene.nodes[k] as Node).is_ancestor_of(mi):
					id = k
			r2.set_shader_parameter("albedo_tex", tex[id])
			r2.set_shader_parameter("use_tex", true)
			r2.set_shader_parameter("tex_tint", Vector3.ONE)
			r2.set_shader_parameter("snow_amount", 0.0)
			r2.set_shader_parameter("mottle_amp", 0.0)
			r2.set_shader_parameter("hatch_amp", 0.0)
			(mi as MeshInstance3D).material_override = r2
	await _settle()
	_crops("lit", plates)
	print("[overlay] %d pieces, unlit and lit, cropped into %s" % [ids.size(), out_dir])
	quit(0)


func _crops(tag: String, plates: Dictionary) -> void:
	var img: Image = vp.get_texture().get_image()
	for id in ids:
		var r: Array = plates[id]["rect_px"]
		var x0 := maxi(int(r[0]) - MARGIN, 0)
		var y0 := maxi(int(r[1]) - MARGIN, 0)
		var x1 := mini(int(r[0]) + int(r[2]) + MARGIN, GUIDE.x)
		var y1 := mini(int(r[1]) + int(r[3]) + MARGIN, GUIDE.y)
		img.get_region(Rect2i(x0, y0, x1 - x0, y1 - y0)).save_png("%s/%s_%s.png" % [out_dir, tag, id])


func _settle() -> void:
	for i in 10:
		await physics_frame
		await process_frame
	RenderingServer.force_draw()
	for i in 3:
		await process_frame
