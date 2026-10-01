extends Node3D
## C-9 -- MIX v2's SMOULDERING CINDERS, above the scorch (Matt, 2026-09-30: "the flames left on the ground
## afterwards to be more like real smoldering cinders with a bit of small realistic burning areas"). drax.
##
## The scorch and its ember cracks are the ground term (PaintedWorld.FX_GROUND_CINDERS). Here: a FEW SMALL
## FLAMES flickering low at scattered points of the patch, and two faint SMOKE WISPS -- one MultiMesh, one
## unshaded shader in continuous colour (a real flame's yellow-white root, orange body, red tips; a soft
## edge), one draw. Each flame dies at its own time over the burn; the wisps rise and thin. Built and
## drawn once, invisibly, at load (warm_up). Nothing is created at cast time.

const FLAMES := 9
const WISPS := 2
const SHADER := """
shader_type spatial;
render_mode unshaded, blend_mix, depth_draw_never, cull_disabled, shadows_disabled, fog_disabled;
uniform sampler2D noise_tex : filter_linear_mipmap, repeat_enable;
uniform float fx_time = 0.0;
varying vec4 v_c;
void vertex() { v_c = INSTANCE_CUSTOM; }    // x kind (0 flame, 1 smoke), y life 0..1 (1 = gone), z seed, w alpha
float lin(float c) { return c <= 0.04045 ? c / 12.92 : pow((c + 0.055) / 1.055, 2.4); }
void fragment() {
	vec2 uv = vec2(UV.x, 1.0 - UV.y);   // x across 0..1, y UP 0..1 (a QuadMesh's UV.y runs down; the quad stands on its base)
	float seed = v_c.z;
	vec3 col;
	float a;
	if (v_c.x < 0.5) {
		// THE FLAME: a teardrop, its sides torn by noise rising through it, narrowing to a flickering tip
		float n = texture(noise_tex, vec2(uv.x * 1.3 + seed * 7.1, uv.y * 1.6 - fx_time * 2.4 + seed * 3.7)).r;
		float n2 = texture(noise_tex, vec2(uv.x * 2.9 + seed * 3.3, uv.y * 3.1 - fx_time * 3.9)).r;
		float y = uv.y;
		float half_w = 0.42 * pow(max(1.0 - y, 0.0), 0.75) * smoothstep(0.0, 0.12, y + 0.02);
		float x = abs(uv.x - 0.5 + (n - 0.5) * 0.35 * y);
		float body = 1.0 - smoothstep(half_w * 0.75, half_w, x);
		body *= 1.0 - smoothstep(0.55 + 0.35 * n2, 0.95, y);
		float core = (1.0 - smoothstep(half_w * 0.25, half_w * 0.55, x)) * (1.0 - smoothstep(0.1, 0.45, y));
		float t = clamp(core + (1.0 - y) * 0.45 * body, 0.0, 1.0);
		col = mix(vec3(0.75, 0.12, 0.03), vec3(1.0, 0.45, 0.06), smoothstep(0.0, 0.45, t));
		col = mix(col, vec3(1.0, 0.86, 0.55), smoothstep(0.55, 1.0, t));
		a = body * (0.7 + 0.3 * t);
	} else {
		// THE WISP: a thin grey column, curling with the noise, thinning as it rises
		float n = texture(noise_tex, vec2(uv.x * 1.1 + seed * 5.0, uv.y * 0.9 - fx_time * 0.35)).r;
		float x = abs(uv.x - 0.5 + (n - 0.5) * 0.6 * uv.y);
		float w = 0.12 + 0.18 * uv.y;
		a = (1.0 - smoothstep(w * 0.4, w, x)) * smoothstep(0.0, 0.2, uv.y) * (1.0 - smoothstep(0.6, 1.0, uv.y));
		a *= 0.55 + 0.45 * n;
		col = vec3(0.42, 0.40, 0.39);
	}
	a *= v_c.w;
	if (a < 0.01) { discard; }
	ALBEDO = vec3(lin(col.r), lin(col.g), lin(col.b));
	ALPHA = clamp(a, 0.0, 1.0);
}
"""

var cam: Camera3D
var mm: MultiMesh
var mat: ShaderMaterial
var spots: Array = []
var warmed := false
var _warm := 0
var _collapsed := Transform3D(Basis(Vector3.ZERO, Vector3.ZERO, Vector3.ZERO), Vector3.ZERO)
var last_us := 0


func setup(p_cam: Camera3D, noise: Texture2D) -> void:
	cam = p_cam
	var sh := Shader.new()
	sh.code = SHADER
	mat = ShaderMaterial.new()
	mat.shader = sh
	mat.render_priority = PaintStack.AFTER_POST_PRIORITY
	mat.set_shader_parameter("noise_tex", noise)
	var quad := QuadMesh.new()
	quad.size = Vector2(1, 1)
	quad.center_offset = Vector3(0, 0.5, 0)      # stands on its base
	quad.material = mat
	mm = MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.use_custom_data = true
	mm.mesh = quad
	mm.instance_count = FLAMES + WISPS
	for i in mm.instance_count:
		mm.set_instance_transform(i, _collapsed)
		mm.set_instance_custom_data(i, Color(0, 1, 0, 0))
	var mi := MultiMeshInstance3D.new()
	mi.name = "Cinders"
	mi.multimesh = mm
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mi.custom_aabb = AABB(Vector3(-500, -100, -500), Vector3(1000, 200, 1000))
	add_child(mi)
	_warm = 4


func start(target: Vector3, radius: float, ground_y: Callable) -> void:
	"""The cinders for one burn at target: FLAMES small flames at scattered points inside 0.7 x radius,
	each with its own size, flicker and the moment it dies; WISPS faint smoke columns."""
	spots.clear()
	var rng := RandomNumberGenerator.new()
	rng.seed = int(Time.get_ticks_usec())
	for i in FLAMES + WISPS:
		var a := rng.randf() * TAU
		var r := radius * sqrt(rng.randf()) * (0.7 if i < FLAMES else 0.35)
		var p := target + Vector3(cos(a) * r, 0.0, sin(a) * r)
		p.y = float(ground_y.call(p)) + 0.01
		spots.append({"pos": p, "smoke": i >= FLAMES, "seed": rng.randf(),
			"h": rng.randf_range(0.32, 0.62) if i < FLAMES else rng.randf_range(1.0, 1.5),
			"born": rng.randf_range(0.35, 0.8), "dies": rng.randf_range(1.6, 2.9)})


func step(ti: float, burn_s: float) -> void:
	"""ti: seconds since the impact (negative: nothing). Each flame flickers in its window; the wisps rise late."""
	var t0 := Time.get_ticks_usec()
	mat.set_shader_parameter("fx_time", float(Time.get_ticks_msec()) / 1000.0)
	if _warm > 0:
		_warm -= 1
		var at := cam.global_position + (-cam.global_transform.basis.z) * 5.0
		mm.set_instance_transform(0, Transform3D(Basis.IDENTITY.scaled(Vector3(0.01, 0.01, 0.01)), at))
		mm.set_instance_custom_data(0, Color(0, 0, 0.5, 0.0))
		if _warm == 0:
			mm.set_instance_transform(0, _collapsed)
			warmed = true
		return
	if spots.is_empty():
		return
	var b := cam.global_transform.basis
	var right := b.x.normalized()
	for i in spots.size():
		var sp: Dictionary = spots[i]
		var smoke: bool = sp["smoke"]
		var born: float = float(sp["born"]) + (0.4 if smoke else 0.0)
		var dies: float = minf(float(sp["dies"]) + (0.3 if smoke else 0.0), burn_s)
		if ti < born or ti > dies:
			mm.set_instance_transform(i, _collapsed)
			continue
		var life := (ti - born) / maxf(dies - born, 1e-3)
		var fade := smoothstep(0.0, 0.15, life) * (1.0 - smoothstep(0.6, 1.0, life))
		var h: float = float(sp["h"]) * (0.85 + 0.15 * sin(ti * 11.0 + float(sp["seed"]) * 30.0)) * (1.0 - 0.45 * life if not smoke else 1.0)
		var w := h * (0.55 if not smoke else 0.45)
		# billboarded round the vertical: it stands up, turned to the camera
		var fwd := Vector3(b.z.x, 0.0, b.z.z).normalized()
		var basis := Basis(right * w, Vector3.UP * h, fwd * 0.01)
		mm.set_instance_transform(i, Transform3D(basis, sp["pos"]))
		mm.set_instance_custom_data(i, Color(1.0 if smoke else 0.0, life, float(sp["seed"]), fade * (0.22 if smoke else 1.0)))
	last_us = Time.get_ticks_usec() - t0


func clear() -> void:
	for i in mm.instance_count:
		mm.set_instance_transform(i, _collapsed)
	spots.clear()
