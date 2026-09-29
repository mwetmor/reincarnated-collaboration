extends SceneTree
# C-9 T7-A: the LIVE 2D H1 view, through a SubViewport that is EXACTLY 1920x1080.
#
# The window is not. Asked for 1920x1080 this Mac returns 1726x971, and the 2D project
# stretches in canvas_items mode, so the whole scene comes back at 0.899 scale -- measured,
# tools/probe_2d_layers.gd: final transform scale (0.898958, 0.899074), which is exactly
# 1726/1920. A side-by-side taken from that window compares a 0.899-scale 2D against a
# 1:1 3D and the difference reads as a projection error. A SubViewport is the size it is
# told to be, and the 3D side already captures through one.
#
#   Godot --path godot --resolution 1920x1080 --script tools/shot_2d_fixed.gd -- --out D

const SHOT := Vector2i(1920, 1080)
const CAM_OFFSET := Vector2(-2, -55)        # the Camera2D hangs off the player by this
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
	var vp := SubViewport.new()
	vp.size = SHOT
	vp.transparent_bg = false
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	vp.add_child(scene)
	var keeper = scene.find_child("Keeper", true, false)
	for i in 30:
		await physics_frame
		await process_frame
	# HIDE EVERYTHING THE PLAYER BRINGS, by sweep rather than by name. The named list the
	# earlier version used left the figure and the HUD band in the reference -- the skin
	# builds its sprite and its CanvasLayer at runtime, so a list written from the .tscn
	# cannot name them. The comparison is of the painted WORLD; a figure only one of the
	# two scenes has is a difference that says nothing.
	var hidden := 0
	for c in keeper.get_children():
		if c is Camera2D:
			continue                      # the camera is how the shot is aimed
		if c is CanvasItem:
			(c as CanvasItem).visible = false
			hidden += 1
		elif c is Node3D:
			(c as Node3D).visible = false
			hidden += 1
	for cl in scene.find_children("*", "CanvasLayer", true, false):
		(cl as CanvasLayer).visible = false
		hidden += 1
	for cl in root.find_children("*", "CanvasLayer", true, false):
		(cl as CanvasLayer).visible = false
	print("  hid %d player-side nodes" % hidden)
	for i in 10:
		await physics_frame
		await process_frame
	for name in SPOTS:
		keeper.global_position = SPOTS[name] - CAM_OFFSET
		for i in 14:
			await physics_frame
			await process_frame
		var img := vp.get_texture().get_image()
		img.save_png("%s/%s_2d.png" % [out, name])
		print("  2D %s at canvas %s -> %s" % [name, str(SPOTS[name]), str(img.get_size())])
	print("[ref2d] -> ", out)
	quit(0)
