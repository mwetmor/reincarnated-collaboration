extends Node3D
## nb_w2 (R-C9-81): the JOIN sword in the barbarian's right hand -- stills at the TRUE play scale, the
## pairing still, and a short 2x film. A sandbox: its own project, nothing installed anywhere.
##
## BINDING is gear.gd's (attack_lab/t12/godot/scripts/gear.gd), reproduced: every piece's skinned
## MeshInstance3D reparented under the body's own Skeleton3D, its skin kept, `skeleton` pointed at
## it; each marker under a BoneAttachment3D recreated on the body's skeleton with its local
## transform. So the sockets `main_grip` / `main_tip` are read here exactly as a port would read them.
##
## POSE: the armed idle is `idle_guard` (its right arm IS axe_guard_R). The armed walk is `walk_armed`
## with the right arm taken from `axe_guard_R` through a filtered Blend2 (RightShoulder..RightHand) --
## the T12 (c) runtime guard layer. It is NOT knight.gd's tree (no armed-speed split: legs and upper
## body both from walk_armed), and says so on the card. weapon_r comes from each clip's own channel.
## grip_R = 1 (the sword); grip_L = 1 only when the off hand holds the axe (the pairing still).
##
## SCALE: rendered into an OFFSCREEN SubViewport of exactly the size asked, cam.size = rows/(PPM*scale):
## 100.6 px/m at 1x, 201.2 at 2x. Never the window (this display clamps a 1080-row window to 971).
## FILM frames are piped raw to ffmpeg, stepping exactly 1/30 s. env W2_MODE = stills | film,
## W2_CFG = the json (res:// path).

const PPM := 100.617553710938
const PL_PITCH_DEG := 52.95354112560294
const PL_YAW_DEG := 47.0
const CAM_STANDOFF := 60.0
const ARM_R := ["RightShoulder", "RightArm", "RightForeArm", "RightHand"]

var cfg: Dictionary
var who: Node3D
var skel: Skeleton3D
var ap: AnimationPlayer
var tree: AnimationTree
var body: MeshInstance3D
var sv: SubViewport
var cam: Camera3D
var markers := {}
var pipe: Dictionary = {}
var plan: Array = []
var i_shot := -1
var t_shot := 0.0
var frames := 0

func winter_sun() -> DirectionalLight3D:
	# VERBATIM from paint_stack.gd (as film.gd copied it): one light, low, pale-warm, screen upper-left
	var l := DirectionalLight3D.new()
	var e := deg_to_rad(55.0); var a := deg_to_rad(305.0)
	var d := Vector3(-sin(a) * cos(e), -sin(e), -cos(a) * cos(e)).normalized()
	l.look_at_from_position(Vector3(0, 30, 0), Vector3(0, 30, 0) + d, Vector3.UP)
	l.light_color = Color(1.0, 0.955, 0.885); l.light_energy = 0.90
	l.shadow_enabled = true; l.shadow_blur = 1.7
	l.directional_shadow_max_distance = CAM_STANDOFF + 50.0
	return l

func _ready() -> void:
	cfg = JSON.parse_string(FileAccess.get_file_as_string(OS.get_environment("W2_CFG")))
	var rig := Node3D.new(); rig.rotation_degrees.y = PL_YAW_DEG; add_child(rig); rig.add_child(winter_sun())
	var env := Environment.new(); env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.86, 0.88, 0.90)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(1, 1, 1); env.ambient_light_energy = 0.30
	var we := WorldEnvironment.new(); we.environment = env; add_child(we)
	var g := MeshInstance3D.new(); var pm := PlaneMesh.new(); pm.size = Vector2(80, 80); g.mesh = pm
	var sm := StandardMaterial3D.new(); sm.albedo_color = Color(0.80, 0.80, 0.82); sm.roughness = 0.95
	g.material_override = sm; add_child(g)
	who = (load(String(cfg["body"])) as PackedScene).instantiate(); add_child(who)
	skel = who.find_children("*", "Skeleton3D", true, false)[0]
	ap = who.find_child("AnimationPlayer", true, false)
	for p in cfg.get("pieces", []):
		_bind(String(p))
	for mi in who.find_children("*", "MeshInstance3D", true, false):
		if (mi as MeshInstance3D).find_blend_shape_by_name("grip_R") >= 0:
			body = mi
	_build_tree()
	sv = SubViewport.new()
	sv.size = Vector2i(int(cfg.get("w", 1920)), int(cfg.get("h", 1080)))
	sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	add_child(sv)
	cam = Camera3D.new(); cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT; cam.near = 0.05; cam.far = CAM_STANDOFF + 300.0
	sv.add_child(cam); cam.current = true
	get_tree().create_timer(float(cfg.get("watchdog_s", 240.0))).timeout.connect(func(): push_error("w2 WATCHDOG"); get_tree().quit(3))
	if OS.get_environment("W2_MODE") == "film":
		await _film()
	else:
		await _stills()
	get_tree().quit()

func _bind(path: String) -> void:
	var src := (load(path) as PackedScene).instantiate()
	for m in src.find_children("*", "MeshInstance3D", true, false):
		var mi := m as MeshInstance3D
		if mi.mesh == null:
			continue
		var local := mi.transform; var skin := mi.skin
		mi.owner = null; mi.get_parent().remove_child(mi)
		skel.add_child(mi)
		mi.transform = local; mi.skin = skin; mi.skeleton = NodePath("..")
	for n in src.find_children("*", "Node3D", true, false):
		var par := n.get_parent()
		if not (par is BoneAttachment3D) or n is MeshInstance3D or n is Skeleton3D:
			continue
		var att := BoneAttachment3D.new()
		att.bone_name = (par as BoneAttachment3D).bone_name
		skel.add_child(att)
		var mk := Node3D.new(); mk.name = String(n.name); att.add_child(mk)
		mk.transform = (n as Node3D).transform
		markers[String(n.name)] = mk
	src.queue_free()

func _build_tree() -> void:
	for c in ["idle_guard", "walk_armed", "axe_guard_R"]:
		if ap.has_animation(c):
			ap.get_animation(c).loop_mode = Animation.LOOP_LINEAR
	ap.stop()
	tree = AnimationTree.new(); ap.get_parent().add_child(tree)
	tree.anim_player = tree.get_path_to(ap)
	var bt := AnimationNodeBlendTree.new()
	var a_clip := AnimationNodeAnimation.new(); a_clip.animation = "idle_guard"
	var a_guard := AnimationNodeAnimation.new(); a_guard.animation = "axe_guard_R"
	var seek := AnimationNodeTimeSeek.new()
	var arm := AnimationNodeBlend2.new(); arm.filter_enabled = true
	bt.add_node("clip", a_clip); bt.add_node("seek", seek); bt.add_node("guard", a_guard); bt.add_node("arm", arm)
	bt.connect_node("seek", 0, "clip"); bt.connect_node("arm", 0, "seek"); bt.connect_node("arm", 1, "guard")
	bt.connect_node("output", 0, "arm")
	var an := ap.get_animation("walk_armed")
	for i in an.get_track_count():
		var pth: NodePath = an.track_get_path(i)
		if String(pth.get_concatenated_subnames()) in ARM_R:
			arm.set_filter_path(pth, true)
	tree.tree_root = bt
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	tree.active = true

func _pose(clip: String, t: float) -> void:
	((tree.tree_root as AnimationNodeBlendTree).get_node("clip") as AnimationNodeAnimation).animation = clip
	tree.set("parameters/arm/blend_amount", 1.0)
	tree.set("parameters/seek/seek_request", t)
	tree.advance(0.0)
	_morphs()

func _morphs() -> void:
	if body == null:
		return
	body.set_blend_shape_value(body.find_blend_shape_by_name("grip_R"), 1.0)
	body.set_blend_shape_value(body.find_blend_shape_by_name("grip_L"), float(cfg.get("grip_L", 0.0)))
	var hi := body.find_blend_shape_by_name("helmet_on")
	if hi >= 0:
		body.set_blend_shape_value(hi, 1.0 if "res://helmet.glb" in cfg.get("pieces", []) else 0.0)

func _aim(scale: float) -> void:
	cam.size = float(sv.size.y) / (PPM * scale)
	var p := deg_to_rad(PL_PITCH_DEG); var y := deg_to_rad(PL_YAW_DEG)
	var f := Vector3(-sin(y) * cos(p), -sin(p), -cos(y) * cos(p)).normalized()
	var at := who.global_position + Vector3(0, 0.95, 0)
	cam.look_at_from_position(at - f * CAM_STANDOFF, at, Vector3.UP)

func _stills() -> void:
	var out := String(cfg["out"])
	var sock := {}
	for clip in cfg["clips"]:
		for hd in cfg["headings"]:
			who.rotation_degrees.y = float(hd)
			_pose(String(clip), float(cfg.get("t", 1.0)))
			for sc in cfg["scales"]:
				_aim(float(sc))
				for i in 4: await RenderingServer.frame_post_draw
				sv.get_texture().get_image().save_png("%s/%s_%s_h%03d_s%d.png" % [out, cfg["tag"], clip, int(hd), int(sc)])
			# the sockets as a port reads them: marker world positions, in HIS frame (unrotated), metres
			var inv := who.global_transform.affine_inverse()
			var row := {}
			for k in markers:
				row[k] = inv * (markers[k] as Node3D).global_position
			sock["%s h%d" % [clip, int(hd)]] = row
	var f := FileAccess.open("%s/%s_sockets.json" % [out, cfg["tag"]], FileAccess.WRITE)
	var ser := {}
	for k in sock:
		var r := {}
		for m in sock[k]:
			var v: Vector3 = sock[k][m]
			r[m] = [snappedf(v.x, 0.0001), snappedf(v.y, 0.0001), snappedf(v.z, 0.0001)]
		ser[k] = r
	f.store_string(JSON.stringify(ser, " ")); f.close()
	print("[w2] stills done; markers bound: ", markers.keys())

func _film() -> void:
	plan = cfg["plan"]
	var sc := float(cfg.get("scale", 2.0))
	var args := ["-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % [sv.size.x, sv.size.y],
		"-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
		"-movflags", "+faststart", String(cfg["out_mp4"])]
	pipe = OS.execute_with_pipe("/opt/homebrew/bin/ffmpeg", args, true)
	var io: FileAccess = pipe["stdio"]
	var dt := 1.0 / 30.0
	_next()
	while i_shot < plan.size():
		_aim(sc)
		await RenderingServer.frame_post_draw
		var img := sv.get_texture().get_image(); img.convert(Image.FORMAT_RGB8)
		io.store_buffer(img.get_data()); frames += 1
		tree.advance(dt); _morphs()
		var s: Dictionary = plan[i_shot]
		var v := float(s.get("speed", 0.0))
		if v > 0.0:
			who.global_position += who.global_transform.basis.z * v * dt
		t_shot += dt
		if t_shot >= float(s["seconds"]) - 1e-6:
			_next()
	io.close()
	var pid := int(pipe["pid"])
	while OS.is_process_running(pid):
		await get_tree().create_timer(0.2).timeout
	print("[w2] film: %d frames piped (%.2f s) at %.1f px/m -> %s" % [frames, frames / 30.0, sv.size.y / cam.size, cfg["out_mp4"]])

func _next() -> void:
	i_shot += 1
	if i_shot >= plan.size():
		return
	t_shot = 0.0
	var s: Dictionary = plan[i_shot]
	who.rotation_degrees.y = float(s.get("heading_deg", 25.0))
	_pose(String(s["clip"]), 0.0)
