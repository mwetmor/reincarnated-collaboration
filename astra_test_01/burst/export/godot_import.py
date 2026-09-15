"""Build a self-contained Godot 4.6 review stub; no art transformations.

Usage: python3 -B -m export.godot_import --cells DIR --out PROJECT
       [--vfx DIR] [--gear-variant DIR] [--scene DIR | --parallax DIR [--props DIR]]
Cells can be nested cut outputs or a frames/<animation>/<direction> tree.
Frames must be <animation>_<direction>_<zero-based-number>.png.
"""
import argparse
import json
import math
from pathlib import Path
import re
import shutil
import time

from PIL import Image

DIRECTIONS = ('S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE')
FPS = {'idle': 8, 'walk': 12, 'run': 12, 'jump': 12, 'cast': 20}
FRAME = re.compile(r'(idle|walk|run|jump|cast)_(S|SW|W|NW|N|NE|E|SE)_(\d+)\.png')
VIDEO = re.compile(r'(idle|walk|run|jump|cast)_(S|SW|W|NW|N|NE|E|SE)(?:_(1to1|2x))?\.mp4')


def local_file(path, root):
    path, root = Path(path), Path(root).resolve()
    if not path.resolve().is_relative_to(root) or not path.is_file():
        raise ValueError('Missing or escaping input asset: ' + str(path))
    return path


def _nearby(folder, root, filename):
    while True:
        candidate = folder / filename
        if candidate.exists():
            return local_file(candidate, root)
        if folder == root:
            return None
        folder = folder.parent


def discover_cells(cells, allow_video=False):
    """Return cells by animation_direction; reject duplicate/gapped/bad PNGs.

    Nearby registration.json supplies explicit fps_out/fps_output to the
    viewer only. Legacy native fps is ignored. numbers.json is retained as-is.
    Packet-only MP4s are supported for the viewer, never for engine export.
    """
    root = Path(cells).resolve()
    if not root.is_dir():
        raise ValueError('Cells directory does not exist')
    result = {}
    for path in sorted(root.rglob('*.png')):
        if any(part in ('sheets', 'img', 'evidence', 'rest') for part in path.relative_to(root).parts[:-1]):
            continue
        match = FRAME.fullmatch(path.name)
        if not match:
            # Diagnostic rasters and the unnumbered rest reference are not cells.
            if path.name.startswith(tuple(a+'_' for a in FPS)):
                raise ValueError('Malformed numbered frame: ' + path.name)
            continue
        local_file(path, root)
        anim, direction, index = match.groups()
        name = anim+'_'+direction
        entry = result.setdefault(name, {'anim': anim, 'direction': direction,
                                         'folder': path.parent, 'frames': []})
        if entry['folder'] != path.parent:
            raise ValueError('Duplicate cell: ' + name)
        entry['frames'].append((int(index), path))
    if allow_video:
        for path in sorted(root.rglob('*.mp4')):
            match = VIDEO.fullmatch(path.name)
            if not match:
                continue
            local_file(path, root)
            anim, direction, suffix = match.groups()
            name = anim+'_'+direction
            entry = result.setdefault(name, {'anim': anim, 'direction': direction,
                                             'folder': path.parent, 'frames': []})
            rank = {'1to1': 0, None: 1, '2x': 2}[suffix]
            if 'video' in entry and entry['video'].parent != path.parent:
                raise ValueError('Duplicate video cell: '+name)
            if rank < entry.get('video_rank', 99):
                entry.update(video=path, video_rank=rank)
    for name, entry in result.items():
        indexed = sorted(entry['frames'])
        if [i for i, _ in indexed] != list(range(len(indexed))):
            raise ValueError('Frame indices must start at zero without gaps: '+name)
        entry['frames'] = [p for _, p in indexed]
        for path in entry['frames']:
            with Image.open(path) as im:
                if im.size != (512, 512) or im.mode != 'RGBA':
                    raise ValueError('Registered frames must be 512x512 RGBA: '+str(path))
                im.verify()
        metadata = _nearby(entry['folder'], root, 'registration.json')
        metadata = json.loads(metadata.read_text()) if metadata else {}
        if not isinstance(metadata, dict):
            raise ValueError('registration.json must be an object')
        fps = metadata.get('fps_out', metadata.get('fps_output', FPS[entry['anim']]))
        if isinstance(fps, bool) or not isinstance(fps, (int, float)) or not math.isfinite(fps) or fps <= 0:
            raise ValueError('Output fps must be finite and positive')
        entry['fps'] = fps
        numbers = _nearby(entry['folder'], root, 'numbers.json')
        entry['numbers'] = json.loads(numbers.read_text()) if numbers else []
        # Strict JSON also prevents NaN from producing invalid embedded viewer data.
        json.dumps(entry['numbers'], allow_nan=False)
    return result


def _output(out, inputs):
    out = Path(out).resolve()
    for source in inputs:
        if source is not None:
            source = Path(source).resolve()
            if out.is_relative_to(source) or source.is_relative_to(out):
                raise ValueError('Output and input directories must not overlap')
    if out.exists() and any(out.iterdir()):
        raise ValueError('Output directory must be empty (prevents stale assets)')
    out.mkdir(parents=True, exist_ok=True)
    return out


def write_spriteframes(out, resource, animations, frame_durations=None):
    """Write SpriteFrames from {name: (relative_texture_paths, fps, loop)}.

    Optional frame_durations maps every name to per-frame seconds. Godot stores
    seconds * fps as its duration multiplier. Omission retains legacy bytes.
    """
    if frame_durations is not None:
        if set(frame_durations) != set(animations):
            raise ValueError('Durations must match animations')
        for name, (paths, fps, loop) in animations.items():
            values = frame_durations[name]
            if len(values) != len(paths) or any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v <= 0 for v in values):
                raise ValueError('Durations must be positive and match frame counts')
    textures = []
    blocks = []
    for name, (paths, fps, loop) in sorted(animations.items()):
        frames = []
        for index, path in enumerate(paths):
            local_file(out/path, out)
            ident = str(len(textures)+1)
            textures.append(f'[ext_resource type="Texture2D" path="res://{path}" id="{ident}"]')
            duration = '1.0' if frame_durations is None else repr(float(frame_durations[name][index])*fps)
            frames.append('{"duration": '+duration+', "texture": ExtResource("'+ident+'")}')
        blocks.append('{"frames": ['+',\n'.join(frames)+'], "loop": '+str(loop).lower()+
                      ', "name": &'+json.dumps(name)+', "speed": '+str(float(fps))+'}')
    target = out/resource
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('[gd_resource type="SpriteFrames" load_steps='+str(len(textures)+1)+
                      ' format=3]\n\n'+'\n'.join(textures)+'\n\n[resource]\nanimations = ['+
                      ',\n'.join(blocks)+']\n')


def validate_resources(project, include_scenes=False):
    """Re-read resources and verify all referenced res:// files stay in project."""
    root = Path(project).resolve()
    references = []
    for resource in sorted(root.rglob('*.tres')):
        text = resource.read_text()
        if not text.startswith('[gd_resource type="SpriteFrames"') or 'animations = [' not in text:
            raise ValueError('Not a SpriteFrames resource: '+str(resource))
        for path in re.findall(r'path="res://([^"\n]+)"', text):
            local_file(root/path, root)
            references.append(path)
        declared = set(re.findall(r'\[ext_resource [^\n]+ id="([^"]+)"\]', text))
        used = set(re.findall(r'ExtResource\("([^"]+)"\)', text))
        if declared != used or not used:
            raise ValueError('Invalid texture resource references')
    if not references:
        raise ValueError('No texture resources')
    if include_scenes:
        for resource in sorted(root.rglob('*.tscn')):
            text = resource.read_text()
            if not text.startswith('[gd_scene ') or '[node ' not in text:
                raise ValueError('Invalid scene header or missing root node')
            declarations = re.findall(r'\[ext_resource [^\n]+ id="([^"]+)"\]', text)
            used = set(re.findall(r'ExtResource\("([^"]+)"\)', text))
            if len(set(declarations)) != len(declarations) or set(declarations) != used:
                raise ValueError('Invalid scene external resource references')
            for path in re.findall(r'path="res://([^"\n]+)"', text):
                local_file(root/path, root)
                references.append(path)
            sub = set(re.findall(r'\[sub_resource [^\n]+ id="([^"]+)"\]', text))
            if sub != set(re.findall(r'SubResource\("([^"]+)"\)', text)):
                raise ValueError('Invalid scene subresource references')
        settings = (root/'project.godot').read_text()
        main = re.search(r'^run/main_scene="res://([^"\n]+)"$', settings, re.MULTILINE)
        if main is None:
            raise ValueError('Missing project main_scene')
        local_file(root/main[1], root)
        references.append(main[1])
    return references


KEEPER_SCRIPT = '''extends CharacterBody2D

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

func _ready() -> void:
    base_frames = sprite.sprite_frames
    if ResourceLoader.exists("res://frames/keeper_advanced.tres"):
        advanced_frames = load("res://frames/keeper_advanced.tres")
    if ResourceLoader.exists("res://vfx/frost_bolt.tres"):
        frost_frames = load("res://vfx/frost_bolt.tres")
    sprite.animation_finished.connect(_animation_finished)
    _play_state()

func _physics_process(delta: float) -> void:
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
    var input_vector: Vector2 = Input.get_vector("move_left", "move_right", "move_up", "move_down")
    if input_vector.length_squared() > 0.0:
        facing = DIRECTIONS[posmod(roundi(input_vector.angle() / (PI / 4.0)) + 6, 8)]
    if Input.is_action_just_pressed("cast"):
        state = "cast"
        velocity = Vector2.ZERO
        _play_state()
        _spawn_frost()
        return
    if Input.is_action_just_pressed("jump"):
        state = "jump"
        velocity = Vector2.ZERO
        _play_state()
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
        for kind in ["walk", "run", "jump", "cast"]:
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
'''


def _project_settings():
    keys = {'move_left': [4194319, 65], 'move_right': [4194321, 68],
            'move_up': [4194320, 87], 'move_down': [4194322, 83],
            'jump': [32], 'cast': [69], 'gear_toggle': [71], 'run_modifier': [4194325]}
    actions = []
    for name, codes in keys.items():
        events = ['Object(InputEventKey,"physical_keycode":'+str(code)+')' for code in codes]
        if name == 'cast':
            events.append('Object(InputEventMouseButton,"button_index":1)')
        actions.append(name+'={"deadzone":0.2,"events":['+','.join(events)+']}')
    return '''config_version=5

[application]
config/name="Keeper cell review stub"
run/main_scene="res://scenes/main.tscn"

[debug]
file_logging/enable_file_logging=false

[display]
window/size/viewport_width=960
window/size/viewport_height=640

[rendering]
renderer/rendering_method="gl_compatibility"
textures/canvas_textures/default_texture_filter=2
environment/defaults/default_clear_color=Color(0.09, 0.12, 0.17, 1)

[input]
'''+ '\n'.join(actions)+'\n'


def build_project(cells, out, vfx=None, gear_variant=None, scene=None, vfx_kit=None, sockets=None, parallax=None, props=None, vfx_kits=None):
    started = time.monotonic()
    if vfx_kits is not None and (vfx_kit is not None or vfx is not None):
        raise ValueError('Choose --vfx-kits, --vfx-kit or legacy --vfx')
    if vfx_kits is not None and sockets is None:
        raise ValueError('--vfx-kits requires --sockets')
    kits = _load_vfx_kits(vfx_kits) if vfx_kits is not None else None
    base = discover_cells(cells)
    advanced = discover_cells(gear_variant) if gear_variant is not None else None
    if not base or advanced == {}:
        raise ValueError('Each supplied character set needs at least one cell')
    effects = {}
    if vfx is not None:
        root = Path(vfx).resolve()
        if not root.is_dir():
            raise ValueError('VFX directory does not exist')
        for path in sorted(root.rglob('*.png')):
            match = re.fullmatch(r'(cast|travel|impact|frost_bolt)_(\d+)\.png', path.name)
            if not match:
                raise ValueError('VFX frames must use cast/travel/impact/frost_bolt_N.png')
            local_file(path, root)
            with Image.open(path) as im:
                if im.mode != 'RGBA':
                    raise ValueError('VFX frames must be RGBA')
                im.verify()
            name, index = match.groups()
            effects.setdefault(name, []).append((int(index), path))
        if not effects:
            raise ValueError('VFX directory contains no frames')
        for name, frames in effects.items():
            frames.sort()
            if [i for i, _ in frames] != list(range(len(frames))):
                raise ValueError('VFX indices must be contiguous from zero: '+name)
    if props is not None and parallax is None:
        raise ValueError("--props requires --parallax")
    props_data = None
    if props is not None:
        from export.props_layer import load_props
        props_data = load_props(props)
    parallax_data = None
    if parallax is not None:
        if scene is not None:
            raise ValueError("Choose --scene or --parallax")
        from export.parallax_scene import load_parallax
        parallax_data = load_parallax(parallax)
    annotation = None
    if scene is not None:
        from export.scene_kit import load_annotation
        scene = Path(scene).resolve()
        annotation = load_annotation(local_file(scene/'annotation.json', scene))
        with Image.open(local_file(scene/'plate.png', scene)) as plate:
            if list(plate.size) != annotation['plate_size']:
                raise ValueError('Plate image size differs from plate_size')
            plate.verify()
    kit = _load_vfx_kit(vfx_kit) if vfx_kit is not None else None
    if sockets is not None and kit is None and kits is None:
        raise ValueError('--sockets requires --vfx-kit or --vfx-kits')
    if kit is not None and vfx is not None:
        raise ValueError('Choose legacy --vfx or directional --vfx-kit')
    socket_data = None
    if sockets is not None:
        from export.sockets import load_sockets
        socket_data = load_sockets(sockets, base)
    out = _output(out, [cells, vfx, gear_variant, scene, vfx_kit, sockets, parallax, props,
                        vfx_kits] + [k['root'] for k in kits or []])
    for entries, prefix, resource in [(base, 'sprites', 'frames/keeper.tres'),
                                       (advanced, 'sprites_advanced', 'frames/keeper_advanced.tres')]:
        if entries is None:
            continue
        animations = {}
        for name, entry in sorted(entries.items()):
            paths = []
            for source in entry['frames']:
                relative = Path(prefix)/entry['anim']/entry['direction']/source.name
                (out/relative).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, out/relative)
                paths.append(relative.as_posix())
            fps = FPS[entry['anim']]
            if parallax_data is not None and 'movement' in parallax_data and entry['anim'] in ('walk', 'run'):
                fps = parallax_data['movement'][entry['anim']+'_anim_fps']
            animations[name] = (paths, fps, entry['anim'] not in ('jump', 'cast'))
        write_spriteframes(out, resource, animations)
    if effects:
        animations = {}
        for name, frames in effects.items():
            paths = []
            for _, source in frames:
                relative = Path('vfx')/'sprites'/name/source.name
                (out/relative).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, out/relative)
                paths.append(relative.as_posix())
            animations[name] = (paths, 20, name == 'travel')
        write_spriteframes(out, 'vfx/frost_bolt.tres', animations)
    (out/'project.godot').write_text(_project_settings())
    (out/'scripts').mkdir()
    (out/'scripts/keeper.gd').write_text(KEEPER_SCRIPT)
    (out/'scenes').mkdir()
    (out/'scenes/main.tscn').write_text('''[gd_scene load_steps=3 format=3]

[ext_resource type="Script" path="res://scripts/keeper.gd" id="1"]
[ext_resource type="SpriteFrames" path="res://frames/keeper.tres" id="2"]

[node name="Main" type="Node2D"]

[node name="Floor" type="Polygon2D" parent="."]
polygon = PackedVector2Array(-10000, -10000, 10000, -10000, 10000, 10000, -10000, 10000)
color = Color(0.18, 0.22, 0.28, 1)

[node name="Keeper" type="CharacterBody2D" parent="."]
position = Vector2(480, 400)
script = ExtResource("1")
motion_mode = 1

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="Keeper"]
sprite_frames = ExtResource("2")
centered = false
offset = Vector2(-256, -400)

[node name="Camera2D" type="Camera2D" parent="Keeper"]
position = Vector2(0, -100)
''')
    (out/'README.md').write_text('''# Keeper cell review stub — Godot 4.6

Open project.godot. Arrows/WASD move; Shift runs; Space jumps; E or left
mouse casts; G switches gear when an advanced set was supplied.
Eight directions rotate the selected cell, never mirror its pixels.
The screen projection and light are baked into the supplied images.
PNG bytes are copied unchanged; offset (-256,-400) anchors the feet pivot.
Linear filtering is enabled. Idle=8, walk/run/jump=12, cast=20 fps;
jump/cast do not loop. Missing directions choose the nearest circular
direction within the state; missing states try idle, then another state.
Each missing request prints once. Ties follow S SW W NW N NE E SE.
Action states return to idle on animation_finished; a loop-only fallback
returns after one fallback cycle. No combat logic or collision geometry.

Optional gear uses a second complete SpriteFrames resource. Optional VFX
accepts numbered cast/travel/impact/frost_bolt PNGs at 20 fps. Casting
spawns an effect at the exported staff_tip_offset relative to the feet.
The default (0,-160) is a configurable stub offset, not a measured socket.
Non-loop effects free on completion; travel-only effects free after 1 s.

Build using python3 -B -m export.godot_import --cells DIR --out EMPTY_DIR
[--gear-variant DIR] [--vfx DIR]. Input cells have contiguous zero-based
animation_DIRECTION_N.png, 512x512 RGBA. Output directories must be empty.
No resampling, external assets, dependencies, or network are required.
The project requests file logging disabled; this did not prevent the bundled
macOS engine's logger startup under the restricted acceptance environment.
Godot editor settings and user-data setup still use the engine's normal OS
locations, which must be writable for a completely clean headless import.
''')
    scene_report = _write_tower(out, scene, annotation) if annotation is not None else None
    parallax_report = None
    if parallax_data is not None:
        from export.parallax_scene import write_cliffside
        parallax_report = write_cliffside(out, parallax_data, props=props_data)
    kit_report = _write_vfx_kit(out, kit, base, cells, socket_data, annotation) if kit is not None else None
    kits_report = _write_vfx_kits(out, kits, base, cells, socket_data, annotation) if kits is not None else None
    refs = validate_resources(out)
    if scene_report is not None:
        scene_report['resource_references'] = len(validate_resources(out, include_scenes=True))
    if parallax_report is not None:
        parallax_report['resource_references'] = len(validate_resources(out, include_scenes=True))
    return {'cells': sorted(base), 'frames': sum(len(e['frames']) for e in base.values()),
            'texture_references': len(refs), 'gear_cells': len(advanced or {}),
            'vfx_animations': len(effects), **({'parallax': parallax_report} if parallax_report is not None else {}), **({'vfx_kit': kit_report} if kit_report is not None else {}), **({'vfx_kits': kits_report} if kits_report is not None else {}), **({'scene': scene_report} if scene_report is not None else {}), 'wall_s': time.monotonic()-started}


def _write_tower(out, scene, annotation):
    """Add the plate room; registered frame bytes and sandbox scene stay intact."""
    from export.scene_kit import collision, cut_occluders, shadow_texture
    w, h = annotation['plate_size']
    height = annotation['figure_height_px']
    scale = height/240.0
    zoom = max(1536.0/w, 1024.0/h)  # Fill: crop excess on mismatched aspect ratios.
    target = out/'scene'
    target.mkdir()
    shutil.copyfile(scene/'plate.png', target/'plate.png')
    shutil.copyfile(scene/'annotation.json', target/'annotation.json')
    cuts = cut_occluders(scene/'plate.png', annotation, target/'occluders')
    shadow_texture(target/'shadow.png')
    polygons = collision(annotation)
    external = [
        '[ext_resource type="Script" path="res://scripts/keeper.gd" id="1"]',
        '[ext_resource type="SpriteFrames" path="res://frames/keeper.tres" id="2"]',
        '[ext_resource type="Texture2D" path="res://scene/plate.png" id="3"]',
        '[ext_resource type="Texture2D" path="res://scene/shadow.png" id="4"]']
    for i, cut in enumerate(cuts, 5):
        external.append(f'[ext_resource type="Texture2D" path="res://scene/occluders/{cut["file"]}" id="{i}"]')

    def vector(p):
        return 'Vector2('+', '.join(format(float(v), '.12g') for v in p)+')'

    def packed(points):
        return 'PackedVector2Array('+', '.join(format(float(v), '.12g') for p in points for v in p)+')'

    # Godot advises against non-uniform CollisionShape2D scaling. Approximate
    # the ellipse with 32 convex vertices at actual plate-pixel dimensions.
    feet = [[height*0.11*math.cos(i*math.tau/32), height*0.04*math.sin(i*math.tau/32)]
            for i in range(32)]
    nodes = f'''[sub_resource type="ConvexPolygonShape2D" id="Feet"]
points = {packed(feet)}

[node name="Tower" type="Node2D"]

[node name="Plate" type="Sprite2D" parent="."]
z_index = -10
texture = ExtResource("3")
centered = false

[node name="World" type="Node2D" parent="."]
y_sort_enabled = true

[node name="Keeper" type="CharacterBody2D" parent="World"]
position = {vector(annotation['spawn'])}
script = ExtResource("1")
motion_mode = 1
walk_speed = {150.0*scale:.12g}
run_speed = {250.0*scale:.12g}
staff_tip_offset = {vector([0, -160*scale])}

[node name="ContactShadow" type="Sprite2D" parent="World/Keeper"]
z_index = -1
texture = ExtResource("4")
scale = {vector([height*0.22/64, height*0.08/20])}

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="World/Keeper"]
sprite_frames = ExtResource("2")
centered = false
offset = Vector2(-256, -400)
scale = {vector([scale, scale])}

[node name="CollisionShape2D" type="CollisionShape2D" parent="World/Keeper"]
shape = SubResource("Feet")
'''
    for i, cut in enumerate(cuts, 5):
        with Image.open(target/'occluders'/cut['file']) as image:
            width = image.width
        x0, y0 = cut['position']
        origin = [x0+width/2, cut['baseline_y']]
        nodes += f'''
[node name="Occluder_{Path(cut['file']).stem}" type="Sprite2D" parent="World"]
position = {vector(origin)}
texture = ExtResource("{i}")
centered = false
offset = {vector([x0-origin[0], y0-origin[1]])}
'''
    nodes += '\n[node name="Walls" type="StaticBody2D" parent="."]\n'
    for i, polygon in enumerate(polygons):
        nodes += f'''
[node name="Collision_{i}" type="CollisionPolygon2D" parent="Walls"]
polygon = {packed(polygon)}
'''
    nodes += f'''
[node name="Camera2D" type="Camera2D" parent="."]
position = {vector([w/2, h/2])}
zoom = {vector([zoom, zoom])}
limit_left = 0
limit_top = 0
limit_right = {w}
limit_bottom = {h}
position_smoothing_enabled = false
'''
    (out/'scenes/tower.tscn').write_text(
        f'[gd_scene load_steps={len(external)+2} format=3]\n\n'+'\n'.join(external)+'\n\n'+nodes)
    settings = _project_settings().replace('res://scenes/main.tscn', 'res://scenes/tower.tscn')
    settings = settings.replace('viewport_width=960', 'viewport_width=1536')
    settings = settings.replace('viewport_height=640', 'viewport_height=1024\nwindow/stretch/mode="canvas_items"')
    (out/'project.godot').write_text(settings)
    readme = (out/'README.md').read_text().replace('No combat logic or collision geometry.', 'No combat logic. The tower scene supplies floor collisions.')
    readme += f'''

Tower room: scenes/tower.tscn is the main scene; scenes/main.tscn remains
available as the original sandbox. Annotation geometry is in plate pixels.
World sorts the Keeper and cutouts by their feet/baseline y coordinate.
Cutouts feather inward by one pixel. The body uses a 32-vertex convex feet
ellipse (width 0.22 * figure height); only the art sprite is scaled.
Figure height: {height:g} px; sprite/movement scale: {scale:g}.
The fixed camera fills 1536 x 1024 at zoom {zoom:g}; excess plate content
is cropped symmetrically for mismatched aspect ratios. Exits are retained
in scene/annotation.json as annotation metadata; no transition logic.
'''
    (out/'README.md').write_text(readme)
    return {'plate_size': [w, h], 'occluders': len(cuts), 'collision_polygons': len(polygons),
            'figure_height_px': height, 'scale': scale, 'feet_width_px': height*0.22,
            'walk_speed': 150*scale, 'run_speed': 250*scale, 'camera_zoom': zoom,
            'camera_visible_plate_px': [1536/zoom, 1024/zoom]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cells', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--vfx')
    parser.add_argument('--gear-variant')
    parser.add_argument('--scene')
    parser.add_argument('--parallax')
    parser.add_argument('--props')
    kit_group = parser.add_mutually_exclusive_group()
    kit_group.add_argument('--vfx-kit')
    kit_group.add_argument('--vfx-kits')
    parser.add_argument('--sockets')
    args = parser.parse_args()
    print(json.dumps(build_project(args.cells, args.out, args.vfx, args.gear_variant, args.scene, args.vfx_kit, args.sockets, args.parallax, args.props, args.vfx_kits), indent=2))




def _load_vfx_kits(path):
    """Validate the whole ordered catalogue before writing any project files.

    Relative kit directories are relative to KITS_JSON, not the shell cwd.
    Each entry retains the exact T3i kit validation, including impact_range.
    """
    path = Path(path).resolve()
    if not path.is_file():
        raise ValueError('Missing VFX kits JSON')
    data = json.loads(path.read_text())
    if (not isinstance(data, dict) or set(data) != {'kits'}
            or not isinstance(data['kits'], list) or not 1 <= len(data['kits']) <= 12):
        raise ValueError('VFX kits requires exactly kits: a list of 1..12 entries')
    result, names = [], set()
    for entry in data['kits']:
        if (not isinstance(entry, dict) or not {'name', 'dir'} <= set(entry)
                or set(entry) - {'name', 'dir', 'tint'}):
            raise ValueError('Kit requires name, dir and optional tint only')
        name = entry['name']
        if (not isinstance(name, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', name)
                or name.casefold() in names):
            raise ValueError('Kit names must be unique safe identifiers (case-insensitive)')
        names.add(name.casefold())
        directory = entry['dir']
        if not isinstance(directory, str) or not directory or '\x00' in directory:
            raise ValueError('Kit dir must be a nonempty path')
        if 'tint' in entry:
            tint = entry['tint']
            if (not isinstance(tint, list) or len(tint) != 3
                    or any(isinstance(v, bool) or not isinstance(v, (float, int))
                           or not math.isfinite(v) or not 0 <= v <= 1 for v in tint)):
                raise ValueError('Kit tint must contain three finite components in [0,1]')
        kit = _load_vfx_kit(path.parent/directory)
        result.append({**kit, 'name': name, **({'tint': entry['tint']} if 'tint' in entry else {})})
    return result


def _load_vfx_kit(directory):
    root = Path(directory).resolve()
    if not root.is_dir():
        raise ValueError('VFX kit directory does not exist')
    selection = root/'vfx_select.json'
    selection = json.loads(local_file(selection, root).read_text()) if selection.exists() else {}
    if not isinstance(selection, dict):
        raise ValueError('vfx_select.json must be an object')
    result = {'root': root, 'credits': local_file(root/'CREDITS.txt', root).read_text()}
    for name in ('flare', 'impact'):
        frames = []
        for path in (root/name).glob('*.png'):
            match = re.fullmatch(name+r'_(\d+)\.png', path.name)
            if match is None:
                raise ValueError('Malformed kit frame: '+path.name)
            local_file(path, root)
            with Image.open(path) as im:
                if im.mode != 'RGBA':
                    raise ValueError('Kit frames must be RGBA')
                im.verify()
            frames.append((int(match[1]), path))
        frames.sort()
        if not frames or [i for i, _ in frames] != list(range(len(frames))):
            raise ValueError('Kit indices must be contiguous from zero: '+name)
        if name == 'impact' and 'impact_range' in selection:
            r = selection['impact_range']
            if not isinstance(r, list) or len(r) != 2 or any(isinstance(v, bool) or not isinstance(v, int) for v in r) or not 0 <= r[0] <= r[1] < len(frames):
                raise ValueError('impact_range must be inclusive [first,last] frame indices')
            frames = frames[r[0]:r[1]+1]
        result[name] = [p for _, p in frames]
    if (root/'kit.json').exists():
        from export.effect_kit import load_kit
        result['effect'] = load_kit(root)
        # Metadata is authoritative for authored frame order and durations.
        for phase, record in result['effect']['phases'].items():
            name = 'flare' if phase == 'cast' else phase
            result[name] = [root/f['file'] for f in record['frames']]
    return result


RADIAL_RESOURCES = '''[sub_resource type="CanvasItemMaterial" id="Additive"]
blend_mode = 1

[sub_resource type="Gradient" id="RadialColors"]
offsets = PackedFloat32Array(0, 0.25, 1)
colors = PackedColorArray(1, 1, 1, 1, 0.35, 0.9, 1, 0.7, 0.1, 0.6, 1, 0)

[sub_resource type="GradientTexture2D" id="Dot"]
gradient = SubResource("RadialColors")
width = 32
height = 32
fill = 1
fill_from = Vector2(0.5, 0.5)
fill_to = Vector2(1, 0.5)

[sub_resource type="Gradient" id="CometColors"]
offsets = PackedFloat32Array(0, 0.35, 1)
colors = PackedColorArray(1, 1, 1, 1, 0.1, 0.85, 1, 0.8, 0.1, 0.65, 1, 0)

[sub_resource type="Curve" id="Shrink"]
_data = [Vector2(0, 1), 0.0, -1.0, 0, 0, Vector2(1, 0), -1.0, 0.0, 0, 0]
point_count = 2
'''

BOLT_SCRIPT = '''extends Area2D

var direction: Vector2 = Vector2.DOWN
var spell_scale: float = 1.0
var distance: float = 0.0
var expired: bool = false
var caster: CollisionObject2D

func _ready() -> void:
    body_entered.connect(_on_body_entered)
    $Head.scale = Vector2.ONE * 0.55 * spell_scale
    $Trail.direction = -direction
    $Trail.initial_velocity_min = 40.0 * spell_scale
    $Trail.initial_velocity_max = 60.0 * spell_scale
    $Trail.scale_amount_min = 0.10 * spell_scale
    $Trail.scale_amount_max = 0.20 * spell_scale
    $CollisionShape2D.shape = $CollisionShape2D.shape.duplicate()
    $CollisionShape2D.shape.radius = 3.0 * spell_scale

func _physics_process(delta: float) -> void:
    if expired:
        return
    var step: float = minf(520.0 * spell_scale * delta, 650.0 * spell_scale - distance)
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
    $Head.hide()
    $Trail.emitting = false
    set_deferred("monitoring", false)
    var effect: Node2D = preload("res://scenes/frost_impact.tscn").instantiate()
    effect.spell_scale = spell_scale
    get_parent().add_child(effect)
    effect.global_position = global_position
    get_tree().create_timer(0.4).timeout.connect(queue_free)
'''

IMPACT_SCRIPT = '''extends Node2D

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
'''

DIRECTIONAL_KEEPER = '''
# Directional kit: sockets refer to the actual displayed animation/frame.
var socket_cells: Dictionary = {}
var cast_fired: bool = false
var active_flare: AnimatedSprite2D
const FACING_VECTORS = {"S": Vector2(0,1), "SW": Vector2(-1,1),
    "W": Vector2(-1,0), "NW": Vector2(-1,-1), "N": Vector2(0,-1),
    "NE": Vector2(1,-1), "E": Vector2(1,0), "SE": Vector2(1,1)}

func _load_directional_kit() -> void:
    var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://sockets.json"))
    socket_cells = data.cells
    sprite.frame_changed.connect(_cast_frame_changed)

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
    var socket: Variant = _socket_world()
    if socket == null:
        push_warning("No measured release socket: " + String(sprite.animation))
        return
    var direction: Vector2 = FACING_VECTORS[facing].normalized()
    var art_scale: float = sprite.global_transform.x.length()
    var flare := AnimatedSprite2D.new()
    flare.sprite_frames = preload("res://vfx/flare.tres")
    var additive := CanvasItemMaterial.new()
    additive.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
    flare.material = additive
    get_parent().add_child(flare)
    flare.global_position = socket
    flare.rotation = direction.angle()
    flare.scale = Vector2.ONE * art_scale
    flare.animation_finished.connect(flare.queue_free, CONNECT_ONE_SHOT)
    flare.play("flare")
    active_flare = flare
    var bolt: Area2D = preload("res://scenes/frost_bolt.tscn").instantiate()
    bolt.direction = direction
    bolt.spell_scale = art_scale
    bolt.caster = self
    get_parent().add_child(bolt)
    bolt.global_position = socket

func _process(_delta: float) -> void:
    if state == "cast" and is_instance_valid(active_flare):
        var socket: Variant = _socket_world()
        if socket != null:
            active_flare.global_position = socket
'''


def _write_vfx_kit(out, kit, base, cells, socket_data, annotation, kit_name=None, tint=None):
    # Named exports reuse the T3i scene/script templates. The absent-name path
    # deliberately keeps every legacy byte, filename and report key intact.
    resource_root = 'vfx' if kit_name is None else 'vfx/'+kit_name
    prefix = 'frost' if kit_name is None else 'vfx_'+kit_name
    if socket_data is None:
        from export.sockets import build_sockets
        socket_data = build_sockets(cells, out/'sockets.json')
    else:
        (out/'sockets.json').write_text(json.dumps(socket_data, indent=2, allow_nan=False)+'\n')
    counts = {}
    for name in ('flare', 'impact'):
        paths = []
        for source in kit[name]:
            relative = Path(resource_root)/'sprites'/name/source.name
            (out/relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, out/relative)
            paths.append(relative.as_posix())
        write_spriteframes(out, resource_root+'/'+name+'.tres', {name: (paths, 20, False)})
        counts[name] = len(paths)
    (out/f'scripts/{prefix}_bolt.gd').write_text(BOLT_SCRIPT.replace('scenes/frost_impact.tscn', f'scenes/{prefix}_impact.tscn'))
    (out/f'scripts/{prefix}_impact.gd').write_text(IMPACT_SCRIPT)
    bolt_scene = '''[gd_scene load_steps=8 format=3]

[ext_resource type="Script" path="res://scripts/frost_bolt.gd" id="Script"]

'''+RADIAL_RESOURCES+'''
[sub_resource type="CircleShape2D" id="HitShape"]
radius = 3.0

[node name="FrostBolt" type="Area2D"]
script = ExtResource("Script")
collision_layer = 0
collision_mask = 1

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("HitShape")

[node name="Head" type="Sprite2D" parent="."]
material = SubResource("Additive")
texture = SubResource("Dot")

[node name="Trail" type="CPUParticles2D" parent="."]
material = SubResource("Additive")
texture = SubResource("Dot")
local_coords = false
amount = 70
lifetime = 0.35
direction = Vector2(0, -1)
spread = 8.0
gravity = Vector2(0, 0)
initial_velocity_min = 40.0
initial_velocity_max = 60.0
scale_amount_min = 0.1
scale_amount_max = 0.2
scale_amount_curve = SubResource("Shrink")
color_ramp = SubResource("CometColors")
'''
    if tint is not None:
        # Replace every travel-gradient RGB stop; retain the T3i alpha envelope.
        def recolor(match):
            values = [float(v) for v in match[1].split(',')]
            values = [v for i in range(0, len(values), 4) for v in (*tint, values[i+3])]
            return 'colors = PackedColorArray('+', '.join(format(v, '.12g') for v in values)+')'
        bolt_scene = re.sub(r'colors = PackedColorArray\(([^)]+)\)', recolor, bolt_scene)
    (out/f'scenes/{prefix}_bolt.tscn').write_text(bolt_scene.replace('scripts/frost_bolt.gd', f'scripts/{prefix}_bolt.gd'))
    impact_scene = '''[gd_scene load_steps=8 format=3]

[ext_resource type="Script" path="res://scripts/frost_impact.gd" id="Script"]
[ext_resource type="SpriteFrames" path="res://vfx/impact.tres" id="Frames"]

'''+RADIAL_RESOURCES+'''
[node name="FrostImpact" type="Node2D"]
script = ExtResource("Script")

[node name="Shatter" type="AnimatedSprite2D" parent="."]
sprite_frames = ExtResource("Frames")

[node name="Burst" type="CPUParticles2D" parent="."]
emitting = false
material = SubResource("Additive")
texture = SubResource("Dot")
local_coords = false
one_shot = true
explosiveness = 1.0
amount = 40
lifetime = 0.5
spread = 180.0
gravity = Vector2(0, 300)
initial_velocity_min = 120.0
initial_velocity_max = 260.0
scale_amount_curve = SubResource("Shrink")
color_ramp = SubResource("CometColors")
'''
    (out/f'scenes/{prefix}_impact.tscn').write_text(impact_scene.replace(
        'scripts/frost_impact.gd', f'scripts/{prefix}_impact.gd').replace('vfx/impact.tres', resource_root+'/impact.tres'))
    if 'effect' in kit:
        _write_authored_effect(out, kit, resource_root, prefix, counts)
    keeper = KEEPER_SCRIPT.replace('    base_frames = sprite.sprite_frames', '    _load_directional_kit()\n    base_frames = sprite.sprite_frames')
    keeper = keeper.replace('        state = "cast"\n', '        cast_fired = false\n        state = "cast"\n')
    keeper = keeper.replace('        _spawn_frost()', '        _cast_frame_changed()')
    if kit_name is None:
        (out/'scripts/keeper.gd').write_text(keeper+DIRECTIONAL_KEEPER)
    rectangle = None
    rectangle_report = None
    if annotation is not None:
        from export.scene_kit import largest_walkable_rectangle
        rectangle_report = {}
        rectangle = largest_walkable_rectangle(annotation, report=rectangle_report)
        x0, y0, x1, y1 = rectangle
        # An infinitesimal inset keeps uniform random boundary samples off walls.
        cx, cy = (x0+x1)/2, (y0+y1)/2
        ex, ey = max(0, (x1-x0)/2-1e-6), max(0, (y1-y0)/2-1e-6)
        (out/'scenes/ambient.tscn').write_text(f'''[gd_scene load_steps=5 format=3]

[sub_resource type="CanvasItemMaterial" id="Additive"]
blend_mode = 1

[sub_resource type="Gradient" id="Gold"]
colors = PackedColorArray(1, 0.75, 0.2, 0.5, 1, 0.6, 0.1, 0)

[sub_resource type="GradientTexture2D" id="Dot"]
gradient = SubResource("Gold")
width = 16
height = 16
fill = 1
fill_from = Vector2(0.5, 0.5)
fill_to = Vector2(1, 0.5)

[sub_resource type="Gradient" id="Fade"]
offsets = PackedFloat32Array(0, 0.3, 1)
colors = PackedColorArray(1, 0.8, 0.3, 0, 1, 0.8, 0.3, 0.5, 1, 0.8, 0.3, 0)

[node name="GoldMotes" type="CPUParticles2D"]
position = Vector2({cx:.12g}, {cy:.12g})
z_index = 2
material = SubResource("Additive")
texture = SubResource("Dot")
color_ramp = SubResource("Fade")
amount = 40
lifetime = 6.0
local_coords = false
emission_shape = 3
emission_rect_extents = Vector2({ex:.12g}, {ey:.12g})
direction = Vector2(0, -1)
spread = 30.0
gravity = Vector2(0, -4)
initial_velocity_min = 5.0
initial_velocity_max = 15.0
scale_amount_min = 0.08
scale_amount_max = 0.2
''')
        tower = out/'scenes/tower.tscn'
        text = tower.read_text()
        text = re.sub(r'load_steps=(\d+)', lambda m: 'load_steps='+str(int(m[1])+1), text, count=1)
        pos = text.index('[sub_resource ')
        text = text[:pos]+'[ext_resource type="PackedScene" path="res://scenes/ambient.tscn" id="Ambient"]\n\n'+text[pos:]
        text += '\n[node name="GoldMotes" parent="." instance=ExtResource("Ambient")]\n'
        tower.write_text(text)
    readme = (out/'README.md').read_text()
    readme += '\n\nDirectional VFX kit (--vfx-kit DIR [--sockets PATH])\n------------------------------------------------\n'
    readme += ('With this kit, casts fire once at the measured release_index (default 3),\n'
               'using the displayed frame socket through the sprite transform. Missing\n'
               'sockets suppress firing with a warning. Facing is screen space; diagonals\n'
               'are normalized. Bolts move at 520*scale px/s up to 650*scale px, with\n'
               'StaticBody2D collision and shatter/burst cleanup. impact_range in the\n'
               'selection JSON is an inclusive [first,last]; absent means all frames.\n'
               'Ambient emits inside the largest full-cell unblocked floor rectangle,\n'
               'on an 8 px grid, inset by one cell on every side. Spawn containment\n'
               'is guaranteed; subsequent particle drift is unconstrained.\n')
    readme += '\n## Credits\n\n'+kit['credits'].rstrip()+'\n'
    (out/'README.md').write_text(readme)
    references = validate_resources(out, include_scenes=True)
    return {'frames': counts, 'socket_cells': len(socket_data['cells']),
            'missing_sockets': sum(p is None for c in socket_data['cells'].values() for p in c['sockets']),
            'ambient_rectangle': rectangle, 'ambient_rectangle_report': rectangle_report,
            'resource_references': len(references)}


def _write_authored_effect(out, kit, resource_root, prefix, counts):
    """Author-kit-only scene path; the legacy templates above stay byte-stable."""
    from export.effect_kit import LAYER_SCRIPT, AUTHORED_BOLT, AUTHORED_IMPACT
    data = kit['effect']
    layers = data['layers']
    phase_durations = {}
    for phase, definition in data['phases'].items():
        name = 'flare' if phase == 'cast' else phase
        paths, durations = [], []
        for source, frame in zip(kit[name], definition['frames']):
            relative = Path(resource_root)/'sprites'/name/source.name
            (out/relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, out/relative)
            paths.append(relative.as_posix())
            durations.append(frame['hold_frames']/60)
        write_spriteframes(out, resource_root+'/'+name+'.tres',
                           {name: (paths, 1, phase == 'travel')}, {name: durations})
        counts[name] = len(paths)
        phase_durations[name] = sum(durations)
    exported_metadata = json.loads(json.dumps(data))
    for phase, definition in exported_metadata['phases'].items():
        name = 'flare' if phase == 'cast' else phase
        definition['sheet'] = 'sprites/'+name+'/'+Path(definition['sheet']).name
        for frame in definition['frames']:
            frame['file'] = 'sprites/'+name+'/'+Path(frame['file']).name
    (out/resource_root/'kit.json').write_text(json.dumps(exported_metadata, indent=2)+'\n')
    textures = {}
    for name, key in (('decal', 'file'), ('particles', 'texture')):
        if key in layers.get(name, {}):
            relative = Path(resource_root)/'layers'/Path(layers[name][key]).name
            (out/relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(kit['root']/layers[name][key], out/relative)
            textures[name] = relative.as_posix()
    def number(v): return format(float(v), '.12g')
    def vector(x, y): return 'Vector2('+number(x)+', '+number(y)+')'
    def color(rgb, alpha=1): return 'Color('+', '.join(number(v) for v in (*rgb, alpha))+')'
    floor = layers.get('floor_light', {})
    flash = layers.get('flash', {})
    decal = layers.get('decal', {})
    particles = layers.get('particles', {})
    stop = layers.get('hitstop', {})
    shake = layers.get('shake', {})
    constants = (
        'const FLOOR_DURATION = '+repr(float(floor.get('duration_s', 0)))+'\n'+
        'const FLASH_DURATION = '+repr(float(flash.get('duration_s', 0)))+'\n'+
        'const FLASH_TO = '+repr(float(flash.get('scale_to', 1)))+'\n'+
        'const DECAL_DURATION = '+repr(float(decal.get('duration_s', 0)))+'\n')
    tail = max(.001, particles.get('lifetime_s', 0), floor.get('duration_s', 0), flash.get('duration_s', 0), decal.get('duration_s', 0))
    total = max(phase_durations['impact']+phase_durations.get('residual', 0), tail)+.05
    with Image.open(kit['travel'][0]) as im: streak_offset = im.width/2
    for phase, template in (('travel', AUTHORED_BOLT), ('impact', AUTHORED_IMPACT)):
        kind = 'bolt' if phase == 'travel' else 'impact'
        script = template + constants + LAYER_SCRIPT
        if kind == 'bolt':
            script += 'const IMPACT_PATH = '+json.dumps('res://scenes/'+prefix+'_impact.tscn')+'\n'
            script += 'const TAIL_DURATION = '+repr(float(tail))+'\n'
            script += 'const STREAK_OFFSET = '+repr(float(streak_offset))+'\n'
        else:
            script += 'const BODY_DURATION = '+repr(phase_durations['impact'])+'\n'
            script += 'const TOTAL_DURATION = '+repr(total)+'\n'
        (out/f'scripts/{prefix}_{kind}.gd').write_text(script)
        ext = [f'[ext_resource type="Script" path="res://scripts/{prefix}_{kind}.gd" id="Script"]',
               f'[ext_resource type="SpriteFrames" path="res://{resource_root}/{phase}.tres" id="Frames"]']
        sub = []
        nodes = [f'[node name="Effect{kind.title()}" type="'+('Area2D' if kind == 'bolt' else 'Node2D')+'"]\n'
                 'texture_filter = 1\nscript = ExtResource("Script")\n'
                 f'ground_squash = {number(data["ground_squash"])}\n'
                 f'hitstop_duration = {number(stop.get("duration_s", 0))}\n'
                 f'hitstop_time_scale = {number(stop.get("time_scale", 1))}\n'
                 f'shake_distance = {number(shake.get("distance", 0))}\n'
                 f'shake_duration = {number(shake.get("duration_s", 0))}\n']
        if kind == 'bolt':
            nodes[0] += 'collision_layer = 0\ncollision_mask = 1\nspeed_px_s = '+number(data['phases']['travel'].get('speed_px_s', 520))+'\n'
            sub.append('[sub_resource type="CircleShape2D" id="HitShape"]\nradius = 3.0\n')
            nodes.append('[node name="CollisionShape2D" type="CollisionShape2D" parent="."]\nshape = SubResource("HitShape")\n')
        nodes.append('[node name="Ground" type="Node2D" parent="."]\n')
        def material(name, mode):
            declaration = f'[sub_resource type="CanvasItemMaterial" id="{name}"]\nblend_mode = {mode}\n'
            if declaration not in sub: sub.append(declaration)
            return f'material = SubResource("{name}")\n'
        def animated(name, extra='', resource='Frames', parent='Ground'):
            nodes.append(f'[node name="{name}" type="AnimatedSprite2D" parent="{parent}"]\n'
                         f'sprite_frames = ExtResource("{resource}")\n'+extra)
        if layers.get('dark_duplicate', False):
            animated('DarkDuplicate', 'z_index = -1\nmodulate = Color(0, 0, 0, 1)\n'+material('Mix', 0))
        animated('Travel' if kind == 'bolt' else 'Shatter', material('Mix', 0))
        if 'glow' in layers:
            glow = layers['glow']
            animated('Glow', material('Additive', 1)+'scale = '+vector(glow['scale'], glow['scale'])+'\nmodulate = '+color([1,1,1], glow['alpha'])+'\n')
        if kind == 'bolt' and data['phases']['travel'].get('streak', False):
            animated('Streak', 'z_index = -2\nscale = Vector2(1.5, 1)\nmodulate = Color(1, 1, 1, 0.35)\n'+material('Additive', 1))
        if flash:
            animated('Flash', material('Additive', 1)+'scale = '+vector(flash['scale_from'], flash['scale_from'])+'\nmodulate = '+color([1,1,1], flash['alpha'])+'\n')
        if floor:
            sub.append('[sub_resource type="Gradient" id="FloorColors"]\ncolors = PackedColorArray(1, 1, 1, 1, 1, 1, 1, 0)\n')
            sub.append('[sub_resource type="GradientTexture2D" id="FloorDisc"]\ngradient = SubResource("FloorColors")\nwidth = 32\nheight = 32\nfill = 1\nfill_from = Vector2(0.5, 0.5)\nfill_to = Vector2(1, 0.5)\n')
            radius = floor['radius_px']/16
            nodes.append('[node name="FloorLight" type="Sprite2D" parent="."]\nz_index = -3\ntexture = SubResource("FloorDisc")\n'+material('Additive', 1)+
                         'scale = '+vector(radius, radius*data['ground_squash'])+'\nmodulate = '+color(data['tint'])+'\n')
        if decal:
            if 'decal' in textures:
                ext.append(f'[ext_resource type="Texture2D" path="res://{textures["decal"]}" id="DecalTexture"]')
            else:
                relative = Path(resource_root)/'sprites'/phase/kit[phase][0].name
                ext.append(f'[ext_resource type="Texture2D" path="res://{relative.as_posix()}" id="DecalTexture"]')
            nodes.append('[node name="Decal" type="Sprite2D" parent="."]\nz_index = -4\ntexture = ExtResource("DecalTexture")\n'+material('Mix', 0)+'scale = '+vector(1, data['ground_squash'])+'\n')
        if particles:
            ext.append(f'[ext_resource type="Texture2D" path="res://{textures["particles"]}" id="ParticleTexture"]')
            velocity = particles['velocity_px_s']
            lo, hi = velocity if isinstance(velocity, list) else (velocity, velocity)
            nodes.append('[node name="Particles" type="CPUParticles2D" parent="."]\ntexture = ExtResource("ParticleTexture")\n'+material('Additive', 1)+
                         'modulate = '+color(data['tint'])+'\n'+
                         'local_coords = false\ngravity = Vector2(0, 0)\n'
                         f'one_shot = {str(kind == "impact").lower()}\nexplosiveness = {1 if kind == "impact" else 0}\n'
                         f'amount = {particles["amount"]}\nlifetime = {number(particles["lifetime_s"])}\n'
                         f'direction = {vector(*particles["direction"])}\nspread = {number(particles["spread_deg"])}\n'
                         f'initial_velocity_min = {number(lo)}\ninitial_velocity_max = {number(hi)}\n')
        if kind == 'impact' and 'residual' in data['phases']:
            ext.append(f'[ext_resource type="SpriteFrames" path="res://{resource_root}/residual.tres" id="ResidualFrames"]')
            animated('Residual', 'visible = false\nz_index = -2\n'+material('Mix', 0), 'ResidualFrames', '.')
        text = f'[gd_scene load_steps={1+len(ext)+len(sub)} format=3]\n\n'+'\n'.join(ext)+'\n\n'+'\n'.join(sub)+'\n'.join(nodes)
        (out/f'scenes/{prefix}_{kind}.tscn').write_text(text)


PICKER_SCRIPT = '''
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
'''


def _write_vfx_kits(out, kits, base, cells, socket_data, annotation):
    reports, entries = [], []
    for index, kit in enumerate(kits):
        name = kit['name']
        report = _write_vfx_kit(out, kit, base, cells, socket_data,
                                annotation if index == 0 else None,
                                kit_name=name, tint=kit.get('tint'))
        reports.append({'name': name, **report})
        entries.append({'name': name, 'flare': f'res://vfx/{name}/flare.tres',
                        'bolt': f'res://scenes/vfx_{name}_bolt.tscn'})
    keeper = KEEPER_SCRIPT.replace('    base_frames = sprite.sprite_frames',
                                   '    _load_directional_kit()\n    _load_vfx_picker()\n    base_frames = sprite.sprite_frames')
    keeper = keeper.replace('func _physics_process(delta: float) -> void:\n',
                            'func _physics_process(delta: float) -> void:\n'
                            '    if Input.is_action_just_pressed("vfx_cycle"):\n'
                            '        vfx_kit_index = (vfx_kit_index + 1) % VFX_KITS.size()\n'
                            '        _update_vfx_label()\n')
    keeper = keeper.replace('        state = "cast"\n',
                            '        cast_kit_index = vfx_kit_index\n        cast_fired = false\n        state = "cast"\n')
    keeper = keeper.replace('        _spawn_frost()', '        _cast_frame_changed()')
    directional = DIRECTIONAL_KEEPER.replace('preload("res://vfx/flare.tres")',
                                            'load(VFX_KITS[cast_kit_index]["flare"])')
    directional = directional.replace('preload("res://scenes/frost_bolt.tscn")',
                                      'load(VFX_KITS[cast_kit_index]["bolt"])')
    (out/'scripts/keeper.gd').write_text(keeper+directional+'\nconst VFX_KITS = '+
                                       json.dumps(entries, allow_nan=False)+'\n'+PICKER_SCRIPT)
    settings = out/'project.godot'
    settings.write_text(settings.read_text()+
                        'vfx_cycle={"deadzone":0.2,"events":[Object(InputEventKey,"physical_keycode":4194306)]}\n')
    credits = ''.join(kit['credits'] for kit in kits)
    (out/'CREDITS_VFX.txt').write_text(credits)
    readme = out/'README.md'
    readme.write_text(readme.read_text()+'\nTab cycles the ordered VFX kits; the HUD shows the selection.\n'
                      'Casts retain their starting kit through release, travel and impact.\n')
    return {'kits': reports, 'credits': credits,
            'resource_references': len(validate_resources(out, include_scenes=True))}


if __name__ == '__main__':
    main()
