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
// THE BAND EDGES ARE A FUNCTION OF THE SUN'S ELEVATION, and moving the sun without moving
// them flattens the world (snow-lab drax, following R-C9-74 note 3).
//
// `raw` is ndl * 0.5 + 0.5, so FLAT GROUND under a sun at elevation E sits at
// 0.5 + sin(E)/2: at 17 degrees that is 0.646, in the MIDDLE band, with the top band held
// for surfaces actually turned toward the light. At 55 degrees it is 0.910 -- past e1 = 0.70
// by a wide margin, and so is every sun-facing slope, so the whole lit half of the scene
// collapses into m2 = 1.00 and has no form left. Nothing errors. The picture just goes flat,
// and it looks like a fog or an exposure problem rather than like a ramp tuned for a
// different sun.
//
// Re-derived arithmetically for a 55 degree sun rather than nudged by eye:
//   e1 0.90, soft 0.075  -- the top band starts just above flat ground, so a crest turned
//                           into the light separates from the flat beside it
//   m1 0.60              -- the middle band lifts, because at this elevation a surface in it
//                           is a flank catching light, not a shadow side
// Giving away-flank / flat / lit crest = 0.60 / 0.84 / 1.00, against 0.56 / 1.00 / 1.00 at
// the old constants. e0 and m0 are unchanged: the dark end is about facing AWAY from the
// light, which the elevation does not move.
uniform float band_e0 = 0.47;
uniform float band_e1 = 0.90;
uniform float band_m0 = 0.10;
uniform float band_m1 = 0.60;
uniform float band_m2 = 1.00;
uniform float band_soft = 0.075;
uniform float wash_amp = 0.17;
uniform float wash_scale = 0.62;
uniform float shadow_bite = 1.0;
uniform float ramp_mix = 1.0;
uniform sampler2D wash_noise : hint_default_white, filter_linear_mipmap, repeat_enable;
// T10-1d: THE CAST SHADOW IS APPLIED AFTER THE BANDS (the coordinator's call). Through T10-1c
// it multiplied N.L BEFORE the band edges, and the soft shadow filter's per-pixel rotated
// kernel made the penumbra noisy -- the band edges (soft 0.075: slope 10) thresholded that
// noise into a regular 2-px halftone along every shadow edge. Now only the FORM term goes
// through the bands; the shadow then pulls the banded value toward the away-facing value m0,
// as its own step -- LINEAR by default, which amplifies the filter's noise by exactly 1.
// 1 = the T10-1d ramp, 0 = the T10-1c ramp: a uniform, so the A/B and its cost are one run.
uniform float shadow_after_bands = 1.0;
// the shadow's own step, a linear remap of the filter's coverage: (0, 1) is the coverage
// itself; narrowing it sharpens the shadow's edge and multiplies the noise by 1 / (hi - lo)
uniform float shadow_step_lo = 0.0;
uniform float shadow_step_hi = 1.0;
// THE AMBIENT, INSIDE THE SUN'S PASS -- the phone build only (R-C9-83); 0 on the desktop, where
// the engine adds the sky ambient itself. The Compatibility renderer draws a SHADOWED light in
// an ADDITIVE pass, and each pass is sRGB-encoded BEFORE the two are added: srgb(ambient) +
// srgb(sun) instead of srgb(ambient + sun). Measured on the play frame (tools/probe_web_look.gd,
// Compatibility on ANGLE/Metal against Forward+): mean RGB 225/225/222 against the desktop's
// 188/179/174, |difference| 47 per channel -- every blue shadow and warm band summed toward
// white. With the environment's ambient moved HERE (PaintStack.move_ambient_into_light zeroes
// the environment's), the base pass adds nothing and the one sum is done in linear light
// inside this pass: |difference| 17, the rest being the web's cards and pen.
uniform vec3 ambient_in_light = vec3(0.0);
// THE SKY'S REFLECTION, emulated -- the phone build only; 0 on the desktop, which gets the real
// one. Forward+ adds the sky's radiance as specular even under specular_disabled (that mode
// stops only the light's own highlight), and the roughness MARKS make it uneven: thin props
// carry 0.25 for the pen and so reflect like wet leaves. Measured on the desktop's ambient-only
// frame, with and without the sky reflection, in linear light: thin 0.032 / 0.037 / 0.047,
// snow 0.005 / 0.008 / 0.014, the rest 0.005 / 0.006 / 0.010. Compatibility scales its
// reflection by the ambient energy that move_ambient_into_light zeroes, so it had none; this
// puts the measured amount back per class (PaintStack.web_color_space), in the sun's pass.
uniform vec3 web_sheen = vec3(0.0);
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
	float sh = mix(1.0, att, bite);                    // the cast shadow: 1 lit, 0 shadowed
	// THE FORM goes through the bands. With shadow_after_bands 0 the shadow multiplies in
	// BEFORE them, as it did through T10-1c (and the halftone comes back)
	float t = raw * mix(sh, 1.0, shadow_after_bands) + (w - 0.5) * amp;
	float b = m0;
	b += smoothstep(e0 - soft, e0 + soft, t) * (m1 - m0);
	b += smoothstep(e1 - soft, e1 + soft, t) * (m2 - m1);
	// ...THEN THE SHADOW: toward the away-facing value, so a cast shadow and a surface turned
	// from the light still land on ONE value -- reached through the filter's own gradient
	// instead of through a band edge
	float s2 = clamp((sh - shadow_step_lo) / max(shadow_step_hi - shadow_step_lo, 1e-3), 0.0, 1.0);
	b = mix(b, mix(m0, b, s2), shadow_after_bands);
	vec3 warm = light_color / PI;                      // see note 2: LIGHT_COLOR carries a PI
	vec3 cool = sh_col * sh_e;                         // shadow is BLUE-VIOLET, never black
	vec3 ramped = mix(cool, warm, clamp(b, 0.0, 1.0));
	vec3 plain = (light_color / PI) * max(ndl, 0.0) * att;
	// + the ambient on the phone build only (ambient_in_light, above); 0 on the desktop
	return mix(plain, ramped, mix_amt) + ambient_in_light;   // mix_amt 0 == the stack OFF, for A/B
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
// T10-1c: a per-material grade on the painted albedo -- the heather is pulled onto the
// painting's own heather hue by it, measured (see the barrow's HEATHER_TINT). A LINEAR
// multiplier, deliberately without source_color: with the hint, Godot runs the value through
// the sRGB curve and a 0.6 acts as 0.32.
uniform vec3 tex_tint = vec3(1.0);
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
// WHAT THIS MESH IS, for the screen-space pen, written into the roughness channel. 1.0 is
// ordinary world; 0.25 says "thin" -- twigs and sprigs, where a full-strength line is wider
// than the thing it outlines. Both shaders are `specular_disabled`, so this changes no pixel
// of the render and costs nothing. See POST_SHADER.
uniform float mesh_mark = 1.0;
// T10-1d: a per-INSTANCE tone, hashed from the instance's own origin so it is the same whether
// the prop is drawn as a node or inside a MultiMesh. 0 = none; the heather's base uses it.
uniform float tone_jitter = 0.0;
varying vec3 v_world;
varying vec3 v_wnormal;
varying float v_rnd;
""" + RAMP_BODY + """
void vertex() {
	v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	v_wnormal = normalize((MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz);
	v_rnd = fract(sin(dot(MODEL_MATRIX[3].xz, vec2(12.9898, 78.233))) * 43758.5453);
}

float snow_coverage(vec3 wpos, vec3 wn, sampler2D mn, float thr, float jit, float soft,
		float nscale, float amount) {
	float up = dot(normalize(wn), vec3(0.0, 1.0, 0.0));
	float sn = _fbm2(mn, wpos.xz * nscale + vec2(11.3, 4.7));
	float t = thr + (sn - 0.5) * jit;
	return smoothstep(t, t + soft, up) * clamp(amount, 0.0, 1.0);
}

void fragment() {
	vec3 base = use_tex ? texture(albedo_tex, UV * tex_scale).rgb * tex_tint : base_color;
	base *= 1.0 + (v_rnd - 0.5) * tone_jitter;
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
	ROUGHNESS = mesh_mark;
}

void light() {
	DIFFUSE_LIGHT += _ramp_light(NORMAL, LIGHT, ATTENUATION, LIGHT_COLOR, v_world, wash_noise,
		band_e0, band_e1, band_m0, band_m1, band_m2, band_soft, wash_amp, wash_scale,
		shadow_bite, shadow_color, shadow_energy, ramp_mix);
	SPECULAR_LIGHT += web_sheen;      // the phone build's sky reflection; 0 on the desktop
}
"""

# --- the ground, wearing the six painted tiles ---------------------------------
# WORLD_SHADER with one thing added and nothing removed: the base colour comes from five
# generated 1024² tiles blended by the concept's own splat map instead of from a constant.
# The ramp, the mottle, the hatch, the wash and the snow layer are the SAME code, so the
# ground is not a second shading model wearing the first one's colours.
#
# FIVE DECISIONS, each of which has a way of being silently wrong:
#
# 1. THE TILE UV IS WORLD METRES, NOT MESH UV. barrow_heightfield.gd emits UV = xz * 0.25,
#    which is a perfectly good UV and is NOT metres; tiling on it would put the tile at a
#    scale nothing states. `v_world.xz / tile_m` means the number in `tile_m` IS the size of
#    one tile on the ground, in metres, and can be checked with a ruler in the frame.
#
# 2. THE SPLAT IS SAMPLED AS WEIGHTS, NOT AS IDS. The shipped map is a 300x300 image of
#    class ids 0..4. Bilinear filtering of ids is meaningless -- halfway between snow (0) and
#    rock (2) is path (1), which is not a blend, it is a third material appearing along every
#    border. So the ids are expanded to five weight fields and BLURRED ON THE CPU before
#    upload (splat_weight_texture), and what the GPU filters is a weight.
#
# 3. FOUR CHANNELS CARRY FIVE CLASSES and the fifth is `1 - sum`. The implied class is SNOW,
#    deliberately: the quantisation error of four 8-bit channels lands entirely on the
#    implied one (up to 4/255), and snow is the class that is already near 1 where it
#    matters. Implying ICE instead would spread a 1.6% ice wash over the whole moor.
#
# 4. OUTSIDE THE PAINTED 15 m THE MOOR IS SNOW. The concept covers 15x15 m of a 92x92 m
#    world; the weights relax to pure snow over `splat_relax_m`, the same way the heightfield
#    relaxes to its rim level, so the join is a gradient rather than a square edge.
#
# 5. THE PROCEDURAL SNOW LAYER IS SCALED PER CLASS. At the ground's shipped threshold every
#    up-facing triangle came back 100% covered -- which is why the stand-in frame is a white
#    desert -- and a tile map under a total snow layer is a tile map nobody can see. `keep`
#    is how much of the drift each class holds: snow all of it, heather and rock little. The
#    CPU mirror in measure_snow takes the same factor through `amount_scale`, so the measured
#    share is of what is actually drawn.
const GROUND_SHADER := """
shader_type spatial;
render_mode specular_disabled, cull_back;
""" + RAMP_UNIFORMS + """
uniform vec3 base_color : source_color = vec3(0.44, 0.42, 0.47);
uniform sampler2D tile_snow : source_color, hint_default_white, filter_linear_mipmap, repeat_enable;
uniform sampler2D tile_path : source_color, hint_default_white, filter_linear_mipmap, repeat_enable;
uniform sampler2D tile_rock : source_color, hint_default_white, filter_linear_mipmap, repeat_enable;
uniform sampler2D tile_heather : source_color, hint_default_white, filter_linear_mipmap, repeat_enable;
uniform sampler2D tile_ice : source_color, hint_default_white, filter_linear_mipmap, repeat_enable;
// RGBA = path, rock, heather, ice. Snow is 1 - their sum. NO source_color hint: these are
// weights, not colour, and an sRGB decode on them would bend every border.
uniform sampler2D splat_w : filter_linear, repeat_disable;
uniform vec2 splat_origin = vec2(-4.43, -7.56);   // world xz of the splat's (0,0) corner
uniform vec2 splat_size = vec2(15.0, 15.0);
uniform float splat_relax_m = 6.0;
uniform float tile_m = 2.5;                       // METRES per tile repeat. Stated, not implied.
uniform float detile_mix = 0.35;                  // second sample, rotated and rescaled
uniform float tile_tint = 1.0;                    // 0 = flat base_color, for the A/B
// how much of the world-space drift each class holds: snow, path, rock, heather, ice
uniform vec4 snow_keep_path_rock_heather_ice = vec4(0.45, 0.30, 0.22, 0.25);
uniform float snow_keep_snow = 1.0;
uniform sampler2D mottle_noise : hint_default_white, filter_linear_mipmap, repeat_enable;
uniform float mottle_amp = 0.13;
uniform float mottle_scale = 0.33;
uniform float hatch_amp = 0.05;
uniform float hatch_scale = 5.5;
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

// TWO SAMPLES OF THE SAME TILE, the second turned 90 degrees and at 0.61x, mixed. A 2.5 m
// tile repeats six times across the painted ground and the lattice is plain at the play
// camera; one extra fetch per class breaks it without a second texture to author.
vec3 _tile2(sampler2D t, vec2 uv, vec2 uv2, float m) {
	return mix(texture(t, uv).rgb, texture(t, uv2).rgb, m);
}

float snow_coverage(vec3 wpos, vec3 wn, sampler2D mn, float thr, float jit, float soft,
		float nscale, float amount) {
	float up = dot(normalize(wn), vec3(0.0, 1.0, 0.0));
	float sn = _fbm2(mn, wpos.xz * nscale + vec2(11.3, 4.7));
	float t = thr + (sn - 0.5) * jit;
	return smoothstep(t, t + soft, up) * clamp(amount, 0.0, 1.0);
}

void fragment() {
	vec2 suv = (v_world.xz - splat_origin) / splat_size;
	vec4 w = texture(splat_w, clamp(suv, vec2(0.0), vec2(1.0)));
	float w_snow = clamp(1.0 - (w.r + w.g + w.b + w.a), 0.0, 1.0);
	// how far outside the painted square we are, IN METRES, and the relax to plain snow
	vec2 d = max(max(-suv, suv - vec2(1.0)), vec2(0.0)) * splat_size;
	float t_out = smoothstep(0.0, splat_relax_m, length(d));
	float w0 = mix(w_snow, 1.0, t_out);
	vec4 wr = w * (1.0 - t_out);                  // path, rock, heather, ice
	float wsum = max(w0 + wr.r + wr.g + wr.b + wr.a, 1e-4);

	vec2 tuv = v_world.xz / max(tile_m, 1e-3);
	vec2 tuv2 = vec2(tuv.y, -tuv.x) * 0.61 + vec2(0.37, 0.19);
	vec3 tiles = (_tile2(tile_snow, tuv, tuv2, detile_mix) * w0
				+ _tile2(tile_path, tuv, tuv2, detile_mix) * wr.r
				+ _tile2(tile_rock, tuv, tuv2, detile_mix) * wr.g
				+ _tile2(tile_heather, tuv, tuv2, detile_mix) * wr.b
				+ _tile2(tile_ice, tuv, tuv2, detile_mix) * wr.a) / wsum;
	vec3 base = mix(base_color, tiles, clamp(tile_tint, 0.0, 1.0));

	float m = _fbm2(mottle_noise, v_world.xz * mottle_scale + v_world.y * 0.17);
	base *= (1.0 - mottle_amp * 0.5 + m * mottle_amp);
	float h = texture(mottle_noise, v_world.xz * hatch_scale + vec2(0.5, 0.17)).r;
	base *= (1.0 - hatch_amp * 0.5 + h * hatch_amp);

	float keep = (snow_keep_snow * w0 + dot(snow_keep_path_rock_heather_ice, wr)) / wsum;
	float k = snow_coverage(v_world, v_wnormal, mottle_noise, snow_threshold, snow_jitter,
			snow_soft, snow_noise_scale, snow_amount) * keep;
	float sm = _fbm2(wash_noise, v_world.xz * 1.9);
	vec3 snow = snow_color * (1.0 - snow_mottle * 0.5 + sm * snow_mottle);
	ALBEDO = mix(base, snow, k);
	ROUGHNESS = 1.0;
}

void light() {
	DIFFUSE_LIGHT += _ramp_light(NORMAL, LIGHT, ATTENUATION, LIGHT_COLOR, v_world, wash_noise,
		band_e0, band_e1, band_m0, band_m1, band_m2, band_soft, wash_amp, wash_scale,
		shadow_bite, shadow_color, shadow_energy, ramp_mix);
	SPECULAR_LIGHT += web_sheen;      // the phone build's sky reflection; 0 on the desktop
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
// HIS MARK IN THE ROUGHNESS CHANNEL. See POST_SHADER: the screen-space pen has to know which
// pixels are him so it can leave them to his hull line, and the normal-roughness buffer's
// alpha is the only per-pixel channel a post pass can read that nothing else is using --
// both shaders here are `specular_disabled`, so ROUGHNESS changes no pixel of the render.
// 0.5 against the world's 1.0 is half the channel apart; anything within 0.12 of it is him.
uniform float char_mark = 0.5;
varying vec3 v_world;
""" + RAMP_BODY + """
void vertex() { v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz; }

void fragment() {
	ALBEDO = texture(albedo_tex, UV).rgb * tint;
	ROUGHNESS = char_mark;
}

void light() {
	DIFFUSE_LIGHT += _ramp_light(NORMAL, LIGHT, ATTENUATION, LIGHT_COLOR, v_world, wash_noise,
		band_e0, band_e1, band_m0, band_m1, band_m2, band_soft, wash_amp, wash_scale,
		shadow_bite, shadow_color, shadow_energy, ramp_mix);
	SPECULAR_LIGHT += web_sheen;      // the phone build's sky reflection; 0 on the desktop
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
uniform float depth_edge_px = 3.0;
uniform float depth_edge_floor = 0.45;   // the fraction of the threshold where the line begins
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
// ONE PASS ON HIM, NOT TWO (R-C9-74 note 5). Matt, on the 15:20 build: "There is a WAY too
// thick outline of black around the barbarian." He was getting BOTH pens: his own hull line
// at outline_px 1.1 -- the one approved in the cliffside 3D app -- and this pass's depth
// line on top of it, which at the time measured 3.76 px median. Two lines side by side read
// as one thick line, and no amount of tuning either one alone fixes it.
//
// The fix keeps HIS hull, because that is exactly the approved look, and takes this pass off
// him: every tap that lands on his pixels kills the edge there, including the taps on the
// GROUND side of his silhouette -- otherwise the pass would still draw a line hugging his
// outside edge and the two would still stack. `char_exclude` 0 puts it back, which is how
// the before/after is measured on one run rather than two.
uniform float char_exclude = 1.0;
uniform float char_mark_ref = 0.5;
uniform float char_mark_tol = 0.12;
// THE PEN, TURNED DOWN ON THINGS THINNER THAN IT. A heather sprig and a birch twig are a few
// millimetres across; at the play camera that is under a pixel, and every one of them is a
// depth break of half a metre against the ground behind. The pen draws all of them at full
// strength and there is nothing left of the plant -- measured on look_play at 1920x1080: the
// nineteen tussocks and every birch canopy rendered as solid ink with no internal structure,
// which is not a stylised tree, it is a blot.
//
// NOT ZERO. At zero they lose their silhouette entirely and read as smudges on the snow. At
// 0.28 the twigs come through as grey and the trunks still carry a line -- the same pen at
// the same colour, drawing less of itself, which is what a pen does on something small.
uniform float thin_mark_ref = 0.25;
uniform float thin_pen_scale = 0.28;
// NO LINE WHOSE NEAR SIDE IS SNOW (T10-1b). The 3D snow field writes ROUGHNESS 0.75. Its drift
// crests and trail edges are real depth breaks, and the pen drew them as flecks -- small black
// ticks scattered across a white field, which read as dirt. Tested on the CENTRE tap only, and
// that is the whole trick: the positive-side second difference draws a line on the NEAR
// surface, so where a stone stands in snow the silhouette pixel IS the stone and keeps its
// line, while a crest whose near side is snow is skipped. Neighbour taps are not tested --
// that would also take the line off every object where it meets the snow.
uniform float snow_exclude = 1.0;
uniform float snow_mark_ref = 0.75;
// NO PEN ON THE PAINTING (barrow_full, T10-2 step 4 -- the conductor's ruling: the painting is
// the world's light AND ITS INK). A painted static piece writes ROUGHNESS 0.0 (PaintedWorld.
// PAINTED_MARK); its outline is already in its plate, the 3 px ring the painter inked. So no line
// whose NEAR side is painted -- the centre tap, exactly as the snow's test above: where he or the
// heather stands in front of a painted stone, the near pixel is theirs and keeps its line.
// Measured before it was written (tools/probe_paint_light.gd): the buffer's alpha IS the roughness
// written, linear -- 0.0 reads 0.0, 0.25 reads 0.25 -- moving or not.
uniform float painted_exclude = 1.0;
uniform float painted_mark_ref = 0.0;

float _lin_depth(vec2 uv, mat4 inv_proj) {
	float d = texture(depth_tex, uv).r;
	vec4 v = inv_proj * vec4(vec3(uv * 2.0 - 1.0, d), 1.0);
	return -(v.z / v.w);
}

vec3 _nrm(vec2 uv) { return texture(nrm_tex, uv).xyz * 2.0 - 1.0; }

// IS THIS PIXEL THE CHARACTER. CHAR_SHADER writes ROUGHNESS = char_mark (0.5) where the
// world writes 1.0, and both are `specular_disabled` so the channel changes no pixel of the
// render -- it is a free per-pixel tag in a buffer this pass is already sampling.
float _is_char(vec2 uv) {
	return 1.0 - step(char_mark_tol, abs(texture(nrm_tex, uv).a - char_mark_ref));
}

float _is_thin(vec2 uv) {
	return 1.0 - step(char_mark_tol, abs(texture(nrm_tex, uv).a - thin_mark_ref));
}

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
		float dc = _lin_depth(uv, INV_PROJECTION_MATRIX);
		// THE DEPTH EDGE IS A SECOND DIFFERENCE, not a first one, and that is the fix.
		//
		// A first difference (Roberts) measures how fast depth changes. A silhouette and a
		// steeply-raked facet BOTH change depth fast, so no threshold on a first difference
		// separates them -- which is why the facet interiors of every stone inked solid. I
		// tried to correct for it by predicting the gradient a planar surface of that normal
		// would produce and subtracting it, but the prediction divides by the normal's view-Z
		// and a silhouette is EXACTLY where that goes to zero. The two cases are the same
		// condition for that operator. Raising the clamp floor 0.12 -> 0.35 to compensate ran
		// the wrong way and made it worse still: median 3.76 -> 6.99 px, p90 12.9 -> 18.3.
		//
		// A SECOND difference has no such problem, by construction: for ANY plane, at any
		// rake, d(u+o) + d(u-o) - 2*d(u) is zero. Curvature gives a little, a depth
		// DISCONTINUITY gives metres. So the operator itself distinguishes a silhouette from
		// a slope, and there is nothing to tune per-angle.
		float dxp = _lin_depth(uv + vec2(o.x, 0.0), INV_PROJECTION_MATRIX);
		float dxm = _lin_depth(uv - vec2(o.x, 0.0), INV_PROJECTION_MATRIX);
		float dyp = _lin_depth(uv + vec2(0.0, o.y), INV_PROJECTION_MATRIX);
		float dym = _lin_depth(uv - vec2(0.0, o.y), INV_PROJECTION_MATRIX);
		// THE SIGN IS THE OTHER HALF OF THE FIX, and it is what makes this pen the SAME
		// WEIGHT as the hull (R-C9-74 note 5: "one pen, one weight").
		//
		// A second difference at a depth step is non-zero on BOTH pixels straddling it, with
		// OPPOSITE SIGNS: the foreground pixel sees (fg, fg, bg) and gets +(bg - fg), the
		// background pixel sees (fg, bg, bg) and gets -(bg - fg). Taking abs() draws both, so
		// the operator's natural line is two pixels -- measured at p50 2.29 px against the
		// hull's 1.16, which is exactly 2x and not a coincidence.
		//
		// Keeping only the POSITIVE side draws the line on the NEAR surface, which is where a
		// hull pen draws it and where a pen drawn by hand goes: the contour belongs to the
		// object, not to the sky behind it. One pixel, on the object, same colour, same
		// weight.
		float gd = max(max(dxp + dxm - 2.0 * dc, dyp + dym - 2.0 * dc), 0.0);
		float thresh = depth_edge_px * m_per_px;
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
		float dmin = min(min(min(dxp, dxm), min(dyp, dym)), dc);
		e *= 1.0 - step(sky_depth_m, dmin);
		// HIM, AND THE SKIRT AROUND HIM. Any tap on the character suppresses the edge: his
		// own creases, his silhouette, and the ground pixel just outside it that the depth
		// break also fires on. Five taps, the same five the depth term already fetched.
		float ch = max(max(max(_is_char(uv + vec2(o.x, 0.0)), _is_char(uv - vec2(o.x, 0.0))),
						   max(_is_char(uv + vec2(0.0, o.y)), _is_char(uv - vec2(0.0, o.y)))),
					   _is_char(uv));
		e *= 1.0 - ch * clamp(char_exclude, 0.0, 1.0);
		float th = max(max(max(_is_thin(uv + vec2(o.x, 0.0)), _is_thin(uv - vec2(o.x, 0.0))),
						   max(_is_thin(uv + vec2(0.0, o.y)), _is_thin(uv - vec2(0.0, o.y)))),
					   _is_thin(uv));
		e *= mix(1.0, clamp(thin_pen_scale, 0.0, 1.0), th);
		float sn = 1.0 - step(char_mark_tol, abs(texture(nrm_tex, uv).a - snow_mark_ref));
		e *= 1.0 - sn * clamp(snow_exclude, 0.0, 1.0);
		float pt = 1.0 - step(char_mark_tol, abs(texture(nrm_tex, uv).a - painted_mark_ref));
		e *= 1.0 - pt * clamp(painted_exclude, 0.0, 1.0);
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
	return ImageTexture.create_from_image(make_fbm_image(size, seed_i, octaves))


static func make_fbm_image(size := 512, seed_i := 7411, octaves := 4) -> Image:
	"""The fbm as a CPU Image, mipmapped, RGB8. Split out of make_fbm_texture so a caller that
	needs the bytes keeps THIS image rather than reading the texture back: ImageTexture.
	get_image() is a GPU readback, it can change the format (Metal has no RGB8), and under the
	headless dummy renderer it can come back empty -- which a byte lookup reads as zero noise,
	cleanly, on every probe."""
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
	return img


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
static var _shader_cache := {}


# --- LANE B: THE METEOR'S FIRE ON HIM AND HER (vfx_meteor_3d; scripts/meteor_fx.gd) -------------------
# NOTHING ABOVE CHANGES. With the Meteor wanted, MeteorFx derives a second shader for the characters' ramp
# materials, with_char_fire(<their live code>), and swaps it in only while a Meteor is alive: the fire's light
# is added INSIDE THE SUN'S PASS -- the way the phone build's ambient is (ambient_in_light),
# and for the same reason: Compatibility sRGB-encodes each light's pass before it adds them, so a separate
# fire light (the first build's OmniLight3D) summed hot on the web. Here the sum is one, in linear light, on
# both renderers. Two hard warm bands by N.L times an omni light's own falloff (range window x 1/d); the
# light itself is two global uniforms, so there is no light node, no light list and no shader variant to
# meet at cast time.
const CHAR_FIRE_UNIFORMS := """global uniform vec4 fx_char_light;       // LANE B: the Meteor's fire on him and her: centre, energy
global uniform vec4 fx_char_light_col;   // its colour (linear) and its range (m)
"""

const CHAR_FIRE_LIGHT := """	// LANE B: the Meteor's fire, in this (the sun's) pass
	if (LIGHT_IS_DIRECTIONAL && fx_char_light.w > 0.0) {
		vec3 wn = normalize((INV_VIEW_MATRIX * vec4(NORMAL, 0.0)).xyz);
		vec3 fd = fx_char_light.xyz - v_world;
		float dist = max(length(fd), 1e-3);
		float win = pow(max(1.0 - pow(dist / max(fx_char_light_col.w, 1e-3), 4.0), 0.0), 2.0);
		float e = max(dot(wn, fd / dist), 0.0) * win / dist;
		float s = smoothstep(0.05 - band_soft * 0.3, 0.05 + band_soft * 0.3, e) * 0.45
			+ smoothstep(0.30 - band_soft * 0.3, 0.30 + band_soft * 0.3, e) * 0.55;
		DIFFUSE_LIGHT += fx_char_light_col.rgb * fx_char_light.w * s;
	}
"""


static func with_char_fire(code: String) -> String:
	"""LANE B: a character ramp material's live code (CHAR_SHADER) with the Meteor's fire folded into the
	sun's pass (see above)."""
	var s := code
	assert(s.count("uniform float char_mark = 0.5;\n") == 1, "with_char_fire: the char mark uniform moved")
	s = s.replace("uniform float char_mark = 0.5;\n", "uniform float char_mark = 0.5;\n" + CHAR_FIRE_UNIFORMS)
	var tail := "	SPECULAR_LIGHT += web_sheen;      // the phone build's sky reflection; 0 on the desktop\n}\n"
	assert(s.count(tail) == 1, "with_char_fire: the ramp's light() tail moved")
	return s.replace(tail, "	SPECULAR_LIGHT += web_sheen;      // the phone build's sky reflection; 0 on the desktop\n"
		+ CHAR_FIRE_LIGHT + "}\n")


static func _shader(code: String) -> Shader:
	"""ONE Shader RESOURCE PER SOURCE, shared by every material that uses it.

	A fresh Shader per material means a fresh COMPILE per material, and the props turned that
	from a detail into the scene's whole load time: 70 prop meshes is 70 compiles of the same
	120 lines, and on Metal each one is a pipeline build. Sharing the resource is also what
	lets `_world_mats` set a uniform on 70 materials without 70 pipeline swaps at draw."""
	if _shader_cache.has(code):
		return _shader_cache[code]
	var s := Shader.new()
	s.code = code
	_shader_cache[code] = s
	return s


static func world_material(fbm: Texture2D, base: Color, params := {}) -> ShaderMaterial:
	# "_two_sided" is a SELECTOR, not a uniform (keys with a leading underscore never reach
	# the shader). The ramp culls back faces, which is right for a closed solid and wrong for
	# a heather tussock: its blades are single planes, authored `doubleSided` in the GLB, and
	# with cull_back every blade turned away from the camera vanishes -- about half of them.
	# Godot flips NORMAL for a back face when culling is off, so the ramp lights the far side
	# of a blade as its own side. (The barrow ships its heather ONE-sided now, measured: see
	# barrow_world.heather_two_sided. The selector stays for the next asset that needs it.)
	var two := bool(params.get("_two_sided", false))
	var code := WORLD_SHADER.replace("cull_back", "cull_disabled") if two else WORLD_SHADER
	if is_compatibility() and float(params.get("mesh_mark", 1.0)) < 0.5:
		# THE WEB'S "THIN" MARK: the stencil, since Compatibility has no roughness buffer
		code = stencil_write(code, STENCIL_THIN)
	var m := ShaderMaterial.new()
	m.shader = _shader(code)
	m.set_shader_parameter("wash_noise", fbm)
	m.set_shader_parameter("mottle_noise", fbm)
	m.set_shader_parameter("base_color", base)
	for k in params:
		if String(k).begins_with("_"):
			continue
		m.set_shader_parameter(k, params[k])
	return m


static func ground_material(fbm: Texture2D, tiles: Dictionary, splat: Texture2D,
		params := {}) -> ShaderMaterial:
	"""The tiled ground. `tiles` is keyed by splat-class NAME, so a missing tile is a missing
	key rather than a silently-shifted index -- the class order (snow, path, rock, heather,
	ice) is stated in three places in this project and an off-by-one between any two of them
	would paint the tarn with heather and look like an art decision."""
	var m := ShaderMaterial.new()
	m.shader = _shader(GROUND_SHADER)
	m.set_shader_parameter("wash_noise", fbm)
	m.set_shader_parameter("mottle_noise", fbm)
	for k in ["snow", "path", "rock", "heather", "ice"]:
		if tiles.has(k) and tiles[k] != null:
			m.set_shader_parameter("tile_" + k, tiles[k])
	if splat != null:
		m.set_shader_parameter("splat_w", splat)
	for k in params:
		m.set_shader_parameter(k, params[k])
	return m


static func load_tile(path: String) -> ImageTexture:
	"""OFF A REAL FILE, WITH MIPMAPS GENERATED HERE, for the same reason
	barrow_heightfield.gd loads its PNG rather than its import: what the importer produces
	for these is a mipless CompressedTexture2D (mipmaps/generate=false in every one of the
	six .import files), and a 1024² tile repeating every 2.5 m minifies about 5:1 at the play
	camera. Without mips that is not "slightly soft", it is a crawling moiré that reads as a
	broken shader. Generating them here also keeps the .import files -- generated artifacts a
	re-import rewrites -- out of the commit.

	COSTS ~35 ms PER TILE and there are five; timed by the caller and reported, because it is
	cold-start time Matt pays looking at a black window."""
	var img := _image_from(path)
	if img == null:
		push_error("[paintstack] cannot load tile %s" % path)
		return null
	img.generate_mipmaps()
	return ImageTexture.create_from_image(img)


static func _image_from(path: String) -> Image:
	"""THE IMPORTED RESOURCE FIRST, THE RAW FILE SECOND, and the order is about the exported
	.app rather than about the editor.

	Image.load() on a res:// path reads the FILE. In an export the file is only in the pck if
	an include_filter puts it there -- otherwise all six tiles come back null and the ground
	renders in base_color, which looks like a lighting bug and is a missing-asset bug. Godot
	says so itself: `Loaded resource as image file, this will not work on export`.

	load() reads the IMPORTED resource, which always ships. Both are kept because they fail in
	opposite conditions: the import can be absent in a fresh checkout before the first
	--import, and the raw file can be absent in an export. Whichever answers, answers."""
	var res = load(path)
	if res is Texture2D:
		var i: Image = (res as Texture2D).get_image()
		if i != null:
			if i.is_compressed():
				i.decompress()
			return i
	var img := Image.new()
	if img.load(path) != OK:
		return null
	if img.is_compressed():
		img.decompress()
	return img


static func splat_weight_texture(png: String, classes := 5, blur_px := 7,
		implied_class := 0) -> Dictionary:
	"""ID MAP -> BLURRED WEIGHT MAP, on the CPU, once at load.

	The shipped splat is an 8-bit image whose VALUE is a class id. Three things make it
	unusable as-is on the GPU and all three are silent:

	  - bilinear filtering of ids invents classes at every border (see GROUND_SHADER note 2);
	  - nearest filtering gives a hard 5 cm staircase along every border at 0.05 m/px;
	  - the importer compresses it, and a lossy id is a different material.

	So: expand to `classes` weight fields, blur each with two box passes (a box twice is
	close enough to a Gaussian for a border feather and is O(n) rather than O(n*r)), and
	normalise so the five sum to exactly 1. `implied_class` is dropped from the packing and
	reconstructed in the shader as 1 - sum, which is where all four channels' quantisation
	error lands -- so it must be the class that is near 1 over the largest area.

	Returns the texture AND the numbers: the class shares before and after the blur (a blur
	that moved a share by more than a couple of points has eaten a thin feature), and the
	worst reconstruction error of the implied channel, measured rather than reasoned about."""
	var out := {"tex": null, "report": {}}
	var img := _image_from(png)
	if img == null:
		push_error("[paintstack] cannot load splat %s" % png)
		return out
	var w := img.get_width()
	var h := img.get_height()
	var n := w * h
	# ONE FLAT ARRAY, class-major, and not an Array of PackedFloat32Array. `fields[c][i] = v`
	# on the nested form does not write: indexing an Array yields the packed array BY VALUE,
	# so the write lands on a temporary and is thrown away -- in Godot 4.6 it raises rather
	# than silently dropping it, which is the only reason this was a crash and not an
	# all-snow ground that looked like a tuning problem.
	var fields := PackedFloat32Array()
	fields.resize(n * classes)
	var raw_counts := []
	for c in classes:
		raw_counts.append(0)
	for y in h:
		for x in w:
			# 8-bit grey: the id is the byte. get_pixel returns 0..1, so *255 and round.
			var id: int = clampi(int(round(img.get_pixel(x, y).r * 255.0)), 0, classes - 1)
			fields[id * n + y * w + x] = 1.0
			raw_counts[id] += 1
	for c in classes:
		var f := fields.slice(c * n, (c + 1) * n)
		for _pass in 2:
			f = _box_blur(f, w, h, blur_px)
		for i in n:
			fields[c * n + i] = f[i]
	# normalise, and count what each class ends up owning
	var blurred_sum := []
	for c in classes:
		blurred_sum.append(0.0)
	for i in n:
		var s := 0.0
		for c in classes:
			s += fields[c * n + i]
		s = maxf(s, 1e-6)
		for c in classes:
			var v: float = fields[c * n + i] / s
			fields[c * n + i] = v
			blurred_sum[c] = float(blurred_sum[c]) + v
	# pack: every class except the implied one, in ascending class order, into RGBA
	var order := []
	for c in classes:
		if c != implied_class:
			order.append(c)
	var packed := Image.create(w, h, false, Image.FORMAT_RGBA8)
	var worst := 0.0
	for y in h:
		for x in w:
			var i := y * w + x
			var v := [0.0, 0.0, 0.0, 0.0]
			for j in mini(order.size(), 4):
				v[j] = fields[int(order[j]) * n + i]
			packed.set_pixel(x, y, Color(v[0], v[1], v[2], v[3]))
			# what the shader will reconstruct for the implied class, through the same
			# 8-bit rounding the texture will store
			var q := 0.0
			for j in mini(order.size(), 4):
				q += round(float(v[j]) * 255.0) / 255.0
			worst = maxf(worst, absf((1.0 - q) - fields[implied_class * n + i]))
	var tex := ImageTexture.create_from_image(packed)
	out["tex"] = tex
	out["img"] = packed          # the CPU copy: see make_fbm_image for why not get_image()
	out["report"] = {
		"png": png, "size": [w, h], "classes": classes,
		"blur_px_per_pass": blur_px, "passes": 2,
		"implied_class": implied_class,
		"packed_rgba_classes": order.slice(0, 4),
		"share_before_blur_pct": _shares(raw_counts, float(n)),
		"share_after_blur_pct": _shares(blurred_sum, float(n)),
		"worst_implied_channel_error": snappedf(worst, 1e-5),
		"_error_budget": "4 channels at 1/255 each; anything over 0.02 means the implied class is the wrong one",
	}
	return out


static func _shares(counts: Array, total: float) -> Array:
	var o := []
	for c in counts:
		o.append(snappedf(float(c) / maxf(total, 1.0) * 100.0, 0.01))
	return o


static func _box_blur(src: PackedFloat32Array, w: int, h: int, r: int) -> PackedFloat32Array:
	"""Separable running-sum box blur with CLAMPED edges. Clamped and not wrapped: the splat
	is a 15 m square of a 92 m world, not a tiling texture, and wrapping would carry the
	tarn's ice round to the far edge."""
	var tmp := PackedFloat32Array()
	tmp.resize(w * h)
	var dst := PackedFloat32Array()
	dst.resize(w * h)
	var inv := 1.0 / float(2 * r + 1)
	for y in h:
		var row := y * w
		var acc := 0.0
		for k in range(-r, r + 1):
			acc += src[row + clampi(k, 0, w - 1)]
		for x in w:
			tmp[row + x] = acc * inv
			acc += src[row + clampi(x + r + 1, 0, w - 1)] - src[row + clampi(x - r, 0, w - 1)]
	for x in w:
		var acc2 := 0.0
		for k in range(-r, r + 1):
			acc2 += tmp[clampi(k, 0, h - 1) * w + x]
		for y in h:
			dst[y * w + x] = acc2 * inv
			acc2 += tmp[clampi(y + r + 1, 0, h - 1) * w + x] - tmp[clampi(y - r, 0, h - 1) * w + x]
	return dst


static func adopt_prop(node: Node3D, fbm: Texture2D, ink: Color, hull_world_m: float,
		params := {}) -> Dictionary:
	"""A LOADED GLB, BROUGHT UNDER THE SAME LIGHT AND GIVEN THE SAME PEN.

	Identical in spirit to adopt_character and different in one way that matters: the props
	arrive with NO ink line, so one is built here -- a copy of each mesh, inflated along its
	own normal and culled front, in the one pen. That is the T9 hull, and the T9 failure mode
	comes with it: on an OPEN mesh the inflated copy is not a rim, it IS the surface, flat and
	1 cm proud. These are closed image-to-3D solids so it is the right pen for them -- but the
	measurement is what says so, not this comment, and the capture isolates the hull's pixels
	by hiding exactly these meshes.

	`hull_world_m` is the line's width IN WORLD METRES and is divided by the node's own scale,
	because VERTEX += NORMAL * width happens in model space and the fit scale is applied after
	it. A prop normalised to 2.71 m from a 1.0 m export carries a scale of 2.71, and a width
	not divided by it draws a line 2.71x too thick on exactly the tallest stones."""
	var saved := {"meshes": [], "inks": []}
	for n in node.find_children("*", "MeshInstance3D", true, false):
		var mi := n as MeshInstance3D
		if mi.mesh == null or String(mi.name).ends_with("_ink"):
			continue
		var tex: Texture2D = null
		var act := mi.get_active_material(0) as BaseMaterial3D
		if act != null:
			tex = act.albedo_texture if act.albedo_texture != null else act.emission_texture
		var p := params.duplicate()
		p["use_tex"] = tex != null
		var ramp := world_material(fbm, Color(0.62, 0.60, 0.58), p)
		if tex != null:
			ramp.set_shader_parameter("albedo_tex", tex)
		saved["meshes"].append({"mi": mi, "mat": mi.material_override, "ramp": ramp})
		mi.material_override = ramp
		# A HULL WIDTH OF ZERO MEANS NO HULL, and it is how a caller says "this mesh has no
		# inside". See barrow_world._hull_for: on a heather tussock or a birch's twigs the
		# inflated copy is not a rim around the stem, it IS the stem -- at the play camera a
		# 3 m tree with 8 mm twigs inked solid black, and nineteen tussocks read as scribble.
		if hull_world_m <= 0.0:
			continue
		# the pen, as a sibling so it inherits the same transform
		var sc: Vector3 = mi.global_transform.basis.get_scale()
		var s: float = maxf((absf(sc.x) + absf(sc.y) + absf(sc.z)) / 3.0, 1e-6)
		var line := MeshInstance3D.new()
		line.name = String(mi.name) + "_ink"
		line.mesh = mi.mesh
		line.material_override = hull_ink_material(hull_world_m / s, ink)
		line.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		mi.add_child(line)
		saved["inks"].append({"mi": line, "width_model": hull_world_m / s})
	return saved


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


# THE TRANSPARENT ORDER, in one place. The post pass paints its pre-transparent screen copy
# over the whole frame at POST_PRIORITY; what must still be SEEN and is transparent draws after
# it: the phone build's depthless heather cards (BarrowWorld.WEB_CARD_PRIORITY, 125) and every
# particle system -- the snowfall, the ridge gust, the kicked-up puffs (126).
const POST_PRIORITY := 120
const AFTER_POST_PRIORITY := 126


# THE WEB PEN'S MARKS, IN THE STENCIL (R-C9-83). The desktop pen reads three per-pixel marks from
# the normal-roughness buffer -- him, thin growth, the near side of snow -- and Compatibility has
# no such buffer: on the phone build the depth-only pen inked the junipers and birches solid and
# drew every edge of his trail. The stencil carries two of them instead. Thin props and the snow
# field WRITE a class (stencil_write, on Compatibility only); the post pass is drawn as THREE
# passes of the same quad, chained by next_pass, each reading one class (compare_equal), so each
# pixel is inked by exactly one of: full pen (0), the thin pen (1, thin_pen_scale), no pen (2).
# A stencil cannot be SAMPLED, so this is the centre-pixel test only -- which is the one the
# desktop's snow mark uses, and the side a positive second difference draws its line on.
const STENCIL_THIN := 1
const STENCIL_SNOW := 2


static func stencil_write(code: String, ref: int) -> String:
	"""`code` with a stencil write of `ref` on every fragment it draws, after its render_mode."""
	return _after_render_mode(code, "stencil_mode write, compare_always, %d;" % ref)


static func _after_render_mode(code: String, line: String) -> String:
	var lines := code.split("\n")
	for i in lines.size():
		if lines[i].strip_edges().begins_with("render_mode"):
			lines.insert(i + 1, line)
			return "\n".join(lines)
	assert(false, "no render_mode line to put '%s' after" % line)
	return code


static func post_set(mat: Material, key: String, value) -> void:
	"""A post-pass parameter onto the pass AND its chained stencil passes (the phone build's)."""
	var m := mat
	while m != null:
		if m is ShaderMaterial:
			(m as ShaderMaterial).set_shader_parameter(key, value)
		m = m.next_pass


static func post_material(paper: Texture2D, ink: Color, params := {}) -> ShaderMaterial:
	var m := _post_pass(paper, ink, params, post_shader_code(0))
	if is_compatibility():
		# the web's two further passes, one per stencil class (see STENCIL_THIN)
		var thin := _post_pass(paper, ink, params, post_shader_code(STENCIL_THIN))
		thin.set_shader_parameter("stencil_thin", 1.0)
		var snow := _post_pass(paper, ink, params, post_shader_code(STENCIL_SNOW))
		snow.set_shader_parameter("stencil_snow", 1.0)
		m.next_pass = thin
		thin.next_pass = snow
	return m


static func _post_pass(paper: Texture2D, ink: Color, params: Dictionary, code: String) -> ShaderMaterial:
	var m := ShaderMaterial.new()
	m.shader = _shader(code)
	m.set_shader_parameter("paper_tex", paper)
	m.set_shader_parameter("ink_color", ink)
	# drawn LAST among the world. It reads hint_screen_texture, which puts it in the
	# transparent queue -- and the screen is copied ONCE, BEFORE the transparent pass, on
	# both renderers. So everything transparent drawn before this pass is painted over by
	# the copy it did not make it into: the falling snow drew 28 px of the play frame on the
	# desktop and 0 on the web (the air on/off pair, tools/probe_web_look.gd --air-ab), until
	# the particles moved AFTER it (AFTER_POST_PRIORITY). The original intent -- grade the
	# particles -- is not reachable with one copy; ungraded white flakes are the cheaper truth.
	m.render_priority = POST_PRIORITY
	for k in params:
		m.set_shader_parameter(k, params[k])
	return m


static func is_compatibility() -> bool:
	return RenderingServer.get_current_rendering_method() == "gl_compatibility"


static func is_web() -> bool:
	"""THE PHONE BUILD'S BRANCHES, in one predicate: true in the browser, and true on the desktop
	when the command line carries `-- --as-web` -- so the desktop harness can put the web path
	under the Compatibility renderer and capture it with stdout, instead of by browser only
	(tools/probe_web_look.gd)."""
	return OS.has_feature("web") or OS.get_cmdline_user_args().has("--as-web")


static func web_query(key: String) -> String:
	"""A value off the phone page's own URL (`?msaa=0&scale3d=0.7`), "" when absent or not on the
	web. The tuning levers are read here so a phone can be tried at another setting without a
	rebuild."""
	if not OS.has_feature("web"):
		return ""
	var v = JavaScriptBridge.eval("new URLSearchParams(window.location.search).get('%s') || ''" % key, true)
	return String(v) if typeof(v) == TYPE_STRING else ""


static func _materials_under(root: Node) -> Array:
	"""Every material a GeometryInstance3D under `root` draws with, once each, as [node, material]:
	its override, its surface overrides, and -- where it has no override -- its mesh's own (a
	MultiMesh's, a particle system's draw pass)."""
	var out := []
	var seen := {}
	for n in root.find_children("*", "GeometryInstance3D", true, false):
		var gi := n as GeometryInstance3D
		var mats: Array = []
		if gi.material_override != null:
			mats.append(gi.material_override)
		var mesh: Mesh = null
		if gi is MeshInstance3D:
			mesh = (gi as MeshInstance3D).mesh
			if mesh != null:
				for s in mesh.get_surface_count():
					var o := (gi as MeshInstance3D).get_surface_override_material(s)
					if o != null:
						mats.append(o)
		elif gi is MultiMeshInstance3D and (gi as MultiMeshInstance3D).multimesh != null:
			mesh = (gi as MultiMeshInstance3D).multimesh.mesh
		elif gi is GPUParticles3D:
			mesh = (gi as GPUParticles3D).draw_pass_1
		if mesh != null and gi.material_override == null:
			for s in mesh.get_surface_count():
				var m := mesh.surface_get_material(s)
				if m != null:
					mats.append(m)
		for m in mats:
			# and each material's next_pass chain (the web's three post passes are one)
			while m != null and not seen.has(m):
				seen[m] = true
				out.append([gi, m])
				m = m.next_pass
	return out


static func move_ambient_into_light(root: Node, env: Environment) -> Dictionary:
	"""THE PHONE BUILD'S LIGHT SUM (see ambient_in_light in RAMP_UNIFORMS). Every material that
	carries the ramp gets the environment's ambient -- linear, times its energy: what the engine
	would have added in its base pass -- and the environment's own is zeroed, so the ambient is
	added ONCE, in the sun's pass, in linear light. Counts what it set, and NAMES any lit
	material without the ramp: that one would lose its ambient, and should be seen to."""
	var amb := env.ambient_light_color.srgb_to_linear() * env.ambient_light_energy
	var v := Vector3(amb.r, amb.g, amb.b)
	var set_n := 0
	var unramped := []
	for pair in _materials_under(root):
		var gi: GeometryInstance3D = pair[0]
		var m: Material = pair[1]
		var sm := m as ShaderMaterial
		if sm != null and sm.shader != null and sm.shader.code.contains("ambient_in_light"):
			sm.set_shader_parameter("ambient_in_light", v)
			set_n += 1
		elif m is BaseMaterial3D and (m as BaseMaterial3D).shading_mode != BaseMaterial3D.SHADING_MODE_UNSHADED:
			unramped.append("%s (%s)" % [String(gi.name), m.get_class()])
		elif sm != null and sm.shader != null and not sm.shader.code.contains("unshaded"):
			unramped.append("%s (ShaderMaterial)" % String(gi.name))
	env.ambient_light_energy = 0.0
	return {"ramp_materials_set": set_n, "ambient_linear": [snappedf(v.x, 1e-4), snappedf(v.y, 1e-4),
			snappedf(v.z, 1e-4)], "lit_without_ramp": unramped,
			"_why": "Compatibility adds a shadowed light's pass to the base pass after both are sRGB-encoded"}


# THE WEB'S ALBEDO IS sRGB-ENCODED (R-C9-83), and every number that assumed otherwise moves.
# Compatibility runs `albedo = srgb_to_linear(albedo)` AFTER the fragment shader, so the whole
# fragment's colour maths happens on sRGB-encoded values: a source_color texture or uniform
# arrives raw, and whatever the shader writes to ALBEDO is read back as sRGB. Measured with a
# micro-test, an unshaded quad writing a plain vec3 of 0.5: 188 on Forward+ (0.5 is linear),
# 128 on Compatibility (0.5 is sRGB); a source_color 0.5: 127 and 128. The consequences here:
#   LINEAR MULTIPLIERS ON THE ALBEDO (tex_tint, snow_tint, albedo_mul): k on sRGB is ~k^2.2 on
#     light. The juniper's (0.354, 0.163, 0.020) turned near-black -- 60% of the thin props'
#     pixels under 40 -- the snow's (1.03, 1.10, 1.17) blue, the heather cards' saturated.
#     Each is raised to 1/2.2: the same multiply, in the space it runs in.
#   MULTIPLICATIVE NOISE (mottle_amp, hatch_amp, snow_mottle, tone_jitter, and the post pass's
#     paper grain, paper_amount): a +-a swing on sRGB is +-2.2a on light, so each is / 2.2.
#   A COLOUR USED AS LIGHT (the ramp's shadow_color, source_color): the desktop linearises it
#     and light() reads linear; here it arrived raw, and the shadowed snow came out (183, 191,
#     209) for the desktop's (163, 169, 191). Linearised here, once.
# The power law is the sRGB curve's approximation; the curve's toe (under 0.04) is where the two
# still differ. The shaders' own literal multipliers (the heather's hue slide, the snow's warm
# edge) are left as they are.
const WEB_GAMMA := 2.2
const WEB_SHEEN_THIN := Vector3(0.032, 0.037, 0.047)
const WEB_SHEEN_SNOW := Vector3(0.005, 0.008, 0.014)
const WEB_SHEEN_OTHER := Vector3(0.005, 0.006, 0.010)
const _WEB_TINTS := ["tex_tint", "snow_tint", "albedo_mul"]
const _WEB_AMPLITUDES := ["mottle_amp", "hatch_amp", "snow_mottle", "tone_jitter", "paper_amount"]


static func web_color_space(root: Node) -> Dictionary:
	"""The Compatibility renderer's colour-space corrections, onto every material under `root`
	(see WEB_GAMMA above). Once, after everything is built; counts what it moved."""
	var n := {"tints": 0, "amplitudes": 0, "shadow_colour": 0}
	for pair in _materials_under(root):
		var sm := pair[1] as ShaderMaterial
		if sm == null or sm.shader == null:
			continue
		var code: String = sm.shader.code
		for key in _WEB_TINTS:
			if code.contains("uniform vec3 %s " % key):
				var tv := _as_vec3(_param_or_default(sm, key))
				sm.set_shader_parameter(key, Vector3(pow(maxf(tv.x, 0.0), 1.0 / WEB_GAMMA),
					pow(maxf(tv.y, 0.0), 1.0 / WEB_GAMMA), pow(maxf(tv.z, 0.0), 1.0 / WEB_GAMMA)))
				n["tints"] += 1
		for key in _WEB_AMPLITUDES:
			if code.contains("uniform float %s " % key):
				sm.set_shader_parameter(key, float(_param_or_default(sm, key)) / WEB_GAMMA)
				n["amplitudes"] += 1
		if code.contains("uniform vec3 shadow_color : source_color"):
			var c := _as_color(_param_or_default(sm, "shadow_color")).srgb_to_linear()
			sm.set_shader_parameter("shadow_color", Vector3(c.r, c.g, c.b))
			n["shadow_colour"] += 1
		if code.contains("uniform vec3 web_sheen"):
			var sheen := WEB_SHEEN_OTHER
			if code.contains("uniform sampler2D field_tex"):
				sheen = WEB_SHEEN_SNOW
			elif code.contains("uniform float mesh_mark") and float(_param_or_default(sm, "mesh_mark")) < 0.5:
				sheen = WEB_SHEEN_THIN
			sm.set_shader_parameter("web_sheen", sheen)
			n["sheen"] = int(n.get("sheen", 0)) + 1
	return n


static func _param_or_default(sm: ShaderMaterial, key: String):
	var v = sm.get_shader_parameter(key)
	if v == null:
		v = RenderingServer.shader_get_parameter_default(sm.shader.get_rid(), key)
	return v


static func _as_vec3(v) -> Vector3:
	if v is Vector3:
		return v
	if v is Color:
		return Vector3((v as Color).r, (v as Color).g, (v as Color).b)
	return Vector3.ONE


static func _as_color(v) -> Color:
	if v is Color:
		return v
	if v is Vector3:
		return Color((v as Vector3).x, (v as Vector3).y, (v as Vector3).z)
	return Color(1, 1, 1)


static func post_shader_code(stencil_ref := 0) -> String:
	"""THE PEN, AND ITS WEB FALLBACK (the phone build, R-C9-83). The Compatibility renderer the
	web runs on has no normal-roughness buffer, and that buffer carries three things the pen
	reads: the crease term, and the per-pixel marks that keep the pen off him (0.5), off thin
	growth (0.25) and off the near side of snow (0.75). So on Compatibility the pen is DEPTH
	ONLY: the same positive-side second difference, the same threshold, the same sky test --
	and none of the marks, which the web build answers another way (the heather is drawn as
	blended cards that write no depth, and his own hull is hidden so he keeps one pen)."""
	if not is_compatibility():
		return POST_SHADER
	var s := POST_SHADER.replace(
		"uniform sampler2D nrm_tex : hint_normal_roughness_texture, filter_nearest;\n", "")
	s = s.replace("vec3 _nrm(vec2 uv) { return texture(nrm_tex, uv).xyz * 2.0 - 1.0; }",
		"vec3 _nrm(vec2 uv) { return vec3(0.0, 0.0, 1.0); }")
	s = s.replace("return 1.0 - step(char_mark_tol, abs(texture(nrm_tex, uv).a - char_mark_ref));",
		"return 0.0;")
	# thin and snow come from the STENCIL instead: each of the three passes reads one class
	s = s.replace("return 1.0 - step(char_mark_tol, abs(texture(nrm_tex, uv).a - thin_mark_ref));",
		"return stencil_thin;")
	s = s.replace("float sn = 1.0 - step(char_mark_tol, abs(texture(nrm_tex, uv).a - snow_mark_ref));",
		"float sn = stencil_snow;")
	# (barrow_full) the painted mark has no stencil class: nothing painted exists on the web build
	s = s.replace("float pt = 1.0 - step(char_mark_tol, abs(texture(nrm_tex, uv).a - painted_mark_ref));",
		"float pt = 0.0;")
	s = s.replace("uniform float snow_mark_ref = 0.75;",
		"uniform float snow_mark_ref = 0.75;\nuniform float stencil_thin = 0.0;\nuniform float stencil_snow = 0.0;")
	s = _after_render_mode(s, "stencil_mode read, compare_equal, %d;" % stencil_ref)
	# AND THE DEPTH IS OPENGL'S: NDC z runs -1..1 (2d - 1), where the desktop's Vulkan takes d as
	# is. Read the desktop way, every depth break measures HALF its size on the orthographic
	# camera, and the pen draws half as much of the world.
	var lin := "vec4 v = inv_proj * vec4(vec3(uv * 2.0 - 1.0, d), 1.0);"
	assert(s.contains(lin), "the pen's depth read moved; the web fallback must follow it")
	s = s.replace(lin, "vec4 v = inv_proj * vec4(vec3(uv, d) * 2.0 - 1.0, 1.0);")
	assert(not s.contains("nrm_tex"), "the web pen still reads the normal-roughness buffer")
	assert(s.contains("stencil_thin;") and s.contains("float sn = stencil_snow;"),
		"the web pen's stencil classes did not replace the marks")
	return s


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
static func winter_sun(elev_deg := 55.0, screen_az_deg := 305.0) -> DirectionalLight3D:
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
	# THE SUN CAME UP FROM 17 DEGREES TO 55, AND THE BIAS CAME DOWN WITH IT (R-C9-74 note 3).
	# Matt, on the 15:20 build: "The lighting on the character and 3D objects throws very odd
	# shadows on the ground." Two measured causes, and both are this function's:
	#
	#   LENGTH. A shadow is height/tan(elevation) long. At 17 degrees that is 3.27x the
	#     caster -- a 1.85 m man throwing a 6.0 m shadow across the frame, which is what
	#     "very odd" is. At 55 degrees it is 0.70x, inside the 0.8x the ruling asks for.
	#   THE GAP AT THE FOOT. shadow_normal_bias pushes the shadow lookup along the SURFACE
	#     NORMAL, so it moves the shadow away from its caster's base by roughly
	#     normal_bias * texel / tan(elev). At 3.0 and 17 degrees that gap is visible; it is
	#     why every shadow started a hand's breadth from the thing casting it.
	#
	# Raising the sun shrinks the depth error a texel represents by tan(55)/tan(17) = 4.7x,
	# so the bias that 17 degrees needed is 4.7x more than 55 does. 0.55 and 0.03 are the
	# sweep is tools/probe_shadow.gd and its answer was not the one I expected: on the mound
	# -- the scene's only curved surface, and so the only thing that CAN self-shadow now the
	# floor is flat -- there is NO measurable acne at any normal_bias from 0.0 to 3.0. Against
	# a shadows-off control at 0.18407 dark share, the excess runs 0.0124 / 0.0119 / 0.0122 /
	# 0.0116 / 0.0105 / 0.0038 for 0.0 / 0.15 / 0.35 / 0.55 / 1.2 / 3.0, and that excess is the
	# props' REAL shadows, not acne: it is flat until 1.2 and then collapses, which is bias
	# eating the shadow rather than cleaning it.
	#
	# The snow-lab drax derives these instead by scaling the shipped 17-degree pair by
	# tan(17)/tan(55) = 0.214, which gives 0.028 / 0.64. That agrees with the measurement on
	# the bias term (0.028 against 0.03) and is four times larger on the normal term. The
	# sweep says smaller is safe here and smaller keeps the shadow attached, so the measured
	# value stands and theirs is recorded beside it rather than silently discarded.
	#
	# So "the smallest value with no acne" is measured as 0.0, and 0.15 is taken instead --
	# one step of margin for geometry the sweep does not cover, keeping 95.8% of the shadow
	# area that zero produces where 3.0 keeps 30%. Blur unchanged, per the ruling.
	l.shadow_bias = 0.03
	l.shadow_normal_bias = 0.15
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
	# NO DISTANCE FOG. It was measured changing EXACTLY 0.0% of the play frame -- the frame
	# spans ~53-67 m of view depth and the fog began at 68 m, so it ended where the fog
	# started. Rather than drag it inward, it is off: a 13 m deep tactical frame has no
	# distance for aerial perspective to describe, and the wide framings get theirs from the
	# sky. What is left is the HEIGHT term alone, pooling in the basin, which is the one
	# place in this world where low mist is a thing the player can be standing in.
	#
	# EXPONENTIAL mode with fog_density 0 is what leaves the height term running by itself;
	# DEPTH mode gates on fog_depth_begin and takes the height fog with it. That is measured
	# in tools/probe_fog.gd, not assumed -- it is exactly the kind of coupling that returns
	# a clean zero and looks like a tuning problem.
	env.fog_enabled = true
	env.fog_mode = Environment.FOG_MODE_EXPONENTIAL
	env.fog_light_color = Color(0.815, 0.870, 0.940)
	env.fog_light_energy = 1.0
	env.fog_sun_scatter = 0.05
	env.fog_density = 0.0                 # the distance term, off
	env.fog_sky_affect = 0.0
	env.fog_height = 0.0                  # the scene sets this to the basin's own rim
	# 0.18: chosen off the measured sweep (tools/probe_fog.gd), not by eye. At the play camera
	# over the basin it lifts the frame by about 2.8% per channel across 98% of it, with the
	# mound control -- which stands 5.9 m above the fog top -- changing by EXACTLY 0.00%.
	# The sweep: 0.006 -> 0.10%, 0.025 -> 0.42%, 0.05 -> 0.83%, 0.20 -> 3.07%, 0.55 -> 7.05%.
	env.fog_height_density = 0.18
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
	mm.render_priority = AFTER_POST_PRIORITY      # after the post pass, or it paints them out
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
	mm.render_priority = AFTER_POST_PRIORITY      # after the post pass, or it paints them out
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


static func measure_snow(groups: Array, img: Image, covered_at := 0.5,
		max_tris_per_group := 24000) -> Dictionary:
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
		# THE GROUND SCALES THE DRIFT PER SPLAT CLASS (GROUND_SHADER note 5) and this is the
		# CPU's copy of that factor -- supplied by the scene as a Callable over world xz, so
		# there is no second implementation of the splat lookup living in here to drift out of
		# step with the first. A group without one measures the plain layer, as before.
		var keep: Callable = g.get("amount_scale", Callable())
		var up_a := [0.0, 0.0, 0.0, 0.0]
		var sn_a := [0.0, 0.0, 0.0, 0.0]
		var down_a := 0.0
		var down_snow := 0.0
		var tris := 0
		# A UNIFORM STRIDE, because the props are now 1.2 MILLION triangles and this loop is
		# GDScript doing a transform and two bilinear noise fetches per triangle. At 1:1 it
		# does not finish; at a stride it is the same estimator on an evenly spaced sample of
		# the same population, and the areas it sums are the areas of the triangles it took
		# -- so every share stays a ratio of like to like. The stride is reported; a share
		# taken at stride 50 and a share taken at 1 that disagree would mean the sample is
		# not uniform, and the terrain group (stride 1) is the control for that.
		var total_tris := 0
		for mi0 in g["meshes"]:
			var nd0 := mi0 as MeshInstance3D
			if nd0 == null or nd0.mesh == null:
				continue
			for s0 in nd0.mesh.get_surface_count():
				# the index COUNT, not a copy of the index array -- see barrow_world's note
				if nd0.mesh is ArrayMesh:
					total_tris += (nd0.mesh as ArrayMesh).surface_get_array_index_len(s0) / 3
				else:
					var ix0 = nd0.mesh.surface_get_arrays(s0)[Mesh.ARRAY_INDEX]
					total_tris += (ix0.size() / 3) if ix0 != null else 0
		var stride: int = maxi(1, int(ceil(float(total_tris) / float(maxi(max_tris_per_group, 1)))))
		var step := 3 * stride
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
				for t in range(0, ix.size() - 2, step):
					var p0 := xf * v[ix[t]]
					var p1 := xf * v[ix[t + 1]]
					var p2 := xf * v[ix[t + 2]]
					var area: float = (p1 - p0).cross(p2 - p0).length() * 0.5
					if area <= 0.0:
						continue
					var wn := (nb * ((nn[ix[t]] + nn[ix[t + 1]] + nn[ix[t + 2]]) / 3.0)).normalized()
					var cen := (p0 + p1 + p2) / 3.0
					var a_here := amt
					if keep.is_valid():
						a_here *= float(keep.call(cen))
					var k := snow_at(img, cen, wn, thr, jit, soft, nsc, a_here)
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
			"triangles_in_group": total_tris,
			"triangles_sampled": tris,
			"stride": stride,
			"per_class_amount_scale": keep.is_valid(),
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
			"_of": "the LAYER function alone, before any per-class amount_scale -- that factor "
				+ "is a property of the ground's splat, not of this function, and folding it "
				+ "in would make a correct shader fail a check about something else",
		}
	out["instrument_check_known_faces"] = checks
	return out


# --- reading a frame back ------------------------------------------------------
static func srgb_to_linear(c: float) -> float:
	return c / 12.92 if c <= 0.04045 else pow((c + 0.055) / 1.055, 2.4)


static func linear_to_srgb(c: float) -> float:
	return c * 12.92 if c <= 0.0031308 else 1.055 * pow(c, 1.0 / 2.4) - 0.055
