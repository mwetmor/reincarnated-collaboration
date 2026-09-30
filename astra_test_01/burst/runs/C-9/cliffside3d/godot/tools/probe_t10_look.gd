extends SceneTree
# C-9 T10 — THREE FRAMES, FAST, SO THE EYE CAN VETO BEFORE THE TWELVE-MINUTE CAPTURE RUNS.
#
# Not a measurement. The full harness (shot_barrow.gd) produces twenty frames, a bias sweep,
# a contact test and a movie, and it is not worth starting if the tiles are at the wrong
# scale or the mound is inside out. This renders the play camera, the wide framing and the
# scale shot and quits.
#
#   Godot --path godot --resolution 640x360 --script tools/probe_t10_look.gd -- --out DIR

const SHOT := Vector2i(1920, 1080)
var out_dir := ""
var vp: SubViewport
var scene


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	if out_dir == "":
		out_dir = ProjectSettings.globalize_path("user://look")
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/barrow.tscn").instantiate()
	if "--baseline" in args:
		# the heather as it was before the T10-1c warmth change, for a before/after in one code
		scene.heather_core = false
		scene.heather_two_sided = false
	vp.add_child(scene)
	for i in 70:
		await process_frame
		await physics_frame
	var k = scene.knight
	k.set_gear_stack(k.gear_stack_count() - 1)
	k.set_physics_process(false)
	for i in 30:
		k.drive_dir(Vector2.ZERO, false, 1.0 / 24.0)
		await physics_frame
		await process_frame
	scene.freeze_pose(true)
	k.state = "idle"
	scene.set_hud_visible(false)
	scene.place_knight(3.48, 0.28, "N")
	# CENTRED ON HIM: the aim is his chest, not the 2D route's 55 px lift above his feet
	scene.park_camera(k.global_position + Vector3(0, 0.9, 0), 1.0)
	await _settle()
	await _shot("look_play")
	scene.set_stack(false)
	await _settle()
	await _shot("look_play_off")
	scene.set_stack(true)
	scene.park_camera(Vector3(2.0, scene.world.height_at(2.0, -3.0) + 1.2, -3.0), 0.45)
	await _settle()
	await _shot("look_wide")
	scene.place_knight(4.85, -3.95, "NW")
	await _settle()
	scene.park_camera(Vector3(4.25, scene.world.height_at(4.25, -4.35) + 1.35, -4.35), 2.35)
	await _settle()
	await _shot("look_scale")
	# THE PAINTING'S OWN FRAMING: 1536x1024, ortho height 1024 / 140.86 = 7.2696 m, aimed at
	# the painting's centre pixel unprojected onto the flat floor, him where the painting has him
	vp.size = Vector2i(1536, 1024)
	scene.place_knight(3.48, 0.28, "N")
	await _settle()
	scene.park_camera(Vector3(2.619, 0.0, -0.472), (1024.0 / 100.617553710938) / 7.2696)
	await _settle()
	await _shot("look_painting_frame")
	# the ID pass too, under the names barrow_paint_compare.py reads, so a look run can be
	# measured for coverage and warmth without the full capture
	vp.msaa_3d = Viewport.MSAA_DISABLED
	scene.set_class_id_view(true)
	await _settle()
	await _shot("barrow_painting_ids")
	scene.set_class_id_view(false)
	scene.set_class_id_view(true, true)
	await _settle()
	await _shot("barrow_painting_ids_occl")
	scene.set_class_id_view(false)
	vp.msaa_3d = Viewport.MSAA_4X
	await _settle()
	await _shot("barrow_painting_frame")
	print("[look] -> %s" % out_dir)
	quit(0)


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
	print("[look] %s" % nm)
