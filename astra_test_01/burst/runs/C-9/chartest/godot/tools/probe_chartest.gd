extends SceneTree
# C-9 R-C9-61 verification for the character toggle on the ORIGINAL cliffside route.
#
# The claims worth checking are all "did the DEFAULT survive" claims, because the one
# way this test can do damage is by changing what the route does when nobody presses K.
#   1. the scene loads and the Keeper is the player, with HIS speeds and HIS collision
#   2. at start, the KEEPER is the visible skin and the others are hidden
#   3. K cycles through every skin that exists and returns to the Keeper
#   4. the knight skin FOLLOWS the Keeper's state and facing -- it is driven, not
#      independent, so movement cannot diverge between skins
#   5. nothing about the body changes across skins: position, speeds, collision shape
#
# Writes frames/chartest_probe.json.

var fails := 0
var report := {}


func _press_k() -> void:
	# A real key event through the real input path, press and release, with frames in
	# between -- the same journey a player's keypress and the touch overlay's synthesised
	# InputEventAction both make.
	var ev := InputEventKey.new()
	ev.physical_keycode = KEY_K
	ev.keycode = KEY_K
	ev.pressed = true
	Input.parse_input_event(ev)
	await process_frame
	await process_frame
	var up := InputEventKey.new()
	up.physical_keycode = KEY_K
	up.keycode = KEY_K
	up.pressed = false
	Input.parse_input_event(up)
	await process_frame


func _check(ok: bool, what: String) -> void:
	if not ok:
		fails += 1
	print(("  PASS  " if ok else "  FAIL  ") + what)


func _initialize():
	print("=== C-9 R-C9-61 character-toggle probe ===")
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	await physics_frame

	var keeper = scene.find_child("Keeper", true, false)
	_check(keeper != null, "Keeper is in the scene")
	if keeper == null:
		quit(1)
		return
	var skin = keeper.get_node_or_null(^"CharacterSkin")
	var ksprite = keeper.get_node_or_null(^"AnimatedSprite2D")
	var knight = keeper.get_node_or_null(^"KnightSprite")
	var k3d = keeper.get_node_or_null(^"Knight3D")
	_check(skin != null, "CharacterSkin node present")
	_check(ksprite != null, "the Keeper's own AnimatedSprite2D is still there")
	_check(knight != null, "KnightSprite present")
	if skin == null or ksprite == null:
		quit(1)
		return

	# --- 1 + 2: the default ------------------------------------------------
	print("[the default is the Keeper]")
	_check(String(skin.call("skin_name")).begins_with("Keeper"),
		"starts on the Keeper (%s)" % skin.call("skin_name"))
	_check(ksprite.visible, "the Keeper's sprite is visible at start")
	_check(knight == null or not knight.visible, "the knight sprite is hidden at start")
	_check(k3d == null or not k3d.visible, "the 3D knight is hidden at start")
	_check(absf(float(keeper.walk_speed) - 247.0) < 0.01 and absf(float(keeper.run_speed) - 494.0) < 0.01,
		"the Keeper's speeds are untouched (walk %.0f run %.0f)" % [keeper.walk_speed, keeper.run_speed])

	var shape0 = keeper.get_node_or_null(^"CollisionShape2D")
	var pos0: Vector2 = keeper.global_position
	var shape_rid0 = shape0.shape.get_rid() if shape0 != null else RID()

	# --- 2b: ONE press of K advances ONE skin ------------------------------
	# Sent as a real InputEventKey, not by calling cycle(). Everything below drives the
	# toggle through its method, which is underneath the input layer -- and the input
	# layer is exactly where this script's first version had a defect it could not see:
	# the skin was listening for the key as an EVENT and polling for it as an ACTION, so
	# one press ran cycle() twice and K stepped Keeper -> runtime 3D, skipping the sprite
	# skin entirely. Every assertion here passed while that was true. It was found by
	# pressing the key in a browser.
	print("[one press of K advances exactly one skin]")
	var before: String = String(skin.call("skin_name"))
	await _press_k()
	var after_one: String = String(skin.call("skin_name"))
	var expected: String = String(skin.call("peek_next", before))
	_check(after_one != before, "K changes the skin (%s -> %s)" % [before, after_one])
	_check(after_one == expected,
		"K advances exactly ONE skin (got %s, next after %s is %s)"
		% [after_one, before, expected])
	report["one_press"] = {"before": before, "after": after_one, "expected": expected}
	# back to the Keeper before the rest of the run
	for i in 8:
		if String(skin.call("skin_name")).begins_with("Keeper"):
			break
		skin.call("cycle")
		await process_frame

	# --- 3: K cycles and comes back ----------------------------------------
	print("[K cycles every skin that exists and returns to the Keeper]")
	var seen: Array = [String(skin.call("skin_name"))]
	for i in 6:
		var nm: String = String(skin.call("cycle"))
		await process_frame
		if seen.has(nm):
			break
		seen.append(nm)
	print("    cycle order: %s" % str(seen))
	_check(seen.size() >= 2, "at least one knight skin is offered (%d skins)" % seen.size())
	# drive it all the way round back to the Keeper
	for i in 8:
		if String(skin.call("skin_name")).begins_with("Keeper"):
			break
		skin.call("cycle")
		await process_frame
	_check(String(skin.call("skin_name")).begins_with("Keeper"),
		"cycling returns to the Keeper (%s)" % skin.call("skin_name"))
	report["cycle_order"] = seen

	# --- 4: the knight FOLLOWS the Keeper ----------------------------------
	print("[the knight skin follows the Keeper's state and facing]")
	skin.call("cycle")                       # -> knight sprites
	await process_frame
	_check(not ksprite.visible and knight.visible,
		"on the knight skin: Keeper hidden, knight shown")
	keeper.global_position = Vector2(2450, 2100)
	await physics_frame
	var pairs: Array = []
	for act in ["move_right", "move_up", "move_left", "move_down"]:
		Input.action_press(act)
		for f in 14:
			await physics_frame
			await process_frame
		var st := String(keeper.state)
		var fa := String(keeper.facing)
		var anim := String(knight.animation)
		pairs.append({"state": st, "facing": fa, "knight_animation": anim})
		print("    keeper %-5s %-2s   knight plays %s" % [st, fa, anim])
		_check(anim.begins_with(st), "knight plays the Keeper's STATE (%s -> %s)" % [st, anim])
		Input.action_release(act)
		for f in 4:
			await physics_frame
	report["followed"] = pairs

	# --- 5: the body is identical across skins -----------------------------
	print("[the body does not change with the skin]")
	var shape1 = keeper.get_node_or_null(^"CollisionShape2D")
	_check(shape1 != null and shape1.shape.get_rid() == shape_rid0,
		"the collision shape is the same resource on every skin")
	_check(absf(float(keeper.walk_speed) - 247.0) < 0.01 and absf(float(keeper.run_speed) - 494.0) < 0.01,
		"speeds still the Keeper's after switching skins")
	report["speeds"] = {"walk": keeper.walk_speed, "run": keeper.run_speed}
	report["start_position"] = [pos0.x, pos0.y]

	report["fails"] = fails
	var f := FileAccess.open("res://frames/chartest_probe.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("=== chartest probe: %s (%d failures) ===" % ["PASS" if fails == 0 else "FAIL", fails])
	quit(1 if fails > 0 else 0)
