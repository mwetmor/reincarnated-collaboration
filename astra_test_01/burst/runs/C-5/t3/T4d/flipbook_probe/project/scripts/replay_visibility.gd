extends Node
# Hide initial scene drawables individually. Ancestors and scripts remain live;
# subsequently spawned effect nodes, floor light, tint, hit-stop and shake survive.
func _ready() -> void:
    get_tree().process_frame.connect(_configure, CONNECT_ONE_SHOT)

static func hide_scene(node: Node) -> Array:
    var hidden: Array = []
    if node.is_in_group("replay_effect"):
        return hidden
    if node is Sprite2D or node is AnimatedSprite2D or node is Polygon2D or node is Line2D or node is Control or node is GPUParticles2D or node is CPUParticles2D or node is TileMapLayer or node is TileMap:
        node.hide()
        hidden.append(str(node.get_path()))
    for child in node.get_children():
        hidden.append_array(hide_scene(child))
    return hidden

func _configure() -> void:
    get_viewport().transparent_bg = true
    if get_tree().current_scene != null:
        hide_scene(get_tree().current_scene)
