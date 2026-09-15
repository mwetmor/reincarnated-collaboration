"""T3t: explicit authored frames, strict validation, timing and picker layers.

Fixture CLI writes only the requested T3t directory. Tests use tests/tmp.
No source artwork or external image-generation services are involved.
"""
import colorsys
import copy
import hashlib
import io
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
from export.effect_kit import build, load_kit, _tint
from export.godot_import import build_project, validate_resources, write_spriteframes
from oracle.vfx_measure import measure

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT/'runs/C-3/t3/T3t'
TMP = ROOT/'tests/tmp'
RAMP_ARTIFACTS = ROOT/'runs/C-3/t3/T3u'
RAMP = {'core': [.85, .95, 1], 'rim': [.15, .3, .9], 'hue_shift_deg_per_band': 8}


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


def picker_fixture(root, legacy=None, tint=None, phase_scale=None):
    """Tiny E/N/S cells and measured sockets; return kit and exported project."""
    root = Path(root).resolve()
    path, data = definition_fixture(root/'inputs')
    if tint is not None:
        data['tint'] = copy.deepcopy(tint)
    if phase_scale is not None:
        data['phase_scale'] = copy.deepcopy(phase_scale)
    path.write_text(json.dumps(data, indent=2)+'\n')
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


class TintRampTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix='t3u-', dir=TMP)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.path, self.data = definition_fixture(self.root/'inputs')
        self.data['tint'] = copy.deepcopy(RAMP)

    def build_data(self, data=None, name='kit'):
        self.path.write_text(json.dumps(self.data if data is None else data))
        out = self.root/name
        build(self.path, out)
        return out

    def test_ramp_t3t_literal_o4_acceptance(self):
        result = measure(self.build_data()/'impact', [1000*2/60, 1000*5/60])
        self.assertGreaterEqual(result['O4']['hue_sd_deg_at_peak'], 8)

    def test_ramp_t3t_literal_o5_acceptance(self):
        result = measure(self.build_data()/'impact', [1000*2/60, 1000*5/60])
        self.assertLess(result['O5']['bright_15_median_at_peak'],
                        result['O5']['dim_25_median_at_peak'])

    def test_mapping_matches_smoothstep_multiply_then_hsv_for_every_byte(self):
        # Independent scalar reference, including hue wrap and endpoint clamps.
        source = np.zeros((16,16,4), dtype=np.uint8)
        source[..., :3] = np.arange(256, dtype=np.uint8).reshape(16,16,1)
        source[..., 3] = 255
        p = self.root/'levels.png'; Image.fromarray(source).save(p)
        for shift in (-60, 0, 8, 60):
            tint = dict(RAMP, hue_shift_deg_per_band=shift)
            actual = np.array(_tint(p, tint, 1))
            for grey in range(256):
                light = grey/255
                t = 3*light**2-2*light**3
                base = [grey*((1-t)*rim+t*core)/255 for rim,core in zip(tint['rim'],tint['core'])]
                h,s,v = colorsys.rgb_to_hsv(*base)
                target = ([255]*3 if light >= .92 else
                          [round(x*255) for x in colorsys.hsv_to_rgb((h+(255-grey)*shift/360)%1,s,v)])
                np.testing.assert_array_equal(actual[grey//16,grey%16,:3], target)

    def test_sheet_band_indices_stable_when_frame_omits_bright_levels(self):
        # Sheet defines all four bands; sparse frame keeps dark band's index 3.
        sheet = np.array([[[v,v,v,255] for v in (255,192,128,64)]], dtype=np.uint8)
        Image.fromarray(sheet).save(self.root/'inputs/frame_0.png')
        Image.fromarray(sheet[:,3:]).save(self.root/'inputs/frame_1.png')
        out = self.build_data()
        first = np.array(Image.open(out/'impact/impact_00.png'))
        sparse = np.array(Image.open(out/'impact/impact_01.png'))
        np.testing.assert_array_equal(first[0,-1], sparse[0,0])

    def test_white_core_thresholds_alpha_hidden_rgb_and_zero_saturation(self):
        for keep in (.8,.92,1):
            tint = dict(RAMP, white_core_keep=keep)
            path = self.root/'inputs/frame_0.png'
            source = np.array(Image.open(path))
            actual = np.array(_tint(path,tint,1))
            np.testing.assert_array_equal(actual[...,3],source[...,3])
            white = (source[...,0]/255 >= keep) & (source[...,3] > 0)
            self.assertGreaterEqual(int(actual[white,:3].min()),250)
            np.testing.assert_array_equal(actual[source[...,3] == 0],source[source[...,3] == 0])
        neutral = {'core':[1,1,1], 'rim':[1,1,1], 'hue_shift_deg_per_band':60}
        image = np.array(_tint(path,neutral,1))
        np.testing.assert_array_equal(image[...,0],image[...,1])
        np.testing.assert_array_equal(image[...,1],image[...,2])

    def test_plain_tint_png_bytes_match_t3t_arithmetic(self):
        self.data['tint'] = [.25,.5,1]
        out = self.build_data()
        for phase in ('flare','travel','impact','residual'):
            for i in range(2):
                pixels = np.array(Image.open(self.root/f'inputs/frame_{i}.png'))
                grey = pixels[...,:3].astype(float) @ np.array([.2126,.7152,.0722])
                pixels[...,:3] = np.rint(pixels[...,:3]*np.array([.25,.5,1])).astype(np.uint8)
                pixels[grey >= .92*255,:3] = 255
                image = Image.fromarray(pixels).resize((48,48),Image.Resampling.NEAREST)
                stream = io.BytesIO();image.save(stream,format='PNG')
                self.assertEqual((out/phase/f'{phase}_{i:02d}.png').read_bytes(),stream.getvalue())
        self.assertNotIn('phase_scale',load_kit(out))

    def test_ramp_defaults_and_runtime_view_preserve_authored_json(self):
        self.data['tint'] = {k:RAMP[k] for k in ('core','rim')}
        out = self.build_data()
        before = (out/'kit.json').read_bytes()
        raw = load_kit(out,preserve_ramp=True)
        self.assertEqual(raw['tint'],dict(self.data['tint'],hue_shift_deg_per_band=0,white_core_keep=.92))
        self.assertEqual(raw['phase_scale'],dict.fromkeys(('cast','travel','impact','residual'),1))
        self.assertEqual(load_kit(out)['tint'],RAMP['core'])
        self.assertEqual((out/'kit.json').read_bytes(),before)

    def test_phase_scale_two_nearest_steps_boundaries_and_layers_unchanged(self):
        baseline = self.build_data(name='unscaled')
        self.data['phase_scale'] = {'cast':.5,'travel':1.125,'impact':4,'residual':2}
        out = self.build_data()
        for phase,name in [('cast','flare'),('travel','travel'),('impact','impact'),('residual','residual')]:
            scale = self.data['phase_scale'][phase]
            size = int(math.floor(48*scale+.5))
            original = Image.open(baseline/name/f'{name}_00.png')
            actual = Image.open(out/name/f'{name}_00.png')
            self.assertEqual(actual.size,(size,size))
            np.testing.assert_array_equal(actual,original.resize((size,size),Image.Resampling.NEAREST))
        for p in (baseline/'layers').glob('*.png'):
            self.assertEqual(p.read_bytes(),(out/'layers'/p.name).read_bytes())

    def test_fractional_scale_rounds_half_up_after_pixel_scale(self):
        path = self.root/'small.png';Image.new('RGBA',(3,5),(128,128,128,255)).save(path)
        self.assertEqual(_tint(path,RAMP,1,.5).size,(2,3))

    def test_picker_ramp_and_legacy_scenes_and_scaled_resource_bytes(self):
        plain = picker_fixture(self.root/'plain')
        ramp = picker_fixture(self.root/'ramp',tint=RAMP,phase_scale={'impact':2,'residual':.5})
        legacy_scenes = sorted((plain['project']/'scenes').glob('vfx_frost_*.tscn'))
        self.assertTrue(legacy_scenes)
        for p in legacy_scenes:
            self.assertEqual(p.read_bytes(),(ramp['project']/'scenes'/p.name).read_bytes())
        for p in (plain['project']/'scripts').glob('vfx_*.gd'):
            self.assertEqual(p.read_bytes(),(ramp['project']/'scripts'/p.name).read_bytes())
        project_kit = ramp['project']/'vfx/synthetic_ice'
        for phase,size in [('impact',96),('travel',48),('residual',24)]:
            with Image.open(project_kit/f'sprites/{phase}/{phase}_00.png') as image:
                self.assertEqual(image.size,(size,size))
        for p in ramp['kit'].rglob('*.png'):
            relative = p.relative_to(ramp['kit'])
            target = project_kit/relative if relative.parts[0] == 'layers' else project_kit/'sprites'/relative
            self.assertEqual(p.read_bytes(),target.read_bytes())
        scene = (ramp['project']/'scenes/vfx_synthetic_ice_impact.tscn').read_text()
        self.assertIn('res://vfx/synthetic_ice/impact.tres',scene)
        self.assertIn('texture_filter = 1',scene)
        self.assertIn('modulate = Color(0.85, 0.95, 1, 1)',scene)
        self.assertGreater(len(validate_resources(ramp['project'],True)),0)

    def test_invalid_ramps_and_scales_rejected_before_output(self):
        cases = [None,[],{}, {'core':[1,1,1]},dict(RAMP,unknown=0)]
        for field in ('core','rim'):
            for value in (None,[1,1],[1,1,1,1],[-.01,0,0],[1.01,0,0],[True,0,0],[float('nan'),0,0],[float('inf'),0,0]):
                cases.append(dict(RAMP,**{field:value}))
        for field,values in [('hue_shift_deg_per_band',[-60.01,60.01,True,None,float('nan'),float('inf'),'8']),
                             ('white_core_keep',[.7999,1.001,True,None,float('nan'),'0.92'])]:
            cases.extend(dict(RAMP,**{field:v}) for v in values)
        variants = [dict(self.data,tint=t) for t in cases]
        variants += [dict(self.data,phase_scale=s) for s in (None,[],{'unknown':1})]
        variants += [dict(self.data,phase_scale={'impact':v}) for v in (.49,4.01,True,None,float('nan'),float('inf'),'2')]
        for i,data in enumerate(variants):
            with self.subTest(case=i), self.assertRaises(ValueError): self.build_data(data)
            self.assertFalse((self.root/'kit').exists())

    def test_particle_independent_grayscale_size_and_frame_exception(self):
        independent = self.root/'inputs/particle.png'
        self.data['layers']['particles']['texture'] = 'particle.png'
        for size in ((1,1),(16,16),(16,1)):
            Image.new('L',size,128).save(independent)
            out = self.build_data(name='particle-'+str(size))
            with Image.open(out/'layers/particles.png') as image:
                self.assertEqual(image.size,tuple(3*v for v in size))
            load_kit(out)
        for size,colour in [((17,1),(128,128,128)),((1,17),(128,128,128)),((16,16),(128,127,128))]:
            Image.new('RGB',size,colour).save(independent)
            with self.subTest(size=size,colour=colour), self.assertRaises(ValueError): self.build_data()
            self.assertFalse((self.root/'kit').exists())
        Image.new('RGBA',(32,24),(128,128,128,255)).save(self.root/'inputs/frame_1.png')
        self.data['layers']['particles']['texture'] = 'frame_1.png'
        with Image.open(self.build_data()/'layers/particles.png') as image:
            self.assertEqual(image.size,(96,72))

    def test_four_band_diagnostic_measures_hue_and_saturation_known_bad_control(self):
        source = np.zeros((16,16,4),dtype=np.uint8)
        for i,grey in enumerate((255,160,96,32)):
            source[:,i*4:(i+1)*4,:3] = grey
        source[...,3] = 255
        path = self.root/'four-band.png';Image.fromarray(source).save(path)
        for label,tint in [('ramp',RAMP),('flat',[.25,.5,1])]:
            out = self.root/label;out.mkdir()
            _tint(path,tint,1).save(out/'frame.png')
            result = measure(out,60)
            if label == 'ramp':
                self.assertGreaterEqual(result['O4']['hue_sd_deg_at_peak'],8)
                self.assertLess(result['O5']['bright_15_median_at_peak'],result['O5']['dim_25_median_at_peak'])
            else:
                self.assertLess(result['O4']['hue_sd_deg_at_peak'],1)

    def test_runtime_invalid_ramp_and_scale_rejected(self):
        out = self.build_data()
        original = json.loads((out/'kit.json').read_text())
        for data in (dict(original,tint=dict(RAMP,hue_shift_deg_per_band=61)),
                     dict(original,phase_scale={'impact':0})):
            (out/'kit.json').write_text(json.dumps(data))
            with self.assertRaises(ValueError): load_kit(out)


def measure_ramp_fixture(root):
    """Literal T3t acceptance, recorded without substituting a different mask."""
    started = time.monotonic()
    root = Path(root).resolve();root.mkdir(parents=True,exist_ok=True)
    path,data = definition_fixture(root/'inputs')
    data['tint'] = copy.deepcopy(RAMP)
    data['phase_scale'] = {'impact':2,'residual':.5}
    path.write_text(json.dumps(data,indent=2)+'\n')
    report = build(path,root/'kit')
    measured = measure(root/'kit/impact',[1000*2/60,1000*5/60])
    (root/'measure.json').write_text(json.dumps(measured,indent=2)+'\n')
    with tempfile.TemporaryDirectory(prefix='t3u-acceptance-',dir=TMP) as tmp:
        plain = picker_fixture(Path(tmp)/'plain')
        ramp = picker_fixture(Path(tmp)/'ramp',tint=RAMP,phase_scale=data['phase_scale'])
        baseline = json.loads((RAMP_ARTIFACTS/'baseline.json').read_text())
        comparisons = {}
        for key in ('kit','project'):
            comparisons[key] = {name:hashlib.sha256((plain[key]/name).read_bytes()).hexdigest() == digest
                                for name,digest in baseline[key].items()}
        legacy = {p.name:p.read_bytes() == (ramp['project']/'scenes'/p.name).read_bytes()
                  for p in (plain['project']/'scenes').glob('vfx_frost_*.tscn')}
        resources = len(validate_resources(ramp['project'],True))
        picker_wall = ramp['export_report']['wall_s']
    pixels = np.array(Image.open(root/'kit/impact/impact_00.png'))
    result = {'id':'t3u_tint_ramp_acceptance','subject':'T3t unchanged 16x16 fixture','passed':None,
              'value':{'hue_sd_deg':measured['O4']['hue_sd_deg_at_peak'],
                       'bright_15_median_s':measured['O5']['bright_15_median_at_peak'],
                       'dim_25_median_s':measured['O5']['dim_25_median_at_peak'],
                       'white_core_min':int(pixels[:,48:72,:3].min()),
                       'baseline_byte_comparisons':comparisons,'legacy_scenes_byte_identical':legacy,
                       'phase_dimensions':{name:list(Image.open(root/f'kit/{name}/{name}_00.png').size)
                                           for name in ('flare','travel','impact','residual')},
                       'resource_references':resources},
              'threshold':{'hue_sd_deg_min':8,'bright_vs_dim':'strictly less','white_core_min':250,
                           'baseline_byte_comparisons':'all identical','legacy_scenes':'all identical'},
              'op':'report','unit':'mixed','evidence':[str(root/'measure.json'),str(root/'kit/kit.json')],
              'notes':'Literal fixture retained: opaque zero grey makes dim-25 median zero; only 64 and 128 bands exceed S>.3. No replacement acceptance fixture.',
              'build_wall_s':report['wall_s'],'picker_wall_s':picker_wall,'wall_s':time.monotonic()-started}
    (root/'acceptance.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def measure_frozen_orb_ramp(root):
    """Diagnostic only: recover nonwhite greys from Frozen Orb's unit blue tint.

    Source white levels were collapsed by T3t and cannot be reconstructed;
    preserve them as 255. Already scaled frames retain their native size.
    The original kit and its stored measurement are never rewritten.
    """
    started = time.monotonic()
    root = Path(root).resolve();root.mkdir(parents=True,exist_ok=True)
    frozen = ROOT/'runs/C-3/vfx_kits/frozen_orb'
    definition = json.loads((frozen/'kit.json').read_text())
    if definition['tint'][2] != 1:
        raise ValueError('Diagnostic recovery requires original blue tint exactly one')
    frames = definition['phases']['impact']['frames']
    timing = [f['hold_frames']*1000/60 for f in frames]
    baseline = measure(frozen/'impact',timing)
    recorded = json.loads((ROOT/'runs/C-3/artifacts/CS-vfx-frozenorb-kit-in/measure/fo_impact_measure.json').read_text())
    source,out = root/'source',root/'ramp'
    source.mkdir();out.mkdir()
    levels = set()
    for frame in frames:
        with Image.open(frozen/frame['file']) as image:
            rgba = np.array(image.convert('RGBA'))
        rgba[...,:3] = rgba[...,2,None]
        levels.update(np.unique(rgba[...,0][rgba[...,3]>0]).tolist())
        Image.fromarray(rgba).save(source/Path(frame['file']).name)
    for path in sorted(source.glob('*.png')):
        _tint(path,RAMP,1,band_levels=sorted(levels,reverse=True)).save(out/path.name)
    measured = measure(out,timing)
    (root/'measure.json').write_text(json.dumps(measured,indent=2)+'\n')
    def quantities(m):
        return {'hue_sd_deg':m['O4']['hue_sd_deg_at_peak'],
                'bright_15_median_s':m['O5']['bright_15_median_at_peak'],
                'dim_25_median_s':m['O5']['dim_25_median_at_peak']}
    result = {'id':'t3u_frozen_orb_diagnostic','subject':'Frozen Orb impact, recovered greys','passed':None,
              'value':{'recorded':quantities(recorded),'remeasured':quantities(baseline),
                       'ramp':quantities(measured),'source_grey_levels_bright_to_dark':sorted(levels,reverse=True)},
              'threshold':None,'op':'report','unit':'mixed',
              'evidence':[str(root/'measure.json')],
              'notes':'Diagnostic, not the literal T3t acceptance fixture. Unit blue recovers nonwhite greys; original white greys are unavailable and represented by 255. No extra resizing.',
              'wall_s':time.monotonic()-started}
    (root/'diagnostic.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--fixture':
        print(json.dumps(measure_fixture(sys.argv[2]), indent=2))
    elif len(sys.argv) == 3 and sys.argv[1] == '--ramp-fixture':
        print(json.dumps(measure_ramp_fixture(sys.argv[2]), indent=2))
    elif len(sys.argv) == 3 and sys.argv[1] == '--frozen-orb-ramp':
        print(json.dumps(measure_frozen_orb_ramp(sys.argv[2]), indent=2))
    else:
        unittest.main()
