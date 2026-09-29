extends SceneTree
# C-9 T10 — VERIFY THE INSTRUMENTS BEFORE BUILDING THE STACK.
#
# Four things the barrow render stack is about to depend on, none of which I am willing to
# assume from documentation:
#
#   1. hint_normal_roughness_texture: WHICH SPACE are those normals in? A Roberts cross on
#      normals is the same arithmetic in view space and world space, but the SNOW layer and
#      any "is this facing up" test are not, and a stack that silently reads a view normal
#      as a world normal looks plausible from one camera angle and only one.
#   2. hint_depth_texture through INV_PROJECTION_MATRIX under an ORTHOGRAPHIC camera:
#      does it come back as metres from the camera, and is it linear?
#   3. Environment's fog property names in 4.6 — height fog in a basin needs the real ones.
#   4. The watercolour light() ramp: does the shader's banded N.L match the arithmetic
#      GDScript says it should be, on surfaces whose normals I know exactly?
#
# Every answer is read off a rendered pixel over geometry whose world normal and distance
# are known by construction, not off a scene that happens to be lying around.
#
#   Godot --path godot --resolution 640x360 --script tools/probe_gfx.gd

const RES := Vector2i(640, 360)
const PITCH := 52.95354112560294
const YAW := 47.0
const PPM := 100.617553710938

var out := ""
var report := {}


func _initialize() -> void:
	out = ProjectSettings.globalize_path("user://probe_gfx")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out)

	_probe_env_props()
	await _probe_buffers()
	await _probe_ramp()

	var f := FileAccess.open(out + "/probe_gfx.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("[probe_gfx] -> %s/probe_gfx.json" % out)
	quit(0)


# --- 3: what Environment actually calls its fog ---------------------------------
func _probe_env_props() -> void:
	var e := Environment.new()
	var fog := []
	for p in e.get_property_list():
		var n := String(p["name"])
		if n.begins_with("fog_") or n.begins_with("adjustment_") or n == "fog_mode":
			fog.append(n)
	report["environment_fog_properties"] = fog
	var modes := []
	for k in ["FOG_MODE_EXPONENTIAL", "FOG_MODE_DEPTH"]:
		modes.append(k)
	report["fog_mode_constants_exist"] = {
		"FOG_MODE_EXPONENTIAL": Environment.FOG_MODE_EXPONENTIAL,
		"FOG_MODE_DEPTH": Environment.FOG_MODE_DEPTH,
	}


# --- a known world: a floor (+Y), a wall facing camera-ish, a cube ---------------
func _known_world(vp: SubViewport) -> Dictionary:
	var root3 := Node3D.new()
	vp.add_child(root3)
	# floor: a 20 m plane, world normal exactly (0,1,0)
	var floor_mi := MeshInstance3D.new()
	var pm := PlaneMesh.new()
	pm.size = Vector2(20, 20)
	floor_mi.mesh = pm
	root3.add_child(floor_mi)
	# wall: a plane rotated so its world normal is exactly (0,0,1)
	var wall := MeshInstance3D.new()
	var pw := PlaneMesh.new()
	pw.size = Vector2(6, 6)
	wall.mesh = pw
	wall.rotation = Vector3(deg_to_rad(90.0), 0.0, 0.0)
	wall.position = Vector3(0.0, 3.0, -4.0)
	root3.add_child(wall)
	# the camera: the law. ortho, pitch 52.95, yaw 47, size = rows / PPM
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.size = float(RES.y) / PPM * 4.0        # 4x zoomed out so 20 m fits in 360 rows
	cam.near = 0.05
	cam.far = 600.0
	var p := deg_to_rad(PITCH)
	var y := deg_to_rad(YAW)
	# a view direction that descends at PITCH below horizontal, on the YAW azimuth
	var fwd := Vector3(-sin(y) * cos(p), -sin(p), -cos(y) * cos(p)).normalized()
	var aim := Vector3(0.0, 0.0, 0.0)
	var dist := 100.0
	vp.add_child(cam)
	cam.look_at_from_position(aim - fwd * dist, aim, Vector3.UP)
	cam.current = true
	return {"root": root3, "cam": cam, "floor": floor_mi, "wall": wall,
			"fwd": fwd, "dist": dist, "aim": aim}


# --- 1 + 2: what the screen-space buffers hand back -----------------------------
func _probe_buffers() -> void:
	var vp := SubViewport.new()
	vp.size = RES
	vp.own_world_3d = true
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	var w := _known_world(vp)
	var cam: Camera3D = w["cam"]

	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0, 0, 0, 1)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(1, 1, 1)
	env.ambient_light_energy = 1.0
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	var we := WorldEnvironment.new()
	we.environment = env
	vp.add_child(we)

	# THE READOUT QUAD: a full-screen unshaded pass that writes what the buffers say,
	# straight into the colour channels, with no tonemap curve to invert (LINEAR above).
	var sh := Shader.new()
	sh.code = """
shader_type spatial;
render_mode unshaded, depth_draw_never, depth_test_disabled, cull_disabled, fog_disabled;
uniform sampler2D depth_tex : hint_depth_texture, filter_nearest;
uniform sampler2D nrm_tex : hint_normal_roughness_texture, filter_nearest;
uniform int mode = 0;          // 0 = raw normal buffer rgb, 1 = linear depth / 200
void vertex() { POSITION = vec4(VERTEX.xy * 2.0, 1.0, 1.0); }
void fragment() {
	vec2 uv = SCREEN_UV;
	if (mode == 0) {
		ALBEDO = texture(nrm_tex, uv).rgb;
	} else {
		float d = texture(depth_tex, uv).r;
		vec3 ndc = vec3(uv * 2.0 - 1.0, d);
		vec4 v = INV_PROJECTION_MATRIX * vec4(ndc, 1.0);
		v.xyz /= v.w;
		ALBEDO = vec3(-v.z / 200.0);
	}
}
"""
	var mat := ShaderMaterial.new()
	mat.shader = sh
	mat.render_priority = 100
	var q := MeshInstance3D.new()
	var qm := QuadMesh.new()
	qm.size = Vector2(2, 2)
	q.mesh = qm
	q.material_override = mat
	q.extra_cull_margin = 1e5
	cam.add_child(q)
	q.position = Vector3(0, 0, -1)

	# Where to look: the pixel the AIM point lands on is the viewport centre by
	# construction (the camera looks AT the aim), which is on the FLOOR. A point on the
	# WALL is found by projecting its world position through the camera itself rather than
	# by counting pixels.
	await _settle(vp)
	var centre := Vector2i(RES.x / 2, RES.y / 2)
	var wall_world := Vector3(0.0, 3.0, -4.0)
	var wall_px := cam.unproject_position(wall_world)

	mat.set_shader_parameter("mode", 0)
	await _settle(vp)
	var img_n: Image = vp.get_texture().get_image()
	img_n.save_png(out + "/buf_normal.png")
	mat.set_shader_parameter("mode", 1)
	await _settle(vp)
	var img_d: Image = vp.get_texture().get_image()
	img_d.save_png(out + "/buf_depth.png")

	# what the camera's own matrices say the answer SHOULD be
	var view := cam.global_transform.affine_inverse()
	var floor_n_world := Vector3(0, 1, 0)
	var wall_n_world := Vector3(0, 0, 1)
	var floor_n_view := (view.basis * floor_n_world).normalized()
	var wall_n_view := (view.basis * wall_n_world).normalized()

	var got_floor := _enc(img_n, centre)
	var got_wall := _enc(img_n, Vector2i(int(wall_px.x), int(wall_px.y)))
	# depth: distance along the view direction from the camera plane
	var d_floor: float = absf((w["aim"] as Vector3 - cam.global_position).dot(-view.basis.z * -1.0))
	var cam_fwd := -cam.global_transform.basis.z
	var d_floor2: float = ((w["aim"] as Vector3) - cam.global_position).dot(cam_fwd)
	var d_wall: float = (wall_world - cam.global_position).dot(cam_fwd)
	var got_d_floor := img_d.get_pixelv(centre).r * 200.0
	var got_d_wall := img_d.get_pixelv(Vector2i(int(wall_px.x), int(wall_px.y))).r * 200.0

	report["normal_buffer"] = {
		"_q": "which space? compare decoded n*2-1 against world and view normals",
		"floor": {"decoded": _v(got_floor), "world": _v(floor_n_world), "view": _v(floor_n_view),
				  "err_world": snappedf((got_floor - floor_n_world).length(), 0.001),
				  "err_view": snappedf((got_floor - floor_n_view).length(), 0.001)},
		"wall": {"decoded": _v(got_wall), "world": _v(wall_n_world), "view": _v(wall_n_view),
				 "err_world": snappedf((got_wall - wall_n_world).length(), 0.001),
				 "err_view": snappedf((got_wall - wall_n_view).length(), 0.001)},
		"wall_px": [int(wall_px.x), int(wall_px.y)],
	}
	report["depth_buffer"] = {
		"_q": "metres from the camera plane along its forward, under an ORTHO projection",
		"floor": {"got_m": snappedf(got_d_floor, 0.01), "expect_m": snappedf(d_floor2, 0.01)},
		"wall": {"got_m": snappedf(got_d_wall, 0.01), "expect_m": snappedf(d_wall, 0.01)},
	}
	vp.queue_free()


# --- 4: the ramp, against the arithmetic ---------------------------------------
func _probe_ramp() -> void:
	var vp := SubViewport.new()
	vp.size = RES
	vp.own_world_3d = true
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	var w := _known_world(vp)
	var cam: Camera3D = w["cam"]

	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0, 0, 0, 1)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0, 0, 0)
	env.ambient_light_energy = 0.0        # NO ambient: the ramp alone, or the check is of a sum
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	env.tonemap_exposure = 1.0
	env.tonemap_white = 1.0
	env.sdfgi_enabled = false
	env.ssao_enabled = false
	env.glow_enabled = false
	var we := WorldEnvironment.new()
	we.environment = env
	vp.add_child(we)

	# one light, direction KNOWN
	var sun := DirectionalLight3D.new()
	var elev := deg_to_rad(18.0)
	var az := deg_to_rad(125.0)
	var ldir := Vector3(-sin(az) * cos(elev), -sin(elev), -cos(az) * cos(elev)).normalized()
	sun.look_at_from_position(Vector3(0, 10, 0), Vector3(0, 10, 0) + ldir, Vector3.UP)
	sun.light_energy = 1.0
	sun.light_color = Color(1, 1, 1)
	sun.shadow_enabled = false
	vp.add_child(sun)

	# the ramp, with the NOISE OFF so it is a pure function of N.L and therefore checkable
	var sh := Shader.new()
	sh.code = _RAMP_CODE
	var mat := ShaderMaterial.new()
	mat.shader = sh
	mat.set_shader_parameter("base_albedo", Color(1, 1, 1))
	mat.set_shader_parameter("noise_amp", 0.0)
	mat.set_shader_parameter("snow_amount", 0.0)
	mat.set_shader_parameter("shadow_color", Color(0, 0, 0))
	mat.set_shader_parameter("shadow_strength", 0.0)
	(w["floor"] as MeshInstance3D).material_override = mat
	(w["wall"] as MeshInstance3D).material_override = mat

	await _settle(vp)
	var img: Image = vp.get_texture().get_image()
	img.save_png(out + "/ramp_known.png")
	var centre := Vector2i(RES.x / 2, RES.y / 2)
	var wall_px := cam.unproject_position(Vector3(0.0, 3.0, -4.0))

	var got_floor := img.get_pixelv(centre).r
	var got_wall := img.get_pixelv(Vector2i(int(wall_px.x), int(wall_px.y))).r
	# L in the shader points FROM the surface TOWARD the light, i.e. -ldir
	var L := -ldir
	var ndl_floor: float = Vector3(0, 1, 0).dot(L)
	var ndl_wall: float = Vector3(0, 0, 1).dot(L)
	report["ramp"] = {
		"_q": "does the shader's banded N.L equal the same arithmetic in GDScript",
		"light_dir": _v(ldir),
		"floor": {"ndl": snappedf(ndl_floor, 0.0001), "expect": snappedf(_band(ndl_floor), 0.001),
				  "got_srgb": snappedf(got_floor, 0.001),
				  "got_linear": snappedf(_srgb_to_lin(got_floor), 0.001)},
		"wall": {"ndl": snappedf(ndl_wall, 0.0001), "expect": snappedf(_band(ndl_wall), 0.001),
				 "got_srgb": snappedf(got_wall, 0.001),
				 "got_linear": snappedf(_srgb_to_lin(got_wall), 0.001)},
	}
	vp.queue_free()


# The SAME band arithmetic as the shader, written once here in GDScript. If these two
# disagree the shader is not doing what the design says, and that is the whole point.
const E0 := 0.34
const E1 := 0.62
const M0 := 0.30
const M1 := 0.66
const M2 := 1.00
const SOFT := 0.10


func _band(ndl: float) -> float:
	var t: float = ndl * 0.5 + 0.5
	var b: float = M0
	b += smoothstep(E0 - SOFT, E0 + SOFT, t) * (M1 - M0)
	b += smoothstep(E1 - SOFT, E1 + SOFT, t) * (M2 - M1)
	return b


const _RAMP_CODE := """
shader_type spatial;
render_mode diffuse_burley, specular_disabled;
uniform vec3 base_albedo : source_color = vec3(1.0);
uniform float e0 = 0.34;
uniform float e1 = 0.62;
uniform float m0 = 0.30;
uniform float m1 = 0.66;
uniform float m2 = 1.00;
uniform float soft = 0.10;
uniform float noise_amp = 0.0;
uniform float snow_amount = 0.0;
uniform vec3 shadow_color : source_color = vec3(0.0);
uniform float shadow_strength = 0.0;
void fragment() { ALBEDO = base_albedo; }
void light() {
	float t = dot(normalize(NORMAL), normalize(LIGHT)) * 0.5 + 0.5;
	float b = m0;
	b += smoothstep(e0 - soft, e0 + soft, t) * (m1 - m0);
	b += smoothstep(e1 - soft, e1 + soft, t) * (m2 - m1);
	vec3 lc = mix(shadow_color * shadow_strength, LIGHT_COLOR, b);
	DIFFUSE_LIGHT += ALBEDO * lc * ATTENUATION;
}
"""


func _srgb_to_lin(c: float) -> float:
	return c / 12.92 if c <= 0.04045 else pow((c + 0.055) / 1.055, 2.4)


func _enc(img: Image, px: Vector2i) -> Vector3:
	var c := img.get_pixelv(px)
	return Vector3(c.r * 2.0 - 1.0, c.g * 2.0 - 1.0, c.b * 2.0 - 1.0)


func _v(v: Vector3) -> Array:
	return [snappedf(v.x, 0.001), snappedf(v.y, 0.001), snappedf(v.z, 0.001)]


func _settle(vp: SubViewport) -> void:
	for i in 6:
		await process_frame
	RenderingServer.force_draw()
	await process_frame
