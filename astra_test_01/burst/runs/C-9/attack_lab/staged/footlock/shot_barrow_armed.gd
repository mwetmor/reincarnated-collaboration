extends SceneTree
# C-9: the Barrow, walked ARMED at the play camera -- slash, chop and block from idle, then
# from a run -- to check the foot-lock install in the real scene.
#
#   Godot --path godot --fixed-fps 24 --resolution 640x360 --script tools/shot_barrow_armed.gd \
#         -- --out DIR
#
# --fixed-fps 24 IS NOT OPTIONAL. The foot lock times its hold and release on the frame delta
# (the skeleton's modifiers run in the game's IDLE mode, as shipped), and a 1080p capture renders
# slower than real time: with a free-running clock the 0.3 s lock would pass in a frame or two
# and the film would not show what a player sees. Fixed fps makes every frame exactly 1/24 s of
# game time for the tree AND the modifiers.
#
# The controller is driven from here (drive_dir), as shot_barrow.gd does; the tree and the
# modifiers are left in the modes the game runs them in -- that is what is being checked.
const SHOT := Vector2i(1920, 1080)
const DT := 1.0 / 24.0
const START := Vector2(7.9, 5.1)          # shot_barrow.gd's WALK_FROM
var vp: SubViewport
var scene
var k
var out_dir := ""
var _mf := 0
var log_lines := []

func _initialize() -> void:
	create_timer(900.0).timeout.connect(func(): push_error("WATCHDOG: quitting a hung capture"); quit(4))
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir + "/frames")
	Engine.physics_ticks_per_second = 24
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
	scene.place_knight(START.x, START.y, "N")
	scene.unpark_camera()                   # the play zoom, following him
	var fl = k.get("_foot_lock")
	_say("armed=%s foot_lock=%s modifier mode=%d (1 = IDLE, as shipped)" % [str(k.armed()), str(fl != null),
		(k._skel as Skeleton3D).modifier_callback_mode_process])
	await _hold(Vector2.ZERO, false, 24)
	# ---- from IDLE ------------------------------------------------------------------
	for which in ["slash", "chop"]:
		k.try_strike(which)
		_say("%s from idle at frame %d" % [which, _mf])
		await _until_done(12)
		await _hold(Vector2.ZERO, false, 12)
	k.set_block(true); _say("block from idle at frame %d" % _mf)
	await _hold(Vector2.ZERO, false, 24)
	k.set_block(false)
	await _hold(Vector2.ZERO, false, 18)
	# ---- from a RUN (alternating direction so he stays on the floor) ---------------
	var dirs := [Vector2(0, -1), Vector2(0, 1), Vector2(0, -1)]
	var i := 0
	for which in ["slash", "chop", "block"]:
		await _hold(dirs[i], true, 24)
		if which == "block":
			k.set_block(true)
		else:
			k.try_strike(which)
		_say("%s from a run at frame %d" % [which, _mf])
		if which == "block":
			await _hold(Vector2.ZERO, false, 24)
			k.set_block(false)
			await _hold(Vector2.ZERO, false, 18)
		else:
			await _until_done(12)
		i += 1
	await _hold(Vector2.ZERO, false, 12)
	if fl != null:
		_say("foot-lock decisions (last %d): %s" % [(fl.events as Array).size(), str(fl.events)])
		_say("reach releases %d, landings %d" % [int(fl.reach_releases), int(fl.landings)])
	_say("frames %d" % _mf)
	var f := FileAccess.open(out_dir + "/barrow_armed_log.txt", FileAccess.WRITE)
	f.store_string("\n".join(log_lines))
	f.close()
	quit(0)

func _say(s: String) -> void:
	print("[armed] " + s)
	log_lines.append(s)

func _step(dir: Vector2, run: bool) -> void:
	k.drive_dir(dir, run, DT)
	await physics_frame
	await process_frame
	vp.get_texture().get_image().save_jpg("%s/frames/f_%04d.jpg" % [out_dir, _mf], 0.92)
	_mf += 1

func _hold(dir: Vector2, run: bool, n: int) -> void:
	for j in n:
		await _step(dir, run)

func _until_done(tail: int) -> void:
	var g := 0
	while (k.attacking() or g < 6) and g < 400:
		await _step(Vector2.ZERO, false)
		g += 1
	await _hold(Vector2.ZERO, false, tail)
