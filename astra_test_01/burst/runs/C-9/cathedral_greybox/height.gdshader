shader_type spatial;
render_mode unshaded, cull_back, depth_draw_opaque, shadows_disabled, fog_disabled;
// Height -> two 8-bit channels.  ALBEDO written from a shader is treated as LINEAR and is
// sRGB-ENCODED on output, so a raw byte/255 does NOT survive the round trip (measured: the
// floor's 42 came back as 113). Emitting the sRGB-DECODED value makes the hardware encode
// restore the byte exactly. StandardMaterial3D.albedo_color is unaffected because Godot
// already decodes it, which is why the id pass round-tripped byte-exact and this did not.
uniform float h_min = -8.0;
uniform float h_max = 64.0;
vec3 s2l(vec3 c) {
	return mix(c / 12.92, pow((c + 0.055) / 1.055, vec3(2.4)), step(vec3(0.04045), c));
}
void fragment() {
	vec3 wp = (INV_VIEW_MATRIX * vec4(VERTEX, 1.0)).xyz;
	float t = clamp((wp.y - h_min) / (h_max - h_min), 0.0, 1.0);
	float v = t * 65535.0;
	float hi = floor(v / 256.0);
	float lo = floor(v - hi * 256.0);
	ALBEDO = s2l(vec3(hi / 255.0, lo / 255.0, 0.0));
}
