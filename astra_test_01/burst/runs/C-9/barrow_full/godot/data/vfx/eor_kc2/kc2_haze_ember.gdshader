shader_type spatial;
// ============================================================================
// kc2_haze_ember.gdshader — C-9 R-C9-146 / EOR2 PORT 20 (drax, 2026-10-02). THE RED EYE OF RECKONING'S HAZE.
//
// Matt, verbatim: "Maybe the haze can be the part that changes to a reddish color for eye of reckoning. Maybe the
// red color can be due to particles/sparks or the cloud's transparent edges running intermittently red hot."
//
// The PORT 17 snow-powder haze (eor_kc2_fx.gd `_smoke`), drawn by THIS shader on `eortint=red` instead of its
// StandardMaterial -- same quad, same texture, same particle colours, same billboard, same soft-particle fade,
// same draw. One thing is added: the LOW-ALPHA RIM BAND of each puff (the texture's thin outer alpha) runs
// red-hot, on and off, per particle.
//
// ⚑ ONE DRAW, MIX AND ADD AT ONCE: blend_premul_alpha. The cloud is premultiplied (colour x alpha, exactly the mix
//   the StandardMaterial drew); the ember is ADDED on top without adding alpha, so it glows over the snow instead
//   of painting it. The core stays light: the ember mask is zero where the puff is dense.
// ⚑ IT CRAWLS, IT DOES NOT PULSE: each particle's on/off window is a phase of (its own seeded offset, its angle
//   around the cloud's centre, the clock), so a lit band travels around the disc and breaks up.
// ⚑ NO WALL CLOCK. `ember_clock` is the effect's own revolution clock (PORT 1), written per frame -- the source's
//   determinism law (FG-10) holds; INSTANCE_ID is the particle's slot, stable under the pinned seed.
// ============================================================================
render_mode unshaded, blend_premul_alpha, depth_draw_never, cull_back, shadows_disabled;

uniform sampler2D albedo_tex : source_color, filter_linear, repeat_disable;
uniform sampler2D depth_texture : hint_depth_texture, filter_nearest, repeat_disable;
uniform float fade = 1.0;                       // PORT 9's fade (the StandardMaterial's albedo alpha)
uniform float proximity_fade_distance = 0.8;    // PORT 18
uniform vec3 ember_mid : source_color = vec3(1.0, 0.42, 0.06);    // the source ramp's knee (PAL_MID)
uniform vec3 ember_tail : source_color = vec3(0.98, 0.07, 0.02);  // ...and its crawl (PAL_TAIL)
uniform float ember_gain = 0.9;
uniform float rim_lo = 0.04;                    // texture alpha where the rim band starts
uniform float rim_hi = 0.30;                    // ...and where the puff is dense enough to be "core"
uniform float duty = 0.30;                      // fraction of each cycle a particle's rim runs hot
uniform float rate = 0.5;                       // cycles per revolution
uniform float waves = 2.0;                      // lobes of the crawl around the disc
uniform float jitter = 0.35;                    // per-particle seeded phase spread
uniform float ember_clock = 0.0;                // revolutions (PORT 1 clock)
uniform vec3 ember_centre = vec3(0.0);          // the cloud's centre, world space

varying float v_on;
varying float v_heat;

float h1(float n) {
	return fract(sin(n * 12.9898 + 78.233) * 43758.5453);
}

void vertex() {
	// BILLBOARD_PARTICLES, as StandardMaterial3D generates it (the haze's billboard mode)
	mat4 mat_world = mat4(normalize(INV_VIEW_MATRIX[0]), normalize(INV_VIEW_MATRIX[1]), normalize(INV_VIEW_MATRIX[2]), MODEL_MATRIX[3]);
	mat_world = mat_world * mat4(vec4(cos(INSTANCE_CUSTOM.x), -sin(INSTANCE_CUSTOM.x), 0.0, 0.0), vec4(sin(INSTANCE_CUSTOM.x), cos(INSTANCE_CUSTOM.x), 0.0, 0.0), vec4(0.0, 0.0, 1.0, 0.0), vec4(0.0, 0.0, 0.0, 1.0));
	MODELVIEW_MATRIX = VIEW_MATRIX * mat_world;
	MODELVIEW_MATRIX = MODELVIEW_MATRIX * mat4(vec4(length(MODEL_MATRIX[0].xyz), 0.0, 0.0, 0.0), vec4(0.0, length(MODEL_MATRIX[1].xyz), 0.0, 0.0), vec4(0.0, 0.0, length(MODEL_MATRIX[2].xyz), 0.0), vec4(0.0, 0.0, 0.0, 1.0));
	MODELVIEW_NORMAL_MATRIX = mat3(MODELVIEW_MATRIX);
	// the crawl: seeded per particle, travelling around the disc on the effect's clock
	float id = float(INSTANCE_ID);
	vec3 d = MODEL_MATRIX[3].xyz - ember_centre;
	float ang = atan(d.x, d.z) / 6.28318530718;
	float x = fract(ember_clock * rate - ang * waves + jitter * h1(id));
	v_on = smoothstep(0.0, 0.08, x) * (1.0 - smoothstep(duty - 0.08, duty, x));
	v_heat = h1(id + 17.0);
}

void fragment() {
	vec4 tex = texture(albedo_tex, UV);
	float a = COLOR.a * tex.a * fade;
	// PORT 18 soft particles (the StandardMaterial's proximity fade, written out)
	float depth = textureLod(depth_texture, SCREEN_UV, 0.0).r;
#if CURRENT_RENDERER == RENDERER_COMPATIBILITY
	vec3 ndc = vec3(SCREEN_UV * 2.0 - 1.0, depth * 2.0 - 1.0);
#else
	vec3 ndc = vec3(SCREEN_UV * 2.0 - 1.0, depth);
#endif
	vec4 view = INV_PROJECTION_MATRIX * vec4(ndc, 1.0);
	view.xyz /= view.w;
	float prox = clamp(1.0 - smoothstep(view.z + proximity_fade_distance, view.z, VERTEX.z), 0.0, 1.0);
	a *= prox;
	// the rim: the puff's thin outer alpha, not its dense core
	float rim = smoothstep(rim_lo, rim_lo + 0.06, tex.a) * (1.0 - smoothstep(rim_hi - 0.12, rim_hi, tex.a));
	float glow = rim * v_on * fade * prox * smoothstep(0.0, 0.05, COLOR.a);
	vec3 hot = mix(ember_mid, ember_tail, v_heat);
	ALBEDO = COLOR.rgb * tex.rgb * a + hot * glow * ember_gain;   // premultiplied cloud + added ember
	ALPHA = a;
}
