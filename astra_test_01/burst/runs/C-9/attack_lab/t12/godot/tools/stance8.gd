extends SceneTree
# R-C9-122 STANCE SHEET: his standing pose at the 8 game headings, through the knight's own tree (the game's blend, the
# guard layer on), ortho at the play camera's pitch -- row 1 ARMED (the full gear stack: idle_guard + the guard layer),
# row 2 UNARMED (gear stack 0: the plain idle). The camera goes round him (azimuth 47 + 45 k, the gate's 8 cells), so
# every tile is the same moment seen from one of the 8 directions the game can show him in.
# env: STANCE_OUT (png), STANCE_LABEL, STANCE_SIZE (ortho metres, default 2.3)
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
const PITCH_DEG := 52.9535411256029
const DT := 1.0 / 60.0
const CW := 300
const CH := 360
var k
var tree: AnimationTree

func _initialize() -> void:
	create_timer(600.0).timeout.connect(func(): print("[stance8] WATCHDOG"); quit(4))
	var outp: String = OS.get_environment("STANCE_OUT") if OS.has_environment("STANCE_OUT") else "/tmp/stance8.png"
	var label: String = OS.get_environment("STANCE_LABEL") if OS.has_environment("STANCE_LABEL") else ""
	var size: float = float(OS.get_environment("STANCE_SIZE")) if OS.has_environment("STANCE_SIZE") else 2.3
	var ground := StaticBody3D.new()
	ground.collision_layer = CliffWorld.TERRAIN_BIT
	var cs := CollisionShape3D.new(); var box := BoxShape3D.new(); box.size = Vector3(4000, 1, 4000)
	cs.shape = box; cs.position = Vector3(0, -0.5, 0); ground.add_child(cs); root.add_child(ground)
	var sun := DirectionalLight3D.new(); sun.rotation_degrees = Vector3(-55, 35, 0); root.add_child(sun)
	var we := WorldEnvironment.new(); var env := Environment.new()
	env.background_mode = Environment.BG_COLOR; env.background_color = Color(0.86, 0.84, 0.80)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR; env.ambient_light_color = Color(0.75, 0.75, 0.78)
	we.environment = env; root.add_child(we)
	k = load("res://scripts/knight.gd").new()
	k.setup(RIGHT, UP, FWD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	tree = k._tree
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var sv := SubViewport.new(); sv.size = Vector2i(CW, CH); sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(sv)
	var cam := Camera3D.new(); cam.projection = Camera3D.PROJECTION_ORTHOGONAL; cam.size = size; cam.near = 0.1; cam.far = 200.0
	sv.add_child(cam); cam.current = true
	var lb := Label.new(); lb.position = Vector2(5, 4); lb.add_theme_font_size_override("font_size", 13)
	lb.add_theme_color_override("font_color", Color(0.1, 0.1, 0.12)); sv.add_child(lb)
	var sheet := Image.create(CW * 8, CH * 2, false, Image.FORMAT_RGB8)
	var rows := [["armed guard", k.gear_stack_count() - 1], ["unarmed idle", 0]]
	for r in rows.size():
		k.set_gear_stack(int(rows[r][1]))
		for i in 4: await process_frame
		k.global_position = Vector3(0, 0.03, 0)
		for i in 90:
			k.drive_dir(Vector2.ZERO, false, DT); tree.advance(DT)
		var sk: Skeleton3D = k._skel
		var hips: Vector3 = (sk.global_transform * sk.get_bone_global_pose(sk.find_bone("Hips"))).origin
		var tgt := Vector3(hips.x, hips.y * 0.55 + 0.25, hips.z)
		for c in 8:
			var y := deg_to_rad(47.0 + 45.0 * float(c)); var th := deg_to_rad(PITCH_DEG)
			var fh := Vector3(sin(y), 0, cos(y))
			var dv := (fh * cos(th) + Vector3(0, -1, 0) * sin(th)).normalized()
			cam.look_at_from_position(tgt - dv * 30.0, tgt, Vector3.UP)
			lb.text = "%s | %s | cell %d" % [label, String(rows[r][0]), c]
			for i in 3: await process_frame
			await RenderingServer.frame_post_draw
			var im: Image = sv.get_texture().get_image(); im.convert(Image.FORMAT_RGB8)
			sheet.blit_rect(im, Rect2i(0, 0, CW, CH), Vector2i(c * CW, r * CH))
	sheet.save_png(outp)
	print("[stance8] %s -> %s" % [label, outp])
	quit(0)
