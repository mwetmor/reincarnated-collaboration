extends Node3D
## C-9 BV2F ARENA (R-C9-367) -- DAMAGE NUMBERS, the NUM-POP style Matt accepted (reincarnated-godot
## scripts/wr2_playback.gd `_float_number` @ 978a423, 2026-08-02, the version that rendered his ice-golem clip; ported
## here, that file is not edited): the Bangers display face (read in place, OFL) emboldened 0.08, a black rim at 0.20 of
## the size, the em at 8.5 % of the frame height, POP 0.35 -> 1.15 (0.022 s) -> 1.0 (0.038 s), alpha in 0.045 s, held
## 0.42 s, out over 0.72 s, an ease-out rise of 2.1 m over 1.18 s. Colour = the hit's ELEMENT (wr2's ELEMENT_COLORS: the
## clip's purple numbers are CHAOS hits, the cream ones PHYSICAL); a crit is red. Only damage the warlord DEALS is shown.
## Pooled: POOL labels, reused oldest-first; past MAX_LIVE the hit is not shown (cheap by construction).

const Paths = preload("res://scripts/arena/arena_paths.gd")
static var FONT_PATH: String = Paths.font()
const EM_FRAC := 0.085 * 0.8    # NUM_EM_FRAC_DEALT x 0.8 (R-C9-368, Matt: "a bit smaller")
const PIXEL_SIZE := 0.012
const OUTLINE_RATIO := 0.20
const EMBOLDEN := 0.08
const POP_IN := 0.35
const POP_PEAK := 1.15
const POP_T_UP := 0.022
const POP_T_SETTLE := 0.038
const ALPHA_IN := 0.045
const HOLD := 0.42
const FADE := 0.72
const RISE_M := 2.1
const RISE_T := 1.18
const POOL := 40
const MAX_LIVE := 28
const MIN_SHOWN := 1.0          # hits under this many points are not drawn (the channel's tick crumbs)
const COL_CRIT := Color(1.00, 0.12, 0.10)
const ELEMENT_COLORS := {
	"cold": Color(0.70, 0.90, 1.00), "chaos": Color(0.72, 0.45, 0.95), "physical": Color(0.88, 0.88, 0.88),
	"fire": Color(1.00, 0.45, 0.20), "lightning": Color(0.95, 0.90, 0.35), "poison": Color(0.55, 0.85, 0.25)}
## R-C9-368 (Matt: "the basic damage numbers changed from white to red"): the basic (physical) number is a strong red
## that reads on snow under the black rim; the element colours (purple chaos ...) stay as ported
const COL_BASIC := Color(0.93, 0.10, 0.08)

var cam: Camera3D = null
var _pool: Array = []           # [{lbl, t0, start, col, live}]
var _next := 0
var _font: FontVariation = null
var n_shown := 0
var _by_key: Dictionary = {}
const MERGE_S := 0.25
const JITTER_M := 0.35
var n_dropped := 0


func setup(c: Camera3D) -> void:
	cam = c
	var ff := FontFile.new()
	var fb := Paths.bytes(FONT_PATH)
	ff.data = fb
	if fb.size() > 0:
		_font = FontVariation.new()
		_font.base_font = ff
		_font.variation_embolden = EMBOLDEN
	else:
		push_warning("[arena] NUM-POP font not found at %s: the project font is used" % FONT_PATH)
	for i in POOL:
		var l := Label3D.new()
		l.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		l.no_depth_test = true
		l.pixel_size = PIXEL_SIZE
		l.render_priority = 127
		l.outline_render_priority = 126
		l.outline_modulate = Color(0, 0, 0, 1)
		if _font != null:
			l.font = _font
		l.visible = false
		add_child(l)
		_pool.append({"lbl": l, "t0": 0.0, "start": Vector3.ZERO, "col": Color.WHITE, "live": false})


func _live() -> int:
	var n := 0
	for p in _pool:
		n += int(p["live"])
	return n


## `key` (the body hit): hits on one body within MERGE_S of its number's spawn ADD to that number (the channel's
## 12.25 Hz ticks read as ~4 numbers a second per body, not a stack of overlapping labels); then a fresh number pops.
func show_hit(at: Vector3, amount: float, element: String, crit: bool, key: int = -1) -> void:
	if amount <= 0.0 or cam == null:
		return
	var now := Time.get_ticks_msec() / 1000.0
	if key >= 0 and _by_key.has(key):
		var q: Dictionary = _by_key[key]
		if q["live"] and int(q.get("key", -2)) == key and now - float(q["t0"]) < MERGE_S and not crit:
			q["sum"] = float(q["sum"]) + amount
			(q["lbl"] as Label3D).text = _fmt(float(q["sum"]))
			return
	if amount < MIN_SHOWN:
		return
	if _live() >= MAX_LIVE:
		n_dropped += 1
		return
	var p: Dictionary = _pool[_next]
	_next = (_next + 1) % POOL
	var l: Label3D = p["lbl"]
	l.text = _fmt(amount)
	# the em at EM_FRAC of the frame: ortho, so px per metre = frame rows / cam.size
	var fs := int(round(EM_FRAC * cam.size / PIXEL_SIZE))
	l.font_size = clampi(fs, 16, 512)
	l.outline_size = maxi(2, int(round(float(l.font_size) * OUTLINE_RATIO)))
	var el := element.to_lower()
	var col: Color = COL_CRIT if crit else (COL_BASIC if el == "physical" or not ELEMENT_COLORS.has(el) else ELEMENT_COLORS[el])
	p["col"] = col
	p["t0"] = Time.get_ticks_msec() / 1000.0
	p["start"] = at + Vector3(0, 1.6, 0)
	p["live"] = true
	p["sum"] = amount
	p["key"] = key
	if key >= 0:
		_by_key[key] = p
	p["start"] = (p["start"] as Vector3) + Vector3(randf_range(-JITTER_M, JITTER_M), 0, 0)
	l.position = p["start"]
	l.scale = Vector3.ONE * POP_IN
	l.modulate = Color(col.r, col.g, col.b, 0.0)
	l.outline_modulate = Color(0, 0, 0, 0.0)
	l.visible = true
	n_shown += 1


func _process(_dt: float) -> void:
	var now := Time.get_ticks_msec() / 1000.0
	for p in _pool:
		if not p["live"]:
			continue
		var t: float = now - float(p["t0"])
		var l: Label3D = p["lbl"]
		var a: float
		if t < ALPHA_IN:
			a = t / ALPHA_IN
		elif t < ALPHA_IN + HOLD:
			a = 1.0
		else:
			a = 1.0 - clampf((t - ALPHA_IN - HOLD) / FADE, 0.0, 1.0)
			a = a * a                                       # EASE_IN on the fade
		var s: float
		if t < POP_T_UP:
			s = lerpf(POP_IN, POP_PEAK, _ease_out_quad(t / POP_T_UP))
		elif t < POP_T_UP + POP_T_SETTLE:
			s = lerpf(POP_PEAK, 1.0, _ease_out_back((t - POP_T_UP) / POP_T_SETTLE))
		else:
			s = 1.0
		var r := _ease_out_quad(clampf(t / RISE_T, 0.0, 1.0))
		l.position = (p["start"] as Vector3) + Vector3(0, RISE_M * r, 0)
		l.scale = Vector3.ONE * s
		var c: Color = p["col"]
		l.modulate = Color(c.r, c.g, c.b, a)
		l.outline_modulate = Color(0, 0, 0, a)
		if t >= RISE_T and t >= ALPHA_IN + HOLD + FADE:
			p["live"] = false
			l.visible = false


static func _ease_out_quad(x: float) -> float:
	return 1.0 - (1.0 - x) * (1.0 - x)


static func _ease_out_back(x: float) -> float:
	var c1 := 1.70158
	var c3 := c1 + 1.0
	return 1.0 + c3 * pow(x - 1.0, 3) + c1 * pow(x - 1.0, 2)


static func _fmt(v: float) -> String:
	var n := int(round(v))
	var s := str(absi(n))
	var out := ""
	var c := 0
	for i in range(s.length() - 1, -1, -1):
		out = s[i] + out
		c += 1
		if c % 3 == 0 and i > 0:
			out = "," + out
	return out
