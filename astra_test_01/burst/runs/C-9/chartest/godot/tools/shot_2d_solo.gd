extends SceneTree
# C-9 T7-A: render the live 2D with ONE parallax layer and nothing else.
#
# get_global_transform_with_canvas() on a Parallax2D's child sprite gave a screen position
# that reproduced a closed-form law to the last decimal, at four camera points -- and the
# composite it predicts does not match the picture the 2D actually draws. So the transform
# is not the whole story of where Parallax2D puts its texture. One layer alone, over an
# empty scene, is: whatever is on the screen IS where that layer is, and the offset can be
# recovered from the pixels instead of from the node.
#
#   Godot --path godot --resolution 1920x1080 --script tools/shot_2d_solo.gd -- --out D

const SHOT := Vector2i(1920, 1080)
const CAM_OFFSET := Vector2(-2, -55)
const SPOT := Vector2(3459.88, 1027.18)      # the bridge
const LAYERS := ["Layer_sky", "Layer_far_ruins", "Layer_forest_valley", "Layer_mist"]


func _initialize():
	var out := ProjectSettings.globalize_path("user://ref2d")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out)
	var vp := SubViewport.new()
	vp.size = SHOT
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	vp.add_child(scene)
	var keeper = scene.find_child("Keeper", true, false)
	for i in 30:
		await physics_frame
		await process_frame
	keeper.global_position = SPOT - CAM_OFFSET
	for cl in scene.find_children("*", "CanvasLayer", true, false):
		(cl as CanvasLayer).visible = false
	for i in 12:
		await physics_frame
		await process_frame
	for target in LAYERS:
		for c in scene.get_children():
			if c is CanvasItem:
				(c as CanvasItem).visible = (String(c.name) == target)
		for i in 8:
			await process_frame
		vp.get_texture().get_image().save_png("%s/solo_%s.png" % [out, target])
		print("  solo %s" % target)
	print("[solo] -> ", out)
	quit(0)
