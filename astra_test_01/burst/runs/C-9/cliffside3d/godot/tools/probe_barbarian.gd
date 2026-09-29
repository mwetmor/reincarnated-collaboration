extends SceneTree
# C-9 R-C9-69: what shape is the barbarian actually in, as GODOT sees him?
#
# The sidecar describes the BLENDER scene -- "feet on z = 0, facing -Y, his right at -X,
# +Z up" -- and glTF is defined Y-up, so a standard export has already converted it. Which
# convention actually reached the file is a measurement, not a reading: a model taken on
# trust and rotated by a guessed 90 deg is a character lying on his back in the deliverable.
#
#   Godot --headless --path godot --script tools/probe_barbarian.gd
const MODEL := "res://models/T8-barbarian.glb"
const SCALE := 1.25178

func _initialize():
	var glb := (load(MODEL) as PackedScene).instantiate()
	root.add_child(glb)
	await process_frame
	var skel: Skeleton3D = null
	var mesh: MeshInstance3D = null
	var anim: AnimationPlayer = null
	for n in glb.find_children("*", "", true, false):
		if n is Skeleton3D: skel = n
		elif n is MeshInstance3D and mesh == null: mesh = n
		elif n is AnimationPlayer: anim = n
	print("mesh  : %s" % (mesh.name if mesh else "NONE"))
	var ab: AABB = mesh.get_aabb()
	print("  aabb min %s  max %s  size %s" %
		[str(ab.position.snappedf(0.001)), str((ab.position + ab.size).snappedf(0.001)),
		 str(ab.size.snappedf(0.001))])
	var tall := "Y" if ab.size.y > maxf(ab.size.x, ab.size.z) else ("Z" if ab.size.z > ab.size.x else "X")
	print("  tallest axis = %s  -> %s" % [tall, "Y-up, as Godot wants" if tall == "Y" else "NOT Y-up: needs a rotation"])
	print("  height %.4f m   x %.4f m across   feet at %s = %.4f" %
		[ab.size.y, ab.size.x, tall, ab.position.y])
	print("  at figure scale %.5f -> %.4f m in the world, %.1f canvas px at 100.6176 px/m x cos(52.95)" %
		[SCALE, ab.size.y * SCALE, ab.size.y * SCALE * 100.617553710938 * 0.602462407085])
	print("skel  : %s   bones %d" % [skel.name if skel else "NONE", skel.get_bone_count() if skel else 0])
	if skel:
		var names := []
		for i in skel.get_bone_count():
			names.append(skel.get_bone_name(i))
		print("  bones: %s" % str(names))
	print("anim  : %s" % (anim.name if anim else "NONE"))
	if anim:
		for c in anim.get_animation_list():
			var a := anim.get_animation(c)
			print("  clip %-10s  %.4f s  (%d frames at 24 fps)  loop=%s" %
				[c, a.length, int(round(a.length * 24.0)), str(a.loop_mode)])
	quit(0)
