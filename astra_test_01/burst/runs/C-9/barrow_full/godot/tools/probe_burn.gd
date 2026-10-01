extends SceneTree
## R-C9-118 (c) debug: the heather and stones under a hand-set impact -- the shader term alone. drax.
func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var out := String(args[args.find("--out") + 1])
	var scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)
	while not scene.ready_done:
		await process_frame
	var v = scene.get("veil")
	while v != null and not v.stage_done():
		await process_frame
	scene.set_hud_visible(false)
	for c in scene.get_children():
		if c is CanvasLayer:
			(c as CanvasLayer).visible = false
	var at := Vector3(14.74, 0.0, 8.82)
	scene.park_camera(at, 1.0)
	var hits := 0
	for n in scene.find_children("*", "MultiMeshInstance3D", true, false):
		var m = (n as GeometryInstance3D).material_override
		if m is ShaderMaterial and (m as ShaderMaterial).shader != null and (m as ShaderMaterial).shader.code.contains("fx_imp_at"):
			hits += 1
			if hits == 1:
				var code: String = (m as ShaderMaterial).shader.code
				var i := code.find("BURN AND CRUMBLE")
				print("[burn] code head: ", code.substr(0, 120).replace("\n", " | "))
				print("[burn] at burn: ", code.substr(i - 200, 700).replace("\n", " | "))
				print("[burn] node ", n.get_path(), " instances ", (n as MultiMeshInstance3D).multimesh.instance_count, " first ", (n as MultiMeshInstance3D).global_transform * (n as MultiMeshInstance3D).multimesh.get_instance_transform(0).origin)
	print("[burn] multimeshes with the term: ", hits)
	for age in [0.0, 1.5, 6.0, 12.6]:
		RenderingServer.global_shader_parameter_set("fx_imp0", Vector4(at.x, 0.0, at.z, 3.0))
		RenderingServer.global_shader_parameter_set("fx_imp_age", Vector4(age, 0, 0, 0))
		RenderingServer.global_shader_parameter_set("fx_imp_life", 12.6)
		RenderingServer.global_shader_parameter_set("fx_imp_n", 1.0 if age > 0.0 else 0.0)
		for f in 4:
			await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(out + "_%04.1f.png" % age)
	for n in scene.find_children("Heather_*", "MultiMeshInstance3D", true, false):
		(n as Node3D).visible = false
	for f in 4:
		await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(out + "_noheather.png")
	quit(0)
