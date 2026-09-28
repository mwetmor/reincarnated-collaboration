extends SceneTree
# C-9 R-C9-61: capture all three character states in the ORIGINAL cliffside scene, and
# measure the frame rate of each.
#
# Needs a real window -- run WITHOUT --headless, or the renderer is the dummy one and
# every viewport texture comes back null.  (It does, and the null reads as "the 3D render
# is empty", which sounds like a broken model rather than a missing renderer.)
#
# Each skin gets two frames: the whole 1920x1080 view, so the figure can be judged at the
# size a player sees, and a 3x inset around the player, so the ink line and the pollaxe
# can be judged at all.  A 1.1 px line is invisible in a full-frame screenshot; a capture
# that cannot resolve the thing being reviewed is not evidence about it.
#
# FRAME RATE is measured with vsync OFF and no fps cap. With vsync on, all three skins
# report 60 and the measurement says nothing except that the display is 60 Hz -- which is
# the shape of a check that runs, returns cleanly, and answers a different question.

const OUT := "user://shots"
const WARM := 40                 # frames to settle before measuring or shooting
const MEASURE_FRAMES := 240
const INSET := 3
const INSET_SRC := Vector2i(300, 300)

var report := {}


func _initialize():
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	Engine.max_fps = 0
	DirAccess.make_dir_recursive_absolute(OUT)

	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	var keeper = scene.find_child("Keeper", true, false)
	var skin = keeper.get_node_or_null(^"CharacterSkin")
	var k3 = keeper.get_node_or_null(^"Knight3D")
	if skin == null:
		print("FAIL: no CharacterSkin")
		quit(1)
		return
	for i in WARM:
		await physics_frame
	report["spawn"] = [keeper.global_position.x, keeper.global_position.y]
	report["resolution"] = [root.size.x, root.size.y]
	report["skins"] = []

	var walking := false
	for pass_i in 2:
		# Pass 0 standing, pass 1 walking east: a standing figure says nothing about the
		# gait, and a walking one hides the silhouette behind its own motion.
		walking = pass_i == 1
		if walking:
			Input.action_press("move_right")
		for idx in 3:
			_select(skin, idx)
			for i in WARM:
				await physics_frame
				await process_frame
			var name_now: String = String(skin.call("skin_name"))
			var tag := "%d_%s%s" % [idx, _slug(name_now), "_walk" if walking else "_stand"]

			var img := root.get_texture().get_image()
			img.save_png(OUT + "/%s_full.png" % tag)
			_inset(img, keeper).save_png(OUT + "/%s_inset.png" % tag)

			var fps := await _measure()
			var row := {"index": idx, "skin": name_now, "walking": walking,
						"fps": fps, "full": "%s_full.png" % tag,
						"inset": "%s_inset.png" % tag}
			if idx == 2 and k3 != null:
				row["knight3d"] = k3.call("status")
			report["skins"].append(row)
			print("  %-28s %-6s  %6.1f fps   -> %s" % [name_now,
				"walk" if walking else "stand", fps, tag])
		if walking:
			Input.action_release("move_right")

	# Back to the default, and check it: the capture must not be the thing that leaves
	# the scene on a test skin.
	for i in 6:
		_select(skin, 0)
		await process_frame
	report["ends_on"] = String(skin.call("skin_name"))
	var f := FileAccess.open("user://chartest_shots.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("shots in ", ProjectSettings.globalize_path(OUT))
	print("ends on: ", report["ends_on"])
	quit(0)


func _slug(s: String) -> String:
	var out := ""
	for c in s.to_lower():
		out += c if (c >= "a" and c <= "z") or (c >= "0" and c <= "9") else ""
	return out


func _select(skin, idx: int) -> void:
	# cycle() is the only way in, so drive it round rather than reaching for the enum --
	# this then also exercises the path the K key takes.
	for i in 6:
		var n: String = String(skin.call("skin_name"))
		if (idx == 0 and n.begins_with("Keeper")) \
			or (idx == 1 and n.find("sprites") >= 0) \
			or (idx == 2 and n.find("3D") >= 0):
			return
		skin.call("cycle")


func _inset(img: Image, keeper) -> Image:
	var xf: Transform2D = keeper.get_viewport().get_canvas_transform()
	var at: Vector2 = xf * keeper.global_position
	var r := Rect2i(int(at.x) - INSET_SRC.x / 2, int(at.y) - int(INSET_SRC.y * 0.72),
					INSET_SRC.x, INSET_SRC.y)
	r = r.intersection(Rect2i(Vector2i.ZERO, img.get_size()))
	var cut := img.get_region(r)
	cut.resize(r.size.x * INSET, r.size.y * INSET, Image.INTERPOLATE_NEAREST)
	return cut


func _measure() -> float:
	var t0 := Time.get_ticks_usec()
	for i in MEASURE_FRAMES:
		await process_frame
	var dt := float(Time.get_ticks_usec() - t0) / 1e6
	return 0.0 if dt <= 0.0 else float(MEASURE_FRAMES) / dt
