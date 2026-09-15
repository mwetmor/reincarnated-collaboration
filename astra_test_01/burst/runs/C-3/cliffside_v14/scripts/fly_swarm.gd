extends Node2D
# One y-sort anchor for the whole swarm; centre is local to that anchor.
@export var centre: Vector2 = Vector2.ZERO
@export var radius_px: float = 30.0
@export var speed_px_s: Vector2 = Vector2(70.0, 110.0)
@export var land_time_s: Vector2 = Vector2(0.14, 0.22)
@export var flight_time_s: Vector2 = Vector2(0.25, 0.38)
@export var jitter_px: float = 0.15
@export var fly_seeds: PackedInt64Array
enum State { FLIGHT, LAND }
var flies: Array[Dictionary] = []

func _point(rng: RandomNumberGenerator) -> Vector2:
    # Exactly 60% probability in the inner half-radius disk, 40% in the
    # outer annulus. Square-root radial sampling is uniform by area in each.
    var inner: bool = rng.randf() < 0.6
    var angle: float = rng.randf_range(0.0, TAU)
    var radius: float = sqrt(rng.randf_range(0.0, 0.25) if inner else rng.randf_range(0.25, 1.0))
    return Vector2.from_angle(angle) * radius * radius_px

func _ready() -> void:
    for i in range(fly_seeds.size()):
        var rng := RandomNumberGenerator.new()
        rng.seed = fly_seeds[i]
        var fly: Dictionary = {"rng": rng, "sprite": get_node("Fly_" + str(i)),
            "base": _point(rng), "elapsed": 0.0,
            "phase": Vector2(rng.randf_range(0.0, TAU), rng.randf_range(0.0, TAU)),
            "hz": Vector2(rng.randf_range(8.0, 14.0), rng.randf_range(8.0, 14.0)),
            "twitch": rng.randf_range(1.0, 1.4)}
        _flight(fly)
        # Warm each independent clock to a random point in its first cycle.
        _advance(fly, rng.randf_range(0.0, flight_time_s.y + land_time_s.y))
        _paint(fly)
        flies.append(fly)

func _flight(fly: Dictionary) -> void:
    var rng: RandomNumberGenerator = fly.rng
    fly.state = State.FLIGHT
    fly.target = _point(rng)
    fly.speed = rng.randf_range(speed_px_s.x, speed_px_s.y)
    fly.remaining = rng.randf_range(flight_time_s.x, flight_time_s.y)

func _land(fly: Dictionary) -> void:
    var rng: RandomNumberGenerator = fly.rng
    fly.state = State.LAND
    # On a flight timeout the reached point becomes the landing target.
    # Never teleport to a distant target when the flight budget expires.
    fly.target = fly.base
    fly.land_elapsed = 0.0
    fly.remaining = rng.randf_range(land_time_s.x, land_time_s.y)

func _advance(fly: Dictionary, delta: float) -> void:
    var left: float = delta
    while left > 0.0000001:
        var step: float = minf(left, minf(1.0 / 120.0, fly.remaining))
        fly.elapsed += step
        fly.remaining -= step
        left -= step
        if fly.state == State.FLIGHT:
            fly.base = (fly.base as Vector2).move_toward(fly.target, fly.speed * step)
            if (fly.base as Vector2).distance_to(fly.target) <= 2.0 or fly.remaining <= 0.0000001:
                _land(fly)
        else:
            fly.land_elapsed += step
            if fly.remaining <= 0.0000001:
                _flight(fly)

func _paint(fly: Dictionary) -> void:
    var displacement: Vector2
    if fly.state == State.FLIGHT:
        displacement = Vector2(sin(TAU * fly.hz.x * fly.elapsed + fly.phase.x),
            sin(TAU * fly.hz.y * fly.elapsed + fly.phase.y)) * jitter_px
    else:
        # A 1..1.4 px twitch stays below 3 px peak-to-peak in any interval.
        displacement = Vector2.from_angle(fly.phase.x) * fly.twitch * sin(fly.land_elapsed * TAU * 3.0)
    # Both-axis jitter and edge twitches cannot escape the contracted disk.
    fly.sprite.position = centre + ((fly.base as Vector2) + displacement).limit_length(radius_px + jitter_px)

func _physics_process(delta: float) -> void:
    for fly in flies:
        _advance(fly, delta)
        _paint(fly)
