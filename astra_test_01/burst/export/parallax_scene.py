"""Cliffside scene export: exact tiles, bounded floor complement and follow camera.

Layer records (including optional mist/*.png) all live in parallax.json.layers;
no implicit scroll factors or z positions are invented for unlisted mist files.
Foreground tiles use nearest filtering (Godot CanvasItem enum 1), with no
padding, resampling, mipmaps or overlapping geometry. Other textures retain
project filtering. Camera limits can displace the anchor at world edges.
"""
import json
import math
from pathlib import Path
import re
import shutil
import time

from PIL import Image
from export.scene_kit import _number, _validate, collision, shadow_texture

VIEW = (1920, 1080)


def _vector(values):
    return 'Vector2(' + ', '.join(format(float(v), '.12g') for v in values) + ')'


def _packed(points):
    return 'PackedVector2Array(' + ', '.join(format(float(v), '.12g') for p in points for v in p) + ')'


def _rectangle(values, label):
    if (not isinstance(values, list) or len(values) != 4 or
            not all(_number(v) for v in values) or
            values[0] >= values[2] or values[1] >= values[3]):
        raise ValueError(label + ' must be finite [x0,y0,x1,y1] with positive area')
    return values


def _annotation(walkable):
    keys = {'canvas_size', 'walkable', 'blocked', 'spawn', 'bounds', 'figure_height_px'}
    if not isinstance(walkable, dict) or set(walkable) != keys:
        raise ValueError('walkable.json must contain exactly the cliffside geometry fields')
    annotation = {k: walkable[k] for k in ('walkable', 'blocked', 'spawn', 'figure_height_px')}
    annotation.update(plate_size=walkable['canvas_size'], occluders=[], exits=[])
    _validate(annotation)
    x0, y0, x1, y1 = _rectangle(walkable['bounds'], 'bounds')
    w, h = walkable['canvas_size']
    if not (0 <= x0 < x1 <= w and 0 <= y0 < y1 <= h):
        raise ValueError('bounds must be inside the foreground canvas')
    x, y = walkable['spawn']
    if not (x0 < x < x1 and y0 < y < y1):
        raise ValueError('spawn must be strictly inside bounds')
    return annotation


def camera_offset(camera):
    """Offset in 1920x1080 world pixels preserving anchor/view fractions."""
    if not isinstance(camera, dict) or set(camera) != {'anchor', 'view', 'limits'}:
        raise ValueError('camera requires anchor, view and limits')
    for name in ('anchor', 'view'):
        values = camera[name]
        if not isinstance(values, list) or len(values) != 2 or not all(_number(v) for v in values):
            raise ValueError('camera.' + name + ' must be finite [x,y]')
    if any(v <= 0 for v in camera['view']):
        raise ValueError('camera.view must be positive')
    if any(not 0 <= a <= v for a, v in zip(camera['anchor'], camera['view'])):
        raise ValueError('camera.anchor must lie inside camera.view')
    limits = _rectangle(camera['limits'], 'camera.limits')
    if any(isinstance(v, bool) or not isinstance(v, int) for v in limits):
        raise ValueError('Camera2D limits must be integers')
    return [size * (0.5 - anchor/view) for size, anchor, view in
            zip(VIEW, camera['anchor'], camera['view'])]


def load_parallax(directory):
    """Validate all source assets and geometry before project output is created."""
    from export.godot_import import local_file
    root = Path(directory).resolve()
    walkable = json.loads(local_file(root/'walkable.json', root).read_text())
    _annotation(walkable)
    with Image.open(local_file(root/'foreground.png', root)) as image:
        if image.mode != 'RGBA' or list(image.size) != walkable['canvas_size']:
            raise ValueError('foreground.png must be RGBA and match canvas_size')
        image.verify()
    data = json.loads(local_file(root/'parallax.json', root).read_text())
    if not isinstance(data, dict) or not {'layers', 'camera'} <= set(data) or set(data) - {'layers', 'camera', 'movement'} or not isinstance(data['layers'], list):
        raise ValueError('parallax.json requires layers and camera')
    camera_offset(data['camera'])
    if 'movement' in data:
        movement = data['movement']
        keys = {'walk_px_s', 'run_px_s', 'walk_anim_fps', 'run_anim_fps'}
        if (not isinstance(movement, dict) or set(movement) != keys or
                any(not _number(v) or v <= 0 for v in movement.values())):
            raise ValueError('movement requires four finite positive speeds and animation fps')
    names = set()
    for layer in data['layers']:
        if not isinstance(layer, dict) or set(layer) != {'name', 'file', 'scroll_scale', 'position', 'z'}:
            raise ValueError('Each layer requires name, file, scroll_scale, position and z')
        name = layer['name']
        if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', name) or name in names:
            raise ValueError('Layer names must be unique safe node names')
        names.add(name)
        if not _number(layer['scroll_scale']) or layer['scroll_scale'] < 0:
            raise ValueError('scroll_scale must be finite and nonnegative')
        position = layer['position']
        if not isinstance(position, list) or len(position) != 2 or not all(_number(v) for v in position):
            raise ValueError('Layer position must be finite [x,y]')
        z = layer['z']
        if isinstance(z, bool) or not isinstance(z, int) or not -4096 <= z <= 4096:
            raise ValueError('Layer z must be an integer in the Godot range [-4096,4096]')
        file = layer['file']
        if (not isinstance(file, str) or Path(file).is_absolute() or '..' in Path(file).parts
                or Path(file).suffix.lower() != '.png'):
            raise ValueError('Layer file must be a relative PNG path within DIR')
        with Image.open(local_file(root/file, root)) as image:
            image.verify()
    return {'root': root, 'walkable': walkable,
            'layers': sorted(data['layers'], key=lambda layer: layer['z']), 'camera': data['camera'],
            **({'movement': data['movement']} if 'movement' in data else {})}


def tile_foreground(foreground_png, out_dir, tile_size=4096):
    """Lossless integer crops; return file, position and size for each tile."""
    if isinstance(tile_size, bool) or not isinstance(tile_size, int) or not 1 <= tile_size <= 4096:
        raise ValueError('tile_size must be an integer from 1 through 4096')
    out = Path(out_dir)
    with Image.open(foreground_png) as source:
        if source.mode != 'RGBA':
            raise ValueError('Foreground must be RGBA')
        source.load()
        out.mkdir(parents=True, exist_ok=True)
        records = []
        for y in range(0, source.height, tile_size):
            for x in range(0, source.width, tile_size):
                w, h = min(tile_size, source.width-x), min(tile_size, source.height-y)
                file = f'tile_{x}_{y}.png'
                source.crop((x, y, x+w, y+h)).save(out/file)
                records.append({'file': file, 'position': [x, y], 'size': [w, h]})
    return records


def collision_polygons(walkable):
    """Every blocked polygon, plus the exact walkable-union complement in bounds.

    Reuse the existing exact slab decomposition; clip its convex complement
    pieces to bounds with half-plane clipping. Blocked inputs remain verbatim.
    No raster approximation or new polygon dependency is needed.
    """
    annotation = _annotation(walkable)
    result = collision(annotation)
    count = len(annotation['blocked'])
    clipped = result[:count]
    x0, y0, x1, y1 = walkable['bounds']
    for polygon in result[count:]:
        for axis, limit, sign in ((0, x0, 1), (0, x1, -1), (1, y0, 1), (1, y1, -1)):
            output = []
            for a, b in zip(polygon, polygon[1:]+polygon[:1]):
                ain, bin = sign*(a[axis]-limit) >= 0, sign*(b[axis]-limit) >= 0
                if ain != bin:
                    t = (limit-a[axis])/(b[axis]-a[axis])
                    intersection = [a[k]+t*(b[k]-a[k]) for k in (0, 1)]
                    intersection[axis] = limit  # Exact boundary despite floating roundoff.
                    output.append(intersection)
                if bin:
                    output.append(b)
            polygon = output
        clean = []
        for p in polygon:
            if not clean or math.dist(p, clean[-1]) > 1e-9:
                clean.append(p)
        if len(clean) > 1 and math.dist(clean[0], clean[-1]) <= 1e-9:
            clean.pop()
        area2 = sum(a[0]*b[1]-b[0]*a[1] for a, b in zip(clean, clean[1:]+clean[:1]))
        if len(clean) >= 3 and abs(area2) > 1e-9:
            clipped.append(clean)
    return clipped


def write_cliffside(out, parallax, props=None):
    """Extend an exported Keeper project with validated cliffside inputs."""
    from export.godot_import import _project_settings
    started = time.monotonic()
    out = Path(out)
    root, walkable = parallax['root'], parallax['walkable']
    target = out/'parallax'
    tiles = tile_foreground(root/'foreground.png', target/'tiles')
    for file in ('walkable.json', 'parallax.json'):
        shutil.copyfile(root/file, target/file)
    shadow_texture(target/'shadow.png')
    height = walkable['figure_height_px']
    scale = height/240.0
    movement = parallax.get('movement', {})
    walk_speed = movement.get('walk_px_s', 150*scale)
    run_speed = movement.get('run_px_s', 250*scale)
    offset = camera_offset(parallax['camera'])
    polygons = collision_polygons(walkable)
    external = [
        '[ext_resource type="Script" path="res://scripts/keeper.gd" id="Keeper"]',
        '[ext_resource type="SpriteFrames" path="res://frames/keeper.tres" id="Frames"]',
        '[ext_resource type="Texture2D" path="res://parallax/shadow.png" id="Shadow"]']
    feet = [[height*0.11*math.cos(i*math.tau/32), height*0.04*math.sin(i*math.tau/32)] for i in range(32)]
    nodes = f'''[sub_resource type="ConvexPolygonShape2D" id="Feet"]
points = {_packed(feet)}

[node name="Cliffside" type="Node2D"]
'''
    for i, layer in enumerate(parallax['layers']):
        file = 'parallax/layers/'+layer['name']+'.png'
        (out/file).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root/layer['file'], out/file)
        external.append(f'[ext_resource type="Texture2D" path="res://{file}" id="Layer{i}"]')
        # Parallax2D computes position from scroll_offset on camera updates.
        # Set both so the supplied position survives the first such update.
        nodes += f'''
[node name="Layer_{layer['name']}" type="Parallax2D" parent="."]
z_index = {layer['z']}
position = {_vector(layer['position'])}
scroll_offset = {_vector(layer['position'])}
scroll_scale = {_vector([layer['scroll_scale']]*2)}

[node name="Sprite2D" type="Sprite2D" parent="Layer_{layer['name']}"]
texture = ExtResource("Layer{i}")
centered = false
'''
    for i, tile in enumerate(tiles):
        external.append(f'[ext_resource type="Texture2D" path="res://parallax/tiles/{tile["file"]}" id="Tile{i}"]')
        nodes += f'''
[node name="Foreground_{i}" type="Sprite2D" parent="."]
z_index = 0
texture_filter = 1
position = {_vector(tile['position'])}
texture = ExtResource("Tile{i}")
centered = false
'''
    nodes += '\n[node name="Walls" type="StaticBody2D" parent="."]\ncollision_layer = 1\ncollision_mask = 1\n'
    for i, polygon in enumerate(polygons):
        nodes += f'\n[node name="Collision_{i}" type="CollisionPolygon2D" parent="Walls"]\npolygon = {_packed(polygon)}\n'
    nodes += f'''
[node name="Keeper" type="CharacterBody2D" parent="."]
z_index = 1
position = {_vector(walkable['spawn'])}
script = ExtResource("Keeper")
motion_mode = 1
collision_layer = 1
collision_mask = 1
walk_speed = {walk_speed:.12g}
run_speed = {run_speed:.12g}
staff_tip_offset = {_vector([0, -160*scale])}

[node name="ContactShadow" type="Sprite2D" parent="Keeper"]
z_index = -1
texture = ExtResource("Shadow")
scale = {_vector([height*0.22/64, height*0.08/20])}

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="Keeper"]
sprite_frames = ExtResource("Frames")
centered = false
offset = Vector2(-256, -400)
scale = {_vector([scale, scale])}

[node name="CollisionShape2D" type="CollisionShape2D" parent="Keeper"]
shape = SubResource("Feet")

[node name="Camera2D" type="Camera2D" parent="Keeper"]
position = Vector2(0, 0)
offset = {_vector(offset)}
position_smoothing_enabled = false
limit_smoothed = false
'''
    for name, value in zip(('left', 'top', 'right', 'bottom'), parallax['camera']['limits']):
        nodes += f'limit_{name} = {value}\n'
    extra_subresources = []
    props_report = None
    if props is not None:
        from export.props_layer import near_coverage, write_layers
        # Measure opaque frame width, respecting the existing figure scale.
        widths = []
        for path in sorted((out/'sprites').rglob('*.png')):
            with Image.open(path) as image:
                bbox = image.getchannel('A').point(lambda a: 255 if a >= 128 else 0).getbbox()
                if bbox:
                    widths.append(bbox[2]-bbox[0])
        body_width = max(widths, default=48/scale)*scale
        fragments = write_layers(out, props, body_width=body_width)
        external.extend(fragments['external'])
        extra_subresources = fragments['subresources']
        keeper_header = '[node name="Keeper" type="CharacterBody2D" parent="."]\nz_index = 1'
        nodes = nodes.replace(keeper_header, fragments['collisions']+fragments['before_keeper']+
                              '\n[node name="Keeper" type="CharacterBody2D" parent="Actors"]')
        nodes = nodes.replace('parent="Keeper"', 'parent="Actors/Keeper"')
        nodes += fragments['after_keeper']
        props_report = {**fragments['counts'], 'collision_polygons': sum(
            a['collide'] for i in props['instances'] for a in props['assets'] if a['name'] == i['asset']),
            'body_width_px': body_width, 'body_height_px': 130,
            'near_coverage': near_coverage(props, walkable, parallax['camera']),
            'coverage_step_px': 64, 'opaque_alpha_min': 128}
    (out/'scenes/cliffside.tscn').write_text(f'[gd_scene load_steps={len(external)+len(extra_subresources)+2} format=3]\n\n'+'\n'.join(external)+'\n\n'+''.join(extra_subresources)+nodes)
    settings = _project_settings().replace('res://scenes/main.tscn', 'res://scenes/cliffside.tscn')
    settings = settings.replace('viewport_width=960', 'viewport_width=1920')
    settings = settings.replace('viewport_height=640', 'viewport_height=1080\nwindow/stretch/mode="canvas_items"')
    (out/'project.godot').write_text(settings)
    readme = (out/'README.md').read_text().replace('No combat logic or collision geometry.', 'The cliffside scene supplies floor collision geometry.')
    readme += ('\n\nCliffside: --parallax DIR selects scenes/cliffside.tscn. Foreground tiles\n'
               'use nearest filtering (texture_filter = 1), no padding or resampling;\n'
               'their integer rectangles cover the canvas exactly. Background and mist\n'
               'entries in parallax.json.layers use identical Parallax2D handling, sorted\n'
               'by z; no repeat_size is set. Positions are retained as scroll_offset.\n'
               'The Camera2D follows Keeper without smoothing. Its offset preserves\n'
               'anchor/view fractions in the 1920x1080 viewport. Limits take priority\n'
               'near world edges, where feet can leave that screen anchor.\n'
               f'Figure scale {scale:g}; walk/run speeds {walk_speed:g}/{run_speed:g} px/s.\n')
    (out/'README.md').write_text(readme)
    report = {'canvas_size': walkable['canvas_size'], 'tiles': tiles, 'tile_count': len(tiles),
              'tile_area_px2': sum(t['size'][0]*t['size'][1] for t in tiles),
              'filtering': 'nearest (texture_filter=1), no padding, no resampling',
              'layers': parallax['layers'], 'collision_polygons': len(polygons),
              'figure_height_px': height, 'scale': scale, 'walk_speed': walk_speed,
              'run_speed': run_speed, 'camera_offset': offset,
              'camera_anchor_px': [v/2-o for v, o in zip(VIEW, offset)],
              'camera_limits': parallax['camera']['limits'], 'wall_s': time.monotonic()-started}
    if props_report is not None:
        report['props'] = props_report
        report['near_coverage'] = props_report['near_coverage']
    if movement:
        report['movement'] = movement
    (target/'export.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    return report
