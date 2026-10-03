// Run C-9 Phase 2, lane DV (drax): barrow_v2 spawn VFX -- the crack-field REVEAL (p01 ground cracks, p05 ambush hold cracks).
// Godot 4 CanvasItem shader. TEXTURE = the painted crack field (<name>.png, straight alpha); reveal_map = <name>_reveal.png (L8).
// reveal_map.r = arrival / build_s (0..1; 1.0 = never shown). The runtime sets `progress` FROM AN ORACLE EVENT, never a free timer:
//   progress = clamp((t_now - t_event) / build_s, 0.0, 1.0)     (p05: t_event = EV_AMBUSH_HOLD_START, build_s = 4.0 exactly)
// and `fade` for the outro (1 -> 0). Python twin: tools/svfx_core.py reveal() (used by the preview).
shader_type canvas_item;
uniform sampler2D reveal_map : filter_linear;
uniform float progress = 0.0;
uniform float fade = 1.0;
uniform float soft = 0.015;        // a pixel fades in over 1.5 % of the build
uniform float glint = 0.6;         // the pale glint riding the crack front
uniform float glint_w = 0.06;
uniform vec3 glint_col = vec3(0.922, 0.965, 1.0);
void fragment() {
	vec4 c = texture(TEXTURE, UV);
	float r = texture(reveal_map, UV).r;
	float arr = r * 255.0 / 254.0;
	float on = clamp((progress - arr) / soft, 0.0, 1.0) * step(r, 254.5 / 255.0);
	float g = (1.0 - clamp((progress - arr) / glint_w, 0.0, 1.0)) * on * glint;
	COLOR = vec4(mix(c.rgb, glint_col, g), c.a * on * fade);
}
