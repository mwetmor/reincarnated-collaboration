extends SceneTree
# C-9 T9: the same bridge frame as T9-0 and T9-1c, in FOUR states, in ONE run.
#
#   painted          the plate carrying its own light -- the reference every drop is measured against
#   lit_base         lit world, original plate, card props      (must reproduce T9-0)
#   lit_albedo       lit world, ALBEDO plate, card props        (what 1b bought)
#   lit_props        lit world, original plate, 3D props        (what 1a bought)
#   lit_albedo_props lit world, ALBEDO plate, 3D props          (the delivered state)
#
# ONE run and not four, because four runs differ in more than the thing under test: the
# camera settles, the idle animation lands somewhere, the shader cache is cold. Attribution
# is a subtraction, and a subtraction between two runs measures the runs as well.
#
# The frames are SAVED and the numbers computed in tools/t9_metrics.py. Luma thresholds are
# a definition, not a measurement, and a definition belongs in one readable place rather
# than inside a capture loop where it silently becomes the number everyone quotes.
#
# HIM, measured in PIXELS. T9-0 reports 123.3 canvas px at scale 1.0; probe_t9_scale.gd and
# probe_t9_figure.gd both get 103.8 from the one and only Skeleton3D's head_end bone. Rather
# than arbitrate between two bone readings, this saves the final frame WITH and WITHOUT him
# and lets the silhouette say how tall he is. (The AABB route is not available: get_aabb()
# on a skinned mesh returns rest-pose bounds in mesh space -- it reported him 0.02 m tall,
# cleanly.)
#
#   Godot --path godot --resolution 1920x1080 --script tools/shot_t9b.gd -- --out DIR [--mp4frames DIR]

const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const PITCH_COS := 0.602462407085
const FPS := 24.0
const DT := 1.0 / 24.0
const AIM := Vector2(3459.88, 1027.18)
const STAND := Vector2(3380.0, 1120.0)

var out_dir := ""
var mp4_dir := ""
var scene
var vp: SubViewport
var cam: Camera3D
var report := {}
var _mf := 0


func _initialize() -> void:
	out_dir = ProjectSettings.globalize_path("user://t9b")
	mp4_dir = ""
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
		if args[i] == "--mp4frames" and i + 1 < args.size():
			mp4_dir = args[i + 1]
	if mp4_dir == "":
		mp4_dir = out_dir + "/mp4frames"
	DirAccess.make_dir_recursive_absolute(out_dir)
	DirAccess.make_dir_recursive_absolute(mp4_dir)
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

	report["albedo_plate"] = scene.albedo_plate_in_use()
	report["props3d"] = scene.props3d_report()
	report["px_per_vertical_m"] = snappedf(PPM * PITCH_COS, 0.001)

	var k = scene.knight
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var g := CliffWorld.ground_at(space, STAND, scene.right, scene.up, scene.fwd)
	k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.02
	k.facing = "NE"
	k.state = "idle"
	k._drive()

	# ---- the five frames, one camera, one pose ------------------------------
	scene.set_lit(false)
	k.set_figure_scale(1.0)          # TRUE scale in the painted panel too: only light moves
	scene.look_at_canvas(AIM, 0.0, 1.0)
	await _settle()
	await _shot("t9b_bridge_painted")

	for state in [["lit_base", false, false], ["lit_albedo", true, false],
				  ["lit_props", false, true], ["lit_albedo_props", true, true]]:
		scene.set_lit(true)
		k.set_figure_scale(1.0)
		scene.use_albedo_plate(bool(state[1]))
		scene.use_props3d(bool(state[2]))
		await _settle()
		await _shot("t9b_bridge_%s" % String(state[0]))
		print("[t9b] %s captured" % String(state[0]))

	# ---- him, in pixels, in the delivered state -----------------------------
	k.visible = false
	await _settle()
	await _shot("t9b_bridge_final_noknight")
	k.visible = true

	# ---- the pair Matt sees, him on the bridge ------------------------------
	scene.set_lit(false)
	k.set_figure_scale(1.0)
	await _settle()
	await _shot("t9b_pair_painted")
	scene.set_lit(true)
	k.set_figure_scale(1.0)
	scene.use_albedo_plate(true)
	scene.use_props3d(true)
	await _settle()
	await _shot("t9b_pair_lit")

	# ---- one lit walk across the bridge -------------------------------------
	# The camera is parked, as T9-0 parked it: a frame that moves and a world that
	# changes cannot be told apart afterwards.
	var g2 := CliffWorld.ground_at(space, Vector2(3118.09, 1471.77), scene.right, scene.up, scene.fwd)
	k.global_position = (g2["position"] as Vector3) + Vector3.UP * 0.05
	k.velocity = Vector3.ZERO
	scene.look_at_canvas(Vector2(3300.0, 1180.0), 0.0, 1.15)
	await _settle()
	for i in 90:
		k.drive_dir(Vector2(0.42, -1.0), false, DT)
		await physics_frame
		scene.settle_fade()
		await _frame()
	report["mp4_frames"] = _mf

	scene.set_lit(false)                      # the app ships in painted mode
	var f := FileAccess.open(out_dir + "/t9b.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("[t9b] -> %s  (%d movie frames)" % [out_dir, _mf])
	quit(0)


func _settle() -> void:
	for i in 10:
		await physics_frame
		await process_frame


func _mirror() -> void:
	cam.global_transform = scene.cam.global_transform
	cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))


func _shot(nm: String) -> void:
	_mirror()
	for i in 4:
		await process_frame
	vp.get_texture().get_image().save_png("%s/%s.png" % [out_dir, nm])


func _frame() -> void:
	_mirror()
	await process_frame
	await process_frame
	vp.get_texture().get_image().save_jpg("%s/f_%04d.jpg" % [mp4_dir, _mf], 0.92)
	_mf += 1
