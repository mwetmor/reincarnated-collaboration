extends SceneTree
# C-9 A/B verification probe.  Loads scenes/cliffside.tscn headless and asserts:
#   1. the scene instantiates and reaches a physics frame
#   2. the build starts in B, with every plate tile + parallax layer pointing at the
#      Illuminated texture set, each B layer sprite carrying its offsets.json y offset,
#      the KNIGHT as the visible player sprite, and the H1 dressing hidden
#   3. the knight walks in ALL EIGHT directions in B -- the body moves, the facing
#      follows the input, and the played animation is the knight cell for that facing
#      at that cell's own painted fps
#   4. T-equivalent toggle() swaps all 6 textures to A, restores every layer sprite to
#      y = 0, shows the H1 dressing and puts the KEEPER back as the player sprite;
#      toggling again reverses all of it
#   5. the Keeper still moves under input in A
# (movement logic is lifted from runs/C-3/conductor_scripts/probe_move.gd)

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
# input action -> the facing keeper.gd derives from it -> the knight cell that must play
const WALKS := [
	["move_right", "E"], ["move_left", "W"],
	["move_down", "S"], ["move_up", "N"],
]
const DIAGONALS := [
	[["move_right", "move_down"], "SE"], [["move_left", "move_down"], "SW"],
	[["move_right", "move_up"], "NE"], [["move_left", "move_up"], "NW"],
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


func _layer_y(scene) -> Array:
	var out := []
	for i in range(2, SPRITES.size()):
		var s = scene.get_node_or_null(NodePath(SPRITES[i]))
		out.append(0.0 if s == null else s.position.y)
	return out


func _hidden_count(scene) -> Array:
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


# Returns [distance_px, animation_playing_WHILE_WALKING].  The animation MUST be
# sampled before the input is released: keeper.gd drops back to idle on the very next
# physics frame after release, so a post-release read reports idle_<D> for a walk that
# ran correctly -- which is what the first version of this probe did, and it failed the
# Keeper in A too.  The check running is not the check passing.
func _walk(keeper, actions: Array, frames: int, watch) -> Array:
	var start = keeper.global_position
	for a in actions:
		Input.action_press(a)
	var anim := ""
	for f in frames:
		await physics_frame
		if f == frames - 1:
			anim = String(watch.animation)
	for a in actions:
		Input.action_release(a)
	await physics_frame
	return [start.distance_to(keeper.global_position), anim]


func _initialize():
	print("=== C-9 cliffside A/B probe (knight in B) ===")
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	await physics_frame
	_check(scene != null, "scene instantiated")

	var keeper = scene.find_child("Keeper", true, false)
	_check(keeper != null, "Keeper body found at " + str(keeper.global_position))
	var knight = keeper.get_node_or_null(^"KnightSprite")
	var keeper_spr = keeper.get_node_or_null(^"AnimatedSprite2D")
	_check(knight != null, "KnightSprite node present")
	_check(keeper_spr != null, "Keeper AnimatedSprite2D present")

	# --- 1. starts in B -------------------------------------------------
	print("[start state]")
	var hits := _matches(scene, EXPECT_B)
	_check(hits == 6, "starts in B: %d/6 textures are the Illuminated set" % hits)
	_check(scene.style_name() == "B", "style_name() == B")
	var want_dy: Array = scene.layer_offsets()
	var got_dy: Array = _layer_y(scene)
	print("    layer y offsets: want %s  got %s" % [str(want_dy), str(got_dy)])
	var dy_ok := true
	for i in want_dy.size():
		if absf(float(got_dy[i]) - float(want_dy[i])) > 0.01:
			dy_ok = false
	_check(dy_ok, "all 4 B layer sprites carry their offsets.json y offset")
	_check(knight.visible and not keeper_spr.visible,
		"player sprite in B is the knight (%s)" % scene.player_sprite_name())
	var vh := _hidden_count(scene)
	print("    H1 dressing nodes: visible %d, hidden %d (total %d)" % [vh[0], vh[1], vh[0] + vh[1]])
	_check(vh[0] == 0 and vh[1] > 0, "all %d H1-register nodes hidden in B" % vh[1])

	# --- 1b. the knight's 16 cells all exist, no mirroring --------------
	print("[knight cells]")
	var sf: SpriteFrames = knight.sprite_frames
	var missing := []
	for d in ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]:
		for kind in ["walk", "idle"]:
			var nm: String = String(kind) + "_" + String(d)
			if not sf.has_animation(nm) or sf.get_frame_count(nm) != 12:
				missing.append(nm)
	_check(missing.is_empty(), "all 16 knight cells present with 12 frames each%s"
		% ("" if missing.is_empty() else " (missing/short: " + str(missing) + ")"))
	for d in ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]:
		print("    walk_%-3s %6.3f fps    idle_%-3s %6.3f fps"
			% [d, sf.get_animation_speed("walk_" + d), d, sf.get_animation_speed("idle_" + d)])
	_check(absf(knight.scale.x - knight.scale.y) < 1e-6, "knight sprite scale is uniform (%.6f)" % knight.scale.x)

	# --- 2. the knight walks all 8 directions in B ----------------------
	print("[knight walks, all 8 directions in B]")
	for pair in WALKS:
		var r: Array = await _walk(keeper, [pair[0]], 40, knight)
		_check(float(r[0]) > 20.0 and String(r[1]) == "walk_" + String(pair[1]),
			"%-11s moved %6.1f px, facing %-2s, playing %s"
			% [pair[0], r[0], keeper.facing, r[1]])
	for pair in DIAGONALS:
		var r2: Array = await _walk(keeper, pair[0], 40, knight)
		_check(float(r2[0]) > 20.0 and String(r2[1]) == "walk_" + String(pair[1]),
			"%-22s moved %6.1f px, facing %-2s, playing %s"
			% [str(pair[0]), r2[0], keeper.facing, r2[1]])
	await physics_frame
	await physics_frame
	_check(String(knight.animation).begins_with("idle_"),
		"knight returns to idle when input stops (%s)" % knight.animation)

	# --- 3. toggle to A --------------------------------------------------
	print("[toggle -> A]")
	var swapped: int = scene.toggle()
	await physics_frame
	_check(swapped == 6, "toggle() reported %d textures swapped (want 6)" % swapped)
	hits = _matches(scene, EXPECT_A)
	_check(hits == 6, "now in A: %d/6 textures are the H1 set" % hits)
	_check(scene.style_name() == "A", "style_name() == A")
	got_dy = _layer_y(scene)
	var zeroed := true
	for v in got_dy:
		if absf(float(v)) > 0.01:
			zeroed = false
	_check(zeroed, "all 4 layer sprites back to y = 0 in A  (got %s)" % str(got_dy))
	_check(keeper_spr.visible and not knight.visible,
		"player sprite in A is the Keeper (%s)" % scene.player_sprite_name())
	vh = _hidden_count(scene)
	print("    H1 dressing nodes: visible %d, hidden %d" % [vh[0], vh[1]])
	_check(vh[1] == 0 and vh[0] > 0, "all %d H1-register nodes visible in A" % vh[0])

	# --- 4. movement in A ------------------------------------------------
	print("[Keeper walks in A]")
	for pair in WALKS:
		var r3: Array = await _walk(keeper, [pair[0]], 40, keeper_spr)
		_check(float(r3[0]) > 20.0 and String(r3[1]) == "walk_" + String(pair[1]),
			"%-11s moved %6.1f px, playing %s" % [pair[0], r3[0], r3[1]])

	# --- 5. toggle back to B ---------------------------------------------
	print("[toggle -> B]")
	swapped = scene.toggle()
	await physics_frame
	_check(swapped == 6, "toggle() reported %d textures swapped (want 6)" % swapped)
	hits = _matches(scene, EXPECT_B)
	_check(hits == 6, "back in B: %d/6 textures are the Illuminated set" % hits)
	_check(knight.visible and not keeper_spr.visible, "knight is the player sprite again")
	got_dy = _layer_y(scene)
	dy_ok = true
	for i in want_dy.size():
		if absf(float(got_dy[i]) - float(want_dy[i])) > 0.01:
			dy_ok = false
	_check(dy_ok, "B layer offsets restored (%s)" % str(got_dy))
	vh = _hidden_count(scene)
	_check(vh[0] == 0, "H1-register nodes hidden again (%d hidden)" % vh[1])

	print("=== probe result: %s (%d failures) ===" % ["PASS" if fails == 0 else "FAIL", fails])
	quit(1 if fails > 0 else 0)
