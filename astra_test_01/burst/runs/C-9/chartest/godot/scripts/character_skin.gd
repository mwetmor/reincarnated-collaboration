extends Node
# C-9 R-C9-61: the CHARACTER TOGGLE for the original cliffside route.
#
#   K  (and the K touch button)   Keeper  ->  Knight (sprites, T1)  ->  Knight (3D, T3)  ->  Keeper
#
# NO SCENE SWITCHING.  This swaps only the player's VISUAL, inside the one scene that is
# already running.  Matt's read is that the A/B route lags because it switches scenes;
# whether or not that is the cause there, it is not a cost this test needs to pay -- the
# body, the collision shape, the camera and the walk/run speeds are the Keeper's and are
# never touched.  Each skin is a sibling node under the same CharacterBody2D and exactly
# one of them is visible.
#
# THE KEEPER REMAINS THE DEFAULT and the authority.  keeper.gd keeps driving its own
# AnimatedSprite2D and keeps owning `state` and `facing`; the other skins READ those and
# follow.  So the Keeper is not a special case of the toggle -- it is what the scene does
# when the toggle is not asked for anything, which is what "don't break the default"
# means in practice.  If this script fails to find a skin it disables itself and leaves
# the Keeper showing.

# 'Skin' shadows a native class in Godot 4.6, so the enum is named for what it selects.
enum Which { KEEPER, KNIGHT_2D, KNIGHT_3D }

const DIRECTIONS := ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]
const LABELS := {
	Which.KEEPER: "Keeper (default)",
	Which.KNIGHT_2D: "Knight — sprites (T1)",
	Which.KNIGHT_3D: "Knight — runtime 3D (T3)",
}

var _keeper: CharacterBody2D
var _keeper_sprite: AnimatedSprite2D
var _knight2d: AnimatedSprite2D
var _knight3d: Node               # scripts/knight3d.gd, or null if not built
var _skin: int = Which.KEEPER
var _label: Label
var _placeholder_note := ""
var _warned := {}
var _order: Array[int] = []
var _fps := 0.0
var _hud_age := 0.0


func _ready() -> void:
	_keeper = get_parent() as CharacterBody2D
	if _keeper == null:
		push_error("character_skin: parent is not the player body; toggle disabled")
		set_process(false)
		return
	_keeper_sprite = _keeper.get_node_or_null(^"AnimatedSprite2D")
	_knight2d = _keeper.get_node_or_null(^"KnightSprite")
	_knight3d = _keeper.get_node_or_null(^"Knight3D")

	# Only offer skins that actually exist. A toggle that cycles onto a missing skin
	# shows an empty player and reads as a crash.
	_order = [Which.KEEPER]
	if _knight2d != null and _knight2d.sprite_frames != null:
		_order.append(Which.KNIGHT_2D)
	if _knight3d != null:
		_order.append(Which.KNIGHT_3D)

	if FileAccess.file_exists("res://frames/knight_test.json"):
		var j = JSON.parse_string(FileAccess.get_file_as_string("res://frames/knight_test.json"))
		if typeof(j) == TYPE_DICTIONARY:
			# Whatever the BUILDER says is provisional about this set, not just whether
			# the whole thing is a stand-in. The note used to be gated on a single
			# `placeholder` flag, so the moment real art landed it would have gone silent
			# while still being true of the states the painter had not reached -- and
			# "the run you are watching is really the walk" is precisely the thing a
			# reviewer must not have to discover for themselves.
			var notes: Array = j.get("hud_notes", [])
			if not notes.is_empty():
				_placeholder_note = "  ⚠ " + " · ".join(PackedStringArray(notes))
	_build_hud()
	_apply()
	print("character_skin: skins available %d  (keeper=%s knight2d=%s knight3d=%s)"
		% [_order.size(), str(_keeper_sprite != null), str(_knight2d != null), str(_knight3d != null)])


func _unhandled_input(event: InputEvent) -> void:
	# ONE path in, and it is the EVENT path.
	#
	# This used to listen here AND poll Input.is_action_just_pressed() in _process, on
	# the reasoning that the touch overlay might only drive the polled API. It drives
	# both -- it calls Input.action_press AND Input.parse_input_event -- so the two
	# listeners were not redundant cover, they were a DOUBLE FIRE: one press of K ran
	# cycle() twice and the toggle skipped a skin, stepping Keeper -> runtime 3D and
	# leaving the sprite skin unreachable except by going round again.
	#
	# It survived the scene probe because the probe calls cycle() directly -- underneath
	# the input layer, which is where the defect lived. It was caught by pressing the
	# key in a browser. tools/probe_chartest.gd now sends a real InputEventKey and
	# asserts the skin advances by exactly one, so the check and the defect finally
	# occupy the same layer.
	if event.is_action_pressed("char_toggle"):
		cycle()


func _process(delta: float) -> void:
	_tick_fps(delta)
	if _skin == Which.KNIGHT_2D:
		_drive_2d()
	elif _skin == Which.KNIGHT_3D and _knight3d != null:
		_knight3d.call("drive", String(_keeper.state), String(_keeper.facing))


func cycle() -> String:
	_skin = _order[(_order.find(_skin) + 1) % _order.size()]
	_apply()
	return String(LABELS[_skin])


func skin_name() -> String:
	return String(LABELS[_skin])


func peek_next(from_label: String) -> String:
	# What ONE step forward from a given skin should land on. Exposed so the probe can
	# state its expectation in the toggle's own terms instead of re-deriving the order.
	for k in _order:
		if String(LABELS[k]) == from_label:
			return String(LABELS[_order[(_order.find(k) + 1) % _order.size()]])
	return ""


func _apply() -> void:
	if _keeper_sprite != null:
		_keeper_sprite.visible = (_skin == Which.KEEPER)
	if _knight2d != null:
		_knight2d.visible = (_skin == Which.KNIGHT_2D)
	if _knight3d != null:
		_knight3d.call("set_active", _skin == Which.KNIGHT_3D)
	if _skin == Which.KNIGHT_2D:
		_drive_2d()
	_refresh_hud()


# --- the 2D knight skin -------------------------------------------------------
# The same nearest-direction fallback keeper.gd uses, over the KNIGHT'S OWN frames.
# It must be computed against this skin's set, not the Keeper's: the knight has no
# cast or jump, and asking the Keeper's set which animations exist would answer for
# the wrong character and silently play nothing.
func _drive_2d() -> void:
	var want := String(_keeper.state)
	var chosen := _nearest(want)
	if chosen.is_empty():
		chosen = _nearest("idle")
	if chosen.is_empty():
		return
	var requested := want + "_" + String(_keeper.facing)
	if chosen != requested and not _warned.has(requested):
		print("character_skin: knight has no ", requested, "; using ", chosen)
		_warned[requested] = true
	if _knight2d.animation != chosen or not _knight2d.is_playing():
		_knight2d.play(chosen)


func _nearest(kind: String) -> String:
	var best := ""
	var best_d := 99
	var wanted: int = DIRECTIONS.find(String(_keeper.facing))
	for i in range(8):
		var cand: String = kind + "_" + String(DIRECTIONS[i])
		var d: int = absi(i - wanted)
		d = mini(d, 8 - d)
		if _knight2d.sprite_frames.has_animation(cand) and d < best_d:
			best = cand
			best_d = d
	return best


# --- HUD ----------------------------------------------------------------------
func _build_hud() -> void:
	var canvas := CanvasLayer.new()
	canvas.layer = 190
	add_child(canvas)
	var panel := ColorRect.new()
	panel.color = Color(0, 0, 0, 0.5)
	panel.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	panel.offset_bottom = 34.0
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	canvas.add_child(panel)
	_label = Label.new()
	_label.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	_label.offset_top = 6.0
	_label.offset_left = 10.0
	_label.add_theme_font_size_override("font_size", 18)
	_label.add_theme_color_override("font_color", Color(1, 0.95, 0.85))
	_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	canvas.add_child(_label)


func _refresh_hud() -> void:
	if _label == null:
		return
	var note := _placeholder_note if _skin == Which.KNIGHT_2D else ""
	_label.text = "  CHARACTER  %s   %d fps    K = next character%s" % [
		LABELS[_skin], int(round(_fps)), note]


func _tick_fps(delta: float) -> void:
	# On the HUD because the web frame rate is one of the two numbers this test exists to
	# produce, and there is no other way to read it off a page on a phone. Smoothed over
	# about a second so it reports the frame rate rather than the last frame.
	if delta > 0.0:
		var inst := 1.0 / delta
		_fps = inst if _fps <= 0.0 else _fps + (inst - _fps) * minf(delta / 1.0, 1.0)
	_hud_age += delta
	if _hud_age >= 0.25:
		_hud_age = 0.0
		_refresh_hud()
