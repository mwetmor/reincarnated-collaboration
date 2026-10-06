extends SceneTree
## R-C9-159 lane BS: the barrow_v2 SW level (scripts/barrow_v2_sw.gd) -- guide renders, stills, film.
##   godot --path . --resolution 1920x1080 --script tools/v2sw_run.gd -- guide OUT    ground-only guide, the paint frame
##   ... -- lit OUT                                                                    the direct-sun map, the paint frame
##   ... -- stills OUT                                                                 the painted level, v1 camera, 3 views
##   ... --fixed-fps 24 --write-movie X.avi --script tools/v2sw_run.gd -- film        him walking the coast
var scene
var mode := "guide"
var out_dir := ""
var frame := 0
var wait := 0
var k := 0
var sv: SubViewport
var cam: Camera3D
var settle := 10
var legs := []
var wp_i := 0
var best_d := INF
var stall := 0
var settle_end := -1
var hold := 0
var rep := {}


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	mode = args[0]
	if args.size() > 1:
		out_dir = args[1]
	scene = load("res://scenes/barrow_painted.tscn" if mode == "v1stills" else "res://scenes/barrow_v2_sw.tscn").instantiate()
	if mode in ["guide", "lit"]:
		scene.painted = false
		scene.skip_character = true
		scene.v2_mode = mode
	root.add_child(scene)


func _frame() -> Dictionary:
	return scene.lvl["frame"]["paint"]


func _process(_delta: float) -> bool:
	frame += 1
	if not scene.ready_done:
		return false
	if mode in ["guide", "lit"]:
		return _guide()
	if mode == "stills":
		return _stills()
	if mode == "v1stills":
		return _v1stills()
	return _film()


func _guide() -> bool:
	var F := _frame()
	if sv == null:
		scene.set_stack(false)
		if scene.post_q != null:
			scene.post_q.visible = false
		var W := int(F["size_px"][0])
		var H := int(F["size_px"][1])
		sv = SubViewport.new()
		sv.size = Vector2i(W, H)
		sv.world_3d = root.world_3d
		sv.msaa_3d = Viewport.MSAA_4X
		sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		cam = Camera3D.new()
		cam.projection = Camera3D.PROJECTION_ORTHOGONAL
		cam.keep_aspect = Camera3D.KEEP_HEIGHT
		var ppm := float(F["ppm"])
		cam.size = float(H) / ppm
		cam.near = 0.05
		cam.far = 400.0
		sv.add_child(cam)
		root.add_child(sv)
		var p := deg_to_rad(scene.PL_PITCH_DEG)
		var uc := float(F["u0"]) + float(W) / ppm * 0.5
		var sc := float(F["v1"]) * sin(p) - float(H) / ppm * 0.5
		var aim: Vector3 = scene.uv_to_world(uc, sc / sin(p), 0.0)
		cam.global_transform = Transform3D(scene.cam.global_transform.basis, aim - scene.fwd * 60.0)
		cam.make_current()
	wait += 1
	if wait < settle:
		return false
	var img := sv.get_texture().get_image()
	var path: String = out_dir.path_join("v2sw_%s.png" % mode)
	img.save_png(path)
	print("[v2sw] %s %dx%d -> %s" % [mode, img.get_width(), img.get_height(), path])
	return true


func _stills() -> bool:
	# the frame's still targets, S3 lowered 1.4 m of screen so the turned cave and the stair's foot sit in it (inside the painted frame)
	var S: Dictionary = {"S1_wreck": [-47.0, 12.0], "S2_coast": [-27.0, 31.0], "S3_cave_stair": [4.8, 42.2]}
	var ids := S.keys()
	if k >= ids.size():
		print("[v2sw] stills done")
		return true
	var id: String = ids[k]
	var t: Array = S[id]
	if wait == 0:
		scene.set_hud_visible(false)
		var heroes := {"S1_wreck": [-40.5, 8.0, "W"], "S2_coast": [-25.5, 27.0, "S"], "S3_cave_stair": [11.5, 36.0, "S"]}
		var h: Array = heroes.get(id, [t[0], t[1], "S"])
		var huv: Vector2 = scene.world_to_uv(Vector3(float(h[0]), 0.0, float(h[1])))
		scene.place_knight(huv.x, huv.y, String(h[2]))
		scene.park_camera(Vector3(float(t[0]), 0.0, float(t[1])))
	wait += 1
	if wait < settle + 30:
		return false
	var img := root.get_texture().get_image()
	img.save_png(out_dir.path_join("%s.png" % id))
	print("[v2sw] still %s" % id)
	k += 1
	wait = 0
	return false


func _film() -> bool:
	if settle_end < 0:
		if frame >= 72:
			settle_end = frame
			scene.set_hud_visible(false)
			var r: Array = scene.lvl["film_route_xz"]
			for q in r:
				legs.append(scene.world_to_uv(Vector3(float(q[0]), 0.0, float(q[1]))))
			scene.place_knight(legs[0].x, legs[0].y, "S")
			print('[v2sw] film {"trim_frames":%d}' % settle_end)
		return false
	var kn = scene.knight
	var here: Vector2 = scene.knight_uv()
	# the camera LEADS toward the coast (the sea, the ice and the cliff fill the frame's left/bottom half: the water's
	# movement and the coast's heather are what this film is for); it never turns, and stays inside the painted frame
	scene.set_process(false)
	var lead := Vector2(-5.5, 1.0).lerp(Vector2(-4.0, -4.0), clampf((25.0 - here.y) / 30.0, 0.0, 1.0))
	var aim: Vector3 = scene.aim_for(scene.uv_to_world(here.x + lead.x, here.y + lead.y))
	scene.look_at_world(aim)
	if scene.snowfall != null:
		scene.snowfall.global_position = aim + scene.up * 9.0 - scene.fwd * 6.0
	if hold < 24:
		hold += 1
		kn.drive_dir(Vector2.ZERO, false, 1.0 / 24.0)
		return false
	if wp_i >= legs.size():
		kn.drive_dir(Vector2.ZERO, false, 1.0 / 24.0)
		hold += 1
		if hold > 24 + 48:
			print("[v2sw] film done frames=%d" % (frame - settle_end))
			return true
		return false
	var target: Vector2 = legs[wp_i]
	var d := here.distance_to(target)
	if d < best_d - 0.005:
		best_d = d
		stall = 0
	else:
		stall += 1
	if d < 0.3 or stall > 36:
		if stall > 36:
			rep.get_or_add("passed_by", []).append([wp_i, snappedf(best_d, 0.01)])
		wp_i += 1
		best_d = INF
		stall = 0
		if wp_i >= legs.size():
			hold = 24
			print("[v2sw] route ", JSON.stringify(rep))
		return false
	kn.drive_dir(scene.canvas_dir_uv(here, target), false, 1.0 / 24.0)
	return false


## the v1 Barrow, as live (scenes/barrow_painted.tscn), at three places, for Matt's consistency check
func _v1stills() -> bool:
	var S := [["V1_tarn", Vector2(-6.0, -7.0)], ["V1_ring", Vector2(2.0, 1.0)], ["V1_door", Vector2(0.0, 6.5)]]
	if k >= S.size():
		print("[v2sw] v1 stills done")
		return true
	if wait == 0:
		scene.set_hud_visible(false)
		scene.set_crucible_visible(false)
		var uv: Vector2 = S[k][1]
		scene.place_knight(uv.x - 1.5, uv.y - 1.0, "S")
		scene.park_camera(scene.uv_to_world(uv.x, uv.y))
	wait += 1
	if wait < settle + 30:
		return false
	root.get_texture().get_image().save_png(out_dir.path_join("%s.png" % S[k][0]))
	print("[v2sw] v1 still %s" % S[k][0])
	k += 1
	wait = 0
	return false
