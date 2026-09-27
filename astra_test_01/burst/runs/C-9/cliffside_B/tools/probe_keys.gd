extends SceneTree
# C-9 probe R-C9-34: press the ACTUAL KEYS.  scene.toggle_rig() working is not the same
# claim as "G does it": G is also bound to gear_toggle (keeper.gd), so this drives the
# real input path -- Input.parse_input_event -> _unhandled_input -> style_toggle.gd --
# and checks that one key press moves exactly one thing.
var fails := 0

func _check(ok: bool, what: String) -> void:
	if not ok:
		fails += 1
	print(("  PASS  " if ok else "  FAIL  ") + what)

func _key(code: int) -> void:
	var e := InputEventKey.new()
	e.physical_keycode = code
	e.pressed = true
	Input.parse_input_event(e)
	await process_frame
	await physics_frame
	var u := InputEventKey.new()
	u.physical_keycode = code
	u.pressed = false
	Input.parse_input_event(u)
	await process_frame
	await physics_frame

func _initialize():
	print("=== C-9 key probe: T and G ===")
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	await process_frame
	var keeper = scene.find_child("Keeper", true, false)
	var knight = keeper.get_node(^"KnightSprite")
	var keeper_spr = keeper.get_node(^"AnimatedSprite2D")
	var base_frames = keeper_spr.sprite_frames

	# face E so the rig is the thing G changes
	Input.action_press("move_right")
	for f in 20:
		await physics_frame
		await process_frame
	Input.action_release("move_right")
	await physics_frame
	await process_frame
	_check(String(keeper.facing) == "E", "facing E")

	print("[G in style B]")
	_check(scene.style_name() == "B" and scene.rig_mode() == "RIG", "start: style B, E = RIG")
	await _key(71)      # G
	_check(scene.rig_mode() == "GROK", "G -> E = GROK (%s)" % scene.rig_mode())
	_check(keeper_spr.sprite_frames == base_frames,
		"G did NOT also swap the Keeper's gear frames while the knight is worn")
	await _key(71)
	_check(scene.rig_mode() == "RIG", "G -> E = RIG (%s)" % scene.rig_mode())

	print("[T]")
	await _key(84)      # T
	_check(scene.style_name() == "A", "T -> style A (%s)" % scene.style_name())
	_check(keeper_spr.visible and not knight.visible, "player sprite is the Keeper in A")
	await _key(84)
	_check(scene.style_name() == "B", "T -> style B (%s)" % scene.style_name())
	_check(knight.visible and not keeper_spr.visible, "player sprite is the knight in B")
	_check(scene.rig_mode() == "RIG", "rig mode survived the style round trip (%s)" % scene.rig_mode())

	print("[G's other binding]")
	# G is also project.godot's gear_toggle, which keeper.gd uses to swap the Keeper to
	# frames/keeper_advanced.tres.  THAT FILE IS NOT IN THIS BUILD, so the gear toggle
	# has always been inert here and G was a free key before this probe took it.  The
	# guard added to keeper.gd (only swap while the Keeper is the visible sprite) is
	# therefore belt-and-braces, not a fix for a live collision -- stated here so the
	# next reader does not go looking for a bug that the missing file explains.
	var has_advanced := ResourceLoader.exists("res://frames/keeper_advanced.tres")
	print("    frames/keeper_advanced.tres present: %s" % str(has_advanced))
	await _key(84)      # -> A
	await _key(71)      # G with the Keeper visible
	if has_advanced:
		_check(keeper_spr.sprite_frames != base_frames,
			"in A, G still swaps the Keeper's gear frames")
	else:
		_check(keeper_spr.sprite_frames == base_frames,
			"in A, G changes nothing -- gear_toggle has no advanced frames in this build")
	await _key(84)      # back to B

	print("[Shift = run]")
	# Shift is project.godot's run_modifier. The claim is that it now reaches the
	# knight's OWN painted run cells rather than the old run->walk mapping.
	Input.action_press("move_right")
	for f in 16:
		await physics_frame
		await process_frame
	_check(String(knight.animation) == "walk_E",
		"walking east plays walk_E (%s)" % knight.animation)
	Input.action_press("run_modifier")
	for f in 16:
		await physics_frame
		await process_frame
	_check(String(keeper.state) == "run", "Keeper state is run (%s)" % keeper.state)
	_check(String(knight.animation) == "run_E",
		"Shift plays the knight's painted run_E, not walk_E (%s)" % knight.animation)
	Input.action_release("run_modifier")
	Input.action_release("move_right")
	await physics_frame
	await process_frame
	# and the un-painted direction falls back along the STATE
	Input.action_press("move_left")
	Input.action_press("run_modifier")
	for f in 20:
		await physics_frame
		await process_frame
	_check(String(keeper.facing) == "W", "facing W (%s)" % keeper.facing)
	_check(String(knight.animation) == "walk_W",
		"W has no painted run, so it falls back to walk_W -- not to another direction (%s)"
		% knight.animation)
	Input.action_release("run_modifier")
	Input.action_release("move_left")
	await physics_frame

	print("=== key probe: %s (%d failures) ===" % ["PASS" if fails == 0 else "FAIL", fails])
	quit(1 if fails > 0 else 0)
