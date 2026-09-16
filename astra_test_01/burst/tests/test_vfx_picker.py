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
        result = subprocess.run([GODOT, '--headless', '--log-file', str(project/'godot.log'),
                                 '--path', str(project), *args],
                                capture_output=True, text=True, timeout=60)
        log = result.stdout+result.stderr
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
        for token in ('area_entered.connect', 'space.cast_motion(query)', '"release"', '"contact"', '"expire"', '"cancel"'):
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
        baseline = json.loads((ARTIFACTS/'baseline_t3m_text_sha256.json').read_text())
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
        bolt._on_area_entered(target)
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
    check(bolt.global_position.distance_to(keeper._socket_world()) < 0.001, "staff socket")
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
    inflight.resolved.target = target
    inflight.resolved.kind = "prop"
    inflight._on_area_entered(target)
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
        temporary = ROOT/'runs/C-5/t3/T4i/tmp'
        temporary.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='touch-aim-', dir=temporary) as directory:
            root = Path(directory)
            cells, sockets, kits, _ = fixture_inputs(root/'inputs')
            project = root/'project'
            build_project(cells, project, sockets=sockets, vfx_kits=kits)
            (project/'touch_aim_probe.gd').write_text(TOUCH_AIM_PROBE)
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
