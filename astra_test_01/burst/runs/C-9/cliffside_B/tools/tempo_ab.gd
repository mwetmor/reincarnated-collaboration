extends SceneTree
# C-9: show that the knight's walk cadence now matches the Keeper's.
#
# Walks EAST from one spot in B (knight), then toggles and walks east from the SAME
# spot in A (Keeper), recording both halves as one JPG sequence.  Played back, the two
# gaits step at the same rate -- which is the thing Matt reported wrong in v2 and the
# thing a still screenshot cannot show.
#
# Needs a real window and --fixed-fps, same as tools/record_walk.gd:
#   Godot --path . --resolution 1920x1080 --fixed-fps 30 --script tools/tempo_ab.gd
#   REC_OUT, REC_FPS (default 30), REC_SECONDS per half (default 3), REC_POS
#
# Each half also prints the sprite's animation frame index at start and end, so the
# advance is on the record as a NUMBER as well as in the pictures: same elapsed time,
# same frame count advanced, means same cadence.

func _half(keeper, sprite, pos: Vector2, out: String, first: int, count: int) -> int:
	keeper.velocity = Vector2.ZERO
	keeper.global_position = pos
	keeper.state = "idle"
	await physics_frame
	for i in 4:
		await process_frame
	var f0: int = sprite.frame
	Input.action_press("move_right")
	var n := first
	for i in count:
		await process_frame
		await RenderingServer.frame_post_draw
		var img: Image = root.get_texture().get_image()
		if img.get_width() != 1920 or img.get_height() != 1080:
			img.resize(1920, 1080, Image.INTERPOLATE_LANCZOS)
		img.save_jpg(out + "/f_%04d.jpg" % n, 0.92)
		n += 1
	Input.action_release("move_right")
	await physics_frame
	print("   frames %d..%d  anim %s  sprite frame %d -> %d  (12-frame stride at %.3f fps)"
		% [first, n - 1, sprite.animation, f0, sprite.frame,
			sprite.sprite_frames.get_animation_speed(sprite.animation)])
	return n


func _initialize():
	var out := OS.get_environment("REC_OUT")
	var fps := 30
	if OS.get_environment("REC_FPS") != "":
		fps = int(OS.get_environment("REC_FPS"))
	var half := 3.0
	if OS.get_environment("REC_SECONDS") != "":
		half = float(OS.get_environment("REC_SECONDS"))
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
	var keeper_spr = keeper.get_node(^"AnimatedSprite2D")
	var count := int(round(half * fps))

	print("B (knight) walking east:")
	var n: int = await _half(keeper, knight, pos, out, 0, count)
	scene.toggle()
	await physics_frame
	print("A (Keeper) walking east, same spot:")
	n = await _half(keeper, keeper_spr, pos, out, n, count)
	print("tempo_ab: %d frames -> %s" % [n, out])
	quit()
