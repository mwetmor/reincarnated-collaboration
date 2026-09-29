extends SceneTree
# T9-0: how big is the world next to a 1.85 m man? Names and world sizes of the foreground
# meshes, and the props' own card heights, so "too large" can be a number.
const PPM := 100.617553710938
const PITCH_COS := 0.602462407085
func _initialize():
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60: await process_frame
	print("FOREGROUND MESHES, world AABB in metres:")
	for mi in scene._fg:
		var ab: AABB = (mi as MeshInstance3D).global_transform * (mi as MeshInstance3D).get_aabb()
		print("   %-26s size %7.2f x %7.2f x %7.2f" % [mi.name, ab.size.x, ab.size.y, ab.size.z])
	print("")
	print("PROP CARDS, world size in metres (w = px/PPM, h = px/PPM/cos(pitch)):")
	var props = scene.get_node_or_null(^"Props")
	for n in ["bridge_post_1", "bridge_post_0", "tree_living_a", "stump_a", "rock_a", "cache_crates_barrel"]:
		for c in props.get_children():
			if (c as MeshInstance3D).name == n:
				var q := (c as MeshInstance3D).mesh as QuadMesh
				print("   %-22s %.3f w x %.3f h" % [n, q.size.x, q.size.y])
	quit(0)
