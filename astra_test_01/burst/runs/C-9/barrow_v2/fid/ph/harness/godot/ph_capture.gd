extends SceneTree
## BV2F lane PH (galadriel) -- P3 input capture for a barrow_v2-style level that EXTENDS barrow_full.gd.
## Read-only on the level: nothing is saved into barrow_full/godot; frames go to OUT (under fid/ph/).
##
##   cd barrow_full/godot && Godot --path . --resolution 640x360 --script <abs>/ph_capture.gd -- <scene> <OUT>
##     <scene>  res://scenes/barrow_v2_sw.tscn  (R-C9-159) -- or a later fid level with the same paint frame law
##
## The PAINT FRAME camera (the level's lvl.frame.paint: u0, v1, ppm, size_px), as tools/v2sw_run.gd _guide places it,
## but the level PAINTED and AS PLAYED (pen on, both suns), him absent, falling snow hidden, the wind held:
##   render.png             the statics as the player sees them, at the painting's own pixels
##   hide_<group>.png       the same frame with one group of static models SHADOW-ONLY (body gone, its cast shadow kept;
##                          a group = one GLB key);
##                          |render - hide_<group>| > 0 is that group's visible silhouette, occlusion included
##   hide_heather.png       the same frame with the 3D heather hidden (its pixels are movers, not statics)
##   ph_capture.json        what was hidden per frame, the frame, the renderer
var scene
var out_dir := ""
var scene_path := ""
var vp: SubViewport
var rep := {}


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	scene_path = args[0]
	out_dir = args[1]
	DirAccess.make_dir_recursive_absolute(out_dir)
	_run()


func _settle(n := 10) -> void:
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
	print("[ph] %s.png %dx%d" % [nm, img.get_width(), img.get_height()])


func _run() -> void:
	vp = SubViewport.new()
	vp.size = Vector2i(640, 360)
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load(scene_path).instantiate()
	scene.skip_character = true
	vp.add_child(scene)
	var waited := 0
	while not scene.ready_done and waited < 4000:
		await process_frame
		waited += 1
	if not scene.ready_done:
		print("[ph] HALT: the scene never finished building")
		quit(3)
		return
	scene.set_hud_visible(false)
	scene.set_crucible_visible(false)
	for c in scene.get_children():
		if c is CanvasLayer:
			(c as CanvasLayer).visible = false
	if scene.heather_mat != null:
		scene.heather_mat.set_shader_parameter("wind_on", 0.0)
	if scene.snowfall != null:
		scene.snowfall.visible = false
		scene.snowfall.emitting = false
	RenderingServer.directional_shadow_atlas_set_size(8192, true)
	var F: Dictionary = scene.lvl["frame"]["paint"]
	var W := int(F["size_px"][0])
	var H := int(F["size_px"][1])
	vp.size = Vector2i(W, H)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	var ppm := float(F["ppm"])
	cam.size = float(H) / ppm
	cam.near = 0.05
	cam.far = 400.0
	vp.add_child(cam)
	var p := deg_to_rad(scene.PL_PITCH_DEG)
	var uc := float(F["u0"]) + float(W) / ppm * 0.5
	var sc := float(F["v1"]) * sin(p) - float(H) / ppm * 0.5
	var aim: Vector3 = scene.uv_to_world(uc, sc / sin(p), 0.0)
	cam.global_transform = Transform3D(scene.cam.global_transform.basis, aim - scene.fwd * 60.0)
	cam.make_current()
	rep["frame"] = F
	rep["renderer"] = {"method": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name()}
	rep["painted"] = scene.report.get("painted", {})
	await _settle(30)
	await _shot("render")
	var groups := {}
	for key in scene.model_meshes:
		var nm := String(key).get_file().get_basename()
		if groups.has(nm):
			nm = nm + "_" + str(groups.size())
		groups[nm] = scene.model_meshes[key]
	rep["groups"] = {}
	for nm in groups:
		var saved := {}
		for mi in groups[nm]:
			saved[mi] = (mi as GeometryInstance3D).cast_shadow
			(mi as GeometryInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_SHADOWS_ONLY
		await _settle()
		await _shot("hide_" + nm)
		for mi in groups[nm]:
			(mi as GeometryInstance3D).cast_shadow = saved[mi]
		rep["groups"][nm] = (groups[nm] as Array).size()
	var hs := {}
	for mmi in scene._heather_mmi:
		hs[mmi] = (mmi as GeometryInstance3D).cast_shadow
		(mmi as GeometryInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_SHADOWS_ONLY
	await _settle()
	await _shot("hide_heather")
	for mmi in scene._heather_mmi:
		(mmi as GeometryInstance3D).cast_shadow = hs[mmi]
	var f := FileAccess.open(out_dir.path_join("ph_capture.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(rep, " "))
	f.close()
	print("[ph] done -> %s" % out_dir)
	quit(0)
