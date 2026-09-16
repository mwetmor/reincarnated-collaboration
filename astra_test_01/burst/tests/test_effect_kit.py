"""T3t..T4a: indexed frames, strict validation, timing and shared palette materials.

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
from export.effect_kit import (build, load_kit, _tint, distance_field, material_pixels,
                               validate_material, shader_source, write_vfx_material)
from export.godot_import import build_project, validate_resources, write_spriteframes
from oracle.vfx_measure import measure

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT/'runs/C-3/t3/T3t'
TMP = ROOT/'tests/tmp'
RAMP_ARTIFACTS = ROOT/'runs/C-3/t3/T3u'
PALETTE = [[12/255, 30/255, 60/255, 1], [42/255, 86/255, 156/255, 1],
           [80/255, 175/255, 225/255, 1], [220/255, 244/255, 250/255, 1]]
RAMP = {'core': [.85, .95, 1], 'rim': [.15, .3, .9], 'hue_shift_deg_per_band': 8}


def definition_fixture(root):
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    pixels = np.zeros((16, 16, 4), dtype=np.uint8)
    values = [0, 85, 170, 255, 255, 255, 170, 85]
    for i, value in enumerate(values):
        pixels[:, 2*i:2*i+2, :3] = value
        pixels[:, 2*i:2*i+2, 3] = 128 if i == 6 else (0 if i == 7 else 255)
    for i in range(2):
        Image.fromarray(np.roll(pixels, i, axis=1)).save(root/f'frame_{i}.png')
    data = {'name': 'synthetic_ice', 'element': 'frost', 'material': {'palette': copy.deepcopy(PALETTE)},
            'ground_squash': .6,
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
        data['material'] = {'palette': copy.deepcopy(PALETTE)}
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

    def test_native_index_frames_alpha_and_dimensions(self):
        report = build(self.path, self.out)
        self.assertIsNone(report['passed'])
        for phase in ('flare', 'travel', 'impact', 'residual'):
            self.assertEqual(len(list((self.out/phase).glob('*.png'))), 2)
            with Image.open(self.out/phase/f'{phase}_00.png') as actual, Image.open(self.path.parent/'frame_0.png') as source:
                self.assertEqual(actual.size, (16,16))
                np.testing.assert_array_equal(actual, source)
        self.assertEqual(load_kit(self.out)['layers']['hitstop'], {'duration_s': .08, 'time_scale': .1})

    def test_holds_are_seconds_at_speed_one_in_every_resource(self):
        build(self.path, self.out)
        for phase in ('flare', 'travel', 'impact', 'residual'):
            text = (self.out/(phase+'.tres')).read_text()
            self.assertEqual([float(v) for v in re.findall(r'"duration": ([0-9.e+-]+)', text)], [2/60,5/60])
            self.assertIn('"speed": 1.0', text)
            self.assertIn('"loop": '+str(phase == 'travel').lower(), text)

    def test_retired_pixel_scale_rejected_without_output(self):
        for scale in range(1,9):
            data = dict(self.data, pixel_scale=scale)
            self.path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, 'pixel_scale'):
                build(self.path, self.out)
            self.assertFalse(self.out.exists())

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
        for path, key in [((), 'name'), ((), 'material'), (('phases',), 'travel'),
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
        self.data['material'] = {'palette': copy.deepcopy(PALETTE)}

    def build_data(self, data=None, name='kit'):
        self.path.write_text(json.dumps(self.data if data is None else data))
        out = self.root/name
        build(self.path, out)
        return out

    def test_legacy_kit_white_core_keep_rejected_at_load(self):
        with self.assertRaisesRegex(ValueError, 'white_core_keep'):
            load_kit(ROOT/'runs/C-3/vfx_kits/frozen_orb_v3')

    def test_legacy_kit_white_core_keep_rejected_before_build(self):
        legacy = ROOT/'runs/C-3/vfx_kits/frozen_orb_v3/kit.json'
        with self.assertRaisesRegex(ValueError, 'white_core_keep'):
            build(legacy, self.root/'kit')
        self.assertFalse((self.root/'kit').exists())

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
        sheet = np.array([[[v,v,v,255] for v in (255,170,85,0)]], dtype=np.uint8)
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

    def test_plain_multiply_tint_rejected_at_build_and_load(self):
        out = self.build_data()
        for tint in ([.25,.5,1], RAMP):
            with self.assertRaisesRegex(ValueError, 'tint'):
                self.build_data(dict(self.data, tint=tint), 'bad')
            meta = json.loads((out/'kit.json').read_text())
            meta['tint'] = tint
            (out/'kit.json').write_text(json.dumps(meta))
            with self.assertRaisesRegex(ValueError, 'tint'): load_kit(out)

    def test_material_defaults_and_runtime_view_preserve_authored_json(self):
        out = self.build_data()
        before = (out/'kit.json').read_bytes()
        raw = load_kit(out, preserve_ramp=True)
        self.assertEqual(raw['material'], dict(palette=PALETTE, blend_mode='MIX', light_participation=False, erode=0., dissolve=0.))
        self.assertEqual(load_kit(out), raw)
        self.assertEqual((out/'kit.json').read_bytes(), before)

    def test_phase_scale_is_runtime_only_and_native_pngs_unchanged(self):
        baseline = self.build_data(name='unscaled')
        self.data['phase_scale'] = {'cast':.5,'travel':1.125,'impact':4,'residual':2}
        out = self.build_data()
        for p in baseline.rglob('*.png'):
            self.assertEqual(p.read_bytes(), (out/p.relative_to(baseline)).read_bytes())
        project = particle_scenes(out, self.root/'project')
        scene = (project/'scenes/vfx_synthetic_ice_impact.tscn').read_text()
        self.assertIn('scale = Vector2(4, 4)', scene)
        self.assertIn('scale = Vector2(2, 2)', scene)

    def test_fractional_scale_rounds_half_up_after_pixel_scale(self):
        path = self.root/'small.png';Image.new('RGBA',(3,5),(128,128,128,255)).save(path)
        self.assertEqual(_tint(path,RAMP,1,.5).size,(2,3))

    def test_picker_palette_and_legacy_scenes_byte_lock(self):
        plain = picker_fixture(self.root/'plain')
        ramp = picker_fixture(self.root/'ramp', phase_scale={'impact':2,'residual':.5})
        legacy = sorted((plain['project']/'scenes').glob('vfx_frost_*.tscn'))
        self.assertTrue(legacy)
        for p in legacy:
            self.assertEqual(p.read_bytes(), (ramp['project']/'scenes'/p.name).read_bytes())
        for p in (plain['project']/'scripts').glob('vfx_frost*.gd'):
            self.assertEqual(p.read_bytes(), (ramp['project']/'scripts'/p.name).read_bytes())
        scene = (ramp['project']/'scenes/vfx_synthetic_ice_impact.tscn').read_text()
        self.assertIn('texture_filter = 2', scene)
        self.assertNotIn('texture_filter = 1', scene)
        self.assertIn('MaterialBody', scene)
        self.assertGreater(len(validate_resources(ramp['project'], True)), 0)
        self.assertEqual(load_kit(ramp['project']/'vfx/synthetic_ice')['material']['palette'], PALETTE)
        keeper = (ramp['project']/'scripts/keeper.gd').read_text()
        self.assertIn('materials/Additive.tres', keeper)
        self.assertIn('material.gd").bind(flare', keeper)

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
            Image.new('L',size,85).save(independent)
            out = self.build_data(name='particle-'+str(size))
            with Image.open(out/'layers/particles.png') as image:
                self.assertEqual(image.size,size)
            load_kit(out)
        for size,colour in [((17,1),(128,128,128)),((1,17),(128,128,128)),((16,16),(128,127,128))]:
            Image.new('RGB',size,colour).save(independent)
            with self.subTest(size=size,colour=colour), self.assertRaises(ValueError): self.build_data()
            self.assertFalse((self.root/'kit').exists())
        Image.new('RGBA',(32,24),(85,85,85,255)).save(self.root/'inputs/frame_1.png')
        self.data['layers']['particles']['texture'] = 'frame_1.png'
        with Image.open(self.build_data()/'layers/particles.png') as image:
            self.assertEqual(image.size,(32,24))

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


PARTICLE_ARTIFACTS = ROOT/'runs/C-3/t3/T3v'


def particle_fixture(root, tint, element_class=None):
    """Four-pixel greyscale mote, including partial and zero alpha."""
    path, data = definition_fixture(root)
    rgba = np.full((4, 4, 4), 255, dtype=np.uint8)
    rgba[..., 3] = np.array([0, 64, 128, 255], dtype=np.uint8)[:, None]
    Image.fromarray(rgba).save(path.parent/'mote.png')
    data['material'] = {'palette': copy.deepcopy(PALETTE)}
    data['layers']['particles'] = {'texture': 'mote.png', 'velocity_px_s': [10, 30],
                                   'direction': [1, 0], 'spread_deg': 15}
    if element_class is not None:
        data['element_class'] = element_class
    path.write_text(json.dumps(data, indent=2)+'\n')
    return path, data


def particle_scenes(kit_path, out, name='synthetic_ice'):
    from export.godot_import import _load_vfx_kit, _write_authored_effect
    for part in ('scripts', 'scenes', 'vfx/'+name):
        (out/part).mkdir(parents=True, exist_ok=True)
    _write_authored_effect(out, _load_vfx_kit(kit_path), 'vfx/'+name, 'vfx_'+name, {})
    return out


def particle_node(text):
    marker = '[node name="Particles" type="CPUParticles2D" parent="."]\n'
    return text.split(marker, 1)[1].split('[node ', 1)[0]


def t3v_regression(root):
    """Compare pre-change captures; normalize only the requested additions."""
    baseline = json.loads((PARTICLE_ARTIFACTS/'baseline.json').read_text())
    fixture = picker_fixture(root/'synthetic')
    comparisons = {}

    def compare(label, directory, expected, tint=None):
        actual = {str(p.relative_to(directory)): p for p in directory.rglob('*') if p.is_file()}
        result = {'file_set_equal': set(actual) == set(expected), 'identical': [],
                  'allowed_changes': [], 'unexpected_changes': []}
        for name, digest in expected.items():
            if name not in actual:
                result['unexpected_changes'].append(name)
                continue
            raw = actual[name].read_bytes()
            if hashlib.sha256(raw).hexdigest() == digest:
                result['identical'].append(name)
                continue
            normalized = raw
            if name.endswith('kit.json'):
                data = json.loads(raw)
                if data.pop('element_class', None) != 'strike':
                    result['unexpected_changes'].append(name)
                    continue
                normalized = (json.dumps(data, indent=2)+'\n').encode()
            elif name.endswith('.tscn') and b'[node name="Particles"' in raw:
                text = raw.decode()
                node = particle_node(text)
                colour = ', '.join(format(float(v), '.12g') for v in (*tint, 1))
                line = 'modulate = Color('+colour+')\n'
                if node.count(line) != 1:
                    result['unexpected_changes'].append(name)
                    continue
                normalized = text.replace(node, node.replace(line, '', 1), 1).encode()
            elif name.endswith('layers/particles.png'):
                result['allowed_changes'].append(name)
                continue
            key = ('allowed_changes' if hashlib.sha256(normalized).hexdigest() == digest
                   else 'unexpected_changes')
            result[key].append(name)
        comparisons[label] = result

    for key in ('kit', 'project'):
        compare('synthetic/'+key, fixture[key], baseline['synthetic'][key], [.25, .5, 1])
    for name in ('frozen_orb_v3', 'zeus_chain'):
        kit = ROOT/'runs/C-3/vfx_kits'/name
        target = particle_scenes(kit, root/name, name)
        compare(name, target, baseline['real'][name], load_kit(kit)['tint'])
    return comparisons


class TintedParticleTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix='t3v-', dir=TMP)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_particles_use_native_indices_and_independent_alpha(self):
        path, data = particle_fixture(self.root/'source', None)
        out = self.root/'kit'
        build(path, out)
        with Image.open(path.parent/'mote.png') as source, Image.open(out/'layers/particles.png') as result:
            np.testing.assert_array_equal(result, source)
            rendered = material_pixels(np.array(result), PALETTE)
            np.testing.assert_array_equal(rendered[..., 3], np.array(source)[..., 3])
        self.assertEqual(load_kit(out)['layers']['particles']['amount'], 8)

    def test_small_mote_cap_across_pixel_scales_and_ramp_thresholds(self):
        from export.effect_kit import _tint_particles
        for size in ((1, 1), (2, 4), (4, 4)):
            path = self.root/'mote.png'
            Image.new('RGBA', size, (255, 255, 255, 128)).save(path)
            for scale in (1, 3, 8):
                outputs = []
                for keep in (.8, .92, 1):
                    image = _tint_particles(path, dict(RAMP, white_core_keep=keep), scale)
                    self.assertLessEqual(max(image.size), 4)
                    outputs.append(np.array(image))
                np.testing.assert_array_equal(outputs[0], outputs[1])
                np.testing.assert_array_equal(outputs[1], outputs[2])

    def test_bolt_and_impact_particles_have_linear_shader_and_defaults(self):
        path, _ = particle_fixture(self.root/'source', None)
        kit = self.root/'kit'; build(path, kit)
        project = particle_scenes(kit, self.root/'project')
        for kind in ('bolt', 'impact'):
            node = particle_node((project/f'scenes/vfx_synthetic_ice_{kind}.tscn').read_text())
            self.assertIn('texture_filter = 2', node)
            self.assertIn('MaterialAdditive', node)
            self.assertIn('modulate = Color(1, 1, 1, 1)', node)
            self.assertIn('amount = 8\nlifetime = 0.5', node)
        (project/'project.godot').write_text('[application]\nrun/main_scene="res://scenes/vfx_synthetic_ice_bolt.tscn"\n')
        self.assertGreater(len(validate_resources(project, True)), 0)

    def test_element_classes_and_explicit_particle_settings(self):
        for value in ('strike', 'holy', 'field'):
            path, data = particle_fixture(self.root/value, [.2, .6, .8], value)
            data['layers']['particles'].update(amount=16, lifetime_s=.7)
            path.write_text(json.dumps(data))
            out = self.root/(value+'-kit'); build(path, out)
            self.assertEqual(load_kit(out)['element_class'], value)
            self.assertEqual(load_kit(out)['layers']['particles']['amount'], 16)
            self.assertEqual(load_kit(out)['layers']['particles']['lifetime_s'], .7)
            project = particle_scenes(out, self.root/(value+'-project'))
            self.assertEqual(json.loads((project/'vfx/synthetic_ice/kit.json').read_text())['element_class'], value)

    def test_unknown_element_classes_rejected_before_output_and_at_load(self):
        path, data = particle_fixture(self.root/'inputs', [.2, .6, .8])
        out = self.root/'kit'; build(path, out)
        metadata = json.loads((out/'kit.json').read_text())
        for value in ('unknown', 'Strike', '', None, True, 1, [], {}):
            with self.subTest(value=value):
                path.write_text(json.dumps(dict(data, element_class=value)))
                with self.assertRaises(ValueError): build(path, self.root/'bad')
                self.assertFalse((self.root/'bad').exists())
                (out/'kit.json').write_text(json.dumps(dict(metadata, element_class=value)))
                with self.assertRaises(ValueError): load_kit(out)

    def test_non_authored_export_byte_lock_and_legacy_validation(self):
        first = picker_fixture(self.root/'first')
        second = picker_fixture(self.root/'second', phase_scale={'impact':2})
        for part in ('scenes', 'scripts'):
            names = list((first['project']/part).glob('vfx_frost*'))
            self.assertTrue(names)
            for file in names:
                self.assertEqual(file.read_bytes(), (second['project']/part/file.name).read_bytes())
        with self.assertRaisesRegex(ValueError, 'white_core_keep'):
            load_kit(ROOT/'runs/C-3/vfx_kits/frozen_orb_v3')


def material_fixture():
    """Literal T4a 64x64 fixture: four equally covered opaque index bands."""
    pixels = np.full((64, 64, 4), 255, dtype=np.uint8)
    for band, level in enumerate((0, 85, 170, 255)):
        pixels[:, band*16:(band+1)*16, :3] = level
    return pixels


def assert_render_proof(test, report):
    """Conductor result checks. Missing/dummy rendering can never be accepted."""
    test.assertEqual(report['renderer'], 'gl_compatibility')
    test.assertTrue(report['shader_loaded'])
    test.assertTrue(report['rendered_frame_available'])
    test.assertLessEqual(report['palette_max_delta_255'], 1)
    test.assertEqual(report['index_0_min_alpha_255'], 255)
    test.assertEqual(report['erode_removed_percent'][0], 0)
    test.assertLessEqual(abs(report['erode_removed_percent'][1]-50), 3)
    test.assertEqual(report['erode_removed_percent'][2], 100)
    test.assertEqual(report['dissolve_05_removed_per_band'], [0, 0, 0, 1024])
    test.assertLessEqual(report['dissolve_retained_rgb_max_delta_255'], 1)
    test.assertLessEqual(report['add_black_mix_max_delta_255'], 1)


class SharedVFXMaterialTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix='t4a-', dir=TMP)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.rgba = material_fixture()
        self.field = distance_field(self.rgba)

    def test_exact_four_band_palette_including_opaque_dark_index(self):
        actual = material_pixels(self.rgba, PALETTE)
        for band in range(4):
            expected = np.rint(np.asarray(PALETTE[band])*255).astype(np.uint8)
            np.testing.assert_array_equal(actual[:, band*16:(band+1)*16],
                                          np.broadcast_to(expected, (64,16,4)))
        self.assertEqual(int(actual[:,:16,3].min()), 255)

    def test_coverage_is_independent_of_luminance_and_palette_alpha(self):
        self.rgba[..., :3] = 0
        self.rgba[..., 3] = np.arange(64, dtype=np.uint8)[:,None]*4
        palette = copy.deepcopy(PALETTE); palette[0][3] = .5
        actual = material_pixels(self.rgba, palette)
        np.testing.assert_array_equal(actual[...,3], np.rint(self.rgba[...,3]*.5))
        # Zero-index coverage includes partial, opaque and transparent pixels.
        self.rgba[...,3] = 255
        self.assertTrue((material_pixels(self.rgba, PALETTE)[...,3] == 255).all())

    def test_erode_zero_half_one_coverage_and_centre_out_order(self):
        removed = []
        for erode in (0, .5, 1):
            actual = material_pixels(self.rgba, PALETTE, self.field, erode=erode)
            removed.append(100*(1-actual[...,3].sum()/self.rgba[...,3].sum()))
        self.assertEqual(removed[0], 0)
        self.assertLessEqual(abs(removed[1]-50), 3)
        self.assertEqual(removed[2], 100)
        half = material_pixels(self.rgba, PALETTE, self.field, erode=.5)
        self.assertEqual(half[32,32,3], 0)
        self.assertEqual(half[0,0,3], 255)
        self.assertTrue(np.all(distance_field(np.zeros_like(self.rgba)) == 255))

    def test_distance_quantiles_respect_partial_coverage(self):
        self.rgba[:32,:,3] = 64
        field = distance_field(self.rgba)
        half = material_pixels(self.rgba, PALETTE, field, erode=.5)
        removed = 100*(1-half[...,3].sum()/self.rgba[...,3].sum())
        self.assertLessEqual(abs(removed-50), 3)

    def test_dissolve_half_removes_brightest_only_and_holds_hue(self):
        original = material_pixels(self.rgba, PALETTE)
        half = material_pixels(self.rgba, PALETTE, dissolve=.5)
        np.testing.assert_array_equal(original[:,:48], half[:,:48])
        self.assertEqual(np.count_nonzero(half[:,48:,3]), 0)
        np.testing.assert_array_equal(original[...,:3], half[...,:3])
        for amount, remaining in ((0,4096), (.49,4096), (.5,3072), (.7,2048), (.9,1024), (1,0)):
            with self.subTest(amount=amount):
                self.assertEqual(np.count_nonzero(material_pixels(self.rgba, PALETTE, dissolve=amount)[...,3]), remaining)

    def test_premultiplied_alpha_is_applied_exactly_once(self):
        self.rgba[...,3] = 128
        straight = material_pixels(self.rgba, PALETTE)
        premult = material_pixels(self.rgba, PALETTE, blend_mode='PREMULT_ALPHA')
        np.testing.assert_allclose(premult[...,:3], np.rint(straight[...,:3].astype(float)*128/255.), atol=1)
        np.testing.assert_array_equal(premult[...,3], straight[...,3])
        self.assertTrue(np.all(material_pixels(self.rgba, PALETTE, dark_duplicate=True)[...,:3] == 0))

    def test_all_six_compatibility_variants_and_material_parameters(self):
        Image.fromarray(self.field).save(self.root/'distance.png')
        for mode in ('MIX', 'ADD', 'PREMULT_ALPHA'):
            for lit in (False, True):
                config = dict(palette=PALETTE, blend_mode=mode, light_participation=lit, erode=.25, dissolve=.5)
                resource = write_vfx_material(self.root, mode+str(lit)+'.tres', config, 'distance.png')
                text = resource.read_text()
                self.assertIn('type="ShaderMaterial"', text)
                self.assertIn('shader_parameter/erode = 0.25', text)
                self.assertIn('shader_parameter/dissolve = 0.5', text)
                self.assertIn('shader_parameter/palette_0 = Color(', text)
                shader = shader_source(mode, lit)
                self.assertEqual('unshaded' in shader, not lit)
                self.assertIn('PREMULTIPLIED = '+str(mode == 'PREMULT_ALPHA').lower(), shader)
                self.assertNotIn('filter_nearest', shader)
                self.assertNotIn('hint_screen_texture', shader)
                self.assertIn('filter_linear', shader)
        self.assertGreater(len(validate_resources(self.root)), 0)

    def test_invalid_material_values_and_nonindex_assets_rejected_before_output(self):
        path, data = definition_fixture(self.root/'source')
        variants = [dict(palette=p) for p in (None, [], [[0,0,0,1]]*3, [[0,0,0]]*4)]
        variants += [dict(palette=PALETTE, **{k:v}) for k, values in {
            'erode':[-.1,1.1,True,float('nan')], 'dissolve':[-.1,1.1,None],
            'blend_mode':['MULTIPLY',None,0], 'light_participation':[1,None,'yes']}.items() for v in values]
        variants += [dict(palette=[[0,0,0,v]]*4) for v in (-.1,1.1,True,float('inf'))]
        for material in variants:
            with self.subTest(material=material), self.assertRaises(ValueError):
                build(dict(data, material=material), self.root/'bad')
            self.assertFalse((self.root/'bad').exists())
        for level in (1,64,128,254):
            Image.new('RGBA', (16,16), (level,level,level,255)).save(path.parent/'frame_0.png')
            with self.assertRaisesRegex(ValueError, '0/85/170/255'): build(path, self.root/'bad')
            self.assertFalse((self.root/'bad').exists())

    def test_distance_fields_complete_confined_and_matching_dimensions(self):
        path, _ = definition_fixture(self.root/'source')
        kit = self.root/'kit'; build(path, kit)
        original = json.loads((kit/'kit.json').read_text())
        for value in ({}, {'flare/flare_00.png':'../source/frame_0.png'}, None):
            (kit/'kit.json').write_text(json.dumps(dict(original, distance_fields=value)))
            with self.assertRaisesRegex(ValueError, 'distance_fields'): load_kit(kit)
        first = next(iter(original['distance_fields'].values()))
        (kit/'kit.json').write_text(json.dumps(original))
        Image.new('L', (1,1)).save(kit/first)
        with self.assertRaisesRegex(ValueError, 'dimensions'): load_kit(kit)

    def test_every_material_sprite_is_linear_and_animation_fields_are_bound(self):
        fixture = picker_fixture(self.root/'fixture')
        project = fixture['project']
        component = (project/'scenes/vfx/g1_projectile.tscn').read_text()
        head = next(n for n in re.split(r'(?=\[node )', component) if 'name="Head"' in n)
        self.assertIn('type="AnimatedSprite2D"', head)
        self.assertIn('texture_filter = 2', head)
        script = (project/'scripts/vfx_g1.gd').read_text()
        self.assertIn('$Head.material = load(config.material)', script)
        self.assertIn('load(config.binding).bind($Head, config.fields)', script)
        keeper = (project/'scripts/keeper.gd').read_text()
        self.assertIn('res://vfx/synthetic_ice/materials/Body.tres', keeper)
        self.assertIn('res://vfx/synthetic_ice/distance/travel/', keeper)
        scene = (project/'scenes/vfx_synthetic_ice_impact.tscn').read_text()
        nodes = re.split(r'(?=\[node )', scene)[1:]
        sprites = [n for n in nodes if any(f'type="{t}"' in n.splitlines()[0] for t in ('Sprite2D','AnimatedSprite2D','CPUParticles2D'))]
        self.assertTrue(sprites)
        for node in sprites:
            self.assertIn('texture_filter = 2', node)
            self.assertRegex(node, r'material = ExtResource\("Material')
        script = (project/'scripts/vfx_synthetic_ice_impact.gd').read_text()
        self.assertIn('_bind_vfx_materials()', script)
        self.assertIn('distance/', script)
        binder = (project/'scripts/vfx_synthetic_ice_material.gd').read_text()
        self.assertIn('frame_changed.connect', binder)
        self.assertIn('animation_changed.connect', binder)
        self.assertIn('node.material.duplicate()', binder)
        dark = (project/'vfx/synthetic_ice/materials/Dark.tres').read_text()
        self.assertIn('shader_parameter/dark_duplicate = true', dark)
        self.assertIn('vfx_material_mix_unlit.gdshader', dark)

    def test_RED_dark_index_rendered_transparent_is_rejected(self):
        report = self._good_report()
        report['index_0_min_alpha_255'] = 0
        with self.assertRaises(AssertionError): assert_render_proof(self, report)

    def test_RED_material_failing_to_load_on_Compatibility_is_rejected(self):
        for key, value in (('shader_loaded',False), ('renderer','forward_plus'), ('rendered_frame_available',False)):
            report = self._good_report(); report[key] = value
            with self.subTest(key=key), self.assertRaises(AssertionError): assert_render_proof(self, report)

    def test_RED_legacy_white_core_keep_validation_names_key(self):
        path, data = definition_fixture(self.root/'source')
        data['material']['white_core_keep'] = .92
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'white_core_keep'): build(path, self.root/'bad')
        self.assertFalse((self.root/'bad').exists())

    def test_render_proof_guard_rejects_wrong_colour_erosion_and_dissolve(self):
        assert_render_proof(self, self._good_report())
        for key, value in (('palette_max_delta_255',2), ('erode_removed_percent',[0,54,100]),
                           ('dissolve_05_removed_per_band',[0,0,1024,1024]),
                           ('dissolve_retained_rgb_max_delta_255',2), ('add_black_mix_max_delta_255',2)):
            report = self._good_report(); report[key] = value
            with self.subTest(key=key), self.assertRaises(AssertionError): assert_render_proof(self, report)

    def test_proof_fixture_resources_and_scene_include_both_blends(self):
        root = self.root/'proof'
        report = material_proof_fixture(root)
        self.assertIsNone(report['passed'])
        self.assertIsNone(report['value']['compatibility_render'])
        self.assertGreater(len((root/'project.godot').read_text().splitlines()), 10)
        self.assertGreater(len(validate_resources(root, True)), 0)
        script = (root/'proof.gd').read_text()
        self.assertIn('sprite(view, material("Dark"), -1)', script)
        self.assertIn('render(material("ADD_unlit"), true)', script)
        self.assertIn('Dark index rendered transparent', script)
        self.assertIn('No rendered frame', script)
        self.assertIn('Compatibility shader compile/uniform check failed', script)
        self.assertEqual(len(list((root/'materials').glob('*.gdshader'))), 6)

    @staticmethod
    def _good_report():
        return {'renderer':'gl_compatibility', 'shader_loaded':True, 'rendered_frame_available':True,
                'palette_max_delta_255':0, 'index_0_min_alpha_255':255,
                'erode_removed_percent':[0,50,100], 'dissolve_05_removed_per_band':[0,0,0,1024],
                'dissolve_retained_rgb_max_delta_255':0, 'add_black_mix_max_delta_255':0}


MATERIAL_PROOF_SCRIPT = '''extends SceneTree

var report: Dictionary = {"renderer": "", "shader_loaded": false,
    "rendered_frame_available": false, "errors": []}
var failed: bool = false
var palette: Array = []
var source: Texture2D

func _initialize() -> void:
    _run.call_deferred()

func need(condition: bool, reason: String) -> bool:
    if not condition:
        report.errors.append(reason)
        failed = true
        push_error(reason)
    return condition

func material(name: String) -> ShaderMaterial:
    var loaded: Resource = load("res://materials/" + name + ".tres")
    if not need(loaded is ShaderMaterial, "Compatibility ShaderMaterial did not load: " + name):
        return null
    var result: ShaderMaterial = loaded.duplicate()
    if name == "MIX_unlit" and OS.get_cmdline_user_args().has("--known-bad-compatibility"):
        result.shader = Shader.new()
        result.shader.code = "shader_type canvas_item; void fragment() { COLOR = missing_symbol; }"
    if not need(result.shader != null, "Missing shader: " + name):
        return null
    var names: Array = []
    for uniform in result.shader.get_shader_uniform_list():
        names.append(String(uniform.name))
    if not need(names.has("palette_0") and names.has("erode") and names.has("dissolve"),
                "Compatibility shader compile/uniform check failed: " + name):
        return null
    return result

func sprite(view: SubViewport, paint: Material, z: int) -> Sprite2D:
    var node := Sprite2D.new()
    node.texture = source
    node.material = paint
    node.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
    node.position = Vector2(32, 32)
    node.z_index = z
    view.add_child(node)
    return node

func render(paint: ShaderMaterial, composite: bool = false) -> Image:
    var view := SubViewport.new()
    view.size = Vector2i(64, 64)
    view.disable_3d = true
    view.transparent_bg = true
    view.world_2d = World2D.new()
    view.render_target_update_mode = SubViewport.UPDATE_ALWAYS
    root.add_child(view)
    if composite:
        var background := ColorRect.new()
        background.size = Vector2(64, 64)
        background.color = Color(0.1, 0.2, 0.3, 1)
        background.z_index = -2
        view.add_child(background)
        sprite(view, material("Dark"), -1)
    sprite(view, paint, 0)
    # Bounded wait: dummy --headless rendering never emits frame_post_draw.
    for frame in range(8):
        await process_frame
    var image: Image = view.get_texture().get_image()
    view.queue_free()
    if not need(image != null and not image.is_empty(),
                "No rendered frame: a dummy headless renderer is not a Compatibility proof"):
        return null
    image.convert(Image.FORMAT_RGBA8)
    return image

func expected(x: int) -> Color:
    var entry: Array = palette[x / 16]
    return Color(entry[0], entry[1], entry[2], entry[3])

func max_delta(image: Image, width: int = 64) -> float:
    var delta: float = 0
    for y in range(64):
        for x in range(width):
            var a: Color = image.get_pixel(x, y)
            var b: Color = expected(x)
            delta = maxf(delta, maxf(absf(a.r-b.r), maxf(absf(a.g-b.g), absf(a.b-b.b))) * 255)
    return delta

func save_image(image: Image, name: String) -> void:
    var error: Error = image.save_png("res://rendered/" + name + ".png")
    need(error == OK, "Cannot write rendered evidence: " + name)

func finish() -> void:
    var file := FileAccess.open("res://rendered/render_proof.json", FileAccess.WRITE)
    if file != null:
        file.store_string(JSON.stringify(report, "  ") + "\n")
    else:
        failed = true
    print(JSON.stringify(report))
    quit(1 if failed else 0)

func _run() -> void:
    DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://rendered"))
    report.renderer = RenderingServer.get_current_rendering_method()
    report.engine_version = Engine.get_version_info().string
    if not need(report.renderer == "gl_compatibility", "Renderer must be gl_compatibility"):
        finish()
        return
    palette = JSON.parse_string(FileAccess.get_file_as_string("res://palette.json"))
    source = load("res://indices.png")
    var mix: ShaderMaterial = material("MIX_unlit")
    for variant in ["MIX_lit", "ADD_unlit", "ADD_lit", "PREMULT_ALPHA_unlit", "PREMULT_ALPHA_lit", "Dark"]:
        material(variant)
    if failed:
        finish()
        return
    report.shader_loaded = true
    if OS.get_cmdline_user_args().has("--known-bad-dark-index"):
        mix.set_shader_parameter("palette_0", Color(0.05, 0.1, 0.2, 0))
    var baseline: Image = await render(mix)
    if baseline == null:
        finish()
        return
    report.rendered_frame_available = true
    save_image(baseline, "palette")
    report.palette_max_delta_255 = max_delta(baseline)
    var dark_alpha: int = 255
    for y in range(64):
        for x in range(16):
            dark_alpha = mini(dark_alpha, roundi(baseline.get_pixel(x,y).a*255))
    report.index_0_min_alpha_255 = dark_alpha
    need(report.palette_max_delta_255 <= 1.00001, "Ramp colour delta exceeds 1/255")
    need(dark_alpha == 255, "Dark index rendered transparent")
    var removed: Array = []
    for amount in [0.0, 0.5, 1.0]:
        var paint: ShaderMaterial = material("MIX_unlit")
        paint.set_shader_parameter("erode", amount)
        var frame: Image = await render(paint)
        if frame == null:
            finish()
            return
        save_image(frame, "erode_" + str(amount))
        var coverage: float = 0
        for y in range(64):
            for x in range(64):
                coverage += frame.get_pixel(x,y).a
        removed.append(100.0*(1.0-coverage/4096.0))
    report.erode_removed_percent = removed
    need(removed[0] == 0 and absf(removed[1]-50) <= 3 and removed[2] == 100,
         "Erosion coverage must be 0 / 50+-3 / 100 percent")
    var dissolved: ShaderMaterial = material("MIX_unlit")
    dissolved.set_shader_parameter("dissolve", 0.5)
    var half: Image = await render(dissolved)
    if half == null:
        finish()
        return
    save_image(half, "dissolve_05")
    var dropped: Array = [0,0,0,0]
    for y in range(64):
        for x in range(64):
            if half.get_pixel(x,y).a < 0.5:
                dropped[x/16] += 1
    report.dissolve_05_removed_per_band = dropped
    report.dissolve_retained_rgb_max_delta_255 = max_delta(half, 48)
    need(dropped == [0,0,0,1024], "Dissolve 0.5 must remove the brightest band and no other")
    need(report.dissolve_retained_rgb_max_delta_255 <= 1.00001, "Dissolve changed retained hue")
    var composite: Image = await render(material("ADD_unlit"), true)
    if composite == null:
        finish()
        return
    save_image(composite, "add_over_black_mix")
    report.add_black_mix_max_delta_255 = max_delta(composite)
    need(report.add_black_mix_max_delta_255 <= 1.00001, "ADD over black MIX duplicate composite differs")
    report.variants_rendered = []
    for variant in ["MIX_lit", "ADD_lit", "PREMULT_ALPHA_unlit", "PREMULT_ALPHA_lit"]:
        var frame: Image = await render(material(variant))
        if frame == null:
            finish()
            return
        save_image(frame, variant)
        need(max_delta(frame) <= 1.00001, "Variant did not render exact palette: " + variant)
        report.variants_rendered.append(variant)
    finish()
'''


def material_proof_fixture(root):
    """Prepare deterministic CPU quantities and the conductor's Godot project."""
    started = time.monotonic()
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    pixels = material_fixture()
    field = distance_field(pixels)
    Image.fromarray(pixels).save(root/'indices.png')
    Image.fromarray(field).save(root/'distance.png')
    (root/'palette.json').write_text(json.dumps(PALETTE, indent=2)+'\n')
    for mode in ('MIX','ADD','PREMULT_ALPHA'):
        for lit in (False, True):
            label = mode+('_lit' if lit else '_unlit')
            write_vfx_material(root, 'materials/'+label+'.tres',
                               dict(palette=PALETTE, blend_mode=mode, light_participation=lit), 'distance.png')
    write_vfx_material(root, 'materials/Dark.tres', dict(palette=PALETTE), 'distance.png', True)
    (root/'proof.gd').write_text(MATERIAL_PROOF_SCRIPT)
    (root/'proof.tscn').write_text('[gd_scene format=3]\n[node name="T4aProof" type="Node2D"]\n')
    (root/'project.godot').write_text('config_version=5\n[application]\nconfig/name="T4a Compatibility material proof"\nrun/main_scene="res://proof.tscn"\n[display]\nwindow/size/viewport_width=64\nwindow/size/viewport_height=64\n[rendering]\nrenderer/rendering_method="gl_compatibility"\nrenderer/rendering_method.mobile="gl_compatibility"\ntextures/default_filters/use_nearest_mipmap_filter=false\ntextures/canvas_textures/default_texture_filter=2\n')
    baseline = material_pixels(pixels, PALETTE)
    eroded = [material_pixels(pixels, PALETTE, field, erode=value) for value in (0,.5,1)]
    half = material_pixels(pixels, PALETTE, dissolve=.5)
    value = {'instrument':'CPU reference, not rendered acceptance',
             'palette_max_delta_255':int(np.abs(baseline.astype(int)-np.repeat(np.rint(np.asarray(PALETTE)*255).astype(int),16,axis=0)[None,:,:]).max()), 'index_0_min_alpha_255':int(baseline[:,:16,3].min()),
             'erode_removed_percent':[float(100*(1-image[...,3].sum()/pixels[...,3].sum())) for image in eroded],
             'dissolve_05_removed_per_band':[int(np.count_nonzero(half[:,i*16:(i+1)*16,3] == 0)) for i in range(4)],
             'dissolve_retained_rgb_max_delta_255':int(np.abs(half[:,:48,:3].astype(int)-baseline[:,:48,:3]).max()),
             'compatibility_render':None, 'add_black_mix_render':None, 'shader_variants':6}
    report = {'id':'t4a_material_reference', 'subject':'64x64 four-band fixture', 'passed':None,
              'value':value, 'threshold':{'palette_max_delta_255':1, 'index_0_min_alpha_255':255,
                'erode_removed_percent':[0,'50 +/- 3',100], 'dissolve_05_removed_per_band':[0,0,0,1024]},
              'op':'report', 'unit':'mixed', 'evidence':[str(root/'indices.png'),str(root/'proof.gd')],
              'notes':'Conductor must run real Compatibility rendering outside sandbox; CPU metrics do not satisfy rendered-frame acceptance.',
              'wall_s':time.monotonic()-started}
    (root/'cpu_reference.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


class PiecePhaseTests(unittest.TestCase):
    """T4h validation, byte-preserving masks and seeded motion."""
    def setUp(self):
        TMP.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='t4h-pieces-', dir=TMP)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path, self.data = definition_fixture(self.root/'source')
        rgba = np.zeros((16,16,4), dtype=np.uint8)
        rgba[...,3] = 255
        for band in range(4): rgba[:,band*4:band*4+4,:3] = band*85
        Image.fromarray(rgba).save(self.path.parent/'piece.png')
        Image.fromarray(rgba).save(self.path.parent/'peak_index.png')
        self.record = {'schema_version':2, 'canvas':[16,16], 'centre':[7.5,7.5],
            'peak_index':'peak_index.png', 'pieces':[{'id':1,'mask':'piece.png',
            'pivot':[7.5,7.5], 'radial_angle_deg':0, 'radial_distance_px':0,
            'area_px':256,'dominant_band':0}]}
        self.manifest = self.path.parent/'pieces.json'
        self.data['pieces'] = {'source':'pieces.json', 'template':'burst_v1',
            'hold_frames':2,'base_speed_px_s':1400,'residue_s':.6,'residue_fraction':.2,'seed':2026}
        self.out = self.root/'kit'
        self.save()

    def save(self):
        self.path.write_text(json.dumps(self.data))
        self.manifest.write_text(json.dumps(self.record))

    def test_missing_mask_rejected_before_output(self):
        self.record['pieces'][0]['mask'] = 'missing.png';self.save()
        with self.assertRaisesRegex(ValueError, 'Missing PNG'): build(self.path, self.out)
        self.assertFalse(self.out.exists())

    def test_pivot_outside_mask_rejected(self):
        with Image.open(self.path.parent/'piece.png') as image: pixels = np.array(image)
        pixels[8,8,3] = 0
        Image.fromarray(pixels).save(self.path.parent/'piece.png')
        with self.assertRaisesRegex(ValueError, 'pivot outside'): build(self.path, self.out)
        self.assertFalse(self.out.exists())

    def test_residue_and_band_and_hold_ranges_rejected(self):
        for name, value in [('residue_fraction',.149),('residue_fraction',.251),
                            ('residue_s',.29),('hold_frames',3),('seed',True)]:
            previous = self.data['pieces'][name];self.data['pieces'][name] = value;self.save()
            with self.subTest(name=name, value=value), self.assertRaises(ValueError): build(self.path,self.out)
            self.data['pieces'][name] = previous
        self.record['pieces'][0]['dominant_band'] = 4;self.save()
        with self.assertRaisesRegex(ValueError,'dominant_band'): build(self.path,self.out)

    def test_self_contained_mask_bytes_distance_and_runtime_validation(self):
        build(self.path,self.out)
        data = load_kit(self.out)
        self.assertEqual(data['pieces']['source'],'pieces/pieces.json')
        self.assertEqual((self.out/'pieces/piece.png').read_bytes(),(self.path.parent/'piece.png').read_bytes())
        field = data['distance_fields']['pieces/piece.png']
        with Image.open(self.out/field) as image:
            self.assertEqual(image.mode,'L');self.assertEqual(image.size,(16,16))
        (self.out/'pieces/piece.png').unlink()
        with self.assertRaisesRegex(ValueError,'Missing PNG'):load_kit(self.out)

    def test_seeded_factor_deterministic_order_independent_and_bounded(self):
        from export.effect_kit import piece_motion
        forward = {i:piece_motion(2026,i) for i in range(24)}
        reverse = {i:piece_motion(2026,i) for i in reversed(range(24))}
        self.assertEqual(forward,reverse)
        self.assertNotEqual(forward,{i:piece_motion(2027,i) for i in range(24)})
        for sample in forward.values():
            self.assertTrue(.6 <= sample['speed_factor'] <= 1.4)
            self.assertTrue(abs(sample['rotation_deg']) <= 30)
            self.assertTrue(abs(sample['scale_delta']) <= .15)


class PieceStretchPhaseTests(PiecePhaseTests):
    """Run the same rejection tests for v2; v1 fixtures remain untouched."""
    def setUp(self):
        super().setUp()
        self.data['pieces']['template'] = 'burst_v2'
        self.record['pieces'][0]['tip'] = [15,15]
        self.save()

    def test_stretch_seed_bounds_and_whole_body_distance(self):
        from export.effect_kit import piece_stretch, piece_geometry
        a = {i:piece_stretch(2026,i) for i in range(24)}
        self.assertEqual(a,{i:piece_stretch(2026,i) for i in reversed(range(24))})
        self.assertNotEqual(a,{i:piece_stretch(2027,i) for i in range(24)})
        for value in a.values():
            self.assertTrue(2.0 <= value['along'] <= 2.5)
            self.assertTrue(abs(value['rotation_deg']) <= 10)
        geometry = piece_geometry(self.record,self.path.parent)
        self.assertEqual(geometry['pieces'][0]['root'],[7,7])
        self.assertTrue(geometry['pieces'][0]['core'])
        build(self.path,self.out)
        kit = load_kit(self.out)
        self.assertTrue(0 <= kit['pieces']['root_drift'] <= .5)
        self.assertEqual((self.out/kit['distance_fields']['pieces/piece.png']).read_bytes(),
                         (self.out/kit['distance_fields']['pieces/peak_index.png']).read_bytes())



def burst_v2_geometry_diagnostic(kit_root):
    """Inverse-affine bilinear alpha support, no Godot/rendered claim.

    The stationary source-mask layer and early core erosion match emitted v2.
    Full 1024-square scratch support avoids clipping the measured geometry.
    """
    from scipy import ndimage
    from export.effect_kit import load_pieces, piece_geometry, piece_stretch
    kit_root = Path(kit_root)
    kit = load_kit(kit_root)
    config, record, _ = load_pieces(kit['pieces'], kit_root, runtime=True)
    source = kit_root/Path(config['source']).parent
    geometry = piece_geometry(record, source)
    with Image.open(source/record['peak_index']) as image:
        peak = np.asarray(image.convert('RGBA'))
    field = distance_field(peak)/255
    py, px = np.nonzero(peak[...,3])
    extent = int(max(np.ptp(px)+1, np.ptp(py)+1))
    yy, xx = np.indices((1024,1024), dtype=float)
    world = np.stack((xx-512, yy-512)).reshape(2,-1)
    centre = np.asarray(record['centre'])
    masks = []
    for item in geometry['pieces']:
        if not item['animated']: continue
        with Image.open(source/item['mask']) as image:
            masks.append((item, np.asarray(image.convert('RGBA'))[...,3]/255))
    def rotation(angle):
        c, s = math.cos(angle), math.sin(angle)
        return np.array([[c,-s],[s,c]])
    rows = []
    for tick in range(16):
        ease = 1-(1-tick/15)**3
        support = np.zeros((1024,1024),dtype=bool)
        for item, alpha in masks:
            stationary = ndimage.map_coordinates(alpha,[world[1]+centre[1],world[0]+centre[0]],order=1,mode='constant').reshape(support.shape)
            support |= stationary > 0
            sample = piece_stretch(config['seed'], item['id'])
            root = np.asarray(item['root'])
            angle = item['axis_radians']
            if item['core']:
                scale = [1+.25*(1-(1-min(tick/9,1))**3)]*2
                drift = 0
                erode = max(0,(tick-9)/27)
            else:
                scale = [1+(sample['along']-1)*ease, 1-.3*ease]
                drift = config['root_drift']*geometry['core_radius_px']*ease
                erode = 0
            matrix = rotation(angle+math.radians(sample['rotation_deg'])*ease) @ np.diag(scale) @ rotation(-angle)
            position = root-centre+rotation(angle)[:,0]*drift
            source_xy = np.linalg.solve(matrix,world-position[:,None])+root[:,None]
            coordinates = [source_xy[1],source_xy[0]]
            warped = ndimage.map_coordinates(alpha,coordinates,order=1,mode='constant').reshape(support.shape)
            sampled_field = ndimage.map_coordinates(field,coordinates,order=1,mode='constant').reshape(support.shape)
            support |= (warped > 0) & (sampled_field >= erode)
        labels, count = ndimage.label(support,structure=np.ones((3,3)))
        sizes = np.bincount(labels.ravel())[1:]
        y,x = np.nonzero(support)
        rows.append({'expansion_tick':tick,'age_frames':tick+config['hold_frames']+max(1,round(kit['layers'].get('flash',{}).get('duration_s',1/60)*60)),
                     'extent_px':int(max(np.ptp(x)+1,np.ptp(y)+1)),
                     'coverage_px':int(support.sum()),'largest_component_fraction':float(sizes.max()/support.sum())})
    return {'instrument':'CPU inverse-affine bilinear alpha>0 support; not rendered acceptance',
            'source_peak_extent_px':extent, 'core_radius_px':geometry['core_radius_px'],
            'root_drift_max_px':config['root_drift']*geometry['core_radius_px'],
            'extent_ratio_at_expansion_025s':rows[-1]['extent_px']/extent,
            'extent_ratio_at_effect_age_025s':next(r['extent_px']/extent for r in rows if r['age_frames']==15),
            'minimum_largest_component_fraction':min(r['largest_component_fraction'] for r in rows),
            'frames':rows}


class DissolveOrderTests(unittest.TestCase):
    def test_legacy_default_and_explicit_legacy_shader_bytes(self):
        from export.effect_kit import dissolve_thresholds, LEGACY_DISSOLVE_ORDER
        self.assertEqual(dissolve_thresholds(), [1-i/6 for i in range(4)])
        self.assertEqual(shader_source(), shader_source(dissolve_order=LEGACY_DISSOLVE_ORDER))
        self.assertNotIn('dissolve_order', validate_material({'palette':PALETTE}))

    def test_order_must_partition_all_four_bands(self):
        from export.effect_kit import dissolve_thresholds
        for order in [None, [], [[3],[2],[1]], [[3],[2],[1],[0,0]], [[3],[2],[1],[]],
                      [[3],[2],[1],[True]], [[3],[2],[1],[4]], '3210', [[3.0],[2],[1],[0]]]:
            with self.subTest(order=order), self.assertRaisesRegex(ValueError,'dissolve_order'):
                validate_material({'palette':PALETTE,'dissolve_order':order})
        self.assertEqual(dissolve_thresholds([[3],[2],[1,0]]), [1-1/6,1-1/6,1-2/6,.5])

    def test_contour_and_fill_drop_together_without_changing_hue(self):
        pixels = np.array([[[i*85]*3+[255] for i in range(4)]],dtype=np.uint8)
        for value, visible in [(0,4),(.5,3),(1-2/6,2),(.8,2),(1-1/6,0),(1,0)]:
            output = material_pixels(pixels, PALETTE, dissolve=value,dissolve_order=[[3],[2],[1,0]])
            self.assertEqual(np.count_nonzero(output[...,3]),visible)
            self.assertEqual(int(output[0,0,3]),int(output[0,1,3]))
            self.assertTrue(np.array_equal(output[...,:3],material_pixels(pixels,PALETTE)[...,:3]))


class PieceLap2ValidationTests(PieceStretchPhaseTests):
    def test_template_order_validation_and_drift_default(self):
        from export.effect_kit import load_pieces
        config, _, _ = load_pieces(self.data['pieces'],self.path.parent)
        self.assertEqual(config['root_drift'],.5)
        for key,value in [('root_drift',-.01),('root_drift',.501),('root_drift',True),
                          ('dissolve_order',[[3],[2],[1]])]:
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):
                load_pieces(dict(self.data['pieces'],**{key:value}),self.path.parent)
        self.data['pieces']['dissolve_order']=[[3],[2],[1,0]];self.save()
        build(self.path,self.out)
        self.assertEqual(load_kit(self.out)['pieces']['dissolve_order'],[[3],[2],[1,0]])


class PieceLap2GeometryTests(unittest.TestCase):
    def test_delivered_t4e_masks_extent_and_connectivity(self):
        report = burst_v2_geometry_diagnostic(ROOT/'runs/C-5/vfx_kits/v9/fire_burst_e0p_v2')
        self.assertGreaterEqual(report['extent_ratio_at_expansion_025s'],1.8)
        self.assertGreaterEqual(report['extent_ratio_at_effect_age_025s'],1.8)
        self.assertGreaterEqual(report['minimum_largest_component_fraction'],.9)

if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--material-fixture':
        print(json.dumps(material_proof_fixture(sys.argv[2]), indent=2))
    elif len(sys.argv) == 3 and sys.argv[1] == '--fixture':
        print(json.dumps(measure_fixture(sys.argv[2]), indent=2))
    elif len(sys.argv) == 3 and sys.argv[1] == '--ramp-fixture':
        print(json.dumps(measure_ramp_fixture(sys.argv[2]), indent=2))
    elif len(sys.argv) == 3 and sys.argv[1] == '--frozen-orb-ramp':
        print(json.dumps(measure_frozen_orb_ramp(sys.argv[2]), indent=2))
    else:
        unittest.main()


# T4k: CPU sampling instrument. It intentionally does not claim rendered proof.
def burst_v2_stretched_sampling_diagnostic(kit_root):
    """3x radial stretch, inverse original-UV sampling, and a clipped control.

    Coverage is alpha-weighted to compare with the analytic affine Jacobian.
    The bad control imposes the ORIGINAL canvas rectangle in world space;
    this is not asserted to be a rule in the existing shader.
    """
    from scipy.ndimage import map_coordinates
    from export.effect_kit import load_pieces, piece_geometry
    kit_root = Path(kit_root)
    kit = load_kit(kit_root)
    config, record, _ = load_pieces(kit['pieces'], kit_root, runtime=True)
    source = kit_root/Path(config['source']).parent
    geometry = piece_geometry(record, source)
    centre = np.asarray(record['centre'])
    rows = []
    for item in geometry['pieces']:
        if not item['animated']:
            continue
        with Image.open(source/item['mask']) as image:
            alpha = np.asarray(image.convert('RGBA'))[..., 3].astype(float)/255
        angle = item['axis_radians']
        c, s = math.cos(angle), math.sin(angle)
        rotation = np.array([[c,-s],[s,c]])
        matrix = rotation @ np.diag([3.0,.7]) @ rotation.T
        root = np.asarray(item['root'])
        position = root-centre + rotation[:,0]*config['root_drift']*geometry['core_radius_px']
        y,x = np.nonzero(alpha)
        corners = np.array([[x.min()-1,y.min()-1],[x.max()+1,y.min()-1],
                            [x.min()-1,y.max()+1],[x.max()+1,y.max()+1]]).T
        bounds = matrix @ (corners-root[:,None]) + position[:,None]
        low = np.floor(bounds.min(axis=1)).astype(int)-2
        high = np.ceil(bounds.max(axis=1)).astype(int)+2
        yy,xx = np.mgrid[low[1]:high[1]+1,low[0]:high[0]+1]
        world = np.stack([xx,yy]).reshape(2,-1)
        original = np.linalg.solve(matrix,world-position[:,None])+root[:,None]
        sample = map_coordinates(alpha,[original[1],original[0]],order=1,mode='constant')
        visible = sample > 0
        original_uv = (original+.5)/np.asarray(record['canvas'])[:,None]
        boundary_discards = visible & np.any((original_uv<0)|(original_uv>1),axis=0)
        world_source = world+centre[:,None]
        clipped = np.any((world_source<0)|(world_source>=np.asarray(record['canvas'])[:,None]),axis=0)
        analytic = float(alpha.sum()*abs(np.linalg.det(matrix)))
        rows.append({'id':item['id'],'analytic_alpha_coverage_px':analytic,
                     'sampled_alpha_coverage_px':float(sample.sum()),
                     'coverage_ratio':float(sample.sum()/analytic),
                     'original_uv_boundary_discards':int(boundary_discards.sum()),
                     'outside_original_world_canvas_samples':int((visible&clipped).sum()),
                     'known_bad_clipped_ratio':float(sample[~clipped].sum()/analytic)})
    return {'instrument':'CPU inverse-affine bilinear alpha coverage at along=3, across=0.7; not a rendered bake',
            'pieces':rows,'minimum_coverage_ratio':min(r['coverage_ratio'] for r in rows),
            'boundary_discards':sum(r['original_uv_boundary_discards'] for r in rows),
            'minimum_known_bad_clipped_ratio':min(r['known_bad_clipped_ratio'] for r in rows)}


class PieceLap3SamplingTests(unittest.TestCase):
    def test_original_uv_3x_coverage_and_canvas_clip_control(self):
        report = burst_v2_stretched_sampling_diagnostic(ROOT/'runs/C-5/vfx_kits/v9/fire_burst_e0p_v2')
        self.assertGreaterEqual(report['minimum_coverage_ratio'],.95)
        self.assertEqual(report['boundary_discards'],0)
        self.assertLess(report['minimum_known_bad_clipped_ratio'],.95)
        self.assertGreater(sum(r['outside_original_world_canvas_samples'] for r in report['pieces']),0)


# T4l instruments: actual emitted schedule, separate from retired lap-2 checks.
def burn_back_cpu(project):
    from scipy import ndimage
    root = Path(project).resolve()/'vfx/fire_burst_e0p_v2/pieces'
    def asset(name):
        path = root/name
        if path.is_file(): return path.read_bytes()
        import tarfile
        evidence = ROOT/'runs/C-5/t3/T4l'
        with tarfile.open(evidence/'evidence.tar.gz') as archive:
            return archive.extractfile(path.relative_to(evidence).as_posix()).read()
    cfg = json.loads(asset('burst_runtime.json'))
    peak = np.array(Image.open(io.BytesIO(asset('peak_index.png'))).convert('RGBA'))
    field = np.array(Image.open(io.BytesIO(asset('whole_body_distance.png'))))/255
    centre = np.asarray(cfg['centre'])
    py,px = np.nonzero(peak[...,3]); extent = int(max(np.ptp(px)+1,np.ptp(py)+1))
    # A fixed world pixel lattice; enlarged beyond the authored canvas.
    size=1024; yy,xx=np.indices((size,size),dtype=float)
    world=np.stack([xx-size//2,yy-size//2]).reshape(2,-1)
    flight=cfg['flash_frames']+cfg['hold_frames']; erosion=flight+15
    residue=erosion+21; end=residue+cfg['residue_frames']
    masks=[]
    for item in cfg['pieces']:
        if not item['animated']: continue
        pixels=np.array(Image.open(io.BytesIO(asset(item['mask']))).convert('RGBA'))
        # Sample only a bounding rectangle for each transformed sprite.
        y,x=np.nonzero(pixels[...,3]); bounds=np.array([[x.min()-1,y.min()-1],[x.max()+1,y.min()-1],[x.min()-1,y.max()+1],[x.max()+1,y.max()+1]]).T
        masks.append((item,pixels,bounds))
    def rot(a):
        c,s=math.cos(a),math.sin(a);return np.array([[c,-s],[s,c]])
    stationary=[]
    for item,pixels,bounds in masks:
        y,x=np.nonzero(pixels[...,3]); wx=np.rint(x-centre[0]+size//2).astype(int);wy=np.rint(y-centre[1]+size//2).astype(int)
        stationary.append((wy,wx,field[y,x],pixels[y,x,0]//85))
    cache={};rows=[]
    for age in range(cfg['flash_frames'],end+1):
        support=np.zeros((size,size),bool)
        stage='hold' if age<flight else 'expansion' if age<=erosion else 'erosion' if age<residue else 'residue' if age<end else 'zero'
        et=np.clip((age-erosion)/21,0,1); rt=np.clip((age-residue)/cfg['residue_frames'],0,1)
        dissolve=1 if age>=end else .8*rt
        thresholds=np.array([5/6,5/6,2/3,.5])
        if stage=='hold': support[np.rint(py-centre[1]+size//2).astype(int),np.rint(px-centre[0]+size//2).astype(int)]=True
        elif stage!='zero':
            for wy,wx,dist,band in stationary:
                keep=(dist<=1-cfg['residue_erode']*et)&(dissolve<thresholds[band]); support[wy[keep],wx[keep]]=True
            if age<residue:
                tick=min(age-flight,15); ease=1-(1-tick/15)**3
                for item,pixels,bounds in masks:
                    key=(item['id'],tick)
                    if key not in cache:
                        angle=item['axis_radians']; rootp=np.asarray(item['root'])
                        scale=[1+.25*(1-(1-min(tick/9,1))**3)]*2 if item['core'] else [1+(item['along']-1)*ease,1-.15*ease]
                        drift=0 if item['core'] else cfg['root_drift']*cfg['core_radius_px']*ease
                        matrix=rot(angle+math.radians(item['rotation_deg'])*ease)@np.diag(scale)@rot(-angle)
                        position=rootp-centre+rot(angle)[:,0]*drift
                        corners=matrix@(bounds-rootp[:,None])+position[:,None]
                        lo=np.floor(corners.min(axis=1)).astype(int)-2;hi=np.ceil(corners.max(axis=1)).astype(int)+2
                        by,bx=np.mgrid[lo[1]:hi[1]+1,lo[0]:hi[0]+1]
                        original=np.linalg.solve(matrix,np.stack([bx,by]).reshape(2,-1)-position[:,None])+rootp[:,None]
                        coordinates=[original[1],original[0]]
                        alpha=ndimage.map_coordinates(pixels[...,3].astype(float),coordinates,order=1,mode='constant')
                        distance=ndimage.map_coordinates(field,coordinates,order=1,mode='nearest')
                        cache[key]=(by.ravel()+size//2,bx.ravel()+size//2,alpha>0,distance)
                    wy,wx,alpha,distance=cache[key];keep=alpha&(distance<=1-et)
                    support[wy[keep],wx[keep]]=True
        count=int(support.sum());y,x=np.nonzero(support)
        labels,n=ndimage.label(support,np.ones((3,3)));sizes=np.bincount(labels.ravel())[1:]
        rows.append({'age':age,'stage':stage,'coverage_px':count,'extent_px':int(max(np.ptp(x)+1,np.ptp(y)+1)) if count else 0,'centroid_distance_px':float(np.hypot(x.mean()-size//2,y.mean()-size//2)) if count else None,'largest_component_fraction':float(sizes.max()/count) if count else None,'dissolve':float(dissolve),'expanded_erode':float(et),'root_erode':float(cfg['residue_erode']*et)})
    denominator=max(r['coverage_px'] for r in rows if r['stage']=='hold')
    for r in rows:r['hold_peak_fraction']=r['coverage_px']/denominator
    measured=[r for r in rows if r['age']>=erosion and r['coverage_px']]
    return {'instrument':'CPU original-UV bilinear alpha>0 expansion plus nearest stationary support; not rendered acceptance','denominator':'maximum body coverage among hold frames; excludes halo, flash and floor light','hold_peak_coverage_px':denominator,'peak_extent_px':extent,'residue_entry_fraction':next(r['hold_peak_fraction'] for r in rows if r['age']==residue),'minimum_component_from_erosion':min(r['largest_component_fraction'] for r in measured),'max_centroid_peak_extent_fraction_from_erosion':max(r['centroid_distance_px']/extent for r in measured),'extent_ratio_at_age15':next(r['extent_px']/extent for r in rows if r['age']==15),'extent_ratio_at_expansion_end':next(r['extent_px']/extent for r in rows if r['age']==erosion),'rows':rows}


class BurnBackMaterialTests(unittest.TestCase):
    def test_outside_in_tips_before_roots_and_legacy_unchanged(self):
        pixels=np.full((1,255,4),255,np.uint8);field=np.arange(255,dtype=np.uint8)[None,:]
        previous=np.ones(255,bool)
        for erode in np.linspace(0,1,21):
            image=material_pixels(pixels,PALETTE,field,erode=erode,erode_outside_in=True)
            keep=image[0,:,3]>0
            self.assertTrue(np.all(np.diff(keep.astype(int))<=0))
            self.assertTrue(np.all(~keep|previous));previous=keep
        self.assertFalse(previous.any())
        self.assertNotIn('erode_outside_in',shader_source())
        self.assertIn('distance_value > 1.0 - erode',shader_source(erode_outside_in=True))
        for i in range(24):
            from export.effect_kit import piece_stretch
            self.assertTrue(2<=piece_stretch(2026,i)['along']<=2.5)

    def test_real_schedule_compactness_and_hold_denominator(self):
        report=burn_back_cpu(ROOT/'runs/C-5/t3/T4l/project')
        self.assertTrue(.15<=report['residue_entry_fraction']<=.25)
        self.assertGreaterEqual(report['extent_ratio_at_age15'],1.8)
        # R-C5-33: include erosion start and residue entry; embers are exempt.
        erosion_start=max(r['age'] for r in report['rows'] if r['stage']=='expansion')
        residue_entry=next(r['age'] for r in report['rows'] if r['stage']=='residue')
        compact=[r for r in report['rows'] if erosion_start<=r['age']<=residue_entry]
        self.assertEqual([r['age'] for r in compact],list(range(erosion_start,residue_entry+1)))
        self.assertGreaterEqual(min(r['largest_component_fraction'] for r in compact),.9)
        self.assertLessEqual(report['max_centroid_peak_extent_fraction_from_erosion'],.15)


class BurnBackResidueHoldTests(unittest.TestCase):
    def test_literal_fraction_held_for_every_residue_age(self):
        report=burn_back_cpu(ROOT/'runs/C-5/t3/T4l/project')
        residue=[r for r in report['rows'] if r['stage']=='residue']
        self.assertEqual(len(residue),36)
        # R-C5-33: the hold-peak fraction is bounded at entry, then dissolves.
        self.assertGreaterEqual(residue[0]['hold_peak_fraction'],.15)
        self.assertLessEqual(max(r['hold_peak_fraction'] for r in residue),.25)
        release=report['rows'][-1]
        self.assertEqual(release['stage'],'zero')
        self.assertEqual(release['coverage_px'],0)
        tail=residue+[release]
        for previous,current in zip(tail,tail[1:]):
            with self.subTest(age=current['age']):
                self.assertEqual(current['age'],previous['age']+1)
                self.assertLessEqual(current['hold_peak_fraction'],previous['hold_peak_fraction'])

    def test_cpu_replay_agrees_with_actual_headless_uniform_schedule(self):
        project=ROOT/'runs/C-5/t3/T4l/project'
        report=burn_back_cpu(project)
        from test_godot_import import burn_back_trace
        trace={int(r['age_frames']):r for r in burn_back_trace()}
        for row in report['rows']:
            actual=trace[row['age']]
            self.assertEqual(row['stage'],actual['stage'])
            for item in actual['actual_uniforms']:
                paint,root,_,_=item['layers']
                self.assertAlmostEqual(paint['erode'],row['expanded_erode'])
                self.assertAlmostEqual(root['erode'],row['root_erode'])
                self.assertAlmostEqual(root['dissolve'],row['dissolve'])


# T4n: painted-band erosion resistance, CPU evidence (never rendered proof).
def ragged_residue_diagnostic(kit_root):
    from scipy import ndimage
    from export.effect_kit import load_pieces, piece_erode_noise, residue_entry
    kit_root = Path(kit_root)
    data = load_kit(kit_root)
    config, record, _ = load_pieces(data['pieces'], kit_root, runtime=True)
    source = kit_root/Path(config['source']).parent
    peak = np.array(Image.open(source/record['peak_index']).convert('RGBA'))
    field = distance_field(peak)
    rows = []
    for noise in (0.0, piece_erode_noise(data)):
        entry = residue_entry(peak, field, config['residue_fraction'], noise)
        # Union actual active shards; denominator remains the intact hold peak.
        support = np.zeros(peak.shape[:2], bool)
        for piece in record['pieces']:
            if piece['area_px'] < 48:
                continue
            pixels = np.array(Image.open(source/piece['mask']).convert('RGBA'))
            support |= material_pixels(pixels, data['material']['palette'], field,
                erode=entry['residue_erode'], erode_outside_in=True,
                erode_noise=noise)[..., 3] > 0
        padded = np.pad(support, 1)
        axial = (np.count_nonzero(padded[1:, :] != padded[:-1, :]) +
                 np.count_nonzero(padded[:, 1:] != padded[:, :-1]))
        diagonal = (np.count_nonzero(padded[1:, 1:] != padded[:-1, :-1]) +
                    np.count_nonzero(padded[1:, :-1] != padded[:-1, 1:]))
        perimeter = math.pi/8*(axial+diagonal/math.sqrt(2))
        labels, _ = ndimage.label(support, np.ones((3, 3)))
        components = np.bincount(labels.ravel())[1:]
        area = int(support.sum())
        rows.append(dict(erode_noise=noise, **entry, entry_area_px=area,
            entry_fraction=area/entry['source_peak_area_px'], perimeter_px=perimeter,
            isoperimetric_excess=perimeter**2/(4*math.pi*area)-1,
            largest_component_fraction=float(components.max()/area)))
    return dict(instrument='CPU active T4e-r1 shard union at residue entry; no dissolve',
                perimeter='four-direction Crofton transition count, exterior zero padding',
                connectivity=8, zero_control=rows[0], configured=rows[1])


class RaggedResidueMaterialTests(unittest.TestCase):
    def test_t4e_entry_ragged_connected_and_zero_disc_control(self):
        report = ragged_residue_diagnostic(ROOT/'runs/C-5/vfx_kits/v9/fire_burst_e0p_v2')
        actual, control = report['configured'], report['zero_control']
        self.assertEqual(actual['erode_noise'], .08)
        self.assertGreaterEqual(actual['isoperimetric_excess'], .12)
        self.assertLess(abs(control['isoperimetric_excess']), .03)
        for row in (actual, control):
            self.assertGreaterEqual(row['largest_component_fraction'], .9)
            self.assertTrue(.15 <= row['entry_fraction'] <= .25)
            self.assertEqual(row['entry_area_px'], row['predicted_stationary_residue_area_px'])

    def test_noise_bounds_band_resistance_endpoints_and_dissolve(self):
        from export.effect_kit import erosion_distance
        for value in (-.01, 1.01, True, float('nan'), '0.08'):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'erode_noise'):
                validate_material(dict(palette=PALETTE, erode_noise=value))
        pixels = np.array([[[b*85]*3+[255] for b in range(4)]], np.uint8)
        field = np.full((1, 4), 128, np.uint8)
        self.assertTrue(np.all(np.diff(erosion_distance(pixels, field, .08)[0]) < 0))
        for noise in (0, .08, 1):
            args = dict(erode_outside_in=True, erode_noise=noise, dissolve_order=[[3],[2],[1,0]])
            self.assertTrue(np.all(material_pixels(pixels, PALETTE, field, **args)[...,3] == 255))
            self.assertFalse(material_pixels(pixels, PALETTE, field, erode=1, **args)[...,3].any())
            for dissolve, expected in ((0,[1,1,1,1]),(.5,[1,1,1,0]),(.7,[1,1,0,0]),(.9,[0,0,0,0]),(1,[0,0,0,0])):
                actual = material_pixels(pixels, PALETTE, field, dissolve=dissolve, **args)[0,:,3] > 0
                np.testing.assert_array_equal(actual, expected)
        self.assertNotIn('erode_noise', shader_source())
        self.assertNotIn('erode_noise', shader_source(erode_outside_in=True))
        self.assertIn('distance_value -= erode_noise * (band / 3.0)',
                      shader_source(erode_outside_in=True, erode_noise=.08))

    def test_kit_piece_material_scope_validation_and_precedence(self):
        from export.effect_kit import piece_erode_noise, _validate, load_pieces
        fixture = PieceStretchPhaseTests(); fixture.setUp(); self.addCleanup(fixture.doCleanups)
        for scope in ('kit', 'pieces', 'material'):
            for value in (-.01, 1.01, True, float('inf')):
                data = copy.deepcopy(fixture.data)
                owner = data if scope == 'kit' else data[scope]
                owner['erode_noise'] = value
                with self.subTest(scope=scope, value=value), self.assertRaisesRegex(ValueError, 'erode_noise'):
                    _validate(data, fixture.path.parent)
        data = copy.deepcopy(fixture.data)
        self.assertEqual(piece_erode_noise(data), 0)
        data['material']['erode_noise'] = .02
        self.assertEqual(piece_erode_noise(data), .02)
        data['erode_noise'] = .04
        self.assertEqual(piece_erode_noise(data), .04)
        data['pieces']['erode_noise'] = .08
        self.assertEqual(piece_erode_noise(data), .08)
        fixture.data = data; fixture.save(); build(fixture.path, fixture.out)
        self.assertEqual(piece_erode_noise(load_kit(fixture.out)), .08)
        data['pieces']['erode_noise'] = 0
        self.assertEqual(piece_erode_noise(data), 0)
        data['pieces']['template'] = 'burst_v1'
        self.assertEqual(piece_erode_noise(data), 0)
