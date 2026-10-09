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


func st_meta(st: String) -> Dictionary:
	return J.state(kit, st)


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


func advance(dt: float) -> void:
	clock_s += dt
	if a_state != "":
		frame_i = _frame_now()
	_show()


## The current (state, dir, frame) on the card: the strip's frame region, its foot anchor on the node's origin.
## A cell still decoding keeps the last frame shown.
func _show() -> void:
	if kit == "" or a_state == "":
		return
	var cid := "%s/%s" % [a_state, dir]
	var c := J.cell(kit, cid)
	if c.is_empty():
		return
	var tex := J.cell_tex(kit, cid)
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
	var m := Color(1, 1, 1, alpha_mult)
	if clock_s < flash_until_s:
		m = Color(1.8, 1.75, 1.6, alpha_mult)
	modulate = m
