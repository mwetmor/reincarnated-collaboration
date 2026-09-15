"""Validated cliffside props, foreground occlusion and near-layer coverage.

PNG bytes are copied unchanged. Opaque support means alpha >= 128 (including
for bounding boxes and coverage); near fade uses the full displayed rectangle.
Coverage counts the union, before runtime fading, at viewport pixel centres.
Near entries may set fade=false to omit fading; absent fade defaults to true.
Glows and particles can use z_parent='near:<index>' to attach to that near
sprite. Position/rect then use its top-left texture pixel as local origin;
near particles use local_coords=true. Omitted particle z_parent retains Air.
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
    'glows': {'texture', 'position', 'scale', 'color', 'flicker_hz', 'flicker_amount', 'z_parent'},
}
OPTIONAL_FIELDS = {'particles': {'gravity', 'angular_velocity', 'scale_curve', 'additive', 'z_parent'},
                   'glows': {'sort_y'}, 'near': {'fade'}}


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


def _near_parent(value, near_count):
    """Validate a near reference and return its top-left Sprite2D node path."""
    if not isinstance(value, str) or not re.fullmatch(r'near:[0-9]+', value):
        raise ValueError('z_parent must reference near:<nonnegative integer index>')
    index = int(value[5:])
    if index >= near_count:
        raise ValueError('z_parent near index out of range')
    return f'Near_{index}/NearSprite_{index}'


def load_props(directory):
    """Read strict props.json and all relative RGBA PNGs before any writes.

    Returns the six manifest collections plus root and image metadata. No
    catalogue-specific keys are silently accepted; catalogue data must first
    be mapped explicitly to the props.json contract.
    """
    from export.godot_import import local_file
    root = Path(directory).resolve()
    data = json.loads(local_file(root/'props.json', root).read_text())
    if not isinstance(data, dict) or set(data) - (set(COLLECTIONS) | {'glows'}) or not set(COLLECTIONS) <= set(data):
        raise ValueError('props.json requires six legacy collections and optional glows only')
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
    for collection in ('assets', 'instances', 'shadows', 'overhead', 'near', 'particles', 'glows'):
        if collection not in data:
            continue
        entries = data[collection]
        if not isinstance(entries, list):
            raise ValueError(collection + ' must be a list')
        particle_names = set()
        for item in entries:
            if (not isinstance(item, dict) or not FIELDS[collection] <= set(item)
                    or set(item) - FIELDS[collection] - OPTIONAL_FIELDS.get(collection, set())):
                raise ValueError(collection + ' has missing or unknown fields')
            if 'position' in item:
                _values(item['position'], 2, 'position')
            if 'file' in item:
                metadata = png(item['file'])
            if collection == 'assets':
                _name(item['name'], names)
                _values(item['anchor'], 2, 'anchor')
                if any(not 0 <= a <= b for a, b in zip(item['anchor'], metadata['size'])):
                    raise ValueError('anchor must be inside asset pixel bounds')
                footprint = item['footprint']
                if (not isinstance(footprint, dict) or not {'w', 'h'} <= set(footprint)
                        or set(footprint) - {'w', 'h', 'offset', 'shape'}):
                    raise ValueError('footprint requires w, h; optional offset and shape only')
                for key in ('w', 'h'):
                    _positive(footprint[key], 'footprint dimension')
                _values(footprint.get('offset', [0, 0]), 2, 'footprint offset')
                if footprint.get('shape', 'ellipse') not in ('ellipse', 'rect'):
                    raise ValueError('footprint shape must be ellipse or rect')
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
                if 'fade' in item and not isinstance(item['fade'], bool):
                    raise ValueError('near fade must be boolean')
            elif collection == 'particles':
                if 'z_parent' in item:
                    _near_parent(item['z_parent'], len(data['near']))
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
                if 'gravity' in item:
                    _values(item['gravity'], 2, 'gravity')
                if 'angular_velocity' in item:
                    lo, hi = _values(item['angular_velocity'], 2, 'angular_velocity')
                    if hi < lo:
                        raise ValueError('angular_velocity requires ordered bounds')
                if 'scale_curve' in item:
                    if any(v < 0 for v in _values(item['scale_curve'], 2, 'scale_curve')):
                        raise ValueError('scale_curve requires nonnegative endpoints')
                if 'additive' in item and not isinstance(item['additive'], bool):
                    raise ValueError('additive must be boolean')
            elif collection == 'glows':
                png(item['texture'])
                _positive(item['scale'], 'glow scale')
                if any(not 0 <= v <= 1 for v in _values(item['color'], 4, 'glow color')):
                    raise ValueError('glow color components must be in [0,1]')
                for key, lo, hi in (('flicker_hz', .5, 20), ('flicker_amount', 0, .9)):
                    if not _number(item[key]) or not lo <= item[key] <= hi:
                        raise ValueError(key + f' must be finite in [{lo},{hi}]')
                if item['z_parent'] not in ('actors', 'overhead'):
                    _near_parent(item['z_parent'], len(data['near']))
                if 'sort_y' in item and not _number(item['sort_y']):
                    raise ValueError('glow sort_y must be finite')
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
# body_width is retained for mode 2's legacy near-layer rectangle.
@export var keeper_path: NodePath
@export var body_width: float = 48.0
# 0: opaque overlap behind anchor; 1: opaque overlap; 2: near full screen rect.
@export var fade_mode: int = 0
# Retained for byte-compatible scene exports; modes 0/1 now use alpha masks.
@export var opaque_rect: Rect2
@onready var keeper: Node2D = get_node(keeper_path)
var target_alpha: float = 1.0
var fade_tween: Tween
var prop_mask: BitMap
# Texture keys retain their resources and cannot alias recycled instance IDs.
var frame_masks: Dictionary = {}

func _ready() -> void:
    if fade_mode != 2 and texture != null:
        prop_mask = _alpha_mask(texture)

func _alpha_mask(source: Texture2D) -> BitMap:
    var mask := BitMap.new()
    mask.create_from_image_alpha(source.get_image(), 0.5)
    return mask

func _opaque_at(mask: BitMap, point: Vector2, inverse: Transform2D,
        rect: Rect2, horizontal_flip: bool, vertical_flip: bool) -> bool:
    var local: Vector2 = inverse * point
    if not rect.has_point(local):
        return false
    var size: Vector2i = mask.get_size()
    var uv: Vector2 = (local - rect.position) / rect.size
    var pixel := Vector2i(floori(uv.x * size.x), floori(uv.y * size.y))
    if horizontal_flip:
        pixel.x = size.x - 1 - pixel.x
    if vertical_flip:
        pixel.y = size.y - 1 - pixel.y
    return pixel.x >= 0 and pixel.y >= 0 and pixel.x < size.x and pixel.y < size.y and mask.get_bitv(pixel)

func _pixel_overlap() -> bool:
    if prop_mask == null:
        return false
    var sprite := keeper.get_node_or_null("AnimatedSprite2D") as AnimatedSprite2D
    if sprite == null or sprite.sprite_frames == null:
        return false
    var frames: SpriteFrames = sprite.sprite_frames
    if not frames.has_animation(sprite.animation) or frames.get_frame_count(sprite.animation) == 0:
        return false
    var current: Texture2D = frames.get_frame_texture(sprite.animation, sprite.frame)
    if current == null:
        return false
    if not frame_masks.has(current):
        frame_masks[current] = _alpha_mask(current)
    var mask: BitMap = frame_masks[current]
    var size: Vector2 = current.get_size()
    var origin: Vector2 = sprite.offset - (size / 2.0 if sprite.centered else Vector2.ZERO)
    var frame_rect := Rect2(origin, size)
    var prop_rect: Rect2 = get_rect()
    var prop_transform: Transform2D = get_global_transform_with_canvas()
    var frame_transform: Transform2D = sprite.get_global_transform_with_canvas()
    if is_zero_approx(prop_transform.determinant()) or is_zero_approx(frame_transform.determinant()):
        return false
    var intersection: Rect2 = (prop_transform * prop_rect).intersection(frame_transform * frame_rect)
    if not intersection.has_area():
        return false
    var prop_inverse: Transform2D = prop_transform.affine_inverse()
    var frame_inverse: Transform2D = frame_transform.affine_inverse()
    # Fixed canvas pixel-centre lattice, 2 px apart, not a sprite-local grid.
    var first_x: float = ceil((intersection.position.x - 0.5) / 2.0) * 2.0 + 0.5
    var first_y: float = ceil((intersection.position.y - 0.5) / 2.0) * 2.0 + 0.5
    var y: float = first_y
    while y < intersection.end.y:
        var x: float = first_x
        while x < intersection.end.x:
            var point := Vector2(x, y)
            if _opaque_at(prop_mask, point, prop_inverse, prop_rect, flip_h, flip_v) and _opaque_at(mask, point, frame_inverse, frame_rect, sprite.flip_h, sprite.flip_v):
                return true
            x += 2.0
        y += 2.0
    return false

func _process(_delta: float) -> void:
    if not is_instance_valid(keeper):
        return
    var overlap: bool
    if fade_mode == 2:
        # Preserve near's full displayed rect, body proxy, and 0.15 s tween.
        var body: Rect2 = keeper.get_global_transform_with_canvas() * Rect2(-body_width / 2.0, -130.0, body_width, 130.0)
        var displayed: Rect2 = get_global_transform_with_canvas() * get_rect()
        overlap = displayed.has_area() and displayed.intersects(body)
    elif fade_mode == 0:
        overlap = keeper.global_position.y < global_position.y and _pixel_overlap()
    else:
        overlap = _pixel_overlap()
    var wanted: float = 0.35 if overlap else 1.0
    if wanted != target_alpha:
        target_alpha = wanted
        if fade_tween != null:
            fade_tween.kill()
        fade_tween = create_tween()
        fade_tween.tween_property(self, "modulate:a", wanted, 0.15 if fade_mode == 2 else 0.06)
'''


def ellipse(footprint):
    """Local footprint vertices; legacy ellipse by default, optional offset/rect.

    The historical name remains callable. Offsets are level pixels, independent
    of sprite texture offset and scale. Do not add zero to legacy coordinates:
    preserving signed zeros and rounding keeps old scene text identical.
    """
    if footprint.get('shape', 'ellipse') == 'rect':
        w, h = footprint['w']/2, footprint['h']/2
        points = [[-w, -h], [w, -h], [w, h], [-w, h]]
    else:
        points = [[footprint['w']/2*math.cos(i*math.tau/16),
                   footprint['h']/2*math.sin(i*math.tau/16)] for i in range(16)]
    dx, dy = footprint.get('offset', [0, 0])
    if dx or dy:
        points = [[x+dx if dx else x, y+dy if dy else y] for x, y in points]
    return points


GLOW_FLICKER_SCRIPT = '''extends Sprite2D
@export var flicker_hz: float = 4.0
@export var flicker_amount: float = 0.4
# Stable seed per manifest entry: phases differ per instance, never per frame.
@export var phase_seed: int = 1
var phases: Vector3
var elapsed: float = 0.0
var base_alpha: float
var base_scale: Vector2
var centre_offset: Vector2

func _ready() -> void:
    var rng := RandomNumberGenerator.new()
    rng.seed = phase_seed
    phases = Vector3(rng.randf_range(0, TAU), rng.randf_range(0, TAU), rng.randf_range(0, TAU))
    base_alpha = modulate.a
    base_scale = scale
    centre_offset = offset * scale

func _process(delta: float) -> void:
    elapsed += delta
    var t: float = elapsed * TAU * flicker_hz
    var n: float = (sin(t + phases.x) + sin(t * 1.73 + phases.y) + sin(t * 2.61 + phases.z)) / 3.0
    var factor: float = 1.0 + flicker_amount * n
    modulate.a = base_alpha * factor
    scale = base_scale * factor
    # Keep the visual centre fixed while the node's y-sort anchor stays fixed.
    offset = centre_offset / scale
'''


def _glow_sort_y(entry, props):
    """sort_y is the owning anchor y; the glow node sorts one pixel after it.

    Without an override choose the closest prop centre whose displayed bounds
    contain the glow; otherwise the closest prop anchor. Ties use manifest
    order. Standalone glows use their own centre y. No pixel art is changed.
    """
    if 'sort_y' in entry:
        return entry['sort_y'] + 1
    assets = {a['name']: a for a in props['assets']}
    candidates, containing = [], []
    x, y = entry['position']
    for instance in props['instances']:
        asset = assets[instance['asset']]
        px, py = instance['position']
        ax, ay = asset['anchor']
        w, h = props['images'][asset['file']]['size']
        candidates.append(((x-px)**2+(y-py)**2, py))
        if px-ax <= x <= px-ax+w and py-ay <= y <= py-ay+h:
            containing.append(((x-(px-ax+w/2))**2+(y-(py-ay+h/2))**2, py))
    matches = containing or candidates
    return (min(matches, key=lambda p: p[0])[1] if matches else y) + 1


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
    used.update(e['texture'] for e in props.get('glows', []))
    for i, file in enumerate(props['images']):
        ident = f'PropsTexture{i}'
        dest = 'props/'+file
        (out/dest).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(props['root']/file, out/dest)
        if file in used:
            external.append(f'[ext_resource type="Texture2D" path="res://{dest}" id="{ident}"]')
        textures[file] = ident
    fade_used = bool(props['overhead'] or any(e.get('fade', True) for e in props['near']) or any(
        a['fade_when_behind'] and any(i['asset'] == a['name'] for i in props['instances']) for a in props['assets']))
    if fade_used:
        (out/'scripts/occlusion_fade.gd').write_text(OCCLUSION_SCRIPT)
        external.append('[ext_resource type="Script" path="res://scripts/occlusion_fade.gd" id="OcclusionFade"]')
    if props.get('glows'):
        (out/'scripts/glow_flicker.gd').write_text(GLOW_FLICKER_SCRIPT)
        external.append('[ext_resource type="Script" path="res://scripts/glow_flicker.gd" id="GlowFlicker"]')
    if props.get('glows') or any(e.get('additive', False) for e in props['particles']):
        subresources.append('[sub_resource type="CanvasItemMaterial" id="PropsAdditive"]\nblend_mode = 1\n')

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
    near_glows = ''
    for i, entry in enumerate(props.get('glows', [])):
        near_parented = entry['z_parent'] not in ('actors', 'overhead')
        parent = (_near_parent(entry['z_parent'], len(props['near'])) if near_parented
                  else 'Actors' if entry['z_parent'] == 'actors' else 'Overhead')
        x, y = entry['position']
        sort_y = _glow_sort_y(entry, props) if parent == 'Actors' else y
        glow = (f'\n[node name="Glow_{i}" type="Sprite2D" parent="{parent}"]\n'
                  f'position = {_vector([x, sort_y])}\ncentered = true\n'
                  f'offset = {_vector([0, (y-sort_y)/entry["scale"]])}\n'
                  f'scale = {_vector([entry["scale"]]*2)}\n'
                  f'texture = ExtResource("{textures[entry["texture"]]}")\n'
                  'material = SubResource("PropsAdditive")\nscript = ExtResource("GlowFlicker")\n'
                  'modulate = Color('+', '.join(format(v, '.12g') for v in entry['color'])+')\n'
                  f'flicker_hz = {entry["flicker_hz"]:.12g}\nflicker_amount = {entry["flicker_amount"]:.12g}\n'
                  f'phase_seed = {i+1}\n')
        if near_parented:
            near_glows += glow
        else:
            after += glow
    for i, entry in enumerate(props['overhead']):
        after += sprite(f'Overhead_{i}', 'Overhead', entry['file'], entry['position'])
        after += fade(entry['file'], [0, 0], 1, '../../Actors/Keeper')
    for i, entry in enumerate(props['near']):
        after += (f'\n[node name="Near_{i}" type="Parallax2D" parent="."]\nz_index = 4\n'
                  f'position = {_vector(entry["position"])}\nscroll_offset = {_vector(entry["position"])}\n'
                  f'scroll_scale = {_vector([entry["scroll_scale"]]*2)}\n')
        after += sprite(f'NearSprite_{i}', f'Near_{i}', entry['file'], [0, 0])
        if entry.get('fade', True):
            after += fade(entry['file'], [0, 0], 2, '../../Actors/Keeper')
    # PackedScene requires each parent to be declared before its children.
    after += near_glows
    after += '\n[node name="Air" type="Node2D" parent="."]\nz_index = 5\n'
    for i, entry in enumerate(props['particles']):
        near_parented = 'z_parent' in entry
        parent = _near_parent(entry['z_parent'], len(props['near'])) if near_parented else 'Air'
        x0, y0, x1, y1 = entry['rect']
        colors = entry['color_start']+entry['color_end']
        subresources.append(f'[sub_resource type="Gradient" id="PropsGradient{i}"]\noffsets = PackedFloat32Array(0, 1)\ncolors = PackedColorArray('+', '.join(format(v, '.12g') for v in colors)+')\n')
        after += (f'\n[node name="Particles_{entry["name"]}" type="CPUParticles2D" parent="{parent}"]\n'
                  f'position = {_vector([(x0+x1)/2, (y0+y1)/2])}\n'
                  f'texture = ExtResource("{textures[entry["texture"]]}")\n'
                  f'amount = {entry["amount"]}\nlifetime = {entry["lifetime_s"]:.12g}\n'
                  f'local_coords = {str(near_parented).lower()}\nemitting = true\nemission_shape = 3\n'
                  f'emission_rect_extents = {_vector([(x1-x0)/2, (y1-y0)/2])}\n'
                  f'direction = {_vector(entry["direction"])}\nspread = {entry["spread_deg"]:.12g}\n'
                  f'gravity = {_vector(entry.get("gravity", [0, 0]))}\n'
                  f'initial_velocity_min = {entry["velocity_px_s"][0]:.12g}\ninitial_velocity_max = {entry["velocity_px_s"][1]:.12g}\n'
                  f'scale_amount_min = {entry["scale"][0]:.12g}\nscale_amount_max = {entry["scale"][1]:.12g}\n'
                  f'color_ramp = SubResource("PropsGradient{i}")\n')
        if 'angular_velocity' in entry:
            lo, hi = entry['angular_velocity']
            after += f'angular_velocity_min = {lo:.12g}\nangular_velocity_max = {hi:.12g}\n'
        if 'scale_curve' in entry:
            start, end = entry['scale_curve']
            # Curve._data requires Variant::FLOAT tangents even for integers.
            slope = repr(float(end-start))
            subresources.append(f'[sub_resource type="Curve" id="PropsScale{i}"]\n'
                                f'min_value = {min(0, start, end):.12g}\nmax_value = {max(1, start, end):.12g}\n'
                                f'_data = [Vector2(0, {start:.12g}), 0.0, {slope}, 0, 0, '
                                f'Vector2(1, {end:.12g}), {slope}, 0.0, 0, 0]\npoint_count = 2\n')
            after += f'scale_amount_curve = SubResource("PropsScale{i}")\n'
        if entry.get('additive', False):
            after += 'material = SubResource("PropsAdditive")\n'
    return {'external': external, 'subresources': subresources, 'before_keeper': before,
            'after_keeper': after, 'collisions': collisions,
            'counts': {**{k: len(props[k]) for k in COLLECTIONS},
                       **({'glows': len(props['glows'])} if 'glows' in props else {})}}
