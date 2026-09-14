"""T3l layered cliffside contracts and malformed inputs.

PYTHONPATH=.:tests python3 -B tests/test_props_layer.py --fixture runs/C-3/t3/T3l
"""
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from PIL import Image, ImageDraw
from export.godot_import import build_project, validate_resources
from export.parallax_scene import load_parallax
from export.props_layer import load_props, near_coverage, _camera_top_left, ellipse, write_layers, OCCLUSION_SCRIPT
from test_parallax_scene import (make_inputs, rectangle, scene_nodes, vector,
                                 scene_polygons, contains, GODOT, TMP)

BASELINE = {
    'README.md': 'd56e3f32e2cf8a45d4f1fa4bfe0c5e54a5e89007ad2a328e8fe09c6118202f40',
    'frames/keeper.tres': '039613597231247f133ba55b2d752810b8b64121d552f3e1e7f686b909340cfa',
    'parallax/export.json': 'f72c429db87bc649230ad709067492255edf4f3f11018508a5a279cca344b1a3',
    'parallax/parallax.json': 'e7677434d57020847c73b5c44314a44b7f7ae806ba454e07a32d31d64949beeb',
    'parallax/walkable.json': 'e90ccc92a55be3d1c9a29c05a7322d0a5bf380562a24743fb20fc6f821062a86',
    'project.godot': '2e99461d74d52642cb886e8a7062aaa8db73639eedb535603e5943cebd4aabba',
    'scenes/cliffside.tscn': 'b1c4e769c37aeb01a8d3b1fb5af4a8944ee5d0a555aab9978a12f4a53f18bf43',
    'scenes/main.tscn': 'a7ff2b1ba99ca306dacd7fbee1556fbfbed54d72cc8e3c01ab72e1aba58b874d',
    'scripts/keeper.gd': '89e9e64440aa00541acf90980852293abb81e345295f6d9bd9d771f7d3b67399',
}
MOVEMENT = {'walk_px_s': 173.25, 'run_px_s': 301.5, 'walk_anim_fps': 9.5, 'run_anim_fps': 17.25}


def text_hashes(project):
    return {f.relative_to(project).as_posix(): hashlib.sha256(f.read_bytes()).hexdigest()
            for f in sorted(project.rglob('*')) if f.is_file() and f.suffix != '.png'}


def make_props(root):
    root.mkdir()
    for file, size in [('tree.png', (100, 180)), ('stone.png', (60, 50)),
                       ('shadow.png', (90, 30)), ('overhead.png', (300, 180)),
                       ('near.png', (600, 360)), ('mote.png', (8, 8))]:
        im = Image.new('RGBA', size)
        d = ImageDraw.Draw(im)
        border = 10 if min(size) > 30 else 1
        d.rectangle((border, border, size[0]-border-1, size[1]-border-1), fill=(40, 90, 130, 255))
        im.save(root/file)
    data = {
        'assets': [{'name': 'tree', 'file': 'tree.png', 'anchor': [49.5, 174],
                    'footprint': {'w': 70, 'h': 24}, 'collide': True, 'fade_when_behind': True},
                   {'name': 'stone', 'file': 'stone.png', 'anchor': [30, 49],
                    'footprint': {'w': 45, 'h': 15}, 'collide': False, 'fade_when_behind': False}],
        'instances': [{'asset': 'tree', 'position': [400, 360]},
                      {'asset': 'tree', 'position': [750.5, 610.25]},
                      {'asset': 'stone', 'position': [550, 450]}],
        'shadows': [{'file': 'shadow.png', 'position': [350, 340], 'opacity': .6},
                    {'file': 'shadow.png', 'position': [700, 590], 'opacity': .35}],
        'overhead': [{'file': 'overhead.png', 'position': [300, 120]}],
        'near': [{'file': 'near.png', 'position': [0, 0], 'scroll_scale': 1.2}],
        'particles': [{'name': 'mist_motes', 'texture': 'mote.png', 'rect': [200, 200, 800, 600],
                       'amount': 37, 'lifetime_s': 2.75, 'velocity_px_s': [4.5, 12],
                       'direction': [-1, -0.2], 'spread_deg': 23, 'scale': [.2, .7],
                       'color_start': [.3, .6, .9, .8], 'color_end': [.2, .3, .5, 0]}],
    }
    (root/'props.json').write_text(json.dumps(data, indent=2)+'\n')
    return data


def half_coverage_case(root):
    """Two samples at x=2000 and x=6000, y=2000; first covers 120000px.

    First camera top-left is (1040,1460), so position (1248,1752) maps
    exactly to screen (0,0) at factor 1.2. The other sample is offscreen.
    """
    root.mkdir()
    Image.new('RGBA', (400, 300), (20, 40, 80, 255)).save(root/'near.png')
    data = {k: [] for k in ('assets', 'instances', 'shadows', 'overhead', 'near', 'particles')}
    data['near'] = [{'file': 'near.png', 'position': [1248, 1752], 'scroll_scale': 1.2}]
    (root/'props.json').write_text(json.dumps(data))
    walkable = {'canvas_size': [8000, 4000], 'walkable': [rectangle(0, 0, 8000, 4000)],
                'blocked': [], 'spawn': [2000, 2000], 'bounds': [0, 0, 8000, 4000], 'figure_height_px': 130}
    camera = {'anchor': [960, 540], 'view': [1920, 1080], 'limits': [0, 0, 8000, 4000]}
    return load_props(root), walkable, camera


class PropsLayerTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='t3l-', dir=TMP)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source, self.cells, self.kit, self.sockets = make_inputs(self.root, (1200, 900))
        self.props = self.root/'props'
        self.data = make_props(self.props)

    def export(self, **kwargs):
        out = self.root/'project'
        report = build_project(self.cells, out, parallax=self.source, props=self.props, **kwargs)
        return out, report, (out/'scenes/cliffside.tscn').read_text()

    def test_layers_anchors_y_sort_z_order_and_fade_assignment(self):
        out, result, text = self.export()
        nodes = scene_nodes(text)
        self.assertIn('y_sort_enabled = true', nodes['Actors'])
        self.assertIn('[node name="Keeper" type="CharacterBody2D" parent="Actors"]', text)
        self.assertNotIn('z_index', nodes['Keeper'])  # same effective z as props for y-sort
        props = re.findall(r'\[node name="Prop_\d+" type="Sprite2D" parent="Actors"\]', text)
        self.assertEqual(len(props), 3)
        for i, instance in enumerate(self.data['instances']):
            asset = next(a for a in self.data['assets'] if a['name'] == instance['asset'])
            node = nodes[f'Prop_{i}']
            self.assertEqual(vector(node, 'position'), instance['position'])
            self.assertEqual(vector(node, 'offset'), [-v for v in asset['anchor']])
            self.assertIn('centered = false', node)
            self.assertEqual('script = ExtResource("OcclusionFade")' in node, asset['fade_when_behind'])
        self.assertEqual([int(re.search(r'z_index = (-?\d+)', nodes[n])[1]) for n in
                          ('Foreground_0', 'Shadows', 'Actors', 'Overhead', 'Near_0', 'Air')], list(range(6)))
        self.assertEqual(vector(nodes['Near_0'], 'scroll_scale'), [1.2, 1.2])
        self.assertEqual(vector(nodes['Near_0'], 'scroll_offset'), self.data['near'][0]['position'])
        self.assertIn('fade_mode = 1', nodes['Overhead_0'])
        self.assertIn('fade_mode = 2', nodes['NearSprite_0'])
        for i, entry in enumerate(self.data['shadows']):
            self.assertEqual(vector(nodes[f'Shadow_{i}'], 'position'), entry['position'])
            self.assertIn(f'modulate = Color(1, 1, 1, {entry["opacity"]})', nodes[f'Shadow_{i}'])
        self.assertIn('opaque_rect = Rect2(-39.5, -164, 80, 160)', nodes['Prop_0'])
        self.assertIn('body_width = 20', nodes['Prop_0'])
        script = (out/'scripts/occlusion_fade.gd').read_text()
        for token in ('-130.0', '0.35', '0.15', 'get_global_transform_with_canvas()',
                      'keeper.global_position.y < global_position.y', 'fade_tween.kill()', 'get_rect()'):
            self.assertIn(token, script)
        self.assertEqual(result['parallax']['props']['instances'], 3)

    def test_collision_ellipses_at_anchors_and_noncollider_absent(self):
        _, result, text = self.export()
        nodes = scene_nodes(text)
        self.assertEqual([n for n in nodes if n.startswith('PropCollision_')], ['PropCollision_0', 'PropCollision_1'])
        for i in (0, 1):
            node = nodes[f'PropCollision_{i}']; polygon = scene_polygons(node)[0]
            pos = vector(node, 'position')
            self.assertEqual(len(polygon), 16)
            self.assertEqual(pos, self.data['instances'][i]['position'])
            translated = [[x+pos[0], y+pos[1]] for x, y in polygon]
            self.assertTrue(contains(pos, translated))
            self.assertFalse(contains([pos[0]+36, pos[1]], translated))
            self.assertAlmostEqual(max(x for x, _ in polygon)-min(x for x, _ in polygon), 70)
            self.assertAlmostEqual(max(y for _, y in polygon)-min(y for _, y in polygon), 24)
        self.assertEqual(result['parallax']['props']['collision_polygons'], 2)

    def test_particles_all_parameters_resources_and_texture_bytes(self):
        out, report, text = self.export()
        node = scene_nodes(text)['Particles_mist_motes']
        for value in ('amount = 37', 'lifetime = 2.75', 'local_coords = false', 'emitting = true',
                      'emission_shape = 3', 'spread = 23', 'initial_velocity_min = 4.5',
                      'initial_velocity_max = 12', 'scale_amount_min = 0.2', 'scale_amount_max = 0.7',
                      'gravity = Vector2(0, 0)', 'color_ramp = SubResource("PropsGradient0")'):
            self.assertIn(value, node)
        self.assertEqual(vector(node, 'position'), [500, 400])
        self.assertEqual(vector(node, 'emission_rect_extents'), [300, 200])
        self.assertEqual(vector(node, 'direction'), [-1, -.2])
        self.assertIn('PackedColorArray(0.3, 0.6, 0.9, 0.8, 0.2, 0.3, 0.5, 0)', text)
        refs = validate_resources(out, include_scenes=True)
        self.assertTrue(refs)
        for path in re.findall(r'path="res://([^"]+)"', text):
            self.assertTrue((out/path).is_file(), path)
        for file in load_props(self.props)['images']:
            self.assertEqual((self.props/file).read_bytes(), (out/'props'/file).read_bytes())
        exported = json.loads((out/'parallax/export.json').read_text())
        self.assertEqual(exported['near_coverage'], report['parallax']['near_coverage'])

    def test_known_half_coverage_exact_and_empty_layer_zero(self):
        props, walkable, camera = half_coverage_case(self.root/'half')
        self.assertEqual(near_coverage(props, walkable, camera, step_px=4000), .5)
        props['near'] = []
        self.assertEqual(near_coverage(props, walkable, camera, step_px=4000), 0)

    def test_coverage_alpha_holes_union_threshold_and_blocked_samples(self):
        props, walkable, camera = half_coverage_case(self.root/'half')
        # Sparse opaque support has same bounding box but less than 5% coverage.
        im = Image.new('RGBA', (400, 300), (20, 40, 80, 127))
        d = ImageDraw.Draw(im);d.rectangle((0, 0, 399, 99), fill=(20, 40, 80, 255));im.save(props['root']/'near.png')
        props['near'] *= 3  # duplicates cannot inflate union area
        self.assertEqual(near_coverage(props, walkable, camera, 4000), 0)
        Image.new('RGBA', (400, 300), (20, 40, 80, 128)).save(props['root']/'near.png')
        self.assertEqual(near_coverage(props, walkable, camera, 4000), .5)
        walkable['blocked'] = [rectangle(5900, 1900, 6100, 2100)]
        self.assertEqual(near_coverage(props, walkable, camera, 4000), 1)
        walkable['blocked'] = [rectangle(1900, 1900, 2100, 2100)]
        walkable['spawn'] = [6000, 2000]
        self.assertEqual(near_coverage(props, walkable, camera, 4000), 0)

    def test_coverage_camera_anchor_limits_and_invalid_sampling(self):
        props, walkable, camera = half_coverage_case(self.root/'half')
        camera['anchor'] = [962, 595]
        self.assertEqual(_camera_top_left([2000, 2000], camera), [1038, 1405])
        for actual, expected in zip(_camera_top_left([10, 10], camera), [-2, -55]):
            self.assertAlmostEqual(actual, expected, places=10)
        self.assertEqual(_camera_top_left([7990, 3990], camera), [6078, 2865])
        for value in (0, -1, True, float('nan'), float('inf')):
            with self.subTest(value=value), self.assertRaises(ValueError):
                near_coverage(props, walkable, camera, value)
        with self.assertRaisesRegex(ValueError, 'No walkable camera samples'):
            near_coverage(props, walkable, camera, 20000)

    def reject(self, bad):
        (self.props/'props.json').write_text(json.dumps(bad))
        out = self.root/'bad'
        with self.assertRaises(ValueError):
            build_project(self.cells, out, parallax=self.source, props=self.props)
        self.assertFalse(out.exists())

    def test_required_six_bad_cases_before_any_output(self):
        bads = []
        a = copy.deepcopy(self.data);a['surprise'] = [];bads.append(a)
        a = copy.deepcopy(self.data);a['assets'][0]['file'] = 'missing.png';bads.append(a)
        a = copy.deepcopy(self.data);a['instances'][0]['asset'] = 'unknown';bads.append(a)
        a = copy.deepcopy(self.data);a['assets'].append(a['assets'][0]);bads.append(a)
        a = copy.deepcopy(self.data);a['assets'][0]['anchor'][0] = float('nan');bads.append(a)
        a = copy.deepcopy(self.data);a['near'][0]['scroll_scale'] = 1.0;bads.append(a)
        for i, bad in enumerate(bads):
            with self.subTest(case=i): self.reject(bad)

    def test_every_collection_unknown_and_missing_keys_and_wrong_types(self):
        for key in self.data:
            for change in ('unknown', 'missing', 'not_list'):
                a = copy.deepcopy(self.data)
                if change == 'unknown': a[key][0]['surprise'] = 1
                elif change == 'missing': del a[key][0][next(iter(a[key][0]))]
                else: a[key] = {}
                with self.subTest(key=key, change=change): self.reject(a)
        a = copy.deepcopy(self.data);a['assets'][0]['footprint']['surprise'] = 'ellipse';self.reject(a)
        for key in self.data:
            a = copy.deepcopy(self.data);del a[key]
            with self.subTest(missing=key): self.reject(a)

    def test_bad_numbers_names_booleans_and_ranges(self):
        cases = {'assets': {'name': ['', '../escape', 'a"'], 'anchor': [[1], [float('inf'), 1]],
                            'footprint': [{'w': 0, 'h': 2}, {'w': 2, 'h': float('nan')}],
                            'collide': [1], 'fade_when_behind': ['false']},
                 'instances': {'position': [[float('nan'), 1], [True, 1]]},
                 'shadows': {'opacity': [-.1, 1.1, float('nan'), True]},
                 'near': {'scroll_scale': [0, -1, float('inf'), True]},
                 'particles': {'amount': [0, 513, 1.5, True], 'lifetime_s': [0, float('inf')],
                               'velocity_px_s': [[-1, 2], [3, 2], [1, float('nan')]],
                               'direction': [[0, 0], [0, float('inf')]], 'spread_deg': [-1, 181, float('nan')],
                               'scale': [[0, 1], [2, 1]], 'rect': [[1, 1, 1, 2]],
                               'color_start': [[0, 0, 0, 2]], 'color_end': [[0, 0, float('nan'), 0]]}}
        for group, fields in cases.items():
            for key, values in fields.items():
                for value in values:
                    a = copy.deepcopy(self.data);a[group][0][key] = value
                    with self.subTest(group=group, key=key, value=value): self.reject(a)
        a = copy.deepcopy(self.data);a['particles'].append(a['particles'][0]);self.reject(a)

    def test_missing_escaping_absolute_symlink_wrong_mode_and_nonpng_assets(self):
        for value in ('../outside.png', '/absolute.png', 'tree.jpg', 'dir\\tree.png', 'x".png'):
            a = copy.deepcopy(self.data);a['assets'][0]['file'] = value
            with self.subTest(file=value): self.reject(a)
        path = self.props/'tree.png';outside = self.root/'outside.png';path.rename(outside);path.symlink_to(outside)
        self.reject(self.data)
        path.unlink();Image.new('RGB', (100, 180)).save(path);self.reject(self.data)
        Image.new('RGBA', (100, 180)).save(path, format='TIFF');self.reject(self.data)
        path.write_bytes(b'not an image');self.reject(self.data)

    def test_props_requires_parallax_and_prevents_input_output_overlap(self):
        with self.assertRaisesRegex(ValueError, 'requires --parallax'):
            build_project(self.cells, self.root/'bad', props=self.props)
        self.assertFalse((self.root/'bad').exists())
        with self.assertRaises(ValueError):
            build_project(self.cells, self.props/'bad', parallax=self.source, props=self.props)
        self.assertFalse((self.props/'bad').exists())

    def test_movement_exact_speeds_fps_all_directions_and_gear(self):
        path = self.source/'parallax.json';data = json.loads(path.read_text());data['movement'] = MOVEMENT
        path.write_text(json.dumps(data))
        for anim in ('walk', 'run'):
            for direction in ('S', 'SW', 'W', 'NW', 'N', 'NE', 'SE'):
                (self.cells/f'{anim}_{direction}_0.png').write_bytes((self.cells/f'{anim}_E_0.png').read_bytes())
        out, result, text = self.export(gear_variant=self.cells)
        keeper = scene_nodes(text)['Keeper']
        self.assertIn('walk_speed = 173.25', keeper);self.assertIn('run_speed = 301.5', keeper)
        self.assertEqual(result['parallax']['scale'], .5)
        for resource in ('keeper.tres', 'keeper_advanced.tres'):
            speeds = dict(re.findall(r'"name": &"([^"]+)", "speed": ([0-9.]+)', (out/'frames'/resource).read_text()))
            self.assertEqual(len([n for n in speeds if n.startswith(('walk_', 'run_'))]), 16)
            for name, fps in speeds.items():
                self.assertEqual(float(fps), MOVEMENT[name.split('_')[0]+'_anim_fps'] if name.startswith(('walk_', 'run_')) else {'idle_S': 8, 'cast_E': 20}[name])

    def test_movement_without_props_and_invalid_movement_before_output(self):
        path = self.source/'parallax.json';data = json.loads(path.read_text());data['movement'] = MOVEMENT
        path.write_text(json.dumps(data));out = self.root/'movement'
        build_project(self.cells, out, parallax=self.source)
        self.assertIn('walk_speed = 173.25', (out/'scenes/cliffside.tscn').read_text())
        self.assertNotIn('name="Actors"', (out/'scenes/cliffside.tscn').read_text())
        for bad in ({}, {**MOVEMENT, 'extra': 1}, None, *[{**MOVEMENT, key: value} for key in MOVEMENT for value in (0, -1, True, float('nan'), float('inf'))]):
            data['movement'] = bad;path.write_text(json.dumps(data))
            with self.subTest(movement=bad), self.assertRaises(ValueError):
                build_project(self.cells, self.root/'bad', parallax=self.source)
            self.assertFalse((self.root/'bad').exists())

    def test_absent_movement_props_byte_identical_to_frozen_t3k_all_text(self):
        out = self.root/'baseline'
        with patch('time.monotonic', return_value=0.0):
            build_project(self.cells, out, parallax=self.source)
        self.assertEqual(text_hashes(out), BASELINE)

    def test_unused_asset_empty_collections_and_no_unneeded_fade_resource(self):
        data = copy.deepcopy(self.data)
        for key in data:
            if key != 'assets': data[key] = []
        (self.props/'props.json').write_text(json.dumps(data))
        out, _, text = self.export()
        self.assertNotIn('OcclusionFade', text)
        self.assertFalse((out/'scripts/occlusion_fade.gd').exists())
        validate_resources(out, include_scenes=True)
        # Preserved manifest and PNG paths can be loaded again.
        self.assertEqual(len(load_props(out/'props')['assets']), 2)

    def test_cli_props_and_requires_parallax(self):
        out = self.root/'cli'
        command = [sys.executable, '-B', '-m', 'export.godot_import', '--cells', str(self.cells),
                   '--out', str(out), '--props', str(self.props)]
        proc = subprocess.run(command, capture_output=True, text=True, timeout=30)
        self.assertNotEqual(proc.returncode, 0);self.assertFalse(out.exists())
        proc = subprocess.run(command+['--parallax', str(self.source)], capture_output=True, text=True, timeout=30)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)['parallax']['props']['instances'], 3)

    @unittest.skipUnless(Path(GODOT).is_file(), 'Godot binary unavailable')
    def test_headless_occlusion_fade_restore_overhead_near_and_particles(self):
        out, _, _ = self.export()
        (out/'probe.gd').write_text(PROBE)
        for args in (['--import'], ['--script', 'res://probe.gd']):
            proc = subprocess.run([GODOT, '--headless', '--path', str(out), *args],
                                  capture_output=True, text=True, timeout=90)
            log = proc.stdout+proc.stderr
            self.assertEqual(proc.returncode, 0, log)
            self.assertNotIn('SCRIPT ERROR', log)
            self.assertNotIn('T3L_ASSERTION:', log)
        self.assertIn('T3L_RUNTIME_ASSERTIONS=complete', log)


PROBE = '''extends SceneTree
func check(value: bool, message: String) -> void:
    if not value:
        printerr("T3L_ASSERTION: ", message)
        quit(7)
func _initialize() -> void:
    call_deferred("probe")
func probe() -> void:
    root.size = Vector2i(1920, 1080)
    var scene: Node = load("res://scenes/cliffside.tscn").instantiate()
    root.add_child(scene)
    await process_frame
    var keeper: Node2D = scene.get_node("Actors/Keeper")
    keeper.set_physics_process(false)
    var tree: Sprite2D = scene.get_node("Actors/Prop_0")
    keeper.position = Vector2(400, 340)
    await create_timer(0.25).timeout
    check(tree.modulate.a <= 0.4, "behind tree fades")
    keeper.position = Vector2(400, 370)
    await create_timer(0.25).timeout
    check(tree.modulate.a >= 0.99, "front restores")
    keeper.position = Vector2(800, 340)
    await create_timer(0.25).timeout
    check(tree.modulate.a >= 0.99, "no horizontal overlap")
    var overhead: Sprite2D = scene.get_node("Overhead/Overhead_0")
    keeper.position = Vector2(400, 350)
    await create_timer(0.25).timeout
    check(overhead.modulate.a <= 0.4, "overhead overlaps without anchor test")
    keeper.position = Vector2(800, 350)
    await create_timer(0.25).timeout
    check(overhead.modulate.a >= 0.99, "overhead restores")
    var near_layer: Parallax2D = scene.get_node("Near_0")
    var near_sprite: Sprite2D = scene.get_node("Near_0/NearSprite_0")
    var camera: Camera2D = keeper.get_node("Camera2D")
    camera.make_current()
    camera.force_update_scroll()
    await process_frame
    # Set sprite local position using actual screen transforms, then restore
    # far away. This verifies near fades use screen coordinates, not feet y.
    near_sprite.position = near_layer.get_global_transform_with_canvas().affine_inverse() * (keeper.get_global_transform_with_canvas().origin - Vector2(100, 150))
    await create_timer(0.25).timeout
    check(near_sprite.modulate.a <= 0.4, "near screen overlap fades")
    near_sprite.position += Vector2(10000, 10000)
    await create_timer(0.25).timeout
    check(near_sprite.modulate.a >= 0.99, "near restores")
    var motes: CPUParticles2D = scene.get_node("Air/Particles_mist_motes")
    check(motes.amount == 37 and is_equal_approx(motes.lifetime, 2.75), "particle parameters")
    check(not motes.local_coords and motes.emitting, "world emission")
    print("T3L_RUNTIME_ASSERTIONS=complete")
    scene.queue_free()
    await process_frame
    quit(0)
'''


def build_fixture(directory):
    started = time.monotonic()
    root = Path(directory);root.mkdir(parents=True, exist_ok=True)
    source, cells, _, _ = make_inputs(root/'fixture_inputs', (1200, 900))
    props = root/'fixture_inputs/props';make_props(props)
    path = source/'parallax.json';data = json.loads(path.read_text());data['movement'] = MOVEMENT
    path.write_text(json.dumps(data))
    out = root/'fixture_project'
    result = build_project(cells, out, parallax=source, props=props)
    (out/'probe.gd').write_text(PROBE)
    half = half_coverage_case(root/'fixture_inputs/half')
    value = near_coverage(*half, step_px=4000)
    text = (out/'scenes/cliffside.tscn').read_text();nodes = scene_nodes(text)
    refs = validate_resources(out, include_scenes=True)
    measured = {'assets': 2, 'prop_sprites': len([n for n in nodes if re.fullmatch('Prop_[0-9]+', n)]),
                'shadows': len([n for n in nodes if re.fullmatch('Shadow_[0-9]+', n)]),
                'overhead': 1, 'near': 1, 'particles': 1,
                'collision_polygons': len([n for n in nodes if n.startswith('PropCollision_')]),
                'near_scroll_scale': vector(nodes['Near_0'], 'scroll_scale'),
                'particle_amount': int(re.search(r'amount = (\d+)', nodes['Particles_mist_motes'])[1]),
                'particle_lifetime_s': float(re.search(r'lifetime = ([0-9.]+)', nodes['Particles_mist_motes'])[1]),
                'known_coverage_share': value, 'known_coverage_samples': 2,
                'resource_references': len(refs), 'missing_resources': 0,
                'walk_speed': result['parallax']['walk_speed'], 'run_speed': result['parallax']['run_speed'],
                'walk_anim_fps': MOVEMENT['walk_anim_fps'], 'run_anim_fps': MOVEMENT['run_anim_fps']}
    metrics = []
    expected = {'assets': 2, 'prop_sprites': 3, 'shadows': 2, 'overhead': 1, 'near': 1, 'particles': 1,
                'collision_polygons': 2, 'particle_amount': 37, 'particle_lifetime_s': 2.75,
                'known_coverage_share': .5, 'missing_resources': 0,
                'walk_speed': 173.25, 'run_speed': 301.5, 'walk_anim_fps': 9.5, 'run_anim_fps': 17.25}
    for name, threshold in expected.items():
        metrics.append({'id': 't3l_'+name, 'subject': 'synthetic_cliffside', 'passed': None,
                        'value': measured[name], 'threshold': threshold, 'op': '==', 'unit': 'share' if name.endswith('share') else 'count_or_px_s',
                        'evidence': ['fixture_project/scenes/cliffside.tscn'], 'notes': 'Instrument only; conductor owns acceptance.'})
    report = {'measured': measured, 'metrics': metrics, 'export': result, 'wall_s': time.monotonic()-started}
    (root/'acceptance.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


# T3m additions are below; the original T3l fixture command remains available.

T3L_PROPS_BASELINE = {
    **BASELINE,
    'parallax/export.json': 'f0287a4091fad7bd3a51d617111bdab89b42b2af1a45bdcdc2ec7d9160d671e2',
    'props/props.json': 'ca8a0a44effd6c925cf99faf696f61286700441d506baba1db3e1d9d765c9265',
    'scenes/cliffside.tscn': '7b40d225aeb834f858c023970942f0d11a77842016b5dad0792ccfe61dd6addf',
    'scripts/occlusion_fade.gd': '6457d041cb822f74c1c26fee1f1b72715e05b30b19b26b85bae230ddb45daeae',
}


class PropsLayerT3mTests(unittest.TestCase):
    setUp = PropsLayerTests.setUp
    export = PropsLayerTests.export
    reject = PropsLayerTests.reject

    def test_offset_ellipse_centre_exact_in_level_pixels(self):
        footprint = self.data['assets'][0]['footprint']
        footprint['offset'] = [13.25, -7.5]
        (self.props/'props.json').write_text(json.dumps(self.data))
        _, _, text = self.export()
        nodes = scene_nodes(text)
        for i in (0, 1):
            node = nodes[f'PropCollision_{i}']
            polygon = scene_polygons(node)[0]
            pos = vector(node, 'position')
            self.assertEqual(pos, self.data['instances'][i]['position'])
            self.assertEqual(len(polygon), 16)
            # Opposite cardinal vertices give the centre without summation noise.
            centre = [(polygon[0][0]+polygon[8][0])/2,
                      (polygon[4][1]+polygon[12][1])/2]
            self.assertEqual(centre, [13.25, -7.5])
            self.assertEqual([pos[k]+centre[k] for k in (0, 1)],
                             [pos[k]+footprint['offset'][k] for k in (0, 1)])
            self.assertEqual(vector(nodes[f'Prop_{i}'], 'offset'), [-49.5, -174])

    def test_rect_four_vertices_and_offset_without_sprite_scaling(self):
        self.data['assets'][0]['footprint'] = {
            'w': 20, 'h': 12, 'shape': 'rect', 'offset': [-4.5, 9.25]}
        (self.props/'props.json').write_text(json.dumps(self.data))
        _, _, text = self.export()
        for i in (0, 1):
            node = scene_nodes(text)[f'PropCollision_{i}']
            self.assertEqual(scene_polygons(node)[0],
                             [[-14.5, 3.25], [5.5, 3.25], [5.5, 15.25], [-14.5, 15.25]])
            self.assertEqual(vector(node, 'position'), self.data['instances'][i]['position'])
        self.assertEqual(ellipse({'w': 20, 'h': 12, 'shape': 'rect'}),
                         [[-10, -6], [10, -6], [10, 6], [-10, 6]])

    def test_optional_defaults_preserve_legacy_vertices_and_scene_text(self):
        baseline = ellipse({'w': 70, 'h': 24})
        expected = [[35*math.cos(i*math.tau/16), 12*math.sin(i*math.tau/16)] for i in range(16)]
        self.assertEqual(baseline, expected)
        for extra in ({'shape': 'ellipse'}, {'offset': [0, 0]},
                      {'shape': 'ellipse', 'offset': [0.0, -0.0]}):
            with self.subTest(extra=extra):
                self.assertEqual(ellipse({'w': 70, 'h': 24, **extra}), baseline)
        # T3l iterates a set when emitting report counts. Freeze its pre-edit
        # iteration order as well as the clock; do not change exporter output.
        class BaselineCollections(set):
            def __iter__(self):
                return iter(('assets', 'near', 'shadows', 'instances', 'particles', 'overhead'))

        with patch('time.monotonic', return_value=0.0), patch(
                'export.props_layer.COLLECTIONS', BaselineCollections(self.data)):
            out, _, before = self.export()
        old_hashes = text_hashes(out)
        self.assertEqual(set(old_hashes), set(T3L_PROPS_BASELINE))
        differences = [p for p in old_hashes if old_hashes[p] != T3L_PROPS_BASELINE[p]]
        # The contract requires a new script. All other old-manifest text is locked.
        self.assertEqual(differences, ['scripts/occlusion_fade.gd'])
        for asset in self.data['assets']:
            asset['footprint'].update(shape='ellipse', offset=[0, 0])
        (self.props/'props.json').write_text(json.dumps(self.data))
        explicit = self.root/'explicit_defaults'
        with patch('time.monotonic', return_value=0.0):
            build_project(self.cells, explicit, parallax=self.source, props=self.props)
        self.assertEqual((explicit/'scenes/cliffside.tscn').read_text(), before)

    def test_invalid_shapes_offsets_and_unknown_keys_before_output(self):
        cases = [({'shape': s}) for s in ('circle', 'RECT', '', None, True, 2, [], {})]
        cases += [{'offset': v} for v in
                  ([float('nan'), 0], [0, float('inf')], [float('-inf'), 0],
                   [True, 0], [0, False], [0], [0, 0, 0], '0,0', None, {}, ['1', 0])]
        cases += [{'surprise': 0}]
        for extra in cases:
            data = copy.deepcopy(self.data)
            data['assets'][0]['footprint'].update(extra)
            with self.subTest(extra=extra):
                self.reject(data)
        for footprint in (None, [], {'h': 12, 'offset': [0, 0]}, {'w': 12, 'shape': 'rect'}):
            data = copy.deepcopy(self.data)
            data['assets'][0]['footprint'] = footprint
            with self.subTest(footprint=footprint):
                self.reject(data)

    def test_generated_pixel_mask_contract_and_legacy_near_branch(self):
        out, _, _ = self.export()
        script = (out/'scripts/occlusion_fade.gd').read_text()
        self.assertEqual(script, OCCLUSION_SCRIPT)
        for token in ('func _ready()', 'create_from_image_alpha(source.get_image(), 0.5)',
                      'frames.get_frame_texture(sprite.animation, sprite.frame)',
                      'frame_masks.has(current)', 'frame_masks[current] = _alpha_mask(current)',
                      'sprite.offset', 'sprite.centered', 'sprite.flip_h', 'sprite.flip_v',
                      'sprite.get_global_transform_with_canvas()', 'affine_inverse()',
                      'x += 2.0', 'y += 2.0', 'mask.get_bitv(pixel)',
                      'if wanted != target_alpha:', '0.15 if fade_mode == 2 else 0.06'):
            self.assertIn(token, script)
        pixel_branch = script.split('func _pixel_overlap()')[1].split('func _process')[0]
        self.assertNotIn('body_width', pixel_branch)
        self.assertNotIn('opaque_rect', pixel_branch)
        self.assertIn('keeper.global_position.y < global_position.y and _pixel_overlap()', script)

    def test_fixture_hollow_square_asymmetry_and_generated_resources(self):
        out = build_t3m_fixture(self.root/'fixture')
        self.assertEqual((out/'scripts/occlusion_fade.gd').read_text(), OCCLUSION_SCRIPT)
        self.assertTrue(validate_resources(out, include_scenes=True))
        with Image.open(out/'props/ring.png') as image:
            alpha = image.getchannel('A')
            self.assertEqual(image.size, (64, 64))
            self.assertEqual(alpha.getpixel((32, 32)), 0)
            self.assertEqual(alpha.getpixel((4, 32)), 255)
        with Image.open(out/'sprites/square.png') as image:
            self.assertEqual(image.size, (6, 6))
            self.assertEqual(image.getchannel('A').getextrema(), (255, 255))
        with Image.open(out/'sprites/asymmetric.png') as image:
            self.assertEqual(image.getchannel('A').getbbox(), (0, 0, 6, 6))
        nodes = scene_nodes((out/'scenes/cliffside.tscn').read_text())
        self.assertEqual(scene_polygons(nodes['PropCollision_1'])[0],
                         [[-6.5, -8.25], [13.5, -8.25], [13.5, 3.75], [-6.5, 3.75]])

    @unittest.skipUnless(Path(GODOT).is_file(), 'Godot binary unavailable')
    def test_headless_ring_hollow_fade_timing_front_flip_current_frame_and_transforms(self):
        out = build_t3m_fixture(self.root/'fixture')
        logs = []
        for args in (['--import'], ['--script', 'res://probe.gd']):
            # Keep the engine logger inside this test's TemporaryDirectory.
            # The macOS default user logger can crash before project settings load.
            proc = subprocess.run([GODOT, '--headless', '--path', str(out),
                                   '--log-file', str(self.root/'godot.log'), *args],
                                  capture_output=True, text=True, timeout=45)
            log = proc.stdout+proc.stderr
            logs.append(log)
            self.assertEqual(proc.returncode, 0, log)
            self.assertNotIn('SCRIPT ERROR', log)
            self.assertNotIn('T3M_ASSERTION:', log)
        self.assertIn('T3M_RUNTIME_ASSERTIONS=complete', logs[-1])
        rows = [json.loads(line.split('=', 1)[1]) for line in logs[-1].splitlines()
                if line.startswith('T3M_MEASURE=')]
        self.assertGreaterEqual(len(rows), 20)


T3M_PROBE = '''extends SceneTree
var errors: int = 0

func check(value: bool, message: String) -> void:
    if not value:
        errors += 1
        printerr("T3M_ASSERTION: ", message)

func record(label: String, value: float, threshold: float, op: String, unit: String = "alpha") -> void:
    print("T3M_MEASURE=", JSON.stringify({"id": "t3m_" + label, "subject": "synthetic_ring",
        "passed": null, "value": value, "threshold": threshold, "op": op, "unit": unit,
        "evidence": ["fixture_project/probe.gd"], "notes": "Engine measurement; conductor owns acceptance."}))
    check(value <= threshold if op == "<=" else value >= threshold, label)

func settle(prop: Sprite2D, label: String, fading: bool) -> void:
    # Apply the trigger at t=0 and measure completion, with a 0.1-second deadline.
    # A stalled engine is reported as late, never relabelled a 0.1-second sample.
    var started: int = Time.get_ticks_usec()
    prop._process(0.0)
    while not is_equal_approx(prop.modulate.a, prop.target_alpha) and Time.get_ticks_usec()-started < 100000:
        await process_frame
    record(label, prop.modulate.a, 0.4 if fading else 0.95, "<=" if fading else ">=")
    record(label + "_wall_s", float(Time.get_ticks_usec()-started)/1000000.0, 0.1, "<=", "s")

func _initialize() -> void:
    call_deferred("probe")

func probe() -> void:
    root.size = Vector2i(320, 240)
    var scene: Node2D = load("res://scenes/cliffside.tscn").instantiate()
    root.add_child(scene)
    await process_frame
    var keeper: Node2D = scene.get_node("Actors/Keeper")
    var sprite: AnimatedSprite2D = keeper.get_node("AnimatedSprite2D")
    var prop: Sprite2D = scene.get_node("Actors/Prop_0")
    sprite.pause()
    keeper.position = Vector2(128, 131)
    await settle(prop, "hollow_initial", false)
    check(is_equal_approx(prop.modulate.a, 1.0), "hollow stays exactly 1")
    check(prop.prop_mask.get_size() == Vector2i(64, 64), "ready creates prop bitmap")
    keeper.position = Vector2(102, 131)
    await settle(prop, "ring_behind", true)
    var tween: Tween = prop.fade_tween
    prop._process(0.0)
    check(prop.fade_tween == tween, "same target does not retrigger tween")
    keeper.position = Vector2(128, 131)
    await settle(prop, "hollow_restored", false)
    keeper.position = Vector2(128, 163)
    check(prop._pixel_overlap(), "front case really overlaps opaque bottom ring")
    await settle(prop, "ring_front", false)
    check(is_equal_approx(prop.modulate.a, 1.0), "front stays exactly 1")
    keeper.position = Vector2(128, 160)
    await settle(prop, "anchor_equal", false)

    # Same pixel rule for overhead, but without the behind predicate.
    prop.fade_mode = 1
    keeper.position = Vector2(128, 163)
    await settle(prop, "overhead_front", true)
    keeper.position = Vector2(128, 131)
    await settle(prop, "overhead_hollow", false)
    prop.fade_mode = 0
    keeper.position = Vector2(102, 131)
    sprite.frame = 1
    await settle(prop, "current_transparent_frame", false)
    check(prop.frame_masks.size() == 2, "one cache entry per distinct frame texture")
    sprite.frame = 0
    await settle(prop, "current_square_frame", true)
    check(prop.frame_masks.size() == 2, "revisit reuses frame bitmap")

    # A 32x6 texture with only its leftmost 6x6 opaque; offset is nonzero.
    sprite.frame = 2
    sprite.offset = Vector2(-8, -6)
    keeper.position = Vector2(132, 131)
    sprite.flip_h = false
    await settle(prop, "asymmetric_unflipped_hollow", false)
    sprite.flip_h = true
    await settle(prop, "asymmetric_flipped_ring", true)
    sprite.flip_h = false
    await settle(prop, "asymmetric_unflipped_restored", false)

    # Alpha threshold straddles 0.5 and must not depend on current modulate.a.
    sprite.offset = Vector2(-3, -6)
    keeper.position = Vector2(102, 131)
    sprite.frame = 3
    await settle(prop, "alpha_127_transparent", false)
    sprite.frame = 4
    await settle(prop, "alpha_128_opaque", true)
    check(prop.frame_masks.size() == 5, "five distinct textures cached")

    # Independent sprite offset/centering/scale and shared rotated canvas transform.
    sprite.frame = 0
    sprite.centered = true
    sprite.offset = Vector2(0, -3)
    sprite.scale = Vector2(1.5, 0.75)
    scene.scale = Vector2(1.5, 0.75)
    scene.rotation = 0.13
    scene.position = Vector2(17, 9)
    keeper.position = Vector2(128, 131)
    await settle(prop, "transformed_hollow", false)
    keeper.position = Vector2(102, 131)
    await settle(prop, "transformed_ring", true)
    sprite.scale.x = -1.5
    await settle(prop, "negative_scale_ring", true)
    sprite.scale = Vector2.ZERO
    await settle(prop, "zero_scale_empty", false)

    # Interrupt an in-progress fade; reverse tween must start from current alpha.
    sprite.scale = Vector2.ONE
    scene.transform = Transform2D.IDENTITY
    keeper.position = Vector2(102, 131)
    prop._process(0.0)
    await create_timer(0.02).timeout
    var interrupted: Tween = prop.fade_tween
    keeper.position = Vector2(128, 131)
    prop._process(0.0)
    check(prop.fade_tween != interrupted, "changed target replaces tween")
    check(not interrupted.is_valid(), "previous tween killed")
    await settle(prop, "interrupted_restore", false)

    if errors == 0:
        print("T3M_RUNTIME_ASSERTIONS=complete")
    scene.queue_free()
    await process_frame
    quit(0 if errors == 0 else 7)
'''


def build_t3m_fixture(directory):
    """Small, persistent ring/6x6 fixture using the actual exported fade script.

    Run Godot --headless --path DIR/fixture_project --import, then the same
    command with --script res://probe.gd. All art is synthetic test geometry.
    """
    from export.godot_import import write_spriteframes
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)
    source = root/'fixture_inputs'
    source.mkdir()
    ring = Image.new('RGBA', (64, 64))
    for y in range(64):
        for x in range(64):
            if 20**2 <= (x-31.5)**2+(y-31.5)**2 <= 31.5**2:
                ring.putpixel((x, y), (40, 90, 130, 255))
    ring.save(source/'ring.png')
    data = {key: [] for key in ('assets', 'instances', 'shadows', 'overhead', 'near', 'particles')}
    for name, footprint, position in (
            ('ring', {'w': 20, 'h': 12, 'offset': [3.5, -2.25]}, [128, 160]),
            ('rect', {'w': 20, 'h': 12, 'offset': [3.5, -2.25], 'shape': 'rect'}, [256, 160])):
        data['assets'].append({'name': name, 'file': 'ring.png', 'anchor': [32, 64],
                               'footprint': footprint, 'collide': True, 'fade_when_behind': True})
        data['instances'].append({'asset': name, 'position': position})
    (source/'props.json').write_text(json.dumps(data, indent=2)+'\n')
    out = root/'fixture_project'
    for folder in ('scripts', 'scenes', 'sprites', 'frames'):
        (out/folder).mkdir(parents=True)
    fragments = write_layers(out, load_props(source))
    for name, alpha in (('square', 255), ('transparent', 0), ('alpha127', 127), ('alpha128', 128)):
        Image.new('RGBA', (6, 6), (60, 130, 190, alpha)).save(out/'sprites'/f'{name}.png')
    asymmetric = Image.new('RGBA', (32, 6))
    ImageDraw.Draw(asymmetric).rectangle((0, 0, 5, 5), fill=(60, 130, 190, 255))
    asymmetric.save(out/'sprites/asymmetric.png')
    paths = ['sprites/'+n+'.png' for n in ('square', 'transparent', 'asymmetric', 'alpha127', 'alpha128')]
    write_spriteframes(out, 'frames/keeper.tres', {'idle_S': (paths, 8, True)})
    external = fragments['external']+[
        '[ext_resource type="SpriteFrames" path="res://frames/keeper.tres" id="Frames"]']
    scene = ('[gd_scene load_steps='+str(len(external)+1)+' format=3]\n\n'+
             '\n'.join(external)+'\n\n[node name="Cliffside" type="Node2D"]\n'+
             '\n[node name="Walls" type="StaticBody2D" parent="."]\n'+fragments['collisions']+
             fragments['before_keeper']+
             '\n[node name="Keeper" type="Node2D" parent="Actors"]\nposition = Vector2(128, 131)\n'+
             '\n[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="Actors/Keeper"]\n'+
             'sprite_frames = ExtResource("Frames")\nanimation = &"idle_S"\ncentered = false\noffset = Vector2(-3, -6)\n'+
             fragments['after_keeper'])
    (out/'scenes/cliffside.tscn').write_text(scene)
    (out/'project.godot').write_text('config_version=5\n\n[application]\nconfig/name="T3m ring probe"\n'
                                   'run/main_scene="res://scenes/cliffside.tscn"\n\n[debug]\n'
                                   'file_logging/enable_file_logging=false\n\n[display]\n'
                                   'window/size/viewport_width=320\nwindow/size/viewport_height=240\n\n'
                                   '[rendering]\nrenderer/rendering_method="gl_compatibility"\n')
    (out/'probe.gd').write_text(T3M_PROBE)
    return out



# T3p: captured from the T3o exporter before adding near.fade. Clock and
# collection iteration order are fixed exactly as in the T3m regression lock.
T3O_PROPS_BASELINE = {
    **T3L_PROPS_BASELINE,
    'scripts/occlusion_fade.gd': '96d37de2e8c7790cb00815fb1f939389872874ba23b43dc017d8530d3db62f61',
}


class PropsLayerT3pTests(unittest.TestCase):
    setUp = PropsLayerTests.setUp
    export = PropsLayerTests.export
    reject = PropsLayerTests.reject

    def mixed(self):
        self.data['near'].append(copy.deepcopy(self.data['near'][0]))
        self.data['near'][0]['fade'] = False
        (self.props/'props.json').write_text(json.dumps(self.data))

    def test_mixed_near_only_default_sprite_has_fade_script(self):
        self.mixed()
        out, report, text = self.export()
        nodes = scene_nodes(text)
        self.assertEqual(report['parallax']['props']['near'], 2)
        for key in ('script =', 'keeper_path =', 'body_width =', 'fade_mode =',
                    'opaque_rect =', 'modulate ='):
            self.assertNotIn(key, nodes['NearSprite_0'])
        self.assertIn('script = ExtResource("OcclusionFade")', nodes['NearSprite_1'])
        self.assertIn('fade_mode = 2', nodes['NearSprite_1'])
        for i in (0, 1):
            self.assertEqual(vector(nodes[f'Near_{i}'], 'scroll_scale'), [1.2, 1.2])
            self.assertEqual(vector(nodes[f'Near_{i}'], 'scroll_offset'), [0, 0])
            self.assertIn('z_index = 4', nodes[f'Near_{i}'])
        self.assertEqual((out/'props/props.json').read_bytes(), (self.props/'props.json').read_bytes())
        self.assertEqual((out/'props/near.png').read_bytes(), (self.props/'near.png').read_bytes())
        self.assertTrue(validate_resources(out, include_scenes=True))

    def test_all_opaque_near_omits_unneeded_fade_resource(self):
        self.mixed()
        for key in self.data:
            if key != 'near':
                self.data[key] = []
        for entry in self.data['near']:
            entry['fade'] = False
        (self.props/'props.json').write_text(json.dumps(self.data))
        out, _, text = self.export()
        self.assertNotIn('OcclusionFade', text)
        self.assertFalse((out/'scripts/occlusion_fade.gd').exists())
        self.assertTrue(validate_resources(out, include_scenes=True))

    def test_opaque_near_keeps_other_layers_fade_resources(self):
        self.data['near'][0]['fade'] = False
        (self.props/'props.json').write_text(json.dumps(self.data))
        out, _, text = self.export()
        nodes = scene_nodes(text)
        for name, mode in (('Prop_0', 0), ('Prop_1', 0), ('Overhead_0', 1)):
            self.assertIn('script = ExtResource("OcclusionFade")', nodes[name])
            self.assertIn(f'fade_mode = {mode}', nodes[name])
        self.assertNotIn('script =', nodes['NearSprite_0'])
        self.assertTrue(validate_resources(out, include_scenes=True))

    def test_non_boolean_fade_rejected_before_any_output(self):
        for value in (None, 0, 1, -1, 0.0, 1.0, 'false', 'true', '', [], {}, [False]):
            bad = copy.deepcopy(self.data)
            bad['near'][0]['fade'] = value
            with self.subTest(fade=value):
                self.reject(bad)

    def test_unknown_keys_and_fade_on_other_collections_rejected(self):
        for key in ('Fade', 'fade_when_behind', 'opacity', 'unexpected'):
            bad = copy.deepcopy(self.data)
            bad['near'][0].update(fade=False)
            bad['near'][0][key] = False
            with self.subTest(key=key):
                self.reject(bad)
        for collection in ('assets', 'instances', 'shadows', 'overhead', 'particles'):
            bad = copy.deepcopy(self.data)
            bad[collection][0]['fade'] = False
            with self.subTest(collection=collection):
                self.reject(bad)

    def test_explicit_true_equals_default_export_text_except_copied_manifest(self):
        with patch('time.monotonic', return_value=0.0):
            before, _, _ = self.export()
        self.data['near'][0]['fade'] = True
        (self.props/'props.json').write_text(json.dumps(self.data))
        after = self.root/'explicit_true'
        with patch('time.monotonic', return_value=0.0):
            build_project(self.cells, after, parallax=self.source, props=self.props)
        a, b = text_hashes(before), text_hashes(after)
        self.assertEqual(set(a), set(b))
        self.assertEqual([p for p in a if a[p] != b[p]], ['props/props.json'])

    def test_no_fade_key_byte_identical_to_t3o_all_text(self):
        class OrderedCollections(set):
            def __iter__(self):
                return iter(('assets', 'near', 'shadows', 'instances', 'particles', 'overhead'))
        with patch('time.monotonic', return_value=0.0), patch(
                'export.props_layer.COLLECTIONS', OrderedCollections(self.data)):
            out, _, _ = self.export()
        self.assertEqual(text_hashes(out), T3O_PROPS_BASELINE)

    def test_coverage_unchanged_for_false_true_and_mixed_entries(self):
        props, walkable, camera = half_coverage_case(self.root/'half')
        self.assertEqual(near_coverage(props, walkable, camera, 4000), .5)
        for flags in ((False,), (True,), (False, None), (False, True)):
            data = {k: copy.deepcopy(props[k]) for k in self.data}
            template = data['near'][0]
            data['near'] = [dict(template, **({} if flag is None else {'fade': flag}))
                            for flag in flags]
            (props['root']/'props.json').write_text(json.dumps(data))
            with self.subTest(flags=flags):
                self.assertEqual(near_coverage(props['root'], walkable, camera, 4000), .5)

    @unittest.skipUnless(Path(GODOT).is_file(), 'Godot binary unavailable')
    def test_headless_mixed_near_overlap_alpha_and_restore(self):
        self.mixed()
        out, _, _ = self.export()
        (out/'probe.gd').write_text(T3P_PROBE)
        logs = []
        for args in (['--import'], ['--script', 'res://probe.gd']):
            proc = subprocess.run([GODOT, '--headless', '--path', str(out),
                                   '--log-file', str(self.root/'godot.log'), *args],
                                  capture_output=True, text=True, timeout=45)
            log = proc.stdout+proc.stderr
            logs.append(log)
            self.assertEqual(proc.returncode, 0, log)
            self.assertNotIn('SCRIPT ERROR', log)
            self.assertNotIn('T3P_ASSERTION:', log)
        self.assertIn('T3P_RUNTIME_ASSERTIONS=complete', logs[-1])
        rows = [json.loads(line.split('=', 1)[1]) for line in logs[-1].splitlines()
                if line.startswith('T3P_MEASURE=')]
        values = {r['id']: r['value'] for r in rows}
        for cycle in range(2):
            self.assertEqual(values[f't3p_opaque_overlap_{cycle}'], 1.0)
            self.assertLessEqual(values[f't3p_default_overlap_{cycle}'], .4)
            self.assertEqual(values[f't3p_opaque_restored_{cycle}'], 1.0)
            self.assertGreaterEqual(values[f't3p_default_restored_{cycle}'], .99)


T3P_PROBE = '''extends SceneTree
var errors: int = 0

func check(value: bool, message: String) -> void:
    if not value:
        errors += 1
        printerr("T3P_ASSERTION: ", message)

func record(label: String, value: float, threshold: float, op: String) -> void:
    print("T3P_MEASURE=", JSON.stringify({"id": "t3p_" + label, "subject": "synthetic_near",
        "passed": null, "value": value, "threshold": threshold, "op": op, "unit": "alpha",
        "evidence": ["fixture_project/probe.gd"], "notes": "Engine measurement; conductor owns acceptance."}))
    if op == "==":
        check(value == threshold, label)
    elif op == "<=":
        check(value <= threshold, label)
    else:
        check(value >= threshold, label)

func _initialize() -> void:
    call_deferred("probe")

func probe() -> void:
    root.size = Vector2i(1920, 1080)
    var scene: Node = load("res://scenes/cliffside.tscn").instantiate()
    root.add_child(scene)
    await process_frame
    var keeper: Node2D = scene.get_node("Actors/Keeper")
    keeper.set_physics_process(false)
    var opaque: Sprite2D = scene.get_node("Near_0/NearSprite_0")
    var fading: Sprite2D = scene.get_node("Near_1/NearSprite_1")
    check(opaque.get_script() == null, "opaque sprite has no script")
    check(fading.get_script() != null, "default sprite has fade script")
    var camera: Camera2D = keeper.get_node("Camera2D")
    camera.make_current()
    camera.force_update_scroll()
    await process_frame
    record("opaque_initial", opaque.modulate.a, 1.0, "==")
    for cycle in range(2):
        for prop in [opaque, fading]:
            prop.position = prop.get_parent().get_global_transform_with_canvas().affine_inverse() * (keeper.get_global_transform_with_canvas().origin - Vector2(100, 150))
        await create_timer(0.25).timeout
        var body: Rect2 = keeper.get_global_transform_with_canvas() * Rect2(-10, -130, 20, 130)
        for prop in [opaque, fading]:
            var displayed: Rect2 = prop.get_global_transform_with_canvas() * prop.get_rect()
            check(displayed.intersects(body), "both near sprites really overlap Keeper")
        record("opaque_overlap_" + str(cycle), opaque.modulate.a, 1.0, "==")
        record("default_overlap_" + str(cycle), fading.modulate.a, 0.4, "<=")
        for prop in [opaque, fading]:
            prop.position += Vector2(10000, 10000)
        await create_timer(0.25).timeout
        record("opaque_restored_" + str(cycle), opaque.modulate.a, 1.0, "==")
        record("default_restored_" + str(cycle), fading.modulate.a, 0.99, ">=")
    if errors == 0:
        print("T3P_RUNTIME_ASSERTIONS=complete")
    scene.queue_free()
    await process_frame
    quit(0 if errors == 0 else 7)
'''


def build_t3p_fixture(directory):
    """Export two synthetic near entries: fade:false and the legacy default."""
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)
    source, cells, _, _ = make_inputs(root/'fixture_inputs', (1200, 900))
    props = root/'fixture_inputs/props'
    data = make_props(props)
    data['near'].append(copy.deepcopy(data['near'][0]))
    data['near'][0]['fade'] = False
    (props/'props.json').write_text(json.dumps(data, indent=2)+'\n')
    out = root/'fixture_project'
    build_project(cells, out, parallax=source, props=props)
    (out/'probe.gd').write_text(T3P_PROBE)
    return out


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--fixture-t3p':
        print(build_t3p_fixture(sys.argv[2]))
    elif len(sys.argv) == 3 and sys.argv[1] == '--fixture-t3m':
        print(build_t3m_fixture(sys.argv[2]))
    elif len(sys.argv) == 3 and sys.argv[1] == '--fixture':
        print(json.dumps(build_fixture(sys.argv[2]), indent=2))
    else:
        unittest.main()
