extends CharacterBody2D

const DIRECTIONS = ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]
@export var walk_speed: float = 150.0
@export var run_speed: float = 250.0
# Offset relative to the registered feet pivot. Calibrate for production art.
@export var staff_tip_offset: Vector2 = Vector2(0, -160)
@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D
var base_frames: SpriteFrames
var advanced_frames: SpriteFrames
var frost_frames: SpriteFrames
var facing: String = "S"
var state: String = "idle"
var warned: Dictionary = {}
var fallback_remaining: float = -1.0

func _ready() -> void:
    _load_directional_kit()
    _load_vfx_picker()
    base_frames = sprite.sprite_frames
    if ResourceLoader.exists("res://frames/keeper_advanced.tres"):
        advanced_frames = load("res://frames/keeper_advanced.tres")
    if ResourceLoader.exists("res://vfx/frost_bolt.tres"):
        frost_frames = load("res://vfx/frost_bolt.tres")
    sprite.animation_finished.connect(_animation_finished)
    _play_state()

func _physics_process(delta: float) -> void:
    if Input.is_action_just_pressed("vfx_cycle"):
        vfx_kit_index = (vfx_kit_index + 1) % VFX_KITS.size()
        _update_vfx_label()
    if Input.is_action_just_pressed("gear_toggle") and advanced_frames != null:
        sprite.sprite_frames = advanced_frames if sprite.sprite_frames == base_frames else base_frames
        _play_state()
    if state == "jump" or state == "cast":
        velocity = Vector2.ZERO
        if fallback_remaining >= 0.0:
            fallback_remaining -= delta
            if fallback_remaining <= 0.0:
                _animation_finished()
        return
    var input_vector: Vector2 = Input.get_vector("move_left", "move_right", "move_up", "move_down")
    if input_vector.length_squared() > 0.0:
        facing = DIRECTIONS[posmod(roundi(input_vector.angle() / (PI / 4.0)) + 6, 8)]
    if Input.is_action_just_pressed("cast"):
        cast_kit_index = vfx_kit_index
        cast_fired = false
        state = "cast"
        velocity = Vector2.ZERO
        _play_state()
        _cast_frame_changed()
        return
    if Input.is_action_just_pressed("jump"):
        state = "jump"
        velocity = Vector2.ZERO
        _play_state()
        return
    state = "idle" if input_vector == Vector2.ZERO else ("run" if Input.is_action_pressed("run_modifier") else "walk")
    velocity = input_vector * (run_speed if state == "run" else walk_speed)
    move_and_slide()
    _play_state()

func _nearest_animation(kind: String) -> String:
    var best: String = ""
    var best_distance: int = 99
    var wanted: int = DIRECTIONS.find(facing)
    for index in range(8):
        var candidate: String = kind + "_" + DIRECTIONS[index]
        var distance: int = absi(index - wanted)
        distance = mini(distance, 8 - distance)
        if sprite.sprite_frames.has_animation(candidate) and distance < best_distance:
            best = candidate
            best_distance = distance
    return best

func _play_state() -> void:
    var requested: String = state + "_" + facing
    var chosen: String = _nearest_animation(state)
    if chosen.is_empty():
        chosen = _nearest_animation("idle")
    if chosen.is_empty():
        # Entire state and idle absent: nearest direction across other states.
        var best_distance: int = 99
        var wanted: int = DIRECTIONS.find(facing)
        for kind in ["walk", "run", "jump", "cast"]:
            var candidate: String = _nearest_animation(kind)
            if not candidate.is_empty():
                var index: int = DIRECTIONS.find(candidate.get_slice("_", 1))
                var distance: int = absi(index - wanted)
                distance = mini(distance, 8 - distance)
                if distance < best_distance:
                    chosen = candidate
                    best_distance = distance
    if chosen != requested and not warned.has(requested):
        print("Missing animation ", requested, "; using ", chosen)
        warned[requested] = true
    if sprite.animation != chosen or not sprite.is_playing():
        sprite.play(chosen)
    fallback_remaining = -1.0
    if (state == "jump" or state == "cast") and sprite.sprite_frames.get_animation_loop(chosen):
        fallback_remaining = float(sprite.sprite_frames.get_frame_count(chosen)) / sprite.sprite_frames.get_animation_speed(chosen)

func _animation_finished() -> void:
    if state == "jump" or state == "cast":
        state = "idle"
        fallback_remaining = -1.0
        _play_state()

func _spawn_frost() -> void:
    if frost_frames == null:
        return
    var effect := AnimatedSprite2D.new()
    effect.sprite_frames = frost_frames
    get_parent().add_child(effect)
    effect.global_position = global_position + staff_tip_offset
    var names: PackedStringArray = frost_frames.get_animation_names()
    var animation_name: String = "cast" if frost_frames.has_animation("cast") else names[0]
    effect.animation_finished.connect(effect.queue_free, CONNECT_ONE_SHOT)
    effect.play(animation_name)
    # Also clean up a supplied looping travel-only effect.
    if frost_frames.get_animation_loop(animation_name):
        get_tree().create_timer(1.0).timeout.connect(func():
            if is_instance_valid(effect):
                effect.queue_free())

# Directional kit: sockets refer to the actual displayed animation/frame.
var socket_cells: Dictionary = {}
var cast_fired: bool = false
var active_flare: AnimatedSprite2D
const FACING_VECTORS = {"S": Vector2(0,1), "SW": Vector2(-1,1),
    "W": Vector2(-1,0), "NW": Vector2(-1,-1), "N": Vector2(0,-1),
    "NE": Vector2(1,-1), "E": Vector2(1,0), "SE": Vector2(1,1)}

func _load_directional_kit() -> void:
    var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://sockets.json"))
    socket_cells = data.cells
    sprite.frame_changed.connect(_cast_frame_changed)

func _socket_world() -> Variant:
    var cell: Dictionary = socket_cells.get(String(sprite.animation), {})
    var points: Array = cell.get("sockets", [])
    if sprite.frame >= points.size() or points[sprite.frame] == null:
        return null
    var point: Array = points[sprite.frame]
    var local: Vector2 = Vector2(point[0], point[1]) + sprite.offset
    if sprite.centered:
        local -= sprite.sprite_frames.get_frame_texture(sprite.animation, sprite.frame).get_size() / 2.0
    return sprite.to_global(local)

func _cast_frame_changed() -> void:
    if state != "cast" or cast_fired:
        return
    var cell: Dictionary = socket_cells.get(String(sprite.animation), {})
    if cell.is_empty() or sprite.frame != int(cell.release_index):
        return
    cast_fired = true
    var socket: Variant = _socket_world()
    if socket == null:
        push_warning("No measured release socket: " + String(sprite.animation))
        return
    var direction: Vector2 = FACING_VECTORS[facing].normalized()
    var art_scale: float = sprite.global_transform.x.length()
    var flare := AnimatedSprite2D.new()
    flare.sprite_frames = load(VFX_KITS[cast_kit_index]["flare"])
    var additive := CanvasItemMaterial.new()
    additive.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
    flare.material = additive
    get_parent().add_child(flare)
    flare.global_position = socket
    flare.rotation = direction.angle()
    flare.scale = Vector2.ONE * art_scale
    flare.animation_finished.connect(flare.queue_free, CONNECT_ONE_SHOT)
    flare.play("flare")
    active_flare = flare
    var bolt: Area2D = load(VFX_KITS[cast_kit_index]["bolt"]).instantiate()
    bolt.direction = direction
    bolt.spell_scale = art_scale
    bolt.caster = self
    get_parent().add_child(bolt)
    bolt.global_position = socket

func _process(_delta: float) -> void:
    if state == "cast" and is_instance_valid(active_flare):
        var socket: Variant = _socket_world()
        if socket != null:
            active_flare.global_position = socket

const VFX_KITS = [{"name": "frost", "flare": "res://vfx/frost/flare.tres", "bolt": "res://scenes/vfx_frost_bolt.tscn"}, {"name": "fire", "flare": "res://vfx/fire/flare.tres", "bolt": "res://scenes/vfx_fire_bolt.tscn"}, {"name": "lightning", "flare": "res://vfx/lightning/flare.tres", "bolt": "res://scenes/vfx_lightning_bolt.tscn"}, {"name": "arcane", "flare": "res://vfx/arcane/flare.tres", "bolt": "res://scenes/vfx_arcane_bolt.tscn"}, {"name": "holy", "flare": "res://vfx/holy/flare.tres", "bolt": "res://scenes/vfx_holy_bolt.tscn"}, {"name": "poison", "flare": "res://vfx/poison/flare.tres", "bolt": "res://scenes/vfx_poison_bolt.tscn"}]

# Selection is live; cast_kit_index is captured before playing the cast frames.
var vfx_kit_index: int = 0
var cast_kit_index: int = 0
var vfx_label: Label

func _load_vfx_picker() -> void:
    var hud := CanvasLayer.new()
    hud.name = "VFXPicker"
    hud.layer = 10
    add_child(hud)
    vfx_label = Label.new()
    vfx_label.name = "Label"
    vfx_label.position = Vector2(16, 16)
    vfx_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
    vfx_label.add_theme_font_size_override("font_size", 22)
    vfx_label.add_theme_color_override("font_color", Color.WHITE)
    vfx_label.add_theme_color_override("font_outline_color", Color(0.04, 0.05, 0.08, 1))
    vfx_label.add_theme_constant_override("outline_size", 4)
    hud.add_child(vfx_label)
    _update_vfx_label()

func _update_vfx_label() -> void:
    vfx_label.text = "VFX: " + VFX_KITS[vfx_kit_index]["name"] + "  (Tab)"
