extends Node3D
## C-9 R-C9-142 -- THE METEOR'S MARK ON WHAT STANDS NEAR IT (Matt retired crater v5 (a), "the meteor stops on the first
## object"). drax. The Meteor now ALWAYS lands on the targeted ground point (crater, fire, smoke, particles there); this
## node only answers "what was standing next to it":
##   SCORCH   every placed 3D piece whose bounds come within BLAST_R of the impact takes a char on the side FACING the
##            impact: a SHELL -- the piece's own mesh drawn again over itself (same transform, a 3 cm view-space nudge
##            toward the camera, depth-tested, no depth write), unshaded, alpha = facing x distance falloff x a noise
##            break-up, a brief ember glow then char, held, then faded (HOLD_S .. FADE_END_S). The painted GROUND is
##            never drawn by it: a shell exists only where its own piece's surface is the nearest thing.
##   KICK     a few embers and dark chips thrown off the facing side (one MultiMesh, CPU-stepped, camera-facing quads).
##   SHAKE    LIGHT props only (birches, cairns, posts): a few cm, ~0.2 s, away from the impact. Standing stones,
##            outcrops, shore rock, logs, the lintel and the mound never move. A baked prop (cairn, post) wears its
##            own UVs and moves as is; a PROJECTED prop (a birch wears the painting through the fixed camera) would
##            leave its paint behind, so for the shake it wears a twin of its live material whose projection is taken
##            at the REST position (`v_world - shake_off`) -- built and drawn once at load (warm), never at cast time.
## Nothing here intercepts the fall and nothing is ray-cast: the objects are a list of bounds built once.

const BLAST_R := 2.2                 # m from the impact to the nearest point of a piece's bounds
const MAX_OBJ := 6                   # the nearest pieces scorched per impact
const SHELLS := 16                   # pooled shell instances (a piece can be several meshes)
const HOLD_S := 2.5
const FADE_END_S := 6.0
const KICK_PER_OBJ := 7              # 4 embers + 3 chips
const KICK_POOL := MAX_OBJ * KICK_PER_OBJ * 2
const SHAKE_S := 0.2
const SHAKE_M := 0.035
const LIGHT := ["birch", "cairn", "post"]
const SKIP := ["mound", "shield", "raven", ""]
const DATA := "res://data/vfx/crater_v4/"

const SHELL_SHADER := """
shader_type spatial;
render_mode unshaded, blend_mix, depth_draw_never, cull_back, shadows_disabled, fog_disabled, specular_disabled;
uniform sampler2D noise_tex : filter_linear_mipmap, repeat_enable;
uniform vec3 imp = vec3(0.0);
uniform float radius = 2.2;
uniform float age = 0.0;
uniform float fade = 1.0;
uniform float warm = 0.0;
uniform float web = 0.0;              // 1 on Compatibility, where ALBEDO is read as sRGB
varying vec3 v_world;
varying vec3 v_n;
void vertex() {
	v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	v_n = normalize((MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz);
	vec4 vp = MODELVIEW_MATRIX * vec4(VERTEX, 1.0);
	vp.z += 0.03;                     // toward the camera: a depth bias that cannot move the silhouette (ortho)
	POSITION = PROJECTION_MATRIX * vp;
}
void fragment() {
	if (warm > 0.5) { discard; }
	vec3 to = imp - v_world;
	float d = length(to);
	float face = smoothstep(-0.05, 0.6, dot(normalize(v_n), to / max(d, 1e-3)));
	float fall = 1.0 - smoothstep(radius * 0.3, radius * 1.1, d);
	float h = max(v_world.y - imp.y, 0.0);
	float low = 1.0 - smoothstep(0.5, 2.6, h);
	float n = texture(noise_tex, v_world.xz * 0.85 + vec2(v_world.y * 0.6, -v_world.y * 0.4)).r;
	float k = face * fall * mix(0.45, 1.0, low);
	k *= smoothstep(0.30, 0.62, n + k * 0.45);
	float glow = clamp(1.0 - age / 0.9, 0.0, 1.0);
	vec3 chr = vec3(0.075, 0.048, 0.036);
	vec3 hot = vec3(1.0, 0.42, 0.10);
	vec3 c = mix(chr, hot, glow * smoothstep(0.35, 0.9, k) * 0.85);
	ALBEDO = web > 0.5 ? c : pow(c, vec3(2.2));
	ALPHA = clamp(k * 1.4, 0.0, 0.82) * fade;
}
"""

const KICK_SHADER := """
shader_type spatial;
render_mode unshaded, blend_mix, depth_draw_never, cull_disabled, shadows_disabled, fog_disabled;
uniform sampler2D tex : source_color, filter_linear_mipmap, repeat_disable;
uniform float warm = 0.0;
varying vec4 v_c;
void vertex() { v_c = INSTANCE_CUSTOM; }      // x: heat 0..1 (1 an ember), y: alpha
void fragment() {
	if (warm > 0.5) { discard; }
	vec4 t = texture(tex, UV);
	ALBEDO = mix(vec3(0.10, 0.075, 0.06), t.rgb, v_c.x);
	ALPHA = t.a * v_c.y;
}
"""

var scene
var cam: Camera3D
var ok := false
var warmed := false
var report := {}
var objects: Array = []            # {id, cls, node, aabb, light, meshes: [MeshInstance3D], projected}
var shells: Array = []             # {mi, mat, age, live}
var _shell_shader: Shader
var _kick_mm: MultiMesh
var _kick_mat: ShaderMaterial
var _kicks: Array = []             # {i, pos, vel, age, life, ember, size, ground}
var _kick_next := 0
var _shakes: Array = []            # {obj, base, dir, t, twins: [[mi, plain_mat, twin_mat]]}
var _twin_cache := {}              # live Shader -> its shake twin (v_world at rest)
var _collapsed := Transform3D(Basis(Vector3.ZERO, Vector3.ZERO, Vector3.ZERO), Vector3.ZERO)
var last_us := 0
var hits: Array = []


func setup(p_scene, p_cam: Camera3D, noise: Texture2D) -> bool:
	scene = p_scene
	cam = p_cam
	_shell_shader = Shader.new()
	_shell_shader.code = SHELL_SHADER
	for i in SHELLS:
		var m := ShaderMaterial.new()
		m.shader = _shell_shader
		m.render_priority = PaintStack.AFTER_POST_PRIORITY
		m.set_shader_parameter("noise_tex", noise)
		m.set_shader_parameter("radius", BLAST_R)
		m.set_shader_parameter("web", 1.0 if PaintStack.is_compatibility() else 0.0)
		var mi := MeshInstance3D.new()
		mi.name = "Scorch_%d" % i
		mi.top_level = true
		mi.material_override = m
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		mi.layers = 1 << 12                       # the meteor's own FX layer: no light, no shadow map
		mi.visible = false
		add_child(mi)
		shells.append({"mi": mi, "mat": m, "age": 1e9, "live": false})
	_kick_mat = ShaderMaterial.new()
	var ks := Shader.new()
	ks.code = KICK_SHADER
	_kick_mat.shader = ks
	_kick_mat.set_shader_parameter("tex", load(DATA + "ember.png"))
	_kick_mat.render_priority = PaintStack.AFTER_POST_PRIORITY
	var q := QuadMesh.new()
	q.size = Vector2(1, 1)
	q.material = _kick_mat
	_kick_mm = MultiMesh.new()
	_kick_mm.transform_format = MultiMesh.TRANSFORM_3D
	_kick_mm.use_custom_data = true
	_kick_mm.mesh = q
	_kick_mm.instance_count = KICK_POOL
	for i in KICK_POOL:
		_kick_mm.set_instance_transform(i, _collapsed)
	var mmi := MultiMeshInstance3D.new()
	mmi.name = "ScorchKick"
	mmi.multimesh = _kick_mm
	mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mmi.custom_aabb = AABB(Vector3(-500, -100, -500), Vector3(1000, 200, 1000))
	add_child(mmi)
	_build_objects()
	ok = not objects.is_empty()
	report = {"objects": objects.size(), "light": objects.filter(func(o): return bool(o["light"])).size(),
		"blast_r": BLAST_R, "max_obj": MAX_OBJ, "shells": SHELLS, "kick_pool": KICK_POOL}
	return ok


func _build_objects() -> void:
	objects.clear()
	if scene == null or not ("nodes" in scene) or not ("layout" in scene):
		return
	for e in scene.layout["placements"]:
		var id := String(e["id"])
		var cls := String(e.get("class", ""))
		if id == "mound" or cls in SKIP or not scene.nodes.has(id):
			continue
		var n: Node3D = scene.nodes[id]
		var meshes: Array = []
		for c in n.find_children("*", "MeshInstance3D", true, false):
			var mi := c as MeshInstance3D
			if mi.visible and mi.mesh != null and mi.material_override is ShaderMaterial:
				meshes.append(mi)
		if meshes.is_empty():
			continue
		var wb: AABB = n.global_transform * scene._node_aabb(n)
		var proj := false
		var m0 := (meshes[0] as MeshInstance3D).material_override as ShaderMaterial
		if m0.get_shader_parameter("project_uv") == true:
			proj = true
		objects.append({"id": id, "cls": cls, "node": n, "aabb": wb, "light": cls in LIGHT, "meshes": meshes,
			"projected": proj, "base": n.position})


static func _closest(b: AABB, p: Vector3) -> Vector3:
	return Vector3(clampf(p.x, b.position.x, b.end.x), clampf(p.y, b.position.y, b.end.y), clampf(p.z, b.position.z, b.end.z))


func hit(target: Vector3) -> Dictionary:
	"""The impact at the ground point `target`: the nearest pieces within BLAST_R scorched, kicked and (light ones)
	shaken. Returns the record."""
	var t0 := Time.get_ticks_usec()
	var near: Array = []
	for o in objects:
		var c := _closest(o["aabb"], target)
		var d := Vector2(c.x - target.x, c.z - target.z).length()
		if d <= BLAST_R:
			near.append([d, o, c])
	near.sort_custom(func(a, b): return float(a[0]) < float(b[0]))
	near = near.slice(0, MAX_OBJ)
	var rec := {"target": [snappedf(target.x, 0.01), snappedf(target.y, 0.01), snappedf(target.z, 0.01)], "objects": []}
	for row in near:
		var o: Dictionary = row[1]
		var c: Vector3 = row[2]
		for mi in o["meshes"]:
			_take_shell(mi as MeshInstance3D, target)
		_kick(o, c, target)
		var shaken := false
		if bool(o["light"]):
			shaken = _shake(o, target)
		rec["objects"].append({"id": o["id"], "cls": o["cls"], "d_m": snappedf(float(row[0]), 0.01), "shells": (o["meshes"] as Array).size(),
			"shake": shaken})
	rec["us"] = Time.get_ticks_usec() - t0
	hits.append(rec)
	report["last_hit"] = rec
	return rec


func _take_shell(src: MeshInstance3D, target: Vector3) -> void:
	var pick := -1
	var oldest := -1.0
	for i in shells.size():
		if not bool(shells[i]["live"]):
			pick = i
			break
		if float(shells[i]["age"]) > oldest:
			oldest = float(shells[i]["age"])
			pick = i
	var sh: Dictionary = shells[pick]
	var mi: MeshInstance3D = sh["mi"]
	mi.mesh = src.mesh
	mi.global_transform = src.global_transform
	mi.visible = true
	sh["src"] = src
	sh["live"] = true
	sh["age"] = 0.0
	var m: ShaderMaterial = sh["mat"]
	m.set_shader_parameter("imp", target)
	m.set_shader_parameter("age", 0.0)
	m.set_shader_parameter("fade", 1.0)


func _kick(o: Dictionary, c: Vector3, target: Vector3) -> void:
	var b: AABB = o["aabb"]
	var away := Vector3(target.x - c.x, 0.0, target.z - c.z)
	if away.length() < 1e-3:
		away = Vector3(1, 0, 0)
	away = away.normalized()
	var gy := float(scene.snow.surface_y(Vector2(c.x, c.z))) if scene.snow != null else target.y
	for k in KICK_PER_OBJ:
		var ember := k < 4
		var h := randf_range(0.15, minf(b.size.y, 1.6) * 0.7)
		var side := away.cross(Vector3.UP).normalized() * randf_range(-0.35, 0.35) * minf(b.size.x + b.size.z, 2.0) * 0.5
		var p := Vector3(c.x, b.position.y + h, c.z) + side + away * 0.05
		var sp := randf_range(0.8, 2.0)
		var v := (away * sp + away.cross(Vector3.UP).normalized() * randf_range(-0.5, 0.5)
			+ Vector3.UP * randf_range(0.6, 1.8))
		var i := _kick_next
		_kick_next = (_kick_next + 1) % KICK_POOL
		_kicks = _kicks.filter(func(x): return int(x["i"]) != i)
		_kicks.append({"i": i, "pos": p, "vel": v, "age": 0.0, "life": randf_range(0.9, 1.6) if ember else randf_range(1.6, 2.4),
			"ember": ember, "size": randf_range(0.05, 0.09) if ember else randf_range(0.04, 0.07), "ground": gy, "landed": false})


func _shake(o: Dictionary, target: Vector3) -> bool:
	for s in _shakes:
		if String(s["obj"]["id"]) == String(o["id"]):
			s["t"] = 0.0
			return true
	var n: Node3D = o["node"]
	var dir := Vector3(n.global_position.x - target.x, 0.0, n.global_position.z - target.z)
	dir = dir.normalized() if dir.length() > 1e-3 else Vector3(1, 0, 0)
	var twins: Array = []
	if bool(o["projected"]):
		for mi in o["meshes"]:
			var plain := (mi as MeshInstance3D).material_override as ShaderMaterial
			var tw := _twin_material(plain)
			if tw == null:
				return false                      # no twin: a projected piece is not moved (it would shed its paint)
			twins.append([mi, plain, tw])
		for t in twins:
			(t[0] as MeshInstance3D).material_override = t[2]
	_shakes.append({"obj": o, "base": o["base"], "dir": dir, "t": 0.0, "twins": twins})
	return true


func _twin_shader(live: Shader) -> Shader:
	if _twin_cache.has(live):
		return _twin_cache[live]
	var code := live.code
	var line := "v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;"
	var tw: Shader = null
	if code.count(line) == 1 and code.contains("varying vec3 v_world;"):
		code = code.replace(line, "v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz - shake_off;")
		code = code.replace("varying vec3 v_world;", "varying vec3 v_world;\nuniform vec3 shake_off = vec3(0.0);")
		tw = Shader.new()
		tw.code = code
	_twin_cache[live] = tw
	return tw


func _twin_material(plain: ShaderMaterial) -> ShaderMaterial:
	if plain == null or plain.shader == null:
		return null
	var sh := _twin_shader(plain.shader)
	if sh == null:
		return null
	var m := plain.duplicate() as ShaderMaterial
	m.shader = sh
	return m


func warm(at: Vector3, on: bool) -> void:
	"""Drawn once in view under the meteor's own warm (its painted fx variants live): a shell, the kick quads and
	a birch's shake twin of the LIVE shader, every fragment discarded or unseen; then hidden."""
	# a shell on one piece of each kind (a projected birch, a baked prop, a stone), so every mesh a hit can draw
	# a shell over has drawn one before the first cast
	var kinds: Array = []
	for want in ["birch", "cairn", "post", "stone_tall", "outcrop"]:
		for o in objects:
			if String(o["cls"]) == want:
				kinds.append(o)
				break
	for i in mini(kinds.size(), shells.size()):
		var sh: Dictionary = shells[i]
		var mi: MeshInstance3D = sh["mi"]
		(sh["mat"] as ShaderMaterial).set_shader_parameter("warm", 1.0 if on else 0.0)
		if on:
			var src: MeshInstance3D = kinds[i]["meshes"][0]
			mi.mesh = src.mesh
			mi.global_transform = Transform3D(Basis.IDENTITY.scaled(Vector3.ONE * 0.01), at + Vector3(0.05 * i, 0, 0))
		mi.visible = on
	_kick_mat.set_shader_parameter("warm", 1.0 if on else 0.0)
	_kick_mm.set_instance_transform(0, Transform3D(Basis.IDENTITY.scaled(Vector3.ONE * 0.01), at) if on else _collapsed)
	var bir: Array = objects.filter(func(o): return bool(o["projected"]) and bool(o["light"]))
	if on:
		if not bir.is_empty():
			var src2: MeshInstance3D = bir[0]["meshes"][0]
			# the twin of the birch's LIVE (fx) shader, on a tiny copy of its mesh at `at`
			var tw := _twin_material(src2.material_override as ShaderMaterial)
			if tw != null:
				var twin := MeshInstance3D.new()
				twin.name = "ScorchTwinWarm"
				twin.top_level = true
				twin.mesh = src2.mesh
				twin.material_override = tw
				twin.layers = src2.layers
				twin.global_transform = Transform3D(Basis.IDENTITY.scaled(Vector3.ONE * 0.01), at)
				add_child(twin)
		report["twin_shaders"] = _twin_cache.size()
		report["warm_kinds"] = kinds.map(func(o): return o["cls"])
	else:
		for c in get_children():
			if String(c.name) == "ScorchTwinWarm":
				c.queue_free()
		warmed = true


func live_count() -> int:
	var n := 0
	for s in shells:
		if bool(s["live"]):
			n += 1
	return n


func _process(dt: float) -> void:
	var t0 := Time.get_ticks_usec()
	for sh in shells:
		if not bool(sh["live"]):
			continue
		sh["age"] = float(sh["age"]) + dt
		var a := float(sh["age"])
		var m: ShaderMaterial = sh["mat"]
		m.set_shader_parameter("age", a)
		var f := 1.0 if a < HOLD_S else clampf(1.0 - (a - HOLD_S) / (FADE_END_S - HOLD_S), 0.0, 1.0)
		m.set_shader_parameter("fade", f)
		var src = sh.get("src")
		if src != null and is_instance_valid(src):
			(sh["mi"] as MeshInstance3D).global_transform = (src as MeshInstance3D).global_transform
		if f <= 0.0:
			sh["live"] = false
			(sh["mi"] as MeshInstance3D).visible = false
	for s in _shakes:
		s["t"] = float(s["t"]) + dt
	var done: Array = []
	for s in _shakes:
		var o: Dictionary = s["obj"]
		var n: Node3D = o["node"]
		var t := float(s["t"])
		if t >= SHAKE_S:
			n.position = o["base"]
			for tw in s["twins"]:
				(tw[0] as MeshInstance3D).material_override = tw[1]
			done.append(s)
			continue
		var env := 1.0 - t / SHAKE_S
		var off: Vector3 = (s["dir"] as Vector3) * SHAKE_M * env * sin(t * TAU * 14.0) \
			+ (s["dir"] as Vector3).cross(Vector3.UP) * SHAKE_M * 0.4 * env * sin(t * TAU * 9.0 + 1.1)
		var loc := off
		if n.get_parent() is Node3D:
			loc = (n.get_parent() as Node3D).global_transform.basis.inverse() * off
		n.position = (o["base"] as Vector3) + loc
		for tw in s["twins"]:
			(tw[2] as ShaderMaterial).set_shader_parameter("shake_off", off)
	for s in done:
		_shakes.erase(s)
	if not _kicks.is_empty():
		var b := cam.global_transform.basis
		var gone: Array = []
		for k in _kicks:
			k["age"] = float(k["age"]) + dt
			var p: Vector3 = k["pos"]
			var v: Vector3 = k["vel"]
			if bool(k["ember"]):
				v *= exp(-2.2 * dt)
				v.y += 0.6 * dt
			elif not bool(k["landed"]):
				v.y -= 9.8 * dt
			if not bool(k["landed"]):
				p += v * dt
				if not bool(k["ember"]) and p.y <= float(k["ground"]) + 0.02 and v.y < 0.0:
					p.y = float(k["ground"]) + 0.02
					k["landed"] = true
			k["pos"] = p
			k["vel"] = v
			var u := float(k["age"]) / float(k["life"])
			var i := int(k["i"])
			if u >= 1.0:
				_kick_mm.set_instance_transform(i, _collapsed)
				gone.append(k)
				continue
			var s2 := float(k["size"]) * (1.0 - 0.4 * u if bool(k["ember"]) else 1.0)
			_kick_mm.set_instance_transform(i, Transform3D(Basis(b.x.normalized() * s2, b.y.normalized() * s2, b.z.normalized() * 0.01), p))
			var heat := clampf(1.0 - u * 0.8, 0.0, 1.0) if bool(k["ember"]) else clampf(0.5 - u * 2.0, 0.0, 1.0)
			_kick_mm.set_instance_custom_data(i, Color(heat, clampf((1.0 - u) * 1.6, 0.0, 1.0), 0.0, 0.0))
		for k in gone:
			_kicks.erase(k)
	last_us = Time.get_ticks_usec() - t0
