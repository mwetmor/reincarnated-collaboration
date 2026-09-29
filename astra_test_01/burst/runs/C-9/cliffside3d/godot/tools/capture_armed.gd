extends SceneTree
# walk armed -> stop in guard -> block (hold) -> release -> slash -> chop -> bash -> run
const DT := 1.0 / 24.0
const SPOT := Vector2(2285.62, 2407.32)
var out_dir := ""
var _mf := 0
var _vp: Viewport
var _k
var _scene
func _initialize():
	out_dir = ProjectSettings.globalize_path("user://armed")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir + "/mp4frames")
	_scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(_scene)
	for i in 60: await process_frame
	Engine.physics_ticks_per_second = 24
	_vp = root
	_k = _scene.knight
	_k.set_physics_process(false)
	_k.set_gear_stack(_k.gear_stack_count() - 1)
	var space: PhysicsDirectSpaceState3D = _scene.get_world_3d().direct_space_state
	var g := CliffWorld.ground_at(space, SPOT, _scene.right, _scene.up, _scene.fwd)
	_k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.05
	_k.velocity = Vector3.ZERO
	_k.facing = "S"
	print("[cap] armed=%s  walk %.1f  run %.1f  strafe %.1f px/s" %
		[_k.armed(), _k.walk_px_s(), _k.run_px_s(), _k.strafe_px_s()])
	await _hold(Vector2.ZERO, false, 8)           # stand
	await _hold(Vector2(1, 0), false, 26)         # armed walk
	await _hold(Vector2(1, 0), true, 34)          # armed run
	await _hold(Vector2.ZERO, false, 14)          # stop, into the guard
	_k.set_block(true)
	await _hold(Vector2.ZERO, false, 14)          # block, held
	await _hold(Vector2(-1, 0), false, 22)        # strafe one way
	await _hold(Vector2(1, 0), false, 22)         # strafe the other
	_k.set_block(false)
	await _hold(Vector2.ZERO, false, 10)          # release
	_k.try_strike("slash")
	await _until_done(46)
	_k.try_strike("chop")
	await _until_done(64)
	await _hold(Vector2.ZERO, false, 10)
	print("[cap] -> %s  (%d frames)" % [out_dir, _mf])
	quit(0)

func _hold(dir: Vector2, run: bool, n: int) -> void:
	for i in n:
		_k.drive_dir(dir, run, DT)
		await physics_frame
		await _shot()

func _until_done(cap: int) -> void:
	var i := 0
	while i < cap:
		_k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
		await _shot()
		i += 1
		if i > 6 and not _k.attacking():
			break

func _shot() -> void:
	await RenderingServer.frame_post_draw
	_vp.get_texture().get_image().save_jpg("%s/mp4frames/f_%04d.jpg" % [out_dir, _mf], 0.92)
	_mf += 1
