extends RefCounted
class_name PaintStack
## C-9 T10 — THE RENDER STACK: what makes a generated world and a painted barbarian one picture.
##
## The barbarian reads as the best artwork this project has produced because every part of
## him obeys one set of rules (T10 verdict § 1). Two of those rules are not his: they are
## the RENDERER's, and they have to be the same renderer for him and for the ground he
## stands on.
##
##   rule 3 — ONE REAL LIGHT. One low winter sun, one sky ambient, and the SAME custom
##            lighting response on the world and on him. Not two shading models that
##            happen to be lit from the same angle.
##   rule 4 — ONE INK LINE. One colour, one weight, whether it is drawn by the hull pass
##            on a character or by the screen-space pass on terrain.
##
## Everything here is GENERATED. No purchased texture, no purchased shader, no kit: the
## noise, the paper grain and the snowflake are built pixel by pixel in _periodic_fbm and
## its neighbours, which also means the SNOW LAYER'S MEASUREMENT can sample the very image
## the GPU samples instead of a re-implementation of it that might disagree.
##
## ─────────────────────────────────────────────────────────────────────────────
## THREE THINGS MEASURED BEFORE ANY OF THIS WAS WRITTEN (tools/probe_gfx.gd, probe_gfx2.gd)
##
## 1. light()'s OUTPUT IS MULTIPLIED BY ALBEDO BY THE ENGINE. A light() writing a constant
##    0.25 onto a surface with ALBEDO 0.5 reads back 0.125. So `DIFFUSE_LIGHT += ALBEDO *
##    ...`, which is what the obvious reading of the docs produces, SQUARES THE PAINT --
##    every texture comes back darker and more saturated than it was painted, worst in the
##    midtones, and it looks like a bad ramp rather than a double multiply. The ramp below
##    therefore writes LIGHT ONLY and never touches ALBEDO.
##
## 2. LIGHT_COLOR CARRIES A FACTOR OF PI. `LIGHT_COLOR * 0.25` from a unit-energy white sun
##    read back 0.392, i.e. LIGHT_COLOR = 3.14. It is the Lambert 1/pi folded into the
##    light. Used raw it is three times overbright, and the fix is not to turn the sun down
##    -- that moves the shadow ramp too. Divided by PI here, so `light_energy` means what
##    it looks like it means.
##
## 3. hint_normal_roughness_texture IS IN VIEW SPACE (floor normal matched the view-space
##    normal to 0.005, the world-space one to 1.04). A Roberts cross does not care, but
##    "is this surface facing UP" does, so THE SNOW LAYER READS A WORLD NORMAL VARYING FROM
##    THE OBJECT'S OWN SHADER and never the screen buffer. A snow layer built on the screen
##    normal would look correct from exactly one camera angle.
##
## And the reading error that produced all three: an 8-bit render target stores sRGB. The
## first pass of probe_gfx read Image.get_pixel and treated the byte as the linear value the
## shader wrote, which made a correct normal buffer and a correct depth buffer both look
## broken. _srgb_to_linear below is not a convenience; it is the instrument.
## ─────────────────────────────────────────────────────────────────────────────

# THE ONE PEN. Dark warm brown, per the T10 brief. The barbarian's hull line shipped as
# vec4(0.055, 0.043, 0.063) -- a cool near-black -- so his line is RE-TINTED to this from
# outside (see retint_character_ink), which is also what keeps the two lines inside ΔE 5:
# they are not matched, they are the same number.
const INK := Color(0.113, 0.082, 0.067)
const PPM := 100.617553710938
const TERRAIN_BIT := 1 << 1        # knight.gd masks its ground ray to this; do not renumber

# --- the shared ramp, as source ------------------------------------------------
# Used verbatim by both the world shader and the character shader, so there is exactly ONE
# definition of how this project turns N.L into paint.
const RAMP_UNIFORMS := """
uniform vec3 shadow_color : source_color = vec3(0.34, 0.37, 0.56);
uniform float shadow_energy = 0.62;
uniform float band_e0 = 0.47;
uniform float band_e1 = 0.70;
uniform float band_m0 = 0.10;
uniform float band_m1 = 0.56;
uniform float band_m2 = 1.00;
uniform float band_soft = 0.085;
uniform float wash_amp = 0.17;
uniform float wash_scale = 0.62;
uniform float shadow_bite = 1.0;
uniform float ramp_mix = 1.0;
uniform sampler2D wash_noise : hint_default_white, filter_linear_mipmap, repeat_enable;
"""

const RAMP_BODY := """
float _fbm2(sampler2D t, vec2 p) {
	return texture(t, p).r * 0.62 + texture(t, p * 2.17 + vec2(0.31, 0.77)).r * 0.38;
}

// THE WATERCOLOUR RAMP. Two soft edges through three levels, and the edges are BROKEN BY
// A WORLD-ANCHORED NOISE so a transition blooms across a surface the way a wet wash does
// instead of stepping cleanly the way a toon ramp does. World-anchored and not screen- or
// UV-anchored: the wash belongs to the rock, so it does not crawl when the camera moves
// and it does not stretch where the terrain's UVs stretch.
vec3 _ramp_light(vec3 n, vec3 l, float att, vec3 light_color, vec3 wpos, sampler2D wn,
		float e0, float e1, float m0, float m1, float m2, float soft,
		float amp, float scale, float bite, vec3 sh_col, float sh_e, float mix_amt) {
	float ndl = dot(normalize(n), normalize(l));
	float raw = ndl * 0.5 + 0.5;                       // wrapped, so the dark side is a value not a void
	float w = _fbm2(wn, wpos.xz * scale + wpos.y * vec2(0.21, 0.13));
	// The shadow multiplies BEFORE the bands, so a cast shadow lands on the same band a
	// surface facing away lands on. A painter has one shadow value, not one for form and
	// another for cast.
	float t = raw * mix(1.0, att, bite) + (w - 0.5) * amp;
	float b = m0;
	b += smoothstep(e0 - soft, e0 + soft, t) * (m1 - m0);
	b += smoothstep(e1 - soft, e1 + soft, t) * (m2 - m1);
	vec3 warm = light_color / PI;                      // see note 2: LIGHT_COLOR carries a PI
	vec3 cool = sh_col * sh_e;                         // shadow is BLUE-VIOLET, never black
	vec3 ramped = mix(cool, warm, clamp(b, 0.0, 1.0));
	vec3 plain = (light_color / PI) * max(ndl, 0.0) * att;
	return mix(plain, ramped, mix_amt);                // mix_amt 0 == the stack OFF, for A/B
}
"""

# --- the world surface --------------------------------------------------------
const WORLD_SHADER := """
shader_type spatial;
render_mode specular_disabled, cull_back;
""" + RAMP_UNIFORMS + """
uniform vec3 base_color : source_color = vec3(0.44, 0.42, 0.47);
uniform sampler2D albedo_tex : source_color, hint_default_white, filter_linear_mipmap, repeat_enable;
uniform bool use_tex = false;
uniform float tex_scale = 1.0;
uniform sampler2D mottle_noise : hint_default_white, filter_linear_mipmap, repeat_enable;
uniform float mottle_amp = 0.13;
uniform float mottle_scale = 0.33;
uniform float hatch_amp = 0.05;
uniform float hatch_scale = 5.5;
// the snow layer: world-space, on terrain AND props, so a generated asset and the ground
// agree about where snow settles without either knowing about the other
uniform float snow_amount = 1.0;
uniform vec3 snow_color : source_color = vec3(0.800, 0.828, 0.876);
uniform float snow_threshold = 0.58;
uniform float snow_jitter = 0.30;
uniform float snow_soft = 0.13;
uniform float snow_noise_scale = 0.85;
uniform float snow_mottle = 0.09;
varying vec3 v_world;
varying vec3 v_wnormal;
""" + RAMP_BODY + """
void vertex() {
	v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	v_wnormal = normalize((MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz);
}

float snow_coverage(vec3 wpos, vec3 wn, sampler2D mn, float thr, float jit, float soft,
		float nscale, float amount) {
	float up = dot(normalize(wn), vec3(0.0, 1.0, 0.0));
	float sn = _fbm2(mn, wpos.xz * nscale + vec2(11.3, 4.7));
	float t = thr + (sn - 0.5) * jit;
	return smoothstep(t, t + soft, up) * clamp(amount, 0.0, 1.0);
}

void fragment() {
	vec3 base = use_tex ? texture(albedo_tex, UV * tex_scale).rgb : base_color;
	// a flat colour reads as a wash, not as plastic: low-frequency value break plus a
	// faint cross-hatch at the scale a pen would hatch
	float m = _fbm2(mottle_noise, v_world.xz * mottle_scale + v_world.y * 0.17);
	base *= (1.0 - mottle_amp * 0.5 + m * mottle_amp);
	float h = texture(mottle_noise, v_world.xz * hatch_scale + vec2(0.5, 0.17)).r;
	base *= (1.0 - hatch_amp * 0.5 + h * hatch_amp);
	float k = snow_coverage(v_world, v_wnormal, mottle_noise, snow_threshold, snow_jitter,
			snow_soft, snow_noise_scale, snow_amount);
	float sm = _fbm2(wash_noise, v_world.xz * 1.9);
	vec3 snow = snow_color * (1.0 - snow_mottle * 0.5 + sm * snow_mottle);
	ALBEDO = mix(base, snow, k);
	ROUGHNESS = 1.0;
}

void light() {
	DIFFUSE_LIGHT += _ramp_light(NORMAL, LIGHT, ATTENUATION, LIGHT_COLOR, v_world, wash_noise,
		band_e0, band_e1, band_m0, band_m1, band_m2, band_soft, wash_amp, wash_scale,
		shadow_bite, shadow_color, shadow_energy, ramp_mix);
}
"""

# --- the character surface ----------------------------------------------------
# The SAME ramp, the painted albedo untouched, and no snow layer: his paint is the thing
# this whole run exists to protect, so the only thing that changes about him is the light.
const CHAR_SHADER := """
shader_type spatial;
render_mode specular_disabled, cull_back;
""" + RAMP_UNIFORMS + """
uniform sampler2D albedo_tex : source_color, hint_default_white, filter_linear_mipmap;
uniform vec3 tint : source_color = vec3(1.0);
varying vec3 v_world;
""" + RAMP_BODY + """
void vertex() { v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz; }

void fragment() {
	ALBEDO = texture(albedo_tex, UV).rgb * tint;
	ROUGHNESS = 1.0;
}

void light() {
	DIFFUSE_LIGHT += _ramp_light(NORMAL, LIGHT, ATTENUATION, LIGHT_COLOR, v_world, wash_noise,
		band_e0, band_e1, band_m0, band_m1, band_m2, band_soft, wash_amp, wash_scale,
		shadow_bite, shadow_color, shadow_energy, ramp_mix);
}
"""

# --- the hull ink line, re-issued -------------------------------------------
# Byte-identical arithmetic to knight.gd/gear.gd's own outline shader, with two changes and
# no others: `fog_disabled`, and the colour comes from this file. Fog matters more than it
# sounds -- the shipped hull shader lets distance fog wash its line toward pale blue while a
# screen-space line composited after fog stays dark, and that is two pens by construction,
# visible as soon as anything is far away. knight.gd is NOT edited to fix this: the material
# is swapped from outside (see retint_character_ink).
const HULL_INK_SHADER := """
shader_type spatial;
render_mode unshaded, cull_front, depth_draw_opaque, shadows_disabled, fog_disabled;
uniform float width_model = 0.01;
uniform vec4 line_color : source_color = vec4(0.113, 0.082, 0.067, 1.0);
void vertex() { VERTEX += normalize(NORMAL) * width_model; }
void fragment() { ALBEDO = line_color.rgb; }
"""

# --- the screen-space pass: ink, grade, paper -------------------------------
# ONE pass, not three. The ink has to composite over the frame, the grade has to act on the
# ink as well as the paint, and the paper sits over both; as separate quads that is three
# screen copies and an ordering question, and the ordering question is the one that produces
# "why is the line the only thing not graded".
#
# THE T9 LESSON IS WHY THIS IS SCREEN-SPACE AT ALL: an inflate-and-cull-front hull outline
# needs the mesh to have an inside. On the cliffside's open, single-sided wall skirts the
# hull was not a rim around the surface, it WAS the surface -- flat, unshaded, 1 cm proud,
# winning the depth test, and 348,743 pixels of one frame. Terrain is open by nature. A
# depth-and-normal pass has no such failure mode.
const POST_SHADER := """
shader_type spatial;
render_mode unshaded, depth_draw_never, depth_test_disabled, cull_disabled, fog_disabled, shadows_disabled;
uniform sampler2D screen_tex : hint_screen_texture, filter_linear;
uniform sampler2D depth_tex : hint_depth_texture, filter_nearest;
uniform sampler2D nrm_tex : hint_normal_roughness_texture, filter_nearest;
uniform sampler2D paper_tex : filter_linear_mipmap, repeat_enable;
uniform vec3 ink_color : source_color = vec3(0.113, 0.082, 0.067);
uniform float ink_on = 1.0;
uniform float line_px = 1.3;
// THE EDGE TEST IS SCALE- AND SLOPE-AWARE, and it has to be.
//
// The first version put the threshold in METRES OF DEPTH BREAK (0.055 m) and compared it
// against a gradient measured in PIXELS. Those are different units joined by the camera's
// metres-per-pixel, so the test only held at one zoom. At the play camera (10.73 m over
// 1080 rows) flat ground changes depth by about 0.010 m across the Roberts span -- well
// under 0.055 -- and the line drew only on real edges. Zoomed out to 0.30, the same ground
// changes by about 0.068 m across the same span, over the threshold, AND THE WHOLE TERRAIN
// INKED ITSELF: black triangles across every slope, which read as a broken mesh rather than
// as a threshold expressed in the wrong frame.
//
// So the threshold is built from two terms that both move with the camera:
//   depth_edge_px * m_per_px          -- a break this many "flat pixels" deep, at any zoom
//   the PLANAR PREDICTION             -- what a locally flat surface of THIS view-space
//                                        normal would produce across the span, which is
//                                        what stops a steep slope reading as a cliff edge
uniform float m_per_px = 0.00994;        // cam.size / viewport rows; the scene keeps it current
uniform float ref_m_per_px = 0.00994;    // the play camera's own, the tuning reference
uniform float depth_edge_px = 4.2;
uniform float depth_edge_floor = 0.45;   // the fraction of the threshold where the line begins
uniform float slope_slack = 1.7;
// THE CREASE TERM IS DELIBERATELY TIMID, and the first setting was not.
//
// At normal_edge 0.60 / weight 0.85 the pass drew clean silhouettes AND filled the interior
// facets of every low-poly stone as broad wedges, and stippled the barbarian's dense mesh all
// over. Measured on the ink mask: the silhouette population sits at p10 = 1.0 px, the filled
// wedges at p90 = 12.4 px, and BOTH are full strength -- so no strength threshold separates
// them and the median width of "the line" was 4.2 px for a line that looks about 1.5.
//
// A silhouette is a DEPTH break and the depth term already draws it. The crease term exists
// only for the edges depth cannot see -- where two surfaces meet at similar depth -- so it is
// set to fire on turns sharper than about 60 degrees (|dn| >= 1.0 for a 60 degree turn) and
// to draw faintly when it does.
uniform float normal_edge = 1.05;
uniform float normal_weight = 0.30;
uniform float normal_fade_m = 70.0;      // creases stop being drawn past here
uniform float ink_gain = 1.15;
uniform float sky_depth_m = 400.0;       // beyond this there is no geometry to outline
uniform float grade_on = 1.0;
uniform vec3 grade_shadow : source_color = vec3(0.90, 0.95, 1.06);
uniform vec3 grade_high : source_color = vec3(1.035, 1.012, 0.975);
uniform float grade_sat = 1.05;
uniform float paper_amount = 0.085;
uniform float paper_scale = 1.0;

float _lin_depth(vec2 uv, mat4 inv_proj) {
	float d = texture(depth_tex, uv).r;
	vec4 v = inv_proj * vec4(vec3(uv * 2.0 - 1.0, d), 1.0);
	return -(v.z / v.w);
}

vec3 _nrm(vec2 uv) { return texture(nrm_tex, uv).xyz * 2.0 - 1.0; }

void vertex() { POSITION = vec4(VERTEX.xy * 2.0, 1.0, 1.0); }

void fragment() {
	vec2 uv = SCREEN_UV;
	vec3 col = texture(screen_tex, uv).rgb;
	if (ink_on > 0.5) {
		// Roberts cross: two diagonals, which is one texel fetch per corner instead of
		// Sobel's eight and gives a thinner line -- and thin is the whole requirement.
		// THE TAPS MUST BE AT LEAST ONE TEXEL APART. The depth and normal buffers are
		// sampled filter_nearest, so a span below 1.0 px puts all four corners of the
		// Roberts cross inside the SAME texel and the gradient is identically zero -- not
		// small, zero. At line_px 0.95 the screen-space pass drew 0 pixels in a 2-megapixel
		// frame, cleanly, with no error and no warning, and it looked like a threshold that
		// needed loosening rather than a sampling pattern that had collapsed.
		float span_px = max(line_px, 1.0);
		vec2 o = (span_px * 0.5) / VIEWPORT_SIZE;
		float d00 = _lin_depth(uv + vec2(-o.x, -o.y), INV_PROJECTION_MATRIX);
		float d11 = _lin_depth(uv + vec2( o.x,  o.y), INV_PROJECTION_MATRIX);
		float d10 = _lin_depth(uv + vec2( o.x, -o.y), INV_PROJECTION_MATRIX);
		float d01 = _lin_depth(uv + vec2(-o.x,  o.y), INV_PROJECTION_MATRIX);
		float dc = _lin_depth(uv, INV_PROJECTION_MATRIX);
		float gd = max(abs(d11 - d00), abs(d10 - d01));
		vec3 nc = _nrm(uv);
		// what a locally FLAT surface carrying this normal would produce across the span
		float planar = (abs(nc.x) + abs(nc.y)) / max(abs(nc.z), 0.12) * m_per_px * span_px;
		float thresh = depth_edge_px * m_per_px + planar * slope_slack;
		// WEIGHT BY THE SIZE OF THE DEPTH BREAK, per the brief: a silhouette against far
		// ground is metres and draws full strength; a crease is centimetres and draws faint.
		float e_depth = smoothstep(thresh * depth_edge_floor, thresh, gd);
		vec3 n00 = _nrm(uv + vec2(-o.x, -o.y));
		vec3 n11 = _nrm(uv + vec2( o.x,  o.y));
		vec3 n10 = _nrm(uv + vec2( o.x, -o.y));
		vec3 n01 = _nrm(uv + vec2(-o.x,  o.y));
		float gn = max(length(n11 - n00), length(n10 - n01));
		// a SMOOTH surface's normal turns by an amount proportional to metres-per-pixel, so
		// the crease threshold rises with the zoom for the same reason the depth one does
		float nth = normal_edge * max(1.0, m_per_px / max(ref_m_per_px, 1e-6));
		float e_nrm = smoothstep(nth * 0.45, nth, gn)
			* (1.0 - smoothstep(normal_fade_m * 0.6, normal_fade_m, dc));
		float e = max(e_depth, e_nrm * normal_weight) * ink_gain;
		// NOTHING TO OUTLINE IN OPEN SKY -- but the test is on the NEAREST tap, not on the
		// centre one. Suppressing by the centre pixel's depth kills the outline on the SKY
		// side of a silhouette while keeping it on the geometry side, so a standing stone
		// against the sky gets half a line: correct-looking, thinner than every other edge in
		// the frame, and thinner by an amount no parameter accounts for. A silhouette against
		// the sky is the most important line in the picture; it is not the one to shave.
		float dmin = min(min(min(d00, d11), min(d10, d01)), dc);
		e *= 1.0 - step(sky_depth_m, dmin);
		col = mix(col, ink_color, clamp(e, 0.0, 1.0));
	}
	if (grade_on > 0.5) {
		vec3 lw = vec3(0.2126, 0.7152, 0.0722);
		float l = dot(col, lw);
		col *= mix(grade_shadow, grade_high, smoothstep(0.0, 0.72, l));
		col = mix(vec3(dot(col, lw)), col, grade_sat);
		float pg = texture(paper_tex, uv * (VIEWPORT_SIZE / vec2(textureSize(paper_tex, 0))) * paper_scale).r;
		col *= (1.0 - paper_amount * 0.5 + pg * paper_amount);
	}
	ALBEDO = col;
}
"""


# =============================================================================
#  GENERATED TEXTURES — periodic, so they tile, and deterministic, so the snow
#  measurement can sample the same image the GPU samples.
# =============================================================================
static func _periodic_value_noise(size: int, lattice: int, seed_i: int) -> PackedFloat32Array:
	"""Value noise on a WRAPPING integer lattice. Tileable by construction: the lattice
	index wraps at `lattice`, so the right edge interpolates back into the left one.
	FastNoiseLite is not used here for exactly that reason -- its output does not tile, and
	a seam across a 60 m snowfield is the one artefact nobody can un-see."""
	var lat := PackedFloat32Array()
	lat.resize(lattice * lattice)
	var rng := RandomNumberGenerator.new()
	rng.seed = seed_i
	for i in lat.size():
		lat[i] = rng.randf()
	var out := PackedFloat32Array()
	out.resize(size * size)
	var step := float(lattice) / float(size)
	for y in size:
		var fy := float(y) * step
		var y0 := int(floorf(fy)) % lattice
		var y1 := (y0 + 1) % lattice
		var ty: float = fy - floorf(fy)
		var sy: float = ty * ty * (3.0 - 2.0 * ty)
		for x in size:
			var fx := float(x) * step
			var x0 := int(floorf(fx)) % lattice
			var x1 := (x0 + 1) % lattice
			var tx: float = fx - floorf(fx)
			var sx: float = tx * tx * (3.0 - 2.0 * tx)
			var a := lat[y0 * lattice + x0]
			var b := lat[y0 * lattice + x1]
			var c := lat[y1 * lattice + x0]
			var d := lat[y1 * lattice + x1]
			out[y * size + x] = lerpf(lerpf(a, b, sx), lerpf(c, d, sx), sy)
	return out


static func make_fbm_texture(size := 512, seed_i := 7411, octaves := 4) -> ImageTexture:
	"""A tileable fbm in R, G and B (three independent fields, so one texture serves the
	wash, the mottle and the snow threshold without them correlating)."""
	var img := Image.create(size, size, false, Image.FORMAT_RGB8)
	var chans := []
	for ch in 3:
		var acc := PackedFloat32Array()
		acc.resize(size * size)
		var amp := 1.0
		var norm := 0.0
		var lat := 8
		for o in octaves:
			var layer := _periodic_value_noise(size, lat, seed_i + ch * 977 + o * 131)
			for i in acc.size():
				acc[i] += layer[i] * amp
			norm += amp
			amp *= 0.5
			lat *= 2
		for i in acc.size():
			acc[i] /= norm
		chans.append(acc)
	for y in size:
		for x in size:
			var i := y * size + x
			img.set_pixel(x, y, Color(chans[0][i], chans[1][i], chans[2][i]))
	img.generate_mipmaps()
	return ImageTexture.create_from_image(img)


static func make_paper_texture(size := 512) -> ImageTexture:
	"""Watercolour paper: a fine tooth, a coarser cold-press grain, and faint fibres. Kept
	near 1.0 because it multiplies the frame -- paper you can SEE is a filter, and the brief
	asks for paper you can only feel."""
	var fine := _periodic_value_noise(size, size / 2, 31)
	var mid := _periodic_value_noise(size, 64, 32)
	var coarse := _periodic_value_noise(size, 16, 33)
	var img := Image.create(size, size, false, Image.FORMAT_RGB8)
	for y in size:
		for x in size:
			var i := y * size + x
			var v := 0.5 + (fine[i] - 0.5) * 0.62 + (mid[i] - 0.5) * 0.30 + (coarse[i] - 0.5) * 0.16
			# fibres: two faint periodic streak fields, so they tile with everything else
			v += sin(float(x) * TAU * 7.0 / float(size) + coarse[i] * 6.0) * 0.022
			v += sin(float(y) * TAU * 11.0 / float(size) + mid[i] * 5.0) * 0.016
			var c := clampf(v, 0.0, 1.0)
			img.set_pixel(x, y, Color(c, c, c))
	img.generate_mipmaps()
	return ImageTexture.create_from_image(img)


static func make_flake_texture(size := 24) -> ImageTexture:
	"""One painted flake: a soft blob with an irregular edge and a slightly denser core, so
	falling snow reads as paint rather than as a point sprite."""
	var n := _periodic_value_noise(size, 6, 91)
	var img := Image.create(size, size, false, Image.FORMAT_RGBA8)
	var c := (float(size) - 1.0) * 0.5
	for y in size:
		for x in size:
			var dx := (float(x) - c) / c
			var dy := (float(y) - c) / c
			var r: float = sqrt(dx * dx + dy * dy)
			var wob: float = 0.80 + n[y * size + x] * 0.34
			var a: float = clampf(1.0 - smoothstep(wob * 0.35, wob, r), 0.0, 1.0)
			a = pow(a, 1.35)
			img.set_pixel(x, y, Color(1.0, 1.0, 1.0, a))
	img.generate_mipmaps()
	return ImageTexture.create_from_image(img)


# =============================================================================
#  MATERIALS
# =============================================================================
static func _shader(code: String) -> Shader:
	var s := Shader.new()
	s.code = code
	return s


static func world_material(fbm: Texture2D, base: Color, params := {}) -> ShaderMaterial:
	var m := ShaderMaterial.new()
	m.shader = _shader(WORLD_SHADER)
	m.set_shader_parameter("wash_noise", fbm)
	m.set_shader_parameter("mottle_noise", fbm)
	m.set_shader_parameter("base_color", base)
	for k in params:
		m.set_shader_parameter(k, params[k])
	return m


static func char_material(fbm: Texture2D, albedo: Texture2D, params := {}) -> ShaderMaterial:
	var m := ShaderMaterial.new()
	m.shader = _shader(CHAR_SHADER)
	m.set_shader_parameter("wash_noise", fbm)
	if albedo != null:
		m.set_shader_parameter("albedo_tex", albedo)
	for k in params:
		m.set_shader_parameter(k, params[k])
	return m


static func hull_ink_material(width_model: float, ink: Color) -> ShaderMaterial:
	var m := ShaderMaterial.new()
	m.shader = _shader(HULL_INK_SHADER)
	m.set_shader_parameter("width_model", width_model)
	m.set_shader_parameter("line_color", ink)
	return m


static func post_material(paper: Texture2D, ink: Color, params := {}) -> ShaderMaterial:
	var m := ShaderMaterial.new()
	m.shader = _shader(POST_SHADER)
	m.set_shader_parameter("paper_tex", paper)
	m.set_shader_parameter("ink_color", ink)
	# drawn LAST. It reads hint_screen_texture, which puts it in the transparent queue
	# alongside the snowfall; priority, not distance, decides which of those two is on top,
	# and a post pass under the particles it is supposed to grade is a silent wrong answer.
	m.render_priority = 120
	for k in params:
		m.set_shader_parameter(k, params[k])
	return m


static func post_quad(cam: Camera3D, mat: ShaderMaterial) -> MeshInstance3D:
	var q := MeshInstance3D.new()
	q.name = "PostStack"
	var qm := QuadMesh.new()
	qm.size = Vector2(2, 2)
	q.mesh = qm
	q.material_override = mat
	q.extra_cull_margin = 1e5
	q.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	cam.add_child(q)
	q.position = Vector3(0, 0, -1)
	return q


# =============================================================================
#  THE CHARACTER, BROUGHT UNDER THE SAME LIGHT — from OUTSIDE knight.gd
# =============================================================================
# knight.gd and gear.gd are owned by a concurrent workstream (the armed motion set), so not
# one line of either is touched. Everything below reaches in through the public node tree:
# it reads the StandardMaterial3D that _style() put on each mesh, lifts its albedo texture,
# and swaps in the ramp. The originals are kept so V can put them back, which is also the
# before/after Matt is shown.
static func adopt_character(knight: Node, fbm: Texture2D, ink: Color,
		params := {}) -> Dictionary:
	var saved := {"meshes": [], "inks": [], "ink_px": []}
	for n in knight.find_children("*", "MeshInstance3D", true, false):
		var mi := n as MeshInstance3D
		if mi.mesh == null:
			continue
		if String(mi.name).ends_with("_ink") or String(mi.name) == "InkLine":
			# the hull line: re-issued in the one pen, keeping its own measured width
			var old := mi.material_override as ShaderMaterial
			var w := 0.011
			if old != null:
				var got = old.get_shader_parameter("width_model")
				if got != null:
					w = float(got)
			saved["inks"].append({"mi": mi, "mat": old})
			saved["ink_px"].append(w)
			mi.material_override = hull_ink_material(w, ink)
			continue
		var src := mi.material_override as BaseMaterial3D
		var tex: Texture2D = null
		if src != null:
			tex = src.albedo_texture
		if tex == null:
			var act := mi.get_active_material(0) as BaseMaterial3D
			if act != null:
				tex = act.albedo_texture if act.albedo_texture != null else act.emission_texture
		var ramp := char_material(fbm, tex, params)
		saved["meshes"].append({"mi": mi, "mat": mi.material_override, "ramp": ramp})
		mi.material_override = ramp
	return saved


static func restore_character(saved: Dictionary) -> void:
	"""Put HIS OWN ORIGINAL MATERIALS back -- knight.gd's StandardMaterial3D at roughness
	0.62 / metallic 0.25, and the cool near-black hull line it shipped with.

	This is a THIRD state and not the same as ramp_mix = 0, which is the distinction that
	makes the before/after honest. ramp_mix = 0 gives plain Lambert on the same albedo
	through the ramp shader, with no metallic term -- close to the old look but not it.
	Metallic is not cosmetic in Godot: it takes energy out of the diffuse. So the frame Matt
	should be shown as "before" is this one, the material he actually approved."""
	for e in saved.get("meshes", []):
		((e["mi"]) as MeshInstance3D).material_override = e["mat"]
	for e in saved.get("inks", []):
		((e["mi"]) as MeshInstance3D).material_override = e["mat"]


static func reapply_character(saved: Dictionary, ink: Color) -> void:
	for e in saved.get("meshes", []):
		((e["mi"]) as MeshInstance3D).material_override = e["ramp"]
	var i := 0
	var widths: Array = saved.get("ink_px", [])
	for e in saved.get("inks", []):
		var w: float = float(widths[i]) if i < widths.size() else 0.011
		((e["mi"]) as MeshInstance3D).material_override = hull_ink_material(w, ink)
		i += 1


static func set_character_ramp(saved: Dictionary, on: bool) -> void:
	"""The V toggle, on him: the ramp's own mix parameter rather than a material swap, so
	his ink line and his albedo are provably identical in both states and the ONLY thing
	the A/B moves is the lighting response."""
	for e in saved.get("meshes", []):
		var m := ((e["mi"]) as MeshInstance3D).material_override as ShaderMaterial
		if m != null:
			m.set_shader_parameter("ramp_mix", 1.0 if on else 0.0)


static func set_character_param(saved: Dictionary, key: String, value) -> void:
	for e in saved.get("meshes", []):
		var m := ((e["mi"]) as MeshInstance3D).material_override as ShaderMaterial
		if m != null:
			m.set_shader_parameter(key, value)


# =============================================================================
#  LIGHT, SKY AND AIR
# =============================================================================
static func winter_sun(elev_deg := 17.0, screen_az_deg := 305.0) -> DirectionalLight3D:
	"""ONE light. Low, pale-warm, from screen upper-LEFT.

	`screen_az_deg` is an azimuth in the camera's own yaw frame, so "upper left" stays
	upper left whatever the world yaw is -- the barrow camera is yawed 47 degrees and a
	light aimed by world azimuth would arrive somewhere else on screen."""
	var l := DirectionalLight3D.new()
	l.name = "WinterSun"
	var e := deg_to_rad(elev_deg)
	var a := deg_to_rad(screen_az_deg)
	var d := Vector3(-sin(a) * cos(e), -sin(e), -cos(a) * cos(e)).normalized()
	l.look_at_from_position(Vector3(0, 30, 0), Vector3(0, 30, 0) + d, Vector3.UP)
	l.light_color = Color(1.0, 0.955, 0.885)        # pale winter warm
	# 0.90, not 1.0, and the difference is not taste. With snow albedo 0.80, ambient 0.30 and
	# the ramp's top band, a slope tipped 12 degrees toward the sun renders at sRGB 1.062 at
	# energy 1.0 -- PAST WHITE, clipped, and so does everything brighter than it. That is why
	# the first snowfield had no form: its whole top end was flat against the ceiling. The
	# number came out of the closed-form pipeline, not out of re-rendering and squinting.
	l.light_energy = 0.90
	l.shadow_enabled = true
	l.shadow_blur = 1.7
	# A 17-DEGREE SUN IS THE WORST CASE FOR SHADOW BIAS. Grazing light turns a shadow-map
	# texel of size s into a depth error of s/tan(17 deg) = 3.3 s, so the bias that a noon
	# sun needs is about a third of what this one does. Under-biased, a 0.55 m terrain grid
	# self-shadows in facets and reads as a broken mesh.
	l.shadow_bias = 0.13
	l.shadow_normal_bias = 3.0
	# ONE SPLIT, because the camera is ORTHOGRAPHIC. Cascades exist to spend shadow
	# resolution where a perspective frustum is narrow and save it where it is wide; an
	# orthographic frustum is a BOX of constant cross-section, so there is no wide end to
	# save for and four splits only divide one map into four smaller ones. The caller sets
	# the distance from its own standoff -- see barrow_world.CAM_STANDOFF for why that is
	# not a free parameter.
	l.directional_shadow_mode = DirectionalLight3D.SHADOW_ORTHOGONAL
	l.directional_shadow_max_distance = 115.0
	l.directional_shadow_fade_start = 0.92
	return l


static func sun_screen_dir(l: DirectionalLight3D, cam: Camera3D) -> Vector2:
	"""Where the light comes FROM, in screen pixels-ish: +x right, +y UP. The brief says
	upper-left, so this must come back negative x, positive y, and saying so in the report
	is cheaper than arguing about a still."""
	var to_light := l.global_transform.basis.z          # -Z points along travel, so +Z is toward the sun
	var b := cam.global_transform.basis
	return Vector2(to_light.dot(b.x), to_light.dot(b.y))


static func barrow_environment(params := {}) -> Environment:
	var env := Environment.new()
	var sky := Sky.new()
	var pm := ProceduralSkyMaterial.new()
	# GENERATED sky, no panorama bought or downloaded
	pm.sky_top_color = Color(0.435, 0.560, 0.745)
	pm.sky_horizon_color = Color(0.815, 0.855, 0.900)
	pm.sky_curve = 0.13
	pm.sky_energy_multiplier = 1.0
	pm.ground_bottom_color = Color(0.760, 0.800, 0.860)
	pm.ground_horizon_color = Color(0.820, 0.860, 0.905)
	pm.sun_angle_max = 12.0
	pm.sun_curve = 0.12
	sky.sky_material = pm
	env.background_mode = Environment.BG_SKY
	env.sky = sky
	# BLUE SKY AMBIENT, set explicitly rather than taken from the sky, because it is one of
	# the numbers the report has to state and a sky-derived ambient is not a number.
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.585, 0.680, 0.870)
	env.ambient_light_energy = 0.30
	env.ambient_light_sky_contribution = 0.0
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	env.tonemap_exposure = 1.0
	env.tonemap_white = 1.0
	env.ssao_enabled = false
	env.ssil_enabled = false
	env.sdfgi_enabled = false
	env.glow_enabled = false
	# DISTANCE FOG, pale blue, in DEPTH mode so where it starts is a metre value and not a
	# density to be guessed at; plus height fog that pools in the basin. Property names read
	# off Environment itself in tools/probe_gfx.gd rather than remembered.
	env.fog_enabled = true
	env.fog_mode = Environment.FOG_MODE_DEPTH
	env.fog_light_color = Color(0.800, 0.860, 0.935)
	env.fog_light_energy = 1.0
	env.fog_sun_scatter = 0.06
	env.fog_density = 0.72
	env.fog_depth_begin = 34.0
	env.fog_depth_end = 205.0
	env.fog_depth_curve = 1.45
	env.fog_sky_affect = 0.30
	env.fog_height = -0.6
	env.fog_height_density = 0.10
	env.fog_aerial_perspective = 0.0
	for k in params:
		env.set(k, params[k])
	return env


static func snowfall(flake: Texture2D, box := Vector3(44, 26, 44), amount := 1700) -> GPUParticles3D:
	var p := GPUParticles3D.new()
	p.name = "Snowfall"
	p.amount = amount
	p.lifetime = 9.0
	p.preprocess = 9.0
	p.local_coords = false            # the emitter follows the camera; the flakes must not
	p.draw_order = GPUParticles3D.DRAW_ORDER_VIEW_DEPTH
	var mesh := QuadMesh.new()
	mesh.size = Vector2(0.055, 0.055)
	var mm := StandardMaterial3D.new()
	mm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mm.blend_mode = BaseMaterial3D.BLEND_MODE_MIX
	mm.albedo_texture = flake
	mm.albedo_color = Color(0.985, 0.992, 1.0, 0.86)
	mm.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
	mm.billboard_keep_scale = true
	mm.disable_receive_shadows = true
	mm.no_depth_test = false
	mm.cull_mode = BaseMaterial3D.CULL_DISABLED
	mesh.material = mm
	p.draw_pass_1 = mesh
	var pr := ParticleProcessMaterial.new()
	pr.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_BOX
	pr.emission_box_extents = box * 0.5
	pr.direction = Vector3(0.35, -1.0, 0.12)
	pr.spread = 14.0
	pr.initial_velocity_min = 0.55
	pr.initial_velocity_max = 1.30
	pr.gravity = Vector3(0.55, -0.85, 0.20)       # drifting, not falling: winter air, not rain
	pr.damping_min = 0.20
	pr.damping_max = 0.60
	pr.scale_min = 0.55
	pr.scale_max = 1.55
	pr.turbulence_enabled = true
	pr.turbulence_noise_strength = 0.42
	pr.turbulence_noise_scale = 1.9
	pr.turbulence_influence_min = 0.10
	pr.turbulence_influence_max = 0.45
	pr.color = Color(1, 1, 1, 1)
	p.process_material = pr
	return p


static func ridge_gust(flake: Texture2D, amount := 420) -> GPUParticles3D:
	"""Snow lifted OFF a ridge line: the optional item. Emitted from a flat box lying on the
	ridge with an upward-and-downwind initial velocity, and pulsed from the scene so it
	reads as gusts rather than as a fountain."""
	var p := GPUParticles3D.new()
	p.name = "RidgeGust"
	p.amount = amount
	p.lifetime = 3.4
	p.preprocess = 2.0
	p.local_coords = false
	p.draw_order = GPUParticles3D.DRAW_ORDER_VIEW_DEPTH
	var mesh := QuadMesh.new()
	mesh.size = Vector2(0.05, 0.05)
	var mm := StandardMaterial3D.new()
	mm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mm.albedo_texture = flake
	mm.albedo_color = Color(1.0, 1.0, 1.0, 0.62)
	mm.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
	mm.billboard_keep_scale = true
	mm.cull_mode = BaseMaterial3D.CULL_DISABLED
	mesh.material = mm
	p.draw_pass_1 = mesh
	var pr := ParticleProcessMaterial.new()
	pr.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_BOX
	pr.emission_box_extents = Vector3(9.0, 0.12, 1.2)
	pr.direction = Vector3(0.55, 0.85, 0.10)
	pr.spread = 26.0
	pr.initial_velocity_min = 1.8
	pr.initial_velocity_max = 4.6
	pr.gravity = Vector3(1.9, -0.55, 0.45)
	pr.damping_min = 0.8
	pr.damping_max = 1.8
	pr.scale_min = 0.45
	pr.scale_max = 1.25
	pr.turbulence_enabled = true
	pr.turbulence_noise_strength = 0.85
	pr.turbulence_noise_scale = 2.6
	pr.turbulence_influence_max = 0.8
	var ramp := Gradient.new()
	ramp.set_color(0, Color(1, 1, 1, 0.0))
	ramp.set_color(1, Color(1, 1, 1, 0.0))
	ramp.add_point(0.18, Color(1, 1, 1, 1.0))
	ramp.add_point(0.55, Color(1, 1, 1, 0.75))
	var gt := GradientTexture1D.new()
	gt.gradient = ramp
	pr.color_ramp = gt
	p.process_material = pr
	return p


# =============================================================================
#  MEASURING THE SNOW LAYER
# =============================================================================
static func _bilinear_r(img: Image, u: float, v: float) -> float:
	"""Sample the fbm image the way the GPU does: wrapped, bilinear, red channel. Reading
	the same image with the same filter is the whole reason the noise is generated here in
	code rather than by FastNoiseLite at draw time -- a second implementation of the noise
	would make the measurement a measurement of the second implementation."""
	var w := img.get_width()
	var h := img.get_height()
	var x: float = u * float(w) - 0.5
	var y: float = v * float(h) - 0.5
	var x0 := int(floorf(x))
	var y0 := int(floorf(y))
	var fx: float = x - float(x0)
	var fy: float = y - float(y0)
	var x1 := posmod(x0 + 1, w)
	var y1 := posmod(y0 + 1, h)
	x0 = posmod(x0, w)
	y0 = posmod(y0, h)
	var a := img.get_pixel(x0, y0).r
	var b := img.get_pixel(x1, y0).r
	var c := img.get_pixel(x0, y1).r
	var d := img.get_pixel(x1, y1).r
	return lerpf(lerpf(a, b, fx), lerpf(c, d, fx), fy)


static func _fbm2_cpu(img: Image, p: Vector2) -> float:
	return _bilinear_r(img, p.x, p.y) * 0.62 \
		+ _bilinear_r(img, p.x * 2.17 + 0.31, p.y * 2.17 + 0.77) * 0.38


static func snow_at(img: Image, wpos: Vector3, wn: Vector3, thr: float, jit: float,
		soft: float, nscale: float, amount: float) -> float:
	"""The shader's `snow_coverage`, line for line, on the CPU."""
	var up := wn.normalized().dot(Vector3.UP)
	var sn := _fbm2_cpu(img, Vector2(wpos.x * nscale + 11.3, wpos.z * nscale + 4.7))
	var t: float = thr + (sn - 0.5) * jit
	return smoothstep(t, t + soft, up) * clampf(amount, 0.0, 1.0)


static func _param(mat: ShaderMaterial, key: String, fallback: float) -> float:
	"""get_shader_parameter returns null for any uniform never explicitly assigned, and the
	shader's own declared default is NOT visible through it. The fallbacks here must track
	the WORLD_SHADER declarations above; where they drift, the measurement quietly reports
	the wrong threshold, so they are kept next to the only caller that needs them."""
	var v = mat.get_shader_parameter(key)
	return fallback if v == null else float(v)


static func measure_snow(groups: Array, img: Image, covered_at := 0.5) -> Dictionary:
	"""AREA-WEIGHTED over the real triangles, not per texel: the snow layer is a world-space
	function, so it has no texel grid of its own, and triangle area is the honest measure of
	"how much of the surface".

	THE INSTRUMENT IS CHECKED ON TWO CASES WHOSE ANSWER IS KNOWN BY CONSTRUCTION -- a
	perfectly horizontal face (n.up = 1, must come back covered) and a perfectly vertical one
	(n.up = 0, must come back bare) -- evaluated through the same function, with the same
	parameters, at a hundred scattered positions. If those two do not come back 1.0 and 0.0
	the rest of the table is not evidence of anything.

	The per-face normal is the mean of the triangle's own VERTEX normals, which is what the
	fragment shader interpolates; a geometric face normal would report a smooth-shaded hill
	as a set of flat facets."""
	var bands := [0.0, 0.25, 0.5, 0.70710678]
	var out := {"groups": {}, "_defn": {
		"up_facing_bands_n_dot_up_greater_than": bands,
		"covered_when_k_at_least": covered_at,
		"weight": "triangle area in m^2",
		"normal": "mean of the triangle's vertex normals (what the fragment shader interpolates)",
	}}
	var tot_up := [0.0, 0.0, 0.0, 0.0]
	var tot_snow := [0.0, 0.0, 0.0, 0.0]
	for g in groups:
		var mat: ShaderMaterial = g["mat"]
		# A ShaderMaterial returns NULL for a uniform that was never explicitly set -- the
		# shader's own default is not readable through get_shader_parameter -- and float(null)
		# is not a conversion, it is a crash. `snow_amount` is exactly that case: nothing sets
		# it until the N key does, so the measurement died before it produced a number.
		var thr := _param(mat, "snow_threshold", 0.58)
		var jit := _param(mat, "snow_jitter", 0.30)
		var soft := _param(mat, "snow_soft", 0.13)
		var nsc := _param(mat, "snow_noise_scale", 0.85)
		var amt := _param(mat, "snow_amount", 1.0)
		var up_a := [0.0, 0.0, 0.0, 0.0]
		var sn_a := [0.0, 0.0, 0.0, 0.0]
		var down_a := 0.0
		var down_snow := 0.0
		var tris := 0
		for mi in g["meshes"]:
			var node := mi as MeshInstance3D
			if node == null or node.mesh == null:
				continue
			var xf := node.global_transform
			var nb := xf.basis.inverse().transposed()
			for s in node.mesh.get_surface_count():
				var a := node.mesh.surface_get_arrays(s)
				var v: PackedVector3Array = a[Mesh.ARRAY_VERTEX]
				var nn: PackedVector3Array = a[Mesh.ARRAY_NORMAL]
				var ix = a[Mesh.ARRAY_INDEX]
				if ix == null:
					continue
				for t in range(0, ix.size(), 3):
					var p0 := xf * v[ix[t]]
					var p1 := xf * v[ix[t + 1]]
					var p2 := xf * v[ix[t + 2]]
					var area: float = (p1 - p0).cross(p2 - p0).length() * 0.5
					if area <= 0.0:
						continue
					var wn := (nb * ((nn[ix[t]] + nn[ix[t + 1]] + nn[ix[t + 2]]) / 3.0)).normalized()
					var cen := (p0 + p1 + p2) / 3.0
					var k := snow_at(img, cen, wn, thr, jit, soft, nsc, amt)
					var u := wn.dot(Vector3.UP)
					tris += 1
					if u <= 0.0:
						down_a += area
						if k >= covered_at:
							down_snow += area
					for bi in bands.size():
						if u > bands[bi]:
							up_a[bi] += area
							if k >= covered_at:
								sn_a[bi] += area
			# nothing else needed per surface
		var rows := {}
		for bi in bands.size():
			rows["n_up_gt_%s" % str(bands[bi])] = {
				"up_area_m2": snappedf(up_a[bi], 0.1),
				"snow_area_m2": snappedf(sn_a[bi], 0.1),
				"share": snappedf(sn_a[bi] / maxf(up_a[bi], 1e-9), 0.0001),
			}
			tot_up[bi] += up_a[bi]
			tot_snow[bi] += sn_a[bi]
		out["groups"][String(g["name"])] = {
			"params": {"threshold": thr, "jitter": jit, "soft": soft, "noise_scale": nsc},
			"triangles": tris,
			"by_band": rows,
			"down_or_side_facing_control": {
				"area_m2": snappedf(down_a, 0.1),
				"snow_area_m2": snappedf(down_snow, 0.1),
				"share": snappedf(down_snow / maxf(down_a, 1e-9), 0.0001),
				"_must_be": "0.0 -- a face pointing down cannot hold snow",
			},
		}
	var totals := {}
	for bi in bands.size():
		totals["n_up_gt_%s" % str(bands[bi])] = {
			"up_area_m2": snappedf(tot_up[bi], 0.1),
			"snow_area_m2": snappedf(tot_snow[bi], 0.1),
			"share": snappedf(tot_snow[bi] / maxf(tot_up[bi], 1e-9), 0.0001),
		}
	out["all_surfaces"] = totals
	# --- the two known cases, through the same function ---------------------
	var checks := {}
	for g in groups:
		var mat: ShaderMaterial = g["mat"]
		var thr := _param(mat, "snow_threshold", 0.58)
		var jit := _param(mat, "snow_jitter", 0.30)
		var soft := _param(mat, "snow_soft", 0.13)
		var nsc := _param(mat, "snow_noise_scale", 0.85)
		var flat := 0.0
		var vert := 0.0
		var rng := RandomNumberGenerator.new()
		rng.seed = 5
		for i in 100:
			var p := Vector3(rng.randf_range(-40.0, 40.0), rng.randf_range(0.0, 8.0),
							 rng.randf_range(-40.0, 40.0))
			flat += 1.0 if snow_at(img, p, Vector3.UP, thr, jit, soft, nsc, 1.0) >= covered_at else 0.0
			vert += 1.0 if snow_at(img, p, Vector3.RIGHT, thr, jit, soft, nsc, 1.0) >= covered_at else 0.0
		checks[String(g["name"])] = {
			"horizontal_face_share": snappedf(flat / 100.0, 0.001),
			"vertical_face_share": snappedf(vert / 100.0, 0.001),
			"_expect": "1.0 and 0.0",
		}
	out["instrument_check_known_faces"] = checks
	return out


# --- reading a frame back ------------------------------------------------------
static func srgb_to_linear(c: float) -> float:
	return c / 12.92 if c <= 0.04045 else pow((c + 0.055) / 1.055, 2.4)


static func linear_to_srgb(c: float) -> float:
	return c * 12.92 if c <= 0.0031308 else 1.055 * pow(c, 1.0 / 2.4) - 0.055
