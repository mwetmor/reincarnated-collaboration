extends SceneTree
# T12 (c) FILMS -- BEFORE (the installed state: knight.gd bf23c13e, character.json b3b62c63, the
# installed GLBs) beside AFTER (the staged T12 guard: the axe_guard_R layer, idle_guard, the
# weapon_r channel), the same input to each, one step of 1/96 s of game time per frame: encoded
# at 24 fps that is QUARTER SPEED. Top row the play camera (ortho, pitch 52.95, each following its
# own knight); bottom row a level side camera on his RIGHT (the axe side), square to his facing.
# One film per action -- idle, walk, run, slash, chop, block -- facing SE. The two knights stand
# 60 m apart along his facing, so neither camera sees the other one.
# Frames to <FILM_OUT>/<action>/f_%05d.jpg. Run with --fixed-fps 96.
# env: FILM_OUT, FILM_ACTIONS (comma list; default all six)
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
const DT := 1.0 / 96.0
const FACE := "SE"
var ks := []
var titles := ["BEFORE -- installed (knight bf23c13e)", (OS.get_environment("FILM_AFTER_TITLE") if OS.has_environment("FILM_AFTER_TITLE") else "AFTER -- T12 guard layer (staged)")]
var svs := []
var cams := []
var labs := []
var out_dir := ""
var film_dir := ""
var mf := 0
var action := ""
var phase := ""
var wd_ms := 0
var face_w := Vector3.ZERO

func _initialize() -> void:
	wd_ms = Time.get_ticks_msec() + 3600000
	out_dir = OS.get_environment("FILM_OUT") if OS.has_environment("FILM_OUT") else "/tmp/guard_film"
	var acts: PackedStringArray = (OS.get_environment("FILM_ACTIONS") if OS.has_environment("FILM_ACTIONS") else "idle,walk,run,slash,chop,block").split(",")
	Engine.physics_ticks_per_second = 96
	var ground := StaticBody3D.new()
	ground.collision_layer = CliffWorld.TERRAIN_BIT
	var cs := CollisionShape3D.new(); var box := BoxShape3D.new(); box.size = Vector3(4000, 1, 4000)
	cs.shape = box; cs.position = Vector3(0, -0.5, 0); ground.add_child(cs); root.add_child(ground)
	var mi := MeshInstance3D.new(); var pm := PlaneMesh.new(); pm.size = Vector2(4000, 4000); mi.mesh = pm
	var sm := ShaderMaterial.new(); var sh := Shader.new()
	sh.code = "shader_type spatial;\nrender_mode unshaded;\nvarying vec3 wp;\nvoid vertex(){ wp = (MODEL_MATRIX * vec4(VERTEX,1.0)).xyz; }\nvoid fragment(){ vec2 c = floor(wp.xz / 0.5); float m = mod(c.x + c.y, 2.0); ALBEDO = mix(vec3(0.42,0.40,0.36), vec3(0.58,0.56,0.51), m); }"
	sm.shader = sh; mi.material_override = sm; root.add_child(mi)
	var sun := DirectionalLight3D.new(); sun.rotation_degrees = Vector3(-50, 30, 0); root.add_child(sun)
	var we := WorldEnvironment.new(); var env := Environment.new()
	env.background_mode = Environment.BG_COLOR; env.background_color = Color(0.16, 0.17, 0.19)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR; env.ambient_light_color = Color(0.8, 0.8, 0.8)
	we.environment = env; root.add_child(we)
	for kp in ["res://scripts/knight_installed.gd", "res://scripts/knight.gd"]:
		var k = load(kp).new()
		k.setup(RIGHT, UP, FWD, 1.0)
		root.add_child(k)
		ks.append(k)
	for i in 6: await process_frame
	for k in ks:
		k.set_physics_process(false)
		k.set_gear_stack(k.gear_stack_count() - 1)
		(k._tree as AnimationTree).callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	for i in 4: await process_frame
	face_w = ks[0].canvas_velocity_to_world(ks[0]._canvas_dir_for(FACE)); face_w.y = 0.0; face_w = face_w.normalized()
	for i in 4:
		var sv := SubViewport.new(); sv.size = Vector2i(960, 540)
		sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(sv)
		var c := Camera3D.new(); c.projection = Camera3D.PROJECTION_ORTHOGONAL; c.size = 2.7; c.near = 0.1; c.far = 400.0
		sv.add_child(c); c.current = true
		var lb := Label.new(); lb.position = Vector2(10, 8)
		lb.add_theme_font_size_override("font_size", 18); lb.add_theme_color_override("font_color", Color(1, 1, 1))
		var sb := StyleBoxFlat.new(); sb.bg_color = Color(0, 0, 0, 0.6)
		sb.content_margin_left = 6; sb.content_margin_right = 6; sb.content_margin_top = 3; sb.content_margin_bottom = 3
		lb.add_theme_stylebox_override("normal", sb)
		sv.add_child(lb)
		svs.append(sv); cams.append(c); labs.append(lb)
	for act in acts:
		await _film(String(act))
		if Time.get_ticks_msec() > wd_ms:
			print("[film] WATCHDOG"); quit(4); return
	print("[film] done")
	quit(0)

func _reset() -> void:
	# unfilmed: both knights back to standing, facing SE, 60 m apart along the facing
	for k in ks:
		k.set_block(false)
		k.facing = FACE
	for j in 144:
		for k in ks:
			k.drive_dir(Vector2.ZERO, false, DT)
			(k._tree as AnimationTree).advance(DT)
	for i in 2:
		var k = ks[i]
		k.global_position = face_w * (60.0 * float(i) - 30.0) + Vector3(0, 0.03, 0)
		k.velocity = Vector3.ZERO

func _film(act: String) -> void:
	_reset()
	action = act
	film_dir = "%s/%s" % [out_dir, act]
	DirAccess.make_dir_recursive_absolute(film_dir)
	mf = 0
	var d := ks[0]._canvas_dir_for(FACE) as Vector2
	match act:
		"idle":
			await _hold(Vector2.ZERO, false, 4.0, "standing")
		"walk":
			await _hold(Vector2.ZERO, false, 0.5, "standing")
			await _hold(d, false, 3.0, "walk")
			await _hold(Vector2.ZERO, false, 0.75, "stop")
		"run":
			await _hold(Vector2.ZERO, false, 0.5, "standing")
			await _hold(d, true, 3.0, "run")
			await _hold(Vector2.ZERO, false, 1.0, "stop")
		"slash", "chop":
			await _hold(Vector2.ZERO, false, 0.5, "standing")
			for k in ks: k.try_strike(act)
			var g := 0
			while g < 24 or ks[0].attacking() or ks[1].attacking():
				await _step(Vector2.ZERO, false, act)
				g += 1
				if g > 96 * 12: break
			await _hold(Vector2.ZERO, false, 0.75, "after the " + act)
		"block":
			await _hold(Vector2.ZERO, false, 0.5, "standing")
			for k in ks: k.set_block(true)
			await _hold(Vector2.ZERO, false, 2.5, "block held")
			for k in ks: k.set_block(false)
			await _hold(Vector2.ZERO, false, 1.25, "block released")
	print("[film] %s: %d frames -> %s" % [act, mf, film_dir])

func _hold(dir: Vector2, run: bool, secs: float, ph: String) -> void:
	for j in int(round(secs / DT)):
		await _step(dir, run, ph)

func _step(dir: Vector2, run: bool, ph: String) -> void:
	phase = ph
	for k in ks:
		k.drive_dir(dir, run, DT)
		(k._tree as AnimationTree).advance(DT)
	_place()
	await process_frame
	await RenderingServer.frame_post_draw
	_grab()

func _place() -> void:
	for i in 2:
		var k = ks[i]
		var tgt: Vector3 = k.global_position + Vector3(0, 0.95, 0)
		(cams[i] as Camera3D).look_at_from_position(tgt - FWD * 60.0, tgt, UP)
		# his right in the skeleton's own frame is -X (forward +Z, up +Y)
		var his_right: Vector3 = (k._skel as Skeleton3D).global_transform.basis * Vector3(-1, 0, 0)
		his_right.y = 0.0; his_right = his_right.normalized()
		(cams[2 + i] as Camera3D).look_at_from_position(tgt + his_right * 60.0, tgt, Vector3.UP)
		(labs[i] as Label).text = "%s\n%s -- %s   QUARTER SPEED   play camera" % [titles[i], action.to_upper(), phase]
		(labs[2 + i] as Label).text = "%s\nside camera, his right" % titles[i]

func _grab() -> void:
	var img := Image.create(1920, 1080, false, Image.FORMAT_RGB8)
	for i in 4:
		var im: Image = (svs[i] as SubViewport).get_texture().get_image()
		im.convert(Image.FORMAT_RGB8)
		img.blit_rect(im, Rect2i(0, 0, 960, 540), Vector2i(960 * (i % 2), 540 * (i / 2)))
	img.save_jpg("%s/f_%05d.jpg" % [film_dir, mf], 0.88)
	mf += 1
