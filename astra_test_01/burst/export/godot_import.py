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
    if kit is not None and 'g4' in kit.get('effect', {}):
        raise ValueError('G4 aura loop requires --vfx-kits for explicit component dispatch')
    if kit is not None and 'g3' in kit.get('effect', {}):
        raise ValueError('G3 bolt chain requires --vfx-kits for explicit component dispatch')
    if kit is not None and 'g2' in kit.get('effect', {}):
        raise ValueError('G2 thrown field requires --vfx-kits with explicit splash dependencies')
    if kit is not None and 'travel_primitives' in kit.get('effect', {}):
        raise ValueError('painted G1 travel requires --vfx-kits with its impact dependency')
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
Eight directions select authored rotated-character cells, never mirror their pixels.
Sockets use that displayed cell row and its full sprite transform, never an E-row rotation.
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
    kits_report = _write_vfx_kits(out, kits, base, cells, socket_data, annotation, parallax_data["walkable"] if parallax_data else annotation) if kits is not None else None
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
            or not isinstance(data['kits'], list) or not 1 <= len(data['kits']) <= 32):
        raise ValueError('VFX kits requires exactly kits: a list of 1..32 entries')
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
    # Preserve the legacy twelve-entry limit; explicit grammar components extend it.
    if len(result) > 12 and sum(not any(g in kit.get('effect', {}) for g in ('g2','g3','g4','orb')) for kit in result) > 12:
        raise ValueError('VFX kits beyond twelve require explicit grammar components')
    by_name = {kit['name']: kit for kit in result}
    for kit in result:
        data = kit.get('effect', {})
        if 'g2' in data:
            if data['element'] == 'fire':
                splash = data['g2']['splash']
                dependency = by_name.get(splash['kit'], {}).get('effect', {})
                # The splash owns its palette; the painted field has an independent ramp.
                if (dependency.get('pieces', {}).get('template') != splash['template']
                        or dependency.get('element') != data['element'] or not dependency.get('screen_px')):
                    raise ValueError('G2 fire splash dependency missing or disagrees with treatment/template/screen_px')
            continue
        if 'travel_primitives' not in data: continue
        binding = data['impact_binding']
        impact = by_name.get(binding['kit'], {}).get('effect', {})
        if (impact.get('pieces', {}).get('template') != binding['template']
                or impact.get('pieces', {}).get('seed') != binding['seed']
                or impact.get('material', {}).get('palette') != data['material']['palette']
                or {k:v for k,v in impact.get('layers', {}).items() if k not in ('cast','travel')} != {k:v for k,v in data['layers'].items() if k not in ('cast','travel')} or not impact.get('screen_px')):
            raise ValueError('projectile impact dependency missing or disagrees with binding/palette/layers')
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
              for source, field in data.get('distance_fields', {}).items() if source.startswith('flare/')}
    old = ('    var additive := CanvasItemMaterial.new()\n'
           '    additive.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD\n'
           '    flare.material = additive\n')
    new = ('    flare.material = load("res://'+resource_root+'/materials/Additive.tres")\n'
           '    flare.animation = &"flare"\n'
           '    preload("res://scripts/'+prefix+'_material.gd").bind(flare, '+json.dumps(fields)+')\n')
    script = script.replace(old, new)
    scale = data.get('phase_scale', {}).get('cast', 1)
    multiplier = '1.0' if data.get('screen_px', False) else 'art_scale'
    return script.replace('flare.scale = Vector2.ONE * art_scale',
                          'flare.scale = Vector2.ONE * '+multiplier+' * '+repr(float(scale)))


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
    if 'contact_light' in layers:
        (out/'scripts/vfx_contact_light.gd').write_text(CONTACT_LIGHT_SCRIPT)
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
    if 'orb' in data:
        _write_orb(out, kit, resource_root)
    if 'travel_primitives' in data:
        _write_painted_travel(out, kit, resource_root)
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
        relative_source = source if source.startswith(('layers/', 'pieces/', 'primitives/', 'travel_keys/')) else 'sprites/'+source
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
        phase_material = dict(data['material'], blend_mode=mode)
        if data.get('pieces', {}).get('template') == 'burst_v2':
            # V2 resistance is bound only on its whole-body piece materials.
            phase_material.pop('erode_noise', None)
        write_vfx_material(out, resource, phase_material, first_field, dark)
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
        if data.get('screen_px', False):
            script = script.replace('func _ready() -> void:\n', 'func _ready() -> void:\n    spell_scale = 1.0\n')
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


def _write_vfx_kits(out, kits, base, cells, socket_data, annotation, ground_geometry=None):
    reports, entries = [], []
    _write_g1_component(out)
    if any(kit.get('effect', {}).get('screen_px', False) for kit in kits):
        g1_path = out/'scripts/vfx_g1.gd'
        g1_path.write_text(g1_path.read_text().replace('spell_scale = art_scale',
            'spell_scale = 1.0 if bool(config.get("screen_px", false)) else art_scale'))
    if any('travel_primitives' in kit.get('effect', {}) or 'orb' in kit.get('effect', {}) for kit in kits):
        _write_painted_g1(out)
    has_g2 = any('g2' in kit.get('effect', {}) for kit in kits)
    if has_g2: _write_g2_component(out)
    has_g3 = any('g3' in kit.get('effect', {}) for kit in kits)
    if has_g3: _write_g3_component(out)
    has_g4 = any('g4' in kit.get('effect', {}) for kit in kits)
    if has_g4: _write_g4_component(out)
    for index, kit in enumerate(kits):
        name = kit['name']
        if 'g4' in kit.get('effect', {}):
            report = _write_g4_kit(out, kit)
            reports.append({'name':name, **report})
            entries.append(_g4_config(kit))
            continue
        if 'g3' in kit.get('effect', {}):
            report = _write_g3_kit(out, kit)
            reports.append({'name':name, **report})
            entries.append(_g3_config(kit))
            continue
        if 'g2' in kit.get('effect', {}):
            report = _write_g2_kit(out, kit)
            reports.append({'name':name, **report})
            entries.append(_g2_config(kit, ground_geometry))
            continue
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
    if any(kit.get('effect', {}).get('screen_px', False) for kit in kits):
        directional = directional.replace('Vector2.ONE * art_scale * float(flare.get_meta',
            'Vector2.ONE * (1.0 if bool(VFX_KITS[cast_kit_index].get("screen_px", false)) else art_scale) * float(flare.get_meta')
    directional = _g1_directional(directional)
    a = directional.index('    var flare := AnimatedSprite2D.new()')
    b = directional.index('    var kit: Dictionary =', a)
    flare_block = ''.join('    '+line+'\n' for line in directional[a:b].splitlines())
    directional = directional[:a] + '    if not VFX_KITS[cast_kit_index].has("painted_travel"):\n' + flare_block + directional[b:]
    keeper = keeper.replace('func _physics_process(delta: float) -> void:\n', 'func _physics_process(delta: float) -> void:\n    _update_cast_halo()\n')
    keeper = keeper.replace('        _cast_frame_changed()', '        _update_cast_halo()\n        _cast_frame_changed()')
    directional = directional.replace('    cast_fired = true\n', '    cast_fired = true\n    _update_cast_halo()\n')
    directional += CAST_HALO_SCRIPT

    if any('travel_primitives' in kit.get('effect', {}) or 'orb' in kit.get('effect', {}) for kit in kits):
        directional = directional.replace('    # Device policy survives', '    var aim_scale: float = 1.0 if bool(kit.get("screen_px", false)) else art_scale\n    # Device policy survives')
        directional = directional.replace('float(kit.range_px) * art_scale', 'float(kit.range_px) * aim_scale')
    if has_g2:
        keeper = keeper.replace('    base_frames = sprite.sprite_frames', '    add_to_group("vfx_actors")\n    base_frames = sprite.sprite_frames')
        directional = directional.replace('const G1 = preload("res://scripts/vfx_g1.gd")', 'const G1 = preload("res://scripts/vfx_g1.gd")\nconst G2 = preload("res://scripts/vfx_g2.gd")')
        marker = '    # Device policy survives'
        start = directional.index(marker)
        stop = directional.index('    if not cast_ready:', start)
        old = directional[start:stop]
        policy = '    var destination: Dictionary\n    if kit.get("grammar", "G1") == "G2":\n        var cursor: Vector2 = get_global_mouse_position() if vfx_cursor_override == null else vfx_cursor_override\n        var touch: bool = vfx_cursor_override == null and (vfx_force_touch_device or DisplayServer.is_touchscreen_available())\n        destination = G2.resolve_ground(global_position, FACING_VECTORS[facing], cursor, float(kit.range_px), touch)\n    else:\n'
        policy += ''.join('    '+line+'\n' for line in old.replace('    var destination: Dictionary\n','').splitlines())
        directional = directional[:start]+policy+directional[stop:]
        directional = directional.replace('    G1.acquire(get_parent(), kit, socket, destination, self, art_scale)', '    if kit.get("grammar", "G1") == "G2":\n        G2.acquire(get_parent(), kit, socket, destination, self, art_scale)\n    else:\n        G1.acquire(get_parent(), kit, socket, destination, self, art_scale)')
    if has_g3:
        directional = directional.replace('const G1 = preload("res://scripts/vfx_g1.gd")', 'const G1 = preload("res://scripts/vfx_g1.gd")\nconst G3 = preload("res://scripts/vfx_g3.gd")')
        # Resolve the instant target from the current release socket on the ready frame.
        directional = directional.replace('    if not cast_ready:', '    if kit.get("grammar", "G1") == "G3":\n        if not cast_ready:\n            await get_tree().physics_frame\n        if not is_inside_tree(): return\n        var release_socket: Variant = _socket_world()\n        if release_socket == null: return\n        var instant_target: Dictionary = G3.resolve_target(get_tree(), release_socket, FACING_VECTORS[facing], float(kit.range_px), self)\n        G3.acquire(get_parent(), kit, release_socket, instant_target, self, art_scale)\n        return\n    if not cast_ready:')
    if has_g4:
        directional = directional.replace('const G1 = preload("res://scripts/vfx_g1.gd")', 'const G1 = preload("res://scripts/vfx_g1.gd")\nconst G4 = preload("res://scripts/vfx_g4.gd")')
        # Root-bound support dispatch precedes socket validation, flash and aim.
        directional = directional.replace('    cast_fired = true\n', '    cast_fired = true\n    if VFX_KITS[cast_kit_index].get("grammar", "") == "G4":\n        if not cast_ready:\n            await get_tree().physics_frame\n        if is_inside_tree(): G4.acquire(self, VFX_KITS[cast_kit_index])\n        return\n')
    by_name = {kit['name']: kit for kit in kits}
    for entry in entries:
        if entry.get('range_expiry') == 'fizzle':
            impact_name = by_name[entry['name']]['effect']['impact_binding']['kit']
            impact_kit = by_name[impact_name]
            record = json.loads((impact_kit['root']/impact_kit['effect']['pieces']['source']).read_text())
            entry['fizzle_pieces'] = [dict(texture='res://vfx/'+impact_name+'/pieces/'+item['mask'],
                material='res://vfx/'+impact_name+'/materials/Piece_Piece_%03d.tres' % item['id'],
                pivot=item['pivot'], area=item['area_px'], id=item['id'])
                for item in sorted(record['pieces'], key=lambda item: (item['area_px'], item['id']))[:3]]
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
[sub_resource type="CapsuleShape2D" id="HeadShape"]
radius = 32.5
height = 65.0
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
var release_facing: Vector2 = Vector2.ZERO
var travel_end: Vector2 = Vector2.ZERO
var release_sweep_start: Variant = null
var struck_ground: Variant = null
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
    release_facing = destination.get("facing", direction).normalized()
    distance = 0.0
    remaining_pierce = int(config.get("pierce", 0))
    struck_ground = null
    contacted.clear()
    strike_fired = false
    cast_origin = origin
    release_sweep_start = null
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
    # FL-2c: canonical world-pixel capsule; art alpha never defines gameplay.
    _configure_capsule(origin)
    set_deferred("monitoring", true)
    show()
    set_physics_process(true)
    _record("release")

func _configure_capsule(origin: Vector2) -> void:
    if direction.is_zero_approx(): direction = Vector2.RIGHT
    var shape := CapsuleShape2D.new()
    shape.radius = float(config.get("collision_radius_bh", 0.25)) * 130.0
    shape.height = maxf(float(config.get("head_length_px", 65.0)), shape.radius * 2.0)
    $CollisionShape2D.shape = shape
    $CollisionShape2D.rotation = direction.angle() - PI / 2.0
    $CollisionShape2D.position = -direction * shape.height / 2.0
    # The node records the leading tip; the capsule's rear starts at the socket.
    global_position = origin + direction * shape.height
    distance = shape.height
    release_sweep_start = origin + direction * shape.height

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
    # Test the complete emergence capsule, then sweep the same shape every frame.
    if release_sweep_start != null:
        start = release_sweep_start
        motion += global_position - start
        release_sweep_start = null
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
        query.transform = $CollisionShape2D.global_transform
        query.transform.origin += start - global_position
        query.motion = Vector2.ZERO
        var overlaps: Array = space.intersect_shape(query)
        var fraction: float = 0.0
        if overlaps.is_empty():
            query.motion = motion
            var fractions: PackedFloat32Array = space.cast_motion(query)
            fraction = fractions[1] if fractions.size() == 2 else 1.0
            query.motion = Vector2.ZERO
            query.transform.origin += motion * fraction
            overlaps = space.intersect_shape(query)
        if overlaps.is_empty():
            break
        for hit in overlaps:
            var body: CollisionObject2D = hit.collider
            excluded.append(body.get_rid())
            var along: float = (body.global_position - cast_origin).dot(release_facing)
            if along >= 32.5:
                hits.append({"area": body, "fraction": fraction, "along": along})
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
        if config.get("range_expiry", "burst") == "fizzle":
            _range_fizzle()
            return
        if bool(config.get("contact_only", false)):
            _spawn_impact(false)
        if contacted.is_empty() and resolved.kind == "cursor":
            _spawn_impact(false)
        if contacted.is_empty() and resolved.kind == "prop":
            cancel()
        else:
            expire()

func contact_body(area: CollisionObject2D, phase: String = "head") -> void:
    # Phase producers (chain hops, shards, field centre/rim) share the cast ledger.
    if not active or not is_instance_valid(area) or area == caster or contacted.has(area.get_instance_id()):
        return
    if phase not in ["head", "chain_hop", "field_centre", "shard", "rim"]:
        return
    # Near/behind candidates are ignored only for this sweep, never contacted.
    # Unshaped legacy phase callbacks explicitly report contact; only physical
    # collision bodies have a meaningful world-space contact envelope.
    if not area.get_shape_owners().is_empty() and (area.global_position - cast_origin).dot(release_facing) < 32.5:
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
    entry["position"] = [global_position.x, global_position.y]
    entry["contact_distance_px"] = cast_origin.distance_to(area.global_position)
    entry["strike_response"] = not strike_fired
    if area.is_in_group("vfx_targets"):
        _contact_label(area, body_index, contact_class)
    struck_ground = area.global_position
    _spawn_impact(not strike_fired, global_position if phase == "head" else area.global_position)
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
    if struck_ground != null: impact.set_meta("ground_anchor", struck_ground)
    impact.set("spell_scale", spell_scale)
    impact.set("caster", caster)
    impact.set("direction", direction)
    impact.position = get_parent().to_local(global_position if point == null else point)
    get_parent().add_child(impact)

func _range_fizzle() -> void:
    expire()

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


def _g1_capsule_config(kit):
    """Canonical BH radius and authored longitudinal extent, independent of alpha.

    Painted heads supply rear and tip coordinates. Orb primitives have declared
    BH extents. Legacy G1 frames use their full rectangular frame extent.
    Godot requires total capsule height >= diameter (a circle at equality).
    """
    data = kit.get('effect', {})
    radius = data.get('g1', {}).get('collision_radius_bh', .25)
    result = {'collision_radius_bh': radius}
    if 'travel_primitives' in data:
        head = data['travel_primitives']['head']
        length = math.dist(head['pivot'], head['rear_socket']) * head['scale'] if 'rear_socket' in head else 1.2 * 130.0
    elif 'orb' in data:
        extents = data['skill_spec']['presentation']['body_extents_bh']
        length = extents['orb'] * 130.0
        result['child_collision_radius_bh'] = data['orb']['shard'].get('collision_radius_bh', .15)
        result['child_head_length_px'] = extents['child'] * 130.0
    else:
        frames = data.get('phases', {}).get('travel', {}).get('frames', [])
        if frames and kit.get('root') is not None:
            with Image.open(kit['root']/frames[0]['file']) as image:
                length = image.width * data.get('phase_scale', {}).get('travel', 1.0)
        else:
            length = 1.2 * 130.0
    result['head_length_px'] = length
    return result


def _g1_config(kit):
    name = kit['name']
    root = 'vfx/'+name
    data = kit.get('effect', {})
    authored = bool(data)
    fields = {'res://'+root+'/sprites/'+source: 'res://'+root+'/'+field
              for source, field in data.get('distance_fields', {}).items() if source.startswith('travel/')}
    return {**({'screen_px': True} if data.get('screen_px', False) else {}), 'name': name, 'flare': 'res://'+root+'/flare.tres',
            'bolt': 'res://scenes/vfx/g1_projectile.tscn',
            'head': 'res://'+root+('/travel.tres' if authored else '/flare.tres'),
            'animation': 'travel' if authored else 'flare',
            'impact': 'res://scenes/vfx_'+name+'_impact.tscn',
            'speed_px_s': data.get('phases', {}).get('travel', {}).get('speed_px_s', 520.0),
            'pierce': data.get('pierce', 0),
            'palette_3': data.get('material', {}).get('palette', [[.35, .65, .8, 1]]*4)[3],
            'palette_2': data.get('material', {}).get('palette', [[.35, .65, .8, 1]]*4)[2],
            'range_px': 650.0, 'ground_squash': 1.0 if 'pieces' in data else data.get('ground_squash', 1.0),
            'phase_scale': data.get('phase_scale', {}).get('travel', 1.0),
            'material': 'res://'+root+'/materials/Body.tres' if authored else '',
            'binding': 'res://scripts/vfx_'+name+'_material.gd' if authored else '',
            **_g1_capsule_config(kit), 'fields': fields, 'trail_color': list(kit.get('tint', [.35, .65, .8]))+[.6], **_painted_g1_config(kit), **_orb_config(kit)}


def _g1_directional(script):
    script = script.replace('var socket_cells: Dictionary = {}',
                            'var socket_cells: Dictionary = {}\nvar cast_ready: bool = false\n'
                            'var vfx_cursor_override: Variant = null\n'
                            'const TOUCH_OVERLAY_BAND = 0.22\n'
                            'var vfx_force_touch_device: bool = false\n'
                            'const G1 = preload("res://scripts/vfx_g1.gd")')
    script = script.replace('    sprite.frame_changed.connect(_cast_frame_changed)',
                            '    sprite.frame_changed.connect(_cast_frame_changed)\n'
                            '    get_tree().physics_frame.connect(_g1_cast_ready, CONNECT_ONE_SHOT)')
    start = script.index('    var bolt: Area2D = ')
    end = script.index('\nfunc _process(', start)
    script = script[:start]+'''    var kit: Dictionary = VFX_KITS[cast_kit_index].duplicate(true)
    # Device policy survives handled overlay touches and browser-emulated mouse.
    # The explicit probe hook keeps precedence; desktop resolution is unchanged.
    var destination: Dictionary
    if vfx_cursor_override == null and (vfx_force_touch_device or DisplayServer.is_touchscreen_available()):
        var forward_point: Vector2 = global_position + FACING_VECTORS[facing].normalized() * float(kit.range_px) * art_scale
        destination = {"point": forward_point, "target": null, "kind": "cursor"}
    else:
        var cursor: Vector2 = get_global_mouse_position() if vfx_cursor_override == null else vfx_cursor_override
        destination = G1.resolve_target(get_tree(), global_position, direction, cursor, float(kit.range_px) * art_scale)
    if not cast_ready:
        await get_tree().physics_frame
    if not is_inside_tree():
        return
    destination["facing"] = FACING_VECTORS[facing].normalized()
    G1.acquire(get_parent(), kit, socket, destination, self, art_scale)

func _g1_cast_ready() -> void:
    cast_ready = true
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
    # G2 has both RGB material glass and indexed bodies; substitute separately.
    for metadata in (out/'vfx').glob('*/kit.json'):
        data = json.loads(metadata.read_text())
        if 'g3' in data:
            for path in (metadata.parent/'materials').glob('*.tres'):
                text=path.read_text()
                text=re.sub(r'(shader_parameter/palette_[0-3] = )Color\([^\n]+', r'\1Color(0.5, 0.5, 0.5, 1)', text)
                path.write_text(text)
            continue
        if 'g2' not in data: continue
        folder = metadata.parent
        for path in [folder/data['g2']['flask'], *sorted((folder/'derived').glob('glass_*.png'))]:
            with Image.open(path) as image:
                grey = Image.new('RGBA', image.size, (128,128,128,255))
                grey.putalpha(image.getchannel('A')); grey.save(path)
        for label in ('Field','Pulse','Decal'):
            path=folder/'materials'/(label+'.tres')
            text=path.read_text()
            text=re.sub(r'(shader_parameter/palette_[0-3] = )Color\([^\n]+', r'\1Color(0.5, 0.5, 0.5, 1)', text)
            path.write_text(text)
    for path in (out/'vfx').rglob('*.png'):
        if 'sprites' not in path.parts:
            continue
        if any(part in ('primitives', 'travel_keys') for part in path.parts):
            continue  # indexed travel uses a grey palette; retain band-step semantics
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
        if any(path in text for path in ('res://scripts/vfx/piece_burst.gd', 'res://scripts/vfx/piece_burst_v2.gd', 'res://scripts/vfx/piece_burst_v2_keys.gd', 'res://scripts/vfx/piece_burst_v1r.gd')):
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
    text = re.sub(r'"material": "(?![^"]*/materials/(?:Travel_|Field))[^"]+"', '"material": ""', text)
    text = re.sub(r'"binding": "[^"]+"', '"binding": ""', text)
    text = re.sub(r'    flare.material = load\([^\n]+\n', '    flare.material = null\n', text)
    text = re.sub(r'^    +preload\([^\n]+\.bind\(flare,[^\n]+\n', '', text, flags=re.M)
    keeper.write_text(text)
    for material in (out/'vfx').glob('*/materials/Travel_*.tres'):
        text = material.read_text()
        text = re.sub(r'(shader_parameter/palette_[0-3] = )Color\([^\n]+', r'\1Color(0.5, 0.5, 0.5, 1)', text)
        material.write_text(text)


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
    if kit['effect'].get('orb',{}).get('expiry_mode')=='nova':
        return _write_orb_nova(out,kit,resource_root,prefix)
    if kit['effect']['pieces']['template'] == 'burst_v1r':
        return _write_piece_burst_v1r(out, kit, resource_root, prefix)
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
        material_config = dict(data['material'], blend_mode=mode or data['material']['blend_mode'])
        if 'dissolve_order' in config:
            material_config['dissolve_order'] = config['dissolve_order']
        write_vfx_material(out, mat, material_config, field, dark)
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
    if bool(config.get("screen_px", false)):
        spell_scale = 1.0
    $FloorLight.scale *= spell_scale
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
        # Seeded along stretch is 2.0..2.5; drift is in core-radius units.
        var root_drift_px: float = 0.0 if bool(item.core) else float(config.root_drift) * float(config.core_radius_px) * ease
        var root_start: Vector2 = Vector2(float(item.root[0])-float(config.centre[0]),float(item.root[1])-float(config.centre[1]))
        axis.set_position(root_start + Vector2.RIGHT.rotated(float(item.axis_radians)) * root_drift_px)
        axis.rotation = float(item.axis_radians) + deg_to_rad(float(item.rotation_deg)) * ease
        if bool(item.core):
            var core_t: float = clampf(float(age-flight_start)/9.0,0.0,1.0)
            node.scale = Vector2.ONE * lerpf(1.0,1.25,1.0-pow(1.0-core_t,3.0))
        else:
            node.scale = Vector2(lerpf(1.0,float(item.along),ease),lerpf(1.0,0.85,ease))
        # Tips burn back first; no band loss during expansion or erosion.
        var erode: float = erosion_t
        var residue_t: float = clampf(float(age-residue_start)/float(config.residue_frames),0.0,1.0)
        var dissolve: float = 1.0 if age >= residue_end else 0.8 * residue_t
        axis.visible = active and age < residue_start
        paint.visible = true
        paint.material.set_shader_parameter("erode",erode)
        paint.material.set_shader_parameter("dissolve",0.0)
        var root_erode: float = float(config.residue_erode) * erosion_t
        var outer: float = 1.0 - root_erode
        root_sprite.visible = active
        root_sprite.material.set_shader_parameter("erode",root_erode)
        root_sprite.material.set_shader_parameter("dissolve",dissolve)
        if data.dark_axis != null:
            var dark: Node2D = data.dark_axis
            dark.transform = axis.transform
            dark.visible = axis.visible
            dark.get_node("Stretch").scale = node.scale
            var dark_paint: Sprite2D = dark.get_node("Stretch/Piece_%03d" % int(item.id))
            dark_paint.visible = true
            dark_paint.material.set_shader_parameter("erode",erode)
            dark_paint.material.set_shader_parameter("dissolve",0.0)
            var dark_root: Sprite2D = data.dark_root
            dark_root.visible = active
            dark_root.material.set_shader_parameter("erode",root_erode)
            dark_root.material.set_shader_parameter("dissolve",dissolve)
        if active:
            count += 1
        states.append({"id":item.id,"visible":active,"core":item.core,"scale":[node.scale.x,node.scale.y],"root_position":[axis.position.x,axis.position.y],"root_displacement_px":root_drift_px,"rotation_deg":float(item.rotation_deg)*ease,"erode":erode,"dissolve":dissolve,"residue_erode":root_erode,"residue_outer":outer,"erode_outside_in":true,"expanded_dissolve":0.0,"screen_px":bool(config.get("screen_px",false))})
    trace.append({"age_frames":age,"stage":stage,"peak_visible":$Art/Peak.visible,"shard_count":count,"source_piece_count":pieces.size(),"pieces":states})
    if age >= residue_end:
        hide()
        _write_trace()
        queue_free()
'''


def _write_piece_burst_v2(out, kit, resource_root, prefix):
    """Rooted anisotropic sprites plus stationary eroded core/root coverage.

    The stationary layer uses the same original masks and whole-body field.
    Outside-in erosion retains the innermost coverage without an inner hole.
    No shader or scene used by a legacy kit is changed.
    """
    import copy
    import numpy as np
    from export.effect_kit import (load_pieces, piece_geometry, piece_stretch,
                                   distance_field, write_vfx_material, piece_erode_noise, residue_entry, erosion_noise_texture)
    data = kit['effect']
    config, record, _ = load_pieces(data['pieces'], kit['root'], runtime=True)
    # Reuse v1's unchanged layer/material plumbing, then replace only this scene.
    legacy = dict(kit, effect=copy.deepcopy(data))
    legacy['effect']['pieces']['template'] = 'burst_v1'
    legacy['effect']['pieces'].pop('key_states', None)
    legacy['effect']['pieces'].pop('boil', None)
    for opt in ('timing','ember_ending','interleave','stretch','core_residue','smoke'): legacy['effect']['pieces'].pop(opt, None)
    if 'ember_ending' in config:
        legacy['effect']['pieces'].update(residue_s=.3,residue_fraction=.2)
    legacy['effect']['material'].pop('erode_noise', None)
    canonical = out/'scenes/vfx/piece_burst.tscn'
    owns_canonical = not canonical.exists()
    _write_piece_burst(out, legacy, resource_root, prefix)
    target = out/f'scenes/{prefix}_impact.tscn'
    scene = target.read_text()
    source_root = kit['root']/Path(config['source']).parent
    geometry = piece_geometry(record, source_root)
    runtime_path = out/resource_root/'pieces/burst_runtime.json'
    runtime = json.loads(runtime_path.read_text())
    runtime.update(template='burst_v2', erode_outside_in=True, screen_px=data.get('screen_px', False), core_centre=geometry['core_centre'],
                   core_radius_px=geometry['core_radius_px'], root_drift=config['root_drift'],
                   grouped_dissolve=config.get('dissolve_order', data['material'].get('dissolve_order', [[3],[2],[1],[0]])) != [[3],[2],[1],[0]], pieces=[])
    with Image.open(source_root/record['peak_index']) as image:
        peak = np.asarray(image.convert('RGBA'))
    field = distance_field(peak)
    field_rel = resource_root+'/pieces/whole_body_distance.png'
    Image.fromarray(field).save(out/field_rel)
    noise = piece_erode_noise(data)
    noise_rel = None
    noise_pixels = None
    if noise or 'boil' in config or any(k in data['layers'] for k in ('core', 'shimmer')):
        noise_rel = resource_root+'/pieces/whole_body_noise.png'
        noise_pixels = erosion_noise_texture(peak)
        Image.fromarray(noise_pixels).save(out/noise_rel)
    runtime.update(residue_entry(peak, field, .12 if 'ember_ending' in config else config['residue_fraction'], noise, noise_pixels))
    if 'stretch' in config: runtime['stretch'] = config['stretch']
    if 'timing' in config: runtime['timing'] = config['timing']
    if 'ember_ending' in config:
        runtime.update(ember_ending=config['ember_ending'], residue_frames=0, residue_s=0)
    if noise_rel:
        runtime['erode_noise'] = noise
        runtime['erosion_noise_texture'] = noise_rel
    scene = scene.replace('res://scripts/vfx/piece_burst.gd','res://scripts/vfx/piece_burst_v2.gd')
    # Root-only upper clip is a v2 shader variant. The shared T4a shader is frozen.
    extra_nodes = ['[node name="Roots" type="Node2D" parent="Art"]\n',
                   '[node name="DarkRoots" type="Node2D" parent="Art"]\nz_index = -1\n']
    def vector(x,y): return f'Vector2({float(x):.12g}, {float(y):.12g})'
    if 'interleave' in config:
        scene = _interleave_nodes(out, kit, resource_root, scene, runtime, geometry, config)
    for item in geometry['pieces']:
        ident = item['id']; name = 'Piece_%03d' % ident
        material_rel = resource_root+'/materials/Piece_'+name+'.tres'
        material_config = dict(data['material'], erode_outside_in=True)
        if noise or 'erode_noise' in material_config:
            material_config['erode_noise'] = noise
        if 'dissolve_order' in config:
            material_config['dissolve_order'] = config['dissolve_order']
        write_vfx_material(out, material_rel, material_config, item.get('interleave_field', field_rel), noise_texture=noise_rel)
        material = (out/material_rel).read_text()
        shader_ref = re.search(r'path="res://([^"]+\.gdshader)"', material)[1]
        root_shader = str(Path(shader_ref).with_name('vfx_material_v2_roots.gdshader'))
        (out/root_shader).write_text((out/shader_ref).read_text())
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
                       + ('visible = false\n' if item.get('interleave') else '') +
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
        runtime['pieces'].append({**item, **piece_stretch(config['seed'],ident, config.get('stretch')),
                                  'erosion_start_tick':15})
        if item.get('interleave') and 'stretch' in config:
            runtime['pieces'][-1]['along'] = 1.3 if config.get('interleave',{}).get('count') == [5,7] else 1.15
    scene += '\n'.join(extra_nodes)
    scene = re.sub(r'load_steps=\d+', 'load_steps='+str(scene.count('[ext_resource ')+1),scene,count=1)
    script = PIECE_BURST_V2_SCRIPT
    if config.get('key_states'):
        scene, script = _emit_key_states(out, kit, resource_root, scene, runtime, config)
        scene = scene.replace('res://scripts/vfx/piece_burst_v2.gd',
                              'res://scripts/vfx/piece_burst_v2_keys.gd')
        (out/'scripts/vfx/piece_burst_v2_keys.gd').write_text(script)
    if layers_fl2 := data['layers'].get('glow', {}).get('peak'):
        runtime['fire_layers'] = data['layers']
        runtime['palette'] = data['material']['palette']
        (out/'scripts/vfx_fire_motes.gd').write_text(FIRE_MOTES_SCRIPT)
        if 'contact_light' in data['layers']:
            (out/'scripts/vfx_contact_light.gd').write_text(CONTACT_LIGHT_SCRIPT)
        script = _fire_burst_script(script if config.get('key_states') else PIECE_BURST_V2_SCRIPT)
        scene = scene.replace('res://scripts/vfx/piece_burst_v2_keys.gd','res://scripts/vfx/piece_burst_fl2.gd').replace('res://scripts/vfx/piece_burst_v2.gd','res://scripts/vfx/piece_burst_fl2.gd')
        (out/'scripts/vfx/piece_burst_fl2.gd').write_text(script)
    if any(k in data['layers'] for k in ('core', 'shimmer')) or 'boil' in config:
        if not config.get('key_states') and not layers_fl2: script = PIECE_BURST_V2_SCRIPT
        scene, script = _emit_anti_decal(out, kit, resource_root, scene, runtime, config, script)
        scene = scene.replace('res://scripts/vfx/piece_burst_fl2.gd', 'res://scripts/vfx/piece_burst_fl3.gd').replace('res://scripts/vfx/piece_burst_v2_keys.gd', 'res://scripts/vfx/piece_burst_fl3.gd').replace('res://scripts/vfx/piece_burst_v2.gd', 'res://scripts/vfx/piece_burst_fl3.gd')
        (out/'scripts/vfx/piece_burst_fl3.gd').write_text(script)
    if 'timing' in config:
        script = _fl4_burst_script(script)
        if 'ember_ending' in config:
            _write_living_ember_assets(out)
            script = script.replace('    tree_exiting.connect(_write_trace)', '    _ready_ember_ending()\n    tree_exiting.connect(_write_trace)')
            script = script.replace('    if age >= residue_end:\n        hide()', '    _clock_ember_ending(age)\n    if age >= 114:\n        hide()')
            script += EMBER_ENDING_SCRIPT
            if 'core_residue' in config or 'smoke' in config:
                script = _fl5_ending(out, kit, resource_root, runtime, config, geometry, script)
        scene = re.sub(r'res://scripts/vfx/piece_burst_(?:v2_keys|v2|fl2|fl3)\.gd', 'res://scripts/vfx/piece_burst_fl4.gd', scene)
        if 'interleave' in config:
            script = _fl4b_burst_script(script)
            if 'stretch' in config:
                script = _fl4c_burst_script(script)
            scene = scene.replace('res://scripts/vfx/piece_burst_fl4.gd', 'res://scripts/vfx/piece_burst_fl4b.gd')
            (out/'scripts/vfx/piece_burst_fl4b.gd').write_text(script)
        else:
            (out/'scripts/vfx/piece_burst_fl4.gd').write_text(script)
    if 'stretch' in config:
        # Apply across to every opted-in v2 template, not only the fire variant.
        script = script.replace('lerpf(1.0,0.85,ease)', 'lerpf(1.0,float(config.stretch.across),ease)')
        script = script.replace('lerpf(1.0,0.85,item_ease)', 'lerpf(1.0,float(config.stretch.across),item_ease)')
        script_path = f'scripts/vfx/{prefix}_stretch.gd'
        scene = re.sub(r'res://scripts/vfx/piece_burst_[^"\n]+\.gd', 'res://'+script_path, scene)
        (out/script_path).write_text(script)
    # Shared files must not depend on which kit was emitted last.
    (out/'scripts/vfx/piece_burst_v2.gd').write_text(PIECE_BURST_V2_SCRIPT)
    runtime_path.write_text(json.dumps(runtime,indent=2)+'\n')
    target.write_text(scene)
    if owns_canonical: canonical.write_text(scene)
    (out/'scenes/vfx/piece_burst_v2.tscn').write_text(scene)


KEY_STATE_READY = """    for item in config.key_states:
        for suffix in ["", "Dark"]:
            var sprite: Sprite2D = get_node("Art/Key_" + str(item.state) + suffix)
            sprite.material = sprite.material.duplicate()
            if grey_bodies and suffix == "":
                for band in range(4):
                    sprite.material.set_shader_parameter("palette_" + str(band), Color(128.0/255.0,128.0/255.0,128.0/255.0,1))
"""

KEY_STATE_CLOCK = """    var active_key: String = ""
    var key_erode: float = float(config.residue_erode) * erosion_t
    var key_residue_t: float = clampf(float(age-residue_start)/float(config.residue_frames),0.0,1.0)
    var key_dissolve: float = 1.0 if age >= residue_end else 0.8 * key_residue_t
    for item in config.key_states:
        var enabled: bool = age >= int(item.at_age) and age < int(item.at_age) + int(item.hold_frames) and age < residue_end
        var sprite: Sprite2D = get_node("Art/Key_" + str(item.state))
        var dark: Sprite2D = get_node("Art/Key_" + str(item.state) + "Dark")
        sprite.visible = enabled
        dark.visible = enabled and bool(config.dark_duplicate)
        for node in [sprite, dark]:
            node.material.set_shader_parameter("erode", key_erode)
            node.material.set_shader_parameter("dissolve", key_dissolve)
        if enabled:
            active_key = str(item.state)
    for name in ["Pieces", "Roots", "DarkPieces", "DarkRoots"]:
        get_node("Art/" + name).visible = active_key == ""
    if active_key != "":
        $Art/Peak.hide()
        $Art/PeakDark.hide()
    trace[-1]["key_state"] = active_key
    trace[-1]["key_erode"] = key_erode
    trace[-1]["key_dissolve"] = key_dissolve
    trace[-1]["pieces_container_visible"] = $Art/Pieces.visible
    trace[-1]["visible_piece_count"] = count if active_key == "" else 0
"""


def _emit_key_states(out, kit, resource_root, scene, runtime, config):
    """Opt-in v2 emission. Empty states preserve all pre-T4q exported bytes.

    Key textures are full guide canvases centred on the impact origin. Their
    distance-field range is preconditioned to the retained fraction at entry:
    already-eroded drawings are not eroded twice on their first held tick.
    Thereafter the SAME absolute erode/dissolve uniforms keep advancing.
    """
    import numpy as np
    from export.effect_kit import distance_field, write_vfx_material
    flight = int(runtime['flash_frames']) + int(runtime['hold_frames'])
    end = flight + 36 + int(runtime['residue_frames'])
    runtime['key_states'] = config['key_states']
    for state in config['key_states']:
        if state['at_age'] < flight or state['at_age'] + state['hold_frames'] > end:
            raise ValueError('key_state interval must lie inside piece lifetime')
        name = state['state']
        source = kit['root']/state['png']
        target = out/resource_root/state['png']
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.resolve() != target.resolve(): shutil.copyfile(source, target)
        with Image.open(source) as image:
            rgba = np.array(image.convert('RGBA'))
        erosion_age = config.get('timing', {}).get('erosion_age', flight+15)
        paint_end = config.get('timing', {}).get('paint_end_age', flight+36)
        erode = float(runtime['residue_erode']) * max(0., min(1., (state['at_age']-erosion_age)/(paint_end-erosion_age)))
        field = np.minimum(254, np.floor(distance_field(rgba).astype(float)*(1-erode))).astype(np.uint8)
        field_rel = resource_root+'/pieces/key_'+name+'_distance.png'
        Image.fromarray(field).save(out/field_rel)
        for dark in (False, True):
            node = 'Key_'+name+('Dark' if dark else '')
            material = dict(kit['effect']['material'], erode_outside_in=True)
            material.pop('erode_noise', None)  # preconditioned whole-state coverage
            if 'dissolve_order' in config: material['dissolve_order'] = config['dissolve_order']
            if dark: material['blend_mode'] = 'MIX'
            mat = resource_root+'/materials/'+node+'.tres'
            noise_rel = None
            noise_uv_transform = None
            if 'boil' in config:
                material['erode_noise'] = runtime.get('erode_noise', .4) or .4
                noise_rel = runtime['erosion_noise_texture']
                with Image.open(out/noise_rel) as whole:
                    sx, sy = rgba.shape[1]/whole.width, rgba.shape[0]/whole.height
                # The held drawings use a larger canvas around the same origin.
                noise_uv_transform = (sx, sy, (1-sx)/2, (1-sy)/2)
            write_vfx_material(out, mat, material, field_rel, dark_duplicate=dark,
                               noise_texture=noise_rel, noise_uv_transform=noise_uv_transform)
            ext = (f'[ext_resource type="Texture2D" path="res://{resource_root}/{state["png"]}" id="T{node}"]\n'
                   f'[ext_resource type="Material" path="res://{mat}" id="M{node}"]\n')
            first = scene.index('[node ')
            scene = scene[:first]+ext+scene[first:]
            scene += (f'\n[node name="{node}" type="Sprite2D" parent="Art"]\n'
                      'visible = false\ntexture_filter = 2\ncentered = false\n'
                      f'offset = Vector2({-rgba.shape[1]/2}, {-rgba.shape[0]/2})\n'
                      f'texture = ExtResource("T{node}")\nmaterial = ExtResource("M{node}")\n'
                      + ('z_index = -1\n' if dark else ''))
    scene = re.sub(r'load_steps=\d+', 'load_steps='+str(scene.count('[ext_resource ')+1),scene,count=1)
    script = PIECE_BURST_V2_SCRIPT.replace('    tree_exiting.connect(_write_trace)', KEY_STATE_READY+'    tree_exiting.connect(_write_trace)')
    script = script.replace('    if age >= residue_end:\n        hide()', KEY_STATE_CLOCK+'    if age >= residue_end:\n        hide()')
    return scene, script



# T4p travel is opt-in. Exporting the previous eight kits emits identical bytes.
def _painted_g1_config(kit):
    data = kit.get('effect', {})
    if 'travel_primitives' not in data: return {}
    root = 'res://vfx/'+kit['name']+'/'
    primitives = json.loads(json.dumps(data['travel_primitives']))
    for role in ('head', 'streak'):
        primitives[role]['png'] = root+primitives[role]['png']
        primitives[role]['material'] = root+'materials/Travel_'+role+'.tres'
        if role == 'head': primitives[role]['fizzle_material'] = root+'materials/Fizzle_head.tres'
    states = json.loads(json.dumps(data.get('key_states', [])))
    for i, state in enumerate(states):
        state['png'] = root+state['png']
        state['material'] = root+'materials/Travel_key_'+str(i)+'.tres'
    return {'fire_layers': data['layers'] if 'cast' in data['layers'] else {}, 'palette': data['material']['palette'], 'bolt': ('res://scenes/vfx/g1_ice_projectile.tscn' if data.get('pieces', {}).get('template') == 'burst_v1r' else 'res://scenes/vfx/g1_fl4_projectile.tscn' if 'core' in data['layers'].get('travel', {}) else 'res://scenes/vfx/g1_painted_projectile.tscn'),
            'range_px': data['skill_spec']['mechanics']['range_px'],
            'speed_px_s': data['skill_spec']['mechanics']['speed_px_s'],
            'spec_speed_px_s': data['skill_spec']['mechanics']['speed_px_s'],
            'contact_only': True, 'grammar': data['skill_spec']['grammar'],
            'aim_rule': data['skill_spec']['mechanics']['aim_rule'],
            'termination': data['skill_spec']['mechanics']['termination'],
            'range_expiry': data['skill_spec']['mechanics'].get('range_expiry', 'burst'),
            'origin_socket': data['skill_spec']['mechanics']['origin_socket'],
            'impact': 'res://scenes/vfx_'+data['impact_binding']['kit']+'_impact.tscn',
            'seed': data['impact_binding']['seed'], 'painted_travel': primitives,
            **(_fl4b_travel_metrics(kit) if 'core' in data['layers'].get('travel', {}) else {}),
            'key_states': states, 'enabled_layers': data['skill_spec']['presentation']['enabled_layers'],
            'dark_duplicate': data['layers'].get('dark_duplicate', False),
            'strike_stop_s': data['skill_spec']['presentation'].get('layers', {}).get('hit_stop', {}).get('frames', data['skill_spec']['presentation']['phase_envelope_s']['contact_frames'])/60.0}


def _write_painted_travel(out, kit, resource_root):
    import numpy as np
    from export.effect_kit import write_vfx_material
    data = kit['effect']
    if data['layers'].get('cast') or data['layers'].get('travel'):
        (out/'scripts/vfx_fire_motes.gd').write_text(FIRE_MOTES_SCRIPT)
    items = [(role, data['travel_primitives'][role]) for role in ('head', 'streak')]
    items += [('key_'+str(i), state) for i, state in enumerate(data.get('key_states', []))]
    for role, item in items:
        source = kit['root']/item['png']
        target = out/resource_root/item['png']
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        field = data['distance_fields'].get(item['png'], 'distance/travel_keys/'+role+'.png')
        destination = out/resource_root/field
        destination.parent.mkdir(parents=True, exist_ok=True)
        if item['png'] in data['distance_fields']:
            shutil.copyfile(kit['root']/field, destination)
        else:
            # Conductor-bound travel keys are emitter-owned, like piece keys.
            from export.effect_kit import distance_field
            with Image.open(source) as image:
                Image.fromarray(distance_field(np.asarray(image.convert('RGBA')))).save(destination)
        if role == 'head' and 'core' in data['layers'].get('travel', {}):
            from export.effect_kit import distance_field
            with Image.open(source) as image: pixels = np.asarray(image.convert('RGBA'))
            Image.fromarray(distance_field(pixels)).save(destination)
        if role == 'streak':
            # T4a centre-out comparison on an x field = tail-to-socket erosion.
            with Image.open(source) as image: rgba = np.asarray(image.convert('RGBA'))
            ys, xs = np.nonzero(rgba[..., 3])
            x = np.arange(rgba.shape[1], dtype=float)
            ramp = np.clip((x-xs.min())/max(1, xs.max()-xs.min()), 0, 1)
            field = 'distance/primitives/tail.png'
            destination = out/resource_root/field
            Image.fromarray(np.broadcast_to(np.rint(ramp*255).astype(np.uint8), rgba.shape[:2])).save(destination)
        if role == 'streak' and data.get('pieces', {}).get('template') == 'burst_v1r':
            # Dedicated scene/script leaves all E1 resources byte-identical.
            _write_ground_effects(out)
            (out/'scripts/vfx_g1_ice.gd').write_text(ICE_G1_SCRIPT)
            ice_scene = G1_SCENE.replace('res://scripts/vfx_g1.gd', 'res://scripts/vfx_g1_ice.gd')
            ice_scene = ice_scene.replace('collision_layer = 0', 'z_as_relative = false\nz_index = 3\ncollision_layer = 0')
            for node in ('Streak', 'KeyState', 'DarkHead', 'DarkStreak', 'DarkKey', 'CastHalo'):
                ice_scene += '\n[node name="'+node+'" type="Sprite2D" parent="."]\ntexture_filter = 2\nvisible = false\nz_index = '+str(-2 if node.startswith('Dark') else -1 if node in ('Streak','CastHalo') else 0)+'\n'
            (out/'scenes/vfx/g1_ice_projectile.tscn').write_text(ice_scene)
        material = dict(data['material'], erode=0.0, dissolve=0.0, erode_outside_in=False)
        material.pop('erode_noise', None)
        material.pop('dissolve_order', None)
        noise_rel = None
        if role == 'streak' and data['layers'].get('travel', {}).get('erode_noise'):
            # Keep the longitudinal field canonical: 0 at tail, 255 at socket.
            # A dedicated shader adapter converts to the outside-in noise plane.
            from export.effect_kit import erosion_noise_texture
            noise_rel = resource_root+'/distance/primitives/tail_noise.png'
            Image.fromarray(erosion_noise_texture(rgba)).save(out/noise_rel)
            material.update(erode_outside_in=True, erode_noise=data['layers']['travel']['erode_noise'])
        write_vfx_material(out, resource_root+'/materials/Travel_'+role+'.tres', material, resource_root+'/'+field, noise_texture=noise_rel,
                           noise_uv_transform=(1,1,0,0) if role == 'streak' and 'boil' in data['layers'].get('travel', {}) else None)
        if role == 'streak' and noise_rel:
            # Preserve FL-2's exact noise/erosion function without reversing the
            # stored tail field or modifying the shared head/piece shader.
            material_path = out/resource_root/'materials/Travel_streak.tres'
            material_text = material_path.read_text()
            shader_path = re.search(r'path="res://([^"\n]+\.gdshader)"', material_text)[1]
            tail_path = Path(shader_path).with_stem(Path(shader_path).stem+'_tail')
            shader_text = (out/shader_path).read_text()
            shader_text = shader_text.replace(
                'float distance_value = texture(distance_texture, UV).r;',
                'float distance_value = 1.0 - texture(distance_texture, UV).r;')
            (out/tail_path).write_text(shader_text)
            material_path.write_text(material_text.replace(shader_path, tail_path.as_posix()))
        if role == 'head':
            write_vfx_material(out, resource_root+'/materials/Fizzle_head.tres', dict(material, erode_outside_in=True), resource_root+'/'+field)

    if 'core' in data['layers'].get('travel', {}): _write_fl4_travel(out, kit, resource_root)


PAINTED_G1_SCRIPT = r'''extends "res://scripts/vfx_g1.gd"
var draining: bool = false
var stop_age: int = 0
var travel_state: String = "rest"
var rest_head: Texture2D
var fizzling: bool = false
var fizzle_trace: Array = []
var fizzle_shards: Array[Sprite2D] = []
var fire_fx: Node2D
var trail_motes: Node2D
var fire_trace: Array = []
var release_sort_override: bool = false
var normal_z_index: int = 0
var normal_z_as_relative: bool = true

# FL-5c: elevated tip crosses the body on camera-facing casts. Ages 0..10
# include the release sample; at age 11 restore the ordinary scene/y-sort.
func _effective_z(item: CanvasItem) -> int:
    var total: int = item.z_index
    while item.z_as_relative and item.get_parent() is CanvasItem:
        item = item.get_parent()
        total += item.z_index
    return total

func _release_draw_order(age: int) -> void:
    if not release_sort_override: return
    if age <= 10 and is_instance_valid(caster):
        z_as_relative = false
        z_index = _effective_z(caster) + 1
    else:
        z_index = normal_z_index
        z_as_relative = normal_z_as_relative
        release_sort_override = false

func release(kit: Dictionary, origin: Vector2, destination: Dictionary, owner_node: Node2D = null, art_scale: float = 1.0) -> void:
    if release_sort_override:
        z_index = normal_z_index
        z_as_relative = normal_z_as_relative
    normal_z_index = z_index
    normal_z_as_relative = z_as_relative
    release_sort_override = false
    draining = false
    fizzling = false
    fizzle_trace.clear()
    for shard in fizzle_shards: shard.queue_free()
    fizzle_shards.clear()
    super.release(kit, origin, destination, owner_node, art_scale)
    release_sort_override = release_facing.y > 0.0 and is_instance_valid(caster)
    _release_draw_order(0)
    # Authored screen pixels must not inherit the actor/world drawing scale.
    # A top-level transform also keeps velocity and bound key states in pixels.
    if bool(config.get("screen_px", false)):
        top_level = true
        global_transform = Transform2D(0.0, origin)
    # Snapshot direction at release and terminate at range, never the cursor.
    if direction.is_zero_approx():
        direction = Vector2.RIGHT
    var paint: Dictionary = config.painted_travel
    _configure_capsule(origin)
    cast_origin = origin
    travel_end = origin + direction * float(config.range_px)
    rest_head = load(paint.head.png)
    $Head.sprite_frames = $Head.sprite_frames.duplicate()
    $Head.sprite_frames.set_frame("travel", 0, rest_head)
    $Head.centered = false
    $Head.offset = -Vector2(paint.head.pivot[0], paint.head.pivot[1])
    $Head.scale = Vector2.ONE * float(paint.head.scale)
    $Head.material = load(paint.head.material).duplicate()
    $Head.show()
    for node in [$Streak, $KeyState, $DarkHead, $DarkStreak, $DarkKey, $CastHalo]:
        node.rotation = direction.angle()
        node.modulate = Color.WHITE
    $Head.rotation = direction.angle()
    $Streak.texture = load(paint.streak.png)
    $Streak.centered = false
    $Streak.offset = -Vector2(paint.streak.pivot[0], paint.streak.pivot[1])
    $Streak.material = load(paint.streak.material).duplicate()
    $Streak.show()
    $KeyState.hide()
    $CastHalo.hide()
    $Trail.hide()
    fire_trace.clear()
    fire_fx = null
    trail_motes = null
    if not config.get("fire_layers", {}).is_empty():
        var pool = load("res://scripts/vfx_fire_motes.gd")
        fire_fx = pool.acquire(get_parent())
        fire_fx.start_cast(config, origin, caster.global_position if is_instance_valid(caster) else origin, direction)
        if config.fire_layers.get("travel", {}).has("trail"):
            trail_motes = pool.acquire(get_parent())
            trail_motes.start_trail(config.fire_layers.travel.trail, config.palette, int(config.seed))
    _paint_clock(0)

func _physics_process(delta: float) -> void:
    _release_draw_order(age_frames())
    if is_instance_valid(trail_motes): trail_motes.emitting = active
    if fizzling:
        _fizzle_clock(age_frames() - stop_age)
        return
    if draining:
        var erode: float = clampf(float(age_frames() - stop_age) / (float(config.painted_travel.tail_s) * 60.0), 0.0, 1.0)
        $Streak.material.set_shader_parameter("erode", erode)
        $DarkStreak.material.set_shader_parameter("erode", erode)
        if erode >= 1.0:
            draining = false
            hide()
            set_physics_process(false)
        return
    if active:
        _paint_clock(age_frames())
    super._physics_process(delta)
    $Trail.hide()

func _paint_clock(age: int) -> void:
    _release_draw_order(age)
    var paint: Dictionary = config.painted_travel
    var ratio: float = clampf(float(config.speed_px_s) / float(config.spec_speed_px_s), 0.6, 1.4)
    $Streak.scale = Vector2(ratio, 1.0) * float(paint.streak.scale)
    var socket: Vector2 = (Vector2(paint.head.rear_socket[0], paint.head.rear_socket[1]) - Vector2(paint.head.pivot[0], paint.head.pivot[1])) * float(paint.head.scale)
    $Streak.position = socket.rotated(direction.angle())
    # Two held ticks per flicker state; only band 3 is removed at 0.5.
    $Streak.material.set_shader_parameter("dissolve", 0.5 if (age / 2) % 2 == 1 else 0.0)
    $Head.material.set_shader_parameter("dissolve", 0.0)
    var selected: Dictionary = {}
    var states: Array = config.key_states
    if not states.is_empty():
        var cycle: int = 0
        for state in states:
            cycle += int(paint.rest_hold_frames) + int(state.hold_frames)
        var tick: int = age % cycle
        for state in states:
            if tick < int(paint.rest_hold_frames):
                break
            tick -= int(paint.rest_hold_frames)
            if tick < int(state.hold_frames):
                selected = state
                break
            tick -= int(state.hold_frames)
    travel_state = str(selected.get("state", "rest"))
    $Head.visible = selected.is_empty()
    $Streak.visible = selected.is_empty()
    $KeyState.visible = not selected.is_empty()
    if not selected.is_empty():
        $KeyState.texture = load(selected.png)
        $KeyState.material = load(selected.material)
        $KeyState.centered = false
        $KeyState.offset = -Vector2(selected.pivot[0], selected.pivot[1])
        $KeyState.scale = Vector2.ONE * float(selected.scale)
    if not config.get("fire_layers", {}).is_empty():
        var travel: Dictionary = config.fire_layers.get("travel", {})
        var period: int = int(travel.get("flicker_frames", 0))
        var swapped: bool = period > 0 and (age / maxi(1,period)) % 2 == 1
        for band in [2,3]:
            var colour: Array = config.palette[5-band if swapped else band]
            $Head.material.set_shader_parameter("palette_"+str(band), Color(colour[0],colour[1],colour[2],colour[3]))
            if $KeyState.visible:
                $KeyState.material = $KeyState.material.duplicate()
                $KeyState.material.set_shader_parameter("palette_"+str(band), Color(colour[0],colour[1],colour[2],colour[3]))
        if is_instance_valid(trail_motes):
            trail_motes.source_point = global_position + socket.rotated(direction.angle())
            trail_motes.emitting = active
        fire_trace.append({"age":age,"swapped":swapped,"period":period,"rear":[(global_position+socket.rotated(direction.angle())).x,(global_position+socket.rotated(direction.angle())).y]})
    _dark_copy($DarkHead, $Head, rest_head)
    _dark_copy($DarkStreak, $Streak, $Streak.texture)
    if not selected.is_empty():
        _dark_copy($DarkKey, $KeyState, $KeyState.texture)
    else:
        $DarkKey.hide()

func _dark_copy(node: Sprite2D, source: Node2D, texture: Texture2D) -> void:
    node.texture = texture
    node.centered = false
    node.offset = source.offset
    node.transform = source.transform
    node.visible = source.visible and bool(config.dark_duplicate)
    node.material = source.material.duplicate()
    node.material.set_shader_parameter("dark_duplicate", true)

func contact_body(area: CollisionObject2D, phase: String = "head") -> void:
    var fresh: bool = active and is_instance_valid(area) and area != caster and not contacted.has(area.get_instance_id())
    var first_strike: bool = fresh and not strike_fired
    super.contact_body(area, phase)
    if first_strike and contacted.has(area.get_instance_id()) and "hit_stop" in config.enabled_layers:
        _strike_stop()
    if fresh and contacted.has(area.get_instance_id()) and config.get("fire_layers", {}).has("contact_light"):
        var light = load("res://scripts/vfx_contact_light.gd").new()
        get_parent().add_child(light)
        light.start(area, global_position, config)
    elif fresh and contacted.has(area.get_instance_id()) and "victim_tint" in config.enabled_layers:
        var victim: CanvasItem = area
        var prop: Node = area.get_parent().get_node_or_null("Prop_" + String(area.name).trim_prefix("VfxTarget_"))
        if prop is CanvasItem:
            victim = prop
        var previous: Color = victim.modulate
        var colour: Array = config.palette_3
        victim.modulate = Color(colour[0], colour[1], colour[2], previous.a)
        var tween: Tween = victim.create_tween()
        tween.set_ignore_time_scale(true)
        tween.tween_property(victim, "modulate", previous, 0.15)

func _strike_stop() -> void:
    # The spec's one contact frame supplies the shared strike hold duration.
    var tree: SceneTree = get_tree()
    var controller: Node = tree.root.get_node_or_null("EffectHitstop")
    if controller == null:
        controller = Node.new()
        controller.name = "EffectHitstop"
        controller.set_meta("baseline", Engine.time_scale)
        controller.set_meta("generation", 0)
        tree.root.add_child(controller)
    var generation: int = int(controller.get_meta("generation")) + 1
    controller.set_meta("generation", generation)
    Engine.time_scale = 0.1
    tree.create_timer(float(config.strike_stop_s), true, false, true).timeout.connect(func():
        if is_instance_valid(controller) and int(controller.get_meta("generation")) == generation:
            Engine.time_scale = float(controller.get_meta("baseline"))
            controller.name = "EffectHitstopDone"
            controller.queue_free())

func _range_fizzle() -> void:
    if is_instance_valid(trail_motes): trail_motes.emitting = false
    active = false
    expired = true
    fizzling = true
    stop_age = age_frames()
    set_deferred("monitoring", false)
    _record("expire")
    events[-1]["range_expiry"] = "fizzle"
    $Head.stop()
    $Head.show()
    $Head.material = load(config.painted_travel.head.fizzle_material).duplicate()
    for node in [$KeyState, $DarkKey, $Streak, $DarkStreak, $DarkHead, $CastHalo, $Trail]: node.hide()
    var rng := RandomNumberGenerator.new()
    rng.seed = int(config.get("seed", 2026))
    for piece in config.get("fizzle_pieces", []):
        var shard := Sprite2D.new()
        shard.texture = load(piece.texture)
        shard.material = load(piece.material).duplicate()
        shard.material.set_shader_parameter("erode", 0.0)
        shard.material.set_shader_parameter("dissolve", 0.0)
        shard.centered = false
        shard.offset = -Vector2(piece.pivot[0], piece.pivot[1])
        shard.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
        shard.set_meta("velocity", Vector2.from_angle(rng.randf_range(0, TAU)) * rng.randf_range(18, 32))
        shard.set_meta("piece_id", piece.id)
        add_child(shard)
        fizzle_shards.append(shard)
    _fizzle_clock(0)

func _fizzle_clock(tick: int) -> void:
    var t: float = clampf(float(tick) / 6.0, 0.0, 1.0)
    $Head.scale = Vector2.ONE * float(config.painted_travel.head.scale) * lerpf(1.0, 0.5, t)
    $Head.material.set_shader_parameter("erode", t)
    $Head.visible = tick < 6
    for shard in fizzle_shards:
        shard.position = shard.get_meta("velocity") * minf(float(tick)/60.0, 0.3)
        shard.modulate.a = maxf(0.0, 1.0-float(tick)/18.0)
        shard.visible = tick < 18
    fizzle_trace.append({"tick":tick,"scale_ratio":lerpf(1.0,0.5,t),"erode":t,
        "head_visible":$Head.visible,"ember_count":fizzle_shards.size() if tick < 18 else 0,
        "key_visible":$KeyState.visible,"position":[global_position.x,global_position.y]})
    if tick >= 18:
        fizzling = false
        for shard in fizzle_shards: shard.queue_free()
        fizzle_shards.clear()
        hide()
        set_physics_process(false)

func _recycle() -> void:
    if is_instance_valid(trail_motes): trail_motes.emitting = false
    active = false
    expired = true
    draining = true
    stop_age = age_frames()
    set_deferred("monitoring", false)
    $Head.stop()
    $Head.hide()
    $DarkHead.hide()
    $KeyState.hide()
    $DarkKey.hide()
    $CastHalo.hide()
    $Trail.clear_points()
    $Trail.hide()
    $Streak.show()
    $DarkStreak.visible = bool(config.dark_duplicate)
    set_physics_process(true)
'''


def _write_painted_g1(out):
    path = out/'scripts/vfx_g1.gd'
    script = path.read_text()
    script = script.replace('and not candidate.active and not candidate.is_queued_for_deletion():',
        'and not candidate.active and not candidate.is_queued_for_deletion() and candidate.scene_file_path == str(kit.get("bolt", "res://scenes/vfx/g1_projectile.tscn")) and candidate.get("draining") != true and candidate.get("fizzling") != true:')
    script = script.replace('load("res://scenes/vfx/g1_projectile.tscn").instantiate()',
        'load(kit.get("bolt", "res://scenes/vfx/g1_projectile.tscn")).instantiate()')
    script = script.replace('if resolved.kind == "prop" and not is_instance_valid(resolved.target)',
        'if not bool(config.get("contact_only", false)) and resolved.kind == "prop" and not is_instance_valid(resolved.target)')
    script = script.replace('if contacted.is_empty() and resolved.kind == "cursor":',
        'if contacted.is_empty() and resolved.kind == "cursor" and not bool(config.get("contact_only", false)):')
    script = script.replace('if contacted.is_empty() and resolved.kind == "prop":',
        'if contacted.is_empty() and resolved.kind == "prop" and not bool(config.get("contact_only", false)):')
    path.write_text(script)
    scene = G1_SCENE.replace('res://scripts/vfx_g1.gd', 'res://scripts/vfx_g1_painted.gd')
    for name in ('Streak', 'KeyState', 'DarkHead', 'DarkStreak', 'DarkKey', 'CastHalo'):
        scene += '\n[node name="'+name+'" type="Sprite2D" parent="."]\ntexture_filter = 2\nvisible = false\n'
        scene += 'z_index = '+str(-2 if name.startswith('Dark') else -1 if name in ('Streak', 'CastHalo') else 0)+'\n'
    (out/'scenes/vfx/g1_painted_projectile.tscn').write_text(scene)
    (out/'scripts/vfx_g1_painted.gd').write_text(PAINTED_G1_SCRIPT)


# T4r: independent ice flight/residue treatment; v1/v2 emitters stay frozen.
ICE_G1_SCRIPT = '''extends "res://scripts/vfx_g1_painted.gd"
func _paint_clock(age: int) -> void:
    super._paint_clock(age)
    $Streak.modulate.a = float(config.painted_travel.streak.alpha)
    $DarkStreak.modulate.a = $Streak.modulate.a
'''

PIECE_BURST_V1R_SCRIPT = '''extends "res://scripts/vfx/piece_burst.gd"
@onready var ground_decal: Sprite2D = $Decal

func _ready() -> void:
    spell_scale = 1.0
    super._ready()
    preload("res://scripts/vfx_ground.gd").attach(ground_decal, self, get_meta("ground_anchor", global_position))
    ground_decal.material = ground_decal.material.duplicate()
    if grey_bodies:
        for band in range(4):
            ground_decal.material.set_shader_parameter("palette_" + str(band), Color(0.5,0.5,0.5,1))

func set_effect_age(age: int) -> void:
    if age == last_age:
        return
    last_age = age
    var flight_start: int = int(config.flash_frames) + int(config.hold_frames)
    var erosion_start: int = flight_start + 15
    var residue_start: int = erosion_start + 21
    var residue_end: int = residue_start + int(config.residue_frames)
    var decal_end: int = residue_end + int(config.decal_frames)
    stage = "onset" if age < int(config.flash_frames) else ("hold" if age < flight_start else ("expansion" if age < erosion_start else ("erosion" if age < residue_start else ("residue" if age < residue_end else ("decal" if age < decal_end else "zero")))))
    var erosion_t: float = clampf(float(age-erosion_start)/21.0,0.0,1.0)
    var residue_t: float = clampf(float(age-residue_start)/float(config.residue_frames),0.0,1.0)
    var dissolve: float = 1.0 if age >= residue_end else 0.8 * residue_t
    # The original peak anchors the eroded residue at the contact origin.
    for name in ["Peak", "PeakDark"]:
        var node: Sprite2D = get_node("Art/"+name)
        node.visible = age >= int(config.flash_frames) and age < residue_end and (name == "Peak" or bool(config.dark_duplicate))
        node.material.set_shader_parameter("erode",float(config.residue_erode)*erosion_t)
        node.material.set_shader_parameter("dissolve",dissolve)
    $Art/Flash.visible = stage == "onset"
    var flash_t: float = float(age)/maxf(1.0,float(config.flash_frames))
    $Art/Flash.scale = Vector2.ONE * lerpf(float(config.flash_from),float(config.flash_to),flash_t)
    $Art/Flash.modulate.a = float(config.flash_alpha)*(1.0-flash_t)
    $Art/Glow.visible = age < flight_start and bool(config.glow_enabled)
    $FloorLight.visible = age < int(config.floor_frames) and bool(config.floor_enabled)
    $FloorLight.modulate.a = maxf(0.0,1.0-float(age)/maxf(1.0,float(config.floor_frames)))
    var flight_t: float = clampf(float(age-flight_start)/15.0,0.0,1.0)
    var states: Array = []
    var count: int = 0
    for data in pieces:
        var item: Dictionary = data.record
        var motion: Dictionary = data.motion
        var node: Sprite2D = data.node
        var active: bool = age >= flight_start and age < residue_start
        var radial: Vector2 = Vector2.RIGHT.rotated(deg_to_rad(float(item.radial_angle_deg)))
        var start: Vector2 = Vector2(item.pivot[0]-config.centre[0],item.pivot[1]-config.centre[1])
        # Same seeded v1 translation/rotation verb, on a 0.25 s radial curve.
        node.position = start + radial*float(config.base_speed_px_s)*float(motion.speed_factor)*0.25*flight_t
        node.rotation = deg_to_rad(float(motion.rotation_deg))*flight_t
        node.scale = Vector2.ONE*(1.0+float(roundi(float(item.final_step)*flight_t))/float(item.native_extent))
        node.visible = active
        node.material.set_shader_parameter("erode",erosion_t)
        node.material.set_shader_parameter("dissolve",0.0)
        if data.dark != null:
            data.dark.transform = node.transform
            data.dark.visible = active
            data.dark.material.set_shader_parameter("erode",erosion_t)
            data.dark.material.set_shader_parameter("dissolve",0.0)
        if active: count += 1
        states.append({"id":item.id,"visible":active,"position":[node.position.x,node.position.y],"rotation_deg":rad_to_deg(node.rotation),"scale":node.scale.x,"erode":erosion_t})
    ground_decal.visible = age >= residue_end and age < decal_end
    ground_decal.modulate.a = clampf(1.0-float(age-residue_end)/float(config.decal_frames),0.0,1.0)
    trace.append({"age_frames":age,"stage":stage,"shard_count":count,"source_piece_count":pieces.size(),"pieces":states,"residue_erode":float(config.residue_erode)*erosion_t,"dissolve":dissolve,"decal_visible":ground_decal.visible,"decal_alpha":ground_decal.modulate.a,"decal_position":[ground_decal.global_position.x,ground_decal.global_position.y],"decal_z_index":ground_decal.z_index})
    if age >= decal_end:
        hide()
        _write_trace()
        queue_free()
'''


def _write_piece_burst_v1r(out, kit, resource_root, prefix):
    """V1 radial flight with v2's whole-peak ragged origin residue and decal."""
    _write_ground_effects(out)
    import copy
    import numpy as np
    from export.effect_kit import (load_pieces, distance_field, residue_entry,
                                   erosion_noise_texture, write_vfx_material, piece_erode_noise)
    data = kit['effect']
    config, record, _ = load_pieces(data['pieces'], kit['root'], runtime=True)
    legacy = dict(kit, effect=copy.deepcopy(data))
    legacy['effect']['pieces']['template'] = 'burst_v1'
    legacy['effect']['material'].pop('erode_noise', None)
    canonical = out/'scenes/vfx/piece_burst.tscn'
    owns_canonical = not canonical.exists()
    _write_piece_burst(out, legacy, resource_root, prefix)
    target = out/f'scenes/{prefix}_impact.tscn'
    scene = target.read_text().replace('res://scripts/vfx/piece_burst.gd','res://scripts/vfx/piece_burst_v1r.gd')
    runtime_path = out/resource_root/'pieces/burst_runtime.json'
    runtime = json.loads(runtime_path.read_text())
    peak_source = kit['root']/Path(config['source']).parent/record['peak_index']
    with Image.open(peak_source) as im: peak = np.asarray(im.convert('RGBA'))
    field = distance_field(peak); noise = piece_erode_noise(data)
    field_rel = resource_root+'/pieces/whole_body_distance.png'
    noise_rel = resource_root+'/pieces/whole_body_noise.png'
    noise_pixels = erosion_noise_texture(peak)
    Image.fromarray(field).save(out/field_rel)
    Image.fromarray(noise_pixels).save(out/noise_rel)
    runtime.update(residue_entry(peak,field,config['residue_fraction'],noise,noise_pixels))
    runtime.update(template='burst_v1r',screen_px=True,erode_outside_in=True,erode_noise=noise,
                   decal_frames=math.ceil(data['decal_s']*60),decal_s=data['decal_s'])
    for name,dark in [('Peak',False),('PeakDark',True)]:
        material = dict(data['material'], erode_outside_in=True, erode_noise=noise,
                        dissolve_order=config.get('dissolve_order', [[3],[2],[1,0]]))
        write_vfx_material(out,resource_root+'/materials/Piece_'+name+'.tres',material,field_rel,dark,noise_rel)
    for item in record['pieces']:
        source = (Path(config['source']).parent/item['mask']).as_posix()
        material = dict(data['material'],erode_outside_in=True,erode_noise=noise,dissolve_order=config.get('dissolve_order', [[3],[2],[1,0]]))
        write_vfx_material(out,resource_root+'/materials/Piece_Piece_%03d.tres'%item['id'],material,
                           resource_root+'/'+data['distance_fields'][source],noise_texture=noise_rel)
    decal = data['layers']['decal']['file']
    decal_material = resource_root+'/materials/FrostDecal.tres'
    material = dict(data['material'],blend_mode='MIX',erode=0.0,dissolve=0.0,erode_outside_in=False)
    material.pop('erode_noise',None)
    write_vfx_material(out,decal_material,material,resource_root+'/'+data['distance_fields'][decal])
    ext = (f'[ext_resource type="Texture2D" path="res://{resource_root}/{decal}" id="FrostTexture"]\n'
           f'[ext_resource type="Material" path="res://{decal_material}" id="FrostMaterial"]\n')
    first = scene.index('[node '); scene=scene[:first]+ext+scene[first:]
    scene += ('\n[node name="Decal" type="Sprite2D" parent="."]\ntexture_filter = 2\nvisible = false\n'
              'position = Vector2(0, 0)\n'
              f'scale = Vector2(1, {data["ground_squash"]})\n'
              'texture = ExtResource("FrostTexture")\nmaterial = ExtResource("FrostMaterial")\n')
    scene = re.sub(r'load_steps=\d+','load_steps='+str(scene.count('[ext_resource ')+1),scene,count=1)
    runtime_path.write_text(json.dumps(runtime,indent=2)+'\n')
    target.write_text(scene)
    if owns_canonical: canonical.write_text(scene)
    if 'orb' not in data or not (out/'scenes/vfx/piece_burst_v1r.tscn').exists():
        (out/'scenes/vfx/piece_burst_v1r.tscn').write_text(scene)
    (out/'scripts/vfx/piece_burst_v1r.gd').write_text(PIECE_BURST_V1R_SCRIPT)


# T4s-r2: top_level severs CanvasItem z inheritance as well as transforms.
GROUND_EFFECTS_SCRIPT = r'''extends RefCounted
static func attach(visual: Node2D, effect: Node2D, point: Vector2) -> void:
    var host: Node = effect.get_parent()
    if host.name == "Actors": host = host.get_parent()
    var layer: Node2D = host.get_node_or_null("GroundEffects")
    if layer == null:
        layer = Node2D.new()
        layer.name = "GroundEffects"
        layer.z_as_relative = false
        layer.y_sort_enabled = true
        var actors: Node2D = host.get_node_or_null("Actors")
        var keeper: Node2D = host.get_node_or_null("Keeper")
        layer.z_index = actors.z_index - 1 if actors != null else (keeper.z_index - 1 if keeper != null else 1)
        host.add_child(layer)
        # Without Actors, share foreground z but precede the Keeper in tree order.
        if keeper != null: host.move_child(layer, keeper.get_index())
    var size: Vector2 = visual.scale
    visual.reparent(layer, false)
    visual.top_level = false
    visual.z_as_relative = true
    visual.z_index = 0
    visual.y_sort_enabled = false
    visual.scale = size
    visual.global_position = point
    # Detached ground art belongs to the effect's lifetime, including cancellation.
    effect.tree_exiting.connect(visual.queue_free, CONNECT_ONE_SHOT)
'''


def _write_ground_effects(out):
    (out/'scripts/vfx_ground.gd').write_text(GROUND_EFFECTS_SCRIPT)


# T4s. G2 emission is opt-in, leaving the eleven-kit G1 export untouched.
def _g2_config(kit, ground_geometry=None):
    from export.effect_kit import tick_schedule_report
    d=kit['effect']; spec=d['skill_spec']; m=spec['mechanics']; g=d['g2']; root='res://vfx/'+kit['name']+'/'
    return dict(name=kit['name'],grammar='G2',screen_px=True,flare=root+'flare.tres',
                bolt='res://scenes/vfx/g2_thrown_field.tscn',range_px=m['range_px'],
                apex_px=m['arc']['apex_px'],flight_s=m['arc']['flight_s'],radius_px=m['field']['radius_px'],
                duration_s=m['field']['duration_s'],ticks=m['field']['tick_schedule_s'],
                schedule=tick_schedule_report(m['field']['tick_schedule_s'],m['field'].get('tick_cv_min',.25)),
                residue_s=spec['presentation']['phase_envelope_s']['residue'],ground_squash=d['ground_squash'],
                roil_uv_per_s=g.get('roil_uv_per_s',0.),dark_offset_px=g.get('dark_offset_px',0.),dark_alpha=g.get('dark_alpha',.25),field_erode=d['material'].get('erode',0.),
                flask=root+g['flask'],field=root+'derived/field.png',pulse=root+g['pulse'],
                fragments=[root+'derived/glass_'+str(i)+'.png' for i in range(3)],
                material=root+'materials/Field.tres',pulse_material=root+'materials/Pulse.tres',
                decal_material=root+'materials/Decal.tres',additive_material=root+'materials/Halo.tres',
                dark_material=root+'materials/Dark.tres',palette_3=d['material']['palette'][3],
                treatment=d['element'],density=d.get('density',1.),seed=g['seed'],
                field_binding=g.get('field_binding', {}),
                lick_anchors=_g2_lick_anchors(kit) if g.get('field_binding') else [],
                walkable=(ground_geometry or {}).get('walkable', []),
                blocked=(ground_geometry or {}).get('blocked', []),
                px_per_bh=spec.get('scale', {}).get('px_per_bh', 130),
                launch_angle_deg=m['arc'].get('launch_angle_deg', 18.0),
                lick_flicker_hz=spec['presentation'].get('lick_flicker_hz', []),
                lick_coherence=spec['presentation'].get('lick_coherence', ''),
                residue_diameter_px=spec['presentation']['body_extents_bh'].get('residue_diameter', 0)*spec.get('scale', {}).get('px_per_bh', 130),
                residue_fade_in_s=.1 if d['element']=='fire' else 0.,
                residue_fade_out_s=min(1.,spec['presentation']['phase_envelope_s']['residue']) if d['element']=='fire' else spec['presentation']['phase_envelope_s']['residue'],
                flask_width=spec['presentation']['body_extents_bh']['flask']*130,
                splash=('res://scenes/vfx_'+g['splash']['kit']+'_impact.tscn' if d['element']=='fire' else ''),
                splash_scale=g['splash'].get('scale',1),enabled_layers=spec['presentation']['enabled_layers'])


def _g2_lick_anchors(kit):
    """Three deterministic samples ON the largest painted plane-3 tongues."""
    import numpy as np
    from scipy.ndimage import label
    with Image.open(kit['root']/kit['effect']['g2']['field_source']) as image:
        rgba = np.asarray(image.convert('RGBA'))
    mask = (rgba[...,0] == 255) & (rgba[...,3] > 0)
    labels, count = label(mask)
    groups = sorted(range(1, count+1), key=lambda i: (-int(np.count_nonzero(labels == i)), i))[:3]
    if len(groups) < 3:
        raise ValueError('painted_pool requires three plane-3 flame tongues')
    anchors = []
    for group in groups:
        points = np.argwhere(labels == group)
        point = points[np.argmin(np.sum((points-points.mean(axis=0))**2, axis=1))]
        anchors.append([int(point[1]), int(point[0])])
    return anchors


def _write_g2_kit(out, kit):
    import numpy as np
    from export.effect_kit import distance_field, write_vfx_material, erosion_noise_texture
    d=kit['effect']; root='vfx/'+kit['name']; dest=out/root
    dest.mkdir(parents=True,exist_ok=True)
    for path in kit['root'].rglob('*'):
        if path.is_file():
            target=dest/path.relative_to(kit['root']);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
    for phase,folder in [('cast','flare'),('travel','travel'),('impact','impact')]:
        frames=d['phases'][phase]['frames']
        write_spriteframes(out,root+'/'+folder+'.tres',{folder:([root+'/'+f['file'] for f in frames],1,False)},
                           {folder:[f['hold_frames']/60 for f in frames]})
    derived=dest/'derived';derived.mkdir(exist_ok=True)
    with Image.open(dest/d['g2']['flask']) as im: flask=np.asarray(im.convert('RGBA')).copy()
    ys,xs=np.nonzero(flask[...,3]);cx,cy=xs.mean(),ys.mean(); y,x=np.indices(flask.shape[:2]);
    sectors=np.floor(((np.arctan2(y-cy,x-cx)+2*np.pi)%(2*np.pi))/(2*np.pi/3)).astype(int)
    for i in range(3):
        shard=flask.copy();shard[...,3]=np.where(sectors==i,shard[...,3],0);Image.fromarray(shard).save(derived/f'glass_{i}.png')
    # Painted fire pool stays native; poison uses the supplied density puff.
    # Poison source is the supplied lobed density puff. No new drawing.
    with Image.open(dest/d['g2']['field_source']) as im: field=np.asarray(im.convert('RGBA'))
    Image.fromarray(field).save(derived/'field.png')
    Image.fromarray(distance_field(field)).save(derived/'field_distance.png')
    with Image.open(dest/d['g2']['pulse']) as im: pulse=np.asarray(im.convert('RGBA'))
    Image.fromarray(distance_field(pulse)).save(derived/'pulse_distance.png')
    mat=dict(d['material'],blend_mode='MIX',erode_outside_in=True,erode=0.,dissolve=0.)
    mat.pop('erode_noise',None)
    for label,source,mode,dark in [('Field','field','MIX',False),('Pulse','pulse','MIX',False),('Halo','field','ADD',False),('Additive','pulse','ADD',False),('Dark','field','MIX',True),('Decal','field','MIX',False)]:
        material=dict(mat,blend_mode=mode)
        if label=='Decal':
            material['palette']=([[.065,.035,.025,.55]]*4 if d['element']=='fire' else [[.035,.12,.055,.55]]*4)
        noise_rel=None
        if d['g2'].get('roil_uv_per_s') and label in ('Field','Dark'):
            noise_rel=root+'/derived/field_noise.png'
            Image.fromarray(erosion_noise_texture(field)).save(out/noise_rel)
            material.update(erode_noise=d['material']['erode_noise'],erode=d['material']['erode'])
        write_vfx_material(out,root+'/materials/'+label+'.tres',material,root+'/derived/'+source+'_distance.png',dark,noise_rel)
        if noise_rel:
            # A private shader variant adds drift without changing any other kit.
            material_path=out/root/'materials'/f'{label}.tres'
            text=material_path.read_text()
            shader_path=re.search(r'path="res://([^"]+\.gdshader)"',text).group(1)
            original=out/shader_path; drift=original.with_name(original.stem+'_roil.gdshader')
            source_text=original.read_text().replace('void fragment()', 'uniform vec2 noise_uv_offset = vec2(0.0);\nvoid fragment()').replace('texture(erosion_noise_texture, UV)', 'texture(erosion_noise_texture, UV + noise_uv_offset)')
            drift.write_text(source_text)
            material_path.write_text(text.replace(shader_path,drift.relative_to(out).as_posix()))
    # Flare material is required by the existing CAST frame plumbing.
    write_vfx_material(out,root+'/materials/Body.tres',mat,root+'/derived/pulse_distance.png')
    from export.effect_kit import MATERIAL_BINDING_SCRIPT
    (out/f'scripts/vfx_{kit["name"]}_material.gd').write_text('extends RefCounted\n'+MATERIAL_BINDING_SCRIPT)
    return {'grammar':'G2','frames':sum(len(p['frames']) for p in d['phases'].values())}


def _write_g2_component(out):
    _write_ground_effects(out)
    (out/'scripts/vfx_g2.gd').write_text(G2_SCRIPT)
    scene='[gd_scene load_steps=2 format=3]\n[ext_resource type="Script" path="res://scripts/vfx_g2.gd" id="G2"]\n[node name="G2ThrownField" type="Node2D"]\nscript = ExtResource("G2")\ntexture_filter = 2\nz_as_relative = false\nz_index = 2\n'
    for name,kind,parent in [('Flask','Sprite2D','.'),('Fragments','Node2D','.'),('Splash','Node2D','.'),('Ground','Node2D','.'),('Decal','Sprite2D','Ground'),('FloorLight','Sprite2D','Ground'),('Halo','Sprite2D','Ground'),('DarkDuplicate','Sprite2D','Ground'),('Field','Sprite2D','Ground'),('Licks','Node2D','Ground'),('Lobes','Node2D','Ground'),('Flash','Sprite2D','Ground')]:
        scene+='\n[node name="'+name+'" type="'+kind+'" parent="'+parent+'"]\ntexture_filter = 2\n'
        # Ground children share one z and draw in material order; the group sorts at its landing point.
    (out/'scenes/vfx/g2_thrown_field.tscn').write_text(scene)


G2_SCRIPT = r'''extends Node2D
# One effect-age frame clock; target policy uses a ground point, never props.
static var events: Array = []
static var label_events: Array = []
static var next_id: int = 0
var effect_id: int = 0
var config: Dictionary = {}
var cast_origin: Vector2
var ground_point: Vector2
var release_tick: int
var caster: Node2D
var active: bool = false
var landed: bool = false
var field_ended: bool = false
var tick_index: int = 0
var last_tick: int = -100
var labelled: Dictionary = {}
var tinted: Array = []
var trace: Array = []
var rng := RandomNumberGenerator.new()
var field_scale: float = 1.0
var pulse_scale: float = 1.0
var flask_scale: float = 1.0
var field_pivot: Vector2
var walkable_polygons: Array[PackedVector2Array] = []
var blocked_polygons: Array[PackedVector2Array] = []
var lick_rngs: Array = []
var lick_states: Array = []

static func packed_polygons(polygons: Array) -> Array[PackedVector2Array]:
    var result: Array[PackedVector2Array] = []
    for polygon in polygons:
        var packed := PackedVector2Array()
        for point in polygon: packed.append(Vector2(point[0],point[1]))
        result.append(packed)
    return result

static func is_walkable(point: Vector2, walkable: Array[PackedVector2Array], blocked: Array[PackedVector2Array]) -> bool:
    for polygon in blocked:
        if Geometry2D.is_point_in_polygon(point,polygon): return false
    for polygon in walkable:
        if Geometry2D.is_point_in_polygon(point,polygon): return true
    return false

static func landing_point(origin: Vector2, direction: Vector2, distance: float, bh: float, walkable: Array[PackedVector2Array], blocked: Array[PackedVector2Array]) -> Dictionary:
    var axis: Vector2 = direction.normalized()
    var fallback: Vector2 = origin+axis*bh
    if not is_walkable(origin,walkable,blocked):
        return {"point":fallback,"reason":"release_not_walkable"}
    var chosen: Vector2 = fallback
    var found: bool = false
    # Include the minimum and exact endpoint in addition to the 8-px lattice.
    var samples: Array[float] = [bh]
    for step in range(0,int(floor(distance/8.0))+1):
        if float(step)*8.0>=bh: samples.append(float(step)*8.0)
    if distance>=bh: samples.append(distance)
    for d in samples:
        var point: Vector2 = origin+axis*d
        # Vector2 uses float32: round the minimum outward, never below 1 BH.
        if d==bh and origin.distance_to(point)<bh:
            point=origin+axis*(bh+.001)
        if is_walkable(point,walkable,blocked):
            chosen=point
            found=true
    return {"point":chosen,"reason":"last_walkable" if found else "no_walkable_at_minimum"}

func _lick_sample(index: int, frame: int) -> Vector2:
    var state: Dictionary = lick_states[index]
    var noise: RandomNumberGenerator = lick_rngs[index]
    # Damped narrow-band stochastic oscillator, independently seeded per lick.
    # White excitation keeps coherence low; damage ticks never enter this clock.
    while int(state.frame)<frame:
        var white: float = noise.randf_range(-1.0,1.0)
        var value: float = 2.0*.94*cos(TAU*float(state.hz)/60.0)*float(state.y)-.94*.94*float(state.previous)+white
        state.previous=state.y
        state.y=value
        state.frame+=1
        state.scale=1.0+.18*tanh(value*.28)
        state.alpha=.70+.24*tanh((value+white)*.28)
    return Vector2(state.scale,state.alpha)
@onready var ground_visual: Node2D = $Ground

static func resolve_ground(origin: Vector2, facing: Vector2, cursor: Vector2, range_px: float, touch: bool) -> Dictionary:
    if not origin.is_finite() or not facing.is_finite() or not cursor.is_finite() or facing.is_zero_approx() or not is_finite(range_px) or range_px <= 0.0:
        return {}
    var offset: Vector2 = facing.normalized()*range_px if touch else (cursor-origin).limit_length(range_px)
    return {"point":origin+offset,"kind":"ground","target":null,"facing":facing.normalized(),"touch":touch}

static func acquire(parent: Node2D, kit: Dictionary, origin: Vector2, destination: Dictionary, owner_node: Node2D = null, _art_scale: float = 1.0) -> Node2D:
    if kit.get("grammar","") != "G2" or destination.get("kind","") != "ground" or not destination.get("point") is Vector2 or not origin.is_finite() or not destination.point.is_finite():
        return null
    var effect: Node2D = load("res://scenes/vfx/g2_thrown_field.tscn").instantiate()
    parent.add_child(effect)
    effect.release(kit,origin,destination,owner_node)
    return effect

func _ready() -> void:
    set_physics_process(false)

func age_frames() -> int:
    return roundi(float(Engine.get_physics_frames()-release_tick)*60.0/Engine.physics_ticks_per_second)

func _record(event: String, fields: Dictionary = {}) -> void:
    var item: Dictionary = {"event":event,"effect_id":effect_id,"kit":config.name,"age_frames":age_frames(),"target_kind":"ground","target_point":[ground_point.x,ground_point.y]}
    item.merge(fields)
    events.append(item)

func _sprite(node: Sprite2D, path: String, material: String = "") -> void:
    node.texture = load(path)
    node.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
    node.material = load(material).duplicate() if material != "" else null
    node.centered = false
    var box: Rect2i = node.texture.get_image().get_used_rect()
    node.offset = -(Vector2(box.position)+Vector2(box.size)*0.5)

func release(kit: Dictionary, origin: Vector2, destination: Dictionary, owner_node: Node2D = null) -> void:
    config = kit.duplicate(true)
    caster = owner_node
    cast_origin = origin
    ground_point = destination.point
    var landing_reason: String = "unbounded_scene"
    if not config.walkable.is_empty():
        walkable_polygons=packed_polygons(config.walkable)
        blocked_polygons=packed_polygons(config.blocked)
        var direction: Vector2 = destination.get("facing",origin.direction_to(ground_point)) if destination.get("touch",false) else origin.direction_to(ground_point)
        var distance: float = float(config.range_px) if destination.get("touch",false) else minf(origin.distance_to(ground_point),float(config.range_px))
        var resolved: Dictionary = landing_point(origin,direction,distance,float(config.px_per_bh),walkable_polygons,blocked_polygons)
        ground_point=resolved.point
        landing_reason=resolved.reason
        if landing_reason=="no_walkable_at_minimum":
            # No point can satisfy both walkability and the 1-BH minimum.
            # Cancel instead of creating a field on a known non-walkable point.
            next_id+=1
            effect_id=next_id
            release_tick=Engine.get_physics_frames()
            _record("cancel",{"reason":landing_reason})
            queue_free()
            return
        var actual_distance: float = origin.distance_to(ground_point)
        config.flight_s=actual_distance/(float(kit.range_px)/float(kit.flight_s))
        config.apex_px=actual_distance*tan(deg_to_rad(float(config.launch_angle_deg)))/4.0
    top_level = true
    global_transform = Transform2D(0.0,origin)
    preload("res://scripts/vfx_ground.gd").attach(ground_visual, self, ground_point)
    next_id += 1
    effect_id = next_id
    release_tick = Engine.get_physics_frames()
    rng.seed = int(config.seed)
    _sprite($Flask,config.flask)
    # CanvasItemMaterial MIX/NORMAL preserves RGB dark glass and its coverage.
    var glass := CanvasItemMaterial.new()
    glass.blend_mode = CanvasItemMaterial.BLEND_MODE_MIX
    glass.light_mode = CanvasItemMaterial.LIGHT_MODE_NORMAL
    $Flask.material = glass
    flask_scale = float(config.flask_width)/$Flask.texture.get_image().get_used_rect().size.x
    $Flask.scale = Vector2.ONE*flask_scale
    # Both flasks share the same absolute flight layer, independent of parent Y sort.
    $Flask.z_as_relative = false
    $Flask.z_index = 3
    $Flask.modulate = Color.WHITE
    _sprite(ground_visual.get_node("Field"),config.field,config.material)
    var painted: bool = not config.field_binding.is_empty()
    field_scale = 2.0*float(config.radius_px)/ground_visual.get_node("Field").texture.get_image().get_used_rect().size.x
    _sprite(ground_visual.get_node("Decal"),config.field,config.decal_material)
    _sprite(ground_visual.get_node("Halo"),config.field,config.additive_material)
    _sprite(ground_visual.get_node("FloorLight"),config.field,config.additive_material)
    _sprite(ground_visual.get_node("Flash"),config.field,config.additive_material)
    _sprite(ground_visual.get_node("DarkDuplicate"),config.field,config.dark_material)
    for node in [ground_visual.get_node("Field"),ground_visual.get_node("Decal"),ground_visual.get_node("Halo"),ground_visual.get_node("FloorLight"),ground_visual.get_node("Flash"),ground_visual.get_node("DarkDuplicate")]:
        node.scale = Vector2.ONE*field_scale if painted else Vector2(1.0,float(config.ground_squash))*field_scale
        if painted:
            node.offset = -Vector2(config.field_binding.pivot[0],config.field_binding.pivot[1])
    if float(config.residue_diameter_px)>0:
        ground_visual.get_node("Decal").scale=Vector2.ONE*float(config.residue_diameter_px)/ground_visual.get_node("Decal").texture.get_image().get_used_rect().size.x
    for i in range(3):
        var shard := Sprite2D.new()
        $Fragments.add_child(shard)
        _sprite(shard,config.fragments[i])
        shard.material = glass
        shard.scale = Vector2.ONE*flask_scale
        shard.hide()
        shard.set_meta("angle",TAU*float(i)/3.0+0.2)
        shard.set_meta("velocity",rng.randf_range(65,110))
    var pulse: Texture2D = load(config.pulse)
    pulse_scale = 65.0/pulse.get_image().get_used_rect().size.x
    for i in range(3 if config.treatment=="fire" else 4):
        var lobe := Sprite2D.new()
        (ground_visual.get_node("Licks") if config.treatment=="fire" else ground_visual.get_node("Lobes")).add_child(lobe)
        lobe.name = ("Lick" if config.treatment=="fire" else "Lobe")+str(i)
        _sprite(lobe,config.pulse,config.pulse_material)
        lobe.scale = Vector2.ONE*pulse_scale
        if painted:
            var anchor: Array = config.lick_anchors[i]
            lobe.set_meta("anchor",Vector2(anchor[0],anchor[1])-Vector2(config.field_binding.pivot[0],config.field_binding.pivot[1]))
            lobe.rotation = -PI/2.0
        if not config.lick_flicker_hz.is_empty():
            var local_rng := RandomNumberGenerator.new()
            local_rng.seed=int(config.seed)+7919*(i+1)
            lick_rngs.append(local_rng)
            lick_states.append({"frame":-1,"y":0.0,"previous":0.0,"scale":1.0,"alpha":.7,"hz":local_rng.randf_range(float(config.lick_flicker_hz[0]),float(config.lick_flicker_hz[1]))})
        lobe.hide()
        lobe.set_meta("angle",TAU*float(i)/4.0)
        lobe.set_meta("velocity",rng.randf_range(60,110))
    ground_visual.hide()
    active = true
    _record("release",{"schedule":config.schedule,"origin":[origin.x,origin.y],"distance_px":origin.distance_to(ground_point),"flight_s":config.flight_s,"apex_px":config.apex_px,"landing_reason":landing_reason,"walkable":is_walkable(ground_point,walkable_polygons,blocked_polygons) if not walkable_polygons.is_empty() else null})
    if not bool(config.schedule.ff08_satisfied):
        _record("constraint_unhonoured",{"constraint":"FF-08","interval_cv":config.schedule.interval_cv,"minimum":config.schedule.minimum_cv})
    set_physics_process(true)
    _clock(0)

func _physics_process(_delta: float) -> void:
    if active: _clock(age_frames())

func _clock(age: int) -> void:
    var flight: int = ceili(float(config.flight_s)*60.0)
    var land_age: int = age-flight
    var end_field: int = ceili(float(config.duration_s)*60.0)
    var residue_frames: int = ceili(float(config.residue_s)*60.0)
    var t: float = clampf(float(age)/flight,0.0,1.0)
    var lift: float = 4.0*float(config.apex_px)*t*(1.0-t)
    $Flask.global_position = cast_origin.lerp(ground_point,t)+Vector2(0,-lift)
    $Flask.rotation = deg_to_rad(15.0)*sin(t*TAU)
    $Flask.visible = land_age<=0
    if land_age>=0 and not landed:
        landed = true
        ground_visual.show()
        _record("contact",{"collision_age_frames":age,"contact_lag_frames":0,"phase":"ground","contact_frames":1})
        _record("field_start")
        if config.treatment=="fire":
            var splash: Node2D = load(config.splash).instantiate()
            splash.set_meta("strike_response",true)
            splash.set("spell_scale",1.0)
            splash.set("caster",caster)
            $Splash.add_child(splash)
            splash.global_position = ground_point
            var art: Node2D = splash.get_node_or_null("Art")
            if art != null: art.scale *= float(config.splash_scale)
        _strike_stop()
    var field_live: bool = land_age>=0 and land_age<end_field
    if field_live:
        while tick_index<config.ticks.size() and land_age>=roundi(float(config.ticks[tick_index])*60.0):
            last_tick = roundi(float(config.ticks[tick_index])*60.0)
            _tick(tick_index,last_tick)
            tick_index += 1
    if land_age>=end_field and not field_ended:
        field_ended = true
        _record("field_end",{"duration_frames":end_field,"tick_count":tick_index,"licks":ground_visual.get_node("Licks").get_children().map(func(n):return {"scale":n.scale.x/pulse_scale,"alpha":n.modulate.a,"visible":n.visible})})
        _record("decal_start")
    for shard in $Fragments.get_children():
        shard.visible = land_age>0 and land_age<=12
        var st: float = clampf(float(land_age-1)/12.0,0.0,1.0)
        var axis := Vector2.from_angle(float(shard.get_meta("angle")))
        shard.global_position = ground_point + axis*float(shard.get_meta("velocity"))*st*.2*Vector2(1,.58)+Vector2(0,-12.0*4.0*st*(1.0-st))
        shard.rotation = axis.angle()*st*.15
        shard.modulate.a = 1.0-st
    if config.treatment=="poison":
        for lobe in ground_visual.get_node("Lobes").get_children():
            lobe.visible = land_age>=0 and land_age<15
            var st: float = clampf(float(land_age)/15.0,0,1)
            var axis := Vector2.from_angle(float(lobe.get_meta("angle")))
            lobe.global_position = ground_point+axis*float(lobe.get_meta("velocity"))*st*.25*Vector2(1,.58)+Vector2(0,-12.0*sin(PI*st))
            lobe.rotation = axis.angle()+deg_to_rad(20.0)*st
            # Keep all four planes readable throughout the short translating splash.
            lobe.material.set_shader_parameter("erode",0.0)
            lobe.modulate.a = clampf(float(15-land_age)/3.0,0,1)
    ground_visual.get_node("Field").visible = field_live
    var coverage: float = lerpf(.5,1.0,clampf(float(land_age)/24.0,0,1)) if config.treatment=="poison" else 1.0
    # Coverage is area: sqrt growth on each axis; density exclusively multiplies alpha.
    var painted: bool = not config.field_binding.is_empty()
    ground_visual.get_node("Field").scale = Vector2.ONE*field_scale if painted else Vector2(1,float(config.ground_squash))*field_scale*sqrt(coverage)
    # Multiplicative breath: authored density bounds the translucent cloud.
    var next_tick: int = roundi(float(config.ticks[tick_index])*60.0) if tick_index<config.ticks.size() else end_field
    var phase: float = clampf(float(land_age-last_tick)/maxi(1,next_tick-last_tick),0,1)
    var wave: float = sin(TAU*phase)
    var breathe: float = 1.0+wave*(.05 if wave>=0 else .10)/.75 if config.treatment=="poison" and field_live else 1.0
    var dissolve: float = 0.0
    if painted and land_age>=end_field-24:
        var fade_age: int = land_age-(end_field-24)
        # Drop 3, then 2, and finally 1+0 at release; no alpha wash to cream.
        dissolve = .5 if fade_age<8 else (.7 if fade_age<24 else 1.0)
    ground_visual.get_node("Field").material.set_shader_parameter("dissolve",dissolve)
    ground_visual.get_node("Field").modulate.a = float(config.density)*breathe
    for name in ["Field","DarkDuplicate"]:
        ground_visual.get_node(name).material.set_shader_parameter("erode",float(config.field_erode))
        if float(config.roil_uv_per_s)>0:
            ground_visual.get_node(name).material.set_shader_parameter("noise_uv_offset",Vector2(float(maxi(0,land_age))/60.0*float(config.roil_uv_per_s),0))
    ground_visual.get_node("Field").position = Vector2(float(maxi(0,land_age))/60.0*2.0,0) if config.treatment=="poison" else Vector2.ZERO
    for i in range(ground_visual.get_node("Licks").get_child_count()):
        var lick: Sprite2D = ground_visual.get_node("Licks").get_child(i)
        var pulse_age: int = land_age-last_tick
        lick.visible = field_live and pulse_age>=0 and pulse_age<6
        var axis := Vector2.from_angle(float(lick.get_meta("angle")))
        lick.position = lick.get_meta("anchor")*field_scale if painted else axis*float(config.radius_px)*.35*Vector2(1,.58)
        lick.rotation = -PI/2.0 if painted else axis.angle()
        if painted and land_age>=end_field-24: lick.hide()
        lick.material.set_shader_parameter("erode",clampf(float(pulse_age)/5.0,0,1))
        if not config.lick_flicker_hz.is_empty():
            var sample: Vector2 = _lick_sample(i,maxi(0,land_age))
            lick.visible=field_live and land_age<end_field-24
            lick.scale=Vector2.ONE*pulse_scale*sample.x
            lick.modulate.a=sample.y
            lick.material.set_shader_parameter("erode",0.0)
    ground_visual.get_node("Decal").visible = land_age>=end_field and land_age<end_field+residue_frames
    ground_visual.get_node("Decal").modulate.a = minf(clampf(float(land_age-end_field)/maxf(1.0,float(config.residue_fade_in_s)*60.0),0,1) if float(config.residue_fade_in_s)>0 else 1.0,clampf(float(end_field+residue_frames-land_age)/maxf(1.0,float(config.residue_fade_out_s)*60.0),0,1))
    ground_visual.get_node("Halo").visible = field_live and config.treatment=="fire" and "halo" in config.enabled_layers
    ground_visual.get_node("Halo").modulate.a = .12
    ground_visual.get_node("DarkDuplicate").visible = field_live and "dark_duplicate" in config.enabled_layers
    ground_visual.get_node("DarkDuplicate").scale = ground_visual.get_node("Field").scale
    ground_visual.get_node("DarkDuplicate").position = ground_visual.get_node("Field").position+Vector2(0,float(config.dark_offset_px))
    ground_visual.get_node("DarkDuplicate").modulate.a = float(config.density)*breathe*float(config.dark_alpha)
    ground_visual.get_node("FloorLight").visible = field_live and config.treatment=="fire" and "floor_light" in config.enabled_layers
    ground_visual.get_node("FloorLight").modulate.a = .15
    for name in ["Halo","FloorLight","DarkDuplicate"]:
        ground_visual.get_node(name).material.set_shader_parameter("dissolve",dissolve)
    ground_visual.get_node("Flash").visible = land_age==0 and "flash" in config.enabled_layers
    ground_visual.get_node("Flash").modulate.a = .8
    _tint_clock(age)
    trace.append({"age_frames":age,"lift_px":lift,"flask_position":[$Flask.global_position.x,$Flask.global_position.y],"rotation_deg":rad_to_deg($Flask.rotation),"contact":land_age==0,"fragments":$Fragments.get_children().filter(func(n):return n.visible).size(),"field_alive":field_live,"coverage":coverage,"density":config.density,"field_alpha":ground_visual.get_node("Field").modulate.a,"field_erode":ground_visual.get_node("Field").material.get_shader_parameter("erode"),"dark_offset_px":config.dark_offset_px,"drift_px":ground_visual.get_node("Field").position.x,"ground_point":[ground_visual.global_position.x,ground_visual.global_position.y],"ground_z":ground_visual.z_index,"decal_visible":ground_visual.get_node("Decal").visible,"decal_alpha":ground_visual.get_node("Decal").modulate.a,"tick_count":tick_index,"licks":ground_visual.get_node("Licks").get_children().map(func(n):return {"scale":n.scale.x/pulse_scale,"alpha":n.modulate.a,"visible":n.visible})})
    if land_age>=end_field+residue_frames:
        _record("expire")
        active = false
        hide()
        ground_visual.hide()
        set_physics_process(false)
        _restore_tints()
        queue_free()

func _tick(index: int, scheduled: int) -> void:
    _record("tick",{"tick_index":index,"scheduled_field_age_frames":scheduled})
    if config.field_binding.is_empty():
        for lick in ground_visual.get_node("Licks").get_children(): lick.set_meta("angle",rng.randf_range(0,TAU))
    var actors: Array = get_tree().get_nodes_in_group("vfx_targets")
    for actor in get_tree().get_nodes_in_group("vfx_actors"):
        if actor not in actors: actors.append(actor)
    for actor in actors:
        if not is_instance_valid(actor) or not actor is Node2D or actor==caster or actor.global_position.distance_to(ground_point)>float(config.radius_px): continue
        var body_index: int = int(actor.get_meta("body_index",get_tree().get_nodes_in_group("vfx_targets").find(actor) if actor.is_in_group("vfx_targets") else actors.find(actor)))
        var contact_class: String = "primary" if actor.global_position.distance_to(ground_point)<=4.0 else "secondary"
        _record("contact",{"body_index":body_index,"contact_class":contact_class,"phase":"field_centre" if contact_class=="primary" else "rim","tick_index":index,"collision_age_frames":age_frames(),"contact_lag_frames":0})
        if "victim_tint" in config.enabled_layers:
            var victim: CanvasItem = actor
            var prop: Node = actor.get_parent().get_node_or_null("Prop_"+String(actor.name).trim_prefix("VfxTarget_"))
            if prop is CanvasItem: victim=prop
            var original: Color = victim.modulate
            for entry in tinted:
                if entry.node==victim: original=entry.original
            tinted = tinted.filter(func(entry):return entry.node!=victim)
            tinted.append({"node":victim,"original":original,"end":age_frames()+9})
            var c: Array = config.palette_3
            victim.modulate = Color(c[0],c[1],c[2],original.a)
            _record("victim_tint",{"body_index":body_index,"tick_index":index})
        if "contact_label" in config.enabled_layers and not labelled.has(actor.get_instance_id()):
            labelled[actor.get_instance_id()]=true
            _record("contact_label",{"body_index":body_index,"tick_index":index,"contact_class":contact_class})
            var label: Label = null
            for candidate in get_tree().get_nodes_in_group("vfx_contact_labels"):
                if not candidate.visible:
                    label=candidate
                    break
            if label==null:
                label=Label.new()
                label.set_script(load("res://scripts/vfx_contact_label.gd"))
                get_parent().add_child(label)
            label.top_level=true
            label.scale=Vector2.ONE
            label.rotation=0.0
            var c: Array = config.palette_3
            label.show_contact(actor.global_position+Vector2(0,-70),"FULL" if contact_class=="primary" else "PARTIAL",Color(c[0],c[1],c[2],c[3]),effect_id,body_index,label_events)

func _tint_clock(age: int) -> void:
    for entry in tinted:
        if is_instance_valid(entry.node) and age>=int(entry.end): entry.node.modulate=entry.original
    tinted=tinted.filter(func(entry):return is_instance_valid(entry.node) and age<int(entry.end))

func _restore_tints() -> void:
    for entry in tinted:
        if is_instance_valid(entry.node): entry.node.modulate=entry.original
    tinted.clear()

func _strike_stop() -> void:
    if "hit_stop" not in config.enabled_layers: return
    var tree: SceneTree = get_tree()
    var controller: Node = tree.root.get_node_or_null("EffectHitstop")
    if controller == null:
        controller=Node.new()
        controller.name="EffectHitstop"
        controller.set_meta("baseline",Engine.time_scale)
        controller.set_meta("generation",0)
        tree.root.add_child(controller)
    var generation: int = int(controller.get_meta("generation"))+1
    controller.set_meta("generation",generation)
    Engine.time_scale=.1
    tree.create_timer(1.0/60.0,true,false,true).timeout.connect(func():
        if is_instance_valid(controller) and int(controller.get_meta("generation"))==generation:
            Engine.time_scale=float(controller.get_meta("baseline"))
            controller.name="EffectHitstopDone"
            controller.queue_free())

func cancel() -> void:
    if not active: return
    _record("cancel")
    _restore_tints()
    active=false
    queue_free()
'''


# T4t: opt-in G3 export leaves all existing G1/G2 resources byte-identical.
def _g3_config(kit):
    from export.effect_kit import chain_schedule_report
    import numpy as np
    d=kit['effect'];g=d['g3'];m=d['skill_spec']['mechanics'];root='res://vfx/'+kit['name']+'/'
    schedule=chain_schedule_report(m['chain'])
    with Image.open(kit['root']/g['link']['png']) as image: a=np.asarray(image)
    y,x=np.nonzero(a[...,3]);height=int(y.max()-y.min()+1)
    scale=m['width_px']/g['link']['coverage_width']
    primitives={role:dict(g[role],png=root+g[role]['png'],material=root+'materials/'+role.title()+'.tres') for role in ('link','branch','prong')}
    return dict(name=kit['name'],grammar='G3',screen_px=True,flare=root+'flare.tres',bolt='res://scenes/vfx/g3_bolt_chain.tscn',
                range_px=m['range_px'],hop_range_px=m['chain']['hop_range_px'],delays=schedule['delays_s'],cumulative=schedule['cumulative_s'],schedule=schedule,
                primitives=primitives,link_scale=scale,link_length_px=math.dist(g['link']['start'],g['link']['end'])*scale,
                width_px=m['width_px'],width_multiplier=g['width_multiplier'],prong_length_px=d['skill_spec']['presentation']['body_extents_bh'].get('end_prongs',.6)*130,
                max_branches=g['max_branches'],prongs=g['prongs'],min_links=g['min_links'],max_links=g['max_links'],segment_fraction=g['segment_fraction'],jitter_px=g['jitter_px'],
                seed=g['seed'],life_s=g['life_s'],afterimage_s=g['afterimage_s'],palette_3=d['material']['palette'][3],
                enabled_layers=d['skill_spec']['presentation']['enabled_layers'])


def _write_g3_kit(out, kit):
    import numpy as np
    from export.effect_kit import distance_field,write_vfx_material,MATERIAL_BINDING_SCRIPT
    d=kit['effect'];root='vfx/'+kit['name'];dest=out/root
    for path in kit['root'].rglob('*'):
        if path.is_file():
            target=dest/path.relative_to(kit['root']);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
    for phase,folder in [('cast','flare'),('travel','travel'),('impact','impact')]:
        frames=d['phases'][phase]['frames']
        write_spriteframes(out,root+'/'+folder+'.tres',{folder:([root+'/'+f['file'] for f in frames],1,False)},
                           {folder:[f['hold_frames']/60 for f in frames]})
    (dest/'distance').mkdir(exist_ok=True)
    for role in ('link','branch','prong'):
        with Image.open(dest/d['g3'][role]['png']) as image: a=np.asarray(image)
        field=root+'/distance/'+role+'.png';Image.fromarray(distance_field(a)).save(out/field)
        write_vfx_material(out,root+'/materials/'+role.title()+'.tres',d['material'],field)
    write_vfx_material(out,root+'/materials/Body.tres',d['material'],root+'/distance/prong.png')
    (out/f'scripts/vfx_{kit["name"]}_material.gd').write_text('extends RefCounted\n'+MATERIAL_BINDING_SCRIPT)
    return {'grammar':'G3','frames':3,'schedule':_g3_config(kit)['schedule']}


def _write_g3_component(out):
    (out/'scripts').mkdir(parents=True,exist_ok=True);(out/'scenes/vfx').mkdir(parents=True,exist_ok=True)
    (out/'scripts/vfx_g3.gd').write_text(G3_SCRIPT)
    (out/'scripts/vfx_contact_label.gd').write_text(CONTACT_LABEL_SCRIPT)
    scene='[gd_scene load_steps=2 format=3]\n[ext_resource type="Script" path="res://scripts/vfx_g3.gd" id="G3"]\n[node name="G3BoltChain" type="Node2D"]\nscript = ExtResource("G3")\ntexture_filter = 2\nz_as_relative = false\nz_index = 2\n'
    for name in ('Links','Branches','Prongs','StrikeFlash'):
        scene+='\n[node name="'+name+'" type="Node2D" parent="."]\ntexture_filter = 2\n'
    (out/'scenes/vfx/g3_bolt_chain.tscn').write_text(scene)


G3_SCRIPT = r'''extends Node2D
# Instant geometry; effect age uses physics ticks, independent of hit-stop delta.
static var events: Array = []
static var label_events: Array = []
static var next_id: int = 0
var effect_id: int
var release_tick: int
var current_age: int = 0
var config: Dictionary = {}
var caster: Node2D
var active: bool = false
var hit: Dictionary = {}
var bolts: Array = []
var trace: Array = []
var tinted: Array = []
var last_target: Node2D
var last_point: Vector2
var hop_index: int = 0
var chain_done: bool = false
var rng := RandomNumberGenerator.new()

static func eligible(actor: Node, owner_node: Node = null) -> bool:
    return is_instance_valid(actor) and actor is Area2D and actor != owner_node and actor.is_inside_tree() and not actor.is_queued_for_deletion() and actor.is_in_group("vfx_targets")

static func resolve_target(tree: SceneTree, origin: Vector2, facing: Vector2, range_px: float, owner_node: Node = null) -> Dictionary:
    if not origin.is_finite() or not facing.is_finite() or facing.is_zero_approx() or not is_finite(range_px) or range_px <= 0.0: return {}
    var best: Node2D = null
    var nearest: float = INF
    var axis: Vector2 = facing.normalized()
    for actor in tree.get_nodes_in_group("vfx_targets"):
        if not eligible(actor,owner_node): continue
        var offset: Vector2 = actor.global_position-origin
        var distance: float = offset.length()
        if distance<=range_px and (distance<0.000001 or axis.dot(offset/distance)>=cos(deg_to_rad(30.0))-0.000001) and distance<nearest:
            best=actor
            nearest=distance
    return {"point":best.global_position if best!=null else origin+axis*range_px,"target":best,"kind":"prop" if best!=null else "miss","facing":axis}

static func acquire(parent: Node2D, kit: Dictionary, origin: Vector2, destination: Dictionary, owner_node: Node2D = null, _art_scale: float = 1.0) -> Node2D:
    if kit.get("grammar","")!="G3" or not origin.is_finite() or not destination.get("point") is Vector2 or not destination.point.is_finite() or destination.get("kind","") not in ["prop","miss"]: return null
    if destination.kind=="prop" and not eligible(destination.get("target"),owner_node): return null
    var effect: Node2D = load("res://scenes/vfx/g3_bolt_chain.tscn").instantiate()
    parent.add_child(effect)
    effect.release(kit,origin,destination,owner_node)
    return effect

func _ready() -> void:
    set_physics_process(false)

func age_frames() -> int:
    return current_age

func _record(event: String, fields: Dictionary = {}) -> void:
    var row: Dictionary = {"event":event,"effect_id":effect_id,"kit":config.name,"age_frames":current_age}
    row.merge(fields)
    events.append(row)

func release(kit: Dictionary, origin: Vector2, destination: Dictionary, owner_node: Node2D = null) -> void:
    config=kit.duplicate(true)
    caster=owner_node
    top_level=true
    global_transform=Transform2D.IDENTITY
    next_id+=1
    effect_id=next_id
    release_tick=Engine.get_physics_frames()
    # Re-seeded per cast; explicit cast_seed enables reproducible probes/replays.
    rng.seed=int(config.get("cast_seed",int(config.seed)+effect_id))
    current_age=0
    active=true
    last_target=destination.get("target")
    last_point=last_target.global_position if eligible(last_target,caster) else destination.point
    _record("release",{"seed":rng.seed,"target_kind":destination.kind,"target_point":[last_point.x,last_point.y],"schedule":config.schedule})
    _bolt(origin,last_point,last_target,0,0.0)
    chain_done=last_target==null or config.delays.is_empty()
    set_physics_process(true)

func _physics_process(_delta: float) -> void:
    if active: _clock(roundi(float(Engine.get_physics_frames()-release_tick)*60.0/Engine.physics_ticks_per_second))

func _nearest_unhit(point: Vector2) -> Node2D:
    var best: Node2D = null
    var nearest: float = INF
    for actor in get_tree().get_nodes_in_group("vfx_targets"):
        if not eligible(actor,caster) or hit.has(actor.get_instance_id()): continue
        var distance: float = point.distance_to(actor.global_position)
        if distance<=float(config.hop_range_px) and distance<nearest:
            best=actor
            nearest=distance
    return best

func _sprite(role: String, parent: Node, point: Vector2, angle: float, length: float, width: float) -> Sprite2D:
    var item: Dictionary = config.primitives[role]
    var start := Vector2(item.start[0],item.start[1])
    var finish := Vector2(item.end[0],item.end[1])
    var axis: Vector2 = finish-start
    var sprite := Sprite2D.new()
    sprite.texture=load(item.png)
    sprite.material=load(item.material).duplicate()
    sprite.centered=false
    var region: Array = item.region
    sprite.region_enabled=true
    sprite.region_rect=Rect2(region[0],region[1],region[2],region[3])
    sprite.region_filter_clip_enabled=true
    sprite.offset=Vector2(region[0],region[1])-start
    sprite.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
    # A basis maps the painted socket axis exactly onto the world segment.
    var along: Vector2 = Vector2.from_angle(angle)*(length/axis.length())
    var across: Vector2 = Vector2.from_angle(angle+PI/2.0)*width
    var u: Vector2 = axis.normalized()
    parent.add_child(sprite)
    sprite.transform=Transform2D(along*u.x-across*u.y,along*u.y+across*u.x,point)
    return sprite

func _bolt(origin: Vector2, target: Vector2, actor: Node2D, index: int, scheduled_s: float) -> void:
    var group := Node2D.new()
    group.name="Bolt_"+str(index)
    $Links.add_child(group)
    var branches := Node2D.new()
    branches.name="Branches_"+str(index)
    $Branches.add_child(branches)
    var prongs := Node2D.new()
    prongs.name="Prongs_"+str(index)
    $Prongs.add_child(prongs)
    var offset: Vector2 = target-origin
    var distance: float = offset.length()
    var axis: Vector2 = offset.normalized() if distance>0.00001 else Vector2.RIGHT
    var perpendicular := Vector2(-axis.y,axis.x)
    var nominal: float = float(config.link_length_px)
    var count: int = clampi(roundi(distance/(float(config.segment_fraction)*nominal)),int(config.min_links),int(config.max_links))
    var points: Array[Vector2] = [origin]
    for i in range(1,count):
        var jitter: float = rng.randf_range(-float(config.jitter_px),float(config.jitter_px))
        points.append(origin+axis*(distance*float(i)/count)+perpendicular*jitter)
    points.append(target)
    # If a jittered segment exceeds 1.15 of the native-width link, subdivide it.
    var fitted: Array[Vector2] = [origin]
    for i in range(points.size()-1):
        var splits: int = maxi(1,ceili(points[i].distance_to(points[i+1])/(1.15*nominal)))
        for j in range(1,splits+1): fitted.append(points[i].lerp(points[i+1],float(j)/splits))
    points=fitted
    var links: Array = []
    for i in range(points.size()-1):
        var a: Vector2 = points[i]
        var b: Vector2 = points[i+1]
        var length: float = a.distance_to(b)
        var node: Sprite2D = _sprite("link",group,a,(b-a).angle(),length,float(config.link_scale))
        node.name="Link_"+str(i)
        links.append({"start":[a.x,a.y],"end":[b.x,b.y],"length_px":length,"stretch_ratio":length/nominal,"transform":[[node.transform.x.x,node.transform.x.y],[node.transform.y.x,node.transform.y.y],[a.x,a.y]]})
    var branch_count: int = 0
    var branch_point: Variant = null
    if points.size()>2 and int(config.max_branches)>0:
        var vertex: int = rng.randi_range(1,points.size()-2)
        branch_point=[points[vertex].x,points[vertex].y]
        branch_count=int(config.max_branches)
        # Two forks use the junction; one fork uses the supplied needle so no hidden second fork appears.
        var role: String = "branch" if branch_count==2 else "prong"
        var branch: Sprite2D = _sprite(role,branches,points[vertex],axis.angle()+rng.randf_range(-.7,.7),float(config.prong_length_px),float(config.link_scale))
        branch.name="BranchJunction"
    var prong_positions: Array = []
    for i in range(int(config.prongs)):
        var prong: Sprite2D = _sprite("prong",prongs,target,TAU*float(i)/int(config.prongs)+axis.angle(),float(config.prong_length_px),float(config.link_scale)*.7)
        prong.name="NeedleProng_"+str(i)
        prong_positions.append([prong.position.x,prong.position.y])
    var flash: Node2D = Node2D.new()
    flash.name="StrikeFlash_"+str(index)
    $StrikeFlash.add_child(flash)
    if "flash" in config.enabled_layers:
        for i in range(4):
            var ray: Sprite2D = _sprite("prong",flash,target,TAU*float(i)/4.0,float(config.prong_length_px)*.45,float(config.link_scale))
            ray.modulate.a=.8
    var halo: Sprite2D = _sprite("branch",flash,target,0,float(config.prong_length_px)*.6,float(config.link_scale)*2.0)
    halo.name="Halo"
    halo.visible="halo" in config.enabled_layers
    halo.modulate.a=.12
    bolts.append({"node":group,"art":[group,branches,prongs],"flash":flash,"born":current_age,"index":index,"ended":false})
    _record("bolt",{"hop_index":index,"scheduled_s":scheduled_s,"origin":[origin.x,origin.y],"target_point":[target.x,target.y],"links":links,"link_count":links.size(),"prong_positions":prong_positions,"branch_count":branch_count,"junction_sprite_count":1 if branch_count==2 else 0,"branch_point":branch_point,"nominal_length_px":nominal,"width_px":config.width_px})
    if eligible(actor,caster):
        hit[actor.get_instance_id()]=true
        var body_index: int = int(actor.get_meta("body_index",actor.get_instance_id()))
        _record("contact",{"body_index":body_index,"contact_class":"primary","phase":"chain_hop","hop_index":index,"target_point":[target.x,target.y],"collision_age_frames":current_age,"contact_lag_frames":0,"strike_response":true})
        _response(actor,body_index)

func _response(actor: Node2D, body_index: int) -> void:
    var c: Array = config.palette_3
    if "victim_tint" in config.enabled_layers:
        var victim: CanvasItem = actor
        var prop: Node = actor.get_parent().get_node_or_null("Prop_"+String(actor.name).trim_prefix("VfxTarget_"))
        if prop is CanvasItem: victim=prop
        tinted.append({"node":victim,"original":victim.modulate,"end":current_age+6})
        victim.modulate=Color(c[0],c[1],c[2],victim.modulate.a)
        _record("victim_tint",{"body_index":body_index})
    if "contact_label" in config.enabled_layers:
        var label: Label = null
        for candidate in get_tree().get_nodes_in_group("vfx_contact_labels"):
            if not candidate.visible:
                label=candidate
                break
        if label==null:
            label=Label.new()
            label.set_script(load("res://scripts/vfx_contact_label.gd"))
            get_parent().add_child(label)
        label.top_level=true
        label.scale=Vector2.ONE
        label.rotation=0.0
        label.show_contact(actor.global_position+Vector2(0,-70),"FULL",Color(c[0],c[1],c[2],c[3]),effect_id,body_index,label_events)
    if "hit_stop" in config.enabled_layers:
        _record("hit_stop",{"body_index":body_index,"duration_s":1.0/60.0,"time_scale":.1})
        _strike_stop()

func _clock(age: int) -> void:
    if not active: return
    current_age=age
    while not chain_done and hop_index<config.cumulative.size() and age>=ceili(float(config.cumulative[hop_index])*60.0-0.000001):
        if eligible(last_target,caster): last_point=last_target.global_position
        var target: Node2D = _nearest_unhit(last_point)
        if target==null:
            chain_done=true
            _record("chain_end",{"reason":"no_eligible_unhit_target","completed_hops":hop_index})
            break
        var start: Vector2 = last_point
        last_target=target
        last_point=target.global_position
        _bolt(start,last_point,target,hop_index+1,float(config.cumulative[hop_index]))
        hop_index+=1
        if hop_index>=config.cumulative.size(): chain_done=true
    var visible_count: int = 0
    for bolt in bolts:
        var local_age: int = age-int(bolt.born)
        var seconds: float = float(local_age)/60.0
        # End on the final representable frame no later than the specified deadline.
        var end_frame: int = floori((float(config.life_s)+float(config.afterimage_s))*60.0+0.000001)
        var dissolve: float = clampf((seconds-float(config.life_s))/float(config.afterimage_s),0.0,1.0)
        bolt.node.visible=local_age<end_frame
        bolt.flash.visible=local_age==0
        if bolt.node.visible: visible_count+=1
        for art in bolt.art:
            art.visible=bolt.node.visible
            for sprite in art.get_children(): sprite.material.set_shader_parameter("dissolve",dissolve)
        if local_age>=end_frame and not bolt.ended:
            bolt.ended=true
            _record("bolt_end",{"hop_index":bolt.index,"local_age_frames":local_age,"local_age_s":seconds})
        trace.append({"age_frames":age,"hop_index":bolt.index,"local_age_frames":local_age,"visible":bolt.node.visible,"dissolve":dissolve,"flash_visible":bolt.flash.visible})
    for entry in tinted:
        if is_instance_valid(entry.node) and age>=int(entry.end): entry.node.modulate=entry.original
    tinted=tinted.filter(func(entry):return is_instance_valid(entry.node) and age<int(entry.end))
    if chain_done and visible_count==0:
        _record("expire")
        active=false
        hide()
        set_physics_process(false)
        _restore_tints()
        queue_free()

func _restore_tints() -> void:
    for entry in tinted:
        if is_instance_valid(entry.node): entry.node.modulate=entry.original
    tinted.clear()

func cancel() -> void:
    if not active: return
    _record("cancel")
    _restore_tints()
    active=false
    queue_free()

func _strike_stop() -> void:
    if "hit_stop" not in config.enabled_layers: return
    var tree: SceneTree = get_tree()
    var controller: Node = tree.root.get_node_or_null("EffectHitstop")
    if controller == null:
        controller=Node.new()
        controller.name="EffectHitstop"
        controller.set_meta("baseline",Engine.time_scale)
        controller.set_meta("generation",0)
        tree.root.add_child(controller)
    var generation: int = int(controller.get_meta("generation"))+1
    controller.set_meta("generation",generation)
    Engine.time_scale=.1
    tree.create_timer(1.0/60.0,true,false,true).timeout.connect(func():
        if is_instance_valid(controller) and int(controller.get_meta("generation"))==generation:
            Engine.time_scale=float(controller.get_meta("baseline"))
            controller.name="EffectHitstopDone"
            controller.queue_free())
'''



# T4u: explicit G4 dispatch, with no target resolution in the renderer.
def _g4_config(kit):
    from export.effect_kit import tick_schedule_report
    d=kit['effect'];m=d['skill_spec']['mechanics'];p=d['skill_spec']['presentation'];g=d['g4'];root='res://vfx/'+kit['name']+'/'
    return dict(name=kit['name'],grammar='G4',screen_px=True,bolt='res://scenes/vfx/g4_aura_loop.tscn',flare=root+'flare.tres',
                radius_px=m['radius_px'],duration_s=m['duration_s'],pulses=m['pulse_schedule_s'],
                schedule=tick_schedule_report(m['pulse_schedule_s'],m['pulse_cv_min']),
                orbit_period_s=p['phase_envelope_s']['ring_orbit_period'],petal_life_s=p['phase_envelope_s']['petal_life'],
                release_s=g['release_s'],seed=g['seed'],support_tint=g['support_tint'],seal_aspect=g['seal_aspect'],
                primitives={role:dict(g[role],png=root+g[role]['png'],material=root+'materials/'+role.title()+'.tres') for role in ('ring','petal','seal')},
                halo_material=root+'materials/Halo.tres',floor_material=root+'materials/FloorLight.tres')


def _write_g4_kit(out, kit):
    import numpy as np
    from export.effect_kit import distance_field,write_vfx_material,MATERIAL_BINDING_SCRIPT
    d=kit['effect'];root='vfx/'+kit['name'];dest=out/root
    for path in kit['root'].rglob('*'):
        if path.is_file():
            target=dest/path.relative_to(kit['root']);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
    for phase,folder in [('cast','flare'),('travel','travel'),('impact','impact')]:
        frames=d['phases'][phase]['frames']
        write_spriteframes(out,root+'/'+folder+'.tres',{folder:([root+'/'+f['file'] for f in frames],1,False)}, {folder:[f['hold_frames']/60 for f in frames]})
    (dest/'distance').mkdir(exist_ok=True)
    for role in ('ring','petal','seal'):
        with Image.open(dest/d['g4'][role]['png']) as im:a=np.asarray(im)
        field=root+'/distance/'+role+'.png';Image.fromarray(distance_field(a)).save(out/field)
        write_vfx_material(out,root+'/materials/'+role.title()+'.tres',dict(d['material'],blend_mode='MIX' if role=='seal' else 'ADD'),field)
    for label,role in [('Body','petal'),('Additive','petal'),('Halo','seal'),('FloorLight','seal')]:
        write_vfx_material(out,root+'/materials/'+label+'.tres',d['material'],root+'/distance/'+role+'.png')
    (out/f'scripts/vfx_{kit["name"]}_material.gd').write_text('extends RefCounted\n'+MATERIAL_BINDING_SCRIPT)
    return {'grammar':'G4','frames':3,'schedule':_g4_config(kit)['schedule']}


def _write_g4_component(out):
    (out/'scripts').mkdir(parents=True,exist_ok=True);(out/'scenes/vfx').mkdir(parents=True,exist_ok=True)
    (out/'scripts/vfx_g4.gd').write_text(G4_SCRIPT)
    (out/'scripts/vfx_contact_label.gd').write_text(CONTACT_LABEL_SCRIPT)
    scene='[gd_scene load_steps=2 format=3]\n[ext_resource type="Script" path="res://scripts/vfx_g4.gd" id="G4"]\n[node name="G4AuraLoop" type="Node2D"]\nscript = ExtResource("G4")\ntexture_filter = 2\n'
    for name,kind,parent in [('Ground','Node2D','.'),('SealPivot','Node2D','Ground'),('Seal','Sprite2D','Ground/SealPivot'),('Halo','Sprite2D','Ground'),('FloorLight','Sprite2D','Ground'),('Ring','Node2D','.'),('Petals','Node2D','.')]:
        scene+='\n[node name="'+name+'" type="'+kind+'" parent="'+parent+'"]\ntexture_filter = 2\n'
    (out/'scenes/vfx/g4_aura_loop.tscn').write_text(scene)


G4_SCRIPT = r'''extends Node2D
static var events: Array = []
static var label_events: Array = []
static var next_id: int = 0
var effect_id: int = 0
var generation: int = 0
var config: Dictionary = {}
var caster: Node2D
var age: int = 0
var pulse_index: int = 0
var active: bool = false
var releasing: bool = false
var rng := RandomNumberGenerator.new()
var tinted: Array = []
var trace: Array = []

static func acquire(owner_root: Node2D, kit: Dictionary) -> Node2D:
    if not is_instance_valid(owner_root) or kit.get("grammar", "") != "G4": return null
    for child in owner_root.get_children():
        if child.has_meta("g4_aura") and child.config.name == kit.name:
            child.start(kit, owner_root, true)
            return child
    var effect: Node2D = load("res://scenes/vfx/g4_aura_loop.tscn").instantiate()
    next_id += 1
    effect.effect_id = next_id
    effect.set_meta("g4_aura", true)
    owner_root.add_child(effect)
    effect.start(kit, owner_root, false)
    return effect

func age_frames() -> int:
    return age

func _record(event: String, extra: Dictionary = {}) -> void:
    var entry: Dictionary = {"event":event,"effect_id":effect_id,"generation":generation,"age_frames":age}
    entry.merge(extra)
    events.append(entry)

func _bind(sprite: Sprite2D, role: String) -> void:
    var p: Dictionary = config.primitives[role]
    sprite.texture = load(p.png)
    sprite.centered = false
    sprite.offset = -Vector2(p.pivot[0],p.pivot[1])
    sprite.scale = Vector2.ONE * float(p.scale)
    sprite.material = load(p.material).duplicate()
    sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR

func _absolute_z(node: CanvasItem) -> int:
    var total: int = node.z_index
    var cursor: Node = node.get_parent()
    while node.z_as_relative and cursor is CanvasItem:
        node = cursor
        total += node.z_index
        cursor = cursor.get_parent()
    return total

func _sync() -> void:
    # Parent ownership supplies immediate translation; remove inherited art scale/rotation.
    global_transform = Transform2D(0.0, caster.global_position)
    var actor_z: int = _absolute_z(caster)
    $Ground.z_as_relative = false
    $Ground.z_index = actor_z-1
    for segment in $Ring.get_children():
        segment.z_as_relative = false
        segment.z_index = actor_z-1 if segment.position.y<0 else actor_z+1
    $Petals.z_as_relative = false
    $Petals.z_index = actor_z+1

func start(kit: Dictionary, owner_root: Node2D, refresh: bool) -> void:
    _restore_tints()
    config = kit.duplicate(true)
    caster = owner_root
    generation += 1
    age = 0
    pulse_index = 0
    releasing = false
    active = true
    rng.seed = int(config.seed)
    for container in [$Ring,$Petals]:
        for child in container.get_children(): child.free()
    _bind($Ground/SealPivot/Seal,"seal")
    $Ground/SealPivot.scale = Vector2(1,float(config.seal_aspect))
    $Ground/SealPivot/Seal.scale.y /= float(config.seal_aspect)
    $Ground/SealPivot/Seal.rotation = 0.0
    $Ground/SealPivot/Seal.modulate.a = .8
    for name in ["Halo","FloorLight"]:
        var sprite: Sprite2D = get_node("Ground/"+name)
        _bind(sprite,"seal")
        sprite.material = load(config.halo_material if name=="Halo" else config.floor_material).duplicate()
        sprite.scale *= 1.02 if name=="Halo" else 1.15
        sprite.modulate.a = .2 if name=="Halo" else .15
    for i in range(5):
        var segment := Sprite2D.new()
        segment.name = "Segment"+str(i)
        $Ring.add_child(segment)
        _bind(segment,"ring")
    show()
    _record("refresh" if refresh else "release",{"clock_reset":0})
    if not bool(config.schedule.ff08_satisfied):
        _record("schedule_assertion",{"interval_cv":config.schedule.interval_cv,"minimum_cv":config.schedule.minimum_cv,"satisfied":false})
        push_warning("FF-08 authored pulse interval CV below minimum; schedule retained")
    _clock(0)
    set_physics_process(true)

func _physics_process(_delta: float) -> void:
    _clock(age+1)

func _clock(frame: int) -> void:
    if not active: return
    if not is_instance_valid(caster): cancel(); return
    age = frame
    _tint_clock()
    var ending: int = ceili(float(config.duration_s)*60)
    var release_frames: int = ceili(float(config.release_s)*60)
    while pulse_index<config.pulses.size() and roundi(float(config.pulses[pulse_index])*60)<=age and age<ending:
        _pulse(pulse_index)
        pulse_index += 1
    if age>=ending and not releasing:
        releasing = true
        _record("release_start")
    var fade: float = clampf(float(age-ending)/release_frames,0,1)
    $Ground/SealPivot/Seal.rotation = TAU*float(age)/480.0
    $Ground/SealPivot/Seal.modulate.a = .8*(1.0-fade)
    $Ground/Halo.modulate.a = .2*(1.0-fade)
    $Ground/FloorLight.modulate.a = .15*(1.0-fade)
    for i in range(5):
        var segment: Sprite2D = $Ring.get_child(i)
        var theta: float = TAU*(float(i)/5.0+float(age)/60.0/float(config.orbit_period_s))
        segment.position = Vector2(cos(theta),sin(theta)*.58)*float(config.radius_px)
        segment.rotation = 0.0
        segment.material.set_shader_parameter("erode",fade)
    for petal in $Petals.get_children():
        var life: int = age-int(petal.get_meta("born"))
        var total: int = roundi(float(config.petal_life_s)*60)
        if life>=total:
            _record("petal_end",{"petal_id":petal.get_meta("id"),"lifetime_frames":life})
            petal.free()
            continue
        var progress: float = float(life)/float(total-1)
        petal.scale = Vector2.ONE*float(config.primitives.petal.scale)*lerpf(.6,1.0,progress)
        petal.position = petal.get_meta("origin")+Vector2(0,-60.0*progress)
        petal.rotation = 0.0
        var dissolve: float = 0.0 if life<18 else (.5 if life<22 else .7)
        petal.material.set_shader_parameter("dissolve",dissolve)
        petal.modulate.a = 1.0 if life<18 else 1.0-float(life-18)/9.0
    _sync()
    trace.append({"age_frames":age,"generation":generation,"owner":[caster.global_position.x,caster.global_position.y],"seal":[ $Ground/SealPivot/Seal.global_position.x,$Ground/SealPivot/Seal.global_position.y],"ring_center":[ $Ring.global_position.x,$Ring.global_position.y],"petal_count":$Petals.get_child_count(),"pulse_count":pulse_index,"erode":fade,"seal_alpha":$Ground/SealPivot/Seal.modulate.a})
    if age>=ending+release_frames:
        _record("expire")
        active = false
        _restore_tints()
        hide()
        set_physics_process(false)
        queue_free()

func _pulse(index: int) -> void:
    _record("pulse",{"pulse_index":index,"scheduled_age_frames":roundi(float(config.pulses[index])*60)})
    for i in range(6):
        var petal := Sprite2D.new()
        $Petals.add_child(petal)
        _bind(petal,"petal")
        var theta: float = rng.randf_range(0,TAU)
        var point := Vector2(cos(theta),sin(theta)*.58)*float(config.radius_px)
        petal.set_meta("born",age)
        petal.set_meta("origin",point)
        petal.set_meta("id",index*6+i)
        _record("petal_start",{"petal_id":index*6+i,"origin":[point.x,point.y],"lifetime_frames":27})
    var actors: Array = get_tree().get_nodes_in_group("vfx_targets")
    for actor in get_tree().get_nodes_in_group("vfx_actors"):
        if actor not in actors: actors.append(actor)
    if caster not in actors: actors.append(caster)
    for actor in actors:
        if not is_instance_valid(actor) or not actor is Node2D or actor.global_position.distance_to(caster.global_position)>float(config.radius_px): continue
        var body_index: int = int(actor.get_meta("body_index",actor.get_instance_id()))
        var victim: CanvasItem = actor
        var prop: Node = actor.get_parent().get_node_or_null("Prop_"+String(actor.name).trim_prefix("VfxTarget_"))
        if prop is CanvasItem: victim=prop
        var original: Color = victim.modulate
        for entry in tinted:
            if entry.node==victim: original=entry.original
        tinted=tinted.filter(func(entry):return entry.node!=victim)
        tinted.append({"node":victim,"original":original,"end":age+9})
        var c: Array = config.support_tint
        victim.modulate=Color(c[0],c[1],c[2],original.a)
        _record("support_tint",{"body_index":body_index,"pulse_index":index,"colour":c})
        var label: Label = null
        for candidate in get_tree().get_nodes_in_group("vfx_contact_labels"):
            if not candidate.visible:
                label=candidate
                break
        if label==null:
            label=Label.new()
            label.set_script(load("res://scripts/vfx_contact_label.gd"))
            caster.get_parent().add_child(label)
        label.top_level=true
        label.scale=Vector2.ONE
        label.rotation=0.0
        label.show_contact(actor.global_position+Vector2(0,-70),"+",Color(c[0],c[1],c[2],c[3]),effect_id,body_index,label_events)
        _record("heal_label",{"body_index":body_index,"pulse_index":index,"text":"+"})

func _tint_clock() -> void:
    for entry in tinted:
        if is_instance_valid(entry.node) and age>=int(entry.end): entry.node.modulate=entry.original
    tinted=tinted.filter(func(entry):return is_instance_valid(entry.node) and age<int(entry.end))

func _restore_tints() -> void:
    for entry in tinted:
        if is_instance_valid(entry.node): entry.node.modulate=entry.original
    tinted.clear()

func cancel() -> void:
    _record("cancel")
    active=false
    _restore_tints()
    queue_free()

func _exit_tree() -> void:
    _restore_tints()
'''




def _write_orb_nova(out, kit, resource_root, prefix):
    """Reuse the sixteen immutable masks with a separate expiry clock."""
    import copy
    from export.effect_kit import write_vfx_material
    d=kit['effect']; legacy=dict(kit,effect=copy.deepcopy(d))
    legacy['effect'].pop('orb')
    legacy['effect']['pieces']['template']='burst_v1'
    legacy['effect']['layers']['dark_duplicate']=False
    _write_piece_burst(out,legacy,resource_root,prefix)
    scene_path=out/f'scenes/{prefix}_impact.tscn'; scene=scene_path.read_text()
    scene=scene.replace('res://scripts/vfx/piece_burst.gd','res://scripts/vfx/orb_nova.gd')
    body=d['orb']['body']; source=kit['root']/body['png']
    target=out/resource_root/body['png']; target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    field=d['distance_fields'][body['png']]; target=out/resource_root/field;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(kit['root']/field,target)
    with Image.open(source) as im: box=im.getchannel('A').getbbox()
    scale=d['orb']['expiry_core_bh']*130/max(box[2]-box[0],box[3]-box[1])
    material=resource_root+'/materials/NovaCore.tres'
    write_vfx_material(out,material,dict(d['material'],blend_mode='ADD'),resource_root+'/'+field)
    ext=f'[ext_resource type="Texture2D" path="res://{resource_root}/{body["png"]}" id="CoreTexture"]\n[ext_resource type="Material" path="res://{material}" id="CoreMaterial"]\n'
    index=scene.index('[node ');scene=scene[:index]+ext+scene[index:]
    scene += ('\n[node name="Core" type="Sprite2D" parent="Art"]\ntexture_filter = 2\ncentered = false\n'
              f'offset = Vector2({-body["pivot"][0]}, {-body["pivot"][1]})\nscale = Vector2({scale}, {scale})\n'
              'texture = ExtResource("CoreTexture")\nmaterial = ExtResource("CoreMaterial")\n')
    scene=re.sub(r'load_steps=\d+','load_steps='+str(scene.count('[ext_resource ')+1),scene,count=1)
    scene_path.write_text(scene)
    runtime_path=out/resource_root/'pieces/burst_runtime.json';runtime=json.loads(runtime_path.read_text())
    runtime.update(phase_scale=1.,expiry_mode='nova',expiry_core_bh=d['orb']['expiry_core_bh'],expiry_decal=False,hold_frames=0,residue_frames=0)
    runtime_path.write_text(json.dumps(runtime,indent=2)+'\n')
    (out/'scripts/vfx/orb_nova.gd').write_text(ORB_NOVA_SCRIPT)


ORB_NOVA_SCRIPT = r'''extends "res://scripts/vfx/piece_burst.gd"
func set_effect_age(age: int) -> void:
    if age==last_age: return
    last_age=age
    for name in ["Peak","PeakDark","Flash","Glow"]: get_node("Art/"+name).hide()
    $FloorLight.hide()
    $Art/Core.visible=age<6
    $Art/Core.modulate.a=maxf(0.0,1.0-float(age)/6.0)
    var states: Array=[]
    var alive: bool=age<30
    for item in pieces:
        var node: Sprite2D=item.node
        var angle: float=deg_to_rad(float(item.record.radial_angle_deg))
        var axis: Vector2=Vector2.from_angle(angle)
        node.position=axis*float(config.base_speed_px_s)*float(age)/60.0
        node.rotation=angle
        node.scale=Vector2.ONE
        node.visible=alive
        node.material.set_shader_parameter("erode",clampf(float(age)/30.0,0,1))
        node.material.set_shader_parameter("dissolve",0.0)
        states.append({"id":item.record.id,"position":[node.position.x,node.position.y],"distance_px":node.position.length(),"rotation_deg":rad_to_deg(angle),"visible":alive,"erode":clampf(float(age)/30.0,0,1)})
    trace.append({"age_frames":age,"stage":"nova" if alive else "zero","peak_visible":$Art/Peak.visible or $Art/PeakDark.visible or $Art/Flash.visible or $Art/Glow.visible,"decal_visible":has_node("Decal"),"residue_visible":false,"core_visible":$Art/Core.visible,"core_alpha":$Art/Core.modulate.a,"shard_count":pieces.size() if alive else 0,"pieces":states})
    if not alive:
        hide()
        _write_trace()
        queue_free()
'''


def _orb_config(kit):
    from export.effect_kit import orb_schedule_report
    d=kit.get('effect', {})
    if 'orb' not in d: return {}
    m=d['skill_spec']['mechanics']; g=json.loads(json.dumps(d['orb'])); root='res://vfx/'+kit['name']+'/'
    for role in ('body','shard'):
        g[role]['png']=root+g[role]['png']
        g[role]['material']=root+'materials/Orb_'+role+'.tres'
    return dict(grammar='G1',bolt='res://scenes/vfx/g1_orb.tscn',orb=g,
                range_px=m['range_px'],speed_px_s=m['speed_px_s'],contact_only=True,
                expiry_frames=math.ceil(m['expiry']['time_s']*60),child_speed_px_s=m['emission']['child_speed_px_s'],
                child_range_px=m['emission']['child_range_px'],schedule=orb_schedule_report(d),
                enabled_layers=d['skill_spec']['presentation']['enabled_layers'],strike_stop_s=1/60)


def _write_orb(out, kit, resource_root):
    from export.effect_kit import write_vfx_material
    d=kit['effect']
    for role in ('body','shard'):
        item=d['orb'][role];target=out/resource_root/item['png'];target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(kit['root']/item['png'],target)
        field=out/resource_root/d['distance_fields'][item['png']]
        field.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(kit['root']/d['distance_fields'][item['png']],field)
        write_vfx_material(out,resource_root+'/materials/Orb_'+role+'.tres',
            dict(d['material'],erode=0.,dissolve=0.,erode_outside_in=False),resource_root+'/'+d['distance_fields'][item['png']])
    body_field=resource_root+'/'+d['distance_fields'][d['orb']['body']['png']]
    write_vfx_material(out,resource_root+'/materials/Orb_dark.tres',d['material'],body_field,True)
    write_vfx_material(out,resource_root+'/materials/Orb_halo.tres',dict(d['material'],blend_mode='ADD'),body_field)
    shard_field=resource_root+'/'+d['distance_fields'][d['orb']['shard']['png']]
    write_vfx_material(out,resource_root+'/materials/Orb_flash.tres',dict(d['material'],blend_mode='ADD'),shard_field)
    scene=G1_SCENE.replace('res://scripts/vfx_g1.gd','res://scripts/vfx_g1_orb.gd')
    scene=scene.replace('collision_layer = 0','z_as_relative = false\nz_index = 3\ncollision_layer = 0')
    scene += '\n[node name="OrbBody" type="Sprite2D" parent="."]\ntexture_filter = 2\n'
    for name in ('OrbDark','OrbHalo'):
        scene += '\n[node name="'+name+'" type="Sprite2D" parent="."]\ntexture_filter = 2\nz_index = -1\n'
    scene += '\n[node name="Rim" type="Node2D" parent="."]\n'
    for i in range(4): scene += '\n[node name="Shard%d" type="Sprite2D" parent="Rim"]\ntexture_filter = 2\n'%i
    scene += '\n[node name="ChildPool" type="Node2D" parent="."]\ntop_level = true\n'
    (out/'scenes/vfx/g1_orb.tscn').write_text(scene)
    child=G1_SCENE.replace('res://scripts/vfx_g1.gd','res://scripts/vfx_g1_orb_child.gd')
    child += '\n[node name="Shard" type="Sprite2D" parent="."]\ntexture_filter = 2\n'
    child += '\n[node name="StrikeFlash" type="Sprite2D" parent="."]\ntexture_filter = 2\nvisible = false\n'
    (out/'scenes/vfx/g1_orb_child.tscn').write_text(child)
    (out/'scripts/vfx_g1_orb.gd').write_text(ORB_SCRIPT)
    (out/'scripts/vfx_g1_orb_child.gd').write_text(ORB_CHILD_SCRIPT)

ORB_SCRIPT = r'''extends "res://scripts/vfx_g1.gd"
var draining: bool = false
var expiry_age: int = -1
var emission_index: int = 0
var schedule_index: int = 0
var burst_started: bool = false
var rng := RandomNumberGenerator.new()
var initial_angle: float = 0.0
var labelled: Dictionary = {}
var tinted: Array = []
var trace: Array = []
var burst_node: Node2D
var contact_flash_end: int = -1

func _bind(node: Sprite2D, item: Dictionary) -> void:
    node.texture = load(item.png)
    node.material = load(item.material).duplicate()
    node.centered = false
    node.offset = -Vector2(item.pivot[0], item.pivot[1])
    node.scale = Vector2.ONE * float(item.scale)

func release(kit: Dictionary, origin: Vector2, destination: Dictionary, owner_node: Node2D = null, art_scale: float = 1.0) -> void:
    super.release(kit, origin, destination, owner_node, art_scale)
    draining = false
    expiry_age = -1
    emission_index = 0
    schedule_index = 0
    burst_started = false
    labelled.clear()
    trace.clear()
    rng.seed = int(config.orb.seed)
    initial_angle = rng.randf_range(0.0, 360.0)
    _bind($OrbBody, config.orb.body)
    for pair in [[$OrbDark,"dark"],[$OrbHalo,"halo"]]:
        _bind(pair[0],config.orb.body)
        pair[0].material = load(String(config.orb.body.material).replace("Orb_body","Orb_"+pair[1]))
        pair[0].show()
    $OrbHalo.scale *= 1.02
    $OrbHalo.modulate.a = 0.2
    contact_flash_end = -1
    for node in $Rim.get_children():
        _bind(node, config.orb.shard)
        var angle: float = node.get_index() * TAU / 4.0
        node.position = Vector2.RIGHT.rotated(angle) * float(config.orb.rim_radius_px)
        node.rotation = angle
    while $ChildPool.get_child_count() < int(config.orb.pool_size):
        var child: Area2D = load("res://scenes/vfx/g1_orb_child.tscn").instantiate()
        child.name = "Child_%02d" % $ChildPool.get_child_count()
        $ChildPool.add_child(child)
    $ChildPool.global_position = Vector2.ZERO
    $OrbBody.show()
    $Rim.show()
    $Head.hide()
    $Trail.hide()

func _physics_process(_delta: float) -> void:
    var age: int = age_frames()
    if not draining:
        # One displacement per effect-age frame, independent of hit-stop delta.
        var desired: float = minf(float(config.range_px), float(config.speed_px_s) * minf(age, int(config.expiry_frames)) / 60.0)
        super._physics_process(maxf(0.0, desired - distance) / float(config.speed_px_s))
        $Trail.hide()
        $OrbBody.rotation = age * TAU / (60.0 * float(config.orb.turn_s))
        $Rim.rotation = $OrbBody.rotation
        $OrbDark.rotation = $OrbBody.rotation
        $OrbHalo.rotation = $OrbBody.rotation
        $OrbHalo.modulate.a = 0.8 if age < contact_flash_end else 0.2
        # Consume the exported seeded ages verbatim: Python and Godot RNGs differ.
        while schedule_index < config.schedule.emission_ages.size() and int(config.schedule.emission_ages[schedule_index]) <= mini(age, int(config.schedule.flight_frames)):
            _emit_child(int(config.schedule.emission_ages[schedule_index]))
            schedule_index += 1
        if age >= int(config.expiry_frames) and not draining: expire()
    if draining and not burst_started and age >= expiry_age + (0 if config.orb.expiry_mode=="nova" else 2):
        burst_started = true
        burst_node = load(config.impact).instantiate()
        burst_node.set("spell_scale", 1.0)
        burst_node.set("caster", caster)
        burst_node.set("direction", direction)
        burst_node.position = get_parent().to_local(global_position)
        get_parent().add_child(burst_node)
        # The orb already held for two ticks. Enter v1r's radial stage directly.
        var start_age: int = 0 if config.orb.expiry_mode=="nova" else 3
        burst_node.release_tick = Engine.get_physics_frames() - start_age
        burst_node.set_effect_age(start_age)
        _record("expiry_burst")
        events[-1].merge({"shards":16,"position":[global_position.x,global_position.y],"hold_frames":age-expiry_age})
        $OrbBody.hide()
        $OrbDark.hide()
        $OrbHalo.hide()
        $Rim.hide()
    var live: int = 0
    for child in $ChildPool.get_children():
        if child.active: live += 1
    trace.append({"age_frames":age,"position":[global_position.x,global_position.y],"distance_px":distance,"children_live":live,"pool_nodes":$ChildPool.get_child_count(),"emissions":emission_index,"draining":draining})
    for i in range(tinted.size()-1,-1,-1):
        var item: Dictionary = tinted[i]
        if age >= int(item.until):
            if is_instance_valid(item.node): item.node.modulate = item.colour
            tinted.remove_at(i)
    if draining and burst_started and live == 0 and tinted.is_empty():
        draining = false
        super._recycle()

func _emit_child(scheduled: int) -> void:
    var child: Area2D = null
    for candidate in $ChildPool.get_children():
        if not candidate.active:
            child = candidate
            break
    if child == null:
        _record("pool_exhausted")
        return
    var angle: float = initial_angle + emission_index * float(config.orb.angle_step_deg)
    var axis: Vector2 = Vector2.RIGHT.rotated(deg_to_rad(angle))
    var child_config: Dictionary = config.duplicate(true)
    child_config.pierce = 0
    child_config.collision_radius_bh = config.child_collision_radius_bh
    child_config.head_length_px = config.child_head_length_px
    child_config.range_px = config.child_range_px
    child_config.speed_px_s = config.child_speed_px_s
    child_config.animation = "travel"
    child_config.binding = ""
    child.orb_owner = self
    child.release(child_config, global_position, {"point":global_position+axis*float(config.child_range_px),"kind":"cursor","target":null},caster,1.0)
    emission_index += 1
    _record("child_emission")
    events[-1].merge({"index":emission_index-1,"scheduled_age":scheduled,"angle_deg":angle,"position":[global_position.x,global_position.y],"pool_slot":child.get_index()})

func _contact_label(area: CollisionObject2D, body_index: int, contact_class: String) -> void:
    if labelled.has(area.get_instance_id()): return
    labelled[area.get_instance_id()] = true
    super._contact_label(area,body_index,contact_class)

func _spawn_impact(_strike_response: bool = true, _point: Variant = null) -> void:
    contact_flash_end = age_frames()+2
    if _strike_response: _strike_stop()

func contact_body(area: CollisionObject2D, phase: String = "head") -> void:
    var fresh: bool = is_instance_valid(area) and not contacted.has(area.get_instance_id())
    super.contact_body(area,phase)
    if fresh and contacted.has(area.get_instance_id()): tint_target(area)

func _strike_stop() -> void:
    # The spec's one contact frame supplies the shared strike hold duration.
    var tree: SceneTree = get_tree()
    var controller: Node = tree.root.get_node_or_null("EffectHitstop")
    if controller == null:
        controller = Node.new()
        controller.name = "EffectHitstop"
        controller.set_meta("baseline", Engine.time_scale)
        controller.set_meta("generation", 0)
        tree.root.add_child(controller)
    var generation: int = int(controller.get_meta("generation")) + 1
    controller.set_meta("generation", generation)
    Engine.time_scale = 0.1
    tree.create_timer(float(config.strike_stop_s), true, false, true).timeout.connect(func():
        if is_instance_valid(controller) and int(controller.get_meta("generation")) == generation:
            Engine.time_scale = float(controller.get_meta("baseline"))
            controller.name = "EffectHitstopDone"
            controller.queue_free())


func tint_target(area: CollisionObject2D) -> void:
    var victim: CanvasItem = area
    var prop: Node = area.get_parent().get_node_or_null("Prop_"+String(area.name).trim_prefix("VfxTarget_"))
    if prop is CanvasItem: victim = prop
    for item in tinted:
        if item.node == victim:
            item.until = age_frames()+6
            return
    tinted.append({"node":victim,"colour":victim.modulate,"until":age_frames()+6})
    victim.modulate = Color(0.64,0.88,0.96,1)

func expire() -> void:
    if not active or draining: return
    _record("expire")
    events[-1].merge({"position":[global_position.x,global_position.y],"distance_px":distance,"reason":"range" if distance >= float(config.range_px) else "time"})
    expiry_age = age_frames()
    expired = true
    draining = true
    set_deferred("monitoring", false)

func cancel() -> void:
    if active: _record("cancel")
    for child in $ChildPool.get_children(): child.cancel()
    for item in tinted:
        if is_instance_valid(item.node): item.node.modulate = item.colour
    tinted.clear()
    if is_instance_valid(burst_node): burst_node.queue_free()
    draining = false
    super._recycle()
'''

ORB_CHILD_SCRIPT = r'''extends "res://scripts/vfx_g1.gd"
var orb_owner: Area2D
var flash_end: int = -1
var draining: bool = false

func release(kit: Dictionary, origin: Vector2, destination: Dictionary, owner_node: Node2D = null, art_scale: float = 1.0) -> void:
    super.release(kit,origin,destination,owner_node,art_scale)
    flash_end = -1
    draining = false
    orb_owner._bind($Shard, config.orb.shard)
    orb_owner._bind($StrikeFlash, config.orb.shard)
    $StrikeFlash.material = load(String(config.orb.shard.material).replace("Orb_shard","Orb_flash"))
    $Shard.rotation = direction.angle()
    $Shard.show()
    $StrikeFlash.hide()
    $Head.hide()
    $Trail.hide()

func _physics_process(_delta: float) -> void:
    if flash_end >= 0:
        if age_frames() >= flash_end: super._recycle()
        return
    var desired: float = minf(float(config.range_px),float(config.speed_px_s)*age_frames()/60.0)
    super._physics_process(maxf(0.0,desired-distance)/float(config.speed_px_s))
    $Trail.hide()

func contact_body(area: CollisionObject2D, _phase: String = "head") -> void:
    if not active or flash_end >= 0 or area == caster or not is_instance_valid(area): return
    if contacted.has(area.get_instance_id()): return
    if (area.global_position - cast_origin).dot(release_facing) < 32.5: return
    contacted[area.get_instance_id()] = true
    var index: int = int(area.get_meta("body_index",area.get_instance_id()))
    _record("contact",age_frames())
    events[-1].merge({"position":[global_position.x,global_position.y],"parent_effect_id":orb_owner.effect_id,"body_index":index,"phase":"shard","contact_class":"secondary","strike_response":false})
    if area.is_in_group("vfx_targets"): orb_owner._contact_label(area,index,"secondary")
    orb_owner.tint_target(area)
    $Shard.hide()
    $StrikeFlash.rotation = direction.angle()
    $StrikeFlash.scale *= 1.25
    $StrikeFlash.show()
    flash_end = age_frames()+2
    set_deferred("monitoring",false)
    _record("child_strike_flash")

func _spawn_impact(_strike_response: bool = true, _point: Variant = null) -> void:
    pass

func cancel() -> void:
    flash_end = -1
    $StrikeFlash.hide()
    super.cancel()
'''




# FL-1a: caster-owned, updated on entry and every physics frame, independent of projectile life.
CAST_HALO_SCRIPT = r''' 
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
'''





def _fire_burst_script(script):
    script = script.replace('    tree_exiting.connect(_write_trace)', '''    $FloorLight.material = $FloorLight.material.duplicate()
    var colour: Array = config.palette[2]
    for band in range(4): $FloorLight.material.set_shader_parameter("palette_"+str(band),Color(colour[0],colour[1],colour[2],1))
    $Art/Glow.material = $Art/Glow.material.duplicate()
    tree_exiting.connect(_write_trace)''')
    script = script.replace('    $FloorLight.modulate.a = maxf(0.0,1.0-float(age)/maxf(1.0,float(config.floor_frames)))', '''    var light_t: float = clampf(float(age)/float(config.floor_frames),0.0,1.0)
    $FloorLight.modulate.a = float(config.fire_layers.floor_light.alpha) * pow(1.0-light_t,2.0)''')
    # After key-state selection so only the expanded painting owns the halo.
    marker = '    if age >= residue_end:\n        hide()'
    clock = '''    var peak: bool = trace[-1].get("key_state", "") == "expanded"
    var glow: Dictionary = config.fire_layers.glow.peak if peak else config.fire_layers.glow
    $Art/Glow.visible = peak or (age < flight_start and bool(config.glow_enabled))
    $Art/Glow.modulate.a = float(glow.alpha)
    $Art/Glow.scale = Vector2.ONE * float(glow.scale)
    if peak:
        $Art/Glow.texture = $Art/Key_expanded.texture
        $Art/Glow.offset = $Art/Key_expanded.offset
    trace[-1]["floor_alpha"] = $FloorLight.modulate.a
    trace[-1]["floor_seconds"] = float(age)/60.0
    trace[-1]["glow_alpha"] = $Art/Glow.modulate.a
    trace[-1]["glow_scale"] = $Art/Glow.scale.x
    trace[-1]["peak_halo"] = peak
    if age >= residue_start and not has_meta("embers_started") and config.has("embers"):
        set_meta("embers_started", true)
        var motes = load("res://scripts/vfx_fire_motes.gd").acquire(get_parent())
        motes.start_residue(config.embers,config.palette,int(config.seed),global_position,float(config.residue_frames)/60.0)
'''
    return script.replace(marker,clock+marker)


FIRE_MOTES_SCRIPT = r'''extends Node2D
# Bounded per-effect pool; all ages are integer physics ticks, never scaled delta.
static var trace: Array = []
var busy: bool = false
var emitting: bool = false
var source_point := Vector2.ZERO
var clock_start: int = 0
var mode: String = ""
var settings: Dictionary = {}
var palette: Array = []
var slots: Array = []
var births: int = 0
var total: int = 0
var duration: float = 0.0
var rng := RandomNumberGenerator.new()
var puff: Sprite2D
var floor_disc: Polygon2D

static func acquire(parent: Node2D) -> Node2D:
    for node in parent.get_tree().get_nodes_in_group("fire_mote_pool"):
        if node.get_parent() == parent and not node.busy: return node
    var node := Node2D.new()
    node.set_script(load("res://scripts/vfx_fire_motes.gd"))
    parent.add_child(node)
    node.add_to_group("fire_mote_pool")
    return node

func begin(kind: String) -> void:
    mode = kind
    busy = true
    emitting = true
    clock_start = Engine.get_physics_frames()
    births = 0
    top_level = true
    global_transform = Transform2D.IDENTITY
    show()
    set_physics_process(true)
    for item in slots: item.node.hide(); item.live = false
    if puff != null: puff.hide()
    if floor_disc != null: floor_disc.hide()

func start_trail(data: Dictionary, colours: Array, seed_value: int) -> void:
    begin("trail")
    settings = data; palette = colours; rng.seed = seed_value

func start_residue(data: Dictionary, colours: Array, seed_value: int, point: Vector2, seconds: float) -> void:
    begin("residue")
    settings=data; palette=colours; rng.seed=seed_value
    source_point=point; duration=seconds
    total=rng.randi_range(int(data.count[0]),int(data.count[1]))
    trace.append({"kind":"residue_start","count":total,"duration_s":duration})

func start_cast(config: Dictionary, socket: Vector2, feet: Vector2, aim: Vector2) -> void:
    begin("cast")
    settings = config.fire_layers.cast
    if settings.has("muzzle_puff"):
        if puff == null: puff=Sprite2D.new(); add_child(puff)
        puff.texture=load(config.painted_travel.head.png)
        puff.material=load(config.painted_travel.head.material).duplicate()
        var shader: Shader = puff.material.shader.duplicate()
        shader.code=shader.code.replace("blend_mix", "blend_add")
        puff.material.shader=shader
        puff.centered=false
        var rear: Array=config.painted_travel.head.rear_socket
        puff.offset=-Vector2(rear[0],rear[1])
        puff.scale=Vector2.ONE * float(config.painted_travel.head.scale) * float(settings.muzzle_puff.scale)
        puff.rotation=aim.angle(); puff.position=socket; puff.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
    if settings.has("floor_light"):
        if floor_disc == null:
            floor_disc=Polygon2D.new(); add_child(floor_disc)
            var additive:=CanvasItemMaterial.new(); additive.blend_mode=CanvasItemMaterial.BLEND_MODE_ADD; floor_disc.material=additive
        var polygon:=PackedVector2Array()
        for i in 48: polygon.append(Vector2(cos(TAU*i/48.0),sin(TAU*i/48.0)*.6)*130.0*float(settings.floor_light.radius_bh))
        floor_disc.polygon=polygon; floor_disc.position=feet; floor_disc.z_index=-3
        var c:Array=config.palette[2]; floor_disc.color=Color(c[0],c[1],c[2],1)
    _tick(0)

func _physics_process(_delta: float) -> void:
    if busy: _tick(roundi(float(Engine.get_physics_frames()-clock_start)*60.0/Engine.physics_ticks_per_second))

func _birth(tick: int) -> void:
    var slot: Dictionary = {}
    for item in slots:
        if not item.live: slot=item; break
    var cap: int=8 if mode=="trail" else 12
    if slot.is_empty():
        if slots.size()>=cap: return
        var node:=Polygon2D.new(); add_child(node)
        var additive:=CanvasItemMaterial.new(); additive.blend_mode=CanvasItemMaterial.BLEND_MODE_ADD; node.material=additive
        slot={"node":node,"live":false}; slots.append(slot)
    var size: float=rng.randf_range(settings.size_px[0],settings.size_px[1])
    slot.node.polygon=PackedVector2Array([Vector2(-size/2,0),Vector2(0,-size/2),Vector2(size/2,0),Vector2(0,size/2)])
    var band: int=2 if mode=="trail" else settings.bands[rng.randi_range(0,1)]
    var c:Array=palette[band];slot.node.color=Color(c[0],c[1],c[2],1)
    slot.life=float(settings.life_s) if mode=="trail" else rng.randf_range(settings.life_s[0],settings.life_s[1])
    slot.life = floor(float(slot.life)*60.0)/60.0
    slot.tick=tick;slot.origin=source_point;slot.phase=rng.randf_range(0,TAU);slot.live=true;slot.id=births
    slot.node.show(); births+=1
    trace.append({"kind":"birth","mode":mode,"id":slot.id,"tick":tick,"life_s":slot.life,"size_px":size,"band":band,"position":[source_point.x,source_point.y]})

func _tick(tick: int) -> void:
    var seconds: float=float(tick)/60.0
    if mode=="cast":
        var end: int=0
        if settings.has("muzzle_puff"):
            end=maxi(end,int(settings.muzzle_puff.frames));puff.visible=tick<int(settings.muzzle_puff.frames)
            puff.modulate.a=maxf(0,1.0-float(tick)/float(settings.muzzle_puff.frames))
        if settings.has("floor_light"):
            end=maxi(end,int(settings.floor_light.frames));floor_disc.visible=tick<int(settings.floor_light.frames)
            floor_disc.modulate.a=float(settings.floor_light.alpha)*maxf(0,1.0-float(tick)/float(settings.floor_light.frames))
        trace.append({"kind":"cast","tick":tick,"puff_alpha":puff.modulate.a if puff!=null else 0,"floor_alpha":floor_disc.modulate.a if floor_disc!=null else 0})
        if tick>=end: finish()
        return
    var live: int=0
    for item in slots:
        if not item.live: continue
        var age: float=float(tick-int(item.tick))/60.0
        if age>=float(item.life):
            item.live=false;item.node.hide()
            trace.append({"kind":"death","mode":mode,"id":item.id,"tick":tick,"age_s":age,"life_s":item.life})
            continue
        item.node.position=item.origin+Vector2(float(settings.lateral_px)*(sin(item.phase+age*8)-sin(item.phase))*.5,-float(settings.rise_px_s)*age)
        item.node.modulate.a=1.0-age/float(item.life); live+=1
    var target: int=mini(total,int(floor(seconds/duration*total))+1) if mode=="residue" else int(floor(seconds*float(settings.rate_per_s)))
    if emitting and (mode!="residue" or seconds<duration):
        while births<target:
            var before: int=births
            _birth(tick)
            if births==before: break
    live=0
    for item in slots:
        if item.live: live+=1
    trace.append({"kind":"pool","mode":mode,"tick":tick,"live":live,"births":births})
    if mode=="residue" and seconds>=duration: emitting=false
    if not emitting and live==0: finish()

func finish() -> void:
    busy=false;emitting=false;hide();set_physics_process(false)
'''




# R-C5-99 FL-3. Runtime additions are emitted only for explicit opt-in fields.
def _emit_anti_decal(out, kit, resource_root, scene, runtime, config, script):
    import numpy as np
    from PIL import ImageFilter
    data = kit['effect']
    runtime['anti_decal'] = {key: data['layers'][key] for key in ('core', 'shimmer') if key in data['layers']}
    if 'boil' in config:
        runtime['anti_decal']['boil'] = config['boil']
    runtime['anti_decal']['noise_texture'] = 'res://'+runtime['erosion_noise_texture']
    runtime['anti_decal']['palette_2'] = data['material']['palette'][2]
    if 'core' in runtime['anti_decal']:
        # Derived masks only: preserve source PNG bytes and filter band 3 before
        # blurring coverage. Padding is transparent; no colour from lower bands.
        root = kit['root']/Path(config['source']).parent
        record = json.loads((kit['root']/config['source']).read_text())
        sources = ['pieces/'+record['peak_index']] + ['pieces/'+p['mask'] for p in record['pieces']]
        sources += [s['png'] for s in config.get('key_states', [])]
        if 'interleave' in config:
            from export.effect_kit import load_interleave
            _, tongues = load_interleave(config['interleave'], kit['root'])
            sources += list(tongues)
        masks = {}
        for i, relative in enumerate(dict.fromkeys(sources)):
            source = out/resource_root/relative
            rgba = np.array(Image.open(source).convert('RGBA'))
            alpha = np.where(rgba[...,0] >= 213, rgba[...,3], 0).astype(np.uint8)
            blurred = Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(float(data['layers']['core']['blur_px'])))
            result = Image.new('RGBA', blurred.size, (255,255,255,0)); result.putalpha(blurred)
            destination = resource_root+f'/core/mask_{i:03d}.png'
            (out/destination).parent.mkdir(parents=True, exist_ok=True); result.save(out/destination)
            masks['res://'+resource_root+'/'+relative] = 'res://'+destination
        runtime['anti_decal']['core_textures'] = masks
    if 'shimmer' in runtime['anti_decal']:
        shader = resource_root+'/materials/heat_shimmer.gdshader'
        (out/shader).write_text(HEAT_SHIMMER_SHADER)
        runtime['anti_decal']['shimmer_shader'] = 'res://'+shader
        runtime['anti_decal']['distance_texture'] = 'res://'+resource_root+'/pieces/whole_body_distance.png'
    script = script.replace('    tree_exiting.connect(_write_trace)', '    _ready_anti_decal()\n    tree_exiting.connect(_write_trace)')
    marker = '    if age >= residue_end:\n        hide()'
    script = script.replace(marker, '    _clock_anti_decal(age, residue_start, residue_end)\n'+marker)
    return scene, script + ANTI_DECAL_SCRIPT


HEAT_SHIMMER_SHADER = r'''shader_type canvas_item;
render_mode blend_add, unshaded;
// Compatibility-safe light only; never reads the framebuffer.
uniform sampler2D erosion_noise_texture : filter_linear, repeat_enable;
uniform sampler2D distance_texture : filter_linear, repeat_disable;
uniform vec4 band_2 : source_color = vec4(1.0, 0.55, 0.12, 1.0);
uniform float amplitude_px = 3.0;
uniform float age_s = 0.0;
uniform float residue_erode = 0.8;
uniform float residue_fade = 0.0;
float boil(vec2 p) {
    return (texture(erosion_noise_texture,p).r + 0.5*texture(erosion_noise_texture,p*2.0+vec2(0.37,0.19)).r)/1.5;
}
void fragment() {
    vec2 p = UV + vec2(0.0,age_s*0.35);
    vec2 shift = vec2(boil(p),boil(p+vec2(0.31,0.13)))*2.0-1.0;
    vec2 uv = p + shift * TEXTURE_PIXEL_SIZE * amplitude_px * clamp(residue_fade,0.0,1.0);
    float mask = texture(TEXTURE,UV).a * step(texture(distance_texture,UV).r,1.0-residue_erode);
    float alpha = clamp(0.12 * mask * boil(uv) * residue_fade, 0.0, 0.12);
    COLOR = vec4(band_2.rgb, alpha);
}
'''


ANTI_DECAL_SCRIPT = r'''
var core_pairs: Array = []
var heat_quad: Sprite2D
func _ready_anti_decal() -> void:
    var opts: Dictionary = config.anti_decal
    if opts.has("core"):
        var core := Node2D.new()
        core.name = "Core"
        var add := CanvasItemMaterial.new()
        add.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
        core.material = add
        $Art.add_child(core)
        var sources: Array = [$Art/Peak]
        for key in config.get("key_states", []): sources.append(get_node("Art/Key_"+str(key.state)))
        for piece in pieces:
            sources.append(piece.paint)
            sources.append(piece.root)
        for source in sources:
            var paint := Sprite2D.new()
            paint.name = "Core_"+str(core_pairs.size())
            paint.texture = load(opts.core_textures[source.texture.resource_path])
            paint.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
            paint.centered = source.centered
            paint.offset = source.offset
            paint.material = source.material.duplicate()
            var shader := Shader.new()
            shader.code = source.material.shader.code.replace("blend_mix", "blend_add")
            if not "uniform sampler2D erosion_noise_texture" in shader.code:
                shader.code = shader.code.replace("uniform bool dark_duplicate", "uniform sampler2D erosion_noise_texture : filter_linear, repeat_enable;\nuniform bool dark_duplicate")
            shader.code = shader.code.replace("COLOR = vec4(rgb, coverage);", "COLOR = vec4(rgb, coverage * (0.85 + 0.15 * texture(erosion_noise_texture, UV).r));")
            paint.material.shader = shader
            paint.material.set_shader_parameter("erosion_noise_texture", load(opts.noise_texture))
            paint.material.set_shader_parameter("dark_duplicate", false)
            core.add_child(paint)
            core_pairs.append({"source":source,"paint":paint})
    if opts.has("shimmer"):
        var peak: Sprite2D = $Art/Peak
        heat_quad = Sprite2D.new()
        heat_quad.name = "HeatShimmer"
        heat_quad.texture = peak.texture
        heat_quad.centered = peak.centered
        heat_quad.offset = peak.offset
        heat_quad.z_index = 3
        heat_quad.material = ShaderMaterial.new()
        heat_quad.material.shader = load(opts.shimmer_shader)
        heat_quad.material.set_shader_parameter("distance_texture", load(opts.distance_texture))
        heat_quad.material.set_shader_parameter("erosion_noise_texture", load(opts.noise_texture))
        var tint: Array = opts.palette_2
        heat_quad.material.set_shader_parameter("band_2", Color(tint[0],tint[1],tint[2],tint[3]))
        heat_quad.material.set_shader_parameter("amplitude_px", float(opts.shimmer.amplitude_px))
        $Art.add_child(heat_quad)

func _clock_anti_decal(age: int, residue_start: int, residue_end: int) -> void:
    var opts: Dictionary = config.anti_decal
    var row: Dictionary = trace[-1]
    var key: String = row.get("key_state", "")
    var fade: float = clampf(1.0-float(age-residue_start)/maxf(1.0,float(residue_end-residue_start)),0.0,1.0)
    if opts.has("boil") and key != "":
        var boil: Dictionary = opts.boil
        var uv := Vector2(0.0, -float(age)/60.0*float(boil.uv_per_s))
        var oscillation: float = float(boil.erode_amp)*sin(TAU*float(boil.hz)*float(age)/60.0)
        var erosion: float = clampf(float(row.key_erode)+oscillation,0.0,1.0)
        for suffix in ["", "Dark"]:
            var material: ShaderMaterial = get_node("Art/Key_"+key+suffix).material
            material.set_shader_parameter("noise_uv_offset", uv)
            material.set_shader_parameter("erode", erosion)
        row["boil_uv"] = [uv.x,uv.y]
        row["boil_erode"] = erosion
        row["boil_delta"] = oscillation
    if opts.has("core"):
        var alpha: float = float(opts.core.alpha)*fade
        $Art/Core.modulate.a = alpha
        var count: int = 0
        for pair in core_pairs:
            var source: Sprite2D = pair.source
            var paint: Sprite2D = pair.paint
            paint.global_transform = source.global_transform
            paint.visible = (source.is_visible_in_tree() or (source == $Art/Peak and stage == "onset")) and age < residue_end
            for uniform in ["erode", "dissolve", "noise_uv_offset"]:
                var value: Variant = source.material.get_shader_parameter(uniform)
                if value != null: paint.material.set_shader_parameter(uniform,value)
            if paint.visible: count += 1
        row["core_alpha"] = alpha
        row["core_additive"] = $Art/Core.material.blend_mode == CanvasItemMaterial.BLEND_MODE_ADD
        row["core_draws"] = count
    if is_instance_valid(heat_quad):
        var seconds: float = float(age-residue_start)/60.0
        var heat_fade: float = minf(fade,clampf(1.0-seconds/float(opts.shimmer.seconds),0.0,1.0)) if seconds >= 0.0 else 0.0
        heat_quad.visible = heat_fade > 0.0
        heat_quad.material.set_shader_parameter("age_s", maxf(0.0,seconds))
        heat_quad.material.set_shader_parameter("residue_fade", heat_fade)
        heat_quad.material.set_shader_parameter("residue_erode", float(config.residue_erode))
        row["shimmer_alpha"] = 0.12*heat_fade
        row["shimmer_noise_texture"] = heat_quad.material.get_shader_parameter("erosion_noise_texture").resource_path
        row["shimmer_amplitude_px"] = float(opts.shimmer.amplitude_px)*heat_fade
        row["shimmer_age_s"] = seconds
'''


CONTACT_LIGHT_SCRIPT = r'''extends Node
# One composition owner prevents competing tweens. The .15-s band-3 victim
# tint is applied AFTER the band-2 contact light and therefore keeps priority.
static var trace: Array = []
var victim: CanvasItem
var previous: Color
var band2: Color
var band3: Color
var settings: Dictionary
var victim_tint: bool = false
var age: int = 0
var dark: Node2D
var dark_origin: Vector2
var away: Vector2
var body_index: int
func start(area: CollisionObject2D, impact: Vector2, config: Dictionary) -> void:
    victim = area
    var prop: Node = area.get_parent().get_node_or_null("Prop_"+String(area.name).trim_prefix("VfxTarget_"))
    if prop is CanvasItem: victim = prop
    # Repeated contacts restore the original state before handing ownership on.
    for old in get_tree().get_nodes_in_group("vfx_body_light"):
        if old != self and old.victim == victim: old.finish()
    add_to_group("vfx_body_light")
    previous = victim.modulate
    settings = config.fire_layers.contact_light
    var p2: Array = config.palette[2]
    var p3: Array = config.palette[3]
    band2 = Color(p2[0],p2[1],p2[2],previous.a)
    band3 = Color(p3[0],p3[1],p3[2],previous.a)
    victim_tint = "victim_tint" in config.enabled_layers
    body_index = int(area.get_meta("body_index", -1))
    dark = victim.get_node_or_null("DarkDuplicate")
    if dark == null: dark = victim.get_parent().get_node_or_null(String(victim.name)+"DarkDuplicate")
    away = (area.global_position-impact).normalized()
    if away.is_zero_approx(): away = Vector2.RIGHT
    if is_instance_valid(dark): dark_origin = dark.global_position
    sample()
func _physics_process(_delta: float) -> void:
    age += 1
    sample()
    if age >= maxi(int(settings.frames),9 if victim_tint else 0): finish()
func sample() -> void:
    if not is_instance_valid(victim): queue_free(); return
    var weight: float = float(settings.lerp)*pow(clampf(1.0-float(age)/float(settings.frames),0.0,1.0),2.0)
    var tint_weight: float = clampf(1.0-float(age)/9.0,0.0,1.0) if victim_tint else 0.0
    victim.modulate = previous.lerp(band2,weight).lerp(band3,tint_weight)
    if is_instance_valid(dark): dark.global_position = dark_origin + away*4.0*clampf(1.0-float(age)/float(settings.frames),0.0,1.0)
    trace.append({"age":age,"body_index":body_index,"modulate":[victim.modulate.r,victim.modulate.g,victim.modulate.b,victim.modulate.a],"contact_weight":weight,"victim_weight":tint_weight,"dark_offset_px":dark.global_position.distance_to(dark_origin) if is_instance_valid(dark) else 0.0})
func finish() -> void:
    if is_instance_valid(victim): victim.modulate = previous
    if is_instance_valid(dark): dark.global_position = dark_origin
    remove_from_group("vfx_body_light")
    set_physics_process(false)
    queue_free()
'''


# FL-4a opt-in adapters. Existing emitted scripts (including ice) retain bytes.
def _fl4_burst_script(script):
    return (script.replace('var expansion_end: int = flight_start + 15', 'var expansion_end: int = int(config.timing.erosion_age)')
            .replace('var residue_start: int = expansion_end + 21', 'var residue_start: int = int(config.timing.paint_end_age)')
            .replace('float(age-flight_start)/15.0', 'float(age-flight_start)/float(int(config.timing.expanded_age)-flight_start)')
            .replace('var ease: float = 1.0-pow(1.0-flight_t,3.0)', 'var ease: float = flight_t * flight_t')
            .replace('float(age-expansion_end)/21.0', 'float(age-expansion_end)/float(residue_start-expansion_end)')
            .replace('/float(config.residue_frames)', '/maxf(1.0,float(config.residue_frames))'))


def _write_living_ember_assets(out):
    from export.props_layer import GLOW_FLICKER_SCRIPT
    # Same source files as the scene props. Never synthesize replacement art.
    source = Path(__file__).resolve().parents[1]/'runs/C-5/artifacts/CS-props-v25/fx'
    target = out/'vfx/fire_ending/fx'; target.mkdir(parents=True, exist_ok=True)
    for name in ('ember_1.png', 'glow.png'): shutil.copyfile(source/name,target/name)
    (out/'scripts/vfx/glow_flicker_fl4.gd').write_text(GLOW_FLICKER_SCRIPT)


EMBER_ENDING_SCRIPT = r'''
var ending_sparks: Array = []
var ending_glow: Sprite2D
var ending_core: Sprite2D
var ending_births: Array = []
func _ready_ember_ending() -> void:
    var opts: Dictionary = config.ember_ending
    var rng := RandomNumberGenerator.new()
    rng.seed = int(config.seed)
    var add := CanvasItemMaterial.new()
    add.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
    for i in int(opts.amount):
        var sprite := Sprite2D.new()
        sprite.name = "CrackEmber_%02d" % i
        sprite.texture = load("res://vfx/fire_ending/fx/ember_1.png")
        sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
        sprite.material = add
        sprite.hide()
        add_child(sprite)
        var birth: int = 20 + int(floor(float(i)*30.0/float(int(opts.amount)-1)))
        # A late birth samples only lifetimes fitting the registered total cap.
        var life: int = int(floor(rng.randf_range(float(opts.life_s[0])*60.0,minf(float(opts.life_s[1])*60.0,114-birth))))
        var origin := Vector2(rng.randf_range(-.5,.5)*float(opts.rect_bh[0])*130.0,rng.randf_range(-.5,.5)*float(opts.rect_bh[1])*130.0)
        var velocity: Vector2 = Vector2.UP.rotated(deg_to_rad(rng.randf_range(-28,28))) * rng.randf_range(opts.speed_px_s[0],opts.speed_px_s[1])
        ending_sparks.append({"node":sprite,"birth":birth,"life":life,"origin":origin,"velocity":velocity,"scale":rng.randf_range(opts.scale[0],opts.scale[1]),"angular":rng.randf_range(-90,90),"born":false})
    ending_glow = Sprite2D.new()
    ending_glow.name = "GlowFlicker"
    ending_glow.texture = load("res://vfx/fire_ending/fx/glow.png")
    ending_glow.material = add
    ending_glow.modulate = Color(1,.45,.12,float(opts.glow_alpha))
    ending_glow.scale = Vector2(1,.5) * (2.0*130.0*float(opts.glow_radius_bh)/ending_glow.texture.get_width())
    ending_glow.set_script(load("res://scripts/vfx/glow_flicker_fl4.gd"))
    ending_glow.flicker_hz = 4.7
    ending_glow.flicker_amount = .35
    ending_glow.phase_seed = int(config.seed)
    add_child(ending_glow)
    ending_glow.set_process(false)
    ending_core = Sprite2D.new()
    ending_core.name = "WhiteHotAfterglow"
    ending_core.texture = ending_glow.texture
    ending_core.material = add
    ending_core.modulate = Color(1,.94,.75,1)
    ending_core.scale = Vector2.ONE*(2.0*130.0*float(opts.core_radius_bh)/ending_core.texture.get_width())
    add_child(ending_core)

func _clock_ember_ending(age: int) -> void:
    var opts: Dictionary = config.ember_ending
    var live: int = 0
    for spark in ending_sparks:
        var tick: int = age-int(spark.birth)
        if tick >= 0 and not spark.born:
            spark.born = true
            ending_births.append({"age":spark.birth,"life_frames":spark.life,"end_age":int(spark.birth)+int(spark.life)})
        spark.node.visible = tick >= 0 and tick < int(spark.life)
        if not spark.node.visible: continue
        live += 1
        var seconds: float = float(tick)/60.0
        var t: float = float(tick)/float(spark.life)
        spark.node.position = spark.origin + spark.velocity*seconds + Vector2(0,-8)*seconds*seconds*.5
        spark.node.rotation = deg_to_rad(float(spark.angular))*seconds
        spark.node.scale = Vector2.ONE*float(spark.scale)*lerpf(1,.3,t)
        spark.node.modulate = Color(1,.85,.5,1).lerp(Color(1,.25,.05,0),t)
    var t: float = clampf(float(age-22)/(60.0*float(opts.glow_s)),0,1)
    var envelope: float = float(opts.glow_alpha)*pow(1.0-t,2.0) if age >= 22 else 0.0
    ending_glow.base_alpha = envelope
    ending_glow.elapsed = float(age-22)/60.0
    ending_glow._process(0.0)
    ending_glow.visible = envelope > 0
    ending_core.modulate.a = pow(clampf(1.0-float(age-22)/(60.0*float(opts.core_s)),0,1),2.0) if age >= 22 else 0.0
    ending_core.visible = ending_core.modulate.a > 0
    # The complete painted subtree leaves at the spent hold's exclusive end.
    $Art.visible = age < int(config.timing.paint_end_age)
    var row: Dictionary = trace[-1]
    row["painted_subtree_visible"] = $Art.visible
    row["painted_pixels_upper_bound"] = -1 if $Art.visible else 0
    row["ember_births"] = ending_births.size()
    row["live_embers"] = live
    row["ending_glow_envelope"] = envelope
    row["ending_glow_alpha"] = ending_glow.modulate.a
    row["afterglow_alpha"] = ending_core.modulate.a
    row["ending_additive"] = ending_core.material.blend_mode == CanvasItemMaterial.BLEND_MODE_ADD
'''


def _write_fl4_travel(out, kit, resource_root):
    import numpy as np
    from PIL import ImageFilter
    opts = kit['effect']['layers']['travel']
    head = kit['effect']['travel_primitives']['head']
    rgba = np.array(Image.open(kit['root']/head['png']).convert('RGBA'))
    alpha = Image.fromarray(np.where(rgba[...,0] == 255,rgba[...,3],0).astype(np.uint8)).filter(ImageFilter.GaussianBlur(opts['core']['blur_px']))
    mask = Image.new('RGBA',alpha.size,(255,255,255,0));mask.putalpha(alpha)
    mask.save(out/resource_root/'primitives/head_core.png')
    scene = G1_SCENE.replace('res://scripts/vfx_g1.gd','res://scripts/vfx_g1_fl4.gd')
    for name in ('Streak','KeyState','DarkHead','DarkStreak','DarkKey','CastHalo'):
        scene += '\n[node name="'+name+'" type="Sprite2D" parent="."]\ntexture_filter = 2\nvisible = false\nz_index = '+str(-2 if name.startswith('Dark') else -1 if name in ('Streak','CastHalo') else 0)+'\n'
    (out/'scenes/vfx/g1_fl4_projectile.tscn').write_text(scene)
    script = PAINTED_G1_SCRIPT.replace('res://scripts/vfx_fire_motes.gd','res://scripts/vfx_fire_motes_fl4.gd')
    script = script.replace('    _paint_clock(0)', '    _ready_flight_light()\n    _paint_clock(0)')
    script = script.replace('    _dark_copy($DarkHead, $Head, rest_head)', '    _clock_flight_light(age)\n    _dark_copy($DarkHead, $Head, rest_head)')
    script = script.replace('func _physics_process(delta: float) -> void:\n', 'func _physics_process(delta: float) -> void:\n    if is_instance_valid(flight_core) and not active: _clock_flight_light(age_frames())\n')
    script = script.replace('trail_motes.source_point = global_position + socket.rotated(direction.angle())', 'trail_motes.source_point = global_position + socket.rotated(direction.angle()) + Vector2(float(config.sheet_tail[0]), float(config.sheet_tail[1])).rotated(direction.angle())')
    script += FLIGHT_LIGHT_SCRIPT + FL4B_CONTACT_SCRIPT
    script = _fl5_eruption_script(script)
    (out/'scripts/vfx_g1_fl4.gd').write_text(script)
    motes = FIRE_MOTES_SCRIPT.replace('res://scripts/vfx_fire_motes.gd','res://scripts/vfx_fire_motes_fl4.gd')
    motes = motes.replace('var band: int=2 if mode=="trail" else settings.bands[rng.randi_range(0,1)]','var band: int=settings.get("bands",[2,2])[rng.randi_range(0,1)] if mode=="trail" else settings.bands[rng.randi_range(0,1)]')
    (out/'scripts/vfx_fire_motes_fl4.gd').write_text(motes)


FLIGHT_LIGHT_SCRIPT = r'''
var flight_core: Sprite2D
var flight_halo: Sprite2D
var flight_smear: Line2D
func _ready_flight_light() -> void:
    if is_instance_valid(flight_core): flight_core.queue_free(); flight_halo.queue_free(); flight_smear.queue_free()
    var add := CanvasItemMaterial.new()
    add.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
    flight_core = Sprite2D.new()
    flight_core.name = "FlightCore"
    flight_core.material = add
    flight_core.texture = load(str(config.painted_travel.head.png).get_base_dir()+"/head_core.png")
    flight_core.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
    flight_core.centered = false
    flight_core.offset = $Head.offset
    flight_core.modulate = Color(1,.94,.75,1)
    add_child(flight_core)
    flight_halo = flight_core.duplicate()
    flight_halo.name = "FlightHalo"
    flight_halo.modulate = Color(1,.55,.12,1)
    flight_halo.z_index = -1
    add_child(flight_halo)
    flight_smear = Line2D.new()
    flight_smear.name = "MotionSmear"
    flight_smear.material = add
    flight_smear.width = 14
    var gradient := Gradient.new()
    var tint: Array = config.palette[int(config.fire_layers.travel.smear.band)]
    gradient.set_color(0,Color(tint[0],tint[1],tint[2],0))
    gradient.set_color(1,Color(tint[0],tint[1],tint[2],float(config.fire_layers.travel.smear.alpha)))
    flight_smear.gradient = gradient
    add_child(flight_smear)

func _clock_flight_light(age: int) -> void:
    var opts: Dictionary = config.fire_layers.travel
    var seconds: float = float(age)/60.0
    var pulse: float = lerpf(1.0,float(opts.core.pulse_scale),.5+.5*sin(TAU*float(opts.core.hz)*seconds))
    flight_core.transform = $Head.transform
    flight_core.scale *= pulse
    flight_core.modulate.a = float(opts.core.alpha)
    flight_core.visible = active
    flight_halo.transform = $Head.transform
    flight_halo.scale *= float(opts.halo.scale)
    flight_halo.modulate.a = float(opts.halo.alpha)
    flight_halo.visible = active
    var uv := Vector2(seconds*float(opts.boil.uv_per_s),0)
    var erode: float = .1 + float(opts.boil.erode_amp)*sin(TAU*float(opts.boil.hz)*seconds)
    $Streak.material.set_shader_parameter("noise_uv_offset",uv)
    $Streak.material.set_shader_parameter("erode",erode)
    flight_smear.points = PackedVector2Array([-direction*130.0*float(opts.smear.length_bh),Vector2.ZERO])
    flight_smear.modulate.a = 1.0 if active else clampf(1.0-float(age-stop_age)/float(opts.smear.frames),0,1)
    flight_smear.visible = flight_smear.modulate.a > 0
    if not fire_trace.is_empty():
        var row: Dictionary = fire_trace[-1]
        row["core_additive"] = flight_core.material.blend_mode == CanvasItemMaterial.BLEND_MODE_ADD
        row["core_alpha"] = flight_core.modulate.a
        row["core_scale"] = pulse
        row["trail_rate"] = opts.trail.rate_per_s
        var actual_uv: Vector2 = $Streak.material.get_shader_parameter("noise_uv_offset")
        row["streak_uv"] = [actual_uv.x,actual_uv.y]
        row["streak_erode"] = $Streak.material.get_shader_parameter("erode")
        row["noise_uv_consumed"] = "UV * noise_uv_scale + noise_uv_origin - noise_uv_offset" in $Streak.material.shader.code
        row["noise_bound"] = $Streak.material.get_shader_parameter("erosion_noise_texture") != null
        row["head_extent_bh"] = config.head_extent_bh
        row["sheet_extent_bh"] = config.sheet_extent_bh * $Streak.scale.x / float(config.painted_travel.streak.scale)
        var rear := Vector2(config.painted_travel.head.rear_socket[0],config.painted_travel.head.rear_socket[1])
        row["attachment_error_px"] = $Streak.global_position.distance_to($Head.to_global(rear+$Head.offset))
        row["sheet_tail_world"] = [trail_motes.source_point.x,trail_motes.source_point.y] if is_instance_valid(trail_motes) else []
'''



def _fl4b_travel_metrics(kit):
    import numpy as np
    data = kit['effect']
    result = {}
    for role in ('head','streak'):
        item = data['travel_primitives'][role]
        with Image.open(kit['root']/item['png']) as image: a = np.asarray(image.convert('RGBA'))
        # Literal drawn support remains alpha > 0. The supplied dimensions
        # describe alpha > 8; report that second measurement without using it
        # to replace the literal trace or dropping any painted alpha.
        ys,xs = np.nonzero(a[:,:,3] > 0)
        result['head_extent_bh' if role=='head' else 'sheet_extent_bh'] = float(xs.max()-xs.min()+1)*item['scale']/130
        ys,xs = np.nonzero(a[:,:,3] > 8)
        result[role+'_body_extent_bh'] = float(xs.max()-xs.min()+1)*item['scale']/130
        if role == 'streak':
            left = xs == xs.min()
            tail = [float(xs.min()),float(ys[left].mean())]
            result['sheet_tail'] = [(tail[i]-item['pivot'][i])*item['scale'] for i in (0,1)]
    result['extent_alpha_threshold'] = 0
    result['body_alpha_threshold'] = 8
    return result


def _interleave_nodes(out, kit, resource_root, scene, runtime, geometry, config):
    import numpy as np
    from export.effect_kit import load_interleave, interleave_gaps
    library, assets = load_interleave(config['interleave'], kit['root'])
    base = json.loads((kit['root']/config['source']).read_text())
    runtime['interleave'] = dict(config['interleave'], gaps=interleave_gaps(base), seed_rule='effect_id XOR contact_frame XOR world_random')
    for item in library['pieces']:
        ident = 1000+item['id']; name = 'Piece_%03d' % ident
        relative = config['interleave']['library']+'/'+item['png']
        target = out/resource_root/relative; target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(kit['root']/relative,target)
        with Image.open(target) as image: a=np.asarray(image.convert('RGBA'))
        yy,xx=np.indices(a.shape[:2]);radius=np.hypot(xx-item['pivot'][0],yy-item['pivot'][1])
        field=resource_root+'/distance/interleave/'+item['png'];(out/field).parent.mkdir(parents=True,exist_ok=True)
        Image.fromarray(np.rint(np.clip(radius/max(1,radius[a[:,:,3]>0].max()),0,1)*255).astype(np.uint8)).save(out/field)
        geometry['pieces'].append(dict(item,id=ident,library_id=item['id'],mask='interleave/'+item['png'],root=item['pivot'],
                                       core=False,animated=True,interleave=True,axis_radians=math.radians(item['radial_angle_deg']),interleave_field=field))
        ext = (f'[ext_resource type="Texture2D" path="res://{resource_root}/{relative}" id="T{name}"]\n'
               f'[ext_resource type="Material" path="res://{resource_root}/materials/Piece_{name}.tres" id="M{name}"]\n')
        first=scene.index('[node ');scene=scene[:first]+ext+scene[first:]
        scene+=f'\n[node name="{name}" type="Sprite2D" parent="Art/Pieces"]\nvisible = false\n'
    return scene


def _fl4b_burst_script(script):
    script=script.replace('    for item in config.pieces:', '    _seed_interleave()\n    for item in config.pieces:',1)
    script=script.replace('var flight_start: int = int(config.flash_frames) + int(config.hold_frames)', 'var flight_start: int = int(config.flash_frames)')
    script=script.replace('$Art/Peak.visible = stage == "hold"','$Art/Peak.visible = false')
    script=script.replace('$Art/PeakDark.visible = stage == "hold" and bool(config.dark_duplicate)','$Art/PeakDark.visible = false')
    script=script.replace('float(age-flight_start)/9.0','float(age-flight_start-int(config.hold_frames))/9.0')
    script=script.replace('        var root_drift_px:', '        var item_ease: float = ease * (.85 if item.get("interleave",false) else 1.0)\n        var root_drift_px:')
    script=script.replace('float(config.core_radius_px) * ease','float(config.core_radius_px) * item_ease')
    script=script.replace('float(item.rotation_deg)) * ease','float(item.rotation_deg)) * item_ease')
    script=script.replace('Vector2(lerpf(1.0,float(item.along),ease),lerpf(1.0,0.85,ease))','Vector2(lerpf(1.0,float(item.along),item_ease),lerpf(1.0,0.85,item_ease))')
    script=script.replace('        # Tips burn back first;', '        if item.get("interleave",false):\n            node.scale *= float(item.jitter_scale)\n            if bool(item.mirrored): node.scale.y *= -1\n        # Tips burn back first;')
    script=script.replace('root_sprite.visible = active','root_sprite.visible = active and not item.get("interleave",false)')
    script=script.replace('dark_root.visible = active','dark_root.visible = active and not item.get("interleave",false)')
    # The keyless pieces receive the existing boil uniforms before their additive
    # duplicates sample those uniforms. No key-state clocks are reintroduced.
    script=script.replace('    _clock_anti_decal(age, residue_start, residue_end)', '    _clock_interleave(age)\n    _clock_anti_decal(age, residue_start, residue_end)')
    return script + INTERLEAVE_SCRIPT


INTERLEAVE_SCRIPT = r'''
var interleave_seed: int
var tongue_selection: Array = []
func _interleave_sample(label: String) -> int:
    return (str(interleave_seed)+":"+label).sha256_text().substr(0,8).hex_to_int()
func _seed_interleave() -> void:
    interleave_seed = int(get_meta("interleave_seed", int(config.seed) ^ int(get_instance_id()) ^ int(Engine.get_physics_frames()) ^ int(randi()))) & 0x7fffffff
    config.seed = interleave_seed
    var library: Array = config.pieces.filter(func(p): return p.get("interleave",false))
    config.pieces = config.pieces.filter(func(p): return not p.get("interleave",false))
    library.sort_custom(func(a,b): return _interleave_sample("pick"+str(int(a.library_id))) < _interleave_sample("pick"+str(int(b.library_id))))
    var count: int = int(config.interleave.count[0]) + _interleave_sample("count") % 3
    var slots: Array = config.interleave.gaps.duplicate(true)
    for rank in range(count):
        var item: Dictionary = library[rank].duplicate(true)
        slots.sort_custom(func(a,b): return float(a.width_deg) > float(b.width_deg) if not is_equal_approx(float(a.width_deg),float(b.width_deg)) else float(a.start_deg) < float(b.start_deg))
        var gap: Dictionary = slots.pop_front()
        var limit: float = minf(12, maxf(0,40-float(gap.width_deg)/2))
        var jitter: float = (float(_interleave_sample("angle"+str(rank)))/4294967295.0*2-1)*limit
        var angle: float = fposmod(float(gap.start_deg)+float(gap.width_deg)/2+jitter,360)
        var left: float = float(gap.width_deg)/2+jitter
        slots.append({"start_deg":gap.start_deg,"width_deg":left})
        slots.append({"start_deg":angle,"width_deg":float(gap.width_deg)-left})
        var radius: float = float(config.core_radius_px)*.9*1.1
        var root := Vector2.RIGHT.rotated(deg_to_rad(angle))*radius
        item.root = [float(config.centre[0])+root.x,float(config.centre[1])+root.y]
        item.axis_radians = deg_to_rad(angle)
        item.rotation_deg = 0.0
        item.jitter_scale = 1.2+.4*float(_interleave_sample("scale"+str(rank)))/4294967295.0
        item.mirrored = _interleave_sample("mirror"+str(rank)) % 2 == 1
        config.pieces.append(item)
        tongue_selection.append({"id":item.library_id,"gap_rank":rank,"angle_deg":angle,"jitter_deg":jitter,"scale":item.jitter_scale,"mirrored":item.mirrored,"speed_factor":.85,"root_radius_px":root.length()})
func _clock_interleave(age: int) -> void:
    var row: Dictionary = trace[-1]
    row["interleave_seed"] = interleave_seed
    row["tongues"] = tongue_selection
    if config.anti_decal.has("boil"):
        var boil: Dictionary = config.anti_decal.boil
        var uv := Vector2(0,-float(age)/60*float(boil.uv_per_s))
        var oscillation: float = float(boil.erode_amp)*sin(TAU*float(boil.hz)*float(age)/60)
        for part in pieces:
            for sprite in [part.paint,part.root]:
                sprite.material.set_shader_parameter("noise_uv_offset",uv)
                var erode: float = float(sprite.material.get_shader_parameter("erode"))
                sprite.material.set_shader_parameter("erode",clampf(erode+oscillation,0,1))
        row["boil_uv"] = [uv.x,uv.y]
'''


FL4B_CONTACT_SCRIPT = r'''
func _spawn_impact(strike_response: bool = true, point: Variant = null) -> void:
    var impact: Node2D = load(config.impact).instantiate()
    impact.set_meta("strike_response", strike_response)
    if str(config.impact).contains("fire_burst_e0p_v3"):
        var contact_frame: int = Engine.get_physics_frames()
        var world_random: int = randi()
        impact.set_meta("interleave_seed", (effect_id ^ contact_frame ^ world_random) & 0x7fffffff)
        impact.set_meta("cast_seed_inputs", {"effect_id":effect_id,"contact_frame":contact_frame,"world_random":world_random})
    if struck_ground != null: impact.set_meta("ground_anchor", struck_ground)
    impact.set("spell_scale", spell_scale)
    impact.set("caster", caster)
    impact.set("direction", direction)
    impact.position = get_parent().to_local(global_position if point == null else point)
    get_parent().add_child(impact)
'''



def _fl4c_burst_script(script):
    """R-C5-117: kit stretch and white-last burn-down, outside-in unchanged."""
    script = script.replace('lerpf(1.0,0.85,item_ease)', 'lerpf(1.0,float(config.stretch.across),item_ease)')
    script = script.replace('lerpf(1.0,float(item.along),item_ease)', 'lerpf(1.0,float(item.along),ease if item.get("interleave",false) else item_ease)')
    script = script.replace('var dissolve: float = 1.0 if age >= residue_end else 0.8 * residue_t',
                            'var dissolve: float = 1.0 if age >= residue_end else erosion_t')
    script = script.replace('set_shader_parameter("dissolve",0.0)', 'set_shader_parameter("dissolve",dissolve)')
    script = script.replace('"expanded_dissolve":0.0', '"expanded_dissolve":dissolve')
    # Keep the underlying dark copies on the same erosion samples, so they
    # cannot remain exposed where a boiling painted source has disappeared.
    script = script.replace('for sprite in [part.paint,part.root]:',
        'for sprite in [part.paint,part.root,part.dark_axis.get_node("Stretch/Piece_%03d" % int(part.record.id)),part.dark_root]:' )
    return script



# FL-5 adapters: no source painting or ice resource is changed.
def _fl5_eruption_script(script):
    script = script.replace('    _clock_flight_light(age)', '    _clock_eruption(age)\n    _clock_flight_light(age)', 1)
    script = script.replace('flight_core.modulate.a = float(opts.core.alpha)', 'flight_core.modulate.a = 1.0 if opts.has("eruption") and age < int(opts.eruption.frames) else float(opts.core.alpha)')
    script = script.replace('row["head_extent_bh"] = config.head_extent_bh', 'row["head_extent_bh"] = float(config.head_extent_bh) * $Head.scale.x / float(config.painted_travel.head.scale)\n        row["sheet_visible"] = $Streak.visible\n        row["eruption_scale"] = $Head.scale.x / float(config.painted_travel.head.scale)\n        row["head_world"] = [$Head.global_position.x,$Head.global_position.y]')
    return script + ERUPTION_SCRIPT


ERUPTION_SCRIPT = r'''
func _clock_eruption(age: int) -> void:
    var eruption: Dictionary = config.fire_layers.get("travel",{}).get("eruption",{})
    if eruption.is_empty(): return
    var t: float = clampf(float(age)/float(eruption.frames),0,1)
    var growth: float = lerpf(float(eruption.scale_from),1.0,1.0-pow(1.0-t,3.0))
    $Head.position = -direction * float($CollisionShape2D.shape.height) * (1.0-t)
    $Head.scale = Vector2.ONE * float(config.painted_travel.head.scale) * growth
    $KeyState.scale *= growth
    var rear := Vector2(config.painted_travel.head.rear_socket[0],config.painted_travel.head.rear_socket[1])
    $Streak.position = $Head.transform * (rear+$Head.offset)
    var delay: int = int(eruption.sheet_delay_frames)
    $Streak.visible = $Streak.visible and age >= delay
    var sheet_t: float = clampf(float(age-delay+1)/float(int(eruption.frames)-delay+1),0,1)
    $Streak.scale *= Vector2(sheet_t,growth)
    if is_instance_valid(trail_motes):
        trail_motes.source_point = global_position + $Streak.position + Vector2(float(config.sheet_tail[0])*sheet_t,float(config.sheet_tail[1])*growth).rotated(direction.angle())
'''


def _fl5_ending(out, kit, resource_root, runtime, config, geometry, script):
    import numpy as np
    from export.effect_kit import distance_field, write_vfx_material
    script = script.replace('rng.randf_range(-28,28)','rng.randf_range(-float(opts.get("spread_deg",28)),float(opts.get("spread_deg",28)))')
    script = script.replace('"end_age":int(spark.birth)+int(spark.life)}','"end_age":int(spark.birth)+int(spark.life),"origin":[spark.origin.x,spark.origin.y],"scale":spark.scale,"velocity":[spark.velocity.x,spark.velocity.y]}')
    for role in ('core_residue','smoke'):
        if role in config: runtime[role] = dict(config[role])
    if 'core_residue' in config:
        candidates = []
        for part in geometry['pieces']:
            if not part.get('core'): continue
            source = kit['root']/Path(config['source']).parent/part['mask']
            rgba = np.array(Image.open(source).convert('RGBA'))
            white = (rgba[...,0] == 255) & (rgba[...,3] > 0)
            candidates.append((int(white.sum()),part,rgba,white))
        _,part,rgba,white = max(candidates,key=lambda c:c[0])
        rgba[...,3] = np.where(white,rgba[...,3],0)
        ys,xs = np.nonzero(rgba[...,3])
        rel = resource_root+'/pieces/core_residue.png'
        Image.fromarray(rgba).save(out/rel)
        field = resource_root+'/pieces/core_residue_distance.png'
        Image.fromarray(distance_field(rgba)).save(out/field)
        mat = resource_root+'/materials/CoreResidue.tres'
        write_vfx_material(out,mat,dict(kit['effect']['material'],erode_outside_in=True,erode=0,dissolve=0),field)
        runtime['core_residue'].update(texture='res://'+rel,material='res://'+mat,
            pivot=[(float(xs.min())+float(xs.max()))/2,(float(ys.min())+float(ys.max()))/2],
            native_extent=int(max(xs.max()-xs.min()+1,ys.max()-ys.min()+1)),source_piece_id=part['id'])
    if 'smoke' in config:
        rel = resource_root+'/materials/ending_smoke.gdshader'
        (out/rel).write_text(ENDING_SMOKE_SHADER)
        runtime['smoke'].update(shader='res://'+rel,texture='res://'+runtime['erosion_noise_texture'])
    script = script.replace('    _ready_ember_ending()', '    _ready_ember_ending()\n    _ready_fl5_ending()')
    script = script.replace('    _clock_ember_ending(age)', '    _clock_ember_ending(age)\n    _clock_fl5_ending(age)')
    # The matching afterglow starts with the residue, at the spent frame.
    script = script.replace('float(age-22)/(60.0*float(opts.core_s))','float(age-int(config.timing.paint_end_age))/(60.0*float(opts.core_s))')
    script = script.replace('if age >= 22 else 0.0\n    ending_core.visible', 'if age >= int(config.timing.paint_end_age) else 0.0\n    ending_core.visible')
    return script + FL5_ENDING_SCRIPT


ENDING_SMOKE_SHADER = r'''shader_type canvas_item;
render_mode blend_mix, unshaded;
uniform vec4 smoke_tint : source_color = vec4(0.35,0.3,0.28,1.0);
void fragment() {
    float n = (texture(TEXTURE,UV).r + .5*texture(TEXTURE,fract(UV*2.0+vec2(.37,.19))).r)/1.5;
    float envelope = 1.0-smoothstep(.1,.5,length(UV-vec2(.5)));
    COLOR = vec4(smoke_tint.rgb,COLOR.a*n*envelope);
}
'''

FL5_ENDING_SCRIPT = r'''
var core_residue: Sprite2D
var ending_smoke: Sprite2D
func _ready_fl5_ending() -> void:
    if config.has("core_residue"):
        var opts: Dictionary = config.core_residue
        core_residue = Sprite2D.new()
        core_residue.name = "CoreResidue"
        core_residue.texture = load(opts.texture)
        core_residue.material = load(opts.material).duplicate()
        core_residue.centered = false
        core_residue.offset = -Vector2(opts.pivot[0],opts.pivot[1])
        core_residue.scale = Vector2.ONE * float(opts.scale_bh)*130.0/float(opts.native_extent)
        core_residue.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
        core_residue.z_index = -2
        add_child(core_residue)
    if config.has("smoke"):
        var opts: Dictionary = config.smoke
        ending_smoke = Sprite2D.new()
        ending_smoke.name = "EndingSmoke"
        ending_smoke.texture = load(opts.texture)
        ending_smoke.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
        var mat := ShaderMaterial.new()
        mat.shader = load(opts.shader)
        mat.set_shader_parameter("smoke_tint",Color(opts.tint[0],opts.tint[1],opts.tint[2],1))
        ending_smoke.material = mat
        ending_smoke.scale = Vector2.ONE * 2.0*float(opts.radius_bh)*130.0/ending_smoke.texture.get_width()
        ending_smoke.z_index = -1
        add_child(ending_smoke)
func _clock_fl5_ending(age: int) -> void:
    var seconds: float = float(age-int(config.timing.paint_end_age))/60.0
    var row: Dictionary = trace[-1]
    if is_instance_valid(core_residue):
        var t: float = clampf(seconds/float(config.core_residue.seconds),0,1)
        core_residue.modulate.a = 1.0-t if seconds >= 0 else 0.0
        core_residue.visible = core_residue.modulate.a > 0
        core_residue.material.set_shader_parameter("erode",t)
        row["core_residue_alpha"] = core_residue.modulate.a
        row["core_residue_erode"] = t
        row["core_residue_visible"] = core_residue.visible
        row["core_residue_extent_bh"] = float(config.core_residue.native_extent)*core_residue.scale.x/130.0
    if is_instance_valid(ending_smoke):
        ending_smoke.modulate.a = float(config.smoke.alpha)*(1.0-clampf(seconds/float(config.smoke.seconds),0,1)) if seconds >= 0 else 0.0
        ending_smoke.visible = ending_smoke.modulate.a > 0
        ending_smoke.position = Vector2(0,-maxf(0,seconds)*float(config.smoke.rise_px_s))
        row["smoke_alpha"] = ending_smoke.modulate.a
        row["smoke_y"] = ending_smoke.position.y
        row["smoke_z"] = ending_smoke.z_index
'''

if __name__ == "__main__":
    main()
