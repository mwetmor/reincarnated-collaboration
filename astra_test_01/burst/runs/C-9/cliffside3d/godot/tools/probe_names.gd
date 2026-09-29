extends SceneTree
func _initialize() -> void:
	var vp := SubViewport.new(); vp.size = Vector2i(64, 64); vp.own_world_3d = false
	root.add_child(vp)
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 40: await process_frame
	var names := []
	for m in scene.level.find_children("*", "MeshInstance3D", true, false):
		names.append(String((m as MeshInstance3D).name))
	print("[names] Level meshes (%d): %s" % [names.size(), ", ".join(names)])
	quit(0)
