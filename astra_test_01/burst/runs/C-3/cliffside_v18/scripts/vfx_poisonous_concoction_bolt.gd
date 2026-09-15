extends Area2D
var direction: Vector2 = Vector2.RIGHT
var distance: float = 0.0
var expired: bool = false
var caster: CollisionObject2D
@export var speed_px_s: float = 520.0

func _ready() -> void:
    body_entered.connect(_on_body_entered)
    _start_layers("travel", direction.angle())
    if has_node("Ground/Streak"):
        $Ground/Streak.position = -direction * STREAK_OFFSET
    $CollisionShape2D.shape = $CollisionShape2D.shape.duplicate()
    $CollisionShape2D.shape.radius *= spell_scale

func _physics_process(delta: float) -> void:
    if expired:
        return
    var step: float = minf(speed_px_s * spell_scale * delta, 650.0 * spell_scale - distance)
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
    $Ground.hide()
    if has_node("Particles"):
        $Particles.emitting = false
    set_deferred("monitoring", false)
    var effect: Node2D = load(IMPACT_PATH).instantiate()
    effect.spell_scale = spell_scale
    effect.position = get_parent().to_local(global_position)
    get_parent().add_child(effect)
    get_tree().create_timer(TAIL_DURATION).timeout.connect(queue_free)
const FLOOR_DURATION = 0.35
const FLASH_DURATION = 0.1
const FLASH_TO = 1.0
const DECAL_DURATION = 2.0

@export var ground_squash: float = 0.6
@export var hitstop_duration: float = 0.0
@export var hitstop_time_scale: float = 1.0
@export var shake_distance: float = 0.0
@export var shake_duration: float = 0.0
var spell_scale: float = 1.0

func _start_layers(animation_name: String, angle: float = 0.0) -> void:
    $Ground.scale = Vector2(1, ground_squash) * spell_scale
    for node in $Ground.get_children():
        if node is AnimatedSprite2D:
            node.rotation = angle
            node.play(animation_name)
    if has_node("FloorLight"):
        $FloorLight.scale *= spell_scale
        create_tween().tween_property($FloorLight, "modulate:a", 0.0, FLOOR_DURATION)
    if has_node("Ground/Flash"):
        var flash: AnimatedSprite2D = $Ground/Flash
        var tween: Tween = create_tween().set_parallel(true)
        tween.tween_property(flash, "modulate:a", 0.0, FLASH_DURATION)
        tween.tween_property(flash, "scale", Vector2.ONE * FLASH_TO, FLASH_DURATION)
    if has_node("Decal"):
        $Decal.scale *= spell_scale
        create_tween().tween_property($Decal, "modulate:a", 0.0, DECAL_DURATION)
    if has_node("Particles"):
        $Particles.initial_velocity_min *= spell_scale
        $Particles.initial_velocity_max *= spell_scale
        $Particles.scale = Vector2.ONE * spell_scale

func _feedback() -> void:
    var tree: SceneTree = get_tree()
    if hitstop_duration > 0.0:
        var controller: Node = tree.root.get_node_or_null("EffectHitstop")
        if controller == null:
            controller = Node.new()
            controller.name = "EffectHitstop"
            controller.set_meta("baseline", Engine.time_scale)
            controller.set_meta("generation", 0)
            tree.root.add_child(controller)
        var generation: int = int(controller.get_meta("generation")) + 1
        controller.set_meta("generation", generation)
        Engine.time_scale = hitstop_time_scale
        tree.create_timer(hitstop_duration, true, false, true).timeout.connect(func():
            if is_instance_valid(controller) and int(controller.get_meta("generation")) == generation:
                Engine.time_scale = float(controller.get_meta("baseline"))
                controller.name = "EffectHitstopDone"
                controller.queue_free())
    var camera: Camera2D = get_viewport().get_camera_2d()
    if camera != null and shake_duration > 0.0 and shake_distance > 0.0:
        if camera.has_meta("effect_shake_tween"):
            var previous: Tween = camera.get_meta("effect_shake_tween")
            previous.kill()
        else:
            camera.set_meta("effect_shake_baseline", camera.offset)
        var baseline: Vector2 = camera.get_meta("effect_shake_baseline")
        camera.offset = baseline + Vector2(shake_distance, 0)
        var shake: Tween = tree.create_tween().bind_node(camera).set_ignore_time_scale(true)
        camera.set_meta("effect_shake_tween", shake)
        shake.tween_property(camera, "offset", baseline - Vector2(shake_distance, 0), shake_duration * 0.5)
        shake.tween_property(camera, "offset", baseline, shake_duration * 0.5)
        shake.tween_callback(func():
            camera.remove_meta("effect_shake_tween")
            camera.remove_meta("effect_shake_baseline"))
const IMPACT_PATH = "res://scenes/vfx_poisonous_concoction_impact.tscn"
const TAIL_DURATION = 2.0
const STREAK_OFFSET = 96.0
