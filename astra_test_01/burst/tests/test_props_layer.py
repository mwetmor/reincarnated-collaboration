"""T3l layered cliffside contracts and malformed inputs.

PYTHONPATH=.:tests python3 -B tests/test_props_layer.py --fixture runs/C-3/t3/T3l
"""
import copy
import hashlib
import json
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
from export.props_layer import load_props, near_coverage, _camera_top_left
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
        a = copy.deepcopy(self.data);a['assets'][0]['footprint']['shape'] = 'ellipse';self.reject(a)
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


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--fixture':
        print(json.dumps(build_fixture(sys.argv[2]), indent=2))
    else:
        unittest.main()
