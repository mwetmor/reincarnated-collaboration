extends Sprite2D
# body_width is the exported character opaque width in level pixels.
@export var keeper_path: NodePath
@export var body_width: float = 48.0
# 0: prop behind anchor; 1: overhead opaque bounds; 2: near full screen rect.
@export var fade_mode: int = 0
@export var opaque_rect: Rect2
@onready var keeper: Node2D = get_node(keeper_path)
var target_alpha: float = 1.0
var fade_tween: Tween

func _process(_delta: float) -> void:
    if not is_instance_valid(keeper):
        return
    var body: Rect2 = keeper.get_global_transform_with_canvas() * Rect2(-body_width / 2.0, -130.0, body_width, 130.0)
    var local_bounds: Rect2 = get_rect() if fade_mode == 2 else opaque_rect
    var displayed: Rect2 = get_global_transform_with_canvas() * local_bounds
    var overlap: bool = displayed.has_area() and displayed.intersects(body)
    if fade_mode == 0:
        overlap = overlap and keeper.global_position.y < global_position.y
    var wanted: float = 0.35 if overlap else 1.0
    if wanted != target_alpha:
        target_alpha = wanted
        if fade_tween != null:
            fade_tween.kill()
        fade_tween = create_tween()
        fade_tween.tween_property(self, "modulate:a", wanted, 0.15)
