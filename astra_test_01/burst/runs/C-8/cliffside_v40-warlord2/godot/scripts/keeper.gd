extends CharacterBody2D

const DIRECTIONS = ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]
@export var walk_speed: float = 150.0
@export var run_speed: float = 250.0
# Offset relative to the registered feet pivot. Calibrate for production art.
@export var staff_tip_offset: Vector2 = Vector2(0, -160)
@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D
var base_frames: SpriteFrames
var advanced_frames: SpriteFrames
var frost_frames: SpriteFrames
var facing: String = "S"
var state: String = "idle"
var warned: Dictionary = {}
var fallback_remaining: float = -1.0
var whirlwind: Node2D

func _ready() -> void:
    _load_directional_kit()
    _load_vfx_picker()
    add_to_group("vfx_actors")
    base_frames = sprite.sprite_frames
    if ResourceLoader.exists("res://frames/keeper_advanced.tres"):
        advanced_frames = load("res://frames/keeper_advanced.tres")
    if ResourceLoader.exists("res://vfx/frost_bolt.tres"):
        frost_frames = load("res://vfx/frost_bolt.tres")
    sprite.animation_finished.connect(_animation_finished)
    _play_state()
    # PATCH(drax whirlwind_patch): Eye of Reckoning whirlwind VFX
    whirlwind = preload("res://scripts/whirlwind.gd").new()
    whirlwind.name = "Whirlwind"
    add_child(whirlwind)
    whirlwind.bind(sprite)

func _physics_process(delta: float) -> void:
    _update_cast_halo()
    if Input.is_action_just_pressed("vfx_cycle"):
        vfx_kit_index = (vfx_kit_index + 1) % VFX_KITS.size()
        _update_vfx_label()
    if Input.is_action_just_pressed("gear_toggle") and advanced_frames != null:
        sprite.sprite_frames = advanced_frames if sprite.sprite_frames == base_frames else base_frames
        _play_state()
    if state == "jump" or state == "cast":
        velocity = Vector2.ZERO
        if fallback_remaining >= 0.0:
            fallback_remaining -= delta
            if fallback_remaining <= 0.0:
                _animation_finished()
        return
    # PATCH(drax attack_patch): attack state
    if state == "attack":
        if not Input.is_action_pressed("attack"):
            state = "idle"
            if whirlwind != null:
                whirlwind.end()
            _play_state()
            return
        # PATCH(drax attack_patch A2): the whirlwind TRAVELS, at walk pace.
        # run_modifier is deliberately IGNORED -- the spin costs you your
        # sprint, which is the trade D2 Whirlwind and PoE Cyclone both make.
        # No direction held leaves velocity zero, i.e. exactly the old gate.
        # The animation does NOT change to walk: attack_<DIR> keeps playing and
        # he translates while spinning. The attack frames were drawn feet-
        # planted, so he foot-skates; that is known and accepted at 2.5 rev/s.
        var spin_vector: Vector2 = Input.get_vector("move_left", "move_right", "move_up", "move_down")
        var spin_facing: String = facing
        if spin_vector.length_squared() > 0.0:
            spin_facing = DIRECTIONS[posmod(roundi(spin_vector.angle() / (PI / 4.0)) + 6, 8)]
        velocity = spin_vector * walk_speed
        move_and_slide()
        if spin_facing != facing:
            # Phase-preserving cell switch. Every attack_<DIR> cell is the SAME
            # eight stills rolled by the direction index (C-8 TURNAROUND-AS-
            # SPIN), so carrying the frame by the index delta keeps the
            # IDENTICAL still on screen and the revolution does not hitch when
            # he turns. Without it _play_state() restarts at frame 0 and the
            # spin jumps on every direction change -- which, now that he walks
            # while spinning, is constantly.
            var carry_frame: int = sprite.frame
            var carry_progress: float = sprite.get_frame_progress()
            var carry_delta: int = DIRECTIONS.find(facing) - DIRECTIONS.find(spin_facing)
            facing = spin_facing
            _play_state()
            if sprite.sprite_frames.get_frame_count(sprite.animation) == 8:
                sprite.set_frame_and_progress(posmod(carry_frame + carry_delta, 8), carry_progress)
        else:
            _play_state()
        return
    var input_vector: Vector2 = Input.get_vector("move_left", "move_right", "move_up", "move_down")
    if input_vector.length_squared() > 0.0:
        facing = DIRECTIONS[posmod(roundi(input_vector.angle() / (PI / 4.0)) + 6, 8)]
    if Input.is_action_just_pressed("cast"):
        cast_kit_index = vfx_kit_index
        cast_fired = false
        state = "cast"
        velocity = Vector2.ZERO
        _play_state()
        _update_cast_halo()
        _cast_frame_changed()
        return
    if Input.is_action_just_pressed("jump"):
        state = "jump"
        velocity = Vector2.ZERO
        _play_state()
        return
    if Input.is_action_just_pressed("attack"):
        state = "attack"
        velocity = Vector2.ZERO
        _play_state()
        if whirlwind != null:
            whirlwind.begin()
        return
    state = "idle" if input_vector == Vector2.ZERO else ("run" if Input.is_action_pressed("run_modifier") else "walk")
    velocity = input_vector * (run_speed if state == "run" else walk_speed)
    move_and_slide()
    _play_state()

func _nearest_animation(kind: String) -> String:
    var best: String = ""
    var best_distance: int = 99
    var wanted: int = DIRECTIONS.find(facing)
    for index in range(8):
        var candidate: String = kind + "_" + DIRECTIONS[index]
        var distance: int = absi(index - wanted)
        distance = mini(distance, 8 - distance)
        if sprite.sprite_frames.has_animation(candidate) and distance < best_distance:
            best = candidate
            best_distance = distance
    return best

func _play_state() -> void:
    var requested: String = state + "_" + facing
    var chosen: String = _nearest_animation(state)
    if chosen.is_empty():
        chosen = _nearest_animation("idle")
    if chosen.is_empty():
        # Entire state and idle absent: nearest direction across other states.
        var best_distance: int = 99
        var wanted: int = DIRECTIONS.find(facing)
        for kind in ["walk", "run", "jump", "cast", "attack"]:
            var candidate: String = _nearest_animation(kind)
            if not candidate.is_empty():
                var index: int = DIRECTIONS.find(candidate.get_slice("_", 1))
                var distance: int = absi(index - wanted)
                distance = mini(distance, 8 - distance)
                if distance < best_distance:
                    chosen = candidate
                    best_distance = distance
    if chosen != requested and not warned.has(requested):
        print("Missing animation ", requested, "; using ", chosen)
        warned[requested] = true
    if sprite.animation != chosen or not sprite.is_playing():
        sprite.play(chosen)
    fallback_remaining = -1.0
    if (state == "jump" or state == "cast") and sprite.sprite_frames.get_animation_loop(chosen):
        fallback_remaining = float(sprite.sprite_frames.get_frame_count(chosen)) / sprite.sprite_frames.get_animation_speed(chosen)

func _animation_finished() -> void:
    if state == "jump" or state == "cast":
        state = "idle"
        fallback_remaining = -1.0
        _play_state()

func _spawn_frost() -> void:
    if frost_frames == null:
        return
    var effect := AnimatedSprite2D.new()
    effect.sprite_frames = frost_frames
    get_parent().add_child(effect)
    effect.global_position = global_position + staff_tip_offset
    var names: PackedStringArray = frost_frames.get_animation_names()
    var animation_name: String = "cast" if frost_frames.has_animation("cast") else names[0]
    effect.animation_finished.connect(effect.queue_free, CONNECT_ONE_SHOT)
    effect.play(animation_name)
    # Also clean up a supplied looping travel-only effect.
    if frost_frames.get_animation_loop(animation_name):
        get_tree().create_timer(1.0).timeout.connect(func():
            if is_instance_valid(effect):
                effect.queue_free())

# Directional kit: sockets refer to the actual displayed animation/frame.
var socket_cells: Dictionary = {}
var cast_ready: bool = false
var vfx_cursor_override: Variant = null
const TOUCH_OVERLAY_BAND = 0.22
var vfx_force_touch_device: bool = false
const G1 = preload("res://scripts/vfx_g1.gd")
const G4 = preload("res://scripts/vfx_g4.gd")
const G3 = preload("res://scripts/vfx_g3.gd")
const G2 = preload("res://scripts/vfx_g2.gd")
var cast_fired: bool = false
var active_flare: AnimatedSprite2D
const FACING_VECTORS = {"S": Vector2(0,1), "SW": Vector2(-1,1),
    "W": Vector2(-1,0), "NW": Vector2(-1,-1), "N": Vector2(0,-1),
    "NE": Vector2(1,-1), "E": Vector2(1,0), "SE": Vector2(1,1)}

func _load_directional_kit() -> void:
    var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://sockets.json"))
    socket_cells = data.cells
    sprite.frame_changed.connect(_cast_frame_changed)
    get_tree().physics_frame.connect(_g1_cast_ready, CONNECT_ONE_SHOT)

func _socket_world() -> Variant:
    var cell: Dictionary = socket_cells.get(String(sprite.animation), {})
    var points: Array = cell.get("sockets", [])
    if sprite.frame >= points.size() or points[sprite.frame] == null:
        return null
    var point: Array = points[sprite.frame]
    var local: Vector2 = Vector2(point[0], point[1]) + sprite.offset
    if sprite.centered:
        local -= sprite.sprite_frames.get_frame_texture(sprite.animation, sprite.frame).get_size() / 2.0
    return sprite.to_global(local)

func _cast_frame_changed() -> void:
    if state != "cast" or cast_fired:
        return
    var cell: Dictionary = socket_cells.get(String(sprite.animation), {})
    if cell.is_empty() or sprite.frame != int(cell.release_index):
        return
    cast_fired = true
    if VFX_KITS[cast_kit_index].get("grammar", "") == "G4":
        if not cast_ready:
            await get_tree().physics_frame
        if is_inside_tree(): G4.acquire(self, VFX_KITS[cast_kit_index])
        return
    _update_cast_halo()
    var socket: Variant = _socket_world()
    if socket == null:
        push_warning("No measured release socket: " + String(sprite.animation))
        return
    var direction: Vector2 = FACING_VECTORS[facing].normalized()
    var art_scale: float = sprite.global_transform.x.length()
    if not VFX_KITS[cast_kit_index].has("painted_travel"):
        var flare := AnimatedSprite2D.new()
        flare.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
        flare.sprite_frames = load(VFX_KITS[cast_kit_index]["flare"])
        if cast_kit_index == 0:
            flare.material = load("res://vfx/frozen_orb/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_frozen_orb_material.gd").bind(flare, {"res://vfx/frozen_orb/sprites/flare/flare_00.png": "res://vfx/frozen_orb/distance/flare/flare_00.png", "res://vfx/frozen_orb/sprites/flare/flare_01.png": "res://vfx/frozen_orb/distance/flare/flare_01.png", "res://vfx/frozen_orb/sprites/flare/flare_02.png": "res://vfx/frozen_orb/distance/flare/flare_02.png", "res://vfx/frozen_orb/sprites/flare/flare_03.png": "res://vfx/frozen_orb/distance/flare/flare_03.png", "res://vfx/frozen_orb/sprites/flare/flare_04.png": "res://vfx/frozen_orb/distance/flare/flare_04.png", "res://vfx/frozen_orb/sprites/flare/flare_05.png": "res://vfx/frozen_orb/distance/flare/flare_05.png"})
            flare.set_meta("phase_scale", 1.0)
        elif cast_kit_index == 1:
            flare.material = load("res://vfx/blackwater_cocktail/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_blackwater_cocktail_material.gd").bind(flare, {"res://vfx/blackwater_cocktail/sprites/flare/flare_00.png": "res://vfx/blackwater_cocktail/distance/flare/flare_00.png", "res://vfx/blackwater_cocktail/sprites/flare/flare_01.png": "res://vfx/blackwater_cocktail/distance/flare/flare_01.png", "res://vfx/blackwater_cocktail/sprites/flare/flare_02.png": "res://vfx/blackwater_cocktail/distance/flare/flare_02.png", "res://vfx/blackwater_cocktail/sprites/flare/flare_03.png": "res://vfx/blackwater_cocktail/distance/flare/flare_03.png", "res://vfx/blackwater_cocktail/sprites/flare/flare_04.png": "res://vfx/blackwater_cocktail/distance/flare/flare_04.png", "res://vfx/blackwater_cocktail/sprites/flare/flare_05.png": "res://vfx/blackwater_cocktail/distance/flare/flare_05.png"})
            flare.set_meta("phase_scale", 1.0)
        elif cast_kit_index == 2:
            flare.material = load("res://vfx/poisonous_concoction/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_poisonous_concoction_material.gd").bind(flare, {"res://vfx/poisonous_concoction/sprites/flare/flare_00.png": "res://vfx/poisonous_concoction/distance/flare/flare_00.png", "res://vfx/poisonous_concoction/sprites/flare/flare_01.png": "res://vfx/poisonous_concoction/distance/flare/flare_01.png", "res://vfx/poisonous_concoction/sprites/flare/flare_02.png": "res://vfx/poisonous_concoction/distance/flare/flare_02.png", "res://vfx/poisonous_concoction/sprites/flare/flare_03.png": "res://vfx/poisonous_concoction/distance/flare/flare_03.png", "res://vfx/poisonous_concoction/sprites/flare/flare_04.png": "res://vfx/poisonous_concoction/distance/flare/flare_04.png", "res://vfx/poisonous_concoction/sprites/flare/flare_05.png": "res://vfx/poisonous_concoction/distance/flare/flare_05.png"})
            flare.set_meta("phase_scale", 1.0)
        elif cast_kit_index == 3:
            flare.material = load("res://vfx/lightning_blast/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_lightning_blast_material.gd").bind(flare, {"res://vfx/lightning_blast/sprites/flare/flare_00.png": "res://vfx/lightning_blast/distance/flare/flare_00.png", "res://vfx/lightning_blast/sprites/flare/flare_01.png": "res://vfx/lightning_blast/distance/flare/flare_01.png", "res://vfx/lightning_blast/sprites/flare/flare_02.png": "res://vfx/lightning_blast/distance/flare/flare_02.png", "res://vfx/lightning_blast/sprites/flare/flare_03.png": "res://vfx/lightning_blast/distance/flare/flare_03.png", "res://vfx/lightning_blast/sprites/flare/flare_04.png": "res://vfx/lightning_blast/distance/flare/flare_04.png", "res://vfx/lightning_blast/sprites/flare/flare_05.png": "res://vfx/lightning_blast/distance/flare/flare_05.png"})
            flare.set_meta("phase_scale", 1.0)
        elif cast_kit_index == 4:
            flare.material = load("res://vfx/zeus_chain/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_zeus_chain_material.gd").bind(flare, {"res://vfx/zeus_chain/sprites/flare/flare_00.png": "res://vfx/zeus_chain/distance/flare/flare_00.png", "res://vfx/zeus_chain/sprites/flare/flare_01.png": "res://vfx/zeus_chain/distance/flare/flare_01.png", "res://vfx/zeus_chain/sprites/flare/flare_02.png": "res://vfx/zeus_chain/distance/flare/flare_02.png", "res://vfx/zeus_chain/sprites/flare/flare_03.png": "res://vfx/zeus_chain/distance/flare/flare_03.png", "res://vfx/zeus_chain/sprites/flare/flare_04.png": "res://vfx/zeus_chain/distance/flare/flare_04.png", "res://vfx/zeus_chain/sprites/flare/flare_05.png": "res://vfx/zeus_chain/distance/flare/flare_05.png"})
            flare.set_meta("phase_scale", 1.0)
        elif cast_kit_index == 5:
            flare.material = load("res://vfx/healing_hands/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_healing_hands_material.gd").bind(flare, {"res://vfx/healing_hands/sprites/flare/flare_00.png": "res://vfx/healing_hands/distance/flare/flare_00.png", "res://vfx/healing_hands/sprites/flare/flare_01.png": "res://vfx/healing_hands/distance/flare/flare_01.png", "res://vfx/healing_hands/sprites/flare/flare_02.png": "res://vfx/healing_hands/distance/flare/flare_02.png", "res://vfx/healing_hands/sprites/flare/flare_03.png": "res://vfx/healing_hands/distance/flare/flare_03.png", "res://vfx/healing_hands/sprites/flare/flare_04.png": "res://vfx/healing_hands/distance/flare/flare_04.png", "res://vfx/healing_hands/sprites/flare/flare_05.png": "res://vfx/healing_hands/distance/flare/flare_05.png"})
            flare.set_meta("phase_scale", 1.0)
        elif cast_kit_index == 6:
            flare.material = load("res://vfx/fire_burst_e0p/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_fire_burst_e0p_material.gd").bind(flare, {"res://vfx/fire_burst_e0p/sprites/flare/flare_00.png": "res://vfx/fire_burst_e0p/distance/flare/flare_00.png"})
            flare.set_meta("phase_scale", 1.0)
        elif cast_kit_index == 7:
            flare.material = load("res://vfx/fire_burst_e0p_v2/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_fire_burst_e0p_v2_material.gd").bind(flare, {"res://vfx/fire_burst_e0p_v2/sprites/flare/flare_00.png": "res://vfx/fire_burst_e0p_v2/distance/flare/flare_00.png"})
            flare.set_meta("phase_scale", 1.0)
        elif cast_kit_index == 8:
            flare.material = load("res://vfx/fire_bolt_e1_A/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_fire_bolt_e1_A_material.gd").bind(flare, {"res://vfx/fire_bolt_e1_A/sprites/flare/flare_00.png": "res://vfx/fire_bolt_e1_A/distance/flare/flare_00.png"})
            flare.set_meta("phase_scale", 1.0)
        elif cast_kit_index == 9:
            flare.material = load("res://vfx/fire_bolt_e1_B/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_fire_bolt_e1_B_material.gd").bind(flare, {"res://vfx/fire_bolt_e1_B/sprites/flare/flare_00.png": "res://vfx/fire_bolt_e1_B/distance/flare/flare_00.png"})
            flare.set_meta("phase_scale", 1.0)
        elif cast_kit_index == 10:
            flare.material = load("res://vfx/ice_bolt_e2/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_ice_bolt_e2_material.gd").bind(flare, {"res://vfx/ice_bolt_e2/sprites/flare/flare_00.png": "res://vfx/ice_bolt_e2/distance/flare/flare_00.png"})
            flare.set_meta("phase_scale", 1.0)
        elif cast_kit_index == 11:
            flare.material = load("res://vfx/blackwater_cocktail_e3/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_blackwater_cocktail_e3_material.gd").bind(flare, {})
            flare.set_meta("phase_scale", 1.0)
        elif cast_kit_index == 12:
            flare.material = load("res://vfx/poisonous_concoction_e3/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_poisonous_concoction_e3_material.gd").bind(flare, {})
            flare.set_meta("phase_scale", 1.0)
        elif cast_kit_index == 13:
            flare.material = load("res://vfx/lightning_blast_e3/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_lightning_blast_e3_material.gd").bind(flare, {})
            flare.set_meta("phase_scale", 1.0)
        elif cast_kit_index == 14:
            flare.material = load("res://vfx/zeus_chain_e3/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_zeus_chain_e3_material.gd").bind(flare, {})
            flare.set_meta("phase_scale", 1.0)
        elif cast_kit_index == 15:
            flare.material = load("res://vfx/healing_hands_e3/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_healing_hands_e3_material.gd").bind(flare, {})
            flare.set_meta("phase_scale", 1.0)
        elif cast_kit_index == 16:
            flare.material = load("res://vfx/frozen_orb_e3/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_frozen_orb_e3_material.gd").bind(flare, {"res://vfx/frozen_orb_e3/sprites/flare/flare_00.png": "res://vfx/frozen_orb_e3/distance/flare/flare_00.png"})
            flare.set_meta("phase_scale", 1.0)
        elif cast_kit_index == 17:
            flare.material = load("res://vfx/fire_burst_e0p_v3/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_fire_burst_e0p_v3_material.gd").bind(flare, {"res://vfx/fire_burst_e0p_v3/sprites/flare/flare_00.png": "res://vfx/fire_burst_e0p_v3/distance/flare/flare_00.png"})
            flare.set_meta("phase_scale", 1.0)
        elif cast_kit_index == 18:
            flare.material = load("res://vfx/blackwater_cocktail_e3_V/materials/Additive.tres")
            flare.animation = &"flare"
            preload("res://scripts/vfx_blackwater_cocktail_e3_V_material.gd").bind(flare, {})
            flare.set_meta("phase_scale", 1.0)
        else:
            var additive := CanvasItemMaterial.new()
            additive.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
            flare.material = additive
        get_parent().add_child(flare)
        flare.global_position = socket
        flare.rotation = direction.angle()
        flare.scale = Vector2.ONE * (1.0 if bool(VFX_KITS[cast_kit_index].get("screen_px", false)) else art_scale) * float(flare.get_meta("phase_scale", 1.0))
        flare.animation_finished.connect(flare.queue_free, CONNECT_ONE_SHOT)
        flare.play("flare")
        active_flare = flare
    var kit: Dictionary = VFX_KITS[cast_kit_index].duplicate(true)
    var aim_scale: float = 1.0 if bool(kit.get("screen_px", false)) else art_scale
    var destination: Dictionary
    if kit.get("grammar", "G1") == "G2":
        var cursor: Vector2 = get_global_mouse_position() if vfx_cursor_override == null else vfx_cursor_override
        var touch: bool = vfx_cursor_override == null and (vfx_force_touch_device or DisplayServer.is_touchscreen_available())
        destination = G2.resolve_ground(global_position, FACING_VECTORS[facing], cursor, float(kit.range_px), touch)
    else:
        # Device policy survives handled overlay touches and browser-emulated mouse.
        # The explicit probe hook keeps precedence; desktop resolution is unchanged.
        if vfx_cursor_override == null and (vfx_force_touch_device or DisplayServer.is_touchscreen_available()):
            var forward_point: Vector2 = global_position + FACING_VECTORS[facing].normalized() * float(kit.range_px) * aim_scale
            destination = {"point": forward_point, "target": null, "kind": "cursor"}
        else:
            var cursor: Vector2 = get_global_mouse_position() if vfx_cursor_override == null else vfx_cursor_override
            destination = G1.resolve_target(get_tree(), global_position, direction, cursor, float(kit.range_px) * aim_scale)
    if kit.get("grammar", "G1") == "G3":
        if not cast_ready:
            await get_tree().physics_frame
        if not is_inside_tree(): return
        var release_socket: Variant = _socket_world()
        if release_socket == null: return
        var instant_target: Dictionary = G3.resolve_target(get_tree(), release_socket, FACING_VECTORS[facing], float(kit.range_px), self)
        G3.acquire(get_parent(), kit, release_socket, instant_target, self, art_scale)
        return
    if not cast_ready:
        await get_tree().physics_frame
    if not is_inside_tree():
        return
    destination["facing"] = FACING_VECTORS[facing].normalized()
    if kit.get("grammar", "G1") == "G2":
        G2.acquire(get_parent(), kit, socket, destination, self, art_scale)
    else:
        G1.acquire(get_parent(), kit, socket, destination, self, art_scale)

func _g1_cast_ready() -> void:
    cast_ready = true

func _process(_delta: float) -> void:
    if state == "cast" and is_instance_valid(active_flare):
        var socket: Variant = _socket_world()
        if socket != null:
            active_flare.global_position = socket
 
var cast_halo: Sprite2D
var halo_start_tick: int = -1
func _update_cast_halo() -> void:
    var kit: Dictionary = VFX_KITS[cast_kit_index]
    var cell: Dictionary = socket_cells.get(String(sprite.animation), {})
    var live: bool = state == "cast" and not cast_fired and not cell.is_empty() and sprite.frame < int(cell.release_index) and kit.get("grammar", "G1") == "G1"
    if not live:
        if is_instance_valid(cast_halo): cast_halo.hide()
        halo_start_tick = -1
        return
    var socket: Variant = _socket_world()
    if socket == null: return
    if not is_instance_valid(cast_halo):
        cast_halo = Sprite2D.new()
        cast_halo.name = "CastHalo"
        var gradient := Gradient.new()
        gradient.offsets = PackedFloat32Array([0.0, 0.25, 1.0])
        gradient.colors = PackedColorArray([Color.WHITE, Color(1,1,1,0.7), Color(1,1,1,0)])
        var disc := GradientTexture2D.new()
        disc.gradient = gradient
        disc.width = 64
        disc.height = 64
        disc.fill = GradientTexture2D.FILL_RADIAL
        disc.fill_from = Vector2(0.5,0.5)
        disc.fill_to = Vector2(1.0,0.5)
        cast_halo.texture = disc
        var additive := CanvasItemMaterial.new()
        additive.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
        cast_halo.material = additive
        cast_halo.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
        add_child(cast_halo)
        cast_halo.top_level = true
    if halo_start_tick < 0: halo_start_tick = Engine.get_physics_frames()
    var duration: float = maxf(1.0, float(cell.release_index) * 60.0 / sprite.sprite_frames.get_animation_speed(sprite.animation) - 1.0)
    var t: float = clampf(float(Engine.get_physics_frames()-halo_start_tick)/duration, 0.0, 1.0)
    var bh: float = 130.0 if bool(kit.get("screen_px", false)) else 240.0 * sprite.global_transform.x.length()
    var pulse: float = 1.0 + 0.15 * sin(PI*t)
    cast_halo.scale = Vector2.ONE * (2.0 * 0.35 * bh / 64.0) * pulse
    var band: Array = kit.palette_2
    cast_halo.modulate = Color(band[0],band[1],band[2],lerpf(0.6,0.9,t))
    cast_halo.global_position = socket
    cast_halo.show()

const VFX_KITS = [{"name": "frozen_orb", "flare": "res://vfx/frozen_orb/flare.tres", "bolt": "res://scenes/vfx/g1_projectile.tscn", "head": "res://vfx/frozen_orb/travel.tres", "animation": "travel", "impact": "res://scenes/vfx_frozen_orb_impact.tscn", "speed_px_s": 640, "pierce": -1, "palette_3": [1.0, 1.0, 1.0, 1.0], "palette_2": [0.5019607843137255, 0.5254901960784314, 0.6705882352941176, 1.0], "range_px": 650.0, "ground_squash": 0.58, "phase_scale": 1, "material": "res://vfx/frozen_orb/materials/Body.tres", "binding": "res://scripts/vfx_frozen_orb_material.gd", "collision_radius_bh": 0.25, "head_length_px": 192, "fields": {"res://vfx/frozen_orb/sprites/travel/travel_00.png": "res://vfx/frozen_orb/distance/travel/travel_00.png", "res://vfx/frozen_orb/sprites/travel/travel_01.png": "res://vfx/frozen_orb/distance/travel/travel_01.png", "res://vfx/frozen_orb/sprites/travel/travel_02.png": "res://vfx/frozen_orb/distance/travel/travel_02.png", "res://vfx/frozen_orb/sprites/travel/travel_03.png": "res://vfx/frozen_orb/distance/travel/travel_03.png", "res://vfx/frozen_orb/sprites/travel/travel_04.png": "res://vfx/frozen_orb/distance/travel/travel_04.png", "res://vfx/frozen_orb/sprites/travel/travel_05.png": "res://vfx/frozen_orb/distance/travel/travel_05.png"}, "trail_color": [0.35, 0.65, 0.8, 0.6]}, {"name": "blackwater_cocktail", "flare": "res://vfx/blackwater_cocktail/flare.tres", "bolt": "res://scenes/vfx/g1_projectile.tscn", "head": "res://vfx/blackwater_cocktail/travel.tres", "animation": "travel", "impact": "res://scenes/vfx_blackwater_cocktail_impact.tscn", "speed_px_s": 480, "pierce": 0, "palette_3": [1.0, 1.0, 1.0, 1.0], "palette_2": [0.6352941176470588, 0.47843137254901963, 0.3686274509803922, 1.0], "range_px": 650.0, "ground_squash": 0.6, "phase_scale": 1, "material": "res://vfx/blackwater_cocktail/materials/Body.tres", "binding": "res://scripts/vfx_blackwater_cocktail_material.gd", "collision_radius_bh": 0.25, "head_length_px": 192, "fields": {"res://vfx/blackwater_cocktail/sprites/travel/travel_00.png": "res://vfx/blackwater_cocktail/distance/travel/travel_00.png", "res://vfx/blackwater_cocktail/sprites/travel/travel_01.png": "res://vfx/blackwater_cocktail/distance/travel/travel_01.png", "res://vfx/blackwater_cocktail/sprites/travel/travel_02.png": "res://vfx/blackwater_cocktail/distance/travel/travel_02.png", "res://vfx/blackwater_cocktail/sprites/travel/travel_03.png": "res://vfx/blackwater_cocktail/distance/travel/travel_03.png", "res://vfx/blackwater_cocktail/sprites/travel/travel_04.png": "res://vfx/blackwater_cocktail/distance/travel/travel_04.png", "res://vfx/blackwater_cocktail/sprites/travel/travel_05.png": "res://vfx/blackwater_cocktail/distance/travel/travel_05.png"}, "trail_color": [0.35, 0.65, 0.8, 0.6]}, {"name": "poisonous_concoction", "flare": "res://vfx/poisonous_concoction/flare.tres", "bolt": "res://scenes/vfx/g1_projectile.tscn", "head": "res://vfx/poisonous_concoction/travel.tres", "animation": "travel", "impact": "res://scenes/vfx_poisonous_concoction_impact.tscn", "speed_px_s": 420, "pierce": 0, "palette_3": [1.0, 1.0, 1.0, 1.0], "palette_2": [0.42745098039215684, 0.5882352941176471, 0.3843137254901961, 1.0], "range_px": 650.0, "ground_squash": 0.6, "phase_scale": 1, "material": "res://vfx/poisonous_concoction/materials/Body.tres", "binding": "res://scripts/vfx_poisonous_concoction_material.gd", "collision_radius_bh": 0.25, "head_length_px": 192, "fields": {"res://vfx/poisonous_concoction/sprites/travel/travel_00.png": "res://vfx/poisonous_concoction/distance/travel/travel_00.png", "res://vfx/poisonous_concoction/sprites/travel/travel_01.png": "res://vfx/poisonous_concoction/distance/travel/travel_01.png", "res://vfx/poisonous_concoction/sprites/travel/travel_02.png": "res://vfx/poisonous_concoction/distance/travel/travel_02.png", "res://vfx/poisonous_concoction/sprites/travel/travel_03.png": "res://vfx/poisonous_concoction/distance/travel/travel_03.png", "res://vfx/poisonous_concoction/sprites/travel/travel_04.png": "res://vfx/poisonous_concoction/distance/travel/travel_04.png", "res://vfx/poisonous_concoction/sprites/travel/travel_05.png": "res://vfx/poisonous_concoction/distance/travel/travel_05.png"}, "trail_color": [0.35, 0.65, 0.8, 0.6]}, {"name": "lightning_blast", "flare": "res://vfx/lightning_blast/flare.tres", "bolt": "res://scenes/vfx/g1_projectile.tscn", "head": "res://vfx/lightning_blast/travel.tres", "animation": "travel", "impact": "res://scenes/vfx_lightning_blast_impact.tscn", "speed_px_s": 1400, "pierce": 0, "palette_3": [1.0, 1.0, 1.0, 1.0], "palette_2": [0.5529411764705883, 0.5372549019607843, 0.6705882352941176, 1.0], "range_px": 650.0, "ground_squash": 0.6, "phase_scale": 1, "material": "res://vfx/lightning_blast/materials/Body.tres", "binding": "res://scripts/vfx_lightning_blast_material.gd", "collision_radius_bh": 0.25, "head_length_px": 192, "fields": {"res://vfx/lightning_blast/sprites/travel/travel_00.png": "res://vfx/lightning_blast/distance/travel/travel_00.png", "res://vfx/lightning_blast/sprites/travel/travel_01.png": "res://vfx/lightning_blast/distance/travel/travel_01.png", "res://vfx/lightning_blast/sprites/travel/travel_02.png": "res://vfx/lightning_blast/distance/travel/travel_02.png", "res://vfx/lightning_blast/sprites/travel/travel_03.png": "res://vfx/lightning_blast/distance/travel/travel_03.png", "res://vfx/lightning_blast/sprites/travel/travel_04.png": "res://vfx/lightning_blast/distance/travel/travel_04.png", "res://vfx/lightning_blast/sprites/travel/travel_05.png": "res://vfx/lightning_blast/distance/travel/travel_05.png"}, "trail_color": [0.35, 0.65, 0.8, 0.6]}, {"name": "zeus_chain", "flare": "res://vfx/zeus_chain/flare.tres", "bolt": "res://scenes/vfx/g1_projectile.tscn", "head": "res://vfx/zeus_chain/travel.tres", "animation": "travel", "impact": "res://scenes/vfx_zeus_chain_impact.tscn", "speed_px_s": 1400, "pierce": 0, "palette_3": [1.0, 1.0, 1.0, 1.0], "palette_2": [0.5803921568627451, 0.5529411764705883, 0.592156862745098, 1.0], "range_px": 650.0, "ground_squash": 0.6, "phase_scale": 1, "material": "res://vfx/zeus_chain/materials/Body.tres", "binding": "res://scripts/vfx_zeus_chain_material.gd", "collision_radius_bh": 0.25, "head_length_px": 192, "fields": {"res://vfx/zeus_chain/sprites/travel/travel_00.png": "res://vfx/zeus_chain/distance/travel/travel_00.png", "res://vfx/zeus_chain/sprites/travel/travel_01.png": "res://vfx/zeus_chain/distance/travel/travel_01.png", "res://vfx/zeus_chain/sprites/travel/travel_02.png": "res://vfx/zeus_chain/distance/travel/travel_02.png", "res://vfx/zeus_chain/sprites/travel/travel_03.png": "res://vfx/zeus_chain/distance/travel/travel_03.png", "res://vfx/zeus_chain/sprites/travel/travel_04.png": "res://vfx/zeus_chain/distance/travel/travel_04.png", "res://vfx/zeus_chain/sprites/travel/travel_05.png": "res://vfx/zeus_chain/distance/travel/travel_05.png"}, "trail_color": [0.35, 0.65, 0.8, 0.6]}, {"name": "healing_hands", "flare": "res://vfx/healing_hands/flare.tres", "bolt": "res://scenes/vfx/g1_projectile.tscn", "head": "res://vfx/healing_hands/travel.tres", "animation": "travel", "impact": "res://scenes/vfx_healing_hands_impact.tscn", "speed_px_s": 520, "pierce": 0, "palette_3": [1.0, 1.0, 1.0, 1.0], "palette_2": [0.6549019607843137, 0.5686274509803921, 0.4666666666666667, 1.0], "range_px": 650.0, "ground_squash": 0.6, "phase_scale": 1, "material": "res://vfx/healing_hands/materials/Body.tres", "binding": "res://scripts/vfx_healing_hands_material.gd", "collision_radius_bh": 0.25, "head_length_px": 192, "fields": {"res://vfx/healing_hands/sprites/travel/travel_00.png": "res://vfx/healing_hands/distance/travel/travel_00.png", "res://vfx/healing_hands/sprites/travel/travel_01.png": "res://vfx/healing_hands/distance/travel/travel_01.png", "res://vfx/healing_hands/sprites/travel/travel_02.png": "res://vfx/healing_hands/distance/travel/travel_02.png", "res://vfx/healing_hands/sprites/travel/travel_03.png": "res://vfx/healing_hands/distance/travel/travel_03.png", "res://vfx/healing_hands/sprites/travel/travel_04.png": "res://vfx/healing_hands/distance/travel/travel_04.png", "res://vfx/healing_hands/sprites/travel/travel_05.png": "res://vfx/healing_hands/distance/travel/travel_05.png"}, "trail_color": [0.35, 0.65, 0.8, 0.6]}, {"name": "fire_burst_e0p", "flare": "res://vfx/fire_burst_e0p/flare.tres", "bolt": "res://scenes/vfx/g1_projectile.tscn", "head": "res://vfx/fire_burst_e0p/travel.tres", "animation": "travel", "impact": "res://scenes/vfx_fire_burst_e0p_impact.tscn", "speed_px_s": 640, "pierce": 0, "palette_3": [1, 0.94, 0.75, 1], "palette_2": [1, 0.55, 0.12, 1], "range_px": 650.0, "ground_squash": 1.0, "phase_scale": 1.0, "material": "res://vfx/fire_burst_e0p/materials/Body.tres", "binding": "res://scripts/vfx_fire_burst_e0p_material.gd", "collision_radius_bh": 0.25, "head_length_px": 12.0, "fields": {"res://vfx/fire_burst_e0p/sprites/travel/travel_00.png": "res://vfx/fire_burst_e0p/distance/travel/travel_00.png"}, "trail_color": [0.35, 0.65, 0.8, 0.6]}, {"screen_px": true, "name": "fire_burst_e0p_v2", "flare": "res://vfx/fire_burst_e0p_v2/flare.tres", "bolt": "res://scenes/vfx/g1_projectile.tscn", "head": "res://vfx/fire_burst_e0p_v2/travel.tres", "animation": "travel", "impact": "res://scenes/vfx_fire_burst_e0p_v2_impact.tscn", "speed_px_s": 640, "pierce": 0, "palette_3": [1, 0.94, 0.75, 1], "palette_2": [1, 0.55, 0.12, 1], "range_px": 650.0, "ground_squash": 1.0, "phase_scale": 1.0, "material": "res://vfx/fire_burst_e0p_v2/materials/Body.tres", "binding": "res://scripts/vfx_fire_burst_e0p_v2_material.gd", "collision_radius_bh": 0.25, "head_length_px": 12.0, "fields": {"res://vfx/fire_burst_e0p_v2/sprites/travel/travel_00.png": "res://vfx/fire_burst_e0p_v2/distance/travel/travel_00.png"}, "trail_color": [0.35, 0.65, 0.8, 0.6]}, {"screen_px": true, "name": "fire_bolt_e1_A", "flare": "res://vfx/fire_bolt_e1_A/flare.tres", "bolt": "res://scenes/vfx/g1_fl4_projectile.tscn", "head": "res://vfx/fire_bolt_e1_A/travel.tres", "animation": "travel", "impact": "res://scenes/vfx_fire_burst_e0p_v2_impact.tscn", "speed_px_s": 1510, "pierce": 0, "palette_3": [1, 0.94, 0.75, 1], "palette_2": [1, 0.55, 0.12, 1], "range_px": 520, "ground_squash": 0.6, "phase_scale": 1.0, "material": "res://vfx/fire_bolt_e1_A/materials/Body.tres", "binding": "res://scripts/vfx_fire_bolt_e1_A_material.gd", "collision_radius_bh": 0.25, "head_length_px": 74.66383117615416, "fields": {"res://vfx/fire_bolt_e1_A/sprites/travel/travel_00.png": "res://vfx/fire_bolt_e1_A/distance/travel/travel_00.png"}, "trail_color": [0.35, 0.65, 0.8, 0.6], "fire_layers": {"dark_duplicate": true, "glow": {"alpha": 0.2, "scale": 1.02, "peak": {"alpha": 0.35, "scale": 1.06}}, "floor_light": {"radius_px": 160, "duration_s": 0.35, "curve": "ease_out", "tint": "palette_2", "alpha": 0.6}, "flash": {"duration_s": 0.03333333333333333, "alpha": 0.8, "scale_from": 1.04, "scale_to": 1}, "cast": {"muzzle_puff": {"scale": 0.45, "frames": 4}, "floor_light": {"radius_bh": 0.8, "frames": 6, "alpha": 0.5}}, "travel": {"flicker_frames": 2, "trail": {"rate_per_s": 12, "size_px": [3, 5], "life_s": 0.45, "rise_px_s": 30, "lateral_px": 10, "bands": [3, 2]}, "erode_noise": 0.3, "core": {"band": 3, "alpha": 0.7, "blur_px": 4, "pulse_scale": 1.08, "hz": 8}, "halo": {"alpha": 0.3, "scale": 1.2}, "boil": {"uv_per_s": 0.5, "erode_amp": 0.08, "hz": 8}, "smear": {"band": 2, "alpha": 0.2, "length_bh": 1, "frames": 6}, "eruption": {"frames": 8, "scale_from": 0.25, "sheet_delay_frames": 3}}, "core": {"band": 3, "alpha": 0.55, "blur_px": 6}, "contact_light": {"lerp": 0.45, "frames": 6}, "shimmer": {"amplitude_px": 3, "seconds": 0.8}}, "palette": [[0.25, 0.08, 0.04, 1], [0.7, 0.16, 0.08, 1], [1, 0.55, 0.12, 1], [1, 0.94, 0.75, 1]], "spec_speed_px_s": 1510, "contact_only": true, "grammar": "G1", "aim_rule": "release-locked", "termination": "first_contact_or_range", "range_expiry": "burst", "origin_socket": "cast_release", "seed": 2026, "painted_travel": {"head": {"binding": "P01_fire_head", "png": "res://vfx/fire_bolt_e1_A/primitives/head.png", "pivot": [334, 273], "scale": 0.7926829268292683, "rear_socket": [240, 267], "material": "res://vfx/fire_bolt_e1_A/materials/Travel_head.tres", "fizzle_material": "res://vfx/fire_bolt_e1_A/materials/Fizzle_head.tres"}, "streak": {"binding": "P02_fire_streak", "png": "res://vfx/fire_bolt_e1_A/primitives/streak.png", "pivot": [405, 274], "scale": 0.7138728323699421, "material": "res://vfx/fire_bolt_e1_A/materials/Travel_streak.tres"}, "rest_hold_frames": 3, "tail_s": 0.15}, "head_extent_bh": 1.0, "head_body_extent_bh": 0.9756097560975611, "sheet_extent_bh": 1.8999999999999997, "streak_body_extent_bh": 1.6254335260115607, "sheet_tail": [-207.73699421965316, -26.05635838150289], "extent_alpha_threshold": 0, "body_alpha_threshold": 8, "key_states": [{"state": "stretched", "png": "res://vfx/fire_bolt_e1_A/key_states/stretched_clipped.png", "hold_frames": 4, "pivot": [329.0, 258.2], "scale": 1.0, "material": "res://vfx/fire_bolt_e1_A/materials/Travel_key_0.tres"}, {"state": "pulsed", "png": "res://vfx/fire_bolt_e1_A/key_states/pulsed_clipped.png", "hold_frames": 3, "pivot": [318.4, 262.3], "scale": 1.0, "material": "res://vfx/fire_bolt_e1_A/materials/Travel_key_1.tres"}], "enabled_layers": ["flash", "halo", "floor_light", "dark_duplicate", "victim_tint", "hit_stop", "contact_label"], "dark_duplicate": true, "strike_stop_s": 0.05}, {"screen_px": true, "name": "fire_bolt_e1_B", "flare": "res://vfx/fire_bolt_e1_B/flare.tres", "bolt": "res://scenes/vfx/g1_fl6_projectile.tscn", "head": "res://vfx/fire_bolt_e1_B/travel.tres", "animation": "travel", "impact": "res://scenes/vfx_fire_burst_e0p_v3_impact.tscn", "speed_px_s": 1510, "pierce": 0, "palette_3": [1, 0.94, 0.75, 1], "palette_2": [1, 0.55, 0.12, 1], "range_px": 520, "ground_squash": 0.6, "phase_scale": 1.0, "material": "res://vfx/fire_bolt_e1_B/materials/Body.tres", "binding": "res://scripts/vfx_fire_bolt_e1_B_material.gd", "collision_radius_bh": 0.25, "head_length_px": 74.66383117615416, "fields": {"res://vfx/fire_bolt_e1_B/sprites/travel/travel_00.png": "res://vfx/fire_bolt_e1_B/distance/travel/travel_00.png"}, "trail_color": [0.35, 0.65, 0.8, 0.6], "fire_layers": {"dark_duplicate": true, "glow": {"alpha": 0.2, "scale": 1.02, "peak": {"alpha": 0.35, "scale": 1.06}}, "floor_light": {"radius_px": 160, "duration_s": 0.35, "curve": "ease_out", "tint": "palette_2", "alpha": 0.6}, "flash": {"duration_s": 0.03333333333333333, "alpha": 0.8, "scale_from": 1.04, "scale_to": 1}, "cast": {"muzzle_puff": {"scale": 0.45, "frames": 4}, "floor_light": {"radius_bh": 0.8, "frames": 6, "alpha": 0.5}}, "travel": {"flicker_frames": 2, "trail": {"rate_per_s": 12, "size_px": [3, 5], "life_s": 0.45, "rise_px_s": 30, "lateral_px": 10, "bands": [3, 2]}, "erode_noise": 0.3, "core": {"band": 3, "alpha": 0.7, "blur_px": 4, "pulse_scale": 1.08, "hz": 8}, "halo": {"alpha": 0.3, "scale": 1.2}, "boil": {"uv_per_s": 0.5, "erode_amp": 0.08, "hz": 8}, "smear": {"band": 2, "alpha": 0.2, "length_bh": 1, "frames": 6}, "eruption": {"frames": 8, "scale_from": 0.25, "sheet_delay_frames": 3}, "flame_dance": {"layers": 3, "back_scale": 0.94, "front_scale": 1.04, "front_alpha": 0.85, "front_source": "inner_planes", "tongue_root_radius_factor": 1.15, "tongue_count": [6, 8], "tongue_scale": [1.1, 1.4], "tongue_core_alpha": 0.5, "jitter_px": 4, "jitter_deg": 2.5, "jitter_scale": 0.03, "step_frames": [2, 3], "flicker_hz": [3.3, 3.6], "seed_offset": 7}}, "core": {"band": 3, "alpha": 0.55, "blur_px": 6}, "contact_light": {"lerp": 0.45, "frames": 6}, "shimmer": {"amplitude_px": 3, "seconds": 0.8}}, "palette": [[0.25, 0.08, 0.04, 1], [0.7, 0.16, 0.08, 1], [1, 0.55, 0.12, 1], [1, 0.94, 0.75, 1]], "spec_speed_px_s": 1510, "contact_only": true, "grammar": "G1", "aim_rule": "release-locked", "termination": "first_contact_or_range", "range_expiry": "burst", "origin_socket": "cast_release", "seed": 2026, "painted_travel": {"head": {"binding": "P01_fire_head", "png": "res://vfx/fire_bolt_e1_B/primitives/head.png", "pivot": [334, 273], "scale": 0.7926829268292683, "rear_socket": [240, 267], "material": "res://vfx/fire_bolt_e1_B/materials/Travel_head.tres", "fizzle_material": "res://vfx/fire_bolt_e1_B/materials/Fizzle_head.tres"}, "streak": {"binding": "P02_fire_streak", "png": "res://vfx/fire_bolt_e1_B/primitives/streak.png", "pivot": [405, 274], "scale": 0.7138728323699421, "material": "res://vfx/fire_bolt_e1_B/materials/Travel_streak.tres"}, "rest_hold_frames": 3, "tail_s": 0.15}, "head_extent_bh": 1.0, "head_body_extent_bh": 0.9756097560975611, "sheet_extent_bh": 1.8999999999999997, "streak_body_extent_bh": 1.6254335260115607, "sheet_tail": [-207.73699421965316, -26.05635838150289], "extent_alpha_threshold": 0, "body_alpha_threshold": 8, "key_states": [], "enabled_layers": ["flash", "halo", "floor_light", "dark_duplicate", "victim_tint", "hit_stop", "contact_label"], "dark_duplicate": true, "strike_stop_s": 0.05}, {"screen_px": true, "name": "ice_bolt_e2", "flare": "res://vfx/ice_bolt_e2/flare.tres", "bolt": "res://scenes/vfx/g1_ice_projectile.tscn", "head": "res://vfx/ice_bolt_e2/travel.tres", "animation": "travel", "impact": "res://scenes/vfx_ice_bolt_e2_impact.tscn", "speed_px_s": 1040, "pierce": 0, "palette_3": [1, 1, 1, 1], "palette_2": [0.64, 0.88, 0.96, 1], "range_px": 520, "ground_squash": 1.0, "phase_scale": 1.0, "material": "res://vfx/ice_bolt_e2/materials/Body.tres", "binding": "res://scripts/vfx_ice_bolt_e2_material.gd", "collision_radius_bh": 0.25, "head_length_px": 91.61837953781873, "fields": {"res://vfx/ice_bolt_e2/sprites/travel/travel_00.png": "res://vfx/ice_bolt_e2/distance/travel/travel_00.png"}, "trail_color": [0.35, 0.65, 0.8, 0.6], "fire_layers": {}, "palette": [[0.035, 0.065, 0.13, 1], [0.22, 0.38, 0.52, 1], [0.64, 0.88, 0.96, 1], [1, 1, 1, 1]], "spec_speed_px_s": 1040, "contact_only": true, "grammar": "G1", "aim_rule": "release-locked", "termination": "first_contact_or_range", "range_expiry": "burst", "origin_socket": "cast_release", "seed": 2026, "painted_travel": {"head": {"binding": "P_ice_shard (oriented, 0.7 BH)", "png": "res://vfx/ice_bolt_e2/primitives/head.png", "pivot": [337, 266.0], "scale": 0.3611111111111111, "rear_socket": [86, 229.0], "material": "res://vfx/ice_bolt_e2/materials/Travel_head.tres", "fizzle_material": "res://vfx/ice_bolt_e2/materials/Fizzle_head.tres"}, "streak": {"binding": "S_ice_puff trail (angular puff, low alpha)", "png": "res://vfx/ice_bolt_e2/primitives/streak.png", "pivot": [388, 265.0], "scale": 1.0, "alpha": 0.6, "material": "res://vfx/ice_bolt_e2/materials/Travel_streak.tres"}, "rest_hold_frames": 3, "tail_s": 0.15}, "key_states": [], "enabled_layers": ["flash", "halo", "floor_light", "dark_duplicate", "victim_tint", "hit_stop", "contact_label"], "dark_duplicate": true, "strike_stop_s": 0.016666666666666666}, {"flame_dance": {"layers": 3, "back_scale": 0.94, "front_scale": 1.04, "front_alpha": 0.85, "front_source": "inner_planes", "tongue_root_radius_factor": 1.15, "tongue_count": [6, 8], "tongue_scale": [1.1, 1.4], "tongue_core_alpha": 0.5, "jitter_px": 3, "jitter_deg": 2.5, "jitter_scale": 0.03, "step_frames": [3, 5], "flicker_hz": [3.3, 3.6], "seed_offset": 7}, "name": "blackwater_cocktail_e3", "grammar": "G2", "screen_px": true, "flare": "res://vfx/blackwater_cocktail_e3/flare.tres", "bolt": "res://scenes/vfx/g2_flame_dance.tscn", "range_px": 520, "apex_px": 42, "flight_s": 0.4, "radius_px": 181, "duration_s": 2.5, "ticks": [0.0, 0.3, 0.95, 1.25, 2.0], "schedule": {"intervals_s": [0.3, 0.6499999999999999, 0.30000000000000004, 0.75], "interval_cv": 0.406201920231798, "minimum_cv": 0.25, "ff08_satisfied": true, "tick_count": 5}, "residue_s": 12.0, "ground_squash": 0.58, "roil_uv_per_s": 0.0, "dark_offset_px": 0.0, "dark_alpha": 0.25, "field_erode": 0.0, "flask": "res://vfx/blackwater_cocktail_e3/primitives/flask.png", "field": "res://vfx/blackwater_cocktail_e3/derived/field.png", "pulse": "res://vfx/blackwater_cocktail_e3/primitives/pulse.png", "fragments": ["res://vfx/blackwater_cocktail_e3/derived/glass_0.png", "res://vfx/blackwater_cocktail_e3/derived/glass_1.png", "res://vfx/blackwater_cocktail_e3/derived/glass_2.png"], "material": "res://vfx/blackwater_cocktail_e3/materials/Field.tres", "pulse_material": "res://vfx/blackwater_cocktail_e3/materials/Pulse.tres", "decal_material": "res://vfx/blackwater_cocktail_e3/materials/Decal.tres", "additive_material": "res://vfx/blackwater_cocktail_e3/materials/Halo.tres", "dark_material": "res://vfx/blackwater_cocktail_e3/materials/Dark.tres", "palette_3": [1, 0.94, 0.75, 1], "treatment": "fire", "density": 1.0, "seed": 2026, "field_binding": {"kind": "painted_pool", "scale": 1.0, "pivot": [256, 320], "dissolve_s": 0.4}, "lick_anchors": [[254, 263], [328, 333], [166, 278]], "walkable": [[[2812.88, 1222.44], [2829.1, 1223.03], [2874.38, 1231.97], [2904.57, 1234.66], [2959.91, 1232.09], [2975.0, 1232.99], [3015.25, 1243.5], [3016.78, 1242.52], [3015.86, 1238.5], [3030.34, 1226.02], [3035.37, 1227.8], [3100.77, 1276.14], [3125.93, 1283.7], [3161.14, 1291.28], [3191.33, 1292.96], [3206.42, 1291.06], [3236.6, 1280.44], [3256.73, 1270.69], [3261.76, 1270.01], [3265.32, 1274.64], [3276.85, 1299.19], [3293.29, 1318.81], [3322.37, 1346.92], [3331.37, 1358.96], [3345.84, 1391.09], [3356.7, 1431.24], [3363.64, 1451.32], [3370.5, 1463.36], [3369.0, 1475.41], [3371.99, 1495.49], [3370.96, 1499.5], [3355.15, 1523.6], [3347.28, 1531.69], [3327.16, 1545.29], [3296.98, 1560.65], [3251.53, 1575.8], [3226.54, 1585.62], [3215.05, 1591.86], [3194.13, 1611.93], [3180.43, 1628.0], [3171.2, 1635.55], [3125.93, 1659.22], [3100.77, 1678.53], [3080.8, 1704.29], [3070.12, 1732.4], [3059.29, 1796.64], [3058.74, 1820.73], [3061.32, 1844.83], [3073.39, 1876.95], [3094.36, 1901.04], [3089.65, 1921.12], [3078.04, 1949.23], [3065.92, 1969.3], [3047.91, 2013.47], [3047.22, 2025.52], [3056.84, 2065.67], [3056.6, 2121.89], [3059.99, 2141.96], [3059.29, 2158.03], [3056.83, 2170.07], [3037.65, 2198.18], [3024.72, 2222.27], [3022.92, 2230.3], [3022.43, 2250.38], [3022.72, 2258.41], [3027.68, 2282.5], [3041.19, 2322.66], [3043.33, 2334.7], [3045.01, 2350.76], [3038.38, 2386.9], [3038.3, 2394.93], [3046.82, 2439.1], [3052.96, 2455.16], [3052.04, 2467.21], [3043.29, 2499.33], [3039.33, 2523.43], [3040.4, 2547.52], [3035.61, 2579.64], [3028.49, 2599.72], [3027.67, 2607.75], [3035.92, 2639.87], [3051.86, 2663.96], [3054.03, 2671.99], [3034.74, 2688.06], [3020.22, 2704.12], [3002.74, 2728.21], [2994.2, 2752.3], [2980.39, 2776.39], [2961.2, 2796.47], [2947.54, 2820.56], [2939.58, 2852.69], [2944.01, 2880.79], [2952.35, 2908.9], [2965.22, 2932.99], [2995.12, 2966.92], [3001.66, 2977.16], [3002.37, 2985.19], [2998.97, 3021.33], [3002.02, 3049.44], [3008.43, 3073.53], [3032.1, 3129.75], [3037.31, 3145.81], [3039.73, 3161.87], [3041.76, 3202.02], [3047.43, 3242.18], [3063.44, 3298.39], [3059.04, 3358.62], [3064.45, 3386.73], [3091.77, 3446.96], [3095.31, 3459.01], [3100.75, 3499.16], [3106.06, 3523.26], [3116.15, 3547.35], [3133.21, 3579.47], [3146.88, 3619.62], [3173.8, 3671.82], [3177.93, 3687.89], [3176.91, 3695.92], [3160.61, 3720.01], [3116.8, 3796.3], [3114.59, 3804.33], [3112.17, 3828.42], [3116.41, 3868.58], [3114.05, 3908.73], [3114.89, 3916.76], [3119.25, 3936.84], [3124.64, 3948.89], [3151.64, 3976.99], [3143.84, 4013.13], [3145.3, 4041.24], [3153.47, 4069.35], [3154.98, 4072.0], [24.0, 4072.0], [24.0, 2923.97], [55.81, 2900.87], [62.08, 2892.84], [73.75, 2872.76], [84.17, 2840.64], [86.02, 2780.41], [94.75, 2728.21], [99.96, 2712.15], [119.75, 2680.03], [130.17, 2659.95], [138.31, 2635.86], [142.62, 2631.92], [177.83, 2627.46], [208.02, 2620.89], [235.61, 2611.76], [278.45, 2594.59], [293.54, 2590.72], [338.82, 2581.36], [363.97, 2579.11], [374.04, 2576.99], [384.1, 2572.95], [409.25, 2558.0], [439.44, 2579.85], [449.5, 2584.15], [479.68, 2593.06], [519.93, 2594.72], [555.15, 2589.1], [580.3, 2582.28], [680.92, 2550.5], [710.08, 2535.47], [741.29, 2513.81], [786.19, 2503.35], [831.85, 2487.94], [912.34, 2457.46], [967.68, 2466.89], [997.86, 2468.76], [1028.05, 2468.72], [1058.23, 2464.28], [1075.54, 2459.18], [1098.48, 2448.87], [1123.64, 2433.63], [1163.88, 2417.5], [1194.2, 2394.93], [1221.91, 2358.79], [1230.11, 2350.76], [1279.59, 2313.15], [1324.87, 2286.03], [1364.08, 2258.41], [1385.24, 2240.05], [1415.43, 2208.79], [1425.49, 2203.24], [1485.86, 2185.0], [1511.01, 2172.8], [1540.84, 2154.01], [1561.87, 2133.93], [1567.97, 2125.9], [1579.77, 2101.81], [1590.76, 2057.64], [1608.46, 2001.43], [1609.44, 1993.4], [1607.79, 1969.3], [1599.78, 1933.16], [1599.13, 1917.1], [1604.3, 1893.01], [1609.65, 1884.98], [1621.69, 1874.73], [1680.68, 1844.83], [1702.07, 1832.78], [1726.57, 1816.72], [1749.7, 1792.63], [1770.69, 1756.49], [1787.71, 1735.54], [1797.77, 1730.16], [1822.93, 1723.66], [1848.08, 1713.14], [1858.14, 1706.67], [1880.56, 1684.21], [1921.19, 1632.01], [1942.51, 1595.87], [1953.73, 1584.92], [1976.3, 1571.78], [2024.16, 1548.54], [2062.37, 1523.6], [2079.5, 1514.65], [2124.78, 1501.23], [2154.97, 1489.46], [2180.12, 1473.86], [2215.34, 1447.73], [2230.43, 1439.4], [2245.52, 1434.4], [2285.77, 1429.14], [2320.99, 1421.36], [2351.17, 1406.43], [2386.39, 1379.46], [2401.48, 1371.8], [2471.91, 1354.35], [2517.19, 1333.04], [2564.77, 1318.81], [2587.62, 1308.35], [2628.85, 1286.69], [2647.99, 1279.89], [2693.27, 1268.13], [2718.42, 1260.08], [2783.83, 1229.63], [2798.92, 1224.61]], [[4003.07, 24.0], [5352.0, 24.0], [5352.0, 1968.86], [5279.14, 1949.44], [5238.89, 1932.8], [5208.71, 1926.17], [5193.62, 1921.4], [5185.17, 1917.1], [5177.43, 1884.98], [5161.66, 1844.83], [5142.42, 1780.58], [5123.7, 1752.47], [5098.43, 1732.4], [5087.97, 1726.97], [5062.81, 1716.67], [5037.66, 1711.12], [5022.57, 1706.03], [4957.17, 1672.99], [4906.86, 1655.58], [4871.64, 1647.53], [4821.33, 1642.98], [4811.27, 1640.73], [4801.21, 1635.42], [4776.05, 1618.18], [4750.9, 1605.78], [4720.71, 1594.78], [4685.5, 1588.31], [4655.31, 1586.6], [4630.16, 1586.78], [4594.94, 1589.92], [4529.54, 1600.8], [4504.39, 1593.78], [4489.29, 1587.11], [4477.17, 1579.81], [4458.62, 1563.75], [4428.56, 1547.69], [4393.71, 1539.33], [4353.46, 1533.14], [4343.4, 1528.78], [4317.72, 1503.52], [4260.34, 1439.27], [4237.75, 1420.9], [4201.1, 1395.1], [4193.73, 1387.07], [4179.66, 1367.0], [4141.71, 1322.83], [4132.29, 1306.76], [4113.67, 1266.61], [4099.64, 1246.53], [4076.76, 1223.42], [4041.51, 1198.35], [4032.38, 1190.32], [4018.3, 1146.15], [4006.58, 1101.98], [4002.67, 1093.95], [3989.19, 1073.87], [3971.1, 1053.8], [3942.43, 1033.72], [3948.32, 1005.61], [3949.15, 957.43], [3943.36, 929.32], [3925.84, 899.45], [3905.71, 879.47], [3870.5, 850.29], [3847.69, 820.9], [3826.81, 800.83], [3800.06, 783.08], [3772.82, 772.72], [3739.69, 756.42], [3729.63, 748.35], [3709.9, 728.55], [3684.66, 712.49], [3639.61, 672.33], [3618.95, 657.79], [3588.77, 642.15], [3563.61, 632.52], [3533.43, 622.97], [3498.21, 613.99], [3495.07, 612.1], [3485.32, 588.01], [3482.37, 575.97], [3482.69, 567.93], [3484.76, 563.92], [3498.21, 550.11], [3512.28, 531.8], [3518.98, 519.75], [3526.46, 495.66], [3528.5, 439.44], [3533.99, 423.38], [3551.35, 391.26], [3585.09, 347.09], [3600.27, 331.03], [3621.27, 314.97], [3665.96, 294.89], [3694.41, 277.38], [3717.43, 254.74], [3729.77, 234.66], [3734.66, 229.62], [3754.79, 227.61], [3764.85, 224.88], [3795.03, 209.92], [3804.78, 202.54], [3826.18, 178.44], [3835.28, 172.52], [3905.71, 159.23], [3917.47, 154.35], [3944.66, 138.29], [3952.65, 130.26], [3968.74, 106.17], [3983.46, 66.01]], [[3228.83, 1403.62], [3342.76, 1305.42], [3121.28, 1141.73], [3007.35, 1239.93]], [[3342.76, 1305.42], [3456.69, 1207.22], [3235.21, 1043.53], [3121.28, 1141.73]], [[3456.69, 1207.22], [3570.61, 1109.02], [3349.13, 945.33], [3235.21, 1043.53]], [[3684.54, 1010.82], [3798.47, 912.62], [3576.99, 748.93], [3463.06, 847.13]], [[3798.47, 912.62], [3912.4, 814.42], [3690.92, 650.73], [3576.99, 748.93]], [[3570.61, 1109.02], [3684.54, 1010.82], [3463.06, 847.13], [3349.13, 945.33]]], "blocked": [[[3224.26, 1412.28], [3239.3, 1399.32], [3255.54, 1411.32], [3240.5, 1424.29]], [[2980.63, 1232.22], [2995.67, 1219.26], [3011.92, 1231.26], [2996.88, 1244.23]], [[3907.83, 823.09], [3922.87, 810.12], [3939.11, 822.13], [3924.07, 835.09]], [[3664.2, 643.03], [3679.24, 630.06], [3695.48, 642.07], [3680.44, 655.03]], [[3228.83, 1403.62], [3912.4, 814.42], [3934.55, 830.79], [3250.98, 1419.99]], [[3007.35, 1239.93], [3690.92, 650.73], [3668.77, 634.36], [2985.2, 1223.56]]], "px_per_bh": 130, "launch_angle_deg": 18.0, "lick_flicker_hz": [3.3, 3.6], "lick_coherence": "low \u2014 turbulent flicker with a characteristic timescale, NOT a pulse train and NOT the 1 Hz damage tick", "residue_diameter_px": 416.0, "residue_fade_in_s": 0.1, "residue_fade_out_s": 1.0, "flask_width": 45.5, "splash": "res://scenes/vfx_fire_burst_e0p_v2_impact.tscn", "splash_scale": 0.7, "enabled_layers": ["flash", "halo", "floor_light", "dark_duplicate", "victim_tint", "hit_stop", "contact_label"]}, {"name": "poisonous_concoction_e3", "grammar": "G2", "screen_px": true, "flare": "res://vfx/poisonous_concoction_e3/flare.tres", "bolt": "res://scenes/vfx/g2_thrown_field.tscn", "range_px": 480, "apex_px": 160, "flight_s": 0.5, "radius_px": 170, "duration_s": 2.0, "ticks": [0.0, 0.25, 0.8, 1.05, 1.7], "schedule": {"intervals_s": [0.25, 0.55, 0.25, 0.6499999999999999], "interval_cv": 0.42008402520840293, "minimum_cv": 0.25, "ff08_satisfied": true, "tick_count": 5}, "residue_s": 1.5, "ground_squash": 0.72, "roil_uv_per_s": 0.05, "dark_offset_px": 6, "dark_alpha": 0.5, "field_erode": 0.3, "flask": "res://vfx/poisonous_concoction_e3/primitives/flask.png", "field": "res://vfx/poisonous_concoction_e3/derived/field.png", "pulse": "res://vfx/poisonous_concoction_e3/primitives/pulse.png", "fragments": ["res://vfx/poisonous_concoction_e3/derived/glass_0.png", "res://vfx/poisonous_concoction_e3/derived/glass_1.png", "res://vfx/poisonous_concoction_e3/derived/glass_2.png"], "material": "res://vfx/poisonous_concoction_e3/materials/Field.tres", "pulse_material": "res://vfx/poisonous_concoction_e3/materials/Pulse.tres", "decal_material": "res://vfx/poisonous_concoction_e3/materials/Decal.tres", "additive_material": "res://vfx/poisonous_concoction_e3/materials/Halo.tres", "dark_material": "res://vfx/poisonous_concoction_e3/materials/Dark.tres", "palette_3": [0.85, 0.95, 0.6, 1], "treatment": "poison", "density": 0.6, "seed": 2026, "field_binding": {}, "lick_anchors": [], "walkable": [[[2812.88, 1222.44], [2829.1, 1223.03], [2874.38, 1231.97], [2904.57, 1234.66], [2959.91, 1232.09], [2975.0, 1232.99], [3015.25, 1243.5], [3016.78, 1242.52], [3015.86, 1238.5], [3030.34, 1226.02], [3035.37, 1227.8], [3100.77, 1276.14], [3125.93, 1283.7], [3161.14, 1291.28], [3191.33, 1292.96], [3206.42, 1291.06], [3236.6, 1280.44], [3256.73, 1270.69], [3261.76, 1270.01], [3265.32, 1274.64], [3276.85, 1299.19], [3293.29, 1318.81], [3322.37, 1346.92], [3331.37, 1358.96], [3345.84, 1391.09], [3356.7, 1431.24], [3363.64, 1451.32], [3370.5, 1463.36], [3369.0, 1475.41], [3371.99, 1495.49], [3370.96, 1499.5], [3355.15, 1523.6], [3347.28, 1531.69], [3327.16, 1545.29], [3296.98, 1560.65], [3251.53, 1575.8], [3226.54, 1585.62], [3215.05, 1591.86], [3194.13, 1611.93], [3180.43, 1628.0], [3171.2, 1635.55], [3125.93, 1659.22], [3100.77, 1678.53], [3080.8, 1704.29], [3070.12, 1732.4], [3059.29, 1796.64], [3058.74, 1820.73], [3061.32, 1844.83], [3073.39, 1876.95], [3094.36, 1901.04], [3089.65, 1921.12], [3078.04, 1949.23], [3065.92, 1969.3], [3047.91, 2013.47], [3047.22, 2025.52], [3056.84, 2065.67], [3056.6, 2121.89], [3059.99, 2141.96], [3059.29, 2158.03], [3056.83, 2170.07], [3037.65, 2198.18], [3024.72, 2222.27], [3022.92, 2230.3], [3022.43, 2250.38], [3022.72, 2258.41], [3027.68, 2282.5], [3041.19, 2322.66], [3043.33, 2334.7], [3045.01, 2350.76], [3038.38, 2386.9], [3038.3, 2394.93], [3046.82, 2439.1], [3052.96, 2455.16], [3052.04, 2467.21], [3043.29, 2499.33], [3039.33, 2523.43], [3040.4, 2547.52], [3035.61, 2579.64], [3028.49, 2599.72], [3027.67, 2607.75], [3035.92, 2639.87], [3051.86, 2663.96], [3054.03, 2671.99], [3034.74, 2688.06], [3020.22, 2704.12], [3002.74, 2728.21], [2994.2, 2752.3], [2980.39, 2776.39], [2961.2, 2796.47], [2947.54, 2820.56], [2939.58, 2852.69], [2944.01, 2880.79], [2952.35, 2908.9], [2965.22, 2932.99], [2995.12, 2966.92], [3001.66, 2977.16], [3002.37, 2985.19], [2998.97, 3021.33], [3002.02, 3049.44], [3008.43, 3073.53], [3032.1, 3129.75], [3037.31, 3145.81], [3039.73, 3161.87], [3041.76, 3202.02], [3047.43, 3242.18], [3063.44, 3298.39], [3059.04, 3358.62], [3064.45, 3386.73], [3091.77, 3446.96], [3095.31, 3459.01], [3100.75, 3499.16], [3106.06, 3523.26], [3116.15, 3547.35], [3133.21, 3579.47], [3146.88, 3619.62], [3173.8, 3671.82], [3177.93, 3687.89], [3176.91, 3695.92], [3160.61, 3720.01], [3116.8, 3796.3], [3114.59, 3804.33], [3112.17, 3828.42], [3116.41, 3868.58], [3114.05, 3908.73], [3114.89, 3916.76], [3119.25, 3936.84], [3124.64, 3948.89], [3151.64, 3976.99], [3143.84, 4013.13], [3145.3, 4041.24], [3153.47, 4069.35], [3154.98, 4072.0], [24.0, 4072.0], [24.0, 2923.97], [55.81, 2900.87], [62.08, 2892.84], [73.75, 2872.76], [84.17, 2840.64], [86.02, 2780.41], [94.75, 2728.21], [99.96, 2712.15], [119.75, 2680.03], [130.17, 2659.95], [138.31, 2635.86], [142.62, 2631.92], [177.83, 2627.46], [208.02, 2620.89], [235.61, 2611.76], [278.45, 2594.59], [293.54, 2590.72], [338.82, 2581.36], [363.97, 2579.11], [374.04, 2576.99], [384.1, 2572.95], [409.25, 2558.0], [439.44, 2579.85], [449.5, 2584.15], [479.68, 2593.06], [519.93, 2594.72], [555.15, 2589.1], [580.3, 2582.28], [680.92, 2550.5], [710.08, 2535.47], [741.29, 2513.81], [786.19, 2503.35], [831.85, 2487.94], [912.34, 2457.46], [967.68, 2466.89], [997.86, 2468.76], [1028.05, 2468.72], [1058.23, 2464.28], [1075.54, 2459.18], [1098.48, 2448.87], [1123.64, 2433.63], [1163.88, 2417.5], [1194.2, 2394.93], [1221.91, 2358.79], [1230.11, 2350.76], [1279.59, 2313.15], [1324.87, 2286.03], [1364.08, 2258.41], [1385.24, 2240.05], [1415.43, 2208.79], [1425.49, 2203.24], [1485.86, 2185.0], [1511.01, 2172.8], [1540.84, 2154.01], [1561.87, 2133.93], [1567.97, 2125.9], [1579.77, 2101.81], [1590.76, 2057.64], [1608.46, 2001.43], [1609.44, 1993.4], [1607.79, 1969.3], [1599.78, 1933.16], [1599.13, 1917.1], [1604.3, 1893.01], [1609.65, 1884.98], [1621.69, 1874.73], [1680.68, 1844.83], [1702.07, 1832.78], [1726.57, 1816.72], [1749.7, 1792.63], [1770.69, 1756.49], [1787.71, 1735.54], [1797.77, 1730.16], [1822.93, 1723.66], [1848.08, 1713.14], [1858.14, 1706.67], [1880.56, 1684.21], [1921.19, 1632.01], [1942.51, 1595.87], [1953.73, 1584.92], [1976.3, 1571.78], [2024.16, 1548.54], [2062.37, 1523.6], [2079.5, 1514.65], [2124.78, 1501.23], [2154.97, 1489.46], [2180.12, 1473.86], [2215.34, 1447.73], [2230.43, 1439.4], [2245.52, 1434.4], [2285.77, 1429.14], [2320.99, 1421.36], [2351.17, 1406.43], [2386.39, 1379.46], [2401.48, 1371.8], [2471.91, 1354.35], [2517.19, 1333.04], [2564.77, 1318.81], [2587.62, 1308.35], [2628.85, 1286.69], [2647.99, 1279.89], [2693.27, 1268.13], [2718.42, 1260.08], [2783.83, 1229.63], [2798.92, 1224.61]], [[4003.07, 24.0], [5352.0, 24.0], [5352.0, 1968.86], [5279.14, 1949.44], [5238.89, 1932.8], [5208.71, 1926.17], [5193.62, 1921.4], [5185.17, 1917.1], [5177.43, 1884.98], [5161.66, 1844.83], [5142.42, 1780.58], [5123.7, 1752.47], [5098.43, 1732.4], [5087.97, 1726.97], [5062.81, 1716.67], [5037.66, 1711.12], [5022.57, 1706.03], [4957.17, 1672.99], [4906.86, 1655.58], [4871.64, 1647.53], [4821.33, 1642.98], [4811.27, 1640.73], [4801.21, 1635.42], [4776.05, 1618.18], [4750.9, 1605.78], [4720.71, 1594.78], [4685.5, 1588.31], [4655.31, 1586.6], [4630.16, 1586.78], [4594.94, 1589.92], [4529.54, 1600.8], [4504.39, 1593.78], [4489.29, 1587.11], [4477.17, 1579.81], [4458.62, 1563.75], [4428.56, 1547.69], [4393.71, 1539.33], [4353.46, 1533.14], [4343.4, 1528.78], [4317.72, 1503.52], [4260.34, 1439.27], [4237.75, 1420.9], [4201.1, 1395.1], [4193.73, 1387.07], [4179.66, 1367.0], [4141.71, 1322.83], [4132.29, 1306.76], [4113.67, 1266.61], [4099.64, 1246.53], [4076.76, 1223.42], [4041.51, 1198.35], [4032.38, 1190.32], [4018.3, 1146.15], [4006.58, 1101.98], [4002.67, 1093.95], [3989.19, 1073.87], [3971.1, 1053.8], [3942.43, 1033.72], [3948.32, 1005.61], [3949.15, 957.43], [3943.36, 929.32], [3925.84, 899.45], [3905.71, 879.47], [3870.5, 850.29], [3847.69, 820.9], [3826.81, 800.83], [3800.06, 783.08], [3772.82, 772.72], [3739.69, 756.42], [3729.63, 748.35], [3709.9, 728.55], [3684.66, 712.49], [3639.61, 672.33], [3618.95, 657.79], [3588.77, 642.15], [3563.61, 632.52], [3533.43, 622.97], [3498.21, 613.99], [3495.07, 612.1], [3485.32, 588.01], [3482.37, 575.97], [3482.69, 567.93], [3484.76, 563.92], [3498.21, 550.11], [3512.28, 531.8], [3518.98, 519.75], [3526.46, 495.66], [3528.5, 439.44], [3533.99, 423.38], [3551.35, 391.26], [3585.09, 347.09], [3600.27, 331.03], [3621.27, 314.97], [3665.96, 294.89], [3694.41, 277.38], [3717.43, 254.74], [3729.77, 234.66], [3734.66, 229.62], [3754.79, 227.61], [3764.85, 224.88], [3795.03, 209.92], [3804.78, 202.54], [3826.18, 178.44], [3835.28, 172.52], [3905.71, 159.23], [3917.47, 154.35], [3944.66, 138.29], [3952.65, 130.26], [3968.74, 106.17], [3983.46, 66.01]], [[3228.83, 1403.62], [3342.76, 1305.42], [3121.28, 1141.73], [3007.35, 1239.93]], [[3342.76, 1305.42], [3456.69, 1207.22], [3235.21, 1043.53], [3121.28, 1141.73]], [[3456.69, 1207.22], [3570.61, 1109.02], [3349.13, 945.33], [3235.21, 1043.53]], [[3684.54, 1010.82], [3798.47, 912.62], [3576.99, 748.93], [3463.06, 847.13]], [[3798.47, 912.62], [3912.4, 814.42], [3690.92, 650.73], [3576.99, 748.93]], [[3570.61, 1109.02], [3684.54, 1010.82], [3463.06, 847.13], [3349.13, 945.33]]], "blocked": [[[3224.26, 1412.28], [3239.3, 1399.32], [3255.54, 1411.32], [3240.5, 1424.29]], [[2980.63, 1232.22], [2995.67, 1219.26], [3011.92, 1231.26], [2996.88, 1244.23]], [[3907.83, 823.09], [3922.87, 810.12], [3939.11, 822.13], [3924.07, 835.09]], [[3664.2, 643.03], [3679.24, 630.06], [3695.48, 642.07], [3680.44, 655.03]], [[3228.83, 1403.62], [3912.4, 814.42], [3934.55, 830.79], [3250.98, 1419.99]], [[3007.35, 1239.93], [3690.92, 650.73], [3668.77, 634.36], [2985.2, 1223.56]]], "px_per_bh": 130, "launch_angle_deg": 18.0, "lick_flicker_hz": [], "lick_coherence": "", "residue_diameter_px": 0, "residue_fade_in_s": 0.0, "residue_fade_out_s": 1.5, "flask_width": 45.5, "splash": "", "splash_scale": 1, "enabled_layers": ["flash", "halo", "floor_light", "dark_duplicate", "victim_tint", "hit_stop", "contact_label"]}, {"name": "lightning_blast_e3", "grammar": "G3", "screen_px": true, "flare": "res://vfx/lightning_blast_e3/flare.tres", "bolt": "res://scenes/vfx/g3_bolt_chain.tscn", "range_px": 560, "hop_range_px": 220, "delays": [0.05], "cumulative": [0.05], "schedule": {"delays_s": [0.05], "cumulative_s": [0.05], "interval_cv": null, "minimum_cv": 0.25, "cv_evaluable": false, "count_semantics": "additional hops after initial contact"}, "primitives": {"link": {"png": "res://vfx/lightning_blast_e3/primitives/link.png", "start": [154.0, 255.0], "end": [357.0, 255.0], "region": [154, 0, 204, 512], "coverage_width": 39, "material": "res://vfx/lightning_blast_e3/materials/Link.tres"}, "branch": {"png": "res://vfx/lightning_blast_e3/primitives/branch.png", "start": [191.0, 263.5], "end": [335.0, 209.0], "region": [191, 0, 145, 512], "coverage_width": 105, "material": "res://vfx/lightning_blast_e3/materials/Branch.tres"}, "prong": {"png": "res://vfx/lightning_blast_e3/primitives/prong.png", "start": [222.0, 302.0], "end": [291.0, 216.5], "region": [222, 0, 70, 512], "coverage_width": 89, "material": "res://vfx/lightning_blast_e3/materials/Prong.tres"}}, "link_scale": 0.5641025641025641, "link_length_px": 114.51282051282051, "width_px": 22, "width_multiplier": 1.0, "prong_length_px": 78.0, "max_branches": 2, "prongs": 4, "min_links": 1, "max_links": 64, "segment_fraction": 0.8, "jitter_px": 12, "seed": 2026, "life_s": 0.12, "afterimage_s": 0.15, "palette_3": [0.88, 0.96, 1, 1], "enabled_layers": ["flash", "halo", "victim_tint", "hit_stop", "contact_label"]}, {"name": "zeus_chain_e3", "grammar": "G3", "screen_px": true, "flare": "res://vfx/zeus_chain_e3/flare.tres", "bolt": "res://scenes/vfx/g3_bolt_chain.tscn", "range_px": 520, "hop_range_px": 260, "delays": [0.06, 0.11, 0.08, 0.13], "cumulative": [0.06, 0.16999999999999998, 0.25, 0.38], "schedule": {"delays_s": [0.06, 0.11, 0.08, 0.13], "cumulative_s": [0.06, 0.16999999999999998, 0.25, 0.38], "interval_cv": 0.2834297266912897, "minimum_cv": 0.25, "cv_evaluable": true, "count_semantics": "additional hops after initial contact"}, "primitives": {"link": {"png": "res://vfx/zeus_chain_e3/primitives/link.png", "start": [154.0, 255.0], "end": [357.0, 255.0], "region": [154, 0, 204, 512], "coverage_width": 39, "material": "res://vfx/zeus_chain_e3/materials/Link.tres"}, "branch": {"png": "res://vfx/zeus_chain_e3/primitives/branch.png", "start": [191.0, 263.5], "end": [335.0, 209.0], "region": [191, 0, 145, 512], "coverage_width": 105, "material": "res://vfx/zeus_chain_e3/materials/Branch.tres"}, "prong": {"png": "res://vfx/zeus_chain_e3/primitives/prong.png", "start": [222.0, 302.0], "end": [291.0, 216.5], "region": [222, 0, 70, 512], "coverage_width": 89, "material": "res://vfx/zeus_chain_e3/materials/Prong.tres"}}, "link_scale": 0.7692307692307693, "link_length_px": 156.15384615384616, "width_px": 30, "width_multiplier": 1.35, "prong_length_px": 78.0, "max_branches": 1, "prongs": 2, "min_links": 2, "max_links": 3, "segment_fraction": 0.8, "jitter_px": 12, "seed": 2026, "life_s": 0.1, "afterimage_s": 0.15, "palette_3": [1.0, 1.0, 0.98, 1.0], "enabled_layers": ["flash", "halo", "victim_tint", "hit_stop", "contact_label"]}, {"name": "healing_hands_e3", "grammar": "G4", "screen_px": true, "bolt": "res://scenes/vfx/g4_aura_loop.tscn", "flare": "res://vfx/healing_hands_e3/flare.tres", "radius_px": 160, "duration_s": 4.0, "pulses": [0.0, 0.45, 1.6, 1.95, 3.1, 3.45], "schedule": {"intervals_s": [0.45, 1.1500000000000001, 0.34999999999999987, 1.1500000000000001, 0.3500000000000001], "interval_cv": 0.5468974569308176, "minimum_cv": 0.25, "ff08_satisfied": true, "tick_count": 6}, "orbit_period_s": 2.6, "petal_life_s": 0.45, "release_s": 0.3, "seed": 2026, "support_tint": [1.0, 0.94, 0.72, 1.0], "seal_aspect": 0.6625, "primitives": {"ring": {"png": "res://vfx/healing_hands_e3/primitives/ring.png", "pivot": [253.0, 247.5], "scale": 0.7, "material": "res://vfx/healing_hands_e3/materials/Ring.tres"}, "petal": {"png": "res://vfx/healing_hands_e3/primitives/petal.png", "pivot": [283.5, 312.0], "scale": 1.0196078431372548, "material": "res://vfx/healing_hands_e3/materials/Petal.tres"}, "seal": {"png": "res://vfx/healing_hands_e3/primitives/seal.png", "pivot": [245.5, 270.5], "scale": 1.0, "material": "res://vfx/healing_hands_e3/materials/Seal.tres"}}, "halo_material": "res://vfx/healing_hands_e3/materials/Halo.tres", "floor_material": "res://vfx/healing_hands_e3/materials/FloorLight.tres"}, {"screen_px": true, "name": "frozen_orb_e3", "flare": "res://vfx/frozen_orb_e3/flare.tres", "bolt": "res://scenes/vfx/g1_orb.tscn", "head": "res://vfx/frozen_orb_e3/travel.tres", "animation": "travel", "impact": "res://scenes/vfx_frozen_orb_e3_impact.tscn", "speed_px_s": 420, "pierce": -1, "palette_3": [1, 1, 1, 1], "palette_2": [0.64, 0.88, 0.96, 1], "range_px": 630, "ground_squash": 1.0, "phase_scale": 1.0, "material": "res://vfx/frozen_orb_e3/materials/Body.tres", "binding": "res://scripts/vfx_frozen_orb_e3_material.gd", "collision_radius_bh": 0.25, "child_collision_radius_bh": 0.15, "child_head_length_px": 45.5, "head_length_px": 117.0, "fields": {"res://vfx/frozen_orb_e3/sprites/travel/travel_00.png": "res://vfx/frozen_orb_e3/distance/travel/travel_00.png"}, "trail_color": [0.35, 0.65, 0.8, 0.6], "grammar": "G1", "orb": {"body": {"png": "res://vfx/frozen_orb_e3/primitives/body.png", "pivot": [281.0, 265.0], "scale": 0.5441860465116279, "binding": "ice orb = P_ice_puff rotated (0.9 BH) + rim shards", "material": "res://vfx/frozen_orb_e3/materials/Orb_body.tres"}, "shard": {"png": "res://vfx/frozen_orb_e3/primitives/shard.png", "pivot": [211.5, 229.0], "scale": 0.18055555555555555, "binding": "P_ice_shard (0.35 BH)", "material": "res://vfx/frozen_orb_e3/materials/Orb_shard.tres"}, "angle_step_deg": 137, "seed": 2026, "pool_size": 12, "turn_s": 1.2, "rim_count": 4, "rim_radius_px": 42, "expiry_count": 16, "child_pierce": 0, "interval_frames_choices": [2, 3, 4], "interval_draw": "balanced_shuffle", "expiry_mode": "nova", "expiry_core_bh": 0.8, "expiry_decal": false}, "contact_only": true, "expiry_frames": 90, "child_speed_px_s": 900, "child_range_px": 260, "schedule": {"intervals_s": [0.06666666666666667, 0.06666666666666667, 0.033333333333333326, 0.06666666666666668, 0.04999999999999999, 0.04999999999999999, 0.033333333333333326, 0.06666666666666671, 0.04999999999999999, 0.04999999999999999, 0.06666666666666665, 0.050000000000000044, 0.033333333333333326, 0.033333333333333326, 0.050000000000000044, 0.06666666666666665, 0.06666666666666665, 0.033333333333333326, 0.04999999999999993, 0.050000000000000155, 0.06666666666666665, 0.033333333333333215, 0.050000000000000044, 0.033333333333333215, 0.03333333333333344, 0.03333333333333344, 0.033333333333333215, 0.03333333333333344, 0.06666666666666665], "interval_cv": 0.2823529411764707, "minimum_cv": 0.25, "ff08_satisfied": true, "tick_count": 30, "emission_ages": [3, 7, 11, 13, 17, 20, 23, 25, 29, 32, 35, 39, 42, 44, 46, 49, 53, 57, 59, 62, 65, 69, 71, 74, 76, 78, 80, 82, 84, 88], "emission_count": 30, "flight_frames": 90, "expiry_distance_px": 630, "range_reached": true}, "enabled_layers": ["flash", "halo", "floor_light", "dark_duplicate", "victim_tint", "hit_stop", "contact_label"], "strike_stop_s": 0.016666666666666666}, {"screen_px": true, "name": "fire_burst_e0p_v3", "flare": "res://vfx/fire_burst_e0p_v3/flare.tres", "bolt": "res://scenes/vfx/g1_projectile.tscn", "head": "res://vfx/fire_burst_e0p_v3/travel.tres", "animation": "travel", "impact": "res://scenes/vfx_fire_burst_e0p_v3_impact.tscn", "speed_px_s": 640, "pierce": 0, "palette_3": [1, 0.94, 0.75, 1], "palette_2": [1, 0.55, 0.12, 1], "range_px": 650.0, "ground_squash": 1.0, "phase_scale": 1.0, "material": "res://vfx/fire_burst_e0p_v3/materials/Body.tres", "binding": "res://scripts/vfx_fire_burst_e0p_v3_material.gd", "collision_radius_bh": 0.25, "head_length_px": 12.0, "fields": {"res://vfx/fire_burst_e0p_v3/sprites/travel/travel_00.png": "res://vfx/fire_burst_e0p_v3/distance/travel/travel_00.png"}, "trail_color": [0.35, 0.65, 0.8, 0.6]}, {"name": "blackwater_cocktail_e3_V", "grammar": "G2", "screen_px": true, "flare": "res://vfx/blackwater_cocktail_e3_V/flare.tres", "bolt": "res://scenes/vfx/g2_flipbook.tscn", "range_px": 520, "apex_px": 42, "flight_s": 0.4, "radius_px": 181, "duration_s": 4.0, "ticks": [0.75, 1.75, 2.75], "schedule": {"intervals_s": [1, 1], "interval_cv": 0.0, "minimum_cv": 0.25, "ff08_satisfied": false, "tick_count": 3}, "residue_s": 12.0, "ground_squash": 0.58, "roil_uv_per_s": 0.0, "dark_offset_px": 0.0, "dark_alpha": 0.25, "field_erode": 0.0, "flask": "res://vfx/blackwater_cocktail_e3_V/primitives/flask.png", "material": "res://vfx/blackwater_cocktail_e3_V/materials/Field.tres", "palette_3": [1, 0.94, 0.75, 1], "treatment": "fire", "density": 1.0, "seed": 2026, "field_binding": {}, "lick_anchors": [], "walkable": [[[2812.88, 1222.44], [2829.1, 1223.03], [2874.38, 1231.97], [2904.57, 1234.66], [2959.91, 1232.09], [2975.0, 1232.99], [3015.25, 1243.5], [3016.78, 1242.52], [3015.86, 1238.5], [3030.34, 1226.02], [3035.37, 1227.8], [3100.77, 1276.14], [3125.93, 1283.7], [3161.14, 1291.28], [3191.33, 1292.96], [3206.42, 1291.06], [3236.6, 1280.44], [3256.73, 1270.69], [3261.76, 1270.01], [3265.32, 1274.64], [3276.85, 1299.19], [3293.29, 1318.81], [3322.37, 1346.92], [3331.37, 1358.96], [3345.84, 1391.09], [3356.7, 1431.24], [3363.64, 1451.32], [3370.5, 1463.36], [3369.0, 1475.41], [3371.99, 1495.49], [3370.96, 1499.5], [3355.15, 1523.6], [3347.28, 1531.69], [3327.16, 1545.29], [3296.98, 1560.65], [3251.53, 1575.8], [3226.54, 1585.62], [3215.05, 1591.86], [3194.13, 1611.93], [3180.43, 1628.0], [3171.2, 1635.55], [3125.93, 1659.22], [3100.77, 1678.53], [3080.8, 1704.29], [3070.12, 1732.4], [3059.29, 1796.64], [3058.74, 1820.73], [3061.32, 1844.83], [3073.39, 1876.95], [3094.36, 1901.04], [3089.65, 1921.12], [3078.04, 1949.23], [3065.92, 1969.3], [3047.91, 2013.47], [3047.22, 2025.52], [3056.84, 2065.67], [3056.6, 2121.89], [3059.99, 2141.96], [3059.29, 2158.03], [3056.83, 2170.07], [3037.65, 2198.18], [3024.72, 2222.27], [3022.92, 2230.3], [3022.43, 2250.38], [3022.72, 2258.41], [3027.68, 2282.5], [3041.19, 2322.66], [3043.33, 2334.7], [3045.01, 2350.76], [3038.38, 2386.9], [3038.3, 2394.93], [3046.82, 2439.1], [3052.96, 2455.16], [3052.04, 2467.21], [3043.29, 2499.33], [3039.33, 2523.43], [3040.4, 2547.52], [3035.61, 2579.64], [3028.49, 2599.72], [3027.67, 2607.75], [3035.92, 2639.87], [3051.86, 2663.96], [3054.03, 2671.99], [3034.74, 2688.06], [3020.22, 2704.12], [3002.74, 2728.21], [2994.2, 2752.3], [2980.39, 2776.39], [2961.2, 2796.47], [2947.54, 2820.56], [2939.58, 2852.69], [2944.01, 2880.79], [2952.35, 2908.9], [2965.22, 2932.99], [2995.12, 2966.92], [3001.66, 2977.16], [3002.37, 2985.19], [2998.97, 3021.33], [3002.02, 3049.44], [3008.43, 3073.53], [3032.1, 3129.75], [3037.31, 3145.81], [3039.73, 3161.87], [3041.76, 3202.02], [3047.43, 3242.18], [3063.44, 3298.39], [3059.04, 3358.62], [3064.45, 3386.73], [3091.77, 3446.96], [3095.31, 3459.01], [3100.75, 3499.16], [3106.06, 3523.26], [3116.15, 3547.35], [3133.21, 3579.47], [3146.88, 3619.62], [3173.8, 3671.82], [3177.93, 3687.89], [3176.91, 3695.92], [3160.61, 3720.01], [3116.8, 3796.3], [3114.59, 3804.33], [3112.17, 3828.42], [3116.41, 3868.58], [3114.05, 3908.73], [3114.89, 3916.76], [3119.25, 3936.84], [3124.64, 3948.89], [3151.64, 3976.99], [3143.84, 4013.13], [3145.3, 4041.24], [3153.47, 4069.35], [3154.98, 4072.0], [24.0, 4072.0], [24.0, 2923.97], [55.81, 2900.87], [62.08, 2892.84], [73.75, 2872.76], [84.17, 2840.64], [86.02, 2780.41], [94.75, 2728.21], [99.96, 2712.15], [119.75, 2680.03], [130.17, 2659.95], [138.31, 2635.86], [142.62, 2631.92], [177.83, 2627.46], [208.02, 2620.89], [235.61, 2611.76], [278.45, 2594.59], [293.54, 2590.72], [338.82, 2581.36], [363.97, 2579.11], [374.04, 2576.99], [384.1, 2572.95], [409.25, 2558.0], [439.44, 2579.85], [449.5, 2584.15], [479.68, 2593.06], [519.93, 2594.72], [555.15, 2589.1], [580.3, 2582.28], [680.92, 2550.5], [710.08, 2535.47], [741.29, 2513.81], [786.19, 2503.35], [831.85, 2487.94], [912.34, 2457.46], [967.68, 2466.89], [997.86, 2468.76], [1028.05, 2468.72], [1058.23, 2464.28], [1075.54, 2459.18], [1098.48, 2448.87], [1123.64, 2433.63], [1163.88, 2417.5], [1194.2, 2394.93], [1221.91, 2358.79], [1230.11, 2350.76], [1279.59, 2313.15], [1324.87, 2286.03], [1364.08, 2258.41], [1385.24, 2240.05], [1415.43, 2208.79], [1425.49, 2203.24], [1485.86, 2185.0], [1511.01, 2172.8], [1540.84, 2154.01], [1561.87, 2133.93], [1567.97, 2125.9], [1579.77, 2101.81], [1590.76, 2057.64], [1608.46, 2001.43], [1609.44, 1993.4], [1607.79, 1969.3], [1599.78, 1933.16], [1599.13, 1917.1], [1604.3, 1893.01], [1609.65, 1884.98], [1621.69, 1874.73], [1680.68, 1844.83], [1702.07, 1832.78], [1726.57, 1816.72], [1749.7, 1792.63], [1770.69, 1756.49], [1787.71, 1735.54], [1797.77, 1730.16], [1822.93, 1723.66], [1848.08, 1713.14], [1858.14, 1706.67], [1880.56, 1684.21], [1921.19, 1632.01], [1942.51, 1595.87], [1953.73, 1584.92], [1976.3, 1571.78], [2024.16, 1548.54], [2062.37, 1523.6], [2079.5, 1514.65], [2124.78, 1501.23], [2154.97, 1489.46], [2180.12, 1473.86], [2215.34, 1447.73], [2230.43, 1439.4], [2245.52, 1434.4], [2285.77, 1429.14], [2320.99, 1421.36], [2351.17, 1406.43], [2386.39, 1379.46], [2401.48, 1371.8], [2471.91, 1354.35], [2517.19, 1333.04], [2564.77, 1318.81], [2587.62, 1308.35], [2628.85, 1286.69], [2647.99, 1279.89], [2693.27, 1268.13], [2718.42, 1260.08], [2783.83, 1229.63], [2798.92, 1224.61]], [[4003.07, 24.0], [5352.0, 24.0], [5352.0, 1968.86], [5279.14, 1949.44], [5238.89, 1932.8], [5208.71, 1926.17], [5193.62, 1921.4], [5185.17, 1917.1], [5177.43, 1884.98], [5161.66, 1844.83], [5142.42, 1780.58], [5123.7, 1752.47], [5098.43, 1732.4], [5087.97, 1726.97], [5062.81, 1716.67], [5037.66, 1711.12], [5022.57, 1706.03], [4957.17, 1672.99], [4906.86, 1655.58], [4871.64, 1647.53], [4821.33, 1642.98], [4811.27, 1640.73], [4801.21, 1635.42], [4776.05, 1618.18], [4750.9, 1605.78], [4720.71, 1594.78], [4685.5, 1588.31], [4655.31, 1586.6], [4630.16, 1586.78], [4594.94, 1589.92], [4529.54, 1600.8], [4504.39, 1593.78], [4489.29, 1587.11], [4477.17, 1579.81], [4458.62, 1563.75], [4428.56, 1547.69], [4393.71, 1539.33], [4353.46, 1533.14], [4343.4, 1528.78], [4317.72, 1503.52], [4260.34, 1439.27], [4237.75, 1420.9], [4201.1, 1395.1], [4193.73, 1387.07], [4179.66, 1367.0], [4141.71, 1322.83], [4132.29, 1306.76], [4113.67, 1266.61], [4099.64, 1246.53], [4076.76, 1223.42], [4041.51, 1198.35], [4032.38, 1190.32], [4018.3, 1146.15], [4006.58, 1101.98], [4002.67, 1093.95], [3989.19, 1073.87], [3971.1, 1053.8], [3942.43, 1033.72], [3948.32, 1005.61], [3949.15, 957.43], [3943.36, 929.32], [3925.84, 899.45], [3905.71, 879.47], [3870.5, 850.29], [3847.69, 820.9], [3826.81, 800.83], [3800.06, 783.08], [3772.82, 772.72], [3739.69, 756.42], [3729.63, 748.35], [3709.9, 728.55], [3684.66, 712.49], [3639.61, 672.33], [3618.95, 657.79], [3588.77, 642.15], [3563.61, 632.52], [3533.43, 622.97], [3498.21, 613.99], [3495.07, 612.1], [3485.32, 588.01], [3482.37, 575.97], [3482.69, 567.93], [3484.76, 563.92], [3498.21, 550.11], [3512.28, 531.8], [3518.98, 519.75], [3526.46, 495.66], [3528.5, 439.44], [3533.99, 423.38], [3551.35, 391.26], [3585.09, 347.09], [3600.27, 331.03], [3621.27, 314.97], [3665.96, 294.89], [3694.41, 277.38], [3717.43, 254.74], [3729.77, 234.66], [3734.66, 229.62], [3754.79, 227.61], [3764.85, 224.88], [3795.03, 209.92], [3804.78, 202.54], [3826.18, 178.44], [3835.28, 172.52], [3905.71, 159.23], [3917.47, 154.35], [3944.66, 138.29], [3952.65, 130.26], [3968.74, 106.17], [3983.46, 66.01]], [[3228.83, 1403.62], [3342.76, 1305.42], [3121.28, 1141.73], [3007.35, 1239.93]], [[3342.76, 1305.42], [3456.69, 1207.22], [3235.21, 1043.53], [3121.28, 1141.73]], [[3456.69, 1207.22], [3570.61, 1109.02], [3349.13, 945.33], [3235.21, 1043.53]], [[3684.54, 1010.82], [3798.47, 912.62], [3576.99, 748.93], [3463.06, 847.13]], [[3798.47, 912.62], [3912.4, 814.42], [3690.92, 650.73], [3576.99, 748.93]], [[3570.61, 1109.02], [3684.54, 1010.82], [3463.06, 847.13], [3349.13, 945.33]]], "blocked": [[[3224.26, 1412.28], [3239.3, 1399.32], [3255.54, 1411.32], [3240.5, 1424.29]], [[2980.63, 1232.22], [2995.67, 1219.26], [3011.92, 1231.26], [2996.88, 1244.23]], [[3907.83, 823.09], [3922.87, 810.12], [3939.11, 822.13], [3924.07, 835.09]], [[3664.2, 643.03], [3679.24, 630.06], [3695.48, 642.07], [3680.44, 655.03]], [[3228.83, 1403.62], [3912.4, 814.42], [3934.55, 830.79], [3250.98, 1419.99]], [[3007.35, 1239.93], [3690.92, 650.73], [3668.77, 634.36], [2985.2, 1223.56]]], "px_per_bh": 130, "launch_angle_deg": 18.0, "lick_flicker_hz": [3.3, 3.6], "lick_coherence": "low \u2014 turbulent flicker with a characteristic timescale, NOT a pulse train and NOT the 1 Hz damage tick", "residue_diameter_px": 416.0, "residue_fade_in_s": 0.1, "residue_fade_out_s": 1.0, "flask_width": 45.5, "splash": "", "splash_scale": 0.7, "enabled_layers": ["floor_light", "victim_tint", "hit_stop", "contact_label"], "body_mode": "flipbook", "spine": "res://vfx/blackwater_cocktail_e3_V/spine.tres", "spine_config": {"body_mode": "flipbook", "frames": ["primitives/spine/bw_000.png", "primitives/spine/bw_001.png", "primitives/spine/bw_002.png", "primitives/spine/bw_003.png", "primitives/spine/bw_004.png", "primitives/spine/bw_005.png", "primitives/spine/bw_006.png", "primitives/spine/bw_007.png", "primitives/spine/bw_008.png", "primitives/spine/bw_009.png", "primitives/spine/bw_010.png", "primitives/spine/bw_011.png", "primitives/spine/bw_012.png", "primitives/spine/bw_013.png", "primitives/spine/bw_014.png", "primitives/spine/bw_015.png", "primitives/spine/bw_016.png", "primitives/spine/bw_017.png", "primitives/spine/bw_018.png", "primitives/spine/bw_019.png", "primitives/spine/bw_020.png", "primitives/spine/bw_021.png", "primitives/spine/bw_022.png", "primitives/spine/bw_023.png", "primitives/spine/bw_024.png", "primitives/spine/bw_025.png", "primitives/spine/bw_026.png", "primitives/spine/bw_027.png", "primitives/spine/bw_028.png", "primitives/spine/bw_029.png", "primitives/spine/bw_030.png", "primitives/spine/bw_031.png", "primitives/spine/bw_032.png", "primitives/spine/bw_033.png", "primitives/spine/bw_034.png", "primitives/spine/bw_035.png", "primitives/spine/bw_036.png", "primitives/spine/bw_037.png", "primitives/spine/bw_038.png", "primitives/spine/bw_039.png", "primitives/spine/bw_040.png", "primitives/spine/bw_041.png", "primitives/spine/bw_042.png", "primitives/spine/bw_043.png", "primitives/spine/bw_044.png", "primitives/spine/bw_045.png", "primitives/spine/bw_046.png", "primitives/spine/bw_047.png", "primitives/spine/bw_048.png", "primitives/spine/bw_049.png", "primitives/spine/bw_050.png", "primitives/spine/bw_051.png", "primitives/spine/bw_052.png", "primitives/spine/bw_053.png", "primitives/spine/bw_054.png", "primitives/spine/bw_055.png", "primitives/spine/bw_056.png", "primitives/spine/bw_057.png", "primitives/spine/bw_058.png", "primitives/spine/bw_059.png", "primitives/spine/bw_060.png", "primitives/spine/bw_061.png", "primitives/spine/bw_062.png", "primitives/spine/bw_063.png", "primitives/spine/bw_064.png", "primitives/spine/bw_065.png", "primitives/spine/bw_066.png", "primitives/spine/bw_067.png", "primitives/spine/bw_068.png", "primitives/spine/bw_069.png", "primitives/spine/bw_070.png", "primitives/spine/bw_071.png", "primitives/spine/bw_072.png", "primitives/spine/bw_073.png", "primitives/spine/bw_074.png", "primitives/spine/bw_075.png", "primitives/spine/bw_076.png", "primitives/spine/bw_077.png", "primitives/spine/bw_078.png", "primitives/spine/bw_079.png", "primitives/spine/bw_080.png", "primitives/spine/bw_081.png", "primitives/spine/bw_082.png", "primitives/spine/bw_083.png", "primitives/spine/bw_084.png", "primitives/spine/bw_085.png", "primitives/spine/bw_086.png", "primitives/spine/bw_087.png", "primitives/spine/bw_088.png", "primitives/spine/bw_089.png", "primitives/spine/bw_090.png", "primitives/spine/bw_091.png", "primitives/spine/bw_092.png", "primitives/spine/bw_093.png", "primitives/spine/bw_094.png", "primitives/spine/bw_095.png", "primitives/spine/bw_096.png", "primitives/spine/bw_097.png", "primitives/spine/bw_098.png", "primitives/spine/bw_099.png", "primitives/spine/bw_100.png", "primitives/spine/bw_101.png", "primitives/spine/bw_102.png", "primitives/spine/bw_103.png", "primitives/spine/bw_104.png", "primitives/spine/bw_105.png", "primitives/spine/bw_106.png", "primitives/spine/bw_107.png", "primitives/spine/bw_108.png", "primitives/spine/bw_109.png", "primitives/spine/bw_110.png", "primitives/spine/bw_111.png", "primitives/spine/bw_112.png", "primitives/spine/bw_113.png", "primitives/spine/bw_114.png", "primitives/spine/bw_115.png", "primitives/spine/bw_116.png", "primitives/spine/bw_117.png", "primitives/spine/bw_118.png", "primitives/spine/bw_119.png", "primitives/spine/bw_120.png", "primitives/spine/bw_121.png", "primitives/spine/bw_122.png", "primitives/spine/bw_123.png", "primitives/spine/bw_124.png", "primitives/spine/bw_125.png", "primitives/spine/bw_126.png", "primitives/spine/bw_127.png", "primitives/spine/bw_128.png", "primitives/spine/bw_129.png", "primitives/spine/bw_130.png", "primitives/spine/bw_131.png", "primitives/spine/bw_132.png", "primitives/spine/bw_133.png", "primitives/spine/bw_134.png", "primitives/spine/bw_135.png", "primitives/spine/bw_136.png", "primitives/spine/bw_137.png", "primitives/spine/bw_138.png", "primitives/spine/bw_139.png", "primitives/spine/bw_140.png", "primitives/spine/bw_141.png", "primitives/spine/bw_142.png", "primitives/spine/bw_143.png", "primitives/spine/bw_144.png"], "frame_sha12": ["dcc13095edfe", "231035085f52", "4eb300be43be", "6be93ef20a9e", "6fe5afcf9496", "2d61f49addc5", "35d1e1d5d324", "fc68a7bf0bdf", "85784d26bc63", "190652e283d2", "8819239df24e", "d3d40c1d089d", "dd5392396d8b", "cb5842869507", "693a25b37f6a", "7cb3ade3e167", "b5d5931ec6c1", "5cb21732533a", "5f768aee781c", "9d61eb254305", "3e52fdb4ba95", "aefc4ae2393c", "1997a703213c", "05f6acf00e41", "57d18356514d", "1049a1fa3e7f", "d05599a598af", "143972de6f66", "149d45b6c8c1", "421adcda182c", "b5fb65e289f7", "f355cb8299a1", "03657fea7eb2", "3102ea4f07e2", "f43e2eb59056", "b19554f9dd75", "d9b1ef658c38", "5f06ad4e8731", "5d9240604dbf", "c820b4368be5", "9483f67c156d", "5b3679ac4e33", "50a832d9ca7c", "c8dd0450be68", "6be39b836857", "f661ea022511", "9102750e1f12", "b07bce547254", "8c7c9138c88e", "3179849adc95", "bc8b1838cde0", "8f46a6ef6c78", "0c3ea0cb295a", "90902c8b3445", "cbd3aae1a978", "4a6263ed098e", "776bdacb9a2f", "e7f3e6da686e", "8942530e8942", "79d1933ce0f2", "4cc31d5d4c03", "01d9aa47d80e", "50605376ce9c", "3db97076fbce", "54bcf8553803", "4376e8beeb60", "2d48871daf23", "b1700a78f144", "12dfed7bbbaf", "36bacae821fc", "2e42b4f87dbe", "2e744b3b63a2", "11abf611cc89", "fe09dc22680b", "15b2579047a8", "da0e5882f3a7", "eada3f873eed", "3019f3d62937", "cf2b08731b85", "15929cb85a8a", "2eae5dda6798", "5396c7bf6ea2", "32b9d71ca549", "2328289113c2", "b2ca9ce427cd", "76799bab6a5f", "ce1f6dd45b62", "d4aa6d9bebe5", "727b684ab2a0", "85bf43aa2fc1", "63e279ab70f8", "8f943ded3cbf", "0a03a366e620", "1d7451a6d0df", "d118ac2185d7", "249507be4f23", "38f95bf87753", "13807542986c", "64db4b95f421", "b455cad409bf", "6d9f0790d897", "6289f2aeff6d", "fc1d5ffaab24", "294322a8ed16", "601fde987914", "377e547753e4", "072d57aa34e0", "2e77bea7b445", "668feee25b9b", "818ffa085668", "3911f43c4fa9", "37cb154dcd6a", "642e5f580d7d", "a2590acb60ef", "a26ee22e1769", "3268104dcbfd", "9adc13713cc6", "03353f9b419a", "f1cf0e7141d8", "601da4729278", "732e3505444b", "03b28b67e6bf", "0689efd901f9", "9b1d40d99a7d", "01e5d2b0d32f", "ddaf535741e6", "7a417b5302c0", "2b4bd57fba70", "b4727b70e68a", "2f979fa5ee86", "59bed0d55fea", "d29bc7985e6e", "cd0c50bc7987", "8ff9b31947cf", "ed0a3116557d", "976379b0065f", "c96a5b7a24bc", "89847ea80fbf", "d4a9f14ffaaa", "b703f2e628bb", "1154a537f240", "bfa3c2a55154", "99547e02f048", "06447d1b3489", "7f089f5afcdb"], "fps": 24, "loop": false, "scale": 1.0, "cell": [485, 581], "pool_centre_px": [247.7, 343.5], "timeline_s": {"contact": 0.0, "flash_peak": 0.17, "pool_stable": 0.75, "steady_end": 4.0, "dies_out": 4.6, "scorch_still_from": 5.0}, "scorch_frame": 144, "tick_schedule_s": [0, 1, 2], "smoke": {"alpha": 0.22, "rise_px_s": 22, "end_s": 6.0, "tint": [0.35, 0.3, 0.28]}, "floor_light": {"peak_alpha": 0.35, "steady_alpha": 0.15, "end_s": 5.0}}, "smoke_shader": "res://vfx/blackwater_cocktail_e3_V/materials/ending_smoke.gdshader", "smoke_texture": "res://vfx/blackwater_cocktail_e3_V/derived/smoke_noise.png", "floor_texture": "res://vfx/blackwater_cocktail_e3_V/derived/floor.png", "palette_2": [1, 0.55, 0.12, 1]}]

# Selection is live; cast_kit_index is captured before playing the cast frames.
var vfx_kit_index: int = 0
var cast_kit_index: int = 0
var vfx_label: Label

func _load_vfx_picker() -> void:
    var hud := CanvasLayer.new()
    hud.name = "VFXPicker"
    hud.layer = 10
    add_child(hud)
    vfx_label = Label.new()
    vfx_label.name = "Label"
    vfx_label.position = Vector2(16, 16)
    vfx_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
    vfx_label.add_theme_font_size_override("font_size", 22)
    vfx_label.add_theme_color_override("font_color", Color.WHITE)
    vfx_label.add_theme_color_override("font_outline_color", Color(0.04, 0.05, 0.08, 1))
    vfx_label.add_theme_constant_override("outline_size", 4)
    hud.add_child(vfx_label)
    _update_vfx_label()

func _update_vfx_label() -> void:
    vfx_label.text = "VFX: " + VFX_KITS[vfx_kit_index]["name"] + "  (Tab)"
