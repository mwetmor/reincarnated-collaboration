extends SceneTree
# C-9 T7-A: a fast look at the two named spots, through a fixed 1920x1080 SubViewport.
# Also counts the COVERAGE VOID at each spot -- magenta pixels under show_void -- which is
# the measurement item 3 asks for.
#
#   Godot --path godot --resolution 1920x1080 --script tools/check.gd -- --out DIR

const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const SPOTS := {
	"plateau": Vector2(2285.62, 2407.32),
	"bridge": Vector2(3459.88, 1027.18),
}

var out_dir := ""
var scene
var vp: SubViewport
var shot_cam: Camera3D


func _initialize() -> void:
	out_dir = ProjectSettings.globalize_path("user://check")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = false
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 50:
		await process_frame
	shot_cam = Camera3D.new()
	shot_cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	shot_cam.keep_aspect = Camera3D.KEEP_HEIGHT
	shot_cam.near = scene.cam.near
	shot_cam.far = scene.cam.far
	shot_cam.cull_mask = scene.cam.cull_mask
	vp.add_child(shot_cam)
	shot_cam.current = true

	var report := {}
	for name in SPOTS:
		scene.look_at_canvas(SPOTS[name])
		if scene.knight != null:
			scene.knight.visible = false
		await _shot("%s_3d" % name)
		scene.show_void(true)
		var img := await _shot("%s_void" % name)
		var v := _count_magenta(img)
		scene.show_void(false)
		scene.set_void_fill(false)
		await _shot("%s_nofill" % name)
		scene.set_void_fill(true)
		report[name] = {"void_px": v, "void_pct": snappedf(100.0 * float(v) / (1920.0 * 1080.0), 0.001)}
		print("  %-8s void %d px = %.3f%% of the play-camera view" %
			[name, v, 100.0 * float(v) / (1920.0 * 1080.0)])
	var f := FileAccess.open(out_dir + "/void.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("[check] -> ", out_dir)
	quit(0)


func _shot(name: String) -> Image:
	shot_cam.global_transform = scene.cam.global_transform
	shot_cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))
	for i in 4:
		await process_frame
	var img := vp.get_texture().get_image()
	img.save_png("%s/%s.png" % [out_dir, name])
	return img


func _count_magenta(img: Image) -> int:
	var n := 0
	for y in img.get_height():
		for x in img.get_width():
			var c := img.get_pixel(x, y)
			if c.r > 0.85 and c.g < 0.18 and c.b > 0.85:
				n += 1
	return n
