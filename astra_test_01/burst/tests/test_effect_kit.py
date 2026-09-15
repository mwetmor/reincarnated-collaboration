"""T3t: explicit authored frames, strict validation, timing and picker layers.

Fixture CLI writes only the requested T3t directory. Tests use tests/tmp.
No source artwork or external image-generation services are involved.
"""
import colorsys
import copy
import json
import math
from pathlib import Path
import re
import shutil
import sys
import tempfile
import time
import unittest

import numpy as np
from PIL import Image
from export.effect_kit import build, load_kit
from export.godot_import import build_project, validate_resources, write_spriteframes

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT/'runs/C-3/t3/T3t'
TMP = ROOT/'tests/tmp'


def definition_fixture(root):
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    pixels = np.zeros((16, 16, 4), dtype=np.uint8)
    values = [0, 64, 128, 234, 235, 255, 128, 64]
    for i, value in enumerate(values):
        pixels[:, 2*i:2*i+2, :3] = value
        pixels[:, 2*i:2*i+2, 3] = 128 if i == 6 else (0 if i == 7 else 255)
    for i in range(2):
        Image.fromarray(np.roll(pixels, i, axis=1)).save(root/f'frame_{i}.png')
    data = {'name': 'synthetic_ice', 'element': 'frost', 'tint': [.25, .5, 1],
            'pixel_scale': 3, 'ground_squash': .6,
            'phases': {phase: {'sheet': 'frame_0.png', 'frames': [
                {'file': 'frame_0.png', 'hold_frames': 2},
                {'file': 'frame_1.png', 'hold_frames': 5}]} for phase in ('cast', 'travel', 'impact', 'residual')},
            'layers': {'dark_duplicate': True, 'glow': {'alpha': .4, 'scale': 1.2},
                       'floor_light': {'duration_s': .2, 'radius_px': 24},
                       'flash': {'duration_s': .1, 'alpha': .5, 'scale_from': 1.2, 'scale_to': 1},
                       'decal': {'file': 'frame_0.png', 'duration_s': 1.5},
                       'hitstop': {'duration_s': .08, 'time_scale': .1},
                       'shake': {'distance': 3, 'duration_s': .12},
                       'particles': {'texture': 'frame_1.png', 'amount': 8, 'lifetime_s': .3,
                                     'velocity_px_s': [10, 30], 'direction': [1, 0], 'spread_deg': 15}}}
    data['phases']['travel'].update(speed_px_s=360, streak=True)
    path = root/'effect.json'
    path.write_text(json.dumps(data, indent=2)+'\n')
    return path, data


def picker_fixture(root, legacy=None):
    """Tiny E/N/S cells and measured sockets; return kit and exported project."""
    root = Path(root).resolve()
    path, data = definition_fixture(root/'inputs')
    kit = root/'kit'
    report = build(path, kit)
    cells = root/'inputs/cells'
    cells.mkdir()
    socket_cells = {}
    for direction in ('E', 'N', 'S'):
        for kind, count in (('idle', 1), ('cast', 4)):
            for i in range(count):
                Image.new('RGBA', (512, 512), (40, 80, 120, 255)).save(cells/f'{kind}_{direction}_{i}.png')
        socket_cells['cast_'+direction] = {'sockets': [[270,240]]*4, 'release_index': 2}
    sockets = root/'inputs/sockets.json'
    sockets.write_text(json.dumps({'version': 1, 'canvas': [512,512], 'cells': socket_cells})+'\n')
    if legacy is None:
        legacy = root/'legacy'
        for name in ('flare', 'impact'):
            (legacy/name).mkdir(parents=True)
            for i in range(2):
                Image.new('RGBA', (8,8), (30,90,180,255)).save(legacy/name/f'{name}_{i}.png')
        (legacy/'CREDITS.txt').write_text('T3t synthetic legacy fixture.\n')
    catalogue = root/'kits.json'
    catalogue.write_text(json.dumps({'kits': [{'name': data['name'], 'dir': str(kit)},
                                             {'name': 'frost', 'dir': str(legacy)}]})+'\n')
    project = root/'project'
    export = build_project(cells, project, vfx_kits=catalogue, sockets=sockets)
    return {'definition': path, 'kit': kit, 'cells': cells, 'sockets': sockets,
            'catalogue': catalogue, 'project': project, 'legacy': legacy,
            'build_report': report, 'export_report': export}


def measure_fixture(root):
    started = time.monotonic()
    fixture = picker_fixture(root, ROOT/'runs/C-3/vfx_kits/frost')
    kit, project = fixture['kit'], fixture['project']
    pixels = np.array(Image.open(kit/'travel/travel_00.png'))
    actual = pixels[0, 12, :3].tolist()
    hue = colorsys.rgb_to_hsv(*(v/255 for v in actual))[0]
    expected_hue = colorsys.rgb_to_hsv(.25,.5,1)[0]
    durations = [float(v) for v in re.findall(r'"duration": ([0-9.e+-]+)', (project/'vfx/synthetic_ice/travel.tres').read_text())]
    legacy_scene = (project/'scenes/vfx_frost_bolt.tscn').read_bytes()
    frozen_scene = (ROOT/'runs/C-3/cliffside_v10/scenes/vfx_frost_bolt.tscn').read_bytes()
    report = {'id': 'effect_kit_acceptance', 'subject': 'T3t/synthetic', 'passed': None,
              'value': {'phases': 4, 'frames_per_phase': 2, 'native_size': [16,16],
                        'pixel_scale': 3, 'output_size': list(pixels.shape[1::-1]),
                        'tinted_rgb': actual, 'hue_error_turns': abs(hue-expected_hue),
                        'white_core_min': int(pixels[:,24:36,:3].min()),
                        'nearest_exact': bool(np.array_equal(pixels, np.repeat(np.repeat(pixels[::3,::3],3,0),3,1))),
                        'durations_s': durations, 'expected_durations_s': [2/60,5/60],
                        'legacy_bolt_byte_identical': legacy_scene == frozen_scene,
                        'resource_references': len(validate_resources(project, True))},
              'threshold': None, 'op': None, 'unit': 'mixed',
              'evidence': [str(kit/'kit.json'), str(project/'scenes/vfx_synthetic_ice_bolt.tscn')],
              'notes': 'Synthetic measurements; runtime E/N and collision are a separate headless test.',
              'build_wall_s': fixture['build_report']['wall_s'],
              'export_wall_s': fixture['export_report']['wall_s'], 'wall_s': time.monotonic()-started}
    (Path(root)/'acceptance.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


class EffectKitTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix='effect-kit-', dir=TMP)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.path, self.data = definition_fixture(self.root/'inputs')
        self.out = self.root/'kit'

    def reject(self, data):
        self.path.write_text(json.dumps(data))
        with self.assertRaises(ValueError): build(self.path, self.out)
        self.assertFalse(self.out.exists(), 'Validation must precede all output')

    def test_two_frame_phases_hue_white_core_alpha_nearest_and_dimensions(self):
        report = build(self.path, self.out)
        self.assertIsNone(report['passed'])
        for phase in ('flare', 'travel', 'impact', 'residual'):
            self.assertEqual(len(list((self.out/phase).glob('*.png'))), 2)
            pixels = np.array(Image.open(self.out/phase/f'{phase}_00.png'))
            self.assertEqual(pixels.shape, (48,48,4))
            np.testing.assert_array_equal(pixels[0,12,:3], [32,64,128])
            hue = colorsys.rgb_to_hsv(*pixels[0,12,:3].astype(float))[0]
            self.assertAlmostEqual(hue, colorsys.rgb_to_hsv(.25,.5,1)[0], places=12)
            self.assertGreaterEqual(int(pixels[:,24:36,:3].min()), 250)
            self.assertEqual(int(pixels[0,36,3]), 128)
            self.assertEqual(int(pixels[0,42,3]), 0)
            np.testing.assert_array_equal(pixels, np.repeat(np.repeat(pixels[::3,::3],3,0),3,1))
            self.assertEqual(set(map(tuple, pixels.reshape(-1,4))),
                {(0,0,0,255), (16,32,64,255), (32,64,128,255), (58,117,234,255),
                 (255,255,255,255), (32,64,128,128), (16,32,64,0)})
        self.assertTrue((self.out/'CREDITS.txt').is_file())
        self.assertTrue((self.out/'vfx_select.json').is_file())
        self.assertEqual(load_kit(self.out)['layers']['hitstop'], {'duration_s': .08, 'time_scale': .1})

    def test_holds_are_seconds_at_speed_one_in_every_resource(self):
        build(self.path, self.out)
        for phase in ('flare', 'travel', 'impact', 'residual'):
            text = (self.out/(phase+'.tres')).read_text()
            self.assertEqual([float(v) for v in re.findall(r'"duration": ([0-9.e+-]+)', text)], [2/60,5/60])
            self.assertIn('"speed": 1.0', text)
            self.assertIn('"loop": '+str(phase == 'travel').lower(), text)

    def test_scale_boundaries_and_white_threshold(self):
        for scale in range(1,9):
            data = copy.deepcopy(self.data);data['pixel_scale'] = scale
            self.path.write_text(json.dumps(data))
            out = self.root/f'scale-{scale}'
            build(self.path, out)
            pixels = np.array(Image.open(out/'flare/flare_00.png'))
            self.assertEqual(pixels.shape[:2], (16*scale,16*scale))
            np.testing.assert_array_equal(pixels[0,6*scale,:3], [58,117,234])
            np.testing.assert_array_equal(pixels[0,8*scale,:3], [255,255,255])

    def test_minimal_definition_optional_layers_residual_and_travel_defaults(self):
        data = copy.deepcopy(self.data)
        data['layers'] = {}
        del data['phases']['residual']
        for key in ('speed_px_s', 'streak'): del data['phases']['travel'][key]
        self.path.write_text(json.dumps(data))
        build(self.path, self.out)
        result = load_kit(self.out)
        self.assertEqual(result['phases']['travel']['speed_px_s'], 520)
        self.assertFalse(result['phases']['travel']['streak'])
        self.assertFalse((self.out/'residual').exists())

    def test_missing_and_unknown_keys_at_all_schema_levels(self):
        paths = [(), ('phases',), ('phases','cast'), ('phases','travel'),
                 ('phases','impact','frames',0), ('layers',)]
        paths += [('layers',name) for name in self.data['layers'] if name != 'dark_duplicate']
        for path in paths:
            data = copy.deepcopy(self.data);item = data
            for key in path: item = item[key]
            item['unexpected'] = 1
            with self.subTest(unknown=path): self.reject(data)
        for path, key in [((), 'name'), ((), 'tint'), (('phases',), 'travel'),
                          (('phases','cast'), 'sheet'), (('phases','cast','frames',0), 'hold_frames'),
                          (('layers','glow'), 'alpha'), (('layers','particles'), 'texture')]:
            data = copy.deepcopy(self.data);item = data
            for part in path: item = item[part]
            del item[key]
            with self.subTest(missing=(path,key)): self.reject(data)

    def test_invalid_numbers_booleans_holds_ranges_and_shapes(self):
        bad = {
            ('pixel_scale',): [0,9,1.5,True,None], ('ground_squash',): [.49,.651,float('nan'),True],
            ('tint',): [[1,0], [1,0,2], [1,-.1,0], [True,0,0], [float('inf'),0,0]],
            ('name',): ['', '../bad', 'two words', True], ('element',): ['', [], None],
            ('phases','cast','frames'): [[], {}, None],
            ('phases','cast','frames',0,'hold_frames'): [0,-1,1.5,True,float('inf')],
            ('phases','travel','speed_px_s'): [0,-1,True,float('nan')],
            ('phases','travel','streak'): [1,'yes',None],
            ('layers','dark_duplicate'): [0,'false',None],
            ('layers','glow','alpha'): [-.1,1.1,True,float('nan')],
            ('layers','glow','scale'): [0,-1,True],
            ('layers','floor_light','radius_px'): [0,-1],
            ('layers','flash','duration_s'): [-1,float('inf')],
            ('layers','hitstop','time_scale'): [0,1.1,True],
            ('layers','shake','distance'): [-1,True],
            ('layers','particles','amount'): [0,513,1.5,True],
            ('layers','particles','lifetime_s'): [0,-1],
            ('layers','particles','velocity_px_s'): [[2,1],[1],[-1,2],True],
            ('layers','particles','direction'): [[0,0],[1],[True,1],[float('nan'),1]],
            ('layers','particles','spread_deg'): [-1,181,True],
        }
        for path, values in bad.items():
            for value in values:
                data = copy.deepcopy(self.data);item = data
                for key in path[:-1]: item = item[key]
                item[path[-1]] = value
                with self.subTest(path=path, value=value): self.reject(data)

    def test_every_asset_validated_missing_corrupt_and_color_before_output(self):
        paths = [('phases','cast','sheet'), ('phases','travel','frames',1,'file'),
                 ('phases','residual','sheet'), ('layers','decal','file'), ('layers','particles','texture')]
        for path in paths:
            data = copy.deepcopy(self.data);item = data
            for key in path[:-1]: item = item[key]
            item[path[-1]] = 'missing.png'
            with self.subTest(path=path): self.reject(data)
        (self.root/'inputs/frame_1.png').write_bytes(b'corrupt')
        self.reject(self.data)
        Image.new('RGBA',(16,16),(40,60,80,255)).save(self.root/'inputs/frame_1.png')
        self.reject(self.data)

    def test_dict_paths_no_cwd_mutation_and_output_overlap_stale_rejected(self):
        data = copy.deepcopy(self.data)
        for phase in data['phases'].values():
            phase['sheet'] = str(self.root/'inputs'/phase['sheet'])
            for frame in phase['frames']: frame['file'] = str(self.root/'inputs'/frame['file'])
        for name,key in (('decal','file'),('particles','texture')):
            data['layers'][name][key] = str(self.root/'inputs'/data['layers'][name][key])
        before = copy.deepcopy(data)
        cwd = Path.cwd()
        build(data,self.out)
        self.assertEqual(data,before)
        self.assertEqual(Path.cwd(),cwd)
        with self.assertRaises(ValueError): build(data,self.out)
        with self.assertRaises(ValueError): build(data,self.root/'inputs')
        self.assertTrue((self.root/'inputs/frame_0.png').is_file())

    def test_generated_metadata_rejects_unknown_missing_and_escaping_assets(self):
        build(self.path,self.out)
        original = json.loads((self.out/'kit.json').read_text())
        for value in ('../../inputs/frame_0.png', str(self.root/'inputs/frame_0.png'), 'missing.png'):
            data = copy.deepcopy(original);data['phases']['travel']['frames'][0]['file'] = value
            (self.out/'kit.json').write_text(json.dumps(data))
            with self.subTest(file=value), self.assertRaises(ValueError): load_kit(self.out)
        original['unknown'] = 1
        (self.out/'kit.json').write_text(json.dumps(original))
        with self.assertRaises(ValueError): load_kit(self.out)

    def test_spriteframe_duration_extension_default_bytes_and_invalid_before_resource(self):
        Image.new('RGBA',(1,1)).save(self.root/'frame.png')
        animations = {'idle': (['frame.png'], 20, True)}
        write_spriteframes(self.root,'legacy.tres',animations)
        text = (self.root/'legacy.tres').read_text()
        self.assertIn('"duration": 1.0',text)
        self.assertIn('"speed": 20.0',text)
        for values in ({}, {'idle':[]}, {'idle':[0]}, {'idle':[True]}, {'idle':[float('nan')]}):
            with self.assertRaises(ValueError): write_spriteframes(self.root,'bad.tres',animations,values)
            self.assertFalse((self.root/'bad.tres').exists())


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--fixture':
        print(json.dumps(measure_fixture(sys.argv[2]), indent=2))
    else:
        unittest.main()
