shader_type canvas_item;
render_mode blend_mix, unshaded;

// Source RGB carries an index, not brightness/coverage. No screen/depth buffers,
// derivatives, compute, light accumulation buffers or Forward+ dependencies.
uniform vec4 palette_0 : source_color = vec4(0.05, 0.1, 0.2, 1.0);
uniform vec4 palette_1 : source_color = vec4(0.15, 0.3, 0.6, 1.0);
uniform vec4 palette_2 : source_color = vec4(0.3, 0.7, 0.9, 1.0);
uniform vec4 palette_3 : source_color = vec4(0.85, 0.95, 1.0, 1.0);
uniform sampler2D distance_texture : filter_linear, repeat_disable;
uniform float erode : hint_range(0.0, 1.0) = 0.0;
uniform float dissolve : hint_range(0.0, 1.0) = 0.0;
uniform bool erode_outside_in = false;
uniform float erode_noise : hint_range(0.0, 1.0) = 0.0;
uniform sampler2D erosion_noise_texture : filter_linear, repeat_enable;
uniform bool dark_duplicate = false;
const bool PREMULTIPLIED = false;
varying float coverage_modulate;

void vertex() {
    // RGB modulation is intentionally ignored: treatment colours are explicit.
    coverage_modulate = COLOR.a;
}

void fragment() {
    vec4 index_sample = texture(TEXTURE, UV);
    float band = floor(clamp(index_sample.r, 0.0, 1.0) * 3.0 + 0.5);
    vec4 paint = palette_0;
    if (band > 0.5) { paint = palette_1; }
    if (band > 1.5) { paint = palette_2; }
    if (band > 2.5) { paint = palette_3; }
    float coverage = index_sample.a * paint.a * coverage_modulate;
    float distance_value = texture(distance_texture, UV).r;
    if (erode_outside_in) {
        vec2 resistance = texture(erosion_noise_texture, UV).rg;
        distance_value -= erode_noise * (0.5 * (2.0 * resistance.r - 1.0) + 0.5 * resistance.g);
        if (erode > 0.0 && (erode >= 1.0 || distance_value > 1.0 - erode)) { coverage = 0.0; }
    } else {
        if (erode > 0.0 && (erode >= 1.0 || distance_value < erode)) { coverage = 0.0; }
    }
    // Hold until 0.5, then remove band 3, 2, 1, 0 at 0.5, 2/3, 5/6, 1.
    if (dissolve >= (1.0 - band / 6.0)) { coverage = 0.0; }
    vec3 rgb = paint.rgb;
    if (dark_duplicate) { rgb = vec3(0.0); }
    if (PREMULTIPLIED) { rgb *= coverage; }
    COLOR = vec4(rgb, coverage);
}
