extends SceneTree
# C-9 D2 re-export: verify the four claims against the files, not the note.
#   five clips on the body / bracers down to two / axe_edge empty present / shield on LeftHand
const DIR := "res://models/gear/"
func _initialize():
	var body := (load(DIR + "nb-body.glb") as PackedScene).instantiate()
	root.add_child(body)
	await process_frame
	var anim: AnimationPlayer = null
	var skel: Skeleton3D = null
	for n in body.find_children("*", "", true, false):
		if n is AnimationPlayer: anim = n
		elif n is Skeleton3D: skel = n
	print("body clips: %s" % str(anim.get_animation_list()))
	for c in anim.get_animation_list():
		var a := anim.get_animation(c)
		print("   %-16s %.4f s (%d frames)  tracks %d" % [c, a.length, int(round(a.length*24.0)), a.get_track_count()])
	var carry := anim.get_animation("shield_carry_L") if anim.has_animation("shield_carry_L") else null
	if carry != null:
		var names := {}
		for i in carry.get_track_count():
			names[String(carry.track_get_path(i).get_concatenated_subnames())] = true
		print("   shield_carry_L touches %d bones: %s" % [names.size(), str(names.keys())])
	for f in ["bracers", "axe", "shield"]:
		var p := (load(DIR + f + ".glb") as PackedScene).instantiate()
		root.add_child(p)
		await process_frame
		var meshes := p.find_children("*", "MeshInstance3D", true, false)
		var others := []
		for n in p.find_children("*", "", true, false):
			if not (n is MeshInstance3D) and not (n is Skeleton3D) and not (n is AnimationPlayer):
				others.append("%s(%s)" % [n.name, n.get_class()])
		print("%-8s meshes %d %s | other nodes: %s" %
			[f, meshes.size(), str(meshes.map(func(m): return m.name)), str(others)])
		# a named empty shows up as a Node3D / BoneAttachment3D; find axe_edge and locate it
		for n in p.find_children("*", "", true, false):
			if String(n.name).to_lower().contains("edge"):
				var n3 := n as Node3D
				print("   FOUND '%s' (%s) at local %s, global %s" %
					[n.name, n.get_class(), str(n3.position.snappedf(0.0001)),
					 str(n3.global_transform.origin.snappedf(0.0001))])
		p.queue_free()
		await process_frame
	quit(0)
