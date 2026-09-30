"""THE STRIKE TRAIL for knight.gd (T12_11) -- a brushed wash behind the weapon's edge line through each
strike's ACTIVE SWING, faded out within `fade_s` of the swing's end.

WHY. The weapon gate flags every strike whose weapon moves more than 35 px on screen in one frame: the
slash's axe head 80 px, the chop's 62, the shield bash 38. At play speed the weapon STROBES -- it is
here, then there -- and the eye cannot read the swing between. A trail puts the swept arc on screen.

WHAT IT IS. A ribbon swept by the weapon's EDGE LINE: two points in a bone's frame per clip (the axe's
cutting edge, beard to horn, in weapon_r's frame; the shield's rim diameter in LeftHand's), sampled at
every step while the clip is inside its window, smoothed between steps by Catmull-Rom so the arc is
continuous whatever the frame rate, the newest end drawn at the weapon. At the window's end it stops
growing and fades out over fade_s (0.15 s), measured in the clip's own time while the strike runs.
Data, not code: character.json strike_trail (clips: bone, edge, window; fade_s; subdiv; style).

THE LOOK -- a dynamic thing under the painted-light ruling (N-C9-PAINTED-LIGHT-RULING: dynamic things
keep the ramp under the same sun, and the pen). A pale warm wash, soft toward its inner edge and its
tail, broken into dry-brush streaks that run along the stroke; lit through two levels and one soft edge
by the scene's own sun (its first DirectionalLight3D; else the Barrow's winter sun, elevation 55,
azimuth 305), the painting's blue-violet on the side turned from it; and the PEN -- the gear's ink colour
-- a ~1.4 px line along the stroke's outer rim, thinning and breaking toward the tail. Unshaded (the
ramp is computed in the shader from the sun), so the desktop's Forward+ and the phone's Compatibility
draw it alike.

    python3 strike_trail_patch.py <knight.gd in> <knight.gd out>

Refusing: every anchor must match once."""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src).read()

FUNCS = '''

# ==== THE STRIKE TRAIL (T12_11: attack_lab/tools/strike_trail_patch.py) ====
func _add_strike_trail() -> void:
	"""The trail behind each strike's edge line (the StrikeTrail class below), if character.json asks for it."""
	var spec: Dictionary = cfg.get("strike_trail", {})
	if spec.is_empty() or _skel == null:
		return
	_trail = StrikeTrail.new()
	_trail.name = "StrikeTrail"
	add_child(_trail)
	_trail.setup(self, spec)


func trail_state() -> Dictionary:
	"""Which strike is running and where its clip is: {key, clip, pos}, or {} when none is."""
	if _tree == null:
		return {}
	var bt := _tree.tree_root as AnimationNodeBlendTree
	if bt == null:
		return {}
	for key in ["slash", "chop", "bash"]:
		if not bt.has_node("a_" + key):
			continue
		if bool(_tree.get("parameters/os_%s/active" % key)):
			return {"key": key, "clip": String((bt.get_node("a_" + key) as AnimationNodeAnimation).animation),
					"pos": float(_tree.get("parameters/a_%s/current_position" % key))}
	return {}


func trail_step(dt: float) -> void:
	"""The tools' way in (they advance the tree by hand, with trail_auto off): one step after the pose moved."""
	if _trail != null:
		_trail.step(dt)


class StrikeTrail extends MeshInstance3D:
	## THE STRIKE TRAIL -- see attack_lab/tools/strike_trail_patch.py for the why and the look.
	const SHADER := """
shader_type spatial;
render_mode unshaded, blend_mix, cull_disabled, depth_draw_never, shadows_disabled, fog_disabled;
uniform vec3 wash_color : source_color = vec3(0.96, 0.92, 0.84);
uniform vec3 shade_color : source_color = vec3(0.78, 0.78, 0.88);
uniform vec3 pen_color : source_color = vec3(0.055, 0.043, 0.063);
uniform vec3 sun_dir = vec3(-0.47, 0.82, 0.33);
uniform float alpha_max = 0.70;
uniform float pen_px = 1.4;
uniform float bristle_floor = 0.35;
uniform float body_u1 = 0.6;          // the wash's soft falloff from the rim toward the inner edge (u 0.02 .. body_u1)
uniform float tail_pow = 0.75;        // the wash thinning toward the stroke's tail, (1 - v)^tail_pow   // the streaks' thinnest paint (1 = no streaks)
uniform vec3 edge_color : source_color = vec3(0.96, 0.92, 0.84);
uniform float edge_w = 0.0;           // a PALE EDGE along the outer rim, inside the pen, this share of the stroke's width (0 = none)
float h21(vec2 p) { p = fract(p * vec2(123.34, 456.21)); p += dot(p, p + 45.32); return fract(p.x * p.y); }
float vnoise(vec2 p) {
	vec2 i = floor(p); vec2 f = fract(p); f = f * f * (3.0 - 2.0 * f);
	return mix(mix(h21(i), h21(i + vec2(1.0, 0.0)), f.x), mix(h21(i + vec2(0.0, 1.0)), h21(i + vec2(1.0, 1.0)), f.x), f.y);
}
void fragment() {
	float u = UV.x;                 // 0 the inner edge, 1 the outer rim
	float v = UV.y;                 // 0 at the weapon (newest), 1 the tail
	// THE WASH: full toward the rim, soft toward the inner edge; along the stroke it thins toward the tail
	float body = smoothstep(0.02, body_u1, u) * pow(max(1.0 - v, 0.0), tail_pow);
	// dry-brush bristles: streaks that run ALONG the stroke (varying across it, stretched along it)
	float bristle = vnoise(vec2(u * 24.0, v * 2.5 + 3.1));
	float grain = vnoise(vec2(u * 70.0, v * 11.0 + 9.7));
	float a = body * mix(bristle_floor, 1.0, bristle) * mix(0.8, 1.0, grain);
	// THE RAMP under the scene's sun: two levels through one soft edge, the painting's blue-violet on the shade side
	vec3 n = normalize(NORMAL);
	if (!FRONT_FACING) { n = -n; }
	vec3 l = normalize((VIEW_MATRIX * vec4(sun_dir, 0.0)).xyz);
	float t = dot(n, l) * 0.5 + 0.5 + (grain - 0.5) * 0.12;
	vec3 col = mix(shade_color, wash_color, smoothstep(0.40, 0.60, t));
	// the two-tone stroke (T12_11b): a pale edge along the rim over the shade body, thinning with the stroke toward its tail
	if (edge_w > 0.0) {
		float e = smoothstep(1.0 - edge_w, 1.0 - edge_w * 0.35, u) * (1.0 - smoothstep(0.55, 1.0, v));
		col = mix(col, edge_color, e);
	}
	// THE PEN along the outer rim: the gear's ink, ~pen_px on screen, thinning and breaking toward the tail
	float fw = max(fwidth(u), 1e-5);
	float pen = 1.0 - smoothstep(0.0, pen_px * fw, 1.0 - u);
	pen *= (1.0 - smoothstep(0.35, 0.95, v)) * smoothstep(0.18, 0.34, bristle);
	col = mix(col, pen_color, pen);
	ALBEDO = col;
	ALPHA = clamp(max(a * alpha_max, pen * 0.85) * COLOR.a, 0.0, 1.0);
}
"""
	var knight
	var spec := {}
	var im := ImmediateMesh.new()
	var mat := ShaderMaterial.new()
	var samples := []            # [[clip pos, inner, outer], ...] oldest first, world space
	var clip := ""
	var last_pos := -1.0
	var fade_t := -1.0           # seconds since the window ended; -1 while drawing (or idle)
	var fade_s := 0.15
	var subdiv := 6
	var alpha := 0.0             # the whole trail's alpha now (measurement): 1 while drawing, then the fade
	var last_pts := []           # the strip as drawn last step: [[inner, outer, v], ...] (measurement)
	var _bones := {}
	var _pre := []               # the last tick BEFORE the window, [pos, inner, outer]: the window's start lies between it and the first tick inside
	var _closed := false         # the window's end has been written (the stroke is complete; only the fade remains)

	func setup(k, s: Dictionary) -> void:
		knight = k
		spec = s
		fade_s = float(s.get("fade_s", 0.15))
		subdiv = maxi(int(s.get("subdiv", 6)), 1)
		mesh = im
		top_level = true
		global_transform = Transform3D.IDENTITY
		cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		process_physics_priority = 1000          # after the AnimationTree's own physics-step update
		var sh := Shader.new()
		sh.code = SHADER
		mat.shader = sh
		material_override = mat
		var st: Dictionary = s.get("style", {})
		for p in ["wash_color", "shade_color", "pen_color", "edge_color"]:
			if st.has(p):
				mat.set_shader_parameter(p, Color(float(st[p][0]), float(st[p][1]), float(st[p][2])))
		for p in ["alpha_max", "pen_px", "bristle_floor", "edge_w", "body_u1", "tail_pow"]:
			if st.has(p):
				mat.set_shader_parameter(p, float(st[p]))
		# THE TRANSPARENT ORDER: the painted world's post pass paints its pre-transparent screen copy over the whole
		# frame (paint_stack.gd POST_PRIORITY 120); a transparent thing that must be SEEN draws after it (126, as the
		# snowfall does) -- at the default 0 the Barrow would paint the trail out
		mat.render_priority = int(st.get("render_priority", 0))
		mat.set_shader_parameter("sun_dir", _sun_dir())
		if k._mesh != null:
			layers = (k._mesh as VisualInstance3D).layers
		visible = false

	func _sun_dir() -> Vector3:
		# TOWARD the sun: the scene's first DirectionalLight3D (its light travels along -Z), else the Barrow's
		# winter sun -- elevation 55, azimuth 305 (the JOIN renderer's and the painting's)
		if is_inside_tree():
			var ls := get_tree().root.find_children("*", "DirectionalLight3D", true, false)
			if ls.size() > 0:
				return ((ls[0] as DirectionalLight3D).global_transform.basis.z).normalized()
		var e := deg_to_rad(55.0)
		var az := deg_to_rad(305.0)
		return Vector3(sin(az) * cos(e), sin(e), cos(az) * cos(e)).normalized()

	func _physics_process(dt: float) -> void:
		if knight != null and bool(knight.trail_auto):
			step(dt)

	func _edge(cs: Dictionary, i: int) -> Vector3:
		var sk: Skeleton3D = knight._skel
		var bn := String(cs["bone"])
		if not _bones.has(bn):
			_bones[bn] = sk.find_bone(bn)
		var p: Array = cs["edge"][i]
		return sk.global_transform * (sk.get_bone_global_pose(int(_bones[bn])) * Vector3(float(p[0]), float(p[1]), float(p[2])))

	func step(dt: float) -> void:
		# ITS OWN MATERIAL, every tick: the painted world re-materials every mesh under the knight from outside
		# (paint_stack.gd adopt_character swaps in the character ramp, restore/reapply swap back), which would
		# turn this stroke into an opaque ramp-lit ribbon
		if material_override != mat:
			material_override = mat
		var st: Dictionary = knight.trail_state()
		var clips: Dictionary = spec.get("clips", {})
		var running := not st.is_empty() and clips.has(String(st["clip"]))
		if running:
			var c := String(st["clip"])
			var pos: float = float(st["pos"])
			var cs: Dictionary = clips[c]
			var w: Array = cs["window"]
			if c != clip or pos < last_pos - 1e-4:
				samples.clear()                  # a new strike
				fade_t = -1.0
				clip = c
				_pre = []
				_closed = false
			var w0 := float(w[0])
			var w1 := float(w[1])
			# THE WINDOW EXACTLY: a physics tick rarely lands on the swing's first or last frame, so the stroke's two
			# ends are the edge line AT w0 and AT w1 -- each interpolated between the ticks either side of it
			if pos < w0 - 1e-4:
				_pre = [pos, _edge(cs, 0), _edge(cs, 1)]
			elif pos <= w1 + 1e-4:
				if samples.is_empty() or pos > last_pos + 1e-5:
					var cur := [pos, _edge(cs, 0), _edge(cs, 1)]
					if samples.is_empty() and not _pre.is_empty() and pos > w0 + 1e-4:
						samples.append(_lerp_sample(_pre, cur, w0))
					samples.append(cur)
			elif not samples.is_empty():
				if not _closed:
					var last: Array = samples[samples.size() - 1]
					if float(last[0]) < w1 - 1e-4:
						samples.append(_lerp_sample(last, [pos, _edge(cs, 0), _edge(cs, 1)], w1))
					_closed = true
				fade_t = pos - w1                # the fade, in the clip's own time while the strike runs
			last_pos = pos
		elif not samples.is_empty():
			fade_t = maxf(fade_t, 0.0) + dt      # the strike ended: the fade goes on in real time
			last_pos = -1.0
			clip = ""
		alpha = 1.0 if fade_t < 0.0 else 1.0 - smoothstep(0.0, fade_s, fade_t)
		if fade_t >= fade_s:
			samples.clear()
			fade_t = -1.0
			alpha = 0.0
		_draw()

	static func _lerp_sample(a: Array, b: Array, t: float) -> Array:
		var u: float = clampf((t - float(a[0])) / maxf(float(b[0]) - float(a[0]), 1e-6), 0.0, 1.0)
		return [t, (a[1] as Vector3).lerp(b[1], u), (a[2] as Vector3).lerp(b[2], u)]

	static func _cr(p0: Vector3, p1: Vector3, p2: Vector3, p3: Vector3, t: float) -> Vector3:
		var t2 := t * t
		var t3 := t2 * t
		return 0.5 * ((2.0 * p1) + (p2 - p0) * t + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * t2 + (3.0 * p1 - p0 - 3.0 * p2 + p3) * t3)

	func _draw() -> void:
		im.clear_surfaces()
		last_pts = []
		var n := samples.size()
		if n < 2 or alpha <= 0.001:
			visible = false
			return
		visible = true
		var pts := []
		for i in n - 1:
			var a0: Array = samples[maxi(i - 1, 0)]
			var a1: Array = samples[i]
			var a2: Array = samples[i + 1]
			var a3: Array = samples[mini(i + 2, n - 1)]
			for sidx in subdiv:
				var tt := float(sidx) / float(subdiv)
				pts.append([_cr(a0[1], a1[1], a2[1], a3[1], tt), _cr(a0[2], a1[2], a2[2], a3[2], tt)])
		pts.append([samples[n - 1][1], samples[n - 1][2]])
		var m := pts.size()
		im.surface_begin(Mesh.PRIMITIVE_TRIANGLE_STRIP)
		for j in m:
			var v := 1.0 - float(j) / float(m - 1)             # 0 at the weapon, 1 at the tail
			var inner: Vector3 = pts[j][0]
			var outer: Vector3 = pts[j][1]
			var inn: Vector3 = outer.lerp(inner, 1.0 - 0.55 * pow(v, 1.4))   # the stroke thins toward its tail
			var along: Vector3 = (pts[mini(j + 1, m - 1)][1] as Vector3) - (pts[maxi(j - 1, 0)][1] as Vector3)
			var nrm := (outer - inn).cross(along)
			nrm = nrm.normalized() if nrm.length() > 1e-9 else Vector3.UP
			var col := Color(1, 1, 1, alpha)
			im.surface_set_normal(nrm)
			im.surface_set_color(col)
			im.surface_set_uv(Vector2(0.0, v))
			im.surface_add_vertex(inn)
			im.surface_set_normal(nrm)
			im.surface_set_color(col)
			im.surface_set_uv(Vector2(1.0, v))
			im.surface_add_vertex(outer)
			last_pts.append([inn, outer, v])
		im.surface_end()
'''

REP = [
    ('''var _tree: AnimationTree
''', '''var _tree: AnimationTree
var _trail = null            # the StrikeTrail (T12_11), when character.json has strike_trail
var trail_auto := true       # the trail steps itself each physics frame; the lab tools turn this off and call trail_step
'''),
    ('''	_build_anim_tree()
	_add_foot_lock()
''', '''	_build_anim_tree()
	_add_foot_lock()
	_add_strike_trail()
'''),
]
for a, b in REP:
    n = s.count(a)
    if n != 1:
        sys.exit("REFUSED: anchor matched %d times: %r" % (n, a[:80]))
    s = s.replace(a, b)
if 'class StrikeTrail' in s:
    sys.exit("REFUSED: already patched")
s = s.rstrip('\n') + '\n' + FUNCS
open(dst, 'w').write(s)
print("patched %s -> %s" % (src, dst))
