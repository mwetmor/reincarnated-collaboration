extends SceneTree
# C-9: record the knight walking a closed octagon loop in style B, as a numbered JPG
# sequence that tools/record_walk.sh muxes into an MP4.
#
# MUST run with a real window (Godot cannot rasterise under --headless) AND with
# --fixed-fps, which pins every frame's delta regardless of how long the readback and
# the JPG encode actually take.  Without it the capture is real-time-coupled: the walk
# animations would advance by the wall-clock cost of saving a frame, and the movie
# would play back at the wrong speed while every individual frame looked correct.
#
#   Godot --path . --resolution 1920x1080 --fixed-fps 30 --script tools/record_walk.gd
#   REC_OUT     frame directory
#   REC_FPS     must match --fixed-fps (default 30)
#   REC_SECONDS total length (default 12 -> 1.5 s per leg)
#   REC_POS     "x,y" loop start (default 2450,2100 -- verified DRIFT 0.00 px by
#               tools/loop_dryrun.gd, so the loop closes without touching collision)
#
# The leg order E SE S SW W NW N NE is a closed octagon with equal legs, so the knight
# shows all EIGHT painted directions -- no mirroring anywhere -- and ends where he began.

const LEGS := [
	[["move_right"], "E"], [["move_right", "move_down"], "SE"],
	[["move_down"], "S"], [["move_left", "move_down"], "SW"],
	[["move_left"], "W"], [["move_left", "move_up"], "NW"],
	[["move_up"], "N"], [["move_right", "move_up"], "NE"],
]


func _initialize():
	var out := OS.get_environment("REC_OUT")
	var fps := 30
	if OS.get_environment("REC_FPS") != "":
		fps = int(OS.get_environment("REC_FPS"))
	var seconds := 12.0
	if OS.get_environment("REC_SECONDS") != "":
		seconds = float(OS.get_environment("REC_SECONDS"))
	var pos := Vector2(2450, 2100)
	if OS.get_environment("REC_POS") != "":
		var xy := OS.get_environment("REC_POS").split(",")
		pos = Vector2(float(xy[0]), float(xy[1]))

	DirAccess.make_dir_recursive_absolute(out)
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	var knight = keeper.get_node(^"KnightSprite")
	keeper.velocity = Vector2.ZERO
	keeper.global_position = pos
	await physics_frame
	var start: Vector2 = keeper.global_position
	var per_leg := int(round(seconds * fps / LEGS.size()))
	print("record: style %s  start %s  %d fps  %d frames/leg  %d frames total"
		% [scene.style_name(), str(start), fps, per_leg, per_leg * LEGS.size()])

	# a couple of settle frames so the first saved frame is not a half-built one
	for i in 6:
		await process_frame

	var n := 0
	for leg in LEGS:
		for a in leg[0]:
			Input.action_press(a)
		for f in per_leg:
			await process_frame
			await RenderingServer.frame_post_draw
			var img: Image = root.get_texture().get_image()
			if img.get_width() != 1920 or img.get_height() != 1080:
				img.resize(1920, 1080, Image.INTERPOLATE_LANCZOS)
			img.save_jpg(out + "/f_%04d.jpg" % n, 0.92)
			n += 1
		for a in leg[0]:
			Input.action_release(a)
		print("  leg %-3s -> %s  at %s  playing %s"
			% [leg[1], keeper.facing, str(keeper.global_position), knight.animation])
		await physics_frame

	print("record: %d frames -> %s   end %s   DRIFT %.2f px"
		% [n, out, str(keeper.global_position), start.distance_to(keeper.global_position)])
	quit()
