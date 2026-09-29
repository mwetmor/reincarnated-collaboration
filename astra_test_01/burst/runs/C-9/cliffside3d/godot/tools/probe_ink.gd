extends SceneTree
# C-9 T9: WHICH ink mesh paints the block?
# 16.8% of the lit bridge frame is exactly RGB(14,11,16) -- the terrain outline's own
# line_color. An `openness` test picked two meshes and skipping them changed nothing, so
# the test was measuring the wrong property. Show the ink meshes ONE AT A TIME and let the
# pixels say which one it is.
const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const AIM := Vector2(3459.88, 1027.18)
var out_dir := ""
var scene
var vp: SubViewport
var cam: Camera3D

func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir)
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
	scene.knight.visible = false
	scene.set_lit(true)
	scene.look_at_canvas(AIM, 0.0, 1.0)
	for i in 10: await process_frame
	var names := []
	for o in scene._terrain_ink:
		o.visible = false
		names.append(String((o as MeshInstance3D).name))
	await _shot("ink_none")
	for i in scene._terrain_ink.size():
		var o: MeshInstance3D = scene._terrain_ink[i]
		o.visible = true
		await _shot("ink_%02d" % i)
		o.visible = false
	var f := FileAccess.open(out_dir + "/ink_names.json", FileAccess.WRITE)
	f.store_string(JSON.stringify({"names": names, "skipped": scene._ink_skipped}, " "))
	f.close()
	print("[ink] %d ink meshes: %s" % [names.size(), ", ".join(names)])
	quit(0)

func _mirror() -> void:
	cam.global_transform = scene.cam.global_transform
	cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))

func _shot(nm: String) -> void:
	_mirror()
	for i in 4: await process_frame
	vp.get_texture().get_image().save_png("%s/%s.png" % [out_dir, nm])
