extends SceneTree
# C-9: the transitions MP4, the grip stills and the size-key heights, in one pass.
#
#   walk -> stop -> idle -> run -> stop -> attack -> walk, at the play camera, driven
#   through drive_dir exactly as the keyboard drives it, so what the video shows is what
#   the player gets rather than a scripted pose sequence.
#
#   Godot --path godot --resolution 1920x1080 --script tools/capture_trans.gd -- --out D

const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const DT := 1.0 / 24.0
const SPOT := Vector2(2285.62, 2407.32)
const STRIKE_FRAME := 16

var out_dir := ""
var scene
var vp: SubViewport
var cam: Camera3D
var report := {}
var _mf := 0


func _initialize() -> void:
	out_dir = ProjectSettings.globalize_path("user://trans")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir + "/mp4frames")
	Engine.physics_ticks_per_second = 24
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
	k.set_gear_stack(k.gear_stack_count() - 1)
	var skel: Skeleton3D = k._skel
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state

	# ---- the size key: what he measures at each step -----------------------
	var steps: Array = k.cfg.get("scale_steps", [])
	var he := skel.find_bone("head_end")
	var sizes := []
	var g0 := CliffWorld.ground_at(space, SPOT, scene.right, scene.up, scene.fwd)
	k.global_position = (g0["position"] as Vector3) + Vector3.UP * 0.02
	for s in steps:
		k.set_figure_scale(float(s))
		for i in 6:
			await physics_frame
			await process_frame
		var top: Vector3 = skel.global_transform * skel.get_bone_global_pose(he).origin
		var a := CliffWorld.canvas_of(top, scene.right, scene.up)
		var b := CliffWorld.canvas_of(Vector3(top.x, k.global_position.y, top.z), scene.right, scene.up)
		sizes.append({"scale": float(s), "world_height_m": snappedf(1.85 * float(s), 0.001),
					  "canvas_px": snappedf(absf(a.y - b.y), 0.1)})
		print("[cap] scale %.5f -> %.3f m, %.1f canvas px" %
			[float(s), 1.85 * float(s), absf(a.y - b.y)])
	report["size_steps"] = sizes

	# ---- the grips, one still per hand, idle and at the strike -------------
	k.set_figure_scale(float(k.cfg.get("scale_default_painted", 1.1)))
	k.facing = "S"
	k._drive()
	for i in 10:
		await physics_frame
		await process_frame
	var hands := {"right": skel.find_bone("RightHand"), "left": skel.find_bone("LeftHand")}
	for moment in ["idle", "strike"]:
		if moment == "strike":
			# pose the strike exactly, by seek, for the same reason as the axe still: a
			# tree stepped frame by frame starts wherever it happens to be
			var anim: AnimationPlayer = k._anim
			k._tree.active = false
			anim.active = true
			anim.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
			anim.play("attack")
			var aa := anim.get_animation("attack")
			anim.seek(aa.length * float(STRIKE_FRAME) / round(aa.length * 24.0), true, true)
			await process_frame
		for hand in hands:
			var w: Vector3 = skel.global_transform * skel.get_bone_global_pose(hands[hand]).origin
			var c := CliffWorld.canvas_of(w, scene.right, scene.up)
			scene.look_at_canvas(c, 0.0, 7.0)
			cam.global_transform = scene.cam.global_transform
			cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))
			for i in 4:
				await process_frame
			vp.get_texture().get_image().save_png("%s/grip_%s_%s.png" % [out_dir, hand, moment])
			print("[cap] grip still: %s hand, %s" % [hand, moment])
	var anim2: AnimationPlayer = k._anim
	anim2.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS
	anim2.active = false
	k._tree.active = true

	# ---- the transitions movie --------------------------------------------
	k.set_figure_scale(float(k.cfg.get("scale_default_painted", 1.1)))
	var g := CliffWorld.ground_at(space, Vector2(1666.0, 2705.0), scene.right, scene.up, scene.fwd)
	k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.05
	k.velocity = Vector3.ZERO
	k.facing = "E"
	k._drive()
	for i in 8:
		await physics_frame
		await process_frame
	var script := [
		["walk", Vector2(1, 0), false, 34],
		["stop", Vector2.ZERO, false, 20],
		["run", Vector2(1, 0), true, 26],
		["stop", Vector2.ZERO, false, 24],
		["attack", Vector2.ZERO, false, 0],
		["idle", Vector2.ZERO, false, 20],
		["walk", Vector2(-1, 0), false, 28],
	]
	for leg in script:
		if String(leg[0]) == "attack":
			k.try_attack()
			var guard := 0
			while k.attacking() and guard < 60:
				k.drive_dir(Vector2.ZERO, false, DT)
				await physics_frame
				await _frame()
				guard += 1
			continue
		for i in int(leg[3]):
			k.drive_dir(leg[1], bool(leg[2]), DT)
			await physics_frame
			scene.settle_fade()
			await _frame()
	report["mp4_frames"] = _mf
	var f := FileAccess.open(out_dir + "/capture_trans.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("[cap] -> %s  (%d frames)" % [out_dir, _mf])
	quit(0)


func _frame() -> void:
	cam.global_transform = scene.cam.global_transform
	cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))
	await process_frame
	await process_frame
	vp.get_texture().get_image().save_jpg("%s/mp4frames/f_%04d.jpg" % [out_dir, _mf], 0.92)
	_mf += 1
