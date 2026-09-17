"""T3o picker, living-embers, legacy byte lock and headless contracts.

Persistent synthetic fixture: PYTHONPATH=.:tests python3 -B
    tests/test_vfx_picker.py --fixture runs/C-3/t3/T3o/fixture
Relative kit directories resolve beside kits.json. Glow sort_y specifies the
owning prop anchor y, before the required +1 px. Particle rect remains xyxy.
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

from PIL import Image
from export.godot_import import (build_project, _load_vfx_kits, validate_resources,
                                 RADIAL_RESOURCES)
from export.props_layer import load_props, write_layers, _glow_sort_y
from test_props_layer import make_props, make_inputs, text_hashes

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT/'runs/C-3/t3/T3o'
TMP = ROOT/'tests/tmp'
GODOT = '/Applications/Godot.app/Contents/MacOS/Godot'
LEGACY_ORDER = ('instances', 'particles', 'assets', 'shadows', 'overhead', 'near')


def fixture_inputs(root):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    cells = root/'cells'
    cells.mkdir()
    for i in range(4):
        Image.new('RGBA', (512, 512), (40, 80, 120, 255)).save(cells/f'cast_S_{i}.png')
    sockets = root/'sockets.json'
    sockets.write_text(json.dumps({'version': 1, 'canvas': [512, 512], 'cells': {
        'cast_S': {'sockets': [[270, 240], [271, 238], [272, 236], [273, 238]],
                   'release_index': 2}}}, indent=2)+'\n')
    entries = []
    for name, count in (('zeta', 2), ('alpha', 3)):
        kit = root/name
        for kind in ('flare', 'impact'):
            (kit/kind).mkdir(parents=True)
            for i in range(count):
                Image.new('RGBA', (8, 8), (20+i, 80, 150, 180)).save(kit/kind/f'{kind}_{i}.png')
        (kit/'CREDITS.txt').write_text('Synthetic '+name+' kit.\n')
        entries.append({'name': name, 'dir': name})
    entries[1]['tint'] = [1, .2, .05]
    kits = root/'kits.json'
    kits.write_text(json.dumps({'kits': entries}, indent=2)+'\n')
    props = root/'props'
    props.mkdir()
    Image.new('RGBA', (32, 64), (60, 90, 120, 255)).save(props/'prop.png')
    Image.new('RGBA', (16, 16), (240, 140, 60, 100)).save(props/'glow.png')
    data = {key: [] for key in LEGACY_ORDER}
    data['assets'] = [{'name': 'brazier', 'file': 'prop.png', 'anchor': [16, 64],
                       'footprint': {'w': 20, 'h': 12}, 'collide': False, 'fade_when_behind': False}]
    data['instances'] = [{'asset': 'brazier', 'position': [100, 200]}]
    data['glows'] = [
        {'texture': 'glow.png', 'position': [100, 154], 'scale': 2,
         'color': [1, .5, .1, .5], 'flicker_hz': 4, 'flicker_amount': .6,
         'z_parent': 'actors', 'sort_y': 200},
        {'texture': 'glow.png', 'position': [130, 120], 'scale': .5,
         'color': [.4, .7, 1, .4], 'flicker_hz': 6, 'flicker_amount': .3,
         'z_parent': 'overhead'}]
    data['particles'] = [{'name': 'embers', 'texture': 'glow.png', 'rect': [90, 140, 110, 160],
        'amount': 12, 'lifetime_s': 1.5, 'velocity_px_s': [10, 30], 'direction': [0, -1],
        'spread_deg': 15, 'scale': [.1, .2], 'color_start': [1, .7, .2, .8],
        'color_end': [1, .2, .05, 0], 'gravity': [3, -24],
        'angular_velocity': [-30, 50], 'scale_curve': [1, 0], 'additive': True}]
    (props/'props.json').write_text(json.dumps(data, indent=2)+'\n')
    return cells, sockets, kits, props


def add_glow_scene(project, props):
    """Isolate the actual props writer in a tiny scene; no parallax dependency."""
    fragments = write_layers(project, load_props(props))
    ext, sub = fragments['external'], fragments['subresources']
    scene = (f'[gd_scene load_steps={len(ext)+len(sub)+1} format=3]\n\n'+
             '\n'.join(ext)+'\n\n'+'\n'.join(sub)+
             '\n[node name="Glows" type="Node2D"]\n'+fragments['before_keeper']+
             fragments['after_keeper'])
    (project/'scenes/glows.tscn').write_text(scene)
    return scene


def build_fixture(directory):
    root = Path(directory)
    cells, sockets, kits, props = fixture_inputs(root/'inputs')
    project = root/'project'
    report = build_project(cells, project, vfx_kits=kits, sockets=sockets)
    add_glow_scene(project, props)
    (project/'picker_probe.gd').write_text(PICKER_PROBE)
    (project/'glow_probe.gd').write_text(GLOW_PROBE)
    report['all_resource_references'] = len(validate_resources(project, True))
    (root/'export_report.json').write_text(json.dumps(report, indent=2)+'\n')
    return project, report


def run_headless(test, project, script):
    engine_errors = []
    for args in (['--import'], ['--script', 'res://'+script]):
        started = time.monotonic()
        result = subprocess.run([GODOT, '--headless', '--log-file', str(project/'godot.log'),
                                 '--path', str(project), *args],
                                capture_output=True, text=True, timeout=60)
        log = result.stdout+result.stderr
        test.assertLess(time.monotonic()-started, 60, 'headless deadline')
        test.assertEqual(result.returncode, 0, log)
        test.assertNotIn('SCRIPT ERROR', log)
        test.assertNotIn('T3O_ASSERTION:', log)
        engine_errors.extend(line for line in log.splitlines() if 'ERROR' in line)
    test.assertIn('T3O_RUNTIME_ASSERTIONS=complete', log)
    print(log)
    test.assertEqual(engine_errors, [], '\n'.join(engine_errors))
    return log


class VfxPickerTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix='picker-', dir=TMP)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.cells, self.sockets, self.kits, self.props = fixture_inputs(self.root/'inputs')
        self.data = json.loads(self.kits.read_text())

    def export(self, **options):
        out = self.root/'project'
        report = build_project(self.cells, out, sockets=self.sockets, vfx_kits=self.kits, **options)
        return out, report

    def reject_catalogue(self, data):
        self.kits.write_text(json.dumps(data))
        out = self.root/'invalid'
        with self.assertRaises(ValueError):
            build_project(self.cells, out, vfx_kits=self.kits, sockets=self.sockets)
        self.assertFalse(out.exists())

    def test_every_kit_resources_scenes_counts_order_tab_label_and_credits(self):
        out, report = self.export()
        refs = validate_resources(out, True)
        self.assertTrue(refs)
        for entry, count in zip(self.data['kits'], (2, 3)):
            name = entry['name']
            for kind in ('flare', 'impact'):
                resource = out/f'vfx/{name}/{kind}.tres'
                self.assertTrue(resource.is_file())
                self.assertEqual(resource.read_text().count('"duration":'), count)
                self.assertIn('"loop": false', resource.read_text())
                self.assertIn('"speed": 20.0', resource.read_text())
                for source in (self.kits.parent/name/kind).glob('*.png'):
                    self.assertEqual(source.read_bytes(), (out/f'vfx/{name}/sprites/{kind}'/source.name).read_bytes())
            self.assertTrue((out/f'scenes/vfx_{name}_impact.tscn').is_file())
            self.assertFalse((out/f'scripts/vfx_{name}_bolt.gd').exists())
            self.assertFalse((out/f'scenes/vfx_{name}_bolt.tscn').exists())
        self.assertTrue((out/'scenes/vfx/g1_projectile.tscn').is_file())
        bolt = (out/'scripts/vfx_g1.gd').read_text()
        for token in ('CapsuleShape2D.new()', 'space.cast_motion(query)', '"release"', '"contact"', '"expire"', '"cancel"'):
            self.assertIn(token, bolt)
        settings = (out/'project.godot').read_text()
        self.assertIn('vfx_cycle={"deadzone":0.2,"events":[Object(InputEventKey,"physical_keycode":4194306)]}', settings)
        keeper = (out/'scripts/keeper.gd').read_text()
        entries = json.loads(re.search(r'^const VFX_KITS = (.+)$', keeper, re.M)[1])
        self.assertEqual([e['name'] for e in entries], ['zeta', 'alpha'])
        for token in ('hud.layer = 10', 'Vector2(16, 16)', '"font_size", 22',
                      '"font_color", Color.WHITE', '"font_outline_color"',
                      '"VFX: " + VFX_KITS[vfx_kit_index]["name"] + "  (Tab)"',
                      'load(VFX_KITS[cast_kit_index]["flare"])',
                      'G1.acquire(get_parent(), kit, socket, destination, self, art_scale)'):
            self.assertIn(token, keeper)
        self.assertLess(keeper.index('cast_kit_index = vfx_kit_index'), keeper.index('        state = "cast"'))
        self.assertLess(keeper.index('is_action_just_pressed("vfx_cycle")'), keeper.index('if state == "jump" or state == "cast":'))
        expected = 'Synthetic zeta kit.\nSynthetic alpha kit.\n'
        self.assertEqual((out/'CREDITS_VFX.txt').read_text(), expected)
        self.assertEqual(report['vfx_kits']['credits'], expected)
        self.assertEqual([k['frames'] for k in report['vfx_kits']['kits']],
                         [{'flare': 2, 'impact': 2}, {'flare': 3, 'impact': 3}])

    def test_tint_changes_every_travel_rgb_stop_default_is_exact(self):
        out, _ = self.export()
        keeper = (out/'scripts/keeper.gd').read_text()
        entries = json.loads(re.search(r'^const VFX_KITS = (.+)$', keeper, re.M)[1])
        self.assertEqual(entries[0]['trail_color'], [.35, .65, .8, .6])
        self.assertEqual(entries[1]['trail_color'], [1, .2, .05, .6])
        self.assertEqual(entries[0]['bolt'], entries[1]['bolt'])

    def test_duplicate_missing_invalid_and_thirteen_kits_before_output(self):
        bads = []
        data = copy.deepcopy(self.data);data['kits'][1]['name'] = 'zeta';bads.append(data)
        data = copy.deepcopy(self.data);data['kits'][1]['dir'] = 'missing';bads.append(data)
        data = copy.deepcopy(self.data);data['kits'][1]['dir'] = 'props';bads.append(data)
        data = {'kits': [{'name': f'kit_{i}', 'dir': 'zeta'} for i in range(13)]};bads.append(data)
        for i, bad in enumerate(bads):
            with self.subTest(case=i): self.reject_catalogue(bad)
        self.kits.write_text(json.dumps(self.data))
        (self.kits.parent/'alpha/impact/impact_1.png').unlink()
        self.reject_catalogue(self.data)

    def test_catalogue_unknown_keys_shapes_identifiers_tints_and_empty_rejected(self):
        for bad in ({}, {'kits': []}, {'kits': {}}, [], {'kits': self.data['kits'], 'extra': 0}):
            with self.subTest(document=bad): self.reject_catalogue(bad)
        for key, values in {
            'name': ['', '../x', 'has space', 'a-b', '9bad', 'ZETA', True, None],
            'dir': ['', None, True],
            'tint': [None, [0, 1], [0, 1, 2], [True, 0, 0], [float('nan'), 0, 0], [0, -1, 0]]
        }.items():
            for value in values:
                data = copy.deepcopy(self.data);data['kits'][1][key] = value
                with self.subTest(key=key, value=value): self.reject_catalogue(data)
        for change in ('unknown', 'missing'):
            data = copy.deepcopy(self.data)
            if change == 'unknown': data['kits'][0]['extra'] = 1
            else: del data['kits'][0]['dir']
            self.reject_catalogue(data)

    def test_one_and_twelve_kits_and_relative_path_resolution(self):
        for count in (1, 12):
            self.kits.write_text(json.dumps({'kits': [{'name': f'kit_{i}', 'dir': 'zeta'} for i in range(count)]}))
            self.assertEqual(len(_load_vfx_kits(self.kits)), count)
        self.kits.write_text(json.dumps(self.data))
        self.assertEqual(_load_vfx_kits(self.kits)[0]['root'], self.kits.parent/'zeta')

    def test_conflicting_options_missing_sockets_and_overlapping_kit_before_output(self):
        out = self.root/'invalid'
        for kwargs in ({'vfx_kit': self.kits.parent/'zeta', 'sockets': self.sockets},
                       {'vfx': self.kits.parent/'zeta', 'sockets': self.sockets}, {}):
            with self.subTest(options=kwargs), self.assertRaises(ValueError):
                build_project(self.cells, out, vfx_kits=self.kits, **kwargs)
            self.assertFalse(out.exists())
        out = self.kits.parent/'zeta/project'
        with self.assertRaises(ValueError):
            build_project(self.cells, out, vfx_kits=self.kits, sockets=self.sockets)
        self.assertFalse(out.exists())
        bad = json.loads(self.sockets.read_text());bad['cells']['cast_S']['sockets'].pop()
        self.sockets.write_text(json.dumps(bad))
        with self.assertRaises(ValueError): self.export()
        self.assertFalse((self.root/'project').exists())

    def test_cli_mutual_exclusion_requires_sockets_and_success(self):
        out = self.root/'cli'
        command = [sys.executable, '-B', '-m', 'export.godot_import', '--cells', str(self.cells),
                   '--out', str(out), '--vfx-kits', str(self.kits)]
        for extra in (['--vfx-kit', str(self.kits.parent/'zeta')], []):
            result = subprocess.run(command+extra, cwd=ROOT, capture_output=True, text=True, timeout=30)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(out.exists())
        result = subprocess.run(command+['--sockets', str(self.sockets)], cwd=ROOT,
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)['vfx_kits']['kits']), 2)

    def test_single_kit_and_legacy_props_all_text_byte_identical_to_t3m(self):
        legacy = self.root/'legacy';legacy.mkdir()
        source, cells, kit, sockets = make_inputs(legacy, (1200, 900))
        props = legacy/'props';make_props(props)
        out = self.root/'legacy_project'
        # Legacy COLLECTIONS is a set. Fix only its iteration order to the
        # captured process order so hash randomisation cannot mask byte drift.
        with patch('time.monotonic', return_value=0.0), patch('export.props_layer.COLLECTIONS', LEGACY_ORDER):
            build_project(cells, out, parallax=source, props=props, vfx_kit=kit, sockets=sockets)
        baseline = json.loads((ROOT/'fixtures/fl1b/VfxPickerTests-4.json').read_text())
        self.assertEqual(text_hashes(out), baseline)
        self.assertEqual(len(baseline), 18)

    def test_real_six_kit_catalogue_validation(self):
        kits = _load_vfx_kits(ROOT/'runs/C-3/vfx_kits/kits.json')
        self.assertEqual([k['name'] for k in kits], ['frost', 'fire', 'lightning', 'arcane', 'holy', 'poison'])
        self.assertTrue(all(k['flare'] and k['impact'] and k['credits'] for k in kits))

    @unittest.skipUnless(Path(GODOT).is_file(), 'Godot binary unavailable')
    def test_headless_tab_twice_cast_scene_labels_and_inflight_kit_lock(self):
        out, _ = self.export()
        (out/'picker_probe.gd').write_text(PICKER_PROBE)
        run_headless(self, out, 'picker_probe.gd')


class LivingEmbersTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix='embers-', dir=TMP)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.cells, self.sockets, self.kits, self.props = fixture_inputs(self.root/'inputs')
        self.data = json.loads((self.props/'props.json').read_text())

    def export(self):
        out = self.root/'project'
        build_project(self.cells, out)
        return out, add_glow_scene(out, self.props)

    def reject(self, data):
        (self.props/'props.json').write_text(json.dumps(data))
        out = self.root/'invalid'
        # Real build_project ordering validates props before reading parallax
        # or creating output, even when the latter path is deliberately absent.
        with self.assertRaises(ValueError):
            build_project(self.cells, out, props=self.props, parallax=self.root/'absent')
        self.assertFalse(out.exists())
        with self.assertRaises(ValueError): load_props(self.props)

    def test_two_glows_additive_script_position_scale_color_sort_and_particles(self):
        out, text = self.export()
        nodes = dict(re.findall(r'\[node name="([^"]+)"[^\n]*\]\n([^\[]*)', text))
        self.assertEqual(len([n for n in nodes if n.startswith('Glow_')]), 2)
        self.assertIn('[node name="Glow_0" type="Sprite2D" parent="Actors"]', text)
        self.assertIn('[node name="Glow_1" type="Sprite2D" parent="Overhead"]', text)
        for name in ('Glow_0', 'Glow_1'):
            self.assertIn('material = SubResource("PropsAdditive")', nodes[name])
            self.assertIn('script = ExtResource("GlowFlicker")', nodes[name])
            self.assertIn('centered = true', nodes[name])
        self.assertIn('position = Vector2(100, 201)', nodes['Glow_0'])
        self.assertIn('offset = Vector2(0, -23.5)', nodes['Glow_0'])
        self.assertIn('scale = Vector2(2, 2)', nodes['Glow_0'])
        self.assertIn('modulate = Color(1, 0.5, 0.1, 0.5)', nodes['Glow_0'])
        self.assertIn('position = Vector2(130, 120)', nodes['Glow_1'])
        self.assertIn('offset = Vector2(0, 0)', nodes['Glow_1'])
        particle = nodes['Particles_embers']
        for token in ('gravity = Vector2(3, -24)', 'angular_velocity_min = -30',
                      'angular_velocity_max = 50', 'scale_amount_curve = SubResource("PropsScale0")',
                      'material = SubResource("PropsAdditive")', 'local_coords = false',
                      'position = Vector2(100, 150)', 'emission_rect_extents = Vector2(10, 10)'):
            self.assertIn(token, particle)
        self.assertIn('blend_mode = 1', text)
        self.assertTrue((out/'scripts/glow_flicker.gd').is_file())
        validate_resources(out, True)
        self.assertEqual((out/'props/glow.png').read_bytes(), (self.props/'glow.png').read_bytes())

    def test_owner_sort_inference_override_ties_and_standalone(self):
        props = load_props(self.props)
        glow = copy.deepcopy(props['glows'][0]);glow.pop('sort_y')
        self.assertEqual(_glow_sort_y(glow, props), 201)
        glow['sort_y'] = 333.5
        self.assertEqual(_glow_sort_y(glow, props), 334.5)
        glow.pop('sort_y');glow['position'] = [900, 900]
        self.assertEqual(_glow_sort_y(glow, props), 201)
        props['instances'] = []
        self.assertEqual(_glow_sort_y(glow, props), 901)

    def test_invalid_glow_hz_amount_parent_before_output(self):
        for key, value in (('flicker_hz', 0), ('flicker_amount', 1.0), ('z_parent', 'air')):
            data = copy.deepcopy(self.data);data['glows'][0][key] = value
            with self.subTest(key=key): self.reject(data)

    def test_glow_unknown_missing_numeric_texture_and_type_validation(self):
        for key, values in {'scale': [0, -1, True, float('inf')],
                            'position': [[1], [0, float('nan')]],
                            'color': [[0, 0, 0], [1, 2, 0, 0], [1, True, 0, 0]],
                            'flicker_hz': [.49, 20.01, True, float('nan')],
                            'flicker_amount': [-.1, .91, True, float('inf')],
                            'sort_y': [True, float('nan'), []],
                            'texture': ['missing.png', '../escape.png'],
                            'z_parent': [None, [], 1]}.items():
            for value in values:
                data = copy.deepcopy(self.data);data['glows'][0][key] = value
                with self.subTest(key=key, value=value): self.reject(data)
        for mode in ('unknown', 'missing', 'not_list'):
            data = copy.deepcopy(self.data)
            if mode == 'unknown': data['glows'][0]['oops'] = 1
            elif mode == 'missing': del data['glows'][0]['color']
            else: data['glows'] = {}
            self.reject(data)

    def test_particle_optional_invalid_shapes_ranges_booleans_unknown(self):
        for key, values in {'gravity': [[0], [0, float('nan')], [True, 0]],
                            'angular_velocity': [[2, 1], [0], [0, float('inf')]],
                            'scale_curve': [[0], [-1, 0], [0, float('nan')]],
                            'additive': [1, 'true', None], 'unknown': [0]}.items():
            for value in values:
                data = copy.deepcopy(self.data);data['particles'][0][key] = value
                with self.subTest(key=key, value=value): self.reject(data)

    def test_glow_boundary_values_and_particle_curve_growth_zero_endpoints(self):
        for hz, amount in ((.5, 0), (20, .9)):
            data = copy.deepcopy(self.data)
            data['glows'][0].update(flicker_hz=hz, flicker_amount=amount)
            data['particles'][0].update(scale_curve=[0, 2], angular_velocity=[-4, -4], additive=False)
            (self.props/'props.json').write_text(json.dumps(data))
            load_props(self.props)
        out, text = self.export()
        self.assertIn('max_value = 2', text)
        self.assertIn('Vector2(0, 0), 0.0, 2.0, 0, 0, Vector2(1, 2), 2.0, 0.0', text)
        particle = text.split('[node name="Particles_embers"')[1]
        self.assertNotIn('material =', particle)

    def test_no_glows_or_new_keys_preserves_all_legacy_layer_text(self):
        # Compare omission with explicit neutral particle options. All legacy
        # scene fragments must be unchanged when keys are absent; the full
        # pre-edit hash lock above covers exported T3m text, including props.
        data = copy.deepcopy(self.data);del data['glows']
        for key in ('gravity', 'angular_velocity', 'scale_curve', 'additive'):
            del data['particles'][0][key]
        (self.props/'props.json').write_text(json.dumps(data))
        out, text = self.export()
        self.assertNotIn('GlowFlicker', text)
        self.assertNotIn('PropsAdditive', text)
        self.assertNotIn('PropsScale', text)
        self.assertIn('gravity = Vector2(0, 0)', text)
        self.assertFalse((out/'scripts/glow_flicker.gd').exists())

    def test_three_sine_normalisation_numerical_envelope_and_extrema(self):
        # Independent reference for the fixed 4 Hz fixture; engine probe also
        # measures the real script with its per-instance Godot RNG phases.
        phases = [.2, 1.3, 2.4]
        samples = [.5*(1+.6*sum(math.sin(2*math.pi*4*t*k+p)
                   for k, p in zip((1, 1.73, 2.61), phases))/3) for t in [i/60 for i in range(60)]]
        extrema = sum((b-a)*(c-b) < 0 for a, b, c in zip(samples, samples[1:], samples[2:]))
        self.assertGreaterEqual(extrema, 6)
        self.assertGreaterEqual(max(samples)-min(samples), .5*.6*.5)
        self.assertTrue(all(.5*(1-.6) <= a <= .5*(1+.6) for a in samples))

    @unittest.skipUnless(Path(GODOT).is_file(), 'Godot binary unavailable')
    def test_headless_glow_sixty_samples_extrema_range_and_particle_properties(self):
        out, _ = self.export()
        (out/'glow_probe.gd').write_text(GLOW_PROBE)
        run_headless(self, out, 'glow_probe.gd')


class AuthoredEffectPickerTests(unittest.TestCase):
    """T3t extension: mixed catalogue, legacy byte lock and real engine probe."""
    def setUp(self):
        from test_effect_kit import picker_fixture
        temporary = ROOT/'tests/tmp'
        temporary.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix='authored-picker-', dir=temporary)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.fixture = picker_fixture(self.root/'fixture', ROOT/'runs/C-3/vfx_kits/frost')
        self.project = self.fixture['project']

    def test_mixed_catalogue_legacy_scenes_and_scripts_byte_identical(self):
        from export.godot_import import BOLT_SCRIPT, IMPACT_SCRIPT
        catalogue = self.root/'legacy.json'
        catalogue.write_text(json.dumps({'kits': [{'name': 'frost', 'dir': str(self.fixture['legacy'])}]}))
        legacy = self.root/'legacy-project'
        build_project(self.fixture['cells'], legacy, sockets=self.fixture['sockets'], vfx_kits=catalogue)
        for relative in ('scenes/vfx_frost_impact.tscn', 'scripts/vfx_frost_impact.gd',
                         'vfx/frost/flare.tres', 'vfx/frost/impact.tres',
                         'scenes/vfx/g1_projectile.tscn', 'scripts/vfx_g1.gd'):
            self.assertEqual((legacy/relative).read_bytes(), (self.project/relative).read_bytes(), relative)
        self.assertFalse((self.project/'scripts/vfx_frost_bolt.gd').exists())
        self.assertEqual((self.project/'scripts/vfx_frost_impact.gd').read_text(), IMPACT_SCRIPT)

    def test_authored_kit_own_travel_durations_layers_and_feedback_parameters(self):
        project = self.project
        metadata = json.loads((self.fixture['kit']/'kit.json').read_text())
        self.assertNotIn('tint', metadata)
        self.assertEqual(len(metadata['material']['palette']), 4)
        self.assertTrue(all(len(c) == 4 for c in metadata['material']['palette']))
        for kind in ('impact',):
            scene = (project/f'scenes/vfx_synthetic_ice_{kind}.tscn').read_text()
            for name in ('DarkDuplicate', 'Glow', 'FloorLight', 'Flash', 'Decal', 'Particles'):
                self.assertIn(f'[node name="{name}"', scene)
            for token in ('materials/Additive.tres', 'materials/Body.tres', 'hitstop_duration = 0.08',
                          'hitstop_time_scale = 0.1', 'shake_distance = 3', 'shake_duration = 0.12',
                          'ground_squash = 0.6', 'texture_filter = 2'):
                self.assertIn(token, scene)
            script = (project/f'scripts/vfx_synthetic_ice_{kind}.gd').read_text()
            for token in ('Engine.time_scale = hitstop_time_scale', 'camera.offset = baseline',
                          '"modulate:a", 0.0, FLOOR_DURATION', '"scale", Vector2.ONE * FLASH_TO',
                          '"modulate:a", 0.0, DECAL_DURATION', 'set_ignore_time_scale(true)'):
                self.assertIn(token, script)
        keeper = (project/'scripts/keeper.gd').read_text()
        entries = json.loads(re.search(r'^const VFX_KITS = (.+)$', keeper, re.M)[1])
        self.assertEqual(entries[0]['head'], 'res://vfx/synthetic_ice/travel.tres')
        self.assertEqual(entries[0]['speed_px_s'], 360)
        self.assertIn('type="Line2D"', (project/'scenes/vfx/g1_projectile.tscn').read_text())
        for phase in ('flare', 'travel', 'impact', 'residual'):
            text = (project/f'vfx/synthetic_ice/{phase}.tres').read_text()
            durations = [float(v) for v in re.findall(r'"duration": ([0-9.e+-]+)', text)]
            self.assertEqual(durations, [2/60,5/60])
            for source in (self.fixture['kit']/phase).glob('*.png'):
                self.assertEqual(source.read_bytes(), (project/f'vfx/synthetic_ice/sprites/{phase}'/source.name).read_bytes())
        self.assertGreater(len(validate_resources(project, True)), 0)
        self.assertIn('[node name="Residual"', (project/'scenes/vfx_synthetic_ice_impact.tscn').read_text())

    def test_corrupt_authored_metadata_rejected_before_project_output(self):
        kit = self.fixture['kit']
        data = json.loads((kit/'kit.json').read_text())
        for change in ('unknown', 'hold', 'asset', 'layer'):
            bad = copy.deepcopy(data)
            if change == 'unknown': bad['unexpected'] = 1
            elif change == 'hold': bad['phases']['travel']['frames'][0]['hold_frames'] = 0
            elif change == 'asset': bad['phases']['residual']['frames'][0]['file'] = 'missing.png'
            else: bad['layers']['glow']['alpha'] = 2
            (kit/'kit.json').write_text(json.dumps(bad))
            out = self.root/'invalid-project'
            with self.subTest(change=change), self.assertRaises(ValueError):
                build_project(self.fixture['cells'], out, vfx_kits=self.fixture['catalogue'], sockets=self.fixture['sockets'])
            self.assertFalse(out.exists())

    def test_minimal_layers_and_optional_decal_fallback(self):
        from export.effect_kit import build
        data = json.loads(self.fixture['definition'].read_text())
        data['layers'] = {'decal': {'duration_s': 1}}
        del data['phases']['residual']
        data['phases']['travel']['streak'] = False
        self.fixture['definition'].write_text(json.dumps(data))
        kit = self.root/'minimal-kit'
        build(self.fixture['definition'], kit)
        catalogue = self.root/'minimal.json'
        catalogue.write_text(json.dumps({'kits': [{'name':'minimal','dir':str(kit)}]}))
        out = self.root/'minimal-project'
        build_project(self.fixture['cells'], out, sockets=self.fixture['sockets'], vfx_kits=catalogue)
        text = (out/'scenes/vfx_minimal_impact.tscn').read_text()
        self.assertIn('[node name="Decal"',text)
        for name in ('DarkDuplicate','Glow','Flash','FloorLight','Streak','Particles','Residual'):
            self.assertNotIn(f'[node name="{name}"',text)
        validate_resources(out,True)

    @unittest.skipUnless(Path(GODOT).is_file(), 'Godot binary unavailable')
    def test_headless_authored_cast_east_north_collision_timing_and_feedback_cleanup(self):
        (self.project/'effect_probe.gd').write_text(EFFECT_PROBE)
        run_headless(self, self.project, 'effect_probe.gd')


EFFECT_PROBE = '''extends SceneTree
var errors: int = 0
func check(ok: bool, message: String) -> void:
    if not ok:
        errors += 1
        printerr("T3O_ASSERTION: ", message)
func _initialize() -> void:
    call_deferred("probe")
func probe() -> void:
    var scene: Node2D = load("res://scenes/main.tscn").instantiate()
    root.add_child(scene)
    await process_frame
    var keeper: CharacterBody2D = scene.get_node("Keeper")
    keeper.set_physics_process(false)
    await physics_frame
    var angles: Array = []
    var collision_paths: Array = []
    var baseline: float = Engine.time_scale
    var camera: Camera2D = keeper.get_node("Camera2D")
    var camera_offset: Vector2 = camera.offset
    for facing in ["E", "N"]:
        keeper.state = "cast"
        keeper.facing = facing
        keeper.cast_fired = false
        keeper.cast_kit_index = 0
        keeper.vfx_cursor_override = keeper.global_position + keeper.FACING_VECTORS[facing] * 400.0
        keeper.sprite.play("cast_" + facing)
        keeper.sprite.pause()
        keeper.sprite.frame = 2
        check(keeper.cast_fired, "socket release " + facing)
        var bolt: Area2D = get_nodes_in_group("vfx_g1_pool")[0]
        bolt.set_physics_process(false)
        check(bolt.scene_file_path == "res://scenes/vfx/g1_projectile.tscn", "authored bolt")
        var travel: AnimatedSprite2D = bolt.get_node("Head")
        var angle: float = bolt.direction.angle() * 180.0 / PI
        angles.append(travel.rotation_degrees)
        check(absf(travel.rotation_degrees-angle) < 0.001, "travel rotation")
        check(travel.scale.is_equal_approx(Vector2(1,0.6)), "ground squash")
        check(travel.sprite_frames.resource_path == "res://vfx/synthetic_ice/travel.tres", "own travel")
        check(is_equal_approx(travel.sprite_frames.get_frame_duration("travel",0) / travel.sprite_frames.get_animation_speed("travel"), 2.0/60.0), "first hold")
        check(is_equal_approx(travel.sprite_frames.get_frame_duration("travel",1), 5.0/60.0), "second hold")
        check(travel.material is ShaderMaterial, "painted head material")
        var old_position: Vector2 = bolt.position
        bolt._physics_process(0.01)
        check(is_equal_approx(bolt.position.distance_to(old_position), 3.6), "authored speed")
        var target := Area2D.new()
        scene.add_child(target)
        bolt.resolved.target = target
        bolt.resolved.kind = "prop"
        bolt.contact_body(target)
        check(bolt.expired, "collision expires bolt")
        var impact: Node2D = scene.get_child(scene.get_child_count()-1)
        collision_paths.append(impact.scene_file_path)
        check(impact.scene_file_path == "res://scenes/vfx_synthetic_ice_impact.tscn", "collision impact")
        check(impact.global_position.distance_to(bolt.global_position) < 0.001, "impact position")
        check(is_equal_approx(Engine.time_scale, 0.1), "hitstop active")
        check(camera.offset.distance_to(camera_offset) > 0, "shake active")
        # Stop restoration is owned by the tree, so early effect deletion is safe.
        if facing == "E":
            impact.queue_free()
        await create_timer(0.22, true, false, true).timeout
        check(is_equal_approx(Engine.time_scale, baseline), "hitstop baseline restored")
        check(camera.offset.distance_to(camera_offset) < 0.001, "camera offset restored")
        if facing == "N":
            check(not impact.get_node("Ground").visible, "body hides after held frames")
            check(impact.get_node("Residual").is_playing(), "residual follows impact")
            await create_timer(0.2, true, false, true).timeout
            check(not impact.get_node("Residual").visible, "residual hides when finished")
            check(impact.get_node("Ground/Flash").modulate.a < 0.001, "flash faded")
            check(impact.get_node("FloorLight").modulate.a < 0.001, "floor light faded")
            check(impact.get_node("Decal").modulate.a > 0.0, "decal outlives impact")
        keeper.state = "idle"
    print("T3T_RUNTIME=" + JSON.stringify({"rotation_degrees":angles,"collision_impacts":collision_paths,"errors":errors}))
    if errors == 0: print("T3O_RUNTIME_ASSERTIONS=complete")
    scene.queue_free()
    await process_frame
    quit(0 if errors == 0 else 7)
'''


PICKER_PROBE = '''extends SceneTree
var errors: int = 0
var keeper: CharacterBody2D
var scene: Node2D
func check(ok: bool, message: String) -> void:
    if not ok:
        errors += 1
        printerr("T3O_ASSERTION: ", message)
func _initialize() -> void:
    call_deferred("probe")
func tab() -> void:
    var event := InputEventKey.new()
    event.physical_keycode = KEY_TAB
    event.pressed = true
    Input.parse_input_event(event)
    Input.flush_buffered_events()
    keeper._physics_process(0.0)
    event = InputEventKey.new()
    event.physical_keycode = KEY_TAB
    event.pressed = false
    Input.parse_input_event(event)
    Input.flush_buffered_events()
func start_cast() -> void:
    keeper.state = "idle"
    keeper.sprite.pause()
    keeper.sprite.frame = 0
    Input.action_press("cast")
    keeper._physics_process(0.0)
    Input.action_release("cast")
    keeper.sprite.pause()
    check(keeper.state == "cast", "entered cast")
    check(not keeper.cast_fired, "not released at frame zero")
func release_bolt() -> Area2D:
    keeper.vfx_cursor_override = keeper._socket_world() + Vector2(0,650)
    keeper.sprite.frame = 2
    check(keeper.cast_fired, "released at socket frame two")
    var bolt: Area2D = get_nodes_in_group("vfx_g1_pool")[0]
    bolt.set_physics_process(false)
    check((bolt.global_position - bolt.direction * bolt.get_node("CollisionShape2D").shape.height).distance_to(keeper._socket_world()) < 0.001, "staff socket at capsule rear")
    check(bolt.resolved.kind == "cursor", "cursor resolved")
    return bolt
func probe() -> void:
    scene = load("res://scenes/main.tscn").instantiate()
    root.add_child(scene)
    await process_frame
    keeper = scene.get_node("Keeper")
    keeper.set_physics_process(false)
    await physics_frame
    keeper.sprite.pause()
    check(InputMap.action_get_events("vfx_cycle")[0].physical_keycode == 4194306, "Tab binding")
    check(keeper.VFX_KITS[0].name == "zeta" and keeper.VFX_KITS[1].name == "alpha", "manifest order")
    check(keeper.vfx_label.text == "VFX: zeta  (Tab)", "default label")
    check(keeper.vfx_label.position == Vector2(16,16), "label position")
    check(keeper.vfx_label.get_parent().layer == 10, "HUD layer")
    check(keeper.vfx_label.get_theme_font_size("font_size") == 22, "HUD font")
    var paths: Array = []
    var labels: Array = []
    for expected in ["alpha", "zeta"]:
        await process_frame
        keeper.state = "idle"
        tab()
        labels.append(keeper.vfx_label.text)
        check(keeper.vfx_label.text == "VFX: " + expected + "  (Tab)", "cycled label " + expected)
        await process_frame
        start_cast()
        var bolt: Area2D = release_bolt()
        paths.append(bolt.scene_file_path)
        check(bolt.config.name == expected, "cycled bolt " + expected)
        var flare: AnimatedSprite2D = keeper.active_flare
        check(flare.sprite_frames.resource_path == "res://vfx/"+expected+"/flare.tres", "matching flare")
        bolt._physics_process(10.0)
        bolt._physics_process(0.0)
        check(bolt.expired, "cursor impact")
        var impact: Node2D = scene.get_child(scene.get_child_count()-1)
        check(impact.scene_file_path == "res://scenes/vfx_"+expected+"_impact.tscn", "matching impact")
    # Start kit one, change selection before release: the entire cast stays one.
    await process_frame
    start_cast()
    await process_frame
    tab()
    check(keeper.vfx_label.text == "VFX: alpha  (Tab)", "label changes during cast")
    check(keeper.cast_kit_index == 0, "release snapshot unchanged")
    var inflight: Area2D = release_bolt()
    check(inflight.config.name == "zeta", "pre-release kit lock")
    await process_frame
    tab()
    var target := Area2D.new()
    scene.add_child(target)
    target.global_position = inflight.cast_origin + inflight.release_facing * 200.0
    inflight.resolved.target = target
    inflight.resolved.kind = "prop"
    inflight.contact_body(target)
    check(inflight.expired, "target collision")
    var impact: Node2D = scene.get_child(scene.get_child_count()-1)
    check(impact.scene_file_path == "res://scenes/vfx_zeta_impact.tscn", "in-flight impact kit lock")
    var report := {"bolt_paths": paths, "labels": labels, "inflight_kit": "zeta", "errors": errors}
    print("T3O_PICKER=" + JSON.stringify(report))
    if errors == 0: print("T3O_RUNTIME_ASSERTIONS=complete")
    scene.queue_free()
    await process_frame
    quit(0 if errors == 0 else 7)
'''

GLOW_PROBE = '''extends SceneTree
var errors: int = 0
func check(ok: bool, message: String) -> void:
    if not ok:
        errors += 1
        printerr("T3O_ASSERTION: ", message)
func _initialize() -> void:
    call_deferred("probe")
func probe() -> void:
    var scene: Node2D = load("res://scenes/glows.tscn").instantiate()
    root.add_child(scene)
    var glow: Sprite2D = scene.get_node("Actors/Glow_0")
    var overhead: Sprite2D = scene.get_node("Overhead/Glow_1")
    glow.set_process(false)
    overhead.set_process(false)
    check(glow.material.blend_mode == CanvasItemMaterial.BLEND_MODE_ADD, "glow additive")
    check(overhead.material.blend_mode == CanvasItemMaterial.BLEND_MODE_ADD, "overhead additive")
    check(glow.position.y == 201, "owner anchor plus one")
    check(glow.phases != overhead.phases, "different fixed instance phases")
    var samples: Array[float] = []
    var base: float = glow.base_alpha
    var amount: float = glow.flicker_amount
    var phases: Vector3 = glow.phases
    for i in range(60):
        glow._process(1.0 / 60.0)
        samples.append(glow.modulate.a)
        check(glow.phases == phases, "phases stay fixed")
        check(is_equal_approx(glow.scale.x / glow.base_scale.x, glow.modulate.a / base), "alpha and scale same multiplier")
        check((glow.position + glow.offset * glow.scale).distance_to(Vector2(100, 154)) < 0.001, "centre fixed while scaling")
    var extrema: int = 0
    var lo: float = samples[0]
    var hi: float = samples[0]
    for i in range(60):
        lo = minf(lo, samples[i])
        hi = maxf(hi, samples[i])
        if i > 0 and i < 59 and (samples[i]-samples[i-1])*(samples[i+1]-samples[i]) < 0:
            extrema += 1
    check(extrema >= 6, "at least six local extrema")
    check(hi-lo >= 0.5*amount*base, "alpha range at least half amount times base")
    check(lo >= base*(1-amount) and hi <= base*(1+amount), "normalised envelope")
    var particle: CPUParticles2D = scene.get_node("Air/Particles_embers")
    check(particle.gravity == Vector2(3,-24), "particle gravity")
    check(particle.material.blend_mode == CanvasItemMaterial.BLEND_MODE_ADD, "particle ADD material")
    check(particle.angular_velocity_min == -30 and particle.angular_velocity_max == 50, "angular velocity")
    check(particle.position == Vector2(100,150) and particle.emission_rect_extents == Vector2(10,10), "rect centre semantics")
    check(not particle.local_coords, "world particle coordinates")
    for x in [0.0, 0.25, 0.5, 0.75, 1.0]:
        check(is_equal_approx(particle.scale_amount_curve.sample(x), 1.0-x), "linear scale curve")
    print("T3O_GLOW=" + JSON.stringify({"samples": 60, "duration_s": 1.0, "fps": 60,
        "extrema": extrema, "alpha_range": hi-lo, "minimum_range": 0.5*amount*base,
        "base_alpha": base, "flicker_amount": amount, "errors": errors}))
    if errors == 0: print("T3O_RUNTIME_ASSERTIONS=complete")
    scene.queue_free()
    await process_frame
    quit(0 if errors == 0 else 7)
'''


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--fixture':
        project, report = build_fixture(sys.argv[2])
        print(json.dumps({'project': str(project), **report}, indent=2))
    else:
        unittest.main()


TOUCH_AIM_PROBE = '''extends SceneTree
const G1 = preload("res://scripts/vfx_g1.gd")
var errors: Array = []
var measurements: Array = []
func check(ok: bool, message: String) -> void:
    if not ok:
        errors.append(message)
        printerr("T3O_ASSERTION: ", message)
func _initialize() -> void:
    call_deferred("probe")
func cast_point(keeper: CharacterBody2D) -> Vector2:
    keeper.state = "idle"
    keeper.sprite.play("cast_S")
    keeper.sprite.pause()
    keeper.sprite.frame = 2
    keeper.state = "cast"
    keeper.cast_kit_index = 0
    keeper.cast_fired = false
    keeper._cast_frame_changed()
    var pool: Array = get_nodes_in_group("vfx_g1_pool")
    check(not pool.is_empty(), "cast released")
    if pool.is_empty():
        return Vector2.INF
    var bolt: Area2D = pool[0]
    var point: Vector2 = bolt.resolved.point
    bolt.cancel()
    return point
func record(label: String, actual: Vector2, expected: Vector2) -> void:
    measurements.append({"case": label, "actual": [actual.x, actual.y],
        "expected": [expected.x, expected.y], "error_px": actual.distance_to(expected)})
    check(actual.distance_to(expected) <= 2.0, label)
func probe() -> void:
    var main: Node2D = load("res://scenes/main.tscn").instantiate()
    root.add_child(main)
    var keeper: CharacterBody2D = main.get_node("Keeper")
    keeper.set_physics_process(false)
    await physics_frame
    await process_frame
    keeper.sprite.scale = Vector2.ONE * 0.75
    keeper.facing = "N"
    var viewport: Vector2 = keeper.get_viewport_rect().size
    var touch := InputEventScreenTouch.new()
    touch.pressed = true
    touch.position = Vector2(viewport.x * 0.5, viewport.y * 0.9)
    var stale := Vector2(-444, 555)
    keeper.vfx_cursor_override = stale
    keeper._unhandled_input(touch)
    check(keeper.vfx_cursor_override == stale, "overlay leaves probe hook untouched")
    var expected: Vector2 = keeper.global_position + keeper.FACING_VECTORS[keeper.facing].normalized() * float(keeper.VFX_KITS[0].range_px) * keeper.sprite.global_transform.x.length()
    record("overlay_forward", cast_point(keeper), expected)
    touch.position = Vector2(viewport.x * 0.4, viewport.y * 0.3)
    keeper._unhandled_input(touch)
    expected = keeper.get_canvas_transform().affine_inverse() * touch.position
    record("world_touch", cast_point(keeper), expected)
    # A later overlay tap must not reuse an earlier world-area aim.
    touch.position = Vector2(viewport.x * 0.5, viewport.y * 0.95)
    touch.pressed = false
    keeper._unhandled_input(touch)
    var emulated := InputEventMouseMotion.new()
    emulated.device = InputEvent.DEVICE_ID_EMULATION
    keeper._unhandled_input(emulated)
    expected = keeper.global_position + Vector2.UP * float(keeper.VFX_KITS[0].range_px) * keeper.sprite.global_transform.x.length()
    record("overlay_release_after_world_and_emulated_mouse", cast_point(keeper), expected)
    var drag := InputEventScreenDrag.new()
    drag.position = Vector2(viewport.x * 0.6, viewport.y * 0.2)
    keeper._unhandled_input(drag)
    expected = keeper.get_canvas_transform().affine_inverse() * drag.position
    record("world_drag", cast_point(keeper), expected)
    drag.position.y = ceilf(viewport.y * (1.0 - keeper.TOUCH_OVERLAY_BAND))
    keeper._unhandled_input(drag)
    expected = keeper.global_position + Vector2.UP * float(keeper.VFX_KITS[0].range_px) * keeper.sprite.global_transform.x.length()
    record("overlay_boundary_drag", cast_point(keeper), expected)
    var mouse := InputEventMouseMotion.new()
    keeper._unhandled_input(mouse)
    check(keeper.vfx_cursor_override == null, "real mouse clears touch override")
    record("mouse_cursor", cast_point(keeper), keeper.get_global_mouse_position())
    keeper.vfx_cursor_override = Vector2(-123, -234)
    record("mouse_probe_override", cast_point(keeper), Vector2(-123, -234))
    var button := InputEventMouseButton.new()
    keeper._unhandled_input(button)
    check(keeper.vfx_cursor_override == null, "mouse button clears probe override")
    record("mouse_button", cast_point(keeper), keeper.get_global_mouse_position())
    DirAccess.make_dir_recursive_absolute("res://out")
    var file := FileAccess.open("res://out/touch_aim.json", FileAccess.WRITE)
    file.store_string(JSON.stringify({"errors": errors, "measurements": measurements}, "  "))
    file.close()
    print("T3O_RUNTIME_ASSERTIONS=complete")
    quit(0 if errors.is_empty() else 7)
'''


class TouchAimRuntimeTests(unittest.TestCase):
    @unittest.skipUnless(Path(GODOT).is_file(), 'Godot binary unavailable')
    def test_headless_overlay_forward_world_touch_and_mouse_probe(self):
        # T4i artifacts remain in the explicitly scoped tooling directory.
        temporary = ROOT/'runs/C-5/t3/T4x/touch'
        temporary.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='touch-aim-', dir=temporary) as directory:
            root = Path(directory)
            cells, sockets, kits, _ = fixture_inputs(root/'inputs')
            project = root/'project'
            build_project(cells, project, sockets=sockets, vfx_kits=kits)
            # T4x: T4i-r1 device-forward policy replaced the retired input hook.
            (project/'touch_aim_probe.gd').write_text(TOUCH_DEVICE_AIM_PROBE)
            run_headless(self, project, 'touch_aim_probe.gd')
            report = json.loads((project/'out/touch_aim.json').read_text())
            self.assertEqual(report['errors'], [])
            self.assertEqual(len(report['measurements']), 8)
            for row in report['measurements']:
                with self.subTest(case=row['case']):
                    self.assertLessEqual(row['error_px'], 2.0)


class G1ComponentTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix='g1-', dir=TMP)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.cells, self.sockets, self.kits, self.props = fixture_inputs(self.root/'inputs')

    def test_shared_component_no_legacy_bolts_and_cast_ready_gate(self):
        out = self.root/'project'
        build_project(self.cells, out, sockets=self.sockets, vfx_kits=self.kits)
        self.assertEqual(list((out/'scripts').glob('vfx_*_bolt.gd')), [])
        scene = (out/'scenes/vfx/g1_projectile.tscn').read_text()
        self.assertIn('type="AnimatedSprite2D"', scene)
        self.assertIn('type="Line2D"', scene)
        self.assertNotIn('texture_filter = 1', scene)
        self.assertEqual(scene.count('texture_filter = 2'), 3)
        keeper = (out/'scripts/keeper.gd').read_text()
        self.assertIn('if not cast_ready:\n        await get_tree().physics_frame', keeper)
        self.assertLess(keeper.index('var kit: Dictionary = VFX_KITS[cast_kit_index]'), keeper.index('await get_tree().physics_frame'))
        validate_resources(out, True)

    def test_grey_all_body_rgb_128_exact_alpha_and_default_bytes(self):
        import numpy as np
        painted, grey = self.root/'painted', self.root/'grey'
        build_project(self.cells, painted, sockets=self.sockets, vfx_kits=self.kits)
        build_project(self.cells, grey, sockets=self.sockets, vfx_kits=self.kits, vfx_grey=True)
        count = 0
        for source in (painted/'vfx').rglob('*.png'):
            with Image.open(source) as im: a = np.array(im)
            with Image.open(grey/source.relative_to(painted)) as im: b = np.array(im)
            self.assertTrue(np.array_equal(a[..., 3], b[..., 3]))
            self.assertTrue(np.all(b[..., :3] == 128))
            count += 1
        self.assertEqual(count, 10)
        with self.assertRaises(ValueError):
            build_project(self.cells, self.root/'bad', vfx_grey=1)
        self.assertFalse((self.root/'bad').exists())

    def test_event_instrument_known_bad_delay_first_miss_unresolved_order(self):
        from export.godot_import import evaluate_g1_events
        good = [dict(effect_id=1, event='release', age_frames=0, target_kind='prop', target_point=[30,20]),
                dict(effect_id=1, event='contact', age_frames=4, collision_age_frames=3),
                dict(effect_id=1, event='expire', age_frames=4)]
        self.assertTrue(all(r['passed'] for r in evaluate_g1_events(good)))
        mutations = []
        late = copy.deepcopy(good); late[1]['collision_age_frames'] = 2
        mutations.append(('g1_contact_lag', late))
        mutations.append(('g1_first_cast', [good[0],good[2]]))
        unresolved = copy.deepcopy(good); unresolved[0].pop('target_point')
        mutations.append(('g1_unresolved_releases', unresolved))
        reversed_age = copy.deepcopy(good); reversed_age[2]['age_frames'] = 1
        mutations.append(('g1_event_order', reversed_age))
        for key, evidence in mutations:
            with self.subTest(key=key):
                rows = {r['id']:r for r in evaluate_g1_events(evidence)}
                self.assertIs(rows[key]['passed'], False)
        self.assertTrue(all(r['passed'] is None for r in evaluate_g1_events([])))
        for evidence in (None, [{}], [dict(effect_id=1,event='bogus',age_frames=0)],
                         [dict(effect_id=1,event='release',age_frames=True)]):
            with self.assertRaises(ValueError): evaluate_g1_events(evidence)

    @unittest.skipUnless(Path(GODOT).is_file(), 'Godot binary unavailable')
    def test_headless_first_cast_contact_cursor_pool_cancel_and_picker(self):
        out = self.root/'project'
        build_project(self.cells, out, sockets=self.sockets, vfx_kits=self.kits)
        run_headless(self, out, 'probe_vfx.gd')
        from export.godot_import import evaluate_g1_events
        rows = evaluate_g1_events(json.loads((out/'out/events.json').read_text()))
        self.assertTrue(all(r['passed'] for r in rows))

    def test_pierce_metadata_default_explicit_and_known_bad(self):
        from test_effect_kit import definition_fixture
        from export.effect_kit import build, load_kit
        path, data = definition_fixture(self.root/'source')
        for value in (None, 0, 1, 3, -1):
            definition = copy.deepcopy(data)
            if value is not None: definition['pierce'] = value
            path.write_text(json.dumps(definition))
            out = self.root/('kit_'+str(value))
            build(path, out)
            self.assertEqual(load_kit(out)['pierce'], 0 if value is None else value)
        omitted, explicit = self.root/'kit_None', self.root/'kit_0'
        self.assertEqual({p.relative_to(omitted):p.read_bytes() for p in omitted.rglob('*') if p.is_file()},
                         {p.relative_to(explicit):p.read_bytes() for p in explicit.rglob('*') if p.is_file()})
        for value in (-2, True, False, 1.5, '1', None, [], float('inf')):
            with self.subTest(value=value):
                definition = dict(data, pierce=value)
                path.write_text(json.dumps(definition))
                with self.assertRaisesRegex(ValueError, 'pierce'):
                    build(path, self.root/'bad')
                self.assertFalse((self.root/'bad').exists())
        metadata = json.loads((omitted/'kit.json').read_text())
        metadata.pop('pierce')
        (omitted/'kit.json').write_text(json.dumps(metadata))
        self.assertEqual(load_kit(omitted)['pierce'], 0)

    def test_pierce_config_defaults_palette_range_and_feedback_gates(self):
        from test_effect_kit import picker_fixture
        from export.godot_import import _g1_config
        fixture = picker_fixture(self.root/'authored')
        kit = _load_vfx_kits(fixture['catalogue'])[0]
        config = _g1_config(kit)
        self.assertEqual(config['pierce'], 0)
        self.assertEqual(config['range_px'], 650.0)
        self.assertEqual(config['palette_3'], kit['effect']['material']['palette'][3])
        kit['effect']['pierce'] = -1
        self.assertEqual(_g1_config(kit)['pierce'], -1)
        impact = (fixture['project']/'scripts/vfx_synthetic_ice_impact.gd').read_text()
        self.assertIn('if get_meta("strike_response", true):\n        _feedback()', impact)
        self.assertIn('if not get_meta("strike_response", true) and has_node("Ground/Flash"):', impact)
        label = (fixture['project']/'scripts/vfx_contact_label.gd').read_text()
        for token in ('LIFETIME_S: float = 0.6', 'RISE_PX: float = 40.0', 'Time.get_ticks_usec()', '"font_size", 22', 'font_outline_color'):
            self.assertIn(token, label)

    @staticmethod
    def _pierce_evidence():
        events = [dict(effect_id=1, event='contact', body_index=i, phase='head',
                       contact_class='primary' if i == 0 else 'secondary',
                       contact_distance_px=60+i*80, strike_response=i == 0) for i in range(3)]
        labels = [dict(effect_id=1, body_index=i, text='FULL' if i == 0 else 'PARTIAL',
                       lifetime_s=.61, rise_px=40) for i in range(3)]
        return events, labels

    def test_pierce_instrument_known_bad_order_strike_duplicate_lifetime_and_class(self):
        from export.godot_import import evaluate_pierce_events
        events, labels = self._pierce_evidence()
        self.assertTrue(all(r['passed'] for r in evaluate_pierce_events(events, labels)))
        mutations = []
        bad = copy.deepcopy(events); bad[2]['contact_distance_px'] = 1
        mutations.append(('pierce_distance_order', bad, labels))
        bad = copy.deepcopy(events); bad[1]['strike_response'] = True
        mutations.append(('pierce_strike_once', bad, labels))
        mutations.append(('pierce_labels_unique', events, labels+[labels[0]]))
        bad = copy.deepcopy(labels); bad[0]['lifetime_s'] = .801
        mutations.append(('pierce_label_lifetime', events, bad))
        bad = copy.deepcopy(labels); bad[0]['text'] = 'PARTIAL'
        mutations.append(('pierce_contact_text', events, bad))
        bad = copy.deepcopy(events); bad[1]['contact_class'] = 'primary'
        mutations.append(('pierce_contact_text', bad, labels))
        bad = copy.deepcopy(labels); bad[0]['rise_px'] = 39
        mutations.append(('pierce_label_rise', events, bad))
        for key, e, l in mutations:
            with self.subTest(key=key):
                self.assertIs({r['id']:r['passed'] for r in evaluate_pierce_events(e,l)}[key], False)
        self.assertTrue(all(r['passed'] is None for r in evaluate_pierce_events([], [])))
        bad = copy.deepcopy(labels); bad[0]['lifetime_s'] = None
        self.assertIsNone({r['id']:r['passed'] for r in evaluate_pierce_events(events,bad)}['pierce_label_lifetime'])
        bad = copy.deepcopy(events); bad[0]['contact_distance_px'] = float('nan')
        with self.assertRaises(ValueError): evaluate_pierce_events(bad,labels)

    def test_pierce_phase_classification_chain_field_shard(self):
        from export.godot_import import evaluate_pierce_events
        for phases, classes in ((['chain_hop']*3, ['primary']*3),
                                (['field_centre','rim','shard'], ['primary','secondary','secondary'])):
            events, labels = self._pierce_evidence()
            for event, label, phase, cls in zip(events,labels,phases,classes):
                event.update(phase=phase, contact_class=cls)
                label['text'] = 'FULL' if cls == 'primary' else 'PARTIAL'
            self.assertTrue(all(r['passed'] for r in evaluate_pierce_events(events, labels)))

    @unittest.skipUnless(Path(GODOT).is_file(), 'Godot binary unavailable')
    def test_headless_pierce_contacts_labels_pool_and_phase_callbacks(self):
        from test_effect_kit import picker_fixture
        from export.godot_import import evaluate_pierce_events
        fixture = picker_fixture(self.root/'authored')
        run_headless(self, fixture['project'], 'probe_pierce.gd')
        report = json.loads((fixture['project']/'out/probe_pierce.json').read_text())
        self.assertEqual(report['errors'], [])
        self.assertTrue(all(row['passed'] for row in evaluate_pierce_events(report['events'], report['labels'])))

    def test_omitted_pierce_matches_pre_t4f_33_file_byte_lock(self):
        from test_effect_kit import definition_fixture
        from export.effect_kit import build
        path, _ = definition_fixture(self.root/'source')
        out = self.root/'byte_lock'
        build(path, out)
        digest = hashlib.sha256()
        files = [p for p in sorted(out.rglob('*')) if p.is_file()]
        self.assertEqual(len(files), 33)
        for path in files:
            data = path.read_bytes()
            if path.name == 'kit.json':
                metadata = json.loads(data)
                self.assertEqual(metadata.pop('pierce'), 0)
                data = (json.dumps(metadata, indent=2, allow_nan=False)+'\n').encode()
            digest.update(path.relative_to(out).as_posix().encode()+b'\0'+data)
        self.assertEqual(digest.hexdigest(), '2495fc1bd2f2d8b3dbee84d527a05632ddb35d418964b8fcb28a3686815548bf')


# T4i-r1 device policy; T4i expectations above are retained verbatim.
TOUCH_DEVICE_AIM_PROBE = '''extends SceneTree
class ConsumingOverlay:
    extends Node
    var observed: int = 0
    func _input(event: InputEvent) -> void:
        if event is InputEventScreenTouch:
            observed += 1
            get_viewport().set_input_as_handled()
const G1 = preload("res://scripts/vfx_g1.gd")
var errors: Array = []
var measurements: Array = []
func check(ok: bool, message: String) -> void:
    if not ok:
        errors.append(message)
        printerr("T3O_ASSERTION: ", message)
func _initialize() -> void:
    call_deferred("probe")
func cast_point(keeper: CharacterBody2D) -> Vector2:
    keeper.state = "idle"
    keeper.sprite.play("cast_S")
    keeper.sprite.pause()
    keeper.sprite.frame = 2
    keeper.state = "cast"
    keeper.cast_kit_index = 0
    keeper.cast_fired = false
    keeper._cast_frame_changed()
    var pool: Array = get_nodes_in_group("vfx_g1_pool")
    check(not pool.is_empty(), "cast released")
    if pool.is_empty():
        return Vector2.INF
    var bolt: Area2D = pool[0]
    var point: Vector2 = bolt.resolved.point
    bolt.cancel()
    return point
func record(label: String, actual: Vector2, expected: Vector2) -> void:
    measurements.append({"case": label, "actual": [actual.x, actual.y],
        "expected": [expected.x, expected.y], "error_px": actual.distance_to(expected)})
    check(actual.distance_to(expected) <= 2.0, label)
func probe() -> void:
    var main: Node2D = load("res://scenes/main.tscn").instantiate()
    root.add_child(main)
    var keeper: CharacterBody2D = main.get_node("Keeper")
    keeper.set_physics_process(false)
    await physics_frame
    await process_frame
    keeper.sprite.scale = Vector2.ONE * 0.75
    keeper.facing = "N"
    # No touch event reaches Keeper before this cast. The mouse is behind it.
    keeper.vfx_force_touch_device = true
    keeper.global_position = keeper.get_global_mouse_position() + Vector2.UP * 200.0
    check((keeper.get_global_mouse_position() - keeper.global_position).dot(Vector2.UP) < 0.0, "mouse behind north-facing Keeper")
    var expected: Vector2 = keeper.global_position + Vector2.UP * float(keeper.VFX_KITS[0].range_px) * keeper.sprite.global_transform.x.length()
    record("touch_device_no_event_N", cast_point(keeper), expected)
    # Reproduce the overlay consuming both world-area and CAST-button touches.
    var overlay := ConsumingOverlay.new()
    root.add_child(overlay)
    var touch := InputEventScreenTouch.new()
    touch.pressed = true
    touch.position = Vector2(150, 100)
    root.push_input(touch)
    touch.pressed = false
    touch.position = Vector2(500, 650)
    root.push_input(touch)
    check(overlay.observed == 2, "overlay consumed both touch events")
    var mouse := InputEventMouseMotion.new()
    mouse.device = InputEvent.DEVICE_ID_EMULATION
    mouse.position = Vector2(500, 650)
    root.push_input(mouse)
    keeper.facing = "NE"
    var axis: Vector2 = keeper.FACING_VECTORS[keeper.facing].normalized()
    keeper.global_position = keeper.get_global_mouse_position() + axis * 200.0
    check((keeper.get_global_mouse_position() - keeper.global_position).dot(axis) < 0.0, "mouse behind northeast-facing Keeper")
    expected = keeper.global_position + axis * float(keeper.VFX_KITS[0].range_px) * keeper.sprite.global_transform.x.length()
    record("touch_device_handled_overlay_NE", cast_point(keeper), expected)
    keeper.vfx_cursor_override = Vector2(-123, -234)
    record("touch_probe_override", cast_point(keeper), Vector2(-123, -234))
    keeper.vfx_cursor_override = null
    keeper.vfx_force_touch_device = false
    check(not DisplayServer.is_touchscreen_available(), "desktop headless device")
    record("mouse_cursor", cast_point(keeper), keeper.get_global_mouse_position())
    keeper.vfx_cursor_override = Vector2(-345, -456)
    record("mouse_probe_override", cast_point(keeper), Vector2(-345, -456))
    keeper.vfx_cursor_override = null
    var prop := Area2D.new()
    root.add_child(prop)
    prop.global_position = keeper.global_position + axis * 100.0 + axis.orthogonal() * 10.0
    prop.add_to_group("vfx_targets")
    record("desktop_nearest_prop", cast_point(keeper), prop.global_position)
    keeper.vfx_force_touch_device = true
    record("touch_ignores_nearest_prop", cast_point(keeper), expected)
    prop.remove_from_group("vfx_targets")
    # Real mouse motion on a hybrid device must also leave forward policy intact.
    mouse.device = 0
    root.push_input(mouse)
    record("touch_device_after_real_mouse", cast_point(keeper), expected)
    prop.queue_free()
    overlay.queue_free()
    DirAccess.make_dir_recursive_absolute("res://out")
    var file := FileAccess.open("res://out/touch_aim.json", FileAccess.WRITE)
    file.store_string(JSON.stringify({"errors": errors, "measurements": measurements}, "  "))
    file.close()
    print("T3O_RUNTIME_ASSERTIONS=complete")
    quit(0 if errors.is_empty() else 7)
'''


class TouchDeviceAimRuntimeTests(unittest.TestCase):
    @unittest.skipUnless(Path(GODOT).is_file(), 'Godot binary unavailable')
    def test_headless_device_forward_handled_overlay_and_mouse_probe(self):
        # T4i-r1 artifacts remain in the explicitly scoped tooling directory.
        temporary = ROOT/'runs/C-5/t3/T4i-r1/tmp'
        temporary.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='touch-aim-', dir=temporary) as directory:
            root = Path(directory)
            cells, sockets, kits, _ = fixture_inputs(root/'inputs')
            project = root/'project'
            build_project(cells, project, sockets=sockets, vfx_kits=kits)
            (project/'touch_aim_probe.gd').write_text(TOUCH_DEVICE_AIM_PROBE)
            run_headless(self, project, 'touch_aim_probe.gd')
            report = json.loads((project/'out/touch_aim.json').read_text())
            self.assertEqual(report['errors'], [])
            self.assertEqual(len(report['measurements']), 8)
            for row in report['measurements']:
                with self.subTest(case=row['case']):
                    self.assertLessEqual(row['error_px'], 2.0)


class PieceLap2ExportTests(unittest.TestCase):
    """T4j real-kit export regression and emitted motion contract."""
    def setUp(self):
        TMP.mkdir(parents=True,exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='t4j-',dir=TMP)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cells = self.root/'cells'; self.cells.mkdir()
        for phase in ('idle','cast'):
            Image.new('RGBA',(512,512)).save(self.cells/(phase+'_E_0.png'))
        self.sockets = self.root/'sockets.json'
        self.sockets.write_text(json.dumps({'version':1,'canvas':[512,512],'cells':{'cast_E':{'sockets':[[256,256]],'release_index':0}}}))

    def test_six_kits_and_v1_match_488_file_pre_t4j_hash_table(self):
        evidence = ROOT/'runs/C-5/t3/T4j'
        expected = json.loads((ROOT/'fixtures/fl1b/PieceLap2ExportTests-3.json').read_text())
        project = self.root/'legacy'
        build_project(self.cells,project,vfx_kits=evidence/'legacy_catalogue.json',sockets=self.sockets)
        actual = {p.relative_to(project).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in sorted(project.rglob('*')) if p.is_file()}
        self.assertEqual(len(actual),488)
        self.assertEqual(actual,expected)

    def test_v2_emits_drift_stretch_groups_and_stationary_residue(self):
        project = self.root/'project'
        build_project(self.cells,project,vfx_kit=ROOT/'runs/C-5/vfx_kits/v9/fire_burst_e0p_v2',sockets=self.sockets)
        script = (project/'scripts/vfx/piece_burst_v2.gd').read_text()
        self.assertIn('Seeded along stretch is 2.0..2.5',script)
        self.assertIn('lerpf(1.0,0.85,ease)',script)
        self.assertIn('float(config.root_drift) * float(config.core_radius_px) * ease',script)
        self.assertIn('axis.set_position(root_start + Vector2.RIGHT.rotated',script)
        self.assertIn('var ease: float = 1.0-pow(1.0-flight_t,3.0)',script)
        runtime = json.loads(next((project/'vfx').rglob('burst_runtime.json')).read_text())
        self.assertEqual(runtime['root_drift'],.5)
        self.assertEqual(runtime['dissolve_order'],[[3],[2],[1,0]])
        self.assertTrue(runtime['grouped_dissolve'])
        self.assertTrue(runtime['erode_outside_in'])
        for item in runtime['pieces']:
            self.assertGreaterEqual(item['along'],2.0)
            self.assertLessEqual(item['along'],2.5)
        material = next((project/'vfx').rglob('Root_001.tres')).read_text()
        shader_path = re.search(r'path="res://([^\"]+gdshader)"',material)[1]
        shader = (project/shader_path).read_text()
        self.assertIn('vec4(0.83333333333333337, 0.83333333333333337, 0.66666666666666674, 0.5)[int(band)]',shader)
        self.assertIn('shader_parameter/erode_outside_in = true',material)
        self.assertIn('distance_value > 1.0 - erode',shader)
        self.assertIn('var residue_t: float = clampf(float(age-residue_start)/float(config.residue_frames),0.0,1.0)',script)
        self.assertIn('var dissolve: float = 1.0 if age >= residue_end else 0.8 * residue_t',script)
        self.assertIn('paint.material.set_shader_parameter("dissolve",0.0)',script)
        self.assertIn('root_sprite.material.set_shader_parameter("dissolve",dissolve)',script)
        self.assertIn('axis.visible = active and age < residue_start',script)
        validate_resources(project,True)


E1_PROBE = r'''extends SceneTree
const G1 = preload("res://scripts/vfx_g1.gd")
const KEEPER = preload("res://scripts/keeper.gd")
var errors: Array = []
var samples: Array = []
var bursts: int = 0
var expected_impact: String = ""
func check(value: bool, message: String) -> void:
    if not value:
        errors.append(message)
        printerr("E1_ASSERTION: ", message)
func _initialize() -> void:
    call_deferred("run")
func run() -> void:
    var world := Node2D.new()
    root.add_child(world)
    world.child_entered_tree.connect(func(node):
        if node.scene_file_path == expected_impact:
            bursts += 1)
    var target := Area2D.new()
    target.name = "VfxTarget_dummy"
    target.position = Vector2(320,0)
    target.collision_layer = 2
    target.collision_mask = 0
    target.set_meta("body_index",0)
    var shape := CollisionShape2D.new()
    shape.shape = RectangleShape2D.new()
    shape.shape.size = Vector2(24,48)
    target.add_child(shape)
    world.add_child(target)
    target.add_to_group("vfx_targets")
    await physics_frame
    await physics_frame
    var kits: Array = KEEPER.VFX_KITS.filter(func(k): return k.has("painted_travel"))
    for kit in kits:
        expected_impact = kit.impact
        var before: int = bursts
        var destination: Dictionary = G1.resolve_target(self,Vector2.ZERO,Vector2.RIGHT,Vector2(float(kit.range_px),0),float(kit.range_px))
        var effect: Area2D = G1.acquire(world,kit,Vector2.ZERO,destination,null,0.25)
        check(effect != null,"resolved cast")
        if effect == null:
            continue
        var id: int = effect.effect_id
        check(effect.spell_scale == 1.0,"screen_px ignores art scale")
        check(effect.get_node("Head").rotation == 0.0,"east orientation")
        var clock: Array = []
        for age in range(int(kit.painted_travel.rest_hold_frames)+kit.key_states.reduce(func(n,s): return n+int(kit.painted_travel.rest_hold_frames)+int(s.hold_frames),0)):
            effect._paint_clock(age)
            clock.append(effect.travel_state)
        var expected: Array = []
        if not kit.key_states.is_empty():
            for state in kit.key_states:
                for tick in range(kit.painted_travel.rest_hold_frames): expected.append("rest")
                for tick in range(state.hold_frames): expected.append(state.state)
            for age in range(clock.size()): check(clock[age] == expected[age % expected.size()],"held key schedule")
        else:
            check(clock.all(func(x): return x == "rest"),"empty keys rest only")
        effect.config.speed_px_s = float(kit.spec_speed_px_s)*10.0
        effect._paint_clock(0)
        check(is_equal_approx(effect.get_node("Streak").scale.x / float(kit.painted_travel.streak.scale),1.4),"upper speed clamp")
        effect.config.speed_px_s = float(kit.spec_speed_px_s)/10.0
        effect._paint_clock(0)
        check(is_equal_approx(effect.get_node("Streak").scale.x / float(kit.painted_travel.streak.scale),0.6),"lower speed clamp")
        effect.config.speed_px_s = float(kit.spec_speed_px_s)
        for frame in range(int(ceil(float(kit.range_px)/float(kit.speed_px_s)*60))+2):
            await physics_frame
            if not effect.active: break
        var contacts: Array = G1.events.filter(func(e): return e.effect_id == id and e.event == "contact")
        var labels: Array = G1.label_events.filter(func(e): return e.effect_id == id)
        check(contacts.size() == 1,"one first contact")
        if contacts.size() == 1:
            check(float(contacts[0].contact_distance_px) <= float(kit.range_px),"contact within range")
            check(contacts[0].contact_class == "primary","primary contact")
            check(contacts[0].contact_lag_frames <= 1,"T4b clock lag")
        check(bursts-before == 1,"one bound pieces burst")
        check(labels.size() == 1,"one label")
        if labels.size() == 1: check(labels[0].text == "FULL","T4f FULL")
        check(effect.draining,"tail retained after stop")
        var tail: Array = []
        for tick in range(int(ceil(float(kit.painted_travel.tail_s)*60))+2):
            await physics_frame
            tail.append(float(effect.get_node("Streak").material.get_shader_parameter("erode")))
        check(not effect.draining and not effect.visible,"tail released after configured lifetime")
        samples.append({"kit":kit.name,"clock":clock,"contacts":contacts,"labels":labels,"tail_erode":tail,"bursts":bursts-before})
        # Cursor distance is aim-only; no burst on range exhaustion.
        before = bursts
        var miss: Area2D = G1.acquire(world,kit,Vector2(0,100),{"kind":"cursor","point":Vector2(10,100),"target":null})
        for frame in range(int(ceil(float(kit.range_px)/float(kit.speed_px_s)*60))+2): await physics_frame
        check(not miss.active,"range expiry")
        check(is_equal_approx(miss.global_position.x,float(kit.range_px)),"configured range despite nearby cursor")
        check(bursts == before,"range expiry has no contact burst")
    for frame in range(50): await physics_frame
    for label in get_nodes_in_group("vfx_contact_labels"):
        check(not label.visible,"labels released within 0.8 seconds")
    var file := FileAccess.open("res://e1_trace.json",FileAccess.WRITE)
    file.store_string(JSON.stringify({"samples":samples,"events":G1.events,"labels":G1.label_events,"errors":errors},"  "))
    file.close()
    print("E1_RUNTIME=" + JSON.stringify({"errors":errors,"casts":samples.size(),"bursts":bursts}))
    quit(0 if errors.is_empty() else 1)
'''


def e1_project_fixture(root, keyed=False):
    """Standalone real-kit headless input; every temporary stays under root."""
    import shutil
    root=Path(root); root.mkdir(parents=True,exist_ok=True)
    cells=root/'cells'; cells.mkdir()
    for direction in ('E','S'):
        for kind,n in [('idle',1),('cast',4)]:
            for i in range(n): Image.new('RGBA',(512,512),(40,80,120,255)).save(cells/f'{kind}_{direction}_{i}.png')
    sockets=root/'sockets.json'
    sockets.write_text(json.dumps({'version':1,'canvas':[512,512],'cells':{'cast_'+d:{'sockets':[[270,240]]*4,'release_index':2} for d in ('E','S')}}))
    kitroot=ROOT/'runs/C-5/vfx_kits/v9'
    entries=[{'name':'fire_burst_e0p_v2','dir':str(kitroot/'fire_burst_e0p_v2')}]
    for arm in ('A','B'):
        name='fire_bolt_e1_'+arm; directory=kitroot/name
        if keyed and arm=='A':
            target=root/name; shutil.copytree(directory,target); directory=target
            data=json.loads((directory/'kit.json').read_text())
            data['key_states']=[dict(state=n,png='primitives/head.png',pivot=[404,266.5],scale=.65,hold_frames=h)
                                for n,h in [('stretched',3),('pulsed',4)]]
            (directory/'kit.json').write_text(json.dumps(data))
        entries.append({'name':name,'dir':str(directory)})
    # FL-4b: include the new B impact without changing the v2 comparison.
    entries.append({'name':'fire_burst_e0p_v3','dir':str(kitroot/'fire_burst_e0p_v3')})
    catalogue=root/'kits.json'; catalogue.write_text(json.dumps({'kits':entries}))
    project=root/'project'; build_project(cells,project,vfx_kits=catalogue,sockets=sockets)
    (project/'e1_probe.gd').write_text(E1_PROBE)
    return project


class ProjectileArmPickerTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(prefix='e1-picker-',dir=TMP)
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def test_empty_key_exports_byte_identically_except_kit_name(self):
        """FL-4b: preserve export byte parity except keys, name, and explicit impact binding."""
        project=e1_project_fixture(self.root)
        a,b=[project/'vfx'/('fire_bolt_e1_'+arm) for arm in ('A','B')]
        def common(root):
            result = {}
            for path in root.rglob('*'):
                rel = path.relative_to(root)
                if not path.is_file() or 'key_states' in rel.parts or 'travel_keys' in rel.parts or path.name.startswith('Travel_key_'):
                    continue
                raw = path.read_bytes().replace(root.name.encode(), b'ARM')
                if path.name == 'kit.json':
                    data = json.loads(raw); data.pop('key_states', None)
                    self.assertEqual(data['impact_binding']['kit'], 'fire_burst_e0p_v2' if root == a else 'fire_burst_e0p_v3')
                    self.assertEqual(data['skill_spec']['presentation']['primitive_bindings']['impact'], data['impact_binding']['kit']+' (pieces phase, burst_v2)')
                    data['skill_spec']['presentation']['primitive_bindings']['impact'] = 'IMPACT (pieces phase, burst_v2)'
                    data['impact_binding']['kit'] = 'IMPACT'
                    raw = json.dumps(data, sort_keys=True).encode()
                result[rel] = raw
            return result
        self.assertEqual(common(a), common(b))
        for folder in ('scripts','scenes'):
            for file in (project/folder).glob('*fire_bolt_e1_A*'):
                bfile=file.with_name(file.name.replace('fire_bolt_e1_A','fire_bolt_e1_B'))
                self.assertEqual(file.read_bytes().replace(b'fire_bolt_e1_A',b'ARM'),bfile.read_bytes().replace(b'fire_bolt_e1_B',b'ARM'))

    @unittest.skipUnless(Path(GODOT).is_file(),'Godot unavailable')
    def test_headless_east_contact_range_tail_and_key_schedule(self):
        project=e1_project_fixture(self.root,keyed=True)
        records=[]
        for arguments in (['--import'],['--script','res://e1_probe.gd']):
            proc=subprocess.run([GODOT,'--headless','--path',str(project),'--log-file',str(self.root/'engine.log'),*arguments],capture_output=True,text=True,timeout=60)
            text=proc.stdout+proc.stderr
            records.append({'arguments':arguments,'exit':proc.returncode,'log':text})
            self.assertEqual(proc.returncode,0,text)
            self.assertNotIn('SCRIPT ERROR',text)
            self.assertNotIn('E1_ASSERTION',text)
        trace=json.loads((project/'e1_trace.json').read_text())
        self.assertEqual(trace['errors'],[])
        expected=[k['name'] for k in _load_vfx_kits(self.root/'kits.json') if 'travel_primitives' in k.get('effect',{})]
        self.assertEqual([sample['kit'] for sample in trace['samples']],expected)
        evidence=ROOT/'runs/C-5/t3/FL-4d/e1'
        evidence.mkdir(parents=True,exist_ok=True)
        (evidence/'e1_key_trace.json').write_text(json.dumps(trace,indent=2)+'\n')
        (evidence/'e1_headless.json').write_text(json.dumps(records,indent=2)+'\n')

    def test_original_eight_export_byte_lock(self):
        baseline=ROOT/'fixtures/fl1b/ProjectileArmPickerTests-2.json'
        self.assertTrue(baseline.is_file(),'T4t current eleven-kit snapshot required')
        cells=self.root/'cells'; cells.mkdir()
        for direction in ('E','N','S'):
            for kind,n in [('idle',1),('cast',4)]:
                for i in range(n): Image.new('RGBA',(512,512),(40,80,120,255)).save(cells/f'{kind}_{direction}_{i}.png')
        sockets=self.root/'sockets.json'
        sockets.write_text(json.dumps({'version':1,'canvas':[512,512],'cells':{'cast_'+d:{'sockets':[[270,240]]*4,'release_index':2} for d in ('E','N','S')}}))
        catalogue_path=ROOT/'runs/C-5/vfx_kits/kits_v9.json'
        data=json.loads(catalogue_path.read_text())
        self.assertEqual([k['name'] for k in data['kits'][8:11]],['fire_bolt_e1_A','fire_bolt_e1_B','ice_bolt_e2'])
        original={'kits':[dict(k,dir=str((catalogue_path.parent/k['dir']).resolve())) for k in data['kits'][:11]]}
        # FL-4b: close B's explicit new dependency before comparing bytes.
        original['kits'] += [dict(k,dir=str((catalogue_path.parent/k['dir']).resolve())) for k in data['kits'] if k['name']=='fire_burst_e0p_v3']
        catalogue=self.root/'kits.json'; catalogue.write_text(json.dumps(original))
        project=self.root/'project'; build_project(cells,project,vfx_kits=catalogue,sockets=sockets)
        actual={p.relative_to(project).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in project.rglob('*') if p.is_file()}
        self.assertEqual(actual,json.loads(baseline.read_text()))


    def test_tail_field_runs_from_tail_to_socket_and_grey_keeps_bands(self):
        from export.godot_import import _grey_vfx
        import numpy as np
        project=e1_project_fixture(self.root)
        for arm in ('A', 'B'):
            arm_root = project/'vfx'/('fire_bolt_e1_'+arm)
            with Image.open(arm_root/'primitives/streak.png') as im: pixels=np.array(im)
            with Image.open(arm_root/'distance/primitives/tail.png') as im: tail=np.array(im)
            yy,xx=np.nonzero(pixels[...,3])
            self.assertEqual(int(tail[yy[xx.argmin()],xx.min()]),0)
            self.assertEqual(int(tail[yy[xx.argmax()],xx.max()]),255)
            self.assertTrue((np.diff(tail.astype(int),axis=1)>=0).all())
            material=(arm_root/'materials/Travel_streak.tres').read_text()
            shader_path=re.search(r'path="res://([^"\n]+\.gdshader)"',material)[1]
            shader=(project/shader_path).read_text()
            self.assertIn('float distance_value = 1.0 - texture(distance_texture, UV).r;',shader)
            self.assertIn('distance_value > 1.0 - erode',shader)
            self.assertIn('shader_parameter/erode_noise = 0.3',material)
            with Image.open(arm_root/'distance/primitives/tail_noise.png') as im: noise=np.array(im)/255.
            resistance=.3*(.5*(2*noise[...,0]-1)+.5*noise[...,1])
            old=(255-tail.astype(float))/255.-resistance
            current=1-tail.astype(float)/255.-resistance
            np.testing.assert_allclose(current,old,atol=1e-15)
            for erosion in (.1,.25,.5,.75,.9):
                # Complement arithmetic differs by <1e-15 at exact threshold
                # ties; require identical coverage away from those ties.
                stable=np.abs(old-(1-erosion))>1e-14
                np.testing.assert_array_equal(current[stable]>1-erosion,old[stable]>1-erosion)
        root=project/'vfx/fire_bolt_e1_B'
        with Image.open(root/'primitives/streak.png') as im: rgba=np.array(im)
        with Image.open(root/'distance/primitives/tail.png') as im: field=np.array(im)
        ys,xs=np.nonzero(rgba[...,3])
        self.assertEqual(int(field[ys[xs.argmin()],xs.min()]),0)
        self.assertEqual(int(field[ys[xs.argmax()],xs.max()]),255)
        self.assertTrue((np.diff(field.astype(int),axis=1)>=0).all())
        _grey_vfx(project)
        with Image.open(root/'primitives/streak.png') as im: np.testing.assert_array_equal(np.array(im),rgba)
        material=(root/'materials/Travel_streak.tres').read_text()
        for band in range(4): self.assertIn(f'shader_parameter/palette_{band} = Color(0.5, 0.5, 0.5, 1)',material)
        keeper=(project/'scripts/keeper.gd').read_text()
        self.assertIn('"material": "res://vfx/fire_bolt_e1_B/materials/Travel_streak.tres"',keeper)


E2_PROBE = r'''extends SceneTree
const G1 = preload("res://scripts/vfx_g1.gd")
const KEEPER = preload("res://scripts/keeper.gd")
var errors: Array = []
var impact: Node2D
var bursts: int = 0
var samples: Array = []
var hitstop_seen: bool = false
func check(value: bool, message: String) -> void:
    if not value: errors.append(message)
func _initialize() -> void:
    call_deferred("run")
func run() -> void:
    var world := Node2D.new()
    root.add_child(world)
    world.child_entered_tree.connect(func(node):
        if node.scene_file_path == "res://scenes/vfx_ice_bolt_e2_impact.tscn":
            impact = node
            bursts += 1)
    var target := Area2D.new()
    target.name = "VfxTarget_ice_dummy"
    target.position = Vector2(320,0)
    target.collision_layer = 2
    target.collision_mask = 0
    target.set_meta("body_index",0)
    var shape := CollisionShape2D.new()
    shape.shape = RectangleShape2D.new()
    shape.shape.size = Vector2(24,48)
    target.add_child(shape)
    world.add_child(target)
    target.add_to_group("vfx_targets")
    await physics_frame
    await physics_frame
    var kits: Array = KEEPER.VFX_KITS.filter(func(k): return k.name == "ice_bolt_e2")
    check(kits.size() == 1,"ice registration")
    if kits.is_empty():
        quit(1)
        return
    var kit: Dictionary = kits[0]
    var destination: Dictionary = G1.resolve_target(self,Vector2.ZERO,Vector2.RIGHT,Vector2(520,0),520.0)
    var effect: Area2D = G1.acquire(world,kit,Vector2.ZERO,destination,null,0.25)
    var id: int = effect.effect_id
    check(is_equal_approx(effect.get_node("Streak").modulate.a,0.6),"puff alpha")
    check(effect.get_node("Head").rotation == 0.0,"east tip orientation")
    var scales: Array = []
    for speed in [520.0,1040.0,1300.0]:
        effect.config.speed_px_s = speed
        effect._paint_clock(0)
        scales.append(effect.get_node("Streak").scale.x)
    check(scales[0] < scales[1] and scales[1] < scales[2],"speed-linked streak")
    effect.config.speed_px_s = 1040.0
    for frame in range(155):
        await physics_frame
        hitstop_seen = hitstop_seen or Engine.time_scale < 1.0
        if is_instance_valid(impact) and not impact.trace.is_empty():
            var row: Dictionary = impact.trace[-1].duplicate(true)
            if samples.is_empty() or samples[-1].age_frames != row.age_frames:
                samples.append(row)
            check(impact.get_node("Art").scale == Vector2.ONE,"screen pixel scale")
            check(not impact.has_node("Residual"),"no residual sprite")
            var decal: Sprite2D = impact.ground_decal
            check(decal.global_position.distance_to(target.global_position) < 0.01,"decal contact anchor")
            check(decal.get_parent().name == "GroundEffects" and decal.z_as_relative,"decal owned by ground layer")
            check(decal.scale == Vector2(1.0,0.6),"decal native scale plus ground squash")
    var contacts: Array = G1.events.filter(func(e): return e.effect_id == id and e.event == "contact")
    var labels: Array = G1.label_events.filter(func(e): return e.effect_id == id)
    check(contacts.size() == 1,"one contact, pierce zero")
    if contacts.size() == 1:
        check(contacts[0].contact_distance_px <= 520.0,"contact range")
        check(contacts[0].contact_lag_frames <= 1,"contact clock")
        check(contacts[0].contact_class == "primary" and contacts[0].strike_response,"primary strike")
    check(bursts == 1,"one impact burst")
    check(labels.size() == 1 and labels[0].text == "FULL","one FULL label")
    check(hitstop_seen and is_equal_approx(Engine.time_scale,1.0),"hit stop and restoration")
    var decal_rows: Array = samples.filter(func(r): return r.decal_visible)
    check(not decal_rows.is_empty(),"decal handoff")
    if not decal_rows.is_empty():
        check(decal_rows[-1].decal_alpha < decal_rows[0].decal_alpha,"decal fades")
        check(decal_rows[-1].age_frames-decal_rows[0].age_frames <= 36,"decal_s clock")
    check(not is_instance_valid(impact),"decal released after decal_s")
    var expanded: Array = samples.filter(func(r): return r.stage == "erosion")
    if not expanded.is_empty():
        check(expanded[0].shard_count == expanded[0].source_piece_count,"all spatial pieces emitted")
        for piece in expanded[0].pieces:
            check(absf(piece.rotation_deg) <= 45.0,"shard rotation bound")
            check(piece.scale >= 0.85 and piece.scale <= 1.15,"native shard scale bound")
    for label in get_nodes_in_group("vfx_contact_labels"):
        check(not label.visible,"label released")
    var a: Node2D = load("res://scenes/vfx_ice_bolt_e2_impact.tscn").instantiate()
    var b: Node2D = load("res://scenes/vfx_ice_bolt_e2_impact.tscn").instantiate()
    root.add_child(a)
    root.add_child(b)
    a.set_physics_process(false)
    b.set_physics_process(false)
    var starts: Array = []
    var translations: Array = []
    var deterministic: bool = true
    for age in range(112):
        a.set_effect_age(age)
        b.set_effect_age(age)
        deterministic = deterministic and a.trace[-1] == b.trace[-1]
        if age == 3:
            for piece in a.pieces: starts.append(piece.node.position)
        if age == 18:
            for i in range(a.pieces.size()):
                translations.append(a.pieces[i].node.position.distance_to(starts[i]))
        if age == 39:
            check(a.get_node("Art/Peak").visible,"stationary residue at entry")
            check(a.get_node("Art/Peak").position == Vector2.ZERO,"residue origin")
            check(a.get_node("Art/Peak").scale == Vector2.ONE,"residue by erosion only")
        if age == 111:
            check(not a.ground_decal.visible and a.ground_decal.modulate.a == 0.0,"decal exact release clock")
    check(deterministic,"seed-equal clocks")
    check(translations.size() == 22 and translations.all(func(v): return v > 0.0),"every shard translates radially")
    var report: Dictionary = {"errors":errors,"contacts":contacts,"labels":labels,"bursts":bursts,"hitstop_seen":hitstop_seen,"streak_scales":scales,"samples":samples,"seed_equal":deterministic,"translations_px":translations,"decal_release_age":111}
    var file := FileAccess.open("res://e2_trace.json",FileAccess.WRITE)
    file.store_string(JSON.stringify(report,"  "))
    file.close()
    print("E2_RUNTIME="+JSON.stringify({"errors":errors,"bursts":bursts,"samples":samples.size()}))
    quit(0 if errors.is_empty() else 1)
'''


class IceTreatmentPickerTests(unittest.TestCase):
    """Real E2 clock proof in a wholly T4r-owned temporary project."""
    def test_headless_contact_shatter_residue_decal(self):
        from test_godot_import import ice_project_fixture
        work=ROOT/'runs/C-5/t3/T4x'
        with tempfile.TemporaryDirectory(prefix='e2-clock-',dir=work) as tmp:
            project=ice_project_fixture(Path(tmp))
            (project/'e2_probe.gd').write_text(E2_PROBE)
            records=[]
            for args in (['--import'],['--script','res://e2_probe.gd']):
                started=time.monotonic()
                result=subprocess.run([GODOT,'--headless','--path',str(project),'--log-file',str(Path(tmp)/'engine.log'),*args],capture_output=True,text=True,timeout=60)
                self.assertLess(time.monotonic()-started,60,'headless deadline')
                records.append(dict(arguments=args,exit=result.returncode,elapsed_s=time.monotonic()-started,log=result.stdout+result.stderr))
                self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                self.assertNotIn('SCRIPT ERROR',result.stdout+result.stderr)
            report=json.loads((project/'e2_trace.json').read_text())
            (work/'e2_trace.json').write_text(json.dumps(report,indent=2)+'\n')
            (work/'e2_headless.json').write_text(json.dumps(records,indent=2)+'\n')
            self.assertEqual(report['errors'],[])


class ThrownFieldPickerTests(unittest.TestCase):
    def test_thirteen_kits_registered_and_grammar_dispatch_explicit(self):
        from export.godot_import import _g2_config
        cat=ROOT/'runs/C-5/vfx_kits/kits_v9.json';kits=_load_vfx_kits(cat)
        self.assertGreaterEqual(len(kits),13)
        self.assertEqual([k['name'] for k in kits[11:13]],['blackwater_cocktail_e3','poisonous_concoction_e3'])
        for kit in kits[11:13]:
            config=_g2_config(kit)
            self.assertEqual(config['grammar'],'G2')
            self.assertEqual(config['ticks'],kit['effect']['skill_spec']['mechanics']['field']['tick_schedule_s'])
            self.assertEqual(config['ground_squash'],kit['effect']['ground_squash'])
            self.assertEqual(config['flask_width'],45.5)

    def test_headless_g2_trace_mechanics_and_scale_evidence(self):
        work=ROOT/'runs/C-5/t3/T4s'
        trace=json.loads((work/'g2_trace.json').read_text())
        self.assertEqual(trace['errors'],[])
        self.assertEqual(len(trace['samples']),2)
        for sample in trace['samples']:
            self.assertLessEqual(sample['fragment_lifetime_s'],.2)
            self.assertEqual(sample['tint_count'],sample['tick_count']*2)
            self.assertFalse(sample['schedule']['ff08_satisfied'])
        scale=json.loads((work/'scale_after.json').read_text())
        for sample in scale:
            self.assertAlmostEqual(sample['head_width_px'],156,places=3)
            self.assertAlmostEqual(sample['streak_length_px'],260,places=3)


class BoltChainPickerTests(unittest.TestCase):
    def test_clock_trace_targets_delays_stretch_and_lifetime(self):
        import numpy as np
        trace=json.loads((ROOT/'runs/C-5/t3/T4t/g3_trace.json').read_text())
        self.assertEqual(trace['errors'],[])
        live=next(s for s in trace['samples'] if s['name']=='live_physics')
        contacts=[e for e in live['events'] if e['event']=='contact']
        self.assertEqual([e['body_index'] for e in contacts],[0,1,2,3,4])
        spec=json.loads((ROOT/'runs/C-5/specs/zeus_chain.json').read_text())
        requested=np.cumsum(spec['mechanics']['chain']['hop_delay_s'])
        observed=np.array([e['age_frames']/60 for e in contacts[1:]])
        self.assertTrue(np.all(observed+1e-9>=requested))
        self.assertTrue(np.all(observed-requested<1/60+1e-9))
        intervals=np.diff([e['age_frames']/60 for e in contacts])
        self.assertGreaterEqual(float(intervals.std()/intervals.mean()),.25)
        for sample in trace['samples']:
            for event in sample['events']:
                if event['event']=='bolt':
                    self.assertLessEqual(event['junction_sprite_count'],1)
                    for link in event['links']: self.assertLessEqual(link['stretch_ratio'],1.15+1e-6)
                    for point in event['prong_positions']:np.testing.assert_allclose(point,event['target_point'],atol=.001)
                if event['event']=='bolt_end':self.assertLessEqual(event['local_age_s'],.27+1e-9)

    def test_source_alpha_geometry_overlap_and_tip_registration(self):
        report=json.loads((ROOT/'runs/C-5/t3/T4t/geometry.json').read_text())
        self.assertLessEqual(report['max_overlap_diameter_px'],4)
        self.assertLessEqual(report['max_stretch'],1.15)
        self.assertLessEqual(report['max_socket_gap_px'],.001)
        for sample in report['samples']:
            for bolt in sample['bolt_metrics']:
                if sample['name'].startswith('zeus_chain') or sample['name']=='live_physics':
                    self.assertTrue(2<=bolt['link_count']<=3)
                for pair in bolt['nearest_nonzero_alpha_to_joint_px']:
                    self.assertLessEqual(max(pair),1.)


class AuraLoopPickerTests(unittest.TestCase):
    def test_g4_dispatch_precedes_socket_and_target_resolution(self):
        from export.godot_import import _load_vfx_kit
        work=ROOT/'runs/C-5/t3/T4u';work.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=work) as tmp:
            root=Path(tmp);cells=root/'cells';cells.mkdir()
            for i in range(4):Image.new('RGBA',(512,512),(20,40,60,255)).save(cells/f'cast_E_{i}.png')
            sockets=root/'sockets.json';sockets.write_text(json.dumps({'version':1,'canvas':[512,512],'cells':{'cast_E':{'sockets':[[270,240]]*4,'release_index':2}}}))
            cat=root/'kits.json';cat.write_text(json.dumps({'kits':[{'name':'renamed_support','dir':str(ROOT/'runs/C-5/vfx_kits/v9/healing_hands_e3')}]}))
            build_project(cells,root/'project',sockets=sockets,vfx_kits=cat)
            script=(root/'project/scripts/keeper.gd').read_text()
            dispatch=script.index('G4.acquire(self, VFX_KITS[cast_kit_index])')
            self.assertLess(dispatch,script.index('var socket: Variant = _socket_world()'))
            self.assertLess(dispatch,script.index('destination = G1.resolve_target'))
            self.assertNotIn('healing_hands_e3',script)
            self.assertIn('"grammar": "G4"',script)


FROZEN_ORB_PROBE = 'extends SceneTree\nvar errors: Array = []\nfunc _initialize() -> void:\n    call_deferred("run")\nfunc run() -> void:\n    var world := Node2D.new()\n    root.add_child(world)\n    for i in range(3):\n        var target := Area2D.new()\n        target.name = "Dummy%d" % i\n        target.position = Vector2(160+i*160,0)\n        target.collision_layer = 2\n        target.collision_mask = 0\n        target.set_meta("body_index",i)\n        target.add_to_group("vfx_targets")\n        var shape := CollisionShape2D.new()\n        var circle := CircleShape2D.new()\n        circle.radius = 25.0\n        shape.shape = circle\n        target.add_child(shape)\n        world.add_child(target)\n    await physics_frame\n    var g1 = load("res://scripts/vfx_g1.gd")\n    var config: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://orb_config.json"))\n    config.pierce = int(config.pierce)\n    var destination: Dictionary = g1.resolve_target(self,Vector2.ZERO,Vector2.RIGHT,Vector2(float(config.range_px),0),float(config.range_px))\n    var orb: Area2D = g1.acquire(world,config,Vector2.ZERO,destination,null,4.0)\n    var source_id: int = orb.effect_id\n    var burst_trace: Array = []\n    var max_nodes: int = 0\n    for frame in range(240):\n        await physics_frame\n        await process_frame\n        max_nodes = maxi(max_nodes,orb.get_node("ChildPool").get_child_count())\n        if is_instance_valid(orb.burst_node):\n            burst_trace = orb.burst_node.trace.duplicate(true)\n    var report: Dictionary = {"events":g1.events.duplicate(true),"labels":g1.label_events.duplicate(true),"trace":orb.trace.duplicate(true),"burst_trace":burst_trace,"pool_nodes":max_nodes,"orb_effect_id":source_id,"errors":errors}\n    var first_instance: int = orb.get_instance_id()\n    var again: Area2D = g1.acquire(world,config,Vector2.ZERO,destination,null,1.0)\n    report["reuse_same_orb"] = again.get_instance_id() == first_instance\n    report["reuse_pool_nodes"] = again.get_node("ChildPool").get_child_count()\n    again.cancel()\n    report["cancel_children_active"] = again.get_node("ChildPool").get_children().filter(func(n): return n.active).size()\n    var file := FileAccess.open("res://orb_trace.json",FileAccess.WRITE)\n    file.store_string(JSON.stringify(report,"  "))\n    file.close()\n    quit()\n'


class FrozenOrbPickerTests(unittest.TestCase):
    def setUp(self):
        from export.godot_import import build_project
        self.work=ROOT/'runs/C-5/t3/T4v'
        self.temp=tempfile.TemporaryDirectory(prefix='orb-runtime-',dir=self.work)
        self.addCleanup(self.temp.cleanup)
        self.project=Path(self.temp.name)/'project'
        build_project(ROOT/'runs/C-3/cells_v7',self.project,
                      vfx_kits=ROOT/'runs/C-5/vfx_kits/kits_v9.json',
                      sockets=ROOT/'runs/C-3/sockets_v2.json')
        result=subprocess.run([GODOT,'--headless','--path',str(self.project),'--log-file',str(self.work/'orb-import.log'),'--editor','--import','--quit'],capture_output=True,text=True,timeout=110)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertNotIn('SCRIPT ERROR',result.stdout+result.stderr)

    def test_headless_orb_clock_and_pool(self):
        from export.godot_import import _g1_config
        work=self.work;project=self.project
        kit=next(k for k in _load_vfx_kits(ROOT/'runs/C-5/vfx_kits/kits_v9.json') if 'orb' in k.get('effect',{}))
        (project/'orb_config.json').write_text(json.dumps(_g1_config(kit)))
        (project/'probe.gd').write_text(FROZEN_ORB_PROBE)
        result=subprocess.run([GODOT,'--headless','--path',str(project),'--log-file',str(work/'orb-test.log'),'--script','res://probe.gd'],capture_output=True,text=True,timeout=60)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertNotIn('SCRIPT ERROR',result.stdout+result.stderr)
        trace=json.loads((project/'orb_trace.json').read_text());events=trace['events'];cast=trace['orb_effect_id']
        (work/'orb_trace.json').write_text(json.dumps(trace,indent=2)+'\n')
        own=[e for e in events if e['effect_id']==cast]
        emissions=[e for e in own if e['event']=='child_emission']
        self.assertEqual([e['scheduled_age'] for e in emissions],_g1_config(kit)['schedule']['emission_ages'])
        self.assertEqual([e['age_frames'] for e in emissions],_g1_config(kit)['schedule']['emission_ages'])
        for a,b in zip(emissions,emissions[1:]):self.assertAlmostEqual(b['angle_deg']-a['angle_deg'],137,places=3)
        contacts=[e for e in own if e['event']=='contact']
        self.assertEqual([e['body_index'] for e in contacts],[0,1,2])
        self.assertEqual([e['contact_class'] for e in contacts],['primary','secondary','secondary'])
        self.assertEqual(sum(e['strike_response'] for e in contacts),1)
        expiry=[e for e in own if e['event']=='expire'];self.assertEqual(len(expiry),1)
        self.assertEqual(expiry[0]['age_frames'],90);self.assertEqual(expiry[0]['position'],[630,0])
        bursts=[e for e in own if e['event']=='expiry_burst'];self.assertEqual(len(bursts),1)
        self.assertEqual(bursts[0]['shards'],16);self.assertEqual(bursts[0]['hold_frames'],0 if kit['effect']['orb']['expiry_mode']=='nova' else kit['effect']['pieces']['hold_frames'])
        self.assertEqual(trace['pool_nodes'],12);self.assertEqual(trace['reuse_pool_nodes'],12)
        self.assertTrue(trace['reuse_same_orb']);self.assertEqual(trace['cancel_children_active'],0)
        self.assertFalse(any(e['event']=='pool_exhausted' for e in events))
        self.assertEqual(max(r['shard_count'] for r in trace['burst_trace']),16)
        decals=[r for r in trace['burst_trace'] if r['decal_visible']]
        self.assertEqual(bool(decals),kit['effect']['orb']['expiry_decal'])
        if decals:
            self.assertTrue(all(r['decal_position']==expiry[0]['position'] for r in decals))
            self.assertLess(decals[-1]['decal_alpha'],decals[0]['decal_alpha'])
        labels=[e for e in trace['labels'] if e['effect_id']==cast]
        self.assertEqual(len(labels),len({e['body_index'] for e in labels}))


# FL-1a: actual headless node traces, shared by acceptance and unittest.
FL1_PROBE = r'''extends SceneTree
const G1 = preload("res://scripts/vfx_g1.gd")
var report: Dictionary = {"halo":[],"release":[],"flight":[],"expiry":[]}
var keeper: CharacterBody2D
var scene: Node2D
var boxes: Dictionary = {"S":Rect2(228,160,70,240),"SW":Rect2(218,170,82,230),"W":Rect2(205,165,89,235),"NW":Rect2(209,165,85,235),"N":Rect2(218,166,75,234),"NE":Rect2(227,165,80,235),"E":Rect2(222,164,78,236),"SE":Rect2(221,164,88,236)}
func _initialize() -> void: call_deferred("run")
func inventory(node: Node) -> Dictionary:
    var counts: Dictionary = {"burst_pieces":0,"floor_lights":0,"impacts":0}
    if node is CanvasItem and node.is_visible_in_tree():
        if String(node.name).begins_with("Piece_"): counts.burst_pieces += 1
        if node.name == "FloorLight": counts.floor_lights += 1
    if String(node.scene_file_path).ends_with("_impact.tscn"): counts.impacts += 1
    for child in node.get_children():
        var sub: Dictionary = inventory(child)
        for key in counts: counts[key] += sub[key]
    return counts
func run() -> void:
    scene = load("res://scenes/main.tscn").instantiate()
    root.add_child(scene)
    keeper = scene.get_node("Keeper")
    keeper.set_physics_process(false)
    keeper.set_process(false)
    keeper.global_position = Vector2(3760,640)
    keeper.sprite.scale = Vector2.ONE * (130.0/240.0)
    await physics_frame
    await process_frame
    for kit_name in ["fire_bolt_e1_B","fire_bolt_e1_A","ice_bolt_e2"]:
        var ki: int = 0
        for i in range(keeper.VFX_KITS.size()):
            if keeper.VFX_KITS[i].name == kit_name: ki = i
        for facing in keeper.DIRECTIONS:
            keeper.state = "idle"
            keeper.facing = facing
            keeper.cast_kit_index = ki
            keeper.cast_fired = false
            keeper.sprite.animation = "cast_"+facing
            keeper.sprite.pause()
            keeper.sprite.frame = 0
            keeper.state = "cast"
            keeper.vfx_cursor_override = keeper.global_position + keeper.FACING_VECTORS[facing].normalized()*2000.0
            keeper.halo_start_tick = -1
            for tick in range(9):
                keeper.sprite.frame = tick/3
                keeper._physics_process(0.0)
                var halo: Sprite2D = keeper.cast_halo
                var socket: Vector2 = keeper._socket_world()
                report.halo.append({"kit":kit_name,"direction":facing,"tick":tick,"frame":keeper.sprite.frame,
                    "texture_class":halo.texture.get_class(),"is_head_texture":halo.texture.resource_path == keeper.VFX_KITS[ki].painted_travel.head.png,
                    "diameter_bh":halo.texture.get_width()*halo.global_scale.x/130.0,"position_error_px":halo.global_position.distance_to(socket),
                    "alpha":halo.modulate.a,"additive":halo.material.blend_mode == CanvasItemMaterial.BLEND_MODE_ADD})
                await physics_frame
                await process_frame
            keeper.sprite.frame = 3
            keeper._cast_frame_changed()
            var pool: Array = get_nodes_in_group("vfx_g1_pool")
            var bolt: Area2D = pool[-1]
            bolt.set_physics_process(false)
            var head: AnimatedSprite2D = bolt.get_node("Head")
            var point: Array = bolt.config.painted_travel.head.rear_socket
            var rear: Vector2 = head.to_global(head.offset + Vector2(point[0],point[1]))
            var derived: Vector2 = keeper._socket_world()
            report.release.append({"kit":kit_name,"direction":facing,"rear_error_px":rear.distance_to(derived),"capsule_rear_error_px":(bolt.global_position-bolt.direction*bolt.get_node("CollisionShape2D").shape.height).distance_to(derived),
                "release_socket_error_px":bolt.cast_origin.distance_to(derived),"release_socket_cell":keeper.socket_cells["cast_"+facing].sockets[int(keeper.socket_cells["cast_"+facing].release_index)],
                "socket_facing_dot_px":(bolt.cast_origin-keeper.global_position).dot(keeper.FACING_VECTORS[facing].normalized()),
                "facing_dot_px":(bolt.global_position-keeper.global_position).dot(keeper.FACING_VECTORS[facing].normalized()),
                "socket_world":[derived.x,derived.y],"bolt_position":[bolt.global_position.x,bolt.global_position.y],"halo_visible":keeper.cast_halo.visible})
            var max_counts: Dictionary = {"burst_pieces":0,"floor_lights":0,"impacts":0}
            for tick in range(60):
                if bolt.active: bolt._paint_clock(tick)
                var painting: Node2D = bolt.get_node("KeyState") if bolt.get_node("KeyState").visible else head
                var tex: Texture2D = painting.texture if painting is Sprite2D else bolt.rest_head
                var box: Rect2 = tex.get_image().get_used_rect()
                var centre: Vector2 = painting.to_global(painting.offset+box.get_center())
                var local: Vector2 = keeper.sprite.to_local(centre)-keeper.sprite.offset
                if painting.visible:
                    report.flight.append({"kit":kit_name,"direction":facing,"tick":tick,"age":bolt.age_frames(),"projectile_z":bolt._effective_z(bolt),"keeper_z":bolt._effective_z(keeper),"head_drawn":painting.is_visible_in_tree(),"normal_z_restored":not bolt.release_sort_override,"head_centre_in_body":boxes[facing].has_point(local),"caster_contact":bolt.contacted.has(keeper.get_instance_id()),"local_centre":[local.x,local.y]})
                var counts: Dictionary = inventory(scene)
                for key in counts: max_counts[key] = maxi(max_counts[key],counts[key])
                bolt._physics_process(1.0/60.0)
                await physics_frame
                await process_frame
            report.expiry.append({"kit":kit_name,"direction":facing,"distance_px":bolt.distance,"fizzle":bolt.fizzle_trace.duplicate(true),"max_visible":max_counts,"strike_fired":bolt.strike_fired,"contacts":bolt.contacted.size(),"events":G1.events.duplicate(true)})
            G1.events.clear()
            bolt.queue_free()
            for child in scene.get_children():
                if String(child.scene_file_path).ends_with("_impact.tscn"): child.queue_free()
            keeper.state = "idle"
            keeper._update_cast_halo()
            await process_frame
    # FL-1b: literal v24 shield footprint on the G1 target collision layer.
    # Check emergence, not just subsequent movement: fire's initial nose is past it.
    var shield := Area2D.new()
    shield.collision_layer = 2
    shield.collision_mask = 0
    shield.set_meta("body_index", 44)
    scene.add_child(shield)
    shield.global_position = Vector2(3911.25,596)
    var polygon := CollisionPolygon2D.new()
    var points := PackedVector2Array()
    for i in range(16): points.append(Vector2(35.2*cos(i*TAU/16),15.4*sin(i*TAU/16)))
    polygon.polygon = points
    shield.add_child(polygon)
    report.near_shield = []
    await physics_frame
    await process_frame
    for kit_name in ["fire_bolt_e1_B","fire_bolt_e1_A","ice_bolt_e2"]:
        keeper.state = "idle"
        keeper.facing = "E"
        for i in range(keeper.VFX_KITS.size()):
            if keeper.VFX_KITS[i].name == kit_name: keeper.cast_kit_index = i
        keeper.cast_fired = false
        keeper.sprite.animation = "cast_E"
        keeper.sprite.pause()
        keeper.sprite.frame = 3
        keeper.state = "cast"
        keeper.vfx_cursor_override = shield.global_position
        keeper._cast_frame_changed()
        var bolt: Area2D = get_nodes_in_group("vfx_g1_pool")[-1]
        var rows: Array = []
        for tick in range(60):
            rows.append({"tick":tick,"position":[bolt.global_position.x,bolt.global_position.y],"active":bolt.active})
            await physics_frame
            await process_frame
        var contacts: Array = G1.events.filter(func(e): return e.event == "contact")
        var edge_error: float = INF
        var tip_error: float = INF
        if not contacts.is_empty():
            var hit := Vector2(contacts[0].position[0],contacts[0].position[1])
            for i in range(points.size()):
                var nearest: Vector2 = Geometry2D.get_closest_point_to_segment(hit,shield.to_global(points[i]),shield.to_global(points[(i+1)%points.size()]))
                edge_error = minf(edge_error,hit.distance_to(nearest))
            var head: AnimatedSprite2D = bolt.get_node("Head")
            var pivot: Array = bolt.config.painted_travel.head.pivot
            # FL-2c collision tip is the capsule node. FL-5 deliberately offsets
            # the growing painting back to the staff tip; art is not a collider.
            tip_error = bolt.global_position.distance_to(hit)
        report.near_shield.append({"kit":kit_name,"rows":rows,"contacts":contacts.duplicate(true),"edge_error_px":edge_error,"tip_error_px":tip_error})
        G1.events.clear()
        bolt.queue_free()
        keeper.state = "idle"
        await process_frame
    var output := FileAccess.open("res://fl1_trace.json",FileAccess.WRITE)
    output.store_string(JSON.stringify(report))
    print("FL1_TRACE_COMPLETE")
    quit()
'''


def fl1_trace(directory):
    """Full catalogue, original cast pixels, independent literal measurements."""
    import os, shutil
    directory = Path(directory)
    cells = directory/'cells'; cells.mkdir(parents=True)
    for direction in ('S','SW','W','NW','N','NE','E','SE'):
        for source in (ROOT/'runs/C-3/cells_v7'/('cast_'+direction)).rglob('cast_*.png'):
            shutil.copyfile(source,cells/source.name)
    project = directory/'project'
    export = build_project(cells, project, sockets=ROOT/'runs/C-3/sockets_v2.json',vfx_kits=ROOT/'runs/C-5/vfx_kits/kits_v9.json')
    (directory/'export.json').write_text(json.dumps(export,indent=2))
    (project/'fl1_probe.gd').write_text(FL1_PROBE)
    logs = []
    for label,args in [('import',['--editor','--import']),('trace',['--script','res://fl1_probe.gd'])]:
        result = subprocess.run([GODOT,'--headless','--path',str(project),'--log-file',str(directory/(label+'-engine.log')),*args],capture_output=True,text=True,timeout=120)
        (directory/(label+'.log')).write_text(result.stdout+result.stderr)
        logs.append(dict(stage=label,exit_code=result.returncode))
        if result.returncode: raise RuntimeError(label+': '+result.stderr[-1000:])
    (directory/'headless.json').write_text(json.dumps(logs,indent=2))
    return json.loads((project/'fl1_trace.json').read_text())


class FireLaneSocketSchemaTests(unittest.TestCase):
    def test_all_release_rows_keep_eight_tip_points_and_provenance(self):
        data=json.loads((ROOT/'runs/C-3/sockets_v2.json').read_text())
        self.assertEqual(data['canvas'],[512,512])
        for direction in ('S','SW','W','NW','N','NE','E','SE'):
            cell=data['cells']['cast_'+direction]
            # FL-5c: annotation text is provenance, never a facing/ferrule instrument.
            self.assertIsInstance(cell['release_socket_rule'],str)
            self.assertTrue(cell['release_socket_rule'])
            self.assertEqual(cell['release_index'],3)
            self.assertEqual(len(cell['sockets']),8)
            self.assertTrue(all(len(p)==2 and all(0<=v<512 for v in p) for p in cell['sockets']))


class FL2TraceContractTests(unittest.TestCase):
    def setUp(self):
        self.report=json.loads((ROOT/'runs/C-5/t3/FL-2c/retained_fl2.json').read_text())

    def test_eased_floor_and_exact_peak_hold(self):
        samples=self.report['part3']['floor_samples']
        self.assertEqual([r['seconds'] for r in samples],[0,.1,.2,.35])
        for row in samples:
            self.assertAlmostEqual(row['alpha'],.6*(1-row['seconds']/.35)**2,places=6)
        self.assertNotAlmostEqual(samples[1]['alpha'],.6*(1-.1/.35),places=4)
        self.assertEqual(self.report['part5']['peak_frames'],[19,20,21,22])
        self.assertAlmostEqual(self.report['part5']['peak_alphas'][0],.35,places=6)
        self.assertAlmostEqual(self.report['part5']['peak_scales'][0],1.06,places=6)

    def test_motes_count_pool_and_every_lifetime(self):
        report=self.report['part4']
        self.assertGreaterEqual(report['ember_count'],8);self.assertLessEqual(report['ember_count'],12)
        self.assertTrue(report['all_motes_dead'])
        self.assertLessEqual(report['max_lifetime_overrun_s'],1e-9)
        self.assertLessEqual(report['last_residue_death_tick'],report['residue_end_plus_max_life_ticks'])
        for mote in report['births']:
            self.assertGreaterEqual(mote['life_s'],.5);self.assertLessEqual(mote['life_s'],.9)
            self.assertIn(mote['band'],[2,3])
        self.assertLessEqual(self.report['part2']['trail_max_live'],8)
        self.assertGreater(len(self.report['part2']['trail_births']),0)

    def test_flicker_and_cast_fade_clocks(self):
        trace=self.report['part2']['flicker_trace']
        self.assertGreaterEqual(len(trace),5)
        for row in trace:self.assertEqual(row['swapped'],(row['age']//2)%2==1)
        rows=self.report['part1']['cast_trace']
        self.assertTrue(any(r['tick']==0 and r['puff_alpha']==1 for r in rows))
        self.assertTrue(any(r['tick']==4 and r['puff_alpha']==0 for r in rows))
        self.assertTrue(any(r['tick']==6 and r['floor_alpha']==0 for r in rows))


class CanonicalCapsuleSweepTests(unittest.TestCase):
    def test_emergence_fraction_order_and_temporarily_ignored_body(self):
        project=ROOT/'runs/C-5/t3/FL-2c/reexport'
        probe=project/'capsule_sweep_test.gd'
        probe.write_text(CAPSULE_SWEEP_PROBE)
        result=subprocess.run([GODOT,'--headless','--path',str(project),'--log-file',str(project/'capsule-sweep-engine.log'),'--script','res://capsule_sweep_test.gd'],capture_output=True,text=True,timeout=45)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        rows=json.loads((project/'capsule_sweep_test.json').read_text())
        self.assertEqual([r['body_index'] for r in rows['contacts']],[2,3,1])
        self.assertTrue(rows['near_ignored_initially'])
        self.assertAlmostEqual(rows['radius'],32.5)
        self.assertAlmostEqual(rows['rear_error'],0,delta=.001)
        self.assertAlmostEqual(rows['contacts'][0]['position'][0],rows['height'],delta=.001)
        self.assertEqual([r['position'][0] for r in rows['contacts']],sorted(r['position'][0] for r in rows['contacts']))

CAPSULE_SWEEP_PROBE = r'''extends SceneTree
func _initialize() -> void:
    call_deferred("run")
func run() -> void:
    var world := Node2D.new()
    root.add_child(world)
    var targets: Array = []
    for i in range(3):
        var body := Area2D.new()
        world.add_child(body)
        body.position = Vector2([10,80,220][i],0)
        body.collision_layer = 2
        body.collision_mask = 0
        body.set_meta("body_index",i+1)
        var collision := CollisionShape2D.new()
        var shape := CircleShape2D.new()
        shape.radius = 10.0
        collision.shape = shape
        body.add_child(collision)
        targets.append(body)
    await physics_frame
    await process_frame
    var g1 = load("res://scripts/vfx_g1.gd")
    var keeper = load("res://scripts/keeper.gd")
    var config: Dictionary = keeper.VFX_KITS[9].duplicate(true)
    config.pierce = -1
    var bolt = g1.acquire(world,config,Vector2.ZERO,{"point":Vector2(520,0),"target":null,"kind":"cursor","facing":Vector2.RIGHT},null,1.0)
    bolt.set_physics_process(false)
    var shape = bolt.get_node("CollisionShape2D").shape
    var report = {"radius":shape.radius,"height":shape.height,"rear_error":(bolt.global_position-bolt.direction*shape.height).length()}
    bolt._physics_process(0.0)
    report.near_ignored_initially = not bolt.contacted.has(targets[0].get_instance_id())
    targets[0].position = Vector2(340,0)
    await physics_frame
    await process_frame
    for i in range(30):
        bolt._physics_process(1.0/60.0)
        await physics_frame
        await process_frame
    report.contacts = g1.events.filter(func(e):return e.event == "contact")
    FileAccess.open("res://capsule_sweep_test.json",FileAccess.WRITE).store_string(JSON.stringify(report))
    quit()
'''


FL3_PROBE = r'''extends SceneTree
const G1 = preload("res://scripts/vfx_g1.gd")
const BodyLight = preload("res://scripts/vfx_contact_light.gd")
var report: Dictionary = {"burst":[],"actual_hold_uniforms":[],"actual_ending_visibility":[],"flare":{},"contacts":[]}
func _initialize() -> void: call_deferred("run")
func run() -> void:
    var scene: Node2D = load("res://scenes/main.tscn").instantiate()
    root.add_child(scene)
    var keeper: CharacterBody2D = scene.get_node("Keeper")
    keeper.set_physics_process(false)
    keeper.set_process(false)
    keeper.global_position = Vector2(3760,640)
    keeper.sprite.scale = Vector2.ONE*(130.0/240.0)
    # Same measured shield footprint as FL1_PROBE, now with a modulated sprite
    # and an optional dark duplicate. This is a headless instrument scene.
    var shield := Area2D.new()
    shield.name = "VfxTarget_Shield"
    shield.collision_layer = 2
    shield.collision_mask = 0
    shield.set_meta("body_index",3)
    scene.add_child(shield)
    shield.global_position = Vector2(3911.25,596)
    var polygon := CollisionPolygon2D.new()
    var points := PackedVector2Array()
    for i in range(16): points.append(Vector2(35.2*cos(i*TAU/16),15.4*sin(i*TAU/16)))
    polygon.polygon = points
    shield.add_child(polygon)
    var prop := Sprite2D.new()
    prop.name = "Prop_Shield"
    prop.texture = GradientTexture2D.new()
    prop.texture.width = 100
    prop.texture.height = 151
    prop.modulate = Color(.4,.5,.6,1)
    prop.offset = Vector2(0,-75.5)
    scene.add_child(prop)
    prop.global_position = shield.global_position
    var dark := Sprite2D.new()
    dark.name = "DarkDuplicate"
    dark.texture = prop.texture
    dark.offset = prop.offset
    prop.add_child(dark)
    await physics_frame
    await process_frame
    keeper.state = "idle"
    keeper.facing = "E"
    for i in range(keeper.VFX_KITS.size()):
        if keeper.VFX_KITS[i].name == "fire_bolt_e1_A": keeper.cast_kit_index = i
    keeper.cast_fired = false
    keeper.sprite.animation = "cast_E"
    keeper.sprite.pause()
    keeper.sprite.frame = 3
    keeper.state = "cast"
    keeper.vfx_cursor_override = shield.global_position
    keeper._cast_frame_changed()
    var burst: Node2D
    for tick in range(125):
        for node in scene.get_children():
            if String(node.scene_file_path).ends_with("vfx_fire_burst_e0p_v2_impact.tscn"): burst = node
        if is_instance_valid(burst) and not burst.trace.is_empty():
            if not burst.has_meta("fl3_trace_hook"):
                burst.set_meta("fl3_trace_hook", true)
                var observed: Node2D = burst
                burst.tree_exiting.connect(func(): report.burst = observed.trace.duplicate(true))
            report.burst = burst.trace.duplicate(true)
            var row: Dictionary = burst.trace[-1]
            report.actual_ending_visibility.append({"age":row.age_frames,"art":burst.get_node("Art").is_visible_in_tree(),"core":burst.get_node("Art/Core").is_visible_in_tree(),"shimmer":burst.get_node("Art/HeatShimmer").is_visible_in_tree()})
            var key: String = row.get("key_state", "")
            if key != "":
                var sprite: Sprite2D = burst.get_node("Art/Key_"+key)
                var uv: Vector2 = sprite.material.get_shader_parameter("noise_uv_offset")
                report.actual_hold_uniforms.append({"age":row.age_frames,"key":key,"uv":[uv.x,uv.y],"erode":sprite.material.get_shader_parameter("erode"),"noise_bound":sprite.material.get_shader_parameter("erosion_noise_texture") != null})
                if key == "expanded":
                    var extent: Vector2 = Vector2(sprite.texture.get_image().get_used_rect().size)*sprite.global_scale
                    report.flare = {"extent_px":[extent.x,extent.y],"max_extent_bh":maxf(extent.x,extent.y)/130.0,"dummy_height_bh":1.16,"measurement":"authored alpha extent at expanded hold, global scale; no rendered framebuffer"}
        # One physics clock sample per tick; process-frame waits can skip short holds.
        await physics_frame
    report.contacts = G1.events.filter(func(e): return e.event == "contact")
    report.contact_light = BodyLight.trace
    report.final_modulate = [prop.modulate.r,prop.modulate.g,prop.modulate.b,prop.modulate.a]
    report.final_dark_offset_px = dark.position.length()
    report.live_contact_controllers = get_nodes_in_group("vfx_body_light").size()
    FileAccess.open("res://fl3_trace.json",FileAccess.WRITE).store_string(JSON.stringify(report))
    print("FL3_TRACE_COMPLETE")
    quit()
'''


def fl3_trace(directory, project=None):
    """Trace FL-3 on the shipping Compatibility path, never render a frame."""
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    if project is None:
        fl1_trace(directory/'catalogue')
        project=directory/'catalogue/project'
    project=Path(project)
    (project/'fl3_probe.gd').write_text(FL3_PROBE)
    result=subprocess.run([GODOT,'--headless','--rendering-method','gl_compatibility','--path',str(project),'--log-file',str(directory/'fl3-engine.log'),'--script','res://fl3_probe.gd'],capture_output=True,text=True,timeout=60)
    log=result.stdout+result.stderr
    (directory/'fl3.log').write_text(log)
    if result.returncode or 'SCRIPT ERROR' in log or 'FL3_TRACE_COMPLETE' not in log:raise RuntimeError(log)
    report=json.loads((project/'fl3_trace.json').read_text())
    report['engine_exit']=result.returncode
    return report


# FL-4a headless deterministic clock; no rendering.
FL4_PROBE = 'extends SceneTree\nfunc _initialize() -> void: call_deferred("run")\nfunc run() -> void:\n    var world := Node2D.new()\n    root.add_child(world)\n    var burst = load("res://scenes/vfx_fire_burst_e0p_v2_impact.tscn").instantiate()\n    world.add_child(burst)\n    burst.set_physics_process(false)\n    var actual: Array = []\n    for age in range(115):\n        burst.set_effect_age(age)\n        actual.append({"age":age,"art_visible":burst.get_node("Art").visible,"glow_alpha":burst.ending_glow.modulate.a})\n    var report: Dictionary = {"burst":burst.trace,"births":burst.ending_births,"actual":actual,"travel":{},"trail":{},"smear":{}}\n    var configs: Array = JSON.parse_string(FileAccess.get_file_as_string("res://fl4_configs.json"))\n    for config in configs:\n        var bolt = load(config.bolt).instantiate()\n        world.add_child(bolt)\n        bolt.release(config,Vector2.ZERO,{"kind":"cursor","point":Vector2(520,0),"facing":Vector2.RIGHT})\n        bolt.set_physics_process(false)\n        for age in range(21): bolt._paint_clock(age)\n        report.travel[config.name] = bolt.fire_trace.duplicate(true)\n        var tm = bolt.trail_motes\n        for tick in range(61): tm._tick(tick)\n        report.trail[config.name] = {"births":tm.births,"rate":tm.settings.rate_per_s,"motes":tm.trace.duplicate(true)}\n        tm.emitting = false\n        for tick in range(61,89): tm._tick(tick)\n        var live: int = 0\n        for slot in tm.slots:\n            if slot.live: live += 1\n        report.trail[config.name]["live_at_88"] = live\n        bolt.active = false\n        bolt.stop_age = 20\n        var smear_samples: Array = []\n        for age in range(20,27):\n            bolt._clock_flight_light(age)\n            smear_samples.append({"age_since_stop":age-20,"alpha":bolt.flight_smear.modulate.a,"length":bolt.flight_smear.points[0].distance_to(bolt.flight_smear.points[1])})\n        report.smear[config.name] = smear_samples\n        bolt.cancel()\n    FileAccess.open("res://fl4_trace.json",FileAccess.WRITE).store_string(JSON.stringify(report))\n    print("FL4_TRACE_COMPLETE")\n    quit()\n'


def fl4_trace(directory):
    from export.godot_import import _g1_config
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    project=e1_project_fixture(directory/'fixture')
    configs=[]
    for name in ('fire_bolt_e1_A','fire_bolt_e1_B'):
        kit=_load_vfx_kits(directory/'fixture/kits.json')
        configs.append(_g1_config(next(k for k in kit if k['name']==name)))
    (project/'fl4_configs.json').write_text(json.dumps(configs))
    (project/'fl4_probe.gd').write_text(FL4_PROBE)
    for label,args in [('import',['--editor','--import','--quit']),('trace',['--script','res://fl4_probe.gd'])]:
        proc=subprocess.run([GODOT,'--headless','--rendering-method','gl_compatibility','--path',str(project),'--log-file',str(directory/(label+'-engine.log')),*args],capture_output=True,text=True,timeout=110)
        log=proc.stdout+proc.stderr;(directory/(label+'.log')).write_text(log)
        if proc.returncode or 'SCRIPT ERROR' in log:raise RuntimeError(log)
    return json.loads((project/'fl4_trace.json').read_text())


class FL4BCatalogueTests(unittest.TestCase):
    def test_eighteen_kits_new_b_binding_and_v2_comparison(self):
        kits=_load_vfx_kits(ROOT/'runs/C-5/vfx_kits/kits_v9.json')
        self.assertEqual(len(kits),18)
        names=[k['name'] for k in kits]
        self.assertEqual(len(set(names)),18)
        self.assertEqual(names[-1],'fire_burst_e0p_v3')
        by_name={k['name']:k['effect'] for k in kits}
        self.assertEqual(by_name['fire_bolt_e1_B']['impact_binding']['kit'],'fire_burst_e0p_v3')
        self.assertEqual(by_name['fire_bolt_e1_A']['impact_binding']['kit'],'fire_burst_e0p_v2')
        self.assertEqual(by_name['fire_burst_e0p_v3']['pieces']['key_states'],[])
        self.assertTrue(by_name['fire_burst_e0p_v2']['pieces']['key_states'])


class FL4CByteLockTests(unittest.TestCase):
    def test_fifteen_kits_and_all_fire_art_match_pre_fl5_bytes(self):
        expected=json.loads((ROOT/'fixtures/fl1b/FL4C-source-assets.json').read_text())
        folder=ROOT/'runs/C-5/vfx_kits/v9'
        actual={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                for p in folder.rglob('*') if p.is_file()
                and p not in {folder/name/'kit.json' for name in ('fire_bolt_e1_A','fire_bolt_e1_B','fire_burst_e0p_v3')}}
        self.assertEqual(actual,expected)
        catalogue=json.loads((ROOT/'runs/C-5/vfx_kits/kits_v9.json').read_text())['kits']
        self.assertEqual(len(catalogue),18)
        names={k['name'] for k in catalogue}
        self.assertEqual(sum(k.endswith('/kit.json') and Path(k).parent.name in names for k in actual),15)


class FL5HeadlessContractTests(unittest.TestCase):
    def report(self):
        return json.loads((ROOT/'runs/C-5/t3/FL-5/runtime_trace.json').read_text())
    def test_eruption_ramp_and_socket_tip_all_eight(self):
        r=self.report()
        self.assertEqual(len(r['directions']),8)
        for d in r['directions']:
            self.assertLessEqual(d['tip_error_px'],13)
        rows=r['travel']
        self.assertEqual([x['age'] for x in rows],list(range(13)))
        for x in rows:
            t=min(1,x['age']/8);expected=.25+.75*(1-(1-t)**3)
            self.assertAlmostEqual(x['eruption_scale'],expected,places=5)
            self.assertEqual(x['sheet_visible'],x['age']>=3)
            self.assertLess(x['attachment_error_px'],.001)
        self.assertAlmostEqual(rows[0]['eruption_scale'],.25)
        self.assertLess(rows[7]['eruption_scale'],1)
        self.assertAlmostEqual(rows[8]['eruption_scale'],1)
    def test_residue_smoke_embers_and_seed_parity(self):
        from export.effect_kit import interleave_placement
        r=self.report();rows={x['age_frames']:x for x in r['ending']}
        self.assertEqual(rows[26]['ember_births']<=36,True)
        self.assertAlmostEqual(rows[26]['core_residue_alpha'],1)
        self.assertGreater(rows[40]['core_residue_alpha'],0)
        self.assertAlmostEqual(rows[56]['core_residue_alpha'],0)
        self.assertAlmostEqual(rows[26]['smoke_alpha'],.28,places=5)
        self.assertGreater(rows[40]['smoke_alpha'],rows[56]['smoke_alpha'])
        self.assertAlmostEqual(rows[80]['smoke_alpha'],0)
        self.assertEqual(len(r['births']),36)
        for b in r['births']:
            self.assertLessEqual(abs(b['origin'][0]),65);self.assertLessEqual(abs(b['origin'][1]),32.5)
            self.assertLessEqual(b['end_age'],114)
        self.assertEqual(len(r['seeds']),20)
        for seed in r['seeds']:
            expected=interleave_placement(seed['seed'],r['gaps'],r['library'])
            self.assertEqual([int(x['id']) for x in seed['tongues']],[x['id'] for x in expected])
            for a,b in zip(seed['tongues'],expected):
                self.assertAlmostEqual(a['angle_deg'],b['angle_deg'],places=5)
                self.assertAlmostEqual(a['scale'],b['scale'],places=5)
                self.assertEqual(a['mirrored'],b['mirrored'])
    def test_range_burst_and_shield_hit_response(self):
        r=self.report()
        north=r['north'];shield=r['shield']
        self.assertEqual(north['contacts'],0);self.assertEqual(north['impacts'],1)
        self.assertTrue(north['expired']);self.assertFalse(north['strike_response'])
        self.assertLess(north['range_error_px'],.01)
        self.assertGreater(north['pieces'],0);self.assertEqual(north['ember_births'],36)
        self.assertEqual(shield['contacts'],1);self.assertEqual(shield['impacts'],1)
        self.assertTrue(shield['strike_response']);self.assertEqual(shield['labels'],1)


FL5C_DRAW_ORDER_PROBE = r'''extends SceneTree
func _initialize() -> void: call_deferred("run")
func need(value: bool, label: String) -> void:
    if not value:
        push_error(label)
        quit(1)
func run() -> void:
    var world := Node2D.new()
    world.z_index = 2
    root.add_child(world)
    var actors := Node2D.new()
    actors.z_index = 5
    actors.y_sort_enabled = true
    world.add_child(actors)
    var caster := Node2D.new()
    caster.z_index = 2
    actors.add_child(caster)
    var configs: Array = load("res://scripts/keeper.gd").VFX_KITS
    var kit: Dictionary
    for config in configs:
        if config.name == "fire_bolt_e1_B": kit = config
    var bolt = load(kit.bolt).instantiate()
    actors.add_child(bolt)
    for axis in [Vector2.DOWN,Vector2.UP,Vector2(1,1).normalized(),Vector2.RIGHT]:
        bolt.release(kit,Vector2.ZERO,{"kind":"cursor","point":axis*520,"facing":axis},caster)
        bolt.set_physics_process(false)
        for age in range(13):
            bolt._paint_clock(age)
            var boosted: bool = axis.y > 0 and age <= 10
            need(bolt._effective_z(bolt)==(10 if boosted else 7),"effective actor z / 10-to-11 boundary")
            need(bolt.z_as_relative != boosted,"normal relative sort restoration")
    # Reuse before the previous override naturally expires.
    bolt.release(kit,Vector2.ZERO,{"kind":"cursor","point":Vector2(0,520),"facing":Vector2.DOWN},caster)
    bolt.release(kit,Vector2.ZERO,{"kind":"cursor","point":Vector2(0,-520),"facing":Vector2.UP},caster)
    need(bolt.z_index==0 and bolt.z_as_relative,"pooled release retained south z")
    bolt.release(kit,Vector2.ZERO,{"kind":"cursor","point":Vector2(0,520),"facing":Vector2.DOWN})
    need(bolt.z_index==0 and bolt.z_as_relative,"ownerless release inherited override")
    print("FL5C_DRAW_ORDER_COMPLETE")
    quit()
'''
