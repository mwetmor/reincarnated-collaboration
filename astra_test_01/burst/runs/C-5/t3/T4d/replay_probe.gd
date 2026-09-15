extends SceneTree
const VisibilityHook = preload("res://scripts/replay_visibility.gd")
var config: Dictionary
var report: Dictionary = {"frames": [], "particle_controls": [], "hidden": [], "probe_only": false}
var world: Node
var effect: Node2D
var camera: Camera2D
var release_tick: int = 0
var captures: int = 0
var started: bool = false
var flip_sprite: Sprite2D
var flip_paths: Array = []
var flip_textures: Array[ImageTexture] = []

func _initialize() -> void:
    config = JSON.parse_string(FileAccess.get_file_as_string("res://replay_config.json"))
    Engine.physics_ticks_per_second = 60
    Engine.time_scale = 1.0
    seed(int(config.seed))
    root.size = Vector2i(int(config.crop[0]), int(config.crop[1]))
    root.content_scale_size = root.size
    root.transparent_bg = bool(config.bake)
    report.probe_only = bool(config.get("probe_only", false))
    report.viewport_size = [root.size.x, root.size.y]
    report.physics_ticks_per_second = Engine.physics_ticks_per_second
    call_deferred("_setup")

func _setup() -> void:
    world = load(config.world).instantiate()
    root.add_child(world)
    current_scene = world
    # Camera is independent of hidden Keeper art; its shake feedback stays live.
    for node in world.find_children("*", "Camera2D", true, false):
        node.enabled = false
    camera = Camera2D.new()
    camera.position = Vector2(float(config.origin[0]), float(config.origin[1]))
    root.add_child(camera)
    camera.make_current()
    camera.reset_smoothing()
    camera.force_update_scroll()
    if bool(config.bake):
        report.hidden = VisibilityHook.hide_scene(world)
    elif str(config.get("background", "ground")) != "ground":
        report.hidden = VisibilityHook.hide_scene(world)
        var background := Sprite2D.new()
        var background_image: Image
        if config.background in ["black", "white"]:
            background_image = Image.create(root.size.x, root.size.y, false, Image.FORMAT_RGBA8)
            background_image.fill(Color.BLACK if config.background == "black" else Color.WHITE)
        else:
            background_image = Image.load_from_file(config.background_path)
        background.texture = ImageTexture.create_from_image(background_image)
        background.position = camera.position
        background.z_index = -4096
        root.add_child(background)
    for keeper in world.find_children("Keeper", "", true, false):
        keeper.set_physics_process(false)
    reset_effect()
    flip_paths = config.get("flipbook", [])
    if not flip_paths.is_empty():
        # Retain feedback on the world, including victim tint and camera shake.
        # The flipbook is screen-space: its recorded shake is not applied twice.
        if is_instance_valid(effect):
            effect.hide()
        # Upload once, before frame_pre_draw. Retain strong references for the
        # entire run: replacing/freeing an ImageTexture during frame_pre_draw
        # can leave the renderer drawing its white fallback texture.
        for path in flip_paths:
            var image := Image.new()
            var error := image.load(str(path))
            if error != OK or image.is_empty() or image.get_size() != root.size or image.get_format() != Image.FORMAT_RGBA8:
                report.flipbook_error = {"path": str(path), "load_error": error}
                push_error("Invalid flipbook RGBA image: " + str(path))
                _finish()
                return
            flip_textures.append(ImageTexture.create_from_image(image))
        report.flipbook_loaded = flip_textures.size()
        var overlay := CanvasLayer.new()
        overlay.layer = 100
        root.add_child(overlay)
        flip_sprite = Sprite2D.new()
        # Native bake pivot is the crop centre, at the effect origin. The
        # screen-space crop already records camera shake; do not shake twice.
        flip_sprite.centered = true
        flip_sprite.position = Vector2(root.size) * 0.5
        flip_sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
        overlay.add_child(flip_sprite)
        _set_flip_frame()
        RenderingServer.frame_pre_draw.connect(_set_flip_frame)
    if bool(config.get("probe_only", false)):
        process_frame.connect(func(): call_deferred("_capture"))
    else:
        RenderingServer.frame_post_draw.connect(_capture)
    started = true

func _set_flip_frame() -> void:
    if not flip_textures.is_empty():
        flip_sprite.texture = flip_textures[mini(captures, flip_textures.size() - 1)]

func seed_particles(node: Node) -> void:
    if node is GPUParticles2D or node is CPUParticles2D:
        var names: Array = []
        for prop in node.get_property_list():
            names.append(prop.name)
        var supported: bool = "use_fixed_seed" in names and "seed" in names
        if supported:
            node.set("use_fixed_seed", true)
            node.set("seed", int(config.seed))
        report.particle_controls.append({"node": str(node.name), "class": node.get_class(), "fixed_seed_supported": supported, "seed": int(config.seed) if supported else null})
    for child in node.get_children():
        seed_particles(child)

func reset_effect() -> void:
    # Each public replay runs in a fresh process: no old SceneTree timers,
    # pooled instances, shader time or deferred callbacks can leak across resets.
    if is_instance_valid(effect):
        effect.free()
    Engine.time_scale = 1.0
    seed(int(config.seed))
    if bool(config.get("blank", false)):
        release_tick = Engine.get_physics_frames()
        return
    effect = load(config.effect).instantiate()
    effect.add_to_group("replay_effect")
    # Keep the supplied scene's parent/z-order, including its floor-light layer.
    var effect_parent: Node2D = world.find_child("Actors", true, false) as Node2D
    if effect_parent == null:
        effect_parent = world as Node2D
    if effect_parent == null:
        push_error("Replay world must provide a Node2D effect parent")
        quit(2)
        return
    effect.position = effect_parent.to_local(Vector2(float(config.origin[0]), float(config.origin[1])))
    seed_particles(effect)
    effect_parent.add_child(effect)
    release_tick = Engine.get_physics_frames()

func _capture() -> void:
    if not started:
        return
    var age: int = Engine.get_physics_frames() - release_tick
    var visible_scene: Array = []
    for path in report.hidden:
        var node: Node = root.get_node_or_null(path)
        if node is CanvasItem and node.is_visible_in_tree():
            visible_scene.append(path)
    var floor_live: bool = is_instance_valid(effect) and effect.has_node("FloorLight") and effect.get_node("FloorLight").is_visible_in_tree()
    report.frames.append({"movie_index": captures, "physics_frame": age, "time_scale": Engine.time_scale, "camera_offset": [camera.offset.x, camera.offset.y], "visible_scene_drawables": visible_scene, "floor_light_live": floor_live})
    captures += 1
    if int(config.frame) >= 0 and age >= int(config.frame):
        if not bool(config.get("probe_only", false)):
            var image: Image = root.get_texture().get_image()
            var error: int = image.save_png(config.capture)
            report.capture_error = error
        report.requested_frame = int(config.frame)
        report.captured_frame = age
        _finish()
    elif int(config.frame) < 0 and captures >= int(config.frames):
        _finish()

func _finish() -> void:
    started = false
    var file := FileAccess.open(config.report, FileAccess.WRITE)
    file.store_string(JSON.stringify(report, "  "))
    file.close()
    quit()
