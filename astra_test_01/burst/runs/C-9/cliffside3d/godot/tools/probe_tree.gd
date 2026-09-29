extends SceneTree
func _initialize():
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60: await process_frame
	var k = scene.knight
	var tree: AnimationTree = k._tree
	var anim: AnimationPlayer = k._anim
	var skel: Skeleton3D = k._skel
	print("tree active=%s  anim_player=%s  root_node=%s" % [tree.active, tree.anim_player, tree.root_node])
	print("  tree resolves anim_player -> %s" % str(tree.get_node_or_null(tree.anim_player)))
	print("  tree resolves root_node   -> %s" % str(tree.get_node_or_null(tree.root_node)))
	print("  anim.root_node=%s -> %s" % [anim.root_node, str(anim.get_node_or_null(anim.root_node))])
	print("  anim.active=%s  player libs=%s" % [anim.active, str(anim.get_animation_library_list())])
	print("  tree animation list=%s" % str(tree.get_animation_list()))
	print("  parameters/base/animation = %s" % str(tree.get("parameters/base/animation")))
	print("  parameters/blend/blend_amount = %s" % str(tree.get("parameters/blend/blend_amount")))
	var hand := skel.find_bone("LeftHand")
	var toe := skel.find_bone("LeftToeBase")
	tree.set("parameters/base/animation", "walk")
	tree.set("parameters/blend/blend_amount", 0.0)
	var seen := []
	for i in 12:
		await physics_frame
		seen.append(snappedf(skel.get_bone_global_pose(toe).origin.y, 0.01))
	print("  with the TREE driving, LeftToeBase y over 12 physics frames: %s" % str(seen))
	tree.active = false
	anim.active = true
	anim.play("walk")
	var seen2 := []
	for i in 12:
		await physics_frame
		seen2.append(snappedf(skel.get_bone_global_pose(toe).origin.y, 0.01))
	print("  with the PLAYER driving, same bone:                        %s" % str(seen2))
	quit(0)
