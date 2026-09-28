extends SceneTree
# C-9 R-C9-61: do all three skins STAND THE SAME HEIGHT on screen?
#
# Matt: "Is the keeper larger?" She was -- by 16% -- because the knight skins were
# registered with HER cell scale (0.629167) while their cells hold a 200 px figure and
# hers holds 238.75. The rule of record (cliffside_B/frames/knight_fit.json) is that
# every player figure is 150.2135 canvas px crown-to-sole.
#
# MEASURED ON A PLAYER-VIEW CAPTURE, not in cell space. A cell-space check would have
# caught this particular bug, but only this one: everything between the cell and the
# screen -- node scale, parent scale, camera zoom, offset -- is exactly where a size
# error can hide, and the player sees the end of that chain, not the start.
#
# The figure is isolated by DIFFERENCING against a frame with every skin hidden, so no
# assumption about the background is needed. Thin props are split off by row width, the
# same instrument the builder uses, validated against the Keeper's published 238.75.
#
# Needs a real window (no --headless).

const SETTLE := 26
const ROW_MIN_CANVAS_PX := 5     # 8 cell px x ~0.63-0.75 scale; a staff, not a torso
const DIFF := 26                 # per-channel, against the background-only frame
const TOLERANCE_PX := 2.0
const RULE_PX := 150.2135416666667

var fails := 0
var report := {"note": "C-9 R-C9-61 on-screen figure height", "rule_px": RULE_PX, "rows": []}


func _check(ok: bool, what: String) -> void:
	if not ok:
		fails += 1
	print(("  PASS  " if ok else "  FAIL  ") + what)


func _initialize():
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	var keeper = scene.find_child("Keeper", true, false)
	var skin = keeper.get_node_or_null(^"CharacterSkin")
	if skin == null:
		print("FAIL: no CharacterSkin")
		quit(1)
		return
	# The contact shadow sits under the feet and belongs to no skin; it would add the
	# same few rows to every measurement, which is harmless for the COMPARISON and
	# wrong for the absolute number the rule is stated in.
	var shadow = keeper.get_node_or_null(^"ContactShadow")
	if shadow != null:
		shadow.visible = false
	for i in SETTLE:
		await physics_frame

	var nodes := {
		"Keeper": keeper.get_node_or_null(^"AnimatedSprite2D"),
		"Knight sprites": keeper.get_node_or_null(^"KnightSprite"),
		"Knight 3D": keeper.get_node_or_null(^"Knight3D"),
	}
	for facing in ["S", "E"]:
		# Face, then STAND: the rule is stated for a standing pose, and a walk frame
		# mid-stride reads shorter (legs split, hip dropped, planted sole unchanged).
		var key := "move_down" if facing == "S" else "move_right"
		Input.action_press(key)
		for i in 14:
			await physics_frame
		Input.action_release(key)
		for i in SETTLE:
			await physics_frame
			await process_frame

		# Each skin is SELECTED through the toggle, not just made visible. The 3D skin's
		# SubViewport sits on UPDATE_DISABLED until set_active() runs -- that is
		# deliberate, so the Keeper never pays for a 3D render nobody asked for -- so
		# setting .visible alone composites a viewport that is not drawing anything.
		# It measured 0.0 px and read as a missing character.
		var heights := {}
		var order := ["Keeper", "Knight sprites", "Knight 3D"]
		for k in order:
			if nodes[k] == null:
				continue
			await _select(skin, order.find(k))
			# Split the haft off the 3D knight's silhouette, keeping his pose. The rule
			# is a CROWN-to-sole; a pollaxe clears the helm, and including it measured
			# 180 px at S and 163 at E -- a 17 px swing between directions that is the
			# haft's projected length changing with azimuth, not the knight's height.
			var k3 = keeper.get_node_or_null(^"Knight3D")
			if k3 != null:
				k3.call("set_weapon_visible", k != "Knight 3D")
			for i in 8:
				await physics_frame
				await process_frame
			var img := root.get_texture().get_image()
			nodes[k].visible = false
			await process_frame
			await process_frame
			var bg := root.get_texture().get_image()
			nodes[k].visible = true
			var h := _figure_height(bg, img) / _canvas_scale()
			heights[k] = h
			print("  %-16s %s  crown-to-sole %6.1f canvas px" % [k, facing, h])
		var k3b = keeper.get_node_or_null(^"Knight3D")
		if k3b != null:
			k3b.call("set_weapon_visible", true)
		await _select(skin, 0)
		await process_frame

		var ref: float = float(heights.get("Keeper", 0.0))
		report["rows"].append({"facing": facing, "heights": heights, "keeper": ref})
		_check(absf(ref - RULE_PX) <= 6.0,
			"%s: the Keeper matches the rule of record (%.1f vs %.1f px)" % [facing, ref, RULE_PX])
		for k in ["Knight sprites", "Knight 3D"]:
			if not heights.has(k):
				continue
			_check(absf(float(heights[k]) - ref) <= TOLERANCE_PX,
				"%s: %s stands the Keeper's height (%.1f vs %.1f, delta %+.1f px, max %.0f)"
				% [facing, k, heights[k], ref, float(heights[k]) - ref, TOLERANCE_PX])

	report["fails"] = fails
	var f := FileAccess.open("user://size_probe.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("=== on-screen figure height: %s (%d failures) ===" % ["PASS" if fails == 0 else "FAIL", fails])
	quit(1 if fails > 0 else 0)


func _canvas_scale() -> float:
	"""Screen pixels per CANVAS pixel.

	The rule is stated in canvas px (150.2135) and a capture is in screen px. With the
	project stretching a 1920-wide canvas into a 1600-wide window those differ by
	0.8333 -- and 150.2135 x 0.8333 = 125.2, which is exactly what the Keeper measured
	when this probe first ran and declared her in breach of a rule she defines. The
	reference was right and the ruler was in the wrong units.
	"""
	var s: float = root.get_final_transform().get_scale().y
	return 1.0 if s <= 0.0 else s


func _select(skin, idx: int) -> void:
	for i in 8:
		var n: String = String(skin.call("skin_name"))
		if (idx == 0 and n.begins_with("Keeper")) \
			or (idx == 1 and n.find("sprites") >= 0) \
			or (idx == 2 and n.find("3D") >= 0):
			return
		skin.call("cycle")
		await process_frame


func _figure_height(bg: Image, img: Image) -> float:
	"""Crown-to-sole of whatever appeared between the two frames, props split off."""
	if bg.get_format() != Image.FORMAT_RGBA8:
		bg.convert(Image.FORMAT_RGBA8)
	if img.get_format() != Image.FORMAT_RGBA8:
		img.convert(Image.FORMAT_RGBA8)
	var a := bg.get_data()
	var b := img.get_data()
	var w := img.get_width()
	var h := img.get_height()
	# Only look near the player. The camera follows with a known offset, so the figure
	# is at a predictable place; a whole-frame diff would also collect flies, flicker
	# and any VFX that moved between the two captures.
	var cx := w / 2 + 2
	var cy := h / 2 + 55
	var x0: int = maxi(0, cx - 180)
	var x1: int = mini(w, cx + 180)
	var y0: int = maxi(0, cy - 320)
	var y1: int = mini(h, cy + 160)
	var top := -1
	var bot := -1
	for y in range(y0, y1):
		var run := 0
		for x in range(x0, x1):
			var i := (y * w + x) * 4
			if absi(int(a[i]) - int(b[i])) > DIFF \
				or absi(int(a[i + 1]) - int(b[i + 1])) > DIFF \
				or absi(int(a[i + 2]) - int(b[i + 2])) > DIFF:
				run += 1
		if run >= ROW_MIN_CANVAS_PX:
			if top < 0:
				top = y
			bot = y
	return 0.0 if top < 0 else float(bot - top)
