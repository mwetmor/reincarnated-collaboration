extends SceneTree
# Conductor proof v11 (R-C3-101): no orphan glow/emitter left of the bridge (~2927,1086); extracted shadows restored (7 shadow sprites incl. cow); screenshots.
var out_dir = OS.get_environment("PROBE_OUT")
func shot(n):
	root.get_texture().get_image().save_png(out_dir + "/" + n + ".png")
func _initialize():
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	var shadows = scene.get_node("Shadows")
	var orphan = 0
	var glows = 0
	for n in scene.get_node("Actors").get_children():
		if n is PointLight2D or n is Sprite2D and n.material is CanvasItemMaterial and n.material.blend_mode == CanvasItemMaterial.BLEND_MODE_ADD:
			glows += 1
			if n.global_position.distance_to(Vector2(2927, 1086)) < 60: orphan += 1
	for n in scene.get_children():
		if n is GPUParticles2D or n is CPUParticles2D:
			if n.global_position.distance_to(Vector2(2927, 1086)) < 60: orphan += 1
	var sh = []
	for s in shadows.get_children():
		sh.append([s.name, s.modulate.a, s.global_position.x, s.global_position.y])
	print("shadows ", shadows.get_child_count(), " ", sh)
	print("add-blend glows ", glows, " orphan near (2927,1086): ", orphan)
	for v in [["spawn", Vector2(2285.62, 2407.32)], ["bridge_left", Vector2(2900, 1150)], ["cow", Vector2(4000, 700)], ["south", Vector2(1900, 3450)]]:
		keeper.global_position = v[1]
		for f in 40:
			await process_frame
		shot("v11_" + v[0])
	quit()
