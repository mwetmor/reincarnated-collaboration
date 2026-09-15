extends Node2D

var spell_scale: float = 1.0

func _ready() -> void:
    var frames: SpriteFrames = $Shatter.sprite_frames
    var max_height: float = 1.0
    for i in range(frames.get_frame_count("impact")):
        max_height = maxf(max_height, frames.get_frame_texture("impact", i).get_height())
    $Shatter.scale = Vector2.ONE * (0.9 * 240.0 * spell_scale / max_height)
    $Burst.initial_velocity_min = 120.0 * spell_scale
    $Burst.initial_velocity_max = 260.0 * spell_scale
    $Burst.gravity = Vector2(0, 300.0 * spell_scale)
    $Burst.scale_amount_min = 0.05 * spell_scale
    $Burst.scale_amount_max = 0.12 * spell_scale
    $Burst.emitting = true
    $Shatter.play("impact")
    var duration: float = float(frames.get_frame_count("impact")) / frames.get_animation_speed("impact")
    get_tree().create_timer(maxf(duration, 0.5) + 0.1).timeout.connect(queue_free)
