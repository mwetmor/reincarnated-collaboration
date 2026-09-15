"""Build an authored effect kit from a dict or JSON path.

Paths in a JSON definition resolve beside that JSON (dict paths resolve from
cwd). A phase's sheet identifies its source PNG; frame.file is an explicit
PNG, relative to the definition, not an implicit atlas rectangle. Repeating a
file is supported. No grid geometry is guessed. Cast/travel/impact are required;
residual and individual layers may be omitted. Travel defaults: 520 px/s,
streak=False. Omitted layers are disabled. Holds are integer 60 Hz ticks.
"""
import copy
import json
import math
from pathlib import Path
import re
import time

import numpy as np
from PIL import Image

PHASES = {'cast': 'flare', 'travel': 'travel', 'impact': 'impact', 'residual': 'residual'}
TOP = {'name', 'element', 'tint', 'phases', 'layers', 'ground_squash', 'pixel_scale'}
LAYER_KEYS = {
    'glow': {'alpha', 'scale'}, 'floor_light': {'duration_s', 'radius_px'},
    'flash': {'duration_s', 'alpha', 'scale_from', 'scale_to'},
    'decal': {'file', 'duration_s'}, 'hitstop': {'duration_s', 'time_scale'},
    'shake': {'distance', 'duration_s'},
    'particles': {'texture', 'amount', 'lifetime_s', 'velocity_px_s', 'direction', 'spread_deg'},
}


def _keys(value, allowed, required, label):
    if not isinstance(value, dict) or set(value)-allowed or not required <= set(value):
        raise ValueError(label+' has missing or unknown keys')


def _number(value, low, high, label, integer=False):
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value) or not low <= value <= high
            or (integer and not isinstance(value, int))):
        raise ValueError(label+' has invalid numeric value')


def _png(value, root, grayscale=False, confined=False):
    if (not isinstance(value, str) or not value or '\\' in value
            or any(ord(c) < 32 or c == '"' for c in value)):
        raise ValueError('Invalid PNG path')
    path = (root/value).resolve()
    if confined and (Path(value).is_absolute() or not path.is_relative_to(root)):
        raise ValueError('Kit asset escapes its directory')
    if not path.is_file() or path.suffix.lower() != '.png':
        raise ValueError('Missing PNG: '+str(path))
    try:
        with Image.open(path) as im:
            if im.format != 'PNG':
                raise ValueError('Asset must be PNG')
            pixels = np.array(im.convert('RGBA'))
            if grayscale:
                rgb = pixels[..., :3][pixels[..., 3] > 0]
                if np.any(rgb[:, 0] != rgb[:, 1]) or np.any(rgb[:, 1] != rgb[:, 2]):
                    raise ValueError('Painted sheets and frames must be greyscale')
    except (OSError, SyntaxError) as exc:
        raise ValueError('Unreadable PNG: '+str(path)) from exc
    return path


def _validate(data, root, runtime=False):
    _keys(data, TOP, TOP, 'effect')
    if not isinstance(data['name'], str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', data['name']):
        raise ValueError('name must be a safe identifier')
    if not isinstance(data['element'], str) or not data['element'].strip():
        raise ValueError('element must be nonempty text')
    tint = data['tint']
    if not isinstance(tint, list) or len(tint) != 3:
        raise ValueError('tint requires three components')
    for v in tint: _number(v, 0, 1, 'tint')
    _number(data['pixel_scale'], 1, 8, 'pixel_scale', True)
    _number(data['ground_squash'], .5, .65, 'ground_squash')
    _keys(data['phases'], set(PHASES), {'cast', 'travel', 'impact'}, 'phases')
    assets = {}
    for name, phase in data['phases'].items():
        fields = {'sheet', 'frames'} | ({'speed_px_s', 'streak'} if name == 'travel' else set())
        _keys(phase, fields, {'sheet', 'frames'}, name)
        assets[phase['sheet']] = _png(phase['sheet'], root, not runtime, runtime)
        if not isinstance(phase['frames'], list) or not phase['frames']:
            raise ValueError(name+' requires at least one frame')
        for frame in phase['frames']:
            _keys(frame, {'file', 'hold_frames'}, {'file', 'hold_frames'}, 'frame')
            _number(frame['hold_frames'], 1, math.inf, 'hold_frames', True)
            assets[frame['file']] = _png(frame['file'], root, not runtime, runtime)
        if name == 'travel':
            _number(phase.get('speed_px_s', 520), 1e-9, math.inf, 'speed_px_s')
            if not isinstance(phase.get('streak', False), bool):
                raise ValueError('streak must be boolean')
    _keys(data['layers'], set(LAYER_KEYS)|{'dark_duplicate'}, set(), 'layers')
    for name, layer in data['layers'].items():
        if name == 'dark_duplicate':
            if not isinstance(layer, bool): raise ValueError('dark_duplicate must be boolean')
            continue
        fields = LAYER_KEYS[name]
        _keys(layer, fields, fields-({'file'} if name == 'decal' else set()), name)
        for key, value in layer.items():
            if key in ('file', 'texture'):
                assets[value] = _png(value, root, False, runtime)
            elif key == 'direction':
                if not isinstance(value, list) or len(value) != 2:
                    raise ValueError('direction requires two components')
                for v in value: _number(v, -math.inf, math.inf, key)
                if value == [0, 0]: raise ValueError('direction cannot be zero')
            elif key == 'velocity_px_s':
                if isinstance(value, list):
                    if len(value) != 2: raise ValueError('velocity bounds require two values')
                    for v in value: _number(v, 0, math.inf, key)
                    if value[1] < value[0]: raise ValueError('velocity bounds must be ordered')
                else: _number(value, 0, math.inf, key)
            else:
                lo = 1e-9 if key in ('scale', 'scale_from', 'scale_to', 'radius_px', 'lifetime_s', 'time_scale') else 0
                hi = 1 if key in ('alpha', 'time_scale') else (180 if key == 'spread_deg' else math.inf)
                if key == 'amount': lo, hi = 1, 512
                _number(value, lo, hi, key, key == 'amount')
    return assets


def load_kit(directory):
    """Validate generated kit metadata and every asset before project creation."""
    root = Path(directory).resolve()
    path = root/'kit.json'
    if not path.resolve().is_relative_to(root):
        raise ValueError('kit.json escapes its directory')
    data = json.loads(path.read_text())
    _validate(data, root, runtime=True)
    return data


def _tint(path, tint, scale):
    with Image.open(path) as im:
        pixels = np.array(im.convert('RGBA'))
    # RGB channels are equal on visible body pixels; retain transparent RGB too.
    luminance = pixels[..., :3].astype(float) @ np.array([.2126, .7152, .0722])
    rgb = np.rint(pixels[..., :3].astype(float)*np.array(tint)).astype(np.uint8)
    rgb[luminance >= .92*255] = 255
    pixels[..., :3] = rgb
    image = Image.fromarray(pixels)
    return image.resize((image.width*scale, image.height*scale), Image.Resampling.NEAREST)


def build(effect_json, out_dir):
    """Validate then tint/upscale explicit frame PNGs into a self-contained kit."""
    started = time.monotonic()
    if isinstance(effect_json, (str, Path)):
        path = Path(effect_json).resolve()
        data, root = json.loads(path.read_text()), path.parent
    else:
        data, root = copy.deepcopy(effect_json), Path.cwd()
    assets = _validate(data, root)
    out = Path(out_dir).resolve()
    if any(p.is_relative_to(out) for p in assets.values()):
        raise ValueError('Output overlaps input assets')
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError('Output must be empty')
    from export.godot_import import write_spriteframes
    out.mkdir(parents=True, exist_ok=True)
    metadata = copy.deepcopy(data)
    counts = {}
    for phase, definition in data['phases'].items():
        name = PHASES[phase]
        (out/name).mkdir()
        frames = []
        for i, frame in enumerate(definition['frames']):
            file = f'{name}/{name}_{i:02d}.png'
            _tint(assets[frame['file']], data['tint'], data['pixel_scale']).save(out/file)
            frames.append({'file': file, 'hold_frames': frame['hold_frames']})
        metadata['phases'][phase]['frames'] = frames
        metadata['phases'][phase]['sheet'] = frames[0]['file']
        if phase == 'travel':
            metadata['phases'][phase].setdefault('speed_px_s', 520)
            metadata['phases'][phase].setdefault('streak', False)
        write_spriteframes(out, name+'.tres', {name: ([f['file'] for f in frames], 1, phase == 'travel')},
                           frame_durations={name: [f['hold_frames']/60 for f in frames]})
        counts[name] = len(frames)
    for name, key in (('decal', 'file'), ('particles', 'texture')):
        layer = metadata['layers'].get(name, {})
        if key in layer:
            file = f'layers/{name}.png'
            (out/'layers').mkdir(exist_ok=True)
            _tint(assets[layer[key]], data['tint'], data['pixel_scale']).save(out/file)
            layer[key] = file
    (out/'kit.json').write_text(json.dumps(metadata, indent=2, allow_nan=False)+'\n')
    (out/'vfx_select.json').write_text(json.dumps({'source': 'effect_kit', 'name': data['name']})+'\n')
    (out/'CREDITS.txt').write_text('Effect '+data['name']+' ('+data['element']+'). Source assets supplied by the effect definition; no license is inferred.\n')
    return {'id': 'effect_kit', 'subject': data['name'], 'passed': None, 'value': counts,
            'threshold': None, 'op': None, 'unit': 'frames', 'evidence': [str(out/'kit.json')],
            'notes': 'Authored frame kit; holds measured in 60 Hz ticks.', 'wall_s': time.monotonic()-started}


# Shared runtime fragment is embedded only in authored-kit scripts. Timers for
# feedback ignore Engine.time_scale, and the tree-owned stop controller survives
# an effect being freed. Multiple hits extend one stop without losing baseline.
LAYER_SCRIPT = '''
@export var ground_squash: float = 0.6
@export var hitstop_duration: float = 0.0
@export var hitstop_time_scale: float = 1.0
@export var shake_distance: float = 0.0
@export var shake_duration: float = 0.0
var spell_scale: float = 1.0

func _start_layers(animation_name: String, angle: float = 0.0) -> void:
    $Ground.scale = Vector2(1, ground_squash) * spell_scale
    for node in $Ground.get_children():
        if node is AnimatedSprite2D:
            node.rotation = angle
            node.play(animation_name)
    if has_node("FloorLight"):
        $FloorLight.scale *= spell_scale
        create_tween().tween_property($FloorLight, "modulate:a", 0.0, FLOOR_DURATION)
    if has_node("Ground/Flash"):
        var flash: AnimatedSprite2D = $Ground/Flash
        var tween: Tween = create_tween().set_parallel(true)
        tween.tween_property(flash, "modulate:a", 0.0, FLASH_DURATION)
        tween.tween_property(flash, "scale", Vector2.ONE * FLASH_TO, FLASH_DURATION)
    if has_node("Decal"):
        $Decal.scale *= spell_scale
        create_tween().tween_property($Decal, "modulate:a", 0.0, DECAL_DURATION)
    if has_node("Particles"):
        $Particles.initial_velocity_min *= spell_scale
        $Particles.initial_velocity_max *= spell_scale
        $Particles.scale = Vector2.ONE * spell_scale

func _feedback() -> void:
    var tree: SceneTree = get_tree()
    if hitstop_duration > 0.0:
        var controller: Node = tree.root.get_node_or_null("EffectHitstop")
        if controller == null:
            controller = Node.new()
            controller.name = "EffectHitstop"
            controller.set_meta("baseline", Engine.time_scale)
            controller.set_meta("generation", 0)
            tree.root.add_child(controller)
        var generation: int = int(controller.get_meta("generation")) + 1
        controller.set_meta("generation", generation)
        Engine.time_scale = hitstop_time_scale
        tree.create_timer(hitstop_duration, true, false, true).timeout.connect(func():
            if is_instance_valid(controller) and int(controller.get_meta("generation")) == generation:
                Engine.time_scale = float(controller.get_meta("baseline"))
                controller.name = "EffectHitstopDone"
                controller.queue_free())
    var camera: Camera2D = get_viewport().get_camera_2d()
    if camera != null and shake_duration > 0.0 and shake_distance > 0.0:
        if camera.has_meta("effect_shake_tween"):
            var previous: Tween = camera.get_meta("effect_shake_tween")
            previous.kill()
        else:
            camera.set_meta("effect_shake_baseline", camera.offset)
        var baseline: Vector2 = camera.get_meta("effect_shake_baseline")
        camera.offset = baseline + Vector2(shake_distance, 0)
        var shake: Tween = tree.create_tween().bind_node(camera).set_ignore_time_scale(true)
        camera.set_meta("effect_shake_tween", shake)
        shake.tween_property(camera, "offset", baseline - Vector2(shake_distance, 0), shake_duration * 0.5)
        shake.tween_property(camera, "offset", baseline, shake_duration * 0.5)
        shake.tween_callback(func():
            camera.remove_meta("effect_shake_tween")
            camera.remove_meta("effect_shake_baseline"))
'''

AUTHORED_BOLT = '''extends Area2D
var direction: Vector2 = Vector2.RIGHT
var distance: float = 0.0
var expired: bool = false
var caster: CollisionObject2D
@export var speed_px_s: float = 520.0

func _ready() -> void:
    body_entered.connect(_on_body_entered)
    _start_layers("travel", direction.angle())
    if has_node("Ground/Streak"):
        $Ground/Streak.position = -direction * STREAK_OFFSET
    $CollisionShape2D.shape = $CollisionShape2D.shape.duplicate()
    $CollisionShape2D.shape.radius *= spell_scale

func _physics_process(delta: float) -> void:
    if expired:
        return
    var step: float = minf(speed_px_s * spell_scale * delta, 650.0 * spell_scale - distance)
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
    $Ground.hide()
    if has_node("Particles"):
        $Particles.emitting = false
    set_deferred("monitoring", false)
    var effect: Node2D = load(IMPACT_PATH).instantiate()
    effect.spell_scale = spell_scale
    effect.position = get_parent().to_local(global_position)
    get_parent().add_child(effect)
    get_tree().create_timer(TAIL_DURATION).timeout.connect(queue_free)
'''

AUTHORED_IMPACT = '''extends Node2D
func _ready() -> void:
    _start_layers("impact")
    _feedback()
    $Ground/Shatter.animation_finished.connect(_body_finished)
    if has_node("Residual"):
        $Residual.scale = Vector2(1, ground_squash) * spell_scale
        $Residual.animation_finished.connect($Residual.hide)
    get_tree().create_timer(TOTAL_DURATION).timeout.connect(queue_free)

func _body_finished() -> void:
    $Ground.hide()
    if has_node("Residual"):
        $Residual.show()
        $Residual.play("residual")
'''
