extends Node2D
# C-9 cliffside A/B style toggle.
#
#   A = the H1 register  (runs/C-7/cliffside_v45 art: parallax/tiles + parallax/layers,
#       plus the 49 H1 props, 12 particle emitters, 7 glows, 1 swarm, near-layer, and
#       the KEEPER as the player character)
#   B = the Illuminated register (parallax/tiles_b + parallax/layers_b, and the
#       KNIGHT as the player character)
#
# Pressing T swaps, in place and with the camera and the player's POSITION untouched:
#   * both plate tiles and all four parallax layer textures
#   * each parallax layer sprite's vertical position (see LAYER OFFSETS below)
#   * the player sprite -- Keeper in A, knight in B
#   * the H1-register dressing, which is visible in A and hidden in B
# The build starts in B.
#
# The plate is painted on the SAME v4 grid as the H1 plate, so camera, walkable.json
# and collision are identical in both registers and nothing about movement changes.
#
# LAYER OFFSETS.  The B parallax art has a different ASPECT from the H1 art, and this
# build scales it to the H1 layer's WIDTH and keeps that aspect rather than stretching
# it to the H1 height (which squashed sky and forest by up to 1.6x last time).  A layer
# that keeps its aspect lands its horizon on the wrong row, so each B layer carries a
# vertical offset -- computed by tools/build_b_assets.py, stored in
# parallax/layers_b/offsets.json -- applied to the layer Sprite2D's own position.  A is
# always 0.  The Parallax2D scroll maths above it is never touched, so the swap is
# exactly reversible.
#
# PLAYER SPRITE.  The knight is a skin on the same Keeper CharacterBody2D (see
# scripts/knight_skin.gd): one physics body, one collision shape, one camera, two
# AnimatedSprite2D children of which exactly one is visible.  The knight has walk and
# idle cells only, so in B run maps to his walk and cast/jump map to his idle -- the
# HUD line says so, because a mapped state must not read as a painted one.

const TILE_NODES := ["Foreground_0", "Foreground_1"]
const TILE_B := [
	"res://parallax/tiles_b/tile_0_0.png",
	"res://parallax/tiles_b/tile_4096_0.png",
]

const LAYER_NODES := [
	"Layer_sky/Sprite2D",
	"Layer_far_ruins/Sprite2D",
	"Layer_forest_valley/Sprite2D",
	"Layer_mist/Sprite2D",
]
const LAYER_B := [
	"res://parallax/layers_b/sky.png",
	"res://parallax/layers_b/far_ruins.png",
	"res://parallax/layers_b/forest_valley.png",
	"res://parallax/layers_b/mist.png",
]
const LAYER_KEYS := ["sky", "far_ruins", "forest_valley", "mist"]
const OFFSETS_JSON := "res://parallax/layers_b/offsets.json"

# Whole subtrees of H1-register dressing, hidden in B.
const H1_BRANCHES := ["Shadows", "Overhead", "Near_0", "Air"]
# Children of Actors/ with these name prefixes are H1-register dressing too.
const H1_ACTOR_PREFIXES := ["Prop_", "Glow_", "Swarm_"]

# %s is the run coverage (built in _ready from frames/knight_fit.json, so it cannot go
# stale if the missing direction is later filled) and %s is the E-facing rig/Grok mode.
const HUD_B := "STYLE  B — Illuminated (knight; %s, cast/jump→idle)   E-facing: %s        T = style      Shift = run      G = E rig/Grok      Esc = quit"
const HUD_A := "STYLE  A — H1 (Keeper; props, particles, glows)        T = style      Esc = quit"

var _sprites: Array[Sprite2D] = []      # tiles then layers, in the order above
var _tex_a: Array[Texture2D] = []
var _tex_b: Array[Texture2D] = []
var _layer_dy: Array[float] = []        # B vertical offset per LAYER_NODES entry
var _layer_dx: Array[float] = []        # B horizontal offset (far_ruins framing)
var _h1_nodes: Array[CanvasItem] = []
var _keeper_sprite: CanvasItem = null
var _knight_sprite: CanvasItem = null
var _figures: Array = []          # the B-only still figures (angel, demon)
var _run_note: String = "run painted"
var _style_b: bool = true
var _label: Label


func _ready() -> void:
	for n in TILE_NODES + LAYER_NODES:
		var s := get_node_or_null(NodePath(n)) as Sprite2D
		if s == null:
			push_error("style_toggle: missing sprite node '%s'" % n)
			continue
		_sprites.append(s)
		_tex_a.append(s.texture)          # A is already loaded by the scene itself
	for p in TILE_B + LAYER_B:
		_tex_b.append(load(p) as Texture2D)

	_load_layer_offsets()

	for b in H1_BRANCHES:
		var node := get_node_or_null(NodePath(b)) as CanvasItem
		if node != null:
			_h1_nodes.append(node)
	var actors := get_node_or_null(^"Actors")
	if actors != null:
		for child in actors.get_children():
			if not (child is CanvasItem):
				continue
			for prefix in H1_ACTOR_PREFIXES:
				if String(child.name).begins_with(prefix):
					_h1_nodes.append(child as CanvasItem)
					break

	_figures.clear()
	var actors_root := get_node_or_null(^"Actors")
	if actors_root != null:
		for child in actors_root.get_children():
			if child.has_method("set_active") and child.has_method("is_active"):
				_figures.append(child)

	var keeper := find_child("Keeper", true, false)
	if keeper != null:
		_keeper_sprite = keeper.get_node_or_null(^"AnimatedSprite2D") as CanvasItem
		_knight_sprite = keeper.get_node_or_null(^"KnightSprite") as CanvasItem
	if _keeper_sprite == null:
		push_error("style_toggle: Keeper/AnimatedSprite2D not found")
	if _knight_sprite == null:
		push_error("style_toggle: Keeper/KnightSprite not found")

	_read_run_coverage()
	_build_hud()
	_apply(true)
	print("style_toggle: ready  sprites=%d  h1_nodes=%d  knight=%s  b_figures=%d"
		% [_sprites.size(), _h1_nodes.size(), str(_knight_sprite != null), _figures.size()])


# The knight's run is painted per direction and Grok did not deliver one for every
# direction, so the HUD states the coverage rather than implying it is complete.
func _read_run_coverage() -> void:
	if not FileAccess.file_exists("res://frames/knight_fit.json"):
		return
	var parsed = JSON.parse_string(FileAccess.get_file_as_string("res://frames/knight_fit.json"))
	if not (parsed is Dictionary):
		return
	var have: Array = parsed.get("run_directions", [])
	var lack: Array = parsed.get("run_missing_directions", [])
	if lack.is_empty():
		_run_note = "run painted 8/8"
	else:
		_run_note = "run painted %d/8, %s→walk" % [have.size(), ", ".join(lack)]


func _load_layer_offsets() -> void:
	var dy := {}
	var dx := {}
	if FileAccess.file_exists(OFFSETS_JSON):
		var parsed = JSON.parse_string(FileAccess.get_file_as_string(OFFSETS_JSON))
		if parsed is Dictionary and parsed.has("offsets"):
			dy = parsed["offsets"]
			dx = parsed.get("offsets_x", {})
		else:
			push_error("style_toggle: %s has no 'offsets'" % OFFSETS_JSON)
	else:
		push_error("style_toggle: %s missing; B layers will sit at 0" % OFFSETS_JSON)
	for key in LAYER_KEYS:
		_layer_dy.append(float(dy.get(key, 0.0)))
		_layer_dx.append(float(dx.get(key, 0.0)))


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed(&"style_toggle"):
		toggle()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"rig_toggle"):
		toggle_rig()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"quit_game"):
		get_tree().quit()


# RIG PROBE (R-C9-34).  G swaps the E-facing knight between the 2D puppet rig cut from
# the painted still and the Grok-generated E cells, in place, so the two can be watched
# on the same spot.  Returns the mode now in force.  Only E changes; the other seven
# directions are Grok cells either way, and the HUD says which mode is live so a rig
# frame is never read as a painted one (and vice versa).
func toggle_rig() -> String:
	if _knight_sprite != null and _knight_sprite.has_method("set_use_rig"):
		_knight_sprite.call("set_use_rig", not bool(_knight_sprite.get("use_rig")))
	_refresh_hud()
	return rig_mode()


func rig_mode() -> String:
	if _knight_sprite == null or not _knight_sprite.has_method("rig_available"):
		return "GROK (no rig)"
	if not bool(_knight_sprite.call("rig_available")):
		return "GROK (no rig)"
	return "RIG" if bool(_knight_sprite.get("use_rig")) else "GROK"


func _refresh_hud() -> void:
	if _label == null:
		return
	_label.text = (HUD_B % [_run_note, rig_mode()]) if _style_b else HUD_A


# Returns the number of textures swapped, so the headless probe can count them.
func toggle() -> int:
	return _apply(not _style_b)


func _apply(to_b: bool) -> int:
	_style_b = to_b
	var swapped := 0
	var src: Array[Texture2D] = _tex_b if to_b else _tex_a
	for i in _sprites.size():
		if i >= src.size() or src[i] == null:
			continue
		if _sprites[i].texture != src[i]:
			_sprites[i].texture = src[i]
			swapped += 1
	# layer sprites follow the tiles in _sprites, so layer i is _sprites[TILE_NODES.size() + i]
	for i in _layer_dy.size():
		var idx := TILE_NODES.size() + i
		if idx < _sprites.size():
			_sprites[idx].position.y = _layer_dy[i] if to_b else 0.0
			_sprites[idx].position.x = _layer_dx[i] if to_b else 0.0
	if _keeper_sprite != null:
		_keeper_sprite.visible = not to_b
	if _knight_sprite != null:
		_knight_sprite.visible = to_b
		if to_b and _knight_sprite.has_method("sync_now"):
			_knight_sprite.call("sync_now")
	for n in _h1_nodes:
		n.visible = not to_b
	# The B-only still figures. They take their COLLISION down with them, not just
	# their sprite: a hidden StaticBody2D still blocks, and the Keeper would walk into
	# an invisible angel in style A.
	for f in _figures:
		f.call("set_active", to_b)
	_refresh_hud()
	return swapped


func style_name() -> String:
	return "B" if _style_b else "A"


func hidden_h1_node_count() -> int:
	return _h1_nodes.size()


func layer_offsets() -> Array[float]:
	return _layer_dy


func layer_offsets_x() -> Array[float]:
	return _layer_dx


func figure_count() -> int:
	return _figures.size()


func active_figure_count() -> int:
	var n := 0
	for f in _figures:
		if bool(f.call("is_active")):
			n += 1
	return n


func player_sprite_name() -> String:
	if _knight_sprite != null and _knight_sprite.visible:
		return "KnightSprite"
	if _keeper_sprite != null and _keeper_sprite.visible:
		return "AnimatedSprite2D"
	return "<none visible>"


func _build_hud() -> void:
	var canvas := CanvasLayer.new()
	canvas.name = "StyleHud"
	canvas.layer = 100
	add_child(canvas)
	var panel := ColorRect.new()
	panel.color = Color(0, 0, 0, 0.45)
	# bottom of the screen: the Keeper's own VFX-kit readout already owns the top-left
	panel.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
	panel.offset_top = -34.0
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	canvas.add_child(panel)
	_label = Label.new()
	_label.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
	_label.offset_top = -28.0
	_label.offset_left = 18.0
	_label.add_theme_color_override("font_color", Color(1, 0.96, 0.86))
	_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	canvas.add_child(_label)
