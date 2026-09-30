extends SceneTree
## C-9 T10-2 steps 4-5: THE PAINTED BARROW, CAPTURED -- the guide frame for the overlay check,
## and play-camera stills of him in it. drax.
##
##   Godot --path godot --resolution 640x360 --script tools/capture_painted.gd -- --out DIR
##         [--guide] [--stills] [--variants inpainted,as_painted] [--heather-mul r,g,b]
##
## --guide   (step 5) the painted scene WITHOUT him at the guide camera, 5376 x 3328, MSAA 4x, the
##           guide's shadow atlas (8192), the wind held still, no falling snow -- per ground variant:
##             guide_<variant>.png      the frame, as drawn (the pen on the heather, as in play)
##             heather_mask.png         the 3D heather alone, white, where it is SEEN (everything
##                                      else drawn black in place, so a stone in front still hides it)
##             heather_colour.png       the 3D heather as drawn, over the same black: its own colour
## --stills  play-camera frames (1920 x 1080) of him, armed, in the assembled Barrow:
##             still_<name>.png  + where he stood and what the suns and his shadow did there

const GUIDE := Vector2i(5376, 3328)
const PLAY := Vector2i(1920, 1080)
const DT := 1.0 / 60.0
# ring_m55's cast shadow's centroid, found in the desktop's light map (_shadow_centroid, half the
# guide): FIXED here, so the desktop and the phone's renderer stand him on the same spot -- the
# phone's quarter-size map finds it 3 cm away, and 3 px of shifted frame is not a renderer difference
const RING_M55_SHADOW := Vector2(-6.39, 6.9)

var out_dir := ""
var do_guide := false
var do_stills := false
var do_shadow_test := false
var do_trail := false
var do_cast := false                # --cast: her two spells, frames at each release and after
var do_feet := false                # --feet: foot-lock against asked speed, walk and run
var feet_passes := 1                # --feet-passes N: N straight passes per gait, alternating east / west, pooled
var quiet := false                  # --quiet: no falling snow, the wind held -- frames that compare
var no_pen := false                 # --no-pen: the post pass hidden (a diagnostic)
var variants := ["inpainted", "as_painted"]
var heather_mul = null
var vp: SubViewport
var scene
var rep := {}


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		var a := String(args[i])
		var nxt := String(args[i + 1]) if i + 1 < args.size() else ""
		if a == "--out":
			out_dir = nxt
		elif a == "--guide":
			do_guide = true
		elif a == "--stills":
			do_stills = true
		elif a == "--shadow-test":
			do_shadow_test = true
		elif a == "--trail":
			do_trail = true
		elif a == "--cast":
			do_cast = true
		elif a == "--feet":
			do_feet = true
		elif a == "--feet-passes":
			feet_passes = maxi(1, int(nxt))
		elif a == "--quiet":
			quiet = true
		elif a == "--no-pen":
			no_pen = true
		elif a == "--variants":
			variants = Array(nxt.split(","))
		elif a == "--heather-mul":
			var p := nxt.split(",")
			heather_mul = Vector3(float(p[0]), float(p[1]), float(p[2]))
	if out_dir == "" or not (do_guide or do_stills or do_shadow_test or do_trail or do_cast or do_feet):
		print("[painted] HALT: --out DIR and one of --guide / --stills are required")
		quit(2)
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = PLAY
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/barrow_painted.tscn").instantiate()
	scene.skip_character = not (do_stills or do_shadow_test or do_trail or do_cast or do_feet)
	vp.add_child(scene)
	var waited := 0
	while not scene.ready_done and waited < 3000:
		await process_frame
		waited += 1
	if not scene.ready_done:
		print("[painted] HALT: the scene never finished building")
		quit(3)
		return
	rep["painted"] = scene.report.get("painted", {})
	rep["launch_line"] = scene._paint_launch_line()
	print("[painted] " + rep["launch_line"])
	if heather_mul != null:
		scene.heather_mat.set_shader_parameter("albedo_mul", heather_mul)
		rep["heather_albedo_mul_override"] = [heather_mul.x, heather_mul.y, heather_mul.z]
	scene.set_hud_visible(false)
	scene.set_overlay(false)
	scene.set_crucible_visible(false)
	for c in scene.get_children():
		if c is CanvasLayer:
			(c as CanvasLayer).visible = false      # the thumb controls, when the web branches run
	if no_pen:
		scene.post_q.visible = false
	if quiet:
		scene.heather_mat.set_shader_parameter("wind_on", 0.0)
		if scene.snowfall != null:
			scene.snowfall.visible = false
			scene.snowfall.emitting = false
	rep["renderer"] = {"method": RenderingServer.get_current_rendering_method(), "web_branches": PaintStack.is_web(),
		"adapter": RenderingServer.get_video_adapter_name()}
	if do_guide:
		await _guide()
	if do_stills:
		await _stills()
	if do_shadow_test:
		await _shadow_test()
	if do_trail:
		await _trail()
	if do_cast:
		await _cast()
	if do_feet:
		await _feet()
	var f := FileAccess.open(out_dir.path_join("capture_painted.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(rep, " "))
	f.close()
	print("[painted] -> %s" % out_dir)
	quit(0)


func _settle(n := 8) -> void:
	for i in n:
		await physics_frame
		await process_frame
	RenderingServer.force_draw()
	await process_frame


func _shot(nm: String) -> void:
	for i in 3:
		await process_frame
	var img: Image = vp.get_texture().get_image()
	if img.get_width() != vp.size.x or img.get_height() != vp.size.y:
		print("[painted] SIZE MISMATCH %s" % nm)
	img.save_png(out_dir.path_join(nm + ".png"))
	print("[painted] %s.png %dx%d" % [nm, img.get_width(), img.get_height()])


func _set_ground(variant: String) -> void:
	var man := PaintedWorld.read_manifest()
	var key := "ground_" + variant
	var loads := {}
	var tex := PaintedWorld.load_png_bin(String(man[key]["file"]), String(man[key]["sha256"]), true, loads)
	var g := scene.level.get_node(^"Ground") as MeshInstance3D
	(g.material_override as ShaderMaterial).set_shader_parameter("paint_tex", tex)
	scene.snow.material().set_shader_parameter("paint_tex", tex)
	rep.get_or_add("ground_loads", {})[variant] = loads


func _guide() -> void:
	RenderingServer.directional_shadow_atlas_set_size(8192, true)
	vp.size = GUIDE
	scene.heather_mat.set_shader_parameter("wind_on", 0.0)
	if scene.snowfall != null:
		scene.snowfall.visible = false
	var gw: Dictionary = scene.layout["frame"]["guide_window"]
	var gc: Array = gw["centre_uv"]
	scene.park_camera(scene.uv_to_world(float(gc[0]), float(gc[1])), 1.0)
	for v in variants:
		_set_ground(String(v))
		await _settle()
		await _shot("guide_" + String(v))
	# THE HEATHER, ALONE WHERE IT IS SEEN: every painted surface black, the snow black (its own
	# id mode), the heather white by emission -- one frame, same camera, same depth
	var saved := {}
	for mi in scene.find_children("*", "MeshInstance3D", true, false):
		var m := (mi as MeshInstance3D).material_override as ShaderMaterial
		if m != null and m.shader != null and m.shader.code.contains("uniform bool id_black"):
			m.set_shader_parameter("id_black", true)
			saved[m] = true
	scene.snow.set_id_black(true)
	scene.post_q.visible = false
	# AND ITS COLOUR, alone: the sprays as drawn, over black -- with the mask's coverage this is the
	# stems' own colour, unmixed with the ground between them (the grade is calibrated on it)
	await _settle()
	await _shot("heather_colour")
	scene.heather_mat.set_shader_parameter("id_white", true)
	await _settle()
	await _shot("heather_mask")
	for m in saved:
		(m as ShaderMaterial).set_shader_parameter("id_black", false)
	scene.snow.set_id_black(false)
	scene.heather_mat.set_shader_parameter("id_white", false)
	scene.post_q.visible = true
	scene.heather_mat.set_shader_parameter("wind_on", 1.0)
	rep["guide"] = {"px": [GUIDE.x, GUIDE.y], "centre_uv": gc, "variants": variants, "shadow_atlas_px": 8192,
		"wind": "held still for the overlay", "falling_snow": "hidden for the overlay", "him": "absent (the guide's barbarian was painted out)"}
	vp.size = PLAY
	scene.unpark_camera()
	if scene.snowfall != null:
		scene.snowfall.visible = true


func _stills() -> void:
	var k = scene.knight
	var spots := [
		# name, where he stands (u, v), facing, what it shows
		["tarn_path", Vector2(-6.0, -7.5), "W", "the path by the tarn"],
		["ring_shadow", RING_M55_SHADOW, "S", "inside ring_m55's painted shadow"],
		["door", Vector2(0.0, 7.2), "N", "the cutting, the door ahead"],
		["open_sun", Vector2(1.5, -1.0), "E", "open sunlit snow in the ring: his own shadow on the painting"],
	]
	var out := {}
	for s in spots:
		scene.place_knight(float(s[1].x), float(s[1].y), String(s[2]))
		for i in 30:
			k.drive_dir(Vector2.ZERO, false, DT)
			await physics_frame
		await _settle(4)
		await _shot("still_" + String(s[0]))
		var at: Vector2 = scene.knight_uv()
		out[String(s[0])] = {"uv": [snappedf(at.x, 0.01), snappedf(at.y, 0.01)], "facing": s[2], "shows": s[3],
			"painted_light_at_his_feet": _lit_at(at)}
	rep["stills"] = out
	rep["him_in_a_painted_shadow"] = await _him_in_shadow()


func _him_pixels(nm: String) -> Dictionary:
	"""His own pixels: the frame with him, and again with him hidden -- what changed is him (and his
	shadow on the ground, which the brightness test below keeps out: it only darkens)."""
	var k = scene.knight
	await _settle(4)
	await _shot(nm)
	var with_him: Image = vp.get_texture().get_image()
	k.visible = false
	await _settle(4)
	var without: Image = vp.get_texture().get_image()
	k.visible = true
	var r: Rect2 = scene.character_screen_rect().grow(40.0)
	var acc := Vector3.ZERO
	var n := 0
	for y in range(maxi(int(r.position.y), 0), mini(int(r.end.y), with_him.get_height())):
		for x in range(maxi(int(r.position.x), 0), mini(int(r.end.x), with_him.get_width())):
			var a := with_him.get_pixel(x, y)
			var b := without.get_pixel(x, y)
			if absf(a.r - b.r) + absf(a.g - b.g) + absf(a.b - b.b) > 0.06:
				var l := a.srgb_to_linear()
				var bl := b.srgb_to_linear()
				# his shadow on the ground is darker than the ground and the same hue; he is not
				# the ground: keep a pixel only if it is not merely a darkened copy of what was there
				var ratio := Vector3(l.r / maxf(bl.r, 1e-4), l.g / maxf(bl.g, 1e-4), l.b / maxf(bl.b, 1e-4))
				if absf(ratio.x - ratio.y) < 0.06 and absf(ratio.y - ratio.z) < 0.06 and ratio.y < 1.0:
					continue
				acc += Vector3(l.r, l.g, l.b)
				n += 1
	return {"px": n, "mean_linear": [snappedf(acc.x / maxf(n, 1), 0.0001), snappedf(acc.y / maxf(n, 1), 0.0001), snappedf(acc.z / maxf(n, 1), 0.0001)]}


func _him_in_shadow() -> Dictionary:
	"""(b), MEASURED: the same pose, facing the same way, in ring_m55's painted shadow and 1.6 m
	south of it in the sun -- his own pixels' mean colour, and the ratio."""
	var k = scene.knight
	var c := RING_M55_SHADOW
	var out := {"stone": "ring_m55", "shadow_centroid_uv": [snappedf(c.x, 0.01), snappedf(c.y, 0.01)]}
	for spot in [["in_shadow", c], ["in_sun", c + Vector2(0.0, -1.6)]]:
		scene.place_knight(float(spot[1].x), float(spot[1].y), "S")
		for i in 30:
			k.drive_dir(Vector2.ZERO, false, DT)
			await physics_frame
		scene.freeze_pose(true)
		out[spot[0]] = await _him_pixels("him_" + String(spot[0]))
		out[spot[0]]["lit_at_his_feet"] = _lit_at(scene.knight_uv())
		scene.freeze_pose(false)
	var a: Array = out["in_shadow"]["mean_linear"]
	var b: Array = out["in_sun"]["mean_linear"]
	out["shadow_over_sun_linear"] = [snappedf(a[0] / maxf(b[0], 1e-4), 0.001), snappedf(a[1] / maxf(b[1], 1e-4), 0.001),
									 snappedf(a[2] / maxf(b[2], 1e-4), 0.001)]
	return out


func _shadow_centroid(id: String) -> Vector2:
	var base: Vector2 = scene.world_to_uv((scene.nodes[id] as Node3D).global_position)
	var acc := Vector2.ZERO
	var n := 0
	for j in 19:
		for i in 22:
			var p := base + Vector2(0.5 + 0.1 * i, -1.2 + 0.1 * j)
			if _lit_at(p) < 0.2:
				acc += p
				n += 1
	return acc / maxf(float(n), 1.0)


func _in_a_stone_shadow(id: String) -> Vector2:
	"""A point in the stone's CAST shadow on the ground, found by walking from the stone's base
	away from the sun (the sun's ground direction, from the scene's own light) until the painted
	light map says shadow -- then 0.25 m further in."""
	var root := scene.nodes[id] as Node3D
	var base: Vector2 = scene.world_to_uv(root.global_position)
	var sd: Vector3 = scene.sun.global_transform.basis.z      # toward the sun
	var away := -Vector2(sd.dot(scene.u_hat), sd.dot(scene.v_hat)).normalized()
	for i in 60:
		var p := base + away * (0.1 * float(i))
		if _lit_at(p) < 0.2 and i > 3:
			return p + away * 0.25
	return base + away * 1.0


func _lit_at(uv: Vector2) -> float:
	var lit: Texture2D = scene._paint_tex.get("lit")
	if lit == null:
		return -1.0
	var img := lit.get_image()
	# THE MAP'S OWN SCALE: half the guide on the desktop, a quarter on the phone page's data
	var k := float(img.get_width()) / PaintedWorld.GUIDE_PX.x
	var x := (uv.x - PaintedWorld.U0) * PaintedWorld.PPM * k
	var y := (PaintedWorld.V1 - uv.y) * PaintedWorld.PPM * sin(deg_to_rad(PaintedWorld.PITCH_DEG)) * k
	if x < 0 or y < 0 or x >= img.get_width() or y >= img.get_height():
		return -1.0
	return snappedf(img.get_pixel(int(x), int(y)).r, 0.01)


func _set_his_shadow(on: bool) -> void:
	for mi in scene.find_children("*", "GeometryInstance3D", true, false):
		var m := (mi as GeometryInstance3D).material_override as ShaderMaterial
		if m != null and m.shader != null and m.shader.code.contains("his_shadow_on"):
			m.set_shader_parameter("his_shadow_on", 1.0 if on else 0.0)


func _shadow_test() -> void:
	"""HIS SHADOW ON THE PAINTING, per shadow configuration: two frames each -- his shadow term
	on, and off -- so the difference IS his shadow and nothing else. Both suns take the setting."""
	var k = scene.knight
	scene.place_knight(1.5, -1.0, "E")
	for i in 30:
		k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
	scene.freeze_pose(true)
	if scene.snowfall != null:
		scene.snowfall.visible = false
	# [name, mode, max distance, split_1, atlas, soft filter quality, blur] -- the PAINT SUN only
	# (his shadow on the painting); the sun keeps the installed setting
	var configs := [
		["A_installed", DirectionalLight3D.SHADOW_ORTHOGONAL, 110.0, 0.1, 4096, RenderingServer.SHADOW_QUALITY_SOFT_LOW, 1.7],
		["E_pssm2_blur06", DirectionalLight3D.SHADOW_PARALLEL_2_SPLITS, 68.0, 0.78, 4096, RenderingServer.SHADOW_QUALITY_SOFT_LOW, 0.6],
		["F_pssm2_blur06_8k", DirectionalLight3D.SHADOW_PARALLEL_2_SPLITS, 68.0, 0.78, 8192, RenderingServer.SHADOW_QUALITY_SOFT_LOW, 0.6],
		["G_ortho68_blur06", DirectionalLight3D.SHADOW_ORTHOGONAL, 68.0, 0.1, 4096, RenderingServer.SHADOW_QUALITY_SOFT_LOW, 0.6],
		["H_pssm2_blur1_8k", DirectionalLight3D.SHADOW_PARALLEL_2_SPLITS, 68.0, 0.78, 8192, RenderingServer.SHADOW_QUALITY_SOFT_LOW, 1.0],
		["I_pssm2_blur06_medium", DirectionalLight3D.SHADOW_PARALLEL_2_SPLITS, 68.0, 0.78, 4096, RenderingServer.SHADOW_QUALITY_SOFT_MEDIUM, 0.6],
	]
	var out := {}
	scene.heather_mat.set_shader_parameter("wind_on", 0.0)
	for c in configs:
		var l: DirectionalLight3D = scene.paint_sun
		l.directional_shadow_mode = c[1]
		l.directional_shadow_max_distance = c[2]
		l.directional_shadow_split_1 = c[3]
		l.shadow_blur = c[6]
		RenderingServer.directional_shadow_atlas_set_size(c[4], true)
		RenderingServer.directional_soft_shadow_filter_set_quality(c[5])
		_set_his_shadow(true)
		await _settle(6)
		await _shot("shadow_%s_on" % c[0])
		_set_his_shadow(false)
		await _settle(6)
		await _shot("shadow_%s_off" % c[0])
		out[c[0]] = {"mode": c[1], "max_distance": c[2], "split_1": c[3], "atlas": c[4], "soft_filter_quality": c[5], "blur": c[6]}
	_set_his_shadow(true)
	var hs: Vector2 = scene.cam.unproject_position(k.global_position)
	rep["shadow_test"] = {"configs": out, "him_screen_px": [hs.x, hs.y], "him_uv": [1.5, -1.0]}


func _trail() -> void:
	"""THE SNOW-TRAIL POLISH, MEASURED. He walks a line over open arena snow; the camera is parked
	over it; then the SAME trail is shot in both shadings -- the first version (trail_relief_only
	0) and the polish (1) -- against the same ground shot before he walked, and an id frame marks
	where the trail is (press red, berm green). Wind still, no falling snow, him hidden for the
	shots. tools/trail_polish.py measures the frames."""
	var k = scene.knight
	var smat: ShaderMaterial = scene.snow.material()
	scene.heather_mat.set_shader_parameter("wind_on", 0.0)
	if scene.snowfall != null:
		scene.snowfall.visible = false
	var start := Vector2(-1.8, -3.0)
	var aim: Vector3 = scene.uv_to_world(1.6, -2.2)
	scene.place_knight(start.x, start.y, "E")
	for i in 20:
		k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
	scene.park_camera(aim, 1.0)
	k.visible = false
	await _settle(4)
	await _shot("trail_untouched")
	k.visible = true
	# a walk east, a turn north-east: ~7 m of prints and berms. HIS OWN physics tick is off while
	# the script drives him (it drives him too -- with no keys held, a zero stick every frame,
	# which held the first walk to 1.6 m of 7)
	k.set_physics_process(false)
	for leg in [[Vector2(3.4, -3.0), 420], [Vector2(4.8, -1.2), 200]]:
		for i in int(leg[1]):
			if scene.knight_uv().distance_to(leg[0]) < 0.25:
				break
			k.drive_dir(scene.canvas_dir_uv(scene.knight_uv(), leg[0]), false, DT)
			await physics_frame
	for i in 10:
		k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
	k.set_physics_process(true)
	rep["trail_walk_end_uv"] = [snappedf(scene.knight_uv().x, 0.01), snappedf(scene.knight_uv().y, 0.01)]
	k.visible = false
	scene.park_camera(aim, 1.0)
	for mode in [0.0, 1.0]:
		smat.set_shader_parameter("trail_relief_only", mode)
		await _settle(3)
		await _shot("trail_mode%d" % int(mode))
	# the id frame: everything black, the trail's press red and berm green
	var saved := []
	for mi in scene.find_children("*", "GeometryInstance3D", true, false):
		var m := (mi as GeometryInstance3D).material_override as ShaderMaterial
		if m != null and m.shader != null and m.shader.code.contains("uniform bool id_black"):
			m.set_shader_parameter("id_black", true)
			saved.append(m)
	for mmi in scene._heather_mmi:
		(mmi as Node3D).visible = false
	smat.set_shader_parameter("trail_id", true)
	scene.post_q.visible = false
	await _settle(3)
	await _shot("trail_id")
	smat.set_shader_parameter("trail_id", false)
	smat.set_shader_parameter("trail_relief_only", 1.0)
	for m in saved:
		(m as ShaderMaterial).set_shader_parameter("id_black", false)
	for mmi in scene._heather_mmi:
		(mmi as Node3D).visible = true
	scene.post_q.visible = true
	k.visible = true
	rep["trail"] = {"walk_uv": [[start.x, start.y], [3.4, -3.0], [4.8, -1.2]], "camera_aim_uv": [1.6, -2.2],
		"frames": ["trail_untouched", "trail_mode0 (the first version)", "trail_mode1 (the polish)", "trail_id (press R, berm G)"]}


func _cast() -> void:
	"""HER TWO SPELLS (run with -- --c sorceress): the Fire Ball, then the Meteor, each fired as the
	SLASH / CHOP keys fire them (try_strike), with frames at the release and after it. The frames and
	spell_fx's own record of when and where each fired."""
	var k = scene.knight
	if scene.who != "sorceress" or scene.spell_fx == null:
		rep["cast"] = {"error": "not the sorceress (run with -- --c sorceress)"}
		return
	scene.place_knight(1.5, -1.5, "E")
	for i in 30:
		k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
	var shots := {}
	for spec in [["slash", "fireball", [0.3, 0.6, 0.92, 1.25]], ["chop", "meteor", [0.8, 1.64, 1.9, 2.2]]]:
		# his own physics tick runs (the strike as the keys fire it); nothing drives him meanwhile
		var ok: bool = k.try_strike(String(spec[0]))
		var t0 := Time.get_ticks_usec()
		var t := 0.0
		var marks: Array = spec[2]
		var mi := 0
		var frames := 0
		while frames < 400 and mi < marks.size():
			await physics_frame
			frames += 1
			t = float(frames) / float(Engine.physics_ticks_per_second)
			if t >= float(marks[mi]):
				await _shot("cast_%s_%.2fs" % [spec[1], float(marks[mi])])
				shots["%s_%.2f" % [spec[1], float(marks[mi])]] = {"attacking": k.attacking(), "strike_anim": String(k._strike_anim)}
				mi += 1
		for i in 240:
			await physics_frame
			if not k.attacking():
				break
		shots[String(spec[1]) + "_fired"] = ok
	rep["cast"] = {"shots": shots, "spell_fx": scene.spell_fx.report}


func _feet() -> void:
	"""HIS OR HER FEET AGAINST THE SPEED ASKED (the coordinator, T12_10: "measure her feet -- foot-lock /
	asked -- before and after"). She is driven in a straight line across the arena, at walk and at
	run, by the same drive_dir the keys use (her own tick off, so nothing else drives her), and every
	physics frame records the body and the four foot joints in world space. The STANCE foot is the
	lower of the two (its toe within 3 cm of its lowest over the run). Per gait:
	  asked      the body's own ground speed, m/s (what knight.gd drives her at)
	  foot_lock  the stance foot's speed RELATIVE TO THE BODY, m/s -- the stride the clip plays
	  ratio      foot_lock / asked: 1.0 = the feet grip the ground; 1.25 = the clip strides a quarter
	             faster than she moves, and the planted foot skates
	  skate      the stance foot's own ground speed, m/s (0 = planted)"""
	var k = scene.knight
	var sk: Skeleton3D = k._skel
	var bones := {}
	for nm in ["LeftFoot", "LeftToeBase", "RightFoot", "RightToeBase"]:
		bones[nm] = sk.find_bone(nm)
	var out := {"who": scene.who, "knight_md5": FileAccess.get_md5("res://scripts/knight.gd").substr(0, 8)}
	out["passes"] = feet_passes
	for gait in [["walk", false], ["run", true]]:
		# pass 0 is T12_10's measure exactly (east from u -5); further passes alternate west and
		# east across the same strip and pool their frames (a pass's first pair is never paired
		# with the last pass's end: its clock restarts, and _feet_stats skips dt <= 0)
		var rows := []
		for pass_i in feet_passes:
			var east := pass_i % 2 == 0
			scene.place_knight(-5.0 if east else 5.0, -2.0, "E" if east else "W")
			for i in 20:
				k.drive_dir(Vector2.ZERO, false, DT)
				await physics_frame
			k.set_physics_process(false)
			var t := 0.0
			while t < 6.0 and (scene.knight_uv().x < 5.0 if east else scene.knight_uv().x > -5.0):
				k.drive_dir(Vector2(1 if east else -1, 0), bool(gait[1]), DT)
				await physics_frame
				t += DT
				if t < 0.8:
					continue
				var fr := {"t": t, "body": k.global_position}
				for nm in bones:
					fr[nm] = (sk.global_transform * sk.get_bone_global_pose(bones[nm])).origin
				rows.append(fr)
			k.set_physics_process(true)
			for i in 20:
				await physics_frame
		out[String(gait[0])] = _feet_stats(rows)
	rep["feet"] = out
	print("[painted] feet " + JSON.stringify(out))


func _feet_stats(rows: Array) -> Dictionary:
	if rows.size() < 10:
		return {"error": "too few frames (%d)" % rows.size()}
	var lo := {"L": INF, "R": INF}
	for fr in rows:
		lo["L"] = minf(lo["L"], (fr["LeftToeBase"] as Vector3).y)
		lo["R"] = minf(lo["R"], (fr["RightToeBase"] as Vector3).y)
	var asked := []
	var lock := []
	var skate := []
	for i in range(1, rows.size()):
		var a: Dictionary = rows[i - 1]
		var b: Dictionary = rows[i]
		var dt: float = float(b["t"]) - float(a["t"])
		if dt <= 0.0:
			continue
		var vb: Vector3 = (b["body"] - a["body"]) / dt
		vb.y = 0.0
		var side := "L" if (b["LeftToeBase"] as Vector3).y <= (b["RightToeBase"] as Vector3).y else "R"
		var toe := "LeftToeBase" if side == "L" else "RightToeBase"
		if (b[toe] as Vector3).y > float(lo[side]) + 0.03:
			continue
		var foot := "LeftFoot" if side == "L" else "RightFoot"
		var vf: Vector3 = ((b[foot] - a[foot]) + (b[toe] - a[toe])) * 0.5 / dt
		vf.y = 0.0
		asked.append(vb.length())
		lock.append((vb - vf).length())
		skate.append(vf.length())
	if asked.is_empty():
		return {"error": "no stance frames"}
	asked.sort()
	lock.sort()
	skate.sort()
	var med := func(v: Array) -> float: return float(v[v.size() / 2])
	return {"stance_frames": asked.size(), "asked_m_s": snappedf(med.call(asked), 0.001),
		"foot_lock_m_s": snappedf(med.call(lock), 0.001),
		"ratio_foot_lock_over_asked": snappedf(med.call(lock) / maxf(med.call(asked), 1e-4), 0.001),
		"skate_m_s_median": snappedf(med.call(skate), 0.001), "skate_m_s_p90": snappedf(float(skate[int(skate.size() * 0.9)]), 0.001)}
