extends SceneTree
# C-9 A/B verification probe.  Loads scenes/cliffside.tscn headless and asserts:
#   1. the scene instantiates and reaches a physics frame
#   2. the build starts in B, with every plate tile + parallax layer pointing at the
#      Illuminated texture set, and the H1 dressing hidden
#   3. T-equivalent toggle() swaps EVERY one of those 6 textures to A and shows the
#      H1 dressing; toggling again swaps all 6 back to B and hides it again
#   4. the Keeper still moves under input, in both registers, from the scene's own
#      start position (movement logic is lifted from runs/C-3/conductor_scripts/probe_move.gd)

const EXPECT_B := [
	"res://parallax/tiles_b/tile_0_0.png",
	"res://parallax/tiles_b/tile_4096_0.png",
	"res://parallax/layers_b/sky.png",
	"res://parallax/layers_b/far_ruins.png",
	"res://parallax/layers_b/forest_valley.png",
	"res://parallax/layers_b/mist.png",
]
const EXPECT_A := [
	"res://parallax/tiles/tile_0_0.png",
	"res://parallax/tiles/tile_4096_0.png",
	"res://parallax/layers/sky.png",
	"res://parallax/layers/far_ruins.png",
	"res://parallax/layers/forest_valley.png",
	"res://parallax/layers/mist.png",
]
const SPRITES := [
	"Foreground_0", "Foreground_1",
	"Layer_sky/Sprite2D", "Layer_far_ruins/Sprite2D",
	"Layer_forest_valley/Sprite2D", "Layer_mist/Sprite2D",
]

var fails := 0


func _check(ok: bool, what: String) -> void:
	if not ok:
		fails += 1
	print(("  PASS  " if ok else "  FAIL  ") + what)


func _paths(scene) -> Array:
	var out := []
	for n in SPRITES:
		var s = scene.get_node_or_null(NodePath(n))
		out.append("<missing>" if s == null or s.texture == null else s.texture.resource_path)
	return out


func _matches(scene, expect: Array) -> int:
	var got := _paths(scene)
	var hits := 0
	for i in expect.size():
		if got[i] == expect[i]:
			hits += 1
		else:
			print("    mismatch[%d]: got %s  want %s" % [i, got[i], expect[i]])
	return hits


func _hidden_count(scene) -> Array:
	# returns [visible, hidden] over the H1-register dressing nodes
	var vis := 0
	var hid := 0
	for b in ["Shadows", "Overhead", "Near_0", "Air"]:
		var n = scene.get_node_or_null(NodePath(b))
		if n != null:
			if n.visible: vis += 1
			else: hid += 1
	var actors = scene.get_node_or_null(^"Actors")
	if actors != null:
		for c in actors.get_children():
			if not (c is CanvasItem):
				continue
			var nm := String(c.name)
			if nm.begins_with("Prop_") or nm.begins_with("Glow_") or nm.begins_with("Swarm_"):
				if c.visible: vis += 1
				else: hid += 1
	return [vis, hid]


func _walk(keeper, action: String, frames: int) -> float:
	var start = keeper.global_position
	Input.action_press(action)
	for f in frames:
		await physics_frame
	Input.action_release(action)
	await physics_frame
	return start.distance_to(keeper.global_position)


func _initialize():
	print("=== C-9 cliffside A/B probe ===")
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	await physics_frame
	_check(scene != null, "scene instantiated")

	var keeper = scene.find_child("Keeper", true, false)
	_check(keeper != null, "Keeper found at " + str(keeper.global_position))

	# --- 1. starts in B -------------------------------------------------
	print("[start state]")
	var hits := _matches(scene, EXPECT_B)
	_check(hits == 6, "starts in B: %d/6 textures are the Illuminated set" % hits)
	_check(scene.style_name() == "B", "style_name() == B")
	var vh := _hidden_count(scene)
	print("    H1 dressing nodes: visible %d, hidden %d (total %d)" % [vh[0], vh[1], vh[0] + vh[1]])
	_check(vh[0] == 0 and vh[1] > 0, "all %d H1-register nodes hidden in B" % vh[1])

	# --- 2. movement in B -----------------------------------------------
	print("[movement in B]")
	for act in ["move_right", "move_down", "move_left", "move_up"]:
		var d: float = await _walk(keeper, act, 60)
		_check(d > 20.0, "%s moved %.1f px in 60 frames (anim %s)"
			% [act, d, keeper.get_node("AnimatedSprite2D").animation])

	# --- 3. toggle to A --------------------------------------------------
	print("[toggle -> A]")
	var swapped: int = scene.toggle()
	await physics_frame
	_check(swapped == 6, "toggle() reported %d textures swapped (want 6)" % swapped)
	hits = _matches(scene, EXPECT_A)
	_check(hits == 6, "now in A: %d/6 textures are the H1 set" % hits)
	_check(scene.style_name() == "A", "style_name() == A")
	vh = _hidden_count(scene)
	print("    H1 dressing nodes: visible %d, hidden %d" % [vh[0], vh[1]])
	_check(vh[1] == 0 and vh[0] > 0, "all %d H1-register nodes visible in A" % vh[0])

	# --- 4. movement in A ------------------------------------------------
	print("[movement in A]")
	for act in ["move_right", "move_left"]:
		var d: float = await _walk(keeper, act, 60)
		_check(d > 20.0, "%s moved %.1f px in 60 frames" % [act, d])

	# --- 5. toggle back to B ---------------------------------------------
	print("[toggle -> B]")
	swapped = scene.toggle()
	await physics_frame
	_check(swapped == 6, "toggle() reported %d textures swapped (want 6)" % swapped)
	hits = _matches(scene, EXPECT_B)
	_check(hits == 6, "back in B: %d/6 textures are the Illuminated set" % hits)
	vh = _hidden_count(scene)
	_check(vh[0] == 0, "H1-register nodes hidden again (%d hidden)" % vh[1])

	print("=== probe result: %s (%d failures) ===" % ["PASS" if fails == 0 else "FAIL", fails])
	quit(1 if fails > 0 else 0)
