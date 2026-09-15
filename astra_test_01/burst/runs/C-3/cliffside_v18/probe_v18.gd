extends SceneTree
# Conductor proof v16: six self-authored kits in the picker; cycle Tab, cast each east into the cow, count impacts, screenshot mid-impact.
var out_dir = OS.get_environment("PROBE_OUT")
func shot(n):
	root.get_texture().get_image().save_png(out_dir + "/" + n + ".png")
func wait(n):
	for f in n:
		await process_frame
func _initialize():
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	var label = scene.find_child("Label", true, false)
	var cow = null
	for c in scene.get_node("Actors").get_children():
		if c is Sprite2D and c.texture and c.texture.resource_path.find("cow_carcass") >= 0: cow = c
	print("shadows ", scene.get_node("Shadows").get_child_count())
	keeper.global_position = cow.global_position + Vector2(-300, -6)
	Input.action_press("cast"); await wait(2); Input.action_release("cast"); await wait(90)
	for k in 6:
		keeper.global_position = cow.global_position + Vector2(-300, -6)
		Input.action_press("move_right"); await wait(3); Input.action_release("move_right"); await wait(30)
		var name = label.text
		Input.action_press("cast"); await wait(2); Input.action_release("cast")
		await wait(10); shot("v18_%d_travel" % k)
		var impacts = 0
		var shot_done = false
		for f in 80:
			await process_frame
			for n in scene.get_node("Actors").get_children():
				if n.scene_file_path.find("_impact") >= 0: impacts += 1
			if impacts >= 3 and not shot_done:
				shot("v18_%d_impact" % k); shot_done = true
		print("kit ", k, " ", name, " impact-frames ", impacts)
		Input.action_press("vfx_cycle"); await wait(2); Input.action_release("vfx_cycle"); await wait(2)
	quit()
