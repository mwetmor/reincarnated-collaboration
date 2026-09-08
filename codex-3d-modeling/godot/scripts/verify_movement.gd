extends SceneTree
## Integration test: real imported character, collision, physical keys and animation.
var player: CharacterBody3D
var failures: Array[String] = []
var measurements: Dictionary = {}

func _initialize() -> void:
	call_deferred("_run")

func frames(count: int) -> void:
	for i: int in range(count):
		await physics_frame

func key(code: Key, pressed: bool) -> void:
	var event: InputEventKey = InputEventKey.new()
	event.keycode = code
	event.physical_keycode = code
	event.pressed = pressed
	Input.parse_input_event(event)
	Input.flush_buffered_events()

func check(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
		push_error(message)

func reset_player() -> void:
	for code: Key in [KEY_W, KEY_A, KEY_S, KEY_D, KEY_SHIFT]:
		key(code, false)
	player.global_position = Vector3(0, 0.02, 0)
	player.velocity = Vector3.ZERO
	await frames(30)

func travel(codes: Array[Key], count: int = 60) -> Dictionary:
	await reset_player()
	var start: Vector3 = player.global_position
	for code: Key in codes:
		key(code, true)
	await frames(count)
	var result: Dictionary = {"distance": Vector2(player.global_position.x-start.x,player.global_position.z-start.z).length(), "speed":player.get("current_speed"), "state":player.get("current_state"), "position":str(player.global_position)}
	for code: Key in codes:
		key(code, false)
	await frames(30)
	check(player.get("current_state") == "Idle", "Releasing movement must return to Idle")
	check(player.velocity.length() < 0.02, "Character must stop after releasing movement")
	check(absf(player.global_position.y) < 0.025, "Character must remain on the floor")
	return result

func _run() -> void:
	var scene: PackedScene = load("res://scenes/courtyard.tscn") as PackedScene
	check(scene != null, "Courtyard scene loads")
	if scene == null:
		quit(1)
		return
	var level: Node = scene.instantiate()
	root.add_child(level)
	current_scene = level
	player = level.get_node("Player") as CharacterBody3D
	await frames(60)
	check(player.is_on_floor(), "Capsule rests on the courtyard floor")
	check(player.get("animation_names").size() == 3, "Three named clips survived Blender export and Godot import")
	check(player.get("current_state") == "Idle", "Character starts in Idle")
	for definition: Array in [["W",KEY_W],["A",KEY_A],["S",KEY_S],["D",KEY_D]]:
		var result: Dictionary = await travel([definition[1]])
		measurements[definition[0]] = result
		check(result["distance"] > 1.0 and result["distance"] < 1.3, "WASD movement covers the expected walking distance: " + definition[0])
		check(result["state"] == "Walk", "Movement selects Walk: " + definition[0])
	var sprint: Dictionary = await travel([KEY_W,KEY_SHIFT])
	measurements["sprint"] = sprint
	check(sprint["speed"] > 2.9 and sprint["state"] == "Run", "Shift + W selects Run at sprint speed")
	check(sprint["distance"] > measurements["W"]["distance"] * 2.0, "Sprint moves substantially faster than walking")
	var diagonal: Dictionary = await travel([KEY_W,KEY_D])
	measurements["diagonal"] = diagonal
	check(absf(diagonal["distance"]-measurements["W"]["distance"]) < 0.06, "Diagonal input must not increase movement speed")
	await reset_player()
	key(KEY_SHIFT, true)
	await frames(20)
	check(player.get("current_state") == "Idle", "Shift without direction stays Idle")
	key(KEY_SHIFT, false)
	player.global_position = Vector3(0, 0.02, -8.6)
	key(KEY_W, true)
	key(KEY_SHIFT, true)
	await frames(120)
	check(player.global_position.z >= -9.13, "Boundary wall stops the capsule")
	measurements["boundary_position"] = str(player.global_position)
	key(KEY_W, false)
	key(KEY_SHIFT, false)
	var report: Dictionary = {"passed":failures.is_empty(),"failures":failures,"measurements":measurements}
	var file: FileAccess = FileAccess.open("res://../logs/movement-verification.json",FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(report,"  "))
	print("WIZARD_MOVEMENT_VERIFICATION ",JSON.stringify(report))
	quit(0 if failures.is_empty() else 1)
