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
// ⚑ ONE DRAW, one MIX: the cloud is the StandardMaterial's mix; the ember, inside its rim mask only, is emissive red
//   that covers what is under it (see fragment). The core stays light: the ember mask is zero where the puff is dense.
// ⚑ IT CRAWLS, IT DOES NOT PULSE: each particle's on/off window is a phase of (its own seeded offset, its angle
//   around the cloud's centre, the clock), so a lit band travels around the disc and breaks up.
// ⚑ NO WALL CLOCK. `ember_clock` is the effect's own revolution clock (PORT 1), written per frame -- the source's
//   determinism law (FG-10) holds; INSTANCE_ID is the particle's slot, stable under the pinned seed.
// ============================================================================
render_mode unshaded, blend_mix, depth_draw_never, cull_back, shadows_disabled;

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
// the rim of the PUFF, not its wisps: the outer band of each quad (radius from its centre, 0 = centre, 1 = edge)
uniform float rim_r_in = 0.48;
uniform float rim_r_out = 0.92;
// 1 = soft-fade against a flat ground at ground_y (world metres) instead of the depth buffer: the 2D arena overlay
// atlas renders the haze with no floor (eor_kc2_fx.gd bind_synthetic)
uniform float ground_mode = 0.0;
uniform float ground_y = 0.0;

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
	if (ground_mode > 0.5) {
		float wy = (INV_VIEW_MATRIX * vec4(VERTEX, 1.0)).y;
		prox = smoothstep(ground_y, ground_y + proximity_fade_distance, wy);
	}
	a *= prox;
	// the rim: the puff's thin outer alpha, not its dense core
	// the puff's EDGE: its outer radial band, where its alpha is thin (tuned 2026-10-02: the texture's alpha band
	// alone traced the smoke's internal wisps and read as pink veins)
	float rr = length(UV - vec2(0.5)) * 2.0;
	float rim = smoothstep(rim_r_in, rim_r_in + 0.18, rr) * (1.0 - smoothstep(rim_r_out - 0.12, rim_r_out, rr))
		* smoothstep(rim_lo, rim_lo + 0.06, tex.a) * (1.0 - smoothstep(rim_hi - 0.12, rim_hi, tex.a));
	float glow = rim * v_on * fade * prox * smoothstep(0.0, 0.05, COLOR.a);
	vec3 hot = mix(ember_mid, ember_tail, v_heat);
	// ⚑ ON SNOW THE EMBER MUST COVER, NOT ADD. Red ADDED over 0.96 snow clips to pale yellow-white (first render,
	//   2026-10-02): it read as lightning, not heat. So inside its own rim mask the ember is emissive red that
	//   REPLACES what is under it by `ge` -- premultiplied: colour (1 - ge) of the cloud plus ge of hot red, alpha
	//   a + ge(1 - a). Outside the mask (ge = 0) this is exactly the cloud.
	float ge = clamp(glow * ember_gain, 0.0, 1.0);
	// The pixel wanted is, premultiplied, cloud x a x (1 - ge) + hot x ge over alpha A = a + ge(1 - a). It is written
	// as an ordinary MIX (colour = that / A): blend_premul_alpha measured darkening the cloud on Compatibility, and
	// PREMUL_ALPHA_FACTOR does not exist there (fragment compile failure). With ge = 0 this is exactly the
	// StandardMaterial's mix: colour = cloud, alpha = a.
	float A = a + ge * (1.0 - a);
	ALBEDO = (COLOR.rgb * tex.rgb * a * (1.0 - ge) + hot * ge) / max(A, 1e-4);
	ALPHA = A;
}
