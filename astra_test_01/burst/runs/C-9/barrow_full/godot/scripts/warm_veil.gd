extends CanvasLayer
## C-9 -- THE WARMING VEIL (the coordinator's ruling (a)): on the phone page the level's first draws compile
## their shaders -- 0.7-1.5 s of 170-990 ms frames straight after the Barrow appears
## (take/build/load_tail.json). The loading look stays up until they are done: lifted on a MEASURED signal
## (every warm-up draw issued -- the level ready, her Fire Ball's and her Meteor's warm draws done -- then
## SETTLE_FRAMES frames in a row under SETTLE_MS), never later than CAP_S after the level is ready.
## It is a veil, not a pause: the world draws under it the whole time, which is the point.

const SETTLE_FRAMES := 8
const SETTLE_MS := 25.0
const CAP_S := 3.0

var scene
var report := {}
var _rect: ColorRect
var _label: Label
var _t_ready := 0
var _last := 0
var _run := 0
var _frames := 0
var _worst_under := 0.0


func setup(p_scene) -> void:
	scene = p_scene
	layer = 128
	_rect = ColorRect.new()
	_rect.color = Color(0, 0, 0, 1)          # the web shell's own loading ground
	_rect.set_anchors_preset(Control.PRESET_FULL_RECT)
	_rect.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(_rect)
	_label = Label.new()
	_label.text = "Loading…"
	_label.add_theme_font_size_override("font_size", 28)
	_label.add_theme_color_override("font_color", Color(0.85, 0.87, 0.9, 0.9))
	_label.set_anchors_preset(Control.PRESET_CENTER)
	_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label.offset_left = -200
	_label.offset_right = 200
	add_child(_label)


func _warmups_done() -> bool:
	if not bool(scene.ready_done):
		return false
	var sfx = scene.spell_fx
	if sfx != null and sfx.fire_ball != null and not bool(sfx.fire_ball.warmed):
		return false
	if sfx != null and sfx.meteor_a != null and not bool(sfx.meteor_a.warmed):
		return false
	if sfx != null and bool(sfx.meteor_a_pending):
		return false
	var mfx0 = scene.get("meteor_fx")
	if mfx0 != null and mfx0.get("proj_a") != null and not bool(mfx0.proj_a.warmed):
		return false
	var mfx = scene.get("meteor_fx")
	if mfx != null and not bool(mfx.warmed):
		return false
	return true


func _process(_dt: float) -> void:
	if scene == null or not visible:
		return
	var now := Time.get_ticks_usec()
	var dt := float(now - _last) / 1000.0 if _last != 0 else 0.0
	_last = now
	if not bool(scene.ready_done):
		return
	if _t_ready == 0:
		_t_ready = now
		return
	_frames += 1
	_worst_under = maxf(_worst_under, dt)
	var since := float(now - _t_ready) / 1e6
	if _warmups_done() and dt < SETTLE_MS:
		_run += 1
	else:
		_run = 0
	var reason := ""
	if _run >= SETTLE_FRAMES:
		reason = "settled"
	elif since >= CAP_S:
		reason = "cap"
	if reason != "":
		visible = false
		report = {"lifted_s_after_ready": snappedf(since, 0.001), "reason": reason, "frames_under_veil": _frames,
			"worst_frame_under_veil_ms": snappedf(_worst_under, 0.1), "warmups_done": _warmups_done()}
		print("[veil] lifted " + JSON.stringify(report))
