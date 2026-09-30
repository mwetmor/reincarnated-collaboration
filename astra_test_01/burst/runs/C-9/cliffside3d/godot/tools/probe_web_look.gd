extends SceneTree
# C-9 R-C9-83 -- THE PHONE BUILD'S LOOK, ON THE DESKTOP, WITH STDOUT.
#
# The browser shows the web build and hides why it looks the way it does. This renders the
# play framing under whichever renderer the command line names, with the web branches on
# (`--as-web`, PaintStack.is_web), so the Compatibility path can be compared against the
# desktop's Forward+ path in ONE harness, and the pass-through frames isolate the post pass:
#
#   web_play            the frame as the phone build draws it (full kit, him at the painting's
#                       clearing, the camera on his chest)
#   post_passthrough    the post pass with its ink and grade OFF -- a copy of the screen
#   post_hidden         the post pass not drawn at all
# post_passthrough == post_hidden is the test that the pass copies the screen faithfully; any
# difference between them is the pass itself (a colour-space round trip, a lost transparent).
#
#   Godot --path godot --rendering-method gl_compatibility --resolution 1280x720 \
#         --script tools/probe_web_look.gd -- --as-web --out DIR [--no-kit]

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
		out_dir = ProjectSettings.globalize_path("user://web_look")
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = true
	# the project's own 3D MSAA (project.godot msaa_3d=2), which the web root viewport inherits
	vp.msaa_3d = Viewport.MSAA_DISABLED if OS.get_cmdline_user_args().has("--no-msaa") else Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/barrow.tscn").instantiate()
	vp.add_child(scene)
	for i in 70:
		await process_frame
		await physics_frame
	# EXPERIMENT SWITCHES, the levers tried on the Compatibility renderer's light sum before the
	# fix (PaintStack.move_ambient_into_light). Measured 2026-09-30 on the play frame, mean
	# |difference| from Forward+ per channel: none 47.1, adjustments 47.2, glow 48.8, 3D scale
	# 0.75 46.1 -- none moves the sum into linear light; the sun's shadow OFF 22.5 (the sun back
	# in the base pass, and no cast shadows). Each is one lever, named on stdout.
	var env: Environment = scene.env_node.environment
	if args.has("--adjust"):
		env.adjustment_enabled = true
		print("[web_look] lever: env adjustments ON (identity)")
	if args.has("--glow"):
		env.glow_enabled = true
		env.glow_intensity = 0.0
		env.glow_bloom = 0.0
		print("[web_look] lever: glow ON at zero intensity")
	var si := args.find("--scale3d")
	if si >= 0 and si + 1 < args.size():
		vp.scaling_3d_scale = float(args[si + 1])
		print("[web_look] lever: scaling_3d_scale %s" % args[si + 1])
	var bi := args.find("--sun-bias")
	if bi >= 0 and bi + 1 < args.size():
		scene.sun.shadow_bias = float(args[bi + 1])
		print("[web_look] lever: sun shadow_bias %s" % args[bi + 1])
	var ni := args.find("--sun-nbias")
	if ni >= 0 and ni + 1 < args.size():
		scene.sun.shadow_normal_bias = float(args[ni + 1])
		print("[web_look] lever: sun shadow_normal_bias %s" % args[ni + 1])
	var pi := args.find("--post-param")
	if pi >= 0 and pi + 2 < args.size():
		scene.set_post_param(args[pi + 1], float(args[pi + 2]))
		print("[web_look] lever: post %s = %s" % [args[pi + 1], args[pi + 2]])
	if args.has("--no-instancing"):
		scene.set_instancing(false)
		print("[web_look] lever: instancing OFF (every prop its own node)")
	if args.has("--no-reflect"):
		env.reflected_light_source = Environment.REFLECTION_SOURCE_DISABLED
		print("[web_look] lever: reflected light OFF")
	if args.has("--play-only"):
		scene.set_hud_visible(false)
	if args.has("--no-sun-shadow"):
		scene.sun.shadow_enabled = false
		print("[web_look] lever: sun shadow OFF")
	print("[web_look] renderer=%s web=%s heather=%s" % [RenderingServer.get_current_rendering_method(),
		str(PaintStack.is_web()), scene.heather_mode])
	var k = scene.knight
	if not args.has("--no-kit"):
		k.set_gear_stack(k.gear_stack_count() - 1)
	k.set_physics_process(false)
	for i in 30:
		k.drive_dir(Vector2.ZERO, false, 1.0 / 24.0)
		await physics_frame
		await process_frame
	scene.freeze_pose(true)
	k.state = "idle"
	scene.set_hud_visible(false)
	for n in scene.find_children("*", "CanvasLayer", true, false):
		(n as CanvasLayer).visible = false
	if scene.has_method("set_heather_wind"):
		scene.set_heather_wind(false)
	scene.place_knight(3.48, 0.28, "N")
	scene.park_camera(k.global_position + Vector3(0, 0.9, 0), 1.0)
	await _settle()
	await _shot("web_play")
	if args.has("--air-ab"):
		# the falling snow's own pixels: the same frame with the particles off
		scene.set_particles(false)
		await _settle()
		await _shot("web_play_air_off")
		scene.set_particles(true)
		await _settle()
	if args.has("--calib"):
		# THE TWO HALVES OF THE LIGHT, each alone, stack OFF (plain Lambert, no post pass): the
		# ambient with the sun at 0, then the sun with the ambient at 0 -- so a difference
		# between renderers is attributed to one term, not guessed at
		scene.set_stack(false)
		var e0: float = scene.sun.light_energy
		scene.sun.light_energy = 0.0
		await _settle()
		await _shot("calib_ambient")
		scene.sun.light_energy = e0
		var env2: Environment = scene.env_node.environment
		var amb0: float = env2.ambient_light_energy
		env2.ambient_light_energy = 0.0
		var saved := _set_ambient_in_light(Vector3.ZERO)
		await _settle()
		await _shot("calib_sun")
		env2.ambient_light_energy = amb0
		for m in saved:
			(m as ShaderMaterial).set_shader_parameter("ambient_in_light", saved[m])
		scene.set_stack(true)
		await _settle()
	if args.has("--play-only"):
		print("[web_look] -> %s" % out_dir)
		quit(0)
		return
	scene.set_post_param("ink_on", 0.0)
	scene.set_post_param("grade_on", 0.0)
	await _settle()
	await _shot("post_passthrough")
	scene.post_q.visible = false
	await _settle()
	await _shot("post_hidden")
	scene.post_q.visible = true
	scene.set_post_param("ink_on", 1.0)
	scene.set_post_param("grade_on", 1.0)
	# the wide framing: the mound, the ring and the tarn in one frame
	scene.park_camera(Vector3(2.0, scene.world.height_at(2.0, -3.0) + 1.2, -3.0), 0.45)
	await _settle()
	await _shot("web_wide")
	print("[web_look] -> %s" % out_dir)
	quit(0)


func _set_ambient_in_light(v: Vector3) -> Dictionary:
	var saved := {}
	for n in scene.find_children("*", "GeometryInstance3D", true, false):
		var m = (n as GeometryInstance3D).material_override
		if m is ShaderMaterial and (m as ShaderMaterial).shader != null \
				and (m as ShaderMaterial).shader.code.contains("ambient_in_light") and not saved.has(m):
			saved[m] = (m as ShaderMaterial).get_shader_parameter("ambient_in_light")
			(m as ShaderMaterial).set_shader_parameter("ambient_in_light", v)
	return saved


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
	print("[web_look] %s" % nm)
