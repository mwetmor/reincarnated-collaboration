extends SceneTree
# T12 (c) CLOSE-UPS OF THE GRIP -- BEFORE (installed) against AFTER (staged T12 guard), the same
# input to each. For each hold state, through the tree, the frame where the AFTER haft leaves the
# fist's channel the MOST (the worst fist turn over one loop: weapon_r's haft against its rest);
# for the slash and the chop, the strike frame (the clip time given by ACCEPT_JSON, the after
# table). Two views: along the play camera, and level from his right. Ortho, 0.55 m tall,
# centred on the fist (the grip point: weapon_r's rest origin in the hand's frame, for both).
# Output: <CLOSE_OUT>/closeup_play.jpg and closeup_side.jpg -- 4 columns; rows in pairs, BEFORE
# above AFTER: idle, walk, run, block / strafe L, strafe R, slash, chop.
# env: CLOSE_OUT, ACCEPT_JSON
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
const DT := 1.0 / 24.0
const TILE := 360
const FACE := "SE"
var ks := []
var svs := []      # [before play, after play, before side, after side]
var cams := []
var grip_l := Vector3.ZERO   # the grip point in RightHand's frame (weapon_r's rest origin)
var tiles := {}    # state -> {"play": [img_b, img_a], "side": [...], "note": String}
var face_w := Vector3.ZERO

func _initialize() -> void:
	var wd := Time.get_ticks_msec() + 1200000
	var out_dir: String = OS.get_environment("CLOSE_OUT") if OS.has_environment("CLOSE_OUT") else "/tmp/guard_close"
	DirAccess.make_dir_recursive_absolute(out_dir)
	var acc := {}
	if OS.has_environment("ACCEPT_JSON"):
		acc = JSON.parse_string(FileAccess.get_file_as_string(OS.get_environment("ACCEPT_JSON")))
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
	for k in ks:
		k.set_physics_process(false)
		k.set_gear_stack(k.gear_stack_count() - 1)
		(k._tree as AnimationTree).callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	for i in 4: await process_frame
	var sa: Skeleton3D = ks[1]._skel
	grip_l = sa.get_bone_rest(sa.find_bone("weapon_r")).origin
	face_w = ks[0].canvas_velocity_to_world(ks[0]._canvas_dir_for(FACE)); face_w.y = 0.0; face_w = face_w.normalized()
	for i in 4:
		var sv := SubViewport.new(); sv.size = Vector2i(TILE, TILE)
		sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(sv)
		var c := Camera3D.new(); c.projection = Camera3D.PROJECTION_ORTHOGONAL; c.size = float(OS.get_environment("CLOSE_SIZE")) if OS.has_environment("CLOSE_SIZE") else 0.55; c.near = 0.05; c.far = 100.0
		sv.add_child(c); c.current = true
		var lb := Label.new(); lb.name = "L"; lb.position = Vector2(4, 4)
		lb.add_theme_font_size_override("font_size", 13); lb.add_theme_color_override("font_color", Color(1, 1, 1))
		var sb := StyleBoxFlat.new(); sb.bg_color = Color(0, 0, 0, 0.65)
		sb.content_margin_left = 4; sb.content_margin_right = 4; sb.content_margin_top = 2; sb.content_margin_bottom = 2
		lb.add_theme_stylebox_override("normal", sb)
		sv.add_child(lb)
		svs.append(sv); cams.append(c)
	for st in ["idle", "walk", "run", "block", "strafe_l", "strafe_r"]:
		if Time.get_ticks_msec() > wd: print("[close] WATCHDOG"); quit(4); return
		await _state(st)
	for k in ks:
		(k._tree as AnimationTree).active = false
		var ap: AnimationPlayer = k._anim
		ap.active = true
		ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	# the strikes: each knight's OWN clip for the role (the chop was re-sourced), at its own strike
	# frame from its acceptance table (ACCEPT_JSON after, ACCEPT_JSON_BEFORE before)
	var accb := {}
	if OS.has_environment("ACCEPT_JSON_BEFORE"):
		accb = JSON.parse_string(FileAccess.get_file_as_string(OS.get_environment("ACCEPT_JSON_BEFORE")))
	for role in ["attack", "chop"]:
		var notes := []
		for i in 2:
			var kk = ks[i]
			var clip := String(kk._roles.get(role, ""))
			var tab: Dictionary = acc if i == 1 else accb
			var t: float = 0.5
			if tab.has("clips") and (tab["clips"] as Dictionary).has(clip):
				t = float(tab["clips"][clip]["edge_lead"]["strike_t"])
			var ap: AnimationPlayer = kk._anim
			ap.play(clip); ap.seek(t, true, true)
			notes.append("%s at its strike frame %.3f s" % [clip, t])
		await _shoot("slash" if role == "attack" else "chop", notes[1])
	for view in ["play", "side"]:
		var sheet := Image.create(TILE * 4, TILE * 4, false, Image.FORMAT_RGB8)
		var order := ["idle", "walk", "run", "block", "strafe_l", "strafe_r", "slash", "chop"]
		for j in order.size():
			if not tiles.has(order[j]): continue
			var col: int = j % 4; var row0: int = (j / 4) * 2
			for w in 2:
				sheet.blit_rect(tiles[order[j]][view][w] as Image, Rect2i(0, 0, TILE, TILE), Vector2i(col * TILE, (row0 + w) * TILE))
		sheet.save_jpg("%s/closeup_%s.jpg" % [out_dir, view], 0.92)
	var notes := {}
	for st in tiles: notes[st] = tiles[st]["note"]
	var f := FileAccess.open("%s/closeups.json" % out_dir, FileAccess.WRITE)
	f.store_string(JSON.stringify(notes, " ")); f.close()
	print("[close] sheets -> %s: %s" % [out_dir, JSON.stringify(notes)])
	quit(0)

func _step(dir: Vector2, run: bool) -> void:
	for k in ks:
		k.drive_dir(dir, run, DT)
		(k._tree as AnimationTree).advance(DT)

func _turn() -> float:
	var s: Skeleton3D = ks[1]._skel
	var wb := s.find_bone("weapon_r")
	var loc: Basis = s.get_bone_pose(wb).basis.orthonormalized()
	return rad_to_deg((loc * Vector3.UP).angle_to(s.get_bone_rest(wb).basis.orthonormalized() * Vector3.UP))

func _strafe_input(k, side: String) -> Vector2:
	var sd: Vector3 = k._strafe_dir(side)
	var want: Vector3 = (Basis(Vector3.UP, float(k.get("_yaw_cur"))) * sd).normalized()
	var best := -2.0; var pick := Vector2.ZERO
	for a in 720:
		var dd := Vector2(cos(deg_to_rad(0.5 * a)), sin(deg_to_rad(0.5 * a)))
		var w3: Vector3 = k.canvas_velocity_to_world(dd); w3.y = 0.0
		if w3.length() < 1e-6: continue
		var c: float = w3.normalized().dot(want)
		if c > best: best = c; pick = dd
	return pick

func _state(st: String) -> void:
	for k in ks:
		k.set_block(false)
		k.facing = FACE
	for i in 48: _step(Vector2.ZERO, false)
	for i in 2:
		ks[i].global_position = face_w * (60.0 * float(i) - 30.0) + Vector3(0, 0.03, 0)
		ks[i].velocity = Vector3.ZERO
	var dir := Vector2.ZERO; var run := false; var n := 96
	match st:
		"walk", "run":
			run = st == "run"; dir = ks[0]._canvas_dir_for(FACE)
			for i in 48: _step(dir, run)
			n = int(round(float(ks[1].get("_cycle_len")) / DT))
		"block":
			for k in ks: k.set_block(true)
			for i in 36: _step(Vector2.ZERO, false)
			n = 24
		"strafe_l", "strafe_r":
			for k in ks: k.set_block(true)
			for i in 24: _step(Vector2.ZERO, false)
			dir = _strafe_input(ks[1], "l" if st == "strafe_l" else "r")
			for i in 36: _step(dir, false)
			n = int(round(2.4583 / DT))
	var best := -1.0
	for i in n:
		_step(dir, run)
		var tr := _turn()
		if tr > best + 0.05:
			best = tr
			await _shoot(st, "worst fist turn %.1f deg (frame %d of %d)" % [tr, i, n])
	for k in ks: k.set_block(false)

func _shoot(st: String, note: String) -> void:
	for i in 2:
		var k = ks[i]
		var s: Skeleton3D = k._skel
		var hb := s.find_bone("RightHand")
		var tgt: Vector3 = s.global_transform * (s.get_bone_global_pose(hb) * grip_l)
		var his_right: Vector3 = s.global_transform.basis * Vector3(-1, 0, 0)
		his_right.y = 0.0; his_right = his_right.normalized()
		(cams[i] as Camera3D).look_at_from_position(tgt - FWD * 20.0, tgt, UP)
		(cams[2 + i] as Camera3D).look_at_from_position(tgt + his_right * 20.0, tgt, Vector3.UP)
	for i in 4:
		((svs[i] as SubViewport).get_node("L") as Label).text = "%s  %s\n%s\n%s" % [
			"BEFORE" if i % 2 == 0 else "AFTER", st.to_upper(),
			"installed: the axe rigid in the hand" if i % 2 == 0 else note,
			"along the play camera" if i < 2 else "level, from his right"]
	await process_frame
	await RenderingServer.frame_post_draw
	var imgs := []
	for i in 4:
		var im: Image = (svs[i] as SubViewport).get_texture().get_image()
		im.convert(Image.FORMAT_RGB8)
		imgs.append(im)
	tiles[st] = {"play": [imgs[0], imgs[1]], "side": [imgs[2], imgs[3]], "note": note}
