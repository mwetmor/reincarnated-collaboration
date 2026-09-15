extends Sprite2D
@export var flicker_hz: float = 4.0
@export var flicker_amount: float = 0.4
# Stable seed per manifest entry: phases differ per instance, never per frame.
@export var phase_seed: int = 1
var phases: Vector3
var elapsed: float = 0.0
var base_alpha: float
var base_scale: Vector2
var centre_offset: Vector2

func _ready() -> void:
    var rng := RandomNumberGenerator.new()
    rng.seed = phase_seed
    phases = Vector3(rng.randf_range(0, TAU), rng.randf_range(0, TAU), rng.randf_range(0, TAU))
    base_alpha = modulate.a
    base_scale = scale
    centre_offset = offset * scale

func _process(delta: float) -> void:
    elapsed += delta
    var t: float = elapsed * TAU * flicker_hz
    var n: float = (sin(t + phases.x) + sin(t * 1.73 + phases.y) + sin(t * 2.61 + phases.z)) / 3.0
    var factor: float = 1.0 + flicker_amount * n
    modulate.a = base_alpha * factor
    scale = base_scale * factor
    # Keep the visual centre fixed while the node's y-sort anchor stays fixed.
    offset = centre_offset / scale
