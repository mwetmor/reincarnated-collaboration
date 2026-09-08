extends CharacterBody3D
## Camera-relative WASD movement. The imported skeleton owns animation only.

@export var walk_speed: float = 1.2
@export var sprint_speed: float = 3.0
@export var acceleration: float = 9.0
@export var deceleration: float = 12.0
@export var turn_speed: float = 12.0

@onready var visual: Node3D = $Visual
@onready var camera: Camera3D = $Camera3D
var animation_player: AnimationPlayer
var current_state: String = "Idle"
var current_speed: float = 0.0
var zoom: float = 1.0
var animation_names: Dictionary = {}
var camera_offset: Vector3 = Vector3(2.5, 2.8, 4.0)

func _ready() -> void:
	for node: Node in visual.find_children("*", "AnimationPlayer", true, false):
		animation_player = node as AnimationPlayer
		break
	assert(animation_player != null, "Wizard GLB must contain an AnimationPlayer")
	for clip: StringName in animation_player.get_animation_list():
		for state: String in ["Idle", "Walk", "Run"]:
			if String(clip).get_file() == state or String(clip) == state:
				animation_names[state] = clip
				animation_player.get_animation(clip).loop_mode = Animation.LOOP_LINEAR
	assert(animation_names.size() == 3, "Wizard GLB must contain Idle, Walk and Run")
	animation_player.play(animation_names["Idle"])
	_update_camera()

func _physics_process(delta: float) -> void:
	var axes: Vector2 = Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var forward_basis: Vector3 = camera.global_basis.z
	var right_basis: Vector3 = camera.global_basis.x
	forward_basis.y = 0.0
	right_basis.y = 0.0
	var direction: Vector3 = right_basis.normalized() * axes.x + forward_basis.normalized() * axes.y
	if direction.length_squared() > 1.0:
		direction = direction.normalized()
	var speed: float = sprint_speed if Input.is_action_pressed("sprint") else walk_speed
	var rate: float = acceleration if axes.length_squared() > 0.001 else deceleration
	# Vector acceleration also preserves the diagonal speed limit while turning.
	var horizontal: Vector2 = Vector2(velocity.x, velocity.z).move_toward(Vector2(direction.x, direction.z) * speed, rate * delta)
	velocity.x = horizontal.x
	velocity.z = horizontal.y
	if not is_on_floor():
		velocity.y -= 9.8 * delta
	else:
		velocity.y = 0.0
	move_and_slide()
	current_speed = Vector2(velocity.x, velocity.z).length()
	if direction.length_squared() > 0.001:
		visual.rotation.y = lerp_angle(visual.rotation.y, atan2(direction.x, direction.z), 1.0 - exp(-turn_speed * delta))
	var next_state: String = "Idle"
	if current_speed > 0.07:
		next_state = "Run" if Input.is_action_pressed("sprint") else "Walk"
	if next_state != current_state:
		current_state = next_state
		animation_player.play(animation_names[current_state], 0.18)
	animation_player.speed_scale = 1.0 if current_state == "Idle" else clampf(current_speed / (sprint_speed if current_state == "Run" else walk_speed), 0.25, 1.25)
	var state_label: Label = get_node_or_null("../HUD/Status") as Label
	if state_label:
		state_label.text = "%s   /   %.1f m/s" % [current_state.to_upper(), current_speed]

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			zoom = clampf(zoom - 0.1, 0.65, 1.6)
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			zoom = clampf(zoom + 0.1, 0.65, 1.6)
		_update_camera()
	if event is InputEventKey and event.pressed and event.keycode == KEY_ESCAPE:
		get_tree().quit()

func _update_camera() -> void:
	camera.position = camera_offset * zoom
	camera.look_at(global_position + Vector3(0, 0.95, 0), Vector3.UP)
