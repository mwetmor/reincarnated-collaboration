extends SceneTree
# Which of three things draws the stripes on the kerb: the shadow map, the pen, or the ramp's
# bands? One frame per variant, the same camera; the variant that loses the stripes names it.
var vp: SubViewport
var scene
func _initialize() -> void:
	var out: String = OS.get_cmdline_user_args()[0]
	vp = SubViewport.new()
	vp.size = Vector2i(900, 520)
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/barrow_full.tscn").instantiate()
	vp.add_child(scene)
	while not scene.ready_done:
		await process_frame
	scene.set_hud_visible(false)
	scene.set_crucible_visible(false)
	scene.knight.visible = false
	scene.park_camera(scene.uv_to_world(-3.6, 10.2, 1.0), 1.0)
	var mound_mat: ShaderMaterial = null
	for mi in scene.nodes["mound"].find_children("*", "MeshInstance3D", true, false):
		if String(mi.name) == "MoundMesh":
			mound_mat = (mi as MeshInstance3D).material_override
	for v in ["all_on", "shadows_off", "ink_off", "soft_bands"]:
		scene.sun.shadow_enabled = v != "shadows_off"
		scene.set_ink(v != "ink_off")
		mound_mat.set_shader_parameter("band_soft", 0.25 if v == "soft_bands" else 0.075)
		for i in 10:
			await process_frame
		RenderingServer.force_draw()
		await process_frame
		vp.get_texture().get_image().save_png("%s/kerb_%s.png" % [out, v])
		print("[probe] ", v)
	quit(0)
