extends SceneTree
# C-9 R-C9-69 / gate G2: the barbarian in the projected cliffside.
#
#   1  he walks the TREE path, through the occluder fade      -> mp4frames
#   2  he walks across the BRIDGE                             -> mp4frames
#   3  five seconds of idle, then the attack, near the post   -> idleframes
#   4  the bridge side-by-side still, with him on the bridge
#
# HE IS WALKED, NOT TELEPORTED. Every earlier sweep in this run set global_position frame
# by frame, which is the one thing that cannot show whether the feet slide -- and the whole
# reason his speed was taken from the clips' own stride is that they must not. So the
# capture drives him through the same drive_dir() the player's input drives, over the real
# collision, at 201.7 / 647.5 canvas px/s, and what the frames show is what a player sees.
#
#   Godot --path godot --resolution 1920x1080 --script tools/capture_barbarian.gd -- --out D

const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const FPS := 24.0
const DT := 1.0 / 24.0

const TREE_START := Vector2(1666.0, 2705.0)     # the measured fade path, west of the trunk
const TREE_DIR := Vector2(1, 0)                 # "E", straight across the trunk
const TREE_FRAMES := 50
const TREE_AIM := Vector2(1896.0, 2640.0)
const TREE_ZOOM := 1.5

const BRIDGE_START := Vector2(3118.09, 1471.77)
const BRIDGE_DIR := Vector2(0.42, -1.0)         # up-screen and a little east, along the deck
const BRIDGE_FRAMES := 64
const BRIDGE_AIM := Vector2(3300.0, 1180.0)
const BRIDGE_ZOOM := 1.15

const POST_SPOT := Vector2(2996.0, 1337.0)      # where he stands in front of bridge_post_1
const POST_AIM := Vector2(2996.0, 1290.0)
const POST_ZOOM := 1.5

const SIDE_SPOT := Vector2(3459.88, 1027.18)    # the bridge, for the 2D comparison
const ON_BRIDGE := Vector2(3380.0, 1120.0)

var out_dir := ""
var scene
var vp: SubViewport
var cam: Camera3D
var report := {}
var _mf := 0
var _if := 0


func _initialize() -> void:
	out_dir = ProjectSettings.globalize_path("user://barb")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir + "/mp4frames")
	DirAccess.make_dir_recursive_absolute(out_dir + "/idleframes")
	# THE PHYSICS TICK MUST MATCH THE FRAME RATE, or the walk is a slide by arithmetic.
	# drive_dir sets a velocity and move_and_slide integrates it over the ENGINE's physics
	# delta, not over the dt passed in. Stepping one physics frame per captured frame at the
	# default 60 Hz therefore advances him 1/60 s of ground for 1/24 s of animation -- he
	# came out at 79.6 px/s against a declared 201.7, which is 24/60 of it exactly, and the
	# feet would have slid by the same factor. At 24 Hz one tick is one frame is 1/24 s.
	Engine.physics_ticks_per_second = int(FPS)
	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = false
	vp.transparent_bg = false
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 50:
		await process_frame
	cam = Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.near = scene.cam.near
	cam.far = scene.cam.far
	cam.cull_mask = scene.cam.cull_mask
	vp.add_child(cam)
	cam.current = true
	var k = scene.knight
	report["character"] = {"model": String(k.cfg.get("model", "?")).get_file(),
						   "figure_scale": k._figure_scale,
						   "walk_px_s": k.cfg.get("walk_px_s", 0),
						   "run_px_s": k.cfg.get("run_px_s", 0)}

	report["tree"] = await _walk_leg(k, TREE_START, TREE_DIR, TREE_FRAMES, TREE_AIM, TREE_ZOOM,
									 "mp4frames", "tree path, through the fade")
	report["bridge"] = await _walk_leg(k, BRIDGE_START, BRIDGE_DIR, BRIDGE_FRAMES,
									   BRIDGE_AIM, BRIDGE_ZOOM, "mp4frames", "across the bridge")
	report["idle_attack"] = await _idle_attack(k)
	report["side_by_side"] = await _side(k)

	var f := FileAccess.open(out_dir + "/barbarian.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("[barb] -> ", out_dir)
	quit(0)


func _place(k, px: Vector2) -> void:
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var g := CliffWorld.ground_at(space, px, scene.right, scene.up, scene.fwd)
	if not g.is_empty():
		k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.05
	k.velocity = Vector3.ZERO


func _walk_leg(k, start: Vector2, dir: Vector2, frames: int, aim: Vector2, zoom: float,
			   folder: String, label: String) -> Dictionary:
	print("[barb] %s" % label)
	k.set_physics_process(false)          # the capture drives him, at its own fixed dt
	k.visible = true
	_place(k, start)
	scene.look_at_canvas(aim, 0.0, zoom)
	for i in 8:
		await physics_frame
		await process_frame
	var first := CliffWorld.canvas_of(k.global_position, scene.right, scene.up)
	var faded_frames := 0
	var steps := []
	print("    physics tick %d Hz, body delta %.6f s" %
		[Engine.physics_ticks_per_second, k.get_physics_process_delta_time()])
	for i in frames:
		var was := CliffWorld.canvas_of(k.global_position, scene.right, scene.up)
		k.drive_dir(dir, false, DT)
		steps.append((CliffWorld.canvas_of(k.global_position, scene.right, scene.up) - was).length())
		await physics_frame
		scene.settle_fade()
		if scene.fade_state.size() > 0:
			faded_frames += 1
		await _frame(folder)
	var last := CliffWorld.canvas_of(k.global_position, scene.right, scene.up)
	k.set_physics_process(true)
	var travelled := (last - first).length()
	var path := 0.0
	for s in steps:
		path += float(s)
	steps.sort()
	print("    per-frame step: median %.2f px, path %.1f px, straight line %.1f px" %
		[steps[steps.size() / 2], path, travelled])
	var seconds := float(frames) * DT
	return {"label": label, "frames": frames, "seconds": snappedf(seconds, 0.01),
			"from_canvas_px": [snappedf(first.x, 0.1), snappedf(first.y, 0.1)],
			"to_canvas_px": [snappedf(last.x, 0.1), snappedf(last.y, 0.1)],
			"travelled_canvas_px": snappedf(travelled, 0.1),
			"path_length_canvas_px": snappedf(path, 0.1),
			"median_step_px": snappedf(steps[steps.size() / 2], 0.01),
			"measured_px_s": snappedf(path / maxf(seconds, 1e-6), 0.1),
			"straight_line_px_s": snappedf(travelled / maxf(seconds, 1e-6), 0.1),
			"declared_walk_px_s": k.cfg.get("walk_px_s", 0),
			"frames_with_a_faded_occluder": faded_frames}


func _idle_attack(k) -> Dictionary:
	print("[barb] five seconds of idle, then the attack, near the post")
	k.set_physics_process(false)
	k.visible = true
	_place(k, POST_SPOT)
	k.facing = "N"
	scene.look_at_canvas(POST_AIM, 0.0, POST_ZOOM)
	for i in 8:
		await physics_frame
		await process_frame
	for i in 120:                                   # five seconds at 24 fps
		k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
		await _frame("idleframes")
	k.state = "attack"
	k.play("attack")
	var n := int(round(k._clip_len.get(String(k._roles.get("attack", "attack")), 1.5) * FPS))
	for i in n:
		k.drive_dir(Vector2.ZERO, false, DT, "attack")
		await physics_frame
		await _frame("idleframes")
	for i in 24:
		k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
		await _frame("idleframes")
	k.set_physics_process(true)
	return {"idle_frames": 120, "attack_frames": n, "tail_frames": 24,
			"attack_clip": String(k._roles.get("attack", "?")),
			"canvas_px": [POST_SPOT.x, POST_SPOT.y]}


func _side(k) -> Dictionary:
	print("[barb] the bridge still, with him on the deck")
	k.set_physics_process(false)
	k.visible = true
	_place(k, ON_BRIDGE)
	k.facing = "NE"
	k.state = "idle"
	k._drive()
	scene.look_at_canvas(SIDE_SPOT)
	for i in 10:
		await physics_frame
		await process_frame
	scene.settle_fade()
	_mirror()
	for i in 4:
		await process_frame
	vp.get_texture().get_image().save_png("%s/bridge_3d_barbarian.png" % out_dir)
	k.visible = false
	for i in 4:
		await process_frame
	vp.get_texture().get_image().save_png("%s/bridge_3d_empty.png" % out_dir)
	k.visible = true
	k.set_physics_process(true)
	return {"spot_canvas_px": [SIDE_SPOT.x, SIDE_SPOT.y],
			"he_stands_at_canvas_px": [ON_BRIDGE.x, ON_BRIDGE.y]}


func _mirror() -> void:
	cam.global_transform = scene.cam.global_transform
	cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))


func _frame(folder: String) -> void:
	_mirror()
	await process_frame
	await process_frame
	var n := _mf if folder == "mp4frames" else _if
	vp.get_texture().get_image().save_jpg("%s/%s/f_%04d.jpg" % [out_dir, folder, n], 0.92)
	if folder == "mp4frames":
		_mf += 1
	else:
		_if += 1
