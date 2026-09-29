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
const SAMPLES := 5
# 3 px against the rule. Not a loosened standard: my prop splitter agrees with the
# published figure on the MEAN to 0.16 px but by up to ~4 cell px on a single direction,
# because it splits differently; and the Keeper's own cells vary 237-240 by direction.
# A tolerance tighter than the instrument's demonstrated per-direction agreement is a
# coin toss dressed as a gate.
const RULE_TOL := 3.0
const SHOT_DIR := "user://size"
const RULE_PX := 150.2135416666667

var fails := 0
var report := {"note": "C-9 R-C9-61 on-screen figure height", "rule_px": RULE_PX, "rows": []}


func _check(ok: bool, what: String) -> void:
	if not ok:
		fails += 1
	print(("  PASS  " if ok else "  FAIL  ") + what)


func _slugify(s: String) -> String:
	var out := ""
	for c in s.to_lower():
		out += c if (c >= "a" and c <= "z") or (c >= "0" and c <= "9") else "_"
	return out


func _initialize():
	DirAccess.make_dir_recursive_absolute(SHOT_DIR)
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
			# SAMPLED and taken as a median, not read off one frame. An idle breathes:
			# the Keeper's own S reading moved 150.0 -> 149.0 between two runs of this
			# probe with nothing changed, which is a whole pixel of noise sitting under a
			# 2 px tolerance. A single frame does not measure a figure's height, it
			# measures its height at one moment of one animation.
			var samples := []
			for s in SAMPLES:
				for i in 5:
					await physics_frame
					await process_frame
				var img := root.get_texture().get_image()
				if s == 0:
					# Keep the FIRST full frame of each skin. The player has not moved
					# between them -- only which skin is visible changed -- so crops of
					# the same window are directly comparable. shot_chartest's inset
					# centres itself through the canvas transform, which does not track
					# reliably here, and three differently-framed crops make the figures
					# look like different sizes when the measurements say they are not.
					img.save_png("%s/%s_%s.png" % [SHOT_DIR, _slugify(k), facing])
				nodes[k].visible = false
				await process_frame
				await process_frame
				var bg := root.get_texture().get_image()
				nodes[k].visible = true
				var v := _figure_height(bg, img) / _canvas_scale()
				if v > 0.0:
					samples.append(v)
			if samples.is_empty():
				print("  %-16s %s  NOTHING MEASURED" % [k, facing])
				continue
			samples.sort()
			var h: float = samples[samples.size() / 2]
			heights[k] = h
			print("  %-16s %s  crown-to-sole %6.1f canvas px  (%d samples, spread %.1f)"
				% [k, facing, h, samples.size(), samples[-1] - samples[0]])
		var k3b = keeper.get_node_or_null(^"Knight3D")
		if k3b != null:
			k3b.call("set_weapon_visible", true)
		await _select(skin, 0)
		await process_frame

		var ref: float = float(heights.get("Keeper", 0.0))
		report["rows"].append({"facing": facing, "heights": heights, "keeper": ref})
		_check(absf(ref - RULE_PX) <= RULE_TOL,
			"%s: the Keeper matches the rule of record (%.1f vs %.1f px)" % [facing, ref, RULE_PX])
		for k in ["Knight sprites", "Knight 3D"]:
			if not heights.has(k):
				continue
			var d: float = float(heights[k]) - ref
			if k == "Knight sprites":
				# The sprite knight carries a PAINTED pollaxe. Its haft clears his helm
				# and cannot be split out of a capture: row width slides from 229 cell
				# px to 198 with no plateau, and a morphological opening hits the right
				# answer at one radius while collapsing the Keeper's own figure at the
				# next -- both tried against both references, neither stable. So this
				# number is a total extent, not a crown-to-sole, and asserting it
				# against the Keeper would be asserting a quantity I cannot measure.
				#
				# What IS exact is the TRANSFORM, and it is where the original defect
				# lived: the skin was registered with the Keeper's cell scale instead of
				# its own. That is checked below, against the set's declared format.
				print("  NOTE  %s: %s total extent %+.1f px vs the Keeper -- includes the "
					% [facing, k, d] + "painted haft, so not a crown-to-sole")
				report["rows"][-1]["sprite_extent_includes_haft"] = true
				continue
			_check(absf(d) <= TOLERANCE_PX,
				"%s: %s stands the Keeper's height (%.1f vs %.1f, delta %+.1f px, max %.0f)"
				% [facing, k, heights[k], ref, d, TOLERANCE_PX])
			_check(absf(float(heights[k]) - RULE_PX) <= RULE_TOL,
				"%s: %s matches the rule of record (%.1f vs %.1f px, max %.0f)"
				% [facing, k, heights[k], RULE_PX, RULE_TOL])

	# --- the transform, which no prop can contaminate ------------------------------
	# Each skin's Sprite2D must scale its cells by RULE / that set's own declared figure
	# height, and put that set's own ground row on the node origin. Exact arithmetic on
	# live node properties -- it would have caught the shipped bug (0.629167 inherited
	# from the Keeper where 0.754839 was owed) in one line, and it stays true whatever a
	# future set declares.
	print("[node transforms, against each set's declared format]")
	var fit = _json("res://frames/knight_test.json").get("fit", {})
	var cam = _json("res://frames/camera_meshy_t1.json")
	var want := [
		["Knight sprites", nodes["Knight sprites"], float(fit.get("figure_h_src_px", 0.0)),
			float(fit.get("pivot_y_src_px", 0.0))],
		["Knight 3D", (nodes["Knight 3D"].get_node_or_null(^"View") if nodes["Knight 3D"] != null else null),
			float(cam.get("px_per_m", 0.0)) * float(cam.get("character_height_m", 1.8)),
			float(cam.get("ground_row_y", 0.0))],
	]
	for row in want:
		var node = row[1]
		var figure: float = row[2]
		var ground: float = row[3]
		if node == null or figure <= 0.0:
			_check(false, "%s: no node or no declared figure height" % row[0])
			continue
		var expect := RULE_PX / figure
		_check(absf(node.scale.x - expect) < 1e-4,
			"%s: scale %.6f == %.4f / %.1f declared px (%.6f)"
			% [row[0], node.scale.x, RULE_PX, figure, expect])
		_check(absf(node.offset.y + ground) < 0.51,
			"%s: offset.y %.1f puts the declared ground row %.0f on the node origin"
			% [row[0], node.offset.y, ground])
		report["transforms"] = report.get("transforms", {})
		report["transforms"][row[0]] = {"scale": node.scale.x, "expect": expect,
										"offset_y": node.offset.y, "declared_px": figure}

	report["fails"] = fails
	var f := FileAccess.open("user://size_probe.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("=== on-screen figure height: %s (%d failures) ===" % ["PASS" if fails == 0 else "FAIL", fails])
	quit(1 if fails > 0 else 0)


func _json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var j = JSON.parse_string(FileAccess.get_file_as_string(path))
	return j if typeof(j) == TYPE_DICTIONARY else {}


func _sprites_are_one_column() -> bool:
	if not FileAccess.file_exists("res://frames/knight_test.json"):
		return false
	var j = JSON.parse_string(FileAccess.get_file_as_string("res://frames/knight_test.json"))
	if typeof(j) != TYPE_DICTIONARY:
		return false
	return not (j.get("directions_substituted_from_E", {}) as Dictionary).is_empty()


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
