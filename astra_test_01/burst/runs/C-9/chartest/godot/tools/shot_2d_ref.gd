extends SceneTree
# C-9 R-C9-66: the LIVE 2D H1 view at a given canvas point, for the 3D comparison.
# The character is hidden: the comparison is of the painted world, not of a figure that
# only one of the two scenes has.
#
#   Godot --path godot --resolution 1920x1080 --script tools/shot_2d_ref.gd -- --out DIR
#
# The 2D camera is a child of the player at offset (-2,-55), so to centre the view on a
# canvas point the player goes to that point MINUS the offset. Getting this wrong would
# show up as a constant translation between the two captures and could easily be read as
# a projection error, so it is stated rather than tuned away afterwards.
const CAM_OFFSET := Vector2(-2, -55)
const SPOTS := {
	"plateau": Vector2(2285.62, 2407.32),
	"bridge": Vector2(3459.88, 1027.18),
}

func _initialize():
	var out := ProjectSettings.globalize_path("user://ref2d")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out)
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	var keeper = scene.find_child("Keeper", true, false)
	for n in ["AnimatedSprite2D", "KnightSprite", "Knight3D", "ContactShadow"]:
		var c = keeper.get_node_or_null(NodePath(n))
		if c != null:
			c.visible = false
	var hud = keeper.get_node_or_null(^"CharacterSkin")
	if hud != null:
		for cl in hud.find_children("*", "CanvasLayer", true, false):
			(cl as CanvasLayer).visible = false
	for i in 20:
		await physics_frame
	for name in SPOTS:
		keeper.global_position = SPOTS[name] - CAM_OFFSET
		for i in 10:
			await physics_frame
			await process_frame
		root.get_texture().get_image().save_png("%s/%s_2d.png" % [out, name])
		print("  2D %s at canvas %s" % [name, str(SPOTS[name])])
	print("[ref2d] -> ", out)
	quit(0)
