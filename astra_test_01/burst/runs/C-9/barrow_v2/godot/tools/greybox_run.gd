extends SceneTree
## barrow_v2 greybox runner (lane BX).
##   views:  godot --path godot --resolution 1920x1080 --script tools/greybox_run.gd -- views OUT_DIR
##           -> one PNG per layout view (ZOOM-GD, the 25 x 18 m window), plus the plate-scale start view
##   film:   godot --path godot --resolution 1280x720 --fixed-fps 24 --write-movie X.avi \
##                 --script tools/greybox_run.gd -- film
##           -> the walker follows layout.walk_film.route at its speed; the camera follows (ZOOM-GD).
##           Prints {"trim_frames": N} once the scene is built so the encoder can cut the settle frames.

var scene: Node3D
var mode := "views"
var out_dir := ""
var frame := 0
var vi := 0
var wait := 0
var route: Array = []
var seg := 0
var seg_t := 0.0
var speed := 6.0
var started := false
var settle := 6


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() >= 1:
		mode = args[0]
	if args.size() >= 2:
		out_dir = args[1]
	scene = load("res://scenes/barrow_v2_greybox.tscn").instantiate()
	root.add_child(scene)


func _process(delta: float) -> bool:
	frame += 1
	if scene.cam == null:
		return false
	scene.free_cam = true
	if mode == "views":
		return _views()
	if mode == "establish":
		return _establish()
	return _film(delta)


func _views() -> bool:
	var views: Array = scene.layout["views"]
	var shots: Array = []
	for v in views:
		shots.append({"id": v["id"], "t": Vector2(float(v["target"][0]), float(v["target"][1])), "gd": true})
	shots.append({"id": "V0_start_plate_scale", "t": Vector2.ZERO, "gd": false})
	# R-C9-149a: one wide establishing still of the whole site at the game pitch (zero yaw), for direct
	# comparison with sketch A; ortho size 78 m of view height = ~98 m of ground depth, labels off

	if vi >= shots.size():
		print("[bv2] views done: %d" % shots.size())
		return true
	var s: Dictionary = shots[vi]
	if wait == 0:
		scene.set_zoom(s["gd"])
		if s.has("size"):
			scene.cam.size = float(s["size"])
		for lb in scene.labels:
			lb.visible = not s.has("nolabels")
		scene.place_camera(s["t"])
		scene.set_walker(s["t"] + Vector2(0.0, 1.5) if not s.has("size") else Vector2.ZERO, Vector2(0, 1))
	wait += 1
	if wait < settle:
		return false
	var img := root.get_texture().get_image()
	var p: String = out_dir.path_join("%s.png" % s["id"])
	img.save_png(p)
	print("[bv2] view %s target %s ppm %.4f cam.size %.5f -> %s (%dx%d)" % [s["id"], s["t"], scene.ppm, scene.cam.size, p, img.get_width(), img.get_height()])
	if s.has("size"):
		scene.set_zoom(false)
	vi += 1
	wait = 0
	return false


## R-C9-149a: the whole site at the game pitch (zero yaw) in one frame, for comparison with sketch A.
## Run at --resolution 1800x1440 so the frame's width stays inside the 128 m terrain extent.
var _sv: SubViewport


func _establish() -> bool:
	# rendered through a 1800 x 1440 SubViewport sharing the scene's world, so the frame is independent of
	# the window (the project's 16:9 stretch lock would otherwise letterbox it)
	if wait == 0:
		for lb in scene.labels:
			lb.visible = false
		scene.set_walker(Vector2.ZERO, Vector2(0, 1))
		_sv = SubViewport.new()
		_sv.size = Vector2i(1800, 1440)
		_sv.world_3d = root.world_3d
		_sv.msaa_3d = Viewport.MSAA_4X
		_sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		var c := Camera3D.new()
		c.projection = Camera3D.PROJECTION_ORTHOGONAL
		c.keep_aspect = Camera3D.KEEP_HEIGHT
		c.size = 93.0
		c.near = 0.5
		c.far = 600.0
		c.rotation_degrees = Vector3(-scene.ALPHA_DEG, 0.0, 0.0)
		var a := deg_to_rad(scene.ALPHA_DEG)
		c.position = Vector3(0.5, 0.0, -3.0) + Vector3(0.0, sin(a), cos(a)) * 250.0
		_sv.add_child(c)
		root.add_child(_sv)
		c.make_current()
	wait += 1
	if wait < settle + 4:
		return false
	var img := _sv.get_texture().get_image()
	var p: String = out_dir.path_join("E0_establishing.png")
	img.save_png(p)
	print("[bv2] establishing ortho size 93.0 m (zero yaw, pitch %.4f) -> %s (%dx%d)" % [scene.ALPHA_DEG, p, img.get_width(), img.get_height()])
	return true


func _film(delta: float) -> bool:
	if not started:
		route = scene.layout["walk_film"]["route"]
		speed = float(scene.layout["walk_film"]["speed_mps"])
		scene.set_zoom(true)
		started = true
	if frame < settle:
		scene.set_walker(Vector2(float(route[0][0]), float(route[0][1])))
		scene.place_camera(Vector2(float(route[0][0]), float(route[0][1])))
		if frame == settle - 1:
			print('[bv2] film {"trim_frames":%d}' % (settle))
		return false
	if seg >= route.size() - 1:
		print("[bv2] film done at frame %d" % frame)
		return true
	var a := Vector2(float(route[seg][0]), float(route[seg][1]))
	var b := Vector2(float(route[seg + 1][0]), float(route[seg + 1][1]))
	var L := a.distance_to(b)
	seg_t += speed * delta
	while seg_t >= L and seg < route.size() - 1:
		seg_t -= L
		seg += 1
		if seg >= route.size() - 1:
			return false
		a = Vector2(float(route[seg][0]), float(route[seg][1]))
		b = Vector2(float(route[seg + 1][0]), float(route[seg + 1][1]))
		L = a.distance_to(b)
	var p := a.lerp(b, seg_t / L)
	scene.set_walker(p, b - a)
	scene.place_camera(p)
	return false
