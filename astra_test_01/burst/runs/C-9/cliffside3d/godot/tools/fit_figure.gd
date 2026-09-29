extends SceneTree
# C-9 R-C9-66: how big is a character in the 3D cliffside?
#
# The rule of record (cliffside_B/frames/knight_fit.json, and walkable.json's
# figure_height_px 151): a player figure stands 150.2135 canvas px crown-to-sole. The
# 2D route gets there by SCALING CELLS. In 3D there are no cells -- there is a body with
# a real height -- so the same rule becomes a scale on the body.
#
# It is not 1.0, and the gap is the point. A 1.80 m body under this world camera --
# orthographic, 100.6176 px/m, pitched 52.95 deg -- projects to about 125 px, because an
# elevated view foreshortens a standing figure. The painted world and the painted
# character simply disagree about how big a person is, and the ART IS THE AUTHORITY on
# how big a character looks in this world. So the body is scaled to the art.
#
# Measured, not solved: the projected height depends on the figure's own depth as well
# as its height (h*cos + d*sin), so it is rendered and read off, exactly as the chartest
# camera fit is. Writes data/figure.json.
#
#   Godot --path godot --resolution 1920x1080 --script tools/fit_figure.gd -- --v4

const RULE_PX := 150.2135416666667
const SPAWN := Vector2(2285.62, 2407.32)
const TOL := 1.0


func _initialize():
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 30:
		await process_frame
	var k = scene.knight
	if k == null:
		print("FAIL: no knight")
		quit(1)
		return
	# Photograph the figure ALONE, on its own layer, so the measurement is of the figure
	# and not of whatever painted rock happens to be behind it.
	var vp := SubViewport.new()
	vp.size = Vector2i(512, 512)
	vp.own_world_3d = false
	vp.transparent_bg = true
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	scene.add_child(vp)
	var c := Camera3D.new()
	c.projection = Camera3D.PROJECTION_ORTHOGONAL
	c.keep_aspect = Camera3D.KEEP_HEIGHT
	c.size = 512.0 / 100.617553710938
	c.near = 0.05
	c.far = 80.0
	c.cull_mask = 4                       # the character's own layer
	vp.add_child(c)

	var fs: float = k._figure_scale
	var passes := []
	for it in 6:
		k._figure_scale = fs
		k.scale = Vector3.ONE
		if k._rig != null:
			k._rig.scale = Vector3.ONE * fs
		var aim: Vector3 = k.global_position + Vector3.UP * 1.0 * fs
		c.global_position = aim - scene.fwd * 25.0
		c.look_at(aim, Vector3.UP)
		for i in 4:
			await process_frame
		var h := _height(vp.get_texture().get_image())
		passes.append({"pass": it, "figure_scale": snappedf(fs, 5), "measured_px": h})
		print("  pass %d  scale %.4f -> %6.1f px  (rule %.1f)" % [it, fs, h, RULE_PX])
		if h <= 0.0:
			print("FAIL: the figure rendered empty")
			quit(1)
			return
		if absf(h - RULE_PX) <= TOL:
			break
		fs *= RULE_PX / h
	var report := {
		"note": "C-9 R-C9-66. The figure scale that makes a body stand the rule's "
			+ "150.2135 canvas px under the world camera (orthographic, 100.6176 px/m, "
			+ "pitch 52.95 deg). MEASURED, because the projected height of a standing "
			+ "figure mixes its height with its depth and cannot be solved from height "
			+ "alone.",
		"rule_px": RULE_PX, "figure_scale": fs, "passes": passes,
		"model_height_m": 1.8, "effective_height_m": 1.8 * fs,
		"why_not_one": "a 1.80 m body projects to about 125 px here; the painted "
			+ "character is drawn larger than the painted world's own metric scale, and "
			+ "the art is the authority on how big a character looks.",
	}
	var f := FileAccess.open("res://data/figure.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("=== figure scale %.5f  (a %.2f m body) -> %.1f px ===" %
		[fs, 1.8 * fs, passes[-1]["measured_px"]])
	quit(0)


func _height(img: Image) -> float:
	if img.get_format() != Image.FORMAT_RGBA8:
		img.convert(Image.FORMAT_RGBA8)
	var d := img.get_data()
	var w := img.get_width()
	var h := img.get_height()
	var top := -1
	var bot := -1
	for y in h:
		var row := y * w * 4 + 3
		var run := 0
		for x in w:
			if d[row + x * 4] > 8:
				run += 1
		# The same prop split the 2D side uses: a pollaxe haft clears the helm, and a
		# crown-to-sole that includes a weapon is measuring the weapon.
		if run >= 8:
			if top < 0:
				top = y
			bot = y
	return 0.0 if top < 0 else float(bot - top)
