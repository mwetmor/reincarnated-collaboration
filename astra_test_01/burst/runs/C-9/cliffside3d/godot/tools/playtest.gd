extends SceneTree
# C-9: play it the way Matt will, through the real input actions.
#
# Input.action_press drives the SAME actions the keyboard does, so this exercises
# _physics_process, _unhandled_input and the HUD rather than calling the methods behind
# them. Walk to the tree, cycle G through all five stacks, attack with the full kit, cycle
# F through its three strengths, and photograph each step.
const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
var vp: SubViewport
var cam: Camera3D
var scene
var out := ""
var shots := 0

func _initialize():
	out = ProjectSettings.globalize_path("user://playtest")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out)
	Engine.physics_ticks_per_second = 24
	scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60: await process_frame
	var k = scene.knight
	print("[play] spawn: stack %d/%d, fade %s" % [k.gear_stack, k.gear_stack_count(), CliffWorld.fade_min])

	# 1. walk toward the tree -- hold the real movement actions
	var start := CliffWorld.canvas_of(k.global_position, scene.right, scene.up)
	Input.action_press("move_left")
	for i in 48: await physics_frame
	Input.action_release("move_left")
	Input.action_press("move_down")
	for i in 36: await physics_frame
	Input.action_release("move_down")
	for i in 6: await physics_frame
	var here := CliffWorld.canvas_of(k.global_position, scene.right, scene.up)
	print("[play] walked %.0f canvas px (from %s to %s); camera aim %s" %
		[(here - start).length(), str(start.round()), str(here.round()), str(scene._aim_px.round())])
	await _shot("01_walked")

	# 2. run
	Input.action_press("run_modifier"); Input.action_press("move_up")
	for i in 20: await physics_frame
	Input.action_release("move_up"); Input.action_release("run_modifier")
	for i in 8: await physics_frame
	await _shot("02_ran")

	# 3. G through all five stacks
	for s in k.gear_stack_count():
		_tap("gear_cycle")
		for i in 8: await physics_frame
		print("[play] G -> stack %d  hud: %s" % [k.gear_stack, scene._hud.text])
		await _shot("03_gear_%d" % k.gear_stack)

	# 4. attack with the full kit (it lands on stack 0 after five taps; one more gets to 4)
	while k.gear_stack != k.gear_stack_count() - 1:
		_tap("gear_cycle")
		for i in 4: await physics_frame
	_tap("attack")
	for i in 3: await physics_frame
	print("[play] attack: attacking=%s clip=%s" % [k.attacking(), k._clip])
	await _shot("04_attack_mid")
	var guard := 0
	while k.attacking() and guard < 80:
		await physics_frame
		guard += 1
	for i in 6: await physics_frame
	print("[play] after the slash: clip=%s state=%s" % [k._clip, k.state])
	await _shot("05_after_attack")

	# 5. F through the three fade strengths
	for i in 3:
		_tap("fade_cycle")
		for j in 6: await physics_frame
		print("[play] F -> fade_min %.2f  hud: %s" % [CliffWorld.fade_min, scene._hud.text])
	await _shot("06_fade")

	# 6. Q/E camera
	Input.action_press("orbit_right")
	for i in 16: await physics_frame
	Input.action_release("orbit_right")
	print("[play] camera yaw %.1f deg" % scene._yaw)
	await _shot("07_orbit")
	print("[play] %d stills -> %s" % [shots, out])
	quit(0)

func _tap(a: String):
	Input.action_press(a)
	Input.action_release(a)

func _shot(name: String):
	if vp == null:
		vp = SubViewport.new(); vp.size = SHOT; vp.own_world_3d = false
		vp.msaa_3d = Viewport.MSAA_4X; vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(vp)
		cam = Camera3D.new(); cam.projection = Camera3D.PROJECTION_ORTHOGONAL
		cam.keep_aspect = Camera3D.KEEP_HEIGHT; cam.near = scene.cam.near; cam.far = scene.cam.far
		cam.cull_mask = scene.cam.cull_mask
		vp.add_child(cam); cam.current = true
	cam.global_transform = scene.cam.global_transform
	cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))
	for i in 4: await process_frame
	vp.get_texture().get_image().save_png("%s/%s.png" % [out, name])
	shots += 1
