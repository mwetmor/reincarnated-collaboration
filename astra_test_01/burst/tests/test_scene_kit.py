"""T3h scene kit: exact geometry, plate cutouts, room wiring and bad inputs."""
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
from PIL import Image

from export.godot_import import build_project, validate_resources
from export.scene_kit import (collision, cut_occluders, load_annotation, shadow_texture,
                              largest_walkable_rectangle, _walkable_grid, _maximal_rectangle)

TMP = Path(__file__).resolve().parent/'tmp'
GODOT = '/Applications/Godot.app/Contents/MacOS/Godot'


def annotation():
    return {'plate_size': [400, 300],
            'walkable': [[[20, 20], [380, 20], [380, 280], [20, 280]]],
            'blocked': [[[250, 100], [300, 100], [300, 150], [250, 150]]],
            'occluders': [{'id': 'pillar', 'polygon': [[250, 60], [300, 60], [300, 150], [250, 150]],
                           'baseline_y': 150}],
            'exits': [{'id': 'south', 'segment': [[160, 280], [220, 280]]}],
            'spawn': [120, 200], 'figure_height_px': 120}


def synthetic_scene(root, data=None):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    data = annotation() if data is None else data
    w, h = data['plate_size']
    yy, xx = np.mgrid[:h, :w]
    rgba = np.stack([xx % 256, yy % 256, (xx+yy) % 256, np.full_like(xx, 255)], axis=2).astype(np.uint8)
    Image.fromarray(rgba).save(root/'plate.png')
    (root/'annotation.json').write_text(json.dumps(data, indent=2)+'\n')
    return rgba


def contains(point, poly):
    """Independent winding-number test, including the polygon boundary."""
    winding = 0
    x, y = point
    for a, b in zip(poly, poly[1:]+poly[:1]):
        cross = (b[0]-a[0])*(y-a[1])-(x-a[0])*(b[1]-a[1])
        if abs(cross) < 1e-8 and min(a[0], b[0])-1e-8 <= x <= max(a[0], b[0])+1e-8 and min(a[1], b[1])-1e-8 <= y <= max(a[1], b[1])+1e-8:
            return True
        if a[1] <= y < b[1] and cross > 0:
            winding += 1
        elif b[1] <= y < a[1] and cross < 0:
            winding -= 1
    return winding != 0


def area(poly):
    return abs(sum(a[0]*b[1]-b[0]*a[1] for a, b in zip(poly, poly[1:]+poly[:1])))/2


class SceneKitTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='t3h-', dir=TMP)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.scene = self.root/'scene'
        self.rgba = synthetic_scene(self.scene)
        self.data = annotation()
        self.cells = self.root/'cells'
        self.cells.mkdir()
        for name in ('idle_S', 'walk_E'):
            Image.new('RGBA', (512, 512), (20, 50, 90, 255)).save(self.cells/(name+'_00.png'))

    def test_load_valid_roundtrip(self):
        self.assertEqual(load_annotation(self.scene/'annotation.json'), self.data)

    def test_schema_known_bad_types_bounds_ids_and_spawn(self):
        bad = []
        for key in self.data:
            value = copy.deepcopy(self.data)
            del value[key]
            bad.append(value)
        for key, values in {
            'plate_size': [[0, 300], [400.5, 300], [True, 300], [400], '400,300'],
            'walkable': [[], None], 'blocked': [None], 'occluders': [{}], 'exits': [{}],
            'spawn': [[-1, 20], [401, 200], [float('nan'), 20], [270, 120], [10, 10], [True, 20]],
            'figure_height_px': [0, -1, True, '120', float('inf')]
        }.items():
            for item in values:
                value = copy.deepcopy(self.data)
                value[key] = item
                bad.append(value)
        value = copy.deepcopy(self.data); value['extra'] = 1; bad.append(value)
        for ident in ('../escape', 'a/b', '', 'x.png', '"quoted'):
            value = copy.deepcopy(self.data);value['occluders'][0]['id'] = ident;bad.append(value)
        value = copy.deepcopy(self.data);value['occluders'] *= 2;bad.append(value)
        value = copy.deepcopy(self.data);value['exits'] *= 2;bad.append(value)
        for baseline in (float('nan'), 301, True):
            value = copy.deepcopy(self.data);value['occluders'][0]['baseline_y'] = baseline;bad.append(value)
        for segment in ([[1, 1]], [[1, 1], [1, 1]], [[1, 1], [500, 1]]):
            value = copy.deepcopy(self.data);value['exits'][0]['segment'] = segment;bad.append(value)
        for i, data in enumerate(bad):
            with self.subTest(case=i):
                (self.scene/'annotation.json').write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    load_annotation(self.scene/'annotation.json')
        (self.scene/'annotation.json').write_text('{bad')
        with self.assertRaises(ValueError):
            load_annotation(self.scene/'annotation.json')

    def test_degenerate_crossed_repeated_and_outside_polygons_rejected(self):
        for poly in ([[[1, 1], [2, 2]]], [[[1, 1], [2, 2], [3, 3]]],
                     [[[10, 10], [100, 100], [10, 100], [80, 10]]],
                     [[[10, 10], [100, 10], [10, 10], [10, 100]]],
                     [[[10, 10], [450, 10], [10, 100]]],
                     [[[10, 10], [100, 10], [80, 10], [80, 100], [10, 100]]]):
            with self.subTest(poly=poly):
                value = copy.deepcopy(self.data);value['blocked'] = poly
                with self.assertRaises(ValueError):
                    collision(value)

    def test_rectangle_cut_bytes_crop_and_one_pixel_feather(self):
        records = cut_occluders(self.scene/'plate.png', self.data, self.root/'cuts')
        self.assertEqual(records, [{'file': 'pillar.png', 'position': [250, 60], 'baseline_y': 150}])
        self.assertEqual(json.loads((self.root/'cuts/occluders.json').read_text()), records)
        with Image.open(self.root/'cuts/pillar.png') as im:
            cut = np.array(im)
            self.assertEqual(im.size, (50, 90))
        np.testing.assert_array_equal(cut[1:-1, 1:-1], self.rgba[61:149, 251:299])
        np.testing.assert_array_equal(cut[:, :, :3], self.rgba[60:150, 250:300, :3])
        self.assertTrue(np.all(cut[0, :, 3] == 128))
        self.assertTrue(np.all(cut[1:-1, 1:-1, 3] == 255))
        canvas = np.zeros((300, 400, 4), dtype=np.uint8)
        canvas[60:150, 250:300] = cut
        self.assertEqual(int(canvas[:60, :, 3].max()), 0)
        self.assertEqual(int(canvas[150:, :, 3].max()), 0)

    def test_triangle_outside_transparent_and_source_alpha_preserved(self):
        self.data['occluders'][0]['polygon'] = [[10.25, 10.25], [70.25, 10.25], [10.25, 70.25]]
        source = self.rgba.copy();source[:, :, 3] = 180
        Image.fromarray(source).save(self.scene/'plate.png')
        records = cut_occluders(self.scene/'plate.png', self.data, self.root/'cuts')
        self.assertEqual(records[0]['position'], [10, 10])
        with Image.open(self.root/'cuts/pillar.png') as im:
            a = np.array(im)
        self.assertEqual(a.shape[:2], (61, 61))
        self.assertEqual(int(a[50, 50, 3]), 0)
        self.assertEqual(int(a[5, 5, 3]), 180)
        np.testing.assert_array_equal(a[5, 5, :3], source[15, 15, :3])
        self.assertGreater(int(a[0, 0, 3]), 0)
        self.assertLess(int(a[0, 0, 3]), 180)

    def test_cut_plate_mismatch_and_empty_occluders(self):
        Image.new('RGB', (399, 300)).save(self.scene/'plate.png')
        with self.assertRaises(ValueError):
            cut_occluders(self.scene/'plate.png', self.data, self.root/'bad')
        synthetic_scene(self.scene)
        self.data['occluders'] = []
        self.assertEqual(cut_occluders(self.scene/'plate.png', self.data, self.root/'cuts'), [])
        self.assertEqual(json.loads((self.root/'cuts/occluders.json').read_text()), [])

    def test_collision_blocked_floor_and_complement_area(self):
        result = collision(self.data)
        self.assertEqual(result[0], self.data['blocked'][0])
        self.assertTrue(any(contains((275, 125), p) for p in result))
        self.assertFalse(any(contains((120, 200), p) for p in result))
        self.assertTrue(any(contains((10, 200), p) for p in result))
        self.assertAlmostEqual(sum(area(p) for p in result[1:]), 400*300-360*260)
        self.assertEqual(self.data, annotation())

    def _compare_union(self, walkable, spawn):
        self.data.update(walkable=walkable, blocked=[], spawn=spawn)
        result = collision(self.data)
        # Offset the independent sample lattice away from vertices and slab seams.
        for y in np.arange(0.37, 300, 6.97):
            for x in np.arange(0.23, 400, 7.13):
                expected = not any(contains((x, y), p) for p in walkable)
                self.assertEqual(any(contains((x, y), p) for p in result), expected, (x, y))
        for poly in result:
            self.assertGreater(area(poly), 0)
            self.assertLessEqual(len(poly), 4)
        return result

    def test_overlapping_diagonal_walkable_union_edge_crossings(self):
        self._compare_union([[[20, 20], [300, 40], [200, 270]],
                             [[90, 240], [140, 10], [380, 230]]], [160, 140])

    def test_concave_floor_and_disconnected_island(self):
        self._compare_union([[[20, 20], [180, 20], [180, 100], [90, 100], [90, 280], [20, 280]],
                             [[250, 140], [360, 140], [360, 260], [250, 260]]], [50, 50])

    def test_walkable_union_hole_and_shared_edges(self):
        walkable = [[[20, 20], [380, 20], [380, 70], [20, 70]],
                    [[20, 230], [380, 230], [380, 280], [20, 280]],
                    [[20, 70], [80, 70], [80, 230], [20, 230]],
                    [[320, 70], [380, 70], [380, 230], [320, 230]]]
        result = self._compare_union(walkable, [40, 40])
        self.assertTrue(any(contains([200, 150], p) for p in result))
        self.assertAlmostEqual(sum(area(p) for p in result), 400*300-(360*260-240*160))

    def test_full_plate_floor_and_winding_reversal(self):
        self.data.update(walkable=[[[0, 0], [400, 0], [400, 300], [0, 300]]], blocked=[])
        self.assertEqual(collision(self.data), [])
        self.data['walkable'][0].reverse()
        self.assertEqual(collision(self.data), [])

    def test_shadow_peak_rim_radial_and_bad_dimensions(self):
        for w, h in ((64, 20), (65, 21)):
            with self.subTest(size=(w, h)):
                path = shadow_texture(self.root/'shadow.png', w, h)
                with Image.open(path) as im:
                    a = np.array(im)
                self.assertEqual(a.shape, (h, w, 4))
                self.assertEqual(int(a[h//2, w//2, 3]), 115)
                self.assertEqual(int(a[:, :, 3].max()), 115)
                self.assertEqual(int(a[0, :, 3].max()), 0)
                self.assertEqual(int(a[-1, :, 3].max()), 0)
                self.assertEqual(int(a[:, 0, 3].max()), 0)
                self.assertEqual(int(a[:, -1, 3].max()), 0)
                np.testing.assert_array_equal(a, a[::-1])
                np.testing.assert_array_equal(a, a[:, ::-1])
                self.assertTrue(np.all(np.diff(a[h//2, :w//2, 3].astype(int)) >= 0))
        for w, h in ((0, 20), (64, -1), (True, 20), (64.5, 20), (2, 20)):
            with self.assertRaises(ValueError):
                shadow_texture(self.root/'bad.png', w, h)

    def test_tower_resources_hierarchy_pivot_speeds_collision_and_camera(self):
        out = self.root/'project'
        report = build_project(self.cells, out, scene=self.scene)
        self.assertEqual(report['cells'], ['idle_S', 'walk_E'])
        self.assertEqual(report['scene']['scale'], 0.5)
        self.assertEqual(report['scene']['feet_width_px'], 26.4)
        self.assertEqual(report['scene']['camera_zoom'], 3.84)
        self.assertTrue((out/'scenes/main.tscn').is_file())
        tower = (out/'scenes/tower.tscn').read_text()
        for fragment in ('name="Plate" type="Sprite2D" parent="."', 'z_index = -10',
                         'name="World" type="Node2D" parent="."', 'y_sort_enabled = true',
                         'name="Keeper" type="CharacterBody2D" parent="World"',
                         'position = Vector2(120, 200)', 'offset = Vector2(-256, -400)',
                         'scale = Vector2(0.5, 0.5)', 'walk_speed = 75', 'run_speed = 125',
                         'name="ContactShadow"', 'z_index = -1', 'type="ConvexPolygonShape2D"',
                         'name="Occluder_pillar" type="Sprite2D" parent="World"',
                         'position = Vector2(275, 150)', 'offset = Vector2(-25, -90)',
                         'name="Walls" type="StaticBody2D" parent="."',
                         'name="Camera2D" type="Camera2D" parent="."',
                         'position = Vector2(200, 150)', 'zoom = Vector2(3.84, 3.84)',
                         'limit_left = 0', 'limit_top = 0', 'limit_right = 400', 'limit_bottom = 300'):
            self.assertIn(fragment, tower)
        self.assertEqual(tower.count('type="CollisionPolygon2D"'), len(collision(self.data)))
        points = [float(v) for v in re.search(r'^points = PackedVector2Array\((.*)\)', tower, re.M)[1].split(',')]
        self.assertEqual(len(points), 64)
        self.assertAlmostEqual(max(points[::2])-min(points[::2]), 120*0.22)
        self.assertAlmostEqual(max(points[1::2])-min(points[1::2]), 120*0.08)
        settings = (out/'project.godot').read_text()
        for fragment in ('run/main_scene="res://scenes/tower.tscn"', 'viewport_width=1536',
                         'viewport_height=1024', 'window/stretch/mode="canvas_items"'):
            self.assertIn(fragment, settings)
        self.assertEqual(len(validate_resources(out, include_scenes=True)), report['scene']['resource_references'])
        for resource in list(out.rglob('*.tres'))+list(out.rglob('*.tscn')):
            for path in re.findall(r'path="res://([^"]+)"', resource.read_text()):
                self.assertTrue((out/path).is_file(), path)
        self.assertEqual((self.scene/'plate.png').read_bytes(), (out/'scene/plate.png').read_bytes())
        for source in self.cells.glob('*.png'):
            anim, direction, _ = source.stem.split('_')
            self.assertEqual(source.read_bytes(), (out/'sprites'/anim/direction/source.name).read_bytes())

    def test_old_sandbox_is_byte_identical_with_scene_option(self):
        plain, tower = self.root/'plain', self.root/'tower'
        report = build_project(self.cells, plain)
        build_project(self.cells, tower, scene=self.scene)
        self.assertNotIn('scene', report)
        for path in ('scenes/main.tscn', 'scripts/keeper.gd', 'frames/keeper.tres'):
            self.assertEqual((plain/path).read_bytes(), (tower/path).read_bytes())
        self.assertIn('run/main_scene="res://scenes/main.tscn"', (plain/'project.godot').read_text())
        self.assertFalse((plain/'scenes/tower.tscn').exists())

    def test_missing_scene_files_overlap_and_bad_plate_rejected_before_output(self):
        with self.assertRaises(ValueError):
            build_project(self.cells, self.scene/'project', scene=self.scene)
        with self.assertRaises(ValueError):
            build_project(self.cells, self.root/'bad', scene=self.root/'missing')
        self.assertFalse((self.root/'bad').exists())
        Image.new('RGB', (401, 300)).save(self.scene/'plate.png')
        with self.assertRaises(ValueError):
            build_project(self.cells, self.root/'bad', scene=self.scene)
        self.assertFalse((self.root/'bad').exists())

    def test_scene_missing_escaping_and_undeclared_resources_rejected(self):
        out = self.root/'project'
        build_project(self.cells, out, scene=self.scene)
        tower = out/'scenes/tower.tscn'
        original = tower.read_text()
        for replacement in (original.replace('res://scene/plate.png', 'res://scene/missing.png'),
                            original.replace('res://scene/plate.png', 'res://../../escape.png'),
                            original.replace('ExtResource("3")', 'ExtResource("999")'),
                            original.replace('SubResource("Feet")', 'SubResource("Missing")')):
            tower.write_text(replacement)
            with self.assertRaises(ValueError):
                validate_resources(out, include_scenes=True)
        tower.write_text(original)
        settings = out/'project.godot'
        settings.write_text(settings.read_text().replace('scenes/tower.tscn', 'scenes/missing.tscn'))
        with self.assertRaises(ValueError):
            validate_resources(out, include_scenes=True)

    def test_cli_scene_option(self):
        proc = subprocess.run([sys.executable, '-B', '-m', 'export.godot_import',
                               '--cells', str(self.cells), '--out', str(self.root/'project'),
                               '--scene', str(self.scene)], capture_output=True, text=True, timeout=30)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)['scene']['plate_size'], [400, 300])

    @unittest.skipUnless(Path(GODOT).is_file(), 'Godot binary unavailable')
    def test_headless_tower_import_run_and_physics(self):
        out = self.root/'project'
        build_project(self.cells, out, scene=self.scene)
        (out/'probe.gd').write_text(PROBE)
        errors = []
        for args in (['--import'], ['--script', 'res://probe.gd']):
            proc = subprocess.run([GODOT, '--headless', '--path', str(out), *args],
                                  capture_output=True, text=True, timeout=90)
            log = proc.stdout+proc.stderr
            self.assertEqual(proc.returncode, 0, log)
            self.assertNotIn('SCRIPT ERROR', log)
            self.assertNotIn('T3H_ASSERTION:', log)
            errors.extend(line for line in log.splitlines() if 'ERROR' in line)
        self.assertIn('T3H_RUNTIME_ASSERTIONS=complete', log)
        self.assertEqual(errors, [], '\n'.join(errors))



def complex_rectangle_annotation():
    """1536x1024, 25 simple polygons, exactly 48 vertices per polygon."""
    a = annotation()
    a.update(plate_size=[1536, 1024], occluders=[], exits=[], spawn=[10, 10])
    corners = [(0, 0), (1536, 0), (1536, 1024), (0, 1024)]
    floor = []
    for first, last in zip(corners, corners[1:] + corners[:1]):
        floor.extend([[first[0]+(last[0]-first[0])*i/12,
                       first[1]+(last[1]-first[1])*i/12] for i in range(12)])
    a['walkable'], a['blocked'] = [floor], []
    for i in range(12):
        cx, cy = 200+(i % 4)*360, 180+(i // 4)*320
        for key, radius in [('walkable', 170), ('blocked', 25)]:
            a[key].append([[cx+radius*math.cos(2*math.pi*j/48),
                            cy+radius*math.sin(2*math.pi*j/48)] for j in range(48)])
    return a


class FastRectangleTests(unittest.TestCase):
    def assert_grid_contained(self, a, rectangle, cell_size=8):
        x0, y0, x1, y1 = rectangle
        self.assertTrue(x0 < x1 and y0 < y1)
        self.assertTrue(all(v % cell_size == 0 for v in rectangle))
        checked = 0
        # Independent winding test at each cell centre and all four corners.
        # Edge-interior adversaries below also verify sub-cell obstacles.
        for y in range(y0, y1, cell_size):
            for x in range(x0, x1, cell_size):
                for dx, dy in ((0, 0), (cell_size, 0), (0, cell_size),
                               (cell_size, cell_size), (cell_size/2, cell_size/2)):
                    point = (x+dx, y+dy)
                    self.assertTrue(any(contains(point, p) for p in a['walkable']), point)
                    self.assertFalse(any(contains(point, p) for p in a['blocked']), point)
                checked += 1
        self.assertEqual(checked, (x1-x0)*(y1-y0)//cell_size**2)
        grid = _walkable_grid(a, cell_size)
        self.assertTrue(grid[y0//cell_size:y1//cell_size, x0//cell_size:x1//cell_size].all())
        return checked

    def test_fixture_grid_maximum_inset_and_measurements(self):
        a = annotation()
        report = {}
        rect = largest_walkable_rectangle(a, report=report)
        self.assertEqual(rect, [32, 32, 240, 272])
        self.assertEqual(report['unshrunk_rectangle'], [24, 24, 248, 280])
        self.assertEqual(report['cells'], 37*50)
        self.assertEqual(report['area_px2'], 49920)
        self.assertEqual(report['rectangle_cells'], self.assert_grid_contained(a, rect))
        self.assertEqual(report['cell_size'], 8)
        self.assertGreaterEqual(report['wall_s'], 0)
        self.assertEqual([rect[0]-8, rect[1]-8, rect[2]+8, rect[3]+8],
                         report['unshrunk_rectangle'])

    def test_concave_l_with_blocked_hole(self):
        a = annotation()
        a.update(walkable=[[[0, 0], [400, 0], [400, 96], [128, 96],
                            [128, 300], [0, 300]]],
                 blocked=[[[40, 120], [72, 120], [72, 160], [40, 160]]], spawn=[16, 16])
        rect = largest_walkable_rectangle(a)
        self.assertEqual(rect, [8, 8, 392, 88])
        self.assert_grid_contained(a, rect)

    def test_tiny_hole_and_subcell_gap_cannot_hide_between_samples(self):
        a = annotation()
        a.update(walkable=[[[0, 0], [400, 0], [400, 300], [0, 300]]], spawn=[10, 10])
        a['blocked'] = [[[201, 121], [202, 121], [202, 122], [201, 122]]]
        grid = _walkable_grid(a, 8)
        self.assertFalse(grid[15, 25])  # No corner/centre is inside this hole.
        self.assert_grid_contained(a, largest_walkable_rectangle(a))
        a['blocked'] = []
        a['walkable'] = [[[0, 0], [201, 0], [201, 300], [0, 300]],
                         [[202, 0], [400, 0], [400, 300], [202, 300]]]
        self.assertFalse(_walkable_grid(a, 8)[:, 25].any())
        self.assert_grid_contained(a, largest_walkable_rectangle(a))

    def test_union_seams_winding_order_and_tie_determinism(self):
        a = annotation()
        a.update(blocked=[], spawn=[10, 10],
                 walkable=[[[0, 0], [201, 0], [201, 300], [0, 300]],
                           [[201, 0], [400, 0], [400, 300], [201, 300]]])
        expected = [8, 8, 392, 288]
        self.assertEqual(largest_walkable_rectangle(a), expected)
        a['walkable'] = [p[::-1] for p in a['walkable'][::-1]]
        self.assertEqual(largest_walkable_rectangle(a), expected)
        a['walkable'][0][0][0] = 200  # Overlap is still floor, not an obstacle.
        self.assertEqual(largest_walkable_rectangle(a), expected)
        grid = np.array([[1, 1, 0, 1, 1], [1, 1, 0, 1, 1]], dtype=bool)
        self.assertEqual(_maximal_rectangle(grid), [0, 0, 2, 2])

    def test_stack_matches_exhaustive_small_grids(self):
        for bits in range(1, 1 << 9):
            grid = np.array([(bits >> i) & 1 for i in range(9)], dtype=bool).reshape(3, 3)
            candidates = []
            for top in range(3):
                for left in range(3):
                    for bottom in range(top+1, 4):
                        for right in range(left+1, 4):
                            if grid[top:bottom, left:right].all():
                                candidates.append((-(bottom-top)*(right-left), top, left, bottom, right))
            _, top, left, bottom, right = min(candidates)
            self.assertEqual(_maximal_rectangle(grid), [left, top, right, bottom], bits)

    def test_named_cell_size_and_no_room_for_inset(self):
        a = annotation()
        a.update(plate_size=[100, 100], walkable=[[[0, 0], [100, 0], [100, 100], [0, 100]]],
                 blocked=[], occluders=[], exits=[], spawn=[10, 10])
        self.assertEqual(largest_walkable_rectangle(a, cell_size=10), [10, 10, 90, 90])
        for size in (0, -1, True, 1.5, '8', None):
            with self.subTest(size=size), self.assertRaises(ValueError):
                largest_walkable_rectangle(a, cell_size=size)
        for size in (50, 101):
            with self.subTest(size=size), self.assertRaises(ValueError):
                largest_walkable_rectangle(a, cell_size=size)
        with self.assertRaises(ValueError):
            largest_walkable_rectangle(a, report=[])
        with self.assertRaises(ValueError):
            _maximal_rectangle(np.zeros((3, 3), dtype=bool))
        a['walkable'] = []
        with self.assertRaises(ValueError):
            largest_walkable_rectangle(a)

    def test_25_polygons_48_vertices_within_five_seconds(self):
        a = complex_rectangle_annotation()
        polygons = a['walkable'] + a['blocked']
        self.assertEqual(len(polygons), 25)
        self.assertTrue(all(len(p) >= 40 for p in polygons))
        report = {}
        started = time.monotonic()
        rect = largest_walkable_rectangle(a, report=report)
        self.assertLessEqual(time.monotonic()-started, 5.0)
        self.assertLessEqual(report['wall_s'], 5.0)
        self.assertEqual(report['cells'], 128*192)
        self.assert_grid_contained(a, rect)


PROBE = '''extends SceneTree

func check(value: bool, message: String) -> void:
    if not value:
        printerr("T3H_ASSERTION: ", message)
        quit(7)

func _initialize() -> void:
    call_deferred("probe")

func probe() -> void:
    check(ProjectSettings.get_setting("application/run/main_scene") == "res://scenes/tower.tscn", "main scene")
    var scene = load("res://scenes/tower.tscn").instantiate()
    root.add_child(scene)
    await process_frame
    var keeper = scene.get_node("World/Keeper")
    keeper.set_physics_process(false)
    check(keeper.position == Vector2(120, 200), "spawn")
    check(keeper.sprite.to_global(Vector2(256, 400) + keeper.sprite.offset).is_equal_approx(keeper.global_position), "feet pivot")
    check(keeper.sprite.scale == Vector2(0.5, 0.5), "sprite scale")
    check(keeper.walk_speed == 75 and keeper.run_speed == 125, "movement scale")
    check(scene.get_node("World").y_sort_enabled, "world sorting")
    var cut = scene.get_node("World/Occluder_pillar")
    check(cut.position == Vector2(275, 150), "baseline origin")
    check(cut.to_global(cut.offset) == Vector2(250, 60), "crop alignment")
    check(keeper.get_node("ContactShadow").z_index < keeper.sprite.z_index, "shadow under figure")
    check(scene.get_node("Camera2D").get_parent() == scene, "fixed camera")
    await physics_frame
    var space = scene.get_world_2d().direct_space_state
    for pair in [[Vector2(275, 125), true], [Vector2(10, 200), true], [Vector2(160, 200), false]]:
        var query = PhysicsPointQueryParameters2D.new()
        query.position = pair[0]
        query.exclude = [keeper.get_rid()]
        check((space.intersect_point(query).size() > 0) == pair[1], "floor collision query")
    keeper.position = Vector2(220, 125)
    await physics_frame
    check(keeper.test_move(keeper.transform, Vector2(70, 0)), "blocked movement")
    keeper.position = Vector2(120, 200)
    await physics_frame
    check(not keeper.test_move(keeper.transform, Vector2(20, 0)), "walkable movement")
    print("T3H_RUNTIME_ASSERTIONS=complete")
    scene.queue_free()
    await process_frame
    quit(0)
'''


if __name__ == '__main__':
    unittest.main()
