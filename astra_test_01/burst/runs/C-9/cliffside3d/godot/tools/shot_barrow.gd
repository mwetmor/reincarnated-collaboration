extends SceneTree
# C-9 T10 — the barrow render stack, captured and measured in ONE run.
#
# ONE RUN AND NOT SEVERAL, for the reason T9 learned the hard way: two runs differ in more
# than the thing under test (the camera settles somewhere else, the idle animation lands on a
# different frame, the shader cache is cold), and attribution is a subtraction, so a
# subtraction between two runs measures the runs as well as the change.
#
# THE PAIRS ARE BUILT TO BE SUBTRACTED. Each pen is isolated by hiding IT and nothing else:
#   screen-space ink = nograde_ink_on  -  nograde_ink_off
#   hull ink         = nograde_ink_off -  nograde_hull_off
# so every ink pixel measured is a pixel that pen actually painted, rather than a dark pixel
# guessed to belong to it. The grade and the paper are off for those four frames only,
# because they multiply the frame and would put the two pens through the same distortion
# twice -- harmless for the ΔE between them, misleading for either against its nominal.
#
#   Godot --path godot --resolution 1920x1080 --script tools/shot_barrow.gd \
#         -- --out DIR [--frames DIR] [--walk 96]

const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const FPS := 24.0
const DT := 1.0 / 24.0

# where he stands for the stills, and where the camera looks: on the ring's south lip, with
# the barrow, two stones and the hill all in frame
const STAND := Vector2(-3.4, 6.2)
const WALK_FROM := Vector2(-8.6, 10.4)

var out_dir := ""
var frames_dir := ""
var walk_n := 96
var vp: SubViewport
var scene
var report := {}
var _mf := 0


func _initialize() -> void:
	out_dir = ProjectSettings.globalize_path("user://barrow")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
		if args[i] == "--frames" and i + 1 < args.size():
			frames_dir = args[i + 1]
		if args[i] == "--walk" and i + 1 < args.size():
			walk_n = int(args[i + 1])
	if frames_dir == "":
		frames_dir = out_dir + "/frames"
	DirAccess.make_dir_recursive_absolute(out_dir)
	DirAccess.make_dir_recursive_absolute(frames_dir)
	Engine.physics_ticks_per_second = int(FPS)

	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/barrow.tscn").instantiate()
	vp.add_child(scene)
	for i in 80:
		await process_frame
		await physics_frame
	report["scene"] = scene.report
	report["viewport"] = {"size": [SHOT.x, SHOT.y], "msaa": "4x"}

	var k = scene.knight
	k.set_physics_process(false)
	scene.freeze_pose(true)
	k.set_gear_stack(k.gear_stack_count() - 1)       # full kit: axe, shield, helmet, byrnie, mantle
	k.state = "idle"
	scene.place_knight(STAND.x, STAND.y, "NE")
	scene.set_hud_visible(false)
	scene.park_camera(scene._aim_for(k.global_position), 1.0)
	await _settle()

	# ---- true scale, in pixels, from his own bones --------------------------
	var rect: Rect2 = scene.character_screen_rect()
	var skel: Skeleton3D = null
	for n in k.find_children("*", "Skeleton3D", true, false):
		if (n as Skeleton3D).find_bone("head_end") >= 0:
			skel = n
	var crown_px := -1.0
	if skel != null:
		var hb := skel.find_bone("head_end")
		var top: Vector3 = skel.global_transform * skel.get_bone_global_pose(hb).origin
		var pcam: Camera3D = scene.cam
		var a: Vector2 = pcam.unproject_position(top)
		var b: Vector2 = pcam.unproject_position(Vector3(top.x, k.global_position.y, top.z))
		crown_px = absf(a.y - b.y)
	report["true_scale"] = {
		"figure_scale": k._figure_scale,
		"model_height_m": k.cfg.get("model_height_m", 1.85),
		"foot_to_crown_px": snappedf(crown_px, 0.1),
		"expected_px": snappedf(float(k.cfg.get("model_height_m", 1.85)) * PPM * 0.602462407085, 0.1),
		"bone_bbox_px": [snappedf(rect.size.x, 0.1), snappedf(rect.size.y, 0.1)],
		"_why_bones": "a silhouette difference also catches his cast shadow; T9 measured a 104 px man at 195 px that way",
	}

	# ---- the snow layer, area-weighted over the real faces ------------------
	report["snow"] = scene.snow_report()

	# ---- the stills ---------------------------------------------------------
	# the delivered look, and the same frame with the stack off
	scene.set_stack(true)
	await _settle()
	await _shot("barrow_stack_on")
	scene.set_stack(false)
	await _settle()
	await _shot("barrow_stack_off")
	scene.set_stack(true)
	await _settle()
	# BOTH pens off, everything else delivered: the pair that gives the ink mask for the
	# min-luma and shadow-hue tests on the frame Matt is actually shown.
	scene.set_pens(false)
	await _settle()
	await _shot("barrow_stack_on_nopen")
	scene.set_pens(true)
	await _settle()

	# the ink, isolable
	scene.set_ink(false)
	await _settle()
	await _shot("barrow_ink_off")
	scene.set_ink(true)
	scene.set_grade(false)
	await _settle()
	await _shot("barrow_nograde_ink_on")
	scene.set_ink(false)
	await _settle()
	await _shot("barrow_nograde_ink_off")
	scene.set_hull_ink_visible(false)
	await _settle()
	await _shot("barrow_nograde_hull_off")
	scene.set_hull_ink_visible(true)
	scene.set_ink(true)
	scene.set_grade(true)
	await _settle()

	# the snow layer alone
	scene.set_snow(false)
	await _settle()
	await _shot("barrow_snow_off")
	scene.set_snow(true)
	await _settle()

	# the air alone
	scene.set_particles(false)
	await _settle()
	await _shot("barrow_air_off")
	scene.set_particles(true)
	scene.set_fog(false)
	await _settle()
	await _shot("barrow_fog_off")
	scene.set_fog(true)
	await _settle()

	# ---- HIM, before and after the ramp, world unchanged --------------------
	# The comparison Matt is owed: the ONLY thing that moves between these two frames is the
	# lighting response on his own materials. Same albedo, same ink line, same world, same
	# light, same pose.
	scene.set_ramp_on_character(true)
	await _settle()
	await _shot("barrow_char_ramp_on")
	scene.set_ramp_on_character(false)
	await _settle()
	await _shot("barrow_char_ramp_off")
	# and the THIRD state: his materials exactly as knight.gd built them, which is the look
	# Matt actually approved. ramp_mix = 0 is plain Lambert through the ramp shader and loses
	# his metallic 0.25, so it is close to the old look without being it.
	scene.set_ramp_on_character(true)
	scene.use_original_character_materials(true)
	await _settle()
	await _shot("barrow_char_original")
	scene.use_original_character_materials(false)
	await _settle()
	# HIM, REMOVED. His bone bounding box is 162x97 px and most of that rectangle is snow, so
	# a "before and after" averaged over the box is mostly an average of pixels that did not
	# change -- it reported a 1.7% difference for a change that is plainly visible on him.
	# This frame is what lets the comparison be masked to his actual silhouette.
	k.visible = false
	await _settle()
	await _shot("barrow_char_noknight")
	k.visible = true
	await _settle()
	report["char_rect_px"] = [int(rect.position.x), int(rect.position.y),
							  int(rect.size.x), int(rect.size.y)]

	# ---- does HE cast a shadow ---------------------------------------------
	report["his_shadow"] = await _shadow_check(k)
	print("[barrow] shadow %s" % JSON.stringify(report["his_shadow"]))

	# ---- the wide framing, for the eye -------------------------------------
	var wide_aim := Vector3(BarrowStandIn.MOUND_CENTRE.x + 1.0,
		scene.world.height_at(BarrowStandIn.MOUND_CENTRE.x, BarrowStandIn.MOUND_CENTRE.y) + 2.0,
		BarrowStandIn.MOUND_CENTRE.y + 2.0)
	scene.park_camera(wide_aim, 0.38)
	await _settle()
	await _shot("barrow_wide_on")
	scene.set_stack(false)
	await _settle()
	await _shot("barrow_wide_off")
	scene.set_stack(true)
	await _settle()

	# ---- FRAME COST, on this M2, at 1920x1080 ------------------------------
	# Measured on the viewport that actually renders the scene, with him WALKING, because a
	# parked idle frame is the cheapest frame the scene has and quoting it would be a
	# measurement of the screenshot rather than of the game.
	scene.unpark_camera()
	scene.freeze_pose(false)              # he has to move again for the cost run and the walk
	scene.place_knight(WALK_FROM.x, WALK_FROM.y, "NE")
	await _settle()
	report["frame_cost_ms"] = {
		"_at": "MSAA 4x, Apple M2, walking with the full kit, vsync off",
		"stack_on": await _time_frames(true, 140, SHOT),
		"stack_off": await _time_frames(false, 140, SHOT),
		"instrument_check_2.25x_pixels": {
			"_expect": "a frame with 2.25x the pixels must cost measurably more",
			"stack_on_at_2880x1620": await _time_frames(true, 90, Vector2i(2880, 1620)),
		},
	}
	scene.set_stack(true)

	# ---- the walk, straight to frames for ffmpeg ---------------------------
	scene.place_knight(WALK_FROM.x, WALK_FROM.y, "NE")
	k.set_physics_process(false)
	await _settle()
	for i in walk_n:
		var run := i > int(float(walk_n) * 0.55)
		k.drive_dir(Vector2(0.62, -1.0), run, DT)
		await physics_frame
		await _frame()
	report["walk_frames"] = _mf
	report["walk_fps"] = FPS

	var f := FileAccess.open(out_dir + "/barrow.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("[barrow] -> %s  (%d walk frames)" % [out_dir, _mf])
	quit(0)


func _time_frames(stack: bool, n: int, res: Vector2i) -> Dictionary:
	"""WALL-CLOCK THROUGHPUT WITH VSYNC OFF, because the obvious instrument lies here.

	RenderingServer.viewport_get_measured_render_time_gpu() returned EXACTLY 0.00 for every
	sample, stack on and stack off, 110 samples each -- and 0.00 ms is not a fast frame, it is
	an unimplemented counter. The CPU half came back at 0.06 ms, which for 56,000 triangles, a
	shadow pass, 1,700 particles and a full-screen post pass is not a plausible number either.
	Both returned cleanly. Neither was measuring anything.

	So: vsync off, run frames as fast as the engine will, divide wall time by frames. And the
	instrument is CHECKED ON A KNOWN CASE by running it at two resolutions -- if a frame with
	2.25x the pixels does not cost measurably more, the number is not about rendering and must
	not be quoted."""
	scene.set_stack(stack)
	var prev := vp.size
	if res != vp.size:
		vp.size = res
	# THE LOOP MUST NOT AWAIT physics_frame. This capture sets physics to 24 Hz so the movie
	# frames are deterministic, and `await physics_frame` then gates the loop at 41.67 ms --
	# which is exactly what the previous version reported, for the stack on, for the stack off
	# and for a frame with 2.25x the pixels, all three within 0.7% of each other and of 1/24 s.
	# THE INSTRUMENT CHECK IS WHAT CAUGHT IT: three numbers that should have differed did not,
	# and the reason they did not was that none of them was about rendering.
	var prev_ticks := Engine.physics_ticks_per_second
	Engine.physics_ticks_per_second = 240
	Engine.max_fps = 0
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	for i in 40:                                  # warm: shader compiles land in the first frames
		scene.knight.drive_dir(Vector2(0.62, -1.0), false, DT)
		await process_frame
	var t0 := Time.get_ticks_usec()
	for i in n:
		scene.knight.drive_dir(Vector2(0.62, -1.0), false, DT)
		await process_frame
	var ms: float = float(Time.get_ticks_usec() - t0) / 1000.0 / float(n)
	Engine.physics_ticks_per_second = prev_ticks
	vp.size = prev
	return {"ms_per_frame": snappedf(ms, 0.01), "fps": snappedf(1000.0 / maxf(ms, 1e-3), 0.1),
			"frames": n, "render_px": [res.x, res.y]}


func _shadow_check(k) -> Dictionary:
	"""DOES HE CAST A SHADOW. Differencing him out of the frame gives his body AND his shadow;
	differencing him out with the sun's shadows OFF gives his body alone. The difference
	between those two areas is the shadow, in pixels. This is the same trap T9 recorded from
	the other side -- it measured a 104 px man at 195 px because his shadow rode along -- used
	here deliberately, as the measurement rather than as the error."""
	var sun: DirectionalLight3D = scene.sun
	var was := sun.shadow_enabled
	var counts := {}
	for spec in [["shadows_on", true], ["shadows_off", false]]:
		sun.shadow_enabled = bool(spec[1])
		await _settle()
		var with_him: Image = vp.get_texture().get_image()
		k.visible = false
		await _settle()
		var without: Image = vp.get_texture().get_image()
		k.visible = true
		var changed := 0
		for y in range(0, with_him.get_height(), 2):
			for x in range(0, with_him.get_width(), 2):
				var a := with_him.get_pixel(x, y)
				var b := without.get_pixel(x, y)
				if absf(a.r - b.r) + absf(a.g - b.g) + absf(a.b - b.b) > 0.012:
					changed += 1
		counts[String(spec[0])] = changed * 4          # every 2nd px in each axis
	sun.shadow_enabled = was
	await _settle()
	var body: int = counts["shadows_off"]
	var both: int = counts["shadows_on"]
	return {
		"px_changed_by_him_with_shadows": both,
		"px_changed_by_him_without_shadows": body,
		"his_shadow_px": both - body,
		"shadow_as_share_of_his_body": snappedf(float(both - body) / maxf(float(body), 1.0), 0.01),
		"verdict": "he casts a shadow" if (both - body) > body / 5 else "NO SHADOW FROM HIM",
	}


func _settle() -> void:
	for i in 8:
		await physics_frame
		await process_frame
	RenderingServer.force_draw()
	await process_frame


func _shot(nm: String) -> void:
	for i in 3:
		await process_frame
	vp.get_texture().get_image().save_png("%s/%s.png" % [out_dir, nm])
	print("[barrow] %s" % nm)


func _frame() -> void:
	await process_frame
	await process_frame
	vp.get_texture().get_image().save_jpg("%s/f_%04d.jpg" % [frames_dir, _mf], 0.93)
	_mf += 1
