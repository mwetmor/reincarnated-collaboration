extends SceneTree
# ARMED SPEED, side by side at quarter speed: UNARMED | ARMED TODAY | ARMED WITH THE SPLIT.
# Three knights on one checkered floor (0.5 m squares), 4 m apart, the same input to each:
# stand, walk, run, stop. Each panel's play camera follows its own knight, so the floor
# scrolling under him IS his ground speed; the label prints the measured speed.
#   --fixed-fps 96 ; frames to <out>/f_%05d.jpg
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
const DT := 1.0 / 96.0
var ks := []
var svs := []
var cams := []
var labs := []
var prev := []
var mf := 0
var out_dir := ""
var spd := [0.0, 0.0, 0.0]

func _initialize() -> void:
	var wd := Time.get_ticks_msec() + 1800000
	out_dir = OS.get_environment("FILM_OUT") if OS.has_environment("FILM_OUT") else "/tmp/film_split"
	DirAccess.make_dir_recursive_absolute(out_dir)
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
	var specs := [["res://scripts/knight.gd", false, "UNARMED"], ["res://scripts/knight_before.gd", true, "ARMED TODAY (armed gait clips)"],
				  ["res://scripts/knight.gd", true, "ARMED + SPLIT (unarmed legs, armed upper body)"]]
	for i in 3:
		var k = load(String(specs[i][0])).new()
		k.setup(RIGHT, UP, FWD, 1.0)
		root.add_child(k)
		ks.append(k)
	for i in 6: await process_frame
	for i in 3:
		var k = ks[i]
		k.set_physics_process(false)
		k.set_gear_stack(k.gear_stack_count() - 1 if bool(specs[i][1]) else 0)
		k.global_position = RIGHT * (float(i) - 1.0) * -4.0 + Vector3(0, 0.03, 0)
		k.velocity = Vector3.ZERO
		(k._tree as AnimationTree).callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
		prev.append(k.global_position)
		var sv := SubViewport.new(); sv.size = Vector2i(640, 1080)
		sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(sv)
		var c := Camera3D.new(); c.projection = Camera3D.PROJECTION_ORTHOGONAL; c.size = 3.4; c.near = 0.1; c.far = 400.0
		sv.add_child(c); c.current = true
		var lb := Label.new(); lb.position = Vector2(10, 10)
		lb.add_theme_font_size_override("font_size", 20); lb.add_theme_color_override("font_color", Color(1, 1, 1))
		var sb := StyleBoxFlat.new(); sb.bg_color = Color(0, 0, 0, 0.6)
		sb.content_margin_left = 8; sb.content_margin_right = 8; sb.content_margin_top = 4; sb.content_margin_bottom = 4
		lb.add_theme_stylebox_override("normal", sb)
		sv.add_child(lb)
		svs.append(sv); cams.append(c); labs.append(lb)
		labs[i].set_meta("title", String(specs[i][2]))
	# stand 1 s, walk 3 s, run 4 s, stop 1.5 s -- game time, 1/96 s steps
	for seg in [[96, Vector2.ZERO, false, "standing"], [288, Vector2(1, 0), false, "walk"], [384, Vector2(1, 0), true, "run"], [144, Vector2.ZERO, false, "stop"]]:
		for j in int(seg[0]):
			if Time.get_ticks_msec() > wd:
				print("[film] WATCHDOG"); quit(4); return
			for i in 3:
				var k = ks[i]
				k.drive_dir(seg[1], bool(seg[2]), DT)
				(k._tree as AnimationTree).advance(DT)
				var p: Vector3 = k.global_position
				var d: Vector3 = p - (prev[i] as Vector3); d.y = 0.0
				spd[i] = lerpf(float(spd[i]), d.length() / DT, 0.08)
				prev[i] = p
			_place(String(seg[3]))
			await physics_frame
			await RenderingServer.frame_post_draw
			_grab()
	print("[film] %d frames -> %s" % [mf, out_dir])
	quit(0)

func _place(phase: String) -> void:
	for i in 3:
		var k = ks[i]
		var tgt: Vector3 = k.global_position + Vector3(0, 0.95, 0)
		(cams[i] as Camera3D).look_at_from_position(tgt - FWD * 60.0, tgt, UP)
		(labs[i] as Label).text = "%s\n%s   %.2f m/s   QUARTER SPEED" % [String((labs[i] as Label).get_meta("title")), phase, float(spd[i])]

func _grab() -> void:
	var img := Image.create(1920, 1080, false, Image.FORMAT_RGB8)
	for i in 3:
		var im: Image = (svs[i] as SubViewport).get_texture().get_image()
		im.convert(Image.FORMAT_RGB8)
		img.blit_rect(im, Rect2i(0, 0, 640, 1080), Vector2i(640 * i, 0))
	img.save_jpg("%s/f_%05d.jpg" % [out_dir, mf], 0.88)
	mf += 1
