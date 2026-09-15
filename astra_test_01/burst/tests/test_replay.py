from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image

from export.godot_import import build_project
from export.replay import (BAKE_HOOK, PROBE, compare_bakes, compare_vo1,
                           background_comparisons, diagnose, install_hooks, movie_command, prepare_project,
                           replay_to_frame, run_replay, scene_pixel_probe)


class ReplayTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).parent / 'tmp'
        root.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=root)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def sequence(self, name, count=3, color=(0, 0, 0, 0)):
        root = self.root / name
        root.mkdir()
        for index in range(count):
            Image.new('RGBA', (8, 8), color).save(root / f'fx{index:05}.png')
        return root

    def test_identical_and_known_bad_frame(self):
        a, b = self.sequence('a'), self.sequence('b')
        self.assertEqual(compare_bakes(a, b)['result']['value'], 0)
        path = b / 'fx00001.png'
        with Image.open(path) as im:
            im.putpixel((2, 2), (255, 0, 0, 255))
            im.save(path)
        result = compare_bakes(a, b)
        self.assertEqual(result['result']['value'], 1)
        self.assertEqual(result['frames'][1]['different_pixels'], 1)
        self.assertFalse(result['result']['passed'])

    def test_missing_frame_is_not_identical(self):
        result = compare_bakes(self.sequence('a', 3), self.sequence('b', 2))
        self.assertEqual(result['result']['value'], 1)

    def test_shifted_numbering_is_not_identical(self):
        a, b = self.sequence('a', 1), self.sequence('b', 1)
        (b / 'fx00000.png').rename(b / 'fx00001.png')
        self.assertEqual(compare_bakes(a, b)['result']['value'], 1)

    def test_byte_identity_not_only_decoded_pixels(self):
        from PIL.PngImagePlugin import PngInfo
        a, b = self.sequence('a', 1), self.sequence('b', 1)
        info = PngInfo()
        info.add_text('different', 'encoding')
        Image.new('RGBA', (8, 8)).save(b / 'fx00000.png', pnginfo=info)
        result = compare_bakes(a, b)
        self.assertEqual(result['result']['value'], 1)
        self.assertEqual(result['frames'][0]['different_pixels'], 0)

    def test_scene_pixels_known_bad(self):
        blank = self.sequence('blank')
        self.assertEqual(scene_pixel_probe(blank)['value'], 0)
        Image.new('RGBA', (8, 8), (60, 70, 80, 255)).save(blank / 'fx00001.png')
        result = scene_pixel_probe(blank)
        self.assertEqual(result['value'], 64)
        self.assertFalse(result['passed'])
        Image.new('RGB', (8, 8)).save(blank / 'fx00001.png')
        with self.assertRaises(ValueError):
            scene_pixel_probe(blank)

    def test_vo1_every_background_every_frame(self):
        live = {name: [10, 0, 100] for name in ('ground', 'black', 'white', 'foliage')}
        baked = {name: [10.5, 0, 106] for name in live}
        rows = compare_vo1(live, baked)
        self.assertEqual(len(rows), 12)
        self.assertEqual(sum(r['passed'] is False for r in rows), 4)
        self.assertTrue(all(r['passed'] is None for r in compare_vo1(live, baked, committed=False)))
        baked['black'][1] = 1
        self.assertFalse(compare_vo1(live, baked)[1]['passed'])
        baked['black'][0] = None
        self.assertIsNone(compare_vo1(live, baked)[0]['passed'])

    def test_vo1_invalid_alignment(self):
        with self.assertRaises(ValueError):
            compare_vo1({}, {})
        live = {name: [1] for name in ('ground', 'black', 'white', 'foliage')}
        with self.assertRaises(ValueError):
            compare_vo1(live, {**live, 'white': []})

    def test_movie_recipe_native_and_fixed(self):
        command = movie_command(self.root, self.root / 'bake')
        self.assertEqual(command[command.index('--fixed-fps') + 1], '60')
        self.assertTrue(command[command.index('--write-movie') + 1].endswith('/fx.png'))
        self.assertNotIn('--headless', command)
        with self.assertRaises(ValueError):
            movie_command(self.root, self.root, 0)

    def project(self):
        source = self.root / 'source'
        source.mkdir()
        (source / 'project.godot').write_text('config_version=5\n[application]\nrun/main_scene="res://main.tscn"\n[display]\nwindow/size/viewport_width=1920\nwindow/size/viewport_height=1080\n[rendering]\n')
        (source / 'main.tscn').write_text('[gd_scene format=3]\n[node name="Main" type="Node2D"]\n')
        return source

    def test_copy_preserves_source_and_installs_visibility(self):
        source = self.project()
        original = (source / 'project.godot').read_bytes()
        output = prepare_project(source, self.root / 'copy', (320, 256))
        self.assertEqual((source / 'project.godot').read_bytes(), original)
        settings = (output / 'project.godot').read_text()
        self.assertIn('viewport_width=320', settings)
        self.assertIn('viewport_height=256', settings)
        self.assertIn('viewport/transparent_background=true', settings)
        self.assertIn('common/physics_ticks_per_second=60', settings)
        self.assertTrue((output / 'replay_probe.gd').exists())
        with self.assertRaises(ValueError):
            prepare_project(source, output)
        with self.assertRaises(ValueError):
            prepare_project(source, source / 'nested')
        with self.assertRaises(ValueError):
            install_hooks(output, (1920, 1080))

    def test_legacy_export_unchanged_by_default(self):
        cells = self.root / 'cells'
        cells.mkdir()
        Image.new('RGBA', (512, 512)).save(cells / 'idle_S_0.png')
        a, b, c = (self.root / n for n in ('default', 'false', 'bake'))
        build_project(cells, a)
        build_project(cells, b, bake=False)
        build_project(cells, c, bake=True)
        for path in a.rglob('*'):
            if path.is_file():
                self.assertEqual(path.read_bytes(), (b / path.relative_to(a)).read_bytes())
        self.assertFalse((a / 'replay_probe.gd').exists())
        self.assertIn('viewport_width=512', (c / 'project.godot').read_text())
        with self.assertRaises(ValueError):
            build_project(cells, self.root / 'invalid', bake='yes')

    def test_reset_to_frame_validation_and_forwarding(self):
        with patch('export.replay.run_replay', return_value={'frame': 9}) as run:
            self.assertEqual(replay_to_frame('p', 'out', 9, seed=2), {'frame': 9})
            run.assert_called_once_with('p', 'out', frame=9, seed=2)
        for kwargs in ({'frame': -1}, {'seed': True}, {'crop': (513, 512)}, {'bake': 'yes'}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                run_replay(self.root, self.root / 'out', **kwargs)

    def test_four_backgrounds_use_independent_live_and_flipbook(self):
        with patch('export.replay.run_replay', return_value={}) as run:
            results = background_comparisons('project', self.root, 'baked', 'foliage.png', seed=4)
        self.assertEqual(set(results), {'ground', 'black', 'white', 'foliage'})
        self.assertEqual(run.call_count, 8)
        self.assertEqual(sum(c.kwargs['flipbook'] is not None for c in run.call_args_list), 4)
        self.assertTrue(all(c.kwargs['bake'] is False for c in run.call_args_list))

    def test_reject_bad_comparison_canvas(self):
        paths = self.sequence('frames')
        for kwargs in ({'background': 'unknown'}, {'background': 'foliage'},
                       {'flipbook': paths, 'bake': False, 'frames': 3},
                       {'probe_only': 'yes'}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                run_replay(self.root, self.root / 'out', **kwargs)

    def test_diagnosis_reports_source_not_verdict(self):
        source = self.project()
        (source / 'effect.tscn').write_text('[node name="Particles" type="CPUParticles2D"]\n')
        (source / 'effect.gdshader').write_text('float clock = TIME;\n')
        kinds = {r['kind'] for r in diagnose(source)}
        self.assertEqual(kinds, {'cpu_particles', 'wall_clock'})


if __name__ == '__main__':
    unittest.main()
