extends Node3D
## C-9 CRATER v4 (R-C9-109, Matt 2026-10-01: "painted + real 3d + particle VFX ... the natural extension from our
## scene and character pipeline but for VFX"). drax. Behind ?meteor=mix4.
##
## THREE LAYERS, the Barrow's method:
##   1 REAL 3D -- a crater mesh built in Blender (tools/crater_mesh.py): a shallow bowl, a raised broken rim, the
##     fault lines cut as V-grooves, one or two runners, a feathered skirt. Three variants. It sits into the
##     snow: the snow is pressed under it (SnowField._stamp, as MIX v3) and the bowl's depth is scaled to the
##     snow it sits in, so it never sinks through the ground.
##   2 PAINTED -- the mesh rendered on the Barrow at the game camera (godot/tools/crater_guide.gd), painted over
##     by one guided Astra EDIT in the Barrow's style, projected back into its UVs (tools/crater_project.py).
##     Unlit (static after impact: the painted-light ruling). A separately painted EMISSION MASK (the cracks and
##     the smouldering centre) driven here: hot orange -> dull red -> dark over the fire field's life
##     (FIRE_LIFE_S, the D2 packet: 30 + 15 (level - 1) ticks at 25/s, 12.6 s at level 20), with a slow,
##     uneven pulse along the cracks. Never rotated (that would turn the painted light).
##   3 PARTICLES -- painted sprites: EMBERS (the kit's ember_1) rising off the cracks, thin SMOKE WISPS (one new
##     painted sheet) from the cracks, and a small burst of DEBRIS at the impact that lands and stays.
## PERFORMANCE (the Fire Ball lesson): one shader per layer; the skins a pool of 4 (four materials of ONE shader,
## their heights never rebuilt -- the meshes are built once); embers one GPUParticles3D, smoke one, debris one
## MultiMesh; all built at load and drawn once under the veil (warm); nothing is created at cast time.

const POOL := 4
const DATA := "res://data/vfx/crater_v4/"
const SEEDS := [11, 23, 37]
const SEEDS_ICE := [101, 102]         # R-C9-118 (b): the ice craters
const SEEDS_EARTH := [201, 202]       # R-C9-118 (b): scorched earth and broken stone
const FADE_S := 1.5
const DEBRIS := 28

## the fire field's life, s (the D2 packet: (30 + 15 * (level - 1)) / 25; 12.6 s at level 20)
static func fire_life_s(level: int) -> float:
	return (30.0 + 15.0 * float(level - 1)) / 25.0

const SKIN := """
shader_type spatial;
render_mode unshaded, blend_mix, depth_draw_never, cull_back, shadows_disabled, fog_disabled, specular_disabled;
uniform sampler2D albedo_tex : source_color, filter_linear_mipmap, repeat_disable;
uniform sampler2D emit_tex : filter_linear_mipmap, repeat_disable;
uniform sampler2D noise_tex : filter_linear_mipmap, repeat_enable;
uniform float age = 100.0;
uniform float life = 12.6;
uniform float fade = 1.0;
uniform float warm = 0.0;
uniform float fx_time = 0.0;
uniform vec3 hot : source_color = vec3(1.0, 0.62, 0.18);
uniform vec3 mid : source_color = vec3(0.92, 0.26, 0.05);
uniform vec3 dull : source_color = vec3(0.42, 0.05, 0.03);
uniform float depth_bias = 0.4;
uniform float emit_gain = 1.0;      // R-C9-118 (b): ice glows faintly in its cracks (steam, not fire)
void vertex() {
	// THE BOWL SITS INTO THE SNOW: drawn this far toward the camera in depth only (the camera is orthographic,
	// so nothing moves on screen), it wins against the snow round and under it, while anyone standing in it,
	// taller than the bias, still hides it
	vec4 vp = MODELVIEW_MATRIX * vec4(VERTEX, 1.0);
	vp.z += depth_bias;
	POSITION = PROJECTION_MATRIX * vp;
}
void fragment() {
	if (warm > 0.5) { discard; }
	vec4 a = texture(albedo_tex, UV);
	float e = texture(emit_tex, UV).r;
	// the field cools over its life: hot orange, then dull red, then dark (the painted cracks show through)
	float k = clamp(age / life, 0.0, 1.0);
	float heat = 1.0 - smoothstep(0.0, 1.0, k);
	heat *= smoothstep(0.0, 0.08, age);                         // it lights in the first frames after the strike
	// a slow, uneven pulse that travels along the cracks
	float n = texture(noise_tex, UV * 3.0 + vec2(fx_time * 0.05, -fx_time * 0.03)).r;
	float n2 = texture(noise_tex, UV * 7.0 - vec2(fx_time * 0.11, fx_time * 0.07)).r;
	float pulse = 0.72 + 0.28 * sin(fx_time * 2.1 + n * 9.0) * (0.6 + 0.4 * n2);
	float g = e * heat * pulse * emit_gain;
	vec3 fire = mix(dull, mid, smoothstep(0.15, 0.55, g));
	fire = mix(fire, hot, smoothstep(0.55, 0.9, g));
	vec3 col = mix(a.rgb, fire, smoothstep(0.04, 0.25, g));
	ALBEDO = col;
	ALPHA = a.a * fade;
}
"""

const DEBRIS_SHADER := """
shader_type spatial;
render_mode unshaded, blend_mix, depth_draw_never, cull_disabled, shadows_disabled, fog_disabled;
uniform sampler2D tex : source_color, filter_linear_mipmap, repeat_disable;
uniform float warm = 0.0;
uniform float shard = 0.0;            // R-C9-118 (b): 0 snow-and-earth clods, 0.5 broken stone, 1 ice shards
varying vec4 v_c;
void vertex() { v_c = INSTANCE_CUSTOM; }      // x: heat 0..1, y: alpha
void fragment() {
	if (warm > 0.5) { discard; }
	vec4 t = texture(tex, UV);
	// a lump of the ground thrown out: the painted ember sprite's shape, darkened as it cools
	vec3 rock = shard > 0.75 ? vec3(0.70, 0.84, 0.93) : (shard > 0.25 ? vec3(0.30, 0.28, 0.26) : vec3(0.16, 0.12, 0.10));
	vec3 c = mix(rock, t.rgb, v_c.x);
	ALBEDO = c;
	ALPHA = t.a * v_c.y;
}
"""

var scene
var cam: Camera3D
var ok := false
var warmed := false
var report := {}
var last_us := 0
var life := 12.6
var slots: Array = []              # {mi, mat, age, live, fade_from, variant, debris: [..]}
var variants: Array = []           # {mesh, albedo, emit}
var embers: GPUParticles3D
var smoke: GPUParticles3D
var deb_mm: MultiMesh
var deb_mat: ShaderMaterial
var _debris: Array = []            # {pos, vel, rest, spin, size, slot}
var _shader: Shader
var _clock := 0.0
var _warm := 0
var _collapsed := Transform3D(Basis(Vector3.ZERO, Vector3.ZERO, Vector3.ZERO), Vector3.ZERO)
var _emit_slot := -1
var _no_embers := false
# R-C9-118 CRATER v5, each part its own toggle until Matt looks (?v5=abc, any subset; desktop -- --v5 abc):
#   a  the fall stops on the first object it hits (meteor_fx: the proxies), no bowl there, a scorch at its base
#   b  the crater by the ground it lands on: snow (v4), ice, earth (the splat)
#   (c, the dressing burning, was tried and dropped: R-C9-118, Matt "if burning is not feasible, let's skip it" --
#    +0.72 ms a frame with 4 impacts on the phone renderer after one focused cut (1.85 ms first); take/build/crater_v5.json)
var v5 := ""
var scorch = null                   # (a): crater_fx.gd's draped skin, scorch only, depth-tested: hidden where the object stands
var _no_smoke := false
var _smoke_sheet := false              # R-C9-128: ?smoke=sheet -- the painted wisp sheet (before)
## R-C9-128 smoke puffs (wwcr-style dust): count, life, size, peak alpha, the Barrow's shadow grey-lilac
const SMOKE_PUFFS := 22
const SMOKE_LIFE_MIN := 0.55
const SMOKE_LIFE_MAX := 1.30
const SMOKE_SIZE := 0.70
const SMOKE_ALPHA := 0.70
const SMOKE_COLOR := Color(0.91, 0.90, 0.94)    # light: it reads over the dark bowl, a shade under the snow
const STEAM_COLOR := Color(0.96, 0.97, 1.0)


func setup(p_scene, p_cam: Camera3D, noise: Texture2D, level: int = 20) -> bool:
	scene = p_scene
	cam = p_cam
	life = fire_life_s(level)
	for s in SEEDS + SEEDS_ICE + SEEDS_EARTH:
		var mesh = _load_mesh(DATA + "crater_%d.glb" % s)
		var alb: Texture2D = load(DATA + "crater_%d_albedo.png" % s) if ResourceLoader.exists(DATA + "crater_%d_albedo.png" % s) else null
		var emi: Texture2D = load(DATA + "crater_%d_emit.png" % s) if ResourceLoader.exists(DATA + "crater_%d_emit.png" % s) else null
		if mesh == null or alb == null or emi == null:
			continue
		variants.append({"seed": s, "mesh": mesh, "albedo": alb, "emit": emi,
			"surf": "ice" if SEEDS_ICE.has(s) else ("earth" if SEEDS_EARTH.has(s) else "snow")})
	if variants.is_empty():
		report["error"] = "no crater variants under " + DATA
		return false
	_shader = Shader.new()
	_shader.code = SKIN
	for i in POOL:
		var mat := ShaderMaterial.new()
		mat.shader = _shader
		mat.render_priority = PaintStack.AFTER_POST_PRIORITY
		mat.set_shader_parameter("noise_tex", noise)
		mat.set_shader_parameter("life", life)
		var v: Dictionary = variants[i % variants.size()]
		mat.set_shader_parameter("albedo_tex", v["albedo"])
		mat.set_shader_parameter("emit_tex", v["emit"])
		var mi := MeshInstance3D.new()
		mi.name = "CraterV4_%d" % i
		mi.mesh = v["mesh"]
		mi.material_override = mat
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		mi.visible = false
		add_child(mi)
		slots.append({"mi": mi, "mat": mat, "age": 1e9, "live": false, "fade_from": -1.0, "variant": i % variants.size()})
	_build_particles()
	_build_debris()
	if Slots.arg("v5").contains("a"):
		scorch = load("res://scripts/crater_fx.gd").new()
		scorch.name = "CraterScorch"
		add_child(scorch)
		scorch.setup(scene, cam, noise, Vector3(0.5, 0.7, 0.5), 0.75)
		scorch.dent = false
		for sl2 in scorch.slots:
			(sl2["mat"] as ShaderMaterial).set_shader_parameter("scorch_only", 1.0)
	_warm = 4
	var a := OS.get_cmdline_user_args()
	_no_embers = a.has("--v4-no-embers")
	_no_smoke = a.has("--v4-no-smoke")
	v5 = Slots.arg("v5")
	ok = true
	report = {"variants": variants.size(), "pool": POOL, "fire_life_s": life, "debris": DEBRIS,
		"draws": {"skins": POOL, "embers": 1, "smoke": 1, "debris": 1}}
	return true


func _load_mesh(path: String) -> Mesh:
	if not ResourceLoader.exists(path):
		return null
	var ps: PackedScene = load(path)
	if ps == null:
		return null
	var n := ps.instantiate()
	var found: Mesh = null
	for c in n.find_children("*", "MeshInstance3D", true, false):
		found = (c as MeshInstance3D).mesh
		break
	n.free()
	return found


func _sprite_mat(tex: Texture2D, frames_h: int, frames_v: int, additive: bool) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	if additive:
		m.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	m.billboard_mode = BaseMaterial3D.BILLBOARD_PARTICLES
	m.albedo_texture = tex
	m.vertex_color_use_as_albedo = true
	m.particles_anim_h_frames = frames_h
	m.particles_anim_v_frames = frames_v
	m.particles_anim_loop = false
	m.render_priority = PaintStack.AFTER_POST_PRIORITY
	return m


func _build_particles() -> void:
	# EMBERS: the kit's painted ember sprite, small, rising and drifting off the cracks while they burn
	embers = GPUParticles3D.new()
	embers.name = "CraterEmbers"
	embers.amount = 40
	embers.lifetime = 1.6
	embers.emitting = false
	embers.local_coords = false
	embers.visibility_aabb = AABB(Vector3(-3, -1, -3), Vector3(6, 5, 6))
	var pm := ParticleProcessMaterial.new()
	pm.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_RING
	pm.emission_ring_axis = Vector3.UP
	pm.emission_ring_radius = 0.9
	pm.emission_ring_inner_radius = 0.1
	pm.emission_ring_height = 0.02
	pm.direction = Vector3.UP
	pm.spread = 25.0
	pm.initial_velocity_min = 0.35
	pm.initial_velocity_max = 0.9
	pm.gravity = Vector3(0.15, 0.25, 0.0)
	pm.scale_min = 0.6               # of the quad's own 0.14 m (the size lives on the mesh: the material's scale alone
	pm.scale_max = 1.0               # did not hold on the Compatibility renderer)
	var grad := Gradient.new()
	grad.set_color(0, Color(1.0, 0.85, 0.5, 1.0))
	grad.set_color(1, Color(0.8, 0.15, 0.05, 0.0))
	var gt := GradientTexture1D.new()
	gt.gradient = grad
	pm.color_ramp = gt
	embers.process_material = pm
	var q := QuadMesh.new()
	q.size = Vector2(0.14, 0.14)
	q.material = _sprite_mat(load(DATA + "ember.png"), 1, 1, true)
	embers.draw_pass_1 = q
	add_child(embers)
	# SMOKE. R-C9-128 (Matt: "the smoke that is a video of steam/wisps doesn't look good ... it would be much better
	# if it were light smoke particles, similar to what we had in the original EoR warlord whirlwind"): light, NEUTRAL
	# puffs built the way the clean-room whirlwind builds its dust (reincarnated-godot wwcr_whirlwind.gd: the shed
	# quanta and scuffs) -- a soft radial sprite (its _soft_radial_texture: 1 - d, to the power 2.1), no flipbook, each
	# puff discrete and brief, thrown up with a little drift and DRAG (an exponential slow-down: wwcr's SHED_DRAG_TAU
	# 0.16 s is damping here), fading as kq^0.55 (wwcr's shed fade), never tinted by the fire. In the Barrow's palette:
	# the cool grey-lilac of its shadows on snow, not wwcr's tile-grey. ?smoke=sheet keeps the painted wisp sheet.
	_smoke_sheet = Slots.arg("smoke") == "sheet"
	smoke = GPUParticles3D.new()
	smoke.name = "CraterSmoke"
	smoke.emitting = false
	smoke.local_coords = false
	smoke.visibility_aabb = AABB(Vector3(-3, -1, -3), Vector3(6, 7, 6))
	var sm := ParticleProcessMaterial.new()
	sm.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_RING
	sm.emission_ring_axis = Vector3.UP
	sm.emission_ring_radius = 0.75
	sm.emission_ring_inner_radius = 0.0
	sm.emission_ring_height = 0.02
	sm.direction = Vector3.UP
	var sq := QuadMesh.new()
	if _smoke_sheet:
		smoke.amount = 10
		smoke.lifetime = 3.2
		sm.spread = 12.0
		sm.initial_velocity_min = 0.25
		sm.initial_velocity_max = 0.45
		sm.gravity = Vector3(0.12, 0.08, 0.05)
		sm.scale_min = 0.7
		sm.scale_max = 1.0
		sm.anim_speed_min = 1.0
		sm.anim_speed_max = 1.0
		var sg := Gradient.new()
		sg.set_color(0, Color(1, 1, 1, 0.0))
		sg.add_point(0.2, Color(1, 1, 1, 0.8))
		sg.set_color(sg.get_point_count() - 1, Color(1, 1, 1, 0.0))
		var st := GradientTexture1D.new()
		st.gradient = sg
		sm.color_ramp = st
		sq.size = Vector2(0.6, 1.2)
		sq.material = _sprite_mat(load(DATA + "smoke_sheet.png"), 4, 2, false)
	else:
		smoke.amount = SMOKE_PUFFS
		smoke.lifetime = SMOKE_LIFE_MAX
		smoke.randomness = 0.0
		sm.lifetime_randomness = 1.0 - SMOKE_LIFE_MIN / SMOKE_LIFE_MAX     # each puff 0.55 .. 1.3 s
		sm.spread = 35.0
		sm.initial_velocity_min = 0.40
		sm.initial_velocity_max = 0.90
		sm.damping_min = 0.35                # drag: the throw dies out, then the drift carries it
		sm.damping_max = 0.60
		sm.gravity = Vector3(0.10, 0.10, 0.04)
		sm.scale_min = 0.75
		sm.scale_max = 1.15
		var sc := Curve.new()                # a puff swells a little as it thins
		sc.add_point(Vector2(0.0, 0.7))
		sc.add_point(Vector2(1.0, 1.35))
		var sct := CurveTexture.new()
		sct.curve = sc
		sm.scale_curve = sct
		var sg2 := Gradient.new()            # wwcr's shed fade: alpha = kq^0.55 of the life left, after a quick rise
		var offs := PackedFloat32Array([0.0])
		var cols := PackedColorArray([Color(1, 1, 1, 0.0)])
		for i in range(0, 9):
			var u := float(i) / 8.0
			offs.append(lerpf(0.08, 1.0, u))
			cols.append(Color(1, 1, 1, SMOKE_ALPHA * pow(1.0 - u, 0.55)))
		sg2.offsets = offs
		sg2.colors = cols
		var st2 := GradientTexture1D.new()
		st2.gradient = sg2
		sm.color_ramp = st2
		sq.size = Vector2(SMOKE_SIZE, SMOKE_SIZE)
		var pm2 := StandardMaterial3D.new()
		pm2.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		pm2.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		pm2.blend_mode = BaseMaterial3D.BLEND_MODE_MIX
		pm2.billboard_mode = BaseMaterial3D.BILLBOARD_PARTICLES
		pm2.albedo_texture = _soft_puff_texture()
		pm2.vertex_color_use_as_albedo = true
		pm2.albedo_color = SMOKE_COLOR
		pm2.disable_receive_shadows = true
		pm2.render_priority = PaintStack.AFTER_POST_PRIORITY
		sq.material = pm2
	smoke.process_material = sm
	smoke.draw_pass_1 = sq
	add_child(smoke)


static func _soft_puff_texture() -> ImageTexture:
	"""wwcr_whirlwind.gd's _soft_radial_texture, byte for byte: 64 px, alpha (1 - d)^2.1."""
	var n := 64
	var img := Image.create(n, n, false, Image.FORMAT_RGBAF)
	var c := (n - 1) * 0.5
	for y in range(n):
		for x in range(n):
			var d := Vector2(x - c, y - c).length() / c
			var a: float = clampf(1.0 - d, 0.0, 1.0)
			a = pow(a, 2.1)
			img.set_pixel(x, y, Color(1, 1, 1, a))
	return ImageTexture.create_from_image(img)


func _build_debris() -> void:
	deb_mat = ShaderMaterial.new()
	var sh := Shader.new()
	sh.code = DEBRIS_SHADER
	deb_mat.shader = sh
	deb_mat.set_shader_parameter("tex", load(DATA + "ember.png"))
	deb_mat.render_priority = PaintStack.AFTER_POST_PRIORITY
	var q := QuadMesh.new()
	q.size = Vector2(1, 1)
	q.material = deb_mat
	deb_mm = MultiMesh.new()
	deb_mm.transform_format = MultiMesh.TRANSFORM_3D
	deb_mm.use_custom_data = true
	deb_mm.mesh = q
	deb_mm.instance_count = DEBRIS * POOL
	for i in deb_mm.instance_count:
		deb_mm.set_instance_transform(i, _collapsed)
	var mmi := MultiMeshInstance3D.new()
	mmi.name = "CraterDebris"
	mmi.multimesh = deb_mm
	mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mmi.custom_aabb = AABB(Vector3(-500, -100, -500), Vector3(1000, 200, 1000))
	add_child(mmi)


func start(target: Vector3, surf := "snow", obj := {}) -> Dictionary:
	"""A crater at target: the oldest skin taken when all are live, a random painted variant (never rotated), the
	snow pressed, the bowl scaled to the snow's depth, the debris thrown, the embers and smoke moved here."""
	var t0 := Time.get_ticks_usec()
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
	# (b) a variant of THIS ground (snow if it has none); (a) on an object, no bowl: a scorch at its base instead
	var pool_v := []
	for i in variants.size():
		if String(variants[i]["surf"]) == surf:
			pool_v.append(i)
	if pool_v.is_empty():
		for i in variants.size():
			if String(variants[i]["surf"]) == "snow":
				pool_v.append(i)
		surf = "snow"
	var vi: int = pool_v[randi() % pool_v.size()]
	var v: Dictionary = variants[vi]
	var mi: MeshInstance3D = sl["mi"]
	if int(sl["variant"]) != vi:
		mi.mesh = v["mesh"]
		(sl["mat"] as ShaderMaterial).set_shader_parameter("albedo_tex", v["albedo"])
		(sl["mat"] as ShaderMaterial).set_shader_parameter("emit_tex", v["emit"])
		sl["variant"] = vi
	var snow = scene.snow if scene != null else null
	var D := 0.0
	var base_y := target.y
	var on_obj := not obj.is_empty()
	if snow != null:
		D = float(snow.depth_at(Vector2(target.x, target.z)))
		base_y = float(snow.surface_y(Vector2(target.x, target.z)))
		if surf == "snow" and not on_obj:
			snow._stamp(Vector2(target.x, target.z), Vector2(0, 1), 0.9, 0.9, 0.25, 0.6)      # the real dent under the bowl
	# the mesh at its full shape (the painting was made of it); the depth bias puts it over the snow
	var ys := 1.0
	mi.transform = Transform3D(Basis.IDENTITY.scaled(Vector3(1.0, ys, 1.0)), Vector3(target.x, base_y + 0.01, target.z))
	mi.visible = not on_obj
	if on_obj and scorch != null:
		scorch.start(Vector3(target.x, base_y, target.z), func(p): return float(snow.surface_y(Vector2(p.x, p.z))) if snow != null else base_y)
	sl["live"] = true
	var burn_at: Vector3 = obj["at"] if on_obj else target
	sl["burn_at"] = burn_at
	sl["age"] = 0.0
	sl["fade_from"] = -1.0
	(sl["mat"] as ShaderMaterial).set_shader_parameter("fade", 1.0)
	(sl["mat"] as ShaderMaterial).set_shader_parameter("age", 0.0)
	(sl["mat"] as ShaderMaterial).set_shader_parameter("emit_gain", 0.4 if surf == "ice" else 1.0)
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
	# the particles move to the newest crater
	embers.global_position = Vector3(target.x, base_y + 0.03, target.z) if not on_obj else (obj["at"] as Vector3)
	smoke.global_position = Vector3(target.x, base_y + 0.05, target.z) if not on_obj else (obj["at"] as Vector3)
	# (b) ice: steam, not smoke -- the same painted wisp, white, quicker and shorter; shards for debris
	var spm := smoke.process_material as ParticleProcessMaterial
	spm.initial_velocity_min = 0.6 if surf == "ice" else 0.25
	spm.initial_velocity_max = 0.9 if surf == "ice" else 0.45
	if _smoke_sheet:
		(smoke.draw_pass_1.surface_get_material(0) as StandardMaterial3D).albedo_color = Color(1.25, 1.25, 1.3, 0.75) if surf == "ice" else Color(1, 1, 1, 1)
	else:
		# ice: steam -- the same puffs, whiter and quicker
		(smoke.draw_pass_1.surface_get_material(0) as StandardMaterial3D).albedo_color = STEAM_COLOR if surf == "ice" else SMOKE_COLOR
		spm.initial_velocity_min = 0.6 if surf == "ice" else 0.40
		spm.initial_velocity_max = 1.0 if surf == "ice" else 0.90
	deb_mat.set_shader_parameter("shard", 1.0 if surf == "ice" else (0.5 if surf == "earth" else 0.0))
	embers.restart()
	smoke.restart()
	embers.emitting = not _no_embers
	smoke.emitting = not _no_smoke
	_emit_slot = pick
	# the debris: DEBRIS lumps thrown out, landing on the snow round the rim, where they stay
	_debris = _debris.filter(func(d): return int(d["slot"]) != pick)
	for k in DEBRIS:
		var a := randf() * TAU
		var sp := randf_range(0.6, 1.6)
		_debris.append({"slot": pick, "k": k, "pos": Vector3(target.x, base_y + 0.15, target.z),
			"vel": Vector3(cos(a) * sp, randf_range(1.6, 3.0), sin(a) * sp), "landed": false,
			"size": randf_range(0.06, 0.13), "ground": base_y})
	var rec := {"slot": pick, "variant": int(variants[vi]["seed"]), "surf": surf, "on_object": String(obj.get("id", "")), "snow_D": snippet(D), "bowl_scale": snippet(ys),
		"start_us": Time.get_ticks_usec() - t0}
	report["last_start"] = rec
	return rec


static func snippet(x: float) -> float:
	return snappedf(x, 0.001)


func _process(dt: float) -> void:
	var t0 := Time.get_ticks_usec()
	_clock += dt
	if _warm > 0:
		_warm -= 1
		var on := 1.0 if _warm > 0 else 0.0
		var at := cam.global_position + (-cam.global_transform.basis.z) * 5.0
		for sl in slots:
			var mi: MeshInstance3D = sl["mi"]
			(sl["mat"] as ShaderMaterial).set_shader_parameter("warm", on)
			mi.global_position = at
			mi.visible = _warm > 0
		deb_mat.set_shader_parameter("warm", on)
		deb_mm.set_instance_transform(0, Transform3D(Basis.IDENTITY.scaled(Vector3.ONE * 0.01), at) if _warm > 0 else _collapsed)
		embers.global_position = at
		smoke.global_position = at
		embers.emitting = _warm > 0
		smoke.emitting = _warm > 0
		if _warm == 0:
			embers.emitting = false
			smoke.emitting = false
			warmed = true
		return
	for i in slots.size():
		var sl: Dictionary = slots[i]
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
				_debris = _debris.filter(func(d): return int(d["slot"]) != i)
				for k in DEBRIS:
					deb_mm.set_instance_transform(i * DEBRIS + k, _collapsed)
		if i == _emit_slot:
			# the embers thin and the smoke lingers as the field cools; both stop at its end
			var k := clampf(float(sl["age"]) / life, 0.0, 1.0)
			embers.amount_ratio = clampf(1.0 - k * 1.1, 0.0, 1.0)
			smoke.amount_ratio = clampf(1.0 - k * 0.8, 0.0, 1.0)
			if float(sl["age"]) > life:
				embers.emitting = false
				smoke.emitting = false
				_emit_slot = -1
	_step_debris(dt)
	last_us = Time.get_ticks_usec() - t0


func _step_debris(dt: float) -> void:
	if _debris.is_empty():
		return
	var b := cam.global_transform.basis
	for d in _debris:
		var sl: Dictionary = slots[int(d["slot"])]
		var p: Vector3 = d["pos"]
		if not bool(d["landed"]):
			var v: Vector3 = d["vel"]
			v.y -= 9.8 * dt
			p += v * dt
			d["vel"] = v
			var gy := float(scene.snow.surface_y(Vector2(p.x, p.z))) if scene.snow != null else float(d["ground"])
			if p.y <= gy + 0.02 and v.y < 0.0:
				p.y = gy + 0.02
				d["landed"] = true
			d["pos"] = p
		var s: float = float(d["size"])
		var heat := clampf(1.0 - float(sl["age"]) / (life * 0.35), 0.0, 1.0)
		var fa := 1.0
		if float(sl["fade_from"]) >= 0.0:
			fa = clampf(1.0 - (float(sl["age"]) - float(sl["fade_from"])) / FADE_S, 0.0, 1.0)
		var idx := int(d["slot"]) * DEBRIS + int(d["k"])
		deb_mm.set_instance_transform(idx, Transform3D(Basis(b.x.normalized() * s, b.y.normalized() * s, b.z.normalized() * 0.01), p))
		deb_mm.set_instance_custom_data(idx, Color(heat, fa, 0.0, 0.0))


func live_count() -> int:
	var n := 0
	for sl in slots:
		if bool(sl["live"]):
			n += 1
	return n
