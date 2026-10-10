extends CanvasLayer
## C-9 BV2F ARENA (R-C9-391) -- THE TOUCH LAYER. One build for PC and phone: hidden until the FIRST touch arrives,
## then shown for the session; the mouse and keyboard keep working throughout (a real mouse moving puts the cursor back).
##
##   on the field   a finger HELD (> HOLD_S, or dragged > DRAG_PX) is the hold-LMB move: he walks to it, following it;
##                  a quick TAP (released inside both) is the left click: the slash on an enemy in reach, else Charge
##   WHIRLWIND      held = the right button held (the channel)
##   1 2 3 4        Potion, Might, Battle Cry, Haste -- aimed where the last finger pointed
##   Z              zoom
## Touches on a button never reach the field. Emulated mouse events from touch are switched off while it is up, so a
## tap is not also a click.

const HOLD_S := 0.20
const DRAG_PX := 22.0
const BTN_R := 58.0
const BUTTONS := [
	{"id": "channel", "label": "WHIRL", "at": Vector2(-120, -150), "r": 1.35},
	{"id": "potion", "label": "1", "at": Vector2(-290, -80), "r": 0.8},
	{"id": "vires_might", "label": "2", "at": Vector2(-270, -230), "r": 0.8},
	{"id": "war_cry", "label": "3", "at": Vector2(-180, -330), "r": 0.8},
	{"id": "rune_of_rush", "label": "4", "at": Vector2(-60, -330), "r": 0.8},
	{"id": "zoom", "label": "Z", "at": Vector2(-60, -470), "r": 0.6},
]
const SUBLABEL := {"channel": "Whirlwind", "potion": "Potion", "vires_might": "Might", "war_cry": "Battle Cry",
	"rune_of_rush": "Haste", "zoom": "zoom"}

var mode = null                       # arena_mode.gd
var shown := false
var _field := {}                      # touch index -> {start, t0, pos, moving}
var _btn_touch := {}                  # touch index -> button id
var _draw: Control = null
var _font: Font = null
var _clock := 0.0


func setup(p_mode) -> void:
	mode = p_mode
	layer = 7
	_draw = Control.new()
	_draw.set_anchors_preset(Control.PRESET_FULL_RECT)
	_draw.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_draw.draw.connect(_on_draw)
	add_child(_draw)
	_font = ThemeDB.fallback_font
	visible = false


func _show() -> void:
	if shown:
		return
	shown = true
	visible = true
	mode.touch_on = true
	Input.emulate_mouse_from_touch = false


func _scr() -> Vector2:
	return get_viewport().get_visible_rect().size


func _ui_k() -> float:
	return clampf(_scr().y / 1080.0, 0.55, 1.6) * 1.15


func _btn_pos(b: Dictionary) -> Vector2:
	var k := _ui_k()
	return _scr() + Vector2(b["at"]) * k


func _btn_at(p: Vector2) -> String:
	var k := _ui_k()
	for b in BUTTONS:
		if p.distance_to(_btn_pos(b)) <= BTN_R * float(b["r"]) * k:
			return String(b["id"])
	return ""


func _input(e: InputEvent) -> void:
	if e is InputEventScreenTouch:
		var t := e as InputEventScreenTouch
		_show()
		if t.pressed:
			var bid := _btn_at(t.position)
			if bid != "":
				_btn_touch[t.index] = bid
				_btn_down(bid)
			else:
				_field[t.index] = {"start": t.position, "t0": _clock, "pos": t.position, "moving": false}
			get_viewport().set_input_as_handled()
		else:
			if _btn_touch.has(t.index):
				_btn_up(String(_btn_touch[t.index]))
				_btn_touch.erase(t.index)
			elif _field.has(t.index):
				var f: Dictionary = _field[t.index]
				_field.erase(t.index)
				if not bool(f["moving"]):
					mode.touch_tap(t.position)
				if _field.is_empty():
					mode.touch_move = null
			get_viewport().set_input_as_handled()
		_draw.queue_redraw()
	elif e is InputEventScreenDrag:
		var d := e as InputEventScreenDrag
		if _field.has(d.index):
			var f: Dictionary = _field[d.index]
			f["pos"] = d.position
			if not bool(f["moving"]) and d.position.distance_to(f["start"]) > DRAG_PX:
				f["moving"] = true
				mode.touch_start()
			get_viewport().set_input_as_handled()
	elif e is InputEventMouseMotion and shown and not (e as InputEventMouseMotion).relative.is_zero_approx():
		mode.touch_pointer = null              # a real mouse: it is the cursor again


func _process(dt: float) -> void:
	_clock += dt
	if not shown:
		return
	var mover = null
	for k in _field.keys():
		var f: Dictionary = _field[k]
		if not bool(f["moving"]) and _clock - float(f["t0"]) > HOLD_S:
			f["moving"] = true
			mode.touch_start()
		if bool(f["moving"]):
			mover = f["pos"]
	mode.touch_move = mover
	_draw.queue_redraw()


func _btn_down(bid: String) -> void:
	if bid == "channel":
		mode.touch_start()
		mode.touch_channel = true
	else:
		mode.touch_skill(bid)


func _btn_up(bid: String) -> void:
	if bid == "channel":
		mode.touch_channel = false


func _on_draw() -> void:
	var k := _ui_k()
	var held := {}
	for v in _btn_touch.values():
		held[String(v)] = true
	for b in BUTTONS:
		var c := _btn_pos(b)
		var r := BTN_R * float(b["r"]) * k
		var on: bool = held.has(String(b["id"])) or (String(b["id"]) == "channel" and bool(mode.touch_channel))
		_draw.draw_circle(c, r, Color(0.08, 0.07, 0.07, 0.62 if not on else 0.82))
		_draw.draw_arc(c, r, 0.0, TAU, 48, Color(0.95, 0.82, 0.55, 0.9 if on else 0.55), 3.0 * k)
		var fs := int(26.0 * k * float(b["r"]))
		var lab := String(b["label"])
		var sz := _font.get_string_size(lab, HORIZONTAL_ALIGNMENT_CENTER, -1, fs)
		_draw.draw_string(_font, c + Vector2(-sz.x * 0.5, fs * 0.35), lab, HORIZONTAL_ALIGNMENT_CENTER, -1, fs,
			Color(1, 0.94, 0.82))
		var sub := String(SUBLABEL.get(String(b["id"]), ""))
		var fs2 := int(13.0 * k)
		var s2 := _font.get_string_size(sub, HORIZONTAL_ALIGNMENT_CENTER, -1, fs2)
		_draw.draw_string(_font, c + Vector2(-s2.x * 0.5, r + fs2 + 2.0), sub, HORIZONTAL_ALIGNMENT_CENTER, -1, fs2,
			Color(1, 0.94, 0.82, 0.85))
	# the move finger
	if mode.touch_move != null:
		_draw.draw_circle(Vector2(mode.touch_move), 22.0 * k, Color(1, 1, 1, 0.18))
		_draw.draw_arc(Vector2(mode.touch_move), 22.0 * k, 0.0, TAU, 32, Color(1, 1, 1, 0.6), 2.0 * k)
