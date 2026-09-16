extends SceneTree
const G1 = preload("res://scripts/vfx_g1.gd")
var report: Dictionary = {"halo":[],"release":[],"flight":[],"expiry":[]}
var keeper: CharacterBody2D
var scene: Node2D
var boxes: Dictionary = {"S":Rect2(228,160,70,240),"SW":Rect2(218,170,82,230),"W":Rect2(205,165,89,235),"NW":Rect2(209,165,85,235),"N":Rect2(218,166,75,234),"NE":Rect2(227,165,80,235),"E":Rect2(222,164,78,236),"SE":Rect2(221,164,88,236)}
func _initialize() -> void: call_deferred("run")
func inventory(node: Node) -> Dictionary:
    var counts: Dictionary = {"burst_pieces":0,"floor_lights":0,"impacts":0}
    if node is CanvasItem and node.is_visible_in_tree():
        if String(node.name).begins_with("Piece_"): counts.burst_pieces += 1
        if node.name == "FloorLight": counts.floor_lights += 1
    if String(node.scene_file_path).ends_with("_impact.tscn"): counts.impacts += 1
    for child in node.get_children():
        var sub: Dictionary = inventory(child)
        for key in counts: counts[key] += sub[key]
    return counts
func run() -> void:
    scene = load("res://scenes/main.tscn").instantiate()
    root.add_child(scene)
    keeper = scene.get_node("Keeper")
    keeper.set_physics_process(false)
    keeper.set_process(false)
    keeper.global_position = Vector2(3760,640)
    keeper.sprite.scale = Vector2.ONE * (130.0/240.0)
    await physics_frame
    await process_frame
    for kit_name in ["fire_bolt_e1_B","fire_bolt_e1_A","ice_bolt_e2"]:
        var ki: int = 0
        for i in range(keeper.VFX_KITS.size()):
            if keeper.VFX_KITS[i].name == kit_name: ki = i
        for facing in keeper.DIRECTIONS:
            keeper.state = "idle"
            keeper.facing = facing
            keeper.cast_kit_index = ki
            keeper.cast_fired = false
            keeper.sprite.animation = "cast_"+facing
            keeper.sprite.pause()
            keeper.sprite.frame = 0
            keeper.state = "cast"
            keeper.vfx_cursor_override = keeper.global_position + keeper.FACING_VECTORS[facing].normalized()*2000.0
            keeper.halo_start_tick = -1
            for tick in range(9):
                keeper.sprite.frame = tick/3
                keeper._physics_process(0.0)
                var halo: Sprite2D = keeper.cast_halo
                var socket: Vector2 = keeper._socket_world()
                report.halo.append({"kit":kit_name,"direction":facing,"tick":tick,"frame":keeper.sprite.frame,
                    "texture_class":halo.texture.get_class(),"is_head_texture":halo.texture.resource_path == keeper.VFX_KITS[ki].painted_travel.head.png,
                    "diameter_bh":halo.texture.get_width()*halo.global_scale.x/130.0,"position_error_px":halo.global_position.distance_to(socket),
                    "alpha":halo.modulate.a,"additive":halo.material.blend_mode == CanvasItemMaterial.BLEND_MODE_ADD})
                await physics_frame
                await process_frame
            keeper.sprite.frame = 3
            keeper._cast_frame_changed()
            var pool: Array = get_nodes_in_group("vfx_g1_pool")
            var bolt: Area2D = pool[-1]
            bolt.set_physics_process(false)
            var head: AnimatedSprite2D = bolt.get_node("Head")
            var point: Array = bolt.config.painted_travel.head.rear_socket
            var rear: Vector2 = head.to_global(head.offset + Vector2(point[0],point[1]))
            var derived: Vector2 = keeper._socket_world()
            report.release.append({"kit":kit_name,"direction":facing,"rear_error_px":rear.distance_to(derived),
                "facing_dot_px":(bolt.global_position-keeper.global_position).dot(keeper.FACING_VECTORS[facing].normalized()),
                "socket_world":[derived.x,derived.y],"bolt_position":[bolt.global_position.x,bolt.global_position.y],"halo_visible":keeper.cast_halo.visible})
            var max_counts: Dictionary = {"burst_pieces":0,"floor_lights":0,"impacts":0}
            for tick in range(60):
                var painting: Node2D = bolt.get_node("KeyState") if bolt.get_node("KeyState").visible else head
                var tex: Texture2D = painting.texture if painting is Sprite2D else bolt.rest_head
                var box: Rect2 = tex.get_image().get_used_rect()
                var centre: Vector2 = painting.to_global(painting.offset+box.get_center())
                var local: Vector2 = keeper.sprite.to_local(centre)-keeper.sprite.offset
                if painting.visible:
                    report.flight.append({"kit":kit_name,"direction":facing,"tick":tick,"head_centre_in_body":boxes[facing].has_point(local),"local_centre":[local.x,local.y]})
                var counts: Dictionary = inventory(scene)
                for key in counts: max_counts[key] = maxi(max_counts[key],counts[key])
                bolt._physics_process(1.0/60.0)
                await physics_frame
                await process_frame
            report.expiry.append({"kit":kit_name,"direction":facing,"distance_px":bolt.distance,"fizzle":bolt.fizzle_trace.duplicate(true),"max_visible":max_counts,"strike_fired":bolt.strike_fired,"contacts":bolt.contacted.size(),"events":G1.events.duplicate(true)})
            G1.events.clear()
            bolt.queue_free()
            for child in scene.get_children():
                if String(child.scene_file_path).ends_with("_impact.tscn"): child.queue_free()
            keeper.state = "idle"
            keeper._update_cast_halo()
            await process_frame
    var output := FileAccess.open("res://fl1_trace.json",FileAccess.WRITE)
    output.store_string(JSON.stringify(report))
    print("FL1_TRACE_COMPLETE")
    quit()
