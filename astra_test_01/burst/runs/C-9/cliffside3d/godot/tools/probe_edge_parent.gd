extends SceneTree
# Where does axe_edge hang? Recreating it on the body needs its parent and local transform,
# and "next to a BoneAttachment3D in a printed list" is not the same as "a child of it".
func _initialize():
	var p := (load("res://models/gear/axe.glb") as PackedScene).instantiate()
	root.add_child(p)
	await process_frame
	for n in p.find_children("*", "", true, false):
		var par := n.get_parent()
		print("%-28s %-22s parent %s" % [n.name, n.get_class(), par.name if par else "-"])
		if String(n.name) == "axe_edge":
			var n3 := n as Node3D
			print("    local  %s" % str(n3.transform))
			print("    global %s" % str(n3.global_transform.origin.snappedf(0.0001)))
	quit(0)
