extends SceneTree
# T12 (c) STILLS of chosen clip frames, BEFORE (installed) | AFTER (staged T12), raw clip seeks,
# full figure: per frame a column of four tiles -- before / after along the play camera, before /
# after level from his right. For looking at a penetration the acceptance table reports.
# env: STILLS "clip:t,clip:t,..." ; STILLS_OUT (jpg) ; STILLS_SIZE (ortho metres, default 2.4) ; STILLS_CENTER=hand
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
const TILE := 400
var ks := []
var svs := []
var cams := []

func _initialize() -> void:
	var specs: PackedStringArray = (OS.get_environment("STILLS") if OS.has_environment("STILLS") else "attack_chop:1.0").split(",")
	var outp: String = OS.get_environment("STILLS_OUT") if OS.has_environment("STILLS_OUT") else "/tmp/stills.jpg"
	var size: float = float(OS.get_environment("STILLS_SIZE")) if OS.has_environment("STILLS_SIZE") else 2.4
	var ground := StaticBody3D.new()
	ground.collision_layer = CliffWorld.TERRAIN_BIT
	var cs := CollisionShape3D.new(); var box := BoxShape3D.new(); box.size = Vector3(4000, 1, 4000)
	cs.shape = box; cs.position = Vector3(0, -0.5, 0); ground.add_child(cs); root.add_child(ground)
	var sun := DirectionalLight3D.new(); sun.rotation_degrees = Vector3(-50, 30, 0); root.add_child(sun)
	var we := WorldEnvironment.new(); var env := Environment.new()
	env.background_mode = Environment.BG_COLOR; env.background_color = Color(0.30, 0.32, 0.36)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR; env.ambient_light_color = Color(0.8, 0.8, 0.8)
	we.environment = env; root.add_child(we)
	for kp in ["res://scripts/knight_installed.gd", "res://scripts/knight.gd"]:
		var k = load(kp).new()
		k.setup(RIGHT, UP, FWD, 1.0)
		root.add_child(k)
		ks.append(k)
	for i in 6: await process_frame
	var face_w: Vector3 = ks[0].canvas_velocity_to_world(ks[0]._canvas_dir_for("SE")); face_w.y = 0.0; face_w = face_w.normalized()
	for i in 2:
		var k = ks[i]
		k.set_physics_process(false)
		k.set_gear_stack(k.gear_stack_count() - 1)
		k.facing = "SE"
		for j in 30: k.drive_dir(Vector2.ZERO, false, 1.0 / 24.0)
		k.global_position = face_w * (60.0 * float(i) - 30.0) + Vector3(0, 0.03, 0)
		k.drive_dir(Vector2.ZERO, false, 1.0 / 24.0)
		(k._tree as AnimationTree).active = false
		var ap: AnimationPlayer = k._anim
		ap.active = true
		ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	for i in 4: await process_frame
	for i in 4:
		var sv := SubViewport.new(); sv.size = Vector2i(TILE, TILE)
		sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(sv)
		var c := Camera3D.new(); c.projection = Camera3D.PROJECTION_ORTHOGONAL; c.size = size; c.near = 0.05; c.far = 200.0
		sv.add_child(c); c.current = true
		var lb := Label.new(); lb.name = "L"; lb.position = Vector2(4, 4)
		lb.add_theme_font_size_override("font_size", 13); lb.add_theme_color_override("font_color", Color(1, 1, 1))
		var sb := StyleBoxFlat.new(); sb.bg_color = Color(0, 0, 0, 0.65)
		sb.content_margin_left = 4; sb.content_margin_right = 4; sb.content_margin_top = 2; sb.content_margin_bottom = 2
		lb.add_theme_stylebox_override("normal", sb)
		sv.add_child(lb)
		svs.append(sv); cams.append(c)
	var sheet := Image.create(TILE * specs.size(), TILE * 4, false, Image.FORMAT_RGB8)
	for j in specs.size():
		var clip: String = specs[j].split(":")[0]
		var t: float = float(specs[j].split(":")[1])
		for k in ks:
			var ap: AnimationPlayer = k._anim
			ap.play(clip); ap.seek(t, true, true)
		for i in 2:
			var k = ks[i]
			var s: Skeleton3D = k._skel
			var tgt: Vector3 = k.global_position + Vector3(0, 0.95, 0)
			if OS.get_environment("STILLS_CENTER") == "hand":
				tgt = s.global_transform * s.get_bone_global_pose(s.find_bone("RightHand")).origin
			var his_right: Vector3 = s.global_transform.basis * Vector3(-1, 0, 0)
			his_right.y = 0.0; his_right = his_right.normalized()
			(cams[i] as Camera3D).look_at_from_position(tgt - FWD * 60.0, tgt, UP)
			(cams[2 + i] as Camera3D).look_at_from_position(tgt + his_right * 60.0, tgt, Vector3.UP)
		for i in 4:
			((svs[i] as SubViewport).get_node("L") as Label).text = "%s  %s %.3f s\n%s" % ["BEFORE" if i % 2 == 0 else "AFTER", clip, t, "play camera" if i < 2 else "from his right"]
		await process_frame
		await RenderingServer.frame_post_draw
		for i in 4:
			var im: Image = (svs[i] as SubViewport).get_texture().get_image()
			im.convert(Image.FORMAT_RGB8)
			var row: int = [0, 1, 2, 3][i]
			sheet.blit_rect(im, Rect2i(0, 0, TILE, TILE), Vector2i(j * TILE, row * TILE))
	sheet.save_jpg(outp, 0.9)
	print("[stills] %d frames -> %s" % [specs.size(), outp])
	quit(0)
