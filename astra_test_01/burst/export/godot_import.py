"""Build a self-contained Godot 4.6 review stub; no art transformations.

Usage: python3 -B -m export.godot_import --cells DIR --out PROJECT
       [--vfx DIR] [--gear-variant DIR]
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


def write_spriteframes(out, resource, animations):
    """Write SpriteFrames from {name: (relative_texture_paths, fps, loop)}."""
    textures = []
    blocks = []
    for name, (paths, fps, loop) in sorted(animations.items()):
        frames = []
        for path in paths:
            local_file(out/path, out)
            ident = str(len(textures)+1)
            textures.append(f'[ext_resource type="Texture2D" path="res://{path}" id="{ident}"]')
            frames.append('{"duration": 1.0, "texture": ExtResource("'+ident+'")}')
        blocks.append('{"frames": ['+',\n'.join(frames)+'], "loop": '+str(loop).lower()+
                      ', "name": &'+json.dumps(name)+', "speed": '+str(float(fps))+'}')
    target = out/resource
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('[gd_resource type="SpriteFrames" load_steps='+str(len(textures)+1)+
                      ' format=3]\n\n'+'\n'.join(textures)+'\n\n[resource]\nanimations = ['+
                      ',\n'.join(blocks)+']\n')


def validate_resources(project):
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


def build_project(cells, out, vfx=None, gear_variant=None):
    started = time.monotonic()
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
    out = _output(out, [cells, vfx, gear_variant])
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
            animations[name] = (paths, FPS[entry['anim']], entry['anim'] not in ('jump', 'cast'))
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
    refs = validate_resources(out)
    return {'cells': sorted(base), 'frames': sum(len(e['frames']) for e in base.values()),
            'texture_references': len(refs), 'gear_cells': len(advanced or {}),
            'vfx_animations': len(effects), 'wall_s': time.monotonic()-started}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cells', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--vfx')
    parser.add_argument('--gear-variant')
    args = parser.parse_args()
    print(json.dumps(build_project(args.cells, args.out, args.vfx, args.gear_variant), indent=2))


if __name__ == '__main__':
    main()
