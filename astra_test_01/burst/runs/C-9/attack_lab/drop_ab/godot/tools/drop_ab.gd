extends SceneTree
# THE DROP. Matt: "after swinging his axe, he drops to the floor as if drunk." This replays
# shot_barrow_armed.gd's sequence exactly -- idle 24; slash, until done, 12; chop, until done, 12;
# block 24, release, 18; then a run of 24 and slash / chop / block from it -- on flat ground at
# figure scale 1.0 (the Barrow's), with the tree and the modifiers in the modes the game ships:
# the tree on PHYSICS frames, the skeleton modifiers on IDLE frames. Run with --fixed-fps.
# Recorded per frame:
#   pelvis      Hips height above the ground (m); the IK does not move the hips, so the animated
#               Hips IS the shown Hips
#   knees       the knee angle each leg SHOWS: from the hip, the ankle as shown (the foot lock's
#               own post-IK record when it exists) and the two bone lengths -- exact for a
#               two-bone chain; 180 = straight
#   block       _block_phase, _block_w; the strike one-shots' activity
# env: DROP_KNIGHT (script), DROP_LABEL, DROP_OUT (json), DROP_FILM (dir; frames), DROP_DT (s/step)
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
var k
var skel: Skeleton3D
var fl = null
var DT := 1.0 / 24.0
var rows := []
var label := ""
var film := ""
var cams := []
var svs := []
var mf := 0
var bones := {}
var lens := {}
var _wd_ms := 0

func _initialize() -> void:
	var wd: float = float(OS.get_environment("DROP_WATCHDOG_S")) if OS.has_environment("DROP_WATCHDOG_S") else 900.0
	_wd_ms = Time.get_ticks_msec() + int(wd * 1000.0)
	print("[drop] watchdog %.0f s of WALL time (a SceneTree timer runs on game time, which --fixed-fps decouples from the clock)" % wd)
	label = OS.get_environment("DROP_LABEL") if OS.has_environment("DROP_LABEL") else "?"
	film = OS.get_environment("DROP_FILM") if OS.has_environment("DROP_FILM") else ""
	if OS.has_environment("DROP_DT"): DT = float(OS.get_environment("DROP_DT"))
	Engine.physics_ticks_per_second = int(round(1.0 / DT))
	var ground := StaticBody3D.new()
	ground.collision_layer = CliffWorld.TERRAIN_BIT
	var cs := CollisionShape3D.new(); var box := BoxShape3D.new(); box.size = Vector3(400, 1, 400)
	cs.shape = box; cs.position = Vector3(0, -0.5, 0); ground.add_child(cs); root.add_child(ground)
	var kp: String = OS.get_environment("DROP_KNIGHT") if OS.has_environment("DROP_KNIGHT") else "res://scripts/knight.gd"
	k = load(kp).new()
	k.setup(RIGHT, UP, FWD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_gear_stack(k.gear_stack_count() - 1)
	k.set_physics_process(false)
	k.global_position = Vector3(0, 0.03, 0)
	k.velocity = Vector3.ZERO
	k.facing = "N"
	skel = k._skel
	fl = k.get("_foot_lock")
	for bn in ["Hips", "LeftUpLeg", "LeftLeg", "LeftFoot", "RightUpLeg", "RightLeg", "RightFoot", "LeftToeBase", "RightToeBase"]:
		bones[bn] = skel.find_bone(bn)
	var s_: float = skel.global_transform.basis.get_scale().x
	for side in ["Left", "Right"]:
		var a: Vector3 = skel.get_bone_global_rest(bones[side + "UpLeg"]).origin
		var b: Vector3 = skel.get_bone_global_rest(bones[side + "Leg"]).origin
		var c: Vector3 = skel.get_bone_global_rest(bones[side + "Foot"]).origin
		lens[side] = [(b - a).length() * s_, (c - b).length() * s_]
	if film != "":
		_build_film()
	print("[drop] %s knight=%s foot_lock=%s model=%s dt=%.4f" % [label, kp.get_file(), str(fl != null), String(k.cfg.get("model", "")), DT])
	var n24 := func(n: int) -> int: return int(round(float(n) * (1.0 / 24.0) / DT))
	await _hold(Vector2.ZERO, false, n24.call(24), "idle")
	for which in ["slash", "chop"]:
		k.try_strike(which)
		await _until_done(n24.call(12), which + "_idle")
		await _hold(Vector2.ZERO, false, n24.call(12), "after_" + which + "_idle")
	k.set_block(true)
	await _hold(Vector2.ZERO, false, n24.call(24), "block_idle")
	k.set_block(false)
	await _hold(Vector2.ZERO, false, n24.call(18), "after_block_idle")
	var dirs := [Vector2(0, -1), Vector2(0, 1), Vector2(0, -1)]
	var i := 0
	for which in ["slash", "chop", "block"]:
		await _hold(dirs[i], true, n24.call(24), "run_" + which)
		if which == "block":
			k.set_block(true)
			await _hold(Vector2.ZERO, false, n24.call(24), "block_run")
			k.set_block(false)
			await _hold(Vector2.ZERO, false, n24.call(18), "after_block_run")
		else:
			k.try_strike(which)
			await _until_done(n24.call(12), which + "_run")
		i += 1
	await _hold(Vector2.ZERO, false, n24.call(12), "end")
	# THE IDLE'S OWN RESTING PELVIS: idle_armed sampled raw, same rig, same scale
	var ap: AnimationPlayer = k._anim
	var tree: AnimationTree = k._tree
	tree.active = false
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var idle_clip := String(k._roles.get("idle", "idle_armed"))
	var ia := ap.get_animation(idle_clip)
	ap.play(idle_clip)
	var hs := []
	var nn: int = int(round(ia.length * 24.0))
	for j in nn + 1:
		ap.seek(ia.length * float(j) / float(nn), true, true)
		hs.append((skel.global_transform * skel.get_bone_global_pose(bones["Hips"]).origin).y - k.global_position.y)
	hs.sort()
	var rest_skel: float = (skel.global_transform * skel.get_bone_global_rest(bones["Hips"]).origin).y - k.global_position.y
	var idle_rest := {"clip": idle_clip, "median": float(hs[hs.size() / 2]), "p10": float(hs[int(hs.size() * 0.1)]),
					  "p90": float(hs[int(hs.size() * 0.9)]), "min": float(hs[0]), "max": float(hs[-1]), "skeleton_rest": rest_skel}
	var out := {"label": label, "knight": kp, "model": String(k.cfg.get("model", "")), "foot_lock": fl != null,
				"dt": DT, "idle_rest": idle_rest, "rows": rows}
	var f := FileAccess.open(OS.get_environment("DROP_OUT") if OS.has_environment("DROP_OUT") else "/tmp/drop.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out)); f.close()
	print("[drop] %s idle '%s' pelvis median %.3f (p10 %.3f, p90 %.3f, min %.3f) m; skeleton rest %.3f m; %d frames"
		% [label, idle_clip, idle_rest["median"], idle_rest["p10"], idle_rest["p90"], idle_rest["min"], rest_skel, rows.size()])
	quit(0)

func _knee(side: String, hip: Vector3, ankle: Vector3) -> float:
	var a: float = float(lens[side][0]); var b: float = float(lens[side][1])
	var d: float = (ankle - hip).length()
	return rad_to_deg(acos(clampf((a * a + b * b - d * d) / (2.0 * a * b), -1.0, 1.0)))

func _record(tag: String) -> void:
	var g: Transform3D = skel.global_transform
	var hip: Vector3 = g * skel.get_bone_global_pose(bones["Hips"]).origin
	var gy: float = 0.0
	var r := {"t": float(rows.size()) * DT, "tag": tag, "pelvis": hip.y - gy}
	for side in ["Left", "Right"]:
		var h: Vector3 = g * skel.get_bone_global_pose(bones[side + "UpLeg"]).origin
		var kn: Vector3 = g * skel.get_bone_global_pose(bones[side + "Leg"]).origin
		var anim_ankle: Vector3 = g * skel.get_bone_global_pose(bones[side + "Foot"]).origin
		lens[side] = [(kn - h).length(), (anim_ankle - kn).length()]
		var shown: Vector3 = anim_ankle
		if fl != null:
			var st = fl.st[side.substr(0, 1)]
			if st is Dictionary and (st as Dictionary).get("shown", Vector3.INF) != Vector3.INF:
				shown = st["shown"]
		r["knee_" + side.substr(0, 1)] = _knee(side, h, shown)
		r["knee_anim_" + side.substr(0, 1)] = _knee(side, h, anim_ankle)
		r["ankle_gap_" + side.substr(0, 1)] = (shown - anim_ankle).length()
		r["toe_" + side.substr(0, 1)] = (g * skel.get_bone_global_pose(bones[side + "ToeBase"]).origin).y - gy
	r["block_phase"] = str(k.get("_block_phase"))
	r["block_w"] = float(k.get("_block_w")) if k.get("_block_w") != null else -1.0
	r["attacking"] = bool(k.attacking())
	r["speed"] = float(k.speed_px_s())
	if fl != null:
		r["gap_rel"] = int(fl.get("gap_releases")) if fl.get("gap_releases") != null else -1
	rows.append(r)

func _step(dir: Vector2, run: bool, tag: String) -> void:
	if Time.get_ticks_msec() > _wd_ms:
		print("[drop] WATCHDOG at frame %d" % rows.size()); quit(4); return
	k.drive_dir(dir, run, DT)
	await physics_frame
	await process_frame
	_record(tag)
	if film != "":
		await RenderingServer.frame_post_draw
		_shoot(tag)

func _hold(dir: Vector2, run: bool, n: int, tag: String) -> void:
	for j in n:
		await _step(dir, run, tag)

func _until_done(tail: int, tag: String) -> void:
	var g := 0
	var min_frames: int = int(round(6.0 * (1.0 / 24.0) / DT))
	while (k.attacking() or g < min_frames) and g < int(400.0 * (1.0 / 24.0) / DT):
		await _step(Vector2.ZERO, false, tag)
		g += 1
	await _hold(Vector2.ZERO, false, tail, "tail_" + tag)

func _build_film() -> void:
	var sun := DirectionalLight3D.new(); sun.rotation_degrees = Vector3(-50, 30, 0); root.add_child(sun)
	var we := WorldEnvironment.new(); var env := Environment.new()
	env.background_mode = Environment.BG_COLOR; env.background_color = Color(0.16, 0.17, 0.19)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR; env.ambient_light_color = Color(0.8, 0.8, 0.8)
	we.environment = env; root.add_child(we)
	var mi := MeshInstance3D.new(); var pm := PlaneMesh.new(); pm.size = Vector2(400, 400); mi.mesh = pm
	var sm := ShaderMaterial.new(); var sh := Shader.new()
	sh.code = "shader_type spatial;\nrender_mode unshaded;\nvarying vec3 wp;\nvoid vertex(){ wp = (MODEL_MATRIX * vec4(VERTEX,1.0)).xyz; }\nvoid fragment(){ vec2 c = floor(wp.xz / 0.5); float m = mod(c.x + c.y, 2.0); ALBEDO = mix(vec3(0.42,0.40,0.36), vec3(0.58,0.56,0.51), m); }"
	sm.shader = sh; mi.material_override = sm; root.add_child(mi)
	for i in 2:
		var sv := SubViewport.new(); sv.size = Vector2i(960, 1080)
		sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(sv)
		var c := Camera3D.new(); c.projection = Camera3D.PROJECTION_ORTHOGONAL; c.size = 3.2; c.near = 0.1; c.far = 400.0
		sv.add_child(c); c.current = true
		var lb := Label.new(); lb.name = "L"; lb.position = Vector2(14, 12)
		lb.add_theme_font_size_override("font_size", 24); lb.add_theme_color_override("font_color", Color(1, 1, 1))
		var sb := StyleBoxFlat.new(); sb.bg_color = Color(0, 0, 0, 0.6)
		sb.content_margin_left = 8; sb.content_margin_right = 8; sb.content_margin_top = 4; sb.content_margin_bottom = 4
		lb.add_theme_stylebox_override("normal", sb)
		sv.add_child(lb)
		svs.append(sv); cams.append(c)

func _shoot(tag: String) -> void:
	var tgt: Vector3 = k.global_position + Vector3(0, 0.95, 0)
	(cams[0] as Camera3D).look_at_from_position(tgt - FWD * 60.0, tgt, UP)
	var face: Vector3 = k.canvas_velocity_to_world(k._canvas_dir_for(k.facing))
	face.y = 0.0
	var side: Vector3 = face.normalized().cross(Vector3.UP)
	(cams[1] as Camera3D).look_at_from_position(tgt - side * 60.0, tgt, Vector3.UP)
	var r: Dictionary = rows[-1]
	((svs[0] as SubViewport).get_node("L") as Label).text = "%s   QUARTER SPEED\n%s   pelvis %.2f m\nplay camera" % [label, tag, float(r["pelvis"])]
	((svs[1] as SubViewport).get_node("L") as Label).text = "side camera"
	var img := Image.create(1920, 1080, false, Image.FORMAT_RGB8)
	for i in 2:
		var im: Image = (svs[i] as SubViewport).get_texture().get_image()
		im.convert(Image.FORMAT_RGB8)
		img.blit_rect(im, Rect2i(0, 0, 960, 1080), Vector2i(960 * i, 0))
	if mf == 0: DirAccess.make_dir_recursive_absolute(film)
	img.save_jpg("%s/f_%05d.jpg" % [film, mf], 0.9)
	mf += 1
