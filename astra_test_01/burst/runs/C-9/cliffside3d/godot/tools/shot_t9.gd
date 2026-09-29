extends SceneTree
# C-9 T9-0: the world lit the way the character is lit, against the world that carries its
# light in the paint -- at the two named spots, with the man at TRUE SCALE in both panels
# so the only thing that differs between them is the lighting.
#
# Also the numbers R-C9-71 asks for: what he measures on screen at 1.0 against 1.25178, and
# how the bridge and the posts stand next to him.
#
#   Godot --path godot --resolution 1920x1080 --script tools/shot_t9.gd -- --out D

const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const FPS := 24.0
const DT := 1.0 / 24.0
const SPOTS := {
	"bridge": {"aim": Vector2(3459.88, 1027.18), "stand": Vector2(3380.0, 1120.0), "zoom": 1.0},
	"tree": {"aim": Vector2(1896.0, 2640.0), "stand": Vector2(1836.0, 2705.0), "zoom": 1.5},
}

var out_dir := ""
var scene
var vp: SubViewport
var cam: Camera3D
var report := {}
var _mf := 0


func _initialize() -> void:
	out_dir = ProjectSettings.globalize_path("user://t9")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir + "/mp4frames")
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
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)        # the full kit, as Matt played him

	# ---- the scale numbers -------------------------------------------------
	var skel: Skeleton3D = null
	for n in k.find_children("*", "Skeleton3D", true, false):
		skel = n
	var he := skel.find_bone("head_end")
	var heights := {}
	for s in [1.25177951388889, 1.0]:
		k.set_figure_scale(s)
		for i in 6:
			await physics_frame
			await process_frame
		var top: Vector3 = skel.global_transform * skel.get_bone_global_pose(he).origin
		var c_top := CliffWorld.canvas_of(top, scene.right, scene.up)
		var c_foot := CliffWorld.canvas_of(Vector3(top.x, k.global_position.y, top.z),
										   scene.right, scene.up)
		heights["scale_%.5f" % s] = {"world_height_m": snappedf(1.85 * s, 0.001),
									 "canvas_px": snappedf(absf(c_top.y - c_foot.y), 0.1)}
	report["figure"] = heights
	print("[t9] figure: %s" % JSON.stringify(heights))

	# ---- the pairs, both panels at TRUE scale ------------------------------
	k.set_figure_scale(1.0)
	for name in SPOTS:
		var spec: Dictionary = SPOTS[name]
		var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
		var g := CliffWorld.ground_at(space, spec["stand"], scene.right, scene.up, scene.fwd)
		k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.02
		k.facing = "NE" if name == "bridge" else "E"
		k.state = "idle"
		k._drive()
		for mode in [false, true]:
			scene.set_lit(mode)
			k.set_figure_scale(1.0)          # true scale in BOTH panels: only the light moves
			scene.look_at_canvas(spec["aim"], 0.0, float(spec["zoom"]))
			for i in 10:
				await physics_frame
				await process_frame
			await _shot("t9_%s_%s" % [name, "lit" if mode else "painted"])
		print("[t9] %s pair done" % name)

	# ---- a short walk in lit mode ------------------------------------------
	scene.set_lit(true)
	k.set_figure_scale(1.0)
	var space2: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var g2 := CliffWorld.ground_at(space2, Vector2(1666.0, 2705.0), scene.right, scene.up, scene.fwd)
	k.global_position = (g2["position"] as Vector3) + Vector3.UP * 0.05
	k.velocity = Vector3.ZERO
	scene.look_at_canvas(Vector2(1896.0, 2640.0), 0.0, 1.5)
	for i in 8:
		await physics_frame
		await process_frame
	for i in 50:
		k.drive_dir(Vector2(1, 0), false, DT)
		await physics_frame
		scene.settle_fade()
		await _frame()
	var g3 := CliffWorld.ground_at(space2, Vector2(3118.09, 1471.77), scene.right, scene.up, scene.fwd)
	k.global_position = (g3["position"] as Vector3) + Vector3.UP * 0.05
	k.velocity = Vector3.ZERO
	scene.look_at_canvas(Vector2(3300.0, 1180.0), 0.0, 1.15)
	for i in 8:
		await physics_frame
		await process_frame
	for i in 55:
		k.drive_dir(Vector2(0.42, -1.0), false, DT)
		await physics_frame
		await _frame()
	report["mp4_frames"] = _mf
	scene.set_lit(false)                      # the app ships in painted mode
	var f := FileAccess.open(out_dir + "/t9.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("[t9] -> %s  (%d movie frames)" % [out_dir, _mf])
	quit(0)


func _mirror() -> void:
	cam.global_transform = scene.cam.global_transform
	cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))


func _shot(name: String) -> void:
	_mirror()
	for i in 4:
		await process_frame
	vp.get_texture().get_image().save_png("%s/%s.png" % [out_dir, name])


func _frame() -> void:
	_mirror()
	await process_frame
	await process_frame
	vp.get_texture().get_image().save_jpg("%s/mp4frames/f_%04d.jpg" % [out_dir, _mf], 0.92)
	_mf += 1
