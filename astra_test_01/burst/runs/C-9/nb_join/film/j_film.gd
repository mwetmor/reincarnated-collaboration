extends Node3D
## nb_join: the barbarian's JOIN moves at the PLAY camera -- 8-heading stills and a 2x film. A sandbox project:
## nothing here is imported or installed (runtime glTF, like join1_render), so it costs no import cache on disk.
##
## BINDING is gear.gd's, reproduced: every piece's skinned MeshInstance3D reparented under the body's Skeleton3D,
## its own skin kept -- each piece is placed by ITS OWN inverse bind matrices on the body's joints (the glTF rule).
## LAYERS are the format agreed with the scene drax (2026-09-30): a list, bottom to top, each
##   {name, action, bones, weight, states, time}  -- a filtered Blend2 over the state's clip, its own animation
## node behind its own TimeSeek: time "pose" = the action at 0, "clip" = the base clip's time. Filter paths are
## taken from the action's own tracks. An un-keyed channel is at REST (Godot's tree, the glTF rule).
## CAMERA: the play camera -- orthographic, pitch 52.9535 deg, yaw 47 deg, 100.617 px/m x scale, looking at the
## ground origin + 0.85 m. Rendered into an OFFSCREEN SubViewport of exactly the size asked; films piped raw to
## ffmpeg at exactly 1/30 s per frame (no Movie Maker, no frames on disk).
## env J_CFG = the config json (absolute path).

const PPM := 100.617553710938
const PL_PITCH_DEG := 52.95354112560294
const PL_YAW_DEG := 47.0
const STANDOFF := 60.0

var cfg: Dictionary
var who: Node3D
var skel: Skeleton3D
var ap: AnimationPlayer
var tree: AnimationTree
var body: MeshInstance3D
var sv: SubViewport
var cam: Camera3D
var layers: Array = []

func _load_glb(path: String) -> Node3D:
	var doc := GLTFDocument.new(); var st := GLTFState.new()
	var err := doc.append_from_file(path, st)
	assert(err == OK, "glTF load failed: " + path)
	return doc.generate_scene(st)

func _bind(path: String) -> void:
	var src := _load_glb(path)
	for m in src.find_children("*", "MeshInstance3D", true, false):
		var mi := m as MeshInstance3D
		if mi.mesh == null or mi.skin == null:
			continue
		var local := mi.transform; var skin := mi.skin
		mi.owner = null; mi.get_parent().remove_child(mi)
		skel.add_child(mi)
		mi.transform = local; mi.skin = skin; mi.skeleton = NodePath("..")
	src.queue_free()

func winter_sun() -> DirectionalLight3D:
	var l := DirectionalLight3D.new()
	var e := deg_to_rad(55.0); var a := deg_to_rad(305.0)
	var d := Vector3(-sin(a) * cos(e), -sin(e), -cos(a) * cos(e)).normalized()
	l.look_at_from_position(Vector3(0, 30, 0), Vector3(0, 30, 0) + d, Vector3.UP)
	l.light_color = Color(1.0, 0.955, 0.885); l.light_energy = 0.90
	l.shadow_enabled = true; l.shadow_blur = 1.7
	l.directional_shadow_max_distance = STANDOFF + 50.0
	return l

func _ready() -> void:
	cfg = JSON.parse_string(FileAccess.get_file_as_string(OS.get_environment("J_CFG")))
	get_tree().create_timer(float(cfg.get("watchdog_s", 900.0))).timeout.connect(func(): push_error("J WATCHDOG"); get_tree().quit(3))
	var rig := Node3D.new(); rig.rotation_degrees.y = PL_YAW_DEG; add_child(rig); rig.add_child(winter_sun())
	var env := Environment.new(); env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.86, 0.88, 0.90)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(1, 1, 1); env.ambient_light_energy = 0.30
	var we := WorldEnvironment.new(); we.environment = env; add_child(we)
	var g := MeshInstance3D.new(); var pm := PlaneMesh.new(); pm.size = Vector2(80, 80); g.mesh = pm
	var sm := StandardMaterial3D.new(); sm.albedo_color = Color(0.80, 0.80, 0.82); sm.roughness = 0.95
	g.material_override = sm; add_child(g)
	who = _load_glb(String(cfg["body"])); add_child(who)
	skel = who.find_children("*", "Skeleton3D", true, false)[0]
	ap = who.find_children("*", "AnimationPlayer", true, false)[0]
	for p in cfg.get("pieces", []):
		_bind(String(p))
	for mi in who.find_children("*", "MeshInstance3D", true, false):
		if (mi as MeshInstance3D).find_blend_shape_by_name("grip_R") >= 0:
			body = mi
	layers = cfg.get("layers", [])
	_build_tree()
	cam = Camera3D.new(); cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT; cam.near = 0.05; cam.far = STANDOFF + 300.0
	if String(cfg.get("mode", "stills")) == "film":
		await _film()
	else:
		await _stills()
	get_tree().quit()

func _build_tree() -> void:
	for n in ap.get_animation_list():
		ap.get_animation(n).loop_mode = Animation.LOOP_NONE
	ap.stop()
	tree = AnimationTree.new(); ap.get_parent().add_child(tree)
	tree.anim_player = tree.get_path_to(ap)
	var bt := AnimationNodeBlendTree.new()
	var a_clip := AnimationNodeAnimation.new(); a_clip.animation = ap.get_animation_list()[0]
	var seek := AnimationNodeTimeSeek.new()
	bt.add_node("clip", a_clip); bt.add_node("seek", seek); bt.connect_node("seek", 0, "clip")
	var prev := "seek"
	for ly in layers:
		var nm := String(ly["name"])
		var an := AnimationNodeAnimation.new(); an.animation = String(ly["action"])
		var ls := AnimationNodeTimeSeek.new()
		var b2 := AnimationNodeBlend2.new(); b2.filter_enabled = true
		var act := ap.get_animation(String(ly["action"]))
		var nf := 0
		var srcs: Array = [act]                           # filter_from: "action" (agreed default) | "all_clips" (see render_cells.gd)
		if String(ly.get("filter_from", "action")) == "all_clips":
			srcs = []
			for n2 in ap.get_animation_list(): srcs.append(ap.get_animation(n2))
		var seen := {}
		for a2 in srcs:
			for i in (a2 as Animation).get_track_count():
				var pth: NodePath = (a2 as Animation).track_get_path(i)
				if String(pth.get_concatenated_subnames()) in ly["bones"] and not seen.has(String(pth)):
					seen[String(pth)] = true
					b2.set_filter_path(pth, true); nf += 1
		bt.add_node("a_" + nm, an); bt.add_node("s_" + nm, ls); bt.connect_node("s_" + nm, 0, "a_" + nm)
		bt.add_node("L_" + nm, b2)
		bt.connect_node("L_" + nm, 0, prev); bt.connect_node("L_" + nm, 1, "s_" + nm)
		prev = "L_" + nm
		print("[j] layer %s: %s, %d tracks filtered (%d bones, from %s), weight %s, states %s, time %s" % [nm, ly["action"], nf, ly["bones"].size(), ly.get("filter_from", "action"), ly.get("weight", 1.0), ly.get("states", []), ly.get("time", "pose")])
	bt.connect_node("output", 0, prev)
	tree.tree_root = bt
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	tree.active = true

func _pose(clip: String, t: float) -> void:
	((tree.tree_root as AnimationNodeBlendTree).get_node("clip") as AnimationNodeAnimation).animation = clip
	tree.set("parameters/seek/seek_request", t)
	for ly in layers:
		var nm := String(ly["name"])
		var on: bool = clip in ly.get("states", [])
		tree.set("parameters/L_%s/blend_amount" % nm, float(ly.get("weight", 1.0)) if on else 0.0)
		tree.set("parameters/s_%s/seek_request" % nm, t if String(ly.get("time", "pose")) == "clip" else 0.0)
	tree.advance(0.0)
	if body:
		for k in cfg.get("morphs", {}):
			var i := body.find_blend_shape_by_name(k)
			if i >= 0:
				body.set_blend_shape_value(i, float(cfg["morphs"][k]))

func _aim(scale: float, rows: float) -> void:
	cam.size = rows / (PPM * scale)
	var p := deg_to_rad(PL_PITCH_DEG); var y := deg_to_rad(PL_YAW_DEG)
	var f := Vector3(-sin(y) * cos(p), -sin(p), -cos(y) * cos(p)).normalized()
	var at := Vector3(0, float(cfg.get("look_at_y", 0.85)), 0)
	cam.look_at_from_position(at - f * STANDOFF, at, Vector3.UP)

func _stills() -> void:
	## per shot: the 8 headings side by side in ONE labelled sheet (a crop of each), not 8 files
	var st: Dictionary = cfg["stills"]
	var w := int(st.get("w", 560)); var h := int(st.get("h", 640)); var scale := float(st.get("scale", 2.0))
	sv = SubViewport.new(); sv.size = Vector2i(w, h); sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	add_child(sv); sv.add_child(cam); cam.current = true
	_aim(scale, float(h))
	var headings: Array = st.get("headings", [0, 45, 90, 135, 180, 225, 270, 315])
	for shot in st["shots"]:
		var clip := String(shot["clip"])
		for t in shot["t"]:
			var sheet := Image.create(w * headings.size(), h, false, Image.FORMAT_RGB8)
			for k in headings.size():
				who.rotation = Vector3(0, deg_to_rad(float(headings[k])), 0)
				_pose(clip, float(t))
				for i in 2: await RenderingServer.frame_post_draw
				var img := sv.get_texture().get_image(); img.convert(Image.FORMAT_RGB8)
				sheet.blit_rect(img, Rect2i(0, 0, w, h), Vector2i(k * w, 0))
			var out := "%s/%s_%s_t%.3f_%dx.png" % [String(st["out_dir"]), String(cfg.get("tag", "j")), clip, float(t), int(scale)]
			sheet.save_png(out)
			print("[j] still %s" % out)

func _film() -> void:
	var fm: Dictionary = cfg["film"]
	var w := int(fm.get("w", 1920)); var h := int(fm.get("h", 1080)); var scale := float(fm.get("scale", 2.0))
	sv = SubViewport.new(); sv.size = Vector2i(w, h); sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	add_child(sv); sv.add_child(cam); cam.current = true
	_aim(scale, float(h))
	var args := ["-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % [w, h], "-r", "30", "-i", "-",
		"-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", String(fm["out_mp4"])]
	var pipe := OS.execute_with_pipe("/opt/homebrew/bin/ffmpeg", args, true)
	var io: FileAccess = pipe["stdio"]
	var frames := 0
	for shot in fm["plan"]:
		var clip := String(shot["clip"]); var secs := float(shot["seconds"])
		var T := ap.get_animation(clip).length
		var rate := float(shot.get("rate", 1.0))
		who.rotation = Vector3(0, deg_to_rad(float(shot.get("heading_deg", 0.0))), 0)
		var n := int(round(secs * 30.0))
		for i in n:
			var tt := i / 30.0 * rate
			var t := fposmod(tt, T) if bool(shot.get("loop", false)) else minf(tt, T)
			_pose(clip, t)
			await RenderingServer.frame_post_draw
			var img := sv.get_texture().get_image(); img.convert(Image.FORMAT_RGB8)
			io.store_buffer(img.get_data()); frames += 1
	io.close()
	var pid := int(pipe["pid"])
	while OS.is_process_running(pid):
		await get_tree().create_timer(0.2).timeout
	print("[j] film: %d frames piped (%.2f s at 30 fps) -> %s" % [frames, frames / 30.0, fm["out_mp4"]])
