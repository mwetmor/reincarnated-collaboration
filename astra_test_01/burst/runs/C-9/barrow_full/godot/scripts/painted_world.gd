extends RefCounted
class_name PaintedWorld
## C-9 T10-2 step 4 -- THE PAINTING IS THE WORLD'S LIGHT AND ITS INK (the conductor's ruling).
##
##   STATIC PAINTED PIECES (the 54 heroes, the birches, the painted ground) show the painting as
##     painted: no ramp, no pen. Their outline ink is in the plate already.
##   DYNAMIC THINGS (him, later the monsters, the heather, the snow's trails, particles) keep the
##     ramp under the same sun, and the pen.
##   WHERE THEY MEET: (a) his shadow darkens the painted world; (b) he is darkened inside a
##     painted shadow; (c) static pieces cast no real shadow onto the painted world.
##
## THE MECHANISM, MEASURED FIRST (tools/probe_paint_light.gd, work/probe/probe_paint_light.json):
## TWO SUNS, ONE DIRECTION. Godot 4.6's Light3D.shadow_caster_mask is independent of its cull mask:
##   the SUN (light A) lights everything but the painted layers, and every caster shadows it --
##     so a ring stone's shadow falls on HIM (b), with the geometry the painter painted over;
##   the PAINT SUN (light B) lights ONLY the painted layers, and ONLY he casts for it -- so his
##     shadow is the one shadow the painted world receives (a), and no stone shadows it (c).
## Probe: painted receiver under a static caster 0.737 (unshadowed) / under him 0.459; dynamic
## receiver under a static caster 0.486; a block on his layer lit by A only (G = 0).
##
## THE PAINTED SURFACE is unlit paint times ONE term: his shadow, as the PAINTER'S shadow -- the
## painting's own shadow colour over its own light (shadow_mul, measured off the painting by
## tools/paint_world_prep.py) -- and only where the painting shows direct sun (lit_map, rendered
## from the blockout's own sun by tools/capture_light.gd): a shadow falling into a painted shadow
## adds nothing, as a real one would not.
##
## THE PROJECTION. The play camera never turns (pitch 52.95354, yaw 47, orthographic), so the
## painting is the complete view of every static surface. A fragment's guide pixel is analytic:
##   x = (u - u0) * ppm ;  y = (v1 - v) * ppm sin(pitch) - h * ppm cos(pitch)
## and a projected piece wears the painting at exactly the pixel the camera sees it at.

const LAYER_PAINTED := 1 << 10       # the static painted pieces: lit by the paint sun only
const LAYER_ON_PAINT := 1 << 11      # dynamic things that wear the painting (heather, the snow)
const ALL_LAYERS := (1 << 20) - 1
const PAINTED_MARK := 0.0            # the pen's mark channel (paint_stack POST_SHADER)
const DATA := "res://data/painted/"
const MANIFEST := "res://data/painted/manifest.json"

const GUIDE_PX := Vector2(5376.0, 3328.0)
const U0 := -28.715
const V1 := 17.7203
const PPM := 100.617553710938
const PITCH_DEG := 52.95354112560294

const PROJ_UNIFORMS := """
uniform vec3 g_u_hat = vec3(0.681998, 0.0, -0.731354);
uniform vec3 g_v_hat = vec3(-0.731354, 0.0, -0.681998);
uniform vec3 g_frame = vec3(-28.715, 17.7203, 100.617553710938);   // u0, v1, px per metre
uniform vec2 g_px_per = vec2(80.3076, 60.6183);                     // ppm sin(pitch), ppm cos(pitch)
uniform vec2 g_size = vec2(5376.0, 3328.0);
// the painting's DIRECT SUN share, in guide space: 1 where the painter painted sunlight, 0 in a
// painted shadow (cast or turned away). His shadow darkens by it.
uniform sampler2D lit_map : filter_linear, repeat_disable;
// the painter's shadow over the painter's light, LINEAR, per channel (measured on open snow)
uniform vec3 shadow_mul = vec3(0.4, 0.46, 0.63);
uniform float his_shadow_on = 1.0;
"""

const PROJ_FUNCS := """
vec2 guide_uv(vec3 p) {
	float u = dot(p, g_u_hat);
	float v = dot(p, g_v_hat);
	return vec2((u - g_frame.x) * g_frame.z, (g_frame.y - v) * g_px_per.x - p.y * g_px_per.y) / g_size;
}

vec3 his_shadow(float att, vec3 wpos) {
	float lit = textureLod(lit_map, guide_uv(wpos), 0.0).r;
	return mix(vec3(1.0), shadow_mul, clamp((1.0 - att) * lit * his_shadow_on, 0.0, 1.0));
}
"""

# THE PAINTED SURFACE. ambient_light_disabled: the environment adds nothing, so the pixel is the
# paint times the paint sun's one term. The paint sun's LIGHT_COLOR is never read -- the painting
# is the light; only its ATTENUATION (his shadow) is.
const PAINTED_SHADER := """
shader_type spatial;
render_mode ambient_light_disabled, specular_disabled, cull_back, fog_disabled;
""" + PROJ_UNIFORMS + """
uniform sampler2D paint_tex : source_color, filter_linear_mipmap, repeat_disable;
uniform bool project_uv = true;      // true: the guide projection; false: the mesh's own UV (a bake)
uniform float painted_mark = 0.0;
uniform bool id_black = false;      // the overlay's heather-mask pass: the painted world drawn black
varying vec3 v_world;
""" + PROJ_FUNCS + """
void vertex() {
	v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
}

void fragment() {
	ALBEDO = id_black ? vec3(0.0) : texture(paint_tex, project_uv ? guide_uv(v_world) : UV).rgb;
	ROUGHNESS = painted_mark;
}

void light() {
	DIFFUSE_LIGHT += his_shadow(ATTENUATION, v_world);
}
"""

static var _shaders := {}


static func _shader(key: String, code: String) -> Shader:
	if not _shaders.has(key):
		var sh := Shader.new()
		sh.code = code
		_shaders[key] = sh
	return _shaders[key]


static func bind_projection(m: ShaderMaterial, lit: Texture2D, shadow_mul: Vector3, u_hat: Vector3,
		v_hat: Vector3) -> void:
	"""The guide camera and his shadow's two inputs, onto any material built on PROJ_UNIFORMS.
	u_hat and v_hat are the LIVE ground basis the scene built in (residual to the analytic one
	~1e-7, reported by the scene)."""
	var p := deg_to_rad(PITCH_DEG)
	m.set_shader_parameter("g_u_hat", u_hat)
	m.set_shader_parameter("g_v_hat", v_hat)
	m.set_shader_parameter("g_frame", Vector3(U0, V1, PPM))
	m.set_shader_parameter("g_px_per", Vector2(PPM * sin(p), PPM * cos(p)))
	m.set_shader_parameter("g_size", GUIDE_PX)
	m.set_shader_parameter("lit_map", lit)
	m.set_shader_parameter("shadow_mul", shadow_mul)


static func painted_material(tex: Texture2D, project: bool, lit: Texture2D, shadow_mul: Vector3,
		u_hat: Vector3, v_hat: Vector3) -> ShaderMaterial:
	var m := ShaderMaterial.new()
	m.shader = _shader("painted", PAINTED_SHADER)
	m.set_shader_parameter("paint_tex", tex)
	m.set_shader_parameter("project_uv", project)
	m.set_shader_parameter("painted_mark", PAINTED_MARK)
	bind_projection(m, lit, shadow_mul, u_hat, v_hat)
	return m


# --- the snow: the installed field, the painting as its albedo, relit where he has moved it ------
static func _swap(code: String, a: String, b: String, what: String) -> String:
	"""A replacement that finds nothing FAILS: the snow shader is derived from the installed one,
	and a derivation that silently stopped applying would ship the installed look unannounced."""
	assert(code.count(a) == 1, "snow_shader_code: '%s' found %d times, not once" % [what, code.count(a)])
	return code.replace(a, b)


static func snow_shader_code() -> String:
	"""SnowField.SHADER, four edits, each asserted:
	  1. no ambient, no fog: the painting is the light (as PAINTED_SHADER);
	  2. the projection uniforms and the painting;
	  3. the albedo is the painting at the surface's own guide pixel, with the snow's own PRESS
	     tint on his trail only (the trodden path is the painting's already);
	  4. RELIT, NOT LIT: the ramp at the surface's normal NOW over the ramp at its UNDISTURBED
	     normal -- exactly 1 on untouched snow, so the painting shows as painted; his prints and
	     berms take the ramp's light and dark where he has moved the surface -- times his shadow."""
	var s: String = SnowField.SHADER
	s = _swap(s, "render_mode specular_disabled, cull_back;",
		"render_mode specular_disabled, cull_back, ambient_light_disabled, fog_disabled;", "render_mode")
	s = _swap(s, "varying float v_press;\n", "varying float v_press;\n" + PROJ_UNIFORMS
		+ "uniform sampler2D paint_tex : source_color, filter_linear_mipmap, repeat_disable;\n", "varyings")
	s = _swap(s, "// ONE definition of the snow's height", PROJ_FUNCS + "\n// ONE definition of the snow's height",
		"snow_h head")
	s = _swap(s, "	ALBEDO = id_black ? vec3(0.0) : base;\n",
		"""	vec3 pb = texture(paint_tex, guide_uv(v_world)).rgb;
	pb = mix(pb, pb * press_tint, clamp(p, 0.0, 1.0) * press_tint_amt);
	ALBEDO = id_black ? vec3(0.0) : pb;
""", "albedo")
	var i := s.find("void light() {")
	assert(i > 0, "snow_shader_code: no light() in SnowField.SHADER")
	s = s.substr(0, i) + """void light() {
	vec4 f0 = textureLod(field_tex, v_uv, 0.0);
	vec3 n0 = normalize((VIEW_MATRIX * vec4(normalize(vec3(-f0.b, 1.0, -f0.a)), 0.0)).xyz);
	vec3 now = _ramp_light(NORMAL, LIGHT, 1.0, LIGHT_COLOR, v_world, wash_noise,
		band_e0, band_e1, band_m0, band_m1, band_m2, band_soft, wash_amp, wash_scale,
		shadow_bite, shadow_color, shadow_energy, ramp_mix);
	vec3 ref = _ramp_light(n0, LIGHT, 1.0, LIGHT_COLOR, v_world, wash_noise,
		band_e0, band_e1, band_m0, band_m1, band_m2, band_soft, wash_amp, wash_scale,
		shadow_bite, shadow_color, shadow_energy, ramp_mix);
	vec3 relit = clamp(now / max(ref, vec3(1e-3)), vec3(0.0), vec3(2.0));
	DIFFUSE_LIGHT += relit * his_shadow(ATTENUATION, v_world);
}
"""
	return s


# --- the heather: BarrowHeather's sprays and wind, coloured from the painting beneath ------------
static func heather_shader_code() -> String:
	"""BarrowHeather's stems, its wind and his push-aside unchanged; two things differ:
	  the colour: v_col (the spray's own dark-stem-to-rust ramp) times albedo_mul (one grade,
	    measured by the overlay) times INSTANCE_CUSTOM -- the painting beneath THIS spray, over
	    the mean of all of them, so a tuft the painter put in shadow is a darker, bluer spray;
	  the light: the ramp for its FORM only (att 1 -- no stone shadows it, the painting has them),
	    times his shadow as the painter's shadow, where the painting shows sun."""
	var vfun: String = BarrowHeather._SHADER_FUNCS
	assert(vfun.count("v_col = COLOR.rgb;") == 1, "heather: the vertex colour line moved")
	vfun = vfun.replace("v_col = COLOR.rgb;", "v_col = COLOR.rgb;\n\tv_mul = INSTANCE_CUSTOM.rgb;")
	return BarrowHeather._SHADER_HEAD + PaintStack.RAMP_UNIFORMS + BarrowHeather._SHADER_UNIFORMS \
		+ PROJ_UNIFORMS + "varying vec3 v_mul;\nuniform bool id_white = false;\n" + PaintStack.RAMP_BODY \
		+ PROJ_FUNCS + vfun + """
void fragment() {
	vec3 base = v_col * albedo_mul * v_mul;
	float m = texture(mottle_noise, v_world.xz * mottle_scale).r;
	base *= (1.0 - mottle_amp * 0.5 + m * mottle_amp);
	ALBEDO = id_white ? vec3(0.0) : base;
	EMISSION = id_white ? vec3(1.0) : vec3(0.0);
	ROUGHNESS = mesh_mark;
}

void light() {
	DIFFUSE_LIGHT += _ramp_light(NORMAL, LIGHT, 1.0, LIGHT_COLOR, v_world, wash_noise,
		band_e0, band_e1, band_m0, band_m1, band_m2, band_soft, wash_amp, wash_scale,
		shadow_bite, shadow_color, shadow_energy, ramp_mix) * his_shadow(ATTENUATION, v_world);
}
"""


static func heather_material(fbm: Texture2D, albedo_mul: Vector3, lit: Texture2D, shadow_mul: Vector3,
		u_hat: Vector3, v_hat: Vector3) -> ShaderMaterial:
	var m := ShaderMaterial.new()
	m.shader = _shader("heather", heather_shader_code())
	m.set_shader_parameter("wash_noise", fbm)
	m.set_shader_parameter("mottle_noise", fbm)
	m.set_shader_parameter("gust_noise", fbm)
	m.set_shader_parameter("albedo_mul", albedo_mul)
	m.set_shader_parameter("mesh_mark", 0.25)
	bind_projection(m, lit, shadow_mul, u_hat, v_hat)
	return m


# --- loading, from the pck, with proof --------------------------------------------------------
static func read_manifest() -> Dictionary:
	if not FileAccess.file_exists(MANIFEST):
		return {}
	var j = JSON.parse_string(FileAccess.get_file_as_string(MANIFEST))
	return j if typeof(j) == TYPE_DICTIONARY else {}


static func load_png_bin(rel: String, want_sha: String, mipmaps: bool, rep: Dictionary) -> ImageTexture:
	"""An image off its RAW bytes (a PNG named .bin: the importer never sees it, so nothing is
	re-compressed, and an include_filter ships the file itself), its sha256 checked against the
	manifest. `rep[rel]` says what happened -- the app's launch line is built from these."""
	var path := DATA + rel
	var r := {"path": path}
	rep[rel] = r
	if not FileAccess.file_exists(path):
		r["error"] = "missing"
		return null
	var bytes := FileAccess.get_file_as_bytes(path)
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(bytes)
	var sha := ctx.finish().hex_encode()
	r["sha256_ok"] = sha == want_sha
	r["bytes"] = bytes.size()
	var img := Image.new()
	var err := img.load_png_from_buffer(bytes)
	if err != OK:
		r["error"] = "decode %d" % err
		return null
	r["px"] = [img.get_width(), img.get_height()]
	if mipmaps:
		img.generate_mipmaps()
	return ImageTexture.create_from_image(img)


static func load_f32_bin(rel: String, want_sha: String, rep: Dictionary) -> PackedFloat32Array:
	var path := DATA + rel
	var r := {"path": path}
	rep[rel] = r
	if not FileAccess.file_exists(path):
		r["error"] = "missing"
		return PackedFloat32Array()
	var bytes := FileAccess.get_file_as_bytes(path)
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(bytes)
	r["sha256_ok"] = ctx.finish().hex_encode() == want_sha
	r["bytes"] = bytes.size()
	return bytes.to_float32_array()
