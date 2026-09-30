extends SceneTree
# STILLS OF RAW CLIP POSES, three views each: play camera | side (profile) | front.
#   --poses=clip@t,clip@t,...   --out=FILE.png   [--label=TEXT]
# The tree is off and the AnimationPlayer is seeked, so each tile is the clip's own pose.
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
const TW := 420
const TH := 520
var A := {}
var k
var svs := []
var cams := []
var labs := []

func _initialize() -> void:
	create_timer(300.0).timeout.connect(func(): push_error("WATCHDOG"); quit(4))
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--"):
			var kv: PackedStringArray = a.substr(2).split("=", true, 1)
			A[kv[0]] = kv[1] if kv.size() > 1 else "1"
	_world()
	k = load("res://scripts/knight.gd").new()
	k.setup(RIGHT, UP, FWD, 1.10)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	k.global_position = Vector3(0, 0.02, 0)
	k.facing = "S"
	k._drive(0.0)
	for i in 3: await process_frame
	(k._tree as AnimationTree).active = false
	var ap: AnimationPlayer = k._anim
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	for i in 3:
		var sv := SubViewport.new()
		sv.size = Vector2i(TW, TH)
		sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(sv)
		var c := Camera3D.new()
		c.projection = Camera3D.PROJECTION_ORTHOGONAL
		c.size = 2.9
		c.near = 0.1; c.far = 400.0
		sv.add_child(c); c.current = true
		var lb := Label.new()
		lb.position = Vector2(8, 6)
		lb.add_theme_font_size_override("font_size", 17)
		lb.add_theme_color_override("font_color", Color(1, 1, 1))
		var sb := StyleBoxFlat.new(); sb.bg_color = Color(0, 0, 0, 0.6)
		sb.content_margin_left = 6; sb.content_margin_right = 6; sb.content_margin_top = 3; sb.content_margin_bottom = 3
		lb.add_theme_stylebox_override("normal", sb)
		sv.add_child(lb)
		svs.append(sv); cams.append(c); labs.append(lb)
	var poses: PackedStringArray = String(A.get("poses", "idle_armed@0")).split(",")
	var sheet := Image.create(TW * 3, TH * poses.size(), false, Image.FORMAT_RGB8)
	for pi in poses.size():
		var pr: PackedStringArray = poses[pi].split("@")
		var clip := pr[0]
		var t := float(pr[1]) if pr.size() > 1 else 0.0
		ap.play(clip)
		ap.seek(t, true, true)
		k._drive(0.0)
		var tgt: Vector3 = k.global_position + Vector3(0, 1.1, 0)
		(cams[0] as Camera3D).look_at_from_position(tgt - FWD * 60.0, tgt, UP)
		var face: Vector3 = k.canvas_velocity_to_world(k._canvas_dir_for(k.facing))
		face.y = 0.0
		face = face.normalized()
		var side: Vector3 = face.cross(Vector3.UP)   # his right side, facing S
		(cams[1] as Camera3D).look_at_from_position(tgt - side * 60.0, tgt, Vector3.UP)
		(cams[2] as Camera3D).look_at_from_position(tgt + face * 60.0, tgt, Vector3.UP)
		var names := ["play camera", "his right side", "front"]
		for i in 3:
			(labs[i] as Label).text = "%s  %s @ %.2f s" % [names[i], clip, t] if i == 0 else String(names[i])
		for f in 3: await RenderingServer.frame_post_draw
		for i in 3:
			var im: Image = (svs[i] as SubViewport).get_texture().get_image()
			im.convert(Image.FORMAT_RGB8)
			sheet.blit_rect(im, Rect2i(0, 0, TW, TH), Vector2i(TW * i, TH * pi))
	sheet.save_png(String(A.get("out", "/tmp/axe_stills.png")))
	print("[stills] wrote ", String(A.get("out", "")), " (", poses.size(), " poses)")
	quit(0)

func _world() -> void:
	var mi := MeshInstance3D.new()
	var pm := PlaneMesh.new(); pm.size = Vector2(60, 60)
	mi.mesh = pm
	var sm := ShaderMaterial.new(); var sh := Shader.new()
	sh.code = "shader_type spatial;\nrender_mode unshaded;\nvarying vec3 wp;\nvoid vertex(){ wp = (MODEL_MATRIX * vec4(VERTEX,1.0)).xyz; }\nvoid fragment(){ vec2 c = floor(wp.xz / 0.5); float m = mod(c.x + c.y, 2.0); ALBEDO = mix(vec3(0.42,0.40,0.36), vec3(0.58,0.56,0.51), m); }"
	sm.shader = sh; mi.material_override = sm
	root.add_child(mi)
	var sun := DirectionalLight3D.new(); sun.rotation_degrees = Vector3(-50, 30, 0); root.add_child(sun)
	var we := WorldEnvironment.new(); var env := Environment.new()
	env.background_mode = Environment.BG_COLOR; env.background_color = Color(0.16, 0.17, 0.19)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR; env.ambient_light_color = Color(0.8, 0.8, 0.8)
	we.environment = env; root.add_child(we)
