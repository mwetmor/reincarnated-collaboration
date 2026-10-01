extends Node3D
## C-9 -- MIX v3's IMPACT CRATER (Matt, 2026-09-30: "leave an impact crater with a smoldering center and have
## fault lines/cracks that actually truly change the painted 3D floor and alter it as a crater would with lines of
## fire across the cracks.. similar size to the smoldering flames now, but all of that detail in that radius, and
## maybe a random line or two extending beyond, mostly perceptible by the fact that it's burning"). drax.
##
## THE DENT IS REAL where there is snow: the snow field's own trail takes a round press with its berm (the same
## stamp a boot makes, SnowField._stamp), so the snow surface goes down and its rim stands up -- the field's
## mesh, its ink and its shading all see it. Over it lies the CRATER SKIN: a grid draped on the (dented)
## ground, one unshaded shader in the painting's own terms --
##   the bowl shaded by the sun across its walls, the wall turned from the sun in the painter's shadow colour;
##   the raised lip, lit on its sun side; charring that thins into soot outside the rim;
##   RADIAL FAULT LINES and a net of smaller cracks, drawn as ink lines, each with a LINE OF FIRE inside it
##   that cools at its own pace over 4-6 s; one or two runners out past the rim, seen mostly while they burn;
##   a SMOULDERING CENTRE glowing deep red, pulsing and cooling.
## The cooled crater stays: a pool of POOL skins, the oldest fading out when a fifth lands. Every skin is
## built and drawn once (invisibly) at load; an impact only rewrites its 17 x 17 heights (one small buffer).

const POOL := 4
const GRID := 16                     # cells per side
const FADE_S := 1.2                  # the oldest crater's fade when it is reused
const LIFT_M := 0.03                 # above the ground it is draped on

const SHADER := """
shader_type spatial;
render_mode unshaded, blend_mix, depth_draw_never, cull_disabled, shadows_disabled, fog_disabled, specular_disabled;
uniform sampler2D noise_tex : filter_linear_mipmap, repeat_enable;
uniform float crater_r = 1.1;          // the rim, m
uniform float out_r = 2.0;             // the skin's reach (the runners), m
uniform float age = 100.0;             // s since the impact
uniform float seed = 0.0;
uniform float fade = 1.0;              // the pool's eviction fade
uniform float warm = 0.0;
uniform float fx_time = 0.0;
uniform vec2 sun_xz = vec2(0.5, 0.5);  // toward the sun, on the ground (its length: how low it is)
uniform float sun_y = 0.7;
uniform vec3 ink : source_color = vec3(0.113, 0.082, 0.067);
uniform vec3 char_c : source_color = vec3(0.27, 0.22, 0.19);
uniform vec3 ash_c : source_color = vec3(0.52, 0.47, 0.43);
uniform vec3 shade_c : source_color = vec3(0.34, 0.37, 0.56);   // the painter's shadow colour (PaintStack)
uniform vec3 f_red : source_color = vec3(0.55, 0.05, 0.03);
uniform vec3 f_org : source_color = vec3(1.0, 0.42, 0.07);
uniform vec3 f_yel : source_color = vec3(1.0, 0.82, 0.38);
varying vec3 v_p;
void vertex() { v_p = VERTEX; }
float h1(float x) { return fract(sin(x * 127.1 + seed * 311.7) * 43758.5453); }
// one crack: how far p is from a wobbling radial line at angle a0, in metres
float radial(vec2 p, float r, float a0, float wob) {
	float n = texture(noise_tex, vec2(r * 0.9 + a0 * 3.1, seed * 1.7 + a0)).r - 0.5;
	float a = a0 + n * wob / max(r, 0.15);
	vec2 d = vec2(cos(a), sin(a));
	return abs(p.x * d.y - p.y * d.x) + (dot(p, d) < 0.0 ? 10.0 : 0.0);
}
vec3 fire(float k) {
	vec3 c = mix(f_red, f_org, smoothstep(0.35, 0.7, k));
	return mix(c, f_yel, smoothstep(0.82, 1.0, k));
}
void fragment() {
	if (warm > 0.5) { discard; }
	vec2 p = v_p.xz;
	float r = length(p);
	float R = crater_r;
	float n1 = texture(noise_tex, p * 0.31 + vec2(seed * 0.37, 0.13)).r;
	float n2 = texture(noise_tex, p * 1.37 + vec2(0.71, seed * 0.53)).r;
	float rw = r / R + (n1 - 0.5) * 0.22;                     // the rim, torn
	float px = max(fwidth(r), 1e-4);
	// --- THE BOWL AND THE LIP: a normal from the shape, lit by the sun ---------------------------------
	vec2 dir = p / max(r, 1e-3);
	float slope = 0.0;                                          // dh/dr
	if (rw < 1.0) { slope = 1.1 * rw; }                         // the wall rising toward the rim
	else if (rw < 1.35) { slope = -1.6 * (rw - 1.0) / 0.35 + 0.5 * (1.0 - (rw - 1.0) / 0.35); }   // over the lip
	vec3 nrm = normalize(vec3(-dir.x * slope, 1.0, -dir.y * slope));
	vec3 sun = normalize(vec3(sun_xz.x, sun_y, sun_xz.y));
	float lit = dot(nrm, sun) - sun.y;                          // against flat ground
	vec3 col = char_c;
	float a = 0.0;
	float inside = 1.0 - smoothstep(0.97, 1.0 + px / R, rw);
	float lip = smoothstep(0.92, 1.02, rw) * (1.0 - smoothstep(1.15, 1.42, rw));
	// the soot thrown past the rim, in two flat washes with torn edges (the painting's way, not an airbrush)
	float sr = rw + (n2 - 0.5) * 0.35;
	float soot = 0.55 * (1.0 - smoothstep(1.30 - px, 1.30 + px, sr)) + 0.25 * (1.0 - smoothstep(1.62 - px, 1.62 + px, sr));
	// the floor of the bowl: charred, ash-flecked
	col = mix(char_c, ash_c, smoothstep(0.55, 0.85, n2) * 0.45 * inside);
	a = max(inside * 0.9, soot);
	// the lip: ashen scorched earth thrown up, its sun side lit
	col = mix(col, mix(ash_c * 0.8, ash_c * 1.25, smoothstep(-0.1, 0.25, lit)), lip * 0.8);
	a = max(a, lip * 0.85);
	// the wall turned from the sun: the painter's shadow colour, flat and hard-edged, as the painting does it
	float shade = smoothstep(0.18 - 0.02, 0.18 + 0.02, -lit) * (inside + lip * 0.6);
	col = mix(col, shade_c * 0.55, shade * 0.45);
	// the wall turned to the sun: warm ash, lit
	col = mix(col, ash_c * 1.1, smoothstep(0.08, 0.3, lit) * inside * 0.55);
	// the rim's own pen line on its shadowed side
	float rim_line = (1.0 - smoothstep(0.0, 0.035 + px, abs(rw - 1.0) * R)) * (0.4 + 0.6 * shade);
	col = mix(col, ink, rim_line * 0.85);
	a = max(a, rim_line * 0.9);
	// --- THE FAULT LINES ---------------------------------------------------------------------------------
	float heat0 = clamp(1.0 - age / 5.2, 0.0, 1.0);             // the fire's whole cooling, 0 by about 5 s
	float crack_ink = 0.0;
	float crack_fire = 0.0;
	for (int k = 0; k < 7; k++) {
		float fk = float(k);
		float a0 = 6.2831853 * (fk + 0.35 * h1(fk)) / 7.0;
		float d = radial(p, r, a0, 0.22);
		float reach = R * (0.85 + 0.3 * h1(fk + 9.0));
		float on = (1.0 - smoothstep(reach * 0.9, reach, r)) * smoothstep(0.08 * R, 0.2 * R, r);
		float w = (0.022 + 0.03 * (1.0 - r / R)) * on;
		float line = (1.0 - smoothstep(w, w + px, d)) * step(0.001, on);
		crack_ink = max(crack_ink, line);
		float hk = clamp(heat0 * (1.0 + 0.6 * h1(fk + 3.0)) - 0.25 * h1(fk + 5.0), 0.0, 1.0);
		crack_fire = max(crack_fire, (1.0 - smoothstep(w * 0.5, w * 0.5 + px, d)) * hk * on);
	}
	// the net of smaller cracks between them: cell edges, inside the bowl
	vec2 q = p * 2.4 / R + seed * 7.0;
	vec2 iq = floor(q);
	float f1 = 9.0; float f2 = 9.0;
	for (int j = -1; j <= 1; j++) { for (int i = -1; i <= 1; i++) {
		vec2 c = iq + vec2(float(i), float(j));
		vec2 o = vec2(fract(sin(dot(c, vec2(12.9898, 78.233))) * 43758.5453), fract(sin(dot(c, vec2(39.3468, 11.135))) * 24634.6345));
		float dd = length(q - c - o);
		if (dd < f1) { f2 = f1; f1 = dd; } else if (dd < f2) { f2 = dd; }
	} }
	float edge = (f2 - f1) * R / 2.4;                            // metres from a cell edge
	float net_on = (1.0 - smoothstep(0.7, 0.95, rw)) * smoothstep(0.12, 0.3, rw);
	float net = (1.0 - smoothstep(0.012, 0.012 + px, edge)) * net_on;
	crack_ink = max(crack_ink, net * 0.8);
	crack_fire = max(crack_fire, (1.0 - smoothstep(0.006, 0.006 + px, edge)) * net_on * clamp(heat0 * 1.3 - 0.3, 0.0, 1.0));
	// the runners: one or two cracks past the rim, thin, seen mostly while they burn
	float runners = 1.0 + step(0.45, h1(41.0));
	for (int k = 0; k < 2; k++) {
		if (float(k) >= runners) { break; }
		float a0 = 6.2831853 * h1(float(k) * 17.0 + 23.0);
		float d = radial(p, r, a0, 0.35);
		float len = R + (out_r - R) * (0.55 + 0.45 * h1(float(k) + 31.0));
		float on = smoothstep(0.75 * R, 0.95 * R, r) * (1.0 - smoothstep(len * 0.8, len, r));
		float w = 0.016 * (1.0 - smoothstep(R, len, r) * 0.6) * on;
		float line = (1.0 - smoothstep(w, w + px, d)) * step(0.001, on);
		float hk = clamp(heat0 * 1.15, 0.0, 1.0);
		crack_ink = max(crack_ink, line * (0.35 + 0.65 * smoothstep(1.4, 1.0, r / R)));
		crack_fire = max(crack_fire, line * hk);
	}
	col = mix(col, ink, crack_ink * 0.92);
	a = max(a, crack_ink * 0.9);
	// --- THE SMOULDERING CENTRE --------------------------------------------------------------------------
	float pulse = 0.82 + 0.18 * sin(fx_time * 5.3 + n2 * 9.0) * sin(fx_time * 3.1 + n1 * 6.0);
	float core_heat = clamp(1.0 - age / 6.5, 0.0, 1.0);
	float centre = (1.0 - smoothstep(0.12, 0.42, rw + (n2 - 0.5) * 0.25)) * core_heat;
	vec3 glow = fire(clamp(centre * 0.85 * pulse, 0.0, 1.0));
	col = mix(col, mix(char_c, glow, smoothstep(0.05, 0.4, centre)), smoothstep(0.02, 0.3, centre));
	// the fire in the cracks, over everything (its own value: yellow-white where hottest, red as it cools)
	float fk = crack_fire * (0.75 + 0.25 * pulse);
	col = mix(col, fire(fk), smoothstep(0.02, 0.12, crack_fire));
	a = max(a, smoothstep(0.02, 0.12, crack_fire));
	a *= fade;
	if (a < 0.01) { discard; }
	ALBEDO = col;
	ALPHA = clamp(a, 0.0, 1.0);
}
"""

var scene
var cam: Camera3D
var slots: Array = []                # {mi, mat, mesh, age, live, fade_from}
var warmed := false
var _warm := 0
var _shader: Shader
var _clock := 0.0
var last_us := 0
var report := {}
var crater_r := 1.1
var out_r := 2.0
var dent := true


func setup(p_scene, p_cam: Camera3D, noise: Texture2D, to_sun: Vector3, p_crater_r: float) -> void:
	scene = p_scene
	cam = p_cam
	crater_r = p_crater_r
	out_r = p_crater_r * 1.85
	_shader = Shader.new()
	_shader.code = SHADER
	var sxz := Vector2(to_sun.x, to_sun.z)
	for i in POOL:
		var mat := ShaderMaterial.new()
		mat.shader = _shader
		# after the post pass, as the cinders and the particles are: the pass composites its own screen copy
		# over the frame and would paint out anything transparent drawn before it
		mat.render_priority = PaintStack.AFTER_POST_PRIORITY
		mat.set_shader_parameter("noise_tex", noise)
		mat.set_shader_parameter("crater_r", crater_r)
		mat.set_shader_parameter("out_r", out_r)
		mat.set_shader_parameter("sun_xz", sxz)
		mat.set_shader_parameter("sun_y", to_sun.y)
		var mesh := _grid_mesh()
		mesh.surface_set_material(0, mat)
		var mi := MeshInstance3D.new()
		mi.name = "Crater%d" % i
		mi.mesh = mesh
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		mi.visible = false
		add_child(mi)
		slots.append({"mi": mi, "mat": mat, "mesh": mesh, "age": 1e9, "live": false, "fade_from": -1.0, "seed": 0.0})
	_warm = 4
	dent = not OS.get_cmdline_user_args().has("--no-dent")      # the A/B for the dent's cost
	report = {"pool": POOL, "grid": GRID, "crater_r": crater_r, "out_r": out_r}


func _grid_mesh() -> ArrayMesh:
	var n := GRID + 1
	var v := PackedVector3Array()
	var idx := PackedInt32Array()
	for j in n:
		for i in n:
			v.append(Vector3(lerpf(-out_r, out_r, float(i) / GRID), 0.0, lerpf(-out_r, out_r, float(j) / GRID)))
	for j in GRID:
		for i in GRID:
			var a := j * n + i
			idx.append_array(PackedInt32Array([a, a + 1, a + n, a + 1, a + n + 1, a + n]))
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = v
	arr[Mesh.ARRAY_INDEX] = idx
	var m := ArrayMesh.new()
	m.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr, [], {}, Mesh.ARRAY_FLAG_USE_DYNAMIC_UPDATE)
	m.custom_aabb = AABB(Vector3(-out_r, -2.0, -out_r), Vector3(out_r * 2.0, 4.0, out_r * 2.0))
	return m


func start(target: Vector3, ground_y: Callable) -> Dictionary:
	"""A crater at target: the snow pressed (if there is snow), the oldest skin taken (fading), draped on the
	dented ground. Returns the timings."""
	var t0 := Time.get_ticks_usec()
	var snow = scene.snow if scene != null else null
	var t_dent := 0
	if dent and snow != null and snow.has_method("_stamp"):
		# the same stamp a boot makes: a round press, its berm standing up as the crater's rim
		snow._stamp(Vector2(target.x, target.z), Vector2(0, 1), crater_r * 0.92, crater_r * 0.92, crater_r * 0.3, 1.6)
		t_dent = Time.get_ticks_usec() - t0
	# the slot: a free one, else the oldest (it fades out while the new one comes in elsewhere -- the
	# oldest is taken only once all POOL are live, and its fade is the new crater's arrival)
	var pick := -1
	var oldest := -1.0
	for i in slots.size():
		if not bool(slots[i]["live"]):
			pick = i
			break
		if float(slots[i]["age"]) > oldest:
			oldest = float(slots[i]["age"])
			pick = i
	var sl: Dictionary = slots[pick]
	var n := GRID + 1
	var v := PackedVector3Array()
	v.resize(n * n)
	for j in n:
		for i in n:
			var lx := lerpf(-out_r, out_r, float(i) / GRID)
			var lz := lerpf(-out_r, out_r, float(j) / GRID)
			var w := target + Vector3(lx, 0.0, lz)
			v[j * n + i] = Vector3(lx, float(ground_y.call(w)) - target.y + LIFT_M, lz)
	# the heights written into the skin's own vertex buffer (a dynamic surface: no new mesh, no new pipeline)
	RenderingServer.mesh_surface_update_vertex_region((sl["mesh"] as ArrayMesh).get_rid(), 0, 0, v.to_byte_array())
	var mi: MeshInstance3D = sl["mi"]
	mi.global_position = target
	mi.visible = true
	sl["live"] = true
	sl["age"] = 0.0
	sl["fade_from"] = -1.0
	sl["seed"] = randf() * 10.0
	(sl["mat"] as ShaderMaterial).set_shader_parameter("seed", sl["seed"])
	(sl["mat"] as ShaderMaterial).set_shader_parameter("fade", 1.0)
	(sl["mat"] as ShaderMaterial).set_shader_parameter("age", 0.0)
	# when the pool is full, the next oldest begins its fade now, so a fifth crater never pops one away
	var live := 0
	var old_i := -1
	var old_a := -1.0
	for i in slots.size():
		if bool(slots[i]["live"]):
			live += 1
			if i != pick and float(slots[i]["age"]) > old_a:
				old_a = float(slots[i]["age"])
				old_i = i
	if live == POOL and old_i >= 0 and float(slots[old_i]["fade_from"]) < 0.0:
		slots[old_i]["fade_from"] = float(slots[old_i]["age"])
	var rec := {"slot": pick, "dent_us": t_dent, "total_us": Time.get_ticks_usec() - t0}
	report["last_start"] = rec
	return rec


func _process(dt: float) -> void:
	var t0 := Time.get_ticks_usec()
	_clock += dt
	if _warm > 0:
		_warm -= 1
		var sl: Dictionary = slots[0]
		var mi: MeshInstance3D = sl["mi"]
		(sl["mat"] as ShaderMaterial).set_shader_parameter("warm", 1.0 if _warm > 0 else 0.0)
		if _warm > 0:
			mi.global_position = cam.global_position + (-cam.global_transform.basis.z) * 5.0
			mi.visible = true
		else:
			mi.visible = false
			warmed = true
		return
	for sl in slots:
		if not bool(sl["live"]):
			continue
		sl["age"] = float(sl["age"]) + dt
		var m: ShaderMaterial = sl["mat"]
		m.set_shader_parameter("age", sl["age"])
		m.set_shader_parameter("fx_time", _clock)
		if float(sl["fade_from"]) >= 0.0:
			var f := 1.0 - (float(sl["age"]) - float(sl["fade_from"])) / FADE_S
			m.set_shader_parameter("fade", clampf(f, 0.0, 1.0))
			if f <= 0.0:
				sl["live"] = false
				sl["fade_from"] = -1.0
				(sl["mi"] as MeshInstance3D).visible = false
	last_us = Time.get_ticks_usec() - t0


func live_count() -> int:
	var n := 0
	for sl in slots:
		if bool(sl["live"]):
			n += 1
	return n
