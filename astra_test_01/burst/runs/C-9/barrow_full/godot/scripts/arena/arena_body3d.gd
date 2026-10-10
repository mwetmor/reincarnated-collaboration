extends Sprite3D
## C-9 BV2F ARENA (R-C9-348) -- ONE JOIN-1 BODY as a camera-facing billboard in the barrow_v2 scene.
##
## The clip clock is kc2_play/src/kc2p_body.gd's, ported line for line (loop / oneshot / hold / window, and the
## two-segment release warp: clip [0, r] -> [t_rel - L1, t_rel], [r, T] -> [t_rel, t_rel + L2], so the release frame
## lands on the oracle's tick). Only the drawing differs: the cell is shown on a Sprite3D (the strips are rendered at
## the barrow camera's pitch, so a screen-facing card reads right) with its foot anchor on the ground point.
## Size: one staged px = factor / (ppm_render * stage_scale) m -- the same metres KC2's 2D view draws it at.

const J = preload("res://scripts/arena/arena_art.gd")
const PRIORITY_MARKS := 121       # ground marks (paint_stack.gd: POST_PRIORITY 120 < these <= 127)
const PRIORITY_UNDER := 124
const PRIORITY_BODY := 125
const PRIORITY_OVER := 126

var kit: String = ""
var state_kit: Dictionary = {}      # R-C9-366: state -> a variant kit that carries it (gd-eor-warlord-eor4x)
var rate := 1.0                     # R-C9-366: the clip clock's speed (Haste plays his run at 1.3x)
var factor: float = 1.0
var ppm_render: float = 151.33680669505316
var stage_scale: float = 0.5
var dir: String = "S"
var clock_s: float = 0.0

var a_state: String = ""
var a_mode: String = ""             # "loop" | "release" | "oneshot" | "window" | "hold"
var a_t0: float = 0.0
var a_rel: float = 0.0
var a_L2: float = 0.0
var a_t1: float = 0.0
var a_pending: bool = false
var frame_i: int = 0
var flash_until_s: float = -1.0
const FLASH_WHITE := Color(1.8, 1.75, 1.6)
const FLASH_RED := Color(2.2, 0.35, 0.30)
var flash_col: Color = FLASH_WHITE
var alpha_mult: float = 1.0
var _shown: String = ""


func setup_body(kit_name: String, f: float) -> void:
	kit = kit_name
	factor = f
	var m := J.kit_meta(kit)
	ppm_render = float(m.get("ppm_render", 151.33680669505316))
	stage_scale = float(m.get("stage_scale", 0.5))
	billboard = BaseMaterial3D.BILLBOARD_ENABLED
	shaded = false
	double_sided = true
	centered = false
	region_enabled = true
	texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR
	alpha_cut = SpriteBase3D.ALPHA_CUT_DISABLED
	cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	pixel_size = factor / (ppm_render * stage_scale)
	# AFTER the barrow's paint post pass (paint_stack.gd POST_PRIORITY 120 reads the screen copied BEFORE the
	# transparent queue, so a transparent card drawn earlier is painted out): its AFTER_POST band, as the snowfall
	render_priority = PRIORITY_BODY


func _k(st: String) -> String:
	return String(state_kit.get(st, kit))


func st_meta(st: String) -> Dictionary:
	return J.state(_k(st), st)


func clip_T(st: String) -> float:
	return float(st_meta(st).get("duration_s", 1.0))


func rel_s(st: String) -> float:
	var r: Variant = st_meta(st).get("release_s", null)
	return float(r) if r != null else 0.0


func play_loop(st: String) -> void:
	if a_mode == "loop" and a_state == st:
		return
	a_state = st
	a_mode = "loop"
	a_t0 = clock_s


func play_oneshot(st: String, hold: bool = false) -> void:
	a_state = st
	a_mode = "hold" if hold else "oneshot"
	a_t0 = clock_s


func begin_windup(st: String, t_until_s: float, after_s: float) -> void:
	var r := rel_s(st)
	a_state = st
	a_mode = "release"
	a_rel = clock_s + maxf(0.0, t_until_s)
	a_t0 = a_rel - minf(r, maxf(0.0, t_until_s))
	a_L2 = maxf(0.05, after_s)
	a_pending = true


func release_now(st: String, after_s: float) -> void:
	if a_mode == "release" and a_state == st and a_pending:
		a_rel = clock_s
		a_t0 = minf(a_t0, a_rel)
	else:
		a_state = st
		a_mode = "release"
		a_t0 = clock_s
		a_rel = clock_s
	a_L2 = maxf(0.05, after_s)
	a_pending = false


func windup_overdue(grace_s: float) -> bool:
	return a_mode == "release" and a_pending and clock_s > a_rel + grace_s


func abandon_windup() -> void:
	a_pending = false
	a_mode = ""


func play_window(st: String, t0_view: float, t1_view: float) -> void:
	a_state = st
	a_mode = "window"
	a_t0 = t0_view
	a_t1 = maxf(t0_view + 0.01, t1_view)


func busy() -> bool:
	match a_mode:
		"release":
			return clock_s < a_rel + a_L2 or a_pending
		"oneshot":
			return clock_s < a_t0 + clip_T(a_state)
		"window":
			return clock_s < a_t1
		"hold":
			return true
	return false


func _clip_time() -> float:
	var T := clip_T(a_state)
	match a_mode:
		"loop":
			return fposmod(clock_s - a_t0, T)
		"oneshot", "hold":
			return clampf(clock_s - a_t0, 0.0, T)
		"window":
			return clampf((clock_s - a_t0) / (a_t1 - a_t0), 0.0, 1.0) * T
		"release":
			var r := rel_s(a_state)
			if clock_s <= a_rel:
				var L1 := a_rel - a_t0
				if clock_s < a_t0:
					return 0.0
				return r if L1 <= 1e-6 else clampf((clock_s - a_t0) / L1, 0.0, 1.0) * r
			return r + clampf((clock_s - a_rel) / a_L2, 0.0, 1.0) * (T - r)
	return 0.0


func loop_rev() -> int:
	if a_mode != "loop":
		return 0
	return int(floor((clock_s - a_t0) / clip_T(a_state)))


func _frame_now() -> int:
	var t_s: Array = st_meta(a_state).get("t_s", [])
	if t_s.is_empty():
		return 0
	var c := _clip_time()
	if a_mode == "loop":
		return clampi(int(floor(c / clip_T(a_state) * float(t_s.size()))), 0, t_s.size() - 1)
	return J.frame_at(t_s, c + 1e-6)


func flash() -> void:
	flash_until_s = clock_s + 0.16
	flash_col = FLASH_WHITE


## R-C9-361: the warlord's red flash when he takes damage
func flash_red() -> void:
	flash_until_s = clock_s + 0.18
	flash_col = FLASH_RED


func advance(dt: float) -> void:
	clock_s += dt * rate
	if a_state != "":
		frame_i = _frame_now()
	_show()


## The current (state, dir, frame) on the card: the strip's frame region, its foot anchor on the node's origin.
## A cell still decoding keeps the last frame shown.
func _show() -> void:
	if kit == "" or a_state == "":
		return
	var cid := "%s/%s" % [a_state, dir]
	var c := J.cell(_k(a_state), cid)
	if c.is_empty():
		return
	var tex := J.cell_tex(_k(a_state), cid)
	if tex == null:
		return
	var n := int(c["n"])
	var fi := clampi(frame_i, 0, n - 1)
	var cols := int(c["cols"])
	var fw := float(c["fw"])
	var fh := float(c["fh"])
	var anc: Array = c["anchor_px"]
	texture = tex
	region_rect = Rect2(float(fi % cols) * fw, float(fi / cols) * fh, fw, fh)
	# Sprite3D, centered = false: the frame's BOTTOM-left sits at `offset` (y up). Foot anchor (ax, ay from the
	# frame's top-left) on the origin: offset = (-ax, ay - fh).
	offset = Vector2(-float(anc[0]), float(anc[1]) - fh)
	_cast_shadow(tex, float(anc[0]), float(anc[1]), fw, fh)
	var m := Color(1, 1, 1, alpha_mult)
	if clock_s < flash_until_s:
		m = Color(flash_col.r, flash_col.g, flash_col.b, alpha_mult)
	modulate = m



# =====================================================================================================================
# R-C9-375 THE CAST SHADOW (Matt: "shadows under the monsters but not the player ... not set to the same angle as the
# rest of the scene"). Every body -- monster and warlord -- lays ITS OWN SILHOUETTE (the frame on the card, this frame)
# on the ground ALONG THE SCENE'S SUN: the same DirectionalLight3D that casts the props' shadows on the snow
# (barrow_full.gd's `sun`; bv2f_pilot.gd's PaintSun is its duplicate, same transform). arena_mode sets sun_dir from it.
#   direction  the sun's ground bearing; length  height / tan(sun elevation); the card's px are screen metres, so a
#              height is px x pixel_size / cos(camera pitch)
#   softness   a blur that widens from the feet out (contact-hard, as the scene's PCF-blurred cast shadows)
#   darkness   SHADOW_TINT, a multiply measured off the props' own cast shadows on this snow (captures/shadows/)
# A multiply-blended ground quad after the paint post (priority 121) on the TRUE ground under the card (depth-tested:
# props in front occlude it), slid SHADOW_LIFT_TOWARD_CAM_M toward the camera. Off with `-- --arena-shadow off`.
# =====================================================================================================================
static var sun_dir := Vector3(-0.5, -0.6, -0.5)   # light travel direction (world), set by arena_mode from scene.sun
static var cam_pitch_deg := 52.95354
## COLOUR measured off a standing stone's own cast shadow on this snow (captures/shadows/): sRGB ratio shadow/lit
## (0.956, 0.920, 0.897), hue (1, 0.962, 0.938). DARKNESS: that prop shadow is a ~6 % darkening, which on a body's
## small footprint does not read at all (stills: invisible) -- so the value is the monsters' blob Matt saw (22 % black,
## sRGB 0.78) on the props' hue: sRGB (0.78, 0.75, 0.73) -> LINEAR (the blend runs in linear) ^2.2. Knob:
## `-- --arena-shadow-tint r,g,b` (linear).
static var shadow_tint := Color(0.579, 0.531, 0.500)
static var card_slide := Vector3.ZERO     # the cards' slide toward the camera (arena_mode); the shadow lies on the TRUE ground
const SHADOW_LIFT_TOWARD_CAM_M := 0.35    # a short slide only: props in front still occlude it, the snow's relief doesn't cut it
static var shadows_on := true
static var _shadow_shader: Shader = null
const SHADOW_SHADER := """
shader_type spatial;
render_mode unshaded, blend_mul, cull_disabled, depth_draw_never, shadows_disabled, fog_disabled;
uniform sampler2D tex : filter_linear, repeat_disable;
uniform vec4 region;          // the frame's uv rect in the strip
uniform vec2 frame_px;
uniform vec3 tint;
uniform float strength = 1.0;
uniform float blur_px = 7.0;
float a_at(vec2 p) {
	if (p.x < 0.0 || p.y < 0.0 || p.x > frame_px.x || p.y > frame_px.y) { return 0.0; }
	return texture(tex, region.xy + p / frame_px * region.zw).a;
}
void fragment() {
	// UV.y 0 at the frame's bottom (the feet end), 1 at its top
	vec2 p = vec2(UV.x, 1.0 - UV.y) * frame_px;
	float r = mix(1.0, blur_px, UV.y);
	float a = a_at(p) * 0.28;
	for (int i = 0; i < 8; i++) {
		float an = 6.2831853 * float(i) / 8.0;
		a += a_at(p + vec2(cos(an), sin(an)) * r) * 0.09;
	}
	vec3 c = mix(vec3(1.0), tint, clamp(a * strength, 0.0, 1.0));
	ALBEDO = c;
}
"""
var _shadow_mi: MeshInstance3D = null
var _shadow_sm: ShaderMaterial = null


func _cast_shadow(tex: Texture2D, ax: float, ay: float, fw: float, fh: float) -> void:
	if not shadows_on:
		return
	if _shadow_mi == null:
		if _shadow_shader == null:
			_shadow_shader = Shader.new()
			_shadow_shader.code = SHADOW_SHADER
		_shadow_sm = ShaderMaterial.new()
		_shadow_sm.shader = _shadow_shader
		_shadow_sm.render_priority = PRIORITY_MARKS
		var am := ArrayMesh.new()
		var arr := []
		arr.resize(Mesh.ARRAY_MAX)
		arr[Mesh.ARRAY_VERTEX] = PackedVector3Array([Vector3(0, 0, 0), Vector3(1, 0, 0), Vector3(1, 1, 0), Vector3(0, 1, 0)])
		arr[Mesh.ARRAY_TEX_UV] = PackedVector2Array([Vector2(0, 0), Vector2(1, 0), Vector2(1, 1), Vector2(0, 1)])
		arr[Mesh.ARRAY_INDEX] = PackedInt32Array([0, 1, 2, 0, 2, 3])
		am.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
		_shadow_mi = MeshInstance3D.new()
		_shadow_mi.name = "CastShadow"
		_shadow_mi.mesh = am
		_shadow_mi.material_override = _shadow_sm
		_shadow_mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		_shadow_mi.top_level = true
		_shadow_mi.custom_aabb = AABB(Vector3(-50, -50, -50), Vector3(100, 100, 100))
		add_child(_shadow_mi)
	var cam := get_viewport().get_camera_3d()
	if cam == null:
		return
	var ps := pixel_size
	var right := cam.global_transform.basis.x
	right.y = 0.0
	right = right.normalized()
	var d := sun_dir.normalized()
	var g := Vector3(d.x, 0.0, d.z)
	var elev := asin(clampf(-d.y, 0.05, 1.0))
	var l_per_m := 1.0 / tan(elev)
	var h_k := 1.0 / cos(deg_to_rad(cam_pitch_deg))     # screen px -> true height
	g = g.normalized() * l_per_m * h_k
	var feet := global_position - card_slide - cam.global_transform.basis.z.normalized() * -SHADOW_LIFT_TOWARD_CAM_M
	# the card's width laid ACROSS the sun's bearing (a body has depth as well as width; a flat card edge-on to
	#   the sun would cast a line)
	var across := Vector3(-g.z, 0.0, g.x).normalized()
	if across.dot(right) < 0.0:
		across = -across
	right = across
	var bx := right * (fw * ps)
	var by := g * (fh * ps)
	var origin := feet - right * (ax * ps) + g * ((ay - fh) * ps)
	_shadow_mi.global_transform = Transform3D(Basis(bx, by, Vector3.UP * 0.01), origin)
	var ts := Vector2(tex.get_width(), tex.get_height())
	var rr := region_rect
	_shadow_sm.set_shader_parameter("tex", tex)
	_shadow_sm.set_shader_parameter("region", Vector4(rr.position.x / ts.x, rr.position.y / ts.y, rr.size.x / ts.x, rr.size.y / ts.y))
	_shadow_sm.set_shader_parameter("frame_px", Vector2(fw, fh))
	_shadow_sm.set_shader_parameter("tint", Vector3(shadow_tint.r, shadow_tint.g, shadow_tint.b))
	_shadow_sm.set_shader_parameter("strength", alpha_mult * (1.0 if visible else 0.0))
	_shadow_mi.visible = visible and alpha_mult > 0.01
