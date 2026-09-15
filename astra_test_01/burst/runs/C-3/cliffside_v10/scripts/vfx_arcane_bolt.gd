extends Area2D

var direction: Vector2 = Vector2.DOWN
var spell_scale: float = 1.0
var distance: float = 0.0
var expired: bool = false
var caster: CollisionObject2D

func _ready() -> void:
    body_entered.connect(_on_body_entered)
    $Head.scale = Vector2.ONE * 0.55 * spell_scale
    $Trail.direction = -direction
    $Trail.initial_velocity_min = 40.0 * spell_scale
    $Trail.initial_velocity_max = 60.0 * spell_scale
    $Trail.scale_amount_min = 0.10 * spell_scale
    $Trail.scale_amount_max = 0.20 * spell_scale
    $CollisionShape2D.shape = $CollisionShape2D.shape.duplicate()
    $CollisionShape2D.shape.radius = 3.0 * spell_scale

func _physics_process(delta: float) -> void:
    if expired:
        return
    var step: float = minf(520.0 * spell_scale * delta, 650.0 * spell_scale - distance)
    var target: Vector2 = global_position + direction * step
    var query := PhysicsRayQueryParameters2D.create(global_position, target, collision_mask)
    var excluded: Array[RID] = [get_rid()]
    if is_instance_valid(caster):
        excluded.append(caster.get_rid())
    query.exclude = excluded
    var hit: Dictionary = get_world_2d().direct_space_state.intersect_ray(query)
    if not hit.is_empty() and hit.collider is StaticBody2D:
        global_position = hit.position
        _impact()
        return
    global_position = target
    distance += step
    if distance >= 650.0 * spell_scale - 0.001:
        _impact()

func _on_body_entered(body: Node2D) -> void:
    if body is StaticBody2D:
        _impact()

func _impact() -> void:
    if expired:
        return
    expired = true
    $Head.hide()
    $Trail.emitting = false
    set_deferred("monitoring", false)
    var effect: Node2D = preload("res://scenes/vfx_arcane_impact.tscn").instantiate()
    effect.spell_scale = spell_scale
    get_parent().add_child(effect)
    effect.global_position = global_position
    get_tree().create_timer(0.4).timeout.connect(queue_free)
