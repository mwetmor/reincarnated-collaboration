extends Node3D
## R-C9-105 (barbarian copy of the R-C9-98 copy; a film step may set "loop": true, e.g. the whirlwind)
## R-C9-98 COPY (gear_sets/sorceress_battlemage/film_rt; so_d7/film_rt read-only): env GS_CHAR names the character json
## (default character_sorceress.json), GS_BODY the body GLB (default GS_EXP/so-body.glb); every mesh carrying a morph_rules
## key gets it (the gauntlets carry grip_R/grip_L too); wand and grimoire are GREEN in the ID pass, as the staff was.
## FILM MODE (R-C9-98, env GS_FILM=<out.mp4>, GS_FILM_SCALE 1|2, GS_FILM_STACK index): the stack dressed, a plan of clips
## (idle/walk/run at the manifest's foot-lock speeds, the casts in place) played at exactly 1/30 s per frame into the
## offscreen SubViewport and piped RAW to ffmpeg (D7 pass 2's capture: no Movie Maker, no window rescale).
## HER GEAR STACKS, CHECKED AT THE PLAY CAMERA (the conductor, 2026-09-30: Matt's R-C9-69 test -- "a character we can make
## with less clothes/gear on and then test the modular armor/gear additions"). One run renders every stack of her scene
## package (so_d7/scene_pkg/character_sorceress.json gear_stacks), each as knight.gd would dress her:
##   pieces   the stack's pieces shown, the rest hidden -- all six bound once, gear.gd's way (each skinned MeshInstance3D
##            reparented under the body's Skeleton3D, its own skin kept: placed by its own inverse bind matrices)
##   morphs   morph_rules: grip_R = 1 only when its piece (the staff) is in the stack
##   layers   ARMED stacks only (every armed_when_pieces piece shown): the staff carry over idle/walk/run, the package's
##            arm_layer_armed_R -- a filtered Blend2 at weight 1 over its nine bones, the filter taken from EVERY clip so a
##            bone the carry keeps at rest (dropped by the importer) blends to rest, as the package's upper_armed makes it.
##            Unarmed stacks: no layer, the raw clip
## Two passes per shot, named for scripts/s11_count.py (<tag>_<clip>_h<heading>_s<scale>_<mode>.png):
##   beauty   lit as her pass-2 stills (the Barrow's winter sun, ambient 0.30, a grey ground)
##   id       UNSHADED flat colour by what a mesh is -- body RED, garments BLUE, staff and circlet GREEN -- so a body pixel
##            enclosed by garment pixels is the body seen THROUGH a garment, and no texture or light can move that count
## PLAY CAMERA: orthographic, pitch 52.9535 deg, yaw 47 deg, 100.617 px/m x scale, the target 0.85 m over her origin;
## a 1920x1080 offscreen SubViewport (exact rows).
##   class    (with env GS_CLASS_TEX) the body UNSHADED with a CLASS texture -- white where a projection camera PAINTED the
##            texel, yellow where the bake FILLED it from its nearest painted texel, magenta where it is BARE -- and every
##            piece flat black, so each visible body pixel says what paint it shows
## env GS_PKG = scene_pkg dir, GS_EXP = so_d7/export dir, GS_OUT = output dir, GS_CFG = shots json
##   {"shots": [[clip, t], ...], "headings": [...], "scales": [...], "watchdog_s": n}
const PPM := 100.617553710938
const PL_PITCH_DEG := 52.95354112560294
const PL_YAW_DEG := 47.0
const STANDOFF := 60.0

var cfg: Dictionary
var ch: Dictionary
var who: Node3D
var skel: Skeleton3D
var ap: AnimationPlayer
var tree: AnimationTree
var body: MeshInstance3D
var sv: SubViewport
var cam: Camera3D
var ground: MeshInstance3D
var sun: DirectionalLight3D
var we: WorldEnvironment
var piece_of := {}            # MeshInstance3D -> piece name ("" = the body)
var orig := {}
var class_tex: ImageTexture = null

func _load_glb(path: String) -> Node3D:
	var doc := GLTFDocument.new(); var st := GLTFState.new()
	var err := doc.append_from_file(path, st)
	assert(err == OK, "glTF load failed: " + path)
	return doc.generate_scene(st)

func _bind(path: String, piece: String) -> void:
	var src := _load_glb(path)
	for m in src.find_children("*", "MeshInstance3D", true, false):
		var mi := m as MeshInstance3D
		if mi.mesh == null or mi.skin == null:
			continue
		var local := mi.transform; var skin := mi.skin
		mi.owner = null; mi.get_parent().remove_child(mi)
		skel.add_child(mi)
		mi.transform = local; mi.skin = skin; mi.skeleton = NodePath("..")
		piece_of[mi] = piece
	src.queue_free()

func _ready() -> void:
	cfg = JSON.parse_string(FileAccess.get_file_as_string(OS.get_environment("GS_CFG")))
	var cj := OS.get_environment("GS_CHAR") if OS.has_environment("GS_CHAR") else "character_sorceress.json"
	ch = JSON.parse_string(FileAccess.get_file_as_string(OS.get_environment("GS_PKG") + "/" + cj))
	get_tree().create_timer(float(cfg.get("watchdog_s", 600.0))).timeout.connect(func(): push_error("GS WATCHDOG"); get_tree().quit(3))
	var rig := Node3D.new(); rig.rotation_degrees.y = PL_YAW_DEG; add_child(rig)
	sun = DirectionalLight3D.new()
	var e := deg_to_rad(55.0); var a := deg_to_rad(305.0)
	var d := Vector3(-sin(a) * cos(e), -sin(e), -cos(a) * cos(e)).normalized()
	sun.look_at_from_position(Vector3(0, 30, 0), Vector3(0, 30, 0) + d, Vector3.UP)
	sun.light_color = Color(1.0, 0.955, 0.885); sun.light_energy = 0.90
	sun.shadow_enabled = true; sun.shadow_blur = 1.7; sun.directional_shadow_max_distance = STANDOFF + 50.0
	rig.add_child(sun)
	var env := Environment.new(); env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.86, 0.88, 0.90)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(1, 1, 1); env.ambient_light_energy = 0.30
	we = WorldEnvironment.new(); we.environment = env; add_child(we)
	ground = MeshInstance3D.new(); var pm := PlaneMesh.new(); pm.size = Vector2(80, 80); ground.mesh = pm
	var sm := StandardMaterial3D.new(); sm.albedo_color = Color(0.80, 0.80, 0.82); sm.roughness = 0.95
	ground.material_override = sm; add_child(ground)
	var exp := OS.get_environment("GS_EXP")
	who = _load_glb(OS.get_environment("GS_BODY") if OS.has_environment("GS_BODY") else exp + "/so-body.glb"); add_child(who)
	skel = who.find_children("*", "Skeleton3D", true, false)[0]
	ap = who.find_children("*", "AnimationPlayer", true, false)[0]
	for mi in who.find_children("*", "MeshInstance3D", true, false):
		piece_of[mi] = ""
		if (mi as MeshInstance3D).find_blend_shape_by_name("grip_R") >= 0:
			body = mi
	var all_pieces := {}
	for st in ch["gear_stacks"]:
		for p in st: all_pieces[String(p)] = true
	for p in all_pieces:
		_bind("%s/%s.glb" % [exp, p], String(p))
	for mi in piece_of:
		orig[mi] = (mi as MeshInstance3D).material_override
	if OS.has_environment("GS_CLASS_TEX"):
		class_tex = ImageTexture.create_from_image(Image.load_from_file(OS.get_environment("GS_CLASS_TEX")))
	_build_tree()
	cam = Camera3D.new(); cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT; cam.near = 0.05; cam.far = STANDOFF + 300.0
	sv = SubViewport.new(); sv.size = Vector2i(1920, 1080); sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	add_child(sv); sv.add_child(cam); cam.current = true
	if OS.has_environment("GS_FILM"):
		await _film()
	else:
		await _shoot()
	get_tree().quit()

func _build_tree() -> void:
	# the clip, then ONE filtered Blend2 for the carry (the package's arm_layer_armed_R), its weight set per stack
	for n in ap.get_animation_list():
		ap.get_animation(n).loop_mode = Animation.LOOP_NONE
	ap.stop()
	tree = AnimationTree.new(); ap.get_parent().add_child(tree)
	tree.anim_player = tree.get_path_to(ap)
	var bt := AnimationNodeBlendTree.new()
	var a_clip := AnimationNodeAnimation.new(); a_clip.animation = "idle"
	var seek := AnimationNodeTimeSeek.new()
	bt.add_node("clip", a_clip); bt.add_node("seek", seek); bt.connect_node("seek", 0, "clip")
	var ly: Dictionary = ch["arm_layer_armed_R"]
	var an := AnimationNodeAnimation.new(); an.animation = String(ly["action"])
	var b2 := AnimationNodeBlend2.new(); b2.filter_enabled = true
	var nf := 0; var seen := {}
	for n2 in ap.get_animation_list():
		var a2: Animation = ap.get_animation(n2)
		for i in a2.get_track_count():
			var pth: NodePath = a2.track_get_path(i)
			if String(pth.get_concatenated_subnames()) in ly["bones"] and not seen.has(String(pth)):
				seen[String(pth)] = true; b2.set_filter_path(pth, true); nf += 1
	bt.add_node("carry", an); bt.add_node("L", b2)
	bt.connect_node("L", 0, "seek"); bt.connect_node("L", 1, "carry")
	bt.connect_node("output", 0, "L")
	tree.tree_root = bt
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	tree.active = true
	print("[gs] carry layer: %s, %d tracks filtered over %d bones (from every clip)" % [ly["action"], nf, ly["bones"].size()])

func _armed(on: Array) -> bool:
	var need: Array = ch.get("armed_when_pieces", [])
	if need.is_empty(): return false
	for p in need:
		if not (String(p) in on): return false
	return true

func _dress(on: Array) -> void:
	for mi in piece_of:
		var p := String(piece_of[mi])
		(mi as MeshInstance3D).visible = (p == "") or (p in on)
	for morph in (ch.get("morph_rules", {}) as Dictionary):
		for mi2 in piece_of:
			var i := (mi2 as MeshInstance3D).find_blend_shape_by_name(String(morph))
			if i >= 0:
				(mi2 as MeshInstance3D).set_blend_shape_value(i, 1.0 if String(ch["morph_rules"][morph]) in on else 0.0)

func _kind(mi: MeshInstance3D) -> Color:
	var p := String(piece_of[mi])
	if p == "": return Color(1, 0, 0)
	if p in ["staff", "circlet", "wand", "grimoire"]: return Color(0, 1, 0)
	return Color(0, 0, 1)

func _set_mode(mode: String) -> void:
	var flat := mode != "beauty"
	ground.visible = not flat; sun.visible = not flat
	we.environment.background_color = {"beauty": Color(0.86, 0.88, 0.90), "id": Color(0, 0, 0), "class": Color(0.5, 0.5, 0.5)}[mode]
	for mi in orig:
		if flat:
			var m := StandardMaterial3D.new(); m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
			if mode == "id":
				m.albedo_color = _kind(mi)
			elif String(piece_of[mi]) == "":
				m.albedo_texture = class_tex; m.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
			else:
				m.albedo_color = Color(0, 0, 0)
			(mi as MeshInstance3D).material_override = m
		else:
			(mi as MeshInstance3D).material_override = orig[mi]

func _aim(scale: float) -> void:
	cam.size = (float(sv.size.y) / PPM) / scale
	var p := deg_to_rad(PL_PITCH_DEG); var y := deg_to_rad(PL_YAW_DEG)
	var f := Vector3(-sin(y) * cos(p), -sin(p), -cos(y) * cos(p)).normalized()
	var at := who.global_position + Vector3(0, 0.85, 0)
	cam.look_at_from_position(at - f * STANDOFF, at, Vector3.UP)

func _pose(clip: String, t: float, armed: bool) -> void:
	((tree.tree_root as AnimationNodeBlendTree).get_node("clip") as AnimationNodeAnimation).animation = clip
	tree.set("parameters/seek/seek_request", t)
	var layered: bool = armed and clip in ["idle", "walk", "run"]
	tree.set("parameters/L/blend_amount", float(ch["arm_layer_armed_R"].get("weight", 1.0)) if layered else 0.0)
	tree.advance(0.0)

func _shoot() -> void:
	var out := OS.get_environment("GS_OUT")
	var stacks: Array = ch["gear_stacks"]
	var rep := {"stacks": []}
	for si in stacks.size():
		var on: Array = stacks[si]
		var armed := _armed(on)
		_dress(on)
		rep["stacks"].append({"index": si, "name": String((ch.get("gear_stack_names", []) as Array)[si]) if si < (ch.get("gear_stack_names", []) as Array).size() else "",
							  "pieces": on, "armed": armed, "grip_R": body.get_blend_shape_value(body.find_blend_shape_by_name("grip_R")),
							  "carry_layer": armed})
		for shot in cfg["shots"]:
			var clip := String(shot[0]); var t := float(shot[1])
			for hd in cfg["headings"]:
				who.rotation_degrees.y = float(hd)
				_pose(clip, t, armed)
				for sc in cfg["scales"]:
					_aim(float(sc))
					for mode in (["beauty", "id", "class"] if class_tex != null else ["beauty", "id"]):
						_set_mode(mode)
						for i in int(cfg.get("settle_frames", 4)): await RenderingServer.frame_post_draw
						var img := sv.get_texture().get_image()
						img.save_png("%s/stack%d_%s_h%d_s%d_%s.png" % [out, si, clip, int(hd), int(sc), mode])
		print("[gs] stack %d %s: pieces %s, armed %s, grip_R %.0f" % [si, rep["stacks"][si]["name"], str(on), str(armed), rep["stacks"][si]["grip_R"]])
	var f := FileAccess.open(out + "/gear_stills_report.json", FileAccess.WRITE); f.store_string(JSON.stringify(rep, " ")); f.close()


func _film() -> void:
	var out := OS.get_environment("GS_FILM")
	var sc := float(OS.get_environment("GS_FILM_SCALE")) if OS.has_environment("GS_FILM_SCALE") else 1.0
	var si := int(OS.get_environment("GS_FILM_STACK")) if OS.has_environment("GS_FILM_STACK") else (ch["gear_stacks"] as Array).size() - 1
	var W := int(960 * sc); var H := int(540 * sc)
	sv.size = Vector2i(W, H)
	var on: Array = ch["gear_stacks"][si]
	var armed := _armed(on)
	_dress(on); _set_mode("beauty")
	var plan: Array = cfg["film_plan"]
	var args := PackedStringArray(["-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", "%dx%d" % [W, H], "-r", "30",
		"-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", out])
	var pipe := OS.execute_with_pipe("/opt/homebrew/bin/ffmpeg", args, true)
	var io: FileAccess = pipe["stdio"]
	var pos := Vector3.ZERO
	var nframes := 0
	for step in plan:
		var clip := String(step["clip"]); var secs := float(step["seconds"]); var spd := float(step.get("speed", 0.0))
		var hd := float(step["heading_deg"])
		who.rotation_degrees.y = hd
		var fwd := Vector3(sin(deg_to_rad(hd)), 0, cos(deg_to_rad(hd)))       # her forward is +Z (character.json forward_axis)
		var alen := ap.get_animation(clip).length
		var n := int(round(secs * 30.0))
		for f in n:
			var t := f / 30.0
			var tc: float = fmod(t, alen) if (clip in ["idle", "walk", "run"] or bool(step.get("loop", false))) else minf(t, alen)
			who.position = pos + fwd * spd * t
			_pose(clip, tc, armed)
			_aim(sc / sc)
			cam.size = (float(H) / PPM) / sc
			for i in 2: await RenderingServer.frame_post_draw
			var img := sv.get_texture().get_image()
			img.convert(Image.FORMAT_RGBA8)
			io.store_buffer(img.get_data())
			nframes += 1
		pos = pos + fwd * spd * secs
	io.close()
	OS.delay_msec(1500)
	print("[gs] film %s: %d frames, %dx%d, stack %d, armed %s" % [out, nframes, W, H, si, str(armed)])
