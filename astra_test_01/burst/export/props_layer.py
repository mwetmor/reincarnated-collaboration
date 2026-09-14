"""Validated cliffside props, foreground occlusion and near-layer coverage.

PNG bytes are copied unchanged. Opaque support means alpha >= 128 (including
for bounding boxes and coverage); near fade uses the full displayed rectangle.
Coverage counts the union, before runtime fading, at viewport pixel centres.
"""
import json
import math
from pathlib import Path
import re
import shutil

import numpy as np
from PIL import Image
from export.scene_kit import _number, _contains
from export.parallax_scene import VIEW, _annotation, _rectangle, _vector, _packed, camera_offset

COLLECTIONS = {'assets', 'instances', 'shadows', 'overhead', 'near', 'particles'}
FIELDS = {
    'assets': {'name', 'file', 'anchor', 'footprint', 'collide', 'fade_when_behind'},
    'instances': {'asset', 'position'},
    'shadows': {'file', 'position', 'opacity'},
    'overhead': {'file', 'position'},
    'near': {'file', 'position', 'scroll_scale'},
    'particles': {'name', 'texture', 'rect', 'amount', 'lifetime_s', 'velocity_px_s',
                  'direction', 'spread_deg', 'scale', 'color_start', 'color_end'},
}


def _fields(value, fields, label):
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError(label + ' requires exactly: ' + ', '.join(sorted(fields)))


def _values(value, size, label):
    if not isinstance(value, list) or len(value) != size or not all(_number(v) for v in value):
        raise ValueError(label + ' must contain finite numbers')
    return value


def _positive(value, label):
    if not _number(value) or value <= 0:
        raise ValueError(label + ' must be finite and positive')


def _name(value, seen):
    if (not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', value)
            or value in seen):
        raise ValueError('Names must be unique safe node names')
    seen.add(value)


def load_props(directory):
    """Read strict props.json and all relative RGBA PNGs before any writes.

    Returns the six manifest collections plus root and image metadata. No
    catalogue-specific keys are silently accepted; catalogue data must first
    be mapped explicitly to the props.json contract.
    """
    from export.godot_import import local_file
    root = Path(directory).resolve()
    data = json.loads(local_file(root/'props.json', root).read_text())
    _fields(data, COLLECTIONS, 'props.json')
    images = {}

    def png(file):
        if (not isinstance(file, str) or not file or Path(file).is_absolute()
                or '..' in Path(file).parts or '\\' in file
                or any(ord(c) < 32 or c == '"' for c in file)
                or Path(file).suffix.lower() != '.png'):
            raise ValueError('Assets must be relative PNG paths inside DIR')
        if file not in images:
            path = local_file(root/file, root)
            try:
                with Image.open(path) as im:
                    if im.format != 'PNG' or im.mode != 'RGBA':
                        raise ValueError('Props textures must be RGBA PNGs')
                    alpha = np.array(im.getchannel('A')) >= 128
                    yy, xx = np.nonzero(alpha)
                    bbox = [int(xx.min()), int(yy.min()), int(xx.max()+1), int(yy.max()+1)] if len(xx) else [0, 0, 0, 0]
                    images[file] = {'size': list(im.size), 'bbox': bbox}
            except (OSError, SyntaxError) as exc:
                raise ValueError('Unreadable PNG: '+file) from exc
        return images[file]

    names = set()
    for collection in ('assets', 'instances', 'shadows', 'overhead', 'near', 'particles'):
        entries = data[collection]
        if not isinstance(entries, list):
            raise ValueError(collection + ' must be a list')
        particle_names = set()
        for item in entries:
            _fields(item, FIELDS[collection], collection)
            if 'position' in item:
                _values(item['position'], 2, 'position')
            if 'file' in item:
                metadata = png(item['file'])
            if collection == 'assets':
                _name(item['name'], names)
                _values(item['anchor'], 2, 'anchor')
                if any(not 0 <= a <= b for a, b in zip(item['anchor'], metadata['size'])):
                    raise ValueError('anchor must be inside asset pixel bounds')
                _fields(item['footprint'], {'w', 'h'}, 'footprint')
                for value in item['footprint'].values():
                    _positive(value, 'footprint dimension')
                if any(not isinstance(item[k], bool) for k in ('collide', 'fade_when_behind')):
                    raise ValueError('collide and fade_when_behind must be booleans')
            elif collection == 'instances':
                if not isinstance(item['asset'], str) or item['asset'] not in names:
                    raise ValueError('Instance references unknown asset')
            elif collection == 'shadows':
                if not _number(item['opacity']) or not 0 <= item['opacity'] <= 1:
                    raise ValueError('opacity must be finite in [0,1]')
            elif collection == 'near':
                if not _number(item['scroll_scale']) or item['scroll_scale'] <= 1:
                    raise ValueError('near scroll_scale must be finite and > 1')
            elif collection == 'particles':
                _name(item['name'], particle_names)
                png(item['texture'])
                _rectangle(item['rect'], 'particle rect')
                amount = item['amount']
                if isinstance(amount, bool) or not isinstance(amount, int) or not 1 <= amount <= 512:
                    raise ValueError('particle amount must be integer 1..512')
                _positive(item['lifetime_s'], 'lifetime_s')
                for key in ('velocity_px_s', 'scale'):
                    lo, hi = _values(item[key], 2, key)
                    if lo < 0 or hi < lo or (key == 'scale' and lo == 0):
                        raise ValueError(key + ' requires ordered nonnegative bounds (scale > 0)')
                direction = _values(item['direction'], 2, 'direction')
                if direction == [0, 0]:
                    raise ValueError('particle direction must be nonzero')
                if not _number(item['spread_deg']) or not 0 <= item['spread_deg'] <= 180:
                    raise ValueError('spread_deg must be in [0,180]')
                for key in ('color_start', 'color_end'):
                    if any(not 0 <= v <= 1 for v in _values(item[key], 4, key)):
                        raise ValueError(key + ' components must be in [0,1]')
    return {**data, 'root': root, 'images': images}


def _camera_top_left(position, camera):
    # Camera2D applies limits to its centred rectangle, then its offset.
    # For a limit span smaller than the view, the right/bottom limit wins.
    offset = camera_offset(camera)
    return [min(max(p-size/2, lo), hi-size)+o
            for p, size, lo, hi, o in zip(position, VIEW, camera['limits'][:2],
                                          camera['limits'][2:], offset)]


def near_coverage(props, walkable, camera, step_px=64):
    """Share of walkable follow-camera samples with >=5% near opaque coverage.

    ``props`` is load_props(DIR)'s result (DIR itself is also accepted).
    Samples are the half-step lattice inside walkable.bounds, excluding blocked
    ground. Each ground sample has equal weight, even at clamped camera limits.
    Camera2D limits precede its anchor-derived offset, as in the engine. Near
    screen top-left = position - scroll_scale * camera_view_top_left; there is
    no repeat. Pixel-centre nearest sampling and alpha >=128 define support.
    Zero eligible samples is unevaluable and raises ValueError, never 0/0.
    """
    if isinstance(props, (str, Path)):
        props = load_props(props)
    if isinstance(step_px, bool) or not _number(step_px) or step_px <= 0:
        raise ValueError('step_px must be finite and positive')
    _annotation(walkable)
    camera_offset(camera)
    masks = []
    for entry in props['near']:
        with Image.open(props['root']/entry['file']) as im:
            masks.append(np.array(im.getchannel('A')) >= 128)
    x0, y0, x1, y1 = walkable['bounds']
    samples = covered = 0
    view = np.zeros((VIEW[1], VIEW[0]), dtype=bool)
    for y in np.arange(y0+step_px/2, y1, step_px):
        for x in np.arange(x0+step_px/2, x1, step_px):
            point = (x, y)
            if (not any(_contains(point, p) for p in walkable['walkable'])
                    or any(_contains(point, p) for p in walkable['blocked'])):
                continue
            samples += 1
            if not masks:
                continue
            top_left = _camera_top_left(point, camera)
            view.fill(False)
            for entry, mask in zip(props['near'], masks):
                px, py = [math.ceil(p-entry['scroll_scale']*c-0.5)
                          for p, c in zip(entry['position'], top_left)]
                h, w = mask.shape
                left, top, right, bottom = max(0, px), max(0, py), min(VIEW[0], px+w), min(VIEW[1], py+h)
                if left < right and top < bottom:
                    view[top:bottom, left:right] |= mask[top-py:bottom-py, left-px:right-px]
            covered += int(np.count_nonzero(view) >= VIEW[0]*VIEW[1]*0.05)
    if not samples:
        raise ValueError('No walkable camera samples at this step_px')
    return covered/samples


OCCLUSION_SCRIPT = '''extends Sprite2D
# body_width is the exported character opaque width in level pixels.
@export var keeper_path: NodePath
@export var body_width: float = 48.0
# 0: prop behind anchor; 1: overhead opaque bounds; 2: near full screen rect.
@export var fade_mode: int = 0
@export var opaque_rect: Rect2
@onready var keeper: Node2D = get_node(keeper_path)
var target_alpha: float = 1.0
var fade_tween: Tween

func _process(_delta: float) -> void:
    if not is_instance_valid(keeper):
        return
    var body: Rect2 = keeper.get_global_transform_with_canvas() * Rect2(-body_width / 2.0, -130.0, body_width, 130.0)
    var local_bounds: Rect2 = get_rect() if fade_mode == 2 else opaque_rect
    var displayed: Rect2 = get_global_transform_with_canvas() * local_bounds
    var overlap: bool = displayed.has_area() and displayed.intersects(body)
    if fade_mode == 0:
        overlap = overlap and keeper.global_position.y < global_position.y
    var wanted: float = 0.35 if overlap else 1.0
    if wanted != target_alpha:
        target_alpha = wanted
        if fade_tween != null:
            fade_tween.kill()
        fade_tween = create_tween()
        fade_tween.tween_property(self, "modulate:a", wanted, 0.15)
'''


def ellipse(footprint):
    """Sixteen local vertices centred at the instance anchor."""
    return [[footprint['w']/2*math.cos(i*math.tau/16),
             footprint['h']/2*math.sin(i*math.tau/16)] for i in range(16)]


def write_layers(out, props, body_width=48.0):
    """Return scene fragments; copy validated textures without transforming art."""
    out = Path(out)
    target = out/'props'
    target.mkdir()
    shutil.copyfile(props['root']/'props.json', target/'props.json')
    external, subresources = [], []
    textures = {}
    used = {a['file'] for a in props['assets'] if any(i['asset'] == a['name'] for i in props['instances'])}
    used.update(e['file'] for key in ('shadows', 'overhead', 'near') for e in props[key])
    used.update(e['texture'] for e in props['particles'])
    for i, file in enumerate(props['images']):
        ident = f'PropsTexture{i}'
        dest = 'props/'+file
        (out/dest).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(props['root']/file, out/dest)
        if file in used:
            external.append(f'[ext_resource type="Texture2D" path="res://{dest}" id="{ident}"]')
        textures[file] = ident
    fade_used = bool(props['overhead'] or props['near'] or any(
        a['fade_when_behind'] and any(i['asset'] == a['name'] for i in props['instances']) for a in props['assets']))
    if fade_used:
        (out/'scripts/occlusion_fade.gd').write_text(OCCLUSION_SCRIPT)
        external.append('[ext_resource type="Script" path="res://scripts/occlusion_fade.gd" id="OcclusionFade"]')

    def sprite(name, parent, file, position, offset=(0, 0)):
        return (f'\n[node name="{name}" type="Sprite2D" parent="{parent}"]\n'
                f'position = {_vector(position)}\ntexture = ExtResource("{textures[file]}")\n'
                f'centered = false\noffset = {_vector(offset)}\n')

    def fade(file, offset, mode, keeper_path):
        x0, y0, x1, y1 = props['images'][file]['bbox']
        rect = [x0+offset[0], y0+offset[1], x1-x0, y1-y0]
        return (f'script = ExtResource("OcclusionFade")\nkeeper_path = NodePath("{keeper_path}")\n'
                f'body_width = {body_width:.12g}\nfade_mode = {mode}\n'
                'opaque_rect = Rect2('+', '.join(format(v, '.12g') for v in rect)+')\n')

    before = '\n[node name="Shadows" type="Node2D" parent="."]\nz_index = 1\n'
    for i, entry in enumerate(props['shadows']):
        before += sprite(f'Shadow_{i}', 'Shadows', entry['file'], entry['position'])
        before += f'modulate = Color(1, 1, 1, {entry["opacity"]:.12g})\n'
    before += '\n[node name="Actors" type="Node2D" parent="."]\ny_sort_enabled = true\nz_index = 2\n'
    after, collisions = '', ''
    assets = {a['name']: a for a in props['assets']}
    for i, instance in enumerate(props['instances']):
        asset = assets[instance['asset']]
        offset = [-v for v in asset['anchor']]
        after += sprite(f'Prop_{i}', 'Actors', asset['file'], instance['position'], offset)
        if asset['fade_when_behind']:
            after += fade(asset['file'], offset, 0, '../Keeper')
        if asset['collide']:
            collisions += (f'\n[node name="PropCollision_{i}" type="CollisionPolygon2D" parent="Walls"]\n'
                           f'position = {_vector(instance["position"])}\npolygon = {_packed(ellipse(asset["footprint"]))}\n')
    after += '\n[node name="Overhead" type="Node2D" parent="."]\nz_index = 3\n'
    for i, entry in enumerate(props['overhead']):
        after += sprite(f'Overhead_{i}', 'Overhead', entry['file'], entry['position'])
        after += fade(entry['file'], [0, 0], 1, '../../Actors/Keeper')
    for i, entry in enumerate(props['near']):
        after += (f'\n[node name="Near_{i}" type="Parallax2D" parent="."]\nz_index = 4\n'
                  f'position = {_vector(entry["position"])}\nscroll_offset = {_vector(entry["position"])}\n'
                  f'scroll_scale = {_vector([entry["scroll_scale"]]*2)}\n')
        after += sprite(f'NearSprite_{i}', f'Near_{i}', entry['file'], [0, 0])
        after += fade(entry['file'], [0, 0], 2, '../../Actors/Keeper')
    after += '\n[node name="Air" type="Node2D" parent="."]\nz_index = 5\n'
    for i, entry in enumerate(props['particles']):
        x0, y0, x1, y1 = entry['rect']
        colors = entry['color_start']+entry['color_end']
        subresources.append(f'[sub_resource type="Gradient" id="PropsGradient{i}"]\noffsets = PackedFloat32Array(0, 1)\ncolors = PackedColorArray('+', '.join(format(v, '.12g') for v in colors)+')\n')
        after += (f'\n[node name="Particles_{entry["name"]}" type="CPUParticles2D" parent="Air"]\n'
                  f'position = {_vector([(x0+x1)/2, (y0+y1)/2])}\n'
                  f'texture = ExtResource("{textures[entry["texture"]]}")\n'
                  f'amount = {entry["amount"]}\nlifetime = {entry["lifetime_s"]:.12g}\n'
                  'local_coords = false\nemitting = true\nemission_shape = 3\n'
                  f'emission_rect_extents = {_vector([(x1-x0)/2, (y1-y0)/2])}\n'
                  f'direction = {_vector(entry["direction"])}\nspread = {entry["spread_deg"]:.12g}\n'
                  'gravity = Vector2(0, 0)\n'
                  f'initial_velocity_min = {entry["velocity_px_s"][0]:.12g}\ninitial_velocity_max = {entry["velocity_px_s"][1]:.12g}\n'
                  f'scale_amount_min = {entry["scale"][0]:.12g}\nscale_amount_max = {entry["scale"][1]:.12g}\n'
                  f'color_ramp = SubResource("PropsGradient{i}")\n')
    return {'external': external, 'subresources': subresources, 'before_keeper': before,
            'after_keeper': after, 'collisions': collisions,
            'counts': {k: len(props[k]) for k in COLLECTIONS}}
