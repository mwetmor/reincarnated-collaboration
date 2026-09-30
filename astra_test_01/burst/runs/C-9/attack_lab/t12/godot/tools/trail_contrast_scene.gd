extends SceneTree
# T12_11b THE TRAIL'S CONTRAST ON THE BARROW'S OWN GROUND -- runs inside a COPY of cliffside3d/godot (never cliffside3d).
# The real barrow.tscn, the play camera following him, HUD off, 60 Hz, --fixed-fps 60. Two takes are compared frame for
# frame: --trail on and --trail off (the trail never stepped). Everything else repeats exactly under the fixed clock; the
# particle systems (the snowfall, the gusts, the puffs -- random per run) are hidden in BOTH takes so nothing else moves.
# Saved, lossless PNG crops (640 x 480 about him):
#   plate.png                    once, him hidden for one frame: the ground's own colour, for classing snow / rock / scrub
#   <strike>_<t>.png             at the first tick whose clip position reaches each listed t
#   Godot --path <copy> --resolution 640x360 --fixed-fps 60 --script <this> -- --out <dir> --trail on|off
#         [--at x,z] [--facing SE]
const SHOT := Vector2i(1920, 1080)
const CROP := Rect2i(640, 320, 640, 480)
const TICK := 1.0 / 60.0
const SHOTS := {"slash": [0.62, 0.68, 0.72, 0.78], "chop": [0.48, 0.54, 0.59, 0.65], "bash": [1.10, 1.16, 1.21, 1.27]}
var vp: SubViewport
var scene
var k
var out_dir := ""
var trail_on := true
var at := Vector2(7.9, 5.1)
var facing := "SE"

func _initialize() -> void:
	create_timer(1200.0).timeout.connect(func(): push_error("WATCHDOG"); quit(4))
	var a := OS.get_cmdline_user_args()
	for i in a.size():
		match a[i]:
			"--out": out_dir = a[i + 1]
			"--trail": trail_on = a[i + 1] == "on"
			"--at": at = Vector2(float(a[i + 1].split(",")[0]), float(a[i + 1].split(",")[1]))
			"--facing": facing = a[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir)
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
	if not trail_on and k.get("trail_auto") != null:
		k.trail_auto = false
	scene.set_hud_visible(false)
	scene.place_knight(at.x, at.y, facing)
	scene.unpark_camera()
	var np := 0
	for n in scene.find_children("*", "GPUParticles3D", true, false):
		(n as Node3D).visible = false; np += 1
	for n in scene.find_children("*", "CPUParticles3D", true, false):
		(n as Node3D).visible = false; np += 1
	print("[contrast] trail %s, at %s %s, %d particle systems hidden" % ["on" if trail_on else "off", str(at), facing, np])
	for i in 30: await _tick()
	k.visible = false
	await _tick()
	await _tick()
	_grab("plate")
	k.visible = true
	for i in 30: await _tick()
	for s in ["slash", "chop", "bash"]:
		for i in 30: await _tick()
		k.try_strike(s)
		var want: Array = (SHOTS[s] as Array).duplicate()
		var g := 0
		while (k.attacking() or g < 6) and g < 900:
			await _tick()
			g += 1
			var pos := _pos(s)
			while not want.is_empty() and pos >= float(want[0]) - 1e-4:
				_grab("%s_%.2f" % [s, float(want[0])])
				want.pop_front()
		for i in 30: await _tick()
	print("[contrast] done")
	quit(0)

func _pos(s: String) -> float:
	var tr: AnimationTree = k._tree
	if not bool(tr.get("parameters/os_%s/active" % s)):
		return -1.0
	return float(tr.get("parameters/a_%s/current_position" % s))

func _tick() -> void:
	k.drive_dir(Vector2.ZERO, false, TICK)
	await physics_frame
	await process_frame
	await RenderingServer.frame_post_draw

func _grab(name: String) -> void:
	var im: Image = vp.get_texture().get_image()
	im.convert(Image.FORMAT_RGB8)
	im.get_region(CROP).save_png("%s/%s.png" % [out_dir, name])
