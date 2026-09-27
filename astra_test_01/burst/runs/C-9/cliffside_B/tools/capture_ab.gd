extends SceneTree
# C-9: capture the SAME camera framing and the SAME player position in both registers.
# Needs a real window (Godot cannot rasterise under --headless), so run it WITHOUT
# --headless:
#   Godot --path . --resolution 1920x1080 --script tools/capture_ab.gd
#
#   CAP_OUT  output directory
#   CAP_POS  "x,y" canvas position to stand the player on (default: the bridge's west
#            landing, 3040,1390 -- the whole span is then in frame up and to the right)
#
# Four shots, one position, one camera:
#   C-9_cliffside_B_knight_standing.png   knight idle by the bridge
#   C-9_cliffside_B_knight_walking.png    knight mid-stride, input STILL HELD -- the
#                                         animation must be sampled while walking;
#                                         keeper.gd drops to idle one frame after release
#   C-9_cliffside_A_keeper_standing.png   same spot, H1 register
#   C-9_cliffside_A_keeper_walking.png

var _keeper
var _scene


func _shot(path: String, note: String) -> void:
	await RenderingServer.frame_post_draw
	var img: Image = root.get_texture().get_image()
	if img.get_width() != 1920 or img.get_height() != 1080:
		img.resize(1920, 1080, Image.INTERPOLATE_LANCZOS)
	var err := img.save_png(path)
	print("capture %-52s %dx%d err=%d  %s"
		% [path.get_file(), img.get_width(), img.get_height(), err, note])


func _settle(n: int) -> void:
	for i in n:
		await process_frame


func _place(pos: Vector2) -> void:
	_keeper.velocity = Vector2.ZERO
	_keeper.global_position = pos
	_keeper.state = "idle"
	await physics_frame
	await physics_frame


func _shoot_pair(prefix: String, pos: Vector2, sprite) -> void:
	await _place(pos)
	await _settle(24)
	await _shot(prefix + "_standing.png",
		"at %s  playing %s" % [str(_keeper.global_position), sprite.animation])
	# walk NE, toward the span, and shoot with the key still down
	Input.action_press("move_up")
	Input.action_press("move_right")
	for i in 26:
		await process_frame
	await _shot(prefix + "_walking.png",
		"at %s  facing %s  playing %s  frame %d"
		% [str(_keeper.global_position), _keeper.facing, sprite.animation, sprite.frame])
	Input.action_release("move_up")
	Input.action_release("move_right")
	await physics_frame


func _initialize():
	var out := OS.get_environment("CAP_OUT")
	var pos_env := OS.get_environment("CAP_POS")
	var pos := Vector2(3040, 1390)
	if pos_env != "":
		var parts := pos_env.split(",")
		if parts.size() == 2:
			pos = Vector2(float(parts[0]), float(parts[1]))
	_scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(_scene)
	await physics_frame
	_keeper = _scene.find_child("Keeper", true, false)
	var knight = _keeper.get_node(^"KnightSprite")
	var keeper_spr = _keeper.get_node(^"AnimatedSprite2D")
	print("style ", _scene.style_name(), "  target position ", pos)

	await _shoot_pair(out + "/C-9_cliffside_B_knight", pos, knight)

	var swapped: int = _scene.toggle()
	print("toggled -> ", _scene.style_name(), "  textures swapped ", swapped)
	await _shoot_pair(out + "/C-9_cliffside_A_keeper", pos, keeper_spr)

	quit()
