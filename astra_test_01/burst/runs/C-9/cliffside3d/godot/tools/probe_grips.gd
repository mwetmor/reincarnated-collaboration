extends SceneTree
# Are the grip morphs actually driven, and by the right piece? The stills are framed through
# a mantle; a blend-shape value is not.
func _initialize():
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60: await process_frame
	var k = scene.knight
	var m: MeshInstance3D = k._mesh
	var names := []
	for i in m.mesh.get_blend_shape_count(): names.append(m.mesh.get_blend_shape_name(i))
	print("morphs on the body: %s" % str(names))
	print("rules: %s" % JSON.stringify(k.cfg.get("morph_rules", {})))
	for s in k.gear_stack_count():
		k.set_gear_stack(s)
		await process_frame
		var vals := {}
		for i in m.mesh.get_blend_shape_count():
			vals[String(m.mesh.get_blend_shape_name(i))] = snappedf(m.get_blend_shape_value(i), 0.01)
		print("  stack %d %-42s %s" % [s, str(k.cfg["gear_stacks"][s]), JSON.stringify(vals)])
	quit(0)
