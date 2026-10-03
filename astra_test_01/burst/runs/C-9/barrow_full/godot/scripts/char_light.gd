extends RefCounted
class_name CharLight
## C-9 R-C9-139 -- CHARACTER LIGHT IN THE PAINTED BARROW (Matt: "all characters in the burrow ... are all too darkly lit.
## In the cliffside, Godot had the sun shine on them"). drax.
##
##   ?charlight=      (empty)  CURRENT: nothing here runs; the light setup is the shipped one, byte for byte
##   ?charlight=a     BRIGHTER SUN: the sun's lit term on the CHARACTERS ONLY x SUN_GAIN
##   ?charlight=b     SUN + FILL: (a)'s sun, plus a soft fill from the camera side and a thin rim on the sun's side
##   ?charlight=c     AMBIENT LIFT: the characters' ambient (the blue sky term) raised, no sun change
## (desktop: -- --charlight a|b|c)
##
## WHY NOT REAL LIGHTS. The characters wear the watercolour ramp (PaintStack.CHAR_SHADER), whose light() returns, PER LIGHT,
## mix(cool, warm, band) + ambient_in_light: the blue-violet shadow floor and (on the phone build) the whole ambient are
## added once for EVERY light that reaches the surface. A second light masked to the characters' layer (CHAR_LAYER 4) would
## add the floor and the ambient a second time -- a blue wash, not light -- and on Compatibility an unshadowed light is
## summed in a different, separately sRGB-encoded pass from the shadowed sun (the very split R-C9-83 moved the ambient into
## the sun's pass to undo). So the candidates are evaluated INSIDE the sun's pass, in the characters' OWN shader only:
##   SUN_GAIN   multiplies the sun's warm term (light_color / PI) -- exactly what raising the sun's energy would do, on
##              the characters alone; the cool floor and the ambient are untouched, the cast shadows still bite
##   FILL       a directional term from a fixed WORLD direction (camera side, low), wrapped, unshadowed: sky bounce
##   RIM        a thin edge on the sun's side (1 - N.V)^p x the sun's wrap: the "two suns, one direction" register holds
##   AMB_GAIN   scales ambient_in_light (phone) / adds the same linear ambient on the desktop
## Each guarded by LIGHT_IS_DIRECTIONAL (the sun is the only directional light that reaches CHAR_LAYER), so a VFX omni light
## on her does not add the fill twice. The painted world, the heather, the snow and the pen are never touched: only the
## ShaderMaterials adopt_character put on the characters (the scene's _char_saved) get the variant. No light is added.
## meteor_fx.gd derives its own fire variant from the LIVE code at attach() (after this runs): the two substrings its
## with_char_fire() asserts on are left intact.

const MODES := {
	"a": {"label": "brighter sun", "sun_gain": 2.0, "fill": 0.0, "rim": 0.0, "amb_gain": 1.0},
	"b": {"label": "sun + fill", "sun_gain": 1.6, "fill": 0.35, "rim": 0.40, "amb_gain": 1.0},
	"c": {"label": "ambient lift", "sun_gain": 1.0, "fill": 0.0, "rim": 0.0, "amb_gain": 3.0},
}
const FILL_COLOR := Color(1.0, 0.97, 0.93)       # neutral-warm bounce off the snow (linear, x fill)
const RIM_COLOR := Color(1.0, 0.955, 0.885)      # the winter sun's own colour (PaintStack.winter_sun)
const RIM_POWER := 3.0
const FILL_ELEV_DEG := 20.0                       # low: from just above the camera's line of sight

const UNIFORMS := """
uniform float cl_sun_gain = 1.0;
uniform vec3 cl_fill_dir = vec3(0.0, 1.0, 0.0);
uniform vec3 cl_fill_col = vec3(0.0);
uniform vec3 cl_rim_col = vec3(0.0);
uniform float cl_rim_power = 3.0;
uniform vec3 cl_amb_add = vec3(0.0);
"""
const LIGHT_ADD := """	if (LIGHT_IS_DIRECTIONAL) {
		vec3 cl_wn = normalize((INV_VIEW_MATRIX * vec4(NORMAL, 0.0)).xyz);
		float cl_f = clamp(dot(cl_wn, normalize(cl_fill_dir)) * 0.5 + 0.5, 0.0, 1.0);
		float cl_s = clamp(dot(normalize(NORMAL), normalize(LIGHT)) * 0.5 + 0.5, 0.0, 1.0);
		float cl_r = pow(1.0 - clamp(dot(normalize(NORMAL), normalize(VIEW)), 0.0, 1.0), cl_rim_power);
		DIFFUSE_LIGHT += cl_fill_col * cl_f * cl_f + cl_rim_col * cl_r * cl_s * ATTENUATION + cl_amb_add;
	}
"""
const TAIL := "	SPECULAR_LIGHT += web_sheen;      // the phone build's sky reflection; 0 on the desktop\n}\n"

static var _cache := {}


static func mode_of(arg: String) -> String:
	return arg if MODES.has(arg) else ""


static func variant_code(code: String) -> String:
	"""The characters' ramp code with the character-light terms. Asserts on what it edits."""
	var s := code
	assert(s.count("varying vec3 v_world;\n") == 1, "char_light: the char shader's varying moved")
	s = s.replace("varying vec3 v_world;\n", UNIFORMS + "varying vec3 v_world;\n")
	assert(s.count("vec3 warm = light_color / PI;") == 1, "char_light: the ramp's warm term moved")
	s = s.replace("vec3 warm = light_color / PI;", "vec3 warm = light_color / PI * cl_sun_gain;")
	assert(s.count(TAIL) == 1, "char_light: the ramp's light() tail moved")
	s = s.replace(TAIL, LIGHT_ADD + TAIL)
	return s


static func apply(scene: Node, mode: String) -> Dictionary:
	"""Put the mode on every character ramp material of the scene. "" = do nothing at all."""
	var rep := {"mode": mode if mode != "" else "current"}
	if mode == "" or not MODES.has(mode):
		return rep
	var p: Dictionary = MODES[mode]
	var saved: Dictionary = scene.get("_char_saved")
	var cam: Camera3D = scene.get("cam")
	# the fill: from the camera's side, low -- the camera's horizontal back vector, raised FILL_ELEV_DEG
	var back := cam.global_basis.z if cam != null else Vector3(0, 0, 1)
	back.y = 0.0
	back = back.normalized() if back.length() > 1e-6 else Vector3(0, 0, 1)
	var e := deg_to_rad(FILL_ELEV_DEG)
	var fdir := (back * cos(e) + Vector3.UP * sin(e)).normalized()
	var fill := Vector3(FILL_COLOR.r, FILL_COLOR.g, FILL_COLOR.b) * float(p["fill"])
	var rim := Vector3(RIM_COLOR.r, RIM_COLOR.g, RIM_COLOR.b) * float(p["rim"])
	var n := 0
	var amb_add := Vector3.ZERO
	var desk_amb := Vector3.ZERO
	var env_node = scene.get("env_node")
	if env_node != null and (env_node as WorldEnvironment).environment != null:
		var env: Environment = (env_node as WorldEnvironment).environment
		var a := env.ambient_light_color.srgb_to_linear() * env.ambient_light_energy
		desk_amb = Vector3(a.r, a.g, a.b)        # 0 on the phone path (move_ambient_into_light zeroed it)
	for ent in saved.get("meshes", []):
		var sm := ent.get("ramp") as ShaderMaterial
		if sm == null or sm.shader == null:
			continue
		var code: String = sm.shader.code
		if not code.contains("uniform float char_mark = 0.5;") or code.contains("cl_sun_gain"):
			continue
		if not _cache.has(code):
			var sh := Shader.new()
			sh.code = variant_code(code)
			_cache[code] = sh
		sm.shader = _cache[code]
		sm.set_shader_parameter("cl_sun_gain", float(p["sun_gain"]))
		sm.set_shader_parameter("cl_fill_dir", fdir)
		sm.set_shader_parameter("cl_fill_col", fill)
		sm.set_shader_parameter("cl_rim_col", rim)
		sm.set_shader_parameter("cl_rim_power", RIM_POWER)
		# THE AMBIENT LIFT: (amb_gain - 1) x the ambient the character already gets, added in the sun's pass once
		var have = sm.get_shader_parameter("ambient_in_light")
		var base: Vector3 = have if have is Vector3 and (have as Vector3).length() > 0.0 else desk_amb
		amb_add = base * (float(p["amb_gain"]) - 1.0)
		sm.set_shader_parameter("cl_amb_add", amb_add)
		n += 1
	rep.merge({"label": p["label"], "sun_gain": p["sun_gain"], "fill": p["fill"], "rim": p["rim"], "amb_gain": p["amb_gain"],
		"materials": n, "fill_dir": [snappedf(fdir.x, 1e-3), snappedf(fdir.y, 1e-3), snappedf(fdir.z, 1e-3)],
		"amb_add": [snappedf(amb_add.x, 1e-4), snappedf(amb_add.y, 1e-4), snappedf(amb_add.z, 1e-4)], "lights_added": 0})
	return rep


static func word(rep: Dictionary) -> String:
	"""The launch line's token: charlight=current | charlight=a(sun1.55,fill0.00,rim0.00,amb1.0,mats=N)"""
	if String(rep.get("mode", "current")) == "current":
		return "charlight=current"
	return "charlight=%s(sun%.2f,fill%.2f,rim%.2f,amb%.1f,mats=%d)" % [rep["mode"], float(rep["sun_gain"]), float(rep["fill"]),
		float(rep["rim"]), float(rep["amb_gain"]), int(rep["materials"])]
