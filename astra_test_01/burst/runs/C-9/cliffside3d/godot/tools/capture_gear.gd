extends SceneTree
# C-9 D2 gate G3: the gear captures.
#
#   1  he walks the TREE path then the BRIDGE, cycling the five stacks as he goes -> mp4
#   2  the attack with the full kit, at the post                                   -> mp4
#   3  a close still of the STRIKE frame, so the blade's orientation can be SEEN --
#      nothing in the export marks the edge, so no instrument here can name it, and a
#      picture at 6x is the honest substitute for a number.
#
# Walked, not teleported, at his own 201.7 canvas px/s, with the physics tick set to the
# frame rate and move_and_slide's implicit delta compensated -- see knight.drive_dir.
#
#   Godot --path godot --resolution 1920x1080 --script tools/capture_gear.gd -- --out D

const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const FPS := 24.0
const DT := 1.0 / 24.0

const TREE_START := Vector2(1666.0, 2705.0)
const TREE_DIR := Vector2(1, 0)
const TREE_FRAMES := 50
const TREE_AIM := Vector2(1896.0, 2640.0)
const TREE_ZOOM := 1.5

const BRIDGE_START := Vector2(3118.09, 1471.77)
const BRIDGE_DIR := Vector2(0.42, -1.0)
const BRIDGE_FRAMES := 65
const BRIDGE_AIM := Vector2(3300.0, 1180.0)
const BRIDGE_ZOOM := 1.15

const POST_SPOT := Vector2(2996.0, 1337.0)
const POST_AIM := Vector2(2996.0, 1290.0)
const POST_ZOOM := 1.6
const STRIKE_FRAME := 16

var out_dir := ""
var scene
var vp: SubViewport
var cam: Camera3D
var report := {}
var _wf := 0
var _rf := 0
var _af := 0


func _initialize() -> void:
	out_dir = ProjectSettings.globalize_path("user://gearcap")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir + "/walkframes")
	DirAccess.make_dir_recursive_absolute(out_dir + "/attackframes")
	DirAccess.make_dir_recursive_absolute(out_dir + "/runframes")
	Engine.physics_ticks_per_second = int(FPS)
	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = false
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

	report["tree"] = await _leg(k, TREE_START, TREE_DIR, TREE_FRAMES, TREE_AIM, TREE_ZOOM,
							   "tree path, cycling the stacks through the fade")
	report["bridge"] = await _leg(k, BRIDGE_START, BRIDGE_DIR, BRIDGE_FRAMES, BRIDGE_AIM,
								  BRIDGE_ZOOM, "across the bridge, cycling the stacks")
	report["run"] = await _run_leg(k)
	report["attack"] = await _attack(k)

	var f := FileAccess.open(out_dir + "/gearcap.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("[gearcap] -> ", out_dir)
	quit(0)


func _place(k, px: Vector2) -> void:
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var g := CliffWorld.ground_at(space, px, scene.right, scene.up, scene.fwd)
	if not g.is_empty():
		k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.05
	k.velocity = Vector3.ZERO


func _leg(k, start: Vector2, dir: Vector2, frames: int, aim: Vector2, zoom: float,
		  label: String) -> Dictionary:
	print("[gearcap] %s" % label)
	k.set_physics_process(false)
	k.visible = true
	_place(k, start)
	scene.look_at_canvas(aim, 0.0, zoom)
	for i in 8:
		await physics_frame
		await process_frame
	var n_stacks: int = k.gear_stack_count()
	var per: int = maxi(1, frames / n_stacks)
	var changes := []
	var faded := 0
	var first := CliffWorld.canvas_of(k.global_position, scene.right, scene.up)
	for i in frames:
		var s: int = mini(i / per, n_stacks - 1)
		if k.gear_stack != s:
			k.set_gear_stack(s)
			changes.append({"frame": i, "stack": s, "pieces": k.cfg["gear_stacks"][s]})
		k.drive_dir(dir, false, DT)
		await physics_frame
		scene.settle_fade()
		if scene.fade_state.size() > 0:
			faded += 1
		await _frame("walkframes")
	var last := CliffWorld.canvas_of(k.global_position, scene.right, scene.up)
	k.set_physics_process(true)
	return {"label": label, "frames": frames,
			"measured_px_s": snappedf((last - first).length() / (float(frames) * DT), 0.1),
			"stack_changes": changes, "frames_with_a_faded_occluder": faded}


func _run_leg(k) -> Dictionary:
	"""The full kit at a run, across the bridge. The arm layer is on for a run, so this is
	also where a shield held in a carry pose has to survive the widest gait he has."""
	print("[gearcap] the full kit at a run, across the bridge")
	k.set_physics_process(false)
	k.visible = true
	k.set_gear_stack(k.gear_stack_count() - 1)
	_place(k, BRIDGE_START)
	scene.look_at_canvas(BRIDGE_AIM, 0.0, BRIDGE_ZOOM)
	for i in 8:
		await physics_frame
		await process_frame
	var first := CliffWorld.canvas_of(k.global_position, scene.right, scene.up)
	# 26 FRAMES, NOT 40. At 647.5 canvas px/s a second and two thirds carries him 1080 px
	# and the bridge is about 560 long: he ran off the far end and stopped against the
	# cliff, which averaged 453.8 px/s and read as a speed defect rather than a path that
	# ran out. One second of run is the crossing.
	var frames := 26
	for i in frames:
		k.drive_dir(BRIDGE_DIR, true, DT)          # running
		await physics_frame
		scene.settle_fade()
		await _frame("runframes")
	var last := CliffWorld.canvas_of(k.global_position, scene.right, scene.up)
	k.set_physics_process(true)
	return {"frames": frames, "stack": k.gear_stack,
			"measured_px_s": snappedf((last - first).length() / (float(frames) * DT), 0.1),
			"declared_run_px_s": k.cfg.get("run_px_s", 0)}


func _attack(k) -> Dictionary:
	print("[gearcap] the attack with the full kit, at the post")
	k.set_physics_process(false)
	k.visible = true
	k.set_gear_stack(k.gear_stack_count() - 1)        # everything on
	_place(k, POST_SPOT)
	k.facing = "S"
	scene.look_at_canvas(POST_AIM, 0.0, POST_ZOOM)
	for i in 10:
		await physics_frame
		await process_frame
	for i in 24:
		k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
		await _frame("attackframes")
	k.state = "attack"
	k.play("attack")
	var n := int(round(float(k._clip_len.get("attack", 1.5)) * FPS))
	for i in n:
		k.drive_dir(Vector2.ZERO, false, DT, "attack")
		await physics_frame
		await _frame("attackframes")
	for i in 16:
		k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
		await _frame("attackframes")
	# and the strike, held and close, so the blade can be read by eye
	var anim: AnimationPlayer = k._anim
	anim.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	anim.play("attack")
	var a := anim.get_animation("attack")
	for fr in [STRIKE_FRAME - 3, STRIKE_FRAME, STRIKE_FRAME + 3]:
		anim.seek(a.length * float(fr) / float(n), true, true)
		scene.look_at_canvas(POST_AIM + Vector2(0, -40), 0.0, 6.0)
		_mirror()
		for i in 4:
			await process_frame
		vp.get_texture().get_image().save_png("%s/strike_f%02d.png" % [out_dir, fr])
	anim.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS
	k.set_physics_process(true)
	return {"idle_frames": 24, "attack_frames": n, "tail_frames": 16,
			"strike_stills": [STRIKE_FRAME - 3, STRIKE_FRAME, STRIKE_FRAME + 3],
			"canvas_px": [POST_SPOT.x, POST_SPOT.y]}


func _mirror() -> void:
	cam.global_transform = scene.cam.global_transform
	cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))


func _frame(folder: String) -> void:
	_mirror()
	await process_frame
	await process_frame
	var n: int = _wf if folder == "walkframes" else (_rf if folder == "runframes" else _af)
	vp.get_texture().get_image().save_jpg("%s/%s/f_%04d.jpg" % [out_dir, folder, n], 0.92)
	if folder == "walkframes":
		_wf += 1
	elif folder == "runframes":
		_rf += 1
	else:
		_af += 1
