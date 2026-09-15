extends Sprite2D
# body_width is retained for mode 2's legacy near-layer rectangle.
@export var keeper_path: NodePath
@export var body_width: float = 48.0
# 0: opaque overlap behind anchor; 1: opaque overlap; 2: near full screen rect.
@export var fade_mode: int = 0
# Retained for byte-compatible scene exports; modes 0/1 now use alpha masks.
@export var opaque_rect: Rect2
@onready var keeper: Node2D = get_node(keeper_path)
var target_alpha: float = 1.0
var fade_tween: Tween
var prop_mask: BitMap
# Texture keys retain their resources and cannot alias recycled instance IDs.
var frame_masks: Dictionary = {}

func _ready() -> void:
    if fade_mode != 2 and texture != null:
        prop_mask = _alpha_mask(texture)

func _alpha_mask(source: Texture2D) -> BitMap:
    var mask := BitMap.new()
    mask.create_from_image_alpha(source.get_image(), 0.5)
    return mask

func _opaque_at(mask: BitMap, point: Vector2, inverse: Transform2D,
        rect: Rect2, horizontal_flip: bool, vertical_flip: bool) -> bool:
    var local: Vector2 = inverse * point
    if not rect.has_point(local):
        return false
    var size: Vector2i = mask.get_size()
    var uv: Vector2 = (local - rect.position) / rect.size
    var pixel := Vector2i(floori(uv.x * size.x), floori(uv.y * size.y))
    if horizontal_flip:
        pixel.x = size.x - 1 - pixel.x
    if vertical_flip:
        pixel.y = size.y - 1 - pixel.y
    return pixel.x >= 0 and pixel.y >= 0 and pixel.x < size.x and pixel.y < size.y and mask.get_bitv(pixel)

func _pixel_overlap() -> bool:
    if prop_mask == null:
        return false
    var sprite := keeper.get_node_or_null("AnimatedSprite2D") as AnimatedSprite2D
    if sprite == null or sprite.sprite_frames == null:
        return false
    var frames: SpriteFrames = sprite.sprite_frames
    if not frames.has_animation(sprite.animation) or frames.get_frame_count(sprite.animation) == 0:
        return false
    var current: Texture2D = frames.get_frame_texture(sprite.animation, sprite.frame)
    if current == null:
        return false
    if not frame_masks.has(current):
        frame_masks[current] = _alpha_mask(current)
    var mask: BitMap = frame_masks[current]
    var size: Vector2 = current.get_size()
    var origin: Vector2 = sprite.offset - (size / 2.0 if sprite.centered else Vector2.ZERO)
    var frame_rect := Rect2(origin, size)
    var prop_rect: Rect2 = get_rect()
    var prop_transform: Transform2D = get_global_transform_with_canvas()
    var frame_transform: Transform2D = sprite.get_global_transform_with_canvas()
    if is_zero_approx(prop_transform.determinant()) or is_zero_approx(frame_transform.determinant()):
        return false
    var intersection: Rect2 = (prop_transform * prop_rect).intersection(frame_transform * frame_rect)
    if not intersection.has_area():
        return false
    var prop_inverse: Transform2D = prop_transform.affine_inverse()
    var frame_inverse: Transform2D = frame_transform.affine_inverse()
    # Fixed canvas pixel-centre lattice, 2 px apart, not a sprite-local grid.
    var first_x: float = ceil((intersection.position.x - 0.5) / 2.0) * 2.0 + 0.5
    var first_y: float = ceil((intersection.position.y - 0.5) / 2.0) * 2.0 + 0.5
    var y: float = first_y
    while y < intersection.end.y:
        var x: float = first_x
        while x < intersection.end.x:
            var point := Vector2(x, y)
            if _opaque_at(prop_mask, point, prop_inverse, prop_rect, flip_h, flip_v) and _opaque_at(mask, point, frame_inverse, frame_rect, sprite.flip_h, sprite.flip_v):
                return true
            x += 2.0
        y += 2.0
    return false

func _process(_delta: float) -> void:
    if not is_instance_valid(keeper):
        return
    var overlap: bool
    if fade_mode == 2:
        # Preserve near's full displayed rect, body proxy, and 0.15 s tween.
        var body: Rect2 = keeper.get_global_transform_with_canvas() * Rect2(-body_width / 2.0, -130.0, body_width, 130.0)
        var displayed: Rect2 = get_global_transform_with_canvas() * get_rect()
        overlap = displayed.has_area() and displayed.intersects(body)
    elif fade_mode == 0:
        overlap = keeper.global_position.y < global_position.y and _pixel_overlap()
    else:
        overlap = _pixel_overlap()
    var wanted: float = 0.35 if overlap else 1.0
    if wanted != target_alpha:
        target_alpha = wanted
        if fade_tween != null:
            fade_tween.kill()
        fade_tween = create_tween()
        fade_tween.tween_property(self, "modulate:a", wanted, 0.15 if fade_mode == 2 else 0.06)
