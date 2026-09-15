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
TMP = ARTIFACTS/'tmp'
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
            for kind in ('bolt', 'impact'):
                self.assertTrue((out/f'scenes/vfx_{name}_{kind}.tscn').is_file())
            bolt = (out/f'scripts/vfx_{name}_bolt.gd').read_text()
            self.assertIn(f'preload("res://scenes/vfx_{name}_impact.tscn")', bolt)
            for token in ('520.0 * spell_scale', '650.0 * spell_scale', 'intersect_ray(query)',
                          'body is StaticBody2D', '$Trail.direction = -direction'):
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
                      'load(VFX_KITS[cast_kit_index]["bolt"])'):
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
        default = (out/'scenes/vfx_zeta_bolt.tscn').read_text()
        self.assertIn(RADIAL_RESOURCES, default)
        tinted = (out/'scenes/vfx_alpha_bolt.tscn').read_text()
        for row in re.findall(r'colors = PackedColorArray\(([^)]+)\)', tinted):
            values = [float(v) for v in row.split(',')]
            self.assertEqual([values[i:i+3] for i in range(0, len(values), 4)], [[1, .2, .05]]*3)
        self.assertIn('1, 0.2, 0.05, 0.7', tinted)
        self.assertIn('1, 0.2, 0.05, 0.8', tinted)

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
        for relative in ('scenes/vfx_frost_bolt.tscn', 'scenes/vfx_frost_impact.tscn',
                         'scripts/vfx_frost_bolt.gd', 'scripts/vfx_frost_impact.gd',
                         'vfx/frost/flare.tres', 'vfx/frost/impact.tres'):
            self.assertEqual((legacy/relative).read_bytes(), (self.project/relative).read_bytes(), relative)
        self.assertEqual((self.project/'scenes/vfx_frost_bolt.tscn').read_bytes(),
                         (ROOT/'runs/C-3/cliffside_v10/scenes/vfx_frost_bolt.tscn').read_bytes())
        self.assertEqual((self.project/'scripts/vfx_frost_bolt.gd').read_text(),
                         BOLT_SCRIPT.replace('scenes/frost_impact.tscn', 'scenes/vfx_frost_impact.tscn'))
        self.assertEqual((self.project/'scripts/vfx_frost_impact.gd').read_text(), IMPACT_SCRIPT)

    def test_authored_kit_own_travel_durations_layers_and_feedback_parameters(self):
        project = self.project
        for kind in ('bolt', 'impact'):
            scene = (project/f'scenes/vfx_synthetic_ice_{kind}.tscn').read_text()
            for name in ('DarkDuplicate', 'Glow', 'FloorLight', 'Flash', 'Decal', 'Particles'):
                self.assertIn(f'[node name="{name}"', scene)
            for token in ('blend_mode = 1', 'blend_mode = 0', 'hitstop_duration = 0.08',
                          'hitstop_time_scale = 0.1', 'shake_distance = 3', 'shake_duration = 0.12',
                          'ground_squash = 0.6', 'texture_filter = 1'):
                self.assertIn(token, scene)
            script = (project/f'scripts/vfx_synthetic_ice_{kind}.gd').read_text()
            for token in ('Engine.time_scale = hitstop_time_scale', 'camera.offset = baseline',
                          '"modulate:a", 0.0, FLOOR_DURATION', '"scale", Vector2.ONE * FLASH_TO',
                          '"modulate:a", 0.0, DECAL_DURATION', 'set_ignore_time_scale(true)'):
                self.assertIn(token, script)
        bolt = (project/'scenes/vfx_synthetic_ice_bolt.tscn').read_text()
        self.assertIn('res://vfx/synthetic_ice/travel.tres', bolt)
        self.assertIn('speed_px_s = 360', bolt)
        self.assertIn('[node name="Streak"', bolt)
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
        text = (out/'scenes/vfx_minimal_bolt.tscn').read_text()
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
        keeper.sprite.play("cast_" + facing)
        keeper.sprite.pause()
        keeper.sprite.frame = 2
        check(keeper.cast_fired, "socket release " + facing)
        var bolt: Area2D = scene.get_child(scene.get_child_count()-1)
        bolt.set_physics_process(false)
        check(bolt.scene_file_path == "res://scenes/vfx_synthetic_ice_bolt.tscn", "authored bolt")
        var travel: AnimatedSprite2D = bolt.get_node("Ground/Travel")
        var angle: float = 0.0 if facing == "E" else -90.0
        angles.append(travel.rotation_degrees)
        check(absf(travel.rotation_degrees-angle) < 0.001, "travel rotation")
        check(bolt.get_node("Ground").scale.is_equal_approx(Vector2(1,0.6)), "ground squash")
        check(travel.sprite_frames.resource_path == "res://vfx/synthetic_ice/travel.tres", "own travel")
        check(is_equal_approx(travel.sprite_frames.get_frame_duration("travel",0) / travel.sprite_frames.get_animation_speed("travel"), 2.0/60.0), "first hold")
        check(is_equal_approx(travel.sprite_frames.get_frame_duration("travel",1), 5.0/60.0), "second hold")
        check(bolt.get_node("Ground/Glow").material.blend_mode == CanvasItemMaterial.BLEND_MODE_ADD, "additive glow")
        check(bolt.get_node("Ground/DarkDuplicate").material.blend_mode == CanvasItemMaterial.BLEND_MODE_MIX, "mix duplicate")
        check(bolt.get_node("Ground/DarkDuplicate").modulate == Color.BLACK, "black duplicate")
        var old_position: Vector2 = bolt.position
        bolt._physics_process(0.01)
        check(is_equal_approx(bolt.position.distance_to(old_position), 3.6), "authored speed")
        bolt._on_body_entered(keeper)
        check(not bolt.expired, "caster ignored")
        var wall := StaticBody2D.new()
        scene.add_child(wall)
        bolt._on_body_entered(wall)
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
    keeper.sprite.frame = 2
    check(keeper.cast_fired, "released at socket frame two")
    var bolt: Area2D = scene.get_child(scene.get_child_count()-1)
    bolt.set_physics_process(false)
    check(bolt.global_position.distance_to(keeper._socket_world()) < 0.001, "staff socket")
    check(bolt.direction == Vector2.DOWN, "direction retained")
    return bolt
func probe() -> void:
    scene = load("res://scenes/main.tscn").instantiate()
    root.add_child(scene)
    await process_frame
    keeper = scene.get_node("Keeper")
    keeper.set_physics_process(false)
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
        check(bolt.scene_file_path == "res://scenes/vfx_"+expected+"_bolt.tscn", "cycled bolt " + expected)
        var flare: AnimatedSprite2D = keeper.active_flare
        check(flare.sprite_frames.resource_path == "res://vfx/"+expected+"/flare.tres", "matching flare")
        bolt._physics_process(10.0)
        check(bolt.expired and is_equal_approx(bolt.distance, 650.0), "range impact")
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
    check(inflight.scene_file_path == "res://scenes/vfx_zeta_bolt.tscn", "pre-release kit lock")
    await process_frame
    tab()
    inflight._on_body_entered(keeper)
    check(not inflight.expired, "ignore caster collision")
    var wall := StaticBody2D.new()
    scene.add_child(wall)
    inflight._on_body_entered(wall)
    check(inflight.expired, "static collision")
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
