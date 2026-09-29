extends SceneTree
# C-9 D2: what is actually inside each gear GLB?
#
# The manifest declares a bind MODE per piece -- bone, skin, socket -- and a mode is a
# statement about intent. Whether a file carries a Skeleton3D, whether its mesh has a skin,
# and whether its bone names match the body's are facts about the file, and binding a
# skinned mesh as if it were rigid puts a byrnie in the middle of the floor.
const DIR := "res://models/gear/"
const BODY := "res://models/gear/nb-body.glb"

func _initialize():
	var body := (load(BODY) as PackedScene).instantiate()
	root.add_child(body)
	await process_frame
	var bskel: Skeleton3D = null
	for n in body.find_children("*", "Skeleton3D", true, false):
		bskel = n
	var bnames := []
	for i in bskel.get_bone_count():
		bnames.append(bskel.get_bone_name(i))
	print("BODY nb-body.glb: skeleton '%s', %d bones" % [bskel.name, bskel.get_bone_count()])
	for m in body.find_children("*", "MeshInstance3D", true, false):
		var mi := m as MeshInstance3D
		print("  mesh %-14s surfaces %d  blend shapes %d  skin=%s  aabb %s" %
			[mi.name, mi.mesh.get_surface_count(), mi.mesh.get_blend_shape_count(),
			 str(mi.skin != null), str(mi.get_aabb().size.snappedf(0.001))])
		for b in mi.mesh.get_blend_shape_count():
			print("      blend shape %d: '%s'" % [b, mi.mesh.get_blend_shape_name(b)])
	var anim: AnimationPlayer = null
	for n in body.find_children("*", "AnimationPlayer", true, false):
		anim = n
	print("  clips %s" % str(anim.get_animation_list() if anim else []))

	for f in ["helmet", "bracers", "byrnie", "mantle", "axe", "shield"]:
		var p := (load(DIR + f + ".glb") as PackedScene).instantiate()
		root.add_child(p)
		await process_frame
		var sk: Skeleton3D = null
		for n in p.find_children("*", "Skeleton3D", true, false):
			sk = n
		var meshes := p.find_children("*", "MeshInstance3D", true, false)
		var same := "n/a"
		if sk != null:
			var names := []
			for i in sk.get_bone_count():
				names.append(sk.get_bone_name(i))
			same = "IDENTICAL to the body" if names == bnames else "DIFFERENT (%d bones)" % names.size()
		print("")
		print("%s.glb: %d mesh(es), skeleton=%s  bones %s" %
			[f, meshes.size(), str(sk != null), same])
		for m in meshes:
			var mi := m as MeshInstance3D
			var wa: AABB = mi.global_transform * mi.get_aabb()
			print("   %-14s skin=%-5s xform-origin %s  world aabb min %s size %s" %
				[mi.name, str(mi.skin != null),
				 str(mi.global_transform.origin.snappedf(0.001)),
				 str(wa.position.snappedf(0.001)), str(wa.size.snappedf(0.001))])
		p.queue_free()
		await process_frame
	quit(0)
