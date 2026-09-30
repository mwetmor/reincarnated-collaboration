extends SceneTree
# One look at Meshy's Combat_Stance on his rig: play camera | his right side | front, three times.
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
func _initialize() -> void:
	create_timer(120.0).timeout.connect(func(): print("[still] WATCHDOG"); quit(4))
	var sun := DirectionalLight3D.new(); sun.rotation_degrees = Vector3(-50, 30, 0); root.add_child(sun)
	var we := WorldEnvironment.new(); var env := Environment.new()
	env.background_mode = Environment.BG_COLOR; env.background_color = Color(0.16, 0.17, 0.19)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR; env.ambient_light_color = Color(0.8, 0.8, 0.8)
	we.environment = env; root.add_child(we)
	var sc := (load("res://models/anims/combat_stance.glb") as PackedScene).instantiate()
	root.add_child(sc)
	var ap: AnimationPlayer = null; var sk: Skeleton3D = null
	for n in sc.find_children("*", "", true, false):
		if n is AnimationPlayer and ap == null: ap = n
		if n is Skeleton3D and sk == null: sk = n
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var clip: String = ap.get_animation_list()[0]
	ap.play(clip)
	var svs := []; var cams := []
	for i in 3:
		var sv := SubViewport.new(); sv.size = Vector2i(420, 520); sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(sv)
		var c := Camera3D.new(); c.projection = Camera3D.PROJECTION_ORTHOGONAL; c.size = 2.4; c.near = 0.1; c.far = 400.0
		sv.add_child(c); c.current = true
		svs.append(sv); cams.append(c)
	var sheet := Image.create(420 * 3, 520 * 3, false, Image.FORMAT_RGB8)
	var times := [0.2, 0.8, 1.4]
	for ti in 3:
		ap.seek(float(times[ti]), true, true)
		var hips: Vector3 = sk.global_transform * sk.get_bone_global_pose(sk.find_bone("Hips")).origin
		var tgt: Vector3 = hips + Vector3(0, 0.2, 0)
		(cams[0] as Camera3D).look_at_from_position(tgt - FWD * 60.0, tgt, UP)
		(cams[1] as Camera3D).look_at_from_position(tgt + Vector3(-60, 0, 0), tgt, Vector3.UP)
		(cams[2] as Camera3D).look_at_from_position(tgt + Vector3(0, 0, 60), tgt, Vector3.UP)
		for f in 3: await RenderingServer.frame_post_draw
		for i in 3:
			var im: Image = (svs[i] as SubViewport).get_texture().get_image(); im.convert(Image.FORMAT_RGB8)
			sheet.blit_rect(im, Rect2i(0, 0, 420, 520), Vector2i(420 * i, 520 * ti))
	sheet.save_png(OS.get_environment("STILL_OUT"))
	print("[still] ok")
	quit(0)
