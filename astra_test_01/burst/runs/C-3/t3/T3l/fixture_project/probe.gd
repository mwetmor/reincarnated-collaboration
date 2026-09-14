extends SceneTree
func check(value: bool, message: String) -> void:
    if not value:
        printerr("T3L_ASSERTION: ", message)
        quit(7)
func _initialize() -> void:
    call_deferred("probe")
func probe() -> void:
    root.size = Vector2i(1920, 1080)
    var scene: Node = load("res://scenes/cliffside.tscn").instantiate()
    root.add_child(scene)
    await process_frame
    var keeper: Node2D = scene.get_node("Actors/Keeper")
    keeper.set_physics_process(false)
    var tree: Sprite2D = scene.get_node("Actors/Prop_0")
    keeper.position = Vector2(400, 340)
    await create_timer(0.25).timeout
    check(tree.modulate.a <= 0.4, "behind tree fades")
    keeper.position = Vector2(400, 370)
    await create_timer(0.25).timeout
    check(tree.modulate.a >= 0.99, "front restores")
    keeper.position = Vector2(800, 340)
    await create_timer(0.25).timeout
    check(tree.modulate.a >= 0.99, "no horizontal overlap")
    var overhead: Sprite2D = scene.get_node("Overhead/Overhead_0")
    keeper.position = Vector2(400, 350)
    await create_timer(0.25).timeout
    check(overhead.modulate.a <= 0.4, "overhead overlaps without anchor test")
    keeper.position = Vector2(800, 350)
    await create_timer(0.25).timeout
    check(overhead.modulate.a >= 0.99, "overhead restores")
    var near_layer: Parallax2D = scene.get_node("Near_0")
    var near_sprite: Sprite2D = scene.get_node("Near_0/NearSprite_0")
    var camera: Camera2D = keeper.get_node("Camera2D")
    camera.make_current()
    camera.force_update_scroll()
    await process_frame
    # Set sprite local position using actual screen transforms, then restore
    # far away. This verifies near fades use screen coordinates, not feet y.
    near_sprite.position = near_layer.get_global_transform_with_canvas().affine_inverse() * (keeper.get_global_transform_with_canvas().origin - Vector2(100, 150))
    await create_timer(0.25).timeout
    check(near_sprite.modulate.a <= 0.4, "near screen overlap fades")
    near_sprite.position += Vector2(10000, 10000)
    await create_timer(0.25).timeout
    check(near_sprite.modulate.a >= 0.99, "near restores")
    var motes: CPUParticles2D = scene.get_node("Air/Particles_mist_motes")
    check(motes.amount == 37 and is_equal_approx(motes.lifetime, 2.75), "particle parameters")
    check(not motes.local_coords and motes.emitting, "world emission")
    print("T3L_RUNTIME_ASSERTIONS=complete")
    scene.queue_free()
    await process_frame
    quit(0)
