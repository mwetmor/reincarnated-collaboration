extends SceneTree
const G1 = preload("res://scripts/vfx_g1.gd")
var errors: Array = []
var measurements: Dictionary = {}
func check(ok: bool, message: String) -> void:
    if not ok:
        errors.append(message)
        printerr("G1_ASSERTION: ", message)
func _initialize() -> void:
    call_deferred("probe")
func dummy(parent: Node2D, point: Vector2, label: String) -> Area2D:
    var area := Area2D.new()
    area.name = label
    area.position = point
    area.collision_layer = 2
    area.collision_mask = 0
    area.monitoring = false
    var shape := CollisionShape2D.new()
    var rectangle := RectangleShape2D.new()
    rectangle.size = Vector2(30, 20)
    shape.shape = rectangle
    area.add_child(shape)
    parent.add_child(area)
    area.add_to_group("vfx_targets")
    return area
func wait_effect(effect: Area2D, budget: int = 300) -> void:
    for i in range(budget):
        if not effect.active:
            return
        await physics_frame
    check(false, "effect exceeded physics frame budget")
    effect.cancel()
func probe() -> void:
    Engine.physics_ticks_per_second = 60
    G1.events.clear()
    var main_path: String = ProjectSettings.get_setting("application/run/main_scene", "res://scenes/main.tscn")
    var main: Node2D = load(main_path).instantiate()
    root.add_child(main)
    var keeper: CharacterBody2D = main.find_child("Keeper", true, false)
    keeper.set_physics_process(false)
    keeper.sprite.pause()
    var parent: Node2D = keeper.get_parent()
    var original_targets: Array = get_nodes_in_group("vfx_targets")
    measurements["live_target_count"] = original_targets.size()
    for target in original_targets:
        target.remove_from_group("vfx_targets")
    var target := dummy(parent, keeper.position + Vector2(0,100), "ProbeTarget")
    # Fire in the scene-load turn, before the first physics frame.
    keeper.facing = "S"
    keeper.state = "cast"
    keeper.cast_kit_index = 0
    keeper.cast_fired = false
    keeper.sprite.play("cast_S")
    keeper.sprite.pause()
    var cell: Dictionary = keeper.socket_cells["cast_S"]
    keeper.sprite.frame = int(cell.release_index)
    keeper._cast_frame_changed()
    measurements["released_before_first_physics"] = G1.events.size()
    check(G1.events.is_empty(), "first cast must wait a physics frame")
    await physics_frame
    await process_frame
    var pool: Array = get_nodes_in_group("vfx_g1_pool")
    check(pool.size() == 1, "first cast creates one resolved effect")
    if pool.is_empty():
        finish()
        return
    var first: Area2D = pool[0]
    var head_id: int = first.get_node("Head").get_instance_id()
    await wait_effect(first)
    var contacts: Array = G1.events.filter(func(e): return e.event == "contact" and e.effect_id == first.effect_id)
    measurements["first_cast_contacts"] = contacts.size()
    check(contacts.size() == 1, "first cast registers exactly one contact")
    for event in contacts:
        check(event.age_frames - event.collision_age_frames <= 1, "contact delay <= one frame")
    # Nearest in inclusive facing cone and inclusive range, plus cursor fallback.
    var origin: Vector2 = keeper.global_position
    var near := dummy(parent, parent.to_local(origin + Vector2(60,0)), "Near")
    var far := dummy(parent, parent.to_local(origin + Vector2(90,0)), "Far")
    var outside := dummy(parent, parent.to_local(origin + Vector2(10,30)), "Outside")
    var resolved: Dictionary = G1.resolve_target(self, origin, Vector2.RIGHT, origin + Vector2(-70, -30), 100.0)
    check(resolved.target == near, "nearest target inside cone")
    near.remove_from_group("vfx_targets")
    far.remove_from_group("vfx_targets")
    outside.remove_from_group("vfx_targets")
    target.remove_from_group("vfx_targets")
    var boundary := dummy(parent, parent.to_local(origin + Vector2.RIGHT.rotated(deg_to_rad(30.0)) * 100.0), "Boundary")
    check(G1.resolve_target(self, origin, Vector2.RIGHT, origin, 100.01).target == boundary, "inclusive 30 degree cone")
    check(G1.resolve_target(self, origin, Vector2.RIGHT, origin, 99.0).kind == "cursor", "range excludes farther target")
    boundary.position = parent.to_local(origin + Vector2.RIGHT.rotated(deg_to_rad(30.1)) * 60.0)
    check(G1.resolve_target(self, origin, Vector2.RIGHT, origin, 100.0).kind == "cursor", "outside 30 degree cone")
    boundary.remove_from_group("vfx_targets")
    near.add_to_group("vfx_targets")
    far.add_to_group("vfx_targets")
    outside.add_to_group("vfx_targets")
    target.add_to_group("vfx_targets")
    var cursor: Vector2 = origin + Vector2(-70, -30)
    var fallback: Dictionary = G1.resolve_target(self, origin, Vector2.LEFT, cursor, 100.0)
    check(fallback.kind == "cursor" and fallback.point == cursor, "no cone target resolves exact cursor")
    measurements["cursor_error_px"] = fallback.point.distance_to(cursor)
    var kit: Dictionary = keeper.VFX_KITS[0].duplicate(true)
    var second: Area2D = G1.acquire(parent, kit, origin, fallback, keeper)
    check(second.get_node("Head").get_instance_id() == head_id, "pooled head reused")
    check(second.get_node("Head").texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR, "linear head")
    await wait_effect(second)
    check(second.global_position.distance_to(cursor) <= 0.001, "cursor effect reaches point")
    var count: int = get_nodes_in_group("vfx_g1_pool").size()
    check(G1.acquire(parent, kit, origin, {}, keeper) == null, "unresolved spawn rejected")
    check(G1.acquire(parent, kit, origin, {"point": origin}, keeper) == null, "incomplete resolution rejected")
    check(get_nodes_in_group("vfx_g1_pool").size() == count, "invalid spawn allocates nothing")
    var cancelled: Area2D = G1.acquire(parent, kit, origin, fallback, keeper)
    cancelled.cancel()
    cancelled.cancel()
    # Real target footprints in the unmodified scene geometry.
    for area in [target, near, far, outside]:
        area.remove_from_group("vfx_targets")
    for area in original_targets:
        area.add_to_group("vfx_targets")
    if not original_targets.is_empty():
        var live: Area2D = original_targets[0]
        var start: Vector2 = live.global_position + Vector2(-80,0)
        var live_resolution: Dictionary = G1.resolve_target(self, start, Vector2.RIGHT, start, 200.0)
        var real_effect: Area2D = G1.acquire(parent, kit, start, live_resolution, keeper)
        await wait_effect(real_effect)
        var real_contacts: Array = G1.events.filter(func(e): return e.event == "contact" and e.effect_id == real_effect.effect_id)
        measurements["live_dummy_contacts"] = real_contacts.size()
        check(real_contacts.size() == 1, "live dummy footprint collision")
    # The picker still changes only future releases.
    await process_frame
    var old_kit: int = keeper.vfx_kit_index
    var event := InputEventKey.new()
    event.physical_keycode = KEY_TAB
    event.pressed = true
    Input.parse_input_event(event)
    Input.flush_buffered_events()
    keeper._physics_process(0.0)
    event = InputEventKey.new()
    event.physical_keycode = KEY_TAB
    event.pressed = false
    Input.parse_input_event(event)
    Input.flush_buffered_events()
    check(keeper.vfx_kit_index == (old_kit+1) % keeper.VFX_KITS.size(), "Tab picker cycles")
    check(keeper.vfx_label.text.begins_with("VFX: " + keeper.VFX_KITS[keeper.vfx_kit_index].name), "Tab label follows selection")
    finish()
func finish() -> void:
    DirAccess.make_dir_recursive_absolute("res://out")
    var file := FileAccess.open("res://out/events.json", FileAccess.WRITE)
    file.store_string(JSON.stringify(G1.events, "  "))
    file.close()
    file = FileAccess.open("res://out/probe_vfx.json", FileAccess.WRITE)
    file.store_string(JSON.stringify({"measurements": measurements, "errors": errors}, "  "))
    file.close()
    print("G1_RUNTIME=" + JSON.stringify({"measurements": measurements, "errors": errors}))
    if errors.is_empty(): print("T3O_RUNTIME_ASSERTIONS=complete")
    quit(0 if errors.is_empty() else 7)
