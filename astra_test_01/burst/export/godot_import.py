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
        spriteframes = text.startswith('[gd_resource type="SpriteFrames"')
        shader_material = text.startswith('[gd_resource type="ShaderMaterial"')
        if not ((spriteframes and 'animations = [' in text) or
                (shader_material and 'shader = ExtResource(' in text)):
            raise ValueError('Not a SpriteFrames or ShaderMaterial resource: '+str(resource))
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


def build_project(cells, out, vfx=None, gear_variant=None, scene=None, vfx_kit=None, sockets=None, parallax=None, props=None, vfx_kits=None, vfx_grey=False, bake=False):
    started = time.monotonic()
    if not isinstance(vfx_grey, bool):
        raise ValueError('vfx_grey must be boolean')
    if not isinstance(bake, bool):
        raise ValueError('bake must be boolean')
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
    if vfx_grey:
        _grey_vfx(out)
    if bake:
        from export.replay import install_hooks
        install_hooks(out)
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
    parser.add_argument('--vfx-grey', action='store_true')
    parser.add_argument('--bake', action='store_true', help='Effect-only 512x512 transparent viewport and replay hooks')
    args = parser.parse_args()
    print(json.dumps(build_project(args.cells, args.out, args.vfx, args.gear_variant, args.scene, args.vfx_kit, args.sockets, args.parallax, args.props, args.vfx_kits, args.vfx_grey, args.bake), indent=2))




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
        if 'effect' in kit and 'tint' in entry:
            raise ValueError('tint multiply-tint override is retired for material kits')
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


def _authored_flare_script(script, resource_root, prefix, data):
    fields = {'res://'+resource_root+'/sprites/'+source: 'res://'+resource_root+'/'+field
              for source, field in data['distance_fields'].items() if source.startswith('flare/')}
    old = ('    var additive := CanvasItemMaterial.new()\n'
           '    additive.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD\n'
           '    flare.material = additive\n')
    new = ('    flare.material = load("res://'+resource_root+'/materials/Additive.tres")\n'
           '    flare.animation = &"flare"\n'
           '    preload("res://scripts/'+prefix+'_material.gd").bind(flare, '+json.dumps(fields)+')\n')
    script = script.replace(old, new)
    scale = data.get('phase_scale', {}).get('cast', 1)
    return script.replace('flare.scale = Vector2.ONE * art_scale',
                          'flare.scale = Vector2.ONE * art_scale * '+repr(float(scale)))


def _write_vfx_kit(out, kit, base, cells, socket_data, annotation, kit_name=None, tint=None, shared_projectile=False):
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
    if not shared_projectile:
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
    if not shared_projectile:
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
        _write_authored_effect(out, kit, resource_root, prefix, counts, shared_projectile=shared_projectile)
    keeper = KEEPER_SCRIPT.replace('    base_frames = sprite.sprite_frames', '    _load_directional_kit()\n    base_frames = sprite.sprite_frames')
    keeper = keeper.replace('        state = "cast"\n', '        cast_fired = false\n        state = "cast"\n')
    keeper = keeper.replace('        _spawn_frost()', '        _cast_frame_changed()')
    if kit_name is None:
        (out/'scripts/keeper.gd').write_text(keeper+(_authored_flare_script(DIRECTIONAL_KEEPER, resource_root, prefix, kit['effect']) if 'effect' in kit else DIRECTIONAL_KEEPER))
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


def _write_authored_effect(out, kit, resource_root, prefix, counts, shared_projectile=False):
    """Author-kit-only scene path; the legacy templates above stay byte-stable."""
    from export.effect_kit import (LAYER_SCRIPT, AUTHORED_BOLT, AUTHORED_IMPACT,
                                   MATERIAL_BINDING_SCRIPT, write_vfx_material, distance_field)
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
    textures = {}
    for name, key in (('decal', 'file'), ('particles', 'texture')):
        if key in layers.get(name, {}):
            relative = Path(resource_root)/'layers'/Path(layers[name][key]).name
            (out/relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(kit['root']/layers[name][key], out/relative)
            textures[name] = relative.as_posix()
            exported_metadata['layers'][name][key] = 'layers/'+Path(layers[name][key]).name
    fields = {}
    exported_metadata['distance_fields'] = {}
    for source, field in data['distance_fields'].items():
        relative_source = source if source.startswith(('layers/', 'pieces/')) else 'sprites/'+source
        destination = Path(resource_root)/field
        (out/destination).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(kit['root']/field, out/destination)
        fields['res://'+resource_root+'/'+relative_source] = 'res://'+destination.as_posix()
        exported_metadata['distance_fields'][relative_source] = field
    (out/resource_root/'kit.json').write_text(json.dumps(exported_metadata, indent=2)+'\n')
    floor_texture = None
    if 'floor_light' in layers:
        import numpy as np
        y, x = np.indices((32, 32))
        alpha = np.clip(1-np.hypot(x-15.5, y-15.5)/16, 0, 1)
        pixels = np.full((32, 32, 4), 255, dtype=np.uint8)
        pixels[..., 3] = np.rint(alpha*255).astype(np.uint8)
        floor_texture = resource_root+'/auxiliary/floor.png'
        floor_field = resource_root+'/auxiliary/floor_distance.png'
        (out/floor_texture).parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(pixels).save(out/floor_texture)
        Image.fromarray(distance_field(pixels)).save(out/floor_field)
        fields['res://'+floor_texture] = 'res://'+floor_field
    binding_path = f'scripts/{prefix}_material.gd'
    (out/binding_path).write_text('extends RefCounted\n'+MATERIAL_BINDING_SCRIPT)
    first_field = resource_root+'/'+next(iter(data['distance_fields'].values()))
    materials = {}
    for label, mode, dark in (('Body', data['material']['blend_mode'], False),
                              ('Mix', 'MIX', False), ('Additive', 'ADD', False), ('Dark', 'MIX', True)):
        resource = resource_root+'/materials/'+label+'.tres'
        write_vfx_material(out, resource, dict(data['material'], blend_mode=mode), first_field, dark)
        materials[label] = resource
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
        if shared_projectile and phase == 'travel':
            continue
        kind = 'bolt' if phase == 'travel' else 'impact'
        script = template + constants + LAYER_SCRIPT
        if shared_projectile and kind == 'impact':
            script = script.replace('    _feedback()\n', '    if get_meta("strike_response", true):\n        _feedback()\n')
            script = script.replace('    _start_layers("impact")',
                                    '    if not get_meta("strike_response", true) and has_node("Ground/Flash"):\n        $Ground/Flash.hide()\n    _start_layers("impact")')
        script = script.replace('func _ready() -> void:\n',
                                'func _ready() -> void:\n    _bind_vfx_materials()\n')
        script += ('\nconst VFX_FIELDS = '+json.dumps(fields)+'\n'
                   'func _bind_vfx_materials() -> void:\n'
                   '    preload("res://'+binding_path+'").bind_tree(self, VFX_FIELDS)\n')
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
                 'texture_filter = 2\nscript = ExtResource("Script")\n'
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
            declaration = f'[ext_resource type="Material" path="res://{materials[name]}" id="Material{name}"]'
            if declaration not in ext: ext.append(declaration)
            return f'material = ExtResource("Material{name}")\n'
        def animated(name, extra='', resource='Frames', parent='Ground'):
            phase_name = 'residual' if name == 'Residual' else phase
            scale = data.get('phase_scale', {}).get(phase_name, 1)
            # Layer-specific scales multiply the authored phase scale at runtime.
            if 'scale = Vector2(' in extra:
                extra = re.sub(r'scale = Vector2\(([^,]+), ([^)]+)\)',
                               lambda m: 'scale = '+vector(float(m[1])*scale, float(m[2])*scale), extra)
            else:
                extra += 'scale = '+vector(scale, scale)+'\n'
            nodes.append(f'[node name="{name}" type="AnimatedSprite2D" parent="{parent}"]\n'
                         'texture_filter = 2\n'
                         f'sprite_frames = ExtResource("{resource}")\n'
                         f'animation = &"{phase_name}"\n'+extra)
        if layers.get('dark_duplicate', False):
            animated('DarkDuplicate', 'z_index = -1\n'+material('Dark', 0))
        animated('Travel' if kind == 'bolt' else 'Shatter', material('Body', 0))
        if 'glow' in layers:
            glow = layers['glow']
            animated('Glow', material('Additive', 1)+'scale = '+vector(glow['scale'], glow['scale'])+'\nmodulate = '+color([1,1,1], glow['alpha'])+'\n')
        if kind == 'bolt' and data['phases']['travel'].get('streak', False):
            animated('Streak', 'z_index = -2\nscale = Vector2(1.5, 1)\nmodulate = Color(1, 1, 1, 0.35)\n'+material('Additive', 1))
        if flash:
            animated('Flash', material('Additive', 1)+'scale = '+vector(flash['scale_from'], flash['scale_from'])+'\nmodulate = '+color([1,1,1], flash['alpha'])+'\n')
        if floor:
            ext.append(f'[ext_resource type="Texture2D" path="res://{floor_texture}" id="FloorTexture"]')
            radius = floor['radius_px']/16
            nodes.append('[node name="FloorLight" type="Sprite2D" parent="."]\ntexture_filter = 2\nz_index = -3\ntexture = ExtResource("FloorTexture")\n'+material('Additive', 1)+
                         'scale = '+vector(radius, radius*data['ground_squash'])+'\nmodulate = Color(1, 1, 1, 1)\n')
        if decal:
            if 'decal' in textures:
                ext.append(f'[ext_resource type="Texture2D" path="res://{textures["decal"]}" id="DecalTexture"]')
            else:
                relative = Path(resource_root)/'sprites'/phase/kit[phase][0].name
                ext.append(f'[ext_resource type="Texture2D" path="res://{relative.as_posix()}" id="DecalTexture"]')
            nodes.append('[node name="Decal" type="Sprite2D" parent="."]\ntexture_filter = 2\nz_index = -4\ntexture = ExtResource("DecalTexture")\n'+material('Mix', 0)+'scale = '+vector(1, data['ground_squash'])+'\n')
        if particles:
            ext.append(f'[ext_resource type="Texture2D" path="res://{textures["particles"]}" id="ParticleTexture"]')
            velocity = particles['velocity_px_s']
            lo, hi = velocity if isinstance(velocity, list) else (velocity, velocity)
            nodes.append('[node name="Particles" type="CPUParticles2D" parent="."]\ntexture = ExtResource("ParticleTexture")\n'+material('Additive', 1)+
                         'texture_filter = 2\nmodulate = Color(1, 1, 1, 1)\n'+
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
    if 'pieces' in data:
        _write_piece_burst(out, kit, resource_root, prefix)


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
    _write_g1_component(out)
    for index, kit in enumerate(kits):
        name = kit['name']
        report = _write_vfx_kit(out, kit, base, cells, socket_data,
                                annotation if index == 0 else None,
                                kit_name=name, tint=kit.get('tint'), shared_projectile=True)
        reports.append({'name': name, **report})
        entries.append(_g1_config(kit))
        for old in (out/f'scripts/vfx_{name}_bolt.gd', out/f'scenes/vfx_{name}_bolt.tscn'):
            old.unlink(missing_ok=True)
        impact = out/f'scenes/vfx_{name}_impact.tscn'
        impact.write_text(impact.read_text().replace('script = ExtResource("Script")', 'texture_filter = 2\nscript = ExtResource("Script")', 1))
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
    if any('effect' in kit for kit in kits):
        old = ('    var additive := CanvasItemMaterial.new()\n'
               '    additive.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD\n'
               '    flare.material = additive\n')
        alternatives = []
        for index, kit in enumerate(kits):
            if 'effect' in kit:
                resource_root, prefix = 'vfx/'+kit['name'], 'vfx_'+kit['name']
                bound = _authored_flare_script(old, resource_root, prefix, kit['effect'])
                scale = kit['effect'].get('phase_scale', {}).get('cast', 1)
                bound += '    flare.set_meta("phase_scale", '+repr(float(scale))+')\n'
                alternatives.append(('if' if not alternatives else 'elif')+
                                    ' cast_kit_index == '+str(index)+':\n'+
                                    ''.join('    '+line+'\n' for line in bound.rstrip().splitlines()))
        alternatives.append('else:\n'+''.join('    '+line+'\n' for line in old.rstrip().splitlines()))
        directional = directional.replace(old, ''.join('    '+part if part.startswith(('if ', 'elif ', 'else:')) else part for part in alternatives))
        directional = directional.replace('flare.scale = Vector2.ONE * art_scale',
                                          'flare.scale = Vector2.ONE * art_scale * float(flare.get_meta("phase_scale", 1.0))')
    directional = _g1_directional(directional)
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



G1_SCENE = '''[gd_scene load_steps=3 format=3]
[ext_resource type="Script" path="res://scripts/vfx_g1.gd" id="G1"]
[sub_resource type="CircleShape2D" id="HeadShape"]
radius = 3.0
[node name="G1Projectile" type="Area2D"]
texture_filter = 2
script = ExtResource("G1")
collision_layer = 0
collision_mask = 2
monitoring = false
monitorable = false
[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("HeadShape")
[node name="Head" type="AnimatedSprite2D" parent="."]
texture_filter = 2
[node name="Trail" type="Line2D" parent="."]
texture_filter = 2
top_level = true
width = 3.0
default_color = Color(0.35, 0.65, 0.8, 0.6)
antialiased = true
'''

G1_SCRIPT = '''extends Area2D
# Physics clock, independent of hitstop/time_scale and accumulated delta rounding.
static var events: Array = []
static var next_id: int = 0
var effect_id: int = 0
var release_tick: int = 0
var active: bool = false
var expired: bool = true
var direction: Vector2 = Vector2.ZERO
var spell_scale: float = 1.0
var caster: Node2D
var config: Dictionary = {}
var resolved: Dictionary = {}
var distance: float = 0.0
var arrival_pending: bool = false
var remaining_pierce: int = 0
var contacted: Dictionary = {}
var strike_fired: bool = false
var cast_origin: Vector2 = Vector2.ZERO
var travel_end: Vector2 = Vector2.ZERO
static var label_events: Array = []

static func resolve_target(tree: SceneTree, origin: Vector2, facing: Vector2, cursor: Vector2, range_px: float = 650.0, cone_degrees: float = 30.0) -> Dictionary:
    if not origin.is_finite() or not cursor.is_finite() or not facing.is_finite() or facing.is_zero_approx() or not is_finite(range_px) or range_px <= 0.0 or not is_finite(cone_degrees) or cone_degrees < 0.0 or cone_degrees > 180.0:
        return {}
    var best: Area2D = null
    var best_distance: float = INF
    var axis: Vector2 = facing.normalized()
    for candidate in tree.get_nodes_in_group("vfx_targets"):
        if not candidate is Area2D or not candidate.is_inside_tree() or candidate.is_queued_for_deletion():
            continue
        var offset: Vector2 = candidate.global_position - origin
        var length: float = offset.length()
        if length <= range_px and (length <= 0.000001 or axis.dot(offset / length) >= cos(deg_to_rad(cone_degrees)) - 0.000001) and length < best_distance:
            best = candidate
            best_distance = length
    return {"point": best.global_position if best != null else cursor, "target": best, "kind": "prop" if best != null else "cursor"}

static func acquire(parent: Node2D, kit: Dictionary, origin: Vector2, destination: Dictionary, owner_node: Node2D = null, art_scale: float = 1.0) -> Area2D:
    # Invalid resolution never creates a node and never records a release.
    if not destination.has("point") or not destination.point is Vector2 or not destination.point.is_finite() or not origin.is_finite() or not is_finite(art_scale) or art_scale <= 0.0:
        return null
    if destination.get("kind", "") not in ["prop", "cursor"] or (destination.get("kind") == "prop" and not is_instance_valid(destination.get("target"))):
        return null
    if typeof(kit.get("pierce", 0)) != TYPE_INT or int(kit.get("pierce", 0)) < -1:
        return null
    if not kit.has("head") or not kit.has("impact") or not ResourceLoader.exists(kit.head) or not ResourceLoader.exists(kit.impact):
        return null
    var projectile: Area2D = null
    for candidate in parent.get_tree().get_nodes_in_group("vfx_g1_pool"):
        if candidate.get_parent() == parent and not candidate.active and not candidate.is_queued_for_deletion():
            projectile = candidate
            break
    if projectile == null:
        projectile = load("res://scenes/vfx/g1_projectile.tscn").instantiate()
        parent.add_child(projectile)
    projectile.release(kit, origin, destination, owner_node, art_scale)
    return projectile

func _ready() -> void:
    add_to_group("vfx_g1_pool")
    area_entered.connect(_on_area_entered)
    body_entered.connect(_on_body_entered)
    set_physics_process(false)
    hide()

func age_frames() -> int:
    return roundi(float(Engine.get_physics_frames() - release_tick) * 60.0 / Engine.physics_ticks_per_second)

func _record(event: String, collision_frame: int = -1) -> void:
    var point: Vector2 = resolved.point
    var entry: Dictionary = {"effect_id": effect_id, "event": event, "age_frames": age_frames(), "kit": config.name, "target_kind": resolved.kind, "target_point": [point.x, point.y]}
    if collision_frame >= 0:
        entry["collision_age_frames"] = collision_frame
        entry["contact_lag_frames"] = age_frames() - collision_frame
    events.append(entry)

func release(kit: Dictionary, origin: Vector2, destination: Dictionary, owner_node: Node2D = null, art_scale: float = 1.0) -> void:
    config = kit.duplicate(true)
    resolved = destination.duplicate()
    caster = owner_node
    spell_scale = art_scale
    global_position = origin
    direction = origin.direction_to(resolved.point)
    distance = 0.0
    remaining_pierce = int(config.get("pierce", 0))
    contacted.clear()
    strike_fired = false
    cast_origin = origin
    travel_end = resolved.point if remaining_pierce == 0 else origin + direction * float(config.get("range_px", 650.0)) * spell_scale
    arrival_pending = false
    active = true
    expired = false
    next_id += 1
    effect_id = next_id
    release_tick = Engine.get_physics_frames()
    for connection in $Head.frame_changed.get_connections():
        $Head.frame_changed.disconnect(connection.callable)
    for connection in $Head.animation_changed.get_connections():
        $Head.animation_changed.disconnect(connection.callable)
    $Head.sprite_frames = load(config.head)
    $Head.material = load(config.material) if config.get("material", "") != "" else null
    $Head.modulate = Color.WHITE
    var phase_scale: float = float(config.get("phase_scale", 1.0)) * spell_scale
    $Head.scale = Vector2(phase_scale, phase_scale * float(config.get("ground_squash", 1.0)))
    $Head.rotation = direction.angle()
    $Head.stop()
    $Head.frame = 0
    $Head.play(config.animation)
    $Head.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
    if config.get("binding", "") != "":
        load(config.binding).bind($Head, config.fields)
    $Trail.clear_points()
    $Trail.global_position = Vector2.ZERO
    $Trail.add_point(origin)
    var tint: Array = config.get("trail_color", [0.35, 0.65, 0.8, 0.6])
    $Trail.default_color = Color(tint[0], tint[1], tint[2], tint[3])
    $Trail.show()
    $CollisionShape2D.shape = $CollisionShape2D.shape.duplicate()
    $CollisionShape2D.shape.radius = 3.0 * spell_scale
    set_deferred("monitoring", true)
    show()
    set_physics_process(true)
    _record("release")

func _physics_process(delta: float) -> void:
    if not active:
        return
    if resolved.kind == "prop" and not is_instance_valid(resolved.target) and contacted.is_empty():
        cancel()
        return
    var remaining: float = global_position.distance_to(travel_end)
    var range_left: float = maxf(0.0, float(config.get("range_px", 650.0)) * spell_scale - distance)
    var step: float = minf(float(config.get("speed_px_s", 520.0)) * spell_scale * delta, minf(remaining, range_left))
    var motion: Vector2 = global_position.direction_to(travel_end) * step
    var start: Vector2 = global_position
    var hits: Array = []
    var space: PhysicsDirectSpaceState2D = get_world_2d().direct_space_state
    # Enumerate every collision body, including untagged legacy fixtures.
    # Exclude each hit and repeat from the same start; dispatch in distance order.
    var query := PhysicsShapeQueryParameters2D.new()
    query.shape = $CollisionShape2D.shape
    query.collision_mask = collision_mask
    query.collide_with_areas = true
    query.collide_with_bodies = true
    query.margin = 0.01
    var excluded: Array[RID] = [get_rid()]
    if caster is CollisionObject2D and is_instance_valid(caster):
        excluded.append(caster.get_rid())
    for id in contacted:
        var body = instance_from_id(id)
        if is_instance_valid(body) and body is CollisionObject2D:
            excluded.append(body.get_rid())
    while true:
        query.exclude = excluded
        query.transform = global_transform
        query.motion = Vector2.ZERO
        var overlaps: Array = space.intersect_shape(query)
        var fraction: float = 0.0
        if overlaps.is_empty():
            query.motion = motion
            var fractions: PackedFloat32Array = space.cast_motion(query)
            fraction = fractions[1] if fractions.size() == 2 else 1.0
            query.motion = Vector2.ZERO
            query.transform.origin = start + motion * fraction
            overlaps = space.intersect_shape(query)
        if overlaps.is_empty():
            break
        for hit in overlaps:
            var body: CollisionObject2D = hit.collider
            excluded.append(body.get_rid())
            hits.append({"area": body, "fraction": fraction, "along": (body.global_position - cast_origin).dot(direction)})
    hits.sort_custom(func(a, b): return a.fraction < b.fraction if not is_equal_approx(a.fraction, b.fraction) else a.along < b.along)
    for hit in hits:
        global_position = start + motion * float(hit.fraction)
        contact_body(hit.area)
        if not active:
            return
    global_position = start + motion
    distance += step
    $Trail.add_point(global_position)
    while $Trail.get_point_count() > 12:
        $Trail.remove_point(0)
    if remaining <= step + 0.001 or range_left <= step + 0.001:
        if contacted.is_empty() and resolved.kind == "cursor":
            _spawn_impact(false)
        if contacted.is_empty() and resolved.kind == "prop":
            cancel()
        else:
            expire()

func _on_area_entered(area: Area2D) -> void:
    # Swept queries own pierce ordering; overlap callbacks must not race them.
    if int(config.get("pierce", 0)) == 0:
        contact_body(area)

func _on_body_entered(body: Node2D) -> void:
    if int(config.get("pierce", 0)) == 0 and body is StaticBody2D:
        contact_body(body)

func contact_body(area: CollisionObject2D, phase: String = "head") -> void:
    # Phase producers (chain hops, shards, field centre/rim) share the cast ledger.
    if not active or not is_instance_valid(area) or area == caster or contacted.has(area.get_instance_id()):
        return
    if phase not in ["head", "chain_hop", "field_centre", "shard", "rim"]:
        return
    var contact_class: String = "primary"
    if phase in ["shard", "rim"] or (phase == "head" and not contacted.is_empty()):
        contact_class = "secondary"
    var body_index: int = int(area.get_meta("body_index", get_tree().get_nodes_in_group("vfx_targets").find(area) if area.is_in_group("vfx_targets") else area.get_instance_id()))
    contacted[area.get_instance_id()] = true
    _record("contact", age_frames())
    var entry: Dictionary = events[-1]
    entry["body_index"] = body_index
    entry["contact_class"] = contact_class
    entry["phase"] = phase
    entry["contact_distance_px"] = cast_origin.distance_to(area.global_position)
    entry["strike_response"] = not strike_fired
    if area.is_in_group("vfx_targets"):
        _contact_label(area, body_index, contact_class)
    _spawn_impact(not strike_fired, area.global_position if area.is_in_group("vfx_targets") else global_position)
    strike_fired = true
    if phase == "head":
        if remaining_pierce == 0:
            expire()
        elif remaining_pierce > 0:
            remaining_pierce -= 1

func _contact_label(area: CollisionObject2D, body_index: int, contact_class: String) -> void:
    var label: Label = null
    for candidate in get_tree().get_nodes_in_group("vfx_contact_labels"):
        if candidate.get_parent() == get_parent() and not candidate.visible:
            label = candidate
            break
    if label == null:
        label = Label.new()
        label.set_script(load("res://scripts/vfx_contact_label.gd"))
        get_parent().add_child(label)
    var colour: Array = config.get("palette_3", [0.35, 0.65, 0.8, 1.0])
    var anchor: Vector2 = area.global_position + Vector2(0, -70)
    var prop: Node = area.get_parent().get_node_or_null("Prop_" + String(area.name).trim_prefix("VfxTarget_"))
    if prop is Sprite2D:
        anchor = area.global_position + Vector2(0, prop.get_rect().position.y * prop.global_scale.y - 8.0)
    label.show_contact(anchor, "FULL" if contact_class == "primary" else "PARTIAL", Color(colour[0], colour[1], colour[2], colour[3]), effect_id, body_index, label_events)

func _spawn_impact(strike_response: bool = true, point: Variant = null) -> void:
    var impact: Node2D = load(config.impact).instantiate()
    impact.set_meta("strike_response", strike_response)
    impact.set("spell_scale", spell_scale)
    impact.set("caster", caster)
    impact.set("direction", direction)
    impact.position = get_parent().to_local(global_position if point == null else point)
    get_parent().add_child(impact)

func expire() -> void:
    if active:
        _record("expire")
        _recycle()

func cancel() -> void:
    if active:
        _record("cancel")
        _recycle()

func _recycle() -> void:
    active = false
    expired = true
    set_deferred("monitoring", false)
    set_physics_process(false)
    $Head.stop()
    $Trail.clear_points()
    $Trail.hide()
    hide()
'''


def _g1_config(kit):
    name = kit['name']
    root = 'vfx/'+name
    data = kit.get('effect', {})
    authored = bool(data)
    fields = {'res://'+root+'/sprites/'+source: 'res://'+root+'/'+field
              for source, field in data.get('distance_fields', {}).items() if source.startswith('travel/')}
    return {'name': name, 'flare': 'res://'+root+'/flare.tres',
            'bolt': 'res://scenes/vfx/g1_projectile.tscn',
            'head': 'res://'+root+('/travel.tres' if authored else '/flare.tres'),
            'animation': 'travel' if authored else 'flare',
            'impact': 'res://scenes/vfx_'+name+'_impact.tscn',
            'speed_px_s': data.get('phases', {}).get('travel', {}).get('speed_px_s', 520.0),
            'pierce': data.get('pierce', 0),
            'palette_3': data.get('material', {}).get('palette', [[.35, .65, .8, 1]]*4)[3],
            'range_px': 650.0, 'ground_squash': 1.0 if 'pieces' in data else data.get('ground_squash', 1.0),
            'phase_scale': data.get('phase_scale', {}).get('travel', 1.0),
            'material': 'res://'+root+'/materials/Body.tres' if authored else '',
            'binding': 'res://scripts/vfx_'+name+'_material.gd' if authored else '',
            'fields': fields, 'trail_color': list(kit.get('tint', [.35, .65, .8]))+[.6]}


def _g1_directional(script):
    script = script.replace('var socket_cells: Dictionary = {}',
                            'var socket_cells: Dictionary = {}\nvar cast_ready: bool = false\n'
                            'var vfx_cursor_override: Variant = null\n'
                            'const G1 = preload("res://scripts/vfx_g1.gd")')
    script = script.replace('    sprite.frame_changed.connect(_cast_frame_changed)',
                            '    sprite.frame_changed.connect(_cast_frame_changed)\n'
                            '    get_tree().physics_frame.connect(_g1_cast_ready, CONNECT_ONE_SHOT)')
    start = script.index('    var bolt: Area2D = ')
    end = script.index('\nfunc _process(', start)
    script = script[:start]+'''    var kit: Dictionary = VFX_KITS[cast_kit_index].duplicate(true)
    var cursor: Vector2 = get_global_mouse_position() if vfx_cursor_override == null else vfx_cursor_override
    var destination: Dictionary = G1.resolve_target(get_tree(), global_position, direction, cursor, float(kit.range_px) * art_scale)
    if not cast_ready:
        await get_tree().physics_frame
    if not is_inside_tree():
        return
    G1.acquire(get_parent(), kit, socket, destination, self, art_scale)

func _g1_cast_ready() -> void:
    cast_ready = true

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventScreenTouch and event.pressed:
        vfx_cursor_override = get_canvas_transform().affine_inverse() * event.position
    elif event is InputEventMouseMotion or event is InputEventMouseButton:
        vfx_cursor_override = null
''' + script[end:]
    return script.replace('    flare.sprite_frames = ', '    flare.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR\n    flare.sprite_frames = ')


def _write_g1_component(out):
    (out/'scenes/vfx').mkdir(parents=True, exist_ok=True)
    (out/'scenes/vfx/g1_projectile.tscn').write_text(G1_SCENE)
    (out/'scripts/vfx_g1.gd').write_text(G1_SCRIPT)
    (out/'scripts/vfx_contact_label.gd').write_text(CONTACT_LABEL_SCRIPT)
    (out/'probe_pierce.gd').write_text(PIERCE_PROBE)
    (out/'probe_vfx.gd').write_text(G1_PROBE)


def _grey_vfx(out):
    """Mid-grey body texels with byte-identical source alpha; disable recolouring."""
    for path in (out/'vfx').rglob('*.png'):
        if 'sprites' not in path.parts:
            continue
        with Image.open(path) as source:
            image = source.convert('RGBA')
            alpha = image.getchannel('A')
            grey = Image.new('RGBA', image.size, (128, 128, 128, 255))
            grey.putalpha(alpha)
            grey.save(path)
    # Body rendering bypasses the painted shader so palette/edge lighting cannot
    # recolour the diagnostic silhouette. Optional light layers stay unchanged.
    for path in (out/'scenes').rglob('*.tscn'):
        text = path.read_text()
        if any(path in text for path in ('res://scripts/vfx/piece_burst.gd', 'res://scripts/vfx/piece_burst_v2.gd')):
            # Keep index RGB for band-step dissolve: grey is a palette swap.
            text = text.replace('script = ExtResource("Script")\n',
                                'script = ExtResource("Script")\ngrey_bodies = true\n', 1)
        text = re.sub(r'(^\[node name="(?:Travel|Shatter|Residual|Head)"[^\n]*\n)(.*?)(?=\n\[|\Z)',
                      lambda m: m[1]+re.sub(r'^material = .*\n', '', m[2], flags=re.M), text, flags=re.M|re.S)
        # Removing a body material also removes its last ExtResource use.
        # Keep declarations only while referenced (shared glow/light materials
        # must survive), and maintain the scene's exact load_steps count.
        used = set(re.findall(r'ExtResource\("([^\"]+)"\)', text))
        text = re.sub(r'^\[ext_resource [^\n]+ id="([^\"]+)"\]\n',
                      lambda m: m[0] if m[1] in used else '', text, flags=re.M)
        steps = 1 + len(re.findall(r'^\[(?:ext_resource|sub_resource) ', text, re.M))
        text = re.sub(r'(?<=load_steps=)\d+', str(steps), text, count=1)
        path.write_text(text)
    keeper = out/'scripts/keeper.gd'
    text = keeper.read_text()
    text = re.sub(r'"material": "[^"]+"', '"material": ""', text)
    text = re.sub(r'"binding": "[^"]+"', '"binding": ""', text)
    text = re.sub(r'    flare.material = load\([^\n]+\n', '    flare.material = null\n', text)
    text = re.sub(r'^    +preload\([^\n]+\.bind\(flare,[^\n]+\n', '', text, flags=re.M)
    keeper.write_text(text)


G1_PROBE = '''extends SceneTree
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
'''


def evaluate_g1_events(events):
    """Report measured event invariants; malformed or absent evidence is unknown."""
    if not isinstance(events, list):
        raise ValueError('events must be a list')
    groups = {}
    for event in events:
        if not isinstance(event, dict) or not {'effect_id', 'event', 'age_frames'} <= event.keys():
            raise ValueError('event requires effect_id, event and age_frames')
        if event['event'] not in ('release', 'contact', 'expire', 'cancel'):
            raise ValueError('unknown G1 event')
        age = event['age_frames']
        if isinstance(age, bool) or not isinstance(age, int) or age < 0:
            raise ValueError('age_frames must be a nonnegative integer')
        groups.setdefault(event['effect_id'], []).append(event)
    contacts = [e for e in events if e['event'] == 'contact']
    lags = [e['age_frames']-e['collision_age_frames'] for e in contacts if isinstance(e.get('collision_age_frames'), int)]
    releases = [e for e in events if e['event'] == 'release']
    def resolved(e):
        p = e.get('target_point')
        return (e.get('target_kind') in ('prop', 'cursor') and isinstance(p, list) and len(p) == 2
                and all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in p))
    missing = sum(not resolved(e) for e in releases)
    first = groups.get(releases[0]['effect_id'], []) if releases else []
    first_contacts = sum(e['event'] == 'contact' for e in first)
    ordered = all([e['age_frames'] for e in es] == sorted(e['age_frames'] for e in es)
                  and es[0]['event'] == 'release' and es[0]['age_frames'] == 0
                  and sum(e['event'] == 'release' for e in es) == 1
                  and es[-1]['event'] in ('expire', 'cancel')
                  and sum(e['event'] in ('expire', 'cancel') for e in es) == 1
                  for es in groups.values())
    values = [('g1_contact_lag', max(lags) if lags else None, 1, '<=', 'frames',
               bool(lags) and len(lags) == len(contacts) and min(lags) >= 0),
              ('g1_first_cast', first_contacts if releases else None, 1, '==', 'contacts', bool(releases)),
              ('g1_unresolved_releases', missing if releases else None, 0, '==', 'effects', bool(releases)),
              ('g1_event_order', int(ordered) if groups else None, 1, '==', 'boolean', bool(groups))]
    return [{'id': name, 'subject': 'g1', 'passed': None if value is None else bool(valid and (value <= threshold if op == '<=' else value == threshold)),
             'value': value, 'threshold': threshold, 'op': op, 'unit': unit,
             'evidence': ['out/events.json'], 'notes': 'Measured probe evidence; no visual/style verdict.'}
            for name, value, threshold, op, unit, valid in values]




CONTACT_LABEL_SCRIPT = '''extends Label
const LIFETIME_S: float = 0.6
const RISE_PX: float = 40.0
var started_usec: int = 0
var start_point: Vector2
var evidence: Dictionary
func _ready() -> void:
    add_to_group("vfx_contact_labels")
    texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
    mouse_filter = Control.MOUSE_FILTER_IGNORE
    z_index = 100
    add_theme_font_size_override("font_size", 22)
    add_theme_color_override("font_outline_color", Color(0.04, 0.05, 0.08, 1))
    add_theme_constant_override("outline_size", 4)
    hide()
    set_process(false)
func show_contact(point: Vector2, words: String, colour: Color, cast_id: int, body_index: int, events: Array) -> void:
    text = words
    add_theme_color_override("font_color", colour)
    reset_size()
    start_point = point + Vector2(-size.x * 0.5, -size.y)
    global_position = start_point
    modulate.a = 1.0
    started_usec = Time.get_ticks_usec()
    evidence = {"effect_id": cast_id, "body_index": body_index, "text": words, "label_id": get_instance_id(), "lifetime_s": null, "rise_px": null}
    events.append(evidence)
    show()
    set_process(true)
func _process(_delta: float) -> void:
    var elapsed: float = float(Time.get_ticks_usec() - started_usec) / 1000000.0
    var progress: float = minf(elapsed / LIFETIME_S, 1.0)
    global_position = start_point + Vector2(0, -RISE_PX * progress)
    modulate.a = 1.0 - progress
    if progress >= 1.0:
        evidence["lifetime_s"] = elapsed
        evidence["rise_px"] = RISE_PX
        hide()
        set_process(false)
'''


PIERCE_PROBE = '''extends SceneTree
const G1 = preload("res://scripts/vfx_g1.gd")
var errors: Array = []
var measurements: Dictionary = {}
var scenarios: Dictionary = {}
func check(ok: bool, message: String) -> void:
    if not ok:
        errors.append(message)
        printerr("PIERCE_ASSERTION: ", message)
func _initialize() -> void:
    call_deferred("probe")
func dummy(parent: Node2D, point: Vector2, index: int) -> Area2D:
    var area := Area2D.new()
    area.position = point
    area.collision_layer = 2
    area.collision_mask = 0
    area.monitoring = false
    var shape := CollisionShape2D.new()
    var rectangle := RectangleShape2D.new()
    rectangle.size = Vector2(16, 12)
    shape.shape = rectangle
    area.add_child(shape)
    parent.add_child(area)
    area.add_to_group("vfx_targets")
    area.set_meta("body_index", index)
    return area
func probe() -> void:
    Engine.physics_ticks_per_second = 60
    G1.events.clear()
    G1.label_events.clear()
    var main: Node2D = load(ProjectSettings.get_setting("application/run/main_scene")).instantiate()
    root.add_child(main)
    var keeper: CharacterBody2D = main.find_child("Keeper", true, false)
    keeper.set_physics_process(false)
    keeper.sprite.pause()
    var parent: Node2D = keeper.get_parent()
    var origin: Vector2 = keeper.global_position + Vector2(0, -300)
    var targets: Array = get_nodes_in_group("vfx_targets")
    measurements["live_target_count"] = targets.size()
    for i in range(targets.size()):
        targets[i].global_position = origin + Vector2(500, 300 + i * 50)
    if targets.size() < 3:
        for i in range(3 - targets.size()):
            targets.append(dummy(parent, Vector2.ZERO, i))
    # Deliberately reverse group enumeration relative to physical distance.
    var ordered: Array = [targets[2], targets[1], targets[0]]
    for i in range(3):
        ordered[i].global_position = origin + Vector2((120 + i * 180) * keeper.sprite.global_transform.x.length(), 0)
        ordered[i].set_meta("body_index", i)
    await physics_frame
    await physics_frame
    var kit: Dictionary = keeper.VFX_KITS[0].duplicate(true)
    var chain: Dictionary = kit.duplicate(true)
    for candidate in keeper.VFX_KITS:
        if candidate.name == "frozen_orb": kit = candidate.duplicate(true)
        if "chain" in candidate.name: chain = candidate.duplicate(true)
    measurements["range_px"] = kit.range_px
    measurements["art_scale"] = keeper.sprite.global_transform.x.length()
    measurements["effective_range_px"] = float(kit.range_px) * keeper.sprite.global_transform.x.length()
    measurements["catalogue_pierce"] = keeper.VFX_KITS.map(func(k): return {"name": k.name, "pierce": k.pierce})
    kit.pierce = -1
    await cast_case("unlimited", parent, keeper, kit, origin, ordered, ["primary", "secondary", "secondary"])
    kit.pierce = 0
    await cast_case("zero", parent, keeper, kit, origin, ordered, ["primary"])
    kit.pierce = 1
    await cast_case("one", parent, keeper, kit, origin, ordered, ["primary", "secondary"])
    kit.pierce = -1
    kit.speed_px_s = 60000.0
    await cast_case("fast_sweep", parent, keeper, kit, origin, ordered, ["primary", "secondary", "secondary"])
    # Explicit phase callbacks exercise chain/field/shard classification; no new aim protocol.
    await phase_case("chain_hops", parent, keeper, chain, origin, ordered, ["chain_hop", "chain_hop", "chain_hop"], ["primary", "primary", "primary"])
    await phase_case("field_and_shard", parent, keeper, kit, origin, ordered, ["field_centre", "rim", "shard"], ["primary", "secondary", "secondary"])
    measurements["label_pool_size"] = get_nodes_in_group("vfx_contact_labels").size()
    check(measurements.label_pool_size == 3, "labels must reuse a pool of three")
    for label in G1.label_events:
        check(label.lifetime_s != null and float(label.lifetime_s) <= 0.8, "label lifetime <= 0.8 s")
        check(label.rise_px == 40.0, "label rises exactly 40 px")
    for label in get_nodes_in_group("vfx_contact_labels"):
        check(not label.visible, "labels all recycled")
        check(label.get_theme_font_size("font_size") == 22, "font size 22")
        check(label.get_theme_constant("outline_size") > 0, "dark outline")
    measurements["label_count"] = G1.label_events.size()
    var report: Dictionary = {"measurements": measurements, "scenarios": scenarios, "events": G1.events, "labels": G1.label_events, "errors": errors}
    DirAccess.make_dir_recursive_absolute("res://out")
    var file := FileAccess.open("res://out/probe_pierce.json", FileAccess.WRITE)
    file.store_string(JSON.stringify(report, "  "))
    file.close()
    print("PIERCE_RUNTIME=" + JSON.stringify({"measurements": measurements, "scenarios": scenarios, "errors": errors}))
    if errors.is_empty(): print("T3O_RUNTIME_ASSERTIONS=complete")
    quit(0 if errors.is_empty() else 7)
func cast_case(name: String, parent: Node2D, keeper: Node2D, kit: Dictionary, origin: Vector2, bodies: Array, expected: Array) -> void:
    var destination: Dictionary = G1.resolve_target(self, origin, Vector2.RIGHT, origin + Vector2(300, 0), float(kit.range_px) * keeper.sprite.global_transform.x.length())
    check(destination.target == bodies[0], "aim remains nearest in facing cone")
    var effect: Area2D = G1.acquire(parent, kit, origin, destination, keeper, keeper.sprite.global_transform.x.length())
    var id: int = effect.effect_id
    for i in range(300):
        if not effect.active: break
        await physics_frame
    check(not effect.active, name + " expires within 300 ticks")
    effect.cancel()
    await create_timer(0.65, true, false, true).timeout
    verify_case(name, id, expected)
func phase_case(name: String, parent: Node2D, keeper: Node2D, kit: Dictionary, origin: Vector2, bodies: Array, phases: Array, expected: Array) -> void:
    var effect: Area2D = G1.acquire(parent, kit, origin, {"kind": "prop", "point": bodies[0].global_position, "target": bodies[0]}, keeper, keeper.sprite.global_transform.x.length())
    effect.set_physics_process(false)
    var id: int = effect.effect_id
    for i in range(3):
        effect.contact_body(bodies[i], phases[i])
        effect.contact_body(bodies[i], phases[i]) # duplicate callbacks must do nothing
    var colour: Array = kit.palette_3
    for label in get_nodes_in_group("vfx_contact_labels"):
        if label.visible:
            check(label.get_theme_color("font_color") == Color(colour[0], colour[1], colour[2], colour[3]), name + " palette_3 colour")
    effect.expire()
    await create_timer(0.65, true, false, true).timeout
    verify_case(name, id, expected)
func verify_case(name: String, id: int, expected: Array) -> void:
    var contacts: Array = G1.events.filter(func(e): return e.event == "contact" and e.effect_id == id)
    var labels: Array = G1.label_events.filter(func(e): return e.effect_id == id)
    var classes: Array = contacts.map(func(e): return e.contact_class)
    var words: Array = labels.map(func(e): return e.text)
    var expected_words: Array = expected.map(func(c): return "FULL" if c == "primary" else "PARTIAL")
    var strikes: int = contacts.filter(func(e): return e.strike_response).size()
    check(classes == expected, name + " contact classes/count")
    check(words == expected_words, name + " FULL/PARTIAL labels/count")
    check(strikes == 1, name + " one strike response")
    var last_distance: float = -1.0
    var seen: Dictionary = {}
    for contact in contacts:
        check(float(contact.contact_distance_px) >= last_distance, name + " distance order")
        last_distance = float(contact.contact_distance_px)
        check(not seen.has(contact.body_index), name + " one contact per body")
        seen[contact.body_index] = true
    scenarios[name] = {"classes": classes, "labels": words, "strike_responses": strikes, "contacts": contacts.size()}
'''


def evaluate_pierce_events(events, labels):
    """Independent contact/label instrument; absent evidence stays unevaluable."""
    if not isinstance(events, list) or not isinstance(labels, list):
        raise ValueError('events and labels must be arrays')
    contacts = [e for e in events if isinstance(e, dict) and e.get('event') == 'contact']
    for e in contacts:
        if (not {'effect_id', 'body_index', 'contact_class', 'phase', 'contact_distance_px', 'strike_response'} <= e.keys()
                or e['contact_class'] not in ('primary', 'secondary')
                or not isinstance(e['strike_response'], bool)
                or isinstance(e['contact_distance_px'], bool)
                or not isinstance(e['contact_distance_px'], (int, float))
                or not math.isfinite(e['contact_distance_px']) or e['contact_distance_px'] < 0):
            raise ValueError('malformed contact evidence')
    for e in labels:
        if not isinstance(e, dict) or not {'effect_id', 'body_index', 'text', 'lifetime_s', 'rise_px'} <= e.keys():
            raise ValueError('malformed label evidence')
        for key in ('lifetime_s', 'rise_px'):
            if e[key] is not None and (isinstance(e[key], bool) or not isinstance(e[key], (int,float)) or not math.isfinite(e[key]) or e[key] < 0):
                raise ValueError('malformed label numeric evidence')
    grouped = {}
    for e in contacts: grouped.setdefault(e['effect_id'], []).append(e)
    inversions = sum(a['contact_distance_px'] > b['contact_distance_px']
                     for group in grouped.values() for a, b in zip(group, group[1:])
                     if a['phase'] == b['phase'] == 'head')
    strike_max = max((sum(e['strike_response'] for e in group) for group in grouped.values()), default=0)
    label_keys = [(e['effect_id'], e['body_index']) for e in labels]
    duplicate_labels = len(label_keys) - len(set(label_keys))
    lifetimes = [e['lifetime_s'] for e in labels]
    wrong = 0
    for group in grouped.values():
        for index, e in enumerate(group):
            expected = 'secondary' if e['phase'] in ('rim', 'shard') or (e['phase'] == 'head' and index > 0) else 'primary'
            wrong += e['contact_class'] != expected
            matches = [label for label in labels if (label['effect_id'], label['body_index']) == (e['effect_id'], e['body_index'])]
            wrong += len(matches) != 1 or (bool(matches) and matches[0]['text'] != ('FULL' if expected == 'primary' else 'PARTIAL'))
    def row(name, value, threshold, op, unit, known=True):
        ok = value <= threshold if op == '<=' else value == threshold
        return {'id': name, 'subject': 'pierce', 'passed': ok if contacts and known else None,
                'value': value if contacts and known else None, 'threshold': threshold, 'op': op,
                'unit': unit, 'evidence': [], 'notes': 'T4f measured contact/label evidence.'}
    return [row('pierce_distance_order', inversions, 0, '==', 'inversions'),
            row('pierce_strike_once', strike_max, 1, '<=', 'responses_per_cast'),
            row('pierce_labels_unique', duplicate_labels, 0, '==', 'duplicates'),
            row('pierce_label_lifetime', max((v for v in lifetimes if v is not None), default=0), .8, '<=', 'seconds', bool(lifetimes) and None not in lifetimes),
            row('pierce_contact_text', wrong, 0, '==', 'mismatches'),
            row('pierce_label_rise', sum(e['rise_px'] != 40 for e in labels), 0, '==', 'mismatches', bool(labels))]




# T4h: emitted only for a kit that explicitly carries the pieces phase.
PIECE_BURST_SCRIPT = '''extends Node2D
# All stage changes use the same 60 Hz effect-age convention as G1.age_frames.
# Impact is this component's release; no timer, tween, delta accumulator or TIME.
@export var configuration: String = ""
@export var grey_bodies: bool = false
var spell_scale: float = 1.0
var caster: Node2D
var direction: Vector2 = Vector2.RIGHT
var release_tick: int = 0
var config: Dictionary
var pieces: Array = []
var trace: Array = []
var last_age: int = -1
var trace_path: String = ""
var stage: String = "onset"

static func piece_motion(seed_value: int, piece_id: int) -> Dictionary:
    var digest: String = (str(seed_value) + ":" + str(piece_id)).sha256_text()
    return {"speed_factor": 0.6 + 0.8 * float(digest.substr(0, 8).hex_to_int()) / 4294967295.0,
        "rotation_deg": -30.0 + 60.0 * float(digest.substr(8, 8).hex_to_int()) / 4294967295.0,
        "scale_delta": -0.08 + 0.16 * float(digest.substr(16, 8).hex_to_int()) / 4294967295.0}

func age_frames() -> int:
    return roundi(float(Engine.get_physics_frames() - release_tick) * 60.0 / Engine.physics_ticks_per_second)

func _ready() -> void:
    config = JSON.parse_string(FileAccess.get_file_as_string(configuration))
    release_tick = Engine.get_physics_frames()
    $Art.scale = Vector2.ONE * float(config.phase_scale) * spell_scale
    for item in config.pieces:
        var node: Sprite2D = get_node("Art/Pieces/Piece_%03d" % int(item.id))
        var paint: ShaderMaterial = node.material.duplicate() as ShaderMaterial
        node.material = paint
        if grey_bodies:
            for band in range(4):
                paint.set_shader_parameter("palette_" + str(band), Color(128.0/255.0, 128.0/255.0, 128.0/255.0, 1))
        var motion: Dictionary = piece_motion(int(config.seed), int(item.id))
        var data: Dictionary = {"node": node, "record": item, "motion": motion, "dark": null}
        if bool(config.dark_duplicate):
            var dark: Sprite2D = node.duplicate() as Sprite2D
            dark.name = "Dark_" + str(item.id)
            dark.z_index = -1
            dark.material = paint.duplicate()
            dark.material.set_shader_parameter("dark_duplicate", true)
            $Art/DarkPieces.add_child(dark)
            data.dark = dark
        pieces.append(data)
    for name in ["Peak", "PeakDark"]:
        var node: Sprite2D = get_node("Art/" + name)
        node.material = node.material.duplicate()
        if grey_bodies and name == "Peak":
            for band in range(4):
                node.material.set_shader_parameter("palette_" + str(band), Color(128.0/255.0, 128.0/255.0, 128.0/255.0, 1))
    # Optional bake instrumentation writes beside the T4c report, never in game.
    if FileAccess.file_exists("res://replay_config.json"):
        var replay: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://replay_config.json"))
        trace_path = str(replay.report).get_base_dir().path_join("pieces_trace.json")
    tree_exiting.connect(_write_trace)
    set_effect_age(0)

func _physics_process(_delta: float) -> void:
    set_effect_age(age_frames())

func set_effect_age(age: int) -> void:
    # Public deterministic clock hook for a frame-step probe, as well as G1 play.
    if age == last_age:
        return
    last_age = age
    var flight_start: int = int(config.flash_frames) + int(config.hold_frames)
    var erosion_start: int = maxi(15, flight_start + 1)
    var residue_start: int = erosion_start + 21
    var residue_end: int = residue_start + int(config.residue_frames)
    stage = "onset" if age < int(config.flash_frames) else ("hold" if age < flight_start else ("expansion" if age < erosion_start else ("erosion" if age < residue_start else ("residue" if age < residue_end else "zero"))))
    $Art/Peak.visible = stage == "hold"
    $Art/PeakDark.visible = stage == "hold" and bool(config.dark_duplicate)
    $Art/Flash.visible = stage == "onset"
    var flash_t: float = float(age) / maxf(1.0, float(config.flash_frames))
    $Art/Flash.scale = Vector2.ONE * lerpf(float(config.flash_from), float(config.flash_to), flash_t)
    $Art/Flash.modulate.a = float(config.flash_alpha) * (1.0 - flash_t)
    $Art/Glow.visible = age < flight_start and bool(config.glow_enabled)
    $FloorLight.visible = age < int(config.floor_frames) and bool(config.floor_enabled)
    $FloorLight.modulate.a = maxf(0.0, 1.0 - float(age) / maxf(1.0, float(config.floor_frames)))
    var flight_ticks: int = clampi(age - flight_start, 0, erosion_start - flight_start)
    var flight_t: float = float(flight_ticks) / float(erosion_start - flight_start)
    var erosion_t: float = clampf(float(age - erosion_start) / float(residue_start - erosion_start), 0.0, 1.0)
    var count: int = 0
    var states: Array = []
    for data in pieces:
        var item: Dictionary = data.record
        var node: Sprite2D = data.node
        # Detached source islands below 48 pixels appear only inside Peak.
        var active: bool = int(item.area_px) >= 48 and age >= flight_start and age < residue_end
        node.visible = active
        var motion: Dictionary = data.motion
        var centre: Vector2 = Vector2(float(config.centre[0]), float(config.centre[1]))
        var pivot: Vector2 = Vector2(float(item.pivot[0]), float(item.pivot[1]))
        var radial: Vector2 = Vector2.RIGHT.rotated(deg_to_rad(float(item.radial_angle_deg)))
        node.position = pivot - centre + radial * float(config.base_speed_px_s) * float(motion.speed_factor) * float(flight_ticks) / 60.0
        node.rotation = deg_to_rad(float(motion.rotation_deg)) * flight_t
        # Integer native-pixel steps of the mask bbox's longest dimension.
        # Freeze scale BEFORE erosion. Residue is never reached by shrinking.
        var native_extent: int = int(item.native_extent)
        var native_step: int = roundi(float(item.final_step) * flight_t)
        var native_scale: float = 1.0 + float(native_step) / float(native_extent)
        node.scale = Vector2.ONE * native_scale
        var erode: float = float(item.residue_erode) * erosion_t
        var dissolve: float = 0.5 * erosion_t
        if age >= residue_end:
            erode = 1.0
            dissolve = 1.0
        node.material.set_shader_parameter("erode", erode)
        node.material.set_shader_parameter("dissolve", dissolve)
        if data.dark != null:
            var dark: Sprite2D = data.dark
            dark.visible = active
            dark.transform = node.transform
            dark.material.set_shader_parameter("erode", erode)
            dark.material.set_shader_parameter("dissolve", dissolve)
        if active:
            count += 1
        states.append({"id": item.id, "visible": active, "scale": native_scale, "native_step": native_step, "rotation_deg": rad_to_deg(node.rotation), "position": [node.position.x, node.position.y], "erode": erode, "dissolve": dissolve})
    trace.append({"age_frames": age, "stage": stage, "peak_visible": $Art/Peak.visible, "shard_count": count, "source_piece_count": pieces.size(), "pieces": states})
    if age >= residue_end:
        hide()
        _write_trace()
        queue_free()

func _write_trace() -> void:
    if trace_path != "":
        var file := FileAccess.open(trace_path, FileAccess.WRITE)
        if file != null:
            file.store_string(JSON.stringify({"seed": config.seed, "phase_scale": config.phase_scale, "frames": trace}, "  "))
'''


def _write_piece_burst(out, kit, resource_root, prefix):
    """Emit spatial shards using unmodified T4e index masks and T4a materials."""
    if kit['effect']['pieces']['template'] == 'burst_v2':
        return _write_piece_burst_v2(out, kit, resource_root, prefix)
    import numpy as np
    from export.effect_kit import load_pieces, piece_motion, write_vfx_material
    data = kit['effect']
    config, record, _ = load_pieces(data['pieces'], kit['root'], runtime=True)
    source_root = (kit['root']/config['source']).parent
    target_root = out/resource_root/'pieces'
    target_root.mkdir(parents=True, exist_ok=True)
    for file in [record['peak_index']] + [p['mask'] for p in record['pieces']]:
        destination = target_root/file
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_root/file, destination)
    shutil.copyfile(kit['root']/config['source'], target_root/'pieces.json')
    (out/'scenes/vfx').mkdir(parents=True, exist_ok=True)
    (out/'scripts/vfx').mkdir(parents=True, exist_ok=True)
    (out/'scripts/vfx/piece_burst.gd').write_text(PIECE_BURST_SCRIPT)
    layers = data['layers']
    flash, glow, floor = (layers.get(k, {}) for k in ('flash', 'glow', 'floor_light'))
    phase_scale = data.get('phase_scale', {}).get('impact', 1.0)
    runtime = {**config, 'centre': record['centre'], 'phase_scale': phase_scale,
               'residue_frames': math.ceil(config['residue_s']*60),
               'flash_frames': max(1, round(flash.get('duration_s', 1/60)*60)),
               'flash_from': flash.get('scale_from', 1), 'flash_to': flash.get('scale_to', 1),
               'flash_alpha': flash.get('alpha', 1), 'glow_enabled': bool(glow),
               'floor_enabled': bool(floor), 'floor_frames': round(floor.get('duration_s', 0)*60),
               'dark_duplicate': layers.get('dark_duplicate', False), 'pieces': []}
    ext = ['[ext_resource type="Script" path="res://scripts/vfx/piece_burst.gd" id="Script"]']
    nodes = ['[node name="PieceBurst" type="Node2D"]\ntexture_filter = 2\nscript = ExtResource("Script")\n'
             'configuration = "res://'+resource_root+'/pieces/burst_runtime.json"\n',
             '[node name="Art" type="Node2D" parent="."]\n',
             '[node name="DarkPieces" type="Node2D" parent="Art"]\n',
             '[node name="Pieces" type="Node2D" parent="Art"]\n']
    def vector(x, y): return f'Vector2({float(x):.12g}, {float(y):.12g})'
    def sprite(name, texture, field, pivot, position, parent='Art', dark=False, mode=None, extra=''):
        mat = resource_root+'/materials/Piece_'+name+'.tres'
        write_vfx_material(out, mat, dict(data['material'], blend_mode=mode or data['material']['blend_mode']), field, dark)
        ext.extend([f'[ext_resource type="Texture2D" path="res://{texture}" id="T{name}"]',
                    f'[ext_resource type="Material" path="res://{mat}" id="M{name}"]'])
        nodes.append(f'[node name="{name}" type="Sprite2D" parent="{parent}"]\n'
                     'texture_filter = 2\nvisible = false\ncentered = false\n'
                     f'texture = ExtResource("T{name}")\nmaterial = ExtResource("M{name}")\n'
                     'offset = '+vector(-pivot[0], -pivot[1])+'\nposition = '+vector(*position)+'\n'+extra)
    peak = resource_root+'/pieces/'+record['peak_index']
    peak_source = Path(config['source']).parent/record['peak_index']
    peak_field = resource_root+'/'+data['distance_fields'][peak_source.as_posix()]
    for name, dark, mode in [('Peak', False, None), ('PeakDark', True, 'MIX'), ('Flash', False, 'ADD'), ('Glow', False, 'ADD')]:
        extra = 'z_index = -1\n' if dark else ''
        if name == 'Glow':
            extra += 'scale = '+vector(glow.get('scale', 1), glow.get('scale', 1))+'\nmodulate = Color(1, 1, 1, '+str(glow.get('alpha', 0))+')\n'
        sprite(name, peak, peak_field, record['centre'], (0, 0), dark=dark, mode=mode, extra=extra)
    for piece in record['pieces']:
        source = (Path(config['source']).parent/piece['mask']).as_posix()
        field = data['distance_fields'][source]
        with Image.open(kit['root']/source) as image: pixels = np.asarray(image.convert('RGBA'))
        with Image.open(kit['root']/field) as image: distance = np.asarray(image)
        ys, xs = np.nonzero(pixels[..., 3])
        extent = int(max(xs.max()-xs.min()+1, ys.max()-ys.min()+1))
        motion = piece_motion(config['seed'], piece['id'])
        # floor bounds handle tiny masks too; inactive islands retain unit scale.
        limit = math.floor(.15*extent)
        step = max(-limit, min(limit, round(motion['scale_delta']*extent))) if piece['area_px'] >= 48 else 0
        final_scale = 1+step/extent
        eligible = (pixels[..., 3] > 0) & (pixels[..., 0] < 255)
        histogram = np.bincount(distance[eligible], minlength=256)
        remaining = np.cumsum(histogram[::-1])[::-1]*final_scale**2
        target = piece['area_px']*config['residue_fraction']
        threshold = int(np.argmin(abs(remaining-target)))
        item = {k: piece[k] for k in ('id', 'pivot', 'area_px', 'radial_angle_deg', 'dominant_band')}
        item.update(native_extent=extent, final_step=step, residue_erode=threshold/255,
                    predicted_residue_area_px=float(remaining[threshold]))
        runtime['pieces'].append(item)
        sprite('Piece_%03d' % piece['id'], resource_root+'/pieces/'+piece['mask'], resource_root+'/'+field,
               piece['pivot'], tuple(a-b for a, b in zip(piece['pivot'], record['centre'])), parent='Art/Pieces')
    if floor:
        radius = floor['radius_px']/16*phase_scale
        sprite('FloorLight', resource_root+'/auxiliary/floor.png', resource_root+'/auxiliary/floor_distance.png',
               (16, 16), (0, 0), parent='.', mode='ADD',
               extra='z_index = -3\nscale = '+vector(radius, radius*data['ground_squash'])+'\n')
    else:
        nodes.append('[node name="FloorLight" type="Sprite2D" parent="."]\nvisible = false\n')
    (target_root/'burst_runtime.json').write_text(json.dumps(runtime, indent=2)+'\n')
    text = f'[gd_scene load_steps={len(ext)+1} format=3]\n'+'\n'.join(ext)+'\n'+'\n'.join(nodes)
    # The per-kit impact path is the G1 config route. The first pieces kit also
    # supplies the stable T4h replay entry point; subsequent kits cannot clobber it.
    (out/f'scenes/{prefix}_impact.tscn').write_text(text)
    canonical = out/'scenes/vfx/piece_burst.tscn'
    if not canonical.exists(): canonical.write_text(text)


# V2 is emitted separately: the v1 script and v1 scene bytes remain unchanged.
PIECE_BURST_V2_SCRIPT = '''extends "res://scripts/vfx/piece_burst.gd"
# R(theta) * S(along, across) * R(-theta), about the original mask root.
# Stationary source coverage anchors the core and tongue roots. Both layers
# use whole-body UV distance, never a distance field re-centred on a shard.
func _ready() -> void:
    config = JSON.parse_string(FileAccess.get_file_as_string(configuration))
    release_tick = Engine.get_physics_frames()
    $Art.scale = Vector2.ONE * float(config.phase_scale) * spell_scale
    for item in config.pieces:
        var name: String = "Axis_%03d" % int(item.id)
        var axis: Node2D = get_node("Art/Pieces/" + name)
        var stretch: Sprite2D = axis.get_node("Stretch")
        var paint: Sprite2D = stretch.get_node("Piece_%03d" % int(item.id))
        var root_sprite: Sprite2D = get_node("Art/Roots/Root_%03d" % int(item.id))
        for sprite in [paint, root_sprite]:
            sprite.material = sprite.material.duplicate()
            if grey_bodies:
                for band in range(4):
                    sprite.material.set_shader_parameter("palette_" + str(band), Color(128.0/255.0,128.0/255.0,128.0/255.0,1))
        var dark_axis: Node2D = null
        var dark_root: Sprite2D = null
        if bool(config.dark_duplicate):
            dark_axis = axis.duplicate()
            $Art/DarkPieces.add_child(dark_axis)
            var dark_paint: Sprite2D = dark_axis.get_node("Stretch/Piece_%03d" % int(item.id))
            dark_paint.material = paint.material.duplicate()
            dark_paint.material.set_shader_parameter("dark_duplicate", true)
            dark_root = root_sprite.duplicate()
            dark_root.material = root_sprite.material.duplicate()
            dark_root.material.set_shader_parameter("dark_duplicate", true)
            $Art/DarkRoots.add_child(dark_root)
        pieces.append({"record":item,"axis":axis,"node":stretch,"paint":paint,"root":root_sprite,"dark_axis":dark_axis,"dark_root":dark_root})
    for name in ["Peak", "PeakDark"]:
        var node: Sprite2D = get_node("Art/" + name)
        node.material = node.material.duplicate()
        if grey_bodies and name == "Peak":
            for band in range(4):
                node.material.set_shader_parameter("palette_" + str(band), Color(128.0/255.0,128.0/255.0,128.0/255.0,1))
    if FileAccess.file_exists("res://replay_config.json"):
        var replay: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://replay_config.json"))
        trace_path = str(replay.report).get_base_dir().path_join("pieces_trace.json")
    tree_exiting.connect(_write_trace)
    set_effect_age(0)

func set_effect_age(age: int) -> void:
    if age == last_age:
        return
    last_age = age
    var flight_start: int = int(config.flash_frames) + int(config.hold_frames)
    var expansion_end: int = flight_start + 15
    var residue_start: int = expansion_end + 21
    var residue_end: int = residue_start + int(config.residue_frames)
    stage = "onset" if age < int(config.flash_frames) else ("hold" if age < flight_start else ("expansion" if age <= expansion_end else ("erosion" if age < residue_start else ("residue" if age < residue_end else "zero"))))
    $Art/Peak.visible = stage == "hold"
    $Art/PeakDark.visible = stage == "hold" and bool(config.dark_duplicate)
    $Art/Flash.visible = stage == "onset"
    var flash_t: float = float(age) / maxf(1.0, float(config.flash_frames))
    $Art/Flash.scale = Vector2.ONE * lerpf(float(config.flash_from), float(config.flash_to), flash_t)
    $Art/Flash.modulate.a = float(config.flash_alpha) * (1.0-flash_t)
    $Art/Glow.visible = age < flight_start and bool(config.glow_enabled)
    $FloorLight.visible = age < int(config.floor_frames) and bool(config.floor_enabled)
    $FloorLight.modulate.a = maxf(0.0,1.0-float(age)/maxf(1.0,float(config.floor_frames)))
    var flight_t: float = clampf(float(age-flight_start)/15.0,0.0,1.0)
    var ease: float = 1.0-pow(1.0-flight_t,3.0)
    var erosion_t: float = clampf(float(age-expansion_end)/21.0,0.0,1.0)
    var states: Array = []
    var count: int = 0
    for data in pieces:
        var item: Dictionary = data.record
        var axis: Node2D = data.axis
        var node: Sprite2D = data.node
        var paint: Sprite2D = data.paint
        var root_sprite: Sprite2D = data.root
        var active: bool = int(item.area_px) >= 48 and age >= flight_start and age < residue_end
        # Position is NEVER animated. Rotation is around the pinned root.
        axis.rotation = float(item.axis_radians) + deg_to_rad(float(item.rotation_deg)) * ease
        if bool(item.core):
            var core_t: float = clampf(float(age-flight_start)/9.0,0.0,1.0)
            node.scale = Vector2.ONE * lerpf(1.0,1.25,1.0-pow(1.0-core_t,3.0))
        else:
            node.scale = Vector2(lerpf(1.0,float(item.along),ease),lerpf(1.0,0.7,ease))
        # Per-piece threshold curve: core erosion starts after its 9-tick swell;
        # tongues start at 15 ticks. Thresholds share the WHOLE-BODY field.
        var start: int = int(item.erosion_start_tick) + flight_start
        var erode_t: float = clampf(float(age-start)/float(residue_start-start),0.0,1.0)
        var erode: float = lerpf(0.0,1.0,erode_t)
        var dissolve: float = 0.5 * erosion_t
        axis.visible = active and age < residue_start
        paint.visible = true
        paint.material.set_shader_parameter("erode",erode)
        paint.material.set_shader_parameter("dissolve",dissolve)
        # Residue-by-erosion: a stationary radial interval of original masks.
        # No shrinking, relocating, replacing or resegmenting the source art.
        var root_erode: float = float(config.residue_erode) * erosion_t
        var outer: float = lerpf(1.0,float(config.residue_outer),erosion_t)
        root_sprite.visible = active
        root_sprite.material.set_shader_parameter("erode",root_erode)
        root_sprite.material.set_shader_parameter("outer_distance",outer)
        root_sprite.material.set_shader_parameter("dissolve",dissolve)
        if data.dark_axis != null:
            var dark: Node2D = data.dark_axis
            dark.transform = axis.transform
            dark.visible = axis.visible
            dark.get_node("Stretch").scale = node.scale
            var dark_paint: Sprite2D = dark.get_node("Stretch/Piece_%03d" % int(item.id))
            dark_paint.visible = true
            dark_paint.material.set_shader_parameter("erode",erode)
            dark_paint.material.set_shader_parameter("dissolve",dissolve)
            var dark_root: Sprite2D = data.dark_root
            dark_root.visible = active
            dark_root.material.set_shader_parameter("erode",root_erode)
            dark_root.material.set_shader_parameter("outer_distance",outer)
            dark_root.material.set_shader_parameter("dissolve",dissolve)
        if active:
            count += 1
        states.append({"id":item.id,"visible":active,"core":item.core,"scale":[node.scale.x,node.scale.y],"root_position":[axis.position.x,axis.position.y],"root_displacement_px":0.0,"rotation_deg":float(item.rotation_deg)*ease,"erode":erode,"dissolve":dissolve,"residue_erode":root_erode,"residue_outer":outer})
    trace.append({"age_frames":age,"stage":stage,"peak_visible":$Art/Peak.visible,"shard_count":count,"source_piece_count":pieces.size(),"pieces":states})
    if age >= residue_end:
        hide()
        _write_trace()
        queue_free()
'''


def _write_piece_burst_v2(out, kit, resource_root, prefix):
    """Rooted anisotropic sprites plus stationary eroded core/root coverage.

    The stationary layer uses the same original masks and whole-body field.
    An upper-distance clip bounds its retained roots; erode still removes the
    centre first. No shader or scene used by a legacy kit is changed.
    """
    import copy
    import numpy as np
    from export.effect_kit import (load_pieces, piece_geometry, piece_stretch,
                                   distance_field, write_vfx_material)
    data = kit['effect']
    config, record, _ = load_pieces(data['pieces'], kit['root'], runtime=True)
    # Reuse v1's unchanged layer/material plumbing, then replace only this scene.
    legacy = dict(kit, effect=copy.deepcopy(data))
    legacy['effect']['pieces']['template'] = 'burst_v1'
    canonical = out/'scenes/vfx/piece_burst.tscn'
    owns_canonical = not canonical.exists()
    _write_piece_burst(out, legacy, resource_root, prefix)
    target = out/f'scenes/{prefix}_impact.tscn'
    scene = target.read_text()
    source_root = kit['root']/Path(config['source']).parent
    geometry = piece_geometry(record, source_root)
    runtime_path = out/resource_root/'pieces/burst_runtime.json'
    runtime = json.loads(runtime_path.read_text())
    runtime.update(template='burst_v2', core_centre=geometry['core_centre'],
                   core_radius_px=geometry['core_radius_px'], pieces=[])
    with Image.open(source_root/record['peak_index']) as image:
        peak = np.asarray(image.convert('RGBA'))
    field = distance_field(peak)
    field_rel = resource_root+'/pieces/whole_body_distance.png'
    Image.fromarray(field).save(out/field_rel)
    # VO1 support, not alpha-weighted area; band 3 has already dissolved.
    eligible = np.zeros(peak.shape[:2], dtype=bool)
    for item in geometry['pieces']:
        if item['animated']:
            with Image.open(source_root/item['mask']) as image:
                eligible |= np.asarray(image.convert('RGBA'))[...,3] > 0
    eligible &= peak[...,0] < 255
    lower = .04
    histogram = np.bincount(field[eligible & (field/255 >= lower)], minlength=256)
    cumulative = np.cumsum(histogram)
    target_area = config['residue_fraction'] * np.count_nonzero(peak[...,3])
    cutoff = int(np.argmin(abs(cumulative-target_area)))
    runtime.update(residue_erode=lower, residue_outer=cutoff/255,
                   predicted_stationary_residue_area_px=int(cumulative[cutoff]),
                   source_peak_area_px=int(np.count_nonzero(peak[...,3])))
    scene = scene.replace('res://scripts/vfx/piece_burst.gd','res://scripts/vfx/piece_burst_v2.gd')
    # Root-only upper clip is a v2 shader variant. The shared T4a shader is frozen.
    extra_nodes = ['[node name="Roots" type="Node2D" parent="Art"]\n',
                   '[node name="DarkRoots" type="Node2D" parent="Art"]\nz_index = -1\n']
    def vector(x,y): return f'Vector2({float(x):.12g}, {float(y):.12g})'
    for item in geometry['pieces']:
        ident = item['id']; name = 'Piece_%03d' % ident
        material_rel = resource_root+'/materials/Piece_'+name+'.tres'
        write_vfx_material(out, material_rel, data['material'], field_rel)
        material = (out/material_rel).read_text()
        shader_ref = re.search(r'path="res://([^"]+\.gdshader)"', material)[1]
        root_shader = str(Path(shader_ref).with_name('vfx_material_v2_roots.gdshader'))
        source = (out/shader_ref).read_text()
        source = source.replace('uniform bool dark_duplicate', 'uniform float outer_distance = 1.0;\nuniform bool dark_duplicate')
        source = source.replace('float distance_value = texture(distance_texture, UV).r;',
                                'float distance_value = texture(distance_texture, UV).r;\n    if (distance_value > outer_distance) { coverage = 0.0; }')
        (out/root_shader).write_text(source)
        root_mat = resource_root+'/materials/Root_%03d.tres' % ident
        (out/root_mat).write_text(material.replace(shader_ref, root_shader))
        ext = f'[ext_resource type="Material" path="res://{root_mat}" id="RootM{ident}"]\n'
        # All external resources precede the first node.
        first_node = scene.index('[node ')
        scene = scene[:first_node] + ext + scene[first_node:]
        pattern = r'\[node name="'+name+r'" type="Sprite2D" parent="Art/Pieces"\]\n.*?(?=\[node |\Z)'
        axis_name = 'Axis_%03d' % ident
        position = tuple(a-b for a,b in zip(item['root'],record['centre']))
        angle = item['axis_radians']
        replacement = (f'[node name="{axis_name}" type="Node2D" parent="Art/Pieces"]\n'
                       f'position = {vector(*position)}\nrotation = {angle:.12g}\n'
                       f'[node name="Stretch" type="Sprite2D" parent="Art/Pieces/{axis_name}"]\n'
                       f'[node name="{name}" type="Sprite2D" parent="Art/Pieces/{axis_name}/Stretch"]\n'
                       'texture_filter = 2\ncentered = false\n'
                       f'rotation = {-angle:.12g}\noffset = {vector(-item["root"][0],-item["root"][1])}\n'
                       f'texture = ExtResource("T{name}")\nmaterial = ExtResource("M{name}")\n')
        scene, matches = re.subn(pattern,lambda _:replacement,scene,flags=re.S)
        if matches != 1: raise ValueError('Missing v2 piece node')
        extra_nodes.append(f'[node name="Root_{ident:03d}" type="Sprite2D" parent="Art/Roots"]\n'
                           'texture_filter = 2\ncentered = false\nvisible = false\n'
                           f'offset = {vector(-record["centre"][0],-record["centre"][1])}\n'
                           f'texture = ExtResource("T{name}")\nmaterial = ExtResource("RootM{ident}")\n')
        runtime['pieces'].append({**item, **piece_stretch(config['seed'],ident),
                                  'erosion_start_tick':9 if item['core'] else 15})
    scene += '\n'.join(extra_nodes)
    scene = re.sub(r'load_steps=\d+', 'load_steps='+str(scene.count('[ext_resource ')+1),scene,count=1)
    (out/'scripts/vfx/piece_burst_v2.gd').write_text(PIECE_BURST_V2_SCRIPT)
    runtime_path.write_text(json.dumps(runtime,indent=2)+'\n')
    target.write_text(scene)
    if owns_canonical: canonical.write_text(scene)
    (out/'scenes/vfx/piece_burst_v2.tscn').write_text(scene)


if __name__ == '__main__':
    main()
