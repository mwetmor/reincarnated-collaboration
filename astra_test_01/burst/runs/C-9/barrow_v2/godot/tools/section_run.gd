extends SceneTree
## barrow_v2 SECTION SW runner (R-C9-158, lane BS).
##   guide  OUT                 -> OUT/tile_<i>_<j>.png: the section at the game camera (ortho, pitch 52.95, yaw 0)
##                                 at PLATE density (100.6 px/m), 4 x 4 tiles of 1984 x 1216 = the 7936 x 4864 frame
##   stills OUT [paint=PNG]     -> OUT/<id>.png: V3 wreck, V-coast, V7 cave/stair at ZOOM-GD (75.67 px/m), 1920 x 1080,
##                                 the hero standing on the floor
##   film   [paint=PNG]         -> (with --write-movie) the hero runs the coast on the floor; the camera follows
var scene: Node3D
var mode := "guide"
var out_dir := ""
var frame := 0
var wait := 0
var k := 0
var sv: SubViewport
var cam: Camera3D
const TW := 1984
const TH := 1216
var F: Dictionary
var shots := []
var route: Array = []
var seg := 0
var seg_t := 0.0
var speed := 5.2
var settle := 8


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	mode = args[0]
	if args.size() >= 2 and not args[1].begins_with("paint="):
		out_dir = args[1]
	scene = load("res://scenes/section_sw.tscn").instantiate()
	root.add_child(scene)


func _sec() -> Dictionary:
	return scene.sec


func _place(c: Camera3D, sx: float, sy: float) -> void:
	# centre the ortho camera on SCREEN metres (sx, sy): screen_x = x, screen_y = sin(a) y - cos(a) z
	var a := deg_to_rad(scene.ALPHA_DEG)
	var t := Vector3(sx, 0.0, sy / sin(a))
	c.position = t + Vector3(0.0, sin(a), cos(a)) * 160.0


func _process(delta: float) -> bool:
	frame += 1
	if scene.cam == null:
		return false
	scene.free_cam = true
	if mode == "guide":
		return _guide()
	if mode == "stills":
		return _stills()
	if mode == "overview":
		return _overview()
	return _film(delta)


func _guide() -> bool:
	F = _sec()["frame"]
	if sv == null:
		sv = SubViewport.new()
		sv.size = Vector2i(TW, TH)
		sv.world_3d = root.world_3d
		sv.msaa_3d = Viewport.MSAA_4X
		sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		cam = Camera3D.new()
		cam.projection = Camera3D.PROJECTION_ORTHOGONAL
		cam.keep_aspect = Camera3D.KEEP_HEIGHT
		cam.size = float(TH) / float(F["ppm"])
		cam.near = 1.0
		cam.far = 400.0
		cam.rotation_degrees = Vector3(-scene.ALPHA_DEG, 0.0, 0.0)
		sv.add_child(cam)
		root.add_child(sv)
		cam.make_current()
	var nx := int(F["size_px"][0]) / TW
	var ny := int(F["size_px"][1]) / TH
	if k >= nx * ny:
		print("[sw] guide tiles done %d" % k)
		return true
	var i := k % nx
	var j := k / nx
	if wait == 0:
		var ppm := float(F["ppm"])
		_place(cam, float(F["sx0_m"]) + (i + 0.5) * TW / ppm, float(F["sy0_m"]) + (j + 0.5) * TH / ppm)
	wait += 1
	if wait < settle:
		return false
	var img := sv.get_texture().get_image()
	img.save_png(out_dir.path_join("tile_%d_%d.png" % [i, j]))
	print("[sw] tile %d %d" % [i, j])
	k += 1
	wait = 0
	return false


const STILLS := [
	# V3's window, shifted 5 m west so the wreck and its shore ice sit in frame (the layout's V3 target leaves them on the edge)
	{"id": "S1_V3_wreck", "t": [-44.0, 12.0], "hero": [-40.6, 13.2], "face": [-1, 0.1]},
	{"id": "S2_coast", "t": [-27.0, 32.0], "hero": [-26.0, 26.4], "face": [0.2, 1]},
	{"id": "S3_V7_cave_stair", "t": [5.79, 42.6977], "hero": [13.8, 35.4], "face": [0.2, 1]},
]


func _stills() -> bool:
	if k >= STILLS.size():
		print("[sw] stills done")
		return true
	var s: Dictionary = STILLS[k]
	if wait == 0:
		scene.set_zoom(true)
		scene.place_camera(Vector2(float(s["t"][0]), float(s["t"][1])))
		scene.set_hero(Vector2(float(s["hero"][0]), float(s["hero"][1])), Vector2(float(s["face"][0]), float(s["face"][1])), "idle")
	wait += 1
	if wait < settle:
		return false
	var img := root.get_texture().get_image()
	img.save_png(out_dir.path_join("%s.png" % s["id"]))
	print("[sw] still %s" % s["id"])
	k += 1
	wait = 0
	return false


func _film(delta: float) -> bool:
	if route.is_empty():
		route = _sec()["film_route"]
		scene.set_zoom(true)
	var p0 := Vector2(float(route[0][0]), float(route[0][1]))
	if frame < settle:
		scene.set_hero(p0, Vector2(float(route[1][0]), float(route[1][1])) - p0, "run")
		scene.place_camera(_lead(p0))
		if frame == settle - 1:
			print('[sw] film {"trim_frames":%d}' % settle)
		return false
	if seg >= route.size() - 1:
		print("[sw] film done at frame %d" % frame)
		return true
	var a := Vector2(float(route[seg][0]), float(route[seg][1]))
	var b := Vector2(float(route[seg + 1][0]), float(route[seg + 1][1]))
	var L := a.distance_to(b)
	seg_t += speed * delta
	while seg_t >= L:
		seg_t -= L
		seg += 1
		if seg >= route.size() - 1:
			return false
		a = Vector2(float(route[seg][0]), float(route[seg][1]))
		b = Vector2(float(route[seg + 1][0]), float(route[seg + 1][1]))
		L = a.distance_to(b)
	var p := a.lerp(b, seg_t / L)
	scene.set_hero(p, b - a, "run")
	scene.place_camera(_lead(p))
	return false


func _overview() -> bool:
	if sv == null:
		for ch in scene.static_root.get_children():
			if ch is Node3D:
				var ab: AABB = scene._aabb_of(ch, (ch.get_parent() as Node3D).global_transform)
				if ab.size.x > 30.0 or ab.size.z > 30.0 or ab.size.y > 16.0:
					print("[sw] BIG %s %s" % [ch.name, ab])
		if scene.hero != null:
			print("[sw] hero aabb %s scale %s" % [scene._aabb_of(scene.hero, Transform3D.IDENTITY), scene.hero.get_child(0).scale])
		sv = SubViewport.new()
		sv.size = Vector2i(1984, 1216)
		sv.world_3d = root.world_3d
		sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		cam = Camera3D.new()
		cam.projection = Camera3D.PROJECTION_ORTHOGONAL
		cam.keep_aspect = Camera3D.KEEP_HEIGHT
		cam.size = 50.0
		cam.near = 1.0
		cam.far = 400.0
		cam.rotation_degrees = Vector3(-scene.ALPHA_DEG, 0.0, 0.0)
		sv.add_child(cam)
		root.add_child(sv)
		cam.make_current()
		_place(cam, -18.0, 20.0)
		scene.set_hero(Vector2(-30.0, 20.0), Vector2(0, 1), "idle")
	wait += 1
	if wait < settle:
		return false
	sv.get_texture().get_image().save_png(out_dir.path_join("overview.png"))
	print("[sw] overview saved")
	return true


## the game camera never turns; for the pan it LEADS toward the coast (west at the wreck, south along the cliff) so the
## shore fills the window, and it is clamped so the window never leaves the painted frame (x -57.5 .. 21.37 m)
func _lead(p: Vector2) -> Vector2:
	var off := Vector2(-6.0, 1.0).lerp(Vector2(-1.0, 5.5), clampf((p.y - 8.0) / 16.0, 0.0, 1.0))
	var t := p + off
	t.x = clampf(t.x, -44.7, 8.6)
	return t
