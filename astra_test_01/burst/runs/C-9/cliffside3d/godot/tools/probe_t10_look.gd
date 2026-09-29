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
	vp.add_child(scene)
	for i in 70:
		await process_frame
		await physics_frame
	var k = scene.knight
	k.set_physics_process(false)
	scene.freeze_pose(true)
	k.set_gear_stack(k.gear_stack_count() - 1)
	k.state = "idle"
	scene.set_hud_visible(false)
	scene.place_knight(4.2, -0.3, "NE")
	scene.park_camera(scene._aim_for(k.global_position), 1.0)
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
