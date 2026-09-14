"""T3k synthetic cliffside contracts, malformed inputs and engine probe.

Fixture: PYTHONPATH=. python3 -B tests/test_parallax_scene.py --fixture DIR
"""
import copy
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import unittest

import numpy as np
from PIL import Image, ImageDraw
from export.godot_import import build_project, validate_resources
from export.parallax_scene import (camera_offset, collision_polygons, load_parallax,
                                   tile_foreground)
def contains(point, polygon):
    # Independent winding-number oracle, including boundaries.
    x, y = point
    winding = 0
    for a, b in zip(polygon, polygon[1:]+polygon[:1]):
        cross = (b[0]-a[0])*(y-a[1])-(x-a[0])*(b[1]-a[1])
        if abs(cross) < 1e-8 and min(a[0], b[0]) <= x <= max(a[0], b[0]) and min(a[1], b[1]) <= y <= max(a[1], b[1]):
            return True
        if a[1] <= y < b[1] and cross > 0:
            winding += 1
        elif b[1] <= y < a[1] and cross < 0:
            winding -= 1
    return winding != 0


def area(polygon):
    return abs(sum(a[0]*b[1]-b[0]*a[1] for a, b in zip(polygon, polygon[1:]+polygon[:1])))/2

TMP = Path(__file__).resolve().parent/'tmp'
GODOT = '/Applications/Godot.app/Contents/MacOS/Godot'


def rectangle(x0, y0, x1, y1):
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]


def geometry(size=(5000, 4000)):
    w, h = size
    return {'canvas_size': list(size), 'walkable': [rectangle(100, 100, w-100, h-100)],
            'blocked': [rectangle(w/2+200, h/2-100, w/2+300, h/2+100)],
            'spawn': [w/2, h/2], 'bounds': [0, 0, w, h], 'figure_height_px': 120}


def make_inputs(root, size=(5000, 4000)):
    root = Path(root)
    source, cells = root/'input', root/'cells'
    source.mkdir(parents=True)
    cells.mkdir()
    w, h = size
    # Nonconstant RGB and alpha expose coordinate, edge and alpha mistakes.
    rgba = np.empty((h, w, 4), dtype=np.uint8)
    x, y = np.arange(w, dtype=np.uint16)[None, :], np.arange(h, dtype=np.uint16)[:, None]
    rgba[:, :, 0] = x % 251
    rgba[:, :, 1] = y % 253
    rgba[:, :, 2] = (x+y) % 255
    rgba[:, :, 3] = (3*x+7*y) % 256
    Image.fromarray(rgba).save(source/'foreground.png')
    data = geometry(size)
    (source/'walkable.json').write_text(json.dumps(data))
    (source/'layers').mkdir()
    for name, color in (('far', (10, 30, 60, 255)), ('near', (40, 80, 100, 180))):
        Image.new('RGBA', (48, 32), color).save(source/'layers'/f'{name}.png')
    layers = [{'name': 'near', 'file': 'layers/near.png', 'scroll_scale': 0.7,
               'position': [70, -30], 'z': -2},
              {'name': 'far', 'file': 'layers/far.png', 'scroll_scale': 0.12,
               'position': [-10, 20], 'z': -10}]
    parallax = {'layers': layers, 'camera': {'anchor': [962, 595], 'view': [1920, 1080],
                                          'limits': [0, 0, w, h]}}
    (source/'parallax.json').write_text(json.dumps(parallax))
    frame = Image.new('RGBA', (512, 512))
    draw = ImageDraw.Draw(frame)
    draw.rectangle((236, 160, 275, 399), fill=(40, 110, 160, 255))
    for name in ('idle_S', 'walk_E', 'run_E', 'cast_E'):
        frame.save(cells/f'{name}_0.png')
    kit = root/'kit'
    for name in ('flare', 'impact'):
        (kit/name).mkdir(parents=True)
        Image.new('RGBA', (16, 16), (100, 200, 255, 180)).save(kit/name/f'{name}_0.png')
    (kit/'CREDITS.txt').write_text('Synthetic solid-color test assets; no external artwork.\n')
    sockets = root/'sockets.json'
    sockets.write_text(json.dumps({'version': 1, 'canvas': [512, 512],
                                 'cells': {'cast_E': {'sockets': [[300, 300]], 'release_index': 0}}}))
    return source, cells, kit, sockets


def scene_nodes(text):
    return {m[1]: m[2] for m in re.finditer(r'\[node name="([^"]+)"[^\n]*\]\n(.*?)(?=\n\[node|\Z)', text, re.S)}


def vector(text, name):
    return [float(v) for v in re.search(r'^'+name+r' = Vector2\(([^)]+)\)', text, re.M)[1].split(',')]


def scene_polygons(text):
    result = []
    for match in re.finditer(r'^polygon = PackedVector2Array\(([^)]+)\)', text, re.M):
        v = [float(s) for s in match[1].split(',')]
        result.append([v[i:i+2] for i in range(0, len(v), 2)])
    return result


def measure_fixture(source, project):
    text = (project/'scenes/cliffside.tscn').read_text()
    nodes = scene_nodes(text)
    declarations = dict(re.findall(r'\[ext_resource type="Texture2D" path="res://([^"]+)" id="([^"]+)"\]', text))
    textures = {ident: path for path, ident in declarations.items()}
    with Image.open(source/'foreground.png') as image:
        original = np.array(image)
    reconstructed = np.zeros_like(original)
    coverage = np.zeros(original.shape[:2], dtype=np.uint8)
    tile_sizes = []
    for name, node in nodes.items():
        if not name.startswith('Foreground_'):
            continue
        x, y = map(int, vector(node, 'position'))
        ident = re.search(r'texture = ExtResource\("([^"]+)"\)', node)[1]
        with Image.open(project/textures[ident]) as image:
            tile = np.array(image)
            w, h = image.size
        reconstructed[y:y+h, x:x+w] = tile
        coverage[y:y+h, x:x+w] += 1
        tile_sizes.append([w, h])
    polygons = scene_polygons(text)
    offset = vector(nodes['Camera2D'], 'offset')
    settings = (project/'project.godot').read_text()
    view = [int(re.search('viewport_'+axis+r'=(\d+)', settings)[1]) for axis in ('width', 'height')]
    spawn = vector(nodes['Keeper'], 'position')
    camera_center = [s+o for s, o in zip(spawn, offset)]
    screen = [s-c+v/2 for s, c, v in zip(spawn, camera_center, view)]
    w, h = original.shape[1], original.shape[0]
    refs = validate_resources(project, include_scenes=True)
    return {'tile_count': len(tile_sizes), 'tile_sizes': tile_sizes,
            'tile_area_px2': sum(w*h for w, h in tile_sizes),
            'gaps_px': int(np.count_nonzero(coverage == 0)),
            'overlap_px': int(np.count_nonzero(coverage > 1)),
            'different_rgba_values': int(np.count_nonzero(original != reconstructed)),
            'layer_order': [n for n in nodes if n.startswith('Layer_')],
            'scroll_scales': [vector(nodes[n], 'scroll_scale') for n in nodes if n.startswith('Layer_')],
            'blocked_point_collision': any(contains((w/2+250, h/2), p) for p in polygons),
            'walkable_point_collision': any(contains(spawn, p) for p in polygons),
            'complement_point_collision': any(contains((50, h/2), p) for p in polygons),
            'camera_offset': offset, 'spawn_screen_px': screen,
            'anchor_error_px': math.dist(screen, [962, 595]),
            'resource_references': len(refs), 'missing_resources': 0,
            'main_scene': re.search(r'run/main_scene="([^"]+)"', settings)[1]}


class ParallaxSceneTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='t3k-', dir=TMP)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source, self.cells, self.kit, self.sockets = make_inputs(self.root, (1200, 900))

    def test_large_fixture_exact_tiles_layers_collision_camera_and_resources(self):
        source, cells, kit, sockets = make_inputs(self.root/'large')
        out = self.root/'project'
        result = build_project(cells, out, parallax=source, vfx_kit=kit, sockets=sockets)
        measured = measure_fixture(source, out)
        self.assertEqual(measured['tile_count'], 2)
        self.assertEqual(measured['tile_sizes'], [[4096, 4000], [904, 4000]])
        self.assertEqual(measured['tile_area_px2'], 20000000)
        for name in ('gaps_px', 'overlap_px', 'different_rgba_values', 'anchor_error_px', 'missing_resources'):
            self.assertEqual(measured[name], 0, name)
        self.assertEqual(measured['layer_order'], ['Layer_far', 'Layer_near'])
        self.assertEqual(measured['scroll_scales'], [[0.12, 0.12], [0.7, 0.7]])
        self.assertTrue(measured['blocked_point_collision'])
        self.assertTrue(measured['complement_point_collision'])
        self.assertFalse(measured['walkable_point_collision'])
        self.assertEqual(measured['spawn_screen_px'], [962, 595])
        self.assertEqual(measured['main_scene'], 'res://scenes/cliffside.tscn')
        self.assertEqual(result['parallax']['tile_count'], 2)
        self.assertIn('nearest', result['parallax']['filtering'])

    def test_scene_figure_shadow_bounds_order_and_script_regression(self):
        plain, out = self.root/'plain', self.root/'project'
        build_project(self.cells, plain)
        result = build_project(self.cells, out, parallax=self.source)
        for file in ('scenes/main.tscn', 'scripts/keeper.gd', 'frames/keeper.tres'):
            self.assertEqual((out/file).read_bytes(), (plain/file).read_bytes())
        text = (out/'scenes/cliffside.tscn').read_text()
        nodes = scene_nodes(text)
        self.assertNotIn('repeat_size', text)
        self.assertIn('parent="Keeper"', re.search(r'\[node name="Camera2D"[^\n]+', text)[0])
        self.assertLess(text.index('name="Walls"'), text.index('name="Keeper"'))
        for name in ('far', 'near'):
            node = nodes['Layer_'+name]
            self.assertEqual(vector(node, 'position'), vector(node, 'scroll_offset'))
        self.assertIn('texture_filter = 1', nodes['Foreground_0'])
        self.assertEqual(vector(nodes['AnimatedSprite2D'], 'offset'), [-256, -400])
        self.assertEqual(vector(nodes['AnimatedSprite2D'], 'scale'), [0.5, 0.5])
        self.assertIn('walk_speed = 75', nodes['Keeper'])
        self.assertIn('run_speed = 125', nodes['Keeper'])
        self.assertIn('z_index = -1', nodes['ContactShadow'])
        self.assertEqual(vector(nodes['ContactShadow'], 'scale'), [26.4/64, 9.6/20])
        self.assertIn('position_smoothing_enabled = false', nodes['Camera2D'])
        for side, value in zip(('left', 'top', 'right', 'bottom'), (0, 0, 1200, 900)):
            self.assertIn(f'limit_{side} = {value}', nodes['Camera2D'])
        self.assertEqual(result['parallax']['scale'], 0.5)
        self.assertIn('window/stretch/mode="canvas_items"', (out/'project.godot').read_text())

    def test_optional_mist_is_a_normal_layer_and_stable_z_ties(self):
        path = self.source/'parallax.json'
        data = json.loads(path.read_text())
        (self.source/'mist').mkdir()
        Image.new('RGBA', (12, 10)).save(self.source/'mist/fog.png')
        data['layers'].append({'name': 'fog', 'file': 'mist/fog.png', 'scroll_scale': 0.9,
                               'position': [5, 6], 'z': -2})
        path.write_text(json.dumps(data))
        out = self.root/'project'
        result = build_project(self.cells, out, parallax=self.source)
        self.assertEqual([x['name'] for x in result['parallax']['layers']], ['far', 'near', 'fog'])
        self.assertEqual((out/'parallax/layers/fog.png').read_bytes(), (self.source/'mist/fog.png').read_bytes())
        self.assertIn('scroll_scale = Vector2(0.9, 0.9)', (out/'scenes/cliffside.tscn').read_text())

    def test_vfx_kit_and_sockets_match_existing_export_and_static_collision_mask(self):
        plain, out = self.root/'kit_plain', self.root/'project'
        build_project(self.cells, plain, vfx_kit=self.kit, sockets=self.sockets)
        report = build_project(self.cells, out, parallax=self.source, vfx_kit=self.kit, sockets=self.sockets)
        for file in ('scripts/keeper.gd', 'scripts/frost_bolt.gd', 'scripts/frost_impact.gd',
                     'scenes/frost_bolt.tscn', 'scenes/frost_impact.tscn', 'sockets.json'):
            self.assertEqual((out/file).read_bytes(), (plain/file).read_bytes())
        self.assertIn('collision_mask = 1', (out/'scenes/frost_bolt.tscn').read_text())
        self.assertIn('collision_layer = 1', scene_nodes((out/'scenes/cliffside.tscn').read_text())['Walls'])
        self.assertEqual(report['vfx_kit']['missing_sockets'], 0)
        self.assertIsNone(report['vfx_kit']['ambient_rectangle'])

    def test_bounded_complement_clips_exactly_and_preserves_blocked(self):
        data = geometry((1200, 900))
        data['bounds'] = [50.25, 60.5, 1150.75, 850.5]
        result = collision_polygons(data)
        self.assertEqual(result[0], data['blocked'][0])
        self.assertAlmostEqual(sum(area(p) for p in result[1:]), 1100.5*790-1000*700)
        for poly in result[1:]:
            for x, y in poly:
                self.assertTrue(50.25 <= x <= 1150.75 and 60.5 <= y <= 850.5)
        self.assertTrue(any(contains((70, 450), p) for p in result))
        self.assertFalse(any(contains((40, 450), p) for p in result))
        self.assertFalse(any(contains((600, 450), p) for p in result))

    def test_overlap_union_concavity_holes_and_winding(self):
        data = geometry((1200, 900))
        data['walkable'] = [rectangle(100, 100, 800, 500), rectangle(400, 300, 1100, 800)]
        data['spawn'] = [500, 400]
        data['blocked'] = []
        result = collision_polygons(data)
        self.assertAlmostEqual(sum(area(p) for p in result), 1200*900-(700*400+700*500-400*200))
        for y in range(25, 900, 50):
            for x in range(25, 1200, 50):
                expected = not any(contains((x, y), p) for p in data['walkable'])
                self.assertEqual(any(contains((x, y), p) for p in result), expected)
        data['walkable'] = [list(reversed(p)) for p in reversed(data['walkable'])]
        self.assertAlmostEqual(sum(area(p) for p in collision_polygons(data)), sum(area(p) for p in result))
        data['walkable'] = [rectangle(100, 100, 1100, 200), rectangle(100, 700, 1100, 800),
                            rectangle(100, 200, 200, 700), rectangle(1000, 200, 1100, 700)]
        data['spawn'] = [150, 400]
        self.assertTrue(any(contains((600, 450), p) for p in collision_polygons(data)))
        data['walkable'] = [[[100, 100], [1100, 100], [1100, 300], [300, 300], [300, 800], [100, 800]]]
        self.assertTrue(any(contains((600, 450), p) for p in collision_polygons(data)))
        self.assertFalse(any(contains((150, 450), p) for p in collision_polygons(data)))

    def test_camera_fraction_and_known_bad_camera(self):
        camera = {'anchor': [481, 297.5], 'view': [960, 540], 'limits': [0, 0, 5000, 4000]}
        np.testing.assert_allclose(camera_offset(camera), [-2, -55], atol=1e-10)
        for key, values in {'anchor': [[-1, 0], [961, 0], [True, 10], [float('nan'), 0], None],
                            'view': [[0, 540], [-1, 540], [960], [960, float('inf')]],
                            'limits': [[0, 0, 0, 4000], [0, 0, 5000.5, 4000], [0, 0, True, 2]]}.items():
            for value in values:
                with self.subTest(key=key, value=value):
                    bad = copy.deepcopy(camera);bad[key] = value
                    with self.assertRaises(ValueError): camera_offset(bad)

    def test_bad_walkable_schema_geometry_spawn_and_bounds(self):
        data = geometry((1200, 900))
        bads = []
        for key in data:
            bad = copy.deepcopy(data);del bad[key];bads.append(bad)
        for key, values in {'canvas_size': [[1200.5, 900], [True, 900], [0, 900]],
                            'spawn': [[850, 450], [10, 10], [float('nan'), 450]],
                            'figure_height_px': [0, True, float('inf')],
                            'bounds': [[0, 0, 1201, 900], [0, 0, 1200, 0], [0, 0, 500, 400]],
                            'walkable': [[], [[[10, 10], [100, 100], [10, 100], [90, 10]]]],
                            'blocked': [[[[1, 1], [2, 2], [3, 3]]]]}.items():
            for value in values:
                bad = copy.deepcopy(data);bad[key] = value;bads.append(bad)
        for i, bad in enumerate(bads):
            with self.subTest(case=i):
                with self.assertRaises(ValueError): collision_polygons(bad)

    def test_bad_layer_fields_paths_missing_and_escaping_assets_before_output(self):
        path = self.source/'parallax.json'
        original = json.loads(path.read_text())
        for key, values in {'name': ['../x', 'x"', ''], 'scroll_scale': [-1, True, float('nan')],
                            'position': [[1], [1, float('inf')]], 'z': [1.5, True, 4097],
                            'file': ['../outside.png', '/absolute.png', 'layers/missing.png']}.items():
            for value in values:
                with self.subTest(key=key, value=value):
                    bad = copy.deepcopy(original);bad['layers'][0][key] = value
                    path.write_text(json.dumps(bad))
                    with self.assertRaises(ValueError): build_project(self.cells, self.root/'bad', parallax=self.source)
                    self.assertFalse((self.root/'bad').exists())
        bad = copy.deepcopy(original);bad['layers'].append(bad['layers'][0])
        path.write_text(json.dumps(bad))
        with self.assertRaises(ValueError): load_parallax(self.source)
        path.write_text(json.dumps(original))
        asset = self.source/'layers/near.png'
        outside = self.root/'outside.png';asset.rename(outside);asset.symlink_to(outside)
        with self.assertRaises(ValueError): load_parallax(self.source)

    def test_bad_foreground_mode_size_and_conflicting_overlapping_inputs(self):
        for mode, size in (('RGB', (1200, 900)), ('RGBA', (1199, 900))):
            Image.new(mode, size).save(self.source/'foreground.png')
            with self.assertRaises(ValueError): build_project(self.cells, self.root/'bad', parallax=self.source)
            self.assertFalse((self.root/'bad').exists())
        Image.new('RGBA', (1200, 900)).save(self.source/'foreground.png')
        with self.assertRaises(ValueError): build_project(self.cells, self.source/'out', parallax=self.source)
        with self.assertRaises(ValueError): build_project(self.cells, self.root/'bad', scene=self.source, parallax=self.source)
        with self.assertRaises(ValueError): build_project(self.cells, self.root/'bad', parallax=self.source, sockets=self.sockets)
        with self.assertRaises(ValueError): build_project(self.cells, self.root/'bad', parallax=self.root/'missing')

    def test_tile_size_edges_vertical_splits_and_bad_parameters(self):
        Image.new('RGBA', (9, 9), (1, 2, 3, 4)).save(self.root/'small.png')
        records = tile_foreground(self.root/'small.png', self.root/'tiles', tile_size=4)
        self.assertEqual(len(records), 9)
        self.assertEqual(records[-1]['position'], [8, 8])
        self.assertEqual(records[-1]['size'], [1, 1])
        self.assertEqual(sum(t['size'][0]*t['size'][1] for t in records), 81)
        for size in (0, -1, True, 4097, 4.5):
            with self.assertRaises(ValueError): tile_foreground(self.root/'small.png', self.root/'bad', size)
        Image.new('RGB', (9, 9)).save(self.root/'small.png')
        with self.assertRaises(ValueError): tile_foreground(self.root/'small.png', self.root/'bad')

    def test_missing_export_texture_is_detected(self):
        out = self.root/'project'
        build_project(self.cells, out, parallax=self.source)
        (out/'parallax/tiles/tile_0_0.png').unlink()
        with self.assertRaises(ValueError): validate_resources(out, include_scenes=True)

    def test_cli_parallax_and_directional_kit(self):
        out = self.root/'project'
        proc = subprocess.run([sys.executable, '-B', '-m', 'export.godot_import', '--cells', str(self.cells),
                               '--out', str(out), '--parallax', str(self.source), '--vfx-kit', str(self.kit),
                               '--sockets', str(self.sockets)], capture_output=True, text=True, timeout=30)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)['parallax']['canvas_size'], [1200, 900])
        self.assertTrue((out/'scenes/frost_bolt.tscn').is_file())

    @unittest.skipUnless(Path(GODOT).is_file(), 'Godot binary unavailable')
    def test_headless_cliffside_follow_camera_parallax_and_projectile_collision(self):
        source, cells, kit, sockets = make_inputs(self.root/'large')
        out = self.root/'project'
        build_project(cells, out, parallax=source, vfx_kit=kit, sockets=sockets)
        (out/'probe.gd').write_text(PROBE)
        errors = []
        for args in (['--import'], ['--script', 'res://probe.gd']):
            proc = subprocess.run([GODOT, '--headless', '--path', str(out), *args],
                                  capture_output=True, text=True, timeout=90)
            log = proc.stdout+proc.stderr
            self.assertEqual(proc.returncode, 0, log)
            self.assertNotIn('SCRIPT ERROR', log)
            errors.extend(line for line in log.splitlines() if 'ERROR' in line)
            self.assertNotIn('T3K_ASSERTION:', log)
        self.assertIn('T3K_RUNTIME_ASSERTIONS=complete', log)
        self.assertEqual(errors, [], '\n'.join(errors))


PROBE = '''extends SceneTree

func check(value: bool, message: String) -> void:
    if not value:
        printerr("T3K_ASSERTION: ", message)
        quit(7)

func _initialize() -> void:
    call_deferred("probe")

func probe() -> void:
    root.size = Vector2i(1920, 1080)
    var scene = load("res://scenes/cliffside.tscn").instantiate()
    root.add_child(scene)
    await process_frame
    await physics_frame
    var keeper = scene.get_node("Keeper")
    keeper.set_physics_process(false)
    var camera = keeper.get_node("Camera2D")
    camera.make_current()
    camera.force_update_scroll()
    await process_frame
    check(camera.get_parent() == keeper, "camera follows keeper")
    check(not camera.position_smoothing_enabled, "no smoothing")
    check(keeper.sprite.to_global(Vector2(256,400)+keeper.sprite.offset).is_equal_approx(keeper.global_position), "feet pivot")
    check(keeper.sprite.scale == Vector2(0.5,0.5), "figure scale")
    check(keeper.walk_speed == 75 and keeper.run_speed == 125, "movement scale")
    check(scene.get_node("Foreground_0").texture_filter == 1, "nearest tiles")
    var screen: Vector2 = keeper.get_global_transform_with_canvas().origin
    check(screen.is_equal_approx(Vector2(962,595)), "spawn screen anchor")
    var far = scene.get_node("Layer_far/Sprite2D")
    var near_layer = scene.get_node("Layer_near/Sprite2D")
    var before_far: Vector2 = far.get_global_transform_with_canvas().origin
    var before_near: Vector2 = near_layer.get_global_transform_with_canvas().origin
    keeper.position += Vector2(100,50)
    camera.force_update_scroll()
    await process_frame
    check(keeper.get_global_transform_with_canvas().origin.is_equal_approx(screen), "moving anchor")
    check((far.get_global_transform_with_canvas().origin-before_far).is_equal_approx(Vector2(-12,-6)), "far scroll")
    check((near_layer.get_global_transform_with_canvas().origin-before_near).is_equal_approx(Vector2(-70,-35)), "near scroll")
    await physics_frame
    var space = scene.get_world_2d().direct_space_state
    for pair in [[Vector2(2750,2000), true], [Vector2(50,2000), true], [Vector2(2500,2000), false]]:
        var query = PhysicsPointQueryParameters2D.new()
        query.position = pair[0]
        query.exclude = [keeper.get_rid()]
        check((space.intersect_point(query).size() > 0) == pair[1], "collision point")
    var bolt = load("res://scenes/frost_bolt.tscn").instantiate()
    bolt.direction = Vector2.RIGHT
    bolt.spell_scale = 0.5
    bolt.caster = keeper
    scene.add_child(bolt)
    bolt.global_position = Vector2(2690,2000)
    bolt.set_physics_process(false)
    bolt._physics_process(0.1)
    check(bolt.expired, "projectile hits StaticBody2D")
    check(absf(bolt.global_position.x-2700) < 0.01, "projectile impact position")
    print("T3K_RUNTIME_ASSERTIONS=complete")
    scene.queue_free()
    await process_frame
    quit(0)
'''


def build_fixture(directory):
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    source, cells, kit, sockets = make_inputs(root/'fixture_inputs')
    project = root/'fixture_project'
    report = build_project(cells, project, parallax=source, vfx_kit=kit, sockets=sockets)
    measured = measure_fixture(source, project)
    metrics = []
    for name in ('tile_count', 'tile_area_px2', 'gaps_px', 'overlap_px', 'different_rgba_values', 'anchor_error_px', 'missing_resources'):
        threshold = {'tile_count': 2, 'tile_area_px2': 20000000}.get(name, 0)
        metrics.append({'id': 't3k_'+name, 'subject': 'synthetic_cliffside', 'passed': None,
                        'value': measured[name], 'threshold': threshold, 'op': '==',
                        'unit': 'px' if name.endswith('_px') else 'count',
                        'evidence': ['fixture_project/scenes/cliffside.tscn'],
                        'notes': 'Measured instrument only; conductor owns acceptance.'})
    result = {'measured': measured, 'export': report, 'metrics': metrics,
              'wall_s': time.monotonic()-started}
    (root/'acceptance.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--fixture':
        print(json.dumps(build_fixture(sys.argv[2]), indent=2))
    else:
        unittest.main()
