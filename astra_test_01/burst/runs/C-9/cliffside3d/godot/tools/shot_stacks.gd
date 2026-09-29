extends SceneTree
# C-9 D2 gate G3: one still per gear stack at the bridge, plus a close sheet for reading
# the pieces. Five stacks: base / +helmet+bracers / +byrnie / +mantle / +axe+shield.
const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const BRIDGE := Vector2(3459.88, 1027.18)
const ON_BRIDGE := Vector2(3380.0, 1120.0)
var vp: SubViewport
var cam: Camera3D
var scene

func _initialize():
	var out := ProjectSettings.globalize_path("user://stacks")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out)
	vp = SubViewport.new(); vp.size = SHOT; vp.own_world_3d = false
	vp.msaa_3d = Viewport.MSAA_4X; vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 50: await process_frame
	cam = Camera3D.new(); cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT; cam.near = scene.cam.near; cam.far = scene.cam.far
	cam.cull_mask = scene.cam.cull_mask
	vp.add_child(cam); cam.current = true
	var k = scene.knight
	k.set_physics_process(false)
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var g := CliffWorld.ground_at(space, ON_BRIDGE, scene.right, scene.up, scene.fwd)
	k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.02
	k.facing = "NE"; k.state = "idle"; k._drive()
	for i in 10:
		await physics_frame
		await process_frame
	for s in k.gear_stack_count():
		k.set_gear_stack(s)
		for i in 6:
			await physics_frame
			await process_frame
		# the bridge view, for the deliverable
		scene.look_at_canvas(BRIDGE)
		_mirror()
		for i in 4: await process_frame
		vp.get_texture().get_image().save_png("%s/stack_%d_bridge.png" % [out, s])
		# and a close one, for reading the pieces
		scene.look_at_canvas(ON_BRIDGE + Vector2(0, -60), 0.0, 3.0)
		_mirror()
		for i in 4: await process_frame
		vp.get_texture().get_image().save_png("%s/stack_%d_close.png" % [out, s])
		print("  stack %d: %s" % [s, str(k.cfg["gear_stacks"][s])])
	print("[stacks] -> ", out)
	quit(0)

func _mirror():
	cam.global_transform = scene.cam.global_transform
	cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))
