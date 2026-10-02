extends Node3D
## EN-E2 (drax, R-C9-132): copy of wl_e1's, plus baked-flipbook VFX in film mode (GS_VFX). E1 (drax, wl_e1): copy for the dark knight -- the arm layer is OPTIONAL (no arm_layer_armed_R key = raw clips), the body
## grip morph optional, and the ground wears the Barrow's SNOW tint (barrow_full_layout tints_srgb.snow 0.86/0.84/0.80).
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
var piece_of := {}
var added_bones: Array = []
var sim: SpringBoneSimulator3D = null
var cape_dump: Array = []
var sim_us: Array = []            # MeshInstance3D -> piece name ("" = the body)
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
		# E1 stage K: bind by bone NAME (Godot's glTF skeleton bone order follows each FILE's node order, which differs
		# between a Meshy-built body and a Blender-exported piece -- rig 3's order put every piece on the wrong bones).
		if OS.has_environment("GS_BIND_BY_NAME"):
			var ps := mi.get_node_or_null(mi.skeleton) as Skeleton3D
			if ps != null:
				# E1 R-C9-128: a piece may carry EXTRA bones (the cape chain, cape_*): add them to the body skeleton first, by name,
				# parented by name, with the piece's own rest -- then the name bind below finds them
				for pi in ps.get_bone_count():
					var bn := ps.get_bone_name(pi)
					if skel.find_bone(bn) < 0:
						var ni := skel.add_bone(bn); var pp := ps.get_bone_parent(pi)
						if pp >= 0: skel.set_bone_parent(ni, skel.find_bone(ps.get_bone_name(pp)))
						skel.set_bone_rest(ni, ps.get_bone_rest(pi)); skel.reset_bone_pose(ni)
						added_bones.append(bn)
				skin = skin.duplicate()
				for bi in skin.get_bind_count():
					var bb := skin.get_bind_bone(bi)
					if bb >= 0:
						skin.set_bind_name(bi, ps.get_bone_name(bb))
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
	var sm := StandardMaterial3D.new(); sm.albedo_color = Color(0.86, 0.84, 0.80); sm.roughness = 0.95
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
	if OS.has_environment("GS_CAPE_SIM"):
		_cape_sim(OS.get_environment("GS_CAPE_SIM"))
	if OS.has_environment("GS_EYES"):
		await _eyes(OS.get_environment("GS_EYES"))
	cam = Camera3D.new(); cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT; cam.near = 0.05; cam.far = STANDOFF + 300.0
	sv = SubViewport.new(); sv.size = Vector2i(1920, 1080); sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	add_child(sv); sv.add_child(cam); cam.current = true
	_vfx_load()
	if OS.has_environment("GS_FILM"):
		await _film()
	else:
		await _shoot()
	get_tree().quit()

## E1 EYE SPRITES (stage J): two camera-facing glow quads on the 'Head' bone (GS_EYES = e44's json): billboard, UNSHADED, ADDITIVE,
## depth-tested (the helm hides them from behind); a radial texture with a hot near-white core; a slow subtle flicker in film mode
## (GS_EYES_FLICKER = "hz,amp"). The world size is set against the ancestors' scale, so 'size_m' is metres on screen at 100.6 px/m.
var eye_mats: Array = []
func _eyes(path: String) -> void:
	var E: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(path))
	var col := Color(OS.get_environment("GS_EYES_COLOR")) if OS.has_environment("GS_EYES_COLOR") else Color(0.62, 0.30, 1.0)
	var img := Image.create(64, 64, false, Image.FORMAT_RGBA8)
	for y in 64:
		for x in 64:
			var r := Vector2(x - 31.5, y - 31.5).length() / 31.5
			var a := clampf(1.0 - r, 0.0, 1.0); a = sqrt(a)   # v2: a flatter falloff (v1 a^2 left 1-3 px visible at 1x)
			var core := clampf(1.0 - r / 0.5, 0.0, 1.0)
			var c := col.lerp(Color(1, 0.97, 1), core)
			img.set_pixel(x, y, Color(c.r * a, c.g * a, c.b * a, a))
	var tex := ImageTexture.create_from_image(img)
	var att := BoneAttachment3D.new(); att.bone_name = String(E.get("bone", "Head")); skel.add_child(att)
	for k in (E["eyes"] as Dictionary):
		var p: Array = E["eyes"][k]["head_local"]
		var n := Node3D.new(); n.position = Vector3(float(p[0]), float(p[1]), float(p[2])); att.add_child(n)
		var q := MeshInstance3D.new(); var qm := QuadMesh.new(); n.add_child(q)
		var m := StandardMaterial3D.new(); m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		m.blend_mode = BaseMaterial3D.BLEND_MODE_ADD; m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		m.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED; m.billboard_keep_scale = true; m.albedo_texture = tex
		q.material_override = m; q.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF; eye_mats.append(m)
		await get_tree().process_frame
		var sc := n.global_transform.basis.get_scale().x
		qm.size = Vector2.ONE * float(E.get("sprite_size_m", 0.05)) / maxf(sc, 1e-6); q.mesh = qm
	print("[gs] eye sprites: %d on %s, %.3f m, colour %s" % [eye_mats.size(), String(E.get("bone", "Head")), float(E.get("sprite_size_m", 0.05)), col.to_html()])

func _eye_flicker(t: float) -> void:
	if eye_mats.is_empty() or not OS.has_environment("GS_EYES_FLICKER"): return
	var f := OS.get_environment("GS_EYES_FLICKER").split(",")
	var v := 1.0 - float(f[1]) * (0.5 + 0.5 * sin(TAU * float(f[0]) * t)) - 0.04 * sin(TAU * 3.7 * t + 1.3)
	for m in eye_mats: (m as StandardMaterial3D).albedo_color = Color(v, v, v, 1.0)

## E1 R-C9-128 CAPE SECONDARY MOTION: a SpringBoneSimulator3D on the body skeleton, one setting per cape column (root cape_X_0 ..
## end cape_X_3, the end extended by its own length), body CAPSULE collisions (GS_CAPE_SIM = json: settings + capsules, radii in
## metres, converted to skeleton units by the skeleton's world scale). GS_CAPE_DUMP = out json: every film frame's cape-bone and
## Hips poses in skeleton space (the measuring side skins the cape with them). GS_CAPE_SIM_OFF=1 builds it inactive (rigid chain).
func _cape_sim(path: String) -> void:
	var cfg2: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(path))
	var u := 1.0 / skel.global_transform.basis.get_scale().x
	sim = SpringBoneSimulator3D.new(); skel.add_child(sim)
	var S: Array = cfg2["settings"]; sim.setting_count = S.size()
	for i in S.size():
		var st: Dictionary = S[i]
		sim.set_root_bone_name(i, st["root"]); sim.set_end_bone_name(i, st["end"]); sim.set_extend_end_bone(i, true)
		var eb := skel.find_bone(st["end"]); var lenu := (skel.get_bone_rest(eb).origin).length()
		sim.set_end_bone_length(i, lenu)
		sim.set_stiffness(i, float(st.get("stiffness", 1.0)) * (u if OS.has_environment("GS_CAPE_SCALE_STIFF") else 1.0)); sim.set_drag(i, float(st.get("drag", 0.4)))
		sim.set_gravity(i, float(st.get("gravity", 0.0)) * u); sim.set_gravity_direction(i, Vector3.DOWN)
		sim.set_radius(i, float(st.get("radius_m", 0.02)) * u); sim.set_enable_all_child_collisions(i, true)
	for c in (cfg2.get("capsules", []) as Array):
		var cap := SpringBoneCollisionCapsule3D.new(); sim.add_child(cap)
		cap.bone_name = c["bone"]; var bi := skel.find_bone(c["bone"])
		var ch := skel.find_bone(c.get("to", "")) if c.has("to") else -1
		var L := (skel.get_bone_rest(ch).origin.length() if ch >= 0 else float(c.get("length_m", 0.2)) * u)
		cap.radius = float(c["radius_m"]) * u; cap.height = L + 2.0 * cap.radius
		cap.position_offset = Vector3(0, L * 0.5, 0) + Vector3(float(c.get("dx_m", 0.0)), float(c.get("dy_m", 0.0)), float(c.get("dz_m", 0.0))) * u
	sim.active = not OS.has_environment("GS_CAPE_SIM_OFF")
	skel.skeleton_updated.connect(_on_skel_updated)
	# DETERMINISTIC STEPPING: the film advances the skeleton's modifiers by exactly 1/30 s per output frame (MANUAL), so the cloth
	# sees play-speed time however fast the offscreen renderer runs
	if not OS.has_environment("GS_CAPE_IDLE"): skel.modifier_callback_mode_process = Skeleton3D.MODIFIER_CALLBACK_MODE_PROCESS_MANUAL
	for i in S.size(): print("[gs]   setting %d: joints %d, root %s end %s" % [i, sim.get_joint_count(i), sim.get_root_bone_name(i), sim.get_end_bone_name(i)])
	print("[gs] cape sim: %d settings, %d capsules, active %s, added bones %d, skeleton unit %.4f m" % [S.size(), (cfg2.get("capsules", []) as Array).size(), str(sim.active), added_bones.size(), 1.0 / u])

var cape_last := {}
var cur_clip := ""
var cur_tc := 0.0
var upd_count := 0
func _on_skel_updated() -> void:
	# the MODIFIED poses only exist inside this signal (the skeleton restores the animated poses after skinning)
	upd_count += 1
	for bn in added_bones + ["Hips", "Spine"]:
		cape_last[bn] = skel.get_bone_global_pose(skel.find_bone(bn))

func _cape_record(t: float) -> void:
	if not OS.has_environment("GS_CAPE_DUMP"): return
	var fr := {"t": t, "clip": cur_clip, "tc": cur_tc, "bones": {}, "updates": upd_count}
	for bn in added_bones + ["Hips", "Spine"]:
		var tr: Transform3D = cape_last.get(bn, skel.get_bone_global_pose(skel.find_bone(bn)))
		fr["bones"][bn] = [tr.basis.x.x, tr.basis.x.y, tr.basis.x.z, tr.basis.y.x, tr.basis.y.y, tr.basis.y.z, tr.basis.z.x, tr.basis.z.y, tr.basis.z.z, tr.origin.x, tr.origin.y, tr.origin.z]
	cape_dump.append(fr)

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
	if not ch.has("arm_layer_armed_R"):
		bt.connect_node("output", 0, "seek"); tree.tree_root = bt
		tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL; tree.active = true
		print("[gs] no carry layer"); return
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
	if p in ["staff", "circlet", "wand", "grimoire", "wl_mace"]: return Color(0, 1, 0)
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
	if ch.has("arm_layer_armed_R"):
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
							  "pieces": on, "armed": armed, "grip_R": body.get_blend_shape_value(body.find_blend_shape_by_name("grip_R")) if body != null else -1.0,
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
						# E1: with more than one shot, the clip time goes in the name (one shot keeps the old name)
						if (cfg["shots"] as Array).size() == 1:
							img.save_png("%s/stack%d_%s_h%d_s%d_%s.png" % [out, si, clip, int(hd), int(sc), mode])
						else:
							img.save_png("%s/stack%d_%s@%.2f_h%d_s%d_%s.png" % [out, si, clip, t, int(hd), int(sc), mode])
		print("[gs] stack %d %s: pieces %s, armed %s, grip_R %.0f" % [si, rep["stacks"][si]["name"], str(on), str(armed), rep["stacks"][si]["grip_R"]])
	var f := FileAccess.open(out + "/gear_stills_report.json", FileAccess.WRITE); f.store_string(JSON.stringify(rep, " ")); f.close()


## EN-E2 VFX (R-C9-132): the acolytes' baked flipbooks (scripts/en05_vfx_bake.py) played in FILM mode, the Barrow's discipline:
## one atlas, quads only, nothing built at cast time beyond a small pool. env GS_VFX = <dir>/<id>_frames.json. A film step may carry
## "vfx": "bolt" (cast puff at the hand, the bolt flying from the hand along the facing at "speed" m/s for "range" m, the burst where
## it stops) or "area" (the ring telegraph drawn on the floor "dist" m ahead from the step start, the ring burst + smoke at release),
## "release_s" (the clip's measured release) and "hand" (the release hand bone). Premultiplied blend: out = rgb + dst * (1 - a).
const VFX_SHADER := """
shader_type spatial;
render_mode unshaded, blend_premul_alpha, depth_draw_never, cull_disabled, shadows_disabled;
uniform sampler2D atlas : source_color, filter_linear;
uniform vec4 region;
uniform vec2 size_m;
uniform vec2 center_m;
uniform float rot;
uniform bool billboard;
void vertex() {
	vec2 v = VERTEX.xy * size_m + center_m;
	float c = cos(rot); float s = sin(rot);
	v = vec2(c * v.x - s * v.y, s * v.x + c * v.y);
	VERTEX = vec3(v, 0.0);
	if (billboard) {
		MODELVIEW_MATRIX = VIEW_MATRIX * mat4(INV_VIEW_MATRIX[0], INV_VIEW_MATRIX[1], INV_VIEW_MATRIX[2], MODEL_MATRIX[3]);
	}
}
void fragment() {
	vec4 t = texture(atlas, region.xy + UV * region.zw);
	ALBEDO = t.rgb; ALPHA = t.a;
}
"""
var vfx: Dictionary = {}
var vfx_tex: Texture2D = null
var vfx_live: Array = []

func _vfx_load() -> void:
	if not OS.has_environment("GS_VFX"): return
	var p := OS.get_environment("GS_VFX")
	vfx = JSON.parse_string(FileAccess.get_file_as_string(p))
	vfx_tex = ImageTexture.create_from_image(Image.load_from_file(p.get_base_dir() + "/" + String(vfx["atlas"])))
	print("[gs] vfx %s: %s" % [String(vfx["id"]), str((vfx["phases"] as Dictionary).keys())])

func _vfx_spawn(phase: String, t0: float, pos: Vector3, dir: Vector3 = Vector3.ZERO, vel: float = 0.0, life: float = -1.0) -> void:
	var mi := MeshInstance3D.new(); var q := QuadMesh.new(); q.size = Vector2(1, 1); mi.mesh = q
	var m := ShaderMaterial.new(); var sh := Shader.new(); sh.code = VFX_SHADER; m.shader = sh
	m.set_shader_parameter("atlas", vfx_tex)
	var ground_plane := String(vfx["phases"][phase]["plane"]) == "ground"
	m.set_shader_parameter("billboard", not ground_plane)
	mi.material_override = m; mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	if ground_plane: mi.rotation_degrees.x = -90.0
	add_child(mi); mi.visible = false
	if OS.has_environment("GS_VFX_DEBUG"): print("[gs] vfx spawn %s t0 %.3f at %s plane %s" % [phase, t0, str(pos), str(ground_plane)])
	vfx_live.append({"phase": phase, "t0": t0, "pos": pos, "dir": dir, "vel": vel, "life": life, "mi": mi, "mat": m, "ground": ground_plane})

func _vfx_tick(now: float) -> void:
	var ppm := float(vfx["px_per_m"]); var aw := float(vfx["atlas_size"][0]); var ah := float(vfx["atlas_size"][1])
	for e in vfx_live.duplicate():
		var ph: Dictionary = vfx["phases"][e["phase"]]; var dt: float = now - float(e["t0"])
		var mi: MeshInstance3D = e["mi"]
		if dt < 0.0: mi.visible = false; continue
		var n := int(ph["n"]); var fi := int(floor(dt * float(ph["fps"])))
		if bool(ph["loop"]): fi = fi % n
		var over := (fi >= n and not bool(ph["loop"])) or (float(e["life"]) >= 0.0 and dt > float(e["life"]))
		if over:
			mi.queue_free(); vfx_live.erase(e); continue
		var fr: Dictionary = ph["frames"][fi]
		var pp := float(ph.get("px_per_m", ppm))
		var r: Array = fr["rect"]; var off: Array = fr["offset_px"]
		var p: Vector3 = e["pos"] + (e["dir"] as Vector3) * float(e["vel"]) * dt
		mi.global_position = p + (Vector3(0, 0.02, 0) if bool(e["ground"]) else Vector3.ZERO)
		var m: ShaderMaterial = e["mat"]
		m.set_shader_parameter("region", Vector4(float(r[0]) / aw, float(r[1]) / ah, float(r[2]) / aw, float(r[3]) / ah))
		m.set_shader_parameter("size_m", Vector2(float(r[2]) / pp, float(r[3]) / pp))
		m.set_shader_parameter("center_m", Vector2((float(off[0]) + float(r[2]) / 2.0) / pp, -(float(off[1]) + float(r[3]) / 2.0) / pp))
		var rot := 0.0
		if (e["dir"] as Vector3).length() > 0.0 and e["phase"] == "bolt":
			var a2 := cam.unproject_position(p); var b2 := cam.unproject_position(p + (e["dir"] as Vector3))
			rot = atan2(-(b2.y - a2.y), b2.x - a2.x)
		m.set_shader_parameter("rot", rot)
		mi.visible = true

func _vfx_step(step: Dictionary, t_start: float, pos0: Vector3, fwd: Vector3) -> void:
	if vfx.is_empty() or not step.has("vfx"): return
	var rel := float(step.get("release_s", 0.5))
	var hand := skel.find_bone(String(step.get("hand", "RightHand")))
	if String(step["vfx"]) == "bolt":
		_pose(String(step["clip"]), rel, false)
		var hp: Vector3 = skel.global_transform * skel.get_bone_global_pose(hand).origin
		var spd := float(step.get("speed_vfx", 16.0)); var rng := float(step.get("range", 8.0))
		var start := hp + fwd * 0.15
		_vfx_spawn("cast", t_start + rel - 0.25, hp)
		_vfx_spawn("bolt", t_start + rel, start, fwd, spd, rng / spd)
		_vfx_spawn("burst", t_start + rel + rng / spd, start + fwd * rng)
	elif String(step["vfx"]) == "slash":
		_pose(String(step["clip"]), rel, false)
		var hp2: Vector3 = skel.global_transform * skel.get_bone_global_pose(hand).origin
		_vfx_spawn("slash", t_start + rel - 0.08, hp2 + fwd * 0.25)
	elif String(step["vfx"]) == "aura":
		var lp := float(step["seconds"]) - rel
		_vfx_spawn("aura", t_start + rel, pos0, Vector3.ZERO, 0.0, lp)
		_vfx_spawn("ring_burst", t_start + rel, pos0)
	else:
		var c := pos0 + fwd * float(step.get("dist", 5.0))
		var tele := float(vfx["phases"]["ring_tele"]["n"]) / float(vfx["phases"]["ring_tele"]["fps"])
		_vfx_spawn("ring_tele", t_start + maxf(0.0, rel - tele), c, Vector3.ZERO, 0.0, tele + (0.0 if rel >= tele else rel))
		_vfx_spawn("ring_burst", t_start + rel, c)
		_vfx_spawn("ring_smoke", t_start + rel + 0.1, c)

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
		var t_start := float(nframes) / 30.0
		who.position = pos
		_vfx_step(step, t_start, pos, fwd)
		for f in n:
			var t := f / 30.0
			var tc: float = fmod(t, alen) if (clip in ["idle", "walk", "run"] or bool(step.get("loop", false))) else minf(t, alen)
			who.position = pos + fwd * spd * t
			_pose(clip, tc, armed)
			_eye_flicker(float(nframes) / 30.0)
			if sim != null:
				var t0 := Time.get_ticks_usec(); skel.advance(1.0 / 30.0); sim_us.append(Time.get_ticks_usec() - t0)
			_aim(sc / sc)
			cam.size = (float(H) / PPM) / sc
			if not vfx.is_empty(): _vfx_tick(float(nframes) / 30.0)
			for i in 2: await RenderingServer.frame_post_draw
			var img := sv.get_texture().get_image()
			img.convert(Image.FORMAT_RGBA8)
			io.store_buffer(img.get_data())
			cur_clip = clip; cur_tc = tc
			_cape_record(float(nframes) / 30.0)
			nframes += 1
		pos = pos + fwd * spd * secs
	io.close()
	if not sim_us.is_empty():
		var tot := 0.0
		for v in sim_us: tot += float(v)
		print("[gs] skeleton.advance (modifiers incl. the cape sim): mean %.1f us over %d frames" % [tot / sim_us.size(), sim_us.size()])
	if OS.has_environment("GS_CAPE_DUMP"):
		var fd := FileAccess.open(OS.get_environment("GS_CAPE_DUMP"), FileAccess.WRITE); fd.store_string(JSON.stringify({"frames": cape_dump, "skel_global": str(skel.global_transform)})); fd.close()
	OS.delay_msec(1500)
	print("[gs] film %s: %d frames, %dx%d, stack %d, armed %s" % [out, nframes, W, H, si, str(armed)])
