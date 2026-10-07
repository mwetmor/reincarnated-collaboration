extends RefCounted
## BV2F lane PT, DEV-5 (R-C9-194): THE ANIMATED WATER over the pilot's painted sea + the floes riding the swell, pilot-only.
## WATER_SHADER is R-C9-159's (barrow_full/godot/scripts/barrow_v2_sw.gd), COPIED VERBATIM; "base = the painting" is a
## UNIFORM setting (paint_mix = 1.0: the colour IS the projected painting, the swell/ripples/foam move over it), not a code
## change. The floe bob is R-C9-159's FLOE_BOB motion with REST-POSE UVs: the painting's projection is taken from the
## floe's rest position (v_world before the bob), so the floe moves and its paint does not swim. v1's files are untouched.

const WATER_SHADER := """
shader_type spatial;
render_mode unshaded, cull_disabled, fog_disabled, specular_disabled;
// R-C9-159: the sea and the lagoon, MOVING, in the painting's own hand. The colour is the PAINTING's
// (projected through the fixed camera, as the ground's), so the painted water between the floes stays the
// painter's; over it, slow wash ripples drifting on the swell, a darker lead tone where the water is open,
// and FOAM RINGS that pulse round every floe's edge (the floes' distance field, water_sdf).
uniform sampler2D paint_tex : source_color, filter_linear_mipmap, repeat_disable;
uniform sampler2D noise_tex : filter_linear_mipmap, repeat_enable;
uniform sampler2D water_sdf : filter_linear, repeat_disable;     // R: metres to the nearest floe edge / 2
uniform vec4 sdf_rect = vec4(-70.0, -14.0, 96.0, 76.0);           // x0, z0, w, h (world xz)
uniform vec3 g_u_hat = vec3(0.681998, 0.0, -0.731354);
uniform vec3 g_v_hat = vec3(-0.731354, 0.0, -0.681998);
uniform vec3 g_frame = vec3(0.0, 0.0, 50.0);
uniform vec2 g_px_per = vec2(40.0, 30.0);
uniform vec2 g_size = vec2(2816.0, 3328.0);
uniform vec3 deep_col : source_color = vec3(0.13, 0.22, 0.31);
uniform vec3 crest_col : source_color = vec3(0.62, 0.72, 0.80);
uniform vec3 foam_col : source_color = vec3(0.92, 0.94, 0.96);
uniform float paint_mix = 0.75;
varying vec3 v_world;
vec2 guide_uv(vec3 p) {
	float u = dot(p, g_u_hat);
	float v = dot(p, g_v_hat);
	return vec2((u - g_frame.x) * g_frame.z, (g_frame.y - v) * g_px_per.x - p.y * g_px_per.y) / g_size;
}
void vertex() { v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz; }
void fragment() {
	vec2 xz = v_world.xz;
	vec2 guv = guide_uv(v_world);
	bool inside = guv.x > 0.0 && guv.y > 0.0 && guv.x < 1.0 && guv.y < 1.0;
	vec3 base = mix(deep_col, inside ? texture(paint_tex, guv).rgb : deep_col, paint_mix);
	// the swell: two drifting wash layers, quantised into a few soft bands (a brush, not a gradient)
	float n1 = texture(noise_tex, xz * 0.045 + vec2(TIME * 0.012, TIME * 0.007)).r;
	float n2 = texture(noise_tex, xz * 0.11 + vec2(-TIME * 0.02, TIME * 0.016)).r;
	float sw = n1 * 0.6 + n2 * 0.4;
	float band = smoothstep(0.58, 0.64, sw) - smoothstep(0.70, 0.76, sw);
	vec3 col = base * (0.88 + 0.22 * smoothstep(0.35, 0.75, sw));
	col = mix(col, crest_col, band * 0.35);
	// fine ripple strokes: thin crests travelling across the wind
	float r = texture(noise_tex, vec2(xz.x * 0.35 + TIME * 0.05, xz.y * 0.9 - TIME * 0.03)).r;
	col = mix(col, crest_col, smoothstep(0.80, 0.86, r) * 0.45);
	// foam rings round the floes, breathing with the swell
	vec2 su = (xz - sdf_rect.xy) / sdf_rect.zw;
	float d = texture(water_sdf, su).r * 2.0;
	float pulse = 0.18 + 0.08 * sin(TIME * 1.3 + n1 * 9.0);
	float fn = texture(noise_tex, xz * 0.9 + vec2(TIME * 0.04, -TIME * 0.03)).r;
	// a broken lace of foam hugging the floe edge, its width breathing with the swell
	float lace = (1.0 - smoothstep(pulse * 0.5, pulse, d)) * smoothstep(0.42, 0.62, fn + 0.25 * (1.0 - d / max(pulse, 1e-3)));
	float inb = step(0.0, su.x) * step(su.x, 1.0) * step(0.0, su.y) * step(su.y, 1.0);
	col = mix(col, foam_col, clamp(lace, 0.0, 1.0) * 0.85 * inb);
	ALBEDO = col;
	ROUGHNESS = 0.0;
}
"""


## R-C9-159's FLOE_BOB motion (barrow_v2_sw.gd:603-609), applied AFTER v_world (rest pose) in v1's PAINTED_SHADER, in world
## metres (the blob mesh is a scaled unit sphere), the floe's phase as a uniform
const FLOE_BOB_REST := """	v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	// BV2F-PT DEV-5: REST-POSE UVs -- the projection above is the floe at rest; the bob below moves only the geometry
	float ph = bob_phase * 6.2831;
	vec3 wd = vec3(0.03 * sin(TIME * 0.5 + ph), 0.035 * sin(TIME * 0.9 + ph) + 0.015 * sin(TIME * 2.1 + ph * 1.7), 0.03 * cos(TIME * 0.43 + ph));
	VERTEX += inverse(mat3(MODEL_MATRIX)) * wd;
"""


static func floe_shader_code() -> String:
	var code: String = PaintedWorld.PAINTED_SHADER
	assert(code.count("	v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;\n") == 1, "pt_water: v_world line not found once")
	assert(code.count("uniform float his_shadow_on = 1.0;\n") == 1, "pt_water: his_shadow_on uniform not found once")
	code = code.replace("uniform float his_shadow_on = 1.0;\n", "uniform float his_shadow_on = 1.0;\nuniform float bob_phase = 0.0;   // BV2F-PT DEV-5\n")
	return code.replace("	v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;\n", FLOE_BOB_REST)
