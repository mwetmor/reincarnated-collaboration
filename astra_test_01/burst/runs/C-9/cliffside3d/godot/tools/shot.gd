extends SceneTree
# C-9 R-C9-66: capture the 3D cliffside from the game camera.
#
#   Godot --path godot --resolution 1920x1080 --script tools/shot.gd -- --v4 [--out DIR]
#
# Needs a real window: --headless gives the dummy renderer and every viewport texture
# comes back null.

const SPOTS := {
	"plateau": Vector2(2285.62, 2407.32),   # the spawn; the builder's plateau proxy
	"bridge": Vector2(3459.88, 1027.18),    # midway between the two abutment decks
}

var out_dir := ""


func _initialize():
	out_dir = ProjectSettings.globalize_path("user://shots")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir)

	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 12:
		await process_frame
	print("[shot] out -> ", out_dir)

	for name in SPOTS:
		scene.look_at_canvas(SPOTS[name])
		await process_frame
		await process_frame
		root.get_texture().get_image().save_png("%s/%s_plate.png" % [out_dir, name])
		# the same frame with the painting off, so the geometry under it is visible
		scene.set_plate(false)
		await process_frame
		await process_frame
		root.get_texture().get_image().save_png("%s/%s_grey.png" % [out_dir, name])
		scene.set_plate(true)
		# and with uncovered geometry flagged, for the coverage report
		scene.show_void(true)
		await process_frame
		await process_frame
		root.get_texture().get_image().save_png("%s/%s_void.png" % [out_dir, name])
		scene.show_void(false)
		print("  %s captured" % name)
	quit(0)
