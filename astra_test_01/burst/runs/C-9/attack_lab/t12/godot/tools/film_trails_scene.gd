extends SceneTree
# T12_11 STRIKE TRAILS IN THE PAINTED BARROW -- runs inside a COPY of cliffside3d/godot (never cliffside3d itself):
# the real barrow.tscn, the play camera following him, HUD off, the knight's tree, foot lock and trail in the modes the
# game runs them in (physics 60 Hz, the trail stepping itself). Slash, chop and bash from idle, one film per strike,
# frames straight to ffmpeg (OS.execute_with_pipe), 60 fps.
#   PLAY SPEED:    --fixed-fps 60,  --hold 1: every game tick is one frame
#   QUARTER SPEED: --fixed-fps 240, --hold 4: every 60 Hz game tick is held four frames -- the game's own frames,
#                  slowed; nothing between ticks is invented (the snowfall and the camera run per frame)
#   Godot --path <copy> --resolution 640x360 --fixed-fps 60 --script <this> -- --out <dir> --tag <name> --hold 1
#         [--strikes slash,chop,bash] [--facing SE] [--label "..."]
# after cliffside3d/godot/tools/shot_barrow_armed.gd (its stepping and its knight placement).
const SHOT := Vector2i(1920, 1080)
const TICK := 1.0 / 60.0
const START := Vector2(7.9, 5.1)          # shot_barrow.gd's WALK_FROM
const FFMPEG := "/opt/homebrew/bin/ffmpeg"
var vp: SubViewport
var scene
var k
var out_dir := ""
var tag := "take"
var hold := 1
var facing := "SE"
var label := ""
var strikes: PackedStringArray = ["slash", "chop", "bash"]
var pipe: FileAccess = null
var pid := -1
var mf := 0
var lab: Label

func _initialize() -> void:
	create_timer(2400.0).timeout.connect(func(): push_error("WATCHDOG"); quit(4))
	var a := OS.get_cmdline_user_args()
	for i in a.size():
		match a[i]:
			"--out": out_dir = a[i + 1]
			"--tag": tag = a[i + 1]
			"--hold": hold = int(a[i + 1])
			"--strikes": strikes = a[i + 1].split(",")
			"--facing": facing = a[i + 1]
			"--label": label = a[i + 1]
	Engine.physics_ticks_per_second = 60
	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/barrow.tscn").instantiate()
	vp.add_child(scene)
	for i in 80:
		await process_frame
		await physics_frame
	k = scene.knight
	k.set_gear_stack(k.gear_stack_count() - 1)
	k.set_physics_process(false)
	scene.set_hud_visible(false)
	scene.place_knight(START.x, START.y, facing)
	scene.unpark_camera()
	lab = Label.new(); lab.position = Vector2(16, 12)
	lab.add_theme_font_size_override("font_size", 26); lab.add_theme_color_override("font_color", Color(1, 1, 1))
	var sb := StyleBoxFlat.new(); sb.bg_color = Color(0, 0, 0, 0.55)
	sb.content_margin_left = 8; sb.content_margin_right = 8; sb.content_margin_top = 4; sb.content_margin_bottom = 4
	lab.add_theme_stylebox_override("normal", sb)
	vp.add_child(lab)
	print("[scene] knight %s, trail %s, facing %s, hold %d" % [String(k.get_script().resource_path), str(k.get("_trail") != null), facing, hold])
	for i in 30: await _tick(Vector2.ZERO)
	for s in strikes:
		await _film(String(s))
	print("[scene] done")
	quit(0)

func _film(s: String) -> void:
	var mp4 := "%s/%s_%s.mp4" % [out_dir, tag, s]
	var r := OS.execute_with_pipe(FFMPEG, PackedStringArray(["-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % [SHOT.x, SHOT.y],
		"-r", "60", "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", "-movflags", "+faststart", mp4]), true)
	pipe = r.get("stdio"); pid = int(r.get("pid", -1))
	mf = 0
	lab.text = "%s\n%s   %s" % [label, s.to_upper(), "PLAY SPEED" if hold == 1 else "QUARTER SPEED (each 60 Hz game tick held %d frames)" % hold]
	for i in 30: await _tick(Vector2.ZERO)
	k.try_strike(s)
	var g := 0
	while (k.attacking() or g < 6) and g < 900:
		await _tick(Vector2.ZERO)
		g += 1
	for i in 30: await _tick(Vector2.ZERO)
	pipe.close()
	var w0 := Time.get_ticks_msec()
	while OS.is_process_running(pid) and Time.get_ticks_msec() - w0 < 120000:
		OS.delay_msec(100)
	pipe = null
	print("[scene] %s: %d frames -> %s" % [s, mf, mp4])

func _tick(dir: Vector2) -> void:
	k.drive_dir(dir, false, TICK)
	await physics_frame
	for j in hold:
		await process_frame
		if pipe != null:
			var im: Image = vp.get_texture().get_image()
			im.convert(Image.FORMAT_RGB8)
			pipe.store_buffer(im.get_data())
			mf += 1
