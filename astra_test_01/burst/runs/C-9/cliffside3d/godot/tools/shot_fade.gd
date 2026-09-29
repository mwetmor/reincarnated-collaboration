extends SceneTree
# C-9 R-C9-70: the occluder fade, on and off, at the same four places on the tree path.
# Stills only -- the counting is tools/probe_fade.gd's job; this is the picture Matt sees.
const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const ANCHOR := Vector2(1896.0139860139861, 2765.0)
const STEPS := [-180.0, -60.0, 30.0, 120.0]
const AIM := Vector2(1896.0, 2640.0)
const ZOOM := 1.5
var vp: SubViewport
var cam: Camera3D
var scene

func _initialize():
	var out := ProjectSettings.globalize_path("user://fade")
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
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	for i in STEPS.size():
		var px: Vector2 = ANCHOR + Vector2(STEPS[i], -60.0)
		var g := CliffWorld.ground_at(space, px, scene.right, scene.up, scene.fwd)
		k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.02
		k.velocity = Vector3.ZERO
		k.facing = "E"; k.state = "walk"; k.play("walk"); k.visible = true
		scene.look_at_canvas(AIM, 0.0, ZOOM)
		for j in 6:
			await physics_frame
			await process_frame
		for on in [false, true]:
			scene.set_fade_enabled(on)
			_mirror()
			for j in 4: await process_frame
			vp.get_texture().get_image().save_png("%s/fade_%d_%s.png" % [out, i, "on" if on else "off"])
		print("  step %d at %s" % [i, str(px)])
	scene.set_fade_enabled(true)
	print("[fade] -> ", out)
	quit(0)

func _mirror():
	cam.global_transform = scene.cam.global_transform
	cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))
