extends SceneTree
# R-C9-122 (Matt on T12_12d: "I'll need to see it without gear and during idle as well") -- runs inside a COPY of
# cliffside3d/godot (never cliffside3d itself): the painted barrow.tscn, the play camera following him, HUD off, the knight's
# own tree. GEAR stack 0 ('base': no pieces, so the unarmed clips idle / walk / run) is exactly what the player sees when GEAR
# strips everything.
#   --mode sheet : 8 facings (E NE N NW W SW S SE), row 1 IDLE (placed facing that way, 1.5 s settled), row 2 WALK (1.0 s
#                  into a walk that way); a 170x220 crop about him from the 1920x1080 play frame, enlarged 2x -> <out>/<tag>_sheet.png
#   --mode film  : base: idle 6 s, walk 2.5 s, run 1.5 s, stop 1 s; then the full kit: the same -> <out>/<tag>_film.mp4
#   Godot --path <copy> --resolution 640x360 --fixed-fps 60 --script <this> -- --mode sheet|film --out <dir> --tag <t> --label "..."
const SHOT := Vector2i(1920, 1080)
const TICK := 1.0 / 60.0
const START := Vector2(7.9, 5.1)
const FFMPEG := "/opt/homebrew/bin/ffmpeg"
const CROP := Rect2i(0, 0, 170, 220)
const FACINGS := ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]
var vp: SubViewport
var scene
var k
var lab: Label
var pipe: FileAccess = null
var pid := -1
var mf := 0

func _initialize() -> void:
	create_timer(1800.0).timeout.connect(func(): push_error("WATCHDOG"); quit(4))
	var a := OS.get_cmdline_user_args()
	var mode := "sheet"; var out_dir := "/tmp"; var tag := "bare"; var label := ""
	for i in a.size():
		match a[i]:
			"--mode": mode = a[i + 1]
			"--out": out_dir = a[i + 1]
			"--tag": tag = a[i + 1]
			"--label": label = a[i + 1]
	Engine.physics_ticks_per_second = 60
	vp = SubViewport.new(); vp.size = SHOT; vp.own_world_3d = true; vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/barrow.tscn").instantiate()
	vp.add_child(scene)
	for i in 80:
		await process_frame
		await physics_frame
	k = scene.knight
	k.set_physics_process(false)
	scene.set_hud_visible(false)
	k.set_gear_stack(0)
	scene.place_knight(START.x, START.y, "SE")
	scene.unpark_camera()
	lab = Label.new(); lab.position = Vector2(16, 12)
	lab.add_theme_font_size_override("font_size", 26); lab.add_theme_color_override("font_color", Color(1, 1, 1))
	var sb := StyleBoxFlat.new(); sb.bg_color = Color(0, 0, 0, 0.55)
	sb.content_margin_left = 8; sb.content_margin_right = 8; sb.content_margin_top = 4; sb.content_margin_bottom = 4
	lab.add_theme_stylebox_override("normal", sb)
	vp.add_child(lab)
	print("[bare] gear stack 0 = %s; pieces shown: %s" % [String((k.cfg.get("gear_stack_names", ["?"]) as Array)[0]), str((k.cfg.get("gear_stacks", [[]]) as Array)[0])])
	for i in 30: await _tick(Vector2.ZERO)
	if mode == "sheet":
		await _sheet("%s/%s_sheet.png" % [out_dir, tag], label)
	else:
		await _film("%s/%s_film.mp4" % [out_dir, tag], label)
	print("[bare] done")
	quit(0)

func _grab() -> Image:
	# a crop about HIM: his hips projected through the play camera (it trails him, so he is not at the frame centre), at the
	# play frame's own pixels, then enlarged 2x -- what the player sees, closer
	var im: Image = vp.get_texture().get_image(); im.convert(Image.FORMAT_RGB8)
	var sk: Skeleton3D = k._skel
	var hp: Vector3 = (sk.global_transform * sk.get_bone_global_pose(sk.find_bone("Hips"))).origin
	var sp: Vector2 = vp.get_camera_3d().unproject_position(hp)
	var r := Rect2i(int(sp.x) - CROP.size.x / 2, int(sp.y) - int(CROP.size.y * 0.55), CROP.size.x, CROP.size.y)
	r.position.x = clampi(r.position.x, 0, SHOT.x - r.size.x); r.position.y = clampi(r.position.y, 0, SHOT.y - r.size.y)
	var g := im.get_region(r)
	g.resize(CROP.size.x * 2, CROP.size.y * 2, Image.INTERPOLATE_LANCZOS)
	return g

func _sheet(path: String, label: String) -> void:
	lab.visible = false
	var TW := CROP.size.x * 2; var TH := CROP.size.y * 2
	var sheet := Image.create(TW * 8, TH * 2, false, Image.FORMAT_RGB8)
	for c in 8:
		var f: String = FACINGS[c]
		# IDLE: placed facing f, settled 1.5 s
		scene.place_knight(START.x, START.y, f)
		for i in 90: await _tick(Vector2.ZERO)
		sheet.blit_rect(_grab(), Rect2i(0, 0, TW, TH), Vector2i(c * TW, 0))
		# WALK: 1.0 s into a walk toward f
		scene.place_knight(START.x, START.y, f)
		for i in 20: await _tick(Vector2.ZERO)
		var d: Vector2 = k._canvas_dir_for(f)
		for i in 60: await _tick(d)
		sheet.blit_rect(_grab(), Rect2i(0, 0, TW, TH), Vector2i(c * TW, TH))
	sheet.save_png(path)
	print("[bare] sheet %s -> %s" % [label, path])

func _film(path: String, label: String) -> void:
	var r := OS.execute_with_pipe(FFMPEG, PackedStringArray(["-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % [SHOT.x, SHOT.y],
		"-r", "60", "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", "-movflags", "+faststart", path]), true)
	pipe = r.get("stdio"); pid = int(r.get("pid", -1))
	var d := Vector2(0, -1)
	for stack in [0, k.gear_stack_count() - 1]:
		k.set_gear_stack(stack)
		scene.place_knight(START.x, START.y, "SE")
		var nm: String = "NO GEAR (GEAR stack 0: the unarmed idle / walk / run)" if stack == 0 else "FULL KIT (axe + shield: idle_guard / walk / run + the arm layers)"
		for ph in [["idle", Vector2.ZERO, false, 6.0], ["walk", d, false, 2.5], ["run", d, true, 1.5], ["stop", Vector2.ZERO, false, 1.0]]:
			lab.text = "%s\n%s -- %s   PLAY SPEED" % [label, nm, String(ph[0])]
			for i in int(round(float(ph[3]) / TICK)): await _tick(ph[1], bool(ph[2]))
	pipe.close()
	var w0 := Time.get_ticks_msec()
	while OS.is_process_running(pid) and Time.get_ticks_msec() - w0 < 120000: OS.delay_msec(100)
	pipe = null
	print("[bare] film: %d frames -> %s" % [mf, path])

func _tick(dir: Vector2, run := false) -> void:
	k.drive_dir(dir, run, TICK)
	await physics_frame
	await process_frame
	if pipe != null:
		var im: Image = vp.get_texture().get_image(); im.convert(Image.FORMAT_RGB8)
		pipe.store_buffer(im.get_data()); mf += 1
