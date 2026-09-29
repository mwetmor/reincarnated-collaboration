extends SceneTree
# C-9 R-C9-66 T7-A diagnostic: WHY does a prop card not render over the projected terrain?
#
#   Godot --path godot --resolution 1920x1080 --script tools/probe_card.gd -- [--out D]
#
# Bisects the space in one run rather than reasoning about it:
#   0. does the texture even LOAD at the path build_props uses (globalized, not res://)?
#   1. where is the card, in the camera's own frame, and what does the ray hit?
#   2. does it draw at all -- counted in PIXELS against a card-hidden baseline?
#      as-is / depth_test_disabled / opaque standard material / projector removed /
#      depth_draw_always / res:// texture instead of an absolute path
#
# A pixel count is the instrument because "I cannot see it" is not a measurement and a
# card 3 px wide is invisible to the eye and present to a differ.

const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const PROP_PX := Vector2(1896.0139860139861, 2765.0)   # tree_living_a's anchor
const PITCH_COS := 0.602462407085

var out_dir := ""
var scene
var vp: SubViewport
var shot_cam: Camera3D
var lines: Array[String] = []


func say(s: String) -> void:
	print(s)
	lines.append(s)


func _initialize() -> void:
	out_dir = ProjectSettings.globalize_path("user://probe_card")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir)

	# ---- 0. the texture load, at both paths -----------------------------------
	var abs_dir := ProjectSettings.globalize_path("res://props")
	var rel := "assets/tree_living_a.png"
	say("[0] texture load")
	say("    abs dir            = %s" % abs_dir)
	var p_abs := abs_dir + "/" + rel
	say("    ResourceLoader.exists(abs) = %s" % str(ResourceLoader.exists(p_abs)))
	var t_abs = load(p_abs) if ResourceLoader.exists(p_abs) else null
	say("    load(abs)          = %s%s" % [str(t_abs),
		("  %dx%d" % [t_abs.get_width(), t_abs.get_height()]) if t_abs != null else ""])
	var p_res := "res://props/" + rel
	say("    ResourceLoader.exists(res) = %s" % str(ResourceLoader.exists(p_res)))
	var t_res = load(p_res) if ResourceLoader.exists(p_res) else null
	say("    load(res)          = %s%s" % [str(t_res),
		("  %dx%d" % [t_res.get_width(), t_res.get_height()]) if t_res != null else ""])

	# ---- scene ----------------------------------------------------------------
	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = false
	vp.transparent_bg = false
	vp.msaa_3d = Viewport.MSAA_DISABLED     # exact pixels, no coverage blending
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 40:
		await process_frame
	shot_cam = Camera3D.new()
	shot_cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	shot_cam.keep_aspect = Camera3D.KEEP_HEIGHT
	shot_cam.near = scene.cam.near
	shot_cam.far = scene.cam.far
	shot_cam.cull_mask = scene.cam.cull_mask
	vp.add_child(shot_cam)
	shot_cam.current = true
	if scene.knight != null:
		scene.knight.visible = false

	scene.look_at_canvas(PROP_PX)
	_mirror()
	await process_frame
	await process_frame

	var right: Vector3 = scene.right
	var up: Vector3 = scene.up
	var fwd: Vector3 = scene.fwd
	say("")
	say("[1] frame")
	say("    right = %s   up = %s   fwd = %s" % [str(right), str(up), str(fwd)])
	say("    game cam pos      = %s   dot(fwd) = %.3f   size = %.4f m" %
		[str(scene.cam.global_position), scene.cam.global_position.dot(fwd), scene.cam.size])
	say("    shot cam pos      = %s   dot(fwd) = %.3f   size = %.4f m" %
		[str(shot_cam.global_position), shot_cam.global_position.dot(fwd), shot_cam.size])
	say("    cam.near/far      = %.3f / %.1f" % [shot_cam.near, shot_cam.far])

	# every hit along the painter's own ray, nearest first
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var plane: Vector3 = CliffWorld.canvas_to_plane(PROP_PX, right, up)
	say("    guide-plane point dot(fwd) = %.3f" % plane.dot(fwd))
	var from: Vector3 = plane - fwd * 150.0
	var excl := []
	for n in 8:
		var q := PhysicsRayQueryParameters3D.create(from, from + fwd * 400.0)
		q.exclude = excl
		var h := space.intersect_ray(q)
		if h.is_empty():
			break
		var pos: Vector3 = h["position"]
		var col = h["collider"]
		say("    ray hit %d: dot(fwd) %8.3f  dist-from-cam %7.3f  owner %s" %
			[n, pos.dot(fwd), pos.distance_to(shot_cam.global_position),
			 str(col.get_parent().name)])
		excl.append(h["rid"])

	# how many FG meshes, and what depth range do they span?
	var lo := 1e9
	var hi := -1e9
	for mi in scene._fg:
		var aabb: AABB = (mi as MeshInstance3D).global_transform * (mi as MeshInstance3D).get_aabb()
		for c in 8:
			var d: float = aabb.get_endpoint(c).dot(fwd)
			lo = minf(lo, d)
			hi = maxf(hi, d)
	say("    %d fg meshes span dot(fwd) [%.2f .. %.2f]" % [scene._fg.size(), lo, hi])

	# ---- 2. the card ----------------------------------------------------------
	var tex: Texture2D = t_res if t_res != null else t_abs
	if tex == null:
		say("[2] no texture at either path -- stopping")
		_write()
		quit(1)
		return
	var w := float(tex.get_width())
	var h := float(tex.get_height())
	var anc := Vector2(328.013986013986, 561.0)
	var centre_px := PROP_PX - anc + Vector2(w, h) * 0.5
	var hit := CliffWorld.ground_at(space, PROP_PX, right, up, fwd)
	var h_world := (h / PPM) / PITCH_COS
	var mi2 := MeshInstance3D.new()
	mi2.name = "ProbeCard"
	var qm := QuadMesh.new()
	qm.size = Vector2(w / PPM, h_world)
	mi2.mesh = qm
	mi2.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	scene.add_child(mi2)
	var flat := right
	flat.y = 0.0
	flat = flat.normalized()
	var nrm := flat.cross(Vector3.UP)
	var base: Vector3 = hit["position"] if not hit.is_empty() else plane
	mi2.global_transform = Transform3D(Basis(flat, Vector3.UP, nrm),
		base + Vector3.UP * (h_world * 0.5 * (1.0 - anc.y / maxf(h, 1.0)) + 0.05)
		+ flat * ((centre_px.x - PROP_PX.x) / PPM))
	say("")
	say("[2] the card, built exactly as build_props builds it")
	say("    tex %dx%d  ->  %.2f x %.2f m (h stretched 1/cos(pitch))" %
		[int(w), int(h), w / PPM, h_world])
	say("    ground hit at dot(fwd) %.3f" % (base.dot(fwd)))
	say("    card origin dot(fwd) = %.3f" % mi2.global_position.dot(fwd))
	var ab: AABB = mi2.global_transform * mi2.get_aabb()
	var clo := 1e9
	var chi := -1e9
	for c in 8:
		var d: float = ab.get_endpoint(c).dot(fwd)
		clo = minf(clo, d)
		chi = maxf(chi, d)
	say("    card AABB dot(fwd) [%.3f .. %.3f]   (LOWER = nearer the camera)" % [clo, chi])
	say("    card visible_in_tree = %s  layers = %d  aabb size = %s" %
		[str(mi2.is_visible_in_tree()), mi2.layers, str(mi2.get_aabb().size)])
	# where on screen the card's centre should land
	var uc := shot_cam.unproject_position(mi2.global_position)
	say("    card centre unprojects to screen %s" % str(uc))

	# ---- pixel counting ------------------------------------------------------
	mi2.visible = false
	var baseline := await _grab("00_baseline")
	say("")
	say("[3] does it draw? pixels differing from the card-hidden baseline")

	var cases := [
		["as_is", "scissor+depth_draw_opaque, projector on"],
		["depth_test_off", "same card, depth_test_disabled"],
		["standard_opaque", "plain StandardMaterial3D, magenta, unshaded"],
		["projector_off", "as_is card, terrain material_override removed"],
		["depth_draw_always", "as_is card + depth_draw_always"],
		["no_discard", "as_is card, discard removed (solid)"],
	]
	var results := {}
	for c in cases:
		var nm: String = c[0]
		_configure(mi2, nm, tex)
		mi2.visible = true
		var img := await _grab("01_%s" % nm)
		var n := _diff(baseline, img)
		results[nm] = n
		say("    %-18s %8d px   (%s)" % [nm, n, c[1]])
		mi2.visible = false
		if nm == "projector_off":
			scene.set_plate(true)

	_write()
	var jf := FileAccess.open(out_dir + "/probe_card.json", FileAccess.WRITE)
	jf.store_string(JSON.stringify(results, " "))
	jf.close()
	quit(0)


func _configure(mi: MeshInstance3D, mode: String, tex: Texture2D) -> void:
	scene.set_plate(mode != "projector_off")
	if mode == "standard_opaque":
		var sm := StandardMaterial3D.new()
		sm.albedo_color = Color(1, 0, 1)
		sm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		sm.cull_mode = BaseMaterial3D.CULL_DISABLED
		mi.material_override = sm
		return
	var rm := "unshaded, cull_disabled, depth_draw_opaque, shadows_disabled"
	var body := "vec4 c = texture(tex, UV); if (c.a < 0.35) discard; ALBEDO = c.rgb; ALPHA = 1.0;"
	match mode:
		"depth_test_off":
			rm = "unshaded, cull_disabled, depth_draw_opaque, depth_test_disabled, shadows_disabled"
		"depth_draw_always":
			rm = "unshaded, cull_disabled, depth_draw_always, shadows_disabled"
		"no_discard":
			body = "ALBEDO = vec3(1.0, 0.0, 1.0); ALPHA = 1.0;"
	var sh := Shader.new()
	sh.code = "shader_type spatial;\nrender_mode %s;\nuniform sampler2D tex : source_color, filter_linear_mipmap;\nvoid fragment() { %s }\n" % [rm, body]
	var m := ShaderMaterial.new()
	m.shader = sh
	m.set_shader_parameter("tex", tex)
	mi.material_override = m


func _mirror() -> void:
	shot_cam.global_transform = scene.cam.global_transform
	shot_cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))


func _grab(name: String) -> Image:
	_mirror()
	for i in 4:
		await process_frame
	var img := vp.get_texture().get_image()
	img.save_png("%s/%s.png" % [out_dir, name])
	return img


func _diff(a: Image, b: Image) -> int:
	var n := 0
	for y in range(0, a.get_height()):
		for x in range(0, a.get_width()):
			var ca := a.get_pixel(x, y)
			var cb := b.get_pixel(x, y)
			if absf(ca.r - cb.r) + absf(ca.g - cb.g) + absf(ca.b - cb.b) > 0.02:
				n += 1
	return n


func _write() -> void:
	var f := FileAccess.open(out_dir + "/probe_card.txt", FileAccess.WRITE)
	f.store_string("\n".join(lines) + "\n")
	f.close()
	print("[probe] -> ", out_dir)
