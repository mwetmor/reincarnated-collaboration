extends SceneTree
# T9-1c: the relief moved near-black from 19.04% to 18.93%. That is nothing, and the reason
# matters more than the number. Three candidates, and they are separable by switching one
# thing at a time: the wall FACES AWAY from the key (N.L ~ 0), the wall is IN SHADOW (no
# direct light at all, and no normal can help), or the painted ALBEDO there is already so
# dark that 40% ambient lands under the threshold whatever happens.
const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const AIM := Vector2(3459.88, 1027.18)
var vp: SubViewport
var cam: Camera3D
var scene

func _initialize():
	vp = SubViewport.new(); vp.size = SHOT; vp.own_world_3d = false
	vp.msaa_3d = Viewport.MSAA_DISABLED; vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60: await process_frame
	cam = Camera3D.new(); cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT; cam.near = scene.cam.near; cam.far = scene.cam.far
	cam.cull_mask = scene.cam.cull_mask
	vp.add_child(cam); cam.current = true
	if scene.knight != null: scene.knight.visible = false
	scene.set_lit(true)
	scene.look_at_canvas(AIM)
	var sun := scene.get_node_or_null(^"Lights/Sunset") as DirectionalLight3D
	var env := (scene.get_node(^"Env") as WorldEnvironment).environment
	var base_amb := env.ambient_light_energy
	print("sun energy %.2f  shadows %s  ambient %.2f" % [sun.light_energy, sun.shadow_enabled, base_amb])
	for c in [["as shipped", true, base_amb, sun.light_energy],
			  ["shadows OFF", false, base_amb, sun.light_energy],
			  ["shadows off + ambient x2", false, base_amb * 2.0, sun.light_energy],
			  ["shadows on + sun x2", true, base_amb, sun.light_energy * 2.0],
			  ["ALBEDO only (sun 0, ambient 1)", false, 1.0, 0.0]]:
		sun.shadow_enabled = bool(c[1])
		env.ambient_light_energy = float(c[2])
		sun.light_energy = float(c[3])
		for i in 6: await process_frame
		_mirror()
		for i in 3: await process_frame
		var img := vp.get_texture().get_image()
		var n := 0
		var s := 0.0
		for y in range(0, SHOT.y, 2):
			for x in range(0, SHOT.x, 2):
				var p := img.get_pixel(x, y)
				var l: float = (p.r + p.g + p.b) / 3.0 * 255.0
				s += l
				if l < 24.0: n += 1
		var tot := (SHOT.y / 2) * (SHOT.x / 2)
		print("  %-32s mean luma %5.1f   near-black %5.2f%%" % [String(c[0]), s / float(tot), 100.0 * float(n) / float(tot)])
	quit(0)

func _mirror():
	cam.global_transform = scene.cam.global_transform
	cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))
