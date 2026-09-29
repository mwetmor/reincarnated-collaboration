extends SceneTree
# C-9 T7-A diagnostic round 2. Round 1 showed the card does not draw even with
# depth_test_disabled -- so it is NOT a depth problem -- and that the ONLY case that drew
# with a ShaderMaterial carried `depth_draw_always`. Two candidate explanations remain and
# they are told apart by TIME, not by argument:
#
#   (i)  render_mode semantics      -> 0 px forever, however many frames pass
#   (ii) async pipeline compilation -> 0 px for the first frames, then the real count
#
# So: hold each case and count at 1, 3, 8, 20, 60 frames. Same card, same transform, one
# baseline. Also drops each case's shader code to disk so a compile error cannot hide.

const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const PROP_PX := Vector2(1896.0139860139861, 2765.0)
const PITCH_COS := 0.602462407085
const GRABS := [1, 3, 8, 20, 60]

var out_dir := ""
var scene
var vp: SubViewport
var shot_cam: Camera3D
var lines: Array[String] = []
var card: MeshInstance3D
var tex: Texture2D
var baseline: Image


func say(s: String) -> void:
	print(s)
	lines.append(s)


func _initialize() -> void:
	out_dir = ProjectSettings.globalize_path("user://probe_card2")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir)

	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = false
	vp.msaa_3d = Viewport.MSAA_DISABLED
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60:
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

	tex = load("res://props/assets/tree_living_a.png")
	var right: Vector3 = scene.right
	var up: Vector3 = scene.up
	var fwd: Vector3 = scene.fwd
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var anc := Vector2(328.013986013986, 561.0)
	var w := float(tex.get_width())
	var h := float(tex.get_height())
	var centre_px := PROP_PX - anc + Vector2(w, h) * 0.5
	var hit := CliffWorld.ground_at(space, PROP_PX, right, up, fwd)
	var h_world := (h / PPM) / PITCH_COS
	card = MeshInstance3D.new()
	card.name = "ProbeCard"
	var qm := QuadMesh.new()
	qm.size = Vector2(w / PPM, h_world)
	card.mesh = qm
	card.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	scene.add_child(card)
	var flat := right
	flat.y = 0.0
	flat = flat.normalized()
	var base: Vector3 = hit["position"] if not hit.is_empty() else CliffWorld.canvas_to_plane(PROP_PX, right, up)
	card.global_transform = Transform3D(Basis(flat, Vector3.UP, flat.cross(Vector3.UP)),
		base + Vector3.UP * (h_world * 0.5 * (1.0 - anc.y / maxf(h, 1.0)) + 0.05)
		+ flat * ((centre_px.x - PROP_PX.x) / PPM))

	card.visible = false
	_mirror()
	for i in 20:
		await process_frame
	baseline = vp.get_texture().get_image()
	baseline.save_png(out_dir + "/00_baseline.png")

	say("frames held ->            %s" % str(GRABS))
	for c in _cases():
		var nm: String = c[0]
		card.visible = false
		for i in 5:
			await process_frame
		card.material_override = _mat(c)
		_dump(nm, c)
		card.visible = true
		var row: Array[int] = []
		var prev := 0
		for g in GRABS:
			for i in range(g - prev):
				await process_frame
			prev = g
			var img := vp.get_texture().get_image()
			row.append(_diff(baseline, img))
			if g == GRABS[-1]:
				img.save_png("%s/01_%s.png" % [out_dir, nm])
		say("  %-22s %s   %s" % [nm, str(row), c[3]])

	_write()
	quit(0)


func _cases() -> Array:
	# [name, render_mode, fragment body, note]
	var scissor := "vec4 c = texture(tex, UV); if (c.a < 0.35) discard; ALBEDO = c.rgb; ALPHA = 1.0;"
	var scissor_noalpha := "vec4 c = texture(tex, UV); if (c.a < 0.35) discard; ALBEDO = c.rgb;"
	var solid := "ALBEDO = vec3(1.0, 0.0, 1.0); ALPHA = 1.0;"
	var solid_noalpha := "ALBEDO = vec3(1.0, 0.0, 1.0);"
	return [
		["A_orig", "unshaded, cull_disabled, depth_draw_opaque, shadows_disabled", scissor,
			"the shipped card material, verbatim"],
		["B_draw_always", "unshaded, cull_disabled, depth_draw_always, shadows_disabled", scissor,
			"only depth_draw changed"],
		["C_no_depth_token", "unshaded, cull_disabled, shadows_disabled", scissor,
			"no depth_draw token at all (= opaque, the default)"],
		["D_no_alpha_write", "unshaded, cull_disabled, depth_draw_opaque, shadows_disabled",
			scissor_noalpha, "never assigns ALPHA"],
		["E_solid_alpha", "unshaded, cull_disabled, depth_draw_opaque, shadows_disabled", solid,
			"no discard, assigns ALPHA=1"],
		["F_solid_noalpha", "unshaded, cull_disabled, depth_draw_opaque, shadows_disabled",
			solid_noalpha, "no discard, no ALPHA"],
		["G_cull_back", "unshaded, cull_back, depth_draw_opaque, shadows_disabled", scissor,
			"cull_back instead of cull_disabled"],
		["H_prepass_alpha", "unshaded, cull_disabled, depth_prepass_alpha, shadows_disabled",
			scissor, "depth_prepass_alpha"],
		["I_standard_scissor", "@standard", "", "StandardMaterial3D + alpha scissor"],
		["J_standard_magenta", "@magenta", "", "StandardMaterial3D, opaque magenta"],
	]


func _mat(c: Array) -> Material:
	if c[1] == "@standard":
		var sm := StandardMaterial3D.new()
		sm.albedo_texture = tex
		sm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
		sm.alpha_scissor_threshold = 0.35
		sm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		sm.cull_mode = BaseMaterial3D.CULL_DISABLED
		sm.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
		return sm
	if c[1] == "@magenta":
		var sm2 := StandardMaterial3D.new()
		sm2.albedo_color = Color(1, 0, 1)
		sm2.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		sm2.cull_mode = BaseMaterial3D.CULL_DISABLED
		return sm2
	var sh := Shader.new()
	sh.code = "shader_type spatial;\nrender_mode %s;\nuniform sampler2D tex : source_color, filter_linear_mipmap;\nvoid fragment() { %s }\n" % [c[1], c[2]]
	var m := ShaderMaterial.new()
	m.shader = sh
	m.set_shader_parameter("tex", tex)
	return m


func _dump(nm: String, c: Array) -> void:
	if c[1].begins_with("@"):
		return
	var f := FileAccess.open("%s/shader_%s.gdshader" % [out_dir, nm], FileAccess.WRITE)
	f.store_string("shader_type spatial;\nrender_mode %s;\nuniform sampler2D tex : source_color, filter_linear_mipmap;\nvoid fragment() { %s }\n" % [c[1], c[2]])
	f.close()


func _mirror() -> void:
	shot_cam.global_transform = scene.cam.global_transform
	shot_cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))


func _diff(a: Image, b: Image) -> int:
	var n := 0
	for y in a.get_height():
		for x in a.get_width():
			var ca := a.get_pixel(x, y)
			var cb := b.get_pixel(x, y)
			if absf(ca.r - cb.r) + absf(ca.g - cb.g) + absf(ca.b - cb.b) > 0.02:
				n += 1
	return n


func _write() -> void:
	var f := FileAccess.open(out_dir + "/probe_card2.txt", FileAccess.WRITE)
	f.store_string("\n".join(lines) + "\n")
	f.close()
	print("[probe2] -> ", out_dir)
