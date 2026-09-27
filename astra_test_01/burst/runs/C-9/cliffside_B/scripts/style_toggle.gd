extends Node2D
# C-9 cliffside A/B style toggle.
#
#   A = the H1 register  (runs/C-7/cliffside_v45 art: parallax/tiles + parallax/layers,
#       plus the 49 H1 props, 12 particle emitters, 7 glows, 1 swarm, near-layer)
#   B = the Illuminated register (parallax/tiles_b + parallax/layers_b, painted on the
#       SAME v4 grid/geometry, so camera, walkable.json and collision are identical)
#
# Pressing T swaps every plate tile and every parallax layer texture IN PLACE -- the
# camera, the Keeper and its position are untouched.  The build starts in B.
#
# Props/particles/glows/swarms/near-layer are H1-register art and clash with B, so they
# are VISIBLE in A and HIDDEN in B.  That is a visibility flip only: the nodes, their
# scripts and their collision footprints all stay in the tree, so flipping back to A
# restores them exactly.  The player character is the existing Keeper in both registers
# (the B knight has no animation yet), so the Keeper is never hidden.

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

# Whole subtrees of H1-register dressing, hidden in B.
const H1_BRANCHES := ["Shadows", "Overhead", "Near_0", "Air"]
# Children of Actors/ with these name prefixes are H1-register dressing too.
const H1_ACTOR_PREFIXES := ["Prop_", "Glow_", "Swarm_"]

var _sprites: Array[Sprite2D] = []      # tiles then layers, in the order above
var _tex_a: Array[Texture2D] = []
var _tex_b: Array[Texture2D] = []
var _h1_nodes: Array[CanvasItem] = []
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

	_build_hud()
	_apply(true)
	print("style_toggle: ready  sprites=%d  h1_nodes=%d" % [_sprites.size(), _h1_nodes.size()])


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed(&"style_toggle"):
		toggle()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"quit_game"):
		get_tree().quit()


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
	for n in _h1_nodes:
		n.visible = not to_b
	if _label != null:
		_label.text = ("STYLE  B — Illuminated        T = switch style      Esc = quit"
			if to_b else
			"STYLE  A — H1 (props, particles, glows)        T = switch style      Esc = quit")
	return swapped


func style_name() -> String:
	return "B" if _style_b else "A"


func hidden_h1_node_count() -> int:
	return _h1_nodes.size()


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
