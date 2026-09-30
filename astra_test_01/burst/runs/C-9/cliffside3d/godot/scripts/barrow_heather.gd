extends RefCounted
class_name BarrowHeather
## C-9 T10-1d -- HEATHER AS SPRIG SPRAYS, swayed by the wind and pushed aside by him.
##
## WHY NOT A BLOB. T10-1c's heather matched the painting's MEAN colour to dE 0.6 and still read
## as golden popcorn: round, bright, smooth, evenly spread. Against the painting's heather
## (tools/barrow_heather_stats.py) the blob's interior was too smooth (local std L* 8.4 against
## 11.2; edge density 0.33 against 0.51) and too saturated (chroma p50 29.7 against 21.8). A
## painted tuft is a SPRAY -- dark stems, rust sprig tips, snow between them. Two ways to draw
## one, built side by side and chosen by measurement (Matt / the coordinator, T10-1d):
##
##   STEMS  generated here: many thin curved stems, each ending in a few rust sprig tips, with
##          per-clump variation in count, height, spread and droop. Real silhouettes for the
##          depth/normal pen. ~700 triangles a clump.
##   CARDS  the painting's OWN tufts, cut out of the concept painting with their snow keyed to
##          alpha (tools/barrow_heather_cards.py), each drawn as one quad in the camera plane.
##          2 triangles a clump; alpha-scissored; no silhouette of their own for the pen.
##
## THE FIXED CAMERA IS WHAT MAKES BOTH CHEAP. The play and painting cameras share one direction
## (pitch 52.95354, yaw 47), and a heather instance carries no yaw -- so a stem's ribbon and a
## card's quad are BUILT facing that direction: no second crossed ribbon, no billboard maths in
## the vertex shader. Variety is VARIANTS generated clumps, a per-instance scale, and a
## per-instance tone.
##
## WIND AND PUSH ARE IN THE VERTEX SHADER, so they run inside the MultiMesh with nothing per
## instance on the CPU: a slow sway weighted by height squared with a per-clump phase, gusts
## travelling across the moor along the snow's own wind direction, and the SnowField's trail map
## sampled where each vertex stands -- stems bend away from where he has just waded and come
## back as the trail refills. One clock: the snow's (SnowField.clock()), so a captured film is
## deterministic and the heather and the snow tell the same time.

# (6, not 10: every variant is one more MultiMesh draw per chunk per pass)
const VARIANTS := 6
const SEGMENTS := 4
# THE BUDGET LEVER, measured (T10-1d): 44-70 stems with 3-5 tip sprigs and 1-3 side sprigs was
# ~1,200 triangles a tuft and 2.3-2.6 ms for the heather -- the frame at 17.1-17.7 ms. These
# are the counts that bring it under the line; the texture statistic is re-measured with them.
const STEMS_MIN := 30
const STEMS_MAX := 46
const SPRIGS_MAX := 4
const SIDE_MAX := 2
# the painting/play camera basis (barrow_paint_dress.py; R-C9-68)
const CAM_RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const CAM_UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const CAM_FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)

# LINEAR albedo, before the grade. Stems a dark weathered brown; sprig tips the painting's rust;
# a few tips carry snow crumbs, as the painted tufts do.
# (the base darker than the first pass: the painting's tufts are dark at the heart -- L p10 21
# against the stems' 32 -- and that dark is where their edges come from)
const STEM_COL := Color(0.085, 0.042, 0.018)
const STEM_TIP_COL := Color(0.30, 0.13, 0.040)
const SPRIG_COL := Color(0.45, 0.20, 0.050)
const SPRIG_COL_B := Color(0.36, 0.20, 0.070)
const CRUMB_COL := Color(0.80, 0.80, 0.82)

static var _spray := {}
static var _cards := {}
static var _shaders := {}


static func _hash01(i: int) -> float:
	return fposmod(sin(float(i) * 12.9898 + 78.233) * 43758.5453, 1.0)


static func _face_camera(a: Vector3, b: Vector3, c: Vector3) -> bool:
	"""True if (a, b, c) is a front face seen from the camera. Godot's front face is the
	clockwise one, whose geometric normal is (c - a) x (b - a) -- the same convention
	barrow_world._heather_core_mesh was checked against."""
	return (c - a).cross(b - a).dot(-CAM_FWD) > 0.0


static func _tri(st: Dictionary, a: int, b: int, c: int) -> void:
	var v: PackedVector3Array = st["v"]
	if _face_camera(v[a], v[b], v[c]):
		st["i"].append_array([a, b, c])
	else:
		st["i"].append_array([a, c, b])


static func _vert(st: Dictionary, p: Vector3, n: Vector3, col: Color, hf: float, rnd: float) -> int:
	st["v"].append(p)
	st["n"].append(n.normalized())
	st["c"].append(col)
	st["u2"].append(Vector2(hf, rnd))
	return st["v"].size() - 1


static func _ribbon(st: Dictionary, pts: Array, widths: Array, cols: Array, hmax: float,
		rnd: float, nrm: Vector3) -> void:
	"""A camera-facing strip along `pts`, `widths[k]` wide at node k."""
	var left := []
	var right := []
	for k in pts.size():
		var p: Vector3 = pts[k]
		var tng: Vector3
		if k == 0:
			tng = (pts[1] as Vector3) - p
		elif k == pts.size() - 1:
			tng = p - (pts[k - 1] as Vector3)
		else:
			tng = (pts[k + 1] as Vector3) - (pts[k - 1] as Vector3)
		var ax := tng.cross(CAM_FWD)
		if ax.length() < 1e-6:
			ax = CAM_RIGHT
		ax = ax.normalized() * float(widths[k]) * 0.5
		var hf := clampf(p.y / hmax, 0.0, 1.0)
		left.append(_vert(st, p - ax, nrm, cols[k], hf, rnd))
		right.append(_vert(st, p + ax, nrm, cols[k], hf, rnd))
	for k in pts.size() - 1:
		_tri(st, left[k], right[k], left[k + 1])
		_tri(st, right[k], right[k + 1], left[k + 1])


static func _leaf(st: Dictionary, p0: Vector3, p1: Vector3, w: float, col: Color, hmax: float,
		rnd: float, nrm: Vector3) -> void:
	"""A sprig: a thin diamond from p0 to p1, widest a third of the way out."""
	var d := p1 - p0
	var ax := d.cross(CAM_FWD)
	if ax.length() < 1e-6:
		ax = CAM_RIGHT
	ax = ax.normalized() * w * 0.5
	var m := p0 + d * 0.35
	var a := _vert(st, p0, nrm, col, clampf(p0.y / hmax, 0.0, 1.0), rnd)
	var b := _vert(st, m - ax, nrm, col, clampf(m.y / hmax, 0.0, 1.0), rnd)
	var c := _vert(st, m + ax, nrm, col, clampf(m.y / hmax, 0.0, 1.0), rnd)
	var e := _vert(st, p1, nrm, col, clampf(p1.y / hmax, 0.0, 1.0), rnd)
	_tri(st, a, b, c)
	_tri(st, b, e, c)


static func spray_mesh(variant: int) -> ArrayMesh:
	"""One generated tuft, height 1.0 (the instance's scale is its height in metres). LOW AND
	WIDE, as the painting's are -- its tufts measure 0.15-0.3 m tall and wider than tall; the
	first generator made tall thin sprays that read as dead grass (d_look1). Per variant:
	44-70 stems from a base 0.15-0.30 across its radius, leaning out 25-58 degrees (outer
	stems more), arcing over by a droop of 0.15-0.40, stem heights 50-100% of the tuft. Each
	stem ends in 3-5 rust sprigs and carries 1-3 more along its upper half; one sprig in
	fifteen holds a snow crumb."""
	if _spray.has(variant):
		return _spray[variant]
	var rng := RandomNumberGenerator.new()
	rng.seed = 7300 + variant * 131
	var st := {"v": PackedVector3Array(), "n": PackedVector3Array(), "c": PackedColorArray(),
			   "u2": PackedVector2Array(), "i": PackedInt32Array()}
	var n_stems := rng.randi_range(STEMS_MIN, STEMS_MAX)
	var rb := rng.randf_range(0.15, 0.30)
	var spread := deg_to_rad(rng.randf_range(25.0, 58.0))
	var droop := rng.randf_range(0.15, 0.40)
	var hmax := 1.0
	for s in n_stems:
		var ang := rng.randf() * TAU
		var rr := sqrt(rng.randf()) * rb
		var base := Vector3(cos(ang) * rr, 0.0, sin(ang) * rr)
		var out := Vector3(cos(ang), 0.0, sin(ang))
		var lean := spread * (0.3 + 0.7 * rr / rb) + rng.randf_range(-0.12, 0.12)
		var ld := (out + Vector3(rng.randf_range(-0.45, 0.45), 0.0, rng.randf_range(-0.45, 0.45))).normalized()
		var hs := rng.randf_range(0.50, 1.0)
		var dr := droop * rng.randf_range(0.5, 1.4)
		var rnd := rng.randf()
		var pts := []
		var widths := []
		var cols := []
		for k in SEGMENTS + 1:
			var t := float(k) / float(SEGMENTS)
			var along := t * hs
			var horiz := sin(lean) * along + dr * t * t * hs * 0.6
			var up := cos(lean) * along - dr * t * t * hs * 0.35
			pts.append(base + ld * horiz + Vector3(0.0, maxf(up, 0.0), 0.0))
			widths.append(lerpf(0.060, 0.026, t))
			cols.append(STEM_COL.lerp(STEM_TIP_COL, t * t))
		# a stem's lighting normal: up and toward the way it leans, so stems turned to the sun
		# land in the lit band and the rest do not -- the variation a painted tuft has
		var nrm := (Vector3.UP * 0.75 + ld * 0.55 - CAM_FWD * 0.25).normalized()
		_ribbon(st, pts, widths, cols, hmax, rnd, nrm)
		var tip: Vector3 = pts[SEGMENTS]
		var tdir: Vector3 = (tip - (pts[SEGMENTS - 1] as Vector3)).normalized()
		for q in rng.randi_range(3, SPRIGS_MAX):
			var lvec := (tdir + Vector3(rng.randf_range(-0.9, 0.9), rng.randf_range(-0.15, 0.7),
				rng.randf_range(-0.9, 0.9))).normalized()
			var p0 := tip - tdir * rng.randf_range(0.0, 0.07)
			var col := SPRIG_COL.lerp(SPRIG_COL_B, rng.randf())
			if rng.randf() < 1.0 / 15.0:
				col = CRUMB_COL
			_leaf(st, p0, p0 + lvec * rng.randf_range(0.10, 0.20), 0.075, col, hmax, rnd,
				(Vector3.UP * 0.8 + lvec * 0.4).normalized())
		for q in rng.randi_range(1, SIDE_MAX):
			var t2 := rng.randf_range(0.40, 0.90)
			var k2 := int(floor(t2 * SEGMENTS))
			var pa: Vector3 = (pts[k2] as Vector3).lerp(pts[mini(k2 + 1, SEGMENTS)], fposmod(t2 * SEGMENTS, 1.0))
			var sd := (ld + Vector3(rng.randf_range(-1.0, 1.0), rng.randf_range(0.2, 0.8),
				rng.randf_range(-1.0, 1.0))).normalized()
			_leaf(st, pa, pa + sd * rng.randf_range(0.08, 0.15), 0.065,
				SPRIG_COL.lerp(SPRIG_COL_B, rng.randf()), hmax, rnd, (Vector3.UP * 0.8 + sd * 0.4).normalized())
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = st["v"]
	arr[Mesh.ARRAY_NORMAL] = st["n"]
	arr[Mesh.ARRAY_COLOR] = st["c"]
	arr[Mesh.ARRAY_TEX_UV2] = st["u2"]
	arr[Mesh.ARRAY_INDEX] = st["i"]
	var am := ArrayMesh.new()
	am.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	_spray[variant] = am
	return am


static func card_mesh(tile: Dictionary) -> ArrayMesh:
	"""One painted tuft: a quad in the camera plane, `w_m` x `h_m` screen metres, its base at
	the origin -- the painting's own pixels at the painting's own scale. UV into the atlas
	tile; UV2.x the height fraction, for the sway."""
	var key := String(tile.get("name", str(tile)))
	if _cards.has(key):
		return _cards[key]
	var w: float = float(tile["w_m"])
	var h: float = float(tile["h_m"])
	var bx: float = float(tile.get("base_u", 0.5))      # where the tuft's base is, across the tile
	var uv0: Vector2 = Vector2(float(tile["uv"][0]), float(tile["uv"][1]))
	var uv1: Vector2 = Vector2(float(tile["uv"][2]), float(tile["uv"][3]))
	# a screen-metre step up the card is CAM_UP; a step across is CAM_RIGHT. The base sits on
	# the ground at the origin.
	var o := -CAM_RIGHT * (w * bx)
	var p00 := o
	var p10 := o + CAM_RIGHT * w
	var p01 := o + CAM_UP * h
	var p11 := o + CAM_RIGHT * w + CAM_UP * h
	var st := {"v": PackedVector3Array(), "n": PackedVector3Array(), "c": PackedColorArray(),
			   "u2": PackedVector2Array(), "i": PackedInt32Array()}
	var nrm := (Vector3.UP * 0.7 - CAM_FWD * 0.5).normalized()
	var hmax := maxf(p11.y, 1e-3)
	var a := _vert(st, p00, nrm, Color(1, 1, 1), 0.0, 0.0)
	var b := _vert(st, p10, nrm, Color(1, 1, 1), 0.0, 0.0)
	var c := _vert(st, p01, nrm, Color(1, 1, 1), clampf(p01.y / hmax, 0.0, 1.0), 0.0)
	var d := _vert(st, p11, nrm, Color(1, 1, 1), 1.0, 0.0)
	_tri(st, a, b, c)
	_tri(st, b, d, c)
	var uvs := PackedVector2Array([Vector2(uv0.x, uv1.y), Vector2(uv1.x, uv1.y),
								   Vector2(uv0.x, uv0.y), Vector2(uv1.x, uv0.y)])
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = st["v"]
	arr[Mesh.ARRAY_NORMAL] = st["n"]
	arr[Mesh.ARRAY_COLOR] = st["c"]
	arr[Mesh.ARRAY_TEX_UV] = uvs
	arr[Mesh.ARRAY_TEX_UV2] = st["u2"]
	arr[Mesh.ARRAY_INDEX] = st["i"]
	var am := ArrayMesh.new()
	am.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	_cards[key] = am
	return am


const _SHADER_HEAD := """
shader_type spatial;
render_mode specular_disabled, cull_back;
"""

const _SHADER_UNIFORMS := """
uniform vec3 albedo_mul = vec3(1.0);
uniform float tone_jitter = 0.28;
uniform float hue_jitter = 0.5;
uniform sampler2D mottle_noise : hint_default_white, filter_linear_mipmap, repeat_enable;
uniform float mottle_amp = 0.10;
uniform float mottle_scale = 2.6;
uniform float mesh_mark = 0.25;
uniform sampler2D card_tex : source_color, hint_default_white, filter_linear_mipmap, repeat_disable;
// wind: one clock with the snow
uniform float wind_on = 1.0;
uniform vec2 wind_dir = vec2(1.0, 0.0);
uniform float wind_time = 0.0;
// A FEW CM AT THE TIPS (the coordinator's "gentle"): the first film measured 1-3 cm and read
// as nearly still at the play camera's 1 cm a pixel -- 2 cm of sway, 5 cm in a gust front
uniform float sway_amp = 0.020;
uniform float sway_hz = 0.42;
uniform float gust_amp = 0.050;
uniform float gust_speed = 2.4;
// gust fronts ~2 m across (the fbm's base cell at this scale), crossing the patch in a second
uniform float gust_scale = 0.06;
uniform sampler2D gust_noise : hint_default_white, filter_linear_mipmap, repeat_enable;
// push-aside: the SnowField's trail map
uniform float push_on = 1.0;
uniform sampler2D trail_tex : filter_linear, repeat_disable;
uniform vec2 trail_min = vec2(0.0);
uniform vec2 trail_size = vec2(1.0);
uniform float trail_refill_s = 60.0;
uniform float push_amp = 0.26;
uniform float push_sink = 0.50;
// HIS LEGS ARE WIDER THAN HIS PRINTS: the trail stamps each boot (~22 x 10 cm), and a man
// wading through heather parts it across his stride -- so the press is read as the max over
// a cross of taps this far apart, fading to push_arm at the arms. (0.16 m / 0.6 pushed 10 of
// the 32 clumps along his line and read as barely there in the film; his legs sweep ~0.5 m)
uniform float push_reach_m = 0.26;
uniform float push_arm = 0.85;
varying vec3 v_world;
varying vec3 v_col;
varying float v_rnd;
"""

const _SHADER_FUNCS := """
float _press(vec2 uv) {
	vec4 t = textureLod(trail_tex, uv, 0.0);
	float fade = clamp(1.0 - (wind_time - t.g) / max(trail_refill_s, 1e-3), 0.0, 1.0);
	return clamp(t.r * fade, 0.0, 1.0);
}

void vertex() {
	vec3 origin = MODEL_MATRIX[3].xyz;
	float s = max(length(MODEL_MATRIX[0].xyz), 1e-4);
	float hf = UV2.x;
	v_rnd = fract(sin(dot(origin.xz, vec2(12.9898, 78.233))) * 43758.5453);
	vec3 wp = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	vec3 d = vec3(0.0);
	if (hf > 0.02) {
		// WIND: a slow sway, phase per clump and per stem, weighted by height squared; and
		// GUSTS -- low-frequency noise travelling across the moor along wind_dir
		vec2 gp = (wp.xz - wind_dir * wind_time * gust_speed) * gust_scale;
		float g = smoothstep(0.42, 0.72, textureLod(gust_noise, gp, 0.0).r);
		float sw = sin(wind_time * 6.2831853 * sway_hz + v_rnd * 6.2831853 + UV2.y * 2.1);
		float amp = (sway_amp * (0.55 + 0.45 * sw) + gust_amp * g) * wind_on;
		d.xz += wind_dir * amp * hf * hf;
		// PUSH-ASIDE: where he has just waded, away from the track and down; back as it refills
		if (push_on > 0.5) {
			vec2 uv = (wp.xz - trail_min) / trail_size;
			vec2 e = vec2(push_reach_m) / trail_size;
			float pc = _press(uv);
			float px0 = _press(uv - vec2(e.x, 0.0));
			float px1 = _press(uv + vec2(e.x, 0.0));
			float pz0 = _press(uv - vec2(0.0, e.y));
			float pz1 = _press(uv + vec2(0.0, e.y));
			float p = max(pc, push_arm * max(max(px0, px1), max(pz0, pz1)));
			if (p > 0.002) {
				vec2 gr = vec2(px1 - px0, pz1 - pz0);
				vec2 away = length(gr) > 1e-4 ? -normalize(gr) : normalize(wp.xz - origin.xz + vec2(1e-4, 0.0));
				float hl = max(wp.y - origin.y, 0.0);
				d.xz += away * push_amp * p * hf;
				d.y -= push_sink * p * hl;
			}
		}
		// keep a stem's length: a tip swung sideways by L drops by about L^2 / (2 h)
		float hh = max(wp.y - origin.y, 1e-3);
		d.y -= dot(d.xz, d.xz) / (2.0 * hh);
	}
	VERTEX += d / s;
	v_world = wp + d;
	v_col = COLOR.rgb;
}
"""

const _FRAG_STEMS := """
void fragment() {
	vec3 base = v_col * albedo_mul;
	float tj = v_rnd - 0.5;
	base *= 1.0 + tj * tone_jitter;
	// per clump, a slide between the painting's rust and an olive-brown (less red, less blue --
	// the first version pushed blue and greyed half the clumps)
	base = mix(base, base * vec3(0.90, 1.0, 0.78), clamp(0.5 - v_rnd, 0.0, 0.5) * hue_jitter * 2.0);
	float m = texture(mottle_noise, v_world.xz * mottle_scale).r;
	base *= (1.0 - mottle_amp * 0.5 + m * mottle_amp);
	ALBEDO = base;
	ROUGHNESS = mesh_mark;
}
"""

const _FRAG_CARDS := """
void fragment() {
	vec4 tx = texture(card_tex, UV);
	vec3 base = tx.rgb * albedo_mul;
	float tj = v_rnd - 0.5;
	base *= 1.0 + tj * tone_jitter;
	base = mix(base, base * vec3(0.90, 1.0, 0.78), clamp(0.5 - v_rnd, 0.0, 0.5) * hue_jitter * 2.0);
	ALBEDO = base;
	ALPHA = tx.a;
	ALPHA_SCISSOR_THRESHOLD = 0.5;
	ROUGHNESS = mesh_mark;
}
"""

# THE WEB CARD: cut out, and writing NO depth. On the phone build the pen is depth-only (no
# normal-roughness buffer on Compatibility, so no "thin" mark to turn it down on growth), and a
# card that writes depth is a depth break on every sprig's edge -- the pen would outline each
# tuft in full ink. So the card writes colour and no depth.
#
# A DEPTHLESS MATERIAL IS DRAWN IN THE TRANSPARENT PASS, whatever its alpha (Godot routes
# depth_draw_never there), which is AFTER the post pass has copied the screen -- and the post
# pass, the last transparent at render_priority 120, then painted that copy straight over every
# card: 0 heather on screen with 650 instances in the scene, in the first phone-size test, and
# again with the card cut out instead of blended. So the scene draws the web cards AFTER the
# post pass (BarrowWorld.WEB_CARD_PRIORITY, above 120): occluded by the world's depth as before,
# and outside the grade and the paper grain, which they do not get.
const _HEAD_DEPTHLESS := """
shader_type spatial;
render_mode specular_disabled, cull_back, depth_draw_never;
"""

const _FRAG_CARDS_DEPTHLESS := """
void fragment() {
	vec4 tx = texture(card_tex, UV);
	vec3 base = tx.rgb * albedo_mul;
	float tj = v_rnd - 0.5;
	base *= 1.0 + tj * tone_jitter;
	base = mix(base, base * vec3(0.90, 1.0, 0.78), clamp(0.5 - v_rnd, 0.0, 0.5) * hue_jitter * 2.0);
	ALBEDO = base;
	ALPHA = tx.a;
	ALPHA_SCISSOR_THRESHOLD = 0.5;
}
"""

const _LIGHT := """
void light() {
	DIFFUSE_LIGHT += _ramp_light(NORMAL, LIGHT, ATTENUATION, LIGHT_COLOR, v_world, wash_noise,
		band_e0, band_e1, band_m0, band_m1, band_m2, band_soft, wash_amp, wash_scale,
		shadow_bite, shadow_color, shadow_energy, ramp_mix);
}
"""


static func shader(cards: bool, depthless := false) -> Shader:
	var key := ("cards_depthless" if depthless else "cards") if cards else "stems"
	if _shaders.has(key):
		return _shaders[key]
	var sh := Shader.new()
	var head := _HEAD_DEPTHLESS if (cards and depthless) else _SHADER_HEAD
	var frag := (_FRAG_CARDS_DEPTHLESS if depthless else _FRAG_CARDS) if cards else _FRAG_STEMS
	sh.code = head + PaintStack.RAMP_UNIFORMS + _SHADER_UNIFORMS + PaintStack.RAMP_BODY \
		+ _SHADER_FUNCS + frag + _LIGHT
	_shaders[key] = sh
	return sh


static func material(fbm: Texture2D, cards: bool, params := {}, depthless := false) -> ShaderMaterial:
	var m := ShaderMaterial.new()
	m.shader = shader(cards, depthless)
	m.set_shader_parameter("wash_noise", fbm)
	m.set_shader_parameter("mottle_noise", fbm)
	m.set_shader_parameter("gust_noise", fbm)
	for k in params:
		m.set_shader_parameter(k, params[k])
	return m


static func bind_snow(m: ShaderMaterial, snow: SnowField, wind: Vector2) -> void:
	"""The trail map and its clock, and the wind the drifts were blown by."""
	m.set_shader_parameter("wind_dir", wind.normalized())
	if snow == null:
		m.set_shader_parameter("push_on", 0.0)
		return
	m.set_shader_parameter("trail_tex", snow.trail_texture())
	m.set_shader_parameter("trail_min", snow.area.position)
	m.set_shader_parameter("trail_size", snow.area.size)
	m.set_shader_parameter("trail_refill_s", snow.trail_refill_s)
