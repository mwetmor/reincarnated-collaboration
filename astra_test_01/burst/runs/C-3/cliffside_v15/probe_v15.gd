extends SceneTree
# Conductor proof v15 (no shadows; Frozen Orb v2): Frozen Orb kit first in the picker; cast east into the cow (collision → impact), cast north; timed screenshots.
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
	print("label ", label.text if label else "none", " shadows ", scene.get_node("Shadows").get_child_count() if scene.has_node("Shadows") else -1)
	var cow = null
	for c in scene.get_node("Actors").get_children():
		if c is Sprite2D and c.texture and c.texture.resource_path.find("cow_carcass") >= 0: cow = c
	keeper.global_position = cow.global_position + Vector2(-300, -6)
	Input.action_press("move_right"); await wait(3); Input.action_release("move_right"); await wait(20)
	Input.action_press("cast"); await wait(2); Input.action_release("cast")
	await wait(6); shot("v15_fo_cast")
	await wait(14); shot("v15_fo_travel")
	var impacts = 0
	for f in 90:
		await process_frame
		for n in scene.get_node("Actors").get_children():
			if n.scene_file_path.find("frozen_orb_v2_impact") >= 0: impacts += 1
		if impacts in [1, 3, 5, 7, 9, 11, 13, 15]: shot("v15_fo_impact_%02d" % impacts)
	print("impact nodes seen (frame-sum) ", impacts)
	keeper.global_position = Vector2(2285.62, 2407.32)
	Input.action_press("move_up"); await wait(3); Input.action_release("move_up"); await wait(20)
	Input.action_press("cast"); await wait(2); Input.action_release("cast")
	await wait(24); shot("v15_fo_north")
	var bolts = 0
	for n in scene.get_node("Actors").get_children():
		if n.scene_file_path.find("frozen_orb_v2_bolt") >= 0:
			bolts += 1
			print("bolt rotation ", n.rotation_degrees, " scale ", n.scale, " pos ", n.global_position)
	print("bolts alive ", bolts)
	quit()
