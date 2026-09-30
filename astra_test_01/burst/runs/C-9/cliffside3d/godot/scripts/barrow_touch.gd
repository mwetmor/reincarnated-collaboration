extends CanvasLayer
## The Barrow's touch controls, for the phone build (/playtest/barrow/, R-C9-83). drax.
##
## Added by barrow_world at _ready on the web or on any touchscreen, and hidden until a touch
## arrives, a touchscreen is detected, or the page carries ?touch=1. Everything goes through
## the INPUT ACTIONS knight.gd already reads -- nothing in knight.gd is touched, and the
## keyboard and mouse keep working beside it:
##   left half   a floating thumb stick -> move_left/right/up/down at analog strength, and
##               run_modifier while it is pushed past 60%
##   right side  SLASH (attack), CHOP (attack_chop), BASH (shield_bash), BLOCK (block, held)
##   top right   GEAR (gear_cycle) -- the desktop's G. The phone build starts him in the full
##               kit (barrow_world), because chop, bash and block need the axe and the shield
##
## Adapted from the cliffside playtest overlay (reincarnated-godot/web/_overlay/
## touch_controls.gd): the same two press mechanisms, because a consumer that polls
## Input.is_action_* and one that listens for events see different things --
## Input.action_press serves the first, Input.parse_input_event the second.
##
## Canvas coordinates are the project's 1920x1080 base: [display] stretches canvas items to the
## window (keep aspect), so a phone's landscape screen maps onto this same layout.

const JOY_RADIUS := 150.0
const RUN_THRESHOLD := 0.6
const BUTTONS := [
	{"actions": ["attack"], "label": "SLASH", "anchor": Vector2(-205, -225), "radius": 112.0},
	{"actions": ["attack_chop"], "label": "CHOP", "anchor": Vector2(-445, -150), "radius": 88.0},
	{"actions": ["shield_bash"], "label": "BASH", "anchor": Vector2(-195, -480), "radius": 84.0},
	{"actions": ["block"], "label": "BLOCK", "anchor": Vector2(-430, -385), "radius": 88.0, "hold": true},
	{"actions": ["gear_cycle"], "label": "GEAR", "anchor": Vector2(-120, -960), "radius": 64.0},
]

var _overlay: Control
var _joy_index: int = -1
var _joy_origin := Vector2.ZERO
var _joy_knob := Vector2.ZERO
var _button_touch: Dictionary = {}
var _buttons: Array = []
var _joy_run := false
var _font: Font
var _fps_log := false
var _fps_t := 0.0


func _ready() -> void:
	layer = 20
	process_mode = Node.PROCESS_MODE_ALWAYS
	for button in BUTTONS:
		var live: Array = []
		for action in button.actions:
			if InputMap.has_action(action):
				live.append(action)
		if not live.is_empty():
			var copy: Dictionary = button.duplicate(true)
			copy["actions"] = live
			_buttons.append(copy)
	_overlay = Control.new()
	_overlay.name = "TouchOverlay"
	_overlay.set_anchors_preset(Control.PRESET_FULL_RECT)
	_overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_overlay.draw.connect(_draw_overlay)
	add_child(_overlay)
	_font = ThemeDB.fallback_font
	_set_shown(DisplayServer.is_touchscreen_available() or _query_has("touch=1"))
	# the frame rate, to the browser console, for the phone-size measurement (?fps=1)
	_fps_log = _query_has("fps=1")
	print("[touch] %d buttons; shown=%s" % [_buttons.size(), str(_overlay.visible)])


func _query_has(token: String) -> bool:
	if not OS.has_feature("web"):
		return false
	var search: Variant = JavaScriptBridge.eval("window.location.search", true)
	return typeof(search) == TYPE_STRING and String(search).contains(token)


func _set_shown(on: bool) -> void:
	_overlay.visible = on
	# the key-hint bar is for a keyboard; with the thumb controls up it is clutter
	var scene := get_parent()
	if on and scene != null and scene.has_method("set_hud_visible"):
		scene.set_hud_visible(false)


func _process(dt: float) -> void:
	if _fps_log:
		_fps_t += dt
		if _fps_t >= 2.0:
			_fps_t = 0.0
			print("[fps] %d" % Engine.get_frames_per_second())


func _screen_size() -> Vector2:
	return _overlay.get_rect().size


func _button_center(button: Dictionary) -> Vector2:
	return _screen_size() + button.anchor


func _input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:
		if not _overlay.visible:
			_set_shown(true)
		if event.pressed:
			_touch_down(event.index, event.position)
		else:
			_touch_up(event.index)
		get_viewport().set_input_as_handled()
	elif event is InputEventScreenDrag:
		if event.index == _joy_index:
			_update_joystick(event.position)
			get_viewport().set_input_as_handled()


func _touch_down(index: int, pos: Vector2) -> void:
	for button in _buttons:
		if pos.distance_to(_button_center(button)) <= button.radius * 1.15:
			_button_touch[index] = button.label
			for action in button.actions:
				_press(action, true)
			_overlay.queue_redraw()
			return
	if pos.x < _screen_size().x * 0.5 and _joy_index == -1:
		_joy_index = index
		_joy_origin = pos
		_update_joystick(pos)


func _button_by_label(label: String) -> Dictionary:
	for button in _buttons:
		if button.label == label:
			return button
	return {}


func _press(action: String, pressed: bool) -> void:
	if pressed:
		Input.action_press(action)
	else:
		Input.action_release(action)
	var ev := InputEventAction.new()
	ev.action = action
	ev.pressed = pressed
	Input.parse_input_event(ev)


func _touch_up(index: int) -> void:
	if _button_touch.has(index):
		var button := _button_by_label(_button_touch[index])
		_button_touch.erase(index)
		for action in button.get("actions", []):
			_press(action, false)
		_overlay.queue_redraw()
	if index == _joy_index:
		_joy_index = -1
		_set_move(Vector2.ZERO)
		_overlay.queue_redraw()


func _update_joystick(pos: Vector2) -> void:
	var offset := pos - _joy_origin
	if offset.length() > JOY_RADIUS:
		offset = offset.normalized() * JOY_RADIUS
	_joy_knob = _joy_origin + offset
	_set_move(offset / JOY_RADIUS)
	_overlay.queue_redraw()


func _set_move(v: Vector2) -> void:
	_set_strength("move_right", maxf(v.x, 0.0))
	_set_strength("move_left", maxf(-v.x, 0.0))
	_set_strength("move_down", maxf(v.y, 0.0))
	_set_strength("move_up", maxf(-v.y, 0.0))
	_joy_run = v.length() > RUN_THRESHOLD
	if _joy_run:
		Input.action_press("run_modifier")
	else:
		Input.action_release("run_modifier")


func _set_strength(action: String, strength: float) -> void:
	if strength > 0.0:
		Input.action_press(action, strength)
	else:
		Input.action_release(action)


func _release_all() -> void:
	for index in _button_touch.keys():
		var button := _button_by_label(_button_touch[index])
		for action in button.get("actions", []):
			_press(action, false)
	_button_touch.clear()
	_joy_index = -1
	_set_move(Vector2.ZERO)
	_overlay.queue_redraw()


func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT or what == NOTIFICATION_WM_WINDOW_FOCUS_OUT:
		_release_all()


func _draw_overlay() -> void:
	var size := _screen_size()
	if _joy_index == -1:
		var hint := Vector2(270, size.y - 255)
		_overlay.draw_circle(hint, JOY_RADIUS, Color(1, 1, 1, 0.08))
		_overlay.draw_arc(hint, JOY_RADIUS, 0, TAU, 64, Color(1, 1, 1, 0.35), 4.0, true)
		_overlay.draw_circle(hint, 58, Color(1, 1, 1, 0.22))
		_draw_label(hint + Vector2(0, JOY_RADIUS + 40), "MOVE", 28)
	else:
		_overlay.draw_circle(_joy_origin, JOY_RADIUS, Color(1, 1, 1, 0.12))
		_overlay.draw_arc(_joy_origin, JOY_RADIUS, 0, TAU, 64, Color(1, 1, 1, 0.45), 4.0, true)
		_overlay.draw_arc(_joy_origin, JOY_RADIUS * RUN_THRESHOLD, 0, TAU, 48, Color(1, 1, 1, 0.18), 2.0, true)
		_overlay.draw_circle(_joy_knob, 58, Color(1, 1, 1, 0.45))
	for button in _buttons:
		var center := _button_center(button)
		var held: bool = _button_touch.values().has(button.label)
		_overlay.draw_circle(center, button.radius,
			Color(0.55, 0.8, 1.0, 0.42) if held else Color(0.05, 0.08, 0.12, 0.38))
		_overlay.draw_arc(center, button.radius, 0, TAU, 64, Color(1, 1, 1, 0.6), 4.0, true)
		_draw_label(center, button.label, 34 if button.radius > 100.0 else 28)


func _draw_label(center: Vector2, text: String, font_size: int) -> void:
	var text_size := _font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size)
	var baseline := center + Vector2(-text_size.x * 0.5, text_size.y * 0.3)
	_overlay.draw_string_outline(_font, baseline, text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, 6,
		Color(0.04, 0.05, 0.08, 0.9))
	_overlay.draw_string(_font, baseline, text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size,
		Color(1, 1, 1, 0.95))
