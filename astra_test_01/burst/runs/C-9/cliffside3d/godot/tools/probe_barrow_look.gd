extends SceneTree
# C-9 T10: the WORLD half of the stack, built and captured WITHOUT the character.
#
# Why this exists: knight.gd is owned by a concurrent workstream (the armed motion set) and
# is periodically un-parseable while it is being written. Every part of the stack except the
# character's own materials is independent of it -- the ramp, the snow layer, the ink pass,
# the fog, the grade and the paper are functions of world position, world normal, depth and
# the screen buffer, and none of those know a character exists. So the look can be built,
# looked at, tuned and measured while the shared file is broken, and the full capture run
# becomes a confirmation rather than a first attempt.
#
# It also answers the one thing the smoke test cannot: WHETHER THE SHADERS COMPILED. A Godot
# spatial shader that fails to compile does not stop the scene; it renders, and it renders
# WRONG, and the only reliable way to know is to look at a pixel whose value the design
# predicts. So this prints the frame's own statistics next to the stills.
#
#   Godot --path godot --resolution 640x360 --script tools/probe_barrow_look.gd -- --out DIR

const SHOT := Vector2i(1920, 1080)

var out := ""
var vp: SubViewport
var scene
var report := {}


func _initialize() -> void:
	out = ProjectSettings.globalize_path("user://barrow_look")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out)

	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = preload("res://scripts/barrow_world.gd").new()
	scene.skip_character = true
	vp.add_child(scene)
	for i in 60:
		await process_frame
		await physics_frame
	report["scene"] = scene.report
	scene.set_hud_visible(false)

	var aim := Vector3(BarrowStandIn.MOUND_CENTRE.x - 2.0,
		scene.world.height_at(BarrowStandIn.MOUND_CENTRE.x, BarrowStandIn.MOUND_CENTRE.y + 8.0) + 1.4,
		BarrowStandIn.MOUND_CENTRE.y + 8.0)
	for spec in [["play_on", 1.0, true], ["play_off", 1.0, false],
				 ["wide_on", 0.38, true], ["wide_off", 0.38, false]]:
		scene.park_camera(aim, float(spec[1]))
		scene.set_stack(bool(spec[2]))
		await _settle()
		var img: Image = vp.get_texture().get_image()
		img.save_png("%s/look_%s.png" % [out, String(spec[0])])
		report[String(spec[0])] = _stats(img)
		print("[look] %s  %s" % [String(spec[0]), JSON.stringify(report[String(spec[0])])])

	# the ink pass alone, at the play framing, so its coverage can be seen at a glance
	scene.park_camera(aim, 1.0)
	scene.set_stack(true)
	scene.set_ink(false)
	await _settle()
	vp.get_texture().get_image().save_png(out + "/look_play_noink.png")
	scene.set_ink(true)
	scene.set_snow(false)
	await _settle()
	vp.get_texture().get_image().save_png(out + "/look_play_nosnow.png")
	scene.set_snow(true)
	await _settle()
	report["snow"] = scene.snow_report()

	var f := FileAccess.open(out + "/barrow_look.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("[look] -> %s" % out)
	quit(0)


func _stats(img: Image) -> Dictionary:
	"""Enough of the frame's own numbers to tell a rendered picture from a failed shader.
	A spatial shader that does not compile renders flat and uniform, so a near-zero spread
	is the signature to watch for -- not an error message, because there will not be one."""
	var n := 0
	var sum := Vector3.ZERO
	var mn := 2.0
	var mx := -1.0
	var step := 7
	var lo_black := 0
	for y in range(0, img.get_height(), step):
		for x in range(0, img.get_width(), step):
			var c := img.get_pixel(x, y)
			var l: float = PaintStack.srgb_to_linear(c.r) * 0.2126 \
				+ PaintStack.srgb_to_linear(c.g) * 0.7152 \
				+ PaintStack.srgb_to_linear(c.b) * 0.0722
			sum += Vector3(c.r, c.g, c.b)
			mn = minf(mn, l)
			mx = maxf(mx, l)
			if l < 0.004:
				lo_black += 1
			n += 1
	return {
		"sampled_px": n,
		"mean_srgb": [snappedf(sum.x / n, 0.0001), snappedf(sum.y / n, 0.0001),
					  snappedf(sum.z / n, 0.0001)],
		"min_luma_linear": snappedf(mn, 0.000001),
		"max_luma_linear": snappedf(mx, 0.0001),
		"near_black_share": snappedf(float(lo_black) / float(n), 0.0001),
	}


func _settle() -> void:
	for i in 8:
		await physics_frame
		await process_frame
	RenderingServer.force_draw()
	await process_frame
	await process_frame
