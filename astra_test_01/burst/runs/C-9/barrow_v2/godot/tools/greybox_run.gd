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
	return _film(delta)


func _views() -> bool:
	var views: Array = scene.layout["views"]
	var shots: Array = []
	for v in views:
		shots.append({"id": v["id"], "t": Vector2(float(v["target"][0]), float(v["target"][1])), "gd": true})
	shots.append({"id": "V0_start_plate_scale", "t": Vector2.ZERO, "gd": false})
	if vi >= shots.size():
		print("[bv2] views done: %d" % shots.size())
		return true
	var s: Dictionary = shots[vi]
	if wait == 0:
		scene.set_zoom(s["gd"])
		scene.place_camera(s["t"])
		scene.set_walker(s["t"] + Vector2(0.0, 1.5), Vector2(0, 1))
	wait += 1
	if wait < settle:
		return false
	var img := root.get_texture().get_image()
	var p: String = out_dir.path_join("%s.png" % s["id"])
	img.save_png(p)
	print("[bv2] view %s target %s ppm %.4f cam.size %.5f -> %s (%dx%d)" % [s["id"], s["t"], scene.ppm, scene.cam.size, p, img.get_width(), img.get_height()])
	vi += 1
	wait = 0
	return false


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
