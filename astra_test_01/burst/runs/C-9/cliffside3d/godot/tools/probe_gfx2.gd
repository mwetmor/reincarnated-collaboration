extends SceneTree
# C-9 T10 — probe 2, after probe 1 caught MY OWN READOUT rather than the engine.
#
# probe_gfx.gd reported that the screen-space normal buffer matched neither world nor view
# normals and that linear depth came back 47 m long. Both were true readings of a frame I
# was DECODING WRONG: an 8-bit render target stores sRGB, and I sampled `Image.get_pixel`
# and treated the byte as the linear value the shader wrote. Undoing the transfer function
# by hand, the normal buffer matches the VIEW-SPACE normal to 0.005 on a floor and 0.011 on
# a wall, and depth lands within a quantisation step of the metres the camera says.
# Instrument sound; reader broken. So this probe reads through _lin() everywhere, and asks
# the two questions probe 1 could not answer:
#
#   A. THE OUTPUT PATH ITSELF. A light() that writes a CONSTANT must come back as exactly
#      that constant. Until that holds, no reading of a ramp means anything -- probe 1's
#      ramp came back near-white on a surface facing away from the sun, which is either a
#      wrong ramp or a wrong path, and those need separating before either is chased.
#   B. DEPTH LINEARITY AT A SCALE THE INK PASS CARES ABOUT: two floors a known distance
#      apart in depth, so the metres-per-unit the Roberts threshold is set in is measured
#      and not inferred from one absolute reading near the top of an 8-bit ramp.
#
#   Godot --path godot --resolution 640x360 --script tools/probe_gfx2.gd -- --out DIR

const RES := Vector2i(640, 360)
const PITCH := 52.95354112560294
const YAW := 47.0
const PPM := 100.617553710938

var out := ""
var report := {}


func _initialize() -> void:
	out = ProjectSettings.globalize_path("user://probe_gfx2")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out)
	await _probe_light_path()
	await _probe_depth_scale()
	var f := FileAccess.open(out + "/probe_gfx2.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("[probe_gfx2] -> %s/probe_gfx2.json" % out)
	quit(0)


func _sun_dir() -> Vector3:
	var elev := deg_to_rad(18.0)
	var az := deg_to_rad(125.0)
	return Vector3(-sin(az) * cos(elev), -sin(elev), -cos(az) * cos(elev)).normalized()


func _probe_light_path() -> void:
	var vp := SubViewport.new()
	vp.size = RES
	vp.own_world_3d = true
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)

	var floor_mi := MeshInstance3D.new()
	var pm := PlaneMesh.new()
	pm.size = Vector2(20, 20)
	floor_mi.mesh = pm
	vp.add_child(floor_mi)
	var wall := MeshInstance3D.new()
	var pw := PlaneMesh.new()
	pw.size = Vector2(6, 6)
	wall.mesh = pw
	wall.rotation = Vector3(deg_to_rad(90.0), 0.0, 0.0)
	wall.position = Vector3(0.0, 3.0, -4.0)
	vp.add_child(wall)

	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.size = float(RES.y) / PPM * 4.0
	cam.near = 0.05
	cam.far = 600.0
	var p := deg_to_rad(PITCH)
	var y := deg_to_rad(YAW)
	var fwd := Vector3(-sin(y) * cos(p), -sin(p), -cos(y) * cos(p)).normalized()
	vp.add_child(cam)
	cam.look_at_from_position(-fwd * 100.0, Vector3.ZERO, Vector3.UP)
	cam.current = true

	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0, 0, 0, 1)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0, 0, 0)
	env.ambient_light_energy = 0.0
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	env.tonemap_exposure = 1.0
	env.tonemap_white = 1.0
	env.ssao_enabled = false
	env.ssil_enabled = false
	env.sdfgi_enabled = false
	env.glow_enabled = false
	env.fog_enabled = false
	var we := WorldEnvironment.new()
	we.environment = env
	vp.add_child(we)

	var ldir := _sun_dir()
	var sun := DirectionalLight3D.new()
	sun.look_at_from_position(Vector3(0, 10, 0), Vector3(0, 10, 0) + ldir, Vector3.UP)
	sun.light_energy = 1.0
	sun.light_color = Color(1, 1, 1)
	sun.shadow_enabled = false
	vp.add_child(sun)

	var mat := ShaderMaterial.new()
	var sh := Shader.new()
	sh.code = """
shader_type spatial;
render_mode specular_disabled;
uniform int mode = 0;
void fragment() { ALBEDO = vec3(0.5); }
void light() {
	float ndl = dot(normalize(NORMAL), normalize(LIGHT));
	if (mode == 0) { DIFFUSE_LIGHT = vec3(0.25); }                   // the path itself
	else if (mode == 1) { DIFFUSE_LIGHT = vec3(ndl * 0.5 + 0.5) * 0.5; }  // t, halved
	else if (mode == 2) { DIFFUSE_LIGHT = vec3(ATTENUATION) * 0.5; }
	else if (mode == 3) { DIFFUSE_LIGHT = LIGHT_COLOR * 0.25; }
	else { DIFFUSE_LIGHT = vec3(ALBEDO) * 0.5; }
}
"""
	mat.shader = sh
	floor_mi.material_override = mat
	wall.material_override = mat

	await _settle(vp)
	var centre := Vector2i(RES.x / 2, RES.y / 2)
	var wall_px := cam.unproject_position(Vector3(0.0, 3.0, -4.0))
	var wpx := Vector2i(int(wall_px.x), int(wall_px.y))
	var L := -ldir
	var res := {}
	var names := {0: "const_0.25", 1: "t_halved", 2: "attenuation", 3: "light_color_q", 4: "albedo_halved"}
	for m in [0, 1, 2, 3, 4]:
		mat.set_shader_parameter("mode", m)
		await _settle(vp)
		var img: Image = vp.get_texture().get_image()
		if m == 1:
			img.save_png(out + "/t_halved.png")
		res[names[m]] = {"floor": snappedf(_lin(img.get_pixelv(centre).r), 0.004),
						 "wall": snappedf(_lin(img.get_pixelv(wpx).r), 0.004)}
	report["light_path"] = {
		"_q": "a light() writing a CONSTANT must read back as that constant",
		"read": res,
		"expect": {
			"const_0.25": 0.25,
			"t_halved_floor": snappedf((Vector3(0, 1, 0).dot(L) * 0.5 + 0.5) * 0.5, 0.001),
			"t_halved_wall": snappedf((Vector3(0, 0, 1).dot(L) * 0.5 + 0.5) * 0.5, 0.001),
			"attenuation_no_shadow": 1.0,
			"albedo_halved": 0.25,
		},
		"note_8bit": "one byte at these levels is about %s in linear" % snappedf(_lin(0.5) - _lin(0.5 - 1.0 / 255.0), 0.0001),
	}
	vp.queue_free()


func _probe_depth_scale() -> void:
	"""Two quads a KNOWN 20 m apart along the view direction. The ink pass sets its
	threshold in metres of depth discontinuity, so what has to be measured is metres per
	unit of the reconstruction -- not one absolute distance read off the top of an 8-bit
	ramp, where a byte is three quarters of a metre."""
	var vp := SubViewport.new()
	vp.size = RES
	vp.own_world_3d = true
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.size = 8.0
	cam.near = 0.05
	cam.far = 200.0
	vp.add_child(cam)
	# straight down -Z, so depth is trivially the z separation
	cam.look_at_from_position(Vector3(0, 0, 60), Vector3(0, 0, 0), Vector3.UP)
	cam.current = true
	var near_q := MeshInstance3D.new()
	var qm1 := QuadMesh.new()
	qm1.size = Vector2(4, 8)
	near_q.mesh = qm1
	near_q.position = Vector3(-2.5, 0, 20.0)     # 40 m from the camera
	vp.add_child(near_q)
	var far_q := MeshInstance3D.new()
	var qm2 := QuadMesh.new()
	qm2.size = Vector2(4, 8)
	far_q.mesh = qm2
	far_q.position = Vector3(2.5, 0, 0.0)        # 60 m from the camera
	vp.add_child(far_q)

	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0, 0, 0, 1)
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	var we := WorldEnvironment.new()
	we.environment = env
	vp.add_child(we)

	var sh := Shader.new()
	sh.code = """
shader_type spatial;
render_mode unshaded, depth_draw_never, depth_test_disabled, cull_disabled, fog_disabled;
uniform sampler2D depth_tex : hint_depth_texture, filter_nearest;
uniform float scale_m = 100.0;
void vertex() { POSITION = vec4(VERTEX.xy * 2.0, 1.0, 1.0); }
void fragment() {
	float d = texture(depth_tex, SCREEN_UV).r;
	vec3 ndc = vec3(SCREEN_UV * 2.0 - 1.0, d);
	vec4 v = INV_PROJECTION_MATRIX * vec4(ndc, 1.0);
	v.xyz /= v.w;
	ALBEDO = vec3(-v.z / scale_m);
}
"""
	var mat := ShaderMaterial.new()
	mat.shader = sh
	mat.render_priority = 100
	mat.set_shader_parameter("scale_m", 100.0)
	var q := MeshInstance3D.new()
	var qm := QuadMesh.new()
	qm.size = Vector2(2, 2)
	q.mesh = qm
	q.material_override = mat
	q.extra_cull_margin = 1e5
	cam.add_child(q)
	q.position = Vector3(0, 0, -1)

	await _settle(vp)
	var img: Image = vp.get_texture().get_image()
	img.save_png(out + "/depth_scale.png")
	var pn := cam.unproject_position(Vector3(-2.5, 0, 20.0))
	var pf := cam.unproject_position(Vector3(2.5, 0, 0.0))
	var got_n := _lin(img.get_pixelv(Vector2i(int(pn.x), int(pn.y))).r) * 100.0
	var got_f := _lin(img.get_pixelv(Vector2i(int(pf.x), int(pf.y))).r) * 100.0
	report["depth_scale"] = {
		"_q": "metres per unit of the reconstruction, from a KNOWN 20 m separation",
		"near_quad": {"got_m": snappedf(got_n, 0.01), "expect_m": 40.0},
		"far_quad": {"got_m": snappedf(got_f, 0.01), "expect_m": 60.0},
		"separation": {"got_m": snappedf(got_f - got_n, 0.01), "expect_m": 20.0},
	}
	vp.queue_free()


func _lin(c: float) -> float:
	return c / 12.92 if c <= 0.04045 else pow((c + 0.055) / 1.055, 2.4)


func _settle(vp: SubViewport) -> void:
	for i in 6:
		await process_frame
	RenderingServer.force_draw()
	await process_frame
