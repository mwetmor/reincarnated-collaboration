extends SceneTree
# Is kit 0's silence a first-cast init issue or the kit? Cast three times on kit 0, count bolts + impacts each time.
func wait(n):
	for f in n:
		await process_frame
func _initialize():
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	var cow = null
	for c in scene.get_node("Actors").get_children():
		if c is Sprite2D and c.texture and c.texture.resource_path.find("cow_carcass") >= 0: cow = c
	for t in 3:
		keeper.global_position = cow.global_position + Vector2(-300, -6)
		Input.action_press("move_right"); await wait(3); Input.action_release("move_right"); await wait(30)
		Input.action_press("cast"); await wait(2); Input.action_release("cast")
		var bolts = 0
		var impacts = 0
		for f in 80:
			await process_frame
			for n in scene.get_node("Actors").get_children():
				if n.scene_file_path.find("_bolt") >= 0: bolts += 1
				if n.scene_file_path.find("_impact") >= 0: impacts += 1
		print("cast ", t, " state=", keeper.state, " bolt-frames ", bolts, " impact-frames ", impacts)
		await wait(60)
	quit()
